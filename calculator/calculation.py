from abc import ABC, abstractmethod

from calculator.operations import Operations

class Calculation(ABC):
    def __init__(self, a: float, b: float) -> None:
        self.a = a
        self.b = b

    @abstractmethod
    def get_result(self) -> float:
        """Return the result of this calculation."""


class Add(Calculation):
    def get_result(self) -> float:
        return Operations.add(self.a, self.b)


class Subtract(Calculation):
    def get_result(self) -> float:
        return Operations.subtract(self.a, self.b)
    

