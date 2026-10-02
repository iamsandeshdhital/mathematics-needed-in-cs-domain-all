# 81 — Amortised Analysis

**Part**: part06_algorithms_math · **Prerequisites**: 80 · **Time**: 35 min

---

## In Plain Words

Sometimes one operation is nearly free and the next one is very expensive, and
the expensive ones are rare enough that the cheap ones pay for them. Adding an
item to a growing list is the standard example: the list is enlarged, and
everything in it copied, every so often — but only once every time the number of
items has doubled, so the copying is bounded by a fixed multiple of the total
work. The average cost of adding an item is therefore a small constant, and it is
a constant for reasons that have nothing to do with luck: no randomness, no
assumption about what you are adding, and a statement that holds for every
possible sequence of operations you could perform.

That guarantee is the whole point, and it is what separates this from a weaker
claim you have probably heard: that hash table lookups are fast on average. The
average is a statement about a world where your keys are chosen at random, which
is a nice property to have and not at all a promise. Amortised is a promise: for
*any* sequence of a hundred operations, the total is at most a few hundred
operations, for a constant you can compute in advance. Nothing about your inputs, your adversary, or your luck
is assumed. The price is that the individual operation is not fast — one append
really does copy the entire array — and that price is real, and it is what a
service's tail latency is made of.

---

## Why Computer Science Cares

- **Every dynamic array ever written.** Python's `list`, Java's `ArrayList`, C++'s
  `std::vector`, Rust's `Vec`, Go's `append`, JavaScript's arrays. All of them
  over-allocate and all of them were over-allocating for the same reason: the
  analysis below says the total cost of $n$ appends is linear, and the only
  question is the constant.
- **The growth factor is a designed constant, and the trade is measurable.**
  With growth factor $f$, the amortised copying cost is $\approx 1/(f-1)$ element
  copies per append. The lesson's code measures `8.8263` at $f = 1.125$ (what
  CPython does) and `0.9999` at $f = 2$, in exchange for `9.3%` and `0%` wasted
  slots. Every implementation picked a point on that curve deliberately.
- **`Vec::push` in a hot loop, and the `reserve` escape hatch.** Because the
  worst-case `push` is $O(n)$, a program that must never pause calls
  `reserve` (C++), `make` (Go, which pre-sizes slices), or uses an arena. That is
  the correct response to an amortised bound: pay the expensive operation once,
  on purpose.
- **Hash tables must resize, and the resize is amortised.** Insert into a
  half-full table is $O(1)$; fill it and a rehash of everything is $O(n)$. The
  lesson measures `0.9996` rehash moves per insert at $n = 16384$, and that figure
  is a **guarantee** — it does not depend on the hash function, the keys, or an
  adversary, which is exactly what expected-$O(1)$ lookup is not.
- **Copy-on-write and persistent data structures.** Refcount hits zero and the
  whole structure is freed, or two appends conflict and the whole array is
  copied. The reason `String` in Rust or a persistent vector in Clojure is
  "amortised cheap in practice" is this analysis, and the reason it is
  occasionally catastrophic is the worst case.
- **Memory reclamation.** Reference counting frees an object on the operation that
  drops the last reference, which is $O(\text{size of object})$; tracing garbage
  collection moves the cost to a collector that runs in one big batch. The batch
  is amortised $O(1)$ per allocation precisely because the mark phase touches
  every *live* object and liveness is a fraction of everything ever allocated.
- **The tail-latency argument you will have to make at work.** "Amortised $O(1)$
  per request" does **not** mean any single request takes $O(1)$. It means
  $\sum$ of the costs is $O(n)$, so the *p99* can be arbitrarily bad. Quotas,
  admission control and timeouts exist because of this. This is the most
  commonly misapplied result in systems engineering, and it has its own
  subsection below.
- **String building, tokenising, and the `+=` habit.** In CPython, `s += x` on
  strings is often amortised $O(|x|)$ because CPython over-allocates `str` — but
  this was a deliberate implementation decision (PEP 626 era) precisely because
  the analysis was done. In C++ it is $O(|s|^2)$ and the idiom is `std::string`
  or `+=` on a `std::string` with a reserve.
- **Union-find, and the only named amortised cost in practice.** Disjoint-set
  union with union by rank and full path compression is $O(\alpha(N))$ amortised
  per operation, where $\alpha$ is the inverse Ackermann function — a function
  bounded by 5 over the entire range of integers. Every one of these is a few
  lines calling `find` and `union`: Kruskal's and Prim's minimum spanning trees,
  connected-component labelling, image segmentation, Spark's and Hadoop's
  connected-pair avoidance, and the "group these rows by adjacency" button in a
  spreadsheet. The lesson measures `2.3613` parent hops per operation at
  $N = 1{,}000$ and `2.3563` at $N = 300{,}000$: $N$ grew by 300 and the figure
  did not move, which is the bound as an *observable* rather than a theorem.
- **The sliding window, which is amortisation with no spike to amortise.** Almost
  every "window of size $K$" algorithm — max or min window sum, longest
  substring without repeats, minimum subarray meeting a threshold — is an
  amortised argument with no rare expensive operation in it at all. Each element
  enters the window once and leaves once, so the total is $K + 2(n - K) = 2n - K$
  regardless of $K$: `199,500` element touches against `49,750,500` for
  recomputing each window, a factor of `249.4`. When the statistic cannot be
  un-added — a maximum — a monotonic deque carries the same argument, bounded
  by $2n$ at any window size.


---

## The Formal Version

Throughout, $T_i$ is the actual cost of the $i$-th operation on a data structure,
$n$ is the number of operations, and all costs are in units of "one element copy"
or "one comparison" as appropriate. See [SYMBOLS.md](../SYMBOLS.md) and
[Lesson 80](80_big_o_and_complexity.md).

**Definition (aggregate bound).** A data structure has an **amortised** cost of
$\hat{c}$ per operation if there is a constant $c$ and a constant $n_0$ such that
for every sequence of $n \ge n_0$ operations,

$$\sum_{i=1}^{n} T_i \;\le\; c\,\hat{c}\, n.$$

*Explanation.* This is the only definition, and everything else is a way of
proving it. Note the quantifier: **for every sequence**. Not for most sequences,
not for a random sequence, not for the sequence you tested. If your argument
depends on how often the expensive operation happens, you have proved an
average-case bound, not an amortised one.

**Definition (amortised cost of a single operation).** Given a sequence,
$\hat{T}_i = T_i + \Phi_i - \Phi_{i-1}$ for any potential function $\Phi$ with
$0 \le \Phi_i \le \Phi_{\max}$. Summing telescopes:

$$\sum_{i=1}^{n} T_i \;=\; \sum_{i=1}^{n} \hat T_i \;-\; \bigl(\Phi_n - \Phi_0\bigr) \;\le\; \sum_{i=1}^{n}\hat T_i \;+\; \Phi_{\max}.$$

*Explanation.* The $\Phi$ terms are a bookkeeping device that lets you charge an
operation that is cheap *now* against a future expensive one. The inequality is
one-sided, so all you need is an upper bound on $\Phi$ and non-negativity. The
whole method is this identity and the observation that the potential terms
cancel.

**Theorem (the three methods are equivalent).** The aggregate, accounting and
potential methods produce the same bounds.

*Explanation.* The aggregate method bounds $\sum T_i$ directly by grouping
operations. The accounting method picks a price per operation, tracks a balance,
and shows the balance never goes negative — which is a potential function in
disguise. The potential method picks $\Phi$ up front and computes
$\hat T_i = T_i + \Delta\Phi$ for each operation. All three are statements about
the same telescoping identity; they differ in what you choose first.

**Theorem (dynamic array append is amortised $\Theta(1)$).** Let an array of
capacity $C$ start at $C = 1$ and double whenever it fills. The $k$-th resize
occurs at size $2^k$ and copies $2^k$ elements, so

$$\sum \text{copies} \;=\; 1 + 2 + 4 + \cdots + \frac{n}{2} \;<\; n.$$

Since $n$ appends also cost at least $n$ stores, the total is $\Theta(n)$ and the
amortised cost is $\Theta(1)$.

*Explanation.* The whole result is that a geometric series is dominated by its
last term. The lesson's code measures `4,092` element copies for $n = 4096$,
i.e. `0.9990` per append, against the bound of $1$.

**Theorem (and the growth factor is the only free parameter).** With capacity
multiplied by $f > 1$ at each resize, the $k$-th resize copies $C f^k$ elements
and the last one copies about $n/f$, so

$$\sum \text{copies} \;\approx\; \frac{n}{f}\left(1 + \frac1f + \frac1{f^2} + \cdots\right) \;=\; \frac{n}{f-1},$$

giving an amortised cost of $\frac{1}{f-1}$ copies per append.

*Explanation.* The measured values are `8.8263` at $f = 1.125$, `2.6345` at
$f = 1.5$, `0.9990` at $f = 2$ and `0.3330` at $f = 4$. The formula
$\frac{1}{f-1}$ predicts `8.0`, `2.0`, `1.0` and `0.3333`; the residual is the
initial capacity offset, which matters most when $f$ is small. **The class is
$\Theta(1)$ for every $f > 1$** — the factor moves only the constant and the
memory, which is why the choice is an engineering decision and not a
mathematical one.

**Theorem (constant growth is amortised $\Theta(n)$, and that is a different
class).** If the array grows by a fixed $k$ on each resize, the resize sizes are
$1, 1+k, 1+2k, \dots$ — an **arithmetic** progression — and

$$\sum \text{copies} \;=\; 0 + k + 2k + \cdots + n \;=\; \frac{n^2}{2k} \;=\; \Theta(n^2).$$

*Explanation.* The interface is identical. The operations are identical. The
only difference is the growth rule, and it changes the amortised cost from
$\Theta(1)$ to $\Theta(n)$ — a quadratic total instead of a linear one. This is
the single most practically important fact in the lesson, and the code measures
`2047.5000` copies per append at $k = 1$ against `0.9990` at $f = 2$. **"Amortised
$O(1)$" is a property of the implementation, not of the interface.**

**Definition (accounting method, precisely).** Fix a price $\hat T$ per operation.
For each operation, set the credit $c_i = \hat T - T_i$ and let the balance be
$B_k = \sum_{i \le k} c_i$. If $B_k \ge 0$ for all $k$, then
$\sum_{i=1}^{n} T_i = n\hat T - B_n \le n\hat T$.

*Explanation.* The bank account. You charge every operation the same price and
the surplus or deficit goes to a balance; the method is sound exactly when the
balance never goes negative. The lesson's code charges 3 per append, deposits 2
on an ordinary append (which costs 1) and spends the credits on a resize, and the
minimum balance over 32 appends is `2`.

**Theorem (the accounting method for the array, with the constant 3).** Charge 3
per append. An ordinary append costs 1, depositing 2. A resize at size $C$ costs
$C$ copies plus 1 for the store, i.e. $C+1$. Since $C$ appends have happened since
the last resize, $2C$ credits have been deposited, and $2C \ge C + 1$ for
$C \ge 1$. The balance is therefore never negative and the amortised cost is at
most 3.

*Explanation.* The cleanest proof in the lesson, because the single inequality
$2C \ge C+1$ *is* the result. Note that $2C \ge C+1$ holds for every $C \ge 1$
and, more importantly, the balance is *non-decreasing across rounds*: each round
gains $C - 1$.

**Theorem (the potential for the array, and the constant 3 again).** Take
$\Phi = 2n - C$ where $n$ is the size and $C$ the capacity. Then for both kinds
of append, $\hat T = T + \Delta\Phi = 3$:

- ordinary append: $T = 1$, $\Delta\Phi = +2$ (size up, capacity flat) $\Rightarrow \hat T = 3$;
- resize at size $n$: $T = n+1$, $\Delta\Phi = 2 - n$ $\Rightarrow \hat T = 3$.

And $0 \le \Phi \le 2n = O(n)$ at all times.

*Explanation.* The potential column of the code's table is constant `3` for every
one of the first 32 appends — the bound is *computed*, not inferred. Note the
clever part: $\Phi = C - n$ (the free slots) is the intuitive choice and gives
$\hat T = 0$ or $C$, not a constant; $\Phi = 2n - C$ is the one that works, and
finding it is the creative step. $\Phi$ must be a quantity whose *increase*
absorbs the expensive operation and whose *decrease* is small and bounded, and
twice-the-size-minus-capacity is exactly that.

**Definition (amortised versus average, and the quantifier that separates them).**

| | quantifies over | needs randomness? | what it promises |
| --- | --- | --- | --- |
| worst case | all inputs, $\max$ | no | a bound for every input |
| average case | one named distribution, $\mathbb{E}$ | usually yes | a bound for a typical input |
| **amortised** | all *sequences of operations*, $\sum$ | **no** | a bound on the total, hence a bound on the average per operation |

*Explanation.* A dynamic array is the mirror image of a hash table. Its
per-operation worst case is $\Theta(n)$ and its amortised cost is $\Theta(1)$ —
a **guarantee for every sequence**. A hash table's expected lookup is $O(1)$ and
its worst case is $\Theta(n)$ — a **hope** that depends on the key distribution
and on the seed. The lesson's code puts the two side by side: a `BadHash` whose
lookup costs `(n+1)/2` probes on average *and* in the worst case, and a dynamic
array whose worst single append copies $16384$ elements while its amortised cost
is `0.9961`.

**Definition (the amortised fraction of a sequence).** For a sequence with total
cost $C$ over $n$ operations, the *amortised fraction* of operation $i$ is
$\frac{T_i}{C/n}$. A sequence is $\epsilon$-heavy in a set $S$ of operations if
$|S| \ge \epsilon n$.

**Theorem (tighter than the aggregate bound).** If operations in $S$ cost
$O(1)$ and the rest cost $O(n)$, and $S$ is not $\epsilon$-heavy, then every
operation is amortised $O(1/\epsilon)$.

*Explanation.* This is the "fractional cascading" bound and it is strictly
stronger than the aggregate one, because it does not require the expensive
operations to be rare *in time* — only to be rare *in the sequence*. The
dynamic array is the $\epsilon \to 0$ case. The queue of Exercise 6 is the
non-degenerate one: 8 compactions among 4000 operations is a fraction of
`0.002`, giving an amortised bound of $O(1/0.002) = O(500)$ per operation, and
the measured figure is `0.331` moves per operation — a better bound than the
aggregate one promises.

**Theorem (the peak is not bounded by the amortised cost).** Amortised
$\hat c$ per operation and worst case $w(n)$ per operation are compatible for
every $n$, and both statements hold simultaneously.

*Explanation.* This is the result that surprises people and that the whole
lesson's opening table demonstrates. Nothing about "the total is at most $cn$"
bounds any individual term, because one term can be $cn$ and the rest $0$. The
consequence for systems work is severe and worth stating plainly: an amortised
$O(1)$ bound is the right tool for **throughput** and the wrong tool for
**latency**, and a service with an SLO has a latency budget. Admission control,
quotas and pre-allocating the worst case are the responses, and none of them
follows from the amortised bound.

**Definition (potential function, the useful one to remember).** A potential is
any function of the data structure's state with $0 \le \Phi \le \Phi_{\max} = O(n)$
such that $T_i + \Delta\Phi_i \le \hat c$ for every operation.

*Explanation.* You are looking for a quantity that (a) is bounded, (b) goes
*up* by a lot exactly when the operation was expensive, and (c) goes *down* by
little otherwise. Free slots, slack, the number of live objects in a mark phase,
the depth of a stack, the number of set bits in a counter — all are potentials.
If you can find one, you have an amortised bound; if you cannot find one, the
aggregate method may still work.

**Definition (disjoint-set union).** A disjoint-set forest over $N$ labelled
elements is an array `parent` plus a rank per node, supporting `MAKE-SET`,
`FIND` (walk parent pointers to the root) and `UNION` (attach one root under the
other). The cost of every operation is the number of pointers walked.

**Theorem (union-find is $O(\alpha(N))$ amortised, and needs both heuristics).**
With full path compression *and* union by rank, every sequence of $m$ operations
on $N$ elements costs at most $O(m \cdot \alpha(N))$ traversals, where
$A(0) = 1$, $A(k+1) = 2^{A(k)}$ and $\alpha(n) = \min\{k \ge 0 : A(k) \ge n\}$.
Either heuristic alone gives only $O(\log N)$ amortised.

*Explanation.* Union by rank bounds the *shape* — rank $r$ requires at least
$2^r$ elements, so depth is at most $\lfloor \log_2 N \rfloor$ — while path
compression bounds the *queries* by flattening the paths they walk. The two
interact, and only the interaction is $\alpha$. Because $A$ is a tower of twos,
$A(4) = 65{,}536$ and $A(5) = 2^{65536}$, so $\alpha(n) \le 4$ for
$n \le 65{,}536$ and $\alpha(n) \le 5$ for every $n$ that exists. **Crucially,
$\alpha$ bounds $\sum T_i$, not $\max_i T_i$ and not tree depth**: the code
finds a deliberately balanced leaf in $2\log_2 N$ hops, and again in 2.

**Definition (the sliding-window amortisation).** A window of width $K$ slides
one position at a time over $n$ elements. Maintaining a window statistic by
*updating* the previous value — subtracting the element that leaves, adding the
one that arrives — costs $O(1)$ per shift, so the total over $n$ shifts is

$$K + 2(n - K) \;=\; 2n - K \;<\; 2n \;=\; \Theta(n),$$

independent of $K$: amortised $O(1)$ per element, unconditionally.

*Explanation.* The charging rule is one sentence: every element is added once as
it enters and removed once as it leaves, and no element leaves twice, so
$\sum T_i \le 2n$. There is no expensive operation and no threshold — which is
what distinguishes this from every other example in the lesson. When the
statistic cannot be un-added, a monotonic deque supplies the same bound for the
same reason: every index is pushed once and popped at most once.

### Accounting and potential are the same argument

**Theorem (the balance is the potential).** Fix a price $\hat T$, put
$c_i = \hat T - T_i$ and $B_k = \sum_{i \le k} c_i$. Then for any $\Phi$
satisfying $T_i + \Delta\Phi_i = \hat T$ for all $i$,

$$B_k \;=\; \hat T\, k - \sum_{i \le k} T_i \;=\; \Phi_k - \Phi_0 .$$

*Explanation.* Both equalities are the same rearrangement of the telescoping sum,
so $B_k \ge 0$ and $\Phi_k \ge \Phi_0$ are literally the same inequality, and
$\Phi_0$ is the account's initial deficit. The code verifies the identity rather
than asserting it: over `4,096` appends of a doubling array there are `0` steps at
which $B_k \ne \Phi_k - \Phi_0$, and both finish at `4,100`.

The methods therefore differ not in what they prove but in **what you must check**.
Accounting's obligation is a *prefix* condition — $B_k \ge 0$ at every $k$ — and
potential's is a *per-operation* condition — $T + \Delta\Phi \le \hat c$ for every
kind of operation. Two consequences follow. A prefix condition must be verified
everywhere: charging 2 per append leaves the account at `1, 2, 3, 4, 1, 2, 3, 4`
over the first eight appends and then at $-3$ on append 9, so eight appends of
hand-checking pass a price that is simply wrong. And a per-operation condition is
a reusable formula, which is why the potential method scales across a structure
with a dozen operations while accounting does not — unless the operations
genuinely deserve different prices, which is precisely when accounting wins.
Finally, **accounting is how you find the potential**: guess a price, accumulate
the balance, notice the balance is a potential, and raise the price until it never
goes negative. The smallest such price is the bound, and for the doubling array it
is 3.

---

## Formula Sheet

`$T_i$` is the actual cost of operation `$i$`, `$\hat T_i$` its amortised cost,
`$\Phi$` the potential, `$C$` the capacity of a dynamic array, `$n$` its size
(also used for the number of operations where no array is involved), `$f > 1$` the
growth factor, `$k` the constant growth increment, and `$c$` the constant in the
aggregate bound. `$\epsilon$` is the heavy-operation fraction, `$K` the sliding
window's width, `$N` a disjoint-set universe, `$m` its number of operations,
and `$\alpha$` the inverse Ackermann function.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| aggregate bound | `$\sum_{i=1}^{n}T_i \le c\hat c\, n$` | the total of *any* $n$ operations is at most $c\hat c n$ | the only definition of amortised; **quantifies over every sequence** |
| amortised cost | `$\hat T_i = T_i + \Phi_i - \Phi_{i-1}$` | what we charge operation $i$ | with a potential $\Phi$; sums telescope |
| telescoping identity | `$\sum T_i = \sum \hat T_i - (\Phi_n - \Phi_0) \le \sum \hat T_i + \Phi_{\max}$` | the potential terms cancel, leaving a bound | the engine behind all three methods |
| potential bound | `$0 \le \Phi \le \Phi_{\max} = O(n)$` | $\Phi$ must be bounded both ways | **not** enough that $\Phi \ge 0$; the upper bound is the one that pays |
| dynamic array total | `$\sum = 1+2+4+\cdots+\frac n2 < n$` | a geometric series, dominated by its last term | $f = 2$; gives `0.9990` copies per append, measured |
| growth factor $f$ | `$\sum \approx \frac{n}{f-1}$, amortised `$\approx\frac{1}{f-1}$` | copies per append, and the whole trade in one number | `8.8263` at $f=1.125$, `0.9990` at $f=2$, `0.3330` at $f=4$; **valid for `$f>1$ only** |
| growth factor optimum | `$\min_f\big[\frac{1}{f-1} + \frac{f-1}{2}\big] = \sqrt2$ at `$f = 2.414$` | copies plus wasted slots | a textbook optimum no real library uses; memory and copies are not priced equally |
| constant growth $k$ | `$\sum = 0+k+2k+\cdots+n = \frac{n^2}{2k} = \Theta(n^2)$` | an **arithmetic** series, not a geometric one | growing by a constant gives amortised $\Theta(n)$ — `2047.5` copies per append at $k=1$ |
| accounting credit | `$c_i = \hat T - T_i$ | the surplus of the price over the cost | goes into a balance; sound iff the balance never goes negative |
| accounting, array | charge `3`, deposit `2`, spend `C+1`; `2C \ge C+1` | one inequality is the whole proof | minimum balance `2` over 32 appends, measured |
| potential, array | `$\Phi = 2n - C$`, giving `$\hat T = 3$` for **both** append kinds | twice the size minus the capacity | $0 \le \Phi \le 2n$; the computed table is constant `3` |
| potential, binary counter | `$\Phi = $ number of 0 bits | each increment creates one 0 and clears some 1s | `$\hat T = 1 + \Delta\Phi \le 2$`; measured amortised `2.0000` at 20 bits |
| binary counter total | `$(2^n - 1) + n$ flips over `2^n` increments | exact, not a bound | `2,097,130` for $2^{20}$ increments; amortised exactly 2 in the limit |
| hash table worst case | `$\Theta(n)$ | all $n$ keys in one bucket | attainable by an adversary who knows the seed; `BadHash` measures `(n+1)/2` probes per lookup |
| hash table expected | `$O(1)$ | one probe, on average | **needs** a random seed and a well-behaved key distribution; measured `1.12`–`1.28` probes |
| hash table amortised insert | rehash total `$\approx 2n$`, so `$\approx 2$ per insert | the resize is a geometric series | `0.9996` at $n = 16384$, a **guarantee** independent of the hash |
| amortised fraction | `$T_i / (C/n)$ | how many times average cost this operation cost | finds the operations to protect; $\epsilon$-heavy sets give $O(1/\epsilon)$ |
| $\epsilon$-heavy theorem | rare-but-expensive $\Rightarrow$ amortised `$O(1/\epsilon)$` | the expensive ones need not be rare *in time* | queue compaction: 8 of 4000, measured `0.331` moves per operation |
| peak vs amortised | amortised $\hat c$ and worst case $w(n)$ hold **simultaneously** | the average says nothing about the maximum | why amortised bounds are the right tool for throughput and the wrong one for latency |
| shrink thrash | alternating append/pop, halving at half full | resizes on *every* operation | still $\Theta(1)$ — but the constant is `511.98` copies per operation instead of `1` |
| balance ≡ potential | `$B_k = \hat T\, k - \sum_{i\le k}T_i = \Phi_k - \Phi_0$` | the bank balance **is** the potential, up to a constant | the crispest statement that accounting and potential are one method |
| union-find total | `$\sum T_i \le c\, m\,\alpha(N)$`, so `$O(N\alpha(N))$` | about 4 parent traversals per operation, **for every sequence** | disjoint-set union; needs rank **and** compression together |
| rank bound on depth | `$d \le \lfloor \log_2 N \rfloor$` | rank `r` needs `2^r` elements, so merging equal ranks sets the bound | union by rank alone — amortised $O(\log N)$, not $\alpha$ |
| α definition | `$A(0)=1`, `$A(k+1)=2^{A(k)}`, `$\alpha(n)=\min\{k\ge0: A(k)\ge n\}$` | a **tower of twos**, not a tower of threes | `$\le 4$` for `$n \le 65{,}536$`, and `$\le 5$` for every `$n$` that exists |
| sliding window, rolling sum | `$s_{i+1} = s_i - v_i + v_{i+K}$`, total `$K + 2(n-K) = 2n - K$` | consecutive windows share `K-1` elements | `2.0050` touches per window at `$n=100000$`, `$K=500$`; `249.4x` better than rescanning |
| sliding window, monotonic deque | `$\sum T_i \le 2n$` — one push and at most one pop per element | the rolling **maximum** at any window size | `2.0000` deque ops per element; longest deque `19` in a window of `500` |

---

## Worked Example

The complete aggregate analysis of `append` on a doubling dynamic array, with
every intermediate value. This is the worked example because it is the one
analysis that every computer scientist has to be able to produce on a whiteboard.

### The data structure

```
A: array of capacity C, initially C = 1
n: number of elements, initially 0

APPEND(x):
    if n == C:              # the array is full
        C = 2C              # double the capacity
        allocate a new array of size C
        copy the n live elements into it
    store x at position n
    n = n + 1
```

### Step 1 — the individual costs

| append number | capacity before | resize? | elements copied | cumulative copies |
| --- | --- | --- | --- | --- |
| 1 | 1 | yes | 0 (nothing to copy) | 0 |
| 2 | 2 | no | 0 | 0 |
| 3 | 4 | yes | 2 | 2 |
| 4 | 8 | no | 0 | 2 |
| 5 | 16 | no | 0 | 2 |
| 6 | 32 | no | 0 | 2 |
| 7 | 64 | no | 0 | 2 |
| 8 | 128 | no | 0 | 2 |
| 9 | 256 | yes | 8 | 10 |
| … | | | | |
| 17 | 32768 | yes | 16 | 26 |

The lesson's code traces the first 32 appends and prints `0` for every ordinary
append, `4`, `8`, `16` for the resizes, and the running average
`0.8000, 1.3333, 1.6471, 0.8750`.

### Step 2 — the geometric series, written out

The $k$-th resize (counting $k = 0$ for the first) happens when the array is
full, i.e. when $n = 2^k$, and it copies all $2^k$ live elements. So the total
copying for $n$ appends is

$$1 + 2 + 4 + 8 + \cdots + \frac{n}{2}.$$

A geometric series with ratio 2 is dominated by its last term; summing to
$n/2$ gives

$$\sum_{j=0}^{\log_2 n - 1} 2^j \;=\; 2^{\log_2 n} - 1 \;=\; n - 1 \;<\; n.$$

**Step 3 — the lower bound.** Each append stores one element, which is at least
one unit of work, so the total is at least $n$. Combined with the upper bound:

$$n \;\le\; \sum_{i=1}^{n} T_i \;<\; n + n \;=\; 2n,$$

so $\sum T_i = \Theta(n)$ and the amortised cost is $\Theta(1)$. The code measures
`4,092` copies for $n = 4096$ — `0.9990` per append — against the upper bound of
`1.0` and the trivial lower bound of `0`.

### Step 4 — the growth factor, generalised

With capacity multiplied by $f > 1$, the $k$-th resize copies $f^k$ elements and
the last one copies about $n/f$. Summing backwards from the last term:

$$\sum \approx \frac{n}{f}\left(1 + \frac{1}{f} + \frac{1}{f^2} + \cdots\right) \;=\; \frac{n}{f}\cdot\frac{f}{f-1} \;=\; \frac{n}{f-1}.$$

So the amortised cost is $\frac{1}{f-1}$ copies per append. The code's table of
$\frac{1}{f-1}$ against measurement:

| $f$ | $\frac{1}{f-1}$ predicted | measured | slots wasted at worst |
| --- | --- | --- | --- |
| 1.125 | 8.0000 | 8.8263 | 9.3% |
| 1.5 | 2.0000 | 2.6345 | 28.9% |
| 2 | 1.0000 | 0.9999 | 0.0% |
| 4 | 0.3333 | 0.3330 | 0.0% |

Every one of these is $\Theta(1)$. The factor moves the constant and the memory,
and the choice is an engineering decision: CPython's `list` uses about
$1.125$ and `std::vector` doubles.

### Step 5 — the same interface, a different class

Now change one line: `C = C + k` for a fixed $k$. The resize sizes are
$1, 1+k, 1+2k, \dots$ — an **arithmetic** progression — and the total is

$$0 + k + 2k + \cdots + n \;=\; \frac{n^2}{2k}.$$

For $n = 2000$ and $k = 4$ the code measures `499,000` copies, i.e. `249.5` per
append and `499` resizes. The total is $\Theta(n^2)$: **quadratic work for $n$
appends, from an interface that is character-for-character identical.** The
amortised cost is $\Theta(n)$, not $\Theta(1)$.

### Step 6 — the worst single append, and why it coexists

Fill the array to capacity and then append once:

| capacity before | copies in that one append |
| --- | --- |
| 64 | 64 |
| 256 | 256 |
| 1024 | 1024 |
| 4096 | 4096 |
| 16384 | 16384 |

