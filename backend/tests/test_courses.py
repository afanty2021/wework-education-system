"""Courses Tests

课程模块测试
"""
import pytest

pytestmark = pytest.mark.skip(reason="需要完整数据库配置，仅在 CI 环境中运行")
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_list_courses():
    """测试获取课程列表"""
    response = client.get("/api/v1/courses")
    # TODO: 实现后返回实际数据
    assert response.status_code == 200


def test_create_course():
    """测试创建课程"""
    course_data = {
        "name": "Python编程入门",
        "code": "PYTHON-001",
        "description": "Python基础课程",
        "duration_minutes": 120,
        "price": 2999.00,
    }
    response = client.post("/api/v1/courses", json=course_data)
    # TODO: 实现后返回实际状态码
    assert response.status_code == 200
