"""Homeworks API Routes

作业管理相关 API 路由
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.homework import HomeworkCreate, HomeworkResponse, HomeworkUpdate

router = APIRouter()


@router.get("", response_model=List[HomeworkResponse], tags=["Homeworks"])
async def list_homeworks(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[HomeworkResponse]:
    """获取作业列表"""
    # TODO: 实现作业列表查询
    pass


@router.get("/{homework_id}", response_model=HomeworkResponse, tags=["Homeworks"])
async def get_homework(
    homework_id: int,
    db: AsyncSession = Depends(get_db),
) -> HomeworkResponse:
    """获取作业详情"""
    # TODO: 实现作业详情查询
    pass


@router.post("", response_model=HomeworkResponse, status_code=status.HTTP_201_CREATED, tags=["Homeworks"])
async def create_homework(
    homework_data: HomeworkCreate,
    db: AsyncSession = Depends(get_db),
) -> HomeworkResponse:
    """创建作业"""
    # TODO: 实现作业创建
    pass


@router.put("/{homework_id}", response_model=HomeworkResponse, tags=["Homeworks"])
async def update_homework(
    homework_id: int,
    homework_data: HomeworkUpdate,
    db: AsyncSession = Depends(get_db),
) -> HomeworkResponse:
    """更新作业"""
    # TODO: 实现作业更新
    pass


@router.delete("/{homework_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Homeworks"])
async def delete_homework(
    homework_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除作业"""
    # TODO: 实现作业删除
    pass


@router.post("/{homework_id}/submit", response_model=HomeworkResponse, tags=["Homeworks"])
async def submit_homework(
    homework_id: int,
    submission_data: dict,
    db: AsyncSession = Depends(get_db),
) -> HomeworkResponse:
    """提交作业"""
    # TODO: 实现作业提交
    pass
