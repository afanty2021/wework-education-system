"""WeChat Work (企业微信) API Service

企业微信API服务

功能:
- 获取access_token（带缓存）
- 通过授权码获取用户信息
- 发送文本/卡片消息
"""
import logging
from typing import Optional
from datetime import datetime, timedelta
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)


class WeWorkService:
    """企业微信API服务"""

    def __init__(self):
        self.corp_id = settings.WEWORK_CORP_ID
        self.corp_secret = settings.WEWORK_SECRET
        self.agent_id = settings.WEWORK_AGENT_ID
        self._access_token: Optional[str] = None
        self._token_expire: Optional[datetime] = None

    async def get_access_token(self) -> str:
        """
        获取access_token（带内存缓存）

        Returns:
            str: access_token

        Raises:
            Exception: 获取失败时抛出
        """
        # 检查缓存
        if self._access_token and self._token_expire:
            if datetime.now() < self._token_expire:
                logger.debug("使用缓存的access_token")
                return self._access_token

        # 调用API
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {
            "corpid": self.corp_id,
            "corpsecret": self.corp_secret
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10.0)
            data = response.json()

            if data.get("errcode") == 0:
                self._access_token = data["access_token"]
                # 提前5分钟过期，确保刷新
                self._token_expire = datetime.now() + timedelta(
                    seconds=data["expires_in"] - 300
                )
                logger.info("成功获取企业微信access_token")
                return self._access_token

            logger.error(f"获取access_token失败: {data}")
            raise Exception(f"获取access_token失败: {data}")

    async def get_user_info(self, code: str) -> dict:
        """
        通过授权码获取用户信息

        Args:
            code: 企业微信授权码

        Returns:
            dict: 用户信息
        """
        token = await self.get_access_token()

        # 获取user_id
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://qyapi.weixin.qq.com/cgi-bin/auth/getuserinfo",
                params={"access_token": token, "code": code},
                timeout=10.0
            )
            data = response.json()
            if data.get("errcode") != 0:
                logger.error(f"获取用户ID失败: {data}")
                raise Exception(f"获取用户ID失败: {data}")
            user_id = data["UserId"]

        # 获取用户详情
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://qyapi.weixin.qq.com/cgi-bin/user/get",
                params={"access_token": token, "userid": user_id},
                timeout=10.0
            )
            return response.json()

    async def send_message(self, user_id: str, content: str) -> dict:
        """
        发送文本消息

        Args:
            user_id: 企业微信用户ID
            content: 消息内容

        Returns:
            dict: API响应
        """
        token = await self.get_access_token()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}",
                json={
                    "touser": user_id,
                    "msgtype": "text",
                    "agentid": self.agent_id,
                    "text": {"content": content}
                },
                timeout=10.0
            )
            return response.json()

    async def send_card_message(
        self,
        user_id: str,
        title: str,
        description: str,
        url: str
    ) -> dict:
        """
        发送卡片消息

        Args:
            user_id: 用户ID
            title: 卡片标题
            description: 卡片描述
            url: 跳转URL

        Returns:
            dict: API响应
        """
        token = await self.get_access_token()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}",
                json={
                    "touser": user_id,
                    "msgtype": "textcard",
                    "agentid": self.agent_id,
                    "textcard": {
                        "title": title,
                        "description": description,
                        "url": url
                    }
                },
                timeout=10.0
            )
            return response.json()


# 全局单例
wework_service = WeWorkService()
