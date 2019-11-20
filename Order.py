EQ = 'EQ'
LT = 'LT'
GT = 'GT'

def toInt(ord):
    if ord == LT:
        return -1
    elif ord == EQ:
        return 0
    else:
        return 1

def fromInt(n):
    if n < 0:
        return LT
    elif n == 0:
        return EQ
    else:
        return GT


