import math

from calculator.calculation import Calculation
from calculator.factory import CalculationFactory
from calculator.session import CalculatorSession


def describe(calculation: Calculation, result: float) -> str:
    name = calculation.operation.__name__.capitalize()
    parts = [f"{value:g}" for value in calculation.values]
    for key, value in calculation.options.items():
        parts.append(f"{key}={value:g}")
    return f"{name}({', '.join(parts)}) = {result:g}"


def show_history(session: CalculatorSession) -> None:
    entries = session.get_history()
    for number, (calculation, result) in enumerate(entries, start=1):
        print(f"{number}. {describe(calculation, result)}")


def read_values(command):
    count = CalculationFactory.operand_counts.get(command)
    if count is None:
        text = input("Numbers (separated by spaces): ")
        return [float(piece) for piece in text.split()]
    values = [float(input("First number: "))]
    if count == 2:
        values.append(float(input("Second number: ")))
    return values


def read_options(command):
    options = {}
    for key in CalculationFactory.allowed_options.get(command, ()):
        text = input(f"{key.capitalize()} (blank for default): ").strip()
        if text:
            options[key] = float(text)
    return options


def _run_loop() -> None:
    session = CalculatorSession()
    names = ", ".join(CalculationFactory.operations)
    print("Calculator ready. Type 'help' for commands.")
    while True:
        command = input("Command: ").strip().lower()
        if command == "exit":
            print("Goodbye!")
            break
        if command == "help":
            print(f"Commands: {names}, history, remove, help, exit")
            continue
        if command == "history":
            show_history(session)
            continue
        if command == "remove":
            try:
                number = int(input("Entry number: "))
                removed = session.remove(number - 1)
            except ValueError:
                print("Invalid entry number. Please enter a whole number.")
            except IndexError:
                print("No such entry. Use 'history' to see valid numbers.")
            else:
                print(f"Removed: {describe(*removed)}")
            continue
        if command not in CalculationFactory.operations:
            print("Unknown command. Type 'help' for commands.")
            continue
        try:
            values = read_values(command)
            options = read_options(command)
        except ValueError:
            print("Invalid number. Please enter a valid number.")
            continue
        if not all(math.isfinite(value) for value in values):
            print("Invalid number. Please enter a finite number.")
            continue
        try:
            calculation = CalculationFactory.create(command, *values, **options)
            result = session.calculate(calculation)
        except ZeroDivisionError:
            print("Cannot divide by zero.")
            continue
        except OverflowError:
            print("Result is too large to calculate.")
            continue
        except ValueError as error:
            print(f"Error: {error}")
            continue
        print(f"Result: {result:g}")


def run() -> None:
    try:
        _run_loop()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
