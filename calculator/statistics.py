import math

import pandas as pd

from calculator.validation import numeric_values


def _series(values, minimum, label):
    numbers = numeric_values(values)
    if len(numbers) < minimum:
        raise ValueError(f"{label} requires at least {minimum} value(s)")
    return pd.Series(numbers, dtype=float)


def _finite(result):
    result = float(result)
    if not math.isfinite(result):
        raise ValueError("Result is outside the supported range.")
    return result


def mean(*values):
    return _finite(_series(values, 1, "mean").mean())


def standard_deviation(*values, ddof=1):
    if ddof not in (0, 1):
        raise ValueError("ddof must be 0 or 1")
    series = _series(values, 2, "standard deviation")
    return _finite(series.std(ddof=int(ddof)))
