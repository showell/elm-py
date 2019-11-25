Welcome to elm-py!

This repo ports Elm's core library to Python.

It is a work in progress, but the completed parts are well
tested.  If you find bugs, please file an issue.

### Goals

The main motivation for this project is to eventually support
running ALL Elm code in Python, for all cases where it makes sense.

Example things that could be ported:

- parser libraries (markdown, etc.)
- geometry libraries
- number crunching
- educational libraries

Obviously, one of the main use cases for Elm is to write code
that runs in the browser, so some Elm uses don't naturally port to
Python.  There are some things that can map pretty naturally, though.
If you are using Elm to create static HTML content, for example, that
could map easily to Python.

### Example

Here is an example of using the library:

~~~ py
# ranks =
#     \lst ->
#         lst
#             |> List.indexedMap Tuple.pair
#             |> List.sortBy Tuple.second
#             |> List.map Tuple.first
#             |> List.indexedMap Tuple.pair
#             |> List.sortBy Tuple.second
#             |> List.map Tuple.first
#             |> List.map (\n -> n + 1)

def ranks(lst):
    return \
        pipe(lst,
        [
            F(List.indexedMap)(Tuple.pair),
            F(List.sortBy)(Tuple.second),
            F(List.map)(Tuple.first),
            F(List.indexedMap)(Tuple.pair),
            F(List.sortBy)(Tuple.second),
            F(List.map)(Tuple.first),
            F(List.map)(lambda n: n + 1)
        ])
~~~

### elm-in-elm

