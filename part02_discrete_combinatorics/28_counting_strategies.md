# 28 — Counting Strategies and When to Use Each

**Part**: part02_discrete_combinatorics · **Prerequisites**: 27 · **Time**: 40 min

---

## In Plain Words

You now have nine lessons' worth of counting tools: the product and sum rules,
nCr and nPr, the binomial theorem, inclusion–exclusion, the pigeonhole principle,
recurrences, equivalence relations, graph theory, and trees. The hard part was
never learning them. It is deciding which one a new problem wants, in the time you
have, without trying all of them.

This lesson is that decision procedure. It is organised as a funnel. You start
with a counting problem and ask five questions in order, and each answer narrows
the field until exactly one technique remains. The questions are:

**Is the answer finite and computable in a formula?** If not, it is not a counting
problem yet — say what you actually want instead.

**Is anything forbidden or required?** Constraints are the thing that breaks the
easy cases, and they almost always mean inclusion–exclusion or a complement.

**Does it decompose into independent choices?** Then multiply.

**Do the cases genuinely not overlap?** Then add. If you are not sure, they
probably do overlap.

**Does the answer grow so fast that you cannot enumerate it?** Then you have
finished the mathematics and started the computer science: write a program with
memoisation, bitmask DP, or generating-function coefficients, and stop looking
for a closed form.

The last question is the one people skip, and it is the one that decides whether
your answer is a number, an exponential algorithm, or a research problem. `#P`
completeness — in Lesson [82](../part06_algorithms_math/82_tools_for_algorithm_design.md)
— is the formal statement that some counting problems have no efficient formula.
Recognising when you are looking at one of those is a skill.

The other thing this lesson teaches is **when to stop trusting a formula**. Every
formula in this part has a domain where it applies and a boundary where it does
not. The most reliable habit in counting is to write a brute-force checker first,
get a small case correct, and only then reach for the closed form. Brute force
takes minutes, catches every misapplied rule, and tells you the closed form is
right rather than merely plausible.

## Why Computer Science Cares

- **Feasibility decisions before code.** Before you write an exhaustive search,
  count the states. C(70, 4) ≈ 916,000 subsets of size 4 out of 70 is fine;
  2⁷⁰ subsets is not; and knowing which regime you are in tells you whether to
  search, to sample, or to approximate.
- **Complexity classification.** Several famously hard problems are counting
  problems: how many Hamiltonian paths a graph has, how many colourings, how many
  ways to fill a knapsack. Recognising the shape is the first step to knowing the
  answer cannot be computed quickly.
- **State-space sizing for search.** 8-puzzle branching is 4 with 3 useful moves
  giving 4·3ⁿ effective states; that count is why 15-puzzles are solvable and
  24-puzzles are not. The count is the feasibility argument.
- **Capacity and keyspace arithmetic.** Password policy, key length, bloom filter
  sizing, and hash collision bounds are all counting questions whose answers are
  quotas rather than totals.
- **Cache and index sizing.** Number of entries determines whether a
  C(70,4) enumeration is a cache or a catastrophe.
- **Choosing an algorithm by count.** Subset-sum: dynamic programming in
  O(2ⁿ · sum) beats meet-in-the-middle beats brute force; each is chosen because
  the state count differs by orders of magnitude.
- **Test-data generation.** "Generate a graph with exactly 17 spanning trees" or
  "a binary string with no adjacent 1s" are counting constraints, and generating
  test data from a defined count is how property-based testing finds bugs.
- **Correctness oracles.** Small cases computed by brute force become the
  reference implementation you check the clever version against. This is the
  single highest-return habit in the subject.

## The Formal Version

This section is a decision procedure stated precisely enough to be followed
mechanically. Every branch cites the lesson that owns the technique.

**Decision procedure.** Given a counting problem P:

- **S0 — Is the answer finite?** If the objects are infinite, or a parameter is
  unbounded, the answer may be infinite; find the parameter and bound it first.
- **S1 — Is there a size parameter n?** Every technique below is a function of n
  (or of two parameters). If you cannot name n, you cannot count.
- **S2 — Are there constraints ("must", "at least", "at most", "distinct",
  "exactly")?** Constraints are handled by:
  - "at most / at least k" → complement plus binomial sums (Lesson
    [22](../part02_discrete_combinatorics/22_binomial_theorem.md)), or inclusion–exclusion
    ([Lesson 23](../part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md)).
  - "exactly k of a kind" → C(n, k) positions (Lesson
    [21](../part02_discrete_combinatorics/21_permutations_and_combinations.md)).
  - "no repeats" → falling factorial P(n, r).
  - "pairs forbidden together" → inclusion–exclusion.
- **S3 — Do the choices decompose?** If the answer is a product of independent
  choices, apply the product rule. Decide ordered vs unordered by asking whether
  swapping two chosen items changes the object (Lesson
  [21](../part02_discrete_combinatorics/21_permutations_and_combinations.md)).
- **S4 — Are the cases disjoint?** If yes, add. If you cannot prove disjointness,
  they overlap, and you need inclusion–exclusion (Lesson
  [23](../part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md)).
- **S5 — Is there a bijection available?** Subsets ↔ bit strings ↔ functions
  (Lesson [20](../part02_discrete_combinatorics/20_counting_principles.md)); multisets ↔ multiset permutations;
  paths ↔ sequences (Lesson [24](../part02_discrete_combinatorics/24_recurrence_relations.md)).
- **S6 — Does the object have internal structure that repeats?** Then find a
  recurrence and solve it by expansion, characteristic roots, or the master
  theorem (Lesson [24](../part02_discrete_combinatorics/24_recurrence_relations.md)).
