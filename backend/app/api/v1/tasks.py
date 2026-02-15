"""定时任务管理API

提供定时任务的管理接口：
- 查看所有任务
- 查看任务详情
- 暂停/恢复任务
- 手动触发任务
- 查看任务执行日志
"""
from typing import List, Optional, Dict, Any
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.core.scheduler import scheduler
from app.core.db import async_session_maker
from app.models.task_log import TaskLog, TaskStatistics


router = APIRouter(prefix="/tasks", tags=["定时任务"])


# ==================== Pydantic 模型 ====================

class TaskInfo(BaseModel):
    """任务信息"""
    task_id: str = Field(..., description="任务ID")
    name: str = Field(..., description="任务名称")
    trigger: str = Field(..., description="触发器类型")
    next_run_time: Optional[datetime] = Field(None, description="下次运行时间")


class TaskListResponse(BaseModel):
    """任务列表响应"""
    tasks: List[TaskInfo]
    total: int


class TaskLogEntry(BaseModel):
    """任务执行日志"""
    id: int
    task_id: str
    task_name: str
    trigger_type: str
    start_time: datetime
    end_time: Optional[datetime]
    duration: Optional[float]
    status: int
    result: Optional[str]
    error_message: Optional[str]
    retry_count: int


class TaskLogListResponse(BaseModel):
    """任务日志列表响应"""
    logs: List[TaskLogEntry]
    total: int


class TaskStatisticsResponse(BaseModel):
    """任务统计响应"""
    task_id: str
    task_name: str
    stat_date: datetime
    total_runs: int
    success_runs: int
    failed_runs: int
    avg_duration: Optional[float]
    max_duration: Optional[float]
    min_duration: Optional[float]
    last_run_time: Optional[datetime]
    last_run_status: Optional[int]


# ==================== 任务管理端点 ====================

@router.get("/", response_model=TaskListResponse)
async def list_tasks() -> TaskListResponse:
    """
    获取所有任务列表

    Returns:
        TaskListResponse: 任务列表
    """
    jobs = scheduler.get_jobs()

    tasks = []
    for job in jobs:
        tasks.append(TaskInfo(
            task_id=job.id or "",
            name=job.name or "",
            trigger=str(job.trigger),
            next_run_time=job.next_run_time
        ))

    return TaskListResponse(tasks=tasks, total=len(tasks))


@router.get("/{task_id}", response_model=TaskInfo)
async def get_task(task_id: str) -> TaskInfo:
    """
    获取任务详情

    Args:
        task_id: 任务ID

    Returns:
        TaskInfo: 任务信息

    Raises:
        HTTPException: 任务不存在
    """
    job = scheduler.get_job(task_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"任务不存在: {task_id}"
        )

    return TaskInfo(
        task_id=job.id or "",
        name=job.name or "",
        trigger=str(job.trigger),
        next_run_time=job.next_run_time
    )


@router.post("/{task_id}/pause")
async def pause_task(task_id: str) -> Dict[str, str]:
    """
    暂停任务

    Args:
        task_id: 任务ID

    Returns:
        dict: 操作结果

    Raises:
        HTTPException: 任务不存在
    """
    job = scheduler.get_job(task_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"任务不存在: {task_id}"
        )

    scheduler.pause_job(task_id)

    return {"message": f"任务已暂停: {task_id}"}


@router.post("/{task_id}/resume")
async def resume_task(task_id: str) -> Dict[str, str]:
    """
    恢复任务

    Args:
        task_id: 任务ID

    Returns:
        dict: 操作结果

    Raises:
        HTTPException: 任务不存在
    """
    job = scheduler.get_job(task_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"任务不存在: {task_id}"
        )

    scheduler.resume_job(task_id)

    return {"message": f"任务已恢复: {task_id}"}


@router.post("/{task_id}/trigger")
async def trigger_task(task_id: str) -> Dict[str, str]:
    """
    手动触发任务

    Args:
        task_id: 任务ID

    Returns:
        dict: 操作结果

    Raises:
        HTTPException: 任务不存在或触发失败
    """
    job = scheduler.get_job(task_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"任务不存在: {task_id}"
        )

    try:
        job.modify(next_run_time=datetime.now())
        return {"message": f"任务已触发: {task_id}"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"任务触发失败: {str(e)}"
        )


