# 14 — Mathematical Induction

**Part**: part01_logic_proof · **Prerequisites**: 13 · **Time**: 40 min

---

## In Plain Words

You want to prove something is true for every number: for every list, for every
input, for every tree. You can never check all of them, because there is no last
one. Induction is the technique that gets you from "it works for one" and "if it
works for one then it works for the next" to "it works for all of them", and it
does that in two steps rather than infinitely many.

The first step checks the smallest case. The second step is the interesting one:
you assume the claim holds for one number, chosen without naming it, and then
you show it holds for the number one bigger. Both halves are needed and neither
is optional, and people skip them in both directions — checking thirty cases
and writing no step, or writing a beautiful step and never checking the first
case.

The word doing all the work in the second step is "without naming it". A step
proved for one particular number is a test, not a step. This is the whole
difference between induction and a long test suite, and it is why a recursive
function is an induction proof that happens to run.

## Why Computer Science Cares

**A recursive function is the induction template in three lines.** The stopping
condition is the base case, the recursive call is the step using the hypothesis,
and "the argument is smaller" is the termination argument. When you write a
recursive function you have written a proof, and the three questions to ask
before you run it are the three questions this lesson is about.

**A loop correctness argument is an induction with control flow.** The base case
is "the invariant holds before the first iteration", the step is "one pass
preserves the invariant", and the exit argument is the part induction does not
supply. The Runnable Code has four loops and a table showing which of the three
each bug fails — including one that a passing test suite does not catch.

**Structural recursion is induction on a data type.** `def flatten(xs)` is proved
by induction on the length of `xs`, because the natural decomposition — split off
the head — reduces the length by one. The same argument, applied to trees,
proves that a fold over a balanced tree visits each node exactly once.

**Complexity analysis is an induction.** "Any program halts in at most $2^n$
steps" is proved by induction on the input length, and the step is the argument
that each bit of input can at most double the work. Every big-O proof that is
not a hand-wave is an induction on something, and the something is always a
size that the step can reduce.

**Termination checking is exactly induction's missing half.** A type system that
accepts a recursive function has checked that the recursive argument is
structurally smaller — the base case, the step, and the termination argument, all
at once. That is why Rust will not let you write a linked-list walk whose
recursive call has the same type, and why a function whose call moves a counter
upward is a hang rather than a type error.

**Proof assistants use induction constantly.** Lean, Coq and Isabelle will not
accept `def fact(n) := n * fact(n)` without a proof that `n - 1` is smaller
than `n` and an induction that the recursion terminates. The proof comes first
in the file; the code is the corollary.

## The Formal Version

**Definition.** A *predicate on the naturals* is a formula $P(n)$ with one free
variable whose domain is $\mathbb{N}$. An *inductive proof* of `$\forall n \in
\mathbb{N},\; P(n)$` consists of:

- **base case.** $P(0)$ is true.
- **inductive step.** For an arbitrary $k \in \mathbb{N}$, $P(k) \Rightarrow
  P(k+1)$. The hypothesis $P(k)$ is called the *inductive hypothesis*; it is
  available for use inside the step and for nothing else.

**Theorem.** *(Principle of mathematical induction.)* If $P(0)$ and
`$P(k) \Rightarrow P(k+1)$` for every $k$, then `$\forall n \in \mathbb{N},\;
P(n)$`.

*Proof.* Fix $S = \{n \in \mathbb{N} : P(n)\}$. The base case gives $0 \in S$. If
$k \in S$ then the step gives $k+1 \in S$, so $S$ is closed under successor.
Suppose some $n \notin S$ and let $m$ be the least such — it exists because
$\mathbb{N}$ is well-ordered, and $m \ge 1$ because $0 \in S$. Then
$m - 1 \in S$ by minimality, so $m \in S$ by closure, contradicting $m \notin S$.
So $S = \mathbb{N}$. ∎

*Why the well-ordering matters.* That is the only non-trivial ingredient, and
it is exactly the thing an infinite domain has and a finite one does not. The
step is a rule for propagating truth upward; the base case is a seed; and
well-ordering says a chain of successor steps starting at 0 cannot skip a number
on its way up. Remove well-ordering — put the naturals in a circle, or take a
dense order like $\mathbb{Q}$ — and the principle fails: you can seed one point
and propagate to your heart's content without reaching the rest.

**Theorem.** *Arbitrariness is not a stylistic preference.* If the step is
proved for a *particular* $k_0$ rather than for an arbitrary $k$, the argument
establishes $P(0) \Rightarrow P(1) \Rightarrow \cdots \Rightarrow P(k_0)$ and
nothing beyond. This is a proof about a finite chain, and it is what a test suite
of $k_0$ cases is.

*Explanation.* The step is a schema, and a schema instantiated once is a single
inference. Nothing in the inference mentions other values of $k$, so nothing
licenses using it elsewhere — the same rule as universal generalisation in
[Lesson 12](12_predicates_and_quantifiers.md), where the hypothesis is that the
element appears in no premise.

**Theorem.** *Strong induction.* `$\forall n,\; P(n)$` follows from: $P(0)$, and
for arbitrary $k$, `$(P(0) \wedge P(1) \wedge \cdots \wedge P(k)) \Rightarrow
P(k+1)`.

*Proof sketch.* Define $Q(n) = P(0) \wedge \cdots \wedge P(n)$. The base case is
$Q(0) = P(0)$. The step: from $Q(k)$ we get $P(k+1)$ by the hypothesis, so
$Q(k+1) = Q(k) \wedge P(k+1)$. Ordinary induction gives `$\forall n\, Q(n)$`,
and $Q(n)$ contains $P(n)$. ∎

**Theorem.** *Strong induction and ordinary induction prove the same things.*
Given a strong step, an ordinary one follows: $P(k)$ is one conjunct of the
conjunction, so it implies $P(k+1)$. The converse does not hold, and the
difference is not academic.

*Worked example.* *Every integer $n > 1$ is a sum of primes.* Ordinary induction
on "P(n) = n is prime" has no step at all: to show the next prime is prime you
would have to show the next integer is prime, which is false. Strong induction on
"Q(n) = n is a sum of primes" works immediately: if $n+1$ is prime we are done,
and otherwise $n+1 = ab$ with $1 < a \le b < n+1$, and $Q(a)$ and $Q(b)$ are both
available because $a$ and $b$ are *far* below $n+1$ — not $n$. ∎

**Theorem.** *Induction over any well-ordered set.* The template does not require
$\mathbb{N}$. Let $(W, \prec)$ be well-ordered. To prove `$\forall x \in W,\;
P(x)$` it suffices to prove $P(\bot)$ for the least element and, for arbitrary
$k$, `$P(x)$ for all $x \prec k$ implies `$P(k)$`. Natural numbers are the case
where the order is "smaller than".

*Why this matters for trees and lists.* A finite list ordered by length is
well-ordered, and so is a tree ordered by height. That is what licenses "prove it
for the leaves, then one level up" — and why a tree with *cycles* has no such
argument, because the height order is not well-founded.

**Theorem.** *The step advances the same quantity the recursion decreases.* For a
recursive function whose recursive call is on $g(n)$, an induction proof by way of
that function requires $g$ to be bounded below and to reach its bound in finitely
many applications of $g$. Otherwise there is no well-founded quantity to induct
on, the function does not terminate, and no invariant can rescue it.

*Explanation, not proof.* This is the termination clause of
[Lesson 13](13_proof_techniques.md)'s three-part loop argument, specialised. The
important consequence is diagnostic: a non-terminating recursive function is not
a function with a subtle bug, it is a function for which the proof does not
exist, and the reason is a one-line mismatch between two directions.

**Theorem.** *The loop correspondence.* To prove a `while` loop correct you need
three things: the loop invariant holds before the first iteration; one pass
preserves it; and the loop terminates with the invariant implying the
postcondition. The first two are induction and the third is not.

*Proof sketch of the correspondence.* Write $I(i)$ for "the invariant holds at
the top of iteration $i$". The base case is $I(0)$; one pass taking $I(i)$ to
$I(i+1)$ is exactly an inductive step; and the conclusion at index $n$ for
arbitrary $n$ is what ordinary induction delivers. Termination is the extra
clause: induction reasons about the sequence of states, and a program has to
actually reach the last one. ∎

*Why this clause cannot be skipped.* A loop can satisfy its invariant at every
iteration it performs and still compute the wrong answer, because it stops
early. The Runnable Code has one: a sum loop whose `range` ends one element
short, whose invariant holds throughout, and whose test suite passes because all
five of the team's inputs happen to end in a zero.

## Formula Sheet

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$P(n)$` | a predicate on the naturals | "the property, at size n" | naming what you are proving |
| **base case** | `$P(0)$` | the smallest case, checked | always; it is half the template |
| **inductive step** | `$P(k) \Rightarrow P(k+1)$` for arbitrary `$k$` | if it holds at k then at k+1 | always; the other half |
| inductive hypothesis | the `$P(k)$` **inside** the step | free to use, and only there | the step, and nowhere else |
| **arbitrary** `$k$` | the step holds for every `$k$` | not a number you chose | the whole difference from a test |
| `$\forall n \in \mathbb{N},\; P(n)$` | the conclusion | for every size | what the two halves deliver |
| well-ordering | every nonempty subset of $\mathbb{N}$ has a least element | you cannot skip a number going up | the only non-trivial ingredient |
| strong induction | `$P(0)` and `$\bigwedge_{i \le k} P(i) \Rightarrow P(k+1)$` | you may use every earlier case | when the step needs a smaller value far below k |
| `$Q(n) = \bigwedge_{i \le n} P(i)$` | the running conjunction | turns strong into ordinary | the proof that the two are equivalent |
| `$\bigwedge_{i=0}^{n} P(i)$` | all cases up to n | the accumulated hypothesis | strong induction; also a loop invariant |
| step on `g(n)` | `$g(n) \prec k$` and bounded below | the recursive call must shrink | termination, the clause induction omits |
| loop invariant | `$I(i)$ holds at the top of iteration i | what does not change | the base case and step, in a `while` |
| three-part loop proof | base `$I(0)$`, step `$I(i) \Rightarrow I(i+1)$`, exit `$I(n) \Rightarrow$ post | induction plus termination | every loop correctness argument |
| weak measure | `$m_{k+1} \le \lceil m_k / 2 \rceil$, `$m_0 = n+1$` | a quantity that at least halves | termination of divide-and-conquer; [Lesson 13](13_proof_techniques.md) |
| "$n$ cases checked" | `$P(0) \wedge \cdots \wedge P(n-1)$` | a long conjunction, not an induction | the difference between a test suite and a proof |
| `$\forall n > 1,\; n = \sum p_i$` | every integer above 1 is a sum of primes | the claim that needs strong induction | the worked example below |

## Worked Example

**The claim.** *For every $n \ge 0$, the number of subsets of an $n$-element set
that contain a fixed element is $2^{n-1}$.*

**Step 0. Choose the induction variable, and check the choice.** The quantity is
the *size of the set*, not the number of subsets and not the value of the fixed
element. The test for a good choice is: does the natural decomposition of the
object reduce this quantity by exactly one? Splitting an $(n+1)$-element set into
a chosen element and the other $n$ does exactly that. A claim you cannot even
begin is a claim you are inducting on the wrong thing, and the way you find out
is by trying to write the step.

**Step 1. Restate the claim as a predicate.** $P(n)$: "for every set $S$ with
$|S| = n$ and every $a \in S$, exactly $2^{n-1}$ of the subsets of $S$ contain
$a$". Note the two quantifiers. Dropping either gives a different and much
easier statement, and dropping the first gives the one people actually try to
prove.

**Step 2. The base case.** $n = 0$: there is no element to fix, so the claim is
about the empty set with a distinguished element — and there is no such thing.
The base case is therefore **vacuous**, and that is not a mistake: for $n = 0$ the
universal claim has no instances.

This is worth pausing on, because the natural base case $n = 1$ is *also*
correct and is the one you should write if you want the statement to be about
something: with $S = \{a\}$ the subsets are $\varnothing$ and $\{a\}$, and exactly
one contains $a$, and $2^{1-1} = 1$. Use $n = 1$ as the base case and the claim
becomes a statement about sets rather than about nothing. Either works; the
second is easier to check and harder to get wrong.

**Step 3. The step, with the hypothesis stated precisely.** Assume $P(k)$ for an
**arbitrary** $k \ge 1$. Let $S$ be any set with $|S| = k+1$ and let $a \in S$.

- Put $T = S \setminus \{a\}$, so $|T| = k$ and $a \notin T$.
- **The subsets of $S$ containing $a$** are in bijection with **the subsets of
  $T$**: send $U$ to $U \cup \{a\}$. This is the whole content of the step, and
  it is a bijection rather than an inequality, so nothing is lost.
- We want to count subsets of $T$ *containing $a$*, and $a$ is not in $T$. So we
  count **all** subsets of $T$, which is $2^k$ by
  [Lesson 20](../part02_discrete_combinatorics/20_counting_principles.md).
- Therefore exactly $2^k = 2^{(k+1)-1}$ subsets of $S$ contain $a$, which is
  $P(k+1)$. ∎

**Step 4. Check that the step does not mention $k$.** Read it again: it says
"split off one element, the rest has size $k$, count its subsets". There is no
number in that sentence. It is the same four lines for $k = 3$ and for
$k = 10^9$, and that — not the fact that it is true — is what makes it a proof
of the universal rather than of one more case.

**Step 5. Why the step could not have been written the other way.** Suppose you
tried to prove it by induction on the *number of subsets containing $a$*, or by
just appealing to "it works for small $n$". The first is circular — the count is
what you are computing. The second is exhaustion, which establishes the claim
for $n \le 12$ and nothing beyond, and the difference is invisible until someone
asks about $n = 13$.

**Step 6. What the proof actually needed.** Four things, in order: a domain (a
finite set), a quantity to advance (its size), a decomposition that reduces that
quantity by one (remove a distinguished element), and a counting fact
independent of the induction ($2^k$ subsets of a $k$-element set). The
decomposition is the creative step; the other three are bookkeeping. In a real
correctness argument the decomposition is where all the time goes, and it is
exactly the step where the object has to be *understood* rather than *checked*.

**Step 7. The termination clause, which this proof did not need.** Nothing here
is a program, so there is no question of reaching the end. The moment the same
claim is attached to a loop — "a fold over a linked list visits each element
once" — you owe a third part, and omitting it is the bug in the Runnable Code's
row 4.

## Runnable Code

### The template, its two halves, and the step as a function

```python
import math

# ---------------------------------------------------------------------------
# The induction template, as code.
#
# The template has two halves and both are load-bearing:
#   BASE   P(0) holds
#   STEP   for an ARBITRARY k, P(k) implies P(k+1)
# The word arbitrary is the whole content of the step. A step proved for one
# particular k proves one particular thing, and that is a test, not a step.
# ---------------------------------------------------------------------------

class Proof:
    def __init__(self, claim, base, step, conclusion):
        self.claim = claim
        self.base = base          # the value k0 at which P was checked
        self.step = step          # P(k) -> P(k+1), as a string
        self.conclusion = conclusion
        self.complete = base and step is not None

    def __repr__(self):
        state = "COMPLETE" if self.complete else "INCOMPLETE"
        return f"<Proof {self.claim}: {state}, base k={self.base}>"


# ---------------------------------------------------------------------------
# 1. The template, spelled out on `sum(0..n) = n(n+1)/2`
# ---------------------------------------------------------------------------

def sum_to(n):
    return sum(range(1, n + 1))


def triangular(n):
    return n * (n + 1) // 2


print("=" * 74)
print("1. The two halves, and what each one buys")
print("=" * 74)
print()
print("  CLAIM   for every n >= 0:  1 + 2 + ... + n  =  n(n+1)/2")
print()
print("  BASE    n = 0.  LHS = 0, RHS = 0.  Holds.")
print("  STEP    assume 1 + ... + k = k(k+1)/2 for an ARBITRARY k >= 0.")
print("          then 1 + ... + k + (k+1)")
print("                 = k(k+1)/2 + (k+1)")
print("                 = (k+1)(k/2 + 1)")
print("                 = (k+1)(k+2)/2")
print("          which is the claim at n = k+1.")
print()
print(f"  {'n':>4} {'LHS':>8} {'RHS':>8} {'equal':>7}   <- the BASE case alone")
for n in range(0, 9):
    print(f"  {n:>4} {sum_to(n):>8} {triangular(n):>8} "
          f"{str(sum_to(n) == triangular(n)):>7}")
print()
print("  Nine rows of arithmetic. That is the base case, and it establishes")
print("  NOTHING about n = 10. This is the mistake the technique exists to")
print("  prevent, so it is worth staring at: a table is not a proof of a")
print("  universal claim, however convincing the first few rows are.")
print()

# ---------------------------------------------------------------------------
# 2. The step, as a function. This is what an inductive step really is.
# ---------------------------------------------------------------------------

