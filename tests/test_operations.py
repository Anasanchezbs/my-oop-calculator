import pytest

from calculator.operations import Operations


def test_add():
    assert Operations.add(2, 3) == 5


def test_subtract():
    assert Operations.subtract(20, 7) == 13


def test_multiply():
    assert Operations.multiply(4, 2.5) == 10


def test_divide():
    assert Operations.divide(10, 4) == 2.5


def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        Operations.divide(1, 0)