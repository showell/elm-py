import itertools

"""
We try to keep this module small, but it helps us to have the
most "core" stuff together to avoid circular dependencies for
things like _compare.  It's also a bit helpful to make sure
all of our data types play nice with each other.
"""

def listUncons(lst):
    return (lst[1], lst[2])

def listIsEmpty(xs):
    return xs[0] == '[]'

def listToIter(xs):
    while not listIsEmpty(xs):
        (h, xs) = listUncons(xs)
        yield h

def isList(x):
    if type(x) != tuple:
        return False
    return x[0] == '::' or x[0] == '[]'

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

