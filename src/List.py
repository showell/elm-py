import functools
import itertools

from Order import orderToInt
import ListKernel as lk
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

toElm = lk.toElm
cons = lk.cons
uncons = lk.uncons

# hide builtins
range_ = range
map_ = map
filter_ = filter

# empty is a value!
empty = lk.empty()

def singleton(x):
    return cons(x, empty)

def repeat(n, x):
    out = empty
    for i in range_(n):
        out = cons(x, out)
    return out

def range(lo, hi):
    out = empty
    n = hi
    for n in range_(hi, lo-1, -1):
        out = cons(n, out)
    return out

@Elm.wrap(None, None, toElm)
def map(f, xs):
    return map_(f, xs)

@Elm.wrap(None, None, toElm)
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

@Elm.wrap(None, None, toElm)
def filter(isGood, lst):
    return filter_(isGood, lst)

@Elm.wrap(None, None, toElm)
def filterMap(f, lst):
    for x in lst:
        v = f(x)
        if v.match('Just'):
            yield v.val

def length(lst):
    i = 0
    for _ in lst:
       i += 1
    return i

def reverse(lst):
    return foldl(cons, empty, lst)

def member(x, xs):
    return any(lambda b: Kernel.eq(x, b), xs)

def all(isOkay, lst):
    for x in lst:
        if not isOkay(x):
            return False
    return True

def any(isOkay, lst):
    for x in lst:
        if isOkay(x):
            return True
    return False

def maximum(lst):
    if lk.isEmpty(lst):
        return Maybe.Nothing
    else:
        (x, xs) = uncons(lst)
        return Maybe.Just(foldl(max, x, xs))

def minimum(lst):
    if lk.isEmpty(lst):
        return Maybe.Nothing
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
    if lk.isEmpty(ys):
        return xs
    else:
        return foldr(cons, ys, xs)

def concat(lsts):
    return foldr(append, empty, lsts)

def concatMap(f, lst):
    return concat(map(f, lst))

def intersperse(sep, xs):
    if lk.isEmpty(xs):
        return empty
    else:
        (hd, tl) = uncons(xs)
        step = lambda x, rest: cons(sep, cons(x, rest))
        spersed = foldr(step, empty, tl)
        return cons(hd, spersed)

@Elm.wrap(None, None, None, toElm)
def map2(f, lst1, lst2):
    for (a, b) in zip(lst1, lst2):
        yield f(a, b)

@Elm.wrap(None, None, None, None, toElm)
def map3(f, lst1, lst2, lst3):
    for (a, b, c) in zip(lst1, lst2, lst3):
        yield f(a, b, c)

@Elm.wrap(None, None, None, None, None, toElm)
def map4(f, lst1, lst2, lst3, lst4):
    for (a, b, c, d) in zip(lst1, lst2, lst3, lst4):
        yield f(a, b, c, d)

@Elm.wrap(None, None, None, None, None, None, toElm)
def map5(f, lst1, lst2, lst3, lst4, lst5):
    for (a, b, c, d, e) in zip(lst1, lst2, lst3, lst4, lst5):
        yield f(a, b, c, d, e)

@Elm.wrap(None, None, toElm)
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
        return orderToInt(order)

    return _sortHelper(c, lst)

def isEmpty(lst):
    return lk.isEmpty(lst)

def head(xs):
    if lk.isEmpty(xs):
        return Maybe.Nothing

    (h, xs) = uncons(xs)
    return Maybe.Just(h)

def tail(xs):
    if lk.isEmpty(xs):
        return Maybe.Nothing

    (h, xs) = uncons(xs)
    return Maybe.Just(xs)

@Elm.wrap(None, None, toElm)
def take(n, xs):
    if n <= 0:
        return []

    return itertools.islice(iter(xs), n)

def drop(n, xs):
    if n <= 0:
        return xs

    for i in range_(n):
        if lk.isEmpty(xs):
            return empty
        (_, xs) = uncons(xs)

    return xs

def partition(pred, lst):
    def step(x, tup):
        (trues, falses) = tup

        if pred(x):
            return (cons(x, trues), falses)
        else:
            return (trues, cons(x, falses))

    return foldr(step, (empty, empty), lst)

def unzip(pairs):

    def step(pair, lsts):
        (x, y) = pair
        (xs, ys) = lsts
        return (cons(x, xs), cons(y, ys))

    return foldr(step, (empty, empty), pairs)
