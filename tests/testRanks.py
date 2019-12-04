"""
This tests a simple example of using elm-py.
"""

import sys
sys.path.append('../src')

from Elm import F, wrap, pipe
from Kernel import toElm, toPy
import List
import Tuple

# We could do this F-wrapping more automatically, but
# here we do it explicitly.
List.indexedMap = F(List.indexedMap)
List.sortBy = F(List.sortBy)
List.map = F(List.map)

@wrap(toElm, toPy)
def ranks(lst):
    """
    This returns a list of integers representing the
    "each" element in the input list.  The rank of 0
    is for the "lowest" element in the list, and so on.
    """
    return pipe(
            lst, [
                (List.indexedMap) (Tuple.pair),
                (List.sortBy) (Tuple.second),
                (List.map) (Tuple.first),
                (List.indexedMap) (Tuple.pair),
                (List.sortBy) (Tuple.second),
                (List.map) (Tuple.first),
            ])

if __name__ == '__main__':
    res = ranks([77, 0, 66, 22, 55, 99, 44, 33, 11, 88])
    assert res == [7, 0, 6, 2, 5, 9, 4, 3, 1, 8]

