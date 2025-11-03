"""Memento pattern implementation for undo/redo functionality."""

from typing import List, Optional
from app.calculation import Calculation


class CalculatorMemento:
    """Stores the state of calculator history for undo/redo."""
    
    def __init__(self, history: List[Calculation]):
        """
        Initialize memento with history state.
        
        Args:
            history: List of calculations to save
        """
        self._history = [calc for calc in history]  # Deep copy
    
    def get_state(self) -> List[Calculation]:
        """Return the saved history state."""
        return [calc for calc in self._history]  # Return copy


class HistoryCaretaker:
    """Manages memento states for undo/redo operations."""
    
    def __init__(self):
        """Initialize the caretaker with empty undo/redo stacks."""
        self._states: List[CalculatorMemento] = []
        self._current_index: int = -1
    
    def save_state(self, memento: CalculatorMemento):
        """
        Save a new state and clear any future states.
        
        Args:
            memento: Memento to save
        """
        # Remove any states after current index (for redo clear)
        self._states = self._states[:self._current_index + 1]
        
        # Add new state
        self._states.append(memento)
        self._current_index = len(self._states) - 1
    
    def undo(self) -> Optional[CalculatorMemento]:
        """
        Undo to previous state.
        
        Returns:
            Previous memento state, or None if can't undo
        """
        if not self.can_undo():
            return None
        
        self._current_index -= 1
        return self._states[self._current_index]
    
    def redo(self) -> Optional[CalculatorMemento]:
        """
        Redo to next state.
        
        Returns:
            Next memento state, or None if can't redo
        """
        if not self.can_redo():
            return None
        
        self._current_index += 1
        return self._states[self._current_index]
    
    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return self._current_index > 0
    
    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return self._current_index < len(self._states) - 1
    
    def clear(self):
        """Clear all undo/redo history."""
        self._states.clear()
        self._current_index = -1
