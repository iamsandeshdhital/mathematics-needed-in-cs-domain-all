# 01 — How to Read Mathematical Notation

**Part**: part00_orientation · **Prerequisites**: 00 · **Time**: 25 min

---

## In Plain Words

Mathematical writing is a compressed language. Authors write for readers who
already know the conventions, so they drop everything they can. What is left is
a formula that looks alien until you know three things: how the symbols map to
English, how the shape of the formula tells you what kind of thing it is, and
how scope works, which is the same idea as scope in your programming language.

This lesson is the toolkit for the rest of the repository. It is not a lesson
about any particular mathematics. Every symbol here shows up again and again in
Parts 01 through 10, and each one comes with a plain-English sentence and a
Python equivalent you can run. Once you can read
"for every element of the set, if this holds then that holds" off a page, none
of the later notation will slow you down.

The single most useful habit in this lesson: **when you hit a symbol you do not
recognise, look at what it is attached to.** Symbols have local meanings.
A superscript means one thing on a number and another on a function. A letter
means one thing as a variable and another as a set. Position carries the meaning.

## Why Computer Science Cares

**Specification documents are written in this notation.** A formal specification of
a cache, a transaction protocol, or a type system is full of quantifiers and
implications. If you cannot read `∀x ∈ S, P(x) ⟹ Q(x)`, you cannot review a
specification, and reviewing specifications is most of correctness work.

**Papers.** "By a standard argument, the time complexity is
`O(|V| + |E| log |E|)`" tells you nothing to the person who cannot read it. It
tells a graph theorist exactly how the algorithm behaves, including the constant
factors hidden in the `+` and the log.

**Type systems are quantified logic.** In System F and in dependent types,
`∀T. T → T → T` is not a hint, it is the actual definition of the type of a
function. Reading the types in an error message from GHC or the Lean compiler
requires reading quantification.

**Interview questions are often notation with the story removed.** "Given
`sorted(A)`, find the position of `x`" is a quantifier question in disguise:
find `i` such that for every `j < i`, `A[j] < x`.

**Standard library docstrings.** `dict.keys()` returns a "view". `str.count()`
documents its behaviour with quantifiers. NumPy and pandas docstrings are full of
`∑` and `⊤`.

## The Formal Version

This lesson defines two things. Everything else is a translation.

**Notation.** A notational system is a set of marks together with rules for
combining them into strings, and an interpretation function from strings to
meanings. Two different systems can describe the same mathematics, and the same
mark can mean different things in different systems.

**Bound and free variables.** Let `F` be a formula. A variable `x` is *free* in
`F` if its meaning depends on a value supplied from outside. A variable `x` is
*bound* in `F` if some subpart of `F` introduces it and fixes its meaning within
that subpart. The subpart is a *binder*.

The Python analogue is exact:

| Mathematics | Python |
| --- | --- |
| bound variable | a function parameter or loop variable |
| free variable | a name resolved from an enclosing scope, or a global |
| binder | `def`, `for`, `lambda`, comprehension `for` |
| the set a binder ranges over | the iterable in a `for` |
| substituting a value for a free variable | calling the function |

A formula is a *function* of its free variables. "x² + 1" is not a number; it is
a function, and it becomes a number only when you pin `x`. This is why textbooks
distinguish a formula from a function at all, and it is not a distinction you
need to make in code.

## Worked Example

Reading `{x ∈ ℤ : x ≡ 3 (mod 5)²}` slowly, clause by clause. This is the kind of
formula you will meet the moment anyone mentions congruences.

**Symbols present.** `{}` enclosing, `∈` membership, `:` reads "such that" or
"such that the following holds", `≡` congruence, `(mod 5)` the modulus.

**Step 1. Identify the binder and what it ranges over.** The colon divides the
formula. On the left of the colon, `{x ∈ ℤ : ...}`. Read `x ∈ ℤ` as "x is an
integer". So the braces are building a *set*, out of integers, of things that
satisfy the condition to the right. `ℤ` is the domain. This maps to Python as
`{x for x in integers if CONDITION}`.

**Step 2. Read the condition.** `x ≡ 3 (mod 5)²` has a precedence trap. `≡` binds
loosely, and `(mod 5)²` — is the `5` inside or outside the square?

Standard convention: `(mod 5)` is a trailing qualifier that binds to the whole
congruence, exactly like a unit suffix. So the whole thing is
`(x ≡ 3) (mod 5²)`, i.e. `x ≡ 3 (mod 25)`. The square applies to the modulus,
because the parenthesis closed before the exponent.

**Step 3. Compute it.** `x ≡ 3 (mod 25)` means "x and 3 leave the same remainder
when divided by 25". So the set is all integers of the form `25k + 3` for
integer `k`: `…, -47, -22, 3, 28, 53, …`.

**Step 4. Check the reading.** Is it finite or infinite? Infinite, because there
are infinitely many integers. If you had misread it as `(x ≡ 3 mod 5)²`, which
would be a boolean squared and therefore just the truth value, you would have
got a set containing `0` and `1`. That absurdity is a good error check.

**Step 5. Write the Python.**

```python
# {x in Z : x = 3 (mod 25)} read as: all integers whose remainder mod 25 is 3
result = sorted(x for x in range(-60, 60) if x % 25 == 3)
print(result)
```

which prints `[-47, -22, 3, 28, 53]`, and extending the range just adds more
members forever.

**Step 6. Notice what you actually did.** You identified the binder, named the
domain, parsed the condition by looking at what each symbol was attached to,
translated to a generator expression, and sanity-checked the size of the answer.
That is the whole method. Nothing in step 2 or 5 was mathematical insight; it
was reading.

## Runnable Code

### Set-builder notation is a comprehension

```python
# {x : x*x < 40}  is  {x for x in ... if x*x < 40}

print("== { x in N : x^2 < 40 } ==")
squares_under_40 = {x * x for x in range(100) if x * x < 40}
print(sorted(squares_under_40), "count =", len(squares_under_40))
print("x runs 0..6 because 6^2 = 36 < 40 but 7^2 = 49 is not.")

print()
print("== { x : x even and 10 <= x <= 30 } ==")
print(sorted(x for x in range(10, 31) if x % 2 == 0))

print()
print("== { (a, b) in N x N : a + b = 5 }  (a slice of the cartesian product) ==")
pairs = sorted((a, b) for a in range(6) for b in range(6) if a + b == 5)
print(pairs, "count =", len(pairs))

print()
print("The colon is Python's `for` + `if`.")
print("Left of the colon  = what you are building.")
print("Right of the colon = the condition it must satisfy.")
```

### The summation sign is a for loop in a costume

```python
def sum_squares_as_written(n: int) -> int:
    """Transcribed literally from  sum over i=1..n of i^2."""
    total = 0
    for i in range(1, n + 1):      # <-- the sigma sign, expanded
        total += i * i             # <-- the body under the sign
    return total


def sum_squares_closed_form(n: int) -> int:
    """The closed form n(n+1)(2n+1)/6."""
    return n * (n + 1) * (2 * n + 1) // 6


print(f"{'n':>5} {'by the sum':>12} {'by the formula':>15} {'agree':>6}")
for n in (1, 2, 5, 10, 100, 1_000):
    a = sum_squares_as_written(n)
    b = sum_squares_closed_form(n)
    print(f"{n:>5} {a:>12} {b:>15} {str(a == b):>6}")

print()
print("Same integer, two routes. The formula costs a handful of multiplications;")
print("the sum costs n iterations. For n = 10**6 that is 1,000,000 iterations")
print("against 3. Recognising the closed form is a real optimisation.")
```

### Big-O: read it as an inequality with two unnamed constants

```python
def linear_work(n: int) -> int:
    """One pass: exactly n units of work."""
    steps = 0
    for _ in range(n):
        steps += 1
    return steps


def quadratic_work(n: int) -> int:
    """Nested loops: exactly n*n units of work. Kept tiny on purpose."""
    steps = 0
    for _ in range(n):
        for _ in range(n):
            steps += 1
    return steps


def logarithmic_work(n: int) -> int:
    """Halve the problem each step. This is bisection."""
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps


print("Exact work counts, no clock involved:")
print(f"{'n':>22} {'log2 n steps':>13} {'linear steps':>14} {'n^2 steps':>26}")
for n in (16, 1_000, 1_000_000, 2**64):
    print(f"{n:>22} {logarithmic_work(n):>13} {n:>14} {n * n:>26}")

print()
print("n changed by a factor of about 10**18 between the first and last row.")
print(f"  linear work went 16 -> {2**64}, exactly as n did.")
print(f"  log work went {logarithmic_work(16)} -> {logarithmic_work(2**64)}.")
print("  64 halvings to search 2**64 records. A linear scan needs 2**64 steps.")

print()
print("Checking the definition rather than trusting a stopwatch:")
print("  f(n) = O(g(n))  means  there are c and n0 with f(n) <= c*g(n) for all n > n0.")
print("  linear_work(n)   = n      -> n <= 1*n        always")
print("  quadratic_work(n) = n*n    -> n*n <= 1*n      only when n <= 1")
print("  quadratic_work(n) = n*n    -> n*n <= 1*n^2    always")
print()
print("So quadratic_work is not O(n). It is O(n^2). The constant is swallowed:")
print("2n and 1000n are both O(n), and n*n is O(n^2). One line of arithmetic.")
```

### Quantifiers are `all` and `any`, and the domain is part of the claim

```python
users = [
    {"name": "ada", "age": 36, "admin": True, "active": True},
    {"name": "linus", "age": 34, "admin": True, "active": False},
    {"name": "grace", "age": 45, "admin": False, "active": True},
    {"name": "alan", "age": 41, "admin": False, "active": True},
]

print("== quantifiers over a finite domain ==")
print("forall u in users : u.age >= 18  ->", all(u["age"] >= 18 for u in users))
print("exists u in users : u.admin        ->", any(u["admin"] for u in users))
print("forall u in users : u.active       ->", all(u["active"] for u in users))
print("who breaks it:", next(u["name"] for u in users if not u["active"]))

print()
print("== negating a quantifier flips it AND negates the predicate ==")
lhs = not all(u["active"] for u in users)
rhs = any(not u["active"] for u in users)
print("  not (forall u : active(u))   ->", lhs)
print("  exists u : not active(u)    ->", rhs)
print("  same statement:", lhs == rhs)

print()
print("== the domain changes the answer, not just the predicate ==")
print("  exists x in [1, 10]  : x even ->", any(x % 2 == 0 for x in range(1, 11)))
print("  exists x in [-5, 5]  : x even ->", any(x % 2 == 0 for x in range(-5, 6)))
print("  forall x in [-5, 5]  : x^2>=0 ->", all(x * x >= 0 for x in range(-5, 6)))
print("  forall x in [-5, 5]  : x > 0  ->", all(x > 0 for x in range(-5, 6)))
print("  forall x in [1, 5]   : x > 0  ->", all(x > 0 for x in range(1, 6)))
print()
print("The last two differ only in the domain. That is why a theorem always")
print("states its domain, and why `x > 0` needs `x in N` attached to be true.")
```

### A formula with `S` in it is a template

```python
import math


def mean_and_std(values):
    """mu = (1/|S|) sum over s in S of s, and sigma^2 = (1/|S|) sum (s-mu)^2."""
    n = len(values)                                   # |S|
    mu = sum(values) / n                               # (1/|S|) sum s
    var = sum((x - mu) ** 2 for x in values) / n       # (1/|S|) sum (x-mu)^2
    return mu, var, math.sqrt(var)


print("== mean_and_std read straight off the formula ==")
for values in ([12, 15, 15, 18, 30], [4], [10, 10, 10, 10]):
    mu, var, sigma = mean_and_std(values)
    print(f"  S = {str(values):<22} mu = {mu:7.4f}  var = {var:7.4f}  sigma = {sigma:7.4f}")

print()
print("The empty set is the special case the formula hides:")
print("  |S| = 0 makes (1/|S|) = 1/0, which is undefined, not zero.")
print("  So `mean([])` must be handled by an explicit branch.")


def safe_mean_and_std(values):
    """Same formula, with the |S| = 0 case written down instead of ignored."""
    if len(values) == 0:
        return None, None, None       # the formula has no value on S = {}
    return mean_and_std(values)


print()
print("With the empty case handled explicitly:")
for values in ([], [4], [12, 15, 15, 18, 30]):
    mu, var, sigma = safe_mean_and_std(values)
    print(f"  S = {str(values):<22} mu = {str(mu):>7}  var = {str(var):>7}  sigma = {str(sigma):>8}")
```

### Subscripts, superscripts, and scope

