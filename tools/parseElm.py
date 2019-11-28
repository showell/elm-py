import types

from parse import (
        bigSkip,
        captureKeywordBlock,
        captureOneOf,
        captureOneOrMore,
        captureStuff,
        captureSubBlock,
        captureUntilKeyword,
        captureUntilKeywordEndsLine,
        captureZeroOrMore,
        grab,
        onlyIf,
        parseAll,
        parseBlock,
        parseKeywordBlock,
        parseMyLevel,
        parseRange,
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
        spaceOptional,
        spaceRequired,
        token,
        transform,
        twoPass,
        )
import parse

# We declare a few things to avoid circular dependencies
def captureExpr(state):
    return doCaptureExpr(state)

# This should obviously eventually go away!
capturePunt = \
    transform(
        types.UnParsed,
        grab(parseAll)
    )

parseModule = parseKeywordBlock('module')

parseDocs = parseRange('{-|', '-}')

parseLineComment = bigSkip(pKeyword('--'), pLine)


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
            captureUntilKeywordEndsLine(
                'then',
                captureExpr
                ),
            twoPass(
                parseMyLevel,
                captureExpr
                ),
            captureSubBlock(
                'else',
                captureExpr
                ),
            )
        )

captureCaseOf = \
    transform(
        types.CaseOf,
        captureStuff(
            skip(pKeyword('case')),
            captureUntilKeywordEndsLine(
                'of',
                capturePunt
                ),
            )
        )

capturePatternDef = \
    transform(
        types.PatternDef,
        captureStuff(
            captureUntilKeywordEndsLine(
                '->',
                capturePunt
                ),
            ),
        )

captureOneCase = \
    transform(
        types.OneCase,
        captureStuff(
            capturePatternDef,
            skip(spaceOptional),
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
            skip(spaceOptional),
            twoPass(
                parseMyLevel,
                captureOneOrMore(captureOneCase),
                )
            )
        )

captureTuple = \
    transform(
        types.Tuple,
        captureStuff(
            skip(pKeyword('(')),
            twoPass(
                pUntilChar(')'),
                capturePunt,
                ),
            skip(pKeyword(')')),
            skip(spaceOptional)
            ),
        )

captureParams = \
    transform(
        types.Params,
        captureZeroOrMore(
            captureOneOf(
                grab(token),
                captureTuple,
                )
            )
        )

captureDef = \
    transform(
        types.Def,
        captureUntilKeywordEndsLine(
            '=',
            captureStuff(
                grab(token),
                skip(spaceOptional),
                captureParams,
                ),
            ),
        )

captureBinding = \
    transform(
        types.Binding,
        captureStuff(
            captureDef,
            skip(spaceOptional),
            twoPass(
                parseMyLevel,
                captureExpr
                ),
            skip(spaceOptional),
            ),
        )

captureLetBindings = \
    captureOneOrMore(captureBinding)

captureLet = \
    transform(
        types.Let,
        captureStuff(
            captureSubBlock('let', captureLetBindings),
            captureSubBlock('in', capturePunt),
            )
        )

captureAnnotation = \
    transform(
        types.Annotation,
        captureStuff(
            onlyIf(
                captureStuff(
                    skip(token),
                    skip(spaceOptional),
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
                grab(token),
                captureLambda,
                captureTuple,
                )
            )
        )

# We call annotations "comments" for now
captureComment = \
    captureOneOf(
        skip(spaceRequired),
        skip(parseLineComment),
        skip(parseDocs),
        captureAnnotation,
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
