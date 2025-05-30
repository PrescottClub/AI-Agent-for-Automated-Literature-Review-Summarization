# -*- coding: utf-8 -*-
"""
安全中间件模块
"""
import time
import hashlib
from typing import Dict, Optional
from collections import defaultdict, deque
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """速率限制器"""
    
    def __init__(self, max_requests: int = 100, window: int = 3600):
        """
        初始化速率限制器
        
        Args:
            max_requests: 时间窗口内最大请求数
            window: 时间窗口（秒）
        """
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(deque)
    
    def is_allowed(self, client_ip: str) -> bool:
        """
        检查是否允许请求
        
        Args:
            client_ip: 客户端IP地址
            
        Returns:
            bool: 是否允许请求
        """
        now = time.time()
        client_requests = self.requests[client_ip]
        
        # 清理过期的请求记录
        while client_requests and client_requests[0] < now - self.window:
            client_requests.popleft()
        
        # 检查是否超过限制
        if len(client_requests) >= self.max_requests:
            return False
        
        # 记录新请求
        client_requests.append(now)
        return True


class SecurityMiddleware:
    """安全中间件"""
    
    def __init__(self, max_requests: int = 100, window: int = 3600):
        """
        初始化安全中间件
        
        Args:
            max_requests: 速率限制 - 最大请求数
            window: 速率限制 - 时间窗口
        """
        self.rate_limiter = RateLimiter(max_requests, window)
        self.blocked_ips = set()
        self.suspicious_patterns = [
            "script",
            "javascript:",
            "<script",
            "eval(",
            "document.cookie",
            "alert(",
            "confirm(",
            "prompt(",
        ]
    
    def _get_client_ip(self, request: Request) -> str:
        """获取客户端IP地址"""
        # 检查代理头
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # 回退到直接连接IP
        if request.client:
            return request.client.host
        
        return "unknown"
    
    def _check_suspicious_content(self, content: str) -> bool:
        """检查可疑内容"""
        content_lower = content.lower()
        return any(pattern in content_lower for pattern in self.suspicious_patterns)
    
    async def __call__(self, request: Request, call_next):
        """中间件处理函数"""
        client_ip = self._get_client_ip(request)
        
        # 检查IP是否被阻止
        if client_ip in self.blocked_ips:
            logger.warning(f"Blocked request from IP: {client_ip}")
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "Access denied"}
            )
        
        # 速率限制检查
        if not self.rate_limiter.is_allowed(client_ip):
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": "请求过于频繁，请稍后再试",
                    "retry_after": 60
                }
            )
        
        # 检查请求头
        user_agent = request.headers.get("User-Agent", "")
        if not user_agent or len(user_agent) < 10:
            logger.warning(f"Suspicious request without proper User-Agent from IP: {client_ip}")
        
        # 检查请求体中的可疑内容（仅对POST/PUT请求）
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                if body:
                    body_str = body.decode("utf-8", errors="ignore")
                    if self._check_suspicious_content(body_str):
                        logger.warning(f"Suspicious content detected from IP: {client_ip}")
                        return JSONResponse(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            content={"detail": "Invalid request content"}
                        )
            except Exception as e:
                logger.error(f"Error checking request body: {e}")
        
        # 记录请求信息
        start_time = time.time()
        
        try:
            response = await call_next(request)
            
            # 记录响应时间
            duration = time.time() - start_time
            logger.info(
                f"Request processed",
                extra={
                    "client_ip": client_ip,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration": duration,
                    "user_agent": user_agent[:100]  # 截断长用户代理
                }
            )
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"Request failed: {str(e)}",
                extra={
                    "client_ip": client_ip,
                    "method": request.method,
                    "path": request.url.path,
                    "duration": duration,
                    "error": str(e)
                }
            )
            raise


def create_security_middleware(max_requests: int = 100, window: int = 3600) -> SecurityMiddleware:
    """
    创建安全中间件实例
    
    Args:
        max_requests: 最大请求数
        window: 时间窗口
        
    Returns:
        SecurityMiddleware: 安全中间件实例
    """
    return SecurityMiddleware(max_requests, window)


class InputValidator:
    """输入验证器"""
    
    @staticmethod
    def validate_search_query(query: str) -> str:
        """
        验证搜索查询
        
        Args:
            query: 搜索查询字符串
            
        Returns:
            str: 清理后的查询字符串
            
        Raises:
            HTTPException: 当查询无效时
        """
        if not query or len(query.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="搜索查询不能为空"
            )
        
        if len(query) > 500:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="搜索查询过长（最大500字符）"
            )
        
        # 移除潜在的恶意字符
        import re
        cleaned_query = re.sub(r'[<>"\']', '', query)
        return cleaned_query.strip()
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        验证API密钥格式
        
        Args:
            api_key: API密钥
            
        Returns:
            bool: 是否有效
        """
        if not api_key or len(api_key) < 20:
            return False
        
        # 检查是否只包含允许的字符
        import re
        if not re.match(r'^[a-zA-Z0-9\-_]+$', api_key):
            return False
        
        return True
