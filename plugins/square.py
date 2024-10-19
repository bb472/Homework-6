from decimal import Decimal
from calculator.command import Command
from calculator.command_registry import register_command

class SquareCommand(Command):
    """Concrete Command for Square Calculation"""
    def __init__(self, a: Decimal, b: Decimal = None):
        self.a = a

    def execute(self) -> Decimal:
        return self.a ** 2

register_command('square', SquareCommand)
