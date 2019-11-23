from Custom import CustomType

"""
    BOOL

        It would probably be fine to just use Python bools
        natively, but doing it this way does give us
        some nice runtime checking.
"""

Bool = CustomType('Bool', 'True', 'False')

# Because True/False are keywords, we can't use
# attribute sugar, so we make these constants for
# convenience.
true = getattr(Bool, 'True')
false = getattr(Bool, 'False')

def toElm(b):
    if type(b) != bool:
        raise Exception('need bool')
    if b:
        return true
    else:
        return false

def toPy(x):
    if x == true:
        return True

    if x == false:
        return False

    raise Exception('unexpected value in Elm type')

def toElmPred(f):
    return lambda *args: toElm(f(*args))

def toPyPred(f):
    return lambda *args: toPy(f(*args))

