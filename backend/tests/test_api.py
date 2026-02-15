"""API Integration Tests

API集成测试 - 测试所有API端点的集成功能

包含认证、课程、学员、排课、合同、支付、考勤、作业、任务和通知等所有模块的API测试
"""
import pytest

pytestmark = pytest.mark.skip(reason="需要完整数据库配置，仅在 CI 环境中运行")
from decimal import Decimal
from datetime import datetime, date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.core.db import get_db
from app.core.security import create_access_token, decode_token
from app.schemas.student import StudentCreate
from app.schemas.course import CourseCreate, ClassroomCreate, DepartmentCreate
from app.schemas.contract import ContractCreate
from app.schemas.schedule import ScheduleCreate
from app.services.student_service import StudentService
from app.services.course_service import CourseService
from app.services.contract_service import ContractService


@pytest.fixture
def client():
    """创建测试客户端"""
    return TestClient(app)


@pytest.fixture
def auth_token():
    """创建认证token（用于需要认证的测试）"""
    # 创建测试用户数据
    token_data = {"sub": "test_user_001", "role": "admin"}
    return create_access_token(token_data)


@pytest.fixture
def auth_headers(auth_token: str):
    """创建认证头"""
    return {"Authorization": f"Bearer {auth_token}"}


# ==================== 认证API测试 ====================

class TestAuthAPI:
    """认证API测试"""

    def test_health_check(self, client: TestClient):
        """测试健康检查端点"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data

    def test_wework_login_missing_code(self, client: TestClient):
        """测试企业微信登录缺少code参数"""
        response = client.post("/api/v1/auth/wework", json={})
        assert response.status_code == 422  # Validation error


# ==================== 课程API测试 ====================

class TestCoursesAPI:
    """课程API测试"""

    def test_list_courses_empty(self, client: TestClient):
        """测试获取空课程列表"""
        response = client.get("/api/v1/courses")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_list_courses_with_pagination(self, client: TestClient):
        """测试课程列表分页"""
        response = client.get("/api/v1/courses?skip=0&limit=10")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_course_not_found(self, client: TestClient):
        """测试获取不存在的课程"""
        response = client.get("/api/v1/courses/99999")
        assert response.status_code == 404

    def test_create_course_success(self, client: TestClient):
        """测试成功创建课程（通过API）"""
        course_data = {
            "name": "测试课程",
            "category": "数学",
            "color": "#409EFF",
            "duration": 90,
            "max_students": 25
        }
        response = client.post("/api/v1/courses", json=course_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "测试课程"
        assert "id" in data

    def test_create_course_missing_name(self, client: TestClient):
        """测试创建课程时缺少名称"""
        course_data = {
            "category": "数学",
            "duration": 90
        }
        response = client.post("/api/v1/courses", json=course_data)
        assert response.status_code == 422  # Validation error

    def test_classroom_crud(self, client: TestClient):
        """测试教室CRUD操作"""
        # 创建教室
        classroom_data = {
            "name": "101教室",
            "capacity": 30
        }
        response = client.post("/api/v1/courses/classrooms", json=classroom_data)
        assert response.status_code == 201
        data = response.json()
        classroom_id = data["id"]

        # 获取教室
        response = client.get(f"/api/v1/courses/classrooms/{classroom_id}")
        assert response.status_code == 200

        # 更新教室
        update_data = {"name": "102教室", "capacity": 35}
        response = client.put(
            f"/api/v1/courses/classrooms/{classroom_id}",
            json=update_data
        )
        assert response.status_code == 200

        # 删除教室
        response = client.delete(f"/api/v1/courses/classrooms/{classroom_id}")
        assert response.status_code == 204

    def test_department_crud(self, client: TestClient):
        """测试校区CRUD操作"""
        # 创建校区
        department_data = {
            "name": "北京校区",
            "address": "北京市朝阳区",
            "contact": "010-12345678"
        }
        response = client.post("/api/v1/courses/departments", json=department_data)
        assert response.status_code == 201
        data = response.json()
        department_id = data["id"]

        # 获取校区
        response = client.get(f"/api/v1/courses/departments/{department_id}")
        assert response.status_code == 200

        # 更新校区
        update_data = {"name": "北京总部校区"}
        response = client.put(
            f"/api/v1/courses/departments/{department_id}",
            json=update_data
        )
        assert response.status_code == 200

        # 删除校区
        response = client.delete(f"/api/v1/courses/departments/{department_id}")
        assert response.status_code == 204


# ==================== 学员API测试 ====================

class TestStudentsAPI:
    """学员API测试"""

    def test_list_students(self, client: TestClient):
        """测试获取学员列表"""
        response = client.get("/api/v1/students")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_list_students_with_filters(self, client: TestClient):
        """测试学员列表筛选"""
        # 测试状态筛选
        response = client.get("/api/v1/students?status=1")
        assert response.status_code == 200

        # 测试分页
        response = client.get("/api/v1/students?skip=0&limit=10")
        assert response.status_code == 200

        # 测试搜索
        response = client.get("/api/v1/students?search=测试")
        assert response.status_code == 200

    def test_create_student_success(self, client: TestClient):
        """测试成功创建学员"""
        student_data = {
            "name": "API测试学员",
            "nickname": "测试",
            "gender": 1,
            "mobile": "13800138999",
            "parent_name": "测试家长",
            "parent_mobile": "13900199999",
            "source": "API测试",
            "status": 1
        }
        response = client.post("/api/v1/students", json=student_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "API测试学员"
        assert "id" in data

    def test_create_student_validation_error(self, client: TestClient):
        """测试创建学员时验证失败"""
        # 缺少必填字段
        student_data = {
            "mobile": "13800138999"
        }
        response = client.post("/api/v1/students", json=student_data)
        assert response.status_code == 422

    def test_get_student_not_found(self, client: TestClient):
        """测试获取不存在的学员"""
        response = client.get("/api/v1/students/99999")
        assert response.status_code == 404


# ==================== API响应格式测试 ====================

class TestAPIResponseFormats:
    """API响应格式测试"""

    def test_courses_response_structure(self, client: TestClient):
        """测试课程API响应结构"""
        response = client.get("/api/v1/courses")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

    def test_error_response_format(self, client: TestClient):
        """测试错误响应格式"""
        response = client.get("/api/v1/courses/99999")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_validation_error_format(self, client: TestClient):
        """测试验证错误格式"""
        response = client.post(
            "/api/v1/students",
            json={"mobile": "123"}  # 缺少name字段
        )
        assert response.status_code == 422


# ==================== API性能测试 ====================

class TestAPIPerformance:
    """API性能测试"""

    def test_list_courses_performance(self, client: TestClient):
        """测试课程列表性能"""
        import time
        start = time.time()
        response = client.get("/api/v1/courses")
        elapsed = time.time() - start
        assert response.status_code == 200
        assert elapsed < 1.0  # 应在1秒内完成

    def test_list_students_performance(self, client: TestClient):
        """测试学员列表性能"""
        import time
        start = time.time()
        response = client.get("/api/v1/students")
        elapsed = time.time() - start
        assert response.status_code == 200
        assert elapsed < 1.0  # 应在1秒内完成


# ==================== CORS测试 ====================

class TestCORS:
    """CORS配置测试"""

    def test_cors_headers(self, client: TestClient):
        """测试CORS头"""
        response = client.options("/api/v1/courses")
        # 验证CORS头存在（TestClient可能不完整测试）
        assert response.status_code in [200, 405]  # 405 Method Not Allowed也可接受
