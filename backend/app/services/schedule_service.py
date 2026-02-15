"""排课 Business Logic Service

排课业务逻辑服务层

提供排课管理的业务逻辑处理，包括：
- 排课查询、创建、更新、删除
- 冲突检测（教师、教室、课程）
- 报名管理
- 循环排课支持
"""
import logging
import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, and_, or_, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schedule import Schedule
from app.models.course import Course, Classroom
from app.models.user import User
from app.models.student import Student
from app.schemas.schedule import (
    ScheduleCreate,
    ScheduleUpdate,
    ScheduleEnroll,
    ScheduleConflictCheck,
)


logger = logging.getLogger(__name__)


class ScheduleServiceError(Exception):
    """排课服务异常基类"""
    pass


class ScheduleNotFoundError(ScheduleServiceError):
    """排课不存在异常"""
    pass


class CourseNotFoundError(ScheduleServiceError):
    """课程不存在异常"""
    pass


class TeacherNotFoundError(ScheduleServiceError):
    """教师不存在异常"""
    pass


class ClassroomNotFoundError(ScheduleServiceError):
    """教室不存在异常"""
    pass


class StudentNotFoundError(ScheduleServiceError):
    """学员不存在异常"""
    pass


class ScheduleConflictError(ScheduleServiceError):
    """排课冲突异常"""
    def __init__(self, message: str, conflict_type: str, conflict_ids: List[int] = None):
        super().__init__(message)
        self.conflict_type = conflict_type
        self.conflict_ids = conflict_ids or []


class InvalidScheduleDataError(ScheduleServiceError):
    """无效排课数据异常"""
    pass


class ScheduleCapacityError(ScheduleServiceError):
    """排课容量不足异常"""
    pass


class InvalidScheduleStatusError(ScheduleServiceError):
    """无效排课状态异常"""
    pass


