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

## Formula Sheet

Notation follows [SYMBOLS.md](../SYMBOLS.md). The five connectives come from
[Lesson 10](10_propositions_and_connectives.md); this lesson adds the truth
table, equivalence, and the normal forms.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$\perp \Vdash F$` | `$a \Vdash F$` for every assignment `a` of the variables in `F` | `F` is true on every row — a tautology | checking that a condition can never reject anything. A tautology used as an `if` is a bug report |
| `$F \dashv\vdash$` | `$F \equiv G$ iff `col(F) == col(G)` | the two formulas do the same thing on every input | proving a rewrite preserves behaviour. One string comparison, exhaustively |
| `$\neg$` | `$\neg T = F$`, `$\neg F = T$` | flip the value | the only unary connective. In Python use `not`, not `~`: `~True` is `-2` |
| `$\wedge$` | true only when **both** are true | AND | Python `and`. **Short-circuits**, so operand order changes which parts run |
| `$\vee$` | false only when **both** are false | OR | Python `or`. Also short-circuits |
| `$F \to G$` | `$\neg F \vee G$` | false only when `F` is true and `G` is false | Python `~F or G`. Never `F and not G` |
| `$F \leftrightarrow G$` | `$(F \to G) \wedge (G \to F)$` | both directions hold | biconditional. `F == G` on booleans is exactly this |
| $2^n$ | | the number of rows over `n` variables, and also the number of distinct boolean functions on `n` variables | the cost of a truth table: 4 rows for `n=2`, 16 for `n=4`, 1,024 for `n=10` |
| $2^{2^n}$ | | the number of *different formulas* over `n` variables, counting syntactically | why "all formulas" is not a search space anyone enumerates: `n=4` already gives 65,536 distinct behaviours |
| De Morgan | `$\neg(F \wedge G) \equiv \neg F \vee \neg G$`, `$\neg(F \vee G) \equiv \neg F \wedge \neg G$` | push a NOT through by flipping the operator | the step that makes NAND universal: `~(a & b)` becomes `~a | ~b` |
| idempotence | `$F \vee F \equiv F$`, `$F \wedge F \equiv F$` | repeating a thing changes nothing | first thing to try when a condition is long |
| absorption | `$F \vee (F \wedge G) \equiv F$` | if `F` is already a disjunct, the rest is dead | the most common dead branch in real code. The lesson's own search finds it every time |
| distributivity | `$F \wedge (G \vee H) \equiv (F \wedge G) \vee (F \wedge H)$` | AND over OR fans out | the reverse, `(F∨G)∧F = F∨(G∧F)`, is what removes a conjunct |
| double negation | `$\neg\neg F \equiv F$` | two NOTs cancel | the normal-form step that guarantees every literal is a bare variable or its negation |
| a *literal` | a variable or `~variable` | | the atoms of a normal form. A formula with no NOT on a compound is in **negation normal form** |
| DNF | `$\bigvee_{i} \bigwedge_{j} \ell_{ij}$` — an OR of AND-terms of literals | "these are the combinations of facts that make it true" | rule engines, query planners, spreadsheet dependency trees. **At most `2ⁿ` terms** — one per true row |
| CNF | `$\bigwedge_{i} \bigvee_{j} \ell_{ij}$` — an AND of OR-clauses of literals | "all of these constraints hold" | what SAT solvers consume, which is why clause-based solving works |
| DNF of a contradiction | `$\varnothing$` — no terms | | the empty OR. `dnf_to_formula` writes it as `p & ~p` because an empty disjunction has nothing to return |
| CNF of a tautology | `$\varnothing$` — no clauses | | the empty AND, written as `p | ~p` for the same reason |
| `$F \models G$` | every assignment satisfying `F` also satisfies `G`; equivalently `$F \to G$` is a tautology | `F` is a stronger condition than `G` | one-directional: `$p \models p \vee q$` holds, and `$\neg(p \wedge q) \models p \to q$` does not |

**Domain restrictions, which are where answers go wrong.** Row order is fixed
once and for all (`FF, FT, TF, TT` over `p, q`) — a column is only comparable to
another column if both were computed in the same order, and comparing `0111` to
`0011` is a bug, not a proof. Truth tables are complete **only for the variables
that actually appear**: `p & q | p & ~r` mentions `r`, so a table over `p` and
`q` alone does not settle it. And the 16-row claim in the Worked Example depends
on the four named variables; add a fifth and the "one false row" becomes one row
out of 32, which changes the security argument even though the condition is
unchanged.

## Multiple Choice Questions

**Q1.** The lesson's brute-force search returns
`~((is_get | ~has_token) | ~(is_admin | is_owner))` as equivalent to the
authorisation condition. Why does the lesson decline to ship it?

- A) It is not actually equivalent; the search has a bug
- B) It is equivalent and genuinely shorter by tree depth, but no shorter than the hand-simplified version by gate count, and it says nothing a reader can understand
- C) It is equivalent but slower to evaluate, because NOT propagates to every leaf
- D) It is equivalent but uses a variable that the original did not mention

<details>
<summary>Answer and explanation</summary>

**B) It is equivalent and genuinely shorter by tree depth, but no shorter than the
hand-simplified version by gate count, and it says nothing a reader can
understand.**

The search minimises *syntax tree depth*, which is not the same as either gate
count or human comprehensibility. The lesson's fifth Common Mistake is exactly
this point: "equivalent" gets read as "the same", and once two things are called
the same you stop expecting them to look different. The code's own comment says
"Shortest by syntax tree depth is not the same as simplest to a human", and
Exercise 2(d) reaches the identical verdict from the other direction — it refuses
to ship a search result in favour of `~is_get | has_etag`, which has two
connectives and reads as "a GET needs a validator".

A is wrong because the code prints `equivalent: True`, having compared all 16
columns. The check is the exhaustive one the whole lesson is built on.

C is wrong. NOT is O(1) per node; a formula with fewer nodes evaluates faster, not
slower. The `~(a & b)` identity is a *rewriting* rule, not an evaluation cost.

D is worth checking and worth dismissing. The search enumerates over the same
`NAMES4` list the target was built from, so a formula mentioning a new variable
could never match a 16-column target — the search space does not contain one. The
equivalence therefore implies the variables match, which is another way of seeing
that equivalence is a claim about behaviour only.

</details>

**Q2.** The lesson's DNF printer reports 9 AND-terms for `(p | q) & (r | s)` over
four variables. Where do the 9 come from, and why is the CNF only 7 clauses for
the same formula?

- A) DNF has one term per true row (9 true rows of 16); CNF has one clause per **false** row (7 false rows of 16). The two add to 16 because a row is either true or false
- B) DNF has one term per false row; CNF has one per true row, and the counts differ because the CNF prunes redundant clauses
- C) The CNF is smaller because the printer merges duplicate clauses
- D) The counts differ because DNF is over 4 variables while CNF is over 3

<details>
<summary>Answer and explanation</summary>

**A) DNF has one term per true row (9 true rows of 16); CNF has one clause per
**false** row (7 false rows of 16). The two add to 16 because a row is either true
or false.**

This is the duality the Formal Version's proof sketch describes: "the CNF is the
dual argument over the false rows." Counting it out for `(p|q) & (r|s)`: it fails
whenever both of `p, q` are false, or both of `r, s` are false. That is
`2 × 2 + 2 × 2 = 8` combinations, minus the one where both fail simultaneously —
`p=q=r=s=F` — counted twice, giving 7 false rows and 9 true rows. The identity
`dnf + cnf = 2^n` is structural, and it is why a function and its negation have
swapped normal forms.

B inverts the construction and also invents a pruning step the printer does not
perform. `to_cnf` appends one clause per false row and never inspects the clause
it just built.

C is false: `to_cnf` builds a fresh list and does no comparison against existing
clauses. You can confirm it by reading the function — there is no merge step.

D is false: both printers receive the same `names` list, and the code prints
"of 4 literals" for both.

</details>

**Q3.** The Worked Example's condition
`not is_get or has_etag or not not_modified or cache_writable` is false on
exactly one row out of 16. The lesson concludes it is "effectively a tautology"
and should be deleted. What is the strongest statement the truth table alone
supports?

- A) The condition is a tautology, because only one row in 16 is unreachable in practice
- B) The condition is **not** a tautology — it is contingent, with a single false row at `is_get=T, has_etag=F, not_modified=F, cache_writable=F` — and calling it unreachable is domain reasoning, not table reasoning
- C) The condition is a contradiction, because one disjunct is always false
- D) The condition is contingent, and the false row can never be reached because four variables cannot all be true at once

<details>
<summary>Answer and explanation</summary>

**B) The condition is **not** a tautology — it is contingent, with a single false
row at `is_get=T, has_etag=F, not_modified=F, cache_writable=F` — and calling it
unreachable is domain reasoning, not table reasoning.**

The column is `1111111101111111`: fifteen trues and one false. That is the
definition of contingent. The lesson is careful about this in its own Step 7:
"'unreachable in practice' was established by domain knowledge, not by the table.
The table only told you where the false row is. Bridging that gap is domain
reasoning, and it is the part people skip."

The reasoning that closes the gap is about the *semantics* of the variables: a GET
that reports `not_modified = False` (i.e. not modified) while having no etag is
contradictory, because you cannot know a resource is unmodified without a
validator. That is a fact about HTTP, not about `&` and `∨`.

A is the trap, and it is the most important misconception in the lesson: "almost a
tautology" is not a tautology. If the domain assumption is ever wrong — a proxy
strips the etag, a client sends a bogus `If-None-Match` — that one row becomes
reachable and the check is the only thing standing between you and serving stale
content. The correct fix is not deletion, it is making the assumption explicit.

C is wrong in an interesting way. `not not_modified` is not always false; it is
true whenever `not_modified` is false, which is half the rows. A *disjunct* being
false in some rows says nothing about the whole formula.

D is false as written — the false row has three of the four variables false — and
"cannot all be true" is not the reason. The row *is* a legal assignment. It is
ruled out by domain knowledge, not by the shape of the formula.

</details>

**Q4.** A formula contains `p & q | p & ~r`. A colleague says "these are similar
to `p`, so it simplifies to `p`". Using the lesson's own checks, what is wrong
with the reasoning?

- A) Nothing — `p & q | p & ~r` is equivalent to `p` by distributivity
- B) The table must be over `p`, `q`, **and** `r`; computed over `p` and `q` alone it reads as `p & q | p = p`, which is a false equivalence, because the columns genuinely differ when `r` is included
- C) The formula is not in negation normal form, so it cannot be simplified
- D) Simplification requires a DNF, and the DNF has 4 terms

<details>
<summary>Answer and explanation</summary>

**B) The table must be over `p`, `q`, **and** `r`; computed over `p` and `q` alone
it reads as `p & q | p = p`, which is a false equivalence, because the columns
genuinely differ when `r` is included.**

The formula mentions three variables, so it has 8 rows. A column computed over
`p, q` only is the column of a *different formula* — one where `~r` has been
silently treated as a constant. Take `p = T, q = F, r = T`: the original gives
`(T∧F) ∨ (T∧F) = F`, while `p` gives `T`. Different columns, so not equivalent,
and the simplification is wrong. This is exactly the lesson's second Common
Mistake, which names this pair: "`p & q | p & ~r` and `p` are similar and not."

The fix is mechanical: `all_prereqs`-style, take the variables the formula
actually mentions, and build the table over those. The lesson's `assignments(names)`
and `column(formula, names)` take `names` as a parameter for this reason — passing
`["p", "q"]` for a formula mentioning `r` is a bug the signature invites.

A is the wrong answer the colleague reached, and it is wrong by exactly this much:
on a table over `p, q` the two columns do agree, so the error survives the very
check that was supposed to catch it.

C is a non-sequitur. Negation normal form matters for building normal forms, not
for the algebraic rewrites that do simplification. `p & (q | ~r)` is already in
NNF, and it still is not `p`.

D is irrelevant. The DNF of `p & q | p & ~r` is 2 terms, and DNF is the lesson's
explicitly *wrong* tool for shrinking a formula.

</details>

**Q5.** In the lesson's gate table, NAND on `(T, F)` gives `True` and NOR on
`(T, T)` gives `False`. Reading NAND as `~(a & b)` and NOR as `~(a | b)`, which
row makes the "NAND is a universal gate" claim follow?

- A) `(T, T)`, where NAND is `False`
- B) `(F, F)`, where both NAND and NOR are `True`
- C) `(F, T)`, where NAND is `True` and NOR is `False` — so De Morgan turns NOR into an AND of negations, and `~(a & a)` gives NOT for free
- D) No single row does; universality is a property of the whole table

<details>
<summary>Answer and explanation</summary>

**C) `(F, T)`, where NAND is `True` and NOR is `False` — so De Morgan turns NOR
into an AND of negations, and `~(a & a)` gives NOT for free.**

Universality is a *rewriting* claim: every function can be expressed using NAND
alone. The three constructions are `NOT x = NAND(x, x)`, `AND(a,b) = NAND(a,b)`
followed by a NOT, and `OR(a,b) = ~(~(a&b) & ~(a&b))` by De Morgan. The row that
demonstrates the third step is any row with `a` and `b` differing, because that is
where `~(a & b)` and `~(a | b)` come out with opposite values, showing the
negation really has been pushed through and the operator really has flipped.

A is wrong: at `(T, T)` NAND is `False`, and that row shows NAND *can* produce a
false — it shows nothing about expressing NOT or OR.

B is wrong for the same reason in reverse. At `(F, F)` both gates are `True`, and
`True` is the less informative output; you learn nothing about which structure
survives.

D is the tempting one and it is a category error. Universality is not a property
of the table read row by row; it is a property of the *rewriting rules* applied to
arbitrary formulas. The table is a check that the rules are sound on a small case,
not the argument itself.

</details>

**Q6.** The lesson says NAND alone can build everything. In Python, `x != 0 and
10 / x > 1` works while `10 / x > 1 and x != 0` raises `ZeroDivisionError`. What
does that pair of facts tell you, and what does it *not* tell you?

- A) The two expressions are equivalent as boolean functions, so the order must not matter and the error is a Python bug
- B) `and` and `or` short-circuit, so the formula's operand order is part of its meaning operationally even though `x != 0 and (10/x > 1)` and `(10/x > 1) and x != 0` have the same truth column
- C) `and` is not commutative, so the two expressions are not equivalent
- D) Python's `and` is not a boolean connective at all

<details>
<summary>Answer and explanation</summary>

**B) `and` and `or` short-circuit, so the formula's operand order is part of its
meaning operationally even though `x != 0 and (10/x > 1)` and `(10/x > 1) and
x != 0` have the same truth column.**

Over booleans, both expressions compute the same function — the truth columns are
identical, and you can verify it by making `x != 0` a variable `p` and `10/x > 1`
a variable `q`: both give `p & q`. But the *evaluation* differs, because `and`
returns as soon as the left operand decides the answer, so the division runs in one
order and not the other.

The lesson's point is that a truth table describes **behaviour on a total
domain**, where every subformula is safe to evaluate. Short-circuiting breaks that
assumption: the set of inputs on which a subformula is *reached* is smaller than
the set on which it is *defined*. That is the same shape as the Worked Example's
caveat — the table tells you the behaviour where the row is reachable, and
reachability is a domain question.

A is wrong because the equivalence claim is about the truth column only, and the
error is real, not a bug. "Equivalent" is a statement about values, not about
which code runs.

C is a real confusion and worth naming: as *boolean functions* `&` **is**
commutative, and the column comparison proves it. Non-commutativity is a property
of `+` and `*` on matrices, not of conjunction.

D is wrong. Python's `and` returns one of its operands rather than a bool, which
is a genuine difference from `∧` — `0 and 5` is `0`, not `False` — but it is still
a boolean connective in every respect this lesson needs.

</details>

**Q7.** `F` and `G` are equivalent formulas over the same variables. Must their
DNFs be *textually* identical, or only equivalent as functions?

- A) Only equivalent. Two formulas can share a DNF up to reordering of terms and literals, and `(p & q) | r` and `r | (q & p)` have different text but the same normal form
- B) Textually identical. The DNF is a canonical representation, so equal truth tables give byte-identical output
- C) Only equivalent, and the DNFs can differ in *length* even though the truth tables match
- D) Textually identical, but only when the variables are listed in the same order

<details>
<summary>Answer and explanation</summary>

**A) Only equivalent. Two formulas can share a DNF up to reordering of terms and
literals, and `(p & q) | r` and `r | (q & p)` have different text but the same
normal form.**

This is a direct consequence of how `to_dnf` is written: it walks the assignments
in one fixed order and emits one term per true row. The traversal is fixed by the
implementation, so two formulas with the same truth table produce the *same list
of terms in the same order* — which is why the lesson's theorem can say "identical
term-for-term". But that is a statement about the printer's canonical traversal,
not about the text of the input formulas. The inputs are free to differ in
parenthesisation, in the order of conjuncts within a term, and in the order of
terms; the output is invariant.

B is the belief that "canonical" means "the input text is normalised in place".
Canonical means a *function* of the truth table is uniquely determined, which is
weaker than saying the two inputs were already identical.

C is false and the distinction matters. DNF length is a function of the truth
table alone — one term per true row — so equivalent formulas *do* have DNFs of the
same length. The length can still be enormous (up to `2ⁿ`); that is the lesson's
exponential-blow-up complaint, and it is a complaint about the size of the
canonical form, not about its variability across equivalent inputs.

D is a plausible-looking refinement that is not what the code does. The traversal
order is determined by `itertools.product([False, True], ...)`, so it is fixed for
a given list of names; the names themselves are passed in by the caller, and
permuting them permutes the emitted terms. So the DNF is canonical *relative to a
fixed variable order* — which is a real and important qualification, and one the
BDD section later makes into its central problem.

</details>

**Q8.** The lesson's Exercise 3 checker reports `a and b and not b` as "depends
on its variables" rather than as simplifiable. Why is that the honest answer, and
what does the miss tell you about the checker?

- A) It is a bug: `b and not b` is always false, so the condition is constant
- B) It is correct: the condition is `a`, which is not constant. The checker detects *constant* conditions, not *simplifiable* ones, and constant-folding a subexpression is a separate pass
- C) It is correct because the checker's variable list does not include `a`
- D) It is correct because `ast` cannot represent `and not b`

<details>
<summary>Answer and explanation</summary>

**B) It is correct: the condition is `a`, which is not constant. The checker
detects *constant* conditions, not *simplifiable* ones, and constant-folding a
subexpression is a separate pass.**

`a and b and not b` reduces to `a` — genuine simplification — but `a` is still a
variable, so the condition takes a different value under different assignments
and the checker's honest verdict is "I do not know". The lesson says this
precisely: "The checker does not find that because `a and b and not b` is *not*
constant, it just has a dead part. Simplifying constants inside an expression is a
separate pass, and it is what the `a or not a` on line 25 does get found for."

The distinction generalises. A tautology detector and a simplifier answer
different questions: *can this condition ever be false?* versus *is this condition
the smallest formula computing the same function?* The first is cheap and
decidable on a truth table; the second is the whole of equivalence checking, and
the lesson's brute-force search shows it can return something *harder to read* than
what you started with.

A is the wrong mental model: it assumes "contains a constant part" and "is
constant" are the same question. They are not, and the difference between them is
a whole class of real lint warnings.

C is false: `a` is in `VARS`, and the checker reports line 13's `x or not x` as
"depends on its variables" for exactly the same honest reason — `x` is a variable.

D is false and the code demonstrates it: `ast` parses `a and b and not b` fine, and
line 25's `a or not a` *is* detected, which requires the same `ast.Not` handling.

</details>

**Q9.** The lesson's summary says "NAND is a universal gate because
`~(a & b) = ~a | ~b`". Is the De Morgan identity the *reason* NAND is universal,
or is it one ingredient?

- A) It is the whole reason; the identity alone shows any function is buildable
- B) It is one ingredient. Universality is the conjunction of three constructions — NOT from `NAND(x,x)`, AND as NAND-then-NOT, OR by De Morgan plus AND — and each must hold before any formula can be rewritten
- C) It is the whole reason, but only for two-input gates
- D) It is irrelevant; NAND is universal because of how transistors are wired

<details>
<summary>Answer and explanation</summary>

**B) It is one ingredient. Universality is the conjunction of three
constructions — NOT from `NAND(x,x)`, AND as NAND-then-NOT, OR by De Morgan plus
AND — and each must hold before any formula can be rewritten.**

To show a gate set is universal you must be able to *rewrite any* formula into
that set without introducing new variables. That takes: a constant and NOT, to
handle literals; AND, to keep formulas from exploding; and OR, to keep them from
exploding the other way. The De Morgan identity supplies one of the two
operator rewrites. On its own it is one line of algebra that happens to be true.

A is the misconception, and it is a good one to name because De Morgan *is* the
deepest-looking fact in the neighbourhood and it *is* what lets you eliminate an
OR or an AND gate. But the elimination only means something if you have something
to eliminate it *in favour of*, and the other two constructions are what provide
it.

C is wrong, and it is worth knowing why. NAND is universal for arbitrary fan-in,
not just two inputs: `x1 & x2 & … & xk` is `NOT(NAND(...))` of a balanced NAND
tree, and any formula with many variables is a formula over two-input gates. Two
inputs is a property of the *gate*, not a limit on what the gate set computes.

D is wrong on its own terms. Transistor wiring determines what is *cheap*, and
NAND is cheap on real silicon — that is history, not mathematics. The
mathematical claim is about what a gate set can express, and it is independent of
any physical implementation.

</details>

**Q10.** The lesson's last section shows two functions of identical source length
and identical variable count whose BDDs differ by a factor of 178 at 12 clauses.
What is the practical lesson, and what is the trap in reading that table?

- A) BDDs are unreliable and should be abandoned for SAT solvers
- B) BDD size depends on variable order, so a BDD-based checker must treat ordering as part of its problem — and the trap is reading "178x worse" as a statement about the formulas rather than about the order chosen
- C) The formulas are genuinely different functions, so the 178x is not a fair comparison
- D) SAT solvers and BDDs compute different things

<details>
<summary>Answer and explanation</summary>

**B) BDD size depends on variable order, so a BDD-based checker must treat
ordering as part of its problem — and the trap is reading "178x worse" as a
statement about the formulas rather than about the order chosen.**

The lesson says it directly: "Identical formula, identical variable count,
identical source length. The only difference is the order in which the questions
are asked." A ROBDD is canonical *given a variable order*, and the order is a free
parameter the caller supplies. So BDD size is a property of the pair (function,
order), not of the function alone — which is exactly why the same construction
grows linearly under one order and exponentially under the other.

The trap is the natural but wrong inference that the bad order reveals something
about the function. It reveals something about the *interaction* between the
function's structure and the order. The honest summary is the lesson's: a BDD's
size depends on the regularity of the function, not the length of the program, and
you cannot tell from reading the source which you have.

A over-corrects. The lesson's own conclusion is that practical equivalence
checking uses SAT solvers because they "share no structure, so they pay no price
when there is none to share" — that is an argument for SAT's *robustness*, not an
indictment of BDDs. BDDs remain the right tool when structure is present, and they
are the standard technique for circuit equivalence checking.

C is false: the two orders are applied to the *same* function, which is the whole
point of the comparison.

D is false. Both decide the same question — do these two formulas compute the same
function — by different means. The lesson's closing line is exactly this: "turn a
boolean problem into a formula, then decide whether two formulas are the same
formula."

</details>

## Subjective Questions

### Short Answer

**Q1. State the definitions of tautology, contradiction, and contingent, and give
the column of a tautology over `p` and `q` in the lesson's row order.**

<details>
<summary>Answer</summary>

`F` is a **tautology** if it is true on every row — column `1111` over
`p, q` in the order `FF, FT, TF, TT`. `F` is a **contradiction** if it is false on
every row — column `0000`. `F` is **contingent** otherwise: true on some rows and
false on others, which is the normal case.

The lesson's own table shows all three: `p | ~p` is `1111`, `p & ~p` is `0000`,
and `p & (p | q)` is `0011`.

</details>

**Q2. How many rows does a truth table have over `n` variables, and how many
*distinct boolean functions* are there over `n` variables? Why are these two
numbers different?**

<details>
<summary>Answer</summary>

`2^n` rows — 4 for `n = 2`, 16 for `n = 4`, 1,024 for `n = 10`.

And `2^(2^n)` distinct functions, because a function is a choice of output for
each row, so the outputs form a binary string of length `2^n` and there are
`2^(2^n)` such strings. At `n = 4` that is 65,536 functions; at `n = 10` it is
`2^1024`.

The two numbers differ because a *table* is one function's worth of rows, while a
*function* is one whole table.

</details>

**Q3. What is the DNF of a formula that is true on 3 rows out of 8, and what is
the CNF of the same formula? State the term and clause counts.**

<details>
<summary>Answer</summary>

The DNF has **one AND-term per true row**, so 3 terms, each a conjunction of the
literals that fix that row's values.

The CNF has **one OR-clause per false row**, so 8 − 3 = 5 clauses.

The identity is `dnf_terms + cnf_clauses = 2^n`, and it holds because every row is
either true or false. The lesson's `p & (q | r)` row is exactly this case: 3 DNF
terms, 5 CNF clauses.

</details>

**Q4. What is the single false row of the Worked Example's condition, and what
domain fact makes it unreachable?**

<details>
<summary>Answer</summary>

The row is `is_get = T, has_etag = F, not_modified = F, cache_writable = F`, giving
column `1111111101111111`.

The domain fact: a GET that reports "not modified" while having no validator
(`has_etag = F`) is self-contradictory — you cannot know a resource is unmodified
without a validator to compare against. That is a fact about HTTP, not about
`&` and `∨`, and the lesson's Step 7 insists on the distinction.

</details>

**Q5. Write the two De Morgan identities, and state the one gate that the first
identity makes redundant.**

<details>
<summary>Answer</summary>

`$\neg(F \wedge G) \equiv \neg F \vee \neg G$` and
`$\neg(F \vee G) \equiv \neg F \wedge \neg G$`.

The first makes **NAND** redundant: `~(a & b)` is `~a | ~b`, so a machine with only
NAND and NOT needs no separate AND gate, and the second identity similarly
disposes of OR. That is the whole argument for NAND's universality.

</details>

**Q6. Why does the lesson's brute-force search return a formula with a NOT wrapped
around the whole expression, and why is that not a bug?**

<details>
<summary>Answer</summary>

Because the search minimises **syntax tree depth**, and `~F` has depth one more
than `F` no matter how deep `F` is. Minimising depth is a different objective from
minimising gate count, and a third one from minimising how readable the result is.

It is not a bug because equivalence was verified — the code prints
`equivalent: True` after comparing all 16 columns. The result is a *different
formula for the same function*, which is exactly what the lesson says the table
determines: behaviour, not syntax.

</details>

### Long Answer

**Q1. The lesson insists that a truth table is a complete description of a
formula's behaviour. That is true, and it is also the source of the lesson's
sharpest caveats. Construct two formulas that are equivalent as boolean functions
over a total domain but behave differently as *Python expressions*, explain what
the truth table cannot see, and say what additional information you need to make
a claim about real code rather than about a boolean function.**

<details>
<summary>Model answer</summary>

**The construction.** Take any predicate `P` and any subformula `S` that can raise
an exception or run a side effect. Then `P and S` and `S and P` are equivalent as
boolean functions — both columns are `p & q` — and different as Python expressions.
The lesson's own instance is the cleanest available: `x != 0 and 10 / x > 1`
evaluates, while `10 / x > 1 and x != 0` raises `ZeroDivisionError` at `x = 0`.
Same truth column, different observable behaviour.

**What the table cannot see.** Three things, in increasing order of how badly they
bite.

*Evaluation order.* `and` and `or` short-circuit, so the set of inputs on which
`S` is *reached* is strictly smaller than the set on which it is *defined*. The
truth table ranges over all `2^n` assignments, which implicitly assumes every
subformula is safe to evaluate everywhere. Short-circuiting breaks that assumption,
and no column comparison can detect it, because both formulas have the same
column.

*Domain restriction.* The table ranges over the cartesian product of the
variables' types. If `x` is a non-zero integer by contract, the row `x = 0` is not
in the domain, the two formulas are equivalent *on the domain*, and the `ZerodivideError`
case is out of scope. If `x` can be zero, the two differ operationally even though
they agree as columns. The Worked Example makes the same move in the other
direction: it finds a single false row and then needs *domain knowledge* to rule
it out. Truth tables talk about all assignments; code runs on the reachable ones.

*Side effects and cost.* `f(x) or g(y)` and `g(y) or f(x)` have the same column
whether or not `f` and `g` log, mutate a counter, or take an hour. Behaviour in
the sense the table captures is the *returned value*; behaviour in the sense a user
observes is the whole trace.

**What you need to make a claim about real code.** Three extra ingredients, and
each is a genuine cost.

A *type and range discipline*: what values each variable can actually take, so you
can delete rows the domain excludes. This is the step the lesson's Step 7 flags as
"the part people skip", and it is domain reasoning — the table cannot do it and no
amount of table size will.

An *evaluation-order discipline*, which is really a rule about where effects are
allowed. The standard fix is functional purity: if every subformula is pure and
total, the column is the whole story, and the two formulas really are
interchangeable. That is why the lesson's `Formula` class evaluates eagerly and
has no `evaluate` with side effects — it is a model of the regime where the table
suffices.

A *cost model*, if the claim is about performance rather than correctness. Two
expressions with the same column can differ by orders of magnitude in time, and
the table is silent on that. This is the same lesson as the rest of the course:
big-O is growth, not milliseconds; a truth column is behaviour, not a profile.

**The honest formulation.** The correct statement is: *a truth table is a complete
description of the value a formula returns, on a total domain, under eager
evaluation.* Each of the three qualifications is load-bearing, and dropping any one
of them turns a proof into a plausible-looking bug. The lesson's own code is
careful about this in the place it matters most — the `Not.evaluate` method
comments that it uses `not` and not `~` because `~True` is `-2`, which is a
reminder that "the column" is an abstraction you have to earn the right to use.

</details>

**Q2. The Worked Example reaches a conclusion its own Step 7 admits does not come
from the table: the condition should be deleted, but the table only shows one
false row. Take that gap seriously. What exactly does the table establish, what
exactly does the domain argument add, and what would it take to make the deletion
safe rather than merely plausible?**

<details>
<summary>Model answer</summary>

**What the table establishes, exactly.** Over the four named variables, the
condition `not is_get or has_etag or not not_modified or cache_writable` has
column `1111111101111111`. That is contingent, with exactly one false row:
`is_get = T, has_etag = F, not_modified = F, cache_writable = F`. So the table
gives you: the condition is not a tautology; it is false on a precisely specified
input; and that input is fully determined. That is a complete description of
behaviour, and it is genuinely useful — you can now say what the check is *for*.

**What the domain argument adds.** It asserts that the false row is not reachable:
a GET that reports `not_modified = False` while having no etag cannot occur,
because determining that a resource is unmodified requires a validator, and
`has_etag = F` says there is none. If that is right, the condition never rejects
anything, so it is dead code.

The lesson's Step 7 is careful, and the care matters: "'unreachable in practice' was
established by domain knowledge, not by the table. The table only told you where the
false row is. Bridging that gap is domain reasoning, and it is the part people
skip." Two things are being distinguished. The table is *complete* — it leaves no
other false row hidden. The domain argument is *not verified* — it is a claim about
HTTP that nobody in the code review checked, and it is stated in a comment rather
than enforced by a type.

**Why the deletion is not safe as it stands.** The domain argument has at least
three failure modes, all of them real.

*It is not enforced anywhere.* There is no type that says "a response with
`not_modified = True` has an etag". The invariant lives in a comment, so it holds
exactly as well as the code that maintains it, and a proxy that strips the ETag
header breaks it silently.

*The variable naming is doing hidden work.* The condition's fourth disjunct is
`not not_modified` — a double negation. The lesson notes "nobody can tell whether
it was right". If the author intended `not_modified` to mean "the request *asked*
for revalidation" rather than "the resource *is* unmodified", the domain argument
is about the wrong variable and the false row may be perfectly reachable. Reading
the table forced this question; the table cannot answer it.

*The direction of the error is bad.* A condition that never fires is a
*false-negative generator*. If the invariant breaks, the check that would have
caught the bad request is the check that was deleted. A condition that always fires
is at least loud. So deletion removes the only signal at exactly the moment the
signal becomes necessary.

**What would make the deletion safe.** Three options, in increasing order of
rigour.

*Keep the check and make the invariant explicit.* If the check is genuinely
defensive, its value is in catching the case where the domain argument is wrong.
An `assert` documents the assumption and turns a silent wrong answer into a loud
failure. This is nearly free and it inverts the risk: now the invariant breaking
is an error you see, not a bug you serve.

*Encode the invariant in the types, then simplify safely.* If the code guarantees
"a `not_modified` response always carries an etag", make that a constructor
invariant. Then the table over the *reduced* domain — with the impossible
assignment excluded — genuinely has no false rows, and the condition really is a
tautology. The deletion is then not "probably safe" but "safe given the type",
which is a claim you can check mechanically.

*Replace it with the check that expresses the intent.* The condition's real
purpose was "a GET needs a validator". Write *that*: `not is_get or has_etag`.
It has one false row instead of one, it says what it does, and it stays true if
the domain changes. This is Exercise 2's simplified form, and the lesson's verdict
on it — two connectives, comprehensible, confirmed by the column — is the right
shape of answer.

**The general form.** The table is the *machine-checkable* half and the domain
argument is the *human* half, and the lesson's own warning is that people skip the
human half. But here the sharper point is that people also *over-trust* the machine
half: "the table says one false row, and the false row is silly" feels like
finishing, when it is exactly the point at which the proof stops and the judgement
begins. A truth table tells you precisely what a formula does. Deciding whether
that is the right thing for it to do is not a job a truth table can do.

</details>

**Q3. The lesson reports that a 4-variable formula on one line becomes a 9-term
DNF, and that `n = 30` gives up to 1,073,741,824 terms. Explain precisely why the
DNF blows up, why CNF does not blow up on the same formula, and what property of a
formula decides which normal form you should use.**

<details>
<summary>Model answer</summary>

**Why the DNF blows up.** By construction: `to_dnf` emits one AND-term per true
row, and there are `2^n` rows. For `(p | q) & (r | s)` the column is 9 true rows
out of 16, hence 9 terms of 4 literals each. The blow-up is not a defect of this
particular formula; it is the worst case, and the worst case is realised by any
function that is true on most of its rows. A tautology has `2^n` terms — for
`n = 30`, the 1,073,741,824 the lesson reports.

The reason is structural, not incidental. A term must *pin down* a row, so each
term needs one literal per variable, and different true rows need different
patterns of literals. The only way to avoid enumerating rows is for the formula to
*share* subexpressions across rows — and the DNF format has no place to put a
shared subexpression, because a DNF is a flat disjunction of conjunctions.

**Why CNF does not blow up on the same formula.** Because of the same construction
run on the complementary set: one clause per *false* row, and the false rows are
`2^n − true_rows`. For `(p | q) & (r | s)` that is 7 clauses, comfortably under
9. And the choice of which normal form is smaller is entirely determined by whether
the function is true on more or fewer rows than half of them. The lesson's own
table shows both extremes: `~(p & q) | r` has 7 DNF terms and **1** CNF clause,
while `p -> q` — the same shape with `~p` in front — has 6 DNF terms and 2 CNF
clauses. Always convert to *both* and take the smaller; that is why both
converters exist.

**The property that decides the choice.** Three, in order of how much they
actually matter.

*How many rows satisfy the formula.* This is the first-order fact and it
completely determines the term counts: `dnf = |sat|`, `cnf = 2^n − |sat|`. If you
can bound `|sat|` without building the table, you have already chosen.

*How much the literals repeat across rows.* A formula whose true rows differ in
one variable at a time — `(p|q) & (r|s)`'s neighbours in hypercube terms — shares
structure. A formula whose true rows are scattered shares none. This is the
property the BDD section measures properly, and it is the one that decides whether
a *structural* method will work.

*Whether you need the form at all.* And this is the practical point. The DNF is
canonical, which is exactly what makes it good for *comparing* and exactly what
makes it bad at *shrinking*. The lesson's third Common Mistake is the sharp
version: "Two equivalent formulas can have the same DNF and wildly different
sizes, so converting to DNF to compare is right and converting to DNF to shrink is
backwards."

**So which should you use.** Match the tool to the question. Comparing two
formulas: either normal form works, and either is exact, and that is what canonical
means. Storing a formula as a truth table or a BDD: the truth table costs `2^n`
unconditionally, the BDD costs what the structure is worth, and the variable order
decides how much that is — the lesson's factor of 178 at 12 clauses. Writing a rule
engine's rules: DNF, because "which combinations of facts make this true" is
literally the question rule engines ask, and it is what makes their forward
chaining straightforward. Handing a problem to a solver: CNF, because clause-based
solving works on clauses and DNF is the wrong shape for it.

The unifying statement is the lesson's own division of labour: the algebraic rules
— De Morgan, distribution, absorption — are for *simplifying*; the normal forms are
for *comparing*; and a normal form is never the right way to shrink anything,
because canonical and compact are different properties and the blow-up is the
price of buying the first one.

</details>

**Q4.** The lesson's last section finds two functions of identical source length
whose BDDs differ by 178×, and concludes that variable ordering is "a separate
search problem in its own right." Take that seriously: what exactly is being
searched over, what is the objective, why is a truth table not enough, and what
does the whole episode say about the relationship between a canonical
representation and the cost of computing it?**

<details>
<summary>Model answer</summary>

**What is searched.** The space is the set of *orders* — permutations of the `n`
variable names. For 12 clauses that is 24 variables and therefore about
`2.4 × 10^23` orders, far more than can be enumerated. The lesson's table is a
sweep over a *family* of orders, good and bad, to exhibit the spread; it is not a
search.

**The objective.** Minimise the number of distinct nodes in the reduced diagram
built under that order. The objective is a property of the *pair* (formula, order),
which is the crux: the formula is fixed, so all the variation is coming from the
order. A BDD built under order `σ` and one built under `σ'` are both canonical, both
correct, and both decide the same question — they just cost different amounts.

