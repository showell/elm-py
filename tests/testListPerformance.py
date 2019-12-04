"""
This takes a few seconds to run.  It tests performance for
List operations.  It doesn't do any actual benchmarks; it's
really just testing that List doesn't crash due to recursion
for large lists.
"""

import sys
sys.path.append('../src')

import List
import Maybe
import Tuple

from testHelper import assertEqual

add = lambda x, y: x + y
empty = List.empty

even = lambda x : x % 2 == 0
Nothing = Maybe.Nothing
Just = Maybe.Just

f2 = lambda a, b: (a, b)
f3 = lambda a, b, c: (a, b, c)
f4 = lambda a, b, c, d: (a, b, c, d)
f5 = lambda a, b, c, d, e: (a, b, c, d, e)

def toMaybe(n):
    if n in [2, 4]:
        return Just(10*n)
    else:
        return Nothing


def checkPerformance():
    # Make sure we don't crash on large lists.  (We can't use
    # recursion carelessly in Python.)  These tests only exercise
    # performance.  Correctness tests are above.
    bigList = List.range(1, 100000)
    assertEqual(
            List.foldl(add, 0, bigList),
            5000050000
            )
    assertEqual(
            List.length(List.foldr(List.cons, empty, bigList)),
            List.length(bigList)
            )
    List.all(lambda x: True, bigList)
    List.any(lambda x: False, bigList)
    List.filter(lambda x: True, bigList)
    List.filterMap(toMaybe, bigList)
    List.reverse(bigList)
    assertEqual(List.maximum(bigList), Just(100000))
    assertEqual(List.minimum(bigList), Just(1))
    List.sum(bigList)

    # product is expensive with big numbers!
    List.product(List.repeat(100000, 0))

    assertEqual(
            List.length(List.append(bigList, bigList)),
            200000)

    assertEqual(
            List.length(List.intersperse(0, bigList)),
            199999)

    List.map2(
            f2,
            bigList,
            bigList)

    List.map3(
            f3,
            bigList,
            bigList,
            bigList)

    List.map4(
            f4,
            bigList,
            bigList,
            bigList,
            bigList)

    List.map5(
            f5,
            bigList,
            bigList,
            bigList,
            bigList,
            bigList)

    List.tail(bigList)
    List.take(99999, bigList)
    List.drop(99999, bigList)

    (evens, odds) = List.partition(even, bigList)
    assertEqual(List.length(evens), 50000)
    assertEqual(List.length(odds), 50000)

    bigListOfTups = List.indexedMap(
            lambda i, n: Tuple.pair(i, n * 42),
            bigList)

    tupOfBigLists = List.unzip(bigListOfTups)

    assertEqual(List.head(Tuple.first(tupOfBigLists)), Just(0))
    assertEqual(List.head(Tuple.second(tupOfBigLists)), Just(42))

if __name__ == '__main__':
    checkPerformance()
