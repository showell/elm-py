# Dict.py (code generated via elm-py)

from Custom import CustomType

import List
from List import *
from Maybe import *
from Basics import *
from Order import *

from Elm import (
    patternMatch,
    MatchParam,
    )

Any = MatchParam.Any
Val = MatchParam.Val
Var = MatchParam.Var
Type = MatchParam.Type
Nested = MatchParam.Nested


NColor = CustomType("NColor", "Red", "Black")
Red = NColor.Red
Black = NColor.Black

Dict = CustomType("Dict", "RBEmpty_elm_builtin", RBNode_elm_builtin=5)
RBEmpty_elm_builtin = Dict.RBEmpty_elm_builtin
RBNode_elm_builtin = Dict.RBNode_elm_builtin

def empty():
    return RBEmpty_elm_builtin


def get(targetKey, dict):
    _cv = dict

    res = patternMatch(_cv,
        Type(RBEmpty_elm_builtin))

    if res.match('Just'):
        return Nothing


    res = patternMatch(_cv,
        Type(RBNode_elm_builtin),
        Any,
        Var('key'),
        Var('value'),
        Var('left'),
        Var('right'))

    if res.match('Just'):
        key = res.val['key']
        value = res.val['value']
        left = res.val['left']
        right = res.val['right']
        _cv = compare(targetKey, key)

        res = patternMatch(_cv,
            Type(LT))

        if res.match('Just'):
            return get(targetKey, left)


        res = patternMatch(_cv,
            Type(EQ))

        if res.match('Just'):
            return Just(value)


        res = patternMatch(_cv,
            Type(GT))

        if res.match('Just'):
            return get(targetKey, right)


def member(key, dict):
    _cv = get(key, dict)

    res = patternMatch(_cv,
        Type(Just),
        Any)

    if res.match('Just'):
        return True


    res = patternMatch(_cv,
        Type(Nothing))

    if res.match('Just'):
        return False


def size(dict):
    return sizeHelp(0, dict)


def sizeHelp(n, dict):
    _cv = dict

    res = patternMatch(_cv,
        Type(RBEmpty_elm_builtin))

    if res.match('Just'):
        return n


    res = patternMatch(_cv,
        Type(RBNode_elm_builtin),
        Any,
        Any,
        Any,
        Var('left'),
        Var('right'))

    if res.match('Just'):
        left = res.val['left']
        right = res.val['right']
        return sizeHelp((sizeHelp((n + 1), right)), left)


def isEmpty(dict):
    _cv = dict

    res = patternMatch(_cv,
        Type(RBEmpty_elm_builtin))

    if res.match('Just'):
        return True


    res = patternMatch(_cv,
        Type(RBNode_elm_builtin),
        Any,
        Any,
        Any,
        Any,
        Any)

    if res.match('Just'):
        return False


def insert(key, value, dict):
    _cv = insertHelp(key, value, dict)

    res = patternMatch(_cv,
        Type(RBNode_elm_builtin),
        Val(Red),
        Var('k'),
        Var('v'),
        Var('l'),
        Var('r'))

    if res.match('Just'):
        k = res.val['k']
        v = res.val['v']
        l = res.val['l']
        r = res.val['r']
        return RBNode_elm_builtin(Black, k, v, l, r)


    x = _cv
    return x


def insertHelp(key, value, dict):
    _cv = dict

    res = patternMatch(_cv,
        Type(RBEmpty_elm_builtin))

    if res.match('Just'):
        return RBNode_elm_builtin(Red, key, value, RBEmpty_elm_builtin, RBEmpty_elm_builtin)


    res = patternMatch(_cv,
        Type(RBNode_elm_builtin),
        Var('nColor'),
        Var('nKey'),
        Var('nValue'),
        Var('nLeft'),
        Var('nRight'))

    if res.match('Just'):
        nColor = res.val['nColor']
        nKey = res.val['nKey']
        nValue = res.val['nValue']
        nLeft = res.val['nLeft']
        nRight = res.val['nRight']
        _cv = compare(key, nKey)

        res = patternMatch(_cv,
            Type(LT))

        if res.match('Just'):
            return balance(nColor, nKey, nValue, (insertHelp(key, value, nLeft)), nRight)


        res = patternMatch(_cv,
            Type(EQ))

        if res.match('Just'):
            return RBNode_elm_builtin(nColor, nKey, value, nLeft, nRight)


        res = patternMatch(_cv,
            Type(GT))

        if res.match('Just'):
            return balance(nColor, nKey, nValue, nLeft, (insertHelp(key, value, nRight)))


