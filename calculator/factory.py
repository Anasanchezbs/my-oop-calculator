from calculator.calculation import Calculation
from calculator.operations import Operations
from calculator.validation import numeric_values


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
        "power": Operations.power,
        "mean": Operations.mean,
        "stddev": Operations.stddev,
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
        "power": 1,
    }

    # Named settings each operation accepts.
    allowed_options = {
        "power": ("exponent",),
        "stddev": ("ddof",),
    }

    @staticmethod
    def create(name, *values, **options):
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
        allowed = CalculationFactory.allowed_options.get(name, ())
        clean = {}
        for key, value in options.items():
            if key not in allowed:
                raise ValueError(f"{name} does not accept option: {key}")
            clean[key] = numeric_values([value])[0]
        return Calculation(values, operation, **clean)
