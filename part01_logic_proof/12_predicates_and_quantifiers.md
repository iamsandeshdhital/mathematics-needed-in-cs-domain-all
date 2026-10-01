# 12 — Predicates and Quantifiers

**Part**: part01_logic_proof · **Prerequisites**: 11 · **Time**: 40 min

---

## In Plain Words

A statement like "this request is authenticated" is not really a statement on
its own. It is a sentence with a hole in it, and the hole is the request it is
talking about. Fill the hole with one particular request and the sentence
becomes true or false. Leave the hole open and the sentence is a *predicate*:
something that can be checked, but has no answer yet.

A predicate becomes a real statement the moment you say how many holes you are
going to fill and how you want to fill them. Saying "for every request" makes a
claim about the whole world at once, and it fails the moment a single request
breaks it. Saying "there is some request" makes a claim that succeeds on the
strength of one example and is destroyed by finding that there is none. Those
two words, "every" and "some", are the whole subject of this lesson, and the
single most useful thing to know about them is how to take the opposite of a
sentence that contains one.

Everything else here is that rule, its consequences, and where you already use
it without noticing. Every SQL where clause is a predicate. Every type-system
rule is a claim about all types. Every coverage number is a claim about all
branches — and, as we shall see, not the claim anyone thinks it is.

## Why Computer Science Cares

**A SQL `WHERE` clause is a predicate over a table.** The table is the domain,
the clause is the open sentence, and `SELECT` reports the existential: "here
are the rows for which it held." When a query returns nothing, you cannot tell
whether you wanted an existential or a universal, and the two have different
meanings. `SELECT ... WHERE EXISTS (...)` finds *some* row with a login;
`SELECT ... WHERE NOT EXISTS (SELECT 1 FROM logins ...)` finds *the* row with
no login. Same engine, same rows, opposite question.

**SQL cannot write a universal, so you pay for it every time.** `NOT EXISTS` is
the only tool, and wrapping it around a `WHERE` nests an existential inside it.
Any time you see a double `NOT`, you are looking at a universal that has been
rewritten as an existential with a negation on top.

**Type systems are universal quantifiers over types that are not values.**
`∀α. (α → α) → α → α` says a function of any type at all, with no type named
in the body. Every time a type checker accepts a program, it is discharging a
universal claim. Hindley–Milner, System F and Rust's trait system differ in
*how* they discharge it, not in *whether* they are making the claim.

**Preconditions, postconditions and type signatures are quantified sentences.**
Dafny's `requires P` means "for every input satisfying P". A test asserts
`∃ input` with a specific value. The gap between those two is the entire
difference between testing and verifying, and it is a difference in
quantifier, not in effort.

**Coverage tooling computes a nested quantifier and reports the wrong one.**
"Every branch is covered" is `∀ branch, ∃ test that reaches it`. The claim that
would be worth making — "every input behaves as specified" — is a single
universal over inputs, and no finite test suite can establish it. Knowing which
claim your tooling checks is worth more than the percentage it prints.

**Hoare logic and model checking are quantifier manipulation.** A loop
invariant is a universal statement about every reachable state, and a weakest
precondition is computed by pushing a quantifier inward through a program.
Automated theorem provers spend their time on exactly this.

## The Formal Version

Notation follows [SYMBOLS.md](../SYMBOLS.md). A variable in a formula is
written $x$; the domain is written $D$; a predicate is written $P$.

**Definition.** A *domain* $D$ is a set of values. A variable ranging over $D$
may be assigned any element of $D$ and no other. The domain is part of the
statement, not part of the notation: "there exists a prime number greater than
$n$" is a proposition, while "$x$ is prime" is not, and the difference is
entirely the domain.

**Definition.** A *predicate* (or *open sentence*) is a formula $P(x)$ in which
$x$ occurs and is not quantified. $P(x)$ has no truth value on its own; it has
a truth value for each substitution $x \mapsto d$ with $d \in D$. A predicate
in $k$ variables is a function $D^k \to \{\text{false}, \text{true}\}$, which is
the definition with the quantifier left off.

**Definition.** A variable is *free* in $P$ if some quantifier does not bind it,
and *bound* otherwise. A formula with no free variables is a *closed
sentence*, and a closed sentence is a proposition — which is what
[Lesson 10](../part01_logic_proof/10_propositions_and_connectives.md) demanded and what the truth
table of [Lesson 11](../part01_logic_proof/11_truth_tables_and_equivalence.md) can then be built
over.

**Definition.** The *scope* of a quantifier is the formula immediately to its
right, up to the end of the smallest enclosing formula. A quantifier binds
every free occurrence of its variable within its scope, and nothing outside it.

**Definition.** *Universal quantification.* `$\forall x \in D\; P(x)$` is true
iff $P(d)$ is true for every $d \in D$. It is **false** as soon as one $d \in D$
makes $P(d)$ false. That $d$ is a *counterexample*, and it is the only piece of
information a refutation needs.

**Definition.** *Existential quantification.* `$\exists x \in D\; P(x)$` is true
iff $P(d)$ is true for at least one $d \in D$. It is **false** only when no $d$
works. That $d$, when one exists, is a *witness*, and it is the only piece of
information a confirmation needs.

**Definition.** *Unique existence*, `$\exists! x \in D\; P(x)$`, means exactly one
$d \in D$ satisfies $P$. This is a third quantifier and not a decoration: it is
`∃` plus a distinctness requirement, and its negation needs two variables.

**Theorem.** *Negation of quantifiers.*

    ¬(∀x ∈ D, P(x))  ≡  ∃x ∈ D, ¬P(x)
    ¬(∃x ∈ D, P(x))  ≡  ∀x ∈ D, ¬P(x)
    ¬(∀x ∈ D, P(x) ∧ Q(x))  ≡  ∃x ∈ D, ¬P(x) ∨ ¬Q(x)
    ¬(∃! x ∈ D, P(x))  ≡  ∃x ∈ D, ∃y ∈ D, (P(x) ∧ P(y) ∧ x ≠ y)

*Proof.* The first is a definition in each direction: "not every element works"
means "at least one element fails". The second is the same argument applied to
"not some element works". The third is De Morgan's laws from
[Lesson 11](../part01_logic_proof/11_truth_tables_and_equivalence.md) applied to the body. The fourth
says "the count of solutions is not exactly one", which for a natural number
means it is 0 or at least 2; a negative count is impossible, so 0 is excluded
and two distinct solutions exist. ∎

*Why this is the central fact.* Quantifiers flip **and** the connective inside
flips. A rule that flips only one of the two produces a sentence that looks
like a negation and is not: `¬∀x P(x)` is not `¬∃x P(x)`, and it is not
`∀x ¬P(x)`. Every use of the word "not" on a quantified sentence is a chance
to get this wrong, and in code the error is invisible because the sentence
still parses.

**Theorem.** *Order of quantifiers is part of the meaning.*
`$\forall x \in D\, \exists y \in D\, P(x,y)$` and
`$\exists y \in D\, \forall x \in D\, P(x,y)$` are different propositions, and
neither implies the other on a general relation.

*Proof.* Take $D = \mathbb{R}$ and $P(x,y)$ meaning $x < y$. The first says
every real is exceeded by some real, which is true: $x + 1$ works. The second
says some real exceeds every real, which is false: for any candidate $y$, the
value $y - 1$ does not satisfy $y' < y$ with $y' = y$. So the first is true and
the second false on the same data. ∎

Read the first as "each $x$ gets its own $y$, allowed to depend on $x$" and the
second as "one $y$ that works for all $x$". The first is a matching problem; the
second demands a single universal witness, which usually does not exist.

**Theorem.** *Vacuous truth.* `$\forall x \in \varnothing\; P(x)$` is true, and
`$\exists x \in \varnothing\; P(x)$` is false.

*Proof.* $\varnothing$ has no elements. The universal is `true` unless some
element of $\varnothing$ falsifies the body, and there is none. The existential
needs an element of $\varnothing$ satisfying the body, and there is none. ∎
Neither is a curiosity: they are what "the query matched no rows" means, and
they are why `if not list:` and `if any(not x for x in list):` can both be the
right translation of the same English sentence depending on which one you meant.

**Theorem.** *Cost of a quantifier.* A closed sentence over domain $D$ with $k$
nested quantifiers is decided by at most `$\lvert D\rvert^k$` predicate
evaluations.

*Proof.* The innermost quantifier ranges over $\lvert D\rvert$ values; the next
ranges over $\lvert D\rvert$ for each of those, and so on to $k$ levels. ∎ This
is the point at which quantifiers stop being logic and become algorithms. The
sentence is a program, the nesting depth is a loop count, and
`$\lvert D\rvert^k$` is a runtime. [Lesson 15](../part01_logic_proof/15_sets_and_cardinality.md) shows
that for countably infinite $D$ this number is infinite for every $k \ge 1$,
which is why nobody decides quantified sentences by enumeration over $\mathbb{N}$.

**Theorem.** *Renaming bound variables.* If $x$ and $y$ are both bound, and
neither occurs free in the formula, replacing every bound occurrence of $x$ by
$y$ leaves the meaning unchanged. This is how you check that two quantifiers
have the *same scope*: rewrite both to use the same variable names and compare.

*Proof sketch.* The scope of a quantifier is determined by the smallest
enclosing formula, and the variable name is invisible to that. The only place a
name can matter is a free occurrence, and those were excluded by hypothesis. ∎
This is the practical test for scope mistakes: normalise the names, then read
the text. `∀x (P(x) → ∃x Q(x))` and `∀x (P(x) → ∃y Q(y))` agree; if your
renaming cannot turn one into the other, the scopes differ.

## Formula Sheet

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$D$` | a set of values, stated explicitly | everything the variable is allowed to be | whenever a sentence is not a proposition without it |
| `$P(x)$` | an open sentence in $x$ | "the hole", ready to be filled with one value | writing a check that takes an argument |
| free vs bound | a variable is bound iff some quantifier captures it | "does something already stand in for it?" | finding the scope of a `not` |
| closed sentence | a formula with no free variables | a proposition; truth-table-able | anything you intend to argue about |
| `$P(d)$` | substituting $d$ for `$x$` in `$P(x)$` | running the check on one specific value | evaluating a predicate |
| `$\forall x \in D\; P(x)$` | true iff `$P(d)$ holds for all $d \in D$` | "for every" | specs, invariants, preconditions |
| `$\exists x \in D\; P(x)$` | true iff `$P(d)$ holds for some $d \in D$` | "for some" | finding an example, searching, `EXISTS` |
| `$\exists! x \in D\; P(x)$` | true iff exactly one `$d \in D$` holds | "there is one and only one" | unique keys, unique owners, idempotency |
| `$\forall x \in D\, \exists y \in D\, P(x,y)$` | each `$x$` has its own `$y$` | a **matching**; the `$y$` may depend on `$x$` | assigning each item a resource |
| `$\exists y \in D\, \forall x \in D\, P(x,y)$` | one `$y$` serves every `$x$` | a **single universal witness** | rare, and much stronger; check the order |
| `$\neg \forall x\, P(x) \equiv \exists x\, \neg P(x)$` | "not every" is "some … not" | the universal is refuted by one counterexample | negating a spec into a testable claim |
| `$\neg \exists x\, P(x) \equiv \forall x\, \neg P(x)$` | "none" is "every … not" | the existential is refuted only by exhausting the domain | proving a lookup always succeeds |
| `$\neg (\forall x\, P(x) \wedge Q(x)) \equiv \exists x\, (\neg P(x) \vee \neg Q(x))$` | flip the quantifier **and** the connective | De Morgan applied to the body | negating a two-part requirement |
| `$\neg \exists! x\, P(x) \equiv \exists x \exists y\, (P(x) \wedge P(y) \wedge x \neq y)$` | not-unique means two different witnesses | uniqueness fails by *duplication*, not by absence | duplicate-key and double-charge bugs |
| `$\forall x \in \varnothing\; P(x) \equiv \top$` | universal over nothing is true | vacuous truth | empty tables, empty lists, `if not xs:` |
| `$\exists x \in \varnothing\; P(x) \equiv \bot$` | existential over nothing is false | vacuous falsity | "no rows matched" for an existence claim |
| `$\forall x\, (P(x) \to Q(x)) \equiv \forall x\, (\neg P(x) \vee Q(x))$` | a requirement is a disjunction | "everyone who must, does" | specs stated as implications |
| `$k$` | the number of quantifiers in the sentence | nesting depth | runtime is `$\lvert D\rvert^k$`; two `$k$` are not comparable |
| `$\exists! y \in D\,(\forall x \in D\, P(x,y))$` | one value pairs with every value | a bijection when the sizes match | hashing, indexing, [Lesson 15](../part01_logic_proof/15_sets_and_cardinality.md) |
| `$\forall \alpha.\, (\alpha \to \beta) \to (\beta \to \alpha)$` | a law about *types*, not values | the swap law, checked for every pair of types at once | Hindley–Milner, System F, trait resolution; the "variable" $\alpha$ is not a value |
| `$\forall x \in A \subseteq D,\; P(x)$` | restricted quantification | "for all of this subcollection" | filtering before quantifying: `for all admins, …` |

## Worked Example

**The requirement, in English.** "Any request that is neither authenticated
nor aimed at a public endpoint must be rejected with 401."

**Step 1. Name the domain.** Requests. $R$ is the set of all requests this
service handles. This is not a formality: "all requests" and "all requests that
reached this handler" are different domains, and the bug in the code below is
partly a domain bug.

**Step 2. Name the predicates.** $A(r)$: request $r$ is authenticated. $P(r)$:
request $r$ targets a public endpoint. $D(r)$: request $r$ is denied.

**Step 3. Write the requirement.** A request that is neither one thing nor the
other must be denied:

$$\forall r \in R,\; (\neg A(r) \wedge \neg P(r)) \to D(r)$$

**Step 4. Write what the code does.**

```python
def handle(r):
    if not r.authenticated or not r.public:
        return 401
    return 200
