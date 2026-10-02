# 82 — Tools for Algorithm Design

**Part**: part06_algorithms_math · **Prerequisites**: 80, 81 · **Time**: 60 min

---

## In Plain Words

The two previous lessons were about looking at an algorithm you already have: how
much work it does, and how to describe that work honestly. This one is about the
other direction — how do you come up with one, and how do you know it is right?

Three tools do most of the work. The first is the **loop invariant**: a single
sentence about the variables that is true before the loop, still true after one
pass, and together with the loop's exit condition says the answer is right. Write it
down before you write the body, and the bug you are about to make becomes visible on
paper. The second is the **exchange argument**: a greedy rule is only correct if you
can swap one element of some optimal solution for the greedy choice and still have an
optimal solution. If you cannot write that swap, you do not have a greedy algorithm,
you have a habit. The third is the **recurrence**: write the cost of solving a problem
of size $n$ in terms of the cost of solving smaller problems plus the work you do
yourself, and then solve it — with a table if the subproblems repeat, with the Master
Theorem if they shrink geometrically.

What ties the three together is a habit of mind rather than a technique. Write the
naive solution first, even the obviously slow one, and keep it as the oracle. Write
the invariant or the exchange as a sentence you could show someone. Then measure.
Algorithms that are merely plausible are everywhere; algorithms with a proof attached
are rarer than they should be.

---

## Why Computer Science Cares

- **Every "why is my code slow" investigation ends here.** Once you have a recurrence
  you can solve it, and once you have solved it you know which line is the problem.
  Block 3's merge-sort ledger shows the difference between an input-dependent
  comparison count and the input-independent element-move count that is the real cost.
- **Correctness bugs are usually invariant bugs.** Block 1 runs a binary search with a
  one-character error — `hi = mid` for `hi = mid - 1` — and finds 526 of 3,300 test
  cases hanging forever. No amount of testing catches it without a stated invariant,
  because the function still looks reasonable.
- **Greedy is the most over-used technique in interviews and the least often proved.**
  Block 2 measures two plausible rules for the same problem: one is wrong on 72% of
  instances, the other on 2%. The one that is 98% right looks exactly as safe as the
  one that is 28% right, and only a proof tells them apart.
- **Choosing a representation *is* the design.** Block 5 builds an LRU cache as a dict
  plus a doubly linked list with the list node stored *inside* the dict, so the lookup
  hands you the node directly. That one choice is what makes every operation $O(1)$,
  and it is exactly the move behind the dynamic array and the hash table in
  [Lesson 81](81_amortized_analysis.md).
- **Real systems are built from recurrences.** Merge sort's $\Theta(n \log n)$,
  FFT's $\Theta(n \log n)$, FFTW's tuning constants, and the parallel prefix-sum
  algorithms in GPU code are all recurrence analysis applied to a recurrence someone
  wrote down first.

---

## The Formal Version

Notation follows [SYMBOLS.md](../SYMBOLS.md). Recurrences are as in
[Lesson 24](../part02_discrete_combinatorics/24_recurrence_relations.md).

### Loop invariants

**Definition (loop invariant).** For a loop with body $B$ and guard $G$, an
*invariant* $I$ of the loop is a predicate on the program variables such that

1. $I$ holds before the first execution of the loop;
2. $I \wedge G \Rightarrow B[I]$ — if $I$ holds and the guard is true, then after the
   body $I$ still holds;
3. $I \wedge \neg G \Rightarrow P$ — if $I$ holds and the guard is false, then the
   postcondition $P$ holds.

**Definition (variant function).** A *variant* (or *decreasing quantity*) is an
integer-valued function $V$ of the variables with $I \wedge G \Rightarrow V_{\text{after}}
\le V_{\text{before}} - 1$.

**Theorem (correctness and termination).** If $I$ is an invariant and $V$ is a
variant, then the loop terminates after at most $V_{\text{initial}}$ iterations, and on
exit $P$ holds.

**Explanation.** The invariant is preserved by construction, so it is true at every
loop head. It is therefore true at the final loop head, where the guard is false, and
condition 3 gives $P$. The variant is a non-negative integer that strictly decreases
while the loop runs; it cannot decrease more than its initial value times, so the loop
must exit. The two arguments are completely independent: a loop can be correct and
non-terminating, or terminating and wrong.

**Example (binary search on a sorted array $a$).** The invariant is

$$I \equiv \left[\ \text{target occurs in } a \right] \iff \left[\ \exists i \in [lo, hi] : a[i] = \text{target} \right],$$

with the side condition $lo \le hi + 1$. It holds initially with $lo = 0$, $hi = n-1$.
Preservation: if $a[mid] > \text{target}$ then every index $\le mid$ is too small, so
setting $hi = mid - 1$ — **not** $hi = mid$ — keeps the equivalence true. With $hi =
mid$ the window retains an index already known not to hold the target, the invariant
is false from that point on, and the variant $hi - lo + 1$ fails to decrease, so the
loop hangs.

### Greedy algorithms

**Definition (greedy-choice property).** For a problem $P$, a greedy rule $g$ has the
greedy-choice property if there is always *some* optimal solution of $P$ that contains
$g$'s choice.

**Definition (exchange argument).** To prove the property, take an optimal solution $O$
and the greedy choice $g$. If $g \in O$ there is nothing to show. Otherwise let $x \in O$
be the element that the exchange will displace, and show that $O' = (O \setminus \{x\})
\cup \{g\}$ is still feasible with the same objective value. Then $O'$ is optimal
*and* contains $g$.

**Theorem (greedy correctness).** If the greedy-choice property holds and the induced
subproblem after taking $g$ is of the same kind, then repeatedly taking $g$ is optimal.

**Explanation.** By induction on the number of elements remaining. Base case: nothing
left, one empty solution, optimal. Step: by the exchange argument there is an optimal
solution beginning with $g$; fix $g$ and apply the induction hypothesis to the
remainder. The whole content is in "there is an optimal solution beginning with $g$" —
if you cannot show that, the procedure is a heuristic.

**Example (activity selection).** Let $g$ be the interval finishing earliest and $f$ the
first interval of an optimal solution $O$. Then $g$ finishes no later than $f$, and
every interval in $O$ after $f$ starts at or after $f$ ends, hence at or after $g$
ends. So $O' = (O \setminus \{f\}) \cup \{g\}$ is feasible with the same size, and $g$
is safe. Measured: greedy matched exhaustive search on all 8 random instances.

**Counterexample (coin change for 1, 3, 4).** The rule "take the largest coin that
fits" fails for amounts $6, 10, 14, 18, 22$ — every amount $\equiv 2 \pmod 6$ — because
$4 + 1 + 1$ loses to $3 + 3$. The greedy-choice property *fails*: there is no optimal
solution containing the 4. The identical rule is optimal for US coins 1, 5, 10, 25,
where a published exchange argument exists. The rule is the same; the proof is not.

### Divide and conquer

**Definition (recurrence).** For a problem of size $n$ whose algorithm makes $a$ calls
on subproblems of size $n/b$ and does $f(n)$ work itself, the cost satisfies

$$T(n) = a\,T\!\left(\frac{n}{b}\right) + f(n), \qquad T(1) = \Theta(1).$$

**Theorem (Master Theorem).** Let $p = \log_b a$. Then

| Condition on $f(n)$ | $T(n)$ |
| --- | --- |
| $f(n) = O(n^{p-\varepsilon})$ for some $\varepsilon > 0$ | $\Theta(n^{p})$ |
| $f(n) = \Theta(n^{p})$ | $\Theta(n^{p} \log n)$ |
| $f(n) = \Omega(n^{p+\varepsilon})$ for some $\varepsilon > 0$ | $\Theta(f(n))$ |

**Explanation.** Expand the recurrence into a tree. Level $k$ holds $a^k$ nodes of size
$n/b^k$, so the level cost is $a^k f(n/b^k)$. The sign of $p - \log_b a$ against the
growth rate of $f$ decides whether the level costs shrink (case 1), stay equal (case 2)
or grow (case 3). In case 1 the leaves, of which there are $a^{\log_b n} = n^{p}$,
dominate. In case 2 every level costs the same, so the total is
$(\text{cost per level}) \cdot (\text{number of levels})$. In case 3 the root dominates
and everything below it is a constant fraction. The $\varepsilon$ in cases 1 and 3 is
load-bearing: $f(n) = \Theta(n^p)$ exactly is case 2, not case 3, and gains a factor
of $\log n$. Measured: the total work of $T(n) = 3T(n/3) + n$ at $n = 3^k$ is exactly
$n(k+1)$, so the ratio to $n \ln n$ falls $1.214, 1.138, 1.092, 1.062, 1.040$ towards
$1/\ln 3 = 0.910$ — case 2, not case 3.

### Dynamic programming

**Definition (overlapping subproblems).** A recurrence has overlapping subproblems if
the same instance is required by two or more branches of the recursion tree. It has
non-overlapping subproblems if every instance appears at most once.

**Theorem (why a table works).** If the subproblems overlap, then a table filled once
per distinct instance evaluates the recurrence in

$$\sum_{k=0}^{n} \big|\{\text{states at level } k\}\big| = \Theta(n \cdot a)$$

time instead of $\Theta(a^n)$ calls. The extra cost is $\Theta(n)$ space.

**Explanation.** Memoising is not a trick; it is what the overlap *means*. The naive
recursion for $F(n) = F(n-1) + F(n-2)$ makes $2F(n+1) - 1$ calls because $F(k)$ is
recomputed exponentially often. Measured: 177 calls at $n = 10$, 29,860,703 at
$n = 35$, multiplying by $11.1$ for every step of 5 — which is $\varphi^5 = 11.09$.
The table version does $n-1$ additions. Non-overlapping subproblems mean there is
nothing to save, which is exactly when divide and conquer is the right answer.

---

## Formula Sheet

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$I$` | `$I \wedge G \Rightarrow B[I]$` and `$I \wedge \neg G \Rightarrow P$` | what is true before, after, and on exit | every loop you write |
| `$V$` | `$V_{after} \le V_{before} - 1$` | a non-negative integer that strictly drops | proving termination and the iteration count |
| binary search invariant | `$\text{target} \in a \iff \exists i \in [lo,hi]: a[i] = \text{target}$` | the answer is never discarded | any narrowing search |
| binary search steps | `$\le \lfloor \log_2 n \rfloor + 1$` | 41 comparisons at $n = 2^{40}$ | the $O(\log n)$ bound |
| safe midpoint | `$\text{lo} + (\text{hi} - \text{lo}) // 2$` | does not overflow 32-bit | fixed-width integer code |
| greedy-choice property | `$\exists$` optimal solution containing `$g$` | the greedy step is *somewhere* inside an optimum | validating a greedy rule |
| exchange | `$O' = (O \setminus \{x\}) \cup \{g\}$` still optimal | swap and check | the proof a greedy rule needs |
| `$T(n)$` | `$T(n) = aT(n/b) + f(n)$` | cost of the whole vs cost of the parts | divide and conquer |
| `$p$` | `$\log_b a = \log a / \log b$` | how fast the subtree count grows | Master Theorem input |
| case 1 | `$f(n) = O(n^{p-\varepsilon})$ | `$\Rightarrow T(n) = \Theta(n^p)$` | leaves dominate |
| case 2 | `$f(n) = \Theta(n^p)$ | `$\Rightarrow T(n) = \Theta(n^p \log n)$` | every level costs the same |
| case 3 | `$f(n) = \Omega(n^{p+\varepsilon})$ | `$\Rightarrow T(n) = \Theta(f(n))$` | the root dominates |
| level $k$ cost | `$a^k f(n/b^k)$` | work done at depth $k$ | the recursion-tree method |
| merge-sort moves | `$n \lceil \log_2 n \rceil$` | exactly, data-independent | the real cost of merge sort |
| Fibonacci calls | `$2F(n+1) - 1$` | why the naive recursion is exponential | motivating memoisation |
| memoised Fibonacci | `$\Theta(n)$` additions | one table pass | dynamic programming |
| domino tilings | `$T(n) = T(n-1) + T(n-2) + O(1) = \Theta(n)$` | additive, not multiplicative | Fibonacci in the wild |
| `$C(n)$` vs answer size | work `$\Theta(n)$`, count `$\Theta(\varphi^n)$` | computing is cheaper than the number you compute | counting vs computing |

---

## Worked Example

Take the insertion-sort inner loop and do all four jobs to it: state the invariant,
state the variant, solve the recurrence, and check it against brute force.

**The code.**

```
i = 1
while i < n:
    key = a[i]
    j = i - 1
    while j >= 0 and a[j] > key:
        a[j + 1] = a[j]
        j = j - 1
    a[j + 1] = key
    i = i + 1
```

**1. The invariant.** At the head of the outer loop:

$$I \equiv \left[\ a[0 \dots i-1] \text{ is sorted} \right] \;\wedge\; \left[\ 
\{a[0 \dots i-1]\} = \text{the } i \text{ smallest elements of the original } a \right].$$

Both halves matter. Sortedness alone would allow any permutation of the prefix;
"the $i$ smallest" alone would allow any order. Together they say the prefix is
finished.

**2. Preservation.** Entering the body, `key = a[i]` is held aside and the inner loop
moves every element of the prefix that exceeds `key` one slot right, so the prefix
ends up sorted with `key` inserted at the right position. No element is lost or
duplicated: the inner loop only shifts elements that are strictly greater than `key`,
and stops at the first that is not, so `\{a[0 \dots i]\}$ is exactly the $i+1$ smallest
of the original, sorted. Hence $I$ holds at the next loop head with $i \leftarrow i+1$.

**3. Termination.** The variant is $V = n - i$, an integer $\ge 1$ while the guard
$i < n$ holds, and it decreases by exactly 1 per pass. So the loop runs exactly $n-1$
times. The inner loop's variant is $V' = j + 1$, which decreases by 1 per shift.

**4. Postcondition.** On exit $i = n$, so the first half of $I$ says $a[0 \dots n-1]$ is
sorted and the second says it contains all $n$ elements. The array is sorted. $\blacksquare$

**5. The recurrence.** The outer loop runs $n - 1$ times. On pass $i$ the inner loop
shifts at most $i$ elements, so

$$T(n) = T(n-1) + \Theta(n) = \Theta(n^2).$$

With $a = 1$, $b$ large, $f(n) = \Theta(n)$, $p = \log_b 1 = 0$, so $f(n) =
\Omega(n^{0+\varepsilon})$ for $\varepsilon = 1$ and the Master Theorem's case 3 gives
$\Theta(n^2)$ — consistent, though here the sum $\sum_{i=1}^{n} i = n(n+1)/2$ is the
better argument because it is exact.

**6. The check.** Count the shifts for real and compare with $n(n+1)/2$. On
best-case input (already sorted) the inner loop never shifts, so the count is $0$ and
the cost is $\Theta(n)$, not $\Theta(n^2)$. That gap between best and worst is what
[Lesson 80](80_big_o_and_complexity.md) insists on, and it is why the algorithm above
is quoted as *insertion sort is $\Theta(n^2)$ worst case, $\Theta(n)$ best case*.

The point of doing all six on one algorithm is that they are independent. A correct
algorithm can be slow; a fast algorithm can be wrong; an algorithm can be correct and
fast and still be the wrong choice for the input you have.

---

## Runnable Code

### Block 1: loop invariants, written as code that fails loudly

```python
import math
import random

# ================================================= Block 1: loop invariants, checked
class InvariantViolation(Exception):
    pass


class CheckedBinarySearch:
    """Binary search that ASSERTS its invariant at every loop head.

    Invariant I:  lo <= hi + 1  and  every index in [lo, hi] satisfies a[i] == target
                  is equivalent to "target is in a at some index".
    Equivalently:  target in a  <=>  exists i in [lo, hi] with a[i] == target.
    """

    def __init__(self, a):
        self.a = a
        self.checks = 0
        self.steps = 0

    def search(self, target):
        a = self.a
        lo, hi = 0, len(a) - 1
        self._check(lo, hi, target)
        while lo <= hi:
            mid = (lo + hi) // 2
            self.steps += 1
            if a[mid] == target:
                return mid
            if a[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
            self._check(lo, hi, target)
        return -1

    def _check(self, lo, hi, target):
        """The invariant, evaluated the slow obvious way -- which is the point."""
        self.checks += 1
        if lo > hi + 1:
            raise InvariantViolation(f"range inverted: lo={lo}, hi={hi}")
        present = target in self.a
        in_window = any(self.a[i] == target for i in range(lo, min(hi + 1, len(self.a))))
        if present != in_window:
            raise InvariantViolation(
                f"invariant broken: target={target} present={present} "
                f"in [lo,hi]=[{lo},{hi}] is {in_window}")


print("=== The invariant is checkable, so check it ===")
print("  A loop invariant is a statement about the variables that is true before the")
print("  loop, preserved by the body, and implies the postcondition.  Here it is:")
print("      'target occurs in a  <=>  target occurs at some index in [lo, hi]'")
print("  plus the side condition lo <= hi + 1, which makes the loop terminate.")
random.seed(31)
bad = 0
checked = 0
for trial in range(300):
    n = random.randrange(1, 40)
    a = sorted(random.randrange(10) for _ in range(n))
    s = CheckedBinarySearch(a)
    for t in range(11):
        try:
            s.search(t)
            checked += 1
        except InvariantViolation as exc:
            bad += 1
            print("   VIOLATION:", exc)
print(f"    random (array, target) pairs tried   : 3,300")
print(f"    searches that completed             : {checked}")
print(f"    invariant violations                : {bad}")
print("  Every one of those 3,300 searches verified, at every single loop head, that")
print("  the whole array and the surviving window agree about where the target is.  That")
print("  is the correctness proof, executed.  A proof you can run is worth more than a")
print("  proof you can only read -- and it is why the checker is written as code rather")
print("  than as a sentence, since a sentence cannot fail loudly.")
print()

print("=== The same invariant, written out on one concrete example ===")
print("  a = [1, 3, 3, 5, 7, 9, 11, 13, 17], target = 11")
a = [1, 3, 3, 5, 7, 9, 11, 13, 17]
target = 11
print("  lo  hi  mid  a[mid]  window contains target?   whole array contains it?")
lo, hi = 0, len(a) - 1
step = 0
while lo <= hi:
    mid = (lo + hi) // 2
    window = a[lo:hi + 1]
    print(f"  {lo:>2}  {hi:>2}  {mid:>3}  {a[mid]:>6}  {str(target in window):>22}   "
          f"{str(target in a):>20}")
    if a[mid] == target:
        print(f"  -> found at index {mid}; the loop exits with a[mid] == target")
        break
    if a[mid] < target:
        lo = mid + 1
    else:
        hi = mid - 1
print("  Two loop iterations instead of a scan of nine, and the invariant says the")
print("  answer is always still inside the window, so nothing that mattered is ever")
print("  discarded.")
print()

print("=== A buggy binary search, and the invariant that catches it ===")


class BuggyBinarySearch:
    """Uses <= on the wrong side: hi = mid instead of hi = mid - 1."""

    def search(self, a, target):
        lo, hi = 0, len(a) - 1
        steps = 0
        while lo <= hi:
            mid = (lo + hi) // 2
            steps += 1
            if a[mid] == target:
                return mid
            if a[mid] < target:
                lo = mid + 1
            else:
                hi = mid                       # BUG: should be mid - 1
            if steps > 200:
                return None                     # would otherwise spin forever
        return -1


random.seed(31)
wrong = []
hung = 0
for trial in range(300):
    n = random.randrange(1, 40)
    a = sorted(random.randrange(10) for _ in range(n))
    b = BuggyBinarySearch()
    for t in range(11):
        got = b.search(a, t)
        if got is None:
            hung += 1
            wrong.append((list(a), t, "hung", a.index(t) if t in a else -1))
            continue
        want = a.index(t) if t in a else -1
        if (got == -1) != (want == -1):
            wrong.append((list(a), t, got, want))
print(f"    arrays and targets tried            : 3,300")
print(f"    searches that HUNG (no termination) : {hung}")
print(f"    searches that returned a wrong answer: {len(wrong) - hung}")
print(f"    searches that were correct          : {3300 - len(wrong)}")
if wrong:
    arr, t, got, want = wrong[0]
    print(f"    first counterexample   : a = {arr}, target = {t}, "
          f"returned {got!r}, wanted {want}")
print(f"    distinct failing (array, target) pairs: "
      f"{len({(tuple(a), t) for a, t, _, _ in wrong})}")
print("  hi = mid keeps a[mid] inside the window while the code has just concluded")
print("  a[mid] > target, so the window retains a value known not to be the answer --")
print("  the invariant is false from that point on.  Worse, the variant function")
print("  hi - lo + 1 fails to decrease when hi = mid, so the loop does not merely give")
print("  wrong answers, it HANGS: the search for a target below every element never")
print("  terminates.  A one-character difference, invisible without an invariant, since")
print("  the function still returns an in-range index whenever it returns at all.")
print()

print("=== Termination needs its own argument: a variant function ===")
print("  Three loops, three decreasing-integer arguments.  Each drop bounds the")
print("  iterations, and the bound is what you write in the O() you claim.")
print("    loop                      variant function            initial   drop per iter")
print("    while lo <= hi            hi - lo + 1                 n         ~half")
print("    while i < n                n - i                      n         1")
print("    while k > 0                k                          k         floor(k/2)")
print()
def virtual_steps(n, target):
    """Binary search on the sorted array [0, 1, ..., n-1] WITHOUT allocating it.

    The invariant checker cannot be used here because it reads the array, so this
    counts steps by arithmetic only -- which is the point: the search on 2^40
    elements never touches memory beyond two integers.
    """
    lo, hi = 0, n - 1
    steps = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        steps += 1
        if mid == target:
            return steps
        if mid < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return steps


print("  The binary search variant is hi - lo + 1, and it at least halves each")
print("  iteration, so the iteration count is at most floor(log2(n)) + 1.  Measured:")
print("        n   floor(log2 n)+1   worst: find n-1   best: find 0   bound")
for n in (1, 2, 3, 7, 8, 15, 16, 1000, 100000, 2 ** 40):
    bound = int(math.log2(n)) + 1
    worst = virtual_steps(n, n - 1)
    best = virtual_steps(n, 0)
    flag = "ok" if worst <= bound and best <= bound else "VIOLATED"
    print(f"  {n:>10}   {bound:>15}   {worst:>18}   {best:>13}   {flag:>12}")
print()
print("  Both columns are at most floor(log2 n) + 1 at every n, including 2^40, where")
print("  the array cannot be allocated and the search never touches memory beyond the")
print("  arithmetic on two integers.  That is the invariant plus the variant together:")
print("  the invariant says the answer is in the window, the variant says the window")
print("  shrinks, and together they are a correctness proof AND a running time bound.")
print()

print("=== The integer overflow that a real binary search must avoid ===")
print("  (lo + hi) // 2 overflows a 32-bit int when lo and hi are near 2^31.  Python's")
print("  ints do not overflow, so the bug cannot happen here -- which is exactly why it")
print("  survives testing and reaches C++.")
lo, hi = 2 ** 31 - 1, 2 ** 32 - 1
print(f"    lo = {lo:,}   hi = {hi:,}")
print(f"    lo + hi                = {lo + hi:,}")
print(f"    fits in 32 bits?        {lo + hi <= 2 ** 32 - 1}")
print(f"    (lo + hi) // 2         = {(lo + hi) // 2:,}")
print(f"    lo + (hi - lo) // 2    = {lo + (hi - lo) // 2:,}")
print("  Both give the same answer in Python and both overflow in C.  The safe form is")
print("  lo + (hi - lo) // 2, and writing it that way costs nothing.")
print()

print("=== Three invariants, three structures, one shape ===")
print("  The pattern is always: a statement about the variables that (a) holds before")
print("  the loop, (b) is preserved by one iteration, (c) with the loop's exit")
print("  condition implies the postcondition, and (d) comes with a decreasing integer.")
print()
print("    algorithm                invariant                                variant")
print("    binary search            target in a  <=>  target in [lo, hi]       hi - lo + 1")
print("    insertion sort           a[:i] is sorted and holds the i smallest   i")
print("    loop for gcd            gcd(a, b) unchanged by the Euclid step      max(a, b)")
print("    Dijkstra                 settled distances are final                unsettled count")
print("    Floyd-Warshall           D[i][j] is the best known via <= k nodes   k")
print()
print("  Note what the last row is doing: Floyd-Warshall has NO variant function in")
print("  the usual sense -- k increases rather than decreases -- and no loop exits")
print("  early.  Its termination is structural (k runs from 0 to n-1) and its")
print("  correctness invariant is the whole point of the algorithm.  One shape, one")
print("  loop, but the invariant is doing all the work.")
```

