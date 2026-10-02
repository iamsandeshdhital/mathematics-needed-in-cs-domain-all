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
  algorithm, which is in Lesson [27](../part02_discrete_combinatorics/27_trees_and_spanning_trees.md). Path
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
  [26](../part02_discrete_combinatorics/26_graph_theory.md) makes this concrete; the naive implementation is
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
  [28](../part02_discrete_combinatorics/28_counting_strategies.md).

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
Counting these is the subject of Lesson [28](../part02_discrete_combinatorics/28_counting_strategies.md).

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

## Formula Sheet

Every symbol and formula this lesson introduces. `A` is a finite set, `R ⊆ A × A`
a binary relation, `a R b` means `(a, b) ∈ R`, `~` denotes an equivalence
relation, and `[n]` is the index set `1, …, n`.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| Relation on `A` | `$R \subseteq A \times A$`, written `$a\,R\,b$` | a yes/no test on ordered pairs | the general object this lesson classifies |
| Reflexive | `$\forall a \in A,\ a\,R\,a$ | every object is related to itself | required for equivalence relations and partial orders |
| Irreflexive | `$\nexists a \in A$ with `$a\,R\,a$ | no object is related to itself | the *opposite* of reflexive; `R` and `Rᶜ` cannot both be reflexive unless `A = ∅` |
| Symmetric | `$a\,R\,b \Rightarrow b\,R\,a$ | relatedness is mutual | required for equivalence relations |
| Antisymmetric | `$a\,R\,b \wedge b\,R\,a \Rightarrow a = b$ | mutual relatedness forces equality | required for partial orders; the *opposite* of symmetric |
| Transitive | `$a\,R\,b \wedge b\,R\,c \Rightarrow a\,R\,c$ | relatedness chains | required for equivalence relations and partial orders |
| Equivalence relation | `reflexive $\wedge$ symmetric $\wedge$ transitive` | behaves like `=` | `=`, `≡ mod n`, "same user id", connectivity |
| Equivalence class | `$[a] = \{b \in A : a \sim b\}$` | everything interchangeable with `a` | the blocks of the partition |
| Quotient set | `$A/{\sim} = \{[a] : a \in A\}$` | the set of classes | `DISTINCT` and `GROUP BY` return one row per class |
| Partition theorem | `$\{[a] : a \in A\}$` is a partition of `A` | classes are pairwise disjoint and cover `A` | every element is in **exactly one** class |
| Converse | `$a \sim b \iff a,b$ lie in the same block | each partition gives exactly one equivalence relation | equivalence relations and partitions are one object seen two ways |
| Representative set | `$\lvert R\rvert = \lvert A/{\sim}\rvert$`, each `a` equivalent to exactly one element of `R` | keep one member per class | the legitimacy of `set()`, `DISTINCT`, interning |
| Congruence | `$a \equiv b \pmod n \iff n \mid (a-b)$` | `a` and `b` leave the same remainder | exactly `n` classes on `ℤ`, namely `{a + kn : k ∈ ℤ}`; valid for `n ≥ 1` |
| Composition | `$R \circ S = \{(a,c) : \exists b,\ a\,S\,b \wedge b\,R\,c\}$` | relation-multiplication: two steps at once | reflexive and transitive if both are; need not be symmetric |
| Transitive closure | `$R^{*} = \bigcup_{k \ge 0} R^{k}$` | every pair joined by a chain | the repair that makes "reachable from" an equivalence |
| Components | `classes of `R^{*}`$` | exactly the connected components of the graph with edges `R` | the formal reason union–find solves connectivity |
| Partial order | `reflexive $\wedge$ antisymmetric $\wedge$ transitive | `<=`-shaped: a direction of strictness | sorting, topological order, the type hierarchy |
| Total order | partial order in which every two elements are comparable | `<` on a totally ordered set | `x <= y` on `{1,2,3,4}` is a total order |
| Bell number | `$B_n$` = number of partitions of an `n`-element set | how many equivalence structures exist on `A` | `B₁..B₇ = 1, 2, 5, 15, 52, 203, 877`; see [Lesson 28](../part02_discrete_combinatorics/28_counting_strategies.md) |
| Partitions of 4 by block count | `1, 7, 6, 1` for 1, 2, 3, 4 blocks | `15` in total | the worked example's table |
| Partitions of 6 by block count | `1, 31, 90, 65, 15, 1` for 1 … 6 blocks | `203` in total | what the code prints at `n = 6` |
| Symmetric-relation count | `$2^{C(n,2)}$` | each unordered pair is an edge or is not | `2^6 = 64` acquaintance patterns on 4 people; feasible for `n ≤ 5` |
| Degree argument | among `n+1` people two repeat a degree | the degrees can never be exactly `0, 1, …, n` | whoever knows nobody is known by nobody |
| Union–find | `find(x)` gives the class representative; `union(x,y)` merges | maintain the classes incrementally | path compression + union by rank gives `O(α(n))` amortised |
| Grouping key | `rows equivalent iff `tuple(row[k] for k in keys)` is equal | `GROUP BY` is an equivalence-class operation | the number of groups is the number of classes |

---

## Multiple Choice Questions

**Q1.** Let `A = {a, b, c, d}` and define `x ~ y` iff `|x − y| ≤ 2` in alphabet
order. Which statement is correct?

- A) It is an equivalence relation: it sounds symmetric, so symmetry is all that
  matters
- B) It is symmetric but not transitive — `a ~ c` and `c ~ d` hold while `a ≁ d`
- C) It is transitive but not symmetric
- D) It is irreflexive, so no equivalence class contains more than one element

<details>
<summary>Answer and explanation</summary>

**B) It is symmetric but not transitive — `a ~ c` and `c ~ d` hold while
`a ≁ d`.**

`a` is 2 from `c` and `c` is 1 from `d`, but `a` is 3 from `d`. Transitivity
fails, so the classes computed from it are not a partition. The lesson's code
prints `'within 2 letters' transitive? False ('ac' and 'cd' leave 'cd' 3 apart)`.

- A) is Mistake 1 of this lesson. The phrase *is* symmetric in the everyday
  sense, so you check symmetry, get a yes, and stop. Transitivity is the property
  people forget to test, because it is the one that requires three distinct
  elements and a chain.
- C) has the failure backwards. If `a ~ b` then `b ~ a`, since the distance is
  symmetric; `|x − y| = |y − x|` is immediate.
- D) confuses irreflexive with non-transitive. `a ~ a` holds (distance 0), so the
  relation is reflexive and every element is in at least its own class — the
  classes are just not disjoint.

</details>

**Q2.** Which of these relations on `A = {1, 2, 3, 4}` is an equivalence relation?

- A) `x ≤ y`
- B) `x + y = 6`
- C) `3 | (x − y)`
- D) `|x − y| = 1`

<details>
<summary>Answer and explanation</summary>

**C) `3 | (x − y)`.**

Reflexive: `0` is divisible by 3. Symmetric: `3 | (a−b) ⟹ 3 | (b−a)`.
Transitive: `3 | (a−b)` and `3 | (b−c) ⟹ 3 | (a−c)`. Its two classes are
`{1, 4}` and `{2, 3}` — the same "congruence mod 3" as the code's example on
`{0, …, 8}`, restricted to this set.

- A) is reflexive, antisymmetric and transitive — so it is a partial order, and
  indeed a total one. But it is not symmetric: `1 ≤ 4` while `4 ≰ 1`. That is
  exactly the direction of strictness that makes `<` useful for sorting.
- B) is symmetric and antisymmetric, but not reflexive: `1 + 1 = 2 ≠ 6`, so `1`
  is in no class at all — a partition must cover `A`.
- D) is symmetric but neither reflexive (`1 ≁ 1`) nor transitive (`1 ~ 2` and
  `2 ~ 3` while `1 ≁ 3`).

</details>

**Q3.** The partition theorem says the equivalence classes of an equivalence
relation on `A` form a partition. What does that rule out?

- A) Two classes sharing an element
- B) An element belonging to no class
- C) Two elements in the same class
- D) A class with exactly one element

<details>
<summary>Answer and explanation</summary>

**A) Two classes sharing an element.**

If `[a] ∩ [b] ≠ ∅`, pick `x` in the intersection. Then `a ~ x` and `b ~ x`, so `a
~ b` by symmetry and transitivity, hence `[a] = [b]` — they are the same class,
not two. The theorem's proof is that one sentence, and it is what makes
"collecting into a set" the correct way to compute classes in the code.

- B) is excluded too, by reflexivity: `a ∈ [a]`. But the *argument* is different
  — coverage comes from reflexivity, disjointness from symmetry plus
  transitivity — so option B is testing whether you know which property does
  which work.
- C) is the *point* of an equivalence relation. Everything inside a class is
  interchangeable by definition.
- D) is entirely legitimate: `20` distinct users is 20 classes of size 1, and the
  worked example's `u9` pair shows the other extreme.

</details>

**Q4.** How many equivalence classes does congruence mod 3 have on
`{0, 1, …, 8}`?

- A) 3
- B) 9
- C) 4
- D) 2

<details>
<summary>Answer and explanation</summary>

**A) 3.**

The classes are `{0, 3, 6}`, `{1, 4, 7}` and `{2, 5, 8}` — one per remainder. The
lesson's code prints exactly these three blocks and then
`number of classes = 3 = the modulus 3`. On `ℤ` there are `n` classes for modulus
`n`, since `ℤ/~` is the remainder ring.

- B) is `|A|` itself. It counts elements, not classes; the distinction is exactly
  what `DISTINCT` versus `GROUP BY` surfaces in a database.
- C) is the number of `n`-subsets of a 3-element set, which is unrelated. It is
  attractive only because 3 is the answer to a different question involving 3.
- D) is what you would get from grouping by `x mod 2` — a different modulus, a
  different relation, and a different partition. The class count is always the
  modulus.

</details>

**Q5.** Which relation on `{1, 2, 3, 4}` is a partial order?

- A) `x < y`
- B) `x ≤ y`
- C) `x + y = 6`
- D) `|x − y| = 1`

<details>
<summary>Answer and explanation</summary>

**B) `x ≤ y`.**

A partial order is reflexive, antisymmetric and transitive. For `≤` on a linearly
ordered set: `x ≤ x` holds; `x ≤ y` and `y ≤ x` force `x = y`; and `≤` chains.
Since every two elements are comparable it is in fact a **total** order, which is
the shape sorting and topological order need.

- A) is the same relation with the diagonal removed, and dropping the diagonal is
  fatal: a partial order must be reflexive. This is a common slip when someone
  writes a strict version of a real order and expects the same machinery to work.
- C) is symmetric, not reflexive, and not transitive (`1 ~ 5` and `5 ~ 1` while
  `1 ≁ 1`) — the opposite of a partial order.
- D) is symmetric, not reflexive, not transitive: it has all three wrong for a
  partial order and one right for an equivalence relation.

</details>

**Q6.** How many different partitions does a 4-element set have, and how does
that break down by number of blocks?

- A) 8: `2⁴`
- B) 15: 1 with one block, 7 with two, 6 with three, 1 with four
- C) 52: the same count for a 5-element set
- D) 64: 8 possible subsets

<details>
<summary>Answer and explanation</summary>

**B) 15: 1 with one block, 7 with two, 6 with three, 1 with four.**

This is `B₄`, the fourth Bell number. The lesson's worked example tabulates
exactly these figures and the code reproduces them for `n = 1, …, 7`:
`1, 2, 5, 15, 52, 203, 877`. The lesson makes the point that "group these 4
things" has more answers than you would guess by hand.

- A) is `2^|A|`, the number of subsets. Subsets are not partitions: a partition
  must have *disjoint, non-empty* blocks, and `{{1}, {1, 2}}` is a family of
  subsets that is not a partition at all.
- C) is `B₅`, one size up. It is the answer to "how many groupings of 5 things",
  and it is a common off-by-one when reading a table of Bell numbers.
- D) is `2^{C(4,2)}`, the number of undirected "knows" relations on 4 people —
  the count from the degree argument, a different object with a coincidentally
  equal value.

</details>

**Q7.** How many undirected "knows" relations are there on 4 people — that is,
how many ways can friendships be drawn among them?

- A) `2⁴ = 16`
- B) `2^{C(4,2)} = 2⁶ = 64`
- C) `4! = 24`
- D) `B₄ = 15`

<details>
<summary>Answer and explanation</summary>

**B) `2^{C(4,2)} = 2⁶ = 64`.**

There are `C(4,2) = 6` unordered pairs of people, and each is independently an
edge or is not — the product rule applied six times. The lesson's
`all_symmetric_relations` enumerates exactly `2^6 = 64` patterns for 4 labels and
prints the count.

- A) is `2^{|A|}`, the power-set count. It is the right answer for a different
  question — how many subsets of 4 people exist — and confusing the two is easy
  because both are powers of 2 with 4 in them.
- C) counts the orderings of 4 people, i.e. tournaments with an orientation on
  every pair. An undirected friendship relation has no orientation, so
  `4! = 24` is the count of *directed* complete relations, not undirected ones.
- D) is `B₄`, the number of ways to *group* 4 people, which quotients away
  information: 15 partitions collapse 64 relations. Each partition of `n` into `k`
  blocks corresponds to `k!` distinct relation patterns, so the count is not
  recoverable from the Bell number alone.

</details>

**Q8.** In an undirected graph, is "is reachable from `x` by a path" an
equivalence relation as usually defined?

- A) Yes — reachability is reflexive and symmetric and transitive, so the classes
  are the components
- B) No — it is reflexive and symmetric but **not** transitive; the transitive
  closure `R*` is what repairs it, and `R*`'s classes are the components
- C) No — it is symmetric but not reflexive, because you need at least one edge
- D) Yes, provided the graph is connected; otherwise it fails

<details>
<summary>Answer and explanation</summary>

**B) No — it is reflexive and symmetric but not transitive; the transitive closure
`R*` is what repairs it, and `R*`'s classes are the components.**

Take the lesson's own example: vertices 3 and 4 are adjacent, and 4 and 5 are
adjacent, so 3 and 5 are both "reachable from" 4 — but 3 and 5 are not connected
to each other directly, and reachability is defined by paths, not edges. The code
prints exactly this: `H: 'reachable from 0' is NOT transitive-safe without taking
the closure: 3 -> 4 and 4 -> 5, yet 3 and 0 are not equivalent`.

- A) is what the naive implementation assumes. It is the reason the lesson warns
  that the naive connectivity computation is `O(n³)` while union–find does it in
  near-linear time.
- C) confuses "reachable" with "adjacent". A vertex reaches itself by the
  length-zero path, so the relation is reflexive — which is exactly why `R*`
  automatically includes `(v, v)`.
- D) is a tempting half-truth. Connectivity is not the issue at all: `R*` is an
  equivalence relation whether or not the graph is connected, and when the graph
  is connected it has a single class.

</details>

**Q9.** The worked example has six records: `r1(u7,DE), r2(u3,US), r3(u7,DE),
r4(u9,JP), r5(u3,US), r6(u9,FR)`. What does "how many distinct users" report, and
what does "how many distinct countries" report?

- A) 4 users and 3 countries
- B) 3 users and 4 countries
- C) 3 users and 3 countries
- D) 4 users and 4 countries

<details>
<summary>Answer and explanation</summary>

**B) 3 users and 4 countries.**

The users are `{u7, u3, u9}` — note that `u9` appears on two records with
*different* countries, so it is one user. The countries are `{DE, US, JP, FR}`.
The lesson's code prints `distinct users (DISTINCT): ['u3', 'u7', 'u9']` and
`distinct countries: ['DE', 'FR', 'JP', 'US']`, and the worked example says so in
Step 6: "three distinct users, even though there are four distinct countries,
because `{r4, r6}` spans two countries."

- A) has the two swapped. It is the natural guess from reading the table's column
  order, and the reason the lesson insists on *computing* the classes rather than
  reading the columns.
- C) makes the same mistake in the other direction, treating a user as a
  (user, country) pair — which is Mistake 2 of this lesson: grouping by the key
  the report happens to display rather than the key the question asks for.
- D) double-counts on both sides, as if `u9/JP` and `u9/FR` were two users. That
  is exactly the grouping that produces the wrong partition, and it is a
  perfectly valid equivalence relation — just not the one the question wants.

</details>

**Q10.** Why does a Python `set` need equality and hashing to agree, and what
breaks when they do not?

- A) Nothing; `set()` uses `__eq__` alone, and `__hash__` is a performance
  optimisation
- B) A set stores objects by *hash bucket*, so equal objects must hash equally or
  the second insertion lands in a different bucket and the duplicate survives;
  mutating a key after insertion breaks it too
- C) `set()` preserves insertion order in Python 3.7+, so equality and hashing
  must agree for the ordering to be meaningful
- D) `__hash__` must be a prime, so objects whose hash changes fail an internal
  primality test

<details>
<summary>Answer and explanation</summary>

**B) A set stores objects by *hash bucket*, so equal objects must hash equally or
the second insertion lands in a different bucket and the duplicate survives;
mutating a key after insertion breaks it too.**

The correctness requirement for hashing is exactly that equal objects hash
equally — a relation that must be symmetric and consistent. If `x == y` but
`hash(x) ≠ hash(y)`, the set holds two entries it believes are different, so
deduplication silently fails and `len(s)` is wrong. The Python documentation says
so explicitly. Mistake 4 of this lesson is that this contract is invisible until
it breaks: `set()` works on almost everything, so the invariant is not something
you notice you are relying on.

- A) is the mistake in reverse. `__hash__` is not only performance — it is part
  of the *lookup* contract. A set is a hash table with a set interface.
- C) confuses `set` with `dict`. Plain `set` and `dict` preserve insertion order
  since Python 3.7, but that is an unrelated guarantee; ordering places no
  constraint on hashing.
- D) invents a requirement. Python truncates hashes to `Py_hash_t` and never
  requires primality; the only documented requirement is that equal objects hash
  equally, plus the warning about mutability.

</details>

---

## Subjective Questions

### Short Answer

**Q1. Define *reflexive*, *symmetric*, *antisymmetric* and *transitive* for a
relation `R` on `A`.**

<details>
<summary>Answer</summary>

- **Reflexive:** `a R a` for every `a ∈ A`.
- **Symmetric:** `a R b` implies `b R a`, for all `a, b`.
- **Antisymmetric:** `a R b` and `b R a` imply `a = b`, for all `a, b`.
- **Transitive:** `a R b` and `b R c` imply `a R c`, for all `a, b, c`.

Note that symmetric and antisymmetric are opposites: `≤` is antisymmetric and not
symmetric, `=` is both, and a relation can be neither (`x < y` on `ℝ`). Reflexive
is independent of all three — `x ≤ y` is reflexive, antisymmetric and transitive
but not symmetric.

</details>

**Q2. State the equivalence-relation theorem and the partition theorem, and say
what the partition theorem asserts.**

<details>
<summary>Answer</summary>

**Theorem.** `R` is an equivalence relation if and only if it is reflexive,
symmetric and transitive.

**Partition theorem.** If `~` is an equivalence relation on `A`, then the
equivalence classes `{[a] : a ∈ A}` form a **partition** of `A`: they are
pairwise disjoint, and their union is `A`.

Disjointness: if `[a] ∩ [b] ≠ ∅`, pick `x` in it. Then `a ~ x` and `b ~ x`, so
`a ~ b` by symmetry and transitivity, hence `[a] = [b]`. Coverage: `a ∈ [a]` by
reflexivity. So every element is in exactly one class.

</details>

**Q3. State the converse: what does every partition of `A` give you? Verify each
of the three properties.**

<details>
<summary>Answer</summary>

Every partition of `A` determines exactly one equivalence relation: `a ~ b` iff
`a` and `b` lie in the same block.

- **Reflexive**, because every block contains each of its elements, so `a` is in
  the same block as itself.
- **Symmetric**, because blocks are undirected: if `a` and `b` share a block then
  so do `b` and `a`.
- **Transitive**, because `a ~ b` and `b ~ c` put `a`, `b` and `c` in one block,
  so `a ~ c`.

This is the punchline: **equivalence relations and partitions are the same object
viewed two ways.** A partition is the grouping; the equivalence relation is the
test. Counting one counts the other.

</details>

**Q4. Prove that `a ≡ b (mod n)` is an equivalence relation on `ℤ`, and count its
classes.**

<details>
<summary>Answer</summary>

`a ≡ b (mod n)` means `n` divides `a − b`, for `n ≥ 1`.

- **Reflexive:** `n` divides `0`.
- **Symmetric:** `n | (a − b)` implies `n | −(a − b) = (b − a)`.
- **Transitive:** `n | (a − b)` and `n | (b − c)` imply `n | ((a − b) + (b − c))
  = (a − c)`.

The classes are `{a + kn : k ∈ ℤ}` — one per residue — so there are exactly `n` of
them. The lesson's code checks reflexivity, symmetry and transitivity explicitly
on `ℤ` restricted to `{0, …, 8}` and prints `number of classes = 3 = the modulus`.

</details>

**Q5. What is the composition of two relations, and which of the three properties
does it preserve?**

<details>
<summary>Answer</summary>

$$R \circ S = \{(a,c) : \exists b \text{ with } a\,S\,b \text{ and } b\,R\,c\}$$

Composition is relation-multiplication: "a relates to c by two steps". It is
**reflexive** and **transitive** if `R` and `S` are, but it need not be
**symmetric** — composing two symmetric relations can give an asymmetric one,
because `a R∘S b` via `z` and `b R∘S a` via `y` says nothing about each other
individually.

Taking the transitive closure — adding every pair connected by a chain — is what
repairs it, which is why `R*` rather than `R` is what defines connected
components.

</details>

**Q6. What are the Bell numbers, and how do the partitions of a 6-element set
break down by block count?**

<details>
<summary>Answer</summary>

The **Bell numbers** `B_n` count the partitions of an `n`-element set — that is,
the distinct equivalence structures on it. The lesson's code computes them by
recursively inserting the first element into an existing block or into a new one:

`B₁, …, B₇ = 1, 2, 5, 15, 52, 203, 877`.

For `n = 6` the breakdown by block count is 1 partition with 1 block, 31 with 2,
90 with 3, 65 with 4, 15 with 5, and 1 with 6 — totalling **203**. Counting these
is the subject of
[Lesson 28](../part02_discrete_combinatorics/28_counting_strategies.md).

</details>

### Long Answer

**Q1. Why must you take the transitive closure before "reachable from `x`" is an
equivalence relation? What exactly breaks if you use the raw edge relation?**

<details>
<summary>Model answer</summary>

Three properties are needed and the raw edge relation supplies only two. It is
reflexive only if you add the length-zero path, and it is symmetric only if the
graph is undirected; but transitivity fails for *any* graph with more than one
edge, in either direction. The lesson's counterexample is minimal: vertices 3 and
4 are adjacent and 4 and 5 are adjacent, so 3 and 5 are both reachable from 4,
yet they are in different components. In a directed graph even symmetry fails.

What breaks is not a small edge case — it is the whole algorithm. The
equivalence-class machinery the rest of this lesson provides assumes the relation
is an equivalence relation: that classes are disjoint, that they cover `A`, that
`[a] = [b]` iff `a ~ b`, and that one representative per class is a complete
description. With a non-transitive relation none of that holds. Classes computed
from the raw relation *overlap* — 4 appears in the class of 3 and in the class of
5 — so `len(classes)` no longer equals the number of components, `DISTINCT` no
longer returns one row per group, and any code that assumes "one representative
per class covers everything" is wrong. That is not a degraded result; it is a
wrong one.

The closure fixes it by construction. `R* = ⋃_{k≥0} Rᵏ` adds every pair joined by a
*chain*, so relatedness is automatically chained: if `a R* b` via a path of length
`j` and `b R* c` via a path of length `k`, then concatenating them is a path of
length `j + k`, so `a R* c`. Reflexivity comes from `k = 0`, the empty path, and
symmetry from reversing a path in an undirected graph. So `R*` is reflexive,
symmetric and transitive — an equivalence relation — and its classes are exactly
the connected components, by the definition of "in the same component".

The lesson's Mistake 5 is the engineering lesson attached to this. The naive
closure costs `O(n³)` with Floyd–Warshall and `O(nm)` with repeated BFS, and both
must emit at least `n²` bits of output. Union–find computes the classes in
`O(α(n))` per union without ever materialising the closure, because it maintains
the classes *incrementally* — merging two when an edge connects them — and the
classes are all you wanted. The closure was a means to an end; `find` and `union`
reach the end directly. This is why "is reachable from" appears in
[Lesson 26](../part02_discrete_combinatorics/26_graph_theory.md) as a relation
that "is reflexive and symmetric but not transitive — which is why you must take
the transitive closure before the classes are an equivalence".

</details>

**Q2. Why is the choice of equivalence relation a *modelling decision* rather
than a discovery? Use the worked example.**

<details>
<summary>Model answer</summary>

Because more than one equivalence relation can be true of the same data at the
same time, and they answer different questions. The worked example makes this
concrete: six records carrying `(user, country)`. Define `a ~ b` to mean "same
user id". Then the classes are `{r1, r3}`, `{r2, r5}` and `{r4, r6}`, and the
question "how many distinct users" has the answer 3.

Now define `a ~ b` to mean "same user *and* same country". This relation is
*also* reflexive, symmetric and transitive — it is also an equivalence relation,
and it also gives a clean partition. The difference is that `r4 (u9, JP)` and
`r6 (u9, FR)` are now in different blocks, because their countries differ. Both
relations are mathematically impeccable. Only one answers the question that was
asked.

That is why the lesson's Mistake 2 says "equivalence relations are chosen, not
discovered; the wrong key gives a perfectly valid partition of the wrong thing".
Nothing in the mathematics distinguishes them. The distinction is a statement
about what "the same" is *for*, which is a business decision. The lesson is blunt
about the consequence: "an equivalence relation is not automatically the one you
meant, and the choice of what counts as 'same' is a modelling decision with real
consequences."

This is exactly why SQL asks you to be explicit about which columns go in the
`GROUP BY`. `GROUP BY user` and `GROUP BY user, country` are both equivalence
relations, both partition the rows, both are implemented the same way — and they
return different numbers of groups. The engine cannot guess which you meant,
because both are defensible. The failure mode is silent: the query runs, returns
a plausible number, and the report is wrong in a way nobody notices until someone
audits it.

The transferable habit is to *state the key* before computing the classes, and to
say what question the key answers. In code that means naming the tuple you group
on. In prose it means writing "distinct users" rather than "distinct
user-country pairs". In both cases the cost of being explicit is one clause, and
the cost of being vague is a wrong answer with no error message.

</details>

**Q3. Why must a hashable type satisfy "equal objects hash equally"? What breaks
in each direction, and why is the contract invisible until it breaks?**

<details>
<summary>Model answer</summary>

Because a Python `set` is a hash table with a set interface. Lookup is not "scan
the list comparing with `==`"; it is "compute `hash(x)`, go to that bucket,
compare only what is in it". Soundness of that procedure needs the invariant:

$$x = y \ \Rightarrow\ \operatorname{hash}(x) = \operatorname{hash}(y)$$

which the documentation states explicitly. The two failure directions behave
differently and both are silent.

If equality and hashing *disagree*, a duplicate survives. Insert `x`, then insert
an equal `y`. The two land in different buckets, so the set believes it holds two
distinct objects. `len(s)` is now wrong, `x in s` still works for `x` but the
deduplication you relied on did not happen, and iteration yields both. The set's
documented guarantees — that its elements are pairwise distinct — are violated,
with no exception raised. This is the failure that reaches production: a type
whose `__eq__` ignores a field that `__hash__` includes, so two "equal" objects
hash differently.

If an object's hash *changes after insertion*, the set is silently corrupted. The
bucket index is computed at insertion time and stored; a later lookup computes the
*new* hash and visits a different bucket, so the object cannot be found even
though it is present. Iteration still shows it, so the object appears to be in the
set while `in` says otherwise. The Python documentation calls this out
explicitly, which is unusual and is a hint about how quietly it fails otherwise.

The contract is invisible until it breaks because `set()` works on almost
everything. Mutable objects cannot be dictionary keys or set members at all —
`TypeError: unhashable type` — so the worst case is caught. The dangerous case is
the one with no error: a type that *is* hashable and whose fields change after
insertion, or whose `__eq__` and `__hash__` were written inconsistently. Lesson 25
Mistake 4 puts it as "an invariant, not a feature", and the broader point is that
`==` and `hash` must describe the *same* equivalence relation — get one right and
the other and the data structure is broken while remaining a perfectly ordinary
Python object.

</details>

**Q4. Why does computing the transitive closure cost `O(n³)` while union–find
costs `O(α(n))`? What is each one actually computing?**

<details>
<summary>Model answer</summary>

They compute overlapping things, and the difference is *which* thing.

The transitive closure is a **materialised relation**: `R*` as an explicit subset
of `A × A`, with `(a, c)` present whenever a path of any length joins `a` to `c`.
That output alone is `Θ(n²)` pairs, so no algorithm can do better than `Ω(n²)`
time or space, whatever the input. Floyd–Warshall's `O(n³)` comes from its triple
loop over `(k, i, j)`, propagating "if `i` reaches `k` and `k` reaches `j`, then
`i` reaches `j`" once per intermediate vertex; the lesson's `warshall` function
implements exactly that, and a repeated-BFS variant costs `O(nm)`. When you
genuinely need the relation — to answer "can `a` reach `c`?" for arbitrary pairs
in one query — that cost is the honest one and you cannot dodge it.

Union–find computes something smaller: the **partition**, i.e. the list of
connected components. The lesson is explicit that this is all the classes you
wanted, and it is enough for the questions that matter: "are these two in the
same component?", "how many components are there?", "what are they?". It never
stores a pair of elements; it stores one integer per element, a parent pointer,
and path compression plus union by rank to keep trees shallow. Each `find` is
`O(α(n))` amortised — `α` is the inverse Ackermann function, which is below 5 for
every `n` that exists in practice — so `O(α(n))` per union, essentially constant.

The conceptual difference is what I want to underline: **the partition is a
sufficient statistic for connectivity queries, and the closure is not.** You can
answer every "same component?" question from 6 integers in the worked example's
six-vertex graph. You cannot answer them from `R` without closing it first. So
the right design is to decide which question you will actually ask. If you will
ask "same component?", maintain the components. If you will ask "what is the set
of vertices reachable from `a`?", you need `R*` — or, better, you need the
*transitive closure of one row*, which BFS computes in `O(V + E)` and which is
what the lesson's `bfs` actually returns along with the predecessor tree.

There is a cost to choosing the partition, and it is worth naming: union–find
does not support splitting. If a later edge *removes* connectivity, there is no
way to undo a `union`, and you would need a different data structure entirely. That
asymmetry is the price of the near-constant amortised bound, and it is exactly
why Kruskal's minimum-spanning-tree algorithm in
[Lesson 27](../part02_discrete_combinatorics/27_trees_and_spanning_trees.md) can
use it: it only ever adds edges.

</details>

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
  [Lesson 26](../part02_discrete_combinatorics/26_graph_theory.md).
- Union–find maintains the classes incrementally in O(α(n)) amortised time, and
  choosing the *right* key is a modelling decision with visible consequences.

## Next

[Lesson 26 — Graph Theory](../part02_discrete_combinatorics/26_graph_theory.md) assumes you know what an
equivalence relation and a partition are, and that "connected by a path" is a
relation you may need to close; it turns that into the language of vertices,
degrees, connectivity, and planar graphs.