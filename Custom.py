class Custom:
    def __init__(self, typeClass, vtype, arity):
        if type(typeClass) != CustomType:
            raise Exception('illegal typeClass for variant')

        self.typeClass = typeClass
        self.vtype = vtype
        self.arity = arity

    def isType(self, typeName):
        return self.typeClass.name == typeName

    def __eq__(self, other):
        if type(self.typeClass) != type(other.typeClass):
            raise Exception('illegal comparison')

        if self.vtype != other.vtype:
            return False

        if self.arity == 0:
            return True

class CustomType:
    def __init__(self, name, *consts):
        self.name = name
        self.constants = {
                vtype: Custom(self, vtype, 0)
                for vtype in consts}

    def __attr__(self, vtype):
        return self.get(vtype)

    def get(self, vtype):
        if vtype in self.constants:
            return self.constants[vtype]

        raise Exception('unrecognized variant')


