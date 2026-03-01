"""
学员模型

表: students
说明: 学员信息表
"""

from typing import Optional, List
from sqlmodel import SQLModel, Field, JSON
from datetime import datetime, date


class Student(SQLModel, table=True):
    """学员模型"""
    __tablename__ = "students"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, description="学员姓名")
    nickname: Optional[str] = Field(default=None, max_length=50, description="昵称")
    gender: Optional[int] = Field(default=None, description="性别: 1:男 2:女")
    birthday: Optional[date] = Field(default=None, description="生日")
    mobile: Optional[str] = Field(default=None, max_length=20, description="手机号")
    parent_name: Optional[str] = Field(default=None, max_length=50, description="家长姓名")
    parent_wework_id: Optional[str] = Field(default=None, max_length=64, description="家长企业微信ID")
    parent_mobile: Optional[str] = Field(default=None, max_length=20, description="家长手机号")
    source: Optional[str] = Field(default=None, max_length=50, description="来源: 线上推广/朋友介绍/地推等")
    status: int = Field(default=1, description="状态: 1:潜在 2:在读 3:已流失")
    tags: Optional[List[str]] = Field(default=None, sa_type=JSON, description="标签列表")
    notes: Optional[str] = Field(default=None, description="备注")

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
