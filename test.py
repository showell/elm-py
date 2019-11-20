import List
import Maybe
import Order

# TESTING

def toPy(xs):
    return list(List._toIter(xs))

def toElm(lst):
    return List._fromIter(lst)


def printList(xs):
    print(toPy(xs))

def assertTrue(actual):
    if actual:
        print('pass')
    else:
        print('\n\nFAIL!\n', actual)
        print('\n')
        raise AssertionError

def assertFalse(actual):
    if not actual:
        print('pass')
    else:
        print('\n\nFAIL!\n', actual)
        print('\n')
        raise AssertionError

def assertEqual(actual, expected):
    if actual == expected:
        print('pass')
    else:
        print('\n\nFAIL!\n', actual, expected)
        print('\n')
        raise AssertionError

def assertList(elmList, expected):
    if toPy(elmList) == expected:
        print('pass')
    else:
        print('\n\nFAIL!\n', elmList, expected)
        print('\n')
        raise AssertionError

even = lambda x : x % 2 == 0
negative = lambda x : x < 0
positive = lambda x : x > 0
double = lambda x : x * 2
add = lambda x, y: x + y

def toMaybe(n):
    if n in [2, 4]:
        return Maybe.Just(10*n)
    else:
        return Maybe.Nothing()

lst3 = toElm([0, 1, 2])
numLst = toElm([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
empty = List.empty()
mod10 = lambda x: x % 10

def runTests():
    assertList(List.singleton(5), [5])
    assertList(List.repeat(3, 'x'), ['x', 'x', 'x'])
    assertList(List.range_(3, 6), [3, 4, 5, 6])
    assertList(List.cons(42, lst3), [42, 0, 1, 2])
    assertList(List.map_(double, lst3), [0, 2, 4])

    tup = lambda i, x: (i, 2*x)
    assertList(
            List.indexedMap(tup, lst3),
            [ (0, 0), (1, 2), (2, 4)])

    assertEqual(
            List.foldl(lambda x, acc: acc + x, "L", toElm("123")),
            "L123")

    assertEqual(
            List.foldr(lambda x, acc: acc + x, "R", toElm("123")),
            "R321")

    assertList(
            List.filter_(even, numLst),
            [2, 4, 6, 8, 10])

    assertList(
            List.filterMap(toMaybe, numLst),
            [ 20, 40 ])

    assertEqual(List.length(lst3), 3)

    assertTrue(List.any(even, numLst))
    assertFalse(List.any(negative, numLst))

    assertList(
            List.reverse(lst3),
            [2, 1, 0])

    assertTrue(List.member(7, numLst))
    assertFalse(List.member(987, numLst))

    assertTrue(List.all(positive, numLst))
    assertFalse(List.all(even, numLst))

    assertTrue(List.any(even, numLst))
    assertFalse(List.any(negative, numLst))

    assertEqual(List.maximum(empty), Maybe.Nothing())
    assertEqual(List.maximum(numLst), Maybe.Just(10))

    assertEqual(List.minimum(empty), Maybe.Nothing())
    assertEqual(List.minimum(numLst), Maybe.Just(1))

    assertEqual(List.sum(numLst), 55)
    assertEqual(List.product(numLst), 3628800)

    assertEqual(List.append(empty, lst3), lst3)
    assertEqual(List.append(lst3, empty), lst3)
    assertList(
            List.append(lst3, numLst),
            [0, 1, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    lsts = toElm([empty, lst3, empty, numLst])
    assertList(List.concat(lsts),
            [0, 1, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    mapper = lambda x: toElm([x, 5*x])
    assertList(List.concatMap(mapper, lst3),
            [0, 0, 1, 5, 2, 10])

    assertList(List.intersperse(999, lst3), [0, 999, 1, 999, 2])

    assertList(
            List.map2(
                lambda a, b: (a, b),
                toElm([5, 7]),
                toElm([6, 99, 3, 88888, 77777]),
            ),
            [ (5, 6),
              (7, 99),
            ]
            )

    assertList(
            List.map3(
                lambda a, b, c: (a, b, c),
                toElm([5, 7]),
                toElm([6, 99, 3]),
                toElm([8, 101]),
            ),
            [ (5, 6, 8),
              (7, 99, 101),
            ]
            )

    assertList(
            List.map5(
                lambda a, b, c, d, e: (a, b, c, d, e),
                toElm([1, 2, 3, 4]),
                toElm([2, 4, 6, 8]),
                toElm([3, 6, 9, 12]),
                toElm([10, 20, 30, 40]),
                toElm([33, 66]),
            ),
            [ (1, 2, 3, 10, 33),
              (2, 4, 6, 20, 66),
            ]
            )

    assertList(
            List.Tsort('int', toElm([4, 5, 1, 3, 2])),
            [1, 2, 3, 4, 5]
            )

    assertList(
            List.TsortBy('int', mod10, toElm([34, 15, 71, 83, 92])),
            [ 71
            , 92
            , 83
            , 34
            , 15
            ]
            )

    compF = lambda a, b: Order.fromInt(a - b)
    assertList(
            List.sortWith(compF, toElm([4, 5, 1, 3, 2])),
            [1, 2, 3, 4, 5]
            )

def checkPerformance():
    # Make sure we don't crash on large lists.  (We can't use
    # recursion carelessly in Python.)  These tests only exercise
    # performance.  Correctness tests are above.
    bigList = List.range_(1, 100000)
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
    List.filter_(lambda x: True, bigList)
    List.filterMap(toMaybe, bigList)
    List.reverse(bigList)
    assertEqual(List.maximum(bigList), Maybe.Just(100000))
    assertEqual(List.minimum(bigList), Maybe.Just(1))
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
            lambda a, b: (a, b),
            bigList,
            bigList)

    List.map3(
            lambda a, b, c: (a, b, c),
            bigList,
            bigList,
            bigList)

    List.map4(
            lambda a, b, c, d: (a, b, c, d),
            bigList,
            bigList,
            bigList,
            bigList)

    List.map5(
            lambda a, b, c, d, e: (a, b, c, d, e),
            bigList,
            bigList,
            bigList,
            bigList,
            bigList)

runTests()
checkPerformance()

