"""Payment Flow Tests

支付流程测试 - 完整的支付和退款流程测试
"""
import pytest
from decimal import Decimal
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.payment import PaymentCreate
from app.schemas.student import StudentCreate
from app.schemas.course import CourseCreate
from app.services.payment_service import PaymentService
from app.services.student_service import StudentService
from app.services.course_service import CourseService
from app.services.contract_service import ContractService


@pytest.mark.skip(reason="需要完整的数据库和支付配置，集成测试在CI中运行")
@pytest.mark.asyncio
async def test_payment_flow_full(db_session: AsyncSession):
    """测试完整支付流程

    流程步骤：
    1. 创建学员
    2. 创建课程
    3. 创建合同
    4. 创建支付记录
    5. 确认支付
    6. 更新合同已收金额
    7. 验证支付状态
    """
    # 1. 创建学员
    student = await StudentService.create_student(
        student_data=StudentCreate(
            name="支付测试学员",
            mobile="13800138005"
        ),
        session=db_session
    )
    await db_session.commit()

    # 2. 创建课程
    course = await CourseService.create_course(
        course_data=CourseCreate(
            name="支付测试课程",
            category="测试",
            duration=90,
            max_students=20
        ),
        session=db_session
    )
    await db_session.commit()

    # 3. 创建合同
    contract = await ContractService.create_contract(
        contract_no="CT20250214005",
        student_id=student.id,
        course_id=course.id,
        package_type="48课时",
        total_hours=Decimal("48.00"),
        unit_price=Decimal("150.00"),
        total_amount=Decimal("7200.00"),
        start_date=date.today(),
        session=db_session
    )
    await db_session.commit()

    # 4. 创建支付记录
    payment = await PaymentService.create_payment(
        payment_data=PaymentCreate(
            payment_no="PAY20250214001",
            contract_id=contract.id,
            amount=Decimal("7200.00"),
            payment_method=1,  # 微信支付
            hours=Decimal("48.00"),
            remark="测试支付"
        ),
        session=db_session
    )
    await db_session.commit()
    assert payment.id is not None
    assert payment.status == 1  # 待确认

    # 5. 确认支付
    confirmed_payment = await PaymentService.confirm_payment(
        payment_id=payment.id,
        hours=Decimal("48.00"),
        remark="已确认收款",
        session=db_session
    )
    await db_session.commit()
    assert confirmed_payment.status == 2  # 已确认

    # 6. 更新合同已收金额
    contract = await ContractService.get_contract_by_id(contract.id, db_session)
    assert contract.received_amount == Decimal("7200.00")

    print("\n✅ 完整支付流程测试通过！")


@pytest.mark.asyncio
@pytest.mark.skip(reason="需要完整的数据库和支付配置，集成测试在CI中运行")
async def test_partial_payment_flow(db_session: AsyncSession):
    """测试分期支付流程

    流程步骤：
    1. 创建学员和合同
    2. 第一次支付
    3. 第二次支付
    4. 验证合同已收金额
    """
    # 创建学员和课程
    student = await StudentService.create_student(
        student_data=StudentCreate(
            name="分期付款学员",
            mobile="13800138006"
        ),
        session=db_session
    )
    await db_session.commit()

    course = await CourseService.create_course(
        course_data=CourseCreate(
            name="分期测试课程",
            category="测试",
            duration=90,
            max_students=20
        ),
        session=db_session
    )
    await db_session.commit()

    contract = await ContractService.create_contract(
        contract_no="CT20250214006",
        student_id=student.id,
        course_id=course.id,
        package_type="48课时",
        total_hours=Decimal("48.00"),
        unit_price=Decimal("150.00"),
        total_amount=Decimal("7200.00"),
        start_date=date.today(),
        session=db_session
    )
    await db_session.commit()

    # 第一次支付 3600 元
    payment1 = await PaymentService.create_payment(
        payment_data=PaymentCreate(
            payment_no="PAY20250214002",
            contract_id=contract.id,
            amount=Decimal("3600.00"),
            payment_method=1,
            hours=Decimal("24.00"),
            remark="第一期"
        ),
        session=db_session
    )
    await db_session.commit()

    confirmed1 = await PaymentService.confirm_payment(
        payment_id=payment1.id,
        hours=Decimal("24.00"),
        remark="第一期已收",
        session=db_session
    )
    await db_session.commit()

    # 第二次支付 3600 元
    payment2 = await PaymentService.create_payment(
        payment_data=PaymentCreate(
            payment_no="PAY20250214003",
            contract_id=contract.id,
            amount=Decimal("3600.00"),
            payment_method=2,  # 支付宝
            hours=Decimal("24.00"),
            remark="第二期"
        ),
        session=db_session
    )
    await db_session.commit()

    confirmed2 = await PaymentService.confirm_payment(
        payment_id=payment2.id,
        hours=Decimal("24.00"),
        remark="第二期已收",
        session=db_session
    )
    await db_session.commit()

    # 验证合同已收金额
    contract = await ContractService.get_contract_by_id(contract.id, db_session)
    assert contract.received_amount == Decimal("7200.00")

    print("\n✅ 分期支付流程测试通过！")


