# Advanced Calculator Application

A professional command-line calculator application featuring advanced design patterns, comprehensive testing, and CI/CD integration.

## 🎯 Features

### Core Operations
- **Basic Arithmetic**: Addition, Subtraction, Multiplication, Division
- **Advanced Operations**: 
  - Power (a^b)
  - Root (nth root)
  - Modulus (remainder)
  - Integer Division
  - Percentage Calculation
  - Absolute Difference

### Design Patterns
- ✅ **Factory Pattern**: Dynamic operation creation
- ✅ **Memento Pattern**: Undo/Redo functionality
- ✅ **Observer Pattern**: Logging and auto-save
- ✅ **REPL Pattern**: Interactive command-line interface

### Advanced Features
- 📝 Comprehensive logging with Python logging module
- 💾 History management with pandas CSV serialization
- ⚙️ Configuration management via .env files
- 🎨 Color-coded terminal output with colorama
- 🧪 90%+ test coverage with pytest
- 🔄 CI/CD pipeline with GitHub Actions

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Setup

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd calculator-midterm
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
# OR
venv\Scripts\activate     # On Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment (optional):**
```bash
# Copy and edit .env file if needed
cp .env .env.local
```

## 🚀 Usage

### Starting the Calculator
```bash
python main.py
```

### Available Commands

#### Arithmetic Operations
```
add          - Add two numbers
subtract     - Subtract two numbers
multiply     - Multiply two numbers
divide       - Divide two numbers
power        - Raise to power (a^b)
root         - Calculate nth root
modulus      - Calculate remainder
int_divide   - Integer division
percent      - Calculate percentage
abs_diff     - Absolute difference
```

#### Utility Commands
```
history      - Display calculation history
clear        - Clear history
undo         - Undo last calculation
redo         - Redo last undone calculation
save         - Save history to CSV
load         - Load history from CSV
help         - Show help menu
exit         - Exit application
```

### Example Session
```
calculator> add
Enter first number: 10
Enter second number: 5
Result: 10.0 add 5.0 = 15.0

calculator> power
Enter first number: 2
Enter second number: 8
Result: 2.0 power 8.0 = 256.0

calculator> history
Calculation History:
============================================================
1. 10.0 add 5.0 = 15.0
2. 2.0 power 8.0 = 256.0
============================================================

calculator> undo
Undo successful.

calculator> history
Calculation History:
============================================================
1. 10.0 add 5.0 = 15.0
============================================================

calculator> exit
Thank you for using the calculator. Goodbye!
```

## 🧪 Testing

### Run All Tests
```bash
pytest
```

### Run Tests with Coverage
```bash
pytest --cov=app --cov-report=term-missing
```

### Run Tests with HTML Coverage Report
```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html  # View in browser
```

### Run Specific Test File
```bash
pytest tests/test_calculator.py
pytest tests/test_operations.py -v
```

### Check Coverage Threshold
```bash
pytest --cov=app --cov-fail-under=90
```

## 📁 Project Structure
```
calculator-midterm/
├── app/
│   ├── __init__.py
│   ├── calculator.py           # Main Calculator with Observer pattern
│   ├── calculation.py          # Calculation data class
│   ├── calculator_config.py    # Configuration management
│   ├── calculator_memento.py   # Memento pattern for undo/redo
│   ├── exceptions.py           # Custom exceptions
│   ├── history.py              # History management with pandas
│   ├── input_validators.py     # Input validation
│   ├── logger.py               # Logging configuration
│   └── operations.py           # Operations with Factory pattern
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py
│   ├── test_calculation.py
│   ├── test_calculator_config.py
│   ├── test_calculator_memento.py
│   ├── test_exceptions.py
│   ├── test_history.py
│   ├── test_input_validators.py
│   ├── test_logger.py
│   └── test_operations.py
├── .github/
│   └── workflows/
│       └── python-app.yml      # GitHub Actions CI/CD
├── .env                        # Configuration file
├── .gitignore
├── main.py                     # REPL entry point
├── README.md
└── requirements.txt
```

## ⚙️ Configuration

Configuration is managed via `.env` file:
```env
# Base Directories
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history

# History Settings
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true

# Calculation Settings
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=1000000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

## 🔄 CI/CD Pipeline

GitHub Actions automatically:
- ✅ Runs all tests on push/PR
- ✅ Measures code coverage
- ✅ Fails if coverage < 90%
- ✅ Generates coverage reports

View workflow status in the Actions tab on GitHub.

## 🎨 Design Patterns

### Factory Pattern
Creates operation instances dynamically:
```python
operation = OperationFactory.create_operation('add')
result = operation.execute(5, 3)
```

### Memento Pattern
Enables undo/redo functionality:
```python
calculator.calculate('add', 5, 3)
calculator.undo()  # Reverts last operation
calculator.redo()  # Restores undone operation
```

### Observer Pattern
Notifies observers of calculations:
```python
# LoggingObserver logs each calculation
# AutoSaveObserver saves history to CSV
calculator.add_observer(custom_observer)
```

## 📊 Code Quality

- ✅ 90%+ test coverage
- ✅ PEP 8 compliant
- ✅ Type hints where applicable
- ✅ Comprehensive docstrings
- ✅ Error handling with custom exceptions
- ✅ Input validation
- ✅ Logging at appropriate levels

## 🛠️ Development

### Adding New Operations

1. Create operation class in `app/operations.py`:
```python
class MyOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        return a + b  # Your logic
    
    def get_symbol(self) -> str:
        return "+"
```

2. Register in `OperationFactory`:
```python
_operations = {
    'myop': MyOperation,
    # ... other operations
}
```

3. Add tests in `tests/test_operations.py`

### Running Linters
```bash
# Install development tools
pip install flake8 black pylint

# Run flake8
flake8 app/ tests/

# Format with black
black app/ tests/

# Run pylint
pylint app/
```

## 🐛 Troubleshooting

### Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Test Failures
```bash
# Run tests in verbose mode
pytest -v

# Run specific failing test
pytest tests/test_calculator.py::test_calculator_add -v
```

### Coverage Issues
```bash
# Generate detailed coverage report
pytest --cov=app --cov-report=term-missing

# Check which lines are not covered
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

## 👤 Author

**Your Name**
- Course: Python for Web API Development
- Institution: NJIT
- Semester: Fall 2025

## 📄 License

This project is created for educational purposes as part of a midterm assignment.

## 🙏 Acknowledgments

- Python Software Foundation for excellent documentation
- pytest community for testing framework
- pandas community for data manipulation tools
- colorama developers for terminal colors
