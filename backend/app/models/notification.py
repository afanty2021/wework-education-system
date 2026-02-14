"""SQLModel Notification Model

通知消息模型
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Integer, String, Text, Boolean, SQLModel


class Notification(SQLModel, table=True):
    """通知消息模型"""
    id: Optional[int] = Column(Integer, primary_key=True, index=True)
    title: str = Column(String(200), nullable=False)
    content: str = Column(Text, nullable=False)
    notification_type: str = Column(String(50), nullable=False)  # system, course, homework, payment, etc.
    target_type: Optional[str] = Column(String(50), nullable=True)  # all, student, teacher, specific
    target_id: Optional[int] = Column(Integer, nullable=True)
    is_read: bool = Column(Boolean, default=False)
    read_at: Optional[datetime] = Column(DateTime, nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Notification(id={self.id}, title={self.title})>"
