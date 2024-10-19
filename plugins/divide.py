# plugins/divide.py
from decimal import Decimal
from calculator.command import Command
from calculator.command_registry import register_command

class DivideCommand(Command):
    """Concrete Command for Division"""
    def __init__(self, a: Decimal, b: Decimal):
        if b == 0:
            raise ValueError("Error: Division by zero.")
        self.a = a
        self.b = b

    def execute(self) -> Decimal:
        return self.a / self.b

register_command('divide', DivideCommand)