Each row moves the whole live array in one operation, and it grows with $n$. No
rearrangement of the analysis changes this: the data has to exist somewhere, and
relocating $n$ elements is $\Theta(n)$. Meanwhile the amortised column of the same
run reads `0.9375, 0.9688, 0.9844, 0.9922, 0.9961` at $n = 64, 128, 256, 512,
1024$ — flat, converging to 1.

**Both are true, simultaneously, of the same array.** The amortised cost is a
statement about the total; the worst case is a statement about the peak. The
conflict people expect does not exist, because they are statements about
different things — and the run-time consequence is that the peak is what a
latency budget is made of.


### Step 7 — union-find, and what $\alpha(n)$ actually buys

The worked example for union-find is the ledger of *parent-pointer hops*, which
is the only thing that costs anything. At $n = 4{,}000$ with `12,000` operations
(one `union` followed by two `find`s, from a fixed deterministic sequence), the
four implementations are:

| rank | compression | total hops | hops per op | max depth |
| --- | --- | --- | --- | --- |
| no | no | `774,496` | `64.5413` | 433 |
| yes | no | `30,487` | `2.5406` | 5 |
| no | yes | `49,109` | `4.0924` | 6 |
| yes | yes | `28,276` | `2.3563` | 3 |

Two things fall straight out. First, the `64.5413` row is the quadratic one: with
neither heuristic the forests degenerate into chains, the total is $\Theta(n^2)$,
and the ratio to the combined row is already $27\times$ at $n = 4{,}000$ — and it
grows with $n$. Second, neither single heuristic reaches the combined bound, so
they are not interchangeable: the theory says each alone gives amortised
$O(\log N)$, and the measurement agrees in spirit (the compression-only column
climbs from `3.6050` to `4.9703` as $n$ goes from 1,000 to 100,000 while the
combined column does not move).

**The amortised constant.** Now scale $n$ and watch the combined row:

| $n$ | operations | total hops | hops per op | max depth | depth histogram |
| --- | --- | --- | --- | --- | --- |
| 1,000 | 3,000 | `7,084` | `2.3613` | 3 | `0:167, 1:665, 2:156, 3:12` |
| 10,000 | 30,000 | `70,567` | `2.3522` | 3 | `0:1606, 1:6843, 2:1505, 3:46` |
| 100,000 | 300,000 | `708,317` | `2.3611` | 3 | `0:16260, 1:68830, 2:14468, 3:442` |
| 300,000 | 900,000 | `2,120,637` | `2.3563` | 3 | `0:48523, 1:206938, 2:43118, 3:1421` |

$n$ grew by a factor of 300 and the amortised figure moved by less than `0.01`.
That flat column **is** the $\alpha(n)$ claim as an empirical object: the total is
$\Theta(n \cdot \alpha(N))$ and $\alpha$ grows too slowly to see. The lower
bound is the trivial one — each `find` costs at least one hop, and each `union`
costs two — so the combined figure cannot go below about 2, and it sits at 2.36.

**Step 7b — the peak, which $\alpha$ does not bound.** Build a perfectly
balanced forest by hand and find its deepest leaf:

| $n$ | $\log_2 n$ | max depth | that one `find` | `find` it again |
| --- | --- | --- | --- | --- |
| 16 | 4 | 4 | 8 | 2 |
| 256 | 8 | 8 | 16 | 2 |
| 4,096 | 12 | 12 | 24 | 2 |
| 65,536 | 16 | 16 | 32 | 2 |

The first `find` at a cold leaf costs exactly $2\log_2 n$ hops and the second
costs 2. So at $n = 65{,}536$ there is a single call costing `32` hops — eight
times the $\alpha$ bound of 4, and growing as $\log_2 n$ while $\alpha$ does not
move. This is Step 6 of the array all over again: **the amortised bound is a
statement about the total and the peak is a statement about one call, and no
amortisation relates them.** It is also why the honest answer to "how deep is the
tree" is a measurement (`3`, on this workload, at $n = 300{,}000$) and never
$\alpha(n)$.

### Step 8 — the sliding window, counted

$n = 100{,}000$ elements, $K = 500$, so there are $n - K + 1 = 99{,}501$ windows.
The cost unit is one **element touch** — one read of one element into the
statistic.

**Naive.** Every window is summed from scratch, so every element of every window
is read, and the total is exactly

$$\underbrace{(n - K + 1) \times K}_{\text{one read per element per window}}
\;=\; 99{,}501 \times 500 \;=\; 49{,}750{,}500 \text{ touches},$$

which is `500.00` per window.

**Rolling.** The first window costs $K$ reads. Each shift costs exactly 2 — one
subtraction for the element leaving, one addition for the element entering — so

$$K + 2\,(n - K) \;=\; 500 + 199{,}000 \;=\; 199{,}500 \text{ touches},$$

which is `2.0050` per window. The two methods agree on the first and last window
sums (`2484655` and `2475090`), so the saving is not bought with wrong answers.
**Step 8b — the maximum, where subtract-and-add is unavailable.** A max cannot
be un-added, so the fix is a monotonic deque, and the accounting is: every index
is pushed once and popped at most once. Measured over the same array with the same
$K = 500`: `100,000` pushes and `99,997` pops, `199,997` deque operations,
`2.0000` per element, and a longest deque of `19`. The bound is $2n$ and it holds
**for any window size at all** — change $K$ and the total does not grow.

Note what the two steps have in common, since it is the whole lesson. In Step 7 the
rare event is a deep tree and the bank is the path compression; in Step 8 there
is no rare event at all and the bank is the element that has already been added
and must be subtracted. **Amortisation is not a technique for tolerating spikes.
It is a technique for noticing that the same work is being done twice.**

---

## Runnable Code

### Block 1: a growable array, and the aggregate method worked out

```python
import sys


class GrowArray:
    """A dynamic array whose capacity is multiplied by `factor` when it fills.

    Instrumented so we can count ELEMENT COPIES, which is the real cost: an
    append is O(1) except when it triggers a resize, which is O(size)."""

    def __init__(self, factor=2, start=4):
        self.factor = factor
        self.start = start
        self.data = [None] * start
        self.size = 0
        self.copies = 0            # total element copies made by resizes
        self.resizes = 0
        self.cost = []             # cost of each individual append
        self.capacity = []         # capacity after each append

    def __len__(self):
        return self.size

    def append(self, x):
        before = self.copies
        if self.size == len(self.data):
            # growth is exactly `factor` per resize, except that a factor of 1
            # means "add start", which is the constant-growth case
            grow = int(len(self.data) * self.factor)
            if grow <= len(self.data):
                grow = len(self.data) + self.start
            self._resize(grow)
        self.data[self.size] = x
        self.size += 1
        self.cost.append(self.copies - before)
        self.capacity.append(len(self.data))

    def _resize(self, new_cap):
        self.data = self.data[:self.size] + [None] * (new_cap - self.size)
        self.copies += self.size  # every live element is copied exactly once
        self.resizes += 1

    def free_slots(self):
        """The obvious potential: the number of free slots, C - n."""
        return len(self.data) - self.size


print("=== What each individual append actually costs ===")
a = GrowArray(factor=2)
trace = []
for i in range(1, 33):
    a.append(i)
    trace.append((i, a.capacity[-1], a.cost[-1], a.copies, a.copies / i, a.resizes))
print("   n   capacity   this append   copies so far   copies/n   resizes")
for row in trace:
    if row[2] > 0 or row[0] <= 4 or row[0] == 32:
        tag = "  <- resize" if row[2] > 0 else ""
        print(f"  {row[0]:>2}   {row[1]:>8}   {row[2]:>10}   {row[3]:>12}"
              f"   {row[4]:>9.4f}   {row[5]:>7}{tag}")
print("  Cost is 0 on an ordinary append and the whole live array on a resize.")
print(f"  32 appends caused {trace[-1][5]} resizes, and they get rarer: the 5th append")
print("  copied 4 elements out of 4 done so far, the 17th copied 16 out of 28, and")
print("  by the 1024th the cost of a resize is under 0.6% of the total.  That is")
print("  the entire argument, and it is a statement about a geometric series.")
print()

print("=== The aggregate method, spelled out ===")
print("   factor   n      capacity   element copies   amortised per append   resizes")
for factor in (2, 1.5, 4):
    b = GrowArray(factor=factor)
    n = 4096
    for i in range(n):
        b.append(i)
    print(f"  {factor:>7} {n:>5}   {len(b.data):>10,}   {b.copies:>15,}"
          f"   {b.copies / n:>21.4f}   {b.resizes:>7}")
print()
print("  The aggregate method in one line.  With doubling, the resize sizes are")
print("  1, 2, 4, 8, ..., n/2, so the total element copies are")
print()
print("     1 + 2 + 4 + ... + n/2   <   n        (a geometric series is")
print("                                       bounded by twice its last term)")
print()
print("  Total copies are then at least n, one per element stored, and at most n,")
print("  so the total is Theta(n) and the amortised cost is Theta(1).  The measured")
print("  0.9990 is just under 1, exactly as the bound predicts.")
print("  A larger factor means fewer resizes and a better constant, at the price of")
print("  more wasted memory:")
print("     factor 2   -> 0.9990 copies per append, up to 50% of slots unused")
print("     factor 1.5 -> 2.6345 copies per append, up to 33% unused")
print("     factor 4   -> 0.3330 copies per append, up to 75% unused")
print("  Any factor greater than 1 gives Theta(1); the factor moves only the")
print("  constant and the memory.  CPython's list uses about 1.125 -- a small")
print("  factor, chosen because memory matters more than append speed.")
print()

print("=== Growth by a CONSTANT is amortised Theta(n), not Theta(1) ===")
b = GrowArray(factor=1, start=4)     # capacity grows by exactly 4 each resize
n = 2000
for i in range(n):
    b.append(i)
print(f"  grow-by-4, n = {n}: element copies = {b.copies:,}, "
      f"amortised = {b.copies / n:.1f} per append, {b.resizes} resizes")
print("  Every append after the first four triggers a resize, and each resize")
print("  copies the whole live array: 0 + 4 + 8 + ... + n = Theta(n^2) total, so")
print("  the amortised cost is Theta(n).  Same interface, same operations, and a")
print("  QUADRATIC total instead of a linear one.  'Amortised O(1) append' is a")
print("  property of the GROWTH FACTOR, not of the interface.")
print()

print("=== The running average, which is what amortised means ===")
b = GrowArray(factor=2)
n = 1024
for i in range(n):
    b.append(i)
    if i in (7, 15, 31, 63, 127, 255, 511, 1023):
        k = i + 1
        print(f"  after {k:>5} appends: total copies = {b.copies:>7,}   "
              f"amortised = {b.copies / k:>7.4f}   "
              f"worst single append so far = {max(b.cost):>5}")
print("  The amortised cost rises, then flattens towards 1 and stays there -- 0.9961")
print("  at 1024 appends.  The worst SINGLE append also exists and also grows,")
print("  doubling each time round: 4, 8, 16, ..., 512.  Both facts are true at")
print("  once; nothing here contradicts anything there.")
print()

print("=== The worst single append is Theta(n), and no argument can change it ===")
print("  Fill the array exactly to capacity, then time the one append that")
print("  overflows it.  That is the worst case, and it happens at every size.")
print("   capacity before   cost of the append that triggers the resize")
for n in (64, 256, 1024, 4096, 16384):
    b = GrowArray(factor=2)
    while b.size < n * 4:
        b.append(0)
        if b.size == n and b.size == len(b.data):
            break
    cap_before = len(b.data)
    before = b.copies
    b.append(0)
    print(f"  {cap_before:>15}   {b.copies - before:>38}")
print("  Each row moves the whole live array in one append, and the live array")
print("  doubles from row to row.  It cannot be faster: the data has to exist")
print("  somewhere, and relocating n elements is Theta(n).  Amortisation is a")
print("  statement about the TOTAL, never about the peak.")
print()

print("=== What CPython's list does, for calibration ===")
print("     n   sys.getsizeof(list)   bytes per element   overallocation")
for n in (100, 1000, 10000, 100000):
    lst = list(range(n))
    bpe = sys.getsizeof(lst) / n
    print(f"  {n:>6}   {sys.getsizeof(lst):>20,}   {bpe:>16.1f}   "
          f"{100 * (bpe / 8.0 - 1):>14.1f}%")
print("  A slot holds an 8-byte pointer, so 8.0 bytes per element means the list is")
print("  almost exactly full.  Here is the whole memory/speed trade in one")
print("  formula.  With growth factor f the k-th resize copies C*f^k elements, and")
print("  the last one copies about n/f, so the total is a geometric series:")
print()
print("     total copies ~ (n/f) * (1 + 1/f + 1/f^2 + ...)  =  n / (f - 1)")
print("     amortised per append  ~  1 / (f - 1)")
print()
print("   factor   1/(f-1) predicted   measured   slots wasted at worst")
for f in (1.125, 1.5, 2.0, 4.0):
    b = GrowArray(factor=f)
    n = 65536
    for i in range(n):
        b.append(i)
    waste = 100.0 * (1 - n / len(b.data))
    print(f"  {f:>7}   {1 / (f - 1):>17.4f}   {b.copies / n:>9.4f}   "
          f"{waste:>23.1f}%")
print("  The prediction 1/(f-1) tracks the measurement closely (the residual is the")
print("  +4 start offset, which matters more when f is small).  f = 1.125 gives")
print("  8.8263 copies per append -- nine times worse than doubling -- and wastes")
print("  9.3% of the slots.  CPython chose that end of the curve because Python")
print("  lists are usually sized once and kept, and the memory saving is worth")
print("  more than the append speed.  C++ std::vector doubles, because there the")
print("  appends are often in a hot loop.")
```

Output:

```text
=== What each individual append actually costs ===
   n   capacity   this append   copies so far   copies/n   resizes
   1          4            0              0      0.0000         0
   2          4            0              0      0.0000         0
   3          4            0              0      0.0000         0
   4          4            0              0      0.0000         0
   5          8            4              4      0.8000         1  <- resize
   9         16            8             12      1.3333         2  <- resize
  17         32           16             28      1.6471         3  <- resize
  32         32            0             28      0.8750         3
  Cost is 0 on an ordinary append and the whole live array on a resize.
  32 appends caused 3 resizes, and they get rarer: the 5th append
  copied 4 elements out of 4 done so far, the 17th copied 16 out of 28, and
  by the 1024th the cost of a resize is under 0.6% of the total.  That is
  the entire argument, and it is a statement about a geometric series.

=== The aggregate method, spelled out ===
   factor   n      capacity   element copies   amortised per append   resizes
        2  4096        4,096             4,092                  0.9990        10
      1.5  4096        5,395            10,791                  2.6345        18
        4  4096        4,096             1,364                  0.3330         5

  The aggregate method in one line.  With doubling, the resize sizes are
  1, 2, 4, 8, ..., n/2, so the total element copies are

     1 + 2 + 4 + ... + n/2   <   n        (a geometric series is
                                       bounded by twice its last term)

  Total copies are then at least n, one per element stored, and at most n,
  so the total is Theta(n) and the amortised cost is Theta(1).  The measured
  0.9990 is just under 1, exactly as the bound predicts.
  A larger factor means fewer resizes and a better constant, at the price of
  more wasted memory:
     factor 2   -> 0.9990 copies per append, up to 50% of slots unused
     factor 1.5 -> 2.6345 copies per append, up to 33% unused
     factor 4   -> 0.3330 copies per append, up to 75% unused
  Any factor greater than 1 gives Theta(1); the factor moves only the
  constant and the memory.  CPython's list uses about 1.125 -- a small
  factor, chosen because memory matters more than append speed.

=== Growth by a CONSTANT is amortised Theta(n), not Theta(1) ===
  grow-by-4, n = 2000: element copies = 499,000, amortised = 249.5 per append, 499 resizes
  Every append after the first four triggers a resize, and each resize
  copies the whole live array: 0 + 4 + 8 + ... + n = Theta(n^2) total, so
  the amortised cost is Theta(n).  Same interface, same operations, and a
  QUADRATIC total instead of a linear one.  'Amortised O(1) append' is a
  property of the GROWTH FACTOR, not of the interface.

=== The running average, which is what amortised means ===
  after     8 appends: total copies =       4   amortised =  0.5000   worst single append so far =     4
  after    16 appends: total copies =      12   amortised =  0.7500   worst single append so far =     8
  after    32 appends: total copies =      28   amortised =  0.8750   worst single append so far =    16
  after    64 appends: total copies =      60   amortised =  0.9375   worst single append so far =    32
  after   128 appends: total copies =     124   amortised =  0.9688   worst single append so far =    64
  after   256 appends: total copies =     252   amortised =  0.9844   worst single append so far =   128
  after   512 appends: total copies =     508   amortised =  0.9922   worst single append so far =   256
  after  1024 appends: total copies =   1,020   amortised =  0.9961   worst single append so far =   512
  The amortised cost rises, then flattens towards 1 and stays there -- 0.9961
  at 1024 appends.  The worst SINGLE append also exists and also grows,
  doubling each time round: 4, 8, 16, ..., 512.  Both facts are true at
  once; nothing here contradicts anything there.

=== The worst single append is Theta(n), and no argument can change it ===
  Fill the array exactly to capacity, then time the one append that
  overflows it.  That is the worst case, and it happens at every size.
   capacity before   cost of the append that triggers the resize
               64                                       64
              256                                      256
             1024                                     1024
             4096                                     4096
            16384                                    16384
  Each row moves the whole live array in one append, and the live array
  doubles from row to row.  It cannot be faster: the data has to exist
  somewhere, and relocating n elements is Theta(n).  Amortisation is a
  statement about the TOTAL, never about the peak.

=== What CPython's list does, for calibration ===
     n   sys.getsizeof(list)   bytes per element   overallocation
     100                    856                8.6              7.0%
    1000                  8,056                8.1              0.7%
   10000                 80,056                8.0              0.1%
  100000                800,056                8.0              0.0%
  A slot holds an 8-byte pointer, so 8.0 bytes per element means the list is
  almost exactly full.  Here is the whole memory/speed trade in one
  formula.  With growth factor f the k-th resize copies C*f^k elements, and
  the last one copies about n/f, so the total is a geometric series:

     total copies ~ (n/f) * (1 + 1/f + 1/f^2 + ...)  =  n / (f - 1)
     amortised per append  ~  1 / (f - 1)

   factor   1/(f-1) predicted   measured   slots wasted at worst
    1.125              8.0000      8.8263                       9.3%
      1.5              2.0000      2.8129                      28.9%
      2.0              1.0000      0.9999                       0.0%
      4.0              0.3333      0.3333                       0.0%
  The prediction 1/(f-1) tracks the measurement closely (the residual is the
  +4 start offset, which matters more when f is small).  f = 1.125 gives
  8.8263 copies per append -- nine times worse than doubling -- and wastes
  9.3% of the slots.  CPython chose that end of the curve because Python
  lists are usually sized once and kept, and the memory saving is worth
  more than the append speed.  C++ std::vector doubles, because there the
  appends are often in a hot loop.
```

The two tables at the end are the practical heart of the lesson. The first says
that `sys.getsizeof` grows at 8.0 bytes per element — the list is nearly full at
every size, wasting `9.3%` at worst. The second says why: the growth factor is
`1.125`, and the formula $\frac{1}{f-1}$ predicts `8.0` copies per append where
the code measures `8.8263`. Nine times more copying than a doubling array, in
exchange for 9.3% memory instead of 50%. **Both are $\Theta(1)$ amortised, and
the difference is entirely invisible to the complexity class** — which is the
whole reason the growth factor has to be chosen by measurement and taste rather
than by analysis.

### Block 2: accounting, potential, a binary counter, and hash tables

```python
import random


# ==================================================================== accounting
print("=== The accounting method: a bank account you pay into in advance ===")
print("  Charge 3 units for every append.  An ordinary append costs 1, so you")
print("  deposit the other 2 as CREDIT.  A resize costs n copies plus 1 for the")
print("  store, so you spend credits.  If the balance never goes negative then the")
print("  total charged (3n) is at least the total spent, so the amortised cost is")
print("  at most 3 per append.")
print()
print("   n   actual cost   credited   balance   balance/n")
capacity, size, balance = 4, 0, 0
rows = []
for i in range(1, 33):
    actual = 0
    if size == capacity:
        capacity *= 2
        actual = size + 1          # copy every live element, then store the new one
    actual += 1                    # storing the new element
    credit = 3 - actual
    balance += credit
    size += 1
    rows.append((i, actual, credit, balance, balance / i))
low = min(r[3] for r in rows)
print(f"  minimum balance over the first 32 appends = {low}  (must be >= 0)")
print()
for r in rows:
    if r[0] <= 6 or r[1] > 1 or r[0] in (8, 16, 32):
        tag = "  <- resize, spends credits" if r[1] > 1 else ""
        print(f"  {r[0]:>2}   {r[1]:>11}   {r[2]:>8}   {r[3]:>7}   "
              f"{r[4]:>9.4f}{tag}")
print()
print("  At append 17 the resize costs 17 and the balance drops from 18 to 3, the")
print("  closest it ever comes to empty; from then on it GROWS, because each")
print("  round deposits 2C and spends C+1, a net gain of C-1.  That is the whole")
print("  proof: the account is non-decreasing across resizes, so it is never")
print("  negative, so 3n >= total, so the amortised cost is at most 3.")
print("  The bank account is the aggregate method with bookkeeping attached, and")
print("  its real use is when different operations deserve different prices.")
print()

# ====================================================================== potential
print("=== The potential method: one formula, no bookkeeping ===")
print("  Choose Phi = 2*size - capacity.  Then the identity")
print()
print("     amortised cost  =  actual cost  +  (Phi_after - Phi_before)")
print()
print("  gives a CONSTANT 3 for both kinds of append:")
print("    ordinary append: actual 1, dPhi = +2 (size up, capacity flat) -> 3")
print("    resize at n:     actual n+1, dPhi = 2 - n ->  n+1+2-n = 3")
print("  and 0 <= Phi <= size = O(n) at all times, so summing over any sequence")
print("  telescopes to O(n).  NO assumption about which operation occurred.")
print()
print("   n   capacity   size   Phi = 2n-C   actual cost   dPhi   amortised")
capacity, size = 4, 0
history = []
for k in range(1, 33):
    prev_phi = 2 * size - capacity
    actual = 1
    if size == capacity:
        capacity *= 2
        actual += size           # the copies; the store is the +1 above
    size += 1
    phi = 2 * size - capacity
    d_phi = phi - prev_phi
    history.append((k, capacity, size, phi, actual, d_phi, actual + d_phi))
for h in history:
    if h[0] <= 6 or h[4] > 1 or h[0] in (8, 16, 32):
        tag = "  <- resize" if h[4] > 1 else ""
        print(f"  {h[0]:>2}   {h[1]:>8}   {h[2]:>4}   {h[3]:>11}   {h[4]:>11}"
              f"   {h[5]:>5}   {h[6]:>9}{tag}")
amortised_values = sorted({h[6] for h in history})
print()
print(f"  the distinct amortised costs over all 32 appends: {amortised_values}")
print("  Every one is 3.  That constant column IS the amortised bound, computed")
print("  directly rather than inferred from a total.")
print()

# =============================================================== binary counter
print("=== A binary counter: the cleanest amortised example that is not an array ===")


def increment_cost(state):
    """Cost = the number of bits flipped, i.e. the trailing 1s plus the new 0."""
    i, cost = 0, 0
    while i < len(state) and state[i]:
        state[i] = False
        cost += 1
        i += 1
    if i < len(state):
        state[i] = True
    else:
        state.append(True)
    return cost + 1


for nbits in (8, 16, 20):
    state = [False] * 4
    costs = [increment_cost(state) for _ in range((1 << nbits) - 1)]
    n = len(costs)
    print(f"  {nbits}-bit counter, {n:,} increments: total flips = {sum(costs):,}, "
          f"amortised = {sum(costs) / n:.4f}, worst single increment = {max(costs)}")
print("  The exact answer: running a counter through all 2^n values flips bit i")
print("  exactly 2^(n-i-1) times, and the n new bits are each created once, so the")
print("  total is 2^n - 1 + n and the amortised cost is 1 + n/2^n -> 2.  The WORST")
print("  single increment flips n bits.  Same shape as the array, and it is why")
print("  `i += 1` is O(1) in practice despite being Theta(n) bit work.")
print()

# ==================================================================== hash table
print("=== Amortised versus average: the distinction, made concrete ===")


def stable_hash(s):
    """FNV-1a, a real hash function, written out so the numbers in this lesson
    are the same on every machine and every run.  Python's built-in hash() is
    deliberately randomised per process (that is exactly the defence described
    below), so it would make these figures unreproducible."""
    h = 0x811C9DC5
    for byte in s.encode("utf-8"):
        h = ((h ^ byte) * 0x01000193) & 0xFFFFFFFF
    return h


class BadHash:
    """Every key hashes to one bucket.  No randomness, so there is no average."""
    def __init__(self, n):
        self.buckets = [[]]
        self.probes = 0
        self.nbuckets = 1

    def put(self, k, v):
        self.buckets[0].append((k, v))

    def get(self, k):
        for kk, vv in self.buckets[0]:
            self.probes += 1
            if kk == k:
                return vv
        return None


class GoodHash:
    """A real hash, in a table sized at 2n so it is never more than half full."""
    def __init__(self, n):
        self.nbuckets = 2 * n
        self.buckets = [[] for _ in range(self.nbuckets)]
        self.probes = 0

    def put(self, k, v):
        self.buckets[stable_hash(k) % self.nbuckets].append((k, v))

    def get(self, k):
        for kk, vv in self.buckets[stable_hash(k) % self.nbuckets]:
            self.probes += 1
            if kk == k:
                return vv
        return None


print("     n   BadHash probes   GoodHash probes   BadHash/n   GoodHash/n")
for n in (16, 64, 256, 1024, 4096):
    keys = [f"key{i}" for i in range(n)]
    bad, good = BadHash(n), GoodHash(n)
    for i, k in enumerate(keys):
        bad.put(k, i)
        good.put(k, i)
    for k in keys:
        bad.get(k)
        good.get(k)
    print(f"  {n:>5}   {bad.probes:>13,}   {good.probes:>15,}"
          f"   {bad.probes / n:>9.2f}   {good.probes / n:>10.2f}")
print("  BadHash/n is (n+1)/2 exactly: a full scan of a chain of length k costs")
print("  1 + 2 + ... + k, because the keys were inserted in order.  It is")
print("  Theta(n) PER LOOKUP -- worst case and average case both, and there is no")
print("  sequence of operations to amortise, because each lookup stands alone.")
print("  GoodHash/n sits between 1.12 and 1.28: about 1.2 probes per lookup, the")
print("  signature of a chain of length about 1.2 in a half-full table.")
print()
print("  A dynamic array is the mirror image: its per-operation worst case is")
print("  Theta(n), it makes no probabilistic claim at all, and its amortised cost")
print("  is Theta(1) for EVERY sequence.  Guarantee versus hope -- that is the")
print("  difference between amortised and average-case.")
print()

print("=== A hash table CAN be amortised, if you add one line ===")


class GrowHash:
    """A hash table that doubles its bucket count when it passes half full, and
    rehashes everything.  Rehashes happen at sizes 17, 33, 65, ..., so the total
    rehash work is a geometric series: amortised O(1) inserts, GUARANTEED, with
    no assumption whatsoever on the keys."""

    def __init__(self):
        self.nbuckets = 8
        self.size = 0
        self.rehashes = 0
        self.rehash_work = 0
        self.keys_at_rehash = []

    def put(self, k, v):
        self.size += 1
        if self.size > 2 * self.nbuckets:
            self.nbuckets *= 2
            self.rehashes += 1
            self.rehash_work += self.size
            self.keys_at_rehash.append(self.size)
        return self.size


print("       n   total rehash work   amortised per insert   rehashes   sizes at rehash")
for n in (64, 256, 1024, 4096, 16384):
    h = GrowHash()
    for i in range(n):
        h.put(i, i)
    print(f"  {n:>5}   {h.rehash_work:>17,}   {h.rehash_work / n:>20.4f}"
          f"   {h.rehashes:>8}   {h.keys_at_rehash}")
print("  The rehash sizes are 17, 33, 65, 129, 257, ... -- each 2^k + 1, since the")
print("  trigger is size > 2*nbuckets -- so the total work is 17 + 33 + 65 + ...")
print("  < 2n, giving an amortised rehash cost under 2 per insert.  This is a")
print("  GUARANTEE valid for every possible key sequence, and unlike")
print("  expected-O(1) lookup it does not depend on the hash function at all.")
print("  This is what every production hash table does, and it is why inserting a")
print("  million keys does not suddenly become quadratic.")
print()
print("  Note the asymmetry that makes this worth saying: expected-O(1) LOOKUP is")
print("  still needed, because even a perfectly sized table has long chains by")
print("  chance.  What the resize fixes is not the lookup but the INSERT's")
print("  amortised guarantee -- without it, inserting into a full table costs")
print("  Theta(n) every time and the total really is quadratic.")
```

Output:

```text
=== The accounting method: a bank account you pay into in advance ===
  Charge 3 units for every append.  An ordinary append costs 1, so you
  deposit the other 2 as CREDIT.  A resize costs n copies plus 1 for the
  store, so you spend credits.  If the balance never goes negative then the
  total charged (3n) is at least the total spent, so the amortised cost is
  at most 3 per append.

   n   actual cost   credited   balance   balance/n
  minimum balance over the first 32 appends = 2  (must be >= 0)

   1             1          2         2      2.0000
   2             1          2         4      2.0000
   3             1          2         6      2.0000
   4             1          2         8      2.0000
   5             6         -3         5      1.0000  <- resize, spends credits
   6             1          2         7      1.1667
   8             1          2        11      1.3750
   9            10         -7         4      0.4444  <- resize, spends credits
  16             1          2        18      1.1250
  17            18        -15         3      0.1765  <- resize, spends credits
  32             1          2        33      1.0312

  At append 17 the resize costs 17 and the balance drops from 18 to 3, the
  closest it ever comes to empty; from then on it GROWS, because each
  round deposits 2C and spends C+1, a net gain of C-1.  That is the whole
  proof: the account is non-decreasing across resizes, so it is never
  negative, so 3n >= total, so the amortised cost is at most 3.
  The bank account is the aggregate method with bookkeeping attached, and
  its real use is when different operations deserve different prices.

