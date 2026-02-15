"""Student Pydantic Schemas

学员相关 Pydantic 模型
"""
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class StudentBase(BaseModel):
    """学员基础模型"""
    name: str = Field(..., min_length=1, max_length=50, description="学员姓名")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    gender: Optional[int] = Field(None, ge=1, le=2, description="性别: 1:男 2:女")
    birthday: Optional[date] = Field(None, description="生日")
    mobile: Optional[str] = Field(None, max_length=20, description="手机号")
    parent_name: Optional[str] = Field(None, max_length=50, description="家长姓名")
    parent_wework_id: Optional[str] = Field(None, max_length=64, description="家长企业微信ID")
    parent_mobile: Optional[str] = Field(None, max_length=20, description="家长手机号")
    source: Optional[str] = Field(None, max_length=50, description="来源: 线上推广/朋友介绍/地推等")
    tags: Optional[str] = Field(None, description="标签 JSON数组")
    notes: Optional[str] = Field(None, description="备注")


class StudentCreate(StudentBase):
    """学员创建模型

    创建学员时的必填和可选字段
    """
    status: int = Field(1, ge=1, le=3, description="状态: 1:潜在 2:在读 3:已流失")


class StudentUpdate(BaseModel):
    """学员更新模型

    更新学员时所有字段都是可选的
    """
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="学员姓名")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    gender: Optional[int] = Field(None, ge=1, le=2, description="性别: 1:男 2:女")
    birthday: Optional[date] = Field(None, description="生日")
    mobile: Optional[str] = Field(None, max_length=20, description="手机号")
    parent_name: Optional[str] = Field(None, max_length=50, description="家长姓名")
    parent_wework_id: Optional[str] = Field(None, max_length=64, description="家长企业微信ID")
    parent_mobile: Optional[str] = Field(None, max_length=20, description="家长手机号")
    source: Optional[str] = Field(None, max_length=50, description="来源")
    status: Optional[int] = Field(None, ge=1, le=3, description="状态: 1:潜在 2:在读 3:已流失")
    tags: Optional[str] = Field(None, description="标签 JSON数组")
    notes: Optional[str] = Field(None, description="备注")


class StudentResponse(StudentBase):
    """学员响应模型

    返回给前端的学员信息
    """
    id: int
    status: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StudentListResponse(BaseModel):
    """学员列表响应模型

    用于分页查询的响应
    """
    total: int = Field(..., description="学员总数")
    students: List[StudentResponse] = Field(..., description="学员列表")


class StudentTagCreate(BaseModel):
    """添加标签模型"""
    tag: str = Field(..., min_length=1, max_length=50, description="标签名称")


class StudentSearchQuery(BaseModel):
    """学员搜索查询模型"""
    keyword: Optional[str] = Field(None, description="搜索关键词")
    status: Optional[int] = Field(None, ge=1, le=3, description="状态筛选")
    source: Optional[str] = Field(None, description="来源筛选")
    tag: Optional[str] = Field(None, description="标签筛选")
    skip: int = Field(0, ge=0, description="跳过记录数")
    limit: int = Field(100, ge=1, le=100, description="返回记录数")
