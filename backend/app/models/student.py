"""SQLModel Student Model

学员数据模型
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Integer, String, Text, SQLModel


class Student(SQLModel, table=True):
    """学员模型"""
    id: Optional[int] = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(50), nullable=False, index=True)
    phone: str = Column(String(20), unique=True, nullable=False)
    email: Optional[str] = Column(String(100), nullable=True)
    wechat_openid: Optional[str] = Column(String(100), unique=True, nullable=True, index=True)
    parent_phone: Optional[str] = Column(String(20), nullable=True)
    avatar: Optional[str] = Column(String(500), nullable=True)
    remark: Optional[str] = Column(Text, nullable=True)
    status: str = Column(String(20), default="active")  # active, inactive, graduated
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: Optional[datetime] = Column(DateTime, default=None, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Student(id={self.id}, name={self.name})>"
