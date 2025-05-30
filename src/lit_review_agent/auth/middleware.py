"""FastAPI middleware for authentication and rate limiting."""

import time
from typing import Callable, Optional, List
from fastapi import Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from .auth_manager import get_auth_manager, User, APIKey
from .rate_limiter import get_rate_limiter, RateLimitResult
from ..utils.logger import get_logger

logger = get_logger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    """Authentication middleware for FastAPI."""

    def __init__(
        self, 
        app, 
        exempt_paths: List[str] = None,
        require_auth: bool = True
    ):
        super().__init__(app)
        self.exempt_paths = exempt_paths or ["/health", "/docs", "/openapi.json", "/redoc"]
        self.require_auth = require_auth
        self.auth_manager = get_auth_manager()

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process authentication for incoming requests."""
        # Skip authentication for exempt paths
        if request.url.path in self.exempt_paths:
            return await call_next(request)

        # Skip if authentication is not required
        if not self.require_auth:
            return await call_next(request)

        try:
            # Extract authentication credentials
            auth_result = await self._authenticate_request(request)
            
            if not auth_result:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "detail": "Authentication required",
                        "error": "missing_credentials"
                    },
                    headers={"WWW-Authenticate": "Bearer"}
                )

            user, api_key = auth_result

            # Add user and API key info to request state
            request.state.user = user
            request.state.api_key = api_key
            request.state.authenticated = True

            # Log successful authentication
            logger.debug(f"User {user.username} authenticated for {request.url.path}")

            # Proceed with request
            response = await call_next(request)
            
            # Add authentication headers
            response.headers["X-User-ID"] = user.user_id
            response.headers["X-Auth-Method"] = "api_key" if api_key else "session"

            return response

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Authentication service error",
                    "error": "auth_service_error"
                }
            )

    async def _authenticate_request(self, request: Request) -> Optional[tuple]:
        """Authenticate request and return (user, api_key) or None."""
        # Try API key authentication first
        api_key = self._extract_api_key(request)
        if api_key:
            key_obj = await self.auth_manager.validate_api_key(api_key)
            if key_obj:
                # Get user from API key
                for provider in self.auth_manager.providers:
                    if hasattr(provider, 'users') and key_obj.user_id in provider.users:
                        user = provider.users[key_obj.user_id]
                        return user, key_obj

        # Try session authentication
        session_id = self._extract_session_id(request)
        if session_id:
            user = self.auth_manager.get_session_user(session_id)
            if user:
                return user, None

        # Try Bearer token authentication
        token = self._extract_bearer_token(request)
        if token:
            user = await self.auth_manager.authenticate({"token": token})
            if user:
                return user, None

        return None

    def _extract_api_key(self, request: Request) -> Optional[str]:
        """Extract API key from request."""
        # Check X-API-Key header
        api_key = request.headers.get("X-API-Key")
        if api_key:
            return api_key

        # Check query parameter
        api_key = request.query_params.get("api_key")
        if api_key:
            return api_key

        return None

    def _extract_session_id(self, request: Request) -> Optional[str]:
        """Extract session ID from cookies."""
        return request.cookies.get("session_id")

    def _extract_bearer_token(self, request: Request) -> Optional[str]:
        """Extract Bearer token from Authorization header."""
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header[7:]  # Remove "Bearer " prefix
        return None


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware for FastAPI."""

    def __init__(
        self, 
        app, 
        exempt_paths: List[str] = None,
        enable_rate_limiting: bool = True
    ):
        super().__init__(app)
        self.exempt_paths = exempt_paths or ["/health", "/docs", "/openapi.json", "/redoc"]
        self.enable_rate_limiting = enable_rate_limiting
        self.rate_limiter = get_rate_limiter()

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process rate limiting for incoming requests."""
        # Skip rate limiting for exempt paths
        if request.url.path in self.exempt_paths:
            return await call_next(request)

        # Skip if rate limiting is disabled
        if not self.enable_rate_limiting:
            return await call_next(request)

        try:
            # Determine rate limit identifier
            identifier = self._get_rate_limit_identifier(request)
            
            # Check rate limit
            result = await self.rate_limiter.check_rate_limit(identifier)
            
            if not result.allowed:
                # Rate limit exceeded
                headers = {
                    "X-RateLimit-Limit": str(self._get_limit_for_identifier(identifier)),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(result.reset_time)),
                    "Retry-After": str(result.retry_after or 60)
                }
                
                logger.warning(f"Rate limit exceeded for {identifier} on {request.url.path}")
                
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "detail": "Rate limit exceeded",
                        "error": "rate_limit_exceeded",
                        "retry_after": result.retry_after
                    },
                    headers=headers
                )

            # Proceed with request
            response = await call_next(request)
            
            # Add rate limit headers to response
            limit = self._get_limit_for_identifier(identifier)
            response.headers["X-RateLimit-Limit"] = str(limit)
            response.headers["X-RateLimit-Remaining"] = str(result.remaining)
            response.headers["X-RateLimit-Reset"] = str(int(result.reset_time))

            return response

        except Exception as e:
            logger.error(f"Rate limiting error: {e}")
            # Continue without rate limiting on error
            return await call_next(request)

    def _get_rate_limit_identifier(self, request: Request) -> str:
        """Get rate limit identifier for request."""
        # Use user ID if authenticated
        if hasattr(request.state, 'user') and request.state.user:
            user = request.state.user
            
            # Admin users get higher limits
            if "admin" in user.roles:
                return f"admin:{user.user_id}"
            else:
                return f"user:{user.user_id}"

        # Use API key if available
        if hasattr(request.state, 'api_key') and request.state.api_key:
            return f"apikey:{request.state.api_key.key_id}"

        # Fall back to IP address for unauthenticated requests
        client_ip = self._get_client_ip(request)
        return f"ip:{client_ip}"

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address from request."""
        # Check X-Forwarded-For header (for reverse proxy setups)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        # Check X-Real-IP header
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # Fall back to direct client IP
        return request.client.host if request.client else "unknown"

    def _get_limit_for_identifier(self, identifier: str) -> int:
        """Get rate limit for identifier."""
        # Extract the type from identifier
        if identifier.startswith("admin:"):
            return 1000  # Admin limit
        elif identifier.startswith("user:"):
            return 100   # User limit
        elif identifier.startswith("apikey:"):
            return 100   # API key limit
        elif identifier.startswith("ip:"):
            return 10    # IP-based limit for unauthenticated users
        else:
            return 60    # Default limit


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to responses."""

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Add security headers to response."""
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'"
        )
        
        # Remove server header for security
        if "server" in response.headers:
            del response.headers["server"]

        return response


