"""到期提醒任务

提供各种到期提醒功能：
- 合同到期提醒
- 课时不足提醒
- 排课提醒（上课前N小时）
- 生日祝福
"""
import logging
from datetime import datetime, date, timedelta
from typing import List, Optional
from decimal import Decimal

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contract import Contract
from app.models.student import Student
from app.models.schedule import Schedule
from app.models.notification import Notification
from app.models.attendance import Attendance
from app.core.db import async_session_maker
from app.core.wework import wework_service


logger = logging.getLogger(__name__)


# ==================== 配置常量 ====================

# 合同到期提前提醒天数（默认30天）
DEFAULT_CONTRACT_WARNING_DAYS = 30

# 课时不足阈值（默认4课时）
DEFAULT_LOW_HOURS_THRESHOLD = Decimal("4.0")

# 排课提前提醒小时数（默认2小时）
DEFAULT_CLASS_REMINDER_HOURS = 2

# 生日祝福发送时间（默认早上9点）
BIRTHDAY_GREETING_HOUR = 9


# ==================== 合同到期提醒 ====================

async def check_contract_expiry_reminders(
    warning_days: int = DEFAULT_CONTRACT_WARNING_DAYS,
    low_hours_threshold: Decimal = DEFAULT_LOW_HOURS_THRESHOLD
) -> dict:
    """
    检查合同到期提醒和课时不足提醒

    Args:
        warning_days: 到期预警天数
        low_hours_threshold: 课时不足阈值

    Returns:
        dict: 提醒统计信息
            - expiry_reminders: 到期提醒数量
            - low_hours_reminders: 课时不足提醒数量
            - total: 总提醒数量
    """
    logger.info(f"开始检查合同到期提醒: warning_days={warning_days}, low_hours_threshold={low_hours_threshold}")

    async with async_session_maker() as session:
        today = date.today()
        warning_date = today + timedelta(days=warning_days)

        # 查询即将到期的生效合同
        expiry_query = select(Contract).where(
            and_(
                Contract.status == 1,  # 生效状态
                Contract.end_date.isnot(None),
                Contract.end_date <= warning_date,
                Contract.end_date >= today
            )
        )

        result = await session.execute(expiry_query)
        expiring_contracts = result.scalars().all()

        # 查询课时不足的生效合同
        low_hours_query = select(Contract).where(
            and_(
                Contract.status == 1,  # 生效状态
                Contract.remaining_hours < low_hours_threshold
            )
        )

        result = await session.execute(low_hours_query)
        low_hours_contracts = result.scalars().all()

        # 发送提醒
        expiry_count = 0
        low_hours_count = 0

        for contract in expiring_contracts:
            try:
                await _send_contract_expiry_reminder(session, contract, warning_days)
                expiry_count += 1
            except Exception as e:
                logger.error(f"发送合同到期提醒失败: contract_id={contract.id}, error={e}")

        for contract in low_hours_contracts:
            try:
                await _send_low_hours_reminder(session, contract, low_hours_threshold)
                low_hours_count += 1
            except Exception as e:
                logger.error(f"发送课时不足提醒失败: contract_id={contract.id}, error={e}")

        await session.commit()

        total = expiry_count + low_hours_count
        logger.info(f"合同到期提醒完成: 到期提醒={expiry_count}, 课时不足提醒={low_hours_count}, 总计={total}")

        return {
            "expiry_reminders": expiry_count,
            "low_hours_reminders": low_hours_count,
            "total": total
        }


