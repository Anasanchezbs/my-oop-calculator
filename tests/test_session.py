import pytest

from calculator.calculation import Calculation
from calculator.operations import Operations
from calculator.session import CalculatorSession


def test_calculate_returns_and_records_the_result():
    session = CalculatorSession()
    calculation = Calculation((10, 5), Operations.add)
    assert session.calculate(calculation) == 15
    assert session.get_history() == [(calculation, 15.0)]


def test_failed_calculation_is_not_recorded():
    session = CalculatorSession()
    good = Calculation((10, 5), Operations.add)
    session.calculate(good)
    bad = Calculation((1, 0), Operations.divide)
    with pytest.raises(ZeroDivisionError):
        session.calculate(bad)
    assert session.get_history() == [(good, 15.0)]


def test_clear_empties_the_session_history():
    session = CalculatorSession()
    session.calculate(Calculation((1, 1), Operations.add))
    session.clear()
    assert session.get_history() == []


def test_sessions_are_independent():
    first = CalculatorSession()
    second = CalculatorSession()
    first.calculate(Calculation((1, 1), Operations.add))
    assert second.get_history() == []


def test_changing_the_returned_list_does_not_change_the_session():
    session = CalculatorSession()
    session.calculate(Calculation((1, 1), Operations.add))
    session.get_history().clear()
    assert len(session.get_history()) == 1


def test_remove_returns_the_entry_and_keeps_the_rest():
    session = CalculatorSession()
    first = Calculation((1, 1), Operations.add)
    second = Calculation((2, 2), Operations.add)
    session.calculate(first)
    session.calculate(second)
    assert session.remove(0) == (first, 2.0)
    assert session.get_history() == [(second, 4.0)]