```

**Step 5. Translate the code, honestly.** The condition is
`¬A(r) ∨ ¬P(r)`, and denial happens when that holds. Using the identity from
[Lesson 10](../part01_logic_proof/10_propositions_and_connectives.md), `(¬A ∨ ¬P) → D` is the same
proposition as `¬(¬A ∨ ¬P) ∨ D`, which is `(A ∧ P) ∨ D`. So the code says:

$$\forall r \in R,\; (A(r) \wedge P(r)) \vee D(r)$$

**Step 6. Compare, and notice that a complete requirement is a biconditional.**
Saying denial happens *exactly when* it must is two implications, and they have
different negations:

- **(a) under-enforcement** — everyone who must be denied is:
  `(¬A ∧ ¬P) → D`
- **(b) over-enforcement** — everyone else is let through: `(A ∨ P) → ¬D`

The requirement in step 3 only stated (a). A requirement written in one
direction is half a requirement, and the half you leave out is the half whose
absence no breach audit will ever notice.

| $A(r)$ | $P(r)$ | (a) requires | (b) requires | code | which half breaks |
| --- | --- | --- | --- | --- | --- |
| F | F | deny | — | deny | neither |
| F | T | — | allow | **deny** | (b) |
| T | F | — | allow | **deny** | (b) |
| T | T | — | allow | allow | neither |

**Step 7. Diagnose.** The programmer used `or` where the requirement says "and",
which is the De Morgan error from [Lesson 10](../part01_logic_proof/10_propositions_and_connectives.md)
wearing a different hat. `not A or not P` is true for any request that fails
*either* check, so a logged-in user hitting a private endpoint — `A` true, `P`
false — is denied 401 with a perfectly valid session, and an unauthenticated
request to `/health` is denied too, which takes the public endpoint offline.

**Step 8. Write both tests.** Negate each half and push the negations in.

For (a), under-enforcement:

$$\neg \forall r\, (\neg A(r) \wedge \neg P(r) \to D(r))
\;\equiv\; \exists r\, (\neg A(r) \wedge \neg P(r) \wedge \neg D(r))$$

"Every requirement-breaking request is denied" becomes "there exists a
requirement-breaking request that was not denied".

For (b), over-enforcement:

$$\neg \forall r\, ((A(r) \vee P(r)) \to \neg D(r))
\;\equiv\; \exists r\, ((A(r) \vee P(r)) \wedge D(r))$$

"There is an allowed request that was denied." Both negations are existentials,
so both are queries. Neither original statement was a query, and that is the
whole trick.

**Step 9. Run them, and see what the first one misses.** Against this code the
first test finds *nothing*. The code never lets a bad request through, because
its condition is strictly stronger than the requirement's, not weaker. Only the
second test fails, and it fails on two of the four input shapes.

That asymmetry is the lesson. A security check built from the negation of
direction (a) reports this code as **healthy** — the invariant `SELECT COUNT(*)
… WHERE NOT authenticated AND NOT public_endpoint AND status <> 401` returns 0
and the page stays green. The bug is an outage, not a breach, so a monitor
looking only for breaches never sees it. Both directions need a check, and the
over-enforcement one is the one nobody writes.

**Step 10. Negate the second specification, which needs two variables.** A
second requirement: "no two admins share a primary email address." The `u \neq v`
in the antecedent is load-bearing — without it the statement says that no admin
can be an admin, and it is false the instant one exists:

$$\forall u \in R\, \forall v \in R,\; (A(u) \wedge A(v) \wedge u \neq v) \to \mathrm{email}(u) \neq \mathrm{email}(v)$$

Its negation, with the rule applied to both quantifiers and then to the body:

$$\exists u\, \exists v,\; A(u) \wedge A(v) \wedge \mathrm{email}(u) = \mathrm{email}(v)$$

Read that as SQL and it is the query every engineer has written:

```sql
SELECT email, COUNT(*) FROM users
WHERE role = 'admin'
GROUP BY email
HAVING COUNT(*) > 1;
```

Three quantifiers, one disjunction, and the `GROUP BY … HAVING COUNT(*) > 1` is
literally the ∃∃ of two distinct rows. Note that the negation needs *two*
variables over the *same* domain — the naive `¬∃u (admin(u) ∧ …)` would only
ever find one admin, and would report the bug as absent.

**Step 11. Read the nested case.** A third requirement: "every request must have
at least one administrator who is allowed to approve it." Two readings exist
and they are not the same requirement:

- `$\forall r\, \exists a$`: each request may be handled by a *different*
  administrator. Two admins with complementary permissions satisfy this.
- `$\exists a\, \forall r$`: there is one administrator who can approve
  everything. A single superadmin satisfies this, and it is a much larger
  security concession.

The order of the quantifiers decides whether you are describing a routing
policy or granting a god-mode account. English does not distinguish them, and
neither does the code you are about to write.

## Runnable Code

### Predicates, two quantifiers, and a domain that might be empty

```python
USERS = [
    {"name": "ada", "admin": True, "active": True},
    {"name": "bob", "admin": False, "active": True},
    {"name": "cy", "admin": False, "active": False},
]


def forall(domain, pred):
    """Universal quantification: every element satisfies the predicate."""
    return all(pred(x) for x in domain)


def exists(domain, pred):
    """Existential quantification: at least one element satisfies it."""
    return any(pred(x) for x in domain)


def exactly_one(domain, pred):
    """Unique existence, written `exists!`."""
    return sum(1 for x in domain if pred(x)) == 1


def satisfying(domain, pred):
    """Which elements satisfy the predicate."""
    return [x["name"] for x in domain if pred(x)]


def refuting(domain, pred):
    """Which elements refute a universal claim. Empty iff the claim is true."""
    return [x["name"] for x in domain if not pred(x)]


def is_active(u):
    return u["active"]


def is_admin(u):
    return u["admin"]


def admin_and_active(u):
    return u["admin"] and u["active"]


def active_or_admin(u):
    return u["active"] or u["admin"]


DOMAIN = USERS

print("=" * 68)
print("1. The domain, and four predicates over it")
print("=" * 68)
print()
print(f"domain: {[u['name'] for u in DOMAIN]}   |domain| = {len(DOMAIN)}")
print()
print(f"{'predicate':<20} {'true for':<16} {'false for':<16} holds?")
for label, pred in [("is_active", is_active),
                    ("is_admin", is_admin),
                    ("admin and active", admin_and_active),
                    ("active or admin", active_or_admin)]:
    print(f"{label:<20} {str(satisfying(DOMAIN, pred)):<16} "
          f"{str(refuting(DOMAIN, pred)):<16} {forall(DOMAIN, pred)}")
print()
print("A predicate is just a function from the domain to True/False. Nothing")
print("else. The quantifier is the step that turns a per-element answer into a")
print("single answer about the whole domain, and that step is the one that")
print("carries all the risk: a universal claim is refuted by ONE bad element.")
print()

print("=" * 68)
print("2. Two quantifiers, same domain, opposite failure modes")
print("=" * 68)
print()

claims = [
    ("for all u: active(u)", forall, is_active),
    ("exists u: active(u)", exists, is_active),
    ("for all u: not active(u)", forall, lambda u: not u["active"]),
    ("exists u: not active(u)", exists, lambda u: not u["active"]),
    ("for all u: active(u) or admin(u)", forall, active_or_admin),
    ("exists! u: admin(u)", exactly_one, is_admin),
]

for text, quant, pred in claims:
    print(f"  {text:<36} -> {quant(DOMAIN, pred)}")
print()
print("Read the last three together. The universal claim 'active or admin' is")
print("False, and it is refuted by exactly the users in the refuting column")
print("above: cy. One element out of three is enough. The existential claim")
print("'exists! u: admin(u)' is True on the strength of a single element, and")
print("it is destroyed by a single additional one.")
print()

print("=" * 68)
print("3. Negation, computed rather than remembered")
print("=" * 68)
print()
pairs = [
    ("for all u: active(u)", forall, is_active,
     "exists u: not active(u)", exists, lambda u: not u["active"]),
    ("exists u: active(u)", exists, is_active,
     "for all u: not active(u)", forall, lambda u: not u["active"]),
    ("for all u: active(u) or admin(u)", forall, active_or_admin,
     "exists u: not active(u) and not admin(u)", exists,
     lambda u: not u["active"] and not u["admin"]),
]
print(f"{'claim':<34} {'':>5}  {'its negation':<38} {'':>5}  opposed?")
for a_text, qa, pa, b_text, qb, pb in pairs:
    va, vb = qa(DOMAIN, pa), qb(DOMAIN, pb)
    print(f"{a_text:<34} {str(va):>5}  {b_text:<38} {str(vb):>5}  {va != vb}")
print()
print("The quantifier flips AND the connective inside flips. The existential")
print("claim is refuted by a single witness; the universal claim by a single")
print("counterexample. That asymmetry is the entire content of the rule.")
print()
print("For `exists!` the negation is a genuinely different shape: it needs TWO")
print("variables, over the SAME domain.")
two_admins = exists(
    DOMAIN, lambda u: exists(DOMAIN, lambda v: u["admin"] and v["admin"] and u is not v)
)
print(f"  exists! u: admin(u)                          -> {exactly_one(DOMAIN, is_admin)}")
print(f"  exists u,v: admin(u) and admin(v) and u!=v   -> {two_admins}")
print()
print("A naive 'not exists u: admin(u)' would have said True, and it is False.")
print("This is the error that produces duplicate-key bugs and double-charge bugs")
print("in code that assumed 'the lookup found something, therefore it was unique'.")
print()

print("=" * 68)
print("4. Empty domains: the answers nobody expects")
print("=" * 68)
print()
print(f"{'domain':<12} {'forall(active)':>14} {'exists(active)':>14} "
      f"{'forall(not active)':>20}")
for label, domain in [("empty", []), ("one element", DOMAIN[:1]), ("all three", DOMAIN)]:
    print(f"{label:<12} {str(forall(domain, is_active)):>14} "
          f"{str(exists(domain, is_active)):>14} "
          f"{str(forall(domain, lambda u: not u['active'])):>20}")
print()
print("Over the empty domain the universal claim is True (vacuously: there is")
print("no user who is not active) and the existential claim is False (there is")
print("no active user). Both are correct, and both are worth stating explicitly,")
print("because 'no rows matched' means two different things depending on which")
print("quantifier you wrote.")
```

### Statements as data, so the negation rule is code you can test

```python
# The `truth`, `show` and `count_quantifiers` functions are the ones from the
# Runnable Code section, unchanged. Only `negate` is rebuilt here, with a
# switch for the bug we want to hunt.

