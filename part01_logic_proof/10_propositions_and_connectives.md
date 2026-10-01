# 10 — Propositions and Connectives

**Part**: part01_logic_proof · **Prerequisites**: 01 · **Time**: 30 min

---

## In Plain Words

Some sentences are true or false and stay that way no matter who says them.
"Two plus two is four" is one. "This request has a valid auth token" is one.
"Sort this list" is not, because it is an instruction rather than a claim.
"x is greater than five" is not either, until you say what x is.

A sentence that does have a definite truth value is called a proposition. The
point of logic is to study how propositions combine. Five words do almost all
the work: and, or, not, if-then, and if-and-only-if. This lesson is about what
those five words mean exactly, and the answer for the fourth one surprises
almost everybody.

The single most important thing in the lesson is that "if P then Q" does not
mean P and Q. It means something closer to "not P, or Q". Get that wrong and you
will write a security check that admits exactly the users it was supposed to
reject.

## Why Computer Science Cares

**Boolean conditions are propositions.** Every `if` you write takes a
proposition. Understanding what `not a or b` means relative to `not (a or b)`
is the difference between a working access check and one that fails open for the
precise users it was written to exclude.

**Implication is how specifications are written.** "If the request is not
authenticated then it must be rejected" is a proposition about every input.
Whether your handler satisfies it is a question of logic, not of testing.

**Short-circuit evaluation is an implementation of a connectives.** Python's
`and` stops at the first falsy operand, `or` at the first truthy one. That
behaviour only makes sense once you know these are connectives with specific
truth conditions.

**The `while` loop with a complex condition is a proposition to be negated
correctly.** "Keep going until nothing is left" is `while items:`, and getting
`while not items:` right requires reading `not` as binding to the whole
disjunction rather than to its first term.

**SAT solvers and equivalence checkers exist because of this material.** Every
hardware synthesis tool, every formal verification tool, and every compiler
constraint solver is working with the formulas in this lesson. Datasets, artifact
analysis, and program equivalence all compile down to "find an assignment that
makes this formula true".

**Type theory is this material with the domains filled in.** `∀α. α → α → α` is
literally "a function that takes two things of the same type and returns one of
that type".

## The Formal Version

**Definition.** A *proposition* is a declarative sentence that is either true or
false, but not both, and whose truth value does not depend on who is asking.

**Definition.** A *connective* is an operation that takes propositions and
produces a proposition.

**Definition.** Negation: for a proposition `P`, the proposition `¬P` is true
exactly when `P` is false. `¬¬P` is *logically equivalent* to `P`.

**Definition.** Conjunction: `P ∧ Q` is true exactly when both `P` and `Q` are
true.

**Definition.** Disjunction: `P ∨ Q` is true exactly when at least one of `P`
and `Q` is true. Note "at least one", not "exactly one". `P ∨ Q` is true when
both are true.

**Definition.** Implication: `P → Q` is true except in the one case where `P` is
true and `Q` is false. Equivalently, `P → Q` is false exactly when `P` is true
and `Q` is false.

**Definition.** Biconditional: `P ↔ Q` is true exactly when `P` and `Q` have the
same truth value, whether both true or both false.

**Definition.** Two propositions `P` and `Q` are *logically equivalent*, written
`P ≡ Q`, if they have the same truth value under every assignment. Not merely
"they happen to agree here", but "they agree everywhere".

**Definition.** A *tautology* is a proposition true under every assignment.
A *contradiction* is one false under every assignment. A *contingent*
proposition is neither, and most propositions you will meet are contingent.

