"""Tests for custom exceptions."""

import pytest
from app.exceptions import (
    CalculatorError,
    OperationError,
    ValidationError,
    HistoryError,
    ConfigurationError
)


def test_calculator_error():
    """Test CalculatorError base exception."""
    error = CalculatorError("Test error")
    assert str(error) == "Test error"
    assert isinstance(error, Exception)


def test_operation_error():
    """Test OperationError exception."""
    error = OperationError("Operation failed")
    assert str(error) == "Operation failed"
    assert isinstance(error, CalculatorError)


def test_validation_error():
    """Test ValidationError exception."""
    error = ValidationError("Invalid input")
    assert str(error) == "Invalid input"
    assert isinstance(error, CalculatorError)


def test_history_error():
    """Test HistoryError exception."""
    error = HistoryError("History error")
    assert str(error) == "History error"
    assert isinstance(error, CalculatorError)


def test_configuration_error():
    """Test ConfigurationError exception."""
    error = ConfigurationError("Config error")
    assert str(error) == "Config error"
    assert isinstance(error, CalculatorError)
