"""
微信支付API路由

提供微信支付相关的API端点，包括：
- 创建支付订单
- 查询订单
- 关闭订单
- 申请退款
- 查询退款
- 支付回调处理
"""
import logging
from decimal import Decimal
from typing import Dict, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.payment import (
    handle_payment_callback,
    wechat_pay_service,
)
from app.payment.wechat import (
    WeChatPayAPIError,
    WeChatPayConfigError,
    WeChatPayService,
    WeChatPaySignatureError,
    fen_to_yuan,
    yuan_to_fen,
)
from app.schemas.payment import PaymentCreate, PaymentResponse
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


class WeChatOrderCreate(BaseModel):
    """微信支付订单创建模型"""
    contract_id: int = Field(..., description="合同ID")
    amount: Decimal = Field(..., gt=0, decimal_places=2, description="支付金额（元）")
    body: str = Field(..., min_length=1, max_length=127, description="商品描述")
    trade_type: str = Field(..., description="交易类型：JSAPI/MWEB/APP/NATIVE")
    openid: Optional[str] = Field(None, max_length=128, description="用户标识（JSAPI必填）")
    client_ip: str = Field("127.0.0.1", description="终端IP")
    attach: Optional[str] = Field(None, max_length=127, description="附加数据")
    detail: Optional[Dict] = Field(None, description="商品详情")
    goods_tag: Optional[str] = Field(None, max_length=32, description="订单优惠标记")


class WeChatOrderResponse(BaseModel):
    """微信支付订单响应模型"""
    order_no: str = Field(..., description="商户订单号")
    prepay_id: str = Field(..., description="预支付交易会话标识")
    code_url: Optional[str] = Field(None, description="二维码链接（NATIVE支付）")
    mweb_url: Optional[str] = Field(None, description="支付跳转链接（MWEB支付）")
    # JSAPI支付需要额外参数
    appid: Optional[str] = Field(None, description="小程序APPID")
    timestamp: Optional[str] = Field(None, description="时间戳")
    nonce_str: Optional[str] = Field(None, description="随机字符串")
    package: Optional[str] = Field(None, description="订单详情扩展字符串")
    sign_type: Optional[str] = Field(None, description="签名方式")
    pay_sign: Optional[str] = Field(None, description="签名")


class WeChatRefundCreate(BaseModel):
    """微信支付退款创建模型"""
    order_no: str = Field(..., min_length=1, max_length=50, description="商户订单号")
    refund_no: str = Field(..., min_length=1, max_length=50, description="退款单号")
    total_fee: Decimal = Field(..., gt=0, decimal_places=2, description="订单总金额（元）")
    refund_fee: Decimal = Field(..., gt=0, decimal_places=2, description="退款金额（元）")
    refund_desc: Optional[str] = Field(None, max_length=80, description="退款原因")


# ==================== 创建支付订单 ====================