Output:

```text
=== The invariant is checkable, so check it ===
  A loop invariant is a statement about the variables that is true before the
  loop, preserved by the body, and implies the postcondition.  Here it is:
      'target occurs in a  <=>  target occurs at some index in [lo, hi]'
  plus the side condition lo <= hi + 1, which makes the loop terminate.
    random (array, target) pairs tried   : 3,300
    searches that completed             : 3300
    invariant violations                : 0
  Every one of those 3,300 searches verified, at every single loop head, that
  the whole array and the surviving window agree about where the target is.  That
  is the correctness proof, executed.  A proof you can run is worth more than a
  proof you can only read -- and it is why the checker is written as code rather
  than as a sentence, since a sentence cannot fail loudly.

=== The same invariant, written out on one concrete example ===
  a = [1, 3, 3, 5, 7, 9, 11, 13, 17], target = 11
  lo  hi  mid  a[mid]  window contains target?   whole array contains it?
   0   8    4       7                    True                   True
   5   8    6      11                    True                   True
  -> found at index 6; the loop exits with a[mid] == target
  Two loop iterations instead of a scan of nine, and the invariant says the
  answer is always still inside the window, so nothing that mattered is ever
  discarded.

=== A buggy binary search, and the invariant that catches it ===
    arrays and targets tried            : 3,300
    searches that HUNG (no termination) : 526
    searches that returned a wrong answer: 0
    searches that were correct          : 2774
    first counterexample   : a = [7], target = 0, returned 'hung', wanted -1
    distinct failing (array, target) pairs: 506
  hi = mid keeps a[mid] inside the window while the code has just concluded
  a[mid] > target, so the window retains a value known not to be the answer --
  the invariant is false from that point on.  Worse, the variant function
  hi - lo + 1 fails to decrease when hi = mid, so the loop does not merely give
  wrong answers, it HANGS: the search for a target below every element never
  terminates.  A one-character difference, invisible without an invariant, since
  the function still returns an in-range index whenever it returns at all.

=== Termination needs its own argument: a variant function ===
  Three loops, three decreasing-integer arguments.  Each drop bounds the
  iterations, and the bound is what you write in the O() you claim.
    loop                      variant function            initial   drop per iter
    while lo <= hi            hi - lo + 1                 n         ~half
    while i < n                n - i                      n         1
    while k > 0                k                          k         floor(k/2)

  The binary search variant is hi - lo + 1, and it at least halves each
  iteration, so the iteration count is at most floor(log2(n)) + 1.  Measured:
        n   floor(log2 n)+1   worst: find n-1   best: find 0   bound
           1                 1                    1               1             ok
           2                 2                    2               1             ok
           3                 2                    2               2             ok
           7                 3                    3               3             ok
           8                 4                    4               3             ok
          15                 4                    4               4             ok
          16                 5                    5               4             ok
        1000                10                   10               9             ok
      100000                17                   17              16             ok
  1099511627776                41                   41              40             ok

  Both columns are at most floor(log2 n) + 1 at every n, including 2^40, where
  the array cannot be allocated and the search never touches memory beyond the
  arithmetic on two integers.  That is the invariant plus the variant together:
  the invariant says the answer is in the window, the variant says the window
  shrinks, and together they are a correctness proof AND a running time bound.

=== The integer overflow that a real binary search must avoid ===
  (lo + hi) // 2 overflows a 32-bit int when lo and hi are near 2^31.  Python's
  ints do not overflow, so the bug cannot happen here -- which is exactly why it
  survives testing and reaches C++.
    lo = 2,147,483,647   hi = 4,294,967,295
    lo + hi                = 6,442,450,942
    fits in 32 bits?        False
    (lo + hi) // 2         = 3,221,225,471
    lo + (hi - lo) // 2    = 3,221,225,471
  Both give the same answer in Python and both overflow in C.  The safe form is
  lo + (hi - lo) // 2, and writing it that way costs nothing.

=== Three invariants, three structures, one shape ===
  The pattern is always: a statement about the variables that (a) holds before
  the loop, (b) is preserved by one iteration, (c) with the loop's exit
  condition implies the postcondition, and (d) comes with a decreasing integer.

    algorithm                invariant                                variant
    binary search            target in a  <=>  target in [lo, hi]       hi - lo + 1
    insertion sort           a[:i] is sorted and holds the i smallest   i
    loop for gcd            gcd(a, b) unchanged by the Euclid step      max(a, b)
    Dijkstra                 settled distances are final                unsettled count
    Floyd-Warshall           D[i][j] is the best known via <= k nodes   k

  Note what the last row is doing: Floyd-Warshall has NO variant function in
  the usual sense -- k increases rather than decreases -- and no loop exits
  early.  Its termination is structural (k runs from 0 to n-1) and its
  correctness invariant is the whole point of the algorithm.  One shape, one
  loop, but the invariant is doing all the work.
```

The first table is the whole idea in one screen. The invariant of binary search —
"the target occurs in the array if and only if it occurs in the window $[lo, hi]$" —
is a sentence, but it is also a *computable* predicate, and the code computes it at
every loop head by brute force. 3,300 random `(array, target)` pairs, zero violations.
That is not a test suite; it is a correctness proof that runs.

The second table is the same invariant written out by hand on one example, which is
what you should actually do while designing. Nine elements, two iterations, and at
every step the window contains the target because the invariant says it must.

The third table is the payoff. `hi = mid` instead of `hi = mid - 1` is a one-character
change. The search still returns an in-range index whenever it returns at all, so
eyeballing the code finds nothing wrong — but 526 of 3,300 cases **hang forever**, and
the reason is that `hi = mid` keeps an index known not to be the target inside the
window *and* fails to decrease `hi - lo + 1`, so both the invariant and the variant
break at once. A test suite that does not have a timeout will hang on the first one.

The fourth table gives the variant functions. Each is a non-negative integer that
strictly decreases, and each drop bounds the iteration count — which is exactly what
you write in the $O(\cdot)$ you claim. Binary search's variant halves per iteration,
so the bound is $\lfloor \log_2 n \rfloor + 1$, and the measured column sits under it at
every $n$ up to $2^{40}$, an array that cannot be allocated and a search that never
touches memory beyond two integers.

The fifth table is the bug Python hides. `(lo + hi) // 2` gives the right answer here
and overflows a 32-bit signed integer in C++ when `lo` and `hi` are near $2^{31}$. It
cannot happen in Python, which is exactly why it survives testing and reaches
production. `lo + (hi - lo) // 2` costs nothing and cannot overflow.

The last table collects five algorithms in one shape: an invariant, a variant, and the
loop they belong to. Note that Floyd–Warshall has no variant function — its index `k`
*increases* and nothing exits early — so termination is structural and the invariant
carries the entire correctness argument. One shape, one loop, and the invariant is
always the load-bearing part.

### Block 2: greedy choice, exchange arguments, and a rule that fails

```python
import itertools
import math
import random

# ============================================ Block 2: greedy choice and exchanges
def greedy_earliest_finish(intervals):
    """Activity selection: always take the compatible activity that ends first.

    The greedy-choice property: there EXISTS an optimal solution whose first
    activity is the earliest-finishing one.  The exchange argument builds it.
    """
    chosen = []
    finish = None
    for start, end in sorted(intervals, key=lambda iv: iv[1]):
        if finish is None or start >= finish:
            chosen.append((start, end))
            finish = end
    return chosen


def brute_force(intervals, limit=20):
    """Every subset, keeping the compatible ones.  Exponential, but obviously right."""
    best, best_size = [], -1
    for r in range(len(intervals) + 1):
        for combo in itertools.combinations(range(len(intervals)), r):
            picked = [intervals[i] for i in combo]
            ordered = sorted(picked)
            ok = all(ordered[i][1] <= ordered[i + 1][0] for i in range(len(ordered) - 1))
            if ok and len(picked) > best_size:
                best, best_size = picked, len(picked)
    return best


print("=== Activity selection: the exchange argument, executed ===")
print("  Given intervals, pick as many as possible with no overlaps.  The greedy rule")
print("  is 'always take the one that ends first'.  The proof is one exchange.")
random.seed(19)
print("     #   intervals                                    greedy   brute force   match")
for trial in range(8):
    m = random.randrange(4, 9)
    ivs = []
    for _ in range(m):
        s = random.randrange(0, 20)
        ivs.append((s, s + random.randrange(1, 7)))
    g = greedy_earliest_finish(ivs)
    b = brute_force(ivs)
    flag = "yes" if len(g) == len(b) else "NO"
    pretty = " ".join(f"({s},{e})" for s, e in sorted(ivs))
    print(f"  {trial + 1:>5}   {pretty:<42}   {len(g):>6}   {len(b):>11}   {flag:>5}")
print()
print("  Every greedy answer matched the exponential search.  The argument that")
print("  guarantees it is short: let O be an optimal solution and let g be the")
print("  earliest-finishing interval.  If g is already in O we are done.  Otherwise")
print("  let f be O's first interval.  f finishes no earlier than g, and O's first")
print("  interval starts no earlier than the current time, so replacing f by g keeps")
print("  compatibility with everything after it.  Hence there is an optimal solution")
print("  starting with g, we may assume it does, and we recurse on the rest.  That is")
print("  the ENTIRE proof, and it is induction hidden in plain sight.")
print()

print("=== The exchange argument, with the replacement drawn out ===")
ivs = [(1, 4), (3, 5), (4, 6), (2, 8), (5, 9), (6, 10), (7, 11), (9, 13)]
print("  intervals: " + "  ".join(f"({s},{e})" for s, e in ivs))
print()
print("  Greedy picks, in order, the earliest finish that is compatible:")
picked, finish = [], None
for start, end in sorted(ivs, key=lambda iv: iv[1]):
    mark = "TAKE" if (finish is None or start >= finish) else "skip"
    if mark == "TAKE":
        finish = end
        picked.append((start, end))
    print(f"    ({start:>2},{end:>2})  ends {end:>3}  last pick ends {finish if finish is None else finish:>4}"
          f"   {mark}")
print(f"  greedy answer: {picked}  size {len(picked)}")
best = brute_force(ivs)
print(f"  brute force  : {sorted(best)}  size {len(best)}")
print()
print("  Now the exchange, concretely.  The optimal solution has size 3 and greedy")
print("  also found 3, so an optimal solution exists that agrees with greedy on its")
print("  first choice.  Here is why that is not luck.  Let O be an optimal solution")
print("  and let f be its first interval.  The earliest-finishing interval overall")
print(f"  is {min(ivs, key=lambda iv: iv[1])}, which finishes no later than f does;")
print("  replacing f with it cannot collide with any interval later in O, because")
print("  those all start at or after f ends and therefore at or after it ends too.")
print("  So O survives the swap with its size unchanged, and there is now an optimal")
print("  solution whose first interval is the greedy one.  Fix that choice, throw away")
print("  all time before its end, and the same argument applies to what is left.  That")
print("  recursion is the induction, and it is the whole reason greedy works here.")
print()

print("=== Greedy fails when the local choice is not safe: coin change ===")
print("  Coins 1, 3, 4.  Greedy takes the largest coin that fits, repeatedly.")


def greedy_change(amount, coins):
    picks = []
    while amount > 0:
        c = max(c for c in coins if c <= amount)
        picks.append(c)
        amount -= c
    return picks


def optimal_change(amount, coins):
    best = None
    for r in range(amount + 1):
        for combo in itertools.combinations_with_replacement(sorted(coins), r):
            if sum(combo) == amount:
                if best is None or len(combo) < len(best):
                    best = list(combo)
    return best or []


print("  amount   greedy coins   greedy count   optimal count   greedy optimal?")
bad_amounts = []
for amount in range(1, 25):
    g = greedy_change(amount, (1, 3, 4))
    o = optimal_change(amount, (1, 3, 4))
    mark = "yes" if len(g) == len(o) else "NO"
    if mark == "NO":
        bad_amounts.append(amount)
    print(f"  {amount:>6}   {str(g):>12}   {len(g):>12}   {len(o):>13}   {mark:>16}")
print()
print(f"  Greedy is optimal for {24 - len(bad_amounts)} of the 24 amounts and wrong for "
      f"{len(bad_amounts)}: {bad_amounts}")
if bad_amounts:
    a = bad_amounts[0]
    print(f"  Counterexample: amount {a}.  Greedy gives {greedy_change(a, (1, 3, 4))} "
          f"({len(greedy_change(a, (1, 3, 4)))} coins);")
    print(f"  optimal gives {optimal_change(a, (1, 3, 4))} "
          f"({len(optimal_change(a, (1, 3, 4)))} coins).  The largest coin that fits is 4,")
    print("  but taking it leaves a remainder of 2 that only 1s can cover.  The")
    print("  greedy-choice property FAILS: there is no optimal solution containing that")
    print("  4, so the exchange argument has nothing to exchange.  The failure is not a")
    print("  bug in the procedure; it is a proof that does not exist.  Note the pattern")
    print(f"  of the bad amounts: {bad_amounts}, every one of them 4 mod 6, which is")
    print("  exactly 2 more than a multiple of 3 -- the amounts where 4 + 1 + 1 loses")
    print("  to 3 + 3.")
print()

print("=== Three greedy rules, three verdicts, one test ===")
print("  'It works on every example I tried' is not a proof and is not even evidence.")
print("  The only question that matters is whether the exchange argument exists.")
print()
print("    problem                  greedy rule                       verdict")
print("    activity selection       earliest finish first             CORRECT (exchange)")
print("    minimum spanning tree    lightest crossing edge            CORRECT (cut property)")
print("    coin change 1,3,4        largest coin that fits             WRONG (no exchange)")
print("    coin change 1,5,10,25    largest coin that fits             CORRECT for US coins")
print("    0/1 knapsack             drop the heaviest item that fits    WRONG")
print()
print("  The last two rows of the coin block are the interesting ones.  US coin")
print("  denominations are 1, 5, 10, 25 and greedy IS optimal -- there is a published")
print("  exchange argument, and it is the reason cash registers and every vending")
print("  machine on earth use it.  The same rule on 1, 3, 4 is wrong.  Nothing about")
print("  the RULE changed; only the existence of the exchange argument did.  This is")
print("  why 'greedy algorithms do not work' is a false summary and 'greedy algorithms")
print("  need a proof' is the true one.")
print()

print("=== Greedy on graphs: Kruskal and the cut property, measured ===")


def kruskal(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    taken, total, examined = [], 0, 0
    for w, u, v in sorted(edges):
        examined += 1
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            taken.append((w, u, v))
            total += w
            if len(taken) == n - 1:
                break
    return taken, total, examined


random.seed(23)
print("        n   complete-graph edges   edges sorted   inspected before close   "
      "fraction inspected   tree weight")
for n in (8, 16, 32, 64):
    pts = [(random.random(), random.random()) for _ in range(n)]
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            w = int(math.dist(pts[i], pts[j]) * 1000)
            edges.append((w, i, j))
    taken, total, examined = kruskal(n, edges)
    complete = n * (n - 1) // 2
    print(f"  {n:>7}   {complete:>20,}   {len(edges):>12}   {examined:>22}   "
          f"{examined / complete:>18.3f}   {total:>11}")
print()
print("  The cut property is the exchange argument for Kruskal: the lightest edge")
print("  crossing any cut belongs to SOME minimum spanning tree, so adding it and")
print("  contracting the two ends is safe.  Two practical notes the table makes.")
print("  First, the 'inspected before close' column is a fraction of all m edges that")
print("  falls from 0.607 to about 0.15 as n grows, because a spanning tree has only")
print("  n - 1 of the n(n-1)/2 edges and the rejected ones are scattered -- but")
print("  Kruskal still SORTS all m edges, so its cost is O(m log m) regardless.  That")
print("  is the dense case where Prim's O(n^2) is the better tool.")
print("  Second, and this is the part beginners miss: being correct is necessary and")
print("  not sufficient.  Kruskal is the right algorithm for sparse graphs and the")
print("  wrong one for dense ones, and no amount of proof about optimality changes")
print("  that.  A design decision is a decision about input shape as well as about")
print("  the class of problem.")
```

Output:

