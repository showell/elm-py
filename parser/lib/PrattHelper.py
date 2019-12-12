import ParseHelper

"""
This is a work in progress, and I haven't integrated it
into the actual Elm parser yet.
"""

class Pratt:
    def __init__(self, token, state, tokenizer):
        self.token = token
        self.state = state
        self.tokenizer = tokenizer

    def tokenize(self):
        res = self.tokenizer(self.state)
        if res is None:
            token = None
            state = self.state
        else:
            token = res.ast
            state = res.state
        return Pratt(token, state, self.tokenizer)

    def advance(self, parse):
        state = parse(self.state)
        if state is None:
            raise 'foo'
        return Pratt(None, state, self.tokenizer).tokenize()

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
    pratt = Pratt(None, state, tokenizer).tokenize()
    (left, pratt) = expression(pratt)

    # Since Pratt parsing always looks ahead one token, we
    # cheat here to reset the state for any integration with
    # "outer" parsers.  The ParseHelper module remembers the
    # last valid state.  This is still skipping one too many
    # tokens, though, so I need a better way to keep prior
    # states.
    return ParseHelper.Result(ParseHelper.lastState, left.ast)