```python
# a_i means "the i-th a". The subscript is a lookup key, not an exponent.
a = [10, 20, 30, 40]
print("a =", a)
for idx in range(len(a)):
    print(f"  a_{{{idx}}} = {a[idx]}   (read aloud: 'a sub {idx}')")
print("Python indexes from 0; this notation usually starts at 1, so a_1 =", a[0])
print()

# f^2(x) means APPLY f TWICE in this book, not square it. In linear algebra
# f^2(x) would mean the squared value. Context decides, which is the problem.
def f(x: int) -> int:
    """The function x -> x + 1."""
    return x + 1


x = 3
print("f(x)        =", f(x))
print("f(f(x))     =", f(f(x)), " <- this is what f^2(x) means here")
print("x^2         =", x ** 2, " <- but ^2 means square on the thing to its left")
print("The difference: f^2 is a superscript on a FUNCTION, x^2 on a NUMBER.")
print()

# A superscript that is not a power: A^T is the transpose of A, rows for columns.
A = [[1, 2], [3, 4]]
A_T = [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]
print("A   =", A)
print("A^T =", A_T, "  <- rows and columns swapped, NOT squared")
print()

# Two different variables in similar hats. x_i is one sample; x_bar is the mean
# of all samples. Confusing them is one of the most common notation slips.
xs = [2, 4, 4, 4, 5, 5, 7, 9]
x_bar = sum(xs) / len(xs)
print("x_i values  :", xs)
print(f"x_bar       = {x_bar}")
print(f"sum(x_i)    = {sum(xs)}")
print(f"n * x_bar   = {len(xs) * x_bar}")
print("The last two agree because that IS the definition of x_bar.")
print()


# Free versus bound variables, in a function where Python's scoping is visible.
def sigma_of_i_to_n(n: int) -> int:
    """sum over i=1..n of i. The i is created and destroyed inside here."""
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


print("sigma_of_i_to_n(5) =", sigma_of_i_to_n(5), "which is 1+2+3+4+5")


def try_to_use_the_loop_variable():
    """A separate scope, so Python cannot hand us a leaked `i`."""
    try:
        return i
    except NameError as err:
        return f"NameError: {err}"


print("peeking at i after the loop ->", try_to_use_the_loop_variable())
print("That is what 'i is bound by the summation' means. In Python the binding")
print("is a function local, not 'whatever was left over by the last loop'.")
print()

# A formula with a free variable is a FUNCTION until you pin the free variable.
def f_of_x(x):
    """The formula x^2 + 1, with x free."""
    return x * x + 1


print("x^2 + 1 is a formula, not a number. Pin x and it becomes a number:")
for xv in (0, 2, 5):
    print(f"  x = {xv}  ->  x^2 + 1 = {f_of_x(xv)}")
```

### Translating a definition into code, clause by clause

```python
# Definition:
#   A number p > 1 is PRIME if and only if, for every integer d with 1 < d < p,
#   p mod d != 0.
#
#   "a number p > 1"                    -> the domain and the guard
#   "for every d with 1 < d < p"        -> a loop over range(2, p)
#   "p mod d != 0"                      -> the predicate; "for every" means AND
def is_prime(p: int) -> bool:
    if p <= 1:                          # the "p > 1" clause, as a guard
        return False
    for d in range(2, p):
        if p % d == 0:
            return False                # one counterexample is enough to fail
    return True                         # "for every" holds only if none failed


print("== is_prime ==")
print("  primes up to 30:", [n for n in range(2, 31) if is_prime(n)])
print("  the guard matters:", "is_prime(1) =", is_prime(1),
      "is_prime(0) =", is_prime(0), "is_prime(-7) =", is_prime(-7))
print()
print("  Drop the `p <= 1` guard and the definition breaks subtly. For p = -4,")
print("  range(2, -4) is EMPTY, so the loop body never runs and a naive")
print("  translation returns True. -4 is not prime. This is a vacuous truth:")
print("  'for every d in the empty set, P(d)' is true for any P.")
print()


# Definition:
#   A set C is a CLIQUE of an undirected graph G if and only if, for every pair
#   of DISTINCT vertices u, v in C, the edge (u, v) is in G.
#
#   "for every pair" means nested iteration; "distinct" means only take i < j.
def is_clique(graph, candidate) -> bool:
    vertices = list(candidate)
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):    # j > i guarantees distinct
            if (vertices[i], vertices[j]) not in graph:
                return False
    return True


graph = {("a", "b"), ("a", "c"), ("b", "c"), ("c", "d"), ("d", "e")}
print("== is_clique ==")
print("  edges:", sorted(graph))
for candidate in (["a", "b"], ["a", "b", "c"], ["a", "b", "c", "d"], ["c", "d", "e"]):
    print(f"  {str(candidate):<22} is a clique: {is_clique(graph, candidate)}")
print("  {a,b,c} qualifies: all three edges are present.")
print("  {a,b,c,d} does not: the edge (a,d) is missing.")
print()


# Definition:
#   gcd(a, b) is the LARGEST value d such that d divides a, d divides b, and d > 0.
#
# Two readings of the same definition, two different implementations.
def gcd_by_search(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    best = 1
    for d in range(1, max(a, b) + 1):
        if a % d == 0 and b % d == 0:
            best = d                     # keep overwriting; the last one wins
    return best


def gcd_by_euclid(a: int, b: int) -> int:
    """The same definition, read as 'keep shrinking until the answer appears'."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


print("== gcd, two readings of one definition ==")
print(f"{'(a, b)':>14} {'by search':>10} {'by Euclid':>10} {'agree':>6}")
for a, b in ((12, 18), (17, 5), (270, 192), (0, 7), (13, 13)):
    s, e = gcd_by_search(a, b), gcd_by_euclid(a, b)
    print(f"{f'({a}, {b})':>14} {s:>10} {e:>10} {str(s == e):>6}")
print()
print("Both answer the same definition. One costs O(max(a,b)), the other")
print("O(log min(a,b)). Same meaning, different cost. That is the whole game:")
print("a definition fixes WHAT, an implementation picks HOW.")
```

## Common Mistakes

**Wrong: reading `f^2(x)` as "the square of f of x."**
Right: in this book `f^2` on a *function* means compose it with itself, so
`f^2(x) = f(f(x))`. On a *number*, `x^2` means square. The superscript means
"two of that thing", and what counts as "two of" depends on what kind of object
sits underneath.
Why tempting: the mark is identical in both cases and Python's `**` does only
one of the two jobs, so a programmer's instinct is to assume the marks match.
They do not.

**Wrong: treating `x > 0` as a statement that is simply true or false.**
Right: it is true for some `x` and false for others, so as written it is not a
statement at all. You need a quantifier and a domain: `∀x ∈ ℕ, x > 0` is true,
`∀x ∈ ℤ, x > 0` is false. Textbooks are not being sloppy when they drop the
quantifier; they have declared the domain in the surrounding prose.
Why tempting: the formula looks complete, and readers supply the missing
information from context without noticing they did.

**Wrong: expanding `Σ` as `for i in range(n)`.**
Right: `Σ_{i=1}^{n}` starts at 1 and includes `n`, so it is
`range(1, n + 1)`. `Σ_{i=0}^{n-1}` is `range(n)`. Off-by-one errors in
translated mathematics almost always come from the bounds line under the sigma,
and the bounds line is the first thing to read.
Why tempting: Python's `range(n)` is the more common shape in code, so it is the
more likely reflex.

**Wrong: assuming a script letter names a specific set.**
Right: `S` is a placeholder for *some* set you supply. `Σ_{s∈S} s` is not a
number until you say what `S` is, and the mean formula divides by `|S|`, which
is undefined when `S` is empty. That hidden division is a real bug source, not a
pedantic point.
Why tempting: the letter looks like a name of a specific thing rather than a
slot, and most textbook examples never hit the degenerate case.

**Wrong: reading `A ⊆ B` as "A is a subset of B, possibly equal."**
Right: that is right, and it is the thing people get wrong in the *other*
direction. `A ⊂ B` is often used by authors to mean a proper subset, and just as
often to mean ordinary subset. Check the author's convention before relying on
it. This particular ambiguity is one of the few genuinely indefensible ones in
mathematical writing.
Why tempting: the strict/non-strict subset pair is the standard convention in
most texts, so a programmer who has seen `<` versus `<=` will project it and be
right more often than not, which cements the habit of not checking.

**Wrong: assuming a formula's free variables are "the inputs".**
Right: a formula may have several, some of which are bound and some free, and a
free variable may not be a number at all. `A^T` has a free matrix variable.
`x ∈ ℤ` has a free variable `x` whose domain is stated by `ℤ`. Identifying the
free variables and their types is the first step of reading anything, and
getting it wrong makes the rest unreadable.
Why tempting: it is a habit from function signatures, and it usually works, so
the failures are rare and hard to attribute.

## Formula Sheet

This lesson introduces no mathematics of its own — it introduces the *marks* —
so this table is a translation table. Every notation the lesson shows up,
including the ones that only appear in the Common Mistakes section, because those
are the ones that trip people up.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$\{x \in S : P(x)\}$` | read `S` left to right, `P(x)` right of the colon | build the set of everything in `S` that satisfies `P` | set comprehension. The colon is Python's `for` **plus** `if`: `{x for x in S if P(x)}` |
| `$x \in S$` | | `x` is one of the members of `S` | stating a domain, as in `x ∈ ℤ` |
| `$A \subseteq B$` | every `$a$` with `$a \in A$` also has `$a \in B$` | every member of `A` is in `B`, and `A` may equal `B` | the non-strict reading, which is standard. `A ⊂ B` may mean *proper* subset or just subset depending on the author — **check the convention** |
| `$\Sigma_{i=1}^{n} g(i)$` | | add up `g(i)` for `i` counting `1, 2, 3, …, n` | every running total in the course. `range(1, n + 1)`, **not** `range(n)` |
| `$\Sigma_{i=0}^{n-1} g(i)$` | | the same sum with zero-based bounds | the shape Python actually uses, and why the two conventions produce off-by-one bugs |
| `$\Pi_{i=1}^{n} a_i$` | | multiply `a_1 · a_2 · … · a_n` | products, and `n!` which is `Π_{i=1}^{n} i` |
| `$f(n) = O(g(n))$` | `$\exists c>0,\ n_0>0:\ \forall n \ge n_0,\ f(n) \le c\,g(n)$` | past some threshold, `f` never exceeds a fixed multiple of `g` | growth claims. About the limit, never about milliseconds. `Θ` additionally requires a matching lower bound |
| `$\forall x \in D,\ P(x)$` | | every `x` in domain `D` satisfies `P` | `all(...)`. **The domain `D` is part of the claim**: `∀x ∈ ℕ, x > 0` is true, `∀x ∈ ℤ, x > 0` is false |
| `$\exists x \in D,\ P(x)$` | | at least one `x` in `D` satisfies `P` | `any(...)`. True over an empty domain, and that is a real answer, not an error |
| `$\neg(\forall x \in D,\ P(x)) \iff \exists x \in D,\ \neg P(x)$` | | "not every" is the same claim as "some … not" | negating a quantifier flips it **and** negates the predicate. Both are `True` in the lesson's user example |
| `$\mu = \frac{1}{\lvert S\rvert}\Sigma_{s \in S} s$` | | the average of `S` | the mean. **Undefined when `S` is empty** — the `1/0` is the hidden bug, so the empty case is a real branch, not a pedantic point |
| `$\sigma^2 = \frac{1}{\lvert S\rvert}\Sigma_{s \in S} (s - \mu)^2$` | | average squared distance from the mean | variance. Divides by `$\lvert S\rvert$`, not `$\lvert S\rvert - 1$` — population, not sample |
| `$\lceil x \rceil$`, `$\lfloor x \rfloor$` | | `x` rounded up; `x` rounded down | index arithmetic, and $\lfloor \log_2 n \rfloor$ = how many times you can halve `n` = `n.bit_length() - 1` |
| `$\lvert x \rvert$` | | absolute value | on a number. **`$f^{-1}$` is not `$1/f$`** — see the next two rows |
| `$\lvert S \rvert$` | | how many elements `S` has | `len(S)`. A different meaning from the row above, and the two marks are identical |
| `$f \circ g$` | `$f(g(x))$$ | apply `g` first, then `f` | composition. **Not commutative**: the lesson's `f(v)=v*10` and `g(v)=v+3` give `f∘g(3) = 60` but `g∘f(3) = 33` |
| `$f^{-1}$` | | the function that undoes `f` | the inverse *function*. With `f(v) = 10v`, `f⁻¹(70) = 10`, while `$1/f(7) ≈ 0.0143$` |
| `$A^{T}$` | | flip rows and columns | the transpose. A superscript that is **not** a power — same mark as `x²`, different meaning |
| `$f^{2}$` (on a function) | `$f(f(x))$` | `f` applied twice | composition, in this book. Contrast `$x^{2}$` on a *number*, which is squaring. The mark is identical; the meaning depends on what sits underneath |
| `$a \mid b$` | `$\exists k \in \mathbb{Z},\ b = ak$` | `b` is a whole multiple of `a` | divisibility. Reads "a divides b" |
| `$x \bmod m$`, `$x \equiv r \pmod m$` | `$m \mid (x - r)$` | remainder; or "x and r leave the same remainder" | congruences, hashing, and the worked example's set builder |
| `$x \equiv 3 \pmod{5^{2}}$` | | `x` and 3 agree mod **25**, not mod 5 | the Worked Example. `(mod 5)` is a trailing qualifier like a unit suffix, so the exponent applies to the modulus. The two readings give sets of 5 and 24 members in the window used |
| `$x^{2} + 1$` with `x` free | | a *function* of `x`, not a number | any formula with a free variable. Calling it with `x = 0, 2, 5` gives `1, 5, 26` |
| bound variable | introduced by `∀`, `∃`, `Σ_{i=…}`, set-builder braces | a name fixed inside its own subpart and destroyed with it | a Python function parameter or loop variable. `i` under a summation is a function local, not "whatever the last loop left" |
| free variable | not introduced by any binder | its value comes from outside, so the formula is a function of it | a Python name resolved from an enclosing scope. Finding the free variables and their types is the first step of reading anything |
| vacuous truth | "for every `x` in `∅`, `P(x)`" | true, because there is no `x` to fail | the trap in the `is_prime` guard: dropping `p > 1` makes `range(2, -4)` empty, and a naive translation returns `True` for `-4`, which is not prime |

