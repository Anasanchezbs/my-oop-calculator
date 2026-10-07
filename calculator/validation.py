from math import isfinite


def numeric_values(values):
    numbers = []
    for value in values:
        number = float(value)
        if not isfinite(number):
            raise ValueError("Values must be finite numbers.")
        numbers.append(number)
    return tuple(numbers)