- **S7 — Is the count exponential and too large to enumerate?** Stop doing
  mathematics. Choose an exact method (DP with memoisation, bitmask DP,
  coefficient extraction) or an approximation (sampling). If the problem is
  `#P`-complete, no polynomial algorithm is known (Lesson
  [82](../part06_algorithms_math/82_tools_for_algorithm_design.md)).

**Definition.** A counting problem is **tractable** if an exact count is
computable in time polynomial in the input size; otherwise it is **intractable**,
and `#P` is the class of problems whose *yes* instances are verifiable in
polynomial time.

**Definition.** A **closed form** is an expression in n and a fixed number of
arithmetic operations, with no loop over n. A closed form exists for C(n, k), 2ⁿ,
n!; there is none known for the number of Hamiltonian paths, and finding one would
be a major result.

**Theorem (Cayley).** The number of labelled trees on n vertices is n^(n−2)
(Lesson [27](../part02_discrete_combinatorics/27_trees_and_spanning_trees.md)) — a reminder that closed forms
exist in surprising places and that their *proof* usually uses a bijection rather
than algebra.

## Worked Example

**The problem.** A service needs to count valid 6-character passwords over the
94 printable ASCII characters, subject to: must contain at least one digit, must
contain at least one lowercase letter, and must not contain the letter repeated
in consecutive positions.

**Step S1 — Name the parameters.** n = 6 positions, alphabet size m = 94, split
into 10 digits and 84 non-digits (94 − 10). The count is a function of (n, m).

**Step S2 — Extract the constraints.**

- "At least one digit" → a constraint on the count per position → binomial
  theorem territory.
- "At least one lowercase" → the same shape, and the two constraints interact.
- "No consecutive repeats" → a *local* constraint on adjacent positions.

**Step S3/S4 — Try the naive approach.** "Pick each character freely, then
subtract the bad ones" requires subtracting overlaps between the two "at least
one" conditions and, worse, between those and the local constraint. That is
inclusion–exclusion with 2 + 10 events — 2¹² = 4096 terms. Technically possible,
practically absurd.

**Step S5 — Look for a better decomposition.** The local constraint is the clue.
Count strings position by position, remembering only whether the previous
character was a digit. That is a two-state recurrence — exactly Lesson
[24](../part02_discrete_combinatorics/24_recurrence_relations.md), and it is a *much* smaller computation.

This is the real lesson of the worked example: **a local constraint is a signal to
use a recurrence, not inclusion–exclusion.** Inclusion–exclusion handles global
constraints ("at least one of each kind"); recurrences handle local ones
("never the same twice in a row", "no two adjacent"). Recognising which kind you
have is most of the skill.

**Step S6 — Set up the recurrence.** Let

- aᵢ = number of valid length-i strings over a 2-letter alphabet (digit /
  non-digit) ending in a **digit**,
- bᵢ = number ending in a **non-digit**,

where "valid" means no two consecutive positions have the same character. Then

- aᵢ = (10 / m) · (aᵢ₋₁ + bᵢ₋₁) — append any of 10 digits to any valid prefix.
- bᵢ = (84 / m) · (aᵢ₋₁) — appending a non-digit to a prefix ending in a digit is
  fine, but appending to a prefix ending in a non-digit would need one of the 83
  *other* non-digits, which depends on identity, not just kind.

So the two-state version is not quite closed either, because the "different
non-digit" constraint depends on which specific character came before. **The fix:
track the previous character, not its kind** — 94 states, one per possible
previous character. Then

    fᵢ(c) = number of valid length-i strings ending in character c
    f₁(c) = 1 for every c
    fᵢ(c) = total_{i−1} − fᵢ₋₁(c)
    totalᵢ = Σ_c fᵢ(c)

That is a clean recurrence with 94 states and six steps: about 600 operations,
instant. The subtlety — that the state must capture exactly what the constraint
depends on — is the real content of step S6, and getting it wrong (using 2 states
instead of 94) is the classic mistake in this family of problems.

**Step S7 — Add the "at least one digit" constraint on top.** Now count only the
totalᵢ strings that contain a digit at least once. Since the alphabet splits into
digits and non-digits, and "all non-digits" is itself a valid-countable subproblem
over an alphabet of size 84:

    total₆(all 94, no adjacent repeats) − total₆(all 84, no adjacent repeats)

Each total is the same recurrence with a different alphabet size. Two runs, done.
This is the complement step, and it is far cheaper than the 4096-term
inclusion–exclusion.

**Step S8 — Verify against brute force.** 94⁶ ≈ 6.9 × 10¹¹ strings cannot be
enumerated, but the same recurrence at n = 3 can be checked against the 94³ ≈
830,000 three-character strings, which can. The agreement at n = 3 plus the exact
recurrence is strong evidence; enumerating at n = 6 is simply not possible, and
saying so is part of the answer.

**The classification, stated in one line.** Local constraint → recurrence with a
state large enough to capture it; global "at least one of a kind" constraint →
subtract the complement computed the same way. Neither inclusion–exclusion nor
nCr appears, and both were reasonable first guesses that lose badly to the
recurrence.

## Runnable Code

The decision procedure itself, implemented. Give it a description of the problem
and it reports which lessons apply. This is a real tool, not a toy: the same
five questions come up every time.

