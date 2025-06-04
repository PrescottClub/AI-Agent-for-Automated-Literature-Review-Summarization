"""Performance monitoring utilities for the literature review agent."""

import time
import functools
import psutil
import threading
from typing import Dict, Any, Optional, Callable
from collections import defaultdict, deque
from datetime import datetime, timedelta

from .logger import LoggerMixin


class PerformanceMetrics:
    """Container for performance metrics."""
    
    def __init__(self):
        self.execution_times = defaultdict(deque)  # Function name -> execution times
        self.api_calls = defaultdict(int)  # API endpoint -> call count
        self.memory_usage = deque(maxlen=100)  # Recent memory usage samples
        self.cpu_usage = deque(maxlen=100)  # Recent CPU usage samples
        self.error_counts = defaultdict(int)  # Error type -> count
        self.cache_stats = {"hits": 0, "misses": 0}
        
        # Keep only last 1000 execution times per function
        self.max_samples = 1000
    
    def add_execution_time(self, function_name: str, execution_time: float):
        """Add execution time for a function."""
        times = self.execution_times[function_name]
        times.append(execution_time)
        if len(times) > self.max_samples:
            times.popleft()
    
    def add_api_call(self, endpoint: str):
        """Record an API call."""
        self.api_calls[endpoint] += 1
    
    def add_error(self, error_type: str):
        """Record an error."""
        self.error_counts[error_type] += 1
    
    def add_system_metrics(self):
        """Add current system metrics."""
        try:
            # Memory usage in MB
            memory_mb = psutil.virtual_memory().used / (1024 * 1024)
            self.memory_usage.append(memory_mb)
            
            # CPU usage percentage
            cpu_percent = psutil.cpu_percent()
            self.cpu_usage.append(cpu_percent)
        except Exception:
            # Ignore errors in system monitoring
            pass
    
    def get_function_stats(self, function_name: str) -> Dict[str, Any]:
        """Get statistics for a specific function."""
        times = list(self.execution_times[function_name])
        if not times:
            return {"count": 0}
        
        return {
            "count": len(times),
            "avg_time": sum(times) / len(times),
            "min_time": min(times),
            "max_time": max(times),
            "total_time": sum(times)
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all performance metrics."""
        summary = {
            "timestamp": datetime.now().isoformat(),
            "functions": {},
            "api_calls": dict(self.api_calls),
            "errors": dict(self.error_counts),
            "cache_stats": self.cache_stats.copy(),
            "system": {}
        }
        
        # Function performance
        for func_name in self.execution_times:
            summary["functions"][func_name] = self.get_function_stats(func_name)
        
        # System metrics
        if self.memory_usage:
            summary["system"]["memory_mb"] = {
                "current": self.memory_usage[-1],
                "avg": sum(self.memory_usage) / len(self.memory_usage),
                "max": max(self.memory_usage)
            }
        
        if self.cpu_usage:
            summary["system"]["cpu_percent"] = {
                "current": self.cpu_usage[-1],
                "avg": sum(self.cpu_usage) / len(self.cpu_usage),
                "max": max(self.cpu_usage)
            }
        
        return summary


class PerformanceMonitor(LoggerMixin):
    """Performance monitoring system."""
    
    def __init__(self, enable_system_monitoring: bool = True):
        super().__init__()
        self.metrics = PerformanceMetrics()
        self.enable_system_monitoring = enable_system_monitoring
        self._monitoring_thread = None
        self._stop_monitoring = threading.Event()
        
        if enable_system_monitoring:
            self.start_system_monitoring()
    
    def start_system_monitoring(self):
        """Start background system monitoring."""
        if self._monitoring_thread and self._monitoring_thread.is_alive():
            return
        
        self._stop_monitoring.clear()
        self._monitoring_thread = threading.Thread(
            target=self._system_monitoring_loop,
            daemon=True
        )
        self._monitoring_thread.start()
        self.logger.info("Started system performance monitoring")
    
    def stop_system_monitoring(self):
        """Stop background system monitoring."""
        if self._monitoring_thread and self._monitoring_thread.is_alive():
            self._stop_monitoring.set()
            self._monitoring_thread.join(timeout=5)
            self.logger.info("Stopped system performance monitoring")
    
    def _system_monitoring_loop(self):
        """Background loop for system monitoring."""
        while not self._stop_monitoring.wait(10):  # Sample every 10 seconds
            self.metrics.add_system_metrics()
    
    def record_execution_time(self, function_name: str, execution_time: float):
        """Record execution time for a function."""
        self.metrics.add_execution_time(function_name, execution_time)
    
    def record_api_call(self, endpoint: str):
        """Record an API call."""
        self.metrics.add_api_call(endpoint)
    
    def record_error(self, error_type: str):
        """Record an error."""
        self.metrics.add_error(error_type)
    
    def record_cache_hit(self):
        """Record a cache hit."""
        self.metrics.cache_stats["hits"] += 1
    
    def record_cache_miss(self):
        """Record a cache miss."""
        self.metrics.cache_stats["misses"] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics."""
        return self.metrics.get_summary()
    
    def log_performance_summary(self):
        """Log a performance summary."""
        summary = self.get_metrics()
        
        self.logger.info("=== Performance Summary ===")
        
        # Function performance
        if summary["functions"]:
            self.logger.info("Function Performance:")
            for func_name, stats in summary["functions"].items():
                if stats["count"] > 0:
                    self.logger.info(
                        f"  {func_name}: {stats['count']} calls, "
                        f"avg: {stats['avg_time']:.3f}s, "
                        f"total: {stats['total_time']:.3f}s"
                    )
        
        # API calls
        if summary["api_calls"]:
            self.logger.info("API Calls:")
            for endpoint, count in summary["api_calls"].items():
                self.logger.info(f"  {endpoint}: {count} calls")
        
        # Cache performance
        cache_stats = summary["cache_stats"]
        total_cache_requests = cache_stats["hits"] + cache_stats["misses"]
        if total_cache_requests > 0:
            hit_rate = cache_stats["hits"] / total_cache_requests * 100
            self.logger.info(f"Cache Hit Rate: {hit_rate:.1f}% ({cache_stats['hits']}/{total_cache_requests})")
        
        # System metrics
        if summary["system"]:
            system = summary["system"]
            if "memory_mb" in system:
                mem = system["memory_mb"]
                self.logger.info(f"Memory Usage: {mem['current']:.1f}MB (avg: {mem['avg']:.1f}MB)")
            if "cpu_percent" in system:
                cpu = system["cpu_percent"]
                self.logger.info(f"CPU Usage: {cpu['current']:.1f}% (avg: {cpu['avg']:.1f}%)")
        
        # Errors
        if summary["errors"]:
            self.logger.info("Errors:")
            for error_type, count in summary["errors"].items():
                self.logger.info(f"  {error_type}: {count}")


# Global performance monitor instance
_performance_monitor = None


def get_performance_monitor() -> PerformanceMonitor:
    """Get the global performance monitor instance."""
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = PerformanceMonitor()
    return _performance_monitor


def monitor_performance(func: Optional[Callable] = None, *, name: Optional[str] = None):
    """
    Decorator to monitor function performance.
    
    Args:
        func: Function to monitor (when used as @monitor_performance)
        name: Custom name for the function (optional)
    
    Usage:
        @monitor_performance
        def my_function():
            pass
        
        @monitor_performance(name="custom_name")
        def another_function():
            pass
    """
    def decorator(f):
        function_name = name or f.__name__
        
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            monitor = get_performance_monitor()
            start_time = time.time()
            
            try:
                result = f(*args, **kwargs)
                return result
            except Exception as e:
                monitor.record_error(type(e).__name__)
                raise
            finally:
                execution_time = time.time() - start_time
                monitor.record_execution_time(function_name, execution_time)
        
        @functools.wraps(f)
        async def async_wrapper(*args, **kwargs):
            monitor = get_performance_monitor()
            start_time = time.time()
            
            try:
                result = await f(*args, **kwargs)
                return result
            except Exception as e:
                monitor.record_error(type(e).__name__)
                raise
            finally:
                execution_time = time.time() - start_time
                monitor.record_execution_time(function_name, execution_time)
        
        # Return appropriate wrapper based on function type
        if hasattr(f, '__code__') and f.__code__.co_flags & 0x80:  # CO_COROUTINE
            return async_wrapper
        else:
            return wrapper
    
    if func is None:
        # Called with arguments: @monitor_performance(name="custom")
        return decorator
    else:
        # Called without arguments: @monitor_performance
        return decorator(func)


def monitor_api_call(endpoint: str):
    """
    Decorator to monitor API calls.
    
    Usage:
        @monitor_api_call("arxiv_search")
        async def search_arxiv():
            pass
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            monitor = get_performance_monitor()
            monitor.record_api_call(endpoint)
            return func(*args, **kwargs)
        
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            monitor = get_performance_monitor()
            monitor.record_api_call(endpoint)
            return await func(*args, **kwargs)
        
        # Return appropriate wrapper based on function type
        if hasattr(func, '__code__') and func.__code__.co_flags & 0x80:  # CO_COROUTINE
            return async_wrapper
        else:
            return wrapper
    
    return decorator
