2019-12-05

[Dict.elm](https://github.com/elm/core/blob/1.0.2/src/Dict.elm)
is an interesting, important piece of code in Elm's core
library.

In this article
I do a deep dive on its implementation and discuss some other
explorations related to Dict.

The current version of Dict was primarily authored by Robin Hansen.
You may find his talk about [persistent collections](https://www.youtube.com/watch?v=mmiNobpx7eI&app=desktop)
interesting.


## Dict is a custom type

The `Dict` type is **literally** a custom type:

~~~ elm
type Dict k v
    = RBNode_elm_builtin NColor k v (Dict k v) (Dict k v)
    | RBEmpty_elm_builtin
~~~

Contrast `Dict` to `List`.  The `List` class in Elm is
much more of a builtin, using lots of JS code and not
explicitly surfacing a custom type.  See the "Footnotes"
for more discussion on `List`.

Dict.elm, on the other hand, is 100% pure Elm, and it
**never** directly calls kernel code.

(There are, however, some small indirect kernel dependencies that I cover in
the "Dict Equality" section of the "Footnotes".)

When you reference the `Dict.empty` value in your Elm projects,
you are literally referencing the one and only Elm value of
the custom type variant named `RBEmpty_elm_builtin`:

~~~ elm
empty : Dict k v
empty =
  RBEmpty_elm_builtin
~~~

And when you call `Dict.isEmpty`, it's just a simple
pattern match:

~~~ elm
isEmpty dict =
  case dict of
    RBEmpty_elm_builtin ->
      True

    RBNode_elm_builtin _ _ _ _ _ ->
      False
~~~

Fair enough.  Let's cover the much more interesting case
of non-empty dicts.

## Dict is a binary tree

Let's re-visit the meatier variant of type Dict:

~~~ elm
    RBNode_elm_builtin NColor k v (Dict k v) (Dict k v)
~~~

Every non-empty Dict instance is just a top-level node of a binary
tree, and it has a color (more about this later), a key, a value,
and two subtrees.  Each of the subtrees is either empty or
itself a top-level node of a smaller binary tree.

Here is a pictorial representation of a non-empty Dict:

![tree](https://showell.github.io/redblack.PNG)

The key properities of a binary tree are that you can insert,
remove, and find elements with O(logN) operations.  As a consequence,
here are the algorithmic complexities of the main operations of
Dict:

- insert: O(logN)
- get: O(logN)
- remove: O(logN)

You may have a couple questions:

- Why don't we use a data structure that has O(1) complexity for insert/get/remove?
- What's the deal with the "red" and "black" colors?

Let's cover algorithmic complexity first, and in the process
we'll learn why Dict is a binary tree in the first place.

## Dict is a persistent (i.e. shared) data structure

If you come to Elm from other programming languages with mutable
data structures, you may be wondering why Dict does not use an
O(1) hash implementation.

Let's talk about immutability first (and you can skim the next
section if you kinda know where this is going):

### Immutability

The following page lists the complexities for
Python's `dict` class (toward the bottom):

https://wiki.python.org/moin/TimeComplexity

The key points to know are that Python's dict has these properties:

- Get item: O(1)
- Set item: O(1)
- Delete item: O(1)

Python is O(1), whereas Elm is O(logN) for the same operations.

Are the Python folks just lying? No.

Are they some kind of mad geniuses who have discovered
a cutting edge algorithm? No.

The key difference between Python `dict` and Elm `Dict` is that
the former is mutable.  Let's illustrate:

Python:

~~~py
>>> d = { 1: "one", 2: "two" }
>>> d2 = d
>>> d2[3] = 'three'
>>> d
{1: 'one', 2: 'two', 3: 'three'}
>>> d2
{1: 'one', 2: 'two', 3: 'three'}
~~~

Note that changing `d2` also changes `d`!  This is a key feature
of Python, which is that you can assign multiple bindings to
the **same** dictionary and mutate it in place.

Elm:

~~~elm
> d = Dict.fromList([ (1, "one"), (2, "two") ])
> d2 = Dict.insert 3 "three" d
Dict.fromList [(1,"one"),(2,"two"),(3,"three")]
> d
Dict.fromList [(1,"one"),(2,"two")]
~~~

Note that Elm does not mutate the original dict!  This is a key
feature of Elm, which promises that once you assign a value to
the name, that value will **never** change.

Neither language is wrong here; they just make different choices.

Note that in Python it's completely possible to decouple `d2` from
`d` while still borrowing some of its values:

~~~py
>>> d = { 1: "one", 2: "two" }
>>> d2 = d.copy()
>>> d2[3] = 'three'
>>> d2
{1: 'one', 2: 'two', 3: 'three'}
>>> d
{1: 'one', 2: 'two'}
~~~

In order to make d2 **not** mutate d, we need to make a **copy**
of d when working in Python.  And that's an O(N) operation.

If Elm code is effectively achieving the same thing as the latter Python
example, wouldn't it also be making O(N) copies under the hood?
The answer, fortunately, is "no", and that is where persistent
data structures shine.

### Shared data structures





## Dict is a red-black tree

Dict is implemented as a red-black tree, which you can learn
more about here:

https://en.wikipedia.org/wiki/Red%E2%80%93black_tree


# Footnotes

## List

Elm's `List` could be modeled as a custom type, like so:

~~~ elm
type List a
    = Empty
    | Cons a (List a)
~~~

Conceptually, Elm does implement `List` as a union type
of `Cons` and `Empty` if you squint hard enough, but
there are two important caveats:

- Elm provides lots of sugar to make List instances
look like either `head :: rest` (ok, not too far from `Cons`) or
`[1, 2, 3]` (as opposed to `Cons 1 (Cons 2 (Cons 3 Empty))`).
- Elm cheats big time on the implementation, in a good way, for things
like sorting and mapping, as it transforms back and forth between
the Cons/Empty-like internal data structure (for immutability)
and raw JS lists (for speed).

You can learn a lot about `List` by looking at
[core/src/Elm/Kernel/List.js](https://github.com/elm/core/blob/1.0.2/src/Elm/Kernel/List.js).
Here is an excerpt:

~~~ js
function _List_Cons__PROD(hd, tl) { return { $: 1, a: hd, b: tl }; }
function _List_Cons__DEBUG(hd, tl) { return { $: '::', a: hd, b: tl }; }


var _List_cons = F2(_List_Cons);

function _List_fromArray(arr)
{
	var out = _List_Nil;
	for (var i = arr.length; i--; )
	{
		out = _List_Cons(arr[i], out);
	}
	return out;
}

function _List_toArray(xs)
{
	for (var out = []; xs.b; xs = xs.b) // WHILE_CONS
	{
		out.push(xs.a);
	}
	return out;
}

~~~

Remember I said that `List` is essentially `Cons a (List a)` under the
hood?  Here is how it's represented interally:

~~~ js
{ $: '::', a: hd, b: tl }; }
~~~

Every list is just a tuple-like thing with `::` denoting `Cons` and
`v.a` being the head (of type `a`) and `v.b` being the rest (of
type `List a`).  It's mostly that simple!

But, like I said, Elm's compiler optimizes certain operations:

~~~ js
var _List_sortBy = F2(function(f, xs)
{
	return _List_fromArray(_List_toArray(xs).sort(function(a, b) {
		return _Utils_cmp(f(a), f(b));
	}));
});
~~~

You can learn a lot from looking at the JS inside of your `index.html`.
Evan's compiler does a nice job of being faithful to the traditional
notion of `List` being a custom type without actually sacrificing
performance.

## Dict Equality

You will hear people (including me) say that Dict.elm is 100% pure
Elm, and that's true, but there are a couple compiler back doors that it
relies on.  When you compare two instances of Dict for equality
(using either `Basics.eq` or `==`), you are actually invoking some
custom-written JS code that the compiler emits:

~~~ js
	if (x === y)
	{
		return true;
	}

    // ...

	if (x.$ === 'RBNode_elm_builtin' || x.$ === 'RBEmpty_elm_builtin')
	{
		x = $elm$core$Dict$toList(x);
		y = $elm$core$Dict$toList(y);
	}
~~~

It would be nice to remove the need for that compiler hook in the
compiler.  If the compiler had a mechanism to let pure Elm objects
provide custom `eq` hooks, we would not only get true 100% Elm
purity in core `Dict`, but we could also support equality in
Dict alternatives such as `AssocList`.

I should also point out that `_Debug_toAnsiString` also knows
about `RBNode_elm_builtin` and `RBEmpty_elm_builtin`:

~~~ js
    if (tag === 'RBNode_elm_builtin' || tag === 'RBEmpty_elm_builtin')
    {
        return _Debug_ctorColor(ansi, 'Dict')
            + _Debug_fadeColor(ansi, '.fromList') + ' '
            + _Debug_toAnsiString(ansi, $elm$core$Dict$toList(value));
    }
~~~

Again, it would be nice if the compiler allowed pure Elm objects to
do the work here.

But it's really not that big a deal.  Your key takeaway from `Dict`
should be that 99% of the key pieces are pure Elm.  Also, 100% of
the code inside `Dict.elm` is pure Elm; it's only indirectly coupled
to the kernel code.


## Some history

I first heard about Elm some time around 2016, dabbled a bit in
it during 2018, but only finally took the deep dive this year
(2019).  Starting in October, I decided I would just immerse
myself as much as possible in the language, going down as many
rabbit holes as I needed to scratch my itches, to mix a couple
metaphors.  As long as the project was fun, and as long as I
was learning, all was good.

A great way to learn Elm (or most programming languages, actually)
is to write a simple game.  Elm is particularly good for writing
games.  I wrote a game called FastTrack, which you can see
in action [here](https://showell.github.io/ft.html).  I ended
up writing about 4k lines of
[Elm code](https://github.com/showell/elm-fasttrack/tree/master/src)
for the board game.  Despite being on the steepest part of
Elm's learning curve, I made steady progress throughout the
exercise and learned a lot about Elm itself.

There was only one major irritation along the way.  It turns
out Dict only works on comparable data types for keys.
And that excludes using custom types for keys.  At the time
I found it majorly annoying.  I now only found it minorly
annoying (and I am optimistic about "equalable" eventually
coming to the Elm compiler).

My annoyance isn't the point of this conversation, though.
What's more important is that I got interested in Dict.

