import pytest

from calculator.calculation import Calculation
from calculator.history import History
from calculator.operations import Operations


def make_add(a, b):
    return Calculation((a, b), Operations.add)


def test_new_history_is_empty():
    history = History()
    assert history.get_history() == []


def test_add_stores_the_calculation_object():
    history = History()
    addition = make_add(10, 5)
    history.add(addition)
    assert history.get_history() == [addition]


def test_history_keeps_calculations_in_order():
    history = History()
    first = make_add(10, 5)
    second = Calculation((20, 7), Operations.subtract)
    history.add(first)
    history.add(second)
    assert history.get_history() == [first, second]


def test_get_history_returns_a_copy():
    history = History()
    history.add(make_add(10, 5))
    snapshot = history.get_history()
    snapshot.clear()
    assert len(history.get_history()) == 1


def test_remove_returns_the_removed_calculation():
    history = History()
    first = make_add(10, 5)
    second = Calculation((20, 7), Operations.subtract)
    history.add(first)
    history.add(second)
    removed = history.remove(0)
    assert removed is first
    assert history.get_history() == [second]


def test_remove_rejects_index_past_the_end():
    history = History()
    history.add(make_add(10, 5))
    with pytest.raises(IndexError):
        history.remove(1)
    assert len(history.get_history()) == 1


def test_remove_rejects_negative_index():
    history = History()
    history.add(make_add(10, 5))
    with pytest.raises(IndexError):
        history.remove(-1)
    assert len(history.get_history()) == 1
