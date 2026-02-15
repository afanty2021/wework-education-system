"""
支付API模块

提供微信支付、支付宝等支付方式的API端点
"""
from fastapi import APIRouter

from app.api.v1.payment import alipay, wechat

router = APIRouter()

# 注册微信支付路由
router.include_router(wechat.router, prefix="/wechat", tags=["WeChat Pay"])

# 注册支付宝路由
router.include_router(alipay.router, prefix="/alipay", tags=["AliPay"])

__all__ = ["router"]
