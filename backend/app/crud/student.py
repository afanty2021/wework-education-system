"""Student CRUD Operations

学员数据访问层

提供学员的基础 CRUD 操作
"""
import logging
from typing import List, Optional

from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.student import Student


logger = logging.getLogger(__name__)


class CRUDStudent:
    """学员数据访问类

    提供学员的基础数据访问操作
    更复杂的业务逻辑请使用 StudentService
    """

    @staticmethod
    async def get_all(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        status: Optional[int] = None,
        source: Optional[str] = None
    ) -> List[Student]:
        """
        获取所有学员

        Args:
            session: 数据库会话
            skip: 跳过记录数
            limit: 返回记录数
            status: 状态筛选
            source: 来源筛选

        Returns:
            List[Student]: 学员列表
        """
        query = select(Student)

        conditions = []
        if status is not None:
            conditions.append(Student.status == status)
        if source:
            conditions.append(Student.source == source)

        if conditions:
            query = query.where(and_(*conditions))

        query = query.order_by(Student.created_at.desc()).offset(skip).limit(limit)

        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_by_id(student_id: int, session: AsyncSession) -> Optional[Student]:
        """
        根据ID获取学员

        Args:
            student_id: 学员ID
            session: 数据库会话

        Returns:
            Optional[Student]: 学员对象，不存在则返回 None
        """
        return await session.get(Student, student_id)

    @staticmethod
    async def get_by_mobile(mobile: str, session: AsyncSession) -> Optional[Student]:
        """
        根据手机号获取学员

        Args:
            mobile: 手机号
            session: 数据库会话

        Returns:
            Optional[Student]: 学员对象，不存在则返回 None
        """
        result = await session.execute(
            select(Student).where(Student.mobile == mobile)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create(
        name: str,
        session: AsyncSession,
        nickname: Optional[str] = None,
        gender: Optional[int] = None,
        birthday: Optional = None,
        mobile: Optional[str] = None,
        parent_name: Optional[str] = None,
        parent_wework_id: Optional[str] = None,
        parent_mobile: Optional[str] = None,
        source: Optional[str] = None,
        status: int = 1,
        tags: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Student:
        """
        创建学员（基础操作，不包含业务逻辑验证）

        Args:
            name: 学员姓名
            session: 数据库会话
            nickname: 昵称
            gender: 性别
            birthday: 生日
            mobile: 手机号
            parent_name: 家长姓名
            parent_wework_id: 家长企业微信ID
            parent_mobile: 家长手机号
            source: 来源
            status: 状态
            tags: 标签
            notes: 备注

        Returns:
            Student: 创建的学员对象
        """
        student = Student(
            name=name,
            nickname=nickname,
            gender=gender,
            birthday=birthday,
            mobile=mobile,
            parent_name=parent_name,
            parent_wework_id=parent_wework_id,
            parent_mobile=parent_mobile,
            source=source,
            status=status,
            tags=tags,
            notes=notes
        )
        session.add(student)
        await session.commit()
        await session.refresh(student)
        return student

    @staticmethod
    async def update(
        student: Student,
        session: AsyncSession
    ) -> Student:
        """
        更新学员

        Args:
            student: 学员对象
            session: 数据库会话

        Returns:
            Student: 更新后的学员对象
        """
        await session.commit()
        await session.refresh(student)
        return student

    @staticmethod
    async def delete(student_id: int, session: AsyncSession) -> bool:
        """
        删除学员

        Args:
            student_id: 学员ID
            session: 数据库会话

        Returns:
            bool: 是否删除成功
        """
        student = await session.get(Student, student_id)
        if student:
            await session.delete(student)
            await session.commit()
            return True
        return False

    @staticmethod
    async def count(
        session: AsyncSession,
        status: Optional[int] = None
    ) -> int:
        """
        统计学员数量

        Args:
            session: 数据库会话
            status: 状态筛选

        Returns:
            int: 学员总数
        """
        from sqlalchemy import func

        query = select(func.count(Student.id))
        if status is not None:
            query = query.where(Student.status == status)

        result = await session.execute(query)
        return result.scalar()


# 创建实例
crud_student = CRUDStudent()
