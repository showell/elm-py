class Custom:
    def __init__(self, typeClass, vtype, arity, *vals):
        if type(typeClass) != CustomType:
            raise Exception('illegal typeClass for variant')

        if arity != len(vals):
            raise Exception('wrong number of vals')

        self.typeName = typeClass.name
        self.vals = vals

        if arity == 1:
            self.val = vals[0]

        self.vtype = vtype
        self.arity = arity

    def match(self, vtype):
        return self.vtype == vtype

    def isType(self, typeName):
        return self.typeName == typeName

    def __eq__(self, other):
        if self.typeName != other.typeName:
            raise Exception('illegal comparison')

        if self.vtype != other.vtype:
            return False

        if self.arity == 0:
            return True

        if self.arity == 1:
            return self.val == other.val

        return self.vals == other.vals

    def __str__(self):
        if self.arity == 0:
            return self.vtype

        if self.arity == 1:
            return self.vtype + ' ' + str(self.val)

        return self.vtype + ' ' + str(self.vals)

# TODO: just make this a Variant class with call sugar
def factory(typeClass, vtype, arity):
    def make(*vals):
        if len(vals) != arity:
            raise Exception('wrong number of vals')

        return Custom(typeClass, vtype, arity, *vals)

    make.vtype = vtype
    make.typeName = typeClass.name
    return make

class CustomType:
    def __init__(self, name, *constants, **funcs):
        self.name = name

        for vtype in constants:
            setattr(self, vtype, Custom(self, vtype, 0))

        for vtype, arity in funcs.items():
            setattr(self, vtype, factory(self, vtype, arity))
