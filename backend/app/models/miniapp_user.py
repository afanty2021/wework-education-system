"""SQLModel MiniApp User Model

小程序用户数据模型
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Integer, String, Boolean, ForeignKey, SQLModel


class MiniAppUser(SQLModel, table=True):
    """小程序用户模型"""
    id: Optional[int] = Column(Integer, primary_key=True, index=True)
    openid: str = Column(String(100), unique=True, nullable=False, index=True)
    unionid: Optional[str] = Column(String(100), unique=True, nullable=True, index=True)
    student_id: Optional[int] = Column(Integer, ForeignKey("student.id"), nullable=True, index=True)
    nickname: Optional[str] = Column(String(100), nullable=True)
    avatar: Optional[str] = Column(String(500), nullable=True)
    phone: Optional[str] = Column(String(20), nullable=True)
    is_bind: bool = Column(Boolean, default=False)  # 是否已绑定学员
    last_login_at: Optional[datetime] = Column(DateTime, nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: Optional[datetime] = Column(DateTime, default=None, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<MiniAppUser(id={self.id}, openid={self.openid})>"
