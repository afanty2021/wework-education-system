"""Schedule Pydantic Schemas

排课相关 Pydantic 模型
"""
from datetime import datetime, time
from typing import Optional

from pydantic import BaseModel


class ScheduleBase(BaseModel):
    """排课基础模型"""
    course_id: int
    teacher_id: int
    classroom: str
    week_day: int  # 1-7 (周一到周日)
    start_time: time
    end_time: time
    start_date: datetime
    end_date: datetime


class ScheduleCreate(ScheduleBase):
    """排课创建模型"""
    pass


class ScheduleUpdate(BaseModel):
    """排课更新模型"""
    course_id: Optional[int] = None
    teacher_id: Optional[int] = None
    classroom: Optional[str] = None
    week_day: Optional[int] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None


class ScheduleResponse(ScheduleBase):
    """排课响应模型"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
