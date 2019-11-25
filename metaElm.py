
from Kernel import (
    toElm,
    toPy,
    )
from Elm import F, pipe
import Basics
import Bool
import List
import Maybe
import Order
import Tuple



# This code was automatically generated from here:
# https://github.com/showell/meta-elm/blob/master/src/MeExample.elm
#
# The Python functions were emitted from meta-elm ASTs.

def test(funcName, f, arg, expected):
    result = f(toElm(arg))
    assert result == expected
    print('pass: ', funcName)


# a1a1f2 =
#     \n -> (\x y -> (x * 10) + y) 1 n

def a1a1f2(n):
    return \
        F(F(lambda x, y:
            ((x * 10) + y)
        )(
            1
        ))(
            n
        )

test(
    'a1a1f2',
    a1a1f2,
    2,
    12
)


# a1a1a1f3 =
#     \n ->
#         (\x y z -> (x * 100) + ((y * 10) + z)
#         )
#             1
#             2
#             n

def a1a1a1f3(n):
    return \
        F(F(F(lambda x, y, z:
            ((x * 100) + ((y * 10) + z))
        )(
            1
        ))(
            2
        ))(
            n
        )

test(
    'a1a1a1f3',
    a1a1a1f3,
    3,
    123
)


# all =
#     \lst -> List.all (\x -> 1 == x) lst

def all(lst):
    return \
        F(List.all)(
            lambda x:
                toElm(1 == x)
            ,
            lst
        )

test(
    'all',
    all,
    [1, 1, 1],
    Bool.true
)


test(
    'all',
    all,
    [1, 1, 3],
    Bool.false
)


# any =
#     \lst -> List.any (\x -> 4 == x) lst

def any(lst):
    return \
        F(List.any)(
            lambda x:
                toElm(4 == x)
            ,
            lst
        )

test(
    'any',
    any,
    [1, 2, 3],
    Bool.false
)


test(
    'any',
    any,
    [1, 4, 3],
    Bool.true
)


# basicTupleStuff =
#     \n -> ( 5, 2 + 4 )

def basicTupleStuff(n):
    return \
        Tuple.toElm(( 5, (2 + 4) ))

test(
    'basicTupleStuff',
    basicTupleStuff,
    5,
    Tuple.toElm(( 5, 6 ))
)


# basicListStuff =
#     \n -> [ 5, 2 + 4, n + 100 ]

def basicListStuff(n):
    return \
        List.toElm([ 5, (2 + 4)
        , (n + 100) ])

test(
    'basicListStuff',
    basicListStuff,
    5,
    List.toElm([ 5, 6, 105 ])
)


# compare =
#     \n -> Basics.compare 2 n

def compare(n):
    return \
        F(Basics.compare)(
            2,
            n
        )

test(
    'compare',
    compare,
    1,
    Order.GT
)


test(
    'compare',
    compare,
    2,
    Order.EQ
)


test(
    'compare',
    compare,
    3,
    Order.LT
)


# concat =
#     \lst -> List.concat lst

def concat(lst):
    return \
        F(List.concat)(
            lst
        )

test(
    'concat',
    concat,
    [ [1,2,3], [4,5,6], [7,8]],
    List.toElm([ 1, 2, 3, 4, 5, 6, 7, 8 ])
)


# concatMap =
#     \lst ->
#         List.concatMap
#             List.map (\n -> n * 5)
#             lst

def concatMap(lst):
    return \
        F(List.concatMap)(
            F(List.map)(
                lambda n:
                    (n * 5)
                
            ),
            lst
        )

test(
    'concatMap',
    concatMap,
    [ [1,2,3], [4,5,6], [7,8]],
    List.toElm([ 5, 10, 15, 20, 25, 30, 35, 40 ])
)


# drop =
#     \lst -> List.drop 2 lst

def drop(lst):
    return \
        F(List.drop)(
            2,
            lst
        )

test(
    'drop',
    drop,
    [],
    List.toElm([  ])
)


test(
    'drop',
    drop,
    [1, 2, 3],
    List.toElm([ 3 ])
)


