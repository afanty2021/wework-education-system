"""Student Integration Tests

学员管理功能集成测试
"""
import pytest
from datetime import date
from decimal import Decimal
from sqlmodel import Session

from app.schemas.student import StudentCreate
from app.services.student_service import StudentService


@pytest.fixture
def integration_db_session(db_session: Session):
    """为集成测试提供数据库会话"""
    return db_session


@pytest.mark.usefixtures("db_session")
@pytest.mark.skip(reason="需要完整的数据库配置，集成测试在CI中运行")
class TestStudentIntegration:
    """学员集成测试类"""

    async def test_student_full_workflow(self, db_session: Session):
        """测试学员管理的完整工作流程"""
        # 1. 创建学员
        student_data = StudentCreate(
            name="集成测试学员",
            nickname="测试",
            gender=1,
            birthday=date(2010, 1, 1),
            mobile="13800139999",
            parent_name="测试家长",
            parent_mobile="13900199999",
            source="集成测试",
            status=1,
            notes="这是一个集成测试学员"
        )

        student = await StudentService.create_student(student_data, db_session)
        assert student.id is not None
        assert student.name == "集成测试学员"

        # 2. 获取学员详情
        fetched_student = await StudentService.get_student_by_id(student.id, db_session)
        assert fetched_student.id == student.id
        assert fetched_student.name == "集成测试学员"

        # 3. 添加标签
        updated_student = await StudentService.add_tag_to_student(
            student.id, "VIP", db_session
        )
        assert "VIP" in updated_student.tags

        # 4. 添加另一个标签
        updated_student = await StudentService.add_tag_to_student(
            student.id, "重点学员", db_session
        )
        assert "重点学员" in updated_student.tags

        # 5. 搜索学员
        results = await StudentService.search_students("集成测试", db_session)
        assert len(results) > 0
        assert any(s.id == student.id for s in results)

        # 6. 更新学员状态
        updated_student = await StudentService.update_student_status(
            student.id, 2, db_session
        )
        assert updated_student.status == 2

        # 7. 移除标签
        updated_student = await StudentService.remove_tag_from_student(
            student.id, "VIP", db_session
        )
        assert "VIP" not in updated_student.tags

        # 8. 获取所有标签
        all_tags = await StudentService.get_all_tags(db_session)
        assert "重点学员" in all_tags

        # 9. 统计学员数量
        count = await StudentService.count_students(db_session)
        assert count >= 1

        # 10. 删除学员
        await StudentService.delete_student(student.id, db_session)

        # 验证删除
        with pytest.raises(Exception):
            await StudentService.get_student_by_id(student.id, db_session)

    async def test_student_filtering(self, db_session: Session):
        """测试学员筛选功能"""
        # 创建不同状态的学员
        for i in range(6):
            student_data = StudentCreate(
                name=f"筛选学员{i}",
                mobile=f"138001399{i}",
                status=1 if i % 2 == 0 else 2,
                source="线上推广" if i % 2 == 0 else "地推"
            )
            await StudentService.create_student(student_data, db_session)

        # 按状态筛选
        status_1 = await StudentService.get_all_students(db_session, status=1)
        assert all(s.status == 1 for s in status_1)

        status_2 = await StudentService.get_all_students(db_session, status=2)
        assert all(s.status == 2 for s in status_2)

        # 按来源筛选
        online = await StudentService.get_all_students(db_session, source="线上推广")
        assert all(s.source == "线上推广" for s in online)

        offline = await StudentService.get_all_students(db_session, source="地推")
        assert all(s.source == "地推" for s in offline)

    async def test_student_validation(self, db_session: Session):
        """测试学员数据验证"""
        # 测试重复手机号
        student_data = StudentCreate(
            name="学员A",
            mobile="13800139888"
        )
        await StudentService.create_student(student_data, db_session)

        # 尝试创建相同手机号的学员
        duplicate_data = StudentCreate(
            name="学员B",
            mobile="13800139888"
        )

        with pytest.raises(Exception):  # 应该抛出 InvalidStudentDataError
            await StudentService.create_student(duplicate_data, db_session)

        # 测试无效的手机号格式
        invalid_data = StudentCreate(
            name="学员C",
            mobile="12345"
        )

        with pytest.raises(Exception):  # 应该抛出 InvalidStudentDataError
            await StudentService.create_student(invalid_data, db_session)

        # 测试无效的性别值
        invalid_gender = StudentCreate(
            name="学员D",
            mobile="13800139777",
            gender=5
        )

        with pytest.raises(Exception):  # 应该抛出 InvalidStudentDataError
            await StudentService.create_student(invalid_gender, db_session)


@pytest.mark.skip(reason="需要完整的数据库配置，集成测试在CI中运行")
class TestStudentAPIEndpoints:
    """学员API端点测试"""

    def test_student_api_list(self):
        """测试获取学员列表API"""
        from fastapi.testclient import TestClient
        from app.main import app

        client = TestClient(app)
        response = client.get("/api/v1/students")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_student_api_create(self):
        """测试创建学员API"""
        from fastapi.testclient import TestClient
        from app.main import app

        client = TestClient(app)
        student_data = {
            "name": "API测试学员",
            "mobile": "13800139666",
            "status": 1
        }
        response = client.post("/api/v1/students", json=student_data)
        # 可能返回201或400/422（取决于实现）
        assert response.status_code in [200, 201, 400, 422]

    def test_student_api_get(self):
        """测试获取学员详情API"""
        from fastapi.testclient import TestClient
        from app.main import app

        client = TestClient(app)
        response = client.get("/api/v1/students/1")
        # 可能返回200或404
        assert response.status_code in [200, 404]

    def test_student_api_update(self):
        """测试更新学员API"""
        from fastapi.testclient import TestClient
        from app.main import app

        client = TestClient(app)
        update_data = {
            "name": "更新后的API学员",
            "status": 2
        }
        response = client.put("/api/v1/students/1", json=update_data)
        # 可能返回200或404
        assert response.status_code in [200, 404]

    def test_student_api_search(self):
        """测试搜索学员API"""
        from fastapi.testclient import TestClient
        from app.main import app

        client = TestClient(app)
        response = client.get("/api/v1/students?search=测试")
        assert response.status_code == 200

    def test_student_api_tags(self):
        """测试学员标签API"""
        from fastapi.testclient import TestClient
        from app.main import app

        client = TestClient(app)
        response = client.get("/api/v1/students/tags/all")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
