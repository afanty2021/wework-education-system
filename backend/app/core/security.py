"""Security Utilities

安全认证相关工具函数

功能:
- 密码哈希和验证
- JWT token生成和验证
- Token依赖注入
"""
import logging
from datetime import datetime, timedelta, UTC
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from app.core.config import settings

logger = logging.getLogger(__name__)

# 密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Bearer Token
security = HTTPBearer()


class TokenPayload(BaseModel):
    """Token载荷"""
    sub: str  # 用户ID
    role: str  # 用户角色
    exp: Optional[datetime] = None


class TokenResponse(BaseModel):
    """Token响应"""
    access_token: str
    token_type: str = "bearer"


class AuthService:
    """认证服务"""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """生成密码哈希"""
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        创建JWT token

        Args:
            data: 要编码的数据
            expires_delta: 过期时间增量

        Returns:
            str: JWT token
        """
        to_encode = data.copy()
        expire = datetime.now(UTC) + (
            expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> TokenPayload:
        """
        解码JWT token

        Args:
            token: JWT token

        Returns:
            TokenPayload: 解码后的数据

        Raises:
            HTTPException: token无效时抛出
        """
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            return TokenPayload(**payload)
        except JWTError as e:
            logger.error(f"JWT解码失败: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证凭据",
                headers={"WWW-Authenticate": "Bearer"},
            )


auth_service = AuthService()


# 导出便捷函数（保持向后兼容）
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    创建JWT token

    Args:
        data: 要编码的数据
        expires_delta: 过期时间增量

    Returns:
        str: JWT token
    """
    return auth_service.create_access_token(data, expires_delta)


def decode_token(token: str) -> TokenPayload:
    """
    解码JWT token

    Args:
        token: JWT token

    Returns:
        TokenPayload: 解码后的数据

    Raises:
        HTTPException: token无效时抛出
    """
    return auth_service.decode_token(token)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenPayload:
    """
    获取当前用户依赖

    Returns:
        TokenPayload: 当前用户信息
    """
    token = credentials.credentials
    return auth_service.decode_token(token)


async def get_current_active_user(
    current_user: TokenPayload = Depends(get_current_user)
) -> TokenPayload:
    """
    获取当前活跃用户

    可以扩展为检查用户状态
    """
    return current_user


# 保持向后兼容的旧接口
from fastapi import Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


async def get_current_user_legacy(
    token: Optional[str] = Security(api_key_header),
) -> Optional[dict]:
    """
    旧版获取当前用户（兼容API Key方式）
    """
    if not token:
        return None
    try:
        if token.startswith("Bearer "):
            token = token[7:]
        payload = auth_service.decode_token(token)
        return {"sub": payload.sub, "role": payload.role}
    except HTTPException:
        return None
