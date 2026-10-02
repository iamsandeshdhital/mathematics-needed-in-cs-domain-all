# 82 — Mathematical Tools for Algorithm Design

**Part**: part06_algorithms_math · **Prerequisites**: 24, 80 · **Time**: 45 min

---

## In Plain Words

This lesson is the toolbox you reach for after you know what big-O is. It
covers four things: how to work out how long a recursive algorithm takes by
writing down a recurrence and solving it, how to prove an algorithm is
correct rather than merely hopeful, how to decide whether a problem should be
attacked by divide and conquer, by taking the locally best choice, or by
building a table of answers, and how to prove that a problem is intrinsically
hard so you stop looking for something clever. Each tool is a way of turning
a vague intuition into a statement you can check, and the whole subject comes
down to a handful of patterns that reappear in every algorithm you will ever
read.

---

## Why Computer Science Cares

- **`sorted()` in Python is Timsort**, which is merge sort with a greedy
  twist: it finds the already-sorted *runs* in the input and merges them in
  proportion to their length. On nearly sorted data it is $O(n)$ instead of
  $O(n \log n)$, because the recurrence it induces has fewer effective levels.
- **CPython multiplies large integers with Karatsuba.** Below a size
  threshold it does schoolbook multiplication; above it, the recursion
  $T(n) = 3T(n/2) + \Theta(n)$ takes over and the exponent drops from 2 to
  $\log_2 3 \approx 1.585$. Block 2 measures `43046721` single-digit products
  where schoolbook would need `4294967296` at 65536 digits.
- **`git diff`, `difflib`, and BLAST all run dynamic programming.** Matching
  two versions of a file is a longest-common-subsequence table; aligning two
  DNA sequences is the same table with scores. The states are pairs of
  positions, and the table has one entry per pair.
- **Every router runs a greedy algorithm with an admissible heuristic.**
  A* is Dijkstra plus an estimate of the remaining distance, and it is
  correct only because the estimate never overestimates — a proof obligation,
  not a heuristic feeling.
- **Database engines sort a million rows faster than a comparison sort
  could.** Counting sort, radix sort and bucket sort beat $\Omega(n \log n)$
  because the lower bound's precondition — that the only question you may ask
  is "is $a[i] \le a[j]$?" — does not hold when you may use arithmetic on the
  keys.
- **Knowing a problem is `#P`-complete saves weeks.** That is the formal
  statement that no polynomial algorithm is likely to exist, and recognising
  that a problem is in that class is a skill that
  [Lesson 28](../part02_discrete_combinatorics/28_counting_strategies.md)
  asks for directly.

---

## The Formal Version

**Definition.** A *recurrence relation* for the cost of an algorithm is an
equation $T(n) = \sum_{i=1}^{k} a_i\,T(n/b_i) + \Theta(n^c)$ together with
base cases, where $a_i$ is the number of subproblems of size $n/b_i$ and the
last term is the work done at this node without recursing. It is well-founded
when repeated substitution reaches a base case, which is what makes it a
statement about an actually-terminating program.

*Explanation.* The notation is
[Lesson 80](80_big_o_and_complexity.md)'s, but the content is
[Lesson 24](24_recurrence_relations.md)'s: the cost of a recursive function
on $n$ is a sum of the costs of its recursive calls plus its own work.

**Theorem (Master Theorem).** Let $T(n) = a\,T(n/b) + \Theta(n^c)$ with
$a \ge 1$, $b > 1$, and let $d = \log_b a$. Then

$$T(n) = \begin{cases} \Theta(n^d) & c < d \\ \Theta(n^d \log n) & c = d \\ \Theta(n^c) & c > d \end{cases}$$

*Explanation.* Three shapes, all visible in the recursion tree: leaves dominate
when $c < d$, the internal work dominates when $c > d$, and when they are
equal every level costs the same and there are $\log_b n$ of them.

**Theorem (method of substitution).** Suppose $T(n) \le g(n)$ is the guess.
Then: verify the base case, show $T(n/b) \le g(n/b)$ implies
$T(n) \le g(n)$ by one algebraic step, and conclude. The guess is proved
only when the base case *and* the induction step hold.

*Explanation.* The step is where guesses die. For $T(n) = 3T(n/2) + n$ the
pure guess $c\,n^{d}$ fails for **every** constant $c$, because
$3c(n/2)^d = c\,n^d$ exactly, leaving no slack to absorb the $+n$. The
repair is a guess with a lower-order subtraction, $c\,n^d - \lambda n$.

**Theorem (recursion tree method).** The total cost is the sum over levels of
$(\text{nodes at level } i)\times(\text{work per node})$, plus the leaves. If
the level costs form a geometric series with ratio $\frac{a}{b} > 1$ and the
leaves cost $\Theta(a^k)$ where $n = b^k$, then $T(n) = \Theta(n^{\log_b a})$.

**Definition.** A *loop invariant* is a predicate $I(k)$ about the program's
state after $k$ iterations of a loop, such that (a) $I$ holds before the first
iteration, (b) $I(k) \wedge$ (the guard holds at step $k$) $\Rightarrow I(k+1)$,
and (c) $I(k) \wedge \neg$(guard) implies the postcondition.

**Theorem (invariant template).** If an algorithm is initialised into $I$, and
$I$ is maintained by every iteration, and $I$ plus the failed guard implies
the specification, then the algorithm is correct. Termination must be proved
separately, by a variant that strictly decreases.

*Explanation.* This is just induction on $k$ wearing an implementation's
clothes. The three obligations are the three obligations, and the reason
students skip them is that the code works without them — on the inputs they
tried.

**Definition.** A *greedy algorithm* commits to the locally best choice and
never revises it.

**Theorem (exchange argument).** If, for every optimal solution $O$, there is
an optimal solution $O'$ that contains the greedy choice, then greedy is
optimal. It is proved by exhibiting the swap that turns $O$ into $O'$ while
preserving feasibility and the objective value.

*Explanation.* The proof is always the same shape: take the first point where
greedy and $O$ disagree, swap, show nothing got worse. When no such swap
exists for any of the three possibilities (take it / leave it / replace
something), greedy is wrong — and the failure is always worth writing down,
because knapsack has a 2-line counterexample.

**Definition.** A *matroid* is a pair $(E, \mathcal{I})$ where $E$ is a finite
set, $\mathcal{I}$ is a family of subsets containing $\varnothing$ and closed
under taking subsets, and for all $A, B \in \mathcal{I}$ with $|A| < |B|$
there is an element $x \in B \setminus A$ with $A \cup \{x\} \in \mathcal{I}$.

**Theorem (greedy on matroids).** On a matroid, sorting the ground set by
weight and taking elements while independence is preserved yields a minimum
weight basis. Scheduling, minimum spanning trees and the matching problem on
bipartite graphs are the standard examples.

*Explanation.* The exchange property is exactly the condition the proof needs,
which is why matroid theory is not an abstraction for its own sake: it names
the class of problems where "sort and take" is provably right.

**Definition.** A problem has *optimal substructure* if an optimal solution is
built from optimal solutions of smaller subproblems; it has *overlapping
subproblems* if the same subproblems recur in different branches.

