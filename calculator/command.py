from decimal import Decimal
from abc import ABC, abstractmethod
import multiprocessing

class Command(ABC):
    @abstractmethod
    def execute(self) -> Decimal:
        raise NotImplementedError("Each command must implement the execute method.")

    def execute_in_process(self, result_queue):
        try:
            result = self.execute()
            result_queue.put(result)
        except Exception as e:
            result_queue.put(e)

class AddCommand(Command):
    def __init__(self, a: Decimal, b: Decimal):
        self.a = a
        self.b = b

    def execute(self) -> Decimal:
        return self.a + self.b

class SubtractCommand(Command):
    def __init__(self, a: Decimal, b: Decimal):
        self.a = a
        self.b = b

    def execute(self) -> Decimal:
        return self.a - self.b

class MultiplyCommand(Command):
    def __init__(self, a: Decimal, b: Decimal):
        self.a = a
        self.b = b

    def execute(self) -> Decimal:
        return self.a * self.b

class DivideCommand(Command):
    def __init__(self, a: Decimal, b: Decimal):
        self.a = a
        self.b = b

    def execute(self) -> Decimal:
        if self.b == 0:
            raise ValueError("Cannot divide by zero")
        return self.a / self.b

