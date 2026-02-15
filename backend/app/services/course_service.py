"""Course Business Logic Service

课程业务逻辑服务层

提供课程、教室、校区的业务逻辑处理，包括：
- 课程查询、创建、更新、删除
- 教室管理
- 校区管理
- 业务规则验证
"""
import logging
from datetime import datetime
from typing import List, Optional
from decimal import InvalidOperation, Decimal

from sqlalchemy import select, and_, or_, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.course import Course, Classroom, Department
from app.models.schedule import Schedule
from app.schemas.course import CourseCreate, CourseUpdate


logger = logging.getLogger(__name__)


class CourseServiceError(Exception):
    """课程服务异常基类"""
    pass


class CourseNotFoundError(CourseServiceError):
    """课程不存在异常"""
    pass


class ClassroomNotFoundError(CourseServiceError):
    """教室不存在异常"""
    pass


class DepartmentNotFoundError(CourseServiceError):
    """校区不存在异常"""
    pass


class CourseHasSchedulesError(CourseServiceError):
    """课程存在关联排课异常"""
    pass


class InvalidCourseDataError(CourseServiceError):
    """无效的课程数据异常"""
    pass


class CourseService:
    """课程业务服务类

    提供课程、教室、校区的完整业务逻辑处理
    所有方法都是异步的，需要传入 AsyncSession
    """

    # ==================== 课程查询服务 ====================

    @staticmethod
    async def get_all_courses(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        status: Optional[int] = None,
        search: Optional[str] = None
    ) -> List[Course]:
        """
        获取课程列表，支持分页和筛选

        Args:
            session: 数据库会话
            skip: 跳过记录数
            limit: 返回记录数
            category: 课程分类筛选
            status: 状态筛选 (1:上架 2:下架)
            search: 搜索关键词（名称或编码）

        Returns:
            List[Course]: 课程列表
        """
        logger.info(f"查询课程列表: skip={skip}, limit={limit}, category={category}, status={status}")

        query = select(Course)

        # 应用筛选条件
        conditions = []
        if category:
            conditions.append(Course.category == category)
        if status is not None:
            conditions.append(Course.status == status)
        if search:
            search_pattern = f"%{search}%"
            conditions.append(
                or_(
                    Course.name.ilike(search_pattern),
                    Course.code.ilike(search_pattern)
                )
            )

        if conditions:
            query = query.where(and_(*conditions))

        # 排序和分页
        query = query.order_by(Course.created_at.desc()).offset(skip).limit(limit)

        result = await session.execute(query)
        courses = result.scalars().all()

        logger.info(f"查询到 {len(courses)} 个课程")
        return courses

    @staticmethod
    async def get_course_by_id(course_id: int, session: AsyncSession) -> Course:
        """
        根据ID获取课程详情

        Args:
            course_id: 课程ID
            session: 数据库会话

        Returns:
            Course: 课程对象

        Raises:
            CourseNotFoundError: 课程不存在
        """
        logger.info(f"查询课程详情: course_id={course_id}")

        result = await session.execute(
            select(Course).where(Course.id == course_id)
        )
        course = result.scalar_one_or_none()

        if not course:
            logger.warning(f"课程不存在: course_id={course_id}")
            raise CourseNotFoundError(f"课程不存在: {course_id}")

        logger.info(f"查询到课程: {course.name}")
        return course

    @staticmethod
    async def search_courses(
        keyword: str,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[Course]:
        """
        按名称/分类搜索课程

        Args:
            keyword: 搜索关键词
            session: 数据库会话
            skip: 跳过记录数
            limit: 返回记录数

        Returns:
            List[Course]: 匹配的课程列表
        """
        logger.info(f"搜索课程: keyword={keyword}")

        search_pattern = f"%{keyword}%"
        query = select(Course).where(
            or_(
                Course.name.ilike(search_pattern),
                Course.code.ilike(search_pattern),
                Course.category.ilike(search_pattern),
                Course.description.ilike(search_pattern)
            )
        ).order_by(Course.created_at.desc()).offset(skip).limit(limit)

        result = await session.execute(query)
        courses = result.scalars().all()

        logger.info(f"搜索到 {len(courses)} 个课程")
        return courses

    @staticmethod
    async def count_courses(
        session: AsyncSession,
        category: Optional[str] = None,
        status: Optional[int] = None
    ) -> int:
        """
        统计课程数量

        Args:
            session: 数据库会话
            category: 课程分类筛选
            status: 状态筛选

        Returns:
            int: 课程总数
        """
        query = select(func.count(Course.id))

        conditions = []
        if category:
            conditions.append(Course.category == category)
        if status is not None:
            conditions.append(Course.status == status)

        if conditions:
            query = query.where(and_(*conditions))

        result = await session.execute(query)
        count = result.scalar()

        return count

    # ==================== 课程管理服务 ====================

    @staticmethod
    async def create_course(course_data: CourseCreate, session: AsyncSession) -> Course:
        """
        创建课程

        Args:
            course_data: 课程创建数据
            session: 数据库会话

        Returns:
            Course: 创建的课程对象

        Raises:
            InvalidCourseDataError: 数据验证失败
        """
        logger.info(f"创建课程: name={course_data.name}, code={course_data.code}")

        # 数据验证
        if not course_data.name or not course_data.name.strip():
            raise InvalidCourseDataError("课程名称不能为空")

        if not course_data.code or not course_data.code.strip():
            raise InvalidCourseDataError("课程编码不能为空")

        if course_data.duration <= 0:
            raise InvalidCourseDataError("课程时长必须大于0")

        if course_data.price < 0:
            raise InvalidCourseDataError("课程价格不能为负数")

        # 检查课程编码是否已存在
        existing = await session.execute(
            select(Course).where(Course.code == course_data.code)
        )
        if existing.scalar_one_or_none():
            raise InvalidCourseDataError(f"课程编码已存在: {course_data.code}")

        # 创建课程
        try:
            course = Course(
                name=course_data.name.strip(),
                code=course_data.code.strip(),
                description=course_data.description,
                duration=course_data.duration,
                price=Decimal(str(course_data.price)) if course_data.price else Decimal("0.00"),
                status=1  # 默认上架
            )
            session.add(course)
            await session.commit()
            await session.refresh(course)

            logger.info(f"课程创建成功: id={course.id}, name={course.name}")
            return course

        except (ValueError, InvalidOperation) as e:
            logger.error(f"创建课程失败: {e}")
            await session.rollback()
            raise InvalidCourseDataError(f"数据格式错误: {str(e)}")

    @staticmethod
    async def update_course(
        course_id: int,
        course_data: CourseUpdate,
        session: AsyncSession
    ) -> Course:
        """
        更新课程

        Args:
            course_id: 课程ID
            course_data: 课程更新数据
            session: 数据库会话

        Returns:
            Course: 更新后的课程对象

        Raises:
            CourseNotFoundError: 课程不存在
            InvalidCourseDataError: 数据验证失败
        """
        logger.info(f"更新课程: course_id={course_id}")

        # 获取课程
        course = await CourseService.get_course_by_id(course_id, session)

        # 验证更新数据
        if course_data.name is not None:
            if not course_data.name.strip():
                raise InvalidCourseDataError("课程名称不能为空")
            course.name = course_data.name.strip()

        if course_data.code is not None:
            if not course_data.code.strip():
                raise InvalidCourseDataError("课程编码不能为空")
            # 检查编码是否被其他课程使用
            existing = await session.execute(
                select(Course).where(
                    and_(
                        Course.code == course_data.code,
                        Course.id != course_id
                    )
                )
            )
            if existing.scalar_one_or_none():
                raise InvalidCourseDataError(f"课程编码已存在: {course_data.code}")
            course.code = course_data.code.strip()

        if course_data.duration is not None:
            if course_data.duration <= 0:
                raise InvalidCourseDataError("课程时长必须大于0")
            course.duration = course_data.duration

        if course_data.price is not None:
            if course_data.price < 0:
                raise InvalidCourseDataError("课程价格不能为负数")
            course.price = Decimal(str(course_data.price))

        if course_data.description is not None:
            course.description = course_data.description

        if course_data.is_active is not None:
            course.status = 1 if course_data.is_active else 2

        course.updated_at = datetime.now()

        try:
            await session.commit()
            await session.refresh(course)
            logger.info(f"课程更新成功: id={course.id}, name={course.name}")
            return course

        except (ValueError, InvalidOperation) as e:
            logger.error(f"更新课程失败: {e}")
            await session.rollback()
            raise InvalidCourseDataError(f"数据格式错误: {str(e)}")

    @staticmethod
    async def delete_course(course_id: int, session: AsyncSession) -> None:
        """
        删除课程

        删除前检查是否有关联的排课记录

        Args:
            course_id: 课程ID
            session: 数据库会话

        Raises:
            CourseNotFoundError: 课程不存在
            CourseHasSchedulesError: 课程存在关联排课
        """
        logger.info(f"删除课程: course_id={course_id}")

        # 验证课程存在
        await CourseService.get_course_by_id(course_id, session)

        # 检查是否有关联的排课
        schedule_result = await session.execute(
            select(func.count(Schedule.id)).where(Schedule.course_id == course_id)
        )
        schedule_count = schedule_result.scalar()

        if schedule_count > 0:
            logger.warning(f"课程存在 {schedule_count} 个排课记录，无法删除")
            raise CourseHasSchedulesError(
                f"课程存在 {schedule_count} 个排课记录，无法删除。请先删除相关排课。"
            )

        # 删除课程
        try:
            course = await session.get(Course, course_id)
            await session.delete(course)
            await session.commit()
            logger.info(f"课程删除成功: course_id={course_id}")

        except IntegrityError as e:
            logger.error(f"删除课程失败: {e}")
            await session.rollback()
            raise CourseServiceError(f"删除失败，可能存在其他关联数据")

    @staticmethod
    async def toggle_course_status(course_id: int, session: AsyncSession) -> Course:
        """
        切换课程上架/下架状态

        Args:
            course_id: 课程ID
            session: 数据库会话

        Returns:
            Course: 更新后的课程对象

        Raises:
            CourseNotFoundError: 课程不存在
        """
        logger.info(f"切换课程状态: course_id={course_id}")

        course = await CourseService.get_course_by_id(course_id, session)

        # 切换状态: 1(上架) <-> 2(下架)
        course.status = 2 if course.status == 1 else 1
        course.updated_at = datetime.now()

        await session.commit()
        await session.refresh(course)

        status_text = "上架" if course.status == 1 else "下架"
        logger.info(f"课程状态已切换: id={course.id}, status={status_text}")
        return course

    # ==================== 教室管理服务 ====================

    @staticmethod
    async def get_all_classrooms(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        department_id: Optional[int] = None,
        status: Optional[int] = None
    ) -> List[Classroom]:
        """
        获取教室列表

        Args:
            session: 数据库会话
            skip: 跳过记录数
            limit: 返回记录数
            department_id: 校区ID筛选
            status: 状态筛选

        Returns:
            List[Classroom]: 教室列表
        """
        logger.info(f"查询教室列表: skip={skip}, limit={limit}")

        query = select(Classroom)

        conditions = []
        if department_id:
            conditions.append(Classroom.department_id == department_id)
        if status is not None:
            conditions.append(Classroom.status == status)

        if conditions:
            query = query.where(and_(*conditions))

        query = query.order_by(Classroom.created_at.desc()).offset(skip).limit(limit)

        result = await session.execute(query)
        classrooms = result.scalars().all()

        logger.info(f"查询到 {len(classrooms)} 个教室")
        return classrooms

    @staticmethod
    async def get_classroom_by_id(classroom_id: int, session: AsyncSession) -> Classroom:
        """
        根据ID获取教室详情

        Args:
            classroom_id: 教室ID
            session: 数据库会话

        Returns:
            Classroom: 教室对象

        Raises:
            ClassroomNotFoundError: 教室不存在
        """
        logger.info(f"查询教室详情: classroom_id={classroom_id}")

        classroom = await session.get(Classroom, classroom_id)
        if not classroom:
            raise ClassroomNotFoundError(f"教室不存在: {classroom_id}")

        return classroom

    @staticmethod
    async def create_classroom(
        name: str,
        capacity: int,
        department_id: Optional[int],
        equipment: Optional[str],
        session: AsyncSession
    ) -> Classroom:
        """
        创建教室

        Args:
            name: 教室名称
            capacity: 容纳人数
            department_id: 所属校区
            equipment: 设备JSON数组
            session: 数据库会话

        Returns:
            Classroom: 创建的教室对象

        Raises:
            InvalidCourseDataError: 数据验证失败
            DepartmentNotFoundError: 校区不存在
        """
        logger.info(f"创建教室: name={name}, capacity={capacity}")

        # 数据验证
        if not name or not name.strip():
            raise InvalidCourseDataError("教室名称不能为空")

        if capacity <= 0:
            raise InvalidCourseDataError("教室容量必须大于0")

        # 验证校区存在
        if department_id:
            department = await session.get(Department, department_id)
            if not department:
                raise DepartmentNotFoundError(f"校区不存在: {department_id}")

        classroom = Classroom(
            name=name.strip(),
            capacity=capacity,
            department_id=department_id,
            equipment=equipment,
            status=1
        )
        session.add(classroom)
        await session.commit()
        await session.refresh(classroom)

        logger.info(f"教室创建成功: id={classroom.id}, name={classroom.name}")
        return classroom

    @staticmethod
    async def update_classroom(
        classroom_id: int,
        name: Optional[str],
        capacity: Optional[int],
        department_id: Optional[int],
        equipment: Optional[str],
        session: AsyncSession
    ) -> Classroom:
        """
        更新教室信息

        Args:
            classroom_id: 教室ID
            name: 教室名称
            capacity: 容纳人数
            department_id: 所属校区
            equipment: 设备JSON数组
            session: 数据库会话

        Returns:
            Classroom: 更新后的教室对象

        Raises:
            ClassroomNotFoundError: 教室不存在
            InvalidCourseDataError: 数据验证失败
        """
        logger.info(f"更新教室: classroom_id={classroom_id}")

        classroom = await CourseService.get_classroom_by_id(classroom_id, session)

        if name is not None:
            if not name.strip():
                raise InvalidCourseDataError("教室名称不能为空")
            classroom.name = name.strip()

        if capacity is not None:
            if capacity <= 0:
                raise InvalidCourseDataError("教室容量必须大于0")
            classroom.capacity = capacity

        if department_id is not None:
            # 验证校区存在
            department = await session.get(Department, department_id)
            if not department:
                raise DepartmentNotFoundError(f"校区不存在: {department_id}")
            classroom.department_id = department_id

        if equipment is not None:
            classroom.equipment = equipment

        await session.commit()
        await session.refresh(classroom)

        logger.info(f"教室更新成功: id={classroom.id}")
        return classroom

    @staticmethod
    async def delete_classroom(classroom_id: int, session: AsyncSession) -> None:
        """
        删除教室

        Args:
            classroom_id: 教室ID
            session: 数据库会话

        Raises:
            ClassroomNotFoundError: 教室不存在
            CourseServiceError: 删除失败（存在关联排课）
        """
        logger.info(f"删除教室: classroom_id={classroom_id}")

        # 验证教室存在
        await CourseService.get_classroom_by_id(classroom_id, session)

        # 检查是否有关联的排课
        schedule_result = await session.execute(
            select(func.count(Schedule.id)).where(Schedule.classroom_id == classroom_id)
        )
        schedule_count = schedule_result.scalar()

        if schedule_count > 0:
            logger.warning(f"教室存在 {schedule_count} 个排课记录，无法删除")
            raise CourseServiceError(
                f"教室存在 {schedule_count} 个排课记录，无法删除。请先删除相关排课。"
            )

        # 删除教室
        try:
            classroom = await session.get(Classroom, classroom_id)
            await session.delete(classroom)
            await session.commit()
            logger.info(f"教室删除成功: classroom_id={classroom_id}")

        except IntegrityError as e:
            logger.error(f"删除教室失败: {e}")
            await session.rollback()
            raise CourseServiceError(f"删除失败，可能存在其他关联数据")

    # ==================== 校区管理服务 ====================

    @staticmethod
    async def get_all_departments(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        status: Optional[int] = None
    ) -> List[Department]:
        """
        获取校区列表

        Args:
            session: 数据库会话
            skip: 跳过记录数
            limit: 返回记录数
            status: 状态筛选

        Returns:
            List[Department]: 校区列表
        """
        logger.info(f"查询校区列表: skip={skip}, limit={limit}")

        query = select(Department)

        if status is not None:
            query = query.where(Department.status == status)

        query = query.order_by(Department.created_at.desc()).offset(skip).limit(limit)

        result = await session.execute(query)
        departments = result.scalars().all()

        logger.info(f"查询到 {len(departments)} 个校区")
        return departments

    @staticmethod
    async def get_department_by_id(department_id: int, session: AsyncSession) -> Department:
        """
        根据ID获取校区详情

        Args:
            department_id: 校区ID
            session: 数据库会话

        Returns:
            Department: 校区对象

        Raises:
            DepartmentNotFoundError: 校区不存在
        """
        logger.info(f"查询校区详情: department_id={department_id}")

        department = await session.get(Department, department_id)
        if not department:
            raise DepartmentNotFoundError(f"校区不存在: {department_id}")

        return department

    @staticmethod
    async def create_department(
        name: str,
        parent_id: Optional[int],
        manager_id: Optional[int],
        address: Optional[str],
        contact: Optional[str],
        session: AsyncSession
    ) -> Department:
        """
        创建校区

        Args:
            name: 校区名称
            parent_id: 上级校区
            manager_id: 负责人
            address: 地址
            contact: 联系方式
            session: 数据库会话

        Returns:
            Department: 创建的校区对象

        Raises:
            InvalidCourseDataError: 数据验证失败
        """
        logger.info(f"创建校区: name={name}")

        # 数据验证
        if not name or not name.strip():
            raise InvalidCourseDataError("校区名称不能为空")

        # 检查名称是否已存在
        existing = await session.execute(
            select(Department).where(Department.name == name)
        )
        if existing.scalar_one_or_none():
            raise InvalidCourseDataError(f"校区名称已存在: {name}")

        department = Department(
            name=name.strip(),
            parent_id=parent_id,
            manager_id=manager_id,
            address=address,
            contact=contact,
            status=1
        )
        session.add(department)
        await session.commit()
        await session.refresh(department)

        logger.info(f"校区创建成功: id={department.id}, name={department.name}")
        return department

    @staticmethod
    async def update_department(
        department_id: int,
        name: Optional[str],
        parent_id: Optional[int],
        manager_id: Optional[int],
        address: Optional[str],
        contact: Optional[str],
        session: AsyncSession
    ) -> Department:
        """
        更新校区信息

        Args:
            department_id: 校区ID
            name: 校区名称
            parent_id: 上级校区
            manager_id: 负责人
            address: 地址
            contact: 联系方式
            session: 数据库会话

        Returns:
            Department: 更新后的校区对象

        Raises:
            DepartmentNotFoundError: 校区不存在
            InvalidCourseDataError: 数据验证失败
        """
        logger.info(f"更新校区: department_id={department_id}")

        department = await CourseService.get_department_by_id(department_id, session)

        if name is not None:
            if not name.strip():
                raise InvalidCourseDataError("校区名称不能为空")
            # 检查名称是否被其他校区使用
            existing = await session.execute(
                select(Department).where(
                    and_(
                        Department.name == name,
                        Department.id != department_id
                    )
                )
            )
            if existing.scalar_one_or_none():
                raise InvalidCourseDataError(f"校区名称已存在: {name}")
            department.name = name.strip()

        if parent_id is not None:
            # 验证上级校区存在
            if parent_id != department_id:
                parent = await session.get(Department, parent_id)
                if not parent:
                    raise DepartmentNotFoundError(f"上级校区不存在: {parent_id}")
                department.parent_id = parent_id

        if manager_id is not None:
            department.manager_id = manager_id

        if address is not None:
            department.address = address

        if contact is not None:
            department.contact = contact

        await session.commit()
        await session.refresh(department)

        logger.info(f"校区更新成功: id={department.id}")
        return department

    @staticmethod
    async def delete_department(department_id: int, session: AsyncSession) -> None:
        """
        删除校区

        Args:
            department_id: 校区ID
            session: 数据库会话

        Raises:
            DepartmentNotFoundError: 校区不存在
            CourseServiceError: 删除失败（存在关联数据）
        """
        logger.info(f"删除校区: department_id={department_id}")

        # 验证校区存在
        await CourseService.get_department_by_id(department_id, session)

        # 检查是否有关联的教室
        classroom_result = await session.execute(
            select(func.count(Classroom.id)).where(Classroom.department_id == department_id)
        )
        classroom_count = classroom_result.scalar()

        if classroom_count > 0:
            logger.warning(f"校区存在 {classroom_count} 个教室，无法删除")
            raise CourseServiceError(
                f"校区存在 {classroom_count} 个教室，无法删除。请先删除相关教室。"
            )

        # 检查是否存在下级校区
        child_result = await session.execute(
            select(func.count(Department.id)).where(Department.parent_id == department_id)
        )
        child_count = child_result.scalar()

        if child_count > 0:
            logger.warning(f"校区存在 {child_count} 个下级校区，无法删除")
            raise CourseServiceError(
                f"校区存在 {child_count} 个下级校区，无法删除。请先删除下级校区。"
            )

        # 删除校区
        try:
            department = await session.get(Department, department_id)
            await session.delete(department)
            await session.commit()
            logger.info(f"校区删除成功: department_id={department_id}")

        except IntegrityError as e:
            logger.error(f"删除校区失败: {e}")
            await session.rollback()
            raise CourseServiceError(f"删除失败，可能存在其他关联数据")


# 创建服务实例
course_service = CourseService()
