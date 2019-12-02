import elmTypes as types

from parse import (
        captureBlock,
        captureInt,
        captureKeywordBlock,
        captureLine,
        captureOneOf,
        captureOneOrMore,
        captureOperator,
        captureRange,
        captureSeq,
        captureStuff,
        captureSubBlock,
        captureTokenLower,
        captureTokenUpper,
        captureUnReservedWord,
        captureUntilKeyword,
        captureZeroOrMore,
        onlyIf,
        parseMyLevel,
        pChar,
        pKeyword,
        printState,
        skip,
        skipManyCaptures,
        transform,
        twoPass,
        )
import parse

# We declare a few things at the top to avoid circular dependencies
def captureExpr(state):
    return doCaptureExpr(state)

def captureTypeSpec(state):
    return doCaptureTypeSpec(state)

def capturePatternExpr(state):
    return doCapturePatternExpr(state)

def captureCallPiece(state):
    return doCaptureCallPiece(state)

def captureParen(fCapture):
    return captureStuff(
        skip(pChar('(')),
        fCapture,
        skip(pChar(')')),
        )

reservedWords = [ 'case', 'of', 'let', 'if', 'then', 'else', '->']

captureElmType = \
    transform(
        types.Token,
        captureTokenUpper(reservedWords)
        )

captureExprVar = \
    transform(
        types.ExprVar,
        captureTokenLower(reservedWords)
        )

captureElmToken = \
    transform(
        types.Token,
        captureTokenLower(reservedWords)
        )

captureElmOperator = \
    captureOperator(
        ['<', '>', '<=', '>=', '==',
            '+', '-', '*', '/']
        )

captureElmInt = \
    transform(
        types.Int,
        captureInt
        )

captureWildCardVar = \
    transform(
        types.WildCardVar,
        captureOperator(['_'])
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
            captureLine,
            )
        )

captureUnit = \
    transform(
        types.Unit,
        captureStuff(
            skip(pChar('(')),
            skip(pChar(')')),
            )
        )

captureModule = \
    transform(
        types.Module,
        captureKeywordBlock('module')
        )

captureImport = \
    transform(
        types.Import,
        captureKeywordBlock('import')
        )

doCaptureTypeSpec = \
    captureOneOf(
        captureParen(
            captureOneOrMore(
                captureOneOf(
                    captureElmToken,
                    captureElmType,
                    )
                )
            ),
        captureElmToken,
        captureElmType,
        )

captureVariantDef = \
    transform(
        types.VariantDef,
        captureStuff(
            captureElmType,
            captureZeroOrMore(
                captureTypeSpec
                )
            )
        )

captureTypeName = \
    captureStuff(
        captureElmType,
        skipManyCaptures(
            captureElmToken
            )
        )

