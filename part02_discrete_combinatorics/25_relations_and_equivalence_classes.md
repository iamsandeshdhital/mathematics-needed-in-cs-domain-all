# 25 — Relations and Equivalence Classes

**Part**: part02_discrete_combinatorics · **Prerequisites**: 24 · **Time**: 35 min

---

## In Plain Words

A **relation** is a rule for deciding, for any two objects, whether they are
connected in some way. "Is x smaller than y" is a relation. "Is x a file on the
same volume as y" is a relation. "Does x have the same birthday month as y" is a
relation. Once you write down such a rule as a set of pairs, you can ask three
structural questions, and the answers tell you what you are actually holding.

Is the relation **reflexive** — is every object related to itself? "Is x
divisible by x" is, for nonzero x. "Is x smaller than x" is not.

Is it **symmetric** — does x relating to y imply y relating to x? "Is x a sibling
of y" is symmetric. "Is x smaller than y" is not, which is exactly what makes
"smaller than" useful for sorting and siblings useless for it.

Is it **transitive** — does x relating to y and y relating to z imply x relates
to z? "Is x a descendant of y" is. "Is x within 3 metres of y" is not: a dog can
be within 3 m of one person and that person within 3 m of another, while the dog
is 6 m from the second person.

When all three hold, you have an **equivalence relation**, and that is a
particularly important thing to be holding. An equivalence relation does one
thing perfectly: it chops your set into **groups**, where everything inside a
group is interchangeable and nothing outside a group is. Members of the same
group are *equivalent*. The word "equivalent" is not decoration — it means
provably interchangeable, and that guarantee is what lets you throw away all but
one member.

This is not abstract bookkeeping. Union–find is the fastest way to maintain these
groups. `GROUP BY` in SQL is this operation. Deduplicating a list is this
operation. Deciding whether two file paths point at the same inode is this
operation. Type coercion, string interning, and cache-key normalisation are all
this operation. Learn the definition and you recognise all of them.

## Why Computer Science Cares

- **Union–find (disjoint set union).** The most-used data structure in
  competitive programming, and the engine behind Kruskal's minimum spanning tree
  algorithm, which is in Lesson [27](27_trees_and_spanning_trees.md). Path
  compression plus union by rank gives O(α(n)) amortised time — effectively
  constant. The classes are the sets, maintained incrementally.
- **SQL `GROUP BY`.** The engine groups rows by a tuple of column values. That
  tuple-equality *is* the equivalence relation, and the number of groups is the
  number of equivalence classes. `DISTINCT` picks one representative per class.
- **String interning and symbol tables.** Two string literals with the same
  characters are equivalent, so a dictionary stores one copy. Every compiler
  keeps an interned-symbol table, and `sys.intern` exposes it in Python.
- **Connected components.** In a graph, "is reachable from" is reflexive and
  symmetric but *not* transitive — which is why you must take the transitive
  closure before the classes are an equivalence. Lesson
  [26](26_graph_theory.md) makes this concrete; the naive implementation is
  O(n³) and union–find does it in near-linear time.
- **Type conversion and coercion.** An integer and the string "42" are
  equivalent once a coercion relation is declared. Overloading and implicit
  conversions are equivalence relations you design on purpose.
- **Deduplication and `distinct`.** `set()` in Python uses an equivalence relation
  (same object, or `__eq__` and `__hash__` agreeing). The correctness requirement
  for hashing is exactly that equal objects hash equally — a relation that must be
  both symmetric and consistent.
- **Canonicalisation.** Absolute paths, normalised Unicode, sorted CSV columns,
  and timezone-converted timestamps all exist so that two things that *mean* the
  same become *literally* the same object. Then you can use a set.
- **Bell numbers.** The number of partitions of an n-element set — the number of
  distinct equivalence structures on it — grows fast (15 at n = 4, 52 at n = 5, 203
  at n = 6, 877 at n = 7) and is the subject of Lesson
  [28](28_counting_strategies.md).

## The Formal Version

Let A be a finite set. A **binary relation on A** is a subset R ⊆ A × A. We write
a R b (read "a relates to b") when (a, b) ∈ R.

**Definition.** R is **reflexive** if a R a for every a ∈ A. It is **irreflexive**
if a R a for no a ∈ A. It is **symmetric** if a R b implies b R a for all a, b. It
is
**antisymmetric** if a R b and b R a imply a = b. It is **transitive** if a R b
and b R c imply a R c for all a, b, c.

**Theorem.** R is an **equivalence relation** if and only if it is reflexive,
symmetric, and transitive.

*Explanation.* Reflexivity makes self-comparison always available. Symmetry means
relatedness is mutual, so classes are well-defined. Transitivity means relatedness
chains: if a is as good as b and b is as good as c, then a is as good as c.
Together they mean "as good as" behaves like equality, and a relation that behaves
like equality is precisely an equivalence relation.

**Definition.** If ~ is an equivalence relation on A, the **equivalence class** of
a ∈ A is [a] = {b ∈ A : a ~ b}. The **quotient set** A/~ = {[a] : a ∈ A} is the
set of classes.

**Theorem (Partition theorem).** If ~ is an equivalence relation on A, the
equivalence classes { [a] : a ∈ A } form a **partition** of A: they are pairwise
disjoint, and their union is A.

*Explanation.* Disjointness: if [a] ∩ [b] ≠ ∅, pick x in the intersection. Then
a ~ x and b ~ x, so a ~ b by symmetry and transitivity, hence [a] = [b]. The union
covers A because a ∈ [a] by reflexivity. So every element is in exactly one class.

