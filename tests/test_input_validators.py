"""Tests for input validators."""

import pytest
from app.input_validators import InputValidator
from app.exceptions import ValidationError


def test_validate_number_valid():
    """Test validating valid numbers."""
    assert InputValidator.validate_number("42") == 42.0
    assert InputValidator.validate_number("3.14") == 3.14
    assert InputValidator.validate_number("-10") == -10.0


def test_validate_number_invalid():
    """Test validating invalid numbers."""
    with pytest.raises(ValidationError, match="Invalid number"):
        InputValidator.validate_number("abc")
    
    with pytest.raises(ValidationError, match="Invalid number"):
        InputValidator.validate_number("12.34.56")


def test_validate_number_with_max_value():
    """Test validation with max value constraint."""
    assert InputValidator.validate_number("100", max_value=1000) == 100.0
    
    with pytest.raises(ValidationError, match="exceeds maximum"):
        InputValidator.validate_number("2000", max_value=1000)


def test_validate_number_negative_with_max():
    """Test negative numbers with max value."""
    assert InputValidator.validate_number("-100", max_value=1000) == -100.0
    
    with pytest.raises(ValidationError, match="exceeds maximum"):
        InputValidator.validate_number("-2000", max_value=1000)


def test_validate_operands_valid():
    """Test validating valid operands."""
    a, b = InputValidator.validate_operands("10", "5")
    assert a == 10.0
    assert b == 5.0


def test_validate_operands_with_max():
    """Test validating operands with max value."""
    a, b = InputValidator.validate_operands("100", "200", max_value=1000)
    assert a == 100.0
    assert b == 200.0


def test_validate_operands_first_invalid():
    """Test validation fails on first invalid operand."""
    with pytest.raises(ValidationError):
        InputValidator.validate_operands("abc", "5")


def test_validate_operands_second_invalid():
    """Test validation fails on second invalid operand."""
    with pytest.raises(ValidationError):
        InputValidator.validate_operands("10", "xyz")


def test_validate_operands_exceeds_max():
    """Test validation fails when operand exceeds max."""
    with pytest.raises(ValidationError):
        InputValidator.validate_operands("10", "2000", max_value=1000)
