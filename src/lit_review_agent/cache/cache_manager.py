"""Cache manager for coordinating different caching strategies."""

import asyncio
from typing import Any, Optional, Dict, List, Union
from datetime import datetime, timedelta

from .redis_cache import RedisCache, CacheError
from ..utils.logger import get_logger
from ..utils.config import Config

logger = get_logger(__name__)


class CacheManager:
    """Central cache manager for the literature review agent."""
    
    def __init__(self, config: Config):
        self.config = config
        self.redis_cache: Optional[RedisCache] = None
        self._initialized = False
        
        # Cache TTL configurations by data type
        self.cache_ttls = {
            "search_results": 1800,  # 30 minutes
            "paper_metadata": 7200,  # 2 hours
            "embeddings": 86400,     # 24 hours
            "llm_responses": 3600,   # 1 hour
            "api_responses": 1800,   # 30 minutes
            "user_sessions": 3600,   # 1 hour
            "health_checks": 300,    # 5 minutes
        }
    
    async def initialize(self) -> bool:
        """Initialize cache connections."""
        try:
            # Initialize Redis cache
            redis_url = getattr(self.config, 'redis_url', 'redis://localhost:6379')
            self.redis_cache = RedisCache(
                redis_url=redis_url,
                default_ttl=self.cache_ttls["api_responses"],
                key_prefix="litreview:v1:"
            )
            
            await self.redis_cache.connect()
            self._initialized = True
            
            logger.info("Cache manager initialized successfully")
            return True
            
        except Exception as e:
            logger.warning(f"Cache manager initialization failed: {e}")
            self._initialized = False
            return False
    
    async def shutdown(self) -> None:
        """Shutdown cache connections."""
        if self.redis_cache:
            await self.redis_cache.disconnect()
        self._initialized = False
        logger.info("Cache manager shutdown completed")
    
    def _get_cache_key(self, category: str, identifier: Union[str, Dict]) -> str:
        """Generate standardized cache keys."""
        if isinstance(identifier, dict):
            # Sort dictionary for consistent hashing
            sorted_items = sorted(identifier.items())
            identifier = str(sorted_items)
        
        return f"{category}:{identifier}"
    
    async def get_search_results(self, query: str, source: str = "all") -> Optional[Dict]:
        """Get cached search results."""
        if not self._initialized or not self.redis_cache:
            return None
        
        cache_key = self._get_cache_key("search", {"query": query, "source": source})
        return await self.redis_cache.get(cache_key)
    
    async def cache_search_results(
        self, 
        query: str, 
        source: str, 
        results: Dict,
        ttl: Optional[int] = None
    ) -> bool:
        """Cache search results."""
        if not self._initialized or not self.redis_cache:
            return False
        
        cache_key = self._get_cache_key("search", {"query": query, "source": source})
        ttl = ttl or self.cache_ttls["search_results"]
        
        return await self.redis_cache.set(
            cache_key, 
            results, 
            ttl=ttl,
            tags=["search_results", source]
        )
    
    async def get_paper_metadata(self, paper_id: str, source: str) -> Optional[Dict]:
        """Get cached paper metadata."""
        if not self._initialized or not self.redis_cache:
            return None
        
        cache_key = self._get_cache_key("paper", {"id": paper_id, "source": source})
        return await self.redis_cache.get(cache_key)
    
    async def cache_paper_metadata(
        self, 
        paper_id: str, 
        source: str, 
        metadata: Dict,
        ttl: Optional[int] = None
    ) -> bool:
        """Cache paper metadata."""
        if not self._initialized or not self.redis_cache:
            return False
        
        cache_key = self._get_cache_key("paper", {"id": paper_id, "source": source})
        ttl = ttl or self.cache_ttls["paper_metadata"]
        
        return await self.redis_cache.set(
            cache_key, 
            metadata, 
            ttl=ttl,
            tags=["paper_metadata", source]
        )
    
    async def get_embeddings(self, text_hash: str) -> Optional[List[float]]:
        """Get cached embeddings."""
        if not self._initialized or not self.redis_cache:
            return None
        
        cache_key = self._get_cache_key("embeddings", text_hash)
        return await self.redis_cache.get(cache_key)
    
    async def cache_embeddings(
        self, 
        text_hash: str, 
        embeddings: List[float],
        ttl: Optional[int] = None
    ) -> bool:
        """Cache embeddings."""
        if not self._initialized or not self.redis_cache:
            return False
        
        cache_key = self._get_cache_key("embeddings", text_hash)
        ttl = ttl or self.cache_ttls["embeddings"]
        
        return await self.redis_cache.set(
            cache_key, 
            embeddings, 
            ttl=ttl,
            tags=["embeddings"]
        )
    
    async def get_llm_response(self, prompt_hash: str, model: str) -> Optional[Dict]:
        """Get cached LLM response."""
        if not self._initialized or not self.redis_cache:
            return None
        
        cache_key = self._get_cache_key("llm", {"hash": prompt_hash, "model": model})
        return await self.redis_cache.get(cache_key)
    
    async def cache_llm_response(
        self, 
        prompt_hash: str, 
        model: str, 
        response: Dict,
        ttl: Optional[int] = None
    ) -> bool:
        """Cache LLM response."""
        if not self._initialized or not self.redis_cache:
            return False
        
        cache_key = self._get_cache_key("llm", {"hash": prompt_hash, "model": model})
        ttl = ttl or self.cache_ttls["llm_responses"]
        
        return await self.redis_cache.set(
            cache_key, 
            response, 
            ttl=ttl,
            tags=["llm_responses", model]
        )
    
    async def get_api_response(self, endpoint: str, params_hash: str) -> Optional[Dict]:
        """Get cached API response."""
        if not self._initialized or not self.redis_cache:
            return None
        
        cache_key = self._get_cache_key("api", {"endpoint": endpoint, "params": params_hash})
        return await self.redis_cache.get(cache_key)
    
    async def cache_api_response(
        self, 
        endpoint: str, 
        params_hash: str, 
        response: Dict,
        ttl: Optional[int] = None
    ) -> bool:
        """Cache API response."""
        if not self._initialized or not self.redis_cache:
            return False
        
        cache_key = self._get_cache_key("api", {"endpoint": endpoint, "params": params_hash})
        ttl = ttl or self.cache_ttls["api_responses"]
        
        return await self.redis_cache.set(
            cache_key, 
            response, 
            ttl=ttl,
            tags=["api_responses", endpoint.split("/")[0]]
        )
    
    async def invalidate_search_cache(self, source: Optional[str] = None) -> int:
        """Invalidate search results cache."""
        if not self._initialized or not self.redis_cache:
            return 0
        
        if source:
            return await self.redis_cache.invalidate_by_tag(source)
        else:
            return await self.redis_cache.invalidate_by_tag("search_results")
    
    async def invalidate_paper_cache(self, source: Optional[str] = None) -> int:
        """Invalidate paper metadata cache."""
        if not self._initialized or not self.redis_cache:
            return 0
        
        if source:
            return await self.redis_cache.invalidate_by_tag(source)
        else:
            return await self.redis_cache.invalidate_by_tag("paper_metadata")
    
    async def invalidate_llm_cache(self, model: Optional[str] = None) -> int:
        """Invalidate LLM response cache."""
        if not self._initialized or not self.redis_cache:
            return 0
        
        if model:
            return await self.redis_cache.invalidate_by_tag(model)
        else:
            return await self.redis_cache.invalidate_by_tag("llm_responses")
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics."""
        if not self._initialized or not self.redis_cache:
            return {"status": "not_initialized"}
        
        try:
            redis_stats = await self.redis_cache.get_stats()
            
            return {
                "status": "active",
                "redis": redis_stats,
                "ttl_config": self.cache_ttls,
                "initialized": self._initialized
            }
            
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {"status": "error", "error": str(e)}
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform comprehensive cache health check."""
        if not self._initialized:
            return {
                "status": "unhealthy",
                "error": "Cache manager not initialized"
            }
        
        health_results = {}
        
        # Check Redis cache health
        if self.redis_cache:
            health_results["redis"] = await self.redis_cache.health_check()
        
        # Determine overall health
        all_healthy = all(
            result.get("status") == "healthy" 
            for result in health_results.values()
        )
        
        overall_status = "healthy" if all_healthy else "degraded"
        
        # Check for any unhealthy components
        any_unhealthy = any(
            result.get("status") == "unhealthy"
            for result in health_results.values()
        )
        
        if any_unhealthy:
            overall_status = "unhealthy"
        
        return {
            "status": overall_status,
            "components": health_results,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def cleanup_expired(self) -> Dict[str, int]:
        """Clean up expired cache entries (Redis handles this automatically)."""
        # Redis handles TTL automatically, but we can provide stats
        if not self._initialized or not self.redis_cache:
            return {"error": "Cache not initialized"}
        
        stats = await self.redis_cache.get_stats()
        return {
            "redis_auto_cleanup": True,
            "total_keys": stats.get("total_keys", 0),
            "message": "Redis handles TTL cleanup automatically"
        }


# Global cache manager instance (initialized in app startup)
cache_manager: Optional[CacheManager] = None


async def get_cache_manager() -> Optional[CacheManager]:
    """Get the global cache manager instance."""
    return cache_manager


async def initialize_cache(config: Config) -> CacheManager:
    """Initialize the global cache manager."""
    global cache_manager
    
    cache_manager = CacheManager(config)
    await cache_manager.initialize()
    
    return cache_manager


async def shutdown_cache() -> None:
    """Shutdown the global cache manager."""
    global cache_manager
    
    if cache_manager:
        await cache_manager.shutdown()
        cache_manager = None 