@router.post(
    "/create-order",
    response_model=WeChatOrderResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["WeChat Pay"],
)
async def create_wechat_order(
    order_data: WeChatOrderCreate,
    db: AsyncSession = Depends(get_db),
) -> WeChatOrderResponse:
    """创建微信支付订单

    支持小程序支付、H5支付和Native支付

    1. 生成支付订单号
    2. 调用微信统一下单API
    3. 创建本地缴费记录
    4. 返回支付参数
    """
    try:
        import time

        logger.info(
            f"创建微信支付订单: contract_id={order_data.contract_id}, "
            f"amount={order_data.amount}, trade_type={order_data.trade_type}"
        )

        # 生成订单号
        timestamp = int(time.time())
        order_no = f"W{timestamp}{order_data.contract_id:06d}"

        # 1. 调用微信统一下单API
        result = await wechat_pay_service.create_order(
            order_no=order_no,
            total_fee=yuan_to_fen(order_data.amount),
            body=order_data.body,
            trade_type=order_data.trade_type,
            openid=order_data.openid,
            client_ip=order_data.client_ip,
            time_expire=None,  # TODO: 设置订单过期时间
            attach=order_data.attach,
            detail=order_data.detail,
            goods_tag=order_data.goods_tag,
        )

        # 2. 创建本地缴费记录
        payment_data = PaymentCreate(
            payment_no=order_no,
            contract_id=order_data.contract_id,
            amount=order_data.amount,
            hours=None,  # 支付回调时更新
            payment_method=1,  # 微信支付
            payment_channel=order_data.trade_type,
            transaction_id=result.get("prepay_id"),
            payment_time=None,  # 支付回调时更新
            remark=order_data.attach,
        )

        payment = await PaymentService.create_payment(
            payment_data=payment_data,
            created_by=None,  # TODO: 从认证上下文获取当前用户
            session=db,
        )

        logger.info(
            f"微信支付订单创建成功: order_no={order_no}, "
            f"prepay_id={result.get('prepay_id')}, payment_id={payment.id}"
        )

        # 3. 构建响应
        response_data = WeChatOrderResponse(
            order_no=order_no,
            prepay_id=result.get("prepay_id", ""),
            code_url=result.get("code_url"),
            mweb_url=result.get("mweb_url"),
        )

        # JSAPI支付需要额外参数
        if order_data.trade_type == WeChatPayService.TRADE_TYPE_JSAPI:
            import random
            import string

            timestamp = str(int(time.time()))
            nonce_str = "".join(
                random.choice(string.ascii_letters + string.digits) for _ in range(32)
            )

            # 构建支付参数
            response_data.appid = result.get("appid")
            response_data.timestamp = timestamp
            response_data.nonce_str = nonce_str
            response_data.package = f"prepay_id={result.get('prepay_id')}"
            response_data.sign_type = "MD5"

            # 生成支付签名
            pay_sign = wechat_pay_service._generate_sign(
                {
                    "appId": response_data.appid,
                    "timeStamp": timestamp,
                    "nonceStr": nonce_str,
                    "package": response_data.package,
                    "signType": "MD5",
                }
            )

            response_data.pay_sign = pay_sign

        return response_data

    except ContractNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except PaymentNoExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except InvalidPaymentDataError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except WeChatPayConfigError as e:
        logger.error(f"微信支付配置错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"微信支付配置错误: {str(e)}"
        )

    except WeChatPayAPIError as e:
        logger.error(f"微信支付API错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"微信支付API错误: {str(e)}"
        )

    except Exception as e:
        logger.error(f"创建微信支付订单失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"创建微信支付订单失败: {str(e)}"
        )


# ==================== 支付回调 ====================