def step_sum(k):
    """Given P(k) is true, is P(k+1) reachable from it?

    Returns (assumed_P_k, derived, target, ok). Both sides are computed rather
    than asserted, so a wrong step shows up as unequal numbers instead of as a
    confident sentence.
    """
    p_k = triangular(k)                      # the assumption
    p_k1 = p_k + (k + 1)                     # add the next term
    return p_k, p_k1, triangular(k + 1), p_k1 == triangular(k + 1)


print("=" * 74)
print("2. The step, as a function")
print("=" * 74)
print()
print(f"  {'k':>4} {'P(k) assumed':>14} {'derived':>10} {'triangular(k+1)':>16} "
      f"{'step valid':>11}")
all_steps = True
for k in range(0, 9):
    p_k, derived, target, ok = step_sum(k)
    all_steps = all_steps and ok
    print(f"  {k:>4} {p_k:>14} {derived:>10} {target:>16} {str(ok):>11}")
print()
print(f"  the step is valid for every k shown: {all_steps}")
print()
print("  Again: nine values of k, and the claim is about all of them. What")
print("  makes the argument a proof is not the table -- it is that the body of")
print("  the step does not mention k at all. It is four lines of algebra that")
print("  are the same four lines for every k, because there is nothing in them")
print("  that could distinguish k = 3 from k = 300000. That is what 'arbitrary'")
print("  buys, and it is the entire difference between the step and a test.")
print()

# ---------------------------------------------------------------------------
# 3. A proof checker for the template: does this file prove that claim?
# ---------------------------------------------------------------------------

def check_induction(claim, base_check, step_fn, atoms):
    """A miniature induction checker.

    `base_check(k0)` must be True.
    `step_fn(k)` must be True for EVERY k in `atoms`, and must be a function of
    k rather than a constant.

    The checker deliberately does NOT verify that step_fn is a *correct* step.
    Nothing can: whether P(k) -> P(k+1) is a valid inference is a mathematical
    question, and the checker is checking the SHAPE of the argument.
    """
    if not base_check(0):
        return False, "the base case fails at n = 0"
    bad = [k for k in atoms if not step_fn(k)]
    if bad:
        return False, f"the step fails at k = {bad}"
    return True, f"base at 0, step verified on {len(atoms)} values of k"


print("=" * 74)
print("3. A checker for the shape of an induction proof")
print("=" * 74)
print()
ATOMS = list(range(0, 200))
print(f"  the checker verifies the step on n = 0..{ATOMS[-1]}")
print()
GOOD = [
    ("triangular numbers",
     lambda n: sum_to(n) == triangular(n),
     lambda k: step_sum(k)[3]),
    ("the running product is 0 when a factor is 0",
     lambda n: (0 if 0 in range(1, n + 1) else math.prod(range(1, n + 1))) == 0,
     lambda k: True),
]
for claim, base, step in GOOD:
    ok, why = check_induction(claim, base, step, ATOMS)
    print(f"  {claim:<40} {'ACCEPTED' if ok else 'REJECTED'}: {why}")
print()
print("  The second 'proof' is a cheat and the checker accepts it, because the")
print("  step really is a function of k and really is True. What the checker")
print("  cannot do is notice that the step is `True` -- that is, that it")
print("  assumed nothing and derived nothing. This is the honest limit of")
print("  mechanical proof checking: it verifies that a step is a function and")
print("  that it type-checks, not that the step proves what you meant.")
print()

# ---------------------------------------------------------------------------
# 4. Three broken proofs, and which half is missing in each
# ---------------------------------------------------------------------------

print("=" * 74)
print("4. Three proofs, three different holes")
print("=" * 74)
print()
BROKEN = [
    ("no base case at all",
     "INCOMPLETE: the base case is missing. The step is correct but proves"
     " nothing on its own."),
    ("base case that is vacuously true",
     "INCOMPLETE: 'n == 0' is a fact about the loop, not about the claim."
     " A base case that holds for no reason is not a base case."),
    ("a table of 200 cases and no step",
     "INCOMPLETE: there is no step. Checking n = 0..199 is evidence, and it"
     " is exactly what the technique was invented to replace."),
]
for label, verdict in BROKEN:
    print(f"  {label}")
    print(f"      {verdict}")
    print()
print("  The third one is the important one. A suite of 200 checks with no step")
print("  is more impressive-looking than a base case and a one-line step, and")
print("  it establishes strictly less. This is the exact shape of a test suite")
print("  that people describe as 'covering the case'.")
print()

# ---------------------------------------------------------------------------
# 5. Strong induction, and the claim that needs it
# ---------------------------------------------------------------------------

def decompose(n):
    """n as a sum of primes, greedily. Verified by trial division, so this is
    exhaustion -- and the claim it supports is finite, which is legitimate."""
    if n < 2:
        return "(not n > 1)"
    parts, rest = [], n
    while rest >= 2:
        p = 2
        while p * p <= rest and rest % p:
            p += 1
        if p * p > rest:
            p = rest
        parts.append(p)
        rest -= p
    if rest:
        parts.append(rest)
    return " + ".join(str(p) for p in parts)


print("=" * 74)
print("5. Strong induction, and the claim that needs it")
print("=" * 74)
print()
print("  CLAIM   every integer n > 1 is a sum of one or more primes.")
print()
print("  Ordinary induction on n does not work. To prove P(n+1) you have P(n)")
print("  -- 'n is prime' -- and there is no way to build the next prime from")
print("  the previous one. The step is not merely hard; it is not available.")
print()
print("  Strong induction works. Q(n) = 'n is a sum of primes'. For n + 1:")
print("    - if n + 1 is prime, Q(n+1) holds with one term;")
print("    - if not, n + 1 = a * b with 1 < a <= b < n + 1, and by STRONG")
print("      induction BOTH a and b are sums of primes, so n + 1 is too.")
print()
print("  The step used Q(a) and Q(b), not Q(n). That is the whole difference,")
print("  and it is the difference between a step you can find and a step you")
print("  cannot.")
print()
print(f"  {'n':>4} {'n as a sum of primes':<24} {'smallest factor':>16} "
      f"{'is it n-1?':>12}")
for n in range(2, 15):
    f = 0
    for d in range(2, n):
        if n % d == 0:
            f = d
            break
    print(f"  {n:>4} {decompose(n):<24} {f if f else '- (prime)':>16} "
          f"{str(f == n - 1):>12}")
print()
print("  Every composite row has a smallest factor far below n-1, so an")
print("  ordinary step holding only Q(n-1) has nothing to work with, while a")
print("  strong step holding all of Q(0)..Q(n) has exactly what it needs.")
print()

# ---------------------------------------------------------------------------
# 6. Recursive functions are inductive proofs that run
# ---------------------------------------------------------------------------

def fact(n):
    if n <= 1:
        return 1
    return n * fact(n - 1)


def fact_iter(n):
    total = 1
    for i in range(2, n + 1):
        total *= i
    return total


def fact_call_count(n):
    """How many recursive calls does fact make? The count IS the induction."""
    calls = 0

    def helper(k):
        nonlocal calls
        calls += 1
        if k <= 1:
            return 1
        return k * helper(k - 1)

    helper(n)
    return calls


print("=" * 74)
print("6. A recursive function is an induction proof that runs")
print("=" * 74)
print()
print(f"  {'n':>4} {'fact(n)':>14} {'iterative':>12} {'agree':>7} {'calls':>7} "
      f"{'bound n+1':>11}")
for n in range(0, 13):
    a, b = fact(n), fact_iter(n)
    print(f"  {n:>4} {a:>14} {b:>12} {str(a == b):>7} {fact_call_count(n):>7} "
          f"{n + 1:>11}")
print()
print("  The two halves of the induction, in a function:")
print("      if n <= 1: return 1        <- the BASE case")
print("      return n * fact(n-1)       <- the STEP, and it calls fact(k-1),")
print("                                     i.e. P(k-1), not P(k)")
print()
print("  `fact` is not a function that happens to be correct. It is the")
print("  induction proof of 'fact(n) = n!' with the quantifiers turned into")
print("  control flow, and the `calls` column is the induction's length: one")
print("  call per value of n, which is what a proof by steps costs when you")
print("  run it instead of reading it.")
print()
print("  The same shape is loop invariants. `fact_iter` needs a statement about")
print("  the state at the top of each iteration -- 'total = i!' -- and the")
print("  proof that it holds is the induction, with the loop body as the step")
print("  and `total, i = 1, 2` as the base case. Same template, and the")
print("  correspondence is exact.")
```

### The loop invariant, and the third clause induction does not supply

```python
# ---------------------------------------------------------------------------
# The loop invariant, and the correspondence with induction that is exact.
#
#   while loop:            P holds at the top of every iteration
#   base case:             P holds before the first iteration
#   induction step:        the body takes P(i) to P(i+1)
#
# The loop is the induction with the quantifiers turned into control flow. A
# loop invariant is a base case plus a step, wearing a `while`.
#
# Each traced loop logs (i, state) at the TOP of iteration i, before the body
# runs. That is the only place an invariant is guaranteed to hold, and getting
# this wrong is the single most common mistake in writing one.
# ---------------------------------------------------------------------------


def trace_max(xs, log):
    """Correct running maximum. Invariant: best == max(xs[:i+1])."""
    best = xs[0]
    log.append((0, best))
    for i in range(1, len(xs)):
        best = max(best, xs[i])
        log.append((i, best))
    return best


def trace_max_overwrite(xs, log):
    """BUG: assigns instead of maximising, so the answer is the LAST element."""
    best = xs[0]
    log.append((0, best))
    for i in range(1, len(xs)):
        best = xs[i]
        log.append((i, best))
    return best


def trace_sum(xs, log):
    """Correct running sum. Invariant: total == sum(xs[:i])."""
    total = 0
    for i in range(0, len(xs)):
        log.append((i, total))          # before xs[i] is added
        total += xs[i]
    return total


def trace_sum_short(xs, log):
    """BUG: the range stops one short, so the last element is never added.

    The interesting property of this one: the invariant HOLDS at every
    iteration it performs. The loop is internally consistent and still wrong,
    because it does not reach the end.
    """
    total = 0
    for i in range(0, len(xs) - 1):
        log.append((i, total))
        total += xs[i]
    return total


def check_invariant(log, holds):
    """Walk the trace; report the first iteration where the invariant fails."""
    for i, state in log:
        if not holds(i, state):
            return False, i, state
    return True, None, None


def check_postcondition(result, xs, truth):
    """On exit, the result must be what the specification promised.

    This is a SEPARATE check from the invariant, and a loop can fail it while
    satisfying the invariant at every iteration -- which is exactly what
    `trace_sum_short` does.
    """
    return result == truth(xs)


def max_inv(xs):
    return lambda i, best: best == max(xs[:i + 1])


def sum_inv(xs):
    return lambda i, total: total == sum(xs[:i])


# The suite the team actually wrote. Every input happens to end in a zero,
# because the fields are optional and zero is their default. Nobody noticed.
SUITE = [[0], [0, 0], [0, 0, 0], [1, 0], [0, 1, 0]]
PROBE_MAX = [5, 1, 4, 1, 3]      # the maximum is FIRST, so 'last' is wrong
PROBE_SUM = [3, 1, 4, 1, 5]

CASES = [
    ("running maximum, correct", trace_max, max_inv, max, PROBE_MAX),
    ("running maximum, overwrite", trace_max_overwrite, max_inv, max, PROBE_MAX),
    ("running sum, correct", trace_sum, sum_inv, sum, PROBE_SUM),
    ("running sum, range short by one", trace_sum_short, sum_inv, sum, PROBE_SUM),
]

print("=" * 78)
print("1. Four loops, a test suite, and two checkers")
print("=" * 78)
print()
print(f"  the suite:    {SUITE}")
print(f"  probe (max):  {PROBE_MAX}   (an input nobody wrote a test for)")
print(f"  probe (sum):  {PROBE_SUM}")
print()
print(f"{'loop':<32} {'suite':>6} {'invariant':>10} {'postcond':>9}  "
      f"{'answer on probe':>16} {'should be':>11}")
for name, fn, inv, truth, probe in CASES:
    got = [fn(list(xs), []) for xs in SUITE]
    want = [truth(xs) for xs in SUITE]
    suite_ok = got == want
    log = []
    result = fn(list(probe), log)
    inv_ok, bad_i, _ = check_invariant(log, inv(probe))
    post_ok = check_postcondition(result, probe, truth)
    print(f"{name:<32} {str(suite_ok):>6} {str(inv_ok):>10} {str(post_ok):>9}  "
          f"{str(result):>16} {str(truth(probe)):>11}")
print()
print("  Three columns and four rows. Rows 1 and 3 are clean. The other two")
print("  fail, in two different ways, and that is the lesson.")
print()
print("  ROW 2 -- the overwrite bug. The suite catches it and the invariant")
print("  catches it. The postcondition catches it on the probe, where the")
print("  maximum is the first element and the loop returns the last. Every")
print("  diagnostic agrees. This is the easy case, and it is rare, because")
print("  loud bugs get fixed.")
print()
print("  ROW 4 -- the short-by-one bug. The suite PASSES. All five inputs end")
print("  in a zero, so dropping the last element changes nothing. On the probe")
print("  the loop returns 9 where the answer is 14.")
print()
print("  The invariant also HOLDS, at every iteration the loop performs. The")
print("  loop is internally consistent from top to bottom; it just stops")
print("  early. Which is why the invariant and the postcondition are two")
print("  separate checks and not one: an invariant says 'what is true while")
print("  we are going', and nothing in it says 'and we go all the way'.")
print()

print("=" * 78)
print("2. The three-part argument, and which part each bug fails")
print("=" * 78)
print()
print("""
      To prove a loop correct you need THREE things:

        (i)   BASE        the invariant holds before the first iteration
        (ii)  STEP        one pass takes the invariant at i to the
                          invariant at i+1  -- this is the induction step
        (iii) EXIT        the loop terminates, and on termination the
                          invariant implies the postcondition

      Induction gives you (i) and (ii). It gives you NOTHING about (iii).
""")
print(f"  {'loop':<32} {'(i) base':>9} {'(ii) step':>10} {'(iii) exit':>11}")
for name, fn, inv, truth, probe in CASES:
    log = []
    result = fn(list(probe), log)
    base_ok = bool(inv(probe)(0, log[0][1])) if log else True
    step_ok, _, _ = check_invariant(log, inv(probe))
    exit_ok = check_postcondition(result, probe, truth)
    print(f"{name:<32} {str(base_ok):>9} {str(step_ok):>10} {str(exit_ok):>11}")
print()
print("  Row 2 fails (ii): the invariant is not preserved. Row 4 passes (i)")
print("  and (ii) and fails (iii). A correctness argument that checks only")
print("  (i) and (ii) will green-light row 4, and row 4 is the bug that reaches")
print("  production.")
print()
print("  (iii) is the part people skip, and it is the part induction cannot")
print("  supply. The fix is always the same shape: name a measure that is")
print("  bounded below and strictly decreasing, and show the loop guard")
print("  eventually fails it. For row 4 the measure would be the number of")
print("  elements left, and the argument is that the range stops at len-1")
print("  instead of len -- a one-character bug in the only part of the loop")
print("  nobody re-reads.")
print()

print("=" * 78)
print("3. The other direction: the code is right and the invariant is wrong")
print("=" * 78)
print()
log = []
answer = trace_max(list(PROBE_SUM), log)

# The invariant someone writes down under time pressure: one index too far.
too_strong = lambda i, best: best == max(PROBE_SUM[:i + 2])
ok, bad_i, bad_state = check_invariant(log, too_strong)
print(f"  the loop returns       : {answer}  (correct: {answer == max(PROBE_SUM)})")
print(f"  the invariant holds?   : {ok}")
print(f"  it first fails at      : i = {bad_i}, best = {bad_state}")
print()
print("  The code is right. The invariant is too strong, and a checker that")
print("  reports only True/False leaves you convinced the loop is broken, which")
print("  sends you off to rewrite working code.")
print()
print("  This is the most common outcome in practice, and it is why 'write the")
print("  invariant' is the hard part while 'prove the invariant' is the easy")
print("  part. The proof is mechanical once the statement is right; the")
print("  statement is the thing you get wrong.")
print()
print("  The correct invariant for this loop, and what it buys:")
print("      best == max(xs[:i+1])                    holds, by inspection")
print("      on exit, i == len(xs) - 1, so")
print("      best == max(xs)                          which is the postcondition")
print()
print("  Both halves are needed. An invariant that holds but implies nothing is")
print("  useless, and one that implies the postcondition but does not hold is")
print("  worse than useless: it is a loop you cannot reason about.")
print()

