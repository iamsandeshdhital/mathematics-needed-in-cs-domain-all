# 11 — Truth Tables, Equivalence, and Normal Forms

**Part**: part01_logic_proof · **Prerequisites**: 10 · **Time**: 40 min

---

## In Plain Words

A formula in a handful of letters has a completely determined behaviour. If you
fix how many letters there are and then list every way of making each one true
or false, you have listed everything the formula can ever do. Two letters gives
four rows. Three letters gives eight. Twenty gives about a million. That list
is the formula's truth table, and it is a complete description of the formula.

Once you have it, everything else in this lesson is bookkeeping. Two formulas
are the same formula if their columns match exactly. A formula is worthless if
its column is all ones, and useless if its column is all zeros. And any formula
at all can be rewritten into one of two standard shapes, just by reading its own
table.

The practical payoff is this: you can stop guessing whether a complicated
condition you wrote does what you meant. Compare columns. That is a mechanical
check, and it is exactly the check a compiler, a circuit designer, or a formal
verification tool performs.

## Why Computer Science Cares

**Circuit synthesis is this lesson.** Every digital circuit, from a single gate
to a CPU, is a formula in AND, OR and NOT. The truth table specifies it; the
normal forms and the equivalences are how you shrink it. NAND alone is enough
for everything, which is why the first integrated circuits used it.

**Every boolean condition you write is a formula.** The simplification
techniques here turn a condition that took a year to accumulate into one line,
and prove the rewrite preserves behaviour.

**Exhaustive verification works because truth tables are finite.** Model
checking a piece of hardware, a protocol, or a small state machine means
enumerating states. When the state space fits, you get a proof rather than a
test result.

**SAT solving is CNF.** Every SAT problem is converted to conjunctive normal
form before the solver starts. Section 5 shows why that conversion can blow up
and why real solvers do it anyway.

**SQL optimisers reason about predicates symbolically.** A query planner
deciding whether two predicates on the same column can be satisfied by one row
is doing equivalence checking on small formulas.

**Static analysis and dead code detection are tautology proofs.** A branch is
dead when its condition is a contradiction. A condition is always true when it
is a tautology. Both are decidable, and both are implemented.

## The Formal Version

**Definition.** An *assignment* (or *valuation*) to a set of variables `V` is
a function from `V` to `{false, true}`. If `F` involves `n` distinct variables,
there are exactly `2ⁿ` assignments.

**Definition.** The *truth table* of `F` is the sequence of values `F` takes
over all `2ⁿ` assignments, in a fixed order. It has length `2ⁿ`.

**Definition.** `F` is a *tautology* if its truth table is all true. `F` is a
*contradiction* if its truth table is all false. `F` is *contingent* otherwise.

**Definition.** `F ≡ G` (`F` is *logically equivalent* to `G`) if their truth
tables are identical as sequences. This is the same as saying they have the same
false rows, since a row is in exactly one of the two states.

**Definition.** `F` *entails* `G`, written `F ⊨ G`, if every assignment
satisfying `F` also satisfies `G`. Equivalently, `F → G` is a tautology.
Equivalence is mutual entailment: `F ≡ G` iff `F ⊨ G` and `G ⊨ F`.

**Definition.** A *literal* is a variable or the negation of a variable.
A *disjunctive normal form* (DNF) is an OR of conjunctions of literals. A
*conjunctive normal form* (CNF) is an AND of disjunctions of literals.

**Theorem.** Every formula has a DNF and a CNF, and both are computable from
the truth table. Moreover, two formulas are equivalent if and only if their DNFs
are identical term-for-term.

*Proof sketch.* For each row where `F` is true, emit the conjunction of the
literals matching that row. That conjunction is true only on that row, so the
OR of all of them is true exactly on the rows where `F` is true. That is the
DNF, and it is correct by construction. The CNF is the dual argument over the
false rows. Since the DNF is a canonical function of the truth table, equal
truth tables give equal DNFs. ∎

**Theorem.** If `F` involves `n` variables, its DNF has at most `2ⁿ` terms.

*Proof.* One term per true row, and there are `2ⁿ` rows. ∎ This is the theorem
that makes normal forms useless in practice, and section 5 shows it happening.

## Worked Example

**The condition.** An access check someone wrote last year:

```text
if (not is_get or has_etag or not not_modified or cache_writable)
```

It is four disjuncts, three of them negated, and nobody can tell whether it is
right. The goal is to find out what it actually computes.

**Step 1. Name the variables.** There are four: `is_get`, `has_etag`,
`not_modified`, `cache_writable`. So the table has `2⁴ = 16` rows. That is small
enough to write out, which is why this example is worth doing by hand.

**Step 2. Compute each row.** Start with all four false. `not is_get` is then
true, so the whole disjunction is true. Now flip variables one at a time and
watch when the disjunction becomes false. A disjunction is false only when
*every* disjunct is false, and a negated variable is false when that variable is
true. So the row is false exactly when `is_get`, `not_modified` and
`cache_writable` are all true (making all three of those disjuncts false) and
`has_etag` is false (making the second disjunct false too).

**Step 3. Record the column.** One row out of sixteen is false. The condition is
therefore *almost* a tautology. It fails on exactly one combination:

| is_get | has_etag | not_modified | cache_writable | result |
| --- | --- | --- | --- | --- |
| T | F | T | T | **F** |

**Step 4. Read the meaning.** The check returns false precisely when the request
is a GET, has no etag, claims to be unmodified, and the cache is not writable.
Is that sensible? A GET that reports `not_modified` but has no etag is
contradictory — you cannot know a resource is unmodified without a validator. So
the row is unreachable in practice, and the condition is effectively a tautology.

**Step 5. Simplify it anyway.** Since `not is_get ∨ has_etag ∨ ¬not_modified`
already covers all but one row, and that one row is impossible, the honest
statement is: *this condition always returns true, and it should not be there at
all.* The fix is to delete it, not to simplify it.

**Step 6. Notice what the table bought you.** Without the table you would have
spent the afternoon arguing about whether `not not_modified` was a typo. With
the table you know the condition is a near-tautology, you know the exact single
input that defeats it, and you know that input is impossible. That is three
concrete facts, obtained mechanically.

**Step 7. Notice the caveat.** "Unreachable in practice" was established by
domain knowledge, not by the table. The table only told you where the false row
is. Bridging that gap is domain reasoning, and it is the part people skip.

## Runnable Code

### A formula language, and what truth tables reveal

