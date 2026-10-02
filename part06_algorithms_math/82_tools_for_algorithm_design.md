# 82 — Mathematical Tools for Algorithm Design

**Part**: part06_algorithms_math · **Prerequisites**: 24, 80 · **Time**: 45 min

---

## In Plain Words

This lesson is the toolbox you reach for once you know how to say how fast
something is. It has four parts: how to work out how long a recursive
algorithm takes by writing down an equation for its cost and solving it, and
how to prove an algorithm is correct rather than merely hopeful. Then the two
design patterns you will use for the rest of your career — taking the locally
best choice and hoping, or building a table of answers — together with the test
that tells you which one a problem wants. And finally how to prove that a
problem is hard on purpose, so you stop looking for something clever that does
not exist. Each tool is a way of turning a vague intuition into a statement
you can check, and the whole subject comes down to a handful of patterns that
reappear in every algorithm you will ever read.

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
[Lesson 24](../part02_discrete_combinatorics/24_recurrence_relations.md)'s: the
cost of a recursive function on $n$ is a sum of the costs of its recursive
calls plus its own work.

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
| slack guess | `$T(n)\le c\,n^d-\lambda n$`, needs `$\lambda\ge2$` and `$c\ge\lambda+1$` | leaves the room the additive term needs | worked at `$\lambda=2$`, `$c=3$` in Block 1 |
| level cost | `$n(3/2)^i$ at level $i$ | geometric series, ratio `a/b` | the recursion tree method |
| merge sort comparisons | `$\le n\log_2 n-n+1$`, `$\ge n\log_2 n/2$` | exact at `$n=2^k$` | the tightness of divide and conquer | `45057` worst at `$n=4096$` |
| Karatsuba | `$T(n)=3T(n/2)+\Theta(n)$` | three half-size products instead of four | `$3^{16}=43046721$` leaves at 65536 digits |
| invariant template | `init /\ I\wedge g \Rightarrow I' /\ I\wedge\neg g \Rightarrow$ post | three obligations per loop | every correctness proof with a loop |
| termination variant | `$V$ strictly decreases, `$V\ge0$` | proves the loop ends | the window length in binary search |
| exchange argument | `$O'=(O\setminus\{o\})\cup\{g\}$ optimal and containing `$g$` | one swap repairs the disagreement | activity selection, Huffman, MST |
| matroid | hereditary, and `$\lvert A\rvert<\lvert B\rvert` forces an `$x\in B\setminus A$` that keeps `$\lvert A\cup\{x\}\rvert$` feasible | the exchange property | why "sort and take" is right on MST, matching |
| optimal substructure | `OPT(i) = combine(OPT(j), OPT(k))` | the optimum is built from smaller optima | prerequisite for DP |
| overlapping subproblems | the same state recurs in many branches | e.g. `$fib(n-1)$` appears twice | prerequisite for memoisation |
| DP cost | `$\#\text{states}\times$` work per state | table fill | LCS `$O(mn)$`, knapsack `$O(nC)$` |
| LCS recurrence | `$L(i,j)=L(i-1,j-1)+1$ if equal else `$\max(L(i-1,j),L(i,j-1))$` | match diagonally or skip | sequence alignment, `git diff` |
| knapsack recurrence | `$OPT(i,c)=\max(OPT(i-1,c),v_i+OPT(i-1,c-w_i))$` | skip or take item $i$ | capacity-constrained problems |
| subset states | `$C(n,k)$ states, not `$2^n$` | the state is a subset of fixed size | bitmask DP; `C(20,3)=1140` |
| Bellman-Ford | `$V-1$ relaxation passes suffice | one pass per edge of a path | graphs with negative edges |
| negative cycle test | a `$V$-th pass still relaxes something | then a negative cycle is reachable | edges `X->Y->Z->X` of weight `-1` | detection |
| DAG shortest path | topological order, `$O(V+E)$` | one pass settles everything | `P->Q->R->S = 2+1-3 = 0` |
| Dijkstra | correct iff no negative edge | settles each vertex once | `T=4` instead of `-4` in Block 5 |
| comparison lower bound | `$\log_2 n!$` bits `=$\Theta(n\log n)$` | binary questions distinguish `$n!$` orderings | sorting |
| Stirling | `$\log_2 n!=n\log_2 n-n\log_2 e+\tfrac12\log_2(2\pi n)+O(1/n)$` | the exact shape of the bound | `716.162` bits at `$n=128$ |
| merge sort gap | `$(\log_2 e-1)n\approx0.4427n$` | room left in comparison sorting | `52.84` at `$n=128` |
| counting sort | `$\Theta(n+k)$` operations and `0` comparisons | uses the key range instead of comparing | `1040` vs `9217` at `$n=1024` |

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
print(f"  1.618^28 = {1.618 ** 28:.0f} -- while memoisation is linear in n.")
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

### With Libraries

```python
# Requires numpy + matplotlib; not runnable with the standard library alone.
import math

import matplotlib
matplotlib.use("Agg")          # so the script runs without a display
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(1, 3, figsize=(16.5, 4.6))


def level_cost(n, a, b, level):
    """Work at one level of the recursion tree for T(n) = a*T(n/b) + Theta(n)."""
    return a ** level * n / b ** level


# 1. Recursion trees for the Master's three cases, side by side.
levels = np.arange(0, 13)
n = 4096
for ax, (a, c, case) in zip(axes[:2], ((2, 0, "c < d: leaves dominate"),
                                        (2, 1, "c = d: every level equal"),
                                        (2, 2, "c > d: the top dominates"))):
    ax.bar(levels, level_cost(n, a, 2, levels), color="tab:blue", width=0.7,
           label=f"work at level i")
    ax.set_yscale("log")
    ax.set_xlabel("recursion level i")
    ax.set_ylabel("work at this level")
    ax.set_title(f"T(n) = {a}T(n/{2}) + n^{c}   ({case})")
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=8)

# 3. The comparison-sorting lower bound against what merge sort actually pays.
ns = 2 ** np.arange(2, 13)
lower = np.array([math.lgamma(int(n) + 1) / math.log(2) for n in ns])
merge = np.array([int(n) * (int(n).bit_length() - 1) - int(n) + 1 for n in ns])
axes[2].plot(ns, lower, lw=2, color="tab:red", label=r"lower bound  $\log_2 n!$")
axes[2].plot(ns, merge, lw=2, color="tab:blue", label="merge sort")
axes[2].fill_between(ns, lower, merge, color="tab:orange", alpha=0.35,
                     label="the gap nobody has closed")
axes[2].set_xscale("log", base=2)
axes[2].set_yscale("log")
axes[2].set_title("Sorting: the bound and the best we know")
axes[2].set_xlabel("n")
axes[2].set_ylabel("comparisons")
axes[2].legend(fontsize=8)
axes[2].grid(alpha=0.3, which="both")

plt.tight_layout()
plt.savefig("lesson82_tools.png", dpi=110)
print("wrote lesson82_tools.png")
print(f"  n = {ns[-1]}: log2(n!) = {lower[-1]:.1f} comparisons are unavoidable, "
      f"merge sort pays {merge[-1]}")
print(f"  the gap is {merge[-1] - lower[-1]:.1f}, tracking (log2(e) - 1) * n = "
      f"{0.4427 * ns[-1]:.1f}")
print("  -- it grows linearly, and that is the whole remaining room for")
print("  cleverness in comparison sorting.  The first two panels are why the")
print("  Master Theorem needs three cases rather than one: which of the two")
print("  geometric series dominates is decided by c against log_b(a), and the")
print("  picture changes shape at c = d.")
plt.close(fig)
```

Output:

```text
wrote lesson82_tools.png
  n = 4096: log2(n!) = 43250.0 comparisons are unavoidable, merge sort pays 45057
  the gap is 1807.0, tracking (log2(e) - 1) * n = 1813.3
  -- it grows linearly, and that is the whole remaining room for
  cleverness in comparison sorting.  The first two panels are why the
  Master Theorem needs three cases rather than one: which of the two
  geometric series dominates is decided by c against log_b(a), and the
  picture changes shape at c = d.
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

CALLS = 0


def naive_lcs(x, y, i=0, j=0):
    """Correct, and quadratic-exponential in the number of calls it makes."""
    global CALLS
    CALLS += 1
    if i == len(x) or j == len(y):
        return 0
    if x[i] == y[j]:
        return 1 + naive_lcs(x, y, i + 1, j + 1)
    return max(naive_lcs(x, y, i + 1, j), naive_lcs(x, y, i, j + 1))


@lru_cache(maxsize=None)
def memo_lcs(x, y, i=0, j=0):
    """The same function with one line added: the cache.  This is the whole DP."""
    if i == len(x) or j == len(y):
        return 0
    if x[i] == y[j]:
        return 1 + memo_lcs(x, y, i + 1, j + 1)
    return max(memo_lcs(x, y, i + 1, j), memo_lcs(x, y, i, j + 1))


x, y = "ABCBDAB", "BDCABA"
answer = naive_lcs(x, y)
naive_calls = CALLS
assert memo_lcs(x, y) == answer            # same answer, different cost
states = memo_lcs.cache_info().currsize
assert states < naive_calls
print(f"  LCS length of {x} and {y} = {answer}   (both versions agree)")
print(f"    plain recursion     : {naive_calls} calls to lcs()")
print(f"    memoised states     : {states} of the {(len(x) + 1) * (len(y) + 1)}"
      f" in the table")
print(f"    speed-up            : {naive_calls / states:.1f}x")
print()
print("  The naive version is Theta(C(m+n, m)) calls.  The recursion has at most")
print("  C(m+n, m) distinct diagonals through the (m+1)(n+1) grid, so when")
print("  nothing matches -- no diagonal ever takes the 'match and move' branch --")
print("  every one of them is walked: 2*C(13,7) - 1 = 3431 calls for two strings")
print("  of length 7.  This pair shares a lot of characters, which collapses the")
print("  count to 309, and the cache takes it to 38 states evaluated once each.")
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

**[ ] Exercise 1 —** Solve each recurrence $T(n) = a\,T(n/b) + \Theta(n^c)$ by the
Master Theorem, saying which case applies and why: (a) $T(n) = 2T(n/2) +
\Theta(n)$; (b) $T(n) = 7T(n/2) + \Theta(n)$; (c) $T(n) = 4T(n/2) +
\Theta(n^2)$; (d) $T(n) = T(n/3) + \Theta(n \log n)$ — and for (d) say what
happens to the Master Theorem and what replaces it.

<details>
<summary>Solution</summary>

(a) $a = b = 2$ gives $d = 1$ and $c = 1$, so $c = d$ and
$T(n) = \Theta(n \log n)$. This is merge sort; Block 2's exact count
$n\log_2 n - n + 1$ confirms the shape. **Case 2**, and it is the boundary
case: the level ratio $a/b^c = 2/2 = 1$, so no level dominates.

(b) $d = \log_2 7 \approx 2.8074$ and $c = 1 < d$, so $T(n) = \Theta(n^{2.8074})$
— a 7-way split of a linear-cost problem. **Case 1**: the leaves win. The
Master Theorem works fine; the algorithm is just a bad idea.

(c) $d = \log_2 4 = 2 = c$, so $T(n) = \Theta(n^2 \log n)$. **Case 2** again.
This is the counterintuitive one: doubling the branching factor *doubled*
the answer, because the merge cost grew just as fast as the branching.

