"""
    TUPLES:

        We may eventually just use plain Python tuples
        to represent Elm tuples.  Originally we were reserving
        tuples for possible things like custom types, but that's
        no longer the case.
"""
class Tuple:
    def __init__(self, v):
        self.v = v

    def __eq__(self, other):
        return self.v == other.v

    def __str__(self):
        return (
                '( '
                + str(self.v[0])
                + ', '
                + str(self.v[1])
                + ' )'
                )

def toElm(t):
    return Tuple(t)

def toPy(x):
    # don't recurse
    return x.v

def isTup(x):
    return type(x) == Tuple

