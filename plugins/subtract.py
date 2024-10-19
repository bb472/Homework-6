# plugins/subtract.py
from decimal import Decimal
from calculator.command import Command
from calculator.command_registry import register_command

class SubtractCommand(Command):
    """Concrete Command for Subtraction"""
    def __init__(self, a: Decimal, b: Decimal):
        self.a = a
        self.b = b

    def execute(self) -> Decimal:
        return self.a - self.b

register_command('subtract', SubtractCommand)