(d) $a = 1$, so $d = \log_3 1 = 0$, and the additive term $\Theta(n \log n)$
is **not** of the form $\Theta(n^c)$ for any $c$. The Master Theorem does not
apply. Use Akra–Bazzi: solve $\sum_i a_i b_i^p = 1$, i.e. $(1/3)^p = 1$, giving
$p = 0$. Then

$$\Theta\left(n^0\left(1 + \int_1^n \frac{u \log u}{u^{p+1}}\,du\right)\right) = \Theta\left(1 + \int_1^n \log u\,du\right) = \Theta(n \log n).$$

The $n^0$ prefactor is the whole answer and it is easy to drop: writing
$\Theta(n(\log n)^2)$ instead is the correct answer to a *different*
recurrence, namely $2T(n/2) + \Theta(n \log n)$ — see Challenge (d). The
recursion tree confirms $\Theta(n\log n)$ and even pins the constant: level $i$
costs $(n/3^i)\log_2(n/3^i)$, so with $j = k - i$ for $n = 3^k$ the total is
$\log_2 3 \sum_{j=1}^{k} j\,3^j = \log_2 3 \cdot \tfrac34\,(1 + (2k-1)3^k)$,
which is a constant — $3/2$ — times $n\log_2 n$.

```python
"""Exercise 1 code block."""
import math
from math import log2

CASES = [
    ("(a)  T(n) = 2T(n/2) + Theta(n)",   2, 2, 1),
    ("(b)  T(n) = 7T(n/2) + Theta(n)",   7, 2, 1),
    ("(c)  T(n) = 4T(n/2) + Theta(n^2)", 4, 2, 2),
]

print("Solve T(n) = a T(n/b) + Theta(n^c) with the Master Theorem.")
print()
print(f"{'recurrence':<32} {'d = log_b a':>12} {'c':>3} {'case':>5} {'result':>20}")
for label, a, b, c in CASES:
    d = log2(a) / log2(b)
    if c < d:
        case, result = 1, f"Theta(n^{d:.4f})"
    elif abs(c - d) < 1e-12:
        case, result = 2, "Theta(n^d log n)"
    else:
        case, result = 3, f"Theta(n^{c})"
    print(f"{label:<32} {d:12.4f} {c:3d} {case:5d} {result:>20}")

print()
print("(d)  T(n) = T(n/3) + Theta(n log n):  a = 1, so d = log_3 1 = 0, and")
print("     n log n is not Theta(n^c) for any c.  Master Theorem: DOES NOT APPLY.")
print()
print("     Akra-Bazzi.  Solve  a_1 b_1^p = 1  ->  (1/3)^p = 1  ->  p = 0.")
print("         T(n) = Theta( n^p (1 + INT_1^n g(u)/u^(p+1) du ) )")
print("               = Theta( n^0 (1 + INT_1^n u log u / u^1 du ) )")
print("               = Theta( 1 + INT_1^n log u du )")
print("               = Theta( 1 + n log n - n + 1 )")
print("               = Theta(n log n)")
print()
print("     The n^0 prefactor is the whole answer.  Drop it and you get n log n")
print("     out of an integral that is only n log n in total -- i.e. n (log n)^2,")
print("     which is the answer to a DIFFERENT recurrence (Challenge (d)).")
print()
print("     Recursion tree check.  Level i has 1 node of size n/3^i doing")
print("     (n/3^i) log2(n/3^i) work, so with j = k - i the total is")
print("         SUM_{j=1..k} 3^j * j * log2(3) = log2(3) * (3/4)(1 + (2k-1)3^k).")
print()
print(f"       {'k':>3} {'n = 3^k':>10} {'tree total':>16} {'closed form':>16} {'n log2 n':>16} {'ratio':>8}")
for k in range(3, 15):
    n = 3 ** k
    total, size = 0.0, float(n)
    while size >= 1.0:
        total += size * math.log2(size) if size > 1 else 0.0
        size /= 3
    closed = math.log2(3) * 0.75 * (1 + (2 * k - 1) * 3 ** k)
    print(f"       {k:3d} {n:10d} {total:16.2f} {closed:16.2f} "
          f"{n*math.log2(n):16.2f} {total/(n*math.log2(n)):8.4f}")
print()
print("     The two total columns agree to the last digit, and the ratio tends")
print("     to 3/2 rather than 1.  The constant is not 1 because the work is")
print("     dominated by the LAST levels, not the first: the j-th-from-last")
print("     level does 3^(k-j) * j * log2(3) work, and the j series sums to 3/4,")
print("     which is what produces the factor 3/2 = (3/4) * 2.")
```

```text
Solve T(n) = a T(n/b) + Theta(n^c) with the Master Theorem.

recurrence                        d = log_b a   c  case               result
(a)  T(n) = 2T(n/2) + Theta(n)         1.0000   1     2     Theta(n^d log n)
(b)  T(n) = 7T(n/2) + Theta(n)         2.8074   1     1      Theta(n^2.8074)
(c)  T(n) = 4T(n/2) + Theta(n^2)       2.0000   2     2     Theta(n^d log n)

(d)  T(n) = T(n/3) + Theta(n log n):  a = 1, so d = log_3 1 = 0, and
     n log n is not Theta(n^c) for any c.  Master Theorem: DOES NOT APPLY.

     Akra-Bazzi.  Solve  a_1 b_1^p = 1  ->  (1/3)^p = 1  ->  p = 0.
         T(n) = Theta( n^p (1 + INT_1^n g(u)/u^(p+1) du ) )
               = Theta( n^0 (1 + INT_1^n u log u / u^1 du ) )
               = Theta( 1 + INT_1^n log u du )
               = Theta( 1 + n log n - n + 1 )
               = Theta(n log n)

     The n^0 prefactor is the whole answer.  Drop it and you get n log n
     out of an integral that is only n log n in total -- i.e. n (log n)^2,
     which is the answer to a DIFFERENT recurrence (Challenge (d)).

     Recursion tree check.  Level i has 1 node of size n/3^i doing
     (n/3^i) log2(n/3^i) work, so with j = k - i the total is
         SUM_{j=1..k} 3^j * j * log2(3) = log2(3) * (3/4)(1 + (2k-1)3^k).

         k    n = 3^k       tree total      closed form         n log2 n    ratio
         3         27           161.67           161.67           128.38   1.2593
         4         81           675.19           675.19           513.53   1.3148
         5        243          2600.92          2600.92          1925.73   1.3506
         6        729          9533.55          9533.55          6932.63   1.3752
         7       2187         33797.74         33797.74         24264.19   1.3929
         8       6561        116989.25        116989.25         83191.51   1.4063
         9      19683        397760.60        397760.60        280771.35   1.4167
        10      59049       1333665.11       1333665.11        935904.51   1.4250
        11     177147       4422149.98       4422149.98       3088484.87   1.4318
        12     531441      14529918.66      14529918.66      10107768.68   1.4375
        13    1594323      47380166.86      47380166.86      32850248.20   1.4423
        14    4782969     153511737.96     153511737.96     106131571.10   1.4464

     The two total columns agree to the last digit, and the ratio tends
     to 3/2 rather than 1.  The constant is not 1 because the work is
     dominated by the LAST levels, not the first: the j-th-from-last
     level does 3^(k-j) * j * log2(3) work, and the j series sums to 3/4,
     which is what produces the factor 3/2 = (3/4) * 2.
```

</details>

**[ ] Exercise 2 —** For the recurrence $T(n) = 2T(n/3) + \Theta(n)$: (a) apply
the Master Theorem; (b) write the recursion-tree level costs and sum the
geometric series; (c) prove $T(n) = \Theta(n)$ by substitution, including the
base case.

<details>
<summary>Solution</summary>

(a) $a = 2$, $b = 3$, $d = \log_3 2 \approx 0.6309$; the additive term is
$\Theta(n^1)$ with $c = 1 > d$, so $T(n) = \Theta(n)$. **Case 3**: the root
alone dominates, because the tree shrinks faster than it branches.

(b) Level $i$ has $2^i$ nodes of size $n/3^i$, each doing $n/3^i$ work, so
level $i$ costs $2^i n / 3^i = n (2/3)^i$ — a *decreasing* geometric series
with ratio $2/3 < 1$, summing to at most $n/(1 - 2/3) = 3n$. The leaves number
$2^{\log_3 n} = n^{0.6309}$, which is sublinear. Total $\le 3n + n^{0.6309} = O(n)$,
and $\Omega(n)$ comes from the top level, so $T(n) = \Theta(n)$.

(c) Guess $T(n) \le C n$. The step:

$$T(n) = 2\,T(n/3) + n \le 2C(n/3) + n = \tfrac{2C}{3}n + n \le C n \iff 1 \le \tfrac{C}{3} \iff C \ge 3.$$

The base case $n = 1$ needs $T(1) = 1 \le C$, which $C = 3$ satisfies, and
$\Omega(n)$ is immediate from the root. So $T(n) = \Theta(n)$, and the pure
power guess is *tight* here — unlike Exercise 1(d), where the additive term is
not a power at all. The substitution succeeds exactly when $c \ne d$, and
Challenge (b) proves that statement.

```python
"""Exercise 2 code block."""
from math import log2, log


def log3(x):
    return log(x) / log(3)

a, b, c = 2, 3, 1
d = log3(a)

print(f"a = {a}, b = {b}, f(n) = Theta(n^{c})")
print(f"d = log_{b} a = log_{b} {a} = {d:.4f}")
print(f"c = {c} > d, so Case 3:  T(n) = Theta(n^{c}) = Theta(n)")
print()
print("(b) Recursion tree.  Level i has a^i = %d^i nodes of size n/%d^i," % (a, b))
print("    each doing n/%d^i work, so level i costs n (a/b)^i." % b)
print(f"       {'level':>6} {'nodes':>10} {'size each':>14} {'level work':>16} {'total so far':>16}")
n = 3 ** 10
total, level, size = 0.0, 1, float(n)
i = 0
while size >= 1.0:
    work = level * size
    total += work
    print(f"       {i:6d} {level:10d} {size:14.6f} {work:16.6f} {total:16.6f}")
    level *= a
    size /= b
    i += 1
leaves = n ** d
print()
print(f"    The level work is a GEOMETRIC series with ratio a/b = {a}/{b} = {a/b:.6f} < 1,")
print(f"    so it sums to at most n / (1 - a/b) = {1/(1-a/b):.4f} n.")
print(f"    Leaves: a^(log_b n) = n^(log_b a) = n^{d:.4f} = {leaves:.2f}")
print(f"    Total <= {1/(1-a/b):.4f}n + {leaves:.2f} = O(n);  Omega(n) from the root.  Theta(n).")
print()
print("    Measured:")
print(f"       {'n':>12} {'tree total':>16} {'total / n':>12}")
for k in (4, 6, 8, 10, 12):
    n = 3 ** k
    tot, lev, sz = 0.0, 1, float(n)
    while sz >= 1.0:
        tot += lev * sz
        lev *= a
        sz /= b
    print(f"       {n:12d} {tot:16.4f} {tot/n:12.4f}")
print()
print("    total / n climbs toward 3 and then stalls: Theta(n).  The constant 3")
print("    is exactly the geometric sum 1/(1 - 2/3) = 3, and it is reached")
print("    rather slowly because the leaf term n^0.63 is still visible at these")
print("    sizes -- but n^0.63 is sublinear, so it vanishes as n grows.")
print()
print("(c) Substitution.  Claim: T(n) <= C n for all n >= 1, with C = 3.")
print()
print("    Inductive step, assuming T(m) <= C m for every m < n:")
print("        T(n) = 2 T(n/3) + n <= 2 C (n/3) + n = (2C/3) n + n")
print("        (2C/3) n + n <= C n   iff   1 <= C/3   iff   C >= 3.")
print("    Base case: T(1) = 1 <= C for every C >= 3.  Take C = 3.")
print("    Omega(n) is immediate: the root alone does n units of work.")


def t(n):
    """T(n) = 2 T(n/3) + n, T(1) = 1."""
    if n <= 1:
        return 1
    return 2 * t(n // 3) + n


print()
print(f"       {'n':>10} {'T(n)':>10} {'T(n)/n':>10} {'<= 3n ?':>9}")
for n in (27, 81, 243, 729, 2187, 6561):
    v = t(n)
    print(f"       {n:10d} {v:10d} {v/n:10.4f} {str(v <= 3*n):>9}")
print()
print("    The bound T(n) <= 3n is never violated, and T(n)/n grows slowly")
print("    because n//3 truncation leaves a residue that recurses once more.")
```

