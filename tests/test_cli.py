import runpy

from calculator.cli import run


def run_session(monkeypatch, capsys, answers):
    responses = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(responses))
    run()
    return capsys.readouterr().out


def test_arithmetic_session(monkeypatch, capsys):
    answers = ["add", "10", "5", "subtract", "20", "7", "exit"]
    output = run_session(monkeypatch, capsys, answers)
    assert "Result: 15" in output
    assert "Result: 13" in output
    assert "Goodbye!" in output

def test_history_lists_numbered_entries(monkeypatch, capsys):
    answers = ["add", "10", "5", "subtract", "20", "7", "history", "exit"]
    output = run_session(monkeypatch, capsys, answers)
    assert "1. Add(10, 5) = 15" in output
    assert "2. Subtract(20, 7) = 13" in output


def test_remove_deletes_the_numbered_entry(monkeypatch, capsys):
    answers = [
        "add", "10", "5",
        "subtract", "20", "7",
        "remove", "1",
        "history",
        "exit",
    ]
    output = run_session(monkeypatch, capsys, answers)
    assert "Removed: Add(10, 5) = 15" in output
    assert "1. Subtract(20, 7) = 13" in output
    assert "1. Add(10, 5)" not in output


def test_help_lists_commands(monkeypatch, capsys):
    answers = ["help", "exit"]
    output = run_session(monkeypatch, capsys, answers)
    assert "Commands:" in output
    assert "remove" in output
    assert "Goodbye!" in output
def test_invalid_second_number_recovers(monkeypatch, capsys):
    answers = ["add", "10", "hello", "subtract", "20", "7", "history", "exit"]
    output = run_session(monkeypatch, capsys, answers)
    assert "Invalid number" in output
    assert "Result: 13" in output
    assert "1. Subtract(20, 7) = 13" in output
    assert "Add(10" not in output

def test_invalid_first_number_recovers(monkeypatch, capsys):
    answers = ["add", "hello", "add", "10", "5", "history", "exit"]
    output = run_session(monkeypatch, capsys, answers)
    assert "Invalid number" in output
    assert "Result: 15" in output
    assert "1. Add(10, 5) = 15" in output
    assert "2. " not in output


def test_invalid_removal_text_recovers(monkeypatch, capsys):
    answers = ["add", "10", "5", "remove", "abc", "history", "exit"]
    output = run_session(monkeypatch, capsys, answers)
    assert "Invalid entry number" in output
    assert "1. Add(10, 5) = 15" in output
    assert "Removed" not in output


def test_invalid_removal_number_keeps_history(monkeypatch, capsys):
    for bad_number in ["0", "2", "-1"]:
        answers = ["add", "10", "5", "remove", bad_number, "history", "exit"]
        output = run_session(monkeypatch, capsys, answers)
        assert "No such entry" in output, f"no error message for {bad_number}"
        assert "1. Add(10, 5) = 15" in output, f"history changed for {bad_number}"
        assert "Removed" not in output, f"removed something for {bad_number}"
def test_nonfinite_operands_are_rejected(monkeypatch, capsys):
    for bad_value in ["nan", "inf", "-inf"]:
        answers = ["add", bad_value, "1", "history", "exit"]
        output = run_session(monkeypatch, capsys, answers)
        assert "Invalid number" in output, f"{bad_value} was accepted"
        assert "1. " not in output, f"{bad_value} entered history"


def test_overflowed_result_is_rejected(monkeypatch, capsys):
    answers = ["add", "1e308", "1e308", "history", "exit"]
    output = run_session(monkeypatch, capsys, answers)
    assert "too large" in output
    assert "1. " not in output
def run_interrupted_session(monkeypatch, capsys, answers, error):
    responses = iter(answers)

    def fake_input(prompt=""):
        try:
            return next(responses)
        except StopIteration:
            raise error

    monkeypatch.setattr("builtins.input", fake_input)
    run()
    return capsys.readouterr().out


def test_interrupted_input_ends_cleanly(monkeypatch, capsys):
    scenarios = [
        [],
        ["add"],
        ["add", "10"],
        ["remove"],
    ]
    for error in [EOFError, KeyboardInterrupt]:
        for answers in scenarios:
            output = run_interrupted_session(monkeypatch, capsys, answers, error)
            assert "Goodbye!" in output, f"{error.__name__} after {answers}"   


def test_remove_from_empty_history_is_rejected(monkeypatch, capsys):
    answers = ["remove", "1", "exit"]
    output = run_session(monkeypatch, capsys, answers)
    assert "No such entry" in output


def test_remove_middle_entry_keeps_the_others(monkeypatch, capsys):
    answers = [
        "add", "1", "1",
        "add", "2", "2",
        "add", "3", "3",
        "remove", "2",
        "history",
        "exit",
    ]
    output = run_session(monkeypatch, capsys, answers)
    assert "Removed: Add(2, 2) = 4" in output
    assert "1. Add(1, 1) = 2" in output
    assert "2. Add(3, 3) = 6" in output
    assert "3. " not in output


def test_remove_last_entry_keeps_the_first(monkeypatch, capsys):
    answers = ["add", "1", "1", "add", "2", "2", "remove", "2", "history", "exit"]
    output = run_session(monkeypatch, capsys, answers)
    assert "Removed: Add(2, 2) = 4" in output
    assert "1. Add(1, 1) = 2" in output
    assert "2. " not in output


def test_remove_only_entry_leaves_empty_history(monkeypatch, capsys):
    answers = ["add", "10", "5", "remove", "1", "history", "exit"]
    output = run_session(monkeypatch, capsys, answers)
    assert "Removed: Add(10, 5) = 15" in output
    assert "1. " not in output

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