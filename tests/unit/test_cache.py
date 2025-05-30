"""Unit tests for caching system."""

import pytest
import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta

from src.lit_review_agent.cache.redis_cache import RedisCache, CacheEntry, CacheError
from src.lit_review_agent.cache.cache_manager import CacheManager
from src.lit_review_agent.utils.config import Config


@pytest.mark.unit
class TestCacheEntry:
    """Test CacheEntry model."""

    def test_cache_entry_creation(self):
        """Test basic cache entry creation."""
        entry = CacheEntry(
            data={"test": "value"},
            timestamp=datetime.utcnow(),
            ttl_seconds=3600,
            tags=["test_tag"],
            hit_count=5
        )
        
        assert entry.data == {"test": "value"}
        assert entry.ttl_seconds == 3600
        assert entry.tags == ["test_tag"]
        assert entry.hit_count == 5

    def test_cache_entry_defaults(self):
        """Test cache entry with default values."""
        timestamp = datetime.utcnow()
        entry = CacheEntry(
            data="test_data",
            timestamp=timestamp
        )
        
        assert entry.data == "test_data"
        assert entry.timestamp == timestamp
        assert entry.ttl_seconds is None
        assert entry.tags == []
        assert entry.hit_count == 0


@pytest.mark.unit
class TestRedisCache:
    """Test RedisCache implementation."""

    def test_init(self):
        """Test Redis cache initialization."""
        cache = RedisCache(
            redis_url="redis://localhost:6380",
            default_ttl=7200,
            key_prefix="test:",
            max_retries=5
        )
        
        assert cache.redis_url == "redis://localhost:6380"
        assert cache.default_ttl == 7200
        assert cache.key_prefix == "test:"
        assert cache.max_retries == 5
        assert not cache._connected

    def test_generate_key(self):
        """Test cache key generation."""
        cache = RedisCache()
        
        key = cache._generate_key("test_key")
        assert key == "litreview:test_key"
        
        # Test empty key
        with pytest.raises(CacheError):
            cache._generate_key("")

    def test_hash_key_string(self):
        """Test key hashing for strings."""
        cache = RedisCache()
        
        hashed = cache._hash_key("simple_key")
        assert hashed == "simple_key"

    def test_hash_key_dict(self):
        """Test key hashing for dictionaries."""
        cache = RedisCache()
        
        test_dict = {"b": 2, "a": 1}
        hashed = cache._hash_key(test_dict)
        
        # Should be deterministic
        assert hashed == cache._hash_key({"a": 1, "b": 2})
        assert len(hashed) == 32  # MD5 hash length

    def test_hash_key_list(self):
        """Test key hashing for lists."""
        cache = RedisCache()
        
        test_list = ["b", "a", "c"]
        hashed = cache._hash_key(test_list)
        
        # Should be deterministic (sorted)
        assert hashed == cache._hash_key(["a", "b", "c"])
        assert len(hashed) == 32  # MD5 hash length

    @pytest.mark.asyncio
    async def test_connect_success(self):
        """Test successful Redis connection."""
        mock_redis = MagicMock()
        mock_redis.ping = AsyncMock()
        
        with patch('src.lit_review_agent.cache.redis_cache.redis.from_url', return_value=mock_redis):
            cache = RedisCache()
            await cache.connect()
            
            assert cache._connected
            mock_redis.ping.assert_called_once()

    @pytest.mark.asyncio
    async def test_connect_failure(self):
        """Test Redis connection failure."""
        mock_redis = MagicMock()
        mock_redis.ping = AsyncMock(side_effect=Exception("Connection error"))
        
        with patch('src.lit_review_agent.cache.redis_cache.redis.from_url', return_value=mock_redis):
            cache = RedisCache()
            await cache.connect()
            
            assert not cache._connected

    @pytest.mark.asyncio
    async def test_get_not_connected(self):
        """Test get when not connected."""
        cache = RedisCache()
        result = await cache.get("test_key")
        assert result is None

    @pytest.mark.asyncio
    async def test_get_success(self):
        """Test successful cache get."""
        mock_redis = AsyncMock()
        test_entry = CacheEntry(
            data="test_value",
            timestamp=datetime.utcnow(),
            ttl_seconds=3600,
            hit_count=0
        )
        mock_redis.get.return_value = test_entry.model_dump_json()
        mock_redis.set = AsyncMock()
        
        cache = RedisCache()
        cache._redis = mock_redis
        cache._connected = True
        
        result = await cache.get("test_key")
        
        assert result == "test_value"
        mock_redis.get.assert_called_once()
        mock_redis.set.assert_called_once()  # For hit count update

    @pytest.mark.asyncio
    async def test_get_not_found(self):
        """Test cache get when key not found."""
        mock_redis = AsyncMock()
        mock_redis.get.return_value = None
        
        cache = RedisCache()
        cache._redis = mock_redis
        cache._connected = True
        
        result = await cache.get("nonexistent_key")
        assert result is None

    @pytest.mark.asyncio
    async def test_get_error(self):
        """Test cache get with error."""
        mock_redis = AsyncMock()
        mock_redis.get.side_effect = Exception("Redis error")
        
        cache = RedisCache()
        cache._redis = mock_redis
        cache._connected = True
        
        result = await cache.get("test_key")
        assert result is None

    @pytest.mark.asyncio
    async def test_set_success(self):
        """Test successful cache set."""
        mock_redis = AsyncMock()
        mock_redis.set = AsyncMock()
        mock_redis.sadd = AsyncMock()
        mock_redis.expire = AsyncMock()
        
        cache = RedisCache()
        cache._redis = mock_redis
        cache._connected = True
        
        result = await cache.set("test_key", "test_value", ttl=1800, tags=["tag1"])
        
        assert result is True
        mock_redis.set.assert_called_once()
        mock_redis.sadd.assert_called_once()
        mock_redis.expire.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_not_connected(self):
        """Test set when not connected."""
        cache = RedisCache()
        result = await cache.set("test_key", "test_value")
        assert result is False

    @pytest.mark.asyncio
    async def test_delete_success(self):
        """Test successful cache delete."""
        mock_redis = AsyncMock()
        mock_redis.delete.return_value = 1
        
        cache = RedisCache()
        cache._redis = mock_redis
        cache._connected = True
        
        result = await cache.delete("test_key")
        assert result is True

    @pytest.mark.asyncio
    async def test_exists_success(self):
        """Test successful cache exists check."""
        mock_redis = AsyncMock()
        mock_redis.exists.return_value = 1
        
        cache = RedisCache()
        cache._redis = mock_redis
        cache._connected = True
        
        result = await cache.exists("test_key")
        assert result is True

    @pytest.mark.asyncio
    async def test_invalidate_by_tag(self):
        """Test cache invalidation by tag."""
        mock_redis = AsyncMock()
        mock_redis.smembers.return_value = ["key1", "key2", "key3"]
        mock_redis.delete.return_value = 3
        
        cache = RedisCache()
        cache._redis = mock_redis
        cache._connected = True
        
        result = await cache.invalidate_by_tag("test_tag")
        assert result == 3

    @pytest.mark.asyncio
    async def test_clear_all(self):
        """Test clearing all cache entries."""
        mock_redis = AsyncMock()
        mock_redis.scan_iter.return_value = AsyncMock()
        mock_redis.scan_iter.return_value.__aiter__ = AsyncMock(
            return_value=iter(["key1", "key2", "key3"])
        )
        mock_redis.delete.return_value = 3
        
        cache = RedisCache()
        cache._redis = mock_redis
        cache._connected = True
        
        result = await cache.clear_all()
        assert result is True

    @pytest.mark.asyncio
    async def test_get_stats(self):
        """Test getting cache statistics."""
        mock_redis = AsyncMock()
        mock_redis.info.return_value = {
            "redis_version": "7.0.0",
            "used_memory_human": "1.5M",
            "connected_clients": 5,
            "total_commands_processed": 1000,
            "keyspace_hits": 800,
            "keyspace_misses": 200
        }
        mock_redis.scan_iter.return_value = AsyncMock()
        mock_redis.scan_iter.return_value.__aiter__ = AsyncMock(
            return_value=iter(["key1", "key2"])
        )
        
        cache = RedisCache()
        cache._redis = mock_redis
        cache._connected = True
        
        stats = await cache.get_stats()
        
        assert stats["connected"] is True
        assert stats["total_keys"] == 2
        assert stats["redis_version"] == "7.0.0"

    @pytest.mark.asyncio
    async def test_health_check_healthy(self):
        """Test healthy cache health check."""
        mock_redis = AsyncMock()
        mock_redis.set = AsyncMock()
        mock_redis.get.return_value = '{"timestamp": "2025-01-28T10:00:00"}'
        mock_redis.delete = AsyncMock()
        
        cache = RedisCache()
        cache._redis = mock_redis
        cache._connected = True
        
        result = await cache.health_check()
        
        assert result["status"] == "healthy"
        assert "working properly" in result["message"]

    @pytest.mark.asyncio
    async def test_health_check_unhealthy(self):
        """Test unhealthy cache health check."""
        cache = RedisCache()
        # No Redis client initialized
        
        result = await cache.health_check()
        
        assert result["status"] == "unhealthy"
        assert "not initialized" in result["error"]