```text
a = 2, b = 3, f(n) = Theta(n^1)
d = log_3 a = log_3 2 = 0.6309
c = 1 > d, so Case 3:  T(n) = Theta(n^1) = Theta(n)

(b) Recursion tree.  Level i has a^i = 2^i nodes of size n/3^i,
    each doing n/3^i work, so level i costs n (a/b)^i.
        level      nodes      size each       level work     total so far
            0          1   59049.000000     59049.000000     59049.000000
            1          2   19683.000000     39366.000000     98415.000000
            2          4    6561.000000     26244.000000    124659.000000
            3          8    2187.000000     17496.000000    142155.000000
            4         16     729.000000     11664.000000    153819.000000
            5         32     243.000000      7776.000000    161595.000000
            6         64      81.000000      5184.000000    166779.000000
            7        128      27.000000      3456.000000    170235.000000
            8        256       9.000000      2304.000000    172539.000000
            9        512       3.000000      1536.000000    174075.000000
           10       1024       1.000000      1024.000000    175099.000000

    The level work is a GEOMETRIC series with ratio a/b = 2/3 = 0.666667 < 1,
    so it sums to at most n / (1 - a/b) = 3.0000 n.
    Leaves: a^(log_b n) = n^(log_b a) = n^0.6309 = 1024.00
    Total <= 3.0000n + 1024.00 = O(n);  Omega(n) from the root.  Theta(n).

    Measured:
                  n       tree total    total / n
                 81         211.0000       2.6049
                729        2059.0000       2.8244
               6561       19171.0000       2.9220
              59049      175099.0000       2.9653
             531441     1586131.0000       2.9846

    total / n climbs toward 3 and then stalls: Theta(n).  The constant 3
    is exactly the geometric sum 1/(1 - 2/3) = 3, and it is reached
    rather slowly because the leaf term n^0.63 is still visible at these
    sizes -- but n^0.63 is sublinear, so it vanishes as n grows.

(c) Substitution.  Claim: T(n) <= C n for all n >= 1, with C = 3.

    Inductive step, assuming T(m) <= C m for every m < n:
        T(n) = 2 T(n/3) + n <= 2 C (n/3) + n = (2C/3) n + n
        (2C/3) n + n <= C n   iff   1 <= C/3   iff   C >= 3.
    Base case: T(1) = 1 <= C for every C >= 3.  Take C = 3.
    Omega(n) is immediate: the root alone does n units of work.

                n       T(n)     T(n)/n   <= 3n ?
               27         65     2.4074      True
               81        211     2.6049      True
              243        665     2.7366      True
              729       2059     2.8244      True
             2187       6305     2.8829      True
             6561      19171     2.9220      True

    The bound T(n) <= 3n is never violated, and T(n)/n grows slowly
    because n//3 truncation leaves a residue that recurses once more.
```

</details>

**[ ] Exercise 3 —** Activity selection: (a) give the greedy algorithm and its
exchange proof; (b) give a set of intervals where *earliest start* time greedy
fails while earliest finish succeeds, and explain which step of the exchange
argument breaks; (c) for the interval set $\{(1,4),(3,5),(5,7),(6,8),(2,6)\}$,
compute both greedies and the true optimum.

<details>
<summary>Solution</summary>

(a) Sort by finishing time, take each interval whose start is at or after the
end of the last one. The exchange: let $O$ be an optimal schedule and $g$ the
interval that ends soonest; let $o$ be the *first* interval of $O$. Since
$e(g) \le e(o)$, replacing $o$ by $g$ is feasible — $g$ starts no later than
$o$ ended, so it cannot collide with anything that followed $o$ — and the
count is unchanged. Induction on the remaining intervals finishes the proof.

(b) Earliest-**start** greedy takes the interval that begins soonest. On
$\{(0,3),(1,2),(2,3)\}$ it takes $(0,3)$, which overlaps both other intervals,
so it returns 1 while the optimum is 2.

The broken step is the same one, pointed the other way. For earliest-finish
the swap works because $e(g) \le e(o)$: the greedy interval finishes before the
one it replaces, so everything after survives. For earliest-start,
$g = (0,3)$ has the **latest** end of the three, so substituting it into an
optimal schedule destroys every interval that came after. Feasibility — the
only thing the correct exchange argument actually buys you — is necessary but
not sufficient: you also need the objective to survive the swap, and here the
count drops from 2 to 1.

Worth knowing, because it is easy to guess wrong: **latest**-start greedy is
*optimal*. It is the same algorithm as earliest-finish run on the mirrored
instance $(s,e) \mapsto (-e,-s)$, so it inherits the same proof. That is why
the mirror of a good greedy rule is a good greedy rule here, and why the
earliest-*start* version — one word away from the correct one — is the one
that fails.

(c) Earliest finish, in finish order: $(1,4)$ take; $(3,5)$ starts at
$3 < 4$, skip; $(5,7)$ starts at $5 \ge 4$, take; $(6,8)$ starts at $6 < 7$,
skip; $(2,6)$ starts at $2 < 7$, skip. Two intervals, and exhaustive search
confirms two is optimal.

```python
"""Exercise 3 code block."""
import itertools


def earliest_finish(iv):
    """The greedy rule: take the interval that ends soonest, then repeat."""
    chosen, last = [], float('-inf')
    for s, e in sorted(iv, key=lambda x: (x[1], x[0])):
        if s >= last:
            chosen.append((s, e))
            last = e
    return chosen


def latest_start(iv):
    """The mirror rule: take the interval that starts latest, then repeat."""
    chosen, last = [], float('inf')
    for s, e in sorted(iv, key=lambda x: (-x[0], -x[1])):
        if e <= last:
            chosen.append((s, e))
            last = s
    return chosen


def earliest_start(iv):
    """The TRAP: take the interval that starts soonest."""
    chosen, last = [], float('-inf')
    for s, e in sorted(iv, key=lambda x: (x[0], x[1])):
        if s >= last:
            chosen.append((s, e))
            last = e
    return chosen


def brute(iv):
    """Exhaustive search over every subset: the ground truth."""
    best = []
    for mask in range(1 << len(iv)):
        sel = sorted(iv[i] for i in range(len(iv)) if mask >> i & 1)
        if all(sel[i][1] <= sel[i + 1][0] for i in range(len(sel) - 1)):
            if len(sel) > len(best):
                best = sel
    return best


print("(a) The exchange argument is a claim about ONE choice, and it holds.")
print("    Let O be an optimal schedule and g the interval that ends soonest.")
print("    Let o be the FIRST interval of O.  Then e(g) <= e(o).  Replacing o")
print("    by g is feasible (g starts no later than o ended, so it cannot")
print("    collide with anything after o) and does not change the count.")
print()
print("(b) Earliest-START greedy loses; latest-START greedy does not.")
print()
trap = [(0, 3), (1, 2), (2, 3)]
print(f"    intervals            : {trap}")
print(f"    earliest-finish      : {earliest_finish(trap)} -> {len(earliest_finish(trap))}   (optimal)")
print(f"    latest-start         : {latest_start(trap)} -> {len(latest_start(trap))}   (optimal)")
print(f"    earliest-START (trap): {earliest_start(trap)} -> {len(earliest_start(trap))}")
print(f"    brute force optimum  : {brute(trap)} -> {len(brute(trap))}")
print()
print("    The trap takes (0,3) first because it starts soonest, and (0,3)")
print("    overlaps both other intervals, so nothing else can ever be added.")
print("    The exchange step FAILS for it: the interval starting soonest has the")
print("    LATEST end, so substituting it into an optimal schedule destroys")
print("    every interval that came after.  Feasibility -- the only thing the")
print("    correct exchange argument buys you -- is not the objective here.")
print()
print("    latest-start greedy is optimal because it is earliest-finish greedy")
print("    run on the negated instance (s, e) -> (-e, -s).  Same algorithm,")
print("    mirrored timeline, same proof.  Verified below on 4000 instances:")


def rand_instances(count, seed=11):
    import random
    rng = random.Random(seed)
    for _ in range(count):
        k = rng.randint(2, 7)
        iv = set()
        while len(iv) < k:
            a0 = rng.randint(0, 25)
            iv.add((a0, a0 + rng.randint(1, 12)))
        yield sorted(iv)


bad_ls = bad_es = 0
for iv in rand_instances(4000):
    o = len(brute(iv))
    if len(latest_start(iv)) != o:
        bad_ls += 1
    if len(earliest_start(iv)) != o:
        bad_es += 1
print(f"        latest-start greedy suboptimal   : {bad_ls} of 4000")
print(f"        earliest-start greedy suboptimal : {bad_es} of 4000")
print()
print("(c) The five-interval instance.")
iv = [(1, 4), (3, 5), (5, 7), (6, 8), (2, 6)]
ef, lsx, op = earliest_finish(iv), latest_start(iv), brute(iv)
print(f"    intervals            : {sorted(iv)}")
print(f"    earliest-finish      : {ef} -> {len(ef)}")
print(f"    latest-start         : {lsx} -> {len(lsx)}")
print(f"    brute force optimum  : {op} -> {len(op)}")
print(f"    earliest-finish is optimal: {len(ef) == len(op)}")
print()
print("    Walk through earliest-finish in finish order: (1,4) take; (3,5)")
print("    starts at 3 < 4, skip; (5,7) starts at 5 >= 4, take; (6,8) starts")
print("    at 6 < 7, skip; (2,6) starts at 2 < 7, skip.  Two intervals.")
print()
print("    Search for the smallest instance where earliest-start greedy fails:")


def search_counterexample():
    for k in (3, 4):
        for starts in itertools.combinations(range(6), k):
            for lens in itertools.product(range(1, 5), repeat=k):
                cand = [(starts[i], starts[i] + lens[i]) for i in range(k)]
                if len(set(cand)) < k:
                    continue
                if len(earliest_start(cand)) < len(brute(cand)):
                    return sorted(cand)
    return None


first = search_counterexample()
print(f"        smallest counterexample: {first}")
print(f"        earliest-start gets {len(earliest_start(first))}, "
      f"optimum is {len(brute(first))}")
print("        It needs only three intervals.  That is the signature of a")
print("        structural failure rather than a statistical one: one interval")
print("        chosen on the wrong key can dominate every later choice, so")
print("        enlarging the instance cannot dilute the error.")
```

