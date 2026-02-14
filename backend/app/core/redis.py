"""Redis Cache Client

Redis缓存客户端
"""
from typing import Optional
import redis.asyncio as redis

from app.core.config import settings


class RedisClient:
    """Redis异步客户端"""

    def __init__(self):
        self._client: Optional[redis.Redis] = None

    async def get_client(self) -> redis.Redis:
        """获取Redis客户端"""
        if self._client is None:
            self._client = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
            )
        return self._client

    async def get(self, key: str) -> Optional[str]:
        """获取值"""
        client = await self.get_client()
        return await client.get(key)

    async def set(
        self,
        key: str,
        value: str,
        expire: Optional[int] = None,
    ) -> bool:
        """设置值"""
        client = await self.get_client()
        return await client.set(key, value, ex=expire)

    async def delete(self, key: str) -> int:
        """删除键"""
        client = await self.get_client()
        return await client.delete(key)

    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        client = await self.get_client()
        return await client.exists(key) > 0

    async def close(self):
        """关闭连接"""
        if self._client:
            await self._client.close()
            self._client = None


redis_client = RedisClient()