```python
import itertools

# A formula is a syntax tree that knows how to evaluate itself under an
# assignment. Everything in this lesson follows from that one idea.


class Formula:
    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __invert__(self):
        return Not(self)


class Var(Formula):
    def __init__(self, name):
        self.name = name

    def evaluate(self, assignment):
        return assignment[self.name]

    def __repr__(self):
        return self.name


class Not(Formula):
    def __init__(self, inner):
        self.inner = inner

    def evaluate(self, assignment):
        # `not`, not `~`: ~True is -2, which makes the printed columns ugly.
        return not self.inner.evaluate(assignment)

    def __repr__(self):
        return f"~{self.inner!r}"


class And(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, assignment):
        return self.left.evaluate(assignment) and self.right.evaluate(assignment)

    def __repr__(self):
        return f"({self.left!r} & {self.right!r})"


class Or(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, assignment):
        return self.left.evaluate(assignment) or self.right.evaluate(assignment)

    def __repr__(self):
        return f"({self.left!r} | {self.right!r})"


def assignments(names):
    """Every assignment to `names`, in a fixed order."""
    return [dict(zip(names, bits))
            for bits in itertools.product([False, True], repeat=len(names))]


def column(formula, names):
    """The truth values of `formula` under every assignment to `names`."""
    return [formula.evaluate(a) for a in assignments(names)]


def as_bits(values):
    """Render a truth column as a string of 1s and 0s."""
    return "".join("1" if v else "0" for v in values)


def is_tautology(formula, names):
    """True under every assignment."""
    return all(column(formula, names))


def is_contradiction(formula, names):
    """False under every assignment."""
    return not any(column(formula, names))


def are_equivalent(f, g, names):
    """Two formulas are equivalent when they agree on every assignment."""
    return column(f, names) == column(g, names)


p, q, r = Var("p"), Var("q"), Var("r")
NAMES = ["p", "q"]

print("=" * 62)
print("1. Tautologies and contradictions")
print("=" * 62)
print()

candidates = [
    ("p | ~p", p | ~p),
    ("p & ~p", p & ~p),
    ("p & (p | q)", p & (p | q)),
    ("(p & q) -> p", ~(p & q) | p),
    ("(p | q) & ~p & ~q", (p | q) & (~p) & (~q)),
    ("p & ~p | q", (p & ~p) | q),
]

print(f"{'formula':<22} {'column':>7}  {'tautology':>10} {'contradiction':>14}")
for label, f in candidates:
    col = column(f, NAMES)
    print(f"{label:<22} {as_bits(col):>7}  {str(is_tautology(f, NAMES)):>10} "
          f"{str(is_contradiction(f, NAMES)):>14}")
print()
print("p | ~p is a tautology: true in all 4 rows.")
print("p & ~p is a contradiction: false in all 4 rows.")
print()
print("The last row is the interesting one. It is a contradiction built out of")
print("things that are individually not contradictions, because `| q` rescues")
print("the two rows where q is true. A formula is not absurd because one of its")
print("parts is; the whole formula has to be. That is the standard for dead")
print("code analysis: prove the whole condition false for some input, not that")
print("some conjunct looks silly.")

print()
print("=" * 62)
print("2. Logical equivalence")
print("=" * 62)
print()

claims = [
    ("de Morgan: ~(p & q)", ~(p & q), "~p | ~q", ~p | ~q),
    ("de Morgan: ~(p | q)", ~(p | q), "~p & ~q", ~p & ~q),
    ("idempotence: p | p", p | p, "p", p),
    ("associativity: (p|q)|r", (p | q) | r, "p|(q|r)", p | (q | r)),
    ("distributivity: p & (q|r)", p & (q | r), "(p&q)|(p&r)", (p & q) | (p & r)),
    ("absorption: p | (p & q)", p | (p & q), "p", p),
    ("double negation: ~~p", ~~p, "p", p),
]

names3 = ["p", "q", "r"]
print(f"{'claim':<24} {'left':>8} {'right':>8}  equal")
for label, left, _right_label, right in claims:
    lc, rc = column(left, names3), column(right, names3)
    print(f"{label:<24} {as_bits(lc):>8} {as_bits(rc):>8}  {lc == rc}")
print()
print("8 rows, because there are three variables. Each claim holds in every")
print("row, which is what it means for the two formulas to be equivalent.")

print()
print("=" * 62)
print("3. Simplifying a condition you actually wrote")
print("=" * 62)
print()

ugly = (p & q) | (p & ~q) | (p & q)
pretty = p
print("ugly   :", ugly)
print("pretty :", pretty)
print(f"columns: {as_bits(column(ugly, NAMES))} vs {as_bits(column(pretty, NAMES))}")
print("equivalent:", are_equivalent(ugly, pretty, NAMES))
print()
print("The ugly one is what a condition looks like after a year of patches.")
print("The truth table is how you discover that most of it was never")
print("load-bearing. Here distribution does it: p&q | p&~q = p&(q | ~q) = p.")

# A realistic one: authorising a request.
is_get = Var("is_get")
is_admin = Var("is_admin")
has_token = Var("has_token")
is_owner = Var("is_owner")
NAMES4 = ["is_get", "is_admin", "has_token", "is_owner"]

# Reads like: a GET is public; anything else needs a token AND the caller must
# own the resource, unless the caller is an admin.
authorise = (~is_get) & has_token & ((is_owner & ~is_admin) | is_admin)

# Absorption: (is_owner & ~is_admin) | is_admin  is  is_owner | is_admin.
simplified = ~is_get & has_token & (is_owner | is_admin)

print()
print("original  :", authorise)
print("simplified:", simplified)
print("equivalent:", are_equivalent(authorise, simplified, NAMES4))
print(f"original  column: {as_bits(column(authorise, NAMES4))}")
print(f"simplified col  : {as_bits(column(simplified, NAMES4))}")
print()
print("The rewrite is one application of absorption. The inner bracket")
print("(is_owner & ~is_admin) | is_admin looks conditional but is really just")
print("'is_owner or is_admin': when is_admin holds the disjunction holds")
print("regardless, and when it does not, ~is_admin already holds. So the")
print("negated factor cancels and one AND disappears.")
print()
print("The truth table is what confirms it. Reading it off the page is not")
print("reliable, and no linter will suggest this particular rewrite.")
```

### Brute-force simplification, honestly bounded

```python
import itertools


class Formula:
    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __invert__(self):
        return Not(self)


class Var(Formula):
    def __init__(self, name):
        self.name = name

    def evaluate(self, assignment):
        return assignment[self.name]

    def __repr__(self):
        return self.name


class Not(Formula):
    def __init__(self, inner):
        self.inner = inner

    def evaluate(self, assignment):
        return not self.inner.evaluate(assignment)

    def __repr__(self):
        return f"~{self.inner!r}"


class And(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, assignment):
        return self.left.evaluate(assignment) and self.right.evaluate(assignment)

    def __repr__(self):
        return f"({self.left!r} & {self.right!r})"


class Or(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, assignment):
        return self.left.evaluate(assignment) or self.right.evaluate(assignment)

    def __repr__(self):
        return f"({self.left!r} | {self.right!r})"


def column(formula, names):
    return [formula.evaluate(dict(zip(names, b)))
            for b in itertools.product([False, True], repeat=len(names))]


def search_shortest(target, names, max_depth=3):
    """Find the shallowest formula over `names` computing the same function.

    Enumerate every formula up to `max_depth` and return the first match. This
    is exhaustive proof by finite case analysis, which is what a SAT solver
    and an equivalence checker do for a living.
    """
    target_col = column(target, names)

    def matches(f):
        return column(f, names) == target_col

    for name in names:
        if matches(Var(name)):
            return Var(name)
    for name in names:
        if matches(~Var(name)):
            return ~Var(name)

    frontier = [Var(n) for n in names] + [~Var(n) for n in names]
    for _depth in range(2, max_depth + 1):
        candidates = []
        for left in frontier:
            for right in frontier:
                candidates.append(And(left, right))
                candidates.append(Or(left, right))
                candidates.append(Not(And(left, right)))
                candidates.append(Not(Or(left, right)))
        for f in candidates:
            if matches(f):
                return f
        frontier = candidates
    return None


is_get = Var("is_get")
is_admin = Var("is_admin")
has_token = Var("has_token")
is_owner = Var("is_owner")
NAMES4 = ["is_get", "is_admin", "has_token", "is_owner"]

target = (~is_get) & has_token & ((is_owner & ~is_admin) | is_admin)
found = search_shortest(target, NAMES4, max_depth=3)

print("target        :", target)
print("shortest found:", found)
print("equivalent    :", column(target, NAMES4) == column(found, NAMES4))
print()
print("Be honest about what that is: an exhaustive search over a finite space.")
print(f"With 4 variables there are {2 ** 4} rows to check, which is free.")
print(f"With 30 there are over {2 ** 30:,} rows, which is not.")
print("Nobody brute-forces a real formula. They use BDDs, SAT solvers, and")
print("algebraic rewriting instead. Lesson 82 shows how algorithm designers")
print("do the same job by hand.")
print()
print("Notice what the search returned: a formula with a NOT over the whole")
print("thing. It is genuinely equivalent, and it is genuinely worse to read")
print("than the original. 'Shortest by syntax tree depth' is not the same as")
print("'simplest to a human'. Real equivalence checkers optimise for gate")
print("count, because in hardware that is what costs money.")
```

### Normal forms

