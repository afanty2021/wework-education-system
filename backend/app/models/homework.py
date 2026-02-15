"""
作业模型

表: homeworks, homework_submissions
"""

from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class Homework(SQLModel, table=True):
    """作业模型"""
    __tablename__ = "homeworks"

    id: Optional[int] = Field(default=None, primary_key=True)
    schedule_id: int = Field(foreign_key="schedules.id", description="排课ID")
    title: str = Field(max_length=200, description="作业标题")
    content: Optional[str] = Field(default=None, description="作业内容")
    images: Optional[str] = Field(default=None, description="图片 JSON数组")
    attachments: Optional[str] = Field(default=None, description="附件 JSON数组")
    deadline: Optional[datetime] = Field(default=None, description="截止时间")
    publish_time: Optional[datetime] = Field(default=None, description="发布时间")
    created_by: int = Field(foreign_key="users.id", description="创建人")
    status: int = Field(default=1, description="状态: 1:草稿 2:已发布 3:已结束")

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class HomeworkSubmission(SQLModel, table=True):
    """作业提交模型"""
    __tablename__ = "homework_submissions"

    id: Optional[int] = Field(default=None, primary_key=True)
    homework_id: int = Field(foreign_key="homeworks.id", description="作业ID")
    student_id: int = Field(foreign_key="students.id", description="学员ID")
    content: Optional[str] = Field(default=None, description="提交内容")
    images: Optional[str] = Field(default=None, description="提交图片")
    attachments: Optional[str] = Field(default=None, description="提交附件")
    submit_time: Optional[datetime] = Field(default=None, description="提交时间")
    score: Optional[int] = Field(default=None, description="评分 1-100")
    feedback: Optional[str] = Field(default=None, description="教师反馈")
    graded_by: Optional[int] = Field(default=None, foreign_key="users.id", description="批改人")
    graded_at: Optional[datetime] = Field(default=None, description="批改时间")
    status: int = Field(default=1, description="状态: 1:待批改 2:已批改")

    created_at: datetime = Field(default_factory=datetime.now)