def balance(color, key, value, left, right):
    _cv = right

    res = patternMatch(_cv,
        Type(RBNode_elm_builtin),
        Val(Red),
        Var('rK'),
        Var('rV'),
        Var('rLeft'),
        Var('rRight'))

    if res.match('Just'):
        rK = res.val['rK']
        rV = res.val['rV']
        rLeft = res.val['rLeft']
        rRight = res.val['rRight']
        _cv = left

        res = patternMatch(_cv,
            Type(RBNode_elm_builtin),
            Val(Red),
            Var('lK'),
            Var('lV'),
            Var('lLeft'),
            Var('lRight'))

        if res.match('Just'):
            lK = res.val['lK']
            lV = res.val['lV']
            lLeft = res.val['lLeft']
            lRight = res.val['lRight']
            return RBNode_elm_builtin(Red, key, value, (RBNode_elm_builtin(Black, lK, lV, lLeft, lRight)), (RBNode_elm_builtin(Black, rK, rV, rLeft, rRight)))


        return RBNode_elm_builtin(color, rK, rV, (RBNode_elm_builtin(Red, key, value, left, rLeft)), rRight)


    _cv = left

    res = patternMatch(_cv,
        Type(RBNode_elm_builtin),
        Val(Red),
        Var('lK'),
        Var('lV'),
        Nested([
            Type(RBNode_elm_builtin),
            Val(Red),
            Var('llK'),
            Var('llV'),
            Var('llLeft'),
            Var('llRight')]),
        Var('lRight'))

    if res.match('Just'):
        lK = res.val['lK']
        lV = res.val['lV']
        lRight = res.val['lRight']
        return RBNode_elm_builtin(Red, lK, lV, (RBNode_elm_builtin(Black, llK, llV, llLeft, llRight)), (RBNode_elm_builtin(Black, key, value, lRight, right)))


    return RBNode_elm_builtin(color, key, value, left, right)


def remove(key, dict):
    _cv = removeHelp(key, dict)

    res = patternMatch(_cv,
        Type(RBNode_elm_builtin),
        Val(Red),
        Var('k'),
        Var('v'),
        Var('l'),
        Var('r'))

    if res.match('Just'):
        k = res.val['k']
        v = res.val['v']
        l = res.val['l']
        r = res.val['r']
        return RBNode_elm_builtin(Black, k, v, l, r)


    x = _cv
    return x


def removeHelp(targetKey, dict):
    _cv = dict

    res = patternMatch(_cv,
        Type(RBEmpty_elm_builtin))

    if res.match('Just'):
        return RBEmpty_elm_builtin


    res = patternMatch(_cv,
        Type(RBNode_elm_builtin),
        Var('color'),
        Var('key'),
        Var('value'),
        Var('left'),
        Var('right'))

    if res.match('Just'):
        color = res.val['color']
        key = res.val['key']
        value = res.val['value']
        left = res.val['left']
        right = res.val['right']
        if targetKey < key:
            _cv = left

            res = patternMatch(_cv,
                Type(RBNode_elm_builtin),
                Val(Black),
                Any,
                Any,
                Var('lLeft'),
                Any)

            if res.match('Just'):
                lLeft = res.val['lLeft']
                _cv = lLeft

                res = patternMatch(_cv,
                    Type(RBNode_elm_builtin),
                    Val(Red),
                    Any,
                    Any,
                    Any,
                    Any)

                if res.match('Just'):
                    return RBNode_elm_builtin(color, key, value, (removeHelp(targetKey, left)), right)


                _cv = moveRedLeft(dict)

                res = patternMatch(_cv,
                    Type(RBNode_elm_builtin),
                    Var('nColor'),
                    Var('nKey'),
                    Var('nValue'),
                    Var('nLeft'),
                    Var('nRight'))

                if res.match('Just'):
                    nColor = res.val['nColor']
                    nKey = res.val['nKey']
                    nValue = res.val['nValue']
                    nLeft = res.val['nLeft']
                    nRight = res.val['nRight']
                    return balance(nColor, nKey, nValue, (removeHelp(targetKey, nLeft)), nRight)


                res = patternMatch(_cv,
                    Type(RBEmpty_elm_builtin))

                if res.match('Just'):
                    return RBEmpty_elm_builtin


            return RBNode_elm_builtin(color, key, value, (removeHelp(targetKey, left)), right)
        else:
            return removeHelpEQGT(targetKey, (removeHelpPrepEQGT(targetKey, dict, color, key, value, left, right)))