**Theorem (dynamic programming).** A problem with both properties admits the
table fill $F(s) = \min/\max \{ \text{combine} \}$ over the distinct states $s$,
computed once each, in time $O(\#\text{states} \times \text{work per state})$.

**Theorem (Bellman-Ford).** On a graph with $V$ vertices and negative edge
weights, $V-1$ passes of relaxation compute every shortest path; if a
$V$-th pass still relaxes an edge, a negative cycle is reachable from the
source and shortest paths do not exist.

**Theorem (Dijkstra).** Dijkstra's algorithm is correct when all edge weights
are non-negative, and can return a wrong answer with a single negative edge.

**Definition.** A *lower bound* is a function $g(n)$ such that no correct
algorithm in a stated class runs in $o(g(n))$.

**Theorem (comparison sorting is $\Omega(n \log n)$).** A comparison sort's
execution is a binary decision tree with at least $n!$ leaves, so its depth
is at least

$$\log_2 (n!) = \log_2(n\log_2 e - n + \tfrac12 \log_2 (2\pi n) + O(1/n)) = \Theta(n \log n) .$$

*Explanation.* The bound is a counting argument: there are $n!$ possible
inputs and a binary question gives at most one bit, so $\log_2 n!$ questions
are needed. Merge sort uses $n\log_2 n - n + 1$ comparisons, leaving a gap of
$(\log_2 e - 1)n \approx 0.4427n$ that nobody has closed.

---

## Worked Example

### Example 1: solving $T(n) = 3T(n/2) + n$ three ways

**Step 1 — write the recurrence.** Splitting an array of $n$ elements into
three halves and doing $\Theta(n)$ local work gives $T(n) = 3T(n/2) + n$ with
$T(1) = 1$.

**Step 2 — the recursion tree.** Level $i$ holds $3^i$ nodes of size
$n/2^i$, and each does $n/2^i$ units of local work, so level $i$ costs
$3^i \cdot n/2^i = n(3/2)^i$. For $n = 64$:

| level | nodes | node size | level cost | running total |
| --- | --- | --- | --- | --- |
| 0 | 1 | 64 | 64 | 64 |
| 1 | 3 | 32 | 96 | 160 |
| 2 | 9 | 16 | 144 | 304 |
| 3 | 27 | 8 | 216 | 520 |
| 4 | 81 | 4 | 324 | 844 |
| 5 | 243 | 2 | 486 | 1330 |
| leaves | 729 | 1 | 729 | **2059** |

The internal levels sum to 1330 and the leaves to 729 — but the leaves are
not the biggest single *level*, they are the biggest single term once you
count the last few internal levels, and more importantly they are the term
that does not shrink. The level costs form a geometric series with ratio
$3/2$, so they total $2n((3/2)^{k} - 1) = \Theta(n^{\log_2 3})$, and the
leaves are exactly $3^k = n^{\log_2 3}$. Both contributions are the same
order, and $T(64) = 2059$ confirms it.

**Step 3 — try the substitution method, and fail.** Guess $T(n) \le c\,n^{d}$
with $d = \log_2 3$. The induction step needs

$$c\,n^{d} \ \ge\ 3c\left(\frac{n}{2}\right)^{d} + n = c\,n^{d} + n,$$

because $2^{d} = 3$ makes the recursive term exactly $c\,n^d$. That is false
for every $c$ and every $n$; the code measures the ratio as `1.6667`,
`1.3333`, `1.0667`, `1.0007` for $c = 1, 2, 10, 1000$, all $> 1$. **A guess
with no slack cannot absorb the additive term when the leaves exactly fill
the budget.**

**Step 4 — repair the guess.** Try $T(n) \le c\,n^{d} - \lambda n$. Then

$$3\left(c\left(\tfrac{n}{2}\right)^{d} - \lambda\tfrac{n}{2}\right) + n = c\,n^{d} - \left(\tfrac32\lambda - 1\right)n,$$

so the step succeeds exactly when $\frac32\lambda - 1 \ge \lambda$, i.e.
$\lambda \ge 2$. The base case $n = 1$ needs $1 \le c - \lambda$, i.e.
$c \ge 3$. With $\lambda = 2$, $c = 3$ the bound is *tight*: the code measures
a difference of `0.000000` at every one of $n = 2, 4, \dots, 1024$. The
exact solution is

$$T(2^{k}) = 3^{k+1} - 2^{k+1},$$

and at $n = 1024$ that is `175099`.

**Step 5 — confirm with the Master Theorem.** $a = 3$, $b = 2$, $d = \log_2 3
\approx 1.58496$, additive term $\Theta(n^1)$, so $c = 1 < d$ and

$$T(n) = \Theta(n^{\log_2 3}) = \Theta(n^{1.5850}).$$

All three methods agree, and each contributed something different: the tree
gave the shape, the substitution gave the constant, and the theorem gave the
answer without algebra.

### Example 2: the exchange argument, executed

**Problem.** Choose as many mutually non-overlapping intervals as possible from
$(1,3), (2,5), (3,7), (5,9), (6,10), (8,12), (9,13)$.

**The rule.** Always take the available interval with the earliest finishing
time. The trace is: take $(1,3)$; skip $(2,5)$; take $(3,7)$; skip $(5,9)$;
skip $(6,10)$; take $(8,12)$; skip $(9,13)$. Three intervals.

**The proof.** Let $O$ be any optimal solution and let $g = (1,3)$ be the
earliest-finishing interval overall. $O$'s first interval $o$ satisfies
$\text{finish}(o) \ge \text{finish}(g)$. Consider $O' = (O \setminus \{o\})
\cup \{g\}$. $|O'| = |O|$. Is $O'$ feasible? The only new conflict $g$ could
create is with the interval of $O$ that follows $o$, and that interval starts
at or after $\text{finish}(o) \ge \text{finish}(g)$. So no. Hence $O'$ is
optimal and contains the greedy choice, and the argument repeats on the
intervals starting at or after $\text{finish}(g)$. Brute force over all $2^7 =
128$ subsets confirms the count `3` is optimal.

**Where the same argument breaks.** 0/1 knapsack, capacity 50, items
$(10,60), (20,100), (30,120)$. Greedy by value/weight takes the ratio-6.0 item
first and returns `160`. The optimum is `220`, from items $(20,100)$ and
$(30,120)$. There is no exchange that repairs the swap: the greedy item and
both optimal items fit together, so removing the greedy item does not free
enough capacity to take both, and adding them exceeds the capacity. The
exchange property is genuinely false, which is why knapsack is not solved by
sorting.

### Example 3: a DP table, filled completely

Longest common subsequence of `ABCBDAB` and `BDCABA`. The state is the pair of
prefix lengths; there are $8 \times 7 = 56$ of them:

```
          B  D  C  A  B  A
      |   0  0  0  0  0  0
    A |   0  0  0  0  1  1  1
    B |   0  1  1  1  1  2  2
    C |   0  1  1  2  2  2  2
    B |   0  1  1  2  2  3  3
    D |   0  1  2  2  2  3  3
    A |   0  1  2  2  3  3  4
    B |   0  1  2  2  3  4  4
```

Row $i$ and column $j$ hold the LCS length of the first $i$ characters of the
first string and the first $j$ of the second. Reading a cell: if the two
characters agree, take the diagonal plus one; otherwise take the larger of
the cell above and the cell to the left. The answer is the bottom-right entry,
`4`. The table is $O(mn)$ and the naive recursive version is $O(\varphi^{m+n})$
because it recomputes the same cells exponentially often.

### Example 4: a lower bound by counting

A comparison sort must distinguish $n!$ orderings. Its only tool is a
two-valued question, so its execution tree has at least $n!$ leaves and depth
at least $\log_2 n!$ bits. At $n = 128$ that is `716.162` bits, while merge
sort uses `769` comparisons — a gap of `52.84`, tracking the
$0.4427 \times 128 = 56.67$ that Stirling predicts. The bound is about 7 bits
per element here and it only worsens with $n$.

---

## Runnable Code

### Block 1: one recurrence, three methods

```python
import math


def T(n):
    """T(n) = 3*T(n/2) + n with T(1) = 1, exactly.  n must be a power of 2."""
    if n == 1:
        return 1
    return 3 * T(n // 2) + n


def level_work(n, level):
    """Non-recursive work at one level of the recursion tree."""
    nodes, size = 3 ** level, n // (2 ** level)
    return nodes, size, nodes * size


d = math.log2(3)
print("  Solving T(n) = 3*T(n/2) + n, T(1) = 1, with d = log2(3) = "
      f"{d:.5f}.")
print()
print("  METHOD 1: the recursion tree.  Level i holds 3^i nodes of size")
print("  n/2^i, so level i costs 3^i * n/2^i = n * (3/2)^i: a geometric")
print("  series with ratio 1.5, which is dominated by its last term.")
print()
n = 64
print(f"    level   nodes   node size   work at level   running total")
running = 0
for level in range(int(math.log2(n))):
    nodes, size, work = level_work(n, level)
    running += work
    print(f"  {level:>7}   {nodes:>6}   {size:>10}   {work:>14}   {running:>16}")
leaves = 3 ** int(math.log2(n))
running += leaves
print(f"  {'leaves':>7}   {leaves:>6}   {1:>10}   {leaves:>14}   {running:>16}")
print()
print(f"  T(64) by direct recursion: {T(64)} -- the same total.")

print()
print("  METHOD 2: substitution.  First the guess that FAILS, T(n) <= c*n^d:")
print("     3*c*(n/2)^d = c*n^d exactly, because 2^d = 3, so the induction")
print("     step asks c*n^d >= c*n^d + n, which is impossible.")
print("        c   worst (3*c*(n/2)^d + n) / (c*n^d)   verdict")
for c in (1.0, 2.0, 10.0, 1000.0):
    worst = max((3 * c * (2 ** (k - 1)) ** d + 2 ** k) / (c * (2 ** k) ** d)
                for k in range(1, 12))
    print(f"  {c:>7.1f}   {worst:>34.6f}   {'fails' if worst > 1 else 'works'}")
print("  No constant saves the pure power guess.  The fix is a slack term:")
print("  guess T(n) <= c*n^d - lambda*n.  The induction step then reads")
print("     3*(c*(n/2)^d - lambda*(n/2)) + n = c*n^d - (1.5*lambda - 1)*n,")
print("  so the step succeeds exactly when 1.5*lambda - 1 >= lambda, i.e.")
print(f"  lambda >= 2, and the base case n = 1 needs 1 <= c - lambda, i.e. "
      f"c >= 3.")
lam, c = 2, 3
print()
print(f"  With lambda = {lam} and c = {c} the bound T(n) <= c*n^d - lambda*n "
      f"is tight:")
print("        n   T(n) by recursion   c*n^d - lambda*n   difference")
for k in range(1, 11):
    size = 2 ** k
    exact = T(size)
    bound = c * size ** d - lam * size
    print(f"  {size:>6}   {exact:>17}   {bound:>17.1f}   {exact - bound:>10.6f}")
print(f"  Equality holds at every power of two, so the closed form really is")
print(f"  T(2^k) = 3^(k+1) - 2^(k+1): at k = 10, n = 1024, T = {T(1024)}.")

print()
print("  METHOD 3: the Master Theorem.  a = 3, b = 2, so d = log_b(a) = "
      f"{d:.5f},")
print(f"  and the additive term is Theta(n^1), so c = 1 < d = {d:.4f}.")
print(f"  Verdict: T(n) is Theta(n^d) = Theta(n^{d:.4f}).  The leaves")
print("  dominate, exactly as the tree in Method 1 showed.")
print()
print("  What each method is for:")
print(f"    recursion tree   the shape: {leaves} leaves dominate at n = 64")
print("    substitution     the exact constant: T(2^k) = 3^(k+1) - 2^(k+1)")
print(f"    Master Theorem   the class at once: Theta(n^{d:.4f}), no algebra")
```

### Block 2: divide and conquer, measured

```python
import math


def merge_sort_count(data):
    """Merge sort that returns (sorted list, exact number of key comparisons)."""
    if len(data) <= 1:
        return list(data), 0
    mid = len(data) // 2
    left, cl = merge_sort_count(data[:mid])
    right, cr = merge_sort_count(data[mid:])
    merged, cm = [], 0
    i = j = 0
    while i < len(left) and j < len(right):
        cm += 1                       # one comparison decides this step
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, cl + cr + cm


def lcg(n, seed=987654321):
    """Deterministic pseudo-random data -- reproducible across machines."""
    state, values = seed, []
    for _ in range(n):
        state = (1103515245 * state + 12345) % (2 ** 31)
        values.append(state)
    return values


def worst_case(n):
    """The arrangement that forces every merge to run the full m - 1 times.

    At each merge the two halves are interleaved alternately, so one side is
    never eliminated early.  This is the input an adversary would hand you.
    """
    if n == 1:
        return [1]
    half = n // 2
    low = worst_case(half)
    high = [x + half for x in worst_case(half)]
    merged, i, j = [], 0, 0
    while i < half and j < half:
        merged.append(low[i])
        i += 1
        if i < half and j < half:
            merged.append(high[j])
            j += 1
    merged.extend(low[i:])
    merged.extend(high[j:])
    return merged


print("  MERGE SORT, comparisons counted exactly.  A merge of two sorted")
print("  halves of total size m costs between m/2 and m - 1 comparisons, and")
print("  every level of the recursion holds n elements in all, so every level")
print("  costs between n/2 and n - 1 comparisons.  There are log2(n) levels.")
print()
print("        n     ascending   descending   pseudo-random   adversarial"
      "   n*log2(n)-n+1")
for k in (4, 6, 8, 10, 12):
    n = 2 ** k
    ascending, c_up = merge_sort_count(list(range(1, n + 1)))
    descending, c_down = merge_sort_count(list(range(n, 0, -1)))
    noisy = lcg(n)
    shuffled, c_noisy = merge_sort_count(noisy)
    nasty = worst_case(n)
    _, c_worst = merge_sort_count(nasty)
    assert ascending == descending == list(range(1, n + 1))
    assert shuffled == sorted(noisy) and sorted(nasty) == list(range(1, n + 1))
    print(f"  {n:>7}   {c_up:>12}   {c_down:>11}   {c_noisy:>14}   {c_worst:>11}"
          f"   {n * k - n + 1:>16}")
print("  Sorted and reversed input are BOTH the best case for this merge")
print("  rule: exactly n*log2(n)/2 comparisons.  The adversarial column hits")
print("  the bound n*log2(n) - n + 1 exactly, which is why merge sort is")
print("  quoted as Theta(n log n) and never better.")

LEAVES = 0


def karatsuba(x, y, width):
    """Multiply two integers whose decimal widths are at most `width`.

    Three recursive multiplications of half the size replace the four of
    schoolbook multiplication.  LEAVES counts single-digit products.
    """
    global LEAVES
    if width == 1:
        LEAVES += 1
        return x * y
    half, base = width // 2, 10 ** (width // 2)
    x0, x1 = x % base, x // base
    y0, y1 = y % base, y // base
    z0 = karatsuba(x0, y0, half)
    z2 = karatsuba(x1, y1, half)
    # One extra half-size product replaces the two cross terms:
    z1 = karatsuba(x1 + x0, y1 + y0, half) - z0 - z2
    return z2 * base * base + z1 * base + z0


print()
print("  KARATSUBA MULTIPLICATION: three half-size products instead of four.")
print("  The recursion tree holds 3^i subproblems of size n/2^i at level i,")
print("  so the leaves are 3^k single-digit products for n = 2^k digits:")
print("  n^log2(3) = n^1.5850 single-digit products instead of n^2.")
print()
print("      n   schoolbook n^2   karatsuba leaves   ratio   log_n of the ratio")
for k in (4, 8, 12, 16):
    n = 2 ** k
    x, y = 7 ** n, 3 ** n
    LEAVES = 0
    product = karatsuba(x, y, n)
    leaves = LEAVES
    assert product == x * y
    print(f"  {n:>6}   {n * n:>14}   {leaves:>19}   {n * n / leaves:>6.2f}   "
          f"{math.log(n * n / leaves, n):>17.4f}")
print("  Every product was checked against Python's built-in multiplication,")
print("  and the leaves are exactly 3^k: 81, 6561, 531441, 43046721.")
print("  The measured log_n of the ratio is 0.4150 = 2 - log2(3), so the")
print("  saving is a power-law improvement and not a constant factor.")
print()
print("  Where it comes from: schoolbook needs four half-size products,")
print("  x0y0, x0y1, x1y0, x1y1.  Karatsuba gets the cross terms from")
print("  (x0+x1)(y0+y1) - x0y0 - x1y1, so three calls replace four.  The")
print("  recursion T(n) = 3T(n/2) + Theta(n) is the one solved in Block 1,")
print("  which is why the exponent is that same 1.5850.")
```

### Block 3: greedy, the exchange argument, and where it dies

```python
def brute_force_activities(intervals):
    """Every compatible subset, by brute force.  Only for tiny inputs."""
    best = []
    for mask in range(1 << len(intervals)):
        chosen = [intervals[i] for i in range(len(intervals))
                  if mask >> i & 1]
        chosen.sort()
        ok = all(chosen[i][1] <= chosen[i + 1][0]
                 for i in range(len(chosen) - 1))
        if ok and len(chosen) > len(best):
            best = chosen
    return best


def greedy_activities(intervals):
    """Earliest finishing time first -- the exchange argument in six lines."""
    chosen, finish = [], -1
    for start, end in sorted(intervals, key=lambda iv: iv[1]):
        if start >= finish:
            chosen.append((start, end))
            finish = end
    return chosen


intervals = [(1, 3), (2, 5), (3, 7), (5, 9), (6, 10), (8, 12), (9, 13)]
print("  ACTIVITY SELECTION: choose as many mutually compatible intervals as")
print("  possible.  The greedy rule is 'always take the available interval that")
print("  finishes first', and the proof is an exchange argument.")
print()
print(f"  input: {intervals}")
print("  greedy trace, earliest finish first:")
finish = -1
for start, end in sorted(intervals, key=lambda iv: iv[1]):
    if start >= finish:
        print(f"    take ({start}, {end}) -- nothing ends earlier and still fits")
        finish = end
    else:
        print(f"    skip ({start}, {end}) -- overlaps the interval ending at "
              f"{finish}")
best = brute_force_activities(intervals)
greedy = greedy_activities(intervals)
print()
print(f"  greedy chose {len(greedy)}: {greedy}")
print(f"  brute force found {len(best)}: {best}")
print(f"  optimal: {len(greedy) == len(best)}")
print()
print("  The exchange argument.  Let O be an optimal solution and let g be the")
print("  available interval with the earliest finish.  O's first interval o has")
print("  finish(o) >= finish(g), so replacing o by g keeps the count and cannot")
print("  create a conflict: everything that started after finish(o) also starts")
print("  after finish(g).  Repeat on the remaining intervals.  The whole proof")
print("  is that one swap.")

# --- where greedy fails ------------------------------------------------------
def knapsack_dp(weights, values, capacity):
    """Best value for at most `capacity`, exact and optimal."""
    best = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for c in range(capacity, w - 1, -1):
            best[c] = max(best[c], best[c - w] + v)
    return best[capacity]


items = [(10, 60), (20, 100), (30, 120)]
capacity = 50
print()
print("  WHERE GREEDY FAILS: 0/1 knapsack, capacity "
      f"{capacity}, items (weight, value):")
print(f"    {items}")
print(f"    value/weight ratios: "
      f"{[round(v / w, 3) for w, v in items]}")

greedy_density, left = 0, capacity
for w, v in sorted(items, key=lambda iv: -iv[1] / iv[0]):
    if w <= left:
        greedy_density += v
        left -= w
greedy_value, left = 0, capacity
for w, v in sorted(items, key=lambda iv: -iv[1]):
    if w <= left:
        greedy_value += v
        left -= w
optimal = knapsack_dp([w for w, _ in items], [v for _, v in items], capacity)
print(f"    greedy by value/weight : {greedy_density}   "
      f"(takes the item of ratio 6.0 first)")
print(f"    greedy by raw value    : {greedy_value}")
print(f"    dynamic programming    : {optimal}")
print(f"    greedy by density loses {optimal - greedy_density}, which is exactly")
print("    the classic failure: the densest item blocks two lighter ones whose")
print("    combined value is larger.  Greedy has no way to know that, because")
print("    the ratio of one item says nothing about how items interact.")

print()
print("  The DP table for the same instance, compressed to the capacities where")
print("  the value changes.  The recurrence is")
print("     OPT(i, c) = max( OPT(i-1, c), v_i + OPT(i-1, c - w_i) )")
print("  -- either skip item i, or take it and spend its weight.")
table = [[0] * (capacity + 1)]
for w, v in items:
    row = table[-1][:]
    for c in range(capacity + 1):
        if c >= w:
            row[c] = max(row[c], table[-1][c - w] + v)
    table.append(row)
for i, (w, v) in enumerate(items, 1):
    row = table[i]
    changes = [(c, row[c]) for c in range(1, capacity + 1)
               if row[c] != row[c - 1]]
    print(f"    items 1..{i}, last weight {w:>2}: "
          + "  ".join(f"{val}@c={c}" for c, val in changes))
print(f"  The last row's best entry is {max(table[-1])}, reached at capacity "
      f"{table[-1].index(max(table[-1]))}.")
print(f"  It beats greedy by density ({greedy_density}) because the optimal set")
print("  is the two heaviest items, which greedy by density never puts")
print("  together: it spends the whole capacity on one light item first.")
```

### Block 4: dynamic programming, state by state

```python
from functools import lru_cache
from math import comb


def lcs_table(x, y):
    """The full dynamic-programming table for the longest common subsequence."""
    m, n = len(x), len(y)
    table = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])
    return table


x, y = "ABCBDAB", "BDCABA"
table = lcs_table(x, y)
print("  LONGEST COMMON SUBSEQUENCE.  x = ABCBDAB, y = BDCABA.")
print("  The state is the PAIR OF PREFIX LENGTHS, and there are (m+1)(n+1) of")
print("  them -- 8 * 7 = 56 states, each computed once from two smaller ones.")
print()
print("        " + "".join(f"{c:>3}" for c in " " + y))
for i in range(len(x) + 1):
    label = " " if i == 0 else x[i - 1]
    print(f"  {label} | " + "".join(f"{v:>3}" for v in table[i]))
print()
print(f"  LCS length = {table[-1][-1]}.  The recurrence is")
print("     L(i,j) = L(i-1,j-1) + 1            if x[i-1] == y[j-1]")
print("     L(i,j) = max( L(i-1,j), L(i,j-1) )  otherwise")
print("  The naive alternative -- try both 'take' and 'skip' recursively --")
print("  recomputes the same states exponentially many times.")

CALLS = 0


def fib_naive(n):
    global CALLS
    CALLS += 1
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


@lru_cache(maxsize=None)
def fib_memo(n):
    return n if n < 2 else fib_memo(n - 1) + fib_memo(n - 2)


CALLS = 0
value = fib_naive(28)
naive_calls = CALLS
assert fib_memo(28) == value
memo_states = fib_memo.cache_info().currsize
print()
print(f"  fib(28) = {value}")
print(f"    plain recursion : {naive_calls} function calls")
print(f"    with memoisation: {memo_states} distinct states evaluated, each "
      f"exactly once")
print("  Plain recursion grows like the golden ratio to the n -- about")
print(f"  1.6^28 = {1.618 ** 28:.0f} -- while memoisation is linear in n.")
print("  That is the entire argument for memoisation: the overlapping")
print("  subproblems ARE the subproblems.")

print()
print("  BITMASK DYNAMIC PROGRAMMING: when the state is a SUBSET.")
print("  Choosing k items out of n is C(n,k) states, not 2^n -- and when k is")
print("  fixed that gap is the difference between a search you can finish and")
print("  one you cannot start.")
print("       n   k   C(n,k) states   2^n subsets   ratio")
for n, k in ((8, 3), (20, 3), (30, 3), (40, 4), (60, 3)):
    print(f"  {n:>6}   {k}   {comb(n, k):>13}   {2 ** n:>19}   "
          f"{2 ** n / comb(n, k):>10.1f}x")


def best_k_of_n(values, k):
    """Maximum total value of exactly k items, found by exhaustive search."""
    best = 0
    for choice in range(1 << len(values)):
        if bin(choice).count("1") != k:
            continue
        total = sum(v for i, v in enumerate(values) if choice >> i & 1)
        best = max(best, total)
    return best


values = [3, 9, 2, 7, 5, 11, 4]
answer = best_k_of_n(values, 3)
print()
print(f"  best total of exactly 3 items from {values}: {answer}")
print(f"    the three largest are 11, 9 and 7, which sum to {11 + 9 + 7}")
print("    For 'choose k and maximise an additive score' the exhaustive search")
print("    over C(n,k) subsets is already optimal, and no cleverness improves")
print("    on it: that is Lesson 21's binomial coefficient doing the work.")
```

### Block 5: shortest paths, and the edge that breaks Dijkstra

```python
import heapq


# A graph where Dijkstra gives the WRONG answer, with no ties anywhere.
EDGES = [
    ("S", "A", 1), ("S", "B", 6), ("A", "B", 2), ("A", "C", 5),
    ("B", "C", 3), ("B", "T", 1), ("C", "T", -10),
]
NODES = ["S", "A", "B", "C", "T"]


def adjacency(edges, nodes):
    adj = {v: [] for v in nodes}
    for u, v, w in edges:
        adj[u].append((v, w))
    return adj


def dijkstra(adj, source):
    """Standard Dijkstra: a settled vertex is never reopened."""
    dist = {v: float("inf") for v in adj}
    settled = set()
    dist[source] = 0
    heap, trace = [(0, source)], []
    while heap:
        d, u = heapq.heappop(heap)
        if u in settled:
            continue
        settled.add(u)
        trace.append((u, d))
        for v, w in adj[u]:
            if v not in settled and d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    return dist, trace


def bellman_ford(edges, nodes, source, passes=None):
    """Each pass propagates exactly one more edge along every path."""
    dist = {v: float("inf") for v in nodes}
    dist[source] = 0
    history = []
    for _ in range(len(nodes) - 1 if passes is None else passes):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
        history.append(dict(dist))
    return dist, history


adj = adjacency(EDGES, NODES)
dist, trace = dijkstra(adj, "S")
bf, history = bellman_ford(EDGES, NODES, "S")
print("  SHORTEST PATHS ON A GRAPH WITH A NEGATIVE EDGE.")
print("  directed edges (u, v, weight):")
for u, v, w in EDGES:
    print(f"    {u} -> {v}   weight {w}")
print()
print("  Dijkstra settles vertices in order of distance from S:")
for vertex, d in trace:
    print(f"    settle {vertex} at distance {d}")
print(f"  Dijkstra reports T = {dist['T']}, Bellman-Ford reports "
      f"T = {bf['T']}.")
print("  The true shortest path is S -> A -> B -> C -> T = 1 + 2 + 3 - 10 = -4.")
print(f"  Dijkstra is wrong by {dist['T'] - bf['T']}: it settled T at "
      f"{dist['T']} before it had")
print("  ever reached C, and standard Dijkstra never reopens a settled")
print("  vertex.  One negative edge is enough.")
print()
print("  Bellman-Ford, one pass at a time, n - 1 = 4 passes:")
order = ["S", "A", "B", "C", "T"]
print("    pass " + "".join(f"{v:>9}" for v in order))
for i, snapshot in enumerate(history, 1):
    row = "".join(f"{snapshot[v]:>9}" if snapshot[v] != float("inf")
                  else f"{'inf':>9}" for v in order)
    print(f"    {i:>4} " + row)
print("  Pass 1 already fixes every distance here because the edge list")
print("  happens to be in a helpful order; passes 2 to 4 change nothing,")
print("  which is what the theorem promises.")

NEG = [("X", "Y", 1), ("Y", "Z", -3), ("Z", "X", 1)]
neg_nodes = ["X", "Y", "Z"]
_, neg_history = bellman_ford(NEG, neg_nodes, "X", passes=4)
print()
print("  NEGATIVE CYCLE DETECTION.  Edges X->Y (1), Y->Z (-3), Z->X (1) hold")
print("  the cycle X -> Y -> Z -> X of total weight 1 - 3 + 1 = -1 < 0, so")
print("  distances are unbounded below.  Here is dist[X] after each pass:")
print("    " + ", ".join(f"pass {i}: {snap['X']}"
                       for i, snap in enumerate(neg_history, 1)))
print("  Still improving on pass 4, so a negative cycle is reachable.  The")
print("  rule: if an (n + 1)-th pass relaxes anything, a negative cycle exists.")

DAG = [("P", "Q", 2), ("P", "R", 5), ("Q", "R", 1), ("Q", "S", 4),
       ("R", "S", -3)]
dag_nodes = ["P", "Q", "R", "S"]


def dag_shortest(edges, nodes, source):
    """Topological order first: a vertex's distance is final on arrival."""
    indegree = {v: 0 for v in nodes}
    out = {v: [] for v in nodes}
    for u, v, w in edges:
        out[u].append((v, w))
        indegree[v] += 1
    queue = [v for v in nodes if indegree[v] == 0]
    dist = {v: float("inf") for v in nodes}
    dist[source] = 0
    while queue:
        u = queue.pop(0)
        for v, w in out[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return dist


dag_dist = dag_shortest(DAG, dag_nodes, "P")
print()
print("  ON A DAG THE NEGATIVE EDGE IS HARMLESS: process vertices in")
print("  topological order P, Q, R, S and every distance is final on arrival.")
print("  edges " + str(DAG))
print(f"  distances from P: {dag_dist}")
print(f"  shortest P->S = 2 + 1 - 3 = {dag_dist['S']}, in O(V + E) time and")
print("  without a priority queue -- which is why route-finding on a DAG is")
print("  linear while on a general graph it is O(E log V) or O(V E).")
```

### Block 6: loop invariants, checked by the machine

```python
def binary_search(a, key):
    """Binary search, printing the loop invariant after every step.

    INVARIANT (true at the top of each iteration, and checked below):
      1. the target, if present, lies in a[lo..hi];
      2. a[lo - 1] < key      (everything left of the window is too small);
      3. a[hi + 1] > key      (everything right of the window is too big).
    """
    lo, hi, steps = 0, len(a) - 1, 0
    while lo <= hi:
        steps += 1
        mid = (lo + hi) // 2
        print(f"    step {steps}: window a[{lo}..{hi}], mid index {mid}, "
              f"a[{mid}] = {a[mid]}")
        # --- maintenance: each of the three claims survives the step --------
        if a[mid] == key:
            assert a[lo - 1] < key if lo > 0 else True
            assert a[hi + 1] > key if hi + 1 < len(a) else True
            print(f"      found at index {mid} after {steps} steps")
            return mid
        if a[mid] < key:
            lo = mid + 1
        else:
            hi = mid - 1
        # --- the invariant is re-established here ---------------------------
        assert lo <= hi + 1
        if lo > 0:
            assert a[lo - 1] < key
        if hi + 1 < len(a):
            assert a[hi + 1] > key
    return -1


a = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print("  LOOP INVARIANTS.  The invariant is a statement that is true before")
print("  the loop, preserved by every iteration, and strong enough at the end")
print("  to conclude the postcondition.")
print()
for key in (23, 2, 91, 7):
    print(f"  binary_search(a, {key}):")
    result = binary_search(a, key)
    if result >= 0:
        assert a[result] == key
        print(f"      verified: a[{result}] == {key}")
    else:
        assert key not in a
        print(f"      verified: {key} is not in the list")
print()
print("  The three parts of the proof, mapped onto those lines:")
print("    initialisation  lo = 0, hi = len(a) - 1 brackets the whole array")
print("    maintenance     the three comparisons below the midpoint each cut")
print("                    the window and keep claims 2 and 3 true")
print("    termination     each iteration halves the window, so the loop ends")
print("    conclusion      the answer is inside the window, which is now empty,")
print("                    so it does not exist -- or a[mid] matched")
print("  Without the invariant you have a loop and a hope.")


def partition(a, lo, hi):
    """Lomuto partition.

    INVARIANT: a[lo..p-1] <= a[p] < a[p+1..hi] at every step, and the
    elements below p are all <= the pivot, so the pivot's final index is p.
    """
    pivot = a[hi]
    p = lo
    for j in range(lo, hi):
        if a[j] <= pivot:
            a[j], a[p] = a[p], a[j]
            p += 1
    a[p], a[hi] = a[hi], a[p]
    return p


print()
print("  A second invariant, in quicksort's partition step.  Values "
      "8, 3, 7, 1, 9, 2")
data = [8, 3, 7, 1, 9, 2]
p = partition(data, 0, len(data) - 1)
print(f"  after partitioning: {data}, pivot index {p}")
left, right = data[:p], data[p + 1:]
print(f"    left  of the pivot: {left}, all <= {data[p]}")
print(f"    right of the pivot: {right}, all > {data[p]}")
assert all(v <= data[p] for v in left)
assert all(v > data[p] for v in right)
print("    both claims verified by assertion, exactly as the invariant said")
print("  That is the whole correctness argument for quicksort: the invariant")
print("  guarantees the pivot is in its final place, so each partition")
print("  shrinks the problem without moving anything twice.")
```

### Block 7: a lower bound by counting

```python
import math
from math import factorial, log2


def merge_sort_worst(n):
    """Exact worst-case count n log2(n) - n + 1, for n a power of two."""
    return n * (n.bit_length() - 1) - n + 1


print("  LOWER BOUNDS: WHY NO COMPARISON SORT BEATS n LOG n.")
print()
print("  A comparison sort learns about its input only by asking")
print("  'is a[i] <= a[j]?', a question with two answers.  So its execution is")
print("  a binary decision tree, and it must distinguish all n! possible")
print("  orders: it needs at least n! leaves, and a binary tree with L leaves")
print("  has depth at least log2(L).")
print()
print("       n    log2(n!)   merge sort    gap   0.4427 * n")
for n in (8, 16, 32, 64, 128):
    merge_ops = merge_sort_worst(n)
    print(f"  {n:>4}   {log2(factorial(n)):>10.3f}   {merge_ops:>10}"
          f"   {merge_ops - log2(factorial(n)):>5.2f}   {0.4427 * n:>11.2f}")
print("  The gap column grows without bound and tracks the last one: it is")
print("  asymptotic to (log2(e) - 1) * n = 0.4427 * n comparisons.  That")
print("  0.44 n IS the entire remaining room for cleverness in sorting by")
print("  comparison, and nobody has found a way to spend it.")
print()
print("  Stirling's formula explains the numbers:")
print("    log2(n!) = n log2 n - n log2 e + 0.5 log2(2*pi*n) + O(1/n)")
print(f"  where n log2 e = {log2(math.e):.4f} * n.  At n = 128 the exact value")
n = 128
exact = log2(factorial(n))
stirling = n * log2(n) - n * log2(math.e) + 0.5 * log2(2 * math.pi * n)
print(f"  is {exact:.3f} bits and the formula gives {stirling:.3f}, a difference")
print(f"  of {abs(exact - stirling):.4f} bits.")
print("  The bound is not a technicality: it is about 7 bits per element at")
print("  n = 128, and it only gets worse as n grows.")


def counting_sort(a, k):
    """Sort values in 0..k-1 by counting: O(n + k) operations, no comparisons."""
    counts = [0] * k
    for value in a:
        counts[value] += 1
    out = []
    for value in range(k):
        out.extend([value] * counts[value])
    return out, len(a) + k


print()
print("  THE BOUND HAS A PRECONDITION.  Counting sort makes no comparisons, so")
print("  the lower bound does not apply to it at all.")
print()
print("        n   bins k   counting sort ops   n log2 n   merge sort ops")
for n, k in ((16, 16), (64, 64), (256, 16), (1024, 16)):
    data = [(i * 7919) % k for i in range(n)]
    ordered, ops = counting_sort(data, k)
    assert ordered == sorted(data)
    print(f"  {n:>7}   {k:>6}   {ops:>18}   {n * log2(n):>9.1f}   "
          f"{merge_sort_worst(n):>14}")
print()
print("  Sixteen buckets and 1024 values: counting sort does 1040 operations,")
print(f"  against merge sort's {merge_sort_worst(1024)}, and it never compares")
print("  two inputs, because it used the value RANGE as information the")
print("  problem handed it for free.  Sorting keys of 10**9 + 7 integers, or")
print("  32-bit words, or fixed-width strings, is this same idea, and it is")
print("  why a database sorts a million rows faster than any comparison sort.")
```

---

## Common Mistakes

**Mistake 1 — mislabelling the Master Theorem's three cases.**

```python
import math


def classify(a, b, c):
    """Which Master Theorem case does a*T(n/b) + Theta(n^c) fall in?"""
    d = math.log(a, b)
    if c < d:
        return f"c={c} < d={d:.4f}: Theta(n^{d:.4f}), leaves dominate"
    if c == d:
        return f"c={c} = d: Theta(n^{d:.4f} log n), every level costs the same"
    return f"c={c} > d={d:.4f}: Theta(n^{c}), the top of the tree dominates"


# a, b, c, and what the algorithm actually is
cases = [
    (2, 2, 1, "merge sort"),
    (2, 2, 0, "binary search"),
    (1, 2, 3, "a single scan"),
    (3, 2, 1, "Karatsuba multiply"),
    (4, 2, 2, "a 4-way split costing n^2"),
    (8, 2, 2, "a 8-way split costing n^2"),
    (2, 2, 2, "T(n) = 2T(n/2) + n^2"),
]
print(f"  {'a':>2} {'b':>2} {'c':>2}  {'verdict':<44} algorithm")
for a, b, c, name in cases:
    print(f"  {a:>2} {b:>2} {c:>2}  {classify(a, b, c):<44} {name}")
print()
print("  The two traps are in the last two rows: with a = 8 and c = 2,")
print("  d = 3 > 2 so the answer is Theta(n^3) -- WORSE than merge sort --")
print("  and with a = 2, c = 2 it is the balanced case Theta(n^2 log n).")
print("  Read d = log_b a first, every time, before deciding anything.")
```

Tempting because $c$ and $d$ are easy to swap and the two "easy" cases
($c < d$ and $c > d$) feel symmetric. They are not: they name opposite
things, and swapping them turns $\Theta(n^3)$ into $\Theta(n^2)$.

**Mistake 2 — using a guess with no slack in the substitution method.**

```python
import math


def step_ratio(c, d, k):
    """(3c(n/2)^d + n) / (c n^d) -- above 1 means the guess cannot hold."""
    n = 2 ** k
    return (3 * c * (n // 2) ** d + n) / (c * n ** d)


d = math.log2(3)
print("  Guess T(n) <= c * n^d, with no slack term:")
print("      c     k=4     k=8    verdict")
for c in (1, 3, 1e6):
    print(f"  {c:>7.0f}  {step_ratio(c, d, 4):>6.3f}  {step_ratio(c, d, 8):>6.3f}"
          f"    {'fails' if step_ratio(c, d, 8) > 1 else 'works'}")
print()
print("  Guess T(n) <= c * n^d - lambda * n, with lambda = 2 and c = 3:")
for k in (4, 8, 10):
    n = 2 ** k
    bound = 3 * n ** d - 2 * n
    print(f"    n = {n:>5}: bound {bound:>12.1f}, and T(n) = "
          f"{3 * 3 ** k - 2 * n:>7} -- difference "
          f"{3 * 3 ** k - 2 * n - bound:>6.3f}")
print()
print("  The slack is not a technical trick.  When the leaves exactly fill")
print("  the budget, there is nothing left to pay for the +n, and NO constant")
print("  can fix it: the slack term is the only place that slack can come")
print("  from.")
```

Tempting because "guess and check" feels like a numerical experiment, and the
code happily computes ratios. The failure is algebraic and the algebra is
the proof — but the intuition that "a bigger constant should absorb anything"
is exactly wrong when the recursive term saturates.

**Mistake 3 — applying greedy because the problem "looks like" interval
scheduling.**

```python
items = [(10, 60), (20, 100), (30, 120)]
capacity = 50

greedy = 0
left = capacity
for w, v in sorted(items, key=lambda iv: -iv[1] / iv[0]):
    if w <= left:
        greedy += v
        left -= w

best = 0
for mask in range(1 << len(items)):
    weight = sum(w for i, (w, _) in enumerate(items) if mask >> i & 1)
    if weight <= capacity:
        best = max(best, sum(v for i, (_, v) in enumerate(items)
                            if mask >> i & 1))
print(f"  capacity {capacity}, items {items}")
print(f"  greedy by value/weight: {greedy}")
print(f"  exhaustive optimum    : {best}")
print(f"  the greedy answer is {'optimal' if greedy == best else 'WRONG'}"
      f", by a factor of {best / greedy:.2f}")
print()
print("  Knapsack has no exchange argument: the exchange property needs a")
print("  swap that keeps feasibility, and here no swap exists.  The test is")
print("  not 'does it look greedy', it is 'can I write the swap down'.")
```

Tempting because greedy always wins on the problems students meet first, and
because "pick the best ratio" is the sort of rule that feels like it must
work. The counterexample is three items long.

**Mistake 4 — writing a DP solution that recomputes states.**

```python
from functools import lru_cache


def naive_lcs(x, y, i=0, j=0):
    if i == len(x) or j == len(y):
        return 0
    if x[i] == y[j]:
        return 1 + naive_lcs(x, y, i + 1, j + 1)
    return max(naive_lcs(x, y, i + 1, j), naive_lcs(x, y, i, j + 1))


@lru_cache(maxsize=None)
def memo_lcs(x, y, i=0, j=0):
    if i == len(x) or j == len(y):
        return 0
    if x[i] == y[j]:
        return 1 + memo_lcs(x, y, i + 1, j + 1)
    return max(memo_lcs(x, y, i + 1, j), memo_lcs(x, y, i, j + 1))


x, y = "ABCBDAB", "BDCABA"
answer = naive_lcs(x, y)
print(f"  LCS length of {x} and {y} = {answer}")
print(f"    memoised states computed : {memo_lcs.cache_info().currsize}")
print(f"    states in the whole table: {(len(x) + 1) * (len(y) + 1)}")
print()
print("  The naive recursion costs Theta(C(m+n, m)), which is 2*C(13,7) - 1")
print("  = 3431 calls when nothing matches; this pair happens to match often")
print("  enough to bring it down.  With memoisation it is Theta(mn).")
print("  Memoisation is not an optimisation here, it is the difference")
print("  between a program that finishes and one that does not.")
```

Tempting because the recursive form is easier to write and looks correct on
short strings. The state $(i,j)$ appears in exponentially many branches; only
the table or the cache collapses that.

**Mistake 5 — quoting $\Omega(n \log n)$ as if it were a bound on all
sorting.**

```python
print("  Comparison sort, n = 1024: the lower bound is")
print(f"    log2(1024!) = {__import__('math').log2(__import__('math').factorial(1024)):.1f}"
      f" comparisons")
print("  Counting sort on 1024 values in 16 bins:")
print(f"    1024 + 16 = {1024 + 16} operations, and it beats the bound")
print()
print("  The lower bound says: no algorithm whose ONLY question is")
print("  'is a[i] <= a[j]?' can sort faster.  Counting sort never asks that")
print("  question -- it asks 'what is the index of this value?', which the")
print("  problem hands it for free because the keys are in a known range.")
print("  A lower bound without a stated model is not a result, it is a")
print("  slogan.")
```

Tempting because "sorting requires $n \log n$ comparisons" is repeated so
often that the model restriction drops out. State the model or the bound is
about nothing.

---

## Formula Sheet

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| recurrence | `$T(n)=\sum_i a_iT(n/b_i)+\Theta(n^c)$` | $a_i$ subproblems of size $n/b_i$, plus $n^c$ local work | analysing any recursive algorithm |
| well-founded recurrence | repeated substitution reaches a base case | it describes a terminating program | before solving, not after |
| Master Theorem | `$T(n)=a\,T(n/b)+\Theta(n^c)$`, `$d=\log_ba$ | split into `$a$` parts of size `$n/b$` | merge sort, binary search, Karatsuba, FFT |
| case `$c<d$` | `$T(n)=\Theta(n^d)$` | leaves dominate | Karatsuba: `$3T(n/2)+n$` `$\Rightarrow\Theta(n^{1.5850})$` |
| case `$c=d$` | `$T(n)=\Theta(n^d\log n)$` | every level costs the same | `$2T(n/2)+n$` `$\Rightarrow\Theta(n\log n)$` |
| case `$c>d$` | `$T(n)=\Theta(n^c)$` | the top of the tree dominates | quicksort's balanced case |
| exact solution here | `$T(2^k)=3^{k+1}-2^{k+1}$` | closed form for `$3T(n/2)+n$` | `175099` at `$n=1024$` |
| substitution step | `$c\,n^d\ge a\,c(n/b)^d+n$` | check the guess survives one level | the step that fails without slack |
| slack guess | `$T(n)\le c\,n^d-\lambda n$ |r-1|\ge2$, `$c\ge\lambda+1$ | | leaves the room the additive term needs | worked at `$\lambda=2$`, `$c=3$` |
| level cost | `$n(3/2)^i$ at level $i$ | geometric series, ratio `a/b` | the recursion tree method |
| merge sort comparisons | `$\le n\log_2 n-n+1$`, `$\ge n\log_2 n/2$` | exact at `$n=2^k$ | the tightness of divide and conquer | `45057` worst at `$n=4096$` |
| Karatsuba | `$T(n)=3T(n/2)+\Theta(n)$ | three half-size products instead of four | | `$3^{16}=43046721$` leaves at 65536 digits |
| invariant template | `init /\ I\wedge g \Rightarrow I' /\ I\wedge\neg g \Rightarrow$ post | three obligations per loop | every correctness proof with a loop |
| termination variant | `$V$ strictly decreases, `$V\ge0$` | proves the loop ends | e.g. `$V=|hi-lo|+1$` in binary search |
| exchange argument | `$O'=(O\setminus\{o\})\cup\{g\}$ optimal and containing `$g$` | one swap repairs the disagreement | activity selection, Huffman, MST |
| matroid | hereditary + `$|A|<|B|\Rightarrow\exists x\in B\setminus A$ | exchange property | why "sort and take" is right on MST, matching |
| optimal substructure | `OPT(i) = combine(OPT(j), OPT(k))` | the optimum is built from smaller optima | prerequisite for DP |
| overlapping subproblems | the same state recurs in many branches | e.g. `$fib(n-1)$` appears twice | prerequisite for memoisation |
| DP cost | `$\#\text{states}\times$` work per state | table fill | LCS `$O(mn)$`, knapsack `$O(nC)$` |
| LCS recurrence | `$L(i,j)=L(i-1,j-1)+1$ if equal else `$\max(L(i-1,j),L(i,j-1))$` | match diagonally or skip | sequence alignment, `git diff` |
| knapsack recurrence | `$OPT(i,c)=\max(OPT(i-1,c),v_i+OPT(i-1,c-w_i))$` | skip or take item $i$ | capacity-constrained problems |
| subset states | `$C(n,k)$ not `$2^n$ |` | the state is a subset of fixed size | bitmask DP; `C(20,3)=1140` |
| Bellman-Ford | `$V-1$ relaxation passes suffice | | one pass per edge of a path | graphs with negative edges |
| negative cycle test | `$V$-th pass still relaxes `$\Rightarrow$` negative cycle | | edges `X->Y->Z->X` weight `-1` | detection |
| DAG shortest path | topological order, `$O(V+E)$ | | one pass settles everything | `P->Q->R->S = 2+1-3 = 0` |
| Dijkstra | correct iff no negative edge | settles each vertex once | `T=4` instead of `-4` in Block 5 |
| comparison lower bound | `$\log_2 n!$ | = `\Theta(n\log n)$` | binary questions distinguish `$n!$` orderings | sorting |
| Stirling | `$\log_2 n!=n\log_2 n-n\log_2 e+\tfrac12\log_2(2\pi n)+O(1/n)$` | the exact shape of the bound | `716.162` bits at `$n=128$ |
| merge sort gap | `$(\log_2 e-1)n\approx0.4427n$ |` | room left in comparison sorting | `52.84` at `$n=128$` |
| counting sort | `$\Theta(n+k)$ operations, `0$ comparisons | | uses the key range | `1040` vs `9217` at `$n=1024$` |

---

## Multiple Choice Questions

**Q1.** For $T(n) = 3T(n/2) + \Theta(n)$, what does the Master Theorem say?

- A) $T(n) = \Theta(n^{1.5})$, since $3/2 = 1.5$
- B) $T(n) = \Theta(n^{2})$, since squaring is the largest term that appears
- C) $T(n) = \Theta(n^{\log_2 3}) = \Theta(n^{1.5850})$, since $c = 1 < d = \log_2 3$
- D) $T(n) = \Theta(n \log n)$, because there is an additive $\Theta(n)$ term

<details>
<summary>Answer and explanation</summary>

**C) $T(n) = \Theta(n^{\log_2 3}) = \Theta(n^{1.5850})$, since $c = 1 < d =
\log_2 3$.**

With $a = 3$, $b = 2$ we get $d = \log_2 3 \approx 1.58496$, and the additive
term is $\Theta(n^1)$, so $c = 1 < d$ and the leaves dominate. Block 1
confirms it by measurement: $T(64) = 2059$, and the closed form
$3^{k+1} - 2^{k+1}$ matches to the last digit at every power of two.

Option A mixes up the branching factor with the exponent: $a/b = 1.5$ is the
*ratio of consecutive level costs*, which decides how the geometric series
converges, not the exponent. Option B is the schoolbook multiplication bound,
which is what you get when the additive term is $\Theta(n^2)$ instead.
Option D is the balanced case $c = d$ — an additive $\Theta(n)$ only produces
the extra $\log n$ when the recursion is exactly balanced at $a = b = 2$.

</details>

**Q2.** Why does the guess $T(n) \le c\,n^d$ fail for $T(n) = 3T(n/2) + n$?

- A) Because the base case cannot be verified for any $c$
- B) Because $3c(n/2)^d = c\,n^d$ exactly, leaving no slack for the $+n$
- C) Because $c$ must be an integer and the algebra needs a real
- D) Because the Master Theorem does not apply to this recurrence

<details>
<summary>Answer and explanation</summary>

**B) Because $3c(n/2)^d = c\,n^d$ exactly, leaving no slack for the $+n$.**

Since $2^d = 3$, the recursive term consumes the entire budget $c\,n^d$, and
the induction step asks for $c\,n^d \ge c\,n^d + n$. Block 1 measures the
ratio at `1.6667`, `1.3333`, `1.0667`, `1.0007` for $c = 1, 2, 10, 1000$: it
approaches `1` as $c$ grows but never crosses it, which is the numerical
signature of a failure that no constant can fix. The repair is the slack
guess $c\,n^d - \lambda n$ with $\lambda = 2$, which is tight.

Option A is false — the base case is fine, it just does not rescue a broken
step. Option C is a non-issue; $c$ may be any positive real. Option D is
irrelevant: the Master Theorem is a shortcut for the *answer*, and the
substitution method is an independent proof that happens to expose where the
budget goes.

</details>

**Q3.** In the substitution proof, why does the guess $T(n) \le c\,n^{d} -
\lambda n$ succeed exactly when $\lambda \ge 2$?

- A) Because the leaves must not outnumber the internal nodes
- B) Because the induction step reduces to $\frac32\lambda - 1 \ge \lambda$, and the base case needs $c \ge \lambda + 1$
- C) Because $2^\lambda \le 3$ is required
- D) Because $\lambda$ must equal the additive exponent $c = 1$

<details>
<summary>Answer and explanation</summary>

**B) Because the induction step reduces to $\frac32\lambda - 1 \ge \lambda$,
and the base case needs $c \ge \lambda + 1$.**

Substituting the guess, $3(c(n/2)^d - \lambda n/2) + n = c\,n^d - (\frac32\lambda
- 1)n$, which is at most the guess $c\,n^d - \lambda n$ exactly when
$\frac32\lambda - 1 \ge \lambda$, i.e. $\lambda \ge 2$. The base case $n = 1$
needs $1 \le c - \lambda$, i.e. $c \ge \lambda + 1 = 3$ at the smallest
$\lambda$. Block 1 uses exactly $\lambda = 2$, $c = 3$ and gets equality at
every power of two.

Option A is a misstatement of the leaf argument — the number of leaves has
nothing to do with $\lambda$. Option C inverts a real relation
($2^{\log_2 3} = 3$ is where $d$ came from, and $\lambda = 2$ is a separate
coefficient). Option D confuses two different symbols: $\lambda$ is the slack
coefficient, $c$ is the additive exponent, and in this recurrence $c = 1$.

</details>

**Q4.** Greedy by value/weight fails on capacity 50 with items $(10,60)$,
$(20,100)$, $(30,120)$. What exactly went wrong?

- A) The greedy rule should sort by weight instead
- B) No exchange exists: dropping the densest item cannot free enough capacity for both other items
- C) Ties in the ratios made the choice arbitrary
- D) The greedy rule is correct but the instance is too small to matter

<details>
<summary>Answer and explanation</summary>

**B) No exchange exists: dropping the densest item cannot free enough capacity
for both other items.**

Greedy by density returns `160`; the optimum is `220` from items $(20,100)$
and $(30,120)$, which have ratios `5.0` and `4.0`. For the exchange argument
to work you need a swap that preserves feasibility *and* the objective. Here
dropping $(10,60)$ frees `10` units, which is not enough for the `30`-unit
item, so no repair exists — and that is exactly the statement that the
problem is not a matroid.

Option A is a worse rule, not a better one: sorting by weight would take the
20-unit item first and also fail to see the pair. Option C is false — the
ratios `6.0`, `5.0`, `4.0` are distinct. Option D is not a defect of greedy
algorithms; the failure appears at three items and scales.

</details>

**Q5.** What do the Bellman-Ford passes in Block 5 actually show?

- A) That distances improve monotonically toward the optimum
- B) That each pass propagates one more edge, so $V-1$ passes suffice for any edge ordering
- C) That Bellman-Ford finds shortest paths even with positive cycles
- D) That Dijkstra's answer is always an overestimate

<details>
<summary>Answer and explanation</summary>

**B) That each pass propagates one more edge, so $V-1$ passes suffice for any
edge ordering.**

After one full pass over the edge list, every path of length one edge is
accounted for; after $k$ passes, every path of at most $k$ edges. Block 5
prints four passes and the last three change nothing, which is the theorem in
code: a shortest path has at most $V - 1 = 4$ edges.

Option A is a weaker and slightly misleading reading: distances do improve
monotonically downward, but the reason it converges is the path-length bound.
Option C is false — a *positive* cycle is harmless, but Bellman-Ford's value
is that it also detects the negative kind. Option D is false as stated:
Dijkstra is wrong here by `8`, but it can also *under*estimate in other
graphs; the correct statement is that its settled vertices are never revisited.

</details>

**Q6.** Why is `log2(n!)` the right lower bound for comparison sorting?

- A) Because sorting $n$ items needs at least $n$ comparisons per item
- B) Because a binary question yields one bit, $n!$ orderings need distinguishing, and a binary tree with $L$ leaves has depth at least $\log_2 L$
- C) Because merge sort uses that many comparisons
- D) Because each comparison halves the sorted prefix

<details>
<summary>Answer and explanation</summary>

**B) Because a binary question yields one bit, $n!$ orderings need
distinguishing, and a binary tree with $L$ leaves has depth at least
$\log_2 L$.**

This is pure counting, and it does not depend on the algorithm. At $n = 128$
it demands `716.162` bits, and merge sort spends `769` comparisons — a gap of
`52.84`, tracking the predicted `0.4427 * 128 = 56.67`.

Option A confuses the average with the total and has no counting argument
behind it. Option C is circular: merge sort is an *upper* bound of
$n\log_2 n - n + 1$, and using it to justify a lower bound proves nothing.
Option D is a plausible-sounding mechanism that is not what the decision tree
argument says; the tree's depth is set by the number of leaves, not by how
much of the prefix happens to be sorted.

</details>

**Q7.** Block 2 counts `45057` comparisons for merge sort on $4096$ elements.
What does that number tell you?

- A) That merge sort is $\Theta(n\log n)$ but with a specific tight count of $n\log_2 n - n + 1$
- B) That merge sort is $\Omega(n^2)$ on adversarial input
- C) That merge sort's best case is also $n\log_2 n - n + 1$
- D) That the adversarial arrangement was found by search

<details>
<summary>Answer and explanation</summary>

**A) That merge sort is $\Theta(n\log n)$ but with a specific tight count of
$n\log_2 n - n + 1$.**

At $n = 4096 = 2^{12}$ the bound is $4096 \times 12 - 4096 + 1 = 45057$,
which is what the `worst_case` construction produces by interleaving the two
halves at every merge. The same run reports `24576` comparisons for sorted
input — exactly $n\log_2 n / 2$ — so the worst case is about `1.83` times the
best case, a constant factor.

Option B is a misreading of a large constant: `45057` divided by
`4096 * 4096` is `0.0027`, nowhere near quadratic. Option C inverts the table —
sorted input is the *best* case here, `24576`. Option D is wrong: the
construction is a formula, not a search, which is why it is used in
textbooks.

</details>

**Q8.** A loop invariant is a statement that is true before the loop,
preserved by each iteration, and implies the postcondition when the guard
fails. Why must termination be proved separately?

- A) Because an invariant does not imply the loop ever ends
- B) Because invariants are only used for `while` loops
- C) Because termination is part of the postcondition
- D) Because a variant is easier to write than an invariant

<details>
<summary>Answer and explanation</summary>

**A) Because an invariant does not imply the loop ever ends.**

Partial correctness says "if it terminates, the answer is right". Termination
says "it terminates". Both are needed for total correctness, and they are
proved differently: the invariant by induction on the iteration count, the
termination by a variant that strictly decreases and is bounded below
(`|hi - lo| + 1` in binary search). Block 6 shows the invariant being *checked*
by assertions at every step, which is a machine-checkable form of the same
argument.

Option B is false — invariants apply to `for` loops too, and Python's `for` is
where students most often forget to state one. Option C is a reasonable
description of the goal but does not explain why a separate proof is needed:
termination is about reaching the postcondition, not about it. Option D
inverts the usual relationship; the variant is usually the *easier* argument
and the invariant is the work.

</details>

**Q9.** Which problem does the exchange argument fail on, and what is the
structural reason?

- A) Activity selection, because earliest finish does not maximise the count
- B) 0/1 knapsack, because the feasible sets are not a matroid: there is an $A \subset B$ with $|A| < |B|$ such that no $x \in B \setminus A$ keeps $A \cup \{x\}$ feasible
- C) Minimum spanning trees, because Kruskal's algorithm is not greedy
- D) Huffman coding, because code lengths are not linear

<details>
<summary>Answer and explanation</summary>

**B) 0/1 knapsack, because the feasible sets are not a matroid.**

In the instance $(10,60), (20,100), (30,120)$ with capacity `50`, take
$A = \{(20,100)\}$ (weight `20`) and $B = \{(20,100), (30,120)\}$ (weight
`50`). Then $|A| < |B|$ but adding either element of $B \setminus A$ to $A$
exceeds the capacity — so $B$ is not reachable from $A$ by one exchange, and
greedy has no local move that leads to the optimum. That failure *is* the
definition of not being a matroid.

Option A is false: greedy activity selection is optimal, and Block 3 verifies
it against brute force over all $128` subsets. Option C is false: Kruskal's
algorithm is greedy and the graphic matroid is the reason it works. Option D
is false: Huffman code lengths are $\ell$ for Huffman codes, which is the
deepest possible optimality statement for prefix codes.

</details>

**Q10.** Counting sort sorts 1024 values in 16 bins using `1040`
operations, beating the `9217` comparisons of merge sort. How is this not a
contradiction of $\Omega(n\log n)$?

- A) Because the constants in $\Omega$ are allowed to be large
- B) Because the lower bound is on the number of *comparisons* in a model where comparisons are the only allowed question, and counting sort asks a different question
- C) Because `1040` is really `1040 log 1040` operations
- D) Because merge sort is not $O(n \log n)$

