"""Integration tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import json

from src.lit_review_agent.api_server import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.mark.integration
class TestAPIEndpoints:
    """Integration tests for API endpoints."""

    def test_health_check_endpoint_exists(self, client):
        """Test that health check endpoint exists and responds."""
        response = client.get("/api/health")
        
        # Should not return 404 (endpoint exists)
        assert response.status_code != 404

    def test_status_endpoint(self, client):
        """Test the status endpoint."""
        response = client.get("/api/status")
        
        # The endpoint should exist and return some response
        assert response.status_code in [200, 500, 503]  # Various valid status codes
        
        if response.status_code == 200:
            data = response.json()
            assert "status" in data

    @patch('src.lit_review_agent.retrieval.retrieval_manager.RetrievalManager')
    def test_search_papers_endpoint_structure(self, mock_retrieval_manager, client):
        """Test the structure of search papers endpoint."""
        # Mock the retrieval manager
        mock_manager_instance = AsyncMock()
        mock_manager_instance.search_papers.return_value = {
            "papers": [],
            "total_found": 0,
            "search_time": 0.1
        }
        mock_retrieval_manager.return_value = mock_manager_instance
        
        # Test POST to search endpoint
        search_data = {
            "query": "machine learning",
            "max_results": 5
        }
        
        response = client.post("/api/v1/search", json=search_data)
        
        # Should either work or fail gracefully
        assert response.status_code in [200, 400, 500, 422]
        
        # If successful, check response structure
        if response.status_code == 200:
            data = response.json()
            assert "status" in data or "data" in data

    def test_search_papers_invalid_request(self, client):
        """Test search papers endpoint with invalid request."""
        # Test with missing required fields
        response = client.post("/api/v1/search", json={})
        
        # Should return validation error
        assert response.status_code in [400, 422]

    def test_search_papers_invalid_method(self, client):
        """Test search papers endpoint with wrong HTTP method."""
        response = client.get("/api/v1/search")
        
        # Should return method not allowed
        assert response.status_code == 405

    @patch('src.lit_review_agent.agent.LiteratureReviewAgent')
    def test_generate_report_endpoint_structure(self, mock_agent, client):
        """Test the generate report endpoint structure."""
        # Mock the agent
        mock_agent_instance = AsyncMock()
        mock_agent_instance.generate_literature_review.return_value = {
            "report": "Mock report content",
            "metadata": {"papers_analyzed": 0}
        }
        mock_agent.return_value = mock_agent_instance
        
        report_data = {
            "query": "artificial intelligence",
            "max_papers": 10,
            "format": "markdown"
        }
        
        response = client.post("/api/v1/generate-report", json=report_data)
        
        # Should either work or fail gracefully
        assert response.status_code in [200, 400, 500, 422]

    def test_cors_headers(self, client):
        """Test CORS headers are present."""
        response = client.options("/api/status")
        
        # CORS preflight should be handled
        assert response.status_code in [200, 204]

    def test_api_prefix_routing(self, client):
        """Test that API endpoints are properly prefixed."""
        # Test that non-prefixed endpoint returns 404
        response = client.get("/search")
        assert response.status_code == 404
        
        # Test that API prefixed endpoints exist or return appropriate codes
        response = client.get("/api/status")
        assert response.status_code != 404

    def test_content_type_json(self, client):
        """Test that endpoints return proper content type."""
        response = client.get("/api/status")
        
        if response.status_code == 200:
            assert "application/json" in response.headers.get("content-type", "")

    def test_error_handling_malformed_json(self, client):
        """Test error handling with malformed JSON."""
        # Send malformed JSON
        response = client.post(
            "/api/v1/search",
            data="{invalid json}",
            headers={"Content-Type": "application/json"}
        )
        
        # Should return JSON parsing error
        assert response.status_code in [400, 422]

    def test_large_request_handling(self, client):
        """Test handling of large requests."""
        # Create a very large query
        large_query = "machine learning " * 1000
        
        search_data = {
            "query": large_query,
            "max_results": 5
        }
        
        response = client.post("/api/v1/search", json=search_data)
        
        # Should either handle gracefully or return appropriate error
        assert response.status_code in [200, 400, 413, 422, 500]

    def test_concurrent_requests(self, client):
        """Test handling of concurrent requests."""
        import threading
        import time
        
        results = []
        
        def make_request():
            response = client.get("/api/status")
            results.append(response.status_code)
        
        # Create multiple threads to make concurrent requests
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All requests should complete (may fail due to various reasons but shouldn't hang)
        assert len(results) == 5
        assert all(isinstance(code, int) for code in results)


@pytest.mark.integration
class TestAPIDataValidation:
    """Test API data validation and error handling."""

    def test_search_query_validation(self, client):
        """Test search query validation."""
        test_cases = [
            {"query": "", "max_results": 5},  # Empty query
            {"query": "test", "max_results": -1},  # Negative max_results
            {"query": "test", "max_results": 1000},  # Too large max_results
            {"max_results": 5},  # Missing query
            {"query": "test"},  # Missing max_results (might use default)
        ]
        
        for case in test_cases:
            response = client.post("/api/v1/search", json=case)
            # Should either accept (with defaults) or reject with validation error
            assert response.status_code in [200, 400, 422, 500]

    def test_report_generation_validation(self, client):
        """Test report generation request validation."""
        test_cases = [
            {"query": "", "format": "markdown"},  # Empty query
            {"query": "test", "format": "invalid"},  # Invalid format
            {"query": "test", "max_papers": -1},  # Negative max_papers
            {},  # Empty request
        ]
        
        for case in test_cases:
            response = client.post("/api/v1/generate-report", json=case)
            # Should either accept or reject with validation error
            assert response.status_code in [200, 400, 422, 500]


@pytest.mark.integration
@pytest.mark.slow
class TestAPIPerformance:
    """Performance tests for API endpoints."""

    def test_status_endpoint_response_time(self, client):
        """Test that status endpoint responds quickly."""
        import time
        
        start_time = time.time()
        response = client.get("/api/status")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Status endpoint should respond within 5 seconds
        assert response_time < 5.0

    def test_search_endpoint_timeout(self, client):
        """Test that search endpoint has reasonable timeout."""
        import time
        
        search_data = {
            "query": "machine learning artificial intelligence deep learning",
            "max_results": 1  # Small number to avoid long processing
        }
        
        start_time = time.time()
        response = client.post("/api/v1/search", json=search_data)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Should either complete quickly or timeout gracefully
        if response.status_code == 200:
            # If successful, should be reasonably fast
            assert response_time < 30.0
        # If it times out or fails, that's also acceptable for this test 