**Definition.** The *principle of substitution for equivalence* (often called
Leibniz's law): if `P ≡ Q`, then `P` may be replaced by `Q` in any formula
without changing that formula's truth value. This is the formal justification
for every condition simplification you will ever do.

**Theorem.** `P → Q ≡ ¬P ∨ Q`.

*Why this is the central fact.* Read the definition of implication aloud: "true
except when `P` is true and `Q` is false". The disjunction `¬P ∨ Q` is false in
exactly that same case: it is false only when both `¬P` is false (so `P` is
true) and `Q` is false. Same false case, and a proposition is completely
determined by where it is false. So they are the same proposition. From this
one identity, the rest follow: `¬(P → Q) ≡ P ∧ ¬Q`, and the contrapositive
`P → Q ≡ ¬Q → ¬P`.

## Worked Example

The worked example is a security check, because that is where this material
actually costs money.

**The requirement, written as English.** "Deny the request unless the caller is
an administrator or a superuser."

**Step 1. Translate to a proposition.** Let `A` mean "the caller is an
administrator" and `S` mean "the caller is a superuser". Let `D` mean "deny".
The requirement is: if neither `A` nor `S`, then `D`. In symbols,
`¬(A ∨ S) → D`. Using the theorem, that is `¬¬(A ∨ S) ∨ D`, which simplifies to
`(A ∨ S) ∨ D`.

**Step 2. Simplify the logic.** A denial is granted only when at least one of
`A`, `S` holds. So the check is `if not (A or S): deny`. There is no other case.

**Step 3. Now write what a programmer writes under time pressure.**

```text
if not A or not S:
    deny()
```

**Step 4. Find where it differs.** `not A or not S` parses as `(¬A) ∨ (¬S)`. That
is true whenever `A` is false *or* `S` is false — that is, unless the caller is
**both** an administrator **and** a superuser. The correct version is
`not (A or S)`, true only when neither holds. Compare:

| A | S | `not (A or S)` (wanted) | `not A or not S` (written) |
| --- | --- | --- | --- |
| F | F | True — deny | True — deny |
| F | T | False — allow | True — **deny** |
| T | F | False — allow | True — **deny** |
| T | T | False — allow | False — allow |

**Step 5. Diagnose the mistake.** The programmer applied De Morgan *backwards*.
They turned `not (A or S)` into `¬A ∨ ¬S`, which is the rule for `not (A ∧ S)`.
They had the connective backwards.

**Step 6. Check whether Python would have caught it.** No, and this is the
important part. `not A or not S` is a perfectly well-formed Python expression
with a well-defined meaning. Python does not know what you meant. Neither does a
type checker, and in this case neither does a linter. The only defence is that
you can reason about the truth table, which is what this lesson is for.

**Step 7. Notice that the bug fails open or closed depending on the connective.**
Here it fails *closed*: it denies users it should have allowed. Swap `or` for
`and` in the original and the same mistake fails *open*, admitting users who
should have been denied. Both directions are live bugs, which is why the negation
rule is worth memorising rather than reconstructed.

## Runnable Code

### A tiny proposition language

```python
import itertools

# Each object is a FORMULA, not a value. A formula knows how to evaluate
# itself under an assignment of truth values to its letters.


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
        # `not`, not `~`: `~True` is -2, which would make the output ugly.
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


class Implies(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, assignment):
        # p -> q is FALSE in exactly one case: p is True and q is False.
        # Written this way so the code reads like the definition.
        return (not self.left.evaluate(assignment)) or self.right.evaluate(assignment)

    def __repr__(self):
        return f"({self.left!r} -> {self.right!r})"


class Iff(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, assignment):
        return self.left.evaluate(assignment) == self.right.evaluate(assignment)

    def __repr__(self):
        return f"({self.left!r} <-> {self.right!r})"


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


def print_truth_table(title, formula, names):
    print(title)
    print("  ".join(f"{n:>6}" for n in names) + "  |  result")
    print("-" * (7 * len(names) + 11))
    for a, value in zip(assignments(names), column(formula, names)):
        cells = "  ".join(f"{str(a[n]):>6}" for n in names)
        print(f"{cells}  |  {str(value):>6}")
    print()


p, q = Var("p"), Var("q")
NAMES = ["p", "q"]

print("=" * 64)
print("1. Implication is not conjunction")
print("=" * 64)
print_truth_table("p -> q", Implies(p, q), NAMES)
print_truth_table("p and q", And(p, q), NAMES)

imp = column(Implies(p, q), NAMES)
conj = column(And(p, q), NAMES)
disj = column(Or(p, q), NAMES)
iff = column(Iff(p, q), NAMES)

print(f"{'p':>6} {'q':>6} {'p and q':>9} {'p or q':>8} {'p -> q':>8} {'p <-> q':>9}")
for a, c, d, i, f in zip(assignments(NAMES), conj, disj, imp, iff):
    print(f"{str(a['p']):>6} {str(a['q']):>6} {str(c):>9} {str(d):>8} "
          f"{str(i):>8} {str(f):>9}")
print()
print(f"p -> q is False in {imp.count(False)} row. p and q is False in "
      f"{conj.count(False)} rows.")
print(f"p -> q agrees with p and q in {sum(a == b for a, b in zip(imp, conj))} of 4 rows.")
print(f"p -> q agrees with p or q  in {sum(a == b for a, b in zip(imp, disj))} of 4 rows.")
print(f"p <-> q agrees with p and q in {sum(a == b for a, b in zip(iff, conj))} of 4 rows.")
print()
print("Look at row 1 of the p <-> q column: it is True when both p and q are")
print("False. A biconditional is not 'both hold', it is 'the two agree'. Its")
print("real meaning is (p and q) or (not p and not q), which is why")
print("'p <-> q' and 'p and q' differ on the first row.")

print()
print("=" * 64)
print("2. Negating a compound statement")
print("=" * 64)
print()

pairs = [
    ("not (p and q)", ~And(p, q), "not p or not q", (~p) | (~q)),
    ("not (p or q)", ~Or(p, q), "not p and not q", (~p) & (~q)),
    ("not (p -> q)", ~Implies(p, q), "p and not q", p & (~q)),
    ("not (p <-> q)", ~Iff(p, q), "p or q", p | q),
]

for left_title, left, right_title, right in pairs:
    lc, rc = column(left, NAMES), column(right, NAMES)
    print(f"{left_title:<16} {as_bits(lc)}   vs   {right_title:<16} {as_bits(rc)}"
          f"   equal: {lc == rc}")
print()
print("rows of each column are (p, q) = (F,F), (F,T), (T,F), (T,T)")
print()
print("The first two rows are De Morgan's laws. The third is the negation of")
print("implication: not (p -> q) is 'p and not q', NOT 'p -> not q'.")
print()
print("The fourth is False, and that is the point of including it. Read it out:")
print("  not (p <-> q)  is True when p and q DIFFER, so the column is 0110.")
print("  p or q         is True when at least one holds, so the column is 0111.")
print("They differ on the last row, where both are true and so p <-> q holds,")
print("which makes its negation false.")
print()
xor = (p & (~q)) | (~p & q)
print("The correct rewrites for a biconditional are:")
print(f"  not (p <-> q)  ==  (p and not q) or (not p and q)  -> "
      f"{column(~Iff(p, q), NAMES) == column(xor, NAMES)}")
print(f"  its column     : {as_bits(column(xor, NAMES))}")

print()
print("=" * 64)
print("3. The bug this lesson exists to prevent")
print("=" * 64)
print()
print("Requirement: 'deny the request unless the user is an admin OR a superuser'.")
print()
print("  wanted  : not (is_admin or is_superuser)   # deny unless either")
print("  written : not is_admin or not is_superuser  # NOT what was wanted")
print()
print(f"{'is_admin':>9} {'is_superuser':>13} {'wanted':>8} {'written':>8} {'same?':>7}")
mismatches = []
for is_admin, is_super in [(False, False), (False, True), (True, False), (True, True)]:
    wanted = not (is_admin or is_super)
    written = (not is_admin) or (not is_super)
    if wanted != written:
        mismatches.append((is_admin, is_super))
    print(f"{str(is_admin):>9} {str(is_super):>13} {str(wanted):>8} "
          f"{str(written):>8} {str(wanted == written):>7}")
print()
print(f"the two disagree in {len(mismatches)} of 4 cases.")
print()
print("Python parses `not is_admin or is_superuser` as `(not is_admin) or")
print("is_superuser`, because `not` binds tighter than `or`. The grouping is")
print("not the bug. The bug is dropping the parentheses around the disjunction")
print("and so negating the wrong subformula. When you negate a compound")
print("condition, write the grouping out in full first, then simplify.")

print()
print("=" * 64)
print("4. Which sentences are even propositions?")
print("=" * 64)
print()
print("A proposition has a truth value. Some sentences do not, and treating")
print("them as if they do is the first error. Only two of the seven below are")
print("propositions; the rest have free variables, or are not claims about the")
print("world at all.")
print()

candidates = [
    ("2 + 2 = 4", "statement, and true", True),
    ("London is the capital of France", "statement, and false", True),
    ("x > 5", "not a statement: x is unbound, so no truth value", False),
    ("close the door", "imperative, not a claim about the world", False),
    ("is the server up", "a question", False),
    ("this sentence is false", "a liar: no consistent truth value", False),
    ("n! > 0 for every n", "statement, once you say n ranges over N", True),
]

for text, verdict, is_statement in candidates:
    print(f"  {'PROPOSITION' if is_statement else 'NOT       '}  {text}")
    print(f"              {verdict}")
print()
print("'x > 5' is the case that matters most in practice. It is not a")
print("proposition until you say what x is and what it has been assigned. That")
print("is exactly the domain question Lesson 12 makes precise, and it is why a")
print("type system exists: 'x > 5' has no meaning without a type.")
```

## Common Mistakes

**Wrong: `if not is_admin or is_superuser:` meaning "allow admins and
superusers".**
Right: Python parses this as `(not is_admin) or is_superuser`, so it also
admits anyone who is *not* an admin, which is everyone. The requirement
"allow if admin or superuser" needs `if is_admin or is_superuser:`. The bug is
assuming `not` distributes over `or` the way it distributes over `and`.
Why tempting: `not` binds tighter than `or` in every programming language you
have used, so the grouping is right; the error is believing the negation is
already distributed correctly. De Morgan says `¬(a ∨ b) = ¬a ∧ ¬b`, not
`¬a ∨ ¬b`.

**Wrong: "if p then q means p and q."**
Right: implication is true in three of the four cases, including both cases
where `p` is false. It only asserts a relationship when `p` holds. In code this
is why `if x is not None and x > 0:` is a valid guard — the second clause is
never evaluated when `x` is `None` — while `if x is None or x > 0:` asserts
something entirely different and raises `TypeError`.
Why tempting: in programming, "if" usually introduces a precondition, and
preconditions do feel conjunctive. That is a different connective from the one
in the specification.

**Wrong: treating `p or q` as "exactly one of p, q".**
Right: `or` is inclusive. `p or q` is true when both are true. In Python this is
why `self.x = self.y = None` then `if self.x or self.y: self.z = 1` sets `z` when
both are `None`... no, when *neither* is `None`; and why `bool(a or b)` is not
an exclusive-or. If you want exactly one, you need `(a and not b) or (not a and b)`
or, better, Python's `a != b` on booleans.
Why tempting: natural-language "either A or B" usually means exclusive, and the
same words in the same sentence often do. Mathematics and programming both take
the inclusive reading, and mixing them up in a comment is how bugs get written.

**Wrong: "not (p and q) is the same as not p or not q" without checking which
connective is inside.**
Right: `¬(p ∧ q) = ¬p ∨ ¬q` is true, and `¬(p ∨ q) = ¬p ∧ ¬q` is also true, but
they are different formulas from each other. The rule flips *and* to *or*. Getting
the flip backwards is the single most common logic error in code review, and the
worked example above is that mistake.
Why tempting: the shape "not... or not..." feels right for both, and the two
rules are stated in the same breath so they blur together.

**Wrong: assuming a sentence with a variable in it is not a statement.**
Right: "x is greater than five" has no truth value until `x` is assigned, but
"every natural number greater than five is odd" is a proposition with a free
variable, and once you state the domain it is decidable. The real requirement is
not the absence of variables but the absence of *unbound* ones. This is the gap
Lesson 12 fills.
Why tempting: the criterion "does it have a definite truth value" is correct, and
people apply it to the presence of variables rather than to their being bound,
which is a subtle and easy misreading.

**[ ] Exercise 1 — Build the truth table for eight propositions.** For each,
write the plain-English condition, then produce the truth column over
`(p, q) = (F,F), (F,T), (T,F), (T,T)` using the `Formula` classes from the
Runnable Code section. Report the column as a string of 1s and 0s, and state
whether it is a tautology, a contradiction, or contingent.

1. `¬(p ∧ q)`
2. `p → q`
3. `p ↔ q`
4. `¬p ∨ (q → p)`
5. `(p ∨ q) ∧ ¬(p ∧ q)`   (this is exclusive-or)
6. `p → (q → p)`           (this one is always true; find out why)
7. `¬p → ¬q`              (is this the contrapositive of 2, or its converse?)
8. `(p ∧ q) → (p ∨ q)`     (is this a tautology?)

<details>
<summary>Solution</summary>

```python
import itertools


# The formula classes, exactly as in the Runnable Code section.
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


class Implies(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, a):
        return (not self.left.evaluate(a)) or self.right.evaluate(a)

    def __repr__(self):
        return f"({self.left!r} -> {self.right!r})"


class Iff(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, a):
        return self.left.evaluate(a) == self.right.evaluate(a)

    def __repr__(self):
        return f"({self.left!r} <-> {self.right!r})"


p, q = Var("p"), Var("q")
NAMES = ["p", "q"]
ROWS = [dict(zip(NAMES, b)) for b in itertools.product([False, True], repeat=2)]


def column(f):
    """The truth column of a formula, as a list of booleans."""
    return [f.evaluate(a) for a in ROWS]


def bits(values):
    """Render a truth column as a string of 1s and 0s."""
    return "".join("1" if v else "0" for v in values)


def classify(f):
    """tautology, contradiction, or contingent."""
    col = column(f)
    if all(col):
        return "tautology"
    if not any(col):
        return "contradiction"
    return "contingent"


items = [
    ("not (p and q)", ~(p & q)),
    ("p -> q", Implies(p, q)),
    ("p <-> q", Iff(p, q)),
    ("not p or (q -> p)", ~p | Implies(q, p)),
    ("(p or q) and not (p and q)", (p | q) & ~(p & q)),
    ("p -> (q -> p)", Implies(p, Implies(q, p))),
    ("not p -> not q", Implies(~p, ~q)),
    ("(p and q) -> (p or q)", Implies(p & q, p | q)),
]

print(f"{'#':>2} {'proposition':<32} {'column':>7}  kind")
for i, (label, f) in enumerate(items, 1):
    print(f"{i:>2} {label:<32} {bits(column(f)):>7}  {classify(f)}")

print()
print("English, column by column. Rows are (p, q) = FF, FT, TF, TT.")
print()
print("1  not (p and q) is true when at least one of them is false.")
print("2  p -> q is false only when p is true and q is false.")
print("3  p <-> q is true when they agree: both true, or both false.")
print("4  not p or (q -> p) is a tautology. If p is false the first disjunct")
print("   holds; if p is true the second has a true consequent. Either way.")
print("5  exclusive-or is true when exactly one of p, q holds.")
print("6  p -> (q -> p) is a tautology, for a reason worth reading below.")
print("7  not p -> not q is the CONVERSE, not the contrapositive.")
print("8  (p and q) -> (p or q) is a tautology: nothing satisfies both")
print("   conjuncts without satisfying at least one disjunct.")

print()
print("=" * 68)
print("Why #6 is a tautology, one row at a time")
print("=" * 68)
for a in ROWS:
    inner = Implies(q, p).evaluate(a)
    outer = Implies(p, Implies(q, p)).evaluate(a)
    print(f"  p={str(a['p']):<5} q={str(a['q']):<5} "
          f"q->p={str(inner):<5} p->(q->p)={outer}")
print()
print("  When p is True, the inner q->p is automatically True because p holds,")
print("  so the outer implication has a True consequent and is True.")
print("  When p is False, the outer implication is True by definition.")
print("  Either way the outer is True. That is why it is a tautology.")

print()
print("=" * 68)
print("Converse versus contrapositive")
print("=" * 68)
original = column(Implies(p, q))
contrapositive = column(Implies(~q, ~p))
converse = column(Implies(~p, ~q))
print(f"  p -> q          {bits(original)}")
print(f"  not q -> not p  {bits(contrapositive)}   contrapositive, "
      f"equal to original: {contrapositive == original}")
print(f"  not p -> not q  {bits(converse)}   converse, "
      f"equal to original: {converse == original}")
print()
print("The contrapositive column is the original with the rows reversed, which")
print("is exactly what 'same false case' predicts. The converse column is not,")
print("and it is False on row 2 (p = F, q = T): p -> q is True there while")
print("not p -> not q is False. That single row is a real logical difference,")
print("and Lesson 13's contrapositive proof depends on it.")
```

Output:

```
 # proposition                       column  kind
 1 not (p and q)                       1110  contingent
 2 p -> q                              1101  contingent
 3 p <-> q                             1001  contingent
 4 not p or (q -> p)                   1111  tautology
 5 (p or q) and not (p and q)          0110  contingent
 6 p -> (q -> p)                       1111  tautology
 7 not p -> not q                      1011  contingent
 8 (p and q) -> (p or q)               1111  tautology

  p=False q=False  q->p=True   p->(q->p)=True
  p=False q=True   q->p=False  p->(q->p)=True
  p=True  q=False  q->p=True   p->(q->p)=True
  p=True  q=True   q->p=True   p->(q->p)=True

  p -> q          1101
  not q -> not p  1101   contrapositive, equal to original: True
  not p -> not q  1011   converse, equal to original: False
```

Item 5's column `0110` is exactly `(p ∧ ¬q) ∨ (¬p ∧ q)`, which is
exclusive-or. Python's `^` on booleans computes the same thing: `True ^ True`
is `False`, and so is `True ^ True` here. Item 7 is the one to dwell on,
because the contrapositive being True while the converse is False is the single
most useful fact in Lesson 13.

</details>

**[ ] Exercise 2 — Audit three real conditions.** For each condition below,
(a) write the requirement in English, (b) build the truth table over the
relevant variables, (c) say whether the code matches the requirement, and (d) if
it does not, give the correct version and the single input combination that
exposes the difference.

1. Requirement: "return 400 if the request is malformed **or** unauthenticated".
   Code: `if not well_formed and not authenticated: return 400`
2. Requirement: "retry if the request failed **and** was idempotent".
   Code: `if not failed or not idempotent: retry()`
3. Requirement: "grant access if the user is an admin **or** the resource is
   public **and** not archived". Code: `if is_admin or is_public and not archived:`

<details>
<summary>Solution</summary>

```python
import itertools


def truth_table(labels, fn):
    """Print every row of a boolean function of `labels`, with its value."""
    rows = [dict(zip(labels, b)) for b in itertools.product([False, True],
                                                            repeat=len(labels))]
    for a in rows:
        cells = "  ".join(f"{label}={str(a[label]):<5}" for label in labels)
        print(f"  {cells}  ->  {fn(a)}")
    return rows


def column(labels, fn):
    """The truth column of a boolean function, as a list of booleans."""
    return [fn(dict(zip(labels, b))) for b in
            itertools.product([False, True], repeat=len(labels))]


def bits(values):
    """Render a truth column as a string of 1s and 0s."""
    return "".join("1" if v else "0" for v in values)


def required_1(a):
    """400 if the request is malformed OR unauthenticated."""
    return (not a["well_formed"]) or (not a["authenticated"])


def written_1(a):
    """The code under review, using AND where the requirement says OR."""
    return (not a["well_formed"]) and (not a["authenticated"])


L1 = ["well_formed", "authenticated"]

print("=" * 70)
print("1. 'return 400 if malformed OR unauthenticated'")
print("=" * 70)
print()
print("required : (not well_formed) or (not authenticated)")
print("written  : (not well_formed) and (not authenticated)")
print()
truth_table(L1, required_1)
print(f"  required column : {bits(column(L1, required_1))}")
print(f"  written column  : {bits(column(L1, written_1))}")
print(f"  agree           : {column(L1, required_1) == column(L1, written_1)}")
print()
witness_1 = {"well_formed": True, "authenticated": False}
print(f"witness: well_formed={witness_1['well_formed']}, "
      f"authenticated={witness_1['authenticated']}")
print("  a perfectly well-formed request that simply has no credentials")
print(f"  required says : {required_1(witness_1)}   -> 400")
print(f"  written says  : {written_1(witness_1)}   -> proceed as anonymous")
print()
print("Verdict: BUG, and it fails OPEN. The requirement rejects an")
print("unauthenticated request however well formed it is. The code only")
print("rejects a request that is BOTH malformed AND unauthenticated, so every")
print("anonymous request sails through to whatever the handler does next.")
print()
print("correct code:")
print("    if not well_formed or not authenticated:")
print("        return 400")
print()
print("3 of 4 rows disagree, and the row count is the diagnosis. A table that")
print("disagrees on most rows has the wrong connective. One disagreeing row")
print("usually means a boundary case, not a swapped AND.")
print()


def required_2(a):
    return a["failed"] and a["idempotent"]


def written_2(a):
    return (not a["failed"]) or (not a["idempotent"])


L2 = ["failed", "idempotent"]

print("=" * 70)
print("2. 'retry if failed AND idempotent'")
print("=" * 70)
print()
print("required : failed and idempotent")
print("written  : (not failed) or (not idempotent)")
print()
truth_table(L2, required_2)
print(f"  required column : {bits(column(L2, required_2))}")
print(f"  written column  : {bits(column(L2, written_2))}")
print(f"  agree           : {column(L2, required_2) == column(L2, written_2)}")
print()
witness_2 = {"failed": False, "idempotent": False}
print(f"witness: failed={witness_2['failed']}, idempotent={witness_2['idempotent']}")
print(f"  required says : {required_2(witness_2)}   -> do not retry")
print(f"  written says  : {written_2(witness_2)}   -> RETRY")
print()
print("Verdict: BUG. The written code retries whenever either the request did")
print("NOT fail, or it is not idempotent. So every successful non-idempotent")
print("request gets retried, which is precisely what idempotency exists to stop:")
print("a POST that succeeded, got retried, and charged the card twice.")
print()
print("correct code:")
print("    if failed and idempotent:")
print("        retry()")
print()
print("Or, if the real requirement is 'retry unless it succeeded', write that")
print("instead. Requirements of the form 'not (A and B)' are much harder to")
print("implement correctly than the thing you actually want:")
print("    if not succeeded:")
print("        retry()")
print()


def required_3(a):
    return a["is_admin"] or (a["is_public"] and not a["archived"])


def written_3(a):
    # Python binds `and` tighter than `or`, so this is the code under review.
    return (a["is_admin"] or a["is_public"]) and not a["archived"]


L3 = ["is_admin", "is_public", "archived"]

print("=" * 70)
print("3. 'grant if admin, or public and not archived'")
print("=" * 70)
print()
print("required : is_admin or (is_public and not archived)")
print("written  : is_admin or is_public and not archived")
print("            Python reads that as (is_admin or is_public) and not archived")
print()
print(f"{'is_admin':>9} {'is_public':>10} {'archived':>10} {'required':>10} "
      f"{'written':>8}  result")
mismatches = []
for b in itertools.product([False, True], repeat=3):
    a = dict(zip(L3, b))
    req, wr = required_3(a), written_3(a)
    if req != wr:
        mismatches.append((a, req, wr))
    print(f"{str(a['is_admin']):>9} {str(a['is_public']):>10} "
          f"{str(a['archived']):>10} {str(req):>10} {str(wr):>8}"
          f"  {'ok' if req == wr else 'BUG'}")
print()
print(f"{len(mismatches)} of 8 rows disagree.")
print()
print("Verdict: BUG. An admin is meant to reach an archived resource, but the")
print("written code ANDs `not archived` against the admin case too, so the")
print("admin is blocked from exactly the archive they need to fix.")
print()
print("correct code, with the parentheses written out:")
print("    if is_admin or (is_public and not archived):")
print()
print("Both failing rows have is_admin True and archived True, and they disagree")
print("only when is_public is False. The requirement grants access to the admin")
print("because is_admin alone suffices; the code demands the public branch too,")
print("because `not archived` was ANDed against the whole disjunction instead")
print("of only against the public branch.")
print()
print("The lesson from all three: when a requirement mixes and with or, write")
print("the parentheses in the code. Python will sometimes infer the wrong ones")
print("and will not warn you. And every one of these failed by swapping a")
print("connective or dropping a grouping, never by an arithmetic slip.")
print("Connective mistakes, not arithmetic mistakes.")
```

Output:

```
1. 'return 400 if malformed OR unauthenticated'
required : (not well_formed) or (not authenticated)
written  : (not well_formed) and (not authenticated)

  well_formed=False  authenticated=False  ->  True
  well_formed=False  authenticated=True   ->  True
  well_formed=True   authenticated=False  ->  True
  well_formed=True   authenticated=True   ->  False

  required column : 1110
  written column  : 1000
  agree           : False

2. 'retry if failed AND idempotent'
required : failed and idempotent
written  : (not failed) or (not idempotent)

  failed=False  idempotent=False  ->  False
  failed=False  idempotent=True   ->  False
  failed=True   idempotent=False  ->  False
  failed=True   idempotent=True   ->  True

  required column : 0001
  written column  : 1110
  agree           : False

witness: failed=False, idempotent=False
  required says : False   -> do not retry
  written says  : True    -> RETRY

3. 'grant if admin, or public and not archived'
required : is_admin or (is_public and not archived)
written  : is_admin or is_public and not archived
            Python reads that as (is_admin or is_public) and not archived

  is_admin  is_public  archived  required  written  result
      False      False     False     False    False  ok
      False      False      True     False    False  ok
      False       True     False      True     True  ok
      False       True      True     False    False  ok
       True      False     False      True     True  ok
       True      False      True      True    False  BUG
       True       True     False      True     True  ok
       True       True      True      True    False  BUG

2 of 8 rows disagree.
```

The number of disagreeing rows is the fastest diagnostic in the table. Condition
1 disagrees on three rows out of four, which says the connective itself is
wrong rather than a boundary case being mishandled. Condition 3 disagrees on two
rows out of eight, and both have the same shape, which points at one specific
grouping rather than a wholesale swap. Neither diagnosis could have been made by
reading the code, and both take one line of arithmetic to confirm.

</details>

**[ ] Exercise 3 — Build a formula parser and round-trip it against Python.** Write
a `Parser` class using recursive descent that turns a string like `"p & (q | ~r)"`
into a `Formula`. Grammar, loosest binding first:
`expr := impl ('|' impl)*`, `impl := conj ('->' impl)?`, `conj := unary ('&' unary)*`,
`unary := '~' unary | atom`, `atom := NAME | '(' expr ')'`. Then: (a) verify that
for each of ten test strings, the parsed formula agrees with Python's own `eval`
of the same text under `&`→`and`, `|`→`or`, `~`→`not`, across all 8 assignments of
three variables; (b) show that `~` binds tighter than `&`, which binds tighter than
`|`, by exhibiting two differently-grouped formulas with different columns; (c)
show that `p -> q` is the same formula as `~p | q`; (d) show that `->` is
right-associative by comparing the columns of `p -> q -> r` and `(p -> q) -> r`.

<details>
<summary>Solution</summary>

```python
import itertools


# --- The formula classes, as in the Runnable Code section.
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


class Implies(Formula):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def evaluate(self, a):
        return (not self.left.evaluate(a)) or self.right.evaluate(a)

    def __repr__(self):
        return f"({self.left!r} -> {self.right!r})"


# --- A recursive descent parser. One method per grammar rule.
class Parser:
    def __init__(self, text):
        self.tokens = self.tokenize(text)
        self.pos = 0

    @staticmethod
    def tokenize(text):
        out, i = [], 0
        while i < len(text):
            ch = text[i]
            if ch.isspace():
                i += 1
            elif ch.isalpha():
                j = i
                while j < len(text) and text[j].isalpha():
                    j += 1
                out.append(("NAME", text[i:j]))
                i = j
            elif text[i:i + 2] == "->":
                out.append(("IMPLIES", "->"))
                i += 2
            elif ch in "&|~()":
                out.append((ch, ch))
                i += 1
            else:
                raise ValueError(f"unexpected character {ch!r}")
        return out

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def take(self, expected=None):
        kind, value = self.peek()
        if expected is not None and kind != expected:
            raise ValueError(f"expected {expected!r}, got {kind!r}")
        self.pos += 1
        return kind, value

    def parse(self):
        result = self.expr()
        if self.pos != len(self.tokens):
            raise ValueError(f"trailing tokens at position {self.pos}")
        return result

    def expr(self):
        left = self.impl()
        while self.peek()[0] == "|":
            self.take()
            left = Or(left, self.impl())
        return left

    def impl(self):
        left = self.conj()
        if self.peek()[0] == "IMPLIES":
            self.take()
            # Right-associative: a -> (b -> c), not (a -> b) -> c.
            return Implies(left, self.impl())
        return left

    def conj(self):
        left = self.unary()
        while self.peek()[0] == "&":
            self.take()
            left = And(left, self.unary())
        return left

    def unary(self):
        if self.peek()[0] == "~":
            self.take()
            return Not(self.unary())
        return self.atom()

    def atom(self):
        kind, value = self.peek()
        if kind == "NAME":
            self.take()
            return Var(value)
        if kind == "(":
            self.take()
            inner = self.expr()
            self.take(")")
            return inner
        raise ValueError(f"unexpected token {kind!r}")


def parse(text):
    return Parser(text).parse()


def column(formula, names):
    return [formula.evaluate(dict(zip(names, b)))
            for b in itertools.product([False, True], repeat=len(names))]


def bits(values):
    return "".join("1" if v else "0" for v in values)


def to_python_source(text):
    """Rewrite the token stream as a Python boolean expression.

    Python's precedence for `~`, `&`, `|` matches ours (unary, then and, then
    or), so only the spellings change. `->` has no Python spelling and is
    handled separately in part (c).
    """
    mapping = {"~": "not", "&": "and", "|": "or"}
    out = []
    for kind, value in Parser.tokenize(text):
        out.append(value if kind == "NAME" else mapping.get(kind, value))
    return " ".join(out)


NAMES = ["p", "q", "r"]

test_cases = [
    "p",
    "~p",
    "p & q",
    "p | q",
    "p & q | r",              # & binds tighter, so this is (p & q) | r
    "p & (q | r)",            # needs the parentheses to mean the same thing
    "~p & q | r",             # ~ binds tightest
    "~(p & q) | r",
    "p & q & r",
    "~p & ~q | ~r & (p | q)",
]

print("=" * 68)
print("(a) the parser agrees with Python's own reading of the same text")
print("=" * 68)
print()
print(f"{'text':<24} {'parsed as':<40} {'agrees':>7}")
all_agree = True
for text in test_cases:
    formula = parse(text)
    source = to_python_source(text)
    mismatches = 0
    for b in itertools.product([False, True], repeat=3):
        assignment = dict(zip(NAMES, b))
        mine = bool(formula.evaluate(assignment))
        theirs = bool(eval(source, dict(assignment)))
        if mine != theirs:
            mismatches += 1
    all_agree = all_agree and mismatches == 0
    print(f"{text:<24} {repr(formula):<40} {mismatches == 0:>7}")

print()
print("the python source each row was compared against:")
for text in test_cases:
    print(f"  {text:<24} -> {to_python_source(text)}")
print()
print(f"all ten agree on all 8 assignments: {all_agree}")

print()
print("=" * 68)
print("(b) precedence: ~ before & before |")
print("=" * 68)
print()
for text in ("~p & q", "~(p & q)", "p & q | r", "p | q & r"):
    print(f"  {text:<12} parses to {parse(text)!r}")
print()
print("If ~ bound loosely, '~p & q' would parse as ~(p & q). Compare columns:")
print(f"  (~p) & q   {bits(column(parse('~p & q'), NAMES))}")
print(f"  ~(p & q)   {bits(column(parse('~(p & q)'), NAMES))}")
print("Different columns, so the precedence is observable, and it is the tight")
print("one. This is the same rule as Python's own precedence table.")

print()
print("=" * 68)
print("(c) p -> q is the same formula as ~p | q")
print("=" * 68)
print()
imp_formula = parse("p -> q")
or_formula = parse("~p | q")
print(f"  p -> q   {imp_formula!r}   column {bits(column(imp_formula, NAMES))}")
print(f"  ~p | q   {or_formula!r}   column {bits(column(or_formula, NAMES))}")
print(f"  equivalent: {column(imp_formula, NAMES) == column(or_formula, NAMES)}")
print()
print("So a parser needs no special token for the arrow: NOT and OR already")
print("express it. That is why Python has no implication operator, and why")
print("anyone writing an implication in code writes 'if not p or q'.")

print()
print("=" * 68)
print("(d) -> is right-associative")
print("=" * 68)
print()
print(f"  p -> q -> r       parses to {parse('p -> q -> r')!r}")
print(f"  (p -> q) -> r     parses to {parse('(p -> q) -> r')!r}")
print()
print(f"  column of the first  : {bits(column(parse('p -> q -> r'), NAMES))}")
print(f"  column of the second : {bits(column(parse('(p -> q) -> r'), NAMES))}")
print()
print("Different formulas, so associativity was a choice and the wrong one is a")
print("real bug. Right-associative is correct because it reads like a nested")
print("if: 'if p then (if q then r)'.")
```

Output:

```
(a) the parser agrees with Python's own reading of the same text

text                     parsed as                                 agrees
p                        p                                              1
~p                       ~p                                             1
p & q                    (p & q)                                        1
p | q                    (p | q)                                        1
p & q | r                ((p & q) | r)                                  1
p & (q | r)              (p & (q | r))                                  1
~p & q | r               ((~p & q) | r)                                 1
~(p & q) | r             (~(p & q) | r)                                 1
p & q & r                ((p & q) & r)                                  1
~p & ~q | ~r & (p | q)   ((~p & ~q) | (~r & (p | q)))                   1

the python source each row was compared against:
  p                        -> p
  ~p                       -> not p
  p & q                    -> p and q
  p | q                    -> p or q
  p & q | r                -> p and q or r
  p & (q | r)              -> p and ( q or r )
  ~p & q | r               -> not p and q or r
  ~(p & q) | r             -> not ( p and q ) or r
  p & q & r                -> p and q and r
  ~p & ~q | ~r & (p | q)   -> not p and not q or not r and ( p or q )

all ten agree on all 8 assignments: True

(b) precedence: ~ before & before |
  ~p & q       parses to (~p & q)
  ~(p & q)     parses to ~(p & q)
  p & q | r    parses to ((p & q) | r)
  p | q & r    parses to (p | (q & r))
  (~p) & q   00110000
  ~(p & q)   11111100

(c) p -> q is the same formula as ~p | q
  p -> q   (p -> q)   column 11110011
  ~p | q   (~p | q)   column 11110011
  equivalent: True

(d) -> is right-associative
  p -> q -> r       parses to (p -> (q -> r))
  (p -> q) -> r     parses to ((p -> q) -> r)

  column of the first  : 11111101
  column of the second : 01011101
```

Part (d) is the one to slow down on. `p -> q -> r` and `(p -> q) -> r` are
different formulas with different columns, so associativity was a decision and
the wrong choice is a real bug that would survive any test you happened to write.
Right-associative is right because the arrow reads like a nested `if`.

</details>

**Challenge — Decide whether conditions are correct, using reachability as well
as equivalence.** Take three conditions and, for each: (1) enumerate every input
combination, (2) mark which combinations are actually reachable, using invariants
of the system rather than wishful thinking, (3) compare the code's value with the
requirement's value on every reachable row, and (4) state what the code does on
the unreachable rows. Use a condition with an integer-valued input (such as
`page_size`), because modelling it as a plain boolean hides exactly the thing you
are trying to find. Then report: for each condition, how many rows were reachable,
how many mismatched, and whether any unreachable row was wrong.

<details>
<summary>Solution</summary>

```python
import itertools

# ---------------------------------------------------------------------------
# A truth table has one row per input combination. Some rows describe states
# the program can never be in, because some invariant rules them out.
# Unreachable rows do not need to match the requirement. That is where bugs
# hide, because a test suite only ever visits the reachable ones.
#
# page_size below is NOT a boolean. It takes the values 0 and 25, because 0 is
# the bad value and 25 the normal one, and modelling that with a plain bool is
# what stops you seeing the problem.
# ---------------------------------------------------------------------------

PAGE_SIZES = [0, 25]


def pagination_rows():
    return [{"has_more": m, "page_size": ps, "has_cursor": c}
            for m, c in itertools.product([False, True], repeat=2)
            for ps in PAGE_SIZES]


def report(title, all_rows, code_fn, reachable_fn, req_fn):
    print(title)
    keys = list(all_rows[0])
    header = "  ".join(f"{k:>12}" for k in keys)
    print(f"  {header}   code  required  match  reachable")
    print("  " + "-" * (13 * len(keys) + 33))

    reachable_mismatches = []
    unreachable_wrong = []
    reachable_count = 0
    for a in all_rows:
        code_value = code_fn(a)
        req_value = req_fn(a)
        ok = bool(code_value) == bool(req_value)
        reachable = reachable_fn(a)
        if reachable:
            reachable_count += 1
            if not ok:
                reachable_mismatches.append((a, code_value, req_value))
        elif not ok:
            unreachable_wrong.append((a, code_value, req_value))
        cells = "  ".join(f"{str(a[k]):>12}" for k in keys)
        print(f"  {cells}   {str(code_value):>4}    {str(req_value):>7}"
              f"   {'ok ' if ok else 'BUG'}  {'yes' if reachable else 'NO':>3}")
    return reachable_count, reachable_mismatches, unreachable_wrong


def pagination_code(a):
    """As written. It adds a page_size guard nobody asked for."""
    return a["has_more"] and a["has_cursor"] and a["page_size"] > 0


def pagination_required(a):
    """More pages remain, and we have a cursor to continue from."""
    return a["has_more"] and a["has_cursor"]


ROWS = pagination_rows()

# The invariant: page_size comes from a constant, so it is never zero.
page_size_is_valid = lambda a: a["page_size"] > 0

print("=" * 74)
print("Case A: the invariant holds, so page_size is never zero")
print("=" * 74)
print()
print("code:    if has_more and has_cursor and page_size > 0:")
print("wanted:  if has_more and has_cursor:")
print()
r = report("", ROWS, pagination_code, page_size_is_valid, pagination_required)
print()
print(f"rows in the raw table              : {len(ROWS)}")
print(f"rows the invariant makes reachable : {r[0]}")
print(f"mismatches among reachable rows    : {len(r[1])}")
print(f"mismatches among unreachable rows  : {len(r[2])}")
print()
print("Verdict: correct in practice, wrong in general.")
print()
print("Every reachable row agrees. The unreachable wrong row has page_size == 0,")
print("which the invariant excludes, and in it the extra conjunct silently")
print("stops the fetch. The code is buggy and the table is right; the only")
print("thing standing between them is an assumption about where page_size")
print("comes from.")
print()
print("The moment someone reads page_size from a query parameter, or a config")
print("file that can be zero, or a user's saved preference, the invariant")
print("breaks. The endpoint then returns zero rows to a caller that expected a")
print("page, and the caller sees a valid empty response rather than an error.")
print("That is the worst failure mode a paginated API can have.")
print()

print("=" * 74)
print("Case B: the same guard once page_size can be zero")
print("=" * 74)
print()
r = report("", ROWS, pagination_code, lambda a: True, pagination_required)
print()
print(f"reachable rows now : {r[0]}")
print(f"mismatches now     : {len(r[1])}")
print()
print("Identical code, identical requirement. One row moved from 'unreachable")
print("and wrong' to 'reachable and wrong'. Nothing in the code changed; the")
print("only difference is whether the reader still believes an assumption about")
print("the caller. That is what the reachability column buys you: it turns an")
print("assumption into a line you can go and check.")
print()

print("=" * 74)
print("Case C: a rate limiter, where the bug is a connectiveswap")
print("=" * 74)
print()
print("code:    if over_limit or is_write or not has_credit:   # throttle")
print("wanted:  if over_limit and is_write and not has_credit:")
print()

L4 = ["over_limit", "is_write", "has_credit"]
RATE_ROWS = [dict(zip(L4, b)) for b in itertools.product([False, True], repeat=3)]


def rate_code(a):
    return a["over_limit"] or a["is_write"] or (not a["has_credit"])


def rate_required(a):
    return a["over_limit"] and a["is_write"] and not a["has_credit"]


# No invariant prunes anything: every combination occurs in real traffic.
r4 = report("", RATE_ROWS, rate_code, lambda a: True, rate_required)
print()
print(f"{len(RATE_ROWS)} rows, {len(r4[1])} reachable mismatches, "
      f"{len(r4[2])} unreachable mismatches.")
print()
print("No invariant saves this one, so every row is live and six of the eight")
print("disagree. Concretely: a READ request that is not over the limit and does")
print("have credit still gets throttled, because `is_write` alone makes the")
print("disjunction true. Roughly nine requests in ten are reads, so this rate")
print("limiter throttles most of all traffic on a perfectly healthy day.")
print()
print("The three questions, answered")
print()
print("  1. Which rows are reachable? From invariants, not from the code.")
print("     Anything you cannot justify excluding, count as reachable.")
print("  2. For unreachable rows, what does the code do? Anything at all. It is")
print("     unconstrained, and an unconstrained row is a landmine rather than a")
print("     neutral fact.")
print("  3. Do reachable rows match the requirement? The only question that")
print("     finds bugs, and the only one you can answer mechanically.")
print()
print("Case A is a bug that production is currently hiding. Case C is a bug")
print("with nothing hiding it, which means it should have been caught and was")
print("not. Both pass any test suite that only exercises reachable behaviour,")
print("and that is not a criticism of testing: a test suite cannot tell you")
print("which rows it failed to reach.")
```

Output (the Case A table, which is the one that matters):

```
      has_more     page_size    has_cursor   code  required  match  reachable
  ------------------------------------------------------------------------
         False             0         False   False      False   ok    NO
         False            25         False   False      False   ok   yes
         False             0          True   False      False   ok    NO
         False            25          True   False      False   ok   yes
          True             0         False   False      False   ok    NO
          True            25         False   False      False   ok   yes
          True             0          True   False       True   BUG    NO
          True            25          True    True       True   ok   yes

rows in the raw table              : 8
rows the invariant makes reachable : 4
mismatches among reachable rows    : 0
mismatches among unreachable rows  : 1
```

Case A is the interesting result and it is the reason to do the exercise with an
integer input rather than a boolean. If `page_size` had been modelled as a bool,
the unreachable-wrong row would have collapsed into the reachable-wrong rows and
you would have reported a bug with no explanation. The row is wrong, it is
unreachable, and the only thing saving you is an assumption about where
`page_size` comes from. Four reachable rows all agree, which is exactly why the
bug survived: production exercised four rows and they were the four that work.

</details>## Summary

- A proposition is a declarative sentence with a definite truth value.
  "Sort this list" is not one, and "x > 5" is not one until `x` is bound.
- `¬P ∧ Q`, `P ∨ Q`, and `P ↔ Q` have exact truth conditions, and `∨` is
  inclusive: `P ∨ Q` is true when both are true.
- `P → Q` is false in exactly one case, `P` true and `Q` false. It is therefore
  true in three of four cases, and it is **not** `P ∧ Q`.
- The key identity is `P → Q ≡ ¬P ∨ Q`. Everything else about implication,
  including its negation and its contrapositive, follows from it.
- `¬(P ∧ Q) ≡ ¬P ∨ ¬Q` and `¬(P ∨ Q) ≡ ¬P ∧ ¬Q`. Applying these with the
  connectives swapped is the single most common logic error in code.
- The converse `¬P → ¬Q` is not equivalent to `P → Q`. The contrapositive
  `¬Q → ¬P` is. Lesson 13 needs that difference.
- Negating `P ↔ Q` gives `(P ∧ ¬Q) ∨ (¬P ∧ Q)`, not `P ∨ Q`.
- A tautology is true everywhere and a contradiction is false everywhere.
  Most propositions are contingent, and being contingent is not a criticism.
- Logical equivalence means agreement under every assignment, and substitution
  for equivalence is what licenses rewriting a condition without changing what
  it does.
- Python's `not` binds tighter than `and`, which binds tighter than `or`. When
  a requirement mixes connectives, write the parentheses anyway: Python will
  sometimes infer the wrong ones and will not tell you.

## Next

[Lesson 11 — Truth Tables, Equivalence, and Normal Forms](../part01_logic_proof/11_truth_tables_and_equivalence.md)
turns what you learned here into a mechanical procedure: enumerate every
assignment, compare columns, and simplify conditions by proof rather than by
intuition. It assumes you can negate a compound statement correctly.