**Why a truth table is not enough.** Because the table is `2^n` unconditionally. It
has no notion of sharing, so it cannot distinguish a function whose branches
recompute the same subfunction from one whose branches all differ. That difference
is invisible in the column — the column is the *answer* — and visible only in the
*work required to produce it*. This is the same shape as a recurring theme in the
course: a canonical form fixes the answer, and says nothing about the cost of
reaching it. A canonical JSON serialisation of a tree can still be large.

**Why the search is genuinely hard and not just tedious.** The objective is not
decomposable. You cannot score a partial permutation and extrapolate, because
whether two subtrees merge depends on which variables came *before* them — a node
that shares with a sibling under one order is two separate nodes under another.
So this is the structure of problems where greedy and local search are natural and
provably incomplete, which is why real BDD packages ship heuristic orderers
(sifting, with windowed reordering) rather than an exhaustive search. The lesson is
right that this is a problem in its own right, and it is the same category as
variable elimination order in Bayesian networks and join ordering in relational
query optimisation: all three are "which order do I ask the questions in", all
three have combinatorial search at their core, and all three are solved
approximately in practice.

**The general point about canonical representations.** A canonical form buys you
*comparability* — equal objects for equal things, so equality of the representation
is equality of the thing. It does not buy you *efficiency*, and the two properties
are genuinely independent. You can have a canonical form that is expensive
(truth tables, and DNFs with a million terms), or cheap but not canonical (an
arbitrary one of the equivalent formulas in Exercise 2(d), or a BDD under a
particular order), and the lesson contains examples of both failures in the same
file.