@pytest.mark.unit
class TestCacheManager:
    """Test CacheManager implementation."""

    def test_init(self):
        """Test cache manager initialization."""
        config = Config()
        manager = CacheManager(config)
        
        assert manager.config == config
        assert manager.redis_cache is None
        assert not manager._initialized
        assert isinstance(manager.cache_ttls, dict)

    def test_get_cache_key_string(self):
        """Test cache key generation for strings."""
        config = Config()
        manager = CacheManager(config)
        
        key = manager._get_cache_key("search", "machine learning")
        assert key == "search:machine learning"

    def test_get_cache_key_dict(self):
        """Test cache key generation for dictionaries."""
        config = Config()
        manager = CacheManager(config)
        
        identifier = {"query": "ML", "source": "arxiv"}
        key = manager._get_cache_key("search", identifier)
        assert "search:" in key
        assert "query" in key
        assert "source" in key

    @pytest.mark.asyncio
    async def test_initialize_success(self):
        """Test successful cache manager initialization."""
        config = Config()
        manager = CacheManager(config)
        
        mock_redis_cache = AsyncMock()
        mock_redis_cache.connect = AsyncMock()
        
        with patch('src.lit_review_agent.cache.cache_manager.RedisCache', return_value=mock_redis_cache):
            result = await manager.initialize()
            
            assert result is True
            assert manager._initialized
            assert manager.redis_cache == mock_redis_cache

    @pytest.mark.asyncio
    async def test_initialize_failure(self):
        """Test cache manager initialization failure."""
        config = Config()
        manager = CacheManager(config)
        
        with patch('src.lit_review_agent.cache.cache_manager.RedisCache', side_effect=Exception("Init error")):
            result = await manager.initialize()
            
            assert result is False
            assert not manager._initialized

    @pytest.mark.asyncio
    async def test_get_search_results_not_initialized(self):
        """Test getting search results when not initialized."""
        config = Config()
        manager = CacheManager(config)
        
        result = await manager.get_search_results("test query")
        assert result is None

    @pytest.mark.asyncio
    async def test_cache_search_results_success(self):
        """Test caching search results successfully."""
        config = Config()
        manager = CacheManager(config)
        manager._initialized = True
        
        mock_redis_cache = AsyncMock()
        mock_redis_cache.set.return_value = True
        manager.redis_cache = mock_redis_cache
        
        results = {"papers": ["paper1", "paper2"]}
        success = await manager.cache_search_results("ML query", "arxiv", results)
        
        assert success is True
        mock_redis_cache.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_paper_metadata(self):
        """Test getting cached paper metadata."""
        config = Config()
        manager = CacheManager(config)
        manager._initialized = True
        
        mock_redis_cache = AsyncMock()
        mock_redis_cache.get.return_value = {"title": "Test Paper"}
        manager.redis_cache = mock_redis_cache
        
        metadata = await manager.get_paper_metadata("paper123", "arxiv")
        
        assert metadata == {"title": "Test Paper"}
        mock_redis_cache.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_cache_embeddings(self):
        """Test caching embeddings."""
        config = Config()
        manager = CacheManager(config)
        manager._initialized = True
        
        mock_redis_cache = AsyncMock()
        mock_redis_cache.set.return_value = True
        manager.redis_cache = mock_redis_cache
        
        embeddings = [0.1, 0.2, 0.3, 0.4]
        success = await manager.cache_embeddings("text_hash_123", embeddings)
        
        assert success is True
        mock_redis_cache.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_llm_response(self):
        """Test getting cached LLM response."""
        config = Config()
        manager = CacheManager(config)
        manager._initialized = True
        
        mock_redis_cache = AsyncMock()
        mock_redis_cache.get.return_value = {"response": "Test response"}
        manager.redis_cache = mock_redis_cache
        
        response = await manager.get_llm_response("prompt_hash", "gpt-4")
        
        assert response == {"response": "Test response"}
        mock_redis_cache.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_invalidate_search_cache(self):
        """Test invalidating search cache."""
        config = Config()
        manager = CacheManager(config)
        manager._initialized = True
        
        mock_redis_cache = AsyncMock()
        mock_redis_cache.invalidate_by_tag.return_value = 5
        manager.redis_cache = mock_redis_cache
        
        count = await manager.invalidate_search_cache("arxiv")
        
        assert count == 5
        mock_redis_cache.invalidate_by_tag.assert_called_once_with("arxiv")

    @pytest.mark.asyncio
    async def test_get_cache_stats(self):
        """Test getting cache statistics."""
        config = Config()
        manager = CacheManager(config)
        manager._initialized = True
        
        mock_redis_cache = AsyncMock()
        mock_redis_cache.get_stats.return_value = {"connected": True, "total_keys": 100}
        manager.redis_cache = mock_redis_cache
        
        stats = await manager.get_cache_stats()
        
        assert stats["status"] == "active"
        assert stats["redis"]["total_keys"] == 100
        assert "ttl_config" in stats

    @pytest.mark.asyncio
    async def test_health_check_not_initialized(self):
        """Test health check when not initialized."""
        config = Config()
        manager = CacheManager(config)
        
        result = await manager.health_check()
        
        assert result["status"] == "unhealthy"
        assert "not initialized" in result["error"]

    @pytest.mark.asyncio
    async def test_health_check_healthy(self):
        """Test healthy cache health check."""
        config = Config()
        manager = CacheManager(config)
        manager._initialized = True
        
        mock_redis_cache = AsyncMock()
        mock_redis_cache.health_check.return_value = {"status": "healthy"}
        manager.redis_cache = mock_redis_cache
        
        result = await manager.health_check()
        
        assert result["status"] == "healthy"
        assert "redis" in result["components"]

    @pytest.mark.asyncio
    async def test_health_check_degraded(self):
        """Test degraded cache health check."""
        config = Config()
        manager = CacheManager(config)
        manager._initialized = True
        
        mock_redis_cache = AsyncMock()
        mock_redis_cache.health_check.return_value = {"status": "degraded"}
        manager.redis_cache = mock_redis_cache
        
        result = await manager.health_check()
        
        assert result["status"] == "degraded"
        assert "components" in result

    @pytest.mark.asyncio
    async def test_cleanup_expired(self):
        """Test cleaning up expired cache entries."""
        config = Config()
        manager = CacheManager(config)
        manager._initialized = True
        
        mock_redis_cache = AsyncMock()
        mock_redis_cache.get_stats.return_value = {"total_keys": 150}
        manager.redis_cache = mock_redis_cache
        
        result = await manager.cleanup_expired()
        
        assert result["redis_auto_cleanup"] is True
        assert result["total_keys"] == 150
        assert "automatically" in result["message"]

    @pytest.mark.asyncio
    async def test_shutdown(self):
        """Test cache manager shutdown."""
        config = Config()
        manager = CacheManager(config)
        
        mock_redis_cache = AsyncMock()
        mock_redis_cache.disconnect = AsyncMock()
        manager.redis_cache = mock_redis_cache
        manager._initialized = True
        
        await manager.shutdown()
        
        assert not manager._initialized
        mock_redis_cache.disconnect.assert_called_once()