# f4Test =
#     \n ->
#         (\a b c d -> (a + b) * (c + d))
#             1
#             2
#             3
#             n

def f4Test(n):
    return \
        F(lambda a, b, c, d:
            ((a + b) * (c + d))
        )(
            1,
            2,
            3,
            n
        )

test(
    'f4Test',
    f4Test,
    4,
    21
)


# f5Test =
#     \n ->
#         (\a b c d e ->
#             Tuple.pair
#                 a
#                 Tuple.pair
#                     b
#                     Tuple.pair
#                         c
#                         Tuple.pair d e
#         )
#             1
#             2
#             3
#             4
#             n

def f5Test(n):
    return \
        F(lambda a, b, c, d, e:
            F(Tuple.pair)(
                a,
                F(Tuple.pair)(
                    b,
                    F(Tuple.pair)(
                        c,
                        F(Tuple.pair)(
                            d,
                            e
                        )
                    )
                )
            )
        )(
            1,
            2,
            3,
            4,
            n
        )

test(
    'f5Test',
    f5Test,
    5,
    Tuple.toElm(( 1, Tuple.toElm(( 2, Tuple.toElm(( 3, Tuple.toElm(( 4, 5 )) )) )) ))
)


# factorial =
#     \n ->
#         if n == 0 then
#             1
# 
#         else
#             n * factorial (n - 1)

def factorial(n):
    return \
        (1
        if
            toPy(toElm(n == 0))
        else
            (n * (factorial)(
                (n - 1)
            )))

test(
    'factorial',
    factorial,
    17,
    355687428096000
)


# factorial2 =
#     \n -> List.range 1 n |> List.foldl (*) 1

def factorial2(n):
    return \
        pipe(F(List.range)(
            1,
            n
        ),
        [
            F(List.foldl)(
                lambda a, b: a * b,
                1
            )
        ])
        

test(
    'factorial2',
    factorial2,
    11,
    39916800
)


# filter =
#     \lst -> lst |> List.filter (\x -> x == 4)

def filter(lst):
    return \
        pipe(lst,
        [
            F(List.filter)(
                lambda x:
                    toElm(x == 4)
                
            )
        ])
        

test(
    'filter',
    filter,
    [ 4, 1, 2, 3, 4, 7, 4 ],
    List.toElm([ 4, 4, 4 ])
)


# filterMap =
#     \lst -> List.filterMap List.head lst

def filterMap(lst):
    return \
        F(List.filterMap)(
            List.head,
            lst
        )

test(
    'filterMap',
    filterMap,
    [ [1], [], [2], [], [3] ],
    List.toElm([ 1, 2, 3 ])
)


# foldr =
#     \lst -> lst |> List.foldr List.cons []

def foldr(lst):
    return \
        pipe(lst,
        [
            F(List.foldr)(
                List.cons,
                List.toElm([  ])
            )
        ])
        

test(
    'foldr',
    foldr,
    [ 1, 2, 3],
    List.toElm([ 1, 2, 3 ])
)


# head =
#     \lst -> List.head lst

def head(lst):
    return \
        F(List.head)(
            lst
        )

test(
    'head',
    head,
    [],
    Maybe.Nothing
)


test(
    'head',
    head,
    [1, 2, 3],
    Maybe.Just(1)
)


# incr =
#     \n -> (\x -> x + 1) n

def incr(n):
    return \
        F(lambda x:
            (x + 1)
        )(
            n
        )

test(
    'incr',
    incr,
    8,
    9
)


# intersperse =
#     \n -> List.intersperse n [ 1, 2, 3, 4 ]

def intersperse(n):
    return \
        F(List.intersperse)(
            n,
            List.toElm([ 1, 2, 3, 4 ])
        )

test(
    'intersperse',
    intersperse,
    999,
    List.toElm([ 1, 999, 2, 999, 3, 999, 4 ])
)


# isEmpty =
#     \lst -> List.isEmpty lst

def isEmpty(lst):
    return \
        F(List.isEmpty)(
            lst
        )

