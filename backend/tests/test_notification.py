"""Notification Module Tests

通知模块测试

测试通知的 schema、CRUD 和服务层功能
"""
import pytest
from datetime import datetime, date
from decimal import Decimal

from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
    NotificationResponse,
    NotificationBatchCreate,
    NotificationMarkRead,
    NotificationType,
    ReceiverType,
    NotificationStatus,
)


class TestNotificationSchemas:
    """测试通知 Schema"""

    def test_notification_create_valid(self):
        """测试有效的通知创建"""
        notification = NotificationCreate(
            type=NotificationType.CLASS_REMINDER,
            receiver_id="test_user",
            receiver_type=ReceiverType.WEWORK,
            title="测试通知",
            content="这是一个测试通知",
            url="https://example.com"
        )
        assert notification.type == 1
        assert notification.receiver_id == "test_user"
        assert notification.receiver_type == 1
        assert notification.title == "测试通知"
        assert notification.content == "这是一个测试通知"
        assert notification.url == "https://example.com"

    def test_notification_create_minimal(self):
        """测试最小通知创建"""
        notification = NotificationCreate(
            type=NotificationType.HOMEWORK_NOTICE,
            receiver_id="test_user",
            title="测试通知"
        )
        assert notification.type == 2
        assert notification.receiver_id == "test_user"
        assert notification.receiver_type == 1  # 默认值
        assert notification.title == "测试通知"

    def test_notification_update(self):
        """测试通知更新"""
        update = NotificationUpdate(
            title="更新后的标题",
            content="更新后的内容",
            status=NotificationStatus.READ
        )
        assert update.title == "更新后的标题"
        assert update.content == "更新后的内容"
        assert update.status == 3

    def test_notification_batch_create(self):
        """测试批量通知创建"""
        batch = NotificationBatchCreate(
            receiver_ids=["user1", "user2", "user3"],
            receiver_type=ReceiverType.WEWORK,
            type=NotificationType.SYSTEM_NOTICE,
            title="系统通知",
            content="这是一个系统通知"
        )
        assert len(batch.receiver_ids) == 3
        assert batch.receiver_type == 1
        assert batch.type == 5

    def test_notification_mark_read(self):
        """测试标记已读"""
        mark_read = NotificationMarkRead(
            notification_ids=[1, 2, 3]
        )
        assert len(mark_read.notification_ids) == 3

    def test_notification_type_enum(self):
        """测试通知类型枚举"""
        assert NotificationType.CLASS_REMINDER == 1
        assert NotificationType.HOMEWORK_NOTICE == 2
        assert NotificationType.ATTENDANCE_NOTICE == 3
        assert NotificationType.CONTRACT_NOTICE == 4
        assert NotificationType.SYSTEM_NOTICE == 5

    def test_receiver_type_enum(self):
        """测试接收者类型枚举"""
        assert ReceiverType.WEWORK == 1
        assert ReceiverType.PARENT == 2
        assert ReceiverType.MINIAPP == 3

    def test_notification_status_enum(self):
        """测试通知状态枚举"""
        assert NotificationStatus.PENDING == 0
        assert NotificationStatus.SENT == 1
        assert NotificationStatus.FAILED == 2
        assert NotificationStatus.READ == 3


class TestNotificationServiceTemplates:
    """测试通知服务模板"""

    def test_class_reminder_template(self):
        """测试上课提醒模板"""
        from app.services.notification_service import NotificationService
        from unittest.mock import Mock

        mock_schedule = Mock()
        mock_schedule.start_time = datetime(2026, 2, 15, 10, 0)

        template = NotificationService.create_class_reminder_template(
            schedule=mock_schedule,
            student_name="张三",
            course_name="Python 编程",
            teacher_name="李老师",
            classroom_name="301教室",
            reminder_minutes=30
        )

        assert "上课提醒" in template["title"]
        assert "Python 编程" in template["title"]
        assert "张三" in template["content"]
        assert "李老师" in template["content"]
        assert "301教室" in template["content"]

    def test_homework_notice_template(self):
        """测试作业通知模板"""
        from app.services.notification_service import NotificationService
        from unittest.mock import Mock

        mock_homework = Mock()
        mock_homework.title = "Python 作业 1"
        mock_homework.deadline = datetime(2026, 2, 20, 23, 59)

        template = NotificationService.create_homework_notice_template(
            homework=mock_homework,
            student_name="张三",
            course_name="Python 编程"
        )

        assert "作业通知" in template["title"]
        assert "Python 编程" in template["title"]
        assert "Python 作业 1" in template["content"]
        assert "张三" in template["content"]

    def test_system_notice_template(self):
        """测试系统通知模板"""
        from app.services.notification_service import NotificationService

        template = NotificationService.create_system_notice_template(
            title="系统维护",
            content="系统将于今晚 22:00 进行维护"
        )

        assert "系统通知" in template["title"]
        assert "系统维护" in template["title"]
        assert "系统将于今晚 22:00 进行维护" in template["content"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
