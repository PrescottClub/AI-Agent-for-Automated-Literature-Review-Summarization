# -*- coding: utf-8 -*-
"""
性能监控模块
"""
import time
import psutil
import asyncio
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from fastapi import Request
import logging

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetrics:
    """性能指标数据类"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    disk_usage_percent: float
    request_count: int
    avg_response_time: float
    error_count: int
    active_connections: int


@dataclass
class RequestMetrics:
    """请求指标数据类"""
    path: str
    method: str
    status_code: int
    duration: float
    timestamp: datetime
    client_ip: str
    user_agent: str


class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self, max_metrics_history: int = 1000):
        """
        初始化性能监控器
        
        Args:
            max_metrics_history: 最大指标历史记录数
        """
        self.max_metrics_history = max_metrics_history
        self.metrics_history: List[PerformanceMetrics] = []
        self.request_history: List[RequestMetrics] = []
        self.request_count = 0
        self.error_count = 0
        self.total_response_time = 0.0
        self.active_connections = 0
        self.start_time = datetime.now()
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """获取系统性能指标"""
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # 内存使用情况
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_mb = memory.used / (1024 * 1024)
            
            # 磁盘使用情况
            disk = psutil.disk_usage('/')
            disk_usage_percent = disk.percent
            
            # 计算平均响应时间
            avg_response_time = (
                self.total_response_time / self.request_count 
                if self.request_count > 0 else 0.0
            )
            
            metrics = PerformanceMetrics(
                timestamp=datetime.now(),
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                memory_used_mb=memory_used_mb,
                disk_usage_percent=disk_usage_percent,
                request_count=self.request_count,
                avg_response_time=avg_response_time,
                error_count=self.error_count,
                active_connections=self.active_connections
            )
            
            # 添加到历史记录
            self.metrics_history.append(metrics)
            
            # 保持历史记录在限制范围内
            if len(self.metrics_history) > self.max_metrics_history:
                self.metrics_history.pop(0)
            
            return asdict(metrics)
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            return {}
    
    def record_request(self, request_metrics: RequestMetrics):
        """记录请求指标"""
        self.request_history.append(request_metrics)
        self.request_count += 1
        self.total_response_time += request_metrics.duration
        
        # 记录错误
        if request_metrics.status_code >= 400:
            self.error_count += 1
        
        # 保持请求历史在限制范围内
        if len(self.request_history) > self.max_metrics_history:
            self.request_history.pop(0)
    
    def get_request_stats(self, minutes: int = 60) -> Dict[str, Any]:
        """获取请求统计信息"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        recent_requests = [
            req for req in self.request_history 
            if req.timestamp >= cutoff_time
        ]
        
        if not recent_requests:
            return {
                "total_requests": 0,
                "avg_response_time": 0.0,
                "error_rate": 0.0,
                "requests_per_minute": 0.0,
                "status_codes": {},
                "slowest_endpoints": []
            }
        
        # 计算统计信息
        total_requests = len(recent_requests)
        avg_response_time = sum(req.duration for req in recent_requests) / total_requests
        error_requests = sum(1 for req in recent_requests if req.status_code >= 400)
        error_rate = error_requests / total_requests * 100
        requests_per_minute = total_requests / minutes
        
        # 状态码分布
        status_codes = {}
        for req in recent_requests:
            status_codes[req.status_code] = status_codes.get(req.status_code, 0) + 1
        
        # 最慢的端点
        endpoint_times = {}
        for req in recent_requests:
            key = f"{req.method} {req.path}"
            if key not in endpoint_times:
                endpoint_times[key] = []
            endpoint_times[key].append(req.duration)
        
        slowest_endpoints = []
        for endpoint, times in endpoint_times.items():
            avg_time = sum(times) / len(times)
            slowest_endpoints.append({
                "endpoint": endpoint,
                "avg_response_time": avg_time,
                "request_count": len(times)
            })
        
        slowest_endpoints.sort(key=lambda x: x["avg_response_time"], reverse=True)
        slowest_endpoints = slowest_endpoints[:10]  # 取前10个最慢的
        
        return {
            "total_requests": total_requests,
            "avg_response_time": avg_response_time,
            "error_rate": error_rate,
            "requests_per_minute": requests_per_minute,
            "status_codes": status_codes,
            "slowest_endpoints": slowest_endpoints
        }
    
    def get_health_status(self) -> Dict[str, Any]:
        """获取健康状态"""
        current_metrics = self.get_system_metrics()
        request_stats = self.get_request_stats(minutes=5)  # 最近5分钟
        
        # 判断健康状态
        is_healthy = True
        issues = []
        
        # 检查CPU使用率
        if current_metrics.get("cpu_percent", 0) > 80:
            is_healthy = False
            issues.append("High CPU usage")
        
        # 检查内存使用率
        if current_metrics.get("memory_percent", 0) > 85:
            is_healthy = False
            issues.append("High memory usage")
        
        # 检查磁盘使用率
        if current_metrics.get("disk_usage_percent", 0) > 90:
            is_healthy = False
            issues.append("High disk usage")
        
        # 检查错误率
        if request_stats.get("error_rate", 0) > 10:
            is_healthy = False
            issues.append("High error rate")
        
        # 检查响应时间
        if request_stats.get("avg_response_time", 0) > 5.0:
            is_healthy = False
            issues.append("Slow response time")
        
        uptime = datetime.now() - self.start_time
        
        return {
            "status": "healthy" if is_healthy else "unhealthy",
            "uptime_seconds": uptime.total_seconds(),
            "issues": issues,
            "metrics": current_metrics,
            "request_stats": request_stats
        }
    
    def reset_counters(self):
        """重置计数器"""
        self.request_count = 0
        self.error_count = 0
        self.total_response_time = 0.0
        self.start_time = datetime.now()


class PerformanceMiddleware:
    """性能监控中间件"""
    
    def __init__(self, monitor: PerformanceMonitor):
        """
        初始化性能监控中间件
        
        Args:
            monitor: 性能监控器实例
        """
        self.monitor = monitor
    
    async def __call__(self, request: Request, call_next):
        """中间件处理函数"""
        start_time = time.time()
        self.monitor.active_connections += 1
        
        try:
            response = await call_next(request)
            
            # 记录请求指标
            duration = time.time() - start_time
            client_ip = request.client.host if request.client else "unknown"
            user_agent = request.headers.get("user-agent", "")
            
            request_metrics = RequestMetrics(
                path=request.url.path,
                method=request.method,
                status_code=response.status_code,
                duration=duration,
                timestamp=datetime.now(),
                client_ip=client_ip,
                user_agent=user_agent
            )
            
            self.monitor.record_request(request_metrics)
            
            # 添加性能头
            response.headers["X-Response-Time"] = f"{duration:.3f}s"
            
            return response
            
        except Exception as e:
            # 记录错误请求
            duration = time.time() - start_time
            client_ip = request.client.host if request.client else "unknown"
            user_agent = request.headers.get("user-agent", "")
            
            request_metrics = RequestMetrics(
                path=request.url.path,
                method=request.method,
                status_code=500,
                duration=duration,
                timestamp=datetime.now(),
                client_ip=client_ip,
                user_agent=user_agent
            )
            
            self.monitor.record_request(request_metrics)
            raise
            
        finally:
            self.monitor.active_connections -= 1


# 全局性能监控器实例
performance_monitor = PerformanceMonitor()


def get_performance_monitor() -> PerformanceMonitor:
    """获取性能监控器实例"""
    return performance_monitor
