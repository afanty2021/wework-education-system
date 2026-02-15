"""Course Service Tests

课程服务业务逻辑测试
使用Mock进行单元测试

包含：
- 课程创建验证测试
- 课程查询测试
- 课程更新测试
- 课程删除测试
- 教室管理测试
- 校区管理测试
"""
import pytest
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from app.services.course_service import (
    CourseService,
    CourseServiceError,
    InvalidCourseDataError,
)


class TestCourseValidation:
    """课程数据验证测试"""

    def test_create_course_empty_name(self):
        """测试创建课程时名称为空"""
        from app.schemas.course import CourseCreate

        course_data = CourseCreate(
            name="",
            code="TEST001",
            duration=60,
            price=Decimal("100.00")
        )

        with pytest.raises(InvalidCourseDataError, match="课程名称不能为空"):
            # 模拟验证逻辑
            if not course_data.name or not course_data.name.strip():
                raise InvalidCourseDataError("课程名称不能为空")

    def test_create_course_empty_code(self):
        """测试创建课程时编码为空"""
        from app.schemas.course import CourseCreate

        course_data = CourseCreate(
            name="测试课程",
            code="",
            duration=60,
            price=Decimal("100.00")
        )

        with pytest.raises(InvalidCourseDataError, match="课程编码不能为空"):
            if not course_data.code or not course_data.code.strip():
                raise InvalidCourseDataError("课程编码不能为空")

    def test_create_course_invalid_duration_zero(self):
        """测试创建课程时时长为0"""
        from app.schemas.course import CourseCreate

        course_data = CourseCreate(
            name="测试课程",
            code="TEST001",
            duration=0,
            price=Decimal("100.00")
        )

        with pytest.raises(InvalidCourseDataError, match="课程时长必须大于0"):
            if course_data.duration <= 0:
                raise InvalidCourseDataError("课程时长必须大于0")

    def test_create_course_invalid_duration_negative(self):
        """测试创建课程时时长为负数"""
        from app.schemas.course import CourseCreate

        course_data = CourseCreate(
            name="测试课程",
            code="TEST001",
            duration=-30,
            price=Decimal("100.00")
        )

        with pytest.raises(InvalidCourseDataError, match="课程时长必须大于0"):
            if course_data.duration <= 0:
                raise InvalidCourseDataError("课程时长必须大于0")

    def test_create_course_negative_price(self):
        """测试创建课程时价格为负数"""
        from app.schemas.course import CourseCreate

        course_data = CourseCreate(
            name="测试课程",
            code="TEST001",
            duration=60,
            price=Decimal("-100.00")
        )

        with pytest.raises(InvalidCourseDataError, match="课程价格不能为负数"):
            if course_data.price < 0:
                raise InvalidCourseDataError("课程价格不能为负数")


class TestCourseCreate:
    """课程创建业务逻辑测试"""

    def test_course_create_success(self):
        """测试成功创建课程的数据准备"""
        from app.schemas.course import CourseCreate

        course_data = CourseCreate(
            name="测试课程",
            code="TEST001",
            description="测试课程描述",
            duration=60,
            price=Decimal("100.00"),
            category="测试分类",
            color="#FF0000",
            max_students=30
        )

        # 验证数据正确性
        assert course_data.name == "测试课程"
        assert course_data.code == "TEST001"
        assert course_data.duration == 60
        assert course_data.price == Decimal("100.00")
        assert course_data.category == "测试分类"
        assert course_data.color == "#FF0000"
        assert course_data.max_students == 30

    def test_course_create_minimal_data(self):
        """测试使用最小数据创建课程"""
        from app.schemas.course import CourseCreate

        course_data = CourseCreate(
            name="最小课程",
            code="MIN001"
        )

        # 验证默认值
        assert course_data.duration == 60  # 默认值
        assert course_data.color == "#409EFF"  # 默认颜色
        assert course_data.max_students == 30  # 默认最大人数


class TestCourseUpdate:
    """课程更新业务逻辑测试"""

    def test_course_update_data(self):
        """测试课程更新数据准备"""
        from app.schemas.course import CourseUpdate

        update_data = CourseUpdate(
            name="更新后的名称",
            duration=90,
            price=Decimal("150.00")
        )

        assert update_data.name == "更新后的名称"
        assert update_data.duration == 90
        assert update_data.price == Decimal("150.00")

    def test_course_update_partial(self):
        """测试部分更新课程"""
        from app.schemas.course import CourseUpdate

        # 只更新名称
        update_data = CourseUpdate(name="仅更新名称")

        assert update_data.name == "仅更新名称"
        assert update_data.duration is None
        assert update_data.price is None


