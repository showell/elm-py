"""
This is an incomplete parser for Elm code.

It currently can parser Dict.elm from the core library,
including the following constructs:

    custom type definitions
    if/else
    let/in
    case/of (with basic pattern matching for lists and
        custom types)
    basic operators
    ints
    lambdas

It parses just enough to skip over certain things:

    annotations
    module statement
    imports
    docs/comments
"""

import ElmTypes as types

from ParseHelper import (
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

# We declare a few things at the top to avoid circular dependencies
def captureExpr(state):
    return doCaptureExpr(state)

def captureTypeSpec(state):
    return doCaptureTypeSpec(state)

def capturePatternExpr(state):
    return doCapturePatternExpr(state)

def captureCallPiece(state):
    return doCaptureCallPiece(state)

def captureCustomTypePattern(state):
    return doCaptureCustomTypePattern(state)

def captureSimpleExpr(state):
    return doCaptureSimpleExpr(state)

def captureParen(fCapture):
    return captureStuff(
        skip(pChar('(')),
        fCapture,
        skip(pChar(')')),
        )

reservedWords = [ 'case', 'of', 'let', 'if', 'then', 'else', '->']

# Docs/comments

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

captureComment = \
    captureOneOf(
        captureLineComment,
        captureDocs,
        )

# top of file stuff

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

# Simple types

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

captureUnit = \
    transform(
        types.Unit,
        captureStuff(
            skip(pChar('(')),
            skip(pChar(')')),
            )
        )

# tuples (in expressions)

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

# lists (in expressions)

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

captureExprCons = \
    transform(
        types.ExprCons,
        captureStuff(
            captureSimpleExpr,
            captureOperator(['::']),
            captureExpr,
            )
        )

# expression helpers

captureParenExpr = \
    captureParen(captureExpr)

doCaptureSimpleExpr = \
    captureOneOf(
        captureExprVar,
        captureExprTuple,
    )

# operators

captureElmOperator = \
    captureOperator(
        ['<', '>', '<=', '>=', '==',
            '+', '-', '*', '/']
        )

# I should be smarter about binary operators.
# See https://www.crockford.com/javascript/tdop/tdop.html
# (he implements a Pratt parser, which wouldn't be terribly
# difficult to adapt here...I am just being lazy)
#
# This only captures simple `foo < ...` expressions.

captureBinOp = \
    transform(
        types.BinOp,
        captureStuff(
            captureSimpleExpr,
            captureElmOperator,
            captureExpr,
            )
        )

# value assignments

captureValueAssign = \
    transform(
        types.ValueAssign,
        captureStuff(
            captureExprVar,
            skip(pChar('=')),
            twoPass(
                parseMyLevel,
                captureExpr
                ),
            )
        )

# tuple assignments

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

# function definitions

captureParams = \
    transform(
        types.Params,
        captureOneOrMore(
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

captureDef = \
    transform(
        types.Def,
        captureStuff(
            captureFunctionDef,
            skip(pChar('=')),
            )
        )

captureFunctionAssign = \
    transform(
        types.FunctionAssign,
        captureStuff(
            captureDef,
            twoPass(
                parseMyLevel,
                captureExpr
                ),
            ),
        )

# general bindings

captureBinding = \
    captureOneOf(
        captureValueAssign,
        captureFunctionAssign,
        captureTupleAssign,
    )


# lambdas

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

# function calls

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

# annotations

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

# type definitions

doCaptureTypeSpec = \
    captureOneOf(
        captureParen(
            captureOneOrMore(
                captureTypeSpec,
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
                    skipManyCaptures(captureLineComment),
                    skip(pChar('|')),
                    captureVariantDef,
                    )
                )
            )
        )


# Lets

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

# CASE/PATTERN STUFF

# leaf nodes

capturePatternVar = \
    transform(
        types.PatternVar,
        captureTokenLower(reservedWords)
        )

captureWildCardPattern = \
    transform(
        types.WildCardPattern,
        captureOperator(['_'])
        )

capturePatternType = \
    transform(
        types.PatternType,
        captureTokenUpper(reservedWords)
        )

captureCustomTypeVal = \
    transform(
        types.CustomTypeVal,
        captureElmType,
        )

# Tuples/nesting

capturePatternTuple = \
    transform(
        types.PatternTuple,
        captureSeq(
            '(',
            ',',
            ')',
            capturePatternExpr,
            )
        )

capturePatternAs = \
    transform(
        types.PatternAs,
        captureStuff(
            skip(pChar('(')),
            captureParen(capturePatternExpr),
            skip(pKeyword('as')),
            captureExprVar,
            skip(pChar(')')),
            )
        )

## SomeType _ (SomeOtherType x y) _
captureNestedPattern = \
    transform(
        types.PatternNested,
        captureStuff(
            captureParen(captureCustomTypePattern),
            )
        )

## custom type: SomeType _ x y _

doCaptureCustomTypePattern = \
    transform(
        types.CustomTypePattern,
        captureStuff(
            captureOneOf(
                capturePatternType,
            ),
            captureZeroOrMore(
                captureOneOf(
                    captureNestedPattern,
                    captureCustomTypeVal,
                    capturePatternExpr,
                    )
                )
            )
        )

## list pattern stuff: [], head :: rest

capturePatternListBrackets = \
    transform(
        types.PatternList,
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


## general pattern expression stuff

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

# if/then

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
