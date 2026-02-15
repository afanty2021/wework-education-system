"""统计数据汇总任务

提供每日统计数据汇总功能：
- 每日汇总考勤统计
- 每日汇总缴费统计
- 每日汇总合同统计
- 存储历史统计数据
"""
import logging
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional
from decimal import Decimal

from sqlalchemy import select, and_, func, case, literal_column
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attendance import Attendance
from app.models.payment import Payment, Refund
from app.models.contract import Contract
from app.models.student import Student
from app.models.schedule import Schedule
from app.core.db import async_session_maker


logger = logging.getLogger(__name__)


# ==================== 考勤统计汇总 ====================

async def summarize_daily_attendance(target_date: Optional[date] = None) -> Dict[str, Any]:
    """
    每日汇总考勤统计

    Args:
        target_date: 目标日期，默认为昨天

    Returns:
        dict: 考勤统计信息
            - date: 统计日期
            - total_classes: 总课程数
            - total_attendance: 总出勤数
            - present: 出勤数
            - leave: 请假数
            - absent: 缺勤数
            - late: 迟到数
            - attendance_rate: 出勤率
            - by_course: 按课程分组的统计
    """
    if target_date is None:
        target_date = date.today() - timedelta(days=1)

    logger.info(f"开始汇总考勤统计: date={target_date}")

    async with async_session_maker() as session:
        # 定义时间范围
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = datetime.combine(target_date, datetime.max.time())

        # 查询当天的考勤记录
        attendance_query = select(Attendance).where(
            and_(
                Attendance.created_at >= start_datetime,
                Attendance.created_at <= end_datetime
            )
        )

        result = await session.execute(attendance_query)
        attendances = result.scalars().all()

        # 统计各种状态
        present = sum(1 for a in attendances if a.status == 1)  # 出勤
        leave = sum(1 for a in attendances if a.status == 2)    # 请假
        absent = sum(1 for a in attendances if a.status == 3)   # 缺勤
        late = sum(1 for a in attendances if a.status == 4)     # 迟到

        total_attendance = len(attendances)

        # 计算出勤率（出勤+迟到）/总数
        attendance_rate = (present + late) / total_attendance * 100 if total_attendance > 0 else 0

        # 按课程分组统计
        from app.models.course import Course
        by_course: Dict[int, Dict[str, Any]] = {}

        for attendance in attendances:
            # 获取排课信息
            schedule = await session.get(Schedule, attendance.schedule_id)
            if not schedule:
                continue

            course_id = schedule.course_id

            if course_id not in by_course:
                by_course[course_id] = {
                    "course_name": "",
                    "total": 0,
                    "present": 0,
                    "leave": 0,
                    "absent": 0,
                    "late": 0
                }

            # 获取课程名称
            if not by_course[course_id]["course_name"]:
                course = await session.get(Course, course_id)
                if course:
                    by_course[course_id]["course_name"] = course.name

            by_course[course_id]["total"] += 1

            if attendance.status == 1:
                by_course[course_id]["present"] += 1
            elif attendance.status == 2:
                by_course[course_id]["leave"] += 1
            elif attendance.status == 3:
                by_course[course_id]["absent"] += 1
            elif attendance.status == 4:
                by_course[course_id]["late"] += 1

        # 查询当天排课数
        schedule_query = select(Schedule).where(
            and_(
                Schedule.start_time >= start_datetime,
                Schedule.start_time <= end_datetime
            )
        )

        result = await session.execute(schedule_query)
        schedules = result.scalars().all()
        total_classes = len(schedules)

        summary = {
            "date": target_date.isoformat(),
            "total_classes": total_classes,
            "total_attendance": total_attendance,
            "present": present,
            "leave": leave,
            "absent": absent,
            "late": late,
            "attendance_rate": round(attendance_rate, 2),
            "by_course": by_course
        }

        logger.info(
            f"考勤统计汇总完成: "
            f"日期={target_date}, "
            f"总课程={total_classes}, "
            f"总出勤={total_attendance}, "
            f"出勤率={attendance_rate:.2f}%"
        )

        return summary