async def _send_contract_expiry_reminder(
    session: AsyncSession,
    contract: Contract,
    warning_days: int
) -> None:
    """
    发送合同到期提醒

    Args:
        session: 数据库会话
        contract: 合同对象
        warning_days: 预警天数
    """
    # 获取学员信息
    student = await session.get(Student, contract.student_id)
    if not student or not student.parent_wework_id:
        logger.warning(f"学员或家长企业微信ID不存在: student_id={contract.student_id}")
        return

    days_remaining = (contract.end_date - date.today()).days
    remaining_value = contract.unit_price * contract.remaining_hours

    # 构建提醒消息
    title = "合同即将到期提醒"
    content = (
        f"尊敬的{student.parent_name}家长，您好！\n\n"
        f"您孩子的合同《{contract.contract_no}》即将到期。\n\n"
        f"📅 到期时间：{contract.end_date}\n"
        f"⏰ 剩余天数：{days_remaining}天\n"
        f"📚 剩余课时：{contract.remaining_hours}课时\n"
        f"💰 剩余价值：¥{remaining_value:.2f}\n\n"
        f"请您及时联系课程顾问续费，以免影响孩子的学习进度。\n"
        f"如有疑问，请随时联系我们。"
    )

    # 发送企业微信消息
    try:
        response = await wework_service.send_message(
            user_id=student.parent_wework_id,
            content=content
        )

        if response.get("errcode") == 0:
            logger.info(f"合同到期提醒发送成功: contract_id={contract.id}, user={student.parent_wework_id}")

            # 记录通知
            await _create_notification(
                session=session,
                receiver_id=student.parent_wework_id,
                receiver_type=1,  # 企业微信
                notification_type=4,  # 合同通知
                title=title,
                content=content,
                status=1  # 已发送
            )
        else:
            logger.error(f"企业微信消息发送失败: {response}")
            await _create_notification(
                session=session,
                receiver_id=student.parent_wework_id,
                receiver_type=1,
                notification_type=4,
                title=title,
                content=content,
                status=2,  # 发送失败
                error_msg=str(response)
            )
    except Exception as e:
        logger.error(f"发送企业微信消息异常: {e}")
        await _create_notification(
            session=session,
            receiver_id=student.parent_wework_id,
            receiver_type=1,
            notification_type=4,
            title=title,
            content=content,
            status=2,
            error_msg=str(e)
        )


async def _send_low_hours_reminder(
    session: AsyncSession,
    contract: Contract,
    threshold: Decimal
) -> None:
    """
    发送课时不足提醒

    Args:
        session: 数据库会话
        contract: 合同对象
        threshold: 课时阈值
    """
    # 获取学员信息
    student = await session.get(Student, contract.student_id)
    if not student or not student.parent_wework_id:
        logger.warning(f"学员或家长企业微信ID不存在: student_id={contract.student_id}")
        return

    remaining_value = contract.unit_price * contract.remaining_hours
    usage_percentage = ((contract.total_hours - contract.remaining_hours) / contract.total_hours * 100) if contract.total_hours > 0 else 0

    # 构建提醒消息
    title = "课时不足提醒"
    content = (
        f"尊敬的{student.parent_name}家长，您好！\n\n"
        f"您孩子的课时即将用完。\n\n"
        f"📚 合同编号：{contract.contract_no}\n"
        f"📊 总课时：{contract.total_hours}课时\n"
        f"📉 剩余课时：{contract.remaining_hours}课时\n"
        f"💰 剩余价值：¥{remaining_value:.2f}\n"
        f"📈 已用比例：{usage_percentage:.1f}%\n\n"
        f"请您及时联系课程顾问续费，以免影响孩子的学习进度。\n"
        f"如有疑问，请随时联系我们。"
    )

    # 发送企业微信消息
    try:
        response = await wework_service.send_message(
            user_id=student.parent_wework_id,
            content=content
        )

        if response.get("errcode") == 0:
            logger.info(f"课时不足提醒发送成功: contract_id={contract.id}, user={student.parent_wework_id}")

            # 记录通知
            await _create_notification(
                session=session,
                receiver_id=student.parent_wework_id,
                receiver_type=1,
                notification_type=4,
                title=title,
                content=content,
                status=1
            )
        else:
            logger.error(f"企业微信消息发送失败: {response}")
            await _create_notification(
                session=session,
                receiver_id=student.parent_wework_id,
                receiver_type=1,
                notification_type=4,
                title=title,
                content=content,
                status=2,
                error_msg=str(response)
            )
    except Exception as e:
        logger.error(f"发送企业微信消息异常: {e}")
        await _create_notification(
            session=session,
            receiver_id=student.parent_wework_id,
            receiver_type=1,
            notification_type=4,
            title=title,
            content=content,
            status=2,
            error_msg=str(e)
        )


# ==================== 排课提醒 ====================

