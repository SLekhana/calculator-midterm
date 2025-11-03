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
        self._history = history.copy()
    
    def get_state(self) -> List[Calculation]:
        """Return the saved history state."""
        return self._history.copy()


class HistoryCaretaker:
    """Manages memento states for undo/redo operations."""
    
    def __init__(self):
        """Initialize the caretaker with empty undo/redo stacks."""
        self._undo_stack: List[CalculatorMemento] = []
        self._redo_stack: List[CalculatorMemento] = []
    
    def save_state(self, memento: CalculatorMemento):
        """
        Save a new state and clear redo stack.
        
        Args:
            memento: Memento to save
        """
        self._undo_stack.append(memento)
        self._redo_stack.clear()  # Clear redo stack when new action performed
    
    def undo(self) -> Optional[CalculatorMemento]:
        """
        Undo the last operation.
        
        Returns:
            Previous memento state, or None if nothing to undo
        """
        if len(self._undo_stack) < 2:  # Need at least 2 states to undo
            return None
        
        # Move current state to redo stack
        current_state = self._undo_stack.pop()
        self._redo_stack.append(current_state)
        
        # Return previous state
        return self._undo_stack[-1] if self._undo_stack else None
    
    def redo(self) -> Optional[CalculatorMemento]:
        """
        Redo the last undone operation.
        
        Returns:
            Next memento state, or None if nothing to redo
        """
        if not self._redo_stack:
            return None
        
        # Move state back to undo stack
        next_state = self._redo_stack.pop()
        self._undo_stack.append(next_state)
        
        return next_state
    
    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return len(self._undo_stack) > 1
    
    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return len(self._redo_stack) > 0
    
    def clear(self):
        """Clear all undo/redo history."""
        self._undo_stack.clear()
        self._redo_stack.clear()
