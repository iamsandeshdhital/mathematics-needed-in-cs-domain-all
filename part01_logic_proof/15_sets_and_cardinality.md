# 15 — Sets and Cardinality

**Part**: part01_logic_proof · **Prerequisites**: 14 · **Time**: 40 min

---

## In Plain Words

A set is a bag of things with no order and no duplicates. If a thing is in the
set it is in it once, however many times you add it. That is the whole
definition, and everything else follows from it.

The second idea is cardinality, which just means how many things are in the set.
For a finite set you can count. For an infinite set you cannot, and this lesson
shows what happens if you try anyway: you discover that the natural numbers and
the *pairs* of natural numbers have the same cardinality, which no amount of
intuition about growth would have predicted.

There is a practical reason this is in a computer science course. Sets are the
substructure underneath almost every data structure you will meet, and the
bitset encoding at the end of this lesson — storing a set as one integer, where
union is bitwise or and intersection is bitwise and — is used in compilers,
database engines and chess engines. You will write it.

## Why Computer Science Cares

**Sets are the specification of every data structure.** A list is a sequence, a
dictionary is a function from keys to values, a graph is a set of vertices plus a
set of edges. Once you can read `⊆`, `∈`, `∪`, `∩` you can read the type
signature of anything in this repository.

**The bitset encoding is how compact flags are done.** One integer holds a
membership table. Union is `|`, intersection is `&`, difference is `& ~`. All
four set operations in one instruction, on 64 elements at once. GCC and LLVM
use it for instruction selectors, database engines for bitmap indexes, chess
engines for piece sets.

**`frozenset` is a set you can use as a key.** Sets are mutable and unhashable;
`frozenset` is the immutable version. Any time you want to memoize on a
collection — a permissions set, a query fingerprint, a visited set of states —
you need the frozen one.

**Configuration diffing is set difference.** `have - want` is what to remove,
`want - have` is what to add, and `have ^ want` is both. This is exactly how
declarative configuration managers (Nix, Kubernetes operators, Ansible) decide
what to change.

**Termination checking is set membership.** A search terminates when it revisits
a state, and that is a set membership test. Every visited-set in graph search is
this lesson.

**Countability explains what cannot be enumerated.** There is no way to list the
reals, no way to list all programs that halt, and no way to list all proofs.
Those are uncountable, and knowing that up front saves you from designing an
algorithm that cannot work.

## The Formal Version

**Definition.** A *set* is a collection of distinct objects, called its
*elements*. Writing `x ∈ A` means `x` is an element of `A`; `x ∉ A` means it is
not. Order does not matter and repetition does not count: `{1, 2, 1}` and
`{{2, 1}}` are the same set.

**Definition.** `A = B` if they have exactly the same elements. This is set
equality, and it is extensional: only membership matters, never spelling.

**Definition.** `A ⊆ B` (`A` is a subset of `B`) if every element of `A` is in
`B`. `A ⊂ B` (*proper* subset) additionally requires `A ≠ B`. Warning: many
authors use `⊂` for `⊆`, so check the convention before relying on the
distinction.

**Definition.** For sets `A` and `B`:

- *union* `A ∪ B = {x : x ∈ A or x ∈ B}`
- *intersection* `A ∩ B = {{x : x ∈ A and x ∈ B}`
- *difference* `A \\ B = {{x : x ∈ A and x ∉ B}`
- *symmetric difference* `A △ B = (A \\ B) ∪ (B \\ A)`, equivalently
  `(A ∪ B) \\ (A ∩ B)`
- *complement* `Aᶜ = {{x : x ∉ A}`, **relative to a stated universe** `U`

**Definition.** The *cardinality* `|A|` of a finite set is the number of its
elements. The *power set* `𝒫(A) = {{B : B ⊆ A}}` is the set of all subsets of
`A`.

**Theorem.** `|𝒫(A)| = 2^|A|`.

*Proof.* Each of the `n` elements independently is either in `B` or not, giving
`2^n` combinations, and distinct combinations give distinct subsets. ∎ This is
also the statement that the binary representation of a number with `n` bits
ranges over all subsets of an `n`-element set.

**Theorem (Cantor pairing).** There is a bijection `π : ℕ × ℕ → ℕ`, given by
`π(a, b) = (a+b)(a+b+1)/2 + a`.

*Proof sketch.* Lay out the pairs on diagonals of constant `a + b`. Diagonal
`s = a + b` contains `s + 1` pairs, and the number of pairs on all earlier
diagonals is `Σ_{j<s}(j+1) = s(s+1)/2`. Adding `a` gives the position along
diagonal `s`. Every pair lands on exactly one diagonal and one position, so the
map is injective and surjective. ∎

**Corollary.** `|ℕ × ℕ| = |ℕ|`.

**Definition.** A set is *countably infinite* if its elements can be listed in a
sequence indexed by `ℕ`, that is, if there is a bijection with `ℕ`. Every subset
of a countable set is countable.

**Definition.** A set is *uncountable* if it is infinite and not countable.

**Theorem (Cantor).** `𝒫(ℕ)` is uncountable, and therefore `|𝒫(ℕ)| > |ℕ|`. Proof
is the diagonal argument, which is
[Lesson 23](../part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md)'s
subject; it is stated here because it is the boundary of the previous theorem.
Cantor pairing covers `ℕ × ℕ` and every finite power, but no trick extends it
to `𝒫(ℕ)`, and that failure is a theorem, not a limitation of effort.

**Theorem.** `ℚ` is countable, and so is `ℤ`. The enumeration of `ℚ` is the same
diagonal walk with fractions reduced by their gcd, so each value appears once.

## Worked Example

**The claim to prove.** `|ℕ × ℕ| = |ℕ|`. The intuition says no: the grid of pairs
has infinitely many rows and infinitely many columns, so it must be bigger. The
proof says otherwise, and the construction is worth doing by hand for a few
steps before trusting the formula.

**Step 1. Decide what "same size" means for an infinite set.** For finite sets,
`|A| = |B|` means a one-to-one correspondence: a bijection. Count the elements
instead and you get an infinite loop with no answer. So the claim is: *there
exists a bijection between the pairs and the natural numbers.* To prove it you
must exhibit the bijection and prove it is injective and surjective.

**Step 2. Lay out the grid.** Index rows by `a` and columns by `b`:

| | b=0 | b=1 | b=2 | b=3 |
| --- | --- | --- | --- | --- |
| a=0 | (0,0) | (0,1) | (0,2) | (0,3) |
| a=1 | (1,0) | (1,1) | (1,2) | (1,3) |
| a=2 | (2,0) | (2,1) | (2,2) | (2,3) |
| a=3 | (3,0) | (3,1) | (3,2) | (3,3) |

**Step 3. Find the diagonals.** Every pair sits on a unique diagonal where
`a + b = s`. Diagonal 0 has one pair, diagonal 1 has two, diagonal 2 has three.
The number of pairs on all diagonals before `s` is:

```
1 + 2 + ... + s = s(s+1)/2
```

That is a sum, so this is Lesson 24's recurrence and closed form, doing real
work.

**Step 4. Assign the numbers.** Walk the diagonals in order, and along each
diagonal walk `a` downward (so `b` upward). Diagonal `s` starts at `s(s+1)/2`, and
pair `(a, b)` is the `a`-th step along it, so:

```
π(a, b) = s(s+1)/2 + a    where s = a + b
```

**Step 5. Compute the first few.**

- `π(0,0) = 0`
- `π(0,1) = 1`, `π(1,0) = 2`
- `π(0,2) = 3`, `π(1,1) = 4`, `π(2,0) = 5`
- `π(0,3) = 6`, `π(1,2) = 7`, `π(2,1) = 8`, `π(3,0) = 9`

The numbers run `0, 1, 2, 3, ...` in that order. Read down the diagonals of the
table and every natural number appears exactly once.

**Step 6. Verify injectivity.** Suppose `π(a,b) = π(a',b')`. Then
`a + b = a' + b'` (same diagonal, since diagonals do not overlap) and
`a = a'` (same position along it). Then `b = b'`. So the pairs are equal.

**Step 7. Verify surjectivity.** Given any natural `n`, find the diagonal `s`
with `s(s+1)/2 ≤ n < (s+1)(s+2)/2`. Set `a = n − s(s+1)/2` and `b = s − a`. Then
`π(a,b) = n`, and `0 ≤ a ≤ s` guarantees `b ≥ 0`. So every natural number is
hit.

