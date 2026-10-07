from calculator.calculation import Calculation


class History:
    def __init__(self) -> None:
        self._entries: list[tuple[Calculation, float]] = []

    def add(self, calculation: Calculation, result: float) -> None:
        self._entries.append((calculation, result))

    def get_history(self) -> list[tuple[Calculation, float]]:
        return self._entries.copy()

    def remove(self, index: int) -> tuple[Calculation, float]:
        if index < 0 or index >= len(self._entries):
            raise IndexError("History index out of range")
        return self._entries.pop(index)

    def clear(self) -> None:
        self._entries.clear()
