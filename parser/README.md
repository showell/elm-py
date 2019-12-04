2019-12-04

## Quick links:

- [Dict.elm](https://github.com/showell/elm-py/blob/master/parser/elm/Dict.elm)
- [transpiler](https://github.com/showell/elm-py/blob/master/parser/emitDictPy.py)
- [Dict.py](https://github.com/showell/elm-py/blob/master/src/Dict.py)


## What is this?

This directory contains code that transpiles Elm code into
Python code.

Up until now, I have only written enough code to transpile
`Dict.elm`, which comes from elm's `core` library.

The reason that I chose `Dict.elm` as my first victim is that
`Dict.elm` is written in pure Elm, and it's a powerful part
of Elm's core library.

But let's back up...

## Big picture

I want to be able to translate Elm code into Python code
for things like multi-player games, where the front end
runs in Elm, but I can borrow Elm code to run on the server,
but I will transpile it to Python to play nice with other
Python code (and let Python do things like manage connections,
log results, do imperative things, etc.).

I also am using Python as a target to explore general issues
with transpiling Elm to other targets (like maybe Rust some
day).  Transpiling Elm line-for-line to any non-Elm language
will always reveal some issues.

Ideally you would literally just transpile every single line of
Elm code into Python using some sort of logical mapping, but there
are concepts that don't directly translate, such as pattern
matching in Python.  Also, Elm itself uses kernel code written
in JS, so you have to port the kernel pieces.  Finally, there
are some core pieces that can be optimized in Python, such as
lists (and in some cases this overlaps with code that is kernel
code in the Elm ecosystem).

## Transpiling

Despite what I said earlier about difficulties in translating
certain Elm concepts to Python, the transpiler does nearly
a line-for-line translation of Elm into Python.

It's a two-stage parser, basically:

- parse the Elm into an AST
- emit the Python

It starts with [emitDict.py](https://github.com/showell/elm-py/blob/master/parser/emitDictPy.py), which calls into [lib/ElmParser.py](https://github.com/showell/elm-py/blob/master/parser/lib/ElmParser.py) to do the parsing.

The parsing code returns some AST objects from [lib/ElmTypes.py](https://github.com/showell/elm-py/blob/master/parser/lib/ElmTypes.py), which have `emit` methods.
You call those methods to generate the Python code.  At that point you
will have created `Dict.py`, although of course you can also just pull
[Dict.py](https://github.com/showell/elm-py/blob/master/src/Dict.py) out of
the repo.

Right now it's all hand-written code.  It's basically a recursive descent
parser (i.e. no fancy tooling like grammar generators).

The actual parsing is done mostly with generic code from
[lib/ParserHelper.py](https://github.com/showell/elm-py/blob/master/parser/lib/ParseHelper.py), and there is a pretty long comment at the top of that file that
explains the basic paradigm.

## Dict.py dependencies

`Dict.elm` is **not** a standalone piece of code, and neither is `Dict.py`.

Both rely on other components to do some of their work.  In both languages
we import from libraries like Basics, Maybe, and List.  Right now I don't actually
automatically transpile the imports for `Dict.py`--they are hard coded, but that
may change soon.

So where do List.py and Maybe.py and friend come from?  They can be found in
the [src](https://github.com/showell/elm-py/tree/master/src) directory.  The
modules in `src` were mostly hand coded line-for-line ports of the
corresponding Elm libraries (with some tweaks to be more Pythonic in places).
The exception to that rule is of course, `Dict.py`, which was automatically
transpiled from the original Elm source code.

Another crucial fact about `Dict.py` is that is heavily uses pattern matching.
Pattern matching is a fundamental concept in Elm, but it's not a native concept
to Python, so we emit calls to `patternMatch`, which is just a normal (albeit
powerful) Python function that currently lives
in [../src/Elm.py](https://github.com/showell/elm-py/blob/master/src/Elm.py).

## Quick aside

I hope this all doesn't sound super complicated.  Big picture, we are
just building out a line-for-line port of Elm's core library, and the
Python transpiler is just some tooling to help facilitate that porting
exercise. It's really almost that simple!

## Tests

It would be nice to know that the transpiled code in `Dict.py` actually
works, right?  Well, you can find tests in
[testDict.py](https://github.com/showell/elm-py/blob/master/tests/testDict.py).
We exercise every function from the core library.

You can also find tests for other components of the core library
[here](https://github.com/showell/elm-py/tree/master/tests).

Finally, we have tests for the parser itself
[here](https://github.com/showell/elm-py/tree/master/parser/tests).

## Limitations

The most limited piece of code that currently lives in this repo
is the Elm-to-Python transpiler.  It literally does just enough
parsing to handle the constructs in `Dict.elm`.  It can only
parse similar looking Elm code, and even then there are no guarantees.
Hopefully the code should be easy to extend in the future, and
contributions are welcome.

I'll make bolder claims about `Dict.py` itself.  As far as I know,
it's as bug-free as the original Elm code, and I didn't find any
parts of its API that I had to omit/limit/deprecate.  If you find
bugs, please report them.

I am about 95% confident that the pattern matching code is robust
for the cases it handles, but I only wrote enough code there to
handle the patterns used by `Dict.elm`.  Again, I hope to flesh out
that code.

## Next steps

I will be announcing this to the Elm Community via Slack and Discourse,
so try to find me there if you have further questions.

If you are generally interested in this kind of tooling, you may also
want to check out [elm-in-elm](https://github.com/elm-in-elm/compiler#contributing).

Thanks!

-- Steve Howell

(find me on Elm's Slack or Github: userid = "showell")
