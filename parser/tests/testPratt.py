import sys
sys.path.append('../lib')
sys.path.append('../../src')
sys.path.append('../../tests')

from ParseHelper import (
    captureInt,
    captureOneOf,
    captureOperator,
    captureTokenLower,
    captureTokenUpper,
    grab,
    printState,
    pChar,
    State,
    transform,
)
from PrattHelper import (
    expression,
    parse,
)

from testHelper import assertEqual

import ElmParser
import ElmTypes

class IntToken:
    lbp = 100

    def __init__(self, token):
        self.token = token

    def __str__(self):
        return self.token

    def nud(self, pratt):
        self.ast = ElmTypes.Int(self.token)
        return (self, pratt)

class VarToken:
    lbp = 100

    def __init__(self, token):
        self.token = token

    def __str__(self):
        return self.token

    def nud(self, pratt):
        self.ast = ElmTypes.ExprVar(self.token)
        if pratt.token is not None:
            if pratt.token.lbp >= self.lbp:
                right, pratt = expression(pratt, self.lbp-1)
                self.ast = ElmTypes.Call([self.ast, right.ast])
        return (self, pratt)

class ParenToken:
    lbp = 200

    def __init__(self, token):
        pass

    def __str__(self):
        return str(self.ast)

    def nud(self, pratt):
        right, pratt = expression(pratt, 0)
        self.ast = ElmTypes.Paren(right.ast)
        pratt = pratt.advance(pChar(')'))
        return (self, pratt)

bindingPowers = {
    '||': 20,
    '&&': 30,
    '==': 40,
    '/=': 40,
    '<': 40,
    '>': 40,
    '<=': 40,
    '>=': 40,
    '++': 50,
    '+': 60,
    '-': 60,
    '*': 70,
    '/': 70,
    '//': 70,
    '^': 80,
    }

ops = list(bindingPowers.keys())
ops.sort(key = len, reverse=True)

class OpToken:
    def __init__(self, token):
        self.token = token
        self.lbp = bindingPowers[token]

    def __str__(self):
        if hasattr(self, 'ast'):
            return str(self.ast)
        return 'unhandled: ' + self.token

    def led(self, left, pratt):
        (right, pratt) = expression(pratt, self.lbp)
        self.ast = ElmTypes.BinOp([left.ast, self.token, right.ast])
        return (self, pratt)

var = \
    transform(
        VarToken,
        captureOneOf(
            captureTokenLower(ElmParser.reservedWords),
            captureTokenUpper(ElmParser.reservedWords),
            )
        )

integer = \
    transform(
        IntToken,
        captureInt
        )

op = \
    transform(
        OpToken,
        captureOperator(ops),
        )

paren = \
    transform(
        ParenToken,
        grab(pChar('('))
        )

tokenizer = \
    captureOneOf(
        var,
        op,
        paren,
        integer,
        )

def test(sElm, sPython=None):
    if sPython is None:
        sPython = sElm

    state = State(sElm + ' then foo')
    res = parse(state, tokenizer)
    assertEqual(sPython, res.ast.emit().val)
    # printState(res.state)


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
