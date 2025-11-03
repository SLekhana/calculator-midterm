"""Tests for calculation history."""

import pytest
import tempfile
from pathlib import Path
from app.history import CalculationHistory
from app.calculation import Calculation
from app.exceptions import HistoryError


def test_history_init():
    """Test history initialization."""
    history = CalculationHistory(max_size=50)
    assert len(history) == 0


def test_add_calculation():
    """Test adding calculation to history."""
    history = CalculationHistory()
    calc = Calculation('add', 5, 3, 8)
    
    history.add_calculation(calc)
    
    assert len(history) == 1
    assert history.get_last_calculation() == calc


def test_get_history():
    """Test getting history returns copy."""
    history = CalculationHistory()
    history.add_calculation(Calculation('add', 1, 2, 3))
    
    hist_copy = history.get_history()
    hist_copy.append(Calculation('multiply', 4, 5, 20))
    
    # Original should be unchanged
    assert len(history) == 1


def test_max_size_enforcement():
    """Test history enforces max size."""
    history = CalculationHistory(max_size=3)
    
    history.add_calculation(Calculation('add', 1, 2, 3))
    history.add_calculation(Calculation('subtract', 5, 3, 2))
    history.add_calculation(Calculation('multiply', 2, 3, 6))
    history.add_calculation(Calculation('divide', 10, 2, 5))
    
    # Should only keep last 3
    assert len(history) == 3
    hist = history.get_history()
    assert hist[0].operation == 'subtract'


def test_clear_history():
    """Test clearing history."""
    history = CalculationHistory()
    history.add_calculation(Calculation('add', 1, 2, 3))
    history.add_calculation(Calculation('multiply', 4, 5, 20))
    
    history.clear_history()
    
    assert len(history) == 0
    assert history.get_last_calculation() is None


def test_undo():
    """Test undo functionality."""
    history = CalculationHistory()
    history.add_calculation(Calculation('add', 1, 2, 3))
    history.add_calculation(Calculation('multiply', 4, 5, 20))
    
    success = history.undo()
    
    assert success is True
    assert len(history) == 1


def test_undo_empty():
    """Test undo with empty history."""
    history = CalculationHistory()
    assert history.undo() is False


def test_redo():
    """Test redo functionality."""
    history = CalculationHistory()
    history.add_calculation(Calculation('add', 1, 2, 3))
    history.add_calculation(Calculation('multiply', 4, 5, 20))
    
    history.undo()
    success = history.redo()
    
    assert success is True
    assert len(history) == 2


def test_redo_without_undo():
    """Test redo without undo."""
    history = CalculationHistory()
    history.add_calculation(Calculation('add', 1, 2, 3))
    
    assert history.redo() is False


def test_can_undo():
    """Test can_undo check."""
    history = CalculationHistory()
    assert history.can_undo() is False
    
    history.add_calculation(Calculation('add', 1, 2, 3))
    history.add_calculation(Calculation('multiply', 4, 5, 20))
    
    assert history.can_undo() is True


def test_can_redo():
    """Test can_redo check."""
    history = CalculationHistory()
    assert history.can_redo() is False
    
    history.add_calculation(Calculation('add', 1, 2, 3))
    history.add_calculation(Calculation('multiply', 4, 5, 20))
    history.undo()
    
    assert history.can_redo() is True


def test_save_to_csv():
    """Test saving history to CSV."""
    history = CalculationHistory()
    history.add_calculation(Calculation('add', 1, 2, 3))
    history.add_calculation(Calculation('multiply', 4, 5, 20))
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        filepath = f.name
    
    try:
        history.save_to_csv(filepath)
        assert Path(filepath).exists()
    finally:
        Path(filepath).unlink()


def test_save_empty_history():
    """Test saving empty history raises error."""
    history = CalculationHistory()
    
    with pytest.raises(HistoryError, match="No history to save"):
        history.save_to_csv("test.csv")


def test_load_from_csv():
    """Test loading history from CSV."""
    history = CalculationHistory()
    history.add_calculation(Calculation('add', 1, 2, 3))
    history.add_calculation(Calculation('multiply', 4, 5, 20))
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        filepath = f.name
    
    try:
        history.save_to_csv(filepath)
        
        # Load into new history
        new_history = CalculationHistory()
        new_history.load_from_csv(filepath)
        
        assert len(new_history) == 2
        loaded = new_history.get_history()
        assert loaded[0].operation == 'add'
        assert loaded[1].operation == 'multiply'
    finally:
        Path(filepath).unlink()


def test_load_nonexistent_file():
    """Test loading from nonexistent file raises error."""
    history = CalculationHistory()
    
    with pytest.raises(HistoryError, match="History file not found"):
        history.load_from_csv("nonexistent.csv")
