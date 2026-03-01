"""Contract Pydantic Schemas

合同相关 Pydantic 模型
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ContractBase(BaseModel):
    """合同基础模型"""
    student_id: int = Field(..., description="学员ID")
    course_id: Optional[int] = Field(None, description="报读课程")
    package_type: str = Field(..., min_length=1, max_length=20, description="课时包类型: 48/72/96/自定义")
    total_hours: Decimal = Field(..., gt=0, description="总课时数")
    remaining_hours: Decimal = Field(..., ge=0, description="剩余课时")
    unit_price: Decimal = Field(..., ge=0, description="单价(元/课时)")
    total_amount: Decimal = Field(..., ge=0, description="合同总金额")
    received_amount: Decimal = Field(default=Decimal("0.00"), ge=0, description="实收金额")
    discount_amount: Decimal = Field(default=Decimal("0.00"), ge=0, description="优惠金额")
    start_date: date = Field(..., description="合同开始日期")
    end_date: Optional[date] = Field(None, description="合同到期日期")
    expire_warning_days: int = Field(default=30, ge=0, description="到期预警天数")
    contract_file: Optional[str] = Field(None, max_length=500, description="合同文件路径")
    sales_id: Optional[int] = Field(None, description="课程顾问ID")
    notes: Optional[str] = Field(None, description="备注")


class ContractCreate(ContractBase):
    """合同创建模型"""
    contract_no: str = Field(..., min_length=1, max_length=50, description="合同编号")


class ContractUpdate(BaseModel):
    """合同更新模型"""
    course_id: Optional[int] = Field(None, description="报读课程")
    package_type: Optional[str] = Field(None, min_length=1, max_length=20, description="课时包类型")
    total_hours: Optional[Decimal] = Field(None, gt=0, description="总课时数")
    remaining_hours: Optional[Decimal] = Field(None, ge=0, description="剩余课时")
    unit_price: Optional[Decimal] = Field(None, ge=0, description="单价")
    total_amount: Optional[Decimal] = Field(None, ge=0, description="合同总金额")
    received_amount: Optional[Decimal] = Field(None, ge=0, description="实收金额")
    discount_amount: Optional[Decimal] = Field(None, ge=0, description="优惠金额")
    start_date: Optional[date] = Field(None, description="合同开始日期")
    end_date: Optional[date] = Field(None, description="合同到期日期")
    expire_warning_days: Optional[int] = Field(None, ge=0, description="到期预警天数")
    status: Optional[int] = Field(None, ge=1, le=4, description="状态: 1:生效 2:完结 3:退费 4:过期")
    contract_file: Optional[str] = Field(None, max_length=500, description="合同文件路径")
    sales_id: Optional[int] = Field(None, description="课程顾问ID")
    notes: Optional[str] = Field(None, description="备注")


class ContractResponse(ContractBase):
    """合同响应模型"""
    id: int
    contract_no: str
    status: int = Field(..., description="状态: 1:生效 2:完结 3:退费 4:过期")
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ContractDeductHours(BaseModel):
    """扣减课时模型"""
    hours: Decimal = Field(..., gt=0, description="扣减课时数")
    reason: Optional[str] = Field(None, description="扣减原因")


class ContractAddHours(BaseModel):
    """追加课时模型"""
    hours: Decimal = Field(..., gt=0, description="追加课时数")
    reason: Optional[str] = Field(None, description="追加原因")