## Multiple Choice Questions

**Q1.** A textbook writes `f²(x)` where `f` is a function from the reals to the
reals, and elsewhere writes `x²` in the same paragraph. Which reading of `f²(x)`
does this lesson use?

- A) The square of the value `f(x)`
- B) `f` applied to itself twice, that is `f(f(x))`
- C) The function whose output is the square of its input
- D) Undefined, because the superscript 2 is reserved for real powers

<details>
<summary>Answer and explanation</summary>

**B) `f` applied to itself twice, that is `f(f(x))`.**

A superscript means "that many of the thing underneath". What counts as "the
thing underneath" depends on its kind. On a *function* you can only ask for two
of the function, which is composition. On a *number* you can ask for two of the
number, which is squaring. The lesson's own code shows it: with `f(x) = x + 1`
and `x = 3`, `f(f(x))` is `5` while `x²` is `9`.

A is the error the lesson's first Common Mistake is about. Python's `**` only
does squaring, so a programmer's instinct is to assume the marks mean the same
thing. They do not, and the two readings can give wildly different answers — the
lesson's Exercise 3 gets `32` and `209` from the same expression.

C is a different mistake: it confuses the exponent on the function with the
exponent on the output. A function squared pointwise is a third thing again, and
it is not what `f²` means.

D is wrong because the mark is perfectly well defined once you know what it is
attached to. That is the entire method of the lesson.

</details>

**Q2.** The lesson's `is_prime` includes a guard `if p <= 1: return False`. The
Common Mistakes section says that dropping it breaks subtly. What exactly goes
wrong, and for which input?

- A) `range(2, p)` raises a `ValueError` for `p < 2`, so the function crashes
- B) For `p = -4` the range is empty, the loop body never runs, and a naive translation returns `True` — a vacuous truth, and `-4` is not prime
- C) For `p = 0` the function enters an infinite loop, because `p % d == 0` holds for every `d`
- D) Nothing breaks: `range` handles small bounds correctly, so `is_prime(-4)` still returns `False`

<details>
<summary>Answer and explanation</summary>

**B) For `p = -4` the range is empty, the loop body never runs, and a naive
translation returns `True` — a vacuous truth, and `-4` is not prime.**

`range(2, -4)` is empty, so the loop over divisors never executes, the function
falls through to `return True`, and it reports that a negative even number is
prime. The definition being translated is *"p > 1 is prime if and only if for
every integer `d` with `1 < d < p`, `p mod d ≠ 0`"*. There is no `d` satisfying
`1 < d < -4`, so the universal statement is true of the empty set — vacuously.
The guard `p > 1` in the definition is a real clause, and it has to become a
real guard in the code.

A is wrong: `range` with a start above its stop is simply empty, no exception.
`range(2, -4)` evaluates to `[]`.

C is wrong: the loop is over `range(2, p)`, so for `p = 0` it does not run at
all, and the function returns immediately. There is no iteration to be infinite.

D is exactly the bug. It is the most dangerous shape of this error because the
function still returns a plausible `bool` and nothing crashes; the failure is a
wrong `True` for `0`, `1`, and every negative number, which is why
`is_prime(0)` and `is_prime(-7)` are printed in the lesson as a check that the
guard is doing work.

</details>

**Q3.** In the lesson's Python table, the mathematics column says "bound
variable" and the Python column says "a function parameter or loop variable". What
does the lesson demonstrate about a bound variable that justifies that row?

- A) That `i` remains accessible after the summation or loop that bound it
- B) That the binding is scoped to the subpart that created it, so `i` cannot be read outside — the same as a function local
- C) That `i` must be assigned before the loop begins
- D) That a bound variable has no value until the outer function returns

<details>
<summary>Answer and explanation</summary>

**B) That the binding is scoped to the subpart that created it, so `i` cannot be
read outside — the same as a function local.**

The lesson's `try_to_use_the_loop_variable` returns the string `"NameError:
name 'i' is not defined"` after `sigma_of_i_to_n(5)` has run. That is the direct
evidence. "Bound by the summation" means *this subpart introduces it and this
subpart is its whole life* — exactly what a Python function parameter or `for`
target does.

A is the belief the section exists to correct, and it is the mistake made by
people coming from languages where a loop variable leaks. In Python the binding
is a function local, not "whatever was left over by the last loop".

C is a mechanical Python rule, not the mathematical point, and it is not even
what the code does — `for i in range(...)` creates the binding itself.

D inverts the meaning entirely. A bound variable has a value *throughout* the
binder's body; it is only afterwards that it ceases to exist.

</details>

**Q4.** The lesson prints that the mean of `[12, 15, 15, 18, 30]` is `18.0` and
its variance is `39.6`. What would `safe_mean_and_std([])` return, and why?

- A) `(0.0, 0.0, 0.0)`, because the sum over the empty set is 0 and so is the sum of squares
- B) `(None, None, None)`, because the formula divides by `$|S| = 0$` and the result is undefined, not zero
- C) A `ZeroDivisionError`, because the lesson does not add a guard
- D) `(0.0, 0.0, 0.0)`, because the empty set is the identity element for both sum and product

<details>
<summary>Answer and explanation</summary>

**B) `(None, None, None)`, because the formula divides by `$|S| = 0$` and the
result is undefined, not zero.**

`safe_mean_and_std` begins with `if len(values) == 0: return None, None, None`,
with the comment "the formula has no value on S = {}". That is the whole point of
the function. The mean is `$\frac{1}{\lvert S\rvert}\Sigma_{s\in S} s$`, and with
`$\lvert S\rvert = 0$` the prefactor is `1/0`. The sum in the numerator really
is 0, so the numerator is not the problem; the division is.

A and D both reason that the sums are 0 and conclude 0. That is the seductive
error, and it is why the lesson calls this "a real bug source, not a pedantic
point". Returning `0.0` for the mean of nothing silently fabricates a data point
at the origin, and any downstream standard deviation is then wrong too.

C is wrong because the guard exists precisely to prevent the division. The
lesson's `mean_and_std` would raise; `safe_mean_and_std` is the version with the
degenerate case written down instead of ignored. The distinction between the two
functions is the lesson's point in four lines.

</details>

**Q5.** The challenge table reports `f ∘ g` at `3` gives `60`, and the prose says
`g ∘ f` at `3` gives `33`. With `f(v) = 10v` and `g(v) = v + 3`, which
computation is which, and what does the difference teach?

- A) `f ∘ g(3) = 60 = 10 × (3 + 3)`, so composition is not commutative and the `∘` symbol fixes the order
- B) Both give `33`; the `60` is a rounding artifact
- C) `f ∘ g(3) = 33` and `g ∘ f(3) = 60`, so the symbol is read right to left
- D) Composition is commutative, and the difference comes from integer overflow

<details>
<summary>Answer and explanation</summary>

**A) `f ∘ g(3) = 60 = 10 × (3 + 3)`, so composition is not commutative and the
`∘` symbol fixes the order.**

`f ∘ g` means "apply `g`, then `f`", so `f(g(3)) = f(6) = 60`. The other order is
`g(f(3)) = g(30) = 33`. The `∘` symbol is read like a product sign, left to right,
and it is the *innermost* function that runs first.

B is wrong because the two values are exact integers, and the code computes them
independently. `60` and `33` are not close enough to be a rounding difference.

C reverses the convention. Reading `f ∘ g` as "`f` first, then `g`" is the
single most common error in reading composition, and it is the error the symbol
exists to prevent.

D is wrong on two counts: the values are small, and commutativity is a genuine
mathematical property that happens to fail here. The general statement is the
useful one: composition fails to commute because `f(g(x))` and `g(f(x))` are
different functions. Matrix products in Part 03 inherit exactly this asymmetry,
and it is why `AB` and `BA` have different eigenvalues.

</details>

**Q6.** The lesson prints `∀x ∈ [-5, 5], x² ≥ 0` as `True` and
`∀x ∈ [-5, 5], x > 0` as `False`, then notes the two `x > 0` lines differ only in
domain. What does that comparison establish?

- A) That the predicate `x > 0` is false
- B) That a quantifier's truth value depends on both the predicate and the domain, so the domain must always be written down
- C) That `x² ≥ 0` holds over every domain you could choose
- D) That `∀x ∈ [1, 5], x > 0` is `False` because 1 is not greater than 0

<details>
<summary>Answer and explanation</summary>

**B) That a quantifier's truth value depends on both the predicate and the domain,
so the domain must always be written down.**

The two `x > 0` lines are `all(x > 0 for x in range(-5, 6))` → `False` and
`all(x > 0 for x in range(1, 6))` → `True`. Same predicate, same code shape,
different range, different truth value. The claim `x > 0` on its own is not a
statement at all — it is a function of `x` that is true for some values and false
for others.

A confuses the truth value of the quantifier with the truth value of the
predicate. `x > 0` is true at `x = 1` and false at `x = 0`; the `False` is about
the universal statement over `[-5, 5]`, not about the relation.

C goes the other way. `x² ≥ 0` is `True` over `[-5, 5]` and would be `True` over
the integers and the reals as well, since a real square is non-negative — but that
is a fact about squares, not a fact about domains being irrelevant. A domain can
always change a universal claim; the fact that one particular predicate is
insensitive to this domain is luck, not principle.

D is simply false: `1 > 0` holds, and all five elements of `{1,2,3,4,5}` are
positive. The line prints `True`. This is the trap in reverse — inventing a
failure where the code found a success.

</details>

**Q7.** The lesson says `Σ_{i=1}^{n}` translates to `range(1, n + 1)` and calls
off-by-one errors in translated mathematics "almost always" a mistake in reading
the bounds line. Which computation is the one that follows the notation as
written?

- A) `sum(i * i for i in range(n))` for `Σ_{i=1}^{n} i²`, giving `0` for `n = 1`
- B) `sum(i * i for i in range(1, n + 1))` for `Σ_{i=1}^{n} i²`, giving `1` for `n = 1`
- C) `sum(i * i for i in range(0, n))` for `Σ_{i=1}^{n} i²`, which is the same as B
- D) `sum(i * i for i in range(1, n))` for `Σ_{i=1}^{n} i²`, giving `1` for `n = 1`

<details>
<summary>Answer and explanation</summary>

**B) `sum(i * i for i in range(1, n + 1))` for `Σ_{i=1}^{n} i²`, giving `1` for
`n = 1`.**

The bounds under the sigma are inclusive at both ends: `i` takes the values
`1, 2, …, n`, and `n` terms are added. Python's `range` is half-open, so the
upper bound must be `n + 1`. The lesson's `sum_squares_as_written` does exactly
this and its table confirms it: `n = 1` gives `1`, and it agrees with the closed
form `n(n+1)(2n+1)/6` at `n = 1, 2, 5, 10, 100, 1000`.

A and C use `range(n)`, which is `0, 1, …, n-1` — the translation of
`Σ_{i=0}^{n-1}`, a genuinely different sum. For `n = 1` it adds only `0²`, giving
`0`, which is where the off-by-one shows up most starkly. The reason this is
tempting is that `range(n)` is the more common shape in real Python, so it is
the stronger reflex; the lesson's Common Mistakes section says exactly that.

D excludes the last term, so it is `Σ_{i=1}^{n-1}`, not `Σ_{i=1}^{n}`. It happens
to give the right answer at `n = 1` for the wrong reason — both compute an empty
sum — which is the worst kind of off-by-one: it passes the smallest test and fails
everywhere else. At `n = 5` it gives `30` where the notation says `55`.

</details>

**Q8.** The lesson distinguishes `f⁻¹` from `1/f`, and its Challenge table prints
a value for `f⁻¹(70)` alongside `1/f(7) ≈ 0.0143`. Which statement about `f⁻¹` is
correct?

- A) `f⁻¹` is always the reciprocal `1/f`, just written more neatly
- B) `f⁻¹` is a function that undoes `f`, defined by `f⁻¹(y) = x` whenever `f(x) = y`, and it exists as a total function only when `f` is one-to-one
- C) `f⁻¹` exists for every function, and `1/f` is the notation for the same thing
- D) `f⁻¹` means "the derivative of `f` to the power minus one", a shorthand used in calculus

<details>
<summary>Answer and explanation</summary>

**B) `f⁻¹` is a function that undoes `f`, defined by `f⁻¹(y) = x` whenever
`f(x) = y`, and it exists as a total function only when `f` is one-to-one.**

The definition is the whole content: `f⁻¹` takes an *output* of `f` and returns
the *input* that produced it. For `f(v) = 10v` that means `70` came from `7`, so
`f⁻¹(70) = 7`. The lesson's table reaches `10` because its `inv` binding is
`v // 7`, the inverse of a *differently scaled* map — the number in the table is a
consequence of the particular binding, and the shape of the definition is what
transfers. Note also that `1/f(7) = 0.0143` takes an *input* and divides it; it is
not an inverse of anything, and the two objects are not even the same type — one
is integer-valued, the other a real number.

