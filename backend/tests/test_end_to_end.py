"""End-to-End Business Workflow Tests

端到端业务流程测试 - 测试完整的业务场景

包含从学员注册到上课、考勤、作业提交等完整业务流程
"""
import pytest
from decimal import Decimal
from datetime import datetime, date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.student import StudentCreate
from app.schemas.course import CourseCreate, ClassroomCreate, DepartmentCreate
from app.schemas.contract import ContractCreate
from app.schemas.schedule import ScheduleCreate
from app.schemas.attendance import AttendanceCreate
from app.schemas.homework import HomeworkCreate, HomeworkSubmissionCreate
from app.services.student_service import StudentService
from app.services.course_service import CourseService
from app.services.contract_service import ContractService
from app.services.schedule_service import ScheduleService
from app.services.attendance_service import AttendanceService
from app.services.homework_service import HomeworkService


# ==================== 完整报名上课流程 ====================

@pytest.mark.asyncio
async def test_complete_enrollment_and_class_workflow(db_session: AsyncSession):
    """测试完整的学员报名上课流程

    流程步骤：
    1. 创建校区
    2. 创建教室
    3. 创建课程
    4. 创建学员
    5. 签订合同
    6. 安排排课
    7. 学员上课考勤
    8. 扣减课时
    9. 验证剩余课时
    """
    # 1. 创建校区
    department = await CourseService.create_department(
        name="北京校区",
        address="北京市朝阳区",
        session=db_session
    )
    await db_session.commit()
    assert department.id is not None
    print(f"✓ 创建校区: {department.name} (ID: {department.id})")

    # 2. 创建教室
    classroom = await CourseService.create_classroom(
        name="101教室",
        capacity=30,
        department_id=department.id,
        equipment="投影仪、白板",
        session=db_session
    )
    await db_session.commit()
    assert classroom.id is not None
    print(f"✓ 创建教室: {classroom.name} (ID: {classroom.id})")

    # 3. 创建课程
    course = await CourseService.create_course(
        course_data=CourseCreate(
            name="小学数学提高班",
            category="数学",
            color="#409EFF",
            description="适合3-5年级学生",
            duration=90,
            max_students=25
        ),
        session=db_session
    )
    await db_session.commit()
    assert course.id is not None
    print(f"✓ 创建课程: {course.name} (ID: {course.id})")

    # 4. 创建学员
    student = await StudentService.create_student(
        student_data=StudentCreate(
            name="张小明",
            nickname="小明",
            gender=1,
            birthday=date(2012, 5, 15),
            mobile="13800138001",
            parent_name="张爸爸",
            parent_wework_id="parent_wx_001",
            parent_mobile="13900139001",
            source="线上推广",
            status=2,  # 在读
            notes="数学基础较好"
        ),
        session=db_session
    )
    await db_session.commit()
    assert student.id is not None
    print(f"✓ 创建学员: {student.name} (ID: {student.id})")

    # 5. 签订合同
    contract = await ContractService.create_contract(
        contract_no="CT20250214001",
        student_id=student.id,
        course_id=course.id,
        package_type="48课时",
        total_hours=Decimal("48.00"),
        unit_price=Decimal("150.00"),
        total_amount=Decimal("7200.00"),
        discount_amount=Decimal("0.00"),
        received_amount=Decimal("7200.00"),
        start_date=date.today(),
        notes="家长通过微信支付",
        session=db_session
    )
    await db_session.commit()
    assert contract.id is not None
    assert contract.remaining_hours == Decimal("48.00")
    print(f"✓ 签订合同: {contract.contract_no} (课时: {contract.remaining_hours})")

    # 6. 安排排课
    tomorrow = date.today() + timedelta(days=1)
    schedule = await ScheduleService.create_schedule(
        schedule_data=ScheduleCreate(
            course_id=course.id,
            teacher_id=1,  # 假设教师ID为1
            classroom_id=classroom.id,
            start_time=datetime.combine(tomorrow, datetime.min.time(14, 0)),
            end_time=datetime.combine(tomorrow, datetime.min.time(15, 30)),
            max_students=25
        ),
        session=db_session
    )
    await db_session.commit()
    assert schedule.id is not None
    print(f"✓ 安排排课: {course.name} - {tomorrow} 14:00-15:30")

    # 7. 学员上课考勤
    attendance = await AttendanceService.create_attendance(
        attendence_data=AttendanceCreate(
            schedule_id=schedule.id,
            student_id=student.id,
            status=1,  # 出勤
            hours_consumed=Decimal("1.50")
        ),
        session=db_session
    )
    await db_session.commit()
    assert attendance.id is not None
    print(f"✓ 学员考勤: 出勤 (消耗课时: {attendance.hours_consumed})")

    # 8. 从合同扣减课时
    updated_contract = await ContractService.deduct_hours(
        contract_id=contract.id,
        hours=Decimal("1.50"),
        reason="正常上课",
        session=db_session
    )
    await db_session.commit()
    assert updated_contract.remaining_hours == Decimal("46.50")
    print(f"✓ 扣减课时: 剩余 {updated_contract.remaining_hours} 课时")

    # 9. 验证合同状态
    usage_percentage = ContractService.calculate_usage_percentage(
        contract_id=contract.id,
        session=db_session
    )
    assert usage_percentage > 0
    assert usage_percentage < 100
    print(f"✓ 课时使用率: {usage_percentage:.2f}%")

    print("\n✅ 完整报名上课流程测试通过！")


