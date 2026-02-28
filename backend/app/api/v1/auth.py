"""Authentication API Routes

认证相关 API 路由

企业微信OAuth2登录认证接口
"""
import logging
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_db
from app.core.security import (
    TokenResponse,
    TokenPayload,
    auth_service,
    get_current_user,
)
from app.services.auth_service import AuthBusinessService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["认证"])


class WeWorkLoginRequest(BaseModel):
    """企业微信登录请求"""
    code: str


class WeChatMiniAppLoginRequest(BaseModel):
    """微信小程序登录请求"""
    code: str
    user_info: dict | None = None


class UserInfoResponse(BaseModel):
    """用户信息响应"""
    id: int
    name: str
    avatar: str | None = None
    role: str
    wework_id: str | None = None


@router.post("/wework", response_model=TokenResponse)
async def wework_login(
    request: WeWorkLoginRequest,
    session: AsyncSession = Depends(get_db)
):
    """
    企业微信OAuth2登录

    参数:
        code: 企业微信授权码

    返回:
        TokenResponse: 包含access_token
    """
    try:
        token = await AuthBusinessService.wework_login(request.code, session)
        return TokenResponse(access_token=token)
    except Exception as e:
        logger.error(f"企业微信登录失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/me", response_model=UserInfoResponse)
async def get_current_user_info(
    current_user: TokenPayload = Depends(get_current_user)
):
    """
    获取当前用户信息

    需要在实现User模型后启用认证
    """
    # TODO: 从数据库获取完整用户信息
    return UserInfoResponse(
        id=int(current_user.sub),
        name="未知",
        role=current_user.role
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    current_user: TokenPayload = Depends(get_current_user)
):
    """
    刷新访问令牌

    Args:
        current_user: 当前用户信息

    Returns:
        TokenResponse: 新的access_token
    """
    token = auth_service.create_access_token(
        data={"sub": current_user.sub, "role": current_user.role},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return TokenResponse(access_token=token)