```text
(a) The exchange argument is a claim about ONE choice, and it holds.
    Let O be an optimal schedule and g the interval that ends soonest.
    Let o be the FIRST interval of O.  Then e(g) <= e(o).  Replacing o
    by g is feasible (g starts no later than o ended, so it cannot
    collide with anything after o) and does not change the count.

(b) Earliest-START greedy loses; latest-START greedy does not.

    intervals            : [(0, 3), (1, 2), (2, 3)]
    earliest-finish      : [(1, 2), (2, 3)] -> 2   (optimal)
    latest-start         : [(2, 3), (1, 2)] -> 2   (optimal)
    earliest-START (trap): [(0, 3)] -> 1
    brute force optimum  : [(1, 2), (2, 3)] -> 2

    The trap takes (0,3) first because it starts soonest, and (0,3)
    overlaps both other intervals, so nothing else can ever be added.
    The exchange step FAILS for it: the interval starting soonest has the
    LATEST end, so substituting it into an optimal schedule destroys
    every interval that came after.  Feasibility -- the only thing the
    correct exchange argument buys you -- is not the objective here.

    latest-start greedy is optimal because it is earliest-finish greedy
    run on the negated instance (s, e) -> (-e, -s).  Same algorithm,
    mirrored timeline, same proof.  Verified below on 4000 instances:
        latest-start greedy suboptimal   : 0 of 4000
        earliest-start greedy suboptimal : 439 of 4000

(c) The five-interval instance.
    intervals            : [(1, 4), (2, 6), (3, 5), (5, 7), (6, 8)]
    earliest-finish      : [(1, 4), (5, 7)] -> 2
    latest-start         : [(6, 8), (3, 5)] -> 2
    brute force optimum  : [(1, 4), (5, 7)] -> 2
    earliest-finish is optimal: True

    Walk through earliest-finish in finish order: (1,4) take; (3,5)
    starts at 3 < 4, skip; (5,7) starts at 5 >= 4, take; (6,8) starts
    at 6 < 7, skip; (2,6) starts at 2 < 7, skip.  Two intervals.

    Search for the smallest instance where earliest-start greedy fails:
        smallest counterexample: [(0, 3), (1, 2), (2, 3)]
        earliest-start gets 1, optimum is 2
        It needs only three intervals.  That is the signature of a
        structural failure rather than a statistical one: one interval
        chosen on the wrong key can dominate every later choice, so
        enlarging the instance cannot dilute the error.
```

</details>

**[ ] Exercise 4 —** Knapsack: (a) write the DP recurrence and its state count
for $n$ items and capacity $C$; (b) decide how bad the greedy-by-ratio answer
can be — is it unboundedly bad, or is there a constant? Prove whatever you
claim and exhibit a family that attains your constant; (c) decide whether
*fractional* knapsack is still greedy-solvable, and prove it.

<details>
<summary>Solution</summary>

(a) $\mathrm{OPT}(i,c) = \max(\mathrm{OPT}(i-1,c),\ v_i + \mathrm{OPT}(i-1, c - w_i))$
with $\mathrm{OPT}(0,c) = 0$ and $\mathrm{OPT}(i, 0) = 0$. There are
$(n+1)(C+1)$ states, so $O(nC)$ time and, with rolling rows, $O(C)$ space. The
recurrence is *take or skip*: state $(i,c)$ splits on whether item $i$ is in
the packing, which is the structural reason the DP cannot be replaced by a
single greedy choice.

(b) **Bounded — greedy-by-ratio is a 2-approximation.** The trap in a lazy
answer here is to claim the ratio is unbounded; it is not, and the reason is
the indivisibility of one item.

Take capacity $C = 2N$ and three items: one heavy $(N+1,\, N+1)$ of density
$1$, and two light $(N,\, N-1)$ of density $(N-1)/N = 1 - 1/N$, strictly
lower. Greedy takes the heavy item first (highest density) and then *nothing*
fits, since $2N - (N+1) = N - 1 < N$. The optimum takes both light items for
$2N - 2$. Hence

$$\frac{\mathrm{OPT}}{\mathrm{greedy}} = \frac{2N - 2}{N + 1} \;\longrightarrow\; 2 .$$

The bound is tight, and 2 is the best any density-ordered method can do: the
heavy item has strictly the highest density, so every such method must
consider it first, and a single indivisible item cannot be split to make room.

(c) Fractional knapsack *is* greedy: sort by density and fill until capacity is
exhausted. The exchange works because swapping a fraction $\delta$ of a
lower-density item for a fraction $\delta$ of a higher-density one preserves
total weight and increases total value, and there is no minimum step size to
respect. That is the whole difference: fractional feasibility is closed under
repartitioning weight arbitrarily, which is exactly the exchange property the
0/1 version lacks. Consequently the fractional value is always at least the
0/1 optimum — every 0/1 packing is also a legal fractional packing — and the
run below confirms it is never below and usually strictly above.

```python
"""Exercise 4 code block."""
import itertools


def dp_knapsack(weights, values, C):
    """OPT(i, c) = max(OPT(i-1, c), v_i + OPT(i-1, c - w_i))."""
    n = len(weights)
    opt = [[0] * (C + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for c in range(C + 1):
            opt[i][c] = opt[i - 1][c]
            if weights[i - 1] <= c:
                opt[i][c] = max(opt[i][c],
                                values[i - 1] + opt[i - 1][c - weights[i - 1]])
    return opt[n][C], opt


def greedy_01(weights, values, C):
    """0/1 knapsack by value/weight ratio: take, or skip forever."""
    total_w = total_v = 0
    for i in sorted(range(len(weights)), key=lambda i: -values[i] / weights[i]):
        if total_w + weights[i] <= C:
            total_w += weights[i]
            total_v += values[i]
    return total_v


def greedy_fractional(weights, values, C):
    """Fractional knapsack by ratio: the same order, but you may stop mid-item."""
    rem, total_v = C, 0.0
    for i in sorted(range(len(weights)), key=lambda i: -values[i] / weights[i]):
        if rem <= 0:
            break
        take = min(weights[i], rem)
        total_v += take * values[i] / weights[i]
        rem -= take
    return total_v


def brute(weights, values, C):
    best = 0
    for mask in range(1 << len(weights)):
        if sum(weights[i] for i in range(len(weights)) if mask >> i & 1) <= C:
            best = max(best, sum(values[i] for i in range(len(values)) if mask >> i & 1))
    return best


print("(a) State count and cost.  OPT(i, c) with i = 0..n and c = 0..C:")
print("    (n+1)(C+1) states, O(1) transitions each  ->  O(nC) time,")
print("    O(nC) space, or O(C) space with two rolling rows.")
print()
w = [10, 20, 30]
v = [60, 100, 120]
C = 50
print(f"    Worked: items {[(wi, vi) for wi, vi in zip(w, v)]}, capacity {C}")
best, opt = dp_knapsack(w, v, C)
print(f"    DP value            : {best}   (states filled: {len(opt) - 1} x {len(opt[0]) - 1} = {(len(opt)-1)*(len(opt[0])-1)})")
print(f"    brute force value   : {brute(w, v, C)}")
print(f"    greedy by ratio     : {greedy_01(w, v, C)}")
print(f"    ratios              : {[round(vi/wi, 4) for wi, vi in zip(w, v)]}")
print()
print("(b) How bad can greedy-by-ratio be?  Bounded -- by a factor of 2.")
print("    Capacity C = 2N.  One heavy item (N+1, N+1) of density 1, and two")
print("    items (N, N-1) of density (N-1)/N = 1 - 1/N, slightly lower.")
print("    Greedy takes the heavy item and then NOTHING fits; the optimum takes")
print("    both light items.")
print()
print(f"    {'N':>8} {'C':>9} {'greedy':>10} {'optimum':>10} {'opt/greedy':>12} {'gap':>10}")
for N in (10, 100, 1000, 10000, 100000):
    items_w = [N + 1, N, N]
    items_v = [N + 1, N - 1, N - 1]
    cap = 2 * N
    g = greedy_01(items_w, items_v, cap)
    o = brute(items_w, items_v, cap)
    print(f"    {N:8d} {cap:9d} {g:10d} {o:10d} {o / g:12.4f} {o - g:10d}")
print()
print("    The ratio climbs to 2.0000 and never exceeds it, so greedy-by-ratio")
print("    is a 2-APPROXIMATION, not an unbounded failure.  Derivation:")
print("        greedy = N + 1,  optimum = 2N - 2,  ratio = (2N-2)/(N+1) -> 2.")
print("    A 2-approximation is all that 0/1 knapsack permits: the heavy item")
print("    has strictly higher density, so ANY density-ordered method must")
print("    look at it first, and one indivisible item cannot be split.")
print()
print("(c) Fractional knapsack IS greedy, and the same code shows the difference.")
print()
print(f"    {'instance':<34} {'C':>5} {'0/1 greedy':>12} {'0/1 OPT':>9} {'fractional':>12} {'frac - opt':>12}")
cases = [([10, 20, 30], [60, 100, 120], 50),
         ([10, 20, 30], [60, 100, 120], 60),
         ([5, 5, 5], [10, 10, 10], 12),
         ([7, 11, 13], [10, 100, 100], 20)]
for ws, vs, cap in cases:
    o = brute(ws, vs, cap)
    fr = greedy_fractional(ws, vs, cap)
    print(f"    {str([(a, b) for a, b in zip(ws, vs)]):<34} {cap:5d} "
          f"{greedy_01(ws, vs, cap):12d} {o:9d} {fr:12.2f} {fr - o:12.2f}")
print()
print("    The fractional value is the TRUE fractional optimum, and it is at")
print("    least the 0/1 optimum on every row -- necessarily, since every 0/1")
print("    packing is also a legal fractional packing.  Where they differ, the")
print("    difference is exactly the value of splitting one item partway, which")
print("    is the single capability 0/1 removes.")
print()


def rand_case(rng):
    k = rng.randint(2, 7)
    ws = [rng.randint(1, 20) for _ in range(k)]
    vs = [rng.randint(1, 60) for _ in range(k)]
    return ws, vs, rng.randint(1, 50)


import random
rng = random.Random(5)
violations = 0
strict = 0
for _ in range(4000):
    ws, vs, cap = rand_case(rng)
    o = brute(ws, vs, cap)
    fr = greedy_fractional(ws, vs, cap)
    if fr < o - 1e-9:
        violations += 1
    if fr > o + 1e-9:
        strict += 1
print(f"    Over 4000 random instances: fractional greedy ever below the 0/1")
print(f"    optimum: {violations} times;  strictly above it: {strict} times.")
print()
print("    So the exchange argument for the fractional case is not a heuristic")
print("    that happens to work: it can move an arbitrary amount of weight")
print("    between any two items, so every packing can be driven to ratio-sorted")
print("    order without ever exceeding capacity.  In 0/1 the smallest")
print("    permitted move is 'take it or leave it', which is a step too coarse")
print("    to carry the argument through.")
```