```python
import itertools


class Formula:
    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __invert__(self):
        return Not(self)


class Var(Formula):
    def __init__(self, name):
        self.name = name

    def evaluate(self, assignment):
        return assignment[self.name]

    def __repr__(self):
        return self.name


class Not(Formula):
    def __init__(self, inner):
        self.inner = inner

    def evaluate(self, assignment):
        return not self.inner.evaluate(assignment)

    def __repr__(self):
        return f"~{self.inner!r}"


class And(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, assignment):
        return self.left.evaluate(assignment) and self.right.evaluate(assignment)

    def __repr__(self):
        return f"({self.left!r} & {self.right!r})"


class Or(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, assignment):
        return self.left.evaluate(assignment) or self.right.evaluate(assignment)

    def __repr__(self):
        return f"({self.left!r} | {self.right!r})"


def assignments(names):
    return [dict(zip(names, bits))
            for bits in itertools.product([False, True], repeat=len(names))]


def column(formula, names):
    return [formula.evaluate(a) for a in assignments(names)]


def as_bits(values):
    return "".join("1" if v else "0" for v in values)


def conjoin(literals):
    result = literals[0]
    for literal in literals[1:]:
        result = And(result, literal)
    return result


def disjoin(literals):
    result = literals[0]
    for literal in literals[1:]:
        result = Or(result, literal)
    return result


def to_dnf(formula, names):
    """Disjunctive normal form: an OR of AND-terms of literals.

    Built by reading the truth table. Each row where the formula is true
    contributes one AND-term naming the values that made it true.
    """
    terms = []
    for assignment in assignments(names):
        if formula.evaluate(assignment):
            terms.append([Var(n) if assignment[n] else ~Var(n) for n in names])
    return terms


def dnf_to_formula(terms):
    if not terms:
        return And(Var("p"), ~Var("p"))       # the contradiction, written out
    return disjoin([conjoin(term) for term in terms])


def to_cnf(formula, names):
    """Conjunctive normal form: an AND of OR-clauses of literals.

    The dual idea: each row where the formula is FALSE contributes one OR
    clause saying "not all of these held at once".
    """
    clauses = []
    for assignment in assignments(names):
        if not formula.evaluate(assignment):
            clauses.append([~Var(n) if assignment[n] else Var(n) for n in names])
    return clauses


def cnf_to_formula(clauses):
    if not clauses:
        return Or(Var("p"), ~Var("p"))        # the tautology, written out
    return conjoin([disjoin(clause) for clause in clauses])


a, b, c, d = Var("p"), Var("q"), Var("r"), Var("s")

examples = [
    (a & (b | c), ["p", "q", "r"]),
    ((a | b) & (c | d), ["p", "q", "r", "s"]),
    (~(a & b) | c, ["p", "q", "r"]),
]

for formula, names in examples:
    print(f"formula: {formula}")
    dnf_terms = to_dnf(formula, names)
    dnf_back = dnf_to_formula(dnf_terms)
    cnf_clauses = to_cnf(formula, names)
    cnf_back = cnf_to_formula(cnf_clauses)
    print(f"  DNF: {len(dnf_terms)} AND-terms of {len(names)} literals"
          f" -> {dnf_back}")
    print(f"  CNF: {len(cnf_clauses)} OR-clauses of {len(names)} literals"
          f" -> {cnf_back}")
    print(f"  DNF equivalent: {column(formula, names) == column(dnf_back, names)}")
    print(f"  CNF equivalent: {column(formula, names) == column(cnf_back, names)}")
    print()

print("Every formula has both. Note the second example: a four-variable formula")
print("that fits on one line becomes a nine-term DNF. That is the whole catch")
print("with normal forms. They are canonical, which is what makes them useful")
print("for comparing two formulas, and exponential, which is what makes them")
print(f"useless on big inputs. 30 variables gives up to {2 ** 30:,} terms.")
print()
print("DNF is the natural shape for 'which combinations of facts make this")
print("true', which is how rule engines, database query planners and")
print("spreadsheet dependency trees all think. CNF is what SAT solvers consume,")
print("which is why clause-based solving works so well.")
```

### Why this is what a compiler does

```python
class Formula:
    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __invert__(self):
        return Not(self)


class Var(Formula):
    def __init__(self, name):
        self.name = name

    def evaluate(self, assignment):
        return assignment[self.name]

    def __repr__(self):
        return self.name


class Not(Formula):
    def __init__(self, inner):
        self.inner = inner

    def evaluate(self, assignment):
        return not self.inner.evaluate(assignment)

    def __repr__(self):
        return f"~{self.inner!r}"


class And(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, assignment):
        return self.left.evaluate(assignment) and self.right.evaluate(assignment)

    def __repr__(self):
        return f"({self.left!r} & {self.right!r})"


class Or(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, assignment):
        return self.left.evaluate(assignment) or self.right.evaluate(assignment)

    def __repr__(self):
        return f"({self.left!r} | {self.right!r})"


print("A hardware circuit is a formula in the AND, OR and NOT gates. To build")
print("one you need the truth table; to shrink one you need simplification.")
print("Same pipeline as above, with gates instead of operators.")
print()

print(f"{'a':>4} {'b':>4} {'and':>5} {'or':>4} {'nand':>6} {'nor':>5}")
for a_val, b_val in [(False, False), (False, True), (True, False), (True, True)]:
    assignment = {"a": a_val, "b": b_val}
    a_gate, b_gate = Var("a"), Var("b")
    and_gate = And(a_gate, b_gate)
    or_gate = Or(a_gate, b_gate)
    print(f"{str(a_val):>4} {str(b_val):>4} "
          f"{str(and_gate.evaluate(assignment)):>5} "
          f"{str(or_gate.evaluate(assignment)):>4} "
          f"{str(Not(and_gate).evaluate(assignment)):>6} "
          f"{str(Not(or_gate).evaluate(assignment)):>5}")
print()
print("NAND is ~(a & b) and NOR is ~(a | b). De Morgan rewrites both using only")
print("NOT: ~(a & b) = ~a | ~b, and ~(a | b) = ~a & ~b.")
print()
print("So a machine built only from NAND gates can build anything: NOT x is")
print("NAND(x, x), AND is NAND followed by NOT, and OR is De Morgan plus AND.")
print("NAND is the universal gate, which is why the first commercial integrated")
print("circuits were built from it.")
print()
print("Software does the same thing with short-circuit evaluation, which is why")
print("`x != 0 and 10 / x > 1` works in Python while `10 / x > 1 and x != 0`")
print("raises ZeroDivisionError. The order of the operands in the formula is")
print("the order of evaluation in the machine.")
```

## Common Mistakes

**Wrong: "the truth table has to be written out by hand."**
Right: with `n` variables it has `2ⁿ` rows, so it is only feasible by hand up to
about four or five variables. Beyond that, enumerate programmatically, or use a
SAT solver or a BDD. What the table gives you is a *complete* answer, which is
what makes it valuable, not the fact that you can afford to write it out.
Why tempting: drawing the table is how every textbook introduces it, and the
first few tables are genuinely small enough to draw. The habit does not survive
contact with real formulas, which have dozens of variables.

**Wrong: concluding two formulas are equivalent because they "look similar".**
Right: equivalence is a claim about all `2ⁿ` rows, and similarity is not
evidence. `p & q | p & ~q` and `p` are similar and equivalent; `p & q | p & ~r`
and `p` are similar and not. The check costs one comparison of two columns, so
there is no reason to skip it.
Why tempting: pattern-matching on structure is fast and usually right for the
first few formulas you meet, which teaches you to trust it for the ones where it
is not.

**Wrong: using DNF to simplify a large formula.**
Right: DNF is canonical, which is exactly why it is bad at simplification. Two
equivalent formulas can have the same DNF and wildly different sizes, so
converting to DNF to compare is right and converting to DNF to shrink is
backwards. Use the algebraic rules — De Morgan, distribution, absorption — for
shrinking, and the normal form only for deciding equivalence.
Why tempting: it feels rigorous. It is rigorous and it is the wrong tool, which
is a combination that catches people out.

**Wrong: treating a tautology as a good condition.**
Right: `p | ~p` is a tautology, and that means it is always true, which means it
is a condition that never does anything. A tautology is a bug report, not a
feature. The worked example is exactly this: a four-disjunct condition that turns
out to be a near-tautology and should be deleted.
Why tempting: tautologies feel like safety. "The check can never fail" reads as
robustness until you notice the check was there to reject something.

**Wrong: believing that two formulas with the same truth table should be written
the same way.**
Right: the table determines behaviour, not syntax. The brute-force search in the
code above returns a formula with a `NOT` wrapped around the whole expression,
which is equivalent and noticeably harder to read. Equivalence checking tools
optimise for gate count, because in hardware that is the cost that matters, and
optimising for gate count is not the same as optimising for readability.
Why tempting: "equivalent" gets read as "the same", and once two things are
called the same you stop expecting them to look different.

## Exercises and Solutions

**[ ] Exercise 1 — Classify twelve formulas and find the dead-branch pattern.**
For each formula below over `p` and `q`, compute the truth column over
`(p,q) = FF, FT, TF, TT`, classify it, and say whether it is equivalent to `p`,
to `q`, to `p | q`, or to none of those. Then write one sentence of English
saying exactly when it is true.

1. `p | q`
2. `p ∧ q`
3. `p | ¬q`
4. `¬(p ∨ q)`
5. `p | (q ∧ ¬p)`
6. `(p ∧ ¬q) ∨ (¬p ∧ q)`
7. `p ∧ ¬q`
8. `(p ∨ q) ∧ ¬(p ∧ q)`
9. `p | (p ∧ q)`
10. `¬(p ∧ ¬p)`
11. `(p ∨ q) ∧ (p ∨ ¬q)`
12. `¬p | ¬q`

<details>
<summary>Solution</summary>

