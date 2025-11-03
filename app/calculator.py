"""Main calculator class with Observer pattern implementation."""

from typing import List, Protocol
from pathlib import Path
from app.calculation import Calculation
from app.operations import OperationFactory
from app.history import CalculationHistory
from app.logger import Logger
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError


class CalculatorObserver(Protocol):
    """Protocol for calculator observers."""
    
    def update(self, calculation: Calculation):
        """Called when a new calculation is performed."""
        ...


class LoggingObserver:
    """Observer that logs calculations."""
    
    def __init__(self, logger):
        """Initialize with a logger instance."""
        self.logger = logger
    
    def update(self, calculation: Calculation):
        """Log the calculation."""
        self.logger.info(
            f"Calculation performed: {calculation.operation} | "
            f"Operands: {calculation.operand1}, {calculation.operand2} | "
            f"Result: {calculation.result}"
        )


class AutoSaveObserver:
    """Observer that auto-saves history to CSV."""
    
    def __init__(self, history: CalculationHistory, filepath: str):
        """
        Initialize with history and filepath.
        
        Args:
            history: CalculationHistory instance
            filepath: Path to save CSV file
        """
        self.history = history
        self.filepath = filepath
        
        # Ensure directory exists
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    
    def update(self, calculation: Calculation):
        """Auto-save history when calculation is performed."""
        try:
            self.history.save_to_csv(self.filepath)
        except Exception as e:
            # Don't raise exception, just log it
            print(f"Warning: Auto-save failed: {str(e)}")


class Calculator:
    """Main calculator class with observer pattern support."""
    
    def __init__(self, config: CalculatorConfig = None):
        """
        Initialize calculator with configuration.
        
        Args:
            config: CalculatorConfig instance (creates default if None)
        """
        self.config = config or CalculatorConfig()
        self.logger = Logger.get_logger(
            log_dir=self.config.log_dir,
            log_file="calculator.log"
        )
        self.history = CalculationHistory(max_size=self.config.max_history_size)
        self._observers: List[CalculatorObserver] = []
        
        # Register observers
        self._setup_observers()
        
        self.logger.info("Calculator initialized")
    
    def _setup_observers(self):
        """Set up default observers based on configuration."""
        # Add logging observer
        logging_observer = LoggingObserver(self.logger)
        self.add_observer(logging_observer)
        
        # Add auto-save observer if enabled
        if self.config.auto_save:
            history_file = Path(self.config.history_dir) / "calculator_history.csv"
            auto_save_observer = AutoSaveObserver(self.history, str(history_file))
            self.add_observer(auto_save_observer)
    
    def add_observer(self, observer: CalculatorObserver):
        """Add an observer to be notified of calculations."""
        self._observers.append(observer)
    
    def remove_observer(self, observer: CalculatorObserver):
        """Remove an observer."""
        self._observers.remove(observer)
    
    def _notify_observers(self, calculation: Calculation):
        """Notify all observers of a new calculation."""
        for observer in self._observers:
            observer.update(calculation)
    
    def calculate(self, operation: str, operand1: float, operand2: float) -> float:
        """
        Perform a calculation.
        
        Args:
            operation: Name of the operation to perform
            operand1: First operand
            operand2: Second operand
            
        Returns:
            Result of the calculation
            
        Raises:
            OperationError: If operation fails
        """
        try:
            # Create operation instance
            op = OperationFactory.create_operation(operation)
            
            # Execute operation
            result = op.execute(operand1, operand2)
            
            # Round result based on precision
            result = round(result, self.config.precision)
            
            # Create calculation record
            calculation = Calculation(operation, operand1, operand2, result)
            
            # Add to history
            self.history.add_calculation(calculation)
            
            # Notify observers
            self._notify_observers(calculation)
            
            return result
        except OperationError:
            raise
        except Exception as e:
            raise OperationError(f"Calculation failed: {str(e)}")
    
    def get_history(self) -> List[Calculation]:
        """Get calculation history."""
        return self.history.get_history()
    
    def clear_history(self):
        """Clear calculation history."""
        self.history.clear_history()
        self.logger.info("History cleared")
    
    def undo(self) -> bool:
        """Undo the last calculation."""
        success = self.history.undo()
        if success:
            self.logger.info("Undo performed")
        return success
    
    def redo(self) -> bool:
        """Redo the last undone calculation."""
        success = self.history.redo()
        if success:
            self.logger.info("Redo performed")
        return success
    
    def save_history(self, filepath: str = None):
        """
        Manually save history to file.
        
        Args:
            filepath: Optional custom filepath
        """
        if filepath is None:
            filepath = Path(self.config.history_dir) / "calculator_history.csv"
        
        self.history.save_to_csv(str(filepath))
        self.logger.info(f"History saved to {filepath}")
    
    def load_history(self, filepath: str = None):
        """
        Load history from file.
        
        Args:
            filepath: Optional custom filepath
        """
        if filepath is None:
            filepath = Path(self.config.history_dir) / "calculator_history.csv"
        
        self.history.load_from_csv(str(filepath))
        self.logger.info(f"History loaded from {filepath}")
    
    def get_available_operations(self) -> List[str]:
        """Get list of available operations."""
        return OperationFactory.get_available_operations()
