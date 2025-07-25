"""Rate limiting middleware for the literature review agent."""

import time
from typing import Dict, Any
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi import Request, HTTPException, status
from collections import defaultdict, deque


# Global rate limiter instance
limiter = Limiter(key_func=get_remote_address)


class RateLimitMiddleware:
    """Custom rate limiting middleware with advanced features."""
    
    def __init__(self, app, calls: int = 60, period: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            app: FastAPI application
            calls: Number of calls allowed per period
            period: Time period in seconds
        """
        self.app = app
        self.calls = calls
        self.period = period
        self.clients = defaultdict(deque)
        
        # Add SlowAPI middleware to app
        app.add_middleware(SlowAPIMiddleware)
        app.state.limiter = limiter
        app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    
    def is_rate_limited(self, client_ip: str) -> bool:
        """Check if client is rate limited."""
        now = time.time()
        client_calls = self.clients[client_ip]
        
        # Remove old calls outside the time window
        while client_calls and client_calls[0] <= now - self.period:
            client_calls.popleft()
        
        # Check if limit exceeded
        if len(client_calls) >= self.calls:
            return True
        
        # Add current call
        client_calls.append(now)
        return False
    
    async def __call__(self, request: Request, call_next):
        """Middleware call method."""
        client_ip = get_remote_address(request)
        
        if self.is_rate_limited(client_ip):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded: {self.calls} requests per {self.period} seconds"
            )
        
        response = await call_next(request)
        return response


# Rate limit decorators for different endpoints
def rate_limit_search(func):
    """Rate limit decorator for search endpoints."""
    return limiter.limit("10/minute")(func)


def rate_limit_api(func):
    """Rate limit decorator for general API endpoints."""
    return limiter.limit("60/minute")(func)


def rate_limit_auth(func):
    """Rate limit decorator for authentication endpoints."""
    return limiter.limit("5/minute")(func)