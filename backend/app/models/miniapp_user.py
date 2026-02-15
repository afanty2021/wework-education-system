"""
小程序用户模型

表: miniapp_users
"""

from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class MiniAppUser(SQLModel, table=True):
    """小程序用户模型"""
    __tablename__ = "miniapp_users"

    id: Optional[int] = Field(default=None, primary_key=True)
    openid: str = Field(max_length=100, unique=True, index=True, description="微信openid")
    unionid: Optional[str] = Field(default=None, max_length=100, description="微信unionid")
    platform: str = Field(default="wechat", description="平台: wechat/alipay")
    student_id: Optional[int] = Field(default=None, foreign_key="students.id", description="关联学员")
    nickname: Optional[str] = Field(default=None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(default=None, max_length=500, description="头像")
    phone: Optional[str] = Field(default=None, max_length=20, description="绑定手机号")
    status: int = Field(default=1, description="状态")
    last_login_at: Optional[datetime] = Field(default=None, description="最后登录时间")

    created_at: datetime = Field(default_factory=datetime.now)