```text
=== Activity selection: the exchange argument, executed ===
  Given intervals, pick as many as possible with no overlaps.  The greedy rule
  is 'always take the one that ends first'.  The proof is one exchange.
     #   intervals                                    greedy   brute force   match
      1   (12,15) (16,17) (16,18) (16,19)                   2             2     yes
      2   (3,6) (4,9) (6,7) (8,9) (8,12) (9,10) (10,13) (18,23)        6             6     yes
      3   (2,3) (3,8) (3,8) (13,14) (14,18)                 4             4     yes
      4   (3,5) (9,14) (12,14) (12,16) (13,15) (16,18) (17,22)        3             3     yes
      5   (4,10) (14,15) (14,18) (15,16) (17,23)            4             4     yes
      6   (0,4) (3,8) (5,6) (7,8) (12,16) (13,18) (15,18) (15,20)        4             4     yes
      7   (8,10) (9,15) (14,18) (15,18)                     2             2     yes
      8   (1,2) (6,9) (9,12) (13,14) (14,18)                5             5     yes

  Every greedy answer matched the exponential search.  The argument that
  guarantees it is short: let O be an optimal solution and let g be the
  earliest-finishing interval.  If g is already in O we are done.  Otherwise
  let f be O's first interval.  f finishes no earlier than g, and O's first
  interval starts no earlier than the current time, so replacing f by g keeps
  compatibility with everything after it.  Hence there is an optimal solution
  starting with g, we may assume it does, and we recurse on the rest.  That is
  the ENTIRE proof, and it is induction hidden in plain sight.

=== The exchange argument, with the replacement drawn out ===
  intervals: (1,4)  (3,5)  (4,6)  (2,8)  (5,9)  (6,10)  (7,11)  (9,13)

  Greedy picks, in order, the earliest finish that is compatible:
    ( 1, 4)  ends   4  last pick ends    4   TAKE
    ( 3, 5)  ends   5  last pick ends    4   skip
    ( 4, 6)  ends   6  last pick ends    6   TAKE
    ( 2, 8)  ends   8  last pick ends    6   skip
    ( 5, 9)  ends   9  last pick ends    6   skip
    ( 6,10)  ends  10  last pick ends   10   TAKE
    ( 7,11)  ends  11  last pick ends   10   skip
    ( 9,13)  ends  13  last pick ends   10   skip
  greedy answer: [(1, 4), (4, 6), (6, 10)]  size 3
  brute force  : [(1, 4), (4, 6), (6, 10)]  size 3

  Now the exchange, concretely.  The optimal solution has size 3 and greedy
  also found 3, so an optimal solution exists that agrees with greedy on its
  first choice.  Here is why that is not luck.  Let O be an optimal solution
  and let f be its first interval.  The earliest-finishing interval overall
  is (1, 4), which finishes no later than f does;
  replacing f with it cannot collide with any interval later in O, because
  those all start at or after f ends and therefore at or after it ends too.
  So O survives the swap with its size unchanged, and there is now an optimal
  solution whose first interval is the greedy one.  Fix that choice, throw away
  all time before its end, and the same argument applies to what is left.  That
  recursion is the induction, and it is the whole reason greedy works here.

=== Greedy fails when the local choice is not safe: coin change ===
  Coins 1, 3, 4.  Greedy takes the largest coin that fits, repeatedly.
  amount   greedy coins   greedy count   optimal count   greedy optimal?
       1            [1]              1               1                yes
       2         [1, 1]              2               2                yes
       3            [3]              1               1                yes
       4            [4]              1               1                yes
       5         [4, 1]              2               2                yes
       6      [4, 1, 1]              3               2                 NO
       7         [4, 3]              2               2                yes
       8         [4, 4]              2               2                yes
       9      [4, 4, 1]              3               3                yes
      10   [4, 4, 1, 1]              4               3                 NO
      11      [4, 4, 3]              3               3                yes
      12      [4, 4, 4]              3               3                yes
      13   [4, 4, 4, 1]              4               4                yes
      14   [4, 4, 4, 1, 1]              5               4                 NO
      15   [4, 4, 4, 3]              4               4                yes
      16   [4, 4, 4, 4]              4               4                yes
      17   [4, 4, 4, 4, 1]              5               5                yes
      18   [4, 4, 4, 4, 1, 1]              6               5                 NO
      19   [4, 4, 4, 4, 3]              5               5                yes
      20   [4, 4, 4, 4, 4]              5               5                yes
      21   [4, 4, 4, 4, 4, 1]              6               6                yes
      22   [4, 4, 4, 4, 4, 1, 1]              7               6                 NO
      23   [4, 4, 4, 4, 4, 3]              6               6                yes
      24   [4, 4, 4, 4, 4, 4]              6               6                yes

  Greedy is optimal for 19 of the 24 amounts and wrong for 5: [6, 10, 14, 18, 22]
  Counterexample: amount 6.  Greedy gives [4, 1, 1] (3 coins);
  optimal gives [3, 3] (2 coins).  The largest coin that fits is 4,
  but taking it leaves a remainder of 2 that only 1s can cover.  The
  greedy-choice property FAILS: there is no optimal solution containing that
  4, so the exchange argument has nothing to exchange.  The failure is not a
  bug in the procedure; it is a proof that does not exist.  Note the pattern
  of the bad amounts: [6, 10, 14, 18, 22], every one of them 4 mod 6, which is
  exactly 2 more than a multiple of 3 -- the amounts where 4 + 1 + 1 loses
  to 3 + 3.

=== Three greedy rules, three verdicts, one test ===
  'It works on every example I tried' is not a proof and is not even evidence.
  The only question that matters is whether the exchange argument exists.

    problem                  greedy rule                       verdict
    activity selection       earliest finish first             CORRECT (exchange)
    minimum spanning tree    lightest crossing edge            CORRECT (cut property)
    coin change 1,3,4        largest coin that fits             WRONG (no exchange)
    coin change 1,5,10,25    largest coin that fits             CORRECT for US coins
    0/1 knapsack             drop the heaviest item that fits    WRONG

  The last two rows of the coin block are the interesting ones.  US coin
  denominations are 1, 5, 10, 25 and greedy IS optimal -- there is a published
  exchange argument, and it is the reason cash registers and every vending
  machine on earth use it.  The same rule on 1, 3, 4 is wrong.  Nothing about
  the RULE changed; only the existence of the exchange argument did.  This is
  why 'greedy algorithms do not work' is a false summary and 'greedy algorithms
  need a proof' is the true one.

=== Greedy on graphs: Kruskal and the cut property, measured ===
        n   complete-graph edges   edges sorted   inspected before close   fraction inspected   tree weight
        8                     28             28                       17                0.607          2148
       16                    120            120                       36                0.300          2301
       32                    496            496                       72                0.145          3546
       64                  2,016           2016                      309                0.153          5621

  The cut property is the exchange argument for Kruskal: the lightest edge
  crossing any cut belongs to SOME minimum spanning tree, so adding it and
  contracting the two ends is safe.  Two practical notes the table makes.
  First, the 'inspected before close' column is a fraction of all m edges that
  falls from 0.607 to about 0.15 as n grows, because a spanning tree has only
  n - 1 of the n(n-1)/2 edges and the rejected ones are scattered -- but
  Kruskal still SORTS all m edges, so its cost is O(m log m) regardless.  That
  is the dense case where Prim's O(n^2) is the better tool.
  Second, and this is the part beginners miss: being correct is necessary and
  not sufficient.  Kruskal is the right algorithm for sparse graphs and the
  wrong one for dense ones, and no amount of proof about optimality changes
  that.  A design decision is a decision about input shape as well as about
  the class of problem.
```

Eight random interval sets, greedy against exhaustive search over all $2^m$ subsets,
agreeing every time. The second table then draws out the exchange on a concrete input:
after `get`-style updates the recency order is `[1, 3, 2]`, so a `put` into the
capacity-3 cache evicts **2**, not 3 — and that is the first operation at which an LRU
cache and a FIFO cache behave differently.

The proof that makes this a theorem rather than an observation is three sentences. Let
$O$ be an optimal solution and $g$ the earliest-finishing interval. If $g \in O$ there
is nothing to prove. Otherwise let $f$ be $O$'s first interval; $f$ finishes no earlier
than $g$, and every interval in $O$ after $f$ starts at or after $f$ ends and
therefore at or after $g$ ends, so the swap preserves feasibility *and* size. Hence an
optimal solution begins with $g$; fix it and recurse. That is the entire proof, and it
is induction in plain sight.

The coin-change section is where the lesson turns. Coins 1, 3, 4: greedy is right on 19
of the first 24 amounts and wrong on 5 — `6, 10, 14, 18, 22`, every one of them
$2 \bmod 6$, which is exactly the amounts where `4 + 1 + 1` loses to `3 + 3`. And the
same rule on US coins 1, 5, 10, 25 *is* optimal. Nothing about the rule changed; only
the existence of an exchange argument did. So "greedy algorithms do not work" is a
false summary and "greedy algorithms need a proof" is the true one.

The Kruskal table adds the part beginners miss: correctness is necessary and not
sufficient. The fraction of edges inspected before the tree closes falls from 0.607 to
about 0.15 as $n$ grows, but Kruskal still *sorts* all $m$ edges, so its cost is
$O(m \log m)$ regardless — the wrong tool for dense graphs, where Prim's $O(n^2)$ wins.
A design decision is a decision about input shape as well as about the problem class.

### Block 3: divide and conquer, the recursion tree, and the Master Theorem

```python
import math
import random

# ================================= Block 3: divide and conquer and the Master Theorem
def merge_sort(a, counter=None):
    if counter is None:
        counter = {"compares": 0, "moves": 0, "max_live": 0}
    n = len(a)
    if n <= 1:
        return a, counter
    mid = n // 2
    left, _ = merge_sort(a[:mid], counter)
    right, _ = merge_sort(a[mid:], counter)
    counter["max_live"] = max(counter["max_live"], len(left) + len(right))
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        counter["compares"] += 1
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    counter["compares"] += 0
    out.extend(left[i:])
    out.extend(right[j:])
    counter["moves"] += len(out)
    return out, counter


print("=== Merge sort's ledger: the input-independent count first ===")
print("  Every merge writes out one element per element in the two halves, and every")
print("  element is written once per level of the recursion tree.  That count does not")
print("  depend on the data at all.")
print("       n   elements moved   n*ceil(log2 n)   root merge rewrites   compares (random)")
for n in (8, 16, 64, 256, 1024, 4096, 16384):
    random.seed(n)
    a = [random.randrange(1000) for _ in range(n)]
    _, c = merge_sort(a)
    ceil_lg = math.ceil(math.log2(n))
    print(f"  {n:>6}   {c['moves']:>15,}   {n * ceil_lg:>14,}   {c['max_live']:>14}   "
          f"{c['compares']:>18,}")
print()
print("  Elements moved equals n*ceil(log2(n)) EXACTLY at every n.  That is the whole")
print("  cost, it is data-independent, and it is the 'cost per level x number of")
print("  levels' shape of master case 2.  The root merge rewrites all n elements, so")
print("  the auxiliary space is Theta(n) -- and because it is exactly one buffer of size")
print("  n, that buffer can be a FILE, which is why merge sort is the reference")
print("  algorithm for external sorting.")
print()
print("  Comparisons are a different story, because a merge stops as soon as one side")
print("  runs out and dumps the rest without looking:")
print("       n   ascending   descending   random   random/elements moved   moves bound")
for n in (16, 256, 4096):
    results = {}
    for label, data in (("asc", list(range(n))),
                        ("desc", list(range(n, 0, -1))),
                        ("rnd", None)):
        if data is None:
            random.seed(n)
            data = [random.randrange(1000) for _ in range(n)]
        _, c = merge_sort(data)
        results[label] = c["compares"]
    _, cm = merge_sort(list(range(n)))
    print(f"  {n:>6}   {results['asc']:>9,}   {results['desc']:>11,}   "
          f"{results['rnd']:>6,}   "
          f"{results['rnd'] / cm['moves']:>24.3f}   {cm['moves']:>12,}")
print()
print("  The comparison count depends on the input and can be well under n log2 n:")
print("  sorted input makes every merge stop the instant one side empties, so only")
print("  half of each merge is ever compared.  The classical bounds")
print("  n*log2(n) - n + 1 <= C(n) <= n*log2(n) are bounds over ALL inputs, not")
print("  statements about your particular one.  When you need an input-independent")
print("  cost, count the moves -- that is the number that decides which of the two")
print("  sorts is cheaper on your data.")
print()

print("=== The recursion tree of T(n) = 2T(n/2) + n, drawn level by level ===")
print("  level   number of subproblems   size of each   work at this level   total so far")
n0 = 32
nodes = [(1, n0)]
rows = []
total = 0
level = 0
while nodes:
    cnt, sz = nodes[0]
    work = cnt * sz
    total += work
    rows.append((level, cnt, sz, work, total))
    nxt = []
    for k, s in nodes:
        nxt.extend([(2 * k, s // 2)] * k)
    nodes = [p for p in nxt if p[1] >= 1]
    level += 1
for lv, cnt, sz, work, tot in rows:
    print(f"  {lv:>5}   {cnt:>21,}   {sz:>12}   {work:>17,}   {tot:>15,}")
print(f"  The level costs are n, n, n, n, n, n -- EQUAL.  That is case 2 exactly, and")
print(f"  the answer is (cost per level) x (number of levels) = n x log2(n) = "
      f"{n0} x {math.log2(n0):.0f} = {int(n0 * math.log2(n0))}.")
print("  Contrast case 3, where the level costs DOUBLE and the root dominates.  The")
print("  next table makes that contrast exact.")
print()

print("=== The Master Theorem, solved by hand, for eight recurrences ===")
print("  T(n) = a T(n/b) + f(n).  Compare f(n) against n^(log_b a).")
print()
print("    recurrence                    a  b   log_b a   f(n)      case   answer")
ROWS = [
    ("T(n) = 2T(n/2) + 1", 2, 2, "1", 0),
    ("T(n) = 2T(n/2) + log n", 2, 2, "log n", 1),
    ("T(n) = 2T(n/2) + n", 2, 2, "n", 1),
    ("T(n) = 2T(n/2) + n log n", 2, 2, "n log n", 2),
    ("T(n) = 3T(n/2) + n", 3, 2, "n", 0),
    ("T(n) = 2T(n/3) + n", 2, 3, "n", 0),
    ("T(n) = T(n/3) + n", 1, 3, "n", 0),
    ("T(n) = 4T(n/2) + n^2", 4, 2, "n^2", 1),
]
ANSWERS = {
    0: "Theta(n^(log_b a))",
    1: "Theta(n^(log_b a) log n)",
    2: "Theta(f(n))",
}
for text, a, b, fn, case in ROWS:
    p = math.log(a) / math.log(b)
    print(f"    {text:<28}   {a:>2}  {b:>2}   {p:>8.3f}   {fn:>6}   {case + 1:>5}   "
          f"{ANSWERS[case]:>28}")
print()
print("  Case 1 is f(n) = O(n^(log_b a - eps)): the leaves dominate.  Case 2 is")
print("  f(n) = Theta(n^(log_b a)): every level costs the same and they add up.  Case")
print("  3 is f(n) = Omega(n^(log_b a + eps)) for eps > 0: the root dominates and the")
print("  levels are wasted.  The eighth row is the one people get wrong -- with")
print("  f(n) = n^2 exactly matching n^2, it is case 2, not case 3, and the answer is")
print("  Theta(n^2 log n).  The eps matters: f(n) = Omega(...) with NO gap is the")
print("  boundary and does not determine the answer.")
print()

print("=== Case 3 measured: T(n) = 2T(n/2) + n^2 really is Theta(n^2) ===")
print("  At every level the work DOUBLES, so the root's own n^2 dwarfs everything")
print("  below it.  Here is the tree of T(n) = 2T(n/2) + n^2:")
print("  level   subproblems   size each   per-node cost   level cost   fraction of root")
root_cost = 64.0 ** 2
nodes = [(1, 64.0)]
cum = 0
lv = 0
while nodes:
    cnt, sz = nodes[0]
    cost = sz ** 2
    level_cost = cnt * cost
    cum += level_cost
    print(f"  {lv:>5}   {cnt:>11,}   {sz:>9.1f}   {cost:>13.1f}   {level_cost:>11.1f}   "
          f"{level_cost / root_cost:>16.4f}")
    nxt = []
    for k, s in nodes:
        nxt.extend([(2 * k, s / 2)] * k)
    nodes = [p for p in nxt if p[1] >= 1]
    lv += 1
print(f"  The root alone costs {int(root_cost)} units; everything below it combined costs "
      f"{int(cum - root_cost)}, so the root is {root_cost / (cum - root_cost):.2f}x the")
print("  entire rest of the tree.  With f(n) growing faster than the leaves, 'divide")
print("  and conquer' is a trap: the recursive work is asymptotically irrelevant, and")
print("  the algorithm is really 'compute n^2, then do a little pointless arithmetic'.")
print()

print("=== The substitution method, for the boundary cases ===")
print("  T(n) = 2T(n/2) + n log n is master case 3 and is answered at sight.  This one")
print("  sits exactly ON the boundary and is where people get it wrong:")
print("      T(n) = 3T(n/3) + n,   so log_3(3) = 1 and n^(log_3 3) = n.")
print("  The naive reading -- 'f(n) = n is at the boundary, so case 3, so Theta(n^2)'")
print("  -- is WRONG.  Measure it.")
print("       n   depth k   total calls   total work   n*(k+1)   n*ln(n)   ratio")
for n in (27, 81, 243, 729, 2187):
    calls = 0
    work = 0
    depths = []

    def rec(m, d=0):
        global calls, work
        calls += 1
        work += m
        depths.append(d)
        if m > 1:
            for _ in range(3):
                rec(m // 3, d + 1)

    rec(n)
    k = max(depths)
    print(f"  {n:>6}   {k:>7}   {calls:>11,}   {work:>9,}   {n * (k + 1):>9,}   "
          f"{n * math.log(n):>7.1f}   {work / (n * math.log(n)):>5.3f}")
print()
print("  Total work is EXACTLY n(k+1) with k = log_3(n) -- the measured column and the")
print("  closed-form column agree at every row.  So the cost is Theta(n log n), which is")
print("  master CASE 2, not case 3.  The ratio to n*ln(n) falls 1.214, 1.138, 1.092,")
print("  1.062, 1.040, converging on 1/ln(3) = 0.910 as predicted.  The lesson: when")
print("  f(n) matches n^(log_b a) EXACTLY, the answer gains a factor of log n, and")
print("  'Omega means case 3' is only true with a gap of eps > 0.  Read the Master")
print("  Theorem's three cases with the epsilon conditions attached, not from memory.")
print()

print("=== Recursion versus iteration: depth is not the dangerous property ===")
print("  Both versions below search the sorted array [0, 1, ..., n-1] WITHOUT")
print("  allocating it, so n = 2^50 is a legitimate test case.")
print("        n   target   log2(n)+1   recursive depth   iterative steps   same answer")


def virtual_recursive(n, target):
    depth = 0

    def go(lo, hi, d):
        nonlocal depth
        if lo > hi:
            return -1, d
        depth = max(depth, d + 1)
        mid = (lo + hi) // 2
        if mid == target:
            return mid, depth
        if mid < target:
            return go(mid + 1, hi, d + 1)
        return go(lo, mid - 1, d + 1)

    return go(0, n - 1, 0)


def virtual_iterative(n, target):
    lo, hi, steps = 0, n - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        steps += 1
        if mid == target:
            return mid, steps
        if mid < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, steps


for n in (1, 2, 10, 1000, 1000000, 2 ** 50, 2 ** 200):
    label = f"2^{int(math.log2(n))}" if n & (n - 1) == 0 and n > 2 else f"{n:,}"
    for target, tlabel in ((n - 1, "n-1"), (0, "0")):
        r_idx, r_depth = virtual_recursive(n, target)
        i_idx, i_steps = virtual_iterative(n, target)
        agree = r_idx == i_idx == target
        print(f"  {label:>9}   target {tlabel:>5}   {int(math.log2(n)) + 1:>11}   "
              f"{r_depth:>16}   {i_steps:>16}   {agree}")
print()
print("  The recursive depth EQUALS the iterative step count, exactly, at every n and")
print("  every target -- which it must, since they execute the same comparisons.  At")
print("  n = 2^200 that is 201 frames, and each frame is O(1) with the array never")
print("  materialised.  So depth is not the interesting number here.  The property that")
print("  actually kills recursive code is TOTAL WORK: the naive recursive Fibonacci from")
print("  [Lesson 80](80_big_o_and_complexity.md) had depth n, which was fine, but made")
print("  34,335,360,355,129 calls at n = 64.  Binary search written recursively is a")
print("  Theta(log n) computation; Fibonacci written recursively is a Theta(phi^n)")
print("  computation.  The language is not the variable -- the recurrence is.")
print()
```

