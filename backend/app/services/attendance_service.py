"""Attendance Business Logic Service

考勤业务逻辑服务层

提供考勤管理的业务逻辑处理，包括：
- 考勤查询、创建、更新、删除
- 批量考勤处理
- 课时自动扣减
- 考勤统计
"""
import logging
from datetime import datetime
from typing import List, Optional
from decimal import Decimal, InvalidOperation

from sqlalchemy import select, and_, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attendance import Attendance
from app.models.schedule import Schedule
from app.models.student import Student
from app.models.contract import Contract
from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceBatchCreate,
)
from app.services.contract_service import (
    ContractService,
    ContractNotFoundError,
    InsufficientHoursError,
    ContractServiceError,
)


logger = logging.getLogger(__name__)


class AttendanceServiceError(Exception):
    """考勤服务异常基类"""
    pass


class AttendanceNotFoundError(AttendanceServiceError):
    """考勤不存在异常"""
    pass


class ScheduleNotFoundError(AttendanceServiceError):
    """排课不存在异常"""
    pass


class StudentNotFoundError(AttendanceServiceError):
    """学员不存在异常"""
    pass


class DuplicateAttendanceError(AttendanceServiceError):
    """重复考勤异常"""
    pass


class InvalidAttendanceDataError(AttendanceServiceError):
    """无效考勤数据异常"""
    pass


class InvalidAttendanceStatusError(AttendanceServiceError):
    """无效考勤状态异常"""
    pass


