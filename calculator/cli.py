from calculator.calculation import Add, Calculation, Subtract
from calculator.history import History


def describe(calculation: Calculation) -> str:
    name = type(calculation).__name__
    a = f"{calculation.a:g}"
    b = f"{calculation.b:g}"
    result = f"{calculation.get_result():g}"
    return f"{name}({a}, {b}) = {result}"


def show_history(history: History) -> None:
    entries = history.get_history()
    for number, calculation in enumerate(entries, start=1):
        print(f"{number}. {describe(calculation)}")


def run() -> None:
    operations = {"add": Add, "subtract": Subtract}
    history = History()
    print("Calculator ready. Type 'help' for commands.")
    while True:
        command = input("Command: ").strip().lower()
        if command == "exit":
            print("Goodbye!")
            break
        if command == "help":
            print("Commands: add, subtract, history, remove, help, exit")
            continue
        if command == "history":
            show_history(history)
            continue
        if command == "remove":
            number = int(input("Entry number: "))
            removed = history.remove(number - 1)
            print(f"Removed: {describe(removed)}")
            continue
        operation = operations[command]
        a = float(input("First number: "))
        b = float(input("Second number: "))
        calculation = operation(a, b)
        history.add(calculation)
        print(f"Result: {calculation.get_result():g}")