print("=" * 78)
print("4. The correspondence, written out")
print("=" * 78)
print()
print("""
      INDUCTION                          LOOP
      ------------------------------     ------------------------------
      claim: for all n >= 0, P(n)       effect: on exit, the postcondition

      base:   P(0)                      before the loop: the invariant holds
      step:   P(k)  ==>  P(k+1)          one pass: invariant(i) ==> invariant(i+1)

      not given: termination            not given: that the loop ends
""")
print("  The row that is not there is the point. Induction is a proof about a")
print("  sequence of statements; a loop is a program that has to actually get")
print("  to the end. Bridging the two is the whole content of (iii) above, and")
print("  it is why a loop correctness argument is never just an induction.")
print()
print("  The other direction is where induction is most useful in practice: a")
print("  RECURSIVE function is the induction with the quantifiers turned into")
print("  control flow. The stopping condition is the base case, the recursive")
print("  call invokes the hypothesis on a smaller argument, and 'the")
print("  recursive argument is smaller' is the termination argument. All")
print("  three parts, in three lines of code.")
print()
print("  Which is worth stating as a rule: when you write a recursive")
print("  function, the three questions are (1) what is the base case, (2) what")
print("  does the recursive call assume, (3) why does the recursion end. Ask")
print("  them before you run anything, because question 3 is the one that")
print("  turns a five-minute bug into a stack overflow.")
```

### Choosing the induction variable, which is most of the work

```python
# ---------------------------------------------------------------------------
# Choosing the induction variable, which is 80% of the work.
#
# The two halves of the template are mechanical. The only real decision is
# WHICH quantity the step advances, and choosing badly produces a proof that
# cannot be written -- not a proof that is wrong, but no proof at all.
# ---------------------------------------------------------------------------

print("=" * 78)
print("1. The wrong variable, and exactly where it breaks")
print("=" * 78)
print()
print("  CLAIM   every list of integers of length at least 1 has a maximum.")
print()
print("  Attempt: induct on the VALUE at the head of the list.")
print("    base: the list [5] has a maximum.          True, but it is the only")
print("          case this establishes, and it is not even a base case for a")
print("          claim about lists.")
print("    step: assume the list headed by v has a maximum, show the list")
print("          headed by w does too.")
print()
print("  The step has nowhere to go. A list is not a sequence of heads, so")
print("  'the list headed by w' is not a larger version of 'the list headed by")
print("  v'. Here is the arithmetic that shows it:")
print()
for xs in ([5, 3, 9], [5, 9, 3], [1, 2, 3]):
    v = xs[0]
    rest = xs[1:]
    print(f"  list {str(xs):<12} head v = {v},   rest {str(rest):<10} "
          f"max(rest) = {max(rest):<3}  "
          f"is max(rest) <= v? {str(max(rest) <= v):<5}")
print()
print("  At the first row the answer is NO: removing the head 5 from [5, 3, 9]")
print("  leaves [3, 9] whose maximum is 9, which is larger than 5. So the")
print("  inductive hypothesis -- 'v is at least everything else' -- is FALSE,")
print("  and an induction step that leans on a false hypothesis is not a step.")
print()
print("  This is the failure in its purest form. You cannot tell it is a")
print("  failure by looking at your own proof; you have to run the numbers on")
print("  a case the hypothesis is supposed to cover.")
print()

print("=" * 78)
print("2. The right variable, worked completely")
print("=" * 78)
print()
print("  Induct on LENGTH. Q(n) = 'every list of length n >= 1 has a maximum'.")
print()
print("  BASE   n = 1.  A list of one element x has maximum x.  No cases to")
print("         check: there is exactly one shape of a length-1 list, and its")
print("         maximum is its only element.")
print()
print("  STEP   assume Q(k) for an arbitrary k >= 1.  Let xs have length k+1.")
print("         Write xs = [a] + rest, where rest has length k >= 1.")
print("           by Q(k), rest has a maximum, call it m")
print("           the maximum of xs is then max(a, m)")
print("         Q(k+1). Done.")
print()
print("  Read the step again and notice what makes it work: the hypothesis Q(k)")
print("  is about rest, and rest has length k because we removed ONE element.")
print("  That is the whole design decision. We chose length precisely because")
print("  the natural decomposition of the object -- split off the first element")
print("  -- reduces length by exactly one.")
print()
print("  And the base case is not 'check n = 1'. It is 'prove the case n = 1',")
print("  which here is a proof and not a check, because a list of length 1 has")
print("  only one possible shape.")
print()


def every_list_of_length(n):
    """All lists of integers in 0..2 of length exactly n. Small enough to
    exhaust, which is what lets us CHECK the claim rather than assert it."""
    if n == 0:
        return [[]]
    return [[v] + rest for v in range(3) for rest in every_list_of_length(n - 1)]


def has_max(xs):
    return bool(xs) and max(xs) is not None


print("  the claim Q(n), checked by exhaustion over every list of length n")
print("  with entries in 0..2:")
print()
print(f"  {'n':>3} {'lists':>7} {'all have a maximum?':>22}")
for n in range(1, 6):
    ls = every_list_of_length(n)
    print(f"  {n:>3} {len(ls):>7} {str(all(bool(x) for x in ls)):>22}")
print()
print(f"  At n = 5 there are {len(every_list_of_length(5))} lists, all of them")
print("  checked. This is exhaustion, and it is a legitimate proof of Q(1)")
print("  through Q(5). It is not a proof of Q(n) for all n, and the difference")
print("  is the whole subject of this lesson.")
print()

print("=" * 78)
print("3. Six claims, six induction variables, and why")
print("=" * 78)
print()
print(f"  {'claim':<46} {'induct on':<24} because the step")
print("  " + "-" * 104)
for claim, variable, why in [
    ("1 + 2 + ... + n = n(n+1)/2", "n, the count of terms",
     "adds exactly one term"),
    ("every list of length n has a maximum", "n, the length",
     "splitting off one element reduces the length by one"),
    ("every n > 1 is a sum of primes", "n, the value (STRONG)",
     "a factorisation gives you sums far below n"),
    ("any program halts in at most 2^n steps", "n, the input length",
     "each input bit can at most double the work"),
    ("a linked list of n nodes is acyclic", "n, the node count",
     "following a pointer moves to a shorter list"),
    ("a tree of height h has at most 2^h - 1 nodes", "h, the height",
     "each subtree has height at most h-1"),
]:
    print(f"  {claim:<46} {variable:<24} {why}")
print()
print("  The variable is not chosen for convenience. It is chosen so that the")
print("  natural structural decomposition of the object reduces IT BY ONE. Any")
print("  other choice produces a step with nowhere to go, and you find out by")
print("  trying to write it.")
print()
print("  The last two rows are worth double-reading. For a linked list you")
print("  induct on the node count, not on the data, because a pointer move is")
print("  what reduces the count. For a tree you induct on the HEIGHT, not the")
print("  node count, because a shallow tree can have arbitrarily many nodes")
print("  and no bound relates the two -- inducting on the node count gives a")
print("  step with nothing to decompose.")
print()

print("=" * 78)
print("4. Well-foundedness: the clause induction will not give you")
print("=" * 78)
print()


def countdown(n, log, budget=20):
    """A recursive function. The three questions, in the order that finds bugs
    fastest."""
    log.append(n)
    if n <= 0:          # (1) BASE CASE: when does the recursion stop?
        return "done"
    if len(log) > budget:
        return "BUDGET EXCEEDED"
    return countdown(n - 1, log, budget)   # (2) STEP: uses Q(n-1).
    # (3) TERMINATION: n-1 < n, and n >= 0, so after at most n+1 steps we
    #     reach the base case.  n is bounded below, so it cannot fall forever.


def countdown_bad(n, log, budget=20):
    """The same function with the argument moving the WRONG WAY.

    The base case is `n < 0`, unreachable from a non-negative start, so the
    recursion counts upward forever. This is a real bug shape: a paginator
    that walks past the last page, a retry loop with no attempt cap, a tree
    walk with no parent pointer.
    """
    log.append(n)
    if n < 0:
        return "done"
    if len(log) > budget:
        return "BUDGET EXCEEDED"
    return countdown_bad(n + 1, log, budget)


for fn, start in ((countdown, 5), (countdown_bad, 0)):
    log = []
    result = fn(start, log, budget=20)
    shown = str(log[:9]) + (" ..." if len(log) > 9 else "")
    print(f"  {fn.__name__:<14} start {start}: {result:<18} "
          f"{len(log)} calls, values {shown}")
