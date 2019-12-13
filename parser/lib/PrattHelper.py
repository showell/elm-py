import ParseHelper

"""
This is a work in progress, and I haven't integrated it
into the actual Elm parser yet.
"""

class Pratt:
    def __init__(self, token, state, priorState, tokenizer):
        self.token = token
        self.state = state
        self.priorState = priorState
        self.tokenizer = tokenizer

    def tokenize(self):
        priorState = self.state
        res = self.tokenizer(self.state)
        if res is None:
            token = None
            state = self.state
        else:
            token = res.ast
            state = res.state
        return Pratt(token, state, priorState, self.tokenizer)

    def advance(self, parse):
        state = parse(self.state)
        if state is None:
            raise 'foo'
        return Pratt(None, state, None, self.tokenizer).tokenize()

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

def parse(state, tokenizer):
    pratt = Pratt(None, state, None, tokenizer).tokenize()
    (left, pratt) = expression(pratt)

    return ParseHelper.Result(pratt.priorState, left.ast)

