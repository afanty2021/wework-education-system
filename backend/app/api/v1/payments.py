"""Payments API Routes

支付管理相关 API 路由
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.payment import PaymentCreate, PaymentResponse, PaymentUpdate

router = APIRouter()


@router.get("", response_model=List[PaymentResponse], tags=["Payments"])
async def list_payments(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[PaymentResponse]:
    """获取支付列表"""
    # TODO: 实现支付列表查询
    pass


@router.get("/{payment_id}", response_model=PaymentResponse, tags=["Payments"])
async def get_payment(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
) -> PaymentResponse:
    """获取支付详情"""
    # TODO: 实现支付详情查询
    pass


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED, tags=["Payments"])
async def create_payment(
    payment_data: PaymentCreate,
    db: AsyncSession = Depends(get_db),
) -> PaymentResponse:
    """创建支付"""
    # TODO: 实现支付创建
    pass


@router.put("/{payment_id}", response_model=PaymentResponse, tags=["Payments"])
async def update_payment(
    payment_id: int,
    payment_data: PaymentUpdate,
    db: AsyncSession = Depends(get_db),
) -> PaymentResponse:
    """更新支付"""
    # TODO: 实现支付更新
    pass


@router.post("/alipay/create", tags=["Payments"])
async def create_alipay_order():
    """创建支付宝订单"""
    # TODO: 实现支付宝订单创建
    pass


@router.post("/alipay/notify", tags=["Payments"])
async def alipay_notify():
    """支付宝异步通知"""
    # TODO: 实现支付宝通知处理
    pass


@router.post("/wechat/create", tags=["Payments"])
async def create_wechat_order():
    """创建微信支付订单"""
    # TODO: 实现微信订单创建
    pass


@router.post("/wechat/notify", tags=["Payments"])
async def wechat_notify():
    """微信支付异步通知"""
    # TODO: 实现微信通知处理
    pass
