from Kernel import (
        isList,
        toElm,
        toElmList,
        toElmPred,
        toElmTup,
        toPy,
        toPyTup,
        )
import Elm
import Kernel
import List
import Maybe
import Tuple

# TESTING

F = Elm.F
Nothing = Maybe.Nothing()
Just = Maybe.Just

def printList(xs):
    print(toPy(xs))

def assertTrue(actual):
    if actual == Kernel.true:
        print('pass')
    else:
        print('\n\nFAIL!\n', actual)
        print('\n')
        raise AssertionError

def assertFalse(actual):
    if actual == Kernel.false:
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

even = toElmPred(lambda x : x % 2 == 0)
negative = toElmPred(lambda x : x < 0)
positive = toElmPred(lambda x : x > 0)
double = lambda x : x * 2
triple = lambda x : x * 3
add = lambda x, y: x + y

f2 = lambda a, b: toElmTup((a, b))
f3 = lambda a, b, c: toElmTup((a, b, c))
f4 = lambda a, b, c, d: toElmTup((a, b, c, d))
f5 = lambda a, b, c, d, e: toElmTup((a, b, c, d, e))

def toMaybe(n):
    if n in [2, 4]:
        return Just(10*n)
    else:
        return Nothing

lst3 = toElm([0, 1, 2])
lst3Clone = toElm([0, 1, 2])
s123 = toElm(["1", "2", "3"])