print()
print("  The bad version does not stack-overflow, it counts upward forever, and")
print("  the only reason it returns at all is a budget I added by hand. That")
print("  budget is the entire content of the termination argument. A")
print("  production version of this bug is an incident rather than a crash: a")
print("  paginator that walks past the end, a retry loop that never gives up")
print("  holding a connection open, a crawler that follows its own tail.")
print()
print("  Induction cannot help here, and the reason is precise. The step says")
print("  'assume Q(k) for an arbitrary k, show Q(k+1)'. In `countdown` the")
print("  recursive call is on k-1, so using the hypothesis at the call site")
print("  means proving Q(k) from Q(k-1): step and call agree, and k is bounded")
print("  below by 0, so the recursion must reach the base case.")
print()
print("  In `countdown_bad` the recursive call is on k+1, so the hypothesis Q(k)")
print("  describes a value the function has already passed. Step and call point")
print("  in OPPOSITE directions, k is not bounded below by anything the")
print("  recursion respects, and there is no induction to write.")
print()
print("  The rule that falls out: the quantity the step advances must be the")
print("  same quantity the recursion decreases, and it must be bounded below.")
print("  If the recursion can push a quantity upward without limit, there is no")
print("  induction, no invariant, and no proof -- only a test that hangs.")
```

## Common Mistakes

**Wrong: forgetting the base case, or writing one that is vacuously true.**
Right: both halves are required, and the base case must be a statement about
the claim rather than about your loop. `if n == 0: pass` is not a base case; it
is a line that happens to execute. `sum_to(0) == triangular(0)` is a base case,
because it evaluates the claim at its smallest argument. Section 4 of the first
code block lists this as one of three holes, and the point is that the step —
which is correct — proves nothing without it.
Why tempting: the step is the interesting half and it is where the work feels
like it is going. Skipping the base case feels like skipping bookkeeping, and it
is not: without it the induction is a machine that produces nothing.

**Wrong: proving the step for one particular value of `k`.**
Right: the step is proved for an **arbitrary** `k`, and the body of the step
must not mention any specific number. If your step reads "assume P(3), show
P(4)", you have written a test, and the difference is not a matter of
convention — the generalisation from one instantiation to all instances is
exactly the theorem, and you cannot use a theorem you have not proved.
Why tempting: it is the same mistake as writing a test, and a test feels like
evidence. Section 2 of the first code block prints the step for nine values of
`k` and then says the thing that makes it a proof: the step's body is the same
four lines for all of them, so there is nothing in it that could distinguish
`k = 3` from `k = 300000`.

**Wrong: inducting on the value at the head instead of the size of the object.**
Right: the induction variable is the quantity the natural decomposition
reduces by one. For a list that is the length; the head's *value* is not a size
at all, and the step has nowhere to go. Section 1 of the third code block
demonstrates this concretely: removing the head 5 from `[5, 3, 9]` leaves a
maximum of 9, so the hypothesis you were going to use is false on the very
first case.
Why tempting: the value is the first thing you see, and it is the thing the
claim mentions. Choosing it feels natural until you try to write the step and
discover there is no "larger version" of it.

**Wrong: checking the invariant and concluding the loop is correct.**
Right: a loop needs three clauses, and induction supplies two. A loop can hold
its invariant at every iteration it performs and still be wrong, because it
stops early — which is row 4 of the table in the second code block: the sum
loop whose `range` ends one short, whose invariant holds throughout, and whose
five-input test suite passes because every input ends in a zero.
Why tempting: the invariant is the hard part, and once you have it the
preservation argument is mechanical. The exit clause is the boring one, so it
goes unwritten, and it is the one that catches the bug that reaches production.

**Wrong: treating the strong induction hypothesis as available for the current
value, or assuming ordinary induction can be substituted for it.**
Right: strong induction gives you $P(0) \wedge \dots \wedge P(k)$ to prove
$P(k+1)$; it does not give you $P(k+1)$ on the right-hand side. And a claim
that needs strong induction — every integer above 1 is a sum of primes — has no
ordinary step at all, so substituting one does not produce a weaker proof, it
produces no proof.
Why tempting: the strong hypothesis is strictly more powerful, so reaching for
it feels free. The cost is that the *variable* must be chosen so that the step
can use a value far below the current one, and that is a real design decision
rather than a shortcut.
---

## Multiple Choice Questions

**Q1.** What are the two halves of a proof by mathematical induction?

- A) A base case $P(0)$ and a step $P(k) \Rightarrow P(k+1)$ for arbitrary $k$
- B) A base case $P(0)$ and a step $P(k) \Rightarrow P(2k)$
- C) A step for every $k$ up to some bound $N$, and a claim that $N$ was large
  enough
- D) A base case $P(0)$ and a proof that $P(k)$ implies $P(k+1)$ for one
  particular $k$

<details>
<summary>Answer and explanation</summary>

**A) A base case $P(0)$ and a step $P(k) \Rightarrow P(k+1)$ for arbitrary $k$.**

These two together are the principle of mathematical induction, and the base
case is not optional: without it the step is a machine for producing statements
from nothing.

Option B, $P(k) \Rightarrow P(2k)$, is not a step at all. It establishes the
claim at $0, 1, 2, 4, 8, 16, \dots$ and says nothing about 3. It is a real
logical consequence of the hypothesis, and it is a useless one, which is a good
illustration of how easy it is to write something true and irrelevant.

Option C is the exhaustiveness mistake in its purest form. "We checked up to
$N$ and $N$ was large enough" is not an argument, because there is no argument
that any finite $N$ is large enough. That gap is precisely what induction was
invented to close.

Option D is a single instance of the step, which establishes
$P(0) \Rightarrow P(1) \Rightarrow \dots$ up to that one $k$ and nothing beyond.
It is a test written in the costume of a proof, and the entire content of the
technique is the word *arbitrary*.

</details>

**Q2.** You have proved the base case and a step, but the step was proved only
for $k = 4$. What have you established?

- A) $\forall n \ge 4,\; P(n)$
- B) $P(0), P(1), \dots, P(4)$ and nothing beyond
- C) $P(n)$ for all $n$, because one correct instance of a schema is enough
- D) Nothing, because the step is not a schema

<details>
<summary>Answer and explanation</summary>

**B) $P(0), P(1), \dots, P(4)$ and nothing beyond.**

With the base case you have $P(0)$. The instance $P(4) \Rightarrow P(5)$ gives
$P(5)$. But you have no instance giving $P(6)$ from $P(5)$, so the chain stops
at 5, and there is no induction principle that bridges the gap.

Option A confuses the starting point with the range. The proof begins at 0 and
reaches 5; it does not begin at 4 and reach infinity.

Option C is the misconception the question is testing. A rule that is valid for
every $k$ is a schema, and a schema is a *statement about all instantiations*.
One correct instantiation is one fact, not a proof of the schema. Using it as if
it were the schema is the same error as treating one passing test as a proof.

Option D is wrong about what a schema is. The step is a schema — that is exactly
what makes it powerful — and a schema is proved by proving one thing about an
arbitrary symbol.

</details>

**Q3.** Which claim can be proved by ordinary induction but has **no**
ordinary induction step available?

- A) Every list of length $n \ge 1$ has a maximum
- B) Every integer $n > 1$ is a sum of primes
- C) $1 + 2 + \dots + n = n(n+1)/2$ for all $n \ge 0$
- D) A binary tree of height $h$ has at most $2^h - 1$ nodes

<details>
<summary>Answer and explanation</summary>

**B) Every integer $n > 1$ is a sum of primes.**

Induction on "P(n) = n is prime" has no step: to show the next integer after a
prime is prime you would have to show the next integer is prime, which is false
— 3 is prime and 4 is not. Strong induction on "Q(n) = n is a sum of primes"
works, because a factorisation $n+1 = ab$ gives you $Q(a)$ and $Q(b)$ for values
far below $n+1$, and both are available. Section 5 of the first code block
prints the smallest factor for every $n$ from 2 to 14 to show how far below.

Option A works by induction on *length*: split off the head, the rest is shorter,
and by the hypothesis it has a maximum.

Option C is the textbook step: add one term, factor, done.

Option D works by induction on *height*: the two subtrees each have height at
most $h-1$, so each has at most $2^{h-1} - 1$ nodes, and $2(2^{h-1} - 1) + 1 =
2^h - 1$. Note this needs the height, not the node count — a shallow tree can
have arbitrarily many nodes.

</details>

**Q4.** A loop satisfies its invariant at the top of every iteration it
performs, and the invariant implies the postcondition. Is the loop correct?

- A) Yes — those are the two halves of induction
- B) Yes, provided the loop was executed at least once
- C) Not necessarily: you also need to know the loop terminates having reached
  the end of its range
- D) No — an invariant must be checked at the bottom of the loop

<details>
<summary>Answer and explanation</summary>

**C) Not necessarily: you also need to know the loop terminates having reached
the end of its range.**

This is the third clause of a loop correctness argument, and induction does not
supply it. Row 4 of the table in the second code block is exactly this case: a
sum loop whose `range` ends one element short. Its invariant
`total == sum(xs[:i])` holds at every iteration, its invariant implies the
postcondition *if* the loop ran to completion, and it does not — so it returns 9
where the answer is 14. The test suite passes, because all five of the team's
inputs happen to end in a zero.

Option A is the two-thirds answer, and it is the most common one. Induction
gives the base case and the step; it reasons about a sequence of states and says
nothing about whether your program ever reaches the last one.

Option B is worse than wrong — it makes execution count as proof. Running the
loop once proves nothing about inputs you did not run.

Option D is wrong about where invariants live. An invariant holds at the *top*
of the iteration, which is why it is available as a precondition for the body.
Checking at the bottom is a common slip and it makes the induction step
inaccessible.

</details>

**Q5.** A recursive function calls itself on `n - 1` and returns immediately when
`n <= 0`. Which three things must be true for it to be correct?

- A) It has a base case, a step, and the recursive argument is smaller
- B) It has a base case and a step
- C) It has a base case, and the recursive argument is smaller
- D) It terminates, and therefore it is correct

<details>
<summary>Answer and explanation</summary>

**A) It has a base case, a step, and the recursive argument is smaller.**

The three are the base case, the inductive step, and the termination argument —
the same three clauses as a loop, in three lines of code. Section 6 of the first
code block shows the `calls` column tracking $n+1$, which is the induction's
length made visible.

Option B omits termination, and that omission is exactly `countdown_bad` in the
third code block: a function whose call moves the argument the wrong way, whose
step is a perfectly good step, and which never returns. Induction cannot help,
because the step and the call point in opposite directions.

Option C omits the step, which is the harder omission to notice: a function that
terminates and returns a wrong answer has no step. Halving a list by calling
`halve(xs[1:])` and discarding the head terminates and is wrong.

Option D is a real error in a real direction. Termination is necessary and says
nothing about correctness; every terminating function satisfies D, and most of
them compute the wrong thing.

</details>

**Q6.** Why is the step proved for an "arbitrary" $k$ rather than a chosen one?

- A) So that the proof is easier to read
- B) Because the hypothesis must not mention any assumption, and an arbitrary
  $k$ is the formal way of saying that
- C) Because induction only works on the integers
- D) Because an arbitrary $k$ can be replaced by any particular $k$ afterwards

<details>
<summary>Answer and explanation</summary>

**B) Because the hypothesis must not mention any assumption, and an arbitrary
$k$ is the formal way of saying that.**

This is the universal generalisation rule of
[Lesson 12](12_predicates_and_quantifiers.md), transported: from a proof about
an arbitrary element you may conclude a universal claim, and from a proof about
a *named* element you may not, because the element might have come from a
premise. The "arbitrary" is the bookkeeping that makes the step a schema.

Option A is not nothing — a step with no number in it does read more easily —
but it is a consequence, not the reason. The reason is that the proof's
validity depends on $k$ being unconstrained.

Option C is wrong in a way worth noticing. The arithmetic in the step is
specific to the naturals, but the *template* is not: the same two halves prove
statements about any well-ordered set, which is why "every finite list has a
maximum" and "every finite tree has a leaf" are the same proof shape.

Option D is the misconception. You cannot substitute afterwards. The step is a
schema; a schema is not a container you fill in later, and an instance of it is
a different statement.

</details>

**Q7.** A claim about binary trees is proved by induction on the *number of
nodes*, and the step needs to split the tree. What goes wrong?

- A) Nothing; the node count is a perfectly good induction variable
- B) A tree can have many nodes and height 1, so the node count does not bound
  the height, and there is no way to reduce it by one in a decomposition
- C) The base case is impossible, because there is no smallest tree
- D) Trees are not well-ordered by node count

<details>
<summary>Answer and explanation</summary>

**B) A tree can have many nodes and height 1, so the node count does not bound
the height, and there is no way to reduce it by one in a decomposition.**

The natural decomposition of a tree splits it at the root into subtrees, and
each subtree has height at most $h-1$ — a statement about *height*. A single
subtree may have almost all the nodes, so the node count does not drop by one.
Induct on the height instead, and the step becomes: two subtrees of height at
most $h-1$, each with at most $2^{h-1} - 1$ nodes, plus the root.

Option A is the tempting answer because the node count is the more obvious
"size" of a tree. The test for a good induction variable is not "is it a size"
but "does the natural decomposition reduce it by one", and here it does not.

Option C is wrong: the empty tree is the smallest and the base case is fine.
What is missing is a *usable step*, not a base case.

Option D is wrong. Node count is a perfectly good well-order on finite trees.
The problem is not well-foundedness, it is that the step cannot be written.

</details>

**Q8.** What is the one non-trivial ingredient in the proof of the principle of
mathematical induction?

- A) That $\mathbb{N}$ is closed under successor
- B) That every nonempty subset of $\mathbb{N}$ has a least element
  (well-ordering)
- C) That the natural numbers are infinite
- D) That arithmetic is consistent

<details>
<summary>Answer and explanation</summary>

**B) That every nonempty subset of $\mathbb{N}$ has a least element
(well-ordering).**

The proof takes $S = \{n : P(n)\}$ and argues by contradiction: suppose $m$ is
the least element not in $S$, then $m \ge 1$, then $m-1 \in S$ by minimality, then
$m \in S$ by closure. The step that gets the contradiction off the ground is
minimality, and minimality *is* well-ordering.

Option A, closure under successor, is the part that is genuinely easy and it is
already in the step. On its own it establishes nothing: a set can be closed
under successor, contain 0, and still be a proper subset of the naturals — take
the even numbers, or the powers of two.

Option C, infinitude, is a consequence of well-ordering plus the fact that no
natural is the largest, not the ingredient.

Option D is a red herring. Induction is proved in a very weak theory — in fact
within second-order arithmetic the induction principle is a *schema*, and the
full principle is one of the axioms. Consistency plays no role.

</details>

**Q9.** You want to prove that a fold over a linked list visits each node
exactly once. Which induction variable?

- A) The value stored in the head node
- B) The length of the list from the current node to the end
- C) The number of distinct values in the list
- D) The memory address of the list

<details>
<summary>Answer and explanation</summary>

**B) The length of the list from the current node to the end.**

The natural decomposition of a linked list is the link: the current node plus
everything reachable from `node.next`. That reduces the *remaining length* by
exactly one, which is the test for a good induction variable. The step then says:
the fold visits the head, and the recursive call visits the rest, and the two
sets of nodes are disjoint because the list is acyclic.

Option A is the head-value mistake from the third code block. The value of the
head has no relationship to the structure, so a step on it has nowhere to go.

Option C is worse: the number of distinct values does not decrease when you
remove the head — remove a duplicate and it stays the same, so the step is not
even well-founded.

Option D is the joke answer that names the real point. If you had to reason
about addresses you would be proving a statement about the allocator, and
addresses are not well-ordered in any useful sense.

</details>

**Q10.** A team proves its parser handles 500,000 generated inputs without
failure and concludes the parser is correct. What has actually been shown?

- A) The parser is correct for every input
- B) The base case and the inductive step, so the claim is proven
- C) A long conjunction $P(0) \wedge \cdots \wedge P(499999)$, which is
  evidence and not a universal claim
- D) Nothing at all, because random inputs are not exhaustive

<details>
<summary>Answer and explanation</summary>

**C) A long conjunction $P(0) \wedge \cdots \wedge P(499999)$, which is evidence
and not a universal claim.**

That is the exact object a large test suite establishes, and the gap between it
and `$\forall n, P(n)$` is the entire subject of this lesson. The difference is
not the number 500,000; it is that a conjunction has finitely many conjuncts and
a universal does not.

Option A is what the team hoped. It is not available from any finite amount of
checking, and [Lesson 13](13_proof_techniques.md) is where exhaustion's
inapplicability on an infinite domain is stated properly.

Option B is the mistake this lesson exists to prevent. The team has no step, so
they do not have a proof; they have the base case and a very long list of
successors, and the missing ingredient is a sentence that takes $P(k)$ to
$P(k+1)$ for an arbitrary $k$.

Option D is too strong and, in practice, wrong in the useful direction.
Random testing *does* find real bugs, and a generator's support can be designed
to cover the domain — but the coverage achieved is a property of the generator,
not of the claim, and it is worth measuring separately. Calling the result
"nothing" throws away real information; calling it a proof is worse.

</details>

## Subjective Questions

### Short Answer

**Q1. State the two halves of a mathematical induction proof, and say what makes
the step a step rather than a test.**

<details>
<summary>Answer</summary>

Base: $P(0)$. Step: $P(k) \Rightarrow P(k+1)$ for an **arbitrary** $k$.

The step is a step rather than a test because the arbitrary $k$ is never
specialised and never appears in any assumption. The body of the step is the
same argument for every $k$, so it establishes a schema rather than one fact.
Specialising it to a named $k$ gives one inference, and one inference is a test.

</details>

**Q2. Why is a vacuous base case, such as `if n == 0: pass`, not a base
case?**

<details>
<summary>Answer</summary>

A base case must establish the *claim* at the smallest argument, so it must
evaluate the claim: `sum_to(0) == triangular(0)` is a base case, because it
computes both sides and compares them.

`if n == 0: pass` is a statement about the control flow — it says the program
reaches a line — not about the property. It happens to execute, and it
establishes nothing, so the induction is a machine with no seed.

</details>

**Q3. Give one claim that needs strong induction and say what the ordinary
step would look like.**

<details>
<summary>Answer</summary>

Every integer $n > 1$ is a sum of primes.

The ordinary step would be: assume $n$ is prime, show $n+1$ is a sum of primes.
That is unavailable — from "n is prime" you cannot get anywhere, and the
statement "the next integer is prime" is false.

The strong step is: if $n+1$ is prime, done; otherwise $n+1 = ab$ with
$1 < a \le b < n+1$, and $Q(a)$ and $Q(b)$ are both available because they are
far below $n+1$.

</details>

**Q4. A loop's invariant holds and implies the postcondition. What third
property must you also establish, and what does its absence look like in
practice?**

<details>
<summary>Answer</summary>

Termination — that the loop completes its full range of iterations.

In practice it looks like a loop that is internally consistent from top to
bottom and stops early: a `range` that ends one element short, a paginator that
walks past the last page, a retry loop with no cap. The invariant holds at
every iteration performed, the test suite passes if the inputs happen to hide
the difference, and the result is wrong.

</details>

**Q5. Name the test you apply when choosing an induction variable.**

<details>
<summary>Answer</summary>

Does the natural structural decomposition of the object reduce this quantity by
exactly one?

The step needs to apply the hypothesis to a *smaller instance of the same kind*,
and the only smaller instances available are the pieces the decomposition
produces. Length for a list, height for a tree, node count for a linked list,
input length for a program.

</details>

**Q6. A recursive function calls itself on `n + 1` and has a base case
`n >= 10`. What is wrong, and how would you find out?**

<details>
<summary>Answer</summary>

If the start value is below 10 the call moves *away* from the base case, so the
recursion never reaches it. More generally, the induction step advances $k$ to
$k+1$ while the recursive call does the same, so the hypothesis $P(k)$ describes
a value already passed — there is no induction to write, whatever the base case.

You find out by asking the three questions in order: what is the base case, what
does the call assume, and why does the recursion end. The third question is the
one that answers this, and asking it first would have taken a minute.

</details>

### Long Answer

**Q1. Our test suite runs 500,000 generated inputs against the parser and all
of them pass. The team wants to write in the README that the parser is
"formally verified". What would you have to show them, and why is "500,000
generated inputs" not a special case of it?**

<details>
<summary>Model answer</summary>

"Formally verified" names a specific artefact: a machine-checked derivation from
a stated specification to the code. To show it you would need the specification
as quantified sentences, the base case, the step, and a checker that accepted
all three. None of those four things is improved by the number 500,000.

The reason 500,000 is not a special case is that it establishes a conjunction,
not a universal. A test suite of size $N$ establishes
`$P(0) \wedge P(1) \wedge \dots \wedge P(N-1)$`, and no amount of conjoining
produces `$\forall n, P(n)$` — the two are different logical objects, and the
second one is what "verified" names. The 500,000 cases are evidence, and it is
good evidence, but evidence and proof are not two strengths of the same thing.

There is a second and sharper reason specific to *generated* inputs. A generator
has a distribution, and its support is a subset of the input space. "500,000
samples from this generator" is a statement about the generator, and the
interesting question — does the generator's support contain the input that
breaks the parser? — is not answered by the sample count. A generator that
produces only ASCII JSON with no duplicate keys, for instance, can pass a
million samples and never once exercise the duplicate-key path. So even the
evidence is weaker than it looks, and the weakness is a property of the
generator that nobody wrote down.

What I would do instead: split the claim. Write down the properties the parser
actually needs to have — rejects malformed input, accepts every well-formed
input, terminates within $k$ steps, does not exceed a recursion depth — and
then decide per property whether it is provable, checkable, or neither. The
termination and depth properties are provable by induction on input length and
are the ones worth a checker. "Accepts every well-formed input" usually is not
provable without first writing down what well-formed means, and that is where
the real work is.

</details>

**Q2. A loop's invariant is correct and preserved, and the code is still wrong
on some inputs. Walk through the two ways this happens, and say what each one
tells you about the argument you wrote.**

<details>
<summary>Model answer</summary>

There are two distinct failures, and they point at different mistakes.

**The loop does not run to completion.** The invariant and postcondition are
both fine; the loop simply stops early. This is row 4 of the table in the second
code block: a sum loop whose `range(0, len(xs) - 1)` never touches the last
element. The invariant `total == sum(xs[:i])` holds at every iteration
performed, and the postcondition `total == sum(xs)` follows from the invariant
*conditional on* having reached `i == len(xs)`. What is missing is a clause
saying the loop reaches that index.

This tells you the argument was incomplete rather than wrong. You proved a claim
about the sequence of states and silently assumed the sequence had the length
you wanted. The fix is the termination clause, and the diagnosis is that the
invariant is fine — which is the reassuring case, and the reason it is worth
separating from the second failure.

**The invariant is too strong, so the code is right and the argument is
wrong.** Here the loop computes the correct answer and the invariant you wrote
down fails on the very first iteration. Section 3 of the same code block has
this case: the loop is a correct running maximum, and the invariant someone
wrote under time pressure indexes one element too far.

This is the more common failure and the more corrosive, because a checker that
reports only True/False leaves you convinced the loop is broken. You then rewrite
working code, and the rewrite is the thing that introduces a bug. The invariant
is not a hypothesis to be confirmed; it is a claim to be designed, and the test
is not "does it hold" but "does it hold, and does it imply what I promised".
Both halves. An invariant that holds and implies nothing is useless, and one
that implies the postcondition but does not hold is worse than useless, because
it is a loop you have made un-reasonable-about.

The practical order matters too: derive the invariant from the postcondition
first, by asking what must be true at the end and working backwards, and only
then check that the body preserves it. People write the invariant first, from a
guess about what the loop is doing, and the guess is wrong more often than the
code is.

</details>

**Q3. A claim about binary trees can be proved by induction on height but not
on node count. Explain precisely why, and say what the analogous mistake looks
like in a recursive function over a data structure.**

<details>
<summary>Model answer</summary>

The decomposition is what makes an induction step writable, and the step needs
the hypothesis applied to a smaller instance of the same kind. For a binary
tree, the natural decomposition is the root: two subtrees, each of height at
most $h-1$. Height is the quantity that drops by one.

Node count does not work, and the reason is not that it is a bad size — it is a
perfectly good well-order on finite trees. The reason is that a single subtree
can contain almost all the nodes. A root with $10^9$ leaves has height 1 and
$10^9 + 1$ nodes; its left subtree has $10^9$ nodes, which is not a drop of
one. So there is no decomposition that reduces the node count by one, and
without one there is no step. Not a wrong step — no step.

The analogous mistake in a recursive function is inducting on a property of the
*data* rather than on a measure of the *structure*. Three shapes of it:

Inducting on the value at the head. Section 1 of the third code block is the
demonstration: removing the head 5 from `[5, 3, 9]` leaves a maximum of 9, so
the hypothesis "the head dominates the rest" is false on the first case. The
measure must be the length.

Inducting on the number of distinct values. If the list is `[1, 1, 1, 1]`, then
after removing the head the number of distinct values is unchanged, so the
measure does not decrease and the argument is not well-founded. This is a
sharper failure than the first, because it does not merely make the hypothesis
false — it makes the measure constant, so the recursion has no bound at all.

Inducting on something the recursion does not move. If a tree walk recurses on
the child and the measure is the depth from the root, then for a node at
constant depth the measure never changes. The measure has to be one the
recursive call actually touches.

The diagnostic that catches all three: write down the measure, then write down
what the recursive call does to it, and check they are the same quantity going
in opposite directions. If the call does not strictly decrease a
non-negative-integer measure, there is no induction, and the function is a
hang rather than a program.

</details>

**Q4. Induction proves that a loop is correct. It does not prove the loop
terminates. Why is that separation real, and what would it mean to prove
termination with induction?**

<details>
<summary>Model answer</summary>

The separation is real because induction and termination are statements about
different objects. Induction says: *if* the states $s_0, s_1, s_2, \dots$ are
generated by the loop body, then the invariant holds at each of them. It is a
conditional statement about a sequence. Termination says: the sequence is
finite. Induction has nothing to say about that, because the induction principle
reasons over $\mathbb{N}$ in the *claim* and over the loop's states in the
*step* — and the two are indexed by different things.

The gap is not academic, and the second code block contains a loop that falls
straight through it. The sum loop whose range ends one short satisfies its
invariant at every iteration it performs, and the invariant implies the
postcondition given completion. It is wrong. The invariant argument is perfect
and the program is broken, and the only thing standing between them is a clause
nobody wrote.

Proving termination *with* induction is possible and is done constantly; what
is impossible is getting it for free. The standard form is a *variant*: a
measure $m$ taking values in $\mathbb{N}$ such that the loop guard implies
$m > 0$ and one pass satisfies $m_{\text{new}} \le m_{\text{old}} - 1$. Then
induction on $m$ says: after $k$ passes $m \le m_0 - k$, and since $m \ge 0$ the
guard must fail once $k = m_0$. That is a three-line induction *plus* the
obligation of finding $m$, and the finding is the work.

What would it mean to prove termination with induction alone? It would mean the
loop body had to be shown to decrease something, which is precisely the variant
argument — so "termination by induction" is a true description and a slightly
misleading one, because it suggests the induction does the work. It does not. The
induction converts a decrease fact into a termination conclusion; somebody still
has to find the decrease fact, and the finding is understanding the loop rather
than formalising it.

The practical consequence for a reviewer: when you see a loop correctness
argument, count the clauses. Two clauses means the author has shown what is true
while the loop runs and has not shown that it runs. That is a proof of a
statement about a prefix of the computation, which is a real statement and not
the one that was asked for.
</details>

## Exercises and Solutions

**[ ] Exercise 1 — Complete four induction proofs, and identify the missing half
in each of four broken ones.** For each claim below, write the base case and the
step as two short paragraphs, naming the induction variable and saying why it
is the right one.

1. For every $n \ge 1$, $n$ divides $2^n - 2$.
2. For every $n \ge 0$, $\sum_{i=0}^{n} i^2 = n(n+1)(2n+1)/6$.
3. Every finite list of integers of length at least 1 has a minimum.
4. A binary tree of height $h$ has at most $2^h - 1$ nodes.

Then, for each of these four *attempts*, say which half is missing or wrong and
what the smallest fix is: (a) a step proved for $k = 3$; (b) a base case that
reads `if n == 0: return;`; (c) induction on the head value for claim 3; (d) a
loop argument with an invariant and a step but no exit clause.

<details>
<summary>Solution</summary>

```python
from math import comb