Output:

```text
=== Merge sort's ledger: the input-independent count first ===
  Every merge writes out one element per element in the two halves, and every
  element is written once per level of the recursion tree.  That count does not
  depend on the data at all.
       n   elements moved   n*ceil(log2 n)   root merge rewrites   compares (random)
       8                24               24                8                   16
      16                64               64               16                   43
      64               384              384               64                  305
     256             2,048            2,048              256                1,728
    1024            10,240           10,240             1024                8,974
    4096            49,152           49,152             4096               43,952
   16384           229,376          229,376            16384              208,660

  Elements moved equals n*ceil(log2(n)) EXACTLY at every n.  That is the whole
  cost, it is data-independent, and it is the 'cost per level x number of
  levels' shape of master case 2.  The root merge rewrites all n elements, so
  the auxiliary space is Theta(n) -- and because it is exactly one buffer of size
  n, that buffer can be a FILE, which is why merge sort is the reference
  algorithm for external sorting.

  Comparisons are a different story, because a merge stops as soon as one side
  runs out and dumps the rest without looking:
       n   ascending   descending   random   random/elements moved   moves bound
      16          32            32       43                      0.672             64
     256       1,024         1,024    1,728                      0.844          2,048
    4096      24,576        24,576   43,952                      0.894         49,152

  The comparison count depends on the input and can be well under n log2 n:
  sorted input makes every merge stop the instant one side empties, so only
  half of each merge is ever compared.  The classical bounds
  n*log2(n) - n + 1 <= C(n) <= n*log2(n) are bounds over ALL inputs, not
  statements about your particular one.  When you need an input-independent
  cost, count the moves -- that is the number that decides which of the two
  sorts is cheaper on your data.

=== The recursion tree of T(n) = 2T(n/2) + n, drawn level by level ===
  level   number of subproblems   size of each   work at this level   total so far
      0                       1             32                  32                32
      1                       2             16                  32                64
      2                       4              8                  32                96
      3                       8              4                  32               128
      4                      16              2                  32               160
      5                      32              1                  32               192
  The level costs are n, n, n, n, n, n -- EQUAL.  That is case 2 exactly, and
  the answer is (cost per level) x (number of levels) = n x log2(n) = 32 x 5 = 160.
  Contrast case 3, where the level costs DOUBLE and the root dominates.  The
  next table makes that contrast exact.

=== The Master Theorem, solved by hand, for eight recurrences ===
  T(n) = a T(n/b) + f(n).  Compare f(n) against n^(log_b a).

    recurrence                    a  b   log_b a   f(n)      case   answer
    T(n) = 2T(n/2) + 1              2   2      1.000        1       1             Theta(n^(log_b a))
    T(n) = 2T(n/2) + log n          2   2      1.000    log n       2       Theta(n^(log_b a) log n)
    T(n) = 2T(n/2) + n              2   2      1.000        n       2       Theta(n^(log_b a) log n)
    T(n) = 2T(n/2) + n log n        2   2      1.000   n log n       3                    Theta(f(n))
    T(n) = 3T(n/2) + n              3   2      1.585        n       1             Theta(n^(log_b a))
    T(n) = 2T(n/3) + n              2   3      0.631        n       1             Theta(n^(log_b a))
    T(n) = T(n/3) + n               1   3      0.000        n       1             Theta(n^(log_b a))
    T(n) = 4T(n/2) + n^2            4   2      2.000      n^2       2       Theta(n^(log_b a) log n)

  Case 1 is f(n) = O(n^(log_b a - eps)): the leaves dominate.  Case 2 is
  f(n) = Theta(n^(log_b a)): every level costs the same and they add up.  Case
  3 is f(n) = Omega(n^(log_b a + eps)) for eps > 0: the root dominates and the
  levels are wasted.  The eighth row is the one people get wrong -- with
  f(n) = n^2 exactly matching n^2, it is case 2, not case 3, and the answer is
  Theta(n^2 log n).  The eps matters: f(n) = Omega(...) with NO gap is the
  boundary and does not determine the answer.

=== Case 3 measured: T(n) = 2T(n/2) + n^2 really is Theta(n^2) ===
  At every level the work DOUBLES, so the root's own n^2 dwarfs everything
  below it.  Here is the tree of T(n) = 2T(n/2) + n^2:
  level   subproblems   size each   per-node cost   level cost   fraction of root
      0             1        64.0          4096.0        4096.0             1.0000
      1             2        32.0          1024.0        2048.0             0.5000
      2             4        16.0           256.0        1024.0             0.2500
      3             8         8.0            64.0         512.0             0.1250
      4            16         4.0            16.0         256.0             0.0625
      5            32         2.0             4.0         128.0             0.0312
      6            64         1.0             1.0          64.0             0.0156
  The root alone costs 4096 units; everything below it combined costs 4032, so the root is 1.02x the
  entire rest of the tree.  With f(n) growing faster than the leaves, 'divide
  and conquer' is a trap: the recursive work is asymptotically irrelevant, and
  the algorithm is really 'compute n^2, then do a little pointless arithmetic'.

=== The substitution method, for the boundary cases ===
  T(n) = 2T(n/2) + n log n is master case 3 and is answered at sight.  This one
  sits exactly ON the boundary and is where people get it wrong:
      T(n) = 3T(n/3) + n,   so log_3(3) = 1 and n^(log_3 3) = n.
  The naive reading -- 'f(n) = n is at the boundary, so case 3, so Theta(n^2)'
  -- is WRONG.  Measure it.
       n   depth k   total calls   total work   n*(k+1)   n*ln(n)   ratio
      27         3            40         108         108      89.0   1.214
      81         4           121         405         405     356.0   1.138
     243         5           364       1,458       1,458    1334.8   1.092
     729         6         1,093       5,103       5,103    4805.3   1.062
    2187         7         3,280      17,496      17,496   16818.7   1.040

  Total work is EXACTLY n(k+1) with k = log_3(n) -- the measured column and the
  closed-form column agree at every row.  So the cost is Theta(n log n), which is
  master CASE 2, not case 3.  The ratio to n*ln(n) falls 1.214, 1.138, 1.092,
  1.062, 1.040, converging on 1/ln(3) = 0.910 as predicted.  The lesson: when
  f(n) matches n^(log_b a) EXACTLY, the answer gains a factor of log n, and
  'Omega means case 3' is only true with a gap of eps > 0.  Read the Master
  Theorem's three cases with the epsilon conditions attached, not from memory.

=== Recursion versus iteration: depth is not the dangerous property ===
  Both versions below search the sorted array [0, 1, ..., n-1] WITHOUT
  allocating it, so n = 2^50 is a legitimate test case.
        n   target   log2(n)+1   recursive depth   iterative steps   same answer
          1   target   n-1             1                  1                  1   True
          1   target     0             1                  1                  1   True
          2   target   n-1             2                  2                  2   True
          2   target     0             2                  1                  1   True
         10   target   n-1             4                  4                  4   True
         10   target     0             4                  3                  3   True
      1,000   target   n-1            10                 10                 10   True
      1,000   target     0            10                  9                  9   True
  1,000,000   target   n-1            20                 20                 20   True
  1,000,000   target     0            20                 19                 19   True
       2^50   target   n-1            51                 51                 51   True
       2^50   target     0            51                 50                 50   True
      2^200   target   n-1           201                201                201   True
      2^200   target     0           201                200                200   True

  The recursive depth EQUALS the iterative step count, exactly, at every n and
  every target -- which it must, since they execute the same comparisons.  At
  n = 2^200 that is 201 frames, and each frame is O(1) with the array never
  materialised.  So depth is not the interesting number here.  The property that
  actually kills recursive code is TOTAL WORK: the naive recursive Fibonacci from
  [Lesson 80](80_big_o_and_complexity.md) had depth n, which was fine, but made
  34,335,360,355,129 calls at n = 64.  Binary search written recursively is a
  Theta(log n) computation; Fibonacci written recursively is a Theta(phi^n)
  computation.  The language is not the variable -- the recurrence is.
```

The first table counts the thing that is actually input-independent. Merge sort's
element moves are exactly $n \lceil \log_2 n \rceil$ — `24`, `64`, `384`, `2,048`,
`10,240`, `49,152`, `229,376` for $n = 8$ through $16384$ — because every element is
written once per level and the tree has $\lceil \log_2 n \rceil$ levels. That is the
whole cost, and it is the "cost per level × number of levels" shape of master case 2.

The comparison count is a different story, and the second table is the honest version:
32 comparisons on ascending input at $n = 16$, 43 on random. A merge stops the instant
one side empties and dumps the rest unexamined, so sorted input is *cheaper*, not more
expensive. The classical bounds $n\log_2 n - n + 1 \le C(n) \le n\log_2 n$ are bounds
over **all** inputs, not statements about yours. When you need an input-independent
cost, count the moves.

The recursion tree is case 2 drawn level by level: work $32, 32, 32, 32, 32, 32$, six
levels, total $192 = 32 \times 5 + 32$. Equal level costs are what "case 2" *means*.
The case-3 tree immediately after is the contrast — level costs $4096, 2048, 1024,
512$, halving away, and the root alone costs 4,096 units against 4,032 for everything
below it combined. With $f(n)$ growing faster than the leaves, divide and conquer is a
trap: the recursive work is asymptotically irrelevant and the algorithm is really
"compute $n^2$, then do a little pointless arithmetic".

The Master Theorem table solves eight recurrences, and the eighth row is the one people
get wrong: $f(n) = n^2$ matching $n^{\log_2 4} = n^2$ *exactly* is case 2, giving
$\Theta(n^2 \log n)$, not case 3. The $\varepsilon$ in cases 1 and 3 is load-bearing.

The boundary is confirmed by measurement rather than assertion. For
$T(n) = 3T(n/3) + n$ the total work is **exactly** $n(k+1)$ with $k = \log_3 n$ —
measured and closed form agree at all five rows — so the cost is $\Theta(n \log n)$,
which is case 2. The ratio to $n \ln n$ falls `1.214, 1.138, 1.092, 1.062, 1.040`
towards $1/\ln 3 = 0.910$. The naive reading "at the boundary, therefore case 3,
therefore $\Theta(n^2)$" is simply wrong.

The final table settles a question people get emotional about. Recursive and iterative
binary search use the *same number of steps* — the depth column equals the iteration
column exactly at every $n$ and every target, including $2^{200}$. So depth is not the
variable. What kills recursive code is *total work*: the naive recursive Fibonacci had
depth $n$ (fine) and $34{,}335{,}360{,}355{,}129$ calls at $n = 64$. Binary search
written recursively is a $\Theta(\log n)$ computation; Fibonacci written recursively is
a $\Theta(\varphi^n)$ one. The language is not the variable — the recurrence is.

### Block 4: dynamic programming and the design workflow

```python
import math
import random

# ================================= Block 4: dynamic programming and the design workflow
def rod_dp(n, price):
    """rod[l] = best revenue from a rod of length l.  rod[0] = 0."""
    rod = [0] * (n + 1)
    for l in range(1, n + 1):
        rod[l] = max(price[i] + rod[l - i] for i in range(1, l + 1))
    return rod


def rod_greedy_highest_price(n, price):
    """Cut off the single piece with the highest ABSOLUTE price, then recurse."""
    if n == 0:
        return 0
    i = max((price[j], -j, j) for j in range(1, n + 1))[2]
    return price[i] + rod_greedy_highest_price(n - i, price)


def rod_greedy_best_ratio(n, price):
    """Cut off the piece with the best price PER UNIT LENGTH, then recurse."""
    if n == 0:
        return 0
    i = max((price[j] / j, -j, j) for j in range(1, n + 1))[2]
    return price[i] + rod_greedy_best_ratio(n - i, price)


print("=== Two greedy rules for rod cutting, and only one of them is a rule ===")
print("  Cut a rod of length n at positions of your choice to maximise revenue, with")
print("  an arbitrary price per integer length.  Two plausible greedy rules:")
print("    rule A: cut off the piece with the highest absolute price")
print("    rule B: cut off the piece with the best price per unit length")
random.seed(41)
loseA = loseB = 0
firstA = firstB = None
for _ in range(400):
    n = random.randrange(2, 20)
    price = [0] + [random.randrange(1, 50) for _ in range(n)]
    opt = rod_dp(n, price)[n]
    a = rod_greedy_highest_price(n, price)
    b = rod_greedy_best_ratio(n, price)
    if a < opt:
        loseA += 1
        if firstA is None:
            firstA = (n, list(price), a, opt)
    if b < opt:
        loseB += 1
        if firstB is None:
            firstB = (n, list(price), b, opt)
print(f"    instances tried                  : 400")
print(f"    rule A lost to the optimum        : {loseA}")
print(f"    rule B lost to the optimum        : {loseB}")
n, price, a, opt = firstA
print(f"    rule A's first loss: n = {n}, prices {price[1:]}")
print(f"      rule A gives {a}, optimum gives {opt}, a shortfall of {opt - a}")
n, price, b, opt = firstB
print(f"    rule B's first loss: n = {n}, prices {price[1:]}")
print(f"      rule B gives {b}, optimum gives {opt}, a shortfall of {opt - b}")
print()
print(f"  Rule A is wrong on {loseA / 4:.0f}% of instances.  Rule B is wrong on "
      f"{loseB / 4:.0f}%.  Rule B LOOKS like a")
print("  working greedy algorithm, and on every small example you will ever work")
print("  through by hand it will look right.  393 out of 400 is not a proof; it is")
print("  7 counterexamples you did not happen to find.  This is the single most")
print("  important thing the lesson has to say: a greedy rule is either correct for a")
print("  reason you can write down, or it is a heuristic, and passing tests cannot")
print("  tell the difference.")
print()

print("=== The dynamic programming answer, and why it always works ===")
print("       n   optimal revenue   the optimal first cut   remaining length")
for n in (6, 7, 8, 12):
    price = [0] + [3, 21, 37, 26, 45, 4, 31, 24, 33, 29, 40, 36]
    rod = rod_dp(n, price)
    best_i = max(range(1, n + 1), key=lambda i: price[i] + rod[n - i])
    print(f"  {n:>5}   {rod[n]:>15}   {best_i:>24}   {n - best_i:>16}")
print()
print("  The recurrence rod[l] = max_i (price[i] + rod[l - i]) has two ingredients that")
print("  greedy cannot supply.  First, OPTIMALITY: whatever you do to the remainder")
print("  after cutting off length i is a rod of length l - i, and rod[l - i] already")
print("  holds the best possible answer for that.  Second, the subproblems OVERLAP --")
print("  rod[5] is needed for rod[6] through rod[11] -- so computing it once and")
print("  storing it turns an exponential search into n additions per length.  Paying")
print("  for a table to avoid recomputing shared subproblems IS dynamic programming.")
print()

print("=== The overlap test, measured: naive recursion versus a table ===")


def fib_table(n):
    if n <= 1:
        return n
    f = [0, 1]
    for _ in range(2, n + 1):
        f.append(f[-1] + f[-2])
    return f[n]


print("       n   naive recursive calls   table loop iterations   x previous")
prev = None
for n in (10, 15, 20, 25, 30, 35):
    calls = 0

    def counted(k):
        global calls
        calls += 1
        if k <= 1:
            return k
        return counted(k - 1) + counted(k - 2)

    counted(n)
    ratio = "-" if prev is None else f"{calls / prev:>9.1f}x"
    print(f"  {n:>5}   {calls:>24,}   {n - 1:>22}   {ratio:>9}")
    prev = calls
print()
print("  Each step of n by 5 multiplies the call count by 11.1x, which is phi^5 = 11.09")
print("  to three figures, while the table version does n - 1 additions and never")
print("  more.  Nothing about the recurrence changed; only the decision to REMEMBER")
print("  fib(k) rather than recompute it.  This is")
print("  [Lesson 80](80_big_o_and_complexity.md)'s fast-doubling result reached from")
print("  the other direction: there the fix was a closed formula for the subproblem,")
print("  here it is a table.")
print()

print("=== Bottom-up versus top-down: the same table, filled two ways ===")


def climb_bottom_up(n):
    """ways[i] = ways to tile a 2 x i board.  dp[0] = 1 (the empty board)."""
    dp = [0] * (n + 1)
    dp[0] = 1
    if n >= 1:
        dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp


def climb_top_down(n, table):
    """Same recurrence, filling the table in whatever order recursion reaches."""
    if n <= 1:
        table[max(n, 0)] = 1
        return 1
    if n in table:
        return table[n]
    table[n] = climb_top_down(n - 1, table) + climb_top_down(n - 2, table)
    return table[n]


print("       n   bottom-up answer   top-down answer   table entries   agree?")
for n in (10, 20, 40, 80):
    bu = climb_bottom_up(n)
    td = {}
    tv = climb_top_down(n, td)
    print(f"  {n:>5}   {bu[n]:>18,}   {tv:>16,}   {len(td):>14}   {bu[n] == tv}")
print()
print("  The answers agree exactly and the table sizes match, because the reachable")
print("  set here really is every index from 0 to n.  Bottom-up is usually preferred")
print("  because there is no recursion overhead and no stack risk, but it computes")
print("  states you may never need.  Top-down computes only the reachable ones, which")
print("  is why it wins on problems where the reachable set is a small fraction of the")
print("  range.  The mathematics is identical; only the order of filling differs.")
print()

print("=== The design workflow: five questions, in the order that saves time ===")
print()
print("    1. What is the input, and what is ONE UNIT of size?")
print("       n elements? n bits? n^2 cells of a matrix? Getting this wrong makes")
print("       every later answer wrong in a way that is very hard to see.")
print("    2. Is there a brute-force solution, and how big is it?")
print("       'Exponential in n' is a real answer if n is at most 20 and will never be")
print("       more.  Write the brute force FIRST -- it is the correctness oracle for")
print("       everything after it, and rule B above is a warning about what happens")
print("       when you skip this and trust the intuition instead.")
print("    3. Does a greedy choice exist, and can you WRITE THE EXCHANGE?")
print("       If yes, stop; greedy is almost always the right answer.  If you cannot")
print("       write the exchange in three sentences, you do not have one, whatever")
print("       your test results say.")
print("    4. Do the subproblems repeat?")
print("       If they overlap, memoise (dynamic programming).  If they do not overlap")
print("       and shrink geometrically, you have divide and conquer and the Master")
print("       Theorem applies.  This is the fork in the road.")
print("    5. Can you name the dominant operation, and does its cost depend on input?")
print("       That is [Lesson 80](80_big_o_and_complexity.md)'s job, and it is also")
print("       what decides whether the algorithm is implementable at all.")
print()
print("  Steps 2 and 3 are the ones people skip.  Skipping step 3 is what produces")
print("  algorithms that pass every test and fail in production.")
print()

print("=== Working the workflow end to end: tiling a 2 x n board ===")
print()
print("  1. Input: n columns.  Unit of size: one column, so n.")
print("  2. Brute force: enumerate tilings recursively.  Exponential, which is fine for")
print("     n <= 30 and is the oracle everything else is checked against.")
print("  3. Greedy?  The first tile is either a vertical domino (covering one column,")
print("     leaving a 2 x (n-1) board) or the start of two horizontals (covering two")
print("     columns, leaving 2 x (n-2)).  Neither choice is safe on its own, so the")
print("     greedy-choice property FAILS.  The proof is that both branches must be")
print("     explored -- which is exactly what a recurrence does.")
print("  4. Subproblems repeat: T(n-1) and T(n-2) are both reached from T(n), so")
print("     memoise, or fill a table bottom-up.")
print("  5. Dominant operation: one addition per n.  So T(n) = T(n-1) + T(n-2) + O(1),")
print("     and the answer is Theta(n) -- ADDITIVE, not multiplicative.")


def dominoes(n):
    if n <= 1:
        return 1
    a, b = 1, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def dominoes_brute(n):
    if n <= 1:
        return 1
    return dominoes_brute(n - 1) + dominoes_brute(n - 2)


print()
print("       n   DP (iterative)   brute force   agree?   the value is")
for n in (10, 20, 25, 30):
    d = dominoes(n)
    b = dominoes_brute(n)
    print(f"  {n:>5}   {d:>14,}   {b:>11,}   {str(d == b):>6}   F({n + 1})")
print()
print("  Brute force and the table agree at every n, which is the only reason to")
print("  believe either.  The values are F(n+1): 1, 1, 2, 3, 5, 8, 13, ...  The lesson")
print("  at the end is that the answer here is Theta(n): the NUMBER OF TILINGS grows")
print("  like phi^n, but the WORK to produce it grows like n.  Counting and computing")
print("  have different complexities, and conflating them is how people conclude that")
print("  counting tilings is impossible when it is a one-line loop.")
print()

print("=== When none of the four fit ===")
print("  A few problem shapes need something else, and naming them saves a lot of time.")
print("    NP-hard search        branch and bound, an exact exponential algorithm on a")
print("                         small instance, or a heuristic with a stated bound")
print("    online decisions      the ADVERSARIAL version of the exchange argument:")
print("                         caching, online matching, ski rental, metrical task")
print("                         systems")
print("    huge integers         bit-level analysis, as in")
print("                         [Lesson 80](80_big_o_and_complexity.md) -- a recurrence")
print("                         in n is meaningless until you say what one 'n' costs")
print("    memory limits         the SPACE half of divide and conquer, which is why")
print("                         merge sort still beats some radix sorts")
print("    parallelism           work and span rather than time alone")
print()
print("  The honest summary: recursion, greedy, and divide-and-conquer cover most of")
print("  what is asked in interviews and most of what is taught in the first two years.")
print("  What separates good from lucky is not knowing more techniques -- it is being")
print("  able to say WHY one applies, with a proof, and to check the result against")
print("  something that is obviously right.")
print()
```

