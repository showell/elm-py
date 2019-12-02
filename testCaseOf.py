from testHelper import (
        assertEqual,
        assertTrue,
    )

from Elm import (
        patternMatch,
        MatchParam,
        )

from Custom import CustomType
from Maybe import (
        Just,
        Nothing
        )

def assertNone(v):
    assert v is None

Any = MatchParam.Any
Val = MatchParam.Val
Var = MatchParam.Var
Type = MatchParam.Type

Number = CustomType('Number', 'Zero', OneDigit=1, TwoDigit=2)

Zero = Number.Zero
OneDigit = Number.OneDigit
TwoDigit = Number.TwoDigit

def test():
    zero = Number.Zero
    one = Number.OneDigit(1)
    twelve = Number.TwoDigit(1, 2)

    v1 = (Val, 1)
    v2 = (Val, 2)
    v3 = (Val, 3)
    v4 = (Val, 4)

    x = (Var, 'x')
    y = (Var, 'y')

    # exact, precise matches
    assertEqual(True, patternMatch(zero, Type(Zero)))
    assertEqual(True, patternMatch(one, Type(OneDigit), v1))
    assertEqual(True, patternMatch(twelve, Type(TwoDigit), v1, v2))

    # bad vtypes
    assertNone(patternMatch(one, Type(Zero)))
    assertNone(patternMatch(twelve, Type(OneDigit), v1))
    assertNone(patternMatch(zero, Type(TwoDigit), v1, v2))

    # good vtypes but wrong values
    assertNone(patternMatch(one, Type(OneDigit), v4))
    assertNone(patternMatch(twelve, Type(TwoDigit), v1, v3))

    # easy matches with Any
    assertEqual(True, patternMatch(one, Type(OneDigit), Any))
    assertEqual(True, patternMatch(twelve, Type(TwoDigit), Any, Any))

    # partial matches with Any
    assertEqual(True, patternMatch(twelve, Type(TwoDigit), v1, Any))
    assertEqual(True, patternMatch(twelve, Type(TwoDigit), Any, v2))

    # mismatches with Any
    assertNone(patternMatch(twelve, Type(TwoDigit), v4, Any))
    assertNone(patternMatch(twelve, Type(TwoDigit), Any, v4))

    # capture matches
    assertEqual(patternMatch(one, Type(OneDigit), x),
            dict(x=1))

    assertEqual(patternMatch(twelve, Type(TwoDigit), x, y),
            dict(x=1, y=2))

    # partial capture matches
    assertEqual(patternMatch(twelve, Type(TwoDigit), x, Any),
            dict(x=1))

    assertEqual(patternMatch(twelve, Type(TwoDigit), x, v2),
            dict(x=1))

    assertEqual(patternMatch(twelve, Type(TwoDigit), Any, y),
            dict(y=2))

    assertEqual(patternMatch(twelve, Type(TwoDigit), v1, y),
            dict(y=2))

    # more failures
    assertNone(patternMatch(twelve, Type(TwoDigit), x, v4))
    assertNone(patternMatch(twelve, Type(TwoDigit), v4, x))
    assertNone(patternMatch(zero, Type(TwoDigit), x, y))
test()