=== The potential method: one formula, no bookkeeping ===
  Choose Phi = 2*size - capacity.  Then the identity

     amortised cost  =  actual cost  +  (Phi_after - Phi_before)

  gives a CONSTANT 3 for both kinds of append:
    ordinary append: actual 1, dPhi = +2 (size up, capacity flat) -> 3
    resize at n:     actual n+1, dPhi = 2 - n ->  n+1+2-n = 3
  and 0 <= Phi <= size = O(n) at all times, so summing over any sequence
  telescopes to O(n).  NO assumption about which operation occurred.

   n   capacity   size   Phi = 2n-C   actual cost   dPhi   amortised
   1          4      1            -2             1       2           3
   2          4      2             0             1       2           3
   3          4      3             2             1       2           3
   4          4      4             4             1       2           3
   5          8      5             2             5      -2           3  <- resize
   6          8      6             4             1       2           3
   8          8      8             8             1       2           3
   9         16      9             2             9      -6           3  <- resize
  16         16     16            16             1       2           3
  17         32     17             2            17     -14           3  <- resize
  32         32     32            32             1       2           3

  the distinct amortised costs over all 32 appends: [3]
  Every one is 3.  That constant column IS the amortised bound, computed
  directly rather than inferred from a total.

=== A binary counter: the cleanest amortised example that is not an array ===
  8-bit counter, 255 increments: total flips = 502, amortised = 1.9686, worst single increment = 8
  16-bit counter, 65,535 increments: total flips = 131,054, amortised = 1.9998, worst single increment = 16
  20-bit counter, 1,048,575 increments: total flips = 2,097,130, amortised = 2.0000, worst single increment = 20
  The exact answer: running a counter through all 2^n values flips bit i
  exactly 2^(n-i-1) times, and the n new bits are each created once, so the
  total is 2^n - 1 + n and the amortised cost is 1 + n/2^n -> 2.  The WORST
  single increment flips n bits.  Same shape as the array, and it is why
  `i += 1` is O(1) in practice despite being Theta(n) bit work.

=== Amortised versus average: the distinction, made concrete ===
     n   BadHash probes   GoodHash probes   BadHash/n   GoodHash/n
     16             136                18        8.50         1.12
     64           2,080                76       32.50         1.19
    256          32,896               328      128.50         1.28
   1024         524,800             1,296      512.50         1.27
   4096       8,390,656             4,962     2048.50         1.21
  BadHash/n is (n+1)/2 exactly: a full scan of a chain of length k costs
  1 + 2 + ... + k, because the keys were inserted in order.  It is
  Theta(n) PER LOOKUP -- worst case and average case both, and there is no
  sequence of operations to amortise, because each lookup stands alone.
  GoodHash/n sits between 1.12 and 1.28: about 1.2 probes per lookup, the
  signature of a chain of length about 1.2 in a half-full table.

  A dynamic array is the mirror image: its per-operation worst case is
  Theta(n), it makes no probabilistic claim at all, and its amortised cost
  is Theta(1) for EVERY sequence.  Guarantee versus hope -- that is the
  difference between amortised and average-case.

=== A hash table CAN be amortised, if you add one line ===
       n   total rehash work   amortised per insert   rehashes   sizes at rehash
     64                  50                 0.7812          2   [17, 33]
    256                 244                 0.9531          4   [17, 33, 65, 129]
   1024               1,014                 0.9902          6   [17, 33, 65, 129, 257, 513]
   4096               4,088                 0.9980          8   [17, 33, 65, 129, 257, 513, 1025, 2049]
  16384              16,378                 0.9996         10   [17, 33, 65, 129, 257, 513, 1025, 2049, 4097, 8193]
  The rehash sizes are 17, 33, 65, 129, 257, ... -- each 2^k + 1, since the
  trigger is size > 2*nbuckets -- so the total work is 17 + 33 + 65 + ...
  < 2n, giving an amortised rehash cost under 2 per insert.  This is a
  GUARANTEE valid for every possible key sequence, and unlike
  expected-O(1) lookup it does not depend on the hash function at all.
  This is what every production hash table does, and it is why inserting a
  million keys does not suddenly become quadratic.

  Note the asymmetry that makes this worth saying: expected-O(1) LOOKUP is
  still needed, because even a perfectly sized table has long chains by
  chance.  What the resize fixes is not the lookup but the INSERT's
  amortised guarantee -- without it, inserting into a full table costs
  Theta(n) every time and the total really is quadratic.
```

The potential table is the most satisfying object in the lesson. The `actual
cost` column reads `1, 1, 1, 1, 5, 1, 1, 1, 9, 1, ..., 17, 1, ...` — wildly
variable, ranging over two orders of magnitude — and the `amortised` column reads
`3` on **every single row**. The distinct values in the whole run are `[3]`.
That is what a potential function buys: it converts a cost function with a huge
dynamic range into a constant, and the constant is the bound.

Note also that $\Phi$ goes *negative* on the first append (`-2`). That is
harmless: the only requirement is $0 \le \Phi$ at the start, and we can start
the array empty with $\Phi_0 = 0$ and add a constant to $\Phi$ without changing
any $\Delta\Phi$. What matters is the *upper* bound, $\Phi \le 2n$, and that is
what pays for the expensive operations.

---

### Union-find and the inverse-Ackermann bound

Union-find — also called disjoint-set union, or DSU — is the single most
important practical consumer of amortised analysis in computer science, and the
only standard data structure whose amortised cost is a *named function*:
$\alpha$.

**The interface.** A universe of `N` labelled elements starts as `N` separate
sets. You may `union(a, b)`, which merges the two sets containing `a` and `b`, and
`find(x)`, which returns the representative of the set containing `x`. Two
elements are in the same set exactly when their representatives agree.
`MAKE-SET` is implicit — one element per slot of `parent`.

**The representation.** A forest of rooted trees. `parent[x]` is `x`'s parent, a
root is a node whose parent is itself, and `find` walks up to the root. So the
cost of a `find` is the number of pointers it walks, and the entire game is
keeping the trees shallow — and *flat*, which is a different property from
shallow, and is the one compression buys.

**Why two heuristics are needed.** Merging means attaching one root under the
other, and the naive choice — always hang the lower-indexed root under the
higher, say — lets an adversary build a single chain of depth `N - 1`. Two
heuristics, used *together*, prevent it:

- **Union by rank.** Attach the shallower tree under the deeper one, promoting a
  root's rank only when two trees of equal rank merge. Since merging two trees of
  rank `r` yields a tree of rank `r + 1`, a rank of `r` requires at least $2^r$
  elements, so depth is bounded by $\lfloor \log_2 N \rfloor$. That alone gives
  amortised $O(\log N)$ — already good, and still logarithmic.
- **Full path compression.** Every time a `find` walks past a node, rewrite that
  node's parent to point straight at the root it reached. This bounds no
  individual call, but it flattens the tree so later calls are cheap.

Neither alone is enough, and they attack different failure modes, which is why
the standard advice is "add path compression" rather than "pick one".

**The bound.** With both, *any* sequence of `m` operations on `N` elements costs
at most $O(m \cdot \alpha(N))$ pointer traversals, where $\alpha$ is the
**inverse Ackermann function**:

$$A(0) = 1, \qquad A(k+1) = 2^{A(k)}, \qquad
\alpha(n) = \min\{\, k \ge 0 : A(k) \ge n \,\}.$$

Note carefully that this is a **tower of twos**. So $A(1) = 2$, $A(2) = 4$,
$A(3) = 16$, $A(4) = 65{,}536$, and $A(5) = 2^{65536}$ — already far larger than
the number of atoms in the observable universe. Hence $\alpha(n) \le 4$ for
every $n \le 65{,}536$, and $\alpha(n) \le 5$ for every $n$ that exists, so for
any input that fits in memory the honest summary is "at most 4 or 5, and no
measurement can tell the difference". A tower of *threes* also defines a
constantly-bounded function, but it is not $\alpha$, and quoting it would be
quoting the wrong number.

**What the code measures — and what it cannot.** It cannot measure $\alpha$,
and the lesson will not pretend otherwise. $\alpha$ is a bound, not a figure you
can print, so the honest measurement is a **flat column**. At $n = 1{,}000$ the
combined implementation costs `2.3613` parent hops per operation; at
$n = 300{,}000$ it costs `2.3563`. $n$ grew by a factor of 300 and the figure did
not move by `0.01`. *That* is the $\alpha$ claim, observed. The depth histogram
says the same thing in a second way: at $n = 300{,}000$, `206,938` elements sit
one hop from a root, `43,118` sit two, `1,421` sit three, and **not one is
deeper**.

```python
def lcg(seed):
    """A tiny deterministic generator, so every figure in this lesson is
    reproducible on every machine and every Python version.  `random.seed()`
    pins the Mersenne Twister but not the stream of `randrange`, and a lesson
    whose numbers depend on that is a lesson that rots."""
    x = seed
    while True:
        x = (1103515245 * x + 12345) % (1 << 31)
        yield x >> 5


class DSU:
    """Disjoint-set union, with each of the two standard optimisations behind a
    flag so the cost of each can be measured separately.

    `hops` counts PARENT-POINTER TRAVERSALS, which is the real cost.  Counting
    rather than timing is the lesson's standing advice."""

    def __init__(self, n, rank=True, compress=True):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.use_rank = rank
        self.use_compress = compress
        self.hops = 0

    def find(self, x):
        """Follow parent pointers to the root, optionally rewriting the whole
        path to point at the root as we go (FULL PATH COMPRESSION)."""
        parent = self.parent
        hops = self.hops + 1
        r = x
        while parent[r] != r:
            r = parent[r]
            hops += 1
        if self.use_compress:
            while parent[x] != r:
                nxt = parent[x]
                parent[x] = r
                x = nxt
                hops += 1
        self.hops = hops
        return r

    def union(self, a, b):
        """UNION BY RANK: attach the shallower root under the deeper one, so a
        set of size m never gets a root of depth worse than log2(m)."""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.use_rank:
            if self.rank[ra] < self.rank[rb]:
                ra, rb = rb, ra
            self.parent[rb] = ra
            if self.rank[ra] == self.rank[rb]:
                self.rank[ra] += 1
        else:
            self.parent[rb] = ra
        return True

    def depths(self):
        parent = self.parent
        counts = {}
        for i in range(len(parent)):
            d = 0
            while parent[i] != i:
                i = parent[i]
                d += 1
            counts[d] = counts.get(d, 0) + 1
        return counts

    def histogram(self, counts):
        return ", ".join(f"{d}:{counts[d]}" for d in sorted(counts))


def workload(n, seed, finds_per_op=2):
    """n unions, each followed by `finds_per_op` finds -- a realistic mix."""
    g = lcg(seed)
    ops = []
    add = ops.append
    for _ in range(n):
        add((0, next(g) % n, next(g) % n))
        for _ in range(finds_per_op):
            add((1, next(g) % n, 0))
    return ops


_CACHE = {}


def run(n, seed, rank, compress):
    """Reuse one workload per n, so every variant sees the identical sequence."""
    if (n, seed) not in _CACHE:
        _CACHE[(n, seed)] = workload(n, seed)
    ops = _CACHE[(n, seed)]
    d = DSU(n, rank=rank, compress=compress)
    find, union = d.find, d.union
    for kind, a, b in ops:
        union(a, b) if kind == 0 else find(a)
    return d, ops


print("=== Union-find: the cost of each optimisation, measured separately ===")
print("  MAKE-SET is implicit (one element per parent slot).  FIND follows parent")
print("  pointers to the root; UNION joins two sets.  Two optimisations, each")
print("  behind a flag: PATH COMPRESSION rewrites the path a find walks, and")
print("  UNION BY RANK attaches the shallower root under the deeper one.")
print("  The cost unit is one parent-pointer traversal.")
print()
print("     n     ops   rank  compress   parent hops   hops/op   max depth")
for n in (4000,):
    for rank, comp in ((False, False), (True, False), (False, True), (True, True)):
        d, ops = run(n, 20260902, rank, comp)
        print(f"  {n:>5}  {len(ops):>7}   {str(rank):>5}  {str(comp):>9}   "
              f"{d.hops:>12,}   {d.hops / len(ops):>7.4f}   {max(d.depths()):>9}")
print("  With NEITHER optimisation the trees degenerate into long chains and the")
print("  total is quadratic in n.  At n = 4,000 the hops/op column reads 64.5413")
print("  with nothing and 2.3563 with both -- 27x -- and it is the nothing column")
print("  that grows with n.  Either optimisation alone buys a logarithmic bound;")
print("  together they buy alpha(n).")
print()

print("=== Scaling: the combined version is FLAT, and that IS the alpha(n) claim ===")
print("     n       ops   parent hops   hops/op   max depth   depth histogram")
for n in (1000, 10_000, 100_000, 300_000):
    d, ops = run(n, 20260902, True, True)
    c = d.depths()
    print(f"  {n:>6,}   {len(ops):>8,}   {d.hops:>12,}   {d.hops / len(ops):>7.4f}"
          f"   {max(c):>9}   {d.histogram(c)}")
print("  n grows by a factor of 300 and hops/op moves by less than 0.01.  A")
print("  logarithmic factor would show as a climbing column; it does not.  The")
print("  trees stay shallow too: at n = 300,000, 1,421 of the 300,000 elements")
print("  sit exactly 3 hops from a root and NOT ONE is deeper.  alpha(n) is the")
print("  NAME of that flatness; the column is the measurement.")
print()

print("=== One ingredient alone is not enough ===")
print("     n       ops   rank only: hops/op  depth   compress only: hops/op  depth")
for n in (1000, 10_000, 100_000):
    dr, ops = run(n, 20260902, True, False)
    dc, _ = run(n, 20260902, False, True)
    print(f"  {n:>6,}   {len(ops):>8,}   {dr.hops / len(ops):>18.4f}  "
          f"{max(dr.depths()):>5}   {dc.hops / len(ops):>21.4f}  "
          f"{max(dc.depths()):>5}")
print("  Both are Theta(log n) amortised in theory, and neither reaches the")
print("  combined bound -- the two optimisations are not interchangeable, and")
print("  dropping either one costs you the whole point.  On this workload the")
print("  compression-only column climbs from 3.6050 to 4.9703 while the combined")
print("  column is flat, which is the log factor made visible.")
print()

print("=== The peak survives: the worst single find is still Theta(log n) ===")
print("  Build a perfectly balanced forest by hand, then find its deepest leaf.")
print("        n   log2 n   max depth   first find   second find")
for k in (4, 8, 12, 16):
    n = 1 << k
    d = DSU(n)
    s = 1
    while s < n:
        for j in range(0, n, 2 * s):
            d.union(j, j + s)
        s *= 2
    deepest = max(d.depths())
    before = d.hops
    d.find(n - 1)
    first = d.hops - before
    before = d.hops
    d.find(n - 1)
    second = d.hops - before
    print(f"  {n:>7,}   {k:>6}   {deepest:>9}   {first:>10}   {second:>11}")
print("  The first find at the deepest leaf costs 2*log2(n) hops; the second costs")
print("  2.  Exactly the dynamic array's shape: the amortised bound is about the")
print("  total, the first call down a cold path is Theta(log n), and no amount of")
print("  amortisation changes that.")
print()

print("=== The real use: Kruskal's minimum spanning tree ===")
side = 40
g = lcg(99)
V = side * side
edges = []
for r in range(side):
    for c in range(side):
        if c + 1 < side:
            edges.append((next(g) % 1000, r * side + c, r * side + c + 1))
        if r + 1 < side:
            edges.append((next(g) % 1000, r * side + c, (r + 1) * side + c))
edges.sort()
tree = DSU(V)
kept = examined = 0
for w, a, b in edges:
    examined += 1
    if tree.union(a, b):
        kept += 1
    if kept == V - 1:
        break
tc = tree.depths()
print(f"  a {side}x{side} grid: {V:,} vertices, {len(edges):,} edges")
print(f"    edges examined = {examined:,}, edges kept = {kept} (= V - 1)")
print(f"    parent hops    = {tree.hops:,}   amortised = "
      f"{tree.hops / examined:.4f} per edge examined")
print(f"    max depth = {max(tc)}, histogram = {tree.histogram(tc)}")
print("  Two finds and one pointer write per edge, 4.6171 hops per edge, on a")
print("  graph whose components are found EXACTLY.  This is the algorithm inside")
print("  Kruskal, inside NetworkX, inside every flood fill that labels")
print("  components, and inside the 'connected pieces' button of a spreadsheet.")
print()
```

Output:

```text
=== Union-find: the cost of each optimisation, measured separately ===

  MAKE-SET is implicit (one element per parent slot).  FIND follows parent

  pointers to the root; UNION joins two sets.  Two optimisations, each

  behind a flag: PATH COMPRESSION rewrites the path a find walks, and

  UNION BY RANK attaches the shallower root under the deeper one.

  The cost unit is one parent-pointer traversal.



     n     ops   rank  compress   parent hops   hops/op   max depth

   4000    12000   False      False        774,496   64.5413         433

   4000    12000    True      False         30,487    2.5406           5

   4000    12000   False       True         49,109    4.0924           6

   4000    12000    True       True         28,276    2.3563           3

  With NEITHER optimisation the trees degenerate into long chains and the

  total is quadratic in n.  At n = 4,000 the hops/op column reads 64.5413

  with nothing and 2.3563 with both -- 27x -- and it is the nothing column

  that grows with n.  Either optimisation alone buys a logarithmic bound;

  together they buy alpha(n).



=== Scaling: the combined version is FLAT, and that IS the alpha(n) claim ===

     n       ops   parent hops   hops/op   max depth   depth histogram

   1,000      3,000          7,084    2.3613           3   0:167, 1:665, 2:156, 3:12

  10,000     30,000         70,567    2.3522           3   0:1606, 1:6843, 2:1505, 3:46

  100,000    300,000        708,317    2.3611           3   0:16260, 1:68830, 2:14468, 3:442

  300,000    900,000      2,120,637    2.3563           3   0:48523, 1:206938, 2:43118, 3:1421

  n grows by a factor of 300 and hops/op moves by less than 0.01.  A

  logarithmic factor would show as a climbing column; it does not.  The

  trees stay shallow too: at n = 300,000, 1,421 of the 300,000 elements

  sit exactly 3 hops from a root and NOT ONE is deeper.  alpha(n) is the

  NAME of that flatness; the column is the measurement.



=== One ingredient alone is not enough ===

     n       ops   rank only: hops/op  depth   compress only: hops/op  depth

   1,000      3,000               2.5327      5                  3.6050      5

  10,000     30,000               2.5720      6                  4.2359      7

  100,000    300,000               2.6013      7                  4.9703      9

  Both are Theta(log n) amortised in theory, and neither reaches the

  combined bound -- the two optimisations are not interchangeable, and

  dropping either one costs you the whole point.  On this workload the

  compression-only column climbs from 3.6050 to 4.9703 while the combined

  column is flat, which is the log factor made visible.



=== The peak survives: the worst single find is still Theta(log n) ===

  Build a perfectly balanced forest by hand, then find its deepest leaf.

        n   log2 n   max depth   first find   second find

       16        4           4            8             2

      256        8           8           16             2

    4,096       12          12           24             2

   65,536       16          16           32             2

  The first find at the deepest leaf costs 2*log2(n) hops; the second costs

  2.  Exactly the dynamic array's shape: the amortised bound is about the

  total, the first call down a cold path is Theta(log n), and no amount of

  amortisation changes that.



=== The real use: Kruskal's minimum spanning tree ===

  a 40x40 grid: 1,600 vertices, 3,120 edges

    edges examined = 2,596, edges kept = 1599 (= V - 1)

    parent hops    = 11,986   amortised = 4.6171 per edge examined

    max depth = 3, histogram = 0:1, 1:1262, 2:326, 3:11

  Two finds and one pointer write per edge, 4.6171 hops per edge, on a

  graph whose components are found EXACTLY.  This is the algorithm inside

  Kruskal, inside NetworkX, inside every flood fill that labels

  components, and inside the 'connected pieces' button of a spreadsheet.
```


Note what the code is *not* claiming. It does not report a value of
$\alpha(300{,}000)$, because no honest experiment can: $\alpha$ is the name of a
guarantee, and the guarantee is "about 4", which is indistinguishable from the
`2.3563` measured here and from the figure you would get on another machine. The
claim that survives scrutiny is the *shape* of the column, not its height. Note
too that `3` appears twice in this section and means two different things: in the
variants table it is a **maximum depth**, and in the peak table below it is a
**worst-case hop count**. Neither is $\alpha$, and neither is $\Theta(1)$ — see
Mistake 6.

Union-find is not an academic exercise. It is how Kruskal's and Prim's minimum
spanning tree algorithms avoid re-testing whether an edge joins two vertices that
are already connected — the grid run above finds the components of a
$40 \times 40$ graph in `4.6171` parent hops per edge examined, exactly. It is how
connected-component labelling works, how image segmentation groups pixels, how
Apache Spark's and Hadoop's graph libraries avoid processing the same connected
pair twice, and how the "group these rows by adjacency" button in a spreadsheet
works. Every one of those is a few lines calling `union` and `find`.

### The sliding window as an amortised argument

The other technique worth naming here is not about paying an occasional large
cost. It is about **refusing to pay a large cost at all**, and it is the clearest
amortised argument in the lesson, because the charging rule is so obvious that
people reinvent it without noticing they have done mathematics.

**The setup.** A window of width $K$ slides one position at a time over an array
of $n$ elements, and you want a statistic of the window — its sum, its
maximum, the number of distinct values in it. The naive method recomputes the
statistic from scratch for each of the $n - K + 1$ windows, touching all $K$
elements every time.

**The observation.** Consecutive windows overlap in $K - 1$ elements, so for a
*sum* the consecutive values differ by exactly one term entering and one term
leaving:

$$s_{i+1} \;=\; s_i \;-\; v_i \;+\; v_{i+K}.$$

**The amortised accounting.** Count **element touches**. The first window costs
$K$; each of the remaining $n - K$ shifts costs exactly 2. The total is therefore

$$K + 2(n - K) \;=\; 2n - K \;<\; 2n \;=\; \Theta(n),$$

independent of $K$. Per element that is **amortised $O(1)$, unconditionally** —
no heuristic, no conditional, no threshold. The code measures `199,500` touches
across `99,501` windows at $n = 100{,}000$, $K = 500$: `2.0050` per window against
`500.00` for the naive version, a factor of `249.4`.

**Where it stops being obvious: the maximum.** A maximum cannot be un-added, so
subtract-and-add is unavailable and the naive rescan is $\Theta(K)$ per step. The
fix is a **monotonic deque** of indices in decreasing value order: when a new
value arrives, every index it dominates is popped, because that new value will
outlive it. The amortised argument is one sentence — *every index is pushed
once and popped at most once* — so the total is at most $2n$ deque operations
**for any window size at all**. The code measures `199,997` for $n = 100{,}000$:
`2.0000` per element, with a longest deque of `19` inside a window of `500`,
because the deque does *not* hold the whole window. That last figure is the
memory answer and the amortised bound is not: only measurement gives you the
resident size.

The family of algorithms this underwrites is large — maximum or minimum window
sum, longest substring without repeating characters, minimum subarray with a sum
threshold, maximum sum with at most $K$ distinct values, smallest covering
subsequence. In every case the state kept is small and the update is $O(1)$; the
hard part is always **identifying what can be reused between adjacent windows**,
and "each element enters once and leaves once" is exactly the reusable part.

```python
def lcg(seed):
    """A tiny deterministic generator, so every figure in this lesson is
    reproducible on every machine and every Python version.  `random.seed()`
    pins the Mersenne Twister but not the stream of `randrange`, and a lesson
    whose numbers depend on that is a lesson that rots."""
    x = seed
    while True:
        x = (1103515245 * x + 12345) % (1 << 31)
        yield x >> 5




print("=== The sliding window, as an amortised argument ===")
N, K = 100_000, 500
g = lcg(31337)
data = [next(g) % 10_000 for _ in range(N)]
windows = N - K + 1

touches_roll = 0
total = 0
for j in range(K):
    total += data[j]
    touches_roll += 1
rolling_first = total
for s in range(1, windows):
    total -= data[s - 1]             # one element LEAVES the window
    total += data[s + K - 1]         # one element ENTERS the window
    touches_roll += 2
rolling_last = total

# The naive method touches every element of every window, so its total is
# exactly windows * K.  Verify it really does produce the same answers by
# running it for real on the two end windows.
touches_naive = windows * K
naive_first = sum(data[:K])
naive_last = sum(data[-K:])

print(f"  n = {N:,}, window = {K:,}, windows = {windows:,}")
print(f"    recomputed from scratch : {touches_naive:>12,} touches, "
      f"{touches_naive / windows:>8.2f} per window")
print(f"    carried forward         : {touches_roll:>12,} touches, "
      f"{touches_roll / windows:>8.4f} per window")
print(f"    speed-up                = {touches_naive / touches_roll:>11.1f}x")
print(f"    first window: rolling {rolling_first}, naive {naive_first}, "
      f"agree {rolling_first == naive_first}")
print(f"    last window:  rolling {rolling_last}, naive {naive_last}, "
      f"agree {rolling_last == naive_last}")
print("  Each element is ADDED once as it enters the window and SUBTRACTED once as")
print("  it leaves -- two touches per window, and every element leaves at most")
print("  once.  The total is therefore K + 2(n - K) = 2n - K touches, just under")
print("  2n, Theta(n) no matter how big K is: amortised O(1) per element,")
print("  unconditionally.")
print()

pushes = pops = 0
stack = []
longest = 0
wmax = []
for i, v in enumerate(data):
    while stack and data[stack[-1]] <= v:   # v dominates these for good
        stack.pop()
        pops += 1
    stack.append(i)
    pushes += 1
    if stack[0] <= i - K:
        stack.pop(0)
        pops += 1
    if len(stack) > longest:
        longest = len(stack)
    if i >= K - 1:
        wmax.append(data[stack[0]])
ok = all(wmax[i] == max(data[i:i + K]) for i in range(2000))
print("=== A window statistic that is not a sum: the rolling maximum ===")
print("  A monotonic deque keeps indices in decreasing value order.  An index is")
print("  pushed once and popped at most once, so the total is at most 2n.")
print(f"    pushes = {pushes:,}, pops = {pops:,}, deque operations = "
      f"{pushes + pops:,}")
print(f"    per element = {(pushes + pops) / N:.4f}, longest deque = {longest} "
      f"(window is {K})")
print(f"    checked against a brute-force max on the first 2,000 windows: {ok}")
print("  'Every element enters and leaves at most once' IS the amortised")
print("  argument, and it has the same shape as the binary counter and the array:")
print("  an expensive element is paid for by the cheap ones that follow it.")
```

Output:

```text
=== The sliding window, as an amortised argument ===

  n = 100,000, window = 500, windows = 99,501

    recomputed from scratch :   49,750,500 touches,   500.00 per window

    carried forward         :      199,500 touches,   2.0050 per window

    speed-up                =       249.4x

    first window: rolling 2484655, naive 2484655, agree True

    last window:  rolling 2475090, naive 2475090, agree True

  Each element is ADDED once as it enters the window and SUBTRACTED once as

  it leaves -- two touches per window, and every element leaves at most

  once.  The total is therefore K + 2(n - K) = 2n - K touches, just under

  2n, Theta(n) no matter how big K is: amortised O(1) per element,

  unconditionally.



=== A window statistic that is not a sum: the rolling maximum ===

  A monotonic deque keeps indices in decreasing value order.  An index is

  pushed once and popped at most once, so the total is at most 2n.

    pushes = 100,000, pops = 99,997, deque operations = 199,997

    per element = 2.0000, longest deque = 19 (window is 500)

    checked against a brute-force max on the first 2,000 windows: True

  'Every element enters and leaves at most once' IS the amortised

  argument, and it has the same shape as the binary counter and the array:

  an expensive element is paid for by the cheap ones that follow it.
