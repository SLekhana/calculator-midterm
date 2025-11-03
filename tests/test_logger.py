"""Tests for logger module."""

import pytest
import logging
from pathlib import Path
import tempfile
from app.logger import Logger


def test_get_logger():
    """Test getting logger instance."""
    logger = Logger.get_logger()
    assert logger is not None
    assert isinstance(logger, logging.Logger)
    assert logger.name == 'calculator'


def test_logger_singleton():
    """Test logger returns same instance."""
    logger1 = Logger.get_logger()
    logger2 = Logger.get_logger()
    assert logger1 is logger2


def test_logger_creates_log_directory():
    """Test logger creates log directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        log_dir = Path(tmpdir) / 'test_logs'
        
        # Properly reset the logger singleton
        Logger._logger = None
        
        # Also need to get a fresh logger instance to clear old handlers
        if logging.getLogger('calculator').handlers:
            logging.getLogger('calculator').handlers.clear()
        
        logger = Logger.get_logger(log_dir=str(log_dir), log_file='test.log')
        
        # Directory should exist
        assert log_dir.exists()
        
        # Logger should have handlers
        assert len(logger.handlers) >= 2
        
        # Should have file and stream handlers
        handler_types = [type(h).__name__ for h in logger.handlers]
        assert 'FileHandler' in handler_types
        assert 'StreamHandler' in handler_types


def test_logger_has_handlers():
    """Test logger has file and console handlers."""
    Logger._logger = None  # Reset singleton
    logger = Logger.get_logger()
    
    assert len(logger.handlers) >= 2
    
    handler_types = [type(h).__name__ for h in logger.handlers]
    assert 'FileHandler' in handler_types
    assert 'StreamHandler' in handler_types


def test_logger_level():
    """Test logger level is set correctly."""
    Logger._logger = None  # Reset singleton
    logger = Logger.get_logger()
    
    assert logger.level == logging.DEBUG
