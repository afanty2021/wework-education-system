"""Attendance CRUD Operations

考勤数据访问层

提供考勤的基础 CRUD 操作
"""
import logging
from typing import List, Optional
from decimal import Decimal

from sqlalchemy import select, and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attendance import Attendance


logger = logging.getLogger(__name__)


class AttendanceCRUD:
    """考勤 CRUD 操作类

    提供考勤的基础数据访问操作
    所有方法都是异步的，需要传入 AsyncSession
    """

    @staticmethod
    async def get_all(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        schedule_id: Optional[int] = None,
        student_id: Optional[int] = None,
        contract_id: Optional[int] = None,
        status: Optional[int] = None
    ) -> List[Attendance]:
        """
        获取考勤列表

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

        query = select(Attendance)

        # 应用筛选条件
        conditions = []
        if schedule_id:
            conditions.append(Attendance.schedule_id == schedule_id)
        if student_id:
            conditions.append(Attendance.student_id == student_id)
        if contract_id:
            conditions.append(Attendance.contract_id == contract_id)
        if status is not None:
            conditions.append(Attendance.status == status)

        if conditions:
            query = query.where(and_(*conditions))

        # 排序和分页
        query = query.order_by(Attendance.created_at.desc()).offset(skip).limit(limit)

        result = await session.execute(query)
        attendances = result.scalars().all()

        logger.info(f"查询到 {len(attendances)} 条考勤记录")
        return attendances

    @staticmethod
    async def get_by_id(attendance_id: int, session: AsyncSession) -> Optional[Attendance]:
        """
        根据ID获取考勤

        Args:
            attendance_id: 考勤ID
            session: 数据库会话

        Returns:
            Optional[Attendance]: 考勤对象，不存在返回 None
        """
        logger.info(f"查询考勤: attendance_id={attendance_id}")

        attendance = await session.get(Attendance, attendance_id)

        if attendance:
            logger.info(f"查询到考勤记录: id={attendance_id}")
        else:
            logger.warning(f"考勤不存在: attendance_id={attendance_id}")

        return attendance

    @staticmethod
    async def create(attendance: Attendance, session: AsyncSession) -> Attendance:
        """
        创建考勤

        Args:
            attendance: 考勤对象
            session: 数据库会话

        Returns:
            Attendance: 创建的考勤对象
        """
        logger.info(f"创建考勤: schedule_id={attendance.schedule_id}, student_id={attendance.student_id}")

        session.add(attendance)
        await session.commit()
        await session.refresh(attendance)

        logger.info(f"考勤创建成功: id={attendance.id}")
        return attendance

    @staticmethod
    async def batch_create(
        attendances: List[Attendance],
        session: AsyncSession
    ) -> List[Attendance]:
        """
        批量创建考勤

        Args:
            attendances: 考勤对象列表
            session: 数据库会话

        Returns:
            List[Attendance]: 创建的考勤对象列表
        """
        logger.info(f"批量创建考勤: {len(attendances)} 条")

        for attendance in attendances:
            session.add(attendance)

        await session.commit()

        for attendance in attendances:
            await session.refresh(attendance)

        logger.info(f"批量考勤创建成功: {len(attendances)} 条")
        return attendances

    @staticmethod
    async def update(attendance: Attendance, session: AsyncSession) -> Attendance:
        """
        更新考勤

        Args:
            attendance: 考勤对象
            session: 数据库会话

        Returns:
            Attendance: 更新后的考勤对象
        """
        logger.info(f"更新考勤: id={attendance.id}")

        session.add(attendance)
        await session.commit()
        await session.refresh(attendance)

        logger.info(f"考勤更新成功: id={attendance.id}")
        return attendance

    @staticmethod
    async def delete(attendance: Attendance, session: AsyncSession) -> None:
        """
        删除考勤

        Args:
            attendance: 考勤对象
            session: 数据库会话
        """
        logger.info(f"删除考勤: id={attendance.id}")

        await session.delete(attendance)
        await session.commit()

        logger.info(f"考勤删除成功: id={attendance.id}")

    @staticmethod
    async def count(
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
        query = select(func.count(Attendance.id))

        conditions = []
        if schedule_id:
            conditions.append(Attendance.schedule_id == schedule_id)
        if student_id:
            conditions.append(Attendance.student_id == student_id)
        if contract_id:
            conditions.append(Attendance.contract_id == contract_id)
        if status is not None:
            conditions.append(Attendance.status == status)

        if conditions:
            query = query.where(and_(*conditions))

        result = await session.execute(query)
        count = result.scalar()

        return count

    @staticmethod
    async def get_statistics_by_student(
        session: AsyncSession,
        student_id: int
    ) -> dict:
        """
        获取学员考勤统计

        Args:
            session: 数据库会话
            student_id: 学员ID

        Returns:
            dict: 统计信息
        """
        # 统计总数
        total_query = select(func.count(Attendance.id)).where(
            Attendance.student_id == student_id
        )
        total_result = await session.execute(total_query)
        total_count = total_result.scalar() or 0

        # 统计各状态数量
        status_counts = {1: 0, 2: 0, 3: 0, 4: 0}  # 出勤、请假、缺勤、迟到

        for status_value in status_counts.keys():
            status_query = select(func.count(Attendance.id)).where(
                and_(
                    Attendance.student_id == student_id,
                    Attendance.status == status_value
                )
            )
            status_result = await session.execute(status_query)
            status_counts[status_value] = status_result.scalar() or 0

        # 统计总消耗课时
        hours_query = select(func.sum(Attendance.hours_consumed)).where(
            Attendance.student_id == student_id
        )
        hours_result = await session.execute(hours_query)
        total_hours = hours_result.scalar() or Decimal("0.0")

        return {
            "total_count": total_count,
            "present_count": status_counts[1],
            "leave_count": status_counts[2],
            "absent_count": status_counts[3],
            "late_count": status_counts[4],
            "total_hours_consumed": total_hours
        }

    @staticmethod
    async def get_statistics_by_schedule(
        session: AsyncSession,
        schedule_id: int
    ) -> dict:
        """
        获取排课考勤统计

        Args:
            session: 数据库会话
            schedule_id: 排课ID

        Returns:
            dict: 统计信息
        """
        # 统计总数
        total_query = select(func.count(Attendance.id)).where(
            Attendance.schedule_id == schedule_id
        )
        total_result = await session.execute(total_query)
        total_count = total_result.scalar() or 0

        # 统计各状态数量
        status_counts = {1: 0, 2: 0, 3: 0, 4: 0}

        for status_value in status_counts.keys():
            status_query = select(func.count(Attendance.id)).where(
                and_(
                    Attendance.schedule_id == schedule_id,
                    Attendance.status == status_value
                )
            )
            status_result = await session.execute(status_query)
            status_counts[status_value] = status_result.scalar() or 0

        # 统计总消耗课时
        hours_query = select(func.sum(Attendance.hours_consumed)).where(
            Attendance.schedule_id == schedule_id
        )
        hours_result = await session.execute(hours_query)
        total_hours = hours_result.scalar() or Decimal("0.0")

        return {
            "total_count": total_count,
            "present_count": status_counts[1],
            "leave_count": status_counts[2],
            "absent_count": status_counts[3],
            "late_count": status_counts[4],
            "total_hours_consumed": total_hours
        }

    @staticmethod
    async def check_duplicate_attendance(
        session: AsyncSession,
        schedule_id: int,
        student_id: int,
        exclude_id: Optional[int] = None
    ) -> bool:
        """
        检查是否存在重复考勤

        Args:
            session: 数据库会话
            schedule_id: 排课ID
            student_id: 学员ID
            exclude_id: 排除的考勤ID（用于更新时）

        Returns:
            bool: 存在重复返回 True，否则返回 False
        """
        query = select(func.count(Attendance.id)).where(
            and_(
                Attendance.schedule_id == schedule_id,
                Attendance.student_id == student_id
            )
        )

        if exclude_id:
            query = query.where(Attendance.id != exclude_id)

        result = await session.execute(query)
        count = result.scalar()
        return count > 0
