from math import e

def create_triangular(a, b, c):
    def f(value):
        if value < a:
            return 0
        if value <= b:
            return (value - a) / (b - a)
        if value <= c:
            return (c - value) / (c - b)
        return 0
    return f


def create_trapezoidal(a, b, c, d):
    def f(value):
        if value < a:
            return 0
        if value <= b:
            return (value - a) / (b - a)
        if value <= c:
            return 1
        if value <= d:
            return (d - value) / d
        return 0
    return f


def create_bell(m, sd):
    def f(value):
        return e**((-(value - m)**2) / (2*sd**2))
    return f


def create_s(a, b):
    def f(value):
        if value <= a:
            return 0
        if value <= (b + a) / 2:
            return 2 * ((value - a) / (b - a)) ** 2
        if value < b:
            return 1 - (2 * ((b - value) / (b - a)) ** 2)
        return 1
    return f


def create_singleton(a):
    def f(value):
        if value == a:
            return 1
        return 0
    return f


def create_gamma(a, b):
    def f(value):
        if value <= a:
            return 0
        if value < b:
            return (value - a) / (b - a)
        return 1
    return f


