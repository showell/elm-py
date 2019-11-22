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

    def __eq__(self, other):
        return self.v == other.v

def toElm(t):
    return Tuple(t)

def toPy(x):
    # don't recurse
    return x.v

def isTup(x):
    return type(x) == Tuple

