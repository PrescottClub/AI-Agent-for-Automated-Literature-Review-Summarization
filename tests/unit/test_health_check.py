"""Unit tests for health check system."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import asyncio
from datetime import datetime, timedelta

from src.lit_review_agent.health_check import (
    HealthStatus,
    HealthCheckResult,
    HealthCheck,
    LLMHealthCheck,
    DatabaseHealthCheck,
    APIHealthCheck,
    SystemResourcesHealthCheck,
    HealthCheckManager,
    health_manager,
    setup_health_checks
)


@pytest.mark.unit
class TestHealthStatus:
    """Test HealthStatus enumeration."""

    def test_health_status_values(self):
        """Test health status enumeration values."""
        assert HealthStatus.HEALTHY.value == "healthy"
        assert HealthStatus.DEGRADED.value == "degraded"
        assert HealthStatus.UNHEALTHY.value == "unhealthy"
        assert HealthStatus.UNKNOWN.value == "unknown"


@pytest.mark.unit
class TestHealthCheckResult:
    """Test HealthCheckResult class."""

    def test_basic_creation(self):
        """Test basic health check result creation."""
        result = HealthCheckResult(
            name="test_check",
            status=HealthStatus.HEALTHY,
            message="All good"
        )
        
        assert result.name == "test_check"
        assert result.status == HealthStatus.HEALTHY
        assert result.message == "All good"
        assert isinstance(result.details, dict)
        assert isinstance(result.timestamp, datetime)

    def test_creation_with_details(self):
        """Test health check result creation with details."""
        details = {"cpu": "50%", "memory": "30%"}
        result = HealthCheckResult(
            name="system_check",
            status=HealthStatus.DEGRADED,
            message="System under load",
            details=details,
            response_time_ms=150.5
        )
        
        assert result.details == details
        assert result.response_time_ms == 150.5

    def test_to_dict(self):
        """Test conversion to dictionary."""
        details = {"test": "value"}
        result = HealthCheckResult(
            name="test_check",
            status=HealthStatus.HEALTHY,
            message="OK",
            details=details,
            response_time_ms=100.0
        )
        
        result_dict = result.to_dict()
        
        assert result_dict["name"] == "test_check"
        assert result_dict["status"] == "healthy"
        assert result_dict["message"] == "OK"
        assert result_dict["details"] == details
        assert result_dict["response_time_ms"] == 100.0
        assert "timestamp" in result_dict


@pytest.mark.unit
class TestHealthCheck:
    """Test base HealthCheck class."""

    def test_init(self):
        """Test health check initialization."""
        class TestCheck(HealthCheck):
            async def _perform_check(self):
                return HealthCheckResult("test", HealthStatus.HEALTHY)
        
        check = TestCheck("test_check", timeout=15.0)
        
        assert check.name == "test_check"
        assert check.timeout == 15.0

    @pytest.mark.asyncio
    async def test_check_success(self):
        """Test successful health check."""
        class TestCheck(HealthCheck):
            async def _perform_check(self):
                return HealthCheckResult("test", HealthStatus.HEALTHY, "OK")
        
        check = TestCheck("test_check")
        result = await check.check()
        
        assert result.name == "test"
        assert result.status == HealthStatus.HEALTHY
        assert result.response_time_ms is not None
        assert result.response_time_ms >= 0

    @pytest.mark.asyncio
    async def test_check_timeout(self):
        """Test health check timeout."""
        class SlowCheck(HealthCheck):
            async def _perform_check(self):
                await asyncio.sleep(2)  # Longer than timeout
                return HealthCheckResult("test", HealthStatus.HEALTHY)
        
        check = SlowCheck("slow_check", timeout=0.1)
        result = await check.check()
        
        assert result.name == "slow_check"
        assert result.status == HealthStatus.UNHEALTHY
        assert "timed out" in result.message.lower()

    @pytest.mark.asyncio
    async def test_check_exception(self):
        """Test health check with exception."""
        class FailingCheck(HealthCheck):
            async def _perform_check(self):
                raise ValueError("Test error")
        
        check = FailingCheck("failing_check")
        result = await check.check()
        
        assert result.name == "failing_check"
        assert result.status == HealthStatus.UNHEALTHY
        assert "failed" in result.message.lower()
        assert "Test error" in result.details["error"]


@pytest.mark.unit
class TestLLMHealthCheck:
    """Test LLM health check."""

    @pytest.mark.asyncio
    async def test_llm_health_check_success(self):
        """Test successful LLM health check."""
        # Mock LLM manager
        mock_llm = MagicMock()
        mock_llm.provider = "openai"
        mock_llm.model_name = "gpt-4"
        mock_llm.generate_chat_completion = AsyncMock(return_value={
            "choices": [{"message": {"content": "pong"}}]
        })
        
        check = LLMHealthCheck(mock_llm)
        result = await check._perform_check()
        
        assert result.status == HealthStatus.HEALTHY
        assert "LLM service is responding" in result.message
        assert result.details["provider"] == "openai"
        assert result.details["model"] == "gpt-4"

    @pytest.mark.asyncio
    async def test_llm_health_check_degraded(self):
        """Test degraded LLM health check."""
        mock_llm = MagicMock()
        mock_llm.provider = "openai"
        mock_llm.model_name = "gpt-4"
        mock_llm.generate_chat_completion = AsyncMock(return_value={
            "invalid": "response"
        })
        
        check = LLMHealthCheck(mock_llm)
        result = await check._perform_check()
        
        assert result.status == HealthStatus.DEGRADED
        assert "format unexpected" in result.message

    @pytest.mark.asyncio
    async def test_llm_health_check_failure(self):
        """Test failed LLM health check."""
        mock_llm = MagicMock()
        mock_llm.generate_chat_completion = AsyncMock(
            side_effect=Exception("API error")
        )
        
        check = LLMHealthCheck(mock_llm)
        result = await check._perform_check()
        
        assert result.status == HealthStatus.UNHEALTHY
        assert "LLM service failed" in result.message
        assert "API error" in result.details["error"]


@pytest.mark.unit
class TestDatabaseHealthCheck:
    """Test database health check."""

    @pytest.mark.asyncio
    async def test_database_health_check_success(self):
        """Test successful database health check."""
        mock_db = MagicMock()
        mock_db.get_collection_info.return_value = {
            "count": 100,
            "name": "papers"
        }
        
        check = DatabaseHealthCheck(mock_db)
        result = await check._perform_check()
        
        assert result.status == HealthStatus.HEALTHY
        assert "Vector database is accessible" in result.message
        assert result.details["collection_count"] == 100
        assert result.details["collection_name"] == "papers"

    @pytest.mark.asyncio
    async def test_database_health_check_degraded(self):
        """Test degraded database health check."""
        mock_db = MagicMock()
        mock_db.get_collection_info.return_value = None
        
        check = DatabaseHealthCheck(mock_db)
        result = await check._perform_check()
        
        assert result.status == HealthStatus.DEGRADED
        assert "no collection info" in result.message

    @pytest.mark.asyncio
    async def test_database_health_check_failure(self):
        """Test failed database health check."""
        mock_db = MagicMock()
        mock_db.get_collection_info.side_effect = Exception("Connection error")
        
        check = DatabaseHealthCheck(mock_db)
        result = await check._perform_check()
        
        assert result.status == HealthStatus.UNHEALTHY
        assert "Vector database failed" in result.message


@pytest.mark.unit
class TestAPIHealthCheck:
    """Test API health check."""

    @pytest.mark.asyncio
    async def test_api_health_check_success(self):
        """Test successful API health check."""
        async def mock_test_function():
            return True
        
        check = APIHealthCheck("test_api", mock_test_function)
        result = await check._perform_check()
        
        assert result.status == HealthStatus.HEALTHY
        assert "test_api API is responding" in result.message

    @pytest.mark.asyncio
    async def test_api_health_check_degraded(self):
        """Test degraded API health check."""
        async def mock_test_function():
            return False
        
        check = APIHealthCheck("test_api", mock_test_function)
        result = await check._perform_check()
        
        assert result.status == HealthStatus.DEGRADED
        assert "test failed" in result.message

    @pytest.mark.asyncio
    async def test_api_health_check_failure(self):
        """Test failed API health check."""
        async def mock_test_function():
            raise Exception("API error")
        
        check = APIHealthCheck("test_api", mock_test_function)
        result = await check._perform_check()
        
        assert result.status == HealthStatus.UNHEALTHY
        assert "test_api API failed" in result.message


@pytest.mark.unit
class TestSystemResourcesHealthCheck:
    """Test system resources health check."""

    @pytest.mark.asyncio
    @patch('src.lit_review_agent.health_check.psutil')
    async def test_system_health_check_healthy(self, mock_psutil):
        """Test healthy system resources check."""
        # Mock psutil
        mock_psutil.cpu_percent.return_value = 50.0
        mock_memory = MagicMock()
        mock_memory.percent = 60.0
        mock_memory.available = 8 * (1024**3)  # 8GB
        mock_psutil.virtual_memory.return_value = mock_memory
        
        mock_disk = MagicMock()
        mock_disk.percent = 70.0
        mock_disk.free = 100 * (1024**3)  # 100GB
        mock_psutil.disk_usage.return_value = mock_disk
        
        check = SystemResourcesHealthCheck()
        result = await check._perform_check()
        
        assert result.status == HealthStatus.HEALTHY
        assert "healthy" in result.message.lower()
        assert result.details["cpu_percent"] == 50.0
        assert result.details["memory_percent"] == 60.0

    @pytest.mark.asyncio
    @patch('src.lit_review_agent.health_check.psutil')
    async def test_system_health_check_degraded(self, mock_psutil):
        """Test degraded system resources check."""
        mock_psutil.cpu_percent.return_value = 80.0  # High CPU
        mock_memory = MagicMock()
        mock_memory.percent = 85.0  # High memory
        mock_memory.available = 1 * (1024**3)  # 1GB
        mock_psutil.virtual_memory.return_value = mock_memory
        
        mock_disk = MagicMock()
        mock_disk.percent = 60.0
        mock_disk.free = 50 * (1024**3)  # 50GB
        mock_psutil.disk_usage.return_value = mock_disk
        
        check = SystemResourcesHealthCheck()
        result = await check._perform_check()
        
        assert result.status == HealthStatus.DEGRADED
        assert "under pressure" in result.message.lower()

    @pytest.mark.asyncio
    @patch('src.lit_review_agent.health_check.psutil')
    async def test_system_health_check_unhealthy(self, mock_psutil):
        """Test unhealthy system resources check."""
        mock_psutil.cpu_percent.return_value = 95.0  # Critical CPU
        mock_memory = MagicMock()
        mock_memory.percent = 95.0  # Critical memory
        mock_memory.available = 0.1 * (1024**3)  # 100MB
        mock_psutil.virtual_memory.return_value = mock_memory
        
        mock_disk = MagicMock()
        mock_disk.percent = 98.0  # Critical disk
        mock_disk.free = 1 * (1024**3)  # 1GB
        mock_psutil.disk_usage.return_value = mock_disk
        
        check = SystemResourcesHealthCheck()
        result = await check._perform_check()
        
        assert result.status == HealthStatus.UNHEALTHY
        assert "critically low" in result.message.lower()

    @pytest.mark.asyncio
    async def test_system_health_check_no_psutil(self):
        """Test system health check without psutil."""
        check = SystemResourcesHealthCheck()
        
        with patch.dict('sys.modules', {'psutil': None}):
            result = await check._perform_check()
        
        assert result.status == HealthStatus.UNKNOWN
        assert "psutil not available" in result.message


@pytest.mark.unit
class TestHealthCheckManager:
    """Test HealthCheckManager class."""

    def test_init(self):
        """Test health check manager initialization."""
        manager = HealthCheckManager()
        
        assert isinstance(manager.health_checks, list)
        assert len(manager.health_checks) == 0
        assert manager.last_check_time is None
        assert isinstance(manager.last_results, dict)

    def test_register_health_check(self):
        """Test registering a health check."""
        manager = HealthCheckManager()
        
        class TestCheck(HealthCheck):
            async def _perform_check(self):
                return HealthCheckResult("test", HealthStatus.HEALTHY)
        
        check = TestCheck("test_check")
        manager.register_health_check(check)
        
        assert len(manager.health_checks) == 1
        assert manager.health_checks[0] == check

    @pytest.mark.asyncio
    async def test_run_all_checks_healthy(self):
        """Test running all checks with healthy results."""
        manager = HealthCheckManager()
        
        class HealthyCheck(HealthCheck):
            async def _perform_check(self):
                return HealthCheckResult(self.name, HealthStatus.HEALTHY, "OK")
        
        manager.register_health_check(HealthyCheck("check1"))
        manager.register_health_check(HealthyCheck("check2"))
        
        result = await manager.run_all_checks()
        
        assert result["status"] == "healthy"
        assert result["summary"]["total_checks"] == 2
        assert result["summary"]["healthy_checks"] == 2
        assert "checks" in result
        assert "total_response_time_ms" in result

    @pytest.mark.asyncio
    async def test_run_all_checks_mixed(self):
        """Test running all checks with mixed results."""
        manager = HealthCheckManager()
        
        class HealthyCheck(HealthCheck):
            async def _perform_check(self):
                return HealthCheckResult(self.name, HealthStatus.HEALTHY, "OK")
        
        class DegradedCheck(HealthCheck):
            async def _perform_check(self):
                return HealthCheckResult(self.name, HealthStatus.DEGRADED, "Warning")
        
        manager.register_health_check(HealthyCheck("healthy_check"))
        manager.register_health_check(DegradedCheck("degraded_check"))
        
        result = await manager.run_all_checks()
        
        assert result["status"] == "degraded"
        assert result["summary"]["healthy_checks"] == 1
        assert result["summary"]["degraded_checks"] == 1

    @pytest.mark.asyncio
    async def test_run_all_checks_with_exception(self):
        """Test running checks when one throws an exception."""
        manager = HealthCheckManager()
        
        class FailingCheck(HealthCheck):
            async def check(self):
                raise Exception("Check failed")
        
        class HealthyCheck(HealthCheck):
            async def _perform_check(self):
                return HealthCheckResult(self.name, HealthStatus.HEALTHY, "OK")
        
        manager.register_health_check(FailingCheck("failing_check"))
        manager.register_health_check(HealthyCheck("healthy_check"))
        
        result = await manager.run_all_checks()
        
        assert "failing_check" in result["checks"]
        assert result["checks"]["failing_check"]["status"] == "unhealthy"

    @pytest.mark.asyncio
    async def test_get_health_status_force_refresh(self):
        """Test getting health status with forced refresh."""
        manager = HealthCheckManager()
        
        class TestCheck(HealthCheck):
            async def _perform_check(self):
                return HealthCheckResult(self.name, HealthStatus.HEALTHY, "OK")
        
        manager.register_health_check(TestCheck("test_check"))
        
        result = await manager.get_health_status(force_refresh=True)
        
        assert result["status"] == "healthy"
        assert "cached" not in result
        assert manager.last_check_time is not None

    @pytest.mark.asyncio
    async def test_get_health_status_cached(self):
        """Test getting cached health status."""
        manager = HealthCheckManager()
        manager.last_check_time = datetime.utcnow()
        manager.last_results = {
            "test_check": HealthCheckResult("test_check", HealthStatus.HEALTHY, "OK")
        }
        
        result = await manager.get_health_status()
        
        assert result["status"] == "healthy"
        assert result["cached"] is True


@pytest.mark.unit
class TestSetupHealthChecks:
    """Test health check setup function."""

    @pytest.mark.asyncio
    async def test_setup_health_checks_with_all_components(self):
        """Test setting up health checks with all components."""
        mock_config = MagicMock()
        mock_llm = MagicMock()
        mock_db = MagicMock()
        
        # Clear existing health checks
        global health_manager
        health_manager.health_checks = []
        
        result_manager = await setup_health_checks(
            config=mock_config,
            llm_manager=mock_llm,
            embeddings_manager=mock_db
        )
        
        assert len(result_manager.health_checks) >= 2  # At least system and LLM/DB checks
        
        # Check that different types of health checks are registered
        check_names = [check.name for check in result_manager.health_checks]
        assert "system_resources" in check_names

    @pytest.mark.asyncio
    async def test_setup_health_checks_minimal(self):
        """Test setting up health checks with minimal components."""
        mock_config = MagicMock()
        
        # Clear existing health checks
        global health_manager
        health_manager.health_checks = []
        
        result_manager = await setup_health_checks(config=mock_config)
        
        # Should at least have system resources check
        assert len(result_manager.health_checks) >= 1
        
        check_names = [check.name for check in result_manager.health_checks]
        assert "system_resources" in check_names
``` 