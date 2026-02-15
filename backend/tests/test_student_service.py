"""Student Service Tests

学员服务层测试
"""
import pytest
from datetime import date, datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate
from app.services.student_service import (
    StudentService,
    StudentNotFoundError,
    InvalidStudentDataError,
    StudentServiceError,
)


@pytest.mark.asyncio
async def test_create_student_success(db_session: AsyncSession):
    """测试成功创建学员"""
    student_data = StudentCreate(
        name="张三",
        nickname="小三",
        gender=1,
        birthday=date(2010, 1, 1),
        mobile="13800138000",
        parent_name="张父",
        parent_mobile="13900139000",
        source="线上推广",
        status=1
    )

    student = await StudentService.create_student(student_data, db_session)

    assert student.id is not None
    assert student.name == "张三"
    assert student.nickname == "小三"
    assert student.gender == 1
    assert student.mobile == "13800138000"
    assert student.status == 1
    assert student.created_at is not None
    assert student.updated_at is not None


@pytest.mark.asyncio
async def test_create_student_empty_name(db_session: AsyncSession):
    """测试创建学员时姓名为空"""
    student_data = StudentCreate(
        name=" ",  # 使用空格而非空字符串，让 Pydantic 通过
        mobile="13800138000"
    )

    with pytest.raises(InvalidStudentDataError, match="学员姓名不能为空"):
        await StudentService.create_student(student_data, db_session)


@pytest.mark.asyncio
async def test_create_student_invalid_mobile(db_session: AsyncSession):
    """测试创建学员时手机号格式不正确"""
    student_data = StudentCreate(
        name="张三",
        mobile="12345"
    )

    with pytest.raises(InvalidStudentDataError, match="手机号格式不正确"):
        await StudentService.create_student(student_data, db_session)


@pytest.mark.asyncio
async def test_get_student_by_id_success(db_session: AsyncSession):
    """测试成功获取学员详情"""
    # 先创建一个学员
    student_data = StudentCreate(
        name="李四",
        mobile="13800138001"
    )
    created_student = await StudentService.create_student(student_data, db_session)

    # 获取学员详情
    student = await StudentService.get_student_by_id(created_student.id, db_session)

    assert student.id == created_student.id
    assert student.name == "李四"


@pytest.mark.asyncio
async def test_get_student_by_id_not_found(db_session: AsyncSession):
    """测试获取不存在的学员"""
    with pytest.raises(StudentNotFoundError, match="学员不存在"):
        await StudentService.get_student_by_id(99999, db_session)


@pytest.mark.asyncio
async def test_update_student_success(db_session: AsyncSession):
    """测试成功更新学员"""
    # 先创建一个学员
    student_data = StudentCreate(
        name="王五",
        mobile="13800138002"
    )
    created_student = await StudentService.create_student(student_data, db_session)

    # 更新学员
    update_data = StudentUpdate(
        name="王五五",
        nickname="小五",
        status=2
    )
    updated_student = await StudentService.update_student(
        created_student.id, update_data, db_session
    )

    assert updated_student.name == "王五五"
    assert updated_student.nickname == "小五"
    assert updated_student.status == 2


@pytest.mark.asyncio
async def test_delete_student_success(db_session: AsyncSession):
    """测试成功删除学员"""
    # 先创建一个学员
    student_data = StudentCreate(
        name="赵六",
        mobile="13800138003"
    )
    created_student = await StudentService.create_student(student_data, db_session)

    # 删除学员
    await StudentService.delete_student(created_student.id, db_session)

    # 验证学员已被删除
    with pytest.raises(StudentNotFoundError):
        await StudentService.get_student_by_id(created_student.id, db_session)


@pytest.mark.asyncio
async def test_add_tag_to_student_success(db_session: AsyncSession):
    """测试成功为学员添加标签"""
    # 先创建一个学员
    student_data = StudentCreate(
        name="孙七",
        mobile="13800138004"
    )
    student = await StudentService.create_student(student_data, db_session)

    # 添加标签
    updated_student = await StudentService.add_tag_to_student(
        student.id, "VIP", db_session
    )

    assert updated_student.tags is not None
    assert "VIP" in updated_student.tags


@pytest.mark.asyncio
async def test_add_duplicate_tag_to_student(db_session: AsyncSession):
    """测试添加重复标签"""
    # 先创建一个学员
    student_data = StudentCreate(
        name="周八",
        mobile="13800138005"
    )
    student = await StudentService.create_student(student_data, db_session)

    # 添加标签
    await StudentService.add_tag_to_student(student.id, "VIP", db_session)
    # 再次添加相同标签
    await StudentService.add_tag_to_student(student.id, "VIP", db_session)

    # 验证标签不会重复
    updated_student = await StudentService.get_student_by_id(student.id, db_session)
    tags = eval(updated_student.tags) if updated_student.tags else []
    assert tags.count("VIP") == 1


