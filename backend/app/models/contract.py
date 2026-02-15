"""
合同/课时包模型

表: contracts
说明: 学员课时包合同
"""

from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, date
from decimal import Decimal


class Contract(SQLModel, table=True):
    """合同模型"""
    __tablename__ = "contracts"

    id: Optional[int] = Field(default=None, primary_key=True)
    contract_no: str = Field(max_length=50, unique=True, index=True, description="合同编号")
    student_id: int = Field(foreign_key="students.id", index=True, description="学员ID")
    course_id: Optional[int] = Field(default=None, foreign_key="courses.id", description="报读课程")
    package_type: str = Field(max_length=20, description="课时包类型: 48/72/96/自定义")
    total_hours: Decimal = Field(description="总课时数")
    remaining_hours: Decimal = Field(description="剩余课时")
    unit_price: Decimal = Field(description="单价(元/课时)")
    total_amount: Decimal = Field(description="合同总金额")
    received_amount: Decimal = Field(default=0, description="实收金额")
    discount_amount: Decimal = Field(default=0, description="优惠金额")
    start_date: date = Field(description="合同开始日期")
    end_date: Optional[date] = Field(default=None, description="合同到期日期")
    expire_warning_days: int = Field(default=30, description="到期预警天数")
    status: int = Field(default=1, index=True, description="状态: 1:生效 2:完结 3:退费 4:过期")
    contract_file: Optional[str] = Field(default=None, max_length=500, description="合同文件路径")
    sales_id: Optional[int] = Field(default=None, foreign_key="users.id", description="课程顾问")
    notes: Optional[str] = Field(default=None, description="备注")
    created_by: Optional[int] = Field(default=None, foreign_key="users.id", description="创建人")

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
