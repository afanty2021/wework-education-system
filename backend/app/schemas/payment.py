"""Payment Pydantic Schemas

缴费相关 Pydantic 模型
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class PaymentBase(BaseModel):
    """缴费基础模型"""
    contract_id: int = Field(..., description="合同ID")
    amount: Decimal = Field(..., gt=0, description="缴费金额")
    hours: Optional[Decimal] = Field(None, gt=0, description="购买课时数")
    payment_method: int = Field(..., ge=1, le=5, description="缴费方式: 1:微信 2:支付宝 3:现金 4:银行卡 5:转账")
    payment_channel: Optional[str] = Field(None, max_length=20, description="支付渠道")
    transaction_id: Optional[str] = Field(None, max_length=100, description="第三方交易号")
    trade_no: Optional[str] = Field(None, max_length=100, description="支付宝交易号")
    payment_time: Optional[datetime] = Field(None, description="缴费时间")
    operator_id: Optional[int] = Field(None, description="操作人ID")
    remark: Optional[str] = Field(None, max_length=500, description="备注")


class PaymentCreate(PaymentBase):
    """缴费创建模型"""
    payment_no: str = Field(..., min_length=1, max_length=50, description="缴费单号")


class PaymentUpdate(BaseModel):
    """缴费更新模型"""
    amount: Optional[Decimal] = Field(None, gt=0, description="缴费金额")
    hours: Optional[Decimal] = Field(None, ge=0, description="购买课时数")
    payment_method: Optional[int] = Field(None, ge=1, le=5, description="缴费方式: 1:微信 2:支付宝 3:现金 4:银行卡 5:转账")
    payment_channel: Optional[str] = Field(None, max_length=20, description="支付渠道")
    transaction_id: Optional[str] = Field(None, max_length=100, description="第三方交易号")
    trade_no: Optional[str] = Field(None, max_length=100, description="支付宝交易号")
    payment_time: Optional[datetime] = Field(None, description="缴费时间")
    operator_id: Optional[int] = Field(None, description="操作人ID")
    status: Optional[int] = Field(None, ge=1, le=3, description="状态: 1:待确认 2:已确认 3:已退款")
    remark: Optional[str] = Field(None, max_length=500, description="备注")


class PaymentConfirm(BaseModel):
    """缴费确认模型"""
    hours: Decimal = Field(..., gt=0, description="确认课时数")
    remark: Optional[str] = Field(None, max_length=500, description="确认备注")


class PaymentRefund(BaseModel):
    """缴费退款模型"""
    refund_amount: Decimal = Field(..., gt=0, description="退款金额")
    refund_hours: Optional[Decimal] = Field(None, ge=0, description="退款课时数")
    refund_reason: Optional[str] = Field(None, max_length=500, description="退款原因")
    remark: Optional[str] = Field(None, max_length=500, description="备注")


class PaymentResponse(PaymentBase):
    """缴费响应模型"""
    id: int
    payment_no: str
    status: int = Field(..., description="状态: 1:待确认 2:已确认 3:已退款")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