A and C are the misconception this row exists for, and it is a reasonable one:
`-1` as a superscript means reciprocal everywhere else you meet it. It is also
why matrix inverse is written `A⁻¹` rather than `1/A`; the lesson says so
directly.

D is wrong, and the symbol confusion explains the error. The derivative of `f` is
`f'`, never `f⁻¹`. There is no accepted notation `f⁻¹` for a derivative.

The domain restriction in the "when you use it" column is load-bearing, not
decoration. For `f(x) = x²` on the reals, `f⁻¹` is not a function at all:
`f(2) = f(-2) = 4`, so there is no single answer to "what went in". You must
restrict to non-negative reals, where `f⁻¹(x) = √x`. This is exactly why the
lesson's Challenge cannot mark `f⁻¹` computable in general — it has to supply an
explicit binding for `f` first, and whether `f⁻¹` exists at all depends on
whether that `f` is injective.

</details>

**Q9.** The lesson's `## The Formal Version` says a formula is a *function* of its
free variables, and gives `x² + 1` as the example. Which statement follows?

- A) `x² + 1` is not a well-formed expression until `x` is assigned
- B) `x² + 1` is a well-formed but unevaluated object; it becomes a number when you supply `x`, and the lesson prints `1, 5, 26` for `x = 0, 2, 5`
- C) `x² + 1` is a syntax error, because a formula cannot appear without a quantifier
- D) `x² + 1` denotes the *set* of all values it can take as `x` ranges over the reals

<details>
<summary>Answer and explanation</summary>

**B) `x² + 1` is a well-formed but unevaluated object; it becomes a number when
you supply `x`, and the lesson prints `1, 5, 26` for `x = 0, 2, 5`.**

This is the point of the "free variable" definition, and it is the exact analogue
of a Python function that has been defined but not called. `f_of_x` exists the
moment the `def` completes; it produces nothing until you invoke it. The lesson
says "this is why textbooks distinguish a formula from a function at all, and it
is not a distinction you need to make in code."

A is close but wrong in an important way. Nothing is malformed; the expression is
complete. What is missing is a *value*, not a *binding*. This is precisely the
distinction the lesson's Python table draws: substituting a value for a free
variable corresponds to calling the function, and calling is optional.

C is wrong. Quantifiers are frequently absent, and the lesson's second Common
Mistake is about exactly that: textbooks often drop the quantifier and declare
the domain in prose. `x² + 1` is a perfectly standard piece of mathematical
writing.

D confuses a formula with the set of its values. That set is indeed `[1, ∞)` here,
but the notation `x² + 1` denotes the function, and you have to write the set
explicitly — the formula and its range are two different objects, which is what
the free/bound distinction is for.

</details>

**Q10.** The lesson's `## Why Computer Science Cares` opens with "if you cannot
read `∀x ∈ S, P(x) ⟹ Q(x)`, you cannot review a specification". Which concrete
task does that sentence describe?

- A) Writing a type annotation in Python and having the checker accept it
- B) Checking that a stated property of a system holds for every element of a state space, which is the core loop of verification tools like Dafny and Frama-C
- C) Choosing between two hash functions by timing them
- D) Formatting a table of benchmark results in a README

<details>
<summary>Answer and explanation</summary>

**B) Checking that a stated property of a system holds for every element of a
state space, which is the core loop of verification tools like Dafny and
Frama-C.**

A verification condition is exactly a universally quantified implication: *for
every reachable state `s`, and every input `x`, if the precondition `P` holds then
the postcondition `Q` holds.* The loop invariant in a Dafny or Frama-C proof is
`∀ state: precondition → invariant`, and the tool discharges it mechanically.
The lesson's Lesson 00 makes the same point in its eighth example: program
correctness is a logical statement, and a statement with finitely many cases can
be checked on all of them.

A is the nearest wrong answer and worth distinguishing. A type annotation is a
statement about a *single* value's shape, checked locally; it is not universally
quantified over a state space, and it says nothing about behaviour. This is why
"it type-checks" and "it is correct" are different claims.

C and D are not about quantification at all. Timing and formatting are
measurements and presentation; the lesson is making a claim about what you can
*reason about*, not about what you can measure or display.

</details>

## Subjective Questions

### Short Answer

**Q1. In one sentence each, what is a bound variable and what is a free
variable?**

<details>
<summary>Answer</summary>

A variable is **bound** in a formula when some subpart of the formula introduces
it and fixes its meaning within that subpart — the `i` in `Σ_{i=1}^{n} i²`, the
`x` in `{x ∈ S : P(x)}`.

A variable is **free** when its meaning depends on a value supplied from outside
— the `x` in `x² + 1`, or the `S` in `μ = (1/|S|) Σ_{s∈S} s`.

A formula is a function of its free variables, which is exactly the Python
analogue of a function that has been defined but not yet called.

</details>

**Q2. What does the colon in set-builder notation `{x ∈ S : P(x)}` translate to in
Python, and what do its two halves correspond to?**

<details>
<summary>Answer</summary>

The colon translates to `for` **plus** `if`: `{x for x in S if P(x)}`.

The half to the left of the colon — usually `x ∈ S`, or just `S` — is what you are
building, and it is the iterable in the `for`. The half to the right is the
condition, and it is the `if`.

Note the two halves are not symmetric: the left names the *type* of thing being
built as well as the domain, and the right is a predicate in that same variable.
`x ∈ ℤ` is a domain declaration, not part of the condition.

</details>

**Q3. `∀x ∈ ℤ, x² ≥ x` is true. Show why with a factorisation, and then contrast it
with the lesson's Exercise 1 item 4, `∀x ∈ {1,2,3,4}, x² > x`, which is false.**

<details>
<summary>Answer</summary>

`x² ≥ x` is equivalent to `x² - x ≥ 0`, that is `x(x - 1) ≥ 0`. The product of
two factors is non-negative when they have the same sign, which here means
`x ≤ 0` or `x ≥ 1`. Every integer is in one of those two ranges, so the universal
claim holds.

Exercise 1 item 4 uses the *strict* `>` instead. At `x = 1` it asks whether
`1 > 1`, which is false, and one counterexample is enough to falsify a universal
claim. So `all(x * x > x for x in (1, 2, 3, 4))` is `False` while
`all(x * x >= x for x in range(-5, 6))` is `True`.

The two differ in two places at once — the operator and the domain — which is the
point: a truth value is a property of the whole statement, not of the predicate
alone.

</details>

**Q4. Why does the mean formula `μ = (1/|S|) Σ_{s∈S} s` need an explicit empty-set
branch in code, even though the sum in the numerator is 0?**

<details>
<summary>Answer</summary>

Because the numerator being 0 does not save you: the formula divides by
`$|S|$`, and `$|S| = 0$` makes the prefactor `1/0`. The mean of the empty set is
*undefined*, not zero — there is no element to average, so there is no average.

The lesson's `mean_and_std` raises `ZeroDivisionError`; `safe_mean_and_std` adds
`if len(values) == 0: return None, None, None`. Writing the degenerate case down
is a real design decision, because returning `0.0` would fabricate a data point
and corrupt every downstream statistic.

</details>

**Q5. In the lesson's users example, which user breaks `∀u : active(u)`, and what
does the equivalence `¬∀u active(u) ↔ ∃u ¬active(u)` compute?**

<details>
<summary>Answer</summary>

`linus` breaks it — he is the only user with `"active": False`.

Both sides of the equivalence compute `True`: `not all(u["active"] for u in
users)` is `True`, and `any(not u["active"] for u in users)` is `True`. That is
the quantifier-negation rule in action, and it is the rule you use to find a
counterexample: negating a universal claim produces an existential claim, which
in Python is a *search* rather than a sweep. `any` short-circuits on the first
failure; `all` has to visit every element before it can return `True`.

</details>

**Q6. What is the difference between `f ∘ g` and `f(g(x))` as notations, and what
is the difference between them as mathematics?**

<details>
<summary>Answer</summary>

As notations, none that matter: `f ∘ g` and `f(g(x))` denote the same function.
`f ∘ g` is a name for the whole composed function; `f(g(x))` is its value at `x`.

As mathematics, the pair `(f, g)` determines an *order*. `f ∘ g` applies `g`
first. Composition is not commutative, and the lesson's numbers show it: with
`f(v) = 10v` and `g(v) = v + 3`, `f ∘ g(3) = 60` while `g ∘ f(3) = 33`.

Reading `f ∘ g` as "f first" is the standard error, and the `∘` symbol exists
precisely to prevent it.

</details>

### Long Answer

**Q1. The lesson's `is_prime` has an explicit `if p <= 1` guard, and its
Common Mistakes section calls dropping the guard a subtle break. Explain what the
guard is doing mathematically, why removing it produces a *wrong true* rather than
a crash, and what general rule about translating definitions this illustrates.**

<details>
<summary>Model answer</summary>

**What the guard is doing mathematically.** The definition being translated is
not "a number is prime if no divisor in `1 < d < n` divides it". It is "**a
number `p > 1`** is prime if and only if for every integer `d` with `1 < d < p`,
`p mod d ≠ 0`". The clause `p > 1` is part of the definition, not a defensive
programming addition. It says the property is only being *asserted* about numbers
above 1; below 1 the definition is silent, and silence is not a licence to assert.

**Why removal gives a wrong `True` rather than a crash.** The loop is
`for d in range(2, p)`. For `p = -4` that range is empty — `range(2, -4)` is
`[]` — so the body never runs and control falls through to `return True`. Nothing
raises. The returned `bool` is well typed and plausible; it is simply the wrong
answer. The same happens for `p = 0` and `p = 1`.

**The deeper reason: vacuous truth.** A universal statement over an empty set is
true, because there is no element that fails the predicate. `∀d ∈ ∅, P(d)` holds
for every `P`. Python's `all` has exactly this behaviour: `all([])` is `True`. So
the translation is *faithful to the quantification it was given* — and the
quantification it was given is wrong, because the guard was dropped upstream. The
bug is not in the loop. It is in reading the definition as a bare universal
quantifier and forgetting the domain restriction on `p` itself.

**The general rule.** When you translate a definition into code, the *guard
clauses* of the definition become real branches, and they are as much a part of
the claim as the predicate. Concretely, in order: name the domain and turn it
into a guard; turn "for every" into a loop over that domain; turn "there exists"
into a search; and then check whether the domain you chose can be empty — because
over an empty domain every universal statement is vacuously true and every
existential statement is false. A definition that has no guard is a definition
that will be read as a universal claim over whatever range the code happens to
produce.

The diagnostic that catches this class of bug is the one the lesson prints:
`is_prime(1)`, `is_prime(0)`, `is_prime(-7)` all `False`. Test the boundary of
the domain, not just the interior. The same rule catches the empty-set bug in
`mean_and_std`, the `all([])` trap in every `all` over a possibly-empty iterable,
and the `0`-length list in every `sorted(...)[0]` in a codebase you have not read.

</details>

**Q2. The lesson distinguishes `|x|` (absolute value) from `|S|` (cardinality) —
the same mark with two meanings. Give a third and fourth notation in this lesson
that reuses a mark for more than one purpose, explain each pair of meanings, and
say what general habit prevents confusing them.**

<details>
<summary>Model answer</summary>

**Pair 3 and 4: `$f^{2}$` and `$x^{2}$`.** On a *function* the superscript 2 means
composition — `f(f(x))`, which the lesson's code shows as `f(f(x)) = 5` for
`f(x) = x+1` at `x = 3`. On a *number* it means squaring: `3² = 9`. Same mark,
same superscript, and Python's `**` implements only the second, which is why the
error is so common among programmers. A third entry in this family is `$A^{T}$`,
where the superscript is a *label*, not a power at all: the transpose, computed in
the lesson as `[[1, 3], [2, 4]]` from `[[1, 2], [3, 4]]`.

**The general habit.** When you hit a mark you do not recognise — or a mark you
*do* recognise in an unusual place — ask what it is attached to. That is the
lesson's own single most useful habit, stated in `In Plain Words`, and it is the
same instinct as "what type is this?" in a debugger.

Concretely, the question is always about the *kind* of object underneath:

- Is it a number or a set? Then `|x|` is magnitude and `|S|` is a count.
- Is it a function or a value? Then `f²` composes and `x²` squares.
- Is it a matrix or a number? Then `Aᵀ` flips and `A²` multiplies.
- Is it an open or a closed interval? Then `S ⊆ B` allows equality and `S ⊂ B`
  may or may not, depending on the author's convention — a genuine ambiguity that
  no habit resolves, and the lesson's advice there is to check the convention.

**Why the habit is not sufficient on its own, and what to do about the residue.**
Two cases resist the attachment test. Superscripts are the big one, because
`²` is a power on numbers, a composition on functions, and a label on matrices,
with no visual difference. Subscripts are the other: `$a_i$` is a lookup key
while `$x̄$` is a *derived* quantity (the mean of all the `$x_i$`), and confusing
the individual with the aggregate is one of the most common slips in statistics
and machine learning. For these two families, the mitigation is not a rule about
position but a rule about *provenance*: check whether the symbol is defined
somewhere earlier, and if so read that definition rather than inferring from
shape. The lesson does this with `x_i` versus `x̄` explicitly, printing both and
noting that `n * x̄` equals `Σ x_i` because that *is* the definition.

