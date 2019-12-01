import parse
import parseElm
import types

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

    emitCode(code)
