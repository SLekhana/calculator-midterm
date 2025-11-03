"""Custom exceptions for the calculator application."""


class CalculatorError(Exception):
    """Base exception for calculator errors."""
    pass


class OperationError(CalculatorError):
    """Exception raised when an operation fails."""
    pass


class ValidationError(CalculatorError):
    """Exception raised when input validation fails."""
    pass


class HistoryError(CalculatorError):
    """Exception raised when history operations fail."""
    pass


class ConfigurationError(CalculatorError):
    """Exception raised when configuration loading fails."""
    pass
