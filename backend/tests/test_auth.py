"""Authentication Tests

认证模块测试
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    """测试健康检查接口"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_login_missing_credentials():
    """测试缺少凭据的登录"""
    response = client.post(
        "/api/v1/auth/token",
        data={"username": "", "password": ""},
    )
    assert response.status_code == 422  # Validation error
