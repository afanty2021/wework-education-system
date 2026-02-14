"""SQLModel Schedule Model

排课数据模型
"""
from datetime import datetime, time, date
from typing import Optional

from sqlmodel import Column, DateTime, Integer, String, Date, Boolean, ForeignKey, Field, SQLModel


class Schedule(SQLModel, table=True):
    """排课模型"""
    id: Optional[int] = Column(Integer, primary_key=True, index=True)
    course_id: int = Column(Integer, ForeignKey("course.id"), nullable=False, index=True)
    teacher_id: int = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    classroom: str = Column(String(100), nullable=False)
    week_day: int = Column(Integer, nullable=False)  # 1-7 (周一到周日)
    start_time: time = Column(nullable=False)
    end_time: time = Column(nullable=False)
    start_date: date = Column(nullable=False)
    end_date: date = Column(nullable=False)
    max_students: int = Column(Integer, default=20)
    is_active: bool = Column(Boolean, default=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: Optional[datetime] = Column(DateTime, default=None, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Schedule(id={self.id}, course_id={self.course_id})>"
