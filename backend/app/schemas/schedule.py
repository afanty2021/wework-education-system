"""排课 Pydantic Schemas

排课相关 Pydantic 模型
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ScheduleBase(BaseModel):
    """排课基础模型"""
    course_id: int = Field(..., description="课程ID")
    teacher_id: int = Field(..., description="教师ID")
    classroom_id: int = Field(..., description="教室ID")
    department_id: Optional[int] = Field(None, description="校区ID")
    start_time: datetime = Field(..., description="开始时间")
    end_time: datetime = Field(..., description="结束时间")
    week_day: Optional[int] = Field(None, ge=1, le=7, description="星期几 1-7")
    recurring_type: Optional[str] = Field(None, max_length=20, description="循环类型: single/weekly/biweekly")
    recurring_id: Optional[str] = Field(None, max_length=50, description="关联的循环ID")
    max_students: int = Field(30, ge=1, description="最大人数")
    enrolled_count: int = Field(0, ge=0, description="已报名人数")
    notes: Optional[str] = Field(None, description="备注")


class ScheduleCreate(ScheduleBase):
    """排课创建模型"""
    pass


class ScheduleUpdate(BaseModel):
    """排课更新模型"""
    course_id: Optional[int] = Field(None, description="课程ID")
    teacher_id: Optional[int] = Field(None, description="教师ID")
    classroom_id: Optional[int] = Field(None, description="教室ID")
    department_id: Optional[int] = Field(None, description="校区ID")
    start_time: Optional[datetime] = Field(None, description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    week_day: Optional[int] = Field(None, ge=1, le=7, description="星期几 1-7")
    recurring_type: Optional[str] = Field(None, max_length=20, description="循环类型: single/weekly/biweekly")
    recurring_id: Optional[str] = Field(None, max_length=50, description="关联的循环ID")
    max_students: Optional[int] = Field(None, ge=1, description="最大人数")
    enrolled_count: Optional[int] = Field(None, ge=0, description="已报名人数")
    status: Optional[int] = Field(None, ge=1, le=4, description="状态: 1:已安排 2:已上课 3:已取消 4:已调课")
    notes: Optional[str] = Field(None, description="备注")


class ScheduleResponse(ScheduleBase):
    """排课响应模型"""
    id: int
    status: int
    created_by: Optional[int]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ScheduleEnroll(BaseModel):
    """学员报名模型"""
    student_id: int = Field(..., description="学员ID")
    count: int = Field(1, ge=1, description="报名人数")


class ScheduleConflictCheck(BaseModel):
    """排课冲突检测模型"""
    teacher_id: int = Field(..., description="教师ID")
    classroom_id: int = Field(..., description="教室ID")
    start_time: datetime = Field(..., description="开始时间")
    end_time: datetime = Field(..., description="结束时间")
    exclude_schedule_id: Optional[int] = Field(None, description="排除的排课ID（用于更新时）")


class ScheduleConflictResponse(BaseModel):
    """排课冲突响应模型"""
    has_conflict: bool = Field(..., description="是否存在冲突")
    teacher_conflicts: list[int] = Field(default_factory=list, description="教师冲突的排课ID列表")
    classroom_conflicts: list[int] = Field(default_factory=list, description="教室冲突的排课ID列表")
    course_conflicts: list[int] = Field(default_factory=list, description="课程冲突的排课ID列表")


__all__ = [
    "ScheduleBase",
    "ScheduleCreate",
    "ScheduleUpdate",
    "ScheduleResponse",
    "ScheduleEnroll",
    "ScheduleConflictCheck",
    "ScheduleConflictResponse",
]