def removeHelpPrepEQGT(targetKey, dict, color, key, value, left, right):
    _cv = left

    res = patternMatch(_cv,
        Type(RBNode_elm_builtin),
        Val(Red),
        Var('lK'),
        Var('lV'),
        Var('lLeft'),
        Var('lRight'))

    if res.match('Just'):
        lK = res.val['lK']
        lV = res.val['lV']
        lLeft = res.val['lLeft']
        lRight = res.val['lRight']
        return RBNode_elm_builtin(color, lK, lV, lLeft, (RBNode_elm_builtin(Red, key, value, lRight, right)))


    _cv = right

    res = patternMatch(_cv,
        Type(RBNode_elm_builtin),
        Val(Black),
        Any,
        Any,
        Nested([
            Type(RBNode_elm_builtin),
            Val(Black),
            Any,
            Any,
            Any,
            Any]),
        Any)

    if res.match('Just'):
        return moveRedRight(dict)


    res = patternMatch(_cv,
        Type(RBNode_elm_builtin),
        Val(Black),
        Any,
        Any,
        Val(RBEmpty_elm_builtin),
        Any)

    if res.match('Just'):
        return moveRedRight(dict)


    return dict


def removeHelpEQGT(targetKey, dict):
    _cv = dict

    res = patternMatch(_cv,
        Type(RBNode_elm_builtin),
        Var('color'),
        Var('key'),
        Var('value'),
        Var('left'),
        Var('right'))

    if res.match('Just'):
        color = res.val['color']
        key = res.val['key']
        value = res.val['value']
        left = res.val['left']
        right = res.val['right']
        if targetKey == key:
            _cv = getMin(right)

            res = patternMatch(_cv,
                Type(RBNode_elm_builtin),
                Any,
                Var('minKey'),
                Var('minValue'),
                Any,
                Any)

            if res.match('Just'):
                minKey = res.val['minKey']
                minValue = res.val['minValue']
                return balance(color, minKey, minValue, left, (removeMin(right)))


            res = patternMatch(_cv,
                Type(RBEmpty_elm_builtin))

            if res.match('Just'):
                return RBEmpty_elm_builtin
        else:
            return balance(color, key, value, left, (removeHelp(targetKey, right)))


    res = patternMatch(_cv,
        Type(RBEmpty_elm_builtin))

    if res.match('Just'):
        return RBEmpty_elm_builtin


def getMin(dict):
    _cv = dict

    res = patternMatch(_cv,
        Type(RBNode_elm_builtin),
        Any,
        Any,
        Any,
        (AsVar(
            Type(RBNode_elm_builtin),
            Any,
            Any,
            Any,
            Any,
            Any, left)),
        Any)

    if res.match('Just'):
        return getMin(left)


    return dict


def removeMin(dict):
    _cv = dict

    res = patternMatch(_cv,
        Type(RBNode_elm_builtin),
        Var('color'),
        Var('key'),
        Var('value'),
        (AsVar(
            Type(RBNode_elm_builtin),
            Var('lColor'),
            Any,
            Any,
            Var('lLeft'),
            Any, left)),
        Var('right'))

    if res.match('Just'):
        color = res.val['color']
        key = res.val['key']
        value = res.val['value']
        right = res.val['right']
        _cv = lColor

        res = patternMatch(_cv,
            Type(Black))

        if res.match('Just'):
            _cv = lLeft

            res = patternMatch(_cv,
                Type(RBNode_elm_builtin),
                Val(Red),
                Any,
                Any,
                Any,
                Any)

            if res.match('Just'):
                return RBNode_elm_builtin(color, key, value, (removeMin(left)), right)


            _cv = moveRedLeft(dict)

            res = patternMatch(_cv,
                Type(RBNode_elm_builtin),
                Var('nColor'),
                Var('nKey'),
                Var('nValue'),
                Var('nLeft'),
                Var('nRight'))

            if res.match('Just'):
                nColor = res.val['nColor']
                nKey = res.val['nKey']
                nValue = res.val['nValue']
                nLeft = res.val['nLeft']
                nRight = res.val['nRight']
                return balance(nColor, nKey, nValue, (removeMin(nLeft)), nRight)


            res = patternMatch(_cv,
                Type(RBEmpty_elm_builtin))

            if res.match('Just'):
                return RBEmpty_elm_builtin


        return RBNode_elm_builtin(color, key, value, (removeMin(left)), right)


    return RBEmpty_elm_builtin


