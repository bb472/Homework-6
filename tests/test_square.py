import pytest
from decimal import Decimal
from plugins.square import SquareCommand
from calculator.command_registry import register_command, command_registry

register_command('square', SquareCommand)

def test_square_command_initialization():
    """Test initialization of SquareCommand."""
    command = SquareCommand(Decimal('3'))
    assert command.a == Decimal('3')

def test_square_command_execute():
    """Test the execute method of SquareCommand."""
    command = SquareCommand(Decimal('4'))
    result = command.execute()
    assert result == Decimal('16')

    command = SquareCommand(Decimal('0'))
    result = command.execute()
    assert result == Decimal('0')

    command = SquareCommand(Decimal('-5'))
    result = command.execute()
    assert result == Decimal('25')

def test_register_command():
    """Test if the command is registered correctly."""
    assert 'square' in command_registry
    assert command_registry['square'] is SquareCommand
