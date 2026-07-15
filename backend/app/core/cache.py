import os
import redis.asyncio as redis
import logging

logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Redis connection pool
redis_pool = redis.ConnectionPool.from_url(REDIS_URL, decode_responses=True)

def get_redis_client() -> redis.Redis:
    """Returns an async Redis client for caching and rate limiting."""
    return redis.Redis(connection_pool=redis_pool)

async def get_cache(key: str) -> str:
    """Retrieves a value from cache."""
    client = get_redis_client()
    try:
        return await client.get(key)
    except Exception as e:
        logger.error(f"Redis get error: {e}")
        return None

async def set_cache(key: str, value: str, expire_seconds: int = 3600):
    """Sets a value in cache with expiration."""
    client = get_redis_client()
    try:
        await client.setex(key, expire_seconds, value)
    except Exception as e:
        logger.error(f"Redis set error: {e}")
