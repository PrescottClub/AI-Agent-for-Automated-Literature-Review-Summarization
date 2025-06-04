"""Custom exceptions for the literature review agent.

This module defines a hierarchy of custom exceptions to provide better error
handling and debugging throughout the application.
"""

from typing import Dict, Any, Optional
import traceback
import functools
import time
from datetime import datetime, timezone


class LiteratureReviewError(Exception):
    """Base exception class for all literature review agent errors.

    All custom exceptions in this application should inherit from this class.
    """

    def __init__(
        self,
        message: str,
        error_code: str = None,
        details: Dict[str, Any] = None,
        original_exception: Exception = None,
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        self.original_exception = original_exception
        self.timestamp = datetime.now(timezone.utc).isoformat()

        # Capture stack trace
        self.stack_trace = traceback.format_exc() if original_exception else None

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for JSON serialization."""
        return {
            "error_type": self.__class__.__name__,
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp,
            "stack_trace": self.stack_trace,
        }

    def __str__(self) -> str:
        return f"{self.error_code}: {self.message}"


class ConfigurationError(LiteratureReviewError):
    """Raised when there are configuration-related errors."""

    def __init__(self, message: str, config_key: str = None, **kwargs):
        super().__init__(message, **kwargs)
        if config_key:
            self.details["config_key"] = config_key


class SearchError(LiteratureReviewError):
    """Raised when paper search operations fail."""

    def __init__(self, message: str, query: str = None, source: str = None, **kwargs):
        super().__init__(message, **kwargs)
        if query:
            self.details["query"] = query
        if source:
            self.details["source"] = source


class ProcessingError(LiteratureReviewError):
    """Raised when data processing operations fail."""

    def __init__(
        self,
        message: str,
        processing_stage: str = None,
        input_data: Any = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        if processing_stage:
            self.details["processing_stage"] = processing_stage
        if input_data is not None:
            # Only store safe data (avoid large objects)
            if isinstance(input_data, (str, int, float, bool, list, dict)):
                self.details["input_data"] = str(input_data)[
                    :500
                ]  # Truncate large data


class APIError(LiteratureReviewError):
    """Raised when external API calls fail."""

    def __init__(
        self,
        message: str,
        status_code: int = None,
        response_data: Dict[str, Any] = None,
        api_endpoint: str = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        if status_code:
            self.details["status_code"] = status_code
        if response_data:
            self.details["response_data"] = response_data
        if api_endpoint:
            self.details["api_endpoint"] = api_endpoint


class LLMError(LiteratureReviewError):
    """Raised when LLM operations fail."""

    def __init__(self, message: str, provider: str = None, model: str = None, **kwargs):
        super().__init__(message, **kwargs)
        if provider:
            self.details["provider"] = provider
        if model:
            self.details["model"] = model


class ValidationError(LiteratureReviewError):
    """Raised when input validation fails."""

    def __init__(
        self,
        message: str,
        field_name: str = None,
        field_value: Any = None,
        validation_rule: str = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        if field_name:
            self.details["field_name"] = field_name
        if field_value is not None:
            self.details["field_value"] = str(field_value)[:100]  # Truncate
        if validation_rule:
            self.details["validation_rule"] = validation_rule


class DatabaseError(LiteratureReviewError):
    """Raised when database operations fail."""

    def __init__(
        self, message: str, operation: str = None, collection: str = None, **kwargs
    ):
        super().__init__(message, **kwargs)
        if operation:
            self.details["operation"] = operation
        if collection:
            self.details["collection"] = collection


class FileOperationError(LiteratureReviewError):
    """Raised when file operations fail."""

    def __init__(
        self, message: str, file_path: str = None, operation: str = None, **kwargs
    ):
        super().__init__(message, **kwargs)
        if file_path:
            self.details["file_path"] = file_path
        if operation:
            self.details["operation"] = operation


class RateLimitError(LiteratureReviewError):
    """Raised when rate limits are exceeded."""

    def __init__(
        self, message: str, limit: int = None, reset_time: datetime = None, **kwargs
    ):
        super().__init__(message, **kwargs)
        if limit:
            self.details["limit"] = limit
        if reset_time:
            self.details["reset_time"] = reset_time.isoformat()


class AuthenticationError(LiteratureReviewError):
    """Raised when authentication fails."""

    def __init__(self, message: str, service: str = None, **kwargs):
        super().__init__(message, **kwargs)
        if service:
            self.details["service"] = service


class OperationTimeoutError(LiteratureReviewError):
    """Raised when operations timeout."""

    def __init__(
        self,
        message: str,
        timeout_duration: float = None,
        operation: str = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        if timeout_duration:
            self.details["timeout_duration"] = timeout_duration
        if operation:
            self.details["operation"] = operation


# Exception utilities
class ErrorHandler:
    """Utility class for handling and logging errors."""

    @staticmethod
    def handle_exception(
        exception: Exception, logger=None, reraise: bool = True
    ) -> Optional[LiteratureReviewError]:
        """Handle an exception and optionally convert it to a custom exception.

        Args:
            exception: The original exception
            logger: Logger instance for logging
            reraise: Whether to reraise the exception

        Returns:
            Custom exception if not reraising, None otherwise
        """
        if isinstance(exception, LiteratureReviewError):
            custom_exception = exception
        else:
            # Convert standard exceptions to custom ones
            custom_exception = ErrorHandler._convert_exception(exception)

        if logger:
            logger.error(
                f"Exception handled: {custom_exception}", extra=custom_exception.details
            )

        if reraise:
            raise custom_exception

        return custom_exception

    @staticmethod
    def _convert_exception(exception: Exception) -> LiteratureReviewError:
        """Convert standard exceptions to custom exceptions."""
        error_message = str(exception)

        # Map common exceptions to custom ones
        if isinstance(exception, ValueError):
            return ValidationError(message=error_message, original_exception=exception)
        elif isinstance(exception, FileNotFoundError):
            return FileOperationError(
                message=error_message, operation="read", original_exception=exception
            )
        elif isinstance(exception, PermissionError):
            return FileOperationError(
                message=error_message,
                operation="permission_denied",
                original_exception=exception,
            )
        elif isinstance(exception, ConnectionError):
            return APIError(message=error_message, original_exception=exception)
        elif isinstance(exception, TimeoutError):
            return TimeoutError(message=error_message, original_exception=exception)
        else:
            # Generic wrapper for unknown exceptions
            return LiteratureReviewError(
                message=f"Unexpected error: {error_message}",
                original_exception=exception,
            )


# Enhanced decorator for automatic error handling
def handle_errors(logger=None, reraise=True, default_return=None,
                  record_performance=True):
    """Enhanced decorator for automatic error handling in functions.

    Args:
        logger: Logger instance
        reraise: Whether to reraise exceptions
        default_return: Default value to return on error (if not reraising)
        record_performance: Whether to record performance metrics
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if record_performance:
                from .performance_monitor import get_performance_monitor
                monitor = get_performance_monitor()
                start_time = time.time()

            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                if record_performance:
                    monitor.record_error(type(e).__name__)

                if reraise:
                    ErrorHandler.handle_exception(e, logger, reraise=True)
                else:
                    ErrorHandler.handle_exception(e, logger, reraise=False)
                    return default_return
            finally:
                if record_performance:
                    execution_time = time.time() - start_time
                    monitor.record_execution_time(
                        func.__name__, execution_time)

        return wrapper

    return decorator


# Enhanced async version of the error handling decorator
def handle_errors_async(logger=None, reraise=True, default_return=None,
                        record_performance=True):
    """Enhanced async decorator for automatic error handling."""

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if record_performance:
                from .performance_monitor import get_performance_monitor
                monitor = get_performance_monitor()
                start_time = time.time()

            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                if record_performance:
                    monitor.record_error(type(e).__name__)

                if reraise:
                    ErrorHandler.handle_exception(e, logger, reraise=True)
                else:
                    ErrorHandler.handle_exception(e, logger, reraise=False)
                    return default_return
            finally:
                if record_performance:
                    execution_time = time.time() - start_time
                    monitor.record_execution_time(
                        func.__name__, execution_time)

        return wrapper

    return decorator