**Theorem (Converse).** Conversely, every partition of A determines exactly one
equivalence relation: a ~ b iff a and b lie in the same block. It is reflexive
because every block contains each of its elements; symmetric because blocks are
undirected; transitive because two same-block relations put all three in one
block.

*Explanation.* This is the punchline: **equivalence relations and partitions are
the same object viewed two ways.** A partition is the grouping; the equivalence
relation is the test. Counting one counts the other.

**Corollary (Representative).** Since the classes partition A, choosing one element
from each class gives a set of representatives R with |R| = |A/~| and every element
of A equivalent to exactly one element of R. This is the "keep only one per group"
legitimacy that dedup relies on.

**Definition.** a ≡ b (mod n) means n divides a − b. This is an equivalence
relation on ℤ with classes {a + kn : k ∈ ℤ}, and there are exactly n of them.

*Explanation.* Reflexive: n | 0. Symmetric: n | (a − b) ⟹ n | (b − a).
Transitive: n | (a − b) and n | (b − c) ⟹ n | (a − c). The n classes are the
n distinct remainders, and [SYMBOLS.md](../SYMBOLS.md) lists `≡` in its number
theory section.

**Definition.** The **composition** of R and S is R ∘ S = {(a, c) : ∃b, a S b and
b R c}. The **transitive closure** R* is the reflexive transitive closure.

*Explanation.* Composition is relation-multiplication, and it can leave the class
of equivalence relations: R ∘ S is reflexive and transitive if both R and S are,
but need not be symmetric. Taking the closure — adding every pair connected by a
chain — is what repairs it.

**Definition (Bridge to graphs).** R* is reflexive and symmetric whenever R is, so
R* is an equivalence relation, and its classes are exactly the **connected
components** of the graph with edges R.

*Explanation.* Two elements are equivalent under R* exactly when a path of edges
connects them, which is the definition of being in the same component. This is the
formal reason union–find solves connectivity.

**Definition.** A **partial order** is a relation that is reflexive, antisymmetric,
and transitive. If every two distinct elements are comparable it is a **total
order**.

*Explanation.* Contrast with equivalence: antisymmetry instead of symmetry says
there is a direction of strictness. This is the shape of "less than", and it is
the foundation of sorting, of topological order, and of the type hierarchy. Lesson
[82](../part06_algorithms_math/82_tools_for_algorithm_design.md) develops it
further.

## Worked Example

**The situation.** A log-analysis tool ingests user records and must group them.
Each record has a user id and a country. The tool needs to answer: how many
distinct users are there, and which records belong to the same user?

**Step 1 — Write the relation down.** Define a ~ b to mean "records a and b have
the same user id". Concretely, a and b are *the two sides of a pair in a set of
user ids*:

    R = { (r1, r2) : r1 and r2 are records with the same user id }

**Step 2 — Check reflexive.** Is record r1 related to itself? Yes — it has the same
user id as itself, trivially. Reflexive. ✓

**Step 3 — Check symmetric.** If r1 ~ r2 then they share a user id, so r2 ~ r1.
Sharing is mutual by construction. Symmetric. ✓

**Step 4 — Check transitive.** If r1 ~ r2 and r2 ~ r3, then r1, r2 and r3 all
carry the same user id, so r1 ~ r3. Transitive. ✓

All three hold, so R is an equivalence relation, and by the partition theorem the
classes partition the record set — every record lands in exactly one class, and
each class is one user. The number of classes is the answer to "how many distinct
users".

**Step 5 — Compute the classes from the table.** Records:

| record | user | country |
| - | - | - |
| r1 | u7 | DE |
| r2 | u3 | US |
| r3 | u7 | DE |
| r4 | u9 | JP |
| r5 | u3 | US |
| r6 | u9 | FR |

**Two candidate rules, and only one works.** A tempting alternative is "same user
*and* same country". That relation is also reflexive, symmetric and transitive — it
is also an equivalence relation, and also gives a partition. But it is the *wrong*
relation for the question, because r4 (u9, JP) and r6 (u9, FR) are the same user in
different countries. That rule produces 5 classes where the business question wants
4. The lesson: an equivalence relation is not automatically the one you meant, and
the choice of what counts as "same" is a modelling decision with real consequences.
This is precisely why SQL asks you to be explicit about which columns go in the
`GROUP BY`.

**Step 6 — The classes.** Equivalence class of r1 = {r1, r3}. Of r2 = {r2, r5}. Of
r4 = {r4, r6}. Three classes covering all six records. The quotient set is
{{r1, r3}, {r2, r5}, {r4, r6}} — three distinct users, even though there are four
distinct countries, because {r4, r6} spans two countries.

**Step 7 — Count with the quotient instead.** Since the classes partition, choosing
one representative per class gives {r1, r2, r4} with 3 elements, and every record is
equivalent to exactly one of them. So `SELECT DISTINCT user FROM records` returns 3
rows, and a `set()` of user ids returns 3 elements — and both are provably
complete, not heuristics.

**Step 8 — Connect to counting.** How many *different* partitions of a 4-element
set are there? That is a genuine counting problem with a real answer:

| blocks | count |
| - | - |
| 1 block (everything together) | 1 |
| 2 blocks | 7 |
| 3 blocks | 6 |
| 4 blocks (everything separate) | 1 |
| **total** | **15** |