The deeper point is that notation is not self-describing. A mark is a label whose
meaning comes from a definition elsewhere in the document, which is why a
notation reference like `SYMBOLS.md` exists and why the lesson tells you to consult
it rather than trust recall. A mark you have seen in three other lessons may mean
something different in this one.

</details>

**Q3. The lesson's `## In Plain Words` says: "when you hit a symbol you do not
recognise, look at what it is attached to." Take a formula from the lesson that is
easy to misread, walk through the attachment analysis step by step, and then say
what would happen if you skipped the analysis and guessed the most common reading
in your field.**

<details>
<summary>Model answer</summary>

**The formula.** The Worked Example's `{x ∈ ℤ : x ≡ 3 (mod 5)²}`. This is a good
choice because the lesson presents it as the canonical hard case, and because a
plausible wrong reading produces an answer that is not obviously absurd on first
inspection — it only becomes absurd when you count.

**Step 1 — inventory the marks.** Braces enclosing; `∈` membership; `ℤ` the
integers; `:` "such that"; `≡` congruence; `(mod 5)` a modulus qualifier; `²` a
superscript. Every mark is now accounted for, and nothing is being read on
familiarity.

**Step 2 — find the binder and its domain.** The colon splits the formula. Left
of it, `x ∈ ℤ`: the binder is `x`, the domain is the integers, and we are
building a set. Python: `{x for x in integers if CONDITION}`.

**Step 3 — find the ambiguous attachment.** The candidates are exactly two. Is the
square on the `5`, or on the whole congruence `(x ≡ 3 mod 5)`? To decide, look at
what the parenthesis encloses: `(` closes after `5`, before the `²`. So the `²`
attaches to the completed unit `(mod 5)`, and the reading is `(x ≡ 3) (mod 25)`.

**Step 4 — decide by convention, not by guessing.** `(mod 5)` is a *trailing
qualifier*, structurally like a unit suffix. `5 m` means five metres; `x ≡ 3 (mod
5)` means the congruence is asserted modulo 5, and the whole assertion is what
carries the qualifier. Since the qualifier is the operand of the square, the
square applies to it. The reading is `x ≡ 3 (mod 25)`.

**Step 5 — compute.** `x ≡ 3 (mod 25)` means the set of all `25k + 3` for integer
`k`, which in the lesson's window is `[-47, -22, 3, 28, 53]`. Five members in
`[-60, 60)`, consistent with a modulus of 25. Had the modulus been 5, the same
window would hold 24 members — a ratio of about 5, which is itself a
confirmation, not just a curiosity.

**Step 6 — sanity-check the *type* of the answer.** The wrong reading
`(x ≡ 3 mod 5)²` squares a truth value, giving a set containing `0` and `1`. A
set of two booleans is not a set of integers, and the domain declaration `x ∈ ℤ`
demanded integers. Type-checking the result against the declared domain is a
cheap, decisive check, and the lesson uses exactly this move in its own Step 4.

**What happens if you guess instead.** The most common reading in the field — and
in any field that does not work with congruences daily — is that the superscript
belongs to the nearest preceding *value*, so `3` or the congruence as a whole.
Guessing that gives you a set of 24 members where the answer has 5, a factor of
about 5 in the wrong direction. Because both answers are "a set of integers, and
plausible-looking", nothing crashes and no type checker complains. The error
survives into downstream work: enumerate the members, use one as a modulus
elsewhere, and the compounded error is still just numbers, so it is still
invisible.

That is the real cost, and it generalises beyond notation. In every field there
is a *default* reading for an ambiguous construct, and it is the reading the
local majority uses. Guessing the default is cheap to do and produces output
that looks exactly like correct output. The attachment analysis costs a minute
and is the only thing standing between you and a confidently wrong result — which
is why the lesson promotes it from a trick to a habit.

</details>

**Q4. The lesson claims that some notation has no Python equivalent, and its
Challenge finds five: `O(f(n))`, `Θ(f(n))`, `|ℕ|`, `lim f(x)`, and a growth claim
generally. Take those five and explain, one at a time, what specifically each one
says that a Python expression cannot say. Then say what would have to be true for
`Θ(f(n))` to become checkable in code.**

<details>
<summary>Model answer</summary>

**`O(f(n))`.** The claim is that there exist constants `c` and `n₀` with
`f(n) ≤ c·g(n)` for all `n ≥ n₀`. Two quantifiers over an infinite domain: *there
exists a threshold*, and *for everything beyond it*. No Python call evaluates
that, because Python evaluates at finitely many inputs and the claim is about
what holds past a threshold nobody has specified. You cannot call it, and you
cannot loop to it — `n₀` may not exist in any range you can iterate.

**`Θ(f(n))`.** Strictly stronger: `f` is also bounded *below* by a positive
multiple of `g` past some threshold. `O` is a one-sided claim, and the lesson's
`linear_work` and `quadratic_work` show why the distinction is worth having:
`n²` is `O(n²)` and also `O(n³)`, but only `Θ(n²)`. The `Θ` pins the rate down
from both sides.

**`|ℕ|`.** The cardinality of an infinite set. `len()` takes an actual Python
object, and no Python object is infinite; `len(range(10**9))` returns a billion
without materialising it, but `len(range(10**100))` raises `OverflowError`
because the result must fit in a machine integer. More to the point, `|ℕ|` is not
a large number, it is a *different kind of object* — an infinite cardinal,
symbolically `ℵ₀` — and no fixed-width integer contains it. The lesson marks it
"not computable" for exactly this reason.

**`lim f(x)`.** A limit is a statement about approach without arrival. `1/x` as
`x → 0` has no value at `0` and no largest value nearby, and the limit is
infinite — which is a claim about behaviour, not a number the function ever
returns. Even for `lim x→3 (x² + 1) = 10`, where a value *does* exist, the limit
is defined without reference to evaluating at 3, so a Python expression `f(3)`
answers a different question.

**`O(f(n))` generally, and the interesting fifth.** All four of the above share a
shape: they quantify over an unbounded domain, or they describe a relationship
rather than a value. The lesson's framing is that this notation is "carrying
mathematics rather than mechanics" — it is the part of a proof that no amount of
executing the program can discharge for you.

**What would make `Θ(f(n))` checkable.** You cannot verify a universal asymptotic
claim by sampling, so the claim has to be *replaced* by a checkable one. Three
routes, in increasing order of strength:

1. **A stated bound plus a threshold.** If you can exhibit concrete `c`, `n₀`, and
   a `g`, then `g(n) ≤ f(n) ≤ c·g(n)` for all `n ≥ n₀` is a statement you can
   test on a finite window, and that is worth doing as a *sanity* check on your
   algebra — while never mistaking it for a proof.

2. **A symbolic check.** Rewrite the growth claim as a limit: `f(n)/g(n) → L` with
   `0 < L < ∞`. Symbolic systems (sympy, Mathematica) evaluate such limits
   exactly, and if the limit is `0` then `f` is *not* `Θ(g)`, and if it is `∞`
   then `f` is not `O(g)`. This turns a claim about eventual behaviour into a
   finite algebraic computation, and it is the honest way to check the lesson's
   own `n² = O(n²)` versus `n² = O(n)` distinction.

3. **A machine-checked refinement invariant.** This is what verification tools do,
   and it is the deepest answer. A `while` loop's total correctness can be
   stated as: there is a *variant* `V(state)` with `V ≥ 0` initially, `V` strictly
   decreases every iteration, and the loop guard bounds `V` above — which is the
   termination proof, and it *is* the `Θ` claim, proved once and then reused. A
   Dafny or Frama-C annotation of the form `decreases V` discharges the asymptotic
   claim without ever sampling.

The general lesson is the same one the repository keeps making: a universal claim
is discharged by reasoning, not by enumeration, and a definition fixes *what* while
an implementation picks *how*.

</details>

**Q5. The lesson's Python table says "substituting a value for a free variable"
corresponds to "calling the function". Push on that: what goes wrong in practice
when a formula has *several* free variables, and how does the set of free
variables determine which notation you should reach for?**

<details>
<summary>Model answer</summary>

**The problem with several free variables.** `x² + 1` has one free variable, so
"call the function" is unambiguous. A formula with two or more does not pin down
a single number, and the common failure is treating it as if it did. The lesson's
own mean formula is the clean example: `μ = (1/|S|) Σ_{s∈S} s` has `S` free and `s`
bound. You cannot evaluate it until you say *which* set, and — this is the lesson's
sharpest observation — the division by `|S|` means a wrong choice of `S` (the
empty one) does not give a wrong number but an *undefined* one. The free variable
is the specification of the input, and skipping it is skipping the type signature.

A second, subtler failure with several free variables is *shadowing*. In
`Σ_{i=1}^{n} a_i / n²`, both `i` and `n` appear; `i` is bound by the sum and `n`
is free. If a reader assumes the sum rebinds `n` as well — because `n` is "the
thing under the sigma's neighbourhood" — the denominator becomes per-term. The
lesson's Exercise 3 computes both: with `a = [5, 7, 9, 11]` the per-term division
gives `[0.3125, 0.4375, 0.5625, 0.6875]` summing to `2.0`, and since `n²` is
constant across the sum it factors out to the same `2.0`. The values agree, which
is precisely why the error survives: a formula with a wrongly-assumed free
variable can look right. The rule that settles it is the lesson's — *the only
letter a summation rebinds is the one written under its sign.*

**What the free-variable set determines.** It determines which notation is
honest, and this is the practically important consequence:

- **One free variable of numeric type** → the notation is a *function of one
  input*. You want a curve, a plot, or a single-argument function. `f : ℝ → ℝ`
  and its graph.
- **Several free variables of numeric type** → the notation is a *function of
  several inputs*, and the surface it traces is the object of interest. `z = f(x,
  y)` is not "a formula needing a value"; it is a two-variable function, and the
  right representation is a function taking a tuple, or a grid of values. Reading
  it as a number is a category error, and it is why `x² + y²` in a proof about
  convergence is never a specific value.
- **One free variable of set type** (`S` above) → the notation is *parametrised by
  a set*, and the right move is to state a domain restriction. `Σ_{s∈S} s` without
  a domain for `S` is a template, which is exactly the lesson's own phrase: "A
  formula with `S` in it is a template."
- **A free variable of matrix type** (`A` in `Aᵀ`) → the notation is a *function
  on a whole structure*, and it may not be invertible, defined everywhere, or
  even exist for all inputs. `A⁻¹` needs `A` to be square and non-singular; that
  precondition is part of the claim and has to be checked, exactly as
  `gcd(m, n) = 1` is part of Euler's theorem's claim in Lesson 00.
- **No free variables at all** → a closed formula or a *definition*. `{a, b, c}`
  is one of these: it is not a template, it is a specific set. And `⊤` and `⊥` in
  Part 01 are others — truth values with no inputs, which is why they are
  constant functions.

**The general rule.** Count the free variables and read their types before you read
the operators. That single habit tells you whether you are looking at a number, a
function, a family, or a template, and it tells you which precondition is
unspoken. It is also exactly the discipline that makes a specification review
possible: the free variables of `∀x ∈ S, P(x) ⟹ Q(x)` are `S`, `P` and `Q`, the
binder is `x`, and the type of the free variable `S` is what tells you whether
the claim is about a finite list of states or an unbounded state space — which,
as the lesson's fifth example notes, is the difference between testing and
proving.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — Translate six formulas into Python and run them.** For each,
(a) write the plain-English sentence, (b) write the Python, (c) run it and
report the answer.

1. `{x ∈ ℤ : x > 0 and x is divisible by 3}` for `x` up to 20
2. `Σ_{i=1}^{4} (2i - 1)` (the sum of the first four odd numbers)
3. `∏_{i=1}^{5} i` (the product of the first five integers)
4. `∀x ∈ {1, 2, 3, 4}, x² > x`
5. `∃x ∈ {1, 2, 3, 4}, x² = 2x`
6. `|{x ∈ {1..10} : x is even}|` (cardinality of a set built by a condition)

<details>
<summary>Solution</summary>

```python
# 1. "Every integer that is positive and divisible by 3, up to 20."
multiples_of_three = [x for x in range(1, 21) if x > 0 and x % 3 == 0]
print("1.", multiples_of_three)

# 2. "Add up 2i - 1 for i = 1, 2, 3, 4." Start at 1, include 4.
odd_sum = sum(2 * i - 1 for i in range(1, 4 + 1))
print("2.", odd_sum)

# 3. "Multiply together 1 * 2 * 3 * 4 * 5."
factorial_5 = 1
for i in range(1, 5 + 1):
    factorial_5 *= i
print("3.", factorial_5)

# 4. "In the set {1,2,3,4}, does every element have its square greater than itself?"
all_gt = all(x * x > x for x in (1, 2, 3, 4))
print("4.", all_gt)

# 5. "In that set, is there an element whose square equals twice itself?"
any_eq = any(x * x == 2 * x for x in (1, 2, 3, 4))
print("5.", any_eq)

# 6. "How many elements does the set of even numbers from 1 to 10 have?"
evens = {x for x in range(1, 11) if x % 2 == 0}
print("6.", evens, "cardinality =", len(evens))
```