# ==================== 任务日志端点 ====================

@router.get("/{task_id}/logs", response_model=TaskLogListResponse)
async def get_task_logs(
    task_id: str,
    skip: int = 0,
    limit: int = 50
) -> TaskLogListResponse:
    """
    获取任务执行日志

    Args:
        task_id: 任务ID
        skip: 跳过记录数
        limit: 返回记录数

    Returns:
        TaskLogListResponse: 任务日志列表
    """
    async with async_session_maker() as session:
        from sqlalchemy import select, func

        # 查询总数
        count_query = select(func.count(TaskLog.id)).where(TaskLog.task_id == task_id)
        count_result = await session.execute(count_query)
        total = count_result.scalar_one()

        # 查询日志
        query = (
            select(TaskLog)
            .where(TaskLog.task_id == task_id)
            .order_by(TaskLog.start_time.desc())
            .offset(skip)
            .limit(limit)
        )

        result = await session.execute(query)
        logs = result.scalars().all()

        log_entries = [
            TaskLogEntry(
                id=log.id,
                task_id=log.task_id,
                task_name=log.task_name,
                trigger_type=log.trigger_type,
                start_time=log.start_time,
                end_time=log.end_time,
                duration=log.duration,
                status=log.status,
                result=log.result,
                error_message=log.error_message,
                retry_count=log.retry_count
            )
            for log in logs
        ]

        return TaskLogListResponse(logs=log_entries, total=total)


@router.get("/{task_id}/statistics", response_model=TaskStatisticsResponse)
async def get_task_statistics(task_id: str) -> TaskStatisticsResponse:
    """
    获取任务统计信息

    Args:
        task_id: 任务ID

    Returns:
        TaskStatisticsResponse: 任务统计

    Raises:
        HTTPException: 统计不存在
    """
    async with async_session_maker() as session:
        from sqlalchemy import select
        from app.models.task_log import TaskStatistics

        query = select(TaskStatistics).where(TaskStatistics.task_id == task_id)
        result = await session.execute(query)
        stats = result.scalar_one_or_none()

        if not stats:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"任务统计不存在: {task_id}"
            )

        return TaskStatisticsResponse(
            task_id=stats.task_id,
            task_name=stats.task_name,
            stat_date=stats.stat_date,
            total_runs=stats.total_runs,
            success_runs=stats.success_runs,
            failed_runs=stats.failed_runs,
            avg_duration=stats.avg_duration,
            max_duration=stats.max_duration,
            min_duration=stats.min_duration,
            last_run_time=stats.last_run_time,
            last_run_status=stats.last_run_status
        )


# ==================== 调度器状态端点 ====================

@router.get("/scheduler/status")
async def get_scheduler_status() -> Dict[str, Any]:
    """
    获取调度器状态

    Returns:
        dict: 调度器状态
    """
    jobs = scheduler.get_jobs()
    registered_tasks = scheduler.get_registered_tasks()

    return {
        "running": scheduler.scheduler.running,
        "total_jobs": len(jobs),
        "registered_tasks": len(registered_tasks),
        "jobs": [
            {
                "id": job.id,
                "name": job.name,
                "trigger": str(job.trigger),
                "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None
            }
            for job in jobs
        ]
    }


@router.post("/scheduler/shutdown")
async def shutdown_scheduler(wait: bool = True) -> Dict[str, str]:
    """
    关闭调度器

    Args:
        wait: 是否等待任务完成

    Returns:
        dict: 操作结果

    Warning:
        此操作会关闭所有定时任务
    """
    scheduler.shutdown(wait=wait)
    return {"message": "调度器已关闭"}


@router.post("/scheduler/start")
async def start_scheduler() -> Dict[str, str]:
    """
    启动调度器

    Returns:
        dict: 操作结果
    """
    scheduler.start()
    return {"message": "调度器已启动"}