```text
(a) State count and cost.  OPT(i, c) with i = 0..n and c = 0..C:
    (n+1)(C+1) states, O(1) transitions each  ->  O(nC) time,
    O(nC) space, or O(C) space with two rolling rows.

    Worked: items [(10, 60), (20, 100), (30, 120)], capacity 50
    DP value            : 220   (states filled: 3 x 50 = 150)
    brute force value   : 220
    greedy by ratio     : 160
    ratios              : [6.0, 5.0, 4.0]

(b) How bad can greedy-by-ratio be?  Bounded -- by a factor of 2.
    Capacity C = 2N.  One heavy item (N+1, N+1) of density 1, and two
    items (N, N-1) of density (N-1)/N = 1 - 1/N, slightly lower.
    Greedy takes the heavy item and then NOTHING fits; the optimum takes
    both light items.

           N         C     greedy    optimum   opt/greedy        gap
          10        20         11         18       1.6364          7
         100       200        101        198       1.9604         97
        1000      2000       1001       1998       1.9960        997
       10000     20000      10001      19998       1.9996       9997
      100000    200000     100001     199998       2.0000      99997

    The ratio climbs to 2.0000 and never exceeds it, so greedy-by-ratio
    is a 2-APPROXIMATION, not an unbounded failure.  Derivation:
        greedy = N + 1,  optimum = 2N - 2,  ratio = (2N-2)/(N+1) -> 2.
    A 2-approximation is all that 0/1 knapsack permits: the heavy item
    has strictly higher density, so ANY density-ordered method must
    look at it first, and one indivisible item cannot be split.

(c) Fractional knapsack IS greedy, and the same code shows the difference.

    instance                               C   0/1 greedy   0/1 OPT   fractional   frac - opt
    [(10, 60), (20, 100), (30, 120)]      50          160       220       240.00        20.00
    [(10, 60), (20, 100), (30, 120)]      60          280       280       280.00         0.00
    [(5, 10), (5, 10), (5, 10)]           12           20        20        24.00         4.00
    [(7, 10), (11, 100), (13, 100)]       20          110       110       169.23        59.23

    The fractional value is the TRUE fractional optimum, and it is at
    least the 0/1 optimum on every row -- necessarily, since every 0/1
    packing is also a legal fractional packing.  Where they differ, the
    difference is exactly the value of splitting one item partway, which
    is the single capability 0/1 removes.

    Over 4000 random instances: fractional greedy ever below the 0/1
    optimum: 0 times;  strictly above it: 2841 times.

    So the exchange argument for the fractional case is not a heuristic
    that happens to work: it can move an arbitrary amount of weight
    between any two items, so every packing can be driven to ratio-sorted
    order without ever exceeding capacity.  In 0/1 the smallest
    permitted move is 'take it or leave it', which is a step too coarse
    to carry the argument through.
```

</details>

**[ ] Exercise 5 —** (a) State and prove the LCS recurrence. (b) Give the state
count and time for strings of lengths $m$ and $n$, and for $n$ DNA sequences
of length $L$. (c) Determine the running time of the naive two-branch
recursion $T(p,q) = T(p-1,q) + T(p,q-1)$ with $T = 1$ on either axis, and
explain why guessing $\Theta(\varphi^{m+n})$ is wrong.

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

(c) The recursion has an exact closed form, and it is **not** a Fibonacci-type
growth. $T(p,q) = \binom{p+q}{p}$: Pascal's identity
$\binom{p+q}{p} = \binom{p+q-1}{p-1} + \binom{p+q-1}{p}$ *is* the recurrence,
and $\binom{p}{0} = \binom{0}{q} = 1$ *is* the base case. The invocation count
satisfies $C = 1 + C(p-1,q) + C(p,q-1)$, hence $C = 2\binom{p+q}{p} - 1$.

Stirling on the central case $p = q = k$ gives $\binom{2k}{k} \sim 4^k/\sqrt{\pi k}$,
so

$$T(p,q) = \Theta\!\left(\frac{2^{m+n}}{\sqrt{m+n}}\right).$$

The $\varphi^{m+n}$ guess is tempting because $\varphi^{m+n}$ does satisfy the
*homogeneous* recurrence ($x^{m+n} = x^{m+n-1}(\tfrac1\varphi + 1)$ exactly when
$x^2 = x + 1$) — but it does not satisfy the **base case**, which is the only
thing that determines the solution. The data settles it: $T/2^{m+n}$ drifts
*down* like $1/\sqrt{m+n}$ while $T/\varphi^{m+n}$ blows up, and a function cannot
be $\Theta$ of a quantity its ratio to grows without bound.

Memoisation is the fix, and it is worth noting what it does: it stores each of
the $mn$ interior states exactly once, so the recursion becomes $\Theta(mn)$ —
the same bound as the DP table. The DP is not a shortcut *around* a fast
recursion; it **is** the fast version of an exponential one.

```python
"""Exercise 5 code block."""
import math
from math import comb

X = "ABCBDAB"
Y = "BDCABA"
m, n = len(X), len(Y)


def lcs_table(x, y):
    """The O(mn) DP: L(i, j) = L(i-1, j-1) + 1 if they match, else the max."""
    L = [[0] * (len(y) + 1) for _ in range(len(x) + 1)]
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            if x[i - 1] == y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])
    return L


L = lcs_table(X, Y)
print("(a)/(b) The DP for two strings.")
print(f"    x = {X!r}  (m = {m})")
print(f"    y = {Y!r}  (n = {n})")
print(f"    L(m, n) = {L[m][n]}")
print(f"    states filled: (m+1)(n+1) = {m + 1} x {n + 1} = {(m + 1) * (n + 1)}")
print(f"    time O(mn) = O({m * n}); space O(mn), or O(min(m,n)) = O({min(m, n)}) rolling.")
print()

calls = 0


def naive(p, q):
    """T(p, q) = T(p-1, q) + T(p, q-1), T = 1 on either axis. NO memoisation.

    Returns the value AND the number of invocations, because the two are
    different quantities and the distinction matters for the asymptotics.
    """
    global calls
    calls += 1
    if p == 0 or q == 0:
        return 1
    return naive(p - 1, q) + naive(p, q - 1)


print("(c) The naive two-branch recursion, counted rather than clocked.")
print()
print(f"    {'m':>3} {'n':>3} {'T(m,n)':>12} {'binom(m+n,m)':>13} {'equal':>6} "
      f"{'invocations':>13} {'2*binom - 1':>13} {'T / 2^(m+n)':>13} {'T / phi^(m+n)':>15}")
phi = (1 + math.sqrt(5)) / 2
rows = []
for mm, nn in ((3, 4), (5, 6), (6, 7), (8, 8), (10, 10), (12, 12)):
    calls = 0
    val = naive(mm, nn)
    c = comb(mm + nn, mm)
    rows.append((mm, nn, val, c, calls))
    print(f"    {mm:3d} {nn:3d} {val:12d} {c:13d} {str(val == c):>6} "
          f"{calls:13d} {2 * c - 1:13d} {val / 2 ** (mm + nn):13.6f} {val / phi ** (mm + nn):15.6f}")
print()
print("    T(p, q) = binom(p + q, p) EXACTLY.  Pascal's identity")
print("        binom(p+q, p) = binom(p+q-1, p-1) + binom(p+q-1, p)")
print("    is literally the recurrence, and binom(p, 0) = binom(0, q) = 1 is")
print("    literally the base case.  The invocation count satisfies")
print("    C = 1 + C(p-1,q) + C(p,q-1), hence C = 2 binom(p+q, p) - 1 -- which")
print("    is why the two middle columns agree on every row.")
print()
print("    Stirling on the central case p = q = k:  binom(2k, k) ~ 4^k/sqrt(pi k),")
print("    so T = Theta(2^(m+n) / sqrt(m+n)), NOT Theta(phi^(m+n)).  Read the")
print("    two ratio columns: T / 2^(m+n) drifts DOWN like 1/sqrt(m+n), while")
print("    T / phi^(m+n) BLOWS UP.  An upper bound that the data grows past")
print("    cannot be the answer.")
print()
print(f"    sqrt(pi (m+n)/2) * T / 2^(m+n)  ->  1:")
for mm, nn, val, _, _ in rows:
    print(f"       {'m+n = ' + str(mm + nn):>10} {math.sqrt(math.pi * (mm + nn) / 2) * val / 2 ** (mm + nn):10.6f}")
print()


def memo(p, q, table):
    """The same recursion, but each interior state is computed once."""
    if p == 0 or q == 0:
        return 1
    if (p, q) in table:
        return table[(p, q)]
    table[(p, q)] = memo(p - 1, q, table) + memo(p, q - 1, table)
    return table[(p, q)]


print(f"    {'m':>3} {'n':>3} {'naive calls':>14} {'memo states':>13} {'m*n':>6} {'ratio':>11} {'ratio':>9}")
for mm, nn in ((3, 4), (5, 6), (6, 7), (8, 8), (10, 10)):
    calls = 0
    naive(mm, nn)
    nc = calls
    tbl = {}
    memo(mm, nn, tbl)
    ms = len(tbl) + 1
    print(f"    {mm:3d} {nn:3d} {nc:14d} {ms:13d} {mm * nn:6d} {nc / ms:10.1f}x "
          f"{nc / (ms ** 2):8.3f}")
print()
print("    'memo states' is m*n + 1: every interior state (p, q) with p >= 1")
print("    and q >= 1 is stored exactly once.  The last column is the")
print("    super-linear one -- it grows, so the naive version is super-")
print("    quadratic, i.e. exponential in m + n.")
print()
print(f"    For the lesson's 7 x 6 case: (7+1)(6+1) = 56 entries, exactly the")
print(f"    56 states Block 4 fills, and O(42) transitions -- so the DP table is")
print(f"    not a shortcut around a fast recursion, it IS the fast version of")
print(f"    a recursion that is exponential on its own.")
```

```text
(a)/(b) The DP for two strings.
    x = 'ABCBDAB'  (m = 7)
    y = 'BDCABA'  (n = 6)
    L(m, n) = 4
    states filled: (m+1)(n+1) = 8 x 7 = 56
    time O(mn) = O(42); space O(mn), or O(min(m,n)) = O(6) rolling.

(c) The naive two-branch recursion, counted rather than clocked.

      m   n       T(m,n)  binom(m+n,m)  equal   invocations   2*binom - 1   T / 2^(m+n)   T / phi^(m+n)
      3   4           35            35   True            69            69      0.273438        1.205465
      5   6          462           462   True           923           923      0.225586        2.321549
      6   7         1716          1716   True          3431          3431      0.209473        3.293654
      8   8        12870         12870   True         25739         25739      0.196381        5.831447
     10  10       184756        184756   True        369511        369511      0.176197       12.213658
     12  12      2704156       2704156   True       5408311       5408311      0.161180       26.081248

    T(p, q) = binom(p + q, p) EXACTLY.  Pascal's identity
        binom(p+q, p) = binom(p+q-1, p-1) + binom(p+q-1, p)
    is literally the recurrence, and binom(p, 0) = binom(0, q) = 1 is
    literally the base case.  The invocation count satisfies
    C = 1 + C(p-1,q) + C(p,q-1), hence C = 2 binom(p+q, p) - 1 -- which
    is why the two middle columns agree on every row.

    Stirling on the central case p = q = k:  binom(2k, k) ~ 4^k/sqrt(pi k),
    so T = Theta(2^(m+n) / sqrt(m+n)), NOT Theta(phi^(m+n)).  Read the
    two ratio columns: T / 2^(m+n) drifts DOWN like 1/sqrt(m+n), while
    T / phi^(m+n) BLOWS UP.  An upper bound that the data grows past
    cannot be the answer.

    sqrt(pi (m+n)/2) * T / 2^(m+n)  ->  1:
          m+n = 7   0.906707
         m+n = 11   0.937709
         m+n = 13   0.946584
         m+n = 16   0.984506
         m+n = 20   0.987583
         m+n = 24   0.989640

      m   n    naive calls   memo states    m*n       ratio     ratio
      3   4             69            13     12        5.3x    0.408
      5   6            923            31     30       29.8x    0.960
      6   7           3431            43     42       79.8x    1.856
      8   8          25739            65     64      396.0x    6.092
     10  10         369511           101    100     3658.5x   36.223

    'memo states' is m*n + 1: every interior state (p, q) with p >= 1
    and q >= 1 is stored exactly once.  The last column is the
    super-linear one -- it grows, so the naive version is super-
    quadratic, i.e. exponential in m + n.

    For the lesson's 7 x 6 case: (7+1)(6+1) = 56 entries, exactly the
    56 states Block 4 fills, and O(42) transitions -- so the DP table is
    not a shortcut around a fast recursion, it IS the fast version of
    a recursion that is exponential on its own.
```

