import pytest
from calculator.command import Command, AddCommand, SubtractCommand, MultiplyCommand, DivideCommand
from calculator.command_registry import command_registry
from main import OperationCommand, calculate_and_print, repl, main
from decimal import Decimal
from unittest.mock import patch
from multiprocessing import Queue

def test_operation_command_execute():
    command_registry['add'] = AddCommand
    command_registry['subtract'] = SubtractCommand
    command_registry['multiply'] = MultiplyCommand
    command_registry['divide'] = DivideCommand

    result = OperationCommand.execute('add', Decimal('2'), Decimal('3'))
    assert result == Decimal('5')

    result = OperationCommand.execute('subtract', Decimal('5'), Decimal('3'))
    assert result == Decimal('2')

    result = OperationCommand.execute('multiply', Decimal('4'), Decimal('2'))
    assert result == Decimal('8')

    result = OperationCommand.execute('divide', Decimal('10'), Decimal('2'))
    assert result == Decimal('5')

    with pytest.raises(ValueError, match="Unknown operation: unknown"):
        OperationCommand.execute('unknown', Decimal('1'), Decimal('2'))

def test_operation_command_execute_with_multiprocessing():
    result = OperationCommand.execute('add', Decimal('2'), Decimal('3'), use_multiprocessing=True)
    assert result == Decimal('5')

    with pytest.raises(ValueError, match="Cannot divide by zero"):
        OperationCommand.execute('divide', Decimal('1'), Decimal('0'), use_multiprocessing=True)

    with pytest.raises(ValueError, match="Unknown operation: unknown"):
        OperationCommand.execute('unknown', Decimal('1'), Decimal('2'), use_multiprocessing=True)

def test_calculate_and_print(capsys):
    calculate_and_print('3', '2', 'add', False)
    captured = capsys.readouterr()
    assert "The result of 3 add 2 is 5" in captured.out

    calculate_and_print('5', '0', 'divide', False)
    captured = capsys.readouterr()
    assert "Cannot divide by zero" in captured.out

    calculate_and_print('a', '3', 'add', False)
    captured = capsys.readouterr()
    assert "Invalid number input: a or 3 is not a valid number." in captured.out

    calculate_and_print('5', '2', 'unknown', False)
    captured = capsys.readouterr()
    assert "Unknown operation: unknown" in captured.out

def test_repl_exit():
    with patch('builtins.input', side_effect=['exit']):
        with patch('builtins.print') as mock_print:
            repl()
            mock_print.assert_any_call("Exiting the calculator. Goodbye!")

def test_repl_menu():
    with patch('builtins.input', side_effect=['menu', 'exit']):
        with patch('builtins.print') as mock_print:
            repl()
            
            # Extract all print call arguments
            print_calls = [call.args for call in mock_print.call_args_list]
            
            # Check if 'Available commands' is in one of the print calls
            assert any("Available commands:" in call and 
                       "add" in call[1] and 
                       "subtract" in call[1] and 
                       "multiply" in call[1] and 
                       "divide" in call[1] and 
                       "square" in call[1] and 
                       "cube" in call[1] 
                       for call in print_calls)

def test_repl_invalid_input():
    with patch('builtins.input', side_effect=['invalid command', 'exit']):
        with patch('builtins.print') as mock_print:
            repl()
            mock_print.assert_any_call("Invalid number input: invalid or None is not a valid number.")

def test_execute_in_process():
    command = AddCommand(Decimal('2'), Decimal('3'))
    result_queue = Queue()
    command.execute_in_process(result_queue)
    result = result_queue.get()
    assert result == Decimal('5')

    command = DivideCommand(Decimal('2'), Decimal('0'))
    result_queue = Queue()
    command.execute_in_process(result_queue)
    result = result_queue.get()
    assert isinstance(result, ValueError) and str(result) == "Cannot divide by zero"