numLst = toElm([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
empty = List.empty()
mod10 = lambda x: x % 10

def testListBasics():
    assertEqual(
            lst3 == lst3Clone,
            True
            )

    assertEqual(
            List.empty() == empty,
            True
            )

    assertEqual(
            lst3 == numLst,
            False
            )

    assertEqual(
            Kernel.eq(lst3, lst3Clone),
            Kernel.true
            )

    assertEqual(
            Kernel.eq(List.empty(), empty),
            Kernel.true
            )

    assertEqual(
            Kernel.eq(lst3, numLst),
            Kernel.false
            )

    assertTrue(List.isEmpty(empty))
    assertFalse(List.isEmpty(numLst))

    assertEqual(isList(empty), True)
    assertEqual(isList(lst3), True)
    assertEqual(isList(99), False)

    assertList(List.singleton(5), [5])
    assertList(List.repeat(3, 'x'), ['x', 'x', 'x'])
    assertList(List.range(3, 6), [3, 4, 5, 6])
    assertList(List.cons(42, lst3), [42, 0, 1, 2])
    assertList(List.map(double, lst3), [0, 2, 4])

    tup = lambda i, x: (i, 2*x)
    assertList(
            List.indexedMap(tup, lst3),
            [ (0, 0), (1, 2), (2, 4)])

    assertEqual(
            List.foldl(lambda x, acc: acc + x, "L", s123),
            "L123")

    assertEqual(
            List.foldr(lambda x, acc: acc + x, "R", s123),
            "R321")

    assertList(
            List.filter(even, numLst),
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

    assertEqual(List.maximum(empty), Nothing)
    assertEqual(List.maximum(numLst), Just(10))

    assertEqual(List.minimum(empty), Nothing)
    assertEqual(List.minimum(numLst), Just(1))

    assertEqual(List.sum(numLst), 55)
    assertEqual(List.product(numLst), 3628800)

    assertEqual(List.append(empty, lst3), lst3)
    assertEqual(List.append(lst3, empty), lst3)
    assertList(
            List.append(lst3, numLst),
            [0, 1, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    lsts = toElmList([empty, lst3, empty, numLst])
    assertList(List.concat(lsts),
            [0, 1, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    mapper = lambda x: toElm([x, 5*x])
    assertList(List.concatMap(mapper, lst3),
            [0, 0, 1, 5, 2, 10])

    assertList(List.intersperse(999, lst3), [0, 999, 1, 999, 2])

    assertList(
            toPy(
                List.map2(
                    f2,
                    toElm([5, 7]),
                    toElm([6, 99, 3, 88888, 77777]),
                )
            ),
            [ (5, 6),
              (7, 99),
            ]
            )

    assertList(
            List.map3(
                f3,
                toElm([5, 7]),
                toElm([6, 99, 3]),
                toElm([8, 101]),
            ),
            [ (5, 6, 8),
              (7, 99, 101),
            ]
            )

    assertList(
            List.map4(
                f4,
                toElm([5, 7]),
                toElm([6, 99, 3]),
                toElm([8, 101]),
                toElm([1, 2]),
            ),
            [ (5, 6, 8, 1),
              (7, 99, 101, 2),
            ]
            )

    assertList(
            List.map5(
                f5,
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
            List.sort(toElm([4, 5, 1, 3, 2])),
            [1, 2, 3, 4, 5]
            )

    assertList(
            List.sortBy(mod10, toElm([34, 15, 71, 83, 92])),
            [ 71
            , 92
            , 83
            , 34
            , 15
            ]
            )

    assertList(
            List.sortWith(Kernel.toOrder, toElm([4, 5, 1, 3, 2])),
            [1, 2, 3, 4, 5]
            )

    assertEqual(
            List.tail(empty),
            Nothing)

    assertEqual(
            List.tail(toElm([1, 2, 3])),
            Just(toElm([2, 3]))
            )

    assertList(
            List.take(0, lst3),
            []
            )

    assertList(
            List.take(2, lst3),
            [0, 1]
            )

    assertList(
            List.take(3, lst3),
            [0, 1, 2]
            )

    assertList(
            List.take(4, lst3),
            [0, 1, 2]
            )

    assertList(
            List.take(0, lst3),
            []
            )

    assertList(
            List.take(2, lst3),
            [0, 1]
            )

    assertList(
            List.take(3, lst3),
            [0, 1, 2 ]
            )

    assertList(
            List.take(4, lst3),
            [0, 1, 2 ]
            )

    assertEqual(
            toPy(List.partition(even, numLst)),
            ([2, 4, 6, 8, 10], [1, 3, 5, 7, 9])
            )

    assertEqual(
            toPy(List.unzip(toElm([(1, 11), (2, 22), (3, 33)]))),
            ([1, 2, 3], [11, 22, 33])
            )


def testListOfLists():
    lol = toElm([
                [5],
                [1],
                [1, 2],
                [2],
                [1, 2, 3],
                [1, 2, 4],
                [1, 2, -1],
                [3],
                ])

    h = lambda lst: Maybe.unboxJust(List.head(lst))

    assertEqual(h(h(lol)), 5)

    assertList(List.sort(lol), [
        [ 1 ],
        [ 1, 2],
        [ 1, 2, -1],
        [ 1, 2, 3],
        [ 1, 2, 4],
        [ 2 ],
        [ 3 ],
        [ 5 ],
    ])

    assertEqual(
            List.member(List.singleton(2), lol),
            Kernel.true)

    assertEqual(
            List.member(List.singleton(9), lol),
            Kernel.false)

def testPartialApply():
    assertList(
            F(List.map)(double)(lst3),
            [0, 2, 4])

    accum = lambda x, acc: acc + x
    assertEqual(
            F(List.foldr)(accum)("R")(s123),
            "R321")

    assertEqual(
            F(List.foldr)(accum, "R")(s123),
            "R321")
    assertEqual(
            F(List.foldr)(accum)("R", s123),
            "R321")

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
    List.all(lambda x: Kernel.true, bigList)
    List.any(lambda x: Kernel.false, bigList)
    List.filter(lambda x: Kernel.true, bigList)
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

    (evens, odds) = toPyTup(List.partition(even, bigList))
    assertEqual(List.length(evens), 50000)
    assertEqual(List.length(odds), 50000)

    bigListOfTups = List.indexedMap(
            lambda i, n: Tuple.pair(i, n * 42),
            bigList)

    tupOfBigLists = List.unzip(bigListOfTups)

    assertEqual(List.head(Tuple.first(tupOfBigLists)), Just(0))
    assertEqual(List.head(Tuple.second(tupOfBigLists)), Just(42))

def testTuples():
    assertEqual(Tuple.pair(1,2), Tuple.pair(1,2))
    assertTrue(Kernel.eq(Tuple.pair(1,2), Tuple.pair(1,2)))
    assertFalse(Kernel.eq(Tuple.pair(1,2), Tuple.pair(3,4)))

    t = Tuple.pair(5, 6)
    assertEqual(Tuple.first(t), 5)
    assertEqual(Tuple.second(t), 6)

    assertEqual(
            toPy(Tuple.mapFirst(double, t)),
            (10, 6))

    assertEqual(
            toPy(Tuple.mapSecond(double, t)),
            (5, 12))

    assertEqual(
            toPy(Tuple.mapBoth(triple, double, t)),
            (15, 12))

def testMaybe():
    assertEqual(Maybe.withDefault(Nothing, 5), 5)
    assertEqual(Maybe.withDefault(Just(42), 99), 42)

    assertEqual(Maybe.map(double, Nothing), Nothing)
    assertEqual(Maybe.map(double, Just(42)), Just(84))

    assertEqual(
            Maybe.map2(f2, Just(1), Nothing),
            Nothing)
    assertEqual(
            Maybe.map2(f2, Nothing, Just(2)),
            Nothing)
    assertEqual(
            Maybe.map2(f2, Just(1), Just(2)),
            Just(toElmTup((1, 2))))

    assertEqual(
            Maybe.map3(f3, Just(1), Nothing, Nothing),
            Nothing)
    assertEqual(
            Maybe.map3(f3, Nothing, Just(2), Nothing),
            Nothing)
    assertEqual(
            Maybe.map3(f3, Nothing, Nothing, Just(2)),
            Nothing)
    assertEqual(
            Maybe.map3(f3, Just(1), Just(2), Just(3)),
            Just(toElmTup((1, 2, 3))))

    # cheat for map4/map5
    assertEqual(Maybe.map4, Maybe.mapN)
    assertEqual(Maybe.map5, Maybe.mapN)

    assertEqual(Maybe.andThen(toMaybe, Just(2)), Just(20))
    assertEqual(Maybe.andThen(toMaybe, Just(99)), Nothing)
    assertEqual(Maybe.andThen(toMaybe, Nothing), Nothing)


def testPipes():
    val = Elm.pipe(5, [
            double,
            F(add)(7),
            double,
            F(add)(3),
            ])
    assertEqual(val, 37)

testListBasics()
testPartialApply()
testListOfLists()
testTuples()
testPipes()
testMaybe()

print("\n\nchecking performance...")
checkPerformance()

