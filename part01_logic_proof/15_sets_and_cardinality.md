# 15 — Sets and Cardinality

**Part**: part01_logic_proof · **Prerequisites**: 10, 11, 12 · **Time**: 30 min

---

## In Plain Words

A set is a collection of things in which nothing is counted twice and the order
does not matter, so two lists that hold the same things are one thing described
twice rather than two things. That single idea gives you the questions a
programmer asks all day: which of these things are in both collections, which
are in only one, is this list of allowed things contained in the list of things
a user actually has, and how many things are in the result. The last question is
the dangerous one, because merging two collections that overlap is where the
counting goes wrong. And the biggest surprise is that collections do not all
have the same size: the counting numbers, the negative numbers, the fractions,
and even pairs of counting numbers all turn out to be exactly as big as each
other, while the numbers on a measuring line are strictly bigger than all of
them, with no largest size to describe.

## Why Computer Science Cares

**Python's `set` and `frozenset` are this lesson's two data structures.**
`set` is a mutable collection with duplicates removed and membership by hash, so
`x in s` is expected constant time rather than linear. `frozenset` is the
immutable version, and it exists for one set-theoretic reason: an immutable
object has a stable hash value, so it can be a key in a `dict` or an element of
another `set`. `{1, 2}` cannot be a dict key; `frozenset({1, 2})` can. The
difference is not a style choice, it is the difference between a value that can
be compared for equality repeatedly and one that can be looked up.

**The cost of `in` is a set fact, not an implementation detail.** With $n$ keys
in $m$ buckets the expected chain length is $n/m$, which is why a hash set is
expected $O(1)$ per lookup while a Python `list` is $O(n)$ — the list has no
hash, so there is nowhere to jump to. The pigeonhole principle is the reason
that bound is an *expectation*: $n$ keys in $m$ buckets with $n > m$ forces some
bucket to hold at least $\lceil n/m \rceil$ keys, and an adversary who knows the
hash function can push every key into one. See
[Lesson 23](../part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md)
for the pigeonhole principle itself.

**A subset is an n-bit string.** In C, a 32-bit permission word is a set of 32
features; `flags & required == required` is the subset test and takes one
instruction. This is not a trick that happens to work — a subset of an
$n$-element set has exactly $2^n$ members, so a 20-element set has 1,048,576
subsets, and a 20-bit word names any one of them in a single register while
testing any subset relation in a single instruction. Feature selection is a
search over that power set, which is why it is a research problem and not a loop
somebody forgot to finish.

**Relational algebra is set algebra with the guarantees removed.** A database
table without a primary key is a *bag*: the same value can appear twice.
`SELECT DISTINCT` is the step that turns a bag into a set, and `UNION` versus
`UNION ALL` is exactly the difference between set union and bag union.
`|A ∪ B| = |A| + |B| − |A ∩ B|` is a theorem about sets, and using it on bags is
a bug that produces a report saying there were six users in a table with four
rows. Joins differ in cardinality for the same reason: a semi-join uses the
right-hand table as a set and returns each matching left row once, while an
inner join emits one row per matching pair.

**Type systems, unification and data types are sets of possible values.** A
variable of type `T` ranges over a set; subtyping is subset inclusion;
`Hash`/`Eq` requirements in Rust, `HashSet<T>`/`BTreeSet<T>`, and the
`frozenset` in Python are all the same requirement — *a value whose equality can
be decided cheaply, so that a collection of them can be indexed*.

## The Formal Version

The symbols below are the ones listed in [SYMBOLS.md](../SYMBOLS.md).

**Definition.** A *set* $A$ is a collection of distinct objects with no order
and no repetition. Two sets are equal when they have exactly the same elements:
`$A = B$` iff `$\forall x,\; (x \in A \Leftrightarrow x \in B)$`. That sentence is
the definition of set equality, and it is what makes `{a, b, a}` and `{b, a}`
the same object.

**Definition.** `x ∈ A` reads "$x$ is an element of $A$"; `x ∉ A` is its
negation. A *singleton* is a set with exactly one member, written `$\{x\}$`.

**Definition.** `A ⊆ B` ($A$ is a *subset* of $B$) iff `$\forall x \in A,\;
x \in B$`. `A ⊂ B` ($A$ is a *proper subset*) iff `A ⊆ B` **and** `$A \neq B$`.

*Note on the symbol.* `⊂` is used for "proper subset" throughout this lesson and
in [SYMBOLS.md](../SYMBOLS.md). Some texts use it for "subset, possibly equal" —
which is written `⊆` here. Always check which one a text means, because the
difference is the whole content of the definition.

**Definition.** The *empty set* `∅` has no elements. `$∅ ⊆ A$` for every set
$A$, and `$|∅| = 0`.

**Definition.** For sets $A$ and $B$:
`$A \cup B = \{x : x \in A \text{ or } x \in B\}$` (union),
`$A \cap B = \{x : x \in A \text{ and } x \in B\}$` (intersection),
`$A \setminus B = \{x : x \in A \text{ and } x \notin B\}$` (difference),
`$A \Delta B = (A \setminus B) \cup (B \setminus A)$` (symmetric difference, the
elements in exactly one of the two).

**Definition.** Given a fixed *universal set* $U$, the *complement* of $A$ is
`$A^c = U \setminus A$`. The complement is meaningless without naming $U$: the
complement of "even integers" with respect to the integers is the odd
integers, and with respect to the natural numbers it is different again.

**Definition.** Two sets are *disjoint* iff `$A \cap B = ∅$`. A *partition* of
$A$ is a collection of pairwise disjoint non-empty subsets whose union is $A$.

**Definition.** The *power set* of $A$ is `$\mathcal{P}(A) = \{B : B \subseteq A\}$`,
the set of all subsets of $A$. Note that $A$ and $∅$ are both members of
`$\mathcal{P}(A)$`, so `$\emptyset \in \mathcal{P}(A)$` while
`$\emptyset \notin A$` in general.

**Definition.** $|A|$, the *cardinality* of $A$, is the number of elements in
$A$ — meaningful for finite sets. `$|A| = n$` is also written `$n$`-element set.

**Definition.** A family `$\mathcal{F} \subseteq \mathcal{P}(A)$` in which no
member contains another is an *antichain*. `$A, B \in \mathcal{F}$` and
`$A \subsetneq B$` never both hold.

**Theorem.** `$|\mathcal{P}(A)| = 2^{|A|}$`.

*Proof.* Put `$n = |A|$` and write `$A = \{a_1, \ldots, a_n\}$`. A subset $S$ of
$A$ is determined by, for each $i$, whether $a_i$ belongs to it — an independent
yes/no for each of the $n$ elements. So the map
`$\Phi : \mathcal{P}(A) \to \{0,1\}^n$` given by
`$\Phi(S) = (\mathbb{1}_{a_1 \in S}, \ldots, \mathbb{1}_{a_n \in S})$` is a
bijection, and a length-$n$ binary string has $2^n$ values. ∎

*Why the proof is worth having.* It is a bijection, so nothing is lost and
nothing is invented — not an upper bound. That is the difference between "there
are at most $2^n$ subsets" (which would follow from a weaker argument) and
"$|\mathcal{P}(A)| = 2^n$". The same identity also follows by induction on $n$,
splitting the subsets into those containing a fixed element and those not; see
[Lesson 14](14_mathematical_induction.md), whose worked example is exactly this
theorem.

*Domain note.* `$|\mathcal{P}(A)| = 2^{|A|}$` is a statement about finite $A$ as
written, and it is the reason the theorem "no set is the largest" needs a
different notation for infinite sets. For infinite $A$ the power set is still
strictly larger, but $2^{|A|}$ is not a natural number — see Cantor's theorem
below.

**Theorem.** `$|A \cup B| = |A| + |B| - |A \cap B|$`.

*Proof.* $A \cup B$ splits into three disjoint pieces: `$A \cap B$`, `$A \setminus B$`
and `$B \setminus A$`. Also `$|A| = |A \cap B| + |A \setminus B|$` and
`$|B| = |A \cap B| + |B \setminus A|$`. Adding the last two gives
`$|A| + |B| = 2|A \cap B| + |A \setminus B| + |B \setminus A|`, and substituting
into the first gives the result. ∎

**Corollary.** `$|A \cup B| = |A| + |B|$` **iff** `$A \cap B = ∅$`. So adding
sizes is right exactly when the two sets share nothing, and the general formula
is that formula with the double count removed.

**Theorem.** `$|A \times B| = |A| \cdot |B|$, where `$A \times B$` is the set of
ordered pairs. The pairs are all distinct, so the count is a product and not a
sum. For three sets, `$|A \times B \times C| = |A||B||C|`.

**Theorem.** *Inclusion–exclusion, three sets.*

$$|A \cup B \cup C| = |A| + |B| + |C| - |A \cap B| - |A \cap C| - |B \cap C| + |A \cap B \cap C|$$

*Explanation.* Every element of $A \cup B \cup C$ belongs to exactly one, two or
three of the three sets, and must be counted once. An element in exactly one set
is never subtracted. An element in exactly two is added twice and subtracted
once. An element in all three is added three times, subtracted three times, and
added back once. Each case lands on one. Part 02
([Lesson 23](../part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md))
does the general version with $k$ sets.

**Theorem.** *(Sperner's theorem.)* If `$A$` has $n$ elements and
`$\mathcal{F} \subseteq \mathcal{P}(A)$` is an antichain, then

$$|\mathcal{F}| \le \binom{n}{\lfloor n/2 \rfloor}$$

and the bound is attained by taking every subset of size `$\lfloor n/2 \rfloor$`.

*Proof sketch, by double counting.* $A$ has $n!$ maximal chains
`$\emptyset \subset \{a_1\} \subset \cdots \subset A$`. A subset $S$ of size $k$
lies on exactly `$k!(n-k)!$` of them. No chain meets two members of
$\mathcal{F}$, because two subsets on one chain are comparable. Counting
(chain, member-of-$\mathcal{F}$-on-it) pairs two ways gives

$$\sum_{S \in \mathcal{F}} \frac{1}{\binom{n}{|S|}} \le 1$$

and every summand is at least `$1/\binom{n}{\lfloor n/2\rfloor}$` because the
binomial coefficients peak in the middle. Hence `$\binom{n}{\lfloor n/2
\rfloor} |\mathcal{F}| \le 1$`. ∎

*Why it matters in computing.* A family of feature-flag configurations in which
no configuration's flags contain another's is an antichain, so a system with
$n$ flags admits at most `$\binom{n}{\lfloor n/2\rfloor}$` mutually
independent test configurations — about `$2^n / \sqrt{n}$`, not `$2^n$`. The
same bound is the standard route to monotone boolean circuit lower bounds,
because a monotone function is the characteristic function of an antichain (the
minimal true inputs).

**Definition.** A function `$f : A \to B$` is an *injection* iff
`$f(a) = f(b)` implies `$a = b$`, and a *bijection* iff it is an injection and
onto. Two sets have the same cardinality when a bijection exists between them;
for infinite sets, that bijection — not a count — is the evidence.

**Definition.** A set is *countably infinite* if a bijection with
`$\mathbb{N}$` exists. `$\mathbb{Z}$`, `$\mathbb{Q}$`, and `$\mathbb{N} \times
\mathbb{N}$` are countably infinite. The number is written `$\aleph_0$`.

**Theorem.** `$|\mathbb{N}| = |\mathbb{Z}| = |\mathbb{Q}| = |\mathbb{N} \times \mathbb{N}| = \aleph_0$`.

*Explanation, with the bijections.* `$\mathbb{N} \to \mathbb{Z}$` by the zigzag
`$0 \mapsto 0,\; 1 \mapsto -1,\; 2 \mapsto 1,\; 3 \mapsto -2, \dots$`.
`$\mathbb{N} \times \mathbb{N} \to \mathbb{N}$` by the Cantor pairing function
`$\pi(a, b) = \tfrac{(a+b)(a+b+1)}{2} + b$`, which lays the pairs out on the
diagonals of constant `$a + b$` and numbers the diagonals in turn.
`$\mathbb{N} \to \mathbb{Q}$` by the same diagonal enumeration, keeping the
pairs in lowest terms and dropping duplicates; every rational `$p/q$` with
`$q > 0$` appears at a finite index. All three are verified by round trip in the
Runnable Code.

**Theorem.** *(Cantor's diagonal argument.)* For every set $A$, `$|\mathcal{P}(A)| > |A|$`.

*Proof.* Suppose `$A$` could be listed: `$A = \{a_0, a_1, a_2, \ldots\}$` with
every element appearing. For each $n$ let `$S_n = \{a_n\} \subseteq A$, so the
sets `$S_n$ are all members of `$\mathcal{P}(A)$`. Define
`$D = \{a_n : a_n \notin S_n\} = \{a_n : a_n \ne a_n\}$` — precisely, `$D$ contains
`$a_n$` exactly when `$S_n$` does not. If `$D$ were some `$S_k$`, then `$a_k`
would be in `$D$` exactly when it is in `$S_k$`, and by construction `$a_k$` is
in `$D$` exactly when it is *not* in `$S_k$`. Contradiction, so `$D` is a
subset of $A$ that the list omits. ∎

*What follows.* `$|\mathcal{P}(\mathcal{P}(A))| > |\mathcal{P}(A)| > |A| > \dots$`,
so there is no largest set, and no way to write "the set of everything" in
finite notation. In particular `$|\mathbb{R}| > |\mathbb{N}|$: every real
determines the set of rationals below it, an injection `$\mathbb{R} \to
\mathcal{P}(\mathbb{Q})`, and `$\mathcal{P}(\mathbb{Q})$` is not countable by
the diagonal argument.

**Theorem.** `$|\mathbb{R} \times \mathbb{R}| = |\mathbb{R}|`, and also
`$|\mathbb{R}^n| = |\mathbb{R}|$` for every finite $n \ge 1$.

*Explanation.* A point of `$\mathbb{R}^2$` is two infinite digit strings; a
point of `$\mathbb{R}$` is one; interleave them to get one string, and
de-interleave to get two. That is the space-filling curve: a single continuous
path that passes through every point of the square, which sounds impossible and
is not, because the curve is infinitely long and hits a positive-area region
only in the limit of finer and finer scales.

*One warning, because this is the most commonly misremembered fact in the
lesson.* The statement is about **reals**:
`$|\mathbb{R} \times \mathbb{R}| = |\mathbb{R}|`. It is **not**
`$|\mathbb{N} \times \mathbb{N}| = |\mathbb{R}|`, and that is false:
`$\mathbb{N} \times \mathbb{N}$` is countable (Cantor pairing) and
`$\mathbb{R}$` is not. The interleaving argument works on the reals precisely
because their digit strings are *uncountably* long; applied to the naturals it
gives `$\aleph_0 = \aleph_0$`, which is true but is not the same fact. Also
mind the representation: in binary `$0.1000\ldots = 0.0111\ldots$`, so a naive
injection is not injective on the corner cases. Use base 4 with digits restricted
to $\{0,1\}$, or fix the convention "the representation that does not end in all
1s", which every number has exactly one of.

**Theorem.** *(Cantor–Schröder–Bernstein.)* If there is an injection
`$A \to B$` and an injection `$B \to A$`, then `$|A| = |B|$`.

*Explanation.* You do not have to write down the bijection; the proof builds one
from the two injections by splitting each in two and patching the halves. The
built object is ugly and nobody ever wants to read it, which is the entire
reason the theorem is worth having.

*Where it has content.* For **finite** sets the theorem says nothing: an
injection `$A \to B$` gives `$|A| \le |B|` by counting, swapping `$A$` and `$B$`
gives the reverse, so they are equal and no bijection is required. The theorem
only earns its keep for **infinite** sets, where counting is unavailable. Its
classic application is `$|\mathbb{R}| = |\mathcal{P}(\mathbb{Q})|$: the
injection `$\mathbb{R} \to \mathcal{P}(\mathbb{Q})$` sends a real to the rationals
below it, and the injection `$\mathcal{P}(\mathbb{Q}) \to \mathbb{R}$` sends a set
of rationals to the real whose ternary expansion has a 1 wherever the rational
is present. Both are easy, the bijection is not, and the theorem supplies it.

**Theorem.** *(The pigeonhole connection, stated once.)* If `$A$` is divided
into $m$ classes and `$|A| > m \cdot k$ for some integer `k \ge 1`, then some
class contains at least `$k + 1$` elements.

*Explanation.* The "classes" need not be sets you named — in a hash table the
class of an element is the bucket its hash lands in. With $n$ keys in $m$
buckets some bucket holds at least `$\lceil n/m \rceil` keys, which is why hash
membership is expected `$O(1)$` rather than guaranteed. The full proof, with the
general form and the counting formula, is
[Lesson 23](../part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md);
this lesson needs only the statement.

*Why a set-theoretic fact and a runtime property are the same fact.* `x in s`
for a Python `set` is a question of the form "$x \in A$?", and its cost is the
cost of answering one such question in the data structure that holds $A$. When
the answer is yes-or-no against a hashed container the cost is constant on
average; against a list it is linear, because a list cannot answer the question
without comparison against every member. Nothing about the mathematics changed
between the two cases. The container did.

## Formula Sheet

