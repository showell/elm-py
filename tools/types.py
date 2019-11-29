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

class CustomTypePattern:
    def __init__(self, ast):
        self.token = ast[0]
        self.items = ast[1]

    def __str__(self):
        return 'CUSTOM TYPE ' + self.token + ' ' + formatList(self.items, '(', ')')

class Comment:
    def __init__(self, ast):
        self.ast = ast

    def __str__(self):
        return 'COMMENT: ' + self.ast

class UnParsed:
    def __init__(self, ast):
        self.ast = ast

    def __str__(self):
        return 'unparsed: ' + self.ast

class List:
    def __init__(self, ast):
        self.items = ast

    def __str__(self):
        return 'LIST ' + formatList(self.items, '(', ')')

class Tuple:
    def __init__(self, ast):
        self.items = ast

    def __str__(self):
        return 'TUP ' + formatList(self.items, '(', ')')

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

class Params:
    def __init__(self, ast):
        self.patterns = ast

    def __str__(self):
        return ' '.join(str(p) for p in self.patterns)

class Binding:
    def __init__(self, ast):
        self.def_ = ast[0]
        self.expr = ast[1]

    def __str__(self):
        return j(
            self.def_,
            'EXPR',
            indent(self.expr))

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

class Def:
    def __init__(self, ast):
        self.var = ast[0]
        self.params = ast[1]

    def __str__(self):
        return j(
            'ASSIGN',
            indent(self.var),
            indent(self.params),
            )

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

class Case:
    def __init__(self, ast):
        self.pred = ast[0]
        self.cases = ast[1]

    def __str__(self):
        return j(
            self.pred,
            indent(jj(self.cases))
            )

class CaseOf:
    def __init__(self, ast):
        self.expr = ast

    def __str__(self):
        return 'CASE OF: ' + str(self.expr)

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


