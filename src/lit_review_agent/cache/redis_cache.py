"""Redis-based caching implementation for the literature review agent."""

import json
import hashlib
import asyncio
from typing import Any, Optional, Dict, List, Union
from datetime import datetime, timedelta

import redis.asyncio as redis
from pydantic import BaseModel

from ..utils.logger import get_logger
from ..exceptions import LiteratureReviewError

logger = get_logger(__name__)


class CacheError(LiteratureReviewError):
    """Exception raised for cache-related errors."""
    pass


class CacheEntry(BaseModel):
    """Cache entry with metadata."""
    data: Any
    timestamp: datetime
    ttl_seconds: Optional[int] = None
    tags: List[str] = []
    hit_count: int = 0


class RedisCache:
    """Redis-based cache with advanced features."""
    
    def __init__(
        self, 
        redis_url: str = "redis://localhost:6379",
        default_ttl: int = 3600,  # 1 hour
        key_prefix: str = "litreview:",
        max_retries: int = 3
    ):
        self.redis_url = redis_url
        self.default_ttl = default_ttl
        self.key_prefix = key_prefix
        self.max_retries = max_retries
        self._redis: Optional[redis.Redis] = None
        self._connected = False
    
    async def connect(self) -> None:
        """Connect to Redis server."""
        try:
            self._redis = redis.from_url(
                self.redis_url,
                decode_responses=True,
                retry_on_timeout=True,
                socket_keepalive=True,
                socket_keepalive_options={}
            )
            
            # Test connection
            await self._redis.ping()
            self._connected = True
            logger.info(f"Connected to Redis at {self.redis_url}")
            
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self._connected = False
            # Don't raise exception - allow graceful degradation
    
    async def disconnect(self) -> None:
        """Disconnect from Redis server."""
        if self._redis:
            await self._redis.close()
            self._connected = False
            logger.info("Disconnected from Redis")
    
    def _generate_key(self, key: str) -> str:
        """Generate a prefixed cache key."""
        if not key:
            raise CacheError("Cache key cannot be empty")
        return f"{self.key_prefix}{key}"
    
    def _hash_key(self, key: Union[str, Dict, List]) -> str:
        """Generate a hash for complex keys."""
        if isinstance(key, str):
            return key
        
        # Convert complex objects to deterministic string
        if isinstance(key, dict):
            sorted_items = sorted(key.items())
            key_str = json.dumps(sorted_items, sort_keys=True)
        elif isinstance(key, list):
            key_str = json.dumps(sorted(key))
        else:
            key_str = str(key)
        
        return hashlib.md5(key_str.encode()).hexdigest()
    
    async def get(self, key: Union[str, Dict, List]) -> Optional[Any]:
        """Get value from cache."""
        if not self._connected or not self._redis:
            return None
        
        try:
            cache_key = self._generate_key(self._hash_key(key))
            
            # Get cache entry
            cached_data = await self._redis.get(cache_key)
            if not cached_data:
                return None
            
            # Parse cache entry
            entry_dict = json.loads(cached_data)
            entry = CacheEntry(**entry_dict)
            
            # Update hit count
            entry.hit_count += 1
            await self._redis.set(
                cache_key, 
                entry.model_dump_json(),
                ex=entry.ttl_seconds
            )
            
            logger.debug(f"Cache hit for key: {cache_key}")
            return entry.data
            
        except Exception as e:
            logger.warning(f"Cache get error for key {key}: {e}")
            return None
    
    async def set(
        self, 
        key: Union[str, Dict, List], 
        value: Any, 
        ttl: Optional[int] = None,
        tags: List[str] = None
    ) -> bool:
        """Set value in cache."""
        if not self._connected or not self._redis:
            return False
        
        try:
            cache_key = self._generate_key(self._hash_key(key))
            ttl = ttl or self.default_ttl
            
            # Create cache entry
            entry = CacheEntry(
                data=value,
                timestamp=datetime.utcnow(),
                ttl_seconds=ttl,
                tags=tags or [],
                hit_count=0
            )
            
            # Store in Redis
            await self._redis.set(
                cache_key, 
                entry.model_dump_json(),
                ex=ttl
            )
            
            # Store tags for invalidation
            if tags:
                for tag in tags:
                    tag_key = f"{self.key_prefix}tag:{tag}"
                    await self._redis.sadd(tag_key, cache_key)
                    await self._redis.expire(tag_key, ttl)
            
            logger.debug(f"Cache set for key: {cache_key}")
            return True
            
        except Exception as e:
            logger.warning(f"Cache set error for key {key}: {e}")
            return False
    
    async def delete(self, key: Union[str, Dict, List]) -> bool:
        """Delete value from cache."""
        if not self._connected or not self._redis:
            return False
        
        try:
            cache_key = self._generate_key(self._hash_key(key))
            result = await self._redis.delete(cache_key)
            
            logger.debug(f"Cache delete for key: {cache_key}")
            return result > 0
            
        except Exception as e:
            logger.warning(f"Cache delete error for key {key}: {e}")
            return False
    
    async def exists(self, key: Union[str, Dict, List]) -> bool:
        """Check if key exists in cache."""
        if not self._connected or not self._redis:
            return False
        
        try:
            cache_key = self._generate_key(self._hash_key(key))
            result = await self._redis.exists(cache_key)
            return result > 0
            
        except Exception as e:
            logger.warning(f"Cache exists error for key {key}: {e}")
            return False
    
    async def invalidate_by_tag(self, tag: str) -> int:
        """Invalidate all cache entries with a specific tag."""
        if not self._connected or not self._redis:
            return 0
        
        try:
            tag_key = f"{self.key_prefix}tag:{tag}"
            
            # Get all keys with this tag
            keys = await self._redis.smembers(tag_key)
            
            if keys:
                # Delete all keys
                deleted_count = await self._redis.delete(*keys)
                # Delete the tag set
                await self._redis.delete(tag_key)
                
                logger.info(f"Invalidated {deleted_count} cache entries with tag: {tag}")
                return deleted_count
            
            return 0
            
        except Exception as e:
            logger.warning(f"Cache invalidate by tag error for tag {tag}: {e}")
            return 0
    
    async def clear_all(self) -> bool:
        """Clear all cache entries with our prefix."""
        if not self._connected or not self._redis:
            return False
        
        try:
            # Get all keys with our prefix
            pattern = f"{self.key_prefix}*"
            keys = []
            
            async for key in self._redis.scan_iter(match=pattern):
                keys.append(key)
            
            if keys:
                deleted_count = await self._redis.delete(*keys)
                logger.info(f"Cleared {deleted_count} cache entries")
                return True
            
            return True
            
        except Exception as e:
            logger.error(f"Cache clear all error: {e}")
            return False
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        if not self._connected or not self._redis:
            return {"connected": False}
        
        try:
            # Get Redis info
            info = await self._redis.info()
            
            # Count our keys
            pattern = f"{self.key_prefix}*"
            key_count = 0
            async for _ in self._redis.scan_iter(match=pattern):
                key_count += 1
            
            return {
                "connected": True,
                "total_keys": key_count,
                "redis_version": info.get("redis_version"),
                "used_memory": info.get("used_memory_human"),
                "connected_clients": info.get("connected_clients"),
                "total_commands_processed": info.get("total_commands_processed"),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0)
            }
            
        except Exception as e:
            logger.warning(f"Cache stats error: {e}")
            return {"connected": False, "error": str(e)}
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on Redis connection."""
        try:
            if not self._redis:
                return {
                    "status": "unhealthy",
                    "error": "Redis client not initialized"
                }
            
            # Test basic operations
            test_key = f"{self.key_prefix}health_check"
            test_value = {"timestamp": datetime.utcnow().isoformat()}
            
            # Set test value
            await self._redis.set(test_key, json.dumps(test_value), ex=60)
            
            # Get test value
            retrieved = await self._redis.get(test_key)
            
            # Delete test value
            await self._redis.delete(test_key)
            
            if retrieved:
                parsed_value = json.loads(retrieved)
                if parsed_value == test_value:
                    return {
                        "status": "healthy",
                        "message": "Redis connection working properly"
                    }
            
            return {
                "status": "degraded", 
                "error": "Redis operations not working as expected"
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": f"Redis health check failed: {e}"
            }


# Cache decorators for easy usage
def cached(
    ttl: int = 3600,
    key_func: Optional[callable] = None,
    tags: List[str] = None
):
    """Decorator to cache function results."""
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            # This would be implemented with a global cache instance
            # For now, just call the function
            return await func(*args, **kwargs)
        
        def sync_wrapper(*args, **kwargs):
            # For sync functions, just call directly
            return func(*args, **kwargs)
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator 