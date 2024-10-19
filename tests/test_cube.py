import pytest
from decimal import Decimal
from plugins.cube import CubeCommand
from calculator.command_registry import register_command, command_registry

register_command('cube', CubeCommand)

def test_cube_command_initialization():
    """Test initialization of CubeCommand."""
    command = CubeCommand(Decimal('3'))
    assert command.a == Decimal('3')

def test_cube_command_execute():
    """Test the execute method of CubeCommand."""
    command = CubeCommand(Decimal('2'))
    result = command.execute()
    assert result == Decimal('8')  # 2^3 = 8

    command = CubeCommand(Decimal('0'))
    result = command.execute()
    assert result == Decimal('0')  # 0^3 = 0

    command = CubeCommand(Decimal('-2'))
    result = command.execute()
    assert result == Decimal('-8')  # (-2)^3 = -8

def test_register_command():
    """Test if the command is registered correctly."""
    assert 'cube' in command_registry
    assert command_registry['cube'] is CubeCommand
