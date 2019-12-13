import sys
sys.path.append('../lib')
sys.path.append('../../src')
sys.path.append('../../tests')

import ParseHelper
from testHelper import (
    assertEqual,
    assertTrue,
)
import ElmPratt

def test(sElm, sPython=None):
    if sPython is None:
        sPython = sElm

    state = ParseHelper.State(sElm + ' then foo')
    res = ElmPratt.parse(state)
    assertEqual(sPython, res.ast.emit().val)
    state = res.state
    state = ParseHelper.spaceOptional(state)
    assertTrue(ParseHelper.peek(state, 'then'))

def testTokens():
    test('foo.bar == 5')
    test(
        'a * (b+c) * d + (e*f)',
        'a * (b + c) * d + (e * f)'
        )
    test('bLen <= (branchFactor * 4)')

    test(
        'isGood x',
        'isGood(x)',
        )

    test('reverseNodeList')
    test('len <= foo')
    test('fromIndex < 0')
    test('posIndex > len')
    test('newTailLen == branchFactor')
    test('shift == 5')

    test(
        'index < 0 || index >= len',
        'index < 0 or index >= len'
        )

    test(
        'f a > 2',
        'f(a) > 2'
        )

    test(
        'index >= tailIndex len',
        'index >= tailIndex(len)'
        )

    test(
        'pos >= JsArray.length tree',
        'pos >= JsArray.length(tree)'
        )


    test(
        'JsArray.length jsArray < branchFactor',
        'JsArray.length(jsArray) < branchFactor'
        )

    test(
        'oldShift <= newShift || JsArray.length tree == 0',
        'oldShift <= newShift or JsArray.length(tree) == 0'
        )


testTokens()
