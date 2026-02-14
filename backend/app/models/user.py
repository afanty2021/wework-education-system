"""SQLModel User Model

用户数据模型
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Integer, String, Boolean, SQLModel


class User(SQLModel, table=True):
    """用户模型"""
    id: Optional[int] = Column(Integer, primary_key=True, index=True)
    username: str = Column(String(50), unique=True, index=True, nullable=False)
    email: str = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password: str = Column(String(255), nullable=False)
    full_name: Optional[str] = Column(String(100), nullable=True)
    is_active: bool = Column(Boolean, default=True)
    is_superuser: bool = Column(Boolean, default=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: Optional[datetime] = Column(DateTime, default=None, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
