import pytest

from calculator.calculation import Calculation
from calculator.operations import Operations

def test_add_returns_sum_of_two_numbers():
    add = Calculation(10, 5, Operations.add)
    result = add.get_result()
    assert result == 15

def test_add_handles_negative_numbers():
    first = Calculation(-4, 1, Operations.add)
    result = first.get_result()
    assert result == -3

def test_add_handles_decimals():
    first = Calculation(0.5, 0.25, Operations.add)
    assert first.get_result() == 0.75

def test_two_instances_are_independent():
    first = Calculation(10, 5, Operations.add)
    second = Calculation(100, 50, Operations.add)
    assert first.get_result() == 15
    assert second.get_result() == 150

def test_subtract_returns_difference_of_two_numbers():
    subtract = Calculation(20, 7, Operations.subtract)
    result = subtract.get_result()
    assert result == 13

def test_subtract_handles_negative_numbers():
    subtract = Calculation(3, 10, Operations.subtract)
    result = subtract.get_result()
    assert result == -7

def test_construction_does_not_run_the_operation():
    calls = []

    def spy(a, b):
        calls.append((a, b))
        return a + b

    calculation = Calculation(4, 5, spy)
    assert calls == []
    assert calculation.get_result() == 9
    assert calls == [(4, 5)]


def test_zero_divisor_fails_when_executed_not_when_built():
    calculation = Calculation(1, 0, Operations.divide)
    with pytest.raises(ZeroDivisionError):
        calculation.get_result()


def test_different_calculations_can_be_used_the_same_way():
    calculations = [Calculation(10, 5, Operations.add), Calculation(20, 7, Operations.subtract)]
    results = []
    for calculation in calculations:
        results.append(calculation.get_result())
    assert results == [15, 13]

def test_decimal_and_negative_arithmetic():
    assert Calculation(0.1, 0.2, Operations.add).get_result() == pytest.approx(0.3)
    assert Calculation(-5, -8, Operations.subtract).get_result() == 3
    assert Calculation(1.5, 0.25, Operations.subtract).get_result() == pytest.approx(1.25)