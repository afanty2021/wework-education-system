"""Student Business Logic Service

学员业务逻辑服务层

提供学员的完整业务逻辑处理，包括：
- 学员查询、创建、更新、删除
- 学员标签管理
- 学员状态管理
- 业务规则验证
"""
import json
import logging
from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, and_, or_, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


logger = logging.getLogger(__name__)


class StudentServiceError(Exception):
    """学员服务异常基类"""
    pass


class StudentNotFoundError(StudentServiceError):
    """学员不存在异常"""
    pass


class InvalidStudentDataError(StudentServiceError):
    """无效的学员数据异常"""
    pass


class StudentService:
    """学员业务服务类

    提供学员的完整业务逻辑处理
    所有方法都是异步的，需要传入 AsyncSession
    """

    # ==================== 学员查询服务 ====================

    @staticmethod
    async def get_all_students(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        status: Optional[int] = None,
        source: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Student]:
        """
        获取学员列表，支持分页和筛选

        Args:
            session: 数据库会话
            skip: 跳过记录数
            limit: 返回记录数
            status: 状态筛选 (1:潜在 2:在读 3:已流失)
            source: 来源筛选
            search: 搜索关键词（姓名、手机号、家长手机号）

        Returns:
            List[Student]: 学员列表
        """
        logger.info(f"查询学员列表: skip={skip}, limit={limit}, status={status}, source={source}")

        query = select(Student)

        # 应用筛选条件
        conditions = []
        if status is not None:
            conditions.append(Student.status == status)
        if source:
            conditions.append(Student.source == source)
        if search:
            search_pattern = f"%{search}%"
            conditions.append(
                or_(
                    Student.name.ilike(search_pattern),
                    Student.mobile.ilike(search_pattern),
                    Student.parent_mobile.ilike(search_pattern),
                    Student.parent_name.ilike(search_pattern)
                )
            )

        if conditions:
            query = query.where(and_(*conditions))

        # 排序和分页
        query = query.order_by(Student.created_at.desc()).offset(skip).limit(limit)

        result = await session.execute(query)
        students = result.scalars().all()

        logger.info(f"查询到 {len(students)} 个学员")
        return students

    @staticmethod
    async def get_student_by_id(student_id: int, session: AsyncSession) -> Student:
        """
        根据ID获取学员详情

        Args:
            student_id: 学员ID
            session: 数据库会话

        Returns:
            Student: 学员对象

        Raises:
            StudentNotFoundError: 学员不存在
        """
        logger.info(f"查询学员详情: student_id={student_id}")

        result = await session.execute(
            select(Student).where(Student.id == student_id)
        )
        student = result.scalar_one_or_none()

        if not student:
            logger.warning(f"学员不存在: student_id={student_id}")
            raise StudentNotFoundError(f"学员不存在: {student_id}")

        logger.info(f"查询到学员: {student.name}")
        return student

    @staticmethod
    async def search_students(
        keyword: str,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[Student]:
        """
        按关键词搜索学员

        Args:
            keyword: 搜索关键词
            session: 数据库会话
            skip: 跳过记录数
            limit: 返回记录数

        Returns:
            List[Student]: 匹配的学员列表
        """
        logger.info(f"搜索学员: keyword={keyword}")

        search_pattern = f"%{keyword}%"
        query = select(Student).where(
            or_(
                Student.name.ilike(search_pattern),
                Student.nickname.ilike(search_pattern),
                Student.mobile.ilike(search_pattern),
                Student.parent_mobile.ilike(search_pattern),
                Student.parent_name.ilike(search_pattern),
                Student.notes.ilike(search_pattern)
            )
        ).order_by(Student.created_at.desc()).offset(skip).limit(limit)

        result = await session.execute(query)
        students = result.scalars().all()

        logger.info(f"搜索到 {len(students)} 个学员")
        return students

    @staticmethod
    async def count_students(
        session: AsyncSession,
        status: Optional[int] = None,
        source: Optional[str] = None
    ) -> int:
        """
        统计学员数量

        Args:
            session: 数据库会话
            status: 状态筛选
            source: 来源筛选

        Returns:
            int: 学员总数
        """
        query = select(func.count(Student.id))

        conditions = []
        if status is not None:
            conditions.append(Student.status == status)
        if source:
            conditions.append(Student.source == source)

        if conditions:
            query = query.where(and_(*conditions))

        result = await session.execute(query)
        count = result.scalar()

        return count

    @staticmethod
    async def get_students_by_tag(
        tag: str,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[Student]:
        """
        根据标签获取学员列表

        Args:
            tag: 标签名称
            session: 数据库会话
            skip: 跳过记录数
            limit: 返回记录数

        Returns:
            List[Student]: 学员列表
        """
        logger.info(f"查询标签学员: tag={tag}")

        # 使用 JSON 查询
        query = select(Student).where(
            Student.tags.ilike(f"%{tag}%")
        ).order_by(Student.created_at.desc()).offset(skip).limit(limit)

        result = await session.execute(query)
        students = result.scalars().all()

        logger.info(f"查询到 {len(students)} 个带标签 {tag} 的学员")
        return students

    # ==================== 学员管理服务 ====================

    @staticmethod
    async def create_student(student_data: StudentCreate, session: AsyncSession) -> Student:
        """
        创建学员

        Args:
            student_data: 学员创建数据
            session: 数据库会话

        Returns:
            Student: 创建的学员对象

        Raises:
            InvalidStudentDataError: 数据验证失败
        """
        logger.info(f"创建学员: name={student_data.name}, mobile={student_data.mobile}")

        # 数据验证
        if not student_data.name or not student_data.name.strip():
            raise InvalidStudentDataError("学员姓名不能为空")

        # 验证手机号格式（如果提供）
        if student_data.mobile:
            if not student_data.mobile.isdigit() or len(student_data.mobile) != 11:
                raise InvalidStudentDataError("手机号格式不正确")

        # 验证家长手机号格式（如果提供）
        if student_data.parent_mobile:
            if not student_data.parent_mobile.isdigit() or len(student_data.parent_mobile) != 11:
                raise InvalidStudentDataError("家长手机号格式不正确")

        # 验证性别
        if student_data.gender not in [None, 1, 2]:
            raise InvalidStudentDataError("性别值无效，必须是1（男）或2（女）")

        # 验证状态
        if student_data.status not in [1, 2, 3]:
            raise InvalidStudentDataError("状态值无效，必须是1（潜在）、2（在读）或3（已流失）")

        # 检查手机号是否已存在
        if student_data.mobile:
            existing = await session.execute(
                select(Student).where(Student.mobile == student_data.mobile)
            )
            if existing.scalar_one_or_none():
                raise InvalidStudentDataError(f"手机号已被使用: {student_data.mobile}")

        # 创建学员
        try:
            student = Student(
                name=student_data.name.strip(),
                nickname=student_data.nickname.strip() if student_data.nickname else None,
                gender=student_data.gender,
                birthday=student_data.birthday,
                mobile=student_data.mobile,
                parent_name=student_data.parent_name,
                parent_wework_id=student_data.parent_wework_id,
                parent_mobile=student_data.parent_mobile,
                source=student_data.source,
                status=student_data.status,
                tags=student_data.tags,
                notes=student_data.notes
            )
            session.add(student)
            await session.commit()
            await session.refresh(student)

            logger.info(f"学员创建成功: id={student.id}, name={student.name}")
            return student

        except IntegrityError as e:
            logger.error(f"创建学员失败: {e}")
            await session.rollback()
            raise InvalidStudentDataError(f"数据完整性错误: {str(e)}")

    @staticmethod
    async def update_student(
        student_id: int,
        student_data: StudentUpdate,
        session: AsyncSession
    ) -> Student:
        """
        更新学员

        Args:
            student_id: 学员ID
            student_data: 学员更新数据
            session: 数据库会话

        Returns:
            Student: 更新后的学员对象

        Raises:
            StudentNotFoundError: 学员不存在
            InvalidStudentDataError: 数据验证失败
        """
        logger.info(f"更新学员: student_id={student_id}")

        # 获取学员
        student = await StudentService.get_student_by_id(student_id, session)

        # 验证并更新字段
        if student_data.name is not None:
            if not student_data.name.strip():
                raise InvalidStudentDataError("学员姓名不能为空")
            student.name = student_data.name.strip()

        if student_data.nickname is not None:
            student.nickname = student_data.nickname.strip() if student_data.nickname else None

        if student_data.gender is not None:
            if student_data.gender not in [1, 2]:
                raise InvalidStudentDataError("性别值无效，必须是1（男）或2（女）")
            student.gender = student_data.gender

        if student_data.birthday is not None:
            student.birthday = student_data.birthday

        if student_data.mobile is not None:
            if student_data.mobile:
                if not student_data.mobile.isdigit() or len(student_data.mobile) != 11:
                    raise InvalidStudentDataError("手机号格式不正确")
                # 检查手机号是否被其他学员使用
                existing = await session.execute(
                    select(Student).where(
                        and_(
                            Student.mobile == student_data.mobile,
                            Student.id != student_id
                        )
                    )
                )
                if existing.scalar_one_or_none():
                    raise InvalidStudentDataError(f"手机号已被使用: {student_data.mobile}")
            student.mobile = student_data.mobile

        if student_data.parent_name is not None:
            student.parent_name = student_data.parent_name

        if student_data.parent_wework_id is not None:
            student.parent_wework_id = student_data.parent_wework_id

        if student_data.parent_mobile is not None:
            if student_data.parent_mobile:
                if not student_data.parent_mobile.isdigit() or len(student_data.parent_mobile) != 11:
                    raise InvalidStudentDataError("家长手机号格式不正确")
            student.parent_mobile = student_data.parent_mobile

        if student_data.source is not None:
            student.source = student_data.source

        if student_data.status is not None:
            if student_data.status not in [1, 2, 3]:
                raise InvalidStudentDataError("状态值无效，必须是1（潜在）、2（在读）或3（已流失）")
            student.status = student_data.status

        if student_data.tags is not None:
            student.tags = student_data.tags

        if student_data.notes is not None:
            student.notes = student_data.notes

        student.updated_at = datetime.now()

        try:
            await session.commit()
            await session.refresh(student)
            logger.info(f"学员更新成功: id={student.id}, name={student.name}")
            return student

        except IntegrityError as e:
            logger.error(f"更新学员失败: {e}")
            await session.rollback()
            raise InvalidStudentDataError(f"数据完整性错误: {str(e)}")

    @staticmethod
    async def delete_student(student_id: int, session: AsyncSession) -> None:
        """
        删除学员

        Args:
            student_id: 学员ID
            session: 数据库会话

        Raises:
            StudentNotFoundError: 学员不存在
            StudentServiceError: 删除失败（存在关联数据）
        """
        logger.info(f"删除学员: student_id={student_id}")

        # 验证学员存在
        await StudentService.get_student_by_id(student_id, session)

        # TODO: 检查是否有关联的合同、考勤等数据
        # for now, we'll allow deletion but this should be enhanced

        # 删除学员
        try:
            student = await session.get(Student, student_id)
            await session.delete(student)
            await session.commit()
            logger.info(f"学员删除成功: student_id={student_id}")

        except IntegrityError as e:
            logger.error(f"删除学员失败: {e}")
            await session.rollback()
            raise StudentServiceError(f"删除失败，可能存在关联数据（合同、考勤等）")

    @staticmethod
    async def update_student_status(
        student_id: int,
        status: int,
        session: AsyncSession
    ) -> Student:
        """
        更新学员状态

        Args:
            student_id: 学员ID
            status: 新状态 (1:潜在 2:在读 3:已流失)
            session: 数据库会话

        Returns:
            Student: 更新后的学员对象

        Raises:
            StudentNotFoundError: 学员不存在
            InvalidStudentDataError: 状态值无效
        """
        logger.info(f"更新学员状态: student_id={student_id}, status={status}")

        if status not in [1, 2, 3]:
            raise InvalidStudentDataError("状态值无效，必须是1（潜在）、2（在读）或3（已流失）")

        student = await StudentService.get_student_by_id(student_id, session)
        student.status = status
        student.updated_at = datetime.now()

        await session.commit()
        await session.refresh(student)

        status_text = {1: "潜在", 2: "在读", 3: "已流失"}[status]
        logger.info(f"学员状态已更新: id={student.id}, status={status_text}")
        return student

    # ==================== 标签管理服务 ====================

    @staticmethod
    async def add_tag_to_student(
        student_id: int,
        tag: str,
        session: AsyncSession
    ) -> Student:
        """
        为学员添加标签

        Args:
            student_id: 学员ID
            tag: 标签名称
            session: 数据库会话

        Returns:
            Student: 更新后的学员对象

        Raises:
            StudentNotFoundError: 学员不存在
            InvalidStudentDataError: 标签格式无效
        """
        logger.info(f"为学员添加标签: student_id={student_id}, tag={tag}")

        if not tag or not tag.strip():
            raise InvalidStudentDataError("标签不能为空")

        tag = tag.strip()

        student = await StudentService.get_student_by_id(student_id, session)

        # 解析现有标签
        try:
            tags = json.loads(student.tags) if student.tags else []
        except json.JSONDecodeError:
            tags = []

        # 添加新标签（如果不存在）
        if tag not in tags:
            tags.append(tag)
            student.tags = json.dumps(tags, ensure_ascii=False)
            student.updated_at = datetime.now()

            await session.commit()
            await session.refresh(student)

            logger.info(f"标签添加成功: student_id={student_id}, tag={tag}")
        else:
            logger.info(f"标签已存在: student_id={student_id}, tag={tag}")

        return student

    @staticmethod
    async def remove_tag_from_student(
        student_id: int,
        tag: str,
        session: AsyncSession
    ) -> Student:
        """
        从学员移除标签

        Args:
            student_id: 学员ID
            tag: 标签名称
            session: 数据库会话

        Returns:
            Student: 更新后的学员对象

        Raises:
            StudentNotFoundError: 学员不存在
        """
        logger.info(f"从学员移除标签: student_id={student_id}, tag={tag}")

        student = await StudentService.get_student_by_id(student_id, session)

        # 解析现有标签
        try:
            tags = json.loads(student.tags) if student.tags else []
        except json.JSONDecodeError:
            tags = []

        # 移除标签
        if tag in tags:
            tags.remove(tag)
            student.tags = json.dumps(tags, ensure_ascii=False) if tags else None
            student.updated_at = datetime.now()

            await session.commit()
            await session.refresh(student)

            logger.info(f"标签移除成功: student_id={student_id}, tag={tag}")
        else:
            logger.info(f"标签不存在: student_id={student_id}, tag={tag}")

        return student

    @staticmethod
    async def get_all_tags(session: AsyncSession) -> List[str]:
        """
        获取所有使用中的标签

        Args:
            session: 数据库会话

        Returns:
            List[str]: 标签列表
        """
        logger.info("查询所有标签")

        result = await session.execute(
            select(Student.tags).where(Student.tags.isnot(None))
        )
        tags_list = result.scalars().all()

        # 收集所有标签并去重
        all_tags = set()
        for tags_json in tags_list:
            try:
                tags = json.loads(tags_json)
                all_tags.update(tags)
            except (json.JSONDecodeError, TypeError):
                continue

        tags = sorted(list(all_tags))
        logger.info(f"查询到 {len(tags)} 个标签")
        return tags


# 创建服务实例
student_service = StudentService()
