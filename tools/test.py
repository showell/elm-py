import parseElm
import parse
import types

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

    if type(ast) == types.UnParsed:
        raise Exception('did not really parse')

    print(ast)


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

succeed(parseElm.captureOneCase(
    parse.State("""
    foo bar ->
        hello
        world

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