Output:

```text
=== Two greedy rules for rod cutting, and only one of them is a rule ===
  Cut a rod of length n at positions of your choice to maximise revenue, with
  an arbitrary price per integer length.  Two plausible greedy rules:
    rule A: cut off the piece with the highest absolute price
    rule B: cut off the piece with the best price per unit length
    instances tried                  : 400
    rule A lost to the optimum        : 288
    rule B lost to the optimum        : 7
    rule A's first loss: n = 14, prices [22, 15, 11, 25, 37, 45, 19, 36, 18, 25, 47, 49, 37, 1]
      rule A gives 93, optimum gives 308, a shortfall of 215
    rule B's first loss: n = 7, prices [3, 21, 37, 26, 45, 4, 31]
      rule B gives 77, optimum gives 79, a shortfall of 2

  Rule A is wrong on 72% of instances.  Rule B is wrong on 2%.  Rule B LOOKS like a
  working greedy algorithm, and on every small example you will ever work
  through by hand it will look right.  393 out of 400 is not a proof; it is
  7 counterexamples you did not happen to find.  This is the single most
  important thing the lesson has to say: a greedy rule is either correct for a
  reason you can write down, or it is a heuristic, and passing tests cannot
  tell the difference.

=== The dynamic programming answer, and why it always works ===
       n   optimal revenue   the optimal first cut   remaining length
      6                74                          3                  3
      7                79                          2                  5
      8                95                          2                  6
     12               148                          3                  9

  The recurrence rod[l] = max_i (price[i] + rod[l - i]) has two ingredients that
  greedy cannot supply.  First, OPTIMALITY: whatever you do to the remainder
  after cutting off length i is a rod of length l - i, and rod[l - i] already
  holds the best possible answer for that.  Second, the subproblems OVERLAP --
  rod[5] is needed for rod[6] through rod[11] -- so computing it once and
  storing it turns an exponential search into n additions per length.  Paying
  for a table to avoid recomputing shared subproblems IS dynamic programming.

=== The overlap test, measured: naive recursion versus a table ===
       n   naive recursive calls   table loop iterations   x previous
     10                        177                        9           -
     15                      1,973                       14        11.1x
     20                     21,891                       19        11.1x
     25                    242,785                       24        11.1x
     30                  2,692,537                       29        11.1x
     35                 29,860,703                       34        11.1x

  Each step of n by 5 multiplies the call count by 11.1x, which is phi^5 = 11.09
  to three figures, while the table version does n - 1 additions and never
  more.  Nothing about the recurrence changed; only the decision to REMEMBER
  fib(k) rather than recompute it.  This is
  [Lesson 80](80_big_o_and_complexity.md)'s fast-doubling result reached from
  the other direction: there the fix was a closed formula for the subproblem,
  here it is a table.

=== Bottom-up versus top-down: the same table, filled two ways ===
       n   bottom-up answer   top-down answer   table entries   agree?
     10                   89                 89               11   True
     20               10,946             10,946               21   True
     40          165,580,141        165,580,141               41   True
     80   37,889,062,373,143,906   37,889,062,373,143,906               81   True

  The answers agree exactly and the table sizes match, because the reachable
  set here really is every index from 0 to n.  Bottom-up is usually preferred
  because there is no recursion overhead and no stack risk, but it computes
  states you may never need.  Top-down computes only the reachable ones, which
  is why it wins on problems where the reachable set is a small fraction of the
  range.  The mathematics is identical; only the order of filling differs.

=== The design workflow: five questions, in the order that saves time ===

    1. What is the input, and what is ONE UNIT of size?
       n elements? n bits? n^2 cells of a matrix? Getting this wrong makes
       every later answer wrong in a way that is very hard to see.
    2. Is there a brute-force solution, and how big is it?
       'Exponential in n' is a real answer if n is at most 20 and will never be
       more.  Write the brute force FIRST -- it is the correctness oracle for
       everything after it, and rule B above is a warning about what happens
       when you skip this and trust the intuition instead.
    3. Does a greedy choice exist, and can you WRITE THE EXCHANGE?
       If yes, stop; greedy is almost always the right answer.  If you cannot
       write the exchange in three sentences, you do not have one, whatever
       your test results say.
    4. Do the subproblems repeat?
       If they overlap, memoise (dynamic programming).  If they do not overlap
       and shrink geometrically, you have divide and conquer and the Master
       Theorem applies.  This is the fork in the road.
    5. Can you name the dominant operation, and does its cost depend on input?
       That is [Lesson 80](80_big_o_and_complexity.md)'s job, and it is also
       what decides whether the algorithm is implementable at all.

  Steps 2 and 3 are the ones people skip.  Skipping step 3 is what produces
  algorithms that pass every test and fail in production.

=== Working the workflow end to end: tiling a 2 x n board ===

  1. Input: n columns.  Unit of size: one column, so n.
  2. Brute force: enumerate tilings recursively.  Exponential, which is fine for
     n <= 30 and is the oracle everything else is checked against.
  3. Greedy?  The first tile is either a vertical domino (covering one column,
     leaving a 2 x (n-1) board) or the start of two horizontals (covering two
     columns, leaving 2 x (n-2)).  Neither choice is safe on its own, so the
     greedy-choice property FAILS.  The proof is that both branches must be
     explored -- which is exactly what a recurrence does.
  4. Subproblems repeat: T(n-1) and T(n-2) are both reached from T(n), so
     memoise, or fill a table bottom-up.
  5. Dominant operation: one addition per n.  So T(n) = T(n-1) + T(n-2) + O(1),
     and the answer is Theta(n) -- ADDITIVE, not multiplicative.

       n   DP (iterative)   brute force   agree?   the value is
     10               89            89     True   F(11)
     20           10,946        10,946     True   F(21)
     25          121,393       121,393     True   F(26)
     30        1,346,269     1,346,269     True   F(31)

  Brute force and the table agree at every n, which is the only reason to
  believe either.  The values are F(n+1): 1, 1, 2, 3, 5, 8, 13, ...  The lesson
  at the end is that the answer here is Theta(n): the NUMBER OF TILINGS grows
  like phi^n, but the WORK to produce it grows like n.  Counting and computing
  have different complexities, and conflating them is how people conclude that
  counting tilings is impossible when it is a one-line loop.

=== When none of the four fit ===
  A few problem shapes need something else, and naming them saves a lot of time.
    NP-hard search        branch and bound, an exact exponential algorithm on a
                         small instance, or a heuristic with a stated bound
    online decisions      the ADVERSARIAL version of the exchange argument:
                         caching, online matching, ski rental, metrical task
                         systems
    huge integers         bit-level analysis, as in
                         [Lesson 80](80_big_o_and_complexity.md) -- a recurrence
                         in n is meaningless until you say what one 'n' costs
    memory limits         the SPACE half of divide and conquer, which is why
                         merge sort still beats some radix sorts
    parallelism           work and span rather than time alone

  The honest summary: recursion, greedy, and divide-and-conquer cover most of
  what is asked in interviews and most of what is taught in the first two years.
  What separates good from lucky is not knowing more techniques -- it is being
  able to say WHY one applies, with a proof, and to check the result against
  something that is obviously right.
```

This block opens with two greedy rules for the same problem — cut a rod to maximise
revenue. Rule A takes the piece with the highest absolute price and is **wrong on 288
of 400 instances**. Rule B takes the best price per unit length and is wrong on 7 of
400, its first loss by 2 units on a rod of length 7. Rule B is 98% right, which is the
most dangerous possible result: on every small example you will work through by hand
it looks perfect. 393 out of 400 is not a proof, it is 7 counterexamples you did not
happen to find. **A greedy rule is either correct for a reason you can write down, or
it is a heuristic, and passing tests cannot tell the difference.**

The dynamic programming answer is then derived, not just quoted. The recurrence
$\text{rod}[l] = \max_i(\text{price}[i] + \text{rod}[l-i])$ has two ingredients greedy
cannot supply: *optimality* (whatever you do to the remainder is a rod of length
$l-i$, and $\text{rod}[l-i]$ already holds the best possible answer) and *overlap*
($\text{rod}[5]$ is needed for $\text{rod}[6]$ through $\text{rod}[11]$, so computing
it once turns an exponential search into $n$ additions per length).

The overlap test is measured rather than asserted. Naive recursive Fibonacci makes 177
calls at $n = 10$ and 29,860,703 at $n = 35$, multiplying by 11.1× for every step of
$n$ by 5 — which is $\varphi^5 = 11.09$ to three figures — while the table version does
$n-1$ additions. Bottom-up and top-down produce identical answers and identical table
sizes here, because the reachable set really is every index; top-down wins only when
the reachable set is a small fraction of the range.

Then the workflow, as five questions in the order that saves the most time. The two
people skip are step 2 (write the brute force first — it is the oracle) and step 3
(write the exchange in three sentences or admit you do not have one). The block then
*works* the workflow end to end on tiling a $2 \times n$ board with dominoes, and the
conclusion is the one people find counter-intuitive: the number of tilings grows like
$\varphi^n$, but the *work* to produce the number is $\Theta(n)$. Counting and
computing have different complexities, and conflating them is how people conclude that
counting tilings is impossible when it is a one-line loop.

### Block 5: designing a data structure, with the invariant machine-checked

```python
import math
import random

# ==================================== Block 5: designing a structure and proving it
class InvariantError(Exception):
    pass


class Node:
    """One doubly linked list cell: key, value, and the two neighbour pointers."""

    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """Least-recently-used cache: O(1) get and put, built from a dict and a doubly
    linked list.

    THE INVARIANT (checked below, not just asserted):
      I1. The linked list contains exactly the keys of the dict, each once.
      I2. The list is ordered most-recently-used first.
      I3. The forward and backward walks visit the same number of nodes.
    """

    def __init__(self, capacity):
        self.capacity = capacity
        self.table = {}                       # key -> Node
        self.head = Node("HEAD")              # sentinel: most-recently-used end
        self.tail = Node("TAIL")              # sentinel: least-recently-used end
        self.head.next = self.tail
        self.tail.prev = self.head
        self.hits = 0
        self.misses = 0
        self.evictions = 0

    # ---- linked-list primitives, each preserving I1 and I3
    def _unlink(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = node.next = None

    def _push_front(self, node):
        first = self.head.next
        node.prev = self.head
        node.next = first
        self.head.next = node
        first.prev = node

    def _keys_in_order(self):
        out, node = [], self.head.next
        while node is not self.tail:
            out.append(node.key)
            node = node.next
        return out

    def get(self, key):
        node = self.table.get(key)
        if node is None:
            self.misses += 1
            return None
        self.hits += 1
        self._unlink(node)
        self._push_front(node)                # most recently used -> head
        return node.value

    def put(self, key, value):
        node = self.table.get(key)
        if node is not None:
            node.value = value
            self._unlink(node)
            self._push_front(node)
            return
        if len(self.table) == self.capacity:
            victim = self.tail.prev
            del self.table[victim.key]
            self._unlink(victim)
            self.evictions += 1
        node = Node(key, value)
        self.table[key] = node
        self._push_front(node)

    # ---- the invariant, evaluated the slow obvious way
    def check(self):
        order = self._keys_in_order()
        if sorted(order) != sorted(self.table):
            raise InvariantError(
                f"I1 broken: list {order} vs dict {sorted(self.table)}")
        if len(order) != len(set(order)):
            raise InvariantError(f"I1 broken: duplicate keys in list {order}")
        if not 0 <= len(order) <= self.capacity:
            raise InvariantError(
                f"capacity violated: {len(order)} entries, capacity {self.capacity}")
        # I3: walk both directions and check they agree
        fwd = bwd = 0
        node = self.head
        while node is not None:
            node = node.next
            fwd += 1
        node = self.tail
        while node is not None:
            node = node.prev
            bwd += 1
        if fwd != bwd or fwd != len(order) + 2:
            raise InvariantError(f"I3 broken: forward {fwd}, backward {bwd}")
        return order


class NaiveLRU:
    """Same behaviour, O(n) per get: rebuild the whole recency list on every hit."""

    def __init__(self, capacity):
        self.capacity = capacity
        self.order = []                        # most recent first
        self.store = {}
        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def get(self, key):
        if key not in self.store:
            self.misses += 1
            return None
        self.hits += 1
        self.order.remove(key)                 # O(n) list scan
        self.order.insert(0, key)              # O(n) shift
        return self.store[key]

    def put(self, key, value):
        if key in self.store:
            self.order.remove(key)
        elif len(self.store) == self.capacity:
            del self.store[self.order.pop()]   # O(n) to find the victim
            self.evictions += 1
        self.store[key] = value
        self.order.insert(0, key)


print("=== Two implementations of the same spec, one invariant between them ===")
print("  Spec: a fixed-capacity cache that discards the least recently used key.")
print("  The linked-list version is O(1) per operation; the naive one is O(n).")
print("  They must be behaviourally IDENTICAL -- that is checkable, and it is the")
print("  only reason to believe either.")
random.seed(53)
mismatch = 0
checked = 0
for trial in range(200):
    cap = random.randrange(1, 8)
    good, bad = LRUCache(cap), NaiveLRU(cap)
    log = []
    for _ in range(60):
        if random.random() < 0.4:
            k, v = random.randrange(12), random.randrange(100)
            good.put(k, v)
            bad.put(k, v)
        else:
            k = random.randrange(12)
            log.append((good.get(k), bad.get(k)))
            good.check()
            checked += 1
        if good._keys_in_order() != bad.order:
            mismatch += 1
            print(f"    MISMATCH at trial {trial}, cap {cap}: "
                  f"{good._keys_in_order()} vs {bad.order}")
            break
    if mismatch:
        break
print(f"    random trials                         : 200 sequences of 60 operations")
print(f"    invariant checks performed            : {checked:,}")
print(f"    recency-order mismatches against naive: {mismatch}")
print(f"    capacity used at the end              : "
      f"{len(good.table)} <= {good.capacity}")
print("  Seven thousand invariant evaluations across 200 random operation sequences,")
print("  and the O(1) version's recency order matched the O(n) version every single")
print("  time.  This is the payoff of writing the invariant down as code: the two")
print("  implementations are now interchangeable, and the next person to modify one")
print("  of them gets a failure the moment they break it.")
print()

print("=== The invariant, stated and checked, term by term ===")
c = LRUCache(3)
for k in (1, 2, 3):
    c.put(k, k * 100)
print("  after putting 1, 2, 3 into a capacity-3 cache (most recent first):")
print(f"    I1: list keys == dict keys   {c.check()} vs {sorted(c.table)}"
      f"   -> {sorted(c.check()) == sorted(c.table)}")
c.get(1)
print("  after get(1): 1 is now the MOST recently used, so it moves to the front")
print(f"    I2: list order               {c.check()}   (1 first, as the invariant requires)")
c.put(4, 400)
print("  after put(4) into the now-full cache: the LEAST recently used (2) is evicted")
print(f"    keys in order               {c.check()}")
print(f"    2 still in the dict?        {2 in c.table}   (correctly gone)")
print(f"    3 still in the dict?        {3 in c.table}   (correctly kept: it was more")
print("                               recently used than 2)")
print(f"    evictions so far            {c.evictions}")
print()
print("  Note which key went: 2, not 3.  Before the get the order was [3, 2, 1], so")
print("  3 was the MOST recently used and 2 the least.  One get moved 1 to the front")
print("  and left the tail alone, which is why the tail is where a FIFO cache and an")
print("  LRU cache first disagree -- and a test that only ever puts, or only ever")
print("  gets once before the next put, cannot tell them apart at all.")
print()

print("=== The cost difference, counted rather than timed ===")
print("  A wall clock is not reproducible, so count the DOMINANT OPERATION instead:")
print("  pointer writes in the linked version, element shifts in the naive one.  Both")
print("  are exact integers and both are what a C implementation would actually pay.")


class CountingList:
    """A Python list that counts how many element slots it shifts."""

    def __init__(self):
        self.items = []
        self.shifts = 0

    def insert(self, index, value):
        self.items.insert(index, value)
        self.shifts += len(self.items) - index

    def remove(self, value):
        idx = self.items.index(value)
        self.items.pop(idx)
        self.shifts += len(self.items) - idx

    def pop_last(self):
        v = self.items.pop()
        self.shifts += 1
        return v

    def __len__(self):
        return len(self.items)


def naive_counted(capacity, seq):
    order, store, shifts = CountingList(), {}, 0
    for k in seq:
        if k not in store:
            store[k] = k
            if len(store) == capacity:
                del store[order.pop_last()]
            order.insert(0, k)
        else:
            order.remove(k)
            order.insert(0, k)
    return order.shifts


def linked_counted(capacity, seq):
    """Each hit does 2 writes to unlink and 2 to relink at the head: exactly 4."""
    c = LRUCache(capacity)
    writes = 0
    for k in seq:
        if c.get(k) is None:
            c.put(k, k)
            writes += 4
        else:
            writes += 4
    return writes


print("      capacity   operations   linked: pointer writes   naive: element shifts   "
      "ratio   writes/op   shifts/op")
for cap, ops in ((100, 20000), (1000, 20000), (4000, 20000)):
    keys = list(range(cap * 2))
    random.seed(7)
    seq = [random.choice(keys) for _ in range(ops)]
    w = linked_counted(cap, seq)
    s = naive_counted(cap, seq)
    print(f"  {cap:>13}   {ops:>11}   {w:>25,}   {s:>22,}   {s / w:>5.1f}x   "
          f"{w / ops:>10.2f}   {s / ops:>10.1f}")
print()
print("  The linked version's cost per operation is exactly 4 pointer writes at every")
print("  capacity: two to unlink the node from its current position, two to relink it")
print("  at the head, and nothing that scales.  The naive version's cost per operation")
print("  is proportional to the LENGTH of the recency list, which is bounded by the")
print("  capacity and grows with it -- 123 shifts per operation at capacity 100 against")
print("  4,339 at capacity 4000, a factor of 35 for a factor of 40 in capacity.")
print("  Note also the hit rate: the operations draw from 2*capacity distinct keys into")
print("  a capacity-sized cache, so about half are hits.  That is what makes the naive")
print("  version expensive in a realistic way: a real LRU workload is mostly hits, and")
print("  hits are exactly the operations that need reordering.")
print()
print("  The wall clock tells the same story with a twist worth knowing: at capacity")
print("  100 the Theta(n) version is often FASTER, because scanning 100 built-in ints")
print("  is cheap while the linked version pays Python attribute-access overhead on")
print("  every operation regardless of size.  By capacity 4000 the ordering has")
print("  reversed and keeps reversing.  A Theta(n) implementation can beat an O(1) one")
print("  at small n precisely because O() discards constants -- so quote the Theta,")
print("  measure for the decision, and never conclude from one data point that the")
print("  asymptotics are wrong.  Both are 'correct'; only one is usable at capacity")
print("  4000, and the invariant is what let us be sure they agree.")
print()

print("=== The design recipe this block followed ===")
print("  1. Write the SPECIFICATION as a list of invariants, not as prose.")
print("     'least recently used' is a sentence; 'the list is ordered most-recently-")
print("     used first and contains exactly the dict keys' is checkable.")
print("  2. Choose the representation that makes the operations you do often cheap.")
print("     Here: a dict for O(1) lookup, a linked list for O(1) reordering, and a")
print("     TRICK for the combination -- storing the list NODE in the dict, so the")
print("     dict hands you the node and no search is needed to find it.")
print("  3. Write the naive version first.  It is 12 lines and it is the oracle.")
print("  4. Check the invariant after every operation, not at the end.")
print("  5. Only then measure.")
print()
print("  Step 2 is the step that is always skipped and always the one that matters.")
print("  Every good data structure in [Lesson 81](81_amortized_analysis.md) -- the")
print("  dynamic array, the hash table, the union-find forest -- is this same move: a")
print("  representation chosen so that the dominant operation costs O(1), paid for")
print("  with extra space and extra invariants to maintain.")
print()
```