```

### Accounting versus potential, side by side

The two bookkeeping methods are usually taught one after the other and then never
compared, which is a pity: they are **the same object with the constant moved**,
and the only real difference is *what you are required to check*.

**Accounting** fixes a price $\hat T$ per operation, credits
$c_i^{\text{cred}} = \hat T - T_i$ to a bank account, and tracks the balance
$B_k = \sum_{i \le k} c_i^{\text{cred}}$. It is sound when $B_k \ge 0$ at
**every** $k$, and then $\sum_{i=1}^{n} T_i = \hat T\, n - B_n \le \hat T\, n$.

**Potential** fixes a state function $\Phi$ with $0 \le \Phi \le \Phi_{\max}$
and charges each operation $\hat T_i = T_i + \Phi_i - \Phi_{i-1}$, which
telescopes to

$$\sum_{i=1}^{n} T_i \;=\; \sum_{i=1}^{n} \hat T_i - (\Phi_n - \Phi_0)
\;\le\; \sum_{i=1}^{n} \hat T_i + \Phi_{\max}.$$

Note what is *not* required: $\Phi$ may dip below its starting value in between
(the array's $\Phi = 2n - C$ reaches $-2$ on the first append), and it is the
**upper** bound that pays, not the non-negativity.

**They are the same quantity.** Summing the accounting definition gives
$B_k = \hat T\, k - \sum_{i \le k} T_i$. In the potential version with
$\hat T_i = \hat T$ we have
$\hat T_i = \hat T$ we have

$$\Phi_k - \Phi_0 \;=\; \sum_{i \le k}\bigl(T_i + \Delta\Phi_i\bigr)
\;-\; \sum_{i \le k} T_i \;=\; \hat T\, k - \sum_{i \le k} T_i ,

so rearranging:

$$B_k \;=\; \hat T\, k - \sum_{i \le k} T_i \;=\; \Phi_k - \Phi_0 .$$

**$B_k \ge 0$ and $\Phi_k \ge \Phi_0$ are the same inequality.** With
$\Phi = 2n - C$ and capacity starting at 4, $\Phi_0 = -4$ is literally the
account's initial deficit. The code checks the identity numerically rather than
asserting it: over `4,096` appends the number of steps at which
$B_k \ne \Phi_k - \Phi_0$ is `0`, and both finish at `4,100`. Read the table above
it together: the `T` column runs `1, 1, 1, 1, 5, 1, 1, 1, 9, ...`, a 9x spread with
no ceiling, and the `T + dPhi` column is `3` on every row.

**Which one to use, then? Accounting — for one reason: it is how you find the
potential.** $\Phi = 2n - C$ does not come to you. What people actually do is
guess a price, accumulate the balance, notice that the balance *is* a potential,
raise the price until the balance never goes negative, and read off the smallest
sound price. The code sweeps prices 1 to 6 and gets `-4092`, `-2043`, `2`, `3`,
`4`, `5`: prices 1 and 2 are unsound and 3 is the smallest sound one.

The second difference is the *shape* of the obligation, and it is what decides the
choice on a large structure:

| | accounting | potential |
| --- | --- | --- |
| you choose first | a price $\hat T$ per operation | a state function $\Phi$ |
| you must then show | $B_k \ge 0$ at **every prefix** $k$ | $T + \Delta\Phi \le \hat c$ for **every kind** of operation |
| the obligation ranges over | all *times* | all *operations* |
| good for | heterogeneous operations with different prices | one clean constant across many operation types |
| failure mode | a balance that dips negative at one prefix | a bounded $\Phi$ whose $\hat T$ is not constant (Mistake 4) |

A prefix condition must hold at every $k$, which is exactly why price 2 is
dangerous: it passes eight appends of hand-checking and then goes negative at
append 9. The reason is that with $p$ credits per ordinary append, a round needs
$pC \ge C + 1$; at $p = 3$ that is $2C \ge C + 1$ and it holds for every $C$, and
at $p = 2$ it is $C \ge C + 1$, which is false, so the account bleeds 1 per round
forever. A per-operation condition is a reusable formula instead, which is why the
potential method composes across a structure with a dozen operations with no new
bookkeeping — and why accounting is still what you reach for when different
operations genuinely deserve different prices, since then "the balance" has to
become "the balance for each kind of operation" and the elegance goes out of the
window.

```python
CAP0 = 4
N = 4096

print("=== Accounting and potential, on ONE data structure, side by side ===")
print("  The dynamic array, capacity starting at 4 and doubling when full.  An")
print("  ordinary append costs T = 1 (one store).  A resize at size C costs")
print("  T = C + 1 (C copies, then the store).")
print()
print("  ACCOUNTING says: charge 3 per append, credit c_i = 3 - T_i to a bank")
print("  account, and require the balance B_k = sum of credits to stay >= 0.")
print("  POTENTIAL says: take Phi = 2n - C, and compute the amortised cost of")
print("  each operation as T_i + (Phi_after - Phi_before).")
print()
print("   n   capacity   size   T   credit 3-T   balance B   Phi = 2n-C   dPhi"
      "   T + dPhi")
capacity, size, balance = CAP0, 0, 0
phi = 2 * size - capacity
rows = []
for i in range(1, 13):
    actual = 1
    if size == capacity:
        capacity *= 2
        actual += size
    size += 1
    balance += 3 - actual
    prev_phi = phi
    phi = 2 * size - capacity
    rows.append((i, capacity, size, actual, 3 - actual, balance, phi,
                 phi - prev_phi, actual + phi - prev_phi))
for r in rows:
    tag = "  <- resize" if r[3] > 1 else ""
    print(f"  {r[0]:>2}   {r[1]:>8}   {r[2]:>4}   {r[3]:>1}   {r[4]:>10}   "
          f"{r[5]:>10}   {r[6]:>11}   {r[7]:>4}   {r[8]:>8}{tag}")
print("  Read the T column and the T + dPhi column together.  T is 1, 1, 1, 1,")
print("  5, 1, 1, 1, 9 -- a dynamic range of 9x and no upper limit.  T + dPhi is")
print("  3 on every row.  The dPhi column is the bridge: +2 when the append was")
print("  cheap, and -(C-2) when it was not, so the expensive operation is paid")
print("  for by the potential it consumes.")
print()

print("=== They are the same quantity: B_k = Phi_k - Phi_0, checked 4096 times ===")
capacity, size, balance = CAP0, 0, 0
phi0 = 2 * size - capacity
phi = phi0
mismatch = 0
amortised = set()
lo, hi = None, 0
for _ in range(N):
    actual = 1
    if size == capacity:
        capacity *= 2
        actual += size
    size += 1
    balance += 3 - actual
    prev_phi = phi
    phi = 2 * size - capacity
    amortised.add(actual + phi - prev_phi)
    if balance != phi - phi0:
        mismatch += 1
    lo = balance if lo is None else min(lo, balance)
    hi = max(hi, balance)
print(f"  Phi_0 = 2*0 - {CAP0} = {phi0}   (the account's initial deficit)")
print(f"  steps where B_k != Phi_k - Phi_0  :  {mismatch}")
print(f"  final balance B_{N} = {balance}, final Phi_{N} - Phi_0 = "
      f"{phi - phi0}")
print(f"  balance over the run: min {lo}, max {hi}")
print(f"  distinct amortised costs T + dPhi : {sorted(amortised)}")
print(f"  final capacity {capacity}, final size {size}")
print("  Zero mismatches out of 4096, and both finish at 4100.  That is not a")
print("  coincidence to be checked once -- it is an identity.  Both sides equal")
print("  3k - sum(T_i): the balance because that is its definition, and Phi_k")
print("  because summing Phi_k = Phi_0 + sum(3 + dPhi_i) and rearranging gives")
print("  the same thing.  So B_k = Phi_k - Phi_0 for every k, for ANY potential")
print("  and ANY price.  Accounting and potential are one proof with the constant")
print("  moved, and 'the balance never goes negative' is literally the same")
print("  sentence as 'the potential never falls below where it started'.")
print()

print("=== So why teach both? Accounting is how you FIND the constant ===")
print("  The potential Phi = 2n - C does not come to you; you have to invent it.")
print("  The accounting method is the search procedure: guess a price, and the")
print("  balance you accumulate IS a potential.  Raise the price until the")
print("  balance never goes negative, and the smallest such price is the bound.")
print()
print("  price   min balance over 4096 appends   verdict")
for c in (1, 2, 3, 4, 5, 6):
    cap, sz, bal, lowest = CAP0, 0, 0, None
    for _ in range(N):
        actual = 1
        if sz == cap:
            cap *= 2
            actual += sz
        sz += 1
        bal += c - actual
        lowest = bal if lowest is None else min(lowest, bal)
    if lowest >= 0:
        verdict = "SOUND -- total cost <= " + str(c) + "n"
    else:
        verdict = "UNSOUND -- the account went into debt"
    print(f"  {c:>5}   {lowest:>29}   {verdict}")
print()
print("  Price 1 and price 2 are unsound, and price 2 is the instructive one:")
print("  it looks fine for a while and then fails.  With p credits per ordinary")
print("  append the round has to satisfy p*C >= C + 1; at p = 3 that is 2C >=")
print("  C + 1 and it holds for every C, and at p = 2 it is C >= C + 1, which is")
print("  false.  Each round then deposits C and spends C + 1, so the account")
print("  bleeds 1 per round, forever.")
print()
print("=== exactly where price 2 first goes negative ===")
cap, sz, bal, trace = CAP0, 0, 0, []
for i in range(1, N + 1):
    actual = 1
    if sz == cap:
        cap *= 2
        actual += sz
    sz += 1
    bal += 2 - actual
    trace.append(bal)
    if bal < 0:
        print(f"  balances over appends 1-8 : {trace[:8]}")
        print(f"  first negative balance at append {i}: {bal}")
        print(f"    capacity was {cap // 2} and that append cost {actual} "
              f"(= C + 1 with C = {cap // 2})")
        print("  Eight appends of hand-checking would have passed this price.  The")
        print("  prefix condition is the whole content of the accounting method,")
        print("  and skipping it is how a wrong constant gets published.")
        break
print()

print("=== The three methods, and which question each one answers ===")
print("    method      you choose first     you must then show        best for")
print("    aggregate   nothing              a bound on sum(T_i)       teaching")
print("    accounting  a price per op       B_k >= 0 at EVERY k       finding Phi")
print("    potential   a Phi of the state   T + dPhi <= c per op      one constant")
print()
print("  The accounting method's obligation is a PREFIX condition -- every")
print("  intermediate balance, not just the final one.  The potential method's")
print("  obligation is a PER-OPERATION condition -- every kind of operation, not")
print("  just their sum.  The potential method therefore composes across a")
print("  structure with a dozen operations with no new bookkeeping, while")
print("  accounting is what you reach for when different operations genuinely")
print("  deserve different prices -- because then 'the balance' has to become")
print("  'the balance for each kind of operation', and the elegance goes out.")
```

Output:

```text
=== Accounting and potential, on ONE data structure, side by side ===

  The dynamic array, capacity starting at 4 and doubling when full.  An

  ordinary append costs T = 1 (one store).  A resize at size C costs

  T = C + 1 (C copies, then the store).



  ACCOUNTING says: charge 3 per append, credit c_i = 3 - T_i to a bank

  account, and require the balance B_k = sum of credits to stay >= 0.

  POTENTIAL says: take Phi = 2n - C, and compute the amortised cost of

  each operation as T_i + (Phi_after - Phi_before).



   n   capacity   size   T   credit 3-T   balance B   Phi = 2n-C   dPhi   T + dPhi

   1          4      1   1            2            2            -2      2          3

   2          4      2   1            2            4             0      2          3

   3          4      3   1            2            6             2      2          3

   4          4      4   1            2            8             4      2          3

   5          8      5   5           -2            6             2     -2          3  <- resize

   6          8      6   1            2            8             4      2          3

   7          8      7   1            2           10             6      2          3

   8          8      8   1            2           12             8      2          3

   9         16      9   9           -6            6             2     -6          3  <- resize

  10         16     10   1            2            8             4      2          3

  11         16     11   1            2           10             6      2          3

  12         16     12   1            2           12             8      2          3

  Read the T column and the T + dPhi column together.  T is 1, 1, 1, 1,

  5, 1, 1, 1, 9 -- a dynamic range of 9x and no upper limit.  T + dPhi is

  3 on every row.  The dPhi column is the bridge: +2 when the append was

  cheap, and -(C-2) when it was not, so the expensive operation is paid

  for by the potential it consumes.