Cardinality is written `\lvert A \rvert` inside the table below, because a bare
`|` would be read as a column separator. Outside tables it is written `|A|`, and
both mean the same thing.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$A = B$` | `$\forall x,\; (x \in A \Leftrightarrow x \in B)$` | same elements, whatever order they were written in | deciding whether two collections are the same collection |
| `x ∈ A` | `$x \in A$` | x is one of the members of A | membership tests, the basis of `in` |
| `$A \subseteq B$` | `$\forall x \in A,\; x \in B$` | every member of A is a member of B | permissions, feature coverage, "does this requirement fit" |
| `$A \subsetneq B$` | `$A \subseteq B \wedge A \neq B$` | every member of A is in B, **and** they are not the same | distinguishing "fits" from "is exactly" |
| `$∅ \subseteq A$` | always true | the empty collection is inside everything | edge case in every subset loop: `⊆` holds, `⊂` needs `$A \neq ∅$` |
| `$A \cup B$` | `$\{x : x \in A \vee x \in B\}$` | everything in either, counting shared members once | `DISTINCT`, `UNION`, "all the tags we have seen" |
| `$A \cap B$` | `$\{x : x \in A \wedge x \in B\}$` | only what is in both | inner join, "which countries have both users and leads" |
| `$A \setminus B$` | `$\{x : x \in A \wedge x \notin B\}$` | what is in A and not in B | "what can this candidate drop", `EXCEPT`, revoked permissions |
| `$A \Delta B$` | `(A \setminus B) \cup (B \setminus A)` | in exactly one of the two | symmetric difference, "what changed between two versions" |
| `$A^c$` | `$U \setminus A$` | everything in U that is not in A | **needs a stated universal set U**; means different things for different U |
| `$\lvert A \rvert$` | `$\lvert A \rvert$` | how many members | every cardinality argument |
| `$\mathcal{P}(A)$` | `$\{B : B \subseteq A\}$` | the set of all subsets of A | feature selection, bitmasks, monotone circuits |
| `$\lvert \mathcal{P}(A) \rvert$` | `$2^{\lvert A \rvert}$` | twice one for every element | sizing the configuration space; $n = 32$ gives 4.3 billion |
| `$A \cup B$`, size | `$\lvert A \cup B \rvert = \lvert A \rvert + \lvert B \rvert - \lvert A \cap B \rvert$` | add the sizes, subtract what was counted twice | merging two overlapping collections |
| disjoint | `$A \cap B = ∅$` | no shared members | the case where `$\lvert A \cup B \rvert = \lvert A \rvert + \lvert B \rvert$` is exact |
| `$A \cup B \cup C$`, size | `$\sum \lvert A \rvert - \sum \lvert A \cap B \rvert + \lvert A \cap B \cap C \rvert$` | three-way version of the same correction | three-way dedup, three-way overlap reporting |
| `$A \times B$`, size | `$\lvert A \times B \rvert = \lvert A \rvert \cdot \lvert B \rvert$` | one element for each ordered pair | join fan-out, matrices of combinations |
| `$A^3$`, size | `$\lvert A \times A \times A \rvert = \lvert A \rvert^3$` | one element per ordered triple | three-way joins |
| antichain | `$\mathcal{F} \subseteq \mathcal{P}(A)$, no member contains another` | a family of subsets, none inside another | independent tests, minimal true inputs of a monotone function |
| Sperner's bound | `$\lvert \mathcal{F} \rvert \le \binom{n}{\lfloor n/2 \rfloor} \approx 2^n / \sqrt{n}$` | at most this many mutually incomparable subsets | **valid for any** $n$; the middle layer attains it |
| binom | `$\binom{n}{k} = \frac{n!}{k!\,(n-k)!}$` | ways to choose $k$ of $n$ items, order irrelevant | sizes of the layers of the power set |
| countably infinite | `$\aleph_0$` | the same size as N, via a bijection with N | Z, Q and N × N all have this size |
| pairing function | `$\pi(a,b) = \frac{(a+b)(a+b+1)}{2} + b$` | a bijection from pairs of naturals to naturals | the proof that `$\lvert \mathbb{N} \times \mathbb{N} \rvert = \lvert \mathbb{N} \rvert$` |
| Cantor diagonal | `$D = \{a_n : a_n \notin S_n\}$` where `$S_n = \{a_n\}$` | the subset that every proposed list misses | the proof that `$\lvert \mathcal{P}(A) \rvert > \lvert A \rvert$` |
| Cantor–Schröder–Bernstein | injections `$A \to B$` and `$B \to A$` imply `$A = B$` in size | equal size without constructing the bijection | infinite sets; says nothing new for finite ones |
| digit interleaving | `$\lvert \mathbb{R}^n \rvert = \lvert \mathbb{R} \rvert$` | $n$ infinite digit strings fit in one | space-filling curves; **not** `$\lvert \mathbb{N} \times \mathbb{N} \rvert = \lvert \mathbb{R} \rvert$` |

## Worked Example

Three release candidates of a service are being compared. You have a log of every
endpoint each candidate hit, and you must answer four questions for the release
dashboard. The numbers below are the real output of the code in Exercise 1, and
every intermediate step is shown, because the whole point of this example is the
two arithmetic mistakes rather than the final number.

**The problem, in English.**

- Candidate 1 hit `$A$`: the login, cart, search and health endpoints.
- Candidate 2 hit `$B$`: search, profile, health, metrics and cart.
- Candidate 3 hit `$C$`: health, metrics and login.

Report: (a) how many distinct endpoints were hit by anybody; (b) how many were
hit by all three; (c) which endpoints can candidate 2 stop using without
affecting the other two; (d) how many flag configurations does the release
train have?

**Step 1. Write the sets down, and count them.**

$$A = \{\texttt{/login}, \texttt{/cart}, \texttt{/search}, \texttt{/health}\}, \quad |A| = 4$$
$$B = \{\texttt{/search}, \texttt{/profile}, \texttt{/health}, \texttt{/metrics}, \texttt{/cart}\}, \quad |B| = 5$$
$$C = \{\texttt{/health}, \texttt{/metrics}, \texttt{/login}\}, \quad |C| = 3$$

Sum of the sizes: `$4 + 5 + 3 = 12$`. There are six endpoints in the world that
these three candidates touch, so **12 is wrong** — and this is the answer a
dashboard gives if it adds the row counts together, which it usually does.

**Step 2. Find the double counts.** List the intersections explicitly rather
than assuming the size:

| Intersection | Members | Size |
| --- | --- | --- |
| `$A \cap B$` | `/cart`, `/health`, `/search` | 3 |
| `$A \cap C$` | `/health`, `/login` | 2 |
| `$B \cap C$` | `/health`, `/metrics` | 2 |
| `$A \cap B \cap C$` | `/health` | 1 |

Two things to notice. `/health` is in all three sets, so it gets subtracted
**three** times in step 3 and has to be added back. And the pairwise
intersections are not disjoint: `/health` appears in all three of them, which is
why you cannot simply add the three pairwise sizes and expect a correction.

**Step 3. Apply inclusion–exclusion.**

$$|A \cup B \cup C| = 4 + 5 + 3 - 3 - 2 - 2 + 1 = 6$$

Check against the union written out:

$$A \cup B \cup C = \{\texttt{/cart}, \texttt{/health}, \texttt{/login}, \texttt{/metrics}, \texttt{/profile}, \texttt{/search}\}$$

Six elements. The formula agrees.

**Step 4. Understand why the `+1` is there, by following one element.**
`/health` is in $A$, in $B$ and in $C$. Start at +3 from the raw sum. It is in
$A \cap B$, $A \cap C$ and $B \cap C$, so it is subtracted three times: +3 − 3 =
0. It has now fallen off the end, which is why the triple term `+|A ∩ B ∩ C|`
puts it back exactly once. Every other element behaves the same way:

- `/cart` is in $A$ and $B$: +2, subtracted once in `$A ∩ B$` only: 2 − 1 = 1. ✓
- `/login` is in $A$ and $C$: +2 − 1 = 1. ✓
- `/metrics` is in $B$ and $C$: +2 − 1 = 1. ✓
- `/search` is in $A$ and $B$: +2 − 1 = 1. ✓
- `/profile` is in $B$ only: +1, never subtracted. ✓
- `/health` is in all three: +3 − 3 + 1 = 1. ✓

Six elements, each counted once. That table *is* the proof of
inclusion–exclusion, and it is worth doing by hand once, because the formula is
otherwise something you apply and then hope.

**Step 5. The near-miss.** Suppose you remember the correction but forget the
triple term: `$12 - 3 - 2 - 2 = 5$`. Five is wrong, and it is wrong in the
interesting direction: it is one *too small*, so the dashboard under-reports
shared dependencies rather than inventing them. The second-order mistake
`$|A| + |B| + |C| = 12$` is twice too big. Both are plausible-looking integers,
which is what makes them dangerous; a report saying "13 endpoints" gets a
question, a report saying "6" does not.

**Step 6. Answer (b): the shared dependency.** `$A \cap B \cap C = \{/health\}`,
size 1. One endpoint is on every candidate's critical path. That is the number
that decides whether removing `/health` requires coordinating all three
releases, and it is a *triple* intersection, not a pairwise one — pairwise
intersections have size 3, 2 and 2 and none of them is the right answer.

**Step 7. Answer (c): what candidate 2 can drop.** "Endpoints of `$B$` that no
other candidate touches" is a difference, `$B \setminus (A \cup C)$`:

| Candidate | Its own endpoints nothing else uses | Count |
| --- | --- | --- |
| `$A \setminus (B \cup C)$` | `∅` | 0 |
| `$B \setminus (A \cup C)$` | `{ /profile }` | 1 |
| `$C \setminus (A \cup B)$` | `∅` | 0 |

So candidate 2 can stop calling `/profile`; candidates 1 and 3 cannot drop
anything at all. Note the shape of the computation: `$A \setminus (B \cup C)$`
can be read as `$(A - B) - C`, and those two are equal **always** — removing the
union removes everything in $B$ or in $C$, and removing $B$ and then $C$ removes
exactly the same elements. What is *not* equal is `$A \cap (B \cup C)$` and
`$(A \cap B) \cap C`: intersection distributes over union the other way round,
as `$A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$`. That second pair is the
one people get backwards, because the two look like the same operation with the
brackets moved.

**Step 8. Answer (d): the flag configurations.** The release train carries
feature flags for TLS termination, caching, retry, shadow traffic and a beta
path — five booleans, so `$|\mathcal{P}(\{\text{five flags}\})| = 2^5 = 32$`
configurations. Multiply by the number of test environments and you have the
number of test runs a naive "run every combination" strategy implies. At six
flags it is 64; at twenty it is 1,048,576; at thirty-two it is 4.3 billion.
This is the same $2^n$ as the power set, and it is the reason exhaustive
configuration testing is a research decision rather than a default.

**Step 9. What this example is really about.** Four questions, four different set
operations: union with a three-set correction, triple intersection, difference,
and power-set counting. No arithmetic beyond counting. That is the shape of most
real set problems — the operations do the work, and the only arithmetic is the
double-count correction.

## Runnable Code

Four blocks. The first two are the finite part — set operations, the cardinality
arithmetic, and the power set as bit masks. The third is the infinite part,
where the only possible method is to build an explicit rule and check that it
round-trips. The fourth is the same mathematics applied to code people actually
write: an access check, a dedup loop, and a join.

Everything below is standard library only and runs as written.

### 1. Set operations, and the double-count correction

```python
from itertools import combinations, chain

# ---------------------------------------------------------------------------
# A set is a collection with two properties: no duplicates, and no order.
# Two different constructions that end up with the same elements are the SAME
# set. Everything below is a consequence of that one sentence.
# ---------------------------------------------------------------------------

MONDAY = {"/login", "/search", "/cart", "/checkout", "/health"}
TUESDAY = {"/search", "/cart", "/profile", "/health"}

print("=" * 76)
print("1. A set is determined by its elements, not by how you built it")
print("=" * 76)
print(f"  built in one literal     : {sorted(MONDAY)}")
print(f"  built from a list w/ dupes: {sorted({'/login', '/search', '/cart', '/login'})}")
print()
print(f"  3 list items, 2 of them equal, become {len({'/login', '/login', '/search'})} set elements")
print(f"  order is irrelevant      : {MONDAY == {'/health', '/cart', '/checkout', '/login', '/search'}}")
print(f"  equal lengths, equal sets: {len(MONDAY) == 5} and {MONDAY == {'/login', '/search', '/cart', '/checkout', '/health'}}")
print()
print("  `set` is mutable, so Python refuses to hash it. `frozenset` is the")
print("  immutable version, and immutability is exactly what makes a value")
print("  usable as a dict key or as an element of another set.")
print(f"  {{frozenset({{1,2}}): 'a key'}} -> { {frozenset({1, 2}): 'a key'} }")
print(f"  a plain set is not hashable: {hasattr(set(), '__hash__') and set.__hash__ is None}")
print(f"  frozenset is hashable     : {frozenset({1, 2}) in {frozenset({1, 2}), frozenset({3})}}")

print()
print("=" * 76)
print("2. The cardinality of a union, and where double counting comes from")
print("=" * 76)
print(f"  A (Monday)   = {sorted(MONDAY)}")
print(f"                 |A| = {len(MONDAY)}")
print(f"  B (Tuesday)  = {sorted(TUESDAY)}")
print(f"                 |B| = {len(TUESDAY)}")
print()
print(f"  A & B        = {sorted(MONDAY & TUESDAY)}")
print(f"                 |A and B| = {len(MONDAY & TUESDAY)}")
print(f"  A | B        = {sorted(MONDAY | TUESDAY)}")
print(f"                 |A or B| = {len(MONDAY | TUESDAY)}")
print()
na, nb, nab = len(MONDAY), len(TUESDAY), len(MONDAY & TUESDAY)
print(f"  |A| + |B|                = {na} + {nb} = {na + nb}   <- WRONG, too big")
print(f"  |A| + |B| - |A and B|    = {na} + {nb} - {nab} = {na + nb - nab}  <- the real size of A or B")
print()
print(f"  A - B        = {sorted(MONDAY - TUESDAY)}")
print(f"  B - A        = {sorted(TUESDAY - MONDAY)}")
print(f"  A ^ B        = {sorted(MONDAY ^ TUESDAY)}   (in exactly one of the two)")
print()
print(f"  the three endpoint names counted twice, and only twice: "
      f"{sorted(MONDAY & TUESDAY)}")
print(f"  9 - 3 = {9 - 3}, which is why the count comes out six and not nine.")

print()
print("=" * 76)
print("3. |A or B| = |A| + |B| exactly when the two sets share nothing")
print("=" * 76)
print(f"  {'A':<26} {'B':<26} {'|A|':>4} {'|B|':>4} {'shared':>7} {'sum':>5} "
      f"{'|A or B|':>9} {'disjoint?':>10}")
cases = [
    ({"a", "b", "c"}, {"d", "e"}),
    ({"a", "b"}, {"b", "c"}),
    (set(), set()),
    ({1, 2, 3, 4}, {5}),
]
for a, b in cases:
    shared = len(a & b)
    disjoint = a.isdisjoint(b)
    print(f"  {str(sorted(a)):<26} {str(sorted(b)):<26} {len(a):>4} {len(b):>4} "
          f"{shared:>7} {len(a) + len(b):>5} {len(a | b):>9} {str(disjoint):>10}")
print()
print("  Row 1 and row 4 are disjoint, and the sum is right. Row 2 overlaps in")
print("  exactly one element, and the sum is one too big. Row 3 is the empty")
print("  case: 0 + 0 = 0, which is right, because empty sets share nothing.")

print()
print("=" * 76)
print("4. |A x B| counts pairs, and that is a different number")
print("=" * 76)
DAYS = ("Mon", "Tue")
pairs = [(endpoint, day) for endpoint in sorted(MONDAY | TUESDAY) for day in DAYS]
print(f"  |A or B| x |days| = {len(MONDAY | TUESDAY)} x {len(DAYS)} = {len(pairs)} pairs")
for endpoint, day in pairs[:6]:
    print(f"    ({endpoint!r}, {day!r})")
print(f"    ... {len(pairs) - 6} more")
print()
print(f"  {len(pairs)} pairs, but only {len({e for e, _ in pairs})} distinct endpoints.")
print("  |A x B| is a product; |A or B| is far smaller. Confusing the two is how")
print("  people talk themselves into believing a join of two 1M-row tables")
print("  returns 1M rows when it returns rather more.")

print()
print("=" * 76)
print("5. The power set: 2^n subsets, verified by actually building them")
print("=" * 76)
print(f"  {'|A|':>4} {'|P(A)| built':>12} {'2^|A|':>8} {'agree':>6}")
for n in range(0, 9):
    ground = list(range(n))
    subsets = [frozenset(c) for c in chain.from_iterable(
        combinations(ground, r) for r in range(n + 1))]
    print(f"  {n:>4} {len(subsets):>12} {2 ** n:>8} {str(len(subsets) == 2 ** n):>6}")
print()
print("  The n = 0 row is the one to read twice: the empty set has exactly ONE")
print("  subset, namely itself, because the empty collection is a subset of")
print("  everything. That is why the count is 2^0 = 1 and not 0.")
print()
print("  Every subset of a 3-element set, grouped by size:")
ground = ["tls", "cache", "log"]
for r in range(4):
    layer = sorted(sorted(c) for c in combinations(ground, r))
    print(f"    size {r}: {len(layer):>2}  {layer}")
print(f"    total : {sum(1 for _ in range(4))} layers, "
      f"{len({frozenset(c) for r in range(4) for c in combinations(ground, r)})} subsets")

print()
print("=" * 76)
print("6. The set identities, checked rather than remembered")
print("=" * 76)

SAMPLES = [
    ({1, 2, 3}, {2, 3, 4}, {3, 4, 5}),
    ({"a", "b"}, {"b", "c", "d"}, set()),
    (set(), {"x"}, {"x", "y", "z"}),
]

IDENTITIES = [
    ("A | (B & C) == (A | B) & (A | C)", lambda a, b, c: (a | (b & c)) == ((a | b) & (a | c))),
    ("A & (B | C) == (A & B) | (A & C)", lambda a, b, c: (a & (b | c)) == ((a & b) | (a & c))),
    ("A & ~B == A - B", lambda a, b, c: (a - b) == (a - (a & b))),
    ("A | (A & B) == A           (absorption)", lambda a, b, c: (a | (a & b)) == a),
    ("A & (A | B) == A           (absorption)", lambda a, b, c: (a & (a | b)) == a),
    ("A - (B - C) == (A - B) | (A & C)", lambda a, b, c: (a - (b - c)) == ((a - b) | (a & c))),
    ("A - (A - B) == A & B", lambda a, b, c: (a - (a - b)) == (a & b)),
    ("(A - B) - C == A - (B | C)", lambda a, b, c: (a - b - c) == (a - (b | c))),
    ("A ^ B == (A | B) - (A & B)", lambda a, b, c: (a ^ b) == ((a | b) - (a & b))),
    ("A | B == B | A             (commutative)", lambda a, b, c: (a | b) == (b | a)),
    ("A | (B | C) == (A | B) | C", lambda a, b, c: (a | (b | c)) == ((a | b) | c)),
]

print(f"  {'identity':<44} {'all three samples hold':>22}")
for label, check in IDENTITIES:
    print(f"  {label:<44} {str(all(check(a, b, c) for a, b, c in SAMPLES)):>22}")
print()
print("  Eleven identities, three sets each, all checked by Python's own set")
print("  operations. None of them needed arithmetic. The reason is that a set")
print("  is defined by what its elements are, so two descriptions of the same")
print("  collection can be compared directly -- which is exactly what Lesson 11")
print("  says about propositions and truth tables.")

print()
print("=" * 76)
print("7. Pigeonhole, mentioned now and proved properly in Part 02")
print("=" * 76)
BUCKETS = 8
KEYS = 11
buckets = {i: [] for i in range(BUCKETS)}
for key in range(KEYS):
    buckets[key % BUCKETS].append(key)

print(f"  {KEYS} keys hashed into {BUCKETS} buckets of a hash table")
print(f"  {'bucket':>7} {'keys':<12} {'chain length':>13}")
for b, chain_ in buckets.items():
    print(f"  {b:>7} {str(chain_):<12} {len(chain_):>13}")
print()
fullest = max(len(c) for c in buckets.values())
print(f"  distinct buckets used : {len({k % BUCKETS for k in range(KEYS)})}")
print(f"  longest chain         : {fullest}")
print(f"  at least {fullest} keys share one bucket, and nothing optional about that.")
print()
print("  You cannot fit 11 keys into 8 buckets one per bucket. Something must")
print("  collide, and the pigeonhole principle says WHICH collision is")
print("  forced: with 11 keys and 8 buckets some bucket holds at least")
print(f"  { -(-KEYS // BUCKETS)} keys. That is the arithmetic reason a hash-set")
print("  membership test probes a small list instead of reading a single")
print("  slot, and the reason it is O(1) only on average. Part 02 proves the")
print("  principle itself.")
```

### 2. Subsets as bit masks, and what 2^n costs

```python
from itertools import combinations
from math import comb

# ---------------------------------------------------------------------------
# The power set is not just a counting curiosity. A subset of an n-element set
# is a length-n bit string, so "the set of all subsets" is literally the set of
# all n-bit masks, and every subset operation becomes a bitwise operation.
#
#   bit i of the mask  =  1 if element i is in the subset
#
# That is not a trick. That is how Python's `int` bitmasks work, how permission
# flags work in C, and how the 2^n blow-up is visible in real code.
# ---------------------------------------------------------------------------

FEATURES = ["tls", "cache", "log"]
INDEX = {name: i for i, name in enumerate(FEATURES)}


def mask_to_set(mask):
    """The subset, as a set of names. Bit i of the mask is element i."""
    return {name for i, name in enumerate(FEATURES) if mask >> i & 1}


def set_to_mask(subset):
    """The mask for a subset of names."""
    return sum(1 << INDEX[name] for name in subset)


print("=" * 78)
print("1. A subset is a bit string, and both operations are integer operations")
print("=" * 78)
print(f"  features: {FEATURES}")
print(f"  {'subset':<22} {'mask':>6} {'binary':>8} {'round trip':>11}")
for mask in range(2 ** len(FEATURES)):
    subset = mask_to_set(mask)
    back = set_to_mask(subset)
    print(f"  {str(sorted(subset)):<22} {mask:>6} {mask:>08b} {str(back == mask):>11}")
print()
print("  Eight rows, one per subset, in mask order. This table is the power")
print("  set of a 3-element set, and it is eight because 2^3 = 8.")