def moveRedLeft(dict):
    _cv = dict

    res = patternMatch(_cv,
        Type(RBNode_elm_builtin),
        Var('clr'),
        Var('k'),
        Var('v'),
        Nested([
            Type(RBNode_elm_builtin),
            Var('lClr'),
            Var('lK'),
            Var('lV'),
            Var('lLeft'),
            Var('lRight')]),
        Nested([
            Type(RBNode_elm_builtin),
            Var('rClr'),
            Var('rK'),
            Var('rV'),
            (AsVar(
                Type(RBNode_elm_builtin),
                Val(Red),
                Var('rlK'),
                Var('rlV'),
                Var('rlL'),
                Var('rlR'), rLeft)),
            Var('rRight')]))

    if res.match('Just'):
        clr = res.val['clr']
        k = res.val['k']
        v = res.val['v']
        return RBNode_elm_builtin(Red, rlK, rlV, (RBNode_elm_builtin(Black, k, v, (RBNode_elm_builtin(Red, lK, lV, lLeft, lRight)), rlL)), (RBNode_elm_builtin(Black, rK, rV, rlR, rRight)))


    res = patternMatch(_cv,
        Type(RBNode_elm_builtin),
        Var('clr'),
        Var('k'),
        Var('v'),
        Nested([
            Type(RBNode_elm_builtin),
            Var('lClr'),
            Var('lK'),
            Var('lV'),
            Var('lLeft'),
            Var('lRight')]),
        Nested([
            Type(RBNode_elm_builtin),
            Var('rClr'),
            Var('rK'),
            Var('rV'),
            Var('rLeft'),
            Var('rRight')]))

    if res.match('Just'):
        clr = res.val['clr']
        k = res.val['k']
        v = res.val['v']
        _cv = clr

        res = patternMatch(_cv,
            Type(Black))

        if res.match('Just'):
            return RBNode_elm_builtin(Black, k, v, (RBNode_elm_builtin(Red, lK, lV, lLeft, lRight)), (RBNode_elm_builtin(Red, rK, rV, rLeft, rRight)))


        res = patternMatch(_cv,
            Type(Red))

        if res.match('Just'):
            return RBNode_elm_builtin(Black, k, v, (RBNode_elm_builtin(Red, lK, lV, lLeft, lRight)), (RBNode_elm_builtin(Red, rK, rV, rLeft, rRight)))


    return dict


def update(targetKey, alter, dictionary):
    _cv = alter((get(targetKey, dictionary)))

    res = patternMatch(_cv,
        Type(Just),
        Var('value'))

    if res.match('Just'):
        value = res.val['value']
        return insert(targetKey, value, dictionary)


    res = patternMatch(_cv,
        Type(Nothing))

    if res.match('Just'):
        return remove(targetKey, dictionary)


def singleton(key, value):
    return RBNode_elm_builtin(Black, key, value, RBEmpty_elm_builtin, RBEmpty_elm_builtin)


def union(t1, t2):
    return foldl(insert, t2, t1)


def intersect(t1, t2):
    def _anon1(k, _):
        return member(k, t2)

    return filter(_anon1, t1)


def diff(t1, t2):
    def _anon1(k, v, t):
        return remove(k, t)

    return foldl(_anon1, t1, t2)


def map(func, dict):
    _cv = dict

    res = patternMatch(_cv,
        Type(RBEmpty_elm_builtin))

    if res.match('Just'):
        return RBEmpty_elm_builtin


    res = patternMatch(_cv,
        Type(RBNode_elm_builtin),
        Var('color'),
        Var('key'),
        Var('value'),
        Var('left'),
        Var('right'))

    if res.match('Just'):
        color = res.val['color']
        key = res.val['key']
        value = res.val['value']
        left = res.val['left']
        right = res.val['right']
        return RBNode_elm_builtin(color, key, (func(key, value)), (map(func, left)), (map(func, right)))


def foldl(func, acc, dict):
    _cv = dict

    res = patternMatch(_cv,
        Type(RBEmpty_elm_builtin))

    if res.match('Just'):
        return acc


    res = patternMatch(_cv,
        Type(RBNode_elm_builtin),
        Any,
        Var('key'),
        Var('value'),
        Var('left'),
        Var('right'))

    if res.match('Just'):
        key = res.val['key']
        value = res.val['value']
        left = res.val['left']
        right = res.val['right']
        return foldl(func, (func(key, value, (foldl(func, acc, left)))), right)


def foldr(func, acc, t):
    _cv = t

    res = patternMatch(_cv,
        Type(RBEmpty_elm_builtin))

    if res.match('Just'):
        return acc


    res = patternMatch(_cv,
        Type(RBNode_elm_builtin),
        Any,
        Var('key'),
        Var('value'),
        Var('left'),
        Var('right'))

    if res.match('Just'):
        key = res.val['key']
        value = res.val['value']
        left = res.val['left']
        right = res.val['right']
        return foldr(func, (func(key, value, (foldr(func, acc, right)))), left)


