import Dict
from Kernel import toPy

dct = Dict.empty()
print(toPy(dct))

print(Dict.member(5, dct))
print(Dict.get(5, dct))
print(Dict.size(dct))
print(Dict.isEmpty(dct))

dct = Dict.insert(5, 50, dct)
print(Dict.get(5, dct))
keys = Dict.keys(dct)
print(keys)
