2019-12-05

[Dict.elm](https://github.com/elm/core/blob/1.0.2/src/Dict.elm)
is an interesting, important piece of code in Elm's core
library.

The current version of Dict was primarily authored by Robin H Hansen.
You may find his talk about [persistent collections](https://www.youtube.com/watch?v=mmiNobpx7eI&app=desktop)
interesting.


## Dict is a custom type

The `Dict` type is literally just a custom type:

~~~ elm
type Dict k v
    = RBNode_elm_builtin NColor k v (Dict k v) (Dict k v)
    | RBEmpty_elm_builtin
~~~

Contrast `Dict` to `List`.  The `List` class in Elm relies on
significant chunks of JS code and does not
explicitly use a custom type.  See the [List](#List) section
in the [Footnotes](#Footnotes) for more discussion on `List`.

Dict.elm, on the other hand, is 100% pure Elm, and it
**never** calls kernel code.

(There are some small, indirect kernel dependencies that I cover in
the [Dict Equality](#Dict-Equality) section of the footnotes.)

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

Here is a pictorial representation of a non-empty Dict (showing
integer keys):

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

Let's talk about immutability first.

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

### The copying problem

In Python it's completely possible to decouple `d2` from
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

Elm will never mutate your data structures.

When you create a Dict `d1` with
100 items, and then create a new Dict `d2` with the 100 elements
from `d1` plus some 101st item, Dict won't mutate `d1`.  But Dict
also won't make an entire copy of those 100 items for `d2`.

Instead, `Dict.elm` uses a shared data structure that preserves
the items from `d1` inside of `d2`.  Computer folks call these
type of data structures **persistent collections**, because
the collections persist/preserve the previous versions of
themselves.

For reasons that are a bit difficult to explain, it is hard
to build a persistent dictionary using
a traditional hash table implementation.  Let's say you
create a series of dictionaries with 1, 2, 3, 4, 5, ..., 97,
98, 99, and 100 items, where each dictionary in that sequence adds
one more key/value pair to the previous.  If you want to share
the same hash table entry for the 100th key/value pair, you would
need to indicate all 100 of its owners, and then likewise for
the 99 owners of the 99th item, and then likewise for the 98
owners of the 98th item, and so on.  And so you're right back
to having O(N) operations for any kind of search.  Also, in
order to even get random access to hash table entries, you
probably have to build the hash directly in JS or build on top
of some other pure Elm data structure that is more intrinsically
complex than the Dict itself!

Instead of using a hash table, you could instead go simple and use an
extremely compact list representation for your 100 dicts:

    d1 = (k, v)
    d2 = (k, v) -> copy of d1
    d3 = (k, v) -> copy of d2 (which is just the above)
    d4 = (k, v) -> copy of d3 (which is just the above)
    d5 = (k, v) -> copy of d4 (which is just the above)
    ...

    d99 = (k, v) -> copy of 
    d100 = (k, v) -> copy of d99

And at the end you would only have O(N) elements:

    (k100, v100) -> (k99, v99) -> ... -> (k2, v2) -> (k1, v1)

But then your problem is still speed.  If you want to get the 50th
element, you have to traverse through 50 key/value pairs
before getting to your data.

The way to solve this is using an indexed data structure.
And, indeed, Dict uses a binary search tree.  A binary tree allows
you to inspect its top node to decide which half of the
tree to search for any given key.  And then you can keep
dividing the problem in half, generally making only about
log-base-2-of-N comparisons to find elements.

Let's look again at our image of a binary tree:

![tree](https://showell.github.io/redblack.PNG)

In order to get to any elements, you only have to traverse
3 or 4 edges.  Beautiful!

But what happens when we create a new dictionary just
like the previous?  Can we just add a node to the tree?
Well, no it's not quite that simple.  But we also don't
need to copy the whole tree.  We just need to copy the
3 or 4 nodes between the root of the tree and the new
leaf.

It looks something like below (image from wikipedia):

![shared tree](https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Purely_functional_tree_after.svg/438px-Purely_functional_tree_after.svg.png)

The copying process takes a little while to understand, but the
main point here should not be lost:

**Dict uses binary trees to efficiently implement a persistent
collection.**

The tradoff here is that instead of O(1) lookups, we get O(logN) lookups.
Unless you have a really large N, performance will almost always
be acceptable.  Even a tree with a billion nodes is only about 30
levels deep.

There is, however, one technical problem that I have so far glossed over.
We need to keep the tree balanced.  And this gets us back to why
Dict.elm's `RBNode_elm_builtin` variant has a slot for "color."

## Dict is a red-black tree

Dict is implemented as a red-black tree, which you can learn
more about here:

https://en.wikipedia.org/wiki/Red%E2%80%93black_tree

A perfectly balanced binary search tree looks like this:

        4
     2    6
    1 3  5 7

Unfortunately, your inserts would often lead to something more
like this if you don't balance them:

    
       2
     1   6
        5 7
       3

Or, worst case:

    1
     2
      3
       4
        5
         6
          7

For the N=7 case, the last tree isn't gonna be a performance
disaster, but for large N, it will be.

It turns out that transforming an unbalanced tree into a
perfectly balanced tree is an expensive operation, and you
don't want to do it on every insert.  Instead, you want to
keep the tree "sorta balanced".

The red-black tree algorithm is a clever solution to this
problem.  Under a red-black regime, you only balance your
tree enough to satisfy this condition:

**Red nodes are bad.  You can only have so many of them before
you must do something about it.**

I am only slightly exaggerating! You can read the
[Properties](https://en.wikipedia.org/wiki/Red%E2%80%93black_tree#Properties)
section of the wikipedia article for more detail.

Let's get back to Elm code!

## NColor

Let's get back to the definition of a Dict node:

~~~ elm
    RBNode_elm_builtin NColor k v (Dict k v) (Dict k v)
~~~

I kept you in suspense for a long time about what `NColor`
represented.  Here it is:

~~~ elm
type NColor
    = Red
    | Black
~~~

A bit underwhelming, huh, after all that explanation?

`NColor` is just an implementation detail used to keep the
underlying binary tree balanced using the red-black algorithm.
It only affects operations like insert/remove/update that
create new versions of the binary tree.  For most operations
you can mostly ignore it.

## Searching

Let's look at Dict's get method:

~~~ elm
get targetKey dict =
  case dict of
    RBEmpty_elm_builtin ->
      Nothing

    RBNode_elm_builtin _ key value left right ->
      case compare targetKey key of
        LT ->
          get targetKey left

        EQ ->
          Just value

        GT ->
          get targetKey right
~~~

The above piece of code encapsulates Dict's elegance to
me.  At its heart Dict.elm is just a bunch of functions
doing pattern matches on a simple custom type.  And the
data structure is entirely centered around the equally
simple `Order` type.

~~~
type Order = LT | EQ | GT
~~~

Look closer at the first pattern match:

~~~ elm
    RBNode_elm_builtin _ key value left right ->
~~~

Note how we just pick out all the key fields in the
pattern match expression.  The only field we ignore
is the `NColor` piece, which is what the `_` placeholder
is for.  Beautiful!

# More simple functions

Dict's inherent simplicity also shines in `map` and `foldl`.
If you understand the basic recursive structure of Dict, the
implementations fall out quite naturally:

~~~ elm
map func dict =
  case dict of
    RBEmpty_elm_builtin ->
      RBEmpty_elm_builtin

    RBNode_elm_builtin color key value left right ->
      RBNode_elm_builtin color key (func key value) (map func left) (map func right)

foldl func acc dict =
  case dict of
    RBEmpty_elm_builtin ->
      acc

    RBNode_elm_builtin _ key value left right ->
      foldl func (func key value (foldl func acc left)) right
~~~

Unlike `foldl`, the implementation of `foldr` is quite complicated.

Just kidding!

The only way `foldr` differs from `foldl` is that `right` and `left` swapped in
the recursive step:

~~~ elm
foldr func acc t =
  case t of
    RBEmpty_elm_builtin ->
      acc

    RBNode_elm_builtin _ key value left right ->
      foldr func (func key value (foldr func acc right)) left
~~~

If you are having trouble parsing this...

~~~ elm
  foldr func (func key value (foldr func acc right)) left
~~~

...it may help to think of it like this:

~~~elm
    let
        acc1 = foldr func acc right -- fold the right subtree
        acc2 = func key value acc2 -- apply func to value/acc2
    in
    foldr func acc2 left -- fold the left subtree with acc2
~~~

The key thing to note is that the structure of the code nearly
perfectly reflects the data structure.  And it's all pattern
matching and function application!

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

Dict.elm is truly 100% pure Elm, and it doesn't call kernel code.

There are, however, a couple compiler features that work in support
of Dict.  When you compare two instances of Dict for equality
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


## Back story

How did I get so interested in Dict?

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