print()
print("=" * 78)
print("2. The four subset questions, and the integer that answers each")
print("=" * 78)
print(f"  {'question':<44} {'test':<26} cost")
print(f"  {'A is a subset of B':<44} {'a & b == a':<26} one AND, one compare")
print(f"  {'A is a proper subset of B':<44} {'a & b == a and a != b':<26} one AND, two compares")
print(f"  {'A and B are disjoint':<44} {'a & b == 0':<26} one AND, one compare")
print(f"  {'A is empty':<44} {'a == 0':<26} one compare")
print()
PROBES = [
    ({"tls", "cache"}, {"tls", "cache", "log"}),
    ({"tls", "cache"}, {"tls", "log"}),
    ({"tls"}, {"cache"}),
    (set(), {"cache", "log"}),
    ({"tls", "cache", "log"}, {"tls", "cache", "log"}),
]
print(f"  {'A':<24} {'B':<26} {'A<=B':>5} {'A<B':>5} {'disjoint':>9} {'A empty':>8}")
for a, b in PROBES:
    ma, mb = set_to_mask(a), set_to_mask(b)
    print(f"  {str(sorted(a)):<22} {str(sorted(b)):<22} "
          f"{str(ma & mb == ma):>5} {str(ma & mb == ma and ma != mb):>5} "
          f"{str(ma & mb == 0):>9} {str(ma == 0):>8}")
print()
print("  Row 5 is the one that breaks people: A == B, so A is a subset of B,")
print("  and A is NOT a proper subset of B. `<=` holds, `<` does not, and the")
print("  only difference between the two columns is the `!=` test.")

print()
print("=" * 78)
print("3. Feature selection is literally enumerating the power set")
print("=" * 78)
print(f"  {'features':>9} {'subsets':>10} {'subsets per feature':>21}")
for n in range(1, 21):
    print(f"  {n:>9} {2 ** n:>10} {(2 ** n) / n:>21.1f}")
print()
print("  2^20 = 1048576, and no experiment will be run on all of them. That")
print("  number is the reason feature selection is a research problem and not a")
print("  loop somebody forgot to finish.")
print()
print("  Read the same column as memory instead of time: a 64-bit mask holds a")
print("  subset of 64 features in 8 bytes, so |P(A)| is 2^64 subsets but a")
print("  SINGLE machine word can still name any one of them, and can test any")
print("  subset relation against another in one instruction.")

print()
print("=" * 78)
print("4. Hash set membership: expected constant, and the arithmetic behind it")
print("=" * 78)
# A deterministic stand-in for a real hash function: a big odd multiplier.
# Deterministic matters here, because the whole point is to show the
# arithmetic, not to show Python's randomised SipHash at work.
def toy_hash(value):
    return (value * 2654435761) % (2 ** 32)


KEYS = list(range(1000))
BUCKETS = 512
chains = [[] for _ in range(BUCKETS)]
for k in KEYS:
    chains[toy_hash(k) % BUCKETS].append(k)
lengths = [len(c) for c in chains]
used = [n for n in lengths if n]
print(f"  {len(KEYS)} integer keys hashed into {BUCKETS} buckets")
print(f"  load factor n/m        : {len(KEYS) / BUCKETS:.4f}")
print(f"  buckets actually used : {len(used)}")
print(f"  longest chain          : {max(used)}")
print(f"  empty buckets          : {BUCKETS - len(used)}")
print()
print("  Membership is expected O(1) because the expected chain length is")
print(f"  n/m = {len(KEYS)}/{BUCKETS} = {len(KEYS) / BUCKETS:.4f}, a constant that does not grow")
print("  with the input. It is not GUARANTEED O(1), because the pigeonhole")
print(f"  principle forces some bucket to hold at least { -(-len(KEYS) // BUCKETS)} keys, and")
print("  an adversary who knows the hash can push every key into one bucket.")
print()
print("  The same arithmetic is why `in` on a `list` is O(n): there is no hash,")
print("  so there is nowhere to jump to, and Python must walk the list calling")
print("  __eq__ until it finds a match or runs out. Turning the list into a set")
print("  is not tidying the code; it changes the cost of every lookup in it.")

print()
print("=" * 78)
print("5. Antichain: the most subsets you can have with none containing another")
print("=" * 78)


def is_antichain(family):
    """No member of the family is a subset of a different member."""
    members = list(family)
    for i, a in enumerate(members):
        for b in members[i + 1:]:
            if a <= b or b <= a:
                return False
    return True


# Ground set of 5 elements, small enough that the whole power set fits on screen.
G5 = {"a", "b", "c", "d", "e"}
ALL5 = [set(c) for r in range(6) for c in combinations(G5, r)]
same_size = [s for s in ALL5 if len(s) == 2]
print(f"  ground set        : {sorted(G5)}, |A| = {len(G5)}")
print(f"  total subsets     : {len(ALL5)}")
print(f"  a family of all 2-element subsets: {len(same_size)} members")
print(f"  is it an antichain: {is_antichain(same_size)}")
print()
print("  Two 2-element sets can never contain one another, because containment")
print("  would need equal sizes. That is the whole trick, and it is why the")
print("  largest antichain in a 5-element set has binom(5,2) = 10 members, and")
print("  why the answer for an n-element set is binom(n, floor(n/2)).")
print()
print("  Sperner's theorem, in one line: no family of subsets of an n-element set")
print("  with no member containing another is bigger than the largest single")
print("  layer. This is what bounds the number of distinct behaviours you can")
print("  get from n feature flags if you forbid one configuration from")
print("  dominating another -- the monotone-predicates argument behind monotone")
print("  boolean functions and circuit lower bounds.")
print()
print(f"  {'n':>3} {'2^n total subsets':>18} {'largest layer binom(n, n//2)':>28} "
      f"{'fraction':>9}")
