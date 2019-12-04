"""
Lists -

    Each list is actually a series of List instances.
"""

import functools
import itertools

@functools.total_ordering
class List:
    def __init__(self, v):
        self.v = v

    def __iter__(self):
        xs = self.v
        while xs is not None:
            (h, lst) = xs
            xs = lst.v
            yield h

    def __lt__(self, other):
        for (aa, bb) in itertools.zip_longest(self, other):
            if aa is None:
                return True
            if bb is None:
                return False

            if aa < bb:
                return True

            if aa > bb:
                return False

        return False

    def __eq__(self, other):
        for (aa, bb) in itertools.zip_longest(self, other):
            if aa is None:
                return True
            if bb is None:
                return False

            if aa != bb:
                return False

        return True

    def __str__(self):
        return ('[ '
            + ', '.join(str(a) for a in self)
            + ' ]')

def empty():
    return List(None)

def cons(x, xs):
    return List((x, xs))

def uncons(x):
    if not isList(x):
        raise Exception('not a list!')
    return x.v

def isEmpty(x):
    return x.v is None

def isList(x):
    return type(x) == List

def toElm(it):
    """
    This is a flat conversion (assumes items are already Elm-ish).
    """

    out = empty()
    for x in reversed(list(it)):
        out = cons(x, out)

    return out

