from abc import ABC, abstractmethod


def describe(calculation, result) -> str:
    name = calculation.operation.__name__.capitalize()
    parts = [f"{value:g}" for value in calculation.values]
    for key, value in calculation.options.items():
        parts.append(f"{key}={value:g}")
    return f"{name}({', '.join(parts)}) = {result:g}"


class Command(ABC):
    @abstractmethod
    def execute(self) -> str:
        """Perform an action and return display text."""


class CalculateCommand(Command):
    def __init__(self, session, calculation):
        self.session = session
        self.calculation = calculation

    def execute(self) -> str:
        result = self.session.calculate(self.calculation)
        return f"Result: {result:g}"


class HistoryCommand(Command):
    def __init__(self, session):
        self.session = session

    def execute(self) -> str:
        entries = self.session.get_history()
        if not entries:
            return "History is empty."
        lines = []
        for number, (calculation, result) in enumerate(entries, start=1):
            lines.append(f"{number}. {describe(calculation, result)}")
        return "\n".join(lines)


class ClearHistoryCommand(Command):
    def __init__(self, session):
        self.session = session

    def execute(self) -> str:
        self.session.clear()
        return "History cleared."


class CountCommand(Command):
    def __init__(self, session):
        self.session = session

    def execute(self) -> str:
        return f"Saved calculations: {len(self.session.get_history())}"


class HelpCommand(Command):
    def __init__(self, operation_names):
        self.operation_names = tuple(operation_names)

    def execute(self) -> str:
        names = ", ".join(self.operation_names)
        return f"Commands: {names}, history, clear, count, csv, help, exit"