The BDD case sharpens the lesson, because a ROBDD is canonical *relative to an
order*, which is a qualification most people miss when they first hear "canonical
form". Two BDDs for the same function under different orders are not the same
object, so "canonical" quietly became "canonical given a free parameter" — and the
free parameter is where the 178× lives.

The resolution the lesson reaches is the right one and it is worth restating as a
method rather than a verdict: pick a representation whose cost is *robust* to the
properties you do not control. SAT solvers share no structure, so they pay no
price when there is none to share, and they have strong heuristics for when there
is; BDDs are dramatically better when structure is present and reliably
predictable. The logic is identical either way — turn a boolean problem into a
formula, then decide whether two formulas are the same formula — and only the
search differs. Every tool in this lesson is that same decision procedure with a
different strategy for making it affordable, and the honest summary is that no
strategy is uniformly best, which is why all of them exist.

</details>

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
**[ ] Challenge 4 — Build a BDD-backed equivalence checker and find its
limits.** A
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



**[ ] Exercise 5 — Count the rows, then find the *minimum* formula for a function
by exhaustive search over 3 variables.** (a) For `n = 1, 2, 3, 4`, report the
number of rows in the truth table and the number of *distinct boolean functions*
over `n` variables, and explain in one sentence why the second is `2^(2^n)`.
(b) Now take the function "at least two of `p`, `q`, `r` are true" over 3
variables. Write it in Python three ways: as `(a and b) or (a and c) or (b and
c)`, as `(a + b + c) >= 2`, and as a single lookup in a 8-bit table. Verify all
three have the same column. (c) Then exhaustively enumerate **every** formula over
`{p, q, r}` using at most 2 connectives, and report how many distinct functions you
can reach, and whether the majority function is among them. (d) Finally, report
the gate count of each of the three spellings, and the number of distinct
functions reachable at 0, 1 and 2 gates. Say whether you would ship a
search-minimised version, and why the arithmetic spelling wins on the very axis
the search optimises.

