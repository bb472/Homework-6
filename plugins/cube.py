# plugins/cube.py
from decimal import Decimal
from calculator.command import Command
from calculator.command_registry import register_command

class CubeCommand(Command):
    """Concrete Command for Cube Calculation"""
    def __init__(self, a: Decimal, b: Decimal = None):
        self.a = a

    def execute(self) -> Decimal:
        return self.a ** 3

register_command('cube', CubeCommand)

