import math

from calculator.calculation import Calculation
from calculator.history import History
from calculator.operations import Operations
def describe(calculation: Calculation) -> str:
    name = calculation.operation.__name__.capitalize()
    a = f"{calculation.a:g}"
    b = f"{calculation.b:g}"
    result = f"{calculation.get_result():g}"
    return f"{name}({a}, {b}) = {result}"


def show_history(history: History) -> None:
    entries = history.get_history()
    for number, calculation in enumerate(entries, start=1):
        print(f"{number}. {describe(calculation)}")


def _run_loop() -> None:
    operations = {
        "add": Operations.add,
        "subtract": Operations.subtract,
        "distance": Operations.distance,
    }
    history = History()
    print("Calculator ready. Type 'help' for commands.")
    while True:
        command = input("Command: ").strip().lower()
        if command == "exit":
            print("Goodbye!")
            break
        if command == "help":
            print("Commands: add, subtract, distance, history, remove, help, exit")
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
        operation = operations[command]
        try:
            a = float(input("First number: "))
            b = float(input("Second number: "))
        except ValueError:
            print("Invalid number. Please enter a valid number.")
            continue
        if not (math.isfinite(a) and math.isfinite(b)):
            print("Invalid number. Please enter a finite number.")
            continue
        calculation = Calculation(a, b, operation)
        try:
            result = calculation.get_result()
        except ValueError:
            print("Result is too large to calculate.")
            continue
        history.add(calculation)
        print(f"Result: {result:g}")


def run() -> None:
    try:
        _run_loop()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")


    