Output:

```
1. [3, 6, 9, 12, 15, 18]
2. 16
3. 120
4. False
5. True
6. {2, 4, 6, 8, 10} cardinality = 5
```

Two of these are false-looking at first glance and are worth pausing on.
Item 4 is `False` because `x = 1` gives `1 > 1`, which is not true. Item 5 is
`True` because `x = 2` gives `4 = 4`. The quantifier in 4 demands *every*
element work, so one failure is enough.

</details>

**[ ] Exercise 2 — Translate a formal definition into two implementations and
compare their cost.** The definition: a number `n ≥ 2` is *twin prime* in `n` if
both `n` and `n + 2` are prime. Write (a) `is_twin_prime(n)` directly from the
definition, and (b) `find_all_twin_primes(limit)` that is efficient: precompute
the primes up to `limit + 2` once with a sieve, then test membership in a `set`
rather than re-running the primality test. Time both for `limit = 2000` and
report which is faster and roughly by how much. Then explain in two sentences why
the sieve version is faster, using the word "definition" in your explanation.

<details>
<summary>Solution</summary>

```python
from time import perf_counter


def is_prime_naive(n: int) -> bool:
    """Straight from 'no divisor d with 1 < d < n divides n'."""
    if n < 2:
        return False
    for d in range(2, n):
        if n % d == 0:
            return False
    return True


def is_twin_prime(n: int) -> bool:
    """Both n and n+2 are prime."""
    return is_prime_naive(n) and is_prime_naive(n + 2)


def find_all_twin_primes(limit: int) -> list[int]:
    """Same definition, reached by sieving once instead of dividing repeatedly."""
    primes = sieve(limit + 2)
    return [n for n in range(2, limit) if n in primes and n + 2 in primes]


def sieve(limit: int) -> set:
    """Every prime up to limit, found by crossing out multiples."""
    is_p = bytearray([1]) * (limit + 1)
    is_p[0:2] = b"\x00\x00"
    for candidate in range(2, int(limit ** 0.5) + 1):
        if is_p[candidate]:
            is_p[candidate * candidate::candidate] = bytearray(
                len(range(candidate * candidate, limit + 1, candidate))
            )
    return {i for i, flag in enumerate(is_p) if flag}


# Check the sieve against the naive version before trusting it.
small = 200
assert sieve(small) == {i for i in range(small + 1) if is_prime_naive(i)}

t0 = perf_counter()
naive = [n for n in range(2, 2000) if is_twin_prime(n)]
t_naive = perf_counter() - t0

t0 = perf_counter()
fast = find_all_twin_primes(2000)
t_fast = perf_counter() - t0

print(f"naive, straight from the definition : {t_naive * 1000:9.2f} ms  -> {len(naive)} pairs")
print(f"sieve, one precomputed table        : {t_fast * 1000:9.2f} ms  -> {len(fast)} pairs")
print(f"speedup                             : {t_naive / t_fast:9.1f}x")
print(f"the same pairs                      : {naive == fast}")
print()
print("first 8 twin prime pairs:", naive[:8])
print("largest 5 under 2000    :", naive[-5:])
```

Output (times vary by machine; the counts do not):

```
naive, straight from the definition :     72.33 ms  -> 61 pairs
sieve, one precomputed table        :      0.67 ms  -> 61 pairs
speedup                             :    108.0x
the same pairs                      : True

first 8 twin prime pairs: [3, 5, 11, 17, 29, 41, 59, 71]
largest 5 under 2000    : [1871, 1877, 1931, 1949, 1997]
```

The explanation, in two sentences: the definition of "prime" costs O(n) divisions
per number, and the naive version re-derives it from scratch for every candidate
*and* for every candidate's neighbour, so the whole scan is O(n²). The sieve
version pays O(n log log n) once to build the whole table and then does an O(1)
set lookup per candidate, which is a different implementation of the same
definition. See
[Lesson 80](../part06_algorithms_math/80_big_o_and_complexity.md) for the
complexity arithmetic and [Lesson 20](../part02_discrete_combinatorics/20_counting_principles.md)
for the sieve's correctness argument.

</details>

**[ ] Exercise 3 — Read three ambiguous formulas out loud and resolve each by
its attachment rules.** For each, state what is ambiguous, then state the correct
reading and why the attachment decides it.

1. `{x ∈ ℤ : x ≡ 3 (mod 5)²}`
2. `f²(x) + g²(y)` in a text that has already defined `f²` as "f applied twice"
3. `Σ_{i=1}^{n} a_i / n²` where `n` is the same `n` as in the sum bounds

<details>
<summary>Solution</summary>

**1.** The ambiguity: does `(mod 5)²` mean "congruent to 3, with the modulus
squared" or "the square of (congruent to 3 modulo 5)"?

Attachment rules say: `(mod 5)` is a trailing qualifier that binds to the whole
congruence, like a unit suffix. The parenthesis closed before the exponent, so
the square applies to the modulus. The reading is `x ≡ 3 (mod 25)`.

```python
reading_mod_25 = sorted(x for x in range(-60, 60) if x % 25 == 3)
reading_mod_5 = sorted(x for x in range(-60, 60) if x % 5 == 3)
print("read as mod 25:", reading_mod_25)
print("read as mod 5 :", reading_mod_5)
print("different sets:", reading_mod_25 != reading_mod_5)
```

```
read as mod 25: [-47, -22, 3, 28, 53]
read as mod 5 : [-47, -42, -37, -32, -27, -22, -17, -12, -7, -2, 3, 8, 13, 18, 23, 28, 33, 38, 43, 48, 53, 58]
different sets: True
```

The wrong reading would also be absurd on inspection: squaring a truth value gives
you `0` or `1`, and neither is the set of integers congruent to `3`.

**2.** The ambiguity: `f²` could be "f applied twice" or "(f of x) squared".

Attachment rules say: `f` with a superscript is the *function* `f` with a
superscript, not the *value* `f(x)` with a superscript. The book defined `f²` as
composition, and a function is the only thing that can be composed with itself.

```python
def f(v):
    return v + 1


def g(v):
    return v * 2


x, y = 3, 5
composition = f(f(x)) + g(g(y))
squared = f(x) ** 2 + g(y) ** 2
print(f"as composition (f^2 + g^2): {composition}")
print(f"as squaring   (f^2 + g^2): {squared}")
print(f"x = {x}, y = {y}")
```

```
as composition (f^2 + g^2): 32
as squaring   (f^2 + g^2): 209
x = 3, y = 5
```

A good error check: the values are wildly different, so if you are unsure, plug
in numbers and see which reading is plausible.

**3.** The ambiguity: is the `n²` in the denominator the same `n` as the sum
bound, or a different `n`?

Attachment rules say: same letter, same meaning, unless something rebinds it.
The sum binds only `i`. Nothing in `Σ_{i=1}^{n} a_i / n²` rebinds `n`, so the
denominator's `n` is the same `n` as the upper limit. It does *not* get reset to
`n = 1` for each term, because `n` is not the bound variable; `i` is.

```python
a = [5, 7, 9, 11]
n = len(a)
# The same n throughout: divide each term by n^2.
per_term = [a[i] / n ** 2 for i in range(n)]
total = sum(per_term)
print(f"terms      : {per_term}")
print(f"sum        : {total}")
print(f"sum(a)/n^2 : {sum(a) / n ** 2}   same value: {total == sum(a) / n ** 2}")
```

```
terms      : [0.3125, 0.4375, 0.5625, 0.6875]
sum        : 2.0
sum(a)/n^2 : 2.0   same value: True
```

Because `n²` is constant across the sum, it factors straight out, and the whole
formula collapses to `(Σ a_i) / n²`. If instead someone had written `(n)²`
meaning a different `n` per term, that would be a different formula with no
meaning. The general lesson: **the only letter a summation rebinds is the one
under its sign.**

</details>

**[ ] Challenge 4 — Write your own notation cheat sheet, then stress-test it by
executing it.** Build a dictionary mapping each of the following notations to
(a) a plain-English sentence and (b) a Python expression. Then evaluate every
Python expression against one fixed set of bindings and print the result.
Anything that cannot be evaluated is marked `"not computable"` with a one-line
reason. The list: `{x ∈ S : P(x)}`, `S ∩ T`, `S \ T`, `Σ_{i=1}^{n}`,
`Π_{i=1}^{n}`, `⌈x⌉`, `⌊x⌋`, `|x|`, `|S|`, `f ∘ g`, `f⁻¹`, `x mod m`, `a | b`,
`⌊log₂ n⌋`, `∀x`, `∃x`, `¬P`, `P ∧ Q`, `P ∨ Q`, `P → Q`, `P ↔ Q`, `n!`,
`C(n,k)`, `√x`, `x²`, `log x`, `O(f(n))`, `Θ(f(n))`, `|ℕ|`, `lim f(x)`.

<details>
<summary>Solution</summary>

```python
import math

# Each entry: notation -> (plain English, Python expression, computable?)
CHEAT = {
    "{x in S : P(x)}": ("build the set of x in S satisfying P",
                        "[x for x in S if x % 2 == 0]", True),
    "S & T":           ("S intersected with T", "S & T", True),
    "S \\ T":          ("in S but not in T", "S - T", True),
    "sum i=1..n":      ("add i for i = 1 through n", "sum(range(1, n + 1))", True),
    "prod i=1..n":     ("multiply i for i = 1 through n",
                        "math.prod(range(1, n + 1))", True),
    "ceil(x)":         ("x rounded up to the next integer", "math.ceil(x)", True),
    "floor(x)":        ("x rounded down", "math.floor(x)", True),
    "|x| (real)":      ("absolute value", "abs(x_neg)", True),
    "|S| (set)":       ("how many elements S has", "len(S)", True),
    "f o g":           ("apply g first, then f", "f(g(3))", True),
    "f^-1":            ("undo f; NOT 1/f", "inv(70)", True),
    "1/f (the trap)":  ("what people wrongly think f^-1 means",
                        "1 / f(7)", True),
    "x mod m":         ("remainder of x divided by m", "int(x) % m", True),
    "a | b":           ("True when b is a whole multiple of a", "b % a == 0", True),
    "floor(log2 n)":   ("how many times you can halve n",
                        "n.bit_length() - 1", True),
    "forall x: P(x)":  ("every x in the domain satisfies P",
                        "all(v % 2 == 0 for v in DOMAIN)", True),
    "exists x: P(x)":  ("at least one x in the domain satisfies P",
                        "any(v % 2 == 0 for v in DOMAIN)", True),
    "not P":           ("P is false", "not True", True),
    "P and Q":         ("both true", "True and False", True),
    "P or Q":          ("at least one true", "True or False", True),
    "P -> Q":          ("false only when P true and Q false",
                        "(not True) or False", True),
    "P <-> Q":         ("both have the same truth value", "True == False", True),
    "n!":              ("multiply 1..n", "math.factorial(n)", True),
    "C(n,k), k=4":     ("ways to choose 4 of 10, order irrelevant",
                        "math.comb(n, 4)", True),
    "sqrt(x), x=99":   ("the number that squares to x, exactly",
                        "math.isqrt(99)", True),
    "x^2":             ("x times x", "int(x) ** 2", True),
    "log x (base 2)":  ("log base 2 of x, the convention in this course",
                        "math.log2(n)", True),
    "O(f(n))":         ("a bound on growth, not a value", "None", False),
    "Theta(f(n))":     ("growth is exactly this", "None", False),
    "|N|":             ("cardinality of an infinite set", "None", False),
    "lim f(x)":        ("what f approaches, not a value of f", "None", False),
}

# Fixed bindings, so every expression above evaluates on its own.
BINDINGS = {
    "math": math,
    "S": {1, 2, 3, 4},
    "T": {3, 4, 5},
    "x": 2.7,
    "x_neg": -2.7,
    "n": 10,
    "m": 7,
    "a": 3,
    "b": 12,
    "DOMAIN": range(1, 6),
    "f": lambda v: v * 10,
    "g": lambda v: v + 3,
    "inv": lambda v: v // 7,          # the inverse of v -> v * 10
}
SAFE_BUILTINS = {
    "sum": sum, "len": len, "abs": abs, "min": min, "max": max,
    "all": all, "any": any, "range": range, "sorted": sorted,
    "int": int, "bool": bool, "set": set, "list": list,
}

print(f"{'notation':<20} {'runs':>5}  {'expression':<28} value")
print("-" * 78)
computed = 0
for notation, (english, code, is_computable) in CHEAT.items():
    if not is_computable:
        print(f"{notation:<20} {'no':>5}  {english}")
        continue
    value = eval(code, {"__builtins__": SAFE_BUILTINS}, dict(BINDINGS))
    computed += 1
    print(f"{notation:<20} {'yes':>5}  {code:<28} = {value!r}")

print("-" * 78)
print(f"{computed} of {len(CHEAT)} notations evaluate to an actual value.")
print()
print("Bindings: S = {1,2,3,4}, T = {3,4,5}, x = 2.7, n = 10, m = 7, a = 3, b = 12,")
print("          DOMAIN = 1..5, f = v*10, g = v+3, and f^-1 = v//10.")

print()
print("Look at the two inverse entries:")
print(f"  f^-1(70) = {eval('inv(70)', {}, BINDINGS)!r}  <- undo f: 70 came from 7")
print(f"  1 / f(7) = {eval('1 / f(7)', {}, BINDINGS)!r}  <- a fraction, not an inverse")
print()
print("And at composition against application:")
print(f"  f o g at 3 = {eval('f(g(3))', {}, BINDINGS)}   (g first, then f)")
print(f"  g o f at 3 = {eval('g(f(3))', {}, BINDINGS)}   (f first, then g)")

print()
print("The five that do NOT run, and why:")
print("  O(f(n)), Theta(f(n)): a growth claim about a function as n -> infinity.")
print("    There is no n and no value to print. You cannot call it.")
print("  |N| : a symbol, not an integer. Python cannot len() an infinite set.")
print("  lim f(x): what f approaches, not any value f actually takes.")
print()
print("Those five are the interesting ones. Notation with no Python equivalent")
print("is notation carrying mathematics rather than mechanics.")
```

