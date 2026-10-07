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


def test_distance_is_positive_when_first_is_larger():
    assert Operations.distance(10, 3) == 7


def test_distance_is_positive_when_first_is_smaller():
    assert Operations.distance(3, 10) == 7


def test_distance_of_equal_numbers_is_zero():
    assert Operations.distance(5, 5) == 0

def test_modulo():
    assert Operations.modulo(10, 3) == 1


def test_modulo_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        Operations.modulo(1, 0)


def test_square():
    assert Operations.square(-3) == 9


def test_sqrt():
    assert Operations.sqrt(9) == 3


def test_sqrt_of_negative_raises_value_error():
    with pytest.raises(ValueError):
        Operations.sqrt(-4)


def test_sum_of_many_values():
    assert Operations.sum(1, 2, 3, 4) == 10


def test_sum_of_one_value():
    assert Operations.sum(7) == 7


def test_sum_requires_at_least_one_value():
    with pytest.raises(ValueError):
        Operations.sum()


def test_power_defaults_to_squaring():
    assert Operations.power(3) == 9


def test_power_uses_keyword_only_exponent():
    assert Operations.power(3, exponent=4) == 81


def test_power_rejects_positional_exponent():
    with pytest.raises(TypeError):
        Operations.power(3, 4)


def test_mean_operation():
    assert Operations.mean(10, 20, 30) == 20


def test_stddev_operation_defaults_to_sample():
    assert Operations.stddev(10, 20, 30, 40, 50) == pytest.approx(15.8114, abs=1e-4)


def test_stddev_operation_accepts_ddof_keyword():
    assert Operations.stddev(2, 4, 6, ddof=0) == pytest.approx(1.6330, abs=1e-4)
