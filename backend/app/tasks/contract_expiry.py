"""合同到期检查任务

提供合同到期相关的检查功能：
- 每日检查合同到期情况
- 自动标记过期合同
- 计算合同剩余价值
- 生成续费提醒
"""
import logging
from datetime import datetime, date, timedelta
from typing import List, Dict, Any
from decimal import Decimal

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contract import Contract
from app.models.student import Student
from app.core.db import async_session_maker


logger = logging.getLogger(__name__)


# ==================== 合同到期检查 ====================

async def check_and_mark_expired_contracts() -> Dict[str, Any]:
    """
    检查并标记过期合同

    每日检查合同到期情况，自动标记过期合同。

    Returns:
        dict: 检查统计信息
            - expired_count: 过期合同数量
            - marked_count: 标记为过期的数量
            - upcoming_count: 即将到期数量（30天内）
    """
    logger.info("开始检查合同到期情况")

    async with async_session_maker() as session:
        today = date.today()
        warning_days = 30
        warning_date = today + timedelta(days=warning_days)

        # 查询所有生效的合同
        active_contracts_query = select(Contract).where(
            Contract.status == 1  # 生效状态
        )

        result = await session.execute(active_contracts_query)
        active_contracts = result.scalars().all()

        expired_count = 0
        marked_count = 0
        upcoming_count = 0

        for contract in active_contracts:
            if contract.end_date:
                days_until_expiry = (contract.end_date - today).days

                # 已过期但未标记
                if days_until_expiry < 0:
                    expired_count += 1
                    contract.status = 4  # 标记为过期
                    contract.updated_at = datetime.now()
                    marked_count += 1
                    logger.info(f"标记合同为过期: contract_id={contract.id}, contract_no={contract.contract_no}")

                # 即将到期（30天内）
                elif 0 <= days_until_expiry <= warning_days:
                    upcoming_count += 1
                    logger.debug(f"合同即将到期: contract_id={contract.id}, days={days_until_expiry}")

        await session.commit()

        logger.info(
            f"合同到期检查完成: "
            f"过期={expired_count}, 标记={marked_count}, 即将到期={upcoming_count}"
        )

        return {
            "expired_count": expired_count,
            "marked_count": marked_count,
            "upcoming_count": upcoming_count,
            "total_checked": len(active_contracts)
        }


async def calculate_remaining_value() -> Dict[str, Any]:
    """
    计算所有生效合同的剩余价值

    Returns:
        dict: 统计信息
            - total_contracts: 总合同数
            - total_remaining_value: 总剩余价值
            - total_remaining_hours: 总剩余课时
            - contracts_by_student: 每个学员的合同统计
    """
    logger.info("开始计算合同剩余价值")

    async with async_session_maker() as session:
        # 查询所有生效的合同
        active_contracts_query = select(Contract).where(
            Contract.status == 1  # 生效状态
        )

        result = await session.execute(active_contracts_query)
        active_contracts = result.scalars().all()

        total_remaining_value = Decimal("0.00")
        total_remaining_hours = Decimal("0.00")
        contracts_by_student: Dict[int, Dict[str, Any]] = {}

        for contract in active_contracts:
            # 计算剩余价值
            remaining_value = contract.unit_price * contract.remaining_hours

            total_remaining_value += remaining_value
            total_remaining_hours += contract.remaining_hours

            # 按学员统计
            if contract.student_id not in contracts_by_student:
                contracts_by_student[contract.student_id] = {
                    "contract_count": 0,
                    "total_hours": Decimal("0.00"),
                    "remaining_hours": Decimal("0.00"),
                    "total_value": Decimal("0.00"),
                    "remaining_value": Decimal("0.00")
                }

            student_stats = contracts_by_student[contract.student_id]
            student_stats["contract_count"] += 1
            student_stats["total_hours"] += contract.total_hours
            student_stats["remaining_hours"] += contract.remaining_hours
            student_stats["total_value"] += contract.total_amount
            student_stats["remaining_value"] += remaining_value

        logger.info(
            f"合同剩余价值计算完成: "
            f"合同数={len(active_contracts)}, "
            f"总剩余价值=¥{total_remaining_value:.2f}, "
            f"总剩余课时={total_remaining_hours:.2f}"
        )

        return {
            "total_contracts": len(active_contracts),
            "total_remaining_value": float(total_remaining_value),
            "total_remaining_hours": float(total_remaining_hours),
            "contracts_by_student": contracts_by_student
        }


