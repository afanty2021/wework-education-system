"""Homework Pydantic Schemas

作业相关 Pydantic 模型
"""
from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel


class HomeworkBase(BaseModel):
    """作业基础模型"""
    course_id: int
    title: str
    content: str
    due_date: Optional[date] = None
    max_score: int = 100


class HomeworkCreate(HomeworkBase):
    """作业创建模型"""
    pass


class HomeworkUpdate(BaseModel):
    """作业更新模型"""
    title: Optional[str] = None
    content: Optional[str] = None
    due_date: Optional[date] = None
    max_score: Optional[int] = None
    is_active: Optional[bool] = None


class HomeworkResponse(HomeworkBase):
    """作业响应模型"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HomeworkSubmissionCreate(BaseModel):
    """作业提交创建模型"""
    homework_id: int
    content: str
    attachments: Optional[list] = None


class HomeworkSubmissionResponse(BaseModel):
    """作业提交响应模型"""
    id: int
    homework_id: int
    student_id: int
    content: str
    attachments: Optional[list] = None
    score: Optional[int] = None
    teacher_remark: Optional[str] = None
    submitted_at: datetime

    class Config:
        from_attributes = True
