"""Logging configuration and utilities for the literature review agent."""

import sys
from pathlib import Path
from typing import Optional

from loguru import logger

# Import Rich handler if available
try:
    from .display import get_rich_handler

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


def setup_logger(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    rotation: str = "10 MB",
    retention: str = "1 week",
    use_rich: bool = True,
) -> logger:
    """
    Setup and configure the logger for the application.

    Args:
        log_level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to the log file. If None, only console logging is used.
        rotation: Log file rotation settings
        retention: Log file retention settings
        use_rich: Whether to use Rich formatting for console output

    Returns:
        Configured logger instance
    """
    # Remove default logger
    logger.remove()

    # Configure console logging
    if use_rich and RICH_AVAILABLE:
        # Use Rich handler for enhanced console output
        import logging

        # Create a standard logging logger to bridge with Rich
        logging_logger = logging.getLogger("lit_review_agent")
        logging_logger.setLevel(getattr(logging, log_level.upper()))

        # Add Rich handler to standard logger
        rich_handler = get_rich_handler()
        rich_handler.setLevel(getattr(logging, log_level.upper()))
        logging_logger.addHandler(rich_handler)

        # Configure loguru to forward to standard logging
        logger.add(
            lambda message: logging_logger.info(message.rstrip("\n")),
            level=log_level,
            format="{message}",
            colorize=False,
        )
    else:
        # Fallback to standard loguru console formatting
        logger.add(
            sys.stderr,
            level=log_level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>",
            colorize=True,
        )

    # Add file logging if specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        logger.add(
            log_path,
            level=log_level,
            format="{time:YYYY-MM-DD HH:mm:ss} | "
            "{level: <8} | "
            "{name}:{function}:{line} - "
            "{message}",
            rotation=rotation,
            retention=retention,
            compression="zip",
            enqueue=True,  # Enable async logging for better performance
        )

    return logger


def get_logger(name: str) -> logger:
    """
    Get a logger instance with the specified name.

    Args:
        name: The name for the logger (usually __name__)

    Returns:
        Logger instance
    """
    return logger.bind(name=name)


class LoggerMixin:
    """Mixin class to add logging capabilities to any class."""

    @property
    def logger(self) -> logger:
        """Get a logger instance for this class."""
        return get_logger(f"{self.__class__.__module__}.{self.__class__.__name__}")


# Utility functions for common logging patterns
def log_function_entry(func_name: str, **kwargs) -> None:
    """Log function entry with parameters."""
    params = ", ".join(f"{k}={v}" for k, v in kwargs.items())
    logger.debug(f"Entering {func_name}({params})")


def log_function_exit(func_name: str, result=None) -> None:
    """Log function exit with optional result."""
    if result is not None:
        logger.debug(f"Exiting {func_name} with result: {result}")
    else:
        logger.debug(f"Exiting {func_name}")


def log_api_call(api_name: str, endpoint: str, **kwargs) -> None:
    """Log API call details."""
    params = ", ".join(f"{k}={v}" for k, v in kwargs.items())
    logger.info(f"API Call: {api_name} -> {endpoint} ({params})")


def log_error_with_context(error: Exception, context: str = "") -> None:
    """Log error with additional context."""
    error_msg = f"Error: {str(error)}"
    if context:
        error_msg = f"{context}: {error_msg}"

    logger.error(error_msg)
    logger.debug(f"Error details: {type(error).__name__}: {error}")


def log_performance(operation: str, duration: float, **metrics) -> None:
    """Log performance metrics."""
    metric_str = ", ".join(f"{k}={v}" for k, v in metrics.items())
    logger.info(f"Performance: {operation} took {duration:.2f}s ({metric_str})")
