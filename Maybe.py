import Elm

_nada = ('Nothing',)
_just = lambda v: ('Just', v)
_maybe = lambda v: ('Maybe', v)
_Nothing = _maybe(_nada)

def fromMaybe(v):
    if v[0] != 'Maybe':
        raise Exception('not a Maybe')
    return v[1]

def Just(val):
    return _maybe(_just(val))

def Nothing():
    return _Nothing

def isNothing(v):
    return v == _Nothing

@Elm.wrap(fromMaybe, None)
def isJust(v):
    return v[0] == 'Just'

@Elm.wrap(fromMaybe, None)
def unboxJust(m):
    if m[0] != 'Just':
        raise Exception('illegal unboxing')

    return m[1]

# Normal methods

def withDefault(m, default):
    if isNothing(m):
        return default

    return unboxJust(m)

@Elm.wrap(None, fromMaybe, None)
def map(f, m):
    if m == _nada:
        return _Nothing

    return Just(f(unboxJust(m)))

