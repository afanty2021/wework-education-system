"""Pydantic Settings Configuration

应用配置管理
"""
import os
from typing import List

from pydantic import Field, field_validator, ConfigDict
from pydantic_settings import BaseSettings


def get_default_database_url() -> str:
    """获取默认数据库URL，不包含密码"""
    user = os.getenv("WEWORK_EDU_DB_USER", "postgres")
    host = os.getenv("WEWORK_EDU_DB_HOST", "localhost")
    port = os.getenv("WEWORK_EDU_DB_PORT", "5432")
    name = os.getenv("WEWORK_EDU_DB_NAME", "education_db")
    return f"postgresql://{user}@{host}:{port}/{name}"


class Settings(BaseSettings):
    """应用配置类"""

    # 项目基本信息
    PROJECT_NAME: str = "企业微信教务管理系统"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS 配置
    CORS_ORIGINS: List[str] = Field(default_factory=lambda: [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
    ])

    # 数据库配置
    DATABASE_URL: str = Field(
        default_factory=get_default_database_url,
        description="数据库连接URL，用户名通过环境变量WEWORK_EDU_DB_USER设置，密码通过WEWORK_EDU_DB_PASSWORD设置"
    )
    DATABASE_PASSWORD: str = Field(
        default="",
        description="数据库密码，通过环境变量WEWORK_EDU_DB_PASSWORD设置"
    )

    # Redis 配置
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT 配置
    SECRET_KEY: str = Field(
        default="dev-secret-key-change-in-production",
        description="JWT密钥，生产环境必须通过环境变量WEWORK_EDU_SECRET_KEY设置"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24小时

    # 企业微信配置
    WEWORK_CORP_ID: str = ""
    WEWORK_AGENT_ID: str = ""
    WEWORK_SECRET: str = ""
    WEWORK_TOKEN: str = ""
    WEWORK_ENCODING_AES_KEY: str = ""

    # 微信支付配置
    WECHAT_MCH_ID: str = ""
    WECHAT_MCH_KEY: str = ""
    WECHAT_NOTIFY_URL: str = ""

    # 支付宝配置
    ALIPAY_APP_ID: str = ""
    ALIPAY_PRIVATE_KEY: str = ""
    ALIPAY_PUBLIC_KEY: str = ""
    ALIPAY_NOTIFY_URL: str = ""
    ALIPAY_SANDBOX: bool = False  # 是否使用沙箱环境

    # Celery 配置
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_URL: str = "redis://localhost:6379/2"

    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB

    @field_validator("SECRET_KEY", mode="before")
    @classmethod
    def validate_secret_key(cls, v):
        """验证生产环境必须设置SECRET_KEY"""
        env_secret = os.getenv("WEWORK_EDU_SECRET_KEY")
        if env_secret:
            return env_secret
        if os.getenv("ENVIRONMENT") == "production" and v == "dev-secret-key-change-in-production":
            raise ValueError("生产环境必须设置WEWORK_EDU_SECRET_KEY环境变量")
        return v

    @field_validator("DATABASE_PASSWORD", mode="before")
    @classmethod
    def validate_database_password(cls, v):
        """验证生产环境必须设置数据库密码"""
        if not v:
            return os.getenv("WEWORK_EDU_DB_PASSWORD", "")
        return v

    def get_database_url_with_password(self) -> str:
        """获取包含密码的完整数据库URL"""
        from urllib.parse import urlparse
        parsed = urlparse(self.DATABASE_URL)
        # 如果密码已设置，构建完整URL
        if self.DATABASE_PASSWORD:
            return f"postgresql://{parsed.username}:{self.DATABASE_PASSWORD}@{parsed.hostname}:{parsed.port}{parsed.path}"
        return self.DATABASE_URL

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
