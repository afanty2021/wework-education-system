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

router = APIRouter(tags=["认证"])

# 开发模式账号密码 (生产环境应删除)
DEV_USERNAME = "admin"
DEV_PASSWORD = "admin123"


class LoginRequest(BaseModel):
    """账号密码登录请求"""
    username: str
    password: str


class WeWorkLoginRequest(BaseModel):
    """企业微信登录请求"""
    code: str


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
):
    """
    账号密码登录 (开发模式)

    开发测试用，生产环境应使用企业微信登录
    """
    if request.username == DEV_USERNAME and request.password == DEV_PASSWORD:
        token = auth_service.create_access_token(
            data={"sub": "1", "role": "admin"},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return TokenResponse(access_token=token)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="用户名或密码错误"
    )


class WeChatMiniAppLoginRequest(BaseModel):
    """微信小程序登录请求"""
    code: str
    user_info: dict | None = None


class WeWorkAuthUrlResponse(BaseModel):
    """企业微信授权 URL 响应"""
    auth_url: str
    state: str


class UserInfoResponse(BaseModel):
    """用户信息响应"""
    id: int
    name: str
    avatar: str | None = None
    role: str
    wework_id: str | None = None


@router.get("/wework/url", response_model=WeWorkAuthUrlResponse)
async def get_wework_auth_url():
    """
    获取企业微信授权URL

    返回企业微信OAuth2授权链接，前端可直接跳转或生成二维码
    """
    import secrets
    from app.core.config import settings

    # 生成随机 state 用于防止 CSRF 攻击
    state = secrets.token_urlsafe(16)

    # 构建企业微信授权 URL
    # https://developer.work.weixin.qq.com/document/path/91019
    redirect_uri = f"{settings.FRONTEND_URL}/login/callback"
    auth_url = (
        f"https://open.work.weixin.qq.com/wwopen/sso/qrConnect?"
        f"appid={settings.WEWORK_CORP_ID}"
        f"&agentid={settings.WEWORK_AGENT_ID}"
        f"&redirect_uri={redirect_uri}"
        f"&state={state}"
        f"&usertype=member"
    )

    return WeWorkAuthUrlResponse(auth_url=auth_url, state=state)


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