@pytest.mark.asyncio
async def test_remove_tag_from_student_success(db_session: AsyncSession):
    """测试成功从学员移除标签"""
    # 先创建一个学员并添加标签
    student_data = StudentCreate(
        name="吴九",
        mobile="13800138006"
    )
    student = await StudentService.create_student(student_data, db_session)
    await StudentService.add_tag_to_student(student.id, "VIP", db_session)

    # 移除标签
    updated_student = await StudentService.remove_tag_from_student(
        student.id, "VIP", db_session
    )

    assert updated_student.tags is None or "VIP" not in updated_student.tags


@pytest.mark.asyncio
async def test_get_all_students_with_filters(db_session: AsyncSession):
    """测试获取学员列表并筛选"""
    # 创建多个学员
    for i in range(5):
        student_data = StudentCreate(
            name=f"学员{i}",
            mobile=f"1380013800{i}",
            status=1 if i % 2 == 0 else 2,
            source="线上推广" if i % 2 == 0 else "朋友介绍"
        )
        await StudentService.create_student(student_data, db_session)

    # 获取所有学员
    all_students = await StudentService.get_all_students(db_session)
    assert len(all_students) >= 5

    # 按状态筛选
    status_1_students = await StudentService.get_all_students(
        db_session, status=1
    )
    assert all(s.status == 1 for s in status_1_students)

    # 按来源筛选
    source_students = await StudentService.get_all_students(
        db_session, source="线上推广"
    )
    assert all(s.source == "线上推广" for s in source_students)


@pytest.mark.asyncio
async def test_search_students(db_session: AsyncSession):
    """测试搜索学员"""
    # 创建学员
    student_data = StudentCreate(
        name="测试学员",
        mobile="13800138007",
        parent_mobile="13900139007"
    )
    await StudentService.create_student(student_data, db_session)

    # 按姓名搜索
    results = await StudentService.search_students("测试", db_session)
    assert len(results) > 0
    assert any("测试" in s.name for s in results)

    # 按手机号搜索
    results = await StudentService.search_students("13800138007", db_session)
    assert len(results) > 0
    assert any(s.mobile == "13800138007" for s in results)


@pytest.mark.asyncio
async def test_update_student_status(db_session: AsyncSession):
    """测试更新学员状态"""
    # 先创建一个学员
    student_data = StudentCreate(
        name="郑十",
        mobile="13800138008",
        status=1
    )
    student = await StudentService.create_student(student_data, db_session)

    # 更新状态
    updated_student = await StudentService.update_student_status(
        student.id, 2, db_session
    )

    assert updated_student.status == 2


@pytest.mark.asyncio
async def test_count_students(db_session: AsyncSession):
    """测试统计学员数量"""
    # 创建学员
    for i in range(3):
        student_data = StudentCreate(
            name=f"统计学员{i}",
            mobile=f"1380013801{i}",
            status=1
        )
        await StudentService.create_student(student_data, db_session)

    # 统计总数
    count = await StudentService.count_students(db_session)
    assert count >= 3

    # 按状态统计
    status_1_count = await StudentService.count_students(db_session, status=1)
    assert status_1_count >= 3


@pytest.mark.asyncio
async def test_get_students_by_tag(db_session: AsyncSession):
    """测试根据标签获取学员"""
    # 创建学员并添加标签
    student_data = StudentCreate(
        name="标签学员",
        mobile="13800138009"
    )
    student = await StudentService.create_student(student_data, db_session)
    await StudentService.add_tag_to_student(student.id, "重点学员", db_session)

    # 获取带标签的学员
    tagged_students = await StudentService.get_students_by_tag(
        "重点学员", db_session
    )
    assert len(tagged_students) > 0
    assert any(s.id == student.id for s in tagged_students)


@pytest.mark.asyncio
async def test_get_all_tags(db_session: AsyncSession):
    """测试获取所有标签"""
    # 创建学员并添加不同标签
    tags = ["VIP", "重点学员", "潜力股"]
    mobile_numbers = ["13800138001", "13800138002", "13800138003"]
    for i, tag in enumerate(tags):
        student_data = StudentCreate(
            name=f"{tag}学员",
            mobile=mobile_numbers[i]
        )
        student = await StudentService.create_student(student_data, db_session)
        await StudentService.add_tag_to_student(student.id, tag, db_session)

    # 获取所有标签
    all_tags = await StudentService.get_all_tags(db_session)
    assert len(all_tags) >= 3
    assert all(tag in all_tags for tag in tags)
