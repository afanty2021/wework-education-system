"""Attendance API Routes

考勤管理相关 API 路由
"""
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceResponse,
    AttendanceUpdate,
    AttendanceBatchCreate,
    AttendanceStatistics,
)
from app.services.attendance_service import (
    AttendanceService,
    AttendanceNotFoundError,
    ScheduleNotFoundError,
    StudentNotFoundError,
    DuplicateAttendanceError,
    InvalidAttendanceDataError,
    InvalidAttendanceStatusError,
    AttendanceServiceError,
    ContractNotFoundError,
    InsufficientHoursError,
)


router = APIRouter()


# ==================== 基础 CRUD API ====================

@router.get("", response_model=List[AttendanceResponse], tags=["Attendance"])
async def list_attendances(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=100, description="返回记录数"),
    schedule_id: Optional[int] = Query(None, description="排课ID筛选"),
    student_id: Optional[int] = Query(None, description="学员ID筛选"),
    contract_id: Optional[int] = Query(None, description="合同ID筛选"),
    status: Optional[int] = Query(None, ge=1, le=4, description="状态筛选 (1:出勤 2:请假 3:缺勤 4:迟到)"),
) -> List[AttendanceResponse]:
    """获取考勤列表

    支持分页、排课筛选、学员筛选、合同筛选和状态筛选
    """
    try:
        attendances = await AttendanceService.get_all_attendances(
            session=db,
            skip=skip,
            limit=limit,
            schedule_id=schedule_id,
            student_id=student_id,
            contract_id=contract_id,
            status=status
        )
        return attendances
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取考勤列表失败: {str(e)}"
        )


@router.get("/count", tags=["Attendance"])
async def count_attendances(
    db: AsyncSession = Depends(get_db),
    schedule_id: Optional[int] = Query(None, description="排课ID筛选"),
    student_id: Optional[int] = Query(None, description="学员ID筛选"),
    contract_id: Optional[int] = Query(None, description="合同ID筛选"),
    status: Optional[int] = Query(None, ge=1, le=4, description="状态筛选"),
):
    """统计考勤数量"""
    try:
        count = await AttendanceService.count_attendances(
            session=db,
            schedule_id=schedule_id,
            student_id=student_id,
            contract_id=contract_id,
            status=status
        )
        return {"count": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"统计考勤数量失败: {str(e)}"
        )


@router.get("/{attendance_id}", response_model=AttendanceResponse, tags=["Attendance"])
async def get_attendance(
    attendance_id: int,
    db: AsyncSession = Depends(get_db),
) -> AttendanceResponse:
    """获取考勤详情"""
    try:
        attendance = await AttendanceService.get_attendance_by_id(attendance_id, db)
        return attendance
    except AttendanceNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"考勤不存在: {attendance_id}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取考勤详情失败: {str(e)}"
        )


@router.post("", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED, tags=["Attendance"])
async def create_attendance(
    attendance_data: AttendanceCreate,
    db: AsyncSession = Depends(get_db),
) -> AttendanceResponse:
    """创建考勤记录

    自动验证排课和学员存在性，自动扣减课时（出勤和迟到）
    """
    try:
        attendance = await AttendanceService.create_attendance(
            attendance_data=attendance_data,
            created_by=None,  # TODO: 从认证上下文获取当前用户
            session=db,
            auto_deduct=True
        )
        return attendance
    except ScheduleNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except StudentNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ContractNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DuplicateAttendanceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except InvalidAttendanceStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except InsufficientHoursError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建考勤失败: {str(e)}"
        )


@router.put("/{attendance_id}", response_model=AttendanceResponse, tags=["Attendance"])
async def update_attendance(
    attendance_id: int,
    attendance_data: AttendanceUpdate,
    db: AsyncSession = Depends(get_db),
) -> AttendanceResponse:
    """更新考勤记录"""
    try:
        attendance = await AttendanceService.update_attendance(
            attendance_id=attendance_id,
            attendance_data=attendance_data,
            session=db
        )
        return attendance
    except AttendanceNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"考勤不存在: {attendance_id}"
        )
    except ScheduleNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except StudentNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ContractNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DuplicateAttendanceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except InvalidAttendanceStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新考勤失败: {str(e)}"
        )


@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Attendance"])
async def delete_attendance(
    attendance_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除考勤记录"""
    try:
        await AttendanceService.delete_attendance(attendance_id, db)
    except AttendanceNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"考勤不存在: {attendance_id}"
        )
    except AttendanceServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除考勤失败: {str(e)}"
        )


# ==================== 批量操作 API ====================

@router.post("/batch", response_model=List[AttendanceResponse], tags=["Attendance"])
async def batch_create_attendances(
    batch_data: AttendanceBatchCreate,
    db: AsyncSession = Depends(get_db),
) -> List[AttendanceResponse]:
    """批量创建考勤记录

    支持批量创建，可选择是否自动扣减课时
    """
    try:
        attendances = await AttendanceService.batch_create_attendances(
            batch_data=batch_data,
            created_by=None,  # TODO: 从认证上下文获取当前用户
            session=db
        )
        return attendances
    except ScheduleNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except StudentNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ContractNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DuplicateAttendanceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except InsufficientHoursError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量创建考勤失败: {str(e)}"
        )


# ==================== 统计 API ====================

@router.get("/statistics/student/{student_id}", response_model=AttendanceStatistics, tags=["Attendance"])
async def get_student_attendance_statistics(
    student_id: int,
    db: AsyncSession = Depends(get_db),
) -> AttendanceStatistics:
    """获取学员考勤统计

    包括总次数、各状态次数、出勤率、总消耗课时
    """
    try:
        stats = await AttendanceService.get_student_statistics(student_id, db)
        return stats
    except StudentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"学员不存在: {student_id}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取学员考勤统计失败: {str(e)}"
        )


@router.get("/statistics/schedule/{schedule_id}", response_model=AttendanceStatistics, tags=["Attendance"])
async def get_schedule_attendance_statistics(
    schedule_id: int,
    db: AsyncSession = Depends(get_db),
) -> AttendanceStatistics:
    """获取排课考勤统计

    包括总次数、各状态次数、出勤率、总消耗课时
    """
    try:
        stats = await AttendanceService.get_schedule_statistics(schedule_id, db)
        return stats
    except ScheduleNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"排课不存在: {schedule_id}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取排课考勤统计失败: {str(e)}"
        )


@router.get("/statistics/course/{course_id}", response_model=AttendanceStatistics, tags=["Attendance"])
async def get_course_attendance_statistics(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    start_date: Optional[datetime] = Query(None, description="开始日期"),
    end_date: Optional[datetime] = Query(None, description="结束日期"),
) -> AttendanceStatistics:
    """获取课程考勤统计

    包括总次数、各状态次数、出勤率、总消耗课时
    支持时间范围筛选
    """
    try:
        stats = await AttendanceService.get_course_statistics(
            course_id=course_id,
            session=db,
            start_date=start_date,
            end_date=end_date
        )
        return stats
    except ScheduleNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"课程不存在: {course_id}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取课程考勤统计失败: {str(e)}"
        )
