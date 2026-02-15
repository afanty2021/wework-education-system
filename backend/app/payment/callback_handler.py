"""
支付回调处理器

统一处理微信支付和支付宝支付的回调通知，包括：
- 回调数据验证（签名、金额、防重放）
- 支付成功后自动更新缴费和合同状态
- 完整的异常处理和日志记录
- 防重放攻击保护
"""
import hashlib
import json
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contract import Contract
from app.models.payment import Payment
from app.payment.alipay import AliPayService
from app.payment.wechat import WeChatPayService
from app.schemas.payment import PaymentConfirm, PaymentUpdate

logger = logging.getLogger(__name__)


class PaymentCallbackError(Exception):
    """支付回调处理异常基类"""
    pass


class SignatureVerificationError(PaymentCallbackError):
    """签名验证失败"""
    pass


class AmountMismatchError(PaymentCallbackError):
    """金额不匹配"""
    pass


class PaymentNotFoundError(PaymentCallbackError):
    """缴费不存在"""
    pass


class ContractNotFoundError(PaymentCallbackError):
    """合同不存在"""
    pass


class DuplicateCallbackError(PaymentCallbackError):
    """重复回调通知"""
    pass


class InvalidPaymentStatusError(PaymentCallbackError):
    """无效的缴费状态"""
    pass


