"""
微信支付服务

提供微信支付API集成，包括：
- 统一下单
- 查询订单
- 关闭订单
- 申请退款
- 查询退款
- 支付回调处理
- 退款回调处理
"""
import hashlib
import hmac
import json
import logging
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class WeChatPayError(Exception):
    """微信支付异常基类"""
    pass


class WeChatPayAPIError(WeChatPayError):
    """微信支付API错误"""
    pass


class WeChatPaySignatureError(WeChatPayError):
    """微信支付签名错误"""
    pass


class WeChatPayConfigError(WeChatPayError):
    """微信支付配置错误"""
    pass


class WeChatPayService:
    """微信支付服务类

    提供微信支付V3版本API的完整集成
    支持小程序支付、H5支付和Native支付
    """

    # 微信支付API地址
    _BASE_URL = "https://api.mch.weixin.qq.com"
    _SANDBOX_URL = "https://api.mch.weixin.qq.com/sandboxnew"

    # 支付类型
    TRADE_TYPE_JSAPI = "JSAPI"  # 小程序支付
    TRADE_TYPE_MWEB = "MWEB"  # H5支付
    TRADE_TYPE_APP = "APP"  # APP支付
    TRADE_TYPE_NATIVE = "NATIVE"  # Native支付

    # 订单状态
    TRADE_STATE_SUCCESS = "SUCCESS"  # 支付成功
    TRADE_STATE_REFUND = "REFUND"  # 转入退款
    TRADE_STATE_NOTPAY = "NOTPAY"  # 未支付
    TRADE_STATE_CLOSED = "CLOSED"  # 已关闭
    TRADE_STATE_REVOKED = "REVOKED"  # 已撤销
    TRADE_STATE_USERPAYING = "USERPAYING"  # 用户支付中
    TRADE_STATE_PAYERROR = "PAYERROR"  # 支付失败

    # 退款状态
    REFUND_STATE_SUCCESS = "SUCCESS"  # 退款成功
    REFUND_STATE_FAILED = "FAILED"  # 退款失败
    REFUND_STATE_PROCESSING = "PROCESSING"  # 退款处理中
    REFUND_STATE_ABNORMAL = "ABNORMAL"  # 退款异常

    def __init__(self):
        """初始化微信支付服务"""
        if not settings.WECHAT_MCH_ID:
            raise WeChatPayConfigError("微信支付商户号未配置")

        if not settings.WECHAT_MCH_KEY:
            raise WeChatPayConfigError("微信支付商户密钥未配置")

        self.mch_id = settings.WECHAT_MCH_ID
        self.mch_key = settings.WECHAT_MCH_KEY
        self.notify_url = settings.WECHAT_NOTIFY_URL
        self.base_url = self._BASE_URL

        # 创建异步HTTP客户端
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """获取HTTP客户端实例"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=httpx.Timeout(30.0),
                headers={
                    "Content-Type": "application/json",
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

    def _generate_nonce_str(self) -> str:
        """生成随机字符串

        Returns:
            str: 32位随机字符串
        """
        import random
        import string

        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))

    def _generate_sign(self, params: Dict[str, Any]) -> str:
        """生成签名

        Args:
            params: 待签名参数字典

        Returns:
            str: 签名字符串
        """
        # 过滤空值并排序
        filtered = {k: v for k, v in params.items() if v is not None and v != ''}
        sorted_params = sorted(filtered.items())

        # 拼接参数字符串
        sign_str = '&'.join([f'{k}={v}' for k, v in sorted_params])
        sign_str = f'{sign_str}&key={self.mch_key}'

        # MD5签名并转大写
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()

    def _generate_hmac_sha256_sign(self, params: Dict[str, Any]) -> str:
        """生成HMAC-SHA256签名

        Args:
            params: 待签名参数字典

        Returns:
            str: 签名字符串
        """
        # 过滤空值并排序
        filtered = {k: v for k, v in params.items() if v is not None and v != ''}
        sorted_params = sorted(filtered.items())

        # 拼接参数字符串
        sign_str = '&'.join([f'{k}={v}' for k, v in sorted_params])
        sign_str = f'{sign_str}&key={self.mch_key}'

        # HMAC-SHA256签名
        return hmac.new(
            self.mch_key.encode('utf-8'),
            sign_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest().upper()

    def _verify_sign(self, params: Dict[str, Any], sign: str) -> bool:
        """验证签名

        Args:
            params: 参数字典
            sign: 待验证的签名

        Returns:
            bool: 签名是否有效
        """
        calculated_sign = self._generate_sign(params)
        return calculated_sign == sign

    # ==================== 统一下单 ====================

    async def create_order(
        self,
        order_no: str,
        total_fee: int,
        body: str,
        trade_type: str,
        openid: Optional[str] = None,
        client_ip: str = "127.0.0.1",
        time_expire: Optional[str] = None,
        attach: Optional[str] = None,
        detail: Optional[Dict[str, Any]] = None,
        goods_tag: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """创建统一下单

        Args:
            order_no: 商户订单号（唯一）
            total_fee: 订单总金额（分）
            body: 商品描述
            trade_type: 交易类型（JSAPI/MWEB/APP/NATIVE）
            openid: 用户标识（JSAPI必填）
            client_ip: 终端IP
            time_expire: 订单失效时间（格式：yyyyMMddHHmmss）
            attach: 附加数据
            detail: 商品详情
            goods_tag: 订单优惠标记
            **kwargs: 其他参数

        Returns:
            Dict[str, Any]: 下单结果

        Raises:
            WeChatPayConfigError: 配置错误
            WeChatPayAPIError: API调用失败
        """
        logger.info(f"创建微信支付订单: order_no={order_no}, total_fee={total_fee}, trade_type={trade_type}")

        # 验证交易类型
        if trade_type not in [
            self.TRADE_TYPE_JSAPI,
            self.TRADE_TYPE_MWEB,
            self.TRADE_TYPE_APP,
            self.TRADE_TYPE_NATIVE
        ]:
            raise WeChatPayConfigError(f"不支持的交易类型: {trade_type}")

        # JSAPI支付需要openid
        if trade_type == self.TRADE_TYPE_JSAPI and not openid:
            raise WeChatPayConfigError("JSAPI支付必须提供openid")

        # 构建请求参数
        params = {
            "appid": settings.WEWORK_CORP_ID,
            "mch_id": self.mch_id,
            "nonce_str": self._generate_nonce_str(),
            "body": body,
            "out_trade_no": order_no,
            "total_fee": total_fee,
            "spbill_create_ip": client_ip,
            "notify_url": self.notify_url,
            "trade_type": trade_type,
        }

        # 添加可选参数
        if openid:
            params["openid"] = openid
        if time_expire:
            params["time_expire"] = time_expire
        if attach:
            params["attach"] = attach
        if detail:
            params["detail"] = json.dumps(detail, ensure_ascii=False)
        if goods_tag:
            params["goods_tag"] = goods_tag

        # 添加额外参数
        params.update(kwargs)

        # 生成签名
        params["sign"] = self._generate_sign(params)

        try:
            client = await self._get_client()

            # 发送请求
            response = await client.post(
                "/pay/unifiedorder",
                content=self._dict_to_xml(params),
                headers={"Content-Type": "application/xml"}
            )

            response.raise_for_status()

            # 解析响应
            result = self._xml_to_dict(response.text)

            # 验证签名
            if "sign" in result and not self._verify_sign(result, result["sign"]):
                raise WeChatPaySignatureError("微信支付响应签名验证失败")

            # 检查返回状态
            if result.get("return_code") != "SUCCESS":
                error_msg = result.get("return_msg", "未知错误")
                logger.error(f"微信支付下单失败: {error_msg}")
                raise WeChatPayAPIError(f"微信支付下单失败: {error_msg}")

            if result.get("result_code") != "SUCCESS":
                error_msg = result.get("err_code_des", "未知错误")
                logger.error(f"微信支付下单失败: {error_msg}")
                raise WeChatPayAPIError(f"微信支付下单失败: {error_msg}")

            logger.info(f"微信支付订单创建成功: order_no={order_no}, prepay_id={result.get('prepay_id')}")
            return result

        except httpx.HTTPError as e:
            logger.error(f"微信支付API请求失败: {e}")
            raise WeChatPayAPIError(f"微信支付API请求失败: {str(e)}")

    # ==================== 查询订单 ====================

    async def query_order(
        self,
        order_no: Optional[str] = None,
        transaction_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """查询订单

        Args:
            order_no: 商户订单号
            transaction_id: 微信支付订单号

        Returns:
            Dict[str, Any]: 订单信息

        Raises:
            WeChatPayConfigError: 配置错误
            WeChatPayAPIError: API调用失败
        """
        if not order_no and not transaction_id:
            raise WeChatPayConfigError("订单号和微信支付订单号必须提供其中一个")

        logger.info(f"查询微信支付订单: order_no={order_no}, transaction_id={transaction_id}")

        # 构建请求参数
        params = {
            "appid": settings.WEWORK_CORP_ID,
            "mch_id": self.mch_id,
            "nonce_str": self._generate_nonce_str(),
        }

        if order_no:
            params["out_trade_no"] = order_no
        if transaction_id:
            params["transaction_id"] = transaction_id

        # 生成签名
        params["sign"] = self._generate_sign(params)

        try:
            client = await self._get_client()

            # 发送请求
            response = await client.post(
                "/pay/orderquery",
                content=self._dict_to_xml(params),
                headers={"Content-Type": "application/xml"}
            )

            response.raise_for_status()

            # 解析响应
            result = self._xml_to_dict(response.text)

            # 验证签名
            if "sign" in result and not self._verify_sign(result, result["sign"]):
                raise WeChatPaySignatureError("微信支付响应签名验证失败")

            # 检查返回状态
            if result.get("return_code") != "SUCCESS":
                error_msg = result.get("return_msg", "未知错误")
                logger.error(f"查询微信支付订单失败: {error_msg}")
                raise WeChatPayAPIError(f"查询微信支付订单失败: {error_msg}")

            logger.info(f"查询微信支付订单成功: order_no={order_no}, trade_state={result.get('trade_state')}")
            return result

        except httpx.HTTPError as e:
            logger.error(f"微信支付API请求失败: {e}")
            raise WeChatPayAPIError(f"微信支付API请求失败: {str(e)}")

    # ==================== 关闭订单 ====================

    async def close_order(self, order_no: str) -> Dict[str, Any]:
        """关闭订单

        Args:
            order_no: 商户订单号

        Returns:
            Dict[str, Any]: 关闭结果

        Raises:
            WeChatPayAPIError: API调用失败
        """
        logger.info(f"关闭微信支付订单: order_no={order_no}")

        # 构建请求参数
        params = {
            "appid": settings.WEWORK_CORP_ID,
            "mch_id": self.mch_id,
            "out_trade_no": order_no,
            "nonce_str": self._generate_nonce_str(),
        }

        # 生成签名
        params["sign"] = self._generate_sign(params)

        try:
            client = await self._get_client()

            # 发送请求
            response = await client.post(
                "/pay/closeorder",
                content=self._dict_to_xml(params),
                headers={"Content-Type": "application/xml"}
            )

            response.raise_for_status()

            # 解析响应
            result = self._xml_to_dict(response.text)

            # 验证签名
            if "sign" in result and not self._verify_sign(result, result["sign"]):
                raise WeChatPaySignatureError("微信支付响应签名验证失败")

            # 检查返回状态
            if result.get("return_code") != "SUCCESS":
                error_msg = result.get("return_msg", "未知错误")
                logger.error(f"关闭微信支付订单失败: {error_msg}")
                raise WeChatPayAPIError(f"关闭微信支付订单失败: {error_msg}")

            if result.get("result_code") != "SUCCESS":
                error_msg = result.get("err_code_des", "未知错误")
                logger.error(f"关闭微信支付订单失败: {error_msg}")
                raise WeChatPayAPIError(f"关闭微信支付订单失败: {error_msg}")

            logger.info(f"关闭微信支付订单成功: order_no={order_no}")
            return result

        except httpx.HTTPError as e:
            logger.error(f"微信支付API请求失败: {e}")
            raise WeChatPayAPIError(f"微信支付API请求失败: {str(e)}")

    # ==================== 申请退款 ====================

    async def refund(
        self,
        order_no: str,
        refund_no: str,
        total_fee: int,
        refund_fee: int,
        refund_desc: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """申请退款

        Args:
            order_no: 商户订单号
            refund_no: 退款单号
            total_fee: 订单总金额（分）
            refund_fee: 退款金额（分）
            refund_desc: 退款原因
            **kwargs: 其他参数

        Returns:
            Dict[str, Any]: 退款结果

        Raises:
            WeChatPayAPIError: API调用失败
        """
        logger.info(f"申请微信支付退款: order_no={order_no}, refund_no={refund_no}, refund_fee={refund_fee}")

        # 构建请求参数
        params = {
            "appid": settings.WEWORK_CORP_ID,
            "mch_id": self.mch_id,
            "nonce_str": self._generate_nonce_str(),
            "out_trade_no": order_no,
            "out_refund_no": refund_no,
            "total_fee": total_fee,
            "refund_fee": refund_fee,
            "op_user_id": self.mch_id,
        }

        if refund_desc:
            params["refund_desc"] = refund_desc

        # 添加额外参数
        params.update(kwargs)

        # 生成签名
        params["sign"] = self._generate_sign(params)

        try:
            client = await self._get_client()

            # 发送请求
            response = await client.post(
                "/secapi/pay/refund",
                content=self._dict_to_xml(params),
                headers={"Content-Type": "application/xml"}
            )

            response.raise_for_status()

            # 解析响应
            result = self._xml_to_dict(response.text)

            # 验证签名
            if "sign" in result and not self._verify_sign(result, result["sign"]):
                raise WeChatPaySignatureError("微信支付响应签名验证失败")

            # 检查返回状态
            if result.get("return_code") != "SUCCESS":
                error_msg = result.get("return_msg", "未知错误")
                logger.error(f"申请微信支付退款失败: {error_msg}")
                raise WeChatPayAPIError(f"申请微信支付退款失败: {error_msg}")

            if result.get("result_code") != "SUCCESS":
                error_msg = result.get("err_code_des", "未知错误")
                logger.error(f"申请微信支付退款失败: {error_msg}")
                raise WeChatPayAPIError(f"申请微信支付退款失败: {error_msg}")

            logger.info(f"申请微信支付退款成功: refund_no={refund_no}")
            return result

        except httpx.HTTPError as e:
            logger.error(f"微信支付API请求失败: {e}")
            raise WeChatPayAPIError(f"微信支付API请求失败: {str(e)}")

    # ==================== 查询退款 ====================

    async def query_refund(
        self,
        refund_no: Optional[str] = None,
        transaction_id: Optional[str] = None,
        order_no: Optional[str] = None
    ) -> Dict[str, Any]:
        """查询退款

        Args:
            refund_no: 商户退款单号
            transaction_id: 微信支付订单号
            order_no: 商户订单号

        Returns:
            Dict[str, Any]: 退款信息

        Raises:
            WeChatPayConfigError: 配置错误
            WeChatPayAPIError: API调用失败
        """
        if not refund_no and not transaction_id and not order_no:
            raise WeChatPayConfigError("退款单号、微信支付订单号和商户订单号必须提供其中一个")

        logger.info(f"查询微信支付退款: refund_no={refund_no}, transaction_id={transaction_id}, order_no={order_no}")

        # 构建请求参数
        params = {
            "appid": settings.WEWORK_CORP_ID,
            "mch_id": self.mch_id,
            "nonce_str": self._generate_nonce_str(),
        }

        if refund_no:
            params["out_refund_no"] = refund_no
        if transaction_id:
            params["transaction_id"] = transaction_id
        if order_no:
            params["out_trade_no"] = order_no

        # 生成签名
        params["sign"] = self._generate_sign(params)

        try:
            client = await self._get_client()

            # 发送请求
            response = await client.post(
                "/pay/refundquery",
                content=self._dict_to_xml(params),
                headers={"Content-Type": "application/xml"}
            )

            response.raise_for_status()

            # 解析响应
            result = self._xml_to_dict(response.text)

            # 验证签名
            if "sign" in result and not self._verify_sign(result, result["sign"]):
                raise WeChatPaySignatureError("微信支付响应签名验证失败")

            # 检查返回状态
            if result.get("return_code") != "SUCCESS":
                error_msg = result.get("return_msg", "未知错误")
                logger.error(f"查询微信支付退款失败: {error_msg}")
                raise WeChatPayAPIError(f"查询微信支付退款失败: {error_msg}")

            logger.info(f"查询微信支付退款成功: refund_no={refund_no}")
            return result

        except httpx.HTTPError as e:
            logger.error(f"微信支付API请求失败: {e}")
            raise WeChatPayAPIError(f"微信支付API请求失败: {str(e)}")

    # ==================== 回调处理 ====================

    def parse_notify(self, xml_data: str) -> Dict[str, Any]:
        """解析支付回调通知

        Args:
            xml_data: XML格式的回调数据

        Returns:
            Dict[str, Any]: 解析后的回调数据

        Raises:
            WeChatPaySignatureError: 签名验证失败
        """
        logger.info("解析微信支付回调通知")

        # 解析XML
        data = self._xml_to_dict(xml_data)

        # 验证签名
        if "sign" not in data:
            raise WeChatPaySignatureError("回调数据缺少签名")

        if not self._verify_sign(data, data["sign"]):
            raise WeChatPaySignatureError("回调数据签名验证失败")

        # 检查返回状态
        if data.get("return_code") != "SUCCESS":
            error_msg = data.get("return_msg", "未知错误")
            logger.error(f"微信支付回调失败: {error_msg}")
            raise WeChatPayAPIError(f"微信支付回调失败: {error_msg}")

        logger.info(f"解析微信支付回调成功: order_no={data.get('out_trade_no')}, trade_state={data.get('trade_state')}")
        return data

    def parse_refund_notify(self, xml_data: str) -> Dict[str, Any]:
        """解析退款回调通知

        Args:
            xml_data: XML格式的回调数据

        Returns:
            Dict[str, Any]: 解析后的回调数据

        Raises:
            WeChatPaySignatureError: 签名验证失败
        """
        logger.info("解析微信支付退款回调通知")

        # 解析XML
        data = self._xml_to_dict(xml_data)

        # 验证签名
        if "sign" not in data:
            raise WeChatPaySignatureError("退款回调数据缺少签名")

        if not self._verify_sign(data, data["sign"]):
            raise WeChatPaySignatureError("退款回调数据签名验证失败")

        # 检查返回状态
        if data.get("return_code") != "SUCCESS":
            error_msg = data.get("return_msg", "未知错误")
            logger.error(f"微信支付退款回调失败: {error_msg}")
            raise WeChatPayAPIError(f"微信支付退款回调失败: {error_msg}")

        logger.info(f"解析微信支付退款回调成功: refund_no={data.get('out_refund_no')}, refund_status={data.get('refund_status')}")
        return data

    def build_success_response(self) -> str:
        """构建支付成功响应

        Returns:
            str: XML格式的成功响应
        """
        return self._dict_to_xml({
            "return_code": "SUCCESS",
            "return_msg": "OK"
        })

    def build_fail_response(self, err_msg: str = "FAIL") -> str:
        """构建支付失败响应

        Args:
            err_msg: 错误消息

        Returns:
            str: XML格式的失败响应
        """
        return self._dict_to_xml({
            "return_code": "FAIL",
            "return_msg": err_msg
        })

    # ==================== 工具方法 ====================

    @staticmethod
    def _dict_to_xml(data: Dict[str, Any]) -> str:
        """将字典转换为XML

        Args:
            data: 字典数据

        Returns:
            str: XML字符串
        """
        root = ET.Element("xml")

        for key, value in data.items():
            elem = ET.SubElement(root, key)
            elem.text = str(value)

        return ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')

    @staticmethod
    def _xml_to_dict(xml_data: str) -> Dict[str, Any]:
        """将XML转换为字典

        Args:
            xml_data: XML字符串

        Returns:
            Dict[str, Any]: 字典数据
        """
        root = ET.fromstring(xml_data)
        return {child.tag: child.text for child in root}

    @staticmethod
    def yuan_to_fen(amount: Decimal) -> int:
        """元转分

        Args:
            amount: 金额（元）

        Returns:
            int: 金额（分）
        """
        return int(amount * 100)

    @staticmethod
    def fen_to_yuan(amount: int) -> Decimal:
        """分转元

        Args:
            amount: 金额（分）

        Returns:
            Decimal: 金额（元）
        """
        return Decimal(amount) / Decimal(100)


# 创建服务实例
wechat_pay_service = WeChatPayService()
