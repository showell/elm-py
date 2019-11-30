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
        return 'MISSING params!'

    if len(items) == 1:
        return str(items[0])

    return str(items[0]) + '(' + ', '.join(str(x) for x in items[1:]) + ')'

def emitTuple(asts):
    items = (ast.emit() for ast in asts)
    return formatList(items, '(', ')')

class CustomTypePattern:
    def __init__(self, ast):
        self.token = ast[0]
        self.items = ast[1]

    def __str__(self):
        return 'CUSTOM TYPE ' + str(self.token) + ' ' + formatList(self.items, '(', ')')

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
        return formatList(
            [ast.emit() for ast in self.items],
            '[',
            ']',
            )

class Operator:
    def __init__(self, ast):
        self.op = ast

    def __str__(self):
        return self.op

    def emit(self):
        return self.op

class Token:
    def __init__(self, ast):
        self.token = ast

    def __str__(self):
        return self.token

    def emit(self):
        return self.token

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
        items = [ast.emit() for ast in self.items]
        return commas(items)

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
        stmt = j(
            'if ' + self.cond.emit() + ':',
            indent('return ' + self.thenExpr.emit()),
            'else:',
            indent('return ' + self.elseExpr.emit())
            )
        return stmt

class CaseOf:
    def __init__(self, ast):
        self.expr = ast

    def __str__(self):
        return 'CASE OF: ' + str(self.expr)

    def emit(self):
        # XXX
        return str(self.expr)

class PatternDef:
    def __init__(self, ast):
        self.expr = ast

    def __str__(self):
        return str(self.expr)

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
        cond = 'patternMatch(pred, ...'

        return j(
            'if ' + cond + ':',
            indent(self.body.emit())
            )

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
        stmts = [
            c.emit() for
            c in self.cases]

        body = '\n\n'.join(stmts)

        return j(
            'casePred = ' + self.pred.emit(),
            body
            )

class Params:
    def __init__(self, ast):
        self.params = ast

    def __str__(self):
        return ', '.join(str(p) for p in self.params)

    def emit(self):
        params = ', '.join(
            p.emit() for p in self.params
            )
        return params

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
        return ''.join([
            'def ',
            str(self.var),
            '(',
            str(self.params),
            '):'
            ])

class Binding:
    def __init__(self, ast):
        self.def_ = ast[0]
        self.expr = ast[1]

    def __str__(self):
        return j(
            self.def_,
            'EXPR',
            indent(self.expr))

    def emit(self):
        return j(
            self.def_.emit(),
            indent(self.expr.emit()),
            '\n',
            )

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
        return ' '.join([
            'lambda',
            self.params.emit(),
            ':',
            self.expr.emit()
            ])

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
        return j(
            jj(b.emit() for b in self.bindings),
            'return',
            indent(self.expr.emit())
            )

