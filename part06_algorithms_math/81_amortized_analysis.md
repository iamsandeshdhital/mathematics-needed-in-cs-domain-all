# 81 — Amortised Analysis

**Part**: part06_algorithms_math · **Prerequisites**: 24, 80 · **Time**: 30 min

---

## In Plain Words

Adding one item to the end of a list is sometimes slow — occasionally the
whole list has to be copied to a bigger block of memory — but those slow
moments happen so rarely that the *average* cost of adding an item stays
small, no matter how many items you add and no matter what order you add
them in. Amortised analysis is the discipline of proving that claim
rigorously: instead of asking how expensive one operation might be, you
add up the cost of every operation you actually performed and divide by
how many there were. The word "amortised" means spread out, like paying a
car loan down over years. It is not the same as saying something is "fast
on average": an amortised guarantee is a promise about the total that
holds even against an adversary who deliberately chooses the worst
possible sequence of operations, while an average-case statement is a
promise about one operation averaged over a distribution of inputs.

---

## Why Computer Science Cares

- **`list.append` in Python, `push_back` in `std::vector`, `push` in Rust's
  `Vec`.** Every one of these grows its buffer when it fills up. If they
  did not amortise, appending would be quadratic and nothing built on top
  of them would work. The block in Runnable Code measures what CPython
  actually does: it grows the buffer by about one eighth, not by a factor
  of two, which is a deliberate memory-for-constant trade.
- **Hash tables.** Every real implementation rehashes the whole table when
  the load factor crosses a threshold. Rehash $n$ elements on $n$ inserts
  would be quadratic; because the table doubles each time, each element is
  rehashed only $O(\log n)$ times over the entire life of the table, so the
  total rehash work is linear. This is the calculation
  [Lesson 112](../part09_number_theory_crypto/112_hashing.md) refers to.
- **Union-find (disjoint set union).** Path compression and union by rank
  are both amortised arguments. Without them a `find` can take a linear
  number of parent-pointer steps; with them the amortised cost per operation
  is the inverse Ackermann function, which is a small constant for any
  input that fits in memory. Kruskal's and Borůvka's minimum spanning tree
  algorithms, connected components, and image segmentation all rest on it.
- **Java's `StringBuilder`, network send buffers, log ring buffers, editors
  with undo stacks.** Each of them occasionally flushes or compacts, paying
  $O(n)$ to avoid paying $O(n)$ on every single write.
- **It is a contract.** The documentation of an amortised method says what
  the *total* will be. That is the only kind of guarantee a long-running
  process can actually use: a latency budget of one millisecond per
  operation is not something a service can promise when one operation in a
  million costs a second.

---

## The Formal Version

**Definition.** A *sequence of operations* on a data structure $D$ is an
ordered list $o_1, o_2, \dots, o_n$ of legal operations. Let $c_i$ be the
true cost of $o_i$, counted in elementary steps — element moves, key
comparisons, whatever unit the structure makes you pay in. The *aggregate
cost* of the sequence is

$$\sum_{i=1}^{n} c_i .$$

**Definition.** The *amortised cost* of the sequence is
$\hat{c}(n) = \frac{1}{n}\sum_{i=1}^{n} c_i$. An operation is
**$O(1)$ amortised** if there are constants $c > 0$ and $n_0$ such that
$\sum_{i=1}^{n} c_i \le c\,n$ for **every** sequence of $n \ge n_0$
operations.

The italicised word is the entire definition. The inequality quantifies over
all sequences, so it is a statement about the worst possible caller, not
about a typical one.

*Explanation.* Amortised analysis is the inverse of what
[Lesson 80](80_big_o_and_complexity.md) does when it analyses a loop. There
you sum $c_i$ to get $T(n)$; here you are handed the sequence, sum it, and
divide. It is also the inverse of the sum rule from
[Lesson 24](24_recurrence_relations.md): a loop whose body costs $\Theta(1)$
has $T(n) = T(n-1) + \Theta(1) = \Theta(n)$, hence amortised cost
$\Theta(1)$.

**Theorem (aggregate implies amortised).** If every sequence of $n$
operations satisfies $\sum_{i=1}^{n} c_i \le c\,n$, then every operation is
$O(1)$ amortised with constant $c$, and no caller can do worse.

**Definition.** A *potential function* is a map $\Phi$ from the states of
$D$ to non-negative reals. Let $D_i$ be the state after $o_i$. The
*amortised cost of a single operation* is

$$\hat{c}_i = c_i + \Phi(D_i) - \Phi(D_{i-1}),$$

and the *potential credit* of the operation is $\Delta\Phi = \Phi(D_i) -
\Phi(D_{i-1})$.

**Theorem (potential method).** Suppose $\Phi(D_0) = 0$, $\Phi \ge 0$ on every
state, and $\hat{c}_i \le c$ for every operation $i$ on every state. Then
for every sequence of $n$ operations,

$$\sum_{i=1}^{n} c_i = \sum_{i=1}^{n}\hat{c}_i - \Phi(D_n) + \Phi(D_0)
= \sum_{i=1}^{n}\hat{c}_i - \Phi(D_n) \le \sum_{i=1}^{n}\hat{c}_i \le c\,n .$$

*Proof.* Sum $\hat c_i = c_i + \Phi(D_i) - \Phi(D_{i-1})$ over $i = 1..n$.
The potential terms telescope: $\Phi(D_1) - \Phi(D_0) + \Phi(D_2) -
\Phi(D_1) + \dots + \Phi(D_n) - \Phi(D_{n-1}) = \Phi(D_n) - \Phi(D_0)$.
With $\Phi(D_0) = 0$ and $\Phi(D_n) \ge 0$ the conclusion follows. ∎

*Explanation.* The proof is three lines and there are no hidden ideas in it.
The potential is a bank balance. A cheap operation that leaves the
structure holding unused capacity (an append into slack space) is charged
less than it costs and stores the difference; an expensive operation (a
resize) spends that stored credit. The only requirement is that the bank
never starts in debt and never gives credit for more work than it can pay
for.