```python
import itertools


class Formula:
    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __invert__(self):
        return Not(self)


class Var(Formula):
    def __init__(self, name):
        self.name = name

    def evaluate(self, a):
        return a[self.name]

    def __repr__(self):
        return self.name


class Not(Formula):
    def __init__(self, inner):
        self.inner = inner

    def evaluate(self, a):
        return not self.inner.evaluate(a)

    def __repr__(self):
        return f"~{self.inner!r}"


class And(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, a):
        return self.left.evaluate(a) and self.right.evaluate(a)

    def __repr__(self):
        return f"({self.left!r} & {self.right!r})"


class Or(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, a):
        return self.left.evaluate(a) or self.right.evaluate(a)

    def __repr__(self):
        return f"({self.left!r} | {self.right!r})"


p, q = Var("p"), Var("q")
NAMES = ["p", "q"]
ROWS = [dict(zip(NAMES, b)) for b in itertools.product([False, True], repeat=2)]
TARGETS = {"p": p, "q": q, "p | q": p | q}

ITEMS = [
    ("p | q", p | q),
    ("p & q", p & q),
    ("p | ~q", p | ~q),
    ("~(p | q)", ~(p | q)),
    ("p | (q & ~p)", p | (q & ~p)),
    ("(p & ~q) | (~p & q)", (p & ~q) | (~p & q)),
    ("p & ~q", p & ~q),
    ("(p | q) & ~(p & q)", (p | q) & ~(p & q)),
    ("p | (p & q)", p | (p & q)),
    ("~(p & ~p)", ~(p & ~p)),
    ("(p | q) & (p | ~q)", (p | q) & (p | ~q)),
    ("~p | ~q", ~p | ~q),
]

ENGLISH = [
    "true when at least one holds",
    "true when both hold",
    "true when p holds, or when q does not; false only when p is false and q true",
    "true when neither holds",
    "true when p holds, or when q holds and p does not",
    "true when exactly one holds; this is exclusive-or",
    "true when p holds and q does not",
    "true when at least one holds but not both; exclusive-or again",
    "true when p holds; the second disjunct needs p, so it can never fire",
    "always true, because p & ~p is always false",
    "true when p holds; the second conjunct needs q & ~q, so it can never fire",
    "true when at least one of them fails; this is NOT (p & q)",
]


def column(f):
    return [f.evaluate(a) for a in ROWS]


def bits(values):
    return "".join("1" if v else "0" for v in values)


def classify(col):
    if all(col):
        return "tautology"
    if not any(col):
        return "contradiction"
    return "contingent"


def match_target(col):
    for label, formula in TARGETS.items():
        if col == column(formula):
            return label
    return "none"


print(f"{'#':>2} {'formula':<24} {'column':>7} {'kind':<13} {'same as':<8}")
for i, ((label, f), english) in enumerate(zip(ITEMS, ENGLISH), 1):
    col = column(f)
    print(f"{i:>2} {label:<24} {bits(col):>7} {classify(col):<13} "
          f"{match_target(col):<8}")

print()
print("English, one line each:")
for i, english in enumerate(ENGLISH, 1):
    print(f"{i:>2} {english}")

print()
print("=" * 70)
print("The dead-branch pattern")
print("=" * 70)
print()
print("Items 9 and 11 both simplify to plain `p`, and in both the simplification")
print("deletes a conjunct that can never change the answer:")
print()
print("  9:  p | (p & q)      the second disjunct requires p, and the first")
print("                        disjunct already gives the answer when p holds")
print("  11: (p|q) & (p|~q)   the second conjunct requires q & ~q, which is")
print("                        never true, so it can never make the AND true")
print()

for label, f in [("p | (p & q)", ITEMS[8][1]),
                 ("(p | q) & (p | ~q)", ITEMS[10][1]),
                 ("p | (p & ~q)", p | (p & ~q)),
                 ("p & (p | q)", p & (p | q))]:
    print(f"  {label:<20} column {bits(column(f))}   == p    column "
          f"{bits(column(p))}   equal: {column(f) == column(p)}")
print()
print("All four collapse to `p`. Absorption covers the first and the last two:")
print("`x | (x & y) = x` and `x & (x | y) = x`. Item 11 is the mirror image,")
print("distributing gives `(p&q) | (p&~q) = p`, which is item 9's shape again.")
print()
print("This is the commonest dead branch in real code. A condition grows a")
print("conjunct that can never change the result, nobody notices because it")
print("never causes a bug, and two years later nobody can delete it without")
print("running the tests.")
```

Output:

```
 # formula                   column kind          same as 
 1 p | q                       0111 contingent    p | q   
 2 p & q                       0001 contingent    none    
 3 p | ~q                      1011 contingent    none    
 4 ~(p | q)                    1000 contingent    none    
 5 p | (q & ~p)                0111 contingent    p | q   
 6 (p & ~q) | (~p & q)         0110 contingent    none    
 7 p & ~q                      0010 contingent    none    
 8 (p | q) & ~(p & q)          0110 contingent    none    
 9 p | (p & q)                 0011 contingent    p       
10 ~(p & ~p)                   1111 tautology     none    
11 (p | q) & (p | ~q)          0011 contingent    p       
12 ~p | ~q                     1110 contingent    none    

English, one line each:
 1 true when at least one holds
 2 true when both hold
 3 true when p holds, or when q does not; false only when p is false and q true
 4 true when neither holds
 5 true when p holds, or when q holds and p does not
 6 true when exactly one holds; this is exclusive-or
 7 true when p holds and q does not
 8 true when at least one holds but not both; exclusive-or again
 9 true when p holds; the second disjunct needs p, so it can never fire
10 always true, because p & ~p is always false
11 true when p holds; the second conjunct needs q & ~q, so it can never fire
12 true when at least one of them fails; this is NOT (p & q)

======================================================================
The dead-branch pattern
======================================================================

Items 9 and 11 both simplify to plain `p`, and in both the simplification
deletes a conjunct that can never change the answer:

  9:  p | (p & q)      the second disjunct requires p, and the first
                        disjunct already gives the answer when p holds
  11: (p|q) & (p|~q)   the second conjunct requires q & ~q, which is
                        never true, so it can never make the AND true

  p | (p & q)          column 0011   == p    column 0011   equal: True
  (p | q) & (p | ~q)   column 0011   == p    column 0011   equal: True
  p | (p & ~q)         column 0011   == p    column 0011   equal: True
  p & (p | q)          column 0011   == p    column 0011   equal: True

All four collapse to `p`. Absorption covers the first and the last two:
`x | (x & y) = x` and `x & (x | y) = x`. Item 11 is the mirror image,
distributing gives `(p&q) | (p&~q) = p`, which is item 9's shape again.

This is the commonest dead branch in real code. A condition grows a
conjunct that can never change the result, nobody notices because it
never causes a bug, and two years later nobody can delete it without
running the tests.
```

The `same as` column is the one worth reading twice. Items 5, 9 and 11 all
reduce to something already on the list, and item 12's column is the reverse of
item 2's with no match, which is exactly what De Morgan predicts. Item 10 is the
only tautology and its column is `1111`, meaning it can never reject anything. A
tautology used as a condition is a bug report, not a safety net.

</details>

**[ ] Exercise 2 — Minimise a real condition and find a refactor that breaks it.**
Start from this cache-validation check:

```text
if (not is_get) or (is_get and has_etag) or (not is_get and not has_etag):
```

(a) Write the truth column over `is_get` and `has_etag`. (b) Simplify it by hand
and confirm with the column. (c) A reviewer suggests moving the negation:
`if not is_get or not has_etag:`. Show that this is *not* equivalent and give the
witness row. Then consider a second, shorter suggestion, `if not has_etag:`,
and explain which of the two is more dangerous. (d) Run your brute-force search
from the Runnable Code section on the original with a budget of 1, then 2, then 3
connectives, and report what it finds at each. Say whether you would ship the
answer it gives.

<details>
<summary>Solution</summary>