class AttendanceService:
    """考勤业务服务类

    提供考勤的完整业务逻辑处理
    所有方法都是异步的，需要传入 AsyncSession
    """

    # ==================== 考勤查询服务 ====================

    @staticmethod
    async def get_all_attendances(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        schedule_id: Optional[int] = None,
        student_id: Optional[int] = None,
        contract_id: Optional[int] = None,
        status: Optional[int] = None
    ) -> List[Attendance]:
        """
        获取考勤列表，支持分页和筛选

        Args:
            session: 数据库会话
            skip: 跳过记录数
            limit: 返回记录数
            schedule_id: 排课ID筛选
            student_id: 学员ID筛选
            contract_id: 合同ID筛选
            status: 状态筛选 (1:出勤 2:请假 3:缺勤 4:迟到)

        Returns:
            List[Attendance]: 考勤列表
        """
        logger.info(f"查询考勤列表: skip={skip}, limit={limit}")

        from app.crud.attendance import AttendanceCRUD

        attendances = await AttendanceCRUD.get_all(
            session=session,
            skip=skip,
            limit=limit,
            schedule_id=schedule_id,
            student_id=student_id,
            contract_id=contract_id,
            status=status
        )

        return attendances

    @staticmethod
    async def get_attendance_by_id(
        attendance_id: int,
        session: AsyncSession
    ) -> Attendance:
        """
        根据ID获取考勤详情

        Args:
            attendance_id: 考勤ID
            session: 数据库会话

        Returns:
            Attendance: 考勤对象

        Raises:
            AttendanceNotFoundError: 考勤不存在
        """
        logger.info(f"查询考勤详情: attendance_id={attendance_id}")

        from app.crud.attendance import AttendanceCRUD

        attendance = await AttendanceCRUD.get_by_id(attendance_id, session)

        if not attendance:
            logger.warning(f"考勤不存在: attendance_id={attendance_id}")
            raise AttendanceNotFoundError(f"考勤不存在: {attendance_id}")

        return attendance

    @staticmethod
    async def count_attendances(
        session: AsyncSession,
        schedule_id: Optional[int] = None,
        student_id: Optional[int] = None,
        contract_id: Optional[int] = None,
        status: Optional[int] = None
    ) -> int:
        """
        统计考勤数量

        Args:
            session: 数据库会话
            schedule_id: 排课ID筛选
            student_id: 学员ID筛选
            contract_id: 合同ID筛选
            status: 状态筛选

        Returns:
            int: 考勤总数
        """
        from app.crud.attendance import AttendanceCRUD

        count = await AttendanceCRUD.count(
            session=session,
            schedule_id=schedule_id,
            student_id=student_id,
            contract_id=contract_id,
            status=status
        )

        return count

    # ==================== 考勤管理服务 ====================

    @staticmethod
    async def create_attendance(
        attendance_data: AttendanceCreate,
        created_by: Optional[int],
        session: AsyncSession,
        auto_deduct: bool = True
    ) -> Attendance:
        """
        创建考勤

        Args:
            attendance_data: 考勤创建数据
            created_by: 创建人ID
            session: 数据库会话
            auto_deduct: 是否自动扣减课时

        Returns:
            Attendance: 创建的考勤对象

        Raises:
            ScheduleNotFoundError: 排课不存在
            StudentNotFoundError: 学员不存在
            DuplicateAttendanceError: 重复考勤
            InvalidAttendanceDataError: 数据验证失败
            InsufficientHoursError: 课时不足
        """
        logger.info(
            f"创建考勤: schedule_id={attendance_data.schedule_id}, "
            f"student_id={attendance_data.student_id}"
        )

        # 验证排课存在
        schedule = await session.get(Schedule, attendance_data.schedule_id)
        if not schedule:
            logger.warning(f"排课不存在: schedule_id={attendance_data.schedule_id}")
            raise ScheduleNotFoundError(f"排课不存在: {attendance_data.schedule_id}")

        # 验证学员存在
        student = await session.get(Student, attendance_data.student_id)
        if not student:
            logger.warning(f"学员不存在: student_id={attendance_data.student_id}")
            raise StudentNotFoundError(f"学员不存在: {attendance_data.student_id}")

        # 验证合同存在（如果提供）
        contract = None
        if attendance_data.contract_id:
            contract = await session.get(Contract, attendance_data.contract_id)
            if not contract:
                logger.warning(f"合同不存在: contract_id={attendance_data.contract_id}")
                raise ContractNotFoundError(f"合同不存在: {attendance_data.contract_id}")

        # 检查重复考勤
        from app.crud.attendance import AttendanceCRUD

        if await AttendanceCRUD.check_duplicate_attendance(
            session=session,
            schedule_id=attendance_data.schedule_id,
            student_id=attendance_data.student_id
        ):
            raise DuplicateAttendanceError(
                f"学员已考勤: schedule_id={attendance_data.schedule_id}, "
                f"student_id={attendance_data.student_id}"
            )

        # 验证考勤状态和消耗课时
        if attendance_data.status not in [1, 2, 3, 4]:
            raise InvalidAttendanceStatusError(
                f"无效的考勤状态: {attendance_data.status}"
            )

        # 创建考勤
        try:
            attendance = Attendance(
                schedule_id=attendance_data.schedule_id,
                student_id=attendance_data.student_id,
                contract_id=attendance_data.contract_id,
                status=attendance_data.status,
                check_time=attendance_data.check_time,
                check_method=attendance_data.check_method,
                hours_consumed=attendance_data.hours_consumed,
                notes=attendance_data.notes,
                created_by=created_by,
                created_at=datetime.now()
            )

            attendance = await AttendanceCRUD.create(attendance, session)

            # 自动扣减课时（出勤和迟到需要扣课时）
            if auto_deduct and contract and attendance.status in [1, 4]:
                await AttendanceService._deduct_hours_for_attendance(
                    attendance=attendance,
                    contract=contract,
                    session=session
                )

            return attendance

        except IntegrityError as e:
            logger.error(f"创建考勤失败: {e}")
            await session.rollback()
            raise AttendanceServiceError(f"创建考勤失败: {str(e)}")

    @staticmethod
    async def batch_create_attendances(
        batch_data: AttendanceBatchCreate,
        created_by: Optional[int],
        session: AsyncSession
    ) -> List[Attendance]:
        """
        批量创建考勤

        Args:
            batch_data: 批量创建数据
            created_by: 创建人ID
            session: 数据库会话

        Returns:
            List[Attendance]: 创建的考勤对象列表

        Raises:
            ScheduleNotFoundError: 排课不存在
            StudentNotFoundError: 学员不存在
            DuplicateAttendanceError: 重复考勤
            InsufficientHoursError: 课时不足
        """
        logger.info(f"批量创建考勤: {len(batch_data.attendances)} 条")

        attendances = []

        try:
            for attendance_data in batch_data.attendances:
                attendance = await AttendanceService.create_attendance(
                    attendance_data=attendance_data,
                    created_by=created_by,
                    session=session,
                    auto_deduct=batch_data.auto_deduct_hours
                )
                attendances.append(attendance)

            logger.info(f"批量考勤创建成功: {len(attendances)} 条")
            return attendances

        except AttendanceServiceError:
            # 业务异常直接抛出
            raise
        except Exception as e:
            logger.error(f"批量创建考勤失败: {e}")
            await session.rollback()
            raise AttendanceServiceError(f"批量创建考勤失败: {str(e)}")

    @staticmethod
    async def update_attendance(
        attendance_id: int,
        attendance_data: AttendanceUpdate,
        session: AsyncSession
    ) -> Attendance:
        """
        更新考勤

        Args:
            attendance_id: 考勤ID
            attendance_data: 考勤更新数据
            session: 数据库会话

        Returns:
            Attendance: 更新后的考勤对象

        Raises:
            AttendanceNotFoundError: 考勤不存在
            ScheduleNotFoundError: 排课不存在
            StudentNotFoundError: 学员不存在
            InvalidAttendanceDataError: 数据验证失败
        """
        logger.info(f"更新考勤: attendance_id={attendance_id}")

        # 获取考勤
        attendance = await AttendanceService.get_attendance_by_id(attendance_id, session)

        # 验证排课存在（如果更新）
        if attendance_data.schedule_id is not None:
            schedule = await session.get(Schedule, attendance_data.schedule_id)
            if not schedule:
                logger.warning(f"排课不存在: schedule_id={attendance_data.schedule_id}")
                raise ScheduleNotFoundError(f"排课不存在: {attendance_data.schedule_id}")

            # 检查重复考勤
            from app.crud.attendance import AttendanceCRUD

            if await AttendanceCRUD.check_duplicate_attendance(
                session=session,
                schedule_id=attendance_data.schedule_id,
                student_id=attendance_data.student_id or attendance.student_id,
                exclude_id=attendance_id
            ):
                raise DuplicateAttendanceError(
                    f"学员已考勤: schedule_id={attendance_data.schedule_id}"
                )

        # 验证学员存在（如果更新）
        if attendance_data.student_id is not None:
            student = await session.get(Student, attendance_data.student_id)
            if not student:
                logger.warning(f"学员不存在: student_id={attendance_data.student_id}")
                raise StudentNotFoundError(f"学员不存在: {attendance_data.student_id}")

        # 验证合同存在（如果更新）
        if attendance_data.contract_id is not None:
            contract = await session.get(Contract, attendance_data.contract_id)
            if not contract:
                logger.warning(f"合同不存在: contract_id={attendance_data.contract_id}")
                raise ContractNotFoundError(f"合同不存在: {attendance_data.contract_id}")

        # 更新字段
        if attendance_data.schedule_id is not None:
            attendance.schedule_id = attendance_data.schedule_id
        if attendance_data.student_id is not None:
            attendance.student_id = attendance_data.student_id
        if attendance_data.contract_id is not None:
            attendance.contract_id = attendance_data.contract_id
        if attendance_data.status is not None:
            if attendance_data.status not in [1, 2, 3, 4]:
                raise InvalidAttendanceStatusError(
                    f"无效的考勤状态: {attendance_data.status}"
                )
            attendance.status = attendance_data.status
        if attendance_data.check_time is not None:
            attendance.check_time = attendance_data.check_time
        if attendance_data.check_method is not None:
            attendance.check_method = attendance_data.check_method
        if attendance_data.hours_consumed is not None:
            attendance.hours_consumed = attendance_data.hours_consumed
        if attendance_data.notes is not None:
            attendance.notes = attendance_data.notes

        from app.crud.attendance import AttendanceCRUD

        try:
            return await AttendanceCRUD.update(attendance, session)
        except IntegrityError as e:
            logger.error(f"更新考勤失败: {e}")
            await session.rollback()
            raise AttendanceServiceError(f"更新考勤失败: {str(e)}")

    @staticmethod
    async def delete_attendance(
        attendance_id: int,
        session: AsyncSession
    ) -> None:
        """
        删除考勤

        Args:
            attendance_id: 考勤ID
            session: 数据库会话

        Raises:
            AttendanceNotFoundError: 考勤不存在
            AttendanceServiceError: 删除失败
        """
        logger.info(f"删除考勤: attendance_id={attendance_id}")

        # 获取考勤
        attendance = await AttendanceService.get_attendance_by_id(attendance_id, session)

        from app.crud.attendance import AttendanceCRUD

        try:
            await AttendanceCRUD.delete(attendance, session)
        except IntegrityError as e:
            logger.error(f"删除考勤失败: {e}")
            await session.rollback()
            raise AttendanceServiceError(f"删除考勤失败，可能存在关联数据")

    # ==================== 课时扣减服务 ====================

    @staticmethod
    async def _deduct_hours_for_attendance(
        attendance: Attendance,
        contract: Contract,
        session: AsyncSession
    ) -> None:
        """
        为考勤扣减课时（内部方法）

        Args:
            attendance: 考勤对象
            contract: 合同对象
            session: 数据库会话

        Raises:
            InsufficientHoursError: 课时不足
            InvalidAttendanceStatusError: 状态不允许扣减
        """
        logger.info(
            f"扣减课时: contract_id={contract.id}, "
            f"hours={attendance.hours_consumed}"
        )

        # 检查合同状态
        if contract.status != 1:
            raise InvalidAttendanceStatusError(
                f"合同状态不允许扣减课时: 当前状态={contract.status}"
            )

        # 检查课时是否足够
        if contract.remaining_hours < attendance.hours_consumed:
            raise InsufficientHoursError(
                f"课时不足: 剩余 {contract.remaining_hours} 课时，"
                f"需要扣减 {attendance.hours_consumed} 课时"
            )

        # 扣减课时
        contract.remaining_hours -= attendance.hours_consumed
        contract.updated_at = datetime.now()

        from app.crud.contract import ContractCRUD

        await ContractCRUD.update(contract, session)

        logger.info(
            f"课时扣减成功: contract_id={contract.id}, "
            f"remaining={contract.remaining_hours}"
        )

    # ==================== 考勤统计服务 ====================

    @staticmethod
    async def get_student_statistics(
        student_id: int,
        session: AsyncSession
    ) -> dict:
        """
        获取学员考勤统计

        Args:
            student_id: 学员ID
            session: 数据库会话

        Returns:
            dict: 统计信息（总数、各状态数量、出勤率、总消耗课时）

        Raises:
            StudentNotFoundError: 学员不存在
        """
        logger.info(f"获取学员考勤统计: student_id={student_id}")

        # 验证学员存在
        student = await session.get(Student, student_id)
        if not student:
            logger.warning(f"学员不存在: student_id={student_id}")
            raise StudentNotFoundError(f"学员不存在: {student_id}")

        from app.crud.attendance import AttendanceCRUD

        stats = await AttendanceCRUD.get_statistics_by_student(session, student_id)

        # 计算出勤率
        if stats["total_count"] > 0:
            present_rate = (
                (stats["present_count"] + stats["late_count"]) /
                stats["total_count"] * 100
            )
        else:
            present_rate = 0.0

        stats["present_rate"] = round(present_rate, 2)

        return stats

    @staticmethod
    async def get_schedule_statistics(
        schedule_id: int,
        session: AsyncSession
    ) -> dict:
        """
        获取排课考勤统计

        Args:
            schedule_id: 排课ID
            session: 数据库会话

        Returns:
            dict: 统计信息（总数、各状态数量、出勤率、总消耗课时）

        Raises:
            ScheduleNotFoundError: 排课不存在
        """
        logger.info(f"获取排课考勤统计: schedule_id={schedule_id}")

        # 验证排课存在
        schedule = await session.get(Schedule, schedule_id)
        if not schedule:
            logger.warning(f"排课不存在: schedule_id={schedule_id}")
            raise ScheduleNotFoundError(f"排课不存在: {schedule_id}")

        from app.crud.attendance import AttendanceCRUD

        stats = await AttendanceCRUD.get_statistics_by_schedule(session, schedule_id)

        # 计算出勤率
        if stats["total_count"] > 0:
            present_rate = (
                (stats["present_count"] + stats["late_count"]) /
                stats["total_count"] * 100
            )
        else:
            present_rate = 0.0

        stats["present_rate"] = round(present_rate, 2)

        return stats

    @staticmethod
    async def get_course_statistics(
        course_id: int,
        session: AsyncSession,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> dict:
        """
        获取课程考勤统计

        Args:
            course_id: 课程ID
            session: 数据库会话
            start_date: 开始日期（可选）
            end_date: 结束日期（可选）

        Returns:
            dict: 统计信息（总数、各状态数量、出勤率、总消耗课时）
        """
        logger.info(f"获取课程考勤统计: course_id={course_id}")

        # 通过排课关联查询考勤
        from app.models.course import Course

        # 验证课程存在
        course = await session.get(Course, course_id)
        if not course:
            logger.warning(f"课程不存在: course_id={course_id}")
            raise ScheduleNotFoundError(f"课程不存在: {course_id}")

        # 查询该课程的所有排课ID
        schedule_query = select(Schedule.id).where(Schedule.course_id == course_id)
        schedule_result = await session.execute(schedule_query)
        schedule_ids = [row[0] for row in schedule_result.fetchall()]

        if not schedule_ids:
            return {
                "total_count": 0,
                "present_count": 0,
                "leave_count": 0,
                "absent_count": 0,
                "late_count": 0,
                "present_rate": 0.0,
                "total_hours_consumed": Decimal("0.0")
            }

        # 统计考勤
        from app.crud.attendance import AttendanceCRUD

        query = select(func.count(Attendance.id)).where(
            Attendance.schedule_id.in_(schedule_ids)
        )

        # 应用时间范围筛选
        conditions = []
        if start_date:
            conditions.append(Attendance.created_at >= start_date)
        if end_date:
            conditions.append(Attendance.created_at <= end_date)

        if conditions:
            query = query.where(and_(*conditions))

        total_result = await session.execute(query)
        total_count = total_result.scalar() or 0

        # 统计各状态数量
        status_counts = {1: 0, 2: 0, 3: 0, 4: 0}

        for status_value in status_counts.keys():
            status_query = select(func.count(Attendance.id)).where(
                and_(
                    Attendance.schedule_id.in_(schedule_ids),
                    Attendance.status == status_value
                )
            )

            if conditions:
                status_query = status_query.where(and_(*conditions))

            status_result = await session.execute(status_query)
            status_counts[status_value] = status_result.scalar() or 0

        # 统计总消耗课时
        hours_query = select(func.sum(Attendance.hours_consumed)).where(
            Attendance.schedule_id.in_(schedule_ids)
        )

        if conditions:
            hours_query = hours_query.where(and_(*conditions))

        hours_result = await session.execute(hours_query)
        total_hours = hours_result.scalar() or Decimal("0.0")

        # 计算出勤率
        if total_count > 0:
            present_rate = (
                (status_counts[1] + status_counts[4]) / total_count * 100
            )
        else:
            present_rate = 0.0

        return {
            "total_count": total_count,
            "present_count": status_counts[1],
            "leave_count": status_counts[2],
            "absent_count": status_counts[3],
            "late_count": status_counts[4],
            "present_rate": round(present_rate, 2),
            "total_hours_consumed": total_hours
        }


# 创建服务实例
attendance_service = AttendanceService()
