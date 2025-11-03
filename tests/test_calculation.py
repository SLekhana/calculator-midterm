"""Tests for Calculation class."""

import pytest
from datetime import datetime
from app.calculation import Calculation


def test_calculation_init():
    """Test Calculation initialization."""
    calc = Calculation('add', 5.0, 3.0, 8.0)
    assert calc.operation == 'add'
    assert calc.operand1 == 5.0
    assert calc.operand2 == 3.0
    assert calc.result == 8.0
    assert isinstance(calc.timestamp, datetime)


def test_calculation_repr():
    """Test Calculation repr."""
    calc = Calculation('subtract', 10.0, 4.0, 6.0)
    repr_str = repr(calc)
    assert 'Calculation' in repr_str
    assert 'subtract' in repr_str
    assert '10.0' in repr_str
    assert '4.0' in repr_str
    assert '6.0' in repr_str


def test_calculation_str():
    """Test Calculation string representation."""
    calc = Calculation('multiply', 3.0, 4.0, 12.0)
    assert str(calc) == "3.0 multiply 4.0 = 12.0"


def test_calculation_to_dict():
    """Test Calculation to_dict method."""
    calc = Calculation('divide', 15.0, 3.0, 5.0)
    calc_dict = calc.to_dict()
    
    assert calc_dict['operation'] == 'divide'
    assert calc_dict['operand1'] == 15.0
    assert calc_dict['operand2'] == 3.0
    assert calc_dict['result'] == 5.0
    assert 'timestamp' in calc_dict


def test_calculation_from_dict():
    """Test Calculation from_dict method."""
    data = {
        'operation': 'power',
        'operand1': 2.0,
        'operand2': 3.0,
        'result': 8.0,
        'timestamp': '2025-10-27T10:30:00'
    }
    
    calc = Calculation.from_dict(data)
    assert calc.operation == 'power'
    assert calc.operand1 == 2.0
    assert calc.operand2 == 3.0
    assert calc.result == 8.0


def test_calculation_from_dict_without_timestamp():
    """Test Calculation from_dict without timestamp."""
    data = {
        'operation': 'add',
        'operand1': 1.0,
        'operand2': 2.0,
        'result': 3.0
    }
    
    calc = Calculation.from_dict(data)
    assert calc.operation == 'add'
    assert isinstance(calc.timestamp, datetime)