There is a young project called [elm-in-elm](https://github.com/elm-in-elm/compiler)
that allows you to compile Elm code within Elm.  Once elm-in-elm can
compile all of Elm, it is possible to write a translator from Elm to
Python.

Given that elm-in-elm will eventually allow automatic translation, why
am I bothering to write this library?  Well, some of the core Elm code is
actually "kernel" code written in JS.  Also, for the most core pieces of
Elm, there are performance advantages to using hand-written Python.  Also,
some of this code may go away once elm-in-elm becomes more mature!  (but
having these libraries now allows us to make progress until then)

### Completed pieces

The following modules have been 100% ported:

- Basics
- List
- Maybe
- Order
- Tuple


### Custom types

You can now create arbitrary custom types in Python!

Just follow the example of
[Maybe.py](https://github.com/showell/elm-py/blob/master/Maybe.py).

### Data representation

For the following types of data, we use the native immutable
Python equivalents:

- bools
- numbers
- strings
- tuples

For Elm custom types, we use a Python module called
[Custom.py](https://github.com/showell/elm-py/blob/master/Custom.py).
It has a class called `CustomType` to build new types, and then instances
of the types are instances of `Custom`.

The following types are custom types:

- Order (EQ/LT/GT)
- Maybe (Just/Nothing)

The following things are **not** native Python, but they are
instead wrapped versions of persistent data types:

- Elm List -> custom Python List module (not `list`!)
- Elm Dict -> not implemented yet

### TODO

There is a still a lot of work to do!  Contributions are welcome, but
if you intend to contribute, please find me on the Elm slack for anything
more involved than a simple bug fix.

The most important remaining pieces are Array, Dict, and Set.  For them I
intend to use [pyrsistent](https://pypi.org/project/pyrsistent/):

- Array: wrap PVector
- Dict: wrap PMap
- Set: wrap PSet

The following modules should be straightfoward to port, and I
simply haven't gotten to them yet:

- Bitwise
- Char
- Debug
- Result (should be very similar to Maybe) 
- String

I haven't even really investigated these modules yet to know how hard
they are to port to Python, but they may be the biggest OS-specific
challenges:

- Platform
- Platform.Cmd
- Platform.Sub
- Process
- Task

There are also important packages that aren't technically part of
elm/core that may be worth porting, especially if they use kernel
code:

- elm/html
- elm/http
- elm/json
- elm/parser
- elm/url


### Debugging

I intend to port `Debug.elm` to Python, but most folks will just debug
Python as they normally debug Python (which varies among Python
programmers).

Even though this library is obviously inspired by Elm, the code is
fairly vanilla Python.  All objects support `str()` for easy print
debugging.

### Partial functions

Most Python functions complain if you try to partially apply operators
to them, but this is easily worked around, as demonstrated below:

~~~ python
>>> import List
>>> List.repeat(5)("hello")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: repeat() missing 1 required positional argument: 'x'
>>>
>>> from Elm import F
>>>
>>> F(List.repeat)(5)("hello")
<ListKernel.List object at 0x0382FC40>
>>> list(F(List.repeat)(5)("hello"))
['hello', 'hello', 'hello', 'hello', 'hello']
~~~

See [Elm.py](https://github.com/showell/elm-py/blob/master/Elm.py) for more
details on the `F` function.

### Type conversions

As mentioned above, the elm-py ecosystem mostly uses standard Python types,
so there should be few interop concerns.  If you want to use the Python
equivalent of an Elm list, then use the `toElm` helper on the inbound side.
On the outbound side, just use `list(...)`, because the `List` type is an
iterator.

~~~ python
>>> from Kernel import toElm
>>> lst = toElm([ [1, 2, 3], [4, 5] ])
>>> maybe_list = List.head(lst)
>>> str(maybe_list)
'Just [ 1, 2, 3 ]'
>>> list(maybe_list.val)
[1, 2, 3]
~~~

For deeper conversions, use the `toPy` helper:

~~~ python
>>> from Kernel import toElm, toPy
>>> lstOfLsts = toElm([ [1, 2, 3], [4, 5, 6] ])
>>> list(lstOfLsts)
[<ListKernel.List object at 0x02DE5FD0>, <ListKernel.List object at 0x02DF20B8>]
>>> toPy(lstOfLsts)
[[1, 2, 3], [4, 5, 6]]
~~~

It is also easy to work with Maybe types:

~~~ python
>>> import Maybe
>>> m1 = Maybe.Nothing
>>> m2 = Maybe.Just(42)
>>>
>>> m1.vtype
'Nothing'
>>> m2.vtype
'Just'
>>> m1.match('Just')
False
>>> m2.match('Just')
True
>>> m1 is Maybe.Nothing
True
>>> m2 is Maybe.Nothing
False
>>> m2.val
42
~~~

## Pattern matching

Python doesn't have the equivalent of Elm's case statement, but
you can use idiomatic Python code to accomplish the same
results:

~~~ py
def andThen(f, m):
    if m == Maybe.Nothing:
        return Maybe.Nothing

    return f(m.val)

def minimum(lst):
    if List.isEmpty(lst):
        return Maybe.Nothing
    else:
        (x, xs) = List.uncons(lst)
        return Maybe.Just(foldl(min, x, xs))
~~~


### Static type checking

Python has support for [function annotations](https://www.python.org/dev/peps/pep-3107/),
but I have not added those yet.  I am waiting on this to see how much support I can
get from elm-in-elm, once they add annotation support on the Elm side.

In principle we should be able to make elm-py play nice with any Python static
checker, such as [mypy](http://mypy-lang.org/).  I would consider any PR that adds
type annotations to the library, but let's try to discuss it first on Slack.

### Runtime type checking

I try to make this library Pythonic.  Even though Python is partly dynamic in nature,
it is more strongly typed than, say, JavaScript:

~~~ python
>>> 1 + 'hello'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'int' and 'str'
~~~

Where possible, I try to make elm-py code fail in obvious ways.  All the
errors below are intentional!

~~~ python
>>> m = Maybe.noting
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: module 'Maybe' has no attribute 'noting'
>>> m = Maybe.jut(42)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: module 'Maybe' has no attribute 'jut'
>>>
>>> m = Maybe.Just(42)
>>> m = Maybe.Just("too", "many", "args")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Users\Steve\PROJECTS\elm-py\Custom.py", line 52, in make
    raise Exception('wrong number of vals')
Exception: wrong number of vals
~~~

There is still plenty of room for improvement here.

### Testing

I have automated tests in [test.py](https://github.com/showell/elm-py/blob/master/test.py).

You should also check out [metaElm.py](https://github.com/showell/elm-py/blob/master/metaElm.py),
which tests Python code at was actually generated from Elm!
(It wasn't using elm-in-elm, but it demonstrates a similar idea.)

### Prior art

I am not aware of any other attempts at Elm/Python interoperability.  Let me
know if I am missing anything!  Googling for "Python Elm" turns up many results
on the "Extreme Learning Machine".

Obviously, many Elm concepts are well understood in (parts of ) the Python community.

For example, folks have written libraries like pyrsistent to implement immutable
data structures.  Also, core Python has modules like `functools` and `itertools`
for well over a decade, and they support functional programming concepts.

### Conclusion

Thanks for reading!

After I get more feedback I will announce future plans.  For now the
most immediate goals are to finish porting some of the simpler
libraries from elm/core.

-- Steve Howell

(find me on Elm's Slack or Github: userid = "showell")