def partition(isGood, dict):
    def add(*args):
        key, value, (t1, t2) = args

        if isGood(key, value):
            return (insert(key, value, t1), t2)
        else:
            return (t1, insert(key, value, t2))


    return foldl(add, (empty, empty), dict)


def keys(dict):
    def _anon1(key, value, keyList):
        return List.cons(key, keyList)

    return foldr(_anon1, List.toElm([]), dict)


def values(dict):
    def _anon1(key, value, valueList):
        return List.cons(value, valueList)

    return foldr(_anon1, List.toElm([]), dict)


def toList(dict):
    def _anon1(key, value, list):
        return List.cons((key, value), list)

    return foldr(_anon1, List.toElm([]), dict)


def fromList(assocs):
    def _anon1(*args):
        (key, value), dict = args

        return insert(key, value, dict)

    return List.foldl(_anon1, empty, assocs)


def filter(isGood, dict):
    def _anon1(k, v, d):
        if isGood(k, v):
            return insert(k, v, d)
        else:
            return d

    return foldl(_anon1, empty, dict)


def merge(leftStep, bothStep, rightStep, leftDict, rightDict, initialResult):
    def stepState(*args):
        rKey, rValue, (list, result) = args

        _cv = list

        res = patternMatch(_cv,List.toElm([]))

        if res.match('Just'):
            return (list, rightStep(rKey, rValue, result))


        res = patternMatch(_cv,Cons((Var('lKey'), Var('lValue')), Var('rest')))

        if res.match('Just'):
            if lKey < rKey:
                return stepState(rKey, rValue, (rest, leftStep(lKey, lValue, result)))
            else:
                if lKey > rKey:
                    return (list, rightStep(rKey, rValue, result))
                else:
                    return (rest, bothStep(lKey, lValue, rValue, result))



    (leftovers, intermediateResult) = (
        foldl(stepState, (toList(leftDict), initialResult), rightDict)
    )

    def _anon1(*args):
        (k, v), result = args

        return leftStep(k, v, result)

    return List.foldl(_anon1, intermediateResult, leftovers)


def moveRedRight(dict):
    _cv = dict

    res = patternMatch(_cv,
        Type(RBNode_elm_builtin),
        Var('clr'),
        Var('k'),
        Var('v'),
        Nested([
            Type(RBNode_elm_builtin),
            Var('lClr'),
            Var('lK'),
            Var('lV'),
            Nested([
                Type(RBNode_elm_builtin),
                Val(Red),
                Var('llK'),
                Var('llV'),
                Var('llLeft'),
                Var('llRight')]),
            Var('lRight')]),
        Nested([
            Type(RBNode_elm_builtin),
            Var('rClr'),
            Var('rK'),
            Var('rV'),
            Var('rLeft'),
            Var('rRight')]))

    if res.match('Just'):
        clr = res.val['clr']
        k = res.val['k']
        v = res.val['v']
        return RBNode_elm_builtin(Red, lK, lV, (RBNode_elm_builtin(Black, llK, llV, llLeft, llRight)), (RBNode_elm_builtin(Black, k, v, lRight, (RBNode_elm_builtin(Red, rK, rV, rLeft, rRight)))))


    res = patternMatch(_cv,
        Type(RBNode_elm_builtin),
        Var('clr'),
        Var('k'),
        Var('v'),
        Nested([
            Type(RBNode_elm_builtin),
            Var('lClr'),
            Var('lK'),
            Var('lV'),
            Var('lLeft'),
            Var('lRight')]),
        Nested([
            Type(RBNode_elm_builtin),
            Var('rClr'),
            Var('rK'),
            Var('rV'),
            Var('rLeft'),
            Var('rRight')]))

    if res.match('Just'):
        clr = res.val['clr']
        k = res.val['k']
        v = res.val['v']
        _cv = clr

        res = patternMatch(_cv,
            Type(Black))

        if res.match('Just'):
            return RBNode_elm_builtin(Black, k, v, (RBNode_elm_builtin(Red, lK, lV, lLeft, lRight)), (RBNode_elm_builtin(Red, rK, rV, rLeft, rRight)))


        res = patternMatch(_cv,
            Type(Red))

        if res.match('Just'):
            return RBNode_elm_builtin(Black, k, v, (RBNode_elm_builtin(Red, lK, lV, lLeft, lRight)), (RBNode_elm_builtin(Red, rK, rV, rLeft, rRight)))


    return dict


