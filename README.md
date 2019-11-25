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

### elm-in-elm

There is a young project called [elm-in-elm](https://github.com/elm-in-elm/compiler)
that allows you to compile Elm code within Elm.  Once elm-in-elm can
compile all of Elm, it is possible to write a translator from Elm to
Python.

Given that elm-in-elm will eventually allow automatic translation, why
am I bothering to write this library?  Well, some of the core Elm code is
actually "kernel" code written in JS.  Also, for the most core pieces of
Elm, there are performance advantages to using hand-written Python.  Also,
some of this code may go away once elm-in-elm becomes more mature!  (but we
will make sure the behavior remains the same)

### Completed pieces

The following modules have been ported 100%:

- Basics
- List
- Maybe
- Order
- Tuple

You can also now create arbitrary custom types.  Just follow the
example of [Maybe.py](https://github.com/showell/elm-py/blob/master/Maybe.py).

### Data representation

For the following types of data, we use native Python equivalents:

- numbers
- strings
- tuples
- bools

For Elm custom types, we use a Python module called
[Custom.py](https://github.com/showell/elm-py/blob/master/Custom.py).
It has a class called `CustomType` to build new types, and then instances
of the types are instances of `Custom`.

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
- Debug (most folks will probably just debug natively in Python)
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

