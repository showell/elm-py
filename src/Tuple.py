import Elm

def pair(a, b):
    return (a, b)

def first(t):
    return t[0]

def second(t):
    return t[1]

def mapFirst(f, t):
    return (f(t[0]), t[1])

def mapSecond(g, t):
    return (t[0], g(t[1]))

def mapBoth(f, g, t):
    return (f(t[0]), g(t[1]))