**Definition.** The *accounting method* (also called the *banker's method*)
is the same argument in coins. Charge each operation $\hat c_i \ge c_i$ and
the unused charge $c_i$ is stored inside the structure. The stored total is
exactly the potential: $B_i = \Phi(D_i) - \Phi(D_0) = \Phi(D_i)$.

**Theorem (dynamic array, doubling).** Let an array start with capacity $1$
and, whenever it is full, be replaced by a copy of twice the capacity. Then
for $n$ appends:

- the number of copies is $1 + 2 + 4 + \dots + 2^{k} = 2^{k+1} - 1$ where
  $2^{k} < n \le 2^{k+1}$, so copies $< 2n$;
- each of the $n$ appends writes one element, so the total is
  $< 3n$ and the amortised cost is $< 3$;
- with the potential $\Phi = 2|D| - |S|$ (twice the number of stored elements
  minus the capacity) the amortised cost of **every** append is exactly $3$;
- one single append costs $\Theta(n)$, which is not a contradiction — see
  the worked example.

**Theorem (growth factor).** If the capacity is multiplied by $r \ge 2$ at
each resize instead, the capacity $S$ at the end satisfies $n \le S < rn$ and
the total number of copies lies between $\frac{n}{r-1}$ and
$\frac{r\,n}{r-1}$. The memory overhead is at most a factor $r$.

*Explanation.* Doubling makes $1/(r-1) = 1$ and wastes at most half the
capacity. A smaller $r$ wastes less memory and copies more; a larger $r$
copies less and wastes more. The measured table in Runnable Code shows
exactly this, at $n = 1000$: $r = 1.125$ needs `8466` copies,
$r = 1.5$ needs `2137`, and $r = 2$ needs `1023`.

**Theorem (hash table, resize work).** If a table doubles when its load
factor would exceed $\alpha < 1$, then over $n$ insertions the number of
element *moves* caused by resizing is a geometric series and is $O(n)$.
Consequently insertion costs $O(1)$ amortised, **independently of the hash
function**.

**Theorem (hash table, probe work).** For the same table, the number of
*probes* per insertion is $\Theta(1)$ only in expectation over the random
choice of keys or the seed. An adversary who knows the hash can force every
key into one bucket, making the total $\Theta(n^2)$.

*Explanation.* These two theorems are the reason the phrase "amortised
$O(1)$" is used for `dict` insertion and "expected $O(1)$" for the lookup.
Half the cost is a guarantee and half is an average.

**Theorem (union-find).** On $n$ elements with $m$ operations, union-find
with path compression alone, or with union by rank alone, takes
$O((m+n)\log n)$ total time. With both together it takes $O((m+n)\alpha(n))$,
where $\alpha$ is the inverse Ackermann function.

**Definition.** The *inverse Ackermann function* is
$\alpha(n) = \min\{k \ge 1 : A(k,0) \ge n\}$ where
$A(0,j) = j+1$, $A(m,0) = A(m-1,1)$, $A(m,j) = A(m-1, A(m,j-1))$.

*Explanation.* The ladder $A(1,0) = 2$, $A(2,0) = 3$, $A(3,0) = 5$,
$A(4,0) = 13$, $A(5,0) = 2^{16}-3 = 65533$, $A(6,0) = 2^{65536}-3$ grows so
fast that $\alpha(n) \le 6$ for every $n$ that fits in memory. Textbooks that
start the ladder one rung lower quote `4`; the content is the same.

**Definition.** *Amortised* is not *average case*. An **average-case**
(or expected) bound is a statement about $\mathbb{E}[c_i]$ for a single
operation, averaged over a distribution on inputs. An **amortised** bound is
a deterministic statement about $\sum_i c_i$ for every sequence.

**Theorem (aggregate counting).** If an algorithm processes each of the $n$
input elements at most $c$ times in total — no matter how many times the
element appears in overlapping computations — then it runs in $O(c\,n)$,
independent of any window width, subproblem size, or other second parameter.

*Explanation.* This is the sliding-window technique and the "count the total,
not the parts" principle. It is the same arithmetic as the geometric series:
each element enters once and leaves once, so the total is $2n$ additions
however wide the window is.

---

## Worked Example

### Seventeen appends into a doubling array, counted one at a time

This is the whole lesson in one table. Start with an empty array of capacity
`1` and append the integers `0` to `16`. An append that finds room costs `1`
(the write). An append that finds the buffer full costs `1 + (capacity)`
(the write plus a copy of every stored element into a buffer of twice the
size).

| append | size before | capacity before | capacity after | actual cost | cumulative |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 2 | 2 | 3 |
| 3 | 2 | 2 | 4 | 3 | 6 |
| 4 | 3 | 4 | 4 | 1 | 7 |
| 5 | 4 | 4 | 8 | 5 | 12 |
| 6 | 5 | 8 | 8 | 1 | 13 |
| 7 | 6 | 8 | 8 | 1 | 14 |
| 8 | 7 | 8 | 8 | 1 | 15 |
| 9 | 8 | 8 | 16 | 9 | 24 |
| 10 | 9 | 16 | 16 | 1 | 25 |
| 11 | 10 | 16 | 16 | 1 | 26 |
| 12 | 11 | 16 | 16 | 1 | 27 |
| 13 | 12 | 16 | 16 | 1 | 28 |
| 14 | 13 | 16 | 16 | 1 | 29 |
| 15 | 14 | 16 | 16 | 1 | 30 |
| 16 | 15 | 16 | 16 | 1 | 31 |
| 17 | 16 | 16 | 32 | 17 | 48 |

**Step 1 — count the copies.** They happen at appends `2, 3, 5, 9, 17` and
cost `1, 2, 4, 8, 16`. That is the geometric series

$$1 + 2 + 4 + 8 + 16 = \frac{2^{5} - 1}{2 - 1} = 2^{5} - 1 = 31 .$$

**Step 2 — count the writes.** Seventeen appends write seventeen elements.
So the total is $31 + 17 = 48$ units of work for 17 appends.

**Step 3 — divide.** $48 / 17 = 2.8235$ units per append. The bound says
$< 3$, and $2.8235 < 3$. ✓

**Step 4 — check the worst case.** The table above is not the worst $n$. The
worst is always just past a power of two, because that is where the last
resize lands:

| $n$ | total | total / $n$ |
| --- | --- | --- |
| 3 | 6 | 2.0000 |
| 5 | 12 | 2.4000 |
| 9 | 24 | 2.6667 |
| 17 | 48 | 2.8235 |
| 33 | 96 | 2.9091 |
| 65 | 192 | 2.9538 |

The ratio increases towards `3` and never reaches it. That is the concrete
content of "the total is $< 3n$".

**Step 5 — the potential method gives the same answer with a per-operation
statement.** Take $\Phi(D) = 2|D| - |S|$. Now compute $\hat c_i = c_i +
\Phi(D_i) - \Phi(D_{i-1})$ for each row:

| append | actual $c_i$ | $\Phi$ before | $\Phi$ after | $\Delta\Phi$ | $\hat c_i$ |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | −1 | 1 | 2 | 3 |
| 2 | 2 | 1 | 2 | 1 | 3 |
| 3 | 3 | 2 | 2 | 0 | 3 |
| 4 | 1 | 2 | 4 | 2 | 3 |
| 5 | 5 | 4 | 2 | −2 | 3 |
| 9 | 9 | 8 | 2 | −6 | 3 |
| 17 | 17 | 16 | 2 | −14 | 3 |

(rows for appends 6–8, 10–16 are all $c_i = 1$, $\Delta\Phi = +2$,
$\hat c_i = 3$). So **every single append has amortised cost exactly 3**, and
the ones that do real work pay for it out of the credit the cheap ones stored.
Note how append 17 spends `14` units of stored credit; if there were no credit,
the potential method would not be a proof.

**Step 6 — close the books.** The telescoping sum is
$48 + (2) - (-1) = 51 = 3 \times 17$. The initial potential is $-1$ because a
fresh empty array has capacity `1` and no elements; that one-off costs one
extra unit over the whole sequence, which is why the bound is written
$3n + 1$ rather than $3n$. Run the code below and it prints exactly these
numbers.

### Why a single $O(n)$ operation is not a contradiction

Append `17` above cost `17` units. There is no way to make it cheaper, and
there is no way for the caller to arrange for seventeen of them. If every
append cost $\Theta(n)$ you would need $\Theta(n^2)$ total, but the copies
are `1, 2, 4, 8, 16` — a series dominated by its last term. Over 1024
appends, `1014` of them cost exactly `1`, `4` cost between `2` and `9`, and
only `6` cost `10` or more; those six account for `1014` of the `2047` total
units. The statement "append is $O(1)$ amortised" is a statement about the
column on the right, and that column is flat.

---

## Runnable Code

### Block 1: the accounting argument on a doubling array

```python
class CountingArray:
    """Append-only list with geometric growth; counts every unit of work."""

    def __init__(self):
        self.buf = [None] * 1   # capacity starts at 1
        self.size = 0
        self.copies = 0         # elements relocated by a resize
        self.writes = 0         # elements written by append itself
        self.actual = []        # real cost of each individual append

    def append(self, x):
        cost = 1                            # writing the new element
        if self.size == len(self.buf):
            # Full: relocate everything into a buffer of twice the size.
            old = len(self.buf)
            bigger = [None] * (2 * old)
            for i in range(old):
                bigger[i] = self.buf[i]
            self.copies += old
            cost += old
            self.buf = bigger
        self.buf[self.size] = x
        self.size += 1
        self.writes += 1
        self.actual.append(cost)

    @property
    def capacity(self):
        return len(self.buf)


def total_cost(n):
    """Total work -- copies plus writes -- for n appends into a fresh array."""
    a = CountingArray()
    for i in range(n):
        a.append(i)
    return a, a.copies + a.writes


print("  Cost of n appends into a doubling array.  Capacity starts at 1.")
print()
print("      n   capacity   copies   writes    total   total/n")
for n in (1, 8, 17, 100, 1000):
    a, total = total_cost(n)
    print(f"  {n:>5}   {a.capacity:>7}   {a.copies:>7}   {a.writes:>6}"
          f"   {total:>6}   {total / n:>7.4f}")

print()
print("  Each resize relocates every element stored so far, so the sizes")
print("  relocated are 1, 2, 4, 8, 16, ... : a geometric series.")
a = CountingArray()
series = []
for i in range(17):
    before = a.copies
    a.append(i)
    if a.copies > before:
        moved = a.copies - before
        series.append(moved)
        print(f"    append {i + 1:>2}: full at size {a.size - 1:>2}, copied "
              f"{moved:>2} elements into capacity {a.capacity:>2}")
print(f"    1 + 2 + 4 + 8 + 16 = {sum(series)} = 2^5 - 1 = {2 ** len(series) - 1}")
print(f"    17 appends made {a.copies} copies: copies/n = {a.copies / 17:.4f} < 2")
print(f"    total work = {a.writes} writes + {a.copies} copies = "
      f"{a.writes + a.copies} < 3 * 17 = {3 * 17}")

print()
print("  The worst n is just past a power of two, because that is where the")
print("  last resize happened:")
print("      n   total   total/n   (= (copies + writes) / n, worst case)")
for k in range(1, 7):
    n = 2 ** k + 1
    _, total = total_cost(n)
    print(f"  {n:>5}   {total:>5}   {total / n:>7.4f}")
print("  The ratio approaches 3 from below and never reaches it.")

worst = max(a.actual)
print()
print(f"  The most expensive single append of 17 cost {worst} units, at append")
print(f"  {a.actual.index(worst) + 1}.  Every earlier append cost exactly 1, and")
print("  no input sequence can make any of them cost more.")
```

### Block 2: the potential method, operation by operation

```python
class CountingArray:
    """Append-only list with geometric growth, tracked for the potential method."""

    def __init__(self):
        self.buf = [None] * 1
        self.size = 0
        self.log = []            # one row per append, for the table below

    @property
    def capacity(self):
        return len(self.buf)

    def potential(self):
        # Phi = 2 * size - capacity.  Phi is -1 for a fresh empty array of
        # capacity 1, which costs one extra unit over a whole sequence.
        return 2 * self.size - self.capacity

    def append(self, x):
        size_before, cap_before = self.size, self.capacity
        phi_before = self.potential()
        cost = 1
        if self.size == self.capacity:
            bigger = [None] * (2 * self.capacity)
            for i in range(self.capacity):
                bigger[i] = self.buf[i]
            cost += self.capacity
            self.buf = bigger
        self.buf[self.size] = x
        self.size += 1
        phi_after = self.potential()
        self.log.append((size_before, cap_before, self.capacity, cost,
                         phi_before, phi_after, phi_after - phi_before,
                         cost + phi_after - phi_before))


a = CountingArray()
for v in range(17):
    a.append(v)

print("  POTENTIAL METHOD on a doubling array.")
print("  Potential Phi = 2 * size - capacity.")
print("  Amortised cost = actual cost + Phi_after - Phi_before.")
print()
print("   op  size   cap before   cap after   actual   Phi before   Phi after"
      "   dPhi   amortised")
for i, (s, cb, ca, cost, pb, pa, dphi, am) in enumerate(a.log, 1):
    print(f"  {i:>3}  {s:>4}   {cb:>10}   {ca:>9}   {cost:>6}   {pb:>10}   "
          f"{pa:>9}   {dphi:>4}   {am:>8}")

amortised = [row[7] for row in a.log]
actual_total = sum(row[3] for row in a.log)
print()
print(f"  distinct amortised costs over 17 appends: {sorted(set(amortised))}")
print("  Every append costs exactly 3: 1 for the write, plus the potential")
print("  step of an insert, which is +2 unless a resize pays it back.")
print(f"  total actual cost    = {actual_total}")
print(f"  total amortised cost = {sum(amortised)} = 3 * 17 = {3 * 17}")
print()
print("  Telescoping -- which is the whole proof of the theorem:")
phi0, phi_n = 2 * 0 - 1, a.potential()
print(f"    sum(actual) + Phi_final - Phi_initial = {actual_total} + ({phi_n})"
      f" - ({phi0}) = {actual_total + phi_n - phi0}")
print("  So the total actual cost is the total amortised cost minus one")
print("  boundary term, and the amortised cost per op is exactly 3.")


# --- the same technique on a different structure: a binary counter -----------
class BinaryCounter:
    """A 17-bit counter; one increment flips every trailing 1-bit to 0."""

    def __init__(self):
        self.value = 0
        self.flips = []          # flips used by each increment
        self.ones = []           # 1-bits after each increment = the potential

    def increment(self):
        v, flips = self.value, 1
        while v & 1:
            v >>= 1
            flips += 1
        self.value += 1             # add one to the counter itself
        self.flips.append(flips)
        self.ones.append(bin(self.value).count("1"))


c = BinaryCounter()
for _ in range(17):
    c.increment()
amortised_c = [f + ones_after - ones_before
               for f, ones_before, ones_after in
               zip(c.flips, [0] + c.ones[:-1], c.ones)]
print()
print("  The same technique on a binary counter.  Potential = number of 1-bits,")
print("  which stores credit for the flips a future increment will need.")
print("  1-bits after each increment: " + ", ".join(map(str, c.ones)))
print(f"  flips per increment: " + ", ".join(map(str, c.flips)))
print(f"  distinct amortised costs: {sorted(set(amortised_c))} "
      f"-- exactly 2, always")
print(f"  total flips {sum(c.flips)} + (Phi_final {c.ones[-1]} - Phi_initial 0)"
      f" = {sum(c.flips) + c.ones[-1]} = 2 * 17 = {2 * 17}")
```

### Block 3: growth factors, and what an adversary can actually do

```python
class GrowArray:
    """Append-only list whose capacity is multiplied by r at each resize."""

    def __init__(self, r=2):
        self.r = r
        self.buf = [None]
        self.size = 0
        self.copies = 0
        self.costs = []            # real cost of each individual append

    def append(self, x):
        cost = 1
        if self.size == len(self.buf):
            old = len(self.buf)
            self.buf = [None] * max(int(old * self.r), old + 1)
            self.copies += old
            cost += old
        self.buf[self.size] = x
        self.size += 1
        self.costs.append(cost)


n = 1000
print(f"  Growth factor: {n} appends into a fresh array, for several factors r.")
print("  Capacity always lands in [n, r*n), so total copies land in")
print("  [n/(r-1), r*n/(r-1)) -- the last two columns are that interval.")
print()
print("        r    capacity   capacity/n   copies   copies/n      1/(r-1)"
      "     r/(r-1)")
for r in (1.125, 1.25, 1.5, 2.0, 3.0, 4.0):
    a = GrowArray(r)
    for i in range(n):
        a.append(i)
    print(f"  {r:>7}   {len(a.buf):>8}   {len(a.buf) / n:>11.4f}   {a.copies:>7}"
          f"   {a.copies / n:>9.4f}   {1 / (r - 1):>11.4f}   {r / (r - 1):>10.4f}")
print()
print("  Doubling is the usual compromise: it wastes less than half the")
print("  memory (capacity < 2n) and copies fewer than n elements.  A larger r")
print("  copies less and wastes more -- with r = 3 you may hold 3n slots.")

print()
print("  What an adversary can actually do: 1024 appends, nothing else.")
a = GrowArray(2.0)
for i in range(1024):
    a.append(i)
cheap = sum(1 for c in a.costs if c == 1)
mild = sum(1 for c in a.costs if 2 <= c <= 9)
brutal = sum(1 for c in a.costs if c >= 10)
total = sum(a.costs)
print(f"    appends costing exactly 1        : {cheap}")
print(f"    appends costing 2 to 9           : {mild}")
print(f"    appends costing 10 or more      : {brutal}")
print(f"    total work                      : {total}")
print(f"    total / n                       : {total / 1024:.4f}")
print(f"    work above the floor of 1 per op: {total - 1024}")
print()
print("  The six expensive appends are the resizes at sizes 16, 32, 64, 128,")
print("  256, 512: they copy 16 + 32 + 64 + 128 + 256 + 512 = 1008 elements and")
print("  cost 1008 + 6 writes = 1014 in total.  That is the most any sequence")
print("  can extract, and it is under 2 * 1024 = 2048.")
print(f"    measured total of the six largest costs: "
      f"{sum(sorted(a.costs)[-6:])}")
print(f"    measured total of all copies           : {a.copies} = 2^10 - 1")
```

### Block 4: a hash table — half amortised, half expected

```python
def good_hash(key, capacity):
    """A 32-bit avalanche mixer (the murmur3 finaliser), then mod capacity."""
    h = (key * 2654435761) & 0xFFFFFFFF
    h ^= h >> 16
    h = (h * 2246822519) & 0xFFFFFFFF
    h ^= h >> 13
    h = (h * 3266489917) & 0xFFFFFFFF
    h ^= h >> 16
    return h % capacity


def bad_hash(key, capacity):
    """The hash you get when nobody tests the hash function: all keys collide."""
    return 0


class Table:
    """Linear-probing hash table that doubles when it gets too full."""

    def __init__(self, capacity=8, max_load=0.75, hash_fn=good_hash):
        self.slots = [None] * capacity
        self.count = 0
        self.max_load = max_load
        self.hash_fn = hash_fn
        self.probes = 0          # comparisons made for the caller's inserts
        self.rehash_ins = 0      # keys moved because the table doubled
        self.rehash_probes = 0   # comparisons spent on those moves

    def _insert(self, key):
        i = self.hash_fn(key, len(self.slots))
        while self.slots[i] is not None:
            i = (i + 1) % len(self.slots)
            self.probes += 1
        self.slots[i] = key
        self.count += 1

    def insert(self, key):
        # Doubling keeps the load factor bounded.  Every key stored is
        # re-inserted once per doubling it survives, so the total number of
        # re-insertions over n inserts is a geometric series in n -- a fact
        # that holds no matter how good or bad the hash function is.
        if (self.count + 1) > self.max_load * len(self.slots):
            old, spent = self.slots, self.probes
            self.slots = [None] * (2 * len(old))
            self.rehash_ins += self.count
            for k in old:
                if k is not None:
                    self._insert(k)
            self.rehash_probes += self.probes - spent
            self.probes = spent
        self._insert(key)

    @property
    def total(self):
        return self.probes + self.rehash_ins + self.rehash_probes


print("  n sequential keys into a linear-probing table that doubles at load")
print("  factor 0.75.  Every unit of work is counted.")
print()
print("      n   capacity     load    probes   rehash ins   rehash probes"
      "    total   total/n")
for n in (128, 256, 512, 1024):
    t = Table()
    for k in range(n):
        t.insert(k)
    load = t.count / len(t.slots)
    print(f"  {n:>5}   {len(t.slots):>8}   {load:>6.3f}   {t.probes:>7}"
          f"   {t.rehash_ins:>10}   {t.rehash_probes:>14}"
          f"   {t.total:>7}   {t.total / n:>8.2f}")
print()
print("  Re-insertions are 1 + 2 + 4 + ... : a geometric series, so each key is")
print("  moved at most log2(n) times and the total stays linear in n.  No input")
print("  sequence can change the number of moves, which is what makes the")
print("  guarantee amortised rather than average.")

print()
print("  The same inserts into a table that never resizes, capacity = n, so")
print("  the load factor climbs to 1.0 and clustering explodes:")
print("      n   capacity   probes   total   total/n   total/n, doubling table")
for n in (128, 256, 512, 1024, 2048):
    fixed = Table(capacity=n, max_load=2.0)     # max_load 2.0 disables growth
    for k in range(n):
        fixed.insert(k)
    grow = Table()
    for k in range(n):
        grow.insert(k)
    print(f"  {n:>5}   {n:>8}   {fixed.probes:>7}   {fixed.total:>6}"
          f"   {fixed.total / n:>8.2f}   {grow.total / n:>18.2f}")
print()
print("  The left column climbs from 6.14 to 23.76 per insert as n grows by")
print("  16x.  The right column is flat at about 3.5, because the load factor")
print("  never exceeds 0.75 and each key is re-inserted only log2(n) times.")

print()
print("  AMORTISED IS NOT THE SAME AS EXPECTED.  A hash that collides")
print("  everything -- yet the table still doubles:")
print("      n   capacity    probes   rehash ins   rehash probes   total/n")
for n in (64, 128, 256):
    t = Table(hash_fn=bad_hash)
    for k in range(n):
        t.insert(k)
    print(f"  {n:>5}   {len(t.slots):>8}   {t.probes:>7}   {t.rehash_ins:>10}"
          f"   {t.rehash_probes:>14}   {t.total / n:>9.1f}")
print()
print("  Probes are 0 + 1 + ... + (n-1) = n(n-1)/2, because every key lands in")
print("  one cluster: 64 keys give 2016 = 64*63/2 comparisons.  But the COUNT")
print("  of re-insertions is 187, 379, 763 -- the same geometric series as with")
print("  the good hash.  How many keys move is amortised; how much work each")
print("  move costs is an expectation over random keys.  That is why Python")
print("  salts its string hashes and Rust randomises its HashMap seed.")
```

### Block 5: union-find, with each trick switched off in turn

```python
class DisjointSet:
    """Union-find, with the two standard tricks switched on and off."""

    def __init__(self, n, use_rank=True, use_compression=True):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.use_rank = use_rank
        self.use_compression = use_compression
        self.steps = 0             # parent pointers walked by every find

    def find(self, x):
        root, steps = x, 0
        while self.parent[root] != root:
            root = self.parent[root]
            steps += 1
        if self.use_compression and self.parent[x] != root:
            # Path compression: every node on the path now points at the root,
            # so the next find from any of them is a single step.
            while self.parent[x] != root:
                self.parent[x], x = root, self.parent[x]
        self.steps += steps
        return root

    def union(self, a, b):
        rb = self.find(b)
        if self.use_rank:
            ra = self.find(a)
            if ra == rb:
                return
            if self.rank[ra] < self.rank[rb]:
                ra, rb = rb, ra
            self.parent[rb] = ra
            if self.rank[ra] == self.rank[rb]:
                self.rank[ra] += 1
        else:
            # Naive: hang b's root under the ELEMENT a, not under a's root.
            # That is what turns the structure into a linked list.
            self.parent[rb] = a

    def depth(self, x):
        d = 0
        while self.parent[x] != x:
            x = self.parent[x]
            d += 1
        return d


def chain_order(n, ds):
    """(1,2), (2,3), ..., (n-1,n): each union attaches a fresh element."""
    for i in range(1, n):
        ds.union(i, i + 1)


def balanced_order(n, ds):
    """Merge components two at a time, always joining equals with equals.

    This is the order that separates a real union-find from a linked list:
    it builds a balanced tree when rank is used and a spike when it is not.
    """
    groups = [[i] for i in range(1, n + 1)]
    while len(groups) > 1:
        nxt = []
        for i in range(0, len(groups) - 1, 2):
            ds.union(groups[i][0], groups[i + 1][0])
            nxt.append(groups[i])
        if len(groups) % 2:
            nxt.append(groups[-1])
        groups = nxt


VARIANTS = [
    ("neither", False, False),
    ("path compression only", False, True),
    ("union by rank only", True, False),
    ("rank + compression", True, True),
]


def run(order, n):
    print(f"    variant                 union steps   find steps      total"
          "   total/n   max depth")
    for name, rank, comp in VARIANTS:
        ds = DisjointSet(n + 1, rank, comp)
        order(n, ds)
        union_steps = ds.steps
        deepest = max(ds.depth(x) for x in range(1, n + 1))
        for i in range(1, n + 1):
            ds.find(i)
        total = ds.steps
        print(f"    {name:<22}{union_steps:>11}{ds.steps - union_steps:>12}"
              f"{total:>10}{total / n:>10.1f}{deepest:>11}")


n = 2048
print(f"  {n} elements, {n - 1} unions, then one find per element.")
print("  steps = parent pointers walked.  Amortised claims bound the TOTAL,")
print("  for any order of operations the caller chooses.")
print()
print("  Order A: (1,2), (2,3), ..., (n-1,n).")
run(chain_order, n)
print()
print("  Order B: merge components in pairs, always equals with equals.")
run(balanced_order, n)
print()
print("  Order A without rank builds a chain of depth 2047, so querying every")
print(f"  element costs {n * (n - 1) // 2} steps -- quadratic.  Adding either")
print("  trick alone brings it to 2.0.  In order B the naive version is already")
print("  shallow (depth 11) and rank alone buys nothing there: still 5.5 per")
print("  operation, while compression alone fixes it, 5.5 down to 2.0.  Neither")
print("  experiment exhibits the order built to defeat each trick on its own,")
print("  but the theorems say those orders exist, which is why real")
print("  implementations use both, and why the amortised cost is alpha(n).")


def ack(m, j):
    """A(0,j) = j+1;  A(m,0) = A(m-1,1);  A(m,j) = A(m-1, A(m,j-1))."""
    stack = [m]
    while stack:
        a = stack.pop()
        if a == 0:
            j += 1
        elif j == 0:
            j = 1
            stack.append(a - 1)
        else:
            j -= 1
            stack.append(a - 1)
            stack.append(a)
    return j


# Rungs 1 to 4 are computed from the recurrence.  Rung 5 is A(5,0) =
# 2^16 - 3 and rung 6 is A(6,0) = 2^65536 - 3, from the same recurrence;
# the sixth is a 65536-bit integer, so it is written rather than computed.
LADDER = {k: ack(k, 0) for k in range(1, 5)}
LADDER[5] = 2 ** 16 - 3
LADDER[6] = "2^65536 - 3"


def alpha(n):
    """alpha(n) = the smallest k >= 1 with A(k,0) >= n."""
    for k in sorted(LADDER):
        bound = LADDER[k]
        if isinstance(bound, str) or n <= bound:
            return k
    return len(LADDER)


print()
print("  alpha(n) = the smallest k >= 1 for which n <= A(k,0):")
print("      k        A(k,0)   first n with alpha(n) = k")
for k in sorted(LADDER):
    below = LADDER[k - 1] + 1 if k - 1 in LADDER else 1
    print(f"  {k:>4}   {LADDER[k]:>13}   {below:>12}")
print()
print(f"  alpha(13) = {alpha(13)}   alpha(65533) = {alpha(65533)}   "
      f"alpha(10^6) = {alpha(10 ** 6)}")
print(f"  alpha(10^18) = {alpha(10 ** 18)}   alpha(2^65536 - 3) = "
      f"{alpha(2 ** 65536 - 3)}")
print()
print("  The sixth rung ends at 2^65536 - 3, a 65536-bit integer with 19729")
print("  decimal digits.  Every input that fits in memory has alpha(n) <= 6, so")
print("  union-find with both tricks is O(1) per operation in every program")
print("  anyone has ever written.  Textbooks that start the ladder one rung")
print("  lower quote 4 for the same bound; the content is identical.")
```

### Block 6: the sliding window — aggregate counting on a sequence

```python
values = [3, -1, 4, 1, -5, 9, 2, 6, -3, 7, -2, 8, 5, -4, 6, 1]
n, k = len(values), 4
print(f"  values = {values}")
print(f"  n = {n}, window width k = {k}, so there are {n - k + 1} windows")
print()


def naive_best(values, k):
    """Recompute each window from scratch: Theta(n * k) additions."""
    ops, best, at = 0, None, 0
    for start in range(len(values) - k + 1):
        total = 0
        for i in range(start, start + k):
            total += values[i]
            ops += 1
        if best is None or total > best:
            best, at = total, start
    return best, at, ops


def sliding_best(values, k):
    """Slide the window: each element is added once and removed at most once."""
    ops = 0
    total = sum(values[:k])
    ops += k
    best, at = total, 0
    for start in range(1, len(values) - k + 1):
        total += values[start + k - 1] - values[start - 1]
        ops += 2                       # one addition and one subtraction
        if total > best:
            best, at = total, start
    return best, at, ops


best_n, at_n, ops_n = naive_best(values, k)
best_s, at_s, ops_s = sliding_best(values, k)
print(f"  naive   : best sum {best_n}, window starting at index {at_n}, "
      f"{ops_n} additions")
print(f"  sliding : best sum {best_s}, window starting at index {at_s}, "
      f"{ops_s} operations")
print(f"  same answer: {best_n == best_s and at_n == at_s}")
print()
print(f"  Every window sum printed, both ways:")
for start in range(n - k + 1):
    print(f"    start {start:>2}: {sum(values[start:start + k]):>3}   "
          f"{''.join(f'{v:>4}' for v in values[start:start + k])}")
print()
print(f"  The naive pass touches each element {k} times, so its total is")
print(f"  {ops_n} = (n - k + 1) * k.  The sliding pass touches each element at")
print(f"  most twice -- once when it enters the window, once when it leaves --")
print(f"  for {ops_s} operations whatever k is.  That is the whole idea: replace")
print("  repeated work on overlapping inputs by a total accounting over the")
print("  whole sequence.")
print()
print("  How the gap grows.  Both passes, counted operation by operation:")
print("        n   k   naive ops   sliding ops   ratio")
for n_big, k_big in ((16, 2), (16, 4), (16, 8), (128, 8), (1024, 8)):
    data = (values * (n_big // 16 + 1))[:n_big]
    ops_a = naive_best(data, k_big)[2]
    ops_b = sliding_best(data, k_big)[2]
    print(f"  {n_big:>6}   {k_big}   {ops_a:>10}   {ops_b:>12}   "
          f"{ops_a / ops_b:>5.2f}")
print("  The naive count is (n - k + 1) * k; the sliding count is")
print("  k + 2 * (n - k).  Only the second is linear in n for fixed k.")
```

### Block 7: what a real Python list does

```python
import sys
import time
from collections import deque

# CPython stores a list as a C array of pointers, 8 bytes each, behind a
# 56-byte header, so sys.getsizeof leaks the allocated capacity exactly.
HEADER, SLOT = 56, 8
a = []
jumps = []
previous = 0
for i in range(1, 3001):
    a.append(i)
    capacity = (sys.getsizeof(a) - HEADER) // SLOT
    if capacity != previous:
        jumps.append((i, capacity, capacity / previous if previous else 0.0))
        previous = capacity

print("  Capacity jumps of a real CPython 3.11 list as it grows to 3000:")
print("      size   capacity   growth factor")
for size, capacity, factor in jumps:
    if size <= 200 or size > 2000:
        print(f"  {size:>7}   {capacity:>8}   {factor:>13.4f}")
print()
print("  The factor settles at about 1.127, not 2.  So a CPython list grows by")
print("  roughly one eighth per resize, which caps the wasted memory at an")
print("  eighth and costs about 1/(r-1) = 8 element copies per append instead")
print("  of the 1 that doubling gives.  Same O(1) amortised bound, eight times")
print("  the constant, a quarter of the memory overhead.")

print()
print("  What amortised analysis does NOT rescue: a single Theta(n) operation.")
N = 60000
front, back = [], []
t0 = time.perf_counter()
for i in range(N):
    front.insert(0, i)          # every element moves one slot right
t_front = time.perf_counter() - t0
t0 = time.perf_counter()
for i in range(N):
    back.append(i)              # amortised O(1)
t_back = time.perf_counter() - t0
d = deque(maxlen=0)
t0 = time.perf_counter()
for i in range(N):
    d.appendleft(i)             # O(1) worst case, no reallocation at all
t_deque = time.perf_counter() - t0
print(f"    list.insert(0, x) x {N}: {t_front * 1000:8.1f} ms")
print(f"    list.append(x)     x {N}: {t_back * 1000:8.1f} ms  "
      f"({t_front / t_back:.0f}x faster)")
print(f"    deque.appendleft   x {N}: {t_deque * 1000:8.1f} ms  "
      f"({t_front / t_deque:.0f}x faster)")
print()
print("  Amortised is a property of a SEQUENCE.  list.insert(0, x) is Theta(n)")
print("  on every single call, so a sequence of them is Theta(n^2) and no")
print("  amount of amortised reasoning changes that.  deque keeps its two ends")
print("  in separate blocks, so appendleft is O(1) in the worst case.")
```

---

## Common Mistakes

**Mistake 1 — writing "amortised $O(1)$" when you mean "average $O(1)$".**

```python
# Two tables, same capacity, same load factor, same number of inserts.
def mix(key, capacity):
    h = (key * 2654435761) & 0xFFFFFFFF
    h ^= h >> 16
    h = (h * 2246822519) & 0xFFFFFFFF
    h ^= h >> 13
    h = (h * 3266489917) & 0xFFFFFFFF
    h ^= h >> 16
    return h % capacity


def collisions(hash_fn, n, capacity=64):
    """Count key comparisons for n inserts into a table of fixed capacity."""
    slots, probes = [None] * capacity, 0
    for key in range(n):
        i = hash_fn(key, capacity)
        while slots[i] is not None:
            probes += 1
            i = (i + 1) % capacity
        slots[i] = key
    return probes


good = collisions(mix, 32, 64)
bad = collisions(lambda k, c: 0, 32, 64)
print(f"  a decent hash, 32 keys, 64 slots : {good:>5} comparisons")
print(f"  a hash that collides everything : {bad:>5} comparisons")
print(f"  ratio {bad / good:.0f}x, from the SAME insertion sequence")
print()
print("  'On average' is a claim about a distribution on inputs.  If the")
print("  distribution is the adversary, the average is the worst case.")
```

The wrong version is tempting because the two phrases are used
interchangeably in informal talk, and because `dict` really is $O(1)$ in
practice. The right version names the quantifier: amortised means *for every
sequence*, average means *over a distribution*, and the two can differ
without bound.

**Mistake 2 — adding up the costs of the cheap operations only.**

```python
sequence = [1, 2, 4, 8, 16, 32]        # the capacities a doubling array visits
size, idx, copies, writes, per_op = 0, 0, 0, 0, []
for _ in range(17):
    if size == sequence[idx]:
        copies += sequence[idx]
        per_op.append(1 + sequence[idx])
        idx += 1
    else:
        per_op.append(1)
    writes += 1
    size += 1
print(f"  counting every append : total {sum(per_op)}, amortised "
      f"{sum(per_op) / 17:.4f}")
print(f"  counting only the 1s  : total {writes}, amortised "
      f"{writes / 17:.4f}")
print(f"  forgetting the copies : {writes} + 0 = {writes}, but the real total is "
      f"{sum(per_op)}")
print()
print("  The error is undercounting, so the mistake looks like it proves the")
print("  STRONGER claim.  That is why 'amortised' proofs must charge the")
print("  expensive operations explicitly.")
```

Tempting because the expensive operations are rare and it feels wasteful to
count them. But a proof that drops `31` of the `48` units of real work has
not proved a tighter bound; it has proved nothing.

**Mistake 3 — assuming the amortised bound holds per operation.**

```python
per_op = [1, 2, 3, 1, 5, 1, 1, 1, 9, 1, 1, 1, 1, 1, 1, 1, 17]
print(f"  17 appends into a doubling array, cost of each: {per_op}")
print(f"  maximum single cost  : {max(per_op)}")
print(f"  mean (amortised)     : {sum(per_op) / 17:.4f}")
print(f"  17 * mean            : {sum(per_op) / 17 * 17:.0f}")
print()
print("  'Amortised O(1)' does NOT say every append costs O(1).  Append 17")
print("  costs 17 = Theta(n).  If you need a per-operation guarantee, you")
print("  need a different data structure.")
```

Tempting because engineers routinely say "append is O(1)" and then discover
a 40 ms pause in a latency-sensitive service. Amortised is a promise about
the *total* over the run; it says nothing about the longest single call.

**Mistake 4 — amortising something with no credit account.**

```python
# A structure that copies on EVERY append.  No amount of averaging helps.
class AlwaysCopies:
    def __init__(self):
        self.buf = []
        self.phi = 0            # a potential function was chosen but is useless

    def append(self, x):
        before = self.phi
        self.buf = list(self.buf) + [x]     # Theta(n) every single time
        self.phi = len(self.buf)
        return self.phi - before


a = AlwaysCopies()
charges = [a.append(i) for i in range(6)]
print(f"  amortised charge of each append: {charges}")
print(f"  total charge {sum(charges)} against {6} appends, so the")
print(f"  amortised cost is {sum(charges) / 6:.2f} and GROWS with n.")
print()
print("  The potential Phi = size gives DeltaPhi = +1 per append, so the")
print("  amortised cost is the true cost plus 1: n + n/2 + ... + 1 = Theta(n^2).")
print("  A potential function cannot rescue an operation that is expensive")
print("  every time.  The theorem requires an UPPER BOUND on the charge.")
```

Tempting because writing down a potential makes the proof *look* finished.
The requirement $\hat c_i \le c$ with $c$ constant is the whole content, and
here it is $n/2 + 1$, not a constant.

**Mistake 5 — extending an amortised result to operations it does not
cover.**

```python
# append is amortised O(1).  What about insert(0, x) on the same array?
backing = [0] * 1000
work = 0
for x in range(1000):
    backing.insert(0, x)          # every element shifts right one slot
    work += len(backing)          # one element move per stored element
print(f"  1000 insert(0, x) calls on a growing array: {work} element moves")
print(f"  per operation: {work / 1000:.0f} -- grows with n, so no amortised")
print("  O(1) argument applies.  The guarantee was about append, not insert.")
```

Tempting because the array and the buffer are the same object and it feels
like the same guarantee. It is not: the amortised bound is a statement about
one named operation on one data structure, and the potential function used
to prove it ($\Phi = 2|D| - |S|$) is worthless for a front insertion.

---

## Formula Sheet

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| aggregate cost | `$\sum_{i=1}^{n} c_i$` | the true total work of a whole sequence of operations | the only thing an amortised bound actually controls |
| amortised cost | `$\hat c(n)=\frac{1}{n}\sum_{i=1}^{n}c_i$` | the average cost per operation *over a worst-case sequence* | comparing a data structure's cost per operation |
| `$O(1)$` amortised | `$\exists c>0,\ \forall$ sequences: `$\sum_i c_i\le c\,n$` | constant work per operation in total, whatever the order | `list.append`, `dict` insert, union-find with both tricks |
| potential | `$\Phi:\mathcal{S}\to\mathbb{R}_{\ge0}$` | a non-negative score attached to the structure's state | the general proof technique |
| amortised charge | `$\hat c_i=c_i+\Phi(D_i)-\Phi(D_{i-1})$` | true cost plus what the operation gained or spent from the bank | proving an amortised bound in three lines |
| potential method theorem | `$\sum_i c_i=\sum_i\hat c_i-\Phi(D_n)+\Phi(D_0)\le\sum_i\hat c_i\le cn$` | the potential terms cancel, and the bank never owes you | the proof behind every amortised claim |
| accounting method | `$\hat c_i\ge c_i$`, surplus stored in the structure | pay in advance for future work | explaining why amortised bounds are believable |
| sum rule, inverted | `$T(n)=T(n-1)+\Theta(1)\Rightarrow T(n)=\Theta(n)$` | a loop with a constant-size body is $\Theta(1)$ amortised per iteration | connecting to [Lesson 24](24_recurrence_relations.md) |
| geometric series | `$\sum_{i=0}^{k}2^i=2^{k+1}-1$` | doubling total: `1 + 2 + 4 + 8 + 16 = 31` | every "the copies add up to less than $n$" argument |
| doubling: copies | `$2^{k+1}-1<2n$ where `$2^k<n\le2^{k+1}$` | total element copies for $n$ appends | proving `append` is $O(1)$ amortised |
| doubling: total | `$n+\text{copies}<3n$` | writes plus copies | the headline bound; amortised cost $<3$ |
| potential for doubling | `$\Phi=2|D|-|S|$` | twice the stored elements minus the capacity | getting a clean per-operation statement |
| per-operation charge | `$\hat c_i=c_i+\Delta\Phi=3$` exactly | every append charges 3, whether or not it copies | the sharpest form of the claim |
| initial potential term | `$\Phi(D_0)=2\cdot0-1=-1$` | a fresh empty array of capacity 1 | why the bound is $3n+1$ and not exactly $3n$ |
| growth factor `$r$` | `$n\le|S|<rn$`, copies `$\in[\frac{n}{r-1},\frac{rn}{r-1})$` | how much memory and copying you trade | choosing between memory and constants |
| doubling constant | `$\frac{1}{r-1}=1$ |r=2$` | one copy per element appended | why doubling is the standard choice |
| CPython's factor | `$r\approx1.127$ |r-1|\approx8$` | measured, not theoretical | why a Python list wastes an eighth of its memory |
| hash resize work | `$O(\log n)$` moves per key, `$\sum=O(n)$` total | each key is rehashed once per doubling it survives | `dict` insert is amortised $O(1)$ regardless of the hash |
| hash probe work | expected `$\Theta(1)$`, worst `$\Theta(n)$` | clustering is an expectation, not a guarantee | the reason for `PYTHONHASHSEED` and Rust's random seed |
| adversarial probe total | `$\sum_{k=0}^{n-1}k=\frac{n(n-1)}{2}$` | `2016` comparisons for 64 colliding keys | separating amortised from expected |
| union-find with one trick | `$O((m+n)\log n)$` | either rank or compression alone | why you need both |
| union-find with both | `$O((m+n)\alpha(n))$` | the inverse Ackermann function, `<=6$` for all storable `$n$ | Kruskal, connected components, union of ranges |
| Ackermann function | `$A(0,j)=j+1$`, `$A(m,0)=A(m-1,1)$`, `$A(m,j)=A(m-1,A(m,j-1))$` | the fastest-growing computable function | defining $\alpha$ |
| the $\alpha$ ladder | `$A(k,0)=2,3,5,13,65533,2^{65536}-3$` for `$k=1..6$` | it takes `2^65536` to climb one more rung | why $\alpha$ is a constant in practice |
| aggregate counting | `$\text{each element touched}\le c\ \Rightarrow\ T=O(cn)$` | count the total, not the parts | sliding windows, prefix sums, amortised tree traversals |
| sliding-window counts | naive `$(n-k+1)k$` vs sliding `$k+2(n-k)$ |r=2$` | `52` against `28` operations at `$n=16,k=4$` | every "two pointers" solution |

---

## Multiple Choice Questions

**Q1.** What does "the operation is $O(1)$ amortised" quantify over?

- A) The average of $c_i$ over one fixed sequence of $n$ operations
- B) Every sequence of $n$ operations, including sequences chosen by an adversary
- C) The expected cost of one operation, averaged over uniformly random inputs
- D) The cost of the $n/2$-th operation

<details>
<summary>Answer and explanation</summary>

**B) Every sequence of $n$ operations, including sequences chosen by an
adversary.**

Amortised analysis bounds the total, $\sum_{i=1}^n c_i \le cn$, for *every*
legal sequence. That universal quantifier is the definition, and it is why
the guarantee survives a caller who deliberately tries to trigger resizes.

Option A is the definition of the *arithmetic mean* of the costs, which is a
number, not a bound: an adversary can make the mean of one chosen sequence as
large as it likes, and a bound proven on one sequence proves nothing about
the next. Option C is the *expected* (average-case) bound — a real and useful
thing, but a statement over a distribution, which is exactly the distinction
Block 4 of the lesson measures: a hash that collides everything costs `57.8`
per insert where a decent one costs `3.59`, from the identical insertion
sequence. Option D confuses the amortised cost with the cost of some
particular operation; Block 2 shows the largest single append in 17 is `17`
units while the amortised cost is `3`.

</details>

**Q2.** In the worked example of 17 appends into a doubling array, how many
element copies are made?

- A) 16, because each of the 16 resizes copies the final capacity divided by two
- B) 17, because each append writes one element
- C) 31, since `1 + 2 + 4 + 8 + 16 = 2^5 - 1`
- D) 48, which is the total cost including the writes

<details>
<summary>Answer and explanation</summary>

**C) 31, since `1 + 2 + 4 + 8 + 16 = 2^5 - 1`.**

The resizes happen at appends `2, 3, 5, 9, 17` and copy `1, 2, 4, 8, 16`
elements, so the copies total `31` and the writes total `17`. The two
together give the `48` that Block 1 prints for `n = 17`.

Option A is the arithmetic of a different array — it assumes each resize
copies half the final capacity, which is only true if there were 16 resizes
rather than 5. Option B counts writes and calls them copies, the most common
way to lose a factor of two in this argument. Option D is the *total* cost,
which is the number the amortised bound divides by $n$; `48/17 = 2.8235`
and it is less than `3`, which is the bound.

</details>

**Q3.** The potential function $\Phi = 2|D| - |S|$ gives an amortised cost of
exactly `3` for every append. What does the `3` consist of?

- A) One unit for the write, plus a potential increase of 2 that a resize later spends
- B) Three units of copying, charged in advance
- C) One unit per element stored, times three
- D) The amortised cost of the last append, propagated backwards

<details>
<summary>Answer and explanation</summary>

**A) One unit for the write, plus a potential increase of 2 that a resize later
spends.**

From the table in the worked example: an append that finds room costs `1` and
raises $\Phi$ by `2` (from `2|D| − |S|` with `|S|` unchanged and `|D|` up by
one), so its charge is `3`. An append that resizes costs `1 + |D|` and drops
$\Phi$ by $|D| - 2$, so its charge is also `3`. The credit the cheap appends
store is exactly what pays for the copy.

Option B reverses the direction of the argument: the copies are real work,
charged when they happen, not pre-paid. Option C is a plausible-sounding
formula with no derivation — the charge does not scale with `|D|`, which is
visible in the table where append 17 copies 16 elements and still charges 3.
Option D is nonsense as an argument, though the *total* amortised cost does
equal `3 × 17 = 51`; the sum is what is fixed, not each operation by
inheritance.

</details>

**Q4.** A hash table doubles whenever its load factor would exceed `0.75`.
Which statement about insertion is true regardless of the hash function?

- A) Each insertion costs $\Theta(1)$ expected, so insertion is $\Theta(1)$ amortised
- B) The total number of element moves caused by resizing over $n$ insertions is $O(n)$
- C) The total number of probes over $n$ insertions is $O(n)$
- D) The table never needs to be probed more than twice

<details>
<summary>Answer and explanation</summary>

**B) The total number of element moves caused by resizing over $n$ insertions
is $O(n)$.**

How *many* keys move is forced by the capacity sequence, not by the keys: a
geometric series of table sizes, bounded by `1 + 2 + 4 + …`. Block 4 measures
it at `187`, `379`, `763` re-insertions for the colliding hash — identical to
the decent hash at the same $n$. That is the part of insertion that is
amortised.

Option A is exactly the confusion the question is testing: the $\Theta(1)$
probe cost is an expectation over randomness, not an amortised guarantee.
Option C is false and measurably so — with the colliding hash the probes are
`2016` at $n = 64$ and `32640` at $n = 256$, i.e. $\Theta(n^2)$ in total,
because each insert walks the whole cluster. Option D is false even with a
perfect hash: a load factor of `0.75` means clusters exist and linear
probing has to step through them.

</details>

**Q5.** Why is $\alpha(10^{6}) = 6$ in this lesson's convention, and not
something like `4`?

- A) Because $10^6$ is not a power of two
- B) Because the ladder of Ackermann values is $2, 3, 5, 13, 65533, 2^{65536}-3$, and $\alpha$ is the first rung that covers $n$
- C) Because the Ackermann function is not defined for $j = 0$
- D) Because union-find with both tricks is $\Theta(\log n)$ amortised and the extra `2` accounts for the two tricks

<details>
<summary>Answer and explanation</summary>

**B) Because the ladder of Ackermann values is $2, 3, 5, 13, 65533,
2^{65536}-3$, and $\alpha$ is the first rung that covers $n$.**

With $\alpha(n) = \min\{k \ge 1 : A(k,0) \ge n\}$: $A(3,0) = 5$ and
$A(4,0) = 13$ both fall below a million, and $A(5,0) = 65533$ does too, so
$\alpha(10^6) = 6$. Textbooks that define the ladder one rung lower quote
`4` for the same bound; only the indexing differs.

Option A is a non-sequitur — the Ackermann recursion has nothing to do with
powers of two. Option C is false: the definition $A(m,0) = A(m-1,1)$ is
where the fast growth comes from, and the code computes exactly those rungs.
Option D is a category error: with both tricks the bound is
$O((m+n)\alpha(n))$, and $\alpha$ is not $\log n$; the two tricks are what
make $\alpha$ possible, not an additive cost.

</details>

**Q6.** In Block 6 the sliding-window version of "best sum of $k$
consecutive elements" uses `28` operations where the naive version uses `52`
for $n = 16$, $k = 4$. Why does the sliding version not depend on $k$?

- A) Because it uses a faster arithmetic instruction
- B) Because each element is added once when it enters the window and subtracted at most once when it leaves, so the total is $k + 2(n-k)$
- C) Because `values` contains negative numbers, so the windows cancel
- D) Because the code computes only the windows it needs

<details>
<summary>Answer and explanation</summary>

**B) Because each element is added once when it enters the window and
subtracted at most once when it leaves, so the total is $k + 2(n-k)$.**

That is the aggregate-counting theorem: if each element is touched at most
$c$ times over the whole computation, the total is $O(cn)$ no matter what the
second parameter is. Block 6 shows the ratio climbing to `3.99` at
$(n, k) = (1024, 8)$ and would keep climbing with $k$.

Option A changes the constant factor, not the asymptotics — and lesson 80
already explains that a constant factor never makes one class beat another.
Option C is a misreading: sliding windows work identically on all-negative
data, and the answer `18` is computed from the same `values` list by both
versions. Option D is false, the code evaluates all $n-k+1 = 13$ windows and
prints every one of them.

</details>

**Q7.** Why does a fresh empty CPython list start with capacity `4` rather
than capacity `1`?

- A) Because CPython uses a growth factor of `4`
- B) Because the interpreter amortises the same way but with $r \approx 1.127$, and the small-size cases are special-cased
- C) Because the list object header is counted as four slots
- D) Because appends come in batches

<details>
<summary>Answer and explanation</summary>

**B) Because the interpreter amortises the same way but with $r \approx 1.127$,
and the small-size cases are special-cased.**

Block 7 measures the whole capacity history: `4` at size 1, then `8` at size
5, `16` at 9, `24` at 17, and a factor settling at `1.126` for large lists.
That is over-allocation by roughly one eighth, which caps wasted memory at
an eighth and raises the copy constant to about `1/(r−1) ≈ 8` per append —
the same $O(1)$ amortised bound as doubling with an eighth of the memory
overhead.

Option A is a misreading of the first row: capacity 4 at size 1 is the
initial allocation, not the growth factor, and the measured factor is
`1.127`. Option C is close to true and irrelevant: the 56-byte header is
subtracted precisely so it is *not* counted, which is why `(getsizeof −
56)/8` reads the capacity. Option D is not a mechanism — there is no batching,
and the code appends one element at a time.

</details>

**Q8.** Union-find is given `2048` elements and the sequence of unions
`(1,2), (2,3), ..., (2047,2048)`, followed by one `find` per element. Which
pair of observations is *both* consistent with the theorems?

- A) Naive total `2096128`, depth `2047`; with compression alone the total falls to `4093`
- B) Naive total `2048`, depth `2047`; with compression alone the total is unchanged
- C) Naive total `2096128`, depth `1`; with rank alone the depth stays `2047`
- D) Naive total `4093`, depth `2047`; with rank alone the total rises to `2096128`

<details>
<summary>Answer and explanation</summary>

**A) Naive total `2096128`, depth `2047`; with compression alone the total falls
to `4093`.**

Both figures are in Block 5's order-A table. The naive union hangs $b$'s
root under the *element* $a$, which builds a linked list of depth `2047`, and
querying every element walks $\sum_{i=1}^{2048}(i-1) = 2096128$ pointers.
Path compression flattens each path as it is walked, so the same sequence
costs `4093`.

Option B gets the quadratic figure wrong — the naive union phase costs `0`
(the root of the fresh element is found immediately) but the find phase costs
`2096128`. Option C swaps the two: depth `2047` belongs to the naive version
and depth `1` to the rank version, since equal ranks make every element hang
directly off one root. Option D has the totals backwards: compression
strictly reduces the work, it never increases it.

</details>

**Q9.** A system must guarantee that no single `list.append` takes longer than
`1` ms. Amortised analysis says append is $O(1)$. What follows?

- A) The requirement is satisfied, since $O(1)$ means a constant time
- B) Nothing follows; amortised bounds control totals, and append 17 in the worked example cost `17` units against an amortised `3`
- C) The requirement is satisfied if the list is longer than `1000`
- D) The requirement is satisfied because the amortised cost is an upper bound

<details>
<summary>Answer and explanation</summary>

**B) Nothing follows; amortised bounds control totals, and append 17 in the
worked example cost `17` units against an amortised `3`.**

This is the practical difference between an amortised bound and a worst-case
one. The amortised statement is "over $n$ appends the total is under $3n$",
which permits one call to cost $n$ units — it only forces the other calls to
be cheap. Block 3 shows `6` of `1024` appends costing `10` or more.

Option A confuses a bound on the total with a bound on each term. Option C is
backwards: a longer list makes the worst-case resize *more* expensive, since
the copy is proportional to the size. Option D is precisely the error: an
amortised cost of `3` is a bound on $\frac{1}{n}\sum c_i$, and individual $c_i$
can exceed it — for latency you need a structure like `deque` or a chunked
buffer.

</details>

**Q10.** Which of these is a statement about an *average case* rather than an
amortised bound?

- A) Every sequence of $n$ appends to a doubling array costs less than $3n$
- B) A well-distributed hash gives an expected constant number of probes per lookup
- C) Union-find with rank and path compression costs $O((m+n)\alpha(n))$ in total
- D) A sliding window touches each element at most twice

<details>
<summary>Answer and explanation</summary>

**B) A well-distributed hash gives an expected constant number of probes per
lookup.**

The word *expected* is the tell: it averages over the choice of keys or the
random seed. Block 4 separates the two halves of a dictionary insert — the
re-insertions caused by resizing are `187`, `379`, `763` regardless of the
hash, while the probes are `416` for a decent hash at $n = 1024$ and `32640`
for a colliding one at $n = 256$.

Option A quantifies over every sequence, which is the definition of amortised.
Option C is a total-cost bound over all operation sequences, so it is
amortised. Option D is an aggregate-counting statement — a deterministic
bound on the total, hence amortised in spirit and in letter.

</details>

---

## Subjective Questions

### Short Answer

**Q1. Define the amortised cost of a sequence of $n$ operations.**

<details>
<summary>Answer</summary>

If $c_i$ is the true cost of the $i$-th operation, the aggregate cost of the
sequence is $\sum_{i=1}^{n} c_i$ and the amortised cost is
$\hat c = \frac{1}{n}\sum_{i=1}^{n} c_i$. An operation is called $O(1)$
amortised if there are constants $c > 0$ and $n_0$ such that
$\sum_{i=1}^{n} c_i \le c\,n$ for **every** sequence of $n \ge n_0$
operations. The universal quantifier over sequences is what distinguishes it
from an average-case bound.

</details>

**Q2. State the potential method theorem and the role of each hypothesis.**

<details>
<summary>Answer</summary>

Let $\Phi$ be a potential function assigning a non-negative real to each
state of the data structure, with $\Phi(D_0) = 0$, and let
$\hat c_i = c_i + \Phi(D_i) - \Phi(D_{i-1})$. If $\hat c_i \le c$ for every
operation on every state, then $\sum_{i=1}^n c_i = \sum_i \hat c_i - \Phi(D_n)
\le cn$. The non-negativity is what stops the bank from going into debt
(free work from a negative initial potential), and the uniform bound on
$\hat c_i$ is what makes the total linear.

</details>

**Q3. What potential function proves that appending to a doubling array is
$O(1)$ amortised?**

<details>
<summary>Answer</summary>

$\Phi = 2|D| - |S|$, where $|D|$ is the number of stored elements and $|S|$
the capacity. An append with room costs `1` and raises $\Phi$ by `2`, so it is
charged `3`. An append that resizes costs $1 + |D|$ and lowers $\Phi$ by
$|D| - 2$, so it is also charged `3`. Since $\Phi \ge |D| \ge 0$ everywhere,
the theorem gives a total under $3n + 1$. In the worked example the 17
appends are charged `51 = 3 \times 17` while the true total is `48`.

</details>

**Q4. A hash table doubles at load factor `0.75`. Which part of insert is
amortised and which part is expected?**

<details>
<summary>Answer</summary>

The resize work is amortised: the number of keys that must be re-inserted is
forced by the capacity sequence, a geometric series totalling $O(n)$ over $n$
insertions, whatever the keys are. The probe work is only expected
$\Theta(1)$, averaged over the random seed or the choice of keys; an adversary
who knows the hash can force $\Theta(n)$ per insert and $\Theta(n^2)$ in
total. Block 4 measures both parts separately.

</details>

**Q5. Why is $\alpha(n)$ described as "effectively a constant" when it is a
function of $n$?**

<details>
<summary>Answer</summary>

Because the Ackermann ladder grows faster than any practical computation can
climb: $A(5,0) = 65533$ and $A(6,0) = 2^{65536} - 3$, a 65536-bit integer
with 19729 decimal digits. Since every input that fits in memory satisfies
$n < A(6,0)$, we have $\alpha(n) \le 6$ always. The function is unbounded in
theory and bounded in practice, which is why union-find is described as
$\Theta(1)$ per operation.

</details>

**Q6. Give an operation that is $O(1)$ amortised but not $O(1)$ worst case,
and one that is neither.**

<details>
<summary>Answer</summary>

`list.append` is $O(1)$ amortised (total under $3n$) but $\Theta(n)$ in the
worst case, since the $n$-th append of a doubling array copies $n/2$
elements. `list.insert(0, x)` is neither: every call shifts every stored
element, so $m$ calls cost $\Theta(m^2)$ and no credit is ever stored. The
distinction matters operationally — the second is a latency bug even though
its amortised *total* is linear.

</details>

### Long Answer

**Q1. Why does an amortised guarantee say nothing about worst-case latency,
and what breaks if you treat it as if it did?**

<details>
<summary>Model answer</summary>

An amortised bound is a statement about $\sum_{i=1}^n c_i$ for $n$
operations: it says the total is at most $cn$. Individual terms are
unconstrained beyond that, and one of them may be as large as the total
allows. In the worked example the 17 appends cost `1, 2, 3, 1, 5, 1, 1, 1,
9, 1, 1, 1, 1, 1, 1, 1, 17` — the last one is 17 units while the amortised
cost is `2.8235`, and in Block 3 six of 1024 appends cost 10 or more.

What breaks is any design that promises a per-operation deadline. A garbage
collector that amortises its mark phase over the heap, a network stack that
amortises buffer flushes, a server that promises 1 ms per request: each of
these can hit a pause of order $n$ at the worst moment, and for a service
with a tail-latency target that is the whole game. Two things follow in
practice. First, bound the *maximum* work per operation, not just the total —
either by chunking (flush 64 KB at a time instead of the whole backlog) or by
choosing a structure with a worst-case bound, such as `deque.appendleft` in
place of `list.insert(0, x)`. Second, measure the tail, not the mean:
amortised analysis deliberately averages away exactly the events that a
latency-sensitive system cannot afford.

The deep point is that the two guarantees answer different questions.
Amortised asks "what is the total budget over the run?"; worst case asks
"what is the largest single step?" Only the second bounds a deadline, and
only the first is achievable by the resizing trick that makes append cheap in
the first place.

</details>

**Q2. Prove that $n$ appends to a doubling array copy fewer than $2n$
elements, and say what breaks if the array grows by a factor of `1.1`
instead.**

<details>
<summary>Model answer</summary>

Let the capacities visited be $2^0, 2^1, \dots, 2^{k+1}$, where $2^k < n \le
2^{k+1}$. A resize from capacity $2^j$ copies $2^j$ elements, so the total is
$\sum_{j=0}^{k} 2^j = 2^{k+1} - 1$. Since $2^k < n$, we get $2^{k+1} < 2n$,
hence copies $< 2n$. Block 1 confirms it: $n = 17$ gives `31` copies
($= 2^5 - 1$), $n = 100$ gives `127 = 2^7 - 1$, and $n = 1000$ gives
`1023 = 2^{10} - 1`.

Now let $r = 1.1$. The same summation gives approximately $n/(r-1) = 10n$
copies — still $O(n)$, so the operation is *still* $O(1)$ amortised and the
asymptotic claim survives. What breaks is the constant and the memory trade.
Block 3 measures it at $n = 1000$: $r = 1.125$ needs `8466` copies
(`8.4660` per append) against `1023` for doubling. The copy constant is
$\frac{1}{r-1}$, which diverges as $r \to 1$: at $r = 1.01$ you would copy
about `100n` elements, and no amount of asymptotic notation would hide that
from a profiler.

Why the divergence is not a paradox: the ratio of successive capacities is
$1.1$, so a series with ratio `1.1` converges far more slowly than one with
ratio `2`, and the sum is dominated by the last term times $\frac{1}{r-1}$.
Doubling is the standard choice because it is the largest jump that keeps
$1/(r-1) = 1$ while wasting less than half the capacity; the theoretical
optimum $r = e$ is never used because $2$ is a power of two, which makes the
capacity arithmetic exact.

</details>

**Q3. Amortised analysis is often called "the average case with better
marketing". Give the sharpest version of why that is wrong.**

<details>
<summary>Model answer</summary>

The difference is the quantifier, and it is not cosmetic. An average-case
bound states $\mathbb{E}[c] = O(1)$ for a single operation, where the
expectation is over a distribution on inputs (or over a random seed inside
the data structure). An amortised bound states $\sum_{i=1}^n c_i \le cn$ for
**every** sequence. Averaging requires that some distribution exist and be
known; amortising requires nothing but the sequence itself.

Block 4 makes the gap measurable on one code path. The table that doubles at
load factor `0.75` performs the identical number of key moves — `187`, `379`,
`763` re-insertions for the colliding hash — regardless of the hash function,
because how many keys move depends only on the capacity sequence. Those are
amortised facts. The probes are different: `416` comparisons at $n = 1024$
with a decent hash, `32640` at $n = 256$ with a colliding one. No argument
about the total can rescue the second number, because the adversary chooses
the keys.

Two further consequences. First, amortised bounds are robust under
composition in a way expectations are not: if each of $m$ operations is
$O(1)$ amortised, their total is $O(m)$ regardless of how the caller
interleaves them, which is exactly what union-find needs — the order of
unions and finds is chosen by the algorithm's control flow, not sampled.
Second, the failure mode differs. A violated expectation shows up as
occasional slowness (Python salts `str` hashes precisely because
`PYTHONHASHSEED = 0` was once a denial-of-service vector); a violated
amortised bound shows up as growth in the *total*, which is a different kind
of bug and one that benchmarks can hide.

</details>

**Q4. Union-find with path compression alone and union by rank alone each
cost $O((m+n)\log n)$; with both it is $O((m+n)\alpha(n))$. Explain why the
two tricks are complementary, and why the bound is stated on the total.**

<details>
<summary>Model answer</summary>

The two tricks attack different failure modes. Rank keeps the trees shallow
by always attaching the shallower root to the deeper one, so no element ever
sits more than $\lfloor \log_2 n \rfloor$ pointers from its root — the size
of a component is at least doubled whenever its rank increases, and there are
only $\log_2 n$ ranks. Compression makes the trees flat *along the paths that
are actually walked*, by pointing every node on a walked path straight at the
root; it does nothing about nodes nobody has queried.

Block 5 shows both halves. In order A, where each union attaches a fresh
element to a growing chain, the naive version reaches depth `2047` and costs
`2096128` steps — rank alone fixes this, because the stars it builds have
depth `1`. In order B, where equal-sized components are merged pairwise, the
naive tree is already shallow (depth `11`) and rank alone buys nothing:
still `11264` steps, or `5.5` per operation, while compression alone brings it
to `4083`, or `2.0`. There are inputs constructed to defeat each trick in
isolation; that is why every real implementation uses both.

The bound is on the total because that is what the proof produces. The
potential function counts how much credit a query has stored; an individual
`find` can spend a great deal (Block 5's `2.0` average hides individual walks
of up to `11`), and the amortised argument shows only that the total
converges. With both tricks the total is $O((m+n)\alpha(n))$ and $\alpha$ is
at most `6` for any storable input, which is why union-find is used as if it
were $O(1)$ — while still being the correct answer to "why is this fast?"

</details>

---

## Exercises and Solutions

**[ ] Exercise 1 —** A stack is implemented on a fixed array of capacity $n$
with a pointer `top`. Each `push` writes one element; when `top` reaches the
end the implementation *doubles its capacity*, which costs one copy of all $n$
stored elements. (a) Give the amortised cost of `push` in terms of the
doubling factor. (b) Give the exact total cost of the first $2^{k+1}$ pushes
starting from capacity `1`. (c) Explain why `pop` is $O(1)$ *worst case* here
while `push` is only $O(1)$ amortised.

<details>
<summary>Solution</summary>

(a) With growth factor $r$, the total copies for $n$ pushes lie in
$\left[\frac{n}{r-1}, \frac{rn}{r-1}\right)$, so the amortised cost is
$1 + \frac{1}{r-1}$ (doubling gives $< 2$; CPython's measured $r \approx
1.127$ gives about `9`).

(b) The resizes occur at pushes $2, 3, 5, 9, \dots, 2^{k+1}$ and copy
$1, 2, 4, \dots, 2^{k}$ elements, so the copies total $2^{k+1} - 1$ while the
writes total $2^{k+1}$. The total is therefore $2^{k+2} - 1$. For $k = 4$,
that is $n = 32$ pushes costing $31$ copies plus $32$ writes, i.e. `63`
units, and $63/32 = 1.9688 < 2$.

(c) `pop` removes the top element, which is always at a known position; no
copying and no resizing is ever needed, so its worst-case cost is one write.
`push` must occasionally copy, so it can only be bounded on average — which
is the general asymmetry: destructive monotone operations are often
worst-case cheap, while operations that grow a structure must occasionally
pay for the growth.

</details>

**[ ] Exercise 2 —** You are given a sequence of $n$ operations on a dynamic
array where each operation is either `append` (cost 1 plus any resize cost)
or `delete_last` (cost 1, and it halves the capacity whenever the array is
less than a quarter full). Show that a sequence with no operations at all
still satisfies a total bound of $O(n)$, and explain why shrinking does not
help the adversary.

<details>
<summary>Solution</summary>

Shrinking adds an amortised charge but cannot remove one. Use the potential
$\Phi = 2|D| - |S|$ as before. A `delete_last` that does not trigger a shrink
lowers $|D|$ by one, so $\Delta\Phi = -2$ and its charge is $1 - 2 = -1$: the
operation is *paid* to the bank rather than charged. The bank therefore
builds credit, and a later halving — which copies $|D|$ elements at a moment
when $|S| = 4|D|$ or so — spends it. Since a halving only happens after at
least $|S|/4 \ge |D|$ deletions, the credit is always there. The total over
any sequence stays $\le cn$ with a slightly larger $c$, and deleting elements
gives an adversary no way to force repeated growth, because growth requires
appends and each append is charged at most $c$.

</details>

**[ ] Exercise 3 —** Implement an instrumented array in Python that reports,
after $n$ appends: the capacity, the total number of copies, the total
amortised charge computed with $\Phi = 2|D| - |S|$, and the identity
$\sum \hat c_i = \sum c_i + \Phi(D_n) - \Phi(D_0)$. Verify the identity for
$n = 1, 2, 3, 17, 64$ and print a table. Then break it deliberately: replace
the potential with $\Phi = |D|$ and report the largest single charge you
observe.

<details>
<summary>Solution</summary>

The identity is algebra, not an estimate, so it must hold for every $n$. For
$n = 17$ the true total is `48`, the amortised total is `51`, and
$48 + (2) - (-1) = 51$ exactly, which is what Block 2 prints. A run over
$n = 1, 2, 3, 17, 64$ should show the same agreement to the last digit at
every $n$.

With $\Phi = |D|$ the charges are `2` for an append with room and
$1 + |D| + 1 = |D| + 2$ for one that resizes: at $n = 17$ the largest single
charge is `18`, at append 17, and the charges are unbounded as $n$ grows.

</details>

**[ ] Exercise 4 —** A hash table uses open addressing with linear probing and
doubles at load factor `0.5`. (a) Give an upper bound on the total number of
element moves over $n$ insertions, in terms of $n$. (b) Explain why that
bound is independent of the hash function while the number of probes is not.
(c) With linear probing at load factor $\alpha$, the expected number of probes
per insertion is $\frac{1}{2}\left(1 + \frac{1}{(1-\alpha)^2}\right)$: compute
its value at $\alpha = 0.5$ and at $\alpha = 0.75$.

<details>
<summary>Solution</summary>

(a) Each resize copies the whole table and the table doubles, so the moves
form a geometric series: $O(n)$ in total, and at most $n$ per key per
doubling it survives, $\log_2 n$ doublings. Block 4 measures `3067` re-
insertions at $n = 1024$ with a threshold of `0.75`.

(b) The count of moves depends only on the sequence of capacities, which is
determined by the number of insertions, not by the keys. Probes depend on
where the keys land: Block 4 shows `187`, `379`, `763` moves for both a good
and a colliding hash at the same $n$, but `416` versus `32640` probes.

(c) At $\alpha = 0.5$: $\frac{1}{2}(1 + 4) = 2.5$ probes. At $\alpha = 0.75$:
$\frac{1}{2}(1 + 16) = 8.5$ probes. The expected cost per operation is
constant either way, but it is multiplied by 3.4 — which is why production
tables keep the load factor near `0.5` even though resizing costs something.

</details>

**[ ] Exercise 5 —** Union-find is used to label connected components. (a) Show
that union by rank gives depth at most $\lfloor \log_2 n \rfloor$. (b) Give an
input order for which path compression *alone* still costs
$\Theta((m+n)\log n)$, and say why rank alone also fails on some input.
(c) Explain what the combined bound looks like for the practical case
$n = 10^6$, $m = 10^6$.

<details>
<summary>Solution</summary>

(a) Whenever a root's rank increases, its component's size has just doubled,
because it absorbed an equal-rank component. A component's size is at least
$2^{\text{rank}}$, so rank is at most $\log_2 n$ and so is the depth.

(b) Compression alone fails when the interesting queries hit different deep
paths and the structure is repeatedly rebuilt; rank alone fails on Block 5's
order B, where merging equal-sized components pairwise leaves rank unable to
help and the total stays at `5.5` per operation while compression gets `2.0`.
Both are $O(\log n)$ amortised, and both are fixed by the combination.

(c) $\alpha(10^6) = 6$ with this lesson's convention, so the total is
$O(2 \times 10^6 \times 6) = O(12 \times 10^6)$ steps. Compare with
connected components by BFS, which is $\Theta(n + m)$ with no inverse
Ackermann factor at all — union-find wins only when $m \gg n$, because of the
inverse Ackermann factor's constant.

</details>

**[ ] Exercise 6 —** A program maintains a sorted list and needs the sum of
every contiguous block of length $k$, for one fixed $k$. (a) Give the total
cost of computing each sum independently. (b) Give the total cost of the
sliding-window method. (c) For what values of $k$ is the naive method actually
preferable, and why is the answer "almost never"?

<details>
<summary>Solution</summary>

(a) $(n-k+1)\cdot k$ additions: every element is read $k$ times.
Block 6 measures `52` at $(n,k) = (16,4)$ and `8136` at $(1024,8)$.

(b) $k + 2(n-k)$ operations: `k` to build the first window, then one addition
and one subtraction per shift — `28` at $(16,4)$ and `2040` at $(1024,8)$.

(c) The sliding method is never worse for $k \ge 2$ and is $O(1)$ better at
$k = 2$ (`30` against `30`), then strictly better: `52` against `28` at $k=4$,
`72` against `24` at $k=8$. The naive method's constant per element is
identical to the sliding method's, so there is no $k$ at which it wins.

</details>

**Challenge.**

**[ ]** *Amortised or not?* Your team maintains a buffer with a capacity
policy: start at capacity 8; when full, grow to $1.25$ times the current
capacity plus 4; when the number of elements drops below a quarter of
capacity, shrink to half. (a) Compute, with a script, the amortised cost of
`append` for this policy at $n = 10^5$, and compare it with doubling and with
CPython's measured factor. (b) Find an input sequence — appends and deletes —
that makes the *total* cost larger than any pure-append sequence of the same
length. (c) Explain what the shrink rule buys you, and what it costs, and
decide whether you would keep it.

<details>
<summary>Solution</summary>

(a) Growth by $r = 1.25$ plus a constant 4 gives total copies around
$\frac{n}{r-1} = 4n$, so the amortised cost per append is about `5` against
`2` for doubling and about `9` for CPython's `1.127`. The $+4$ matters only
in the first few resizes; asymptotically the ratio is what counts.

(b) Alternate: append until the buffer is full, then delete enough elements to
drop below a quarter of capacity, then fill again. Each cycle triggers a
shrink *and* a grow, and each of those copies a constant fraction of the
buffer, so the total is $\Theta(n)$ but with a much larger constant than
appending alone. This is the honest answer: amortised bounds hold for
*every* sequence, but they are tight only for some, and adversarial sequences
pick the worst constant.

(c) The shrink rule bounds wasted memory after a burst — a buffer that grew to
a million entries and then emptied should not hold a million slots forever.
It costs an extra copy per shrink and a slightly worse append constant,
because the capacity sequence is no longer monotone and the geometric series
must be restarted. Keep it if memory is the binding constraint, drop it if
throughput is; what you must not do is quote the amortised constant of a
pure-append analysis for a structure whose policy allows these cycles.

</details>

---

## Summary

- Amortised analysis bounds the **total** of a sequence,
  $\sum_{i=1}^{n} c_i \le cn$, for **every** sequence — adversary included —
  and reports the per-operation figure $\frac{1}{n}\sum c_i$.
- The potential method makes the proof three lines: charge
  $\hat c_i = c_i + \Phi(D_i) - \Phi(D_{i-1})$, and the potential terms
  telescope away, leaving $\sum c_i \le \sum \hat c_i$.
- A potential is a bank balance: cheap operations store credit, expensive ones
  spend it. A potential that stores no credit proves nothing.
- Doubling a dynamic array copies $1 + 2 + 4 + \dots = 2^{k+1} - 1 < 2n$
  elements over $n$ appends, so the total is under $3n$ and each append is
  $O(1)$ amortised.
- With $\Phi = 2|D| - |S|$ the amortised cost of every append is **exactly**
  `3`, which is stronger than the average-cost statement.
- One append costing $\Theta(n)$ does not contradict an $O(1)$ amortised
  bound; the series is dominated by its last term, and no sequence of $n$
  appends can pay more than the total.
- Amortised is not average. Resize work in a hash table is amortised
  regardless of the hash; probe work is only an expectation, and a colliding
  hash turns `416` comparisons into `32640`.
- Union-find with rank and path compression costs $O((m+n)\alpha(n))$ in
  total, and $\alpha(n) \le 6$ for any input that fits in memory.
- Growth factor $r$ trades copies $\approx \frac{1}{r-1}$ per append against
  up to a factor $r$ of wasted memory; doubling sits at copies $< n$, memory
  $< 2n$.
- Sliding windows are aggregate counting: if each element is touched at most
  twice, the total is $O(n)$ no matter how wide the window is.
- Never quote an amortised number as a latency guarantee. `list.append` is
  $O(1)$ amortised and `list.insert(0, x)` is $\Theta(n)$ every time; only
  the first is a sum, and only the second is a deadline.

---

## Next

[82 — Mathematical Tools for Algorithm Design](82_tools_for_algorithm_design.md)
collects the rest of the toolkit: recurrences and the Master Theorem,
divide and conquer, greedy algorithms with their exchange argument, dynamic
programming, invariants, and lower bounds. It assumes this lesson's habit of
counting totals over a sequence, because the greedy and dynamic-programming
proofs are all statements about what can be rearranged without paying twice.