class CORSMiddleware(BaseHTTPMiddleware):
    """Custom CORS middleware."""

    def __init__(
        self, 
        app, 
        allow_origins: List[str] = None,
        allow_credentials: bool = True,
        allow_methods: List[str] = None,
        allow_headers: List[str] = None
    ):
        super().__init__(app)
        self.allow_origins = allow_origins or ["http://localhost:3000", "http://localhost:5174"]
        self.allow_credentials = allow_credentials
        self.allow_methods = allow_methods or ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        self.allow_headers = allow_headers or [
            "Authorization", 
            "Content-Type", 
            "X-API-Key",
            "X-Requested-With"
        ]

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Handle CORS for requests."""
        origin = request.headers.get("origin")
        
        # Handle preflight requests
        if request.method == "OPTIONS":
            response = Response()
        else:
            response = await call_next(request)

        # Add CORS headers
        if origin and (origin in self.allow_origins or "*" in self.allow_origins):
            response.headers["Access-Control-Allow-Origin"] = origin
            
        if self.allow_credentials:
            response.headers["Access-Control-Allow-Credentials"] = "true"
            
        response.headers["Access-Control-Allow-Methods"] = ", ".join(self.allow_methods)
        response.headers["Access-Control-Allow-Headers"] = ", ".join(self.allow_headers)
        response.headers["Access-Control-Max-Age"] = "86400"  # 24 hours

        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log request and response information."""

    def __init__(self, app, log_requests: bool = True, log_responses: bool = False):
        super().__init__(app)
        self.log_requests = log_requests
        self.log_responses = log_responses

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Log request and response."""
        start_time = time.time()
        
        # Log request
        if self.log_requests:
            user_id = getattr(request.state, 'user', {})
            user_id = user_id.user_id if hasattr(user_id, 'user_id') else 'anonymous'
            
            logger.info(
                f"Request: {request.method} {request.url.path} "
                f"from {self._get_client_ip(request)} "
                f"user={user_id}"
            )

        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        if self.log_responses:
            logger.info(
                f"Response: {response.status_code} "
                f"for {request.method} {request.url.path} "
                f"in {process_time:.3f}s"
            )

        # Add timing header
        response.headers["X-Process-Time"] = str(process_time)

        return response

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address."""
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.client.host if request.client else "unknown" 