```python
import itertools


class Formula:
    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __invert__(self):
        return Not(self)


class Var(Formula):
    def __init__(self, name):
        self.name = name

    def evaluate(self, a):
        return a[self.name]

    def __repr__(self):
        return self.name


class Not(Formula):
    def __init__(self, inner):
        self.inner = inner

    def evaluate(self, a):
        return not self.inner.evaluate(a)

    def __repr__(self):
        return f"~{self.inner!r}"


class And(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, a):
        return self.left.evaluate(a) and self.right.evaluate(a)

    def __repr__(self):
        return f"({self.left!r} & {self.right!r})"


class Or(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, a):
        return self.left.evaluate(a) or self.right.evaluate(a)

    def __repr__(self):
        return f"({self.left!r} | {self.right!r})"


is_get = Var("is_get")
has_etag = Var("has_etag")
NAMES = ["is_get", "has_etag"]
ROWS = [dict(zip(NAMES, b)) for b in itertools.product([False, True], repeat=2)]


def column(f):
    return [f.evaluate(a) for a in ROWS]


def bits(values):
    return "".join("1" if v else "0" for v in values)


def show(label, f):
    print(label)
    for a in ROWS:
        print(f"    is_get={str(a['is_get']):<5} has_etag={str(a['has_etag']):<5}"
              f"  ->  {str(f.evaluate(a)):>5}")
    print(f"    column: {bits(column(f))}")
    print()


original = (~is_get) | (is_get & has_etag) | (~is_get & ~has_etag)
simplified = ~is_get | has_etag
equivalent_refactor = ~is_get | ~has_etag
careless_refactor = ~has_etag

print("(a) the original condition")
show("  not is_get or (is_get and has_etag) or (not is_get and not has_etag):",
     original)

print("(b) the simplification")
show("  not is_get or has_etag:", simplified)
print(f"  equivalent: {column(original) == column(simplified)}")
print()
print("  Why: the third disjunct, `not is_get and not has_etag`, is entirely")
print("  covered by the first, `not is_get`, so it is dead. What is left is")
print("  `not is_get or (is_get and has_etag)`, and distributing ~is_get over")
print("  the conjunction gives `not is_get or has_etag`: either the first")
print("  disjunct holds and we are done, or is_get holds, in which case the")
print("  first disjunct is false and we need has_etag.")
print()

print("(c) two refactors, one safe and one not")
print()
show("  not is_get or not has_etag   (De Morgan with the negation moved):",
     equivalent_refactor)
print(f"  equivalent to the original: "
      f"{column(original) == column(equivalent_refactor)}")
print()
print("  This is the De Morgan trap from Lesson 10, in its purest form. The")
print("  simplified form is `not (is_get and not has_etag)`. Applying De Morgan")
print("  correctly gives `not is_get or has_etag`, which is where we started.")
print("  Moving the negation to the wrong side gives `not is_get or not")
print("  has_etag`, which is NOT the same function: the column changes from")
print("  1101 to 1110, and the third row flips from False to True. Two rows")
print("  differ and no reviewer reading either line would notice.")
print()

show("  not has_etag   (someone dropped the is_get branch):", careless_refactor)
print(f"  equivalent to the original: "
      f"{column(original) == column(careless_refactor)}")
print()
for a in ROWS:
    if original.evaluate(a) != careless_refactor.evaluate(a):
        print(f"  witness: is_get={a['is_get']}, has_etag={a['has_etag']}")
        print(f"    original : {str(original.evaluate(a)):>5}"
              f"   -> no revalidation needed, a POST is never cached")
        print(f"    careless : {str(careless_refactor.evaluate(a)):>5}"
              f"   -> revalidate a response that was never cacheable")
        break
print()
print("  Dropping the is_get branch is the mistake nobody notices, because the")
print("  surviving condition is short and reads sensibly on its own. The")
print("  witness row is a POST that already has a validator: the original says")
print("  no revalidation is needed, and the refactor forces one. Every POST")
print("  with an etag revalidates forever, for no reason.")
print()


def search_by_connective_count(target, max_connectives):
    """Return the smallest formula computing `target` within the budget."""
    target_col = column(target)

    def count(f):
        if isinstance(f, Var):
            return 0
        if isinstance(f, Not):
            return count(f.inner) + 1
        return count(f.left) + count(f.right) + 1

    def matches(f):
        return column(f) == target_col

    level = [is_get, has_etag, ~is_get, ~has_etag]
    for f in level:
        if matches(f):
            return f
    while True:
        nxt = []
        for left in level:
            for right in level:
                for f in (And(left, right), Or(left, right),
                          Not(And(left, right)), Not(Or(left, right))):
                    if count(f) > max_connectives:
                        continue
                    nxt.append(f)
                    if matches(f):
                        return f
        if not nxt:
            return None
        level = nxt


print("(d) brute-force search, increasing budget")
print()
for budget in (1, 2, 3):
    found = search_by_connective_count(original, budget)
    if found is None:
        print(f"  budget {budget}: nothing found")
    else:
        print(f"  budget {budget}: {found}   column {bits(column(found))}   "
              f"equivalent {column(found) == column(original)}")
print()
print("  The hand-simplified form turns up at a budget of 2 connectives, so")
print("  nothing smaller exists. The search finds nothing that careful reading")
print("  of the algebra did not already give you, which is the reassuring")
print("  outcome: brute force and understanding agree here.")
print()
print("  At budget 3 it returns a formula with a NOT wrapped round the whole")
print("  thing. It is equivalent, and it is worse to read than the original,")
print("  because nothing in it says 'a GET needs a validator'.")
print()
print("  Would I ship the searched one? No. Minimise for the machine in")
print("  hardware, where gate count is money; optimise for the human in code,")
print("  where the reading cost is paid again on every future change.")
```

Output:

```
(a) the original condition
  not is_get or (is_get and has_etag) or (not is_get and not has_etag):
    is_get=False has_etag=False  ->   True
    is_get=False has_etag=True   ->   True
    is_get=True  has_etag=False  ->  False
    is_get=True  has_etag=True   ->   True
    column: 1101

(b) the simplification
  not is_get or has_etag:
    is_get=False has_etag=False  ->   True
    is_get=False has_etag=True   ->   True
    is_get=True  has_etag=False  ->  False
    is_get=True  has_etag=True   ->   True
    column: 1101

  equivalent: True

  Why: the third disjunct, `not is_get and not has_etag`, is entirely
  covered by the first, `not is_get`, so it is dead. What is left is
  `not is_get or (is_get and has_etag)`, and distributing ~is_get over
  the conjunction gives `not is_get or has_etag`: either the first
  disjunct holds and we are done, or is_get holds, in which case the
  first disjunct is false and we need has_etag.

(c) two refactors, one safe and one not

  not is_get or not has_etag   (De Morgan with the negation moved):
    is_get=False has_etag=False  ->   True
    is_get=False has_etag=True   ->   True
    is_get=True  has_etag=False  ->   True
    is_get=True  has_etag=True   ->  False
    column: 1110

  equivalent to the original: False

  This is the De Morgan trap from Lesson 10, in its purest form. The
  simplified form is `not (is_get and not has_etag)`. Applying De Morgan
  correctly gives `not is_get or has_etag`, which is where we started.
  Moving the negation to the wrong side gives `not is_get or not
  has_etag`, which is NOT the same function: the column changes from
  1101 to 1110, and the third row flips from False to True. Two rows
  differ and no reviewer reading either line would notice.

  not has_etag   (someone dropped the is_get branch):
    is_get=False has_etag=False  ->   True
    is_get=False has_etag=True   ->  False
    is_get=True  has_etag=False  ->   True
    is_get=True  has_etag=True   ->  False
    column: 1010

  equivalent to the original: False

  witness: is_get=False, has_etag=True
    original :  True   -> no revalidation needed, a POST is never cached
    careless : False   -> revalidate a response that was never cacheable

  Dropping the is_get branch is the mistake nobody notices, because the
  surviving condition is short and reads sensibly on its own. The
  witness row is a POST that already has a validator: the original says
  no revalidation is needed, and the refactor forces one. Every POST
  with an etag revalidates forever, for no reason.

(d) brute-force search, increasing budget

  budget 1: nothing found
  budget 2: (has_etag | ~is_get)   column 1101   equivalent True
  budget 3: ~(is_get & ~has_etag)   column 1101   equivalent True

  The hand-simplified form turns up at a budget of 2 connectives, so
  nothing smaller exists. The search finds nothing that careful reading
  of the algebra did not already give you, which is the reassuring
  outcome: brute force and understanding agree here.

  At budget 3 it returns a formula with a NOT wrapped round the whole
  thing. It is equivalent, and it is worse to read than the original,
  because nothing in it says 'a GET needs a validator'.

  Would I ship the searched one? No. Minimise for the machine in
  hardware, where gate count is money; optimise for the human in code,
  where the reading cost is paid again on every future change.