So there are 15 distinct ways to group 4 objects, which is why "group these 4
things" has more answers than you would guess by hand. For 6 objects it is 203.
Counting these is the subject of Lesson [28](28_counting_strategies.md).

## Runnable Code

Relations as sets of pairs, and a classifier that checks every property. Run it
on examples designed to fail exactly one property each.

```python
A = {"a", "b", "c", "d"}

def is_reflexive(R, A):
    return all((x, x) in R for x in A)

def is_symmetric(R):
    return all((y, x) in R for (x, y) in R)

def is_antisymmetric(R):
    """No two distinct elements are related in both directions."""
    return all(x == y for (x, y) in R if (y, x) in R)

def is_transitive(R):
    """Every two-step chain x ~ y ~ z gives a one-step chain x ~ z.

    The two middle elements are named y and w and then matched with w == y.
    Writing `for (x, y) in R for (y, z) in R` in one comprehension would rebind y
    on the second loop and quietly test unrelated pairs."""
    return all((x, z) in R for (x, y) in R for (w, z) in R if w == y)

def is_equivalence(R, A):
    return is_reflexive(R, A) and is_symmetric(R) and is_transitive(R)

def is_partial_order(R, A):
    return is_reflexive(R, A) and is_antisymmetric(R) and is_transitive(R)

def describe(R, A):
    props = [
        ("reflexive", is_reflexive(R, A)),
        ("symmetric", is_symmetric(R)),
        ("antisymmetric", is_antisymmetric(R)),
        ("transitive", is_transitive(R)),
    ]
    tags = " ".join(name for name, ok in props if ok)
    kind = ("EQUIVALENCE" if is_equivalence(R, A)
            else "PARTIAL ORDER" if is_partial_order(R, A) else "neither")
    return f"{tags or '(none)':50s} -> {kind}"

# One example per interesting shape.
identity = {(x, x) for x in A}
total = {(x, y) for x in A for y in A}
less = {(x, y) for x in "abcd" for y in "abcd" if x < y}     # antisymmetric
sibling = {("a", "b"), ("b", "a"), ("c", "d"), ("d", "c")}  # symmetric, not reflexive
same_parity = {(x, y) for x in "abcd" for y in "abcd" if (ord(x) - ord("a")) % 2
               == (ord(y) - ord("a")) % 2}
within_2 = {(x, y) for x in "abcd" for y in "abcd" if abs(ord(x) - ord(y)) <= 2}

print("R                              properties")
for name, R in [
    ("identity (=)", identity),
    ("total (everything)", total),
    ("'<' on a<b<c<d", less),
    ("'same parity'", same_parity),
    ("'within 2 letters'", within_2),
    ("'sibling'", sibling),
]:
    print(f"{name:29s} {describe(R, A)}")

# the specific failures, printed so the reasons are visible
print(f"\n'<' is reflexive?          {is_reflexive(less, A)}  (a is not < a)")
print(f"'sibling' is reflexive?    {is_reflexive(sibling, A)}  (a has no sibling here)")
print(f"'within 2 letters' transitive? "
      f"{is_transitive(within_2)}  ('ac' and 'ad' leave 'cd' 3 apart)")
print(f"'< ' antisymmetric?         {is_antisymmetric(less)}  "
      f"(a<b and b<a cannot both hold)")
```

Equivalence classes, and a verification of the partition theorem: every element
in exactly one class.

```python
def classes_of(R, A):
    """The distinct equivalence classes.

    [a] and [b] are the same block whenever a ~ b, so collecting into a set is
    what removes the duplicate representatives."""
    return sorted({frozenset(b for b in A if (a, b) in R) for a in A}, key=sorted)

def check_partition(blocks, A):
    """Verify (i) disjoint and (ii) the union is A -- i.e. every element appears
    in exactly one block."""
    seen = [element for block in blocks for element in block]
    covers = set(seen) == set(A)
    disjoint = len(seen) == len(set(seen))
    return covers, disjoint

# Congruence mod 3 on {0,...,8}
n = 3
mod = {(x, y) for x in range(9) for y in range(9) if x % n == y % n}
blocks = classes_of(mod, set(range(9)))
print(f"congruence mod {n} on 0..8:")
for b in blocks:
    print(f"  {sorted(b)}")
reflexive = all((x, x) in mod for x in range(9))
symmetric = all((y, x) in mod for x, y in mod)
transitive = all((x, z) in mod for (x, y) in mod for (w, z) in mod if w == y)
print(f"reflexive={reflexive}, symmetric={symmetric}, transitive={transitive} "
      f"-> equivalence relation: {reflexive and symmetric and transitive}")
print(f"partition theorem holds: covers={check_partition(blocks, set(range(9)))}")
print(f"number of classes = {len(blocks)} = the modulus {n}")
print(f"representatives = {[sorted(b)[0] for b in blocks]}")

# Bell numbers: how many distinct partitions does an n-element set have?
def set_partitions(items):
    """All partitions of the sequence `items`, as a list of lists of sets."""
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for partition in set_partitions(rest):
        for i in range(len(partition)):
            yield partition[:i] + [partition[i] | {first}] + partition[i + 1:]
        yield [ {first} ] + list(partition)

from collections import Counter

print("\n n : total partitions (Bell number) : by number of blocks")
for n in range(1, 8):
    partitions = list(set_partitions(list(range(n))))
    by_blocks = Counter(len(p) for p in partitions)
    print(f" {n} : {len(partitions):>5d} : {dict(sorted(by_blocks.items()))}")
```

Union–find: maintaining the classes incrementally. This is the equivalence-class
data structure.