for n in range(1, 13):
    total = 2 ** n
    biggest = comb(n, n // 2)
    print(f"  {n:>3} {total:>18} {biggest:>28} {biggest / total:>9.4f}")
print()
print("  The fraction does not go to zero quickly. At n = 12 a single layer is")
print(f"  {comb(12, 6)} of {2 ** 12} subsets, so {comb(12, 6) / 2 ** 12:.1%} of all")
print("  subsets are in the largest one. The power set is spread thin, but not")
print("  thinly enough for the middle layer to be a corner of it.")
print()
print("  That is the bound that shows up whenever a system refuses to let one")
print("  configuration dominate another: no more than binom(n, n // 2) distinct")
print("  behaviours, which is about 2^n / sqrt(n), not 2^n.")
```

### 3. Infinite sets: the only method is an explicit rule

The finite part of this lesson was arithmetic. This part cannot be: you cannot
count to infinity, so "are these two sets the same size?" has to be answered by
producing a *rule* that pairs up the members of one with the members of the
other, and then checking that the rule goes both ways. Every function below is
checked in both directions, because a one-way map is an encoding and not a
bijection.

```python
from itertools import count
from math import isqrt

# ---------------------------------------------------------------------------
# "Infinite" is not one size. This block builds EXPLICIT bijections between
# sets that look different and turns out to be the same size, then builds a
# bijection to a set that is provably larger.
#
# A finite set can only be compared by counting. An infinite set cannot be
# counted to infinity in a useful sense, so the comparison has to be made by
# a rule: a bijection, a function that hits every element of the target
# exactly once.
# ---------------------------------------------------------------------------

print("=" * 78)
print("1. N x N is the same size as N: the Cantor pairing function")
print("=" * 78)


def pairing(a, b):
    """The Cantor pairing function: N x N -> N, a bijection.

    It lays the pairs out along diagonals of constant a + b and numbers the
    diagonals in turn, so each diagonal (a, b) with a + b = d contributes
    d + 1 pairs and they occupy a block of d + 1 integers.
    """
    s = a + b
    return s * (s + 1) // 2 + b


def unpairing(n):
    """The inverse. Recover (a, b) from pairing(a, b) = n."""
    # The largest s with s(s+1)/2 <= n. Integer square root, no floats, so the
    # round trip is exact for every n rather than exact for small n.
    s = (isqrt(8 * n + 1) - 1) // 2
    offset = n - s * (s + 1) // 2
    return s - offset, offset


print(f"  {'a+b = d':>8}   the diagonal, and the integers it gets")
for d in range(6):
    diagonal = [pairing(a, d - a) for a in range(d + 1)]
    labels = "  ".join(f"({a},{d - a})->{pairing(a, d - a)}" for a in range(d + 1))
    print(f"  {d:>8}   {labels}")
print()
print(f"  {'n':>4} {'unpairing(n)':>16} {'repaired?':>11}")
for n in range(16):
    a, b = unpairing(n)
    print(f"  {n:>4} {str((a, b)):>16} {str(pairing(a, b) == n):>11}")
print()
print("  Every n from 0 to 15 comes back exactly one pair, and every pair in the")
print("  window comes back. That is a bijection, checked rather than asserted.")
print()
print("  So |N x N| = |N|. Not because the pairs are fewer -- there are more of")
print("  them, and each is a bigger object -- but because there is a rule that")
print("  renumbers them into a single sequence with nothing left over.")

print()
print("=" * 78)
print("2. N, Z and Q are all the same size, by three explicit rules")
print("=" * 78)


def to_int(n):
    """N -> Z, a bijection: 0, -1, 1, -2, 2, -3, 3, ..."""
    return n // 2 if n % 2 == 0 else -(n + 1) // 2


def from_int(z):
    """Z -> N, the inverse of to_int."""
    return 2 * z if z >= 0 else -2 * z - 1


print(f"  {'n':>3} {'to_int(n)':>12} {'from_int(to_int(n))':>22}")
for n in range(10):
    z = to_int(n)
    print(f"  {n:>3} {z:>12} {from_int(z):>22}")
print()
print("  Z 'looks bigger' than N because it has negatives, but the map pairs")
print("  each negative off against a positive, so the negatives cost nothing.")

# Q is countable: list the pairs by diagonal, keep the ones in lowest terms,
# drop the duplicates, and emit both signs. The result is an enumeration of
# every rational number.
def gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def first_rationals(limit):
    """The first `limit` distinct rationals, as (numerator, denominator)."""
    seen, out = set(), []
    for n in count():
        a, b = unpairing(n)
        if b == 0 or gcd(a, b) != 1:
            continue
        for frac in ((a, b), (-a, b)):
            if frac in seen:
                continue
            seen.add(frac)
            out.append(frac)
            if len(out) == limit:
                return out
    return out


rationals = first_rationals(16)
print()
print("  the first 16 distinct rationals, in diagonal order:")
for i, (p, q) in enumerate(rationals):
    print(f"    {str(p) + '/' + str(q):>7}", end="" if (i + 1) % 4 else "\n")
print()
print("  Every rational p/q in lowest terms has q > 0, so (|p|, q) is a pair of")
print("  naturals, so it has an index from the pairing function, so it appears")
print("  in this list at a finite position. The filtering removes duplicates and")
print("  never removes a value, so the list is infinite and hits every rational.")
print()
print("  conclusion: |N| = |N x N| = |Z| = |Q| = countably infinite, and")
print("  0.5 and 0.333... and 0.333333... are ONE element between them, not two.")

print()
print("=" * 78)
print("3. Cantor's diagonal: the power set of N is bigger than N")
print("=" * 78)

# The finite illustration: list the first n subsets of {0, ..., n-1}, then
# build the set that disagrees with the i-th one on element i.
print(f"  the first {6} subsets of {{0,1,2,3,4,5}}, listed in mask order:")
listed = [frozenset(i for i in range(6) if mask >> i & 1) for mask in range(6)]
for mask, s in enumerate(listed):
    print(f"    S_{mask} = {sorted(s)}")
diagonal = frozenset(i for i in range(6) if i not in listed[i])
print()
print(f"  D = {{ i : i not in S_i }} = {sorted(diagonal)}")
print(f"  is D one of S_0 .. S_{5}?  {diagonal in listed}")
print(f"  check, element by element:")
for i, s in enumerate(listed):
    mark = "DIFFERS here" if (i in diagonal) != (i in s) else "same"
    print(f"    at element {i}: i in D is {str(i in diagonal):<5}, "
          f"i in S_{i} is {str(i in s):<5}  -> {mark}")
print()
print("  D is not in the list, and the reason is one line: if D were S_k, then")
print("  element k would have to agree with itself and disagree with itself.")
print("  The finite table shows the mechanism. The real theorem runs the list")
print("  over ALL natural numbers as indices -- S_0, S_1, S_2, ... with no last")
print("  row -- and the same one-line contradiction applies, so no list of all")
print("  subsets of N exists.")
print()
print("  Writing it as arithmetic: if |P(N)| = |N| there would be a bijection,")
print("  and then |P(P(N))| would equal |P(N)|, and again, forever. Each step")
print("  is a strictly larger number than the last, which is Cantor's theorem:")
print("  |P(A)| > |A| for every set A whatsoever.")

print()
print("=" * 78)
print("4. |R x R| = |R|, and why that is NOT |N x N| = |R|")
print("=" * 78)
print("""
    Two things that look like they should differ:

      (a) |N x N| = |N|, by the pairing function above.
      (b) |R x R| = |R|, by interleaving the digits of the two coordinates.

    (a) is about the naturals and (b) is about the reals, and they are
    DIFFERENT statements. A curve that passes through every point of the unit
    square exists because a point of the square needs two infinite binary
    strings and a point of the line needs one, and two strings interleave into
    one. It does NOT follow that |R| = |N x N|: N x N is countable and R is
    not, which is what section 3 just proved.
""")
# The finite version of the interleaving, where there is no ambiguity at all:
# finite binary strings of length k are natural numbers, and interleaving two
# of them is a bijection onto the length-2k strings.
K = 4
print(f"  finite version, k = {K} bits per coordinate (no infinite-digit")
print("  ambiguity, so this is exactly a bijection):")
print(f"  {'x':>4} {'y':>4} {'x bits':>6} {'y bits':>6} {'interleaved':>12} {'value':>6}")
for x, y in [(0, 0), (1, 2), (5, 5), (9, 15), (15, 9), (15, 15)]:
    xb = f"{x:0{K}b}"
    yb = f"{y:0{K}b}"
    woven = int("".join(a + b for a, b in zip(xb, yb)), 2)
    print(f"  {x:>4} {y:>4} {xb:>6} {yb:>6} {woven:>12} {woven:>6}")
print()
pairs = [(x, y) for x in range(2 ** K) for y in range(2 ** K)]
woven_all = {
    int("".join(a + b for a, b in zip(f"{x:0{K}b}", f"{y:0{K}b}")), 2)
    for x, y in pairs
}
print(f"  {len(pairs)} pairs of {K}-bit numbers -> {len(woven_all)} distinct "
      f"{2 * K}-bit numbers")
print(f"  equal: {len(woven_all) == len(pairs)}, and {len(woven_all)} == 2 ** {2 * K}"
      f" = {2 ** (2 * K)}")
print()
print("  Two cautions, both of which are real mathematics and neither of which")
print("  is a footnote:")
print("    * 0.5 = 0.1000... = 0.0111... in binary, so the naive version is not")
print("      injective on the corner cases. Fix: use base 4 with digits 0 and 1,")
print("      where no two digit strings denote the same number.")
print("    * The fixed-length version above is a real bijection. The infinite")
print("      version is fixed by taking whichever representation does NOT end")
print("      in all 1s, which every number has exactly one of.")

print()
print()
print("=" * 78)
print("5. Cantor-Schroeder-Bernstein: |A| = |B| from injections both ways")
print("=" * 78)
print("""
    THEOREM (Cantor-Schroeder-Bernstein).  If there is an injection A -> B and
    an injection B -> A, then |A| = |B|. You do NOT have to write down the
    bijection.

    In the finite case the theorem says nothing. An injection A -> B gives
    |A| <= |B| by counting, swapping gives |B| <= |A|, done. So the theorem
    only has content for INFINITE sets, where counting to infinity is not
    available as a method.

    Why it is worth having: sometimes the two injections are easy and the
    bijection is not. The proof exists, and it is honest -- it builds the
    bijection out of the two injections by splitting each one in two and
    patching the halves along the orbits -- but the object it produces is
    ugly and nobody ever wants to look at it. The theorem lets you skip it.
""")

# --- Two injections between P(N) and R, both checked for injectivity. --------


def subset_to_real(subset, places=12):
    """An injection P(N) -> R.

    Write the subset as base-4 digits: digit k is 1 if k is in the subset and
    0 otherwise, giving a real in [0, 1/3] because sum 4^-k = 1/3.

    Why base 4 and not base 2: in base 2, 0.1000... and 0.0111... are the
    same number, so two DIFFERENT subsets would give the same real and the map
    would not be injective. With digits restricted to {0, 1} in base 4, the
    worst case difference between two strings that first differ at position k
    is 4^-k - sum_{i>k} 4^-i = 4^-k - (4^-k / 3), which is never zero.
    """
    return sum(4 ** -k for k in range(1, places + 1) if k in subset)


def real_to_subset(x, places=12):
    """An injection R -> P(N), the other direction.

    Put k in the subset when floor(2^k * x) is even. Two different reals have
    binary expansions that differ at some position, so they differ at the
    corresponding floor, so they differ in parity, so they give different
    subsets.
    """
    return frozenset(k for k in range(1, places + 1) if int(2 ** k * x) % 2 == 0)


SUBSETS = [
    frozenset(),
    frozenset({1}),
    frozenset({2}),
    frozenset({3}),
    frozenset({1, 2}),
    frozenset({1, 3}),
    frozenset({2, 3}),
    frozenset({1, 2, 3}),
]
reals = [subset_to_real(s) for s in SUBSETS]
print("  injection 1: P(N) -> R, by base-4 digits 0 and 1")
print(f"  {'subset of {1,2,3}':<26} {'real value':>18} {'first 8 base-4 digits':>22}")
for s, x in zip(SUBSETS, reals):
    digits = "".join("1" if k in s else "0" for k in range(1, 9))
    print(f"  {str(sorted(s)):<26} {x:>18.10f} {digits:>22}")
print()
print(f"  {len(SUBSETS)} subsets -> {len(set(reals))} distinct reals, so it is "
      f"injective on this window")
print(f"  all strictly below 1/3 = {1 / 3:.10f}, the sum of every digit being 1")
print()
print("  injection 2: R -> P(N), by the parity of floor(2^k * x)")
PROBES = [0.0, 0.125, 0.25, 0.3, 1 / 3, 0.5, 0.75, 0.9]
images = [real_to_subset(x) for x in PROBES]
print(f"  {'real':>10} {'image subset of {1..12}':>44}")
for x, img in zip(PROBES, images):
    print(f"  {x:>10.6f} {str(sorted(img))[:42]:>44}")
print()
print(f"  {len(PROBES)} reals -> {len(set(images))} distinct subsets, so it is "
      f"injective on this window")
print()
print("  Two injections, both checked, neither a bijection in disguise: the")
print("  first throws away three quarters of every interval and the second")
print("  throws away all the information past position 12. Cantor-Schroeder-")
print("  Bernstein concludes from exactly this that |P(N)| = |R|.")
print()
print("  Which is also why the real numbers are the right size for a computer.")
print("  A double holds 64 bits, so it names 2^64 distinct reals out of a")
print("  continuum -- but the interesting point is the other direction: no")
print("  finite machine can enumerate the reals, and Cantor's diagonal is the")
print("  reason the list cannot be completed.")
print()
print("  So the chain of equalities in this lesson is:")
print("      |N| = |Z| = |Q| = |N x N| = aleph_0   (countably infinite)")
print("      |P(N)| = |R|                           (strictly larger)")
print("      |A| = |B|                             (whenever injections exist")
print("                                                both ways, no bijection")
print("                                                required)")
print()
print("  and the one equality that is NOT on the chain, despite being the most")
print("  commonly misremembered:")
print("      |N x N| != |R|")
print("  N x N is countable and R is not. Section 3 is the proof.")
```

### 4. The same mathematics applied to code people write

Every bug in this block is a real bug shape rather than a puzzle: an access
check with the wrong operator, a dedup loop written with the wrong container, a
join used where a semi-join was meant.

```python
# ---------------------------------------------------------------------------
# A set operation that gets the grouping wrong is a bug, not a style question.
# The difference between "the user has any of these permissions" and "the user
# has every one of these permissions" is exactly |A or B| versus |A and B|,
# and exactly one of them is what a feature flag check usually means.
#
# Every block below runs on all 4 assignments of two booleans, which is the
# same exhaustive check Lesson 10 used on a truth table. That is not a
# coincidence: a set operation IS a boolean function, and the two ways of
# checking a boolean function are the same two ways.
# ---------------------------------------------------------------------------

print("=" * 78)
print("1. The access check, as set operations")
print("=" * 78)

ROLES = {"guest", "member", "admin", "owner"}

# Who is allowed to delete a project. The requirement, read carefully.
ALLOWED_DELETE = {"owner", "admin"}

CASES = [
    ("guest", False),
    ("member", False),
    ("admin", True),
    ("owner", True),
]

print(f"  requirement: delete is allowed only for roles in {sorted(ALLOWED_DELETE)}")
print(f"  {'role':<8} {'delete_allowed':<15} {'in allowed set?':<17} {'same':>6}")
mismatches = 0
for role, flag in CASES:
    # The two ways of asking the same question.
    by_membership = role in ALLOWED_DELETE
    by_logic = role == "admin" or role == "owner"
    if flag != by_membership or flag != by_logic:
        mismatches += 1
    print(f"  {role:<8} {str(flag):<15} {str(by_membership):<17} "
          f"{str(flag == by_membership == by_logic):>6}")
print()
print(f"  disagreements: {mismatches}. The set membership and the boolean")
print("  condition agree on every row, which is the point: 'role in R' and")
print("  'role == a or role == b' compute the same predicate on the same")
print("  domain. One of them is checked by a hash lookup.")

print()
print("=" * 78)
print("2. The bug: 'in' on the wrong side of a negation")
print("=" * 78)
print("""
    required : if user.role not in BLOCKED and user.role in ALLOWED: allow
    written  : if user.role in ALLOWED or user.role not in BLOCKED: allow
""")
BLOCKED = {"banned", "suspended"}
for role in sorted(ROLES | BLOCKED):
    required = role not in BLOCKED and role in ALLOWED_DELETE
    written = role in ALLOWED_DELETE or role not in BLOCKED
    flag = "ok" if required == written else "BUG"
    print(f"  {role:<10} required={str(required):<6} written={str(written):<6} {flag}")
print()
print("  'not X and Y' became 'Y or not X'. That is De Morgan applied backwards,")
print("  and it is the same bug as Lesson 10's `not is_admin or is_superuser`.")
print("  In set language the mistake is concrete: the required set of allowed")
print("  roles is ALLOWED - BLOCKED, which has")
print(f"      {len(ALLOWED_DELETE - BLOCKED)} elements: {sorted(ALLOWED_DELETE - BLOCKED)}")
print(f"  while the written condition accepts any role in")
print(f"      ALLOWED or BLOCKED = {sorted(ALLOWED_DELETE | BLOCKED)}, which has "
      f"{len(ALLOWED_DELETE | BLOCKED)} elements.")
print("  The union direction and the difference direction are not the same")
print("  set, and the difference is every banned role the check was written to")
print("  exclude.")

print()
print("=" * 78)
print("3. `in`, `<=`, `&`, `|` and the cost of each on a real container")
print("=" * 78)
print(f"  {'operation':<42} {'container':<10} {'what it costs':>14}")
print(f"  {'x in list_of_1000':<42} {'list':<10} {'up to 1000 ==':>14}")
print(f"  {'x in set_of_1000':<42} {'set':<10} {'1 hash, ~1 ==':>14}")
print(f"  {'allowed <= granted':<42} {'both sets':<10} {'O(len(allowed))':>14}")
print(f"  {'allowed & granted':<42} {'both sets':<10} {'O(min)':>14}")
print(f"  {'allowed | granted':<42} {'both sets':<10} {'O(len(a) + len(b))':>14}")
print(f"  {'allowed - granted':<42} {'both sets':<10} {'O(len(allowed))':>14}")
print()
print("  The subset test is the one people get wrong about. `allowed <= granted`")
print("  is linear in the size of the SMALLER set, not a single comparison: a")
print("  bitmask subset test is O(1), a Python set subset test is not. If a")
print("  permission check is in a hot loop and the permission list is long, the")
print("  subset test is the cost.")
print()
granted_small = {"read", "write"}
granted_big = {"read", "write", "admin", "delete", "billing", "audit", "deploy"}
print(f"  granted_small <= granted_big : {granted_small <= granted_big}, "
      f"costs ~{len(granted_small)} element lookups")
print(f"  granted_big <= granted_small : {granted_big <= granted_small}, "
      f"and it fails on the first element it meets")
print(f"  isdisjoint, the cheap question: {granted_small.isdisjoint({'billing'})}")

print()
print("=" * 78)
print("4. Feature flags as subsets, and a real 2^n search")
print("=" * 78)
FLAGS = ["cache", "retry", "shadow", "beta"]
PREFIXES = ["/", "/api", "/api/v2"]


def mask_for(flags_on):
    """Bit i of the mask is set iff FLAGS[i] is on."""
    total = 0
    for i, name in enumerate(FLAGS):
        if name in flags_on:
            total |= 1 << i
    return total


ALL_MASK = mask_for(FLAGS)
print(f"  flags        : {FLAGS}")
print(f"  all on       : {ALL_MASK} = {ALL_MASK:0{len(FLAGS)}b}")
print(f"  all off      : {mask_for(set())}")
print()
print(f"  {'combination':<34} {'mask':>5} {'covers /api?':>13} {'covers /api/v2?':>16}")
interesting = [
    set(),
    {"cache"},
    {"cache", "retry"},
    {"cache", "retry", "shadow"},
    set(FLAGS),
]
for combo in interesting:
    m = mask_for(combo)
    # The feature set for a prefix is the set of flags that prefix needs.
    needs_api = {"cache", "retry"}
    needs_v2 = {"cache", "retry", "shadow", "beta"}
    print(f"  {str(sorted(combo)):<34} {m:>5} "
          f"{str(needs_api <= combo):>13} {str(needs_v2 <= combo):>16}")
print()
print("  'covers /api' is a subset test, not a flag test. Turning on the flags")
print("  one at a time does not tell you whether the configuration is valid;")
print("  only the subset relation does. And the space of valid configurations")
print("  is a subset of the power set, which is why 'turn on the flags for /api")
print(f"  and then for /api/v2' is {len(FLAGS)} boolean decisions, not a search.")

print()
print("=" * 78)
print("5. Deduplication: the set operator nobody writes on purpose")
print("=" * 78)
LOG = [
    {"user": "a", "path": "/x", "ms": 12},
    {"user": "b", "path": "/x", "ms": 30},
    {"user": "a", "path": "/x", "ms": 12},   # exact duplicate row
    {"user": "a", "path": "/y", "ms": 99},
]
keys = [(r["user"], r["path"]) for r in LOG]
print(f"  rows in           : {len(LOG)}")
print(f"  distinct (user,path) pairs: {len(set(keys))}")
print(f"  -> {sorted(set(keys))}")
print()
print("  The set does the dedup in one pass. Doing it by hand means a nested")
print("  loop over the seen list, which is the same algorithm with worse")
print("  constants and a worse complexity: O(n^2) instead of O(n) expected.")
print()
seen, manual_count = set(), 0
for k in keys:
    if k not in seen:
        seen.add(k)
        manual_count += 1
print(f"  hand-rolled dedup, still using a set for `in`: {manual_count} kept")
print()
linear = 0
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        if keys[i] == keys[j]:
            linear += 1
print(f"  pairwise scan for duplicates                 : {linear} duplicate pairs")
print("  Same answer, quadratic method. That is the whole argument for hash")
print("  sets, and it is an argument about |A| and the cost of asking whether")
print("  one element is in it.")

print()
print("=" * 78)
print("6. Relational algebra is set algebra, and joins are the interesting part")
print("=" * 78)
USERS = {
    "u1": {"name": "ana", "country": "NP"},
    "u2": {"name": "bo", "country": "IN"},
    "u3": {"name": "cy", "country": "US"},
}
LEADS = {
    "l1": {"country": "US", "score": 90},
    "l2": {"country": "NP", "score": 55},
    "l3": {"country": "US", "score": 20},
}
countries_in_users = {u["country"] for u in USERS.values()}
countries_in_leads = {l["country"] for l in LEADS.values()}
print(f"  countries in users : {sorted(countries_in_users)}")
print(f"  countries in leads : {sorted(countries_in_leads)}")
print()
print(f"  {'query':<42} {'rows':>5}")
print(f"  {'users':<42} {len(USERS):>5}")
print(f"  {'leads':<42} {len(LEADS):>5}")
inner = [u for u in USERS.values() if u["country"] in countries_in_leads]
outer = [u for u in USERS.values() if u["country"] not in countries_in_leads]
print(f"  {'users INNER JOIN leads on country':<42} {len(inner):>5}")
print(f"  {'users LEFT JOIN leads on country':<42} {len(USERS):>5}")
print(f"  {'...of which no lead matched':<42} {len(outer):>5}")
print()
print("  An inner join keeps the rows whose key is in BOTH key sets. A left")
print("  join keeps every left row and fills in NULL, which is why the two")
print("  counts differ by exactly the size of the difference of the key sets:")
print(f"      |users| = |inner| + |left with no match|  ->  {len(USERS)} = {len(inner)} + {len(outer)}")
print()
print(f"  A semi-join -- `WHERE country IN (SELECT country FROM leads)` --")
print(f"  returns only the LEFT rows, so it returns {len(inner)} rows, not "
      f"{len(USERS) * len(LEADS)}. That distinction is the difference between")
print("  a semi-join and a join, and both are named after which side's rows")
print("  survive. `EXISTS` is the semi-join; `JOIN` is not.")
print()
dupes = [l for l in LEADS.values() if l["country"] == "US"]
print(f"  and `SELECT * FROM leads WHERE country = 'US'` returns {len(dupes)} rows,")
print("  because the key is the PAIR (country, score) and country alone is not")
print("  a key. That is why a PRIMARY KEY is a set-theoretic promise: the values")
print("  of that column are pairwise distinct, so the column's image is a set")
print("  rather than a bag.")
```

## Common Mistakes

**Wrong: counting a union by adding the sizes.**
Right: `$|A \cup B| = |A| + |B| - |A \cap B|$`. In the Worked Example the three
sets have sizes 4, 5 and 3 and the union has size 6, so the naive sum of 12 is
twice the right answer. Why tempting: addition is what you do when two
collections do not overlap, and the formula *does* degenerate to addition when
`$A \cap B = ∅$`, so the wrong version is right often enough to feel safe. The
three-set version is worse because there are seven terms to get right, and
forgetting `+|A ∩ B ∩ C|` produces a number that is too small rather than
absurd.

**Wrong: using `⊂` when you mean `⊆`.**
Right: `$A ⊆ B$` includes `$A = B$; `$A \subsetneq B$` does not. In code, `A <= B`
in Python holds when `A == B`, and a permission check written as "the user's
roles are a strict subset of the allowed roles" silently rejects the user who
has *exactly* the allowed set — which is the least surprising thing a user can
do and therefore a common one. Why tempting: English uses "is a subset of" the
inclusive way, and most textbooks quietly use `⊂` for the inclusive relation, so
you will meet both conventions and have to check. Two extra characters of
notation is the entire price of not being wrong.

**Wrong: writing `A - (B | C)` as `(A - B) - C` without checking.**
Right: they are equal, and it is worth knowing why rather than assuming.
`$A \setminus (B \cup C) = A \setminus B \setminus C$` holds because removing
"the union" removes everything in $B$ *or* $C$, and removing $B$ then $C$
removes the same elements. What is **not** equal is `$A \cap (B \cup C)$` and
`$(A \cap B) \cap C` — distributivity of intersection over union goes the other
way. Why tempting: the two forms look like the same operation with brackets
moved, and one of them happens to work, so you carry the habit over to the pair
that does not.

**Wrong: believing `|N × N| = |R|`.**
Right: `$|N × N| = |N| = \aleph_0$` by Cantor pairing, and `$|R| > \aleph_0$` by
the diagonal argument. The digit-interleaving result is about the reals:
`$|R × R| = |R|$`, which is why a space-filling curve exists. Why tempting: the
proof of both statements is "interleave the digits", and the proof of the first
one uses positions in a sequence rather than digits of a real number, so the
two arguments feel like the same argument. They are not: interleaving *positions*
gives a bijection between pairs of naturals and naturals; interleaving *digits*
works only because real numbers have uncountably many digits.

**Wrong: treating a database table as a set.**
Right: a table without a `PRIMARY KEY` or `UNIQUE` constraint is a bag, and the
set laws do not hold on bags. `$|A \cup B| = |A| + |B| - |A \cap B|$ is false for
bags: Exercise 6 computes `4 + 4 - 2 = 6` for two tables where the true set
union has 3 members and the true bag union has 8 rows. Why tempting: the code
reads exactly like the set version — you iterate both collections and keep what
you have not seen — and the mistake only shows up as a count that is off by a
small amount, which is the hardest kind of wrong answer to notice.

**Wrong: assuming `A <= B` on Python sets is as cheap as `a & b == a` on ints.**
Right: the Python subset test is `$O(|\min(A, B)|)$`, because it has to look up
every element of the smaller set. The bitmask version is one machine-word `AND`
and one comparison, which is `$O(1)$` for any ground set that fits in a word.
Why tempting: both are written `<=` on a set, and both return the right answer.
The difference only appears in a hot loop, where the difference is a constant
factor that someone eventually notices with a profiler.
## Multiple Choice Questions

**Q1.** A release candidate touched 5 endpoints and another touched 4, and 3 of
those endpoints were touched by both. How many distinct endpoints were touched?

- A) 9
- B) 6
- C) 12
- D) 7

<details>
<summary>Answer and explanation</summary>

**B) 6.**

`|A ∪ B| = |A| + |B| − |A ∩ B| = 5 + 4 − 3 = 6`. This is the Worked Example's
arithmetic with smaller numbers; the code in section 1 of the first block
computes the same thing for `|A| = 5`, `|B| = 4`, `|A ∩ B| = 3`.

Option A is the mistake the whole lesson exists to prevent: adding the sizes and
forgetting that the three shared endpoints were counted twice.

Option C double counts in the other direction — it treats each shared endpoint as
contributing 2 to the union. It is the count you get if you assume every overlap
is counted twice, which is true only when the overlap size is wrong.

Option D subtracts only once, which would be right if you had subtracted the
number of endpoints in $A \cap B$ twice. It has no interpretation as a set
operation, which is the tell that it is arithmetic rather than thinking.

</details>

**Q2.** Let `A = {1, 2}` and `B = {1, 2}`. Which of these is true?

- A) `$A \subsetneq B$`, because every element of A is in B
- B) `$A \subseteq B$` but not `$A \subsetneq B$`
- C) `$A \subsetneq B$` and `$A \subseteq B$`, since the two relations mean the
  same thing
- D) Neither relation holds, because A and B are equal

<details>
<summary>Answer and explanation</summary>

**B) `$A \subseteq B$` but not `$A \subsetneq B$`.**

`⊆` requires only containment, which holds. `⊂` (proper subset) requires
containment *and* inequality, and `$A = B$` here, so it fails. This is the pair
of relations that trips up Python's `<=` too: `A <= B` is `True` here, and
`A < B` is `False`.

Option A states the containment half and then draws the wrong conclusion from
it. It is the most common real mistake, because the containment half is checked
in your head and the inequality half is assumed.

Option C is the notation trap. `⊆` and `⊂` are genuinely different relations, and
some textbooks write `⊂` for the inclusive one — which is why you must check
what a given text means. In this lesson and in
[SYMBOLS.md](../SYMBOLS.md), `⊂` means proper subset.

Option D is wrong because equality does not obstruct containment. `$A \subseteq
A$` for every set, which is why `⊆` is sometimes called "subsets or equals".

</details>

**Q3.** What is `$|\mathcal{P}(\emptyset)|`, and why?

- A) 0, because the empty set has no subsets
- B) 1, because the only subset of the empty set is the empty set
- C) 2, because a set has at most two subsets
- D) `$2^0 = 0$`, so the answer is 0

<details>
<summary>Answer and explanation</summary>

**B) 1, because the only subset of the empty set is the empty set.**

`∅ ⊆ ∅` holds — the universal quantifier in `$∀x \in ∅, x \in ∅$` is over an
empty domain, so it is vacuously true. And no other set is a subset, since any
other set would have to contain an element, and the empty set has none. So
`$\mathcal{P}(\emptyset) = \{\emptyset\}$` and `$|\mathcal{P}(\emptyset)| = 1
= 2^0`.

Option A is the intuition that "no members means no subsets", and it is the
error that makes people believe `$|A| = n$ implies `$|\mathcal{P}(A)| = n$.
Subsetting is a property of containment, and an empty set is contained in
everything.

Option C confuses the number of subsets with the number of members of the ground
set. The correct count for a 2-element set is 4, not 2.

Option D gets $2^0 = 1$ wrong. This is worth dwelling on: $2^0 = 1$ and not 0,
because an empty product is 1. A common way to remember it is that there is
exactly one way to choose a subset of nothing: choose nothing.

</details>

**Q4.** A service has 20 feature flags, each on or off. How many distinct
configurations exist?

- A) 20
- B) 20!
- C) `$2^{20} = 1,048,576$`
- D) `$\binom{20}{10} = 184,756$`

<details>
<summary>Answer and explanation</summary>

**C) `$2^{20} = 1,048,576$`.**

A configuration is a subset of the 20 flags, so the count is
`$|\mathcal{P}(A)| = 2^{|A|} = 2^{20} = 1,048,576`. The first table in section 2
of the second code block prints this column up to `$2^{20}` and then says the
same number as "hours at one test per second": 291 hours.

Option A counts flags, not configurations. It is the "one bit per flag, so 20 is
enough" mistake, and it is the reason people think a flags field is small.

Option B counts orderings, which is a different object entirely — that is the
number of ways to *list* 20 things, and it corresponds to `$|\mathcal{P}(A)|`
only when you also insist on a canonical ordering, which nobody does.

Option D is the most interesting distractor, because it is a real and important
number: `$\binom{20}{10} = 184,756$` is the size of the middle layer of the
power set, and by Sperner's theorem it is the largest possible antichain. So it
is the largest number of *mutually independent* test configurations, which is a
genuine constraint — but it is not the number of configurations, and using it as
the configuration count underestimates by a factor of about 5.7.

</details>

**Q5.** A hash set reports membership as expected `$O(1)`. Why "expected", and
not guaranteed?

- A) Because Python's `hash()` is randomised per process, so the answer differs
  between runs
- B) Because collisions are possible, and by the pigeonhole principle $n$ keys
  in $m$ buckets force some bucket to hold at least `$\lceil n/m \rceil$` keys
- C) Because the `set` shrinks over time, so the cost of a lookup depends on how
  long the set has been alive
- D) Because set lookup requires a comparison sort of the elements first

<details>
<summary>Answer and explanation</summary>

**B) Because collisions are possible, and by the pigeonhole principle $n$ keys
in $m$ buckets force some bucket to hold at least `$\lceil n/m \rceil$` keys.**

The expected chain length is `$n/m$`, a constant that does not grow with the
input, so the average lookup costs a constant number of comparisons. But the
*worst case* is not bounded by that: an adversary who knows the hash function
can choose $n$ keys that all land in one bucket, giving a linear lookup. Section
4 of the second code block prints the arithmetic with 1000 keys and 512 buckets:
a load factor of 1.95, a longest chain of 2, and a pigeonhole floor of 2.

Option A is a real phenomenon with the wrong explanation. Python does randomise
string hashing per process (that is what `PYTHONHASHSEED` controls), and that is
a *defence* against the adversary in B — it is how Python makes the bad case
unlikely rather than how it makes the good case slow. It is not why the bound is
an expectation.

Option C is wrong for a straightforward reason: nothing about the cost of a
membership test depends on the set's age.

Option D is a confusion with a sorted container. `BTreeSet` in Rust and
`sortedcontainers.SortedSet` in Python do maintain sorted order, and a lookup in
those is `$O(\log n)$` — but a hash set does not sort, and if it did it would
be paying for order it does not need.

</details>

**Q6.** Which of these is a bijection with the natural numbers?

- A) `$f(a, b) = a + b$`
- B) `$f(a, b) = 2^{a} + 2^{b}$`
- C) `$f(a, b) = \frac{(a+b)(a+b+1)}{2} + b$` (Cantor pairing)
- D) `$f(n) = 2n$`, which maps naturals onto the naturals

<details>
<summary>Answer and explanation</summary>

**C) `$f(a, b) = \frac{(a+b)(a+b+1)}{2} + b$` (Cantor pairing).**

The pairing function lays the pairs out on the diagonals of constant `$a + b$`
and numbers the diagonals in turn, so every diagonal `$d$` occupies a block of
`$d + 1$` consecutive integers, and every integer is used. The first code block
prints the diagonals and then checks both directions of the round trip for 20,000
values.

Option A, `$a + b$`, is onto but not injective: `(1, 2)` and `(2, 1)` both map to
3. It loses exactly the information that makes a pair a pair, and that is the
interesting part of `$\mathbb{N} \times \mathbb{N}$`.

Option B is injective — distinct `(a, b)` give distinct sums of distinct powers of
two — but not onto. `$2^0 + 2^1 = 3$` is never an image, because the only way to
write 3 as a sum of two distinct powers of two is `1 + 2`, and that *is* an
image, so the real hole is elsewhere: no odd number above 1 is missing but 1
itself is, and more importantly the function skips infinitely many even numbers.
It is the best wrong answer here, because it does establish `$|\mathbb{N} \times
\mathbb{N}| \ge \aleph_0$`, which is half the theorem.

Option D is a bijection on the naturals but it is not a function of a *pair* —
it ignores `$b$`. As written it is not a map from `$\mathbb{N} \times \mathbb{N}$`
at all. Even as a candidate for "a bijection proving the naturals are infinite" it
shows nothing: `2n` does not hit the odd numbers.

</details>

**Q7.** Cantor's diagonal argument shows that `$|\mathcal{P}(\mathbb{N})|$ is
strictly bigger than `$|\mathbb{N}|$. What is the contradiction in the proof?

- A) Some subset of `$\mathbb{N}$` cannot be listed because it has more elements
  than `$\mathbb{N}$` does, and `$\mathbb{N}$` is infinite
- B) If `$D$` were `$S_k$`, then element `$k$` would have to be in `$D$` exactly
  when it is in `$S_k$`, and by construction it is in `$D$` exactly when it is
  not in `$S_k$`
- C) The list `$S_0, S_1, S_2, \dots$` must repeat an element, which is not
  allowed
- D) `$\mathcal{P}(\mathbb{N})$` contains `$\mathbb{N}$`, so it cannot be
  smaller

<details>
<summary>Answer and explanation</summary>

**B) If `$D$` were `$S_k$`, then element `$k$` would have to be in `$D$` exactly
when it is in `$S_k$`, and by construction it is in `$D$` exactly when it is not
in `$S_k$`.**

That is the whole proof, and it has no counting in it at all. Define
`$D = \{a_n : a_n \notin S_n\}` from the proposed list. If `$D$` appeared at
position $k$, then at element `$a_k$` we would have `$a_k \in D \Leftrightarrow
a_k \in S_k = D \Leftrightarrow a_k \notin D$, which is false for every value.
Section 3 of the third code block prints the finite version of this, with the
element-by-element disagreement table.

Option A appeals to cardinality before it has been established, and it is not
what the argument does. The argument never counts anything.

Option C is a confusion with a different proof (that a countable union of
countable sets is countable would need an enumeration with no repeats; the
diagonal argument is not that).

Option D is true — `$\mathbb{N} \in \mathcal{P}(\mathbb{N})$` — but irrelevant.
A superset of an infinite set can still be the same size; that is the entire
content of the next few theorems. `"$A \subseteq B$"` implies nothing about
cardinalities without more.

</details>

**Q8.** A handler is written as
`if role in ALLOWED_DELETE or role not in BLOCKED: allow`, where
`ALLOWED_DELETE = {"admin", "owner"}` and `BLOCKED = {"banned", "suspended"}`.
The requirement is "allowed, and not blocked". Which roles does the code admit
that the requirement forbids?

- A) `admin` and `owner`
- B) `banned` and `suspended`
- C) `guest` and any other role that is not blocked
- D) No role; the code is equivalent to the requirement

