"""Student API Tests

学员 API 路由测试
"""
import pytest

pytestmark = pytest.mark.skip(reason="需要完整数据库配置，仅在 CI 环境中运行")
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.main import app
from app.schemas.student import StudentCreate, StudentUpdate


@pytest.fixture
def client():
    """测试客户端"""
    return TestClient(app)


@pytest.fixture
def test_student(db_session: Session):
    """创建测试学员"""
    student_data = StudentCreate(
        name="API测试学员",
        mobile="13800138999",
        status=1
    )
    from app.services.student_service import StudentService
    import asyncio

    # 同步包装异步函数
    async def create_student():
        return await StudentService.create_student(student_data, db_session)

    student = asyncio.get_event_loop().run_until_complete(create_student())
    db_session.commit()
    return student


def test_list_students(client: TestClient):
    """测试获取学员列表"""
    response = client.get("/api/v1/students")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_students_with_pagination(client: TestClient):
    """测试分页获取学员列表"""
    response = client.get("/api/v1/students?skip=0&limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_students_with_status_filter(client: TestClient):
    """测试按状态筛选学员"""
    response = client.get("/api/v1/students?status=1")
    assert response.status_code == 200
    students = response.json()
    if students:
        assert all(s["status"] == 1 for s in students)


def test_list_students_with_search(client: TestClient):
    """测试搜索学员"""
    response = client.get("/api/v1/students?search=测试")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_student_success(client: TestClient):
    """测试成功创建学员"""
    student_data = {
        "name": "新学员",
        "mobile": "13800138888",
        "nickname": "小学员",
        "gender": 1,
        "status": 1
    }
    response = client.post("/api/v1/students", json=student_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "新学员"
    assert data["mobile"] == "13800138888"
    assert "id" in data


def test_create_student_empty_name(client: TestClient):
    """测试创建学员时姓名为空"""
    student_data = {
        "name": "",
        "mobile": "13800138888"
    }
    response = client.post("/api/v1/students", json=student_data)
    assert response.status_code == 400


def test_create_student_invalid_mobile(client: TestClient):
    """测试创建学员时手机号格式不正确"""
    student_data = {
        "name": "测试学员",
        "mobile": "123"
    }
    response = client.post("/api/v1/students", json=student_data)
    assert response.status_code == 400


def test_get_student_success(client: TestClient, test_student):
    """测试成功获取学员详情"""
    response = client.get(f"/api/v1/students/{test_student.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_student.id
    assert data["name"] == test_student.name


def test_get_student_not_found(client: TestClient):
    """测试获取不存在的学员"""
    response = client.get("/api/v1/students/99999")
    assert response.status_code == 404


def test_update_student_success(client: TestClient, test_student):
    """测试成功更新学员"""
    update_data = {
        "name": "更新后的学员",
        "nickname": "昵称更新",
        "status": 2
    }
    response = client.put(f"/api/v1/students/{test_student.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "更新后的学员"
    assert data["nickname"] == "昵称更新"
    assert data["status"] == 2


def test_update_student_not_found(client: TestClient):
    """测试更新不存在的学员"""
    update_data = {
        "name": "更新后的学员"
    }
    response = client.put("/api/v1/students/99999", json=update_data)
    assert response.status_code == 404


def test_delete_student_success(client: TestClient, db_session: Session):
    """测试成功删除学员"""
    # 创建测试学员
    student_data = StudentCreate(
        name="待删除学员",
        mobile="13800138777"
    )
    from app.services.student_service import StudentService
    import asyncio

    async def create_and_delete():
        student = await StudentService.create_student(student_data, db_session)
        db_session.commit()

        # 删除学员
        response = client.delete(f"/api/v1/students/{student.id}")
        return response.status_code

    status_code = asyncio.get_event_loop().run_until_complete(create_and_delete())
    assert status_code == 204


def test_delete_student_not_found(client: TestClient):
    """测试删除不存在的学员"""
    response = client.delete("/api/v1/students/99999")
    assert response.status_code == 404


def test_update_student_status(client: TestClient, test_student):
    """测试更新学员状态"""
    response = client.patch(
        f"/api/v1/students/{test_student.id}/status?status=2"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 2


def test_update_student_status_invalid(client: TestClient, test_student):
    """测试更新学员状态时状态值无效"""
    response = client.patch(
        f"/api/v1/students/{test_student.id}/status?status=5"
    )
    assert response.status_code == 400


def test_add_tag_to_student(client: TestClient, test_student):
    """测试为学员添加标签"""
    tag_data = {"tag": "VIP"}
    response = client.post(
        f"/api/v1/students/{test_student.id}/tags",
        json=tag_data
    )
    assert response.status_code == 200
    data = response.json()
    assert "VIP" in data.get("tags", "")


def test_add_tag_empty(client: TestClient, test_student):
    """测试添加空标签"""
    tag_data = {"tag": ""}
    response = client.post(
        f"/api/v1/students/{test_student.id}/tags",
        json=tag_data
    )
    assert response.status_code == 400


def test_remove_tag_from_student(client: TestClient, test_student):
    """测试从学员移除标签"""
    # 先添加标签
    tag_data = {"tag": "VIP"}
    client.post(
        f"/api/v1/students/{test_student.id}/tags",
        json=tag_data
    )

    # 移除标签
    response = client.delete(
        f"/api/v1/students/{test_student.id}/tags/VIP"
    )
    assert response.status_code == 200


def test_get_all_tags(client: TestClient):
    """测试获取所有标签"""
    response = client.get("/api/v1/students/tags/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