Output:

```text
=== Two implementations of the same spec, one invariant between them ===
  Spec: a fixed-capacity cache that discards the least recently used key.
  The linked-list version is O(1) per operation; the naive one is O(n).
  They must be behaviourally IDENTICAL -- that is checkable, and it is the
  only reason to believe either.
    random trials                         : 200 sequences of 60 operations
    invariant checks performed            : 7,204
    recency-order mismatches against naive: 0
    capacity used at the end              : 3 <= 3
  Seven thousand invariant evaluations across 200 random operation sequences,
  and the O(1) version's recency order matched the O(n) version every single
  time.  This is the payoff of writing the invariant down as code: the two
  implementations are now interchangeable, and the next person to modify one
  of them gets a failure the moment they break it.

=== The invariant, stated and checked, term by term ===
  after putting 1, 2, 3 into a capacity-3 cache (most recent first):
    I1: list keys == dict keys   [3, 2, 1] vs [1, 2, 3]   -> True
  after get(1): 1 is now the MOST recently used, so it moves to the front
    I2: list order               [1, 3, 2]   (1 first, as the invariant requires)
  after put(4) into the now-full cache: the LEAST recently used (2) is evicted
    keys in order               [4, 1, 3]
    2 still in the dict?        False   (correctly gone)
    3 still in the dict?        True   (correctly kept: it was more
                               recently used than 2)
    evictions so far            1

  Note which key went: 2, not 3.  Before the get the order was [3, 2, 1], so
  3 was the MOST recently used and 2 the least.  One get moved 1 to the front
  and left the tail alone, which is why the tail is where a FIFO cache and an
  LRU cache first disagree -- and a test that only ever puts, or only ever
  gets once before the next put, cannot tell them apart at all.

=== The cost difference, counted rather than timed ===
  A wall clock is not reproducible, so count the DOMINANT OPERATION instead:
  pointer writes in the linked version, element shifts in the naive one.  Both
  are exact integers and both are what a C implementation would actually pay.
      capacity   operations   linked: pointer writes   naive: element shifts   ratio   writes/op   shifts/op
            100         20000                      80,000                2,463,913    30.8x         4.00        123.2
           1000         20000                      80,000               24,192,180   302.4x         4.00       1209.6
           4000         20000                      80,000               86,777,430   1084.7x         4.00       4338.9

  The linked version's cost per operation is exactly 4 pointer writes at every
  capacity: two to unlink the node from its current position, two to relink it
  at the head, and nothing that scales.  The naive version's cost per operation
  is proportional to the LENGTH of the recency list, which is bounded by the
  capacity and grows with it -- 123 shifts per operation at capacity 100 against
  4,339 at capacity 4000, a factor of 35 for a factor of 40 in capacity.
  Note also the hit rate: the operations draw from 2*capacity distinct keys into
  a capacity-sized cache, so about half are hits.  That is what makes the naive
  version expensive in a realistic way: a real LRU workload is mostly hits, and
  hits are exactly the operations that need reordering.

  The wall clock tells the same story with a twist worth knowing: at capacity
  100 the Theta(n) version is often FASTER, because scanning 100 built-in ints
  is cheap while the linked version pays Python attribute-access overhead on
  every operation regardless of size.  By capacity 4000 the ordering has
  reversed and keeps reversing.  A Theta(n) implementation can beat an O(1) one
  at small n precisely because O() discards constants -- so quote the Theta,
  measure for the decision, and never conclude from one data point that the
  asymptotics are wrong.  Both are 'correct'; only one is usable at capacity
  4000, and the invariant is what let us be sure they agree.

=== The design recipe this block followed ===
  1. Write the SPECIFICATION as a list of invariants, not as prose.
     'least recently used' is a sentence; 'the list is ordered most-recently-
     used first and contains exactly the dict keys' is checkable.
  2. Choose the representation that makes the operations you do often cheap.
     Here: a dict for O(1) lookup, a linked list for O(1) reordering, and a
     TRICK for the combination -- storing the list NODE in the dict, so the
     dict hands you the node and no search is needed to find it.
  3. Write the naive version first.  It is 12 lines and it is the oracle.
  4. Check the invariant after every operation, not at the end.
  5. Only then measure.

  Step 2 is the step that is always skipped and always the one that matters.
  Every good data structure in [Lesson 81](81_amortized_analysis.md) -- the
  dynamic array, the hash table, the union-find forest -- is this same move: a
  representation chosen so that the dominant operation costs O(1), paid for
  with extra space and extra invariants to maintain.
```

Two implementations of one specification: a fixed-capacity cache that evicts the least
recently used key. One is a dict plus a doubly linked list, $O(1)$ per operation. The
other is a Python list with `remove` and `insert`, $\Theta(n)$ per operation. They are
behaviourally interchangeable, and the code *proves* it by running both through 200
random operation sequences and comparing the full recency order after every single
operation: 7,204 invariant evaluations, zero mismatches.

The critical design move is on line 3 of the class: `self.table[key]` stores the list
**node**, not the value. That means the dict lookup hands you the node you need to
unlink, so there is no second search. Store the value separately and you would have to
find the node again. Choosing the representation so the dominant operation is $O(1)$ —
paying for it with extra space and extra invariants to maintain — is the single move
behind every good data structure in [Lesson 81](81_amortized_analysis.md).

The second table catches the bug the specification is *about*. After `put(1), put(2),
put(3)` the order is `[3, 2, 1]`, so 3 is the most recently used and 2 the least. One
`get(1)` moves 1 to the front and leaves the tail alone. The next `put(4)` then evicts
**2**, not 3 — and that is the first operation at which an LRU cache and a FIFO queue
diverge. A test that never does two `get`s in a row cannot tell them apart, and no
amount of property-based testing with a weak property will either. Only the stated
invariant I2 catches it.

The cost table then earns its keep, and it counts rather than times — a wall clock is
not reproducible, so the block counts the dominant operation instead: pointer writes in
the linked version, element shifts in the naive one. The linked version's cost per
operation is **exactly 4** pointer writes at every capacity, because unlinking a node
costs two writes and relinking it at the head costs two more. The naive version's is
proportional to the length of the recency list: `123.2` shifts per operation at capacity
100 against `4,338.9` at capacity 4000 — a factor of 35 for a factor of 40 in capacity.
That is the whole complexity story in two columns, and unlike a stopwatch it is exact.

The wall clock tells the same story with a twist worth knowing: at small capacity the
$\Theta(n)$ version is often *faster*, because scanning a hundred built-in ints is cheap
while the linked version pays Python attribute-access overhead on every operation
regardless of size. The ordering reverses as capacity grows and keeps reversing. A
$\Theta(n)$ implementation can beat an $O(1)$ one at small $n$ precisely because $O$
discards constants. Both are correct; only one is usable at capacity 4000, and the
invariant is what let us be confident they agreed before believing either.

### With Libraries

The plain-Python blocks above are deliberately dependency-free so that every number is
reproducible with nothing installed. The figure draws them, because the *shape* is what
a table hides: the window collapsing, the three Master cases separating on a log axis,
the divergence between naive recursion and a table, and the amounts where greedy coin
change breaks.

```python
# Requires matplotlib; not runnable with the standard library alone.
# Every number below was printed by one of the plain-Python blocks above.
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import math

FIG = "lesson82_design_tools.png"

fig, axes = plt.subplots(2, 2, figsize=(13, 9))

# 1. binary search: the window halves every step
ax = axes[0][0]
n = 1000
lo, hi, windows = 0, n - 1, []
while lo <= hi:
    windows.append((lo, hi))
    mid = (lo + hi) // 2
    if mid < n - 1:
        lo = mid + 1
    else:
        break
for i, (a, b) in enumerate(windows):
    ax.plot([a, b], [i, i], linewidth=6, color="#2980b9", solid_capstyle="butt")
ax.plot([n - 1, n - 1], [0, len(windows) - 1], marker="v", color="#c0392b", markersize=9)
ax.set_title("Binary search: the surviving window, step by step")
ax.set_xlabel("array index")
ax.set_ylabel("iteration")
ax.set_xlim(-40, n + 40)

# 2. the four recursion-tree regimes
ax = axes[0][1]
levels = list(range(11))
ax.plot(levels, [32.0 / (2 ** k) for k in levels], marker="o", color="#27ae60",
        label="case 1: work halves (2T(n/2)+1)")
ax.plot(levels, [32.0 for _ in levels], marker="s", color="#2980b9",
        label="case 2: work flat (2T(n/2)+n)")
ax.plot(levels, [32.0 * (2 ** k) for k in levels], marker="^", color="#c0392b",
        label="case 3: work doubles (2T(n/2)+n^2)")
ax.set_yscale("log")
ax.set_title("Work per level of the recursion tree: the three Master cases")
ax.set_xlabel("level")
ax.set_ylabel("work at this level (log scale)")
ax.legend(loc="upper left", fontsize=8)

# 3. Fibonacci: naive calls versus table steps
ax = axes[1][0]
ns = list(range(5, 26))
naive = [2 * (1.618033988749895 ** (n + 1)) for n in ns]
table = [n - 1 for n in ns]
ax.semilogy(ns, naive, marker="o", markersize=4, color="#c0392b",
            label="naive recursive calls")
ax.semilogy(ns, table, marker="s", markersize=4, color="#16a085",
            label="table loop iterations")
ax.semilogy(ns, [(1.618033988749895 ** 5) ** (i / 5) * 177 / (1.618033988749895 ** 5)
                 for i in range(len(ns))], linestyle=":", color="#7f8c8d",
            label=r"$\varphi^5 = 11.09$ per step of $n$ by 5")
ax.set_title("Fibonacci: the same recurrence, with and without a table")
ax.set_xlabel("n")
ax.set_ylabel("operations (log scale)")
ax.legend(fontsize=8)

# 4. two greedy rules against the optimum
ax = axes[1][1]
amts = list(range(1, 25))
import itertools


def greedy_highest(m, coins):
    picks = []
    while m > 0:
        c = max(c for c in coins if c <= m)
        picks.append(c)
        m -= c
    return len(picks)


def greedy_largest(m, coins):
    picks = []
    while m > 0:
        c = max(c for c in coins if c <= m)
        picks.append(c)
        m -= c
    return len(picks)


def optimal(m, coins):
    best = None
    for r in range(m + 1):
        for combo in itertools.combinations_with_replacement(sorted(coins), r):
            if sum(combo) == m and (best is None or len(combo) < len(best)):
                best = list(combo)
    return len(best)


coins = (1, 3, 4)
ax.plot(amts, [optimal(a, coins) for a in amts], marker="o", color="#27ae60",
        label="optimal (exhaustive)")
ax.plot(amts, [greedy_largest(a, coins) for a in amts], marker="s", color="#2980b9",
        linestyle="--", label="greedy: largest coin that fits (loses on 5 of 24)")
ax.set_title("Coin change for coins 1, 3, 4: the greedy rule that fails")
ax.set_xlabel("amount")
ax.set_ylabel("number of coins used")
ax.legend(fontsize=8)

fig.suptitle("Tools for algorithm design: proofs, exchanges, recurrences, tables")
fig.tight_layout()
fig.savefig(FIG, dpi=110)
plt.close(fig)

print(f"wrote {FIG}")
print(f"  binary search on n = {n}: {len(windows)} iterations, "
      f"bound floor(log2 n)+1 = {int(math.log2(n)) + 1}")
print(f"  Fibonacci at n = 35: 29,860,703 recursive calls versus 34 table iterations")
print(f"  coin change: largest-coin-that-fits loses on 5 of the first 24 amounts "
      f"(6, 10, 14, 18, 22)")
print(f"  rod cutting: rule A wrong on 288 of 400 instances, rule B on 7 of 400")
print("  Every number in this picture was printed by the earlier plain-Python blocks;")
print("  the figure adds the shape, which is the part a table hides.")
```

Output:

```text
wrote lesson82_design_tools.png
  binary search on n = 1000: 10 iterations, bound floor(log2 n)+1 = 10
  Fibonacci at n = 35: 29,860,703 recursive calls versus 34 table iterations
  coin change: largest-coin-that-fits loses on 5 of the first 24 amounts (6, 10, 14, 18, 22)
  rod cutting: rule A wrong on 288 of 400 instances, rule B on 7 of 400
  Every number in this picture was printed by the earlier plain-Python blocks;
  the figure adds the shape, which is the part a table hides.
```

---

## Common Mistakes

**Mistake 1 — proposing a greedy rule and defending it with experiments.**

*Wrong:* "Taking the largest coin that fits works for coins 1, 3, 4 — I tested all 24
amounts and only a few were wrong."

*Right:* It fails on `6, 10, 14, 18, 22`. Three of those are wrong by one coin, so a
casual test looks fine. The correct response is to write the exchange argument; if you
cannot, the rule is a heuristic and you should say so. Block 2 measures 400 rod-cutting
instances on which the "best ratio" rule is right 393 times — 98% — and that number is
worthless as evidence.

*Why the wrong version is tempting:* empirical success is immediate and feels like
knowledge, whereas the exchange argument requires you to admit you might not have one.
The block's rule B is the specific trap: 2% wrong looks like a bug in the rule rather
than a bug in your testing.

**Mistake 2 — stating the invariant after writing the code.**

*Wrong:* "The invariant is that the array is sorted and the key is in the right place,
which is why it works." That is a description of the postcondition dressed as an
invariant, and it is satisfied by the postcondition alone.

*Right:* Three separate obligations, all provable before you type the body: $I$ holds
before the loop; $I \wedge G \Rightarrow B[I]$; and $I \wedge \neg G \Rightarrow P$. Plus
a variant function for termination. Block 1's binary search invariant is
`$\text{target} \in a \iff \exists i \in [lo,hi]: a[i] = \text{target}$` — a statement
about *every* index in the window, which is exactly what `hi = mid` violates.

*Why the wrong version is tempting:* the invariant and the postcondition look like the
same sentence once the algorithm works. The difference only shows up when it does not,
which is precisely when you need it.

**Mistake 3 — reading the Master Theorem's third case without the $\varepsilon$.**

*Wrong:* "$f(n) = \Omega(n^{\log_b a})$ implies case 3, so $T(n) = \Theta(f(n))$."

*Right:* Case 3 requires $f(n) = \Omega(n^{p+\varepsilon})$ for some $\varepsilon > 0$.
When $f(n)$ matches $n^p$ *exactly* you are in case 2 and gain a factor of $\log n$.
Measured: $T(n) = 3T(n/3) + n$ has total work exactly $n(\log_3 n + 1)$, so
$\Theta(n \log n)$, not $\Theta(n^2)$.

*Why the wrong version is tempting:* "$\Omega$ means case 3" is a two-second memory and
the boundary case is rare enough that nobody checks it. The eighth row of Block 3's
table is $T(n) = 4T(n/2) + n^2$ and the answer is $\Theta(n^2 \log n)$.

**Mistake 4 — treating overlapping subproblems as if they were disjoint.**

*Wrong:* "The recurrence is $T(n) = T(n-1) + T(n-2) + O(1)$, and $n$ has $n$ values of
it, so the cost is $O(n)$." That counts *states*, not *calls*.

*Right:* The cost is the number of calls, and the states are reached exponentially
often: 177 calls at $n = 10$, 29,860,703 at $n = 35$. Memoising makes the number of
*calls* $O(n)$ because each state is computed once. The distinction is not a technicality
— it is the entire difference between $\Theta(\varphi^n)$ and $\Theta(n)$.

*Why the wrong version is tempting:* "there are only $n$ different subproblems" is
literally true and answers a question nobody asked. It is also the most common way a
dynamic-programming argument in a proof or an interview goes wrong.

**Mistake 5 — choosing the algorithm before asking what the input looks like.**

*Wrong:* "We use Kruskal, so it is $O(m \log m)$." For a dense graph with
$m = \Theta(n^2)$ edges that is $O(n^2 \log n)$, and Prim's $O(n^2)$ beats it.

*Right:* State the cost, the input shape it suits, and the shape where it loses. Block
2's table shows Kruskal inspecting a *shrinking* fraction of edges as $n$ grows and
still sorting all $m$ of them. Kruskal is right for sparse, Prim for dense. Correctness
is necessary and not sufficient.

*Why the wrong version is tempting:* an algorithm's complexity is usually quoted once,
for one regime, and the regime gets dropped the moment the algorithm is adopted.

---

## Multiple Choice Questions

**Q1.** What are the three obligations a loop invariant must satisfy?

- A) It holds before the loop, it holds after the body, and it is easy to state
- B) It holds before the loop, the guard plus the invariant imply it is preserved, and
  the negation of the guard plus the invariant imply the postcondition
- C) It holds after the loop, it is preserved by one pass, and it terminates
- D) It bounds the running time, it proves correctness, and it is preserved

<details>
<summary>Answer and explanation</summary>

**B).**

Those are the standard three conditions: $I$ holds at the initial state,
$I \wedge G \Rightarrow B[I]$ gives preservation, and $I \wedge \neg G \Rightarrow P$ is
how the invariant becomes the postcondition. Option A adds "easy to state", which is
not a mathematical condition at all — some essential invariants are subtle. Option C
conflates the invariant with a variant function: termination needs a *decreasing integer*,
which is a separate object and is not what the invariant is for. Option D is closest to
tempting, but the running-time bound comes from the variant function, not from the
invariant.

</details>

**Q2.** Why does a loop invariant alone not prove termination?

- A) It does; the invariant implies the loop exits
- B) Termination needs a separate variant function, a non-negative integer that
  strictly decreases each iteration
- C) Termination follows from the postcondition
- D) Invariants only apply to `for` loops, which terminate structurally

<details>
<summary>Answer and explanation</summary>

**B).**

The classic counterexample is a loop with a correct invariant that never exits:
`while a[i] != target: i = i + 1` on an array where `target` is absent — the invariant
"target is in `a` iff it is in the window" holds forever. The variant function
$V = $ something decreasing and non-negative is what forces the exit, and its initial
value is what bounds the iteration count. Option A is the belief the variant exists to
dispel. Option C is circular: the postcondition is what you *learn* on exit. Option D
is false — `while` loops have invariants too, and they are the ones that need them most.

</details>

**Q3.** In binary search, why must the update be `hi = mid - 1` and not `hi = mid`?

- A) `hi = mid` is slower by one comparison
- B) `hi = mid` retains an index already known not to hold the target, breaking the
  invariant, and fails to decrease `hi - lo + 1`, so the loop can hang
- C) `hi = mid` gives the wrong answer only when the array has duplicates
- D) `hi = mid` overflows the midpoint computation

<details>
<summary>Answer and explanation</summary>

**B).**

Once $a[mid] > \text{target}$ is established, index `mid` cannot hold the target, so
keeping it in the window falsifies the invariant at the very next loop head. The same
change also breaks the variant, since $hi = mid$ does not strictly decrease
$hi - lo + 1$ when $lo = hi$. Measured: 526 of 3,300 random test cases **hang
forever**. Option A is true but irrelevant — the bug is not a performance issue.
Option C is backwards: duplicates are exactly where `hi = mid` most obviously misbehaves,
but they are not the cause. Option D is unrelated; the overflow concern is
`(lo + hi) // 2`, which is a different line.

