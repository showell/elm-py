from testHelper import (
        assertEqual,
        assertTrue,
    )

from Elm import (
        patternMatch,
        MatchParam,
        )

from Custom import CustomType
from Maybe import Nothing

def assertJust(v):
    assertTrue(v.match('Just'))

def assertNothing(v):
    assertEqual(v, Nothing)

Any = MatchParam.Any
Val = MatchParam.Val

Number = CustomType('Number', 'Zero', OneDigit=1, TwoDigit=2)

def test():
    zero = Number.Zero
    one = Number.OneDigit(1)
    twelve = Number.TwoDigit(1, 2)

    v1 = Val(1)
    v2 = Val(2)
    v3 = Val(3)
    v4 = Val(4)

    # exact, precise matches
    assertJust(patternMatch(zero, 'Zero'))
    assertJust(patternMatch(one, 'OneDigit', v1))
    assertJust(patternMatch(twelve, 'TwoDigit', v1, v2))

    # bad vtypes
    assertNothing(patternMatch(one, 'Zero'))
    assertNothing(patternMatch(twelve, 'OneDigit', v1))
    assertNothing(patternMatch(zero, 'TwoDigit', v1, v2))

    # good vtypes but wrong values
    assertNothing(patternMatch(one, 'OneDigit', v4))
    assertNothing(patternMatch(twelve, 'TwoDigit', v1, v3))


test()
