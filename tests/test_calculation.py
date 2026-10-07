import pytest

from calculator.calculation import Calculation
from calculator.operations import Operations


def test_add_returns_sum_of_two_numbers():
    calculation = Calculation((10, 5), Operations.add)
    assert calculation.get_result() == 15


def test_add_handles_negative_numbers():
    assert Calculation((-4, 1), Operations.add).get_result() == -3


def test_add_handles_decimals():
    assert Calculation((0.1, 0.2), Operations.add).get_result() == pytest.approx(0.3)


def test_two_calculations_are_independent():
    first = Calculation((10, 5), Operations.add)
    second = Calculation((100, 50), Operations.add)
    assert first.get_result() == 15
    assert second.get_result() == 150


def test_subtract_returns_difference_of_two_numbers():
    assert Calculation((20, 7), Operations.subtract).get_result() == 13


def test_subtract_can_return_negative_result():
    assert Calculation((3, 10), Operations.subtract).get_result() == -7


def test_construction_does_not_run_the_operation():
    calls = []

    def spy(*values):
        calls.append(values)
        return sum(values)

    calculation = Calculation((4, 5), spy)
    assert calls == []
    assert calculation.get_result() == 9
    assert calls == [(4.0, 5.0)]


def test_zero_divisor_fails_when_executed_not_when_built():
    calculation = Calculation((1, 0), Operations.divide)
    with pytest.raises(ZeroDivisionError):
        calculation.get_result()


def test_values_are_converted_to_floats_in_a_tuple():
    calculation = Calculation(["2", 3], Operations.add)
    assert calculation.values == (2.0, 3.0)


def test_changing_the_original_list_does_not_change_the_calculation():
    numbers = [1, 2]
    calculation = Calculation(numbers, Operations.add)
    numbers.append(100)
    assert calculation.get_result() == 3


def test_one_value_operation():
    assert Calculation((9,), Operations.sqrt).get_result() == 3


def test_many_value_operation():
    assert Calculation((1, 2, 3, 4), Operations.sum).get_result() == 10


def test_nonfinite_result_is_rejected():
    calculation = Calculation((1e308, 1e308), Operations.add)
    with pytest.raises(ValueError):
        calculation.get_result()


def test_options_are_forwarded_to_the_operation():
    calculation = Calculation((3,), Operations.power, exponent=4)
    assert calculation.options == {"exponent": 4}
    assert calculation.get_result() == 81


def test_options_default_to_empty():
    assert Calculation((3,), Operations.power).options == {}
    assert Calculation((3,), Operations.power).get_result() == 9


def test_calculation_keeps_its_own_copy_of_options():
    settings = {"exponent": 3}
    calculation = Calculation((2,), Operations.power, **settings)
    settings["exponent"] = 10
    assert calculation.get_result() == 8
