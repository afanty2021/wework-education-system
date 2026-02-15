"""
课程相关模型

表: courses, classrooms, departments
"""

from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
from decimal import Decimal


class Course(SQLModel, table=True):
    """课程模型"""
    __tablename__ = "courses"

    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(max_length=20, unique=True, description="课程编码")
    name: str = Field(max_length=100, description="课程名称")
    category: Optional[str] = Field(default=None, max_length=50, description="课程分类")
    color: str = Field(default="#409EFF", max_length=10, description="显示颜色")
    duration: int = Field(default=60, description="单节课时长(分钟)")
    price: Optional[Decimal] = Field(default=None, description="单价(元/课时)")
    max_students: int = Field(default=30, description="最大人数")
    description: Optional[str] = Field(default=None, description="课程描述")
    status: int = Field(default=1, description="状态: 1:上架 2:下架")

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def __repr__(self):
        return f"<Course(id={self.id}, name='{self.name}')>"


class Classroom(SQLModel, table=True):
    """教室模型"""
    __tablename__ = "classrooms"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, description="教室名称")
    department_id: Optional[int] = Field(
        default=None,
        foreign_key="departments.id",
        description="所属校区"
    )
    capacity: int = Field(default=30, description="容纳人数")
    equipment: Optional[str] = Field(default=None, description="设备 JSON数组")
    status: int = Field(default=1, description="状态: 1:可用 2:维护中")

    created_at: datetime = Field(default_factory=datetime.now)

    def __repr__(self):
        return f"<Classroom(id={self.id}, name='{self.name}')>"


class Department(SQLModel, table=True):
    """校区/部门模型"""
    __tablename__ = "departments"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, description="校区名称")
    parent_id: Optional[int] = Field(default=None, description="上级校区")
    manager_id: Optional[int] = Field(default=None, description="负责人")
    address: Optional[str] = Field(default=None, max_length=200, description="地址")
    contact: Optional[str] = Field(default=None, max_length=50, description="联系方式")
    status: int = Field(default=1, description="状态")

    created_at: datetime = Field(default_factory=datetime.now)

    def __repr__(self):
        return f"<Department(id={self.id}, name='{self.name}')>"
