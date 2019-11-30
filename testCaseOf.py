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

def assertNothing(v):
    assertEqual(v, Nothing)

Any = MatchParam.Any
Val = MatchParam.Val
Var = MatchParam.Var

Number = CustomType('Number', 'Zero', OneDigit=1, TwoDigit=2)

def test():
    zero = Number.Zero
    one = Number.OneDigit(1)
    twelve = Number.TwoDigit(1, 2)

    v1 = Val(1)
    v2 = Val(2)
    v3 = Val(3)
    v4 = Val(4)

    x = Var('x')
    y = Var('y')

    jd = Just(dict())

    # exact, precise matches
    assertEqual(jd, patternMatch(zero, 'Zero'))
    assertEqual(jd, patternMatch(one, 'OneDigit', v1))
    assertEqual(jd, patternMatch(twelve, 'TwoDigit', v1, v2))

    # bad vtypes
    assertNothing(patternMatch(one, 'Zero'))
    assertNothing(patternMatch(twelve, 'OneDigit', v1))
    assertNothing(patternMatch(zero, 'TwoDigit', v1, v2))

    # good vtypes but wrong values
    assertNothing(patternMatch(one, 'OneDigit', v4))
    assertNothing(patternMatch(twelve, 'TwoDigit', v1, v3))

    # easy matches with Any
    assertEqual(jd, patternMatch(one, 'OneDigit', Any))
    assertEqual(jd, patternMatch(twelve, 'TwoDigit', Any, Any))

    # partial matches with Any
    assertEqual(jd, patternMatch(twelve, 'TwoDigit', v1, Any))
    assertEqual(jd, patternMatch(twelve, 'TwoDigit', Any, v2))

    # mismatches with Any
    assertNothing(patternMatch(twelve, 'TwoDigit', v4, Any))
    assertNothing(patternMatch(twelve, 'TwoDigit', Any, v4))

    # capture matches
    assertEqual(patternMatch(one, 'OneDigit', x),
            Just(dict(x=1)))

    assertEqual(patternMatch(twelve, 'TwoDigit', x, y),
            Just(dict(x=1, y=2)))

    # partial capture matches
    assertEqual(patternMatch(twelve, 'TwoDigit', x, Any),
            Just(dict(x=1)))

    assertEqual(patternMatch(twelve, 'TwoDigit', x, v2),
            Just(dict(x=1)))

    assertEqual(patternMatch(twelve, 'TwoDigit', Any, y),
            Just(dict(y=2)))

    assertEqual(patternMatch(twelve, 'TwoDigit', v1, y),
            Just(dict(y=2)))

    # more failures
    assertNothing(patternMatch(twelve, 'TwoDigit', x, v4))
    assertNothing(patternMatch(twelve, 'TwoDigit', v4, x))
    assertNothing(patternMatch(zero, 'TwoDigit', x, y))
test()
