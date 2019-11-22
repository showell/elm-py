import Elm

_Nothing = ('Maybe', ('Nothing', ))

def unboxMaybe(v):
    if v[0] != 'Maybe':
        raise Exception('not a Maybe')
    return v[1]

def Just(val):
    return ('Maybe', (('Just', val)))

def Nothing():
    return _Nothing

def isNothing(v):
    return v == _Nothing

def isJust(v):
    return unboxMaybe(v)[0] == 'Just'

@Elm.wrap(unboxMaybe, None)
def unboxJust(m):
    if m[0] != 'Just':
        raise Exception('illegal unboxing')

    return m[1]

# Normal methods

def withDefault(m, default):
    if isNothing(m):
        return default

    return unboxJust(m)
