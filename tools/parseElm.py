import types

from parse import (
        bigSkip,
        captureKeywordBlock,
        captureOneOf,
        captureOneOrMore,
        captureSeq,
        captureSubBlock,
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

parseImport = parseKeywordBlock('import')

captureType = \
    transform(
        types.Type,
        captureKeywordBlock('type')
        )

captureIf = \
    transform(
        types.If,
        captureSeq(
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
        captureSeq(
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
        captureSeq(
            captureUntilKeywordEndsLine(
                '->',
                capturePunt
                ),
            ),
        )

captureOneCase = \
    transform(
        types.OneCase,
        captureSeq(
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
        captureSeq(
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
        captureSeq(
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
            captureSeq(
                grab(token),
                skip(spaceOptional),
                captureParams,
                ),
            ),
        )

captureBinding = \
    transform(
        types.Binding,
        captureSeq(
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
        captureSeq(
            captureSubBlock('let', captureLetBindings),
            captureSubBlock('in', capturePunt),
            )
        )

captureAnnotation = \
    transform(
        types.Annotation,
        captureSeq(
            onlyIf(
                captureSeq(
                    skip(token),
                    skip(spaceOptional),
                    skip(pKeyword(':')),
                    ),
                grab(parseBlock),
                ),
            ),
        )

captureNoise = \
    captureOneOf(
        skip(spaceRequired),
        skip(parseModule),
        skip(parseImport),
        skip(parseLineComment),
        skip(parseDocs),
        captureAnnotation,
        )

skipNoise = skipManyCaptures(captureNoise)

captureCall = \
    transform(
        types.Call,
        captureOneOrMore(
            grab(token),
            )
        )

doCaptureExpr = \
    captureSeq(
        skipNoise,
        captureOneOf(
            captureLet,
            captureIf,
            captureCase,
            captureCall,
            capturePunt,
            )
        )

captureStuff = \
    captureOneOf(
        captureNoise,
        captureType,
        captureBinding,
        )

captureAll = \
    captureSeq(
        skipNoise,
        captureOneOrMore(captureStuff)
        )

def parseCode(code):
    state = parse.State(code)
    res = captureAll(state)

    if res is None:
        raise Exception('could not parse')

    state = res.state

    for ast in res.ast:
        print('==')
        print(ast)

    printState(state)

if __name__ == '__main__':
    fn = 'Dict.elm'
    with open(fn) as f:
        code = f.read()
    parseCode(code)