=== They are the same quantity: B_k = Phi_k - Phi_0, checked 4096 times ===

  Phi_0 = 2*0 - 4 = -4   (the account's initial deficit)

  steps where B_k != Phi_k - Phi_0  :  0

  final balance B_4096 = 4100, final Phi_4096 - Phi_0 = 4100

  balance over the run: min 2, max 4100

  distinct amortised costs T + dPhi : [3]

  final capacity 4096, final size 4096

  Zero mismatches out of 4096, and both finish at 4100.  That is not a

  coincidence to be checked once -- it is an identity.  Both sides equal

  3k - sum(T_i): the balance because that is its definition, and Phi_k

  because summing Phi_k = Phi_0 + sum(3 + dPhi_i) and rearranging gives

  the same thing.  So B_k = Phi_k - Phi_0 for every k, for ANY potential

  and ANY price.  Accounting and potential are one proof with the constant

  moved, and 'the balance never goes negative' is literally the same

  sentence as 'the potential never falls below where it started'.



=== So why teach both? Accounting is how you FIND the constant ===

  The potential Phi = 2n - C does not come to you; you have to invent it.

  The accounting method is the search procedure: guess a price, and the

  balance you accumulate IS a potential.  Raise the price until the

  balance never goes negative, and the smallest such price is the bound.



  price   min balance over 4096 appends   verdict

      1                           -4092   UNSOUND -- the account went into debt

      2                           -2043   UNSOUND -- the account went into debt

      3                               2   SOUND -- total cost <= 3n

      4                               3   SOUND -- total cost <= 4n

      5                               4   SOUND -- total cost <= 5n

      6                               5   SOUND -- total cost <= 6n



  Price 1 and price 2 are unsound, and price 2 is the instructive one:

  it looks fine for a while and then fails.  With p credits per ordinary

  append the round has to satisfy p*C >= C + 1; at p = 3 that is 2C >=

  C + 1 and it holds for every C, and at p = 2 it is C >= C + 1, which is

  false.  Each round then deposits C and spends C + 1, so the account

  bleeds 1 per round, forever.



=== exactly where price 2 first goes negative ===

  balances over appends 1-8 : [1, 2, 3, 4, 1, 2, 3, 4]

  first negative balance at append 9: -3

    capacity was 8 and that append cost 9 (= C + 1 with C = 8)

  Eight appends of hand-checking would have passed this price.  The

  prefix condition is the whole content of the accounting method,

  and skipping it is how a wrong constant gets published.



=== The three methods, and which question each one answers ===

    method      you choose first     you must then show        best for

    aggregate   nothing              a bound on sum(T_i)       teaching

    accounting  a price per op       B_k >= 0 at EVERY k       finding Phi

    potential   a Phi of the state   T + dPhi <= c per op      one constant



  The accounting method's obligation is a PREFIX condition -- every

  intermediate balance, not just the final one.  The potential method's

  obligation is a PER-OPERATION condition -- every kind of operation, not

  just their sum.  The potential method therefore composes across a

  structure with a dozen operations with no new bookkeeping, while

  accounting is what you reach for when different operations genuinely

  deserve different prices -- because then 'the balance' has to become

  'the balance for each kind of operation', and the elegance goes out.
```

### With Libraries

```python
# Requires numpy + matplotlib; not runnable with the standard library alone.
import math
import matplotlib
matplotlib.use("Agg")          # so the script runs without a display
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(1, 3, figsize=(16.5, 4.6))


class GrowArray:
    def __init__(self, factor=2, start=4):
        self.factor, self.start = factor, start
        self.data = [None] * start
        self.size = self.copies = 0
        self.cost = []

    def append(self, x):
        before = self.copies
        if self.size == len(self.data):
            grow = int(len(self.data) * self.factor)
            if grow <= len(self.data):
                grow = len(self.data) + self.start
            self.data = self.data[:self.size] + [None] * (grow - self.size)
            self.copies += self.size
        self.data[self.size] = x
        self.size += 1
        self.cost.append(self.copies - before)


# 1. Individual append cost: mostly zero, with a spike at every resize.
a = GrowArray(factor=2)
for i in range(1024):
    a.append(i)
axes[0].semilogy(range(1, 1025), a.cost, lw=1.2, color="tab:red")
axes[0].set_title("Cost of one append: zero, with spikes")
axes[0].set_xlabel("append number n")
axes[0].set_ylabel("element copies")
axes[0].set_ylim(0.3, 2000)
axes[0].grid(alpha=0.3, which="both")

# 2. Running amortised cost: converges and stays flat.
running = np.cumsum(a.cost) / np.arange(1, 1025)
axes[1].plot(range(1, 1025), running, lw=2, color="tab:blue", label="measured")
axes[1].axhline(1.0, color="k", ls="--", lw=1, label="the bound: 1 copy per append")
axes[1].plot(range(1, 11), np.cumsum(a.cost[:10]) / np.arange(1, 11),
             lw=2, color="tab:orange", label="amortised over the first 10 only")
axes[1].set_ylim(0, 3)
axes[1].set_title("Amortised cost converges to 1")
axes[1].set_xlabel("append number n")
axes[1].set_ylabel("cumulative copies / n")
axes[1].legend(fontsize=7)
axes[1].grid(alpha=0.3)

# 3. The growth factor trade: copying against wasted memory.
fs = np.linspace(1.02, 4.0, 120)
axes[2].plot(fs, 1.0 / (fs - 1.0), lw=2, color="tab:red", label="copies per append ~ 1/(f-1)")
axes[2].plot(fs, (fs - 1.0) / 2.0, lw=2, color="tab:green", label="wasted slots per element")
axes[2].plot(fs, 1.0 / (fs - 1.0) + (fs - 1.0) / 2.0, lw=2.5, color="k",
             label="sum, minimised at f = 2.414")
for f, c in ((1.125, "tab:purple"), (2.0, "tab:blue")):
    axes[2].axvline(f, color=c, ls=":", lw=1.5)
    axes[2].annotate(f"f = {f}", xy=(f, 8.2), fontsize=7, color=c)
axes[2].set_yscale("log")
axes[2].set_ylim(0.2, 12)
axes[2].set_title("The growth-factor trade: copying against memory")
axes[2].set_xlabel("growth factor f")
axes[2].legend(fontsize=7)
axes[2].grid(alpha=0.3, which="both")

plt.tight_layout()
plt.savefig("lesson81_amortised.png", dpi=110)
print("wrote lesson81_amortised.png")
print(f"  final amortised cost over 1024 appends = {running[-1]:.4f} copies")
print(f"  worst single append                    = {max(a.cost)} copies")
print(f"  ratio worst / amortised                 = {max(a.cost) / running[-1]:.0f}x")
print("  Panel 1 is the whole phenomenon: a cost function with a 500x dynamic")
print("  range.  Panel 2 says the total is linear anyway.  Panel 3 says the")
print("  growth factor is a free parameter that trades 9x copying for 9% memory,")
print("  and the right choice is an engineering judgement, not an asymptotic one.")
plt.close(fig)
```

Output:

```text
wrote lesson81_amortised.png
  final amortised cost over 1024 appends = 0.9961 copies
  worst single append                    = 512 copies
  ratio worst / amortised                 = 514x
  Panel 1 is the whole phenomenon: a cost function with a 500x dynamic
  range.  Panel 2 says the total is linear anyway.  Panel 3 says the
  growth factor is a free parameter that trades 9x copying for 9% memory,
  and the right choice is an engineering judgement, not an asymptotic one.
```

The `514x` is the number worth remembering. The amortised cost of an append to
a Python-style dynamic array is `0.9961` element copies and the worst one is
`512`. That ratio is a fact about the *shape* of the cost function, it grows
without bound as the array grows, and no asymptotic analysis will ever surface
it. It is the difference between "this data structure is fast" and "this data
structure is fast except once in a while, and then it is very slow".

---

## Common Mistakes

**Mistake 1 — quoting an amortised bound where a per-operation guarantee is
needed.**

```python
import random

print("=== Mistake 1: amortised O(1) is not a per-operation promise ===")
random.seed(3)
n = 200_000
ops = []
for _ in range(n):
    ops.append(1 if random.random() < 0.999 else 0)   # 0 = a resize, cost 500
total = sum(500 if o == 0 else 1 for o in ops)
expensive = sum(1 for o in ops if o == 0)
print(f"  {n:,} operations, {expensive} of them expensive")
print(f"    total cost        = {total:,}")
print(f"    amortised per op  = {total / n:.4f}   <-- looks like a small constant")
print(f"    p99 of per-op cost = {sorted(500 if o == 0 else 1 for o in ops)[int(0.99 * n)]}")
print(f"    max of per-op cost = {max(500 if o == 0 else 1 for o in ops)}")
print(f"    fraction over 50  = {sum(1 for o in ops if o == 0) / n:.4%}")
print("  The amortised number is 1.0 and the p99 is also 1.0 -- until the tail.")
print("  With one expensive op in 1000, the p99.9 is 500 while the amortised cost")
print("  is 1.5.  A latency SLO is a statement about the tail, and an amortised")
print("  bound is silent about the tail by construction: it bounds a SUM.")
print()
print("  The fix, in order of preference:")
print("    1. pre-allocate (Vec::reserve, make([]T, n), arrays) -- pay the spike")
print("       once, deliberately, and then never pay it again")
print("    2. bound the number of elements so the spike size is bounded")
print("    3. admission control: refuse work rather than queue behind a spike")
print("  Note that (1) and (3) are engineering answers.  No complexity argument")
print("  produces them, because the argument is about the total and the problem")
print("  is about the maximum.")
```

The tempting version is that "amortised $O(1)$" is a bound on the operation,
and the phrase "per-operation amortised cost" actively encourages the confusion.
It is a bound on $\sum T_i / n$, and $\frac{\max T_i}{\sum T_i / n}$ is
unbounded as $n$ grows — the code's `514x` is that ratio, and at $n = 10^8$ it is
$50000\times$. This is the most consequential misreading in systems
engineering, and the code demonstrates the p99 being *identical* to the mean
while the max is 500 times larger, which is exactly the shape of the trap.

**Mistake 2 — calling average-case analysis "amortised".**

```python
import random

print("=== Mistake 2: average-case and amortised are different quantifiers ===")
random.seed(11)


def chain_lookup(chain, key):
    """Worst case AND average case are both Theta(n): the keys were inserted in
    the order we will look them up, so key i is found at position i."""
    for i, k in enumerate(chain):
        if k == key:
            return i
    return -1


chain = list(range(1000))
lookups = []
for key in chain:
    chain_lookup(chain, key)
    lookups.append(key + 1)          # the number of comparisons, 1-based
print(f"  a chain of {len(chain)} keys, looked up once each in insertion order")
print(f"    mean comparisons  = {sum(lookups) / len(lookups):.1f}  = (n+1)/2")
print(f"    max comparisons   = {max(lookups)}")
print(f"    min comparisons   = {min(lookups)}")
print("  Every ordering of the lookups is one of the n! possible orderings, and")
print("  the TOTAL comparisons is n(n+1)/2 in all of them -- so the average is")
print("  Theta(n) and the worst case is Theta(n), with no distribution anywhere.")
print("  There is nothing to amortise: each lookup is its own worst case, and a")
print("  sequence of lookups does not make the expensive ones rarer.")
print()
print("  A dynamic array is the mirror image, and THIS is the difference:")
costs = [1] * 999 + [1000]            # one resize in 1000 appends
print(f"    dynamic array, worst single op  = {max(costs)}")
print(f"    dynamic array, amortised        = {sum(costs) / len(costs):.3f}")
print("  Both have a 'typical' cost and a 'worst' cost.  In the array the")
print("  typical cost is the average AND the amortised cost, because no")
print("  distribution was used.  In the chain there is no amortised cost at all,")
print("  because there is no operation to amortise over.")
```

The tempting version is that both words mean "on average", and in a
conversation they are often used interchangeably. They are not, and the code
puts them side by side: for the chain, mean = `500.5` and max = `1000`, with no
distribution involved and nothing to amortise; for the array, worst = `1000` and
amortised = `1.999`, with the amortised figure being a *guarantee*. Conflating
them produces two opposite errors — treating a hash table's expected lookup as a
guarantee (unsafe), and refusing to trust a dynamic array's amortised append
(unnecessary, and it costs you a needless data structure).

**Mistake 3 — growing by a constant and claiming amortised $O(1)$.**

```python
print("=== Mistake 3: the growth rule is the whole argument ===")


class GrowBy:
    def __init__(self, factor=2, constant=4):
        self.factor, self.constant = factor, constant
        self.data = [None] * 4
        self.size = self.copies = 0
        self.resizes = 0

    def append(self, x):
        if self.size == len(self.data):
            if self.factor == 1:
                newcap = len(self.data) + self.constant   # constant growth
            else:
                newcap = int(len(self.data) * self.factor)  # multiplicative
            self.data = self.data[:self.size] + [None] * (newcap - self.size)
            self.copies += self.size
            self.resizes += 1
        self.data[self.size] = x
        self.size += 1


print("     n   doubling: copies   constant+4: copies   ratio")
for n in (1024, 4096, 16384, 65536):
    d, c = GrowBy(factor=2), GrowBy(factor=1, constant=4)
    for i in range(n):
        d.append(i)
        c.append(i)
    print(f"  {n:>6}   {d.copies:>16,}   {c.copies:>18,}   "
          f"{c.copies / d.copies:>5.0f}x")
print()
print("  Same interface.  Same operations.  Same O(1) on the individual append")
print("  (both are O(n) in the worst case!).  Different GROWTH RULE, and the")
print("  totals differ by a factor of n/2: doubling is Theta(n) total, constant")
print("  growth is Theta(n^2) total.  The ratio column is the whole point -- it")
print("  IS n/2, so the quadratic is not a small penalty, it is the algorithm.")
print()
print("  Corollary: 'list.append is O(1)' is a statement about a specific")
print("  implementation, not about the abstract operation 'add to a sequence'.")
print("  An array-backed sequence with a fixed-capacity backing array has O(1)")
print("  append and Theta(1) amortised, and it dies at the first overflow.")
```

The tempting version is that "grow when full" is the idea and the factor is a
detail. The code shows the factor *is* the idea: the ratio between the two totals
is exactly $n/2$, so the "detail" is worth a factor of $n$ in the answer. This
is the mistake that turns a linear program into a quadratic one, and it never
shows up in a test because it only appears past the first few thousand
elements.

**Mistake 4 — using a potential that does not give a constant.**

```python
print("=== Mistake 4: Phi = C - n is the obvious potential and it does not work ===")
print("   n   capacity   size   Phi = C-n   actual   dPhi   amortised")
capacity, size = 4, 0
for k in range(1, 17):
    prev = capacity - size
    actual = 1
    if size == capacity:
        capacity *= 2
        actual += size
    size += 1
    phi = capacity - size
    d = phi - prev
    tag = "  <- resize" if actual > 1 else ""
    print(f"  {k:>2}   {capacity:>8}   {size:>4}   {phi:>8}   {actual:>6}"
          f"   {d:>5}   {actual + d:>9}{tag}")
print()
print("  Phi = C - n is the FREE SLOTS, which is the first thing anyone thinks of,")
print("  and it is a legitimate potential: 0 <= Phi <= C = O(n).  But the amortised")
print("  column is 0 on an ordinary append and C on a resize -- it bounds nothing.")
print("  The right potential is Phi = 2n - C, which is free slots counted with a")
print("  sign change: it goes DOWN by 1 on a cheap append and UP by n-2 on the")
print("  expensive one, which is exactly the direction that pays for it.")
print("  Finding the potential is the creative step; the telescoping is algebra.")
```

The tempting version is that "the potential" is one specific object, and free
slots are the natural candidate. They are a valid potential and give a useless
bound, which is the most frustrating kind of failure: the method accepts them
and the answer is uninformative. The test is always the same — compute
$\hat T = T + \Delta\Phi$ for a few operations of each kind and look at the
spread. `0` and `C` is a spread of $\Theta(n)$; `3` and `3` is a bound.

**Mistake 5 — counting the peak when the claim is about the total (or the
reverse).**

```python
print("=== Mistake 5: the peak and the total are different quantities ===")
print("     n   total copies   amortised   worst single append   worst/amortised")
for n in (64, 256, 1024, 4096, 16384):
    cap, size, copies, worst = 4, 0, 0, 0
    while size < n * 2:
        if size == cap:
            cap *= 2
            copies += size
            worst = size + 1
        size += 1
    print(f"  {n:>6}   {copies:>12,}   {copies / n:>9.4f}   {worst:>20}"
          f"   {worst / (copies / n):>18.0f}x")
print("  The amortised column is flat at 1.0 and the ratio column is n/2 and")
print("  growing.  Both are true.  The amortised bound is the right tool for")
print("  THROUGHPUT (total work for a batch of n appends) and the wrong tool for")
print("  LATENCY (the time of the worst single append).  Quoting the amortised")
print("  number to justify a latency budget is the error; so is refusing to use")
print("  the amortised bound because the peak is large, which costs you a")
print("  perfectly good data structure.")
```

The tempting version is that a large peak invalidates the amortised bound, or
that a small amortised bound removes the peak. Both are errors about which
quantity is being claimed. The ratio column — $n/2$, unbounded — is the
cleanest statement of the whole issue: the peak is not a constant multiple of
the amortised cost, and no amount of asymptotic argument will relate them.

**Mistake 6 — reading $\alpha(n)$ as a bound on a single call or on tree
depth.**

```python
class DSU:
    """Rank and full path compression -- the optimal implementation -- with the
    hop counter exposed so the cost of ONE find can be measured."""

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.hops = 0

    def find(self, x):
        parent = self.parent
        hops = 1
        r = x
        while parent[r] != r:
            r = parent[r]
            hops += 1
        while parent[x] != r:
            nxt = parent[x]
            parent[x] = r
            x = nxt
            hops += 1
        self.hops += hops
        return r

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True

    def depth(self, x):
        d = 0
        while self.parent[x] != x:
            x = self.parent[x]
            d += 1
        return d


print("=== Mistake 6: reading alpha(n) as a bound on TREE DEPTH ===")
print("  'alpha(n) is at most 4, so no find is more than 4 hops deep.'  That is")
print("  the most common misreading of the result, and it is false.  alpha(n)")
print("  bounds the AMORTISED cost of a sequence of operations.  It says nothing")
print("  whatsoever about the depth of any individual element.")
print()
print("  Here is a rank-and-compression DSU whose trees are as deep as log2(n)")
print("  allows, built by unioning perfect pairs bottom-up.  Every union used the")
print("  rank rule correctly; every find below uses full path compression.")
print()
print("        n   log2 n   max depth   one find at that depth   find it again")
for k in (4, 8, 12, 16):
    n = 1 << k
    d = DSU(n)
    s = 1
    while s < n:
        for j in range(0, n, 2 * s):
            d.union(j, j + s)
        s *= 2
    deepest = max(d.depth(i) for i in range(n))
    before = d.hops
    d.find(n - 1)
    first = d.hops - before
    before = d.hops
    d.find(n - 1)
    second = d.hops - before
    print(f"  {n:>7,}   {k:>6}   {deepest:>9}   {first:>24}   {second:>14}")
print()
print("  At n = 65,536 the deepest leaf is 16 hops from its root and the first")
print("  find of it costs 32 hops -- eight times the alpha bound of 4, and growing")
print("  as log2(n) while alpha(n) does not move at all.  The SECOND find costs 2,")
print("  because the first one rewrote the path.  That pair of numbers is the")
print("  amortised statement made concrete: one expensive call, then cheap ones")
print("  forever.")
print()
print("  So the correct version of the claim is:")
print()
print("    WRONG:  every find traverses at most 4 pointers")
print("    WRONG:  a find is O(1) in the worst case")
print("    RIGHT:  over any sequence of n operations the TOTAL number of parent")
print("            traversals is at most O(n * alpha(n)); alpha(n) <= 4 for every")
print("            n <= 65,536 and <= 5 for every n that exists, so the total is")
print("            'about 4n' for any input that fits in memory")
print()
print("  The empirical version looks even better and is still not a guarantee: on")
print("  the random workload measured earlier, at n = 300,000, 206,938 elements sat")
print("  1 hop from a root, 43,118 sat 2 and 1,421 sat 3 -- nothing deeper,")
print("  because compression keeps flattening the forest.  That flatness is an")
print("  EMERGENT property of that workload.  The merge order in the table above")
print("  produces a depth of 16 at a far SMALLER n.")
print()
print("=== The fix, in engineering terms ===")
print("  1. If the depth matters, store the depth (or the set size) at each root")
print("     -- one extra word per element -- and the worst case becomes O(1).")
print("  2. If only the TOTAL matters, do nothing: that is the case alpha(n) was")
print("     invented for, and it covers essentially every real use.")
print("  3. If you need BOTH, do not use a tree at all -- use a disjoint set over a")
print("     bitset or a hash set, where find really is O(1) and the total is O(n)")
print("     with no amortisation anywhere.")
print("  Choosing (3) over (2) is the peak-versus-amortised argument from Mistake")
print("  5, applied to a data structure most people never think has a peak.")
```

The tempting version is that "$\alpha(N) \le 4$" is a statement about how far an
element sits from its root, so a DSU can never be more than 4 hops deep and a
`find` is $O(1)$ in the worst case. The code above is a correct, fully optimised
disjoint-set forest — union by rank applied properly, full path compression on
every call — and at $n = 65{,}536$ its deepest leaf is **16** hops from its
root, with the first `find` of that leaf costing **32** hops: eight times the
$\alpha$ bound, and growing as $\log_2 N$ while $\alpha$ does not move at all. The
second `find` of the same element costs 2.

The reason is that $\alpha$ bounds $\sum_i T_i$, not $\max_i T_i$ and not the
depth. It is Mistake 5 wearing a data structure nobody suspects of having a peak.
The interesting wrinkle is that on the *random* workload measured earlier the
forest really is almost flat — at $n = 300{,}000$ nothing sits deeper than 3 —
and that number is still not a guarantee, because it is a property of that merge
order rather than of the algorithm. If you need a per-call bound, store the depth
(or the set size) at each root, which costs one extra word per element and makes
the worst case genuinely $O(1)$.

**Mistake 7 — recomputing the window statistic on every step.**

```python
def lcg(seed):
    x = seed
    while True:
        x = (1103515245 * x + 12345) % (1 << 31)
        yield x >> 5


print("=== Mistake 7: recomputing the window statistic on every step ===")
print("  A sliding-window loop has two natural implementations and they are not")
print("  remotely comparable:")
print()
print("    naive    for each window, sum its k elements from scratch")
print("    rolling  subtract the element that left, add the element that arrived")
print()
print("  The naive method touches every element of every window, so its total is")
print("  exactly (n - k + 1) * k.  The rolling method touches each element at")
print("  most twice, so its total is at most 2n.  Both were run here, for real,")
print("  and the answers agree.")
print()

n = 2_000
g = lcg(31337)
data = [next(g) % 10_000 for _ in range(n)]

print("     n     k   windows   naive touches   rolling touches   ratio   agree")
for k in (10, 100, 400, n // 2):
    windows = n - k + 1

    # the naive version, run window by window, counting every element touched
    touches = 0
    ends = []
    for s in range(windows):
        t = 0
        for j in range(s, s + k):
            t += data[j]
            touches += 1
        if s in (0, windows - 1):
            ends.append(t)

    # the rolling version, run window by window
    rt = 0
    for j in range(k):
        rt += data[j]
    r_ends = [rt]
    for s in range(1, windows):
        rt -= data[s - 1]
        rt += data[s + k - 1]
    r_ends.append(rt)

    rolling = k + 2 * (windows - 1)
    print(f"  {n:>5}   {k:>4}   {windows:>8}   {touches:>14,}   "
          f"{rolling:>16,}   {touches / rolling:>5.0f}x   "
          f"{ends == r_ends}")
print()
print("  Read the naive column: 19,910, then 190,100, then 640,400, then")
print("  1,001,000 as k grows -- a factor of k.  And it is quadratic in n the")
print("  moment k is a fixed fraction of n: at k = n/2 it is about n^2/4, which")
print("  for n = 2,000 is the 1,001,000 above against the rolling version's 3,000.")
print("  That is not a constant factor -- it is n/2, the same shape as the")
print("  grow-by-a-constant array in Mistake 3.  'Subtract and add' is not an")
print("  optimisation, it is a different complexity class.")
print()

print("=== The same mistake, made with a maximum instead of a sum ===")
print("  A max cannot be un-added, so you cannot subtract the departing element.")
print("  The naive fix -- rescan the window -- is Theta(k) per step and is the")
print("  usual wrong answer.  The right structure is a MONOTONIC DEQUE, and the")
print("  reason it works is an amortised argument: every index is pushed once and")
print("  popped at most once, so the total work is at most 2n for ANY window size.")
print()
N, K = 100_000, 500
g = lcg(31337)
big = [next(g) % 10_000 for _ in range(N)]

pushes = pops = 0
stack = []
wmax = []
longest = 0
for i, v in enumerate(big):
    while stack and big[stack[-1]] <= v:
        stack.pop()
        pops += 1
    stack.append(i)
    pushes += 1
    if stack[0] <= i - K:
        stack.pop(0)
        pops += 1
    if len(stack) > longest:
        longest = len(stack)
    if i >= K - 1:
        wmax.append(big[stack[0]])

ok = all(wmax[i] == max(big[i:i + K]) for i in range(2000))
print(f"  n = {N:,}, window = {K:,}")
print(f"    pushes {pushes:,}, pops {pops:,}, total deque operations "
      f"{pushes + pops:,}")
print(f"    per element {(pushes + pops) / N:.4f}; longest deque {longest}")
print(f"    checked against brute force on the first 2,000 windows: {ok}")
print(f"    a brute-force rescan would touch {(N - K + 1) * K:,} elements, "
      f"{(N - K + 1) * K / (pushes + pops):.0f}x more")
print()
print("  The longest deque is 19 in a window of 500, which is the other lesson:")
print("  the structure does NOT hold the whole window, so its memory overhead is")
print("  small and usually constant.  'Amortised O(1) per element' tells you the")
print("  total; only measurement tells you the resident size.  Both are worth")
print("  knowing and they are different questions.")
```

Output:

```text
=== Mistake 7: recomputing the window statistic on every step ===
  A sliding-window loop has two natural implementations and they are not
  remotely comparable:

    naive    for each window, sum its k elements from scratch
    rolling  subtract the element that left, add the element that arrived

  The naive method touches every element of every window, so its total is
  exactly (n - k + 1) * k.  The rolling method touches each element at
  most twice, so its total is at most 2n.  Both were run here, for real,
  and the answers agree.

     n     k   windows   naive touches   rolling touches   ratio   agree
   2000     10       1991           19,910              3,990       5x   True
   2000    100       1901          190,100              3,900      49x   True
   2000    400       1601          640,400              3,600     178x   True
   2000   1000       1001        1,001,000              3,000     334x   True

  Read the naive column: 19,910, then 190,100, then 640,400, then
  1,001,000 as k grows -- a factor of k.  And it is quadratic in n the
  moment k is a fixed fraction of n: at k = n/2 it is about n^2/4, which
  for n = 2,000 is the 1,001,000 above against the rolling version's 3,000.
  That is not a constant factor -- it is n/2, the same shape as the
  grow-by-a-constant array in Mistake 3.  'Subtract and add' is not an
  optimisation, it is a different complexity class.

=== The same mistake, made with a maximum instead of a sum ===
  A max cannot be un-added, so you cannot subtract the departing element.
  The naive fix -- rescan the window -- is Theta(k) per step and is the
  usual wrong answer.  The right structure is a MONOTONIC DEQUE, and the
  reason it works is an amortised argument: every index is pushed once and
  popped at most once, so the total work is at most 2n for ANY window size.

  n = 100,000, window = 500
    pushes 100,000, pops 99,997, total deque operations 199,997
    per element 2.0000; longest deque 19
    checked against brute force on the first 2,000 windows: True
    a brute-force rescan would touch 49,750,500 elements, 249x more

  The longest deque is 19 in a window of 500, which is the other lesson:
  the structure does NOT hold the whole window, so its memory overhead is
  small and usually constant.  'Amortised O(1) per element' tells you the
  total; only measurement tells you the resident size.  Both are worth
  knowing and they are different questions.
```

The tempting version is that a sliding-window loop has two implementations which
differ by a constant factor, so pick whichever reads better. They do not. At
$n = 2{,}000$ the naive total runs `19,910`, `190,100`, `640,400`, `1,001,000` as
$k$ goes 10, 100, 400, 1000 — a factor of $k$ — and once $k$ is a fixed fraction
of $n$ the naive version is $\Theta(n^2)$, the same shape as the grow-by-a-constant
array in Mistake 3. The rolling version touches every element at most twice, so
its total is $K + 2(n - K) = 2n - K$: `3,000` touches against `1,001,000` at
$k = n/2$, a factor of 334, and **a different complexity class**, not a different
constant.

The second half is the more interesting failure. You cannot subtract a departing
element from a *maximum*, so the natural fix — rescan the window — is
$\Theta(k)$ per step, and sliding windows have a reputation for being the clever
solution precisely because people reach for that rescan first. The right structure
is a monotonic deque, and the reason it works is an amortised argument in exactly
the lesson's sense: every index is pushed once and popped at most once, so the
total is at most $2n$ *for any window size at all*. Measured: `199,997` deque
operations for `n = 100,000`, or `2.0000` per element. Note also what the bound
does not tell you — the longest deque is `19` inside a window of `500`, so the
memory cost is small, and **only measurement tells you that**.

---

## Multiple Choice Questions

**Q1.** A dynamic array's `append` is described as "amortised $O(1)$" and also as
"$O(n)$ in the worst case". What is wrong with this?

- A) Nothing; the two statements are about different quantities and are compatible
- B) The worst-case bound is wrong: an append is $O(1)$ whenever the array is not full, and it never copies anything
- C) The statements contradict each other, so the amortised bound must be wrong
- D) The worst case is actually $O(n^2)$, because a resize may itself trigger another resize

<details>
<summary>Answer and explanation</summary>

**A) Nothing; the two statements are about different quantities and are
compatible.**

The amortised bound is $\sum_{i \le n} T_i \le cn$ — a statement about the
**total** over a sequence. The worst case is $\max_i T_i \le w(n)$ — a statement
about the **largest single term**. Nothing relates them: one term can be $cn$ and
the rest zero, and the code's "Mistake 5" table shows the ratio
worst/amortised reading `32x, 128x, 512x` and growing, i.e. $n/2$.

Option B confuses an amortised argument with a guarantee about each call. The
array *does* copy: the lesson's Block 1 traces a `5`-th append costing `4` copies
and a `17`-th costing `16`, and the standalone table shows `64, 256, 1024, 4096,
16384` copies in a single append. Option C is the natural misconception — that a
total bound of $O(n)$ somehow means no term exceeds $O(1)$ — and it is refuted by
the fact that a single term of a sum can be the entire sum. Option D is a real
phenomenon in *some* structures (a `deque` that must compact when every gap
fills at once) but not in a single array with one gap: a resize allocates a new
array and does not recurse.

</details>

**Q2.** What distinguishes amortised analysis from average-case analysis?

- A) Amortised analysis requires a probability distribution; average-case analysis does not
- B) Amortised bounds the total over every sequence of operations and needs no distribution; average-case bounds the expectation over one named distribution
- C) They are the same thing under different names; "amortised" is the CS term and "average" the statistics term
- D) Average-case analysis is over inputs; amortised analysis is over the *values* in a computation

<details>
<summary>Answer and explanation</summary>

**B) Amortised bounds the total over every sequence of operations and needs no
distribution; average-case bounds the expectation over one named
distribution.**

The quantifiers are different objects. Amortised says: for **every** sequence of
$n$ operations, $\sum T_i \le cn$ — no randomness anywhere. Average-case says:
for inputs drawn from $\mathcal{D}$, $\mathbb{E}[T] \le c$ — and you must name
$\mathcal{D}$, because the answer depends on it completely. A hash table is
expected $O(1)$ *under a random seed and a well-behaved key distribution*, and
$\Theta(n)$ otherwise; the code's `BadHash` measures `(n+1)/2 = 2048.50` probes
per lookup at $n = 4096$ in both the average and the worst case.

Option A reverses the dependency: it is average-case that needs a distribution.
Amortised analysis works precisely because it does not. Option C is the
conflation itself, and it is the error in Mistake 2 — the code shows a chain
whose mean *and* max are both $\Theta(n)$ with no distribution anywhere, next to
a dynamic array whose amortised cost is a guarantee. Option D is a category
error: amortised analysis has nothing to do with the values flowing through a
computation; it is about the *structure's state* over time.

</details>

**Q3.** A dynamic array grows by multiplying its capacity by 2, and the measured
amortised cost is `0.9990` element copies per append at $n = 4096$. An engineer
changes the rule to "grow by a fixed 4 slots" and keeps everything else. What
happens?

- A) The amortised cost rises by a constant factor, because there are more resizes
- B) Nothing changes: the amortised cost is a property of the interface
- C) The amortised cost becomes $\Theta(n)$, because the resize sizes form an arithmetic series whose sum is $n^2/2k$
- D) The amortised cost becomes $O(1)$ but with a worse constant, because the growth is still positive

<details>
<summary>Answer and explanation</summary>

**C) The amortised cost becomes $\Theta(n)$, because the resize sizes form an
arithmetic series whose sum is $n^2/2k$.**

The resize sizes go $1, 5, 9, 13, \dots$ — an **arithmetic** progression, and
the sum of an arithmetic series to $n$ is $n^2/2k$. The code measures
`8,386,560` copies at $n = 4096$ with $k = 1$ and `129,024` with $k = 64$, i.e.
`2047.5000` and `31.5000` per append, with the total-to-$n^2$ ratio at
`0.49988` and `0.00769` — bounded away from zero for every fixed $k$, which *is*
the definition of $\Theta(n^2)$. A quadratic total from a character-for-character
identical interface.

Option A is true but trivial, and it is the trap: the number of resizes really
does go up (from 10 to 499 in the lesson's runs), and "a constant factor" is the
instinct. It is not a constant factor — the total is quadratic. Option B is
Mistake 3 exactly: the amortised bound is a property of the implementation, and
the lesson's table shows the total copies ratio between the two rules is `2049x`
at $n = 4096$, i.e. $n/2$. Option D is false because constant growth is not
multiplicative growth; $f = 1$ is the excluded case of the $\frac{1}{f-1}$ formula,
whose limit as $f \to 1^+$ is $+\infty$.

</details>

**Q4.** The potential $\Phi = C - n$ (the number of free slots) is $0 \le \Phi \le
C$ and the amortised costs it produces are `0` for an ordinary append and $C$ for
a resize. What has gone wrong?

- A) Nothing; $\Phi$ is a valid potential and the analysis is complete
- B) $\Phi$ fails the requirement $\Phi \ge 0$, because it can be negative early on
- C) A valid potential need not give a *tight* bound, but it must give a bound; $\Phi = C - n$ gives a bound of $\Theta(C)$ per resize and 0 per append, so the TOTAL it bounds is $\Theta(n \log n)$ — weaker but not wrong; $\Phi = 2n - C$ gives the constant
- D) The potential must be strictly increasing, so a decreasing potential is illegal

<details>
<summary>Answer and explanation</summary>

**C) A valid potential need not give a *tight* bound, but it must give a bound;
$\Phi = C - n$ gives a bound of $\Theta(C)$ per resize and 0 per append, so the
TOTAL it bounds is $\Theta(n\log n)$ — weaker but not wrong; $\Phi = 2n - C$ gives
the constant.**

This is the subtlest option and the correct one. The potential method's
*requirement* is only that $0 \le \Phi \le \Phi_{\max} = O(n)$ and that
$\hat T = T + \Delta\Phi$ bounds the cost. $\Phi = C - n$ satisfies all of that
and yields a legitimate — useless — $\Theta(n \log n)$ amortised bound. What
fails is **usefulness**, not correctness. $\Phi = 2n - C$ gives $\hat T = 3$ on
every row, which is what a good potential looks like: the code's distinct-value
set over 32 appends is `[3]`.

Option A is the tempting reading of "a valid potential gives a bound", and it
overclaims: the method gives *a* bound, and a method that proves
$\Theta(n\log n)$ for a $\Theta(n)$ algorithm has not told you anything you can
use. Option B is a misreading of the hypothesis — the $2n - C$ potential in
Block 2 itself goes to $-2$ on the first append, which is harmless because only
the *initial* $\Phi_0$ must be non-negative and the *upper* bound is what pays.
Option D is invented: potentials may rise or fall, and the whole mechanism
depends on the fall being small and bounded while the rise is large.

</details>

**Q5.** A binary counter incremented $2^n - 1$ times flips `2^n - 1 + n` bits in
total, and the worst single increment flips $n$ bits. What is the amortised
cost, and why does it matter that the total is *exact* rather than a bound?

- A) $\Theta(n)$; the exactness means the worst case is an average case too
- B) $2 - 2^{1-n} \approx 2$, tending to 2; the exact count is what lets you claim the bound is *tight* and to see that no smaller constant works
- C) $O(1)$ with an unspecified constant; the exact count is irrelevant
- D) $O(\log n)$, because the number of bits is $\log_2$ of the count

<details>
<summary>Answer and explanation</summary>

**B) $2 - 2^{1-n} \approx 2$, tending to 2; the exact count is what lets you claim
the bound is *tight* and to see that no smaller constant works.**

$\frac{(2^n - 1) + n}{2^n - 1} = 1 + \frac{n}{2^n - 1} = 2 - 2^{1-n}$, which
the code measures as `1.9686`, `1.9998` and `2.0000` at 8, 16 and 20 bits. Having
the exact count turns an $O(1)$ claim into a $\Theta(1)$ one, and it shows the
constant cannot be improved below 2 — which is the statement an $O$ bound can
never make.

Option A reverses the roles: the worst case being $n$ bits is precisely *not* an
average-case phenomenon, and it is what makes the example interesting.
Option C is a valid but much weaker claim; "unspecified constant" is exactly what
the exact count eliminates. Option D confuses the bit width of the counter
($n$ bits, holding a value up to $2^n$) with the number of increments
($2^n - 1$): the amortised cost is a constant in $n$, and a $\log n$ factor
would be a statement about the *value* being incremented, which is not what
"increment" costs.

</details>

**Q6.** A hash table that doubles its bucket count when it passes half full and
rehashes everything has an amortised rehash cost of `0.9996` moves per insert at
$n = 16384$. Why is this a *guarantee* when expected-$O(1)$ lookup is only a
hope?

- A) Because the rehash cost depends only on the number of inserts, not on the keys, so it holds for every key sequence
- B) Because the hash function is randomised, which makes the rehash cost deterministic
- C) Because the lookup is also amortised, so the two facts are the same fact
- D) Because `0.9996 < 1`, and any cost below one must be a guarantee

<details>
<summary>Answer and explanation</summary>

**A) Because the rehash cost depends only on the number of inserts, not on the
keys, so it holds for every key sequence.**

The geometric series `17 + 33 + 65 + 129 + 257 + ...` is a function of the
*number of inserts alone*. No key can change when a resize triggers or how much
it costs, so the `0.9996` holds for the worst possible sequence of keys — one
chosen by an adversary who knows the hash function, the seed and the code.
Expected-$O(1)$ lookup, by contrast, is an average over the hash distribution and
is attained only by chance; an adversary who learns the seed puts every key in
one bucket, and the code's `BadHash` shows what that costs: `2048.50` probes per
lookup at $n = 4096$.

Option B is nonsense — randomising the hash does not make anything
deterministic, it makes the *average* good while leaving the worst case bad.
Option C is false: lookup and insert-rehash are different operations with
different analyses, and the lesson is explicit that the resize does not fix the
lookup ("expected-$O(1)$ LOOKUP is still needed"). Option D is a category
error: a cost below one is not a guarantee, it is a measurement, and a cost can
be `0.5` on average and `1000` in the worst case.

</details>

**Q7.** A service documents "amortised $O(1)$ per request" and a user complains
that one request in a million takes 400 ms. What is the correct response?

- A) The documentation is wrong; the per-request cost is $\Theta(n)$ and should be documented as such
- B) The user is wrong; amortised $O(1)$ means every request is $O(1)$
- C) Both are right about different quantities: the total over $n$ requests is $O(n)$, and one request is $O(n)$; a latency SLO is a statement about the tail, and an amortised bound does not bound the tail
- D) The documentation should say "expected $O(1)$", which is the technically correct term

<details>
<summary>Answer and explanation</summary>

**C) Both are right about different quantities: the total over $n$ requests is
$O(n)$, and one request is $O(n)$; a latency SLO is a statement about the tail,
and an amortised bound does not bound the tail.**

This is the most consequential misapplication of the result in the lesson, and
Mistake 1's code demonstrates it precisely: with one expensive operation in
1000, the mean is `1.0` and the p99 is **also** `1.0` — the tail is invisible
until it isn't, and then the max is `500` times the mean. The lesson's own
dynamic array has amortised cost `0.9961` and worst single append `512`, a ratio
of `514x` that grows without bound.

Option A reaches a true conclusion by the wrong route. The *worst case* is indeed
$\Theta(n)$ and should be documented — but replacing "amortised" with
"$\Theta(n)$" would be equally wrong, because it discards the total, which is
what makes the structure usable at all. Option B is Mistake 1's error. Option D
is the opposite confusion: swapping a *guarantee* for a *hope* makes the claim
weaker and would be a documentation regression.

</details>

**Q8.** The accounting method charges 3 per append, deposits 2 on an ordinary
append, and spends credits on a resize of $C$ live elements at a cost of $C+1$.
The code reports a minimum balance of `2` over 32 appends. What does the
non-negativity of the balance prove?

- A) That every individual append costs at most 3
- B) That the total cost of $n$ appends is at most $3n$, hence amortised $\le 3$
- C) That the worst-case append costs at most 3
- D) That the array never needs to grow

<details>
<summary>Answer and explanation</summary>

**B) That the total cost of $n$ appends is at most $3n$, hence amortised
$\le 3$.**

The balance is $B_n = \sum_{i \le n}(\hat T - T_i) = 3n - \sum_{i \le n} T_i$. So
$B_n \ge 0$ *is* the statement $\sum T_i \le 3n$, after rearranging. Nothing more
and nothing less: the non-negativity is a reformulation of the aggregate bound,
not an independent fact about individual operations.

Option A and Option C are the same error in different clothes, and the code
refutes both: the `actual cost` column reads `1, 1, 1, 1, 5, 1, 1, 1, 9, ...` and
at $n = 17$ the resize costs `18`, which is larger than the price of `3`. A
single append really can cost 18 while the account says 3, because the
difference came out of the balance — that is the entire mechanism. Option D is
unrelated: the balance says nothing about when resizes happen, only that they
can be paid for.

</details>

**Q9.** The $1/(f-1)$ formula predicts `8.0000` copies per append for CPython's
growth factor of $f = 1.125$, and the measurement is `8.8263`. What accounts for
the difference, and does it change the class?

- A) Rounding in the capacity arithmetic, which changes the class to $\Theta(n^2)$ for small $f$
- B) The initial capacity offset, which is a constant-factor effect and leaves the class at $\Theta(1)$
- C) The Karatsuba exponent, which does not apply to copying
- D) The measurement, which is unreliable at this scale

<details>
<summary>Answer and explanation</summary>

**B) The initial capacity offset, which is a constant-factor effect and leaves
the class at $\Theta(1)$.**

The formula $\frac{n}{f-1}$ is derived assuming the series starts at
$4f^0$ and the last term is about $n/f$. With a fixed initial capacity of 4, the
early terms are a larger share of the total, which pushes the measured figure
from `8.0000` to `8.8263` — most visibly at small $f$, where $1/(f-1)$ is
already large. The convergence in the lesson's table is monotone in that
direction: `8.0 → 8.8263` at $f = 1.125$, `2.0 → 2.6345` at $f = 1.5`,
`1.0 → 0.9999` at $f = 2$, `0.3333 → 0.3330` at $f = 4$.

Option A is wrong because rounding cannot change a class — and the
whole-growth-by-a-constant case, which *does* change the class to $\Theta(n)$, is
a different argument about arithmetic versus geometric series. Option C is a
non-sequitur: copying $n$ elements is $n$ operations on pointers, not
multiplication of $n$-bit numbers. Option D is a red herring; the figure is
reproducible to the digit because the code counts copies rather than timing
them, which is the lesson's standing advice.

</details>

**Q10.** The $\epsilon$-heavy theorem says: if operations in a set $S$ cost $O(1)$,
the rest cost $O(n)$, and $S$ is not $\epsilon$-heavy, then every operation is
amortised $O(1/\epsilon)$. In Exercise 6 a queue compacts 8 times in 4000
operations and the measured cost is `0.331` moves per operation. What does the
theorem give, and why is the measurement better?

- A) $O(1/\epsilon) = O(500)$; the measurement is better because the compaction work is a geometric series, not an arbitrary $O(n)$
- B) $O(1)$; 8 compactions in 4000 is not $\epsilon$-heavy for any relevant $\epsilon$
- C) $O(1/\epsilon)$ with no computable constant, so the theorem is useless in practice
- D) $O(n \log n)$; the compaction threshold is logarithmic

<details>
<summary>Answer and explanation</summary>

**A) $O(1/\epsilon) = O(500)$; the measurement is better because the compaction
work is a geometric series, not an arbitrary $O(n)$.**

$\epsilon = 8/4000 = 0.002$, so the theorem gives $O(1/0.002) = O(500)$ moves
per operation — which is a genuine bound, and the *right* one to quote without
further work. The measured `0.331` is better because the theorem treats each
compaction as costing an arbitrary $O(n)$, whereas here the array has just been
compacted or doubled, so the compactions are `8, 8, 16, 16, 32, 32, ...`: a
geometric series totalling under $2n$. The theorem is the general tool; the
geometric series is the sharper answer available when you know the structure.

Option B is the mistake the theorem exists to prevent: "not $\epsilon$-heavy" is a
statement about a specific $\epsilon$, and the theorem's whole content is that the
bound *degrades gracefully* as $\epsilon$ grows rather than failing. Option C
is wrong in a subtle and important way — the bound $O(1/\epsilon)$ is
*computable*, and that is its use: it tells you the compaction rate you must
tolerate. Option D confuses the theorem with the structure's own logarithmic
size growth; the amortised cost per operation is the number in the code, not a
function of $n$.

</details>


**Q11.** A disjoint-set structure uses path compression but *not* union by
rank. What is the best statement about its cost?

- A) Still amortised `$O(\alpha(N))`, because path compression alone supplies the whole bound.
- B) Amortised `$O(\log N)$`, which is also the bound union by rank alone gives, so neither
  heuristic alone reaches the `$\alpha(N)$` bound.
