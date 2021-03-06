import sys
sys.path.append('../src')

import math
import random
from time import perf_counter

import Dict
import List
import Maybe
from Kernel import toPy

from Elm import (
    patternMatch,
    MatchParam,
    )

Variant = MatchParam.Variant
Any = MatchParam.Any
Var = MatchParam.Var

# Use a deterministic seed to avoid test flakes. (But you can
# perturb this if you want more randomness.)
random.seed(44)

Just = Maybe.Just

add = lambda k, v: k + v
add3 = lambda a, b, c: a + b + c
double = lambda m: Just(m.val * 2)

def maxDepth(dct):
    res = patternMatch(dct,
        (Variant, Dict.RBNode_elm_builtin),
        Any,
        Any,
        Any,
        (Var, 'left'),
        (Var, 'right'),
        )

    if res is None:
        return 0

    return 1 + max(maxDepth(res['left']), maxDepth(res['right']))

def testBasics():
    print('singleton')
    dct = Dict.singleton(5, 50)
    assert Dict.get(5, dct).val == 50

    print('empty')
    dct = Dict.empty
    print(toPy(dct))
    print('member', Dict.member(5, dct))
    print('get', Dict.get(5, dct))
    print('size', Dict.size(dct))
    print('empty', Dict.isEmpty(dct))

    print('\n\ninsert one...')
    dct = Dict.insert(5, 50, dct)
    print('member', Dict.member(5, dct))
    print('get', Dict.get(5, dct))
    keys = Dict.keys(dct)
    print('keys', keys)
    print('size', Dict.size(dct))
    print('empty', Dict.isEmpty(dct))

def benchmark(n):
    def printRate(elapsed):
        if elapsed == 0:
            print('elapsed = 0')
            return
        print('rate', int(n * 1.0 / elapsed))
        print('\n')


    print('\n\ninsert many...')
    lst = list(range(n))
    random.shuffle(lst)

    dct = Dict.empty
    t = perf_counter()
    for i in lst:
        dct = Dict.insert(i, i*10, dct)
    elapsed = perf_counter() - t
    printRate(elapsed)

    depth = maxDepth(dct)
    print('max depth', depth)
    threshold = 2 * math.log2(n)
    print('threshold', math.ceil(threshold))
    assert depth < threshold
    print()

    print('membership')
    t = perf_counter()
    for i in lst:
        assert Dict.member(i, dct)
    elapsed = perf_counter() - t
    printRate(elapsed)


    print('get')
    t = perf_counter()
    for i in lst:
        assert Dict.get(i, dct).val == i * 10
    elapsed = perf_counter() - t
    printRate(elapsed)

    print('keys')
    t = perf_counter()
    keys = Dict.keys(dct)
    elapsed = perf_counter() - t
    printRate(elapsed)
    assert list(keys) == sorted(lst)

    print('values')
    t = perf_counter()
    values = Dict.values(dct)
    elapsed = perf_counter() - t
    printRate(elapsed)
    assert list(values) == sorted(10 * i for i in lst)


    print('update')
    t = perf_counter()

    for i in lst:
        dct = Dict.update(i, double, dct)
    elapsed = perf_counter() - t
    printRate(elapsed)

    for i in lst:
        assert Dict.get(i, dct).val == i * 20

    assert Dict.size(dct) == n

    print('remove')
    t = perf_counter()
    for i in lst:
        dct = Dict.remove(i, dct)
    elapsed = perf_counter() - t
    printRate(elapsed)

    assert Dict.size(dct) == 0

    print('fromList')
    tups = [(n, n * 2) for n in lst]
    elmLst = List.toElm(tups)
    t = perf_counter()
    dct = Dict.fromList(elmLst)
    elapsed = perf_counter() - t
    printRate(elapsed)

    assert Dict.size(dct) == n

    print('keys')
    t = perf_counter()
    keys = Dict.keys(dct)
    elapsed = perf_counter() - t
    printRate(elapsed)
    assert list(keys) == sorted(lst)

    print('toList')
    t = perf_counter()
    outLst = Dict.toList(dct)
    elapsed = perf_counter() - t
    printRate(elapsed)
    assert list(outLst) == sorted(tups)

    print('map')
    t = perf_counter()
    dct = Dict.map(add, dct)
    elapsed = perf_counter() - t
    printRate(elapsed)
    assert list(Dict.values(dct)) == [
        3*i for i in sorted(lst)]

    print('foldl')
    t = perf_counter()
    bigSum = Dict.foldl(add3, 0, dct)
    elapsed = perf_counter() - t
    printRate(elapsed)
    assert bigSum == 4 * n * (n-1) / 2

    accum = lambda k, v, accLst: List.cons((v, k), accLst)
    print('foldr')
    t = perf_counter()
    outLst = Dict.foldr(accum, List.empty, dct)
    elapsed = perf_counter() - t
    printRate(elapsed)
    assert list(outLst) == [(n*3, n) for n in sorted(lst)]

    evenKey = lambda k, v: k % 2 == 0
    print('filter')
    t = perf_counter()
    filterDct = Dict.filter(evenKey, dct)
    elapsed = perf_counter() - t
    printRate(elapsed)
    outLst = Dict.toList(filterDct)
    assert list(outLst) == [(n, n*3) for n in sorted(lst) if n % 2 == 0]

    evenKey = lambda k, v: k % 2 == 0
    print('partition')
    t = perf_counter()
    (goodDict, badDict) = Dict.partition(evenKey, dct)
    elapsed = perf_counter() - t
    printRate(elapsed)
    goodList = Dict.toList(goodDict)
    badList = Dict.toList(badDict)
    assert list(goodList) == [(n, n*3) for n in sorted(lst) if n % 2 == 0]
    assert list(badList) == [(n, n*3) for n in sorted(lst) if n % 2 != 0]

def runBenchmarks():
    counts = [
        1000,
        ]

    for n in counts:
        benchmark(n)

def testSetStuff():
    dct1 = Dict.fromList(List.toElm([
        (1, 10),
        (2, 20),
        (3, 30),
    ]))

    dct2 = Dict.fromList(List.toElm([
        (3, 300),
        (4, 400),
        (5, 500),
    ]))

    print('union')
    assert list(Dict.keys(Dict.union(dct1, dct2))) == [1,2,3,4,5]

    print('intersect')
    assert list(Dict.keys(Dict.intersect(dct1, dct2))) == [3]

    print('diff')
    assert list(Dict.keys(Dict.diff(dct1, dct2))) == [1,2]

    print('merge')
    outList = Dict.merge(
        lambda k, v, lst: List.cons((k, v), lst),
        lambda k, v1, v2, lst: List.cons((k, v1, v2), lst),
        lambda k, v, lst: List.cons((v, k), lst),
        dct1,
        dct2,
        List.empty)
    assert list(outList) == [ (500, 5), (400, 4), (3, 30, 300), (2, 20), (1, 10) ]

if __name__ == '__main__':
    testBasics()
    runBenchmarks()
    testSetStuff()
