"""
用户模型

表: users
说明: 教师/员工用户表
"""

from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class User(SQLModel, table=True):
    """用户模型"""
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    wework_id: str = Field(max_length=64, unique=True, index=True, description="企业微信用户ID")
    name: str = Field(max_length=50, description="姓名")
    mobile: Optional[str] = Field(default=None, max_length=20, description="手机号")
    avatar: Optional[str] = Field(default=None, max_length=500, description="头像URL")
    role: str = Field(default="teacher", max_length=20, description="角色: admin/teacher/finance")
    department_id: Optional[int] = Field(default=None, description="所属校区")
    status: int = Field(default=1, description="状态: 1:active 0:inactive")

    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")