test(
    'isEmpty',
    isEmpty,
    [],
    Bool.true
)


test(
    'isEmpty',
    isEmpty,
    [1, 2],
    Bool.false
)


# length =
#     \lst -> List.length lst

def length(lst):
    return \
        F(List.length)(
            lst
        )

test(
    'length',
    length,
    [1, 2, 3],
    3
)


# map2 =
#     \lst ->
#         lst
#             |> List.map2
#                 List.range
#                 [ 1, 2, 3 ]

def map2(lst):
    return \
        pipe(lst,
        [
            F(List.map2)(
                List.range,
                List.toElm([ 1, 2, 3 ])
            )
        ])
        

test(
    'map2',
    map2,
    [8, 7, 9],
    List.toElm([ List.toElm([ 1, 2, 3, 4, 5, 6, 7, 8 ])
    , List.toElm([ 2, 3, 4, 5, 6, 7 ])
    , List.toElm([ 3, 4, 5, 6, 7, 8, 9 ]) ])
)


# map2Pythag =
#     \lst ->
#         lst
#             |> List.map2
#                 (\x y -> (x * x) + (y * y))
#                 [ 3, 5, 7 ]

def map2Pythag(lst):
    return \
        pipe(lst,
        [
            F(List.map2)(
                lambda x, y:
                    ((x * x) + (y * y))
                ,
                List.toElm([ 3, 5, 7 ])
            )
        ])
        

test(
    'map2Pythag',
    map2Pythag,
    [4, 12, 24],
    List.toElm([ 25, 169, 625 ])
)


# map3 =
#     \lst ->
#         lst
#             |> List.map3
#                 (\x y z ->
#                     (x * 100)
#                         + ((y * 10) + z)
#                 )
#                 [ 10, 20, 30 ]
#                 [ 5, 8, 7 ]

def map3(lst):
    return \
        pipe(lst,
        [
            F(List.map3)(
                lambda x, y, z:
                    ((x * 100) + ((y * 10) + z))
                ,
                List.toElm([ 10, 20, 30 ]),
                List.toElm([ 5, 8, 7 ])
            )
        ])
        

test(
    'map3',
    map3,
    [8, 7, 9],
    List.toElm([ 1058, 2087, 3079 ])
)


# map4 =
#     \lst ->
#         lst
#             |> List.map4
#                 (\a b c d ->
#                     (a + b) * (c + d)
#                 )
#                 [ 10, 20, 30 ]
#                 [ 5, 8, 7 ]
#                 [ 1, 2 ]

def map4(lst):
    return \
        pipe(lst,
        [
            F(List.map4)(
                lambda a, b, c, d:
                    ((a + b) * (c + d))
                ,
                List.toElm([ 10, 20, 30 ]),
                List.toElm([ 5, 8, 7 ]),
                List.toElm([ 1, 2 ])
            )
        ])
        

test(
    'map4',
    map4,
    [1, 3, 19, 22],
    List.toElm([ 30, 140 ])
)


# map5 =
#     \lst ->
#         lst
#             |> List.map5
#                 (\a b c d e ->
#                     Tuple.pair
#                         a
#                         Tuple.pair
#                             b
#                             Tuple.pair
#                                 c
#                                 Tuple.pair
#                                     d
#                                     e
#                 )
#                 [ 10, 20, 30 ]
#                 [ 5, 8, 7 ]
#                 [ 1, 2, 3, 4, 5 ]
#                 [ 33, 97, 103 ]

def map5(lst):
    return \
        pipe(lst,
        [
            F(List.map5)(
                lambda a, b, c, d, e:
                    F(Tuple.pair)(
                        a,
                        F(Tuple.pair)(
                            b,
                            F(Tuple.pair)(
                                c,
                                F(Tuple.pair)(
                                    d,
                                    e
                                )
                            )
                        )
                    )
                ,
                List.toElm([ 10, 20, 30 ]),
                List.toElm([ 5, 8, 7 ]),
                List.toElm([ 1, 2, 3, 4, 5 ]),
                List.toElm([ 33, 97, 103 ])
            )
        ])
        