UNARY = {
    "active": {"ada", "bob"},
    "admin": {"ada"},
    "audited": {"bob"},
    "verified": {"ada", "cy"},
}
RELATION = {
    "friend": {("ada", "bob"), ("bob", "ada"), ("bob", "cy"), ("cy", "bob")},
}
DOMAIN = ["ada", "bob", "cy"]


def make_negate(buggy=False):
    """Build a negation function. `buggy=True` forgets De Morgan on `and`:
    it returns `a and ~b` where it should return `~a or ~b`."""
    def negate(s):
        kind = s[0]
        if kind == "not":
            return s[1]
        if kind == "forall":
            return ("exists", s[1], negate(s[2]))
        if kind == "exists":
            return ("forall", s[1], negate(s[2]))
        if kind == "and":
            if buggy:
                return ("and", negate(s[1]), negate(s[2]))
            return ("or", negate(s[1]), negate(s[2]))
        if kind == "or":
            return ("and", negate(s[1]), negate(s[2]))
        if kind == "impl":
            return ("and", s[1], negate(s[2]))
        if kind in ("pred", "rel", "ne"):
            return ("not", s)
        raise ValueError(kind)
    return negate


def truth(s, env):
    kind = s[0]
    if kind == "not":
        return not truth(s[1], env)
    if kind == "pred":
        return env[s[2]] in UNARY[s[1]]
    if kind == "rel":
        return (env[s[2]], env[s[3]]) in RELATION[s[1]]
    if kind == "ne":
        return env[s[1]] != env[s[2]]
    if kind == "impl":
        return (not truth(s[1], env)) or truth(s[2], env)
    if kind == "and":
        return truth(s[1], env) and truth(s[2], env)
    if kind == "or":
        return truth(s[1], env) or truth(s[2], env)
    if kind == "forall":
        return all(truth(s[2], {**env, s[1]: v}) for v in DOMAIN)
    if kind == "exists":
        return any(truth(s[2], {**env, s[1]: v}) for v in DOMAIN)
    raise ValueError(kind)


def count_quantifiers(s):
    if s[0] in ("forall", "exists"):
        return 1 + count_quantifiers(s[2])
    if s[0] == "not":
        return count_quantifiers(s[1])
    if s[0] in ("and", "or", "impl"):
        return count_quantifiers(s[1]) + count_quantifiers(s[2])
    return 0


S = [
    ("every user is active", ("forall", "u", ("pred", "active", "u"))),
    ("some user is active", ("exists", "u", ("pred", "active", "u"))),
    ("no user is active", ("forall", "u", ("not", ("pred", "active", "u")))),
    ("every active user is verified",
     ("forall", "u", ("impl", ("pred", "active", "u"), ("pred", "verified", "u")))),
    ("some active user is not verified",
     ("exists", "u", ("and", ("pred", "active", "u"),
                      ("not", ("pred", "verified", "u"))))),
    ("every user has a friend",
     ("forall", "u", ("exists", "v", ("rel", "friend", "u", "v")))),
    ("some user has no friend",
     ("exists", "u", ("forall", "v", ("not", ("rel", "friend", "u", "v"))))),
    ("every user has an admin friend",
     ("forall", "u", ("exists", "v", ("and", ("rel", "friend", "u", "v"),
                                      ("pred", "admin", "v"))))),
    ("every user is active or an admin",
     ("forall", "u", ("or", ("pred", "active", "u"), ("pred", "admin", "u")))),
    ("some user is neither active nor an admin",
     ("exists", "u", ("and", ("not", ("pred", "active", "u")),
                      ("not", ("pred", "admin", "u"))))),
    ("every user has a distinct friend",
     ("forall", "u", ("exists", "v", ("and", ("rel", "friend", "u", "v"),
                                      ("ne", "u", "v"))))),
    ("at most one user is an admin",
     ("not", ("exists", "u", ("exists", "v",
                              ("and", ("pred", "admin", "u"),
                                     ("pred", "admin", "v"),
                                     ("ne", "u", "v")))))),
]

results = {}
for label, buggy in (("correct negate", False), ("buggy negate", True)):
    negate = make_negate(buggy=buggy)
    print("=" * 74)
    print(label)
    print("=" * 74)
    print(f"{'#':>2} {'statement':<40} {'|S|':>4} {'S':>6} {'~S':>6} {'ok':>5}")
    missed = []
    for i, (text, s) in enumerate(S, 1):
        t, nt = truth(s, {}), truth(negate(s), {})
        if t == nt:
            missed.append(i)
        print(f"{i:>2} {text:<40} {count_quantifiers(s):>4} {str(t):>6} "
              f"{str(nt):>6} {str(t != nt):>5}")
    print()
    print(f"  the negation law fails on: {missed if missed else 'nothing'}")
    print()
    results[label] = missed