class PaymentCallbackHandler:
    """支付回调处理器类

    统一处理微信支付和支付宝支付的回调通知
    提供完整的验证、更新和日志记录功能
    """

    # 回调缓存时间（秒），防止重复处理
    CALLBACK_CACHE_TTL = 300  # 5分钟

    def __init__(self, session: AsyncSession):
        """初始化回调处理器

        Args:
            session: 数据库会话
        """
        self.session = session
        self._callback_cache: Dict[str, datetime] = {}

    def _is_duplicate_callback(
        self,
        order_no: str,
        notification_id: str
    ) -> bool:
        """检查是否为重复回调通知

        Args:
            order_no: 商户订单号
            notification_id: 通知ID（微信：transaction_id，支付宝：trade_no）

        Returns:
            bool: True表示重复回调，False表示新回调
        """
        cache_key = f"{order_no}:{notification_id}"
        current_time = datetime.now()

        # 清理过期缓存
        expired_keys = [
            key for key, time in self._callback_cache.items()
            if current_time - time > timedelta(seconds=self.CALLBACK_CACHE_TTL)
        ]
        for key in expired_keys:
            del self._callback_cache[key]

        # 检查是否重复
        if cache_key in self._callback_cache:
            logger.warning(f"检测到重复回调: {cache_key}")
            return True

        # 记录回调
        self._callback_cache[cache_key] = current_time
        return False

    async def _get_payment_by_no(
        self,
        payment_no: str
    ) -> Payment:
        """根据缴费编号获取缴费

        Args:
            payment_no: 缴费编号

        Returns:
            Payment: 缴费对象

        Raises:
            PaymentNotFoundError: 缴费不存在
        """
        from app.crud.payment import PaymentCRUD

        payment = await PaymentCRUD.get_by_no(payment_no, self.session)

        if not payment:
            raise PaymentNotFoundError(f"缴费不存在: {payment_no}")

        return payment

    async def _get_contract_by_id(
        self,
        contract_id: int
    ) -> Contract:
        """根据合同ID获取合同

        Args:
            contract_id: 合同ID

        Returns:
            Contract: 合同对象

        Raises:
            ContractNotFoundError: 合同不存在
        """
        contract = await self.session.get(Contract, contract_id)

        if not contract:
            raise ContractNotFoundError(f"合同不存在: {contract_id}")

        return contract

    def _verify_wechat_signature(
        self,
        wechat_service: WeChatPayService,
        notify_data: Dict[str, Any]
    ) -> None:
        """验证微信支付回调签名

        Args:
            wechat_service: 微信支付服务
            notify_data: 回调数据

        Raises:
            SignatureVerificationError: 签名验证失败
        """
        if "sign" not in notify_data:
            raise SignatureVerificationError("回调数据缺少签名")

        if not wechat_service._verify_sign(notify_data, notify_data["sign"]):
            raise SignatureVerificationError("回调数据签名验证失败")

    def _verify_alipay_signature(
        self,
        alipay_service: AliPayService,
        notify_data: Dict[str, Any]
    ) -> None:
        """验证支付宝回调签名

        Args:
            alipay_service: 支付宝服务
            notify_data: 回调数据

        Raises:
            SignatureVerificationError: 签名验证失败
        """
        if "sign" not in notify_data:
            raise SignatureVerificationError("回调数据缺少签名")

        if not alipay_service._verify_sign(notify_data, notify_data["sign"]):
            raise SignatureVerificationError("回调数据签名验证失败")

    def _verify_amount(
        self,
        payment: Payment,
        callback_amount: Any,
        amount_type: str = "分"
    ) -> None:
        """验证支付金额

        Args:
            payment: 缴费对象
            callback_amount: 回调金额
            amount_type: 金额类型（"分"或"元"）

        Raises:
            AmountMismatchError: 金额不匹配
        """
        # 转换回调金额为Decimal
        try:
            if amount_type == "分":
                callback_amount_decimal = Decimal(int(callback_amount)) / Decimal(100)
            else:  # "元"
                callback_amount_decimal = Decimal(str(callback_amount))
        except (ValueError, TypeError) as e:
            logger.error(f"回调金额格式错误: {callback_amount}, {e}")
            raise AmountMismatchError(f"回调金额格式错误: {callback_amount}")

        # 比较金额（允许0.01元的误差）
        amount_diff = abs(callback_amount_decimal - payment.amount)
        if amount_diff > Decimal("0.01"):
            logger.error(
                f"支付金额不匹配: 订单金额={payment.amount}, "
                f"回调金额={callback_amount_decimal}, 差异={amount_diff}"
            )
            raise AmountMismatchError(
                f"支付金额不匹配: 订单金额={payment.amount}, "
                f"回调金额={callback_amount_decimal}"
            )

    async def _update_payment_status(
        self,
        payment: Payment,
        transaction_id: str,
        payment_time: Optional[datetime],
        status: int
    ) -> Payment:
        """更新缴费状态

        Args:
            payment: 缴费对象
            transaction_id: 第三方交易号
            payment_time: 支付时间
            status: 缴费状态

        Returns:
            Payment: 更新后的缴费对象
        """
        from app.crud.payment import PaymentCRUD

        # 更新缴费信息
        payment.transaction_id = transaction_id
        if payment_time:
            payment.payment_time = payment_time
        payment.status = status
        payment.updated_at = datetime.now()

        # 保存到数据库
        payment = await PaymentCRUD.update(payment, self.session)

        logger.info(
            f"缴费状态更新成功: id={payment.id}, payment_no={payment.payment_no}, "
            f"status={status}"
        )

        return payment

    async def _confirm_payment(
        self,
        payment: Payment,
        amount: Decimal
    ) -> Payment:
        """确认缴费并更新合同

        Args:
            payment: 缴费对象
            amount: 支付金额（元）

        Returns:
            Payment: 确认后的缴费对象
        """
        from app.crud.contract import ContractCRUD

        # 获取合同
        contract = await self._get_contract_by_id(payment.contract_id)

        # 计算课时
        hours = None
        if contract.unit_price and contract.unit_price > 0:
            hours = amount / contract.unit_price
        else:
            logger.warning(
                f"合同单价未设置或为零，无法自动计算课时: contract_id={contract.id}"
            )

        # 检查缴费状态
        if payment.status != 1:
            raise InvalidPaymentStatusError(
                f"只有待确认状态的缴费可以确认: 当前状态={payment.status}"
            )

        # 检查合同状态
        if contract.status not in [1, 2]:  # 生效或完结
            raise InvalidPaymentStatusError(
                f"合同状态不允许确认缴费: 当前状态={contract.status}"
            )

        # 更新缴费状态
        payment.status = 2  # 已确认
        if hours:
            payment.hours = hours
        payment.updated_at = datetime.now()

        # 更新合同
        if hours:
            contract.remaining_hours += hours
            contract.total_hours += hours
        contract.received_amount += payment.amount
        contract.updated_at = datetime.now()

        # 保存到数据库（使用事务）
        try:
            await PaymentCRUD.update(payment, self.session)
            await ContractCRUD.update(contract, self.session)

            logger.info(
                f"缴费确认成功: payment_id={payment.id}, hours={hours}, "
                f"contract_remaining_hours={contract.remaining_hours}"
            )

            return payment

        except IntegrityError as e:
            logger.error(f"确认缴费失败: {e}")
            await self.session.rollback()
            raise PaymentCallbackError(f"确认缴费失败: {str(e)}")

    async def handle_wechat_callback(
        self,
        notify_data: Dict[str, Any],
        wechat_service: WeChatPayService
    ) -> str:
        """处理微信支付回调

        Args:
            notify_data: 回调数据
            wechat_service: 微信支付服务

        Returns:
            str: 成功响应（XML格式）

        Raises:
            PaymentCallbackError: 回调处理失败
        """
        # 1. 验证签名
        self._verify_wechat_signature(wechat_service, notify_data)

        # 2. 提取回调数据
        order_no = notify_data.get("out_trade_no")
        transaction_id = notify_data.get("transaction_id")
        trade_state = notify_data.get("trade_state")
        total_fee = notify_data.get("total_fee")  # 单位：分
        time_end = notify_data.get("time_end")

        if not order_no:
            logger.error("微信支付回调缺少订单号")
            return wechat_service.build_fail_response("缺少订单号")

        # 3. 检查是否重复回调
        if self._is_duplicate_callback(order_no, transaction_id or ""):
            # 重复回调直接返回成功
            return wechat_service.build_success_response()

        logger.info(
            f"处理微信支付回调: order_no={order_no}, transaction_id={transaction_id}, "
            f"trade_state={trade_state}"
        )

        try:
            # 4. 获取缴费
            payment = await self._get_payment_by_no(order_no)

            # 5. 验证金额
            if total_fee and payment.amount:
                self._verify_amount(payment, total_fee, "分")

            # 6. 解析支付时间
            payment_time = None
            if time_end:
                try:
                    payment_time = datetime.strptime(time_end, "%Y%m%d%H%M%S")
                except ValueError as e:
                    logger.error(f"支付时间解析失败: {time_end}, {e}")

            # 7. 判断交易状态
            if trade_state == WeChatPayService.TRADE_STATE_SUCCESS:
                # 支付成功，更新缴费状态
                payment = await self._update_payment_status(
                    payment=payment,
                    transaction_id=transaction_id,
                    payment_time=payment_time,
                    status=2  # 已确认
                )

                # 自动确认缴费
                try:
                    amount = Decimal(int(total_fee)) / Decimal(100) if total_fee else payment.amount
                    payment = await self._confirm_payment(payment, amount)
                except Exception as e:
                    logger.error(f"自动确认缴费失败: {e}")
                    # 继续返回成功（避免重复通知）

            elif trade_state == WeChatPayService.TRADE_STATE_REFUND:
                # 转入退款
                payment.status = 3  # 已退款
                payment.updated_at = datetime.now()

                from app.crud.payment import PaymentCRUD
                await PaymentCRUD.update(payment, self.session)

                logger.info(f"缴费转入退款: payment_id={payment.id}")

            elif trade_state in [
                WeChatPayService.TRADE_STATE_NOTPAY,
                WeChatPayService.TRADE_STATE_CLOSED,
                WeChatPayService.TRADE_STATE_REVOKED,
                WeChatPayService.TRADE_STATE_PAYERROR
            ]:
                # 其他状态不处理
                logger.info(f"微信支付状态无需处理: {trade_state}")

            else:
                logger.warning(f"未知的微信支付状态: {trade_state}")

            # 8. 返回成功响应
            return wechat_service.build_success_response()

        except PaymentCallbackError as e:
            logger.error(f"处理微信支付回调失败: {e}")
            return wechat_service.build_fail_response(str(e))

        except Exception as e:
            logger.error(f"处理微信支付回调失败: {e}", exc_info=True)
            return wechat_service.build_fail_response("处理失败")

    async def handle_alipay_callback(
        self,
        notify_data: Dict[str, Any],
        alipay_service: AliPayService
    ) -> str:
        """处理支付宝回调

        Args:
            notify_data: 回调数据
            alipay_service: 支付宝服务

        Returns:
            str: 成功响应（文本格式）

        Raises:
            PaymentCallbackError: 回调处理失败
        """
        # 1. 验证签名
        self._verify_alipay_signature(alipay_service, notify_data)

        # 2. 提取回调数据
        order_no = notify_data.get("out_trade_no")
        trade_no = notify_data.get("trade_no")
        trade_status = notify_data.get("trade_status")
        total_amount = notify_data.get("total_amount")  # 单位：元
        gmt_payment = notify_data.get("gmt_payment")

        if not order_no:
            logger.error("支付宝回调缺少订单号")
            return alipay_service.build_fail_response()

        # 3. 检查是否重复回调
        if self._is_duplicate_callback(order_no, trade_no or ""):
            # 重复回调直接返回成功
            return alipay_service.build_success_response()

        logger.info(
            f"处理支付宝回调: order_no={order_no}, trade_no={trade_no}, "
            f"trade_status={trade_status}"
        )

        try:
            # 4. 获取缴费
            payment = await self._get_payment_by_no(order_no)

            # 5. 验证金额
            if total_amount and payment.amount:
                self._verify_amount(payment, total_amount, "元")

            # 6. 解析支付时间
            payment_time = None
            if gmt_payment:
                try:
                    # 支付宝时间格式：yyyy-MM-dd HH:mm:ss
                    payment_time = datetime.strptime(gmt_payment, "%Y-%m-%d %H:%M:%S")
                except ValueError as e:
                    logger.error(f"支付时间解析失败: {gmt_payment}, {e}")

            # 7. 判断交易状态
            if trade_status == AliPayService.TRADE_STATUS_TRADE_SUCCESS:
                # 支付成功，更新缴费状态
                payment = await self._update_payment_status(
                    payment=payment,
                    transaction_id=trade_no,
                    payment_time=payment_time,
                    status=2  # 已确认
                )

                # 自动确认缴费
                try:
                    amount = Decimal(str(total_amount)) if total_amount else payment.amount
                    payment = await self._confirm_payment(payment, amount)
                except Exception as e:
                    logger.error(f"自动确认缴费失败: {e}")
                    # 继续返回成功（避免重复通知）

            elif trade_status == AliPayService.TRADE_STATUS_TRADE_FINISHED:
                # 交易结束（不可退款）
                payment.status = 2  # 已确认
                payment.updated_at = datetime.now()

                from app.crud.payment import PaymentCRUD
                await PaymentCRUD.update(payment, self.session)

                logger.info(f"缴费交易结束: payment_id={payment.id}")

            elif trade_status == AliPayService.TRADE_STATUS_TRADE_CLOSED:
                # 交易关闭
                logger.info(f"缴费交易关闭: payment_id={payment.id}")

            elif trade_status == AliPayService.TRADE_STATUS_WAIT_BUYER_PAY:
                # 等待买家付款
                logger.info(f"缴费等待付款: payment_id={payment.id}")

            else:
                logger.warning(f"未知的支付宝交易状态: {trade_status}")

            # 8. 返回成功响应
            return alipay_service.build_success_response()

        except PaymentCallbackError as e:
            logger.error(f"处理支付宝回调失败: {e}")
            return alipay_service.build_fail_response()

        except Exception as e:
            logger.error(f"处理支付宝回调失败: {e}", exc_info=True)
            return alipay_service.build_fail_response()

    def clear_callback_cache(self) -> None:
        """清理回调缓存

        在测试环境中使用，清理内存中的回调缓存
        """
        self._callback_cache.clear()
        logger.info("回调缓存已清理")


# 便捷函数


async def handle_payment_callback(
    payment_method: int,
    notify_data: Dict[str, Any],
    session: AsyncSession,
    wechat_service: Optional[WeChatPayService] = None,
    alipay_service: Optional[AliPayService] = None
) -> str:
    """处理支付回调的便捷函数

    Args:
        payment_method: 支付方式（1:微信 2:支付宝）
        notify_data: 回调数据
        session: 数据库会话
        wechat_service: 微信支付服务（微信支付必填）
        alipay_service: 支付宝服务（支付宝必填）

    Returns:
        str: 成功响应

    Raises:
        ValueError: 参数错误
    """
    handler = PaymentCallbackHandler(session)

    if payment_method == 1:  # 微信支付
        if not wechat_service:
            raise ValueError("微信支付回调需要提供wechat_service")
        return await handler.handle_wechat_callback(notify_data, wechat_service)

    elif payment_method == 2:  # 支付宝
        if not alipay_service:
            raise ValueError("支付宝回调需要提供alipay_service")
        return await handler.handle_alipay_callback(notify_data, alipay_service)

    else:
        raise ValueError(f"不支持的支付方式: {payment_method}")
