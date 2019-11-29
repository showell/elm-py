from testHelper import (
        assertEqual,
    )

from Custom import (
        CustomType,
        patternMatch,
        Nope,
        Yep,
    )


def assertYep(v):
    assertEqual(v, Yep)

def assertNope(v):
    assertEqual(v, Nope)

Any = None

Number = CustomType('Number', 'Zero', OneDigit=1, TwoDigit=2)

def test():
    zero = Number.Zero
    five = Number.OneDigit(5)
    twelve = Number.TwoDigit(1, 2)

    assertYep(patternMatch(zero, 'Zero'))
    assertYep(patternMatch(five, 'OneDigit', 5))
    assertYep(patternMatch(twelve, 'TwoDigit', 1, 2))

    # bad vtypes
    assertNope(patternMatch(five, 'Zero'))
    assertNope(patternMatch(twelve, 'OneDigit', 5))
    assertNope(patternMatch(zero, 'TwoDigit', 1, 2))

    # good vtypes but wrong values
    assertNope(patternMatch(five, 'OneDigit', 6))
    assertNope(patternMatch(twelve, 'TwoDigit', 1, 3))


test()
