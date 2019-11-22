import Elm
import TupleKernel

toElm = TupleKernel.toElm
toPy = TupleKernel.toPy

@Elm.wrap(None, None, toElm)
def pair(a, b):
    return (a, b)

@Elm.wrap(toPy, None)
def first(t):
    return t[0]

@Elm.wrap(toPy, None)
def second(t):
    return t[1]

@Elm.wrap(None, toPy, toElm)
def mapFirst(f, t):
    return (f(t[0]), t[1])

@Elm.wrap(None, toPy, toElm)
def mapSecond(g, t):
    return (t[0], g(t[1]))

@Elm.wrap(None, None, toPy, toElm)
def mapBoth(f, g, t):
    return (f(t[0]), g(t[1]))