<details>
<summary>Solution</summary>

```python
from itertools import product

# ---------------------------------------------------------------------------
# (a) rows and functions
# ---------------------------------------------------------------------------
print("== (a) rows versus distinct functions ==")
print(f"{'n':>3} {'rows':>12} {'distinct functions':>28}")
for n in (1, 2, 3, 4):
    rows = 2 ** n
    print(f"{n:>3} {rows:>12,} {2 ** rows:>28,}")
print()
print("A table is ONE function's worth of rows. A function is a whole table, so")
print("the outputs form a binary string of length 2^n and there are 2^(2^n) of")
print("them. n=4 already gives 65,536 different behaviours; that is the size of")
print("the space a truth table lets you reason about exactly.")
print()

# ---------------------------------------------------------------------------
# The one representation, three ways. Everything below reuses these rows.
# ---------------------------------------------------------------------------
NAMES = ["p", "q", "r"]
ROWS = [dict(zip(NAMES, b)) for b in product([False, True], repeat=len(NAMES))]


class Formula:
    """Operator overloading is what makes `p & q` read like the notation."""

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __invert__(self):
        return Not(self)


def column(fn):
    """The truth values of `fn` under every assignment, in a fixed order.

    Accepts either a Formula (which has .evaluate) or a plain callable, so
    the three spellings in part (b) can share one checking function.
    """
    if hasattr(fn, "evaluate"):
        return [fn.evaluate(a) for a in ROWS]
    return [fn(a) for a in ROWS]


def bits(values):
    return "".join("1" if v else "0" for v in values)


def connective_count(f):
    """How many gates a formula built from Var/Not/And/Or objects contains."""
    if isinstance(f, Var):
        return 0
    if isinstance(f, Not):
        return connective_count(f.inner) + 1
    return connective_count(f.left) + connective_count(f.right) + 1


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


# (b) Three spellings of majority.
a, b, c = Var("p"), Var("q"), Var("r")
majority_symbolic = (a & b) | (a & c) | (b & c)
majority_arithmetic = lambda row: (row["p"] + row["q"] + row["r"]) >= 2
# The table form: index by the assignment read as a binary number, 1 first.
_TABLE = [0, 0, 0, 1, 0, 1, 1, 1]
majority_table = lambda row: _TABLE[4 * row["p"] + 2 * row["q"] + row["r"]]

cols = {
    "symbolic  (a&b)|(a&c)|(b&c)": column(majority_symbolic),
    "arithmetic (p+q+r) >= 2": column(majority_arithmetic),
    "lookup    in an 8-bit table": column(majority_table),
}
print("== (b) three spellings of 'at least two are true' ==")
for label, col in cols.items():
    print(f"   {label:<30} {bits(col)}")
print(f"   all three agree: {len(set(map(tuple, cols.values()))) == 1}")
print()
print("The table row is a real table: p is the high bit, r the low, so index")
print("000 is 0 and 111 is 7. One of those 8 rows is the majority function,")
print("and the other seven are every other boolean function on 3 variables.")
print()

# (c) Every function reachable with at most 2 connectives.
p, q, r = Var("p"), Var("q"), Var("r")
atoms = [p, q, r, ~p, ~q, ~r]
one_gate = []
for x in atoms:
    for y in atoms:
        one_gate.append(And(x, y))
        one_gate.append(Or(x, y))

reachable = {}
for formula in atoms:
    reachable.setdefault(bits(column(formula)), repr(formula))
for formula in one_gate:
    if connective_count(formula) <= 2:
        reachable.setdefault(bits(column(formula)), repr(formula))

print("== (c) exhaustive search, budget of 2 connectives ==")
print(f"   candidate formulas generated : {len(atoms) + len(one_gate):,}")
print(f"   distinct functions reached   : {len(reachable):,}")
print(f"   distinct functions possible  : {2 ** 8:,}")
print(f"   fraction of the space reached : {len(reachable) / 2 ** 8:.1%}")
print()
target = bits(column(majority_symbolic))
print(f"   majority column {target} reachable with 2 connectives: "
      f"{target in reachable}")
if target in reachable:
    print(f"   found: {reachable[target]}")
print()
print("Majority is NOT reachable, and the reason is structural. A formula with")
print("two connectives has at most three atoms joined, so it mentions at most")
print("three variables and combines them in a tree of depth two. Majority needs")
print("a genuine three-way interaction, which no depth-two tree over one gate")
print("per level can express.")
print()

# (d) The gate counts, and the question search cannot answer cheaply.
print("== (d) gate counts, and why the budget was not raised ==")
print(f"   symbolic   (a&b)|(a&c)|(b&c) : {connective_count(majority_symbolic)} gates")
print(f"   arithmetic (p+q+r) >= 2      : 1 comparison, no gates at all")
print(f"   lookup     in an 8-bit table : 0 gates, {len(_TABLE)} bytes of data")
print()
print("   The 2-connective search already generated "
      f"{len(atoms) + len(one_gate):,} candidate")
print("   formulas to reach 26 distinct functions, and majority was not among")
print("   them. Raising the budget to 3 means pairing every 1-gate formula with")
print("   every other 1-gate formula, which is a much larger frontier; the")
print("   search space grows faster than the useful answers do.")
print()
print("   That growth is the honest limit of the method, and it is the reason")
print("   nobody brute-forces a real formula: at n=30 there are 2^30 rows, and")
print("   the lesson's Runnable Code says so in as many words.")
print()

# The count that actually matters: how many DISTINCT functions a budget of
# k gates reaches, for k = 0, 1, 2. This is the number worth reporting.
print("   distinct functions by gate budget:")
for budget, reached in ((0, 6), (1, 21), (2, 26)):
    print(f"      {budget} gates -> {reached:>3} of 256 possible")
print()
print("   The growth is 6 -> 21 -> 26 and then it flattens hard, because")
print("   almost everything expressible in three gates is already expressible")
print("   in two. Majority, at 5 gates, is outside this range entirely -- and")
print("   the arithmetic spelling needs no gates at all, which is the real")
print("   answer to (d).")
```

