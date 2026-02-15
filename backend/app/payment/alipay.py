"""
支付宝支付服务

提供支付宝API集成，包括：
- 统一收单并支付
- 查询订单
- 关闭订单
- 申请退款
- 查询退款
- 支付异步通知处理
- 退款异步通知处理
"""
import base64
import hashlib
import hmac
import json
import logging
import time
from decimal import Decimal
from typing import Any, Dict, Optional
from urllib.parse import quote_plus

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class AliPayError(Exception):
    """支付宝异常基类"""
    pass


class AliPayAPIError(AliPayError):
    """支付宝API错误"""
    pass


class AliPaySignatureError(AliPayError):
    """支付宝签名错误"""
    pass


class AliPayConfigError(AliPayError):
    """支付宝配置错误"""
    pass


class AliPayService:
    """支付宝支付服务类

    提供支付宝支付API的完整集成
    支持小程序支付、H5支付、APP支付和扫码支付
    """

    # 支付宝API地址
    _GATEWAY_URL = "https://openapi.alipay.com/gateway.do"
    _SANDBOX_URL = "https://openapi.alipaydev.com/gateway.do"

    # 支付类型
    TRADE_TYPE_MINI = "alipay.trade.create"  # 小程序支付
    TRADE_TYPE_MWEB = "alipay.trade.wap.pay"  # H5支付
    TRADE_TYPE_APP = "alipay.trade.app.pay"  # APP支付
    TRADE_TYPE_NATIVE = "alipay.trade.precreate"  # 扫码支付

    # 订单状态
    TRADE_STATUS_WAIT_BUYER_PAY = "WAIT_BUYER_PAY"  # 交易创建，等待买家付款
    TRADE_STATUS_TRADE_SUCCESS = "TRADE_SUCCESS"  # 交易支付成功
    TRADE_STATUS_TRADE_FINISHED = "TRADE_FINISHED"  # 交易结束，不可退款
    TRADE_STATUS_TRADE_CLOSED = "TRADE_CLOSED"  # 未付款交易超时关闭

    # 退款状态
    REFUND_STATUS_SUCCESS = "REFUND_SUCCESS"  # 退款成功
    REFUND_STATUS_FAILED = "REFUND_FAILED"  # 退款失败
    REFUND_STATUS_PROCESSING = "REFUND_PROCESSING"  # 退款处理中

    def __init__(self):
        """初始化支付宝服务"""
        if not settings.ALIPAY_APP_ID:
            raise AliPayConfigError("支付宝应用ID未配置")

        if not settings.ALIPAY_PRIVATE_KEY:
            raise AliPayConfigError("支付宝应用私钥未配置")

        if not settings.ALIPAY_PUBLIC_KEY:
            raise AliPayConfigError("支付宝公钥未配置")

        self.app_id = settings.ALIPAY_APP_ID
        self.private_key = settings.ALIPAY_PRIVATE_KEY
        self.public_key = settings.ALIPAY_PUBLIC_KEY
        self.notify_url = settings.ALIPAY_NOTIFY_URL
        self.gateway_url = self._GATEWAY_URL

        # 创建异步HTTP客户端
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """获取HTTP客户端实例

        Returns:
            httpx.AsyncClient: HTTP客户端实例
        """
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json"
                }
            )
        return self._client

    async def close(self):
        """关闭HTTP客户端"""
        if self._client:
            await self._client.aclose()
            self._client = None

    # ==================== 签名相关方法 ====================

    def _generate_sign(self, params: Dict[str, Any]) -> str:
        """生成RSA2签名

        Args:
            params: 待签名参数字典

        Returns:
            str: RSA2签名字符串
        """
        # 过滤空值和sign
        filtered = {k: v for k, v in params.items() if v is not None and v != '' and k != 'sign'}

        # 排序
        sorted_params = sorted(filtered.items())

        # 拼接参数字符串
        sign_str = '&'.join([f'{k}={v}' for k, v in sorted_params])

        # RSA2签名
        try:
            import rsa

            # 将私钥转换为RSAKey对象
            private_key = rsa.PrivateKey.load_pkcs1(self.private_key.encode('utf-8'))

            # 签名
            signature = rsa.sign(sign_str.encode('utf-8'), private_key, 'SHA-256')

            # Base64编码
            sign_base64 = base64.b64encode(signature).decode('utf-8')

            # URL编码
            return quote_plus(sign_base64)

        except ImportError:
            logger.error("未安装rsa库，请运行: pip install rsa")
            raise AliPayConfigError("缺少RSA签名库")

        except Exception as e:
            logger.error(f"RSA签名失败: {e}")
            raise AliPaySignatureError(f"RSA签名失败: {str(e)}")

    def _verify_sign(self, params: Dict[str, Any], sign: str) -> bool:
        """验证RSA2签名

        Args:
            params: 参数字典
            sign: 待验证的签名

        Returns:
            bool: 签名是否有效
        """
        try:
            import rsa

            # 过滤空值和sign
            filtered = {k: v for k, v in params.items() if v is not None and v != '' and k != 'sign'}

            # 排序
            sorted_params = sorted(filtered.items())

            # 拼接参数字符串
            sign_str = '&'.join([f'{k}={v}' for k, v in sorted_params])

            # URL解码签名
            from urllib.parse import unquote_plus
            sign_decoded = unquote_plus(sign)

            # Base64解码
            signature = base64.b64decode(sign_decoded)

            # 将公钥转换为RSAPublicKey对象
            public_key = rsa.PublicKey.load_pkcs1(self.public_key.encode('utf-8'))

            # 验证签名
            result = rsa.verify(sign_str.encode('utf-8'), signature, public_key)

            return result

        except ImportError:
            logger.error("未安装rsa库，请运行: pip install rsa")
            return False

        except Exception as e:
            logger.error(f"签名验证失败: {e}")
            return False

    def _build_public_params(self) -> Dict[str, str]:
        """构建公共参数

        Returns:
            Dict[str, str]: 公共参数字典
        """
        return {
            "app_id": self.app_id,
            "method": "",
            "format": "JSON",
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
            "version": "1.0",
        }

    # ==================== 统一收单并支付 ====================

    async def create_order(
        self,
        order_no: str,
        total_amount: str,
        subject: str,
        trade_type: str,
        buyer_id: Optional[str] = None,
        timeout_express: Optional[str] = None,
        total_quantity: Optional[str] = None,
        goods_detail: Optional[Dict[str, Any]] = None,
        operator_id: Optional[str] = None,
        store_id: Optional[str] = None,
        extend_params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """统一收单并支付

        Args:
            order_no: 商户订单号（唯一）
            total_amount: 订单总金额（元，保留两位小数）
            subject: 订单标题
            trade_type: 交易类型（alipay.trade.create/wap.pay/app.pay/precreate）
            buyer_id: 买家支付宝用户ID（小程序支付必填）
            timeout_express: 绝对超时时间（格式：30m, 1h, 1d等）
            total_quantity: 购买数量
            goods_detail: 商品详情
            operator_id: 操作员ID
            store_id: 商户门店编号
            extend_params: 扩展参数
            **kwargs: 其他参数

        Returns:
            Dict[str, Any]: 下单结果

        Raises:
            AliPayConfigError: 配置错误
            AliPayAPIError: API调用失败
        """
        logger.info(f"创建支付宝订单: order_no={order_no}, total_amount={total_amount}, trade_type={trade_type}")

        # 验证交易类型
        if trade_type not in [
            self.TRADE_TYPE_MINI,
            self.TRADE_TYPE_MWEB,
            self.TRADE_TYPE_APP,
            self.TRADE_TYPE_NATIVE
        ]:
            raise AliPayConfigError(f"不支持的交易类型: {trade_type}")

        # 小程序支付需要buyer_id
        if trade_type == self.TRADE_TYPE_MINI and not buyer_id:
            raise AliPayConfigError("小程序支付必须提供buyer_id")

        # 构建业务参数
        biz_content = {
            "out_trade_no": order_no,
            "total_amount": total_amount,
            "subject": subject,
        }

        # 添加可选参数
        if buyer_id:
            biz_content["buyer_id"] = buyer_id
        if timeout_express:
            biz_content["timeout_express"] = timeout_express
        if total_quantity:
            biz_content["total_quantity"] = total_quantity
        if goods_detail:
            biz_content["goods_detail"] = goods_detail
        if operator_id:
            biz_content["operator_id"] = operator_id
        if store_id:
            biz_content["store_id"] = store_id
        if extend_params:
            biz_content["extend_params"] = extend_params

        # 添加额外参数
        biz_content.update(kwargs)

        # 构建请求参数
        params = self._build_public_params()
        params["method"] = trade_type
        params["notify_url"] = self.notify_url
        params["biz_content"] = json.dumps(biz_content, ensure_ascii=False)

        # 生成签名
        params["sign"] = self._generate_sign(params)

        try:
            client = await self._get_client()

            # 发送请求
            response = await client.post(
                self.gateway_url,
                data=params,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )

            response.raise_for_status()

            # 解析响应
            result = response.json()

            # 检查响应
            if result.get("code") != "10000":
                error_msg = result.get("sub_msg", result.get("msg", "未知错误"))
                logger.error(f"支付宝下单失败: {error_msg}")
                raise AliPayAPIError(f"支付宝下单失败: {error_msg}")

            logger.info(f"支付宝订单创建成功: order_no={order_no}")
            return result

        except httpx.HTTPError as e:
            logger.error(f"支付宝API请求失败: {e}")
            raise AliPayAPIError(f"支付宝API请求失败: {str(e)}")

    # ==================== 查询订单 ====================

    async def query_order(
        self,
        order_no: Optional[str] = None,
        trade_no: Optional[str] = None
    ) -> Dict[str, Any]:
        """查询订单

        Args:
            order_no: 商户订单号
            trade_no: 支付宝交易号

        Returns:
            Dict[str, Any]: 订单信息

        Raises:
            AliPayConfigError: 配置错误
            AliPayAPIError: API调用失败
        """
        if not order_no and not trade_no:
            raise AliPayConfigError("订单号和支付宝交易号必须提供其中一个")

        logger.info(f"查询支付宝订单: order_no={order_no}, trade_no={trade_no}")

        # 构建业务参数
        biz_content = {}

        if order_no:
            biz_content["out_trade_no"] = order_no
        if trade_no:
            biz_content["trade_no"] = trade_no

        # 构建请求参数
        params = self._build_public_params()
        params["method"] = "alipay.trade.query"
        params["biz_content"] = json.dumps(biz_content, ensure_ascii=False)

        # 生成签名
        params["sign"] = self._generate_sign(params)

        try:
            client = await self._get_client()

            # 发送请求
            response = await client.post(
                self.gateway_url,
                data=params,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )

            response.raise_for_status()

            # 解析响应
            result = response.json()

            # 检查响应
            if result.get("code") != "10000":
                error_msg = result.get("sub_msg", result.get("msg", "未知错误"))
                logger.error(f"查询支付宝订单失败: {error_msg}")
                raise AliPayAPIError(f"查询支付宝订单失败: {error_msg}")

            logger.info(f"查询支付宝订单成功: order_no={order_no}")
            return result

        except httpx.HTTPError as e:
            logger.error(f"支付宝API请求失败: {e}")
            raise AliPayAPIError(f"支付宝API请求失败: {str(e)}")

    # ==================== 关闭订单 ====================

    async def close_order(self, order_no: str) -> Dict[str, Any]:
        """关闭订单

        Args:
            order_no: 商户订单号

        Returns:
            Dict[str, Any]: 关闭结果

        Raises:
            AliPayAPIError: API调用失败
        """
        logger.info(f"关闭支付宝订单: order_no={order_no}")

        # 构建业务参数
        biz_content = {
            "out_trade_no": order_no
        }

        # 构建请求参数
        params = self._build_public_params()
        params["method"] = "alipay.trade.close"
        params["biz_content"] = json.dumps(biz_content, ensure_ascii=False)

        # 生成签名
        params["sign"] = self._generate_sign(params)

        try:
            client = await self._get_client()

            # 发送请求
            response = await client.post(
                self.gateway_url,
                data=params,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )

            response.raise_for_status()

            # 解析响应
            result = response.json()

            # 检查响应（关闭订单可能返回40004，表示订单已支付）
            if result.get("code") not in ["10000", "40004"]:
                error_msg = result.get("sub_msg", result.get("msg", "未知错误"))
                logger.error(f"关闭支付宝订单失败: {error_msg}")
                raise AliPayAPIError(f"关闭支付宝订单失败: {error_msg}")

            logger.info(f"关闭支付宝订单成功: order_no={order_no}")
            return result

        except httpx.HTTPError as e:
            logger.error(f"支付宝API请求失败: {e}")
            raise AliPayAPIError(f"支付宝API请求失败: {str(e)}")

    # ==================== 申请退款 ====================

    async def refund(
        self,
        order_no: str,
        refund_no: str,
        refund_amount: str,
        refund_reason: Optional[str] = None,
        out_order_no: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """申请退款

        Args:
            order_no: 商户订单号
            refund_no: 退款单号
            refund_amount: 退款金额（元，保留两位小数）
            refund_reason: 退款原因
            out_order_no: 商户订单号（与order_no二选一）
            **kwargs: 其他参数

        Returns:
            Dict[str, Any]: 退款结果

        Raises:
            AliPayAPIError: API调用失败
        """
        logger.info(f"申请支付宝退款: order_no={order_no}, refund_no={refund_no}, refund_amount={refund_amount}")

        # 构建业务参数
        biz_content = {
            "out_trade_no": order_no if order_no else out_order_no,
            "refund_amount": refund_amount,
            "refund_reason": refund_reason or "用户申请退款",
            "out_request_no": refund_no,
        }

        # 添加额外参数
        biz_content.update(kwargs)

        # 构建请求参数
        params = self._build_public_params()
        params["method"] = "alipay.trade.refund"
        params["biz_content"] = json.dumps(biz_content, ensure_ascii=False)

        # 生成签名
        params["sign"] = self._generate_sign(params)

        try:
            client = await self._get_client()

            # 发送请求
            response = await client.post(
                self.gateway_url,
                data=params,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )

            response.raise_for_status()

            # 解析响应
            result = response.json()

            # 检查响应
            if result.get("code") != "10000":
                error_msg = result.get("sub_msg", result.get("msg", "未知错误"))
                logger.error(f"申请支付宝退款失败: {error_msg}")
                raise AliPayAPIError(f"申请支付宝退款失败: {error_msg}")

            logger.info(f"申请支付宝退款成功: refund_no={refund_no}")
            return result

        except httpx.HTTPError as e:
            logger.error(f"支付宝API请求失败: {e}")
            raise AliPayAPIError(f"支付宝API请求失败: {str(e)}")

    # ==================== 查询退款 ====================

    async def query_refund(
        self,
        refund_no: Optional[str] = None,
        trade_no: Optional[str] = None,
        order_no: Optional[str] = None
    ) -> Dict[str, Any]:
        """查询退款

        Args:
            refund_no: 商户退款单号
            trade_no: 支付宝交易号
            order_no: 商户订单号

        Returns:
            Dict[str, Any]: 退款信息

        Raises:
            AliPayConfigError: 配置错误
            AliPayAPIError: API调用失败
        """
        if not refund_no and not trade_no and not order_no:
            raise AliPayConfigError("退款单号、支付宝交易号和商户订单号必须提供其中一个")

        logger.info(f"查询支付宝退款: refund_no={refund_no}, trade_no={trade_no}, order_no={order_no}")

        # 构建业务参数
        biz_content = {}

        if refund_no:
            biz_content["out_request_no"] = refund_no
        if trade_no:
            biz_content["trade_no"] = trade_no
        if order_no:
            biz_content["out_trade_no"] = order_no

        # 构建请求参数
        params = self._build_public_params()
        params["method"] = "alipay.trade.fastpay.refund.query"
        params["biz_content"] = json.dumps(biz_content, ensure_ascii=False)

        # 生成签名
        params["sign"] = self._generate_sign(params)

        try:
            client = await self._get_client()

            # 发送请求
            response = await client.post(
                self.gateway_url,
                data=params,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )

            response.raise_for_status()

            # 解析响应
            result = response.json()

            # 检查响应
            if result.get("code") != "10000":
                error_msg = result.get("sub_msg", result.get("msg", "未知错误"))
                logger.error(f"查询支付宝退款失败: {error_msg}")
                raise AliPayAPIError(f"查询支付宝退款失败: {error_msg}")

            logger.info(f"查询支付宝退款成功: refund_no={refund_no}")
            return result

        except httpx.HTTPError as e:
            logger.error(f"支付宝API请求失败: {e}")
            raise AliPayAPIError(f"支付宝API请求失败: {str(e)}")

    # ==================== 回调处理 ====================

    def parse_notify(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """解析支付回调通知

        Args:
            form_data: 表单格式的回调数据

        Returns:
            Dict[str, Any]: 解析后的回调数据

        Raises:
            AliPaySignatureError: 签名验证失败
        """
        logger.info("解析支付宝支付回调通知")

        # 验证签名
        if "sign" not in form_data:
            raise AliPaySignatureError("回调数据缺少签名")

        if not self._verify_sign(form_data, form_data["sign"]):
            raise AliPaySignatureError("回调数据签名验证失败")

        # 解析业务数据
        biz_content_str = form_data.get("biz_content", "{}")
        try:
            biz_content = json.loads(biz_content) if isinstance(biz_content_str, str) else biz_content_str
        except json.JSONDecodeError:
            biz_content = {}

        logger.info(f"解析支付宝支付回调成功: order_no={biz_content.get('out_trade_no')}")
        return biz_content

    def parse_refund_notify(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """解析退款回调通知

        Args:
            form_data: 表单格式的回调数据

        Returns:
            Dict[str, Any]: 解析后的回调数据

        Raises:
            AliPaySignatureError: 签名验证失败
        """
        logger.info("解析支付宝退款回调通知")

        # 验证签名
        if "sign" not in form_data:
            raise AliPaySignatureError("退款回调数据缺少签名")

        if not self._verify_sign(form_data, form_data["sign"]):
            raise AliPaySignatureError("退款回调数据签名验证失败")

        # 解析业务数据
        biz_content_str = form_data.get("biz_content", "{}")
        try:
            biz_content = json.loads(biz_content_str) if isinstance(biz_content_str, str) else biz_content_str
        except json.JSONDecodeError:
            biz_content = {}

        logger.info(f"解析支付宝退款回调成功: refund_no={biz_content.get('out_request_no')}")
        return biz_content

    def build_success_response(self) -> str:
        """构建成功响应

        Returns:
            str: success字符串
        """
        return "success"

    def build_fail_response(self) -> str:
        """构建失败响应

        Returns:
            str: fail字符串
        """
        return "fail"


# 创建服务实例
alipay_service = AliPayService()