<details>
<summary>Answer and explanation</summary>

**B) Because the lower bound is on the number of comparisons in a model where
comparisons are the only allowed question, and counting sort asks a different
question.**

Counting sort computes, for each of the `16` possible values, how many inputs
equal it. That is arithmetic on the keys, not a comparison, so the decision
tree argument simply does not apply. The bound is a statement *about a model*,
which is why every correct statement of it names the model.

Option A misuses the notation: the constant in $\Omega$ multiplies a growing
function, and no constant makes `1040 > 9217` for large $n`. Option C is
arithmetic nonsense. Option D contradicts
[Lesson 80](80_big_o_and_complexity.md) and Block 2's measurements: merge sort
uses `45057` comparisons at $n = 4096$, which is $n \log_2 n - n + 1$ exactly.

</details>

---

## Subjective Questions

### Short Answer

**Q1. State the three cases of the Master Theorem for
$T(n) = a\,T(n/b) + \Theta(n^c)$.**

<details>
<summary>Answer</summary>

With $a \ge 1$, $b > 1$ and $d = \log_b a$: if $c < d$ then
$T(n) = \Theta(n^d)$; if $c = d$ then $T(n) = \Theta(n^d \log n)$; if
$c > d$ then $T(n) = \Theta(n^c)$. The three cases are named for what
dominates — leaves, everything equally, or the top of the recursion tree. The
condition $c$ must be exactly $\Theta(n^c)$ matters: a $\log$ factor in the
additive term does not fit and needs Akra–Bazzi.

</details>

**Q2. What three obligations does a loop-invariant proof discharge?**

<details>
<summary>Answer</summary>

Initialisation: the invariant holds before the first iteration. Maintenance:
if the invariant holds and the guard holds at step $k$, then it holds at step
$k+1$. Conclusion (or exit): if the invariant holds and the guard fails, the
postcondition follows. These are the three parts of induction on the
iteration count. Termination is a separate obligation, discharged by a
variant that strictly decreases and is bounded below.

</details>

**Q3. Give the optimal-substructure and overlapping-subproblems conditions for
dynamic programming, and one problem that satisfies each alone.**

<details>
<summary>Answer</summary>

Optimal substructure: an optimal solution is built from optimal solutions of
smaller subproblems. Longest path satisfies it. Overlapping subproblems: the
same subproblem is solved again in different branches. Naive Fibonacci
satisfies it (each $F(n-1)$ is recomputed). Both together are what makes DP
worth writing: optimal substructure means the recurrence is *correct*,
overlapping subproblems means evaluating it recursively is *exponential*.

</details>

**Q4. State the exchange argument, and say what has to be checked.**

<details>
<summary>Answer</summary>

If for every optimal solution $O$ there is an optimal solution $O'$ containing
the greedy choice, then greedy is optimal. To prove it you check two things
for the swap $O' = (O \setminus \{o\}) \cup \{g\}$: that $O'$ is still
feasible (no new violation) and that its objective value did not get worse.
On the 0/1 knapsack instance neither check passes, which is precisely why
greedy fails there.

</details>

**Q5. Why does Dijkstra's algorithm require non-negative edge weights, in one
sentence?**

<details>
<summary>Answer</summary>

Because its correctness rests on the claim that once the closest unsettled
vertex is settled its distance can never improve, and that claim is false when
a later path can arrive along a negative edge — as Block 5 shows, where `T` is
settled at `4` and the real answer is `-4` through a vertex not yet reached.

</details>

**Q6. Give the information-theoretic lower bound for comparison sorting and
the best known comparison sort, and compute the asymptotic gap.**

<details>
<summary>Answer</summary>

The lower bound is $\log_2 n! = n\log_2 n - n\log_2 e +
\frac12\log_2(2\pi n) + O(1/n) = \Theta(n\log n)$ bits, because a binary
comparison yields one bit and $n!$ orderings must be distinguished. Merge sort
uses $n\log_2 n - n + 1$ comparisons. The gap between them is
$(\log_2 e - 1)n + O(\log n) \approx 0.4427n$ comparisons: `52.84` at
$n = 128$ and `447.99` at $n = 1024$, against predictions of `56.67` and
`453.30`.

</details>

### Long Answer

**Q1. Why does the pure-power substitution guess fail for
$T(n) = 3T(n/2) + n$, and what does the repair teach about the Master
Theorem?**

<details>
<summary>Model answer</summary>

Because $2^{\log_2 3} = 3$ exactly, the recursive term consumes the entire
budget: $3c(n/2)^d = c\,n^d$, so the induction step demands
$c\,n^d \ge c\,n^d + n$. No constant helps. Block 1 measures the ratio of the
right-hand side to the left as `1.6667`, `1.3333`, `1.0667`, `1.0007` for
$c = 1, 2, 10, 1000$: it approaches 1 from above and never reaches it, which
is the numeric signature of an impossible step.

The repair is to guess $c\,n^d - \lambda n$. The step then becomes
$c\,n^d - (\frac32\lambda - 1)n \le c\,n^d - \lambda n$, needing
$\lambda \ge 2$, and the base case needs $c \ge 3$. With those values the
bound is *exact*: the difference is `0.000000` at every power of two up to
1024, and the closed form is $T(2^k) = 3^{k+1} - 2^{k+1}$.

What this teaches about the Master Theorem is the meaning of its condition
$c < d$. In the recursion tree, the internal work per level forms a geometric
series with ratio $a/b$, and the leaves number $n^d$. When $c < d$ the leaves
are a larger power of $n$ than any level, so leaves dominate — which is
exactly the situation where the slack term $-\lambda n$ exists to absorb the
per-level work. When $c = d$ every level costs the same, so the additive term
contributes on $\log_b n$ levels and the extra $\log n$ appears. The failure
of the naive guess is not a defect of the method; it is the theorem's
hypothesis showing up as an algebraic obstruction.

</details>

**Q2. A team wants to route packets with minimum total cost over a network
with negative edge weights (a rebate for traffic). Give the algorithm, prove
it correct, and say what would break if you used Dijkstra.**

<details>
<summary>Model answer</summary>

Use Bellman-Ford, at $O(VE)$, or a topological pass if the graph is a DAG
($O(V+E)$). Correctness: after $k$ passes, every path of at most $k$ edges
has been accounted for, because a pass relaxes every edge once in some fixed
order and any path of $k$ edges is traversed by pass $k$ regardless of the
order the edges are listed in. Since a shortest path visits no vertex twice
when there is no negative cycle, it has at most $V-1$ edges, so after $V-1$
passes every distance is final. If a $V$-th pass still relaxes something, a
negative cycle is reachable and distances are unbounded below; Block 5 shows
exactly this, with $X$'s distance walking $-1, -2, -3, -4$ over four passes
along the cycle of weight $-1$.

What breaks with Dijkstra is not accuracy by a little but by a lot. Block 5's
graph has no ties: it settles $S(0)$, $A(1)$, $B(3)$, $T(4)$ and only then
$C(6)$. When $C$ is finally reached it offers $T$ a distance of $-4$, but the
standard implementation never reopens a settled vertex, so it reports `4`
instead of `-4`, wrong by `8`. The proof step that fails is "the unsettled
vertex with the smallest key has final distance", which requires every path
into it to arrive with a non-negative last edge: a negative edge can arrive
later and from further away, yet still win. Routing is exactly the domain
where this matters, since traffic engineering routinely creates rebates,
penalties and priority edges; the practical answer is Dijkstra with potentials
(Johnson's algorithm) or plain Bellman-Ford when the graph is a DAG.

</details>

**Q3. When should you write dynamic programming instead of a greedy
algorithm? Give a decision procedure and two examples on each side.**

<details>
<summary>Model answer</summary>

The decision procedure is: try to write the exchange argument. Take the
greedy choice $g$ and ask whether, for an arbitrary optimal solution $O$,
replacing $O$'s conflicting element by $g$ preserves both feasibility and the
objective value. If you can do that for one of the two cases ($g$ is in $O$
already, or $g$ replaces exactly one element), greedy is optimal and you write
it. If you find yourself enumerating cases, or if replacing one element
requires dropping two, stop.

Greedy works for activity selection (Block 3: replace the first interval, whose
finish is no earlier, and nothing downstream conflicts), for minimum spanning
trees (cut property: some minimum spanning tree contains the cheapest edge
across any cut), and for Huffman coding (the two least frequent symbols can be
siblings in some optimal tree, and swapping frequencies down a tree cannot
increase its weighted length). These are matroid problems — hereditary
feasibility plus exchange — and the matroid theorem guarantees that sorting by
weight and taking while feasible is optimal.

Dynamic programming wins where a choice consumes a resource that a later choice
also wants, so the local optimum blocks the global one. 0/1 knapsack is the
canonical case: capacity `50` with items $(10,60)$, $(20,100)$, $(30,120)$,
greedy by density returns `160` while the optimum is `220`, and no swap exists
because dropping the dense item frees only `10` units. Longest common
subsequence is the other: at each pair of prefixes you choose to match or skip,
and both sub-answers are needed, so the state is the pair $(i,j)$ and there
are $(m+1)(n+1)$ of them.

A useful sanity check is the size of the state space. If the number of
distinct states is polynomial in the input and the transitions between them are
cheap, DP is the answer; if it is exponential, DP will not save you and the
real question is whether the problem is `#P`-complete — which
[Lesson 28](../part02_discrete_combinatorics/28_counting_strategies.md) tells
you how to recognise.

