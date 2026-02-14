"""SQLModel Database Connection

数据库连接管理
"""
from sqlmodel import SQLModel, create_engine, Session

from app.core.config import settings


# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)


def get_session():
    """获取数据库会话"""
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """创建数据库和表"""
    SQLModel.metadata.create_all(engine)


def get_db():
    """依赖注入获取数据库会话"""
    with Session(engine) as session:
        yield session
