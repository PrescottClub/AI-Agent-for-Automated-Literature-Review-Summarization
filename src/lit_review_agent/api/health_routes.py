# -*- coding: utf-8 -*-
"""
健康检查API路由
"""
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from typing import Dict, Any, Optional
import logging

from ..health_check import health_manager
from ..monitoring.performance import get_performance_monitor

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def basic_health_check():
    """基本健康检查端点"""
    try:
        # 获取健康状态
        health_status = await health_manager.get_health_status()
        
        # 简化的响应格式
        return {
            "status": "ok" if health_status["status"] == "healthy" else "degraded",
            "timestamp": datetime.utcnow().isoformat(),
            "agent_status": health_status["status"],
            "version": "2.0.0",
            "services": _extract_service_status(health_status.get("checks", {}))
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Health check failed")


@router.get("/detailed")
async def detailed_health_check(
    force_refresh: bool = Query(False, description="强制刷新健康检查")
):
    """详细健康检查端点"""
    try:
        # 获取详细健康状态
        health_status = await health_manager.get_health_status(force_refresh=force_refresh)
        
        # 获取性能指标
        monitor = get_performance_monitor()
        performance_status = monitor.get_health_status()
        
        return {
            "status": health_status["status"],
            "timestamp": datetime.utcnow().isoformat(),
            "health_checks": health_status,
            "performance_metrics": performance_status["metrics"],
            "request_stats": performance_status["request_stats"],
            "uptime_seconds": performance_status["uptime_seconds"],
            "issues": performance_status["issues"]
        }
        
    except Exception as e:
        logger.error(f"Detailed health check failed: {e}")
        raise HTTPException(status_code=503, detail="Detailed health check failed")


@router.get("/metrics")
async def get_metrics():
    """获取性能指标"""
    try:
        monitor = get_performance_monitor()
        
        # 获取系统指标
        system_metrics = monitor.get_system_metrics()
        
        # 获取请求统计
        request_stats_5min = monitor.get_request_stats(minutes=5)
        request_stats_60min = monitor.get_request_stats(minutes=60)
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "system": system_metrics,
            "requests": {
                "last_5_minutes": request_stats_5min,
                "last_60_minutes": request_stats_60min
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get metrics")


@router.get("/status")
async def get_status():
    """获取简化的状态信息"""
    try:
        monitor = get_performance_monitor()
        health_status = await health_manager.get_health_status()
        
        # 计算整体状态
        overall_healthy = (
            health_status["status"] == "healthy" and
            len(monitor.get_health_status()["issues"]) == 0
        )
        
        return {
            "healthy": overall_healthy,
            "status": health_status["status"],
            "timestamp": datetime.utcnow().isoformat(),
            "version": "2.0.0",
            "uptime_seconds": monitor.get_health_status()["uptime_seconds"]
        }
        
    except Exception as e:
        logger.error(f"Failed to get status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get status")


@router.post("/reset-metrics")
async def reset_metrics():
    """重置性能指标计数器"""
    try:
        monitor = get_performance_monitor()
        monitor.reset_counters()
        
        return {
            "message": "Metrics reset successfully",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to reset metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to reset metrics")


def _extract_service_status(checks: Dict[str, Any]) -> Dict[str, str]:
    """从健康检查结果中提取服务状态"""
    services = {
        "api": "running",
        "agent": "unknown",
        "database": "unknown",
        "llm": "unknown"
    }
    
    for check_name, check_result in checks.items():
        status = check_result.get("status", "unknown")
        
        if "llm" in check_name:
            services["llm"] = "healthy" if status == "healthy" else "unhealthy"
        elif "database" in check_name or "vector" in check_name:
            services["database"] = "connected" if status == "healthy" else "disconnected"
        elif "system" in check_name:
            services["agent"] = "healthy" if status == "healthy" else "degraded"
    
    return services
