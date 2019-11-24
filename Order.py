from Custom import CustomType

Order = CustomType('Order', 'EQ', 'LT', 'GT')

EQ = Order.EQ
LT = Order.LT
GT = Order.GT

def orderToInt(order):
    if order == LT:
        return -1

    if order == EQ:
        return 0

    if order == GT:
        return 1

    raise Exception('unhandled value')

def toOrder(a, b):
    if a < b:
        return LT

    if a == b:
        return EQ

    return GT


