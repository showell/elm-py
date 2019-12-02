import Dict
from Kernel import toPy

print('empty')
dct = Dict.empty()
print(toPy(dct))
print('member', Dict.member(5, dct))
print('get', Dict.get(5, dct))
print('size', Dict.size(dct))
print('empty', Dict.isEmpty(dct))

print('\n\ninsert one...')
dct = Dict.insert(5, 50, dct)
print('member', Dict.member(5, dct))
print('get', Dict.get(5, dct))
keys = Dict.keys(dct)
print('keys', keys)
print('size', Dict.size(dct))
print('empty', Dict.isEmpty(dct))

dct = Dict.empty()

for i in range(1000):
    dct = Dict.insert(i, i*10, dct)


print(list(Dict.toList(dct)))