# ==================== 缴费统计汇总 ====================

async def summarize_daily_payments(target_date: Optional[date] = None) -> Dict[str, Any]:
    """
    每日汇总缴费统计

    Args:
        target_date: 目标日期，默认为昨天

    Returns:
        dict: 缴费统计信息
            - date: 统计日期
            - total_payments: 缴费笔数
            - total_amount: 缴费总额
            - by_method: 按缴费方式分组
            - by_channel: 按支付渠道分组
            - refund_stats: 退费统计
    """
    if target_date is None:
        target_date = date.today() - timedelta(days=1)

    logger.info(f"开始汇总缴费统计: date={target_date}")

    async with async_session_maker() as session:
        # 定义时间范围
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = datetime.combine(target_date, datetime.max.time())

        # 查询当天的缴费记录
        payment_query = select(Payment).where(
            and_(
                Payment.created_at >= start_datetime,
                Payment.created_at <= end_datetime,
                Payment.status == 2  # 已确认
            )
        )

        result = await session.execute(payment_query)
        payments = result.scalars().all()

        total_payments = len(payments)
        total_amount = sum(p.amount for p in payments)

        # 按缴费方式分组
        by_method: Dict[int, Dict[str, Any]] = {}

        for payment in payments:
            method = payment.payment_method

            if method not in by_method:
                by_method[method] = {
                    "count": 0,
                    "amount": Decimal("0.00")
                }

            by_method[method]["count"] += 1
            by_method[method]["amount"] += payment.amount

        # 按支付渠道分组
        by_channel: Dict[str, Dict[str, Any]] = {}

        for payment in payments:
            channel = payment.payment_channel or "未知"

            if channel not in by_channel:
                by_channel[channel] = {
                    "count": 0,
                    "amount": Decimal("0.00")
                }

            by_channel[channel]["count"] += 1
            by_channel[channel]["amount"] += payment.amount

        # 退费统计
        refund_query = select(Refund).where(
            and_(
                Refund.created_at >= start_datetime,
                Refund.created_at <= end_datetime,
                Refund.status == 4  # 已退款
            )
        )

        result = await session.execute(refund_query)
        refunds = result.scalars().all()

        refund_stats = {
            "total_refunds": len(refunds),
            "total_refund_amount": sum(r.refund_amount for r in refunds)
        }

        summary = {
            "date": target_date.isoformat(),
            "total_payments": total_payments,
            "total_amount": float(total_amount),
            "by_method": {
                k: {
                    "count": v["count"],
                    "amount": float(v["amount"])
                }
                for k, v in by_method.items()
            },
            "by_channel": {
                k: {
                    "count": v["count"],
                    "amount": float(v["amount"])
                }
                for k, v in by_channel.items()
            },
            "refund_stats": {
                "total_refunds": refund_stats["total_refunds"],
                "total_refund_amount": float(refund_stats["total_refund_amount"])
            }
        }

        logger.info(
            f"缴费统计汇总完成: "
            f"日期={target_date}, "
            f"总缴费={total_payments}, "
            f"总金额=¥{total_amount:.2f}"
        )

        return summary


# ==================== 合同统计汇总 ====================