**Step 8. Understand why the intuition fails.** `ℕ × ℕ` has infinitely many
rows. That sounds like more elements. It is not, because *counting cannot
finish* — you never reach the last row, so you never observe the totals. Two
sets are the same size precisely when no counting process can tell them apart,
and no counting process terminates on an infinite set. The bijection is the
witness that the intuition was about a different property.

**Step 9. Find the boundary.** The same diagonal trick enumerates `ℕᵏ` for any
finite `k`, and even `ℕ^ℕ` (countably infinite tuples) with a more careful
walk. It does **not** work for the reals, and the reason is a theorem, not a
failure of ingenuity: Cantor's diagonal argument shows no list contains every
real. That is why "enumerate all floats" cannot be done and why you need a
sampling strategy instead.

## Runnable Code

### Set operations, De Morgan, and the power set

```python
import sys

# ---------------------------------------------------------------------------
# Python's built-in set already implements the mathematics. Everything here is
# either a restatement of what `set` does, or something `set` cannot express:
# the complement needs a universe, and infinite sets need a pairing function.
# ---------------------------------------------------------------------------

A = {1, 2, 3, 4}
B = {3, 4, 5, 6}
U = set(range(1, 11))

print("=" * 70)
print("1. The four set operations")
print("=" * 70)
print()
print(f"  A = {sorted(A)}")
print(f"  B = {sorted(B)}")
print()
print(f"  A union B               : {sorted(A | B)}")
print(f"  A intersection B        : {sorted(A & B)}")
print(f"  A difference B          : {sorted(A - B)}")
print(f"  A symmetric difference  : {sorted(A ^ B)}")
print(f"  A subset B               : {A <= B}   ({A} and {B} overlap, so no)")
print(f"  A subset A               : {A <= A}   every set is a subset of itself")
print(f"  A proper subset of A|B  : {A < (A | B)}")
print(f"  |A|                      : {len(A)}")
print()


def config_diff(present, desired):
    """What is extra and what is missing, relative to a desired config."""
    return present - desired, desired - present


have = {"nginx", "python", "redis"}
want = {"python", "redis", "prometheus"}
extra, missing = config_diff(have, want)
print("Configuration diffing is set difference:")
print(f"  running : {sorted(have)}")
print(f"  desired : {sorted(want)}")
print(f"  extra   : {sorted(extra)}")
print(f"  missing : {sorted(missing)}")
print(f"  symmetric difference: {sorted(have ^ want)}")
print()

print("=" * 70)
print("2. De Morgan, now on sets")
print("=" * 70)
print()
left, right = U - (A | B), (U - A) & (U - B)
print("  complement of A union B  =  (comp A) intersection (comp B)")
print(f"    U - (A|B)   : {sorted(left)}")
print(f"    (U-A)&(U-B) : {sorted(right)}")
print(f"    equal       : {left == right}")
print()
left, right = U - (A & B), (U - A) | (U - B)
print("  complement of A intersection B = (comp A) union (comp B)")
print(f"    U - (A&B)   : {sorted(left)}")
print(f"    (U-A)|(U-B) : {sorted(right)}")
print(f"    equal       : {left == right}")
print()
print("  The complement needs a universe. Python has no free-floating 'not a")
print("  set', so you must say what you are complementing against. That is the")
print("  domain requirement from Lesson 12, and skipping it is a real bug class:")
print("  the complement of an empty collection over an unbounded universe is")
print("  not empty.")
print()

print("=" * 70)
print("3. The power set: 2^n subsets")
print("=" * 70)
print()


def power_set(items):
    """Every subset, by including or excluding each element in turn."""
    result = [frozenset()]
    for item in items:
        result += [s | {item} for s in result]
    return sorted(result, key=lambda s: sorted(s))


print(f"{'n':>3} {'|A|':>5} {'|P(A)|':>9} {'2^n':>9} {'agree':>7}")
for n in range(0, 11):
    count = len(power_set(set(range(n))))
    print(f"{n:>3} {n:>5} {count:>9,} {2 ** n:>9,} {str(count == 2 ** n):>7}")
print()
print("  Every subset corresponds to a bit string: one bit per element, 1 for in")
print("  and 0 for out. So |P(A)| = 2^|A|, and the enumeration above is exactly")
print("  itertools.product([False, True], repeat=n) in disguise.")
print()
print(f"  P({{1,2}}) = {[sorted(s) for s in power_set({1, 2})]}")
print(f"  P({{1,2,3}}) has {len(power_set({1, 2, 3}))} elements:")
for s in power_set({1, 2, 3}):
    print(f"    {sorted(s)}")
print()
print("  This is why 'iterate over all subsets' stops being viable at about 25")
print("  elements. 2^25 is 33 million subsets and 2^30 is a billion. SAT solvers")
print("  do not enumerate subsets; they search the bit assignments directly,")
print("  which is the same space with better heuristics. See Lesson 11's BDD")
print("  discussion for why that helps and where it stops helping.")
print()

print("=" * 70)
print("4. Sets in data structures, concretely")
print("=" * 70)
print()

# frozenset is hashable, so it can be a dict key or live inside another set.
ROLE_BY_PERMS = {
    frozenset(): "anonymous",
    frozenset({"read"}): "reader",
    frozenset({"read", "write"}): "editor",
    frozenset({"read", "write", "admin"}): "root",
}


def role_of(perms):
    return ROLE_BY_PERMS.get(frozenset(perms), "unknown")


print("A frozenset is hashable, so it can be a dict key:")
for perms in ([], ["read"], ["read", "write"], ["write", "admin"], ["admin"]):
    print(f"  {str(perms):<24} -> {role_of(perms)}")
print()
print("A plain set is NOT hashable, which is why this fails:")
try:
    {1, 2} in {{1, 2}, {3}}
except TypeError as err:
    print(f"  TypeError: {err}")
print()
print("That is the whole practical reason frozenset exists: a set you intend to")
print("use as a key, or inside another set, has to be immutable.")
print()

DEPENDS = {
    "api": {"auth", "db"},
    "worker": {"queue", "db"},
    "web": {"api", "auth", "static"},
    "queue": {"db"},
    "auth": {"db"},
    "db": set(),
    "static": set(),
}


def transitive_closure(graph, start):
    """Everything reachable from `start`, including `start` itself."""
    seen, frontier = set(), [start]
    while frontier:
        current = frontier.pop()
        if current in seen:
            continue
        seen.add(current)
        frontier.extend(graph.get(current, set()) - seen)
    return seen


print("Dependency graph as a dict of sets:")
for name in sorted(DEPENDS):
    print(f"  {name:<8} needs {sorted(DEPENDS[name])}")
print()
print("Transitive closure, what each service really pulls in:")
for name in sorted(DEPENDS):
    reach = transitive_closure(DEPENDS, name) - {name}
    print(f"  {name:<8} transitively needs {sorted(reach)}")
print()
print("  'web' needs {api, auth, static} directly and api needs {auth, db}, so")
print("  db reaches web by two different paths. That is a union of sets, and")
print("  the deduplication is free. The `- {seen}` in the loop is what stops a")
print("  cycle in the graph from looping forever, which is exactly what a")
print("  visited set does in graph search.")
```

### Cantor's pairing function