```

**Read the two `missed` lists together, because that is the whole exercise.**
The correct `negate` passes all twelve. The buggy one — the one that forgets to
turn `and` into `or` — still passes 1, 2, 3, 6 and 7, which are exactly the
statements whose bodies are a single atom under one quantifier. There is no `and`
inside to mis-flip.

It is caught only by 4, 5, 8, 9, 10, 11 and 12: the statements with a compound
body. That is the general shape of the bug. The version of the negation rule that
people remember correctly is the version for sentences with one atom under one
quantifier, and that is the only version a beginner ever writes. Which is why the
rule should be code, tested against a table, rather than something reconstructed
under pressure.

</details>

**Q2.** Let $D = \mathbb{R}$ and let $P(x,y)$ mean "$x < y$". Which of the two
statements is true?

- A) `$\exists y \in D\, \forall x \in D\; P(x,y)$`
- B) `$\forall x \in D\, \exists y \in D\; P(x,y)$`
- C) Both are true
- D) Neither is true

<details>
<summary>Answer and explanation</summary>

**B) `$\forall x \in D\, \exists y \in D\; P(x,y)$`.**

For any real $x$, the value $y = x + 1$ satisfies $x < y$, so the existential
can always be discharged — and the witness is allowed to depend on $x$. That
dependence is exactly what distinguishes the two statements.

Option A says some real exceeds every real. For any candidate $y$, take $x = y$:
then $x < y$ is $y < y$, which is false. So A is False, and the disproof is a
single value chosen *after* seeing the witness, which is the asymmetry in one
sentence.

Option C is a real claim rather than a hedge, and it is False: one of the two
statements is true and the other is not. On a *finite* domain both can be
False at once — take $D = \{1,2,3\}$ and both fail, because 3 has nothing above
it. The domain matters, and choosing $\mathbb{R}$ is what separates them.

Option D is the same as C. That the two can both be false on a finite domain
does not make them equivalent, and "neither" is not available as an escape
when one of them has just been shown true.

</details>

**Q3.** What is the truth value of `$\forall x \in \varnothing\; P(x)$` for any
predicate P?

- A) False, because no element satisfies P
- B) True, vacuously
- C) Undefined, because the domain is empty
- D) True only if P is a tautology

<details>
<summary>Answer and explanation</summary>

**B) True, vacuously.**

The universal is false when *some* element falsifies the body. There is no
element, so the falsifying condition never triggers and the statement is true.
This is what the `empty` row of the fourth table in the first code block reports:
`forall(active)` is `True` on `[]`.

Option A confuses the universal with the existential. "No element satisfies P"
is the content of `∃x P(x)`, and the code prints that one as `False` on the
empty domain.

Option C is the tempting one, and it is wrong for a specific reason: a domain
being empty does not make any quantifier meaningless. `∅` is a perfectly good
set. What is meaningless is a *free* variable with nothing to range over, which
is a different failure and a real one — see the Common Mistakes entry on
unbound variables in [Lesson 10](../part01_logic_proof/10_propositions_and_connectives.md).

Option D confuses vacuous truth with tautology. A tautology is true on *every*
nonempty domain as well; vacuous truth is true on the empty domain and tells you
nothing about the others.

</details>

**Q4.** What is the negation of `$\exists! x \in D\; P(x)$`?

- A) `$\exists x \in D\; \neg P(x)$`
- B) `$\forall x \in D\; \neg P(x)$`
- C) `$\exists x \in D\, \exists y \in D,\; P(x) \wedge P(y) \wedge x \neq y$`
- D) `$\exists x \in D\, \exists y \in D,\; P(x) \wedge P(y)$`

<details>
<summary>Answer and explanation</summary>

**C) `$\exists x \in D\, \exists y \in D,\; P(x) \wedge P(y) \wedge x \neq y$`.**

The number of solutions is a natural number. "Not exactly one" therefore means
"zero" or "at least two", and zero is already excluded by the requirement that
the solution exist. So not-unique is exactly *two distinct* solutions, which is
option C. The code block prints this directly: with one admin in the domain,
`exists! u: admin(u)` is `True` and the two-witness form is `False`.

Option A is the negation of `∃x P(x)`, not of `∃!x P(x)`. It reports "no admin
at all", which is a different bug with a different fix.

Option B is `¬∃x P(x)`, the same thing again. Both A and B describe absence, and
the interesting failure of uniqueness is duplication.

Option D is almost right and is the classic near-miss: it is satisfied by a
*single* solution, because you can set x = y. The `x ≠ y` is the entire
difference. Option D is the negation of "at most one".

</details>

**Q5.** `$\forall x \in D\; (P(x) \to Q(x))$` is equivalent to which of the
following?

- A) `$\forall x \in D\; (P(x) \wedge Q(x))$`
- B) `$\forall x \in D\; (\neg P(x) \vee Q(x))$`
- C) `$\forall x \in D\; (Q(x) \to P(x))$`
- D) `$\forall x \in D\; \neg(P(x) \wedge Q(x))$`

<details>
<summary>Answer and explanation</summary>

**B) `$\forall x \in D\; (\neg P(x) \vee Q(x))$`.**

This is the theorem from [Lesson 10](../part01_logic_proof/10_propositions_and_connectives.md) with
the quantifier left in place: $P \to Q$ is $\neg P \vee Q$, and the quantifier
does not care. Read it: "every element either is not a P, or is a Q."

Option A drops the implication and keeps only the case where both hold. It is
strictly stronger: on the user domain, "every active user is an admin" is
False, and "every user is both active and an admin" is also False, but the
first fails for a reason (bob is active and not an admin) that the second
mis-describes.

Option C is the **converse**, not the negation or an equivalent. It swaps the
roles, and it is a genuinely different requirement. The contrapositive — which
*is* equivalent — is `∀x (¬Q(x) → ¬P(x))`.

Option D is the negation of "some element is both", which is the negation of
option A. It is False exactly when option A is True.

</details>

**Q6.** In SQL, `SELECT name FROM users u WHERE NOT EXISTS (SELECT 1 FROM
logins l WHERE l.user_id = u.id)` reports which users?

- A) Every user who has at least one login row
- B) Every user who has no login row
- C) The number of users who have no login row
- D) Every user, annotated with whether they have logins

<details>
<summary>Answer and explanation</summary>

**B) Every user who has no login row.**

`NOT EXISTS (...)` is true for exactly those users for whom the inner
existential is false — no login row matches. The code block runs this against a
four-row table and gets back a single name, `cy`, the one user with no logins.

Option A is the same query with `EXISTS` instead of `NOT EXISTS`, and it returns
the other three users. This is the whole existential/universal gap: the outer
`SELECT` is an existential in both cases, and the quantifier you actually care
about is the one inside the negation.

Option C is a real and often-useful query — `SELECT COUNT(*) …` with the same
`WHERE` — and it is what the fifth section of the code block runs to check an
invariant. But it is a different query returning a different type, not a
different reading of this one.

Option D describes a `LEFT JOIN` with a count in the select list, which is the
shape you want when the two cases are not alternatives you care about but facts
you want both. Returning both kinds of row from one query is a legitimate goal
and `NOT EXISTS` cannot do it.

</details>

**Q7.** A table `users` has 0 rows. What does `SELECT COUNT(*) FROM users WHERE
role = 'admin'` return, and what does it tell you?

- A) 0, and therefore the claim "every user is an admin" is true
- B) 0, and therefore the claim "some user is an admin" is true
- C) 0, and therefore nothing about either claim follows without knowing the
  domain
- D) An error, because the domain is empty

<details>
<summary>Answer and explanation</summary>

**C) 0, and therefore nothing about either claim follows without knowing the
domain.**

The count is definitely 0. What that *means* depends on which claim you were
checking. "Every user is an admin" is vacuously true, because there is no
counterexample. "Some user is an admin" is false, because there is no witness.
One query, one number, two opposite conclusions — and the query itself did not
say which conclusion it was supporting.

Option A reads the empty result as success, which is correct for the universal
and dangerously wrong for the existential. This is the single most expensive
ambiguity in production SQL: a nightly check of the form "count the violations,
assert zero" is silently also satisfied by an empty table, so a migration that
empties the table turns every invariant green.

Option B has the quantifier backwards — an empty existential is false, never
true.

Option D is wrong because `∅` is a legitimate domain. SQL handles it without
complaint, which is precisely why the mistake is easy to make.

</details>

**Q8.** How many quantifiers does `$\forall u\, ((\exists v\; A(u,v)) \wedge
(\neg \exists v\; B(u,v)))$` contain?

- A) 1
- B) 2
- C) 3
- D) 4

<details>
<summary>Answer and explanation</summary>

**C) 3.**

There is one `∀u` at the front, and two `∃v` inside — one positive in
`A(u,v)` and one under a negation in `B(u,v)`. The `not` does not remove a
quantifier, it only inverts it, so the count is 1 + 2 = 3. The
`count_quantifiers` function in the Runnable Code block computes exactly this,
and the table it prints uses the same rule for six sample statements.

Option A counts only the quantifiers that are syntactically outermost, which
measures the depth of the sentence rather than its size.

Option B forgets the negated `∃v`. This is the most common way to get the count
wrong, and it matters because the count is the cost: three quantifiers over a
domain of size $n$ cost up to $n^3$ predicate evaluations.

Option D double-counts the `v` because it appears in two separate quantifiers.
Reusing the letter is legal and does not merge the two scopes — the second `∃v`
binds only the `v` inside `B(u,v)`. Renaming them to `v₁` and `v₂` makes the
point immediately, and is exactly the bound-variable renaming from the Formal
Version.

</details>

**Q9.** A test suite covers 100% of branches in a function. What has been
established?

- A) The function is correct for every input
- B) Every input takes some branch, and every branch is reached by at least one
  test
- C) Every branch of the function has been executed at least once
- D) The function is correct for every input the test author thought of

<details>
<summary>Answer and explanation</summary>

**B) Every input takes some branch, and every branch is reached by at least one
test.**

Coverage is `∀ branch, ∃ test` — a universal over branches, an existential over
tests. The second half of B is the trivially true part: a total function's
inputs each land somewhere. Together they are the complete content of a
coverage number, and the code block in section 4 of the Runnable Code prints
the branch-by-branch table that makes the shape visible.

Option C is a strictly weaker restatement — it drops the "every input" half
entirely, so it describes even less than a coverage number does.

Option A is the claim people *hope* the number means, and the difference is
quantified exactly: correctness is `∀ input, program(input) = spec(input)`, a
universal over inputs, which no finite test set can establish. Section 4 of the
code block lists all three quantifiers side by side so the gap is visible
rather than argued.

Option D is closer than A and still wrong. Tests cover the inputs their author
imagined, but a universal claim needs *all* of them, including the one nobody
imagined — which is the entire reason property-based testing exists.

</details>

**Q10.** Which Python expression is the negation of "for every request `r`, `r` is
either authenticated or public"?

- A) `any(not r.authenticated and not r.public for r in requests)`
- B) `all(not r.authenticated and not r.public for r in requests)`
- C) `any(not r.authenticated or not r.public for r in requests)`
- D) `not all(r.authenticated or r.public for r in requests)`

<details>
<summary>Answer and explanation</summary>

**A) `any(not r.authenticated and not r.public for r in requests)`.**

The statement is `∀r (A(r) ∨ P(r))`. Negating flips the quantifier to `∃` and
applies De Morgan to the body: `¬(A ∨ P)` is `¬A ∧ ¬P`. `any` is the
existential, and inside it the disjunction has become a conjunction. A and B
are the two halves of the same mistake: `any` with `and` inside, or `all` with
`and` inside.

Option B keeps `all`, so it is the negation of the wrong sentence. It happens to
be False whenever the domain has even one element satisfying the requirement,
which is nearly always, so it reads as a plausible test and never fires.

Option C uses `any` with `or` inside. That is `∃r (¬A ∨ ¬P)`, the negation of
`∀r (A ∧ P)` — a different original sentence. It will fire on almost every
request and is the shape you write when you forget that `not A or not P` is not
`not (A or P)`. This is the [Lesson 10](../part01_logic_proof/10_propositions_and_connectives.md)
error wearing quantifiers.

Option D is the *logically correct* negation and the operationally useless one.
`not all(...)` is exactly `∃r ¬(A(r) ∨ P(r))` by definition of `all` and `not`,
so it is right. But it returns a bare boolean, and when it fires you have no
idea which request failed. A and D agree on the truth value and differ
completely on usefulness: the negation of a universal is supposed to hand you a
counterexample, and `not all` throws it away.

</details>

## Subjective Questions

### Short Answer

**Q1. What is the difference between a predicate and a proposition?**

<details>
<summary>Answer</summary>

A predicate is a formula with a free variable, so it has no truth value on its
own — only a truth value for each substitution from a stated domain. A
proposition is a closed sentence: no free variables, one definite truth value.

Equivalently, a predicate in one variable over $D$ is a function
$D \to \{\text{false}, \text{true}\}$, and a proposition is a function from the
one-element set $\{\ast\}$ to the same codomain. "The request is authenticated"
is a predicate; "every request is authenticated" is a proposition.

</details>

**Q2. State the two quantifier-negation rules and say, in one sentence each, why
they are true.**

<details>
<summary>Answer</summary>

`¬∀x P(x) ≡ ∃x ¬P(x)`, because "not every element works" and "some element
fails" are two descriptions of the same situation, differing only in emphasis.

`¬∃x P(x) ≡ ∀x ¬P(x)`, because "no element works" and "every element fails" are
the same situation stated negatively and positively.

In both, the quantifier flips *and* the body is negated. Forgetting the second
half is the standard error.

</details>

**Q3. What is a counterexample, and why is it the only thing you need to refute
a universal claim?**

<details>
<summary>Answer</summary>

A counterexample to `∀x ∈ D, P(x)` is a single $d \in D$ with $P(d)$ false.

It is sufficient because the universal is false the moment any one element
falsifies it — there is no threshold and no averaging. It is *necessary* because
if no element falsifies the body then every element satisfies it, which is the
universal holding. So the refutation is complete with one value, and the
practical consequence is that a failing property-based test hands you everything
you need to fix the code.

</details>

**Q4. On a domain with no elements, what are `∀x P(x)` and `∃x P(x)`? Explain
both in one sentence each.**

<details>
<summary>Answer</summary>

`∀x P(x)` is true, vacuously: it is false only if some element falsifies the
body, and there is no element.

`∃x P(x)` is false: it needs an element satisfying the body, and there is none.

The pair matters operationally because an empty result set means the first
passes and the second fails, so a check that only looks at whether rows came
back cannot tell you which claim it discharged.

</details>

**Q5. How many quantifiers are in `∀u (∃v P(u,v) ∧ ¬∃v Q(u,v))`, and what does
each one cost?**

<details>
<summary>Answer</summary>

Three: one `∀u` and two `∃v` — the negation inverts the quantifier but does not
remove it.

Over a domain of size $n$ each costs at most $n$ evaluations, and they are
sequenced, so the total is at most $n^3$ predicate calls. That is the practical
content of "counting quantifiers": the number is a loop count, and $n^3$ is a
runtime. The same statement over a countably infinite domain is not decidable
by enumeration at all — see [Lesson 15](../part01_logic_proof/15_sets_and_cardinality.md).

</details>

**Q6. Why does `SELECT COUNT(*) … WHERE NOT EXISTS (SELECT 1 FROM …)` need the
`NOT` to be inside?**

<details>
<summary>Answer</summary>

Because "no row satisfies P" is a statement about the *whole* table, while the
`WHERE` filters one row at a time. `EXISTS (SELECT 1 FROM logins WHERE …)`
evaluates to a per-row boolean, and `NOT EXISTS` negates that per-row boolean —
so the negation applies where the row filter is, not where the table is.

The consequence is that the query returns a *list of counterexamples* rather
than a verdict. Counting those rows and asserting zero is how you turn it back
into a verdict, and the `COUNT(*)` is doing the universal's job.

</details>

### Long Answer

**Q1. Your requirement is `∀r, (¬A(r) ∧ ¬P(r)) → D(r)`. A test suite passes and
nobody has found a bug. What exactly has been established, and what would break
the conclusion?**

<details>
<summary>Model answer</summary>

What has been established is a finite list of existentials. Each test asserts
`∃r` — a specific request with specific properties, for which the code returned
401. The requirement is a universal over all requests, and the gap between
"every request" and "the requests I wrote down" is not a matter of degree.

Three things would break the conclusion, and they are worth separating because
they need different defences.

**The domain is unstated.** "All requests" is not a set. If it means all
requests that reach this handler, then the test suite is missing everything the
gateway rejected upstream, the ones that timed out, and the ones on the other
two replicas. If it means all requests in existence, it includes ones this
service has never heard of. The universal is only as strong as the domain, and
the domain is a decision someone made in a design document that nobody has
re-read.

**The negation is not testable as written.** You cannot assert `∀r … D(r)`
directly; you can only assert its negation, `∃r (¬A(r) ∧ ¬P(r) ∧ ¬D(r))`. A test
suite that asserts the positive form is asserting a universal, which means it is
either asserting something trivially weak or it is quietly searching for one
specific counterexample and calling that coverage.

**The suite has no notion of a counterexample generator.** The reason property
testing finds bugs unit tests miss is not that it tries harder; it is that it
*constructs* values from the type of the domain rather than from the
imagination of the author. A generator over requests, filtered to those with
`¬A ∧ ¬P`, produces the witness directly.

The concrete fix is to write the test as the negated form, to state the domain
in the test, and to generate the witness rather than enumerate it by hand.

</details>

**Q2. `∀x ∃y P(x,y)` and `∃y ∀x P(x,y)` are both natural English sentences. Give a
concrete system where the difference decides whether a product ships, and
explain what a greedy implementation of the first one gets wrong.**

<details>
<summary>Model answer</summary>

Take an assignment system. $D$ is the set of tasks, and $P(t, s)$ means "worker
`s` is qualified for task `t`."

`∀t ∃s P(t, s)` says every task has *some* qualified worker. It is satisfiable
with a team of two complementary generalists, and it is the requirement almost
every staffing problem actually wants.

`∃s ∀t P(t, s)` says one worker is qualified for everything. It demands a
superworker, it is much harder to satisfy, and it usually implies an enormous
privilege concentration — one account that can approve anything, which is
precisely the kind of thing an audit later objects to.

The implementation trap is that the two look identical in code. A greedy
matching for `∀t ∃s` walks the tasks in order and assigns each the first
qualified worker still free. Suppose the workers are {ann, ben} and the tasks
are: ann can do T1 and T2; ben can do T1 only. Greedy in task order T1, T2
gives T1 to ann, then T2 has nobody, and the loop reports failure — even though
assigning T1 to ben and T2 to ann satisfies `∀t ∃s`. The requirement is
satisfied; the greedy search failed.

That failure is not a bug in the requirement, it is a property of the search
strategy, and it is why real systems use maximum bipartite matching rather than
first-fit. The general principle: `∀∃` is a *global* feasibility question and
any local choice can paint the whole thing into a corner, while `∃∀` is a
single lookup that can never surprise you.

</details>

**Q3. `NOT IN` in SQL returns an empty set when a `NULL` is present in the
column, even though a matching row exists. Explain this in terms of quantifiers
and three-valued logic, and say what it tells us about adding a third truth
value.**

<details>
<summary>Model answer</summary>

`x NOT IN (a, b)` expands to `x <> a AND x <> b` — a universal over the list,
written as a conjunction of the negations of its memberships. When `x` is NULL,
each `x <> a` is UNKNOWN rather than TRUE, because SQL will not assert that
NULL is different from anything. An AND with an UNKNOWN operand is UNKNOWN.
`WHERE` keeps only rows that evaluate to TRUE, so the row is discarded.

Note the quantifier is doing real work here: `x IN (a,b)` is an existential
(`∃y ∈ {a,b}, x = y`) and works fine on NULL, because UNKNOWN OR TRUE is TRUE
and UNKNOWN OR FALSE is also UNKNOWN — but the row is kept only if the whole
thing is TRUE, and the *positive* `IN` returns TRUE when a later element matches.
The negation is what exposes the hole, because it forces the engine to evaluate
*every* disjunct.

The deeper point is that UNKNOWN is a genuine third answer meaning "the database
does not know", and it is not reducible to FALSE. A `NULL` column is a claim
about missing information, and a two-valued logic has no way to say "this is not
false, it is unanswered." Collapsing it to FALSE is what produces the empty
result set, because "we don't know the role" was silently read as "the role is
admin-or-user" and then rejected.

The fix is never to remember a rule. It is to state the intent as a
disjunction that includes the unknown case — `role IS NULL OR role NOT IN (...)`
— or to remove the possibility with a `NOT NULL` constraint plus a sentinel
value. Design the type so the question cannot arise.

</details>

**Q4. Type checkers prove `∀α. (α → α) → α → α` for all types. Our unit tests
check `apply_twice` on eight sample values and conclude it works. What is the
structural difference between the two arguments, and why is the second one not
slightly weaker but categorically different?**

<details>
<summary>Model answer</summary>

The type checker's argument is *structural*. The body of `apply_twice` is
`f(f(x))`. The term `f` is assumed to map α to α; the inner application therefore
has type α; feeding it back to `f` yields α; that is the result type. Nothing in
that reasoning mentions any particular type, so it applies uniformly to every
instantiation of α. The proof has one shape and quantifies over all types
without ever enumerating them.

The test suite's argument is *enumerative*. Eight samples is a witness
construction: here are eight values, and on each of them the function behaved.
It establishes an existential — "there exist eight values on which it works" —
where the statement needed is universal. The two are not close in strength. The
samples say nothing at all about the ninth value, and there is no mechanism by
which adding a ninth sample would change that. Enumerating a universal
quantifier over an infinite domain does not get you closer; it just produces a
longer list.

The categorically different part is where the justification lives. The type
argument is about the *code*, so it transfers to every input the function will
ever see, including ones written after the test was authored. The test argument
is about the *data*, so it is only as good as the imagination of whoever chose
the data, and it rots the first time someone calls the function with a type
nobody tried.

This is also the reason [Lesson 14](../part01_logic_proof/14_mathematical_induction.md) exists: induction
is the technique that converts a structural argument about code into a
universal claim about an infinite domain, without enumeration. The type
checker's rule for `f(f(x))` and the induction step for a recursive function are
the same argument at two levels of a grammar.

</details>

## Exercises and Solutions

**[ ] Exercise 1 — Write six requirements as quantifiers, then negate each one.**
For each English requirement below: (a) name the domain, (b) name the
predicates, (c) write the quantified statement, (d) write its negation with all
negations pushed inside, and (e) say in one sentence whether the negation is
something you could turn into a test.

1. Every active user has a verified email address.
2. Some user has administrative privileges.
3. No request is both unauthenticated and approved.
4. Every user has at least one distinct collaborator.
5. At most one user holds the `owner` role.
6. Every project has a maintainer who is a member of that project.

<details>
<summary>Solution</summary>

```python
# Domains:
#   U = users, P = projects, R = requests
# Predicates:
#   active(u) verified(u) admin(u) approved(r) member(u, p) maintains(u, p)
#   role(u) == 'owner'

