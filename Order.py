from Custom import CustomType

Order = CustomType('Order', 'EQ', 'LT', 'GT')

def orderToInt(order):
    if order == Order.LT:
        return -1

    if order == Order.EQ:
        return 0

    if order == Order.GT:
        return 1

    raise Exception('unhandled value')

def toOrder(a, b):
    if a < b:
        return Order.LT

    if a == b:
        return Order.EQ

    return Order.GT


