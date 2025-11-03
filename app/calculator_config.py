"""Configuration management using environment variables."""

import os
from pathlib import Path
from dotenv import load_dotenv
from app.exceptions import ConfigurationError


class CalculatorConfig:
    """Manages calculator configuration from environment variables."""
    
    def __init__(self):
        """Load configuration from .env file."""
        load_dotenv()
        
        # Base directories
        self.log_dir = os.getenv('CALCULATOR_LOG_DIR', 'logs')
        self.history_dir = os.getenv('CALCULATOR_HISTORY_DIR', 'history')
        
        # History settings
        self.max_history_size = self._get_int('CALCULATOR_MAX_HISTORY_SIZE', 100)
        self.auto_save = self._get_bool('CALCULATOR_AUTO_SAVE', True)
        
        # Calculation settings
        self.precision = self._get_int('CALCULATOR_PRECISION', 2)
        self.max_input_value = self._get_float('CALCULATOR_MAX_INPUT_VALUE', 1e10)
        self.default_encoding = os.getenv('CALCULATOR_DEFAULT_ENCODING', 'utf-8')
        
        # Create directories if they don't exist
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)
        Path(self.history_dir).mkdir(parents=True, exist_ok=True)
    
    def _get_int(self, key: str, default: int) -> int:
        """Get integer value from environment."""
        value = os.getenv(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            raise ConfigurationError(f"Invalid integer value for {key}: {value}")
    
    def _get_float(self, key: str, default: float) -> float:
        """Get float value from environment."""
        value = os.getenv(key)
        if value is None:
            return default
        try:
            return float(value)
        except ValueError:
            raise ConfigurationError(f"Invalid float value for {key}: {value}")
    
    def _get_bool(self, key: str, default: bool) -> bool:
        """Get boolean value from environment."""
        value = os.getenv(key)
        if value is None:
            return default
        return value.lower() in ('true', '1', 'yes', 'on')
