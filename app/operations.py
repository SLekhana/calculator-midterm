"""Operations module implementing the Factory Design Pattern."""

from abc import ABC, abstractmethod
from typing import Dict, Type
from app.exceptions import OperationError


class Operation(ABC):
    """Abstract base class for all operations."""
    
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        """Execute the operation on two operands."""
        pass
    
    @abstractmethod
    def get_symbol(self) -> str:
        """Return the symbol representing this operation."""
        pass


class AddOperation(Operation):
    """Addition operation."""
    
    def execute(self, a: float, b: float) -> float:
        return a + b
    
    def get_symbol(self) -> str:
        return "+"


class SubtractOperation(Operation):
    """Subtraction operation."""
    
    def execute(self, a: float, b: float) -> float:
        return a - b
    
    def get_symbol(self) -> str:
        return "-"


class MultiplyOperation(Operation):
    """Multiplication operation."""
    
    def execute(self, a: float, b: float) -> float:
        return a * b
    
    def get_symbol(self) -> str:
        return "*"


class DivideOperation(Operation):
    """Division operation."""
    
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Cannot divide by zero")
        return a / b
    
    def get_symbol(self) -> str:
        return "/"


class PowerOperation(Operation):
    """Power operation (a^b)."""
    
    def execute(self, a: float, b: float) -> float:
        try:
            return a ** b
        except (ValueError, OverflowError) as e:
            raise OperationError(f"Power operation failed: {str(e)}")
    
    def get_symbol(self) -> str:
        return "^"


class RootOperation(Operation):
    """Root operation (nth root of a)."""
    
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Cannot calculate 0th root")
        if a < 0 and b % 2 == 0:
            raise OperationError("Cannot calculate even root of negative number")
        try:
            return a ** (1 / b)
        except (ValueError, OverflowError) as e:
            raise OperationError(f"Root operation failed: {str(e)}")
    
    def get_symbol(self) -> str:
        return "√"


class ModulusOperation(Operation):
    """Modulus operation (remainder)."""
    
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Cannot perform modulus with zero")
        return a % b
    
    def get_symbol(self) -> str:
        return "%"


class IntDivideOperation(Operation):
    """Integer division operation."""
    
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Cannot divide by zero")
        return a // b
    
    def get_symbol(self) -> str:
        return "//"


class PercentageOperation(Operation):
    """Percentage calculation (a/b * 100)."""
    
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Cannot calculate percentage with zero denominator")
        return (a / b) * 100
    
    def get_symbol(self) -> str:
        return "%of"


class AbsDifferenceOperation(Operation):
    """Absolute difference operation."""
    
    def execute(self, a: float, b: float) -> float:
        return abs(a - b)
    
    def get_symbol(self) -> str:
        return "abs_diff"


class OperationFactory:
    """Factory for creating operation instances."""
    
    _operations: Dict[str, Type[Operation]] = {
        'add': AddOperation,
        'subtract': SubtractOperation,
        'multiply': MultiplyOperation,
        'divide': DivideOperation,
        'power': PowerOperation,
        'root': RootOperation,
        'modulus': ModulusOperation,
        'int_divide': IntDivideOperation,
        'percent': PercentageOperation,
        'abs_diff': AbsDifferenceOperation,
    }
    
    @classmethod
    def create_operation(cls, operation_name: str) -> Operation:
        """
        Create an operation instance based on the operation name.
        
        Args:
            operation_name: Name of the operation
            
        Returns:
            Operation instance
            
        Raises:
            OperationError: If operation name is not recognized
        """
        operation_class = cls._operations.get(operation_name.lower())
        if operation_class is None:
            raise OperationError(f"Unknown operation: {operation_name}")
        return operation_class()
    
    @classmethod
    def get_available_operations(cls) -> list:
        """Return list of available operation names."""
        return list(cls._operations.keys())
