"""Logging configuration module."""

import logging
import os
from pathlib import Path


class Logger:
    """Manages application logging."""
    
    _logger = None
    
    @classmethod
    def get_logger(cls, log_dir: str = "logs", log_file: str = "calculator.log") -> logging.Logger:
        """
        Get or create a logger instance.
        
        Args:
            log_dir: Directory for log files
            log_file: Name of the log file
            
        Returns:
            Configured logger instance
        """
        if cls._logger is not None:
            return cls._logger
        
        # Create logs directory if it doesn't exist
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        
        # Create logger
        cls._logger = logging.getLogger('calculator')
        cls._logger.setLevel(logging.DEBUG)
        
        # Avoid adding duplicate handlers
        if cls._logger.handlers:
            return cls._logger
        
        # Create file handler
        file_handler = logging.FileHandler(log_path / log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        cls._logger.addHandler(file_handler)
        cls._logger.addHandler(console_handler)
        
        return cls._logger