captureTypeDef = \
    transform(
        types.TypeDef,
        captureStuff(
            skip(pKeyword('type')),
            captureTypeName,
            skip(pChar('=')),
            captureVariantDef,
            captureZeroOrMore(
                captureStuff(
                    skip(pChar('|')),
                    captureVariantDef,
                    )
                )
            )
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

captureParenExpr = \
    captureParen(captureExpr)

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
            captureExprVar
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

captureParams = \
    transform(
        types.Params,
        captureZeroOrMore(
            captureOneOf(
                captureUnit,
                captureExprVar,
                captureWildCardVar,
                captureExprTuple,
                )
            )
        )

captureFunctionDef = \
    transform(
        types.FunctionDef,
        captureStuff(
            captureExprVar,
            captureParams,
            )
        )

captureTupleAssign = \
    transform(
        types.TupleAssign,
        captureStuff(
            captureTupleVar,
            skip(pChar('=')),
            twoPass(
                parseMyLevel,
                captureExpr
                ),
            )
        )

captureDef = \
    transform(
        types.Def,
        captureStuff(
            captureFunctionDef,
            skip(pChar('=')),
            )
        )

captureNormalAssign = \
    transform(
        types.NormalAssign,
        captureStuff(
            captureDef,
            twoPass(
                parseMyLevel,
                captureExpr
                ),
            ),
        )

captureBinding = \
    captureOneOf(
        captureNormalAssign,
        captureTupleAssign,
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
                    captureElmToken,
                    skip(pKeyword(':')),
                    ),
                captureBlock,
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

doCaptureCallPiece = \
    captureOneOf(
        captureParen(captureCallPiece),
        captureLambda,
        captureExprTuple,
        captureExprList,
        captureExprVar,
        captureElmInt,
        captureElmType,
        )

captureCall = \
    transform(
        types.Call,
        captureOneOrMore(captureCallPiece),
        )

captureComment = \
    captureOneOf(
        captureLineComment,
        captureDocs,
        )

# I should be smarter about binary operators.
# See https://www.crockford.com/javascript/tdop/tdop.html
# (he implements a Pratt parser, which wouldn't be terribly
# difficult to adapt here...I am just being lazy)
#
# This only captures simple `foo < ...` expressions.

captureSimpleExpr = \
    captureOneOf(
        captureExprVar,
        captureExprTuple,
    )

captureBinOp = \
    transform(
        types.BinOp,
        captureStuff(
            captureSimpleExpr,
            captureElmOperator,
            captureExpr,
            )
        )

captureExprCons = \
    transform(
        types.ExprCons,
        captureStuff(
            captureSimpleExpr,
            captureOperator(['::']),
            captureExpr,
            )
        )

# CASE/PATTERN STUFF

# helpers

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

capturePatternVar = \
    transform(
        types.PatternVar,
        captureTokenLower(reservedWords)
        )

capturePatternType = \
    transform(
        types.PatternType,
        captureTokenUpper(reservedWords)
        )

captureWildCardPattern = \
    transform(
        types.WildCardPattern,
        captureOperator(['_'])
        )

capturePatternAs = \
    transform(
        types.PatternAs,
        captureStuff(
            captureParen(capturePatternExpr),
            skip(pKeyword('as')),
            captureExprVar,
            )
        )

## custom type: SomeType _ x y _

captureCustomTypePattern = \
    transform(
        types.CustomTypePattern,
        captureStuff(
            captureOneOf(
                capturePatternType,
            ),
            captureZeroOrMore(
                captureOneOf(
                    capturePatternAs,
                    captureWildCardPattern,
                    capturePatternVar,
                    capturePatternTuple,
                    captureElmType,
                    )
                )
            )
        )

## list stuff: [], head :: rest

capturePatternListBrackets = \
    transform(
        types.List,
        captureSeq(
            '[',
            ',',
            ']',
            capturePatternExpr,
            )
        )

capturePatternCons = \
    transform(
        types.PatternCons,
        captureStuff(
            captureOneOf(
                captureWildCardPattern,
                capturePatternTuple,
                capturePatternVar,
                captureParen(capturePatternExpr),
                ),
            captureOperator(
                ['::']
                ),
            capturePatternExpr,
            ),
        )

capturePatternList = \
    captureOneOf(
        capturePatternCons,
        capturePatternListBrackets,
        )


## general expression stuff

doCapturePatternExpr = \
    captureStuff(
        skipManyCaptures(captureComment),
        captureOneOf(
            capturePatternAs,
            captureWildCardPattern,
            capturePatternList,
            captureCustomTypePattern,
            capturePatternTuple,
            capturePatternVar,
            )
        )

## pattern matches:  Just _ ->

capturePatternDef = \
    transform(
        types.PatternDef,
        captureStuff(
            capturePatternExpr,
            skip(pKeyword('->')),
            )
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

## case foo of

captureCaseOf = \
    transform(
        types.CaseOf,
        captureStuff(
            skip(pKeyword('case')),
            captureExpr,
            skip(pKeyword('of')),
            )
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

# EXPRESSIONS

doCaptureExpr = \
    captureStuff(
        skipManyCaptures(captureComment),
        captureOneOf(
            captureUnit,
            captureParenExpr,
            captureBinOp,
            captureExprCons,
            captureLet,
            captureIf,
            captureCase,
            captureCall,
            captureLambda,
            )
        )

# TOP LEVEL STRUCTURE

captureTopOfFile = \
    captureOneOrMore(
        captureOneOf(
            captureModule,
            captureImport,
            captureComment,
            captureTypeDef,
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

    if state.incomplete():
        printState(state)
        raise Exception('incomplete!')

    print('TOP\n\n')
    for ast in topAst:
        print('==')
        print(ast)

    print('\n\n\nMAIN\n\n\n')
    for ast in mainAst:
        print('==')
        print(ast)

if __name__ == '__main__':
    fn = 'Dict.elm'
    with open(fn) as f:
        code = f.read()
    parseCode(code)