```python
class UnionFind:
    """Maintains the equivalence classes of a set under the relation
    'is connected to'. Path compression + union by rank: near-constant time."""

    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.rank = {x: 0 for x in items}
        self.count = len(items)

    def find(self, x):
        """The representative of x's class."""
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        # path compression: point everything on the path straight at the root
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx          # attach the shallower tree
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.count -= 1
        return True

    def classes(self):
        groups = {}
        for x in self.parent:
            groups.setdefault(self.find(x), set()).add(x)
        return [frozenset(g) for g in groups.values()]

V = ["r1", "r2", "r3", "r4", "r5", "r6"]
uf = UnionFind(V)
print(f"start: {uf.count} classes {sorted(uf.classes(), key=sorted)}")
for a, b in [("r1", "r3"), ("r2", "r5"), ("r4", "r6")]:
    uf.union(a, b)
    print(f"after union({a},{b}): {uf.count} classes "
          f"{sorted(sorted(c) for c in uf.classes())}")

# Redundant unions change nothing, which is the whole point.
print(f"union(r1, r3) again: merged={uf.union('r1', 'r3')}, "
      f"still {uf.count} classes")

# Cross-check against the transitive closure of the same edges.
edges = [("r1", "r3"), ("r2", "r5"), ("r4", "r6")]
nodes = set(V)
closure = {v: set() for v in nodes}
for a, b in edges:
    closure[a].add(b)      # undirected, so add both directions
    closure[b].add(a)
for k in nodes:            # Warshall transitive closure
    for i in nodes:
        if k in closure[i]:
            closure[i] |= closure[k]
via_closure = {frozenset(v for v in nodes if v == u or v in closure[u]) for u in nodes}
print(f"classes from union-find == classes from transitive closure: "
      f"{sorted(map(sorted, uf.classes())) == sorted(map(sorted, via_closure))}")
```

Database grouping: `GROUP BY` and `DISTINCT` are equivalence-class operations.

```python
records = [
    {"id": 1, "user": "u7", "country": "DE"},
    {"id": 2, "user": "u3", "country": "US"},
    {"id": 3, "user": "u7", "country": "DE"},
    {"id": 4, "user": "u9", "country": "JP"},
    {"id": 5, "user": "u3", "country": "US"},
    {"id": 6, "user": "u9", "country": "FR"},
]

def group_by(rows, keys):
    """Equivalent to SQL GROUP BY: bucket rows by the tuple of key values.

    Rows are equivalent when all key fields match, so the buckets are exactly the
    equivalence classes."""
    buckets = {}
    for row in rows:
        signature = tuple(row[k] for k in keys)
        buckets.setdefault(signature, []).append(row)
    return buckets

by_user = group_by(records, ["user"])
by_user_country = group_by(records, ["user", "country"])

print(f"GROUP BY user            : {len(by_user)} groups  {sorted(by_user)}")
print(f"GROUP BY user, country   : {len(by_user_country)} groups")
print(f"distinct users (DISTINCT) : {sorted({r['user'] for r in records})}")
print(f"distinct countries        : {sorted({r['country'] for r in records})}")
print(f"\nwhy they differ: r4 is u9/JP and r6 is u9/FR -- one user, two countries,")
print(f"so grouping by (user, country) splits them: "
      f"{sorted(by_user_country)}")

# Both groupings are equivalence relations, so both must partition the rows.
def is_partition(buckets, rows):
    ids = [r["id"] for group in buckets.values() for r in group]
    return sorted(ids) == sorted(r["id"] for r in rows)

print(f"\nboth are valid partitions: {is_partition(by_user, records)}, "
      f"{is_partition(by_user_country, records)}")
print(f"one representative per class (first row): "
      f"{ {k: v[0]['id'] for k, v in sorted(by_user.items())} }")
```

The transitive closure, done properly — the step that turns an arbitrary relation
into an equivalence relation.

```python
from collections import defaultdict

def warshall(nodes, relation):
    """Transitive closure by repeated composition.

    reach[k] should contain everything reachable from k. The trick is that after
    processing k, reach[i] also contains everything k can reach, for every i that
    could already reach k."""
    reach = {v: set(relation.get(v, set())) for v in nodes}
    for k in nodes:
        for i in nodes:
            if k in reach[i]:
                reach[i] |= reach[k]
    return reach

# An undirected graph: a road can be driven both ways, so each edge is stored
# in both directions. On a directed relation the closure would not be symmetric.
edges = {0: {1}, 1: {0, 2}, 2: {1, 0}, 3: {4}, 4: {3}}
nodes = set(edges)
reach = warshall(nodes, edges)

# Make the closure reflexive: a component always contains itself.
for v in nodes:
    reach[v].add(v)

print("original adjacency (one triangle 0-1-2, one edge 3-4):")
print(f"  {({v: sorted(edges[v]) for v in sorted(edges)})}")
print("\nreflexive transitive closure:")
print(f"  {({v: sorted(reach[v]) for v in sorted(reach)})}")
print(f"\n0 reaches 4 in the closure: {4 in reach[0]}  (disconnected, so no)")
print(f"4 reaches 0 in the closure: {0 in reach[4]}  (still no)")

reflexive = all(v in reach[v] for v in nodes)
symmetric = all((v in reach[u]) == (u in reach[v]) for u in nodes for v in nodes)
transitive = all(v in reach[u] for u in nodes for v in reach[u] for w in reach[v])
print(f"\nclosure is reflexive={reflexive}, symmetric={symmetric}, "
      f"transitive={transitive}")
print("so it is an equivalence relation, and its classes are the components:")

components = {frozenset(v for v in nodes if v == u or v in reach[u]) for u in nodes}
for c in sorted(components, key=sorted):
    print(f"  {sorted(c)}")
```

