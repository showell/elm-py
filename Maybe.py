def Just(val):
    return ('Just', val)

def Nothing():
    return None

def unboxJust(val):
    if val[0] != 'Just':
        raise Exception('illegal unboxing')

    return val[1]
