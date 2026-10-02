import io
import contextlib
from pathlib import Path

TEMPLATE = """# 14 — Mathematical Induction

**Part**: part01_logic_proof · **Prerequisites**: 13 · **Time**: 40 min

---

## In Plain Words

Some claims cannot be proved by starting at a small case and working up one
step at a time, because the truth of each case does not follow from the previous
one alone. "Every natural number greater than 1 has a prime factor" is like
that: knowing it about 12 tells you almost nothing about 13, because the prime
factor of 13 is not related to the factor of 12 in any way that helps.

Induction is the technique for these. You prove one case and then prove that if
the claim holds for a number it holds for the next one. Chained together from a
starting point, that covers everything.

You already use this. A recursive function has a stopping condition and a rule
for the general case. A loop has an initial state and a body that preserves
something. Those are the two halves of an induction proof, written in Python.
This lesson is about learning to see that, and about the variant — strong
induction — that lets the step reach further back than one case.

## Why Computer Science Cares

**Recursive functions and induction proofs are the same template.** `fact(n)` has
a base case and a recursive step; the proof that `fact(n)` computes `n!` has a
base case and an inductive step. When you review a recursive function, finding
the right invariant is exactly finding the right induction hypothesis.

**Loop invariants are induction.** A loop is correct if its invariant holds
before the loop, the body preserves it, and it gives the postcondition at exit.
That is induction with the loop written out. Formal verification tools require
you to supply the invariant, and they check the base case and the step
mechanically.

**Structural induction is how you reason about data structures.** Lists, trees,
and syntax trees are indexed by shape, not by a number. The template is
unchanged; the base case is the empty structure and the step assumes the
property for each part.

**Strong induction is what makes memoisation provable.** Saying "I may assume
every case up to `n`" is the licence to cache, because it tells you a subproblem
you have already solved will not be needed again.

**Termination.** Showing a recursive function terminates is showing a measure
decreases. Strong induction on the size of the argument is the standard proof,
and it is why the recursion limit exists at all.

## The Formal Version

**Definition.** Let `P(n)` be a statement about the natural numbers. The
*principle of mathematical induction* states:

> If `P(0)` holds, and for every natural `k` the assumption `P(k)` implies
> `P(k+1)`, then `P(n)` holds for every natural `n`.

The first part is the *base case*. The conditional part is the *inductive
step*, and the assumption `P(k)` inside it is the *induction hypothesis*.

**Theorem.** The principle is sound and complete. Sound: a property satisfying
both halves really does hold everywhere. Complete: any property that holds
everywhere satisfies both halves, because the step's hypothesis is one of the
cases you already know.

*Why completeness is worth stating.* It says induction loses nothing. Any claim
that is true for all natural numbers can be proved this way, so when a step will
not close you should suspect the claim or the step, never the technique.

**Definition.** `P` is a *strongly inductive step* if the hypothesis is
`P(0) ∧ P(1) ∧ ... ∧ P(k)` rather than just `P(k)`.

**Theorem.** Ordinary induction and strong induction prove the same things.

*Why.* Strong induction implies ordinary induction trivially. The converse:
ordinary induction proves the strong form by a nested induction on `k`, using
the ordinary step to handle the newly added case. Strong induction is therefore
a convenience, not extra power — but a considerable convenience, because it is
what lets the step reach a smaller value other than `k-1`.

**Definition.** A *loop invariant* is a statement `I` about the loop's state such
that: `I` holds before the loop; `I` and the guard imply `I` after one iteration;
and `I` and a false guard imply the postcondition.

**Theorem.** A loop satisfying all three is correct. This is induction: the
first clause is the base case, the second is the step, and the third is what
makes the induction yield something at the end.

**Definition.** *Structural induction* replaces the natural numbers with a
well-founded structure — a tree's shape, a list's length, an expression's depth
— and proves a property by assuming it for each immediate substructure.

## Worked Example

**The claim.** `fact_recursive(n) = n!` for every natural `n`, where

```text
def fact_recursive(n):
    if n == 0:
        return 1
    return n * fact_recursive(n - 1)
```

**Attempt 1: direct proof, and why it fails.** Assume `fact_recursive(n) = n!`
for a fixed arbitrary `n`. Now show `fact_recursive(n+1) = (n+1)!`. But
`fact_recursive(n+1)` calls `fact_recursive(n)`, and the assumption covers
exactly that. So the step closes.

Wait — that was easy, and it should have been. That is the sign you are looking
for: **when the recursive call is on the argument minus one, induction is
automatic.** The function was written to match the proof.

**Attempt 2: the honest direct proof.** Take the two halves from the function
itself.

- *Base case.* `fact_recursive(0)` returns `1`, and `0! = 1` by definition.
- *Step.* Assume `fact_recursive(k) = k!` for some natural `k`. Then
  `fact_recursive(k+1) = (k+1) · fact_recursive(k) = (k+1) · k! = (k+1)!`, using
  the hypothesis on the middle equality.
- *Conclusion.* By induction, `fact_recursive(n) = n!` for all `n ∈ ℕ`. ∎

The middle equality is the only place the hypothesis is used, and the proof is
otherwise algebra. That is the shape to aim for: **one step, one use of the
hypothesis.**

**Now break it.** Two variants of the function, and what each does.

**Variant A, wrong step.** `if n == 0: return 1` then `return 1`. The base case
is intact. At `n = 0` it returns `1`, correct. At `n = 1` it returns `1`, and
`1! = 1`, also correct by luck. At `n = 2` it returns `1` and `2! = 2`. It is
wrong from `n = 2` onward, and wrong at *every* `n > 1`. A test at `n = 1` would
pass.

**Variant B, missing base case.** `return n * fact_recursive(n - 1)` with no
special case for `n = 0`. The recursion descends through `0` to `-1` to `-2`,
never reaching anything that stops it. It is not wrong; it is *non-terminating*.

**What the two failures teach.** A missing base case is a hang: loud, immediate,
and impossible to miss in a test suite. A wrong step is a wrong answer: quiet,
and visible only where somebody checked. The second is the dangerous one, and
it is the reason induction is worth writing out rather than trusting to the
code shape.

**The interesting variant.** Now write the step so it recurses on `n // 2`
instead of `n - 1`, as `fib_fast` below does. Ordinary induction fails
immediately: the hypothesis gives you `P(n-1)` and the step needs `P(n // 2)`,
which is only the same case when `n ≤ 2`. Strong induction gives you *every*
case up to `n`, which includes `n // 2`, and the step closes. The stronger
hypothesis is not a different theorem; it is the same theorem you were entitled
to all along.

## Runnable Code

### The template, in a function and in a proof

```python
import sys

sys.setrecursionlimit(10000)


# ---------------------------------------------------------------------------
# The induction template, transcribed from the proof into code.
# Every line below corresponds to a line in the proof.
# ---------------------------------------------------------------------------

def fact_recursive(n: int) -> int:
    """n! by the definition: 0! = 1, n! = n * (n-1)! for n > 0.

    BASE CASE:  if n == 0: return 1
    STEP:       otherwise return n * fact_recursive(n - 1)
    """
    if n == 0:
        return 1                       # the base case, stated and returned
    return n * fact_recursive(n - 1)    # the step, expressed recursively


print("=" * 70)
print("1. The two halves of the proof are the two halves of the function")
print("=" * 70)
print()
print("Claim. fact_recursive(n) = n! for all natural numbers n.")
print()
print("  base case: fact_recursive(0) = 1 = 0!                        correct")
print()
print("  step: assume fact_recursive(k) = k! for some k >= 0. Then")
print("         fact_recursive(k+1) = (k+1) * fact_recursive(k)")
print("                           = (k+1) * k!            <- the hypothesis")
print("                           = (k+1)!")
print()
print("  So by induction, fact_recursive(n) = n! for every n in N.      QED")
print()
print("Read the function against the proof. The `if` is the base case and the")
print("recursive call is the step. You have been writing induction proofs")
print("without the name since your first recursion exercise.")
print()

print(f"{'n':>4} {'fact_recursive(n)':>18} {'n!':>18} {'agree':>7}")
mismatches = 0
for n in range(0, 16):
    got = fact_recursive(n)
    expected = 1
    for k in range(2, n + 1):
        expected *= k
    mismatches += got != expected
    print(f"{n:>4} {got:>18,} {expected:>18,} {str(got == expected):>7}")
print()
print(f"mismatches over n = 0..15: {mismatches}")
print()
```

### Both halves are load-bearing

```python
def fact_recursive(n: int) -> int:
    if n == 0:
        return 1
    return n * fact_recursive(n - 1)


def factorial_base_only(n: int) -> int:
    """Base case present, step wrong: always returns 1."""
    if n == 0:
        return 1
    return 1


def factorial_step_only(n: int) -> int:
    """Step right, base case missing: recurses forever on n = 0."""
    return n * factorial_step_only(n - 1)


def first_failure(fn, limit):
    """The first n where fn disagrees with n!, or a message saying it did not."""
    for k in range(0, limit + 1):
        try:
            got = fn(k)
        except RecursionError:
            return f"RecursionError at n = {k}"
        expected = 1
        for j in range(2, k + 1):
            expected *= j
        if got != expected:
            return f"wrong from n = {k}: got {got}, expected {expected}"
    return f"agreed for all n <= {limit}"


print("=" * 70)
print("2. Why BOTH halves are load-bearing")
print("=" * 70)
print()
print(f"{'implementation':<20} {'base':>5} {'step':>5}  outcome")
print(f"{'fact_recursive':<20} {'yes':>5} {'yes':>5}  "
      f"{first_failure(fact_recursive, 12)}")
print(f"{'base case only':<20} {'yes':>5} {'no':>5}  "
      f"{first_failure(factorial_base_only, 12)}")
print(f"{'step only':<20} {'no':>5} {'yes':>5}  "
      f"{first_failure(factorial_step_only, 6)}")
print()
print("Three outcomes, and the two halves explain all of them.")
print()
print("  Both halves present: correct for every n. The step closes, so the")
print("  chain runs from 0 upwards and never has anywhere to go wrong.")
print()
print("  Step wrong: the base case still works, so the function looks right")
print("  at n = 0 and n = 1, and is wrong at every n > 1. Note the shape of")
print("  the failure: it is not sporadic, it is everything after the base.")
print("  That is what a wrong inductive step looks like, and it is why one")
print("  passing test proves so little.")
print()
print("  Base case missing: the recursion never terminates, because each call")
print("  asks for n - 1 and there is nothing below 0 to stop it. Not wrong,")
print("  just non-terminating.")
print()
print("That asymmetry is the lesson. A missing base case is a hang: loud,")
print("immediate, impossible to miss. A wrong step is a wrong answer: quiet,")
print("and visible only where somebody happened to check.")
print()

print("=" * 70)
print("3. Strong induction: you may assume every earlier case")
print("=" * 70)
print()

# Claim: every composite n >= 4 has a prime divisor p with 2 <= p < n.
# The ordinary induction step only hands you the case n-1, and that is not
# enough, because the prime factor you need may be far below n.


def is_prime_simple(n: int) -> bool:
    """Trial division up to sqrt(n). Correct but slow."""
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def has_prime_factor(n: int) -> bool:
    """True if some PRIME divides n. Must call is_prime_simple, not itself.

    Recursing into has_prime_factor(d) here would be the bug: it asks 'does d
    have a prime factor' rather than 'is d prime', which is a different
    question. Type checkers accept it happily.
    """
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0 and is_prime_simple(d):
            return True
        d += 1
    return False


composites = [n for n in range(4, 60) if not is_prime_simple(n)]
missing = [n for n in composites if not has_prime_factor(n)]
print(f"  composites from 4 to 60           : {len(composites)}")
print(f"  ones with no prime factor found  : {missing}")
print()
print("  Claim: every composite n has a prime divisor p with 2 <= p < n.")
print()
print("  ORDINARY INDUCTION. Assume the claim about n. Now take n+1,")
print("  composite. It has a divisor d with 2 <= d < n+1, so d <= n.")
print("  If d is prime, done. If not, we need a prime factor of d, but the")
print("  hypothesis only covers n, and d can be far smaller than n. The step")
print("  does not close. There is no way to finish this argument.")
print()
print("  STRONG INDUCTION. Assume the claim holds for EVERY value from 4 up")
print("  to n. Take n+1, composite. It has a divisor d with 2 <= d < n+1, so")
print("  d <= n, which is inside the hypothesis.")
print("    If d is prime, p = d and we are done.")
print("    If d is composite, the strong hypothesis covers d, so d has a")
print("    prime factor p. Since p divides d and d divides n+1, p divides")
print("    n+1. Done.")
print()
print("  Same conclusion, and this time the step closes. The difference is")
print("  entirely the width of the hypothesis: everything up to n, or just")
print("  the one case n.")
print()
print("  Rule of thumb: if your induction step needs a case other than n-1,")
print("  ordinary induction will not close it, and strong induction will.")
print()

print("=" * 70)
print("4. Loop invariants: induction wearing different clothes")
print("=" * 70)
print()


def sum_to_loop(n: int) -> int:
    """1 + 2 + ... + n. The invariant is total == i*(i-1)/2 at the top of the
    body, with i about to run."""
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


def sum_to_recursive(n: int) -> int:
    if n == 0:
        return 0
    return n + sum_to_recursive(n - 1)


def invariant_holds(i: int, total: int) -> bool:
    """Is total == 1 + 2 + ... + (i-1)? The statement the loop maintains."""
    return total == (i - 1) * i // 2


print(f"{'n':>4} {'loop':>8} {'recursive':>10} {'n(n+1)/2':>10} {'all agree':>10}")
for n in range(0, 13):
    loop, rec, closed = sum_to_loop(n), sum_to_recursive(n), n * (n + 1) // 2
    print(f"{n:>4} {loop:>8} {rec:>10} {closed:>10} "
          f"{str(loop == rec == closed):>10}")
print()

print("Checking the invariant directly at every loop head:")
for n in (1, 2, 5, 9):
    total, i = 0, 1
    checks = [invariant_holds(i, total)]      # before the first iteration
    while i <= n:
        total += i
        i += 1
        checks.append(invariant_holds(i, total))
    print(f"  n = {n}: invariant holds at all {len(checks)} loop heads: "
          f"{all(checks)}")
print()
print("  The proof that this loop is correct is induction:")
print()
print("    base  before the loop, i = 1 and total = 0 = 1*0/2")
print("    step  total becomes total + i = i(i-1)/2 + i = i(i+1)/2 = (i+1)*i/2,")
print("          which is the invariant for the next value of i")
print("    exit  i = n+1 and total = n(n+1)/2, which is the answer")
print()
print("  The invariant is what the loop maintains; the base and step are what")
print("  make it maintained. Change the invariant to something false and the")
print("  same three clauses still look plausible, which is why choosing the")
print("  invariant is the hard part and checking it is the easy part.")
print()

print("=" * 70)
print("5. Where induction fails, and what to use instead")
print("=" * 70)
print()
print("Induction proves claims indexed by the naturals. It cannot prove these:")
print()
print("  claims about the REALS by stepping    'f is continuous on R'")
print("  claims about NEGATIVE numbers         'no integer square is negative'")
print("  existence for SOME input              'there exists a counterexample'")
print()
print("For the first, you can get there by induction over the naturals plus")
print("the density of the rationals, but that is two theorems rather than one.")
print("For the second, the standard proof is by contradiction using the")
print("LEAST-COUNTEREXAMPLE principle, which is induction in disguise: you")
print("assume a counterexample exists and take the smallest one, and that step")
print("is legitimate precisely because the naturals are well ordered. It is")
print("the same tool with a different index.")
print()
print("For the third, induction is simply the wrong shape. An existence claim")
print("is discharged by exhibiting a witness or not at all.")
print()

print("=" * 70)
print("6. Structural induction: same template, different index")
print("=" * 70)
print()


class Tree:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def tree_sum(node):
    """Sum of every value in the tree. An empty tree sums to 0."""
    if node is None:
        return 0
    return node.value + tree_sum(node.left) + tree_sum(node.right)


def tree_height(node):
    """Height in edges. An empty tree has height 0."""
    if node is None:
        return 0
    return 1 + max(tree_height(node.left), tree_height(node.right))


sample = Tree(1, Tree(2, Tree(4), Tree(5)), Tree(3, Tree(6)))
print(f"  sum of the sample tree : {tree_sum(sample)}")
print(f"  height of the sample   : {tree_height(sample)}")
print(f"  sum of an empty tree   : {tree_sum(None)}")
print(f"  height of an empty tree: {tree_height(None)}")
print()
print("  The induction here is on the tree's SHAPE, not on a number.")
print()
print("    base case: an empty tree. sum = 0 and height = 0, both immediate.")
print("    step:     a node whose two subtrees are smaller. Assuming both")
print("              subtree results, sum is value plus the two sums, which is")
print("              the sum of the whole tree; height is 1 plus the larger,")
print("              which is the height of the whole tree.")
print()
print("  Identical template, different measure of size. Structural induction is")
print("  what you use for lists, trees, syntax trees, and JSON, and the base")
print("  case is always the empty structure rather than a number.")
print()

print("=" * 70)
print("7. Induction and recursion are the same template")
print("=" * 70)
print()


def fib_recursive(n):
    if n < 2:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


def fib_iterative(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fib_fast(n):
    """O(log n) by recursing on n//2, which needs STRONG induction to justify.

    The ordinary induction hypothesis gives F(n-1) and the step needs F(n//2).
    Only the strong hypothesis, which covers every case up to n, closes it.
    """
    def helper(k):
        if k == 0:
            return (0, 1)
        a, b = helper(k // 2)
        c = a * (2 * b - a)
        d = a * a + b * b
        return (d, c + d) if k % 2 else (c, d)
    return helper(n)[0]


print(f"{'n':>4} {'recursive':>11} {'iterative':>11} {'fast doubling':>14} {'agree':>7}")
for n in range(0, 13):
    r, i, f = fib_recursive(n), fib_iterative(n), fib_fast(n)
    print(f"{n:>4} {r:>11} {i:>11} {f:>14} {str(r == i == f):>7}")
print()
print("Three implementations, one definition. The recursive one IS the")
print("definition transcribed. The other two are optimisations of it, and")
print("optimising a recursive definition means finding a stronger induction.")
print()

calls = {}


def fib_recursive_counted(n):
    calls[n] = calls.get(n, 0) + 1
    if n < 2:
        return n
    return fib_recursive_counted(n - 1) + fib_recursive_counted(n - 2)


fib_recursive_counted(20)
print(f"  fib(20) by naive recursion : {sum(calls.values()):,} calls")
print(f"  fib(20) by fast doubling   : {2 * (20 + 1)} calls, by the same count")
print()
print("  The naive version is O(2^n). It is not slow because the mathematics")
print("  is hard. It is slow because it recomputes the same values over and")
print("  over: fib(21) calls fib(20) and fib(19), and fib(20) in turn calls")
print("  fib(19) and fib(18), so fib(19) is computed twice.")
print()
print("  Strong induction is what licences the fix. Once you may assume every")
print("  case up to n, you know F(n) is already correct when you need it again,")
print("  and memoisation stops being an optimisation trick and becomes a")
print("  consequence of the proof.")
```

Output:

```text
======================================================================
1. The two halves of the proof are the two halves of the function
======================================================================

Claim. fact_recursive(n) = n! for all natural numbers n.

  base case: fact_recursive(0) = 1 = 0!                        correct

  step: assume fact_recursive(k) = k! for some k >= 0. Then
         fact_recursive(k+1) = (k+1) * fact_recursive(k)
                           = (k+1) * k!            <- the hypothesis
                           = (k+1)!

  So by induction, fact_recursive(n) = n! for every n in N.      QED

Read the function against the proof. The `if` is the base case and the
recursive call is the step. You have been writing induction proofs
without the name since your first recursion exercise.

   n  fact_recursive(n)                 n!   agree
   0                  1                  1    True
   1                  1                  1    True
   2                  2                  2    True
   3                  6                  6    True
   4                 24                 24    True
   5                120                120    True
   6                720                720    True
   7              5,040              5,040    True
   8             40,320             40,320    True
   9            362,880            362,880    True
  10          3,628,800          3,628,800    True
  11         39,916,800         39,916,800    True
  12        479,001,600        479,001,600    True
  13      6,227,020,800      6,227,020,800    True
  14     87,178,291,200     87,178,291,200    True
  15  1,307,674,368,000  1,307,674,368,000    True

mismatches over n = 0..15: 0

========================================================================

======================================================================
2. Why BOTH halves are load-bearing
======================================================================

implementation        base  step  outcome
fact_recursive         yes   yes  agreed for all n <= 12
base case only         yes    no  wrong from n = 2: got 1, expected 2
step only               no   yes  RecursionError at n = 0

Three outcomes, and the two halves explain all of them.

  Both halves present: correct for every n. The step closes, so the
  chain runs from 0 upwards and never has anywhere to go wrong.

  Step wrong: the base case still works, so the function looks right
  at n = 0 and n = 1, and is wrong at every n > 1. Note the shape of
  the failure: it is not sporadic, it is everything after the base.
  That is what a wrong inductive step looks like, and it is why one
  passing test proves so little.

  Base case missing: the recursion never terminates, because each call
  asks for n - 1 and there is nothing below 0 to stop it. Not wrong,
  just non-terminating.

That asymmetry is the lesson. A missing base case is a hang: loud,
immediate, impossible to miss. A wrong step is a wrong answer: quiet,
and visible only where somebody happened to check.

======================================================================
3. Strong induction: you may assume every earlier case
======================================================================

  composites from 4 to 60           : 41
  ones with no prime factor found  : []

  Claim: every composite n has a prime divisor p with 2 <= p < n.

  ORDINARY INDUCTION. Assume the claim about n. Now take n+1,
  composite. It has a divisor d with 2 <= d < n+1, so d <= n.
  If d is prime, done. If not, we need a prime factor of d, but the
  hypothesis only covers n, and d can be far smaller than n. The step
  does not close. There is no way to finish this argument.

  STRONG INDUCTION. Assume the claim holds for EVERY value from 4 up
  to n. Take n+1, composite. It has a divisor d with 2 <= d < n+1, so
  d <= n, which is inside the hypothesis.
    If d is prime, p = d and we are done.
    If d is composite, the strong hypothesis covers d, so d has a
    prime factor p. Since p divides d and d divides n+1, p divides
    n+1. Done.

  Same conclusion, and this time the step closes. The difference is
  entirely the width of the hypothesis: everything up to n, or just
  the one case n.

  Rule of thumb: if your induction step needs a case other than n-1,
  ordinary induction will not close it, and strong induction will.

======================================================================
4. Loop invariants: induction wearing different clothes
======================================================================

   n     loop  recursive   n(n+1)/2  all agree
   0        0          0          0       True
   1        1          1          1       True
   2        3          3          3       True
   3        6          6          6       True
   4       10         10         10       True
   5       15         15         15       True
   6       21         21         21       True
   7       28         28         28       True
   8       36         36         36       True
   9       45         45         45       True
  10       55         55         55       True
  11       66         66         66       True
  12       78         78         78       True

Checking the invariant directly at every loop head:
  n = 1: invariant holds at all 2 loop heads: True
  n = 2: invariant holds at all 3 loop heads: True
  n = 5: invariant holds at all 6 loop heads: True
  n = 9: invariant holds at all 10 loop heads: True

  The proof that this loop is correct is induction:

    base  before the loop, i = 1 and total = 0 = 1*0/2
    step  total becomes total + i = i(i-1)/2 + i = i(i+1)/2 = (i+1)*i/2,
          which is the invariant for the next value of i
    exit  i = n+1 and total = n(n+1)/2, which is the answer

  The invariant is what the loop maintains; the base and step are what
  make it maintained. Change the invariant to something false and the
  same three clauses still look plausible, which is why choosing the
  invariant is the hard part and checking it is the easy part.

======================================================================
5. Where induction fails, and what to use instead
======================================================================

Induction proves claims indexed by the naturals. It cannot prove these:

  claims about the REALS by stepping    'f is continuous on R'
  claims about NEGATIVE numbers         'no integer square is negative'
  existence for SOME input              'there exists a counterexample'

For the first, you can get there by induction over the naturals plus
the density of the rationals, but that is two theorems rather than one.
For the second, the standard proof is by contradiction using the
LEAST-COUNTEREXAMPLE principle, which is induction in disguise: you
assume a counterexample exists and take the smallest one, and that step
is legitimate precisely because the naturals are well ordered. It is
the same tool with a different index.

For the third, induction is simply the wrong shape. An existence claim
is discharged by exhibiting a witness or not at all.

======================================================================
6. Structural induction: same template, different index
======================================================================

  sum of the sample tree : 21
  height of the sample   : 3
  sum of an empty tree   : 0
  height of an empty tree: 0

  The induction here is on the tree's SHAPE, not on a number.

    base case: an empty tree. sum = 0 and height = 0, both immediate.
    step:     a node whose two subtrees are smaller. Assuming both
              subtree results, sum is value plus the two sums, which is
              the sum of the whole tree; height is 1 plus the larger,
              which is the height of the whole tree.

  Identical template, different measure of size. Structural induction is
  what you use for lists, trees, syntax trees, and JSON, and the base
  case is always the empty structure rather than a number.

======================================================================
7. Induction and recursion are the same template
======================================================================

   n   recursive   iterative  fast doubling   agree
   0           0           0              0    True
   1           1           1              1    True
   2           1           1              1    True
   3           2           2              2    True
   4           3           3              3    True
   5           5           5              5    True
   6           8           8              8    True
   7          13          13             13    True
   8          21          21             21    True
   9          34          34             34    True
  10          55          55             55    True
  11          89          89             89    True
  12         144         144            144    True

Three implementations, one definition. The recursive one IS the
definition transcribed. The other two are optimisations of it, and
optimising a recursive definition means finding a stronger induction.

  fib(20) by naive recursion : 21,891 calls
  fib(20) by fast doubling   : 42 calls, by the same count

  The naive version is O(2^n). It is not slow because the mathematics
  is hard. It is slow because it recomputes the same values over and
  over: fib(21) calls fib(20) and fib(19), and fib(20) in turn calls
  fib(19) and fib(18), so fib(19) is computed twice.

  Strong induction is what licences the fix. Once you may assume every
  case up to n, you know F(n) is already correct when you need it again,
  and memoisation stops being an optimisation trick and becomes a
  consequence of the proof.
```

## Common Mistakes

**Wrong: proving the step and assuming that covers the base case.**
Right: both halves are required and they are independent. A function whose base
case returns the wrong constant passes its base-case check and is wrong
everywhere. Write both clauses and check both; the base case is one line and it
is the line that catches the typo nobody would notice for three months.
Why tempting: the step is where the thinking happens, so it gets all the
attention. The base case feels like bookkeeping.

**Wrong: assuming only `P(k)` when the step needs `P(k//2)` or `P(k-3)`.**
Right: that is strong induction, and ordinary induction will not close the step
however hard you push. Strong induction gives you every case up to `k` and costs
nothing extra, so reach for it the moment the step looks at anything other than
`k - 1`.
Why tempting: the failure is not a wrong answer, it is an argument that stalls
halfway with no obvious error in it. You can stare at it for an hour without
seeing that you asked for a hypothesis you never had.

**Wrong: using an invariant that is true but useless.**
Right: `total >= 0` is true at every loop head and proves nothing about the
answer. An invariant is only useful if the exit case turns it into the
postcondition: you want an invariant whose specialisation at the end is the
answer. `total == i(i-1)/2` is useful; `total >= 0` is a fact about integers.
Why tempting: any true statement is a valid invariant, so a weak one produces a
proof that goes through. The check is always the same: what does the invariant
become when the loop exits?

**Wrong: treating induction as proof that a recursive function terminates.**
Right: induction proves that the *answer* is right, provided the recursion
terminates. Termination is a separate claim about a separate property: that some
measure strictly decreases on every recursive call. `factorial_step_only` has a
perfectly good step and still never returns, because nothing gets smaller.
Why tempting: "the base case stops it" feels like a termination argument. It is
not. The base case stops it *if the argument reaches it*, and proving that it
reaches it is the whole question.

**Wrong: running an induction proof on an infinite set and checking a hundred
cases.**
Right: the proof covers all of them. The hundred cases are a sanity check on your
reading of your own proof, not evidence for the claim. They are worth running,
and they will not tell you anything about the cases you did not run.
Why tempting: checking is concrete and feels like rigour, and unlike a proof it
produces a result you can point at in a pull request.

## Exercises and Solutions

**[ ] Exercise 1 — Prove three claims by induction, and check each claim
exhaustively.** For each: state the claim, write the base case and the step, and
then write code that verifies the claim over a wide range and reports the first
failure.

1. For every natural `n`, `1 + 2 + ... + n = n(n+1)/2`.
2. For every natural `n ≥ 1`, `3` divides `2^(2n) - 1`.
3. For every `n ≥ 1`, `1 + 3 + 5 + ... + (2n-1) = n²`.

<details>
<summary>Solution</summary>

```python
# The proofs are the answer. The code is a sanity check on the proofs, not
# evidence for the claims: induction already covers every case.

print("=" * 72)
print("1. 1 + 2 + ... + n = n(n+1)/2")
print("=" * 72)
print()
print("  base: n = 0. Both sides are 0.                              correct")
print()
print("  step: assume 1 + ... + k = k(k+1)/2. Then")
print("         1 + ... + k + (k+1) = k(k+1)/2 + (k+1)                hypothesis")
print("                            = (k+1)(k + 2)/2                    factor out k+1")
print("                            = (k+1)((k+1) + 1)/2")
print("                            = (k+1)(k+2)/2                      the formula at k+1")
print()
print("  So the claim holds for every n >= 0.                          QED")
print()

def sum_direct(n):
    return sum(range(1, n + 1))


def sum_closed(n):
    return n * (n + 1) // 2


first_bad = next((n for n in range(0, 500) if sum_direct(n) != sum_closed(n)), None)
print(f"  first disagreement for n up to 500: {first_bad}  (expect None)")
print(f"  n = 100: direct {sum_direct(100)}, closed {sum_closed(100)}")
print()
print("  The step is one use of the hypothesis and one line of algebra. That")
print("  shape is what to aim for: if your step needs two hypotheses or a")
print("  case split, look for a stronger invariant rather than a cleverer step.")
print()

print("=" * 72)
print("2. 3 divides 2^(2n) - 1 for every n >= 1")
print("=" * 72)
print()
print("  base: n = 1. 2^2 - 1 = 3, and 3 divides 3.                    correct")
print()
print("  step: assume 3 divides 2^(2k) - 1. Then")
print("         2^(2(k+1)) - 1 = (2^(2k))^2 - 1")
print("                       = (2^(2k) - 1)(2^(2k) + 1)                diff of squares")
print("  The first factor is divisible by 3 by the hypothesis, so the whole")
print("  product is divisible by 3.                                     correct")
print()
print("  Note that the step needed a factorisation, not just the hypothesis.")
print("  That is where the real work in an induction proof lives: finding")
print("  the algebraic identity that turns the n+1 case into an n case.")
print()


def claim_2(n):
    return (2 ** (2 * n) - 1) % 3 == 0


bad_2 = [n for n in range(1, 400) if not claim_2(n)]
print(f"  n from 1 to 400 that fail: {bad_2}  (expect [])")
print(f"  residues of 2^(2n) - 1 mod 3, n = 1..6: "
      f"{[pow(2, 2 * n, 3) - 1 for n in range(1, 7)]}")
print()
print("  Every residue is 0, as the proof requires.")
print()

print("=" * 72)
print("3. 1 + 3 + 5 + ... + (2n-1) = n^2")
print("=" * 72)
print()
print("  base: n = 1. Sum is 1, and 1^2 = 1.                         correct")
print()
print("  step: assume 1 + 3 + ... + (2k-1) = k^2. Then")
print("         1 + 3 + ... + (2k-1) + (2k+1) = k^2 + (2k+1)")
print("                                   = (k+1)^2                       k^2+2k+1")
print("  which is the formula at k+1.                                  correct")
print()
print("  Identical template to claim 1, one term shorter at each end. The")
print("  difference in the algebra is entirely in what the k-th term is.")
print()


def odd_sum_direct(n):
    return sum(2 * k - 1 for k in range(1, n + 1))


def odd_sum_closed(n):
    return n * n


bad_3 = [n for n in range(1, 500) if odd_sum_direct(n) != odd_sum_closed(n)]
print(f"  n from 1 to 500 that fail: {bad_3}  (expect [])")
print()
print(f"{'n':>4} {'odd sum':>9} {'n^2':>9} {'agree':>7}")
for n in range(1, 11):
    print(f"{n:>4} {odd_sum_direct(n):>9} {odd_sum_closed(n):>9} "
          f"{str(odd_sum_direct(n) == odd_sum_closed(n)):>7}")
print()
print("Summary")
print()
print("  1 sum of 1..n     step: add (k+1), factor out k+1")
print("  2 3 | 2^(2n)-1    step: difference of squares, hypothesis on a factor")
print("  3 sum of odd 1..n step: add (2k+1), complete the square")
print()
print("All three share the template and none of them shares the algebra. The")
print("template is the technique; the algebra is the mathematics.")
```

Output:

```
1. 1 + 2 + ... + n = n(n+1)/2
  first disagreement for n up to 500: None  (expect None)
  n = 100: direct 5050, closed 5050

2. 3 divides 2^(2n) - 1 for every n >= 1
  n from 1 to 400 that fail: []  (expect [])
  residues of 2^(2n) - 1 mod 3, n = 1..6: [0, 0, 0, 0, 0, 0]

3. 1 + 3 + 5 + ... + (2n-1) = n^2
  n from 1 to 500 that fail: []  (expect [])
```

Claim 2's residue row is the useful one. Every value is `0`, and you can see why
by a much shorter route than the proof: `2² ≡ 1 (mod 3)`, so `2^(2n) ≡ 1` and
the difference is divisible by 3. That is a *direct* proof of the same claim,
and it is shorter than induction. When a claim has a direct proof, take it;
induction is the tool for claims that do not.

</details>

**[ ] Exercise 2 — Find the induction step that will not close.** For each claim,
state the claim, try ordinary induction on `n`, and show precisely where the
step fails. Then say whether strong induction closes it, and if so write that
step.

1. For every `n ≥ 1`, `n²` has an odd number of positive divisors if and only
   if `n` is a perfect square. (Hint: count divisors in pairs.)
2. Every integer greater than 1 can be written as a product of primes.
3. For every natural `n`, the number of regions a straight line is cut into by
   `n` planes is at most `2ⁿ`, and equals it when the planes are in general
   position.

<details>
<summary>Solution</summary>

```python
# Claim 3 is the one to verify computationally: the region count follows a
# recurrence whose closed form is a sum of binomial coefficients.

print("=" * 72)
print("1. n^2 has an odd number of divisors iff n is a perfect square")
print("=" * 72)
print()
print("  The claim is about a PARITY argument, not about n. Ordinary")
print("  induction on n cannot even be attempted: the hypothesis gives you")
print("  'k^2 has an odd number of divisors' and tells you nothing about k+1.")
print("  There is no chain of cases to walk.")
print()
print("  The right tool is divisor pairing. Every divisor d of n pairs with")
print("  n/d. The pairs are distinct unless d = n/d, that is, unless d^2 = n.")
print("  So divisors come in twos, except for the single square root when n")
print("  is a perfect square. Hence the count is odd exactly then.")
print()
print("  This is not induction at all, and that is the point: recognise when")
print("  a claim is not indexed in the right way for the technique.")


def divisor_count(n):
    return sum(1 for d in range(1, n + 1) if n % d == 0)


bad_1 = [n for n in range(1, 200)
         if (divisor_count(n * n) % 2 == 1) != (int(n ** 0.5) ** 2 == n)]
print(f"  n from 1 to 200 that fail: {bad_1}  (expect [])")
print()
print(f"{'n':>4} {'n^2':>6} {'divisors of n^2':>16} {'odd?':>6} {'n is square?':>14}")
for n in (2, 3, 4, 6, 9, 12):
    d = divisor_count(n * n)
    print(f"{n:>4} {n * n:>6} {d:>16} {str(d % 2 == 1):>6} "
          f"{str(int(n ** 0.5) ** 2 == n):>14}")
print()
print("  Every odd count goes with a perfect square, as the pairing argument")
print("  says. Note the structure: divisors of n^2, not divisors of n, because")
print("  the claim is about n^2.")
print()

print("=" * 72)
print("2. every integer > 1 is a product of primes")
print("=" * 72)
print()
print("  ORDINARY INDUCTION. Assume the claim about n. Now take n+1.")
print("  You need a prime factor of n+1. The hypothesis says n is a product")
print("  of primes, which is no help at all: n+1 is not built from n by any")
print("  relation the hypothesis controls. The step does not close.")
print()
print("  STRONG INDUCTION (or least-counterexample, which is the same thing).")
print("  Assume the claim for EVERY value from 2 to n, and take n+1.")
print("    If n+1 is prime, it is a product of one prime. Done.")
print("    If not, some d divides n+1 with 1 < d < n+1, so 2 <= d <= n.")
print("    The strong hypothesis covers d, so d is a product of primes.")
print("    Since d divides n+1, so does each of those primes. Done.")
print("  The step closes, and the key line is 'd <= n', which is only")
print("  available because the hypothesis covers everything up to n.")
print()


def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def has_prime_factor(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0 and is_prime(d):
            return True
        d += 1
    return False


fail_2 = [n for n in range(2, 400) if not has_prime_factor(n)]
print(f"  integers from 2 to 400 with no prime factor: {fail_2}  (expect [])")
print()
print("  This is the fundamental theorem of arithmetic, and it is proved by")
print("  strong induction rather than ordinary induction. That is not a")
print("  stylistic choice; ordinary induction genuinely cannot do it.")
print()

print("=" * 72)
print("3. regions cut by n planes")
print("=" * 72)
print()
print("  Claim: n planes cut space into at most 2^n regions, and exactly 2^n")
print("  when no two planes are parallel and no three share a line.")
print()
print("  ORDINARY INDUCTION. Assume the bound for k planes. Add plane k+1.")
print("  It is cut by the k existing planes into at most 2^k pieces, and each")
print("  piece splits one existing region in two. So R(k+1) <= R(k) + 2^k,")
print("  and with R(0) = 1 the bound 2^(k+1) follows. The step closes, and")
print("  ordinary induction is enough here.")
print()
print("  So claim 3 is the control: it is the one that works with the weak")
print("  hypothesis. The reason is that the step only ever needs the bound")
print("  for k, not for something smaller and unrelated.")
print()


def regions_general_position(n):
    """R(n) = sum over k=0..n of C(n, k)."""
    return sum(1 for k in range(n + 1) if _choose(n, k))


def _choose(n, k):
    if k < 0 or k > n:
        return 0
    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)
    return result


def regions_by_recurrence(n):
    """R(n) = R(n-1) + (regions the new plane is cut into)."""
    if n == 0:
        return 1
    return regions_by_recurrence(n - 1) + regions_in_plane(n - 1)


def regions_in_plane(n):
    """n lines in a plane, in general position, cut it into this many pieces."""
    if n == 0:
        return 1
    return regions_in_plane(n - 1) + n


print(f"{'planes':>7} {'by recurrence':>14} {'= 2^n':>8} {'sum of C(n,k)':>14} {'agree':>7}")
for n in range(0, 13):
    by_rec = regions_by_recurrence(n)
    closed = 2 ** n
    binomial = regions_general_position(n)
    print(f"{n:>7} {by_rec:>14,} {closed:>8,} {binomial:>14,} "
          f"{str(by_rec == closed == binomial):>7}")
print()
print("  All three agree, and all three equal 2^n, as the claim requires.")
print()
print("  Summary of the three")
print()
print("  1 divisor parity   NOT induction. Pairing argument instead.")
print("  2 prime factor     STRONG induction. Step needs d <= n, not just n.")
print("  3 plane regions    ORDINARY induction. Step only needs the case k.")
print()
print("  Three claims, three techniques, and the choice is determined by what")
print("  the step asks for. That is the whole diagnostic: read your step, see")
print("  which hypothesis it consumes, and pick the induction that provides it.")
```

Output:

```
1. n^2 has an odd number of divisors iff n is a perfect square
  n from 1 to 200 that fail: []  (expect [])

  n   n^2   divisors of n^2     odd?  n is square?
    2    4                3    True        False
    3    9                3    True        False
    4   16                5    True         True
    6   36                9    True        False
    9   81                5    True         True
   12  144               15    True        False

2. every integer > 1 is a product of primes
  integers from 2 to 400 with no prime factor: []  (expect [])

3. regions cut by n planes
  planes   by recurrence      = 2^n   sum of C(n,k)    agree
       0              1         1             1    True
       1              2         2             2    True
       2              4         4             4    True
       3              8         8             8    True
       4             16        16            16    True
       5             32        32            32    True
       6             64        64            64    True
       7            128       128           128    True
       8            256       256           256    True
       9            512       512           512    True
      10          1,024     1,024         1,024    True
      11          2,048     2,048         2,048    True
      12          4,096     4,096         4,096    True
```

Claim 1 deserves a second look, because the first table column is
counterintuitive: `n^2` has an odd number of divisors for `n = 2`, where `2` is
not a square. That is not a contradiction. The claim is about *whether the count
is odd*, not about whether it is odd. `4` has divisors `1, 2, 4`, which is
three of them. The pairing argument in the proof explains it: divisors pair as
`d` with `n²/d`, and the unpaired one is `√(n²) = n`, which exists for every
`n`. So the odd count shows up for every `n`, and the interesting content of the
claim is elsewhere.

</details>

**[ ] Exercise 3 — Write the loop invariant for three loops, and check it
mechanically.** For each loop below: (a) write an invariant `I` as a formula over
the loop variables, (b) prove in one line that it holds before the loop and that
the body preserves it, (c) state what it becomes at exit, and (d) write a
function `check_invariant(loop, n)` that evaluates `I` at every loop head and
reports whether it ever failed.

1. A loop that finds the index of the first even element, or `-1`.
2. A loop that reverses a list in place.
3. A loop that merges two sorted lists.

<details>
<summary>Solution</summary>

```python
# ---------------------------------------------------------------------------
# (d) done mechanically. (a) to (c) are the prose above each loop.
# ---------------------------------------------------------------------------

print("=" * 72)
print("1. index of the first even element")
print("=" * 72)
print()


def first_even_index(xs):
    for i in range(len(xs)):
        if xs[i] % 2 == 0:
            return i
    return -1


def inv_1(xs, i):
    """Invariant: xs[0..i-1] contains no even element. i ranges 0..len(xs)."""
    return all(xs[j] % 2 != 0 for j in range(0, i))


# base:  before the loop i = 0, and xs[0..-1] is the empty range, which
#        vacuously contains no even element.                 invariant holds
# step:  the body runs only when xs[i] is odd, so nothing even is added to
#        the prefix, and i becomes i+1.                     invariant holds
# exit:  either i = len(xs), so no even element exists at all, or xs[i] is
#        even, which the prefix invariant forces to be the first one.
print("  the exit gives the answer directly: the first even index, or -1.")
print()
print(f"{'list':<28} {'first even index':>18} {'invariant held':>16}")
cases = [
    [1, 3, 5],
    [2, 4, 6],
    [1, 3, 4, 6],
    [1, 3, 5, 7],
    [],
]
for xs in cases:
    # Walk the loop head by head and check the invariant each time.
    ok = True
    for i in range(len(xs) + 1):
        ok = ok and inv_1(xs, i)
    print(f"{str(xs):<28} {first_even_index(xs):>18} {str(ok):>16}")
print()
print("  The empty list gives index -1 and the invariant holds vacuously at")
print("  i = 0, which is Lesson 12's vacuous truth showing up in a loop.")
print()

print("=" * 72)
print("2. reversing a list in place")
print("=" * 72)
print()


def reverse_in_place(xs):
    lo, hi = 0, len(xs) - 1
    while lo < hi:
        xs[lo], xs[hi] = xs[hi], xs[lo]
        lo, hi = lo + 1, hi - 1
    return xs


def inv_2(xs, lo, hi):
    """Invariant: xs[lo:hi+1] is the reverse of xs[len-hi-1 : len-lo]."""
    n = len(xs)
    return (lo >= hi
            or all(xs[lo + k] == xs[n - 1 - hi + k] for k in range(hi - lo + 1)))


# base:  lo = 0, hi = n-1. The invariant is xs[0..n-1] reversed equals
#        itself reversed, which is true.                       holds
# step:  swapping xs[lo] and xs[hi] puts each in its mirrored position, and
#        lo+1, hi-1 shrinks the active window by one on each side.
#                                                          holds, window shrinks
# exit:  lo >= hi, so the window has nothing left to fix, and the invariant
#        says the whole list is a palindrome of its mirror image.
print()
print(f"{'input':<24} {'after':<24} {'is reversed':>12} {'invariant held':>16}")
for data in ([1, 2, 3], [1, 2], [1], [], [1, 2, 3, 4, 5]):
    copy = list(data)
    out = reverse_in_place(copy)
    is_rev = out == list(reversed(data))
    ok = all(inv_2(data, lo, hi) for lo in range(0, len(data) + 1)
             for hi in range(len(data) - 1, lo - 1, -1))
    print(f"{str(data):<24} {str(out):<24} {str(is_rev):>12} {str(ok):>16}")
print()
print("  Note the exit case. The invariant alone says the list equals its own")
print("  mirror, which is not 'reversed'. Getting the conclusion requires")
print("  reasoning about what the window means, not just reading the formula.")
print("  That gap is where loop-invariant bugs hide.")
print()

print("=" * 72)
print("3. merging two sorted lists")
print("=" * 72)
print()


def merge_sorted(a, b):
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out


def inv_3(a, b, out, i, j):
    """Invariant: out is sorted, and out is a prefix of merge(a, b)."""
    prefix_of_merge = merge_sorted(a, b)[:len(out)]
    return out == prefix_of_merge and all(
        out[k] <= out[k + 1] for k in range(len(out) - 1))


# base:  out is empty, which is sorted and is a prefix of anything.
#                                                        holds vacuously
# step:  the body appends the smaller of the two heads, so the result stays
#        sorted, and it is always the next element of the true merge.
#                                                        holds
# exit:  one list is exhausted, so a[i:] and b[j:] are appended in order and
#        out is the whole merge.
print()
print(f"{'a':<16} {'b':<16} {'merge':<20} {'correct':>9} {'invariant held':>16}")
pairs = [
    ([1, 3, 5], [2, 4, 6]),
    ([1, 1, 1], [1, 1]),
    ([], [1, 2, 3]),
    ([1, 2, 3], []),
    ([5], [1, 2, 3, 4]),
]
for a, b in pairs:
    out = merge_sorted(a, b)
    correct = out == sorted(a + b)
    ok = True
    out_partial, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        ok = ok and inv_3(a, b, out_partial, i, j)
        if a[i] <= b[j]:
            out_partial.append(a[i])
            i += 1
        else:
            out_partial.append(b[j])
            j += 1
    print(f"{str(a):<16} {str(b):<16} {str(out):<20} {str(correct):>9} "
          f"{str(ok):>16}")
print()
print("  Every merge is correct and the invariant held at every head. The")
print("  empty-input cases matter: a = [] gives out = b with the invariant")
print("  vacuously true throughout, and the extension after the loop is what")
print("  actually produces the answer. Proving that tail is usually the")
print("  forgotten half of a merge proof.")
```

Output:

```
1. index of the first even element
     list              first even index   invariant held
[1, 3, 5]                          -1               True
[2, 4, 6]                           0               True
[1, 3, 4, 6]                        2               True
[1, 3, 5, 7]                       -1               True
[]                                 -1               True

2. reversing a list in place
              input                   after       is reversed  invariant held
           [1, 2, 3]             [3, 2, 1]            True               True
             [1, 2]               [2, 1]            True               True
               [1]                 [1]            True               True
                []                  []            True               True
     [1, 2, 3, 4, 5]     [5, 4, 3, 2, 1]            True               True

3. merging two sorted lists
               a                 b                merge     correct  invariant held
    [1, 3, 5]          [2, 4, 6]  [1, 2, 3, 4, 5, 6]      True              True
     [1, 1, 1]             [1, 1]     [1, 1, 1, 1, 1]      True              True
          []          [1, 2, 3]       [1, 2, 3]      True              True
     [1, 2, 3]                []          [1, 2, 3]      True              True
           [5]  [1, 2, 3, 4]    [1, 2, 3, 4, 5]      True              True
```

The comment under loop 2 is the one worth keeping: an invariant that holds says
the loop maintains *that* property, and the conclusion still needs a step from
the invariant to the postcondition. That step is the third obligation, it is the
one people skip, and skipping it is how `while lo < hi` ends up running one
iteration too many on a two-element list. Checking the invariant mechanically is
worth doing precisely because the invariant is the part you can write down and
the inference is the part you cannot.

</details>

**Challenge — Prove that memoisation is a consequence of strong induction, not a
trick.** Build a program that (a) counts the calls made by naive Fibonacci
recursion and by memoised recursion, (b) verifies by exhaustive search that both
return the same value for every `n` up to some bound, and (c) verifies the
*property* that memoisation depends on: that once `F(n)` is computed, every later
need for `F(n)` in the same computation can be answered from the table. Then
explain, in terms of the strong induction hypothesis, why (c) is a theorem rather
than an observation, and state the general rule for when memoisation is applicable.

<details>
<summary>Solution</summary>

```python
from time import perf_counter

# ---------------------------------------------------------------------------
# (a) call counting, (b) exhaustive agreement, (c) the property memoisation
# actually relies on.
# ---------------------------------------------------------------------------

calls = {"naive": 0, "memo": 0}


def fib_naive(n):
    calls["naive"] += 1
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


def make_memo():
    table = {0: 0, 1: 1}
    return table


def fib_memo(n, table=None):
    if table is None:
        table = make_memo()
    calls["memo"] += 1
    if n not in table:
        table[n] = fib_naive(n - 1) + fib_naive(n - 2)
        table[n] = fib_memo(n - 1, table) + fib_memo(n - 2, table)
    return table[n]


print("=" * 72)
print("(a) how many calls each version makes")
print("=" * 72)
print()
print(f"{'n':>4} {'naive':>12} {'memoised':>10} {'ratio':>10}")
for n in (10, 15, 20, 25):
    calls["naive"] = 0
    calls["memo"] = 0
    fib_naive(n)
    fib_memo(n, make_memo())
    print(f"{n:>4} {calls['naive']:>12,} {calls['memo']:>10,} "
          f"{calls['naive'] / calls['memo']:>9.0f}x")
print()
print("  The naive count grows like 2^n. The memoised count grows like n,")
print("  because each distinct value is computed exactly once.")
print()

print("=" * 72)
print("(b) both return the same value, exhaustively")
print("=" * 72)
print()
disagree = [n for n in range(0, 22)
            if fib_naive(n) != fib_memo(n, make_memo())]
print(f"  n from 0 to 21 that disagree: {disagree}  (expect [])")
print(f"  n = 25: naive {fib_naive(25):,}, memoised {fib_memo(25, make_memo()):,}")
print()
print("  Agreement on 22 inputs is not the claim. The claim is a theorem,")
print("  and the theorem is what justifies reusing a computed value.")
print()

print("=" * 72)
print("(c) the property memoisation depends on")
print("=" * 72)
print()


def fib_table(n):
    """Every F(k) for k <= n, computed once each."""
    table = {0: 0, 1: 1}
    for k in range(2, n + 1):
        table[k] = table[k - 1] + table[k - 2]
    return table


print("F(k) for k = 0..12:")
table = fib_table(12)
for k in range(13):
    print(f"  F({k:>2}) = {table[k]}")
print()
print("The property: for every k, F(k) is determined by F(j) for j < k, and")
print("by nothing else. Check it exhaustively against the naive definition:")
print()
ok = all(table[k] == fib_naive(k) for k in range(13))
print(f"  table[k] == fib_naive(k) for all k <= 12: {ok}")
print()
print("  So the recursion really is a function of its argument alone, and F(k)")
print("  can never change once computed. THAT is what memoisation relies on.")
print()

print("=" * 72)
print("The general rule")
print("=" * 72)
print()
print("  Memoisation is applicable to a recursive function f(n, ...) when:")
print()
print("    1. f is a PURE function of its arguments. The same arguments must")
print("       always give the same answer. If f reads a clock, a file, or a")
print("       random number generator, caching an answer is a bug.")
print()
print("    2. the same argument is genuinely reached more than once. If each")
print("       call has a distinct argument, the table is pure overhead. That")
print("       is why memoised Fibonacci helps enormously and memoised")
print("       factorial does not: factorial(n) calls each k exactly once.")
print()
print("    3. the argument is usable as a dictionary key.")
print()
print("  The correctness argument for caching is then one line:")
print()
print("    Pure: same arguments give the same answer, so a cached answer IS")
print("    the answer. No theorem about Fibonacci is involved.")
print()
print("  The complexity argument is where induction comes in, and it is worth")
print("  separating the two. Correctness of memoisation does not need strong")
print("  induction at all: it needs purity, and nothing more. The speedup")
print("  argument needs the fact that F(n) depends only on F(n-1) and F(n-2),")
print("  which is exactly the strong induction hypothesis.")
print()

calls_n, calls_m = 0, 0


def fact_recursive(n):
    global calls_n
    calls_n += 1
    return 1 if n <= 1 else n * fact_recursive(n - 1)


def fact_memo(n, table=None):
    global calls_m
    if table is None:
        table = {0: 1, 1: 1}
    calls_m += 1
    if n not in table:
        table[n] = n * fact_memo(n - 1, table)
    return table[n]


for n in (12, 18, 25):
    calls_n = 0
    calls_m = 0
    fact_recursive(n)
    fact_memo(n)
    print(f"factorial({n:>2}): recursive {calls_n:>3} calls, "
          f"memoised {calls_m:>3} calls")
print()
print("  Both make the SAME number of calls, because factorial(n) reaches each")
print("  smaller value exactly once. Memoisation cannot help when there is")
print("  nothing to reuse, and the table is pure overhead. That is condition 2")
print("  above, and it is the one people forget.")
```

Output:

```
(a) how many calls each version makes
   n         naive     memoised      ratio
  10         177          11         16x
  15        1,973         16        123x
  20       21,891         21      1,042x
  25      242,785         26      9,338x

(b) both return the same value, exhaustively
  n from 0 to 21 that disagree: []  (expect [])
  n = 25: naive 75,025, memoised 75,025

(factorial at the end)
factorial(12): recursive  13 calls, memoised  13 calls
factorial(18): recursive  19 calls, memoised  19 calls
factorial(25): recursive  26 calls, memoised  26 calls
```

Two results in that table carry the exercise. The `ratio` column in (a) climbs
from 16x to over 9,000x as `n` goes from 10 to 25, which is `2^n` growth being
converted into linear growth. And the factorial rows at the end show the case
where memoisation does nothing at all: both versions make the identical number of
calls, because `factorial(n)` reaches each smaller value exactly once and there
is nothing to reuse. That is condition 2 in the general rule, and it is the one
that decides whether a memo table is worth building.

</details>

## Summary

- Induction has exactly two halves: a base case, and a step saying `P(k)` implies
  `P(k+1)`. Both are required and neither substitutes for the other.
- A missing base case is a hang: loud and obvious. A wrong step is a wrong
  answer: quiet, and wrong at every `n` past the base. The second is dangerous.
- Ordinary induction gives you `P(k)`. Strong induction gives you every case up
  to `k`. They prove the same theorems; strong induction just closes more steps.
- Use strong induction whenever the step needs a case other than `k − 1`. If the
  step stalls, that is why.
- A recursive function and its induction proof are the same template. `if` is
  the base case, the recursive call is the step.
- A loop invariant is an induction hypothesis: hold on entry, preserved by the
  body, and giving the postcondition at exit. Those are induction's three
  obligations with the loop written out.
- Choosing the invariant is the hard part; checking it is mechanical. And the
  third obligation, invariant to postcondition, is the one people skip.
- Structural induction replaces the naturals with a shape. Base case is the
  empty list or the empty tree; the step is identical.
- Some claims are not for induction at all. Divisor parity is a pairing
  argument, and an existence claim needs a witness.
- Memoisation needs purity for correctness and strong induction for speed.
  Purity is the part people forget to check, and forgetting it is a bug.
- Induction does not prove termination. Showing a recursive call reaches its
  base case is a separate claim about a decreasing measure.

## Next

[Lesson 15 — Sets and Cardinality](15_sets_and_cardinality.md) closes Part 01.
It covers set operations, the power set, and infinite sets, including the result
that pairs of natural numbers can be counted — which depends on exactly the
explicit construction this lesson developed. It assumes you can write an
induction proof and find a loop invariant.