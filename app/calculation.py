"""Calculation class to represent a single calculation."""

from datetime import datetime
from typing import Any


class Calculation:
    """Represents a single calculation with operation, operands, and result."""
    
    def __init__(self, operation: str, operand1: float, operand2: float, result: float):
        """
        Initialize a calculation.
        
        Args:
            operation: Name of the operation (e.g., 'add', 'subtract')
            operand1: First operand
            operand2: Second operand
            result: Result of the calculation
        """
        self.operation = operation
        self.operand1 = operand1
        self.operand2 = operand2
        self.result = result
        self.timestamp = datetime.now()
    
    def __repr__(self) -> str:
        """String representation of the calculation."""
        return (f"Calculation(operation='{self.operation}', "
                f"operand1={self.operand1}, operand2={self.operand2}, "
                f"result={self.result}, timestamp={self.timestamp})")
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"{self.operand1} {self.operation} {self.operand2} = {self.result}"
    
    def to_dict(self) -> dict:
        """Convert calculation to dictionary for serialization."""
        return {
            'operation': self.operation,
            'operand1': self.operand1,
            'operand2': self.operand2,
            'result': self.result,
            'timestamp': self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Calculation':
        """Create a Calculation from a dictionary."""
        calc = cls(
            operation=data['operation'],
            operand1=float(data['operand1']),
            operand2=float(data['operand2']),
            result=float(data['result'])
        )
        if 'timestamp' in data:
            calc.timestamp = datetime.fromisoformat(data['timestamp'])
        return calc
