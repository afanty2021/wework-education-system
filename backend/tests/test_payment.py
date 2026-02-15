"""Payment Schema Tests

缴费 Pydantic 模型测试
"""
import pytest
from datetime import datetime
from decimal import Decimal
from pydantic import ValidationError

from app.schemas.payment import (
    PaymentBase,
    PaymentCreate,
    PaymentUpdate,
    PaymentConfirm,
    PaymentRefund,
    PaymentResponse,
)


class TestPaymentSchemas:
    """缴费模型测试"""

    def test_payment_base(self):
        """测试缴费基础模型"""
        data = {
            "contract_id": 1,
            "amount": Decimal("100.00"),
            "payment_method": 1,
            "hours": Decimal("10.5"),
        }
        payment = PaymentBase(**data)

        assert payment.contract_id == 1
        assert payment.amount == Decimal("100.00")
        assert payment.payment_method == 1
        assert payment.hours == Decimal("10.5")

    def test_payment_create(self):
        """测试缴费创建模型"""
        data = {
            "payment_no": "P202402140001",
            "contract_id": 1,
            "amount": Decimal("100.00"),
            "payment_method": 1,
            "hours": Decimal("10.5"),
            "remark": "测试缴费",
        }
        payment = PaymentCreate(**data)

        assert payment.payment_no == "P202402140001"
        assert payment.contract_id == 1
        assert payment.amount == Decimal("100.00")

    def test_payment_create_validation_error(self):
        """测试缴费创建模型验证错误"""
        # 金额必须大于0
        with pytest.raises(ValidationError):
            PaymentCreate(
                payment_no="P202402140001",
                contract_id=1,
                amount=Decimal("-100.00"),
                payment_method=1,
            )

        # 支付方式必须在1-5之间
        with pytest.raises(ValidationError):
            PaymentCreate(
                payment_no="P202402140001",
                contract_id=1,
                amount=Decimal("100.00"),
                payment_method=6,
            )

    def test_payment_update(self):
        """测试缴费更新模型"""
        data = {
            "amount": Decimal("200.00"),
            "status": 2,
            "remark": "更新缴费",
        }
        payment = PaymentUpdate(**data)

        assert payment.amount == Decimal("200.00")
        assert payment.status == 2
        assert payment.remark == "更新缴费"

    def test_payment_confirm(self):
        """测试缴费确认模型"""
        data = {
            "hours": Decimal("10.5"),
            "remark": "确认缴费",
        }
        confirm = PaymentConfirm(**data)

        assert confirm.hours == Decimal("10.5")
        assert confirm.remark == "确认缴费"

    def test_payment_confirm_validation_error(self):
        """测试缴费确认模型验证错误"""
        # 课时必须大于0
        with pytest.raises(ValidationError):
            PaymentConfirm(hours=Decimal("-10.5"))

    def test_payment_refund(self):
        """测试缴费退款模型"""
        data = {
            "refund_amount": Decimal("50.00"),
            "refund_hours": Decimal("5.0"),
            "refund_reason": "学员退费",
        }
        refund = PaymentRefund(**data)

        assert refund.refund_amount == Decimal("50.00")
        assert refund.refund_hours == Decimal("5.0")
        assert refund.refund_reason == "学员退费"

    def test_payment_refund_validation_error(self):
        """测试缴费退款模型验证错误"""
        # 退款金额必须大于0
        with pytest.raises(ValidationError):
            PaymentRefund(refund_amount=Decimal("-50.00"))


class TestPaymentServiceCalculations:
    """缴费服务计算测试"""

    def test_payment_amount_validation(self):
        """测试缴费金额验证"""
        # 正常金额
        amount = Decimal("100.00")
        assert amount > 0

        # 异常金额
        with pytest.raises(ValidationError):
            PaymentCreate(
                payment_no="P202402140001",
                contract_id=1,
                amount=Decimal("-100.00"),
                payment_method=1,
            )

    def test_payment_hours_validation(self):
        """测试缴费课时验证"""
        # 正常课时
        hours = Decimal("10.5")
        assert hours > 0

        # 异常课时
        with pytest.raises(ValidationError):
            PaymentCreate(
                payment_no="P202402140001",
                contract_id=1,
                amount=Decimal("100.00"),
                payment_method=1,
                hours=Decimal("-10.5"),
            )


class TestPaymentServiceValidation:
    """缴费服务验证测试"""

    def test_payment_method_validation(self):
        """测试支付方式验证"""
        # 正常支付方式
        for method in [1, 2, 3, 4, 5]:
            payment = PaymentCreate(
                payment_no=f"P202402140001{method}",
                contract_id=1,
                amount=Decimal("100.00"),
                payment_method=method,
            )
            assert payment.payment_method == method

        # 异常支付方式
        with pytest.raises(ValidationError):
            PaymentCreate(
                payment_no="P202402140001",
                contract_id=1,
                amount=Decimal("100.00"),
                payment_method=6,
            )

    def test_payment_status_validation(self):
        """测试缴费状态验证"""
        # 正常状态
        for status_value in [1, 2, 3]:
            payment = PaymentUpdate(status=status_value)
            assert payment.status == status_value

        # 异常状态
        with pytest.raises(ValidationError):
            PaymentUpdate(status=4)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
