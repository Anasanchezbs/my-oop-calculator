import pytest

from calculator.calculation import Add, Calculation, Subtract

def test_add_returns_sum_of_two_numbers():
    add = Add(10, 5)
    result = add.get_result()
    assert result == 15

def test_add_handles_negative_numbers():
    first = Add(-4, 1)
    result = first.get_result()
    assert result == -3

def test_add_handles_decimals():
    first = Add(0.5, 0.25)
    assert first.get_result() == 0.75

def test_two_instances_are_independent():
    first = Add(10, 5)
    second = Add(100, 50)
    assert first.get_result() == 15
    assert second.get_result() == 150

def test_subtract_returns_difference_of_two_numbers():
    subtract = Subtract(20, 7)
    result = subtract.get_result()
    assert result == 13

def test_subtract_handles_negative_numbers():
    subtract = Subtract(3, 10)
    result = subtract.get_result()
    assert result == -7

def test_calculation_cannot_be_created_directly():
    with pytest.raises(TypeError):
        Calculation(1, 2)


def test_different_calculations_can_be_used_the_same_way():
    calculations = [Add(10, 5), Subtract(20, 7)]
    results = []
    for calculation in calculations:
        results.append(calculation.get_result())
    assert results == [15, 13]