from Custom import CustomType

Maybe = CustomType('Maybe', 'Nothing', Just=1)

Nothing = Maybe.Nothing
Just = Maybe.Just

# normal methods

def withDefault(m, default):
    if m == Nothing:
        return default

    return m.val

def mapN(f, *maybes):
    for m in maybes:
        if m == Nothing:
            return Nothing

    vals = [m.val for m in maybes]
    return Just(f(*vals))

map = mapN
map2 = mapN
map3 = mapN
map4 = mapN
map5 = mapN

def andThen(f, m):
    if m == Nothing:
        return Nothing

    return f(m.val)