## Common Mistakes

**1. Assuming symmetry because the words sound symmetric.**

> Wrong: "'is at most 3 away from' sounds symmetric, so it is an equivalence
> relation."
> Right: On the alphabet {a, b, c, d}, "within 2 letters" relates a to c and c to
> e-style chains but a is 3 from d, so transitivity fails: a~c and c~d but not
> a~d. It is symmetric and irreflexive-at-the-edges, not an equivalence.
> Why the wrong one is tempting: the phrase is symmetric in the everyday sense,
> and you check symmetry, get a yes, and stop. Transitivity is the property people
> forget to test.

**2. Forgetting that "same X" needs the key you chose.**

> Wrong: "Group the log records by user and country, since that's what the report
> shows."
> Right: If the question is "how many distinct users", group by user alone.
> Grouping by (user, country) is a different equivalence relation and gives a
> different partition — 5 groups instead of 4 in the worked example.
> Why the wrong one is tempting: the report's columns are the ones in front of
> you. Equivalence relations are chosen, not discovered; the wrong key gives a
> perfectly valid partition of the wrong thing.

**3. Treating a directed relation as an equivalence relation.**

> Wrong: "'a follows b' is transitive, so it is an equivalence relation, so the
> classes are the followers."
> Right: Transitive yes, but not reflexive (you do not follow yourself) and not
> symmetric. You need the reflexive transitive closure, and even that is not
> symmetric — 'follows' is not an equivalence relation at all.
> Why the wrong one is tempting: "transitive" feels like the hard property, so
> passing it feels like finishing. Reflexivity and symmetry are separate
> requirements.

**4. Deduplicating by a hash without a total equivalence.**

> Wrong: "Put the objects in a `set`, so duplicates are gone."
> Right: A set is sound only if equality and hashing agree — equal objects must
> hash equally, and unequal objects must be reliably distinguishable. Mutable
> objects whose hash changes after insertion silently break the set, and the
> Python docs say so explicitly.
> Why the wrong one is tempting: `set()` works on almost everything, so the
> contract is invisible until it breaks. It is an invariant, not a feature.

**5. Assuming the transitive closure is cheap.**

> Wrong: "`'is reachable from'` is not transitive, so just add the pairs you need
> as you find them."
> Right: The naive closure is O(n³) with Floyd–Warshall and O(nm) with repeated
> BFS, and both need n² bits of output at minimum. Union–find computes the classes
> in O(α(n)) per union without ever materialising the closure.
> Why the wrong one is tempting: the number of pairs you need seems small in a
> small example. The cost is visible only when the relation is large, which is
> when you care.

---

## Exercises and Solutions

**[ ] Exercise 1 — Classify five relations.** For each relation on
A = {1, 2, 3, 4}, state whether it is reflexive, symmetric, antisymmetric,
transitive, and whether it is an equivalence relation:

(a) x ~ y iff x ≤ y; (b) x ~ y iff x + y = 6; (c) x ~ y iff x − y is divisible
by 3; (d) x ~ y iff x < y; (e) x ~ y iff |x − y| = 1.

<details>
<summary>Solution</summary>

(a) ≤ : reflexive yes; symmetric no; antisymmetric yes; transitive yes.
Not an equivalence relation (not symmetric). It is a partial order — in fact a
total order, since every two elements are comparable.

(b) x + y = 6: reflexive no (1 + 1 = 2 ≠ 6); symmetric yes; antisymmetric yes;
transitive no (1~5 and 5~1 but 1 ≁ 1). Not an equivalence relation: it is
symmetric but not reflexive.

(c) x − y divisible by 3: reflexive yes (0 is divisible by 3); symmetric yes
(3 | (a − b) ⟹ 3 | (b − a)); antisymmetric **no**, because 1 ~ 4 and 4 ~ 1 while
1 ≠ 4; transitive yes. Reflexive + symmetric + transitive, so it is an equivalence
relation with 2 classes: {1, 4} and {2, 3}.

(d) <: reflexive no; symmetric no; antisymmetric yes; transitive yes. Not an
equivalence relation, and not a partial order either (not reflexive).

(e) |x − y| = 1: reflexive no (unless n = 1); symmetric yes; antisymmetric yes;
transitive no (1~2 and 2~3 but 1 ≁ 3). Not an equivalence relation.

```python
from itertools import product

A = {1, 2, 3, 4}
relations = {
    "x <= y":        lambda x, y: x <= y,
    "x + y = 6":     lambda x, y: x + y == 6,
    "3 | (x - y)":   lambda x, y: (x - y) % 3 == 0,
    "x < y":         lambda x, y: x < y,
    "|x - y| == 1":  lambda x, y: abs(x - y) == 1,
}

def props(R):
    ref = all((x, x) in R for x in A)
    sym = all((y, x) in R for x, y in R)
    anti = all(x == y for x, y in R if (y, x) in R)
    tra = all((x, z) in R for (x, y) in R for (w, z) in R if w == y)
    return ref, sym, anti, tra

print(f"{'relation':16s} {'refl':>5} {'sym':>5} {'anti':>5} {'trans':>6}  verdict")
for name, f in relations.items():
    R = {(x, y) for x, y in product(sorted(A), repeat=2) if f(x, y)}
    ref, sym, anti, tra = props(R)
    if ref and sym and tra:
        verdict = "EQUIVALENCE RELATION"
    elif ref and anti and tra:
        verdict = "partial order"
    else:
        verdict = "neither"
    print(f"{name:16s} {str(ref):>5} {str(sym):>5} {str(anti):>5} {str(tra):>6}  {verdict}")
```
</details>

