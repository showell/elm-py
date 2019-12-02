import Dict
import random
import time
from Kernel import toPy
import  cProfile

print('singleton')
dct = Dict.singleton(5, 50)
assert Dict.get(5, dct).val == 50

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


def benchmark(n):
    print('\n\ninsert many...')
    lst = list(range(n))
    random.shuffle(lst)

    dct = Dict.empty()
    t = time.time()
    for i in lst:
        dct = Dict.insert(i, i*10, dct)
    elapsed = time.time() - t
    print('rate', int(n * 1.0 / elapsed))

    assert(Dict.size(dct) == n)

    print('membership')
    t = time.time()
    for i in lst:
        assert Dict.member(i, dct)
    elapsed = time.time() - t
    print('rate', int(n * 1.0 / elapsed))


    print('get')
    t = time.time()
    for i in lst:
        assert Dict.get(i, dct).val == i * 10
    elapsed = time.time() - t
    print('rate', int(n * 1.0 / elapsed))


    print('remove')
    t = time.time()
    for i in lst:
        dct = Dict.remove(i, dct)
    elapsed = time.time() - t
    print('rate', int(n * 1.0 / elapsed))

    assert Dict.size(dct) == 0
    assert Dict.isEmpty(dct)


counts = [
    1000,
    # 10000,
    ]

for n in counts:
    benchmark(n)

# cProfile.run('benchmark(1000)', sort='time')

# print(list(Dict.toList(dct)))