# ==================== 作业提交流程 ====================

@pytest.mark.asyncio
async def test_homework_submission_workflow(db_session: AsyncSession):
    """测试作业提交流程

    流程步骤：
    1. 创建课程和排课
    2. 教师发布作业
    3. 学员提交作业
    4. 教师批改作业
    """
    # 准备数据
    department = await CourseService.create_department(
        name="上海校区",
        session=db_session
    )
    await db_session.commit()

    classroom = await CourseService.create_classroom(
        name="201教室",
        capacity=25,
        department_id=department.id,
        session=db_session
    )
    await db_session.commit()

    course = await CourseService.create_course(
        course_data=CourseCreate(
            name="初中英语班",
            category="英语",
            duration=90,
            max_students=20
        ),
        session=db_session
    )
    await db_session.commit()

    student = await StudentService.create_student(
        student_data=StudentCreate(
            name="李小红",
            gender=2,
            mobile="13800138002"
        ),
        session=db_session
    )
    await db_session.commit()

    tomorrow = date.today() + timedelta(days=1)
    schedule = await ScheduleService.create_schedule(
        schedule_data=ScheduleCreate(
            course_id=course.id,
            teacher_id=1,
            classroom_id=classroom.id,
            start_time=datetime.combine(tomorrow, datetime.min.time(10, 0)),
            end_time=datetime.combine(tomorrow, datetime.min.time(11, 30))
        ),
        session=db_session
    )
    await db_session.commit()

    # 1. 教师发布作业
    homework = await HomeworkService.create_homework(
        homework_data=HomeworkCreate(
            schedule_id=schedule.id,
            title="第一单元单词练习",
            content="完成教材P20-25的单词填空",
            due_date=tomorrow + timedelta(days=7),
            status=1  # 已发布
        ),
        session=db_session
    )
    await db_session.commit()
    assert homework.id is not None
    print(f"✓ 发布作业: {homework.title}")

    # 2. 学员提交作业
    submission = await HomeworkService.create_submission(
        submission_data=HomeworkSubmissionCreate(
            homework_id=homework.id,
            student_id=student.id,
            content="我的作业答案：1.A 2.B 3.C...",
            attachments=None
        ),
        session=db_session
    )
    await db_session.commit()
    assert submission.id is not None
    print(f"✓ 学员提交作业")

    # 3. 教师批改作业
    graded_submission = await HomeworkService.grade_submission(
        submission_id=submission.id,
        score=95,
        comment="完成得很好，继续保持！",
        session=db_session
    )
    await db_session.commit()
    assert graded_submission.score == 95
    assert graded_submission.status == 2  # 已批改
    print(f"✓ 教师批改作业: {graded_submission.score}分")

    print("\n✅ 作业提交流程测试通过！")


# ==================== 课时预警流程 ====================

@pytest.mark.asyncio
async def test_contract_expiry_warning_workflow(db_session: AsyncSession):
    """测试合同到期预警流程

    流程步骤：
    1. 创建剩余课时较少的合同
    2. 检查即将到期合同
    3. 验证预警功能
    """
    # 准备数据
    course = await CourseService.create_course(
        course_data=CourseCreate(
            name="物理提高班",
            category="物理",
            duration=90,
            max_students=20
        ),
        session=db_session
    )
    await db_session.commit()

    student = await StudentService.create_student(
        student_data=StudentCreate(
            name="王大明",
            gender=1,
            mobile="13800138003"
        ),
        session=db_session
    )
    await db_session.commit()

    # 创建剩余5课时的合同
    contract = await ContractService.create_contract(
        contract_no="CT20250214002",
        student_id=student.id,
        course_id=course.id,
        package_type="48课时",
        total_hours=Decimal("48.00"),
        unit_price=Decimal("150.00"),
        total_amount=Decimal("7200.00"),
        received_amount=Decimal("7200.00"),
        start_date=date.today() - timedelta(days=180),  # 6个月前开始
        notes="已使用43课时",
        session=db_session
    )
    await db_session.commit()

    # 扣减部分课时，剩余5课时
    await ContractService.deduct_hours(
        contract_id=contract.id,
        hours=Decimal("43.00"),
        session=db_session
    )
    await db_session.commit()

    # 检查即将到期合同（剩余<=10课时）
    expiring_contracts = await ContractService.check_expiry(
        warning_threshold=10,
        session=db_session
    )

    assert len(expiring_contracts) > 0
    assert any(c.id == contract.id for c in expiring_contracts)
    print(f"✓ 检测到 {len(expiring_contracts)} 个即将到期合同")

    # 计算剩余价值
    remaining_value = ContractService.calculate_remaining_value(
        contract_id=contract.id,
        session=db_session
    )
    assert remaining_value == Decimal("750.00")  # 5课时 × 150元
    print(f"✓ 剩余课时价值: ¥{remaining_value}")

    print("\n✅ 合同到期预警流程测试通过！")