</details>

**Q4. Every sorting algorithm you can think of is comparison based except
counting, radix and bucket sort. Why does the $\Omega(n \log n)$ lower bound
not stop us from sorting a billion integers in a second?**

<details>
<summary>Model answer</summary>

Because the bound is a statement about a *model*, and the model is the whole
point. The argument is a counting argument: a comparison sort's only
information-gathering move is a two-valued question, its execution tree needs
at least $n!$ leaves to separate all possible orders, and a binary tree of
that size has depth at least $\log_2 n! = \Theta(n\log n)$ bits. Remove the
comparison and every step of the argument fails at once — there is no tree,
no leaves, no counting of information.

Counting sort instead uses the arithmetic of the keys. With values in
$0..k-1$ it makes one pass to count and one to emit, $\Theta(n+k)$ operations.
Block 7 measures `1040` operations for 1024 values in 16 bins against merge
sort's `9217`, and the gap widens with $n$ because merge sort's cost grows
like $n\log n$ while this stays linear. Radix sort generalises it to
fixed-width strings by sorting on one digit at a time, $d$ passes of
$\Theta(n+k)$; bucket sort generalises it to continuous keys with a known
distribution.

The price is the assumption: the keys must live in a small, known range
(counting), be of bounded width (radix), or be spread predictably (bucket).
The moment you sort arbitrary-precision integers, arbitrary-length strings or
arbitrary real numbers, you are back in the comparison model and
$\Omega(n\log n)$ is waiting for you. This is why a database sorts an indexed
integer column in linear time and a `TEXT` column with a comparison sort, and
why the honest statement of any lower bound must name the class of algorithms
it quantifies over.

