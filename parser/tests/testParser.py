"""
This has a lot of ad-hoc tests for the Elm parser.

If you are having trouble parsing an Elm file, a good strategy
is to make a small test case for a particular section in the file
that is tripping up the parser.

This file definitely needs improvement!
"""

import sys
sys.path.append('../lib')
sys.path.append('../../src')

import ElmTypes as types
import ElmParser
import ParseHelper as parse

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
    print('pass\n')

def assertIndent(s, i, expected):
    assert parse.indentLevel(s, i) == expected

def testIndents():
    assertIndent('', 0, 0)
    assertIndent('\n', 0, 0)
    assertIndent('\n', 1, 0)
    assertIndent('  fred', 0, 2)
    assertIndent(' \n  fred', 3, 2)
    assertIndent(' \n  fred', 4, 2)
    assertIndent(' \n  fred', 5, 2)

def testParse():
    succeed(ElmParser.captureModule,
        """
        module foo exposing (
            foo, bar
            )
        """)

    succeed(ElmParser.captureDocs,
        """
        {-|
           bla bla bla
        -}
        """)

    succeed(ElmParser.captureImport,
        """
    import foo exposing ,
        foo, bar
        )
        """)

    succeed(ElmParser.captureTypeDef,
        """
        type Value
            = Int
            | String
        """)

    succeed(ElmParser.captureTypeDef,
        """
        type Foo a b
            = Int a Bar (Baz c d)
            | String b
        """)

    succeed(ElmParser.captureBinding,
        """
        x =
            bla""")

    succeed(ElmParser.captureExpr,
        """
        foo bar
            """)

    succeed(ElmParser.captureLet,
        """
        let
            foo a b c =
                one

            bar x y z =
                two
        in
        foo bar""")

    succeed(ElmParser.captureOneCase,
        """
        foo ->
            let
                x =
                    bar
            in
            x

            """)

    succeed(ElmParser.captureCase,
        """
        case fred of
            foo ->
                f foo
                    bla

            bar ->
                f bar
                    bla
            """)

    succeed(ElmParser.captureIf,
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
    succeed(ElmParser.captureExprTuple,
        """
            ( foo, bar )
            """)

    succeed(ElmParser.captureExpr,
        """
            add a b
            """)

    succeed(ElmParser.captureAnnotation,
        """
    foo : List String  ->
       String ->
       Int""")

    succeed(ElmParser.captureUnit, '()')
    succeed(ElmParser.captureUnit, '(  )')

    succeed(ElmParser.captureLambda,
        """
        \\() -> a (b c)
        """)


    succeed(ElmParser.captureLambda,
        """
        \\a b -> c
        """)


    succeed(ElmParser.captureLambda,
        """
        \\x y ->
            if b then
                t
            else
                f
        """)

    # tuples in lambda params
    succeed(ElmParser.captureExpr,
        """
        \\(x,y) -> a
        """)


    # lambda in expressions
    succeed(ElmParser.captureExpr,
        """
        map2 ( \\x y -> a ) lst
        """)


    succeed(ElmParser.capturePatternListBrackets,
        """
        [ a, b, c ]
        """)


    succeed(ElmParser.capturePatternDef,
        """
        [x, y] ->
        """)

    succeed(ElmParser.capturePatternExpr,
        """
        []
        """)

    succeed(ElmParser.capturePatternCons,
        """
        foo :: rest
            """)

    succeed(ElmParser.captureOneCase,
        """
        foo :: rest ->
            baz
            """)

    succeed(ElmParser.captureOneCase,
        """
        Foo bar ->
            baz
            """)

    succeed(ElmParser.captureOneCase,
        """
        Foo (x, y) ->
            a
            """)

    succeed(ElmParser.captureExpr,
        """
        x < y
            """)

    succeed(ElmParser.captureOneCase,
        """
        head :: rest ->
            a
            """)


    succeed(ElmParser.capturePatternCons,
        """
        (first, second) :: rest""")

    succeed(ElmParser.captureOneCase,
        """
        (first, second) :: rest ->
            a
            """)

    succeed(ElmParser.captureIf,
        """
        if foo then a else b
            """)


    succeed(ElmParser.captureExpr,
        """
        n+m
            """)


    succeed(ElmParser.captureTupleVar,
        """
        (x, y)
            """)

    succeed(ElmParser.captureBinding,
        """
        (x, y) =
            foo
            """)


    succeed(ElmParser.captureCall,
        """
        foo (bar x) y
            """)


    succeed(ElmParser.captureBinding,
        """
        x =
            foldr (\key value list -> a :: b) [] dict
            """)


def testBlocks():
    s = """
    let
        x =
            if cond then
                a

            else
                b
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
        a
    else
        b
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
            a
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

def testEmit():
    print("\n\n\n---- EMIT ---\n\n")
    code = """
        v =
            \\x -> if x then a else b
        """
    state = parse.State(code)
    res = ElmParser.captureBinding(state)
    print(types.getFinalCode(res.ast))

    code = """
        v =
            foo (\\x -> if x then a else b) z
        """
    state = parse.State(code)
    res = ElmParser.captureBinding(state)
    print(types.getFinalCode(res.ast))

    code = """
        (x, y) = foo bar
        """
    state = parse.State(code)
    res = ElmParser.captureBinding(state)
    print(types.getFinalCode(res.ast))

    code = """
        foo a (b, c) d = yo a b c d
        """
    state = parse.State(code)
    res = ElmParser.captureBinding(state)
    print(types.getFinalCode(res.ast))

    code = """
        x =
            case foo of
                Coords x y ->
                    (x, y)

                _ ->
                    foo

        """
    state = parse.State(code)
    res = ElmParser.captureBinding(state)
    print(types.getFinalCode(res.ast))

    code = """
        x =
            case foo of
                Coords x y ->
                    (x, y)

                x ->
                    foo

        """
    state = parse.State(code)
    res = ElmParser.captureBinding(state)
    print(types.getFinalCode(res.ast))

    code = """
        x =
            case foo of
                Foo a ((Bar x y) as bar) ->
                    whatever

        """
    state = parse.State(code)
    res = ElmParser.captureBinding(state)
    print(types.getFinalCode(res.ast))


testIndents()
testParse()
testBlocks()
testEmit()
print('\n\ncompleted tests')
