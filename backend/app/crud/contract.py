"""Contract CRUD Operations

合同数据访问层

提供合同的基础 CRUD 操作
"""
import logging
from typing import List, Optional
from decimal import Decimal

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contract import Contract


logger = logging.getLogger(__name__)


class ContractCRUD:
    """合同 CRUD 操作类

    提供合同的基础数据访问操作
    所有方法都是异步的，需要传入 AsyncSession
    """

    @staticmethod
    async def get_all(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        student_id: Optional[int] = None,
        course_id: Optional[int] = None,
        status: Optional[int] = None
    ) -> List[Contract]:
        """
        获取合同列表

        Args:
            session: 数据库会话
            skip: 跳过记录数
            limit: 返回记录数
            student_id: 学员ID筛选
            course_id: 课程ID筛选
            status: 状态筛选 (1:生效 2:完结 3:退费 4:过期)

        Returns:
            List[Contract]: 合同列表
        """
        logger.info(f"查询合同列表: skip={skip}, limit={limit}")

        query = select(Contract)

        # 应用筛选条件
        conditions = []
        if student_id:
            conditions.append(Contract.student_id == student_id)
        if course_id:
            conditions.append(Contract.course_id == course_id)
        if status is not None:
            conditions.append(Contract.status == status)

        if conditions:
            query = query.where(and_(*conditions))

        # 排序和分页
        query = query.order_by(Contract.created_at.desc()).offset(skip).limit(limit)

        result = await session.execute(query)
        contracts = result.scalars().all()

        logger.info(f"查询到 {len(contracts)} 个合同")
        return contracts

    @staticmethod
    async def get_by_id(contract_id: int, session: AsyncSession) -> Optional[Contract]:
        """
        根据ID获取合同

        Args:
            contract_id: 合同ID
            session: 数据库会话

        Returns:
            Optional[Contract]: 合同对象，不存在返回 None
        """
        logger.info(f"查询合同: contract_id={contract_id}")

        contract = await session.get(Contract, contract_id)

        if contract:
            logger.info(f"查询到合同: {contract.contract_no}")
        else:
            logger.warning(f"合同不存在: contract_id={contract_id}")

        return contract

    @staticmethod
    async def get_by_no(contract_no: str, session: AsyncSession) -> Optional[Contract]:
        """
        根据合同编号获取合同

        Args:
            contract_no: 合同编号
            session: 数据库会话

        Returns:
            Optional[Contract]: 合同对象，不存在返回 None
        """
        logger.info(f"查询合同: contract_no={contract_no}")

        result = await session.execute(
            select(Contract).where(Contract.contract_no == contract_no)
        )
        contract = result.scalar_one_or_none()

        if contract:
            logger.info(f"查询到合同: {contract.contract_no}")
        else:
            logger.warning(f"合同不存在: contract_no={contract_no}")

        return contract

    @staticmethod
    async def create(contract: Contract, session: AsyncSession) -> Contract:
        """
        创建合同

        Args:
            contract: 合同对象
            session: 数据库会话

        Returns:
            Contract: 创建的合同对象
        """
        logger.info(f"创建合同: contract_no={contract.contract_no}")

        session.add(contract)
        await session.commit()
        await session.refresh(contract)

        logger.info(f"合同创建成功: id={contract.id}, contract_no={contract.contract_no}")
        return contract

    @staticmethod
    async def update(contract: Contract, session: AsyncSession) -> Contract:
        """
        更新合同

        Args:
            contract: 合同对象
            session: 数据库会话

        Returns:
            Contract: 更新后的合同对象
        """
        logger.info(f"更新合同: id={contract.id}")

        session.add(contract)
        await session.commit()
        await session.refresh(contract)

        logger.info(f"合同更新成功: id={contract.id}")
        return contract

    @staticmethod
    async def delete(contract: Contract, session: AsyncSession) -> None:
        """
        删除合同

        Args:
            contract: 合同对象
            session: 数据库会话
        """
        logger.info(f"删除合同: id={contract.id}")

        await session.delete(contract)
        await session.commit()

        logger.info(f"合同删除成功: id={contract.id}")

    @staticmethod
    async def count(
        session: AsyncSession,
        student_id: Optional[int] = None,
        course_id: Optional[int] = None,
        status: Optional[int] = None
    ) -> int:
        """
        统计合同数量

        Args:
            session: 数据库会话
            student_id: 学员ID筛选
            course_id: 课程ID筛选
            status: 状态筛选

        Returns:
            int: 合同总数
        """
        query = select(func.count(Contract.id))

        conditions = []
        if student_id:
            conditions.append(Contract.student_id == student_id)
        if course_id:
            conditions.append(Contract.course_id == course_id)
        if status is not None:
            conditions.append(Contract.status == status)

        if conditions:
            query = query.where(and_(*conditions))

        result = await session.execute(query)
        count = result.scalar()

        return count

    @staticmethod
    async def check_exists_by_no(contract_no: str, session: AsyncSession) -> bool:
        """
        检查合同编号是否存在

        Args:
            contract_no: 合同编号
            session: 数据库会话

        Returns:
            bool: 存在返回 True，否则返回 False
        """
        result = await session.execute(
            select(func.count(Contract.id)).where(Contract.contract_no == contract_no)
        )
        count = result.scalar()
        return count > 0

    @staticmethod
    async def get_expiring_contracts(
        session: AsyncSession,
        days: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Contract]:
        """
        获取即将到期的合同

        Args:
            session: 数据库会话
            days: 预警天数
            skip: 跳过记录数
            limit: 返回记录数

        Returns:
            List[Contract]: 即将到期的合同列表
        """
        from datetime import timedelta, date

        warning_date = date.today() + timedelta(days=days)

        query = select(Contract).where(
            and_(
                Contract.status == 1,  # 生效状态
                Contract.end_date.isnot(None),
                Contract.end_date <= warning_date
            )
        ).order_by(Contract.end_date.asc()).offset(skip).limit(limit)

        result = await session.execute(query)
        contracts = result.scalars().all()

        logger.info(f"查询到 {len(contracts)} 个即将到期的合同")
        return contracts
