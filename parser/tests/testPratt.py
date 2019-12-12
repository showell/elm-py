import sys
sys.path.append('../lib')
sys.path.append('../../src')

from ParseHelper import (
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

import ElmParser
import ElmTypes

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

class OpToken:
    def __init__(self, token):
        self.token = token
        if token == '+':
            self.lbp = 60
        elif token == '*':
            self.lbp = 70

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

op = \
    transform(
        OpToken,
        captureOperator(['<', '+', '*']),
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
        )

def testTokens():
    s = " a * (b + c) * d + (e * f) then x + 2"
    state = State(s)
    res = parse(state, tokenizer)
    print('final ast', res.ast.emit())
    printState(res.state)

testTokens()
