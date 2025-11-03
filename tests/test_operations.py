"""Tests for operations and factory."""

import pytest
from app.operations import (
    AddOperation, SubtractOperation, MultiplyOperation, DivideOperation,
    PowerOperation, RootOperation, ModulusOperation, IntDivideOperation,
    PercentageOperation, AbsDifferenceOperation, OperationFactory
)
from app.exceptions import OperationError


# Test basic operations
def test_add_operation():
    """Test addition operation."""
    op = AddOperation()
    assert op.execute(5, 3) == 8
    assert op.get_symbol() == "+"


def test_subtract_operation():
    """Test subtraction operation."""
    op = SubtractOperation()
    assert op.execute(10, 4) == 6
    assert op.get_symbol() == "-"


def test_multiply_operation():
    """Test multiplication operation."""
    op = MultiplyOperation()
    assert op.execute(6, 7) == 42
    assert op.get_symbol() == "*"


def test_divide_operation():
    """Test division operation."""
    op = DivideOperation()
    assert op.execute(15, 3) == 5
    assert op.get_symbol() == "/"


def test_divide_by_zero():
    """Test division by zero raises error."""
    op = DivideOperation()
    with pytest.raises(OperationError, match="Cannot divide by zero"):
        op.execute(10, 0)


# Test advanced operations
def test_power_operation():
    """Test power operation."""
    op = PowerOperation()
    assert op.execute(2, 3) == 8
    assert op.execute(5, 2) == 25
    assert op.get_symbol() == "^"


def test_power_operation_negative_exponent():
    """Test power with negative exponent."""
    op = PowerOperation()
    assert op.execute(2, -1) == 0.5


def test_root_operation():
    """Test root operation."""
    op = RootOperation()
    assert op.execute(27, 3) == 3
    assert op.execute(16, 2) == 4
    assert op.get_symbol() == "√"


def test_root_operation_zero_root():
    """Test root with zero raises error."""
    op = RootOperation()
    with pytest.raises(OperationError, match="Cannot calculate 0th root"):
        op.execute(10, 0)


def test_root_operation_even_root_negative():
    """Test even root of negative number raises error."""
    op = RootOperation()
    with pytest.raises(OperationError, match="Cannot calculate even root"):
        op.execute(-16, 2)


def test_modulus_operation():
    """Test modulus operation."""
    op = ModulusOperation()
    assert op.execute(10, 3) == 1
    assert op.execute(15, 4) == 3
    assert op.get_symbol() == "%"


def test_modulus_by_zero():
    """Test modulus by zero raises error."""
    op = ModulusOperation()
    with pytest.raises(OperationError, match="Cannot perform modulus with zero"):
        op.execute(10, 0)


def test_int_divide_operation():
    """Test integer division operation."""
    op = IntDivideOperation()
    assert op.execute(10, 3) == 3
    assert op.execute(15, 4) == 3
    assert op.get_symbol() == "//"


def test_int_divide_by_zero():
    """Test integer division by zero raises error."""
    op = IntDivideOperation()
    with pytest.raises(OperationError, match="Cannot divide by zero"):
        op.execute(10, 0)


def test_percentage_operation():
    """Test percentage operation."""
    op = PercentageOperation()
    assert op.execute(50, 200) == 25
    assert op.execute(75, 300) == 25
    assert op.get_symbol() == "%of"


def test_percentage_zero_denominator():
    """Test percentage with zero denominator raises error."""
    op = PercentageOperation()
    with pytest.raises(OperationError, match="Cannot calculate percentage with zero"):
        op.execute(10, 0)


def test_abs_difference_operation():
    """Test absolute difference operation."""
    op = AbsDifferenceOperation()
    assert op.execute(10, 3) == 7
    assert op.execute(3, 10) == 7
    assert op.execute(-5, 5) == 10
    assert op.get_symbol() == "abs_diff"


# Test OperationFactory
def test_factory_create_add():
    """Test factory creates add operation."""
    op = OperationFactory.create_operation('add')
    assert isinstance(op, AddOperation)


def test_factory_create_all_operations():
    """Test factory can create all operations."""
    operations = [
        'add', 'subtract', 'multiply', 'divide', 'power',
        'root', 'modulus', 'int_divide', 'percent', 'abs_diff'
    ]
    
    for op_name in operations:
        op = OperationFactory.create_operation(op_name)
        assert op is not None


def test_factory_case_insensitive():
    """Test factory is case insensitive."""
    op1 = OperationFactory.create_operation('ADD')
    op2 = OperationFactory.create_operation('Add')
    op3 = OperationFactory.create_operation('add')
    
    assert isinstance(op1, AddOperation)
    assert isinstance(op2, AddOperation)
    assert isinstance(op3, AddOperation)


def test_factory_unknown_operation():
    """Test factory raises error for unknown operation."""
    with pytest.raises(OperationError, match="Unknown operation"):
        OperationFactory.create_operation('invalid')


def test_factory_get_available_operations():
    """Test getting available operations."""
    operations = OperationFactory.get_available_operations()
    assert 'add' in operations
    assert 'subtract' in operations
    assert 'power' in operations
    assert len(operations) == 10