async def summarize_daily_contracts(target_date: Optional[date] = None) -> Dict[str, Any]:
    """
    每日汇总合同统计

    Args:
        target_date: 目标日期，默认为昨天

    Returns:
        dict: 合同统计信息
            - date: 统计日期
            - new_contracts: 新签合同数
            - new_contracts_amount: 新签合同金额
            - active_contracts: 生效合同数
            - total_remaining_hours: 总剩余课时
            - total_remaining_value: 总剩余价值
            - by_package_type: 按课时包类型分组
            - by_status: 按状态分组
    """
    if target_date is None:
        target_date = date.today() - timedelta(days=1)

    logger.info(f"开始汇总合同统计: date={target_date}")

    async with async_session_maker() as session:
        # 定义时间范围
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = datetime.combine(target_date, datetime.max.time())

        # 查询当天新签的合同
        new_contracts_query = select(Contract).where(
            and_(
                Contract.created_at >= start_datetime,
                Contract.created_at <= end_datetime
            )
        )

        result = await session.execute(new_contracts_query)
        new_contracts = result.scalars().all()

        new_contracts_count = len(new_contracts)
        new_contracts_amount = sum(c.total_amount for c in new_contracts)

        # 查询所有生效合同（截至当天）
        active_contracts_query = select(Contract).where(
            Contract.status == 1  # 生效状态
        )

        result = await session.execute(active_contracts_query)
        active_contracts = result.scalars().all()

        active_contracts_count = len(active_contracts)
        total_remaining_hours = sum(c.remaining_hours for c in active_contracts)
        total_remaining_value = sum(c.unit_price * c.remaining_hours for c in active_contracts)

        # 按课时包类型分组（针对新签合同）
        by_package_type: Dict[str, Dict[str, Any]] = {}

        for contract in new_contracts:
            package_type = contract.package_type or "自定义"

            if package_type not in by_package_type:
                by_package_type[package_type] = {
                    "count": 0,
                    "total_amount": Decimal("0.00"),
                    "total_hours": Decimal("0.00")
                }

            by_package_type[package_type]["count"] += 1
            by_package_type[package_type]["total_amount"] += contract.total_amount
            by_package_type[package_type]["total_hours"] += contract.total_hours

        # 按状态分组（所有合同）
        by_status: Dict[int, Dict[str, Any]] = {}

        # 获取当天所有状态的合同
        all_contracts_query = select(Contract).where(
            and_(
                Contract.created_at >= start_datetime,
                Contract.created_at <= end_datetime
            )
        )

        result = await session.execute(all_contracts_query)
        all_contracts = result.scalars().all()

        for contract in all_contracts:
            status = contract.status

            if status not in by_status:
                by_status[status] = {
                    "count": 0,
                    "total_amount": Decimal("0.00")
                }

            by_status[status]["count"] += 1
            by_status[status]["total_amount"] += contract.total_amount

        summary = {
            "date": target_date.isoformat(),
            "new_contracts": new_contracts_count,
            "new_contracts_amount": float(new_contracts_amount),
            "active_contracts": active_contracts_count,
            "total_remaining_hours": float(total_remaining_hours),
            "total_remaining_value": float(total_remaining_value),
            "by_package_type": {
                k: {
                    "count": v["count"],
                    "total_amount": float(v["total_amount"]),
                    "total_hours": float(v["total_hours"])
                }
                for k, v in by_package_type.items()
            },
            "by_status": {
                k: {
                    "count": v["count"],
                    "total_amount": float(v["total_amount"])
                }
                for k, v in by_status.items()
            }
        }

        logger.info(
            f"合同统计汇总完成: "
            f"日期={target_date}, "
            f"新签={new_contracts_count}, "
            f"生效={active_contracts_count}, "
            f"剩余价值=¥{total_remaining_value:.2f}"
        )

        return summary


# ==================== 学员统计汇总 ====================

async def summarize_daily_students(target_date: Optional[date] = None) -> Dict[str, Any]:
    """
    每日汇总学员统计

    Args:
        target_date: 目标日期，默认为昨天

    Returns:
        dict: 学员统计信息
            - date: 统计日期
            - total_students: 总学员数
            - new_students: 新增学员数
            - active_students: 在读学员数
            - by_status: 按状态分组
            - by_source: 按来源分组
    """
    if target_date is None:
        target_date = date.today() - timedelta(days=1)

    logger.info(f"开始汇总学员统计: date={target_date}")

    async with async_session_maker() as session:
        # 定义时间范围
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = datetime.combine(target_date, datetime.max.time())

        # 查询当天新增的学员
        new_students_query = select(Student).where(
            and_(
                Student.created_at >= start_datetime,
                Student.created_at <= end_datetime
            )
        )

        result = await session.execute(new_students_query)
        new_students = result.scalars().all()

        new_students_count = len(new_students)

        # 查询所有学员
        all_students_query = select(Student)
        result = await session.execute(all_students_query)
        all_students = result.scalars().all()

        total_students = len(all_students)

        # 按状态分组
        by_status: Dict[int, int] = {}

        for student in all_students:
            status = student.status
            by_status[status] = by_status.get(status, 0) + 1

        active_students_count = by_status.get(2, 0)  # 在读状态

        # 按来源分组（针对新学员）
        by_source: Dict[str, int] = {}

        for student in new_students:
            source = student.source or "未知"
            by_source[source] = by_source.get(source, 0) + 1

        summary = {
            "date": target_date.isoformat(),
            "total_students": total_students,
            "new_students": new_students_count,
            "active_students": active_students_count,
            "by_status": by_status,
            "by_source": by_source
        }

        logger.info(
            f"学员统计汇总完成: "
            f"日期={target_date}, "
            f"总学员={total_students}, "
            f"新增={new_students_count}, "
            f"在读={active_students_count}"
        )

        return summary


