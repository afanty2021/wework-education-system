"""SQLModel Contract Model

合同数据模型
"""
from datetime import datetime, date
from typing import Optional

from sqlmodel import Column, DateTime, Integer, String, Float, Date, ForeignKey, Text, SQLModel


class Contract(SQLModel, table=True):
    """合同模型"""
    id: Optional[int] = Column(Integer, primary_key=True, index=True)
    contract_no: str = Column(String(50), unique=True, nullable=False, index=True)
    student_id: int = Column(Integer, ForeignKey("student.id"), nullable=False, index=True)
    course_id: int = Column(Integer, ForeignKey("course.id"), nullable=False, index=True)
    total_amount: float = Column(Float, nullable=False)
    discount_amount: float = Column(Float, default=0.0)
    actual_amount: float = Column(Float, nullable=False)
    total_hours: float = Column(nullable=False)
    used_hours: float = Column(default=0.0)
    start_date: date = Column(nullable=False)
    end_date: date = Column(nullable=False)
    status: str = Column(String(20), default="active")  # active, expired, terminated, completed
    remark: Optional[str] = Column(Text, nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: Optional[datetime] = Column(DateTime, default=None, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Contract(id={self.id}, contract_no={self.contract_no})>"
