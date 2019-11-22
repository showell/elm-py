import itertools
import Elm

"""
We try to keep this module small, but it helps us to have the
most "core" stuff together to avoid circular dependencies for
things like _compare.  It's also a bit helpful to make sure
all of our data types play nice with each other.
"""

def toPy(x):
    if isList(x):
        return list(toPy(item) for item in listToIter(x))
    elif isTup(x):
        return tuple(map(toPy, toPyTup(x)))
    elif isBool(x):
        return toPyBool(x)
    else:
        return x

def toElm(x):
    if type(x) == list:
        return toElmList(toElm(item) for item in x)
    elif type(x) == tuple:
        return toElmTup(tuple(map(toElm, list(x))))
    elif type(x) == bool:
        return toElmBool(x)
    return x

def toElmList(it):
    """
    This is a flat conversion (assumes items are already Elm-ish).
    """

    out = listNil()
    for x in reversed(list(it)):
        out = listCons(x, out)

    return out

def listNil():
    return ('::', None)

def listCons(x, xs):
    return ('::', (x, xs))

def listUncons(tup):
    if tup[0] != '::':
        print(tup)
        raise Exception('not a list!')
    (x, xs) = tup[1]
    return (x, xs)

def listIsEmpty(tup):
    return tup[1] is None

def listToIter(xs):
    while not listIsEmpty(xs):
        (h, xs) = listUncons(xs)
        yield h

def isList(tup):
    if type(tup) != tuple:
        return False
    return tup[0] == '::'

"""
    TUPLES:

        We don't use native tuples for Elm tuples, because
        we instead use tuples to wrap nearly every non-primitive
        Elm type.  Tuples are actually somewhat frowned upon in
        Elm, so the extra level of indirection here is generally
        harmless.
"""
class Tuple:
    def __init__(self, v):
        self.v = v

def toElmTup(t):
    return Tuple(t)

def toPyTup(x):
    # don't recurse
    return x.v

def isTup(x):
    return type(x) == Tuple

"""
    BOOL

        It would probably be fine to just use Python bools
        natively, but I am doing it the hard way to make
        sure that List.elm explicitly calls out bools (or
        will otherwise fail tests).
"""
def isBool(x):
    if type(x) != tuple:
        return False
    return x[0] == 'Bool'

def toElmBool(b):
    return ('Bool', b)

def toPyBool(x):
    if x[0] != 'Bool':
        raise Exception('expected Bool')
    return x[1]

def toElmPred(f):
    return lambda *args: toElmBool(f(*args))

def toPyPred(f):
    return lambda *args: toPyBool(f(*args))

true = ('Bool', True)
false = ('Bool', False)

def compare(a, b):
    if isList(a):
        for (aa, bb) in itertools.zip_longest(listToIter(a), listToIter(b)):
            if aa is None:
                return -1
            if bb is None:
                return 1
            diff = compare(aa, bb)
            if diff != 0:
                return diff

    return a - b

"""
Comparisons
"""

@Elm.wrap(None, None, toElmBool)
def eq(a, b):
    if type(a) == int:
        return a == b
    elif isList(a):
        return a == b
    elif isTup(a):
        return a == b

    raise Exception('eq not implemented fully yet')