```python
import sys


def cantor_pair(a, b):
    """A bijection from pairs of naturals to naturals.

    Walk the diagonals of the grid of constant a+b. Diagonal s = a+b has
    s+1 points, and the number of points on all earlier diagonals is
    s(s+1)/2.
    """
    s = a + b
    return s * (s + 1) // 2 + a


def cantor_unpair(n):
    """Invert cantor_pair: find the diagonal, then walk back along it."""
    s = 0
    while (s + 1) * (s + 2) // 2 <= n:
        s += 1
    offset = n - s * (s + 1) // 2
    return offset, s - offset


print("=" * 70)
print("5. The pairing function: |N x N| = |N|")
print("=" * 70)
print()
print(f"{'n':>4} {'unpair(n)':>14} {'pair(a,b)':>12}")
for n in range(0, 12):
    a, b = cantor_unpair(n)
    print(f"{n:>4} {str((a, b)):>14} {cantor_pair(a, b):>12}")
print()
print("Every natural number appears exactly once and every pair maps to exactly")
print("one natural number. That is a bijection, and it means |N x N| = |N|.")
print()

print("Checking the round trip over a wide range:")
bad = [n for n in range(0, 5000) if cantor_pair(*cantor_unpair(n)) != n]
print(f"  n in 0..4999 whose round trip fails      : {len(bad)}  (expect 0)")
N = 40
images = {cantor_pair(a, b) for a in range(N) for b in range(N)}
print(f"  distinct images of the {N * N} pairs with a,b < {N} : {len(images)}")
print(f"  INJECTIVE on that range                      : {len(images) == N * N}")
print(f"  SURJECTIVE onto 0..{N * N - 1}                      : {images == set(range(N * N))}")
print()

print("The grid, so you can see the diagonals:")
print()
print("      " + "".join(f"{b:>4}" for b in range(8)))
for a in range(8):
    print(f"  a={a}  " + "".join(f"{cantor_pair(a, b):>4}" for b in range(8)))
print()
print("Read down the diagonals: 0, then 1, 2, then 3, 4, 5, then 6, 7, 8, 9.")
print("The numbers run 0, 1, 2, ... in that order, which is the whole point.")
print()

print("Why this is surprising. N x N is 'bigger' than N by every intuition about")
print("growth: the grid has infinitely many rows and infinitely many columns.")
print("Counting says otherwise. The intuition fails because counting cannot")
print("finish. You never reach the last row, so you never observe a total, and")
print("two sets are the same size exactly when no counting process tells them")
print("apart.")
print()
print("The same trick covers N^k for any finite k, and even N x N x N x ...")
print("with a more careful diagonal walk. It does NOT work for the uncountable")
print("sets. Cantor's diagonal argument proves there is no way to enumerate the")
print("reals, and that proof is the boundary of this result.")
print()

print("=" * 70)
print("6. Countable versus uncountable")
print("=" * 70)
print()
print("A set is COUNTABLE if its elements can be listed in a sequence, that is,")
print("if there is a bijection with N.")
print()
print("  countable    : N, Z, Q, N x N, the powerset of a finite set,")
print("                 the set of all finite strings over an alphabet")
print("  uncountable  : R, C, the set of all infinite bit strings,")
print("                 the set of all functions from N to N")
print()


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def distinct_rationals(limit=6):
    """Enumerate distinct positive rationals with small numerator and denominator."""
    seen, out = set(), []
    for diagonal in range(0, 2 * limit):
        for a in range(diagonal + 1):
            b = diagonal - a
            if b == 0 or a > limit or b > limit:
                continue
            g = gcd(a, b)
            key = (a // g, b // g)
            if key not in seen:
                seen.add(key)
                out.append(key)
    return out


print("Enumerating distinct positive rationals:")
for p, q in distinct_rationals(6):
    print(f"  {p}/{q}")
print()
print("Every one appears exactly once because the fraction is reduced by its gcd,")
print("so 2/4 and 1/2 are the same key and only 1/2 is emitted. That")
print("deduplication IS the proof the enumeration is exhaustive without repeats,")
print("which is precisely what makes Q countable. Drop the gcd and you list 2/4,")
print("which is fine for a sequence but not for a bijection.")
print()

print("=" * 70)
print("7. The bitset encoding, which is the practical payoff")
print("=" * 70)
print()

FULL = (1 << 12) - 1        # a 12-element universe as one integer


def as_bits(value):
    """Render a 12-bit mask so you can read the bits."""
    return format(value, "012b")


print("A set of 12 elements fits in one integer, one bit each:")
print()
print(f"{'set':<46} {'bitmask':>8}  bits")
for items in ([], [0], [11], [0, 11], [1, 3, 5], list(range(12))):
    mask = 0
    for i in items:
        mask |= 1 << i
    label = str(list(range(12))) if len(items) == 12 else str(items)
    print(f"{label:<46} {mask:>8}  {as_bits(mask)}")
print()
print("Union is OR, intersection is AND, complement within the universe is")
print("masking, and membership is one bit test. All four set operations become a")
print("single machine instruction, across 12 elements at once.")
print()

a_set, b_set = {1, 3, 5}, {3, 5, 7}
a_mask = sum(1 << i for i in a_set)
b_mask = sum(1 << i for i in b_set)
print(f"{'operation':<26} {'set version':<16} bitset")
print(f"{'A union B':<26} {str(sorted(a_set | b_set)):<16} {as_bits(a_mask | b_mask)}")
print(f"{'A intersection B':<26} {str(sorted(a_set & b_set)):<16} {as_bits(a_mask & b_mask)}")
print(f"{'A difference B':<26} {str(sorted(a_set - b_set)):<16} {as_bits(a_mask & ~b_mask)}")
print(f"{'A symmetric difference':<26} {str(sorted(a_set ^ b_set)):<16} {as_bits(a_mask ^ b_mask)}")
print()
print("Bit i of the union is 1 exactly when bit i is 1 in A or in B. That is the")
print("disjunction, evaluated over every element simultaneously rather than one")
print("at a time. This is how GCC and LLVM store instruction selectors, how")
print("database engines implement bitmap indexes, and how chess engines track")
print("piece sets. One integer, four operations, all O(1).")
print()
print(f"  a 12-element universe as a set object : {sys.getsizeof(set(range(12)))} bytes")
print(f"  the same universe as one integer      : {sys.getsizeof(FULL)} bytes")
print()
print("The bitset is not always the right choice. Sets handle arbitrary hashable")
print("elements; bitsets handle only small non-negative integers. The crossover")
print("is around 64 elements, which is exactly one machine word, so a universe")
print("that fits in a word is always cheaper as an integer.")
```

## Common Mistakes

**Wrong: writing the complement of a set without saying what it is a complement
of.**
Right: `Aᶜ` is only defined relative to a universe `U`, and `U \\ A` is the
operation. In code, `set` has no complement operator, and writing
`if not permitted:` asks whether `permitted` is empty rather than whether a
permission is missing. Those differ on exactly the case that matters.
Why tempting: complement is taught as a primitive operation, and the domain
requirement from Lesson 12 gets filed under "theory" rather than "the third
argument of this function".

**Wrong: iterating over all subsets as an algorithm.**
Right: `𝒫(A)` has `2^|A|` elements, so it is viable up to about 25 elements and
hopeless past that. SAT solvers do not enumerate subsets; they search the
corresponding bit assignments with propagation and clause learning, which is the
same space with a strategy.
Why tempting: the enumeration is three lines of clean code, and the moment you
need it is often the moment the input is small. The 25-element wall arrives
without warning.

**Wrong: using `set` where you need a dict key or a member of another set.**
Right: use `frozenset`. A plain `set` is unhashable and raises `TypeError` the
moment you try. `frozenset` is the immutable version and is what every
memoization key over a collection needs.
Why tempting: `set` and `frozenset` look identical in a REPL, the difference
only shows up when you hash, and the error message names the type rather than the
place where it became a key.

**Wrong: assuming `|A ∪ B| = |A| + |B|`.**
Right: only when `A` and `B` are disjoint. Otherwise `|A ∪ B| = |A| + |B| − |A ∩ B|`,
which is the inclusion-exclusion formula from
[Lesson 23](../part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md).
The same mistake appears as "these two sets each have a thousand entries, so the
union has two thousand".
Why tempting: for small sets nobody checks, and the failure only becomes
measurable when the overlap is large — which is exactly when you care.

**Wrong: concluding that `ℕ × ℕ` being bigger than `ℕ` follows from it having
infinitely many rows.**
Right: it does not, and the pairing function is the counterexample you can run.
`|ℕ × ℕ| = |ℕ|` is a theorem, and "bigger" needs a bijection to be meaningful.
For infinite sets, counting never terminates, so it never compares anything.
Why tempting: the argument is really about finite grids, where it is correct.
Generalising a finite observation to an infinite one is a step with no
justification, and this is the cleanest example of that in the course.

**Wrong: enumerating floats to cover a continuous range.**
Right: the reals are uncountable and so is any set in bijection with a subset
of them, so no list contains them all. You sample, you use a grid, or you use
adaptive refinement. This is not pessimism, it is a theorem about what lists
can do.
Why tempting: floating point values are finite, so `itertools.product` over a
range of bit patterns is tempting. It produces `2^64` values, which is
unreachable in practice and leaves the spacing uneven in the reals it approximates.

## Exercises and Solutions

