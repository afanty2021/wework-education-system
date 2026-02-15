"""排课 API Routes

排课管理相关 API 路由
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.schedule import (
    ScheduleCreate,
    ScheduleResponse,
    ScheduleUpdate,
    ScheduleEnroll,
    ScheduleConflictCheck,
    ScheduleConflictResponse,
)
from app.services.schedule_service import (
    ScheduleService,
    ScheduleNotFoundError,
    CourseNotFoundError,
    TeacherNotFoundError,
    ClassroomNotFoundError,
    StudentNotFoundError,
    ScheduleConflictError,
    InvalidScheduleDataError,
    ScheduleCapacityError,
    InvalidScheduleStatusError,
    ScheduleServiceError,
)


router = APIRouter()


# ==================== 基础 CRUD API ====================

@router.get("", response_model=List[ScheduleResponse], tags=["排课管理"])
async def list_schedules(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=100, description="返回记录数"),
    course_id: Optional[int] = Query(None, description="课程ID筛选"),
    teacher_id: Optional[int] = Query(None, description="教师ID筛选"),
    classroom_id: Optional[int] = Query(None, description="教室ID筛选"),
    department_id: Optional[int] = Query(None, description="校区ID筛选"),
    status: Optional[int] = Query(None, ge=1, le=4, description="状态筛选 (1:已安排 2:已上课 3:已取消 4:已调课)"),
) -> List[ScheduleResponse]:
    """获取排课列表

    支持分页、课程筛选、教师筛选、教室筛选、校区筛选和状态筛选
    """
    try:
        schedules = await ScheduleService.get_all_schedules(
            session=db,
            skip=skip,
            limit=limit,
            course_id=course_id,
            teacher_id=teacher_id,
            classroom_id=classroom_id,
            department_id=department_id,
            status=status
        )
        return schedules
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取排课列表失败: {str(e)}"
        )


@router.get("/stats/count", tags=["排课管理"])
async def count_schedules(
    db: AsyncSession = Depends(get_db),
    course_id: Optional[int] = Query(None, description="课程ID筛选"),
    teacher_id: Optional[int] = Query(None, description="教师ID筛选"),
    classroom_id: Optional[int] = Query(None, description="教室ID筛选"),
    department_id: Optional[int] = Query(None, description="校区ID筛选"),
    status: Optional[int] = Query(None, ge=1, le=4, description="状态筛选"),
):
    """统计排课数量"""
    try:
        count = await ScheduleService.count_schedules(
            session=db,
            course_id=course_id,
            teacher_id=teacher_id,
            classroom_id=classroom_id,
            department_id=department_id,
            status=status
        )
        return {"count": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"统计排课数量失败: {str(e)}"
        )


@router.get("/{schedule_id}", response_model=ScheduleResponse, tags=["排课管理"])
async def get_schedule(
    schedule_id: int,
    db: AsyncSession = Depends(get_db),
) -> ScheduleResponse:
    """获取排课详情"""
    try:
        schedule = await ScheduleService.get_schedule_by_id(schedule_id, db)
        return schedule
    except ScheduleNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"排课不存在: {schedule_id}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取排课详情失败: {str(e)}"
        )


@router.post("", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED, tags=["排课管理"])
async def create_schedule(
    schedule_data: ScheduleCreate,
    db: AsyncSession = Depends(get_db),
) -> ScheduleResponse:
    """创建排课

    自动检测时间冲突（教师、教室、课程）
    """
    try:
        schedule = await ScheduleService.create_schedule(
            schedule_data=schedule_data,
            created_by=None,  # TODO: 从认证上下文获取当前用户
            session=db
        )
        return schedule
    except CourseNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except TeacherNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ClassroomNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except InvalidScheduleDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ScheduleConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建排课失败: {str(e)}"
        )


@router.put("/{schedule_id}", response_model=ScheduleResponse, tags=["排课管理"])
async def update_schedule(
    schedule_id: int,
    schedule_data: ScheduleUpdate,
    db: AsyncSession = Depends(get_db),
) -> ScheduleResponse:
    """更新排课

    更新时会自动检测时间冲突（排除当前排课）
    """
    try:
        schedule = await ScheduleService.update_schedule(
            schedule_id=schedule_id,
            schedule_data=schedule_data,
            session=db
        )
        return schedule
    except ScheduleNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"排课不存在: {schedule_id}"
        )
    except (CourseNotFoundError, TeacherNotFoundError, ClassroomNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except InvalidScheduleDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ScheduleConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新排课失败: {str(e)}"
        )


@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["排课管理"])
async def delete_schedule(
    schedule_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除排课"""
    try:
        await ScheduleService.delete_schedule(schedule_id, db)
    except ScheduleNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"排课不存在: {schedule_id}"
        )
    except ScheduleServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除排课失败: {str(e)}"
        )


