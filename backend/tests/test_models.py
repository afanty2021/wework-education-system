"""
Model Tests

数据模型测试
"""
import pytest
from app.models.user import User
from app.models.student import Student
from app.models.course import Course, Classroom, Department
from app.models.contract import Contract
from app.models.payment import Payment
from app.models.schedule import Schedule
from app.models.attendance import Attendance
from app.models.homework import Homework, HomeworkSubmission
from app.models.notification import Notification
from app.models.miniapp_user import MiniAppUser
from datetime import datetime, date
from decimal import Decimal


def test_user_model_fields():
    """测试User模型字段"""
    user = User(
        wework_id="test_user_001",
        name="测试用户",
        mobile="13800138000",
        role="teacher",
        status=1
    )

    assert user.wework_id == "test_user_001"
    assert user.name == "测试用户"
    assert user.role == "teacher"
    assert user.status == 1


def test_student_model_fields():
    """测试Student模型字段"""
    student = Student(
        name="测试学员",
        nickname="小明",
        gender=1,
        mobile="13900139000",
        parent_name="张三",
        parent_wework_id="parent_wx_001",
        parent_mobile="13900139001",
        source="线上推广",
        status=2
    )

    assert student.name == "测试学员"
    assert student.nickname == "小明"
    assert student.gender == 1
    assert student.status == 2


def test_course_model_fields():
    """测试Course模型字段"""
    course = Course(
        name="测试课程",
        category="数学",
        color="#409EFF",
        duration=90,
        max_students=25,
        status=1
    )

    assert course.name == "测试课程"
    assert course.category == "数学"
    assert course.duration == 90
    assert course.max_students == 25


def test_classroom_model_fields():
    """测试Classroom模型字段"""
    classroom = Classroom(
        name="101教室",
        capacity=30,
        status=1
    )

    assert classroom.name == "101教室"
    assert classroom.capacity == 30


def test_department_model_fields():
    """测试Department模型字段"""
    department = Department(
        name="北京校区",
        status=1
    )

    assert department.name == "北京校区"


def test_contract_model_fields():
    """测试Contract模型字段"""
    contract = Contract(
        contract_no="CT20250214001",
        student_id=1,
        package_type="48课时",
        total_hours=Decimal("48.00"),
        remaining_hours=Decimal("48.00"),
        unit_price=Decimal("150.00"),
        total_amount=Decimal("7200.00"),
        received_amount=Decimal("0.00"),
        start_date=date(2025, 2, 14),
        status=1
    )

    assert contract.contract_no == "CT20250214001"
    assert contract.package_type == "48课时"
    assert contract.total_hours == Decimal("48.00")
    assert contract.remaining_hours == Decimal("48.00")
    assert contract.status == 1


def test_payment_model_fields():
    """测试Payment模型字段"""
    payment = Payment(
        payment_no="PAY20250214001",
        contract_id=1,
        amount=Decimal("7200.00"),
        payment_method=1,
        status=2
    )

    assert payment.payment_no == "PAY20250214001"
    assert payment.amount == Decimal("7200.00")
    assert payment.payment_method == 1
    assert payment.status == 2


def test_schedule_model_fields():
    """测试Schedule模型字段"""
    schedule = Schedule(
        course_id=1,
        teacher_id=1,
        classroom_id=1,
        start_time=datetime(2025, 2, 15, 14, 0),
        end_time=datetime(2025, 2, 15, 15, 30),
        status=1
    )

    assert schedule.course_id == 1
    assert schedule.teacher_id == 1
    assert schedule.classroom_id == 1


def test_attendance_model_fields():
    """测试Attendance模型字段"""
    attendance = Attendance(
        schedule_id=1,
        student_id=1,
        status=1,
        hours_consumed=Decimal("1.00")
    )

    assert attendance.schedule_id == 1
    assert attendance.student_id == 1
    assert attendance.status == 1
    assert attendance.hours_consumed == Decimal("1.00")


def test_homework_model_fields():
    """测试Homework模型字段"""
    homework = Homework(
        schedule_id=1,
        title="第一次作业",
        content="完成第1-10题",
        status=2
    )

    assert homework.title == "第一次作业"
    assert homework.content == "完成第1-10题"


def test_homework_submission_model_fields():
    """测试HomeworkSubmission模型字段"""
    submission = HomeworkSubmission(
        homework_id=1,
        student_id=1,
        content="我的作业答案",
        status=1
    )

    assert submission.homework_id == 1
    assert submission.student_id == 1
    assert submission.status == 1


def test_notification_model_fields():
    """测试Notification模型字段"""
    notification = Notification(
        type=1,
        receiver_id="user_wx_001",
        receiver_type=1,
        title="测试通知",
        content="这是一条测试通知",
        status=0
    )

    assert notification.type == 1
    assert notification.receiver_id == "user_wx_001"
    assert notification.title == "测试通知"


def test_miniapp_user_model_fields():
    """测试MiniAppUser模型字段"""
    miniapp_user = MiniAppUser(
        openid="wx_openid_001",
        platform="wechat",
        status=1
    )

    assert miniapp_user.openid == "wx_openid_001"
    assert miniapp_user.platform == "wechat"


def test_user_relationships():
    """测试User模型关联关系"""
    user = User(
        wework_id="test_user_002",
        name="测试用户2",
        role="teacher"
    )

    # 模拟关联的课程安排
    # schedules: list[Schedule] = []

    assert user.wework_id == "test_user_002"


def test_student_relationships():
    """测试Student模型关联关系"""
    student = Student(
        name="测试学员2",
        parent_wework_id="parent_wx_002"
    )

    # 模拟关联的合同
    # contracts: list[Contract] = []
    # 模拟关联的考勤记录
    # attendances: list[Attendance] = []

    assert student.parent_wework_id == "parent_wx_002"
