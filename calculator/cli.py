import math

from calculator.calculation import Calculation
from calculator.factory import CalculationFactory
from calculator.history import History


def describe(calculation: Calculation) -> str:
    name = calculation.operation.__name__.capitalize()
    parts = [f"{value:g}" for value in calculation.values]
    for key, value in calculation.options.items():
        parts.append(f"{key}={value:g}")
    result = f"{calculation.get_result():g}"
    return f"{name}({', '.join(parts)}) = {result}"


def show_history(history: History) -> None:
    entries = history.get_history()
    for number, calculation in enumerate(entries, start=1):
        print(f"{number}. {describe(calculation)}")


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
    if command == "power":
        text = input("Exponent (blank for 2): ").strip()
        if text:
            return {"exponent": float(text)}
    return {}


def _run_loop() -> None:
    history = History()
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
            show_history(history)
            continue
        if command == "remove":
            try:
                number = int(input("Entry number: "))
                removed = history.remove(number - 1)
            except ValueError:
                print("Invalid entry number. Please enter a whole number.")
            except IndexError:
                print("No such entry. Use 'history' to see valid numbers.")
            else:
                print(f"Removed: {describe(removed)}")
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
            result = calculation.get_result()
        except ZeroDivisionError:
            print("Cannot divide by zero.")
            continue
        except OverflowError:
            print("Result is too large to calculate.")
            continue
        except ValueError as error:
            print(f"Error: {error}")
            continue
        history.add(calculation)
        print(f"Result: {result:g}")


def run() -> None:
    try:
        _run_loop()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