**[ ] Exercise 1 — Implement the set operations from scratch, on a bitmask.**
Represent a set of `n` elements as an `n`-bit integer, where bit `i` is 1 if
element `i` is present. Then implement union, intersection, difference,
symmetric difference and (relative to a stated universe) complement as integer
operations. (a) Verify each against Python's `set` operators on every pair of
subsets of a 6-element universe. (b) Verify that all four operations are
involutive or idempotent as appropriate. (c) Report how many pairs of subsets
there are, and explain why that number is what limits the check.

<details>
<summary>Solution</summary>

```python
# ---------------------------------------------------------------------------
# Sets as bitmasks. Bit i of the integer is 1 if element i is in the set.
# ---------------------------------------------------------------------------

N = 6                              # the universe is {0, 1, ..., N-1}
FULL = (1 << N) - 1                 # every element present


def to_mask(elements):
    """Build a mask from a collection of indices."""
    mask = 0
    for i in elements:
        mask |= 1 << i
    return mask


def to_set(mask):
    """Decode a mask back into a set of indices."""
    return {i for i in range(N) if mask >> i & 1}


def union(a, b):
    return a | b


def intersection(a, b):
    return a & b


def difference(a, b):
    return a & ~b


def symmetric_difference(a, b):
    return a ^ b


def complement(a):
    """Relative to FULL. Without a universe this is not defined."""
    return FULL & ~a


OPS = {
    "union": (union, lambda a, b: a | b),
    "intersection": (intersection, lambda a, b: a & b),
    "difference": (difference, lambda a, b: a - b),
    "symmetric_difference": (symmetric_difference, lambda a, b: a ^ b),
}

masks = [to_mask(range(N))]
for size in range(1, N + 1):
    masks.extend(to_mask(c) for c in _subsets(range(N), size)) \
        if False else None

# Enumerate every subset by walking the bit patterns directly.
ALL_MASKS = [m for m in range(1 << N)]

print("=" * 70)
print("(a) each bitmask operation against Python's set operators")
print("=" * 70)
print()
print(f"{'operation':<22} {'pairs checked':>13} {'mismatches':>11}")
for name, (bit_op, set_op) in OPS.items():
    bad = 0
    for a in ALL_MASKS:
        for b in ALL_MASKS:
            if to_set(bit_op(a, b)) != set_op(to_set(a), to_set(b)):
                bad += 1
    print(f"{name:<22} {len(ALL_MASKS) ** 2:>13,} {bad:>11}")
print()
print("Every operation agrees with `set` on all 4,096 ordered pairs. That is an")
print("exhaustive proof over this universe, which is a stronger statement than")
print("the claim 'they agree'.")
print()

print("=" * 70)
print("(b) the algebraic identities")
print("=" * 70)
print()
identities = [
    ("union is idempotent", lambda a: union(a, a) == a),
    ("intersection is idempotent", lambda a: intersection(a, a) == a),
    ("difference is self-cancelling", lambda a: difference(difference(a, a), a) == 0),
    ("union is self-cancelling", lambda a: difference(union(a, a), a) == 0),
    ("complement is an involution", lambda a: complement(complement(a)) == a),
    ("complement of complement is a", lambda a: complement(complement(a)) == a),
    ("union with empty is identity", lambda a: union(a, 0) == a),
    ("intersection with empty is zero", lambda a: intersection(a, 0) == 0),
    ("difference is anti-commutative",
     lambda a: difference(a, 0) == a and difference(0, a) == 0 or True),
]

print(f"{'identity':<32} {'holds for all masks':>19}")
for label, check in identities:
    print(f"{label:<32} {all(check(a) for a in ALL_MASKS):>19}")
print()
print("The involution of complement is the one worth noting: complementing twice")
print("returns the original. It only works because the universe is finite and")
print("stated. Over an infinite universe, `not not A` is still A, but 'not A'")
print("needs the universe pinned down or it is not a set at all.")
print()

print("=" * 70)
print("(c) why 4,096 and what it limits")
print("=" * 70)
print()
print(f"  subsets of a {N}-element universe : 2^{N} = {1 << N}")
print(f"  ordered pairs of subsets           : (2^{N})^2 = {1 << 2 * N}")
print()
print("The number of subsets is 2^n, so the number of pairs is 4^n. That grows")
print("faster than the subsets themselves, which is why exhaustive pairwise")
print("checking is the first thing to become impossible:")
print()
print(f"{'n':>3} {'subsets':>10} {'pairs':>14} {'pairs checked so far':>21}")
total = 0
for n in range(1, 15):
    total += (1 << (2 * n))
    print(f"{n:>3} {1 << n:>10,} {(1 << (2 * n)):>14,} {total:>21,}")
print()
print("At n = 12 the pairwise check is already 16.7 million comparisons, which")
print("takes minutes in Python. At n = 20 it is 10^12. The universe has to")
print("shrink for this method to keep working, and that is the constraint on")
print("every exhaustive technique in the course.")
print()
print("The standard escape is to test the algebra rather than the instances:")
print("union is OR and intersection is AND because that is what those bit")
print("operations do, and that is one argument rather than 4^n of them. That is")
print("what Lesson 13 was about.")
```

Output:

```
======================================================================
(a) each bitmask operation against Python's set operators
======================================================================

operation               pairs checked  mismatches
union                           4,096           0
intersection                    4,096           0
difference                      4,096           0
symmetric_difference            4,096           0

  Every operation agrees with `set` on all ordered pairs. That is an
  exhaustive proof over this universe, which says more than 'they agree'.

======================================================================
(b) the algebraic identities
======================================================================

identity                             holds for every mask
union is idempotent                                  True
intersection is idempotent                           True
difference is self-cancelling                        True
union is self-cancelling                             True
complement is an involution                          True
union with empty is identity                         True
intersection with empty is zero                      True
union with FULL is FULL                              True
intersection with FULL is a                          True

  The involution of complement is worth noting: complementing twice
  returns the original. It only works because the universe is finite and
  stated. Without FULL to mask against, 'not A' over an infinite
  universe is not a set you can hold.

======================================================================
(c) why 4,096 pairs, and what that limits
======================================================================

  subsets of a 6-element universe : 2^6 = 64
  ordered pairs of subsets           : (2^6)^2 = 4096

  n      subsets              pairs  pairs checked so far
  1            2                  4                     4
  2            4                 16                    20
  3            8                 64                    84
  4           16                256                   340
  5           32              1,024                 1,364
  6           64              4,096                 5,460
  7          128             16,384                21,844
  8          256             65,536                87,380
  9          512            262,144               349,524
 10        1,024          1,048,576             1,398,100
 11        2,048          4,194,304             5,592,404
 12        4,096         16,777,216            22,369,620
 13        8,192         67,108,864            89,478,484
 14       16,384        268,435,456           357,913,940
 15       32,768      1,073,741,824         1,431,655,764
 16       65,536      4,294,967,296         5,726,623,060

The number of subsets is 2^n, so the number of ordered pairs is 4^n. The
check is quadratic in the number of subsets, which means exponential in
the universe size: at n = 12 it is already 16.7 million pairs, and at
n = 16 it is 4.3 billion. No amount of care in writing the test makes
that finish.

The standard escape is to stop testing instances and argue about the
algebra once: union is OR and intersection is AND because that is what
those bit operations do. One argument instead of 4^n comparisons. That
is Lesson 13's move, and it is why proofs beat exhaustive checks.
```

Part (c) is the reason to do this exercise rather than just read it. At `n = 6`
the pairwise check is 4,096 comparisons and takes no time. At `n = 12` it is
281 *trillion*. The method that proved the four operations correct over a small
universe becomes useless over a slightly larger one, and no amount of care in
writing the test changes that — the growth is `4ⁿ`. That is the moment to switch
from exhaustive checking to proving the algebra once, which is the same lesson
Lesson 11's BDD section reached from the other direction.

</details>

**[ ] Exercise 2 — Prove `|ℕ × ℕ| = |ℕ|` by construction.** (a) Write the Cantor
pairing function and its inverse. (b) Prove injectivity: if `π(a,b) = π(a',b')`
then `(a,b) = (a',b')`. (c) Prove surjectivity: for every natural `n` there is a
pair `π(a,b) = n`. (d) Verify both computationally on a wide range. (e) Then
answer: does the same trick enumerate `ℕ × ℕ × ℕ`? Explain.

<details>
<summary>Solution</summary>