</details>

---

## Exercises and Solutions

**[ ] Exercise 1 —** Solve each recurrence by the Master Theorem, saying which
case applies and why: (a) $T(n) = 2T(n/2) + \Theta(n)$; (b) $T(n) = 7T(n/2) +
\Theta(n)$; (c) $T(n) = 4T(n/2) + \Theta(n^2)$; (d) $T(n) = T(n/3) +
\Theta(n \log n)$ — and say what happens to (d).

<details>
<summary>Solution</summary>

(a) $a = b = 2$ gives $d = 1$, and $c = 1$, so $c = d$ and
$T(n) = \Theta(n \log n)$. This is merge sort; Block 2's exact count
$n\log_2 n - n + 1$ confirms the shape.

(b) $d = \log_2 7 \approx 2.807$ and $c = 1 < d$, so
$T(n) = \Theta(n^{2.8074})$ — a 7-way split of a linear-cost problem. The
Master Theorem works fine; the algorithm is just a bad idea.

(c) $d = \log_2 4 = 2 = c$, so $T(n) = \Theta(n^2 \log n)$. This is the
counterintuitive case: doubling the branching factor *doubled* the answer,
because the merge cost grew just as fast as the branching.

(d) $a = 1$, $b = 3$, $d = \log_3 1 = 0$, and the additive term is
$\Theta(n \log n)$, which is **not** of the form $\Theta(n^c)$ for any $c$.
The Master Theorem does not apply. Two correct routes: $T(n) = T(n/3) +
\Theta(n\log n)$ expands to $T(n) = \Theta(n\log n)$ because the per-level
work doubles while the sizes shrink by 3, so the last few levels dominate and
the total is $\Theta(n\log n)$; or apply Akra–Bazzi, which gives
$\Theta(n^1(1 + \int_1^n \frac{u\log u}{u}du)) = \Theta(n(\log n)^2)$.

