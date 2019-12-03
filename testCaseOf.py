from testHelper import (
        assertEqual,
        assertTrue,
    )

from Custom import CustomType
from Elm import (
        patternMatch,
        MatchParam,
        )
from Maybe import (
        Just,
        Nothing
        )
import List

def assertNone(v):
    assert v is None

Any = MatchParam.Any
Val = MatchParam.Val
Var = MatchParam.Var
Variant = MatchParam.Variant
PCons = MatchParam.PCons
PList = MatchParam.PList

def testLists():
    lst0 = List.empty
    lst1 = List.toElm([1])
    lst2 = List.toElm([1, 2, 3])

    assertEqual(True, patternMatch(lst0, PList))
    assertEqual(None, patternMatch(lst1, PList))

    assertEqual(None, patternMatch(lst0, PCons, Any, Any))
    assertEqual(True, patternMatch(lst1, PCons, Any, Any))
    assertEqual(True, patternMatch(lst2, PCons, Any, Any))

    # good vals
    assertEqual(True, patternMatch(lst1, PCons, (Val, 1), Any))
    assertEqual(True, patternMatch(lst2, PCons, (Val, 1), Any))

    # bad vals
    assertEqual(None, patternMatch(lst1, PCons, (Val, 5), Any))
    assertEqual(None, patternMatch(lst2, PCons, (Val, 5), Any))

    # capture
    res = patternMatch(lst2, PCons, (Var, 'h'), (Var, 'r'))
    assertEqual(res['h'], 1)
    assertEqual(list(res['r']), [2, 3])

def testCustomTypes():
    Number = CustomType('Number', 'Zero', OneDigit=1, TwoDigit=2)

    Zero = Number.Zero
    OneDigit = Number.OneDigit
    TwoDigit = Number.TwoDigit

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
    assertEqual(True, patternMatch(zero, (Variant, Zero)))
    assertEqual(True, patternMatch(one, (Variant, OneDigit), v1))
    assertEqual(True, patternMatch(twelve, (Variant, TwoDigit), v1, v2))

    # bad vtypes
    assertNone(patternMatch(one, (Variant, Zero)))
    assertNone(patternMatch(twelve, (Variant, OneDigit), v1))
    assertNone(patternMatch(zero, (Variant, TwoDigit), v1, v2))

    # good vtypes but wrong values
    assertNone(patternMatch(one, (Variant, OneDigit), v4))
    assertNone(patternMatch(twelve, (Variant, TwoDigit), v1, v3))

    # easy matches with Any
    assertEqual(True, patternMatch(one, (Variant, OneDigit), Any))
    assertEqual(True, patternMatch(twelve, (Variant, TwoDigit), Any, Any))

    # partial matches with Any
    assertEqual(True, patternMatch(twelve, (Variant, TwoDigit), v1, Any))
    assertEqual(True, patternMatch(twelve, (Variant, TwoDigit), Any, v2))

    # mismatches with Any
    assertNone(patternMatch(twelve, (Variant, TwoDigit), v4, Any))
    assertNone(patternMatch(twelve, (Variant, TwoDigit), Any, v4))

    # capture matches
    assertEqual(patternMatch(one, (Variant, OneDigit), x),
            dict(x=1))

    assertEqual(patternMatch(twelve, (Variant, TwoDigit), x, y),
            dict(x=1, y=2))

    # partial capture matches
    assertEqual(patternMatch(twelve, (Variant, TwoDigit), x, Any),
            dict(x=1))

    assertEqual(patternMatch(twelve, (Variant, TwoDigit), x, v2),
            dict(x=1))

    assertEqual(patternMatch(twelve, (Variant, TwoDigit), Any, y),
            dict(y=2))

    assertEqual(patternMatch(twelve, (Variant, TwoDigit), v1, y),
            dict(y=2))

    # more failures
    assertNone(patternMatch(twelve, (Variant, TwoDigit), x, v4))
    assertNone(patternMatch(twelve, (Variant, TwoDigit), v4, x))
    assertNone(patternMatch(zero, (Variant, TwoDigit), x, y))

testCustomTypes()
testLists()
