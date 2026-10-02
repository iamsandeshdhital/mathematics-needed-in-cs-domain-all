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

---

## Formula Sheet

`$T_i$` is the actual cost of operation `$i$`, `$\hat T_i$` its amortised cost,
`$\Phi$` the potential, `$C$` the capacity of a dynamic array, `$n$` its size
(also used for the number of operations where no array is involved), `$f > 1$` the
growth factor, `$k` the constant growth increment, and `$c$` the constant in the
aggregate bound. `$\epsilon$` is the heavy-operation fraction.

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
| hash table expected | `$O(1)$ | one probe, on average | **needs** a random seed and a well-behaved key distribution; measured `1.22`–`1.33` probes |
| hash table amortised insert | rehash total `$\approx 2n$`, so `$\approx 2$ per insert | the resize is a geometric series | `0.9996` at $n = 16384$, a **guarantee** independent of the hash |
| amortised fraction | `$T_i / (C/n)$ | how many times average cost this operation cost | finds the operations to protect; $\epsilon$-heavy sets give $O(1/\epsilon)$ |
| $\epsilon$-heavy theorem | rare-but-expensive $\Rightarrow$ amortised `$O(1/\epsilon)$` | the expensive ones need not be rare *in time* | queue compaction: 8 of 4000, measured `0.331` moves per operation |
| peak vs amortised | amortised $\hat c$ and worst case $w(n)$ hold **simultaneously** | the average says nothing about the maximum | why amortised bounds are the right tool for throughput and the wrong one for latency |
| shrink thrash | alternating append/pop, halving at half full | resizes on *every* operation | still $\Theta(1)$ — but the constant is `511.98` copies per operation instead of `1` |

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
print("  GoodHash/n sits between 1.22 and 1.33: about 1.25 probes per lookup, the")
print("  signature of a chain of length 1.25 in a half-full table.")
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
  GoodHash/n sits between 1.22 and 1.33: about 1.25 probes per lookup, the
  signature of a chain of length 1.25 in a half-full table.

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

---

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
half-full table measures `1.24`. The gap between a guarantee and a hope is
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
measures `1.24` probes per lookup in a half-full table — an average that an
adversary destroys.

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
(c) Prove it by the potential method, with $\Phi$ = the number of 0 bits, and
state the constant.
(d) Find the worst-case single increment and explain why it does not contradict
(a).
(e) Explain in one paragraph why `i += 1` is nevertheless treated as $O(1)$.

<details>
<summary>Solution</summary>

**(a)** Over $2^n - 1$ increments the counter visits $1, 2, \dots, 2^n - 1$. Bit
$i$ (counting from 0) is 1 exactly when the value is odd enough, and it is
flipped once every $2^{i+1}$ increments, so exactly
$\frac{2^n - 1}{2^{i+1}}$ times. Summing over $i$ and adding the $n$ bits that
get created from nothing:

$$\text{total} \;=\; \sum_{i=0}^{n-1}\frac{2^n-1}{2^{i+1}} \;+\; n \;=\; (2^n - 1)\left(1 - 2^{-n}\right) + n \;=\; 2^n - 1 + n.$$

So the amortised cost is exactly
$\frac{2^n - 1 + n}{2^n - 1} = 2 - 2^{1-n}$. The code measures `502` flips over
`255` increments (`1.9686`) at $n = 8$, `131,054` over `65,535` (`1.9998`) at
$n = 16$, and `2,097,130` over `1,048,575` (`2.0000`) at $n = 20$.

**(b) Aggregate.** Group the increments by how many trailing 1s they clear:
$2^{n-1}$ increments clear 0 bits, $2^{n-2}$ clear 1, and so on. The total is
$\sum_{t=0}^{n-1} 2^{n-1-t}(t+1) = 2^n - 1 + n$, i.e. a geometric sum evaluated
in closed form, giving $O(m)$ total over $m = 2^n - 1$ increments, hence
amortised $O(1)$. The grouping is what makes it an aggregate argument: it does
not look at any individual increment, only at how many there are of each kind.

**(c) Potential.** Let $\Phi$ = the number of 0 bits, so $0 \le \Phi \le n$ (or
$\le 2n$ allowing a fresh bit). An increment clears $t$ ones and sets one zero,
so $\Delta\Phi = +t - 1$ and $\hat T = (t+1) + (t-1) = 2t$. Now $t$ can be at
most $n-1$, and $t = n$ only when every bit was 1 — at which point a new bit is
created and $n$ increases. So $\hat T \le 2$ for every increment, and
$\sum T_i \le 2m + \Phi_{\max} = O(m)$. The constant is **2**, matching the exact
answer from (a) to the limit.

**(d)** The worst single increment flips $n$ bits: incrementing from $2^n - 1$
(all ones) to $2^n$ clears every bit. The code measures a worst increment of `8`,
`16` and `20` at 8, 16 and 20 bits. This does not contradict (a) because (a) is
about the total over $2^n - 1$ increments and (d) is about one of them; the
worst increment is `2.0 / 1.9998` times the amortised cost, a bounded factor —
which is *not* true of the dynamic array, where the factor is $n/2$. The
counter is the friendlier example precisely because its peak is a constant
multiple of its mean.

**(e)** Three reasons, in increasing order of rigour. First, the hardware does
it: adding 1 to a machine integer modifies the low bits and *propagates the
carry* in hardware, in one cycle for the whole word. The $n$ "flips" are $n/64$
word-level operations, and a 64-bit word is a constant, so the machine-level
cost is $O(1)$ with a small constant. Second, the sequence of *consecutive*
increments is what makes the tail cheap: an expensive increment is always
followed by many cheap ones, which is exactly the amortised statement. Third,
and this is the honest caveat, the model matters: if you count **bit**
operations, `i += 1` on a Python integer is $\Theta(\log n)$ per increment —
and even that is the amortised figure, with a worst case of $O(\log n)$. The
lesson's [Lesson 80](80_big_o_and_complexity.md) measures the growth: `1 + 2 +
4 + 8 + ... ` in the bit model. So "increment is $O(1)$" is true of machine
words, amortised, and "increment is $O(\log n)$" is true of bignums, also
amortised. **The cost model decides, as always.**

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

**(c)** The trick is to use the free slots *anywhere*, not just at the end. With
$n$ elements in a capacity-$C$ array there are $C - n$ free slots distributed in
$n+1$ gaps. To insert at position $p$: if there is a free slot at or to the left
of $p$, shift only the segment between them (cost = the distance, at most $p$);
otherwise shift everything from $p$ to the end (cost $n - p$), which requires a
free slot after the last element.

The potential that pays for it counts each free slot by **how useful it is**:
$\Phi = \sum$ over free slots $f$ of (number of elements to the left of $f$) +
(free slots after the last element). Shifting the segment after an insertion at
$p$ consumes, for each free slot to the right of $p$, one unit of the "elements
to its left" count — so $\Delta\Phi = -(n - p)$ on that path, and
$\hat T = (n - p) - (n - p) = 0$. When every gap is empty, $\Phi = 0$, and the
array grows, restoring all the slack at a cost of $n$; the growth sizes are
geometric, so the total growth cost is $O(n)$ and $\hat T = O(1)$ amortised.
When every gap is empty, $C = n$, so doubling gives $C = 2n$ and $\Phi$ jumps to
$n = \Theta(n)$, which is exactly the $O(n)$ that pays for the $n$ copies.

**(d)** The verification is Exercise 6's queue: 4000 random operations, 8
compactions, `1,323` total element moves, **amortised `0.331` per operation**,
with the structure asserted equal to a Python `list` at every one of the 4000
steps. Compare with (a): `0.9990` copies per append for a pure-`push_back`
workload. The queue is *cheaper* per operation despite doing strictly more work
per operation, because its expensive events are 8-in-4000 rather than
1-in-1000 — and the amortised bound is a statement about the total, so a rarer
expensive event wins.

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
  not. That one distinction is the whole lesson: doubling gives resize sizes
  $1, 2, 4, \dots$ and a total of `4,092` copies for $n = 4096$ (`0.9990` per
  append), while growing by a constant gives $1, 5, 9, \dots$ and `8,386,560`
  copies (`2047.5000` per append) from an identical interface.
- The growth factor is the only free parameter, and it moves the *constant*:
  the amortised cost is $\frac{1}{f-1}$ copies per append, measured at
  `8.8263` for CPython's $f \approx 1.125$ and `0.9999` for $f = 2$, in exchange
  for `9.3%` and `0%` wasted slots. $\frac{1}{f-1} + \frac{f-1}{2}$ is minimised
  at $f = 2.414$, and no library uses it because a wasted byte and a wasted copy
  are not priced alike.
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
  lookup in *both* the average and the worst case; `GoodHash` costs `1.24` on
  average with a $\Theta(n)$ worst case. The resize policy, by contrast, is
  genuinely amortised — `0.9996` rehash moves per insert at $n = 16384$ — and is
  a **guarantee for every key sequence**, because the trigger depends only on
  the sizes `17, 33, 65, 129, ...`, never on the keys.
- The $\epsilon$-heavy theorem bounds a sequence whose expensive operations are
  merely *not too frequent*: $O(1/\epsilon)$, computable and degrading
  gracefully. Exercise 6's queue compacts 8 times in 4000 operations, giving
  $O(500)$ by the theorem against a measured `0.331` moves per operation — the
  gap is the geometric series the theorem deliberately ignores.

## Next

[82 — Tools for Algorithm Design](82_tools_for_algorithm_design.md) turns to
proving that an algorithm is *correct* and picking one. This lesson's aggregate
method is the tool: to check a design that interleaves expensive operations,
bound the total by grouping them, and the grouping argument is exactly the
"there is one hard case per doubling" reasoning that divide and conquer is
built on.