@router.post("/notify", tags=["WeChat Pay"])
async def wechat_pay_notify(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> Dict[str, str]:
    """微信支付回调通知

    处理微信支付结果通知：
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
        # 1. 获取回调数据
        xml_data = await request.body()

        if not xml_data:
            logger.error("微信支付回调数据为空")
            return {"data": wechat_pay_service.build_fail_response("数据为空")}

        logger.debug(f"收到微信支付回调: {xml_data[:200]}")

        # 2. 解析XML为字典
        import xml.etree.ElementTree as ET

        root = ET.fromstring(xml_data)
        notify_data = {child.tag: child.text for child in root}

        logger.info(
            f"解析微信支付回调: order_no={notify_data.get('out_trade_no')}, "
            f"transaction_id={notify_data.get('transaction_id')}, "
            f"trade_state={notify_data.get('trade_state')}"
        )

        # 3. 使用统一的回调处理器
        response = await handle_payment_callback(
            payment_method=1,  # 1: 微信支付
            notify_data=notify_data,
            session=db,
            wechat_service=wechat_pay_service,
        )

        # 4. 返回响应
        return {"data": response}

    except Exception as e:
        logger.error(f"处理微信支付回调失败: {e}", exc_info=True)
        return {"data": wechat_pay_service.build_fail_response("处理失败")}


# ==================== 查询订单 ====================


@router.get("/orders/{order_no}", tags=["WeChat Pay"])
async def query_wechat_order(
    order_no: str,
) -> Dict:
    """查询微信支付订单

    通过商户订单号查询微信支付订单状态
    """
    try:
        logger.info(f"查询微信支付订单: order_no={order_no}")

        result = await wechat_pay_service.query_order(order_no=order_no)

        return {
            "order_no": result.get("out_trade_no"),
            "transaction_id": result.get("transaction_id"),
            "trade_state": result.get("trade_state"),
            "trade_state_desc": result.get("trade_state_desc"),
            "total_fee": fen_to_yuan(int(result.get("total_fee", 0))),
            "cash_fee": fen_to_yuan(int(result.get("cash_fee", 0))),
            "transaction_id": result.get("transaction_id"),
            "time_end": result.get("time_end"),
        }

    except WeChatPayAPIError as e:
        logger.error(f"查询微信支付订单失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"查询微信支付订单失败: {str(e)}"
        )

    except Exception as e:
        logger.error(f"查询微信支付订单失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"查询微信支付订单失败: {str(e)}"
        )


# ==================== 申请退款 ====================


@router.post("/refund", tags=["WeChat Pay"])
async def create_wechat_refund(refund_data: WeChatRefundCreate) -> Dict:
    """申请微信支付退款

    调用微信支付退款API申请退款
    """
    try:
        logger.info(
            f"申请微信支付退款: order_no={refund_data.order_no}, "
            f"refund_no={refund_data.refund_no}, refund_fee={refund_data.refund_fee}"
        )

        result = await wechat_pay_service.refund(
            order_no=refund_data.order_no,
            refund_no=refund_data.refund_no,
            total_fee=yuan_to_fen(refund_data.total_fee),
            refund_fee=yuan_to_fen(refund_data.refund_fee),
            refund_desc=refund_data.refund_desc,
        )

        return {
            "refund_no": result.get("out_refund_no"),
            "refund_id": result.get("refund_id"),
            "refund_status": result.get("refund_status"),
            "refund_channel": result.get("refund_channel"),
            "refund_fee": fen_to_yuan(int(result.get("refund_fee", 0))),
            "success_time": result.get("success_time"),
            "success": result.get("result_code") == "SUCCESS",
        }

    except WeChatPayAPIError as e:
        logger.error(f"申请微信支付退款失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"申请微信支付退款失败: {str(e)}"
        )

    except Exception as e:
        logger.error(f"申请微信支付退款失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"申请微信支付退款失败: {str(e)}"
        )


# ==================== 查询退款 ====================


@router.get("/refunds/{refund_no}", tags=["WeChat Pay"])
async def query_wechat_refund(refund_no: str) -> Dict:
    """查询微信支付退款

    通过商户退款单号查询微信支付退款状态
    """
    try:
        logger.info(f"查询微信支付退款: refund_no={refund_no}")

        result = await wechat_pay_service.query_refund(refund_no=refund_no)

        return {
            "refund_no": result.get("out_refund_no"),
            "refund_id": result.get("refund_id"),
            "refund_status": result.get("refund_status"),
            "refund_status_desc": result.get("refund_status_desc"),
            "refund_channel": result.get("refund_channel"),
            "refund_fee": fen_to_yuan(int(result.get("refund_fee", 0))),
            "total_fee": fen_to_yuan(int(result.get("total_fee", 0))),
            "success_time": result.get("success_time"),
            "recv_account": result.get("recv_account"),
        }

    except WeChatPayAPIError as e:
        logger.error(f"查询微信支付退款失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"查询微信支付退款失败: {str(e)}"
        )

    except Exception as e:
        logger.error(f"查询微信支付退款失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"查询微信支付退款失败: {str(e)}"
        )
