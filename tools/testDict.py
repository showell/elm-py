import Dict
import time
from Kernel import toPy
import  cProfile

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

print('\n\ninsert many...')

def benchmark(n):
    dct = Dict.empty()
    t = time.time()
    for i in range(n):
        dct = Dict.insert(i, i*10, dct)
    elapsed = time.time() - t
    print('done inserting')
    print(elapsed, elapsed / n)
    print('size', Dict.size(dct))

counts = [
    100,
    1000,
    10000,
    ]

for n in counts:
    benchmark(n)

# cProfile.run('benchmark(1000)', sort='time')

# print(list(Dict.toList(dct)))
