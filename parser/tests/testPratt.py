import sys
sys.path.append('../lib')
sys.path.append('../../src')

from ParseHelper import (
    captureOneOf,
    captureOperator,
    captureTokenLower,
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
    lbp = 0

    def __init__(self, token):
        self.token = token

    def __str__(self):
        return self.token

    def nud(self, token, state):
        self.ast = Var(self.token)
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
        return str(self.ast)

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
        return t.nud(token, state)

    token = res.ast
    state = res.state
    (left, token, state) = t.nud(token, state)

    while rbp < token.lbp:
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

tokenize = \
    captureOneOf(
        var,
        op,
        )

def testTokens():
    s = "a * b + c * d + e"
    state = State(s)

    res = tokenize(state)
    (ast, token, state) = expression(res.ast, res.state)
    print('final ast', str(ast.ast))

testTokens()