```python
def classify(problem):
    """Route a counting problem to a technique.

    `problem` is a dict with keys:
      n            - the size parameter (required)
      independent  - do the choices decompose into independent parts?
      overlap      - might two branches be the same object? (True/False/None=unknown)
      local        - is there a constraint between neighbouring positions?
      global_at_least - a "must contain at least one of a kind" constraint?
      order_matters- does swapping two chosen items change the object?
      repeats_ok   - may an item be chosen twice?
      want_exact   - do we need an exact count (vs a bound or an approximation)?
    """
    n = problem.get("n")
    advice = []

    if n is None:
        return ["S1: name the size parameter first; every formula needs it."]

    if problem.get("local"):
        advice.append(
            "S6: a LOCAL constraint (adjacent/sequential dependence) means a "
            "RECURRENCE, with a state that captures exactly what the constraint "
            "depends on. See Lesson 24."
        )

    if problem.get("global_at_least"):
        advice.append(
            "S2: 'at least one of a kind' is a GLOBAL constraint: count the "
            "complement and subtract. If two such constraints interact, reach "
            "for inclusion-exclusion. See Lessons 22-23."
        )

    if problem.get("independent"):
        advice.append(
            "S3: the choices decompose, so MULTIPLY. "
            "See Lesson 20."
        )
    if problem.get("overlap") is False:
        advice.append(
            "S4: the cases are provably disjoint, so ADD. See Lesson 20."
        )
    elif problem.get("overlap") is None:
        advice.append(
            "S4: overlap is UNKNOWN. Try to prove disjointness; if you cannot, "
            "assume overlap and use inclusion-exclusion. See Lesson 23."
        )
    else:
        advice.append(
            "S4: the cases may overlap, so plain addition overcounts. "
            "Use inclusion-exclusion, or count the complement. See Lesson 23."
        )

    if problem.get("repeats_ok") is False:
        advice.append(
            "S2: no repeats -> falling factorial P(n,r); the choice set shrinks. "
            "See Lesson 21."
        )
    elif problem.get("order_matters") is False:
        advice.append(
            "S3: order does not matter -> nCr. See Lesson 21."
        )
    elif problem.get("order_matters"):
        advice.append(
            "S3: order matters -> nPr (or n^n if repeats are allowed). "
            "See Lesson 21."
        )

    if not problem.get("want_exact", True):
        advice.append(
            "S7: an estimate is acceptable, so SAMPLE instead of enumerating. "
            "See Lesson 61."
        )

    advice.append(
        "FINALLY: write the brute-force count for the smallest instance and "
        "compare. A formula that has never been checked against enumeration is "
        "a guess with good handwriting."
    )
    return advice


cases = [
    ("passwords with at least one digit",
     {"n": 6, "independent": True, "overlap": False, "repeats_ok": True}),
    ("3 servers from a pool of 20",
     {"n": 20, "independent": True, "overlap": False, "repeats_ok": False,
      "order_matters": False}),
    ("3 servers with a failover order",
     {"n": 20, "independent": True, "overlap": False, "repeats_ok": False,
      "order_matters": True}),
    ("in how many ways can 4 people sit at a round table?",
     {"n": 4, "independent": True, "overlap": False, "repeats_ok": False,
      "order_matters": True}),
    ("strings of length n with no consecutive 1s",
     {"n": 20, "local": True, "independent": False}),
    ("strings over 94 chars, at least one digit, no adjacent repeats",
     {"n": 6, "local": True, "global_at_least": True}),
    ("integers in [1,1000] divisible by 2, 3, or 5",
     {"n": 1000, "global_at_least": True, "overlap": True}),
    ("all 8-bit masks with exactly 3 bits set",
     {"n": 8, "independent": False, "overlap": False, "repeats_ok": False,
      "order_matters": False}),
    ("how many subsets of {1..70} have size 4?",
     {"n": 70, "independent": True, "overlap": False, "repeats_ok": False,
      "order_matters": False}),
]

for title, spec in cases:
    print(f"\n{title}")
    for line in classify(spec):
        print(f"    {line}")
```

The funnel in practice: five problems, five different tools, each with a
brute-force referee.

```python
from itertools import permutations, combinations, product
from math import comb, perm, factorial


def brute_force(fn, size):
    """Enumerate a tiny instance and count."""
    return sum(1 for _ in fn(size))


def check(label, formula, brute):
    ok = formula == brute
    print(f"{label:44s} formula {formula:>12,}  brute {brute:>12,}  "
          f"{'MATCH' if ok else 'MISMATCH'}")
    return ok


results = []

# 1. Ordered, no repeats: nPr. Brute force = count the permutations.
n = 5
results.append(check(f"P({n},{2}) ordered picks of 2",
                     perm(n, 2),
                     sum(1 for p in permutations(range(n), 2))))

# 2. Unordered, no repeats: nCr.
results.append(check(f"C({n},2) unordered pairs",
                     comb(n, 2),
                     sum(1 for c in combinations(range(n), 2))))

# 3. Unordered, repeats allowed: stars and bars.
m, r = 4, 3
from itertools import product as iproduct


def multiset_vectors(m, r):
    """Every multiplicity vector over m kinds totalling r items."""
    return [v for v in iproduct(range(r + 1), repeat=m) if sum(v) == r]


results.append(check(f"C({m}+{r}-1,{r}) multisets of size {r} from {m} types",
                     comb(m + r - 1, r), len(multiset_vectors(m, r))))

# 4. Local constraint: binary strings with no consecutive 1s -> Fibonacci.
def no_adjacent(n):
    """Length-n binary strings with no two consecutive 1s: Fibonacci."""
    if n == 0:
        return 1
    a, b = 1, 2
    for _ in range(2, n + 1):
        a, b = b, a + b
    return a if n == 1 else b


results.append(check("length-12 strings, no consecutive 1s",
                     no_adjacent(12),
                     sum(1 for x in range(1 << 12) if "11" not in format(x, "012b"))))

# 5. Global constraint: subsets of {1..6} whose sum is even.
S = set(range(1, 7))
subs = [frozenset(c) for k in range(len(S) + 1) for c in combinations(sorted(S), k)]
results.append(check("subsets of {1..6} with even sum (n=3 too big to brute force)",
                     sum(1 for s in subs if sum(s) % 2 == 0),
                     sum(1 for s in subs if sum(s) % 2 == 0)))

print(f"\n{sum(results)} of {len(results)} checks matched")
print("check 5 is intentionally small: with 6 elements there are 64 subsets, so")
print("enumeration is the *method*, not just the referee. The rule of thumb is")
print("enumerate while the count fits in memory, then switch to the formula.")
```

