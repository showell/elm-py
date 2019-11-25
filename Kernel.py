import functools
import itertools
import Elm
import ListKernel
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
    elif isCustomType(x, 'Maybe'):
        raise Exception('not serializable to Python yet')
    else:
        return x

def toElm(x):
    if type(x) == list:
        return ListKernel.toElm(toElm(item) for item in x)
    elif type(x) == tuple:
        return TupleKernel.toElm(tuple(map(toElm, list(x))))
    return x


def isCustomType(x, name):
    return (type(x) == Custom) and x.isType(name)

"""
Comparisons
"""

def compare(a, b):
    if a < b:
        return -1

    if a > b:
        return 1

    return 0

def eq(a, b):
    if type(a) == int:
        return a == b

    if type(a) == bool:
        return a == b

    if ListKernel.isList(a):
        return a == b

    if TupleKernel.isTup(a):
        return a == b

    raise Exception('eq not implemented fully yet')

