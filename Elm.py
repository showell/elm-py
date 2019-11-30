import functools
from inspect import signature
from Maybe import (
        Nothing,
        Just
        )
from Custom import (
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

MatchParam = CustomType('MatchParam', 'Any', Val=1)

def patternMatch(val, vtype, *args):
    if not val.match(vtype):
        return Nothing

    if val.arity != len(args):
        raise Exception('illegal pattern match')

    if val.arity == 0:
        return Just(dict())

    vals = val.vals
    for i, arg in enumerate(args):
        if arg.match('Val'):
            if arg.val != vals[i]:
                return Nothing

    return Just(dict())