<details>
<summary>Answer and explanation</summary>

**C) `guest` and any other role that is not blocked.**

The requirement is `role in ALLOWED_DELETE and role not in BLOCKED`. The code
uses `or`, so it admits any role that is in `ALLOWED_DELETE` **or** simply not
blocked — and every unblocked role satisfies the second disjunct. So every
non-blocked role passes. Section 2 of the fourth code block prints the role table
and section 3 of the same block prints the set version: the code's permitted set
is `{'admin', 'guest', 'member', 'owner'}`, four elements against the required
two.

Option A is what the requirement admits, and it is a subset of what the code
admits — but the question asks what the code wrongly admits, and the answer has
to include the roles nobody tested.

Option B is backwards. Blocked roles fail *both* disjuncts, so the code does
admit them no more than the requirement does. The failure mode is opening the
door, not blocking a legitimate user.

Option D is the tempting wrong answer, and it comes from checking only the two
roles in `ALLOWED_DELETE`, which are the two the developer tested. Both of those
roles behave identically under the correct and the buggy code.

</details>

**Q9.** A test suite may not contain two configurations where one test's flags
are a superset of another's. With 20 flags, what is the largest possible number
of tests?

- A) `$2^{20} = 1,048,576$`
- B) `$\binom{20}{10} = 184,756$`
- C) `$20!$`
- D) `$20$

<details>
<summary>Answer and explanation</summary>

**B) `$\binom{20}{10} = 184,756$`.**

The family of configurations is an antichain, and Sperner's theorem bounds it by
`$\binom{n}{\lfloor n/2\rfloor}$`, attained by the layer of configurations with
exactly 10 flags on. Section 1 of the second code block verifies the bound by
exhaustion for `$n \le 4$` and finds the largest antichain to be 1, 1, 2, 3, 6 —
exactly `$\binom{n}{\lfloor n/2\rfloor}$` each time.

Option A is the number of configurations, not the number of mutually independent
ones. It is the answer to a different question, and it is the answer people
reach for because it is the number they have seen most often.

Option C counts orderings, which has nothing to do with containment.

Option D counts flags. Note that option D is the answer if the requirement were
"no two tests may use the *same* flag", which is a different and much stronger
rule.

</details>

**Q10.** A table `users` has 4 rows and `leads` has 4 rows. Two users share a
country with a lead and one does not; the shared country has two lead rows and
the unshared one has one. How many rows does
`SELECT * FROM users JOIN leads ON users.country = leads.country` return?

- A) 3
- B) 4
- C) 6
- D) 8

<details>
<summary>Answer and explanation</summary>

**C) 6.**

An inner join emits one row per *matching pair*. Three users match a lead, and
the country they match has two lead rows, so the join returns `3 × 2 = 6` rows.
Section 4 of Exercise 6 computes this with the same numbers and also prints the
row count for every other join, which is the fastest way to see the difference.

Option A is the **semi-join** count: three users have a country that appears in
`leads`, so `WHERE country IN (SELECT country FROM leads)` returns 3. This is the
best wrong answer and the one people pick, because `IN` and `JOIN` look
interchangeable and test the same predicate.

Option B is the count of rows on the left side, which is what a `LEFT JOIN`
returns. A left join keeps every left row and NULL-pads the unmatched one.

Option D is a full outer join, which returns every row of both tables.

</details>

**Q11.** You need "all the tags used by any active user, each listed once". A
table of 10,000 users has 4,000 tags with duplicates, because there is no unique
constraint on the tag column. What does `COUNT(*)` give you, and what should it
give?

- A) 4,000 distinct tags — `COUNT(*)` deduplicates by definition
- B) 4,000, because the column is a `VARCHAR` and duplicates cannot occur
- C) 10,000 rows joined against the tag table, not a tag count at all
- D) 4,000 distinct tags, but only if you write `COUNT(DISTINCT tag)`

<details>
<summary>Answer and explanation</summary>

**D) 4,000 distinct tags, but only if you write `COUNT(DISTINCT tag)`.**

`COUNT(*)` counts rows, not distinct values, so without `DISTINCT` it counts the
joined rows, which is a different number again. The column being a `VARCHAR` does
not make it a key: a `VARCHAR` column can hold the same string as many times as
you like, which is why a primary key or a unique constraint is a *set-theoretic*
promise — the values of that column are pairwise distinct, so its image is a set
rather than a bag. Section 4 of Exercise 6 prints the bag-versus-set arithmetic
for exactly this situation: 8 rows, 3 distinct values, and a subtraction that
gives neither.

Option A is the misconception this question is about. `COUNT(*)` never
deduplicates; the deduplication is always something you ask for explicitly, and
the cost is a hash structure or a sort.

Option B is the "a string column is a set" error. Strings are values; a column of
strings is a bag of values.

Option C is right about `COUNT(*)` and wrong about the question. It is worth
noticing that the naive answer mixes a bag count with a set question, which is
the same class of error as Exercise 6's `4 + 4 - 2 = 6`.

</details>

## Subjective Questions

### Short Answer

**Q1. State the definitions of `$A \subseteq B$`, `$A \subsetneq B$`,
`$A \cup B$`, `$A \cap B$` and `$A \setminus B$`, and give one line of Python
for each.**

<details>
<summary>Answer</summary>

- `$A \subseteq B$` iff `$\forall x \in A, x \in B$`; Python: `A <= B`.
- `$A \subsetneq B$` iff `$A \subseteq B$` and `$A \neq B$`; Python:
  `A <= B and A != B` (or `A < B`, which means exactly that).
- `$A \cup B = \{x : x \in A \vee x \in B\}$`; Python: `A | B`.
- `$A \cap B = \{x : x \in A \wedge x \in B\}$`; Python: `A & B`.
- `$A \setminus B = \{x : x \in A \wedge x \notin B\}$`; Python: `A - B`.

The Python names are not arbitrary: `|`, `&` and `-` are the bitwise operators
lifted to sets, so the *bitmask* versions of these operations are the same
characters. That is not a coincidence, and it is why a set of 64 features fits
in one machine word.

</details>

**Q2. Prove `$|\mathcal{P}(A)| = 2^{|A|}$` for finite `$A$, and say in one
sentence why this is a statement about bijections rather than about upper
bounds.**

<details>
<summary>Answer</summary>

Write `$A = \{a_1, \ldots, a_n\}$`. Define `$\Phi : \mathcal{P}(A) \to
\{0,1\}^n$ by `$\Phi(S) = (\mathbb{1}_{a_1 \in S}, \ldots, \mathbb{1}_{a_n \in
S})$`. `$\Phi$ is injective` because a subset is determined by which `$a_i` it
contains, and surjective because any bit string picks out a subset by "include
`$a_i$` iff bit $i$ is 1". So `$\Phi$ is a bijection, and
`$|\mathcal{P}(A)| = |\{0,1\}^n| = 2^n$`.

It is a statement about bijections because a bijection transfers a count
*exactly*. An injection alone would give `$\le 2^n$`, and "at most $2^n$ subsets"
plus "at least $2^n$ subsets" is two arguments; the bijection is one argument
that gets both directions at once.

</details>

**Q3. What is the smallest positive integer $n$ such that a system with $n$
feature flags has more configurations than seconds in a year? What is the
smallest $n$ such that it has more configurations than there are stars in the
observable universe?**

<details>
<summary>Answer</summary>

A year is about 3.15 × 10⁷ seconds, and `2^25 = 33,554,432 > 3.15 × 10^7`, so
**$n = 25$**. Check `$n = 24`: `2^24 = 16,777,216 < 3.15 × 10^7`. So 25 flags
cross the one-second-per-configuration threshold.

There are roughly 10²² stars in the observable universe, and `2^74 ≈ 1.89 ×
10^22`, so **$n = 74$**.

The point of the question is the slope, not the answers. Each flag doubles the
space, so this is a difference of about 25 flags and about 50 flags between
"obviously fine" and "more than the world contains". Design discussions about
flag counts are usually about this slope.

</details>

**Q4. Give an injection from the reals to the subsets of the naturals, and an
injection from the subsets of the naturals back to the reals. What does
Cantor–Schröder–Bernstein conclude from those two?**

<details>
<summary>Answer</summary>

`$\mathbb{R} \to \mathcal{P}(\mathbb{N})$`: send $x$ to the set of positions at
which the binary expansion of $x$ (taken as the one that does not end in all 1s)
has a 1, equivalently `{n : floor(2ⁿ x) is even}`. It is injective because two
different reals have binary expansions differing at some position, hence floors
of different parity at the corresponding `n`.

`$\mathcal{P}(\mathbb{N}) \to \mathbb{R}$`: send `$S$` to
`$\sum_{n \in S} 4^{-n}$`. This lies in `[0, 1/3]` and is injective because base
4 with digits restricted to `{0, 1}` has no two representations of the same
number — the dangerous `0.1000… = 0.0111…` ambiguity needs a digit 3, which we
never use.

Cantor–Schröder–Bernstein concludes `$|\mathbb{R}| = |\mathcal{P}(\mathbb{N})|`
**without** constructing a bijection. Note what that buys: the two maps above are
each obviously injective, and the composite is an obvious mess. The theorem's
whole purpose is to let you skip it.

</details>

**Q5. A colleague says: "We hash every string into 64 buckets, so lookups are
O(1)." What is the correct statement, and what would you ask to check it?**

<details>
<summary>Answer</summary>

The correct statement: lookups are **expected** `$O(1)$` — the expected chain
length is `$n/64$`, constant with respect to $n$ — and the worst case is
`$O(n)$`, because with `$n > 64$` keys some bucket holds at least
`$\lceil n/64 \rceil$ of them, and an adversary who knows the hash function can
construct keys that all land in one bucket.

You would ask two things. First: what is the hash function, and is the seed
randomised per process (Python's `PYTHONHASHSEED`, SipHash in Rust's `HashMap`)?
Without randomisation the bad case is reachable by anyone who can submit keys.
Second: what happens at load factor 8 or above? Most implementations degrade or
rehash before that, and the degradation is where the O(1) quietly stops.

</details>

**Q6. When is `$A \setminus (B \cup C)$ equal to `$(A \setminus B) \setminus
C$`? When is `$A \cap (B \cup C)$ equal to `$(A \cap B) \cap C$`?**

<details>
<summary>Answer</summary>

The first pair is **always** equal, for all sets. Removing the union removes
everything in $B$ or in $C$; removing $B$ and then $C$ removes exactly the same
elements. This is the difference law `$A \setminus (B \cup C) = (A \setminus B)
\setminus C$`, and it is a special case of the fact that difference by a union
is sequential removal.

The second pair is equal only when `$B \cap C \subseteq A$`. If `$B \cap C$` has an
element outside $A$, the left-hand side is `$A` (the element is not in $A$ so it
does not remove anything) while the right-hand side is `$A \cap B \cap C`,
strictly smaller. The correct general law is distributivity:
`$A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$`.

</details>

### Long Answer

**Q1. Why is `$|\mathbb{N} \times \mathbb{N}| = |\mathbb{N}|$ a theorem while
`$|\mathbb{R}| > |\mathbb{N}|$` is also a theorem, and what does each one
require you to *produce*?**

<details>
<summary>Model answer</summary>

They look like the same shape of question — "how big is this set?" — and they
demand completely different evidence, because the sets are of different kinds.

For the first, "how big" cannot mean "counted to the end", since there is no
end. It has to mean *interchangeable in size*, and the evidence is an explicit
**bijection**: the Cantor pairing function, plus a verification that it round
trips. Both directions are needed. An injection one way (`(a, b) ↦ 2^a + 2^b`)
would show only `$|\mathbb{N} \times \mathbb{N}| \ge \aleph_0$`, which is true
and much weaker. So the burden is: write down a rule, and check that it hits
every target exactly once.

For the second, the evidence is a **refutation**: you assume a listing exists and
derive a contradiction in one line, with no counting. If `$D = \{a_n : a_n \notin
S_n\}` were `$S_k$`, then `$a_k$` would be in `$D$` exactly when it is in
`$S_k$`, and by construction exactly when it is not. Nothing to verify and nothing
to construct — that is why the diagonal argument is two sentences and the pairing
function is a page.

The asymmetry is worth internalising because it decides what a proof obligation
looks like. "Prove these two sets are the same size" and "prove this set is
bigger" are different *kinds* of task: the first is constructive and can be
verified by running code, the second is a contradiction and can be verified by
reading one line. And the composite fact — `$|\mathcal{P}(\mathbb{N})| > |N|$`
for *every* set $A$, finite or infinite — is what rules out a largest cardinality
and forces the aleph hierarchy, because the argument never uses the elements of
$A$ at all.

For a programmer the practical version is: when someone says "these two
collections behave the same", the deliverable is a rule with a checked round trip.
A claimed round trip that was only checked one way is an encoding, and an
encoding does not license any reasoning about size.

</details>

**Q2. `SELECT DISTINCT` and `UNION` are set operations. `UNION ALL` and a join
are not. Explain what breaks, why the breakage is hard to notice, and what design
decision removes it.**

<details>
<summary>Model answer</summary>

A relational table without a primary key is a **bag**: the same value may occur
many times. The set laws do not hold on bags. Specifically, the identity
`$|A \cup B| = |A| + |B| - |A \cap B|$` fails, because for bags "union" means
multiset sum, so `$\lvert A \cup B \rvert = \lvert A \rvert + \lvert B \rvert$` and
the correction term is wrong. Absorption and the inclusion–exclusion
formula fail too, because they assume each element is counted once. The Exercise 6
code computes the concrete failure: two tables whose bags have 4 rows each and
whose sets share 2 countries, giving `4 + 4 − 2 = 6`, when the true set union is 3
and the true bag union is 8.

It is hard to notice for three reinforcing reasons. The wrong number is
*plausible* — 6 is the kind of number a dashboard shows, so nobody asks. The code
looks right — iterating both collections and keeping what you have not seen is
exactly the set algorithm, applied to inputs that are not sets. And the error is
often conservative or anti-conservative by a small constant, so it reads as
drift rather than as a defect. The related join confusion is the same problem
wearing a different hat: `WHERE x IN (SELECT ...)` uses the right-hand table as a
set and returns 3 rows, while `JOIN` returns one row per matching pair and returns
6.

The design decision that removes it is to make the *container* a set as early as
possible and never to re-derive distinctness downstream. Concretely: build the
result with `set(...)` at the boundary where untrusted rows enter; let
`DISTINCT`/`UNION` be a property of the query rather than something you remember
to write; and never accumulate into a running sum or a bag when the quantity you
want is the number of distinct values. The idempotence argument is the reason
this is a design decision and not a patch: a set accumulator gives the same answer
when the same batch is processed twice, so a retry, a replay or an at-least-once
delivery cannot change the reported number. A bag accumulator or a running sum
changes on every redelivery — which is exactly the incident you will get at 3am.

The deeper point: every "count the distinct values" requirement is a set
requirement, and the moment it lands on a bag the arithmetic silently changes
kind. Naming the kind is most of the fix.

</details>

**Q3. A team says a 20-flag configuration system has 1,048,576 configurations
and they plan to test "the important ones". What would you ask them, and what
mathematics is relevant to answering well?**

<details>
<summary>Model answer</summary>

I would ask three questions. (1) *Important by what measure?* The set of
configurations that matter is a subset of `$\mathcal{P}(A)$` and there is no
canonical subset — importance has to be defined, and until it is, "the important
ones" is not a set anyone can enumerate. (2) *What is the constraint structure?*
If validity is monotone in the flags (enabling $X$ never lets you turn off a
requirement of $X$), then the valid configurations form an up-set, the minimal
valid configurations form an antichain, and testing just those minimal ones
covers every valid configuration. In Exercise 6 the team has 8 flags, 60 valid
configurations, and **2** minimal valid configurations — a factor of 30 — and
those two sit in the layer of size 1, nowhere near the middle. (3) *What is the
independence requirement?* If no test may be implied by another, the family is an
antichain and Sperner's theorem caps it at `$\binom{20}{10} = 184,756$`, which
is a real limit: no matter how cleverly they choose, at most 184,756 mutually
independent tests exist for 20 flags.

