from Elm import F, wrap, pipe
from Kernel import toElm, toPy
import List
import Tuple

# We could do this F-wrapping more automatically, but
# here we do it explicitly.
List.indexedMap = F(List.indexedMap)
List.sortBy = F(List.sortBy)
List.map_ = F(List.map_)

@wrap(toElm, toPy)
def ranks(lst):
    return pipe(
            lst, [
                (List.indexedMap) (Tuple.pair),
                (List.sortBy) (Tuple.second),
                (List.map_) (Tuple.first),
                (List.indexedMap) (Tuple.pair),
                (List.sortBy) (Tuple.second),
                (List.map_) (Tuple.first),
            ])

print(ranks([77, 0, 66, 22, 55, 99, 44, 33, 11, 88]))

