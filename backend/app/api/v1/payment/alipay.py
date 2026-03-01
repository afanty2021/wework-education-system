"""
支付宝支付API路由

提供支付宝支付相关的API端点，包括：
- 创建支付订单
- 查询订单
- 关闭订单
- 申请退款
- 查询退款
- 支付回调处理
"""
import logging
import time
from decimal import Decimal
from typing import Dict, Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.payment import (
    alipay_service,
    handle_payment_callback,
)
from app.payment.alipay import (
    AliPayAPIError,
    AliPayConfigError,
    AliPayService,
    AliPaySignatureError,
)
from app.schemas.payment import PaymentCreate, PaymentUpdate
from app.services.payment_service import (
    ContractNotFoundError,
    InvalidPaymentDataError,
    PaymentNoExistsError,
    PaymentService,
)
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter()


# ==================== Pydantic 模型 ====================


class AliPayOrderCreate(BaseModel):
    """支付宝支付订单创建模型"""
    contract_id: int = Field(..., description="合同ID")
    amount: Decimal = Field(..., gt=0, decimal_places=2, description="支付金额（元）")
    subject: str = Field(..., min_length=1, max_length=128, description="订单标题")
    trade_type: str = Field(..., description="交易类型：alipay.trade.create/wap.pay/app.pay/precreate")
    buyer_id: Optional[str] = Field(None, max_length=128, description="买家支付宝用户ID（小程序支付必填）")
    timeout_express: Optional[str] = Field(None, max_length=20, description="绝对超时时间（格式：30m, 1h, 1d等）")
    total_quantity: Optional[str] = Field(None, max_length=10, description="购买数量")
    operator_id: Optional[str] = Field(None, max_length=28, description="操作员ID")
    store_id: Optional[str] = Field(None, max_length=32, description="商户门店编号")
    attach: Optional[str] = Field(None, max_length=127, description="附加数据")


class AliPayOrderResponse(BaseModel):
    """支付宝支付订单响应模型"""
    order_no: str = Field(..., description="商户订单号")
    trade_no: Optional[str] = Field(None, description="支付宝交易号")
    out_trade_no: Optional[str] = Field(None, description="商户订单号")
    total_amount: Optional[str] = Field(None, description="订单金额")
    receipt_amount: Optional[str] = Field(None, description="实收金额")
    buyer_pay_amount: Optional[str] = Field(None, description="买家付款金额")
    point_amount: Optional[str] = Field(None, description="积分金额")
    invoice_amount: Optional[str] = Field(None, description="发票金额")
    send_pay_date: Optional[str] = Field(None, description="交易付款时间")
    # 小程序支付返回参数
    code: Optional[str] = Field(None, description="小程序支付码")
    # H5支付返回参数
    mweb_url: Optional[str] = Field(None, description="H5支付链接")
    # 扫码支付返回参数
    qr_code: Optional[str] = Field(None, description="二维码内容")


class AliPayRefundCreate(BaseModel):
    """支付宝退款创建模型"""
    order_no: str = Field(..., min_length=1, max_length=64, description="商户订单号")
    refund_no: str = Field(..., min_length=1, max_length=64, description="退款单号")
    refund_amount: Decimal = Field(..., gt=0, decimal_places=2, description="退款金额（元）")
    refund_reason: Optional[str] = Field(None, max_length=256, description="退款原因")
    out_order_no: Optional[str] = Field(None, max_length=64, description="商户订单号（与order_no二选一）")


# ==================== 创建支付订单 ====================