The relevant mathematics, then, is not counting — that part is one line. It is
(Sperner) what the largest permissible family is, (Lubell-style double counting)
why the middle layer is optimal, and (the up-set/minimal-element structure) how
to shrink 60 cases to 2 when the constraints are monotone. And the honest
warning: Sperner's bound is only a factor of `$\sqrt{n}$` better than `2^n`, so
the exponential is not going away. A 32-flag system has 4.3 billion
configurations and at most `$\binom{32}{16} ≈ 6.0 × 10^8` independent tests.
Constraint propagation, partition testing and coverage criteria do the real work;
the power set tells you what you are trying not to do.

</details>

**Q4. Why does the digit-interleaving argument prove that
`$\lvert \mathbb{R} \times \mathbb{R} \rvert = \lvert \mathbb{R} \rvert$` but
*not* that
`$\lvert \mathbb{N} \times \mathbb{N} \rvert = \lvert \mathbb{R} \rvert$`,
even though the argument looks identical in both cases? What breaks
if you try to reuse it?**

<details>
<summary>Model answer</summary>

The two arguments use different kinds of objects. In the reals case the
interleaving operates on *digit strings that are infinite and not eventually
periodic in a restricted way* — every real has an infinite expansion, and the
set of such strings is uncountable, so two of them interleave into a third
genuinely different from both. In the naturals case the interleaving operates on
*positions in a sequence*: pair `(i, j)` becomes index `2i + j` (or the diagonal
numbering). Both operations are bijections, so the mechanism looks the same, but
the conclusions are different statements about different sets.

What breaks if you reuse it: the proof that `$|\mathbb{N} \times \mathbb{N}| = |\mathbb{N}|$`
produces a bijection between pairs of naturals and naturals. To conclude
`$|\mathbb{N} \times \mathbb{N}| = |\mathbb{R}|$` you would have to compose it
with a bijection between naturals and reals, and no such bijection exists — that
is Cantor's diagonal argument, which applies to any proposed listing of
`$\mathbb{R}$` regardless of how the list was produced. So the reals are not in
the countable chain at all.

There is a second, subtler breakage inside the reals case, and it is the one
people trip over in practice: digit representations are not unique. `$0.1000\ldots_2
= 0.0111\ldots_2$`, so a naive interleave is not injective on the numbers whose
expansion terminates or eventually becomes all 1s. The fix is either to change
the base — use base 4 with digits restricted to `{0,1}`, where two distinct
strings can never denote the same number — or to fix the convention to "the
representation that does not end in all 1s", which every number has exactly one
of. Both fixes are about the *representation*, not about the interleave, which is
the general lesson: in this material most of the difficulty is in making a
description injective, not in the counting.

The computational reading: the space-filling curve is the geometric shadow of
`$|\mathbb{R}^2| = |\mathbb{R}|$`, and it is why you can render a 2D image by
following one 1D path. It is also why nobody renders it *that* way — the curve is
continuous and onto but has terrible locality, so adjacent pixels land far apart
along the path. Being the same cardinality as the line does not make two spaces
interchangeable in practice; it makes them *embeddable*.

</details>

**Q5. Your service deduplicates request IDs with a `list` and has started
dropping under load. Explain the set-theoretic diagnosis, why the profiler looks
like it does, and what the smallest safe change is.**

<details>
<summary>Model answer</summary>

The diagnosis is a membership-test complexity mismatch, and it is a set fact
wearing a data-structure costume. `if request_id in seen:` is the question "is
this element a member of the collection `seen`?" — a perfectly well-defined set
question. The answer's *cost* depends entirely on the container used to hold the
set. A Python `list` must compare the new value against every element until it
finds a match or exhausts the list, so each test is `$O(n)$` in the number of IDs
already seen, and the loop is `$O(n^2)$` overall. A `set` holds the same
collection as a hash index, so the same question costs one hash and about one
comparison: expected `$O(1)$`, giving `$O(n)$` overall.

Why the profiler looks the way it does: the hot line is the membership test, and
it looks cheap because it is one short expression. The quadratic behaviour only
appears as *input size grows*, so it survives every small-scale test and appears
as a latency curve rather than as a bug. And because the arithmetic is 1, 2, 3
rather than a wrong value, no assertion fires and nothing crashes — the service
just gets slower exactly when it is busiest, which is when the request rate is
highest and the collection is largest.

The smallest safe change is `seen = set()` instead of `seen = []`. It is safe
precisely because the *contents* are unchanged: the set of IDs seen after $k$
iterations is the same set, and the loop makes the same decisions. Only the cost
of the membership question changes. Two things to check while you are there: the
elements must be hashable (request IDs are strings, so they are — but if the list
ever held dicts, this change would raise `TypeError`), and if `seen` is ever
iterated expecting duplicates, that is a behaviour change, not a refactor.

The general lesson is the one in the lesson's last paragraph: `x in s` is a set
question whichever container you write it against. Turning the list into a set is
not tidying the code — it changes the cost of every lookup in it.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — Count the overlap in three overlapping sets, and get the
second count right too.** Three release candidates touched these endpoints:

- `$A$` (candidate 1): `/login`, `/cart`, `/search`, `/health`
- `$B$` (candidate 2): `/search`, `/profile`, `/health`, `/metrics`, `/cart`
- `$C$` (candidate 3): `/health`, `/metrics`, `/login`

Compute, showing every intermediate value: (a) `|A|`, `|B|`, `|C|`; (b) each of
`|A ∩ B|`, `|A ∩ C|`, `|B ∩ C|`, `|A ∩ B ∩ C|`; (c) `$|A ∪ B ∪ C|$` by
inclusion–exclusion, and then by listing the union; (d) the number of endpoints
hit by exactly one, exactly two and exactly three candidates, and check they sum
to `|A ∪ B ∪ C|`; (e) which endpoints candidate 2 could stop using without
affecting the other two; (f) both wrong answers — the naive sum of the three
sizes, and the sum with the pairwise corrections but no triple correction — and
say in which direction each is wrong.

<details>
<summary>Solution</summary>

```python
from itertools import combinations

# ---------------------------------------------------------------------------
# Q1: three release candidates hit overlapping sets of endpoints. Count the
# distinct endpoints, and find the arithmetic that gets it right.
# ---------------------------------------------------------------------------

A = {"/login", "/cart", "/search", "/health"}
B = {"/search", "/profile", "/health", "/metrics", "/cart"}
C = {"/health", "/metrics", "/login"}

print("=" * 74)
print("1. The three sets, and their sizes")
print("=" * 74)
for name, s in (("A (candidate 1)", A), ("B (candidate 2)", B), ("C (candidate 3)", C)):
    print(f"  {name:<18} |{name[0]}| = {len(s):<3} {sorted(s)}")
print()
print(f"  adding the three sizes gives {len(A) + len(B) + len(C)}, and there are")
print(f"  only {len(A | B | C)} distinct endpoints. The difference of")
print(f"  {len(A) + len(B) + len(C) - len(A | B | C)} is the number of repeat hits.")
print()

print("=" * 74)
print("2. Every pairwise and triple intersection")
print("=" * 74)
print(f"  A and B          : {len(A & B)}  {sorted(A & B)}")
print(f"  A and C          : {len(A & C)}  {sorted(A & C)}")
print(f"  B and C          : {len(B & C)}  {sorted(B & C)}")
print(f"  A and B and C    : {len(A & B & C)}  {sorted(A & B & C)}")
print()
na, nb, nc = len(A), len(B), len(C)
nab, nac, nbc, nabc = len(A & B), len(A & C), len(B & C), len(A & B & C)
print(f"  |A| + |B| + |C|                    = {na} + {nb} + {nc} = {na + nb + nc}")
print(f"  minus the pairwise intersections  = -{nab} -{nac} -{nbc} "
      f"= {na + nb + nc - nab - nac - nbc}")
print(f"  plus the triple intersection       = +{nabc} = {na + nb + nc - nab - nac - nbc + nabc}")
print(f"  the real size of A or B or C       = {len(A | B | C)}")
print()
print(f"  agreement: {na + nb + nc - nab - nac - nbc + nabc == len(A | B | C)}")
print()
print("  Why the +1 is needed. /health is in all three sets, so the raw sum")
print("  counts it three times. The three pairwise subtractions each remove one")
print("  of those, so after them it has been counted 3 - 3 = 0 times and has")
print("  fallen off the end. The triple term puts it back once, which is the")
print("  right number. That is the whole content of inclusion-exclusion: every")
print("  element must be counted exactly once, and its multiplicity is the")
print("  number of subsets of the sets that contain it.")
print()

print("=" * 74)
print("3. Partition the union by how many candidates hit each endpoint")
print("=" * 74)
EXACTLY_ONE = (A ^ B ^ C) - (A & B & C)
EXACTLY_TWO = ((A & B) | (A & C) | (B & C)) - (A & B & C)
EXACTLY_THREE = A & B & C
for label, s in (("hit by exactly one", EXACTLY_ONE),
                 ("hit by exactly two", EXACTLY_TWO),
                 ("hit by all three  ", EXACTLY_THREE)):
    print(f"  {label}: {len(s):<3} {sorted(s)}")
print(f"  total: {len(EXACTLY_ONE) + len(EXACTLY_TWO) + len(EXACTLY_THREE)}, "
      f"which must equal |A or B or C| = {len(A | B | C)}")
print(f"  agree: {len(EXACTLY_ONE) + len(EXACTLY_TWO) + len(EXACTLY_THREE) == len(A | B | C)}")
print()
print("  This is the partition the dashboard should show, because the three")
print("  numbers mean three different things. 'Hit by exactly one' is dead")
print("  weight. 'Hit by all three' is a shared dependency. 'Hit by exactly")
print("  two' is where the double counting actually lives.")
print()

print("=" * 74)
print("4. Which endpoints can candidate B drop without affecting the others?")
print("=" * 74)
SETS = {"A": A, "B": B, "C": C}
for name in ("A", "B", "C"):
    other_names = [n for n in ("A", "B", "C") if n != name]
    union_of_others = SETS[other_names[0]] | SETS[other_names[1]]
    droppable = SETS[name] - union_of_others
    print(f"  {name} - ({' or '.join(other_names)} union) = {len(droppable)} "
          f"{sorted(droppable)}")
print()
print("  Only candidate B can drop anything, and only /profile. A and C share")
print("  every endpoint they have with somebody else, so nothing may be removed")
print("  from them without coordinating.")
print()
print("  The subset question that actually gets asked is 'is everything A")
print("  touches also touched by somebody else', and the useful one is 'what")
print("  does A need that only B can supply':")
print(f"  A inside B or C ?          {A <= (B | C)}   (A's endpoints = "
      f"{len(A)}, covered by the others = {len(A - (B | C))} of them not)")
only_B_can_supply = A - C
print(f"  A - C                      {len(only_B_can_supply)}  "
      f"{sorted(only_B_can_supply)}")
print(f"  of those, is it inside B ? {only_B_can_supply <= B}")
print(f"  of those, is it inside C ? {only_B_can_supply <= C}")
print()

print("=" * 74)
print("5. The same three questions answered by brute force")
print("=" * 74)
all_endpoints = sorted(A | B | C)
counts = {e: (e in A) + (e in B) + (e in C) for e in all_endpoints}
print(f"  {'endpoint':<12} {'in A':>5} {'in B':>5} {'in C':>5} {'total hits':>11} "
      f"{'raw sum counts it':>20}")
for e in all_endpoints:
    hits = (e in A) + (e in B) + (e in C)
    print(f"  {e:<12} {str(e in A):>5} {str(e in B):>5} {str(e in C):>5} "
          f"{hits:>11} {hits:>20}")
print()
print(f"  sum of raw hits        : {sum(counts.values())}, the WRONG answer")
print(f"  sum of distinct        : {len(all_endpoints)}, the right one")
print(f"  overcount              : {sum(counts.values()) - len(all_endpoints)}, "
      f"which is sum(hits - 1) over the shared endpoints")
print()
print("  Two independent routes to 6. Inclusion-exclusion is the one you can do")
print("  in your head; the brute force is the one you can trust without")
print("  thinking, and it is what you would write to check a report that")
print("  somebody else computed.")
```

The two wrong answers in part (f) are worth keeping. The naive sum of 12 is twice
too big because it counts each shared endpoint once per candidate. The
pairwise-only correction gives 5, which is one too *small*, because it removes
`/health` three times when it should remove it twice. The direction of the error
tells you which mistake was made: too big means you forgot a correction, too
small means you over-corrected.

</details>

**[ ] Exercise 2 — Represent subsets as bit masks, then find the minimal valid
configurations of an 8-flag system.** (a) Write `to_mask` and `to_set` for a
list of 8 flag names, and check the round trip on all 256 masks. (b) Show that
`|P(A)| = 2^8 = 256` by enumerating, and print the table grouped by popcount so
the middle layer is visible. (c) Verify that the size-4 layer has
`$\binom{8}{4} = 70$` members. (d) A system has 32 flags; compute the number of
configurations and say how long exhaustive testing would take at ten tests per
second. (e) The requirement is: `audit` implies `tracing`, `tracing` implies
`retry`, `retry` implies `cache`, **and** at least one of `shadow`/`dryrun` must
be on. Find every valid configuration, then find the *minimal* valid ones, and
explain why testing only those is enough. (f) Explain why sampling the middle
layer instead would be a mistake.

<details>
<summary>Solution</summary>

```python
from itertools import combinations
from math import comb

# ---------------------------------------------------------------------------
# A subset of an n-element set is an n-bit string. Everything about the power
# set then becomes integer arithmetic, and the 2^n blow-up becomes something
# you can see coming rather than something you discover in production.
# ---------------------------------------------------------------------------

FLAGS = ["cache", "retry", "shadow", "beta", "audit", "tracing", "canary", "dryrun"]
N = len(FLAGS)
INDEX = {name: i for i, name in enumerate(FLAGS)}


def to_mask(subset):
    """The subset as an integer: bit i is set exactly when FLAGS[i] is in it."""
    mask = 0
    for i, name in enumerate(FLAGS):
        if name in subset:
            mask |= 1 << i
    return mask


def to_set(mask):
    """The integer back to a subset of flag names."""
    return {FLAGS[i] for i in range(N) if mask >> i & 1}


print("=" * 74)
print("1. The power set, enumerated by counting in binary")
print("=" * 74)
SMALL = FLAGS[:4]
print(f"  ground set: {SMALL}, |A| = {len(SMALL)}")
print(f"  {'mask':>5} {'binary':>8}  subset")
for mask in range(2 ** len(SMALL)):
    subset = {SMALL[i] for i in range(len(SMALL)) if mask >> i & 1}
    print(f"  {mask:>5} {mask:>08b}  {sorted(subset)}")
print()
print(f"  {2 ** len(SMALL)} rows, and the enumeration needed no cleverness at all:")
print("  the masks ARE the subsets, in a fixed order. That is why |P(A)| = 2^n")
print("  is a counting argument rather than a theorem with content -- there is")
print(f"  exactly one subset per yes/no decision per element, and {len(SMALL)}")
print(f"  decisions give 2^{len(SMALL)} = {2 ** len(SMALL)}.")
print()

print("=" * 74)
print("2. Every subset relation, as two integer operations")
print("=" * 74)
print("  A subset of B     :  a & b == a")
print("  A proper subset   :  a & b == a and a != b")
print("  A disjoint from B :  a & b == 0")
print("  A equal to B      :  a == b")
print()
print(f"  {'A':<26} {'B':<26} {'subset':>7} {'proper':>7}")
PROBES = [
    (set(), set()),
    (set(), {"cache"}),
    ({"cache"}, {"cache"}),
    ({"cache"}, {"cache", "retry"}),
    ({"cache", "retry"}, {"cache"}),
]
for a, b in PROBES:
    ma, mb = to_mask(a), to_mask(b)
    print(f"  {str(sorted(a)):<26} {str(sorted(b)):<26} "
          f"{str(ma & mb == ma):>7} {str(ma & mb == ma and ma != mb):>7}")
print()
print("  Row 1 and row 3 are the two that catch people. The empty set is a")
print("  PROPER subset of every non-empty set, which sounds wrong until you")
print("  remember it has no elements that could violate the containment. Row 3")
print("  is the other: A == B means A is a subset of B and NOT a proper subset.")
print()

print("=" * 74)
print("3. Counting subsets by size, and where the largest layer is")
print("=" * 74)
print(f"  {'n':>3} {'2^n':>6}  binomial(n, k) for k = 0 .. n")
for n in range(1, 9):
    row = ", ".join(str(comb(n, k)) for k in range(n + 1))
    print(f"  {n:>3} {2 ** n:>6}  {row}")
print()
middle = [mask for mask in range(2 ** N) if bin(mask).count("1") == N // 2]
print(f"  for our {N} flags the middle layer (size {N // 2}) has {len(middle)} members")
print(f"  out of {2 ** N}, and binom({N}, {N // 2}) = {comb(N, N // 2)}: "
      f"{len(middle) == comb(N, N // 2)}")
print()
print("  The row of counts is the binomial theorem, which is Lesson 22. The one")
print("  fact needed here is that the counts peak in the middle.")
print()

print("=" * 74)
print("4. The 2^n blow-up, as a number you can plan around")
print("=" * 74)
print(f"  {'flags':>6} {'configurations':>21} {'at 10 per second':>20}")
for n in (8, 12, 16, 20, 24, 32, 64):
    total = 2 ** n
    hours = total / 10 / 3600
    label = f"{hours:.1f} h" if hours < 1e6 else f"{hours / 24 / 365:,.0f} years"
    print(f"  {n:>6} {total:>21} {label:>20}")
print()
print("  A 32-bit configuration field holds 4.3 billion states, and no test")
print("  suite exists for it. Every place a program has 2^n reachable states")
print("  -- feature flags, subsets of a key set, hypercube automata, network")
print("  topologies -- you owe an argument for why you do not have to walk it.")
print()

print("=" * 74)
print("5. Feature selection as a search over the power set")
print("=" * 74)
# Requirement, in two parts:
#   (i)  audit implies tracing, tracing implies retry, retry implies cache
#   (ii) at least one of shadow / dryrun must be on
# Part (ii) is what makes the answer interesting: without it, turning
# everything off would be valid and it would be the only minimal case.
IMPLIES = {"audit": "tracing", "tracing": "retry", "retry": "cache"}
ONE_OF = ("shadow", "dryrun")


def is_valid(subset):
    return (all(IMPLIES[f] in subset for f in subset if f in IMPLIES)
            and any(f in subset for f in ONE_OF))


all_configs = [frozenset(to_set(mask)) for mask in range(2 ** N)]
valid = [c for c in all_configs if is_valid(c)]
# Minimal means no PROPER VALID SUBSET -- note the direction of the test.
# `c < other` would ask whether some valid set strictly contains c, which is
# true of almost everything and selects the wrong end of the poset entirely.
minimal = [c for c in valid if not any(other < c for other in valid)]
print("  requirement: audit => tracing => retry => cache, and")
print("               at least one of {shadow, dryrun} must be on")
print(f"  configurations in the power set : {len(all_configs)}")
print(f"  valid configurations            : {len(valid)}")
print(f"  invalid configurations          : {len(all_configs) - len(valid)}")
print()
print("  the MINIMAL valid configurations -- the ones you actually have to test:")
for c in sorted(minimal, key=sorted):
    print(f"    {sorted(c)}")
print(f"  there are {len(minimal)} of them, against {len(valid)} valid configurations.")
print()
covered = sum(1 for v in valid if any(m <= v for m in minimal))
print(f"  valid configurations containing at least one minimal one: {covered}")
print(f"  agree: {covered == len(valid)}")
print()
print("  The minimal valid configurations are pairwise incomparable -- an")
print("  antichain -- because if one were a subset of another, the smaller one")
print("  would not be minimal. And every valid configuration contains one of")
print(f"  them, so testing {len(minimal)} configurations covers all {len(valid)} valid ones. That")
print("  is the entire content of the power-set idea in a test plan.")
print()
print("  And note which layer they came from: the minimal valid configurations")
print(f"  have sizes {sorted({len(c) for c in minimal})}, i.e. they sit in the SMALL layers, not")
print(f"  the middle layer of size {N // 2}. Sampling the middle layer -- the natural")
print("  'representative sample' -- would miss every one of them.")
```