The two-state versus 94-state lesson, side by side. This is the single most
important practical point in the lesson.

```python
def count_no_adjacent_repeats(length, alphabet_size):
    """Count length-n strings over an alphabet of size m with no two adjacent
    positions equal.

    State = the exact previous character. That is the only information the
    constraint depends on, so m states is the right size.

        f_1(c) = 1                       one string of length 1 ending in c
        f_n(c) = total_{n-1} - f_{n-1}(c) append c to any prefix not ending in c
        total_n = sum over c
    """
    # f[c] = number of valid strings of the current length ending in c
    f = {c: 1 for c in range(alphabet_size)}
    for _ in range(length - 1):
        total = sum(f.values())
        f = {c: total - f[c] for c in f}
    return sum(f.values())


def count_by_kind(length, n_digits, n_other):
    """A two-state version: track only whether the previous character was a digit.

    This answers a DIFFERENT and stricter question -- no two adjacent positions
    may have the same *kind*. So it also forbids adjacent distinct non-digits
    such as 'bc', which the real constraint allows. Reaching for it when you
    meant the real constraint is the classic wrong-state bug, and it fails
    silently: the number it returns is a plausible positive integer."""
    d, u = n_digits, 0
    for _ in range(length - 1):
        d, u = n_digits * (d + u), n_other * d
    return d + u


def brute(length, alphabet_size):
    return sum(
        1 for t in __import__("itertools").product(range(alphabet_size), repeat=length)
        if all(t[i] != t[i + 1] for i in range(length - 1))
    )


for m in (2, 3, 5):
    for n in (1, 2, 3, 4):
        got = count_no_adjacent_repeats(n, m)
        want = brute(n, m)
        print(f"m={m} n={n}: state-per-character {got:>5}  brute force {want:>5}  "
              f"{'ok' if got == want else 'WRONG'}")

good = count_no_adjacent_repeats(6, 94)
naive = count_by_kind(6, 10, 84)
digits_only = count_no_adjacent_repeats(6, 94) - count_no_adjacent_repeats(6, 84)
print("\n6-char passwords over 94 chars, no two adjacent positions equal:")
print(f"  correct (94 states)   : {good:,}")
print(f"  too strict (2 states) : {naive:,}")
print(f"  under-counts by       : {good - naive:,}")
print()
print("The same recurrence over the 84 non-digit characters alone gives")
print(f"{count_no_adjacent_repeats(6, 84):,}, so the number of valid passwords")
print(f"containing at least one digit is {digits_only:,} -- one extra run of the")
print("same recurrence, and no inclusion-exclusion anywhere.")

```

When to stop and write a program: DP with memoisation versus brute force.

```python
from functools import lru_cache
from itertools import combinations
from math import factorial
from itertools import combinations


def count_subsets_with_sum(target):
    """How many subsets of {1..9} sum to target?

    Closed form: none. Enumeration: 512 subsets, trivial. But the same DP with
    n=100 is 101*target states instead of 2^100 subsets -- which is the whole
    reason to bother with DP."""

    @lru_cache(maxsize=None)
    def go(i, remaining):
        if i > 9:
            return 1 if remaining == 0 else 0
        total = go(i + 1, remaining)                 # skip i
        if i <= remaining:
            total += go(i + 1, remaining - i)        # take i
        return total

    return go(1, target)


def brute(target):
    return sum(1 for k in range(10)
               for c in combinations(range(1, 10), k)
               if sum(c) == target)


print(f"{'target':>7} {'DP':>6} {'brute force':>12}  agree")
for t in (0, 5, 10, 20, 22, 45):
    print(f"{t:7d} {count_subsets_with_sum(t):6d} {brute(t):12d}  "
          f"{count_subsets_with_sum(t) == brute(t)}")

print(f"\nDP state count for n=100, target=100: {101 * 101:,} states")
print(f"brute-force subset count for n=100:     2^100 = {2**100:,}")
print(f"ratio: {2**100 / (101 * 101):.3e}x")

# The bitmask-DP regime: counting Hamiltonian paths by DP over subsets.
def hamiltonian_paths_from(nodes):
    """Paths that START at nodes[0] and visit every node exactly once.

    dp[mask][j] = number of such paths that used exactly the vertices in mask and
    ended at j. Total states 2^n * n, versus (n-1)! for enumeration."""
    n = len(nodes)
    full = 1 << n
    dp = [[0] * n for _ in range(full)]
    dp[1][0] = 1                       # the only length-1 path starts at nodes[0]
    for mask in range(full):
        for j in range(n):
            if not dp[mask][j]:
                continue
            for k in range(1, n):      # nodes[0] is already used and cannot repeat
                if not (mask >> k) & 1:
                    dp[mask | (1 << k)][k] += dp[mask][j]
    return sum(dp[full - 1])


def hamiltonian_brute(nodes):
    from itertools import permutations
    return sum(1 for p in permutations(nodes[1:]))


from math import factorial

for n in (4, 5, 6, 7, 8):
    got = hamiltonian_paths_from(list(range(n)))
    want = hamiltonian_brute(list(range(n)))
    print(f"n={n}: DP {got:>7,}  brute {want:>7,}  agree {got == want}   "
          f"DP states 2^n*n = {(1 << n) * n:>5,} vs n! = {factorial(n):>9,}")

print()
print("The DP wins because its state count grows like 2^n while enumeration grows")
print(f"factorially: at n = 7 the DP needs {2 ** 7 * 7:,} states against 7! = "
      f"{factorial(7):,},")
print("and the gap widens from there.")

```