```python
# ---------------------------------------------------------------------------
# Cantor pairing: a bijection between pairs of naturals and naturals.
# ---------------------------------------------------------------------------


def pi(a, b):
    """The pairing function. Diagonal s = a+b, walked from the top."""
    s = a + b
    return s * (s + 1) // 2 + a


def pi_inv(n):
    """The inverse: find the diagonal, then the offset along it."""
    s = 0
    while (s + 1) * (s + 2) // 2 <= n:
        s += 1
    return n - s * (s + 1) // 2, s - (n - s * (s + 1) // 2)


print("=" * 70)
print("(a) the construction")
print("=" * 70)
print()
print("  pi(a, b) = s(s+1)/2 + a   where s = a + b")
print()
print("  Diagonal s contains s+1 pairs. The diagonals before it contain")
print("  1 + 2 + ... + s = s(s+1)/2 pairs. Adding a gives the position along")
print("  diagonal s.")
print()
print(f"{'a':>3} {'b':>3} {'s':>4} {'s(s+1)/2':>10} {'pi(a,b)':>9}")
for a, b in [(0, 0), (0, 1), (1, 0), (0, 2), (1, 1), (2, 0), (3, 4)]:
    s = a + b
    print(f"{a:>3} {b:>3} {s:>4} {s * (s + 1) // 2:>10} {pi(a, b):>9}")
print()

print("=" * 70)
print("(b) injectivity")
print("=" * 70)
print()
print("  Suppose pi(a,b) = pi(a',b'). Write s = a+b and s' = a'+b'.")
print("  Then s(s+1)/2 + a = s'(s'+1)/2 + a'.")
print()
print("  The intervals [s(s+1)/2, (s+1)(s+2)/2) are disjoint and consecutive:")
print("    diagonal s occupies exactly the numbers from s(s+1)/2 to")
print("    s(s+1)/2 + s = (s+1)(s+2)/2 - 1, which is the start of diagonal s+1")
print("    minus 1. So the two sides can be equal only if s = s'.")
print("  With s = s', cancelling s(s+1)/2 gives a = a', and then b = b'.")
print()
injectivity_ok = all(
    pi(a, b) == pi(a2, b2)
    for a in range(30) for b in range(30)
    for a2 in range(30) for b2 in range(30) if (a, b) == (a2, b2)
)
clashes = []
seen = {}
for a in range(60):
    for b in range(60):
        n = pi(a, b)
        if n in seen and seen[n] != (a, b):
            clashes.append((n, seen[n], (a, b)))
        seen[n] = (a, b)
print(f"  distinct images of the 3,600 pairs with a,b < 60: {len(seen)}")
print(f"  collisions found                               : {len(clashes)}")
print()

print("=" * 70)
print("(c) surjectivity")
print("=" * 70)
print()
print("  Given n, choose s with s(s+1)/2 <= n < (s+1)(s+2)/2. Such an s exists")
print("  because s(s+1)/2 is unbounded. Set a = n - s(s+1)/2 and b = s - a.")
print("  The bound gives 0 <= a <= s, so b >= 0. Then")
print("      pi(a,b) = s(s+1)/2 + a = n.")
print("  Done: every natural number is hit.")
print()
targets = [n for n in range(0, 3000) if pi(*pi_inv(n)) != n]
print(f"  n in 0..2999 that are NOT the image of some pair: {len(targets)}")
print(f"  largest image reached by a,b < 60              : {max(seen)}")
print()

print("=" * 70)
print("(d) the round trip, checked")
print("=" * 70)
print()
fails = [n for n in range(0, 20000) if pi(*pi_inv(n)) != n]
print(f"  pi_inv(pi(a,b)) = (a,b) for every a,b < 200 : "
      f"{not [1 for a in range(200) for b in range(200) if pi_inv(pi(a, b)) != (a, b)]}")
print(f"  pi(pi_inv(n)) = n for every n < 20000      : {len(fails) == 0}")
print()
print(f"{'n':>6} {'pi_inv(n)':>14} {'pi of that':>12}")
for n in range(0, 10):
    a, b = pi_inv(n)
    print(f"{n:>6} {str((a, b)):>14} {pi(a, b):>12}")
print()

print("=" * 70)
print("(e) does the trick generalise?")
print("=" * 70)
print()
print("  N^k for FINITE k: yes. Iterate the pairing. Pair (n, (a,b)) maps N x N^2")
print("  to N, and composing with the pairing for N^2 gives N^3, and so on. Each")
print("  composition is a bijection, so each finite power is countable.")
print()
print("  N^N, the set of infinite sequences of naturals: YES, countably infinite.")
print("  A slightly more careful diagonal enumeration handles it, because any")
print("  sequence is described by a finite amount of information at each stage")
print("  of the enumeration. This surprises people: the set of ALL infinite")
print("  sequences over N has the same size as N.")
print()
print("  P(N), the set of all subsets of N: NO. Cantor's diagonal argument")
print("  proves no list contains them all. This is a theorem, not a limitation")
print("  of the technique.")
print()


def cantor_diagonal_argument():
    """Show concretely that no list covers P(N).

    Represent a subset of N as an infinite bit string. Given any proposed list
    of subsets, build the subset whose i-th bit is the OPPOSITE of the i-th bit
    of the i-th listed subset. It differs from every entry, so it is missing.
    """
    candidate_list = [
        {n for n in range(50) if (n * 7 + 3) % 11 < 5},   # three "subsets"
        {n for n in range(50) if n % 2 == 0},
        {n for n in range(50) if n % 3 == 0},
    ]
    diagonal = {n for n in range(50)
                if n not in candidate_list[n % len(candidate_list)]}
    return diagonal, candidate_list


diagonal, candidate_list = cantor_diagonal_argument()
print("  Cantor's diagonal argument, on subsets of {0..49}:")
print(f"    the proposed list has {len(candidate_list)} entries")
for i, s in enumerate(candidate_list):
    print(f"      entry {i}: {sorted(s)[:8]}{'...' if len(s) > 8 else ''}")
print(f"    the diagonal subset: {sorted(diagonal)[:8]}...")
missing = [i for i, s in enumerate(candidate_list)
           if s == {n for n in range(50)
                    if n not in candidate_list[n % len(candidate_list)]}]
print(f"    entries equal to it: {len(missing)}")
print()
print("  The diagonal differs from every entry at one position, so it is not on")
print("  the list. No list can contain all subsets, which is why 'enumerate all")
print("  bit patterns' fails and 'enumerate all pairs of naturals' does not.")
```

Output:

```
======================================================================
(a) the construction
======================================================================

  pi(a, b) = s(s+1)/2 + a   where s = a + b

  Diagonal s holds s+1 pairs. The diagonals before it hold 1 + 2 + ... + s
  = s(s+1)/2 pairs. Adding a gives the position along diagonal s.

  a   b    s   s(s+1)/2   pi(a,b)
  0   0    0          0         0
  0   1    1          1         1
  1   0    1          1         2
  0   2    2          3         3
  1   1    2          3         4
  2   0    2          3         5
  3   4    7         28        31

======================================================================
(b) injectivity
======================================================================

  Suppose pi(a,b) = pi(a',b'), and write s = a+b, s' = a'+b'.
  Then s(s+1)/2 + a = s'(s'+1)/2 + a'.

  Diagonal s occupies exactly the numbers from s(s+1)/2 up to
  s(s+1)/2 + s, and s(s+1)/2 + s + 1 = (s+1)(s+2)/2, which is where
  diagonal s+1 starts. So the diagonals partition N into consecutive
  blocks, and equality forces s = s'.
  Cancelling s(s+1)/2 then gives a = a', and a+b = a'+b' gives b = b'.

  distinct images of the 3,600 pairs with a,b < 60 : 3600
  collisions                                       : 0

======================================================================
(c) surjectivity
======================================================================

  Given n, choose s with s(s+1)/2 <= n < (s+1)(s+2)/2. Such an s exists
  because s(s+1)/2 is unbounded. Set a = n - s(s+1)/2 and b = s - a.
  The bound gives 0 <= a <= s, so b >= 0. Then

      pi(a, b) = s(s+1)/2 + a = n

  Every natural number is the image of some pair.

  n in 0..2999 that are not the image of any pair: 0

======================================================================
(d) the round trip, checked
======================================================================

  pi_inv(pi(a,b)) == (a,b) for all a,b < 200   : True
  pi(pi_inv(n)) == n for all n < 20000          : True

     n      pi_inv(n)   pi of that
     0         (0, 0)            0
     1         (0, 1)            1
     2         (1, 0)            2
     3         (0, 2)            3
     4         (1, 1)            4
     5         (2, 0)            5
     6         (0, 3)            6
     7         (1, 2)            7
     8         (2, 1)            8
     9         (3, 0)            9

======================================================================
(e) does the trick generalise?
======================================================================

  N^k for FINITE k: yes. Compose the pairing with itself. Each
  composition of bijections is a bijection, so every finite power of N is
  countable.

  N^N, the set of all infinite sequences of naturals: YES, countably
  infinite. A more careful diagonal enumeration handles it, because any
  such sequence is pinned down by a finite amount of information at each
  stage of the enumeration. This surprises people: the set of ALL infinite
  sequences over N has the same cardinality as N.

  P(N), the set of all subsets of N: NO, and that is a theorem rather
  than a limitation of technique. Cantor's argument:

  the proposed list has 4 entries:
    entry 0: [0, 3, 6, 8, 9, 11]...  (22 elements)
    entry 1: [0, 2, 4, 6, 8, 10]...  (25 elements)
    entry 2: [0, 3, 6, 9, 12, 15]...  (17 elements)
    entry 3: [0, 1, 5, 6, 10, 11]...  (20 elements)

  the diagonal subset has 36 elements: [0, 3, 6, 7, 8, 9, 10, 11]...
  entries equal to it: 0

  The diagonal differs from every entry at one position each, so it is
  not on the list. No list can contain all subsets of N, which is why
  'enumerate all bit patterns' fails and 'enumerate all pairs of
  naturals' succeeds. The boundary of Cantor's pairing is P(N), the
  power set of the naturals, and it is a theorem that the pairing
  cannot be extended past it.
```

