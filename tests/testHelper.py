from Kernel import (
        toElm,
        toPy,
        )

def printList(xs):
    print(toPy(xs))

def assertTrue(actual):
    if actual == True:
        print('pass')
    else:
        print('\n\nFAIL!\n', actual)
        print('\n')
        raise AssertionError

def assertFalse(actual):
    if actual == False:
        print('pass')
    else:
        print('\n\nFAIL!\n', actual)
        print('\n')
        raise AssertionError

def assertFloat(actual, expected):
    if type(actual) == tuple:
        assert len(actual) == 2
        assert len(expected) == 2
        assertFloat(actual[0], expected[0])
        assertFloat(actual[1], expected[1])
        return

    if abs(actual - expected) < 0.000001:
        print('pass')
    else:
        print('\n\nFAIL!\n', actual, expected)
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

