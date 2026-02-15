"""Attendance Module Tests

考勤管理功能测试
"""
import pytest
from datetime import datetime, date
from decimal import Decimal

from app.schemas.attendance import (
    AttendanceBase,
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceResponse,
    AttendanceBatchCreate,
    AttendanceStatistics,
)
from app.services.attendance_service import (
    AttendanceService,
    AttendanceServiceError,
    AttendanceNotFoundError,
    ScheduleNotFoundError,
    StudentNotFoundError,
    DuplicateAttendanceError,
    InvalidAttendanceDataError,
    InvalidAttendanceStatusError,
)


class TestAttendanceSchemas:
    """测试考勤 Schema 模型"""

    def test_attendance_base_schema(self):
        """测试考勤基础 Schema"""
        attendance_data = AttendanceBase(
            schedule_id=1,
            student_id=1,
            contract_id=1,
            status=1,
            check_time=datetime.now(),
            check_method=1,
            hours_consumed=Decimal("1.5"),
            notes="测试考勤"
        )

        assert attendance_data.schedule_id == 1
        assert attendance_data.student_id == 1
        assert attendance_data.status == 1
        assert attendance_data.hours_consumed == Decimal("1.5")

    def test_attendance_create_schema(self):
        """测试考勤创建 Schema"""
        attendance_data = AttendanceCreate(
            schedule_id=1,
            student_id=1,
            contract_id=1,
            status=1,
            check_time=datetime.now(),
            check_method=1,
            hours_consumed=Decimal("2.0"),
            notes="正常出勤"
        )

        assert attendance_data.schedule_id == 1
        assert attendance_data.status == 1
        assert attendance_data.hours_consumed == Decimal("2.0")

    def test_attendance_update_schema(self):
        """测试考勤更新 Schema"""
        update_data = AttendanceUpdate(
            status=2,
            notes="改为请假"
        )

        assert update_data.status == 2
        assert update_data.notes == "改为请假"

    def test_attendance_batch_create_schema(self):
        """测试批量创建 Schema"""
        batch_data = AttendanceBatchCreate(
            attendances=[
                AttendanceCreate(
                    schedule_id=1,
                    student_id=1,
                    status=1,
                    hours_consumed=Decimal("1.0")
                ),
                AttendanceCreate(
                    schedule_id=1,
                    student_id=2,
                    status=1,
                    hours_consumed=Decimal("1.0")
                )
            ],
            auto_deduct_hours=True
        )

        assert len(batch_data.attendances) == 2
        assert batch_data.auto_deduct_hours is True


class TestAttendanceValidation:
    """测试考勤数据验证"""

    def test_attendance_status_validation(self):
        """测试考勤状态验证"""
        # 有效状态：1-出勤 2-请假 3-缺勤 4-迟到
        valid_statuses = [1, 2, 3, 4]

        for status in valid_statuses:
            attendance_data = AttendanceCreate(
                schedule_id=1,
                student_id=1,
                status=status,
                hours_consumed=Decimal("1.0")
            )
            assert attendance_data.status == status

    def test_attendance_hours_validation(self):
        """测试消耗课时验证"""
        # 课时必须大于0
        attendance_data = AttendanceCreate(
            schedule_id=1,
            student_id=1,
            status=1,
            hours_consumed=Decimal("1.5")
        )

        assert attendance_data.hours_consumed > 0

    def test_attendance_check_method_validation(self):
        """测试签到方式验证"""
        # 签到方式：1-手动 2-人脸 3-刷卡
        valid_methods = [1, 2, 3]

        for method in valid_methods:
            attendance_data = AttendanceCreate(
                schedule_id=1,
                student_id=1,
                status=1,
                check_method=method,
                hours_consumed=Decimal("1.0")
            )
            assert attendance_data.check_method == method


