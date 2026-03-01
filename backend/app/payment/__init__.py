"""
支付模块

提供微信支付、支付宝等支付方式的集成
"""
from app.payment.alipay import (
    AliPayAPIError,
    AliPayConfigError,
    AliPayService,
    AliPaySignatureError,
    alipay_service,
)
from app.payment.callback_handler import (
    AmountMismatchError,
    ContractNotFoundError,
    DuplicateCallbackError,
    InvalidPaymentStatusError,
    PaymentCallbackError,
    PaymentCallbackHandler,
    PaymentNotFoundError,
    SignatureVerificationError,
    handle_payment_callback,
)
from app.payment.wechat import (
    WeChatPayAPIError,
    WeChatPayConfigError,
    WeChatPayService,
    WeChatPaySignatureError,
    wechat_pay_service,
)

__all__ = [
    # 微信支付
    "WeChatPayService",
    "WeChatPayError",
    "WeChatPayAPIError",
    "WeChatPayConfigError",
    "WeChatPaySignatureError",
    "wechat_pay_service",
    # 支付宝
    "AliPayService",
    "AliPayError",
    "AliPayAPIError",
    "AliPayConfigError",
    "AliPaySignatureError",
    "alipay_service",
    # 回调处理
    "PaymentCallbackHandler",
    "PaymentCallbackError",
    "SignatureVerificationError",
    "AmountMismatchError",
    "PaymentNotFoundError",
    "ContractNotFoundError",
    "DuplicateCallbackError",
    "InvalidPaymentStatusError",
    "handle_payment_callback",
]
