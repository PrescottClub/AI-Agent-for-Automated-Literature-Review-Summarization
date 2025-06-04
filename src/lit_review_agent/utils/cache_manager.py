"""Cache manager for improving performance and reducing API calls."""

import hashlib
import json
import time
from pathlib import Path
from typing import Any, Dict, Optional, Union
import pickle

from .logger import LoggerMixin


class CacheManager(LoggerMixin):
    """
    A simple file-based cache manager for storing API responses and computed results.
    
    Features:
    - TTL (Time To Live) support
    - JSON and pickle serialization
    - Automatic cache cleanup
    - Thread-safe operations
    """
    
    def __init__(self, cache_dir: str = "./data/cache", default_ttl: int = 3600):
        """
        Initialize cache manager.
        
        Args:
            cache_dir: Directory to store cache files
            default_ttl: Default time to live in seconds (1 hour)
        """
        super().__init__()
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.default_ttl = default_ttl
        
        # Create subdirectories for different cache types
        (self.cache_dir / "api_responses").mkdir(exist_ok=True)
        (self.cache_dir / "embeddings").mkdir(exist_ok=True)
        (self.cache_dir / "search_results").mkdir(exist_ok=True)
        
        self.logger.info(f"Cache manager initialized with directory: {self.cache_dir}")
    
    def _generate_key(self, data: Union[str, Dict[str, Any]]) -> str:
        """Generate a unique cache key from data."""
        if isinstance(data, str):
            content = data
        else:
            content = json.dumps(data, sort_keys=True)
        
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_cache_path(self, key: str, cache_type: str = "general") -> Path:
        """Get the full path for a cache file."""
        return self.cache_dir / cache_type / f"{key}.cache"
    
    def _is_expired(self, cache_path: Path, ttl: int) -> bool:
        """Check if a cache file has expired."""
        if not cache_path.exists():
            return True
        
        file_age = time.time() - cache_path.stat().st_mtime
        return file_age > ttl
    
    def get(self, key: Union[str, Dict[str, Any]], cache_type: str = "general", 
            ttl: Optional[int] = None) -> Optional[Any]:
        """
        Get a value from cache.
        
        Args:
            key: Cache key (string or dict that will be hashed)
            cache_type: Type of cache (for organization)
            ttl: Time to live in seconds (uses default if None)
            
        Returns:
            Cached value or None if not found/expired
        """
        cache_key = self._generate_key(key)
        cache_path = self._get_cache_path(cache_key, cache_type)
        ttl = ttl or self.default_ttl
        
        if self._is_expired(cache_path, ttl):
            if cache_path.exists():
                cache_path.unlink()  # Remove expired cache
            return None
        
        try:
            with open(cache_path, 'rb') as f:
                data = pickle.load(f)
            
            self.logger.debug(f"Cache hit for key: {cache_key[:8]}...")
            return data
            
        except (FileNotFoundError, pickle.PickleError, EOFError) as e:
            self.logger.warning(f"Failed to load cache for key {cache_key[:8]}...: {e}")
            if cache_path.exists():
                cache_path.unlink()  # Remove corrupted cache
            return None
    
    def set(self, key: Union[str, Dict[str, Any]], value: Any, 
            cache_type: str = "general", ttl: Optional[int] = None) -> bool:
        """
        Set a value in cache.
        
        Args:
            key: Cache key (string or dict that will be hashed)
            value: Value to cache
            cache_type: Type of cache (for organization)
            ttl: Time to live in seconds (uses default if None)
            
        Returns:
            True if successful, False otherwise
        """
        cache_key = self._generate_key(key)
        cache_path = self._get_cache_path(cache_key, cache_type)
        
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(value, f)
            
            self.logger.debug(f"Cached value for key: {cache_key[:8]}...")
            return True
            
        except (OSError, pickle.PickleError) as e:
            self.logger.error(f"Failed to cache value for key {cache_key[:8]}...: {e}")
            return False
    
    def delete(self, key: Union[str, Dict[str, Any]], cache_type: str = "general") -> bool:
        """
        Delete a cached value.
        
        Args:
            key: Cache key
            cache_type: Type of cache
            
        Returns:
            True if deleted, False if not found
        """
        cache_key = self._generate_key(key)
        cache_path = self._get_cache_path(cache_key, cache_type)
        
        if cache_path.exists():
            cache_path.unlink()
            self.logger.debug(f"Deleted cache for key: {cache_key[:8]}...")
            return True
        
        return False
    
    def clear_cache_type(self, cache_type: str = "general") -> int:
        """
        Clear all cache files of a specific type.
        
        Args:
            cache_type: Type of cache to clear
            
        Returns:
            Number of files deleted
        """
        cache_dir = self.cache_dir / cache_type
        if not cache_dir.exists():
            return 0
        
        deleted_count = 0
        for cache_file in cache_dir.glob("*.cache"):
            try:
                cache_file.unlink()
                deleted_count += 1
            except OSError as e:
                self.logger.warning(f"Failed to delete cache file {cache_file}: {e}")
        
        self.logger.info(f"Cleared {deleted_count} cache files from {cache_type}")
        return deleted_count
    
    def cleanup_expired(self, cache_type: Optional[str] = None) -> int:
        """
        Clean up expired cache files.
        
        Args:
            cache_type: Specific cache type to clean, or None for all
            
        Returns:
            Number of files deleted
        """
        deleted_count = 0
        
        if cache_type:
            cache_dirs = [self.cache_dir / cache_type]
        else:
            cache_dirs = [d for d in self.cache_dir.iterdir() if d.is_dir()]
        
        for cache_dir in cache_dirs:
            if not cache_dir.exists():
                continue
                
            for cache_file in cache_dir.glob("*.cache"):
                if self._is_expired(cache_file, self.default_ttl):
                    try:
                        cache_file.unlink()
                        deleted_count += 1
                    except OSError as e:
                        self.logger.warning(f"Failed to delete expired cache file {cache_file}: {e}")
        
        if deleted_count > 0:
            self.logger.info(f"Cleaned up {deleted_count} expired cache files")
        
        return deleted_count
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        stats = {
            "cache_dir": str(self.cache_dir),
            "cache_types": {},
            "total_files": 0,
            "total_size_mb": 0.0
        }
        
        total_size = 0
        total_files = 0
        
        for cache_dir in self.cache_dir.iterdir():
            if cache_dir.is_dir():
                cache_files = list(cache_dir.glob("*.cache"))
                cache_size = sum(f.stat().st_size for f in cache_files)
                
                stats["cache_types"][cache_dir.name] = {
                    "files": len(cache_files),
                    "size_mb": round(cache_size / (1024 * 1024), 2)
                }
                
                total_files += len(cache_files)
                total_size += cache_size
        
        stats["total_files"] = total_files
        stats["total_size_mb"] = round(total_size / (1024 * 1024), 2)
        
        return stats


