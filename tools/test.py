import types
import parseElm
import parse

def succeed(fCapture, s):
    state = parse.State(s)
    res = fCapture(state)

    if res is None:
        print('\n\n------------\n')
        parse.printState(state)
        raise Exception('parse failure')

    state = res.state
    ast = res.ast
    (s, i) = state.position()
    if i != len(s):
        print('\n\n------------\n')
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

succeed(parseElm.captureModule,
    """
    module foo exposing (
        foo, bar
        )
    """)

succeed(parseElm.captureDocs,
    """
    {-|
       bla bla bla
    -}
    """)

succeed(parseElm.captureImport,
    """
import foo exposing ,
    foo, bar
    )
    """)

succeed(parseElm.captureType,
    """
    type Value =
        = Int
        | String
    """)

succeed(parseElm.captureDef,
    """
    x =
    """)

succeed(parseElm.captureBinding,
    """
    x =
        5""")

succeed(parseElm.captureExpr,
    """
    foo bar
        """)

succeed(parseElm.captureLet,
    """
    let
        foo a b c =
            one

        bar x y z =
            two
    in
    foo bar""")

succeed(parseElm.captureOneCase,
    """
    foo ->
        let
            x =
                2
        in
        x

        """)

succeed(parseElm.captureCaseOf,
    """
    case fred of
        """)

succeed(parseElm.captureCase,
    """
    case fred of
        foo ->
            f foo
                bla

        bar ->
            f bar
                bla
        """)

succeed(parseElm.captureIf,
    """
    if cond then
        if cond2 then
            a
        else
            b

    else
        false_val
            stuff
        """)

# tuples are dumb now
succeed(parseElm.captureExprTuple,
    """
        ( foo, bar )
        """)

succeed(parseElm.captureExpr,
    """
        add 5 7
        """)

succeed(parseElm.captureAnnotation,
    """
foo : List String  ->
   String ->
   Int""")

succeed(parseElm.captureUnit, '()')
succeed(parseElm.captureUnit, '(  )')

succeed(parseElm.captureLambda,
    """
    \\() -> a (b c)
    """)


succeed(parseElm.captureLambda,
    """
    \\a b -> c
    """)


succeed(parseElm.captureLambda,
    """
    \\x y ->
        if b then
            t
        else
            f
    """)

# tuples in lambda params
succeed(parseElm.captureExpr,
    """
    \\(x,y) -> a
    """)


# lambda in expressions
succeed(parseElm.captureExpr,
    """
    map2 ( \\x y -> 5 ) lst
    """)


succeed(parseElm.capturePatternList,
    """
    [ a, 5, c ]
    """)


succeed(parseElm.capturePatternDef,
    """
    [x, y] ->
    """)

succeed(parseElm.capturePatternExpr,
    """
    []
    """)

succeed(parseElm.captureOneCase,
    """
    foo bar ->
        5
        """)

succeed(parseElm.captureOneCase,
    """
    foo (x y) ->
        5
        """)

succeed(parseElm.captureExpr,
    """
    x < y
        """)

succeed(parseElm.captureOneCase,
    """
    head :: rest ->
        5
        """)


succeed(parseElm.captureOneCase,
    """
    (first, second) :: rest ->
        5
        """)

succeed(parseElm.captureIf,
    """
    if foo then 1 else 2
        """)


succeed(parseElm.captureExpr,
    """
    n+1
        """)


succeed(parseElm.captureTupleVar,
    """
    (x, y)
        """)

succeed(parseElm.captureBinding,
    """
    (x, y) =
        foo
        """)


def testBlocks():
    s = """
    let
        x =
            if cond then
                1

            else
                2
        y =
            bla
    in foo
        """
    state = parse.State(s)
    state = parse.spaceOptional(state)
    assert parse.peek(state, "let")
    assert parse.peek(
        parse.parseBlock(state),
        "in foo")

    state = parse.pKeyword('let')(state)
    state = parse.spaceOptional(state)
    assert parse.peek(state, "x =")
    assert parse.peek(
        parse.parseBlock(state),
        "y =")

    s = """
    else if cond then
        5
    else
        7
        """
    state = parse.State(s)
    state = parse.spaceOptional(state)
    assert parse.peek(state, 'else')
    state = parse.pKeyword('else')(state)
    state = parse.spaceOptional(state)
    assert parse.peek(state, 'if cond')
    assert parse.peek(
        parse.parseBlock(state),
        'else')

    s = """
        let x =
            5
        in foo
        """
    state = parse.State(s)
    state = parse.spaceOptional(state)
    state = parse.pKeyword('let')(state)
    state = parse.spaceOptional(state)
    assert parse.peek(state, 'x =')
    assert parse.peek(
        parse.parseBlock(state),
        'in foo')

testBlocks()