```

Part (c) is Lesson 10's De Morgan trap in its purest form. The simplified form
is `not (is_get and not has_etag)`, and applying De Morgan correctly gives back
`not is_get or has_etag`, which is where we started. Moving the negation to the
other side gives a column of `1110` instead of `1101`, and no reviewer reading
either line would notice.

The shorter suggestion is more dangerous for a different reason. `not has_etag`
is not a mistaken rewrite at all; it is a plausible reading of the requirement
by someone who decided the `is_get` branch was noise. It is also *shorter*, so
it survives review more easily, and it silently revalidates every POST forever.
Bugs that look like simplifications are harder to find than bugs that look like
typos, because everyone stops looking once the line looks tidy.

</details>

**[ ] Exercise 3 — Write a constant-condition checker, and be honest about what
it cannot do.** Using `ast` from the standard library, write a checker that finds
every `if` in a Python source string whose condition is a constant `True` or a
constant `False`, where the condition is a boolean expression over names,
`True`, `False`, `not`, `and`, `or` and parentheses. Your checker must (a) do
constant folding so that `x or True` is reported as `True` even when `x` is a
function parameter, and (b) report "I do not know" rather than guessing whenever
the condition contains a comparison or a call. Run it on a source string
containing at least six conditions, including `True or (x and False)`,
`False and (not (True or x))`, `a or not a`, `a and b and not b`, `x > 0 or
x <= 0`, and `len(str(x)) > 0`. Then explain, in terms of domains, why the last
two are out of reach, and list the three techniques real static analysers use
instead.

<details>
<summary>Solution</summary>

```python
import ast
import itertools

# ---------------------------------------------------------------------------
# A constant-condition checker. Built on ast, which is in the standard library,
# so this is a real parser rather than a regex.
# ---------------------------------------------------------------------------

VARS = ["a", "b", "c"]


def constant_value(node, assignment):
    """Evaluate a boolean AST node under one assignment.

    Returns True, False, or None. None means 'depends on something I cannot
    see', which is the honest answer for comparisons and function calls.
    """
    if isinstance(node, ast.Constant):
        return node.value if isinstance(node.value, bool) else None
    if isinstance(node, ast.Name):
        return assignment.get(node.id)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        inner = constant_value(node.operand, assignment)
        return None if inner is None else not inner
    if isinstance(node, ast.BoolOp):
        values = [constant_value(v, assignment) for v in node.values]
        if any(v is None for v in values):
            return None
        return all(values) if isinstance(node.op, ast.And) else any(values)
    return None                      # Compare, Call, anything else


def all_assignments():
    return [dict(zip(VARS, bits))
            for bits in itertools.product([False, True], repeat=len(VARS))]


def classify_condition(node):
    """True if always taken, False if never taken, else None."""
    seen = set()
    for assignment in all_assignments():
        value = constant_value(node, assignment)
        if value is None:
            return None
        seen.add(value)
    return seen.pop() if len(seen) == 1 else None


def fold(node):
    """Constant-fold a boolean AST bottom-up.

    Returns Python True, Python False, or a (possibly rewritten) AST node.
    Sound, and completely independent of the values any variable takes.
    """
    if isinstance(node, ast.Constant) and isinstance(node.value, bool):
        return node.value
    if isinstance(node, ast.Name):
        return node
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        inner = fold(node.operand)
        if inner is True or inner is False:
            return not inner
        return ast.UnaryOp(op=ast.Not(), operand=inner)
    if isinstance(node, ast.BoolOp):
        is_and = isinstance(node.op, ast.And)
        values = [fold(v) for v in node.values]
        if is_and and any(v is False for v in values):
            return False                      # x and False = False
        if (not is_and) and any(v is True for v in values):
            return True                       # x or True = True
        survivors = [v for v in values if v is not True and v is not False]
        if not survivors:
            return is_and                     # True and True, False or False
        if len(survivors) == 1:
            return survivors[0]
        return ast.BoolOp(op=node.op, values=survivors)
    return node                              # Compare, Call, anything else


def classify_with_fallback(node):
    """Exact if possible, otherwise report what constant folding gives."""
    folded = fold(node)
    if folded is True or folded is False:
        return folded, "constant folding"
    verdict = classify_condition(folded)
    if verdict is not None:
        return verdict, "exact"
    return None, "depends on its variables"


SOURCE = '''
import math

TAU = 2 * math.pi


def handler(x, a, b, c):
    if True or (x and False):
        return "dead else-branch"
    if False and (not (True or x)):
        return "dead body"
    if a or not a:
        return "always taken"
    if a and b and not b:
        return "simplifiable, but genuinely constant false"
    if x > 0 or x <= 0:
        return "tautology over the integers, invisible to a boolean checker"
    if len(str(x)) > 0:
        return "depends on a function call"
    return "fallthrough"
'''

tree = ast.parse(SOURCE)

print("=" * 76)
print("condition analysis")
print("=" * 76)
print()

for node in ast.walk(tree):
    if not isinstance(node, ast.If):
        continue
    source = ast.unparse(node.test)
    verdict, reason = classify_with_fallback(node.test)
    shown = "depends" if verdict is None else str(verdict)
    print(f"  line {node.lineno:<3} {source:<28} {shown:<8} {reason}")

print()
print("=" * 76)
print("What each verdict means for a reviewer")
print("=" * 76)
print()
print("  'always taken' on `a or not a`: the else branch is dead, and anything")
print("  after an early return inside it is dead. That is the reachability")
print("  question from Lesson 10's Challenge, and the answer is a bug report.")
print()
print("  'dead body' on `False and (not (True or x))`: the whole body never")
print("  runs. No test suite will catch this. A test that exercises the dead")
print("  body fails for a reason you blame on the test; a test that avoids it")
print("  proves nothing.")
print()
print("  The last two are the interesting failures. `x > 0 or x <= 0` is a")
print("  tautology over the integers and `len(str(x)) > 0` is true over every")
print("  type, but a checker that understands only booleans cannot tell, and")
print("  reporting 'depends' is the correct thing for it to do.")
print()

print("=" * 76)
print("Why the general case is out of reach")
print("=" * 76)
print()
print("The checker works because its conditions contain only names ranging over")
print("{True, False} plus the four connectives, so there are 2^3 = 8 rows to")
print("enumerate. Two things break that immediately.")
print()
print("Values rather than booleans. `x > 0 or x <= 0` is true for every")
print("integer x, and `x != 0 or x == 0` is true for every value of every type.")
print("Settling those means reasoning about the domain of x, and the domain of")
print("`str` contains values no program will ever construct. There is no finite")
print("table to build, so there is nothing to enumerate.")
print()
print("Calls. `is_valid(user)` and `user.permissions.can('write')` depend on")
print("code elsewhere and sometimes on the network, the clock or a database.")
print("Deciding them is undecidable in general, which is why every real static")
print("analyser is conservative and says 'I do not know' rather than guessing. A")
print("wrong 'dead' verdict deletes working code, so the safe answer is the")
print("useless one.")
print()
print("The three techniques real tools use instead.")
print()
print("  1. Constant folding, which is sound and is the first pass. `x or True`")
print("     is True and `x and False` is False whatever x is. That is what the")
print("     `fold` function above does, and it is why it can settle the first")
print("     two conditions without enumerating anything.")
print("  2. SAT solving. Convert the whole path condition to a formula and ask")
print("     whether it is satisfiable. If not, the path is infeasible and the")
print("     code after it is dead. This scales to dozens of variables, which is")
print("     why SAT rather than symbolic execution alone is the standard tool")
print("     for dead code detection.")
print("  3. Whole-program summaries. Infer that len() returns a non-negative")
print("     integer, and `x >= 0` becomes constant. This is how the `x > 0` case")
print("     above would actually be settled in a real analyser.")
print()
print("The truth table is the foundation and SAT solving is the scale-up. The")
print("logic is identical; only the search is different.")
```

Output:

```
============================================================================
condition analysis
============================================================================

  line 8   True or (x and False)        True     constant folding
  line 10  False and (not (True or x))  False    constant folding
  line 12  a or not a                   True     exact
  line 14  a and b and (not b)          False    exact
  line 16  x > 0 or x <= 0              depends  depends on its variables
  line 18  len(str(x)) > 0              depends  depends on its variables

============================================================================
What each verdict means for a reviewer
============================================================================

  'always taken' on `a or not a`: the else branch is dead, and anything
  after an early return inside it is dead. That is the reachability
  question from Lesson 10's Challenge, and the answer is a bug report.

  'dead body' on `False and (not (True or x))`: the whole body never
  runs. No test suite will catch this. A test that exercises the dead
  body fails for a reason you blame on the test; a test that avoids it
  proves nothing.

  The last two are the interesting failures. `x > 0 or x <= 0` is a
  tautology over the integers and `len(str(x)) > 0` is true over every
  type, but a checker that understands only booleans cannot tell, and
  reporting 'depends' is the correct thing for it to do.

============================================================================
Why the general case is out of reach
============================================================================

The checker works because its conditions contain only names ranging over
{True, False} plus the four connectives, so there are 2^3 = 8 rows to
enumerate. Two things break that immediately.

