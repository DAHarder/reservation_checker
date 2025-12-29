"""Logging configuration for the application."""

import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logger(name: str = "reservation_checker", level: int = logging.INFO) -> logging.Logger:
    """Set up logger with console and file output.
    
    Args:
        name: The logger name
        level: The logging level
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler - only show errors
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    
    # File handler - create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    log_filename = logs_dir / f"reservation_checker_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger
