"""
考勤模型

表: attendances
"""

from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
from decimal import Decimal


class Attendance(SQLModel, table=True):
    """考勤模型"""
    __tablename__ = "attendances"

    id: Optional[int] = Field(default=None, primary_key=True)
    schedule_id: int = Field(foreign_key="schedules.id", index=True, description="排课ID")
    student_id: int = Field(foreign_key="students.id", index=True, description="学员ID")
    contract_id: Optional[int] = Field(default=None, foreign_key="contracts.id", description="合同ID(扣课时用)")
    status: int = Field(description="状态: 1:出勤 2:请假 3:缺勤 4:迟到")
    check_time: Optional[datetime] = Field(default=None, description="签到时间")
    check_method: int = Field(default=1, description="签到方式: 1:手动 2:人脸 3:刷卡")
    hours_consumed: Decimal = Field(default=1, description="消耗课时数")
    notes: Optional[str] = Field(default=None, description="备注")
    created_by: Optional[int] = Field(default=None, foreign_key="users.id", description="记录人")

    created_at: datetime = Field(default_factory=datetime.now)
