"""APScheduler Task Scheduler

定时任务调度器
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from app.core.config import settings


class TaskScheduler:
    """异步任务调度器"""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    def start(self):
        """启动调度器"""
        if not self.scheduler.running:
            self.scheduler.start()

    def shutdown(self):
        """关闭调度器"""
        if self.scheduler.running:
            self.scheduler.shutdown()

    def add_job(
        self,
        func,
        trigger: str = "interval",
        **trigger_args,
    ):
        """添加任务"""
        if trigger == "cron":
            job_trigger = CronTrigger(**trigger_args)
        elif trigger == "interval":
            job_trigger = IntervalTrigger(**trigger_args)
        else:
            raise ValueError(f"Unsupported trigger type: {trigger}")

        self.scheduler.add_job(func, job_trigger)


scheduler = TaskScheduler()