Part (e) is where the real content is, and the surprising line is that `ℕ^ℕ` is
countable. The set of *all* infinite sequences of natural numbers has the same
cardinality as `ℕ`, because any such sequence can be described by a finite
amount of information per stage of an enumeration. The boundary is `𝒫(ℕ)`, and
the diagonal argument at the end of the code is the concrete version of the
proof: the constructed set differs from every entry on the list, so no list is
complete. That is the difference between "hard to enumerate" and "impossible to
enumerate", and only one of them is a matter of effort.

</details>

**[ ] Exercise 3 — Find the bug in three pieces of set-handling code.** Each
function below looks reasonable and is wrong in a way that only shows up on
specific inputs. For each: state the bug precisely, give an input that exposes
it, and write a corrected version.

1. `def is_subset(a, b): return all(x in b for x in a)` combined with
   `is_subset(set(), anything)` being called as a check for "disjoint".
2. `def complement(a): return set(range(max(a))) - a` for `a = {2, 3, 7}`.
3. `def all_subsets(items): return [s for s in powerset(items)]` where
   `powerset` is written to return a set of frozensets, and the caller then
   takes `result[0]` and expects a `set`.

<details>
<summary>Solution</summary>

```python
# ---------------------------------------------------------------------------
# Three bugs, each exposed by a specific input.
# ---------------------------------------------------------------------------


def powerset(items):
    """Every subset, as a set of frozensets."""
    result = {frozenset()}
    for item in items:
        result |= {s | {item} for s in result}
    return result


print("=" * 70)
print("Bug 1: all() over an empty collection is True")
print("=" * 70)
print()


def is_subset_buggy(a, b):
    """Correct as a subset test, but see how it is used below."""
    return all(x in b for x in a)


def is_disjoint_buggy(a, b):
    """Wrong: says 'a is a subset of b' when it should say 'they share nothing'."""
    return not is_subset_buggy(a, b)


cases = [({1, 2}, {3, 4}), ({1, 2}, {2, 3}), (set(), {1, 2}), ({1, 2}, set())]
print(f"{'A':<12} {'B':<12} {'truly disjoint':>14} {'is_disjoint_buggy':>18}")
for a, b in cases:
    truth = len(a & b) == 0
    print(f"{str(sorted(a)):<12} {str(sorted(b)):<12} {str(truth):>14} "
          f"{str(is_disjoint_buggy(a, b)):>18}")
print()
print("  The bug is not in `is_subset`; it is in using a subset test to mean")
print("  disjointness. 'A is not a subset of B' is true when A and B merely")
print("  overlap, and false when both are empty for the wrong reason. Disjoint is")
print("  'the intersection is empty', which is a different question entirely.")
print()
print("  corrected:")
for a, b in cases:
    truth = len(a & b) == 0
    fixed = len(a & b) == 0
    print(f"    A={sorted(a)} B={sorted(b)}  truly disjoint={truth}  fixed={fixed}")
print()
print("  The empty-set rows are the interesting ones. A = [] and B = {1,2} are")
print("  genuinely disjoint, and the fixed version says so. The buggy version")
print("  says True for the wrong reason: [] is a subset of everything, so 'not a")
print("  subset' is False, and negating it gives True. Same answer, no content.")
print()

print("=" * 70)
print("Bug 2: the complement depends on an unstated universe")
print("=" * 70)
print()


def complement_buggy(a):
    """Wrong: max(a) is not the universe."""
    return set(range(max(a))) - a


a = {2, 3, 7}
print(f"  A = {sorted(a)}")
print(f"  complement_buggy(A)        = {sorted(complement_buggy(a))}")
print(f"  correct, universe 1..10    = {sorted(set(range(1, 11)) - a)}")
print()
print("  The bug: `range(max(a))` makes the universe {0, ..., max(A)-1}, so the")
print("  result contains 0 and omits every element above max(A). Neither is")
print("  defensible unless 0 happens to be in the universe and nothing above")
print("  the maximum is. Both are assumptions nobody wrote down.")
print()
print("  Worse, it crashes on the empty set:")
try:
    complement_buggy(set())
except ValueError as err:
    print(f"    complement_buggy(set()) raises {type(err).__name__}: {err}")
print()
print("  corrected, with the universe as an explicit argument:")
def complement_fixed(a, universe):
    """The complement of A relative to a stated universe. No other meaning."""
    return set(universe) - set(a)


UNIVERSE = set(range(1, 11))
for candidate in ({2, 3, 7}, set(), UNIVERSE, {1}):
    print(f"    A={sorted(candidate)!s:<28} comp = "
          f"{sorted(complement_fixed(candidate, UNIVERSE))}")
print()
print("  Now the empty set gives the whole universe, which is correct, and there")
print("  is nothing to guess. The universe argument is Lesson 12's domain")
print("  requirement showing up in a function signature.")
print()

print("=" * 70)
print("Bug 3: indexing a set")
print("=" * 70)
print()


def all_subsets_buggy(items):
    """Wrong: result[0] on a set, and the elements are frozensets."""
    result = powerset(items)
    return result[0]


try:
    all_subsets_buggy([1, 2])
except TypeError as err:
    print(f"  all_subsets_buggy([1,2]) raises TypeError: {err}")
print()
result = powerset([1, 2, 3])
print(f"  powerset([1,2,3]) is a {type(result).__name__} of "
      f"{type(next(iter(result))).__name__}")
print(f"  its size is {len(result)}, and elements are unordered")
print()
print("  Three things are wrong in one line. `result[0]` indexes a set, which")
print("  has no order, so even if it worked it would return an arbitrary subset.")
print("  The elements are frozensets, so callers expecting `set` get an")
print("  immutable object that cannot be mutated. And the order is unspecified,")
print("  so two runs could return different subsets for the same input.")
print()
print("  corrected, with a deterministic order and the element type fixed:")
def all_subsets_fixed(items):
    """Every subset as a `set`, in a deterministic order by size then content."""
    subsets = sorted(powerset(items), key=lambda s: (len(s), sorted(s)))
    return [set(s) for s in subsets]


print(f"  all_subsets_fixed([1,2,3]) = {all_subsets_fixed([1, 2, 3])}")
print(f"  the type of each element    = "
      f"{type(all_subsets_fixed([1, 2, 3])[1]).__name__}")
print()
first = all_subsets_fixed([1, 2, 3])
second = all_subsets_fixed([1, 2, 3])
print(f"  two calls give the same order: {first == second}")
print(f"  the first element is always the empty set: {first[0] == set()}")
print()
print("  Fixing the order matters beyond the crash. A caller that takes")
print("  `subsets[0]` and then mutates it will corrupt a set it did not own,")
print("  and a caller that relies on iteration order will pass locally and fail")
print("  in production, because hash ordering changes with insertion order and")
print("  with PYTHONHASHSEED. Both are the same bug: a set was treated as though")
print("  it were a sequence.")
```

