"""Input validation module."""

from typing import Tuple
from app.exceptions import ValidationError


class InputValidator:
    """Validates user inputs."""
    
    @staticmethod
    def validate_number(value: str, max_value: float = None) -> float:
        """
        Validate and convert a string to a float.
        
        Args:
            value: String representation of a number
            max_value: Maximum allowed value (optional)
            
        Returns:
            Validated float value
            
        Raises:
            ValidationError: If validation fails
        """
        try:
            num = float(value)
        except ValueError:
            raise ValidationError(f"Invalid number: '{value}'")
        
        if max_value is not None and abs(num) > max_value:
            raise ValidationError(f"Number {num} exceeds maximum allowed value {max_value}")
        
        return num
    
    @staticmethod
    def validate_operands(operand1: str, operand2: str, max_value: float = None) -> Tuple[float, float]:
        """
        Validate two operands.
        
        Args:
            operand1: First operand as string
            operand2: Second operand as string
            max_value: Maximum allowed value (optional)
            
        Returns:
            Tuple of two validated floats
            
        Raises:
            ValidationError: If validation fails
        """
        a = InputValidator.validate_number(operand1, max_value)
        b = InputValidator.validate_number(operand2, max_value)
        return a, b
