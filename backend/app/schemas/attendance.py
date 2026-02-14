"""Attendance Pydantic Schemas

考勤相关 Pydantic 模型
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AttendanceBase(BaseModel):
    """考勤基础模型"""
    student_id: int
    schedule_id: int
    attendance_date: datetime
    status: str  # present, absent, late, leave
    remark: Optional[str] = None


class AttendanceCreate(AttendanceBase):
    """考勤创建模型"""
    pass


class AttendanceUpdate(BaseModel):
    """考勤更新模型"""
    status: Optional[str] = None
    remark: Optional[str] = None


class AttendanceResponse(AttendanceBase):
    """考勤响应模型"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
