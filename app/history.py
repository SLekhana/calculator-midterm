"""History management with pandas serialization."""

from typing import List, Optional
from pathlib import Path
import pandas as pd
from app.calculation import Calculation
from app.exceptions import HistoryError
from app.calculator_memento import CalculatorMemento, HistoryCaretaker


class CalculationHistory:
    """Manages calculation history with save/load capabilities."""
    
    def __init__(self, max_size: int = 100):
        """
        Initialize history manager.
        
        Args:
            max_size: Maximum number of calculations to store
        """
        self._history: List[Calculation] = []
        self._max_size = max_size
        self._caretaker = HistoryCaretaker()
        
        # Save initial empty state
        self._caretaker.save_state(CalculatorMemento(self._history))
    
    def add_calculation(self, calculation: Calculation):
        """
        Add a calculation to history.
        
        Args:
            calculation: Calculation to add
        """
        self._history.append(calculation)
        
        # Enforce max size
        if len(self._history) > self._max_size:
            self._history.pop(0)
        
        # Save state after adding
        self._caretaker.save_state(CalculatorMemento(self._history))
    
    def get_history(self) -> List[Calculation]:
        """Return copy of calculation history."""
        return self._history.copy()
    
    def clear_history(self):
        """Clear all calculation history and undo/redo stacks."""
        self._history.clear()
        self._caretaker.clear()
        # Save empty state
        self._caretaker.save_state(CalculatorMemento(self._history))
    
    def get_last_calculation(self) -> Optional[Calculation]:
        """Return the most recent calculation."""
        return self._history[-1] if self._history else None
    
    def undo(self) -> bool:
        """
        Undo the last calculation.
        
        Returns:
            True if undo was successful, False otherwise
        """
        if not self.can_undo():
            return False
        
        memento = self._caretaker.undo()
        if memento is None:
            return False
        
        self._history = memento.get_state()
        return True
    
    def redo(self) -> bool:
        """
        Redo the last undone calculation.
        
        Returns:
            True if redo was successful, False otherwise
        """
        if not self.can_redo():
            return False
        
        memento = self._caretaker.redo()
        if memento is None:
            return False
        
        self._history = memento.get_state()
        return True
    
    def can_undo(self) -> bool:
        """Check if undo is available."""
        return self._caretaker.can_undo()
    
    def can_redo(self) -> bool:
        """Check if redo is available."""
        return self._caretaker.can_redo()
    
    def save_to_csv(self, filepath: str):
        """
        Save history to CSV file using pandas.
        
        Args:
            filepath: Path to save the CSV file
            
        Raises:
            HistoryError: If saving fails
        """
        if not self._history:
            raise HistoryError("No history to save")
        
        try:
            # Convert calculations to list of dictionaries
            data = [calc.to_dict() for calc in self._history]
            
            # Create DataFrame and save to CSV
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False)
        except Exception as e:
            raise HistoryError(f"Failed to save history: {str(e)}")
    
    def load_from_csv(self, filepath: str):
        """
        Load history from CSV file using pandas.
        
        Args:
            filepath: Path to the CSV file
            
        Raises:
            HistoryError: If loading fails
        """
        if not Path(filepath).exists():
            raise HistoryError(f"History file not found: {filepath}")
        
        try:
            # Read CSV into DataFrame
            df = pd.read_csv(filepath)
            
            # Convert DataFrame rows to Calculation objects
            self._history.clear()
            for _, row in df.iterrows():
                calc = Calculation.from_dict(row.to_dict())
                self._history.append(calc)
            
            # Clear undo/redo stacks after loading
            self._caretaker.clear()
            # Save loaded state
            self._caretaker.save_state(CalculatorMemento(self._history))
        except Exception as e:
            raise HistoryError(f"Failed to load history: {str(e)}")
    
    def __len__(self) -> int:
        """Return number of calculations in history."""
        return len(self._history)
