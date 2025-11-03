"""Tests for Calculator class."""

import pytest
import tempfile
from pathlib import Path
from app.calculator import Calculator, LoggingObserver, AutoSaveObserver
from app.calculator_config import CalculatorConfig
from app.calculation import Calculation
from app.exceptions import OperationError


@pytest.fixture
def calculator():
    """Create a calculator instance for testing."""
    return Calculator()


def test_calculator_init(calculator):
    """Test calculator initialization."""
    assert calculator is not None
    assert calculator.history is not None
    assert calculator.logger is not None
    assert calculator.config is not None


def test_calculator_add(calculator):
    """Test addition operation."""
    result = calculator.calculate('add', 5, 3)
    assert result == 8


def test_calculator_subtract(calculator):
    """Test subtraction operation."""
    result = calculator.calculate('subtract', 10, 4)
    assert result == 6


def test_calculator_multiply(calculator):
    """Test multiplication operation."""
    result = calculator.calculate('multiply', 6, 7)
    assert result == 42


def test_calculator_divide(calculator):
    """Test division operation."""
    result = calculator.calculate('divide', 15, 3)
    assert result == 5


def test_calculator_divide_by_zero(calculator):
    """Test division by zero raises error."""
    with pytest.raises(OperationError, match="Cannot divide by zero"):
        calculator.calculate('divide', 10, 0)


def test_calculator_power(calculator):
    """Test power operation."""
    result = calculator.calculate('power', 2, 3)
    assert result == 8


def test_calculator_root(calculator):
    """Test root operation."""
    result = calculator.calculate('root', 27, 3)
    assert result == 3


def test_calculator_modulus(calculator):
    """Test modulus operation."""
    result = calculator.calculate('modulus', 10, 3)
    assert result == 1


def test_calculator_int_divide(calculator):
    """Test integer division operation."""
    result = calculator.calculate('int_divide', 10, 3)
    assert result == 3


def test_calculator_percent(calculator):
    """Test percentage operation."""
    result = calculator.calculate('percent', 50, 200)
    assert result == 25


def test_calculator_abs_diff(calculator):
    """Test absolute difference operation."""
    result = calculator.calculate('abs_diff', 10, 3)
    assert result == 7


def test_calculator_unknown_operation(calculator):
    """Test unknown operation raises error."""
    with pytest.raises(OperationError, match="Unknown operation"):
        calculator.calculate('invalid', 5, 3)


def test_calculator_precision(calculator):
    """Test result precision."""
    result = calculator.calculate('divide', 10, 3)
    assert result == 3.33  # Default precision is 2


def test_calculator_history_tracking(calculator):
    """Test calculations are added to history."""
    calculator.calculate('add', 5, 3)
    calculator.calculate('multiply', 4, 5)
    
    history = calculator.get_history()
    assert len(history) == 2
    assert history[0].operation == 'add'
    assert history[1].operation == 'multiply'


def test_calculator_clear_history(calculator):
    """Test clearing history."""
    calculator.calculate('add', 5, 3)
    calculator.calculate('multiply', 4, 5)
    
    calculator.clear_history()
    
    assert len(calculator.get_history()) == 0


def test_calculator_undo(calculator):
    """Test undo functionality."""
    calculator.calculate('add', 5, 3)
    calculator.calculate('multiply', 4, 5)
    
    success = calculator.undo()
    
    assert success is True
    assert len(calculator.get_history()) == 1


def test_calculator_redo(calculator):
    """Test redo functionality."""
    calculator.calculate('add', 5, 3)
    calculator.calculate('multiply', 4, 5)
    
    calculator.undo()
    success = calculator.redo()
    
    assert success is True
    assert len(calculator.get_history()) == 2


def test_calculator_save_history(calculator):
    """Test saving history to file."""
    calculator.calculate('add', 5, 3)
    calculator.calculate('multiply', 4, 5)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        filepath = f.name
    
    try:
        calculator.save_history(filepath)
        assert Path(filepath).exists()
    finally:
        Path(filepath).unlink()


def test_calculator_load_history(calculator):
    """Test loading history from file."""
    calculator.calculate('add', 5, 3)
    calculator.calculate('multiply', 4, 5)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        filepath = f.name
    
    try:
        calculator.save_history(filepath)
        
        # Clear and load
        calculator.clear_history()
        calculator.load_history(filepath)
        
        history = calculator.get_history()
        assert len(history) == 2
    finally:
        Path(filepath).unlink()


def test_calculator_get_available_operations(calculator):
    """Test getting available operations."""
    operations = calculator.get_available_operations()
    assert 'add' in operations
    assert 'subtract' in operations
    assert 'power' in operations
    assert len(operations) == 10


def test_calculator_observer_notification(calculator):
    """Test observers are notified of calculations."""
    notified = []
    
    class TestObserver:
        def update(self, calculation):
            notified.append(calculation)
    
    observer = TestObserver()
    calculator.add_observer(observer)
    
    calculator.calculate('add', 5, 3)
    
    assert len(notified) == 1
    assert notified[0].operation == 'add'


def test_calculator_remove_observer(calculator):
    """Test removing an observer."""
    notified = []
    
    class TestObserver:
        def update(self, calculation):
            notified.append(calculation)
    
    observer = TestObserver()
    calculator.add_observer(observer)
    calculator.calculate('add', 5, 3)
    
    calculator.remove_observer(observer)
    calculator.calculate('multiply', 4, 5)
    
    # Only first calculation should be notified
    assert len(notified) == 1


def test_logging_observer():
    """Test LoggingObserver logs calculations."""
    from app.logger import Logger
    logger = Logger.get_logger()
    
    observer = LoggingObserver(logger)
    calc = Calculation('add', 5, 3, 8)
    
    # Should not raise error
    observer.update(calc)


def test_auto_save_observer():
    """Test AutoSaveObserver saves history."""
    from app.history import CalculationHistory
    
    history = CalculationHistory()
    history.add_calculation(Calculation('add', 5, 3, 8))
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        filepath = f.name
    
    try:
        observer = AutoSaveObserver(history, filepath)
        calc = Calculation('multiply', 4, 5, 20)
        history.add_calculation(calc)
        
        # Trigger auto-save
        observer.update(calc)
        
        assert Path(filepath).exists()
    finally:
        if Path(filepath).exists():
            Path(filepath).unlink()
