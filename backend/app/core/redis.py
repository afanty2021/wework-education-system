"""Redis Cache Client

Redis缓存客户端 - 扩展版本
支持分布式缓存、会话管理、分布式锁
"""
import json
import logging
from functools import wraps
from typing import Any, Callable, Optional, Union
from datetime import timedelta

import redis.asyncio as redis

from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisCache:
    """Redis异步缓存客户端"""

    def __init__(self):
        self._client: Optional[redis.Redis] = None

    async def get_client(self) -> redis.Redis:
        """获取Redis客户端（单例）"""
        if self._client is None:
            self._client = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
            )
        return self._client

    # ============ 基础操作 ============

    async def get(self, key: str) -> Optional[str]:
        """获取字符串值"""
        client = await self.get_client()
        return await client.get(key)

    async def set(
        self,
        key: str,
        value: str,
        expire: Optional[int] = None,
    ) -> bool:
        """设置字符串值"""
        client = await self.get_client()
        return await client.set(key, value, ex=expire)

    async def set_object(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None,
    ) -> bool:
        """设置对象（自动JSON序列化）"""
        return await self.set(key, json.dumps(value, ensure_ascii=False), expire)

    async def get_object(self, key: str) -> Optional[Any]:
        """获取对象（自动JSON反序列化）"""
        value = await self.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                logger.warning(f"Redis缓存 JSON 解析失败: {key}")
        return None

    async def delete(self, key: str) -> int:
        """删除键"""
        client = await self.get_client()
        return await client.delete(key)

    async def delete_pattern(self, pattern: str) -> int:
        """根据模式删除多个键"""
        client = await self.get_client()
        keys = await client.keys(pattern)
        if keys:
            return await client.delete(*keys)
        return 0

    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        client = await self.get_client()
        return await client.exists(key) > 0

    async def expire(self, key: str, seconds: int) -> bool:
        """设置键的过期时间"""
        client = await self.get_client()
        return await client.expire(key, seconds)

    async def ttl(self, key: str) -> int:
        """获取键的剩余过期时间（秒）"""
        client = await self.get_client()
        return await client.ttl(key)

    # ============ Hash 操作 ============

    async def hset(self, name: str, key: str, value: str) -> int:
        """设置Hash字段"""
        client = await self.get_client()
        return await client.hset(name, key, value)

    async def hget(self, name: str, key: str) -> Optional[str]:
        """获取Hash字段值"""
        client = await self.get_client()
        return await client.hget(name, key)

    async def hgetall(self, name: str) -> dict:
        """获取所有Hash字段"""
        client = await self.get_client()
        return await client.hgetall(name)

    async def hdel(self, name: str, *keys: str) -> int:
        """删除Hash字段"""
        client = await self.get_client()
        return await client.hdel(name, *keys)

    async def hexists(self, name: str, key: str) -> bool:
        """检查Hash字段是否存在"""
        client = await self.get_client()
        return await client.hexists(name, key)

    # ============ List 操作 ============

    async def lpush(self, key: str, *values: str) -> int:
        """将值推入列表左侧"""
        client = await self.get_client()
        return await client.lpush(key, *values)

    async def rpush(self, key: str, *values: str) -> int:
        """将值推入列表右侧"""
        client = await self.get_client()
        return await client.rpush(key, *values)

    async def lrange(self, key: str, start: int = 0, end: int = -1) -> list:
        """获取列表范围"""
        client = await self.get_client()
        return await client.lrange(key, start, end)

    async def lpop(self, key: str) -> Optional[str]:
        """弹出列表左侧元素"""
        client = await self.get_client()
        return await client.lpop(key)

    # ============ Set 操作 ============

    async def sadd(self, key: str, *values: str) -> int:
        """添加Set成员"""
        client = await self.get_client()
        return await client.sadd(key, *values)

    async def smembers(self, key: str) -> set:
        """获取所有Set成员"""
        client = await self.get_client()
        return await client.smembers(key)

    async def sismember(self, key: str, value: str) -> bool:
        """检查是否为Set成员"""
        client = await self.get_client()
        return await client.sismember(key, value)

    async def srem(self, key: str, *values: str) -> int:
        """移除Set成员"""
        client = await self.get_client()
        return await client.srem(key, *values)

    # ============ 分布式锁 ============

    async def lock(
        self,
        name: str,
        timeout: int = 10,
        blocking_timeout: int = 3,
    ) -> Optional["RedisLock"]:
        """获取分布式锁"""
        return RedisLock(self, name, timeout, blocking_timeout)

    # ============ 会话管理 ============

    async def set_session(
        self,
        session_id: str,
        data: dict,
        expire: int = 86400,
    ) -> bool:
        """设置会话（默认24小时）"""
        key = f"session:{session_id}"
        return await self.set_object(key, data, expire)

    async def get_session(self, session_id: str) -> Optional[dict]:
        """获取会话"""
        key = f"session:{session_id}"
        return await self.get_object(key)

    async def delete_session(self, session_id: str) -> int:
        """删除会话"""
        key = f"session:{session_id}"
        return await self.delete(key)

    async def refresh_session(self, session_id: str, expire: int = 86400) -> bool:
        """刷新会话过期时间"""
        key = f"session:{session_id}"
        return await self.expire(key, expire)

    # ============ 缓存装饰器 ============

    def cached(self, key_prefix: str, expire: int = 300):
        """缓存装饰器

        Args:
            key_prefix: 缓存键前缀
            expire: 过期时间（秒），默认5分钟

        Usage:
            @redis_cache.cached("user:", 600)
            async def get_user(user_id: int):
                return await db.get_user(user_id)
        """
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # 构建缓存键
                cache_key = f"{key_prefix}:{':'.join(map(str, args))}"
                if kwargs:
                    cache_key += f":{':'.join(f'{k}={v}' for k, v in sorted(kwargs.items()))}"

                # 尝试从缓存获取
                cached_value = await self.get_object(cache_key)
                if cached_value is not None:
                    logger.debug(f"缓存命中: {cache_key}")
                    return cached_value

                # 执行函数并缓存结果
                result = await func(*args, **kwargs)
                if result is not None:
                    await self.set_object(cache_key, result, expire)
                    logger.debug(f"缓存写入: {cache_key}")

                return result
            return wrapper
        return decorator

    # ============ 关闭连接 ============

    async def close(self):
        """关闭连接"""
        if self._client:
            await self._client.close()
            self._client = None


class RedisLock:
    """Redis分布式锁"""

    def __init__(
        self,
        cache: RedisCache,
        name: str,
        timeout: int = 10,
        blocking_timeout: int = 3,
    ):
        self.cache = cache
        self.name = f"lock:{name}"
        self.timeout = timeout
        self.blocking_timeout = blocking_timeout
        self._locked = False

    async def __aenter__(self):
        client = await self.cache.get_client()
        self._locked = await client.lock(
            self.name,
            timeout=self.timeout,
            blocking_timeout=self.blocking_timeout,
        )
        if not self._locked:
            raise RuntimeError(f"无法获取锁: {self.name}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._locked:
            client = await self.cache.get_client()
            await client.unlock(self._locked)
            self._locked = False


# 全局缓存实例
redis_cache = RedisCache()


# 便捷函数
async def get_cache() -> RedisCache:
    """获取缓存实例"""
    return redis_cache
