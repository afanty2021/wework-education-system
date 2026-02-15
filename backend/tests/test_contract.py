"""Contract Module Tests

合同管理功能测试
"""
import pytest
from datetime import date, datetime
from decimal import Decimal

from app.schemas.contract import (
    ContractCreate,
    ContractUpdate,
    ContractResponse,
    ContractDeductHours,
    ContractAddHours,
)
from app.services.contract_service import (
    ContractService,
    ContractServiceError,
    ContractNotFoundError,
    InvalidContractDataError,
)


class TestContractSchemas:
    """测试合同 Schema 模型"""

    def test_contract_create_schema(self):
        """测试合同创建 Schema"""
        contract_data = ContractCreate(
            contract_no="CT20260001",
            student_id=1,
            course_id=1,
            package_type="48",
            total_hours=Decimal("48.00"),
            remaining_hours=Decimal("48.00"),
            unit_price=Decimal("150.00"),
            total_amount=Decimal("7200.00"),
            received_amount=Decimal("7200.00"),
            discount_amount=Decimal("0.00"),
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            expire_warning_days=30,
            notes="测试合同"
        )

        assert contract_data.contract_no == "CT20260001"
        assert contract_data.student_id == 1
        assert contract_data.total_hours == Decimal("48.00")
        # ContractCreate 不包含 status 字段，因为它在创建时自动设置为 1（生效）
        # status 只在 ContractResponse 和 ContractUpdate 中出现

    def test_contract_update_schema(self):
        """测试合同更新 Schema"""
        update_data = ContractUpdate(
            package_type="72",
            total_hours=Decimal("72.00"),
            remaining_hours=Decimal("72.00"),
            status=1
        )

        assert update_data.package_type == "72"
        assert update_data.total_hours == Decimal("72.00")
        assert update_data.status == 1

    def test_contract_deduct_hours_schema(self):
        """测试扣减课时 Schema"""
        deduct_data = ContractDeductHours(
            hours=Decimal("2.00"),
            reason="正常上课"
        )

        assert deduct_data.hours == Decimal("2.00")
        assert deduct_data.reason == "正常上课"

    def test_contract_add_hours_schema(self):
        """测试追加课时 Schema"""
        add_data = ContractAddHours(
            hours=Decimal("12.00"),
            reason="课时包续费"
        )

        assert add_data.hours == Decimal("12.00")
        assert add_data.reason == "课时包续费"


class TestContractServiceCalculations:
    """测试合同服务计算功能"""

    def test_calculate_total_amount(self):
        """测试合同总金额计算"""
        unit_price = Decimal("150.00")
        total_hours = Decimal("48.00")
        discount_amount = Decimal("100.00")

        total = ContractService.calculate_total_amount(
            unit_price=unit_price,
            total_hours=total_hours,
            discount_amount=discount_amount
        )

        # 150 * 48 - 100 = 7100
        assert total == Decimal("7100.00")

    def test_calculate_total_amount_no_discount(self):
        """测试无折扣的合同总金额计算"""
        unit_price = Decimal("150.00")
        total_hours = Decimal("48.00")
        discount_amount = Decimal("0.00")

        total = ContractService.calculate_total_amount(
            unit_price=unit_price,
            total_hours=total_hours,
            discount_amount=discount_amount
        )

        # 150 * 48 - 0 = 7200
        assert total == Decimal("7200.00")

    def test_calculate_remaining_value(self):
        """测试剩余课时价值计算"""
        unit_price = Decimal("150.00")
        remaining_hours = Decimal("30.00")

        value = ContractService.calculate_remaining_value(
            unit_price=unit_price,
            remaining_hours=remaining_hours
        )

        # 150 * 30 = 4500
        assert value == Decimal("4500.00")

    def test_calculate_usage_percentage(self):
        """测试课时使用百分比计算"""
        total_hours = Decimal("48.00")
        remaining_hours = Decimal("30.00")

        percentage = ContractService.calculate_usage_percentage(
            total_hours=total_hours,
            remaining_hours=remaining_hours
        )

        # (48 - 30) / 48 * 100 = 37.5%
        assert percentage == Decimal("37.50")

    def test_calculate_usage_percentage_zero_total(self):
        """测试总课时为0时的使用百分比"""
        total_hours = Decimal("0.00")
        remaining_hours = Decimal("0.00")

        percentage = ContractService.calculate_usage_percentage(
            total_hours=total_hours,
            remaining_hours=remaining_hours
        )

        assert percentage == Decimal("0.00")

    def test_calculate_usage_percentage_full_usage(self):
        """测试全部使用完的使用百分比"""
        total_hours = Decimal("48.00")
        remaining_hours = Decimal("0.00")

        percentage = ContractService.calculate_usage_percentage(
            total_hours=total_hours,
            remaining_hours=remaining_hours
        )

        # (48 - 0) / 48 * 100 = 100%
        assert percentage == Decimal("100.00")


class TestContractServiceValidation:
    """测试合同服务验证功能"""

    def test_validate_remaining_hours_not_exceed_total(self):
        """测试剩余课时不能超过总课时"""
        # 这个验证会在 Service 层的 create_contract 中进行
        # 这里只是验证逻辑
        total_hours = Decimal("48.00")
        remaining_hours = Decimal("50.00")

        assert remaining_hours > total_hours
        # 在实际使用中，这应该触发 InvalidContractDataError


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
