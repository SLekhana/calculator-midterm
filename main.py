"""Main REPL interface for the calculator application."""

import sys
from colorama import Fore, Style, init
from app.calculator import Calculator
from app.input_validators import InputValidator
from app.exceptions import CalculatorError, ValidationError, OperationError

# Initialize colorama
init(autoreset=True)


class CalculatorREPL:
    """Read-Eval-Print Loop for calculator."""
    
    def __init__(self):
        """Initialize REPL with calculator instance."""
        self.calculator = Calculator()
        self.running = True
        self.validator = InputValidator()
    
    def display_welcome(self):
        """Display welcome message."""
        print(f"{Fore.CYAN}{'=' * 60}")
        print(f"{Fore.CYAN}{'Advanced Calculator Application':^60}")
        print(f"{Fore.CYAN}{'=' * 60}")
        print(f"{Fore.GREEN}Type 'help' for available commands")
        print(f"{Fore.CYAN}{'=' * 60}\n")
    
    def display_help(self):
        """Display help information."""
        print(f"\n{Fore.YELLOW}Available Commands:")
        print(f"{Fore.CYAN}{'=' * 60}")
        
        # Arithmetic operations
        print(f"\n{Fore.GREEN}Arithmetic Operations:")
        operations = self.calculator.get_available_operations()
        for op in operations:
            print(f"  {Fore.WHITE}{op:15} - Perform {op} operation")
        
        # Utility commands
        print(f"\n{Fore.GREEN}Utility Commands:")
        commands = {
            'history': 'Display calculation history',
            'clear': 'Clear calculation history',
            'undo': 'Undo the last calculation',
            'redo': 'Redo the last undone calculation',
            'save': 'Manually save history to file',
            'load': 'Load history from file',
            'help': 'Display this help message',
            'exit': 'Exit the application'
        }
        for cmd, desc in commands.items():
            print(f"  {Fore.WHITE}{cmd:15} - {desc}")
        
        print(f"{Fore.CYAN}{'=' * 60}\n")
    
    def handle_operation(self, operation: str):
        """
        Handle arithmetic operation.
        
        Args:
            operation: Name of the operation to perform
        """
        try:
            # Get operands from user
            operand1 = input(f"{Fore.YELLOW}Enter first number: {Style.RESET_ALL}")
            operand2 = input(f"{Fore.YELLOW}Enter second number: {Style.RESET_ALL}")
            
            # Validate operands
            a, b = self.validator.validate_operands(
                operand1, 
                operand2, 
                self.calculator.config.max_input_value
            )
            
            # Perform calculation
            result = self.calculator.calculate(operation, a, b)
            
            # Display result
            print(f"{Fore.GREEN}Result: {a} {operation} {b} = {result}\n")
        
        except ValidationError as e:
            print(f"{Fore.RED}Validation Error: {str(e)}\n")
        except OperationError as e:
            print(f"{Fore.RED}Operation Error: {str(e)}\n")
        except Exception as e:
            print(f"{Fore.RED}Unexpected Error: {str(e)}\n")
    
    def handle_history(self):
        """Display calculation history."""
        history = self.calculator.get_history()
        
        if not history:
            print(f"{Fore.YELLOW}No calculations in history.\n")
            return
        
        print(f"\n{Fore.CYAN}Calculation History:")
        print(f"{Fore.CYAN}{'=' * 60}")
        for i, calc in enumerate(history, 1):
            print(f"{Fore.WHITE}{i}. {calc}")
        print(f"{Fore.CYAN}{'=' * 60}\n")
    
    def handle_clear(self):
        """Clear calculation history."""
        self.calculator.clear_history()
        print(f"{Fore.GREEN}History cleared successfully.\n")
    
    def handle_undo(self):
        """Undo the last calculation."""
        if self.calculator.undo():
            print(f"{Fore.GREEN}Undo successful.\n")
        else:
            print(f"{Fore.YELLOW}Nothing to undo.\n")
    
    def handle_redo(self):
        """Redo the last undone calculation."""
        if self.calculator.redo():
            print(f"{Fore.GREEN}Redo successful.\n")
        else:
            print(f"{Fore.YELLOW}Nothing to redo.\n")
    
    def handle_save(self):
        """Manually save history to file."""
        try:
            self.calculator.save_history()
            print(f"{Fore.GREEN}History saved successfully.\n")
        except CalculatorError as e:
            print(f"{Fore.RED}Save Error: {str(e)}\n")
    
    def handle_load(self):
        """Load history from file."""
        try:
            self.calculator.load_history()
            print(f"{Fore.GREEN}History loaded successfully.\n")
        except CalculatorError as e:
            print(f"{Fore.RED}Load Error: {str(e)}\n")
    
    def handle_exit(self):
        """Exit the application."""
        print(f"{Fore.CYAN}Thank you for using the calculator. Goodbye!\n")
        self.running = False
    
    def run(self):
        """Run the REPL."""
        self.display_welcome()
        
        while self.running:
            try:
                # Get user input
                command = input(f"{Fore.MAGENTA}calculator> {Style.RESET_ALL}").strip().lower()
                
                if not command:
                    continue
                
                # Handle commands
                if command == 'help':
                    self.display_help()
                elif command == 'history':
                    self.handle_history()
                elif command == 'clear':
                    self.handle_clear()
                elif command == 'undo':
                    self.handle_undo()
                elif command == 'redo':
                    self.handle_redo()
                elif command == 'save':
                    self.handle_save()
                elif command == 'load':
                    self.handle_load()
                elif command == 'exit':
                    self.handle_exit()
                elif command in self.calculator.get_available_operations():
                    self.handle_operation(command)
                else:
                    print(f"{Fore.RED}Unknown command: '{command}'. Type 'help' for available commands.\n")
            
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Use 'exit' command to quit.\n")
            except Exception as e:
                print(f"{Fore.RED}Unexpected error: {str(e)}\n")


def main():
    """Main entry point."""
    repl = CalculatorREPL()
    repl.run()


if __name__ == "__main__":
    main()
