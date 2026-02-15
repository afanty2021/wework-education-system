"""Notifications API Routes

通知管理相关 API 路由
"""
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.notification import (
    NotificationCreate,
    NotificationResponse,
    NotificationUpdate,
    NotificationBatchCreate,
    NotificationMarkRead,
    NotificationListResponse,
)
from app.services.notification_service import (
    NotificationService,
    NotificationNotFoundError,
    NotificationSendError,
    InvalidNotificationDataError,
    NotificationServiceError,
)


router = APIRouter()


# ==================== 通知查询 API ====================

@router.get("", response_model=NotificationListResponse, tags=["Notifications"])
async def list_notifications(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=100, description="返回记录数"),
    type: Optional[int] = Query(None, ge=1, le=5, description="通知类型筛选"),
    receiver_id: Optional[str] = Query(None, description="接收者ID筛选"),
    receiver_type: Optional[int] = Query(None, ge=1, le=3, description="接收者类型筛选"),
    status: Optional[int] = Query(None, ge=0, le=3, description="状态筛选 (0:待发送 1:已发送 2:发送失败 3:已阅读)"),
) -> NotificationListResponse:
    """获取通知列表

    支持分页和多维度筛选
    """
    try:
        from app.services.notification_service import NotificationService

        notifications = await NotificationService.get_all_notifications(
            session=db,
            skip=skip,
            limit=limit,
            notification_type=type,
            receiver_id=receiver_id,
            receiver_type=receiver_type,
            status=status
        )

        # 统计总数和未读数
        total = await NotificationService.count_notifications(
            session=db,
            notification_type=type,
            receiver_id=receiver_id,
            receiver_type=receiver_type,
            status=status
        )

        unread_count = 0
        if receiver_id:
            unread_count = await NotificationService.count_unread_notifications(
                receiver_id=receiver_id,
                session=db,
                receiver_type=receiver_type
            )

        return NotificationListResponse(
            total=total,
            unread_count=unread_count,
            items=notifications
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取通知列表失败: {str(e)}"
        )


@router.get("/receiver/{receiver_id}", response_model=List[NotificationResponse], tags=["Notifications"])
async def list_receiver_notifications(
    receiver_id: str,
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=100, description="返回记录数"),
    unread_only: bool = Query(False, description="是否只获取未读通知"),
) -> List[NotificationResponse]:
    """根据接收者ID获取通知列表"""
    try:
        from app.services.notification_service import NotificationService

        notifications = await NotificationService.get_notifications_by_receiver(
            receiver_id=receiver_id,
            session=db,
            skip=skip,
            limit=limit,
            unread_only=unread_only
        )
        return notifications
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取接收者通知列表失败: {str(e)}"
        )


@router.get("/unread/count", tags=["Notifications"])
async def get_unread_count(
    receiver_id: str = Query(..., description="接收者ID"),
    receiver_type: Optional[int] = Query(None, ge=1, le=3, description="接收者类型筛选"),
    db: AsyncSession = Depends(get_db),
):
    """获取未读通知数量"""
    try:
        from app.services.notification_service import NotificationService

        count = await NotificationService.count_unread_notifications(
            receiver_id=receiver_id,
            session=db,
            receiver_type=receiver_type
        )
        return {"receiver_id": receiver_id, "unread_count": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取未读通知数量失败: {str(e)}"
        )


@router.get("/{notification_id}", response_model=NotificationResponse, tags=["Notifications"])
async def get_notification(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
) -> NotificationResponse:
    """获取通知详情"""
    try:
        from app.services.notification_service import NotificationService

        notification = await NotificationService.get_notification_by_id(notification_id, db)
        return notification
    except NotificationNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"通知不存在: {notification_id}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取通知详情失败: {str(e)}"
        )


# ==================== 通知管理 API ====================