print("=" * 78)
print("1. every active user has a verified email")
print("   S : for all u: active(u) -> verified(u)")
print("   ~S: exists u: active(u) and not verified(u)")
print("   testable? YES -- one row is the whole test")
print()
print("=" * 78)
print("2. some user has administrative privileges")
print("   S : exists u: admin(u)")
print("   ~S: for all u: not admin(u)")
print("   testable? NO as a check on a live system. The negation is a")
print("         universal, so refuting it means scanning every user.")
print()
print("=" * 78)
print("3. no request is both unauthenticated and approved")
print("   S : for all r: not (not auth(r) and approved(r))")
print("   S : for all r: (not auth(r) -> not approved(r))")
print("   ~S: exists r: not auth(r) and approved(r)")
print("   testable? YES, and it is the exact SQL invariant from the lesson:")
print("         SELECT COUNT(*) FROM requests")
print("         WHERE NOT authenticated AND approved;   -- must be 0")
print()
print("=" * 78)
print("4. every user has at least one distinct collaborator")
print("   S : for all u: exists v: collab(u, v) and u != v")
print("   ~S: exists u: for all v: not collab(u, v) or v == u")
print("   testable? PARTIALLY. The negation is a nested pair, so you need the")
print("         'u with no other collaborator' query, not a global count.")
print()
print("=" * 78)
print("5. at most one user holds the owner role")
print("   S : for all u: for all v: (owner(u) and owner(v)) -> u == v")
print("   ~S: exists u: exists v: owner(u) and owner(v) and u != v")
print("   testable? YES, with GROUP BY / HAVING COUNT(*) > 1. Note the negation")
print("         needs TWO variables; `not exists u: owner(u)` is not it.")
print()
print("=" * 78)
print("6. every project has a maintainer who is a member of that project")
print("   S : for all p: exists u: maintains(u, p) and member(u, p)")
print("   ~S: exists p: for all u: not (maintains(u, p) and member(u, p))")
print("   testable? YES. The order matters: `for all u: exists p` would mean")
print("         every user maintains some project, a different requirement.")
```

The pattern worth taking away: **1, 3, 5 and 6 negate to existentials over
things you can point at, so they become queries. 2 negates to a universal over
every user, so it cannot be tested without a full scan. 4 negates to a nested
pair and needs a per-object search.** Whether a requirement is testable is
decided entirely by what its negation looks like.

</details>

**[ ] Exercise 2 — Build an evaluator for quantified statements and check the
negation law over twelve statements.** Write a small first-order evaluator
taking statements as tuples, as in the Runnable Code section. Then for twelve
statements over a fixed domain, (a) print the truth of each, (b) print the
truth of its negation as computed by your `negate` function, and (c) confirm
they are always opposite. Finally, deliberately introduce a bug into `negate`
— make it fail to flip `and` to `or` — and report which of the twelve catches
it.

<details>
<summary>Solution</summary>

```python
UNARY = {
    "active": {"ada", "bob"},
    "admin": {"ada"},
    "audited": {"bob"},
    "verified": {"ada", "cy"},
}
RELATION = {
    "friend": {("ada", "bob"), ("bob", "ada"), ("bob", "cy"), ("cy", "bob")},
}
DOMAIN = ["ada", "bob", "cy"]

QUANTIFIERS = {"forall", "exists"}


def make_negate(buggy=False):
    """Build a negation function. `buggy=True` forgets De Morgan on `and`."""
    def negate(s):
        kind = s[0]
        if kind == "not":
            return s[1]
        if kind == "forall":
            return ("exists", s[1], negate(s[2]))
        if kind == "exists":
            return ("forall", s[1], negate(s[2]))
        if kind == "and":
            if buggy:
                return ("and", negate(s[1]), negate(s[2]))
            return ("or", negate(s[1]), negate(s[2]))
        if kind == "or":
            return ("and", negate(s[1]), negate(s[2]))
        if kind == "impl":
            return ("and", s[1], negate(s[2]))
        if kind in ("pred", "rel", "ne"):
            return ("not", s)
        raise ValueError(kind)
    return negate


def truth(s, env):
    kind = s[0]
    if kind == "not":
        return not truth(s[1], env)
    if kind == "pred":
        return env[s[2]] in UNARY[s[1]]
    if kind == "rel":
        return (env[s[2]], env[s[3]]) in RELATION[s[1]]
    if kind == "ne":
        return env[s[1]] != env[s[2]]
    if kind == "impl":
        return (not truth(s[1], env)) or truth(s[2], env)
    if kind == "and":
        return truth(s[1], env) and truth(s[2], env)
    if kind == "or":
        return truth(s[1], env) or truth(s[2], env)
    if kind == "forall":
        return all(truth(s[2], {**env, s[1]: v}) for v in DOMAIN)
    if kind == "exists":
        return any(truth(s[2], {**env, s[1]: v}) for v in DOMAIN)
    raise ValueError(kind)


def count_quantifiers(s):
    if s[0] in QUANTIFIERS:
        return 1 + count_quantifiers(s[2])
    if s[0] == "not":
        return count_quantifiers(s[1])
    if s[0] in ("and", "or", "impl"):
        return count_quantifiers(s[1]) + count_quantifiers(s[2])
    return 0


def show(s):
    k = s[0]
    if k == "not":
        return f"not ({show(s[1])})"
    if k == "pred":
        return f"{s[1]}({s[2]})"
    if k == "rel":
        return f"{s[1]}({s[2]}, {s[3]})"
    if k == "ne":
        return f"{s[1]} != {s[2]}"
    if k == "impl":
        return f"({show(s[1])} -> {show(s[2])})"
    if k == "and":
        return f"({show(s[1])} and {show(s[2])})"
    if k == "or":
        return f"({show(s[1])} or {show(s[2])})"
    if k == "forall":
        return f"for all {s[1]}: {show(s[2])}"
    return f"exists {s[1]}: {show(s[2])}"


S = [
    ("every user is active", ("forall", "u", ("pred", "active", "u"))),
    ("some user is active", ("exists", "u", ("pred", "active", "u"))),
    ("no user is active", ("forall", "u", ("not", ("pred", "active", "u")))),
    ("every active user is verified",
     ("forall", "u", ("impl", ("pred", "active", "u"), ("pred", "verified", "u")))),
    ("some active user is not verified",
     ("exists", "u", ("and", ("pred", "active", "u"),
                      ("not", ("pred", "verified", "u"))))),
    ("every user has a friend",
     ("forall", "u", ("exists", "v", ("rel", "friend", "u", "v")))),
    ("some user has no friend",
     ("exists", "u", ("forall", "v", ("not", ("rel", "friend", "u", "v"))))),
    ("every user has a friend who is an admin",
     ("forall", "u", ("exists", "v", ("and", ("rel", "friend", "u", "v"),
                                      ("pred", "admin", "v"))))),
    ("every user is active or an admin",
     ("forall", "u", ("or", ("pred", "active", "u"), ("pred", "admin", "u")))),
    ("some user is neither active nor an admin",
     ("exists", "u", ("and", ("not", ("pred", "active", "u")),
                      ("not", ("pred", "admin", "u"))))),
    ("every user has a distinct friend",
     ("forall", "u", ("exists", "v", ("and", ("rel", "friend", "u", "v"),
                                      ("ne", "u", "v"))))),
    ("at most one user is an admin",
     ("forall", "u", ("forall", "v",
                      ("impl", ("and", ("pred", "admin", "u"),
                                ("pred", "admin", "v")),
                       ("ne", "u", "v"))))),
]

for label, buggy in (("correct negate", False), ("buggy negate", True)):
    negate = make_negate(buggy=buggy)
    print("=" * 74)
    print(label)
    print("=" * 74)
    print(f"{'#':>2} {'statement':<40} {'|S|':>4} {'S':>6} {'~S':>6} {'ok':>5}")
    caught, missed = [], []
    for i, (text, s) in enumerate(S, 1):
        t, nt = truth(s, {}), truth(negate(s), {})
        ok = t != nt
        if ok:
            caught.append(i)
        else:
            missed.append(i)
        print(f"{i:>2} {text:<40} {count_quantifiers(s):>4} {str(t):>6} "
              f"{str(nt):>6} {str(ok):>5}")
    print()
    print(f"statements where the law held : {len(caught)} of {len(S)}")
    print(f"statements that caught the bug : {caught if buggy else '(n/a)'}")
    print(f"statements that missed the bug : {missed if buggy else '(n/a)'}")
    print()

