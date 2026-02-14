"""Course Pydantic Schemas

课程相关 Pydantic 模型
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CourseBase(BaseModel):
    """课程基础模型"""
    name: str
    code: str
    description: Optional[str] = None
    duration_minutes: int = 60
    price: float = 0.0


class CourseCreate(CourseBase):
    """课程创建模型"""
    pass


class CourseUpdate(BaseModel):
    """课程更新模型"""
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None


class CourseResponse(CourseBase):
    """课程响应模型"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
