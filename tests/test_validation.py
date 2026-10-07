import pytest

from calculator.validation import numeric_values


def test_numeric_values_converts_to_floats():
    assert numeric_values([2, "3.5"]) == (2.0, 3.5)


def test_numeric_values_rejects_text():
    with pytest.raises(ValueError):
        numeric_values(["hello"])


def test_numeric_values_rejects_nonfinite():
    for bad_value in ["nan", "inf", "-inf"]:
        with pytest.raises(ValueError):
            numeric_values([1, bad_value])
            