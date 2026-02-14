"""Schedules API Routes

排课管理相关 API 路由
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.schedule import ScheduleCreate, ScheduleResponse, ScheduleUpdate

router = APIRouter()


@router.get("", response_model=List[ScheduleResponse], tags=["Schedules"])
async def list_schedules(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[ScheduleResponse]:
    """获取排课列表"""
    # TODO: 实现排课列表查询
    pass


@router.get("/{schedule_id}", response_model=ScheduleResponse, tags=["Schedules"])
async def get_schedule(
    schedule_id: int,
    db: AsyncSession = Depends(get_db),
) -> ScheduleResponse:
    """获取排课详情"""
    # TODO: 实现排课详情查询
    pass


@router.post("", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED, tags=["Schedules"])
async def create_schedule(
    schedule_data: ScheduleCreate,
    db: AsyncSession = Depends(get_db),
) -> ScheduleResponse:
    """创建排课"""
    # TODO: 实现排课创建
    pass


@router.put("/{schedule_id}", response_model=ScheduleResponse, tags=["Schedules"])
async def update_schedule(
    schedule_id: int,
    schedule_data: ScheduleUpdate,
    db: AsyncSession = Depends(get_db),
) -> ScheduleResponse:
    """更新排课"""
    # TODO: 实现排课更新
    pass


@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Schedules"])
async def delete_schedule(
    schedule_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除排课"""
    # TODO: 实现排课删除
    pass