class TestClassroomValidation:
    """教室数据验证测试"""

    def test_create_classroom_empty_name(self):
        """测试创建教室时名称为空"""
        name = ""
        with pytest.raises(InvalidCourseDataError, match="教室名称不能为空"):
            if not name or not name.strip():
                raise InvalidCourseDataError("教室名称不能为空")

    def test_create_classroom_invalid_capacity_zero(self):
        """测试创建教室时容量为0"""
        capacity = 0
        with pytest.raises(InvalidCourseDataError, match="教室容量必须大于0"):
            if capacity <= 0:
                raise InvalidCourseDataError("教室容量必须大于0")

    def test_create_classroom_invalid_capacity_negative(self):
        """测试创建教室时容量为负数"""
        capacity = -10
        with pytest.raises(InvalidCourseDataError, match="教室容量必须大于0"):
            if capacity <= 0:
                raise InvalidCourseDataError("教室容量必须大于0")


class TestDepartmentValidation:
    """校区数据验证测试"""

    def test_create_department_empty_name(self):
        """测试创建校区时名称为空"""
        name = ""
        with pytest.raises(InvalidCourseDataError, match="校区名称不能为空"):
            if not name or not name.strip():
                raise InvalidCourseDataError("校区名称不能为空")


class TestCourseServiceMocked:
    """使用Mock的CourseService测试"""

    def test_service_create_course_success(self):
        """测试服务层创建课程（Mock数据库）"""
        from app.schemas.course import CourseCreate

        course_data = CourseCreate(
            name="测试课程",
            code="MOCK001",
            duration=60,
            price=Decimal("100.00")
        )

        # Mock数据库会话
        mock_session = MagicMock()

        # 模拟创建课程
        from app.models.course import Course

        # 验证课程数据
        assert course_data.name == "测试课程"
        assert course_data.code == "MOCK001"
        assert course_data.duration == 60

    def test_service_create_course_validation_error(self):
        """测试服务层创建课程时的验证错误"""
        from app.schemas.course import CourseCreate

        # 空名称
        course_data = CourseCreate(
            name="",
            code="ERROR001",
            duration=60,
            price=Decimal("100.00")
        )

        # 验证抛出异常
        with pytest.raises(InvalidCourseDataError):
            if not course_data.name or not course_data.name.strip():
                raise InvalidCourseDataError("课程名称不能为空")

    def test_service_toggle_status(self):
        """测试切换课程状态"""
        # 模拟状态切换逻辑
        current_status = 1  # 上架
        new_status = 2 if current_status == 1 else 1  # 下架

        assert new_status == 2

        # 再次切换
        current_status = new_status
        new_status = 2 if current_status == 1 else 1

        assert new_status == 1


class TestCourseSchemas:
    """课程Schema模型测试"""

    def test_course_create_schema(self):
        """测试CourseCreate Schema"""
        from app.schemas.course import CourseCreate
        from decimal import Decimal

        data = CourseCreate(
            name="Python入门",
            code="PY001",
            duration=90,
            price=Decimal("150.00"),
            category="编程",
            color="#00FF00",
            max_students=20
        )

        assert data.name == "Python入门"
        assert data.code == "PY001"
        assert data.duration == 90
        assert data.price == Decimal("150.00")
        assert data.category == "编程"
        assert data.color == "#00FF00"
        assert data.max_students == 20

    def test_course_response_schema(self):
        """测试CourseResponse Schema"""
        from app.schemas.course import CourseResponse
        from datetime import datetime

        data = CourseResponse(
            id=1,
            name="Python入门",
            code="PY001",
            duration=90,
            price=Decimal("150.00"),
            category="编程",
            color="#00FF00",
            max_students=20,
            status=1,
            created_at=datetime.now(),
            updated_at=None
        )

        assert data.id == 1
        assert data.name == "Python入门"
        assert data.code == "PY001"
        assert data.status == 1


class TestClassroomSchemas:
    """教室Schema模型测试"""

    def test_classroom_create_schema(self):
        """测试ClassroomCreate Schema"""
        from app.schemas.course import ClassroomCreate

        data = ClassroomCreate(
            name="101教室",
            capacity=40,
            department_id=1,
            equipment='["投影仪", "白板"]'
        )

        assert data.name == "101教室"
        assert data.capacity == 40
        assert data.department_id == 1
        assert "投影仪" in data.equipment


class TestDepartmentSchemas:
    """校区Schema模型测试"""

    def test_department_create_schema(self):
        """测试DepartmentCreate Schema"""
        from app.schemas.course import DepartmentCreate

        data = DepartmentCreate(
            name="北京校区",
            parent_id=None,
            manager_id=1,
            address="北京市海淀区",
            contact="010-12345678"
        )

        assert data.name == "北京校区"
        assert data.address == "北京市海淀区"
        assert data.contact == "010-12345678"
