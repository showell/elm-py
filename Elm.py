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
        'AsVar',
        'Val',
        'Var',
        'Nested',
        'Variant',
        'PList',
        'PCons',
        )

Variant = MatchParam.Variant
Any = MatchParam.Any
Val = MatchParam.Val
Var = MatchParam.Var
Nested = MatchParam.Nested
AsVar = MatchParam.AsVar
PList = MatchParam.PList
PCons = MatchParam.PCons

def patternMatch(val, main, *args):
    if type(val) == Custom:
        return patternMatchCustom(val, main, *args)

    raise Exception('unsupported pattern match')

def patternMatchCustom(val, main, *args):
    (mainType, mainVal) = main

    if mainType is not Variant:
        raise Exception('illegal pattern match')

    variantClass = mainVal

    if not val.isType(variantClass.typeName):
        return None

    if not val.match(variantClass.vtype):
        return None

    if val.arity != len(args):
        print(val.arity, val)
        print(len(args), args)
        raise Exception('illegal pattern match')

    if val.arity == 0:
        return True

    # In first loop, try to exit early
    vals = val.vals
    for i, arg in enumerate(args):
        if arg is Any:
            continue

        if arg[0] is Val:
            val = arg[1]
            if val != vals[i]:
                return None

    dct = None
    for i, arg in enumerate(args):
        if arg is Any:
            continue

        if arg[0] is AsVar:
            (_, varname, val) = arg
            res = patternMatch(vals[i], *val)
            if res is None:
                return None
            if dct is None:
                dct = dict()
            dct[varname] = vals[i]

        elif arg[0] is Nested:
            val = arg[1]
            res = patternMatch(vals[i], *val)
            if res is None:
                return None
            if dct is None:
                dct = dict()
            dct.update(res)

        elif arg[0] is Var:
            varname = arg[1]
            if dct is None:
                dct = dict()
            dct[varname] = vals[i]

    if dct is None:
        return True

    return dct
