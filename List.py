from Kernel import (
        listIsEmpty,
        toElmBool,
        toElmList,
        toElmTup,
        toPyPred,
        toPyTup
        )
import functools
import itertools
import operator
import Kernel
import Maybe
import Elm

"""
Internally we store Python lists as tuples, which are
immutable.

    [] = ('[]')
    [1] = (1, ('[]',))
    [1, 2] = (1, (2, ...))
"""

cons = Kernel.listCons
empty = Kernel.listNil
uncons = Kernel.listUncons

# hide builtins
range_ = range
map_ = map
filter_ = filter

def singleton(x):
    return cons(x, empty())

def repeat(n, x):
    out = empty()
    for i in range_(n):
        out = cons(x, out)
    return out

def range(lo, hi):
    out = empty()
    n = hi
    for n in range_(hi, lo-1, -1):
        out = cons(n, out)
    return out

@Elm.wrap(None, None, toElmList)
def map(f, xs):
    return map_(f, xs)

@Elm.wrap(None, None, toElmList)
def indexedMap(f, xs):
    return (f(i, a) for i, a in enumerate(xs))

def foldl(func, acc, xs):
    for x in xs:
        acc = func(x, acc)
    return acc

def foldr(func, acc, xs):
    # Note that foldr makes a fully copy of our list.
    for x in reversed(list(iter(xs))):
        acc = func(x, acc)
    return acc

@Elm.wrap(toPyPred, None, toElmList)
def filter(isGood, lst):
    return filter_(isGood, lst)

@Elm.wrap(None, None, toElmList)
def filterMap(f, lst):
    for x in lst:
        v = f(x)
        if Maybe.isJust(v):
            yield Maybe.unboxJust(v)

def length(lst):
    i = 0
    for _ in lst:
       i += 1
    return i

def reverse(lst):
    return foldl(cons, empty(), lst)

def member(x, xs):
    return any(lambda b: Kernel.eq(x, b), xs)

@Elm.wrap(toPyPred, None, toElmBool)
def all(isOkay, lst):
    for x in lst:
        if not isOkay(x):
            return False
    return True

@Elm.wrap(toPyPred, None, toElmBool)
def any(isOkay, lst):
    for x in lst:
        if isOkay(x):
            return True
    return False

def maximum(lst):
    if listIsEmpty(lst):
        return Maybe.Nothing()
    else:
        (x, xs) = uncons(lst)
        return Maybe.Just(foldl(max, x, xs))

def minimum(lst):
    if listIsEmpty(lst):
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
    if listIsEmpty(ys):
        return xs
    else:
        return foldr(cons, ys, xs)

def concat(lsts):
    return foldr(append, empty(), lsts)

def concatMap(f, lst):
    return concat(map(f, lst))

def intersperse(sep, xs):
    if listIsEmpty(xs):
        return empty()
    else:
        (hd, tl) = uncons(xs)
        step = lambda x, rest: cons(sep, cons(x, rest))
        spersed = foldr(step, empty(), tl)
        return cons(hd, spersed)

@Elm.wrap(None, None, None, toElmList)
def map2(f, lst1, lst2):
    for (a, b) in zip(lst1, lst2):
        yield f(a, b)

@Elm.wrap(None, None, None, None, toElmList)
def map3(f, lst1, lst2, lst3):
    for (a, b, c) in zip(lst1, lst2, lst3):
        yield f(a, b, c)

@Elm.wrap(None, None, None, None, None, toElmList)
def map4(f, lst1, lst2, lst3, lst4):
    for (a, b, c, d) in zip(lst1, lst2, lst3, lst4):
        yield f(a, b, c, d)

@Elm.wrap(None, None, None, None, None, None, toElmList)
def map5(f, lst1, lst2, lst3, lst4, lst5):
    for (a, b, c, d, e) in zip(lst1, lst2, lst3, lst4, lst5):
        yield f(a, b, c, d, e)

@Elm.wrap(None, None, toElmList)
def _sortHelper(compF, lst):
    f = functools.cmp_to_key(compF)
    return sorted(list(lst), key=f)

def sort(lst):
    return _sortHelper(Kernel.compare, lst)

def sortBy(f, lst):
    c = lambda a, b: Kernel.compare(f(a), f(b))
    return _sortHelper(c, lst)

def sortWith(compF, lst):
    def c(a, b):
        order = compF(a, b)
        return Kernel.orderToInt(order)

    return _sortHelper(c, lst)

@Elm.wrap(None, toElmBool)
def isEmpty(lst):
    return listIsEmpty(lst)

def head(xs):
    if listIsEmpty(xs):
        return Maybe.Nothing()

    (h, xs) = uncons(xs)
    return Maybe.Just(h)

def tail(xs):
    if listIsEmpty(xs):
        return Maybe.Nothing()

    (h, xs) = uncons(xs)
    return Maybe.Just(xs)

@Elm.wrap(None, None, toElmList)
def take(n, xs):
    if n <= 0:
        return []

    return itertools.islice(iter(xs), n)

def drop(n, xs):
    if n <= 0:
        return xs

    i = 0
    for x in xs:
        if i >= n:
            return x
        i += 1

    return empty()

@Elm.wrap(toPyPred, None, toElmTup)
def partition(pred, lst):
    def step(x, tup):
        (trues, falses) = tup

        if pred(x):
            return (cons(x, trues), falses)
        else:
            return (trues, cons(x, falses))

    return foldr(step, (empty(), empty()), lst)

@Elm.wrap(None, toElmTup)
def unzip(pairs):

    @Elm.wrap(toPyTup, None, None)
    def step(pair, lsts):
        (x, y) = pair
        (xs, ys) = lsts
        return (cons(x, xs), cons(y, ys))

    return foldr(step, (empty(), empty()), pairs)