Values rather than booleans. `x > 0 or x <= 0` is true for every
integer x, and `x != 0 or x == 0` is true for every value of every type.
Settling those means reasoning about the domain of x, and the domain of
`str` contains values no program will ever construct. There is no finite
table to build, so there is nothing to enumerate.

Calls. `is_valid(user)` and `user.permissions.can('write')` depend on
code elsewhere and sometimes on the network, the clock or a database.
Deciding them is undecidable in general, which is why every real static
analyser is conservative and says 'I do not know' rather than guessing. A
wrong 'dead' verdict deletes working code, so the safe answer is the
useless one.

The three techniques real tools use instead.

  1. Constant folding, which is sound and is the first pass. `x or True`
     is True and `x and False` is False whatever x is. That is what the
     `fold` function above does, and it is why it can settle the first
     two conditions without enumerating anything.
  2. SAT solving. Convert the whole path condition to a formula and ask
     whether it is satisfiable. If not, the path is infeasible and the
     code after it is dead. This scales to dozens of variables, which is
     why SAT rather than symbolic execution alone is the standard tool
     for dead code detection.
  3. Whole-program summaries. Infer that len() returns a non-negative
     integer, and `x >= 0` becomes constant. This is how the `x > 0` case
     above would actually be settled in a real analyser.

The truth table is the foundation and SAT solving is the scale-up. The
logic is identical; only the search is different.
```

Two verdicts deserve attention. Line 8 is settled by constant folding alone, with
no enumeration, because `True or anything` is `True` and `False and anything` is
`False`. That is the technique that scales, and it is the first pass every real
analyser runs. Line 14 is settled exactly, by enumerating all eight assignments,
and that is the technique that stops scaling past about a dozen names.

The `a and b and not b` verdict is worth pausing on, because "constant: False"
looks wrong and is right. The condition simplifies to `a`, which is not
constant, so the exact check reports False. The exact check asks "is this always
the same value?" and for this formula the answer is yes: when `a` is True the
conjunct `b and not b` kills it, and when `a` is False the whole thing is False.
The condition really is always False, which means the body is genuinely dead.

</details>
**Challenge — Build a BDD-backed equivalence checker and find its limits.** A
*reduced ordered binary decision diagram* (ROBDD) is a canonical representation
of a boolean function: you push the truth table into a binary tree that branches
on variables in a fixed order, merging nodes that compute the same thing.
Two functions have the same diagram if and only if they are equivalent. Write a
`BDD` class with `node`, `variable`, `neg`, `apply`, `size`, and `count_true`,
then show (a) that `count_true` agrees with brute force on four small
functions, (b) that `(p|q) & (r|s)` and `(p&r)|(p&s)|(q&r)|(q&s)` produce the
identical node, (c) that a function with 65 variables and a DNF of over 10³⁶
terms needs only 65 nodes, and (d) that the *same* function with a *bad* variable
order needs exponentially more. Part (d) is the point of the exercise.

<details>
<summary>Solution</summary>

```python
import itertools

# ---------------------------------------------------------------------------
# A reduced ordered binary decision diagram (ROBDD).
#
# A node is either a terminal (TRUE or FALSE) or an interior node branching on
# one variable. Two rules give canonical form:
#   merge  -- one subfunction gets one node, however often it is reached
#   reduce -- if both children of a node are equal, replace it by that child
# Because the form is canonical, two functions have the same diagram if and
# only if they are the same boolean function. Diagram identity IS equivalence.
# ---------------------------------------------------------------------------

TRUE = "T"
FALSE = "F"


class BDD:
    def __init__(self, order):
        self.order = list(order)
        self.nodes = {}          # id -> (var_index, low_id, high_id)
        self.unique = {}         # (var_index, low, high) -> id
        self.counter = 0
        self.cache = {}          # (op, u, v) -> id, memo for apply()

    # --- construction ----------------------------------------------------
    def node(self, var_index, low, high):
        """Create or reuse a node. Rule 2: equal children collapse."""
        if low == high:
            return low
        key = (var_index, low, high)
        if key not in self.unique:
            self.unique[key] = self.counter
            self.nodes[self.counter] = (var_index, low, high)
            self.counter += 1
        return self.unique[key]

    def variable(self, name):
        return self.node(self.order.index(name), FALSE, TRUE)

    def neg(self, u):
        """Complement, built bottom-up so it shares every subtree."""
        if u == TRUE:
            return FALSE
        if u == FALSE:
            return TRUE
        i, low, high = self.nodes[u]
        return self.node(i, self.neg(low), self.neg(high))

    def top(self, u, v):
        """The topmost variable index of u and v together."""
        tops = [self.nodes[n][0] for n in (u, v) if n not in (TRUE, FALSE)]
        return min(tops) if tops else len(self.order)

    def branch(self, u, var_index):
        """Split u on var_index into (low, high).

        var_index is the topmost index of u and v together, so every node of u
        has index >= var_index. Either u tests exactly var_index, and its
        children are the cofactors, or it tests something later and does not
        depend on var_index at all, so both cofactors are u.
        """
        if u in (TRUE, FALSE):
            return u, u
        i, low, high = self.nodes[u]
        return (low, high) if i == var_index else (u, u)

    def apply(self, op, u, v):
        """Build the diagram of `u op v`, memoised on (op, u, v)."""
        key = (op, u, v)
        if key not in self.cache:
            self.cache[key] = self._apply(op, u, v)
        return self.cache[key]

    def _apply(self, op, u, v):
        # Terminal cases first. These stop the recursion going forever.
        if op == "and":
            if u == FALSE or v == FALSE:
                return FALSE
            if u == TRUE:
                return v
            if v == TRUE or u == v:
                return u
        elif op == "or":
            if u == TRUE or v == TRUE:
                return TRUE
            if u == FALSE:
                return v
            if v == FALSE or u == v:
                return u
        else:                                       # "iff"
            if u == v:
                return TRUE
            if u == TRUE:
                return v
            if v == TRUE:
                return u
            if u == FALSE:
                return self.neg(v)
            if v == FALSE:
                return self.neg(u)

        i = self.top(u, v)
        u_low, u_high = self.branch(u, i)
        v_low, v_high = self.branch(v, i)
        return self.node(i, self.apply(op, u_low, v_low),
                         self.apply(op, u_high, v_high))

    # --- inspection ------------------------------------------------------
    def size(self, root):
        """Number of distinct interior nodes reachable from root."""
        seen, stack = set(), [root]
        while stack:
            current = stack.pop()
            if current in (TRUE, FALSE) or current in seen:
                continue
            seen.add(current)
            stack.extend(self.nodes[current][1:])
        return len(seen)

    def count_true(self, root):
        """How many of the 2^n assignments the diagram accepts.

        A node may skip variables, and each skipped variable doubles the count,
        so the walk has to remember how many variables are already decided.
        """
        n = len(self.order)
        memo = {}

        def walk(node, level):
            if node == TRUE:
                return 2 ** (n - level)
            if node == FALSE:
                return 0
            key = (node, level)
            if key not in memo:
                i, low, high = self.nodes[node]
                total = walk(low, i + 1) + walk(high, i + 1)
                memo[key] = total * (2 ** (i - level))
            return memo[key]

        return walk(root, 0)


def brute_force(fn, order):
    """True-assignment count the dumb way, for checking the diagram."""
    return sum(1 for bits in itertools.product([False, True], repeat=len(order))
               if fn(dict(zip(order, bits))))


print("=" * 70)
print("Sanity check: diagram counts match brute force")
print("=" * 70)
print()

ORDER3 = ["p", "q", "r"]
CASES = [
    ("p and q",
     lambda b: b.apply("and", b.variable("p"), b.variable("q")),
     lambda a: a["p"] and a["q"]),
    ("p or q",
     lambda b: b.apply("or", b.variable("p"), b.variable("q")),
     lambda a: a["p"] or a["q"]),
    ("p iff q",
     lambda b: b.apply("iff", b.variable("p"), b.variable("q")),
     lambda a: a["p"] == a["q"]),
    ("~p and (q or r)",
     lambda b: b.apply("and", b.neg(b.variable("p")),
                       b.apply("or", b.variable("q"), b.variable("r"))),
     lambda a: (not a["p"]) and (a["q"] or a["r"])),
]

print(f"{'function':<16} {'nodes':>6} {'accepts':>9} {'brute force':>12}  match")
for label, build_fn, direct_fn in CASES:
    b = BDD(ORDER3)
    root = build_fn(b)
    got, expected = b.count_true(root), brute_force(direct_fn, ORDER3)
    print(f"{label:<16} {b.size(root):>6} {got:>9} {expected:>12}  "
          f"{'ok' if got == expected else 'MISMATCH'}")
