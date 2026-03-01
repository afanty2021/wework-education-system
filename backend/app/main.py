"""FastAPI Application Entry Point

企业微信教务系统后端入口
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.api import exceptions
from app.core.config import settings
from app.core.db import engine, create_db_and_tables
from app.core.logging import setup_logging
from app.core.scheduler import scheduler, register_default_tasks
from app.api.v1 import api_router
from app.api.v2 import api_router as api_router_v2

# 初始化日志配置
setup_logging(level="DEBUG" if settings.DEBUG else "INFO")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info(f"应用启动 - {settings.PROJECT_NAME} v{settings.VERSION}")

    # Startup: 创建数据库表并启动调度器
    await create_db_and_tables()
    logger.info("数据库表初始化完成")

    # 注册并启动任务调度器
    register_default_tasks()
    scheduler.start()
    logger.info("任务调度器已启动")

    yield

    # Shutdown: 关闭调度器
    scheduler.shutdown(wait=True)
    logger.info("应用已关闭")


def create_app() -> FastAPI:
    """创建FastAPI应用实例"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="企业微信教务管理系统 - 提供课程管理、学员管理、排课、考勤、作业等功能",
        version=settings.VERSION,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS 配置
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 注册路由
    app.include_router(api_router, prefix="/api/v1")
    # API v2 预留
    app.include_router(api_router_v2, prefix="/api")

    # 注册全局异常处理器
    app.add_exception_handler(Exception, exceptions.global_exception_handler)
    app.add_exception_handler(RequestValidationError, exceptions.validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, exceptions.database_exception_handler)

    # 健康检查
    @app.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "ok", "version": settings.VERSION}

    return app


app = create_app()


if __name__ == "__main__":
    import os
    import uvicorn

    environment = os.getenv("ENVIRONMENT", "development")
    is_production = environment == "production"

    print(f"启动环境: {environment}")
    if is_production:
        print("警告: 生产模式启动，已禁用热重载")

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=not is_production and settings.DEBUG,
    )
