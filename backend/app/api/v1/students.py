"""Students API Routes

学员管理相关 API 路由
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate

router = APIRouter()


@router.get("", response_model=List[StudentResponse], tags=["Students"])
async def list_students(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[StudentResponse]:
    """获取学员列表"""
    # TODO: 实现学员列表查询
    pass


@router.get("/{student_id}", response_model=StudentResponse, tags=["Students"])
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
) -> StudentResponse:
    """获取学员详情"""
    # TODO: 实现学员详情查询
    pass


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED, tags=["Students"])
async def create_student(
    student_data: StudentCreate,
    db: AsyncSession = Depends(get_db),
) -> StudentResponse:
    """创建学员"""
    # TODO: 实现学员创建
    pass


@router.put("/{student_id}", response_model=StudentResponse, tags=["Students"])
async def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: AsyncSession = Depends(get_db),
) -> StudentResponse:
    """更新学员"""
    # TODO: 实现学员更新
    pass


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Students"])
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除学员"""
    # TODO: 实现学员删除
    pass