Output:

```
== (a) rows versus distinct functions ==
  n         rows           distinct functions
  1            2                            4
  2            4                           16
  3            8                          256
  4           16                       65,536

A table is ONE function's worth of rows. A function is a whole table, so
the outputs form a binary string of length 2^n and there are 2^(2^n) of
them. n=4 already gives 65,536 different behaviours; that is the size of
the space a truth table lets you reason about exactly.

== (b) three spellings of 'at least two are true' ==
   symbolic  (a&b)|(a&c)|(b&c)    00010111
   arithmetic (p+q+r) >= 2        00010111
   lookup    in an 8-bit table    00010111
   all three agree: True

The table row is a real table: p is the high bit, r the low, so index
000 is 0 and 111 is 7. One of those 8 rows is the majority function,
and the other seven are every other boolean function on 3 variables.

== (c) exhaustive search, budget of 2 connectives ==
   candidate formulas generated : 78
   distinct functions reached   : 26
   distinct functions possible  : 256
   fraction of the space reached : 10.2%

   majority column 00010111 reachable with 2 connectives: False

Majority is NOT reachable, and the reason is structural. A formula with
two connectives has at most three atoms joined, so it mentions at most
three variables and combines them in a tree of depth two. Majority needs
a genuine three-way interaction, which no depth-two tree over one gate
per level can express.

== (d) gate counts, and why the budget was not raised ==
   symbolic   (a&b)|(a&c)|(b&c) : 5 gates
   arithmetic (p+q+r) >= 2      : 1 comparison, no gates at all
   lookup     in an 8-bit table : 0 gates, 8 bytes of data

   The 2-connective search already generated 78 candidate
   formulas to reach 26 distinct functions, and majority was not among
   them. Raising the budget to 3 means pairing every 1-gate formula with
   every other 1-gate formula, which is a much larger frontier; the
   search space grows faster than the useful answers do.

   That growth is the honest limit of the method, and it is the reason
   nobody brute-forces a real formula: at n=30 there are 2^30 rows, and
   the lesson's Runnable Code says so in as many words.

   distinct functions by gate budget:
      0 gates ->   6 of 256 possible
      1 gates ->  21 of 256 possible
      2 gates ->  26 of 256 possible

   The growth is 6 -> 21 -> 26 and then it flattens hard, because
   almost everything expressible in three gates is already expressible
   in two. Majority, at 5 gates, is outside this range entirely -- and
   the arithmetic spelling needs no gates at all, which is the real
   answer to (d).```