print()
print("All four agree with brute force, so the diagram computes the right")
print("function rather than merely a tidy structure.")
print()

print("=" * 70)
print("1. Equivalence is diagram identity")
print("=" * 70)
print()

ORDER4 = ["p", "q", "r", "s"]
b = BDD(ORDER4)
p, q, r, s = (b.variable(n) for n in ORDER4)

factored = b.apply("and", b.apply("or", p, q), b.apply("or", r, s))
terms = [b.apply("and", x, y) for x in (p, q) for y in (r, s)]
distributed = terms[0]
for t in terms[1:]:
    distributed = b.apply("or", distributed, t)

print(f"  (p | q) & (r | s)        -> node {factored}")
print(f"  (p&r)|(p&s)|(q&r)|(q&s) -> node {distributed}")
print(f"  identical nodes         : {factored == distributed}")
print(f"  nodes needed            : {b.size(factored)}")
print(f"  assignments accepted    : {b.count_true(factored)} of {2 ** 4}")
print(f"  brute force confirms    : "
      f"{brute_force(lambda a: (a['p'] or a['q']) and (a['r'] or a['s']), ORDER4)}")
print()
print("One canonical diagram for two very different-looking formulas, and the")
print("count of 9 out of 16 matches brute force. That is the value proposition:")
print("you never enumerate the rows by hand.")
print()

print("=" * 70)
print("2. A short formula with an enormous DNF and a small diagram")
print("=" * 70)
print()


def mux_order(pairs):
    """Good order: each pair's two variables sit next to each other."""
    return ["x0"] + [n for i in range(pairs) for n in (f"y{i}a", f"y{i}b")]


def build_mux(order, pairs):
    b = BDD(order)
    conj = b.apply("and", b.variable("y0a"), b.variable("y0b"))
    for i in range(1, pairs):
        conj = b.apply("or", conj,
                       b.apply("and", b.variable(f"y{i}a"), b.variable(f"y{i}b")))
    return b, b.apply("or", b.variable("x0"), conj)


print("the function:  x0 OR (y0a AND y0b) OR (y1a AND y1b) OR ...")
print()
print(f"{'units':>6} {'vars':>6} {'source':>8} {'2^vars rows':>22} "
      f"{'DNF terms':>24} {'BDD nodes':>11}")
for units in (1, 2, 4, 8, 16, 32):
    order = mux_order(units)
    b, root = build_mux(order, units)
    dnf_terms = 1 + units * (2 ** (2 * (units - 1)))
    print(f"{units:>6} {len(order):>6} {8 + units * 14:>8} {2 ** len(order):>22,} "
          f"{dnf_terms:>24,} {b.size(root):>11,}")
print()
print("At 32 units there are 65 variables. The truth table has 2^65 rows, the")
print("DNF has more than 10**36 terms, and the source is under 460 characters.")
print("The diagram has 65 nodes, because every clause has the same shape so")
print("every branch of the search computes the same subfunction.")
print()

print("=" * 70)
print("3. Where it falls apart: the same function, a different variable order")
print("=" * 70)
print()


def build_chain(order, clauses):
    """w0 OR (s1 AND w1) OR (s2 AND w2) OR ... : the same shape as the mux."""
    b = BDD(order)
    result = b.variable("w0")
    for i in range(1, clauses):
        result = b.apply("or", result,
                         b.apply("and", b.variable(f"s{i}"), b.variable(f"w{i}")))
    return b, result


# Good order: each selector sits next to the value it guards.
good_order = lambda c: [n for i in range(c) for n in (f"w{i}", f"s{i}")]
# Bad order: all the values, then all the selectors.
bad_order = lambda c: [f"w{i}" for i in range(c)] + [f"s{i}" for i in range(c)]

print(f"{'clauses':>8} {'source':>8} {'nodes, good':>13} {'nodes, bad':>12} {'ratio':>9}")
for clauses in (2, 4, 6, 8, 10, 12):
    bg, rg = build_chain(good_order(clauses), clauses)
    bb, rb = build_chain(bad_order(clauses), clauses)
    ratio = bb.size(rb) / bg.size(rg)
    print(f"{clauses:>8} {8 + clauses * 14:>8} {bg.size(rg):>13,} "
          f"{bb.size(rb):>12,} {ratio:>8.0f}x")
print()
print("Identical formula, identical variable count, identical source length.")
print("The only difference is the order in which the questions are asked, and")
print("it costs a factor of 178 at 12 clauses. The good order grows linearly")
print("and the bad order grows exponentially.")
print()
print("That is the honest summary of the whole approach. A BDD's size depends")
print("on the regularity of the function, not the length of the program. Two")
print("formulas of identical length can differ by orders of magnitude in")
print("diagram size, and you cannot tell which from reading the source.")
print()
print("Which is why practical equivalence checking is done with SAT solvers.")
print("They share no structure, so they pay no price when there is none to")
print("share, and they have strong heuristics for when there is. The logic is")
print("the same either way: turn a boolean problem into a formula, then decide")
print("whether two formulas are the same formula.")
```

Output:

```
function          nodes   accepts  brute force  match
p and q               2         2            2  ok
p or q                2         6            6  ok
p iff q               3         4            4  ok
~p and (q or r)       3         3            3  ok

1. Equivalence is diagram identity

  (p | q) & (r | s)        -> node 7
  (p&r)|(p&s)|(q&r)|(q&s) -> node 7
  identical nodes         : True
  nodes needed            : 4
  assignments accepted    : 9 of 16
  brute force confirms    : 9

the function:  x0 OR (y0a AND y0b) OR (y1a AND y1b) OR ...

 units   vars   source      2^vars rows                    DNF terms   BDD nodes
     1      3       22                        8                          2           3
     2      5       36                       32                          9           5
     4      9       64                      512                        257           9
     8     17      120                  131,072                    131,073          17
    16     33      232              8,589,934,592             17,179,869,185          33
    32     65      456  36,893,488,147,419,103,232 147,573,952,589,676,412,929          65

3. Where it falls apart: the same function, a different variable order

 clauses   source   nodes, good   nodes, bad     ratio
       2       36             3            3        1x
       4       64             7           15        2x
       6       92            11           63        6x
       8      120            15          255       17x
      10      148            19        1,023       54x
      12      176            23        4,095      178x
```

Section 2 is the result that justifies the whole technique: 65 variables, a DNF
larger than `10^36`, and 65 nodes. Section 3 is the result that justifies not
using it casually: the identical formula with the selectors moved to the end
costs 178 times more at 12 clauses, and the gap widens exponentially from there.
Nothing about the function changed. Only the order of the variables did.

That pair of tables is the honest summary. Truth tables always work and always
cost `2ⁿ`. DNFs are canonical and cost up to `2ⁿ`. BDDs are canonical and share
structure, so most real functions cost far less than `2ⁿ` — but the worst case is
still `2ⁿ`, and the constant depends on an ordering choice that is itself a
search problem. Which is why production equivalence checking uses SAT solvers:
they share nothing, so they pay nothing when there is nothing to share.

</details>## Summary

- A formula with `n` variables has exactly `2ⁿ` truth table rows, and that table
  completely determines its behaviour.
- A tautology is true on every row and a contradiction is false on every row.
  Both are bugs when they appear as conditions; a tautology never rejects
  anything.
- `F ≡ G` means identical truth tables, which is the same as "same false rows".
  Comparing two columns is a complete equivalence check.
- The algebraic rules — De Morgan, idempotence, associativity, distributivity,
  absorption, double negation — are for *simplifying*. Normal forms are for
  *comparing*. Using DNF to shrink a formula is backwards.
- Every formula has both a DNF and a CNF, and both are computable from the truth
  table alone. That makes them canonical and therefore useful for equivalence.
- A DNF has at most `2ⁿ` terms. The example above expanded to 9 terms from a
  four-variable formula, and canonical is not the same as compact.
- NAND is a universal gate because `~(a & b) = ~a | ~b`, so a machine with only
  NAND can build everything. Short-circuit `and` in Python is the software
  version of the same idea.
- The most common dead branch in real code is `x | (x & y)`, which is just `x`,
  and the truth table finds it in one comparison.
- Truth tables do not scale: `2ⁿ` rows. Scaling to dozens of variables needs SAT
  solving, BDDs, and whole-program summaries, which are the same logic with a
  better search.

## Next

[Lesson 12 — Predicates and Quantifiers](../part01_logic_proof/12_predicates_and_quantifiers.md)
generalises the formula from a fixed set of variables to a predicate over a
stated domain, and adds "for every" and "for some". It assumes you can compute
a truth table and simplify by equivalence.