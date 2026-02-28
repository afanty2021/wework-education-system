"""Logging Configuration

统一日志配置 - 结构化 JSON 日志
"""
import json
import logging
import sys
from datetime import datetime
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """JSON 格式化器 - 输出结构化日志"""

    def __init__(self, include_extra: bool = True):
        super().__init__()
        self.include_extra = include_extra

    def format(self, record: logging.LogRecord) -> str:
        """格式化日志为 JSON 格式"""
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # 添加异常信息
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # 添加额外字段
        if self.include_extra:
            extra = {
                k: v
                for k, v in record.__dict__.items()
                if k not in logging.LogRecord(
                    "", 0, "", 0, "", (), None
                ).__dict__ and not k.startswith("_")
            }
            if extra:
                log_data["extra"] = extra

        # 添加请求ID（如果存在）
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id

        return json.dumps(log_data, ensure_ascii=False, default=str)


class ContextFilter(logging.Filter):
    """日志上下文过滤器 - 添加请求ID等上下文信息"""

    def __init__(self):
        super().__init__()
        self.request_id = None

    def filter(self, record: logging.LogRecord) -> bool:
        """过滤并添加上下文"""
        if self.request_id:
            record.request_id = self.request_id
        return True


def setup_logging(
    level: str = "INFO",
    json_format: bool = False,
) -> None:
    """配置日志系统

    Args:
        level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: 是否使用 JSON 格式输出
    """
    # 获取根日志记录器
    root_logger = logging.getLogger()

    # 设置日志级别
    log_level = getattr(logging, level.upper(), logging.INFO)
    root_logger.setLevel(log_level)

    # 清除现有处理器
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    # 设置格式化器
    if json_format:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(level)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    console_handler.setFormatter(formatter)

    # 添加处理器
    root_logger.addHandler(console_handler)

    # 设置第三方库日志级别
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """获取日志记录器

    Args:
        name: 日志记录器名称（通常使用 __name__）

    Returns:
        配置好的日志记录器
    """
    return logging.getLogger(name)


# 默认日志配置
setup_logging(level="INFO", json_format=False)
