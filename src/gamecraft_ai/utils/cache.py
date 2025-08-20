import json
import time
from typing import Any

from ..config import settings


class CacheService:
    """Simple caching service with TTL support"""

    def __init__(self):
        # Simple in-memory cache for MVP
        # In production, this would use Redis
        self._cache: dict[str, dict[str, Any]] = {}
        self._use_redis = hasattr(settings, "redis_url") and settings.redis_url

        if self._use_redis:
            try:
                import redis

                self._redis = redis.from_url(settings.redis_url)
                self._redis.ping()  # Test connection
            except Exception as e:
                print(f"Redis connection failed, using memory cache: {e}")
                self._use_redis = False

    def get(self, key: str) -> Any | None:
        """Get value from cache"""
        try:
            if self._use_redis:
                return self._get_redis(key)
            else:
                return self._get_memory(key)
        except Exception as e:
            print(f"Cache get error: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache with TTL"""
        try:
            if self._use_redis:
                return self._set_redis(key, value, ttl)
            else:
                return self._set_memory(key, value, ttl)
        except Exception as e:
            print(f"Cache set error: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            if self._use_redis:
                return bool(self._redis.delete(key))
            else:
                if key in self._cache:
                    del self._cache[key]
                    return True
                return False
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False

    def clear(self) -> bool:
        """Clear all cache"""
        try:
            if self._use_redis:
                return bool(self._redis.flushdb())
            else:
                self._cache.clear()
                return True
        except Exception as e:
            print(f"Cache clear error: {e}")
            return False

    def _get_memory(self, key: str) -> Any | None:
        """Get from memory cache"""
        if key not in self._cache:
            return None

        cache_entry = self._cache[key]

        # Check TTL
        if time.time() > cache_entry["expires"]:
            del self._cache[key]
            return None

        return cache_entry["value"]

    def _set_memory(self, key: str, value: Any, ttl: int) -> bool:
        """Set in memory cache"""
        self._cache[key] = {"value": value, "expires": time.time() + ttl, "created": time.time()}
        return True

    def _get_redis(self, key: str) -> Any | None:
        """Get from Redis cache"""
        cached = self._redis.get(key)
        if cached:
            return json.loads(cached)
        return None

    def _set_redis(self, key: str, value: Any, ttl: int) -> bool:
        """Set in Redis cache"""
        serialized = json.dumps(value, default=str)
        return bool(self._redis.setex(key, ttl, serialized))

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics"""
        if self._use_redis:
            try:
                info = self._redis.info("memory")
                return {
                    "type": "redis",
                    "memory_used": info.get("used_memory_human", "N/A"),
                    "keys": self._redis.dbsize(),
                }
            except Exception:
                return {"type": "redis", "status": "error"}
        else:
            # Memory cache stats
            total_entries = len(self._cache)
            expired_entries = 0
            current_time = time.time()

            for cache_entry in self._cache.values():
                if current_time > cache_entry["expires"]:
                    expired_entries += 1

            return {
                "type": "memory",
                "total_entries": total_entries,
                "active_entries": total_entries - expired_entries,
                "expired_entries": expired_entries,
            }
