import pytest

from calculator.calculation import Calculation
from calculator.factory import CalculationFactory
from calculator.operations import Operations


def test_create_returns_a_calculation_without_running_it():
    calculation = CalculationFactory.create("add", 2, 3)
    assert isinstance(calculation, Calculation)
    assert calculation.operation is Operations.add


def test_create_normalizes_the_name_and_converts_operands():
    calculation = CalculationFactory.create("  ADD ", "2", "3")
    assert calculation.get_result() == 5.0


def test_registered_operations_compute_expected_results():
    expected = {
        "add": 5,
        "subtract": -1,
        "multiply": 6,
        "divide": pytest.approx(2 / 3),
        "distance": 1,
    }
    for name, answer in expected.items():
        assert CalculationFactory.create(name, 2, 3).get_result() == answer, name


def test_unknown_name_raises_value_error():
    with pytest.raises(ValueError, match="Unknown operation: power"):
        CalculationFactory.create("power", 2, 3)


def test_invalid_operand_is_not_reported_as_unknown_operation():
    with pytest.raises(ValueError) as error:
        CalculationFactory.create("add", "hello", 1)
    assert "Unknown operation" not in str(error.value)


def test_creation_does_not_execute_division_by_zero():
    calculation = CalculationFactory.create("divide", 1, 0)
    with pytest.raises(ZeroDivisionError):
        calculation.get_result()


def test_modulo_is_registered_and_name_is_normalized():
    calculation = CalculationFactory.create("  Modulo ", "10", "3")
    assert calculation.get_result() == 1


def test_one_operand_operation_is_created():
    calculation = CalculationFactory.create("square", 5)
    assert calculation.values == (5.0,)
    assert calculation.get_result() == 25


def test_many_operand_operation_is_created():
    calculation = CalculationFactory.create("sum", 1, 2, 3, 4, 5)
    assert calculation.get_result() == 15


def test_wrong_operand_count_is_rejected():
    for name, values in [("add", [1]), ("add", [1, 2, 3]), ("sqrt", [1, 2])]:
        with pytest.raises(ValueError, match="needs"):
            CalculationFactory.create(name, *values)


def test_empty_sum_is_created_but_fails_when_executed():
    calculation = CalculationFactory.create("sum")
    with pytest.raises(ValueError):
        calculation.get_result()


def test_negative_square_root_is_created_but_fails_when_executed():
    calculation = CalculationFactory.create("sqrt", -4)
    with pytest.raises(ValueError):
        calculation.get_result()
