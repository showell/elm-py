import parse
import parseElm
import elmTypes as types

def normalPrelude():
    return """# Dict.py (code generated via elm-py)

from Custom import CustomType

import List
from List import *
from Maybe import *
from Basics import *
from Order import *

from Elm import (
    patternMatch,
    MatchParam,
    )

Any = MatchParam.Any
Val = MatchParam.Val
Var = MatchParam.Var
Variant = MatchParam.Variant
Nested = MatchParam.Nested

""".lstrip()

def emitCode(code):
    state = parse.State(code)
    res = parseElm.captureAll(state)

    if res is None:
        raise Exception('could not parse')

    state = res.state

    if state.incomplete():
        parse.printState(state)
        raise Exception('incomplete!')

    topAst, mainAst = res.ast

    for ast in topAst + mainAst:
        if hasattr(ast, 'emit'):
            print(types.getFinalCode(ast))

if __name__ == '__main__':
    fn = 'Dict.elm'
    with open(fn) as f:
        code = f.read()

    print(normalPrelude())
    emitCode(code)