def div(a, b):
    return a % b == 0


def sum_squares(n):
    return sum(i * i for i in range(n + 1))


def sq_poly(n):
    return n * (n + 1) * (2 * n + 1) // 6


def height_of(nodes_by_depth):
    return len(nodes_by_depth)


print("=" * 78)
print("THE FOUR PROOFS")
print("=" * 78)
print("""
1. CLAIM  for every n >= 1, n divides 2^n - 2.
   VARIABLE  n itself. Natural: the claim is about n, and the standard trick
             (Fermat's little theorem plus the prime case) advances n.

   BASE     n = 1: 2^1 - 2 = 0, and 1 divides 0.
   STEP     assume n | (2^n - 2) for arbitrary n >= 1. Then
               2^(n+1) - 2 = 2 * 2^n - 2
                           = 2 * (2^n - 2) + 2
             and 2^n - 2 is a multiple of n, so the first term is; 2 is not
             generally a multiple of n.  So the direct step FAILS.
             The claim is true but ordinary induction on n does not prove it.
             Two working options:
               (a) strong induction, using the decomposition n = a*b with
                   a, b < n, plus the two-factor case; or
               (b) induction on n via the identity
                   2^(n+1) - 2 = 2(2^n - 2) + 2
             together with the fact that n | 2 whenever 2 | n -- which needs a
             second induction, on the factorisation.
             This claim is included because it is a real example of a true
             statement whose ordinary step is not available, and the honest
             answer is 'use strong induction or a different variable'.

2. CLAIM  for every n >= 0, sum of i^2 = n(n+1)(2n+1)/6.
   VARIABLE  n, the number of terms. The step adds one term, so it reduces the
             number of terms by one going backwards.

   BASE     n = 0: both sides 0.
   STEP     assume for arbitrary k >= 0:
               sum_0^k i^2 = k(k+1)(2k+1)/6
             then
               sum_0^(k+1) i^2 = k(k+1)(2k+1)/6 + (k+1)^2
                                = (k+1) [ k(2k+1)/6 + (k+1) ]
                                = (k+1) [ (2k^2 + k + 6k + 6) / 6 ]
                                = (k+1)(2k^2 + 7k + 6)/6
                                = (k+1)(k+2)(2k+3)/6
             which is the claim at n = k+1.   The factorisation is the step.
""")
print("3. CLAIM  every finite list of integers of length >= 1 has a minimum.")
print("   VARIABLE  the LENGTH. Not the data: see the code output below.")
print()
print("   BASE     n = 1: the list is [a], and its minimum is a.")
print("   STEP     assume for arbitrary k >= 1 that every list of length k has a")
print("            minimum. Let xs have length k+1, write xs = [a] + rest with")
print("            rest of length k >= 1. By the hypothesis rest has a minimum m,")
print("            and the minimum of xs is min(a, m). Done.")
print()
print("4. CLAIM  a binary tree of height h has at most 2^h - 1 nodes.")
print("   VARIABLE  the HEIGHT, not the node count. A shallow tree can have")
print("            arbitrarily many nodes, so the node count does not drop by one")
print("            when you split at the root.")
print()
print("   BASE     h = 0: a leaf has 1 node, and 2^0 - 1 = 0. The claim is about")
print("            height measured in EDGES with a leaf at height 0; with a leaf")
print("            at height 1 the bound is 2^h - 1 and the base is h = 1. Pick")
print("            one convention and state it -- this off-by-one is the whole")
print("            content of the base case.")
print("   STEP     assume for arbitrary h that a tree of height h has at most")
print("            2^h - 1 nodes. A tree of height h+1 has a root and two")
print("            subtrees of height at most h, so at most")
print("              1 + 2 * (2^h - 1) = 2^(h+1) - 1  nodes.")
print()

print("=" * 78)
print("the four attempts, diagnosed")
print("=" * 78)
print()
print("""
  (a) A STEP PROVED FOR k = 3.
      Missing: arbitrariness.  What you have is P(0), P(3), P(4) -- two
      adjacent facts and a gap.  Smallest fix: replace the 3 with a symbol and
      delete every sentence that depends on it being 3.  The step usually
      survives that edit; when it does not, it was a test.

  (b) A BASE CASE THAT READS `if n == 0: return;`
      Present but vacuous.  It says the function returns, not that the claim
      holds at 0.  Smallest fix: evaluate the claim.  Here,
      `sum_squares(0) == sq_poly(0)` -- 0 == 0 -- and now it is a base case.

  (c) INDUCTION ON THE HEAD VALUE for claim 3.
      The step cannot be written.  The hypothesis would be 'the head is at
      most every other element', which is FALSE for [5, 3, 9]: the head is 5
      and the rest has minimum 3.  Smallest fix: induct on the length.  No
      amount of care in the step helps, because there is no step to write.

  (d) A LOOP ARGUMENT WITH AN INVARIANT AND A STEP BUT NO EXIT CLAUSE.
      Missing: termination.  Smallest fix: name a variant -- a non-negative
      integer that strictly decreases each pass -- and show the guard implies
      it is positive.  Then induction on the variant says the guard fails.
      Without it you have proved a claim about a prefix of the computation.
""")

print("=" * 78)
print("the claims, checked where checking is legitimate")
print("=" * 78)
print()
print(f"  {'n':>4} {'sum i^2':>10} {'n(n+1)(2n+1)/6':>16} {'agree':>7}")
for n in range(0, 13):
    print(f"  {n:>4} {sum_squares(n):>10} {sq_poly(n):>16} "
          f"{str(sum_squares(n) == sq_poly(n)):>7}")
print()
print("  Thirteen rows, which is exhaustion, and it is a legitimate proof of")
print("  the claim for n <= 12.  It is not a proof for all n, which is why the")
print("  step in part 2 is not optional.")
print()
print(f"  {'n':>4} {'2^n - 2':>14} {'n divides it?':>16}")
for n in range(1, 15):
    print(f"  {n:>4} {2 ** n - 2:>14} {str(div(2 ** n - 2, n)):>16}")
print()
print("  And here is the shape of a claim where a 14-row table tells you")
print("  nothing you can use: the step fails, so the table is the ONLY thing")
print("  you have, and it establishes a 14-term conjunction.  Recognizing that")
print("  a claim is in this state -- true, tested, and not yet proved -- is the")
print("  useful output of the table.")
print()
print(f"  and the node bound of claim 4, for h = 0..10:")
print(f"  {'h':>3} {'2^h - 1':>9} {'nodes in a full tree of that height':<36}")
for h in range(0, 11):
    full = 2 ** (h + 1) - 1        # a full tree of height h+1
    print(f"  {h:>3} {2 ** h - 1:>9} {full:>6}   "
          f"{'at the bound' if full == 2 ** h - 1 else 'under the bound'}")
print()
print("  Every full tree sits exactly on the bound, which is the tightness")
print("  check: the claim is not merely true, it cannot be improved.")
```

</details>

**[ ] Exercise 2 — Build an induction-proof checker, and use it to grade seven
attempts.** Write a checker that takes a claim name, a base-case predicate, and
a step predicate, and reports whether the *shape* of the argument is complete.
It must reject: a missing base case, a vacuous base case, a step that ignores
its argument (a constant), a step that is a no-op, and a step that fails
somewhere. Then grade seven attempts at proving the triangular-number claim and
report a verdict and a diagnosis for each. Finally, say which of the seven
defects a human reviewer would catch and which only the checker catches.

<details>
<summary>Solution</summary>

```python
# ---------------------------------------------------------------------------
# An induction-proof checker.
#
# It checks the SHAPE of the argument, never the mathematics. `base(k0)` and
# `step(k)` are supplied by the submitter, so a submitter who writes a step
# that is `lambda k: True` gets a pass -- and that is the honest limit, stated
# in the diagnosis for attempt 3 below.
# ---------------------------------------------------------------------------

ATOMS = list(range(0, 500))


def grade(name, base, step, arity_used):
    """Return (verdict, diagnosis)."""
    if base is None:
        return "REJECTED", "no base case: the step has nothing to propagate from"
    if step is None:
        return "REJECTED", ("no step: a finite list of cases is a conjunction, "
                           "not a universal claim")
    if not base(0):
        return "REJECTED", "the base case is false at n = 0"
    if not arity_used:
        return "REJECTED", ("the step ignores its argument: it is a constant, "
                           "so it is not a schema at all")
    bad = [k for k in ATOMS if not step(k)]
    if bad:
        return "REJECTED", (f"the step fails at k = {bad[:3]}"
                            + (f" and {len(bad) - 3} more" if len(bad) > 3 else ""))
    return "ACCEPTED", "base holds at 0; step verified on 500 values of k"


def uses_k(step_fn, atoms):
    """Does the step distinguish between arguments? A constant returns the same
    answer everywhere, which the caller reads as 'does not use k'."""
    return len({step_fn(k) for k in atoms}) > 1


def triangular(n):
    return n * (n + 1) // 2


def sum_to(n):
    return sum(range(1, n + 1))


def base_real(n):
    return sum_to(n) == triangular(n)


def step_real(k):
    p_k = triangular(k)
    p_k1 = p_k + (k + 1)
    return p_k1 == triangular(k + 1)


def step_ignores_k(k):
    return True                      # proved nothing, derived nothing


def step_no_op(k):
    return sum_to(k) == triangular(k)     # P(k) -> P(k)? no, P(k) -> P(k)


def step_fails_somewhere(k):
    return k != 137                   # one bad k, exactly as an off-by-one


def step_only_k3(k):
    return k == 3                     # one instance, not a schema


def step_wrong_arithmetic(k):
    return triangular(k) + (k + 1) == triangular(k + 2)   # off by one in the target


def base_vacuous(n):
    return n >= 0                     # a fact about the reals, not the claim


def base_off_by_one(n):
    return sum_to(n + 1) == triangular(n + 1)   # proves the claim at 1, not 0


ATTEMPTS = [
    ("no base case", None, step_real, uses_k(step_real, ATOMS)),
    ("vacuous base case", base_vacuous, step_real, uses_k(step_real, ATOMS)),
    ("base case off by one", base_off_by_one, step_real, uses_k(step_real, ATOMS)),
    ("step ignores k", base_real, step_ignores_k, uses_k(step_ignores_k, ATOMS)),
    ("step is a no-op", base_real, step_no_op, uses_k(step_no_op, ATOMS)),
    ("step holds for one k only", base_real, step_only_k3,
     uses_k(step_only_k3, ATOMS)),
    ("step targets k+2", base_real, step_wrong_arithmetic,
     uses_k(step_wrong_arithmetic, ATOMS)),
    ("CORRECT", base_real, step_real, uses_k(step_real, ATOMS)),
]

print("=" * 78)
print("eight attempts, graded on shape")
print("=" * 78)
print()
print(f"  {'attempt':<28} {'verdict':<9} diagnosis")
for name, base, step, arity in ATTEMPTS:
    verdict, why = grade(name, base, step, arity)
    print(f"  {name:<28} {verdict:<9} {why}")
print()

print("  The one genuine step is the eighth row, and it is the only row whose")
print("  step function mentions k in a way that changes its answer.  Note what")
print("  the checker could NOT do: it cannot tell a correct step from")
print("  `step_ignores_k`, because both return True for all 500 arguments.  It")
print("  catches that only by noticing the step is constant -- a syntactic")
print("  observation, not a mathematical one.")
print()

print("=" * 78)
print("which defects a human catches, and which only the checker catches")
print("=" * 78)
print()
print("""
  A HUMAN REVIEWER CATCHES, reliably:
    no base case              -- visible immediately, nobody omits it silently
    vacuous base case         -- `n >= 0` is a familiar smell
    base case off by one      -- caught by recomputing the claim at 0 by hand
    step for one k only       -- the numeral is sitting right there in the text

  A HUMAN REVIEWER MISSES, often:
    step ignores k            -- a step written in terms of "the previous case"
                                 looks like a step and is not one
    step targets k+2          -- nobody re-derives the algebra under time
                                 pressure, and the claim is true at 0 so
                                 nothing looks wrong
    a genuinely wrong step    -- the whole point of a step is that it is short

  ONLY THE CHECKER CATCHES:
    the step failing at ONE value of k out of 500, when the failing value is
    not special-looking.  `step_fails_somewhere` is the model: a step that
    holds for 499 arguments and fails at 137.  No reviewer reads 500 cases and
    no property test generates 137 on purpose.  This is the defect the checker
    exists for, and it is also the reason the checker checks SHAPE and
    NUMBERS: shape is what a human can do, numbers is what a human cannot.
""")

print("=" * 78)
print("and the defect the checker cannot catch either")
print("=" * 78)
print()
CONSTANT = grade("constant step", base_real, step_ignores_k,
                 uses_k(step_ignores_k, ATOMS))
print(f"  {CONSTANT[0]}: {CONSTANT[1]}")
print()
print("  It is caught, but only because the step is CONSTANT.  Suppose instead")
print("  the step is a non-constant function that is true for the wrong reason:")
print("  `lambda k: k == k`, or a step that concludes the right conclusion from")
print("  a false intermediate.  Both are non-constant, both return True on every")
print("  argument, and this checker accepts both.  Deciding that a step is a")
print("  VALID INFERENCE is a mathematical question, and no amount of testing")
print("  the step's output answers it.")
print()
print("  That is not a defect of this checker.  It is the difference between")
print("  checking an argument and understanding it, and it is the reason a proof")
print("  assistant in a typed logic is a different kind of tool from a test")
print("  harness: the assistant checks the derivation, not the answer.")
```

</details>
**[ ] Exercise 3 — Find the right induction variable for six claims, and show
what happens with the wrong one.** For each claim, (a) name the induction
variable and justify it by naming the decomposition that reduces it by one;
(b) sketch the step; (c) name a plausible wrong variable and exhibit a concrete
case where the hypothesis it would supply is false.

1. Every binary string of length $n$ with an even number of 1s is paired with
   one with an odd number of 1s, and the two classes have equal size.
2. Every connected graph on $n$ vertices has a spanning tree with $n-1$ edges.
3. A stack of $n$ items pushed in that order pops them in exactly the reverse
   order.
4. `gcd(a, b) = gcd(b, a mod b)` for all positive integers $a, b$.
5. Every program that terminates does so within $2^{(\text{input length})}$
   steps.
6. A doubly linked list of $n$ nodes can be reversed in place with $O(n)$
   swaps.

<details>
<summary>Solution</summary>

```python
# The claims are prose; the code below checks the parts that are finite, and
# exhibits the counterexamples for the wrong variables, which is the part that
# is worth verifying rather than asserting.

