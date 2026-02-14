"""Authentication Business Logic Service

认证业务逻辑服务
"""
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.core.wework import wework_service
from app.core.security import auth_service

logger = logging.getLogger(__name__)


class AuthBusinessService:
    """认证业务服务"""

    @staticmethod
    async def wework_login(code: str, session: AsyncSession) -> str:
        """
        企业微信OAuth2登录

        流程:
        1. 用code换取用户信息
        2. 查询或创建用户
        3. 生成JWT token

        Args:
            code: 企业微信授权码
            session: 数据库会话

        Returns:
            str: JWT token
        """
        # 获取企业微信用户信息
        logger.info(f"企业微信登录: code={code[:10]}...")
        wework_user = await wework_service.get_user_info(code)

        if wework_user.get("errcode") != 0:
            logger.error(f"企业微信登录失败: {wework_user}")
            raise Exception(f"企业微信登录失败: {wework_user.get('errmsg', '未知错误')}")

        user_id = wework_user.get("userid")
        name = wework_user.get("name")
        avatar = wework_user.get("avatar")

        # 查询用户是否存在
        result = await session.execute(
            select(User).where(User.wework_id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            # 创建新用户
            logger.info(f"创建新用户: wework_id={user_id}, name={name}")
            user = User(
                wework_id=user_id,
                name=name or "未知",
                avatar=avatar,
                role="teacher",
                status=1
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

        # 生成token
        token = auth_service.create_access_token(
            data={"sub": str(user.id), "role": user.role}
        )
        logger.info(f"用户登录成功: user_id={user.id}, token生成完成")

        return token

    @staticmethod
    async def get_or_create_user(
        wework_id: str,
        name: str,
        avatar: str,
        session: AsyncSession
    ) -> User:
        """
        获取或创建用户

        Args:
            wework_id: 企业微信用户ID
            name: 用户名
            avatar: 头像URL
            session: 数据库会话

        Returns:
            User: 用户对象
        """
        result = await session.execute(
            select(User).where(User.wework_id == wework_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                wework_id=wework_id,
                name=name,
                avatar=avatar,
                role="teacher",
                status=1
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

        return user
