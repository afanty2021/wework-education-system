"""Alembic Environment Configuration

数据库迁移环境配置
"""
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic.runtime.environment import EnvironmentContext
from alembic.script import ScriptDirectory

from sqlmodel import SQLModel
from app.core.config import settings
from app.models import *  # 导入所有模型


def run_migrations_offline() -> None:
    """离线运行迁移"""
    url = settings.DATABASE_URL
    context = EnvironmentContext(
        settings.DATABASE_URL,
        script=ScriptDirectory.from_config(config),
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """执行迁移"""
    context = EnvironmentContext(
        settings.DATABASE_URL,
        script=ScriptDirectory.from_config(config),
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """异步执行迁移"""
    connectable = async_engine_from_config(
        settings.DATABASE_URL,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_async_migrations())
