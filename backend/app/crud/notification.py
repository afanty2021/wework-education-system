"""Notification CRUD

通知数据访问层

提供通知的 CRUD 操作
"""
import logging
from typing import List, Optional
from datetime import datetime

from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification


logger = logging.getLogger(__name__)


class NotificationCRUD:
    """通知 CRUD 操作类

    提供通知的完整数据访问层操作
    所有方法都是静态方法，需要传入 AsyncSession
    """

    @staticmethod
    async def get_all(
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
        logger.debug(f"查询通知列表: skip={skip}, limit={limit}")

        # 构建查询
        conditions = []

        if notification_type is not None:
            conditions.append(Notification.type == notification_type)

        if receiver_id is not None:
            conditions.append(Notification.receiver_id == receiver_id)

        if receiver_type is not None:
            conditions.append(Notification.receiver_type == receiver_type)

        if status is not None:
            conditions.append(Notification.status == status)

        if start_date is not None:
            conditions.append(Notification.created_at >= start_date)

        if end_date is not None:
            conditions.append(Notification.created_at <= end_date)

        # 执行查询
        if conditions:
            statement = select(Notification).where(
                and_(*conditions)
            ).order_by(Notification.created_at.desc()).offset(skip).limit(limit)
        else:
            statement = select(Notification).order_by(
                Notification.created_at.desc()
            ).offset(skip).limit(limit)

        result = await session.execute(statement)
        notifications = result.scalars().all()

        logger.debug(f"查询到 {len(notifications)} 条通知")
        return notifications

    @staticmethod
    async def get_by_id(notification_id: int, session: AsyncSession) -> Optional[Notification]:
        """
        根据ID获取通知

        Args:
            notification_id: 通知ID
            session: 数据库会话

        Returns:
            Optional[Notification]: 通知对象，不存在则返回 None
        """
        logger.debug(f"查询通知: notification_id={notification_id}")

        statement = select(Notification).where(Notification.id == notification_id)
        result = await session.execute(statement)
        notification = result.scalar_one_or_none()

        return notification

    @staticmethod
    async def get_by_receiver(
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
        logger.debug(f"查询接收者通知: receiver_id={receiver_id}, unread_only={unread_only}")

        conditions = [Notification.receiver_id == receiver_id]

        if unread_only:
            conditions.append(Notification.status.in_([0, 1]))  # 待发送或已发送但未读

        statement = select(Notification).where(
            and_(*conditions)
        ).order_by(Notification.created_at.desc()).offset(skip).limit(limit)

        result = await session.execute(statement)
        notifications = result.scalars().all()

        return notifications

    @staticmethod
    async def count(
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
        # 构建查询
        conditions = []

        if notification_type is not None:
            conditions.append(Notification.type == notification_type)

        if receiver_id is not None:
            conditions.append(Notification.receiver_id == receiver_id)

        if receiver_type is not None:
            conditions.append(Notification.receiver_type == receiver_type)

        if status is not None:
            conditions.append(Notification.status == status)

        if start_date is not None:
            conditions.append(Notification.created_at >= start_date)

        if end_date is not None:
            conditions.append(Notification.created_at <= end_date)

        # 执行查询
        if conditions:
            statement = select(func.count(Notification.id)).where(and_(*conditions))
        else:
            statement = select(func.count(Notification.id))

        result = await session.execute(statement)
        count = result.scalar()

        return count

    @staticmethod
    async def count_unread(
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
        conditions = [
            Notification.receiver_id == receiver_id,
            Notification.status.in_([0, 1])  # 待发送或已发送但未读
        ]

        if receiver_type is not None:
            conditions.append(Notification.receiver_type == receiver_type)

        statement = select(func.count(Notification.id)).where(and_(*conditions))
        result = await session.execute(statement)
        count = result.scalar()

        return count

    @staticmethod
    async def create(notification: Notification, session: AsyncSession) -> Notification:
        """
        创建通知

        Args:
            notification: 通知对象
            session: 数据库会话

        Returns:
            Notification: 创建的通知对象
        """
        logger.info(f"创建通知: type={notification.type}, receiver_id={notification.receiver_id}")

        session.add(notification)
        await session.flush()
        await session.refresh(notification)

        logger.debug(f"通知创建成功: id={notification.id}")
        return notification

    @staticmethod
    async def create_batch(notifications: List[Notification], session: AsyncSession) -> List[Notification]:
        """
        批量创建通知

        Args:
            notifications: 通知对象列表
            session: 数据库会话

        Returns:
            List[Notification]: 创建的通知对象列表
        """
        logger.info(f"批量创建通知: count={len(notifications)}")

        for notification in notifications:
            session.add(notification)

        await session.flush()

        for notification in notifications:
            await session.refresh(notification)

        logger.debug(f"批量通知创建成功: count={len(notifications)}")
        return notifications

    @staticmethod
    async def update(notification: Notification, session: AsyncSession) -> Notification:
        """
        更新通知

        Args:
            notification: 通知对象
            session: 数据库会话

        Returns:
            Notification: 更新后的通知对象
        """
        logger.info(f"更新通知: id={notification.id}")

        session.add(notification)
        await session.flush()
        await session.refresh(notification)

        logger.debug(f"通知更新成功: id={notification.id}")
        return notification

    @staticmethod
    async def mark_as_read(notification_ids: List[int], session: AsyncSession) -> int:
        """
        标记通知为已读

        Args:
            notification_ids: 通知ID列表
            session: 数据库会话

        Returns:
            int: 更新的记录数
        """
        logger.info(f"标记通知为已读: count={len(notification_ids)}")

        # 查询通知
        statement = select(Notification).where(Notification.id.in_(notification_ids))
        result = await session.execute(statement)
        notifications = result.scalars().all()

        # 标记为已读
        now = datetime.now()
        for notification in notifications:
            notification.status = 3  # 已读
            notification.read_at = now
            session.add(notification)

        await session.flush()

        logger.debug(f"标记已读成功: count={len(notifications)}")
        return len(notifications)

    @staticmethod
    async def delete(notification: Notification, session: AsyncSession) -> None:
        """
        删除通知

        Args:
            notification: 通知对象
            session: 数据库会话
        """
        logger.info(f"删除通知: id={notification.id}")

        await session.delete(notification)
        await session.flush()

        logger.debug(f"通知删除成功: id={notification.id}")

    @staticmethod
    async def delete_batch(notification_ids: List[int], session: AsyncSession) -> int:
        """
        批量删除通知

        Args:
            notification_ids: 通知ID列表
            session: 数据库会话

        Returns:
            int: 删除的记录数
        """
        logger.info(f"批量删除通知: count={len(notification_ids)}")

        # 查询通知
        statement = select(Notification).where(Notification.id.in_(notification_ids))
        result = await session.execute(statement)
        notifications = result.scalars().all()

        # 删除通知
        for notification in notifications:
            await session.delete(notification)

        await session.flush()

        logger.debug(f"批量删除成功: count={len(notifications)}")
        return len(notifications)