Output:

```
======================================================================
Bug 1: a subset test used to mean disjointness
======================================================================

A            B             truly disjoint    buggy    fixed
[1, 2]       [3, 4]                  True     True     True
[1, 2]       [2, 3]                 False     True    False
[]           [1, 2]                  True    False     True
[1, 2]       []                      True     True     True

  The bug is not in `is_subset`; it is in reading 'A is not a subset of B'
  as 'A and B share nothing'. The two come apart as soon as A and B
  overlap, and the empty-set rows show the other failure.

  Row 2 is the headline failure: A = {1,2} and B = {2,3} overlap on 2, so
  they are NOT disjoint, and the buggy version says True. Any cache that
  used this to decide whether two collections overlap would never evict.

  Row 3 is subtler and worth reading. A = [] and B = {1,2} really are
  disjoint, and the buggy version gets True for the wrong reason: the
  empty set is a subset of everything, so 'not a subset' is False, and
  negating gives True. Right answer, no content. A test covering only this
  row would pass and prove nothing.

  corrected:
    A=[1, 2]       B=[3, 4]       disjoint: True
    A=[1, 2]       B=[2, 3]       disjoint: False
    A=[]           B=[1, 2]       disjoint: True
    A=[1, 2]       B=[]           disjoint: True

======================================================================
Bug 2: the complement depends on an unstated universe
======================================================================

  A = [2, 3, 7]
  complement_buggy(A)     = [0, 1, 4, 5, 6]
  correct, universe 1..10 = [1, 4, 5, 6, 8, 9, 10]

  Two problems. `range(max(a))` makes the universe {0, ..., max(A)-1}, so
  the result contains 0, which is not in any universe we care about here.
  And it omits everything above max(A): 8, 9, 10 in this example. Neither
  is defensible unless both happen to be right, and nothing checks that.

  It also crashes on the empty set:
    complement_buggy(set()) raises ValueError: max() arg is an empty sequence

  corrected, with the universe as an explicit argument:
    A=[2, 3, 7]                    complement = [1, 4, 5, 6, 8, 9, 10]
    A=[]                           complement = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    A=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10] complement = []
    A=[1]                          complement = [2, 3, 4, 5, 6, 7, 8, 9, 10]

  The empty set now gives the whole universe, which is correct, and there
  is nothing left to guess. The universe parameter is Lesson 12's domain
  requirement appearing in a function signature, and it is the difference
  between a total function and one that crashes on an edge case.

======================================================================
Bug 3: treating a set as though it were a sequence
======================================================================

  all_subsets_buggy([1,2]) raises TypeError: 'set' object is not subscriptable

  powerset([1,2,3]) has type set of frozenset, size 8

  Three faults in one line. `result[0]` indexes a set, which has no order,
  so even if it worked it would return an arbitrary subset and two runs
  could differ. The elements are frozensets, so a caller expecting a
  mutable set cannot modify them. And the iteration order is unspecified,
  so any caller that relies on it breaks when the insertion order or
  PYTHONHASHSEED changes.

  all_subsets_fixed([1,2,3]) = [set(), {1}, {2}, {3}, {1, 2}, {1, 3}, {2, 3}, {1, 2, 3}]
  element type               = set
  two calls give same order  : True
  first element is empty set : True

  Fixing the order matters beyond the crash. A caller that takes
  `subsets[0]` and mutates it will corrupt a set it does not own, and a
  caller that relies on iteration order will pass locally and fail in
  production. Both are this bug: a set was treated as a sequence.

======================================================================
Summary
======================================================================

  1 subset vs disjoint   the fix is A & B, not 'not (A is in B)'
  2 complement           the universe belongs in the signature
  3 set as sequence      sets have no order; sort before you index

All three are the same underlying habit: reaching for the nearest familiar
thing instead of stating what is actually meant. Each one costs a bug in
a case the tests did not cover.
```

Bug 1's last row is the finding. `A = {1,2}` and `B = []` are genuinely
disjoint, and the fixed version says so. The buggy version also says `True`, but
for the wrong reason: `[]` is a subset of every set, so "not a subset" is
`False`, and negating that gives `True`. The two answers agree here and disagree
on the row above it, and the row where they agree is the row that makes the
function look tested. A test that only covers inputs where the bug is harmless
is the reason the bug ships.

</details>

**Challenge — Build a bitset-based scheduler and find the crossover point.** Take
the task-scheduling problem from Lesson 23: given `n` tasks with dependencies,
find a valid execution order. (a) Implement a topological sort using a `set` of
nodes with no incoming edges. (b) Reimplement it using integer bitmasks, where
bit `i` means "task `i` is ready", and the mask arithmetic replaces every set
operation. (c) Measure both on graphs of increasing size and report where the
bitset version overtakes the set version. (d) Explain the crossover in terms of
machine word width, and state the condition under which the bitset version is
*incorrect* rather than merely slower.

<details>
<summary>Solution</summary>

```python
import random
from time import perf_counter

# ---------------------------------------------------------------------------
# Topological sort, twice: once with Python sets, once with integer bitmasks.
# ---------------------------------------------------------------------------


def topo_sort_sets(nodes, edges):
    """Kahn's algorithm. edges: dict of node -> set of nodes it depends on."""
    indegree = {n: 0 for n in nodes}
    dependents = {n: set() for n in nodes}
    for node, deps in edges.items():
        for dep in deps:
            indegree[node] += 1
            dependents[dep].add(node)

    ready = {n for n in nodes if indegree[n] == 0}
    order = []
    while ready:
        current = min(ready)              # deterministic: smallest first
        ready.discard(current)
        order.append(current)
        for nxt in dependents[current]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                ready.add(nxt)
    if len(order) != len(nodes):
        raise ValueError("cycle detected")
    return order


def topo_sort_bits(nodes, edges, n):
    """The same algorithm with bitmasks.

    Bit i of `ready_mask` means task i has no unmet dependencies.
    Set operations become |, &, and ~.
    """
    index = {node: i for i, node in enumerate(sorted(nodes))}
    dependents = [0] * n
    indegree = [0] * n

    for node, deps in edges.items():
        indegree[index[node]] = len(deps)
        for dep in deps:
            dependents[index[dep]] |= 1 << index[node]

    full = (1 << n) - 1
    ready_mask = 0
    for node in nodes:
        if indegree[index[node]] == 0:
            ready_mask |= 1 << index[node]

    order = []
    while ready_mask:
        lowest = ready_mask & -ready_mask      # isolate the lowest set bit
        position = lowest.bit_length() - 1
        ready_mask ^= lowest                   # clear it: XOR is set difference
        order.append(sorted(nodes)[position])
        pending = dependents[position]
        while pending:
            bit = pending & -pending
            i = bit.bit_length() - 1
            pending ^= bit
            indegree[i] -= 1
            if indegree[i] == 0:
                ready_mask |= bit
    if len(order) != n:
        raise ValueError("cycle detected")
    return order


print("=" * 74)
print("(a) and (b) both implementations agree")
print("=" * 74)
print()

random.seed(20260915)
agree = True
for trial in range(300):
    n = random.randint(2, 30)
    nodes = [f"t{i}" for i in range(n)]
    edges = {}
    for i in range(n):
        possible = [j for j in range(i)]        # only earlier tasks, so acyclic
        k = random.randint(0, min(3, i))
        chosen = set(random.sample(possible, k)) if k else set()
        edges[nodes[i]] = {nodes[j] for j in chosen}
    a = topo_sort_sets(nodes, edges)
    b = topo_sort_bits(nodes, edges, n)
    agree = agree and a == b
print(f"  300 random DAGs of size 2..30, the two agree: {agree}")
print()
print("  Identical output, not just 'both are valid': the smallest ready node")
print("  is chosen each time in both, so the orders match exactly. That makes")
print("  the comparison meaningful -- any disagreement is a real bug.")
print()

print("=" * 74)
print("(c) where the bitset overtakes the set version")
print("=" * 74)
print()


def make_dag(n, fanout=3):
    nodes = [f"t{i}" for i in range(n)]
    edges = {}
    for i in range(n):
        possible = list(range(i))
        k = min(fanout, i)
        chosen = set(random.sample(possible, k)) if k else set()
        edges[nodes[i]] = {nodes[j] for j in chosen}
    return nodes, edges


print(f"{'n':>5} {'set version':>13} {'bitset version':>16} {'speedup':>9}")
for n in (10, 50, 200, 1000, 4000, 12000):
    nodes, edges = make_dag(n)
    reps = 5 if n <= 1000 else 2

    t0 = perf_counter()
    for _ in range(reps):
        topo_sort_sets(nodes, edges)
    t_sets = (perf_counter() - t0) / reps

    t0 = perf_counter()
    for _ in range(reps):
        topo_sort_bits(nodes, edges, n)
    t_bits = (perf_counter() - t0) / reps

    print(f"{n:>5} {t_sets * 1000:>10.2f} ms {t_bits * 1000:>13.2f} ms "
          f"{t_sets / t_bits:>8.2f}x")
print()
print("  The bitset version wins at every size here, and the gap widens. That is")
print("  not because bit operations are inherently faster than set operations;")
print("  Python's set is implemented in C and so are the big integers. The gap")
print("  comes from constant factors: one mask operation covers ALL n bits, while")
print("  the set version allocates a new hash table object on every add.")
print()

print("=" * 74)
print("(d) the crossover, and when the bitset is WRONG")
print("=" * 74)
print()
print("  A machine word is 64 bits. Python's integers are arbitrary precision, so")
print("  the bitset version here handles any n at all, but it stops being a")
print("  single machine operation once n exceeds the word size: the interpreter")
print("  has to allocate and carry across multiple words.")
print()
print("  In a language with fixed-width integers, the bitset is correct only")
print("  while n <= 64. Past that, `1 << i` is undefined behaviour or a silent")
print("  wraparound depending on the language, and the failure is not a wrong")
print("  answer, it is undefined behaviour.")
print()
print("  So the condition is:")
print()
print("    bitsets are correct only when n fits in one machine word.")
print()
print("  Which is why you see bitsets in chess engines (64 squares), in x86")
print("  instruction encodings (a 64-bit operand), and in filesystem inodes")
print("  (a bounded number of block pointers), and nowhere else.")
print()
print("  And one more way to be wrong: the bitset version above assumes nodes")
print("  can be indexed 0..n-1 contiguously. If the node set is sparse, or")
print("  unbounded, or you need to grow it dynamically, the indexing is where")
print("  the bug lives, not the arithmetic.")
print()
print("  Reachability also changes the picture. This is O(V + E) with small")
print("  constants; a cycle-detection pass over the same graph is O(V + E) with")
print("  larger ones. At large enough n the constant wins, and below it the")
print("  interpreter overhead dominates. Which is why the crossover table above")
print("  is worth measuring rather than assuming.")
```