test(
    'map5',
    map5,
    [5, 10, 15, 20],
    List.toElm([ Tuple.toElm(( 10, Tuple.toElm(( 5, Tuple.toElm(( 1, Tuple.toElm(( 33, 5 )) )) )) ))
    , Tuple.toElm(( 20, Tuple.toElm(( 8, Tuple.toElm(( 2, Tuple.toElm(( 97, 10 )) )) )) ))
    , Tuple.toElm(( 30, Tuple.toElm(( 7, Tuple.toElm(( 3, Tuple.toElm(( 103, 15 )) )) )) )) ])
)


# maximum =
#     \lst -> List.maximum lst

def maximum(lst):
    return \
        F(List.maximum)(
            lst
        )

test(
    'maximum',
    maximum,
    [],
    Maybe.Nothing
)


test(
    'maximum',
    maximum,
    [40, 10, 30, 20],
    Maybe.Just(40)
)


# member =
#     \lst -> List.member 42 lst

def member(lst):
    return \
        F(List.member)(
            42,
            lst
        )

test(
    'member',
    member,
    [41, 42, 43],
    Bool.true
)


# minimum =
#     \lst -> List.minimum lst

def minimum(lst):
    return \
        F(List.minimum)(
            lst
        )

test(
    'minimum',
    minimum,
    [],
    Maybe.Nothing
)


test(
    'minimum',
    minimum,
    [40, 10, 30, 20],
    Maybe.Just(10)
)


# partition =
#     \lst ->
#         List.partition
#             (\n -> Basics.modBy 2 n == 0)
#             lst

def partition(lst):
    return \
        F(List.partition)(
            lambda n:
                toElm(F(Basics.modBy)(
                    2,
                    n
                ) == 0)
            ,
            lst
        )

test(
    'partition',
    partition,
    [1, 2, 3, 4, 5, 6, 7],
    Tuple.toElm(( List.toElm([ 2, 4, 6 ]), List.toElm([ 1, 3, 5, 7 ]) ))
)


# permuteFloats =
#     \lst ->
#         let
#             startList =
#                 lst
#                     |> List.map
#                         Basics.toFloat
# 
#             newElements =
#                 startList
#                     |> List.sort
#                     |> List.map
#                         (\n -> n + 0.5)
#                     |> (\items ->
#                             0.5 :: items
#                        )
#         in
#         newElements
#             |> List.map List.singleton
#             |> List.map
#                 (\x -> startList ++ x)

def permuteFloats(lst):
    startList = \
        pipe(lst,
        [
            F(List.map)(
                Basics.toFloat
            )
        ])
        
    
    newElements = \
        pipe(startList,
        [
            List.sort,
            F(List.map)(
                lambda n:
                    (n + 0.5)
                
            ),
            lambda items:
                List.cons(0.5, items)
            
        ])
        
    
    return pipe(newElements,
    [
        F(List.map)(
            List.singleton
        ),
        F(List.map)(
            lambda x:
                List.append(startList, x)
            
        )
    ])
    

test(
    'permuteFloats',
    permuteFloats,
    [ 4, 3, 2, 5, 1 ],
    List.toElm([ List.toElm([ 4, 3, 2, 5, 1, 0.5 ])
    , List.toElm([ 4, 3, 2, 5, 1, 1.5 ])
    , List.toElm([ 4, 3, 2, 5, 1, 2.5 ])
    , List.toElm([ 4, 3, 2, 5, 1, 3.5 ])
    , List.toElm([ 4, 3, 2, 5, 1, 4.5 ])
    , List.toElm([ 4, 3, 2, 5, 1, 5.5 ]) ])
)


# product =
#     \lst -> List.product lst

def product(lst):
    return \
        F(List.product)(
            lst
        )

test(
    'product',
    product,
    [1.2, 2.3, 3.8],
    10.488
)


# pythagTest =
#     \n -> (\x y -> (x * x) + (y * y)) 9 n

