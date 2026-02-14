"""Student Pydantic Schemas

学员相关 Pydantic 模型
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class StudentBase(BaseModel):
    """学员基础模型"""
    name: str
    phone: str
    email: Optional[EmailStr] = None
    wechat_openid: Optional[str] = None
    parent_phone: Optional[str] = None
    remark: Optional[str] = None


class StudentCreate(StudentBase):
    """学员创建模型"""
    pass


class StudentUpdate(BaseModel):
    """学员更新模型"""
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    wechat_openid: Optional[str] = None
    parent_phone: Optional[str] = None
    remark: Optional[str] = None


class StudentResponse(StudentBase):
    """学员响应模型"""
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
