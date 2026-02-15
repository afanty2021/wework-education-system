"""Courses API Routes

课程管理相关 API 路由
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.course import (
    CourseCreate,
    CourseResponse,
    CourseUpdate,
    ClassroomCreate,
    ClassroomResponse,
    ClassroomUpdate,
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate,
)
from app.services.course_service import (
    CourseService,
    CourseNotFoundError,
    CourseHasSchedulesError,
    CourseServiceError,
    InvalidCourseDataError,
    ClassroomNotFoundError,
    DepartmentNotFoundError,
)


router = APIRouter()


@router.get("", response_model=List[CourseResponse], tags=["Courses"])
async def list_courses(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=100, description="返回记录数"),
    category: Optional[str] = Query(None, description="课程分类筛选"),
    status: Optional[int] = Query(None, ge=1, le=2, description="状态筛选 (1:上架 2:下架)"),
    search: Optional[str] = Query(None, description="搜索关键词"),
) -> List[CourseResponse]:
    """获取课程列表

    支持分页、分类筛选、状态筛选和关键词搜索
    """
    try:
        courses = await CourseService.get_all_courses(
            session=db,
            skip=skip,
            limit=limit,
            category=category,
            status=status,
            search=search
        )
        return courses
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取课程列表失败: {str(e)}"
        )


@router.get("/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
) -> CourseResponse:
    """获取课程详情"""
    try:
        course = await CourseService.get_course_by_id(course_id, db)
        return course
    except CourseNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"课程不存在: {course_id}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取课程详情失败: {str(e)}"
        )


@router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED, tags=["Courses"])
async def create_course(
    course_data: CourseCreate,
    db: AsyncSession = Depends(get_db),
) -> CourseResponse:
    """创建课程"""
    try:
        course = await CourseService.create_course(course_data, db)
        return course
    except InvalidCourseDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建课程失败: {str(e)}"
        )


@router.put("/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def update_course(
    course_id: int,
    course_data: CourseUpdate,
    db: AsyncSession = Depends(get_db),
) -> CourseResponse:
    """更新课程"""
    try:
        course = await CourseService.update_course(course_id, course_data, db)
        return course
    except CourseNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"课程不存在: {course_id}"
        )
    except InvalidCourseDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新课程失败: {str(e)}"
        )


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Courses"])
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除课程

    删除前会检查是否有关联的排课记录
    """
    try:
        await CourseService.delete_course(course_id, db)
    except CourseNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"课程不存在: {course_id}"
        )
    except CourseHasSchedulesError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除课程失败: {str(e)}"
        )


@router.patch("/{course_id}/toggle-status", response_model=CourseResponse, tags=["Courses"])
async def toggle_course_status(
    course_id: int,
    db: AsyncSession = Depends(get_db),
) -> CourseResponse:
    """切换课程上架/下架状态"""
    try:
        course = await CourseService.toggle_course_status(course_id, db)
        return course
    except CourseNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"课程不存在: {course_id}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"切换课程状态失败: {str(e)}"
        )


# ==================== 教室管理 API ====================

@router.get("/classrooms", response_model=List[ClassroomResponse], tags=["Classrooms"])
async def list_classrooms(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=100, description="返回记录数"),
    department_id: Optional[int] = Query(None, description="校区ID筛选"),
    status: Optional[int] = Query(None, ge=1, le=2, description="状态筛选 (1:可用 2:维护中)"),
) -> List[ClassroomResponse]:
    """获取教室列表

    支持分页、校区筛选和状态筛选
    """
    try:
        classrooms = await CourseService.get_all_classrooms(
            session=db,
            skip=skip,
            limit=limit,
            department_id=department_id,
            status=status
        )
        return classrooms
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取教室列表失败: {str(e)}"
        )


@router.get("/classrooms/{classroom_id}", response_model=ClassroomResponse, tags=["Classrooms"])
async def get_classroom(
    classroom_id: int,
    db: AsyncSession = Depends(get_db),
) -> ClassroomResponse:
    """获取教室详情"""
    try:
        classroom = await CourseService.get_classroom_by_id(classroom_id, db)
        return classroom
    except ClassroomNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"教室不存在: {classroom_id}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取教室详情失败: {str(e)}"
        )