# ==================== 综合统计汇总 ====================

async def generate_daily_summary(target_date: Optional[date] = None) -> Dict[str, Any]:
    """
    生成每日综合统计汇总

    Args:
        target_date: 目标日期，默认为昨天

    Returns:
        dict: 综合统计信息
            - date: 统计日期
            - attendance: 考勤统计
            - payments: 缴费统计
            - contracts: 合同统计
            - students: 学员统计
    """
    if target_date is None:
        target_date = date.today() - timedelta(days=1)

    logger.info(f"开始生成每日综合统计: date={target_date}")

    # 并行执行各项统计
    attendance_summary = await summarize_daily_attendance(target_date)
    payments_summary = await summarize_daily_payments(target_date)
    contracts_summary = await summarize_daily_contracts(target_date)
    students_summary = await summarize_daily_students(target_date)

    summary = {
        "date": target_date.isoformat(),
        "attendance": attendance_summary,
        "payments": payments_summary,
        "contracts": contracts_summary,
        "students": students_summary
    }

    logger.info(f"每日综合统计完成: date={target_date}")

    return summary


# ==================== 趋势分析 ====================

async def analyze_trends(days: int = 30) -> Dict[str, Any]:
    """
    分析指定天数内的趋势

    Args:
        days: 分析天数

    Returns:
        dict: 趋势分析结果
            - period: 分析周期
            - daily_trends: 每日趋势数据
            - trends: 趋势指标
    """
    logger.info(f"开始分析趋势: days={days}")

    trends = []

    for i in range(days):
        target_date = date.today() - timedelta(days=i)
        daily_summary = await generate_daily_summary(target_date)
        trends.append(daily_summary)

    # 按日期排序
    trends.sort(key=lambda x: x["date"])

    # 计算趋势指标
    total_payments = sum(t["payments"]["total_payments"] for t in trends)
    total_amount = sum(t["payments"]["total_amount"] for t in trends)
    avg_payments = total_payments / days if days > 0 else 0
    avg_amount = total_amount / days if days > 0 else 0

    # 计算增长率（比较最近7天和前7天）
    recent_7 = trends[:7]
    previous_7 = trends[7:14] if len(trends) >= 14 else []

    if previous_7:
        recent_payments = sum(t["payments"]["total_payments"] for t in recent_7)
        previous_payments = sum(t["payments"]["total_payments"] for t in previous_7)
        payment_growth_rate = (
            (recent_payments - previous_payments) / previous_payments * 100
            if previous_payments > 0 else 0
        )
    else:
        payment_growth_rate = 0

    summary = {
        "period": f"{days}天",
        "daily_trends": trends,
        "trends": {
            "total_payments": total_payments,
            "total_amount": total_amount,
            "avg_daily_payments": round(avg_payments, 2),
            "avg_daily_amount": round(avg_amount, 2),
            "payment_growth_rate_7d": round(payment_growth_rate, 2)
        }
    }

    logger.info(
        f"趋势分析完成: "
        f"周期={days}天, "
        f"日均缴费={avg_payments:.2f}, "
        f"日均金额=¥{avg_amount:.2f}, "
        f"增长率={payment_growth_rate:.2f}%"
    )

    return summary
