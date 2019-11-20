import functools
import itertools
import operator
import Maybe
import Order

"""
Internally we store Python lists as tuples, which are
immutable.

    [] = None
    [1] = (1, None)
    [1, 2] = (1, (2, None))
    [1, 2, 3] = (1, (2, (3, None))))

    isEmpty(lst) = lst is None
    (x, xs) = lst
"""

def _fromIter(it):
    lst = reversed(list(it))

    out = None
    for x in lst:
        out = (x, out)

    return out

def _toIter(xs):
    while xs is not None:
        (h, xs) = xs
        yield h

def singleton(x):
    # optimized
    return (x, None)

def repeat(n, x):
    # optimized
    out = None
    for i in range(n):
        out = (x, out)
    return out

def range_(lo, hi):
    # optimized
    out = None
    n = hi
    for n in range(hi, lo-1, -1):
        out = (n, out)
    return out

def cons(x, xs):
    return (x, xs)

def map_(f, xs):
    # optimized
    return _fromIter(map(f, _toIter(xs)))

def indexedMap(f, xs):
    # optimized
    return _fromIter(f(i, a) for i, a
                     in enumerate(_toIter(xs)))

def foldl(func, acc, xs):
    # optimized
    for x in _toIter(xs):
        acc = func(x, acc)
    return acc

def foldr(func, acc, xs):
    # optimized
    # Note that foldr makes a fully copy of our list.
    for x in reversed(list(_toIter(xs))):
        acc = func(x, acc)
    return acc

def filter_(isGood, lst):
    # optimized
    return _fromIter(filter(isGood, _toIter(lst)))

def filterMap(f, xs):
    # optimized
    def sieve():
        for x in _toIter(xs):
            v = f(x)
            if v != Maybe.Nothing():
                yield Maybe.unboxJust(v)

    return _fromIter(sieve())

def length(lst):
    # optimized
    i = 0
    while (lst):
       i += 1
       lst = lst[1]
    return i

def reverse(lst):
    return foldl(cons, None, lst)

def member(x, xs):
    return any(lambda a: a == x, xs)

def all(isOkay, lst):
    # optimized
    for x in _toIter(lst):
        if not isOkay(x):
            return False
    return True

def any(isOkay, lst):
    for x in _toIter(lst):
        if isOkay(x):
            return True
    return False

def maximum(lst):
    if lst is None:
        return None
    else:
        (x, xs) = lst
        return Maybe.Just(foldl(max, x, xs))

def minimum(lst):
    if lst is None:
        return None
    else:
        (x, xs) = lst
        return Maybe.Just(foldl(min, x, xs))

def sum(lst):
    return foldl(
            lambda a, b: a + b,
            0,
            lst)

def product(lst):
    # could use mat
    return foldl(
            lambda a, b: a * b,
            1,
            lst)

def append(xs, ys):
    if ys is None:
        return xs
    else:
        return foldr(cons, ys, xs)

def concat(lsts):
    return foldr(append, None, lsts)

def concatMap(f, lst):
    return concat(map_(f, lst))

def intersperse(sep, xs):
    if xs is None:
        return None
    else:
        (hd, tl) = xs
        step = lambda x, rest: (sep, (x, rest))
        spersed = foldr(step, None, tl)
        return (hd, spersed)

def map2(f, lst1, lst2):
    # optimized
    def combine():
        for (a, b) in zip(
                _toIter(lst1),
                _toIter(lst2)):
            yield f(a, b)

    return _fromIter(combine())

def map3(f, lst1, lst2, lst3):
    # optimized
    def combine():
        for (a, b, c) in zip(
                _toIter(lst1),
                _toIter(lst2),
                _toIter(lst3)):
            yield f(a, b, c)

    return _fromIter(combine())

def map4(f, lst1, lst2, lst3, lst4):
    # optimized
    def combine():
        for (a, b, c, d) in zip(
                _toIter(lst1),
                _toIter(lst2),
                _toIter(lst3),
                _toIter(lst4)):
            yield f(a, b, c, d)

    return _fromIter(combine())

def map5(f, lst1, lst2, lst3, lst4, lst5):
    # optimized
    def combine():
        for (a, b, c, d, e) in zip(
                _toIter(lst1),
                _toIter(lst2),
                _toIter(lst3),
                _toIter(lst4),
                _toIter(lst5)):
            yield f(a, b, c, d, e)

    return _fromIter(combine())

"""
NOTE:

For Tsort/TsortBy...

We need the compiler to pass in the type, so we know
how to compare elements.
"""

def _sortHelper(compF, lst):
    f = functools.cmp_to_key(compF)
    return _fromIter(sorted(_toIter(lst), key=f))

def _compare(T):
    if T == 'int':
        return lambda a, b: a - b

def Tsort(T, lst):
    # optimized
    c = _compare(T)
    return _sortHelper(c, lst)

def TsortBy(T, f, lst):
    # optimized
    c = lambda a, b: _compare(T)(f(a), f(b))
    return _sortHelper(c, lst)

def sortWith(compF, lst):
    c = lambda a, b: Order.toInt(compF(a, b))
    return _sortHelper(c, lst)






