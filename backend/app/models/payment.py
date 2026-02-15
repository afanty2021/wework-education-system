"""
缴费模型

表: payments, refunds
"""

from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
from decimal import Decimal


class Payment(SQLModel, table=True):
    """缴费记录模型"""
    __tablename__ = "payments"

    id: Optional[int] = Field(default=None, primary_key=True)
    payment_no: str = Field(max_length=50, unique=True, index=True, description="缴费单号")
    contract_id: int = Field(foreign_key="contracts.id", index=True, description="合同ID")
    amount: Decimal = Field(description="缴费金额")
    hours: Optional[Decimal] = Field(default=None, description="购买课时数")
    payment_method: int = Field(description="缴费方式: 1:微信 2:支付宝 3:现金 4:银行卡 5:转账")
    payment_channel: Optional[str] = Field(default=None, max_length=20, description="支付渠道")
    transaction_id: Optional[str] = Field(default=None, max_length=100, description="第三方交易号")
    trade_no: Optional[str] = Field(default=None, max_length=100, description="支付宝交易号")
    payment_time: Optional[datetime] = Field(default=None, description="缴费时间")
    operator_id: Optional[int] = Field(default=None, foreign_key="users.id", description="操作人")
    status: int = Field(default=1, description="状态: 1:待确认 2:已确认 3:已退款")
    remark: Optional[str] = Field(default=None, max_length=500, description="备注")

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Refund(SQLModel, table=True):
    """退费记录模型"""
    __tablename__ = "refunds"

    id: Optional[int] = Field(default=None, primary_key=True)
    refund_no: str = Field(max_length=50, unique=True, index=True, description="退费单号")
    contract_id: int = Field(foreign_key="contracts.id", description="合同ID")
    payment_id: Optional[int] = Field(default=None, foreign_key="payments.id", description="原缴费ID")
    refund_amount: Decimal = Field(description="退费金额")
    refund_hours: Optional[Decimal] = Field(default=None, description="退费课时数")
    refund_reason: Optional[str] = Field(default=None, max_length=500, description="退费原因")
    approver_id: Optional[int] = Field(default=None, foreign_key="users.id", description="审批人")
    status: int = Field(default=1, description="状态: 1:待审批 2:已批准 3:已拒绝 4:已退款")
    remark: Optional[str] = Field(default=None, max_length=500, description="备注")
    created_by: Optional[int] = Field(default=None, foreign_key="users.id", description="申请人")

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