</details>

**[ ] Exercise 6 —** (a) Give a decision tree proving $\Omega(n \log n)$ for
comparison sorting. (b) Compute the gap between merge sort's worst case
$n\log_2 n - n + 1$ and $\log_2 n!$ at $n = 1024$, and compare it with the
asymptotic prediction $0.4427n$ — is the prediction an over- or an
under-estimate, and why? (c) Explain why insertion sort on nearly sorted input
is faster, and what that says about the model the lower bound lives in.

<details>
<summary>Solution</summary>

(a) Each comparison has two outcomes, so the execution of a comparison sort on
$n$ distinct keys is a binary tree; two inputs that lead to the same leaf are
indistinguishable to the algorithm and must produce the same output, so each
leaf covers at most one of the $n!$ orders; a tree with at least $n!$ leaves
has depth at least $\lceil\log_2 n!\rceil = \Omega(n \log n)$. The bound is
simultaneously in bits and in comparisons, because one comparison carries at
most one bit.

(b) At $n = 1024 = 2^{10}$: merge sort's worst case is
$1024 \cdot 10 - 1024 + 1 = 9217$ comparisons, and
$\log_2(1024!) = 8769.006$ bits, a gap of **447.994**.

The asymptotic prediction $0.4427n = 453.32$ **overstates** the gap by 5.33
comparisons, about 1.19%. That is not noise, because the prediction drops a
term that is not yet small: from Stirling,
$\log_2 n! = n\log_2 n - n\log_2 e + \tfrac12\log_2(2\pi n) + O(1/n)$, so

$$\text{gap} = (\log_2 e - 1)\,n + 1 - \tfrac12 \log_2(2\pi n) + O(1/n) = 0.4427n + 1 - 6.3257 = 447.994,$$

exactly the observed value. The dropped term grows like $\tfrac12\log_2 n$, so
the relative error of the bare linear estimate decays only like
$\log_2 n / n$ — far too slowly to trust at any $n$ you will actually sort.

(c) Insertion sort is a comparison sort, so $\Omega(n \log n)$ still applies to
it in the worst case; it is faster on nearly sorted data because its cost is
$\Theta(n + I)$ where $I$ is the number of inversions. The point is that the
lower bound constrains the *worst case over all inputs of a model*, and a
model parameter — here the input order — can matter as much as $n$. That is
also why Timsort is legal: it is still a comparison sort, but it detects and
merges existing runs proportionally, so its typical case is linear while its
worst case remains $O(n \log n)$.

```python
"""Exercise 6 code block."""
import math
import random
from math import lgamma, log, log2

LN2 = log(2)


def log2_fact(n):
    """log2(n!) via lgamma, so we do not have to build the factorial."""
    return lgamma(n + 1) / LN2


def merge_sort_worst(n):
    """n log2 n - n + 1, the tight worst case for n a power of two."""
    return n * log2(n) - n + 1


def leaf_depth(n):
    """The deepest leaf of the decision tree: ceil(log2(n!)) bits."""
    return math.ceil(log2_fact(n))


print("(a) The decision tree.  Every comparison has two outcomes, so an")
print("    execution is a path in a binary tree.  Two inputs that reach the")
print("    same leaf are indistinguishable to the algorithm, and a correct")
print("    sort must emit different outputs for them, so every leaf covers at")
print("    most one of the n! orders.  Depth >= ceil(log2(n!)) = Omega(n log n).")
print()
print("    The bound is in bits and comparisons at once, because one comparison")
print("    is worth at most one bit of information.")
print()
print("(b) The gap at n = 1024, against its own asymptotic prediction.")
print()
print(f"    {'n':>7} {'log2(n!)':>14} {'ceil':>8} {'merge worst':>13} {'gap':>10} "
      f"{'0.4427 n':>10} {'exact pred':>12}")
for n in (32, 64, 128, 256, 512, 1024, 2048, 4096):
    lf = log2_fact(n)
    ms = merge_sort_worst(n)
    exact = (log2(math.e) - 1) * n + 1 - 0.5 * log2(2 * math.pi * n)
    print(f"    {n:7d} {lf:14.3f} {leaf_depth(n):8d} {ms:13.1f} "
          f"{ms - lf:10.3f} {0.4427 * n:10.2f} {exact:12.3f}")
print()
n = 1024
lf = log2_fact(n)
ms = merge_sort_worst(n)
print(f"    At n = {n}:")
print(f"        log2(n!)          = {lf:.3f} bits")
print(f"        merge sort worst  = {n} * {log2(n):.0f} - {n} + 1 = {ms:.0f} comparisons")
print(f"        gap               = {ms - lf:.3f}")
print(f"    Derivation of the prediction, term by term:")
print(f"        log2(n!) = n log2 n - n log2 e + 0.5 log2(2 pi n) + O(1/n)")
print(f"        gap     = (n log2 n - n + 1) - log2(n!)")
print(f"               = (log2 e - 1) n + 1 - 0.5 log2(2 pi n) + O(1/n)")
print(f"               = {(log2(math.e) - 1):.4f} n + 1 - {0.5 * log2(2 * math.pi * n):.4f}")
print(f"               = {(log2(math.e) - 1) * n:.3f} + 1 - {0.5 * log2(2 * math.pi * n):.4f}")
print(f"               = {(log2(math.e) - 1) * n + 1 - 0.5 * log2(2 * math.pi * n):.3f}")
print(f"        observed gap      = {ms - lf:.3f}   -- exact, to 3 decimals")
print()
over = 0.4427 * n - (ms - lf)
print(f"    The 0.4427 n estimate OVERSTATES the gap by {over:.2f} comparisons,")
print(f"    a relative error of {100 * over / (ms - lf):.2f}%, and that is not noise:")
print("    it drops the -0.5 log2(2 pi n) term, still -6.33 at n = 1024.")
print("    That term grows like 0.5 log2 n, so the relative error of the pure")
print("    linear estimate decays only like log2(n) / n -- slow enough that the")
print("    approximation is useless at any n you will ever sort.")
print()
print("(c) Insertion sort on nearly sorted input.")
print()


def inversions(a):
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])


def insertion_comparisons(a):
    c = 0
    for i in range(1, len(a)):
        j = i
        while j > 0 and a[j - 1] > a[j]:
            a[j - 1], a[j] = a[j], a[j - 1]
            j -= 1
            c += 1
    return c


n = 64
rng = random.Random(3)
shuffled = list(range(n))
rng.shuffle(shuffled)
swapped = list(range(n))
swapped[30], swapped[31] = swapped[31], swapped[30]
print(f"    {'input':<34} {'inversions':>11} {'comparisons':>13} {'n + I':>8}")
for label, arr in [("random permutation", shuffled),
                   ("sorted", list(range(n))),
                   ("one swap from sorted", swapped),
                   ("reversed", list(range(n))[::-1])]:
    arr = list(arr)
    I = inversions(arr)
    c = insertion_comparisons(arr)
    print(f"    {label:<34} {I:11d} {c:13d} {n + I:8d}")
print()
print("    Insertion sort does exactly one comparison per inversion plus one")
print("    per key, so it costs Theta(n + I).  On nearly sorted data I = 0 or")
print("    I = O(n), giving Theta(n) -- linear, not n log n.")
print()
print("    This does NOT contradict Omega(n log n).  The lower bound is a")
print("    statement about the WORST case of a model: over all inputs, some")
print("    arrangement has Theta(n^2) inversions and the algorithm must pay.")
print("    An algorithm may be much faster on easy inputs without ceasing to")
print("    be a comparison sort.  Timsort is exactly this: it detects and")
print("    merges existing runs, so its typical case is linear while its")
print("    worst case stays n log n.")
```

```text
(a) The decision tree.  Every comparison has two outcomes, so an
    execution is a path in a binary tree.  Two inputs that reach the
    same leaf are indistinguishable to the algorithm, and a correct
    sort must emit different outputs for them, so every leaf covers at
    most one of the n! orders.  Depth >= ceil(log2(n!)) = Omega(n log n).

    The bound is in bits and comparisons at once, because one comparison
    is worth at most one bit of information.

(b) The gap at n = 1024, against its own asymptotic prediction.

          n       log2(n!)     ceil   merge worst        gap   0.4427 n   exact pred
         32        117.663      118         129.0     11.337      14.17       11.340
         64        295.995      296         321.0     25.005      28.33       25.007
        128        716.162      717         769.0     52.838      56.67       52.839
        256       1683.996     1684        1793.0    109.004     113.33      109.004
        512       3875.166     3876        4097.0    221.834     226.66      221.834
       1024       8769.006     8770        9217.0    447.994     453.32      447.994
       2048      19580.186    19581       20481.0    900.814     906.65      900.814
       4096      43250.047    43251       45057.0   1806.953    1813.30     1806.953

    At n = 1024:
        log2(n!)          = 8769.006 bits
        merge sort worst  = 1024 * 10 - 1024 + 1 = 9217 comparisons
        gap               = 447.994
    Derivation of the prediction, term by term:
        log2(n!) = n log2 n - n log2 e + 0.5 log2(2 pi n) + O(1/n)
        gap     = (n log2 n - n + 1) - log2(n!)
               = (log2 e - 1) n + 1 - 0.5 log2(2 pi n) + O(1/n)
               = 0.4427 n + 1 - 6.3257
               = 453.320 + 1 - 6.3257
               = 447.994
        observed gap      = 447.994   -- exact, to 3 decimals

    The 0.4427 n estimate OVERSTATES the gap by 5.33 comparisons,
    a relative error of 1.19%, and that is not noise:
    it drops the -0.5 log2(2 pi n) term, still -6.33 at n = 1024.
    That term grows like 0.5 log2 n, so the relative error of the pure
    linear estimate decays only like log2(n) / n -- slow enough that the
    approximation is useless at any n you will ever sort.

(c) Insertion sort on nearly sorted input.

    input                               inversions   comparisons    n + I
    random permutation                         847           847      911
    sorted                                       0             0       64
    one swap from sorted                         1             1       65
    reversed                                  2016          2016     2080

    Insertion sort does exactly one comparison per inversion plus one
    per key, so it costs Theta(n + I).  On nearly sorted data I = 0 or
    I = O(n), giving Theta(n) -- linear, not n log n.

    This does NOT contradict Omega(n log n).  The lower bound is a
    statement about the WORST case of a model: over all inputs, some
    arrangement has Theta(n^2) inversions and the algorithm must pay.
    An algorithm may be much faster on easy inputs without ceasing to
    be a comparison sort.  Timsort is exactly this: it detects and
    merges existing runs, so its typical case is linear while its
    worst case stays n log n.
```

</details>

**Challenge — Prove the whole chain.**