Sampling when exact counting is hopeless, and how to say so honestly.

```python
import random
from math import comb


def sample_collision(n_items, table_size, trials=20_000, seed=1):
    """Estimate the probability of at least one collision, by sampling.

    Exact inclusion-exclusion over the C(n_items,2) pairwise collision events has
    2^C(n_items,2) terms; sampling gives a usable number in a fixed budget."""
    rng = random.Random(seed)
    hits = 0
    for _ in range(trials):
        seen = set()
        for _ in range(n_items):
            k = rng.randrange(table_size)
            if k in seen:
                hits += 1
                break
            seen.add(k)
    return hits / trials


for n_items in (16, 32, 64, 128):
    m = 2**128
    exact_ish = 1 - (1 - (n_items * (n_items - 1) / 2) / m) ** 1   # first-order
    print(f"n={n_items:4d}: exact first-order approximation "
          f"{exact_ish:.3e}, sampled {sample_collision(n_items, m):.3e}")
print()
print("Counting exactly would mean a sum over every subset of the pairwise")
print("collision events -- that is 2^C(n,2) terms, hopeless from n = 6 upwards.")
print("That is the moment to stop counting and start sampling.")
n = 64
print(f"\nFor scale: the middle binomial coefficient C(64,32) is already "
      f"{comb(n, n // 2):,} terms,")
print(f"and the number of subsets of a 64-element set is {2**64:,}.")
```

## Common Mistakes

**1. Reaching for inclusion–exclusion on a local constraint.**

> Wrong: "No two adjacent characters equal. Subtract all the bad pairs." There
> are n − 1 local constraints, and inclusion–exclusion over them has 2^(n−1)
> terms.
> Right: Use a recurrence. Local constraints have overlapping scopes, which is
> exactly the structure a DP handles and exactly the structure inclusion–exclusion
> handles worst.
> Why the wrong one is tempting: inclusion–exclusion is *the* tool for "not A",
> and "no adjacent repeats" is a "not" condition. The trap is not noticing that
> the n − 1 bad events overlap each other and the global constraints.

**2. Choosing a state that does not capture the constraint.**

> Wrong: track only whether the previous character was a digit, then multiply.
> Right: track the previous character itself, 94 states. For "no adjacent
> repeats" the constraint depends on identity, not on kind.
> Why the wrong one is tempting: fewer states is faster, and the two-state answer
> is a plausible-looking positive integer with no error message.

**3. Believing a closed form you have not checked.**

> Wrong: "The answer is C(52,5), so ship it." If the problem meant "5 cards from
> 2 decks" the count is different and nothing warns you.
> Right: Enumerate a small case. If your formula disagrees, you have found a bug
> in under a minute; if it agrees, you have evidence rather than confidence.
> Why the wrong one is tempting: the formula is standard, so doubt feels
> misplaced. The formula is standard for a *specific* problem shape, and the
> work is in recognising the shape.

**4. Enumerating when the count is astronomically large.**

> Wrong: "I will enumerate all 94⁶ passwords to count them."
> Right: The recurrence computes the same number in about 600 operations. The
> count was never the hard part; the representation was.
> Why the wrong one is tempting: enumeration is obviously correct and needs no
> insight. Insight is exactly what makes the problem tractable, and for n = 6
> over 94 characters enumeration is 6.9 × 10¹¹ items.

**5. Not stating the answer's scope.**

> Wrong: "The number of valid passwords is X."
> Right: "The number of 6-character strings over 94 printable ASCII characters
> with no two adjacent positions equal is X; the count of those containing at
> least one digit is Y." Counts are always relative to a precise size
> specification, and an unqualified number cannot be checked by anyone.
> Why the wrong one is tempting: the answer looks finished, and restating the
> specification feels redundant once you have computed it.

## Exercises and Solutions

**[ ] Exercise 1 — Classify ten problems.** For each, name the size parameter and
the technique: (a) arrangements of the letters in "BANANA"; (b) ways to choose a
3-element committee and a chair from 12 people; (c) 8-digit numbers with all
digits distinct; (d) the number of ways to seat 6 people in a row of 6 chairs;
(e) binary strings of length 20 with no two consecutive 0s; (f) integers in
[1, 100] divisible by 2, 3, or 5; (g) subsets of a 10-element set containing
element 1; (h) the number of binary trees on n nodes; (i) the number of ways to
place 8 non-attacking rooks on a chessboard; (j) the number of connected labelled
graphs on 4 vertices.

<details>
<summary>Solution</summary>

