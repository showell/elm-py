import functools
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
    for n in reversed(range(lo, hi+1)):
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

def foldl(func, acc, lst):
    # internal
    if lst is None:
        return acc
    else:
        (x, xs) = lst
        return foldl(func, func(x, acc), xs)

def foldr(func, acc, xs):
    # optimized
    if xs is None:
        return acc
    else:
        (x, xs) = xs
        return func(x, foldr(func, acc, xs))

def filter_(isGood, lst):
    # optimized
    if lst is None:
        return None

    else:
        (x, xs) = lst
        rest = filter_(isGood, xs)
        if isGood(x):
            return (x, rest)
        else:
            return rest

def filterMap(f, xs):
    # optimized
    if xs is None:
        return None

    else:
        (x, xs) = xs
        v = f(x)
        if v is None:
            return filterMap(f, xs)
        else:
            return (v[1], filterMap(f, xs))

def length(lst):
    # optimized
    if lst is None:
        return 0
    else:
        return 1 + length(lst[1])

def reverse(lst):
    return foldl(cons, None, lst)

def member(x, xs):
    return any(lambda a: a == x, xs)

def all(isOkay, lst):
    # optimized
    if lst is None:
        return True
    else:
        (x, xs) = lst
        return isOkay(x) and all(isOkay, xs)

def any(isOkay, lst):
    if lst is None:
        return False
    else:
        (x, xs) = lst
        return isOkay(x) or any(isOkay, xs)

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
    if lst1 is None: return None
    if lst2 is None: return None

    (h1, r1) = lst1
    (h2, r2) = lst2
    return (
            f(h1, h2),
            map2(f, r1, r2))

def map3(f, lst1, lst2, lst3):
    # optimized
    if lst1 is None: return None
    if lst2 is None: return None
    if lst3 is None: return None

    (h1, r1) = lst1
    (h2, r2) = lst2
    (h3, r3) = lst3
    return (
            f(h1, h2, h3),
            map3(f, r1, r2, r3))

def map4(f, lst1, lst2, lst3, lst4):
    # optimized
    if lst1 is None: return None
    if lst2 is None: return None
    if lst3 is None: return None
    if lst4 is None: return None

    (h1, r1) = lst1
    (h2, r2) = lst2
    (h3, r3) = lst3
    (h4, r4) = lst4
    return (
            f(h1, h2, h3, h4),
            map4(f, r1, r2, r3, r4))

def map5(f, lst1, lst2, lst3, lst4, lst5):
    # optimized
    if lst1 is None: return None
    if lst2 is None: return None
    if lst3 is None: return None
    if lst4 is None: return None
    if lst5 is None: return None

    (h1, r1) = lst1
    (h2, r2) = lst2
    (h3, r3) = lst3
    (h4, r4) = lst4
    (h5, r5) = lst5
    return (
            f(h1, h2, h3, h4, h5),
            map5(f, r1, r2, r3, r4, r5))

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






