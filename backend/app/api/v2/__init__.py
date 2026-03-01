"""API Router Initialization

API v2 路由聚合 - 预留版本
用于未来功能扩展和 API 变更
"""
from fastapi import APIRouter

# 预留 v2 路由
# 当 v1 API 需要不兼容变更时，在此版本中添加

api_router_v2 = APIRouter(prefix="/v2")

# 示例：未来添加的新端点
# from app.api.v2 import new_endpoints
# api_router_v2.include_router(new_endpoints.router, prefix="/new", tags=["New Features"])

# 占位路由 - 标识 API v2 已预留
@api_router_v2.get("/health")
async def health_check_v2():
    """API v2 健康检查"""
    return {"status": "ok", "version": "v2", "message": "API v2 is under development"}
