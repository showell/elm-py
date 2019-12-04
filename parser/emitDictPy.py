"""
This script specifically transpiles Dict.elm to Dict.py.
(Actually, it just writes to standard out, and you can
redirect the output to your desired location.)

Right now we hard code the imports to work for Dict.elm.

The goal is to eventually generalize this script, obviously.
"""

import os
import sys

sys.path.append('../src')
sys.path.append('./lib')

import ParseHelper
import ElmParser
import ElmTypes as types

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
AsVar = MatchParam.AsVar
PList = MatchParam.PList
PCons = MatchParam.PCons

""".lstrip()

def emitCode(code):
    state = ParseHelper.State(code)
    res = ElmParser.captureAll(state)

    if res is None:
        raise Exception('could not parse')

    state = res.state

    if state.incomplete():
        ParseHelper.printState(state)
        raise Exception('incomplete!')

    topAst, mainAst = res.ast

    for ast in topAst + mainAst:
        if hasattr(ast, 'emit'):
            print(types.getFinalCode(ast))

if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    fn = path + '/elm/Dict.elm'
    with open(fn) as f:
        code = f.read()

    print(normalPrelude())
    emitCode(code)
