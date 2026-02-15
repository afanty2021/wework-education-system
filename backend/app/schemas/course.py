"""Course Pydantic Schemas

课程相关 Pydantic 模型
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class CourseBase(BaseModel):
    """课程基础模型"""
    name: str = Field(..., description="课程名称")
    description: Optional[str] = Field(None, description="课程描述")
    duration: int = Field(60, description="单节课时长(分钟)")
    price: Optional[Decimal] = Field(None, description="单价(元/课时)")


class CourseCreate(CourseBase):
    """课程创建模型"""
    code: str = Field(..., description="课程编码")
    category: Optional[str] = Field(None, description="课程分类")
    color: str = Field("#409EFF", description="显示颜色")
    max_students: int = Field(30, description="最大人数")


class CourseUpdate(BaseModel):
    """课程更新模型"""
    name: Optional[str] = Field(None, description="课程名称")
    code: Optional[str] = Field(None, description="课程编码")
    description: Optional[str] = Field(None, description="课程描述")
    duration: Optional[int] = Field(None, description="单节课时长(分钟)")
    price: Optional[Decimal] = Field(None, description="单价(元/课时)")
    category: Optional[str] = Field(None, description="课程分类")
    color: Optional[str] = Field(None, description="显示颜色")
    max_students: Optional[int] = Field(None, description="最大人数")
    status: Optional[int] = Field(None, description="状态: 1:上架 2:下架")


class CourseResponse(CourseBase):
    """课程响应模型"""
    id: int
    code: str
    category: Optional[str]
    color: str
    max_students: int
    status: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class ClassroomBase(BaseModel):
    """教室基础模型"""
    name: str = Field(..., description="教室名称")
    capacity: int = Field(30, description="容纳人数")
    department_id: Optional[int] = Field(None, description="所属校区")
    equipment: Optional[str] = Field(None, description="设备 JSON数组")


class ClassroomCreate(ClassroomBase):
    """教室创建模型"""
    pass


class ClassroomUpdate(BaseModel):
    """教室更新模型"""
    name: Optional[str] = Field(None, description="教室名称")
    capacity: Optional[int] = Field(None, description="容纳人数")
    department_id: Optional[int] = Field(None, description="所属校区")
    equipment: Optional[str] = Field(None, description="设备 JSON数组")
    status: Optional[int] = Field(None, description="状态: 1:可用 2:维护中")


class ClassroomResponse(ClassroomBase):
    """教室响应模型"""
    id: int
    status: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DepartmentBase(BaseModel):
    """校区基础模型"""
    name: str = Field(..., description="校区名称")
    parent_id: Optional[int] = Field(None, description="上级校区")
    manager_id: Optional[int] = Field(None, description="负责人")
    address: Optional[str] = Field(None, max_length=200, description="地址")
    contact: Optional[str] = Field(None, max_length=50, description="联系方式")


class DepartmentCreate(DepartmentBase):
    """校区创建模型"""
    pass


class DepartmentUpdate(BaseModel):
    """校区更新模型"""
    name: Optional[str] = Field(None, description="校区名称")
    parent_id: Optional[int] = Field(None, description="上级校区")
    manager_id: Optional[int] = Field(None, description="负责人")
    address: Optional[str] = Field(None, max_length=200, description="地址")
    contact: Optional[str] = Field(None, max_length=50, description="联系方式")
    status: Optional[int] = Field(None, description="状态")


class DepartmentResponse(DepartmentBase):
    """校区响应模型"""
    id: int
    status: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