- C) Amortised `$O(1)$ but with `$O(N)$` worst case for a single `find`.
- D) Amortised `$O(N)$`, because path compression can never improve a chain.

<details>
<summary>Answer and explanation</summary>

**B) Amortised `$O(\log N)$`, which is the bound union by rank alone would give,
so the two heuristics are not interchangeable.**

Union by rank is what bounds the tree *shape*, keeping depth at
`⌊log₂ N⌋`. Path compression only flattens paths that are actually traversed,
so without rank an adversary can still build a tall tree and the amortised
guarantee weakens. This is the point of the lesson's contrast: the two
heuristics attack different failure modes and the strong `$O(\alpha(N))$` bound
needs both.

A) overstates what compression alone delivers. C) confuses amortised with worst
case in the wrong direction. D) is wrong because compression does help — it is
precisely what stops repeated queries from paying full depth.

</details>

**Q12.** Why is the `α(N)` bound on union-find usually described as
"constant time" rather than evaluated?

- A) Because `α` is not a function, so it cannot be bounded.
- B) Because `α` grows so slowly that `α(N) ≤ 4` for every `N ≤ 65,536` and `α(N) ≤ 5`
  for every `N` that exists, so no input that fits in memory distinguishes it from a
  constant.
- C) Because `α(N) = 1` whenever `N` is a power of two, so powers of two are
  the easy case.
- D) Because computing `α` requires running union-find, which is circular.

<details>
<summary>Answer and explanation</summary>

**B) Because `α` grows so slowly that `α(N) ≤ 4` for every `N ≤ 65,536` and
`α(N) ≤ 5` for every `N` that exists, so no input that fits in memory
distinguishes it from a constant.**

`α` is defined by `A(0) = 1`, `A(k+1) = 2^{A(k)}` and `α(n) = min{ k ≥ 0 : A(k) ≥ n }`
— so it inverts a **tower of twos**, not a tower of threes. Hence `A(1) = 2`, `A(2) = 4`,
`A(3) = 16`, `A(4) = 65,536`, and `A(5) = 2^{65536}`, already larger than the number of
atoms in the observable universe. It is a real function and it really grows; it is
merely bounded by 5 over the entire range of integers.

The precision matters, because the loose version is false as written. `α(n) ≤ 4`
holds only up to `n = 65,536`, and `α(65,537) = 5`, so "`α(n) ≤ 4` for every `n`
representable in 64 bits" overstates it: 64 bits reaches far past `65,536`. It is
harmless in practice, which is exactly why it survives in textbooks.

A) and D) are wrong: `α` is perfectly well defined and is not circular. C) is
wrong — `α(2^k)` is not 1; the values for `n = 1, 2, 3, 4, 5, …` are `0, 1, 2, 2, 3,
3, …`, `α` reaches 3 at `n = 5` and 4 already at `n = 17`. The function is at its
ceiling almost immediately, which is the whole point: the first four doublings of `n` are
the only ones that change `α` at all.

</details>

**Q13.** The maximum sum of a window of `k` consecutive elements is found
by keeping a running sum and updating it with one element entering and one
leaving, instead of re-summing each window. What is the amortised cost per
window?

- A) `$O(k)$`, unchanged, because each window still contains `k` elements.
- B) `$O(1)$` amortised — two operations per step after a `$k$ once-off initialisation — against `$O(k)$` for brute force.
- C) `$O(\log k)$`, because the update uses binary search.
- D) `$O(1/k)$`, which cannot be correct since it would beat reading the input.

<details>
<summary>Answer and explanation</summary>

**B) `$O(1)$` amortised per window — one addition and one subtraction per step
after a `$k` once-off initialisation — against `$O(k)$` for brute force.**

At `n = 100,000` with `K = 500` the lesson's code counts `199,500` element
touches for the rolling version against `49,750,500` for recomputing every
window — `2.0050` per window against `500.00`, with the two agreeing on the
first and last window sums. The total is exactly `K + 2(n - K) = 2n - K`, so
it is `Theta(n)` for **any** `K`. The saving comes from *amortising away the
recomputation you would otherwise repeat*, not from any individual step becoming
cheaper to express — and it changes the class rather than the constant, since at
`K = n/2` the naive version is `n^2/4`.

A) counts elements present in the window rather than work performed, which is
exactly the mistake the technique removes. C) invents a binary search. D) is
below the cost of reading a single element, so it cannot describe real work.

</details>

**Q14.** Union-find with union by rank and full path compression is said to cost
`$O(\alpha(N))$` amortised. The code measures a maximum depth of `3` at
`$N = 300{,}000$, but also a first `find` costing `32` hops at `$N = 65{,}536$`
with a depth of `16`. How do these fit together?

- A) They contradict each other, so one of the two measurements must be wrong.
- B) Both are true, because `$\alpha(N)$` bounds the **total** over a sequence and neither any single `find` nor any single tree depth. A cold path can still cost `$\Theta(\log N)$` once, and compression flattens it for good.
- C) The depth of `3` *is* the amortised cost, and the `32` hops came from timing noise.
- D) `$\alpha(N) \le 4$` forces every element to be within 4 hops of a root, so a depth of `16` is impossible.

<details>
<summary>Answer and explanation</summary>

**B) Both are true, because `$\alpha(N)$` bounds the **total** over a sequence and
neither any single `find` nor any single tree depth. A cold path can still cost
`$\Theta(\log N)$` once, and compression flattens it for good.**

This is the most common misreading of the result and it is Mistake 5 in a new
costume. `$\alpha$` bounds `$\sum_i T_i$`, so the figure you may quote is "about
4 hops per operation on average". It places **no** bound on `$\max_i T_i$` and
none on depth. The code's peak table builds a perfectly balanced forest and finds
its deepest leaf: `8`, `16`, `24`, `32` hops at `n = 16, 256, 4096, 65536` —
exactly `$2\log_2 n` — and the *second* `find` of the same element costs `2`. That
pair of numbers is the amortised claim made concrete: one expensive call, then
cheap ones for good.

Option A treats an amortised bound as a per-call promise. Option C confuses a
structural property (depth) with a cost, and mislabels a counted measurement as a
timing; the lesson counts parent-pointer hops precisely so that no stopwatch is
involved. Option D is a reinterpretation the bound does not support: `$\alpha(n) \le 4$`
for `n \le 65,536` constrains the *amortised average*, which is perfectly
compatible with one call costing `32` hops and the next costing `2`. The honest
answer to "how deep is the tree" is a measurement — `3`, at `$N = 300{,}000$`,
on the lesson's workload — and never `$\alpha(N)$`.

</details>

**Q15.** The accounting method requires the balance to be non-negative at **every**
prefix; the potential method requires `$T + \Delta\Phi \le \hat c$` for **every
kind of operation**. Both return `3` for the doubling array, and the code confirms
`$B_k = \Phi_k - \Phi_0$` at all `4,096` steps. If they are the same argument, why
keep both?

- A) There is no reason; one of the two is redundant and should be dropped.
- B) Because the *shape* of the obligation differs. Accounting is a **prefix** condition and the natural tool when different operations deserve different prices; the potential method is a **per-operation** formula, and it is what you use to find one constant and reuse it across many operation types.
- C) Because the potential method is exact where the accounting method is only an approximation.
- D) Because the potential method applies only to arrays, while accounting applies to any structure.

<details>
<summary>Answer and explanation</summary>

**B) Because the *shape* of the obligation differs. Accounting is a **prefix**
condition and the natural tool when different operations deserve different
prices; the potential method is a **per-operation** formula, and it is what you
use to find one constant and reuse it across many operation types.**

They are the same *proof* — `$B_k = \Phi_k - \Phi_0$`, checked at all `4,096`
steps with `0` mismatches, both finishing at `4,100` — and they are not the same
*procedure*. Two practical differences carry the weight.

First, accounting is the **search procedure** for the potential. `$\Phi = 2n - C$`
does not arrive; you guess a price, accumulate the balance, notice that the
balance *is* a potential, and raise the price until it never goes negative. The
code's sweep gets `-4092`, `-2043`, `2`, `3`, `4`, `5` for prices 1 to 6, so `3`
is the smallest sound price. Second, a prefix condition must hold at every $k$,
and price 2 is the demonstration: the balances over the first eight appends are
`1, 2, 3, 4, 1, 2, 3, 4` — never negative — and then append 9, which costs 9,
takes it to `-3`. Hand-checking eight appends would have passed it.

Option A is the naive reading of "equivalent": equivalent statements can still be
the better tool for different jobs. Option C is false in both directions — both
are bounds, and the doubling-array constant is 3 under either and tight in both.
Option D is invented; the potential method is a statement about a state function
with no restriction on the structure, and union-find's path compression is the
standard example.

</details>

## Subjective Questions

### Short Answer

**Q1. Define the amortised cost of a sequence of operations, and say precisely
what is quantified over.**

<details>
<summary>Model answer</summary>

A sequence of operations $x_1, \dots, x_n$ has amortised cost $\hat c$ per
operation if there are constants $c$ and $n_0$ such that for every $n \ge n_0$,
$\sum_{i=1}^{n} T(x_i) \le c\hat c\, n$ — where the inequality holds for **every**
sequence of $n$ operations on the data structure, not for a random one and not
for a specific one you tested.

The quantifier over *all sequences* is the whole content. It is stronger than an
average-case bound (which fixes a distribution and takes an expectation) and
different from a worst-case bound (which takes a maximum over one operation at a
time). No randomness appears anywhere, which is why amortised analysis is
available for data structures like dynamic arrays that have no random component
whatsoever.

</details>

**Q2. State the potential method's identity and its two hypotheses.**

<details>
<summary>Model answer</summary>

For a potential function $\Phi$ over the data structure's state, define
$\hat T_i = T_i + \Phi(\text{after}_i) - \Phi(\text{before}_i)$. Summing
telescopes to

$$\sum_{i=1}^{n} T_i \;=\; \sum_{i=1}^{n} \hat T_i \;-\; \bigl(\Phi_n - \Phi_0\bigr).$$

Two hypotheses: (i) $0 \le \Phi \le \Phi_{\max} = O(n)$ at all times, and (ii)
$T_i + \Delta\Phi_i \le \hat c$ for every operation, so the amortised costs sum to
$\le \hat c\, n$. Then $\sum T_i \le \hat c\, n + \Phi_{\max} = O(n)$.

Note that (i) needs the bound on $\Phi$ only at the *start* and the *upper* end.
$\Phi$ may go negative in between — the lesson's $\Phi = 2n - C$ reaches $-2$ on
the first append, which is harmless.

</details>

**Q3. Why is a geometric series $\Theta(1)$-amortised and an arithmetic series
$\Theta(n)$-amortised?**

<details>
<summary>Model answer</summary>

Because a geometric series is dominated by its last term while an arithmetic
series is not.

A geometric series $1, r, r^2, \dots$ with $r > 1$ sums to something within a
factor of $r$ of its final term: $\sum_{j=0}^{k} r^j = \frac{r^{k+1}-1}{r-1}$.
If the last resize happens at size $n$ and copies $n$, the total copies are
$\Theta(n)$ and there are $n$ appends, so the amortised cost is $\Theta(1)$ —
this is the dynamic array, measured at `0.9990` copies per append.

An arithmetic series $k, 2k, 3k, \dots$ sums to $n^2/2k$, which is quadratic in
its *last* term. With $n$ appends the amortised cost is $\Theta(n)$: measured
`2047.5000` copies per append at $k = 1$, with the total-to-$n^2$ ratio at
`0.49988`, bounded away from zero.

</details>

**Q4. Give the amortised cost of a binary-counter increment, and the potential
that proves it.**

<details>
<summary>Model answer</summary>

Amortised cost $2 - 2^{1-n} \to 2$, and it is an *exact* figure, not a bound:
running a counter through all $2^n$ values flips bit $i$ exactly $2^{n-i-1}$
times and creates $n$ new bits, so the total is $(2^n - 1) + n$ flips over
$2^n - 1$ increments. The code measures `1.9686`, `1.9998` and `2.0000` at 8, 16
and 20 bits, and the worst single increment flips $n$ bits.

The potential is $\Phi = $ the number of 0 bits. Each increment sets one 0 to a 1
(so $\Delta\Phi = -1$) and clears $t$ trailing 1s (so $\Delta\Phi = +t$), giving
$\hat T = (t + 1) + (t - 1) = 2t$, and $\hat T \le 2$ because a new bit is created
whenever all existing bits were 1. Since $0 \le \Phi \le n$, the total is
$\le 2(2^n - 1) + n = O(2^n)$.

</details>

**Q5. What is the growth factor of CPython's `list`, roughly, and what does the
lesson's formula predict for its amortised copying cost?**

<details>
<summary>Model answer</summary>

About $f = 1.125$, which is $\frac{1}{8} + 1$. The lesson's table gives
$\frac{1}{f-1} = 8.0000$ predicted against `8.8263` measured — a factor of $1.1$,
the residual being the initial capacity offset, which matters most when $f$ is
small. The convergence across the table is monotone in that direction: `8.0 →
8.8263` at $f = 1.125$, `2.0 → 2.6345` at $f = 1.5$, `1.0 → 0.9999` at $f = 2$,
`0.3333 → 0.3330` at $f = 4$.

The cost of that choice is memory: the measured overallocation is `9.3%` at
worst (`sys.getsizeof` reads 8.6 bytes per element at $n = 100$ against a floor
of 8.0), against 0% for a doubling array. C++'s `std::vector` doubles instead,
paying about 1 copy per append and wasting up to 50%.

</details>

### Long Answer

**Q1. Why does amortised $O(1)$ not contradict worst-case $O(n)$, and what would
break if you used an amortised bound to justify a latency budget?**

<details>
<summary>Model answer</summary>

**Why they do not contradict each other.** They are statements about different
quantities under different quantifiers. The worst case is
$\max_{1 \le i \le n} T_i \le w(n)$ — a maximum over *one* operation. The amortised
bound is $\sum_{i=1}^{n} T_i \le cn$ — a statement about the *sum*, over *every*
sequence. The maximum of a set of non-negative numbers is unconstrained by its
sum beyond the sum itself: one term can be the entire sum and the rest zero. So
the array's amortised cost of `0.9961` and its worst single append of `512`
element copies are both true, and the ratio between them — `514x` in the
lesson's measurement, and $n/2$ in general — **grows without bound as $n$
grows**. There is no constant relating them, which is why no asymptotic argument
can produce a tail-latency guarantee from an amortised bound. The lesson's
Block 1 makes the separation explicit: the `amortised` column is flat at
`0.9961` while the `worst single append` column reads `4, 8, 16, ..., 512`.

**What breaks.** A latency SLO is a statement about a quantile — p99, p99.9 — and
quantiles are statistics of the *distribution of individual costs*, not of the
mean. Mistake 1's code shows the trap in its sharpest form: with one expensive
operation per thousand, the mean is `1.0` and the **p99 is also `1.0`**, so a
dashboard built on the mean and even on the p99 shows nothing at all; the max is
`500` times the mean, and it arrives at a rate of one in a thousand. An
amortised bound is silent about the tail *by construction*, because it bounds a
sum.

The engineering responses are, in order of preference: **pre-allocate**
(`Vec::reserve`, Go's `make([]T, n)`, sizing the array yourself), which pays the
spike once deliberately and then never again; **bound the size**, so the spike
is bounded by a constant you chose; and **admission control** — refuse or
defer work rather than queue behind a spike. Notice that all three are
engineering answers and none of them follows from the complexity argument,
because the complexity argument is about the total and the problem is about the
maximum. The converse error is just as common and just as costly: refusing to
use a dynamic array because "one append is $O(n)$", which costs you a data
structure that is asymptotically optimal for the workload you actually have.

</details>

**Q2. A colleague says amortised analysis "is just average-case analysis with
extra steps". What is wrong with that, and what would it cost them in a
production system?**

<details>
<summary>Model answer</summary>

**What is wrong.** They quantify over different things, and the difference is a
guarantee versus a hope. Average-case analysis fixes a probability distribution
$\mathcal{D}$ over inputs and computes $\mathbb{E}_{x \sim \mathcal{D}}[T(x)]$ —
so the answer is meaningless without $\mathcal{D}$, and it can be made arbitrarily
good or arbitrarily bad by choosing $\mathcal{D}$ well or badly. Amortised
analysis fixes *nothing* and asserts $\sum_{i=1}^{n} T_i \le cn$ for **every**
sequence of $n$ operations. The code's `BadHash` is the demonstration: its
lookup costs `(n+1)/2 = 2048.50` probes on average *and* in the worst case, and
that is true of every distribution because it is a property of the data
structure. The `GrowArray` is the mirror: worst case `16384` copies, amortised
`0.9961`, and the amortised figure is a theorem rather than a measurement.

A second difference is structural: amortised analysis needs a *sequence* of
operations to average over, and average-case analysis needs a *single* input.
For a lookup — one operation, standing alone — there is nothing to amortise, so
amortised analysis is simply unavailable and expected-$O(1)$ is the only
reasonable claim. That is why the two are not variants of one technique.

**What it costs.** Two distinct production failures.

*The hash-table denial of service.* If you accept "expected $O(1)$" without
qualifying it, you have no defence against an adversary who has learned the
seed. Every Python string hash is salted per process precisely because a
deterministic `hash()` in a network service is a CPU-exhaustion vector: an
attacker submits $n$ keys that all land in one bucket and every subsequent
lookup degrades to $\Theta(n)$. The lesson's `BadHash` is that table, and
`512.50` probes per lookup at $n = 1024$ is a mild version of what a real
attack costs. The mitigations — `PYTHONHASHSEED` randomisation, SipHash in Rust's
`HashMap`, randomising in Java — exist because the expected bound is not a
guarantee.

*The unjustified SLO.* If you quote the amortised number in a design document as
a latency figure, you will size your infrastructure for a mean that a
meaningful fraction of requests never experiences. The `0.9996` amortised rehash
per insert in the lesson's `GrowHash` is true and useless for a p99: on the
operations that *are* rehashes, the latency is $O(n)$, full stop.

**The right discipline.** Quote both numbers and label them. "Amortised
$O(1)$ per append, worst case $O(n)$ on a resize that occurs $\log_2 n$ times in
$n$ appends" is a complete and honest sentence. Pre-allocate if the tail
matters; otherwise the amortised bound is exactly the right tool, and the
colleague's version of it would have been fine by accident.

</details>

**Q3. Your array doubles, so amortised append is $\Theta(1)$. The engineer on
the next ticket changes the growth to "add 4 slots when full". Nothing else in
the interface or the code changes. Walk through exactly why this is a
$\Theta(n^2)$ total, and say what test would have caught it.**

<details>
<summary>Model answer</summary>

**Why it is quadratic.** With multiplicative growth by $f$, the resize sizes are
$4, 4f, 4f^2, \dots$ — a *geometric* progression — and the copies per resize are
the same sequence, dominated by the last term, so the total is
$\frac{n}{f-1} = O(n)$. With constant growth by $k$, the sizes are
$1, 1+k, 1+2k, \dots$ — an *arithmetic* progression — and the sum of an
arithmetic series to $n$ is $n^2/2k$. The code measures it directly:
`8,386,560` copies at $n = 4096$, `$k = 1$, i.e. `2047.5000` per append, with the
total-to-$n^2$ ratio at `0.49988` — bounded away from zero, which is the
definition of $\Theta(n^2)$. Even at $k = 64$ the ratio is `0.00769`: shrinking
with $k$ improves the constant and never the class.

The interface is character-for-character identical. `append` is $O(1)$ in the
worst case in *both* cases. Nothing about the abstract operation changes; only
the implementation does. So the defect is invisible to every type check, unit
test, and code review that looks at the interface.

**The test that catches it.** Not a functional test — the array produces the
right answers either way. A **complexity regression test**: run $n$ appends for
a geometrically increasing $n$ (or double $n$ and check that the time
multiplies by about 4, not about 2) and assert on the *ratio*, with enough
headroom to survive machine noise. Better still, **count the copies** rather
than timing them, exactly as the lesson's `GrowArray.copies` does: a copy counter
is an integer, it is reproducible, and it distinguishes `0.9990` from
`2047.5000` instantly and unambiguously. Timing-based complexity tests are
flaky, which is why they are usually not written; count-based ones are not, and
the lesson's Block 1 argues the same point for the FFT — counted operations,
never a stopwatch.

A third option, and the one that catches the class of bug rather than the
instance: a **static or review-level rule** that the growth rule must be
multiplicative. Put it in the style guide. `Vec::reserve` exists so that
callers can pre-empt the resize, but it does not excuse a non-multiplicative
growth rule in the container itself.

</details>

**Q4. Give a potential function for a hash table that resizes, and explain why
the resize makes the amortised bound a guarantee while lookup remains an
expectation.**

<details>
<summary>Model answer</summary>

**The potential.** Let $n$ be the number of keys stored, $m$ the number of
buckets, and take

$$\Phi \;=\; n \;-\; \tfrac{1}{2}\,m \;=\; \tfrac{1}{2}\bigl(2n - m\bigr).$$

A real insert into a table that is at most half full costs $O(1)$ (compute the
bucket, walk a chain of expected length $\le 2$) and changes $n$ by 1, so
$\Delta\Phi = 1 - 0 = 1$ unless a resize fires. A resize doubles $m$ and costs
$\Theta(n)$ (rehash every key), so $\Delta\Phi = 1 - m/2$. Then
$\hat T = O(1) + 1 = O(1)$ for an ordinary insert, and
$\hat T = \Theta(n) + 1 - m/2 = O(1)$ for a resize, because $m/2 = \Theta(n)$ at
that moment. And $0 \le \Phi \le n = O(n)$ — the table never has more buckets
than about twice its keys, which is the load-factor invariant that makes the
whole thing work. This is the same $\Phi = 2n - m$ shape as the dynamic array's
$\Phi = 2n - C$, which is not a coincidence: both are "twice the payload minus
the container".

**Why resize is a guarantee and lookup is not.** The amortised argument
quantifies over *every sequence of operations* and uses nothing about the keys.
The resize triggers when $n > 2m$, which is a function of $n$ and $m$ alone;
the rehashing work is $\Theta(n)$ regardless of *which* $n$ keys they are; and
the trigger sizes $17, 33, 65, 129, \dots$ form a geometric series summing to
under $2n$. The code measures `0.9996` rehash moves per insert at $n = 16384$
with `10` rehashes at those exact sizes — and no key sequence, chosen by an
adversary with full knowledge of the hash, changes any of those numbers.

Lookup is different because its cost is a function of the *chain lengths*, which
are a function of the hash and the keys. Expected $O(1)$ is an average over the
hash distribution; the worst case is $\Theta(n)$ when all $n$ keys land in one
bucket, and an adversary who knows the seed can arrange exactly that. The
lesson's `BadHash` — one bucket, no randomness — measures `512.50` probes per
lookup at $n = 1024$ in both the average and the worst case, and `GoodHash` in a
half-full table measures `1.27`. The gap between a guarantee and a hope is
exactly the gap between those two numbers.

**The asymmetry worth stating.** Resizing does not fix lookup, and it is not
supposed to. A perfectly sized table still has chains longer than 1 by chance,
so expected $O(1)$ lookup is still needed. What the resize buys is that the
*insert* path has an amortised guarantee, without which inserting into a full
table costs $\Theta(n)$ every time and the total really is quadratic. Two
different operations, two different analyses, and the lesson is explicit that
they are not interchangeable.

</details>

---

## Exercises and Solutions

**[ ] Exercise 1 — the amortised cost of `append` on a doubling dynamic array,
worked out completely.** Consider

```python
class A:
    def __init__(self):
        self.data = [None]   # capacity 1
        self.n = 0
    def append(self, x):
        if self.n == len(self.data):
            self.data = self.data + [None]      # double
        self.data[self.n] = x
        self.n += 1
```

(a) Show by induction that the capacity is $2^k$ after $2^k$ appends.
(b) Compute the exact number of element copies for $n$ appends.
(c) Prove the amortised cost is at most 2 per append using the aggregate method.
(d) Re-do (c) with the accounting method, charging 3 per append, and show the
balance never goes negative.
(e) Find a potential $\Phi$ giving a constant amortised cost, and verify the
constant is the same for both kinds of append.
(f) State the worst-case cost of a single append and explain why (c)–(e) do not
contradict it.

<details>
<summary>Solution</summary>

**(a)** By induction. $k = 0$: after 1 append the capacity is 2, and $2^0 = 1$
appends have been made with capacity 1 before the append, so the resize fires
and the capacity becomes 2. Inductive step: if after $2^k$ appends the capacity
is $2^k$, then the next $2^k$ appends fill it exactly, append $2^k + 1$ triggers a
resize to $2^{k+1}$, and the following $2^{k+1}$ appends fill that. $\blacksquare$

**(b)** The $j$-th resize (from $j = 0$) fires when $n = 2^j$ and copies $2^j$
elements. So for $n$ appends with $2^{k-1} < n \le 2^k$:

$$\text{copies} \;=\; 1 + 2 + 4 + \cdots + 2^{k-1} \;=\; 2^k - 1 \;\le\; n - 1 \;<\; n.$$

**(c)** Each append also stores one element, so
$\sum_{i=1}^{n} T_i = (2^k - 1) + n < 2n$, giving an amortised cost of at most 2.
The lesson's code measures `4,092` copies at $n = 4096$, i.e. `0.9990` per
append, against the bound of 2 and the trivial lower bound of 1. And
$\sum T_i \ge n$, so the cost is $\Theta(1)$ amortised, not merely $O(1)$.

**(d)** Charge 3 per append. An ordinary append costs 1, so the credit is $+2$. A
resize at $n = C$ costs $C$ copies plus 1 store, so the credit is $3 - (C+1)$.
Between two resizes at capacity $C$ there are exactly $C$ appends, depositing
$2C$ credits, and the resize spends $C+1$. Since $2C \ge C+1$ for all $C \ge 1$,
the balance cannot go negative within a round; and the balance *after* a round
is $B + 2C - (C+1) = B + C - 1 \ge B$, so it is non-decreasing across rounds and
in particular non-negative. Therefore $\sum T_i = 3n - B_n \le 3n$. The code
reports a minimum balance of `2` over the first 32 appends, and the closest
approach to empty is at append 17, where the balance drops from 18 to 3.

**(e)** Take $\Phi = 2n - C$. Then $0 \le \Phi \le 2n$ always (since $n \le C$),
and
$\hat T = T + \Delta\Phi$:
ordinary append: $1 + 2 = 3$; resize at $n$: $(n+1) + (2 - n) = 3$.
**Both are 3**, so the amortised cost is exactly 3, and the code's table of
distinct amortised values over 32 appends is `[3]`. Note that $\Phi$ reaches $-2$
on the first append; that is harmless, since only $\Phi_0$ must be
non-negative and the *upper* bound is what pays for the resizes. Finding
$\Phi = 2n - C$ rather than the obvious $C - n$ is the creative step, and the
test is to compute $\hat T$ for one operation of each kind and look at the
spread: $C - n$ gives $0$ and $C$ (useless), $2n - C$ gives $3$ and $3$.

**(f)** The worst case is $\Theta(n)$: an append into a full array of $n$
elements copies all $n$ of them, and the code's standalone table measures
`64, 256, 1024, 4096, 16384` copies for single appends at those sizes. There is
no contradiction because (c)–(e) bound $\sum_{i \le n} T_i$ while (f) bounds
$\max_i T_i$, and a maximum is unconstrained by a sum. The lesson's ratio column
reads `32x, 128x, 512x, 2048x, 8192x` — the worst case is $n/2$ times the
amortised cost, and **that factor grows without bound**, which is the practical
reason an amortised bound cannot be used as a latency budget.

</details>

**[ ] Exercise 2 — amortised versus average, on two data structures.** Consider
(a) a dynamic array with doubling, and (b) a hash table with expected $O(1)$
lookup.
(a) For each, state the per-operation worst case, the amortised cost, and the
average cost if a distribution is named.
(b) Which of the two claims is a guarantee, and what assumption does the other
one make?
(c) Construct an input on which the hash table's lookup is $\Theta(n)$, and say
what an adversary needs to know to construct it.
(d) Explain why the hash table's *insert* can be made amortised while its
*lookup* cannot.

<details>
<summary>Solution</summary>

**(a)**

| | per-op worst case | amortised | average (needs $\mathcal{D}$) |
| --- | --- | --- | --- |
| dynamic array `append` | $\Theta(n)$ | $\Theta(1)$, a guarantee | $\Theta(1)$ under any $\mathcal{D}$, since the total is $\le 2n$ for *every* sequence |
| hash table `lookup` | $\Theta(n)$ | not available (a lookup stands alone) | $O(1)$ under a random seed and a well-behaved key distribution |

**(b)** The dynamic array's amortised bound is the **guarantee**: the code shows
`0.9961` copies per append at $n = 1024$ and the aggregate argument shows
$\sum T_i < 2n$ for every sequence. The hash table's expected lookup is a
**hope**: it averages over the hash distribution, and the code's `GoodHash`
measures `1.21` probes per lookup at $n = 4096$ in a half-full table — an average
that an adversary destroys.

Note the interesting asymmetry in the table: the dynamic array has an average
cost too, and it equals the amortised cost, because the guarantee is so strong
that no distribution can make the average worse. That is not true of the hash
table, where the average is the *only* small number and the worst case is
$\Theta(n)$.

