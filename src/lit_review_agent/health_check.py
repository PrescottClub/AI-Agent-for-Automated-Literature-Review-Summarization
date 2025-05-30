"""Health check system for monitoring application components.

This module provides comprehensive health checking capabilities for all
components of the literature review agent system.
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
import logging

from .exceptions import DatabaseError, APIError, LiteratureReviewError
from .utils.logger import get_logger

logger = get_logger(__name__)


class HealthStatus(Enum):
    """Health status enumeration."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class HealthCheckResult:
    """Result of a health check."""
    
    def __init__(
        self, 
        name: str, 
        status: HealthStatus, 
        message: str = "", 
        details: Dict[str, Any] = None,
        response_time_ms: float = None
    ):
        self.name = name
        self.status = status
        self.message = message
        self.details = details or {}
        self.response_time_ms = response_time_ms
        self.timestamp = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "status": self.status.value,
            "message": self.message,
            "details": self.details,
            "response_time_ms": self.response_time_ms,
            "timestamp": self.timestamp.isoformat()
        }


class HealthCheck:
    """Base class for health checks."""
    
    def __init__(self, name: str, timeout: float = 10.0):
        self.name = name
        self.timeout = timeout
    
    async def check(self) -> HealthCheckResult:
        """Perform the health check."""
        start_time = time.time()
        
        try:
            # Run check with timeout
            result = await asyncio.wait_for(
                self._perform_check(), 
                timeout=self.timeout
            )
            
            response_time = (time.time() - start_time) * 1000
            result.response_time_ms = response_time
            
            return result
            
        except asyncio.TimeoutError:
            response_time = (time.time() - start_time) * 1000
            return HealthCheckResult(
                name=self.name,
                status=HealthStatus.UNHEALTHY,
                message=f"Health check timed out after {self.timeout}s",
                response_time_ms=response_time
            )
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return HealthCheckResult(
                name=self.name,
                status=HealthStatus.UNHEALTHY,
                message=f"Health check failed: {str(e)}",
                details={"error": str(e)},
                response_time_ms=response_time
            )
    
    async def _perform_check(self) -> HealthCheckResult:
        """Override this method to implement specific health check logic."""
        raise NotImplementedError


class LLMHealthCheck(HealthCheck):
    """Health check for LLM services."""
    
    def __init__(self, llm_manager, timeout: float = 15.0):
        super().__init__("llm_service", timeout)
        self.llm_manager = llm_manager
    
    async def _perform_check(self) -> HealthCheckResult:
        try:
            # Test basic LLM functionality
            test_messages = [{"role": "user", "content": "ping"}]
            response = await self.llm_manager.generate_chat_completion(
                messages=test_messages,
                max_tokens=5
            )
            
            if response and "choices" in response:
                return HealthCheckResult(
                    name=self.name,
                    status=HealthStatus.HEALTHY,
                    message="LLM service is responding",
                    details={
                        "provider": self.llm_manager.provider,
                        "model": self.llm_manager.model_name
                    }
                )
            else:
                return HealthCheckResult(
                    name=self.name,
                    status=HealthStatus.DEGRADED,
                    message="LLM service responded but format unexpected",
                    details={"response": str(response)[:200]}
                )
                
        except Exception as e:
            return HealthCheckResult(
                name=self.name,
                status=HealthStatus.UNHEALTHY,
                message="LLM service failed",
                details={"error": str(e)}
            )


class DatabaseHealthCheck(HealthCheck):
    """Health check for vector database."""
    
    def __init__(self, embeddings_manager, timeout: float = 10.0):
        super().__init__("vector_database", timeout)
        self.embeddings_manager = embeddings_manager
    
    async def _perform_check(self) -> HealthCheckResult:
        try:
            # Test database connectivity
            collection_info = self.embeddings_manager.get_collection_info()
            
            if collection_info:
                return HealthCheckResult(
                    name=self.name,
                    status=HealthStatus.HEALTHY,
                    message="Vector database is accessible",
                    details={
                        "collection_count": collection_info.get("count", 0),
                        "collection_name": collection_info.get("name", "unknown")
                    }
                )
            else:
                return HealthCheckResult(
                    name=self.name,
                    status=HealthStatus.DEGRADED,
                    message="Vector database accessible but no collection info"
                )
                
        except Exception as e:
            return HealthCheckResult(
                name=self.name,
                status=HealthStatus.UNHEALTHY,
                message="Vector database failed",
                details={"error": str(e)}
            )


class APIHealthCheck(HealthCheck):
    """Health check for external APIs."""
    
    def __init__(self, api_name: str, test_function: Callable, timeout: float = 10.0):
        super().__init__(f"api_{api_name}", timeout)
        self.api_name = api_name
        self.test_function = test_function
    
    async def _perform_check(self) -> HealthCheckResult:
        try:
            result = await self.test_function()
            
            if result:
                return HealthCheckResult(
                    name=self.name,
                    status=HealthStatus.HEALTHY,
                    message=f"{self.api_name} API is responding"
                )
            else:
                return HealthCheckResult(
                    name=self.name,
                    status=HealthStatus.DEGRADED,
                    message=f"{self.api_name} API responded but test failed"
                )
                
        except Exception as e:
            return HealthCheckResult(
                name=self.name,
                status=HealthStatus.UNHEALTHY,
                message=f"{self.api_name} API failed",
                details={"error": str(e)}
            )


