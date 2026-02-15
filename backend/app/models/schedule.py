"""
排课模型

表: schedules
说明: 课程安排表
"""

from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class Schedule(SQLModel, table=True):
    """排课模型"""
    __tablename__ = "schedules"

    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="courses.id", description="课程ID")
    teacher_id: int = Field(foreign_key="users.id", index=True, description="教师ID")
    classroom_id: int = Field(foreign_key="classrooms.id", description="教室ID")
    department_id: Optional[int] = Field(default=None, description="校区ID")
    start_time: datetime = Field(description="开始时间")
    end_time: datetime = Field(description="结束时间")
    week_day: Optional[int] = Field(default=None, description="星期几 1-7")
    recurring_type: Optional[str] = Field(default=None, max_length=20, description="循环类型: single/weekly/biweekly")
    recurring_id: Optional[str] = Field(default=None, max_length=50, description="关联的循环ID")
    max_students: int = Field(default=30, description="最大人数")
    enrolled_count: int = Field(default=0, description="已报名人数")
    status: int = Field(default=1, description="状态: 1:已安排 2:已上课 3:已取消 4:已调课")
    notes: Optional[str] = Field(default=None, description="备注")
    created_by: Optional[int] = Field(default=None, foreign_key="users.id", description="创建人")

    created_at: datetime = Field(default_factory=datetime.now)
