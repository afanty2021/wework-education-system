"""SQLModel Payment Model

支付数据模型
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Integer, String, Float, ForeignKey, Text, SQLModel


class Payment(SQLModel, table=True):
    """支付模型"""
    id: Optional[int] = Column(Integer, primary_key=True, index=True)
    order_no: str = Column(String(50), unique=True, nullable=False, index=True)
    student_id: int = Column(Integer, ForeignKey("student.id"), nullable=False, index=True)
    contract_id: int = Column(Integer, ForeignKey("contract.id"), nullable=False, index=True)
    amount: float = Column(Float, nullable=False)
    payment_method: str = Column(String(20), nullable=False)  # alipay, wechat, cash, bank_transfer
    status: str = Column(String(20), default="pending")  # pending, paid, failed, refunded
    trade_no: Optional[str] = Column(String(100), nullable=True)  # 第三方交易号
    remark: Optional[str] = Column(Text, nullable=True)
    paid_at: Optional[datetime] = Column(DateTime, nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: Optional[datetime] = Column(DateTime, default=None, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Payment(id={self.id}, order_no={self.order_no})>"
