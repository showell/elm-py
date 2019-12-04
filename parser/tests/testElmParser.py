import sys
sys.path.append('../lib')
sys.path.append('../../src')

from ElmParser import captureAll
import ParseHelper

def parseCode(code):
    state = ParseHelper.State(code)
    res = captureAll(state)

    if res is None:
        raise Exception('could not parse')

    state = res.state

    if state.incomplete():
        printState(state)
        raise Exception('incomplete!')

    # printResults(res)
    print('pass!')

def printResults(res):
    topAst, mainAst = res.ast

    print('TOP\n\n')
    for ast in topAst:
        print('==')
        print(ast)

    print('\n\n\nMAIN\n\n\n')
    for ast in mainAst:
        print('==')
        print(ast)

if __name__ == '__main__':
    fn = '../elm/Dict.elm'
    with open(fn) as f:
        code = f.read()
    parseCode(code)