Part (e) is the part worth the exercise. Getting zero minimal configurations
would mean no test is required at all; getting 80 would mean you have to test
everything. The answer is 2, and the reason is that the constraints factor into
an implication chain (which is satisfied vacuously by having nothing on) and a
"at least one of" clause (which is not). Note also the direction of the
minimality test in the code: you must ask whether some *proper valid subset* of
the candidate exists, not whether some valid set *contains* it. Getting that
backwards selects the single largest valid configuration and you have learned
nothing.

</details>

**[ ] Exercise 3 — Audit an access check written as set operations.** The
requirement is: *a user may delete a project if their role is in
`ALLOWED_DELETE` and their account is not in `BLOCKED`*. With
`ALLOWED_DELETE = {"admin", "owner"}` and `BLOCKED = {"banned", "suspended"}`,
and a role universe of `{guest, member, admin, owner, banned, suspended}`:

(a) Write the requirement as a set of permitted roles and check it against the
two-list form `role in ALLOWED_DELETE and role not in BLOCKED`.
(b) Two buggy versions are written: `... or role not in BLOCKED` and
`... and role not in ALLOWED_DELETE`. For each, list the roles it wrongly admits
and the roles it wrongly denies, and say which failure direction is dangerous.
(c) Express each buggy version as a set operation and report its size, then
notice anything surprising about one of the sizes.
(d) Write a single regression assertion that fails for both buggy versions and
does not depend on which role the test suite happens to log in as.

<details>
<summary>Solution</summary>

```python
# ---------------------------------------------------------------------------
# An access check written as set operations, and the two ways of getting it
# wrong. Both bugs are real, both fail on a live system, and neither is caught
# by a test suite that only tests the roles the developer uses.
# ---------------------------------------------------------------------------

ROLES = {"guest", "member", "admin", "owner", "banned", "suspended"}
ALLOWED_DELETE = {"admin", "owner"}
BLOCKED = {"banned", "suspended"}

print("=" * 74)
print("1. The requirement, and the set it actually describes")
print("=" * 74)
print("  requirement: 'a user may delete a project if their role is allowed")
print("               and their account is not blocked'")
print()
PERMITTED = ALLOWED_DELETE - BLOCKED
print(f"  ALLOWED_DELETE - BLOCKED = {sorted(PERMITTED)}")
print(f"  |ALLOWED_DELETE| = {len(ALLOWED_DELETE)}, |BLOCKED| = {len(BLOCKED)}, "
      f"|A and B| = {len(ALLOWED_DELETE & BLOCKED)}")
print(f"  |A - B| = {len(ALLOWED_DELETE)} + {len(BLOCKED)} - "
      f"{len(ALLOWED_DELETE & BLOCKED)} = {len(PERMITTED)}")
print()
print("  The correct one-liner is a difference, and the two errors are a union")
print("  in place of the difference, or the difference computed with `and`")
print("  where it needed `or`.")
print()

print("=" * 74)
print("2. Three implementations, checked on every role")
print("=" * 74)


def wanted(role):
    """The requirement, read directly."""
    return role in ALLOWED_DELETE and role not in BLOCKED


def buggy_or(role):
    """'and' silently turned into 'or'. Fails OPEN."""
    return role in ALLOWED_DELETE or role not in BLOCKED


def buggy_and(role):
    """De Morgan applied backwards to the negation. Fails CLOSED."""
    return role not in ALLOWED_DELETE and role not in BLOCKED


print(f"  {'role':<11} {'required':>9} {'or-version':>11} {'and-version':>12}  verdict")
for role in sorted(ROLES):
    w, o, a = wanted(role), buggy_or(role), buggy_and(role)
    notes = []
    if o != w:
        notes.append(f"or-version {'ADMITS' if o else 'DENIES'}")
    if a != w:
        notes.append(f"and-version {'ADMITS' if a else 'DENIES'}")
    print(f"  {role:<11} {str(w):>9} {str(o):>11} {str(a):>12}  "
          f"{'; '.join(notes) if notes else 'agrees'}")
print()
print("  The or-version ADMITS guest and member: the blocked check is defeated")
print("  by having any unblocked role at all. The and-version ADMITS guest and")
print("  member too, and DENIES admin and owner: a permission check nobody can")
print("  pass. Both are one character, both compile, and the failure that")
print("  reaches an incident is the one that opens the door.")
print()

print("=" * 74)
print("3. The same two bugs, as set algebra")
print("=" * 74)
permitted_by_or = ALLOWED_DELETE | (ROLES - BLOCKED)
permitted_by_and = ROLES - (ALLOWED_DELETE | BLOCKED)
print(f"  required      accepts: {sorted(PERMITTED)}  (size {len(PERMITTED)})")
print(f"  or-version    accepts: {sorted(permitted_by_or)}  "
      f"(size {len(permitted_by_or)})")
print(f"  and-version   accepts: {sorted(permitted_by_and)}  "
      f"(size {len(permitted_by_and)})")
print()
print(f"  the or-version wrongly adds    : {sorted(permitted_by_or - PERMITTED)}")
print(f"  the and-version wrongly drops  : {sorted(PERMITTED - permitted_by_and)}")
print(f"  the and-version wrongly adds   : {sorted(permitted_by_and - PERMITTED)}")
print()
print(f"  Note the and-version: it accepts a set of size {len(permitted_by_and)}, which is")
print(f"  the SAME SIZE as the required set of {len(PERMITTED)}, and a completely")
print("  different set. Any test that checks a count rather than a membership")
print("  passes it. That is the argument for asserting on the set, not on len.")
print()
print("  Reading the bug as a set difference is what makes it diagnosable: you")
print("  can point at the exact elements that are in the wrong set, and they")
print("  are the roles nobody on the team uses.")
print()

print("=" * 74)
print("4. The fix, and a regression test that would have caught it")
print("=" * 74)
print("  correct code:")
print("      if role in ALLOWED_DELETE and role not in BLOCKED:")
print()
print("  correct code, as one set:")
print(f"      if role in {sorted(PERMITTED)}:")
print()
print("  the second is shorter and cheaper, and it is also a different design:")
print("  it puts the policy in one place instead of deriving it at every call")
print("  site. Every call site that re-derives the same difference from two")
print("  lists is a place the bug can be reintroduced.")
print()
failures = [r for r in sorted(ROLES) if wanted(r) != (r in PERMITTED)]
print(f"  roles where 'and the two lists' and 'in the difference' disagree: "
      f"{len(failures)}")
print(f"  agree on all roles: {not failures}")
print()
print("  A test that pins the set:")
print("    assert set(roles_allowed_to_delete()) == {'admin', 'owner'}")
print()
print("  That single assertion fails for both buggy versions, and it does not")
print("  care which role anybody happens to log in as while the suite runs.")
```

Part (c) is the finding to sit with: the second buggy version accepts a set of
the **same size** as the required one and a completely different set of roles.
Any test that asserts on a count rather than on membership passes it. That is
the strongest argument in this lesson for asserting on sets, and it is also why
"the test says the number is right" is weaker evidence than it sounds.

</details>

**[ ] Exercise 4 — Bags, `DISTINCT`, and join cardinalities.** You have
`users` (4 rows) and `leads` (4 rows) with the countries and scores given in the
code below, plus a stream of 7 login events for 3 distinct users.

(a) Compute the number of rows returned by `UNION ALL`, by `UNION`, and by the
mistaken formula `|A| + |B| − |A ∩ B|` applied to the two **bags**. Show all
three numbers and explain why the third is neither of the other two.
(b) Compute the distinct user count by streaming the events with a `set`, and
the bag count with `len`. Report the overcount.
(c) Build `Counter`-based bag union, intersection and difference, and check which
set laws survive: idempotence of union, commutativity of union, distributivity,
absorption, and the inclusion–exclusion formula.
(d) Compute the row counts of `users`, of a semi-join, of an inner join, of a
left join and of a full outer join, and explain why the semi-join and the inner
join differ by more than one.

<details>
<summary>Solution</summary>

```python
from collections import Counter

# ---------------------------------------------------------------------------
# A relational table without a uniqueness constraint is a BAG. Every count
# computed on a bag has to say which bag, and the set identities stop holding
# the moment duplicates exist. This is where DISTINCT comes from.
# ---------------------------------------------------------------------------

USERS = [
    {"id": 1, "name": "ana", "country": "NP", "plan": "free"},
    {"id": 2, "name": "bo", "country": "IN", "plan": "free"},
    {"id": 3, "name": "cy", "country": "US", "plan": "pro"},
    {"id": 4, "name": "di", "country": "NP", "plan": "free"},
]
LEADS = [
    {"country": "US", "score": 90},
    {"country": "NP", "score": 55},
    {"country": "US", "score": 20},
    {"country": "NP", "score": 10},
]
EVENTS = [
    ("ana", "login"), ("ana", "login"), ("ana", "cart"),
    ("bo", "login"), ("cy", "cart"), ("cy", "cart"), ("cy", "cart"),
]

print("=" * 74)
print("1. Two bag unions and one set union, and the number each produces")
print("=" * 74)
user_countries_bag = [r["country"] for r in USERS]
lead_countries_bag = [r["country"] for r in LEADS]
user_countries = set(user_countries_bag)
lead_countries = set(lead_countries_bag)
print(f"  users, as a bag: {user_countries_bag}")
print(f"  leads, as a bag: {lead_countries_bag}")
print()
print(f"  UNION ALL  (bags) : {len(user_countries_bag) + len(lead_countries_bag)} rows")
print(f"  UNION      (sets) : {len(user_countries | lead_countries)} rows  "
      f"{sorted(user_countries | lead_countries)}")
print(f"  the mistake      : {len(user_countries_bag)} + {len(lead_countries_bag)} - "
      f"{len(user_countries & lead_countries)} = "
      f"{len(user_countries_bag) + len(lead_countries_bag) - len(user_countries & lead_countries)}")
print()
print("  Look at the three numbers: 8, 3, and 6. The mistake subtracts the")
print("  number of SHARED DISTINCT values from the number of ROWS, which mixes")
print("  two different counts and lands on a number that is neither the bag")
print("  count nor the set count. |A union B| = |A| + |B| - |A and B| is a")
print("  statement about sets, and every term in it has to be a set size.")
print()

print("=" * 74)
print("2. DISTINCT, and what it costs")
print("=" * 74)
print(f"  {'event':<16} {'running DISTINCT count':>24}")
seen = set()
for i, (user, action) in enumerate(EVENTS, 1):
    seen.add(user)
    print(f"  {user + ': ' + action:<16} {len(seen):>24}")
print()
print(f"  rows processed : {len(EVENTS)}")
print(f"  distinct users  : {len(seen)}  {sorted(seen)}")
print(f"  overcount       : {len(EVENTS) - len(seen)}")
print()
print("  The distinct count is |the image of the projection|, and it is")
print("  maintained incrementally in one line. The bag count is len(), and")
print("  the difference between them is the entire subject of DISTINCT.")
print()

print("=" * 74)
print("3. Which bag laws break, and on which row")
print("=" * 74)


def bag(rows):
    return Counter(rows)


A = bag(["x", "x", "y"])
B = bag(["y", "y"])
SA, SB = set(A), set(B)                     # the same collections as sets
print(f"  A = {dict(A)}      as a set: {sorted(SA)}")
print(f"  B = {dict(B)}      as a set: {sorted(SB)}")
print()
LAWS = [
    ("A union A == A            (idempotent)",
     bag(list(A.elements()) * 2) == A, (SA | SA) == SA),
    ("|A union B| = |A| + |B| - |A and B|",
     sum((A + B).values()) == sum(A.values()) + sum(B.values())
     - sum((A & B).values()),
     len(SA | SB) == len(SA) + len(SB) - len(SA & SB)),
    ("A and B is the largest bag inside both",
     all((A & B)[k] <= min(A[k], B[k]) for k in set(A) | set(B)),
     (SA & SB) == SA & SB),
]
print(f"  {'statement':<40} {'on bags':>9} {'on sets':>9}")
for label, on_bag, on_set in LAWS:
    print(f"  {label:<40} {str(on_bag):>9} {str(on_set):>9}")
print()
print(f"  A union A as a bag: {dict(bag(list(A.elements()) * 2))}, every count doubled.")
print(f"  A union A as a set: {sorted(SA | SA)}, unchanged.")
print()
print("  Idempotence is the one that bites: A union A doubles every count, so")
print("  running the same batch twice through a bag-accumulating pipeline")
print("  doubles the reported totals. The set version is idempotent, which is")
print("  why the fix is always 'make it a set' and never 'subtract the")
print("  duplicates afterwards'.")
print()

print("=" * 74)
print("4. Joins, and the cardinality arithmetic behind them")
print("=" * 74)
semi = [u for u in USERS if u["country"] in lead_countries]
inner = [(u, l) for u in USERS for l in LEADS if u["country"] == l["country"]]
left_only = [u for u in USERS if u["country"] not in lead_countries]
print(f"  {'query':<46} {'rows':>5}")
print(f"  {'users':<46} {len(USERS):>5}")
print(f"  {'leads':<46} {len(LEADS):>5}")
print(f"  {'users SEMI JOIN leads (EXISTS)':<46} {len(semi):>5}")
print(f"  {'users INNER JOIN leads ON country':<46} {len(inner):>5}")
print(f"  {'users LEFT JOIN leads ON country':<46} {len(USERS):>5}")
print(f"  {'...left rows with no lead':<46} {len(left_only):>5}")
print()
print(f"  |users| = |semi| + |left with no match| -> "
      f"{len(USERS)} = {len(semi)} + {len(left_only)}")
print()
print(f"  Note the semi join returns {len(semi)} rows and the inner join returns "
      f"{len(inner)}.")
print("  Same predicate on the country, double the rows, because the inner")
print("  join emits one row per MATCHING PAIR and there are two NP leads and")
print(f"  two US leads: {len(inner)} = {len(semi)} left rows x 2 matches each.")
print()
print("  So the join cardinalities are:")
print(f"      semi  = {len(semi)}   (left rows whose key is in the right KEY SET)")
print(f"      inner = {len(inner)}   (one row per matching pair)")
print(f"      left  = {len(USERS)}   (all left rows, NULL-padded)")
print(f"      full  = {len(USERS) + len(LEADS)}   (all rows of both)")
print()
print("  The inner join is the one that surprises people, because `IN` and")
print(f"  `JOIN` look interchangeable and differ by a factor of {len(inner) // len(semi)} here.")
```

Part (a) is the one to remember: three plausible numbers, 8, 3 and 6, for what
sounds like one question. The third is the dangerous one, because it is what you
get by subtracting a *set* count from *bag* counts, and it produces a number that
looks like a count of something.

</details>

**[ ] Exercise 5 — Antichains, Sperner's bound, and the Dedekind numbers.**
(a) Define an antichain and write a pairwise checker for a family of subsets.
(b) For `$n = 0, 1, 2, 3, 4$`, enumerate **every** family of subsets of an
$n$-element set, count how many are antichains, and report the largest antichain
size. Compare the largest with `$\binom{n}{\lfloor n/2\rfloor}$` and with the
total number of families you had to try.
(c) Explain why the counts in (b) — 2, 3, 6, 20, 168 — are the Dedekind numbers
and why they are the number of monotone boolean functions on $n$ variables.
(d) Give the proof sketch of Sperner's theorem via the maximal-chain double count,
including why no chain can meet two members of the family.
(e) A test suite on 8, 12, 16 and 20 flags may not contain a test implied by
another. Give the maximum size of such a suite for each, and say what fraction of
the power set that is.

<details>
<summary>Solution</summary>

```python
from itertools import combinations
from math import comb

# ---------------------------------------------------------------------------
# An antichain is a family of subsets in which no member contains another. Two
# facts are worth having: the largest antichain has binom(n, floor(n/2))
# members (Sperner), and the number of antichains in an n-element set is the
# nth Dedekind number, which grows faster than 2^(2^n) comparisons would
# suggest and has no closed form.
#
# Both are checkable by exhaustion for small n, which is what this block does.
# ---------------------------------------------------------------------------


def power_set(elements):
    return [frozenset(c) for r in range(len(elements) + 1)
            for c in combinations(elements, r)]


def is_antichain(family):
    members = list(family)
    for i, a in enumerate(members):
        for b in members[i + 1:]:
            if a <= b or b <= a:
                return False
    return True


def all_antichains(subsets):
    """Every antichain among `subsets`, by exhaustively trying every family.

    There are 2^len(subsets) families, which is 65536 for a 4-element set and
    4 billion for a 5-element one -- which is itself the lesson."""
    total = len(subsets)
    for choice in range(2 ** total):
        family = [subsets[i] for i in range(total) if choice >> i & 1]
        if is_antichain(family):
            yield family


print("=" * 74)
print("1. Sperner's bound, verified by exhaustion for n = 0 .. 4")
print("=" * 74)
print(f"  {'n':>2} {'subsets':>8} {'families tried':>15} {'antichains':>11} "
      f"{'largest':>8} {'binom(n,n//2)':>15} {'agree':>6}")
DEDEKIND = []
for n in range(0, 5):
    subsets = power_set(list(range(n)))
    biggest, count_of_antichains = 0, 0
    for family in all_antichains(subsets):
        count_of_antichains += 1
        biggest = max(biggest, len(family))
    DEDEKIND.append(count_of_antichains)
    predicted = comb(n, n // 2)
    print(f"  {n:>2} {len(subsets):>8} {2 ** len(subsets):>15} "
          f"{count_of_antichains:>11} {biggest:>8} {predicted:>15} "
          f"{str(biggest == predicted):>6}")
print()
print("  The third column is the cost: 65536 families for four elements, and")
print("  2^32 = 4294967296 for five. Exhaustion proves the bound for four")
print("  elements and is hopeless at five, which is why Sperner's theorem is")
print("  proved by double counting rather than by trying.")
print()
print("  The Dedekind numbers in the antichains column -- 2, 3, 6, 20, 168 --")
print("  are the number of monotone boolean functions on n variables, because")
print("  a monotone function is exactly the characteristic function of an")
print("  antichain. They are the numbers behind circuit lower bounds, and")
print("  nobody has a closed form for them.")
print()

print("=" * 74)
print("2. Why the middle layer wins")
print("=" * 74)
print("""
    Sperner's theorem:  no antichain in P(A) is bigger than the largest layer,
                       which is the layer of size binom(n, floor(n/2)).

    The counting argument is one paragraph. Take an antichain F and count, for
    each member S of F, the number of maximal chains

        { }  <  {a1}  <  {a1, a2}  <  ...  <  A

    that pass through S. If |S| = k then S sits on exactly k! (n - k)! chains,
    and since A has n! maximal chains in total, the chain through S is shared
    with k! (n - k)! other subsets of A. No other member of F can be on that
    chain, or the two would be comparable. So

        sum over S in F of 1 / binom(n, |S|)   <=   1

    and every term is at least 1 / binom(n, floor(n/2)), because binom(n, k) is
    largest at the middle. Hence |F| <= binom(n, floor(n/2)), and taking the
    middle layer itself shows the bound is attained.
""")
print("  Here is the middle layer for n = 5, checked to be an antichain:")
MIDDLE = [s for s in power_set(range(5)) if len(s) == 2]
print(f"    size {len(MIDDLE)}, is an antichain: {is_antichain(MIDDLE)}")
print(f"    binom(5, 2) = {comb(5, 2)}, agree: {len(MIDDLE) == comb(5, 2)}")
print()
print("  And here is a family that is NOT an antichain, which is what a")
print("  careless implementation produces:")
NOT_ANTICHAIN = [frozenset({1}), frozenset({1, 2})]
print(f"    {[sorted(s) for s in NOT_ANTICHAIN]}")
print(f"    is an antichain: {is_antichain(NOT_ANTICHAIN)}, because "
      f"{sorted(NOT_ANTICHAIN[0])} is inside {sorted(NOT_ANTICHAIN[1])}")
print()
print("  The witness is always a pair: an antichain fails exactly when some")
print("  pair of members is comparable, so testing every PAIR is enough and")
print("  testing every triple is wasted work. That is the practical content")
print("  of the definition, and it is why the checker above is quadratic in")
print("  the family size rather than exponential.")
print()

print("=" * 74)
print("3. Where an antichain is the right object")
print("=" * 74)
print("""
    A test suite that is not allowed to contain a test implied by another one
    is an antichain: no test's flag configuration is a subset of another's.
    Maximal such suites are the antichains of the power set of your flags,
    and Sperner says the biggest one you can possibly have has
    binom(n, n//2) members -- so a 20-flag system admits at most 184756
    independent tests, no matter how they are chosen.

    The same bound appears in monotone circuit lower bounds: a circuit whose
    gates are all AND/OR computes a monotone function, and a function with a
    large antichain of minimal true inputs needs a large circuit.
""")
for n in (8, 12, 16, 20, 24):
    print(f"  n = {n:>3}: at most {comb(n, n // 2):>10} independent tests, "
          f"out of {2 ** n:>13} configurations")
print()
print("  The ratio is the interesting column: binom(n, n//2) is about")
print("  2^n / sqrt(pi n / 2), so the bound saves a factor of sqrt(n) -- a real")
print("  saving, but not the exponential saving people usually imagine when")
print("  they say 'exhaustive'.")
```

