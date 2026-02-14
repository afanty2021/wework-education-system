"""Payment Pydantic Schemas

支付相关 Pydantic 模型
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PaymentBase(BaseModel):
    """支付基础模型"""
    student_id: int
    contract_id: int
    amount: float
    payment_method: str  # alipay, wechat, cash, bank_transfer
    remark: Optional[str] = None


class PaymentCreate(PaymentBase):
    """支付创建模型"""
    pass


class PaymentUpdate(BaseModel):
    """支付更新模型"""
    status: Optional[str] = None
    remark: Optional[str] = None


class PaymentResponse(PaymentBase):
    """支付响应模型"""
    id: int
    order_no: str
    status: str
    paid_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
