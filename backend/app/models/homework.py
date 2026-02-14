"""SQLModel Homework Model

作业数据模型
"""
from datetime import datetime, date
from typing import Optional

from sqlmodel import Column, DateTime, Integer, String, Date, Text, Boolean, ForeignKey, SQLModel


class Homework(SQLModel, table=True):
    """作业模型"""
    id: Optional[int] = Column(Integer, primary_key=True, index=True)
    course_id: int = Column(Integer, ForeignKey("course.id"), nullable=False, index=True)
    title: str = Column(String(200), nullable=False)
    content: str = Column(Text, nullable=False)
    attachments: Optional[str] = Column(Text, nullable=True)  # JSON格式存储附件路径
    due_date: Optional[date] = Column(Date, nullable=True)
    max_score: int = Column(Integer, default=100)
    is_active: bool = Column(Boolean, default=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: Optional[datetime] = Column(DateTime, default=None, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Homework(id={self.id}, title={self.title})>"


class HomeworkSubmission(SQLModel, table=True):
    """作业提交模型"""
    id: Optional[int] = Column(Integer, primary_key=True, index=True)
    homework_id: int = Column(Integer, ForeignKey("homework.id"), nullable=False, index=True)
    student_id: int = Column(Integer, ForeignKey("student.id"), nullable=False, index=True)
    content: str = Column(Text, nullable=False)
    attachments: Optional[str] = Column(Text, nullable=True)  # JSON格式存储附件路径
    score: Optional[int] = Column(Integer, nullable=True)
    teacher_remark: Optional[str] = Column(Text, nullable=True)
    submitted_at: datetime = Column(DateTime, default=datetime.utcnow)
    graded_at: Optional[datetime] = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<HomeworkSubmission(id={self.id}, homework_id={self.homework_id}, student_id={self.student_id})>"