**[ ] Exercise 2 — Find the classes.** Let A = {0, 1, 2, 3, 4, 5, 6, 7, 8} and
x ~ y iff x ≡ y (mod 4). List the equivalence classes, verify the partition
theorem, and say how many there are without listing them.

<details>
<summary>Solution</summary>

Classes are the remainder sets: {0, 4, 8}, {1, 5}, {2, 6}, {3, 7}. Four classes.

Number of classes without listing: [a] is determined by a mod 4, so there is one
class per residue class, and the residue classes of mod n number exactly n. So
four — the modulus.

```python
A = set(range(9))
n = 4
R = {(x, y) for x in A for y in A if x % n == y % n}
# [a] and [b] are the same block whenever a ~ b, so a set removes the duplicates.
blocks = sorted({frozenset(b for b in A if (a, b) in R) for a in A}, key=sorted)

seen = [e for b in blocks for e in b]
print(f"classes: {[sorted(b) for b in blocks]}")
print(f"number of classes: {len(blocks)}")
print(f"covers A: {set(seen) == A}")
print(f"pairwise disjoint: {len(seen) == len(set(seen))}")
print(f"every element in exactly one class: {len(seen) == len(A) == len(set(seen))}")
```
</details>

**[ ] Exercise 3 — Union–find on a network.** Six hosts, with links
(A,B), (C,D), (B,C), (E,F). After adding each link, how many connected components
are there? Show that the answer equals the number of equivalence classes of the
"connected by a path" relation.

<details>
<summary>Solution</summary>

Links: A–B, C–D, B–C, E–F. Union–find merges two classes only when they were
distinct, so:

- start: 6 components
- A–B: 5
- C–D: 4
- B–C: merges {A,B} with {C,D} → 3
- E–F: 2

Final: {A,B,C,D} and {E,F}. The transitive closure of the link relation gives the
same two classes, which is the bridge from Lesson 24's Part on reachability.

```python
class UnionFind:
    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.rank = {x: 0 for x in items}
        self.count = len(items)

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.count -= 1
        return True

    def classes(self):
        groups = {}
        for x in self.parent:
            groups.setdefault(self.find(x), set()).add(x)
        return [frozenset(g) for g in groups.values()]

hosts = list("ABCDEF")
uf = UnionFind(hosts)
print(f"start: {uf.count} components")
for x, y in [("A", "B"), ("C", "D"), ("B", "C"), ("E", "F")]:
    merged = uf.union(x, y)
    print(f"link {x}-{y}: merged={merged}, components={uf.count}")
print(f"final classes: {sorted(sorted(c) for c in uf.classes())}")
```
</details>

**[ ] Exercise 4 — Which grouping is right?** You have user records with columns
`user`, `country`, and `plan`. Answer these and justify each:

(a) how many distinct users; (b) how many user-country combinations; (c) how many
distinct (user, country, plan) triples.

Which of these counts is a "number of equivalence classes", and what is the
equivalence relation in each case?

<details>
<summary>Solution</summary>

All three are equivalence classes — for a key tuple K, the relation "rows agree on
every field in K" is reflexive, symmetric, and transitive by construction.

(a) key = (user). Relation: same user id. Classes: one per user.
(b) key = (user, country). Relation: same user *and* same country. This is
strictly finer than (a): a user appearing in two countries occupies two classes.
(c) key = (user, country, plan). Strictly finer than (b), and a user who changed
plan occupies two classes.

Refinement is the ordering principle: adding a key field can only split classes,
never merge them, because agreement on more fields implies agreement on fewer. That
monotonicity is exactly the transitivity of the underlying relations.

```python
records = [
    {"user": "u1", "country": "DE", "plan": "pro"},
    {"user": "u1", "country": "FR", "plan": "pro"},
    {"user": "u2", "country": "DE", "plan": "free"},
    {"user": "u1", "country": "DE", "plan": "free"},
]

def group_count(rows, keys):
    return len({tuple(r[k] for k in keys) for r in rows})

for keys in (("user",), ("user", "country"), ("user", "country", "plan")):
    print(f"{str(keys):32s} -> {group_count(records, keys)} classes")
print("\ncounts never decrease as keys are added: refining an equivalence")
print("relation can only split classes, because agreeing on more implies less")
```
</details>

**[ ] Exercise 5 — Bell numbers.** How many partitions does a 5-element set have?
Break it down by number of blocks, and verify the total by an independent route:
count the ways to write 5 as an unordered sum of positive integers.

<details>
<summary>Solution</summary>

By number of blocks (Stirling numbers of the second kind S(5, k)):

| blocks k | S(5, k) |
| - | - |
| 1 | 1 |
| 2 | 15 |
| 3 | 25 |
| 4 | 10 |
| 5 | 1 |

Total 52, which is B₅.