print("Read the two tables together. The correct negate passes all twelve.")
print("The buggy one still passes 1, 2, 3, 6 and 7 -- the statements whose")
print("bodies are a single atom under the quantifier, where there is no `and`")
print("to mis-flip. It is caught only by 4, 5, 8, 9, 10, 11 and 12: the ones")
print("with a compound body. That is the lesson of the exercise: the bug is")
print("invisible on exactly the sentences a beginner writes, because a beginner")
print("puts one predicate under one quantifier.")
```

</details>

**[ ] Exercise 3 — Audit an access check in both directions, and write the
health checks that would have caught it.** Given this handler:

```python
def handle(r):
    if not r.authenticated or not r.public:
        return 401
    return 200
```

and the requirement "deny with 401 exactly those requests that are neither
authenticated nor aimed at a public endpoint": (a) write the complete
requirement as two quantified statements, one for each direction; (b) enumerate
all four combinations of (authenticated, public) and mark which direction the
code breaks; (c) give the corrected handler; (d) load the seven requests below
into `sqlite3` with a column recording the status the code actually returned,
then write the two health-check queries, one per direction, and report how many
rows each returns; (e) say which single query an on-call engineer should be
paged on, and why the other one is a trap.

The data:

| id | path | authenticated | public_endpoint | status the code returned |
| --- | --- | --- | --- | --- |
| 1 | `/health` | no | yes | 401 |
| 2 | `/users` | yes | no | 401 |
| 3 | `/users` | no | no | 401 |
| 4 | `/status` | no | yes | 401 |
| 5 | `/admin` | no | no | 401 |
| 6 | `/admin` | yes | no | 401 |
| 7 | `/admin` | yes | yes | 200 |

<details>
<summary>Solution</summary>

```python
import sqlite3

REQUESTS = [
    # (id, path, authenticated, public_endpoint, status_returned)
    (1, "/health", 0, 1, 401),   # public, unauthenticated  -> should be 200
    (2, "/users",  1, 0, 401),   # private, authenticated  -> should be 200
    (3, "/users",  0, 0, 401),   # private, unauthenticated -> should be 401
    (4, "/status", 0, 1, 401),   # public, unauthenticated  -> should be 200
    (5, "/admin",  0, 0, 401),   # private, unauthenticated -> should be 401
    (6, "/admin",  1, 0, 401),   # private, authenticated  -> should be 200
    (7, "/admin",  1, 1, 200),   # private AND authenticated -> should be 200
]


def required_401(auth, public):
    """The requirement's direction (a): neither authenticated nor public."""
    return (not auth) and (not public)


def code_401(auth, public):
    """What the handler does: `(not auth) or (not public)`."""
    return (not auth) or (not public)


print("=" * 78)
print("(a) and (b) the two directions, and where the code breaks")
print("=" * 78)
print()
print("  (a) under-enforcement:  for all r, (not A(r) and not P(r)) -> D(r)")
print("  (b) over-enforcement :  for all r, (A(r) or P(r))      -> not D(r)")
print()
print(f"{'auth':>5} {'public':>7} {'(a) needs':>10} {'(b) needs':>10} "
      f"{'code':>5}  verdict")
under = over = 0
for auth in (False, True):
    for public in (False, True):
        a, b, c = required_401(auth, public), not required_401(auth, public), code_401(auth, public)
        note = "ok"
        if c and not a:
            note = "over-enforcing (b) broken"
            over += 1
        elif a and not c:
            note = "under-enforcing (a) broken"
            under += 1
        elif a and c:
            note = "ok"
        print(f"{str(auth):>5} {str(public):>7} {str(a):>10} {str(b):>10} "
              f"{str(c):>5}  {note}")
print()
print(f"  combinations breaking (a): {under}   (the security direction)")
print(f"  combinations breaking (b): {over}   (the availability direction)")
print()
print("  The code breaks direction (b) on exactly the two shapes where at")
print("  least one of A, P holds. Direction (a) is never broken: the code's")
print("  condition is strictly STRONGER than the requirement's, so it denies")
print("  a superset of the required set. `or` where `and` was meant always")
print("  over-denies; it under-denies only if the programmer also flipped the")
print("  negation, e.g. `if not (r.authenticated and r.public)`.")
print()
print("  which malformed condition is equivalent to the requirement's?")
print("  (deny exactly when `not A and not P` holds)")
print()
print(f"{'condition':<34} {'denies on':<26} verdict")
for cond in ["not A or not P", "not (A or P)", "not (A and P)", "A or P",
             "not A and not P", "not P or A"]:
    denies = []
    for auth in (False, True):
        for public in (False, True):
            got = eval(cond, {}, {"A": auth, "P": public})
            if got:
                denies.append(f"{'T' if auth else 'F'},{'T' if public else 'F'}")
    right = (cond == "not A and not P")
    print(f"{cond:<34} {', '.join(denies):<26} "
          f"{'CORRECT' if right else 'over-denies'}")
print()
print("  Only one of the six is right, and it is the one that is a conjunction")
print("  of two negations -- which is exactly what the English said. Every")
print("  other plausible spelling denies at least one case the requirement")
print("  permits. The table is four rows long; there is no reason to argue")
print("  about `or` versus `and` when you can enumerate.")
print()

print("=" * 78)
print("(c) the corrected handler")
print("=" * 78)
print()
print("""
def handle(r):
    if not r.authenticated and not r.public:
        return 401
    return 200
""")
print("`and`, not `or`. The requirement is a conjunction of two negations, and")
print("De Morgan was applied in the wrong direction when the code was written.")
print()

print("=" * 78)
print("(d) the two health checks, run against the data")
print("=" * 78)
print()
con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE requests (id INTEGER, path TEXT, "
            "authenticated INTEGER, public_endpoint INTEGER, status INTEGER)")
cur.executemany("INSERT INTO requests VALUES (?, ?, ?, ?, ?)", REQUESTS)


def rows(sql):
    cur.execute(sql)
    return [tuple(r) for r in cur.fetchall()]


CHECK_A = """
SELECT COUNT(*) FROM requests
WHERE NOT authenticated AND NOT public_endpoint AND status <> 401
"""
CHECK_B = """
SELECT COUNT(*) FROM requests
WHERE (authenticated OR public_endpoint) AND status = 401
"""
LIST_B = """
SELECT id, path, status FROM requests
WHERE (authenticated OR public_endpoint) AND status = 401
ORDER BY id
"""
print("  direction (a), under-enforcement -- the security check")
print("      WHERE NOT authenticated AND NOT public_endpoint AND status <> 401")
print("    ->", rows(CHECK_A)[0][0], "violations")
print()
print("  direction (b), over-enforcement -- the availability check")
print("      WHERE (authenticated OR public_endpoint) AND status = 401")
print("    ->", rows(CHECK_B)[0][0], "violations")
print()
print("  the rows behind direction (b):")
for r in rows(LIST_B):
    print(f"    id={r[0]}  path={r[1]:<9} returned {r[2]}")
print()
print("  Direction (a) reports ZERO. The system is, by the one security check")
print("  anybody writes, perfectly healthy -- while every authenticated user")
print("  in the table is being logged out by a valid session and the public")
print("  endpoints are returning 401 to the entire internet.")
print()

print("=" * 78)
print("(e) which query should page someone")
print("=" * 78)
print()
print("  Direction (b) first, because it is the direction with symptoms. Every")
print("  user complaint this code produces -- 'I am logged out', '/health is")
print("  down' -- is an instance of it, and 4 of 7 rows are instances of it.")
print("  A monitor on (b) would have paged somebody before the second deploy.")
print()
print("  Direction (a) is not useless, it is just not sufficient. It is the")
print("  only one that catches a genuine breach, and a future regression that")
print("  writes `if r.authenticated and not r.public:` would break (a) while")
print("  leaving (b) partly satisfied. Two monitors, two pages.")
print()
print("  But the real lesson is one step earlier and needs no query at all.")
print("  This check returns 0 for the correct handler and 0 for this one. A")
print("  monitor that cannot distinguish right from wrong is worse than no")
print("  monitor, because it converts an open question into a closed one. The")
print("  fix is upstream of SQL: write both directions of the requirement down")
print("  at the same time, and check that each one's negation is a query you")
print("  can actually run. A requirement you can only state in one direction")
print("  is a requirement whose other half will never be tested by anyone.")
con.close()
```

</details>

**[ ] Exercise 4 — Separate `∀∃` from `∃∀` with a concrete counterexample, and
show what greedy matching gets wrong.** Consider a small world of four people
and a `friend` relation. (a) Give a relation for which `∀u ∃v friend(u,v)` is
true but `∃v ∀u friend(u,v)` is false, and verify by enumeration. (b) Give a
*different* relation for which both are false, and say what that pair tells you
about the implication between the two statements. (c) Write a greedy witness
finder for `∀u ∃v` and a correct one (search all of $D \times D$), and exhibit
an input where they disagree. (d) Explain, in terms of what a code reviewer can
see, why this class of bug survives a passing test suite.

<details>
<summary>Solution</summary>

```python
import itertools

PEOPLE = ["ann", "ben", "cid", "dot"]


def all_have_a_friend(edges):
    """for all u: exists v friend(u, v)"""
    return all(any((u, v) in edges for v in PEOPLE) for u in PEOPLE)


def one_friend_to_all(edges):
    """exists v: for all u friend(u, v)"""
    return any(all((u, v) in edges for u in PEOPLE) for v in PEOPLE)


def greedy_witnesses(order, edges):
    """for all u: exists v P(u,v), by giving each u its first *free* v.

    The bug is not that it can fail to find a witness. The bug is that it can
    CONSUME the v another u needs, because it silently solves the stronger
    problem `for all u: exists v, P(u,v) and v not yet used`.
    """
    used = set()
    table = {}
    for u in order:
        for v in PEOPLE:
            if (u, v) in edges and v not in used:
                table[u] = v
                used.add(v)
                break
    return table


def plain_witnesses(edges):
    """for all u: exists v P(u,v), with no constraint at all between the v's."""
    table = {}
    for u in PEOPLE:
        options = [v for v in PEOPLE if (u, v) in edges]
        if not options:
            return None
        table[u] = options[0]
    return table


def grid(edges):
    header = "  " + "".join(f"{v:>5}" for v in PEOPLE)
    rows = "".join(f"{u:>5}" + "".join(f"{('X' if (u, v) in edges else '.'):>5}"
                                       for v in PEOPLE) + "\n" for u in PEOPLE)
    return header + "\n" + rows


WORLD_A = {("ann", "ben"), ("ben", "ann"), ("ben", "cid"), ("cid", "ben"),
           ("cid", "dot"), ("dot", "cid"), ("ann", "dot")}
WORLD_B = {("ann", "ben")}

print("=" * 78)
print("(a) for-all/exists true, exists/for-all false")
print("=" * 78)
print()
print(f"  edges: {sorted(WORLD_A)}")
print()
print(grid(WORLD_A))
print(f"  for all u: exists v: friend(u, v)  -> {all_have_a_friend(WORLD_A)}")
print(f"  exists v: for all u: friend(u, v)  -> {one_friend_to_all(WORLD_A)}")
print()

print("=" * 78)
print("(b) a world where BOTH are false")
print("=" * 78)
print()
print(f"  edges: {sorted(WORLD_B)}")
print(f"  for all u: exists v: friend(u, v)  -> {all_have_a_friend(WORLD_B)}")
print(f"  exists v: for all u: friend(u, v)  -> {one_friend_to_all(WORLD_B)}")
print()
print("  WORLD_A shows exists/for-all does NOT imply for-all/exists.")
print("  Neither world shows the converse, and no finite world can: with a")
print("  single person the two statements coincide, because there is only one")
print("  candidate witness. The converse needs a domain of size 2 or more,")
print("  or an element related to itself.")
print()

