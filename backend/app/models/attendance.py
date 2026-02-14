"""SQLModel Attendance Model

考勤数据模型
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Integer, String, ForeignKey, Text, SQLModel


class Attendance(SQLModel, table=True):
    """考勤模型"""
    id: Optional[int] = Column(Integer, primary_key=True, index=True)
    student_id: int = Column(Integer, ForeignKey("student.id"), nullable=False, index=True)
    schedule_id: int = Column(Integer, ForeignKey("schedule.id"), nullable=False, index=True)
    attendance_date: datetime = Column(DateTime, nullable=False, index=True)
    status: str = Column(String(20), nullable=False)  # present, absent, late, leave
    check_in_time: Optional[datetime] = Column(DateTime, nullable=True)
    check_out_time: Optional[datetime] = Column(DateTime, nullable=True)
    duration_hours: float = Column(default=0.0)
    remark: Optional[str] = Column(Text, nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: Optional[datetime] = Column(DateTime, default=None, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Attendance(id={self.id}, student_id={self.student_id}, status={self.status})>"
