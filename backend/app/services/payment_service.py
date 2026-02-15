"""Payment Business Logic Service

缴费业务逻辑服务层

提供缴费管理的业务逻辑处理，包括：
- 缴费查询、创建、更新、删除
- 缴费确认（增加合同课时）
- 退款处理
"""
import logging
from datetime import datetime
from typing import List, Optional
from decimal import Decimal

from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment import Payment
from app.models.contract import Contract
from app.schemas.payment import (
    PaymentCreate,
    PaymentUpdate,
    PaymentConfirm,
    PaymentRefund,
)


logger = logging.getLogger(__name__)


class PaymentServiceError(Exception):
    """缴费服务异常基类"""
    pass


class PaymentNotFoundError(PaymentServiceError):
    """缴费不存在异常"""
    pass


class PaymentNoExistsError(PaymentServiceError):
    """缴费编号已存在异常"""
    pass


class ContractNotFoundError(PaymentServiceError):
    """合同不存在异常"""
    pass


class InvalidPaymentDataError(PaymentServiceError):
    """无效缴费数据异常"""
    pass


class InvalidPaymentStatusError(PaymentServiceError):
    """无效缴费状态异常"""
    pass


class PaymentService:
    """缴费业务服务类

    提供缴费的完整业务逻辑处理
    所有方法都是异步的，需要传入 AsyncSession
    """

    # ==================== 缴费查询服务 ====================

    @staticmethod
    async def get_all_payments(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        contract_id: Optional[int] = None,
        status: Optional[int] = None,
        payment_method: Optional[int] = None
    ) -> List[Payment]:
        """
        获取缴费列表，支持分页和筛选

        Args:
            session: 数据库会话
            skip: 跳过记录数
            limit: 返回记录数
            contract_id: 合同ID筛选
            status: 状态筛选 (1:待确认 2:已确认 3:已退款)
            payment_method: 支付方式筛选 (1:微信 2:支付宝 3:现金 4:银行卡 5:转账)

        Returns:
            List[Payment]: 缴费列表
        """
        logger.info(f"查询缴费列表: skip={skip}, limit={limit}")

        from app.crud.payment import PaymentCRUD

        payments = await PaymentCRUD.get_all(
            session=session,
            skip=skip,
            limit=limit,
            contract_id=contract_id,
            status=status,
            payment_method=payment_method
        )

        return payments

    @staticmethod
    async def get_payment_by_id(payment_id: int, session: AsyncSession) -> Payment:
        """
        根据ID获取缴费详情

        Args:
            payment_id: 缴费ID
            session: 数据库会话

        Returns:
            Payment: 缴费对象

        Raises:
            PaymentNotFoundError: 缴费不存在
        """
        logger.info(f"查询缴费详情: payment_id={payment_id}")

        from app.crud.payment import PaymentCRUD

        payment = await PaymentCRUD.get_by_id(payment_id, session)

        if not payment:
            logger.warning(f"缴费不存在: payment_id={payment_id}")
            raise PaymentNotFoundError(f"缴费不存在: {payment_id}")

        return payment

    @staticmethod
    async def get_payment_by_no(payment_no: str, session: AsyncSession) -> Payment:
        """
        根据缴费编号获取缴费

        Args:
            payment_no: 缴费编号
            session: 数据库会话

        Returns:
            Payment: 缴费对象

        Raises:
            PaymentNotFoundError: 缴费不存在
        """
        logger.info(f"查询缴费: payment_no={payment_no}")

        from app.crud.payment import PaymentCRUD

        payment = await PaymentCRUD.get_by_no(payment_no, session)

        if not payment:
            logger.warning(f"缴费不存在: payment_no={payment_no}")
            raise PaymentNotFoundError(f"缴费不存在: {payment_no}")

        return payment

    @staticmethod
    async def count_payments(
        session: AsyncSession,
        contract_id: Optional[int] = None,
        status: Optional[int] = None,
        payment_method: Optional[int] = None
    ) -> int:
        """
        统计缴费数量

        Args:
            session: 数据库会话
            contract_id: 合同ID筛选
            status: 状态筛选
            payment_method: 支付方式筛选

        Returns:
            int: 缴费总数
        """
        from app.crud.payment import PaymentCRUD

        count = await PaymentCRUD.count(
            session=session,
            contract_id=contract_id,
            status=status,
            payment_method=payment_method
        )

        return count

    # ==================== 缴费管理服务 ====================

    @staticmethod
    async def create_payment(
        payment_data: PaymentCreate,
        created_by: Optional[int],
        session: AsyncSession
    ) -> Payment:
        """
        创建缴费

        Args:
            payment_data: 缴费创建数据
            created_by: 创建人ID
            session: 数据库会话

        Returns:
            Payment: 创建的缴费对象

        Raises:
            ContractNotFoundError: 合同不存在
            PaymentNoExistsError: 缴费编号已存在
            InvalidPaymentDataError: 数据验证失败
        """
        logger.info(f"创建缴费: payment_no={payment_data.payment_no}")

        from app.crud.payment import PaymentCRUD

        # 验证合同存在
        contract = await session.get(Contract, payment_data.contract_id)
        if not contract:
            logger.warning(f"合同不存在: contract_id={payment_data.contract_id}")
            raise ContractNotFoundError(f"合同不存在: {payment_data.contract_id}")

        # 检查缴费编号是否已存在
        if await PaymentCRUD.check_exists_by_no(payment_data.payment_no, session):
            raise PaymentNoExistsError(f"缴费编号已存在: {payment_data.payment_no}")

        # 创建缴费
        try:
            payment = Payment(
                payment_no=payment_data.payment_no,
                contract_id=payment_data.contract_id,
                amount=payment_data.amount,
                hours=payment_data.hours,
                payment_method=payment_data.payment_method,
                payment_channel=payment_data.payment_channel,
                transaction_id=payment_data.transaction_id,
                trade_no=payment_data.trade_no,
                payment_time=payment_data.payment_time,
                operator_id=payment_data.operator_id,
                status=1,  # 默认待确认
                remark=payment_data.remark,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            return await PaymentCRUD.create(payment, session)

        except IntegrityError as e:
            logger.error(f"创建缴费失败: {e}")
            await session.rollback()
            raise PaymentServiceError(f"创建缴费失败: {str(e)}")

    @staticmethod
    async def update_payment(
        payment_id: int,
        payment_data: PaymentUpdate,
        session: AsyncSession
    ) -> Payment:
        """
        更新缴费

        Args:
            payment_id: 缴费ID
            payment_data: 缴费更新数据
            session: 数据库会话

        Returns:
            Payment: 更新后的缴费对象

        Raises:
            PaymentNotFoundError: 缴费不存在
            InvalidPaymentDataError: 数据验证失败
        """
        logger.info(f"更新缴费: payment_id={payment_id}")

        # 获取缴费
        payment = await PaymentService.get_payment_by_id(payment_id, session)

        # 更新字段
        if payment_data.amount is not None:
            payment.amount = payment_data.amount
        if payment_data.hours is not None:
            payment.hours = payment_data.hours
        if payment_data.payment_method is not None:
            payment.payment_method = payment_data.payment_method
        if payment_data.payment_channel is not None:
            payment.payment_channel = payment_data.payment_channel
        if payment_data.transaction_id is not None:
            payment.transaction_id = payment_data.transaction_id
        if payment_data.trade_no is not None:
            payment.trade_no = payment_data.trade_no
        if payment_data.payment_time is not None:
            payment.payment_time = payment_data.payment_time
        if payment_data.operator_id is not None:
            payment.operator_id = payment_data.operator_id
        if payment_data.status is not None:
            payment.status = payment_data.status
        if payment_data.remark is not None:
            payment.remark = payment_data.remark

        payment.updated_at = datetime.now()

        from app.crud.payment import PaymentCRUD

        try:
            return await PaymentCRUD.update(payment, session)
        except IntegrityError as e:
            logger.error(f"更新缴费失败: {e}")
            await session.rollback()
            raise PaymentServiceError(f"更新缴费失败: {str(e)}")

    @staticmethod
    async def delete_payment(payment_id: int, session: AsyncSession) -> None:
        """
        删除缴费

        Args:
            payment_id: 缴费ID
            session: 数据库会话

        Raises:
            PaymentNotFoundError: 缴费不存在
            PaymentServiceError: 删除失败
        """
        logger.info(f"删除缴费: payment_id={payment_id}")

        # 获取缴费
        payment = await PaymentService.get_payment_by_id(payment_id, session)

        # 检查是否可以删除（只有待确认状态可以删除）
        if payment.status != 1:
            raise InvalidPaymentStatusError(
                f"只有待确认状态的缴费可以删除: 当前状态={payment.status}"
            )

        from app.crud.payment import PaymentCRUD

        try:
            await PaymentCRUD.delete(payment, session)
        except IntegrityError as e:
            logger.error(f"删除缴费失败: {e}")
            await session.rollback()
            raise PaymentServiceError(f"删除缴费失败，可能存在关联数据")

    # ==================== 缴费确认服务 ====================

    @staticmethod
    async def confirm_payment(
        payment_id: int,
        confirm_data: PaymentConfirm,
        session: AsyncSession
    ) -> Payment:
        """
        确认缴费

        确认后自动增加合同剩余课时

        Args:
            payment_id: 缴费ID
            confirm_data: 确认数据
            session: 数据库会话

        Returns:
            Payment: 更新后的缴费对象

        Raises:
            PaymentNotFoundError: 缴费不存在
            InvalidPaymentStatusError: 缴费状态不允许确认
            ContractNotFoundError: 合同不存在
        """
        logger.info(f"确认缴费: payment_id={payment_id}, hours={confirm_data.hours}")

        # 获取缴费
        payment = await PaymentService.get_payment_by_id(payment_id, session)

        # 检查缴费状态
        if payment.status != 1:
            raise InvalidPaymentStatusError(
                f"只有待确认状态的缴费可以确认: 当前状态={payment.status}"
            )

        # 获取合同
        contract = await session.get(Contract, payment.contract_id)
        if not contract:
            raise ContractNotFoundError(f"合同不存在: {payment.contract_id}")

        # 检查合同状态
        if contract.status not in [1, 2]:  # 生效或完结
            raise InvalidPaymentStatusError(
                f"合同状态不允许确认缴费: 当前状态={contract.status}"
            )

        # 更新缴费状态
        payment.status = 2  # 已确认
        payment.hours = confirm_data.hours
        if confirm_data.remark:
            payment.remark = confirm_data.remark
        payment.updated_at = datetime.now()

        # 增加合同剩余课时
        contract.remaining_hours += confirm_data.hours
        contract.total_hours += confirm_data.hours
        contract.received_amount += payment.amount
        contract.updated_at = datetime.now()

        from app.crud.payment import PaymentCRUD
        from app.crud.contract import ContractCRUD

        try:
            # 更新缴费和合同
            await PaymentCRUD.update(payment, session)
            await ContractCRUD.update(contract, session)

            logger.info(f"缴费确认成功: payment_id={payment_id}, 增加课时={confirm_data.hours}")
            return payment

        except IntegrityError as e:
            logger.error(f"确认缴费失败: {e}")
            await session.rollback()
            raise PaymentServiceError(f"确认缴费失败: {str(e)}")

    # ==================== 退款服务 ====================

    @staticmethod
    async def refund_payment(
        payment_id: int,
        refund_data: PaymentRefund,
        session: AsyncSession
    ) -> Payment:
        """
        退款

        Args:
            payment_id: 缴费ID
            refund_data: 退款数据
            session: 数据库会话

        Returns:
            Payment: 更新后的缴费对象

        Raises:
            PaymentNotFoundError: 缴费不存在
            InvalidPaymentStatusError: 缴费状态不允许退款
            ContractNotFoundError: 合同不存在
            InvalidPaymentDataError: 退款数据验证失败
        """
        logger.info(f"退款: payment_id={payment_id}, refund_amount={refund_data.refund_amount}")

        # 获取缴费
        payment = await PaymentService.get_payment_by_id(payment_id, session)

        # 检查缴费状态
        if payment.status != 2:
            raise InvalidPaymentStatusError(
                f"只有已确认状态的缴费可以退款: 当前状态={payment.status}"
            )

        # 检查退款金额
        if refund_data.refund_amount > payment.amount:
            raise InvalidPaymentDataError(
                f"退款金额不能超过缴费金额: 缴费金额={payment.amount}, 退款金额={refund_data.refund_amount}"
            )

        # 获取合同
        contract = await session.get(Contract, payment.contract_id)
        if not contract:
            raise ContractNotFoundError(f"合同不存在: {payment.contract_id}")

        # 检查退款课时
        if refund_data.refund_hours is not None:
            if refund_data.refund_hours > contract.remaining_hours:
                raise InvalidPaymentDataError(
                    f"退款课时不能超过合同剩余课时: 剩余课时={contract.remaining_hours}, 退款课时={refund_data.refund_hours}"
                )

        # 更新缴费状态
        payment.status = 3  # 已退款
        payment.updated_at = datetime.now()

        # 扣减合同课时和金额
        if refund_data.refund_hours is not None:
            contract.remaining_hours -= refund_data.refund_hours
            contract.total_hours -= refund_data.refund_hours
        contract.received_amount -= refund_data.refund_amount
        contract.updated_at = datetime.now()

        from app.crud.payment import PaymentCRUD
        from app.crud.contract import ContractCRUD

        try:
            # 更新缴费和合同
            await PaymentCRUD.update(payment, session)
            await ContractCRUD.update(contract, session)

            logger.info(f"退款成功: payment_id={payment_id}")
            return payment

        except IntegrityError as e:
            logger.error(f"退款失败: {e}")
            await session.rollback()
            raise PaymentServiceError(f"退款失败: {str(e)}")


# 创建服务实例
payment_service = PaymentService()
