"""Notification Schemas

通知相关的 Pydantic 模型

用于通知的创建、更新和响应
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict
from enum import IntEnum


class NotificationType(IntEnum):
    """通知类型枚举"""
    CLASS_REMINDER = 1  # 上课提醒
    HOMEWORK_NOTICE = 2  # 作业通知
    ATTENDANCE_NOTICE = 3  # 考勤通知
    CONTRACT_NOTICE = 4  # 合同通知
    SYSTEM_NOTICE = 5  # 系统通知


class ReceiverType(IntEnum):
    """接收者类型枚举"""
    WEWORK = 1  # 企业微信
    PARENT = 2  # 家长
    MINIAPP = 3  # 小程序


class NotificationStatus(IntEnum):
    """通知状态枚举"""
    PENDING = 0  # 待发送
    SENT = 1  # 已发送
    FAILED = 2  # 发送失败
    READ = 3  # 已阅读


class NotificationBase(BaseModel):
    """通知基础模型"""
    type: int = Field(..., ge=1, le=5, description="通知类型: 1:上课提醒 2:作业通知 3:考勤通知 4:合同通知 5:系统通知")
    receiver_id: str = Field(..., min_length=1, max_length=64, description="接收者ID")
    receiver_type: int = Field(default=1, ge=1, le=3, description="接收者类型: 1:企业微信 2:家长 3:小程序")
    title: str = Field(..., min_length=1, max_length=200, description="通知标题")
    content: Optional[str] = Field(None, max_length=2000, description="通知内容")
    url: Optional[str] = Field(None, max_length=500, description="跳转链接")

    @field_validator('type')
    @classmethod
    def validate_type(cls, v: int) -> int:
        """验证通知类型"""
        try:
            NotificationType(v)
        except ValueError:
            raise ValueError(f'无效的通知类型: {v}')
        return v

    @field_validator('receiver_type')
    @classmethod
    def validate_receiver_type(cls, v: int) -> int:
        """验证接收者类型"""
        try:
            ReceiverType(v)
        except ValueError:
            raise ValueError(f'无效的接收者类型: {v}')
        return v


class NotificationCreate(NotificationBase):
    """创建通知模型"""
    pass


class NotificationUpdate(BaseModel):
    """更新通知模型"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="通知标题")
    content: Optional[str] = Field(None, max_length=2000, description="通知内容")
    url: Optional[str] = Field(None, max_length=500, description="跳转链接")
    status: Optional[int] = Field(None, ge=0, le=3, description="通知状态: 0:待发送 1:已发送 2:发送失败 3:已阅读")
    error_msg: Optional[str] = Field(None, max_length=500, description="错误信息")

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: Optional[int]) -> Optional[int]:
        """验证通知状态"""
        if v is not None:
            try:
                NotificationStatus(v)
            except ValueError:
                raise ValueError(f'无效的通知状态: {v}')
        return v


class NotificationResponse(NotificationBase):
    """通知响应模型"""
    id: int
    sent_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    status: int
    error_msg: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NotificationBatchCreate(BaseModel):
    """批量创建通知模型"""
    receiver_ids: List[str] = Field(..., min_length=1, max_length=100, description="接收者ID列表")
    receiver_type: int = Field(..., ge=1, le=3, description="接收者类型")
    type: int = Field(..., ge=1, le=5, description="通知类型")
    title: str = Field(..., min_length=1, max_length=200, description="通知标题")
    content: Optional[str] = Field(None, max_length=2000, description="通知内容")
    url: Optional[str] = Field(None, max_length=500, description="跳转链接")


class NotificationMarkRead(BaseModel):
    """标记通知已读模型"""
    notification_ids: List[int] = Field(..., min_length=1, max_length=100, description="通知ID列表")


class NotificationSearchQuery(BaseModel):
    """通知搜索查询模型"""
    type: Optional[int] = Field(None, ge=1, le=5, description="通知类型筛选")
    receiver_id: Optional[str] = Field(None, max_length=64, description="接收者ID筛选")
    receiver_type: Optional[int] = Field(None, ge=1, le=3, description="接收者类型筛选")
    status: Optional[int] = Field(None, ge=0, le=3, description="通知状态筛选")
    start_date: Optional[datetime] = Field(None, description="开始日期筛选")
    end_date: Optional[datetime] = Field(None, description="结束日期筛选")


class NotificationUnreadCount(BaseModel):
    """未读通知数量模型"""
    receiver_id: str = Field(..., min_length=1, max_length=64, description="接收者ID")
    receiver_type: Optional[int] = Field(None, ge=1, le=3, description="接收者类型筛选")


class NotificationListResponse(BaseModel):
    """通知列表响应模型"""
    total: int = Field(..., description="总记录数")
    unread_count: int = Field(..., description="未读数量")
    items: List[NotificationResponse] = Field(..., description="通知列表")