@pytest.mark.unit  
class TestCacheIntegration:
    """Test cache system integration."""

    @pytest.mark.asyncio
    async def test_full_cache_workflow(self):
        """Test complete cache workflow."""
        # Mock Redis for this integration test
        mock_redis = AsyncMock()
        mock_redis.ping = AsyncMock()
        mock_redis.set = AsyncMock()
        mock_redis.get.return_value = None  # Cache miss first
        mock_redis.exists.return_value = 0
        mock_redis.delete.return_value = 1
        
        with patch('src.lit_review_agent.cache.redis_cache.redis.from_url', return_value=mock_redis):
            # Initialize cache system
            config = Config()
            manager = CacheManager(config)
            
            await manager.initialize()
            assert manager._initialized
            
            # Test cache miss
            result = await manager.get_search_results("test query", "arxiv")
            assert result is None
            
            # Test cache set
            test_results = {"papers": ["paper1", "paper2"]}
            success = await manager.cache_search_results("test query", "arxiv", test_results)
            assert success is True
            
            # Test cache hit (mock return value)
            mock_redis.get.return_value = json.dumps({
                "data": test_results,
                "timestamp": datetime.utcnow().isoformat(),
                "ttl_seconds": 1800,
                "tags": ["search_results", "arxiv"],
                "hit_count": 0
            })
            
            cached_result = await manager.get_search_results("test query", "arxiv")
            assert cached_result == test_results
            
            # Test invalidation
            invalidated = await manager.invalidate_search_cache("arxiv")
            # Should work without error
            
            # Test cleanup
            await manager.shutdown() 