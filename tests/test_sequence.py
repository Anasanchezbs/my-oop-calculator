from calculator.factory import CalculationFactory
from calculator.sequence import execute_sequence
from calculator.session import CalculatorSession


def make(name, *values, **options):
    return CalculationFactory.create(name, *values, **options)


def test_worked_request_runs_each_item_independently():
    session = CalculatorSession()
    calculations = [make("add", 2, 3), make("divide", 1, 0), make("square", 3)]
    results, errors = execute_sequence(session, calculations)
    assert results == [5.0, 9.0]
    assert len(errors) == 1
    assert "division" in errors[0]
    assert len(session.get_history()) == 2


def test_a_later_success_still_runs_after_an_earlier_failure():
    session = CalculatorSession()
    calculations = [make("divide", 1, 0), make("add", 1, 1)]
    results, errors = execute_sequence(session, calculations)
    assert results == [2.0]
    assert len(errors) == 1


def test_every_expected_kind_of_error_is_collected():
    session = CalculatorSession()
    calculations = [
        make("sqrt", -4),
        make("power", 10, exponent=1000),
        make("divide", 1, 0),
    ]
    results, errors = execute_sequence(session, calculations)
    assert results == []
    assert len(errors) == 3
    assert session.get_history() == []


def test_empty_sequence_returns_nothing():
    session = CalculatorSession()
    assert execute_sequence(session, []) == ([], [])


def test_preparing_calculations_records_nothing_until_executed():
    session = CalculatorSession()
    calculations = [make("add", 1, 2)]
    assert session.get_history() == []
    execute_sequence(session, calculations)
    assert len(session.get_history()) == 1


def test_changing_the_returned_history_list_cannot_change_the_session():
    session = CalculatorSession()
    execute_sequence(session, [make("add", 1, 2), make("add", 3, 4)])
    session.get_history().clear()
    assert len(session.get_history()) == 2
