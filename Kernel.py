import functools
import itertools
import Elm
import ListKernel
import MaybeKernel
import TupleKernel

"""
We try to keep this module small, but it helps us to have the
most "core" stuff together to avoid circular dependencies for
things like _compare.  It's also a bit helpful to make sure
all of our data types play nice with each other.
"""

def toPy(x):
    if ListKernel.isList(x):
        return list(map(toPy, x))
    elif TupleKernel.isTup(x):
        return tuple(map(toPy, TupleKernel.toPy(x)))
    elif isBool(x):
        return toPyBool(x)
    elif MaybeKernel.isMaybe(x):
        raise Exception('not serializable to Python yet')
    else:
        return x

def toElm(x):
    if type(x) == list:
        return ListKernel.toElm(toElm(item) for item in x)
    elif type(x) == tuple:
        return TupleKernel.toElm(tuple(map(toElm, list(x))))
    elif type(x) == bool:
        return toElmBool(x)
    return x


"""
    BOOL

        It would probably be fine to just use Python bools
        natively, but I am doing it the hard way to make
        sure that List.elm explicitly calls out bools (or
        will otherwise fail tests).
"""

class Bool:
    def __init__(self, v):
        self.v = v

    def __eq__(self, other):
        return self.v == other.v

def isBool(x):
    return type(x) == Bool

def toElmBool(b):
    return Bool(b)

def toPyBool(x):
    if not isBool(x):
        raise Exception('expected Bool')
    return x.v

def toElmPred(f):
    return lambda *args: toElmBool(f(*args))

def toPyPred(f):
    return lambda *args: toPyBool(f(*args))

true = Bool(True)
false = Bool(False)

"""
    Order
"""

class Order:
    def __init__(self, v):
        self.v = v

    def __lt__(self, other):
        raise Exception("comparing Ord types is usually an error")

    def __eq__(self, other):
        raise Exception("comparing Ord types is usually an error")


EQ = 'EQ'
LT = 'LT'
GT = 'GT'

def orderToInt(ord):
    if type(ord) != Order:
        raise Exception("expected Order")

    if ord.v == LT:
        return -1

    if ord.v == EQ:
        return 0

    return 1

@Elm.wrap(None, None, Order)
def toOrder(a, b):
    if a < b:
        return LT

    if a == b:
        return EQ

    return GT


"""
Comparisons
"""

def compare(a, b):
    if a < b:
        return -1

    if a > b:
        return 1

    return 0

@Elm.wrap(None, None, toElmBool)
def eq(a, b):
    if type(a) == int:
        return a == b
    elif ListKernel.isList(a):
        return a == b
    elif TupleKernel.isTup(a):
        return a == b

    raise Exception('eq not implemented fully yet')