WORLD_C = {("ann", "ben"), ("ben", "ann"), ("cid", "ben"), ("dot", "ann")}
print("=" * 78)
print("(c) greedy versus exhaustive, on a world built to punish greedy")
print("=" * 78)
print()
print(f"  edges: {sorted(WORLD_C)}")
for u in PEOPLE:
    print(f"  {u}'s only option: {[v for v in PEOPLE if (u, v) in WORLD_C]}")
print()
greedy = greedy_witnesses(PEOPLE, WORLD_C)
plain = plain_witnesses(WORLD_C)
print(f"  greedy     : {greedy}  -> {len(greedy)} of {len(PEOPLE)}")
print(f"  exhaustive : {plain}  -> {len(plain)} of {len(PEOPLE)}")
print()
print("  The requirement HOLDS and the greedy search reports failure. Read the")
print("  fix carefully: `for all u, exists v, P(u,v) and u != v` is a *different,")
print("  stronger* requirement -- a matching -- and only under that reading is")
print("  first-fit even the right algorithm, and even then it needs a backtrack.")
print()

print("=" * 78)
print("(d) the same requirement, three ways of varying the input")
print("=" * 78)
print()
VARIANTS = [
    ("original order", ["ann", "ben", "cid", "dot"], WORLD_C),
    ("cid, dot first", ["cid", "dot", "ann", "ben"], WORLD_C),
    ("bob first", ["bob", "ann", "cid", "dot"], WORLD_C),
    ("ann friends itself", ["ann", "ben", "cid", "dot"],
     WORLD_C | {("ann", "ann")}),
]
for label, order, edges in VARIANTS:
    g = greedy_witnesses(order, edges)
    dropped = [u for u in order if u not in g]
    print(f"  {label:<22} greedy {g}   dropped {dropped}")
print()
print("  Four variations, four different pairs of casualties, one requirement")
print("  that holds in all four. No hand-picked case set walks into all of it,")
print("  which is the argument for generating the relation rather than writing")
print("  it.")
print()
print("  The natural test for this function is a property, not an example:")
print("  'whenever every person has some option, the search assigns all of")
print("  them'. That is true of the exhaustive search and false of the greedy")
print("  one, and here it is checked over all 256 relations drawn from eight")
print("  candidate edges rather than over a handful of hand-picked worlds.")
print()
CANDIDATE = sorted(WORLD_C | {(u, u) for u in PEOPLE})
holds = fails = 0
counter = None
for mask in range(1 << len(CANDIDATE)):
    edges = {CANDIDATE[i] for i in range(len(CANDIDATE)) if (mask >> i) & 1}
    if plain_witnesses(edges) is None:
        continue                       # requirement does not hold; nothing to say
    if len(greedy_witnesses(PEOPLE, edges)) == len(PEOPLE):
        holds += 1
    else:
        fails += 1
        if counter is None:
            counter = edges
print(f"    candidate edges            : {CANDIDATE}")
print(f"    relations searched         : {1 << len(CANDIDATE)}")
print(f"    where the requirement holds: {holds + fails}")
print(f"    ... and greedy succeeds    : {holds}")
print(f"    ... and greedy fails       : {fails}")
print(f"    smallest failing relation  : {sorted(counter)}")
print()
print(f"  The property fails on {fails} of the {holds + fails} relations that")
print("  satisfy the requirement. A developer who wrote one example instead")
print("  of this property would have shipped whichever half of it they")
print("  happened to try.")
```

Every statement above is checked by the code rather than asserted here. The
three results to carry away: the two quantifier orders are not comparable; the
requirement in (c) holds while a greedy search for it fails; and the property a
test author naturally writes for a greedy function — "the first free option in
iteration order is the right one" — is false on all four variations.

</details>

**[ ] Exercise 5 — Explain three real coverage numbers, and write the universal
claim each one does and does not discharge.** For each of the following,
(a) write it as a quantified sentence, (b) say whether it is a universal over
branches, over inputs, or something else, (c) say what would have to be true
about the code for it to be False, and (d) say what extra work would be needed
to make it a claim about behaviour rather than about shape.

1. "Line coverage is 94%."
2. "Branch coverage is 100%, and mutation score is 87%."
3. "Property-based tests pass on 1,000 generated inputs per property."

<details>
<summary>Solution</summary>

```python
METRICS = [
    ("line coverage 94%",
     "for all lines L, exists a test T with T executing L",
     "a line nothing reaches: dead code, or a bug that killed the path",
     "none. The 6% is about which instructions ran, not whether they were right."),
    ("branch coverage 100%, mutation score 87%",
     "for all branches B, exists T reaching B;  for all mutants M, exists T in "
     "the suite that kills M",
     "an unreached branch; a mutant no test distinguishes from the original",
     "closer, but still no. Mutation score measures the suite's SENSITIVITY, "
     "not the code's CORRECTNESS. A suite that kills every mutant of a "
     "function with the wrong spec scores 100%."),
    ("property tests, 1000 generated inputs per property",
     "for all properties P, for all seeds i in 1..1000: assert P(generate(P, i))",
     "one seed whose generated value breaks P; the framework reports and "
     "shrinks it, which is the whole value",
     "much closer, and this is the claim worth making. The property IS a "
     "spec. What is still missing is the universal over inputs, and the "
     "guarantee that the generator's support IS the domain."),
]

for name, sentence, falsifier, behaviour in METRICS:
    print("=" * 76)
    print(name)
    print("=" * 76)
    print()
    print(f"  as a sentence: {sentence}")
    print()
    print(f"  what makes it False: {falsifier}")
    print()
    print(f"  a statement about behaviour? {behaviour}")
    print()

print("=" * 76)
print("the honest summary, all five in one place")
print("=" * 76)
print()
for row in [
    ("line coverage", "universal over lines", "existential over tests"),
    ("branch coverage", "universal over branches", "existential over tests"),
    ("mutation score", "universal over mutants", "existential over tests"),
    ("property testing", "universal over a finite generated slice", "no oracle gap"),
    ("what you want", "universal over ALL inputs", "with an oracle"),
]:
    print(f"  {row[0]:<18} {row[1]:<40} {row[2]}")
print()
print("Four of the five are about the relationship between code and tests.")
print("Only the last is about code and behaviour. That is not a criticism of")
print("the first four -- they are cheap and they do catch real defects. It is")
print("a statement about which claim each one is entitled to make.")
```

The line to remember is the last row. Every tool in the list is answering
"does my suite reach this?" and the question you need answered is "does my
program do the right thing?". Converting the first into the second requires an
oracle, and an oracle is a specification. There is no metric that supplies one.

</details>

**[ ] Exercise 6 — Write the quantifier structure of three specifications you
own, and translate each into the code that would be wrong.** Pick three
requirements from code you have written: an access check, a validation rule, and
a loop's termination condition. (a) Write each as a quantified statement. (b)
Write the code as it would plausibly be written under time pressure. (c) Find
the counterexample by enumeration. (d) Rewrite the code correctly. (e) For each,
state the *word* that did the damage — "and" for "or", a swapped quantifier, an
unstated domain — and say how a reviewer would catch it.

<details>
<summary>Solution</summary>

A worked model answer for a common set of three, using the same machinery.

```python
CONFIG_VALUES = [0, 1, 5, -3, 2.5, True, "7"]
ITEMS = [("a", "ok"), ("b", "partial"), ("c", "ok"), ("d", "skipped"),
         ("e", "failed")]


def requirement_1(v):
    """for all v in config: isinstance(v, int) and v > 0"""
    return isinstance(v, int) and v > 0


def requirement_1_strict(v):
    """The same with the domain tightened. `bool` subclasses `int` in Python,
    so True is accepted by the first version and is not a positive integer."""
    return isinstance(v, int) and not isinstance(v, bool) and v > 0


def code_1(v):
    """What gets written: `if v:` as a proxy for 'positive'."""
    return bool(v)


print("=" * 78)
print("1. 'every config value is a positive integer'")
print("=" * 78)
print()
print(f"{'value':>8} {'requirement':>12} {'strict':>8} {'if v:':>7}  verdict")
for v in CONFIG_VALUES:
    req, strict, code = requirement_1(v), requirement_1_strict(v), code_1(v)
    note = "ok" if req == code else "WRONG"
    if strict != req:
        note += " (domain leak)"
    print(f"{repr(v):>8} {str(req):>12} {str(strict):>8} {str(code):>7}  {note}")
print()
print("  correct code:")
print("      if not isinstance(v, int) or isinstance(v, bool) or v <= 0:")
print("          raise ConfigError(f'expected positive int, got {v!r}')")
print()

print("=" * 78)
print("2. 'every item is either skipped or fully processed'")
print("=" * 78)
print()
ALLOWED = {"ok", "skipped"}


def requirement_2(status):
    return status in ALLOWED


def code_2(status):
    """What gets written: `if status != 'partial'` as the failure test."""
    return status != "partial"


print(f"{'item':>6} {'status':>10} {'requirement':>12} {'!= partial':>11}  verdict")
for name, status in ITEMS:
    req, code = requirement_2(status), code_2(status)
    print(f"{name:>6} {status:>10} {str(req):>12} {str(code):>11}  "
          f"{'ok' if req == code else 'WRONG'}")
print()
print("  correct code:")
print("      OK = {'ok', 'skipped'}")
print("      bad = [i for i in batch if i.status not in OK]")
print()

print("=" * 78)
print("3. 'the loop terminates when no work remains'")
print("=" * 78)
print()
print("  as a statement : exists n >= 0 such that after n iterations the work")
print("                  set is empty. Equivalently: it strictly shrinks on")
print("                  every iteration that does not finish it.")
print()
print("  what gets written:")
print("      while work:")
print("          handle(work.pop() if work else None)")
print()
print("  correct code, with the shrink in one visible place:")
print("      def drain(work):")
print("          steps = 0")
print("          while work:")
print("              item = work.pop()   # the shrink is HERE")
print("              handle(item)")
print("              steps += 1")
print("          return steps")
print()
print("  and the property to test, which is the negation pushed in:")
print("      def drain_is_correct(work):")
print("          # exists n: work is empty after n pops. Proven by induction")
print("          # in Lesson 14; asserted here as a one-line smoke test.")
print("          return drain(list(work)) == len(work)")
```

**What the three have in common.** The damaging moves are, in order: using an
existential test (`if v:`, which asks whether *something* is there) for a
universal claim; using a one-element denylist for a universal over an allow-list;
and, in the third case, simply never stating the claim at all — the shrink lives
on a different line in a different function, so a reviewer cannot see it and
neither can a type checker.

The first two are caught by a four-row table. The third is caught only by asking
for the loop invariant, which is [Lesson 14](../part01_logic_proof/14_mathematical_induction.md).

</details>

**Challenge — Build a first-order logic parser, evaluator, and negation
normaliser, and use it to find a real bug.** Write a recursive-descent parser
for a small first-order language with grammar (loosest binding first):
`stmt := 'not' stmt | quant stmt | '(' stmt ')' | binop`,
`quant := ('forall' | 'exists') NAME '.' stmt`, `binop := '&' stmt | '|' stmt |
'->' stmt`. Then (a) parse a dozen statements; (b) decide each against a small
finite domain with unary and binary predicates; (c) push all negations to the
atoms and check that the normalised negation has the opposite truth value on
every statement; (d) count the quantifiers in each; and (e) use the whole
machinery on a permission system: model roles, resources and grants, express
"no user can read a resource they do not own unless they are an admin", find a
model in which the code's check is wrong, and print the counterexample as a
concrete grant table.

<details>
<summary>Solution</summary>

```python
# ---------------------------------------------------------------------------
# A first-order logic toolkit: parse, evaluate, normalise, count.
#
# The point of building it is not the language. The point is that once the
# rules are CODE, "I negated a quantified statement correctly" stops being a
# thing you believe and becomes a thing you checked.
# ---------------------------------------------------------------------------

UNARY = {"admin": {"root", "ada"}, "active": {"ada", "bob"}}
RELATION = {
    "owns": {("ada", "db"), ("bob", "logs")},
    "granted": {("bob", "db")},          # the bug: bob can read the database
}
USERS = ["ada", "bob", "root", "cy"]
RESOURCES = ["db", "logs"]