The column to watch in part (b) is the third one. Verifying Sperner's bound for
four elements takes 65,536 families; for five elements it takes 4.3 billion,
which is why the theorem is proved by counting chains rather than by trying. And
the antichain counts in part (c) grow faster than the family counts do not — the
Dedekind numbers are `$2^{2^n}$` in the denominator, not in the numerator, and
they have no closed form, which is why monotone circuit lower bounds are hard.

</details>

**[ ] Exercise 6 — Build the bijections, and prove that `$\mathcal{P}(\mathbb{N})$`
is not countable.** (a) Write the Cantor pairing function and its inverse, and
verify both directions of the round trip on a large window. Print the diagonals
so the numbering is visible. (b) Write a bijection `$\mathbb{N} \to \mathbb{Z}$`
and verify it. (c) Enumerate the rationals by diagonal order, keeping lowest
terms and dropping duplicates, then verify on a window that every rational in the
window appears and none appears twice. (d) Write the finite version of Cantor's
diagonal: list the first `$n$` subsets of `$\{0, \dots, n-1\}$`, build
`$D = \{i : i \notin S_i\}$`, and check `$D$` is not in the list. Then state
precisely why the finite version does **not** prove the theorem and what the real
theorem adds.

<details>
<summary>Solution</summary>

```python
from itertools import count
from math import isqrt

# ---------------------------------------------------------------------------
# Three explicit bijections, each verified by round trip, and one set that is
# provably larger than all of them.
# ---------------------------------------------------------------------------


def pairing(a, b):
    """Cantor pairing: N x N -> N, a bijection. Lay the pairs out on the
    diagonals of constant a + b and number the diagonals in turn."""
    s = a + b
    return s * (s + 1) // 2 + b


def unpairing(n):
    """The inverse of `pairing`, with no floating point anywhere."""
    s = (isqrt(8 * n + 1) - 1) // 2
    offset = n - s * (s + 1) // 2
    return s - offset, offset


def zigzag(n):
    """N -> Z: 0, -1, 1, -2, 2, -3, 3, ..."""
    return n // 2 if n % 2 == 0 else -(n + 1) // 2


def unzigzag(z):
    return 2 * z if z >= 0 else -2 * z - 1


print("=" * 74)
print("1. N x N -> N, and the round trip")
print("=" * 74)
print(f"  {'d = a + b':>9}   the diagonal")
for d in range(5):
    print(f"  {d:>9}   " + "  ".join(
        f"({a},{d - a})->{pairing(a, d - a)}" for a in range(d + 1)))
print()
print(f"  {'n':>4} {'unpairing(n)':>16} {'round trip':>12}")
for n in range(12):
    a, b = unpairing(n)
    print(f"  {n:>4} {str((a, b)):>16} {str(pairing(a, b) == n):>12}")
print()
ok = all(pairing(*unpairing(n)) == n for n in range(20000))
ok2 = all(pairing(a, b) == unpairing(pairing(a, b)) for a in range(200)
          for b in range(200))
print(f"  pairing(unpairing(n)) == n for all n < 20000       : {ok}")
print(f"  unpairing(pairing(a, b)) == (a, b) for a, b < 200  : {ok2}")
print()
print("  Two directions checked, so it is a bijection rather than a clever")
print("  encoding. That is the difference between 'these two sets look alike'")
print("  and '|N x N| = |N|', and only the second one is a statement.")
print()

print("=" * 74)
print("2. N -> Z, and the round trip")
print("=" * 74)
print(f"  {'n':>3} {'zigzag(n)':>11} {'unzigzag':>10}")
for n in range(10):
    print(f"  {n:>3} {zigzag(n):>11} {unzigzag(zigzag(n)):>10}")
print()
print(f"  round trip holds for n < 100000: "
      f"{all(unzigzag(zigzag(n)) == n for n in range(100000))}")
print(f"  the image covers every integer in [-5000, 5000]: "
      f"{set(zigzag(n) for n in range(10001)) == set(range(-5000, 5001))}")
print()
print("  Z looks bigger than N because it has negatives. The map shows it does")
print("  not: each negative is paid for by a positive, and the positives are")
print("  already there.")
print()

print("=" * 74)
print("3. Q, by diagonal enumeration")
print("=" * 74)


def gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def rationals_in_order(limit):
    seen, out = set(), []
    for n in count():
        p, q = unpairing(n)
        if q == 0 or gcd(p, q) != 1:
            continue
        for frac in ((p, q), (-p, q)):
            if frac not in seen:
                seen.add(frac)
                out.append(frac)
                if len(out) == limit:
                    return out
    return out


ORDER = rationals_in_order(20)
print("  the first 20 distinct rationals:")
for i in range(0, 20, 5):
    print("    " + "  ".join(f"{p}/{q}" for p, q in ORDER[i:i + 5]))
print()
# The property that matters: every rational in a window appears, and no
# rational appears twice.
FULL = rationals_in_order(500)
window = {(p, q) for p in range(-6, 7) for q in range(1, 7) if gcd(p, q) == 1}
produced = set(FULL)
print(f"  rationals p/q with |p| <= 6, 1 <= q <= 6, in lowest terms: {len(window)}")
print(f"  how many of them appear in the first 500 of the enumeration: "
      f"{len(window & produced)}")
print(f"  all of them appear: {window <= produced}")
print(f"  no duplicates in the first 500: {len(FULL) == len(produced)}")
print()
print("  Every p/q in lowest terms has q > 0, so (|p|, q) is a pair of naturals,")
print("  so it has an index from the pairing function, so it turns up at a")
print("  FINITE position in this list. That is the whole proof that Q is")
print("  countable, and it is the same shape as the proof that N x N is")
print("  countable: a pairing function plus a filter that removes duplicates")
print("  without removing values.")
print()

print("=" * 74)
print("4. Cantor's diagonal, in the finite version and in the real one")
print("=" * 74)
N = 8
listed = [frozenset(i for i in range(N) if mask >> i & 1) for mask in range(N)]
diagonal = frozenset(i for i in range(N) if i not in listed[i])
print(f"  the first {N} subsets of {{0 .. {N - 1}}}, in mask order:")
for mask, s in enumerate(listed):
    print(f"    S_{mask} = {sorted(s)}")
print()
print(f"  D = {{ i : i not in S_i }} = {sorted(diagonal)}")
print(f"  D in the list? {diagonal in listed}")
print()
print("  If D were S_k then, at element k, D would contain k exactly when")
print("  S_k does, and also exactly when it does not. One line, no arithmetic.")
print()
print("  The finite table shows the mechanism only. The theorem lists the")
print("  subsets of N as S_0, S_1, S_2, ... indexed by ALL natural numbers, and")
print("  builds D = { i : i not in S_i } as a subset of N. The same one-line")
print("  contradiction applies, and it is not avoided by the missing last row,")
print("  because there is no last row. So no list of all subsets of N exists:")
print("      |P(N)| > |N|.")
print()
print("  Which is the punchline of the lesson's infinite half:")
print("      |N| = |Z| = |Q| = |N x N|          (all countably infinite)")
print("      |P(N)| = |R|, and |R| is strictly bigger than all of those.")
print()
print("  The naturals sit inside the reals -- every n is a real -- and the")
print("  diagonal says the reals are not exhausted by them, however far you")
print("  enumerate. Which is the honest reason a program can never check 'all'")
print("  of something: the only infinite set a finite machine can hold all of")
print("  is the countable one, and even there only by giving up on order.")
```

The gap between the finite table and the real theorem is the whole lesson about
infinite sets in miniature. The finite table escapes the *first* `$n$` subsets;
the real theorem escapes *all* of them, because the list is indexed by all
natural numbers and has no last row. So "I checked 8 cases and the diagonal was
missing" is evidence, not proof — exactly the lesson of
[Lesson 14](14_mathematical_induction.md) about tables, arriving through a
different door.

</details>

**[ ] Challenge 7 — Bag algebra, and the smallest input that breaks each law.** (a)
Implement bag union, intersection and difference over `Counter`s, with
`support()` giving the underlying set. (b) For each of these six set laws —
inclusion–exclusion for the union, commutativity of union, idempotence of
intersection, absorption, the difference law `A \ (A ∩ B) = A \ B`, and
distributivity — report whether it holds on bags, and check the same law on sets
as a control. (c) For every law that fails, search for the *smallest* pair of
bags over the alphabet `{a, b}` that breaks it, and print it. (d) A metrics
pipeline accumulates `rows in this batch` into an accumulator and reports
`|users ∪ leads|` as `len(users_rows) + len(leads_rows) − len(set(users_rows) &
set(leads_rows))` where 4 + 4 − 2 = 6, the true set union is 3, and the true bag
union is 8. Explain why the reported number survives review, and give the design
change that makes the metric correct *and* immune to a redelivered batch.

<details>
<summary>Solution</summary>

```python
from collections import Counter
from itertools import combinations

# ---------------------------------------------------------------------------
# A challenge with two parts:
#
#   1. Implement bag set algebra, find every set law that breaks, and give the
#      smallest input that breaks each one.
#   2. Build a query planner that only knows about SETS, and show why it
#      silently produces a wrong row count on a bag.
# ---------------------------------------------------------------------------

print("=" * 74)
print("1. Bag algebra, and which set laws survive")
print("=" * 74)


def bag(rows):
    return Counter(rows)


def bag_union(x, y):
    return x + y


def bag_intersection(x, y):
    """The largest bag inside both: the minimum multiplicity."""
    return Counter({k: min(x[k], y[k]) for k in set(x) & set(y)})


def bag_difference(x, y):
    return Counter({k: v - y[k] for k, v in x.items() if v > y[k]})


def support(x):
    """The underlying set: what DISTINCT would give you."""
    return set(x)


LAWS = [
    ("|A union B| = |A| + |B| - |A and B|",
     lambda x, y: sum(bag_union(x, y).values())
     == sum(x.values()) + sum(y.values()) - sum(bag_intersection(x, y).values()),
     lambda x, y: len(support(x) | support(y))
     == len(support(x)) + len(support(y)) - len(support(x) & support(y))),
    ("A union B = B union A  (commutative)",
     lambda x, y: bag_union(x, y) == bag_union(y, x),
     lambda x, y: (support(x) | support(y)) == (support(y) | support(x))),
    ("A and A = A  (idempotent)",
     lambda x, y: bag_intersection(x, x) == x,
     lambda x, y: (support(x) & support(x)) == support(x)),
    ("A union (A and B) = A  (absorption)",
     lambda x, y: bag_union(x, bag_intersection(x, y)) == x,
     lambda x, y: (support(x) | (support(x) & support(y))) == support(x)),
    ("A - (A and B) = A - B",
     lambda x, y: bag_difference(x, bag_intersection(x, y)) == bag_difference(x, y),
     lambda x, y: (support(x) - (support(x) & support(y))) == (support(x) - support(y))),
]

LAWS3 = [
    ("A union (B and C) = (A union B) and (A union C)  (distributive)",
     lambda x, y, z: bag_union(x, bag_intersection(y, z))
     == bag_intersection(bag_union(x, y), bag_union(x, z)),
     lambda x, y, z: (support(x) | (support(y) & support(z)))
     == ((support(x) | support(y)) & (support(x) | support(z)))),
]

PAIRS = [
    (bag(["a", "a", "b"]), bag(["b", "b"])),
    (bag(["a", "b"]), bag(["b", "c"])),
    (bag(["a", "a", "a"]), bag(["a"])),
    (bag(["x"]), bag(["y", "y", "y"])),
]


def law_holds(law, pairs):
    return all(law(x, y) for x, y in pairs)


print(f"  {'set law':<62} {'bags':>6} {'sets':>6}")
for label, on_bag, on_set in LAWS:
    bag_ok = all(on_bag(x, y) for x, y in PAIRS)
    set_ok = all(on_set(x, y) for x, y in PAIRS)
    print(f"  {label:<62} {str(bag_ok):>6} {str(set_ok):>6}")
for label, on_bag, on_set in LAWS3:
    bag_ok = all(on_bag(x, y, z) for x, y in PAIRS for z, _ in PAIRS)
    set_ok = all(on_set(x, y, z) for x, y in PAIRS for z, _ in PAIRS)
    print(f"  {label:<62} {str(bag_ok):>6} {str(set_ok):>6}")
print()
print("  All six hold for sets, so the sets column is all True by construction")
print("  -- which is exactly what makes it useful as a control.")
print("  The bags column is the interesting one.")
print()

print("=" * 74)
print("2. The smallest input that breaks each law")
print("=" * 74)


def smallest_witness(law, alphabet=("a", "b"), max_len=2):
    """The shortest, then lexicographically first, pair of bags that breaks it."""
    rows = [r for k in range(1, max_len + 1) for r in combinations(alphabet, k)]
    for x in rows:
        for y in rows:
            if not law(bag(x), bag(y)):
                return x, y
    return None


for label, on_bag, _ in LAWS:
    witness = smallest_witness(on_bag)
    if witness is None:
        print(f"  {label}")
        print("      no witness with rows of length 1 or 2")
    else:
        x, y = witness
        print(f"  {label}")
        print(f"      A = {list(x)}, B = {list(y)}")
        print(f"      A union B = {dict(bag_union(bag(x), bag(y)))}")
print()

print("=" * 74)
print("3. A planner that knows only about sets, run against a bag")
print("=" * 74)
# The planner's model: 'these are the countries we have users in'. It stores a
# set, so it is right about every SET question and wrong about every BAG one.
users_rows = ["NP", "IN", "US", "NP"]
leads_rows = ["US", "NP", "US", "NP"]

planner_distinct = set(users_rows) | set(leads_rows)
planner_inclusion_exclusion = (len(users_rows) + len(leads_rows)
                               - len(set(users_rows) & set(leads_rows)))
truth_bag = len(users_rows) + len(leads_rows)
truth_set = len(planner_distinct)

print(f"  {'what is being reported':<44} {'number':>7}")
print(f"  {'rows actually stored (bag count)':<44} {truth_bag:>7}")
print(f"  {'distinct values (set count)':<44} {truth_set:>7}")
print(f"  {'what the planner reports':<44} {planner_inclusion_exclusion:>7}")
print()
print(f"  the planner is right about the question it was asked -- |A or B| for")
print(f"  the SETS A and B -- because that is {truth_set}, and its answer of")
print(f"  {planner_inclusion_exclusion} is a different quantity computed from")
print("  inputs of two different kinds.")
print()
print(f"  Is the planner's answer even reachable as a real count? Yes: it is")
print(f"  the number of rows you get from a query that dedupes the shared")
print(f"  values only. That is why the bug survives review -- it returns a")
print("  plausible small number rather than an obvious nonsense one.")
print()
print("  The fix is one line, and it is a design decision rather than a patch:")
print()
print("      reported = len(set(users_rows) | set(leads_rows))")
print()
print("  or, better, make the pipeline carry sets from the start:")
print("      seen_countries |= set(rows_in_this_batch)")
print()
print("  A pipeline that accumulates into a set is idempotent, so re-running a")
print("  batch cannot change the answer. A pipeline that accumulates into a bag")
print("  or a running sum can, and it will, on the retry.")
print()
bag_accumulate = Counter()
for batch in (["NP", "IN"], ["NP", "IN"]):        # a redelivered batch
    bag_accumulate += Counter(batch)
set_accumulate = set()
for batch in (["NP", "IN"], ["NP", "IN"]):
    set_accumulate |= set(batch)
print(f"  bag accumulator after the same batch twice : {dict(bag_accumulate)}")
print(f"  set accumulator after the same batch twice: {sorted(set_accumulate)}")
print(f"  The bag reports {sum(bag_accumulate.values())} rows for "
      f"{len(set_accumulate)} distinct values, and it changed when the batch")
print("  was delivered twice. The set reports 2 both times, which is the")
print("  number of distinct values and the number there should be.")
```

The last test is the one that decides whether you have fixed the bug or the
symptom. A pipeline that accumulates into a set is idempotent, so replaying a
batch cannot change the answer; a pipeline that accumulates into a bag or a
running sum changes on every redelivery, and at-least-once delivery is the
default in every system you will ever work in. The power-set idea is doing real
work here: the set of distinct countries is a mathematical object that does not
care how many times you were told about it.

</details>

## Summary
- The correction formula is `$|A ∪ B| = |A| + |B| − |A ∩ B|$`, and it
  degenerates to addition precisely when `$A ∩ B = ∅$`. For three sets there
  are seven terms, and dropping the triple term makes the answer one too
  *small*.
- `$|\mathcal{P}(A)| = 2^{|A|}$`, and it is a bijection argument rather than
  an upper bound. A subset of an `$n$`-element set is an `$n$`-bit string,
  which is why bitmask subset tests cost one instruction.
- `$|A \times B| = |A| \cdot |B|$`: pairs are counted with a product, unions
  with a sum-minus-correction. Confusing the two is how a join of two large
  tables "returns 1M rows".
- Hash membership is expected `$O(1)$` because the expected chain length is
  `$n/m$`, and only an *expectation* because pigeonhole forces some bucket to
  hold at least `$\lceil n/m \rceil$` keys.
- `$|\mathbb{N}| = |\mathbb{Z}| = |\mathbb{Q}| = |\mathbb{N} \times
  \mathbb{N}|$`, each proved by an explicit bijection that round-trips. Pairs
  of naturals are countable; the reals are not.
- `$|\mathcal{P}(A)| > |A|$` for every set $A$, by a one-line contradiction
  with no counting in it. So `$|\mathbb{R}| > |\mathbb{N}|$ and there is no
  largest set. Do **not** confuse this with `$|\mathbb{R} \times \mathbb{R}| =
  |\mathbb{R}|$ — the interleaving result is about reals, not naturals.
- Cantor–Schröder–Bernstein: injections both ways give equal cardinality with
  no bijection required. It says nothing new for finite sets and is
  indispensable for infinite ones.
- A database table without a unique constraint is a **bag**, and the set laws
  do not hold on bags. `DISTINCT`, `UNION` and `EXISTS` are where the set-ness
  is restored, and a bag accumulator changes its answer on every redelivered
  batch.

## Next

[Lesson 20 — Counting Principles](../part02_discrete_combinatorics/20_counting_principles.md)
turns `$|\mathcal{P}(A)| = 2^{|A|}$ into a general counting method: the rule of
product, the rule of sum, and the bijection argument this lesson used for
`|N × N| = |N|` named as a technique. It assumes you can say whether two sets
have the same size and why.