# ==================== 报名管理 API ====================

@router.post("/{schedule_id}/enroll", response_model=ScheduleResponse, tags=["排课管理"])
async def enroll_student(
    schedule_id: int,
    enroll_data: ScheduleEnroll,
    db: AsyncSession = Depends(get_db),
) -> ScheduleResponse:
    """学员报名

    会检查排课容量和状态
    """
    try:
        schedule = await ScheduleService.enroll_student(
            schedule_id=schedule_id,
            enroll_data=enroll_data,
            session=db
        )
        return schedule
    except ScheduleNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"排课不存在: {schedule_id}"
        )
    except StudentNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ScheduleCapacityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except InvalidScheduleStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"学员报名失败: {str(e)}"
        )


@router.post("/{schedule_id}/cancel-enrollment", response_model=ScheduleResponse, tags=["排课管理"])
async def cancel_enrollment(
    schedule_id: int,
    student_id: int = Query(..., description="学员ID"),
    count: int = Query(1, ge=1, description="取消人数"),
    db: AsyncSession = Depends(get_db),
) -> ScheduleResponse:
    """取消报名"""
    try:
        schedule = await ScheduleService.cancel_enrollment(
            schedule_id=schedule_id,
            student_id=student_id,
            count=count,
            session=db
        )
        return schedule
    except ScheduleNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"排课不存在: {schedule_id}"
        )
    except (InvalidScheduleDataError, InvalidScheduleStatusError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"取消报名失败: {str(e)}"
        )


@router.post("/{schedule_id}/cancel", response_model=ScheduleResponse, tags=["排课管理"])
async def cancel_schedule(
    schedule_id: int,
    db: AsyncSession = Depends(get_db),
) -> ScheduleResponse:
    """取消排课

    将排课状态更新为已取消（3）
    """
    try:
        schedule = await ScheduleService.cancel_schedule(schedule_id, db)
        return schedule
    except ScheduleNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"排课不存在: {schedule_id}"
        )
    except InvalidScheduleStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"取消排课失败: {str(e)}"
        )


# ==================== 冲突检测 API ====================

@router.post("/conflicts/check", response_model=ScheduleConflictResponse, tags=["排课管理"])
async def check_schedule_conflicts(
    conflict_check: ScheduleConflictCheck,
    db: AsyncSession = Depends(get_db),
) -> ScheduleConflictResponse:
    """检测排课冲突

    检测教师、教室、课程在指定时间是否存在冲突
    """
    try:
        conflicts = await ScheduleService.check_conflicts(
            conflict_check=conflict_check,
            session=db
        )
        return conflicts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"检测排课冲突失败: {str(e)}"
        )


# ==================== 循环排课 API ====================

@router.post("/recurring", response_model=List[ScheduleResponse], status_code=status.HTTP_201_CREATED, tags=["排课管理"])
async def create_recurring_schedules(
    base_schedule: ScheduleCreate,
    recurring_type: str = Query(..., description="循环类型 (weekly/biweekly)"),
    recurring_count: int = Query(..., ge=2, le=52, description="循环次数"),
    interval_days: int = Query(7, ge=1, le=14, description="间隔天数"),
    db: AsyncSession = Depends(get_db),
) -> List[ScheduleResponse]:
    """创建循环排课

    根据基础排课数据和循环规则创建多个排课
    """
    try:
        schedules = await ScheduleService.create_recurring_schedules(
            base_schedule=base_schedule,
            recurring_type=recurring_type,
            recurring_count=recurring_count,
            interval_days=interval_days,
            created_by=None,  # TODO: 从认证上下文获取当前用户
            session=db
        )
        return schedules
    except (CourseNotFoundError, TeacherNotFoundError, ClassroomNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except (InvalidScheduleDataError, ScheduleConflictError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST if isinstance(e, InvalidScheduleDataError) else status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建循环排课失败: {str(e)}"
        )
