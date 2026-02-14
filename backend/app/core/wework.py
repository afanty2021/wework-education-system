"""WeChat Work (企微) SDK Integration

企业微信SDK封装
"""
from typing import Optional, Dict, Any
import httpx

from app.core.config import settings


class WeWorkClient:
    """企业微信客户端"""

    def __init__(self):
        self.corp_id = settings.WEWORK_CORP_ID
        self.agent_id = settings.WEWORK_AGENT_ID
        self.secret = settings.WEWORK_SECRET
        self._access_token: Optional[str] = None

    async def get_access_token(self) -> str:
        """获取access_token"""
        if self._access_token:
            return self._access_token

        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {
            "corpid": self.corp_id,
            "corpsecret": self.secret,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()

            if data.get("errcode") == 0:
                self._access_token = data.get("access_token")
                return self._access_token

            raise Exception(f"Failed to get access_token: {data}")

    async def send_message(
        self,
        user_id: str,
        content: str,
        msg_type: str = "text",
    ) -> Dict[str, Any]:
        """发送应用消息"""
        access_token = await self.get_access_token()

        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send"
        params = {"access_token": access_token}

        data = {
            "touser": user_id,
            "msgtype": msg_type,
            "agentid": self.agent_id,
            msg_type: {"content": content},
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, params=params, json=data)
            return response.json()

    async def get_user_info(self, code: str) -> Dict[str, Any]:
        """通过code获取用户信息"""
        access_token = await self.get_access_token()

        url = "https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo"
        params = {
            "access_token": access_token,
            "code": code,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            return response.json()


wework_client = WeWorkClient()
