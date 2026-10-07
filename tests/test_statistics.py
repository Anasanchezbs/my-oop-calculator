import pytest

from calculator.statistics import mean, standard_deviation


def test_mean_of_several_values():
    assert mean(2, 4, 6) == 4


def test_mean_of_one_value():
    assert mean(7) == 7


def test_mean_requires_at_least_one_value():
    with pytest.raises(ValueError):
        mean()


def test_sample_standard_deviation_is_the_default():
    assert standard_deviation(2, 4, 6) == pytest.approx(2.0)


def test_population_standard_deviation_with_ddof_zero():
    assert standard_deviation(2, 4, 6, ddof=0) == pytest.approx(1.632993, abs=1e-5)


def test_identical_values_have_zero_deviation():
    assert standard_deviation(5, 5, 5) == 0


def test_deviation_requires_two_observations_for_either_setting():
    for ddof in [0, 1]:
        with pytest.raises(ValueError):
            standard_deviation(5, ddof=ddof)


def test_unsupported_ddof_is_rejected():
    with pytest.raises(ValueError):
        standard_deviation(1, 2, 3, ddof=2)


def test_text_that_is_not_a_number_is_rejected():
    with pytest.raises(ValueError):
        mean(1, "x")


def test_missing_and_nonfinite_values_are_rejected():
    for bad_value in [float("nan"), float("inf"), "nan"]:
        with pytest.raises(ValueError):
            mean(1, bad_value)


def test_overflowing_result_is_rejected():
    with pytest.raises(ValueError):
        mean(1e308, 1e308)