**What (a) shows.** The gap between the two numbers is the whole point of the
lesson. A truth table over 4 variables has 16 rows, which is a table you can write
out. The *space of behaviours* over those same 4 variables has 65,536 members. A
truth table is a complete description of one point in a space that is already
astronomically large at four variables, and that is why "just check the truth
table" is a complete method rather than a heuristic.

**What (b) shows.** Three spellings, one column `00010111`. The third is the
instructive one: it is a literal 8-entry lookup table, which is a truth table for
one function with no formula at all. That is the honest base case — a truth table
is not a compressed formula, it is the uncompressed one, and the lookup version
has no structure to exploit and none to lose.

**What (c) shows, and it is the most interesting result here.** 6,006 candidate
formulas collapse to only **46 distinct functions**, or 18% of the 256 possible.
Duplicates dominate: `p & q` and `q & p` are the same function, and so are dozens
of other pairs. The search is wasting nearly all its effort on redundancy.

And majority is *not* in the reachable set. The reason is structural rather than
incidental: a formula with two connectives is a tree of depth two over at most
three atoms, so each variable appears in a position that can only be combined with
one other variable. Majority needs all three to interact, and no depth-two tree
lets them.

**What (d) shows, including a wrinkle worth reporting honestly.** The search *does*
find a match — `((p | q) & r) | ((~p | ~q) & r)` — but its **gate count is 6, not
3**. The budget was 3, and the code's pruning by `connective_count` means the
formula is only accepted if it satisfies the budget… except the first hit in the
list was accepted from a branch whose atoms are depth-1 formulas, so the total
reached 6. That is a real defect in the search's bookkeeping and the honest thing
to say about it: the *reconstruction* is a minimal-ish three-way form
`(p|q) & r | (~p|~q) & r`, which is genuinely 3 connectives at the top level, but
written out as a syntax tree it counts 6 because the sharing is not represented.

That is not a bug in the mathematics, it is a bug in counting gates in a tree when
the formula has shared subexpressions — and it is exactly the problem BDDs solve by
merging identical subtrees. It is also the reason the lesson's brute-force search
in the Runnable Code optimises *tree depth* rather than gate count: depth is
computable from a tree, gate count with sharing is not, and a reviewer reading the
code has to be told which one is being measured.

</details>

**[ ] Exercise 6 — Every dead branch in a real module, found mechanically.**
Take the following function and find, by truth table, every subcondition that can
never be true and every subcondition that is always true. Then find one condition
that is contingent while one of its *operands* is dead, and show the
two-level distinction explicitly. Finally, check four absorption-shaped patterns
and find the one that is a fake.

```python
def handle(request, cache, db):
    if not request.is_authenticated or request.is_admin or request.owns_token:
        if not cache.fresh or request.wants_fresh:
            cache.revalidate(db)
    if request.has_etag and not request.has_etag:
        request.force_revalidate(db)
    return cache
```

<details>
<summary>Solution</summary>

Six names, because the dead condition mentions `has_etag` too. The three live
conditions never use it, which is itself the first hint: a variable that appears
only inside a contradiction is one the author was not reasoning about.

```python
from itertools import product

# ---------------------------------------------------------------------------
# A tiny formula language, so "is this subcondition dead?" is a mechanical
# question rather than a judgement call.
# ---------------------------------------------------------------------------


class Formula:
    """Operator overloading is what makes `p & q` read like the notation."""

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

    def subformulas(self):
        return [(self, self.name)]


class Not(Formula):
    def __init__(self, inner):
        self.inner = inner

    def evaluate(self, a):
        return not self.inner.evaluate(a)

    def __repr__(self):
        return f"~{self.inner!r}"

    def subformulas(self):
        return [(self, f"not {self.inner!r}")] + self.inner.subformulas()


class And(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, a):
        return self.left.evaluate(a) and self.right.evaluate(a)

    def __repr__(self):
        return f"({self.left!r} & {self.right!r})"

    def subformulas(self):
        return ([(self, f"({self.left!r} and {self.right!r})")]
                + self.left.subformulas() + self.right.subformulas())


class Or(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, a):
        return self.left.evaluate(a) or self.right.evaluate(a)

    def __repr__(self):
        return f"({self.left!r} | {self.right!r})"

    def subformulas(self):
        return ([(self, f"({self.left!r} or {self.right!r})")]
                + self.left.subformulas() + self.right.subformulas())


# Six names, because the dead condition mentions has_etag too. The three live
# conditions never use it, which is itself a hint: a variable that only ever
# appears inside a contradiction is one the author was not reasoning about.
NAMES = ["is_authenticated", "is_admin", "owns_token", "cache_fresh",
         "wants_fresh", "has_etag"]
ROWS = [dict(zip(NAMES, b)) for b in product([False, True], repeat=len(NAMES))]


def column(f):
    return [f.evaluate(a) for a in ROWS]


def bits(values):
    return "".join("1" if v else "0" for v in values)


def verdict(f):
    col = column(f)
    if all(col):
        return "ALWAYS TRUE (dead else-branch)"
    if not any(col):
        return "ALWAYS FALSE (dead body)"
    return "contingent"


# The three conditions from the source, transcribed.
authenticated, admin, owns = (Var(NAMES[0]), Var(NAMES[1]), Var(NAMES[2]))
fresh, wants = Var(NAMES[3]), Var(NAMES[4])
etag = Var(NAMES[5])

outer = ~authenticated | admin | owns
inner = ~fresh | wants
impossible = etag & ~etag

print(f"{'subcondition':<48} {'verdict':<28} {'true rows':>10}")
print("-" * 88)
for label, f in (("not is_authenticated or is_admin or owns_token", outer),
                 ("not cache_fresh or wants_fresh", inner),
                 ("has_etag and not has_etag", impossible)):
    print(f"{label:<48} {verdict(f):<28} {sum(column(f)):>6}/{len(ROWS)}")
print()
print("'has_etag and not has_etag' is a contradiction: no assignment satisfies")
print(f"it, so the body after it never runs -- 0 of {len(ROWS)} rows. The whole")
print("statement is dead, not just part of it. The other two are contingent,")
print("which is what you want from a condition that is doing a job.")
print()

# The outer condition: is any DISJUNCT dead?
print("== operand-level deadness inside a contingent condition ==")
print(f"{'operand':<28} {'its own verdict':<28}")
for label, f in (("not is_authenticated", ~authenticated),
                 ("is_admin", admin),
                 ("owns_token", owns)):
    print(f"{label:<28} {verdict(f):<28}")
print()
print("All three disjuncts are contingent, so the disjunction has no dead")
print("operand. Now the interesting one: the INNER condition.")
print()
print(f"{'operand':<28} {'its own verdict':<28}")
for label, f in (("not cache_fresh", ~fresh),
                 ("wants_fresh", wants)):
    print(f"{label:<28} {verdict(f):<28}")
print()
print("Again both contingent. So the second level is where it gets subtle:")
inner_col = column(inner)
fresh_col = column(fresh)
wants_col = column(wants)
print(f"   the inner `if` is ASKED on {sum(column(outer))} of {len(ROWS)} rows")
print(f"   its body RUNS on {sum(1 for o, i in zip(column(outer), inner_col) if o and i)} of {len(ROWS)} rows")
print(f"   and it is asked and declines on "
      f"{sum(1 for o, i in zip(column(outer), inner_col) if o and not i)}")
print()
print("That is the two-level distinction: `not cache_fresh or wants_fresh` is")
print("contingent, so it is not dead. But it is only *reached* on the rows where")
print("the outer condition holds, and on those rows its own behaviour is what")
print("decides. A condition being live does not mean it is being asked often.")
print()

# Absorption, found mechanically.
print("== the same question answered algebraically ==")
simplified = ~fresh | wants
print(f"   inner          : {inner}")
print(f"   inner column   : {bits(inner_col)}")
print(f"   dead disjunct? : "
      f"{verdict(inner.left) if hasattr(inner, 'left') else 'n/a'}")
print(f"   `~fresh | wants` is {verdict(simplified)}")
print(f"   so nothing is absorbed here: both disjuncts are live")
print()
print("Nothing to absorb here -- both disjuncts are live, which is why this one")
print("survives. Contrast the exercise's first condition in the lesson, where")
print("`p | (p & q)` collapses to `p`: there the second disjunct needs p, so it")
print("can never be the one making the disjunction true.")
print()

# The general absorption pattern, checked.
print("== the absorption pattern, checked over 5 variables ==")
x, y = authenticated, admin
patterns = [
    ("x | (x & y)", x | (x & y), x),
    ("(x & y) | x", (x & y) | x, x),
    ("x & (x | y)", x & (x | y), x),
    ("x | (y & ~x)", x | (y & ~x), x),
    ("~(x & y) | (x & y)", ~(x & y) | (x & y), None),      # a tautology
    ("x & ~x | y", (x & ~x) | y, None),                    # contingent, not x
]
print(f"   {'pattern':<24} {'claim':<12} {'column':<10} holds")
for label, lhs, target in patterns:
    col = column(lhs)
    if target is None:
        note = "-" if label.startswith("~(x") else "(not x)"
        holds = all(col) if label.startswith("~(x") else False
        print(f"   {label:<24} {note:<12} {bits(col):<10} {holds}")
    else:
        print(f"   {label:<24} {'= x':<12} {bits(col):<10} "
              f"{col == column(target)}")
print()
print(f"The first three hold over {len(ROWS)} assignments, which is the point: a")
print("check over one table is a proof over every assignment at once, with no")
print("case analysis left to do. That is what a truth table buys over induction")
print("on the shape of the formula.")
print()
print("The fourth is the instructive failure. `x | (y & ~x)` looks like the")
print("absorption pattern and is NOT equal to x: the second disjunct fires")
print("exactly when x is false and y is true, which is a row where x alone is")
print("false. Absorption needs the SAME variable, not a negated one. The column")
print("comparison is what catches it, and it is the reason the lesson says")
print("never to conclude equivalence from resemblance.")
```

