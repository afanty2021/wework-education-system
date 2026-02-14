"""Courses API Routes

课程管理相关 API 路由
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.user import User
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate

router = APIRouter()


@router.get("", response_model=List[CourseResponse], tags=["Courses"])
async def list_courses(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[CourseResponse]:
    """获取课程列表"""
    # TODO: 实现课程列表查询
    pass


@router.get("/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
) -> CourseResponse:
    """获取课程详情"""
    # TODO: 实现课程详情查询
    pass


@router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED, tags=["Courses"])
async def create_course(
    course_data: CourseCreate,
    db: AsyncSession = Depends(get_db),
) -> CourseResponse:
    """创建课程"""
    # TODO: 实现课程创建
    pass


@router.put("/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def update_course(
    course_id: int,
    course_data: CourseUpdate,
    db: AsyncSession = Depends(get_db),
) -> CourseResponse:
    """更新课程"""
    # TODO: 实现课程更新
    pass


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Courses"])
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除课程"""
    # TODO: 实现课程删除
    pass
