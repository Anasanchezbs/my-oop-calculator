from math import isfinite

from calculator.validation import numeric_values


class Calculation:
    def __init__(self, values, operation):
        self.values = numeric_values(values)
        self.operation = operation

    def get_result(self):
        result = float(self.operation(*self.values))
        if not isfinite(result):
            raise ValueError("Result is outside the supported range.")
        return result
