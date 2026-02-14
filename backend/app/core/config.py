"""Pydantic Settings Configuration

应用配置管理
"""
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


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
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/education_db"

    # Redis 配置
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT 配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
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

    # Celery 配置
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_URL: str = "redis://localhost:6379/2"

    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
