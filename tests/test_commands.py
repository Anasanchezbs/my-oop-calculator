import pytest

from calculator.calculation import Calculation
from calculator.commands import (
    CalculateCommand,
    ClearHistoryCommand,
    Command,
    HelpCommand,
    HistoryCommand,
)
from calculator.operations import Operations
from calculator.session import CalculatorSession


def make_add(a, b):
    return Calculation((a, b), Operations.add)


def test_creating_a_calculate_command_does_not_calculate():
    session = CalculatorSession()
    CalculateCommand(session, make_add(10, 5))
    assert session.get_history() == []


def test_calculate_command_records_and_returns_display_text():
    session = CalculatorSession()
    command = CalculateCommand(session, make_add(10, 5))
    assert command.execute() == "Result: 15"
    assert len(session.get_history()) == 1


def test_failed_calculate_command_propagates_and_records_nothing():
    session = CalculatorSession()
    command = CalculateCommand(session, Calculation((1, 0), Operations.divide))
    with pytest.raises(ZeroDivisionError):
        command.execute()
    assert session.get_history() == []


def test_clear_command_empties_history():
    session = CalculatorSession()
    session.calculate(make_add(1, 1))
    assert ClearHistoryCommand(session).execute() == "History cleared."
    assert session.get_history() == []


def test_history_command_on_empty_history():
    assert HistoryCommand(CalculatorSession()).execute() == "History is empty."


def test_history_command_lists_numbered_entries():
    session = CalculatorSession()
    session.calculate(make_add(10, 5))
    session.calculate(Calculation((3,), Operations.power, exponent=4))
    lines = HistoryCommand(session).execute().split("\n")
    assert lines == ["1. Add(10, 5) = 15", "2. Power(3, exponent=4) = 81"]


def test_help_command_lists_operations_and_actions():
    text = HelpCommand(["add", "power"]).execute()
    assert text == "Commands: add, power, history, clear, count, help, exit"


def test_command_cannot_be_created_directly():
    with pytest.raises(TypeError):
        Command()


def test_subclass_without_execute_cannot_be_created():
    class Incomplete(Command):
        pass

    with pytest.raises(TypeError):
        Incomplete()


def test_different_commands_are_used_the_same_way():
    session = CalculatorSession()
    commands = [
        CalculateCommand(session, make_add(10, 5)),
        HistoryCommand(session),
        ClearHistoryCommand(session),
        HelpCommand(["add"]),
    ]
    outputs = [command.execute() for command in commands]
    assert outputs[0] == "Result: 15"
    assert outputs[1] == "1. Add(10, 5) = 15"
    assert outputs[2] == "History cleared."
    assert outputs[3].startswith("Commands:")


def test_count_command_reports_only_saved_calculations():
    from calculator.commands import CountCommand

    session = CalculatorSession()
    assert CountCommand(session).execute() == "Saved calculations: 0"
    session.calculate(make_add(1, 1))
    with pytest.raises(ZeroDivisionError):
        session.calculate(Calculation((1, 0), Operations.divide))
    assert CountCommand(session).execute() == "Saved calculations: 1"
