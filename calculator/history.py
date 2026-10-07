from calculator.calculation import Calculation


class History:
    def __init__(self) -> None:
        self._calculations: list[Calculation] = []

    def add(self, calculation: Calculation) -> None:
        self._calculations.append(calculation)

    def get_history(self) -> list[Calculation]:
        return self._calculations.copy()

    def remove(self, index: int) -> Calculation:
        if index < 0 or index >= len(self._calculations):
            raise IndexError("History index out of range")
        return self._calculations.pop(index)
    