async def check_class_reminders(
    reminder_hours: int = DEFAULT_CLASS_REMINDER_HOURS
) -> dict:
    """
    检查排课提醒（上课前N小时）

    Args:
        reminder_hours: 提前提醒小时数

    Returns:
        dict: 提醒统计信息
            - reminders_sent: 发送提醒数量
            - students: 提醒学员数量
    """
    logger.info(f"开始检查排课提醒: reminder_hours={reminder_hours}小时")

    async with async_session_maker() as session:
        now = datetime.now()
        reminder_time = now + timedelta(hours=reminder_hours)

        # 查询在提醒时间窗口内的排课
        start_window = reminder_time - timedelta(minutes=30)
        end_window = reminder_time + timedelta(minutes=30)

        schedules_query = select(Schedule).where(
            and_(
                Schedule.status == 1,  # 已安排
                Schedule.start_time >= start_window,
                Schedule.start_time <= end_window
            )
        )

        result = await session.execute(schedules_query)
        schedules = result.scalars().all()

        reminders_sent = 0
        students_reminded = set()

        for schedule in schedules:
            try:
                # 查询该排课的所有考勤记录
                attendances_query = select(Attendance).where(
                    and_(
                        Attendance.schedule_id == schedule.id,
                    )
                )

                result = await session.execute(attendances_query)
                attendances = result.scalars().all()

                for attendance in attendances:
                    # 获取学员信息
                    student = await session.get(Student, attendance.student_id)
                    if not student or not student.parent_wework_id:
                        continue

                    # 发送上课提醒
                    await _send_class_reminder(session, schedule, student, reminder_hours)
                    reminders_sent += 1
                    students_reminded.add(student.id)

            except Exception as e:
                logger.error(f"发送排课提醒失败: schedule_id={schedule.id}, error={e}")

        await session.commit()

        logger.info(f"排课提醒完成: 提醒数量={reminders_sent}, 学员数量={len(students_reminded)}")

        return {
            "reminders_sent": reminders_sent,
            "students": len(students_reminded)
        }


async def _send_class_reminder(
    session: AsyncSession,
    schedule: Schedule,
    student: Student,
    reminder_hours: int
) -> None:
    """
    发送上课提醒

    Args:
        session: 数据库会话
        schedule: 排课对象
        student: 学员对象
        reminder_hours: 提前小时数
    """
    # 获取课程信息
    from app.models.course import Course
    course = await session.get(Course, schedule.course_id)

    # 获取教师信息
    from app.models.user import User
    teacher = await session.get(User, schedule.teacher_id)

    # 构建提醒消息
    title = "上课提醒"
    content = (
        f"尊敬的{student.parent_name}家长，您好！\n\n"
        f"提醒您孩子{reminder_hours}小时后有课程安排。\n\n"
        f"📚 课程：{course.name if course else '未知'}\n"
        f"👨‍🏫 教师：{teacher.name if teacher else '未知'}\n"
        f"🕐 上课时间：{schedule.start_time.strftime('%Y-%m-%d %H:%M')}\n"
        f"🕐 结束时间：{schedule.end_time.strftime('%H:%M')}\n\n"
        f"请提前安排好时间，确保准时参加课程。\n"
        f"如有疑问，请随时联系我们。"
    )

    # 发送企业微信消息
    try:
        response = await wework_service.send_message(
            user_id=student.parent_wework_id,
            content=content
        )

        if response.get("errcode") == 0:
            logger.info(f"上课提醒发送成功: schedule_id={schedule.id}, student_id={student.id}")

            # 记录通知
            await _create_notification(
                session=session,
                receiver_id=student.parent_wework_id,
                receiver_type=1,
                notification_type=1,  # 上课提醒
                title=title,
                content=content,
                status=1
            )
        else:
            logger.error(f"企业微信消息发送失败: {response}")
    except Exception as e:
        logger.error(f"发送企业微信消息异常: {e}")


# ==================== 生日祝福 ====================

