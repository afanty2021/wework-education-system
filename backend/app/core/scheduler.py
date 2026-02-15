"""APScheduler Task Scheduler

定时任务调度器，支持：
- Cron表达式调度
- 固定间隔调度
- 任务执行日志记录
- 失败重试机制
"""
import logging
from datetime import datetime
from typing import Callable, Optional, Any, Dict
from functools import wraps

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor

from app.core.config import settings


logger = logging.getLogger(__name__)


# ==================== 任务装饰器 ====================

def log_task_execution(task_name: str):
    """
    记录任务执行情况的装饰器

    Args:
        task_name: 任务名称
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = datetime.now()
            logger.info(f"任务开始执行: {task_name}")

            try:
                result = await func(*args, **kwargs)

                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()

                logger.info(
                    f"任务执行成功: {task_name}, "
                    f"耗时={duration:.2f}秒, "
                    f"结果={result}"
                )

                return result

            except Exception as e:
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()

                logger.error(
                    f"任务执行失败: {task_name}, "
                    f"耗时={duration:.2f}秒, "
                    f"错误={str(e)}",
                    exc_info=True
                )

                raise

        return wrapper
    return decorator


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """
    失败重试装饰器

    Args:
        max_retries: 最大重试次数
        delay: 重试延迟（秒）
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            import asyncio

            last_exception = None

            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)

                except Exception as e:
                    last_exception = e
                    logger.warning(
                        f"任务执行失败，准备重试: "
                        f"尝试={attempt + 1}/{max_retries}, "
                        f"错误={str(e)}"
                    )

                    if attempt < max_retries - 1:
                        await asyncio.sleep(delay)

            logger.error(f"任务重试{max_retries}次后仍然失败")
            raise last_exception

        return wrapper
    return decorator


# ==================== 任务调度器 ====================

class TaskScheduler:
    """异步任务调度器

    提供完整的任务调度功能，包括：
    - Cron表达式调度
    - 固定间隔调度
    - 任务执行日志
    - 失败重试
    - 任务状态监控
    """

    def __init__(self):
        # 配置任务存储（使用内存存储）
        jobstores = {
            "default": MemoryJobStore()
        }

        # 配置执行器
        executors = {
            "default": AsyncIOExecutor()
        }

        # 配置任务默认选项
        job_defaults = {
            "coalesce": True,          # 合并多次触发的任务
            "max_instances": 1,          # 同一任务最多1个实例运行
            "misfire_grace_time": 60     # 错过执行宽限时间（秒）
        }

        # 创建调度器
        self.scheduler = AsyncIOScheduler(
            jobstores=jobstores,
            executors=executors,
            job_defaults=job_defaults,
            timezone="Asia/Shanghai"
        )

        # 添加事件监听器
        self._add_event_listeners()

        # 任务注册表
        self._registered_tasks: Dict[str, Dict[str, Any]] = {}

    def _add_event_listeners(self):
        """添加事件监听器"""
        def job_executed_listener(event):
            """任务执行完成监听器"""
            job_id = event.job_id
            logger.info(f"任务执行完成: job_id={job_id}")

        def job_error_listener(event):
            """任务执行错误监听器"""
            job_id = event.job_id
            exception = event.exception
            logger.error(f"任务执行错误: job_id={job_id}, exception={exception}")

        self.scheduler.add_listener(
            job_executed_listener,
            EVENT_JOB_EXECUTED
        )
        self.scheduler.add_listener(
            job_error_listener,
            EVENT_JOB_ERROR
        )

    def start(self):
        """启动调度器"""
        if not self.scheduler.running:
            logger.info("启动任务调度器")
            self.scheduler.start()
        else:
            logger.warning("调度器已在运行中")

    def shutdown(self, wait: bool = True):
        """关闭调度器

        Args:
            wait: 是否等待任务完成
        """
        if self.scheduler.running:
            logger.info(f"关闭任务调度器: wait={wait}")
            self.scheduler.shutdown(wait=wait)

    def add_job(
        self,
        func: Callable,
        trigger: str = "interval",
        task_id: Optional[str] = None,
        task_name: Optional[str] = None,
        **trigger_args
    ):
        """添加任务

        Args:
            func: 任务函数
            trigger: 触发器类型 (cron/interval)
            task_id: 任务ID（唯一标识）
            task_name: 任务名称（用于日志）
            **trigger_args: 触发器参数

        Returns:
            Job: 添加的任务对象
        """
        if trigger == "cron":
            job_trigger = CronTrigger(**trigger_args)
        elif trigger == "interval":
            job_trigger = IntervalTrigger(**trigger_args)
        else:
            raise ValueError(f"不支持的触发器类型: {trigger}")

        # 使用装饰器包装任务函数
        wrapped_func = log_task_execution(task_name or task_id or "unknown")(func)

        # 添加任务到调度器
        job = self.scheduler.add_job(
            func=wrapped_func,
            trigger=job_trigger,
            id=task_id,
            name=task_name
        )

        # 记录到任务注册表
        if task_id:
            self._registered_tasks[task_id] = {
                "name": task_name,
                "trigger": trigger,
                "trigger_args": trigger_args,
                "func": func
            }

        logger.info(
            f"任务已添加: id={task_id}, "
            f"name={task_name}, "
            f"trigger={trigger}"
        )

        return job

    def remove_job(self, task_id: str):
        """移除任务

        Args:
            task_id: 任务ID
        """
        try:
            self.scheduler.remove_job(task_id)
            self._registered_tasks.pop(task_id, None)
            logger.info(f"任务已移除: task_id={task_id}")
        except Exception as e:
            logger.error(f"移除任务失败: task_id={task_id}, error={e}")

    def pause_job(self, task_id: str):
        """暂停任务

        Args:
            task_id: 任务ID
        """
        try:
            self.scheduler.pause_job(task_id)
            logger.info(f"任务已暂停: task_id={task_id}")
        except Exception as e:
            logger.error(f"暂停任务失败: task_id={task_id}, error={e}")

    def resume_job(self, task_id: str):
        """恢复任务

        Args:
            task_id: 任务ID
        """
        try:
            self.scheduler.resume_job(task_id)
            logger.info(f"任务已恢复: task_id={task_id}")
        except Exception as e:
            logger.error(f"恢复任务失败: task_id={task_id}, error={e}")

    def get_jobs(self):
        """获取所有任务

        Returns:
            List[Job]: 任务列表
        """
        return self.scheduler.get_jobs()

    def get_job(self, task_id: str):
        """获取指定任务

        Args:
            task_id: 任务ID

        Returns:
            Optional[Job]: 任务对象或None
        """
        return self.scheduler.get_job(task_id)

    def get_registered_tasks(self) -> Dict[str, Dict[str, Any]]:
        """获取已注册的任务列表

        Returns:
            Dict: 任务注册表
        """
        return self._registered_tasks.copy()

    def print_jobs_status(self):
        """打印所有任务状态"""
        jobs = self.get_jobs()

        logger.info("=" * 60)
        logger.info("任务调度器状态")
        logger.info("=" * 60)

        if not jobs:
            logger.info("当前无已注册的任务")
        else:
            for job in jobs:
                next_run_time = job.next_run_time
                logger.info(
                    f"任务ID: {job.id}\n"
                    f"  名称: {job.name}\n"
                    f"  触发器: {job.trigger}\n"
                    f"  下次运行: {next_run_time}\n"
                )

        logger.info("=" * 60)