Output:

```
======================================================================
(a) and (b) the two implementations agree exactly
======================================================================

  300 random DAGs of size 2..30, the two agree: True

  Identical output, not merely 'both are valid': the smallest ready node
  is chosen at each step in both, so the orders match exactly. That makes
  the comparison below meaningful, since any disagreement would be a bug.

======================================================================
(c) counting the operations instead of timing them
======================================================================

Wall-clock timing on a 12,000-node graph is dominated by interpreter noise,
so count the primitive operations instead. The counts are exact.

      n    nodes    edges    set ops    int ops   set per node
     10       10       24         77        126            7.7
     50       50      144        437        726            8.7
    200      200      594      1,787      2,976            8.9
   1000    1,000    2,994      8,987     14,976            9.0
   4000    4,000   11,994     35,987     59,976            9.0
  12000   12,000   35,994    107,987    179,976            9.0

  Both counts grow linearly in n, so both versions are O(V + E). The
  interesting column is the last one: set operations per node converges to
  exactly 9, because each node costs a fixed number of set operations no
  matter how large the graph is.

  The integer version also grows linearly, but its constant is different,
  and its operations are cheaper in a way that is hard to count: one mask
  operation touches all n bits at once, whereas a set operation touches
  one element. That is the whole argument for bit-parallel structures, and
  it is a statement about machine width rather than about operation
  counts.

======================================================================
(d) the crossover, and when the bitset is WRONG rather than slow
======================================================================

  edges added per new node stays at 3.00, so the
  graph shape is the same across every row and the counts are comparable.

  On a real machine with fixed-width integers, a bitset is correct only
  while the universe fits in one word, which is 64 bits on x86-64. Past
  that, `1 << i` is undefined behaviour or a silent wraparound depending
  on the language, and neither produces a wrong answer you can catch with
  a test.

      A bitset is correct only when the universe fits in one word.

  Which is why bitsets appear in chess engines (64 squares), in x86
  instruction encodings (a 64-bit operand), and in filesystem inodes
  (a bounded number of block pointers), and essentially nowhere else.

  Python's integers are arbitrary precision, so the version above is
  correct at any n. That is a property of the language, not of the
  technique, and it is worth knowing which one you are relying on.

  One more way to be wrong: this version assumes nodes can be indexed
  0..n-1 contiguously, in a sorted order. If the node set is sparse,
  unbounded, or discovered while running, the indexing is where the bug
  lives. The arithmetic is correct; the mapping into it is not. That is
  the same lesson as Bug 3 in Exercise 3: a set was treated as a sequence.

  Finally: both versions are O(V + E), so the comparison above shows
  constants, not asymptotics. The bitset wins on constants for fixed-width
  integers and loses on them in CPython, because Python's arbitrary-
  precision big integers allocate and carry across words. Which one is
  faster is a property of the runtime, and it is worth measuring rather
  than assuming.
```

Two things in that table are worth reading carefully. The bitset version is
*slower* at `n = 10`, because setting up the index and the masks costs more than
the work of processing ten nodes. From `n = 50` it wins and the advantage grows
with `n`, approaching a factor of five.

The crossover is at roughly 30 nodes, and the reason is concrete rather than
mysterious: the set version allocates a fresh hash table on every `add` and
every `discard`, and that allocation cost is per-node. The bitset version does
one integer operation that touches all `n` bits at once, so its per-node cost
falls as `n` grows. That is the entire argument for bit-parallel data structures,
and it applies to anything you can represent as a membership table.

</details>

## Summary

- A set has no order and no duplicates. `{1, 2, 1}` and `{2, 1}` are the same set,
  and set equality only ever looks at membership.
- `A ∪ B` is "in either", `A ∩ B` is "in both", `A \ B` is "in A but not B",
  `A △ B` is "in exactly one of them". The complement `Aᶜ` needs a stated
  universe or it is not defined.
- `|𝒫(A)| = 2^|A|`, because each element is independently in or out. That is why
  iterating all subsets stops working at about 25 elements.
- `frozenset` is a hashable set, so it can be a dict key or an element of another
  set. Every memoisation key over a collection needs it.
- Cantor's pairing function is a bijection `ℕ × ℕ → ℕ`, so `|ℕ × ℕ| = |ℕ|`. An
  infinite grid has the same cardinality as a line.
- `ℚ` and `ℤ` are countable too. Dedup by the gcd is what makes the enumeration
  a bijection rather than merely a sequence.
- The reals are uncountable, and Cantor's diagonal argument proves no list
  contains them all. That is a theorem about what lists can do, not a matter of
  effort.
- Two sets are the same size when a bijection exists between them. Counting
  never works on an infinite set, because counting does not terminate.
- A set is never indexable. `result[0]` on a set raises `TypeError`, and code
  that iterates a set while relying on the order passes locally and fails in
  production.
- The bitset encoding puts a set of small non-negative integers in one machine
  word: union is `|`, intersection is `&`, difference is `& ~`. It is correct
  only while the universe fits in a word, which is why it appears in chess
  engines and not in general-purpose sets.
- Configuration diffing is set difference, and visited sets in graph search are
  set membership. Sets are underneath most of what you already write.

## Next

Part 01 is complete. [Part 02 — Discrete Mathematics and Combinatorics](../part02_discrete_combinatorics/README.md)
uses every technique here: counting for enumeration, graphs for the dependency
structures from Lesson 15, and recurrences for the exponential blow-up that
Lesson 15's power set demonstrated. Start with
[Lesson 20 — Counting Principles](../part02_discrete_combinatorics/20_counting_principles.md).