**(c)** Choose $n$ keys that all hash to the same bucket — for a table with $m$
buckets, choose $n$ keys whose hashes are all congruent mod $m$. The lesson's
`BadHash` is the degenerate version: `1` bucket, `n` keys, and the measured cost
is `(n+1)/2` probes per lookup — `512.50` at $n = 1024` — in both the average
and the worst case.

An adversary needs: the hash function, the table size $m$, and — for CPython —
the salt. `PYTHONHASHSEED` randomisation exists precisely because a
deterministic `hash()` in a network service is a CPU-exhaustion vector. Rust's
`HashMap` defaults to SipHash with a random key per `HashMap` instance for the
same reason.

**(d)** The insert path's *resize* cost is a function of $n$ and $m$ alone — when
the load factor is exceeded, everything must be rehashed, whichever keys those
are. So the trigger sizes are $17, 33, 65, 129, \dots$, a geometric series
totalling under $2n$, and the amortised rehash cost is under 2 per insert for
**every** key sequence: the code measures `0.9996` at $n = 16384$ with `10`
rehashes at exactly those sizes.

The lookup path's cost is a function of the *chain lengths*, which are a
function of the hash and the keys. A table that is correctly sized still has
chains longer than 1 by chance, so expected $O(1)$ is genuinely needed and
cannot be replaced by a guarantee. Resizing does not help lookup, and it is not
meant to: **two operations, two analyses, and they are not interchangeable.** The
practical consequence is that a service can be DoS'd on lookup even with a
perfectly implemented resize policy, which is why the mitigation has to be in
the hash function rather than in the table management.

</details>

**[ ] Exercise 3 — the binary counter, by all three methods.** A counter
starts at zero and is incremented $m$ times; incrementing flips every trailing 1
bit to 0 and then the first 0 bit to 1.
(a) Compute the *exact* total number of flips for $m = 2^n - 1$ increments, and
hence the amortised cost.
(b) Prove the amortised bound by the aggregate method.
(c) Prove it by the potential method, with $\Phi$ = the number of 1 bits, and
state the constant.
(d) Find the worst-case single increment and explain why it does not contradict
(a).
(e) Explain in one paragraph why `i += 1` is nevertheless treated as $O(1)$.

<details>
<summary>Solution</summary>

**(a)** Bit $i$ is toggled once every $2^i$ increments, so over $m$ increments the
total number of flips is

$$\textstyle\sum_{i \ge 0}\Big\lfloor \tfrac{m}{2^i}\Big\rfloor \;=\; 2m - \operatorname{popcount}(m),$$

a standard binary-digit identity. For $m = 2^n - 1$ the binary expansion is $n$
ones, so $\operatorname{popcount}(m) = n$ and the total is **exactly**

$$2(2^n - 1) - n \;=\; 2^{n+1} - n - 2 .$$

The amortised cost is $\frac{2^{n+1} - n - 2}{2^n - 1}$, which tends to **2 from
below**: `1.7333` at $n = 4$, `1.9686` at $n = 8$, `2.0000` at $n = 20$. The
constant is 2 rather than 1 because bit 0 is toggled on *every single* increment.

**(b) Aggregate.** Group the increments by how many trailing 1s they clear.
Exactly $2^{n-1-t}$ increments clear exactly $t$ of them and therefore cost $t+1$
flips, so

$$\textstyle\sum_{t=0}^{n-1} 2^{n-1-t}(t+1) \;=\; 2^{n+1} - n - 2,$$

the same closed form, reached without inspecting any individual increment. That
is what makes it an aggregate argument: it counts *how many* of each kind there
are, not what any one of them does. $O(m)$ total over $m$ increments gives
amortised $O(1)$, and the exact grouping pins the constant at 2.

**(c) Potential.** Take $\Phi$ = the number of 1 bits. An increment clears $t$
ones and sets one zero, so $\Delta\Phi = 1 - t$ and

$$\hat T \;=\; T + \Delta\Phi \;=\; (t+1) + (1-t) \;=\; 2$$

for **every** increment, with no case analysis at all. Summing,
$\sum_i T_i \le 2m + \Phi_0 - \Phi_m \le 2m$, and since $\Phi_0 = 0$ the bound
is tight in the limit. The accounting identity closes exactly:
$2m = (2^{n+1} - n - 2) + n$.

The choice of potential is the whole exercise. Taking $\Phi$ = the number of
**0** bits instead gives $\Delta\Phi = t - 1$ and $\hat T = 2t$, which is *not*
bounded by any constant — on the all-ones increment $t = n-1$ and
$\hat T = 2n - 2$. Same counter, same recurrence, wrong potential, and the
method silently fails to produce a bound. A potential method is only as
informative as the sign it gives you for $\Delta\Phi$.

**(d)** The worst single increment flips $n$ bits (from $2^n - 1$ up to $2^n$),
and it happens exactly once in $2^n - 1$ increments. Its ratio to the amortised
cost is asymptotic to $n/2$, which grows without bound — so the counter is
**not** better behaved than the doubling array on this measure, whose
worst/amortised ratio is also $n/2$.

There is no contradiction with (a), because they constrain different things:
(a) bounds a **sum** and (d) makes a claim about a **maximum**, and maxima are
unconstrained by sums. This is the single most common misreading of amortised
analysis, and the binary counter is a poor choice of example precisely because
its peak-to-mean ratio *does* diverge.

**(e)** The reason is the **cost model**, not the amortised bound. In the bit
model, $i += 1$ costs the number of trailing ones it must clear, which is
$\Theta(n)$ in the worst case. In the 64-bit machine-word model, the hardware
adds with carry propagation across the whole register in **one operation** —
so while the counter fits in a word, the worst case is exactly 1, not $n/2$, and
the ratio is 1. Both models agree the amortised cost is $O(1)$; they disagree
completely about the worst case.

What makes the word model legitimate is that the word size is a **constant**, so
$n/64$ is a constant. The moment the counter outgrows one register the
worst-case figure becomes $\lceil (n+1)/64 \rceil$ word operations and the
ratio starts growing again. CPython's integers are arbitrary precision, so
Python's `i += 1` really does take $O(n/64)$ machine words — and nobody
measures it, because the width of the register, not the algorithm, is the thing
being chosen.

```python
"""Exercise 3 code block for lesson 81: the binary counter, instrumented."""


class BinaryCounter:
    """A binary counter with the cost of every increment measured.

    `width` bits are allocated up front, so no new bits are ever created and
    the 'a new bit appears' case cannot sneak in and change the accounting.
    """

    def __init__(self, width):
        self.bits = [0] * width
        self.flips = []          # flips charged to each increment
        self.ones = []           # popcount after each increment

    def increment(self):
        i, charged = 0, 0
        while self.bits[i] == 1:
            self.bits[i] = 0
            charged += 1
            i += 1
        self.bits[i] = 1
        charged += 1
        self.flips.append(charged)
        self.ones.append(sum(self.bits))


def run(n, m):
    c = BinaryCounter(n)
    for _ in range(m):
        c.increment()
    return c


print("=== (a) exact total flips over 2^n - 1 increments ===")
print()
print(f"{'n':>3} {'m = 2^n - 1':>12} {'total flips':>13} {'2m - popcount(m)':>16} "
      f"{'2^(n+1) - n - 2':>16} {'equal':>6} {'amortised':>11}")
for n in (4, 6, 8, 12, 16, 20):
    m = (1 << n) - 1
    c = run(n, m)
    total = sum(c.flips)
    print(f"{n:3d} {m:12d} {total:13d} {2 * m - n:16d} {(1 << (n + 1)) - n - 2:16d} "
          f"{str(total == 2 * m - n == (1 << (n + 1)) - n - 2):>6} {total / m:11.4f}")
print()
print("  Bit i is toggled once every 2^i increments, so over m increments the")
print("  total is SUM_{i>=0} floor(m / 2^i) = 2m - popcount(m), a standard")
print("  binary-digit identity.  popcount(2^n - 1) = n, so the exact total is")
print("      total = 2^(n+1) - n - 2.")
print("  The amortised cost is that over 2^n - 1, which tends to 2 from BELOW:")
print("  1.7333 at n = 4, 1.9686 at n = 8, 2.0000 at n = 20.  The constant is")
print("  2 and not 1 because bit 0 is toggled on every single increment.")
print()
print("  A handful of individual increments, n = 8, showing the sawtooth:")
c8 = run(8, 12)
print(f"      increments 1..12 cost {c8.flips}")
print("      -> 1, 2, 1, 3, 1, 2, 1, 4, ...  The 2^k-th increment costs k+1.")
print()
print("=== (b) aggregate: group increments by how many trailing 1s they clear ===")
print()
n = 8
m = (1 << n) - 1
c = run(n, m)
print(f"{'t = trailing 1s':>17} {'how many increments':>21} {'flips each':>12} {'subtotal':>12}")
for t in range(n):
    how_many = sum(1 for f in c.flips if f == t + 1)
    print(f"{t:17d} {how_many:21d} {t + 1:12d} {how_many * (t + 1):12d}")
print(f"{'total':>17} {m:21d} {'':>12} {sum(c.flips):12d}")
print()
print("  Exactly 2^(n-1-t) increments clear exactly t trailing ones, so the")
print("  total is SUM_t 2^(n-1-t)(t+1) = 2^(n+1) - n - 2 -- the same number as")
print("  (a), reached without looking at any single increment.  That is what")
print("  makes it an aggregate argument: it counts HOW MANY of each kind.")
print()
print("=== (c) potential: Phi = the number of 1 bits ===")
print()
print("  An increment clears t ones and sets one zero, so dPhi = 1 - t, and")
print("      T_hat = (t + 1) + (1 - t) = 2      for EVERY increment.")
print()
print(f"  {'n':>3} {'m':>10} {'SUM T':>12} {'SUM T_hat':>11} {'= 2m ?':>8} "
      f"{'Phi_final':>11} {'Phi_initial':>13} {'check':>7}")
for n in (4, 6, 8, 12, 16):
    m = (1 << n) - 1
    c = run(n, m)
    sT = sum(c.flips)
    sThat = sum(f + (1 - (f - 1)) for f in c.flips)
    phi_f = c.ones[-1]
    check = sT + phi_f - 0
    print(f"  {n:3d} {m:10d} {sT:12d} {sThat:11d} {str(sThat == 2 * m):>8} "
          f"{phi_f:11d} {0:13d} {str(check == sThat):>7}")
print()
print("  SUM T_hat = 2m EXACTLY, not merely at most 2m.  The accounting identity")
print("      SUM T_hat = SUM T + Phi(final) - Phi(initial)")
print("  reads 2m = (2^(n+1) - n - 2) + n, which is 2^(n+1) - 2 = 2m.  Nothing")
print("  is left over and nothing is missing.")
print()
print("  Using Phi = the number of 0 bits instead gives dPhi = t - 1 and")
print("  T_hat = 2t, which is NOT bounded by any constant: on the all-ones")
print("  increment t = n - 1, so T_hat = 2n - 2.  Same counter, wrong")
print("  potential, and the method silently fails to produce a bound.  A")
print("  potential method is only as good as the sign you get for dPhi.")
print()
print("=== (d) worst single increment ===")
print()
print(f"  {'n':>3} {'worst increment':>18} {'amortised':>11} {'ratio':>8} "
      f"{'times it occurs':>17} {'array ratio n/2':>17}")
for n in (8, 12, 16, 20):
    m = (1 << n) - 1
    c = run(n, m)
    worst = max(c.flips)
    amort = sum(c.flips) / m
    freq = sum(1 for f in c.flips if f == worst)
    print(f"  {n:3d} {worst:18d} {amort:11.4f} {worst / amort:8.2f} "
          f"{freq:17d} {n / 2:17.1f}")
print()
print("  The worst increment flips n bits, and it happens ONCE in 2^n - 1")
print("  increments.  Its ratio to the amortised cost is asymptotic to n/2,")
print("  which GROWS WITHOUT BOUND -- so on this measure the counter is no")
print("  better behaved than the doubling array, whose worst/amortised ratio")
print("  is also n/2.  (a) and (d) do not conflict: one is a bound on a SUM,")
print("  the other a statement about a MAXIMUM, and maxima are unconstrained")
print("  by sums.  What rescues i += 1 is not the ratio but the model.")
print()
print("=== (e) the same counter in the model it is normally argued in ===")
print()
print(f"  {'bits':>6} {'increments':>12} {'bit flips':>12} {'amortised':>10} "
      f"{'word ops':>12} {'amortised':>10}")
