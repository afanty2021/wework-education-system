"""定时任务模块

本模块包含系统的所有定时任务，包括：
- 到期提醒任务
- 合同到期检查任务
- 统计数据汇总任务

使用 APScheduler 进行任务调度
"""

from app.tasks.reminders import check_contract_expiry_reminders, check_class_reminders, send_birthday_greetings
from app.tasks.contract_expiry import check_and_mark_expired_contracts, calculate_remaining_value
from app.tasks.statistics import summarize_daily_attendance, summarize_daily_payments, summarize_daily_contracts

__all__ = [
    "check_contract_expiry_reminders",
    "check_class_reminders",
    "send_birthday_greetings",
    "check_and_mark_expired_contracts",
    "calculate_remaining_value",
    "summarize_daily_attendance",
    "summarize_daily_payments",
    "summarize_daily_contracts",
]