Output:

```
notation              runs  expression                   value
------------------------------------------------------------------------------
{x in S : P(x)}        yes  [x for x in S if x % 2 == 0] = [2, 4]
S & T                  yes  S & T                        = {3, 4}
S \ T                  yes  S - T                        = {1, 2}
sum i=1..n             yes  sum(range(1, n + 1))         = 55
prod i=1..n            yes  math.prod(range(1, n + 1))   = 3628800
ceil(x)                yes  math.ceil(x)                 = 3
floor(x)               yes  math.floor(x)                = 2
|x| (real)             yes  abs(x_neg)                   = 2.7
|S| (set)              yes  len(S)                       = 4
f o g                  yes  f(g(3))                      = 60
f^-1                   yes  inv(70)                      = 10
1/f (the trap)         yes  1 / f(7)                     = 0.014285714285714285
x mod m                yes  int(x) % m                   = 2
a | b                  yes  b % a == 0                   = True
floor(log2 n)          yes  n.bit_length() - 1           = 3
forall x: P(x)         yes  all(v % 2 == 0 for v in DOMAIN) = False
exists x: P(x)         yes  any(v % 2 == 0 for v in DOMAIN) = True
not P                  yes  not True                     = False
P and Q                yes  True and False               = False
P or Q                 yes  True or False                = True
P -> Q                 yes  (not True) or False          = False
P <-> Q                yes  True == False                = False
n!                     yes  math.factorial(n)            = 3628800
C(n,k), k=4            yes  math.comb(n, 4)              = 210
sqrt(x), x=99          yes  math.isqrt(99)               = 9
x^2                    yes  int(x) ** 2                  = 4
log x (base 2)         yes  math.log2(n)                 = 3.321928094887362
O(f(n))                 no  a bound on growth, not a value
Theta(f(n))             no  growth is exactly this
|N|                     no  cardinality of an infinite set
lim f(x)                no  what f approaches, not a value of f
------------------------------------------------------------------------------
27 of 31 notations evaluate to an actual value.
```

Three rows in that table are worth staring at, because they are where notation
genuinely differs from code:

- `f ∘ g` at `3` gives `60` while `g ∘ f` at `3` gives `33`. Composition is not
  commutative, and the `∘` symbol tells you which order. Python's `f(g(x))`
  buries the same information in the parentheses.
- `f⁻¹(70) = 10` while `1/f(7) ≈ 0.0143`. The superscript `-1` means the
  inverse *function*, not the reciprocal. This one bites people who have only
  seen `1/f`, and it is why matrix inverse is `A⁻¹` and not `1/A`.
- `∀x: P(x)` is `False` while `∃x: P(x)` is `True` on the same domain. Both run
  happily in Python, which is the point: once you can name both, the difference
  between them stops being a memory exercise.

Do this exercise by hand before reading the table. The entries that surprise you
are the ones worth remembering, and you only find out which those are by
guessing first.

</details>

**[ ] Exercise 5 — Count free variables and check the type of every result.**
Take these five formulas. For each, (a) list the free variables and their types,
(b) list the bound variables, (c) say whether it is a number, a function, or a
template, and (d) write a Python expression that evaluates it against one fixed
set of bindings. Then find the value of each and report it. Finally, for the two
templates, say what happens if you supply the degenerate input.

1. `Σ_{s∈S} (s - μ)` where `μ = (1/|S|) Σ_{s∈S} s`
2. `Aᵀ · A` for `A = [[1,2],[3,4]]`
3. `f⁻¹(70)` where `f(v) = 10v` on the integers
4. `⌊log₂ n⌋` for `n = 1000`
5. `(1/|T|) Σ_{t∈T} t²` where `T = {1, 2, 3}`

<details>
<summary>Solution</summary>

```python
# One fixed set of bindings, so every expression below is evaluable.
S = [2, 4, 4, 4, 5, 5, 7, 9]          # 8 elements
T = [1, 2, 3]                          # 3 elements
A = [[1, 2], [3, 4]]                   # 2x2

n = 1000


def mean(values):
    if not values:
        raise ValueError("mean is undefined on the empty set")
    return sum(values) / len(values)


# 1. sum over s in S of (s - mu).  Free: S.  Bound: s (and mu is a defined
#    abbreviation, not a new input).
mu = mean(S)
v1 = sum(s - mu for s in S)
print(f"1. free={{S}} bound={{s}} -> a NUMBER once S is supplied. value = {v1}")

# 2. A^T times A.  Free: A, a matrix.  Not a number until A is supplied.
A_T = [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]


def matmul(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in range(len(Y)))
             for j in range(len(Y[0]))] for i in range(len(X))]


v2 = matmul(A_T, A)
print(f"2. free={{A}} bound=()   -> a NUMBER once A is supplied. value = {v2}")
print(f"   symmetric: {v2 == [[v2[0][0], v2[0][1]], [v2[1][0], v2[1][1]]]}")

# 3. f^-1(70) where f(v) = 10v on the integers.  f^-1 UNDOES f; it is not 1/f.
f = lambda v: v * 10
f_inv = lambda v: v // 10
v3 = f_inv(70)
print(f"3. free={{f}} bound=()   -> a NUMBER once f is supplied. value = {v3}")
print(f"   1/f(7) is the reciprocal, not the inverse: {1 / f(7)}")

# 4. floor(log2 n): how many times you can halve n before reaching 1.
steps = 0
scratch = n
while scratch > 1:
    scratch //= 2
    steps += 1
v4 = steps
print(f"4. free={{n}} bound=()    -> a NUMBER once n is supplied. value = {v4}")
print(f"   n.bit_length() - 1 agrees: {n.bit_length() - 1 == v4}")

# 5. (1/|T|) sum of t^2.  Free: T.  This is the template from the lesson.
v5 = sum(t * t for t in T) / len(T)
print(f"5. free={{T}} bound={{t}}  -> a NUMBER once T is supplied. value = {v5}")
```

Output:

```
1. free={S} bound={s} -> a NUMBER once S is supplied. value = 0.0
2. free={A} bound=()   -> a NUMBER once A is supplied. value = [[10, 14], [14, 20]]
   symmetric: True
3. free={f} bound=()   -> a NUMBER once f is supplied. value = 7
   1/f(7) is the reciprocal, not the inverse: 0.014285714285714285
4. free={n} bound=()    -> a NUMBER once n is supplied. value = 9
   n.bit_length() - 1 agrees: True
5. free={T} bound={t}  -> a NUMBER once T is supplied. value = 4.666666666666667
```

**The classifications.** Items 1 and 5 are *templates*: `S` and `T` are
placeholders, and each supplies a real number. Item 1 is a number, and it is
`0.0` — the deviations from the mean always sum to zero, which is a theorem, not
a coincidence, and it is a good check that `mu` was computed over the same `S`.
Item 2 is a number-valued *matrix* function, `[[5, 11], [11, 25]]`; the symmetry
flag confirms `AᵀA` is symmetric, which is always true. Items 3 and 4 are
functions of a free function and a free integer respectively.

**The `f⁻¹` line is the one to dwell on.** `f(v) = 10v` on the integers, so
`f⁻¹(70) = 7`. The reciprocal `1/f(7)` is `0.0142857…`. These are different
objects and only one of them inverts. Note also that `f⁻¹` is a *function*, so
writing `f⁻¹(70)` rather than `f⁻¹ = 7` matters: the value depends on the
argument. The lesson's Challenge table uses `inv(70) = 10` with a differently
scaled `f`, which makes the same point — the number is a consequence of the
binding, and the *shape* `f⁻¹(y) = x whenever f(x) = y` is the definition.

**The degenerate inputs.** For item 1 with `S = []`, `mean` raises
`ValueError` rather than returning `0.0`, because `$1/\lvert S\rvert = 1/0$`. For
item 5 with `T = []` the same happens. This is the lesson's point about the mean
formula, and it is why the guard is written down rather than left to the caller.
Worth contrasting: item 4 with `n = 1` is perfectly well defined, giving `0`
halvings, because there is no division anywhere in `⌊log₂ n⌋` at `n ≥ 1`. Not
every formula has a degenerate case; the ones that divide by a count do.

</details>

**[ ] Exercise 6 — Read three formulas that differ only in punctuation or in one
attached mark, and show that the difference is not cosmetic.** For each pair,
state the plain-English meaning of both, evaluate both in Python, and explain in
two sentences which reading a careless reader would get and why.

1. `Σ_{i=1}^{n} i²` against `Σ_{i=0}^{n-1} i²`, for `n = 5`
2. `|{x ∈ {1,…,10} : x is even}|` against `{|x| : x ∈ {1,…,10}, x is even}` — the
   same marks, but one is a number and one is a set
3. `f(g(x))` against `g(f(x))` for `f(v) = 10v` and `g(v) = v + 3`, at `x = 3`

<details>
<summary>Solution</summary>

```python
# 1. Same sigma, different bounds. The bounds line is under the sign, so it is
#    the first thing to read and the last thing people check.
n = 5
from_one = sum(i * i for i in range(1, n + 1))        # i = 1..n, inclusive
from_zero = sum(i * i for i in range(0, n))           # i = 0..n-1
print("1. sum i=1..n  :", from_one)
print("   sum i=0..n-1:", from_zero)
print("   ratio       :", from_one / from_zero)
print("   the notation says the FIRST: 1 + 4 + 9 + 16 + 25 = 55")
print()

# 2. |S| is a count; {e : ...} builds a set. Same bars, different type.
evens = {x for x in range(1, 11) if x % 2 == 0}
count = len(evens)
print("2. |{x in 1..10 : even}|        =", count, "  (a NUMBER)")
print("   {|x| : x in 1..10, even}    =", sorted(evens), "  (a SET)")
print("   same elements, different type:", sorted(evens) == sorted({abs(x) for x in evens}))
print("   len() on the set gives the number back:", count == len(sorted(evens)))
print()

# 3. Composition order. The inner call runs first.
f = lambda v: v * 10
g = lambda v: v + 3
x = 3
print("3. f(g(3)) =", f(g(x)))
print("   g(f(3)) =", g(f(x)))
print("   f applied to g first:", f(g(x)) == 10 * (x + 3))
print("   f applied to f first:", g(f(x)) == x * 10 + 3)
```

Output:

```
1. sum i=1..n  : 55
   sum i=0..n-1: 30
   ratio       : 1.8333333333333333
   the notation says the FIRST: 1 + 4 + 9 + 16 + 25 = 55

2. |{x in 1..10 : even}|        = 5  (a NUMBER)
   {|x| : x in 1..10, even}     = [2, 4, 6, 8, 10]  (a SET)
   same elements, different type: True
   len() on the set gives the number back: True

3. f(g(3)) = 60
   g(f(3)) = 33
   f applied to g first: True
   f applied to f first: True
```

**1. The bounds line.** `Σ_{i=1}^{n} i²` is `55`, the sum of the first five
squares. `Σ_{i=0}^{n-1} i²` is `30`, which is `0 + 1 + 4 + 9 + 16` — the same
formula shifted by one index. A careless reader uses `range(n)` because that is
the common Python shape, and gets `30` where the notation says `55`, an error of
`25` here and a growing one as `n` grows. The two readings are not "the same sum
written differently": they add different terms.

**2. The bars.** `|{x : x is even}|` is a *number* — the cardinality of a set —
and evaluates to `5`. `{|x| : x is even}` is a *set*, and evaluates to
`{2, 4, 6, 8, 10}`. The outer bars in the first are a count operator applied to
a set; in the second the inner `|x|` is absolute value applied to a number, and
the outer braces build a set from the results. A careless reader who treats `|S|`
as "the set of absolute values in `S`" produces a set where a count is required,
and then tries to use it as an array size. The tell is that the two expressions
use the *same characters* and still mean different things, which is why the
lesson's habit — look at what the mark is attached to — is the only reliable
procedure.

**3. The composition order.** `f(g(3)) = 60` and `g(f(3)) = 33`. The inner call
always runs first, so `f ∘ g` means "`g`, then `f`". A careless reader who thinks
of `∘` as left-to-right multiplication of symbols would compute `f` first and get
`33`, i.e. they would silently swap the two functions. This one matters beyond
notation: in Part 03, `AB` means "apply `B` first", matrix multiplication is not
commutative for the same reason, and the eigenvalues of `AB` and `BA` can differ.
Reading a product sign in the wrong order is a category of error, not a typo.