# ==================== 全局调度器实例 ====================

scheduler = TaskScheduler()


# ==================== 任务注册函数 ====================

def register_default_tasks():
    """注册默认定时任务

    在应用启动时调用此函数，注册所有默认的定时任务。
    """
    # 导入任务模块
    from app.tasks.reminders import (
        check_contract_expiry_reminders,
        check_class_reminders,
        send_birthday_greetings
    )
    from app.tasks.contract_expiry import (
        check_and_mark_expired_contracts,
        calculate_remaining_value
    )
    from app.tasks.statistics import (
        generate_daily_summary,
        analyze_trends
    )

    # 每日上午9点检查合同到期提醒
    scheduler.add_job(
        func=check_contract_expiry_reminders,
        trigger="cron",
        task_id="contract_expiry_reminders",
        task_name="合同到期提醒",
        hour=9,
        minute=0
    )

    # 每2小时检查一次排课提醒
    scheduler.add_job(
        func=check_class_reminders,
        trigger="interval",
        task_id="class_reminders",
        task_name="排课提醒",
        hours=2
    )

    # 每日上午9点发送生日祝福
    scheduler.add_job(
        func=send_birthday_greetings,
        trigger="cron",
        task_id="birthday_greetings",
        task_name="生日祝福",
        hour=9,
        minute=0
    )

    # 每日凌晨0点检查并标记过期合同
    scheduler.add_job(
        func=check_and_mark_expired_contracts,
        trigger="cron",
        task_id="check_expired_contracts",
        task_name="检查过期合同",
        hour=0,
        minute=0
    )

    # 每日上午10点计算合同剩余价值
    scheduler.add_job(
        func=calculate_remaining_value,
        trigger="cron",
        task_id="calculate_remaining_value",
        task_name="计算合同剩余价值",
        hour=10,
        minute=0
    )

    # 每日凌晨1点生成每日统计汇总
    scheduler.add_job(
        func=generate_daily_summary,
        trigger="cron",
        task_id="daily_summary",
        task_name="每日统计汇总",
        hour=1,
        minute=0
    )

    # 每周日凌晨2点分析趋势（30天）
    scheduler.add_job(
        func=lambda: analyze_trends(days=30),
        trigger="cron",
        task_id="weekly_trend_analysis",
        task_name="每周趋势分析",
        day_of_week=0,  # 周日
        hour=2,
        minute=0
    )

    logger.info("默认定时任务注册完成")


# ==================== 辅助函数 ====================

def get_cron_expression(hour: int, minute: int, day_of_week: Optional[int] = None) -> str:
    """
    生成Cron表达式

    Args:
        hour: 小时 (0-23)
        minute: 分钟 (0-59)
        day_of_week: 星期几 (0-6, None表示每天)

    Returns:
        str: Cron表达式

    Examples:
        >>> get_cron_expression(9, 0)
        "0 9 * * *"
        >>> get_cron_expression(9, 0, 1)
        "0 9 * * 1"
    """
    minute_part = str(minute)
    hour_part = str(hour)
    day_month_part = "*"
    month_part = "*"
    day_week_part = str(day_of_week) if day_of_week is not None else "*"

    return f"{minute_part} {hour_part} {day_month_part} {month_part} {day_week_part}"


def parse_interval_to_hours(interval: str) -> float:
    """
    解析时间间隔字符串为小时数

    Args:
        interval: 时间间隔字符串 (e.g., "2h", "30m", "1d")

    Returns:
        float: 小时数

    Examples:
        >>> parse_interval_to_hours("2h")
        2.0
        >>> parse_interval_to_hours("30m")
        0.5
        >>> parse_interval_to_hours("1d")
        24.0
    """
    interval = interval.lower().strip()

    if interval.endswith("h"):
        return float(interval[:-1])
    elif interval.endswith("m"):
        return float(interval[:-1]) / 60
    elif interval.endswith("d"):
        return float(interval[:-1]) * 24
    else:
        raise ValueError(f"无法解析时间间隔: {interval}")