</details>

**[ ] Exercise 2 —** For the recurrence $T(n) = 2T(n/3) + \Theta(n)$: (a) apply
the Master Theorem; (b) write the recursion-tree level costs and sum the
geometric series; (c) prove $T(n) = \Theta(n^{\log_3 2})$ by substitution,
including the base case.

<details>
<summary>Solution</summary>

(a) $a = 2$, $b = 3$, $d = \log_3 2 \approx 0.6309$; the additive term is
$\Theta(n^1)$ with $c = 1 > d$, so $T(n) = \Theta(n^1) = \Theta(n)$.

(b) Level $i$ has $2^i$ nodes of size $n/3^i$, each doing $n/3^i$ work, so
level $i$ costs $2^i n/3^i = n(2/3)^i$ — a *decreasing* geometric series with
ratio $2/3 < 1$, summing to at most $3n$. The leaves number $2^{\log_3 n} =
n^{0.6309}$. Total $\le 3n + n^{0.6309} = O(n)$, and $\Omega(n)$ comes from the
top level, so $T(n) = \Theta(n)$.

(c) Guess $T(n) \le c\,n$. The step: $2c(n/3) + n = \frac{2c}{3}n + n \le c\,n$
iff $1 \le c/3$, i.e. $c \ge 3$. The base case $n = 1$ needs $T(1) \le c$, so
$c \ge 3$ works there too. Hence $T(n) = \Theta(n)$, and it is *tight* here —
unlike Example 1, the pure power guess succeeds because the recursion shrinks
faster than it branches.