# ==================== 多学员排课流程 ====================

@pytest.mark.asyncio
async def test_multiple_students_class_workflow(db_session: AsyncSession):
    """测试多学员排课流程

    流程步骤：
    1. 创建课程和排课
    2. 创建多个学员
    3. 为所有学员进行考勤
    4. 验证考勤记录
    """
    # 准备数据
    department = await CourseService.create_department(
        name="广州校区",
        session=db_session
    )
    await db_session.commit()

    classroom = await CourseService.create_classroom(
        name="301教室",
        capacity=30,
        department_id=department.id,
        session=db_session
    )
    await db_session.commit()

    course = await CourseService.create_course(
        course_data=CourseCreate(
            name="编程入门班",
            category="编程",
            duration=120,
            max_students=30
        ),
        session=db_session
    )
    await db_session.commit()

    tomorrow = date.today() + timedelta(days=1)
    schedule = await ScheduleService.create_schedule(
        schedule_data=ScheduleCreate(
            course_id=course.id,
            teacher_id=1,
            classroom_id=classroom.id,
            start_time=datetime.combine(tomorrow, datetime.min.time(9, 0)),
            end_time=datetime.combine(tomorrow, datetime.min.time(11, 0)),
            max_students=30
        ),
        session=db_session
    )
    await db_session.commit()

    # 创建5个学员
    students = []
    for i in range(1, 6):
        student = await StudentService.create_student(
            student_data=StudentCreate(
                name=f"学员{i:02d}",
                mobile=f"1380013800{i}",
                status=2
            ),
            session=db_session
        )
        students.append(student)
        await db_session.commit()
    print(f"✓ 创建了 {len(students)} 个学员")

    # 为所有学员进行考勤
    attendances = []
    for student in students:
        attendance = await AttendanceService.create_attendance(
            attendence_data=AttendanceCreate(
                schedule_id=schedule.id,
                student_id=student.id,
                status=1,  # 全部出勤
                hours_consumed=Decimal("2.00")
            ),
            session=db_session
        )
        attendances.append(attendance)
        await db_session.commit()
    print(f"✓ 创建了 {len(attendances)} 条考勤记录")

    # 验证考勤记录
    schedule_attendances = await AttendanceService.get_attendances_by_schedule(
        schedule_id=schedule.id,
        session=db_session
    )
    assert len(schedule_attendances) == 5
    assert all(a.status == 1 for a in schedule_attendances)
    print(f"✓ 验证考勤: {len(schedule_attendances)} 人出勤")

    print("\n✅ 多学员排课流程测试通过！")


# ==================== 学员状态变更流程 ====================

@pytest.mark.asyncio
async def test_student_status_change_workflow(db_session: AsyncSession):
    """测试学员状态变更流程

    流程步骤：
    1. 创建潜在学员
    2. 转为在读学员（签合同）
    3. 变为已流失学员
    """
    # 1. 创建潜在学员
    student = await StudentService.create_student(
        student_data=StudentCreate(
            name="赵小刚",
            gender=1,
            mobile="13800138004",
            status=1,  # 潜在
            source="地推",
            notes="家长还在考虑"
        ),
        session=db_session
    )
    await db_session.commit()
    assert student.status == 1
    print(f"✓ 创建潜在学员: {student.name}")

    # 2. 签订合同，转为在读
    course = await CourseService.create_course(
        course_data=CourseCreate(
            name="化学基础班",
            category="化学",
            duration=90,
            max_students=25
        ),
        session=db_session
    )
    await db_session.commit()

    contract = await ContractService.create_contract(
        contract_no="CT20250214003",
        student_id=student.id,
        course_id=course.id,
        package_type="24课时",
        total_hours=Decimal("24.00"),
        unit_price=Decimal("150.00"),
        total_amount=Decimal("3600.00"),
        start_date=date.today(),
        session=db_session
    )
    await db_session.commit()

    # 更新学员状态为在读
    updated_student = await StudentService.update_student_status(
        student_id=student.id,
        status=2,
        session=db_session
    )
    await db_session.commit()
    assert updated_student.status == 2
    print(f"✓ 学员状态更新为: 在读")

    # 3. 所有课时使用完毕，转为已流失
    await ContractService.deduct_hours(
        contract_id=contract.id,
        hours=Decimal("24.00"),
        session=db_session
    )
    await db_session.commit()

    # 标记为已流失
    lost_student = await StudentService.update_student_status(
        student_id=student.id,
        status=3,
        session=db_session
    )
    await db_session.commit()
    assert lost_student.status == 3
    print(f"✓ 学员状态更新为: 已流失")

    print("\n✅ 学员状态变更流程测试通过！")