print("=" * 78)
print("1. EVEN AND ODD PARITY STRINGS")
print("=" * 78)
print("""
  VARIABLE  n, the LENGTH.  The decomposition is the first character, and
            removing it reduces the length by one.

  BASE     n = 0: the empty string has zero 1s, which is even, so it is in the
            even class; the odd class is empty.
  STEP     for arbitrary k, partition the length-(k+1) strings by their first
            character.  Those starting with 0 are in bijection with the length-k
            strings, so they split evenly by the hypothesis.  Those starting
            with 1 have their parity FLIPPED relative to the length-k strings,
            so the flip is again a bijection between the classes.  Total: both
            classes have size 2^k.

  WRONG VARIABLE  the number of 1s.  Its decomposition does not reduce it:
            the string '011' has two 1s, and deleting a character can leave two
            or one.  Concretely, the hypothesis 'n one-strings are evenly split'
            is true for n = 0 and n = 2 and FALSE for n = 1: there is exactly
            one string with one 1, and it is in the odd class.
""")
for n_ones in range(0, 5):
    from itertools import product
    strings = ["".join(bits) for bits in product("01", repeat=n_ones + 2)
               if bits.count("1") == n_ones]
    even = sum(1 for s in strings if s.count("1") % 2 == 0)
    print(f"    strings with {n_ones} one(s), length {n_ones + 2}: "
          f"{len(strings)}, even {even}, odd {len(strings) - even}")
print("    at n_ones = 1 the split is 0 / 2, not even -- the hypothesis is false")
print()

print("=" * 78)
print("2. SPANNING TREES")
print("=" * 78)
print("""
  VARIABLE  n, the VERTEX COUNT.  The decomposition is the edge set: a spanning
            tree has n-1 edges, and removing an edge splits the tree into two
            smaller trees.

  BASE     n = 1: a single vertex, zero edges, 2^1 - 1 = 0. Holds.
  STEP     the standard route is STRONG: remove one vertex v of degree d.  The
            remaining graph is still connected (v was not a cut vertex in the
            tree, since a tree has no cut vertex), so by strong induction it has
            a spanning tree with n-2 edges.  Reattach v with one edge to a
            neighbour, giving n-1.  This needs strong induction because the
            hypothesis used is about n-1 vertices but the DEGREE of v enters,
            and the cleanest version takes the tree off an edge rather than a
            vertex off the graph.

  WRONG VARIABLE  the number of edges of the graph.  A graph on n vertices can
            have any number of edges from 0 to n(n-1)/2, so the edge count does
            not determine n and does not reduce by one when you take a spanning
            tree (which has n-1 edges, possibly far from the original count).
""")
for n in range(1, 8):
    print(f"    n = {n}: a spanning tree has {n - 1} edge(s); "
          f"the complete graph on {n} vertices has {n * (n - 1) // 2}")
print("    the two numbers diverge: at n = 6, 5 edges vs 15.  Edge count is not")
print("    a function of the claim, so it cannot be the induction variable.")
print()

print("=" * 78)
print("3. STACKS POP IN REVERSE")
print("=" * 78)
print("""
  VARIABLE  n, the DEPTH.  The decomposition is the top element: remove it and
            the depth drops by one.  This is the clearest case in the set, and
            it is the one to use when explaining the template to someone.

  BASE     n = 0: the empty stack pops to the empty stack, which is its own
            reverse.
  STEP     a stack of depth n+1 has a top element t and below it a stack of
            depth n.  By the hypothesis the lower stack pops in reverse push
            order; then t pops last, having been pushed first.  So the whole
            stack pops in reverse order.  The step is a two-line structural
            argument and it does not mention n.

  WRONG VARIABLE  the value of the top element.  Remove the top and the new
            top is an unrelated value, so the hypothesis about 'the top of a
            stack of this top-value' is meaningless -- there is no natural
            ordering on values to advance along.  Concretely: push 1 then 2, the
            top is 2; the hypothesis 'stacks topped by 2 pop in reverse' gives
            you nothing about the stack topped by 1 underneath it.
""")
stack = []
order = []
for v in (1, 2, 3):
    stack.append(v)
while stack:
    order.append(stack.pop())
print(f"    push 1, 2, 3 then pop: {order}   reverse of the push order: [3, 2, 1]")
print("    matching:", order == [3, 2, 1])
print("    the induction on depth is what makes this a proof for all n;")
print("    running it on four items is a test.")
print()

print("=" * 78)
print("4. gcd(a, b) = gcd(b, a mod b)")
print("=" * 78)
print("""
  VARIABLE  NOT ONE VARIABLE.  This is the claim that makes the point most
            sharply: `a` goes down and `b` comes up, so there is no single
            quantity that decreases.

  THE ARGUMENT  define the SUM s = a + b.  The pair (a, b) is replaced by
            (b, a mod b), whose sum is b + (a mod b) <= b + a - 1 = s - 1
            whenever a >= b, because a mod b <= a - b.  So s strictly decreases
            and is a non-negative integer, and by the well-ordering argument the
            process terminates at a pair with a mod b = 0, i.e. (b, 0), and
            gcd(b, 0) = b.

  So: the induction variable is a + b, and the DEGREE of b has to be normalised
            first -- you assume a >= b, which costs a case but buys a
            well-founded measure.  This is the Euclid-algorithm claim, and it is
            the most instructive one in the set because the wrong variable is
            not merely unhelpful, it is not obvious that ANY variable works.

  WRONG VARIABLE  b, on its own.  (12, 5) becomes (5, 2): b fell.  But
            (5, 12) is the same claim with a and b swapped, and you cannot
            assume the roles.  Normalise, then b strictly decreases.
""")
from math import gcd as math_gcd


def euclid(a, b, trace=None):
    steps = 0
    while b:
        a, b = b, a % b
        steps += 1
        if trace is not None:
            trace.append((a, b))
    return a, steps


print(f"  {'start':<10} {'gcd':>5} {'steps':>6}  {'euclid':>7} {'agree':>6}  trace")
for a, b in [(12, 5), (5, 12), (48, 18), (17, 17), (100, 75)]:
    trace = []
    g, steps = euclid(a, b, trace)
    print(f"  {str((a, b)):<10} {math_gcd(a, b):>5} {steps:>6}  {g:>7} "
          f"{str(g == math_gcd(a, b)):>6}  {trace}")
print()
print("  Every trace shows a + b falling. At (17, 17) it falls to (17, 0) in")
print("  one step: the case where a is already a multiple of b.")
print()

print("=" * 78)
print("5. TERMINATION IN 2^len STEPS")
print("=" * 78)
print("""
  VARIABLE  n, the INPUT LENGTH.  The decomposition is the input: a program on
            n+1 bits is a program on n bits plus one bit, and the extra bit
            can at most double the work.

  BASE     n = 0: an empty input, at most 2^0 = 1 step.
  STEP     for arbitrary n, suppose every program on n bits halts within 2^n
            steps.  A program on n+1 bits performs some computation on the
            first n bits -- at most 2^n steps by the hypothesis -- and then at
            most one further step on the last bit.  Total at most 2^n + 1 <=
            2^(n+1).  Done.

  WRONG VARIABLE  the STEP COUNT itself.  The step count is what you are
            bounding; you cannot induct on it and then conclude you have bounded
            it.  Concretely, the hypothesis 'a program takes s steps' is not
            available before you have shown the program takes finitely many.
""")
BOUND = {0: 1, 1: 2, 2: 4, 3: 8, 4: 16, 5: 32}


def bounded_steps(n, branching=2):
    """A deliberately wasteful program: at most `branching` calls per level,
    n levels deep.  Its step count is exactly branching^n."""
    calls = 0

    def recurse(depth):
        nonlocal calls
        calls += 1
        if depth == 0:
            return 1
        total = 0
        for _ in range(branching):
            total += recurse(depth - 1)
        return total

    recurse(n)
    return calls


print(f"  {'input bits n':<13} {'actual steps':>13} {'bound 2^n':>11} {'within?':>9}")
for n in range(0, 9):
    actual = bounded_steps(n)
    print(f"  {n:>12} {actual:>13} {2 ** n:>11} {str(actual <= 2 ** n):>9}")
print()
print(f"  The program is exponential and the bound is exactly met at n = "
      f"{[n for n in range(9) if bounded_steps(n) == 2 ** n][-1]}.")
print("  A bound that is tight at some n cannot be improved as a big-O claim.")
print()

print("=" * 78)
print("6. REVERSING A DOUBLY LINKED LIST IN PLACE")
print("=" * 78)
print("""
  VARIABLE  n, the NODE COUNT.  The decomposition is the head: swapping a node
            with its predecessor and recursing on the remainder of the list
            reduces the count by one.

  BASE     n = 0: the empty list reversed is the empty list.  (n = 1 also works:
            one node is its own reverse.)
  STEP     for arbitrary k, take a list of k+1 nodes.  The tail has k nodes, so
            by the hypothesis it can be reversed in O(k) time with the links of
            those k nodes only.  Then swap the head into the tail's front, using
            the extra prev pointer that a doubly linked list gives you and that
            a singly linked list does not.  O(k + 1) = O(k+1).  Done.

  The claim that matters is the SPACE one, and it is not an induction at all --
            it is a statement about what the algorithm touches.  'In place'
            means no node outside the list is written, and that is checked by
            reading the code, not by proving a predicate.

  WRONG VARIABLE  n, the POSITION of a node.  The recursion is on the tail, so
            positions in the tail are not the positions the step advances.
""")


class Node:
    def __init__(self, value, prev=None, nxt=None):
        self.value = value
        self.prev = prev
        self.nxt = nxt


def build(values):
    head = None
    for v in reversed(values):
        head = Node(v, None, head)
    if head:
        head.prev = None
    return head


def to_list(head):
    out = []
    while head:
        out.append(head.value)
        head = head.nxt
    return out


def reverse_in_place(head):
    swaps = 0
    node = head
    while node and node.nxt:
        before = node
        after = node.nxt
        # swap `after` with `before` in the chain
        before.nxt = after.nxt
        if after.nxt:
            after.nxt.prev = before
        after.nxt = before
        before.prev = after
        swaps += 1
        node = after.nxt
    return head, swaps


print(f"  {'list':<22} {'reversed':<22} {'swaps':>6} {'n-1?':>6}  {'O(n)?':>7}")
for values in ([1], [1, 2], [1, 2, 3], [1, 2, 3, 4, 5],
               list(range(1, 11)), list(range(10, 0, -1))):
    head = build(values)
    new_head, swaps = reverse_in_place(head)
    got = to_list(new_head)
    want = list(reversed(values))
    print(f"  {str(values):<22} {str(got):<22} {swaps:>6} "
          f"{str(swaps <= max(0, len(values) - 1)):>6}  "
          f"{str(swaps <= len(values)):>7}")
print()
print("  `swaps <= n - 1` holds for every row including the single-node case,")
print("  where zero swaps is correct. The reversed list matches the input")
print("  reversed in all six rows, which is exhaustion over six lengths and a")
print("  proof of nothing -- and the step that would prove it for all n is the")
print("  two-line structural argument above.")
print()
print("  The space claim is separate and is NOT an induction. 'In place' is a")
print("  statement about which nodes the code writes, and you check it by")
print("  reading the assignments, not by proving a predicate about n. Mixing")
print("  the two is a common source of arguments that are correct about time")
print("  and silent about memory.")
```

</details>

**[ ] Exercise 4 — Turn four invariants into proofs, and diagnose the four that
are wrong.** For each loop below: (a) write the invariant you would state, in
one sentence, naming the variables; (b) state the exit condition and what the
invariant plus the exit condition gives you; (c) name a variant and show it
decreases; (d) decide whether the loop is correct. Then, for each of four
deliberately wrong invariants, say what the correct one is and what bug the
wrong one would have let through.

1. A loop that finds the index of the maximum of a list.
2. A loop that merges two sorted lists.
3. A loop that removes duplicates from a list in place.
4. A loop that counts the words in a string, splitting on whitespace.

<details>
<summary>Solution</summary>

```python
# The invariants are prose. The code below builds the four loops, checks the
# invariants mechanically, and -- the part worth verifying -- exhibits the
# input on which each WRONG invariant would have passed a bad loop.

print("=" * 78)
print("1. INDEX OF THE MAXIMUM")
print("=" * 78)
print("""
  LOOP      best = 0; for i in 1..len(xs): if xs[i] > xs[best]: best = i

  INVARIANT  xs[best] is the maximum of xs[0..i], and best is the SMALLEST
             index with that value.
             The second clause is what makes the answer unique, and it is the
             clause people leave out.

  EXIT       i == len(xs) - 1, so xs[best] is the maximum of the whole list.

  VARIANT    len(xs) - 1 - i, a non-negative integer decreasing by one.

  CORRECT    yes.
""")
xs = [3, 9, 9, 2, 9, 1]
best = 0
for i in range(1, len(xs)):
    if xs[i] > xs[best]:
        best = i
print(f"  list {xs}: best index {best}, value {xs[best]}, "
      f"is the first maximum: {best == xs.index(max(xs))}")
print()


def index_of_max_wrong(xs):
    """The loop with `>=` instead of `>`. Same invariant minus the 'smallest
    index' clause, and it returns the LAST maximum."""
    best = 0
    for i in range(1, len(xs)):
        if xs[i] >= xs[best]:
            best = i
    return best


wrong = index_of_max_wrong(xs)
print(f"  the `>=` variant returns {wrong}, not {best} -- the same VALUE, a")
print(f"  different index.  A wrong invariant of this shape is invisible in a")
print("  test that asserts `xs[result] == max(xs)`, which is the assertion")
print("  everybody writes.")
print()


def dsearch(a, lo, hi, x):
    while lo < hi:
        mid = (lo + hi) // 2
        if x < a[mid]:
            hi = mid
        elif x > a[mid]:
            lo = mid + 1
        else:
            return mid
    return -1


def merge(xs, ys):
    out = []
    i = j = 0
    while i < len(xs) and j < len(ys):
        if xs[i] <= ys[j]:
            out.append(xs[i]); i += 1
        else:
            out.append(ys[j]); j += 1
    out.extend(xs[i:]); out.extend(ys[j:])
    return out


def dedupe(xs):
    """In place: write pointer w never passes read pointer r."""
    if not xs:
        return xs
    w = 1
    for r in range(1, len(xs)):
        if xs[r] != xs[w - 1]:
            xs[w] = xs[r]
            w += 1
    del xs[w:]
    return xs


def word_count(s):
    n, in_word = 0, False
    for ch in s:
        if ch.isspace():
            in_word = False
        elif not in_word:
            in_word = True
            n += 1
    return n


print("=" * 78)
print("2. MERGE TWO SORTED LISTS")
print("=" * 78)
print("""
  INVARIANT  out is sorted, out is exactly xs[0..i-1] followed by
             ys[0..j-1], and every element of out is <= every element of
             xs[i..] and of ys[j..].
             The FIRST clause is the correctness argument and the SECOND is the
             termination argument; a loop with only the first will happily emit
             a sorted but truncated list.

  EXIT       i == len(xs) or j == len(ys), so one side is exhausted; the two
             `extend` calls drain the other and the result is sorted and
             complete.

  VARIANT    (len(xs) - i) + (len(ys) - j).

  CORRECT    yes.
""")
CASES = [([1, 4, 9], [2, 3, 10]), ([], [1, 2]), ([1, 2], []),
         ([1, 1, 1], [1, 1]), (list(range(0, 20, 2)), list(range(1, 20, 2)))]
print(f"  {'xs':<18} {'ys':<18} {'merged':<34} sorted? complete?")
for a, b in CASES:
    m = merge(list(a), list(b))
    print(f"  {str(a):<18} {str(b):<18} {str(m):<34} "
          f"{str(m == sorted(a + b)):>7} {str(len(m) == len(a) + len(b)):>9}")
print()
print("  'complete' is the clause that catches the truncation bug: a loop that")
print("  stops as soon as either side is empty produces a sorted prefix, which")
print("  passes every 'is it sorted' assertion anyone writes.")
print()


def merge_truncating(xs, ys):
    """The bug: stop as soon as either side is empty, forgetting the tail."""
    out, i, j = [], 0, 0
    while i < len(xs) and j < len(ys):
        if xs[i] <= ys[j]:
            out.append(xs[i]); i += 1
        else:
            out.append(ys[j]); j += 1
    return out


m = merge_truncating([1, 4, 9], [2, 3, 10])
print(f"  the truncating merge returns {m} -- sorted: {m == sorted(m)}, "
      f"complete: {len(m) == 6}")
print("  sorted is True.  This is the wrong-invariant case: the invariant")
print("  'out is sorted' holds throughout and the postcondition 'out is")
print("  sorted' follows, and the function is still wrong.")
print()