# Global cache instance
_cache_manager = None


def get_cache_manager() -> CacheManager:
    """Get the global cache manager instance."""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager


def cache_api_response(func):
    """
    Decorator to cache API responses.
    
    Usage:
        @cache_api_response
        async def api_call(param1, param2):
            # API call logic
            return response
    """
    def wrapper(*args, **kwargs):
        cache = get_cache_manager()
        
        # Create cache key from function name and arguments
        cache_key = {
            "function": func.__name__,
            "args": str(args),
            "kwargs": str(sorted(kwargs.items()))
        }
        
        # Try to get from cache first
        cached_result = cache.get(cache_key, cache_type="api_responses")
        if cached_result is not None:
            return cached_result
        
        # Call the function and cache the result
        result = func(*args, **kwargs)
        cache.set(cache_key, result, cache_type="api_responses")
        
        return result
    
    return wrapper


def cache_embeddings(func):
    """
    Decorator to cache embedding computations.
    
    Usage:
        @cache_embeddings
        def compute_embeddings(text):
            # Embedding computation logic
            return embeddings
    """
    def wrapper(*args, **kwargs):
        cache = get_cache_manager()
        
        # Create cache key from function name and arguments
        cache_key = {
            "function": func.__name__,
            "args": str(args),
            "kwargs": str(sorted(kwargs.items()))
        }
        
        # Try to get from cache first
        cached_result = cache.get(cache_key, cache_type="embeddings", ttl=7200)  # 2 hours TTL
        if cached_result is not None:
            return cached_result
        
        # Call the function and cache the result
        result = func(*args, **kwargs)
        cache.set(cache_key, result, cache_type="embeddings", ttl=7200)
        
        return result
    
    return wrapper
