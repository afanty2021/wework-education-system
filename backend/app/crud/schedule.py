"""排课 CRUD Operations

排课数据访问层

提供排课的基础 CRUD 操作
"""
import logging
from typing import List, Optional

from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schedule import Schedule


logger = logging.getLogger(__name__)


class ScheduleCRUD:
    """排课 CRUD 操作类

    提供排课的基础数据访问操作
    所有方法都是异步的，需要传入 AsyncSession
    """

    @staticmethod
    async def get_all(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        course_id: Optional[int] = None,
        teacher_id: Optional[int] = None,
        classroom_id: Optional[int] = None,
        department_id: Optional[int] = None,
        status: Optional[int] = None
    ) -> List[Schedule]:
        """
        获取排课列表

        Args:
            session: 数据库会话
            skip: 跳过记录数
            limit: 返回记录数
            course_id: 课程ID筛选
            teacher_id: 教师ID筛选
            classroom_id: 教室ID筛选
            department_id: 校区ID筛选
            status: 状态筛选 (1:已安排 2:已上课 3:已取消 4:已调课)

        Returns:
            List[Schedule]: 排课列表
        """
        logger.info(f"查询排课列表: skip={skip}, limit={limit}")

        query = select(Schedule)

        # 应用筛选条件
        conditions = []
        if course_id:
            conditions.append(Schedule.course_id == course_id)
        if teacher_id:
            conditions.append(Schedule.teacher_id == teacher_id)
        if classroom_id:
            conditions.append(Schedule.classroom_id == classroom_id)
        if department_id:
            conditions.append(Schedule.department_id == department_id)
        if status is not None:
            conditions.append(Schedule.status == status)

        if conditions:
            query = query.where(and_(*conditions))

        # 排序和分页
        query = query.order_by(Schedule.start_time.desc()).offset(skip).limit(limit)

        result = await session.execute(query)
        schedules = result.scalars().all()

        logger.info(f"查询到 {len(schedules)} 个排课")
        return schedules

    @staticmethod
    async def get_by_id(schedule_id: int, session: AsyncSession) -> Optional[Schedule]:
        """
        根据ID获取排课

        Args:
            schedule_id: 排课ID
            session: 数据库会话

        Returns:
            Optional[Schedule]: 排课对象，不存在返回 None
        """
        logger.info(f"查询排课: schedule_id={schedule_id}")

        schedule = await session.get(Schedule, schedule_id)

        if schedule:
            logger.info(f"查询到排课: id={schedule.id}")
        else:
            logger.warning(f"排课不存在: schedule_id={schedule_id}")

        return schedule

    @staticmethod
    async def get_by_time_range(
        start_time,
        end_time,
        session: AsyncSession,
        teacher_id: Optional[int] = None,
        classroom_id: Optional[int] = None,
        course_id: Optional[int] = None,
        exclude_schedule_id: Optional[int] = None
    ) -> List[Schedule]:
        """
        获取时间范围内的排课（用于冲突检测）

        Args:
            start_time: 开始时间
            end_time: 结束时间
            session: 数据库会话
            teacher_id: 教师ID筛选
            classroom_id: 教室ID筛选
            course_id: 课程ID筛选
            exclude_schedule_id: 排除的排课ID

        Returns:
            List[Schedule]: 时间重叠的排课列表
        """
        logger.info(f"查询时间范围排课: start={start_time}, end={end_time}")

        conditions = []

        # 时间重叠条件: (start_time < 现有排课的结束时间) AND (end_time > 现有排课的开始时间)
        time_overlap = and_(
            start_time < Schedule.end_time,
            end_time > Schedule.start_time
        )
        conditions.append(time_overlap)

        # 其他筛选条件
        if teacher_id:
            conditions.append(Schedule.teacher_id == teacher_id)
        if classroom_id:
            conditions.append(Schedule.classroom_id == classroom_id)
        if course_id:
            conditions.append(Schedule.course_id == course_id)

        # 排除特定排课（用于更新时）
        if exclude_schedule_id:
            conditions.append(Schedule.id != exclude_schedule_id)

        # 只查询未取消的排课
        conditions.append(Schedule.status != 3)  # 3: 已取消

        query = select(Schedule).where(
            and_(*conditions)
        ).order_by(Schedule.start_time)

        result = await session.execute(query)
        schedules = result.scalars().all()

        logger.info(f"查询到 {len(schedules)} 个时间重叠的排课")
        return schedules

    @staticmethod
    async def create(schedule: Schedule, session: AsyncSession) -> Schedule:
        """
        创建排课

        Args:
            schedule: 排课对象
            session: 数据库会话

        Returns:
            Schedule: 创建的排课对象
        """
        logger.info(f"创建排课: course_id={schedule.course_id}, teacher_id={schedule.teacher_id}")

        session.add(schedule)
        await session.commit()
        await session.refresh(schedule)

        logger.info(f"排课创建成功: id={schedule.id}")
        return schedule

    @staticmethod
    async def update(schedule: Schedule, session: AsyncSession) -> Schedule:
        """
        更新排课

        Args:
            schedule: 排课对象
            session: 数据库会话

        Returns:
            Schedule: 更新后的排课对象
        """
        logger.info(f"更新排课: id={schedule.id}")

        session.add(schedule)
        await session.commit()
        await session.refresh(schedule)

        logger.info(f"排课更新成功: id={schedule.id}")
        return schedule

    @staticmethod
    async def delete(schedule: Schedule, session: AsyncSession) -> None:
        """
        删除排课

        Args:
            schedule: 排课对象
            session: 数据库会话
        """
        logger.info(f"删除排课: id={schedule.id}")

        await session.delete(schedule)
        await session.commit()

        logger.info(f"排课删除成功: id={schedule.id}")

    @staticmethod
    async def count(
        session: AsyncSession,
        course_id: Optional[int] = None,
        teacher_id: Optional[int] = None,
        classroom_id: Optional[int] = None,
        department_id: Optional[int] = None,
        status: Optional[int] = None
    ) -> int:
        """
        统计排课数量

        Args:
            session: 数据库会话
            course_id: 课程ID筛选
            teacher_id: 教师ID筛选
            classroom_id: 教室ID筛选
            department_id: 校区ID筛选
            status: 状态筛选

        Returns:
            int: 排课总数
        """
        query = select(func.count(Schedule.id))

        conditions = []
        if course_id:
            conditions.append(Schedule.course_id == course_id)
        if teacher_id:
            conditions.append(Schedule.teacher_id == teacher_id)
        if classroom_id:
            conditions.append(Schedule.classroom_id == classroom_id)
        if department_id:
            conditions.append(Schedule.department_id == department_id)
        if status is not None:
            conditions.append(Schedule.status == status)

        if conditions:
            query = query.where(and_(*conditions))

        result = await session.execute(query)
        count = result.scalar()

        return count

    @staticmethod
    async def get_by_teacher_and_time(
        teacher_id: int,
        start_time,
        end_time,
        session: AsyncSession,
        exclude_schedule_id: Optional[int] = None
    ) -> List[Schedule]:
        """
        获取教师在指定时间的排课

        Args:
            teacher_id: 教师ID
            start_time: 开始时间
            end_time: 结束时间
            session: 数据库会话
            exclude_schedule_id: 排除的排课ID

        Returns:
            List[Schedule]: 时间重叠的排课列表
        """
        logger.info(f"查询教师时间冲突: teacher_id={teacher_id}")

        return await ScheduleCRUD.get_by_time_range(
            start_time=start_time,
            end_time=end_time,
            session=session,
            teacher_id=teacher_id,
            exclude_schedule_id=exclude_schedule_id
        )

    @staticmethod
    async def get_by_classroom_and_time(
        classroom_id: int,
        start_time,
        end_time,
        session: AsyncSession,
        exclude_schedule_id: Optional[int] = None
    ) -> List[Schedule]:
        """
        获取教室在指定时间的排课

        Args:
            classroom_id: 教室ID
            start_time: 开始时间
            end_time: 结束时间
            session: 数据库会话
            exclude_schedule_id: 排除的排课ID

        Returns:
            List[Schedule]: 时间重叠的排课列表
        """
        logger.info(f"查询教室时间冲突: classroom_id={classroom_id}")

        return await ScheduleCRUD.get_by_time_range(
            start_time=start_time,
            end_time=end_time,
            session=session,
            classroom_id=classroom_id,
            exclude_schedule_id=exclude_schedule_id
        )

    @staticmethod
    async def get_by_course_and_time(
        course_id: int,
        start_time,
        end_time,
        session: AsyncSession,
        exclude_schedule_id: Optional[int] = None
    ) -> List[Schedule]:
        """
        获取课程在指定时间的排课

        Args:
            course_id: 课程ID
            start_time: 开始时间
            end_time: 结束时间
            session: 数据库会话
            exclude_schedule_id: 排除的排课ID

        Returns:
            List[Schedule]: 时间重叠的排课列表
        """
        logger.info(f"查询课程时间冲突: course_id={course_id}")

        return await ScheduleCRUD.get_by_time_range(
            start_time=start_time,
            end_time=end_time,
            session=session,
            course_id=course_id,
            exclude_schedule_id=exclude_schedule_id
        )
