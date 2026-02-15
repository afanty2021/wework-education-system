"""Notification Service

通知业务逻辑服务层

提供通知管理的完整业务逻辑处理，包括：
- 通知的创建、查询、更新、删除
- 企业微信消息推送
- 消息模板生成
- 批量通知发送
- 通知状态管理
"""
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification
from app.models.contract import Contract
from app.models.schedule import Schedule
from app.models.homework import Homework
from app.models.attendance import Attendance
from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
    NotificationBatchCreate,
)
from app.core.wework import WeWorkService


logger = logging.getLogger(__name__)


class NotificationServiceError(Exception):
    """通知服务异常基类"""
    pass


class NotificationNotFoundError(NotificationServiceError):
    """通知不存在异常"""
    pass


class NotificationSendError(NotificationServiceError):
    """通知发送失败异常"""
    pass


class InvalidNotificationDataError(NotificationServiceError):
    """无效通知数据异常"""
    pass


class NotificationService:
    """通知业务服务类

    提供通知的完整业务逻辑处理
    所有方法都是异步的，需要传入 AsyncSession
    """

    def __init__(self):
        """初始化通知服务"""
        self.wework_service = WeWorkService()

    # ==================== 通知查询服务 ====================

    @staticmethod
    async def get_all_notifications(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        notification_type: Optional[int] = None,
        receiver_id: Optional[str] = None,
        receiver_type: Optional[int] = None,
        status: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Notification]:
        """
        获取通知列表，支持分页和筛选

        Args:
            session: 数据库会话
            skip: 跳过记录数
            limit: 返回记录数
            notification_type: 通知类型筛选
            receiver_id: 接收者ID筛选
            receiver_type: 接收者类型筛选
            status: 状态筛选
            start_date: 开始日期筛选
            end_date: 结束日期筛选

        Returns:
            List[Notification]: 通知列表
        """
        logger.info(f"查询通知列表: skip={skip}, limit={limit}")

        from app.crud.notification import NotificationCRUD

        notifications = await NotificationCRUD.get_all(
            session=session,
            skip=skip,
            limit=limit,
            notification_type=notification_type,
            receiver_id=receiver_id,
            receiver_type=receiver_type,
            status=status,
            start_date=start_date,
            end_date=end_date
        )

        return notifications

    @staticmethod
    async def get_notification_by_id(notification_id: int, session: AsyncSession) -> Notification:
        """
        根据ID获取通知详情

        Args:
            notification_id: 通知ID
            session: 数据库会话

        Returns:
            Notification: 通知对象

        Raises:
            NotificationNotFoundError: 通知不存在
        """
        logger.info(f"查询通知详情: notification_id={notification_id}")

        from app.crud.notification import NotificationCRUD

        notification = await NotificationCRUD.get_by_id(notification_id, session)

        if not notification:
            logger.warning(f"通知不存在: notification_id={notification_id}")
            raise NotificationNotFoundError(f"通知不存在: {notification_id}")

        return notification

    @staticmethod
    async def get_notifications_by_receiver(
        receiver_id: str,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        unread_only: bool = False
    ) -> List[Notification]:
        """
        根据接收者ID获取通知列表

        Args:
            receiver_id: 接收者ID
            session: 数据库会话
            skip: 跳过记录数
            limit: 返回记录数
            unread_only: 是否只获取未读通知

        Returns:
            List[Notification]: 通知列表
        """
        logger.info(f"查询接收者通知: receiver_id={receiver_id}")

        from app.crud.notification import NotificationCRUD

        notifications = await NotificationCRUD.get_by_receiver(
            receiver_id=receiver_id,
            session=session,
            skip=skip,
            limit=limit,
            unread_only=unread_only
        )

        return notifications

    @staticmethod
    async def count_notifications(
        session: AsyncSession,
        notification_type: Optional[int] = None,
        receiver_id: Optional[str] = None,
        receiver_type: Optional[int] = None,
        status: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> int:
        """
        统计通知数量

        Args:
            session: 数据库会话
            notification_type: 通知类型筛选
            receiver_id: 接收者ID筛选
            receiver_type: 接收者类型筛选
            status: 状态筛选
            start_date: 开始日期筛选
            end_date: 结束日期筛选

        Returns:
            int: 通知总数
        """
        from app.crud.notification import NotificationCRUD

        count = await NotificationCRUD.count(
            session=session,
            notification_type=notification_type,
            receiver_id=receiver_id,
            receiver_type=receiver_type,
            status=status,
            start_date=start_date,
            end_date=end_date
        )

        return count

    @staticmethod
    async def count_unread_notifications(
        receiver_id: str,
        session: AsyncSession,
        receiver_type: Optional[int] = None
    ) -> int:
        """
        统计未读通知数量

        Args:
            receiver_id: 接收者ID
            session: 数据库会话
            receiver_type: 接收者类型筛选

        Returns:
            int: 未读通知数量
        """
        from app.crud.notification import NotificationCRUD

        count = await NotificationCRUD.count_unread(
            receiver_id=receiver_id,
            session=session,
            receiver_type=receiver_type
        )

        return count

    # ==================== 通知管理服务 ====================

    @staticmethod
    async def create_notification(
        notification_data: NotificationCreate,
        session: AsyncSession
    ) -> Notification:
        """
        创建通知

        Args:
            notification_data: 通知创建数据
            session: 数据库会话

        Returns:
            Notification: 创建的通知对象

        Raises:
            InvalidNotificationDataError: 数据验证失败
        """
        logger.info(f"创建通知: type={notification_data.type}, receiver_id={notification_data.receiver_id}")

        # 创建通知对象
        notification = Notification(
            type=notification_data.type,
            receiver_id=notification_data.receiver_id,
            receiver_type=notification_data.receiver_type,
            title=notification_data.title,
            content=notification_data.content,
            url=notification_data.url,
            status=0,  # 待发送
            created_at=datetime.now()
        )

        from app.crud.notification import NotificationCRUD

        try:
            return await NotificationCRUD.create(notification, session)
        except Exception as e:
            logger.error(f"创建通知失败: {e}")
            raise InvalidNotificationDataError(f"创建通知失败: {str(e)}")

    @staticmethod
    async def update_notification(
        notification_id: int,
        notification_data: NotificationUpdate,
        session: AsyncSession
    ) -> Notification:
        """
        更新通知

        Args:
            notification_id: 通知ID
            notification_data: 通知更新数据
            session: 数据库会话

        Returns:
            Notification: 更新后的通知对象

        Raises:
            NotificationNotFoundError: 通知不存在
        """
        logger.info(f"更新通知: notification_id={notification_id}")

        # 获取通知
        notification = await NotificationService.get_notification_by_id(notification_id, session)

        # 更新字段
        if notification_data.title is not None:
            notification.title = notification_data.title
        if notification_data.content is not None:
            notification.content = notification_data.content
        if notification_data.url is not None:
            notification.url = notification_data.url
        if notification_data.status is not None:
            notification.status = notification_data.status
        if notification_data.error_msg is not None:
            notification.error_msg = notification_data.error_msg

        from app.crud.notification import NotificationCRUD

        return await NotificationCRUD.update(notification, session)

    @staticmethod
    async def delete_notification(notification_id: int, session: AsyncSession) -> None:
        """
        删除通知

        Args:
            notification_id: 通知ID
            session: 数据库会话

        Raises:
            NotificationNotFoundError: 通知不存在
        """
        logger.info(f"删除通知: notification_id={notification_id}")

        # 获取通知
        notification = await NotificationService.get_notification_by_id(notification_id, session)

        from app.crud.notification import NotificationCRUD

        await NotificationCRUD.delete(notification, session)

    @staticmethod
    async def mark_notifications_as_read(
        notification_ids: List[int],
        session: AsyncSession
    ) -> int:
        """
        标记通知为已读

        Args:
            notification_ids: 通知ID列表
            session: 数据库会话

        Returns:
            int: 更新的记录数
        """
        logger.info(f"标记通知为已读: count={len(notification_ids)}")

        from app.crud.notification import NotificationCRUD

        return await NotificationCRUD.mark_as_read(notification_ids, session)

    # ==================== 批量通知服务 ====================

    async def create_batch_notifications(
        self,
        batch_data: NotificationBatchCreate,
        session: AsyncSession
    ) -> List[Notification]:
        """
        批量创建通知

        Args:
            batch_data: 批量创建数据
            session: 数据库会话

        Returns:
            List[Notification]: 创建的通知列表
        """
        logger.info(f"批量创建通知: count={len(batch_data.receiver_ids)}")

        # 创建通知对象列表
        notifications = [
            Notification(
                type=batch_data.type,
                receiver_id=receiver_id,
                receiver_type=batch_data.receiver_type,
                title=batch_data.title,
                content=batch_data.content,
                url=batch_data.url,
                status=0,  # 待发送
                created_at=datetime.now()
            )
            for receiver_id in batch_data.receiver_ids
        ]

        from app.crud.notification import NotificationCRUD

        try:
            return await NotificationCRUD.create_batch(notifications, session)
        except Exception as e:
            logger.error(f"批量创建通知失败: {e}")
            raise InvalidNotificationDataError(f"批量创建通知失败: {str(e)}")

    # ==================== 企业微信消息推送服务 ====================

    async def send_notification_to_wework(
        self,
        notification: Notification,
        session: AsyncSession
    ) -> Notification:
        """
        发送通知到企业微信

        Args:
            notification: 通知对象
            session: 数据库会话

        Returns:
            Notification: 更新后的通知对象

        Raises:
            NotificationSendError: 发送失败
        """
        logger.info(f"发送企业微信通知: notification_id={notification.id}")

        # 发送消息
        try:
            # 根据通知类型选择消息格式
            if notification.url:
                # 如果有跳转链接，发送卡片消息
                response = await self.wework_service.send_card_message(
                    user_id=notification.receiver_id,
                    title=notification.title,
                    description=notification.content or "",
                    url=notification.url
                )
            else:
                # 否则发送文本消息
                message = f"{notification.title}\n\n{notification.content or ''}"
                response = await self.wework_service.send_message(
                    user_id=notification.receiver_id,
                    content=message
                )

            # 检查发送结果
            if response.get("errcode") == 0:
                # 发送成功
                notification.status = 1  # 已发送
                notification.sent_at = datetime.now()
                logger.info(f"企业微信通知发送成功: notification_id={notification.id}")
            else:
                # 发送失败
                notification.status = 2  # 发送失败
                notification.error_msg = f"errcode={response.get('errcode')}, errmsg={response.get('errmsg')}"
                logger.error(f"企业微信通知发送失败: {notification.error_msg}")
                raise NotificationSendError(notification.error_msg)

        except NotificationSendError:
            raise
        except Exception as e:
            # 发送异常
            notification.status = 2  # 发送失败
            notification.error_msg = str(e)
            logger.error(f"企业微信通知发送异常: {e}")
            raise NotificationSendError(f"发送异常: {str(e)}")

        # 更新通知状态
        from app.crud.notification import NotificationCRUD

        return await NotificationCRUD.update(notification, session)

    async def send_and_create_notification(
        self,
        notification_data: NotificationCreate,
        session: AsyncSession
    ) -> Notification:
        """
        创建并发送通知

        Args:
            notification_data: 通知创建数据
            session: 数据库会话

        Returns:
            Notification: 创建并发送的通知对象
        """
        # 创建通知
        notification = await self.create_notification(notification_data, session)

        # 如果是企业微信用户，立即发送
        if notification.receiver_type == 1:  # 企业微信
            try:
                notification = await self.send_notification_to_wework(notification, session)
            except NotificationSendError as e:
                logger.error(f"发送通知失败: {e}")
                # 即使发送失败，也返回通知对象（状态为失败）

        return notification

    async def send_batch_notifications(
        self,
        batch_data: NotificationBatchCreate,
        session: AsyncSession
    ) -> List[Notification]:
        """
        批量创建并发送通知

        Args:
            batch_data: 批量创建数据
            session: 数据库会话

        Returns:
            List[Notification]: 创建并发送的通知列表
        """
        # 批量创建通知
        notifications = await self.create_batch_notifications(batch_data, session)

        # 如果是企业微信用户，批量发送
        if batch_data.receiver_type == 1:  # 企业微信
            for notification in notifications:
                try:
                    await self.send_notification_to_wework(notification, session)
                except NotificationSendError as e:
                    logger.error(f"发送通知失败: notification_id={notification.id}, error={e}")

        return notifications

    # ==================== 消息模板服务 ====================

    @staticmethod
    def create_class_reminder_template(
        schedule: "Schedule",
        student_name: str,
        course_name: str,
        teacher_name: str,
        classroom_name: str,
        reminder_minutes: int = 30
    ) -> Dict[str, str]:
        """
        创建上课提醒消息模板

        Args:
            schedule: 排课对象
            student_name: 学员姓名
            course_name: 课程名称
            teacher_name: 教师姓名
            classroom_name: 教室名称
            reminder_minutes: 提前提醒分钟数

        Returns:
            Dict[str, str]: 包含 title 和 content 的字典
        """
        start_time = schedule.start_time.strftime("%Y-%m-%d %H:%M")

        title = f"上课提醒：{course_name}"
        content = (
            f"亲爱的{student_name}同学，您好！\n\n"
            f"您有一节{course_name}课程即将开始，请提前做好准备。\n\n"
            f"课程：{course_name}\n"
            f"教师：{teacher_name}\n"
            f"教室：{classroom_name}\n"
            f"时间：{start_time}\n\n"
            f"请准时参加，祝您学习愉快！"
        )

        return {"title": title, "content": content}

    @staticmethod
    def create_homework_notice_template(
        homework: "Homework",
        student_name: str,
        course_name: str
    ) -> Dict[str, str]:
        """
        创建作业通知消息模板

        Args:
            homework: 作业对象
            student_name: 学员姓名
            course_name: 课程名称

        Returns:
            Dict[str, str]: 包含 title 和 content 的字典
        """
        deadline = homework.deadline.strftime("%Y-%m-%d %H:%M") if homework.deadline else "无截止时间"

        title = f"作业通知：{course_name}"
        content = (
            f"亲爱的{student_name}同学，您好！\n\n"
            f"您的{course_name}课程发布了新的作业。\n\n"
            f"作业：{homework.title}\n"
            f"课程：{course_name}\n"
            f"截止时间：{deadline}\n\n"
            f"请及时完成并提交，祝您学习愉快！"
        )

        return {"title": title, "content": content}

    @staticmethod
    def create_attendance_notice_template(
        attendance: "Attendance",
        student_name: str,
        course_name: str,
        attendance_date: date
    ) -> Dict[str, str]:
        """
        创建考勤通知消息模板

        Args:
            attendance: 考勤对象
            student_name: 学员姓名
            course_name: 课程名称
            attendance_date: 考勤日期

        Returns:
            Dict[str, str]: 包含 title 和 content 的字典
        """
        status_map = {
            1: "出勤",
            2: "请假",
            3: "缺勤",
            4: "迟到"
        }

        status_text = status_map.get(attendance.status, "未知")

        title = f"考勤通知：{course_name}"
        content = (
            f"亲爱的{student_name}家长，您好！\n\n"
            f"您的孩子参加了{course_name}课程的考勤。\n\n"
            f"课程：{course_name}\n"
            f"日期：{attendance_date.strftime('%Y-%m-%d')}\n"
            f"考勤状态：{status_text}\n"
            f"备注：{attendance.notes or '无'}\n\n"
            f"感谢您的关注！"
        )

        return {"title": title, "content": content}

    @staticmethod
    def create_contract_expiry_reminder_template(
        contract: "Contract",
        student_name: str,
        course_name: str,
        days_until_expiry: int
    ) -> Dict[str, str]:
        """
        创建合同到期提醒消息模板

        Args:
            contract: 合同对象
            student_name: 学员姓名
            course_name: 课程名称
            days_until_expiry: 距到期天数

        Returns:
            Dict[str, str]: 包含 title 和 content 的字典
        """
        remaining_value = contract.unit_price * contract.remaining_hours

        title = f"合同到期提醒"
        content = (
            f"亲爱的{student_name}家长，您好！\n\n"
            f"您孩子的{course_name}课程合同即将到期。\n\n"
            f"课程：{course_name}\n"
            f"到期日期：{contract.end_date.strftime('%Y-%m-%d') if contract.end_date else '未知'}\n"
            f"剩余天数：{days_until_expiry}天\n"
            f"剩余课时：{contract.remaining_hours}课时\n"
            f"剩余价值：¥{remaining_value:.2f}\n\n"
            f"如需续费，请及时联系课程顾问。感谢您的支持！"
        )

        return {"title": title, "content": content}

    @staticmethod
    def create_contract_insufficient_hours_template(
        contract: "Contract",
        student_name: str,
        course_name: str
    ) -> Dict[str, str]:
        """
        创建合同课时不足提醒消息模板

        Args:
            contract: 合同对象
            student_name: 学员姓名
            course_name: 课程名称

        Returns:
            Dict[str, str]: 包含 title 和 content 的字典
        """
        remaining_value = contract.unit_price * contract.remaining_hours

        title = f"课时不足提醒"
        content = (
            f"亲爱的{student_name}家长，您好！\n\n"
            f"您孩子的{course_name}课程课时即将用完。\n\n"
            f"课程：{course_name}\n"
            f"剩余课时：{contract.remaining_hours}课时\n"
            f"剩余价值：¥{remaining_value:.2f}\n\n"
            f"为不影响学习进度，建议及时续费。感谢您的支持！"
        )

        return {"title": title, "content": content}

    @staticmethod
    def create_system_notice_template(
        title: str,
        content: str
    ) -> Dict[str, str]:
        """
        创建系统通知消息模板

        Args:
            title: 通知标题
            content: 通知内容

        Returns:
            Dict[str, str]: 包含 title 和 content 的字典
        """
        return {
            "title": f"系统通知：{title}",
            "content": content
        }

    # ==================== 场景化通知服务 ====================

    async def send_class_reminder(
        self,
        schedule: Schedule,
        student_id: str,
        student_name: str,
        course_name: str,
        teacher_name: str,
        classroom_name: str,
        session: AsyncSession,
        reminder_minutes: int = 30
    ) -> Notification:
        """
        发送上课提醒通知

        Args:
            schedule: 排课对象
            student_id: 学员ID（企业微信ID）
            student_name: 学员姓名
            course_name: 课程名称
            teacher_name: 教师姓名
            classroom_name: 教室名称
            reminder_minutes: 提前提醒分钟数
            session: 数据库会话

        Returns:
            Notification: 创建并发送的通知对象
        """
        # 生成消息模板
        template = self.create_class_reminder_template(
            schedule=schedule,
            student_name=student_name,
            course_name=course_name,
            teacher_name=teacher_name,
            classroom_name=classroom_name,
            reminder_minutes=reminder_minutes
        )

        # 创建通知数据
        notification_data = NotificationCreate(
            type=1,  # 上课提醒
            receiver_id=student_id,
            receiver_type=1,  # 企业微信
            title=template["title"],
            content=template["content"]
        )

        # 创建并发送通知
        return await self.send_and_create_notification(notification_data, session)

    async def send_homework_notice(
        self,
        homework: Homework,
        student_id: str,
        student_name: str,
        course_name: str,
        session: AsyncSession
    ) -> Notification:
        """
        发送作业通知

        Args:
            homework: 作业对象
            student_id: 学员ID（企业微信ID）
            student_name: 学员姓名
            course_name: 课程名称
            session: 数据库会话

        Returns:
            Notification: 创建并发送的通知对象
        """
        # 生成消息模板
        template = self.create_homework_notice_template(
            homework=homework,
            student_name=student_name,
            course_name=course_name
        )

        # 创建通知数据
        notification_data = NotificationCreate(
            type=2,  # 作业通知
            receiver_id=student_id,
            receiver_type=1,  # 企业微信
            title=template["title"],
            content=template["content"],
            url=f"/homeworks/{homework.id}"  # 跳转到作业详情
        )

        # 创建并发送通知
        return await self.send_and_create_notification(notification_data, session)

    async def send_attendance_notice(
        self,
        attendance: Attendance,
        parent_id: str,
        student_name: str,
        course_name: str,
        attendance_date: date,
        session: AsyncSession
    ) -> Notification:
        """
        发送考勤通知

        Args:
            attendance: 考勤对象
            parent_id: 家长ID（企业微信ID）
            student_name: 学员姓名
            course_name: 课程名称
            attendance_date: 考勤日期
            session: 数据库会话

        Returns:
            Notification: 创建并发送的通知对象
        """
        # 生成消息模板
        template = self.create_attendance_notice_template(
            attendance=attendance,
            student_name=student_name,
            course_name=course_name,
            attendance_date=attendance_date
        )

        # 创建通知数据
        notification_data = NotificationCreate(
            type=3,  # 考勤通知
            receiver_id=parent_id,
            receiver_type=1,  # 企业微信
            title=template["title"],
            content=template["content"],
            url=f"/attendances/{attendance.id}"  # 跳转到考勤详情
        )

        # 创建并发送通知
        return await self.send_and_create_notification(notification_data, session)

    async def send_contract_expiry_reminder(
        self,
        contract: Contract,
        parent_id: str,
        student_name: str,
        course_name: str,
        days_until_expiry: int,
        session: AsyncSession
    ) -> Notification:
        """
        发送合同到期提醒通知

        Args:
            contract: 合同对象
            parent_id: 家长ID（企业微信ID）
            student_name: 学员姓名
            course_name: 课程名称
            days_until_expiry: 距到期天数
            session: 数据库会话

        Returns:
            Notification: 创建并发送的通知对象
        """
        # 生成消息模板
        template = self.create_contract_expiry_reminder_template(
            contract=contract,
            student_name=student_name,
            course_name=course_name,
            days_until_expiry=days_until_expiry
        )

        # 创建通知数据
        notification_data = NotificationCreate(
            type=4,  # 合同通知
            receiver_id=parent_id,
            receiver_type=1,  # 企业微信
            title=template["title"],
            content=template["content"],
            url=f"/contracts/{contract.id}"  # 跳转到合同详情
        )

        # 创建并发送通知
        return await self.send_and_create_notification(notification_data, session)

    async def send_system_notice(
        self,
        title: str,
        content: str,
        receiver_id: str,
        session: AsyncSession,
        receiver_type: int = 1,
        url: Optional[str] = None
    ) -> Notification:
        """
        发送系统通知

        Args:
            title: 通知标题
            content: 通知内容
            receiver_id: 接收者ID
            receiver_type: 接收者类型
            url: 跳转链接
            session: 数据库会话

        Returns:
            Notification: 创建并发送的通知对象
        """
        # 生成消息模板
        template = self.create_system_notice_template(
            title=title,
            content=content
        )

        # 创建通知数据
        notification_data = NotificationCreate(
            type=5,  # 系统通知
            receiver_id=receiver_id,
            receiver_type=receiver_type,
            title=template["title"],
            content=template["content"],
            url=url
        )

        # 创建并发送通知
        return await self.send_and_create_notification(notification_data, session)


# 创建服务实例
notification_service = NotificationService()