class SystemResourcesHealthCheck(HealthCheck):
    """Health check for system resources."""
    
    def __init__(self, timeout: float = 5.0):
        super().__init__("system_resources", timeout)
    
    async def _perform_check(self) -> HealthCheckResult:
        try:
            import psutil
            
            # Check CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Check memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Check disk usage
            disk = psutil.disk_usage('.')
            disk_percent = disk.percent
            
            details = {
                "cpu_percent": cpu_percent,
                "memory_percent": memory_percent,
                "disk_percent": disk_percent,
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "disk_free_gb": round(disk.free / (1024**3), 2)
            }
            
            # Determine status based on resource usage
            if cpu_percent > 90 or memory_percent > 90 or disk_percent > 95:
                status = HealthStatus.UNHEALTHY
                message = "System resources critically low"
            elif cpu_percent > 70 or memory_percent > 80 or disk_percent > 85:
                status = HealthStatus.DEGRADED
                message = "System resources under pressure"
            else:
                status = HealthStatus.HEALTHY
                message = "System resources are healthy"
            
            return HealthCheckResult(
                name=self.name,
                status=status,
                message=message,
                details=details
            )
            
        except ImportError:
            return HealthCheckResult(
                name=self.name,
                status=HealthStatus.UNKNOWN,
                message="psutil not available for system monitoring"
            )
        except Exception as e:
            return HealthCheckResult(
                name=self.name,
                status=HealthStatus.UNHEALTHY,
                message="Failed to check system resources",
                details={"error": str(e)}
            )


class HealthCheckManager:
    """Manager for coordinating health checks."""
    
    def __init__(self):
        self.health_checks: List[HealthCheck] = []
        self.last_check_time: Optional[datetime] = None
        self.last_results: Dict[str, HealthCheckResult] = {}
    
    def register_health_check(self, health_check: HealthCheck):
        """Register a health check."""
        self.health_checks.append(health_check)
        logger.info(f"Registered health check: {health_check.name}")
    
    async def run_all_checks(self) -> Dict[str, Any]:
        """Run all registered health checks."""
        start_time = time.time()
        results = {}
        
        # Run all checks concurrently
        tasks = [check.check() for check in self.health_checks]
        check_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        overall_status = HealthStatus.HEALTHY
        healthy_count = 0
        total_count = len(self.health_checks)
        
        for i, result in enumerate(check_results):
            if isinstance(result, Exception):
                # Handle exceptions from health checks
                check_name = self.health_checks[i].name
                result = HealthCheckResult(
                    name=check_name,
                    status=HealthStatus.UNHEALTHY,
                    message=f"Health check threw exception: {str(result)}"
                )
            
            results[result.name] = result.to_dict()
            self.last_results[result.name] = result
            
            # Update overall status
            if result.status == HealthStatus.HEALTHY:
                healthy_count += 1
            elif result.status == HealthStatus.UNHEALTHY:
                overall_status = HealthStatus.UNHEALTHY
            elif result.status == HealthStatus.DEGRADED and overall_status == HealthStatus.HEALTHY:
                overall_status = HealthStatus.DEGRADED
        
        # Determine overall status
        if healthy_count == total_count:
            overall_status = HealthStatus.HEALTHY
        elif healthy_count == 0:
            overall_status = HealthStatus.UNHEALTHY
        else:
            overall_status = HealthStatus.DEGRADED
        
        total_time = (time.time() - start_time) * 1000
        self.last_check_time = datetime.utcnow()
        
        return {
            "status": overall_status.value,
            "timestamp": self.last_check_time.isoformat(),
            "total_response_time_ms": round(total_time, 2),
            "checks": results,
            "summary": {
                "total_checks": total_count,
                "healthy_checks": healthy_count,
                "degraded_checks": sum(1 for r in self.last_results.values() 
                                     if r.status == HealthStatus.DEGRADED),
                "unhealthy_checks": sum(1 for r in self.last_results.values() 
                                      if r.status == HealthStatus.UNHEALTHY)
            }
        }
    
    async def get_health_status(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Get current health status, optionally forcing a refresh."""
        if (force_refresh or 
            self.last_check_time is None or 
            datetime.utcnow() - self.last_check_time > timedelta(minutes=5)):
            return await self.run_all_checks()
        
        # Return cached results
        overall_status = HealthStatus.HEALTHY
        for result in self.last_results.values():
            if result.status == HealthStatus.UNHEALTHY:
                overall_status = HealthStatus.UNHEALTHY
                break
            elif result.status == HealthStatus.DEGRADED:
                overall_status = HealthStatus.DEGRADED
        
        return {
            "status": overall_status.value,
            "timestamp": self.last_check_time.isoformat(),
            "checks": {name: result.to_dict() for name, result in self.last_results.items()},
            "cached": True
        }


# Global health check manager instance
health_manager = HealthCheckManager()


async def setup_health_checks(config, llm_manager=None, embeddings_manager=None):
    """Setup all health checks based on configuration."""
    
    # Register LLM health check
    if llm_manager:
        health_manager.register_health_check(
            LLMHealthCheck(llm_manager)
        )
    
    # Register database health check
    if embeddings_manager:
        health_manager.register_health_check(
            DatabaseHealthCheck(embeddings_manager)
        )
    
    # Register system resources check
    health_manager.register_health_check(
        SystemResourcesHealthCheck()
    )
    
    # Register API health checks (examples)
    # These would be implemented based on actual API clients
    
    logger.info(f"Setup {len(health_manager.health_checks)} health checks")
    
    return health_manager 