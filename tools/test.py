import types

def error(*args):
    raise Exception('could not parse')

types.UnParsed = error

import parseElm
import parse

def succeed(res):
    if res is None:
        raise Exception('parse failure')
    state = res.state
    ast = res.ast
    (s, i) = state.position()
    if i != len(s):
        parse.printState(state)
        raise Exception('partial parse')
    print("\n---")

    print(ast)

def assertIndent(s, i, expected):
    assert parse.indentLevel(s, i) == expected

assertIndent('', 0, 0)
assertIndent('\n', 0, 0)
assertIndent('\n', 1, 0)
assertIndent('  fred', 0, 2)
assertIndent(' \n  fred', 3, 2)
assertIndent(' \n  fred', 4, 2)
assertIndent(' \n  fred', 5, 2)

succeed(parseElm.skip(parseElm.parseModule)(
    parse.State("""
    module foo exposing (
        foo, bar
        )
    """)))

succeed(parseElm.captureDocs(
    parse.State("""
    {-|
       bla bla bla
    -}
    """)))

succeed(parseElm.captureImport(
    parse.State("""
import foo exposing (
    foo, bar
    )
    """)))

succeed(parseElm.captureType(
    parse.State("""
    type Value =
        = Int
        | String
    """)))

succeed(parseElm.captureDef(
    parse.State("""
    x =
    """)))

succeed(parseElm.captureBinding(
    parse.State("""
    x =
        5""")))

succeed(parseElm.captureExpr(
    parse.State("""
    foo bar
        """)))

succeed(parseElm.captureOneCase(
    parse.State("""
    foo ->
        let
            x =
                2
        in
        x

        """)))

succeed(parseElm.captureCaseOf(
    parse.State("""
    case fred of
        """)))

succeed(parseElm.captureCase(
    parse.State("""
    case fred of
        foo ->
            f foo
                bla

        bar ->
            f bar
                bla
        """)))

succeed(parseElm.captureLet(
    parse.State("""
    let
        foo a b c =
            one

        bar x y z =
            two
    in
    foo bar""")))

succeed(parseElm.captureIf(
    parse.State("""
    if cond then
        if cond2 then
            a
        else
            b

    else
        false_val
            stuff
        """)))

# tuples are dumb now
succeed(parseElm.captureTuple(
    parse.State("""
        ( foo, bar )
        """)))

succeed(parseElm.captureExpr(
    parse.State("""
        add 5 7
        """)))

succeed(parseElm.captureAnnotation(
    parse.State("""
foo : List String  ->
   String ->
   Int""")))

succeed(parseElm.captureLambda(
    parse.State("""
    \\a b -> c
    """)))


succeed(parseElm.captureLambda(
    parse.State("""
    \\x y ->
        if b then
            t
        else
            f
    """)))

# tuples in lambda params
succeed(parseElm.captureExpr(
    parse.State("""
    \\(x,y) -> a
    """)))


# lambda in expressions
succeed(parseElm.captureExpr(
    parse.State("""
    map2 ( \\x y -> 5 ) lst
    """)))


succeed(parseElm.capturePatternList(
    parse.State("""
    [ a, 5, c ]
    """)))


succeed(parseElm.capturePatternDef(
    parse.State("""
    [x, y] ->
    """)))

succeed(parseElm.capturePatternExpr(
    parse.State("""
    []
    """)))

succeed(parseElm.captureOneCase(
    parse.State("""
    foo bar ->
        5
        """)))

succeed(parseElm.captureOneCase(
    parse.State("""
    foo (x y) ->
        5
        """)))

succeed(parseElm.captureExpr(
    parse.State("""
    x < y
        """)))

succeed(parseElm.captureOneCase(
    parse.State("""
    head :: rest ->
        5
        """)))


succeed(parseElm.captureOneCase(
    parse.State("""
    (first, second) :: rest ->
        5
        """)))


