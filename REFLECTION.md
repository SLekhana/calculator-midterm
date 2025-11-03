Reflection on Advanced Calculator Project
Overview

For this project, I developed an advanced calculator application in Python, incorporating a command-line interface (REPL), multiple arithmetic operations, error handling, and several design patterns (Factory, Memento, Observer). The project also included optional enhancements, automated testing, and CI/CD integration with GitHub Actions.

Learning Outcomes

Git and Version Control (CLO1)

I practiced initializing and maintaining a Git repository, committing changes regularly, and organizing branches for feature development.

This helped me understand proper version control workflows and ensured a clear development history.

Linux Command Execution (CLO2)

I used Linux commands for project setup, virtual environments, and running scripts in the terminal.

Python Application Development (CLO3 & CLO6)

Implemented object-oriented principles to structure the calculator with classes and modules.

Incorporated design patterns:

Factory Pattern: Managed dynamic creation of arithmetic operation instances.

Memento Pattern: Enabled undo/redo functionality.

Observer Pattern: Implemented logging and auto-save observers.

Added optional features such as a dynamic help menu and color-coded output to enhance usability.

CI/CD with GitHub Actions (CLO4)

Set up GitHub Actions to run automated tests and ensure a minimum of 90% code coverage on each push.

Learned how CI/CD pipelines can enforce quality standards and improve project reliability.

Command-Line Interface (CLO5)

Developed a REPL interface with commands for all arithmetic operations, history management, undo/redo, and file operations.

Focused on user-friendly interactions and meaningful error messages.

CSV Data Handling (CLO8)

Used pandas for serializing and deserializing calculation history to CSV files.

Learned to handle file I/O exceptions and validate data integrity.

Challenges and Solutions

Design Patterns Integration:

Initially, combining Factory, Memento, and Observer patterns in a modular design was challenging.

I resolved this by clearly separating concerns into different modules (calculator.py, calculator_memento.py, logger.py) and ensuring each pattern had a distinct responsibility.

Undo/Redo Logic:

Implementing the Memento pattern with a stack-based history required careful state management.

Solved by maintaining separate stacks for undo and redo, ensuring proper restoration of calculator states.

Test Coverage:

Covering all edge cases, such as division by zero, negative roots, and large numbers, required extensive parameterized tests with pytest.

Used # pragma: no cover for lines that were intentionally excluded from coverage, such as exception placeholders.

Configuration Management:

Using .env files to configure directories, file paths, and calculation settings improved flexibility.

Ensured default values were applied when environment variables were missing.

Lessons Learned

Proper use of OOP principles and design patterns makes code more maintainable and extensible.

Writing comprehensive tests early in development helps catch errors before deployment.

Integrating CI/CD pipelines ensures quality control and encourages best practices in collaborative projects.

Clear and consistent logging and error handling improve both debugging and user experience.

Optional features like dynamic help menus and color-coded outputs enhance usability without complicating core functionality.

Future Improvements

Implement additional design patterns such as the Command Pattern to further modularize operations.

Extend the REPL interface with more advanced mathematical functions (e.g., trigonometric, logarithmic).

Include a GUI version to make the calculator accessible to non-technical users.

Improve the auto-save feature to support multiple file formats (JSON, Excel).

Author: Lekhana Sandra
