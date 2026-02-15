"""Contract Business Logic Service

合同业务逻辑服务层

提供合同管理的业务逻辑处理，包括：
- 合同查询、创建、更新、删除
- 课时管理（扣减、追加）
- 到期检查
- 金额计算
"""
import logging
from datetime import datetime, date, timedelta
from typing import List, Optional
from decimal import Decimal, InvalidOperation

from sqlalchemy import select, and_, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contract import Contract
from app.models.student import Student
from app.models.course import Course
from app.schemas.contract import (
    ContractCreate,
    ContractUpdate,
    ContractDeductHours,
    ContractAddHours,
)


logger = logging.getLogger(__name__)


class ContractServiceError(Exception):
    """合同服务异常基类"""
    pass


class ContractNotFoundError(ContractServiceError):
    """合同不存在异常"""
    pass


class ContractNoExistsError(ContractServiceError):
    """合同编号已存在异常"""
    pass


class StudentNotFoundError(ContractServiceError):
    """学员不存在异常"""
    pass


class CourseNotFoundError(ContractServiceError):
    """课程不存在异常"""
    pass


class InsufficientHoursError(ContractServiceError):
    """课时不足异常"""
    pass


class InvalidContractDataError(ContractServiceError):
    """无效合同数据异常"""
    pass


class InvalidContractStatusError(ContractServiceError):
    """无效合同状态异常"""
    pass


