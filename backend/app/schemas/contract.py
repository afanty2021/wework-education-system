"""Contract Pydantic Schemas

合同相关 Pydantic 模型
"""
from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel


class ContractBase(BaseModel):
    """合同基础模型"""
    student_id: int
    course_id: int
    total_amount: float
    discount_amount: float = 0.0
    actual_amount: float
    total_hours: int
    start_date: date
    end_date: date
    remark: Optional[str] = None


class ContractCreate(ContractBase):
    """合同创建模型"""
    pass


class ContractUpdate(BaseModel):
    """合同更新模型"""
    total_amount: Optional[float] = None
    discount_amount: Optional[float] = None
    actual_amount: Optional[float] = None
    total_hours: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    remark: Optional[str] = None
    status: Optional[str] = None


class ContractResponse(ContractBase):
    """合同响应模型"""
    id: int
    status: str
    used_hours: float = 0.0
    remaining_hours: float = 0.0
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
