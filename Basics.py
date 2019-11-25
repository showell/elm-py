import Order
import math

"""
Operators -- We don't have any special support for operators.  Most
    numerical operators in Elm are similar to Python.  On the Python
    side, if you are working with numbers or strings, just use
    normal Python operators.  If you need to pass in partial functions,
    use things like `lambda a: a + 1`.
"""

round = round
toFloat = float
floor = math.floor
ceiling = math.ceil
truncate = math.trunc
max = max
min = min

def compare(a, b):
    return Order.toOrder(a, b)

def xor(a, b):
    return bool(a) != bool(b)

def modBy(a, b):
    return b % a

def remainderBy(a, b):
    if b >= 0:
        return b % abs(a)
    else:
        return -1 * ((-1 * b) % abs(a))

