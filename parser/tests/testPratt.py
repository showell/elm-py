import sys
sys.path.append('../lib')
sys.path.append('../../src')

from ParseHelper import (
    captureOneOf,
    captureOperator,
    captureTokenLower,
    grab,
    pChar,
    State,
    transform,
)

import ElmParser

class Var:
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return self.token

class VarToken:
    lbp = 100

    def __init__(self, token):
        self.token = token

    def __str__(self):
        return self.token

    def nud(self, token, state):
        if token and hasattr(token, 'nud'):
            (right, token, state) = expression(token, state, self.lbp-1)
        self.ast = Var(self.token)
        return (self, token, state)

class ParenToken:
    lbp = 200

    def __init__(self, token):
        pass

    def __str__(self):
        return str(self.ast)

    def nud(self, token, state):
        right, token, state = expression(token, state, 0)
        self.ast = right

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

class Op:
    def __init__(self, first, op, second):
        self.first = first
        self.op = op
        self.second = second

    def __str__(self):
        return str((self.op, str(self.first), str(self.second)))

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
        self.ast = Op(left, self.token, right)
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

def testTokens():
    s = "a x y * (b + c) * d + (e * f)"
    state = State(s)

    res = tokenize(state)
    (ast, token, state) = expression(res.ast, res.state)
    print('final ast', str(ast.ast))

testTokens()
