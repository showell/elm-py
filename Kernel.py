import functools
import itertools
import Elm
import Bool
import ListKernel
import MaybeKernel
import TupleKernel
from Custom import Custom, CustomType

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
    elif isCustomType(x, 'Bool'):
        return Bool.toPy(x)
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
        return Bool.toElm(x)
    return x


def isCustomType(x, name):
    return (type(x) == Custom) and x.isType(name)

"""
    Order
"""

Order = CustomType('Order', 'EQ', 'LT', 'GT')

def isOrder(x):
    return isCustomType(x, 'Order')

def orderToInt(order):
    if not isOrder(order):
        raise Exception("expected Order")

    if order == Order.LT:
        return -1

    if order == Order.EQ:
        return 0

    return 1

def toOrder(a, b):
    if a < b:
        return Order.LT

    if a == b:
        return Order.EQ

    return Order.GT


"""
Comparisons
"""

def compare(a, b):
    if a < b:
        return -1

    if a > b:
        return 1

    return 0

@Elm.wrap(None, None, Bool.toElm)
def eq(a, b):
    if type(a) == int:
        return a == b
    elif ListKernel.isList(a):
        return a == b
    elif TupleKernel.isTup(a):
        return a == b

    raise Exception('eq not implemented fully yet')

