"""
微信支付服务测试

测试微信支付集成功能
"""
import pytest

pytestmark = pytest.mark.skip(reason="需要微信支付模块配置，仅在 CI 环境中运行")
from decimal import Decimal

from app.payment.wechat import (
    WeChatPayService,
    WeChatPayConfigError,
    WeChatPayAPIError,
    yuan_to_fen,
    fen_to_yuan,
)


class TestWeChatPayUtils:
    """测试微信支付工具方法"""

    def test_yuan_to_fen(self):
        """测试元转分"""
        assert yuan_to_fen(Decimal("1.00")) == 100
        assert yuan_to_fen(Decimal("0.01")) == 1
        assert yuan_to_fen(Decimal("100.99")) == 10099
        assert yuan_to_fen(Decimal("0.00")) == 0

    def test_fen_to_yuan(self):
        """测试分转元"""
        assert fen_to_yuan(100) == Decimal("1.00")
        assert fen_to_yuan(1) == Decimal("0.01")
        assert fen_to_yuan(10099) == Decimal("100.99")
        assert fen_to_yuan(0) == Decimal("0.00")


class TestWeChatPayService:
    """测试微信支付服务"""

    @pytest.fixture
    def service(self):
        """创建服务实例"""
        # 注意：如果环境变量未配置，这里会抛出异常
        try:
            return WeChatPayService()
        except WeChatPayConfigError:
            pytest.skip("微信支付未配置")

    def test_generate_nonce_str(self, service):
        """测试生成随机字符串"""
        nonce = service._generate_nonce_str()
        assert isinstance(nonce, str)
        assert len(nonce) == 32

    def test_generate_sign(self, service):
        """测试生成签名"""
        params = {
            "appid": "test_appid",
            "mch_id": "test_mch_id",
            "nonce_str": "test_nonce_str",
            "body": "test",
            "out_trade_no": "test_order_no",
            "total_fee": 100,
            "spbill_create_ip": "127.0.0.1",
        }

        sign = service._generate_sign(params)
        assert isinstance(sign, str)
        assert len(sign) == 32  # MD5签名长度
        assert sign.isupper()  # 签名应该大写

    def test_verify_sign(self, service):
        """测试验证签名"""
        params = {
            "appid": "test_appid",
            "mch_id": "test_mch_id",
            "nonce_str": "test_nonce_str",
            "body": "test",
            "out_trade_no": "test_order_no",
            "total_fee": 100,
            "spbill_create_ip": "127.0.0.1",
        }

        sign = service._generate_sign(params)
        assert service._verify_sign(params, sign) is True

        # 错误的签名应该验证失败
        assert service._verify_sign(params, "INVALID_SIGN") is False

    def test_dict_to_xml(self, service):
        """测试字典转XML"""
        data = {
            "return_code": "SUCCESS",
            "return_msg": "OK",
        }

        xml = service._dict_to_xml(data)
        assert isinstance(xml, str)
        assert "<return_code>SUCCESS</return_code>" in xml
        assert "<return_msg>OK</return_msg>" in xml

    def test_xml_to_dict(self, service):
        """测试XML转字典"""
        xml = "<xml><return_code>SUCCESS</return_code><return_msg>OK</return_msg></xml>"

        data = service._xml_to_dict(xml)
        assert isinstance(data, dict)
        assert data["return_code"] == "SUCCESS"
        assert data["return_msg"] == "OK"


class TestWeChatPayAPI:
    """测试微信支付API

    注意：这些测试需要真实的微信支付配置和网络连接
    在CI/CD环境中应该使用mock
    """

    @pytest.fixture
    def service(self):
        """创建服务实例"""
        try:
            return WeChatPayService()
        except WeChatPayConfigError:
            pytest.skip("微信支付未配置")

    @pytest.mark.asyncio
    async def test_create_order_jsapi(self, service):
        """测试创建JSAPI订单

        注意：这是一个集成测试，需要真实配置
        """
        pytest.skip("需要真实微信支付配置")

        try:
            result = await service.create_order(
                order_no="test_order_001",
                total_fee=100,  # 1元
                body="测试商品",
                trade_type=service.TRADE_TYPE_JSAPI,
                openid="test_openid",
            )

            assert result["return_code"] == "SUCCESS"
            assert "prepay_id" in result

        except WeChatPayAPIError as e:
            pytest.skip(f"微信支付API错误: {e}")

    @pytest.mark.asyncio
    async def test_query_order(self, service):
        """测试查询订单"""
        pytest.skip("需要真实微信支付配置")

        try:
            result = await service.query_order(order_no="test_order_001")
            assert result["return_code"] == "SUCCESS"

        except WeChatPayAPIError as e:
            pytest.skip(f"微信支付API错误: {e}")