def pythagTest(n):
    return \
        F(lambda x, y:
            ((x * x) + (y * y))
        )(
            9,
            n
        )

test(
    'pythagTest',
    pythagTest,
    40,
    1681
)


# ranks =
#     \lst ->
#         lst
#             |> List.indexedMap Tuple.pair
#             |> List.sortBy Tuple.second
#             |> List.map Tuple.first
#             |> List.indexedMap Tuple.pair
#             |> List.sortBy Tuple.second
#             |> List.map Tuple.first
#             |> List.map (\n -> n + 1)

def ranks(lst):
    return \
        pipe(lst,
        [
            F(List.indexedMap)(
                Tuple.pair
            ),
            F(List.sortBy)(
                Tuple.second
            ),
            F(List.map)(
                Tuple.first
            ),
            F(List.indexedMap)(
                Tuple.pair
            ),
            F(List.sortBy)(
                Tuple.second
            ),
            F(List.map)(
                Tuple.first
            ),
            F(List.map)(
                lambda n:
                    (n + 1)
                
            )
        ])
        

test(
    'ranks',
    ranks,
    [ 40, 31, 59, 12, 27 ],
    List.toElm([ 4, 3, 5, 1, 2 ])
)


# repeat =
#     \n -> List.repeat n 42

def repeat(n):
    return \
        F(List.repeat)(
            n,
            42
        )

test(
    'repeat',
    repeat,
    5,
    List.toElm([ 42, 42, 42, 42, 42 ])
)


# reverse =
#     \lst -> List.reverse lst

def reverse(lst):
    return \
        F(List.reverse)(
            lst
        )

test(
    'reverse',
    reverse,
    [1, 2, 3],
    List.toElm([ 3, 2, 1 ])
)


# sortWith =
#     \lst ->
#         List.sortWith
#             (\a b ->
#                 Basics.compare
#                     (\n -> Basics.modBy 10 n)
#                         a
#                     (\n -> Basics.modBy 10 n)
#                         b
#             )
#             lst

def sortWith(lst):
    return \
        F(List.sortWith)(
            lambda a, b:
                F(Basics.compare)(
                    F(lambda n:
                        F(Basics.modBy)(
                            10,
                            n
                        )
                    )(
                        a
                    ),
                    F(lambda n:
                        F(Basics.modBy)(
                            10,
                            n
                        )
                    )(
                        b
                    )
                )
            ,
            lst
        )

test(
    'sortWith',
    sortWith,
    [53, 27, 11, 49, 82],
    List.toElm([ 11, 82, 53, 27, 49 ])
)


# sum =
#     \lst -> List.sum lst

def sum(lst):
    return \
        F(List.sum)(
            lst
        )

test(
    'sum',
    sum,
    [1.2, 2.3, 3.8],
    7.3
)


# tail =
#     \lst -> List.tail lst

def tail(lst):
    return \
        F(List.tail)(
            lst
        )

test(
    'tail',
    tail,
    [],
    Maybe.Nothing
)


test(
    'tail',
    tail,
    [1, 2, 3],
    Maybe.Just(List.toElm([ 2, 3 ]))
)


# take =
#     \lst -> List.take 2 lst

def take(lst):
    return \
        F(List.take)(
            2,
            lst
        )

test(
    'take',
    take,
    [],
    List.toElm([  ])
)


test(
    'take',
    take,
    [1, 2, 3],
    List.toElm([ 1, 2 ])
)


# unzip =
#     \lst ->
#         lst
#             |> List.map
#                 (\x -> Tuple.pair x (x * 3))
#             |> List.unzip

def unzip(lst):
    return \
        pipe(lst,
        [
            F(List.map)(
                lambda x:
                    F(Tuple.pair)(
                        x,
                        (x * 3)
                    )
                
            ),
            List.unzip
        ])
        

test(
    'unzip',
    unzip,
    [ 1, 2, 3, 4 ],
    Tuple.toElm(( List.toElm([ 1, 2, 3, 4 ]), List.toElm([ 3, 6, 9, 12 ]) ))
)