async def generate_renewal_reminders() -> Dict[str, Any]:
    """
    生成续费提醒

    为即将到期的合同生成续费提醒记录。

    Returns:
        dict: 统计信息
            - high_priority: 高优先级提醒（7天内）
            - medium_priority: 中优先级提醒（30天内）
            - low_priority: 低优先级提醒（60天内）
    """
    logger.info("开始生成续费提醒")

    async with async_session_maker() as session:
        today = date.today()

        # 定义优先级
        priorities = [
            (7, "high_priority"),    # 7天内，高优先级
            (30, "medium_priority"), # 30天内，中优先级
            (60, "low_priority")     # 60天内，低优先级
        ]

        reminders = {
            "high_priority": [],
            "medium_priority": [],
            "low_priority": []
        }

        # 查询所有生效的合同
        active_contracts_query = select(Contract).where(
            and_(
                Contract.status == 1,  # 生效状态
                Contract.end_date.isnot(None)
            )
        )

        result = await session.execute(active_contracts_query)
        active_contracts = result.scalars().all()

        for contract in active_contracts:
            if contract.end_date:
                days_until_expiry = (contract.end_date - today).days

                # 只处理即将到期的合同
                if 0 <= days_until_expiry <= 60:
                    # 获取学员信息
                    student = await session.get(Student, contract.student_id)

                    reminder_info = {
                        "contract_id": contract.id,
                        "contract_no": contract.contract_no,
                        "student_id": contract.student_id,
                        "student_name": student.name if student else "未知",
                        "end_date": contract.end_date.isoformat(),
                        "days_until_expiry": days_until_expiry,
                        "remaining_hours": float(contract.remaining_hours),
                        "remaining_value": float(contract.unit_price * contract.remaining_hours)
                    }

                    # 按优先级分类
                    for days, category in priorities:
                        if days_until_expiry <= days:
                            reminders[category].append(reminder_info)
                            break

        # 统计数量
        summary = {
            "high_priority": len(reminders["high_priority"]),
            "medium_priority": len(reminders["medium_priority"]),
            "low_priority": len(reminders["low_priority"]),
            "total": sum(len(v) for v in reminders.values())
        }

        logger.info(
            f"续费提醒生成完成: "
            f"高优先级={summary['high_priority']}, "
            f"中优先级={summary['medium_priority']}, "
            f"低优先级={summary['low_priority']}, "
            f"总计={summary['total']}"
        )

        return summary


