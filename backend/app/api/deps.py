"""API Dependencies

API 路由依赖项

认证和授权相关的依赖注入函数
"""
from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.security import (
    auth_service,
    get_current_user,
    get_current_active_user,
    TokenPayload,
)
from app.models.user import User


# OAuth2 Scheme (密码模式)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

# HTTP Bearer Scheme (JWT模式)
bearer_scheme = HTTPBearer()


async def get_current_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> TokenPayload:
    """
    从Bearer Token获取当前用户

    Returns:
        TokenPayload: 当前用户信息
    """
    token = credentials.credentials
    return auth_service.decode_token(token)


async def get_current_user_db(
    current_user: TokenPayload = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    从数据库获取当前用户

    Args:
        current_user: Token载荷
        db: 数据库会话

    Returns:
        User: 用户对象

    Raises:
        HTTPException: 用户不存在时抛出
    """
    from sqlalchemy import select
    result = await db.execute(
        select(User).where(User.id == int(current_user.sub))
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_teacher(
    current_user: TokenPayload = Depends(get_current_user_from_token)
) -> TokenPayload:
    """
    验证当前用户是否为教师角色

    Args:
        current_user: 当前用户信息

    Returns:
        TokenPayload: 教师用户信息

    Raises:
        HTTPException: 用户不是教师时抛出
    """
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要教师权限"
        )
    return current_user


async def get_current_admin(
    current_user: TokenPayload = Depends(get_current_user_from_token)
) -> TokenPayload:
    """
    验证当前用户是否为管理员

    Args:
        current_user: 当前用户信息

    Returns:
        TokenPayload: 管理员用户信息

    Raises:
        HTTPException: 用户不是管理员时抛出
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    return current_user


async def get_current_active_user_db(
    user: User = Depends(get_current_user_db)
) -> User:
    """
    验证当前数据库用户是否活跃

    Args:
        user: 数据库用户对象

    Returns:
        User: 活跃用户

    Raises:
        HTTPException: 用户已被禁用时抛出
    """
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已被禁用"
        )
    return user


# 保持向后兼容的旧接口
async def get_current_user_legacy(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    旧版获取当前用户（兼容OAuth2密码模式）

    Args:
        token: OAuth2 token
        db: 数据库会话

    Returns:
        Optional[User]: 用户对象或None
    """
    if not token:
        return None
    try:
        payload = auth_service.decode_token(token)
        result = await db.execute(
            select(User).where(User.id == int(payload.sub))
        )
        return result.scalar_one_or_none()
    except Exception:
        return None
