import sys
sys.path.append('../lib')
sys.path.append('../../src')

import ParseHelper
from ParseHelper import (
    captureOneOf,
    captureOperator,
    captureTokenLower,
    grab,
    lastState,
    printState,
    pChar,
    Result,
    State,
    transform,
)

import ElmParser
import ElmTypes

class Pratt:
    def __init__(self, token, state):
        self.token = token
        self.state = state

    def tokenize(self):
        res = tokenize(self.state)
        if res is None:
            token = None
            state = self.state
        else:
            token = res.ast
            state = res.state
        return Pratt(token, state)

    def advance(self, parse):
        state = parse(self.state)
        if state is None:
            raise 'foo'
        return Pratt(None, state).tokenize()

class VarToken:
    lbp = 100

    def __init__(self, token):
        self.token = token

    def __str__(self):
        return self.token

    def nud(self, pratt):
        """
        # This is sorta broken--we parse over any arguments, but otherwise
        # ignore them
        if token and hasattr(token, 'nud'):
            (right, token, state) = expression(token, state, self.lbp-1)
        """
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

def expression(pratt, rbp=0):
    t = pratt.token
    pratt = pratt.tokenize()
    if pratt.token is None:
        return t.nud(pratt)

    (left, pratt) = t.nud(pratt)

    while pratt.token and rbp < pratt.token.lbp:
        t = pratt.token
        pratt = pratt.tokenize()
        (left, pratt) = t.led(left, pratt)

    return (left, pratt)

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

tokenize = \
    captureOneOf(
        var,
        op,
        paren,
        )

def parse(state):
    pratt = Pratt(None, state).tokenize()
    (left, pratt) = expression(pratt)

    # Since Pratt parsing always looks ahead one token, we
    # cheat here to reset the state for any integration with
    # "outer" parsers.  The ParseHelper module remembers the
    # last valid state.  This is still skipping one too many
    # tokens, though, so I need a better way to keep prior
    # states.
    return Result(ParseHelper.lastState, left.ast)

def testTokens():
    s = " a * (b + c) * d + (e * f) then x + 2"
    state = State(s)
    res = parse(state)
    print('final ast', res.ast.emit())
    printState(res.state)

testTokens()