async def get_contract_expiry_statistics(days: int = 90) -> Dict[str, Any]:
    """
    获取合同到期统计信息

    Args:
        days: 统计未来多少天的到期情况

    Returns:
        dict: 统计信息
            - by_period: 按时间段分组的统计
            - by_month: 按月份分组的统计
            - total_value_at_risk: 风险总价值
    """
    logger.info(f"开始获取合同到期统计: days={days}")

    async with async_session_maker() as session:
        today = date.today()
        end_date = today + timedelta(days=days)

        # 查询在统计期间内的生效合同
        contracts_query = select(Contract).where(
            and_(
                Contract.status == 1,  # 生效状态
                Contract.end_date.isnot(None),
                Contract.end_date >= today,
                Contract.end_date <= end_date
            )
        )

        result = await session.execute(contracts_query)
        contracts = result.scalars().all()

        # 按时间段分组（7天一组）
        by_period: Dict[str, Dict[str, Any]] = {}
        period_size = 7

        for contract in contracts:
            days_until_expiry = (contract.end_date - today).days
            period_key = f"{(days_until_expiry // period_size) * period_size + 1}-{(days_until_expiry // period_size + 1) * period_size}天"

            if period_key not in by_period:
                by_period[period_key] = {
                    "count": 0,
                    "total_value": Decimal("0.00"),
                    "remaining_hours": Decimal("0.00")
                }

            by_period[period_key]["count"] += 1
            by_period[period_key]["total_value"] += contract.total_amount
            by_period[period_key]["remaining_hours"] += contract.remaining_hours

        # 按月份分组
        by_month: Dict[str, Dict[str, Any]] = {}

        for contract in contracts:
            if contract.end_date:
                month_key = contract.end_date.strftime("%Y-%m")

                if month_key not in by_month:
                    by_month[month_key] = {
                        "count": 0,
                        "total_value": Decimal("0.00"),
                        "remaining_hours": Decimal("0.00")
                    }

                by_month[month_key]["count"] += 1
                by_month[month_key]["total_value"] += contract.total_amount
                by_month[month_key]["remaining_hours"] += contract.remaining_hours

        # 计算风险价值（60天内到期的合同价值）
        risk_end_date = today + timedelta(days=60)
        risk_contracts = [c for c in contracts if c.end_date and c.end_date <= risk_end_date]
        total_value_at_risk = sum((c.unit_price * c.remaining_hours) for c in risk_contracts)

        logger.info(
            f"合同到期统计完成: "
            f"合同数={len(contracts)}, "
            f"风险价值=¥{total_value_at_risk:.2f}"
        )

        return {
            "by_period": {
                k: {
                    "count": v["count"],
                    "total_value": float(v["total_value"]),
                    "remaining_hours": float(v["remaining_hours"])
                }
                for k, v in by_period.items()
            },
            "by_month": {
                k: {
                    "count": v["count"],
                    "total_value": float(v["total_value"]),
                    "remaining_hours": float(v["remaining_hours"])
                }
                for k, v in by_month.items()
            },
            "total_value_at_risk": float(total_value_at_risk),
            "total_contracts": len(contracts)
        }


async def cleanup_expired_contracts(days_since_expiry: int = 365) -> Dict[str, Any]:
    """
    清理过期合同数据（可选任务）

    清理指定天数前已过期的合同，可以用于归档或删除。

    Args:
        days_since_expiry: 过期多少天后的合同

    Returns:
        dict: 清理统计信息
            - archived_count: 归档数量
            - deleted_count: 删除数量
            - total_processed: 总处理数量
    """
    logger.info(f"开始清理过期合同: days_since_expiry={days_since_expiry}")

    async with async_session_maker() as session:
        today = date.today()
        cleanup_date = today - timedelta(days=days_since_expiry)

        # 查询需要清理的过期合同
        expired_contracts_query = select(Contract).where(
            and_(
                Contract.status == 4,  # 过期状态
                Contract.end_date.isnot(None),
                Contract.end_date <= cleanup_date
            )
        )

        result = await session.execute(expired_contracts_query)
        expired_contracts = result.scalars().all()

        archived_count = 0
        deleted_count = 0

        # 这里可以根据需求实现归档或删除逻辑
        # 目前只记录日志
        for contract in expired_contracts:
            logger.debug(
                f"待处理过期合同: "
                f"contract_id={contract.id}, "
                f"contract_no={contract.contract_no}, "
                f"end_date={contract.end_date}"
            )
            archived_count += 1

        logger.info(
            f"过期合同清理完成: "
            f"归档={archived_count}, "
            f"删除={deleted_count}, "
            f"总计={len(expired_contracts)}"
        )

        return {
            "archived_count": archived_count,
            "deleted_count": deleted_count,
            "total_processed": len(expired_contracts)
        }