The independent route: a partition into k blocks of sizes
n₁ + ⋯ + n_k = 5 with n₁ ≤ ⋯ ≤ n_k is exactly an integer partition of 5. The
integer partitions of 5 are 5, 4+1, 3+2, 3+1+1, 2+2+1, 2+1+1+1, 1+1+1+1+1 — seven
of them. For each block-size shape, the number of set partitions is
5!/(∏ n_i! ∏ (multiplicity of each size)!). Summing: 5 gives 1; 4+1 gives
C(5,1) = 5; 3+2 gives C(5,3) = 10; 3+1+1 gives C(5,3) = 10; 2+2+1 gives
C(5,2)C(3,2)/2! = 15; 2+1+1+1 gives C(5,2) = 10; 1+1+1+1+1 gives 1. Sum = 52 ✓

```python
from itertools import combinations
from math import factorial

def integer_partitions(n, max_part=None):
    if n == 0:
        yield []
        return
    if max_part is None or max_part > n:
        max_part = n
    for k in range(max_part, 0, -1):
        for rest in integer_partitions(n - k, k):
            yield [k] + rest

def set_partitions_count_by_shape(items, shape):
    """Partition `items` into blocks whose sizes, sorted, equal `shape`."""
    n = len(items)
    from collections import Counter
    mult = Counter(shape)
    denom = 1
    for size in shape:
        denom *= factorial(size)
    for m in mult.values():
        denom *= factorial(m)
    return factorial(n) // denom

items = list(range(5))
total = 0
for shape in integer_partitions(5):
    ways = set_partitions_count_by_shape(items, shape)
    total += ways
    print(f"  block sizes {str(shape):22s} -> {ways:3d} partitions")
print(f"total partitions of a 5-element set: {total}")

# And the same total straight from set partitions.
def set_partitions(seq):
    if not seq:
        yield frozenset()
        return
    first, rest = seq[0], seq[1:]
    for p in set_partitions(rest):
        for i in range(len(p)):
            yield p[:i] + [p[i] | {first}] + p[i + 1:]
        yield [{first}] + list(p)

print(f"enumerated directly: {len(list(set_partitions(list(range(5)))))}")
print(f"agree: {total == len(list(set_partitions(list(range(5)))))}")
```
</details>

**[ ] Exercise 6 — Build a relation from a partition.** Let `A = {1, 2, 3, 4, 5, 6}`.
Consider two partitions:

    P1 = { {1,2}, {3}, {4,5,6} }
    P2 = { {1,2,3}, {4}, {5,6} }

(a) Write down the relation "a and b lie in the same block" for each, as an
explicit set of pairs. (b) Verify that each is reflexive, symmetric, and transitive.
(c) Recover the classes from the relation and confirm you get the original partition.
(d) Do the two relations differ, and by how many pairs? Finally, how many partitions
does a **4**-element set have, and how does that number relate to the two
partitions above?

<details>
<summary>Solution</summary>

**(a) The relations.** The relation from a partition contains every ordered pair
`(a, b)` lying in one block.

    R1 = {1,2}×{1,2} ∪ {3}×{3} ∪ {4,5,6}×{4,5,6}       (4 + 1 + 9 = 14 pairs)
    R2 = {1,2,3}×{1,2,3} ∪ {4}×{4} ∪ {5,6}×{5,6}       (9 + 1 + 4 = 14 pairs)

Note the useful identity this exhibits: `|R| = Σ (block size)²`, because `R` is the
union of complete relations on each block.

**(b) The three properties, for both.**

*Reflexive:* every element lies in a block and a block contains itself, so `(a, a)`
is in the relation. This is the only place reflexivity is used.
*Symmetric:* blocks are undirected, so if `(a, b)` is in a block's complete relation
then so is `(b, a)`.
*Transitive:* if `a ~ b` and `b ~ c`, then `a`, `b` and `c` all lie in one block, so
`(a, c)` is in the same block's complete relation.

Both are therefore equivalence relations, by the definition.

**(c) The round trip.** Recovering the classes means computing `[a] = {b : (a, b) ∈ R}`
for each `a` and collapsing duplicates. Because symmetry plus transitivity give
`[a] = [b]` whenever `a ~ b`, the distinct classes are exactly the blocks. The code
below confirms this for both partitions.

**(d) They differ.** Both relations have 14 pairs, but they are not the *same* 14
pairs: `(1, 3)` belongs to `R₂` and not to `R₁`, while `(3, 4)` belongs to `R₁` and
not to `R₂`. So the converse theorem really is one relation per partition, and
"same cardinality" does not mean "same relation".

For the counting link: a 4-element set has **15** partitions, hence 15 equivalence
relations, hence `B₄ = 15`. Both `P₁` and `P₂` above are partitions of a 6-element
set with exactly 3 blocks, and each is one of the 3-block partitions of that set —
there are 90 of them, which is `S(6,3) = 90` in the lesson's Stirling row. Counting
one structure therefore counts the other exactly.

