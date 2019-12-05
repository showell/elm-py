2019-12-05

This article is mostly about `Dict`.  Skip the first section
if you like, but it provides a little color to the story.

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

## Enter Dict

For those of you who have never looked at the innards of
[Dict.elm](https://github.com/elm/core/blob/1.0.2/src/Dict.elm).
It is a really interesting piece of code.

### quick aside to List

Before we learn about `Dict`, though, did you know that
`List` is really just a glorified custom type?:

~~~ elm
type List a
    = Empty
    | Cons a (List a)
~~~

Some of your are saying "duh, of course it is".  And on the other
hand, some of you are saying "no, it's not really exposed that way
in Elm".  And you're both kinda right.  Conceptually, Elm really
does implement `List` as a union type of `Cons` and `Empty` if you
squint hard enough, but there are two important caveats:

- Elm provides lots of sweet, sweet sugar to make List instances
look like either `head :: rest` (ok, not too far from `Cons`) or
`[1, 2, 3]` (as opposed to `Cons 1 (Cons 2 (Cons 3 Empty))`).
- Elm cheats big time on the implementation, in a good way, for things
like sorting and mapping, as it transforms back and forth between
the Cons/Empty-like internal data structure (for immutability)
and raw JS lists (for speed).

If you're curious about List, see the "Footnotes" section.

### back to Dict

So here's the thing about Dict.  It's not just figuratively a
custom type.  It's **literally** a custom type:

~~~ elm
type Dict k v
    = RBNode_elm_builtin NColor k v (Dict k v) (Dict k v)
    | RBEmpty_elm_builtin
~~~

The entire `Dict` data structure is build on top of this 
data structure! No, wait, not "on top of".  Dict **is**
this custom type.

Dict is 100% pure Elm, which only one small caveat that
I cover in the "Dict Equality" section of the "Footnotes."

# Footnotes

## List

You can learn a lot about `List` by looking at
[core/src/Elm/Kernel/List.js](https://github.com/elm/core/blob/1.0.2/src/Elm/Kernel/List.js):

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
Elm, and that's true, but there is one compiler back door that it
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
should be that 99% of the key pieces are pure Elm.



