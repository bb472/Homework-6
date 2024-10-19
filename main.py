import sys
import time
import os
import logging
import logging.config
from decimal import Decimal, InvalidOperation
from calculator.command_registry import command_registry
from calculator.calculations import Calculations
from plugins.plugins_loader import load_plugins
from calculator.calculation import Calculation
from dotenv import load_dotenv

def load_environment_variables():
    load_dotenv()
    settings = {key: value for key, value in os.environ.items()}
    logging.info("Environment variables loaded.")
    return settings

def configure_logging():
    os.makedirs('logs', exist_ok=True)
    logging_conf_path = 'logging.conf'
    if os.path.exists(logging_conf_path):
        logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Logging configured.")

class OperationCommand:
    """Uses the global command registry"""
    @staticmethod
    def execute(operation_name, a, b, use_multiprocessing=False):
        if use_multiprocessing:
            return OperationCommand.execute_with_multiprocessing(operation_name, a, b)
        else:
            command_class = command_registry.get(operation_name)
            if not command_class:
                raise ValueError(f"Unknown operation: {operation_name}")
            command = command_class(a, b)
            return command.execute()

    @staticmethod
    def execute_with_multiprocessing(operation_name, a, b):
        from multiprocessing import Process, Queue
        command_class = command_registry.get(operation_name)
        if not command_class:
            raise ValueError(f"Unknown operation: {operation_name}")

        result_queue = Queue()
        command = command_class(a, b)

        process = Process(target=OperationCommand._execute_command_in_process, args=(command, result_queue))
        process.start()
        process.join()

        result = result_queue.get()

        if isinstance(result, Exception):
            raise result

        return result

    @staticmethod
    def _execute_command_in_process(command, result_queue):
        """Helper function to execute a command in a separate process."""
        try:
            result = command.execute()
            result_queue.put(result)
        except Exception as e:
            result_queue.put(e)  


def get_available_commands():
    """Fetch available commands from the global command registry."""
    return list(command_registry.keys())

def repl(use_multiprocessing=False):
    load_plugins()
    logging.info("Entering REPL Mode")
    print("Welcome to the Interactive Calculator. Type 'menu' to see available commands or 'exit' to quit.")
    if use_multiprocessing:
        print("Running with multiprocessing enabled.")

    while True:
        user_input = input("Enter command (e.g., 3 4 add or 3 cube): ").strip()
        if user_input.lower() == "exit":
            logging.info("Exiting the REPL Mode")
            print("Exiting the calculator. Goodbye!")
            break
        elif user_input.lower() == "menu":
            available_commands = get_available_commands()
            print("Available commands:", ", ".join(available_commands))
            continue

        try:
            parts = user_input.split()
            if len(parts) == 3:
                a, b, operation_name = parts
                calculate_and_print(a, b, operation_name, use_multiprocessing)
            elif len(parts) == 2:
                a, operation_name = parts
                calculate_and_print(a, None, operation_name, use_multiprocessing)
            else:
                print("Invalid input. Please enter in the format: <number1> <number2> <operation> or <number> <operation>")
        except ValueError:
            print("Invalid input. Please enter in the format: <number1> <number2> <operation> or <number> <operation>")

def calculate_and_print(a, b, operation_name, use_multiprocessing):
    try:
        a_decimal = Decimal(a)
        if operation_name in ['add', 'subtract', 'multiply', 'divide']:
            if not b:
                print("Invalid input. Please enter in the format: <number1> <number2> <operation>")
                return
            b_decimal = Decimal(b)
        else:
            b_decimal = None

        start_time = time.time()
        result = OperationCommand.execute(operation_name, a_decimal, b_decimal, use_multiprocessing)
        elapsed_time = time.time() - start_time

        Calculations.add_calculation(Calculation.create(a_decimal, b_decimal, lambda: result))
        logging.info(f"Calculation performed: {a_decimal} {operation_name} {b_decimal} = {result}")

        if b_decimal is not None:
            print(f"The result of {a} {operation_name} {b} is {result}")
        else:
            print(f"The result of {a} {operation_name} is {result}")

        print(f"Calculation took {elapsed_time:.4f} seconds.")
    except InvalidOperation:
        logging.error(f"Invalid number input: {a} or {b} is not a valid number.")
        print(f"Invalid number input: {a} or {b} is not a valid number.")
    except ZeroDivisionError:
        logging.error("Error: Division by zero.")
        print("Error: Division by zero.")
    except ValueError as e:
        logging.error(e)
        print(e)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

def main():
    use_multiprocessing = "mp" in sys.argv or os.getenv("USE_MULTIPROCESSING") == "true"
    try:
        if len(sys.argv) == 1 or "mp" in sys.argv:
            repl(use_multiprocessing)
        elif len(sys.argv) == 4:
            _, a, b, operation_name = sys.argv
            calculate_and_print(a, b, operation_name, use_multiprocessing)
        else:
            print("Usage: python main.py [mp] <number1> <number2> <operation>")
            sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    configure_logging()
    settings = load_environment_variables()

    logging.info(f"Environment: {settings.get('ENVIRONMENT')}")
    logging.info("Application started.")

    main()
