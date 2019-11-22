import Elm

class Maybe:
    def __init__(self, v):
        self.v = v

    def __eq__(self, other):
        return self.v == other.v

_nada = ('Nothing',)
_just = lambda v: ('Just', v)
_Nothing = Maybe(_nada)

def fromMaybe(x):
    if type(x) != Maybe:
        raise Exception('not a Maybe')
    return x.v

def Just(val):
    return Maybe(_just(val))

def Nothing():
    return _Nothing

def isNothing(v):
    return v == _Nothing

@Elm.wrap(fromMaybe, None)
def isJust(v):
    return v[0] == 'Just'

@Elm.wrap(fromMaybe, None)
def unboxJust(m):
    return _unboxJust(m)

def _unboxJust(m):
    if m[0] != 'Just':
        raise Exception('illegal unboxing')

    return m[1]

# Normal methods

def withDefault(m, default):
    if isNothing(m):
        return default

    return unboxJust(m)

def mapN(f, *args):
    maybes = [fromMaybe(a) for a in args]

    for m in maybes:
        if m == _nada:
            return _Nothing

    vals = [_unboxJust(m) for m in maybes]
    return Just(f(*vals))

map = mapN
map2 = mapN
map3 = mapN
map4 = mapN
map5 = mapN

@Elm.wrap(None, fromMaybe, None)
def andThen(f, m):
    if m == _nada:
        return _Nothing

    return f(_unboxJust(m))


