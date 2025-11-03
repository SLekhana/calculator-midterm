"""Tests for memento pattern implementation."""

import pytest
from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento, HistoryCaretaker


def test_memento_stores_state():
    """Test memento stores history state."""
    history = [
        Calculation('add', 1, 2, 3),
        Calculation('subtract', 5, 3, 2)
    ]
    
    memento = CalculatorMemento(history)
    restored = memento.get_state()
    
    assert len(restored) == 2
    assert restored[0].operation == 'add'
    assert restored[1].operation == 'subtract'


def test_memento_returns_copy():
    """Test memento returns a copy, not original."""
    history = [Calculation('add', 1, 2, 3)]
    memento = CalculatorMemento(history)
    restored = memento.get_state()
    
    # Modify restored
    restored.append(Calculation('multiply', 2, 3, 6))
    
    # Original should be unchanged
    assert len(memento.get_state()) == 1


def test_caretaker_save_state():
    """Test caretaker saves state."""
    caretaker = HistoryCaretaker()
    history = [Calculation('add', 1, 2, 3)]
    
    memento = CalculatorMemento(history)
    caretaker.save_state(memento)
    
    assert caretaker.can_undo() is False  # Need at least 2 states


def test_caretaker_undo():
    """Test caretaker undo functionality."""
    caretaker = HistoryCaretaker()
    
    # Save initial state
    history1 = [Calculation('add', 1, 2, 3)]
    caretaker.save_state(CalculatorMemento(history1))
    
    # Save second state
    history2 = [
        Calculation('add', 1, 2, 3),
        Calculation('multiply', 4, 5, 20)
    ]
    caretaker.save_state(CalculatorMemento(history2))
    
    # Now we can undo
    assert caretaker.can_undo() is True
    memento = caretaker.undo()
    assert memento is not None
    restored = memento.get_state()
    assert len(restored) == 1


def test_caretaker_redo():
    """Test caretaker redo functionality."""
    caretaker = HistoryCaretaker()
    
    # Save two states
    caretaker.save_state(CalculatorMemento([Calculation('add', 1, 2, 3)]))
    caretaker.save_state(CalculatorMemento([
        Calculation('add', 1, 2, 3),
        Calculation('multiply', 4, 5, 20)
    ]))
    
    # Undo
    caretaker.undo()
    
    # Now we can redo
    assert caretaker.can_redo() is True
    memento = caretaker.redo()
    assert memento is not None
    restored = memento.get_state()
    assert len(restored) == 2


def test_caretaker_undo_clears_redo():
    """Test that new state clears redo stack."""
    caretaker = HistoryCaretaker()
    
    # Save states and undo
    caretaker.save_state(CalculatorMemento([Calculation('add', 1, 2, 3)]))
    caretaker.save_state(CalculatorMemento([
        Calculation('add', 1, 2, 3),
        Calculation('multiply', 4, 5, 20)
    ]))
    caretaker.undo()
    
    assert caretaker.can_redo() is True
    
    # Save new state - should clear redo
    caretaker.save_state(CalculatorMemento([
        Calculation('add', 1, 2, 3),
        Calculation('divide', 10, 2, 5)
    ]))
    
    assert caretaker.can_redo() is False


def test_caretaker_cannot_undo_empty():
    """Test cannot undo with empty stack."""
    caretaker = HistoryCaretaker()
    assert caretaker.can_undo() is False
    assert caretaker.undo() is None


def test_caretaker_cannot_redo_empty():
    """Test cannot redo with empty redo stack."""
    caretaker = HistoryCaretaker()
    assert caretaker.can_redo() is False
    assert caretaker.redo() is None


def test_caretaker_clear():
    """Test clearing caretaker stacks."""
    caretaker = HistoryCaretaker()
    
    caretaker.save_state(CalculatorMemento([Calculation('add', 1, 2, 3)]))
    caretaker.save_state(CalculatorMemento([
        Calculation('add', 1, 2, 3),
        Calculation('multiply', 4, 5, 20)
    ]))
    
    caretaker.clear()
    
    assert caretaker.can_undo() is False
    assert caretaker.can_redo() is False
