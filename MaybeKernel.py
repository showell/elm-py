import Elm

"""
    Maybe:

        This code works, but it's a sloppy version of a custom
        type.  We'll want to have a nicer abstraction for
        variants like Just and Nothing.
"""

class Maybe:
    def __init__(self, v):
        self.v = v

    def __eq__(self, other):
        return self.v == other.v

def isMaybe(x):
    return type(x) == Maybe

_nothing = ('Nothing',)
_just = lambda v: ('Just', v)

_Nothing = Maybe(_nothing)

def raw(x):
    if type(x) != Maybe:
        raise Exception('not a Maybe')
    return x.v

def Nothing():
    return _Nothing

def isRawNothing(v):
    return v == _nothing

def isNothing(v):
    return v == _Nothing

def isRawJust(v):
    return v[0] == 'Just'

def Just(val):
    return Maybe(_just(val))

def isJust(v):
    return isRawJust(raw(v))

def unboxRawJust(m):
    if m[0] != 'Just':
        raise Exception('illegal unboxing')

    return m[1]

@Elm.wrap(raw, None)
def unboxJust(m):
    return unboxRawJust(m)