```python
from itertools import product

A = set(range(1, 7))

def relation_from_partition(blocks):
    """a ~ b exactly when a and b lie in the same block."""
    R = set()
    for block in blocks:
        for a, b in product(block, repeat=2):
            R.add((a, b))
    return R

def is_reflexive(R, A):
    return all((x, x) in R for x in A)

def is_symmetric(R):
    return all((y, x) in R for (x, y) in R)

def is_transitive(R):
    return all((x, z) in R for (x, y) in R for (w, z) in R if w == y)

def classes_of(R, A):
    """[a] and [b] coincide whenever a ~ b, so a set removes the duplicates."""
    return sorted({frozenset(b for b in A if (a, b) in R) for a in A}, key=sorted)

P1 = [{1, 2}, {3}, {4, 5, 6}]
P2 = [{1, 2, 3}, {4}, {5, 6}]

for name, P in (("P1", P1), ("P2", P2)):
    R = relation_from_partition(P)
    want = sorted({frozenset(b) for b in P}, key=sorted)
    print(f"{name}: reflexive={is_reflexive(R, A)} symmetric={is_symmetric(R)} "
          f"transitive={is_transitive(R)}")
    print(f"   blocks given  : {[sorted(b) for b in want]}")
    print(f"   classes of R  : {[sorted(b) for b in classes_of(R, A)]}")
    print(f"   round trip ok : {want == classes_of(R, A)}")
    print(f"   |R| = {len(R)} = sum of block-size squares = "
          f"{sum(len(b) ** 2 for b in P)}")

R1, R2 = relation_from_partition(P1), relation_from_partition(P2)
print(f"\nR1 == R2 as relations: {R1 == R2}")
print(f"(1,3) in R2: {(1, 3) in R2}  |  (1,3) in R1: {(1, 3) in R1}")
```

Output:

```
P1: reflexive=True symmetric=True transitive=True
   blocks given  : [[1, 2], [3], [4, 5, 6]]
   classes of R  : [[1, 2], [3], [4, 5, 6]]
   round trip ok : True
   |R| = 14 = sum of block-size squares = 14
P2: reflexive=True symmetric=True transitive=True
   blocks given  : [[1, 2, 3], [4], [5, 6]]
   classes of R  : [[1, 2, 3], [4], [5, 6]]
   round trip ok : True
   |R| = 14 = sum of block-size squares = 14

R1 == R2 as relations: False
(1,3) in R2: True  |  (1,3) in R1: False
```

</details>

**[ ] Challenge 7 — A relation that is not an equivalence.** On A = {1, 2, 3, 4, 5}
let R be the directed relation "x reaches y if y = 2x" restricted to A. Is R an
equivalence relation? Is R ∪ R⁻¹? Is R*? Compute the classes at each stage.

<details>
<summary>Solution</summary>

R = {(1,2), (2,4)}: not reflexive (no (x,x)), not symmetric ((1,2) ∈ R but
(2,1) ∉ R), not transitive. Not an equivalence relation.

R ∪ R⁻¹ = {(1,2), (2,4), (2,1), (4,2)}: symmetric now, still not reflexive and
not transitive ((1,2) and (2,1) but (1,1) ∉ R).

R* (reflexive transitive closure) = R ∪ R⁻¹ ∪ {(x,x)} plus the chains. Chaining
1→2→4 and 4→2→1 gives 1→4 and 4→1; chaining 1→4→2 gives 1→2 (already there).
So R* = {(1,2),(2,4),(4,2),(2,1),(1,4),(4,1)} ∪ {(1,1),(2,2),(3,3),(4,4),(5,5)}.

R* is reflexive and symmetric and transitive — an equivalence relation, with
classes {1, 2, 4}, {3}, {5}. Note 3 and 5 are isolated: their class is a
singleton, which the reflexivity clause guarantees.

```python
A = {1, 2, 3, 4, 5}
R = {(x, 2 * x) for x in A if 2 * x in A}
inv = {(y, x) for (x, y) in R}
Rstar = (R | inv | {(x, x) for x in A})
# close it under composition
changed = True
while changed:
    changed = False
    for x, y in list(Rstar):
        for y2, z in list(Rstar):
            if y == y2 and (x, z) not in Rstar:
                Rstar.add((x, z)); changed = True

def check(rel):
    ref = all((x, x) in rel for x in A)
    sym = all((y, x) in rel for x, y in rel)
    tra = all((x, z) in rel for x, y in rel for w, z in rel if w == y)
    return ref, sym, tra

for name, rel in [("R", R), ("R u R^-1", R | inv), ("R*", Rstar)]:
    ref, sym, tra = check(rel)
    classes = sorted(sorted({x for x in A if (a, x) in rel} - {a}) + [a] for a in A)
    print(f"{name:10s} reflexive={ref!s:5} symmetric={sym!s:5} transitive={tra!s:5}")
print(f"\nR* = {sorted(Rstar)}")
distinct = sorted({frozenset({a} | {x for x in A if (a, x) in Rstar}) for a in A},
                   key=sorted)
print(f"classes of R* : {[sorted(c) for c in distinct]}")
```
</details>

## Summary

- A binary relation on A is a subset of A × A; reflexive, symmetric,
  antisymmetric, and transitive are the four structural tests.
- Reflexive + symmetric + transitive = equivalence relation, which is exactly a
  relation that behaves like equality.
- Equivalence classes always partition A: disjoint, exhaustive, and unique. This
  is proved in two lines from the three axioms.
- Equivalence relations and partitions are the same object: the converse theorem
  turns any partition into exactly one equivalence relation.
- Congruence modulo n is the model example, with exactly n classes.
- Because classes partition, picking one representative per class is legitimate —
  that is the correctness argument for `set()`, `DISTINCT`, and string interning.
- The transitive closure of a symmetric relation is an equivalence relation, and
  its classes are the connected components — the bridge to
  [Lesson 26](26_graph_theory.md).
- Union–find maintains the classes incrementally in O(α(n)) amortised time, and
  choosing the *right* key is a modelling decision with visible consequences.

## Next

[Lesson 26 — Graph Theory](26_graph_theory.md) assumes you know what an
equivalence relation and a partition are, and that "connected by a path" is a
relation you may need to close; it turns that into the language of vertices,
degrees, connectivity, and planar graphs.