@router.post("/classrooms", response_model=ClassroomResponse, status_code=status.HTTP_201_CREATED, tags=["Classrooms"])
async def create_classroom(
    classroom_data: ClassroomCreate,
    db: AsyncSession = Depends(get_db),
) -> ClassroomResponse:
    """创建教室"""
    try:
        classroom = await CourseService.create_classroom(
            name=classroom_data.name,
            capacity=classroom_data.capacity,
            department_id=classroom_data.department_id,
            equipment=classroom_data.equipment,
            session=db
        )
        return classroom
    except DepartmentNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except InvalidCourseDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建教室失败: {str(e)}"
        )


@router.put("/classrooms/{classroom_id}", response_model=ClassroomResponse, tags=["Classrooms"])
async def update_classroom(
    classroom_id: int,
    classroom_data: ClassroomUpdate,
    db: AsyncSession = Depends(get_db),
) -> ClassroomResponse:
    """更新教室信息"""
    try:
        classroom = await CourseService.update_classroom(
            classroom_id=classroom_id,
            name=classroom_data.name,
            capacity=classroom_data.capacity,
            department_id=classroom_data.department_id,
            equipment=classroom_data.equipment,
            session=db
        )
        return classroom
    except ClassroomNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"教室不存在: {classroom_id}"
        )
    except DepartmentNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except InvalidCourseDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新教室失败: {str(e)}"
        )


@router.delete("/classrooms/{classroom_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Classrooms"])
async def delete_classroom(
    classroom_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除教室

    删除前会检查是否有关联的排课记录
    """
    try:
        await CourseService.delete_classroom(classroom_id, db)
    except ClassroomNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"教室不存在: {classroom_id}"
        )
    except CourseServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除教室失败: {str(e)}"
        )


# ==================== 校区管理 API ====================

@router.get("/departments", response_model=List[DepartmentResponse], tags=["Departments"])
async def list_departments(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=100, description="返回记录数"),
    status: Optional[int] = Query(None, ge=1, le=2, description="状态筛选"),
) -> List[DepartmentResponse]:
    """获取校区列表

    支持分页和状态筛选
    """
    try:
        departments = await CourseService.get_all_departments(
            session=db,
            skip=skip,
            limit=limit,
            status=status
        )
        return departments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取校区列表失败: {str(e)}"
        )


@router.get("/departments/{department_id}", response_model=DepartmentResponse, tags=["Departments"])
async def get_department(
    department_id: int,
    db: AsyncSession = Depends(get_db),
) -> DepartmentResponse:
    """获取校区详情"""
    try:
        department = await CourseService.get_department_by_id(department_id, db)
        return department
    except DepartmentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"校区不存在: {department_id}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取校区详情失败: {str(e)}"
        )


@router.post("/departments", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED, tags=["Departments"])
async def create_department(
    department_data: DepartmentCreate,
    db: AsyncSession = Depends(get_db),
) -> DepartmentResponse:
    """创建校区"""
    try:
        department = await CourseService.create_department(
            name=department_data.name,
            parent_id=department_data.parent_id,
            manager_id=department_data.manager_id,
            address=department_data.address,
            contact=department_data.contact,
            session=db
        )
        return department
    except InvalidCourseDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建校区失败: {str(e)}"
        )


@router.put("/departments/{department_id}", response_model=DepartmentResponse, tags=["Departments"])
async def update_department(
    department_id: int,
    department_data: DepartmentUpdate,
    db: AsyncSession = Depends(get_db),
) -> DepartmentResponse:
    """更新校区信息"""
    try:
        department = await CourseService.update_department(
            department_id=department_id,
            name=department_data.name,
            parent_id=department_data.parent_id,
            manager_id=department_data.manager_id,
            address=department_data.address,
            contact=department_data.contact,
            session=db
        )
        return department
    except DepartmentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"校区不存在: {department_id}"
        )
    except InvalidCourseDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新校区失败: {str(e)}"
        )


@router.delete("/departments/{department_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Departments"])
async def delete_department(
    department_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除校区

    删除前会检查是否有关联的教室或下级校区
    """
    try:
        await CourseService.delete_department(department_id, db)
    except DepartmentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"校区不存在: {department_id}"
        )
    except CourseServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除校区失败: {str(e)}"
        )