**[ ]** (a) Show that $c = d$ is exactly the regime where the recursion-tree
level costs are all equal. (b) Show that the pure-power substitution guess
succeeds iff $c \ne d$, and give the slack term needed at $c = d$. (c) Using
your answers, predict which of $T(n) = 8T(n/2) + \Theta(n)$ and
$T(n) = 8T(n/2) + \Theta(n^2)$ is faster for large $n$, and explain why the
intuition "more work per node should be slower" fails. (d) Extend: what does
Akra–Bazzi say about $T(n) = 2T(n/2) + \Theta(n \log n)$, and how does the
FFT recurrence $2T(n/2) + \Theta(n)$ differ — what would break if you used the
FFT's answer for the other one?

<details>
<summary>Solution</summary>

**(a)** Level $i$ of the tree has $a^i$ nodes of size $n/b^i$ each doing
$(n/b^i)^c$ work, so it costs

$$a^i \left(\frac{n}{b^i}\right)^c = n^c \left(\frac{a}{b^c}\right)^i .$$

The ratio between consecutive levels is $a/b^c$, and that ratio equals $1$
precisely when $c = \log_b a = d$. So $c = d$ is exactly the point where no
level decays and none grows: every level costs the same $\Theta(n^d)$, and the
$\log_b n$ levels can no longer be swallowed by a geometric sum. The answer is
$\Theta(n^d \log n)$ rather than $\Theta(n^d)$.

This is the real content of "Case 2". It is not that two things happen to tie;
it is that the *ratio of successive terms* is $1$, which is the only value for
which the geometric-series trick fails.

**(b)** Guess $T(n) \le K n^d$. The step is
$aK(n/b)^d + n^c \le K n^d$, i.e. $n^c \le K n^d\left(1 - a/b^d\right)$.

- If $c > d$: $a/b^d < 1$, so the bracket is a positive constant and $n^c$ is
  dominated — the guess succeeds with slack.
- If $c < d$: $a/b^d > 1$ and the bracket is negative, so the guess fails but
  a *smaller* power $K n^c$ works, which is Case 3.
- If $c = d$: $a/b^d = 1$, the bracket is $0$, and the guess demands
  $n^d \le 0$. It fails for every $K$. The slack must carry the extra log:
  guess $T(n) \le K n^d \log_b n$, whose step is
  $K n^d(\log_b n - 1) + n^d \le K n^d \log_b n \iff K \ge 1$; the base cases
  ($T(2) = a + 2^d$ with $\log_b 2 = 1$) force $K \ge 2$. Take $K = 2$.

So the pure-power guess succeeds iff $c \ne d$, and at $c = d$ the slack term is
a multiplicative $\log_b n$ rather than an additive constant.

**(c)** Neither is faster: both are $\Theta(n^3)$. The level ratio is $4$ and $2$
respectively — both greater than $1$, so in both cases the leaves dominate and
the level sum collapses onto them. Measured, the ratio between the two
recurrences tends to $3/2$ (or $3$ if you exclude the shared leaf term), a
**constant**, not a factor of $n$.

The intuition fails because "more work per node" only bites once the per-node
cost reaches the *leaf* cost $n^d$. Raising the local cost from $n$ to $n^2$
while $d = 3$ is still far below $n^3$, so it is invisible in the total; push
it to $n^4$ and you finally pay a factor of $n$. The boundary is $c = d$ — the
same boundary as (a) and (b).

**(d)** $T(n) = 2T(n/2) + \Theta(n \log n)$: the additive term is not
$\Theta(n^c)$ for any $c$, so the Master Theorem does not apply. Akra–Bazzi
gives $p$ from $2(1/2)^p = 1$, so $p = 1$, and

$$\Theta\left(n^1\left(1 + \int_1^n \frac{u \log u}{u^{2}}\,du\right)\right) = \Theta\left(n\left(1 + \int_1^n \frac{\log u}{u}\,du\right)\right) = \Theta\!\left(n(\log n)^2\right).$$

The FFT recurrence is $2T(n/2) + \Theta(n)$, which **does** fit the Master
Theorem at $c = d = 1$ and gives $\Theta(n \log n)$.

**What would break if you reused the FFT's answer?** Everything downstream,
and silently. The two differ by a full factor of $\log n$, which grows without
bound, so the error is not a constant you can absorb into a big-O: it changes
the complexity class from $n\log n$ to $n\log^2 n$. A prediction built on the
FFT answer would under-report the cost of a level of the transform by an
unbounded factor, and — because the two recurrences look almost identical on
the page — nothing in the code would complain. The single factor of $u$ in the
integrand is what does it: $\int_1^n \log u\,du$ grows like $n\log n$, while
$\int_1^n \frac{\log u}{u}\,du$ grows like $\tfrac12(\log n)^2$. Both
measured below, converging to $1$ and $1/2$ respectively.

```python
"""Challenge code block."""
import math
from math import log


def logb(x, b):
    return log(x) / log(b)


def classify(a, b, c):
    d = logb(a, b)
    if c < d - 1e-12:
        return d, 1, f"Theta(n^{d:.4f})"
    if abs(c - d) < 1e-12:
        return d, 2, f"Theta(n^{d:.4f} log n)"
    return d, 3, f"Theta(n^{c})"


def tree_cost(a, b, c, k):
    """T(2^k) for T(n) = a T(n/b) + n^c, by summing every LEVEL of the tree.

    Level i holds a^i nodes of size 2^(k-i), each doing (2^(k-i))^c work.
    The floor division is exact because n = 2^k.
    """
    total, nodes, m = 0, 1, 1 << k
    while m > 1:
        total += nodes * m ** c
        nodes *= a
        m //= b
    total += nodes          # the leaves
    return total


print("(a) c = d is exactly the regime where the per-level work is CONSTANT.")
print()
print("    Level i of the tree costs  a^i (n/b^i)^c = n^c (a / b^c)^i, so the")
print("    ratio between consecutive levels is a / b^c.  That ratio is 1")
print("    precisely when c = d = log_b a -- no term decays, none grows, and")
print("    the number of levels can no longer be absorbed into a geometric sum.")
print()
print(f"    {'recurrence':<20} {'c':>3} {'d':>8} {'a/b^c':>10} {'level ratio':>26} {'result':>22}")
for label, a, b, c in [("2T(n/2) + n", 2, 2, 1),
                       ("2T(n/2) + n^2", 2, 2, 2),
                       ("8T(n/2) + n", 8, 2, 1),
                       ("8T(n/2) + n^2", 8, 2, 2),
                       ("8T(n/2) + n^3", 8, 2, 3),
                       ("8T(n/2) + n^4", 8, 2, 4)]:
    d, case, res = classify(a, b, c)
    ratio = a / b ** c
    verdict = "CONSTANT" if abs(ratio - 1) < 1e-12 else ("growing" if ratio > 1 else "decaying")
    print(f"    {label:<20} {c:3d} {d:8.4f} {ratio:10.6f} {verdict:>26} {res:>22}")
print()
print("    Read the fifth row carefully: c = 3 and d = 3 are EQUAL, so the")
print("    level ratio is 1 and the answer is Theta(n^3 log n), not Theta(n^3).")
print("    Every other row has the ratio strictly off 1, so one term dominates")
print("    and the geometric sum collapses onto it.")
print()
print("    Measured on 8T(n/2) + n^3, a genuine c = d case.  Each level costs")
print("    exactly n^3, so with log2 n levels the total is n^3 log2 n + n^3:")
print(f"       {'k':>3} {'n = 2^k':>10} {'T(n)':>18} {'n^3 log2 n':>18} {'ratio':>9} {'(k+1)/k':>9}")
for k in range(3, 13):
    n = 1 << k
    t = tree_cost(8, 2, 3, k)
    exact = n ** 3 * k
    print(f"       {k:3d} {n:10d} {t:18d} {exact:18d} {t / exact:9.4f} {(k + 1) / k:9.4f}")
print()
print("    The ratio IS (k+1)/k and tends to 1 from above.  The excess is the")
print("    leaf term n^3 -- one extra level's worth -- which is lower order and")
print("    exactly what the substitution argument in (b) forces you to absorb.")
print()
print("(b) When does the pure-power guess work?  Guess T(n) <= K n^d.")
print()
print("    Step:  a K (n/b)^d + n^c <= K n^d")
print("      <=> n^c <= K n^d (1 - a/b^d).")
print("    At c = d we have a/b^d = 1, so the right side is 0 while the left")
print("    side is n^d.  The guess FAILS for every K: there is no slack left.")
print()
print("    The slack has to carry the extra log factor.  Guess T(n) <= K n^d log_b n.")
print("        a K (n/b)^d log_b(n/b) + n^d")
print("          = a K n^d b^-d (log_b n - 1) + n^d")
print("          = K n^d (log_b n - 1) + n^d            [since a / b^d = 1]")
print("          = K n^d log_b n - (K - 1) n^d")
print("        <= K n^d log_b n   iff   K >= 1.")
print("    Base cases: T(1) = 1 and T(2) = a + 2^d = 16, and log_b 2 = 1, so")
print("    16 <= K * 8 * 1 forces K >= 2.  Take K = 2; it satisfies both.")
print()
print("    Verified on 8T(n/2) + n^3 with the guess T(n) <= 2 n^3 log2 n:")
print(f"       {'n':>8} {'T(n)':>18} {'2 n^3 log2 n':>18} {'holds':>7} {'K needed':>10}")
for k in (3, 6, 9, 12, 15, 18):
    n = 1 << k
    t = tree_cost(8, 2, 3, k)
    print(f"       {n:8d} {t:18d} {2 * n ** 3 * k:18d} "
          f"{str(t <= 2 * n ** 3 * k):>7} {t / (n ** 3 * k):10.4f}")
print()
print("    So the pure-power guess succeeds iff c != d.  c < d is Case 1")
print("    (leaves win) and c > d is Case 3 (the root wins); both sit far from")
print("    the boundary, which is exactly why the three Master Theorem cases")
print("    are so easy to remember and so easy to get wrong by intuition.")
print()
print("(c) 8T(n/2) + n versus 8T(n/2) + n^2.  Same order: both Theta(n^3).")
print()
print("    Closed forms for n = 2^k, by summing the levels exactly:")
print("        level i costs 8^i (n/2^i)   = n 2^(2i)   -> internal sum (n^3 - n)/3")
print("        level i costs 8^i (n/2^i)^2 = n^2 2^i   -> internal sum n^3 - n^2")
print("        both then add the leaf term 8^k = n^3, so")
print("            T(n) = n^3 + (n^3 - n)/3 = (4n^3 - n)/3")
print("            T(n) = n^3 + (n^3 - n^2) = 2n^3 - n^2")
print()
print(f"       {'n':>8} {'8T(n/2)+n':>18} {'(4n^3-n)/3':>20} {'8T(n/2)+n^2':>18} {'2n^3-n^2':>20} {'ratio':>9}")
for k in (6, 10, 14, 18, 22):
    n = 1 << k
    t1 = tree_cost(8, 2, 1, k)
    t2 = tree_cost(8, 2, 2, k)
    print(f"       {n:8d} {t1:18d} {(4 * n ** 3 - n) / 3:20.1f} {t2:18d} "
          f"{2 * n ** 3 - n ** 2:20d} {t2 / t1:9.4f}")
print()
print("    The internal sums alone have ratio 3, but the leaves add the SAME")
print("    n^3 to both, which drags the overall ratio down to 3/2.  Either way")
print("    it is a CONSTANT, not a factor of n: both recurrences are Theta(n^3)")
print("    = 8^(log2 n), and the extra per-node n^2 cost is invisible because")
print("    the leaves already set the total.  The intuition that more work per")
print("    node must be slower only becomes true once the per-node cost")
print("    crosses the leaf cost, i.e. at c = 3:")
print(f"       {'n':>8} {'8T(n/2)+n^2':>16} {'8T(n/2)+n^3':>16} {'8T(n/2)+n^4':>16}")
for k in (10, 14, 18):
    n = 1 << k
    print(f"       {n:8d} {tree_cost(8, 2, 2, k):16d} {tree_cost(8, 2, 3, k):16d} "
          f"{tree_cost(8, 2, 4, k):16d}")
print()
print("    The n^4 column finally costs a factor of n over the n^3 column --")
print(f"    here 2n / log2 n, i.e. {2 * (1 << 18) / 18:.0f} at n = {1 << 18}.  That")
print("    is the boundary from (a), and it is why 'more work per node' is")
print("    wrong below the boundary and right above it.")
print()
print("(d) 2T(n/2) + Theta(n log n): the Master Theorem does not apply.")
print("    Akra-Bazzi: solve a_1 b_1^p = 1  ->  2 (1/2)^p = 1  ->  p = 1.")
print()
print("        T(n) = Theta( n^1 (1 + INT_1^n u log u / u^2 du ) )")
print("              = Theta( n (1 + INT_1^n log u / u du ) )")
print("              = Theta( n (1 + 0.5 (ln n)^2) )")
print("              = Theta(n (log n)^2)")
print()
print("    The FFT recurrence, by contrast, is 2T(n/2) + Theta(n), which DOES")
print("    fit the Master Theorem at c = d = 1.  Both, measured:")
print()
print(f"       {'n':>10} {'FFT: 2T+n':>16} {'n log2 n':>14} {'ratio':>8} "
      f"{'2T+n log n':>16} {'n log2^2 n':>16} {'ratio':>8}")
for k in (10, 14, 18, 22, 26):
    n = 1 << k
    fft = tree_cost(2, 2, 1, k)
    extra, nodes, m = 0, 1, n
    while m > 1:
        extra += nodes * m * math.log2(m)
        nodes *= 2
        m //= 2
    extra += nodes
    print(f"       {n:10d} {fft:16d} {n * k:14d} {fft / (n * k):8.4f} "
          f"{extra:16.0f} {n * k * k:16.0f} {extra / (n * k * k):8.4f}")
print()
print("    The first ratio tends to 1, not 2: every level costs exactly n, and")
print("    there are log2 n of them, so T = n log2 n + n.  The second tends to")
print("    0.5: level i costs n log2(n/2^i) = n (k-i), and sum (k-i) = k(k+1)/2,")
print("    so T = n k(k+1)/2 = (1/2) n (log2 n)^2 + lower order.")
print()
print("    One extra factor of log, and the difference is a single factor of u")
print("    in the integrand: INT log u du grows like n log n, but INT log u/u du")
print("    grows like (log n)^2.  Lesson 80 covers the first with the Master")
print("    Theorem and the second only with Akra-Bazzi -- which is the reason")
print("    the course teaches Akra-Bazzi at all.")
```

