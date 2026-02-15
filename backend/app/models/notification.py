"""
通知消息模型

表: notifications
"""

from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class Notification(SQLModel, table=True):
    """通知消息模型"""
    __tablename__ = "notifications"

    id: Optional[int] = Field(default=None, primary_key=True)
    type: int = Field(description="类型: 1:上课提醒 2:作业通知 3:考勤通知 4:合同通知 5:系统通知")
    receiver_id: str = Field(max_length=64, description="接收者ID")
    receiver_type: int = Field(default=1, description="接收者类型: 1:企业微信 2:家长 3:小程序")
    title: str = Field(max_length=200, description="标题")
    content: Optional[str] = Field(default=None, description="内容")
    url: Optional[str] = Field(default=None, max_length=500, description="跳转链接")
    sent_at: Optional[datetime] = Field(default=None, description="发送时间")
    read_at: Optional[datetime] = Field(default=None, description="阅读时间")
    status: int = Field(default=0, description="状态: 0:pending 1:sent 2:failed 3:read")
    error_msg: Optional[str] = Field(default=None, description="错误信息")

    created_at: datetime = Field(default_factory=datetime.now)