@pytest.mark.asyncio
@pytest.mark.skip(reason="需要完整的数据库和支付配置，集成测试在CI中运行")
async def test_refund_flow(db_session: AsyncSession):
    """测试退款流程

    流程步骤：
    1. 创建学员和合同
    2. 确认支付
    3. 申请退款
    4. 处理退款
    5. 验证合同状态
    """
    # 创建学员和课程
    student = await StudentService.create_student(
        student_data=StudentCreate(
            name="退款测试学员",
            mobile="13800138007"
        ),
        session=db_session
    )
    await db_session.commit()

    course = await CourseService.create_course(
        course_data=CourseCreate(
            name="退款测试课程",
            category="测试",
            duration=90,
            max_students=20
        ),
        session=db_session
    )
    await db_session.commit()

    contract = await ContractService.create_contract(
        contract_no="CT20250214007",
        student_id=student.id,
        course_id=course.id,
        package_type="48课时",
        total_hours=Decimal("48.00"),
        unit_price=Decimal("150.00"),
        total_amount=Decimal("7200.00"),
        start_date=date.today(),
        session=db_session
    )
    await db_session.commit()

    # 确认支付
    payment = await PaymentService.create_payment(
        payment_data=PaymentCreate(
            payment_no="PAY20250214004",
            contract_id=contract.id,
            amount=Decimal("7200.00"),
            payment_method=1,
            hours=Decimal("48.00"),
            remark="全额付款"
        ),
        session=db_session
    )
    await db_session.commit()

    confirmed = await PaymentService.confirm_payment(
        payment_id=payment.id,
        hours=Decimal("48.00"),
        remark="已收款",
        session=db_session
    )
    await db_session.commit()

    # 申请退款
    refund = await PaymentService.refund_payment(
        payment_id=payment.id,
        refund_amount=Decimal("3600.00"),
        refund_hours=Decimal("24.00"),
        refund_reason="学员退费一半",
        session=db_session
    )
    await db_session.commit()
    assert refund.status == 3  # 已退款

    print("\n✅ 退款流程测试通过！")


@pytest.mark.asyncio
@pytest.mark.skip(reason="需要完整的数据库和支付配置，集成测试在CI中运行")
async def test_payment_list_and_filter(db_session: AsyncSession):
    """测试支付列表和筛选

    测试支付记录的查询和筛选功能
    """
    # 创建测试数据
    student = await StudentService.create_student(
        student_data=StudentCreate(
            name="筛选测试学员",
            mobile="13800138008"
        ),
        session=db_session
    )
    await db_session.commit()

    course = await CourseService.create_course(
        course_data=CourseCreate(
            name="筛选测试课程",
            category="测试",
            duration=90,
            max_students=20
        ),
        session=db_session
    )
    await db_session.commit()

    contract = await ContractService.create_contract(
        contract_no="CT20250214008",
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

    # 创建多笔支付
    for i in range(3):
        payment = await PaymentService.create_payment(
            payment_data=PaymentCreate(
                payment_no=f"PAY2025021401{i}",
                contract_id=contract.id,
                amount=Decimal("1200.00"),
                payment_method=i + 1,
                hours=Decimal("8.00"),
                remark=f"第{i+1}期"
            ),
            session=db_session
        )
        await db_session.commit()

    # 按状态筛选
    pending = await PaymentService.get_all_payments(
        session=db_session,
        status=1
    )
    assert len(pending) >= 3

    # 确认所有支付
    payments = await PaymentService.get_all_payments(session=db_session)
    for p in payments:
        if p.status == 1:
            await PaymentService.confirm_payment(
                payment_id=p.id,
                hours=p.hours,
                session=db_session
            )
            await db_session.commit()

    # 再次筛选已确认
    confirmed = await PaymentService.get_all_payments(
        session=db_session,
        status=2
    )
    assert len(confirmed) >= 3

    print("\n✅ 支付列表和筛选测试通过！")