```text
(a) c = d is exactly the regime where the per-level work is CONSTANT.

    Level i of the tree costs  a^i (n/b^i)^c = n^c (a / b^c)^i, so the
    ratio between consecutive levels is a / b^c.  That ratio is 1
    precisely when c = d = log_b a -- no term decays, none grows, and
    the number of levels can no longer be absorbed into a geometric sum.

    recurrence             c        d      a/b^c                level ratio                 result
    2T(n/2) + n            1   1.0000   1.000000                   CONSTANT  Theta(n^1.0000 log n)
    2T(n/2) + n^2          2   1.0000   0.500000                   decaying             Theta(n^2)
    8T(n/2) + n            1   3.0000   4.000000                    growing        Theta(n^3.0000)
    8T(n/2) + n^2          2   3.0000   2.000000                    growing        Theta(n^3.0000)
    8T(n/2) + n^3          3   3.0000   1.000000                   CONSTANT  Theta(n^3.0000 log n)
    8T(n/2) + n^4          4   3.0000   0.500000                   decaying             Theta(n^4)

    Read the fifth row carefully: c = 3 and d = 3 are EQUAL, so the
    level ratio is 1 and the answer is Theta(n^3 log n), not Theta(n^3).
    Every other row has the ratio strictly off 1, so one term dominates
    and the geometric sum collapses onto it.

    Measured on 8T(n/2) + n^3, a genuine c = d case.  Each level costs
    exactly n^3, so with log2 n levels the total is n^3 log2 n + n^3:
         k    n = 2^k               T(n)         n^3 log2 n     ratio   (k+1)/k
         3          8               2048               1536    1.3333    1.3333
         4         16              20480              16384    1.2500    1.2500
         5         32             196608             163840    1.2000    1.2000
         6         64            1835008            1572864    1.1667    1.1667
         7        128           16777216           14680064    1.1429    1.1429
         8        256          150994944          134217728    1.1250    1.1250
         9        512         1342177280         1207959552    1.1111    1.1111
        10       1024        11811160064        10737418240    1.1000    1.1000
        11       2048       103079215104        94489280512    1.0909    1.0909
        12       4096       893353197568       824633720832    1.0833    1.0833

    The ratio IS (k+1)/k and tends to 1 from above.  The excess is the
    leaf term n^3 -- one extra level's worth -- which is lower order and
    exactly what the substitution argument in (b) forces you to absorb.

(b) When does the pure-power guess work?  Guess T(n) <= K n^d.

    Step:  a K (n/b)^d + n^c <= K n^d
      <=> n^c <= K n^d (1 - a/b^d).
    At c = d we have a/b^d = 1, so the right side is 0 while the left
    side is n^d.  The guess FAILS for every K: there is no slack left.

    The slack has to carry the extra log factor.  Guess T(n) <= K n^d log_b n.
        a K (n/b)^d log_b(n/b) + n^d
          = a K n^d b^-d (log_b n - 1) + n^d
          = K n^d (log_b n - 1) + n^d            [since a / b^d = 1]
          = K n^d log_b n - (K - 1) n^d
        <= K n^d log_b n   iff   K >= 1.
    Base cases: T(1) = 1 and T(2) = a + 2^d = 16, and log_b 2 = 1, so
    16 <= K * 8 * 1 forces K >= 2.  Take K = 2; it satisfies both.

    Verified on 8T(n/2) + n^3 with the guess T(n) <= 2 n^3 log2 n:
              n               T(n)       2 n^3 log2 n   holds   K needed
              8               2048               3072    True     1.3333
             64            1835008            3145728    True     1.1667
            512         1342177280         2415919104    True     1.1111
           4096       893353197568      1649267441664    True     1.0833
          32768    562949953421312   1055531162664960    True     1.0667
         262144 342273571680157696 648518346341351424    True     1.0556

    So the pure-power guess succeeds iff c != d.  c < d is Case 1
    (leaves win) and c > d is Case 3 (the root wins); both sit far from
    the boundary, which is exactly why the three Master Theorem cases
    are so easy to remember and so easy to get wrong by intuition.

(c) 8T(n/2) + n versus 8T(n/2) + n^2.  Same order: both Theta(n^3).

    Closed forms for n = 2^k, by summing the levels exactly:
        level i costs 8^i (n/2^i)   = n 2^(2i)   -> internal sum (n^3 - n)/3
        level i costs 8^i (n/2^i)^2 = n^2 2^i   -> internal sum n^3 - n^2
        both then add the leaf term 8^k = n^3, so
            T(n) = n^3 + (n^3 - n)/3 = (4n^3 - n)/3
            T(n) = n^3 + (n^3 - n^2) = 2n^3 - n^2

              n          8T(n/2)+n           (4n^3-n)/3        8T(n/2)+n^2             2n^3-n^2     ratio
             64             349504             349504.0             520192               520192    1.4884
           1024         1431655424         1431655424.0         2146435072           2146435072    1.4993
          16384      5864062009344      5864062009344.0      8795824586752        8795824586752    1.5000
         262144  24019198012555264  24019198012555264.0  36028728299487232    36028728299487232    1.5000
        4194304 98382635059782877184 98382635059782877184.0 147573934997490368512 147573934997490368512    1.5000

    The internal sums alone have ratio 3, but the leaves add the SAME
    n^3 to both, which drags the overall ratio down to 3/2.  Either way
    it is a CONSTANT, not a factor of n: both recurrences are Theta(n^3)
    = 8^(log2 n), and the extra per-node n^2 cost is invisible because
    the leaves already set the total.  The intuition that more work per
    node must be slower only becomes true once the per-node cost
    crosses the leaf cost, i.e. at c = 3:
              n      8T(n/2)+n^2      8T(n/2)+n^3      8T(n/2)+n^4
           1024       2146435072      11811160064    2197949513728
          16384    8795824586752   65970697666560 144110790029344768
         262144 36028728299487232 342273571680157696 9444714951340780945408

    The n^4 column finally costs a factor of n over the n^3 column --
    here 2n / log2 n, i.e. 29127 at n = 262144.  That
    is the boundary from (a), and it is why 'more work per node' is
    wrong below the boundary and right above it.

(d) 2T(n/2) + Theta(n log n): the Master Theorem does not apply.
    Akra-Bazzi: solve a_1 b_1^p = 1  ->  2 (1/2)^p = 1  ->  p = 1.

        T(n) = Theta( n^1 (1 + INT_1^n u log u / u^2 du ) )
              = Theta( n (1 + INT_1^n log u / u du ) )
              = Theta( n (1 + 0.5 (ln n)^2) )
              = Theta(n (log n)^2)

    The FFT recurrence, by contrast, is 2T(n/2) + Theta(n), which DOES
    fit the Master Theorem at c = d = 1.  Both, measured:

                n        FFT: 2T+n       n log2 n    ratio       2T+n log n       n log2^2 n    ratio
             1024            11264          10240   1.1000            57344           102400   0.5600
            16384           245760         229376   1.0714          1736704          3211264   0.5408
           262144          4980736        4718592   1.0556         45088768         84934656   0.5309
          4194304         96468992       92274688   1.0455       1065353216       2030043136   0.5248
         67108864       1811939328     1744830464   1.0385      23622320128      45365592064   0.5207

    The first ratio tends to 1, not 2: every level costs exactly n, and
    there are log2 n of them, so T = n log2 n + n.  The second tends to
    0.5: level i costs n log2(n/2^i) = n (k-i), and sum (k-i) = k(k+1)/2,
    so T = n k(k+1)/2 = (1/2) n (log2 n)^2 + lower order.

    One extra factor of log, and the difference is a single factor of u
    in the integrand: INT log u du grows like n log n, but INT log u/u du
    grows like (log n)^2.  Lesson 80 covers the first with the Master
    Theorem and the second only with Akra-Bazzi -- which is the reason
    the course teaches Akra-Bazzi at all.
```

</details>

---


---

## Summary

- Every recursive algorithm gives a recurrence, and the three tools for solving it
  — recursion tree (shape), substitution (constant), Master Theorem (class) —
  always agree; the pure guess $c\,n^d$ fails whenever the recursion saturates
  the budget, and the repair is a slack term $-\lambda n$.
- $T(n) = a\,T(n/b) + \Theta(n^c)$ with $d = \log_b a$: leaves dominate when
  $c < d$, every level ties when $c = d$, the top dominates when $c > d$.
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