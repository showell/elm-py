import Elm
from Kernel import (
        toElmTup,
        toPyTup,
        )

"""
The Elm Tuple type is just (a, b).  In Python we
box it up as ('#', (a, b)).

The wrappers just use toPyTup and toElmTup to
unbox and box the instances.
"""

@Elm.wrap(None, None, toElmTup)
def pair(a, b):
    return (a, b)

@Elm.wrap(toPyTup, None)
def first(t):
    return t[0]

@Elm.wrap(toPyTup, None)
def second(t):
    return t[1]

@Elm.wrap(None, toPyTup, toElmTup)
def mapFirst(f, t):
    return (f(t[0]), t[1])

@Elm.wrap(None, toPyTup, toElmTup)
def mapSecond(g, t):
    return (t[0], g(t[1]))

@Elm.wrap(None, None, toPyTup, toElmTup)
def mapBoth(f, g, t):
    return (f(t[0]), g(t[1]))