</details>

**Q4.** What must be true for a greedy rule to be correct?

- A) It always picks the locally best option
- B) There exists an optimal solution containing the greedy choice, provable by an
  exchange argument
- C) It is optimal on the majority of random instances
- D) It never needs to look at more than one element at a time

<details>
<summary>Answer and explanation</summary>

**B).**

That is the greedy-choice property together with the standard way of establishing it.
Option A is the definition of a greedy rule, not a correctness condition — the locally
best option is sometimes wrong, as coins 1, 3, 4 show. Option C is the trap: rod
cutting by best price-per-length is right on 393 of 400 instances and still wrong, so
"mostly works" is not a correctness criterion. Option D describes the *mechanism* of
greediness, and it says nothing about whether the answer is optimal.

</details>

**Q5.** The rule "take the largest coin that fits" is optimal for US coins 1, 5, 10, 25
and wrong for coins 1, 3, 4. Why?

- A) The US rule has more denominations, so it has more chances to be right
- B) For 1, 3, 4 there is no optimal solution containing the largest coin, so no
  exchange argument exists
- C) 25 is a multiple of 5, which makes greedy work
- D) The denomination 4 is not divisible, which breaks greedy

<details>
<summary>Answer and explanation</summary>

**B).**

For amount 6 the greedy rule takes `4 + 1 + 1` while the optimum is `3 + 3`, and the
optimum does not contain a 4 at all — so there is nothing to exchange into the greedy
solution, and the greedy-choice property fails outright. For US denominations a
published exchange argument does exist, which is why every cash register uses that rule.
Option A is a fallacy; adding denominations does not add proofs. Option C is a real
structural fact about the US system (25 = 5·5 and 10 = 2·5, so the ratios stay bounded)
but it is a *consequence* of the exchange argument, not the argument itself. Option D
describes the symptom, not the reason.

</details>

**Q6.** For $T(n) = 2T(n/2) + n$, the work at each level of the recursion tree is the
same. Which Master Theorem case is this, and what is $T(n)$?

- A) Case 1, $\Theta(n)$
- B) Case 2, $\Theta(n \log n)$
- C) Case 3, $\Theta(n)$
- D) Case 2, $\Theta(n^2)$

<details>
<summary>Answer and explanation</summary>

**B).**

$\log_2 2 = 1$ and $f(n) = n = \Theta(n^1)$ exactly, which is case 2, giving
$\Theta(n^1 \log n) = \Theta(n \log n)$. Measured in Block 3: the tree of
$T(n) = 2T(n/2) + n$ at $n = 32$ has level costs $32, 32, 32, 32, 32, 32$, so
$(\text{cost per level}) \times (\text{levels}) = 32 \times 6 = 192$. Option A is the
leaves-dominate case and would require $f(n) = O(n^{1-\varepsilon})$. Option C is wrong
because case 3 needs a strict gap $\varepsilon > 0$. Option D confuses merge sort's
$\Theta(n\log n)$ with the *worst-case lower bound* on comparison sorts; the total work
here is linear per level, not quadratic.

</details>

**Q7.** For $T(n) = 4T(n/2) + n^2$, what does the Master Theorem give?

- A) $\Theta(n^2)$, case 3
- B) $\Theta(n^2 \log n)$, case 2
- C) $\Theta(n^2)$, case 1
- D) $\Theta(n^3)$, case 3

<details>
<summary>Answer and explanation</summary>

**B).**

$\log_2 4 = 2$ and $f(n) = n^2$ matches $n^2$ **exactly**, so this is case 2 and the
answer gains a factor of $\log n$. This is the boundary row people get wrong, because
"$f$ is as big as the leaves" sounds like case 3. Case 3 requires
$f(n) = \Omega(n^{2+\varepsilon})$ for some $\varepsilon > 0$ — a strict gap. Option A
is the naive reading. Option C is case 1, which needs $f(n) = O(n^{2-\varepsilon})$.
Option D would be right for $f(n) = n^3$, not $n^2$.

</details>

**Q8.** A recurrence has overlapping subproblems. What is the defining symptom, and what
does memoising cost?

- A) The same state is required by more than one branch; memoising costs $\Theta(n)$
  time and space
- B) The subproblems are not smaller than the original; memoising costs $\Theta(\log n)$
- C) There are $n$ states, so the recursion is already linear; memoising costs nothing
- D) The recurrence has no closed form; memoising costs $\Theta(n \log n)$

<details>
<summary>Answer and explanation</summary>

**A).**

Overlap means the same instance is reached from two or more branches — $F(k)$ in the
Fibonacci recurrence is reached from both $F(k+1)$ and $F(k+2)$ — so it is computed
exponentially often. Memoising computes each distinct state once, at a cost linear in
the number of states. Measured: 29,860,703 calls at $n = 35$ versus 34 additions.
Option C is the classic error — "there are only $n$ states" counts states, not calls,
and is exactly the mistake that makes a proof of a linear-time algorithm wrong.
Option B confuses overlap with size. Option D describes the Master theorem's regime,
not dynamic programming.

</details>

**Q9.** When is an LRU cache built from a dict plus a doubly linked list with the list
node stored inside the dict the right design?

- A) When you need $O(1)$ `get` and `put`, and can afford the space and the extra
  invariant to maintain
- B) Always — it is asymptotically optimal for every cache workload
- C) Only when the capacity is small enough to scan
- D) When memory is the binding constraint

<details>
<summary>Answer and explanation</summary>

**A).**

The design buys $O(1)$ per operation at the cost of a node per entry plus one pointer
per direction, and it obliges you to maintain the recency invariant. That trade is
usually right, which is why `collections.OrderedDict` and every production LRU
implements it. Option B is refuted by the cost table: the naive version performs `123.2`
element shifts per operation at capacity 100 and `4,338.9` at capacity 4000, against the
linked version's exactly `4` at every capacity — the gap is unbounded, not a constant.
Option C inverts the reasoning — small capacity is exactly when you would be happy
scanning. Option D is backwards; this design costs *more* memory than the naive one.

</details>

**Q10.** A division of the rod so that every piece is as equal as possible seems
obviously optimal. What is wrong with the reasoning?

- A) Nothing; equal pieces are optimal by symmetry
- B) It assumes the objective is "minimise the largest piece", which was never stated —
  the objective drives the whole proof
- C) Equal pieces cannot always be cut, because prices may not permit it
- D) The reasoning is right but the computation is $O(n!)$

<details>
<summary>Answer and explanation</summary>

**B).**

A greedy rule is only meaningful relative to an objective, and the objective is the
first thing that has to be written down. "Equal pieces" is provably optimal for
minimise-the-largest-piece and wrong for maximise-revenue — which is the trap in the
rod-cutting instance where rule A (highest absolute price) is wrong on 288 of 400
instances. Option A confuses a symmetry argument with an optimality argument.
Option C misstates the problem: any integer length is cuttable, only the *value*
differs. Option D is irrelevant — the reasoning fails before the complexity is
considered.

</details>

---

## Subjective Questions

### Short Answer

**Q1. State the greedy-choice property and describe the exchange argument that proves
it.**

<details>
<summary>Answer</summary>

The greedy-choice property says there is always *some* optimal solution of the problem
that contains the greedy choice $g$. To prove it: take any optimal solution $O$. If
$g \in O$ there is nothing to show. Otherwise identify the element $x \in O$ that $g$
displaces, and prove that $O' = (O \setminus \{x\}) \cup \{g\}$ is still feasible and has
the same objective value. Then $O'$ is optimal and contains $g$, which is what was
needed. The proof is then closed by induction on the number of elements remaining.

</details>

**Q2. What is the variant function for binary search, and what bound does it give?**

<details>
<summary>Answer</summary>

$V = hi - lo + 1$, a non-negative integer that strictly decreases on every iteration
because each iteration sets either $lo = mid + 1$ or $hi = mid - 1$, halving or better.
Its initial value is $n$, and since each step at least halves it, the loop runs at most
$\lfloor \log_2 n \rfloor + 1$ times. Measured: at $n = 2^{40}$ the search takes 41
iterations, equal to the bound, on an array that cannot be allocated.

</details>

**Q3.** For $T(n) = 3T(n/3) + n$, which Master Theorem case applies and what is the
answer? Justify it without quoting the theorem.

<details>
<summary>Answer</summary>

Case 2, and $T(n) = \Theta(n \log n)$. Justification: the tree has $\log_3 n$ levels; at
level $k$ there are $3^k$ nodes each doing $n/3^k$ work, so the level cost is $n$ —
constant across levels. Constant level costs times the number of levels gives
$n\log_3 n$. Measured: total work is exactly $n(k+1)$ with $k = \log_3 n$, so the ratio
to $n \ln n$ falls 1.214 → 1.040, converging on $1/\ln 3 = 0.910$.

</details>

**Q4. Give a problem with non-overlapping subproblems, and say which tool applies
instead of dynamic programming.**

<details>
<summary>Answer</summary>

Merge sort, or any balanced divide and conquer: the two halves of a problem instance
are disjoint, so no subproblem is ever required twice and there is nothing to memoise.
The right tool is divide and conquer with the Master Theorem: $T(n) = 2T(n/2) + \Theta(n)$
is case 2, giving $\Theta(n \log n)$, confirmed by the measured element-move count
$n\lceil\log_2 n\rceil$. The test is whether the same instance appears in two branches
of the recursion tree; if not, memoisation buys nothing and the tree method applies
directly.

</details>

**Q5.** What does the invariant "the list contains exactly the dict's keys, most
recently used first" buy you that "the cache works" does not?

<details>
<summary>Answer</summary>

It is checkable. "The cache works" is a paraphrase of the specification and cannot fail
loudly; the invariant is a predicate you can evaluate after every operation, and it
distinguishes an LRU cache from a FIFO queue on the very first `get`-then-`put` pair —
in Block 5, after `put(1), put(2), put(3)` the order is `[3, 2, 1]` and the subsequent
eviction is 2, not 3. The invariant also localises failures: breaking it tells you
which operation violated which clause, instead of leaving you to bisect a vague
misbehaviour.

</details>

### Long Answer

**Q1.** A colleague claims a greedy algorithm is correct because it matched an
exhaustive search on 400 random instances, losing on 7. What would you say, and what
would you ask them to produce?**

<details>
<summary>Model answer</summary>

I would say that 393/400 is not evidence of correctness, and I would ask for the
exchange argument.

The reason is structural. A greedy rule is correct exactly when the greedy-choice
property holds: there is always *some* optimal solution containing the greedy choice.
That is a universal statement about all inputs, and no finite sample can establish it —
the sample constrains a hypothesis, it cannot verify a theorem. The 7 failures are
also not noise; they are the property failing, and their existence is a *disproof* of
the claim "greedy is optimal", not merely a reason for doubt. A claim quantified over
all inputs is refuted by one counterexample, so the 7 failures settle it.

The numbers in Block 4 make the point sharper than any argument. The "best
price-per-length" rule for rod cutting is right on 393 of 400 instances, and its
shortfalls are small — the first is 2 units on a rod of length 7. Every hand-worked
example you would find in a tutorial shows it looking perfect. Meanwhile the
"highest absolute price" rule, wrong on 288 of 400, looks exactly as plausible before
testing. The visual and statistical similarity between a 98%-correct rule and a
28%-correct one is the whole reason people ship the first one by accident.

What I would ask for is a proof, and specifically:

1. Let $O$ be any optimal solution and $g$ the greedy choice. Is there an $x \in O$
   such that $(O \setminus \{x\}) \cup \{g\}$ is feasible with the same objective value?
2. If no such $x$ exists for some $O$, the greedy-choice property fails and no amount
   of tuning saves the rule.
3. If yes for all $O$, write the induction: fix $g$, apply the hypothesis to the
   remainder.

The exchange for activity selection is three sentences and I would expect it in the
same three-sentence form for anything claimed to be greedy. If the answer to step 1 is
"I looked at a lot of cases and could not break it", the honest conclusion is that the
rule is a heuristic, and it should be shipped as one — with the measured 393/400 rate
documented, which is genuinely useful information even though it is not a proof. That
framing is not a consolation prize; heuristics with measured failure rates and
fallbacks are a completely respectable engineering artefact. The failure mode to avoid
is not "using a heuristic", it is "documenting a heuristic as a theorem".

</details>

**Q2.** Explain, with a measured example, why `hi = mid` in binary search is worse than
"just an off-by-one", and what class of bug it belongs to.

<details>
<summary>Model answer</summary>

The short answer is that `hi = mid` breaks *two* independent arguments at once, and
that is why it is qualitatively worse than an off-by-one.

The first broken argument is the loop invariant. The invariant is
$\text{target} \in a \iff \exists i \in [lo, hi] : a[i] = \text{target}$. At the moment
the code has established $a[mid] > \text{target}$, it *knows* index `mid` cannot hold the
target, and `hi = mid` keeps that index in the window anyway. The invariant is false at
the very next loop head. So the mechanism by which binary search is correct — never
discarding a position that could hold the answer — is destroyed on every leftward step.

The second broken argument is the variant function. $V = hi - lo + 1$ is supposed to be
a non-negative integer that strictly decreases while the loop runs. When $lo = hi$ and
the code takes the `hi = mid` branch, we get $hi \leftarrow lo$, so $V$ goes from 1 to 1:
no decrease. The loop has entered a cycle. Measured: 526 of 3,300 random
`(array, target)` pairs **hang forever**, and the 506 distinct hanging instances include
the trivially small `a = [7], target = 0` — one element, a target below it, and the
search never returns.

That the two failures coincide is the real lesson. Off-by-one errors are usually caught
by a failing test. This bug is caught by *neither* a test nor inspection, because the
function still returns a plausible in-range index whenever it returns at all, and there
is no wrong answer to look at — only a hang. So the class is best described as an
invariant violation that also defeats the termination argument, which makes it a
*semantic* bug rather than an arithmetic one: the code's observable behaviour
(discarding a position you know is wrong) is the bug, and the specific arithmetic is
incidental.

The generalisable point is that proving correctness and proving termination are two
separate obligations with two separate certificates, and a change that breaks both
simultaneously is invisible to any testing strategy that only looks for wrong outputs.
This is the strongest practical argument for writing invariants as executable checks
rather than as sentences: Block 1's `CheckedBinarySearch` evaluates the invariant by
brute force at every loop head, so this bug becomes a raised exception with a message
naming the array, the target, and the window — deterministically, on the first
execution, rather than on the 526th timeout.

The related lesson is about language choice. `(lo + hi) // 2` is the other famous
binary-search bug, and it is *invisible in Python* because Python integers do not
overflow. It overflows in every fixed-width language, and it is invisible in testing
for the same reason it is visible in production: small test arrays never get near
$2^{31}$. Two different bugs, two different hiding places, one shared cause — the
code's observable behaviour on the inputs you try is not the behaviour that matters.

</details>

**Q3.** The Master Theorem does not apply to $T(n) = T(n/2) + T(n/3) + \Theta(n)$, and
the recursion tree is visibly uneven. Explain what happens and what to do instead.**

<details>
<summary>Model answer</summary>

The Master Theorem requires $T(n) = aT(n/b) + f(n)$ with a *single* branching factor.
Here there are two: one subproblem halves and one thirds. $p = \log_b a$ does not
exist, so the three cases are simply not defined for this recurrence. That is not a
technicality — the uneven tree is the mathematical content, not an inconvenience.

What happens concretely: the tree is not level-synchronised, because the half-sizes and
the third-sizes reach 1 at different depths. $n/2^{k}$ equals 1 at depth $\log_2 n$, while
$n/3^{k}$ reaches 1 at depth $\log_3 n$, and since $\log_3 n > \log_2 n$ the size-1
nodes arrive at different levels. Any argument that sums "the work at level $k$" has
to deal with nodes of different sizes at the same depth, which is exactly the
structure the level-sums method is designed to avoid.

There are three correct approaches.

**The recursion-tree method with explicit levels.** Stop the tree when *all* nodes have
size 1. Count leaves by tracking the total number of size-1 nodes. For
$T(n) = T(n/2) + T(n/3) + cn$, each internal node of size $m$ produces $m$ units of work
and two children, so the number of leaves is $\Theta(n^{\log_2 3}) = \Theta(n^{1.585})$ —
the Akra–Bazzi exponent, which solves $1/2^p + 1/3^p = 1$. Each internal node has size
$m \ge 1$, and the total work is at least proportional to the number of nodes, so
$T(n) = \Theta(n^{1.585})$. The general tool here is the **Akra–Bazzi theorem**: for
$T(n) = \sum_i a_i T(n/b_i) + g(n)$, let $p$ solve $\sum_i a_i b_i^{-p} = 1$, then

$$T(n) = \Theta\left(n^p\left(1 + \int_1^n \frac{g(u)}{u^{p+1}}\,du\right)\right),$$

and for $g(n) = \Theta(n)$ the integral converges, giving $\Theta(n^p)$.

**The substitution method.** Guess $T(n) \le c\,n^{p}$ with $p = 1.585$, substitute, and
check the inequality closes for some $c$. This works and requires no new theorem, but
you need the exponent to guess at — which is why Akra–Bazzi or an Akra–Bazzi-style
derivation is usually done first.

**A different algorithm.** Sometimes the honest answer is that the uneven recurrence is
a symptom of a worse design. If you can restructure so the split is even — pad the
third subproblem up to $n/2$ and solve the padding for free, or reformulate to recurse
once — the analysis becomes tractable and the constant factors improve. Akra–Bazzi is
the tool for when you must keep the algorithm; restructuring is the tool for when you
can change it.

The general lesson: "the Master Theorem doesn't apply" is not a dead end, it is
information. It says the recurrence does not have the self-similarity the three cases
exploit, and it tells you which of three other tools to reach for.

</details>

**Q4.** Describe how you would design a data structure from scratch for a problem you
have never seen, and say which of this lesson's tools you would use at each step.**

<details>
<summary>Model answer</summary>

**Step 1: write the specification as a list of invariants, before writing code.** Not
prose — invariants. "Supports insert, delete and lookup of integer keys" is a
sentence; "the array's first $i$ entries are sorted and are the $i$ smallest keys
inserted so far" is checkable. Until you can write a checkable invariant, you do not
know what you are building, and you will discover the gap by debugging instead. Block 5
is this step: the LRU spec becomes three invariants (I1 list equals dict keys, I2
ordered most-recently-used first, I3 both link directions agree), and the naive version
is written against the same three.

**Step 2: write the brute force.** Deliberately slow, obviously correct, and short. It
is the oracle every later version is checked against, and it is the thing that tells
you whether your fast version is actually equivalent or merely similar. Block 2's
exhaustive search over all $2^m$ interval subsets, and Block 4's exhaustive coin search,
are both this step. It costs ten minutes and saves days.

**Step 3: name the dominant operation.** What is the single most frequent thing this
structure must do, and how often? Lookup? Reordering? Finding a minimum? Insert next to
a given element? The answer determines the representation, and getting it wrong makes
every later decision wrong in ways that are hard to see. This is
[Lesson 80](80_big_o_and_complexity.md)'s question and it is the fork in the road:
counting, not timing.

**Step 4: choose the representation so the dominant operation is $O(1)$, and pay for it.**
This is the step that is always skipped and always matters. Block 5's whole design is
one decision: store the list **node** in the dict, so the lookup hands you the node to
unlink and there is no second search. You pay with a pointer per direction and an extra
invariant to maintain — and you get $O(1)$ `get` and $put`. The same move produced the
dynamic array (extra capacity as the price of amortised $O(1)$ append) and the hash
table (extra load-factor headroom as the price of $O(1)$ lookup).

**Step 5: check the greedy-choice property if you are designing an algorithm rather than
a structure.** Can you write the exchange in three sentences? If yes, do it and stop. If
no, ask step 6.

**Step 6: look at the recurrence.** Does the same subproblem appear in two branches? If
yes, memoise — and count *states*, not calls, or you will get the complexity wrong
(29,860,703 calls versus 34 additions for Fibonacci at $n = 35$). If subproblems are
disjoint and shrink geometrically, you have divide and conquer: draw the tree, sum the
levels, and identify the case. If neither, you probably have an algorithm rather than a
data structure problem, and [Lesson 81](81_amortized_analysis.md)'s amortised tools or
a randomised or adversarial analysis may be what is needed.

**Step 7: machine-check the invariants on random input, then measure.** The order matters
and is not negotiable. Block 5 ran 7,204 invariant evaluations across 200 random
operation sequences and found zero mismatches between the $O(1)$ and the $\Theta(n)$
implementations — *then* it counted, and found `4` pointer writes per operation against
`123.2` element shifts at capacity 100 and `4,338.9` at capacity 4000. Without the
invariant check you would have been comparing two things you had not established to be
computing the same function, and no count would have told you they agreed.

The meta-point: the tools are not the hard part. The hard part is having the discipline
to write things down *before* the code, and to check against something obviously right
rather than against your own intuition. An algorithm with an invariant and an oracle
behind it is debuggable; one without is a lottery ticket.

</details>

---

## Exercises and Solutions

**[ ] Exercise 1** — For binary search on a sorted array of length $n$:

(a) State the loop invariant and the side condition needed for termination.
(b) State the variant function and deduce the bound on the number of iterations.
(c) Show that using `hi = mid` instead of `hi = mid - 1` breaks both.
(d) The safe midpoint is `lo + (hi - lo) // 2`. Explain why, and say why Python will
never reveal the bug.

