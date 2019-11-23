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
    def __init__(self, name, *constants):
        self.name = name

        for vtype in constants:
            setattr(self, vtype, Custom(self, vtype, 0))


