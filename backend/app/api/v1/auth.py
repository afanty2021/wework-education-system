"""Authentication API Routes

认证相关 API 路由
"""
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.security import (
    Token,
    User,
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from app.schemas.user import TokenResponse, UserCreate, UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse, tags=["Authentication"])
async def register(user_data: UserCreate) -> UserResponse:
    """用户注册"""
    # TODO: 实现用户注册逻辑
    pass


@router.post("/token", response_model=TokenResponse, tags=["Authentication"])
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> TokenResponse:
    """用户登录获取 Token"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "type": "access"},
        expires_delta=access_token_expires,
    )

    return TokenResponse(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse, tags=["Authentication"])
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> UserResponse:
    """获取当前用户信息"""
    return UserResponse.model_validate(current_user)


@router.post("/refresh", response_model=TokenResponse, tags=["Authentication"])
async def refresh_token(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> TokenResponse:
    """刷新访问令牌"""
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.username, "type": "access"},
        expires_delta=access_token_expires,
    )

    return TokenResponse(access_token=access_token, token_type="bearer")
