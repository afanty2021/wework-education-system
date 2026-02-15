"""SQLModel Database Connection

数据库连接管理
"""
from typing import AsyncGenerator

from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.core.config import settings


# 创建同步数据库引擎（用于管理任务和脚本）
database_url = settings.get_database_url_with_password()
sync_engine = create_engine(
    database_url,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

# 创建异步数据库引擎（用于API和业务逻辑）
# 将 postgresql:// 替换为 postgresql+asyncpg://
async_database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
async_engine = create_async_engine(
    async_database_url,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

# 创建异步会话工厂
async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """依赖注入获取异步数据库会话

    用于 FastAPI 依赖注入系统，提供数据库会话管理。
    使用示例:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with async_session_maker() as session:
        yield session


def get_sync_db():
    """依赖注入获取同步数据库会话

    用于管理任务和脚本，提供同步数据库会话。
    使用示例:
        @app.get("/admin/tasks")
        def run_task(db: Session = Depends(get_sync_db)):
            ...
    """
    with Session(sync_engine) as session:
        yield session


async def create_db_and_tables():
    """创建数据库和表（异步版本）"""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


def create_db_and_tables_sync():
    """创建数据库和表（同步版本）"""
    SQLModel.metadata.create_all(sync_engine)


def get_engine():
    """获取同步数据库引擎实例（已废弃，建议使用 async_engine）"""
    return sync_engine


async def get_async_engine():
    """获取异步数据库引擎实例"""
    return async_engine
