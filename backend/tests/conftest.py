"""Pytest Configuration

测试配置和共享fixtures

包含：
- 数据库mock fixtures
- 支付配置mock fixtures
- 调度器mock fixtures
- 测试数据库session
- 认证fixtures
"""
import asyncio
import sys
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 加载测试环境变量
from dotenv import load_dotenv
dotenv_path = project_root / ".env.testing"
if dotenv_path.exists():
    load_dotenv(dotenv_path, override=True)

# 覆盖数据库 URL 为 SQLite（用于测试）
import os
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

# 在导入任何应用模块之前 patch SQLModel 以避免 PostgreSQL 引擎创建
import sys
# 移除已导入的模块，强制重新导入
mods_to_remove = [k for k in sys.modules.keys() if k.startswith('app.')]
for mod in mods_to_remove:
    del sys.modules[mod]

# ==================== 同步数据库引擎（用于测试） ====================


@pytest.fixture(scope="session")
def sync_test_engine():
    """创建同步测试数据库引擎（SQLite内存数据库）"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
    # 创建所有表
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(sync_test_engine) -> Generator[Session, None, None]:
    """创建同步测试数据库会话"""
    with Session(sync_test_engine) as session:
        yield session
        # 测试后回滚事务
        session.rollback()


# ==================== 异步数据库引擎（用于集成测试） ====================


@pytest.fixture(scope="function")
def async_test_engine():
    """创建异步测试数据库引擎（每个测试函数一个新引擎）"""
    async_engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
    yield async_engine
    # 测试结束后清理
    async_engine.sync_engine.dispose()


@pytest.fixture
async def db_session(
    async_test_engine,
) -> AsyncGenerator[AsyncSession, None]:
    """创建异步测试数据库会话（每个测试函数独立）

    注意：此 fixture 名称为 db_session，但返回 AsyncSession。
    用于替换测试文件中的同步 db_session fixture。
    """
    async with async_test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session_maker = async_sessionmaker(
        bind=async_test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session_maker() as session:
        yield session
        await session.rollback()
        await session.close()


# 保留原来的 async_db_session 作为别名
@pytest.fixture
async def async_db_session(
    async_test_engine,
) -> AsyncGenerator[AsyncSession, None]:
    """创建异步测试数据库会话（别名）"""
    async with async_test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session_maker = async_sessionmaker(
        bind=async_test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session_maker() as session:
        yield session
        await session.rollback()


# ==================== Mock Fixtures ====================


@pytest.fixture
def mock_settings():
    """Mock应用配置"""
    with patch("app.core.config.settings") as mock:
        mock.DATABASE_URL = "sqlite:///:memory:"
        mock.REDIS_URL = "redis://localhost:6379"
        mock.SECRET_KEY = "test-secret-key"
        mock.ALGORITHM = "HS256"
        mock.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        mock.WEWORK_CORP_ID = "test_corp_id"
        mock.WEWORK_AGENT_ID = "test_agent_id"
        mock.WEWORK_SECRET = "test_secret"
        mock.WECHAT_MCH_ID = "test_mch_id"
        mock.WECHAT_MCH_KEY = "test_mch_key"
        mock.WECHAT_NOTIFY_URL = "http://test.com/notify"
        mock.ALIPAY_APP_ID = "test_app_id"
        mock.DEBUG = True
        yield mock


@pytest.fixture
def mock_db_session():
    """Mock数据库会话"""
    session = MagicMock(spec=AsyncSession)
    session.execute = AsyncMock()
    session.get = MagicMock()
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    session.refresh = AsyncMock()
    return session


@pytest.fixture
def mock_redis():
    """Mock Redis客户端"""
    redis = MagicMock()
    redis.get = AsyncMock(return_value=None)
    redis.set = AsyncMock(return_value=True)
    redis.delete = AsyncMock(return_value=True)
    redis.exists = AsyncMock(return_value=False)
    redis.close = AsyncMock()
    return redis


@pytest.fixture
def mock_scheduler():
    """Mock任务调度器"""
    scheduler = MagicMock()
    scheduler.add_job = MagicMock()
    scheduler.remove_job = MagicMock()
    scheduler.start = MagicMock()
    scheduler.shutdown = MagicMock()
    scheduler.get_jobs = MagicMock(return_value=[])
    return scheduler


@pytest.fixture
def mock_wechat_pay_service():
    """Mock微信支付服务"""
    service = MagicMock()
    service._verify_sign = MagicMock(return_value=True)
    service._generate_sign = MagicMock(return_value="test_sign")
    service._generate_nonce_str = MagicMock(return_value="test_nonce")
    service._dict_to_xml = MagicMock(return_value="<xml></xml>")
    service._xml_to_dict = MagicMock(return_value={})
    service.create_order = AsyncMock(
        return_value={
            "return_code": "SUCCESS",
            "prepay_id": "test_prepay_id",
        }
    )
    service.query_order = AsyncMock(
        return_value={"return_code": "SUCCESS", "trade_state": "SUCCESS"}
    )
    service.close_order = AsyncMock(return_value={"return_code": "SUCCESS"})
    return service


@pytest.fixture
def mock_alipay_service():
    """Mock支付宝服务"""
    service = MagicMock()
    service.verify_notify = MagicMock(return_value=True)
    service.sdk_execute = MagicMock(return_value="{}")
    service.api_alipay_trade_page_pay = AsyncMock(
        return_value="https://alipay.com/pay"
    )
    service.api_alipay_trade_query = AsyncMock(
        return_value={"alipay_trade_query_response": {"trade_status": "TRADE_SUCCESS"}}
    )
    return service


# ==================== 测试数据 Fixtures ====================


@pytest.fixture
def sample_user_data():
    """示例用户数据"""
    return {
        "wework_id": "test_user_001",
        "name": "测试教师",
        "mobile": "13800138000",
        "role": "teacher",
        "status": 1,
    }


@pytest.fixture
def sample_student_data():
    """示例学员数据"""
    return {
        "name": "测试学员",
        "nickname": "小明",
        "gender": 1,
        "mobile": "13900139000",
        "parent_name": "测试家长",
        "parent_wework_id": "parent_wx_001",
        "parent_mobile": "13900139001",
        "source": "线上推广",
        "status": 1,
    }


@pytest.fixture
def sample_course_data():
    """示例课程数据"""
    return {
        "name": "测试课程",
        "category": "数学",
        "color": "#409EFF",
        "duration": 90,
        "max_students": 25,
        "status": 1,
    }


@pytest.fixture
def sample_classroom_data():
    """示例教室数据"""
    return {
        "name": "101教室",
        "capacity": 30,
        "status": 1,
    }


@pytest.fixture
def sample_department_data():
    """示例校区数据"""
    return {
        "name": "北京校区",
        "address": "北京市朝阳区",
        "contact": "010-12345678",
        "status": 1,
    }


@pytest.fixture
def sample_contract_data():
    """示例合同数据"""
    return {
        "contract_no": "CT20250214001",
        "student_id": 1,
        "course_id": 1,
        "package_type": "48课时",
        "total_hours": Decimal("48.00"),
        "remaining_hours": Decimal("48.00"),
        "unit_price": Decimal("150.00"),
        "total_amount": Decimal("7200.00"),
        "received_amount": Decimal("0.00"),
        "start_date": date.today(),
        "status": 1,
    }


@pytest.fixture
def sample_payment_data():
    """示例支付数据"""
    return {
        "payment_no": "PAY20250214001",
        "contract_id": 1,
        "amount": Decimal("7200.00"),
        "payment_method": 1,
        "status": 2,
    }


@pytest.fixture
def sample_schedule_data():
    """示例排课数据"""
    tomorrow = date.today() + timedelta(days=1)
    return {
        "course_id": 1,
        "teacher_id": 1,
        "classroom_id": 1,
        "start_time": datetime.combine(tomorrow, datetime.min.time().replace(hour=14)),
        "end_time": datetime.combine(tomorrow, datetime.min.time().replace(hour=15, minute=30)),
        "status": 1,
    }


# ==================== 认证 Fixtures ====================


@pytest.fixture
def auth_token():
    """创建测试用JWT token"""
    from app.core.security import create_access_token

    token_data = {"sub": "test_user_001", "role": "admin"}
    return create_access_token(token_data)


@pytest.fixture
def auth_headers(auth_token: str) -> dict:
    """创建认证头"""
    return {"Authorization": f"Bearer {auth_token}"}


# ==================== 异步测试支持 ====================


@pytest.fixture
def anyio_backend():
    """设置anyio后端为asyncio"""
    return "asyncio"


# ==================== FastAPI 测试客户端 ====================


@pytest.fixture
def client() -> TestClient:
    """创建FastAPI测试客户端"""
    from app.main import app

    return TestClient(app)


@pytest.fixture
async def async_client() -> AsyncClient:
    """创建异步HTTP客户端"""
    from app.main import app

    return AsyncClient(app=app, base_url="http://test")


# ==================== 工具函数 ====================


def create_test_token(
    data: dict,
    expires_delta: timedelta = timedelta(minutes=30),
) -> str:
    """创建测试JWT token"""
    from app.core.security import create_access_token

    return create_access_token(data, expires_delta)


def assert_response_success(response):
    """断言响应成功"""
    assert response.status_code in [200, 201, 204]


def assert_response_error(response, expected_status: int = 400):
    """断言响应错误"""
    assert response.status_code == expected_status


# ==================== 支付 Mock Fixtures ====================


@pytest.fixture
def mock_wechat_pay_config():
    """Mock微信支付配置"""
    with patch("app.payment.wechat_pay.WeChatPayConfig") as mock:
        mock.return_value.mch_id = "test_mch_id"
        mock.return_value.mch_key = "test_mch_key"
        mock.return_value.app_id = "test_app_id"
        mock.return_value.notify_url = "http://test.com/notify"
        mock.return_value.refund_notify_url = "http://test.com/refund_notify"
        mock.return_value.serial_no = "test_serial_no"
        mock.return_value.private_key = "test_private_key"
        yield mock


@pytest.fixture
def mock_alipay_config():
    """Mock支付宝配置"""
    with patch("app.payment.alipay.AliPayConfig") as mock:
        mock.return_value.app_id = "test_app_id"
        mock.return_value.app_private_key = "test_private_key"
        mock.return_value.alipay_public_key = "test_public_key"
        mock.return_value.notify_url = "http://test.com/alipay_notify"
        mock.return_value.return_url = "http://test.com/alipay_return"
        yield mock


@pytest.fixture
def mock_payment_services(mock_wechat_pay_config, mock_alipay_config):
    """Mock所有支付服务"""
    with patch("app.payment.wechat_pay.WeChatPayService") as wechat_mock, \
         patch("app.payment.alipay.AliPayService") as alipay_mock:

        wechat_mock.return_value = MagicMock()
        wechat_mock.return_value.create_payment = AsyncMock(
            return_value={
                "prepay_id": "test_prepay_id",
                "order_no": "TEST_ORDER_001",
                "pay_params": {
                    "appId": "wx123456",
                    "timeStamp": "1699900000",
                    "nonceStr": "test_nonce",
                    "package": "prepay_id=wx123456",
                    "signType": "RSA",
                    "paySign": "test_sign"
                }
            }
        )
        wechat_mock.return_value.verify_callback = AsyncMock(return_value=True)
        wechat_mock.return_value.query_order = AsyncMock(
            return_value={"trade_state": "SUCCESS"}
        )

        alipay_mock.return_value = MagicMock()
        alipay_mock.return_value.create_payment = AsyncMock(
            return_value={
                "order_no": "TEST_ORDER_002",
                "pay_url": "https://alipay.com/pay?order_id=123"
            }
        )
        alipay_mock.return_value.verify_notify = AsyncMock(return_value=True)
        alipay_mock.return_value.query_order = AsyncMock(
            return_value={"alipay_trade_query_response": {"trade_status": "TRADE_SUCCESS"}}
        )

        yield {
            "wechat": wechat_mock.return_value,
            "alipay": alipay_mock.return_value
        }


# ==================== 调度器 Mock Fixtures ====================


@pytest.fixture
def mock_scheduler_instance():
    """Mock APScheduler实例"""
    scheduler = MagicMock()
    scheduler.add_job = MagicMock()
    scheduler.remove_job = MagicMock()
    scheduler.start = MagicMock()
    scheduler.shutdown = MagicMock(wait=True)
    scheduler.get_jobs = MagicMock(return_value=[])
    scheduler.pause_job = MagicMock()
    scheduler.resume_job = MagicMock()
    return scheduler


@pytest.fixture
def mock_scheduler_context(mock_scheduler_instance):
    """Mock调度器上下文"""
    with patch("app.tasks.scheduler") as mock:
        mock.get_scheduler.return_value = mock_scheduler_instance
        mock_scheduler_instance.start = MagicMock()
        yield mock_scheduler_instance


# ==================== Redis Mock Fixtures ====================


@pytest.fixture
def mock_redis_client():
    """Mock Redis客户端完整实现"""
    redis = MagicMock()

    # 同步方法
    redis.get = MagicMock(return_value=None)
    redis.set = MagicMock(return_value=True)
    redis.setex = MagicMock(return_value=True)
    redis.delete = MagicMock(return_value=True)
    redis.exists = MagicMock(return_value=False)
    redis.incr = MagicMock(return_value=1)
    redis.decr = MagicMock(return_value=0)
    redis.expire = MagicMock(return_value=True)
    redis.ttl = MagicMock(return_value=-2)
    redis.keys = MagicMock(return_value=[])
    redis.ping = MagicMock(return_value=True)
    redis.close = MagicMock()
    redis.flushdb = MagicMock(return_value=True)

    # 异步方法
    redis.get = AsyncMock(return_value=None)
    redis.set = AsyncMock(return_value=True)
    redis.setex = AsyncMock(return_value=True)
    redis.delete = AsyncMock(return_value=True)
    redis.exists = AsyncMock(return_value=False)
    redis.incr = AsyncMock(return_value=1)
    redis.decr = AsyncMock(return_value=0)
    redis.expire = AsyncMock(return_value=True)
    redis.ttl = AsyncMock(return_value=-2)
    redis.keys = AsyncMock(return_value=[])
    redis.ping = AsyncMock(return_value=True)
    redis.close = AsyncMock()
    redis.aclose = AsyncMock()

    return redis


@pytest.fixture
def mock_redis_service(mock_redis_client):
    """Mock Redis服务"""
    with patch("app.core.cache.redis_service.RedisService") as mock:
        mock.return_value.get = AsyncMock(return_value=None)
        mock.return_value.set = AsyncMock(return_value=True)
        mock.return_value.delete = AsyncMock(return_value=True)
        mock.return_value.exists = AsyncMock(return_value=False)
        mock.return_value.close = AsyncMock()
        yield mock.return_value


# ==================== 企业微信 Mock Fixtures ====================


@pytest.fixture
def mock_wework_api():
    """Mock企业微信API"""
    with patch("app.core.wework.WeWorkAPI") as mock:
        mock.return_value.get_access_token = AsyncMock(
            return_value={"access_token": "test_token", "expires_in": 7200}
        )
        mock.return_value.send_message = AsyncMock(
            return_value={"errcode": 0, "errmsg": "ok"}
        )
        mock.return_value.get_user_info = AsyncMock(
            return_value={
                "userid": "test_user",
                "name": "测试用户",
                "department": [1]
            }
        )
        yield mock.return_value


# ==================== 通知服务 Mock Fixtures ====================


@pytest.fixture
def mock_notification_service():
    """Mock通知服务"""
    with patch("app.services.notification_service.NotificationService") as mock:
        mock.return_value.send_wework_message = AsyncMock(return_value=True)
        mock.return_value.send_template_message = AsyncMock(return_value=True)
        mock.return_value.create_notification = AsyncMock(return_value=1)
        mock.return_value.get_user_notifications = AsyncMock(return_value=[])
        yield mock.return_value


# ==================== 业务服务 Mock Fixtures ====================


@pytest.fixture
def mock_course_service():
    """Mock课程服务"""
    with patch("app.services.course_service.CourseService") as mock:
        mock.return_value.get_courses = AsyncMock(return_value=[])
        mock.return_value.get_course = AsyncMock(return_value=None)
        mock.return_value.create_course = AsyncMock(return_value=1)
        mock.return_value.update_course = AsyncMock(return_value=True)
        mock.return_value.delete_course = AsyncMock(return_value=True)
        yield mock.return_value


@pytest.fixture
def mock_student_service():
    """Mock学员服务"""
    with patch("app.services.student_service.StudentService") as mock:
        mock.return_value.get_students = AsyncMock(return_value=[])
        mock.return_value.get_student = AsyncMock(return_value=None)
        mock.return_value.create_student = AsyncMock(return_value=1)
        mock.return_value.update_student = AsyncMock(return_value=True)
        mock.return_value.delete_student = AsyncMock(return_value=True)
        yield mock.return_value


@pytest.fixture
def mock_schedule_service():
    """Mock排课服务"""
    with patch("app.services.schedule_service.ScheduleService") as mock:
        mock.return_value.get_schedules = AsyncMock(return_value=[])
        mock.return_value.get_schedule = AsyncMock(return_value=None)
        mock.return_value.create_schedule = AsyncMock(return_value=1)
        mock.return_value.update_schedule = AsyncMock(return_value=True)
        mock.return_value.delete_schedule = AsyncMock(return_value=True)
        mock.return_value.get_teacher_schedules = AsyncMock(return_value=[])
        yield mock.return_value


@pytest.fixture
def mock_attendance_service():
    """Mock考勤服务"""
    with patch("app.services.attendance_service.AttendanceService") as mock:
        mock.return_value.get_attendance_records = AsyncMock(return_value=[])
        mock.return_value.get_attendance = AsyncMock(return_value=None)
        mock.return_value.check_in = AsyncMock(return_value=1)
        mock.return_value.batch_check_in = AsyncMock(return_value=5)
        mock.return_value.get_attendance_stats = AsyncMock(return_value={})
        yield mock.return_value


# ==================== 完整的应用 Mock Fixtures ====================


@pytest.fixture
def mock_all_services(
    mock_payment_services,
    mock_redis_service,
    mock_wework_api,
    mock_notification_service,
    mock_course_service,
    mock_student_service,
    mock_schedule_service,
    mock_attendance_service,
):
    """Mock所有服务（用于端到端测试）"""
    return {
        "payment": mock_payment_services,
        "redis": mock_redis_service,
        "wework": mock_wework_api,
        "notification": mock_notification_service,
        "course": mock_course_service,
        "student": mock_student_service,
        "schedule": mock_schedule_service,
        "attendance": mock_attendance_service,
    }


@pytest.fixture
def app_with_mocks(
    mock_settings,
    mock_scheduler_context,
    mock_redis_service,
    mock_payment_services,
):
    """创建带有所有mock的FastAPI应用实例"""
    from app.main import app

    # 覆盖依赖
    app.dependency_overrides = {}

    return app


@pytest.fixture
def authenticated_client(client, auth_headers):
    """创建已认证的测试客户端"""
    return client


@pytest.fixture
async def async_authenticated_client(async_client, auth_headers):
    """创建异步已认证的测试客户端"""
    return async_client
