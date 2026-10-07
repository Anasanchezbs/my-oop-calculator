from calculator.commands import (
    CalculateCommand,
    ClearHistoryCommand,
    HelpCommand,
    HistoryCommand,
)
from calculator.factory import CalculationFactory
from calculator.session import CalculatorSession


def prepare_command(line, session):
    pieces = line.split()
    if not pieces:
        raise ValueError("Enter a command. Type 'help' for commands.")
    name = pieces[0].lower()
    arguments = pieces[1:]
    if name in ("history", "clear", "help"):
        if arguments:
            raise ValueError(f"{name} takes no arguments")
        if name == "history":
            return HistoryCommand(session)
        if name == "clear":
            return ClearHistoryCommand(session)
        return HelpCommand(CalculationFactory.operations)
    values = []
    options = {}
    for piece in arguments:
        if "=" not in piece:
            values.append(piece)
            continue
        key, _, text = piece.partition("=")
        if not key or not text:
            raise ValueError(f"Invalid option: {piece}")
        if key in options:
            raise ValueError(f"Duplicate option: {key}")
        options[key] = text
    calculation = CalculationFactory.create(name, *values, **options)
    return CalculateCommand(session, calculation)


def _run_loop() -> None:
    session = CalculatorSession()
    print("Calculator ready. Type 'help' for commands.")
    while True:
        line = input("> ").strip()
        if line.lower() == "exit":
            print("Goodbye!")
            break
        try:
            command = prepare_command(line, session)
            print(command.execute())
        except ZeroDivisionError:
            print("Error: Cannot divide by zero.")
        except OverflowError:
            print("Error: Result is too large to calculate.")
        except ValueError as error:
            print(f"Error: {error}")


def run() -> None:
    try:
        _run_loop()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