class ScheduleService:
    """排课业务服务类

    提供排课的完整业务逻辑处理
    所有方法都是异步的，需要传入 AsyncSession
    """

    # ==================== 排课查询服务 ====================

    @staticmethod
    async def get_all_schedules(
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
        获取排课列表，支持分页和筛选

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

        from app.crud.schedule import ScheduleCRUD

        schedules = await ScheduleCRUD.get_all(
            session=session,
            skip=skip,
            limit=limit,
            course_id=course_id,
            teacher_id=teacher_id,
            classroom_id=classroom_id,
            department_id=department_id,
            status=status
        )

        return schedules

    @staticmethod
    async def get_schedule_by_id(schedule_id: int, session: AsyncSession) -> Schedule:
        """
        根据ID获取排课详情

        Args:
            schedule_id: 排课ID
            session: 数据库会话

        Returns:
            Schedule: 排课对象

        Raises:
            ScheduleNotFoundError: 排课不存在
        """
        logger.info(f"查询排课详情: schedule_id={schedule_id}")

        from app.crud.schedule import ScheduleCRUD

        schedule = await ScheduleCRUD.get_by_id(schedule_id, session)

        if not schedule:
            logger.warning(f"排课不存在: schedule_id={schedule_id}")
            raise ScheduleNotFoundError(f"排课不存在: {schedule_id}")

        return schedule

    @staticmethod
    async def count_schedules(
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
        from app.crud.schedule import ScheduleCRUD

        count = await ScheduleCRUD.count(
            session=session,
            course_id=course_id,
            teacher_id=teacher_id,
            classroom_id=classroom_id,
            department_id=department_id,
            status=status
        )

        return count

    # ==================== 排课管理服务 ====================

    @staticmethod
    async def create_schedule(
        schedule_data: ScheduleCreate,
        created_by: Optional[int],
        session: AsyncSession
    ) -> Schedule:
        """
        创建排课

        Args:
            schedule_data: 排课创建数据
            created_by: 创建人ID
            session: 数据库会话

        Returns:
            Schedule: 创建的排课对象

        Raises:
            CourseNotFoundError: 课程不存在
            TeacherNotFoundError: 教师不存在
            ClassroomNotFoundError: 教室不存在
            InvalidScheduleDataError: 数据验证失败
            ScheduleConflictError: 存在时间冲突
        """
        logger.info(f"创建排课: course_id={schedule_data.course_id}, teacher_id={schedule_data.teacher_id}")

        # 验证课程存在
        course = await session.get(Course, schedule_data.course_id)
        if not course:
            logger.warning(f"课程不存在: course_id={schedule_data.course_id}")
            raise CourseNotFoundError(f"课程不存在: {schedule_data.course_id}")

        # 验证教师存在
        teacher = await session.get(User, schedule_data.teacher_id)
        if not teacher:
            logger.warning(f"教师不存在: teacher_id={schedule_data.teacher_id}")
            raise TeacherNotFoundError(f"教师不存在: {schedule_data.teacher_id}")

        # 验证教室存在
        classroom = await session.get(Classroom, schedule_data.classroom_id)
        if not classroom:
            logger.warning(f"教室不存在: classroom_id={schedule_data.classroom_id}")
            raise ClassroomNotFoundError(f"教室不存在: {schedule_data.classroom_id}")

        # 数据验证
        if schedule_data.start_time >= schedule_data.end_time:
            raise InvalidScheduleDataError("开始时间必须早于结束时间")

        if schedule_data.enrolled_count > schedule_data.max_students:
            raise InvalidScheduleDataError("已报名人数不能超过最大人数")

        # 检测时间冲突
        conflict_check = ScheduleConflictCheck(
            teacher_id=schedule_data.teacher_id,
            classroom_id=schedule_data.classroom_id,
            start_time=schedule_data.start_time,
            end_time=schedule_data.end_time
        )
        conflicts = await ScheduleService.check_conflicts(conflict_check, session)

        if conflicts.has_conflict:
            error_messages = []
            if conflicts.teacher_conflicts:
                error_messages.append(f"教师时间冲突: {conflicts.teacher_conflicts}")
            if conflicts.classroom_conflicts:
                error_messages.append(f"教室时间冲突: {conflicts.classroom_conflicts}")
            if conflicts.course_conflicts:
                error_messages.append(f"课程时间冲突: {conflicts.course_conflicts}")

            raise ScheduleConflictError(
                message="; ".join(error_messages),
                conflict_type="time_conflict",
                conflict_ids=conflicts.teacher_conflicts + conflicts.classroom_conflicts + conflicts.course_conflicts
            )

        # 生成循环ID（如果是循环排课）
        recurring_id = schedule_data.recurring_id
        if schedule_data.recurring_type and schedule_data.recurring_type != "single":
            if not recurring_id:
                recurring_id = str(uuid.uuid4())

        # 创建排课
        try:
            schedule = Schedule(
                course_id=schedule_data.course_id,
                teacher_id=schedule_data.teacher_id,
                classroom_id=schedule_data.classroom_id,
                department_id=schedule_data.department_id,
                start_time=schedule_data.start_time,
                end_time=schedule_data.end_time,
                week_day=schedule_data.week_day,
                recurring_type=schedule_data.recurring_type,
                recurring_id=recurring_id,
                max_students=schedule_data.max_students,
                enrolled_count=schedule_data.enrolled_count,
                status=1,  # 默认已安排
                notes=schedule_data.notes,
                created_by=created_by,
                created_at=datetime.now()
            )

            from app.crud.schedule import ScheduleCRUD

            return await ScheduleCRUD.create(schedule, session)

        except IntegrityError as e:
            logger.error(f"创建排课失败: {e}")
            await session.rollback()
            raise ScheduleServiceError(f"创建排课失败: {str(e)}")

    @staticmethod
    async def update_schedule(
        schedule_id: int,
        schedule_data: ScheduleUpdate,
        session: AsyncSession
    ) -> Schedule:
        """
        更新排课

        Args:
            schedule_id: 排课ID
            schedule_data: 排课更新数据
            session: 数据库会话

        Returns:
            Schedule: 更新后的排课对象

        Raises:
            ScheduleNotFoundError: 排课不存在
            CourseNotFoundError: 课程不存在
            TeacherNotFoundError: 教师不存在
            ClassroomNotFoundError: 教室不存在
            InvalidScheduleDataError: 数据验证失败
            ScheduleConflictError: 存在时间冲突
        """
        logger.info(f"更新排课: schedule_id={schedule_id}")

        # 获取排课
        schedule = await ScheduleService.get_schedule_by_id(schedule_id, session)

        # 验证课程存在（如果提供）
        if schedule_data.course_id is not None:
            course = await session.get(Course, schedule_data.course_id)
            if not course:
                logger.warning(f"课程不存在: course_id={schedule_data.course_id}")
                raise CourseNotFoundError(f"课程不存在: {schedule_data.course_id}")
            schedule.course_id = schedule_data.course_id

        # 验证教师存在（如果提供）
        if schedule_data.teacher_id is not None:
            teacher = await session.get(User, schedule_data.teacher_id)
            if not teacher:
                logger.warning(f"教师不存在: teacher_id={schedule_data.teacher_id}")
                raise TeacherNotFoundError(f"教师不存在: {schedule_data.teacher_id}")
            schedule.teacher_id = schedule_data.teacher_id

        # 验证教室存在（如果提供）
        if schedule_data.classroom_id is not None:
            classroom = await session.get(Classroom, schedule_data.classroom_id)
            if not classroom:
                logger.warning(f"教室不存在: classroom_id={schedule_data.classroom_id}")
                raise ClassroomNotFoundError(f"教室不存在: {schedule_data.classroom_id}")
            schedule.classroom_id = schedule_data.classroom_id

        # 更新字段
        if schedule_data.department_id is not None:
            schedule.department_id = schedule_data.department_id

        if schedule_data.start_time is not None:
            schedule.start_time = schedule_data.start_time

        if schedule_data.end_time is not None:
            schedule.end_time = schedule_data.end_time

        # 时间验证
        if schedule.start_time >= schedule.end_time:
            raise InvalidScheduleDataError("开始时间必须早于结束时间")

        if schedule_data.week_day is not None:
            schedule.week_day = schedule_data.week_day

        if schedule_data.recurring_type is not None:
            schedule.recurring_type = schedule_data.recurring_type

        if schedule_data.recurring_id is not None:
            schedule.recurring_id = schedule_data.recurring_id

        if schedule_data.max_students is not None:
            schedule.max_students = schedule_data.max_students

        if schedule_data.enrolled_count is not None:
            if schedule_data.enrolled_count > schedule.max_students:
                raise InvalidScheduleDataError("已报名人数不能超过最大人数")
            schedule.enrolled_count = schedule_data.enrolled_count

        if schedule_data.status is not None:
            schedule.status = schedule_data.status

        if schedule_data.notes is not None:
            schedule.notes = schedule_data.notes

        # 检测时间冲突
        conflict_check = ScheduleConflictCheck(
            teacher_id=schedule.teacher_id,
            classroom_id=schedule.classroom_id,
            start_time=schedule.start_time,
            end_time=schedule.end_time,
            exclude_schedule_id=schedule_id
        )
        conflicts = await ScheduleService.check_conflicts(conflict_check, session)

        if conflicts.has_conflict:
            error_messages = []
            if conflicts.teacher_conflicts:
                error_messages.append(f"教师时间冲突: {conflicts.teacher_conflicts}")
            if conflicts.classroom_conflicts:
                error_messages.append(f"教室时间冲突: {conflicts.classroom_conflicts}")
            if conflicts.course_conflicts:
                error_messages.append(f"课程时间冲突: {conflicts.course_conflicts}")

            raise ScheduleConflictError(
                message="; ".join(error_messages),
                conflict_type="time_conflict",
                conflict_ids=conflicts.teacher_conflicts + conflicts.classroom_conflicts + conflicts.course_conflicts
            )

        from app.crud.schedule import ScheduleCRUD

        try:
            return await ScheduleCRUD.update(schedule, session)
        except IntegrityError as e:
            logger.error(f"更新排课失败: {e}")
            await session.rollback()
            raise ScheduleServiceError(f"更新排课失败: {str(e)}")

    @staticmethod
    async def delete_schedule(schedule_id: int, session: AsyncSession) -> None:
        """
        删除排课

        Args:
            schedule_id: 排课ID
            session: 数据库会话

        Raises:
            ScheduleNotFoundError: 排课不存在
            ScheduleServiceError: 删除失败
        """
        logger.info(f"删除排课: schedule_id={schedule_id}")

        # 获取排课
        schedule = await ScheduleService.get_schedule_by_id(schedule_id, session)

        from app.crud.schedule import ScheduleCRUD

        try:
            await ScheduleCRUD.delete(schedule, session)
        except IntegrityError as e:
            logger.error(f"删除排课失败: {e}")
            await session.rollback()
            raise ScheduleServiceError(f"删除排课失败，可能存在关联数据")

    @staticmethod
    async def cancel_schedule(schedule_id: int, session: AsyncSession) -> Schedule:
        """
        取消排课

        Args:
            schedule_id: 排课ID
            session: 数据库会话

        Returns:
            Schedule: 更新后的排课对象

        Raises:
            ScheduleNotFoundError: 排课不存在
            InvalidScheduleStatusError: 排课状态不允许取消
        """
        logger.info(f"取消排课: schedule_id={schedule_id}")

        schedule = await ScheduleService.get_schedule_by_id(schedule_id, session)

        # 检查状态
        if schedule.status == 3:
            raise InvalidScheduleStatusError("排课已经是取消状态")

        if schedule.status == 2:
            raise InvalidScheduleStatusError("已上课的排课不能取消")

        # 更新状态为取消
        schedule.status = 3

        from app.crud.schedule import ScheduleCRUD

        return await ScheduleCRUD.update(schedule, session)

    # ==================== 冲突检测服务 ====================

    @staticmethod
    async def check_conflicts(
        conflict_check: ScheduleConflictCheck,
        session: AsyncSession
    ):
        """
        检测排课冲突

        Args:
            conflict_check: 冲突检测数据
            session: 数据库会话

        Returns:
            ScheduleConflictResponse: 冲突检测结果
        """
        from app.crud.schedule import ScheduleCRUD
        from app.schemas.schedule import ScheduleConflictResponse

        logger.info(f"检测排课冲突: teacher_id={conflict_check.teacher_id}, classroom_id={conflict_check.classroom_id}")

        teacher_conflicts = []
        classroom_conflicts = []
        course_conflicts = []

        # 检测教师时间冲突
        teacher_schedules = await ScheduleCRUD.get_by_teacher_and_time(
            teacher_id=conflict_check.teacher_id,
            start_time=conflict_check.start_time,
            end_time=conflict_check.end_time,
            session=session,
            exclude_schedule_id=conflict_check.exclude_schedule_id
        )
        teacher_conflicts = [s.id for s in teacher_schedules]

        # 检测教室时间冲突
        classroom_schedules = await ScheduleCRUD.get_by_classroom_and_time(
            classroom_id=conflict_check.classroom_id,
            start_time=conflict_check.start_time,
            end_time=conflict_check.end_time,
            session=session,
            exclude_schedule_id=conflict_check.exclude_schedule_id
        )
        classroom_conflicts = [s.id for s in classroom_schedules]

        # 如果有课程ID，检测课程时间冲突
        # （同一课程在同一时间段不能有多个排课）
        if hasattr(conflict_check, 'course_id') and conflict_check.course_id:
            course_schedules = await ScheduleCRUD.get_by_course_and_time(
                course_id=conflict_check.course_id,
                start_time=conflict_check.start_time,
                end_time=conflict_check.end_time,
                session=session,
                exclude_schedule_id=conflict_check.exclude_schedule_id
            )
            course_conflicts = [s.id for s in course_schedules]

        has_conflict = bool(teacher_conflicts or classroom_conflicts or course_conflicts)

        logger.info(f"冲突检测结果: has_conflict={has_conflict}")

        return ScheduleConflictResponse(
            has_conflict=has_conflict,
            teacher_conflicts=teacher_conflicts,
            classroom_conflicts=classroom_conflicts,
            course_conflicts=course_conflicts
        )

    # ==================== 报名管理服务 ====================

    @staticmethod
    async def enroll_student(
        schedule_id: int,
        enroll_data: ScheduleEnroll,
        session: AsyncSession
    ) -> Schedule:
        """
        学员报名

        Args:
            schedule_id: 排课ID
            enroll_data: 报名数据
            session: 数据库会话

        Returns:
            Schedule: 更新后的排课对象

        Raises:
            ScheduleNotFoundError: 排课不存在
            StudentNotFoundError: 学员不存在
            ScheduleCapacityError: 排课容量不足
            InvalidScheduleStatusError: 排课状态不允许报名
        """
        logger.info(f"学员报名: schedule_id={schedule_id}, student_id={enroll_data.student_id}")

        # 获取排课
        schedule = await ScheduleService.get_schedule_by_id(schedule_id, session)

        # 验证学员存在
        student = await session.get(Student, enroll_data.student_id)
        if not student:
            logger.warning(f"学员不存在: student_id={enroll_data.student_id}")
            raise StudentNotFoundError(f"学员不存在: {enroll_data.student_id}")

        # 检查排课状态
        if schedule.status != 1:
            raise InvalidScheduleStatusError(f"排课状态不允许报名: 当前状态={schedule.status}")

        # 检查容量
        if schedule.enrolled_count + enroll_data.count > schedule.max_students:
            raise ScheduleCapacityError(
                f"排课容量不足: 当前{schedule.enrolled_count}人，最大{schedule.max_students}人，报名{enroll_data.count}人"
            )

        # 更新报名人数
        schedule.enrolled_count += enroll_data.count

        from app.crud.schedule import ScheduleCRUD

        return await ScheduleCRUD.update(schedule, session)

    @staticmethod
    async def cancel_enrollment(
        schedule_id: int,
        student_id: int,
        session: AsyncSession,
        count: int = 1
    ) -> Schedule:
        """
        取消报名

        Args:
            schedule_id: 排课ID
            student_id: 学员ID
            count: 取消人数
            session: 数据库会话

        Returns:
            Schedule: 更新后的排课对象

        Raises:
            ScheduleNotFoundError: 排课不存在
            InvalidScheduleDataError: 取消人数超过已报名人数
            InvalidScheduleStatusError: 排课状态不允许取消报名
        """
        logger.info(f"取消报名: schedule_id={schedule_id}, student_id={student_id}, count={count}")

        # 获取排课
        schedule = await ScheduleService.get_schedule_by_id(schedule_id, session)

        # 检查排课状态
        if schedule.status != 1:
            raise InvalidScheduleStatusError(f"排课状态不允许取消报名: 当前状态={schedule.status}")

        # 检查取消人数
        if count > schedule.enrolled_count:
            raise InvalidScheduleDataError(
                f"取消人数超过已报名人数: 取消{count}人，已报名{schedule.enrolled_count}人"
            )

        # 更新报名人数
        schedule.enrolled_count -= count

        from app.crud.schedule import ScheduleCRUD

        return await ScheduleCRUD.update(schedule, session)

    # ==================== 循环排课支持 ====================

    @staticmethod
    async def create_recurring_schedules(
        base_schedule: ScheduleCreate,
        recurring_type: str,
        recurring_count: int,
        interval_days: int,
        created_by: Optional[int],
        session: AsyncSession
    ) -> List[Schedule]:
        """
        创建循环排课

        Args:
            base_schedule: 基础排课数据
            recurring_type: 循环类型 (weekly/biweekly)
            recurring_count: 循环次数
            interval_days: 间隔天数
            created_by: 创建人ID
            session: 数据库会话

        Returns:
            List[Schedule]: 创建的排课列表

        Raises:
            InvalidScheduleDataError: 数据验证失败
        """
        logger.info(f"创建循环排课: type={recurring_type}, count={recurring_count}")

        if recurring_type not in ["weekly", "biweekly"]:
            raise InvalidScheduleDataError(f"不支持的循环类型: {recurring_type}")

        if recurring_count < 2:
            raise InvalidScheduleDataError("循环次数必须大于1")

        # 生成循环ID
        recurring_id = str(uuid.uuid4())

        # 创建多个排课
        schedules = []
        for i in range(recurring_count):
            from datetime import timedelta

            # 计算新的开始和结束时间
            start_time = base_schedule.start_time + timedelta(days=i * interval_days)
            end_time = base_schedule.end_time + timedelta(days=i * interval_days)

            # 更新星期几
            week_day = start_time.isoweekday() if base_schedule.week_day else base_schedule.week_day

            schedule_data = ScheduleCreate(
                course_id=base_schedule.course_id,
                teacher_id=base_schedule.teacher_id,
                classroom_id=base_schedule.classroom_id,
                department_id=base_schedule.department_id,
                start_time=start_time,
                end_time=end_time,
                week_day=week_day,
                recurring_type=recurring_type,
                recurring_id=recurring_id,
                max_students=base_schedule.max_students,
                enrolled_count=base_schedule.enrolled_count,
                notes=base_schedule.notes
            )

            schedule = await ScheduleService.create_schedule(schedule_data, created_by, session)
            schedules.append(schedule)

        logger.info(f"循环排课创建成功: 创建{len(schedules)}个排课")
        return schedules


# 创建服务实例
schedule_service = ScheduleService()