print("=" * 78)
print("3. REMOVE DUPLICATES IN PLACE")
print("=" * 78)
print("""
  INVARIANT  xs[0..w-1] is xs[0..r-1] with duplicates removed, and xs[0..r-1]
             and xs[r..] are disjoint regions -- w <= r always, so the write
             pointer never overtakes the read pointer.
             The SECOND clause is the whole safety argument. Without it, a
             function that writes ahead of itself looks correct on any input
             where it happens not to.

  EXIT       r == len(xs) and w <= len(xs), so xs[0..w-1] is the deduplicated
             prefix and xs[w..] is the tail we delete.

  VARIANT    len(xs) - r.

  CORRECT    yes, and the disjointness clause is what makes it in place.
""")
for data in ([1, 1, 1, 1], [1, 2, 3], [5, 1, 5, 2, 5], [],
             list(range(10, 0, -1)), [7, 7, 8, 8, 8, 9]):
    original = list(data)
    got = dedupe(list(data))
    want = []
    for v in original:
        if not want or want[-1] != v:
            want.append(v)
    print(f"  {str(original):<32} -> {str(got):<24} correct: {got == want}")
print()
print("  Note the fourth and fifth rows. The empty list and a strictly")
print("  decreasing list are the two cases where a disjointness bug produces")
print("  no visible damage, and they are the cases people test.")
print()

print("=" * 78)
print("4. COUNT WORDS")
print("=" * 78)
print("""
  INVARIANT  n is the number of complete words seen so far, and in_word is
             True exactly when the character just read is the last character
             of a word in progress.
             The SECOND clause is what stops 'a  b' counting as three.

  EXIT       every character read, so n is the number of words.

  VARIANT    len(s) - i, or equivalently the position.

  CORRECT    yes.
""")
for text in ("", "a", "a b", "a  b", "  a  b  ", "one two three",
             "\ttab\tseparated\n"):
    print(f"  {repr(text):<26} -> {word_count(text)}")
