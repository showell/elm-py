from Custom import (
    CustomType
    )

"""
We have to desugar some stuff:

    You can't say:

        (a, (b, c))

    We say instead:
        (a, _foo1)

        (b, c) = _foo1

    You can't say:
        x =
            if cond:
                return 2
            else:
                return 3

    We say instead:
        def _foo1():
            if cond:
                return 2
            else:
                return 3
        return _foo1()

    You can't say:
        x = (
            z = 2
            def a():
                return x + y + z
            )(**arg)

    We say instead:

        def _foo1():
            z = 2
            def a():
                return x + y + z
        x = _foo1(**arg)


    We can't say:
        if x:
            return \
                if a:
                    return 2
                else:
                    return 3
        else:
            return 4

    We want to try to combine those:
        if x:
            if a:
                return 2
            else:
                return 3
        else:
            return 4

    Some expressions are simple:

        5 + 2

        foo(2, 3)

    Some statements are final:

        def a(x):
            return 5

    Other statements are ready-to-return, but not final nor
    easily wrapped:

        x = 2
        if cond:
            return 2
        else:
            return 3
"""


PythonCode = CustomType('PythonCode', Simple =1, Block=1, Anon=1)
Simple = PythonCode.Simple
Block = PythonCode.Block
Anon = PythonCode.Anon

def getFinalCode(ast):
    code = ast.emit()

    if code.match('Simple'):
        return code.val

    raise Exception('not supported yet')

def getBlockCode(ast):
    body = ast.emit()

    if body.match('Simple'):
        bodyCode = j(
            'return ' + body.val
            )
    elif body.match('Block'):
        bodyCode = body.val
    else:
        raise Exception('illegal')

    return bodyCode

def getCode(ast):
    code = ast.emit()

    if code.match('Simple'):
        return code.val

    raise Exception('not supported yet')

def getCodeList(asts):
    return [getCode(ast) for ast in asts]

def processItems(asts):
    preludes = []
    items = []
    i = 0

    for ast in asts:
        code = ast.emit()

        if code.match('Simple'):
            items.append(code.val)

        elif code.match('Anon'):
            i += 1
            name = '_anon' + str(i)
            preludes.append('def ' + name + code.val)
            items.append(name)

        elif code.match('Block'):
            i += 1
            name = '_foo' + str(i)
            preludes.append(j(
                'def ' + name + '():',
                indent(code.val)
            ))
            items.append(name + '()')

    prelude = '\n\n'.join(preludes)

    return (prelude, items)

def indent(s):
    return '\n'.join(
            '    ' + line
            for line in str(s).split('\n'))

def j(*lst):
    return '\n'.join(str(item) for item in lst)

def jj(lst):
    return '\n\n'.join(str(item) for item in lst)

def oneLine(*lst):
    return ' '.join(lst)

def formatList(lst, start, end):
    return start + ', '.join(str(item) for item in lst) + end

def commas(items):
    if len(items) == 0:
        raise Exception('MISSING')

    if len(items) == 1:
        return str(items[0])

    return str(items[0]) + '(' + ', '.join(str(x) for x in items[1:]) + ')'

def emitTuple(asts):
    prelude, items = processItems(asts)

    # XXX - need to blockify preludes
    if prelude:
        stmt = j(
            prelude,
            'return ' + formatList(items, '(', ')'),
            )
        return Block(stmt)

    stmt = formatList(items, '(', ')')
    return Simple(stmt)

class Comment:
    def __init__(self, ast):
        self.ast = ast

    def __str__(self):
        return 'COMMENT: ' + self.ast

class List:
    def __init__(self, ast):
        self.items = ast

    def __str__(self):
        return 'LIST ' + formatList(self.items, '(', ')')

    def emit(self):
        items = getCodeList(self.items)
        stmt = formatList(
            items,
            '[',
            ']',
            )
        return Simple(stmt)

class WildCard:
    def __init__(self, ast):
        assert(ast == '_')

    def __str__(self):
        return 'ANY'

    def emit(self):
        return Simple('Any')

class BinOp:
    def __init__(self, ast):
        self.expr1, self.op, self.expr2 = ast

    def __str__(self):
        return j(
            str(self.expr1),
            str(self.op),
            str(self.expr2),
            )

    def emit(self):
        expr1 = getCode(self.expr1)
        expr2 = getCode(self.expr2)

        stmt = expr1 + ' ' + self.op + ' ' + expr2

        return Simple(stmt)

class Token:
    def __init__(self, ast):
        self.token = ast

    def __str__(self):
        return self.token

    def emit(self):
        return Simple(self.token)

class PatternCons:
    def __init__(self, ast):
        self.token = ast

    def __str__(self):
        return self.token

    def emit(self):
        return Simple(self.token)

class Tuple:
    def __init__(self, ast):
        self.items = ast

    def __str__(self):
        return 'TUP ' + formatList(self.items, '(', ')')

    def emit(self):
        return emitTuple(self.items)

class TupleVar:
    def __init__(self, ast):
        self.items = ast

    def __str__(self):
        return 'TUPVAR ' + formatList(self.items, '(', ')')

    def emit(self):
        return emitTuple(self.items)

class Unit:
    def __init__(self, ast):
        assert len(ast) == 0

    def __str__(self):
        return 'UNIT'

class Module:
    def __init__(self, ast):
        self.ast = ast

    def __str__(self):
        return j(
            'MODULE',
            self.ast)

class Import:
    def __init__(self, ast):
        self.ast = ast

    def __str__(self):
        return j(
            'IMPORT',
            self.ast)

class Annotation:
    def __init__(self, ast):
        self.ast = ast

    def __str__(self):
        return j(
            'ANNOTATION',
            self.ast)

