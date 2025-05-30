"""Rate limiting implementation for API protection."""

import asyncio
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, Any
from enum import Enum

from ..utils.logger import get_logger

logger = get_logger(__name__)


class RateLimitStrategy(Enum):
    """Rate limiting strategies."""
    FIXED_WINDOW = "fixed_window"
    SLIDING_WINDOW = "sliding_window" 
    TOKEN_BUCKET = "token_bucket"
    LEAKY_BUCKET = "leaky_bucket"


@dataclass
class RateLimit:
    """Rate limit configuration."""
    requests: int  # Number of requests allowed
    window: int    # Time window in seconds
    strategy: RateLimitStrategy = RateLimitStrategy.SLIDING_WINDOW
    burst: int = None  # Burst capacity for token bucket


@dataclass
class RateLimitResult:
    """Rate limit check result."""
    allowed: bool
    remaining: int
    reset_time: float
    retry_after: Optional[int] = None


class RateLimiter:
    """Advanced rate limiter with multiple strategies."""

    def __init__(self):
        self.limits: Dict[str, RateLimit] = {}
        self.counters: Dict[str, Dict] = defaultdict(dict)
        self.cleanup_interval = 300  # 5 minutes
        self.last_cleanup = time.time()

    def set_limit(self, key: str, rate_limit: RateLimit):
        """Set rate limit for a key pattern."""
        self.limits[key] = rate_limit
        logger.info(f"Rate limit set for {key}: {rate_limit.requests}/{rate_limit.window}s")

    def _get_rate_limit(self, identifier: str) -> Optional[RateLimit]:
        """Get rate limit for identifier."""
        # Check for exact match first
        if identifier in self.limits:
            return self.limits[identifier]
        
        # Check for pattern matches (simple prefix matching)
        for pattern, limit in self.limits.items():
            if pattern.endswith("*") and identifier.startswith(pattern[:-1]):
                return limit
        
        # Default limit if none specified
        return self.limits.get("default")

    async def check_rate_limit(self, identifier: str, cost: int = 1) -> RateLimitResult:
        """Check if request is within rate limit."""
        rate_limit = self._get_rate_limit(identifier)
        if not rate_limit:
            # No limit configured - allow request
            return RateLimitResult(
                allowed=True,
                remaining=float('inf'),
                reset_time=time.time()
            )

        # Cleanup old entries periodically
        await self._cleanup_if_needed()

        # Apply rate limiting strategy
        if rate_limit.strategy == RateLimitStrategy.SLIDING_WINDOW:
            return await self._sliding_window_check(identifier, rate_limit, cost)
        elif rate_limit.strategy == RateLimitStrategy.FIXED_WINDOW:
            return await self._fixed_window_check(identifier, rate_limit, cost)
        elif rate_limit.strategy == RateLimitStrategy.TOKEN_BUCKET:
            return await self._token_bucket_check(identifier, rate_limit, cost)
        elif rate_limit.strategy == RateLimitStrategy.LEAKY_BUCKET:
            return await self._leaky_bucket_check(identifier, rate_limit, cost)
        else:
            # Default to sliding window
            return await self._sliding_window_check(identifier, rate_limit, cost)

    async def _sliding_window_check(self, identifier: str, rate_limit: RateLimit, cost: int) -> RateLimitResult:
        """Sliding window rate limiting."""
        current_time = time.time()
        window_start = current_time - rate_limit.window

        # Initialize if not exists
        if identifier not in self.counters:
            self.counters[identifier] = {"requests": deque(), "total": 0}

        counter = self.counters[identifier]
        requests = counter["requests"]

        # Remove old requests outside the window
        while requests and requests[0] <= window_start:
            requests.popleft()

        current_count = len(requests)
        
        if current_count + cost <= rate_limit.requests:
            # Add new requests
            for _ in range(cost):
                requests.append(current_time)
            
            remaining = rate_limit.requests - current_count - cost
            reset_time = current_time + rate_limit.window
            
            return RateLimitResult(
                allowed=True,
                remaining=remaining,
                reset_time=reset_time
            )
        else:
            # Rate limit exceeded
            oldest_request = requests[0] if requests else current_time
            reset_time = oldest_request + rate_limit.window
            retry_after = int(reset_time - current_time)
            
            return RateLimitResult(
                allowed=False,
                remaining=0,
                reset_time=reset_time,
                retry_after=max(1, retry_after)
            )

    async def _fixed_window_check(self, identifier: str, rate_limit: RateLimit, cost: int) -> RateLimitResult:
        """Fixed window rate limiting."""
        current_time = time.time()
        window_start = int(current_time // rate_limit.window) * rate_limit.window

        # Initialize if not exists
        if identifier not in self.counters:
            self.counters[identifier] = {"window_start": window_start, "count": 0}

        counter = self.counters[identifier]

        # Reset counter if new window
        if counter["window_start"] != window_start:
            counter["window_start"] = window_start
            counter["count"] = 0

        if counter["count"] + cost <= rate_limit.requests:
            counter["count"] += cost
            remaining = rate_limit.requests - counter["count"]
            reset_time = window_start + rate_limit.window
            
            return RateLimitResult(
                allowed=True,
                remaining=remaining,
                reset_time=reset_time
            )
        else:
            reset_time = window_start + rate_limit.window
            retry_after = int(reset_time - current_time)
            
            return RateLimitResult(
                allowed=False,
                remaining=0,
                reset_time=reset_time,
                retry_after=max(1, retry_after)
            )

    async def _token_bucket_check(self, identifier: str, rate_limit: RateLimit, cost: int) -> RateLimitResult:
        """Token bucket rate limiting."""
        current_time = time.time()
        bucket_size = rate_limit.burst or rate_limit.requests
        refill_rate = rate_limit.requests / rate_limit.window  # tokens per second

        # Initialize if not exists
        if identifier not in self.counters:
            self.counters[identifier] = {
                "tokens": bucket_size,
                "last_refill": current_time
            }

        counter = self.counters[identifier]

        # Refill tokens
        time_passed = current_time - counter["last_refill"]
        tokens_to_add = time_passed * refill_rate
        counter["tokens"] = min(bucket_size, counter["tokens"] + tokens_to_add)
        counter["last_refill"] = current_time

        if counter["tokens"] >= cost:
            counter["tokens"] -= cost
            remaining = int(counter["tokens"])
            
            # Calculate when bucket will be full again
            if counter["tokens"] < bucket_size:
                time_to_full = (bucket_size - counter["tokens"]) / refill_rate
                reset_time = current_time + time_to_full
            else:
                reset_time = current_time
            
            return RateLimitResult(
                allowed=True,
                remaining=remaining,
                reset_time=reset_time
            )
        else:
            # Calculate retry after time
            tokens_needed = cost - counter["tokens"]
            retry_after = int(tokens_needed / refill_rate) + 1
            
            return RateLimitResult(
                allowed=False,
                remaining=0,
                reset_time=current_time + retry_after,
                retry_after=retry_after
            )

    async def _leaky_bucket_check(self, identifier: str, rate_limit: RateLimit, cost: int) -> RateLimitResult:
        """Leaky bucket rate limiting."""
        current_time = time.time()
        bucket_size = rate_limit.burst or rate_limit.requests
        leak_rate = rate_limit.requests / rate_limit.window  # requests per second

        # Initialize if not exists
        if identifier not in self.counters:
            self.counters[identifier] = {
                "level": 0,
                "last_leak": current_time
            }

        counter = self.counters[identifier]

        # Leak from bucket
        time_passed = current_time - counter["last_leak"]
        leaked = time_passed * leak_rate
        counter["level"] = max(0, counter["level"] - leaked)
        counter["last_leak"] = current_time

        if counter["level"] + cost <= bucket_size:
            counter["level"] += cost
            remaining = int(bucket_size - counter["level"])
            
            # Calculate reset time based on current level
            if counter["level"] > 0:
                time_to_empty = counter["level"] / leak_rate
                reset_time = current_time + time_to_empty
            else:
                reset_time = current_time
            
            return RateLimitResult(
                allowed=True,
                remaining=remaining,
                reset_time=reset_time
            )
        else:
            # Calculate retry after time
            overflow = (counter["level"] + cost) - bucket_size
            retry_after = int(overflow / leak_rate) + 1
            
            return RateLimitResult(
                allowed=False,
                remaining=0,
                reset_time=current_time + retry_after,
                retry_after=retry_after
            )

    async def _cleanup_if_needed(self):
        """Clean up old rate limit data."""
        current_time = time.time()
        if current_time - self.last_cleanup < self.cleanup_interval:
            return

        logger.debug("Starting rate limiter cleanup")
        
        # Clean up sliding window data
        for identifier, counter in list(self.counters.items()):
            if "requests" in counter:
                # Sliding window cleanup
                window_start = current_time - 3600  # Keep last hour
                requests = counter["requests"]
                while requests and requests[0] <= window_start:
                    requests.popleft()
                
                # Remove if empty
                if not requests:
                    del self.counters[identifier]
            
            elif "last_refill" in counter:
                # Token bucket cleanup - remove if not used for 1 hour
                if current_time - counter["last_refill"] > 3600:
                    del self.counters[identifier]
            
            elif "last_leak" in counter:
                # Leaky bucket cleanup - remove if not used for 1 hour
                if current_time - counter["last_leak"] > 3600:
                    del self.counters[identifier]

        self.last_cleanup = current_time
        logger.debug(f"Rate limiter cleanup completed. Active counters: {len(self.counters)}")

    def get_stats(self) -> Dict[str, Any]:
        """Get rate limiter statistics."""
        return {
            "active_limits": len(self.limits),
            "active_counters": len(self.counters),
            "limits": {
                key: {
                    "requests": limit.requests,
                    "window": limit.window,
                    "strategy": limit.strategy.value
                }
                for key, limit in self.limits.items()
            },
            "last_cleanup": datetime.fromtimestamp(self.last_cleanup).isoformat()
        }

    async def reset_limit(self, identifier: str):
        """Reset rate limit for an identifier."""
        if identifier in self.counters:
            del self.counters[identifier]
            logger.info(f"Rate limit reset for {identifier}")

    def set_default_limits(self):
        """Set default rate limits."""
        default_limits = {
            "default": RateLimit(100, 60),  # 100 requests per minute
            "search": RateLimit(20, 60),    # 20 searches per minute
            "admin": RateLimit(1000, 60),   # 1000 requests per minute for admin
            "guest": RateLimit(10, 60),     # 10 requests per minute for guests
        }
        
        for key, limit in default_limits.items():
            self.set_limit(key, limit)

        logger.info("Default rate limits configured")


# Global rate limiter instance
rate_limiter: Optional[RateLimiter] = None


def get_rate_limiter() -> RateLimiter:
    """Get the global rate limiter instance."""
    global rate_limiter
    if rate_limiter is None:
        rate_limiter = RateLimiter()
        rate_limiter.set_default_limits()
    return rate_limiter


def initialize_rate_limiter() -> RateLimiter:
    """Initialize the global rate limiter."""
    global rate_limiter
    rate_limiter = RateLimiter()
    rate_limiter.set_default_limits()
    return rate_limiter 