</details>

**[ ] Exercise 3 —** Activity selection: (a) give the greedy algorithm and its
exchange proof; (b) give a set of intervals where *latest* start time greedy
fails while earliest finish succeeds; (c) for the interval set
$\{(1,4),(3,5),(5,7),(6,8),(2,6)\}$, compute both greedies and the true optimum.

<details>
<summary>Solution</summary>

(a) Sort by finishing time, take each interval whose start is at or after the
end of the last one. The exchange: $g$ ends no later than $O$'s first
interval $o$, so replacing $o$ by $g$ keeps the count and cannot conflict with
anything that followed $o$.

(b) Latest-start greedy fails on $\{(1,3),(2,4),(3,5),(4,6)\}$. Latest start
takes $(4,6)$ and then nothing fits, giving 1. Earliest finish takes
$(1,3)$ and then $(3,5)$, giving 2 — and 2 is optimal, because no three of
these four intervals are mutually non-overlapping.

(c) Sorted by finish: $(1,4)$ take, $(2,6)$ skip, $(3,5)$ skip, $(5,7)$ take,
$(6,8)$ skip — earliest finish gets 2. Sorted by latest start: $(6,8)$ take,
then nothing fits — 1. The optimum is 2, e.g. $\{(1,4),(5,7)\}$, so earliest
finish is optimal here and latest start is not.

