import runpy

import pytest

from calculator.cli import prepare_command, run
from calculator.commands import (
    CalculateCommand,
    ClearHistoryCommand,
    HelpCommand,
    HistoryCommand,
)
from calculator.session import CalculatorSession


def run_session(monkeypatch, capsys, lines):
    responses = iter(lines)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(responses))
    run()
    return capsys.readouterr().out


def run_interrupted_session(monkeypatch, capsys, lines, error):
    responses = iter(lines)

    def fake_input(prompt=""):
        try:
            return next(responses)
        except StopIteration:
            raise error

    monkeypatch.setattr("builtins.input", fake_input)
    run()
    return capsys.readouterr().out


def test_arithmetic_session(monkeypatch, capsys):
    output = run_session(
        monkeypatch, capsys, ["add 10 5", "subtract 20 7", "exit"]
    )
    assert "Result: 15" in output
    assert "Result: 13" in output
    assert "Goodbye!" in output


def test_command_name_is_case_and_space_insensitive(monkeypatch, capsys):
    output = run_session(monkeypatch, capsys, ["  ADD   2   3  ", "exit"])
    assert "Result: 5" in output


def test_history_lists_numbered_entries(monkeypatch, capsys):
    lines = ["add 10 5", "subtract 20 7", "history", "exit"]
    output = run_session(monkeypatch, capsys, lines)
    assert "1. Add(10, 5) = 15" in output
    assert "2. Subtract(20, 7) = 13" in output


def test_history_when_empty(monkeypatch, capsys):
    output = run_session(monkeypatch, capsys, ["history", "exit"])
    assert "History is empty." in output


def test_clear_empties_history(monkeypatch, capsys):
    lines = ["add 1 1", "clear", "history", "exit"]
    output = run_session(monkeypatch, capsys, lines)
    assert "History cleared." in output
    assert "History is empty." in output
    assert "1. " not in output


def test_help_lists_operations_and_actions(monkeypatch, capsys):
    output = run_session(monkeypatch, capsys, ["help", "exit"])
    assert "Commands:" in output
    assert "power" in output
    assert "clear" in output


def test_power_accepts_a_named_option(monkeypatch, capsys):
    lines = ["power 3 exponent=4", "history", "exit"]
    output = run_session(monkeypatch, capsys, lines)
    assert "Result: 81" in output
    assert "1. Power(3, exponent=4) = 81" in output


def test_many_values_are_accepted(monkeypatch, capsys):
    output = run_session(monkeypatch, capsys, ["sum 1 2 3 4", "exit"])
    assert "Result: 10" in output


def test_divide_by_zero_is_reported_and_not_saved(monkeypatch, capsys):
    lines = ["divide 1 0", "history", "exit"]
    output = run_session(monkeypatch, capsys, lines)
    assert "Cannot divide by zero" in output
    assert "History is empty." in output


def test_overflow_is_reported_and_not_saved(monkeypatch, capsys):
    lines = ["power 10 exponent=1000", "history", "exit"]
    output = run_session(monkeypatch, capsys, lines)
    assert "too large" in output
    assert "History is empty." in output


def test_negative_square_root_is_reported_and_not_saved(monkeypatch, capsys):
    lines = ["sqrt -4", "history", "exit"]
    output = run_session(monkeypatch, capsys, lines)
    assert "Error:" in output
    assert "History is empty." in output


def test_empty_sum_is_reported(monkeypatch, capsys):
    output = run_session(monkeypatch, capsys, ["sum", "exit"])
    assert "at least one value" in output


def test_unknown_operation_is_reported(monkeypatch, capsys):
    output = run_session(monkeypatch, capsys, ["banana 1 2", "exit"])
    assert "Unknown operation: banana" in output
    assert "Goodbye!" in output


def test_wrong_operand_count_is_reported(monkeypatch, capsys):
    output = run_session(monkeypatch, capsys, ["add 1", "exit"])
    assert "needs 2" in output


def test_invalid_number_is_reported(monkeypatch, capsys):
    output = run_session(monkeypatch, capsys, ["add 1 x", "exit"])
    assert "Error:" in output


def test_nonfinite_number_is_reported(monkeypatch, capsys):
    output = run_session(monkeypatch, capsys, ["add nan 1", "exit"])
    assert "finite" in output


def test_blank_line_is_reported(monkeypatch, capsys):
    output = run_session(monkeypatch, capsys, ["", "exit"])
    assert "Enter a command" in output
    assert "Goodbye!" in output


def test_action_commands_reject_arguments(monkeypatch, capsys):
    output = run_session(monkeypatch, capsys, ["history now", "exit"])
    assert "takes no arguments" in output


def test_bad_option_forms_are_reported(monkeypatch, capsys):
    cases = [
        ("power 3 exponent=", "Invalid option"),
        ("power 3 =4", "Invalid option"),
        ("power 3 exponent=2 exponent=3", "Duplicate option"),
        ("power 3 base=2", "does not accept option"),
    ]
    for line, message in cases:
        output = run_session(monkeypatch, capsys, [line, "exit"])
        assert message in output, line


def test_interrupted_input_ends_cleanly(monkeypatch, capsys):
    for error in [EOFError, KeyboardInterrupt]:
        for lines in [[], ["add 1 2"]]:
            output = run_interrupted_session(monkeypatch, capsys, lines, error)
            assert "Goodbye!" in output, error.__name__


def test_prepare_command_builds_without_executing():
    session = CalculatorSession()
    command = prepare_command("add 2 3", session)
    assert isinstance(command, CalculateCommand)
    assert session.get_history() == []
    assert command.execute() == "Result: 5"
    assert len(session.get_history()) == 1


def test_prepare_command_selects_the_action_class():
    session = CalculatorSession()
    assert isinstance(prepare_command("history", session), HistoryCommand)
    assert isinstance(prepare_command("clear", session), ClearHistoryCommand)
    assert isinstance(prepare_command("help", session), HelpCommand)


def test_package_entry_point_starts_the_repl(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt="": "exit")
    runpy.run_module("calculator", run_name="__main__")
    assert "Goodbye!" in capsys.readouterr().out


def test_entry_point_does_not_start_when_imported(monkeypatch, capsys):
    def fail_if_called(prompt=""):
        raise AssertionError("input should not be called")

    monkeypatch.setattr("builtins.input", fail_if_called)
    runpy.run_module("calculator", run_name="imported")
    assert capsys.readouterr().out == ""


def test_count_ignores_failed_calculations(monkeypatch, capsys):
    lines = ["add 1 2", "divide 1 0", "count", "exit"]
    output = run_session(monkeypatch, capsys, lines)
    assert "Saved calculations: 1" in output