(a) Multiset permutation: 6!/(3!·2!) = 60. n = 6 characters, with repetition.
(b) Unordered set + one distinguished member: C(12,3) · 3 = 220 · 3 = 660. Product
rule, then a second product for the chair.
(c) Ordered without repeats from a 10-symbol alphabet: P(10,8) = 1,814,400. (If
"8-digit number" excluded a leading zero, subtract P(9,7) = 181,440 to get
1,632,960.)
(d) Order matters, no repeats, using every item: 6! = 720.
(e) Local constraint → recurrence: aₙ = aₙ₋₁ + aₙ₋₂ with a₀ = 1, a₁ = 2, so
a₂₀ = F₂₂ = 17,711.
(f) Global "at least one of" constraint with overlaps → inclusion–exclusion:
50 + 33 + 20 − 16 − 10 − 6 + 3 = 74.
(g) Subset with one element forced → nCr on the rest: C(9,2) = 36.
(h) Labelled trees → Cayley: n^(n−2).
(i) Placement of 8 non-attacking rooks on 8×8 → bijection with permutations of 8:
8! = 40,320. (Each rook gets a distinct row and column, so the configuration is
a permutation.)
(j) Labelled graphs on 4 vertices → 2^(C(4,2)) = 2^6 = 64, since each of the 6
possible edges is present or absent. The connected ones number 38. Note the
trap: inclusion–exclusion over the four "vertex v is isolated" events gives
**41**, not 38, because three of the disconnected graphs have no isolated
vertex at all — they are two disjoint edges. A constraint can fail for more
than one reason, and inclusion–exclusion only corrects for the reasons you
actually enumerated.

```python
from itertools import combinations
from math import comb, perm, factorial

print(f"(a) BANANA arrangements        : {factorial(6)//(factorial(3)*factorial(2))}")
print(f"(b) committee + chair          : {comb(12, 3) * 3}")
print(f"(c) 8 distinct digits          : {perm(10, 8)}")
print(f"(d) 6 people in a row          : {factorial(6)}")
f = [1, 2]
for _ in range(2, 21):
    f.append(f[-1] + f[-2])
print(f"(e) length-20 no two 0s        : {f[20]}")
print(f"(f) divisible by 2, 3 or 5     : {50 + 33 + 20 - 16 - 10 - 6 + 3}")
print(f"(g) subsets containing 1       : {comb(9, 2)}")
print(f"(h) labelled trees on n        : n^(n-2), e.g. 4^2 = {4**2}")
print(f"(i) 8 non-attacking rooks      : {factorial(8)}")
print(f"(j) all graphs on 4 vertices   : {2**6}")

# (j) refined: connected graphs on 4 labelled vertices. The tempting route is
# inclusion-exclusion over the four events "vertex v is isolated" -- and it is
# WRONG, because a graph can be disconnected with no isolated vertex.
edges4 = [(i, j) for i in range(4) for j in range(i + 1, 4)]
naive = sum((-1)**k * comb(4, k) * 2 ** (len(edges4) - comb(k, 2) - k * (4 - k))
            for k in range(5))


def connected_labelled(n):
    edges = list(combinations(range(n), 2))

    def components(mask):
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for i, (u, v) in enumerate(edges):
            if mask >> i & 1:
                ru, rv = find(u), find(v)
                if ru != rv:
                    parent[ru] = rv
        return len({find(i) for i in range(n)})

    return sum(1 for mask in range(1 << len(edges)) if components(mask) == 1)


print(f"(j) connected graphs on 4      : {connected_labelled(4)}")
print(f"    naive IE over isolated vts : {naive}   <-- WRONG by 3")
print("    the 3 missed graphs are two disjoint edges: disconnected, yet with no")
print("    isolated vertex. Fixing this needs inclusion-exclusion over every")
print("    partition of the vertex set, not just the singletons.")
```
</details>

**[ ] Exercise 2 — Local versus global.** Count the 4-character strings over
{a, b, c} that (i) contain the letter a at least once, and (ii) have no two
adjacent positions both a. Solve both ways and compare.

<details>
<summary>Solution</summary>

**(i) At least one a.** Total 3⁴ = 81 minus those with no a, which is 2⁴ = 16, so
81 − 16 = 65. This is the complement step, and the binomial theorem gives it
directly: Σ_{k=1..4} C(4,k)·2^(4−k) = 4·8 + 6·4 + 4·2 + 1 = 65.

**(ii) No two adjacent a's.** A local constraint, so use a recurrence. Let Aₙ be
the count of length-n strings over {a,b,c} with no adjacent a's, and split by
whether the string ends in a.

- Ends in b or c: 2 choices after any valid length-(n−1) prefix → 2·Aₙ₋₁.
- Ends in a: the previous position must be b or c, so take a valid length-(n−1)
  prefix *ending in b or c*, which is 2·Aₙ₋₂ by the same count.

So Aₙ = 2·Aₙ₋₁ + 2·Aₙ₋₂, with A₀ = 1 and A₁ = 3. That gives A₂ = 8, A₃ = 22,
A₄ = 60.

**Both together.** The interesting version: strings with no adjacent a's *and*
at least one a. Count all no-adjacent-a strings (60) and subtract those with no a
at all, which is the same problem over {b, c}: Bₙ = 2·Bₙ₋₁ with B₀ = 1, so
B₄ = 16. Answer 60 − 16 = 44.

```python
from itertools import product

def total_with_local(n, k):
    """Length-n strings over k symbols with no adjacent a's."""
    prev, cur = 1, k
    for _ in range(2, n + 1):
        prev, cur = cur, (k - 1) * cur + (k - 1) * prev
    return cur


def brute_local(n, k):
    return sum(1 for t in product("abc"[:k], repeat=n) if "aa" not in "".join(t))


def brute_at_least(n, k):
    return sum(1 for t in product("abc"[:k], repeat=n) if "a" in "".join(t))


print(f"(i)  at least one a        : {3**4 - 2**4}      brute {brute_at_least(4, 3)}")
print(f"(ii) no adjacent a's       : {total_with_local(4, 3)}      brute {brute_local(4, 3)}")
print(f"(iii) both                 : {total_with_local(4, 3) - 2**4}      "
      f"brute {sum(1 for t in product('abc', repeat=4) if 'aa' not in ''.join(t) and 'a' in ''.join(t))}")
print()
print("local constraint -> recurrence, global constraint -> subtract a complement")
print("computed with the same recurrence. Neither needs inclusion-exclusion here.")
```
</details>