class Type:
    def __init__(self, ast):
        self.ast = ast

    def __str__(self):
        return j(
            'TYPE',
            self.ast)

class Call:
    def __init__(self, ast):
        self.items = ast

    def __str__(self):
        return 'CALL ' + commas(self.items)

    def emit(self):
        prelude, items = processItems(self.items)

        if prelude:
            stmt = j(
                prelude + '\n',
                'return ' + commas(items),
                )
            return Block(stmt)

        else:
            return Simple(commas(items))

class If:
    def __init__(self, ast):
        self.cond = ast[0]
        self.thenExpr = ast[1]
        self.elseExpr = ast[2]

    def __str__(self):
        return j(
            'IF',
            indent(self.cond),
            'THEN',
            indent(self.thenExpr),
            'ELSE',
            indent(self.elseExpr))

    def emit(self):
        condCode = getCode(self.cond)
        thenCode = getBlockCode(self.thenExpr)
        elseCode = getBlockCode(self.elseExpr)

        stmt = j(
            'if ' + condCode + ':',
            indent(thenCode),
            'else:',
            indent(elseCode),
            )
        return Block(stmt)

class CaseOf:
    def __init__(self, ast):
        self.expr = ast

    def __str__(self):
        return 'CASE OF: ' + str(self.expr)

    def emit(self):
        return Simple(getCode(self.expr))

class CustomTypePattern:
    def __init__(self, ast):
        self.token = ast[0]
        self.items = ast[1]

    def __str__(self):
        return 'CUSTOM TYPE ' + str(self.token) + ' ' + formatList(self.items, '(', ')')

    def emit(self):
        typeParam = 'Type(' + getCode(self.token) + ')'
        items = getCodeList(self.items)

        return Simple(', '.join([typeParam] + items))

class PatternDef:
    def __init__(self, ast):
        self.expr = ast

    def __str__(self):
        return str(self.expr)

    def emit(self):
        return Simple(getCode(self.expr))

class OneCase:
    def __init__(self, ast):
        self.patternDef = ast[0]
        self.body = ast[1]

    def __str__(self):
        return '\n'.join([
            'PATTERN',
            indent(self.patternDef),
            'BODY',
            indent(self.body)
            ])

    def emit(self):
        patternCode = getCode(self.patternDef)

        cond = 'patternMatch(pred, ' + patternCode + ')'

        bodyCode = getBlockCode(self.body)

        return Simple(j(
            'if ' + cond + ':',
            indent(bodyCode)
            ))

class Case:
    def __init__(self, ast):
        self.pred = ast[0]
        self.cases = ast[1]

    def __str__(self):
        return j(
            self.pred,
            indent(jj(self.cases))
            )

    def emit(self):
        predCode = getCode(self.pred)
        stmts = getCodeList(self.cases)

        body = '\n\n\n'.join(stmts)

        return Block(j(
            'casePred = ' + predCode + '\n',
            body
            ))

class Params:
    def __init__(self, ast):
        self.params = ast

    def __str__(self):
        return ', '.join(str(p) for p in self.params)

    def emit(self):
        params = ', '.join(getCodeList(self.params))
        return Simple(params)

class Def:
    def __init__(self, ast):
        self.ast = ast

    def __str__(self):
        return 'Def ASSIGN ' + str(self.ast)

    def emit(self):
        return self.ast.emit()

class FunctionDef:
    def __init__(self, ast):
        self.var = ast[0]
        self.params = ast[1]

    def __str__(self):
        return j(
            'ASSIGN',
            indent(self.var),
            indent(self.params),
            )

    def emit(self):
        fname = getCode(self.var)
        params = getCode(self.params)

        if '(' in params:
            unpackCode = params + ' = args\n'
            stmt = 'def ' + fname + '(*args):\n' + indent(unpackCode)
        else:
            stmt = 'def ' + fname + '(' + params + '):'

        return Simple(stmt)

class TupleAssign:
    def __init__(self, ast):
        self.def_ = ast[0]
        self.expr = ast[1]

    def __str__(self):
        return j(
            'TUP ASSIGN',
            self.def_,
            'EXPR',
            indent(self.expr))

    def emit(self):
        defCode = getCode(self.def_)

        bodyCode = getBlockCode(self.expr)

        return Simple(j(
            defCode + ' =',
            indent(bodyCode),
            '\n',
            ))

class NormalAssign:
    def __init__(self, ast):
        self.def_ = ast[0]
        self.expr = ast[1]

    def __str__(self):
        return j(
            self.def_,
            'EXPR',
            indent(self.expr))

    def emit(self):
        if type(self.def_) == TupleVar:
            raise Exception('tuple binding')

        defCode = getCode(self.def_)
        bodyCode = getBlockCode(self.expr)

        return Simple(j(
            defCode,
            indent(bodyCode),
            '\n',
            ))

class Lambda:
    def __init__(self, ast):
        self.params = ast[0]
        self.expr = ast[1]

    def __str__(self):
        return oneLine(
            str(self.params),
            '->',
            str(self.expr)
            )

    def emit(self):
        paramCode = getCode(self.params)
        bodyCode = getBlockCode(self.expr)

        stmt = j(
            '(' + paramCode + '):',
            indent(bodyCode)
            )
        return Anon(stmt)


class Let:
    def __init__(self, ast):
        self.bindings = ast[0]
        self.expr = ast[1]

    def __str__(self):
        return j(
            'LET',
            indent(jj(self.bindings)),
            'IN',
            indent(str(self.expr)))

    def emit(self):
        bindings = getCodeList(self.bindings)

        stmt = j(
            jj(bindings),
            getBlockCode(self.expr),
            )
        return Block(stmt)

