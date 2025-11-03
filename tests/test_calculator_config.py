"""Tests for calculator configuration."""

import pytest
import os
from pathlib import Path
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


def test_config_default_values():
    """Test configuration uses default values."""
    config = CalculatorConfig()
    
    assert config.log_dir == 'logs'
    assert config.history_dir == 'history'
    assert config.max_history_size == 100
    assert config.auto_save is True
    assert config.precision == 2
    assert config.max_input_value == 1e10
    assert config.default_encoding == 'utf-8'


def test_config_creates_directories():
    """Test configuration creates necessary directories."""
    config = CalculatorConfig()
    
    assert Path(config.log_dir).exists()
    assert Path(config.history_dir).exists()


def test_config_from_env(monkeypatch):
    """Test configuration loads from environment variables."""
    monkeypatch.setenv('CALCULATOR_LOG_DIR', 'custom_logs')
    monkeypatch.setenv('CALCULATOR_HISTORY_DIR', 'custom_history')
    monkeypatch.setenv('CALCULATOR_MAX_HISTORY_SIZE', '50')
    monkeypatch.setenv('CALCULATOR_AUTO_SAVE', 'false')
    monkeypatch.setenv('CALCULATOR_PRECISION', '4')
    monkeypatch.setenv('CALCULATOR_MAX_INPUT_VALUE', '999999')
    monkeypatch.setenv('CALCULATOR_DEFAULT_ENCODING', 'ascii')
    
    config = CalculatorConfig()
    
    assert config.log_dir == 'custom_logs'
    assert config.history_dir == 'custom_history'
    assert config.max_history_size == 50
    assert config.auto_save is False
    assert config.precision == 4
    assert config.max_input_value == 999999
    assert config.default_encoding == 'ascii'


def test_config_bool_true_variations(monkeypatch):
    """Test boolean configuration accepts various true values."""
    for value in ['true', 'True', 'TRUE', '1', 'yes', 'Yes', 'on', 'On']:
        monkeypatch.setenv('CALCULATOR_AUTO_SAVE', value)
        config = CalculatorConfig()
        assert config.auto_save is True


def test_config_bool_false_variations(monkeypatch):
    """Test boolean configuration accepts various false values."""
    for value in ['false', 'False', 'FALSE', '0', 'no', 'No', 'off', 'Off']:
        monkeypatch.setenv('CALCULATOR_AUTO_SAVE', value)
        config = CalculatorConfig()
        assert config.auto_save is False


def test_config_invalid_int(monkeypatch):
    """Test invalid integer value raises error."""
    monkeypatch.setenv('CALCULATOR_MAX_HISTORY_SIZE', 'not_a_number')
    
    with pytest.raises(ConfigurationError, match="Invalid integer value"):
        CalculatorConfig()


def test_config_invalid_float(monkeypatch):
    """Test invalid float value raises error."""
    monkeypatch.setenv('CALCULATOR_MAX_INPUT_VALUE', 'not_a_number')
    
    with pytest.raises(ConfigurationError, match="Invalid float value"):
        CalculatorConfig()
