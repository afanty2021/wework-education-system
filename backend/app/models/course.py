"""SQLModel Course Model

课程数据模型
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Integer, String, Text, Float, Boolean, SQLModel


class Course(SQLModel, table=True):
    """课程模型"""
    id: Optional[int] = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(100), nullable=False)
    code: str = Column(String(50), unique=True, nullable=False, index=True)
    description: Optional[str] = Column(Text, nullable=True)
    cover_image: Optional[str] = Column(String(500), nullable=True)
    duration_minutes: int = Column(Integer, default=60)
    price: float = Column(Float, default=0.0)
    is_active: bool = Column(Boolean, default=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: Optional[datetime] = Column(DateTime, default=None, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Course(id={self.id}, name={self.name})>"