# The domain is the UNION. The specification says `for all u, for all v:
# granted(u, v) -> ...`, and it quantifies over BOTH users and resources, so
# both kinds of value have to be in range. Leaving `db` out makes
# `granted(u, v)` false for every v, which makes the implication vacuously
# true, which makes the whole specification vacuously true. An unstated domain
# is not a formality: it can silently delete your bug.
DOMAIN = USERS + RESOURCES


# ------------------------------- parsing -----------------------------------

def tokenize(text):
    out, i = [], 0
    while i < len(text):
        ch = text[i]
        if ch.isspace():
            i += 1
        elif ch.isalpha() or ch == "_":
            j = i
            while j < len(text) and (text[j].isalnum() or text[j] == "_"):
                j += 1
            out.append(("NAME", text[i:j]))
            i = j
        elif text[i:i + 2] == "->":
            out.append(("IMPL", "->"))
            i += 2
        elif ch in "&|().!,":
            out.append((ch, ch))
            i += 1
        else:
            raise ValueError(f"unexpected character {ch!r} at {i}")
    return out


class Parser:
    """One method per grammar rule. The grammar is the lesson's; the code is
    bookkeeping."""

    def __init__(self, text):
        self.tokens = tokenize(text)
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def take(self, expected=None):
        kind, value = self.peek()
        if expected is not None and kind != expected:
            raise ValueError(f"expected {expected!r}, got {kind!r}")
        self.pos += 1
        return value

    def parse(self):
        s = self.stmt()
        if self.pos != len(self.tokens):
            raise ValueError("trailing tokens")
        return s

    def stmt(self):
        kind, value = self.peek()
        if kind == "NAME" and value == "not":
            self.take()
            return ("not", self.stmt())
        if kind == "NAME" and value in ("forall", "exists"):
            self.take()
            var = self.take("NAME")
            self.take(".")
            return (value, var, self.stmt())
        if kind == "(":
            self.take("(")
            inner = self.stmt()
            self.take(")")
            return inner
        return self.binop()

    def binop(self):
        left = self.atom()
        kind, _ = self.peek()
        if kind == "&":
            self.take()
            return ("and", left, self.binop())
        if kind == "|":
            self.take()
            return ("or", left, self.binop())
        if kind == "IMPL":
            self.take()
            return ("impl", left, self.binop())
        return left

    def atom(self):
        kind, value = self.peek()
        if kind == "(":
            self.take("(")
            inner = self.stmt()
            self.take(")")
            return inner
        self.take()
        if kind == "!":
            return ("not", self.atom())
        if kind != "NAME":
            raise ValueError(f"expected a name, got {kind!r}")
        if self.peek()[0] == "(":
            self.take("(")
            args = [self.take("NAME")]
            while self.peek()[0] == ",":
                self.take(",")
                args.append(self.take("NAME"))
            self.take(")")
            if len(args) == 1:
                return ("pred", value, args[0])
            return ("rel", value, args[0], args[1])
        return ("eq", value)


# ----------------------------- normalisation -------------------------------

def nnf(s, negated=False):
    """Negation normal form: `not` only over atoms. `negated` is the polarity."""
    kind = s[0]
    if kind == "not":
        return nnf(s[1], not negated)
    if kind in ("forall", "exists"):
        # A quantifier FLIPS when the polarity is negative, and the polarity
        # then carries into the body unchanged. This is the whole rule.
        flipped = {"forall": "exists", "exists": "forall"}[kind]
        return (flipped if negated else kind, s[1], nnf(s[2], negated))
    if kind == "and":
        if negated:
            return ("or", nnf(s[1], True), nnf(s[2], True))
        return ("and", nnf(s[1], False), nnf(s[2], False))
    if kind == "or":
        if negated:
            return ("and", nnf(s[1], True), nnf(s[2], True))
        return ("or", nnf(s[1], False), nnf(s[2], False))
    if kind == "impl":
        # p -> q is ~p | q;  ~(p -> q) is p & ~q
        if negated:
            return ("and", nnf(s[1], False), nnf(s[2], True))
        return ("or", nnf(s[1], True), nnf(s[2], False))
    if kind in ("pred", "rel", "eq"):
        return ("not", s) if negated else s
    raise ValueError(kind)


def count_quantifiers(s):
    if s[0] in ("forall", "exists"):
        return 1 + count_quantifiers(s[2])
    if s[0] == "not":
        return count_quantifiers(s[1])
    if s[0] in ("and", "or", "impl"):
        return count_quantifiers(s[1]) + count_quantifiers(s[2])
    return 0                     # an atom: pred, rel, eq. No quantifier inside.


def free_vars(s, bound=frozenset()):
    kind = s[0]
    if kind in ("forall", "exists"):
        return free_vars(s[2], bound | {s[1]})
    if kind == "not":
        return free_vars(s[1], bound)
    if kind in ("and", "or", "impl"):
        return free_vars(s[1], bound) | free_vars(s[2], bound)
    if kind == "pred":
        return set() if s[2] in bound else {s[2]}
    if kind == "rel":
        return {v for v in (s[2], s[3]) if v not in bound}
    return set()


# ------------------------------ evaluation ---------------------------------

def truth(s, env):
    kind = s[0]
    if kind == "not":
        return not truth(s[1], env)
    if kind == "pred":
        return env[s[2]] in UNARY[s[1]]
    if kind == "rel":
        return (env[s[2]], env[s[3]]) in RELATION[s[1]]
    if kind == "eq":
        return True            # a bare identifier in argument position
    if kind == "impl":
        return (not truth(s[1], env)) or truth(s[2], env)
    if kind == "and":
        return truth(s[1], env) and truth(s[2], env)
    if kind == "or":
        return truth(s[1], env) or truth(s[2], env)
    if kind == "forall":
        return all(truth(s[2], {**env, s[1]: v}) for v in DOMAIN)
    if kind == "exists":
        return any(truth(s[2], {**env, s[1]: v}) for v in DOMAIN)
    raise ValueError(kind)


def find_counterexample(s, env=None):
    """Refute a `forall` by finding one value. Returns None if none exists --
    and for a two-quantifier statement None is not the same as 'no problem'."""
    env = env or {}
    if s[0] == "forall":
        for v in DOMAIN:
            if not truth(s[2], {**env, s[1]: v}):
                return v
        return None
    if s[0] == "not":
        return find_counterexample(s[1], env)
    if s[0] == "and":
        return find_counterexample(s[1], env) or find_counterexample(s[2], env)
    return None


def find_pair_counterexample(s):
    """The same job for `forall u. forall v. S(u, v)`: search all of D x D.

    A one-variable finder cannot refute this statement. It binds `u` and then
    checks the body, and the body is a universal over `v` that happens to hold
    for every individual `u` -- including the offender. The two values have to
    be chosen together, so the search space is the product.
    """
    _, u_var, body = s
    _, v_var, core = body
    for u in DOMAIN:
        for v in DOMAIN:
            if not truth(core, {u_var: u, v_var: v}):
                return (u, v)
    return None


# ------------------------------- the tests ---------------------------------

STATEMENTS = [
    "forall u. admin(u)",
    "exists u. admin(u)",
    "not forall u. active(u)",
    "not exists u. admin(u)",
    "forall u. active(u) | admin(u)",
    "not forall u. active(u) | admin(u)",
    "forall u. active(u) -> admin(u)",
    "not forall u. active(u) -> admin(u)",
    "forall u. exists v. owns(u, v)",
    "not forall u. exists v. owns(u, v)",
    "exists v. forall u. granted(u, v)",
    "not exists v. forall u. granted(u, v)",
]

print("=" * 84)
print("(a)-(d) parse, decide, normalise, count")
print("=" * 84)
print()
print(f"{'#':>2} {'statement':<42} {'|Q|':>4} {'S':>6} {'~S (nnf)':>10} "
      f"{'agree':>6}  free vars")
ok = True
for i, text in enumerate(STATEMENTS, 1):
    s = Parser(text).parse()
    n = nnf(s, negated=True)
    t, nt = truth(s, {}), truth(n, {})
    ok = ok and (t != nt)
    print(f"{i:>2} {text:<42} {count_quantifiers(s):>4} {str(t):>6} {str(nt):>10} "
          f"{str(t != nt):>6}  {sorted(free_vars(s))}")
print()
print(f"all 12 normalise correctly and disagree with their negation: {ok}")
print()

SPEC = Parser("forall u. forall v. granted(u, v) -> (admin(u) | owns(u, v))").parse()
print("=" * 84)
print("(e) the permission system")
print("=" * 84)
print()
print("  specification: for all u, for all v: granted(u, v) -> (admin(u) or owns(u, v))")
print("  in words     : nobody can read a resource they do not own, unless admin")
print()
print(f"  the grants table: {sorted(RELATION['granted'])}")
print(f"  the owners table: {sorted(RELATION['owns'])}")
print()
print(f"  the spec holds                : {truth(SPEC, {})}")
print(f"  one-variable search returns   : {find_counterexample(SPEC)}")
print(f"  two-variable search returns   : {find_pair_counterexample(SPEC)}")
_saved = DOMAIN
DOMAIN = USERS
print(f"  the spec, DOMAIN = USERS only : {truth(SPEC, {})}   <- vacuously true")
DOMAIN = _saved
print()
print(f"{'user':>6} {'resource':>10} {'admin?':>7} {'owner?':>7} {'permitted?':>11}")
for u, v in sorted(RELATION["granted"]):
    print(f"{u:>6} {v:>10} {str(u in UNARY['admin']):>7} "
          f"{str((u, v) in RELATION['owns']):>7} "
          f"{str(u in UNARY['admin'] or (u, v) in RELATION['owns']):>11}")
```

Three results are worth reading twice.

**The one-variable search returns `'bob'`; the two-variable search returns
`('bob', 'db')`.** Both are correct and neither is enough on its own. `bob` is a
suspicious user who in a real system holds three grants, so the search has
narrowed the space without identifying a row to revoke. The pair is actionable.
The difference is structural: the negation of `∀u ∀v` is `∃u ∃v` over the
*product*, so a refutation procedure has to search the product.

**The same specification evaluates to `True` when the domain omits the
resources.** `granted(u, v)` is then false for every `v`, the implication is
vacuously true, and the bug vanishes — same parser, same data, one value missing
from the range. That is not a logic exercise; it is the most common way a
permission model gets written wrong.

**Every `free vars` entry is empty.** That is the only reason these twelve
sentences are propositions rather than predicates, and a non-empty list is the
warning sign that a quantifier is missing.

</details>

## Summary

- A predicate is a formula with a free variable and no truth value; a closed
  sentence is a proposition. The domain is part of the statement, not part of
  the notation.
- `∀` and `∃` are the two ways of turning per-element answers into one answer.
  `∀` is refuted by one counterexample; `∃` is confirmed by one witness.
- Negating a quantified statement flips the quantifier **and** negates the body.
  `¬∀x P(x) ≡ ∃x ¬P(x)` and `¬∃x P(x) ≡ ∀x ¬P(x)`, plus De Morgan on compound
  bodies.
- `¬∃!x P(x)` needs two variables over the same domain, with `x ≠ y`. A naive
  single-variable negation reports every duplicate as absent.
- Nested quantifier order is part of the meaning. `∀x ∃y` is a matching and the
  witness may depend on `x`; `∃y ∀x` demands one universal witness and is much
  stronger.
- `k` quantifiers over a domain of size `n` cost up to `nᵏ` predicate
  evaluations, so counting quantifiers is counting loop nests.
- Over the empty domain, `∀` is vacuously true and `∃` is false. One empty
  result set supports both conclusions, so the query must say which it means.
- A SQL `WHERE` clause is a predicate and `SELECT` reports an existential.
  `NOT EXISTS` is how a universal is smuggled in, and `NOT IN` on a `NULL`
  silently returns nothing.
- Type signatures are universals over types; a test suite is a finite list of
  existentials; 100% branch coverage is `∀ branch, ∃ test`, not `∀ input`.

## Next

[Lesson 13 — Proof Techniques](../part01_logic_proof/13_proof_techniques.md) takes the closed sentences
this lesson produces and shows how to argue that they are true: direct proof,
contrapositive, contradiction, and exhaustion. It assumes you can write a
quantified statement and negate it correctly, which is the hard half.
