"""API Dependencies

API 路由依赖项
"""
from typing import AsyncGenerator, Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.security import get_current_active_user
from app.models.user import User

# OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """获取当前登录用户"""
    # TODO: 实现从数据库获取用户
    pass


async def get_current_teacher(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """获取当前教师用户"""
    # TODO: 验证用户是否为教师角色
    pass


async def get_current_student(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """获取当前学员用户"""
    # TODO: 验证用户是否为学员角色
    pass
