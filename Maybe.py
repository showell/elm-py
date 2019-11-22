import Elm
import MaybeKernel as mk

# helper methods for other classes

Just = mk.Just
Nothing = mk.Nothing
isJust = mk.isJust
unboxJust = mk.unboxJust

# normal methods

def withDefault(m, default):
    if mk.isNothing(m):
        return default

    return mk.unboxJust(m)

def mapN(f, *args):
    maybes = [mk.raw(a) for a in args]

    for m in maybes:
        if mk.isRawNothing(m):
            return Nothing()

    vals = [mk.unboxRawJust(m) for m in maybes]
    return Just(f(*vals))

map = mapN
map2 = mapN
map3 = mapN
map4 = mapN
map5 = mapN

@Elm.wrap(None, mk.raw, None)
def andThen(f, m):
    if mk.isRawNothing(m):
        return Nothing()

    return f(mk.unboxRawJust(m))


