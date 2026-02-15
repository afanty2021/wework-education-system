"""Students API Routes

学员管理相关 API 路由
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.student import (
    StudentCreate,
    StudentResponse,
    StudentUpdate,
    StudentTagCreate,
)
from app.services.student_service import (
    StudentService,
    StudentNotFoundError,
    StudentServiceError,
    InvalidStudentDataError,
)


router = APIRouter()


@router.get("", response_model=List[StudentResponse], tags=["Students"])
async def list_students(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=100, description="返回记录数"),
    status: Optional[int] = Query(None, ge=1, le=3, description="状态筛选 (1:潜在 2:在读 3:已流失)"),
    source: Optional[str] = Query(None, description="来源筛选"),
    search: Optional[str] = Query(None, description="搜索关键词"),
) -> List[StudentResponse]:
    """获取学员列表

    支持分页、状态筛选、来源筛选和关键词搜索
    """
    try:
        students = await StudentService.get_all_students(
            session=db,
            skip=skip,
            limit=limit,
            status=status,
            source=source,
            search=search
        )
        return students
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取学员列表失败: {str(e)}"
        )


@router.get("/{student_id}", response_model=StudentResponse, tags=["Students"])
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
) -> StudentResponse:
    """获取学员详情"""
    try:
        student = await StudentService.get_student_by_id(student_id, db)
        return student
    except StudentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"学员不存在: {student_id}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取学员详情失败: {str(e)}"
        )


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED, tags=["Students"])
async def create_student(
    student_data: StudentCreate,
    db: AsyncSession = Depends(get_db),
) -> StudentResponse:
    """创建学员"""
    try:
        student = await StudentService.create_student(student_data, db)
        return student
    except InvalidStudentDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建学员失败: {str(e)}"
        )


@router.put("/{student_id}", response_model=StudentResponse, tags=["Students"])
async def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: AsyncSession = Depends(get_db),
) -> StudentResponse:
    """更新学员"""
    try:
        student = await StudentService.update_student(student_id, student_data, db)
        return student
    except StudentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"学员不存在: {student_id}"
        )
    except InvalidStudentDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新学员失败: {str(e)}"
        )


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Students"])
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除学员

    删除前会检查是否有关联的合同、考勤等数据
    """
    try:
        await StudentService.delete_student(student_id, db)
    except StudentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"学员不存在: {student_id}"
        )
    except StudentServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除学员失败: {str(e)}"
        )


@router.patch("/{student_id}/status", response_model=StudentResponse, tags=["Students"])
async def update_student_status(
    student_id: int,
    status: int = Query(..., ge=1, le=3, description="新状态 (1:潜在 2:在读 3:已流失)"),
    db: AsyncSession = Depends(get_db),
) -> StudentResponse:
    """更新学员状态"""
    try:
        student = await StudentService.update_student_status(student_id, status, db)
        return student
    except StudentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"学员不存在: {student_id}"
        )
    except InvalidStudentDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新学员状态失败: {str(e)}"
        )


# ==================== 标签管理 API ====================

@router.post("/{student_id}/tags", response_model=StudentResponse, tags=["Students"])
async def add_tag_to_student(
    student_id: int,
    tag_data: StudentTagCreate,
    db: AsyncSession = Depends(get_db),
) -> StudentResponse:
    """为学员添加标签"""
    try:
        student = await StudentService.add_tag_to_student(student_id, tag_data.tag, db)
        return student
    except StudentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"学员不存在: {student_id}"
        )
    except InvalidStudentDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"添加标签失败: {str(e)}"
        )


@router.delete("/{student_id}/tags/{tag}", response_model=StudentResponse, tags=["Students"])
async def remove_tag_from_student(
    student_id: int,
    tag: str,
    db: AsyncSession = Depends(get_db),
) -> StudentResponse:
    """从学员移除标签"""
    try:
        student = await StudentService.remove_tag_from_student(student_id, tag, db)
        return student
    except StudentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"学员不存在: {student_id}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"移除标签失败: {str(e)}"
        )


@router.get("/tags/all", response_model=List[str], tags=["Students"])
async def get_all_tags(
    db: AsyncSession = Depends(get_db),
) -> List[str]:
    """获取所有使用中的标签"""
    try:
        tags = await StudentService.get_all_tags(db)
        return tags
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取标签列表失败: {str(e)}"
        )