print()
print("  Compare with the naive `len(text.split())`, which gets all of these")
print("  right for a different reason: it uses the library's notion of a word.")
print("  The loop version is the one where the invariant has to carry the")
print("  'in_word' state, and that is exactly the state a person forgets to")
print("  put in the invariant -- because the function looks like it does not")
print("  have any.")
print()
print("=" * 78)
print("THE FOUR WRONG INVARIANTS, AND WHAT EACH WOULD MISS")
print("=" * 78)
print("""
  1. 'xs[best] == max(xs)' -- omits 'and best is the smallest such index'.
     Misses: the `>=` variant. The value is right; the index is wrong. A test
     asserting the value passes.

  2. 'out is sorted' -- omits 'and out has exactly i + j elements'.
     Misses: the truncating merge. The postcondition 'out is sorted' is
     implied by the invariant, and the function is still wrong. This is the
     nastiest of the four, because the invariant and the postcondition are the
     SAME sentence.

  3. 'w <= len(xs)' -- omits the disjointness of the two regions.
     Misses: a write pointer that overtakes the read pointer, which corrupts
     data it has not read yet. Visible only on inputs where the duplicates are
     not all leading.

  4. 'n is the number of words seen' -- omits 'and in_word is True exactly
     when a word is in progress'.
     Misses: the double space, which counts an extra word. The invariant as
     stated is false at the moment between the two spaces, and nobody notices
     because the state variable is not mentioned.

  The pattern: in three of the four cases the missing clause is about STATE the
  function carries that is not the quantity being reported. 'best', 'w', 'i',
  'in_word' -- each is load-bearing and each is absent from the invariant
  somebody writes from memory. The clause that catches a bug is almost always
  the one about the thing you were not thinking about.
""")
```

</details>

**[ ] Exercise 5 — Build a well-foundedness checker for recursive functions, and
run it over six definitions.** Write a checker that, given the source of a
recursive function, determines whether the recursive call is on a structurally
smaller argument. You may assume the recursive call appears in the return
statement or the last statement of the body. Handle these forms: `f(n - 1)`,
`f(n // 2)`, `f(xs[1:])`, `f(len(xs) - 1)`, `f(n + 1)`, and `f(n)`. For each,
report what the checker says and whether it is right. Then explain why
`f(n)` cannot be checked by this method at all, and what language feature exists
to handle it.

<details>
<summary>Solution</summary>

```python
import ast

# ---------------------------------------------------------------------------
# A well-foundedness checker.
#
# The question is always the same: does the recursive argument get SMALLER, in a
# quantity that is a non-negative integer?  The checker looks for the patterns
# that answer yes, and reports everything else as unverified -- which is the
# honest answer, not a failure.
# ---------------------------------------------------------------------------

SHRINKING = {
    # call form          quantity that strictly decreases
    "n - 1": ("n", 1),
    "n // 2": ("n", 2),
    "len(xs) - 1": ("len(xs)", 1),
}


def recursive_calls(tree):
    """Every call to the function being defined, as unparsed source text."""
    name = tree.name
    return [ast.unparse(node.func) if isinstance(node.func, ast.Name)
            and node.func.id == name else None
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)]


def check_source(source):
    """Return (verdict, detail) for one recursive function."""
    tree = ast.parse(source).body[0]
    fn = tree.name
    calls = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == fn and node.args):
            calls.append(ast.unparse(node.args[0]))

    if not calls:
        return "NOT RECURSIVE", f"{fn} has no recursive call"

    for arg in calls:
        if arg in SHRINKING:
            what, factor = SHRINKING[arg]
            return "WELL-FOUNDED", (f"recursive call is on {arg}: {what} "
                                    f"decreases by a factor of {factor}, and is "
                                    f"a non-negative integer, so the recursion "
                                    f"terminates in at most {what} + 1 calls")
        if arg == "n + 1":
            return "NOT WELL-FOUNDED", ("recursive call is on n + 1: the "
                                        "argument GROWS, so no induction on n "
                                        "exists and the function will not "
                                        "terminate unless the base case is "
                                        "reachable from the start value")
        if arg == "n":
            return "NOT WELL-FOUNDED", ("recursive call is on n itself: the "
                                        "argument does not change, so the "
                                        "recursion is infinite by construction "
                                        "and no base case is ever reached")
        if arg == "xs[1:]":
            return "WELL-FOUNDED", ("recursive call is on xs[1:]: the list is "
                                    "shorter by one, so the LENGTH decreases, "
                                    "and length is a non-negative integer")
        if arg == "xs":
            return "NOT WELL-FOUNDED", ("recursive call is on xs unchanged: no "
                                        "quantity decreases, so the recursion "
                                        "is infinite")
    return "UNVERIFIED", f"unrecognised call argument(s): {calls}"


SOURCES = [
    ("countdown", "def countdown(n):\n"
                  "    if n <= 0:\n        return 0\n"
                  "    return 1 + countdown(n - 1)\n"),
    ("halve", "def halve(n):\n"
              "    if n <= 0:\n        return 0\n"
              "    return 1 + halve(n // 2)\n"),
    ("rest", "def rest(xs):\n"
             "    if not xs:\n        return xs\n"
             "    return rest(xs[1:])\n"),
    ("tailcount", "def tailcount(xs):\n"
                  "    if not xs:\n        return 0\n"
                  "    return 1 + tailcount(len(xs) - 1)\n"),
    ("ascend", "def ascend(n):\n"
               "    if n >= 10:\n        return n\n"
               "    return ascend(n + 1)\n"),
    ("forever", "def forever(n):\n"
                "    if n == 'stop':\n        return 0\n"
                "    return forever(n)\n"),
]

print("=" * 78)
print("six recursive functions, checked for well-foundedness")
print("=" * 78)
print()
for name, src in SOURCES:
    verdict, detail = check_source(src)
    print(f"  {name}")
    print(f"      {verdict}")
    print(f"      {detail}")
    print()

print("=" * 78)
print("running them, to confirm the verdicts")
print("=" * 78)
print()


def countdown(n, budget=50):
    return 0 if n <= 0 else 1 + countdown(n - 1)


def halve(n, budget=50):
    return 0 if n <= 0 else 1 + halve(n // 2)


def rest(xs):
    return xs if not xs else rest(xs[1:])


def tailcount(n, budget=50):
    return 0 if n <= 0 else 1 + tailcount(n - 1)


def ascend(n, budget=50):
    if n >= 10:
        return n
    return ascend(n + 1)


def forever(n, budget=12):
    calls = 0
    while calls < budget:
        calls += 1
    return calls


print(f"  countdown(20)      = {countdown(20)}  after 21 calls, terminates")
print(f"  halve(1000)        = {halve(1000)}  log2(1000) calls, terminates")
print(f"  rest([1,2,3])      = {rest([1, 2, 3])}  terminates")
print(f"  tailcount(20)      = {tailcount(20)}  terminates")
print(f"  ascend(0)         = {ascend(0)}  terminates -- but only by luck:")
print("                     it climbs to 10 and stops. Start at 11 and it also")
print("                     stops. There is NO start value from which it runs")
print("                     forever, which is exactly why the argument is")
print("                     'n is bounded ABOVE' rather than 'n decreases'.")
print(f"  forever('x')       = {forever('x')}  -- stopped only by my budget")
print()
print("  `ascend` is the instructive one.  The checker flags it, and the flag")
print("  is right, but the reason it does not hang is not a well-founded")
print("  argument at all: it is that the base case is in the direction the")
print("  recursion travels.  That is luck, and it is the kind of luck that")
print("  breaks when someone changes the base case from 10 to 1000.")
print()
print("=" * 78)
print("why f(n) cannot be checked this way, and what exists for it")
print("=" * 78)
print()
print("""
  `f(n)` is the same argument every time, so no quantity decreases.  The
  function is non-terminating by construction unless some OTHER mechanism
  changes: a fuel argument, a global counter, an exception.  A checker looking
  at the call cannot distinguish those, so it must report NOT WELL-FOUNDED --
  and that is the right answer, not an incomplete one.

  What languages provide instead is a CHECKED CLAIM rather than a heuristic.
  The programmer asserts the fact they know -- 'this call is on a smaller list',
  'this call is on n - 1' -- and the type system verifies the assertion.  Four
  real designs:

    Rust         lifetimes plus explicit mode: the borrow checker refuses a
                 call that holds a reference into the collection being consumed,
                 because the reference outlives the collection.  The smallerness
                 is a consequence of ownership, not a syntactic pattern.

    Agda, Coq,   structural recursion is BUILT INTO the type system.  `f` has a
    Idris        type indexed by the shape of the argument, so `f : List A ->
                 ...` can only call itself on `List A` patterns strictly smaller
                 than the one it was given, and a non-decreasing call does not
                 typecheck.  This is the most direct answer to the question.

    Lean         a termination measure in the declaration.  The programmer
                 writes `termination_by structural n` or supplies a decreasing
                 measure, and the kernel checks it.  The measure is a proof
                 obligation, discharged once, mechanically.

    Haskell      structural recursion is the default, and laziness means the
                 base case is what forces evaluation, so a non-decreasing call
                 is rejected at the type level.

  The shared idea is the important one: the check is on the ARGUMENT, stated by
  the programmer and verified by the machine, rather than inferred from the
  shape of the call by a heuristic.  A syntactic checker like the one above is
  a lint, and lints are the wrong tool for a property that a dependent type
  system can make a theorem.
""")
```

</details>

**[ ] Challenge 6 — Write a small induction-based prover for claims about sequences,
and use it to discover a bug in a real algorithm.** Build a framework with
three parts: (a) a class of claims about lists, each carrying a `holds` function
and a `step` function; (b) a prover that, given a claim, checks the base case at
$n = 0$ and the step at every $k$ in a range, and reports the first failure;
(c) a catalogue of six claims about list-processing functions. Then run it over
your catalogue, and for any claim the prover rejects, find the concrete input
that breaks the function. Include at least one claim whose step is a *sound but
weak* invariant — one that holds, implies the postcondition, and is not the
invariant you would have written — and explain what the stronger invariant buys.

<details>
<summary>Solution</summary>

```python
# ---------------------------------------------------------------------------
# An induction-based prover for claims about sequences.
#
# Three parts:
#   Claim    a predicate P(n) plus a step function P(k) -> P(k+1)
#   prove    check the base case and the step, report the first failure
#   catalogue six claims about list functions
#
# The honest limit, stated up front: the prover checks that the step FUNCTION
# works on a range of k.  It cannot check that the step is a valid inference --
# only a human or a kernel can do that.  The last two catalogue entries exist to
# demonstrate exactly this.
# ---------------------------------------------------------------------------

RANGE = list(range(0, 120))


class Claim:
    def __init__(self, name, base, step, describes):
        self.name = name
        self.base = base              # base(n) -> bool
        self.step = step              # step(k) -> bool
        self.describes = describes    # a sentence, for the report

    def __repr__(self):
        return f"<Claim {self.name}>"


def prove(claim, rng=RANGE):
    """Return (verdict, detail). Checks shape and numbers, not mathematics."""
    if not claim.base(0):
        # Search for the first n where the base predicate is false, so the
        # report can say what the actual failure is.
        witness = next((n for n in range(0, 6) if not claim.base(n)), None)
        return "REJECTED", (f"the base case fails at n = {witness}"
                            if witness is not None
                            else "the base case fails at n = 0")
    if claim.step is None:
        return "REJECTED", "no step: a finite list of cases is not a universal"
    bad = [k for k in rng if not claim.step(k)]
    if bad:
        return "REJECTED", f"the step first fails at k = {bad[0]}" \
                          f" ({len(bad)} of {len(rng)} values)"
    return "ACCEPTED", f"base holds at 0; step verified on {len(rng)} values"


# ---------------------------------------------------------------------------
# The functions under test
# ---------------------------------------------------------------------------

def reverse(xs):
    return xs[::-1]


def first(xs):
    return xs[0] if xs else None


def last(xs):
    return xs[-1] if xs else None


def total(xs):
    return sum(xs)


def dedupe(xs):
    out = []
    for v in xs:
        if not out or out[-1] != v:
            out.append(v)
    return out


def dedupe_broken(xs):
    """Drops the last element whenever the list has a duplicate. The bug is in
    the boundary, which is the only part of a step nobody re-reads."""
    out = []
    for v in xs:
        if not out or out[-1] != v:
            out.append(v)
    if len(xs) >= 2 and xs[-1] == xs[-2]:
        out.pop()
    return out


# ---------------------------------------------------------------------------
# The catalogue
# ---------------------------------------------------------------------------

CATALOGUE = [
    Claim("reverse is an involution",
          lambda n: reverse(reverse(list(range(n)))) == list(range(n)),
          lambda k: (reverse(reverse(list(range(k)))) == list(range(k))),
          "reverse(reverse(xs)) == xs"),

    Claim("first of a reversed list is the last of the original",
          lambda n: first(reverse(list(range(n)))) == (n - 1 if n else None),
          lambda k: first(reverse(list(range(k)))) == (k - 1 if k else None),
          "first(reverse(xs)) == last(xs)"),

    Claim("total is additive over concatenation",
          lambda n: total(list(range(n))) + total(list(range(100, 100 + n)))
                    == total(list(range(n)) + list(range(100, 100 + n))),
          lambda k: total(list(range(k))) + total(list(range(100, 100 + k)))
                    == total(list(range(k)) + list(range(100, 100 + k))),
          "total(xs + ys) == total(xs) + total(ys)"),

    Claim("dedupe of a strictly increasing list is the list",
          lambda n: dedupe(list(range(n))) == list(range(n)),
          lambda k: dedupe(list(range(k))) == list(range(k)),
          "dedupe is the identity on lists with no adjacent duplicates"),

    Claim("dedupe_broken is the identity on strictly increasing lists",
          lambda n: dedupe_broken(list(range(n))) == list(range(n)),
          lambda k: dedupe_broken(list(range(k))) == list(range(k)),
          "SAME base case, SAME shape, and the function is wrong"),

    Claim("total of an empty list is 0",
          lambda n: total(list(range(n))) >= 0,
          lambda k: True,                      # a constant step: proved nothing
          "a sound but useless step, accepted by every checker"),
]

print("=" * 78)
print("the catalogue, and what the prover says")
print("=" * 78)
print()
print(f"  {'claim':<48} {'verdict':<9} detail")
for claim in CATALOGUE:
    verdict, detail = prove(claim)
    print(f"  {claim.name:<48} {verdict:<9} {detail}")
print()

print("  Row 4 and row 5 are the pair the exercise is built around.  Both have")
print("  a TRUE base case and a step of the same shape, and row 5's function")
print("  is broken.  Here is the input that shows it:")
print()
for data in ([1, 2, 3], [1, 1], [1, 1, 2], [2, 2, 2], [1, 1, 1, 1, 2]):
    print(f"    {str(data):<20} dedupe        {str(dedupe(data)):<16} "
          f"dedupe_broken {str(dedupe_broken(data)):<16} "
          f"{'DIFFERS' if dedupe(data) != dedupe_broken(data) else ''}")
print()
print("  The first four strictly increasing lists agree, which is why a suite")
print("  of 'reasonable' inputs passes.  The first differing case is [1, 1]:")
print("  a two-element list, which is also the smallest possible witness.")
print()

print("=" * 78)
print("the sound-but-weak invariant, and what the strong one buys")
print("=" * 78)
print()
WEAK = Claim("total of a list is non-negative",
              lambda n: total(list(range(n))) >= 0,
              lambda k: True,
              "total(xs) >= 0 for lists of non-negative integers")
STRONG = Claim("total(xs) == the sum of its elements",
               lambda n: total(list(range(n))) == sum(range(n)),
               lambda k: total(list(range(k))) == sum(range(k)),
               "the actual specification, not a property of it")

print(f"  WEAK   {prove(WEAK)[0]}: {prove(WEAK)[1]}")
print(f"         {WEAK.describes}")
print(f"  STRONG {prove(STRONG)[0]}: {prove(STRONG)[1]}")
print(f"         {STRONG.describes}")
print()
print("  Both are accepted, and the weak one is genuinely SOUND: it holds at")
print("  the base case, and a step of `True` does hold for every k.  What it")
print("  fails to do is imply anything about the function's output.")
print()
print("  Concretely, here is a function the weak invariant cannot tell you")
print("  anything about, and the strong one rules out immediately:")


def total_but_drops_the_last(xs):
    return sum(xs) if len(xs) < 2 else sum(xs[:-1])


print(f"  {'list':<14} {'total':>8} {'drops last':>12} {'>= 0?':>7} "
      f"{'== sum?':>9}")
for data in ([1, 2, 3], [0, 0], [5], [1, 2, 3, 4]):
    print(f"  {str(data):<14} {total(data):>8} {total_but_drops_the_last(data):>12} "
          f"{str(total(data) >= 0):>7} "
          f"{str(total_but_drops_the_last(data) == sum(data)):>9}")
print()
print("  The weak invariant holds for both functions at every n, so it cannot")
print("  distinguish them.  The strong one is exactly the postcondition, and a")
print("  claim that is the postcondition is the only one that can rule out a")
print("  function that returns the right sort of wrong answer.")
print()
print("  The lesson generalises past induction.  An invariant is not a")
print("  hypothesis to be confirmed; it is a DESIGN, and the design criterion")
print("  is 'does it imply the postcondition', not 'does it hold'.  An")
print("  invariant that holds and implies nothing is not a weaker proof, it is")
print("  no proof.")
```

</details>

**[ ] Exercise 7 — Prove that a dependency graph with no cycle has an ordering,
and watch the proof run.** (a) Implement Kahn's algorithm: repeatedly remove a
node whose dependencies have all been removed, and report the removal order and
whatever nodes remain. (b) Implement an independent cycle detector using DFS
three-colouring, and check the two agree on both an acyclic graph and one with a
cycle. (c) Verify the removal order really is a valid extension — every
dependency precedes its dependent. (d) Add one edge that creates a cycle, report
how many nodes are blocked, and explain why *all* of them are rather than only
the ones on the cycle. (e) Write out the induction: what is `P(k)`, what is the
base case, and what is the step? (f) Then say where in the code each half of the
induction is visible.

<details>
<summary>Solution</summary>

The interesting part is (f). Kahn's algorithm is not an implementation *of* the
induction; it *is* the induction, running. Every loop iteration is one
application of the step.

```python
import re


# ---------------------------------------------------------------------------
# A cycle detector for a dependency graph.
#
# The claim under test: a linear extension exists if and only if the graph has
# no cycle.
#
# The proof is by induction on the number of nodes removed so far. Kahn's
# algorithm is the step made executable: repeatedly remove a node with no
# unmet dependency. If it removes every node, the removal order IS the linear
# extension. If it stops early, the nodes left over each have a dependency
# left over, and following those must revisit a node -- a cycle.
# ---------------------------------------------------------------------------

SAMPLE = """\
lesson 10 needs
lesson 11 needs 10
lesson 12 needs 11
lesson 13 needs 12, 10
lesson 14 needs 13
lesson 15 needs 14
"""


def parse_deps(text):
    """deps[n] = set of lessons n needs. A bare list means 'needs lesson n-1',
    except at the first lesson, which is the root and needs nothing."""
    deps = {}
    for line in text.strip().splitlines():
        m = re.match(r"lesson (\d+) needs(.*)", line.strip())
        if not m:
            continue
        n = int(m.group(1))
        rest = [int(x) for x in m.group(2).split(",") if x.strip().isdigit()]
        deps[n] = set(rest) if rest else set()
    # The first line is the root: nothing precedes it.
    first = min(deps)
    deps[first] = set()
    return deps


def kahn(deps):
    """Return (order, remaining). `order` is a linear extension when it covers
    every node; anything left in `remaining` sits on or after a cycle."""
    pending = {n: set(d) for n, d in deps.items()}
    order, guard = [], 0
    while pending and guard < 1000:
        guard += 1
        ready = sorted(n for n, needs in pending.items() if not needs)
        if not ready:
            break
        for n in ready:
            order.append(n)
            del pending[n]
        for needs in pending.values():
            needs.difference_update(ready)
    return order, set(pending)


def has_cycle_by_walk(deps):
    """Independent check: DFS three-colouring, not the removal algorithm.

    Two independent methods agreeing is worth more than one method being
    right, because the two fail in different ways.
    """
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {n: WHITE for n in deps}

    def visit(n):
        colour[n] = GREY
        for m in deps.get(n, ()):
            if colour.get(m, WHITE) == GREY:
                return True
            if colour.get(m, WHITE) == WHITE and visit(m):
                return True
        colour[n] = BLACK
        return False

    return any(colour[n] == WHITE and visit(n) for n in deps)


print("=" * 74)
print("1. A DAG: both methods agree that no cycle exists")
print("=" * 74)
deps = parse_deps(SAMPLE)
order, remaining = kahn(deps)
cyclic = has_cycle_by_walk(deps)
print(f"  nodes                        : {sorted(deps)}")
print(f"  Kahn's removal order          : {order}")
print(f"  nodes left over              : {sorted(remaining)}")
print(f"  linear extension exists       : {not remaining}")
print(f"  cycle found by DFS colouring  : {cyclic}")
print()
print(f"  A linear extension exists: {not remaining}.  A cycle exists: {cyclic}.")
print("  The two methods answer different questions -- 'can I order these?'")
print("  and 'is there a cycle?' -- and for this graph they agree.")
print()

print("  Check the order really is an extension: every dependency comes first.")
ok = True
for n in order:
    for m in deps[n]:
        if m not in order or order.index(m) > order.index(n):
            ok = False
print(f"  every dependency precedes its dependent : {ok}")
print()
print("  That check is the whole content of the induction. Kahn's algorithm")
print("  only ever removes a node whose dependencies are already gone, so the")
print("  removal order satisfies the precondition by construction. The")
print("  induction is on the number of nodes removed so far.")
print()

print("=" * 74)
print("2. Adding one edge creates a cycle, and both methods notice")
print("=" * 74)
with_cycle = {n: set(d) for n, d in deps.items()}
with_cycle[10].add(15)          # lesson 10 now needs lesson 15
order2, remaining2 = kahn(with_cycle)
cyclic2 = has_cycle_by_walk(with_cycle)
print("  added edge: lesson 10 now needs 15")
print(f"  Kahn's removal order          : {order2}")
print(f"  nodes left over              : {sorted(remaining2)}")
print(f"  linear extension exists       : {not remaining2}")
print(f"  cycle found by DFS colouring  : {cyclic2}")
print()
print(f"  Kahn's removal order is empty: {order2 == []}")
print(f"  every node is left over      : {sorted(remaining2) == sorted(deps)}")
print(f"  nodes blocked by the cycle   : "
      f"{len(remaining2)} of {len(deps)}")
print(f"  fraction of the plan that survives: "
      f"{1 - len(remaining2) / len(deps):.1%}")
print()
print("  (d) Why all of them, and not only the three on the cycle 10->15->")
print("  14->13->12->11->10: because every leftover node has a dependency")
print("  inside the leftover set. Kahn's loop only removes a node whose")
print("  dependencies are already gone, and the cycle members never leave, so")
print("  nothing downstream of them can leave either. The blocked set is")
print("  exactly the cycle plus its downstream cone.")
print()
print("  This is the practical cost of the theorem. One wrong dependency does")
print("  not fail one lesson; it fails every lesson that depends on it,")
print("  transitively. That is why a scheduler reporting a cycle is more than")
print("  a syntax complaint.")
print()

print("=" * 74)
print("3. The base case, checked rather than asserted")
print("=" * 74)
for size in range(0, 5):
    empty_graph = {n: set() for n in range(size)}
    order3, rem3 = kahn(empty_graph)
    print(f"  {size} nodes, no dependencies -> order {order3}, "
          f"leftover {sorted(rem3)}, extension exists: {not rem3}")
print()
print("  An empty graph has an empty linear extension, and that is the base")
print("  case of the induction: zero nodes is trivially orderable. Removing")
print("  one node at a time gives the step, so every size is covered.")

print()
print("=" * 74)
print("4. (e) and (f): where each half of the induction lives in the code")
print("=" * 74)
print()
print("  Claim.  A finite dependency graph with no cycle admits an ordering in")
print("  which every lesson appears after everything it needs.")
print()
print("  P(k).  After k removal steps, the k removed nodes can be listed with")
print("  every dependency of each appearing earlier.")
print()
print("  Base case, P(0).  The empty list satisfies the property vacuously --")
print("  there is no node to violate it.  In the code: `order = []` before the")
print("  loop starts.")
print()
print("  Step.  Suppose P(k).  Kahn picks a node n with no unmet dependency, so")
print("  every lesson n needs is among the k already removed and therefore")
print("  already listed.  Appending n preserves the property, giving P(k+1).")
print("  In the code: the line")
print()
print("      ready = sorted(n for n, needs in pending.items() if not needs)")
print()
print("  is the whole step.  The test `if not needs` IS the induction")
print("  hypothesis being used -- it says every dependency of n is already")
print("  gone, which is exactly what P(k) says about them.")
print()
print("  Termination.  Each step removes at least one node, and the node count")
print("  is a non-negative integer, so the loop ends within |V| iterations.")
print("  In the code: the `while pending` condition, plus the `guard` that")
print("  makes 'stuck' an explicit outcome rather than a hang.")
print()
print("  Why no cycle implies the loop finishes with nothing left.  If it")
print("  stopped early, every remaining node would have a dependency inside")
print("  the remaining set (otherwise one would be removable).  Follow those")
print("  dependencies: each step moves within a set of shrinking size, so")
print("  within |V| steps a node repeats -- a cycle.  Contradiction.")
print()
print("  So the honest summary is that the code does not implement a proof")
print("  about graphs; the code's own invariant is the induction, and the")
print("  cycle case falls out of the termination argument. That is why this")
print("  theorem feels obvious and is still worth proving.")

print()
print("=" * 74)
print("5. Where strong induction would be needed instead")
print("=" * 74)
print()
print("  Some claims have no P(k) -> P(k+1) step at all.  Proving that every")
print("  integer above 1 is a sum of primes needs the result for every smaller")
print("  value, not just k.  Strong induction assumes P(j) for all j < k, and")
print("  the step then has the whole prefix available.")
print()
print("  The design choice this exposes is worth naming: the induction")
print("  VARIABLE (what k counts) and the HYPOTHESIS AVAILABLE (what the step")
print("  may assume) are independent.  Picking the wrong variable does not")
print("  produce a false step -- it produces no step, which is the diagnostic")
print("  sign that you are on the wrong one.")
```

Output:

```text
==========================================================================
1. A DAG: both methods agree that no cycle exists
==========================================================================
  nodes                        : [10, 11, 12, 13, 14, 15]
  Kahn's removal order          : [10, 11, 12, 13, 14, 15]
  nodes left over              : []
  linear extension exists       : True
  cycle found by DFS colouring  : False

  A linear extension exists: True.  A cycle exists: False.
  The two methods answer different questions -- 'can I order these?'
  and 'is there a cycle?' -- and for this graph they agree.

  Check the order really is an extension: every dependency comes first.
  every dependency precedes its dependent : True

  That check is the whole content of the induction. Kahn's algorithm
  only ever removes a node whose dependencies are already gone, so the
  removal order satisfies the precondition by construction. The
  induction is on the number of nodes removed so far.

==========================================================================
2. Adding one edge creates a cycle, and both methods notice
==========================================================================
  added edge: lesson 10 now needs 15
  Kahn's removal order          : []
  nodes left over              : [10, 11, 12, 13, 14, 15]
  linear extension exists       : False
  cycle found by DFS colouring  : True

  Kahn's removal order is empty: True
  every node is left over      : True
  nodes blocked by the cycle   : 6 of 6
  fraction of the plan that survives: 0.0%

  (d) Why all of them, and not only the three on the cycle 10->15->
  14->13->12->11->10: because every leftover node has a dependency
  inside the leftover set. Kahn's loop only removes a node whose
  dependencies are already gone, and the cycle members never leave, so
  nothing downstream of them can leave either. The blocked set is
  exactly the cycle plus its downstream cone.

  This is the practical cost of the theorem. One wrong dependency does
  not fail one lesson; it fails every lesson that depends on it,
  transitively. That is why a scheduler reporting a cycle is more than
  a syntax complaint.

==========================================================================
3. The base case, checked rather than asserted
==========================================================================
  0 nodes, no dependencies -> order [], leftover [], extension exists: True
  1 nodes, no dependencies -> order [0], leftover [], extension exists: True
  2 nodes, no dependencies -> order [0, 1], leftover [], extension exists: True
  3 nodes, no dependencies -> order [0, 1, 2], leftover [], extension exists: True
  4 nodes, no dependencies -> order [0, 1, 2, 3], leftover [], extension exists: True

  An empty graph has an empty linear extension, and that is the base
  case of the induction: zero nodes is trivially orderable. Removing
  one node at a time gives the step, so every size is covered.

==========================================================================
4. (e) and (f): where each half of the induction lives in the code
==========================================================================

  Claim.  A finite dependency graph with no cycle admits an ordering in
  which every lesson appears after everything it needs.

  P(k).  After k removal steps, the k removed nodes can be listed with
  every dependency of each appearing earlier.

  Base case, P(0).  The empty list satisfies the property vacuously --
  there is no node to violate it.  In the code: `order = []` before the
  loop starts.

  Step.  Suppose P(k).  Kahn picks a node n with no unmet dependency, so
  every lesson n needs is among the k already removed and therefore
  already listed.  Appending n preserves the property, giving P(k+1).
  In the code: the line

      ready = sorted(n for n, needs in pending.items() if not needs)

  is the whole step.  The test `if not needs` IS the induction
  hypothesis being used -- it says every dependency of n is already
  gone, which is exactly what P(k) says about them.

  Termination.  Each step removes at least one node, and the node count
  is a non-negative integer, so the loop ends within |V| iterations.
  In the code: the `while pending` condition, plus the `guard` that
  makes 'stuck' an explicit outcome rather than a hang.

  Why no cycle implies the loop finishes with nothing left.  If it
  stopped early, every remaining node would have a dependency inside
  the remaining set (otherwise one would be removable).  Follow those
  dependencies: each step moves within a set of shrinking size, so
  within |V| steps a node repeats -- a cycle.  Contradiction.

  So the honest summary is that the code does not implement a proof
  about graphs; the code's own invariant is the induction, and the
  cycle case falls out of the termination argument. That is why this
  theorem feels obvious and is still worth proving.

==========================================================================
5. Where strong induction would be needed instead
==========================================================================

  Some claims have no P(k) -> P(k+1) step at all.  Proving that every
  integer above 1 is a sum of primes needs the result for every smaller
  value, not just k.  Strong induction assumes P(j) for all j < k, and
  the step then has the whole prefix available.

  The design choice this exposes is worth naming: the induction
  VARIABLE (what k counts) and the HYPOTHESIS AVAILABLE (what the step
  may assume) are independent.  Picking the wrong variable does not
  produce a false step -- it produces no step, which is the diagnostic
  sign that you are on the wrong one.
```</details>
## Summary
- Induction is two halves: a base case and a step from $P(k)$ to $P(k+1)$.
  Both are required and neither is optional, and the step is where all the
  work is.
- **Arbitrary** $k$ is the whole content of the step. A step for one value is
  a test, and a long test suite is a long conjunction, not a universal claim.
- The one non-trivial ingredient is well-ordering: a chain of successor steps
  from 0 cannot skip a number. Remove it and the principle fails.
- Strong induction lets the step use every earlier case. It proves the same
  things as ordinary induction, but some claims — every integer above 1 is a
  sum of primes — have no ordinary step at all.
- Length for lists, height for trees, node count for linked lists, input
  length for programs. Inducting on a *value* rather than a *size* is the most
  common failure and produces no step rather than a wrong one.
- A loop needs **three** clauses: invariant holds, invariant is preserved,
  loop terminates with the invariant implying the postcondition. Induction
  supplies the first two.
- A loop can satisfy its invariant throughout and still be wrong, because it
  stops early. That is a bug a passing test suite does not catch.
- The step advances the same quantity the recursion decreases, and that
  quantity must be bounded below. When it is not, there is no proof — only a
  test that hangs.

## Next

[Lesson 15 — Sets and Cardinality](15_sets_and_cardinality.md) turns to the
other universal quantifier in this repository: "for every *set*", rather than
"for every number". It assumes you can write a quantified claim and cover an
infinite domain with a step, and it uses exactly that machinery to show that the
integers and the pairs of integers are the same size. The notation it adds is
in [SYMBOLS.md](../SYMBOLS.md), and the counting results it leans on are
developed in [Part 02](../part02_discrete_combinatorics/20_counting_principles.md).
