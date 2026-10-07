from calculator.calculation import Calculation
from calculator.operations import Operations


class CalculationFactory:
    operations = {
        "add": Operations.add,
        "subtract": Operations.subtract,
        "multiply": Operations.multiply,
        "divide": Operations.divide,
        "distance": Operations.distance,
        "modulo": Operations.modulo,
        "square": Operations.square,
        "sqrt": Operations.sqrt,
        "sum": Operations.sum,
    }

    # Fixed-arity operations. Operations missing here (sum) accept many values.
    operand_counts = {
        "add": 2,
        "subtract": 2,
        "multiply": 2,
        "divide": 2,
        "distance": 2,
        "modulo": 2,
        "square": 1,
        "sqrt": 1,
    }

    @staticmethod
    def create(name, *values):
        name = name.strip().lower()
        try:
            operation = CalculationFactory.operations[name]
        except KeyError:
            raise ValueError(f"Unknown operation: {name}") from None
        expected = CalculationFactory.operand_counts.get(name)
        if expected is not None and len(values) != expected:
            raise ValueError(
                f"{name} needs {expected} value(s), got {len(values)}"
            )
        return Calculation(values, operation)
