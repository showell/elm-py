import sys
sys.path.append('../lib')
sys.path.append('../../src')
sys.path.append('../../tests')

from ParseHelper import (
    captureInt,
    captureOneOf,
    captureOperator,
    captureTokenLower,
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
        captureTokenLower(ElmParser.reservedWords)
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

"""
index >= tailIndex len
pos >= JsArray.length tree
JsArray.length jsArray < branchFactor

oldShift <= newShift || JsArray.length tree == 0

isGood x
"""

def test1(sElm, sPython=None):
    if sPython is None:
        sPython = sElm

    state = State(sElm + ' then foo')
    res = parse(state, tokenizer)
    assertEqual(sPython, res.ast.emit().val)
    # printState(res.state)


def testTokens():
    test1(
        'a * (b+c) * d + (e*f)',
        'a * (b + c) * d + (e * f)'
        )
    test1('bLen <= (branchFactor * 4)')

    test1('reverseNodeList')
    test1('len <= foo')
    test1('fromIndex < 0')
    test1('posIndex > len')
    test1('newTailLen == branchFactor')
    test1('shift == 5')

    test1(
        'index < 0 || index >= len',
        'index < 0 or index >= len'
        )

testTokens()