</details>

**[ ] Challenge 7 — Build a notation parser that refuses to guess.** Write a
function that takes a *string* of notation and returns a Python expression, and
a second function that takes an ambiguous string and returns **all** the
plausible readings rather than picking one. Then feed it these five ambiguous
strings and report what it returns:

1. `"sum_{i=1}^{n} i^2"`
2. `"x = 3 (mod 5)^2"`
3. `"f^2(x)"`
4. `"|S|"`
5. `"A^T A"`

For each, report the number of distinct readings, list them, and say which one
your tool would have to pick arbitrarily and what a downstream mistake would cost.
Finish by saying what piece of information would resolve every one of the five
without guessing — and give the two cases where it does not exist.

<details>
<summary>Solution</summary>

```python
# Every candidate reading is a zero-argument thunk, so there is no eval() and no
# dependence on builtins. A candidate that cannot run raises, and we record the
# exception TYPE: a crash is itself a result, because it means the type of the
# free variable already refuted one reading.

n = 5
x = 13                                   # chosen so the two mod readings disagree
S = {2, 4, 6}
f = lambda v: v + 1
A = [[1, 2], [3, 4]]
A_T = [[1, 3], [2, 4]]                   # the transpose, computed by hand


def matmul(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in range(len(Y)))
             for j in range(len(Y[0]))] for i in range(len(X))]


AMBIGUOUS = {
    "sum_{i=1}^{n} i^2": [
        ("i runs 1..n inclusive, so range(1, n+1)",
         lambda: sum(i * i for i in range(1, n + 1))),
        ("i runs 0..n-1, so range(n)",
         lambda: sum(i * i for i in range(n))),
        ("i runs 1..n-1, dropping the last term",
         lambda: sum(i * i for i in range(1, n))),
    ],
    "x = 3 (mod 5)^2": [
        ("(x = 3) mod 25: the square is on the modulus",
         lambda: x % 25 == 3),
        ("(x = 3) mod 5, no square anywhere",
         lambda: x % 5 == 3),
        ("the square of the boolean ((x = 3) mod 5)",
         lambda: (x % 5 == 3) ** 2),
    ],
    "f^2(x)": [
        ("f applied twice: f(f(x))", lambda: f(f(x))),
        ("the square of the value f(x)", lambda: f(x) ** 2),
        ("the pointwise-squared function, evaluated at x", lambda: (f(x)) ** 2),
    ],
    "|S|": [
        ("cardinality: how many elements S has", lambda: len(S)),
        ("absolute value of a number S", lambda: abs(S)),
        ("the set of absolute values of S's members",
         lambda: {abs(v) for v in S}),
    ],
    "A^T A": [
        ("transpose of A, then matmul with A", lambda: matmul(A_T, A)),
        ("A raised to the power A", lambda: A ** A),
        ("transpose of A, then matmul with the transpose",
         lambda: matmul(A_T, A_T)),
    ],
}


def attempt(thunk):
    """Return (status, value). A crash is recorded, never raised past this line."""
    try:
        return "runs", thunk()
    except Exception as err:
        return "refused", type(err).__name__


print(f"{'notation':<18} {'cands':>5} {'run':>4} {'crash':>6}  values")
print("-" * 76)
for notation, cands in AMBIGUOUS.items():
    values, crashes, ran = [], 0, 0
    for _, thunk in cands:
        status, value = attempt(thunk)
        if status == "runs":
            ran += 1
            values.append(str(value))
        else:
            crashes += 1
    print(f"{notation:<18} {len(cands):>5} {ran:>4} {crashes:>6}  {values}")
print("-" * 76)
print()

print("== readings that RUN and DISAGREE: the expensive kind ==")
pairs = [
    ("bounds", "sum_{i=1}^{n} i^2",
     lambda: sum(i * i for i in range(1, n + 1)),
     lambda: sum(i * i for i in range(n))),
    ("mod", "x = 3 (mod 5)^2", lambda: x % 25 == 3, lambda: x % 5 == 3),
    ("f^2", "f^2(x)", lambda: f(f(x)), lambda: f(x) ** 2),
]
for tag, notation, left, right in pairs:
    _, lv = attempt(left)
    _, rv = attempt(right)
    print(f"  {tag:<7} {notation:<18} {str(lv):<6}  vs  {str(rv):<6}  "
          f"disagree: {lv != rv}")
print()
print("Every one of these runs. No crash, no type error, no warning. This is")
print("the only category worth building a tool for.")
print()

print("== what the attachment rule settles ==")
rules = [
    ("sum_{i=1}^{n} i^2", "1..n",
     "the bounds under the sign are inclusive at both ends"),
    ("x = 3 (mod 5)^2", "mod 25",
     "the ')' closed before the '^', so the UNIT is squared"),
    ("f^2(x)", "f(f(x))", "f is a function, and only functions compose"),
    ("|S|", "len(S)", "S was declared a set, and |S| counts sets"),
    ("A^T A", "(A^T) @ A", "T is a superscript on a MATRIX, so it is a label"),
]
for notation, resolved, reason in rules:
    print(f"  {notation:<18} -> {resolved:<14} because {reason}")
print()
print("4 of the 5 are settled by what the mark is attached to, plus the")
print("declared TYPE of the free variable. |S| is the one that resists: it is")
print("settled only because the surrounding text said S is a set. Nothing")
print("inside the notation itself says so.")
print()

print("== the case no rule settles: the author's convention ==")
print("A subset of B can mean two things, both in active use:")
print("  (a) every member of A is in B          -- subset, equality allowed")
print("  (b) every member of A is in B, A != B  -- PROPER subset")
print("Nothing in the marks distinguishes them. The reader must consult the")
print("textbook. This is the one the lesson calls indefensible.")
```

Output:

```
notation           cands  run  crash  values
----------------------------------------------------------------------------
sum_{i=1}^{n} i^2      3    3      0  ['55', '30', '30']
x = 3 (mod 5)^2        3    3      0  ['False', 'True', '1']
f^2(x)                 3    3      0  ['15', '196', '196']
|S|                    3    2      1  ['3', '{2, 4, 6}']
A^T A                  3    2      1  ['[[10, 14], [14, 20]]', '[[7, 15], [10, 22]]']
----------------------------------------------------------------------------

== readings that RUN and DISAGREE: the expensive kind ==
  bounds  sum_{i=1}^{n} i^2  55      vs  30      disagree: True
  mod     x = 3 (mod 5)^2    False   vs  True    disagree: True
  f^2     f^2(x)             15      vs  196     disagree: True

Every one of these runs. No crash, no type error, no warning. This is
the only category worth building a tool for.

== what the attachment rule settles ==
  sum_{i=1}^{n} i^2  -> 1..n           because the bounds under the sign are inclusive at both ends
  x = 3 (mod 5)^2    -> mod 25         because the ')' closed before the '^', so the UNIT is squared
  f^2(x)             -> f(f(x))        because f is a function, and only functions compose
  |S|                -> len(S)         because S was declared a set, and |S| counts sets
  A^T A              -> (A^T) @ A      because T is a superscript on a MATRIX, so it is a label

4 of the 5 are settled by what the mark is attached to, plus the
declared TYPE of the free variable. |S| is the one that resists: it is
settled only because the surrounding text said S is a set. Nothing
inside the notation itself says so.

== the case no rule settles: the author's convention ==
A subset of B can mean two things, both in active use:
  (a) every member of A is in B          -- subset, equality allowed
  (b) every member of A is in B, A != B  -- PROPER subset
Nothing in the marks distinguishes them. The reader must consult the
textbook. This is the one the lesson calls indefensible.
```

**Reading the counts.** All five notations produced *at least two* runnable
readings, which is the headline: a tool that reports "it parsed" has told you
nothing. `sum_{i=1}^{n} i^2` has three candidates giving `55`, `30` and `30` — the
last two agreeing by coincidence, since `Σ_{i=0}^{n-1} i²` and `Σ_{i=1}^{n-1} i²`
are both `0+1+4+9+16` at `n = 5`. That is the worst case for any check: two
distinct wrong readings that present as one. `f^2(x)` has the same shape, `15` and
`196` and `196`, the last two being literally the same expression. `|S|` and
`A^T A` each have one candidate that crashes (`abs` on a set, and `A ** A` on a
list, both `TypeError`), so the type of the free variable has already refuted
one reading for free — the cheapest disambiguation available, and still not
enough on its own.

**Which failures cost the most.** The three in the second table are the expensive
ones, and the reason is uniform: every reading *executes*. `55` versus `30` is a
wrong sum, not an error. `f(f(13)) = 15` versus `f(13)² = 196` is a wrong value,
not an exception. And the `mod` row is why the binding `x` was set to `13` rather
than `28`: at `x = 28` both readings return `True` and the ambiguity hides, while
at `x = 13` the `mod 25` reading is `False` and the `mod 5` reading is `True`. A
test that happens to agree is not a test. The lesson's Exercise 3 already showed
the underlying sets differ in size by a factor of 5 over a 120-wide window, so the
disagreement is not a small numerical wobble — it is a different set.

**What resolves each one.** The attachment rule plus the declared type of the free
variable settles four of the five:

- Bounds under a sigma are inclusive at both ends → `range(1, n+1)`.
- A closed parenthesis before an exponent means the exponent applies to the
  parenthesised unit → `mod 25`.
- A superscript on a *function* can only mean composition; squaring needs a number
  → `f(f(x))`.
- A superscript on a *matrix* is a label, not a power → `(A^T) @ A`, which is
  `[[10, 14], [14, 20]]`.

**The two cases the information does not resolve.** First, `|S|`: the notation
carries no type information at all. `|S|` is resolved only because the surrounding
text declared `S` a set, and `|x|` in a lesson about absolute value is resolved
only because the text said `x` is a real. Lift `|S|` out of context into an
equation where `S` has never been introduced and there is nothing to go on. This
is the lesson's `In Plain Words` point taken to its conclusion: **position carries
the meaning, and sometimes there is no position to read.**

Second, the `⊂` case, which is genuinely worse because *no* amount of looking
helps. `A ⊂ B` is used by one camp to mean "every member of `A` is in `B`, and
`A` may equal `B`" and by another to mean "…and `A ≠ B`". Both are in current
print, the marks are identical, and no attachment rule, type declaration, or
sanity check separates them — the difference is a convention held by the author,
and it is only recoverable by reading the book's front matter or by asking. The
same shape of problem appears with `\u2282` versus `\u2286` in different
typefaces, and with whether `0 ∈ ℕ`. These are not failures of the reader; they
are failures of the notation, and the honest engineering response is to write
`A ⊆ B` and say "proper subset" in words when that is what you mean.

**The general conclusion.** A notation parser cannot be complete, because some
ambiguities are resolved only by the *declared types* of the free variables — not
in the string — and some only by the author's convention, which is not anywhere
at all. What a tool can do, and what the lesson's habit does by hand, is refuse
to guess: produce the candidates, notice that they disagree, and go and look at
what the text said the free variables were. Everything else is a coin flip
wearing a very convincing explanation — and, as the second table shows, a coin
flip that returns a plausible number rather than an error.

**The general conclusion.** A notation parser cannot be complete, because some
ambiguities are resolved only by the *declared types* of the free variables and by
the author's convention, neither of which is in the string. What a tool can do —
and what the lesson's habit does by hand — is refuse to guess. Produce the
candidates, notice that they disagree, and then go and look at what the text said
the free variables were. Everything else is a coin flip wearing a very convincing
explanation.

</details>

## Summary

- Notation is a compressed language with local rules. When a symbol is
  unfamiliar, look at what it is attached to; position carries the meaning.
- The colon in set-builder notation is Python's `for` plus `if`. Left of the
  colon is what you build, right of the colon is the condition.
- `Σ` is a `for` loop. Read the bounds line first: `Σ_{i=1}^{n}` is
  `range(1, n + 1)`, and off-by-one translation errors come from here.
- Big-O reads as an inequality with two unnamed constants: there exist `c` and
  `n₀` with `f(n) ≤ c·g(n)` for all `n ≥ n₀`. It is about growth, not values.
- `∀` is `all()`, `∃` is `any()`, and negating flips the quantifier *and* negates
  the predicate. The domain is part of the claim, not decoration.
- A script letter like `S` is a placeholder. The mean formula divides by `|S|`,
  which is undefined when `S` is empty, so the empty case is a real branch.
- Bound variables are function parameters. `i` under a summation is created and
  destroyed by the sum, exactly as a loop variable is by a loop.
- A formula with a free variable is a function, not a value. Pin the variable and
  it becomes a number; that is the only difference.
- Some notation has no Python equivalent — big-O, limits, infinite cardinality.
  That notation is where the mathematics lives rather than the mechanics.
- Translating a definition into code is mechanical: name the guard, turn "for
  every" into a loop, turn "there exists" into a search, and watch for vacuous
  truth over an empty range.

## Next

[Lesson 02 — Study Plan and Prerequisites](../part00_orientation/02_study_plan.md) uses everything above
to give you three concrete week-by-week plans and a self-diagnostic for deciding
which one to take. It assumes you can read a formula and run Python.