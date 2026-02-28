"""Global Exception Handlers

全局异常处理器
"""
import logging
from typing import Any

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """全局异常处理器 - 处理所有未捕获的异常

    Args:
        request: FastAPI 请求对象
        exc: 异常对象

    Returns:
        JSON 格式的错误响应
    """
    logger.error(
        f"全局异常: {request.method} {request.url.path}",
        exc_info=True,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "detail": str(exc) if logger.level == logging.DEBUG else "请联系管理员",
        },
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """请求参数验证异常处理器

    Args:
        request: FastAPI 请求对象
        exc: 验证异常对象

    Returns:
        JSON 格式的验证错误响应
    """
    logger.warning(f"参数验证失败: {request.method} {request.url.path}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": 422,
            "message": "参数验证失败",
            "errors": exc.errors(),
        },
    )


async def database_exception_handler(
    request: Request, exc: SQLAlchemyError
) -> JSONResponse:
    """数据库异常处理器

    Args:
        request: FastAPI 请求对象
        exc: SQLAlchemy 异常对象

    Returns:
        JSON 格式的数据库错误响应
    """
    logger.error(f"数据库错误: {request.method} {request.url.path}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "数据库操作失败",
            "detail": "请稍后重试",
        },
    )
