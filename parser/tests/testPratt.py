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

class VarToken:
    lbp = 100

    def __init__(self, token):
        self.token = token

    def __str__(self):
        return self.token

    def nud(self, token, state):
        """
        # This is sorta broken--we parse over any arguments, but otherwise
        # ignore them
        if token and hasattr(token, 'nud'):
            (right, token, state) = expression(token, state, self.lbp-1)
        """
        self.ast = ElmTypes.ExprVar(self.token)
        return (self, token, state)

class ParenToken:
    lbp = 200

    def __init__(self, token):
        pass

    def __str__(self):
        return str(self.ast)

    def nud(self, token, state):
        right, token, state = expression(token, state, 0)
        self.ast = ElmTypes.Paren(right.ast)

        state = pChar(')')(state)
        if state is None:
            raise 'foo'

        res = tokenize(state)
        if res is None:
            token = None
            state = None
        else:
            token = res.ast
            state = res.state

        return (self, token, state)

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

    def led(self, left, token, state):
        (right, token, state) = expression(token, state, self.lbp)
        self.ast = ElmTypes.BinOp([left.ast, self.token, right.ast])
        return (self, token, state)

def expression(token, state, rbp=0):
    # This code is adapted from this article:
    #
    # http://effbot.org/zone/simple-top-down-parsing.htm
    t = token
    res = tokenize(state)
    if res is None:
        return t.nud(None, state)

    token = res.ast
    state = res.state
    (left, token, state) = t.nud(token, state)

    while token and rbp < token.lbp:
        t = token
        res = tokenize(state)
        if res is None:
            print('break')
            break
        token = res.ast
        state = res.state
        (left, token, state) = t.led(left, token, state)

    return (left, token, state)

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
    res = tokenize(state)
    (left, token, state) = expression(res.ast, res.state)

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