@router.post(
    "/create-order",
    response_model=AliPayOrderResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["AliPay"],
)
async def create_alipay_order(
    order_data: AliPayOrderCreate,
    db: AsyncSession = Depends(get_db),
) -> AliPayOrderResponse:
    """创建支付宝支付订单

    支持小程序支付、H5支付、APP支付和扫码支付

    1. 生成支付订单号
    2. 调用支付宝统一收单API
    3. 创建本地缴费记录
    4. 返回支付参数
    """
    try:
        logger.info(
            f"创建支付宝支付订单: contract_id={order_data.contract_id}, "
            f"amount={order_data.amount}, trade_type={order_data.trade_type}"
        )

        # 生成订单号
        timestamp = int(time.time())
        order_no = f"A{timestamp}{order_data.contract_id:06d}"

        # 1. 调用支付宝统一收单API
        result = await alipay_service.create_order(
            order_no=order_no,
            total_amount=str(order_data.amount),
            subject=order_data.subject,
            trade_type=order_data.trade_type,
            buyer_id=order_data.buyer_id,
            timeout_express=order_data.timeout_express,
            total_quantity=order_data.total_quantity,
            operator_id=order_data.operator_id,
            store_id=order_data.store_id,
        )

        # 2. 创建本地缴费记录
        payment_data = PaymentCreate(
            payment_no=order_no,
            contract_id=order_data.contract_id,
            amount=order_data.amount,
            hours=None,  # 支付回调时更新
            payment_method=2,  # 支付宝
            payment_channel=order_data.trade_type,
            transaction_id=result.get("trade_no"),
            payment_time=None,  # 支付回调时更新
            remark=order_data.attach,
        )

        payment = await PaymentService.create_payment(
            payment_data=payment_data,
            created_by=None,  # TODO: 从认证上下文获取当前用户
            session=db,
        )

        logger.info(
            f"支付宝支付订单创建成功: order_no={order_no}, "
            f"trade_no={result.get('trade_no')}, payment_id={payment.id}"
        )

        # 3. 构建响应
        response_data = AliPayOrderResponse(
            order_no=order_no,
            trade_no=result.get("trade_no"),
            out_trade_no=result.get("out_trade_no"),
            total_amount=result.get("total_amount"),
            receipt_amount=result.get("receipt_amount"),
            buyer_pay_amount=result.get("buyer_pay_amount"),
            point_amount=result.get("point_amount"),
            invoice_amount=result.get("invoice_amount"),
            send_pay_date=result.get("send_pay_date"),
        )

        # 根据支付类型返回不同参数
        if order_data.trade_type == AliPayService.TRADE_TYPE_MINI:
            # 小程序支付返回code
            response_data.code = result.get("code")
        elif order_data.trade_type == AliPayService.TRADE_TYPE_MWEB:
            # H5支付返回跳转链接
            response_data.mweb_url = result.get("mweb_url")
        elif order_data.trade_type == AliPayService.TRADE_TYPE_NATIVE:
            # 扫码支付返回二维码
            response_data.qr_code = result.get("qr_code")

        return response_data

    except ContractNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except PaymentNoExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except InvalidPaymentDataError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except AliPayConfigError as e:
        logger.error(f"支付宝配置错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"支付宝配置错误: {str(e)}"
        )

    except AliPayAPIError as e:
        logger.error(f"支付宝API错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"支付宝API错误: {str(e)}"
        )

    except Exception as e:
        logger.error(f"创建支付宝支付订单失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"创建支付宝支付订单失败: {str(e)}"
        )


# ==================== 支付回调 ====================