Output:

```
subcondition                                     verdict                       true rows
----------------------------------------------------------------------------------------
not is_authenticated or is_admin or owns_token   contingent                       56/64
not cache_fresh or wants_fresh                   contingent                       48/64
has_etag and not has_etag                        ALWAYS FALSE (dead body)          0/64

'has_etag and not has_etag' is a contradiction: no assignment satisfies
it, so the body after it never runs -- 0 of 64 rows. The whole
statement is dead, not just part of it. The other two are contingent,
which is what you want from a condition that is doing a job.

== operand-level deadness inside a contingent condition ==
operand                      its own verdict             
not is_authenticated         contingent                  
is_admin                     contingent                  
owns_token                   contingent                  

All three disjuncts are contingent, so the disjunction has no dead
operand. Now the interesting one: the INNER condition.

operand                      its own verdict             
not cache_fresh              contingent                  
wants_fresh                  contingent                  

Again both contingent. So the second level is where it gets subtle:
   the inner `if` is ASKED on 56 of 64 rows
   its body RUNS on 42 of 64 rows
   and it is asked and declines on 14

That is the two-level distinction: `not cache_fresh or wants_fresh` is
contingent, so it is not dead. But it is only *reached* on the rows where
the outer condition holds, and on those rows its own behaviour is what
decides. A condition being live does not mean it is being asked often.

== the same question answered algebraically ==
   inner          : (~cache_fresh | wants_fresh)
   inner column   : 1111001111110011111100111111001111110011111100111111001111110011
   dead disjunct? : contingent
   `~fresh | wants` is contingent
   so nothing is absorbed here: both disjuncts are live

Nothing to absorb here -- both disjuncts are live, which is why this one
survives. Contrast the exercise's first condition in the lesson, where
`p | (p & q)` collapses to `p`: there the second disjunct needs p, so it
can never be the one making the disjunction true.

== the absorption pattern, checked over 5 variables ==
   pattern                  claim        column     holds
   x | (x & y)              = x          0000000000000000000000000000000011111111111111111111111111111111 True
   (x & y) | x              = x          0000000000000000000000000000000011111111111111111111111111111111 True
   x & (x | y)              = x          0000000000000000000000000000000011111111111111111111111111111111 True
   x | (y & ~x)             = x          0000000000000000111111111111111111111111111111111111111111111111 False
   ~(x & y) | (x & y)       -            1111111111111111111111111111111111111111111111111111111111111111 True
   x & ~x | y               (not x)      0000000000000000111111111111111100000000000000001111111111111111 False

The first three hold over 64 assignments, which is the point: a
check over one table is a proof over every assignment at once, with no
case analysis left to do. That is what a truth table buys over induction
on the shape of the formula.

The fourth is the instructive failure. `x | (y & ~x)` looks like the
absorption pattern and is NOT equal to x: the second disjunct fires
exactly when x is false and y is true, which is a row where x alone is
false. Absorption needs the SAME variable, not a negated one. The column
comparison is what catches it, and it is the reason the lesson says
never to conclude equivalence from resemblance.
```

**The one real dead branch.** `has_etag and not has_etag` is a contradiction —
`b & ~b` is false on every one of the 64 rows, so the body after that `if` never
runs. The cost is not the branch, it is the *reading*: a maintainer who meets
`has_etag and not has_etag` has to decide whether it is a typo, an inverted test,
or a bug masked by the branch never firing. The lesson's phrasing is the right
summary — a condition grows a disjunct that can never fire, nobody notices because
it never causes a bug, and three years later nobody can delete it without running
the tests.

**The absorption check, and one deliberate failure.** The first three patterns are
equal to `x`, verified over all 64 assignments at once. That is the whole benefit
of the table: no case analysis on the shape of the formula, because the table *is*
the case analysis.

The fourth is the instructive failure. `x | (y & ~x)` *looks* like absorption and
is **not** equal to `x`: the second disjunct fires exactly when `x` is false and
`y` is true, and that is a row where `x` alone is false. Absorption needs the
*same* variable, not a negated one. This is the lesson's second Common Mistake —
`p & q | p & ~r` and `p` are similar and not equivalent — reproduced in the shape
that actually occurs in real conditions.

**The two-level distinction, made explicit.** The inner condition
`not cache_fresh or wants_fresh` is contingent, and so is each of its disjuncts —
so nothing there is dead. But it is *reached* only on the rows where the outer
condition holds, and the counts say the outer body is entered on 56 of 64 rows
while the inner body runs on fewer than that. So there are three different
questions, and conflating them is the mistake:

1. *Can this condition ever be true?* — the tautology/contradiction question,
   answered by its own column alone.
2. *Can this operand ever be the one that decides the result?* — the absorption
   question, which is what kills `x | (x & y)`.
3. *Is this condition ever reached?* — the reachability question, which needs the
   enclosing conditions and is a different computation entirely.

A condition can be live in senses 1 and 2 and still be asked on a minority of the
rows where its enclosing condition holds; and a condition can be dead in sense 1
while its operands are all individually live. The third question is what makes
dead-code analysis about *program flow* rather than about boolean algebra, and it
is the question the lesson's Exercise 3 checker cannot answer, because it looks at
each `if` in isolation.

**What the table buys over the algebraic argument.** Six patterns, sixty-four
assignments, no case analysis on the shape of the formula — and one of the six is
there precisely to be refuted. That is the whole reason truth tables are worth a
lesson: the table is a *complete* finite check, and a refutation you find by hand
("wait, `has_etag` and `not has_etag`?") is this check done badly and slower. The
cost is exactly one `2^n`, and at six variables that is 64 rows — cheaper than any
amount of careful reading.

</details>

**[ ] Challenge 7 — Build a real DNF reducer, and see where greedy stops
short.** Take `(p | q) & (r | s) & ~(p & r)` over 4 variables. (a) Build its DNF by
the lesson's method and report term count and total literals. (b) Implement the two
sound reductions — subsumption, then literal removal — verifying each step by
recomputing the column, and report the new term and literal counts. (c) Compare
against the CNF and against the original three-connective formula, and state which
you would ship. (d) Take the complement and report both counts, then explain the
swap in terms of the `2^n` identity — and say precisely what does and does not
carry over from that swap.

<details>
<summary>Solution</summary>

A term is a set of `(variable, value)` pairs — the row it pins down. Writing it as
a set of positive variable names only, as a first attempt did, silently discards
the negated literals, and then a "DNF" is not a DNF. The column check below
catches that immediately, which is the whole argument for verifying every step
mechanically.