async def send_birthday_greetings(
    greeting_hour: int = BIRTHDAY_GREETING_HOUR
) -> dict:
    """
    发送生日祝福（学员生日当天）

    Args:
        greeting_hour: 发送时间（小时）

    Returns:
        dict: 发送统计信息
            - greetings_sent: 发送数量
    """
    logger.info(f"开始检查生日祝福: greeting_hour={greeting_hour}")

    async with async_session_maker() as session:
        now = datetime.now()

        # 只在指定时间运行
        if now.hour != greeting_hour:
            logger.info(f"当前时间不在发送窗口内: {now.hour} != {greeting_hour}")
            return {"greetings_sent": 0}

        today = now.date()

        # 查询今天生日的学员
        birthday_query = select(Student).where(
            and_(
                Student.birthday.isnot(None),
                # 提取月日进行比较
                Student.birthday.between(
                    date(1900, today.month, today.day),
                    date(1900, today.month, today.day)
                )
            )
        )

        result = await session.execute(birthday_query)
        birthday_students = result.scalars().all()

        greetings_sent = 0

        for student in birthday_students:
            try:
                if not student.parent_wework_id:
                    logger.warning(f"学员家长企业微信ID不存在: student_id={student.id}")
                    continue

                # 计算年龄
                age = today.year - student.birthday.year - (
                    (today.month, today.day) < (student.birthday.month, student.birthday.day)
                )

                # 发送生日祝福
                await _send_birthday_greeting(session, student, age)
                greetings_sent += 1

            except Exception as e:
                logger.error(f"发送生日祝福失败: student_id={student.id}, error={e}")

        await session.commit()

        logger.info(f"生日祝福完成: 发送数量={greetings_sent}")

        return {"greetings_sent": greetings_sent}


async def _send_birthday_greeting(
    session: AsyncSession,
    student: Student,
    age: int
) -> None:
    """
    发送生日祝福

    Args:
        session: 数据库会话
        student: 学员对象
        age: 年龄
    """
    # 构建祝福消息
    title = "生日祝福"
    content = (
        f"🎂 生日快乐 🎂\n\n"
        f"亲爱的{student.name}小朋友，祝你{age}岁生日快乐！\n\n"
        f"愿你在新的一岁里：\n"
        f"✨ 学习进步，快乐成长\n"
        f"✨ 身体健康，天天开心\n"
        f"✨ 梦想成真，前程似锦\n\n"
        f"我们很荣幸能陪伴你的学习旅程！\n"
        f"继续加油，未来可期！🌟"
    )

    # 发送企业微信消息
    try:
        response = await wework_service.send_message(
            user_id=student.parent_wework_id,
            content=content
        )

        if response.get("errcode") == 0:
            logger.info(f"生日祝福发送成功: student_id={student.id}, user={student.parent_wework_id}")

            # 记录通知
            await _create_notification(
                session=session,
                receiver_id=student.parent_wework_id,
                receiver_type=1,
                notification_type=5,  # 系统通知
                title=title,
                content=content,
                status=1
            )
        else:
            logger.error(f"企业微信消息发送失败: {response}")
    except Exception as e:
        logger.error(f"发送企业微信消息异常: {e}")


# ==================== 通知记录 ====================

async def _create_notification(
    session: AsyncSession,
    receiver_id: str,
    receiver_type: int,
    notification_type: int,
    title: str,
    content: str,
    status: int,
    url: Optional[str] = None,
    error_msg: Optional[str] = None
) -> Notification:
    """
    创建通知记录

    Args:
        session: 数据库会话
        receiver_id: 接收者ID
        receiver_type: 接收者类型 (1:企业微信 2:家长 3:小程序)
        notification_type: 通知类型 (1:上课提醒 2:作业通知 3:考勤通知 4:合同通知 5:系统通知)
        title: 标题
        content: 内容
        status: 状态 (0:pending 1:sent 2:failed 3:read)
        url: 跳转链接
        error_msg: 错误信息

    Returns:
        Notification: 创建的通知对象
    """
    notification = Notification(
        type=notification_type,
        receiver_id=receiver_id,
        receiver_type=receiver_type,
        title=title,
        content=content,
        url=url,
        sent_at=datetime.now() if status == 1 else None,
        status=status,
        error_msg=error_msg,
        created_at=datetime.now()
    )

    session.add(notification)
    return notification
