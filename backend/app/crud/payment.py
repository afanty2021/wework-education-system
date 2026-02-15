"""Payment CRUD Operations

缴费数据访问层

提供缴费的基础 CRUD 操作
"""
import logging
from typing import List, Optional

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment import Payment


logger = logging.getLogger(__name__)


class PaymentCRUD:
    """缴费 CRUD 操作类

    提供缴费的基础数据访问操作
    所有方法都是异步的，需要传入 AsyncSession
    """

    @staticmethod
    async def get_all(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        contract_id: Optional[int] = None,
        status: Optional[int] = None,
        payment_method: Optional[int] = None
    ) -> List[Payment]:
        """
        获取缴费列表

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

        query = select(Payment)

        # 应用筛选条件
        conditions = []
        if contract_id:
            conditions.append(Payment.contract_id == contract_id)
        if status is not None:
            conditions.append(Payment.status == status)
        if payment_method is not None:
            conditions.append(Payment.payment_method == payment_method)

        if conditions:
            query = query.where(and_(*conditions))

        # 排序和分页
        query = query.order_by(Payment.created_at.desc()).offset(skip).limit(limit)

        result = await session.execute(query)
        payments = result.scalars().all()

        logger.info(f"查询到 {len(payments)} 个缴费记录")
        return payments

    @staticmethod
    async def get_by_id(payment_id: int, session: AsyncSession) -> Optional[Payment]:
        """
        根据ID获取缴费

        Args:
            payment_id: 缴费ID
            session: 数据库会话

        Returns:
            Optional[Payment]: 缴费对象，不存在返回 None
        """
        logger.info(f"查询缴费: payment_id={payment_id}")

        payment = await session.get(Payment, payment_id)

        if payment:
            logger.info(f"查询到缴费: {payment.payment_no}")
        else:
            logger.warning(f"缴费不存在: payment_id={payment_id}")

        return payment

    @staticmethod
    async def get_by_no(payment_no: str, session: AsyncSession) -> Optional[Payment]:
        """
        根据缴费编号获取缴费

        Args:
            payment_no: 缴费编号
            session: 数据库会话

        Returns:
            Optional[Payment]: 缴费对象，不存在返回 None
        """
        logger.info(f"查询缴费: payment_no={payment_no}")

        result = await session.execute(
            select(Payment).where(Payment.payment_no == payment_no)
        )
        payment = result.scalar_one_or_none()

        if payment:
            logger.info(f"查询到缴费: {payment.payment_no}")
        else:
            logger.warning(f"缴费不存在: payment_no={payment_no}")

        return payment

    @staticmethod
    async def create(payment: Payment, session: AsyncSession) -> Payment:
        """
        创建缴费

        Args:
            payment: 缴费对象
            session: 数据库会话

        Returns:
            Payment: 创建的缴费对象
        """
        logger.info(f"创建缴费: payment_no={payment.payment_no}")

        session.add(payment)
        await session.commit()
        await session.refresh(payment)

        logger.info(f"缴费创建成功: id={payment.id}, payment_no={payment.payment_no}")
        return payment

    @staticmethod
    async def update(payment: Payment, session: AsyncSession) -> Payment:
        """
        更新缴费

        Args:
            payment: 缴费对象
            session: 数据库会话

        Returns:
            Payment: 更新后的缴费对象
        """
        logger.info(f"更新缴费: id={payment.id}")

        session.add(payment)
        await session.commit()
        await session.refresh(payment)

        logger.info(f"缴费更新成功: id={payment.id}")
        return payment

    @staticmethod
    async def delete(payment: Payment, session: AsyncSession) -> None:
        """
        删除缴费

        Args:
            payment: 缴费对象
            session: 数据库会话
        """
        logger.info(f"删除缴费: id={payment.id}")

        await session.delete(payment)
        await session.commit()

        logger.info(f"缴费删除成功: id={payment.id}")

    @staticmethod
    async def count(
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
        query = select(func.count(Payment.id))

        conditions = []
        if contract_id:
            conditions.append(Payment.contract_id == contract_id)
        if status is not None:
            conditions.append(Payment.status == status)
        if payment_method is not None:
            conditions.append(Payment.payment_method == payment_method)

        if conditions:
            query = query.where(and_(*conditions))

        result = await session.execute(query)
        count = result.scalar()

        return count

    @staticmethod
    async def check_exists_by_no(payment_no: str, session: AsyncSession) -> bool:
        """
        检查缴费编号是否存在

        Args:
            payment_no: 缴费编号
            session: 数据库会话

        Returns:
            bool: 存在返回 True，否则返回 False
        """
        result = await session.execute(
            select(func.count(Payment.id)).where(Payment.payment_no == payment_no)
        )
        count = result.scalar()
        return count > 0

    @staticmethod
    async def get_payments_by_contract(
        contract_id: int,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[Payment]:
        """
        获取合同的所有缴费记录

        Args:
            contract_id: 合同ID
            session: 数据库会话
            skip: 跳过记录数
            limit: 返回记录数

        Returns:
            List[Payment]: 缴费列表
        """
        query = select(Payment).where(
            Payment.contract_id == contract_id
        ).order_by(Payment.created_at.desc()).offset(skip).limit(limit)

        result = await session.execute(query)
        payments = result.scalars().all()

        logger.info(f"查询到合同 {contract_id} 的 {len(payments)} 个缴费记录")
        return payments