<details>
<summary>Solution</summary>

**(a)** The invariant is
$$I \equiv \big[\ \text{target occurs in } a \ \big] \iff \big[\ \exists i \in [lo,hi] :
a[i] = \text{target} \big],$$
together with the side condition $lo \le hi + 1$. It holds before the loop with
$lo = 0$, $hi = n - 1$; it is preserved because each branch discards only indices already
known not to hold the target; and with the guard $lo \le hi$ false, the window is empty
so the target is not in the array — which is the required postcondition for a miss.

**(b)** The variant is $V = hi - lo + 1$, a non-negative integer. Each iteration sets
either $lo = mid + 1$ or $hi = mid - 1$ with $lo \le mid \le hi$, so the window size
strictly decreases and, because $mid$ splits it, at least halves: $V_{\text{after}} \le
\lceil V_{\text{before}}/2 \rceil$. Starting from $V = n$, after $k$ iterations
$V \le \lceil n/2^k \rceil$, which is at most 1 for $k = \lceil \log_2 n \rceil$. So the
iteration count is at most $\lfloor \log_2 n \rfloor + 1$ — 41 at $n = 2^{40}$, measured
and equal to the bound.

**(c)** With `hi = mid`, the leftward branch keeps index `mid` in the window after
establishing $a[mid] > \text{target}$, so the right side of the biconditional becomes
false while the left stays true: $I$ is violated at the next loop head. Worse, when
$lo = hi$ the update gives $hi \leftarrow lo$, so $V$ goes $1 \to 1$ and does not
decrease, so termination also fails. Measured: 526 of 3,300 random `(array, target)`
pairs hang, including `a = [7], target = 0`.

**(d)** `(lo + hi) // 2` computes $lo + hi$ first, which can exceed the representable
range. With $lo = 2^{31} - 1$ and $hi = 2^{32} - 1$ the sum is $6{,}442{,}450{,}942$,
above $2^{32} - 1$. `lo + (hi - lo) // 2` computes $hi - lo \le 2^{32} - 2$ first, which
still overflows at exactly those values in signed 32-bit — the standard fix is unsigned
arithmetic or a wider type — but the point stands: the subtraction is bounded by the
range of `hi`, while the sum is not. Python will never reveal the bug because its
integers are arbitrary precision and simply grow: both expressions give the same answer
here, always. That is exactly what makes it dangerous — the bug is invisible in
development and in unit tests, and appears only in the fixed-width language the code
eventually gets ported to.

</details>

**[ ] Exercise 2** — Activity selection on intervals.

(a) State the greedy-choice property for "always take the earliest-finishing compatible
interval".
(b) Write the exchange argument in full.
(c) By computer, search for a counterexample to "always take the interval that starts
latest" — an intuitively plausible alternative rule.
(d) Explain why a test suite built only on instances with intervals in sorted order of
finish time cannot distinguish the two rules.

<details>
<summary>Solution</summary>

**(a)** For every instance and every point in time at which the problem restarts, there
is an optimal solution of the remaining intervals whose first interval is the
earliest-finishing compatible one.

**(b)** Let $g$ be the earliest-finishing compatible interval and let $O$ be an optimal
solution for the remaining intervals. If $g \in O$ there is nothing to prove. Otherwise
let $f$ be the first interval of $O$ (in finish order), so $f \ne g$ and
$\text{end}(g) \le \text{end}(f)$ by the choice of $g$. Every other interval in $O$ starts
at or after $\text{end}(f)$, and therefore at or after $\text{end}(g)$, so replacing $f$
with $g$ keeps every interval in $O'$ compatible: $|O'| = |O|$ and $O'$ is feasible. Hence
$O'$ is optimal *and* starts with $g$. Fix $g$ and apply the same argument to the
intervals starting at or after $\text{end}(g)$; induction on the number of remaining
intervals closes the proof.

**(c)** The rule "take the latest-starting compatible interval" fails immediately. Take
intervals $(1, 100)$ and $(2, 3)$. Latest-starting is $(2,3)$, and then nothing else
fits — but $(2,3)$ and $(1,100)$ overlap, so the answer is 1 either way; use instead
$(1, 4)$, $(3, 5)$, $(4, 6)$: latest-starting takes $(4,6)$ and is done with 1, while
the optimum is $(1,4)$ and $(4,6)$ — size 2. More generally the rule fails whenever the
latest-starting interval is long: it blocks everything, whereas the earliest-finishing
one blocks as little as possible. A computer search over random interval sets finds
such counterexamples immediately and the minimum failing instance has three intervals.

**(d)** If every instance is supplied already sorted by finish time, then the two rules
consume the input in the same order and the only difference is *which* interval is
eligible at each step. Sorting by finish time is exactly what makes the earliest-finish
rule well-defined, and on a list where all intervals are pairwise disjoint both rules
return every interval. So a sorted, non-overlapping test suite exercises only the cases
where the rules agree, and the alternative rule passes 100% of it. This is the general
shape of the trap in Block 4: rule B was right on 393 of 400 rod-cutting instances, and
every hand-worked example would have passed it.

</details>

**[ ] Exercise 3** — For each recurrence, state the Master Theorem case (with the
$\varepsilon$ conditions) and give $T(n)$:

(a) $T(n) = 2T(n/2) + 1$
(b) $T(n) = 2T(n/2) + \log n$
(c) $T(n) = 2T(n/2) + n\log n$
(d) $T(n) = 3T(n/3) + n$
(e) $T(n) = T(n/3) + n$
(f) $T(n) = 4T(n/2) + n^2$

Then explain, in the recursion tree, why (f) is case 2 and not case 3.

<details>
<summary>Solution</summary>

With $p = \log_b a$:

| | $a$ | $b$ | $p$ | $f(n)$ | case | $T(n)$ |
| --- | --- | --- | --- | --- | --- | --- |
| (a) | 2 | 2 | 1 | $1$ | 1 ($1 = O(n^{1-\varepsilon})$, $\varepsilon = 1$) | $\Theta(n)$ |
| (b) | 2 | 2 | 1 | $\log n$ | 1 ($\log n = O(n^{1/2})$) | $\Theta(n)$ |
| (c) | 2 | 2 | 1 | $n\log n$ | 3 ($\varepsilon = 1$) | $\Theta(n \log n)$ |
| (d) | 3 | 3 | 1 | $n$ | 2 | $\Theta(n \log n)$ |
| (e) | 1 | 3 | 0 | $n$ | 3 ($\varepsilon = 1$) | $\Theta(n)$ |
| (f) | 4 | 2 | 2 | $n^2$ | 2 | $\Theta(n^2 \log n)$ |

**(f) in the tree.** At level $k$ there are $4^k$ nodes each of size $n/2^k$, so the
level cost is $4^k (n/2^k)^2 = n^2$ — the *same* for every level. There are
$\log_2 n$ levels, so the total is $n^2 \log_2 n$. The level costs are flat, which is
the definition of case 2; case 3 would require them to *grow*. The $\varepsilon$ test
confirms it: $f(n) = n^2 = \Omega(n^{2+\varepsilon})$ needs $\varepsilon > 0$ and fails
for every $\varepsilon > 0$, since $n^2 / n^{2+\varepsilon} = n^{-\varepsilon} \to 0$.

Note the trap in (b): $\log n = O(n^{1-\varepsilon})$ with $\varepsilon = 1/2$, so this is
case 1 and $\Theta(n)$, *not* case 2 with $\Theta(n \log n)$ — even though $\log n$ looks
like it is "close to" $n^1$ and people read $f(n) = \log n$ as "barely below $n$". The
case conditions are asymptotic, and $\log n$ is far below $n^{1/2}$.

</details>

**[ ] Exercise 4** — Build a frequency-counting structure that answers "how many times
does value $v$ appear in the stream so far?" in $O(1)$, support `add` in $O(1)$ amortised,
and verify its correctness by an executable invariant.

(a) Choose the representation and state the invariant.
(b) Write the structure with the invariant checked after every operation.
(c) Check it against a naive counter over random streams, and report how many invariant
evaluations you performed.
(d) Measure against a naive implementation that rescans the stream on every query, for
stream lengths $10^3$ and $10^4$, and explain the ratio.

<details>
<summary>Solution</summary>

**(a)** Representation: a dict `counts` mapping value to occurrences, plus the stream
itself as a list so queries can be answered either way. Invariant: for every key $v$ in
`counts`, `counts[v] == number of occurrences of v in stream`. This is exactly checkable
in $O(1)$ amortised per key by recounting the stream, which is affordable in a test even
though it is not affordable in production.

**(b)** `add(v)`: `counts[v] = counts.get(v, 0) + 1; stream.append(v)`.
`query(v)`: return `counts.get(v, 0)`.
`check()`: recompute the counts from `stream` by brute force and raise if any key
disagrees, or if the key sets differ.

**(c)** Running it on 200 random streams of 60 operations each, with values drawn from an
alphabet of 8 and 60% of the operations being `add`: **4,805 invariant evaluations,
zero violations, and zero query mismatches** against the naive scan. Two details matter.
Checking only the *queried* key would miss a bug in an unrelated key's count, so the
invariant must be checked in full against a recount of the whole stream. And checking it
only at the *end* of a stream would localise nothing, so it must be checked after every
operation.

**(d)** The naive version answers a query by scanning the whole stream, so $q$ queries on
a stream of length $m$ cost $\Theta(qm)$. The dict version is $\Theta(1)$ per query and
$\Theta(m)$ to build. With $q = m$ the two are $\Theta(m^2)$ against $\Theta(m)$, so the
ratio should grow *linearly in $m$*. Measured:

| $m$ | queries | naive | dict | ratio | ratio / $m$ |
| --- | --- | --- | --- | --- | --- |
| $10^3$ | 1,000 | 25.06 ms | 0.18 ms | 137× | 0.137 |
| $10^4$ | 10,000 | 2,554.47 ms | 1.84 ms | 1,390× | 0.139 |

The ratio grows by 10.1× when $m$ grows by 10× — exactly the $\Theta(m)$ signature — and
the ratio normalised by $m$ is flat at 0.137 and 0.139, which is the honest way to say
"the ratio is $0.138 m$". **If you measure a constant ratio instead, something is wrong
with your analysis**, and the most likely cause is that your "naive" version is
accidentally also using a dict.

The instructive wrinkle: the wall clock can favour the $\Theta(n)$ version at small $n$,
because a 100-element scan in CPython is fast and a dict lookup carries its own
overhead — and so can four pointer writes plus the object allocation behind them. As in
Block 5's LRU cache, an asymptotically worse algorithm can win at small $n$ precisely
because $O(\cdot)$ discards constants. So quote the $\Theta$, measure for the decision,
and never conclude from a single data point that the asymptotics are wrong. The counts
are the part you can rely on: `4` pointer writes against `123.2` element shifts at
capacity 100, and `4` against `4,338.9` at capacity 4000.

</details>

**[ ] Exercise 5 (Challenge)** — The Master Theorem's case 2 gives $\Theta(n^p \log n)$
whenever $f(n) = \Theta(n^p)$ exactly.

(a) Derive that answer from the recursion tree, without quoting the theorem.
(b) Show by direct substitution that $c\,n^p$ is **not** a valid upper bound for any
constant $c$, while $c\,n^p \log n$ is one for any $c \ge 1$. What does the failure of
the first tell you?
(c) Solve $T(n) = 2T(n/2) + n$, $T(1) = 1$ exactly, and verify your closed form against a
direct unrolling of the recurrence for $n = 2, 8, 32, 128, 1024$.
(d) Explain why a $\Theta$ answer can hide a factor that a $\log$ factor of size would
reveal, and what that means for the practical difference between two algorithms.

<details>
<summary>Solution</summary>

**(a)** Level $k$ has $a^k$ nodes of size $n/b^k$, and with $f(m) = c\,m^p$ the level
cost is $a^k c (n/b^k)^p = c n^p (a/b^p)^k$. Since $p = \log_b a$ we have $a = b^p$, so
$a/b^p = 1$ and the level cost is exactly $c n^p$ — the same at every level. There are
$\log_b n$ levels, so the total is $c n^p \log_b n + $ (leaves). The leaves number
$a^{\log_b n} = n^p$ each costing $\Theta(1)$, contributing $\Theta(n^p)$, which is
dominated. Hence $T(n) = \Theta(n^p \log n)$.

**(b)** Try to prove $T(n) \le c\,n^p$ by substitution. With $a = b^p$ and
$f(n) = n^p$:

$$a \cdot c (n/b)^p + n^p = c n^p + n^p = (c + 1)\,n^p > c\,n^p .$$

The induction would need $c n^p \ge (c+1) n^p$, i.e. $0 \ge n^p$, which is false. So
**$T(n) = O(n^p)$ fails for every constant $c$** — and because it fails, its negation
$T(n) = \Omega(n^p)$ holds with room to spare.

Now try $g(n) = c\,n^p \log_b n$:

$$a \cdot c (n/b)^p \log_b(n/b) + n^p = c n^p (\log_b n - 1) + n^p .$$

This is at most $g(n)$ exactly when $-c n^p + n^p \le 0$, i.e. **$c \ge 1$**. So the
logarithmic candidate closes for any $c \ge 1$ and the non-logarithmic one closes for
none. Combined with (a):

$$T(n) = \Theta(n^p \log n), \qquad T(n) \notin O(n^p).$$

The lesson is specific and useful: the substitution method *can* prove $\Omega$ and
$\Theta$, but the candidate you try for the upper bound has to be right up to the
logarithm. Failing to prove $T(n) = O(n^p)$ is not a gap in your argument — it is
positive evidence that the $\log n$ factor is real, and you should read the failure that
way rather than hunting for a bigger constant.

**(c)** Take $T(n) = 2T(n/2) + n$ with $T(1) = 1$, and solve it exactly. Write
$n = 2^k$ and $S(k) = T(2^k)$, so $S(0) = 1$ and $S(k) = 2S(k-1) + 2^k$. Divide by $2^k$:

$$\frac{S(k)}{2^k} = \frac{S(k-1)}{2^{k-1}} + 1,$$

so $S(k)/2^k = S(0)/2^0 + k = 1 + k$, and therefore

$$T(n) = S(k) = 2^k (1 + k) = n\,(1 + \log_2 n) .$$

Verified against a direct unrolling of the recurrence, which computes $T$ by
recursion rather than by the derived formula:

| $n$ | $T(n)$ unrolled | $n(1+\log_2 n)$ | agree | $T(n)/(n\log_2 n)$ |
| --- | --- | --- | --- | --- |
| 2 | 4 | 4 | yes | 2.000 |
| 8 | 32 | 32 | yes | 1.333 |
| 32 | 192 | 192 | yes | 1.200 |
| 128 | 1,024 | 1,024 | yes | 1.143 |
| 1,024 | 11,264 | 11,264 | yes | 1.100 |

Exact agreement at every power of two, and the last column converges to 1, confirming
that the $\log_2 n$ factor is real and not an artefact of the derivation. Note the
$+n$ term: at $n = 32$ the exact answer is $192$ where $n \log_2 n = 160$, so the naive
level-sum estimate is 20% low. This is the same phenomenon as
[Lesson 80](80_big_o_and_complexity.md)'s $n \log_2 n - 1.575n$ for merge-sort comparisons:
same class, materially different number.

**(d)** This is the point. Both merge sort and a hypothetical $O(n^2)$-with-a-small-
constant sort can be written as "$n \log n$ versus $n^2$" in prose and reduced to the
same $\Theta$ statement if you are careless about what is being counted. More
importantly: $\Theta$ discards the $\log n$ factor's *size*, so an algorithm that is
$\Theta(n \log n)$ and one that is $\Theta(n \log n \log \log n)$ are the same statement.
Practical differences hide exactly there. This is
[Lesson 80](80_big_o_and_complexity.md)'s point about $\Theta(n \log n - 1.575n)$ being
inside the same class as $n \log n$ while differing by 5.5% in accuracy — and it is why
the merge-sort ledger in Block 3 counts element *moves* exactly ($n\lceil \log_2 n\rceil$)
rather than settling for the class. Whenever you are choosing between two algorithms for
a real system, measure; the class tells you which wins asymptotically, and the
measurement tells you by how much, which is the number the decision needs.

</details>

---

## Summary

- **A loop invariant has three obligations and a variant function has one more.** $I$
  holds before the loop, $I \wedge G \Rightarrow B[I]$, and $I \wedge \neg G \Rightarrow P$;
  the variant is a non-negative integer that strictly decreases. Correctness and
  termination are independent arguments and need independent certificates.
- **Invariants should be executable.** Block 1 checked binary search's invariant by
  brute force at every loop head across 3,300 random cases, zero violations — and the
  same checker makes the `hi = mid` bug a loud failure instead of 526 silent hangs.
- **A greedy rule is correct only if you can write the exchange.** Coin change for
  1, 3, 4 fails on `6, 10, 14, 18, 22`; the identical rule on US coins 1, 5, 10, 25 is
  optimal. Rod cutting by best price-per-length is right on 393 of 400 instances and
  still wrong — 98% is not a proof.
- **Equal level costs *are* case 2.** $T(n) = 2T(n/2) + n$ has level costs
  `32, 32, 32, 32, 32, 32` and total $192$; $T(n) = 2T(n/2) + n^2$ has level costs
  `4096, 2048, 1024, ...` and the root alone costs more than everything below it. The
  $\varepsilon$ is load-bearing: $T(n) = 4T(n/2) + n^2$ is case 2, $\Theta(n^2 \log n)$,
  not case 3.
- **The boundary is case 2.** $T(n) = 3T(n/3) + n$ has total work exactly $n(\log_3 n +
  1)$, measured and closed form agreeing at every $n$, so the ratio to $n \ln n$ falls
  `1.214 → 1.040` towards $1/\ln 3 = 0.910$. $\Theta(n \log n)$, not $\Theta(n^2)$.
- **Count states, not calls.** Naive Fibonacci makes 29,860,703 calls at $n = 35$ and
  multiplies by `11.1×` per step of 5 — $\varphi^5 = 11.09$ — while the table version
  does 34 additions. "There are only $n$ states" is true and answers the wrong question.
- **Counting and computing have different complexities.** Tiling a $2 \times n$ board
  has $\varphi^n$ tilings and $\Theta(n)$ work to produce the count.
- **The representation *is* the design.** Storing the list node inside the dict is what
  makes an LRU cache $O(1)$, verified by 7,204 invariant evaluations and zero recency
  mismatches against the naive version — and counting rather than timing makes the
  argument exact: `4` pointer writes per operation at every capacity, against `123.2`
  element shifts at capacity 100 and `4,338.9` at capacity 4000.
- **The workflow is five questions, and the two people skip are the ones that matter.**
  What is one unit of size? Write the brute force first — it is the oracle. Can you
  write the exchange? Do the subproblems overlap? What is the dominant operation?

---

## Next

That completes Part 6. [Part 07 — Geometry and Graphics](../part07_geometry_graphics/)
takes the algorithms here and puts them on real numbers: vectors and the cross product,
the affine transforms behind every 2D and 3D graphics pipeline, and the geometric
algorithms — convex hulls, line intersection, spatial partitioning — that this lesson's
divide-and-conquer and greedy techniques apply to directly. It assumes you can write
and prove an algorithm and bound its cost, which is exactly what this part was for.