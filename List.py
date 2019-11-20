import functools
import operator
import Kernel
import Maybe
import Order

"""
Internally we store Python lists as tuples, which are
immutable.

    [] = ('[]')
    [1] = (1, ('[]',))
    [1, 2] = (1, (2, ...))
"""

def _fromIter(it):
    lst = reversed(list(it))

    out = empty()
    for x in lst:
        out = cons(x, out)

    return out

toIter = Kernel.listToIter
uncons = Kernel.listUncons
isEmpty = Kernel.listIsEmpty

def empty():
    return ('[]',)


def singleton(x):
    # optimized
    return cons(x, empty())

def repeat(n, x):
    # optimized
    out = empty()
    for i in range(n):
        out = cons(x, out)
    return out

def range_(lo, hi):
    # optimized
    out = empty()
    n = hi
    for n in range(hi, lo-1, -1):
        out = cons(n, out)
    return out

def cons(x, xs):
    return ('::', x, xs)

def map_(f, xs):
    # optimized
    return _fromIter(map(f, toIter(xs)))

def indexedMap(f, xs):
    # optimized
    return _fromIter(f(i, a) for i, a
                     in enumerate(toIter(xs)))

def foldl(func, acc, xs):
    # optimized
    for x in toIter(xs):
        acc = func(x, acc)
    return acc

def foldr(func, acc, xs):
    # optimized
    # Note that foldr makes a fully copy of our list.
    for x in reversed(list(toIter(xs))):
        acc = func(x, acc)
    return acc

def filter_(isGood, lst):
    # optimized
    return _fromIter(filter(isGood, toIter(lst)))

def filterMap(f, xs):
    # optimized
    def sieve():
        for x in toIter(xs):
            v = f(x)
            if v != Maybe.Nothing():
                yield Maybe.unboxJust(v)

    return _fromIter(sieve())

def length(lst):
    # optimized
    i = 0
    for _ in toIter(lst):
       i += 1
    return i

def reverse(lst):
    return foldl(cons, empty(), lst)

def member(x, xs):
    return any(lambda a: a == x, xs)

def all(isOkay, lst):
    # optimized
    for x in toIter(lst):
        if not isOkay(x):
            return False
    return True

def any(isOkay, lst):
    for x in toIter(lst):
        if isOkay(x):
            return True
    return False

def maximum(lst):
    if isEmpty(lst):
        return Maybe.Nothing()
    else:
        (x, xs) = uncons(lst)
        return Maybe.Just(foldl(max, x, xs))

def minimum(lst):
    if isEmpty(lst):
        return Maybe.Nothing()
    else:
        (x, xs) = uncons(lst)
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
    if isEmpty(ys):
        return xs
    else:
        return foldr(cons, ys, xs)

def concat(lsts):
    return foldr(append, empty(), lsts)

def concatMap(f, lst):
    return concat(map_(f, lst))

def intersperse(sep, xs):
    if isEmpty(xs):
        return empty()
    else:
        (hd, tl) = uncons(xs)
        step = lambda x, rest: cons(sep, cons(x, rest))
        spersed = foldr(step, empty(), tl)
        return cons(hd, spersed)

def map2(f, lst1, lst2):
    # optimized
    def combine():
        for (a, b) in zip(
                toIter(lst1),
                toIter(lst2)):
            yield f(a, b)

    return _fromIter(combine())

def map3(f, lst1, lst2, lst3):
    # optimized
    def combine():
        for (a, b, c) in zip(
                toIter(lst1),
                toIter(lst2),
                toIter(lst3)):
            yield f(a, b, c)

    return _fromIter(combine())

def map4(f, lst1, lst2, lst3, lst4):
    # optimized
    def combine():
        for (a, b, c, d) in zip(
                toIter(lst1),
                toIter(lst2),
                toIter(lst3),
                toIter(lst4)):
            yield f(a, b, c, d)

    return _fromIter(combine())

def map5(f, lst1, lst2, lst3, lst4, lst5):
    # optimized
    def combine():
        for (a, b, c, d, e) in zip(
                toIter(lst1),
                toIter(lst2),
                toIter(lst3),
                toIter(lst4),
                toIter(lst5)):
            yield f(a, b, c, d, e)

    return _fromIter(combine())

def _sortHelper(compF, lst):
    f = functools.cmp_to_key(compF)
    return _fromIter(sorted(toIter(lst), key=f))

def sort(lst):
    return _sortHelper(Kernel.compare, lst)

def sortBy(f, lst):
    # optimized
    c = lambda a, b: Kernel.compare(f(a), f(b))
    return _sortHelper(c, lst)

def sortWith(compF, lst):
    c = lambda a, b: Order.toInt(compF(a, b))
    return _sortHelper(c, lst)

def head(xs):
    if isEmpty(xs):
        return Maybe.Nothing()
    else:
        (h, xs) = uncons(xs)
        return Maybe.Just(h)



