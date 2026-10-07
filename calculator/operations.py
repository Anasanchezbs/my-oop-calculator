import math


class Operations:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        return a / b

    @staticmethod
    def distance(a, b):
        return abs(a - b)

    @staticmethod
    def modulo(a, b):
        return a % b

    @staticmethod
    def square(value):
        return value * value

    @staticmethod
    def sqrt(value):
        return math.sqrt(value)

    @staticmethod
    def sum(*values):
        if not values:
            raise ValueError("sum requires at least one value")
        total = 0
        for value in values:
            total += value
        return total

    @staticmethod
    def power(value, *, exponent=2):
        return math.pow(value, exponent)