class ContractService:
    """合同业务服务类

    提供合同的完整业务逻辑处理
    所有方法都是异步的，需要传入 AsyncSession
    """

    # ==================== 合同查询服务 ====================

    @staticmethod
    async def get_all_contracts(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        student_id: Optional[int] = None,
        course_id: Optional[int] = None,
        status: Optional[int] = None
    ) -> List[Contract]:
        """
        获取合同列表，支持分页和筛选

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

        from app.crud.contract import ContractCRUD

        contracts = await ContractCRUD.get_all(
            session=session,
            skip=skip,
            limit=limit,
            student_id=student_id,
            course_id=course_id,
            status=status
        )

        return contracts

    @staticmethod
    async def get_contract_by_id(contract_id: int, session: AsyncSession) -> Contract:
        """
        根据ID获取合同详情

        Args:
            contract_id: 合同ID
            session: 数据库会话

        Returns:
            Contract: 合同对象

        Raises:
            ContractNotFoundError: 合同不存在
        """
        logger.info(f"查询合同详情: contract_id={contract_id}")

        from app.crud.contract import ContractCRUD

        contract = await ContractCRUD.get_by_id(contract_id, session)

        if not contract:
            logger.warning(f"合同不存在: contract_id={contract_id}")
            raise ContractNotFoundError(f"合同不存在: {contract_id}")

        return contract

    @staticmethod
    async def get_contract_by_no(contract_no: str, session: AsyncSession) -> Contract:
        """
        根据合同编号获取合同

        Args:
            contract_no: 合同编号
            session: 数据库会话

        Returns:
            Contract: 合同对象

        Raises:
            ContractNotFoundError: 合同不存在
        """
        logger.info(f"查询合同: contract_no={contract_no}")

        from app.crud.contract import ContractCRUD

        contract = await ContractCRUD.get_by_no(contract_no, session)

        if not contract:
            logger.warning(f"合同不存在: contract_no={contract_no}")
            raise ContractNotFoundError(f"合同不存在: {contract_no}")

        return contract

    @staticmethod
    async def count_contracts(
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
        from app.crud.contract import ContractCRUD

        count = await ContractCRUD.count(
            session=session,
            student_id=student_id,
            course_id=course_id,
            status=status
        )

        return count

    # ==================== 合同管理服务 ====================

    @staticmethod
    async def create_contract(
        contract_data: ContractCreate,
        created_by: Optional[int],
        session: AsyncSession
    ) -> Contract:
        """
        创建合同

        Args:
            contract_data: 合同创建数据
            created_by: 创建人ID
            session: 数据库会话

        Returns:
            Contract: 创建的合同对象

        Raises:
            StudentNotFoundError: 学员不存在
            CourseNotFoundError: 课程不存在
            ContractNoExistsError: 合同编号已存在
            InvalidContractDataError: 数据验证失败
        """
        logger.info(f"创建合同: contract_no={contract_data.contract_no}")

        from app.crud.contract import ContractCRUD

        # 验证学员存在
        student = await session.get(Student, contract_data.student_id)
        if not student:
            logger.warning(f"学员不存在: student_id={contract_data.student_id}")
            raise StudentNotFoundError(f"学员不存在: {contract_data.student_id}")

        # 验证课程存在（如果提供）
        if contract_data.course_id:
            course = await session.get(Course, contract_data.course_id)
            if not course:
                logger.warning(f"课程不存在: course_id={contract_data.course_id}")
                raise CourseNotFoundError(f"课程不存在: {contract_data.course_id}")

        # 检查合同编号是否已存在
        if await ContractCRUD.check_exists_by_no(contract_data.contract_no, session):
            raise ContractNoExistsError(f"合同编号已存在: {contract_data.contract_no}")

        # 数据验证
        if contract_data.remaining_hours > contract_data.total_hours:
            raise InvalidContractDataError("剩余课时不能超过总课时")

        # 计算总金额 = 单价 × 总课时 - 折扣金额
        calculated_total = (
            contract_data.unit_price * contract_data.total_hours
            - contract_data.discount_amount
        )
        if abs(calculated_total - contract_data.total_amount) > Decimal("0.01"):
            raise InvalidContractDataError(
                f"合同总金额计算错误: 应为 {calculated_total}，实际为 {contract_data.total_amount}"
            )

        # 创建合同
        try:
            contract = Contract(
                contract_no=contract_data.contract_no,
                student_id=contract_data.student_id,
                course_id=contract_data.course_id,
                package_type=contract_data.package_type,
                total_hours=contract_data.total_hours,
                remaining_hours=contract_data.remaining_hours,
                unit_price=contract_data.unit_price,
                total_amount=contract_data.total_amount,
                received_amount=contract_data.received_amount,
                discount_amount=contract_data.discount_amount,
                start_date=contract_data.start_date,
                end_date=contract_data.end_date,
                expire_warning_days=contract_data.expire_warning_days,
                contract_file=contract_data.contract_file,
                sales_id=contract_data.sales_id,
                notes=contract_data.notes,
                status=1,  # 默认生效
                created_by=created_by,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            return await ContractCRUD.create(contract, session)

        except IntegrityError as e:
            logger.error(f"创建合同失败: {e}")
            await session.rollback()
            raise ContractServiceError(f"创建合同失败: {str(e)}")

    @staticmethod
    async def update_contract(
        contract_id: int,
        contract_data: ContractUpdate,
        session: AsyncSession
    ) -> Contract:
        """
        更新合同

        Args:
            contract_id: 合同ID
            contract_data: 合同更新数据
            session: 数据库会话

        Returns:
            Contract: 更新后的合同对象

        Raises:
            ContractNotFoundError: 合同不存在
            CourseNotFoundError: 课程不存在
            InvalidContractDataError: 数据验证失败
        """
        logger.info(f"更新合同: contract_id={contract_id}")

        # 获取合同
        contract = await ContractService.get_contract_by_id(contract_id, session)

        # 验证课程存在（如果提供）
        if contract_data.course_id is not None:
            course = await session.get(Course, contract_data.course_id)
            if not course:
                logger.warning(f"课程不存在: course_id={contract_data.course_id}")
                raise CourseNotFoundError(f"课程不存在: {contract_data.course_id}")

        # 更新字段
        if contract_data.course_id is not None:
            contract.course_id = contract_data.course_id
        if contract_data.package_type is not None:
            contract.package_type = contract_data.package_type
        if contract_data.total_hours is not None:
            contract.total_hours = contract_data.total_hours
        if contract_data.remaining_hours is not None:
            if contract_data.remaining_hours > contract.total_hours:
                raise InvalidContractDataError("剩余课时不能超过总课时")
            contract.remaining_hours = contract_data.remaining_hours
        if contract_data.unit_price is not None:
            contract.unit_price = contract_data.unit_price
        if contract_data.total_amount is not None:
            contract.total_amount = contract_data.total_amount
        if contract_data.received_amount is not None:
            contract.received_amount = contract_data.received_amount
        if contract_data.discount_amount is not None:
            contract.discount_amount = contract_data.discount_amount
        if contract_data.start_date is not None:
            contract.start_date = contract_data.start_date
        if contract_data.end_date is not None:
            contract.end_date = contract_data.end_date
        if contract_data.expire_warning_days is not None:
            contract.expire_warning_days = contract_data.expire_warning_days
        if contract_data.status is not None:
            contract.status = contract_data.status
        if contract_data.contract_file is not None:
            contract.contract_file = contract_data.contract_file
        if contract_data.sales_id is not None:
            contract.sales_id = contract_data.sales_id
        if contract_data.notes is not None:
            contract.notes = contract_data.notes

        contract.updated_at = datetime.now()

        from app.crud.contract import ContractCRUD

        try:
            return await ContractCRUD.update(contract, session)
        except IntegrityError as e:
            logger.error(f"更新合同失败: {e}")
            await session.rollback()
            raise ContractServiceError(f"更新合同失败: {str(e)}")

    @staticmethod
    async def delete_contract(contract_id: int, session: AsyncSession) -> None:
        """
        删除合同

        Args:
            contract_id: 合同ID
            session: 数据库会话

        Raises:
            ContractNotFoundError: 合同不存在
            ContractServiceError: 删除失败
        """
        logger.info(f"删除合同: contract_id={contract_id}")

        # 获取合同
        contract = await ContractService.get_contract_by_id(contract_id, session)

        from app.crud.contract import ContractCRUD

        try:
            await ContractCRUD.delete(contract, session)
        except IntegrityError as e:
            logger.error(f"删除合同失败: {e}")
            await session.rollback()
            raise ContractServiceError(f"删除合同失败，可能存在关联数据")

    # ==================== 课时管理服务 ====================

    @staticmethod
    async def deduct_hours(
        contract_id: int,
        deduct_data: ContractDeductHours,
        session: AsyncSession
    ) -> Contract:
        """
        扣减课时

        Args:
            contract_id: 合同ID
            deduct_data: 扣减数据
            session: 数据库会话

        Returns:
            Contract: 更新后的合同对象

        Raises:
            ContractNotFoundError: 合同不存在
            InsufficientHoursError: 课时不足
            InvalidContractStatusError: 合同状态不允许扣减
        """
        logger.info(f"扣减课时: contract_id={contract_id}, hours={deduct_data.hours}")

        # 获取合同
        contract = await ContractService.get_contract_by_id(contract_id, session)

        # 检查合同状态
        if contract.status != 1:
            raise InvalidContractStatusError(
                f"合同状态不允许扣减课时: 当前状态={contract.status}"
            )

        # 检查课时是否足够
        if contract.remaining_hours < deduct_data.hours:
            raise InsufficientHoursError(
                f"课时不足: 剩余 {contract.remaining_hours} 课时，需要扣减 {deduct_data.hours} 课时"
            )

        # 扣减课时
        contract.remaining_hours -= deduct_data.hours
        contract.updated_at = datetime.now()

        from app.crud.contract import ContractCRUD

        return await ContractCRUD.update(contract, session)

    @staticmethod
    async def add_hours(
        contract_id: int,
        add_data: ContractAddHours,
        session: AsyncSession
    ) -> Contract:
        """
        追加课时

        Args:
            contract_id: 合同ID
            add_data: 追加数据
            session: 数据库会话

        Returns:
            Contract: 更新后的合同对象

        Raises:
            ContractNotFoundError: 合同不存在
            InvalidContractStatusError: 合同状态不允许追加
        """
        logger.info(f"追加课时: contract_id={contract_id}, hours={add_data.hours}")

        # 获取合同
        contract = await ContractService.get_contract_by_id(contract_id, session)

        # 检查合同状态
        if contract.status not in [1, 2]:  # 生效或完结
            raise InvalidContractStatusError(
                f"合同状态不允许追加课时: 当前状态={contract.status}"
            )

        # 追加课时
        contract.remaining_hours += add_data.hours
        contract.total_hours += add_data.hours
        contract.updated_at = datetime.now()

        from app.crud.contract import ContractCRUD

        return await ContractCRUD.update(contract, session)

    # ==================== 到期检查服务 ====================

    @staticmethod
    async def check_expiry(session: AsyncSession) -> List[Contract]:
        """
        检查即将到期的合同

        Args:
            session: 数据库会话

        Returns:
            List[Contract]: 即将到期的合同列表
        """
        logger.info("检查即将到期的合同")

        from app.crud.contract import ContractCRUD

        # 获取所有生效的合同
        contracts = await ContractCRUD.get_all(
            session=session,
            skip=0,
            limit=1000,  # 获取足够多的合同
            status=1
        )

        expiring_contracts = []
        today = date.today()

        for contract in contracts:
            if contract.end_date:
                days_until_expiry = (contract.end_date - today).days

                # 如果到期天数在预警范围内
                if 0 <= days_until_expiry <= contract.expire_warning_days:
                    expiring_contracts.append(contract)

                # 自动标记过期合同
                elif days_until_expiry < 0 and contract.status == 1:
                    contract.status = 4  # 标记为过期
                    contract.updated_at = datetime.now()
                    await ContractCRUD.update(contract, session)

        logger.info(f"发现 {len(expiring_contracts)} 个即将到期的合同")
        return expiring_contracts

    @staticmethod
    async def mark_as_expired(contract_id: int, session: AsyncSession) -> Contract:
        """
        标记合同为过期

        Args:
            contract_id: 合同ID
            session: 数据库会话

        Returns:
            Contract: 更新后的合同对象

        Raises:
            ContractNotFoundError: 合同不存在
            InvalidContractStatusError: 合同状态不允许标记
        """
        logger.info(f"标记合同为过期: contract_id={contract_id}")

        # 获取合同
        contract = await ContractService.get_contract_by_id(contract_id, session)

        # 检查合同状态
        if contract.status == 4:
            raise InvalidContractStatusError("合同已经是过期状态")

        # 标记为过期
        contract.status = 4
        contract.updated_at = datetime.now()

        from app.crud.contract import ContractCRUD

        return await ContractCRUD.update(contract, session)

    # ==================== 金额计算服务 ====================

    @staticmethod
    def calculate_total_amount(
        unit_price: Decimal,
        total_hours: Decimal,
        discount_amount: Decimal = Decimal("0.00")
    ) -> Decimal:
        """
        计算合同总金额

        Args:
            unit_price: 单价
            total_hours: 总课时
            discount_amount: 折扣金额

        Returns:
            Decimal: 合同总金额

        Formula:
            总金额 = 单价 × 总课时 - 折扣金额
        """
        total = unit_price * total_hours - discount_amount
        return total.quantize(Decimal("0.01"))

    @staticmethod
    def calculate_remaining_value(
        unit_price: Decimal,
        remaining_hours: Decimal
    ) -> Decimal:
        """
        计算剩余课时价值

        Args:
            unit_price: 单价
            remaining_hours: 剩余课时

        Returns:
            Decimal: 剩余课时价值
        """
        value = unit_price * remaining_hours
        return value.quantize(Decimal("0.01"))

    @staticmethod
    def calculate_usage_percentage(total_hours: Decimal, remaining_hours: Decimal) -> Decimal:
        """
        计算课时使用百分比

        Args:
            total_hours: 总课时
            remaining_hours: 剩余课时

        Returns:
            Decimal: 使用百分比（0-100）
        """
        if total_hours == 0:
            return Decimal("0.00")

        used_hours = total_hours - remaining_hours
        percentage = (used_hours / total_hours) * 100
        return percentage.quantize(Decimal("0.01"))


# 创建服务实例
contract_service = ContractService()