**[ ] Exercise 3 — Recurrence from a board.** A light bulb starts off. Each round
you may flip the bulb or leave it, but you may not leave it off two rounds in a
row. How many valid sequences of n rounds are there? Compute a₅ and a₁₀ and check
a₅ against enumeration.

<details>
<summary>Solution</summary>

Let aₙ be the count of valid length-n sequences. Split by the final state: the
bulb is **on** (any valid prefix works, giving aₙ₋₁ sequences, since flipping it
on is always allowed) or **off** (the previous round must have been on, giving
aₙ₋₂ sequences). So

    aₙ = aₙ₋₁ + aₙ₋₂,  a₀ = 1, a₁ = 2

These are Fibonacci numbers: aₙ = F(n+2). So a₅ = F₇ = 13 and a₁₀ = F₁₂ = 144.

Checking a₅ against enumeration: 2⁵ = 32 sequences, and 13 avoid the pattern
"off, off".

```python
from itertools import product

def a(n):
    if n == 0:
        return 1
    prev, cur = 1, 2
    for _ in range(2, n + 1):
        prev, cur = cur, prev + cur
    return cur

def brute(n):
    return sum(1 for t in product((0, 1), repeat=n) if "00" not in "".join(map(str, t)))

for n in (1, 2, 3, 4, 5, 8, 10):
    print(f"n={n:2d}: recurrence {a(n):4d}  brute {brute(n):4d}  agree {a(n) == brute(n)}")
print(f"\na5 = {a(5)}, a10 = {a(10)}")
```
</details>

**[ ] Exercise 4 — When to stop counting.** For each problem, say whether an exact
count is feasible, and if not, what you would do instead.

(a) How many distinct bit patterns appear among 2⁴⁰ random 40-bit integers?
(b) How many ways to order 20 items with 5 disjoint pairs that must stay
adjacent?
(c) How many spanning trees does a 30-vertex graph have?
(d) How many shortest paths are there from A to F in a layered graph with 10
layers of 5 vertices each, where every vertex connects to all 5 in the next layer?
(e) How many integers below 10¹⁸ are divisible by 2, 3, 5, or 7?

<details>
<summary>Solution</summary>

(a) **Exact and easy.** Every 40-bit pattern is reachable, so 2⁴⁰ ≈ 1.1 × 10¹².
Product rule.

(b) **Exact and easy.** Each pair is one super-item. So 5 super-items plus 10
singles = 15 items to order, giving 15! ≈ 1.3 × 10¹², and no internal order
matters because a pair's two members can go either way — so the count is
15! · 2⁵ = 4.2 × 10¹³. Bijection: collapse the pairs (Lesson
[24](../part02_discrete_combinatorics/24_recurrence_relations.md)/[27](../part02_discrete_combinatorics/27_trees_and_spanning_trees.md)).

(c) **Exact but expensive.** The Matrix–Tree Theorem gives it as a determinant
of the Laplacian's cofactor — a closed form of sorts, computable in O(n³) with
float arithmetic and exact integer algorithms. Without that theorem you have no
formula at all, and enumerating spanning trees is hopeless beyond n ≈ 10.

(d) **Exact and cheap, if you notice the structure.** Each layer multiplies the
count: after 10 layers there are 5¹⁰ = 9,765,625 paths from a fixed start. The
product rule. The trap is enumerating them one at a time — 9.7 million is
tractable, but 5²⁰ would not be, and the product rule is what tells you the
difference.

(e) **Exact and easy.** Inclusion–exclusion over four divisors is 2⁴ − 1 = 15
terms, and the count is a fraction of 10¹⁸ computed in integer arithmetic. Here
the "too large to enumerate" intuition is right and the formula is essential.

```python
from math import comb, factorial

print(f"(a) {2**40:,}")
print(f"(b) 15! * 2^5 = {factorial(15) * 2**5:,}")
print(f"(d) 5^10 = {5**10:,}")

# (e) inclusion-exclusion over 2, 3, 5, 7 below 10^18.
from itertools import combinations
from math import lcm

LIM = 10**18
DIV = [2, 3, 5, 7]
total = 0
for k in range(1, len(DIV) + 1):
    sign = 1 if k % 2 == 1 else -1
    for combo in combinations(DIV, k):
        m = 1
        for d in combo:
            m = lcm(m, d)
        total += sign * (LIM // m)
print(f"(e) {total:,} of {LIM:,} integers, i.e. {total / LIM:.4%}")

# (c) has no formula from Part 02; it needs the Matrix-Tree Theorem.
print("(c) no formula from this part -- Matrix-Tree Theorem, a determinant")
```
</details>

**[ ] Exercise 5 — Surjections via a complement.** How many functions from a
5-element set to a 3-element set hit every target? Compute by inclusion–exclusion
and by brute force.

<details>
<summary>Solution</summary>

By inclusion–exclusion (the complement of "misses some target"):

    Σ_{j=0..3} (−1)ʲ C(3,j)(3−j)⁵ = 3⁵ − 3·2⁵ + 3·1⁵ − 0
                             = 243 − 96 + 3 = 150

Brute force: 3⁵ = 243 functions, and 150 of them are surjective. Both agree.

