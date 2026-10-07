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