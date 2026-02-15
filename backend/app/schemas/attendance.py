"""Attendance Pydantic Schemas

考勤相关 Pydantic 模型
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class AttendanceBase(BaseModel):
    """考勤基础模型"""
    schedule_id: int = Field(..., description="排课ID")
    student_id: int = Field(..., description="学员ID")
    contract_id: Optional[int] = Field(None, description="合同ID(扣课时用)")
    status: int = Field(..., ge=1, le=4, description="状态: 1:出勤 2:请假 3:缺勤 4:迟到")
    check_time: Optional[datetime] = Field(None, description="签到时间")
    check_method: int = Field(default=1, ge=1, le=3, description="签到方式: 1:手动 2:人脸 3:刷卡")
    hours_consumed: Decimal = Field(default=Decimal("1.0"), gt=0, description="消耗课时数")
    notes: Optional[str] = Field(None, max_length=500, description="备注")


class AttendanceCreate(AttendanceBase):
    """考勤创建模型"""
    pass


class AttendanceUpdate(BaseModel):
    """考勤更新模型"""
    schedule_id: Optional[int] = Field(None, description="排课ID")
    student_id: Optional[int] = Field(None, description="学员ID")
    contract_id: Optional[int] = Field(None, description="合同ID")
    status: Optional[int] = Field(None, ge=1, le=4, description="状态: 1:出勤 2:请假 3:缺勤 4:迟到")
    check_time: Optional[datetime] = Field(None, description="签到时间")
    check_method: Optional[int] = Field(None, ge=1, le=3, description="签到方式: 1:手动 2:人脸 3:刷卡")
    hours_consumed: Optional[Decimal] = Field(None, gt=0, description="消耗课时数")
    notes: Optional[str] = Field(None, max_length=500, description="备注")


class AttendanceResponse(AttendanceBase):
    """考勤响应模型"""
    id: int
    created_by: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AttendanceBatchCreate(BaseModel):
    """批量创建考勤模型"""
    attendances: List[AttendanceCreate] = Field(..., min_length=1, description="考勤列表")
    auto_deduct_hours: bool = Field(default=True, description="是否自动扣减课时")


class AttendanceStatistics(BaseModel):
    """考勤统计模型"""
    total_count: int = Field(..., description="总考勤次数")
    present_count: int = Field(..., description="出勤次数")
    leave_count: int = Field(..., description="请假次数")
    absent_count: int = Field(..., description="缺勤次数")
    late_count: int = Field(..., description="迟到次数")
    present_rate: float = Field(..., description="出勤率(%)")
    total_hours_consumed: Decimal = Field(..., description="总消耗课时数")
