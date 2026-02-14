"""API Router Initialization

API v1 路由聚合
"""
from fastapi import APIRouter

from app.api.v1 import auth, courses, students, schedules, contracts, payments, attendance, homeworks

api_router = APIRouter()

# 认证模块
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"],
)

# 课程模块
api_router.include_router(
    courses.router,
    prefix="/courses",
    tags=["Courses"],
)

# 学员模块
api_router.include_router(
    students.router,
    prefix="/students",
    tags=["Students"],
)

# 排课模块
api_router.include_router(
    schedules.router,
    prefix="/schedules",
    tags=["Schedules"],
)

# 合同模块
api_router.include_router(
    contracts.router,
    prefix="/contracts",
    tags=["Contracts"],
)

# 支付模块
api_router.include_router(
    payments.router,
    prefix="/payments",
    tags=["Payments"],
)

# 考勤模块
api_router.include_router(
    attendance.router,
    prefix="/attendance",
    tags=["Attendance"],
)

# 作业模块
api_router.include_router(
    homeworks.router,
    prefix="/homeworks",
    tags=["Homeworks"],
)