@router.post("", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED, tags=["Notifications"])
async def create_notification(
    notification_data: NotificationCreate,
    db: AsyncSession = Depends(get_db),
) -> NotificationResponse:
    """创建通知"""
    try:
        from app.services.notification_service import NotificationService

        notification = await NotificationService.create_notification(
            notification_data=notification_data,
            session=db
        )
        return notification
    except InvalidNotificationDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建通知失败: {str(e)}"
        )


@router.post("/batch", response_model=List[NotificationResponse], status_code=status.HTTP_201_CREATED, tags=["Notifications"])
async def create_batch_notifications(
    batch_data: NotificationBatchCreate,
    db: AsyncSession = Depends(get_db),
) -> List[NotificationResponse]:
    """批量创建通知"""
    try:
        from app.services.notification_service import notification_service

        notifications = await notification_service.create_batch_notifications(
            batch_data=batch_data,
            session=db
        )
        return notifications
    except InvalidNotificationDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量创建通知失败: {str(e)}"
        )


@router.put("/{notification_id}", response_model=NotificationResponse, tags=["Notifications"])
async def update_notification(
    notification_id: int,
    notification_data: NotificationUpdate,
    db: AsyncSession = Depends(get_db),
) -> NotificationResponse:
    """更新通知"""
    try:
        from app.services.notification_service import NotificationService

        notification = await NotificationService.update_notification(
            notification_id=notification_id,
            notification_data=notification_data,
            session=db
        )
        return notification
    except NotificationNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"通知不存在: {notification_id}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新通知失败: {str(e)}"
        )


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Notifications"])
async def delete_notification(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除通知"""
    try:
        from app.services.notification_service import NotificationService

        await NotificationService.delete_notification(notification_id, db)
    except NotificationNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"通知不存在: {notification_id}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除通知失败: {str(e)}"
        )


# ==================== 通知状态管理 API ====================

@router.post("/mark-read", tags=["Notifications"])
async def mark_notifications_as_read(
    mark_data: NotificationMarkRead,
    db: AsyncSession = Depends(get_db),
):
    """标记通知为已读"""
    try:
        from app.services.notification_service import NotificationService

        count = await NotificationService.mark_notifications_as_read(
            notification_ids=mark_data.notification_ids,
            session=db
        )
        return {"marked_count": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"标记通知已读失败: {str(e)}"
        )


# ==================== 消息发送 API ====================

@router.post("/{notification_id}/send", response_model=NotificationResponse, tags=["Notifications"])
async def send_notification(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
) -> NotificationResponse:
    """发送通知到企业微信"""
    try:
        from app.services.notification_service import notification_service

        # 获取通知
        notification = await notification_service.get_notification_by_id(notification_id, db)

        # 发送通知
        notification = await notification_service.send_notification_to_wework(notification, db)
        return notification
    except NotificationNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"通知不存在: {notification_id}"
        )
    except NotificationSendError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"发送通知失败: {str(e)}"
        )


@router.post("/send-and-create", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED, tags=["Notifications"])
async def send_and_create_notification(
    notification_data: NotificationCreate,
    db: AsyncSession = Depends(get_db),
) -> NotificationResponse:
    """创建并发送通知"""
    try:
        from app.services.notification_service import notification_service

        notification = await notification_service.send_and_create_notification(
            notification_data=notification_data,
            session=db
        )
        return notification
    except InvalidNotificationDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建并发送通知失败: {str(e)}"
        )


@router.post("/batch/send", response_model=List[NotificationResponse], status_code=status.HTTP_201_CREATED, tags=["Notifications"])
async def send_batch_notifications(
    batch_data: NotificationBatchCreate,
    db: AsyncSession = Depends(get_db),
) -> List[NotificationResponse]:
    """批量创建并发送通知"""
    try:
        from app.services.notification_service import notification_service

        notifications = await notification_service.send_batch_notifications(
            batch_data=batch_data,
            session=db
        )
        return notifications
    except InvalidNotificationDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量创建并发送通知失败: {str(e)}"
        )
