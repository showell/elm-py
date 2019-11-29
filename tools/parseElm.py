import types

def error(*args):
    raise Exception('could not parse')

types.UnParsed = error


from parse import (
        captureKeywordBlock,
        captureOneOf,
        captureOneOrMore,
        captureRange,
        captureSeq,
        captureStuff,
        captureSubBlock,
        captureUnReservedWord,
        captureUntilKeyword,
        captureUntilKeywordEndsLine,
        captureZeroOrMore,
        grab,
        onlyIf,
        parseAll,
        parseBlock,
        parseKeywordBlock,
        parseMyLevel,
        parseOperator,
        parseSameLine,
        peek,
        pChar,
        pKeyword,
        pLine,
        printState,
        pUntil,
        pUntilChar,
        pUntilLineEndsWith,
        skip,
        skipManyCaptures,
        spaceRequired,
        token,
        transform,
        twoPass,
        )
import parse

# We declare a few things at the top to avoid circular dependencies
def captureExpr(state):
    return doCaptureExpr(state)

def capturePatternExpr(state):
    return doCapturePatternExpr(state)

# This should obviously eventually go away!
capturePunt = \
    transform(
        types.UnParsed,
        grab(parseAll)
    )

parseModule = parseKeywordBlock('module')

captureElmToken = \
    captureUnReservedWord(
        [ 'case', 'of', 'let', 'if', 'then', 'else', '->']
        )

captureElmOperator = \
    captureStuff(
        grab(
            parseOperator(
                ['<', '>', '<=', '>=', '==',
                    '+', '-', '*', '/']
                )
            )
        )

capturePatternOperator = \
    captureStuff(
        grab(
            parseOperator(
                ['::']
                )
            )
        )

captureDocs = \
    transform(
        types.Comment,
        captureRange(
            '{-|',
            '-}',
            ),
        )


captureLineComment = \
    transform(
        types.Comment,
        captureStuff(
            skip(pKeyword('--')),
            grab(pLine)
            )
        )

captureImport = \
    transform(
        types.Import,
        captureKeywordBlock('import')
        )

captureType = \
    transform(
        types.Type,
        captureKeywordBlock('type')
        )

captureIf = \
    transform(
        types.If,
        captureStuff(
            skip(pKeyword('if')),
            captureExpr,
            skip(pKeyword('then')),
            captureExpr,
            skip(pKeyword('else')),
            captureExpr
            )
        )

captureCaseOf = \
    transform(
        types.CaseOf,
        captureStuff(
            skip(pKeyword('case')),
            captureUntilKeywordEndsLine(
                'of',
                captureExpr,
                ),
            )
        )

capturePattern = \
    captureOneOf(
        capturePatternExpr,
        )

capturePatternDef = \
    transform(
        types.PatternDef,
        captureStuff(
            captureUntilKeywordEndsLine(
                '->',
                capturePattern
                ),
            ),
        )

captureOneCase = \
    transform(
        types.OneCase,
        captureStuff(
            capturePatternDef,
            twoPass(
                parseMyLevel,
                captureExpr,
                ),
            ),
        )

captureCase = \
    transform(
        types.Case,
        captureStuff(
            captureCaseOf,
            twoPass(
                parseMyLevel,
                captureOneOrMore(captureOneCase),
                )
            )
        )

captureExprTuple = \
    transform(
        types.Tuple,
        captureSeq(
            '(',
            ',',
            ')',
            captureExpr,
            )
        )

captureTupleVar = \
    transform(
        types.TupleVar,
        captureSeq(
            '(',
            ',',
            ')',
            grab(token),
            )
        )

capturePatternTuple = \
    transform(
        types.Tuple,
        captureSeq(
            '(',
            ',',
            ')',
            capturePatternExpr,
            )
        )

captureExprList = \
    transform(
        types.List,
        captureSeq(
            '[',
            ',',
            ']',
            captureExpr,
            )
        )

capturePatternList = \
    transform(
        types.List,
        captureSeq(
            '[',
            ',',
            ']',
            capturePatternExpr,
            )
        )

captureParams = \
    transform(
        types.Params,
        captureZeroOrMore(
            captureOneOf(
                captureElmToken,
                captureExprTuple,
                )
            )
        )

captureFunctionDef = \
    transform(
        types.FunctionDef,
        captureStuff(
            captureElmToken,
            captureParams,
            )
        )

captureDef = \
    transform(
        types.Def,
        captureUntilKeywordEndsLine(
            '=',
            captureOneOf(
                captureTupleVar,
                captureFunctionDef,
                ),
            ),
        )

captureBinding = \
    transform(
        types.Binding,
        captureStuff(
            captureDef,
            twoPass(
                parseMyLevel,
                captureExpr
                ),
            ),
        )

captureLetBindings = \
    captureOneOrMore(captureBinding)

captureLet = \
    transform(
        types.Let,
        captureStuff(
            captureSubBlock('let', captureLetBindings),
            captureSubBlock('in', captureExpr),
            )
        )

captureAnnotation = \
    transform(
        types.Annotation,
        captureStuff(
            onlyIf(
                captureStuff(
                    skip(token),
                    skip(pKeyword(':')),
                    ),
                grab(parseBlock),
                ),
            ),
        )

captureLambda = \
    transform(
        types.Lambda,
        captureStuff(
            skip(pChar('\\')),
            captureUntilKeyword(
                '->',
                captureParams
                ),
            captureExpr,
            )
        )

captureCall = \
    transform(
        types.Call,
        captureOneOrMore(
            captureOneOf(
                captureLambda,
                captureExprTuple,
                captureExprList,
                captureElmOperator,
                captureElmToken,
                )
            )
        )

captureComment = \
    captureOneOf(
        skip(spaceRequired),
        captureLineComment,
        captureDocs,
        )

captureCustomTypePattern = \
    transform(
        types.CustomTypePattern,
        captureStuff(
            captureOneOf(
                captureElmToken,
                capturePatternTuple,
            ),
            captureZeroOrMore(
                captureOneOf(
                    capturePatternTuple,
                    capturePatternList,
                    capturePatternOperator,
                    captureElmToken,
                    )
                )
            )
        )

doCaptureExpr = \
    captureStuff(
        skipManyCaptures(captureComment),
        captureOneOf(
            captureLet,
            captureIf,
            captureCase,
            captureCall,
            captureLambda,
            capturePunt,
            )
        )

doCapturePatternExpr = \
    captureStuff(
        skipManyCaptures(captureComment),
        captureOneOf(
            capturePatternList,
            captureCustomTypePattern,
            capturePunt,
            )
        )

captureTopOfFile = \
    captureOneOrMore(
        captureOneOf(
            skip(parseModule),
            captureImport,
            captureComment,
            captureType,
            )
        )

captureMainCode = \
    captureOneOrMore(
        captureOneOf(
            captureComment,
            captureAnnotation,
            captureBinding,
            )
        )

captureAll = \
    captureStuff(
        captureTopOfFile,
        captureMainCode,
        )

def parseCode(code):
    state = parse.State(code)
    res = captureAll(state)

    if res is None:
        raise Exception('could not parse')

    state = res.state
    topAst, mainAst = res.ast

    print('TOP\n\n')
    for ast in topAst:
        print('==')
        print(ast)

    print('\n\n\nMAIN\n\n\n')
    for ast in mainAst:
        print('==')
        print(ast)

    printState(state)

if __name__ == '__main__':
    fn = 'Dict.elm'
    with open(fn) as f:
        code = f.read()
    parseCode(code)
