import functools
from inspect import signature

def F(f):
    n = len(signature(f).parameters)

    def wrapper(*args):
        if len(args) == 0:
            raise Exception("function expects args")

        if len(args) == n:
            return f(*args)

        return F(functools.partial(f, *args))

    return wrapper

def pipe(val, fns):
    for fn in fns:
        val = fn(val)
    return val