@router.post("/notify", tags=["AliPay"])
async def alipay_notify(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> Dict[str, str]:
    """支付宝支付回调通知

    处理支付宝支付结果通知：
    1. 验证签名
    2. 解析回调数据
    3. 更新订单状态
    4. 自动确认缴费（增加合同课时）
    5. 返回成功响应

    使用统一的 PaymentCallbackHandler 处理器，提供：
    - 完整的签名验证
    - 金额匹配验证
    - 防重放攻击保护
    - 自动更新缴费和合同状态
    - 详细的日志记录
    """
    try:
        # 1. 获取回调数据（表单格式）
        form_data = await request.form()

        if not form_data:
            logger.error("支付宝支付回调数据为空")
            return {"data": alipay_service.build_fail_response()}

        # 转换为字典
        form_dict = dict(form_data)

        logger.info(
            f"解析支付宝支付回调: order_no={form_dict.get('out_trade_no')}, "
            f"trade_no={form_dict.get('trade_no')}, "
            f"trade_status={form_dict.get('trade_status')}"
        )

        # 2. 使用统一的回调处理器
        response = await handle_payment_callback(
            payment_method=2,  # 2: 支付宝
            notify_data=form_dict,
            session=db,
            alipay_service=alipay_service,
        )

        # 3. 返回响应
        return {"data": response}

    except Exception as e:
        logger.error(f"处理支付宝支付回调失败: {e}", exc_info=True)
        return {"data": alipay_service.build_fail_response()}


# ==================== 查询订单 ====================


@router.get("/orders/{order_no}", tags=["AliPay"])
async def query_alipay_order(
    order_no: str,
) -> Dict:
    """查询支付宝支付订单

    通过商户订单号查询支付宝支付订单状态
    """
    try:
        logger.info(f"查询支付宝支付订单: order_no={order_no}")

        result = await alipay_service.query_order(order_no=order_no)

        # 解析业务数据
        biz_content = result.get("biz_content", {})

        return {
            "order_no": biz_content.get("out_trade_no"),
            "trade_no": biz_content.get("trade_no"),
            "trade_status": biz_content.get("trade_status"),
            "total_amount": biz_content.get("total_amount"),
            "receipt_amount": biz_content.get("receipt_amount"),
            "buyer_pay_amount": biz_content.get("buyer_pay_amount"),
            "point_amount": biz_content.get("point_amount"),
            "invoice_amount": biz_content.get("invoice_amount"),
            "send_pay_date": biz_content.get("send_pay_date"),
        }

    except AliPayAPIError as e:
        logger.error(f"查询支付宝支付订单失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"查询支付宝支付订单失败: {str(e)}"
        )

    except Exception as e:
        logger.error(f"查询支付宝支付订单失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"查询支付宝支付订单失败: {str(e)}"
        )


# ==================== 申请退款 ====================


@router.post("/refund", tags=["AliPay"])
async def create_alipay_refund(refund_data: AliPayRefundCreate) -> Dict:
    """申请支付宝退款

    调用支付宝退款API申请退款
    """
    try:
        logger.info(
            f"申请支付宝退款: order_no={refund_data.order_no}, "
            f"refund_no={refund_data.refund_no}, refund_amount={refund_data.refund_amount}"
        )

        result = await alipay_service.refund(
            order_no=refund_data.order_no,
            refund_no=refund_data.refund_no,
            refund_amount=str(refund_data.refund_amount),
            refund_reason=refund_data.refund_reason,
            out_order_no=refund_data.out_order_no,
        )

        # 解析业务数据
        biz_content = result.get("biz_content", {})

        return {
            "refund_no": biz_content.get("out_request_no"),
            "refund_status": biz_content.get("refund_status"),
            "refund_amount": biz_content.get("refund_amount"),
            "success": result.get("code") == "10000",
        }

    except AliPayAPIError as e:
        logger.error(f"申请支付宝退款失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"申请支付宝退款失败: {str(e)}"
        )

    except Exception as e:
        logger.error(f"申请支付宝退款失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"申请支付宝退款失败: {str(e)}"
        )


# ==================== 查询退款 ====================


@router.get("/refunds/{refund_no}", tags=["AliPay"])
async def query_alipay_refund(refund_no: str) -> Dict:
    """查询支付宝退款

    通过商户退款单号查询支付宝退款状态
    """
    try:
        logger.info(f"查询支付宝退款: refund_no={refund_no}")

        result = await alipay_service.query_refund(refund_no=refund_no)

        # 解析业务数据
        biz_content = result.get("biz_content", {})

        return {
            "refund_no": biz_content.get("out_request_no"),
            "trade_no": biz_content.get("trade_no"),
            "refund_status": biz_content.get("refund_status"),
            "refund_amount": biz_content.get("refund_amount"),
            "total_amount": biz_content.get("total_amount"),
        }

    except AliPayAPIError as e:
        logger.error(f"查询支付宝退款失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"查询支付宝退款失败: {str(e)}"
        )

    except Exception as e:
        logger.error(f"查询支付宝退款失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"查询支付宝退款失败: {str(e)}"
        )