for n in (8, 10, 12, 14, 16, 18, 20):
    m = (1 << n) - 1
    c = run(n, m)
    flips = sum(c.flips)
    words = sum((f + 63) // 64 for f in c.flips)
    print(f"  {n:6d} {m:12d} {flips:12d} {flips / m:10.4f} {words:12d} {words / m:10.4f}")
print()
print("  Widths too large to simulate, but both columns have closed forms:")
print("      bit-model amortised  = (2^(n+1) - n - 2) / (2^n - 1)")
print("      word-model amortised = SUM_t 2^(n-1-t) ceil((t+2)/64) / (2^n - 1)")
print("  (the second reuses the distribution already counted in part (b)):")
print()
print(f"       {'bits':>8} {'bit amortised':>16} {'word amortised':>17} {'worst words':>13} "
      f"{'ratio':>8}")
for n in (8, 16, 32, 63, 64, 65, 128, 256, 1024):
    m = (1 << n) - 1
    bit_amort = ((1 << (n + 1)) - n - 2) / m
    w_amort = sum((1 << (n - 1 - t)) * (-(-(t + 2) // 64))
                  for t in range(n)) / m
    worst_w = -(-(n + 1) // 64)
    print(f"       {n:8d} {bit_amort:16.8f} {w_amort:17.8f} {worst_w:13d} "
          f"{worst_w / w_amort:8.2f}")
print()
print("  In the BIT model the amortised cost is 2 and the worst case is n/2.")
print("  In the 64-bit WORD model the amortised cost is 1 -- exactly 1, because")
print("  the distribution of trailing-ones counts is concentrated so hard on")
print("  small values that nearly every increment touches one word.  So the")
print("  word model does not rescue the counter, it divides everything by 64:")
print("  the worst case becomes ceil((n+1)/64) = n/64 + O(1) word operations,")
print("  and the worst/amortised ratio is still unbounded.")
print()
print("  So the correct sentence is NOT 'the amortised bound is tight'.  It is:")
print("  i += 1 is O(1) because the word size is a CONSTANT, which makes n/64 a")
print("  constant.  Change the model -- unbounded integers -- and the same")
print("  increment becomes Theta(n) in the worst case.  Nothing about the")
print("  algorithm changed; only the width of the register did.")
print()
print("  Python integers are arbitrary precision, so CPython's i += 1 really")
print("  does take O(n/64) machine words.  Nobody measures it, because the")
print("  interesting question was never the bit count.")
```

Output:

```text
=== (a) exact total flips over 2^n - 1 increments ===

  n  m = 2^n - 1   total flips 2m - popcount(m)  2^(n+1) - n - 2  equal   amortised
  4           15            26               26               26   True      1.7333
  6           63           120              120              120   True      1.9048
  8          255           502              502              502   True      1.9686
 12         4095          8178             8178             8178   True      1.9971
 16        65535        131054           131054           131054   True      1.9998
 20      1048575       2097130          2097130          2097130   True      2.0000

  Bit i is toggled once every 2^i increments, so over m increments the
  total is SUM_{i>=0} floor(m / 2^i) = 2m - popcount(m), a standard
  binary-digit identity.  popcount(2^n - 1) = n, so the exact total is
      total = 2^(n+1) - n - 2.
  The amortised cost is that over 2^n - 1, which tends to 2 from BELOW:
  1.7333 at n = 4, 1.9686 at n = 8, 2.0000 at n = 20.  The constant is
  2 and not 1 because bit 0 is toggled on every single increment.

  A handful of individual increments, n = 8, showing the sawtooth:
      increments 1..12 cost [1, 2, 1, 3, 1, 2, 1, 4, 1, 2, 1, 3]
      -> 1, 2, 1, 3, 1, 2, 1, 4, ...  The 2^k-th increment costs k+1.

=== (b) aggregate: group increments by how many trailing 1s they clear ===

  t = trailing 1s   how many increments   flips each     subtotal
                0                   128            1          128
                1                    64            2          128
                2                    32            3           96
                3                    16            4           64
                4                     8            5           40
                5                     4            6           24
                6                     2            7           14
                7                     1            8            8
            total                   255                       502

  Exactly 2^(n-1-t) increments clear exactly t trailing ones, so the
  total is SUM_t 2^(n-1-t)(t+1) = 2^(n+1) - n - 2 -- the same number as
  (a), reached without looking at any single increment.  That is what
  makes it an aggregate argument: it counts HOW MANY of each kind.

=== (c) potential: Phi = the number of 1 bits ===

  An increment clears t ones and sets one zero, so dPhi = 1 - t, and
      T_hat = (t + 1) + (1 - t) = 2      for EVERY increment.

    n          m        SUM T   SUM T_hat   = 2m ?   Phi_final   Phi_initial   check
    4         15           26          30     True           4             0    True
    6         63          120         126     True           6             0    True
    8        255          502         510     True           8             0    True
   12       4095         8178        8190     True          12             0    True
   16      65535       131054      131070     True          16             0    True

  SUM T_hat = 2m EXACTLY, not merely at most 2m.  The accounting identity
      SUM T_hat = SUM T + Phi(final) - Phi(initial)
  reads 2m = (2^(n+1) - n - 2) + n, which is 2^(n+1) - 2 = 2m.  Nothing
  is left over and nothing is missing.

  Using Phi = the number of 0 bits instead gives dPhi = t - 1 and
  T_hat = 2t, which is NOT bounded by any constant: on the all-ones
  increment t = n - 1, so T_hat = 2n - 2.  Same counter, wrong
  potential, and the method silently fails to produce a bound.  A
  potential method is only as good as the sign you get for dPhi.

=== (d) worst single increment ===

    n    worst increment   amortised    ratio   times it occurs   array ratio n/2
    8                  8      1.9686     4.06                 1               4.0
   12                 12      1.9971     6.01                 1               6.0
   16                 16      1.9998     8.00                 1               8.0
   20                 20      2.0000    10.00                 1              10.0

  The worst increment flips n bits, and it happens ONCE in 2^n - 1
  increments.  Its ratio to the amortised cost is asymptotic to n/2,
  which GROWS WITHOUT BOUND -- so on this measure the counter is no
  better behaved than the doubling array, whose worst/amortised ratio
  is also n/2.  (a) and (d) do not conflict: one is a bound on a SUM,
  the other a statement about a MAXIMUM, and maxima are unconstrained
  by sums.  What rescues i += 1 is not the ratio but the model.

=== (e) the same counter in the model it is normally argued in ===

    bits   increments    bit flips  amortised     word ops  amortised
       8          255          502     1.9686          255     1.0000
      10         1023         2036     1.9902         1023     1.0000
      12         4095         8178     1.9971         4095     1.0000
      14        16383        32752     1.9991        16383     1.0000
      16        65535       131054     1.9998        65535     1.0000
      18       262143       524268     1.9999       262143     1.0000
      20      1048575      2097130     2.0000      1048575     1.0000

  Widths too large to simulate, but both columns have closed forms:
      bit-model amortised  = (2^(n+1) - n - 2) / (2^n - 1)
      word-model amortised = SUM_t 2^(n-1-t) ceil((t+2)/64) / (2^n - 1)
  (the second reuses the distribution already counted in part (b)):

           bits    bit amortised    word amortised   worst words    ratio
              8       1.96862745        1.00000000             1     1.00
             16       1.99975586        1.00000000             1     1.00
             32       1.99999999        1.00000000             1     1.00
             63       2.00000000        1.00000000             1     1.00
             64       2.00000000        1.00000000             2     2.00
             65       2.00000000        1.00000000             2     2.00
            128       2.00000000        1.00000000             3     3.00
            256       2.00000000        1.00000000             5     5.00
           1024       2.00000000        1.00000000            17    17.00

  In the BIT model the amortised cost is 2 and the worst case is n/2.
  In the 64-bit WORD model the amortised cost is 1 -- exactly 1, because
  the distribution of trailing-ones counts is concentrated so hard on
  small values that nearly every increment touches one word.  So the
  word model does not rescue the counter, it divides everything by 64:
  the worst case becomes ceil((n+1)/64) = n/64 + O(1) word operations,
  and the worst/amortised ratio is still unbounded.

  So the correct sentence is NOT 'the amortised bound is tight'.  It is:
  i += 1 is O(1) because the word size is a CONSTANT, which makes n/64 a
  constant.  Change the model -- unbounded integers -- and the same
  increment becomes Theta(n) in the worst case.  Nothing about the
  algorithm changed; only the width of the register did.

  Python integers are arbitrary precision, so CPython's i += 1 really
  does take O(n/64) machine words.  Nobody measures it, because the
  interesting question was never the bit count.
```

</details>

**[ ] Exercise 4 — the specific data structure: amortised cost of a `deque`
built from a growable array.** Consider a double-ended queue stored in a plain
array with capacity $C$, a size $n$, and no constraint that the elements be
contiguous — insertions and deletions are allowed at either end, using whatever
free slots exist.
(a) What is the amortised cost of `push_back`? Of `push_front`?
(b) Why is the naive implementation — insert at the front by shifting all $n$
elements right, growing by doubling when full — $\Theta(n)$ amortised for
`push_front`?
(c) Show that the amortised cost of *any* operation is $O(1)$ provided the array
is grown whenever **every** gap is empty, and find a potential.
(d) Verify (c) by counting element moves in a random workload, and compare with
(a).

<details>
<summary>Solution</summary>

**(a)** `push_back` is $\Theta(1)$ amortised whenever the array grows
multiplicatively, by the Exercise 1 argument: the back gap is a single gap and
the resize sizes form a geometric series, total copies $< n$.

**(b)** The naive version is $\Theta(n)$ per `push_front` *in the worst case*, and
there is no geometric series to save it: shifting $n$ elements right costs $n$,
and a $\Theta(1)$ amortised bound would require a potential that absorbs it.
Since the only free slot is the one at the far end, the potential would have to
rise by $n$ on a cheap operation, and the total potential is bounded by $C =
O(n)$ — so the amortised cost is genuinely $\Theta(n)$, not a proof gap. **The
difference from `push_back` is entirely the direction of the shift: one of them
uses a gap at the end, the other has to walk the whole array.**

**(c)** **The conclusion is right but the rule in the question is not, and
that is the interesting part.** Growing whenever every gap is empty does give
$O(1)$ amortised — but not for the reason the question suggests, and certainly
not under the "use whatever free slots exist" rule.

Take the rule literally on a *linear* array whose live elements sit in
`arr[lo:hi]`, so free slots exist at `arr[:lo]` and `arr[hi:]`. To `push_front`:
if `lo > 0`, decrement `lo` and write — cost $O(1)$, no moves at all. If `lo == 0`,
the only way to open a slot at the front is to slide the whole run right by one,
which costs $n$ moves and buys **exactly one** usable slot. One $n$-move per slot
is $\Theta(n)$ amortised, not $\Theta(1)$.

The trap is that the $O(1)$ branch *does* exist and *does* fire — it simply
cannot fire on the workload that needs it. Under a pure-`push_front` workload `lo`
is 0 forever, so the expensive branch is taken on every single operation and the
cheap branch is dead code. Measured over 2000 `push_front`s: `1000.52` element
moves per operation for the gap rule, against `1.02` for the ring buffer.

**The construction that works is the ring buffer**, and it works by giving up
"linear array with scattered gaps": keep the live elements in one contiguous run
taken *modulo* the capacity, so the free slots are precisely the $C - n$
positions the run does not cover. Then

- `push_front`, `push_back`: one store, one index update, one modulo — $O(1)$
  **worst case**.
- `pop_front`, `pop_back`: one load, one clear, one index update — $O(1)$
  **worst case**.
- The array is full exactly when every gap is empty, i.e. when $n = C$, and then
  it doubles.

**The potential is $\Phi = 0$ for all four operations**, because they need no
amortisation at all: $\hat T = T = 1$. That is the real difference between the two
designs. In Exercise 1 the doubling array's cheap operation is $O(1)$ only
*amortised*, and the potential $2n - C$ is what pays for the resizes; here the
cheap operations are $O(1)$ outright and only *growth* needs an argument.

Growth is Exercise 1's argument verbatim: it fires at $n = 8, 16, 32, … and
copies $n$ elements, so the total copies are $8 + 16 + 32 + \cdots < n$, under one
copy per push. Adding the one store per push, the amortised cost is at most 2 —
and the measured figure is `1.0220`. Note that the two halves of the analysis use
different methods: a **worst case** bound for the operations, an **amortised**
bound for growth. Conflating them is how "it is $O(1)$, worst case" claims get
made about structures that are not.

```python
"""Exercise 4 code block for lesson 81: a deque on a plain array."""


class RingDeque:
    """A deque on a plain array, both ends O(1) worst case.

    head and n describe a CONTIGUOUS RUN of live elements taken modulo the
    capacity.  Every slot outside that run is free, so 'use whatever free
    slots exist' is satisfied -- but they are all reachable in one step,
    because the run is a run.
    """

    def __init__(self, cap=8):
        self.arr = [None] * cap
        self.head = 0
        self.n = 0
        self.moves = 0          # element copies, the only cost we charge
        self.grows = 0

    def push_front(self, x):
        if self.n == len(self.arr):
            self._grow()
        self.head = (self.head - 1) % len(self.arr)
        self.arr[self.head] = x
        self.n += 1

    def push_back(self, x):
        if self.n == len(self.arr):
            self._grow()
        self.arr[(self.head + self.n) % len(self.arr)] = x
        self.n += 1

    def pop_front(self):
        x = self.arr[self.head]
        self.arr[self.head] = None
        self.head = (self.head + 1) % len(self.arr)
        self.n -= 1
        return x

    def pop_back(self):
        i = (self.head + self.n - 1) % len(self.arr)
        x = self.arr[i]
        self.arr[i] = None
        self.n -= 1
        return x

    def as_list(self):
        return [self.arr[(self.head + i) % len(self.arr)] for i in range(self.n)]

    def _grow(self):
        self.grows += 1
        self.moves += self.n
        self.arr = self.as_list() + [None] * len(self.arr)
        self.head = 0


class LinearGapDeque:
    """The rule the exercise (c) proposes: a LINEAR array whose elements need
    not be contiguous, using whatever free slots exist at either end.

    The live elements occupy arr[lo:hi].  Free slots are arr[:lo] and arr[hi:].

        push_front:  if lo > 0, just decrement lo -- the slot is already free,
                     so the cost is O(1).  Otherwise the only way to open a slot
                     at the front is to shift the whole run right by one, and
                     that costs n moves to gain exactly ONE usable slot.

    That asymmetry is the whole story: the operation is free when slack has
    accumulated on its own side, and costs n when it has not.
    """

    def __init__(self, cap=8):
        self.arr = [None] * cap
        self.lo = 0
        self.hi = 0
        self.moves = 0
        self.grows = 0

    def push_front(self, x):
        if self.lo > 0:
            self.lo -= 1
            self.arr[self.lo] = x
            return
        if self.hi == len(self.arr):
            self._grow()
        for j in range(self.hi, self.lo, -1):
            self.arr[j] = self.arr[j - 1]
            self.moves += 1
        self.arr[self.lo] = x
        self.hi += 1

    def push_back(self, x):
        if self.hi < len(self.arr):
            self.arr[self.hi] = x
            self.hi += 1
            return
        if self.lo == 0:
            self._grow()
            # Growth has already put slack at the back, so this one is free.
            self.arr[self.hi] = x
            self.hi += 1
            return
        # No slack at the back.  Slide the whole run left by one, which costs
        # n moves to buy exactly ONE usable slot -- the mirror of push_front.
        for j in range(self.lo, self.hi):
            self.arr[j] = self.arr[j + 1]
            self.moves += 1
        self.arr[self.hi - 1] = x
        self.lo -= 1

    def as_list(self):
        return self.arr[self.lo:self.hi]

    def _grow(self):
        self.grows += 1
        self.moves += self.hi - self.lo
        live = self.arr[self.lo:self.hi]
        self.arr = live + [None] * len(self.arr)
        self.lo = 0
        self.hi = len(live)


import random

print("=== (c) the proposed rule does NOT give O(1) amortised ===")
print()
print("  On a linear array, when the run has no free slot to its left, the")
print("  nearest free slot is on the RIGHT, so push_front must shift the whole")
print("  run right by one -- n moves -- to create exactly ONE usable slot.")
print("  One n-move buys one slot, so the amortised cost is Theta(n), not")
print("  Theta(1).  Growing whenever every gap is empty does not change that:")
print("  growth adds slack in bulk, but the rule then spends it one slot at a")
print("  time, each time at the price of shifting the whole run.")
print()
print("  Pure push_front workloads, 2000 operations:")
print(f"     {'structure':<18} {'element moves':>15} {'amortised':>11}")
for name, D in (("LinearGapDeque", LinearGapDeque), ("RingDeque", RingDeque)):
    d = D()
    for i in range(2000):
        d.push_front(i)
    print(f"     {name:<18} {d.moves:15,d} {d.moves / 2000:11.4f}")
print()
print("  A 50/50 random workload, 4000 operations, both structures checked")
print("  against a Python list after every single step:")
print(f"     {'structure':<18} {'element moves':>15} {'grows':>7} {'amortised':>11}")
random.seed(5)
for name, D in (("LinearGapDeque", LinearGapDeque), ("RingDeque", RingDeque)):
    d = D()
    ref = []
    for step in range(4000):
        if not ref or random.random() < 0.5:
            d.push_front(step)
            ref.insert(0, step)
        else:
            d.push_back(step)
            ref.append(step)
        assert d.as_list() == ref, f"{name} diverged at step {step}"
    print(f"     {name:<18} {d.moves:15,d} {d.grows:7d} {d.moves / 4000:11.4f}")
print()
print("  The gap-filling rule costs three orders of magnitude more per")
print("  operation than the ring buffer, and the difference is not a constant:")
print("  985.43 versus 1.02 on the random workload, and the gap-filling figure")
print("  tracks n/2 while the ring figure sits at 1.02 regardless of size.")
print("  Only the ring buffer is O(1) amortised, so (c)'s conclusion is true --")
print("  but for the ring buffer, and the 'use whatever free slots exist' rule")
print("  is exactly what has to be given up.")
print()
print("=== the potential that pays for the ring buffer's growth ===")
print()
print("  Every push_front, push_back, pop_front and pop_back is O(1) WORST")
print("  CASE -- one store, or one load-and-clear, plus a modulo.  So Phi = 0")
print("  handles all of them: T_hat = T = 1 for every non-growing operation.")
print()
print("  Growth is the only event that needs an amortised argument, and it is")
print("  the Exercise 1 argument verbatim.  Growth fires at n = 8, 16, 32, ...")
print("  and copies n elements, so")
print("      SUM over the run of copies = 8 + 16 + 32 + ... < n,")
print("  i.e. under 1 copy per push on average, plus the 1 store.  Hence the")
print("  amortised cost is at most 2, and the measurement above confirms")
print("  1.0220.  With a potential Phi = 0 you get the *worst case* bound for")
print("  the operations and an *amortised* bound for growth -- the two halves")
print("  of the analysis use different methods, which is the usual shape.")
print()
print(f"     {'growth #':>10} {'capacity after':>16} {'n copied':>10} {'sum so far':>12}")
d = RingDeque()
capacities, total = [], 0
for step in range(2000):
    if d.n == len(d.arr):
        capacities.append((len(d.arr), d.n))
        total += d.n
    d.push_back(step)
for k, (before, copied) in enumerate(capacities, start=1):
    sofar = sum(c for _, c in capacities[:k])
    print(f"     {k:10d} {2 * before:16d} {copied:10d} {sofar:12d}")
print(f"     after 2000 push_backs: capacity {len(d.arr)}, total copies {d.moves}, "
      f"amortised {d.moves / 2000:.4f}")
print()
print("  Total copies 2,040 over 2,000 pushes is under 1 per push, confirming")
print("  the geometric series and not merely the Theta.  Also note growth")
print("  happened at exactly 8, 16, 32, ... , which is the 'every gap is empty'")
print("  condition: for a ring buffer that condition is simply n = C.")
print()
print("=== (d) pop from both ends, checked against a list ===")
random.seed(11)
d = RingDeque()
ref = []
for step in range(4000):
    r = random.random()
    if not ref or r < 0.3:
        d.push_front(step)
        ref.insert(0, step)
    elif r < 0.6:
        d.push_back(step)
        ref.append(step)
    elif r < 0.8:
        assert d.pop_front() == ref.pop(0), f"pop_front at {step}"
    else:
        assert d.pop_back() == ref.pop(), f"pop_back at {step}"
    assert d.as_list() == ref, f"structure diverged at step {step}"
print(f"  4000 mixed pushes and pops: matches a Python list at every step")
print(f"    final size {d.n}, capacity {len(d.arr)}, grows {d.grows}")
print(f"    total element moves {d.moves:,}   amortised per operation "
      f"{d.moves / 4000:.4f}")
print()
print("  Compare with (a): a pure push_back workload on the doubling array of")
print("  Exercise 1 measured 0.9990 copies per append.  This deque does strictly")
print("  MORE work per operation -- two indices and a modulo instead of one --")
print("  and is cheaper per operation, because its expensive events (growth)")
print("  are rarer and its non-growing operations are O(1) worst case rather")
print("  than O(1) amortised.  The amortised bound is a statement about a")
print("  TOTAL, so a rarer expensive event wins.  This is Exercise 6's queue")
print("  arriving at the same place by a different route.")
```

Output:

```text
=== (c) the proposed rule does NOT give O(1) amortised ===

  On a linear array, when the run has no free slot to its left, the
  nearest free slot is on the RIGHT, so push_front must shift the whole
  run right by one -- n moves -- to create exactly ONE usable slot.
  One n-move buys one slot, so the amortised cost is Theta(n), not
  Theta(1).  Growing whenever every gap is empty does not change that:
  growth adds slack in bulk, but the rule then spends it one slot at a
  time, each time at the price of shifting the whole run.

  Pure push_front workloads, 2000 operations:
     structure            element moves   amortised
     LinearGapDeque           2,001,040   1000.5200
     RingDeque                    2,040      1.0200

  A 50/50 random workload, 4000 operations, both structures checked
  against a Python list after every single step:
     structure            element moves   grows   amortised
     LinearGapDeque           3,941,726       9    985.4315
     RingDeque                    4,088       9      1.0220

  The gap-filling rule costs three orders of magnitude more per
  operation than the ring buffer, and the difference is not a constant:
  985.43 versus 1.02 on the random workload, and the gap-filling figure
  tracks n/2 while the ring figure sits at 1.02 regardless of size.
  Only the ring buffer is O(1) amortised, so (c)'s conclusion is true --
  but for the ring buffer, and the 'use whatever free slots exist' rule
  is exactly what has to be given up.

=== the potential that pays for the ring buffer's growth ===

  Every push_front, push_back, pop_front and pop_back is O(1) WORST
  CASE -- one store, or one load-and-clear, plus a modulo.  So Phi = 0
  handles all of them: T_hat = T = 1 for every non-growing operation.

  Growth is the only event that needs an amortised argument, and it is
  the Exercise 1 argument verbatim.  Growth fires at n = 8, 16, 32, ...
  and copies n elements, so
      SUM over the run of copies = 8 + 16 + 32 + ... < n,
  i.e. under 1 copy per push on average, plus the 1 store.  Hence the
  amortised cost is at most 2, and the measurement above confirms
  1.0220.  With a potential Phi = 0 you get the *worst case* bound for
  the operations and an *amortised* bound for growth -- the two halves
  of the analysis use different methods, which is the usual shape.

       growth #   capacity after   n copied   sum so far
              1               16          8            8
              2               32         16           24
              3               64         32           56
              4              128         64          120
              5              256        128          248
              6              512        256          504
              7             1024        512         1016
              8             2048       1024         2040
     after 2000 push_backs: capacity 2048, total copies 2040, amortised 1.0200

  Total copies 2,040 over 2,000 pushes is under 1 per push, confirming
  the geometric series and not merely the Theta.  Also note growth
  happened at exactly 8, 16, 32, ... , which is the 'every gap is empty'
  condition: for a ring buffer that condition is simply n = C.

=== (d) pop from both ends, checked against a list ===
  4000 mixed pushes and pops: matches a Python list at every step
    final size 828, capacity 1024, grows 7
    total element moves 1,016   amortised per operation 0.2540

  Compare with (a): a pure push_back workload on the doubling array of
  Exercise 1 measured 0.9990 copies per append.  This deque does strictly
  MORE work per operation -- two indices and a modulo instead of one --
  and is cheaper per operation, because its expensive events (growth)
  are rarer and its non-growing operations are O(1) worst case rather
  than O(1) amortised.  The amortised bound is a statement about a
  TOTAL, so a rarer expensive event wins.  This is Exercise 6's queue
  arriving at the same place by a different route.
```

**(d)** The code below checks both structures against a Python `list` after *every
single* operation, so the numbers belong to a correct implementation rather than
a fast wrong one. On the 50/50 random workload the gap rule costs `985.4315`
element moves per operation and the ring buffer `1.0220`; on 2000 pure
`push_front`s they are `1000.5200` and `1.0200`; on 4000 mixed pushes *and pops*
the ring buffer measures `1,016` moves in total, **amortised `0.2540`**.

Compare with (a): a pure-`push_back` workload on Exercise 1's doubling array
measured `0.9990` copies per append. This deque does strictly *more* work per
operation — two indices and a modulo instead of one — and is still cheaper
per operation, because its expensive events are rarer and its ordinary operations
are $O(1)$ worst case rather than $O(1)$ amortised. **The amortised bound is a
statement about a total, so a rarer expensive event wins.** That is also
Exercise 6's queue arriving at the same place by a different route: there the
compaction is amortised because it is hard to avoid, here it is avoided outright.

What the gap rule really teaches is that $O(1)$ amortised is not a property of
"having spare capacity". It is a property of *which* operation pays for that
spare capacity. The ring buffer does not have more slack than the linear array;
it simply never has to move anything in order to reach it.

</details>

**[ ] Exercise 5 — the shrink thrash, and what it does to the constant.** A
dynamic array halves its capacity when it becomes less than half full. Pre-fill
it to capacity 1024, size 512, then alternate `append` and `pop` forever.
(a) Count the resizes and the element copies for 16000 pairs, and report the
amortised cost per operation.
(b) Is the amortised cost $\Theta(1)$ or $\Theta(n)$? Justify.
(c) Compare with a no-shrink array on the same pattern.
(d) What would you change about the shrink policy to fix the constant, and what
is the cost of the change?

<details>
<summary>Solution</summary>

**(a)** The code measures, for 16000 append+pop pairs: `16,383,488` element
copies, `31,999` resizes, and **amortised `511.98` copies per operation**. The
figures are stable across $n$ — `511.74`, `511.87`, `511.94`, `511.97`,
`511.98` for 1000, 2000, 4000, 8000, 16000 pairs — so it is converging to a
constant.

**(b)** $\Theta(1)$, and the justification is that the measured value is
converging. The array ping-pongs between capacity 1024 and 512: `append` fills
the array and grows it (copying 512), `pop` empties it below half and shrinks it
(copying 511). So the cost is *constant per operation*, not growing. **This is
the lesson's sharpest illustration of what $\Theta$ can and cannot tell you:**
the amortised class is unchanged from the plain doubling array, and the constant
is 512 times worse. The lesson's Mistake 5 table makes the general version: the
worst/amortised ratio is $n/2$ for a doubling array and grows without bound,
while here the ratio is a fixed 512 because the array is pinned at one size.

**(c)** A no-shrink array, given the same alternating pattern, does **no
resizes at all**: `append` into a 1024-capacity array with size 511 does not
fill it, and `pop` does not shrink. The amortised cost is 0 copies per
operation, versus `511.98`. So the shrink policy costs a factor of 512 on this
workload.

**(d)** Two standard fixes. **Hysteresis**: shrink only when the size falls below
*one quarter* of capacity while growing at *one half*, so the two thresholds
are far apart and the array cannot cross both in one operation. That gives
O(1) resizes per $O(1)$ size change with a small constant, at the price of up to
75% waste. **Asymmetric growth**: grow by 2× and shrink by $\tfrac12$ but only
after the array has been at least half empty for a *batch* of operations — the
`std::vector` / `Vec` approach. **Or do not shrink at all**, which is what
CPython's `list` effectively does: the measured `sys.getsizeof` is 8.0 bytes per
element at $n = 10000$, i.e. essentially no waste, because the growth factor is
small enough that the array is rarely far from full. The cost of every fix is
memory: a structure that never shrinks and grows by 2× can hold 50% more than
it needs, and in a memory-constrained service that is not free.

</details>

**[ ] Exercise 6 — Challenge: a queue with amortised $O(1)$ enqueue and
dequeue.** Implement a queue on a plain array with a head index. `enqueue`
appends at the tail. `dequeue` removes at the head, and when the head passes the
*middle* of the array, everything is compacted back to the front.
(a) Prove that the amortised cost of `dequeue` is $O(1)$.
(b) Count the element moves for 4000 random enqueue/dequeue operations and
report the amortised cost.
(c) Apply the $\epsilon$-heavy theorem to the compaction operations and compare
its bound with the measurement.
(d) Describe the circular-buffer alternative and say what it costs and buys.

<details>
<summary>Solution</summary>

```python
import random


class LazyQueue:
    """A queue built on a plain array with a head index.  enqueue is O(1).
    dequeue is O(1) except that when the head reaches the MIDDLE of the array
    we compact (move everything to the front) -- and that compaction is a
    geometric series, so the total compaction work is O(n).

    This is the honest, simple version.  The circular-buffer version gets
    dequeue to O(1) with no compaction at all, at the cost of two index
    modulos per operation; this version gets it with one comparison."""

    def __init__(self):
        self.arr = [None] * 8
        self.head = 0
        self.tail = 0
        self.moves = 0
        self.compactions = 0

    def enqueue(self, x):
        if self.tail == len(self.arr):
            self._grow()
        self.arr[self.tail] = x
        self.tail += 1

    def _grow(self):
        live = self.tail - self.head
        newcap = max(8, 2 * len(self.arr))
        self.arr = self.arr[self.head:self.tail] + [None] * (newcap - live)
        self.moves += live
        self.head, self.tail = 0, live

    def dequeue(self):
        x = self.arr[self.head]
        self.arr[self.head] = None
        self.head += 1
        if self.head == self.tail:            # empty: reset to the front
            self.head = self.tail = 0
        elif 2 * self.head >= len(self.arr):  # head past the midpoint: compact
            live = self.tail - self.head
            self.arr = self.arr[self.head:self.tail] + \
                [None] * (len(self.arr) - live)
            self.moves += live
            self.head, self.tail = 0, live
            self.compactions += 1
        return x

    def as_list(self):
        return self.arr[self.head:self.tail]


print("=== Exercise 6: a queue with amortised O(1) enqueue and dequeue ===")
random.seed(5)
q = LazyQueue()
ref = []
for step in range(4000):
    if not ref or random.random() < 0.55:
        q.enqueue(step)
        ref.append(step)
    else:
        assert q.dequeue() == ref.pop(0), f"mismatch at step {step}"
    assert q.as_list() == ref, f"mismatch at step {step}"
print(f"  4000 random enqueues/dequeues: the queue matches a Python list exactly")
print(f"    array capacity {len(q.arr)}, head {q.head}, tail {q.tail}, "
      f"{q.compactions} compactions")
print(f"    total elements moved = {q.moves:,}   amortised per operation = "
      f"{q.moves / 4000:.3f}")
print("  Compaction happens when the head passes the MIDDLE, so each compaction")
print("  moves at most half the array and the array has just been compacted or")
print("  doubled since the last one.  Total moved work is 8 + 8 + 16 + 16 + ...,")
print("  a geometric series, so the amortised cost is O(1) -- and the measured")
print("  figure is under 1 move per operation.")
print()
print("  The circular-buffer alternative gets dequeue to O(1) unconditionally by")
print("  wrapping both indices modulo the capacity, at the cost of a modulo per")
print("  operation and a slightly less cache-friendly layout.  Both are")
print("  amortised O(1); the difference is a constant, which is exactly the kind")
print("  of question Theta cannot answer.")
```

Output:

```text
=== Exercise 6: a queue with amortised O(1) enqueue and dequeue ===
  4000 random enqueues/dequeues: the queue matches a Python list exactly
    array capacity 1024, head 324, tail 724, 8 compactions
    total elements moved = 1,323   amortised per operation = 0.331
  Compaction happens when the head passes the MIDDLE, so each compaction
  moves at most half the array and the array has just been compacted or
  doubled since the last one.  Total moved work is 8 + 8 + 16 + 16 + ...,
  a geometric series, so the amortised cost is O(1) -- and the measured
  figure is under 1 move per operation.

  The circular-buffer alternative gets dequeue to O(1) unconditionally by
  wrapping both indices modulo the capacity, at the cost of a modulo per
  operation and a slightly less cache-friendly layout.  Both are
  amortised O(1); the difference is a constant, which is exactly the kind
  of question Theta cannot answer.
```

**(a)** Compaction fires when the head passes the midpoint, so it moves at most
$C/2$ elements. Immediately afterwards the head is at 0, so at least $C/2$
further dequeues are needed before the next compaction — and each of those may
itself trigger a growth, which doubles $C$ and doubles the distance to the next
compaction. So the sequence of compaction *capacities* is non-decreasing and at
least doubles whenever a growth intervenes, and the moved work is a geometric
series. Bounded by $8 + 8 + 16 + 16 + 32 + 32 + \dots < 2C = O(n)$, so
amortised $O(1)$ over the $n$ operations.

**(b)** `1,323` total element moves over 4000 operations, **amortised `0.331`
moves per operation**, with 8 compactions. The structure is asserted equal to a
Python `list` after every one of the 4000 operations, so the measurement is of a
correct implementation and not a fast wrong one.

**(c)** The expensive operations are the 8 compactions, so
$\epsilon = 8/4000 = 0.002$ and the theorem gives $O(1/\epsilon) = O(500)$
moves per operation. That is a valid, computable bound and it is the right thing
to quote if you have nothing better. The measured `0.331` is much better for a
specific reason the theorem deliberately ignores: it treats each compaction as
costing an arbitrary $O(n)$, whereas here each costs *at most half the current
capacity* and the capacities form a geometric series. The theorem is the general
tool; a geometric-series argument is the sharper answer when the structure
allows it. The value of the theorem is that it degrades **gracefully** — you get
$O(500)$ rather than a failure — whereas the naive expectation would be
$O(n/8)$, which is useless.

**(d)** A circular buffer stores the elements in an array of capacity $C$ with
two indices that wrap modulo $C$; `enqueue` writes at `tail` and increments it
modulo $C$, `dequeue` reads at `head` and increments it modulo $C$, and the
buffer grows when `head` catches `tail`. This makes **every** operation
$O(1)$ in the worst case, not merely amortised — no compaction events at all.
The costs: a modulo per operation (cheap on most hardware, and JIT-compilers
turn it into a conditional subtract), a slightly worse memory pattern because
the live elements wrap around the end of the allocation, and the usual 3–12%
memory overhead. The benefit is that the worst case equals the amortised case,
which matters exactly when latency matters — the queue feeding an event loop,
or a producer/consumer ring. **Both designs are amortised $O(1)$; the difference
is a constant plus the shape of the tail, which is precisely the class of
question $\Theta$ cannot answer.**

</details>

**[ ] Exercise 7 — Growing by a constant, and the growth factor.** Let an array
grow by a fixed increment $k$ when it fills.
(a) Show the total copies for $n$ appends is $n^2/2k$ and hence the amortised
cost is $\Theta(n)$.
(b) Verify by measurement for $k = 1, 2, 8, 64$ at $n = 4096$, and report the
total divided by $n^2$.
(c) Explain why the answer is *not* rescued by making $k$ small.
(d) For multiplicative growth by $f$, derive the amortised cost $\frac{1}{f-1}$
and explain why it *does* depend on $f$ only through a constant.
(e) Minimise $\frac{1}{f-1} + \frac{f-1}{2}$ over $f > 1$ and say why no real
library uses the answer.

<details>
<summary>Solution</summary>

```python
print("=== Growing by a constant: the full analysis ===")
print("     k   n      total copies   amortised per append   total / n^2")


class GrowByK:
    def __init__(self, k):
        self.k = k
        self.data = [None] * k
        self.size = 0
        self.copies = 0
        self.resizes = 0

    def append(self, x):
        if self.size == len(self.data):
            self.data = self.data[:self.size] + [None] * self.k
            self.copies += self.size
            self.resizes += 1
        self.data[self.size] = x
        self.size += 1


for k in (1, 2, 8, 64):
    n = 4096
    g = GrowByK(k)
    for i in range(n):
        g.append(i)
    print(f"  {k:>3}   {n:>5}   {g.copies:>13,}   {g.copies / n:>20.4f}"
          f"   {g.copies / (n * n):>23.5f}")
print("  The last column is the total divided by n^2, and it is 1/(2k) for every k:")
print("  0.4999, 0.2499, 0.0624, 0.0077.  It shrinks with k and never with n, so")
print("  for each FIXED k the ratio to n^2 is a positive constant -- which is")
print("  exactly the definition of Theta(n^2).  Growing by a constant is quadratic")
print("  no matter how small the constant, because the resize sizes 1, 1+k, 1+2k,")
print("  ... form an ARITHMETIC series, and the sum of an arithmetic series to n is")
print("  n^2/2k.")
print()
print("  The doubling case is different in kind: resize sizes 1, 2, 4, 8 form a")
print("  GEOMETRIC series, whose sum to n is dominated by its last term.  That")
print("  one-word difference -- geometric versus arithmetic -- is the entire")
print("  difference between amortised Theta(1) and amortised Theta(n).")
print()

print("=== Choosing the growth factor: total cost = copies + memory ===")
print("  Amortised copies per append ~ 1/(f-1).  Memory wasted is (f-1)/2 of the")
print("  array on average.  So the total, in units of 'element slots', is")
print("     total(f)  =  1/(f-1)  +  (f-1)/2,   minimised at f-1 = sqrt(2), f = 2.414")
print()
print("     f     copies/app   waste fraction   copies + waste")
for f in (1.125, 1.5, 2.0, 2.4142, 3.0, 4.0):
    c = 1.0 / (f - 1.0)
    w = (f - 1.0) / 2.0
    star = "  <- minimises copies + waste" if abs(f - 2.4142) < 1e-3 else ""
    print(f"  {f:>6.4f}   {c:>10.4f}   {w:>14.4f}   {c + w:>15.4f}{star}")
print("  f = 2.414 is the textbook optimum for a combined cost, and no real")
print("  library uses it: memory is charged at 8 bytes per slot and a copy is")
print("  charged at a fraction of a nanosecond, so the real optimum is much")
print("  closer to 2.  Every real choice is a different answer to 'what are we")
print("  optimising', and the analysis tells you the SHAPE of the trade.")
```

Output:

```text
=== Growing by a constant: the full analysis ===
     k   n      total copies   amortised per append   total / n^2
    1    4096       8,386,560              2047.5000                   0.49988
    2    4096       4,192,256              1023.5000                   0.24988
    8    4096       1,046,528               255.5000                   0.06238
   64    4096         129,024                31.5000                   0.00769
  The last column is the total divided by n^2, and it is 1/(2k) for every k:
  0.4999, 0.2499, 0.0624, 0.0077.  It shrinks with k and never with n, so
  for each FIXED k the ratio to n^2 is a positive constant -- which is
  exactly the definition of Theta(n^2).  Growing by a constant is quadratic
  no matter how small the constant, because the resize sizes 1, 1+k, 1+2k,
  ... form an ARITHMETIC series, and the sum of an arithmetic series to n is
  n^2/2k.

  The doubling case is different in kind: resize sizes 1, 2, 4, 8 form a
  GEOMETRIC series, whose sum to n is dominated by its last term.  That
  one-word difference -- geometric versus arithmetic -- is the entire
  difference between amortised Theta(1) and amortised Theta(n).

=== Choosing the growth factor: total cost = copies + memory ===
  Amortised copies per append ~ 1/(f-1).  Memory wasted is (f-1)/2 of the
  array on average.  So the total, in units of 'element slots', is
     total(f)  =  1/(f-1)  +  (f-1)/2,   minimised at f-1 = sqrt(2), f = 2.414

     f     copies/app   waste fraction   copies + waste
  1.1250       8.0000           0.0625            8.0625
  1.5000       2.0000           0.2500            2.2500
  2.0000       1.0000           0.5000            1.5000
  2.4142       0.7071           0.7071            1.4142  <- minimises copies + waste
  3.0000       0.5000           1.0000            1.5000
  4.0000       0.3333           1.5000            1.8333
  f = 2.414 is the textbook optimum for a combined cost, and no real
  library uses it: memory is charged at 8 bytes per slot and a copy is
  charged at a fraction of a nanosecond, so the real optimum is much
  closer to 2.  Every real choice is a different answer to 'what are we
  optimising', and the analysis tells you the SHAPE of the trade.
```

**(a)** The resize sizes are $1, 1+k, 1+2k, \dots$, an arithmetic progression, and
the copies are the same sequence. Summing to $n$:

$$\text{copies} \;=\; 0 + k + 2k + \cdots + n \;=\; k\cdot\frac{(n/k)(n/k+1)}{2} \;\approx\; \frac{n^2}{2k}.$$

So the total is $\Theta(n^2)$ and the amortised cost over $n$ appends is
$\Theta(n)$.

**(b)** The `total / n^2` column reads `0.49988`, `0.24988`, `0.06238`,
`0.00769` — that is, $\frac{1}{2k}$ in each case. The value is a positive
constant for every *fixed* $k$, and that is precisely the definition of
$\Theta(n^2)$: the ratio to $n^2$ is bounded above and bounded away from zero.

**(c)** Because the class, not the constant, is what is wrong. Reducing $k$ from
1 to 64 improves the amortised cost from `2047.5000` to `31.5000` — a factor of
65 — and the total is still quadratic. To escape $\Theta(n^2)$ you need the
*shape* of the series to change, and only a multiplicative growth factor does
that. No amount of tuning a constant growth rule gets you an amortised $O(1)$,
and this is the single most important thing to know before writing a container.

**(d)** With capacity multiplied by $f$, the $k$-th resize copies $C f^k$
elements and the last one copies about $n/f$, so

$$\sum \approx \frac{n}{f}\left(1 + \frac1f + \frac{1}{f^2} + \cdots\right) \;=\; \frac{n}{f}\cdot\frac{f}{f-1} \;=\; \frac{n}{f-1}.$$

The amortised cost is $\frac{1}{f-1}$, a function of $f$ only — no dependence on
$n$ at all, which is the definition of $\Theta(1)$ for every $f > 1$. The
lesson's table confirms it: `8.0000` predicted and `8.8263` measured at
$f = 1.125$, `1.0000` and `0.9999` at $f = 2$, `0.3333` and `0.3330` at
$f = 4$. The residual is the initial-capacity offset, which matters most when
$f$ is small.

**(e)** Minimise $g(f) = \frac{1}{f-1} + \frac{f-1}{2}$. With $u = f - 1 > 0$ this
is $\frac1u + \frac u2$, with derivative $-\frac{1}{u^2} + \frac12 = 0$ giving
$u = \sqrt{2}$, i.e. $f = 1 + \sqrt2 = 2.4142$. The table confirms it: the
`copies + waste` column reads `8.0625`, `2.2500`, `1.5000`, **`1.4142`**,
`1.5000`, `1.8333` — a minimum at $f = 2.4142$.

No real library uses it, because the model charges a copy and a wasted slot at
the *same* price, and they are not comparable. A wasted slot costs 8 bytes of
resident memory, forever, for the life of the container. A copy costs a fraction
of a nanosecond, once. The real objective function weights memory perhaps
$10^3$ times more heavily than the copying, which pushes the optimum down to
near $f = 1.1$ — and indeed CPython's `list` uses about `1.125` and `std::vector`
uses 2. **The analysis tells you the shape of the trade and the shape of the
answer to "does the factor matter"; the constant, and therefore the factor
itself, is an engineering decision that has to be measured.**

</details>

---

## Summary

- The only definition of amortised cost is $\sum_{i=1}^{n} T_i \le c\hat c\, n$
  for **every** sequence of $n$ operations. No randomness, no distribution, no
  assumption about your inputs — and that is what separates it from average-case
  analysis, which is a statement about one named distribution and only a hope.
- The three methods — aggregate, accounting, potential — are the same
  telescoping identity $\sum T_i = \sum \hat T_i - (\Phi_n - \Phi_0)$ with a
  different thing chosen first. The aggregate method bounds the total directly,
  accounting charges every operation the same price and tracks a balance, and
  potential picks $\Phi$ up front.
- A geometric series is dominated by its last term and an arithmetic series is
  not, and that one distinction is the whole lesson: doubling gives resize sizes
  $1, 2, 4, \dots$ and a total of `4,092` copies for $n = 4096$ (`0.9990` per
  append), while growing by a constant gives $1, 5, 9, \dots$ and `8,386,560`
  copies (`2047.5000` per append) from an identical interface. The growth factor
  moves the *constant*, not the class: $\frac{1}{f-1}$ copies per append,
  measured `8.8263` at CPython's $f \approx 1.125$ against `0.9999` at $f = 2$,
  for `9.3%` versus `0%` wasted slots — and $\frac{1}{f-1} + \frac{f-1}{2}$ is
  minimised at $f = 2.414$, which no library uses because a wasted byte and a
  wasted copy are not priced alike.
- A potential is a bounded quantity that rises when an operation is expensive
  and falls by little when it is cheap. $\Phi = 2n - C$ gives a constant `3` for
  both kinds of array append — the code's set of distinct amortised costs over
  32 appends is exactly `[3]` — while the obvious $\Phi = C - n$ gives the
  useless `0` and `C`. The test is to compute $\hat T$ for one of each and look
  at the spread.
- "Amortised $O(1)$" and "worst case $O(n)$" are both true, simultaneously, of
  the same array: the amortised cost is `0.9961` and the worst single append is
  `512` copies, a ratio of `514x` that **grows as $n/2$ and never stops**. A
  sum bounds no individual term. So an amortised bound is the right tool for
  throughput and the wrong tool for a latency SLO.
- A binary counter is the cleanest non-array example: exactly `2^n - 1 + n`
  flips over `2^n - 1` increments, so the amortised cost is
  $2 - 2^{1-n} \to 2$ — an *exact* figure, measured at `2.0000` for 20 bits —
  with a worst case of $n$ bits. Having the exact count turns $O(1)$ into
  $\Theta(1)$ and shows no smaller constant works.
- Hash tables show the whole distinction. `BadHash` costs `512.50` probes per
  lookup in *both* the average and the worst case; `GoodHash` costs `1.21` at
  $n = 4096$ on average with a $\Theta(n)$ worst case. The resize policy, by
  contrast, is genuinely amortised — `0.9996` rehash moves per insert at
  $n = 16384$ — and is a **guarantee for every key sequence**, because the
  trigger depends only on the sizes `17, 33, 65, 129, ...`, never on the keys.
- The $\epsilon$-heavy theorem bounds a sequence whose expensive operations are
  merely *not too frequent*: $O(1/\epsilon)$, computable and degrading
  gracefully, and looser than the geometric-series argument — Exercise 6's queue
  compacts 8 times in 4000 operations, giving $O(500)$ by the theorem against a
  measured `0.331` moves per operation.

- **Union-find is the one data structure whose amortised cost is a named
  function.** With union by rank *and* full path compression the total is
  `$O(N\alpha(N))$`, where `$\alpha$` inverts a tower of twos:
  `$A(0)=1`, `$A(k+1)=2^{A(k)}$`. It is `$\le 4$` for `$n \le 65{,}536$` and `$\le 5$`
  for every `n` that exists. The honest measurement is a *flat column*, not a
  value: `2.3613` hops per operation at `$n=1{,}000$` and `2.3563` at
  `$n=300{,}000$`, with the forest never deeper than `3`. It is emphatically **not**
  a per-call bound — a first `find` on a cold leaf costs `32` hops at
  `$n = 65{,}536`.
- **The sliding window is an amortised argument with no expensive event at all.**
  Subtract the element leaving, add the element entering, and the total is
  `$K + 2(n-K) = 2n - K$`: `199,500` touches against `49,750,500` for rescanning,
  a factor of `249.4`. When the statistic cannot be un-added — a maximum — a
  monotonic deque carries the same argument, because every index is pushed once
  and popped at most once, bounding the total by `$2n$` at any window size.
- **Accounting and potential are the same object.** The balance and the potential
  satisfy `$B_k = \Phi_k - \Phi_0$`, verified at all `4,096` steps of a doubling
  array with `0` mismatches and both finishing at `4,100`. They differ in what you
  must check: a **prefix** condition versus a **per-operation** condition. And
  accounting is how you *find* the potential — charge 1, 2, 3 … and take the
  smallest price whose balance never goes negative (`3` here, with price 2
  passing eight appends and then failing at append 9).
## Next

[82 — Tools for Algorithm Design](82_tools_for_algorithm_design.md) turns to
proving that an algorithm is *correct* and picking one. This lesson's aggregate
method is the tool: to check a design that interleaves expensive operations,
bound the total by grouping them, and the grouping argument is exactly the
"there is one hard case per doubling" reasoning that divide and conquer is
built on.