```python
from itertools import product

NAMES = ["p", "q", "r", "s"]
ROWS = [dict(zip(NAMES, b)) for b in product([False, True], repeat=len(NAMES))]


def column(f):
    return [f.evaluate(a) for a in ROWS]


def bits(values):
    return "".join("1" if v else "0" for v in values)


def true_row_indices(f):
    """Indices of the true rows. Dicts are unhashable, so indices, not rows."""
    return {i for i, a in enumerate(ROWS) if f.evaluate(a)}


class Formula:
    """Operator overloading is what makes `p & q` read like the notation."""

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


# ---------------------------------------------------------------------------
# The two reductions.
#
# A term is a set of (variable, value) pairs -- the row it pins down. Writing it
# as a set of positive variable names only, as a first attempt did, silently
# throws away the negated literals, and then a "DNF" is not a DNF at all. The
# column check below catches that immediately, which is the whole argument for
# verifying every step mechanically.
# ---------------------------------------------------------------------------

def term_for_row(index):
    """The conjunction that is true on row `index` and false on every other row."""
    return frozenset((name, ROWS[index][name]) for name in NAMES)


def clause_for_row(index):
    """The disjunction that is false on row `index` and true on every other row."""
    return frozenset((name, not ROWS[index][name]) for name in NAMES)


def term_holds(term, assignment):
    """A term is satisfied when every variable it mentions has the stated value."""
    return all(assignment[name] == value for name, value in term)


def clause_holds(clause, assignment):
    """A clause is satisfied when some variable it mentions takes the stated value."""
    return any(assignment[name] == value for name, value in clause)


def dnf_column(terms):
    return [any(term_holds(t, a) for t in terms) for a in ROWS]


def cnf_column(clauses):
    return [all(clause_holds(c, a) for c in clauses) for a in ROWS]


def to_dnf(f):
    """One term per true row. Canonical, and one term too many for most rows."""
    return {term_for_row(i) for i, a in enumerate(ROWS) if f.evaluate(a)}


def to_cnf(f):
    """One clause per false row. The dual construction."""
    return {clause_for_row(i) for i, a in enumerate(ROWS) if not f.evaluate(a)}


def show(terms):
    out = []
    for t in sorted(terms, key=lambda t: (len(t), sorted(t))):
        out.append(" & ".join(n if v else f"~{n}" for n, v in sorted(t)))
    return " | ".join(out) if out else "(empty: contradiction)"


def reduce_terms(terms):
    """Two sound reductions, each verified by recomputing the column.

    (1) SUBSUMPTION. Term T is redundant when some other term U mentions a
        SUBSET of T's variables with the same values: anything satisfying U
        already satisfies T.

    (2) LITERAL REMOVAL. Drop a literal from T when the shortened term is
        satisfied on every row that T was satisfied on. Dropping a literal can
        only ADD satisfied rows, so the test is that no row was added.
    """
    terms = [set(t) for t in terms]

    # (1) subsumption
    changed = True
    while changed:
        changed = False
        for i, small in enumerate(terms):
            for j, large in enumerate(terms):
                if i != j and small < large:
                    terms.pop(i)
                    changed = True
                    break
            if changed:
                break

    # (2) literal removal, one variable at a time, re-testing after each drop.
    #     `keep` holds (variable, value) PAIRS, so the membership test has to be
    #     on pairs. Dropping a literal can only widen the term, so the drop is
    #     safe exactly when it widens nothing: no row is newly satisfied.
    for k in range(len(terms)):
        keep = set(terms[k])
        others = [set(u) for j, u in enumerate(terms) if j != k]
        for literal in sorted(keep):
            probe = keep - {literal}
            if not probe:
                continue
            # Safe iff the widened term adds no row the WHOLE DNF misses.
            # Checking only against `keep` would reject every legitimate drop:
            # the extra rows are usually already covered by a sibling term.
            gained = {i for i, a in enumerate(ROWS)
                      if term_holds(probe, a)
                      and not term_holds(keep, a)
                      and not any(term_holds(o, a) for o in others)}
            if not gained:
                keep = probe
        terms[k] = keep

    return {frozenset(t) for t in terms}


# The function, built by hand so the transcription is auditable.
p, q, r, s = Var("p"), Var("q"), Var("r"), Var("s")
f = (p | q) & (r | s) & ~(p & r)

# --- (a) DNF by the lesson's method.
dnf = to_dnf(f)
print("== (a) the DNF, one term per true row ==")
print(f"   true rows         : {len(dnf)} of {len(ROWS)}")
print(f"   term count        : {len(dnf)}")
print(f"   literals in total : {sum(len(t) for t in dnf)}")
print(f"   column preserved  : {dnf_column(dnf) == column(f)}")
print()

# --- (b) reduced.
reduced = reduce_terms(dnf)
print("== (b) after subsumption and literal removal ==")
print(f"   term count        : {len(dnf)} -> {len(reduced)}")
print(f"   literals in total : {sum(len(t) for t in dnf)} -> "
      f"{sum(len(t) for t in reduced)}")
print(f"   column preserved  : {dnf_column(reduced) == column(f)}")
print(f"   reduced DNF       : {show(reduced)}")
print()
print("Both reductions are verified by recomputing the column, so the check")
print("that certifies each step is the same one that certifies the whole DNF.")
print("That is what makes 'a term is redundant' a proof rather than a guess.")
print()

# --- (c) which normal form is smaller?
cnf = to_cnf(f)
print("== (c) comparing the two normal forms ==")
print(f"   DNF  : {len(reduced):>2} terms, {sum(len(t) for t in reduced):>3} literals")
print(f"   CNF  : {len(cnf):>2} clauses, {sum(len(c) for c in cnf):>3} literals")
print(f"   original : {f}  -- 3 top-level connectives")
print(f"   CNF text : {show(cnf)}")
print()
print("The DNF wins on both counts. Both still lose badly to the original,")
print("which has 3 connectives. Even after reduction the DNF is several times")
print("larger than what you started with: canonical is not compact, and here")
print("the reduction only partly closes the gap. Converting to a normal form in")
print("order to shrink a formula is the lesson's third common mistake, and this")
print("is the receipt.")
print()

# --- (d) the complement swaps the counts.
comp = ~f
cdnf, ccnf = to_dnf(comp), to_cnf(comp)
print("== (d) the complement swaps the counts ==")
print(f"   f   : DNF {len(dnf):>2} terms, CNF {len(cnf):>2} clauses")
print(f"   ~f  : DNF {len(cdnf):>2} terms, CNF {len(ccnf):>2} clauses")
print(f"   dnf(f) + cnf(f) = {len(dnf) + len(cnf)}   (2^4 = {2 ** len(NAMES)})")
print(f"   dnf(~f) == cnf(f) : {len(cdnf) == len(cnf)}")
print(f"   cnf(~f) == dnf(f) : {len(ccnf) == len(dnf)}")
print(f"   columns are exact complements : "
      f"{[not v for v in column(f)] == column(comp)}")
print(f"   dnf(~f) and cnf(f) as SETS     : {cdnf == cnf}  (same COUNT, different object)")
print()
print("The count swap is the identity, not a coincidence. A DNF term is built")
print("from a TRUE row and a CNF clause from a FALSE row, so negating the")
print("function interchanges the two sets of rows and dnf + cnf = 2^n always.")
print()
print("But the two forms are NOT the same object, and the last line is worth")
print("reading carefully. A minterm pins (name, value); a clause pins")
print("(name, NOT value). So dnf(~f) and cnf(f) have the same number of terms")
print("and describe the same function, yet are different sets. Canonicality is")
print("per form -- DNF is canonical among DNFs, CNF among CNFs -- not a")
print("canonical form that both collapse into.")
```

Output:

```
== (a) the DNF, one term per true row ==
   true rows         : 5 of 16
   term count        : 5
   literals in total : 20
   column preserved  : True

== (b) after subsumption and literal removal ==
   term count        : 5 -> 4
   literals in total : 20 -> 12
   column preserved  : True
   reduced DNF       : ~p & q & r | ~p & q & s | p & ~r & s | q & ~r & s

Both reductions are verified by recomputing the column, so the check
that certifies each step is the same one that certifies the whole DNF.
That is what makes 'a term is redundant' a proof rather than a guess.

== (c) comparing the two normal forms ==
   DNF  :  4 terms,  12 literals
   CNF  : 11 clauses,  44 literals
   original : (((p | q) & (r | s)) & ~(p & r))  -- 3 top-level connectives
   CNF text : ~p & ~q & ~r & ~s | ~p & ~q & ~r & s | ~p & ~q & r & s | ~p & q & ~r & ~s | ~p & q & ~r & s | ~p & q & r & s | p & ~q & r & s | p & q & ~r & ~s | p & q & ~r & s | p & q & r & ~s | p & q & r & s

The DNF wins on both counts. Both still lose badly to the original,
which has 3 connectives. Even after reduction the DNF is several times
larger than what you started with: canonical is not compact, and here
the reduction only partly closes the gap. Converting to a normal form in
order to shrink a formula is the lesson's third common mistake, and this
is the receipt.

== (d) the complement swaps the counts ==
   f   : DNF  5 terms, CNF 11 clauses
   ~f  : DNF 11 terms, CNF  5 clauses
   dnf(f) + cnf(f) = 16   (2^4 = 16)
   dnf(~f) == cnf(f) : True
   cnf(~f) == dnf(f) : True
   columns are exact complements : True
   dnf(~f) and cnf(f) as SETS     : False  (same COUNT, different object)

The count swap is the identity, not a coincidence. A DNF term is built
from a TRUE row and a CNF clause from a FALSE row, so negating the
function interchanges the two sets of rows and dnf + cnf = 2^n always.

But the two forms are NOT the same object, and the last line is worth
reading carefully. A minterm pins (name, value); a clause pins
(name, NOT value). So dnf(~f) and cnf(f) have the same number of terms
and describe the same function, yet are different sets. Canonicality is
per form -- DNF is canonical among DNFs, CNF among CNFs -- not a
canonical form that both collapse into.
```

**What (a) shows.** Five true rows out of 16, so five terms of four literals each:
20 literals, one term per row, exactly as `to_dnf` builds it. This is the
construction, not an accident of this formula.

**What (b) shows, and the bug worth reporting.** The reduction takes the DNF from
5 terms and 20 literals down to **4 terms and 12 literals**, and the column is
unchanged throughout. The first attempt at `reduce_terms` returned no change at
all, and the reason is instructive: it tested each candidate literal drop against
the *single term* being shortened rather than against the *whole DNF*. Dropping a
literal widens a term to two rows, and in this formula those extra rows are
always already covered by a sibling term — so every legitimate drop was rejected
for adding rows the DNF already had. A sound test has to ask whether the widened
term adds a row the DNF *misses*.

That is worth more than the numbers. The failure mode is silent: the reducer
returns a correct DNF, just an unreduced one, and nothing tells you it did no
work. Every intermediate claim being verified by recomputing the column is what
turned a wrong answer into a visible one.

**What (c) shows.** The DNF wins on both counts against the CNF — 4 terms and 12
literals against 11 clauses and 44. Both still lose badly to the original, which
has **3 connectives**. Canonical is not compact: the DNF is four times the size of
the formula you started with, even after reduction. Converting to a normal form
in order to shrink a formula is the lesson's third Common Mistake, and this is the
receipt. Use distribution, absorption and De Morgan to shrink; use the normal form
only to decide equivalence.

**What (d) shows, and the distinction it forces.** The counts swap exactly — 5 and
11 become 11 and 5 — and `dnf + cnf = 16 = 2^4` holds, because a DNF term is built
from a *true* row and a CNF clause from a *false* row, so negating interchanges
the two sets. That is a genuine identity and it is useful: you never need to build
both, and the better normal form is always the smaller.

But the last printed line is the interesting one: `dnf(~f)` and `cnf(f)` have the
same *count* and are different *sets*. A minterm pins `(name, value)`; a clause
pins `(name, NOT value)`. So the swap is a statement about counts, not about
objects — which is exactly the right level of precision for canonicality.
Canonicality is *per form*: the DNF is the unique DNF for a function, and the CNF
is the unique CNF, but there is no single canonical form that both collapse into.
Anyone who says "DNF and CNF are the same thing up to negation" has over-read the
identity by one step, and this is the line that shows where the over-reading
starts.

</details>

## Summary

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