from calculator.commands import (
    CalculateCommand,
    ClearHistoryCommand,
    CountCommand,
    HelpCommand,
    HistoryCommand,
)
from calculator.factory import CalculationFactory
from calculator.inputs import read_csv_values
from calculator.session import CalculatorSession


def split_arguments(arguments):
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
    return values, options


def prepare_csv_command(arguments, session):
    if len(arguments) < 2:
        raise ValueError("Usage: csv OPERATION PATH [option=value]")
    operation, path = arguments[0], arguments[1]
    extra_values, options = split_arguments(arguments[2:])
    if extra_values:
        raise ValueError("csv accepts only option=value after the path")
    values = read_csv_values(path)
    calculation = CalculationFactory.create(operation, *values, **options)
    return CalculateCommand(session, calculation)


def prepare_command(line, session):
    pieces = line.split()
    if not pieces:
        raise ValueError("Enter a command. Type 'help' for commands.")
    name = pieces[0].lower()
    arguments = pieces[1:]
    if name in ("history", "clear", "count", "help"):
        if arguments:
            raise ValueError(f"{name} takes no arguments")
        if name == "history":
            return HistoryCommand(session)
        if name == "clear":
            return ClearHistoryCommand(session)
        if name == "count":
            return CountCommand(session)
        return HelpCommand(CalculationFactory.operations)
    if name == "csv":
        return prepare_csv_command(arguments, session)
    values, options = split_arguments(arguments)
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
        except OSError as error:
            print(f"Error: {error}")


def run() -> None:
    try:
        _run_loop()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
