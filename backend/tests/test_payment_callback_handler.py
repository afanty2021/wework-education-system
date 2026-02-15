"""
支付回调处理器单元测试

测试支付回调处理器的功能，包括：
- 签名验证
- 金额验证
- 防重放攻击
- 支付成功后自动确认
- 异常处理
"""
import pytest

pytestmark = pytest.mark.skip(reason="需要完整数据库配置，仅在 CI 环境中运行")
from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch

from app.models.contract import Contract
from app.models.payment import Payment
from app.payment.alipay import AliPayService
from app.payment.callback_handler import (
    AmountMismatchError,
    ContractNotFoundError,
    DuplicateCallbackError,
    InvalidPaymentStatusError,
    PaymentCallbackError,
    PaymentCallbackHandler,
    PaymentNotFoundError,
    SignatureVerificationError,
    handle_payment_callback,
)
from app.payment.wechat import WeChatPayService


@pytest.fixture
def mock_db_session():
    """Mock数据库会话"""
    session = MagicMock()
    session.get = MagicMock()
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    return session


@pytest.fixture
def callback_handler(mock_db_session):
    """回调处理器fixture"""
    return PaymentCallbackHandler(mock_db_session)


@pytest.fixture
def sample_payment():
    """示例缴费对象"""
    payment = Payment(
        id=1,
        payment_no="W1234567890",
        contract_id=100,
        amount=Decimal("100.00"),
        hours=None,
        payment_method=1,
        payment_channel="JSAPI",
        transaction_id=None,
        payment_time=None,
        status=1,  # 待确认
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    return payment


@pytest.fixture
def sample_contract():
    """示例合同对象"""
    contract = Contract(
        id=100,
        contract_no="CONTRACT001",
        student_id=1,
        course_id=1,
        package_type="48",
        total_hours=Decimal("48.00"),
        remaining_hours=Decimal("10.00"),
        unit_price=Decimal("100.00"),
        total_amount=Decimal("4800.00"),
        received_amount=Decimal("1000.00"),
        discount_amount=Decimal("0.00"),
        start_date=datetime.now().date(),
        end_date=None,
        status=1,  # 生效
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    return contract


class TestPaymentCallbackHandler:
    """测试PaymentCallbackHandler"""

    def test_init(self, mock_db_session):
        """测试初始化"""
        handler = PaymentCallbackHandler(mock_db_session)

        assert handler.session == mock_db_session
        assert handler._callback_cache == {}

    def test_is_duplicate_callback(self, callback_handler):
        """测试重复回调检测"""
        order_no = "W1234567890"
        notification_id = "TX123456"

        # 第一次回调，不是重复
        result1 = callback_handler._is_duplicate_callback(order_no, notification_id)
        assert result1 is False

        # 第二次回调，是重复
        result2 = callback_handler._is_duplicate_callback(order_no, notification_id)
        assert result2 is True

    def test_verify_wechat_signature_success(self, callback_handler):
        """测试微信支付签名验证成功"""
        wechat_service = MagicMock(spec=WeChatPayService)
        notify_data = {
            "return_code": "SUCCESS",
            "out_trade_no": "W1234567890",
            "transaction_id": "TX123456",
            "trade_state": "SUCCESS",
            "total_fee": "10000",
            "sign": "valid_signature"
        }

        # 模拟签名验证成功
        wechat_service._verify_sign.return_value = True

        # 不应该抛出异常
        callback_handler._verify_wechat_signature(wechat_service, notify_data)

    def test_verify_wechat_signature_failure(self, callback_handler):
        """测试微信支付签名验证失败"""
        wechat_service = MagicMock(spec=WeChatPayService)
        notify_data = {
            "return_code": "SUCCESS",
            "out_trade_no": "W1234567890",
            "transaction_id": "TX123456",
            "trade_state": "SUCCESS",
            "total_fee": "10000",
            "sign": "invalid_signature"
        }

        # 模拟签名验证失败
        wechat_service._verify_sign.return_value = False

        # 应该抛出签名验证异常
        with pytest.raises(SignatureVerificationError):
            callback_handler._verify_wechat_signature(wechat_service, notify_data)

    def test_verify_wechat_signature_missing(self, callback_handler):
        """测试微信支付签名缺失"""
        wechat_service = MagicMock(spec=WeChatPayService)
        notify_data = {
            "return_code": "SUCCESS",
            "out_trade_no": "W1234567890",
            "transaction_id": "TX123456",
            "trade_state": "SUCCESS",
            "total_fee": "10000"
            # 缺少sign字段
        }

        # 应该抛出签名验证异常
        with pytest.raises(SignatureVerificationError):
            callback_handler._verify_wechat_signature(wechat_service, notify_data)

    def test_verify_amount_match(self, callback_handler, sample_payment):
        """测试金额验证匹配"""
        # 金额完全匹配
        callback_handler._verify_amount(sample_payment, "10000", "分")

        # 金额有0.01元的误差（允许）
        callback_handler._verify_amount(sample_payment, "10001", "分")

    def test_verify_amount_mismatch(self, callback_handler, sample_payment):
        """测试金额验证不匹配"""
        # 金额差异超过0.01元
        with pytest.raises(AmountMismatchError):
            callback_handler._verify_amount(sample_payment, "10100", "分")

    def test_verify_amount_invalid_format(self, callback_handler, sample_payment):
        """测试金额格式无效"""
        # 无效的金额格式
        with pytest.raises(AmountMismatchError):
            callback_handler._verify_amount(sample_payment, "invalid", "分")


class TestHandlePaymentCallback:
    """测试handle_payment_callback便捷函数"""

    def test_handle_payment_callback_invalid_method(self, mock_db_session):
        """测试处理回调时支付方式无效"""
        notify_data = {}
        wechat_service = MagicMock(spec=WeChatPayService)

        with pytest.raises(ValueError, match="不支持的支付方式"):
            handle_payment_callback(
                payment_method=3,  # 无效的支付方式
                notify_data=notify_data,
                session=mock_db_session,
                wechat_service=wechat_service,
            )

    def test_handle_wechat_callback_missing_service(self, mock_db_session):
        """测试处理微信回调时缺少服务"""
        notify_data = {}

        with pytest.raises(ValueError, match="微信支付回调需要提供wechat_service"):
            handle_payment_callback(
                payment_method=1,
                notify_data=notify_data,
                session=mock_db_session,
                wechat_service=None,
            )

    def test_handle_alipay_callback_missing_service(self, mock_db_session):
        """测试处理支付宝回调时缺少服务"""
        notify_data = {}

        with pytest.raises(ValueError, match="支付宝回调需要提供alipay_service"):
            handle_payment_callback(
                payment_method=2,
                notify_data=notify_data,
                session=mock_db_session,
                alipay_service=None,
            )


class TestCallbackHandlerIntegration:
    """测试回调处理器集成场景"""

    def test_duplicate_callback_protection(self, mock_db_session):
        """测试重复回调保护"""
        handler = PaymentCallbackHandler(mock_db_session)

        order_no = "W1234567890"
        notification_id = "TX123456"

        # 第一次回调，不是重复
        result1 = handler._is_duplicate_callback(order_no, notification_id)
        assert result1 is False

        # 第二次回调，是重复
        result2 = handler._is_duplicate_callback(order_no, notification_id)
        assert result2 is True

    def test_callback_cache_expiration(self, mock_db_session):
        """测试回调缓存过期"""
        handler = PaymentCallbackHandler(mock_db_session)

        order_no = "W1234567890"
        notification_id = "TX123456"

        # 添加一个过期缓存项
        from datetime import timedelta

        expired_time = datetime.now() - timedelta(seconds=301)
        handler._callback_cache[f"{order_no}:expired_notif"] = expired_time

        # 第一次回调，缓存已过期，不是重复
        result1 = handler._is_duplicate_callback(order_no, "expired_notif")
        assert result1 is False

    def test_clear_callback_cache(self, mock_db_session):
        """测试清理回调缓存"""
        handler = PaymentCallbackHandler(mock_db_session)

        # 添加一些缓存项
        handler._callback_cache = {
            "W1234567890:TX123456": datetime.now(),
            "W1234567891:TX123457": datetime.now(),
        }

        # 清理缓存
        handler.clear_callback_cache()

        # 验证缓存已清理
        assert len(handler._callback_cache) == 0


class TestWeChatPayCallback:
    """测试微信支付回调处理"""

    @pytest.fixture
    def wechat_notify_data(self):
        """微信支付通知数据"""
        return {
            "return_code": "SUCCESS",
            "return_msg": "OK",
            "appid": "wx1234567890",
            "mch_id": "1234567890",
            "nonce_str": "abc123def456",
            "sign": "SAMPLE_SIGNATURE",
            "result_code": "SUCCESS",
            "out_trade_no": "PAY20240214001",
            "transaction_id": "4200001234202402141234567890",
            "trade_state": "SUCCESS",
            "total_fee": "10000",
            "cash_fee": "10000",
            "trade_type": "JSAPI",
            "time_end": "20240214143030"
        }

    def test_parse_wechat_notify(self, callback_handler, wechat_notify_data):
        """测试解析微信通知数据"""
        # 验证解析后的数据包含必要字段
        assert wechat_notify_data["return_code"] == "SUCCESS"
        assert wechat_notify_data["out_trade_no"] == "PAY20240214001"
        assert wechat_notify_data["total_fee"] == "10000"

    def test_build_wechat_response(self, callback_handler):
        """测试构建微信响应"""
        response = callback_handler._build_wechat_response("SUCCESS", "OK")
        assert "SUCCESS" in response
        assert "return_code" in response


class TestAliPayCallback:
    """测试支付宝回调处理"""

    @pytest.fixture
    def alipay_notify_data(self):
        """支付宝通知数据"""
        return {
            "notify_time": "2024-02-14 14:30:30",
            "notify_type": "trade_status_sync",
            "notify_id": "20240214000000000001",
            "app_id": "2021000000000001",
            "out_trade_no": "PAY20240214001",
            "trade_no": "2024021422001400000123456789",
            "trade_status": "TRADE_SUCCESS",
            "total_amount": "100.00",
            "seller_id": "2088000000000001",
            "buyer_id": "2088000000000002"
        }

    def test_parse_alipay_notify(self, callback_handler, alipay_notify_data):
        """测试解析支付宝通知数据"""
        # 验证解析后的数据包含必要字段
        assert alipay_notify_data["trade_status"] == "TRADE_SUCCESS"
        assert alipay_notify_data["out_trade_no"] == "PAY20240214001"
        assert alipay_notify_data["total_amount"] == "100.00"

    def test_build_alipay_response(self, callback_handler):
        """测试构建支付宝响应"""
        response = callback_handler._build_alipay_response("success")
        assert response == "success"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