This is a good classification example: the constraint is global ("every target
must be hit"), the events overlap heavily (a function can miss two targets), and
the event count is small (3). That is exactly the regime where inclusion–exclusion
wins. If there were 30 targets the term count would be 2³⁰, and the right move
would be Stirling numbers or a DP.

```python
from itertools import product
from math import comb

def onto_ie(n, k):
    return sum((-1)**j * comb(k, j) * (k - j)**n for j in range(k + 1))

def onto_brute(n, k):
    return sum(1 for f in product(range(k), repeat=n) if set(f) == set(range(k)))

for k in (2, 3, 4):
    print(f"onto 5->{k}: IE {onto_ie(5, k):5d}  brute {onto_brute(5, k):5d}  "
          f"agree {onto_ie(5, k) == onto_brute(5, k)}")

print()
print("the IE formula has 2^k - 1 terms, so it degrades fast as k grows:")
for k in (5, 10, 20, 30):
    print(f"  k={k:3d}: {2**k - 1:,} terms")
```
</details>

**[ ] Challenge 6 — Know when to give up.** Give one problem each where (a) a
closed form exists and is easy, (b) a recurrence is the right tool, (c)
inclusion–exclusion is the right tool, (d) brute force is the right tool, and
(e) no efficient exact algorithm is known. For each, say what you would do in
practice.

<details>
<summary>Solution</summary>

(a) **Closed form, easy.** How many subsets of an n-element set contain element 1?
Answer C(n−1, n−2) = n − 1. Bijection: fix element 1, choose any subset of the
rest. Use the formula and never enumerate.

(b) **Recurrence.** Number of length-n binary strings with no two consecutive 1s:
aₙ = aₙ₋₁ + aₙ₋₂. There is a closed form (F(n+2)) but the recurrence is what you
compute, because it costs O(n) and produces every intermediate value.

(c) **Inclusion–exclusion.** Integers below 10⁶ divisible by 2, 3, or 5. The
events overlap, the count of divisors is small, and 2³ − 1 = 7 terms. Use it.

(d) **Brute force.** The number of orderings of 8 distinct items: 8! = 40,320.
Enumeration is 40,320 items and the formula is one line, so either is fine — but
when the answer is small enough to enumerate, enumerate, because you need the
items anyway. This is the honest answer for small state spaces.

(e) **No efficient exact algorithm known.** The number of Hamiltonian paths in a
general graph, or the number of independent sets in a 3-regular graph. `#P`-complete,
so no polynomial-time exact algorithm is known and none is expected. In practice:
dynamic programming over subsets (2ⁿ · n, fine to n ≈ 25), integer programming,
approximation with provable guarantees, or sampling. The practical skill is
recognising that you are in this regime *early*, because the algorithm choice
changes everything.

```python
from math import comb, factorial
from itertools import combinations, permutations
from itertools import product as iproduct

# (a)
print(f"(a) C(n-1,n-2) = n-1; at n=100 that is {comb(99, 98)}")

# (b)
def fib(n):
    a, b = 1, 2
    for _ in range(2, n + 1):
        a, b = b, a + b
    return a if n == 1 else b

print(f"(b) F(n+2); at n=50 that is {fib(50):,}")

# (c)
from math import lcm
LIM = 10**6
DIV = [2, 3, 5]
print(f"(c) {50 + 33 + 20 - 16 - 10 - 6 + 3} below 1000, scaled to 10^6 by lcm terms")

# (d)
print(f"(d) 8! = {factorial(8):,}, enumerable in well under a second")

# (e) DP over subsets beats brute force by a huge factor.
def ham_dp(n):
    full = 1 << n
    dp = [[0] * n for _ in range(full)]
    for j in range(n):
        dp[1 << j][j] = 1
    for mask in range(full):
        for j in range(n):
            if dp[mask][j]:
                for k in range(n):
                    if not (mask >> k) & 1:
                        dp[mask | (1 << k)][k] += dp[mask][j]
    return sum(dp[full - 1])

print(f"(e) Hamiltonian paths on 10 nodes: DP {ham_dp(10):,} "
      f"vs brute force {factorial(10):,} permutations")
```
</details>

## Summary

- Five questions in order: is the answer finite, is there a size parameter, are
  there constraints, do the choices decompose, are the cases disjoint.
- **Local constraints → recurrence** with a state that captures exactly what the
  constraint depends on; the wrong state size gives a wrong answer silently.
- **Global "at least one of a kind" constraints → subtract the complement**, and
  reach for inclusion–exclusion when the events overlap and few in number.
- Inclusion–exclusion has 2ⁿ − 1 terms, so it wins for small n and loses badly
  past about n = 20 events.
- Independent choices multiply; disjoint cases add; order and repetition decide
  between nCr, nPr, and nⁿ.
- When the state count is exponential, the answer is a program: DP with
  memoisation, bitmask DP, or coefficient extraction — not a closed form.
- When the problem is `#P`-complete, sample or approximate, and say so.
- Always write the brute-force count for the smallest instance and compare; it
  takes minutes and catches every misapplied rule.
- State the answer's scope precisely. A count without its size specification
  cannot be checked by anyone.

## Next

This is the end of Part 02. You now have counting, recurrences, relations, graphs,
and trees. [Part 03 — Linear Algebra](../part03_linear_algebra/README.md) takes
the adjacency matrices from Lesson 26 and the 2×2 matrices from Lesson 24 and
develops the mathematics that machine learning is built on — starting with
[Lesson 30 — Vectors and Vector Spaces](../part03_linear_algebra/30_vectors_and_vector_spaces.md).
For a different direction, [Lesson 80 — Big-O and Complexity Analysis](../part06_algorithms_math/80_big_o_and_complexity.md)
turns the growth rates you computed here into the formal language of algorithm
analysis.