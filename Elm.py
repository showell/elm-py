import functools
from inspect import signature
from Maybe import (
        Nothing,
        Just
        )
from Custom import (
        Custom,
        CustomType,
        )

def F(f):
    n = len(signature(f).parameters)

    def wrapper(*args):
        if len(args) == 0:
            raise Exception("function expects args")

        if len(args) == n:
            return f(*args)

        return F(functools.partial(f, *args))

    return wrapper

def wrap(*converters):
    argFuncs = converters[:-1]
    returnFunc = converters[-1]

    def convert(i, a):
        if argFuncs[i] is None:
            return a
        else:
            return argFuncs[i](a)

    def wrap(f):
        @functools.wraps(f)
        def wrapper(*args):
            newArgs = [
                    convert(i, a)
                    for i, a
                    in enumerate(args)
                    ]
            result = f(*newArgs)
            if returnFunc is None:
                return result
            else:
                return returnFunc(result)

        return wrapper

    return wrap


def pipe(val, fns):
    for fn in fns:
        val = fn(val)
    return val

def lcompose(g, f):
    return lambda x: g(f(x))

def rcompose(g, f):
    return lambda x: f(g(x))

MatchParam = CustomType('MatchParam',
        'Any',
        Val=1,
        Var=1,
        Type=1,
        )

def patternMatch(val, main, *args):
    def check(arg):
        if type(arg) != Custom:
            raise Exception('illegal pattern match')

        if arg.typeName != 'MatchParam':
            raise Exception('illegal pattern match')

    check(main)
    for arg in args:
        check(arg)

    if type(val) == Custom:
        if not main.match('Type'):
            raise Exception('illegal pattern match')

        variantClass = main.val

        if not val.isType(variantClass.typeName):
            return Nothing

        if not val.match(variantClass.vtype):
            return Nothing

        if val.arity != len(args):
            raise Exception('illegal pattern match')

        if val.arity == 0:
            return Just(dict())

        dct = dict()
        vals = val.vals
        for i, arg in enumerate(args):
            if arg.match('Val'):
                if arg.val != vals[i]:
                    return Nothing
            elif arg.match('Var'):
                dct[arg.val] = vals[i]
            else:
                if not arg.match('Any'):
                    raise Exception('illegal pattern match')

        return Just(dct)

    raise Exception('unsupported pattern match')

