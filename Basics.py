import Order
import math

"""
Operators -- We don't have any special support for operators.  Most
    numerical operators in Elm are similar to Python.  On the Python
    side, if you are working with numbers or strings, just use
    normal Python operators.  If you need to pass in partial functions,
    use things like `lambda a: a + 1`.
"""

round_ = round

def compare(a, b):
    return Order.toOrder(a, b)

def modBy(a, b):
    return b % a

def toFloat(n):
    return float(n)

def round(n):
    return round_(n)

def floor(n):
    return math.floor(n)

def ceiling(n):
    return math.ceil(n)

def truncate(n):
    return math.trunc(n)