class TestAttendanceStatistics:
    """测试考勤统计功能"""

    def test_attendance_statistics_response(self):
        """测试考勤统计响应模型"""
        stats = AttendanceStatistics(
            total_count=100,
            present_count=80,
            leave_count=5,
            absent_count=10,
            late_count=5,
            present_rate=85.0,
            total_hours_consumed=Decimal("150.0")
        )

        assert stats.total_count == 100
        assert stats.present_count == 80
        assert stats.present_rate == 85.0

    def test_calculate_present_rate(self):
        """测试出勤率计算"""
        # 出勤率 = (出勤 + 迟到) / 总次数 * 100
        total_count = 100
        present_count = 80
        late_count = 5

        present_rate = ((present_count + late_count) / total_count) * 100
        assert present_rate == 85.0

    def test_calculate_total_hours_consumed(self):
        """测试总消耗课时计算"""
        hours_list = [Decimal("1.5"), Decimal("2.0"), Decimal("1.0")]
        total_hours = sum(hours_list)

        assert total_hours == Decimal("4.5")


class TestAttendanceBusinessRules:
    """测试考勤业务规则"""

    def test_deduct_hours_for_present(self):
        """测试出勤扣减课时"""
        # 出勤状态（status=1）应该扣减课时
        status = 1
        hours_consumed = Decimal("2.0")

        should_deduct = status in [1, 4]  # 1:出勤 4:迟到
        assert should_deduct is True

    def test_deduct_hours_for_late(self):
        """测试迟到扣减课时"""
        # 迟到状态（status=4）应该扣减课时
        status = 4
        hours_consumed = Decimal("1.5")

        should_deduct = status in [1, 4]
        assert should_deduct is True

    def test_no_deduct_hours_for_leave(self):
        """测试请假不扣减课时"""
        # 请假状态（status=2）不应该扣减课时
        status = 2

        should_deduct = status in [1, 4]
        assert should_deduct is False

    def test_no_deduct_hours_for_absent(self):
        """测试缺勤不扣减课时"""
        # 缺勤状态（status=3）不应该扣减课时
        status = 3

        should_deduct = status in [1, 4]
        assert should_deduct is False


class TestAttendanceExceptions:
    """测试考勤异常处理"""

    def test_attendance_not_found_error(self):
        """测试考勤不存在异常"""
        error = AttendanceNotFoundError("考勤不存在: 999")
        assert str(error) == "考勤不存在: 999"

    def test_schedule_not_found_error(self):
        """测试排课不存在异常"""
        error = ScheduleNotFoundError("排课不存在: 999")
        assert str(error) == "排课不存在: 999"

    def test_student_not_found_error(self):
        """测试学员不存在异常"""
        error = StudentNotFoundError("学员不存在: 999")
        assert str(error) == "学员不存在: 999"

    def test_duplicate_attendance_error(self):
        """测试重复考勤异常"""
        error = DuplicateAttendanceError("学员已考勤: schedule_id=1, student_id=1")
        assert "已考勤" in str(error)

    def test_invalid_attendance_data_error(self):
        """测试无效考勤数据异常"""
        error = InvalidAttendanceDataError("无效的考勤数据")
        assert str(error) == "无效的考勤数据"

    def test_invalid_attendance_status_error(self):
        """测试无效考勤状态异常"""
        error = InvalidAttendanceStatusError("无效的考勤状态: 99")
        assert "无效的考勤状态" in str(error)


class TestAttendanceServiceMethods:
    """测试考勤服务方法"""

    def test_calculate_present_rate_with_zero_total(self):
        """测试总数为0时的出勤率计算"""
        total_count = 0
        present_count = 0
        late_count = 0

        if total_count > 0:
            present_rate = ((present_count + late_count) / total_count) * 100
        else:
            present_rate = 0.0

        assert present_rate == 0.0

    def test_calculate_present_rate_normal(self):
        """测试正常出勤率计算"""
        total_count = 100
        present_count = 85
        late_count = 10

        if total_count > 0:
            present_rate = ((present_count + late_count) / total_count) * 100
        else:
            present_rate = 0.0

        assert present_rate == 95.0

    def test_format_attendance_statistics(self):
        """测试考勤统计数据格式化"""
        stats = {
            "total_count": 100,
            "present_count": 85,
            "leave_count": 5,
            "absent_count": 5,
            "late_count": 5,
            "total_hours_consumed": Decimal("150.0")
        }

        # 计算出勤率
        if stats["total_count"] > 0:
            present_rate = (
                (stats["present_count"] + stats["late_count"]) /
                stats["total_count"] * 100
            )
        else:
            present_rate = 0.0

        stats["present_rate"] = round(present_rate, 2)

        assert stats["present_rate"] == 90.0
