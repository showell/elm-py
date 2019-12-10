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
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return self.token

    def nud(self, state):
        return (Var(self.token), state)

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

    def __str__(self):
        return self.token

    def led(self, state, left):
        res = tokenize(state)
        token = res.ast
        (right, state) = expression(token, state)
        ast = Op(left, self.token, right)
        return (ast, state)

def expression(token, state):
    t = token
    res = tokenize(state)
    token = res.ast
    state = res.state
    (left, state) = t.nud(state)

    while True:
        t = token
        res = tokenize(state)
        if res is None:
            break
        (left, state) = t.led(state, left)
        break

    return (left, state)


var = \
    transform(
        VarToken,
        captureTokenLower(ElmParser.reservedWords)
        )

op = \
    transform(
        OpToken,
        captureOperator(['<']),
    )

def tokenize(state):
    res = captureOneOf(
        var,
        op
    )(state)
    return res

def testTokens():
    s = "x < y"
    state = State(s)

    res = tokenize(state)
    (ast, state) = expression(res.ast, res.state)
    print('final ast', str(ast))

testTokens()