</details>

**[ ] Exercise 4 —** Knapsack: (a) write the DP recurrence and its state count
for $n$ items and capacity $C$; (b) explain why the greedy-by-ratio answer can
be arbitrarily bad by constructing a family; (c) decide whether *fractional*
knapsack is still greedy-solvable, and prove it.

<details>
<summary>Solution</summary>

(a) $\mathrm{OPT}(i,c) = \max(\mathrm{OPT}(i-1,c),\ v_i + \mathrm{OPT}(i-1,
c - w_i))$ with $\mathrm{OPT}(0,c) = 0$; there are $(n+1)(C+1)$ states, so
$O(nC)$ time and, with rolling rows, $O(C)$ space.

(b) Here is a family with an unbounded gap. Fix $w \ge 3$ and set capacity
$C = 2w$. Take one item $A = (w+1,\ 2w+2)$, of ratio exactly 2, and $k \ge 2$
items of weight $w$ and value $2w-1$, of ratio $2 - 1/w < 2$. Greedy by ratio
takes $A$ first, leaving $w - 1$ units — not enough for any of the others —
and returns $2w + 2$. The optimum takes two of the others for $4w - 2$. The
gap is $2w - 4$, so the loss grows without bound as $w$ grows.

(c) Fractional knapsack *is* greedy: sort by ratio and fill until capacity is
exhausted. The exchange argument works because swapping a fraction of a
lower-ratio item for a fraction of a higher-ratio one keeps the total weight and
increases the value, and feasibility is about weight only. That is the whole
difference: fractional feasibility is closed under any repartition of weight,
which is the matroid-like exchange the 0/1 version lacks.

</details>

**[ ] Exercise 5 —** (a) State and prove the LCS recurrence. (b) Give the state
count and time for strings of lengths $m$ and $n$, and for $n$ DNA sequences
of length $L$. (c) Explain why the naive two-branch recursion is
$\Theta(\varphi^{m+n})$.

<details>
<summary>Solution</summary>

(a) If $x_{i-1} = y_{j-1}$ then $L(i,j) = L(i-1,j-1) + 1$: a longest common
subsequence can be chosen to end in that matched pair, and any longer one
would give a longer common subsequence of the shorter prefixes. Otherwise the
last elements cannot both be used, so $L(i,j) = \max(L(i-1,j), L(i,j-1))$.
Base cases $L(0,j) = L(i,0) = 0$.

(b) $(m+1)(n+1)$ states, $O(1)$ work each, so $O(mn)$ time and $O(mn)$ space,
or $O(\min(m,n))$ space with rolling rows. For $n$ sequences of length $L$
with one merged state it is $O(nL)$; the $k$-way LCS state is a tuple of $k$
positions, $O(L^k)$ states — the same exponential trap as naive Fibonacci.

(c) The recursion satisfies $T(i,j) = T(i-1,j) + T(i,j-1)$ whenever the
characters differ, with $T(0,j) = T(i,0) = 1$, so by Pascal's identity the
number of calls is exactly $2\binom{m+n}{m} - 1$ in the worst case — `1847`
calls for two strings of length 6 sharing no characters, and
$\Theta\left(4^L/\sqrt{\pi L}\right)$ when $m = n = L$. Matching characters
make it cheaper: `ABCBDAB` against `BDCABA` needs only `152` calls because
each match collapses a branch. Memoisation caps it at the
$(m+1)(n+1) = 56` states Block 4 fills.

</details>

**[ ] Exercise 6 —** (a) Give a decision tree proving $\Omega(n\log n)$ for
comparison sorting. (b) Compute the gap between merge sort's worst case and
$\log_2 n!$ at $n = 1024$ and show it is asymptotic to $0.4427n$. (c) Explain
why insertion sort on nearly sorted input is faster, and what that says about
the model.

<details>
<summary>Solution</summary>

(a) Each comparison has two outcomes, so the execution of a comparison sort on
$n$ distinct keys is a binary tree; two inputs that lead to the same leaf are
indistinguishable to the algorithm and must produce the same output, so each
leaf covers at most one of the $n!$ orders; a tree with at least $n!$ leaves
has depth at least $\lceil\log_2 n!\rceil = \Omega(n\log n)$.

(b) At $n = 1024$: merge sort's worst case is $1024 \times 10 - 1024 + 1 =
9217$ comparisons and $\log_2(1024!) = 8769.006$ bits, a gap of `447.99`. The
asymptotic form is $(n\log_2 n - n + 1) - (n\log_2 n - n\log_2 e +
\frac12\log_2(2\pi n)) = (\log_2 e - 1)n + 1 - \frac12\log_2(2\pi n) \approx
0.4427n$; at $n = 1024$ that predicts `453.30`, and the `5.3` discrepancy is
the $\frac12\log_2(2\pi n)$ correction term, which is `6.5` at this size.

(c) Insertion sort is a comparison sort, so $\Omega(n\log n)$ still applies to
it in the worst case; it is faster on nearly sorted data because its
recurrence's constant depends on the number of inversions, $\Theta(n + I)$. The
point is that the lower bound constrains the worst case of a model, and a
model parameter — here the input order — can be as important as $n$. That is
also why Timsort is legal: it is still a comparison sort, but it detects runs
and merges them proportionally, so its *worst case over adversarial inputs*
remains $O(n\log n)$ while its typical case is far better.

</details>

**Challenge.**

**[ ]** *Prove the whole chain.* (a) Show that the Master Theorem's case $c =
d$ is exactly the regime where the recursion-tree level sums and the leaf
count are the same order. (b) Show that the pure-power substitution guess
succeeds iff $c \ne d$, and give the slack term when it fails. (c) Using your
answers, predict which of $T(n) = 8T(n/2) + \Theta(n)$ and
$T(n) = 8T(n/2) + \Theta(n^2)$ is faster for large $n$, and explain why the
intuition is wrong. (d) Extend: what happens to $T(n) = 2T(n/2) + \Theta(n
\log n)$, and which theorem from Lesson 80 handles it?

<details>
<summary>Solution</summary>

(a) Level $i$ of the tree holds $a^i$ nodes of size $n/b^i$, and each does
$(n/b^i)^c$ work, so level $i$ costs $n^c\left(a/b^c\right)^i$. The level costs
therefore form a geometric series with ratio $a/b^c$. If $a/b^c > 1$ the last
level dominates and, since $k = \log_b n$ levels, the sum is $\Theta(n^d)$;
if $a/b^c < 1$ the series converges to $\Theta(n^c)$; and if $a/b^c = 1$ —
equivalently $a = b^c$, equivalently $c = d$ — every single level costs
$\Theta(n^c) = \Theta(n^d)$, so multiplying by the $\log_b n$ levels produces
the extra $\log n$. The three Master Theorem cases are exactly the three
behaviours of that ratio.

(b) Since $d = \log_b a$, we have $b^d = a$ *exactly*, so the recursive term
is $a\,c'n^d/b^d = c'n^d$ for every constant $c'$. The pure guess
$T(n) \le c'n^d$ therefore never has room for the additive term, in any case
— which is Example 1 in its most general form. The guess $c'n^c$ does work,
but only when $c > d$: it reduces to $c'(a/b^c) + 1 \le c'$, which has a
solution exactly when $a/b^c < 1$. So a pure-power guess succeeds precisely
when the local work dominates, and when it does not you need either the slack
form of Example 1 or the Master Theorem.

(c) $8T(n/2) + \Theta(n)$: $d = \log_2 8 = 3 > c = 1$, so $T(n) = \Theta(n^3)$.
$8T(n/2) + \Theta(n^2)$: $d = 3 > c = 2$, so again $T(n) = \Theta(n^3)$. They
are the *same* order, and the intuition — "more work per node should be
slower" — fails because in both cases the leaves dominate: there are $8^k = n^3$
leaves either way, and no amount of local work below $n^3$ catches up. To see
a difference you must raise the local cost past $n^3$, for example
$8T(n/2) + \Theta(n^{3.5})$.

(d) $T(n) = 2T(n/2) + \Theta(n\log n)$ has $d = 1$ and an additive term that
is not $\Theta(n^c)$ for any single $c$, so the Master Theorem does not apply —
this is the FFT recurrence. Akra–Bazzi gives
$\Theta\left(n^{1}\left(1 + \int_1^n \frac{u\log u}{u^2}du\right)\right) =
\Theta(n\log n)$, which is exactly what the FFT achieves.

</details>

---

## Summary

- Every recursive algorithm gives a recurrence; the three tools for solving it
  are the recursion tree (shape), substitution (constant) and the Master
  Theorem (class), and they always agree.
- $T(n) = a\,T(n/b) + \Theta(n^c)$ with $d = \log_b a$: leaves dominate when
  $c < d$, every level ties when $c = d$, the top dominates when $c > d$.
- The pure guess $c\,n^d$ fails whenever the recursion saturates the budget —
  for $3T(n/2) + n$ it fails for *every* constant, and the repair is a slack
  term $- \lambda n$ with $\lambda = 2$.
- A greedy algorithm is optimal only if you can write the exchange argument;
  0/1 knapsack with capacity 50 returns `160` where the optimum is `220`, and
  that failure is exactly the absence of the matroid exchange property.
- Dynamic programming applies when a problem has optimal substructure *and*
  overlapping subproblems; the state count is the budget — `56` cells for a
  `7 × 6` LCS, `C(n,k)` for a subset state.
- Memoisation converts an exponential recursion into a linear table; the naive
  Fibonacci at `n = 28` makes `1028457` calls where the memoised version
  evaluates `29` states.
- Bellman-Ford needs `V-1` passes and one negative cycle is enough to break
  Dijkstra: Block 5's graph has Dijkstra reporting `4` where the truth is
  `-4`.
- A loop invariant has three obligations — initialisation, maintenance,
  conclusion — and termination is a separate proof via a decreasing variant.
- Lower bounds are statements about a model: `log2(n!)` bits lower-bounds
  comparison sorting, merge sort sits `0.4427n` above it, and counting sort
  escapes only by asking a question comparisons cannot ask.

---

## Next

[90 — Vectors in 3D and the Cross Product](../part07_geometry_graphics/90_vectors_3d_and_cross_product.md)
moves from the algebra of algorithms to the geometry of the data those
algorithms manipulate. The recurrence-solving and correctness-proof habits
carry over unchanged; the subject matter becomes directions, planes, and the
quantities that graphics and physics code compute every frame.