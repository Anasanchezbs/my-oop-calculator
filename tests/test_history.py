import pytest

from calculator.calculation import Calculation
from calculator.history import History
from calculator.operations import Operations


def make_add(a, b):
    return Calculation((a, b), Operations.add)


def test_new_history_is_empty():
    history = History()
    assert history.get_history() == []


def test_add_stores_the_calculation_and_its_result():
    history = History()
    addition = make_add(10, 5)
    history.add(addition, 15.0)
    assert history.get_history() == [(addition, 15.0)]


def test_history_keeps_entries_in_order():
    history = History()
    first = make_add(10, 5)
    second = Calculation((20, 7), Operations.subtract)
    history.add(first, 15.0)
    history.add(second, 13.0)
    assert history.get_history() == [(first, 15.0), (second, 13.0)]


def test_get_history_returns_a_copy():
    history = History()
    history.add(make_add(10, 5), 15.0)
    snapshot = history.get_history()
    snapshot.clear()
    assert len(history.get_history()) == 1


def test_remove_returns_the_removed_entry():
    history = History()
    first = make_add(10, 5)
    second = Calculation((20, 7), Operations.subtract)
    history.add(first, 15.0)
    history.add(second, 13.0)
    removed = history.remove(0)
    assert removed == (first, 15.0)
    assert history.get_history() == [(second, 13.0)]


def test_remove_rejects_index_past_the_end():
    history = History()
    history.add(make_add(10, 5), 15.0)
    with pytest.raises(IndexError):
        history.remove(1)
    assert len(history.get_history()) == 1


def test_remove_rejects_negative_index():
    history = History()
    history.add(make_add(10, 5), 15.0)
    with pytest.raises(IndexError):
        history.remove(-1)
    assert len(history.get_history()) == 1


def test_clear_removes_every_entry():
    history = History()
    history.add(make_add(1, 1), 2.0)
    history.add(make_add(2, 2), 4.0)
    history.clear()
    assert history.get_history() == []
