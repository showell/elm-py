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
abs = abs
sqrt = math.sqrt
e = math.e
pi = math.pi

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

def negate(n):
    return -1 * n

def clamp(lo, hi, x):
    return max(min(x, hi), lo)

def logBase(base, n):
    return math.log(n, base)

def degrees(n):
    return n * pi / 180

def radians(n):
    return n

def turns(n):
    return 2 * pi * n
