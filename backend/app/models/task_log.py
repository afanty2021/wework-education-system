"""任务执行日志模型

表: task_logs
说明: 定时任务执行日志记录
"""

from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class TaskLog(SQLModel, table=True):
    """任务执行日志模型"""
    __tablename__ = "task_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: str = Field(max_length=100, index=True, description="任务ID")
    task_name: str = Field(max_length=200, description="任务名称")
    trigger_type: str = Field(max_length=20, description="触发器类型: cron/interval")
    trigger_args: Optional[str] = Field(default=None, description="触发器参数JSON")
    start_time: datetime = Field(description="开始时间")
    end_time: Optional[datetime] = Field(default=None, description="结束时间")
    duration: Optional[float] = Field(default=None, description="执行耗时（秒）")
    status: int = Field(default=1, description="状态: 1:运行中 2:成功 3:失败")
    result: Optional[str] = Field(default=None, description="执行结果JSON")
    error_message: Optional[str] = Field(default=None, description="错误信息")
    retry_count: int = Field(default=0, description="重试次数")

    created_at: datetime = Field(default_factory=datetime.now)


class TaskStatistics(SQLModel, table=True):
    """任务统计模型"""
    __tablename__ = "task_statistics"

    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: str = Field(max_length=100, index=True, description="任务ID")
    task_name: str = Field(max_length=200, description="任务名称")
    stat_date: datetime = Field(description="统计日期")
    total_runs: int = Field(default=0, description="总执行次数")
    success_runs: int = Field(default=0, description="成功次数")
    failed_runs: int = Field(default=0, description="失败次数")
    avg_duration: Optional[float] = Field(default=None, description="平均执行时长（秒）")
    max_duration: Optional[float] = Field(default=None, description="最大执行时长（秒）")
    min_duration: Optional[float] = Field(default=None, description="最小执行时长（秒）")
    last_run_time: Optional[datetime] = Field(default=None, description="最后执行时间")
    last_run_status: Optional[int] = Field(default=None, description="最后执行状态")

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
