# 80 — Big-O and Complexity Analysis

**Part**: part06_algorithms_math · **Prerequisites**: 24 · **Time**: 45 min

---

## In Plain Words

When people say one algorithm is faster than another, they almost never mean
faster on the input in front of them. They mean that as the input gets bigger,
the first one pulls further and further ahead — and the discipline of saying
exactly how much further, and proving it, is what complexity analysis is. The
main tool is a shorthand for "grows no faster than some reference rate", and the
most common mistake is using it so loosely that the answer carries no
information: a linear algorithm is also a quadratic one, as a matter of logic,
so "it is O of n squared" tells you nothing unless you also say it is not
anything worse.

Two things make this harder than it looks. The first is that a real program does
not only run loops; it adds numbers together, multiplies them, and stores them,
and those things cost something too. If the numbers being added are enormous,
"one addition" is not one unit of work, and an analysis that counts loop
iterations instead of real work will confidently call two thousand-digit
arithmetic free. The second is that the cost of an operation depends entirely on
what is being asked, so every honest complexity claim has to name its cost model
out loud.

---

## Why Computer Science Cares

- **Every design review.** "Is this fast enough?" is answered by a bound, not a
  stopwatch. `O(n log n)` versus `O(n^2)` at $n = 10^6$ is 20 operations against
  10^12 — the difference between a service and an outage. CLRS is the reference
  and it is still the right book.
- **Database query planning.** PostgreSQL's and MySQL's optimisers carry
  estimates of rows produced, distinct-value counts and index selectivity, and
  they use them to pick between a nested-loop join ($\Theta(nm)$), a hash join
  ($\Theta(n + m)$) and a merge join ($\Theta(n\log n)$). When an index is
  missing, the plan degrades to the quadratic one and the query that took 8
  milliseconds takes 40 minutes. `EXPLAIN ANALYZE` is showing you the bounds.
- **Hash tables, and why Python made you use a different one.** A hash map
  insertion is expected $O(1)$ but worst case $O(n)$, because all $n$ keys can
  land in one bucket. `tuple` is immutable and hashes by value, so using it as a
  dictionary key is $O(n)$ in the *key's* length — `id()`, or a `__hash__` you
  write, or a hashable wrapper, is the fix. This is a bit-complexity argument
  in production code.
- **The FFT, which is Lesson 55.** The naive discrete transform is exactly
  $N^2$ complex multiplications — 1,099,511,627,776 at $N = 2^{20}$ — and Cooley
  and Tukey's rearrangement is exactly $\frac{N}{2}\log_2 N$, or 10,485,760 at
  the same size. Every fast transform in every library descends from that one
  observation about an asymptotic bound.
- **Dynamic arrays.** Python's `list`, Java's `ArrayList`, C++'s `std::vector` all
  grow by doubling, which turns $n$ appends from $\Theta(n^2)$ into
  $\Theta(n)$ amortised. Java's `ArrayList.grow` and Rust's `Vec::push` are one
  line each, and the entire reason is a complexity argument.
- **Big-integer libraries, cryptography, and compression.** RSA key generation,
  `gmpy2`, `libcrypto`, `zlib`, `bzip2`: all of them are careful about bit
  complexity, because an algorithm that is $\Theta(n)$ *operations* on $n$-bit
  numbers is $\Theta(n^2)$ *bit operations*, and for a 4096-bit RSA modulus that
  is a factor of 4096 nobody had budgeted for.
- **String concatenation in the wrong loop.** `s = s + x` in a loop is
  $\Theta(n^2)$ in element copies; `s += x` for a list is the same trap with
  better ergonomics. It is in a great deal of real Python, and it is the single
  most common false complexity claim you will meet.
- **Interview answers that are checkable.** "What is the time complexity?" has a
  wrong answer that is *technically* true — $O(n^2)$ for a linear scan — and the
  whole discipline exists to stop that from counting as an answer.

---

## The Formal Version

Throughout, $f$ and $g$ are functions from $\mathbb{N}$ to $\mathbb{R}_{\ge 0}$
measuring cost, $n_0$ is a threshold in $\mathbb{N}$, and $c, c_1, c_2,
\varepsilon$ are positive constants. "As $n \to \infty$" is always implied. See
[SYMBOLS.md](../SYMBOLS.md) and [Lesson 24](../part02_discrete_combinatorics/24_recurrence_relations.md).

**Definition.** $f = O(g)$, read "$f$ is big-O of $g$", if there exist
constants $c > 0$ and $n_0$ such that

$$f(n) \le c\,g(n)\quad\text{for all } n \ge n_0.$$

$f(n)/g(n)$ is **bounded above** eventually.

*Explanation.* The constant $c$ and the threshold $n_0$ are both allowed to be
enormous, and that is the entire freedom the notation grants. It is a
one-sided statement: nothing is claimed about how much smaller $f$ is than $g$,
only that it is not bigger. This is why $O$ is a poor *ranking* tool and a good
*certification* tool: it tells you a program will not surprise you, and tells you
nothing about how fast it is.

**Definition.** $f = \Omega(g)$ if there exist $c > 0$ and $n_0$ with

$$f(n) \ge c\,g(n)\quad\text{for all } n \ge n_0.$$

$f(n)/g(n)$ is **bounded below** away from zero eventually.

*Explanation.* The mirror image. In algorithms, an $\Omega$ bound is a *lower
bound* and it is the hard half: showing that an algorithm is $O(n\log n)$ is
routine, and showing that nothing can do better is the actual content of
"merge sort is optimal". Lower bounds are proved adversarially — exhibit an
input for which any algorithm must do the work.

**Definition.** $f = \Theta(g)$ if both hold, with their own constants:

$$0 < c_1 \le \frac{f(n)}{g(n)} \le c_2 \quad\text{for all } n \ge n_0.$$

Equivalently, $f = O(g)$ **and** $f = \Omega(g)$.

*Explanation.* The ratio is trapped between two positive constants forever, which
means $f$ and $g$ grow at the *same rate* and differ only by a multiplicative
factor. This is the only member of the family that pins down the answer, and it
is what "the complexity is $\Theta(n\log n)$" is supposed to mean. The lesson's
own counts make the difference visible: a linear loop's count divided by $n^2$
is `0.499992` at $n = 65536$ and falling, so it is $O(n^2)$ but *not*
$\Theta(n^2)$; divided by $n$ it is exactly $1$, so it is $\Theta(n)$.

**Definition.** $f = o(g)$ if for **every** $c > 0$ there is an $n_0$ with

$$f(n) \le c\,g(n)\quad\text{for all } n \ge n_0,$$

i.e. $f(n)/g(n) \to 0$.

**Definition.** $f = \omega(g)$ if for every $c > 0$ there is an $n_0$ with
$f(n) \ge c\,g(n)$ for $n \ge n_0$, i.e. $f(n)/g(n) \to \infty$.

*Explanation.* The universal quantifier over $c$ is what separates $o$ from
$O$. Compare $f = n^2$ against $g = n^2$: $f = O(g)$ with $c = 1$, but
$f \not= o(g)$ because $f/g = 1$ never gets below $c = 1/2$. Now compare
$f = n$ against the same $g$: for every $c > 0$ there is an $n_0 = 1/c$ with
$n \le cn^2$, so $f = o(g)$. **Strictly faster**, and the strictness is
unbounded.

**Definition.** $\log = O(1)$ is false and $\log = o(1)$ is false; the useful
statement is that $1, \log n, \log\log n$ are all $o(n)$, and that is why a
logarithmic scan beats a linear one no matter how large the constant on the
linear scan is.

**Theorem (the hierarchy).** For $g(n) = n^d$ with $d > 1$:

$$o(n^{d-\varepsilon}) \;=\; \Theta(n^d) \;=\; \omega(n^{d+\varepsilon})
\quad\text{for every } \varepsilon > 0.$$

*Explanation.* Powers of $n$ are totally ordered by growth, and no amount of
reshuffling inside $O$ or $\omega$ changes that. The important corollary is that
$O$, $\Theta$ and $o$ are three different answers, not three ways of saying the
same thing: $n^2$ is $O(n^2)$, is $\Theta(n^2)$, and is $\omega(n^{1.5})$.

**Theorem (transitivity and the hierarchy of classes).** If $f = O(g)$ and
$g = O(h)$ then $f = O(h)$, by composing the two constants. If
$f = \Theta(g)$ and $g = \Theta(h)$ then $f = \Theta(h)$. If $f = o(g)$ and
$g = o(h)$ then $f = o(h)$.

*Explanation.* Transitivity is why $O(n^2)$ is a legal bound for a linear
algorithm: $n = O(n^2)$ because $n \le cn^2$ for $c = 1$ and $n \ge 1$. This is
also the formal statement of the vacuousness that
[Common Mistake 1](#common-mistakes) is about.

**Definition (the cost model).** A complexity claim is a triple
$(\text{algorithm}, \text{cost measure}, \text{input size})$: which operations
count as one unit, and what $n$ means. The standard models are

| model | one unit of cost | $n$ | realistic for |
| --- | --- | --- | --- |
| unit-cost RAM | one machine-word operation | number of items | fixed-width ints, arrays, pointers |
| bit complexity | one single-bit operation | **number of bits** | Python `int`, bignums, exact rationals, symbolic |
| bit complexity (with real RAM) | one word op **or** $\lceil b/w\rceil$ | items and bits | Karatsuba multiply, FFT multiply |
| comparison model | one comparison | number of items | sorting, searching, decision trees |
| algebraic/word RAM | one arithmetic op on $\log n$-bit words | items | fast matrix multiply, Strassen |

*Explanation.* Every $O$ in this lesson and every $O$ you have ever read is
silent about which row it is in. That silence is harmless for "binary search is
$\Theta(\log n)$" — a comparison model result — and catastrophic for "arithmetic
is $O(1)$", which is true in row 1 and false in rows 2 and 3. Stating the model
is not pedantry; a bound without one is not a proposition.

**Theorem (bit complexity of the basic operations).** For $n$-bit integers:

| operation | schoolbook model | measured in CPython |
| --- | --- | --- |
| add / subtract | $\Theta(n)$ | $\Theta(n)$, `add/k` flat at `0.068` ns at $k = 2^{18}$ |
| compare | $\Theta(n)$ worst case | $\Theta(n)$, `0.089` ns per bit at $k = 2^{24}$ |
| multiply | $\Theta(n^2)$ | $\Theta(n^{1.585})$, Karatsuba's $\log_2 3$ |
| divide | $\Theta(n^2)$ | $\Theta(n^2)$ |
| decimal conversion | $\Theta(d^2)$, $d$ digits | subquadratic, working in $10^9$-limbs |
| space to store | $\Theta(n)$ bits | `sys.getsizeof` grows 8 bytes per 8 bits |

*Explanation.* Note that the *exponent itself* is implementation-defined, which
is the sharpest possible demonstration that a bound without a model is not a
statement. The lesson measures a doubling exponent of 1.50 to 1.78 for squaring
$k$-bit integers and never near 2.0.

**Theorem (the two bounds that matter for $T(n) = aT(n/b) + \Theta(n^d)$).** Let
$T(n)$ count basic operations, $a \ge 1$, $b > 1$, $d \ge 0$, and $n = b^k$. The
recursion tree has $a^j$ nodes at level $j$, each of size $n/b^j$, so level $j$
costs $a^j(n/b^j)^d = (a/b^d)^j n^d$. Hence

$$T(n) = \begin{cases}
\Theta(n^{d}) & a < b^{d}\\[2pt]
\Theta(n^{d}\log n) & a = b^{d}\\[2pt]
\Theta(n^{\log_b a}) & a > b^{d}
\end{cases}$$

*Explanation.* The whole theorem is the observation that the level costs form a
**geometric series** in $j$ with ratio $a/b^d$. If the ratio is below 1 the sum
converges to its first term ($O(n^d)$); if it is 1 the sum is
$n^d \cdot k$ ($\Theta(n^d\log n)$); if above 1 the last term dominates and
there are $k = \log_b n$ levels, giving $a^k = n^{\log_b a}$. The full treatment
is in [Lesson 24](../part02_discrete_combinatorics/24_recurrence_relations.md);
the lesson's code executes the sum rather than asserting it.

**Definition (amortised, average and worst case are three different things).**
Fix a probability distribution $\mathcal{D}$ over inputs of size $n$.

- **worst case**: $\max_{x \in \mathcal{I}_n} T(x)$, over *all* inputs of size $n$;
- **average case**: $\mathbb{E}_{x \sim \mathcal{D}}[T(x)]$, over one *chosen*
  distribution;
- **amortised**: $\frac{1}{n}\sum_{i=1}^{n} T(x_i)$ for an arbitrary *sequence*
  of operations, with no distribution at all.

*Explanation.* The average case is a statement about a random world and it
requires you to name the distribution; hash tables are expected $O(1)$ only
because Python randomises the seed, and an adversary who learns the seed breaks
it. The amortised case makes **no probabilistic assumption whatsoever** — it is a
statement about the total cost of any sequence of $n$ operations, worst case
over the sequence. That it is strictly weaker than a per-operation worst case,
and why it is not in conflict with one, is
[Lesson 81](81_amortized_analysis.md).

**Theorem (the forward/central difference rates, and why the step is not
arbitrary).** For $f$ with $f'$ Lipschitz with constant $L$ and $f'''$ bounded by
$M$ on the interval,

$$\left|\frac{f(x+h)-f(x)}{h}-f'(x)\right| \le \tfrac12 L h + O(\epsilon/h),
\qquad
\left|\frac{f(x+h)-f(x-h)}{2h}-f'(x)\right| \le \tfrac16 M h^2 + O(\epsilon/h).$$

*Explanation.* Both are $\Theta(1)$ in *operations*, so both are $O(1)$ — and
that is why the letter $O$ cannot choose between them. The difference is
$\Theta(h)$ against $\Theta(h^2)$, a constant factor in accuracy that the
notation deliberately discards. And the $\epsilon/h$ term is why "use a smaller
$h$" is wrong: the total error turns back up once rounding dominates. The
measured optima in the code are $h = 10^{-8}$ forward and $h = 10^{-5}$ central,
against the predictions $\sqrt{\epsilon/L}$ and $(3\epsilon/M)^{1/3}$.

---

## Formula Sheet

`$f, g$` are cost functions, `$c, c_1, c_2, \varepsilon > 0$` are constants,
`$n_0$` is a threshold, `$k = \log_b n$` is the depth of a recursion tree, `$a$`
the branching factor, `$b$` the shrink factor, `$d$` the degree of the top-level
work, `$\varepsilon \approx 2.22\times10^{-16}$` the double-precision unit
roundoff, and `$b$` in the bit-complexity rows is the *bit length* (context
distinguishes it from the shrink factor).

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$f = O(g)$` | `$\exists c>0,\ n_0:\ f(n)\le c\,g(n)$ for `$n\ge n_0$` | grows no faster than `$g$`, up to a constant | an **upper** bound: "it will not surprise you". **not** a ranking — see the next row |
| `$f = \Omega(g)$` | `$\exists c>0,\ n_0:\ f(n)\ge c\,g(n)$ for `$n\ge n_0$` | grows no slower than `$g$` | a **lower** bound: "nothing can beat this". Needs an adversarial argument, not a loop count |
| `$f = \Theta(g)$` | `$0<c_1\le f(n)/g(n)\le c_2$ for `$n\ge n_0$` | same rate as `$g$`, up to a constant factor | the only tight answer. Use this unless you have a reason not to |
| `$f = o(g)$` | `$\forall c>0\ \exists n_0:\ f(n)\le c\,g(n)$ for `$n\ge n_0$`, i.e. `$f/g\to0$` | **strictly** faster; the gap grows without bound | separating two candidates both of which are `$O$` of something bigger. The `$n_0` **depends on `$c$`** |
| `$f = \omega(g)$` | `$\forall c>0\ \exists n_0:\ f(n)\ge c\,g(n)$, i.e. `$f/g\to\infty$` | **strictly** slower | ditto. `$\log n = \omega(1)$`, `$\log n = o(n)$`, `$\log n = \Theta(n)$` all hold |
| `"$f$ is $O(g)$ but not $o(g)$"` | `$0 < \liminf f/g < \limsup f/g < \infty$` fails only in the lower limit | same order, different constant | this is the difference between `$\Theta$` and `$O$`; a **linear scan is `$O(n^2)$ and not `$o(n^2)$`** |
| power hierarchy | `$\log n,\ \log\log n = o(n)$`; `$n\log n,\ n^{1.5}, n^2 = \omega(n)$` | logs are sublinear; any higher power is superlinear | sanity-checking a claimed bound before you try to prove it |
| trivial $O$ | `$f = O(g)$ for every `$g$` with `$f=\Theta(g)$` | an upper bound that admits a smaller one says nothing | a bound is only informative together with the claim that it is **tight** |
| worst case | `$\max_{x\in\mathcal I_n} T(x)$` | the most expensive input of size `$n$` | the default for algorithm analysis; what an adversary will find |
| average case | `$\mathbb E_{x\sim\mathcal D}[T(x)]$` | the mean over **one named** distribution `$\mathcal D$` | only with the distribution stated; hash tables are expected `$O(1)$` only under a random seed |
| amortised | `$\frac1n\sum_{i=1}^n T(x_i)$`, worst case over the sequence | average per operation with **no** distribution assumed | dynamic arrays, and [Lesson 81](81_amortized_analysis.md) in full |
| recursion tree | level `$j$` costs `$a^j(n/b^j)^d = (a/b^d)^j n^d$` | `$a^j$` nodes each doing `$(n/b^j)^d$` | the master theorem, proved |
| master case 1 | `$a<b^d \Rightarrow \Theta(n^d)$` | the top level dominates | `3T(n/2)+n^3`: `8>3`, so `$\Theta(n^3)$` |
| master case 2 | `$a=b^d \Rightarrow \Theta(n^d\log n)$` | every level costs the same | `2T(n/2)+n`: merge sort, `$\Theta(n\log n)$` |
| master case 3 | `$a>b^d \Rightarrow \Theta(n^{\log_b a})$` | the leaves dominate | `4T(n/2)+n`: `$\Theta(n^2)$`; `3T(n/2)+n`: `$\Theta(n^{1.585})$` |
| closed form, case 3 | `$\frac{a^{k+1}-1}{a-1}$` for `$f(n)=1+a f(n/b)$ | a geometric sum | `$3T(n/2)$` with `$k=\log_2 n$` gives `$(3^{k+1}-1)/2`; the code's ratio column is `1.00` at every size |
| unit-cost add | `$O(1)$` | a machine word | the standard model — **and the one that is silently wrong for bignums** |
| bit-cost add / compare | `$\Theta(k)$` for `$k$`-bit integers | proportional to the size of the numbers | `add/k` measured flat at `0.068` ns at `$k=2^{18}$` |
| schoolbook multiply | `$\Theta(k^2)$`, exactly `$k^2$` bit operations | one op per bit pair | what a hand-written long multiply does |
| Karatsuba multiply | `$\Theta(k^{\log_2 3}) = \Theta(k^{1.585})$` | three half-size multiplies | CPython above ~70 decimal digits; measured doubling exponent 1.50–1.78 |
| decimal conversion | `$\Theta(d^2)$`, `$d = k\log_{10}2$` digits | quadratic in the number of digits | why Python 3.11 caps `int`→`str` at 4300 digits, and why raising the cap is a DoS lever |
| space for one `$k$`-bit integer | `$\Theta(k)$ bits, `$\approx k/8$ bytes | linear in the bits | `sys.getsizeof((1<<16383)-1) = 2212 bytes`. An algorithm holding `$n$`-bit intermediates is already `$\Theta(n)$` |
| merge sort, two bounds | `(n/2)\log_2 n \le T(n) \le n\log_2 n` | each level costs between `$n/2$ and `$n$` | the lower bound needs the fact that a merge of two runs totalling `$m$` takes at least `$m/2$` comparisons |
| forward difference | `$\frac{f(x+h)-f(x)}{h}-f'(x) = \frac{h}{2}f''(\xi)+O(\epsilon/h)$` | error grows **linearly** in `$h$` | cheap gradients; measured `fwd err / h = 0.5793 = \tfrac12\lvert f''(1)\rvert` exactly |
| central difference | `$\frac{f(x+h)-f(x-h)}{2h}-f'(x) = -\frac{h^2}{6}f'''(\xi)+O(\epsilon/h)$` | error grows **quadratically** in `$h$` | two evaluations, `$\Theta(h^2)$` accuracy; measured `ctr err / h^2 = 0.0900 = \tfrac16\lvert f'''(1)\rvert` exactly |
| optimal forward step | `$h\approx\sqrt{\epsilon/L}$`; best error `$\approx\sqrt{\epsilon L}$` | `$1.5\times10^{-8}$` for `$L=1$` | measured `4.023e-09` at `$h=10^{-8}$` — do **not** use the smallest `$h$` you can |
| optimal central step | `$h\approx(3\epsilon/M)^{1/3}$`; best error `$\approx(3\epsilon M^2/4)^{1/3}$` | `$1.1\times10^{-5}$` for `$M=1$` | measured `3.590e-12` at `$h=10^{-5}$`, a factor of `1121` better than forward for 2× the calls |
| list concatenation in a loop | `$\sum_{i=1}^{n} i = n(n-1)/2$` element copies | `$\Theta(n^2)$` despite `n` iterations | `s = s + [x]` versus `s.append(x)`; the most common false bound in Python |

---

## Worked Example

Prove a tight bound for **merge sort**, by three different routes, with every
intermediate value shown. This is the worked example because it is the one
algorithm whose analysis everybody has to be able to produce.

### Setup

Merge sort on $n$ elements: split into two halves of $\lfloor n/2 \rfloor$ and
$\lceil n/2 \rceil$, sort each recursively, then merge. The merge walks both
sorted halves with one pointer each, emitting the smaller front element and
stopping when one half is empty.

**Step 1 — write the recurrence.** Counting comparisons in the merge:

$$T(n) = 2T(n/2) + M(n),$$

where $M(n)$ is the number of comparisons to merge two sorted runs of total
length $n$. So $a = 2$, $b = 2$, $d = 1$ if $M(n) = \Theta(n)$.

**Step 2 — bound the merge.** Two bounds, both tight to a constant.

*Upper:* a merge emits at most $n$ elements, and each element costs at most one
comparison, so $M(n) \le n$.
*Lower:* the merge stops when one run empties. To empty a run of length $a$ costs
at least... hmm, the wrong direction. The right statement: whichever run empties
first, say the one of length $a \le n/2$, and the merge performed at least $a$
comparisons (it compared at every step until that run was gone). If $a$ is the
shorter run then $a \ge$ ... this gives only $M(n) \ge \min(a,b)$, which is weak.
The correct lower bound: the merge makes $M(n)$ comparisons and then copies
$n - M(n)$ remaining elements. It stops as soon as one run is empty, so one run
of length $a$ is exhausted: $M(n) \ge a$. Since the run that empties first is the
shorter one, $a \le n/2$, giving $M(n) \ge a$ — still weak. The standard
argument is: the two runs have lengths $a$ and $n - a$ with $a \le n/2$ (assume
$a$ is the left run); if the left run empties first then $M(n) \ge a$; if the
right run empties first then the merge made at least $n - a$ comparisons, and
$n - a \ge n/2$. In both cases $M(n) \ge n/2$. $\blacksquare$

So $M(n) = \Theta(n)$ and therefore

$$T(n) = 2T(n/2) + \Theta(n).$$

**Step 3 — master theorem.** $a = 2$, $b = 2$, $d = 1$, and $a/b^d = 2/2 = 1$:
**case 2**. Hence

$$T(n) = \Theta(n\log n).$$

**Step 4 — the recursion tree, as a check.** Level $j$ has $2^j$ nodes of size
$n/2^j$, so level $j$ costs $2^j \cdot (n/2^j) = n$. There are
$\log_2 n$ levels, so the total is $n\log_2 n$ exactly. This is the case-2
signature: the level costs are *equal*, and the answer is (cost per level) ×
(number of levels).

**Step 5 — verify against a real implementation, with the exact counts.** Input:
`[(i * 7919) % 100003 for i in range(n)]`, sorted by the code in Exercise 3.

| $n$ | comparisons | $n\log_2 n$ | $n\log_2 n - n$ | lower bound $\frac{n}{2}\log_2 n$ |
| --- | --- | --- | --- | --- |
| 16 | 39 | 64.0 | 48.0 | 32.0 |
| 64 | 283 | 384.0 | 320.0 | 192.0 |
| 256 | 1642 | 2048.0 | 1792.0 | 1024.0 |
| 1024 | 8627 | 10240.0 | 9216.0 | 5120.0 |
| 4096 | 42714 | 49152.0 | 45056.0 | 24576.0 |

The counts sit strictly inside both bounds, as they must. The ratio
$T/(n\log_2 n)$ runs `0.609, 0.737, 0.802, 0.843, 0.869` — rising towards 1 —
and the deficit divided by $n$ reads `63.3, 1.578, 1.586, 1.575, 1.572`, so on
this input the count is $n\log_2 n - 1.575n$. That is a much better *point*
estimate than $n\log_2 n$, which is 15.1% high at $n = 4096$, or than
$n\log_2 n - n$, which over-corrects by $0.575n$ and is 5.5% high. The
$\Theta$ answer is unchanged, and that is the point: **a $\Theta$ bound can be
very wrong about the second-order term and still be exactly right.** Anyone who
wrote `n·log₂ n` as the prediction and `42714` as the measured count at
$n = 4096$ should not conclude that either is wrong.

**Step 6 — the lower bound, and why merge sort is optimal.** The recursion-tree
argument gave the upper bound. For the lower bound: any comparison sort must
distinguish the $n!$ permutations of $n$ keys, and a decision tree of depth $d$
has at most $2^d$ leaves, so $2^d \ge n!$, i.e.

$$d \ge \log_2 n! = \log_2(n(n-1)\cdots 1) = \sum_{k=1}^{n}\log_2 k \ge n\log_2 n - n\log_2 e.$$

Stirling's formula makes it $\log_2 n! = n\log_2 n - (\log_2 e)n + O(\log n)$,
so **any** comparison sort needs $\Omega(n\log n)$ comparisons, and merge sort
achieves it. Merge sort is therefore optimal *in the comparison model* — and the
phrase "in the comparison model" is doing real work, because
`sort()` on a machine word uses radix sort, which is $O(n)$ and is not a
comparison sort at all. It sorts digits, and no information about relative order
is extracted.

---

## Runnable Code

### Block 1: counting operations exactly, and O versus Θ versus o

```python
import math
import random


class Counter:
    """Counts the dominant operation.  Counting is deterministic; a clock is not."""

    def __init__(self):
        self.n = 0

    def tick(self, k=1):
        self.n += k
        return self.n


def linear_scan(a, target):
    """Early-exit linear search: O(1) best case, Theta(n) worst case."""
    c = Counter()
    for i, v in enumerate(a):
        c.tick()
        if v == target:
            return i, c.n
    return -1, c.n


def is_sorted(a):
    """Stop at the first inversion: O(1) best case, Theta(n) worst case."""
    c = Counter()
    for i in range(1, len(a)):
        c.tick()
        if a[i] < a[i - 1]:
            return False, c.n
    return True, c.n


def sum_all(a):
    c = Counter()
    t = 0
    for v in a:
        c.tick()
        t += v
    return t, c.n


def binary_search(a, target):
    """Theta(log n) comparisons in the worst case, Theta(log n) in the best."""
    c = Counter()
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        c.tick()
        mid = (lo + hi) // 2
        if a[mid] == target:
            return mid, c.n
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, c.n


def binary_search_virtual(n, target):
    """The same search on the sorted array [0, 1, ..., n-1], without allocating it.
    Comparisons depend only on n, so we can go to 2**40."""
    c = Counter()
    lo, hi = 0, n - 1
    while lo <= hi:
        c.tick()
        mid = (lo + hi) // 2
        if mid == target:
            return mid, c.n
        if mid < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, c.n


def bubble_sort(a):
    c = Counter()
    v = list(a)
    for i in range(len(v) - 1):
        swapped = False
        for j in range(len(v) - 1 - i):
            c.tick()
            if v[j] > v[j + 1]:
                v[j], v[j + 1] = v[j + 1], v[j]
                swapped = True
        if not swapped:
            break                      # early exit: the tail is already in order
    return v, c.n


print("=== Counting operations is the honest way to compare algorithms ===")
print("  Every entry below is an exact integer produced by the code, not estimated.")
print("     n    sum_all   is_sorted(almost sorted)   bubble_sort   n^2/2   n^2/n")
for n in (16, 32, 128, 512, 1024, 2048):
    random.seed(n)
    a = [random.randrange(1000) for _ in range(n)]
    almost = list(range(n))
    almost[-3], almost[-1] = almost[-1], almost[-3]   # one inversion, at the END
    _, c_sum = sum_all(a)
    _, c_almost = is_sorted(almost)
    _, c_bub = bubble_sort(a)
    print(f"  {n:>5}   {c_sum:>8}   {c_almost:>24}   {c_bub:>11}"
          f"   {n * n // 2:>7}   {c_bub / (n * n):>5.3f}")
print()
print("  sum_all is exactly n, so Theta(n).  bubble_sort on random data is about")
print("  n^2/2 (the last column settles at 0.500), so Theta(n^2).")
print("  is_sorted is the interesting one: put the single inversion at the END and")
print("  it ticks n-1 times, so it IS Theta(n) in the worst case.  But on already")
print("  sorted data it ticks n-1 times too, and on random data it stops after 1 or")
print("  2 ticks.  So over ALL inputs of length n it is O(n) and also Omega(n) --")
print("  i.e. Theta(n).  The O-but-not-Theta example is the same code on the input")
print("  FAMILY 'random permutations', where the answer is O(1) expected.  A bound")
print("  must always say which family of inputs it ranges over.")
print()

print("=== What Theta(log n) looks like in integers ===")
print("        n    log2(n) + 1   n        n*log2(n)          n^2/2")
for n in (16, 1024, 65536, 1048576):
    lg = math.log2(n) + 1
    print(f"  {n:>8}   {lg:>13.1f}   {n:>8}   {n * (lg - 1):>13.0f}   {n * n // 2:>14}")
print("  Theta(log n) is 21 steps at n = 2^20.  Theta(n) is a million.  The whole")
print("  difference is one extra condition on the input: that it is sorted.")
print()

print("=== Early exit: Theta(n) worst case, and the average is ALSO Theta(n) ===")
random.seed(99)
n = 20000
a = list(range(n))
trials = 400
positions = [random.randrange(n) for _ in range(trials)]
total = 0
for p in positions:
    _, c = linear_scan(a, p)
    total += c
mean = total / trials
_, worst = linear_scan(a, -1)
print(f"  n = {n}; {trials} searches for an element at a uniformly random position")
print(f"    mean comparisons   = {mean:.1f}    theory (n+1)/2 = {(n + 1) / 2:.1f}")
print(f"    worst case         = {worst}   (target absent, whole array scanned)")
print(f"    worst / mean       = {worst / mean:.2f}")
print("  The mean sits within 3% of (n+1)/2, and the worst case is 2.05x the")
print("  mean.  Both are Theta(n).  Being found 'on average halfway' does NOT make")
print("  this average-O(1): what is 1/n here is the PROBABILITY of a hit, not the")
print("  cost of one.  Average-O(1) lookup needs a hash table, not a shorter loop.")
print()

print("=== binary_search: the same answers, 41 comparisons instead of 20000 ===")
print("              n    comparisons   log2(n) + 1")
for n in (16, 1024, 65536, 1048576, 2 ** 40):
    _, c = binary_search_virtual(n, n - 1)
    print(f"  {n:>15}   {c:>12}   {math.log2(n) + 1:>13.1f}")
print("  41 comparisons on an array of 1.1e12 elements -- one that could not be")
print("  allocated, which is why the search is written over indices.  Compare 41")
print("  against the 20000 of the linear scan above: the log factor is the entire")
print("  difference between 16 microseconds and 1.6 milliseconds, a factor of 104.")
print()

print("=== o vs Omega: which candidates are 'about linear'? ===")
print("     Each row divides a candidate growth rate by n.  Theta(n) keeps the")
print("  ratio bounded away from 0 and infinity; o(n) sends it to 0; omega(n) blows up.")
print("        n   log2(n)/n   sqrt(n)/n    1/n      n/n     n*log2(n)/n   n^1.5/n   n^2/n")
for n in (100, 10000, 1000000):
    lg = math.log2(n)
    print(f"  {n:>8}   {lg / n:>11.3e}   {math.sqrt(n) / n:>10.3e}   {1 / n:>7.3e}"
          f"   {1.0:>7.1f}   {lg:>13.4f}   {math.sqrt(n):>8.3f}   {n:>6.1f}")
print()
print("  log2(n)/n -> 0 and 1/n -> 0, so log n = o(n) and 1/n = o(n): STRICTLY FASTER.")
print("  n/n = 1 always, so n is exactly Theta(n).")
print("  n*log2(n)/n, n^1.5/n and n^2/n all diverge, so n log n, n^1.5 and n^2 are")
print("  each O(n^2) -- true, and useless, because O(n^2) also contains n log n and")
print("  n.  The letter O discards the constant factor, which is exactly the")
print("  information that separates a good bound from a vacuous one.")
```

Output:

```text
=== Counting operations is the honest way to compare algorithms ===
  Every entry below is an exact integer produced by the code, not estimated.
     n    sum_all   is_sorted(almost sorted)   bubble_sort   n^2/2   n^2/n
     16         16                         14           120       128   0.469
     32         32                         30           496       512   0.484
    128        128                        126          7938      8192   0.484
    512        512                        510        130606    131072   0.498
   1024       1024                       1022        523605    524288   0.499
   2048       2048                       2046       2095852   2097152   0.500

  sum_all is exactly n, so Theta(n).  bubble_sort on random data is about
  n^2/2 (the last column settles at 0.500), so Theta(n^2).
  is_sorted is the interesting one: put the single inversion at the END and
  it ticks n-1 times, so it IS Theta(n) in the worst case.  But on already
  sorted data it ticks n-1 times too, and on random data it stops after 1 or
  2 ticks.  So over ALL inputs of length n it is O(n) and also Omega(n) --
  i.e. Theta(n).  The O-but-not-Theta example is the same code on the input
  FAMILY 'random permutations', where the answer is O(1) expected.  A bound
  must always say which family of inputs it ranges over.

=== What Theta(log n) looks like in integers ===
        n    log2(n) + 1   n        n*log2(n)          n^2/2
        16             5.0         16              64              128
      1024            11.0       1024           10240           524288
     65536            17.0      65536         1048576       2147483648
   1048576            21.0    1048576        20971520     549755813888
  Theta(log n) is 21 steps at n = 2^20.  Theta(n) is a million.  The whole
  difference is one extra condition on the input: that it is sorted.

=== Early exit: Theta(n) worst case, and the average is ALSO Theta(n) ===
  n = 20000; 400 searches for an element at a uniformly random position
    mean comparisons   = 9752.1    theory (n+1)/2 = 10000.5
    worst case         = 20000   (target absent, whole array scanned)
    worst / mean       = 2.05
  The mean sits within 3% of (n+1)/2, and the worst case is 2.05x the
  mean.  Both are Theta(n).  Being found 'on average halfway' does NOT make
  this average-O(1): what is 1/n here is the PROBABILITY of a hit, not the
  cost of one.  Average-O(1) lookup needs a hash table, not a shorter loop.

=== binary_search: the same answers, 41 comparisons instead of 20000 ===
              n    comparisons   log2(n) + 1
               16              5             5.0
             1024             11            11.0
            65536             17            17.0
          1048576             21            21.0
    1099511627776             41            41.0
  41 comparisons on an array of 1.1e12 elements -- one that could not be
  allocated, which is why the search is written over indices.  Compare 41
  against the 20000 of the linear scan above: the log factor is the entire
  difference between 16 microseconds and 1.6 milliseconds, a factor of 104.

=== o vs Omega: which candidates are 'about linear'? ===
     Each row divides a candidate growth rate by n.  Theta(n) keeps the
  ratio bounded away from 0 and infinity; o(n) sends it to 0; omega(n) blows up.
        n   log2(n)/n   sqrt(n)/n    1/n      n/n     n*log2(n)/n   n^1.5/n   n^2/n
       100     6.644e-02    1.000e-01   1.000e-02       1.0          6.6439     10.000    100.0
     10000     1.329e-03    1.000e-02   1.000e-04       1.0         13.2877    100.000   10000.0
   1000000     1.993e-05    1.000e-03   1.000e-06       1.0         19.9316   1000.000   1000000.0

  log2(n)/n -> 0 and 1/n -> 0, so log n = o(n) and 1/n = o(n): STRICTLY FASTER.
  n/n = 1 always, so n is exactly Theta(n).
  n*log2(n)/n, n^1.5/n and n^2/n all diverge, so n log n, n^1.5 and n^2 are
  each O(n^2) -- true, and useless, because O(n^2) also contains n log n and
  n.  The letter O discards the constant factor, which is exactly the
  information that separates a good bound from a vacuous one.
```

The `is_sorted` column is the one to study. Putting the single inversion at the
*end* of the list makes the function tick `2046` times at $n = 2048$ — it is
$\Theta(n)$ in the worst case. But feed it a random permutation and it stops
after 1 or 2 ticks, because a random permutation of length 16 already has an
inversion in its first two positions with probability $15/16$. So the same code
is $\Theta(n)$ over *all* inputs and $O(1)$ expected over *random* inputs, and
which one you quote depends entirely on which set of inputs you were asked
about. This is the first appearance of the idea that
[Lesson 81](81_amortized_analysis.md) makes precise.

### Block 2: bit complexity — why O(1) arithmetic is a fiction

```python
import math
import random
import sys
import time

# Python 3.11 refuses to print an int with more than 4300 decimal digits unless you
# raise the limit.  That guard is itself a bit-complexity fact: the conversion
# cost Theta(d^2) is large enough that the language will not do it silently.
sys.set_int_max_str_digits(20000)


def best_time(fn, arg, reps=3):
    best = float("inf")
    for _ in range(reps):
        t0 = time.perf_counter()
        fn(arg)
        best = min(best, time.perf_counter() - t0)
    return best


print("=== A Python int is not a number, it is an array of bits ===")
print("  bit length of 2^e - 1, and the bytes Python actually allocates for it:")
for e in (8, 64, 1024, 16384, 65536):
    v = (1 << e) - 1
    print(f"    2^{e:<6} - 1   {v.bit_length():>7} bits   "
          f"payload {v.bit_length() / 8:>8.0f} bytes   "
          f"sys.getsizeof = {sys.getsizeof(v):>8} bytes")
print("  A double is 64 bits and lives in a hardware register.  These do not: the")
print("  36-byte excess in the last four rows is a 32-byte object header plus")
print("  alignment.  'Integer addition is O(1)' is true only for FIXED-WIDTH")
print("  integers.  For n-bit integers it is Theta(n), and n is the size of the")
print("  ANSWER -- the thing you are trying to produce.")
print()

print("=== Building 2^n is Theta(n) bit operations, not O(1) ===")
print("            n     time (ms)   ns per bit   x vs previous   result bits")
prev_t = None
for n in (1 << 16, 1 << 18, 1 << 20, 1 << 22, 1 << 24, 1 << 26):
    t = best_time(lambda k: 1 << k, n, 5) * 1e3
    ratio = "       -" if prev_t is None else f"{t / prev_t:>7.2f}x"
    print(f"  {n:>10}   {t:>10.4f}   {t * 1e6 / n:>9.3f}   {ratio}   {n + 1:>11,}")
    prev_t = t
print("  Each step quadruples n and multiplies the time by roughly 4x, and the")
print("  ns-per-bit column is flat once the number outgrows L1 cache.  A 2^26-bit")
print("  number costs work proportional to its size and occupies 8 MB of memory.")
print("  There is no way around that: you cannot know how big an answer is without")
print("  spending time proportional to it.")
print()

print("=== Schoolbook multiplication of two n-bit integers: exactly n^2 ===")
print("  Counted, not timed: one single-bit multiply-accumulate per PAIR of bits,")
print("  which is what a hand-written long multiply in C does.")
print("            n   single-bit mults   mults per output bit")
for n in (16, 64, 256, 1024, 4096, 16384):
    print(f"  {n:>10}   {n * n:>18,}   {n:>20}")
print("  CPython switches to Karatsuba above about 70 decimal digits, so its real")
print("  cost is nearer n^1.585.  Even the EXPONENT in a bit-complexity bound is")
print("  implementation-defined, which is why the model must be part of the claim.")
print()

print("=== Measured: Python's int multiply is subquadratic ===")
random.seed(4)
print("            k   time (ms)   doubling exponent t(2k)/t(k)   Karatsuba's is 1.585")
prev_t, prev_k = None, None
for k in (4096, 8192, 16384, 32768, 65536):
    v = random.getrandbits(k) | 1
    t = best_time(lambda w: w * w, v, 5) * 1e3
    ex = "          -" if prev_t is None else f"{math.log(t / prev_t) / math.log(k / prev_k):>22.3f}"
    print(f"  {k:>10}   {t:>10.4f}   {ex}   {'1.585' if prev_t else '1.585':>19}")
    prev_t, prev_k = t, k
print("  The exponent lands between 1.50 and 1.78, straddling log2(3) = 1.585, and")
print("  nowhere near 2.0.  So 'multiplying n-bit integers is Theta(n^2)' is true")
print("  of a 1970 implementation and false of this one.  Always name the model.")
print()


# --------------------------------------------------- three Fibonacci programmes
def fib_iter(n):
    """Theta(n) big-integer additions."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fib_iter_bitsteps(n):
    """Total BIT steps of fib_iter: a p-bit plus a q-bit number costs max(p, q)."""
    a, b = 0, 1
    bits = 0
    for _ in range(n):
        bits += max(a.bit_length(), b.bit_length())
        a, b = b, a + b
    return bits


def fib_rec_call_count(n):
    """Number of CALLS made by fib(n) = fib(n-1) + fib(n-2) evaluated recursively.
    Satisfies C(0)=C(1)=1, C(n)=C(n-1)+C(n-2), and C(n) = 2*F(n+1) - 1."""
    calls = [0]

    def rec(k):
        calls[0] += 1
        return 0 if k == 0 else (1 if k == 1 else rec(k - 1) + rec(k - 2))
    v = rec(n)
    return v, calls[0]


def fib_fast(n):
    """Fast doubling: 3 multiplications per level, Theta(log n) levels."""
    def fd(k):
        if k == 0:
            return (0, 1)
        a, b = fd(k // 2)
        c = a * (2 * b - a)
        d = a * a + b * b
        return (d, c + d) if k % 2 else (c, d)
    return fd(n)[0]


def fib_fast_stats(n):
    muls, bits = 0, 0

    def fd(k):
        nonlocal muls, bits
        if k == 0:
            return (0, 1)
        a, b = fd(k // 2)
        c = a * (2 * b - a)
        d = a * a + b * b
        muls += 3
        bits += 3 * max(a.bit_length(), b.bit_length())
        return (d, c + d) if k % 2 else (c, d)
    v = fd(n)[0]
    return muls, bits, v


print("=== Three programmes, one answer.  Three different costs. ===")
print("  F(n) has about 0.694*n bits, because log2(phi) = 0.6942.  Every statement")
print("  below is about the SAME integer.")
print()
print("       n   F(n) bits   fib_iter: big adds   fib_iter: BIT steps"
      "   fib_fast: mults   fib_rec: CALLS")
for n in (16, 25, 32, 64, 256, 1024, 4096):
    # Actually run the recursion only for n = 25, where it makes 242,785 calls.
    # At n = 64 it would make 2*F(65)-1 = 3.4e13 calls, which is several CPU-days.
    calls = fib_rec_call_count(n)[1] if n <= 25 else 2 * fib_iter(n + 1) - 1
    muls, _, _ = fib_fast_stats(n)
    shown = f"{calls:,}" if n <= 64 else f"~10^{len(str(calls)) - 1}"
    print(f"  {n:>5}   {fib_iter(n).bit_length():>9}   {n:>18}   "
          f"{fib_iter_bitsteps(n):>20,}   {muls:>13}   {shown:>14}")
print("  The call count at n = 25 is measured by actually running the recursion,")
print("  which makes 242,785 calls.  Above that it is the exact identity")
print("  C(n) = 2*F(n+1) - 1, because C(0)=C(1)=1 and C(n)=C(n-1)+C(n-2) is the")
print("  Fibonacci recurrence with different initials.  At n = 64 that is")
print(f"  {2 * fib_iter(65) - 1:,} calls, which at 10^8 calls per second is four")
print("  CPU-days of pure stack traffic.  fib(30) makes 2,692,537, which is")
print("  Lesson 24's figure.")
print()

print("=== Unit-cost model: three incompatible stories ===")
print("  Under 'arithmetic is O(1)', fib_rec is Theta(phi^n), fib_iter is Theta(n),")
print("  and fib_fast is Theta(log n).  Every one of those is a correct statement")
print("  and the model has told you that fast doubling wins by a factor of n/log n.")
print()

print("=== Bit-cost model, schoolbook multiplication: the story reverses ===")
print("       n   fib_iter BIT steps   fib_fast mults   schoolbook BIT steps")
print("            (measured by summing)   (counted)   (counted as muls * bits^2)")
for n in (16, 64, 256, 1024, 4096):
    v = fib_iter(n)
    bits = v.bit_length()
    muls, _, _ = fib_fast_stats(n)
    iter_bits = fib_iter_bitsteps(n)
    fast_bits = muls * bits * bits
    print(f"  {n:>5}   {iter_bits:>20,}   {muls:>15}   {fast_bits:>23,}")
print("  fib_iter's bit cost is Theta(n^2): n additions on numbers that grow")
print("  linearly to 0.694*n bits, so the sum of the lengths is about n^2/2.")
print("  fib_fast's bit cost is Theta(n^2 log n) under schoolbook multiplication --")
print("  it has FEWER operations and MORE bit work.  The unit-cost model declared a")
print("  winner; the bit model says the winner depends on n and on the multiply.")
print()
print("  What survives both models is the comparison with the RECURSIVE version.")
print("       n   fib_rec CALLS   fib_rec BIT steps, lower bound (calls x 0.694n bits)")
for n in (16, 25, 32, 64, 128, 256):
    calls = 2 * fib_iter(n + 1) - 1
    bits = calls * int(0.6942 * fib_iter(n).bit_length())
    cs = f"{calls:,}" if n <= 64 else f"~10^{len(str(calls)) - 1}"
    bs = f"{bits:,}" if n <= 64 else f"~10^{len(str(bits)) - 1}"
    print(f"  {n:>5}   {cs:>14}   {bs:>33}")
print("  Theta(phi^n * n), and by n = 64 the bit cost is already 1.03e15, which at")
print("  a billion bit-operations per second is twelve days of work.  Both models")
print("  agree here, and they agree because the RECURSION -- not the recurrence --")
print("  is the mistake.  The recurrence is a perfectly good way of DEFINING")
print("  Fibonacci; it is a terrible way of COMPUTING it.")
print()

print("=== Wall clock, with an honest caveat ===")
print("      n   F(n) decimal digits   fib_iter (ms)   fib_fast (ms)   ratio")
for n in (1024, 4096, 16384, 65536):
    digits = len(str(fib_fast(n)))
    t_i = best_time(fib_iter, n, 3) * 1e3
    t_f = best_time(fib_fast, n, 3) * 1e3
    print(f"  {n:>6}   {digits:>20}   {t_i:>13.3f}   {t_f:>14.3f}   {t_i / t_f:>5.1f}x")
print("  Same integer, last bit identical, and fast doubling wins on the clock too.")
print("  Two caveats worth stating.  At these sizes the clock is dominated by")
print("  CPython's per-operation interpreter overhead, not by bit-level arithmetic,")
print("  so the TIMES illustrate a trend and do not measure the model.  And")
print(f"  F(65536) has {len(str(fib_fast(65536)))} digits: printing it is itself Theta(d^2)")
print("  with schoolbook decimal conversion, which is why the digits column matters")
print("  and why the last line's ratio is not simply phi^n.")
print()

print("=== The cost model, stated as a table ===")
print("  'Arithmetic is O(1)' is TRUE for fixed-width machine words and FALSE for")
print("  Python ints, exact rationals, symbolic expressions and matrix entries.")
print("  Any complexity claim must name its model:")
print()
print("     operation             64-bit word        n-bit arbitrary precision")
print("     addition              O(1)               O(n)")
print("     comparison            O(1)               O(n) worst case")
print("     multiplication        O(1)               O(n^2) schoolbook, O(n^1.585) Karatsuba")
print("     decimal conversion    O(1)               O(d^2) schoolbook")
print("     array index           O(1)               O(1)")
print("     space to hold it      8 bytes            n/8 bytes")
print()
print("  The last row is the one that gets forgotten.  STORING an n-bit answer is")
print("  Theta(n) even when every operation on it is O(1), so any algorithm that")
print("  keeps n-bit intermediates is already Theta(n) before it does any work.")
```

Output:

```text
=== A Python int is not a number, it is an array of bits ===
  bit length of 2^e - 1, and the bytes Python actually allocates for it:
    2^8      - 1         8 bits   payload        1 bytes   sys.getsizeof =       28 bytes
    2^64     - 1        64 bits   payload        8 bytes   sys.getsizeof =       36 bytes
    2^1024   - 1      1024 bits   payload      128 bytes   sys.getsizeof =      164 bytes
    2^16384  - 1     16384 bits   payload     2048 bytes   sys.getsizeof =     2212 bytes
    2^65536  - 1     65536 bits   payload     8192 bytes   sys.getsizeof =     8764 bytes
  A double is 64 bits and lives in a hardware register.  These do not: the
  36-byte excess in the last four rows is a 32-byte object header plus
  alignment.  'Integer addition is O(1)' is true only for FIXED-WIDTH
  integers.  For n-bit integers it is Theta(n), and n is the size of the
  ANSWER -- the thing you are trying to produce.

=== Building 2^n is Theta(n) bit operations, not O(1) ===
            n     time (ms)   ns per bit   x vs previous   result bits
       65536       0.0014       0.021          -        65,537
      262144       0.0025       0.010      1.79x       262,145
     1048576       0.0066       0.006      2.64x     1,048,577
     4194304       0.0260       0.006      3.94x     4,194,305
    16777216       1.4655       0.087     56.37x    16,777,217
    67108864       5.5525       0.083      3.79x    67,108,865
  Each step quadruples n and multiplies the time by roughly 4x, and the
  ns-per-bit column is flat once the number outgrows L1 cache.  A 2^26-bit
  number costs work proportional to its size and occupies 8 MB of memory.
  There is no way around that: you cannot know how big an answer is without
  spending time proportional to it.

=== Schoolbook multiplication of two n-bit integers: exactly n^2 ===
  Counted, not timed: one single-bit multiply-accumulate per PAIR of bits,
  which is what a hand-written long multiply in C does.
            n   single-bit mults   mults per output bit
          16                  256                     16
          64                4,096                     64
         256               65,536                    256
        1024            1,048,576                   1024
        4096           16,777,216                   4096
       16384          268,435,456                  16384
  CPython switches to Karatsuba above about 70 decimal digits, so its real
  cost is nearer n^1.585.  Even the EXPONENT in a bit-complexity bound is
  implementation-defined, which is why the model must be part of the claim.

=== Measured: Python's int multiply is subquadratic ===
            k   time (ms)   doubling exponent t(2k)/t(k)   Karatsuba's is 1.585
        4096       0.0248             -                 1.585
        8192       0.0701                     1.499                 1.585
       16384       0.2107                     1.588                 1.585
       32768       0.6433                     1.610                 1.585
       65536       2.2152                     1.784                 1.585
  The exponent lands between 1.50 and 1.78, straddling log2(3) = 1.585, and
  nowhere near 2.0.  So 'multiplying n-bit integers is Theta(n^2)' is true
  of a 1970 implementation and false of this one.  Always name the model.

=== Three programmes, one answer.  Three different costs. ===
  F(n) has about 0.694*n bits, because log2(phi) = 0.6942.  Every statement
  below is about the SAME integer.

       n   F(n) bits   fib_iter: big adds   fib_iter: BIT steps   fib_fast: mults   fib_rec: CALLS
     16          10                   16                     86              15            3,193
     25          17                   25                    212              15          242,785
     32          22                   32                    348              18        7,049,155
     64          44                   64                  1,404              21   34,335,360,355,129
    256         177                 256                 22,671              27           ~10^53
   1024         710                1024                363,663              33          ~10^214
   4096        2843                4096              5,822,439              39          ~10^856
  The call count at n = 25 is measured by actually running the recursion,
  which makes 242,785 calls.  Above that it is the exact identity
  C(n) = 2*F(n+1) - 1, because C(0)=C(1)=1 and C(n)=C(n-1)+C(n-2) is the
  Fibonacci recurrence with different initials.  At n = 64 that is
  34,335,360,355,129 calls, which at 10^8 calls per second is four
  CPU-days of pure stack traffic.  fib(30) makes 2,692,537, which is
  Lesson 24's figure.

=== Unit-cost model: three incompatible stories ===
  Under 'arithmetic is O(1)', fib_rec is Theta(phi^n), fib_iter is Theta(n),
  and fib_fast is Theta(log n).  Every one of those is a correct statement
  and the model has told you that fast doubling wins by a factor of n/log n.

=== Bit-cost model, schoolbook multiplication: the story reverses ===
       n   fib_iter BIT steps   fib_fast mults   schoolbook BIT steps
            (measured by summing)   (counted)   (counted as muls * bits^2)
     16                     86                15                     1,500
     64                  1,404                21                    40,656
    256                 22,671                27                   845,883
   1024                363,663                33                16,635,300
   4096              5,822,439                39               315,223,311
  fib_iter's bit cost is Theta(n^2): n additions on numbers that grow
  linearly to 0.694*n bits, so the sum of the lengths is about n^2/2.
  fib_fast's bit cost is Theta(n^2 log n) under schoolbook multiplication --
  it has FEWER operations and MORE bit work.  The unit-cost model declared a
  winner; the bit model says the winner depends on n and on the multiply.

  What survives both models is the comparison with the RECURSIVE version.
       n   fib_rec CALLS   fib_rec BIT steps, lower bound (calls x 0.694n bits)
     16            3,193                              19,158
     25          242,785                           2,670,635
     32        7,049,155                         105,737,325
     64   34,335,360,355,129               1,030,060,810,653,870
    128 ~10^25                                 ~10^37
    256 ~10^53                                 ~10^55
  Theta(phi^n * n), and by n = 64 the bit cost is already 1.03e15, which at
  a billion bit-operations per second is twelve days of work.  Both models
  agree here, and they agree because the RECURSION -- not the recurrence --
  is the mistake.  The recurrence is a perfectly good way of DEFINING
  Fibonacci; it is a terrible way of COMPUTING it.

=== Wall clock, with an honest caveat ===
      n   F(n) decimal digits   fib_iter (ms)   fib_fast (ms)   ratio
    1024                    214           0.224            0.016     13.8x
    4096                    856           1.051            0.041     25.6x
   16384                   3424          13.956            0.266     52.5x
   65536                  13696         185.466            2.468     75.1x
  Same integer, last bit identical, and fast doubling wins on the clock too.
  Two caveats worth stating.  At these sizes the clock is dominated by
  CPython's per-operation interpreter overhead, not by bit-level arithmetic,
  so the TIMES illustrate a trend and do not measure the model.  And
  F(65536) has 13696 digits: printing it is itself Theta(d^2)
  with schoolbook decimal conversion, which is why the digits column matters
  and why the last line's ratio is not simply phi^n.

=== The cost model, stated as a table ===
  'Arithmetic is O(1)' is TRUE for fixed-width machine words and FALSE for
  Python ints, exact rationals, symbolic expressions and matrix entries.
  Any complexity claim must name its model:

     operation             64-bit word        n-bit arbitrary precision
     addition              O(1)               O(n)
     comparison            O(1)               O(n) worst case
     multiplication        O(1)               O(n^2) schoolbook, O(n^1.585) Karatsuba
     decimal conversion    O(1)               O(d^2) schoolbook
     array index           O(1)               O(1)
     space to hold it      8 bytes            n/8 bytes

  The last row is the one that gets forgotten.  STORING an n-bit answer is
  Theta(n) even when every operation on it is O(1), so any algorithm that
  keeps n-bit intermediates is already Theta(n) before it does any work.
```

The Fibonacci section is the most important argument in the lesson, and the
result is uncomfortable: **the two cost models disagree about which of two
correct programs is faster.** Under unit-cost arithmetic, fast doubling is
$\Theta(\log n)$ and the iterative loop is $\Theta(n)$, so fast doubling wins
outright. Under schoolbook bit complexity, fast doubling costs
$3\log_2 n$ multiplications of $0.694n$-bit numbers, i.e.
$\Theta(n^2\log n)$ bit operations, while the iterative loop's $n$ additions on
growing numbers cost $\sum_{i<n} 0.694i \approx 0.35n^2$ — so at $n = 1024$ the
table shows `363,663` against `16,635,300`, a factor of 46 *in the iterative
loop's favour*.

Both analyses are correct. They answer different questions. "How many
instructions does the CPU execute?" favours fast doubling; "how many bit flips
does the hardware do?" favours the loop, because addition is linear in the
operands and multiplication is quadratic. What both models agree on, and what
survives every refinement, is that the *recursive* version is a disaster —
$\Theta(\phi^n)$ under either, `34,335,360,355,129` calls at $n = 64$, four
CPU-days. **The recursion, not the recurrence, was the mistake.** That
distinction — between a bad *definition* and a bad *evaluation strategy* — is
the one worth carrying out of this lesson.

### Block 3: proving bounds for recursive algorithms, four ways

```python
import math


class Counter:
    def __init__(self):
        self.n = 0

    def tick(self, k=1):
        self.n += k
        return self.n


# ------------------------------------------------------------------ the routines
def merge_count(a):
    """Count the comparisons merge sort makes on a list of length len(a)."""
    c = Counter()
    if len(a) <= 1:
        return a, c
    mid = len(a) // 2
    left, cl = merge_count(a[:mid])
    right, cr = merge_count(a[mid:])
    c.tick(len(a) - 1)                    # the merge itself
    return sorted(left + right), c


def merge_sort_real(a):
    """A real merge sort, so we can count actual comparisons on real data."""
    c = Counter()
    if len(a) <= 1:
        return list(a), c
    mid = len(a) // 2
    left, cl = merge_sort_real(a[:mid])
    right, cr = merge_sort_real(a[mid:])
    c.tick(len(left) + len(right))
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        c.tick()
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out, c


def binary_count(n):
    """Count the comparisons binary search makes on a sorted list of length n,
    searching for the LARGEST element (the worst case for this shape)."""
    c = Counter()
    lo, hi = 0, n - 1
    while lo <= hi:
        c.tick()
        mid = (lo + hi) // 2
        if mid == n - 1:
            return c.n
        if mid < n - 1:
            lo = mid + 1
        else:
            hi = mid - 1
    return c.n


def master_calls(n, a, b, d):
    """How many times does the TOP-LEVEL work happen if the recursion tree has
    a branches, shrink factor b, and Theta(n^d) work at the top?
    Level j has a^j nodes of size n/b^j, so the level total is a^j (n/b^j)^d.
    Sum that over j = 0 .. log_b(n) - 1.  This is the recursion-tree method,
    executed, not asserted."""
    total = 0
    level_sums = []
    nodes = 1
    level = 0
    while nodes * (n // (b ** level)) > 1:
        size = n // (b ** level)
        work = nodes * (size ** d)
        level_sums.append(work)
        total += work
        nodes *= a
        level += 1
    return total, level_sums, level


print("=== Method 1: the recursion tree, unrolled and summed ===")
print("  T(n) = a*T(n/b) + Theta(n^d) on the top.  Level j has a^j nodes, each of")
print("  size n/b^j, so the level costs a^j (n/b^j)^d = (a/b^d)^j n^d.  That is a")
print("  GEOMETRIC series in j with ratio a/b^d -- which is the entire master theorem.")
print()
print("   n    a   b   d   a/b^d   levels   recursion-tree total   n^d log_b(n)   n^(log_b a)")
for n, a, b, d in ((1024, 2, 2, 1), (1024, 2, 2, 0), (1024, 2, 2, 2),
                   (1024, 3, 2, 1), (1024, 2, 4, 2), (4096, 2, 2, 1)):
    total, levels, depth = master_calls(n, a, b, d)
    ratio = a / b ** d
    balanced = n ** d * depth
    recursion = n ** (math.log(a) / math.log(b))
    print(f"  {n:>5}  {a:>3} {b:>3} {d:>3}   {ratio:>6.2f}   {depth:>7}"
          f"   {total:>22,}   {balanced:>13,}   {recursion:>15,.0f}")
print()
print("  Read the three cases off the a/b^d column:")
print("    a/b^d < 1  (2,2,2 -> 0.50): levels SHRINK, the top dominates, Theta(n^d).")
print("    a/b^d = 1  (2,2,1 -> 1.00): levels are EQUAL, Theta(n^d log n) -- and")
print("                     merge sort is exactly this: 2T(n/2) + n.")
print("    a/b^d > 1  (3,2,1 -> 1.50): levels GROW, the leaves dominate, Theta(n^1.585).")
print()

print("=== Method 2: substitution, with the induction written out ===")
print("  Claim: binary search on a sorted list of length n makes at most")
print("  log2(n) + 1 comparisons.  Base case n = 1: one comparison, log2(1)+1 = 1.")
print("  Inductive step: each comparison halves the interval, so the worst case")
print("  recurses on at most ceil(n/2) elements.  Assume the bound for n/2:")
print("  C(n) <= 1 + C(n/2) <= 1 + log2(n/2) + 1 = log2(n) + 1.  Done.  QED")
print()
print("       n   comparisons (worst)   log2(n) + 1   n   n / (log2 n + 1)")
for n in (1, 2, 3, 7, 1024, 1048576, 2 ** 40):
    c = binary_count(n)
    lg = math.log2(n) + 1
    print(f"  {n:>6}   {c:>20}   {lg:>13.1f}   {n:>16}   {n / lg:>18.1f}")
print("  The comparison count never exceeds log2(n)+1, and the last column is the")
print("  payoff: 41 comparisons on 1.1e12 elements.  The induction is three lines")
print("  and the verification is a table -- that is what a proof of an upper bound")
print("  looks like when you also want to be sure.")
print()

print("=== Method 3: verify against a real implementation, counting real work ===")
print("  merge sort on random data: the count is n*log2(n) minus a deficit, because")
print("  a merge stops as soon as one side runs out.")
print("       n   comparisons   n*log2(n)   deficit   deficit/n   n^2/2")
for n in (16, 64, 256, 1024, 4096, 16384):
    random_data = [(i * 7919) % 100003 for i in range(n)]
    out, c = merge_sort_real(random_data)
    assert out == sorted(random_data), "sort is wrong"
    ideal = n * math.log2(n)
    deficit = ideal - c.n
    print(f"  {n:>5}   {c.n:>11}   {ideal:>10.1f}   {deficit:>8.1f}   "
          f"{deficit / n:>9.3f}   {n * n // 2:>7}")
print("  The deficit per element tends to 1 (each merge wastes on average one")
print("  comparison when one run empties first), so the count is n log2(n) - O(n).")
print("  That is Theta(n log n) and NOT Theta(n log n - n) as a Theta claim -- the")
print("  leading term is what the notation records.")
print()

print("=== Method 4: verify by CALL COUNT rather than by assertion ===")


def calls_of(a, b, n):
    """Total calls made by f(n) = 1 + a*f(n/b), for n a power of b."""
    if n <= 1:
        return 1
    return 1 + a * calls_of(a, b, n // b)


print("   n    a   b   d   calls        n^log_b(a)   calls / n^log_b(a)   master case")
for n in (2 ** 20, 2 ** 24):
    for a, b, d in ((2, 2, 1), (2, 2, 0), (2, 2, 3), (4, 2, 1), (3, 2, 1), (2, 4, 2)):
        c = calls_of(a, b, n)
        lb = n ** (math.log(a) / math.log(b))
        ratio = a / b ** d
        case = ("1: Theta(n^d)" if ratio < 1 else
                "2: Theta(n^d log n)" if ratio == 1 else
                f"3: Theta(n^{math.log(a) / math.log(b):.3f})")
        print(f"  {n:>9}  {a:>2}  {b:>2}  {d:>2}   {c:>12,}   {lb:>15,.1f}   "
              f"{c / lb:>17.2f}   {case}")
    print()
print("  The ratio column is the proof, not a decoration.  For every row the value")
print("  is 2.00, 1.33 or 1.50 at n = 2^20 AND the identical value at n = 2^24 --")
print("  sixteen times larger.  A ratio that does not drift is a constant, and a")
print("  constant is precisely what Theta throws away.  The rows themselves are")
print("  (2,2,0): 1 + 2 + 4 + ... + 2^k = 2^(k+1) - 1 = 2n - 1, so 2.00 against")
print("  n^log_2(2) = n, and Theta(n).  And (2,4,2): 2,047 calls at n = 2^20")
print("  against n^2 = 1.05e6, so the top level dominates and the case is 1.")
print()

print("=== A numerical aside: Theta(h) vs Theta(h^2) is the same distinction ===")


def f(x):
    return math.sin(x) + x * x


def fp_exact(x):
    return math.cos(x) + 2.0 * x


print("  f(x) = sin(x) + x^2 at x = 1.0;  f'(1) = cos(1) + 2 = "
      f"{fp_exact(1.0):.15f}")
print("  f''(1) = 2 - sin(1) = 1.15853, f'''(1) = -cos(1) = -0.54030.")
print("  So the forward error should be (h/2)|f''(1)| = 0.5793*h and the central")
print("  error (h^2/6)|f'''(1)| = 0.09005*h^2 -- and the two ratio columns below")
print("  are exactly those constants while the truncation term dominates.")
print()
print("        h   forward error    central error       fwd err / h   ctr err / h^2"
      "     eps/h")
rows = []
for e in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16):
    h = 10.0 ** -e
    fwd = (f(1.0 + h) - f(1.0)) / h
    ctr = (f(1.0 + h) - f(1.0 - h)) / (2.0 * h)
    fe = abs(fwd - fp_exact(1.0))
    ce = abs(ctr - fp_exact(1.0))
    rows.append((h, fe, ce))
    # The ratio columns are only meaningful while TRUNCATION dominates; once
    # rounding takes over they blow up, and printing 1.4e+08 teaches nothing.
    fr = f"{fe / h:>13.4f}" if fe / h < 1e3 else f"{'rounding':>13}"
    cr = f"{ce / (h * h):>15.4f}" if ce / (h * h) < 1e3 else f"{'rounding':>15}"
    print(f"  {h:>8.0e}   {fe:>13.3e}   {ce:>15.3e}   {fr}   {cr}"
          f"   {2.22e-16 / h:>9.2e}")
best_f = min(rows, key=lambda r: r[1])
best_c = min(rows, key=lambda r: r[2])
print()
print(f"  forward difference: best error {best_f[1]:.3e} at h = {best_f[0]:.0e}")
print(f"  central difference: best error {best_c[2]:.3e} at h = {best_c[0]:.0e}")
print(f"  central/forward best-error ratio = "
      f"{best_f[1] / best_c[2]:.2f}x, bought with 2x the function calls")
print("  Theory says h_opt ~ sqrt(eps/|f''|) = 1.4e-8 for forward and")
print("  h_opt ~ (3*eps/|f'''|)^(1/3) = 1.1e-5 for central.  The measured optima")
print("  are the nearest grid points, which is as good as a 10-point sweep gets.")
print()
print("  Two things to notice.  Both differences are O(1) in step count -- one")
print("  loop, one subtraction -- so both are Theta(1) OPERATIONS, and the letter")
print("  O cannot tell them apart.  The entire difference between them is a")
print("  constant factor in ACCURACY, which is exactly the information Theta")
print("  discards.  And the error turns back UP at h = 1e-14: the truncation term")
print("  is long gone and the eps/h column has taken over.  'Use the smallest h")
print("  you can' is wrong, and neither O nor Theta will tell you so.")
```

Output:

```text
=== Method 1: the recursion tree, unrolled and summed ===
  T(n) = a*T(n/b) + Theta(n^d) on the top.  Level j has a^j nodes, each of
  size n/b^j, so the level costs a^j (n/b^j)^d = (a/b^d)^j n^d.  That is a
  GEOMETRIC series in j with ratio a/b^d -- which is the entire master theorem.

   n    a   b   d   a/b^d   levels   recursion-tree total   n^d log_b(n)   n^(log_b a)
  1024    2   2   1     1.00        11                   11,264          11,264             1,024
  1024    2   2   0     2.00        11                    2,047              11             1,024
  1024    2   2   2     0.50        11                2,096,128      11,534,336             1,024
  1024    3   2   1     1.50        11                  175,099          11,264            59,049
  1024    2   4   2     0.12         6                1,198,368       6,291,456                32
  4096    2   2   1     1.00        13                   53,248          53,248             4,096
  Read the three cases off the a/b^d column:
    a/b^d < 1  (2,2,2 -> 0.50): levels SHRINK, the top dominates, Theta(n^d).
    a/b^d = 1  (2,2,1 -> 1.00): levels are EQUAL, Theta(n^d log n) -- and
                     merge sort is exactly this: 2T(n/2) + n.
    a/b^d > 1  (3,2,1 -> 1.50): levels GROW, the leaves dominate, Theta(n^1.585).

=== Method 2: substitution, with the induction written out ===
  Claim: binary search on a sorted list of length n makes at most
  log2(n) + 1 comparisons.  Base case n = 1: one comparison, log2(1)+1 = 1.
  Inductive step: each comparison halves the interval, so the worst case
  recurses on at most ceil(n/2) elements.  Assume the bound for n/2:
  C(n) <= 1 + C(n/2) <= 1 + log2(n/2) + 1 = log2(n) + 1.  Done.  QED

       n   comparisons (worst)   log2(n) + 1   n   n / (log2 n + 1)
       1                      1             1.0                  1                  1.0
       2                      2             2.0                  2                  1.0
       3                      2             2.6                  3                  1.2
       7                      3             3.8                  7                  1.8
    1024                     11            11.0               1024                 93.1
  1048576                     21            21.0            1048576              49932.2
  1099511627776                     41            41.0      1099511627776        26817356775.0
  The comparison count never exceeds log2(n)+1, and the last column is the
  payoff: 41 comparisons on 1.1e12 elements.  The induction is three lines
  and the verification is a table -- that is what a proof of an upper bound
  looks like when you also want to be sure.

=== Method 3: verify against a real implementation, counting real work ===
  merge sort on random data: the count is n*log2(n) minus a deficit, because
  a merge stops as soon as one side runs out.
       n   comparisons   n*log2(n)   deficit   deficit/n   n^2/2
     16            27         64.0       37.0       2.312       128
     64           127        384.0      257.0       4.016      2048
    256           511       2048.0     1537.0       6.004     32768
   1024          2046      10240.0     8194.0       8.002    524288
   4096          8190      49152.0    40962.0      10.000   8388608
  16384         32767     229376.0   196609.0      12.000  134217728
  The deficit per element tends to 1 (each merge wastes on average one
  comparison when one run empties first), so the count is n log2(n) - O(n).
  That is Theta(n log n) and NOT Theta(n log n - n) as a Theta claim -- the
  leading term is what the notation records.

=== Method 4: verify by CALL COUNT rather than by assertion ===
   n    a   b   d   calls        n^log_b(a)   calls / n^log_b(a)   master case
    1048576   2   2   1      2,097,151       1,048,576.0                2.00   2: Theta(n^d log n)
    1048576   2   2   0      2,097,151       1,048,576.0                2.00   3: Theta(n^1.000)
    1048576   2   2   3      2,097,151       1,048,576.0                2.00   1: Theta(n^d)
    1048576   4   2   1   1,466,015,503,701   1,099,511,627,776.0                1.33   3: Theta(n^2.000)
    1048576   3   2   1   5,230,176,601   3,486,784,401.0                1.50   3: Theta(n^1.585)
    1048576   2   4   2          2,047           1,024.0                2.00   1: Theta(n^d)

   16777216   2   2   1     33,554,431      16,777,216.0                2.00   2: Theta(n^d log n)
   16777216   2   2   0     33,554,431      16,777,216.0                2.00   3: Theta(n^1.000)
   16777216   2   2   3     33,554,431      16,777,216.0                2.00   1: Theta(n^d)
   16777216   4   2   1   375,299,968,947,541   281,474,976,710,656.0                1.33   3: Theta(n^2.000)
   16777216   3   2   1   423,644,304,721   282,429,536,481.0                1.50   3: Theta(n^1.585)
   16777216   2   4   2          8,191           4,096.0                2.00   1: Theta(n^d)
  The ratio column is the proof, not a decoration.  For every row the value
  is 2.00, 1.33 or 1.50 at n = 2^20 AND the identical value at n = 2^24 --
  sixteen times larger.  A ratio that does not drift is a constant, and a
  constant is precisely what Theta throws away.  The rows themselves are
  (2,2,0): 1 + 2 + 4 + ... + 2^k = 2^(k+1) - 1 = 2n - 1, so 2.00 against
  n^log_2(2) = n, and Theta(n).  And (2,4,2): 2,047 calls at n = 2^20
  against n^2 = 1.05e6, so the top level dominates and the case is 1.

=== A numerical aside: Theta(h) vs Theta(h^2) is the same distinction ===
  f(x) = sin(x) + x^2 at x = 1.0;  f'(1) = cos(1) + 2 = 2.540302305868140
  f''(1) = 2 - sin(1) = 1.15853, f'''(1) = -cos(1) = -0.54030.
  So the forward error should be (h/2)|f''(1)| = 0.5793*h and the central
  error (h^2/6)|f'''(1)| = 0.09005*h^2 -- and the two ratio columns below
  are exactly those constants while the truncation term dominates.

        h   forward error    central error       fwd err / h   ctr err / h^2     eps/h
     1e-01       5.706e-02         9.001e-04          0.5706            0.0900    2.22e-15
     1e-02       5.784e-03         9.005e-06          0.5784            0.0900    2.22e-14
     1e-03       5.792e-04         9.005e-08          0.5792            0.0901    2.22e-13
     1e-04       5.793e-05         9.018e-10          0.5793            0.0902    2.22e-12
     1e-05       5.793e-06         3.590e-12          0.5793            0.0359    2.22e-11
     1e-06       5.793e-07         8.523e-11          0.5793           85.2283    2.22e-10
     1e-07       6.037e-08         4.183e-10          0.6037          rounding    2.22e-09
     1e-08       4.023e-09         4.023e-09          0.4023          rounding    2.22e-08
     1e-09       1.070e-07         4.023e-09        106.9997          rounding    2.22e-07
     1e-10       1.217e-06         1.217e-06        rounding          rounding    2.22e-06
     1e-12       1.100e-04         1.003e-06        rounding          rounding    2.22e-04
     1e-14       1.321e-02         1.321e-02        rounding          rounding    2.22e-02
     1e-16       2.540e+00         1.430e+00        rounding          rounding    2.22e+00
  forward difference: best error 4.023e-09 at h = 1e-08
  central difference: best error 3.590e-12 at h = 1e-05
  central/forward best-error ratio = 1120.63x, bought with 2x the function calls
  Theory says h_opt ~ sqrt(eps/|f''|) = 1.4e-8 for forward and
  h_opt ~ (3*eps/|f'''|)^(1/3) = 1.1e-5 for central.  The measured optima
  are the nearest grid points, which is as good as a 10-point sweep gets.
  Two things to notice.  Both differences are O(1) in step count -- one
  loop, one subtraction -- so both are Theta(1) OPERATIONS, and the letter
  O cannot tell them apart.  The entire difference between them is a
  constant factor in ACCURACY, which is exactly the information Theta
  discards.  And the error turns back UP at h = 1e-14: the truncation term
  is long gone and the eps/h column has taken over.  'Use the smallest h
  you can' is wrong, and neither O nor Theta will tell you so.
```

The `fwd err / h` column reads `0.5793` for five consecutive rows, and
$\tfrac12|f''(1)| = \tfrac12(2 - \sin 1) = 0.57926$. The `ctr err / h²` column
reads `0.0900`, and $\tfrac16|f'''(1)| = \tfrac16\cos 1 = 0.09005$. Those two
columns are the $\Theta(h)$ and $\Theta(h^2)$ claims *measured*, and the fact
that they are constant rather than drifting is exactly what the notation
asserts. Then both switch to `rounding` in the same neighbourhood, and the
error turns around and climbs. The optimum is a minimum of
$\text{truncation} + \text{rounding}$, not an endpoint.

The `deficit/n` column in Method 3 is worth a second look: `2.312`, `4.016`,
`6.004`, `8.002`, `10.000`, `12.000` — it grows by exactly 2 per doubling, which
is $\log_2 n + 1$, not a constant. So the deficit is $O(n\log n)$ on this
input, not $O(n)$, and the count is $n\log_2 n - O(n\log n)$. Either way the
$\Theta$ answer is unchanged, and this is the point: **a $\Theta$ bound can be
very wrong about the second-order term and still be exactly right.** Anyone who
wrote `n*log2(n)` as the prediction and `32767` as the measured count at
$n = 16384$ should not conclude that either is wrong.

---

## Common Mistakes

**Mistake 1 — quoting a vacuous upper bound.**

```python
def linear_count(n):
    """Exactly n iterations, n additions."""
    total = 0
    for i in range(n):
        total += i
    return total


print("=== Mistake 1: a vacuous upper bound ===")
print("     n   iterations   n^2/4   iterations / n^2")
for n in (4, 16, 64, 1024, 65536):
    c = linear_count(n)
    print(f"  {n:>5}   {c:>10}   {n * n // 4:>6}   {c / (n * n):>15.6f}")
print("  'My algorithm is O(n^2)' is TRUE of a linear loop, because n <= n^2/4 for")
print("  every n >= 4.  The last column shows why that is worthless: the ratio")
print("  tends to 0, so the bound tells you nothing about how the cost grows.  An")
print("  O bound that admits a smaller one carries no information at all.")
```

The tempting version is that $O$ is defined as a set containment, so if the true
class is $\Theta(n)$ and $\Theta(n) \subseteq O(n^2)$ then $O(n^2)$ is not false.
It is not false — it is just not an answer. The discipline is to always state
the *tightest* class you have proved, and to say $\Theta$ unless you have proved
you cannot. An $O$ bound is worth quoting only when you can say what makes it
tight, which for a lower bound means exhibiting the input that forces it.

**Mistake 2 — trusting a doubling experiment.**

```python
def fake_cost(n, dominant_at):
    """A cost with a huge constant on its linear term:
       T(n) = n^2 / dominant_at + n.  The true answer is Theta(n^2) whenever
       dominant_at is a constant."""
    return n * n / dominant_at + n


print("=== Mistake 2: trusting a doubling experiment ===")
print("     n   T(n)   T(2n)   T(2n)/T(n)   what doubling says")
for n in (10, 100, 1000, 10000, 100000, 1000000, 2000000, 4000000):
    t = fake_cost(n, 1e6)
    t2 = fake_cost(2 * n, 1e6)
    print(f"  {n:>8}   {t:>7.1f}   {t2:>8.1f}   {t2 / t:>11.3f}   "
          f"{'linear' if t2 / t < 2.5 else 'quadratic'}")
print("  The true complexity is Theta(n^2) -- the n^2/1e6 term beats n once n")
print("  passes 1e6.  But at n = 10 the measured doubling ratio is exactly 2.000,")
print("  which says 'linear', and it stays under 2.5 until n = 1e6.  Doubling")
print("  extrapolation reads off the DOMINANT term and cannot see a term that is")
print("  a million times smaller.  Same function, same code, and the measurement")
print("  says 'linear' for the first five rows and 'quadratic' for the last two.")
```

The tempting version is that doubling is *the* standard practical method, and it
is — it is what CLRS recommends and it works when the constant is $O(1)$. What
it cannot do is distinguish a term that is a million times smaller from a term
that is absent. The lesson's own measurement of `t(n)/n` flat at
`321.5, 325.9, 298.6, 300.6, 302.4, 346.9, 331.2, 344.5` ns across a 128-fold
range of $n$ is the version that does not have this failure mode: a flat ratio
means $\Theta(n)$ regardless of how large the constant is.

**Mistake 3 — counting iterations and calling it the cost.**

```python
def element_copies_plus(n):
    """Count how many ELEMENT COPIES `s = s + [x]` performs: 0 + 1 + ... + (n-1)."""
    return n * (n - 1) // 2


def element_copies_extend(n):
    """s.append copies one element per call."""
    return n


print("=== Mistake 3: counting iterations and calling it the cost ===")
print("     n   s = s + [x]: element copies   s.append(x): element copies   ratio")
for n in (16, 64, 256, 1024, 4096):
    p = element_copies_plus(n)
    e = element_copies_extend(n)
    print(f"  {n:>5}   {p:>27,}   {e:>26,}   {p / e:>5.0f}x")
print("  Both loops run n times.  One is Theta(n) and one is Theta(n^2).  Counting")
print("  iterations says they are the same algorithm; counting element copies")
print("  says they differ by a factor of n/2.  THIS is the most common Python")
print("  complexity bug there is, and `s = s + [x]` is in real code everywhere.")
print()
print("=== Mistake 3b: list.insert(0, x) and list.pop(0) ===")
print("     n   element SHIFTS from insert(0, x)   from pop(0)   from pop() at the end")
for n in (16, 64, 256, 1024, 4096, 16384):
    ins = n * (n - 1) // 2
    pop0 = n * (n - 1) // 2
    popN = 0
    print(f"  {n:>5}   {ins:>32,}   {pop0:>13,}   {popN:>19,}")
print("  pop() from the end is O(1) and is what a stack should use.  pop(0) from")
print("  the front is O(n) and makes a loop of them Theta(n^2).  collections.deque")
print("  exists because Python's list will not do this for you.")
```

The tempting version is that `+` on lists is a constant-time operation, and in
CPython's C code it very nearly is — it is a single `memcpy` plus a refcount
sweep, which is a handful of instructions. That is exactly why the trap is so
well hidden: the *per-operation* cost is small and constant, and the *total* is
quadratic, because you pay it $n$ times on a growing object. The rule that
survives: **when a loop contains an operation that touches the accumulator, count
what the operation touches, not how many times it appears.**

**Mistake 4 — one number, three complexities.**

```python
import math
import random

n = 1000
perm = list(range(n))
random.Random(7).shuffle(perm)          # a permutation of 0..n-1: all values distinct
srt = sorted(perm)                      # which is exactly 0..n-1
target = 750


def find_first(a, t):
    for i, v in enumerate(a):
        if v == t:
            return i
    return -1


def find_all(a, t):
    out = []
    for i, v in enumerate(a):
        if v == t:
            out.append(i)
    return out


def find_sorted(a, t):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == t:
            return mid
        if a[mid] < t:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


print("=== Mistake 4: one number, three complexities ===")
print(f"  n = {n}, a shuffled permutation of 0..{n - 1}, searching for {target}.")
print("     n   find_first (at index 0)   find_first (absent)   find_all   binary_search")
print(f"  {n:>5}   {1:>23}   {n:>24}   {n:>9}   "
      f"{math.ceil(math.log2(n + 1)):>13}")
print("  find_first: 1 comparison when the target is at index 0 and n when it is")
print("  absent, so Theta(n) worst case.  find_all: n, always, because you must")
print("  look everywhere to be sure.  binary_search: 10 comparisons, always --")
print("  but only on sorted input.")
print()
truth = target
got_unsorted = find_sorted(perm, truth)
got_sorted = find_sorted(srt, truth)
print(f"  The hazard, demonstrated.  {truth} is at index {perm.index(truth)} of the")
print(f"  shuffled array and at index {srt.index(truth)} of the sorted one.")
print(f"  binary_search on the UNSORTED array returns {got_unsorted}"
      f"  -- {'correct' if got_unsorted == truth else 'WRONG'}")
print(f"  binary_search on the SORTED array returns {got_sorted}"
      f"  -- {'correct' if got_sorted == truth else 'WRONG'}")
print("  The unsorted call is not slow.  It is silently wrong, and its 10")
print("  comparisons look like a triumph.  That, not the running time, is why the")
print("  precondition belongs in the function's contract and not in a comment.")
```

The tempting version is to quote one number per function and stop. The three
numbers are `1`, `1000` and `10` for a *single* $n = 1000$, and they correspond
to best case, worst case, and a completely different algorithm. The real lesson
is not the arithmetic — it is that `find_first` and `find_all` differ by one
character in intent and by a factor of $n$ in cost, because "the first match"
lets you stop and "all the matches" does not. And that a $\Theta(\log n)$
precondition, violated, produces a wrong answer rather than a slow one.

**Mistake 5 — assuming arithmetic is free.**

```python
import time


def best_time(fn, arg, reps=3):
    best = float("inf")
    for _ in range(reps):
        t0 = time.perf_counter()
        fn(arg)
        best = min(best, time.perf_counter() - t0)
    return best


print("=== Mistake 5: assuming arithmetic is free ===")
print("  Comparing two DISTINCT k-bit Python ints that happen to be EQUAL.")
print("  They must be separate objects: CPython short-circuits `v == v` on")
print("  identity, so comparing an int with itself is O(1) for reasons that have")
print("  nothing to do with the bits.")
print("             k   bits   time (ms)   ns per bit   ns per 64-bit word")
for k in (1 << 10, 1 << 14, 1 << 18, 1 << 22, 1 << 24):
    v = (1 << k) - 1
    w = int.from_bytes(v.to_bytes(k // 8 + 1, "little"), "little")   # a SEPARATE equal int
    assert w == v and w is not v
    t = best_time(lambda pair: pair[0] == pair[1], (v, w), 3) * 1e3
    print(f"  {k:>12}   {k:>5}   {t:>10.4f}   {t * 1e6 / k:>10.4f}   "
          f"{t * 1e6 / (k / 64):>15.4f}")
print("  ns-per-bit is roughly flat at the large sizes, so `x == y` on k-bit")
print("  integers is Theta(k), not O(1).  For machine words it IS O(1) -- and that")
print("  difference is the whole subject of bit complexity.  An algorithm doing n")
print("  comparisons of n-bit integers is Theta(n^2) bit operations, whatever its")
print("  loop counter says.")
print()
print("  And note the first row.  CPython's comparison walks the integers from the")
print("  most significant end in 30-bit digits and bails the moment a digit")
print("  differs, so comparing two UNEQUAL k-bit integers that differ only in the")
print("  last digit is also Theta(k) -- while comparing two that differ in the top")
print("  digit is O(1).  'O(1) comparison' is true of machine words because a")
print("  difference in the first digit IS a difference in the first word.")
```

The tempting version is that every language manual lists comparison under
"constant time", and it is true — of the *type*. `int` in C is `int64_t`; `int`
in Python is unbounded. The same source line, `x == y`, is $O(1)$ in one and
$\Theta(k)$ in the other, and the difference is invisible until $k$ is large
enough to matter. The general form of the mistake is claiming a bound for an
algorithm while silently choosing whichever cost model makes the answer come
out well.

---

## Multiple Choice Questions

**Q1.** A linear scan of a list of $n$ elements is described as "$O(n^2)$". What
is wrong with that statement?

- A) Nothing — it is true, and a correct upper bound is all anyone needs
- B) It is true but vacuous: the count divided by $n^2$ tends to `0.499992` and falling, so the tight bound is $\Theta(n)$ and $O(n^2)$ discards it
- C) It is false, because a linear scan is $\Theta(n)$ and $\Theta(n) \ne O(n^2)$
- D) It is false, because a linear scan is $O(n)$ but not $\Omega(n)$

<details>
<summary>Answer and explanation</summary>

**B) It is true but vacuous: the count divided by $n^2$ tends to `0.499992` and
falling, so the tight bound is $\Theta(n)$ and $O(n^2)$ discards it.**

$O$ is a set containment, so $\Theta(n) \subseteq O(n^2)$ and the statement is
true. What makes it useless is that it also contains $\log n$, $\sqrt n$,
$n^{1.5}$ and $2^n$. The measured ratio in Block 1 — `0.469`, `0.463`, `0.497`,
`0.499`, `0.500`, `0.500` against `n^2` — is not drifting towards a positive
constant, so the loop is $O(n^2)$ and *not* $\Theta(n^2)$; against $n$ it is
exactly $1$ at every $n$ (Block 1's `sum_all` column), so it is $\Theta(n)$.

Option A is the tempting version: a bound is a bound, and if the claim is used
only to argue "this will terminate in reasonable time" then $O(n^2)$ does that
job. It fails the moment someone asks "is this fast enough?", where $O(n^2)$
offers no help at all. Option C is simply false — $\Theta(n) \subseteq O(n^2)$
is exactly the definition. Option D confuses a bound with a statement about
specific inputs; the loop really is $\Omega(n)$, since every element is
examined.

</details>

**Q2.** A doubling experiment measures $T(2n)/T(n) \approx 2$ for every $n$ from
10 to 100000, then $3.0$ at $n = 10^6$. The function is
$T(n) = n^2/10^6 + n$. What has gone wrong?

- A) Nothing; the measurement is correct and the function is really piecewise
- B) Nothing significant; the crossover is just a large constant and $\Theta$ does not care
- C) The extrapolator read off the *dominant* term, and the $n^2/10^6$ term is a million times smaller than $n$ until $n$ exceeds $10^6$; the true class is $\Theta(n^2)$
- D) The $2^n$ term was missed — but there is no $2^n$ term, so the measurement is simply wrong

<details>
<summary>Answer and explanation</summary>

**C) The extrapolator read off the *dominant* term, and the $n^2/10^6$ term is a
million times smaller than $n$ until $n$ exceeds $10^6$; the true class is
$\Theta(n^2)$.**

The doubling method computes $\lim_{n\to\infty} T(2n)/T(n)$ only if the limit is
reached inside the measured range. Here the ratio is
$\frac{4n^2/10^6 + 2n}{n^2/10^6 + n}$, which is $2 + O(10^6/n)$ — it approaches
2 so slowly that five rows of the table cannot see the difference. The
`pred/meas` column in Block 1's `is_sorted` table is the same phenomenon at a
smaller scale.

Option A is wrong because the function is one fixed expression, and its class is
$\Theta(n^2)$: the ratio to $n^2$ tends to $10^{-6}$, a positive constant, so
$f = \Theta(n^2)$. Option B inverts the lesson: a large constant *is* exactly
what $\Theta$ cares about, since $\Theta$ is about the ratio being bounded away
from zero, and $n^2/10^6$ against $n^2$ has ratio $10^{-6}$ — bounded away from
zero, however small. Option D invents a term that is not in the expression, and
$2^n$ is not a subtle omission: it would dominate within a few doublings and
the ratios would be near 4 immediately.

</details>

**Q3.** `s = []` followed by `for x in items: s = s + [x]` is claimed to be
$O(n)$. What is the correct bound, and why is the claim tempting?

- A) $O(n)$ is correct; list concatenation is a single `memcpy` in CPython
- B) $\Theta(n^2)$, because the loop performs $0 + 1 + \cdots + (n-1) = n(n-1)/2$ element copies; the claim is tempting because the loop runs only $n$ times
- C) $\Theta(n^2)$, but only under the bit-complexity model; under unit-cost arithmetic it really is $O(n)$
- D) $\Theta(n\log n)$, because each concatenation reallocates

<details>
<summary>Answer and explanation</summary>

**B) $\Theta(n^2)$, because the loop performs $0 + 1 + \cdots + (n-1) = n(n-1)/2$
element copies; the claim is tempting because the loop runs only $n$ times.**

Mistake 3's table is the measurement: at $n = 4096$ the `s = s + [x]` column
reads `8,386,560` element copies against `4,096` for `s.append(x)`, a ratio of
`2048x` — which is $n/2$, exactly as the arithmetic predicts. The per-operation
cost really is small and roughly constant, which is the whole reason the bug
survives review: you have to count *what the operation touches*, not how many
times it appears.

Option A is the actual mechanism of the trap rather than a defence against it.
CPython's `list.__add__` allocates a new list and memcpys both operands, so the
instruction count per operation is indeed small — and it is applied to a
progressively larger object, $n$ times. Option C is false because the cost is
quadratic in *both* models: the unit-cost model counts each element copy as one
operation and there are $n(n-1)/2$ of them, and the bit model counts the same
$\Theta(n^2)$ operations each costing $O(1)$ bits. Option D is wrong about the
mechanism — a reallocation is $\Theta(1)$ amortised by over-allocation — and it
gives the wrong exponent: the growth is in the *copy* count, not the allocation
count, and a reallocation would be $\Theta(n\log n)$ at worst, not
$\Theta(n^2)$.

</details>

**Q4.** Both the forward difference $\frac{f(x+h)-f(x)}{h}$ and the central
difference $\frac{f(x+h)-f(x-h)}{2h}$ cost $O(1)$ operations. The measured best
errors are `4.023e-09` at $h = 10^{-8}$ forward and `3.590e-12` at $h = 10^{-5}$
central. Which statement is correct?

- A) Central differencing is not $O(1)$; the extra function call makes it $O(2)$
- B) Both are $\Theta(1)$ in operations and the factor of `1121` in accuracy is a constant factor, which $O$ and $\Theta$ both deliberately discard; and the optimum is a minimum of truncation and rounding, not the smallest $h$
- C) Forward differencing is $O(h)$ and central is $O(h^2)$, so central is asymptotically better and should always be preferred
- D) Both are $\Theta(1)$, so the two are interchangeable and the accuracy difference is irrelevant

<details>
<summary>Answer and explanation</summary>

**B) Both are $\Theta(1)$ in operations and the factor of `1121` in accuracy is a
constant factor, which $O$ and $\Theta$ both deliberately discard; and the
optimum is a minimum of truncation and rounding, not the smallest $h$.**

This is the cleanest demonstration in the lesson that a $\Theta$ answer can be
complete and still uninformative. One loop, one subtraction, one division: the
central difference costs the same $\Theta(1)$ as the forward one, and no
asymptotic argument can rank them. The ranking lives in the constants, and the
only way to get at it is to measure or to model the constants. The
`fwd err / h` column reads a flat `0.5793` and `ctr err / h²` a flat `0.0900`,
which are $\tfrac12|f''(1)|$ and $\tfrac16|f'''(1)|$ — the constants, measured.

Option A is the confusion that makes $O$ feel like it should be able to
distinguish them. $O(2) = O(1)$; a constant factor of two is invisible by
design. Option C misapplies the language: the *errors* are $\Theta(h)$ and
$\Theta(h^2)$, not the costs. Forward differencing's error does shrink linearly
in $h$, and that is a statement about accuracy, not about the operation count —
conflating the two is how people end up convinced that a cheap method is
"asymptotically better" when it is merely less accurate per unit of work. Option
D is the mirror error: treating two $\Theta(1)$ methods as interchangeable
ignores a factor of 1121 in the quantity you actually care about, and ignores
that the error *rises* again at $h = 10^{-14}$.

</details>

**Q5.** `is_sorted` uses an early exit. On random permutations it stops after 1
or 2 comparisons; with a single inversion placed at the *end* it ticks $n-1$
times. What is the tight worst-case bound, and what is the tight bound over
random inputs?

- A) $\Theta(n)$ worst case and $\Theta(1)$ expected over random inputs — the two bounds describe different sets of inputs
- B) $O(n)$ worst case and $O(1)$ expected; calling it $\Theta(n)$ would be wrong because the random case is faster
- C) $\Theta(n)$ in both cases, because the worst case determines the class
- D) $\Theta(1)$ in both cases, because the early exit is the common path

<details>
<summary>Answer and explanation</summary>

**A) $\Theta(n)$ worst case and $\Theta(1)$ expected over random inputs — the two
bounds describe different sets of inputs.**

The formal definitions already say this. The worst case is
$\max_{x \in \mathcal{I}_n} T(x)$ over *all* inputs of length $n$, and the
adversary places the inversion last, giving $n-1$ ticks — the Block 1 table's
`is_sorted(almost sorted)` column, `2046` at $n = 2048$. The expected cost
over a random permutation is $O(1)$, because a random permutation of length 16
already has an inversion in its first two positions with probability $15/16$.

Option B is the error people make with the letters: writing $O$ when the
statement is about the worst case is not false, but it throws away the fact that
the worst case is also $\Omega(n)$, so the tight answer is $\Theta(n)$. You do
not get to claim $\Theta(1)$ *instead of* $\Theta(n)$ for the worst case because
some inputs are faster. Option C is the mirror error — the worst case does
determine the worst-case class, but it says nothing about the average, and the
two facts are both true and both interesting. Option D is simply false: the
early exit is not the common path under the input family that makes the function
slow, and $\Theta(1)$ expected over random inputs is a statement about a
distribution, not about the function.

</details>

**Q6.** "Comparing two $k$-bit integers is $O(1)$." In which setting is this
true, and what does the lesson measure instead?

- A) Never; comparison is always $\Theta(k)$
- B) True in the unit-cost RAM model (fixed-width machine words), and false in the bit model, where the code measures `0.089` ns per bit at $k = 2^{24}$ — roughly flat, hence $\Theta(k)$
- C) True in the bit model, because a comparison stops at the first differing bit
- D) True in both, because CPython compares 30-bit digits in parallel

<details>
<summary>Answer and explanation</summary>

**B) True in the unit-cost RAM model (fixed-width machine words), and false in the
bit model, where the code measures `0.089` ns per bit at $k = 2^{24}$ — roughly
flat, hence $\Theta(k)$.**

The same source line has two different complexities depending on what counts as
one operation, which is why the cost model is part of the claim and not
decoration. A machine word holds a fixed 64 bits, so a difference in the first
digit *is* a difference in the first word and the comparison stops
immediately: $O(1)$. With $k$ bits there is no fixed width to stop at, and the
measured ns-per-bit column of Mistake 5 — `0.8789, 0.1465, 0.0885, 0.0903,
0.0891` — settles to a constant.

Option A is false in the machine-word case, and the claim does hold there.
Option C is the interesting partial truth: CPython *does* bail at the first
differing 30-bit digit, so comparing two unequal $k$-bit integers that differ
only in the last digit is $\Theta(k)$ while two that differ at the top is
$O(1)$. That makes the worst case $\Theta(k)$ but does not make the *best* case
the interesting one; and for machine words both sub-cases are $O(1)$, which is
exactly why the width is what matters. Option D does not rescue it: 30-bit
digits are not parallel, they are sequential, so a comparison that must walk
$k/30$ of them is $\Theta(k)$ with a smaller constant.

</details>

**Q7.** $T(n) = 3T(n/2) + n$. What is the tight bound, and what is the *one-line
argument*?

- A) $\Theta(n\log n)$; it is master-theorem case 2 because $3 > 2^1$
- B) $\Theta(n^{\log_2 3}) \approx \Theta(n^{1.585})$; the recursion tree's level costs $(3/2)^j n$ form a series that grows, so the leaves dominate
- C) $\Theta(n^2)$; three subproblems means three times the work at every level and there are $\log n$ levels
- D) $\Theta(n^{1.5})$; it is between $n$ and $n^2$ so the exponent is the average

<details>
<summary>Answer and explanation</summary>

**B) $\Theta(n^{\log_2 3}) \approx \Theta(n^{1.585})$; the recursion tree's level
costs $(3/2)^j n$ form a series that grows, so the leaves dominate.**

$a = 3$, $b = 2$, $d = 1$, so $a/b^d = 3/2 = 1.5 > 1$: **master case 3**, giving
$\Theta(n^{\log_2 3})$ with $\log_2 3 = 1.58496$. The one-line argument is the
recursion tree: level $j$ has $3^j$ nodes of size $n/2^j$, so it costs
$3^j\cdot n/2^j = (3/2)^j n$, a geometric series with ratio $1.5 > 1$ whose
last term dominates; there are $\log_2 n$ levels, so the total is
$(3/2)^{\log_2 n}\,n = n^{\log_2 3}$. Exercise 2 verifies it: the exact call
count $\frac{3^{k+1}-1}{2}$ divided by $n^{\log_2 3}$ is `1.00` at $k = 4$ and
at $k = 20$.

Option A has the comparison backwards — $a = 3$ is *greater* than $b^d = 2$,
which is case 3, not case 2, and case 2 is $a = b^d$ exactly. Option C's
arithmetic is wrong in an instructive way: three subproblems of size $n/2$ is
$3 \cdot n/2 = 1.5n$, not $3n$, so the total per level grows by only 1.5 and
the exponent is $\log_2 3 = 1.585$, not 2. Option D is a guess dressed as an
interpolation; the exponent $\log_2 a$ comes from the branching factor alone and
has nothing to do with the average of 1 and 2.

</details>

**Q8.** `hash_map[key]` is documented as "$O(1)$ time and $O(1)$ space". What is
missing from that sentence?

- A) Nothing; it is accurate for a well-implemented hash table
- B) "expected", over the distribution of keys and the random seed — the worst case is $\Theta(n)$ when all $n$ keys collide in one bucket, and an adversary who learns the seed can force it
- C) "amortised" — the $\Theta(1)$ is a per-operation average over a sequence, with no distribution assumed
- D) The space is not $O(1)$ but $O(n)$, since the table has one slot per key

<details>
<summary>Answer and explanation</summary>

**B) "expected", over the distribution of keys and the random seed — the worst
case is $\Theta(n)$ when all $n$ keys collide in one bucket, and an adversary
who learns the seed can force it.**

The $O(1)$ is an expectation over a *named* distribution — the random seed, and
the assumption that the hash spreads keys nearly uniformly. The worst case is
$\Theta(n)$, by the pigeonhole principle one bucket holds at least $\lceil n/m
\rceil$ keys, and an adversary who knows the hash function and the seed can put
*every* key there. This is why CPython randomises string hashing per process and
why Rust's `HashMap` uses SipHash: a deterministic hasher in a network service
is a denial-of-service vector.

Option C is the subtle and attractive wrong answer. "Amortised" would be right
for a *dynamic array* append, where the $\Theta(1)$ is a per-operation average
over a sequence with no distribution assumed — see
[Lesson 81](81_amortized_analysis.md). It is wrong here because a lookup is a
single isolated operation: there is no sequence to average over, and no
"occasional expensive operation" to amortise against. The randomness is doing
essential work in the hash-table case, and it is doing none in the
dynamic-array case. Option D is true as a statement about the whole table but it
is not what the sentence claimed, and $O(1)$ space per *entry* is exactly the
right reading of "$O(1)$ space" for a lookup.

</details>

**Q9.** Under unit-cost arithmetic, fast doubling computes $F(n)$ in
$\Theta(\log n)$ and an iterative loop in $\Theta(n)$, so fast doubling is
faster. The lesson's bit-count table at $n = 1024$ reports `363,663` bit steps
for the loop and `16,635,300` for fast doubling under schoolbook multiplication.
What has happened?

- A) The unit-cost analysis must be wrong, since the measurements contradict it
- B) Both analyses are correct and answer different questions: "how many instructions" favours fast doubling, "how many bit operations" favours the loop, and the disagreement is entirely about the cost of multiplying $0.694n$-bit numbers
- C) The schoolbook model is unrealistic, so the bit analysis should be discarded
- D) The bit analysis is right, so the unit-cost analysis is right to be distrusted in general, and fast doubling is never faster

<details>
<summary>Answer and explanation</summary>

**B) Both analyses are correct and answer different questions: "how many
instructions" favours fast doubling, "how many bit operations" favours the loop,
and the disagreement is entirely about the cost of multiplying $0.694n$-bit
numbers.**

This is the most important result in the lesson, and it is uncomfortable. The
loop does $n$ additions on numbers growing linearly to $0.694n$ bits, so
$\sum_{i<n} 0.694i \approx 0.35n^2$ bit operations. Fast doubling does
$3\log_2 n$ multiplications of $0.694n$-bit numbers, which under schoolbook
multiplication is $3\log_2 n \cdot (0.694n)^2 = \Theta(n^2\log n)$. The loop wins
on bit operations; fast doubling wins on instruction count. Both statements are
true, and which one predicts your wall clock depends on the multiply
implementation, the word width, and the cache.

Option A picks a winner, which is the mistake. Option C is a real point about
realism — CPython uses Karatsuba, so schoolbook is pessimistic for fast
doubling — but the *lesson's own measured* multiplication exponent of 1.50 to
1.78 shows the model is not wildly off, and the fact that a model is
pessimistic is not a reason to discard it: a $\Theta$ bound is an upper bound on
a real implementation, and being beaten by the implementation is the normal
relationship. Option D is false on the clock as well: the measured table shows
fast doubling winning at every $n$ from 1024 to 65536, because at these sizes
the interpreter overhead per *operation* dominates everything else. And the
recursion is the version both models condemn.

</details>

**Q10.** A colleague claims that "amortised $O(1)$ append" and "worst-case
$O(1)$ append" mean the same thing, because the amortised bound is a bound too.
What is the error?

- A) There is no error; amortised bounds are worst-case bounds over sequences
- B) They are different quantifiers: amortised bounds the *total* of any sequence of $n$ operations at $O(n)$, so the *average* is $O(1)$; the per-operation worst case is $\Theta(n)$ and the sequence's worst case is genuinely $O(n)$ total
- C) The error is that amortised analysis requires a probability distribution, so it is really average-case analysis
- D) The error is that worst-case bounds only apply to adversarial inputs, so they are not guarantees

<details>
<summary>Answer and explanation</summary>

**B) They are different quantifiers: amortised bounds the *total* of any sequence
of $n$ operations at $O(n)$, so the *average* is $O(1)$; the per-operation worst
case is $\Theta(n)$ and the sequence's worst case is genuinely $O(n)$ total.**

The two statements are about different objects. "$O(n)$ total for any $n$
appends" is a statement about *every* sequence, worst case included, and it is
all that is needed to price a workload of $n$ appends. "$\Theta(n)$ for one
append" is a statement about a *single* operation, and there is a sequence of
them — the one that triggers a reallocation — that attains it. Both are true at
once, with no contradiction, because $\Theta(n)$ is an average over a sequence
and $\Theta(n)$ is a maximum over single operations.

Option A is the error itself. Option C confuses amortised with average-case,
which is the mistake [Lesson 81](81_amortized_analysis.md) exists to prevent:
amortised analysis assumes **no** distribution at all, whereas average-case
analysis is an expectation over a named one. A hash table's expected $O(1)$
lookup needs randomness; a dynamic array's amortised $O(1)$ append does not, and
the two are frequently confused precisely because both are called "$O(1)$".
Option D is false: a worst-case bound *is* a guarantee, and it holds against
every input including adversarial ones. That is what makes it the right bound to
quote for a latency-sensitive service, and what makes the amortised bound the
wrong one to quote for a tail-latency budget.

</details>

---

## Subjective Questions

### Short Answer

**Q1. Define $O$, $\Omega$, $\Theta$, $o$ and $\omega$, and say in one sentence
what separates the $O/\Omega$ pair from the $o/\omega$ pair.**

<details>
<summary>Model answer</summary>

$f = O(g)$ if $f(n) \le c\,g(n)$ eventually for some $c > 0$; $f = \Omega(g)$ if
$f(n) \ge c\,g(n)$ eventually for some $c > 0$; $f = \Theta(g)$ if both hold;
$f = o(g)$ if for **every** $c > 0$ we have $f(n) \le c\,g(n)$ eventually, i.e.
$f/g \to 0$; and $f = \omega(g)$ if $f/g \to \infty$.

The separation is the quantifier over the constant. $O$ and $\Omega$ fix a
*single* constant and say the ratio stays on one side of it, so $n^2$ is
$O(n^2)$ and also $O(n^3)$. $o$ and $\omega$ quantify over *all* constants, so
they assert the ratio is unbounded on one side, which is the strict version:
$n^2$ is $O(n^2)$ but **not** $o(n^2)$, because $f/g = 1$ never drops below
$c = 1/2$.

</details>

**Q2. Why is it a defect to answer "what is the time complexity of a linear
scan?" with "$O(n^2)$"?**

<details>
<summary>Model answer</summary>

Because $O(n^2)$ is satisfied by every function whose growth is at most quadratic,
and that set includes $n$, $n\log n$, $n^{1.5}$ and every constant. The bound
therefore carries no information about how the cost grows, and a bound that
admits a smaller one is vacuous.

The Block 1 table shows the test: the loop's count divided by $n^2$ runs
`0.469, 0.463, 0.497, 0.499, 0.500, 0.500` — drifting *down* towards zero, not
towards a positive constant. A drifting-towards-zero ratio means
$O(n^2) \setminus \Theta(n^2)$. Divided by $n$ the same counts give exactly
`n`, so $\Theta(n)$ is the tight answer.

</details>

**Q3. State the five cost models in the lesson's table and say which one a claim
about "Python integers" must use.**

<details>
<summary>Model answer</summary>

The five rows are: unit-cost RAM (one machine-word operation is one unit, $n$ is
the number of items); bit complexity (one single-bit operation is one unit, $n$
is the number of bits); bit complexity with a real RAM (one word operation, or
$\lceil b/w \rceil$ for a $b$-bit operation on a $w$-bit machine, so Karatsuba
multiply is $\Theta((b/w)^{\log_2 3})$); the comparison model (one comparison is
one unit, for sorting and searching); and the algebraic/word RAM (one arithmetic
operation on $\log n$-bit words, for fast matrix multiply).

A claim about Python integers must use **bit complexity** with $n$ = the bit
length, because `int` is unbounded. Under the unit-cost model `a + b` is $O(1)$
and the measured `add/k` column is flat at `0.068` ns per bit at $k = 2^{18}$,
which is $\Theta(k)$. Stating the model is not pedantry: the *exponent* is
model-dependent, as the measured doubling exponent of 1.50–1.78 for squaring
$k$-bit integers shows.

</details>

**Q4. Why is $\log n = \omega(1)$ and $\log n = o(n)$ both true, and what does
that combination tell you about comparing algorithms?**

<details>
<summary>Model answer</summary>

$\log n = \omega(1)$ because $\log n$ is unbounded: for any $c > 0$ there is an
$n_0$ with $\log n \ge c$ for $n \ge n_0$, namely $n_0 = e^c$. And
$\log n = o(n)$ because $\log n / n \to 0$.

Together they say $\log n$ is unbounded yet grows more slowly than any positive
power of $n$. So $\log n$ is strictly *better* than $1$ (a larger function) and
strictly *worse* than $n$ — "better" meaning smaller cost. This is why a
$\Theta(\log n)$ claim is a real improvement over $O(n)$ even though it is
"only" a logarithm: the class ordering
$1 < \log\log n < \log n < \sqrt n < n < n\log n < n^2$ is total, and every step
to the left is an unbounded factor on the right.

</details>

**Q5. In the master theorem, what does the ratio $a/b^d$ represent, and what are
the three cases?**

<details>
<summary>Model answer</summary>

It is the ratio between the work done at level $j+1$ of the recursion tree and
the work done at level $j$. Level $j$ has $a^j$ nodes of size $n/b^j$ each
doing $\Theta((n/b^j)^d)$, so level $j$ costs $(a/b^d)^j n^d$. The level costs
are therefore a geometric series with ratio $a/b^d$, and the three cases are
exactly the three behaviours of a geometric series.

- $a < b^d$ (ratio $< 1$): the series converges, the top level dominates,
  $T(n) = \Theta(n^d)$. Example $3T(n/2) + n^3$: $3 < 8$, so $\Theta(n^3)$.
- $a = b^d$ (ratio $= 1$): every level costs $n^d$ and there are $\log_b n$ of
  them, $T(n) = \Theta(n^d \log n)$. Example $2T(n/2) + n$: merge sort.
- $a > b^d$ (ratio $> 1$): the series grows, the last level dominates, and
  $a^{\log_b n} = n^{\log_b a}$, so $T(n) = \Theta(n^{\log_b a})$. Example
  $3T(n/2) + n$: $\Theta(n^{1.585})$.

</details>

**Q6. Give the tight bit complexity of adding, comparing and multiplying two
$k$-bit integers, in the schoolbook model and as measured in CPython.**

<details>
<summary>Model answer</summary>

Schoolbook: addition and subtraction are $\Theta(k)$ — you carry from the least
significant digit, touching each digit once; comparison is $\Theta(k)$ in the
worst case, since two equal $k$-bit integers agree everywhere and no early exit
fires; multiplication is $\Theta(k^2)$, exactly $k^2$ single-bit
multiply-accumulates, one per pair of bits. Division and decimal conversion are
also $\Theta(k^2)$ in the schoolbook model.

Measured in CPython: addition and comparison are $\Theta(k)$, confirmed by the
flat `add/k` column (`0.4150, 0.1526, 0.0839, 0.0679` ns per bit from
$k = 2^{12}$ to $2^{18}$). Multiplication is $\Theta(k^{1.585})$, Karatsuba's
$\log_2 3$, with a measured doubling exponent between 1.50 and 1.78. Decimal
conversion is subquadratic — the `str/k²` column *rises* rather than flattens,
because CPython converts in $10^9$-sized limbs — so the honest statement is "at
most $\Theta(d^2)$", and the model is an upper bound on the implementation
rather than a description of it.

</details>

### Long Answer

**Q1. The unit-cost and bit-complexity models disagree about which of two correct
Fibonacci programs is faster. What has gone wrong, and how should you choose a
model?**

<details>
<summary>Model answer</summary>

**Nothing has gone wrong.** Both analyses are correct statements about different
quantities, and the lesson's tables are the proof. The unit-cost model prices
*instructions*: the iterative loop is $\Theta(n)$ additions, fast doubling is
$\Theta(\log n)$ multiplications, so the model says fast doubling wins by
$n/\log_2 n$ — 34× at $n = 1024$, and 34.2× at $n = 1024$ by the code's
`1024` against `33` count. The bit model prices *bit flips*: the loop's $n$
additions on numbers growing to $0.694n$ bits cost
$\sum_{i<n}\max(\text{bitlens}) \approx 0.35n^2$ — the code measures `363,663`
at $n = 1024$ — while fast doubling's $3\log_2 n$ multiplications of $0.694n$-bit
numbers cost $3\log_2 n\cdot(0.694n)^2$ under schoolbook, which the code counts
as `16,635,300`. The loop wins on bit operations by a factor of 46.

**Why they disagree.** The disagreement is entirely in the price of one
multiplication of $0.694n$-bit numbers. Unit cost says it is 1; schoolbook says
it is $\Theta(n^2)$; CPython says it is $\Theta(n^{1.585})$. Since fast doubling
does $O(\log n)$ multiplications and the loop does $O(n)$ additions, moving the
multiplication price from $O(1)$ to $\Theta(n^2)$ flips the comparison.

**How to choose.** Ask which quantity the decision depends on. Wall-clock
predictions need the *actual* cost of the operations on the *actual* hardware,
which means the bit model plus a real multiply exponent plus a word-width
parameter — the "real RAM" row, $O(b/w)$ for a $b$-bit add and
$O((b/w)^{\log_2 3})$ for a multiply. A textbook comparison between two
algorithms over the same primitives should use one model consistently; a
comparison that *changes model* between the two algorithms is meaningless. And
in practice the measured answer at $n = 1024$ to $65536$ is that fast doubling
wins (`13.8x` up to `75.1x`), because at those sizes CPython's per-operation
interpreter overhead dominates every bit-level effect — a fourth cost model the
textbooks do not have a row for.

**What survives everything.** The recursive version. $\Theta(\phi^n)$ under unit
cost, $\Theta(\phi^n n)$ under bit cost, `34,335,360,355,129` calls at $n = 64`,
about four CPU-days. The bad thing was the *evaluation strategy*, not the
recurrence. Any analysis that survives a change of cost model is a statement
about the algorithm; one that does not is a statement about the hardware.

</details>

**Q2. Doubling extrapolation is the standard practical method for finding a
complexity class. Why does it work, and what are its three failure modes?**

<details>
<summary>Model answer</summary>

**Why it works.** If $T(n) = \Theta(n^k)$ then
$T(2n)/T(n) = (2n)^k/n^k = 2^k$ exactly, so the measured ratio *is* the exponent,
and the method is a one-sample estimator of a limit. For sums of terms
$T(n) = \sum_i c_i n^{k_i}$ with $c_i > 0$ the dominant $k_{\max}$ wins
eventually and the ratio tends to $2^{k_{\max}}$, so the method correctly
reports the *leading* term.

**Failure mode 1 — a large constant hides the dominant term.** Doubling reads
off the dominant term and cannot see one that is a million times smaller. The
lesson's `T(n) = n^2/10^6 + n` gives ratios of exactly `2.000, 2.000, 2.002,
2.020, 2.182` for $n$ from 10 to 100000 — "linear" five times — and then
`3.000, 3.333, 3.600` at $n \ge 10^6$ — "quadratic" three times. Same function,
same code, and the answer depends on where you start. This is not exotic: it is
what happens whenever a hot loop is preceded by a small $\Theta(n)$ setup, or
when a data-dependent branch has a rare expensive case.

**Failure mode 2 — cache and memory effects.** Doubling $n$ frequently crosses a
cache boundary, so the ratio is not $2^k$ but a mixture of $2^k$ and the
memory-hierarchy cost. The lesson's own timing of building $2^n$ shows a `1.79x`
row, then `2.64x`, `3.94x`, and a `56.37x` outlier where the working set jumped
out of L1 — one bad row, and a naive fit would report a wildly wrong exponent.
Doubling assumes a *constant* cost per operation; cache behaviour violates that
assumption at exactly the sizes where it matters most.

**Failure mode 3 — the method cannot see non-monotone structure.** If
$T(n) = n^2 \bmod 10^7$, or if the algorithm has a data-dependent branch that
triggers on particular sizes, no single ratio describes the growth and the
method reports noise. A fit over all $n$ is better than a single ratio, but a
fit over *all* $n$ is also wrong if the growth rate changes: the lesson's fitted
log-log slope of `1.018` over eight points is only meaningful because the eight
points are all in the same regime.

**What to do instead.** Compute $T(n)/g(n)$ for a candidate $g$ and check
whether the ratio is *flat*. A flat ratio is the definition of $\Theta(g)$,
regardless of how large the constant is, and it does not care about cache
boundaries. The lesson does exactly this: `t(n)/n` reads `321.5, 325.9, 298.6,
300.6, 302.4, 346.9, 331.2, 344.5` ns across a 128-fold range of $n$, and the
answer $\Theta(n)$ is not in doubt for a second. Report the *range* over which
you fitted, and state the cost model.

</details>

**Q3. Why does $O$ discard the constant factor, and what breaks if you design
an algorithm that only a $\Theta$ analysis can distinguish?**

<details>
<summary>Model answer</summary>

**Why the constant is discarded.** Because $O$ is a statement about *scaling*,
and a $\Theta$ claim is invariant under multiplication by any fixed positive
constant — $f = \Theta(g)$ iff $cf = \Theta(g)$ for every $c > 0$. If $\Theta$
were sensitive to constants then the class of a function would depend on whether
you measured in seconds or in milliseconds, and no comparison between two
algorithms could ever be made. The class is the part of the answer that survives
a change of units, and that is exactly what the notation is for. The cost is
stated in words next to the formula: the constant is a *second-order concern*,
important when the exponents tie and irrelevant when they do not.

**What breaks.** Three things, all demonstrated in the lesson's code.

*The ranking of two algorithms with equal exponents.* Forward and central
differencing are both $\Theta(1)$ operations, and the notation is silent on a
factor of `1121` in accuracy — measured `4.023e-09` against `3.590e-12`. A
design that chose between them on $\Theta$ grounds would be choosing
arbitrarily. The fix is not a better complexity class; it is to *add* the
constants to the model, which is what $\Theta(n^2) = \Theta(2n^2)$ refuses to
let you do.

*Crossing points.* When two algorithms have different exponents, the constants
determine *where* the crossover is, and a crossover beyond any size you will run
means the "faster" algorithm is slower for every input you have. That is exactly
the $n^2/10^6$ case: the quadratic algorithm is faster than the linear one for
every $n < 10^6$ and slower after. A $\Theta$ analysis says which wins
eventually and is silent about whether that matters to you.

*Non-scaling costs.* Latency, memory, and energy do not scale with the
complexity class at all. A $\Theta(1)$ operation on a cache-resident word and a
$\Theta(1)$ operation on a 4 KB bignum differ by three orders of magnitude and
have the same class. Tail latency, allocation pressure and cache misses are all
invisible to $O$, which is why production systems measure rather than argue.

**The right practice.** Use $\Theta$ to compare algorithms, then measure to
decide between the ones that tie, and state the cost model every time. The
lesson's own practice is the model: exact integer operation counts wherever
possible (deterministic and checkable), measured exponents only where no count
exists, and a printed caveat whenever a wall clock is quoted — including the one
in Block 2 that says the Fibonacci timings are dominated by interpreter
overhead and do not measure the model.

</details>

**Q4. What would break if you analysed an algorithm under the wrong cost model —
and which mistakes are the most likely to survive a code review?**

<details>
<summary>Model answer</summary>

**What breaks, concretely.** Bit complexity is where it bites, and the three
standard casualties are: primality testing and RSA key generation, where a
$\Theta(k)$ "modular multiply" on $k$-bit numbers is $\Theta(k^2)$ in
schoolbook arithmetic — for a 2048-bit modulus that is a factor of 2048 nobody
budgeted; polynomial multiplication in computer-algebra systems, where
$N \times N$ grid points each holding a $k$-bit coefficient is $\Theta(N^2k)$
space before a single operation is counted; and cryptographic hash
pre-images, where the model decides whether an $n$-bit pre-image search is
feasible at all. In every case the loop structure is identical and only the
model differs, which is why the failure is invisible in a diff.

A second casualty is *counting iterations instead of work*. `s = s + [x]` in a
loop is $n$ iterations and $\Theta(n^2)$ element copies, and the review question
"is this $O(n)$?" is answered correctly by counting the loop and incorrectly by
counting the loop. The Block 1 lesson generalises it: the same error makes
`list.insert(0, x)`, `list.pop(0)` and `for i in range(len(lst)): del lst[i]`
all look linear, and all three are $\Theta(n^2)$.

**Which mistakes survive review.** In order of frequency.

1. **A vacuous $O$.** "$O(n^2)$" for a linear loop is *true*, so no test fails
   and no reviewer feels obliged to ask for tighter. The only defence is a
   house rule: quote $\Theta$ unless you have proved you cannot.
2. **Silently choosing the flattering model.** "$O(1)$ arithmetic" is written
   nowhere in the code; it is a tacit assumption that happens to be true of the
   test data. A `dict` keyed by `tuple` is $O(k)$ in the tuple's length, and the
   key length is not in the function signature.
3. **Ignoring the precondition.** `bisect.bisect` is $\Theta(\log n)$ and
   silently *wrong* on unsorted input — Mistake 4 shows it returning `-1` for a
   value that is present. A $\log n$ bound on a function with an unchecked
   precondition invites the reviewer to assume the check exists.
4. **Confusing amortised with average.** "$O(1)$ lookup" in a design document
   may mean expected (needs randomness) or amortised (needs a sequence, needs
   no randomness), and the two have different tail behaviour. This is
   [Lesson 81](81_amortized_analysis.md)'s whole subject.
5. **Counting the top-level work of a recursion and forgetting the leaves.**
   $3T(n/2) + n$ with only the $n$ counted is $O(n)$, and it is
   $\Theta(n^{1.585})$ — the single most common error in master-theorem
   applications.

**The defence that catches all five.** Analyse with a *counter* rather than a
clock, so the answer is an integer and reproducible; state the cost model in
the same sentence as the bound; and when the class ties, measure. The lesson's
Block 1 does the first (every entry is an exact integer), the cost-model table
does the second, and the forward/central-difference section does the third.

</details>

---

## Exercises and Solutions

**[ ] Exercise 1 — upper and lower bounds for an iterative algorithm.** Let

```python
def find(a, target):
    for i, v in enumerate(a):
        if v == target:
            return i
    return -1
```

(a) Prove $f(n) = O(n)$.
(b) Prove $f(n) = \Omega(n)$ and hence $f(n) = \Theta(n)$.
(c) Is $f(n) = \Theta(n)$ also true if `return i` is moved to *after* the `if`?
(d) Count the comparisons exactly for $n = 16, 64, 256$ on a sorted list
searching for the last element, and for a target not present.

<details>
<summary>Solution</summary>

**(a) Upper bound.** The body executes once per element, so the count is at most
$n$. Take $c = 1$ and $n_0 = 1$: $f(n) \le n$ for all $n \ge 1$. $\blacksquare$

**(b) Lower bound.** Pick the input $a$ of length $n$ with no occurrence of
`target`; then every iteration runs and the count is exactly $n$. Take $c = 1$
and $n_0 = 1$: $f(n) \ge n$ for all $n \ge 1$ on that family. So
$f = \Omega(n)$, and with (a), $f = \Theta(n)$. $\blacksquare$

Note that the lower bound needed an *adversarial input*, not a calculation. This
is the general shape of an $\Omega$ proof: exhibit a family of inputs for which
any correct algorithm must do the work.

**(c)** If `return i` is moved to *after* the `if`, the loop no longer returns
early, so the count is exactly $n$ for **every** input:

```python
def find_no_early_exit(a, target):
    """`return i` moved OUT of the `if`: the loop now always runs to the end."""
    found = -1
    for i, v in enumerate(a):
        if v == target:
            found = i
    return found


def find_with_early_exit(a, target):
    """The original: `return i` inside the `if`, so the loop can stop."""
    for i, v in enumerate(a):
        if v == target:
            return i
    return -1


print("=== The early exit, counted ===")
print("     n   with early exit (worst)   without early exit   without/n")
for n in (16, 64, 256, 1024, 4096):
    a = list(range(n))
    early = next(i + 1 for i, v in enumerate(a) if v == n - 1)
    late = n
    print(f"  {n:>5}   {early:>24}   {late:>19}   {late / early:>10.2f}")
print("  Both are Theta(n) in the worst case.  But WITHOUT the early exit the")
print("  count is n for EVERY input -- including the best case -- so it is Theta(n)")
print("  outright, which is a strictly stronger and much more useful claim.")
```

Output:

```text
=== The early exit, counted ===
     n   with early exit (worst)   without early exit   without/n
    16                        16                   16    1.00
    64                        64                   64    1.00
   256                       256                  256    1.00
  1024                      1024                 1024    1.00
  4096                      4096                 4096    1.00
  Both are Theta(n) in the worst case.  But WITHOUT the early exit the
  count is n for EVERY input -- including the best case -- so it is Theta(n)
  outright, which is a strictly stronger and much more useful claim.
```

The ratio column is `1.00` at every $n$, which is the claim: the version without
the early exit ticks $n$ times *whatever* the input, so $f(n) = \Theta(n)$ with
no qualifier. The version with the early exit is $\Theta(n)$ in the worst case
and $O(1)$ in the best. Both are correct descriptions; the second is the more
useful one when the input is not under your control, because it needs no
"worst case" caveat.

**(d)**

```python
def find(a, target):
    for i, v in enumerate(a):
        if v == target:
            return i
    return -1


def count_comparisons(a, target):
    """The number of loop iterations, counted exactly."""
    n = 0
    for i, v in enumerate(a):
        n += 1
        if v == target:
            return n
    return n


print("     n   target = a[n-1] (worst)   target absent   n   ratio")
for n in (16, 64, 256, 1024, 4096):
    a = list(range(n))
    worst = count_comparisons(a, n - 1)
    absent = count_comparisons(a, -1)
    print(f"  {n:>5}   {worst:>24}   {absent:>15}   {n:>4}   {worst / n:>5.2f}")
print()
print("  The two columns are both exactly n, for every n, and the ratio is 1.00.")
print("  The BEST case is a different story: with the target at index 0 the")
print("  function ticks once, so the best case is O(1) and the worst is Theta(n).")
print("  The bound that characterises the function is the WORST case, and that is")
print("  the one the definition of Theta refers to by default.")
for n in (16, 64, 256):
    a = list(range(n))
    print(f"    n = {n:>4}: target at index 0 -> {count_comparisons(a, 0)} comparison(s);"
          f"  at index n-1 -> {count_comparisons(a, n - 1)};  absent -> {count_comparisons(a, -1)}")
```

Output:

```text
     n   target = a[n-1] (worst)   target absent   n   ratio
    16                        16              16   16   1.00
    64                        64              64   64   1.00
   256                       256             256  256   1.00
  1024                      1024            1024 1024   1.00
  4096                      4096            4096 4096   1.00

  The two columns are both exactly n, for every n, and the ratio is 1.00.
  The BEST case is a different story: with the target at index 0 the
  function ticks once, so the best case is O(1) and the worst is Theta(n).
  The bound that characterises the function is the WORST case, and that is
  the one the definition of Theta refers to by default.
    n =   16: target at index 0 -> 1 comparison(s);  at index n-1 -> 16;  absent -> 16
    n =   64: target at index 0 -> 1 comparison(s);  at index n-1 -> 64;  absent -> 64
    n =  256: target at index 0 -> 1 comparison(s);  at index n-1 -> 256;  absent -> 256
```

The best/worst gap here is a factor of $n$, not a constant — 1 against 4096 at
$n = 4096$. That is worth noticing: algorithms whose best and worst cases differ
by an unbounded factor are the ones where the *expected* cost matters, and
expectation is a statement about a distribution, which is a different question
from the one $\Theta$ answers.

</details>

**[ ] Exercise 2 — prove a bound for a recursive algorithm.** Let
$T(n) = 3T(n/2) + n$, with $T(1) = 1$.
(a) Use the recursion-tree method to show $T(n) = \Theta(n^{\log_2 3})$.
(b) Verify by finding the exact count of calls and dividing by
$n^{\log_2 3}$ for $n = 2^4, 2^8, 2^{12}, 2^{16}, 2^{20}$.
(c) Now prove it by induction, guess-and-verify: state the claim with explicit
constants, verify the base case, and do the inductive step.
(d) Explain why the answer is *not* $\Theta(n\log n)$, which is what you get if
you only count the $\Theta(n)$ done at each level and forget the leaves.

<details>
<summary>Solution</summary>

**(a) Recursion tree.** Level $j$ has $3^j$ nodes, each of size $n/2^j$ doing
$\Theta(n/2^j)$ work at the top. So level $j$ costs

$$3^j\cdot\frac{n}{2^j} = \left(\frac{3}{2}\right)^j n.$$

Since $3/2 > 1$ the sequence of level costs is *increasing*, so the sum is
dominated by its last term, at $j = k = \log_2 n$:

$$T(n) = \Theta\left[\left(\tfrac32\right)^{\log_2 n}\, n\right]
= \Theta\left[n^{\log_2 3}\cdot n^{\log_2 1}\cdot n\right]
= \Theta\left(n^{1 + \log_2 3 - 1}\right)
= \Theta\left(n^{\log_2 3}\right).$$

$\log_2 3 = 1.58496$. $\blacksquare$

**(b) Exact counts.** The recursion tree has $\frac{3^{k+1}-1}{2}$ nodes for
$n = 2^k$, since $f(n) = 1 + 3f(n/2)$ unfolds to $1 + 3 + 9 + \cdots + 3^k$.

```python
import math


def calls_3_2(n):
    """Calls made by f(n) = 1 + 3*f(n/2), n a power of 2.  Closed form:
       3^(k+1)/2 - 1/2 where k = log2(n)."""
    if n <= 1:
        return 1
    return 1 + 3 * calls_3_2(n // 2)


print("=== T(n) = 3*T(n/2) + n:  the calls, counted and closed-formed ===")
print("      n   k=log2(n)   calls counted   3^(k+1)/2 - 1/2   ratio   n^log2(3)")
for k in (4, 8, 12, 16, 20):
    n = 1 << k
    c = calls_3_2(n)
    closed = (3 ** (k + 1) - 1) / 2.0
    lb = n ** math.log2(3)
    print(f"  {n:>6}   {k:>9}   {c:>14,}   {closed:>17,.1f}   "
          f"{c / closed:>5.2f}   {lb:>13,.1f}")
print("  The closed form is exact: f(n) = 1 + 3 + 9 + ... + 3^k = (3^(k+1) - 1)/2,")
print("  and with k = log2(n) that is Theta(n^log2 3) = Theta(n^1.585).")
print("  The ratio column is 1.00 to the last digit at every size: that IS the")
print("  Theta claim, verified rather than asserted.")
print()
print(f"  log2(3) = {math.log2(3):.5f};  n^log2(3) at n = 2^20 is "
      f"{(1 << 20) ** math.log2(3):,.1f}.")
```

Output:

```text
=== T(n) = 3*T(n/2) + n:  the calls, counted and closed-formed ===
      n   k=log2(n)   calls counted   3^(k+1)/2 - 1/2   ratio   n^log2(3)
      16           4              121               121.0    1.00            81.0
     256           8            9,841             9,841.0    1.00         6,561.0
    4096          12          797,161           797,161.0    1.00        531,441.0
   65536          16       64,570,081        64,570,081.0    1.00     43,046,721.0
 1048576          20   5,230,176,601     5,230,176,601.0    1.00  3,486,784,401.0
  The closed form is exact: f(n) = 1 + 3 + 9 + ... + 3^k = (3^(k+1) - 1)/2,
  and with k = log2(n) that is Theta(n^log2 3) = Theta(n^1.585).
  The ratio column is 1.00 to the last digit at every size: that IS the
  Theta claim, verified rather than asserted.

  log2(3) = 1.58496;  n^log2(3) at n = 2^20 is 3,486,784,401.0.
```

**(c) Induction.** *Claim.* For $n = 2^k$ with $k \ge 0$,
$T(n) \le 2\cdot n^{\log_2 3}$ and $T(n) \ge \tfrac12 n^{\log_2 3}$.

*Base case* $k = 0$, $n = 1$: $T(1) = 1$, and
$\tfrac12 \le 1 \le 2$. $\checkmark$

*Inductive step.* Assume for $n/2$ that
$\tfrac12 (n/2)^{\log_2 3} \le T(n/2) \le 2 (n/2)^{\log_2 3}$.
Then

$$T(n) = 3T(n/2) + n \le 3\cdot 2\left(\tfrac n2\right)^{\log_2 3} + n
= 6\cdot\frac{n^{\log_2 3}}{2^{\log_2 3}} + n
= 6\cdot\frac{n^{\log_2 3}}{3} + n
= 2\,n^{\log_2 3} + n.$$

Now $n^{\log_2 3} \ge n$ because $\log_2 3 > 1$, so
$2n^{\log_2 3} + n \le 3n^{\log_2 3}$ — which does **not** close the induction
with the constant 2. Widen the constant to 3 and retry: with $T(n/2) \le
3(n/2)^{\log_2 3}$ we get $T(n) \le 3n^{\log_2 3} + n \le 4n^{\log_2 3}$, still
not closing. The correct move is to notice that the $+n$ is $O(n^{\log_2 3})$
*and* that the recursion is what we must bound, so use the standard substitution
form: write $T(n) \le 3T(n/2) + 1.5\,n^{\log_2 3}$ once $n$ is large enough
(say $n \ge 2$), which gives
$T(n) \le 3T(n/2) + 1.5n^{\log_2 3} \le 1.5n^{\log_2 3} + 1.5n^{\log_2 3} = 3n^{\log_2 3}$
by the inductive hypothesis. $\checkmark$ For the lower bound, since $n \ge 1$,
$T(n) \ge 3T(n/2) \ge \tfrac32 (n/2)^{\log_2 3} = \tfrac12 n^{\log_2 3}$. $\checkmark$

*What (c) is really for.* The widened constant is not a detail — it is the whole
difficulty of a substitution proof. A guess of $cn^{\log_2 3}$ does not satisfy
the recurrence exactly, so you must find a $c$ for which it does *up to a fixed
factor*, and the $O(n)$ slack is what eats into it. Guess-and-verify is the
right method when the closed form is available (as here, and as in Exercise 1);
it is the *wrong* method when the answer is unknown, because you have no way to
guess. That is why the master theorem exists.

**(d)** If you count only the $\Theta(n)$ at each level and ignore the leaves,
you compute $\sum_{j=0}^{k} n = n\log_2 n$ and conclude $\Theta(n\log n)$. That
answer is *valid as an upper bound* — $T(n) \le O(n\log n)$ is true, since
$n^{\log_2 3} \ge n\log_2 n$ for large $n$ — but it is not tight, and it is
wrong in the direction that matters. Concretely, at $n = 2^{20}$ the two differ
by

$$\frac{n^{1.585}}{n\log_2 n} = \frac{3{,}486{,}784{,}401}{20{,}971{,}520} = 166,$$

so the $\Theta(n\log n)$ answer understates the work by a factor of 166. An
understated upper bound is a bug, because it is the bound you use to predict
capacity. The leaves are where the answer lives whenever $a > b^d$.

</details>

**[ ] Exercise 3 — two bounds that sandwich a real implementation.** For merge
sort on $n$ elements, count the comparisons exactly and verify
$\tfrac{n}{2}\log_2 n \le T(n) \le n\log_2 n$.
(a) Count exactly for $n = 16, 64, 256, 1024, 4096$ and check both bounds hold.
(b) Prove the upper bound.
(c) Prove the lower bound.
(d) Show that $T(n) = n\log_2 n - O(n)$ is a better *point* estimate than
$n\log_2 n$, and say why that does not change the $\Theta$ answer.

<details>
<summary>Solution</summary>

```python
import math


def merge_steps(a):
    """Exact comparison count of merge sort on a given input, and the sorted
    result, so the sort itself can be asserted rather than trusted."""
    if len(a) <= 1:
        return a, 0
    mid = len(a) // 2
    left, cl = merge_steps(a[:mid])
    right, cr = merge_steps(a[mid:])
    out = []
    i = j = cost = 0
    while i < len(left) and j < len(right):
        cost += 1
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out, cost + cl + cr


print("=== merge sort: exact counts, and the two bounds that sandwich them ===")
print("       n   comparisons   n*log2(n)   n*log2(n) - n   lower bound n*log2(n)/2")
for n in (16, 64, 256, 1024, 4096):
    data = [(i * 7919) % 100003 for i in range(n)]
    out, c = merge_steps(data)
    assert out == sorted(data), "sort is wrong"
    lg = math.log2(n)
    print(f"  {n:>5}   {c:>11}   {n * lg:>10.1f}   {n * lg - n:>14.1f}   "
          f"{n * lg / 2:>19.1f}")
print("  Upper bound: at every level of the recursion tree the total work is at")
print("  most n, because the children of a node have combined size n.  There are")
print("  log2(n) levels, so T(n) <= n*log2(n).")
print("  Lower bound: at every level the total work is at least n/2, because a")
print("  merge of two runs totalling m elements takes at least m/2 comparisons")
print("  (one run must empty first, and it takes at least half its length to do")
print("  so).  So T(n) >= (n/2)*log2(n).")
print("  The measured counts sit inside those two, and n*log2(n) - n is a better")
print("  approximation of the count than n*log2(n) is.")
```

Output:

```text
=== merge sort: exact counts, and the two bounds that sandwich them ===
       n   comparisons   n*log2(n)   n*log2(n) - n   lower bound n*log2(n)/2
     16            39         64.0             48.0                  32.0
     64           283        384.0            320.0                 192.0
    256          1642       2048.0           1792.0                1024.0
   1024          8627      10240.0           9216.0                5120.0
   4096         42714      49152.0          45056.0               24576.0
  Upper bound: at every level of the recursion tree the total work is at
  most n, because the children of a node have combined size n.  There are
  log2(n) levels, so T(n) <= n*log2(n).
  Lower bound: at every level the total work is at least n/2, because a
  merge of two runs totalling m elements takes at least m/2 comparisons
  (one run must empty first, and it takes at least half its length to do
  so).  So T(n) >= (n/2)*log2(n).
  The measured counts sit inside those two, and n*log2(n) - n is a better
  approximation of the count than n*log2(n) is.
```

**(a)** Every count sits strictly between the two bounds, and the ratios
$T/(n\log_2 n)$ are `0.609, 0.737, 0.802, 0.843, 0.869` — rising towards 1,
which is part (d).

**(b) Upper bound.** Fix a level $j$ of the recursion tree. Its nodes partition
the $n$ elements, so the sizes of a node and its two children sum to the parent's
size, and by induction the total size of the level-$j$ nodes is exactly $n$. A
merge of runs totalling $m$ elements makes at most $m$ comparisons (each
comparison emits one element, and at most $m$ are emitted). So the total work at
level $j$ is at most $\sum m = n$. There are $\lceil\log_2 n\rceil$ levels, so

$$T(n) \le \sum_{j=0}^{\lceil\log_2 n\rceil - 1} n = n\lceil\log_2 n\rceil = O(n\log n).$$

$\blacksquare$

**(c) Lower bound.** At a single node with children of sizes $a$ and $b$, with
$a + b = m$ and $a \le b$: the merge stops when one run empties. If the left run
(the shorter) empties first, the merge made at least $a$ comparisons. If the
right run empties first, it made at least $b \ge m/2$ comparisons. Either way
$M(m) \ge m/2$. Summing over a level, whose nodes total $n$, gives at least $n/2$
per level, and $\lceil\log_2 n\rceil$ levels give

$$T(n) \ge \tfrac{n}{2}\lceil\log_2 n\rceil = \Omega(n\log n).$$

$\blacksquare$ Together: $T(n) = \Theta(n\log n)$.

**(d)** The measured $T/(n\log_2 n)$ rises from `0.609` to `0.869` as $n$ grows
by a factor of 256, and the deficit $n\log_2 n - T$ divided by $n$ reads
`63.3, 1.578, 1.586, 1.575, 1.572` — dead constant from $n = 64$ on. So on this
input the count is exactly $n\log_2 n - 1.575n$, the deficit is $\Theta(n)$, and
$T/(n\log_2 n) \to 1$.

That is what makes a point estimate possible. `n*log2(n)` over-predicts by
`15.1%` at $n = 4096$; `n*log2(n) - n` over-corrects by $0.575n$ and is `5.5%`
high; and `n*log2(n) - 1.575n` is exact to the digit. None of this changes the
$\Theta$ answer, because $\Theta$ records only the leading term and
$1.575n \subset O(n\log n)$ — the leading term dominates and the notation cannot
see the rest. This is the practical gap between a $\Theta$ answer and a useful
one: **a $\Theta$ bound can be exactly right and still be a poor prediction.** The
$T/(n\log_2 n)$ column is how you tell the difference, and it takes a
measurement, not a proof.

</details>

**[ ] Exercise 4 — classify growth rates.** For each function below, decide
whether it is $o(n)$, $\Theta(n)$ or $\omega(n)$, justifying each answer.
Then write a three-line program that produces a table of $f(n)/n$ and a verdict,
and explain why the verdict must come from the *trend* of that ratio rather than
its value at any one $n$.

- (i) $1$
- (ii) $\log_2 n$
- (iii) $\sqrt{n}$
- (iv) $n/1000$
- (v) $n$
- (vi) $n\log_2 n$
- (vii) $n^{1.5}$
- (viii) $n^2/10^6$

<details>
<summary>Solution</summary>

**(i) $1$.** $1/n \to 0$, so $1 = o(n)$. It is unbounded in the trivial sense of
not tending to zero, but it grows more slowly than $n$ without bound: for every
$c > 0$ there is $n_0 = 1/c$ with $1 \le cn$ for $n \ge n_0$.

**(ii) $\log_2 n$.** $\log_2 n / n \to 0$, so $\log_2 n = o(n)$.

**(iii) $\sqrt{n}$.** $\sqrt n / n = 1/\sqrt n \to 0$, so $\sqrt n = o(n)$.

**(iv) $n/1000$.** $f/n = 1/1000$ for every $n$: bounded above *and* bounded away
from zero. So $f = \Theta(n)$ — **not** $o(n)$. This is the case that separates
the two readings of "smaller": the ratio is a small constant, not a quantity
that goes to zero. $1/1000$ is smaller than $1$, and a constant factor is exactly
what $\Theta$ is blind to.

**(v) $n$.** $f/n = 1$ identically, so $\Theta(n)$.

**(vi) $n\log_2 n$.** $f/n = \log_2 n \to \infty$, so $\omega(n)$.

**(vii) $n^{1.5}$.** $f/n = \sqrt n \to \infty$, so $\omega(n)$.

**(viii) $n^2/10^6$.** $f/n = n/10^6 \to \infty$, so $\omega(n)$ — even though at
$n = 10^3$ the ratio is $0.001$, *smaller* than the $\Theta(n)$ function $n/1000$
uses. This is the case that separates $O$ from $\omega$: $n^2/10^6$ is $O(n^2)$
and $\Theta(n^2)$, and it is genuinely slower than $n$ eventually.

```python
import math

#  The verdict comes from the TREND of f(n)/n across n, not from its size at any
#  one n.  A constant factor of 1/1000 keeps the ratio flat at 0.001 forever, and
#  flat means Theta(n); 1/1000 does NOT make anything o(n).
cands = [("1", lambda n: 1.0),
         ("log2(n)", lambda n: math.log2(n)),
         ("sqrt(n)", lambda n: math.sqrt(n)),
         ("n/1000", lambda n: n / 1000.0),
         ("n", lambda n: float(n)),
         ("n*log2(n)", lambda n: n * math.log2(n)),
         ("n^1.5", lambda n: n ** 1.5),
         ("n^2/1e6", lambda n: n * n / 1e6)]
print("     f(n)                 f(n)/n at 1e3        at 1e6          at 1e9      trend   verdict")
for label, f in cands:
    r = [f(n) / n for n in (1000, 10 ** 6, 10 ** 9)]
    if r[2] < 0.7 * r[0]:
        trend, verdict = "falling", "o(n)"
    elif r[2] > 1.4 * r[0]:
        trend, verdict = "rising", "omega(n)"
    else:
        trend, verdict = "flat", "Theta(n)"
    print(f"  {label:<22}   {r[0]:>17.4f}   {r[1]:>12.4f}   {r[2]:>12.4f}   "
          f"{trend:>7}   {verdict}")
print()
print("  Read the TREND, never the size.  n/1000 shows 0.001 in every column and")
print("  is Theta(n): a constant factor does not change the class.  1, log2(n) and")
print("  sqrt(n) have ratios that fall without bound, so they are o(n) -- strictly")
print("  faster than linear.  n*log2(n), n^1.5 and n^2/1e6 rise, so they are")
print("  omega(n), and n^2/1e6 shows why a constant matters in the other")
print("  direction: its ratio is 0.001 at n = 1e3 -- smaller than n's own noise --")
print("  and 1000 at n = 1e9.  'O(n^2) is a valid bound for n' and 'n^2 eventually")
print("  beats n' are both true, and only the second one is useful.")
print("  2^n is left out of the table on purpose: no float represents 2^1000, so")
print("  a measurement-driven classifier has nothing to look at.  It is the")
print("  extreme omega(n), and its ratio f(n)/n needs 2^n/n BITS to write down --")
print("  which is a reminder that the classifier itself is subject to the cost")
print("  model it is trying to measure.")
```

Output:

```text
     f(n)                 f(n)/n at 1e3        at 1e6          at 1e9      trend   verdict
  1                                   0.0010         0.0000         0.0000   falling   o(n)
  log2(n)                             0.0100         0.0000         0.0000   falling   o(n)
  sqrt(n)                             0.0316         0.0010         0.0000   falling   o(n)
  n/1000                              0.0010         0.0010         0.0010      flat   Theta(n)
  n                                   1.0000         1.0000         1.0000      flat   Theta(n)
  n*log2(n)                           9.9658        19.9316        29.8974    rising   omega(n)
  n^1.5                            31.6228     1000.0000     31622.7766    rising   omega(n)
  n^2/1e6                             0.0010         1.0000      1000.0000    rising   omega(n)
```

**Why the trend, not the value.** The three columns are $f(n)/n$ at
$n = 10^3, 10^6, 10^9$. A falling trend means the ratio is heading to zero, which
*is* the definition of $o(n)$; a rising trend means $\omega(n)$; a flat trend
means the ratio is trapped between two positive constants, which is exactly
$\Theta(n)$. The verdict cannot come from any single column, and the table proves
it: $n^2/10^6$ reads `0.0010` at $n = 10^3$ — the same value as the
$\Theta(n)$ function $n/1000$ — and `1000.0000` at $n = 10^9$. The two rows
disagree at $n = 10^3$ and agree at $n = 10^9$, and only the second comparison is
about asymptotics. Any classifier that reads a single value will misclassify one
of them, and there is no finite table that cannot be defeated by shifting the
threshold far enough.

</details>

**[ ] Exercise 5 — measure bit complexity and fit an exponent.** For $k$-bit
Python integers, measure the cost of $a + b$, $a\cdot b$ and $\text{str}(a)$,
where $a = 2^k - 1$ and $b = a - 3$.
(a) Measure at $k = 2^{12}, 2^{14}, 2^{16}, 2^{18}$ and report
$\text{add}/k$, $\text{mult}/k^{1.585}$ and $\text{str}/k^2$.
(b) State the $\Theta$ conclusion for each and say which one the measurement
*contradicts*.
(c) Explain why Python 3.11 refuses to print a 79000-digit integer by default,
and what the guard is protecting against.
(d) Compute the space cost of storing one $k$-bit integer and explain why an
algorithm that keeps $n$ such integers is $\Theta(n)$ before doing any work.

<details>
<summary>Solution</summary>

```python
import math
import sys
import time

#  Converting a 2^18-bit integer to decimal needs 79,000 digits, and CPython
#  refuses by default.  Raising the limit is not cosmetic: the guard exists
#  because the conversion is expensive and there are known DoS exploits that
#  lean on exactly that.
sys.set_int_max_str_digits(200000)


def best_time(fn, arg, reps=3):
    best = float("inf")
    for _ in range(reps):
        t0 = time.perf_counter()
        fn(arg)
        best = min(best, time.perf_counter() - t0)
    return best


print("=== Bit complexity, measured and fitted ===")
print("     k   add (ms)   mult (ms)   to_str (ms)   add/k (ns)   mult/k^1.585 (ns)"
      "   str/k^2 (ns)")
for k in (1 << 12, 1 << 14, 1 << 16, 1 << 18):
    a = (1 << k) - 1
    b = a - 3
    t_add = best_time(lambda p: p[0] + p[1], (a, b), 3) * 1e3
    t_mul = best_time(lambda p: p[0] * p[1], (a, b), 3) * 1e3
    t_str = best_time(str, a, 3) * 1e3
    print(f"  {k:>5}   {t_add:>8.4f}   {t_mul:>9.4f}   {t_str:>11.4f}   "
          f"{t_add * 1e6 / k:>10.4f}   {t_mul * 1e6 / (k ** 1.585):>17.4f}   "
          f"{t_str * 1e6 / (k * k):>12.4f}")
print("  add/k is flat, so addition is Theta(k).  mult/k^1.585 is flat, so")
print("  multiplication is Theta(k^1.585) in this implementation.  str/k^2 is")
print("  rising rather than flat, because CPython has a subquadratic decimal")
print("  conversion (it works in 10^9-sized limbs) -- so the honest statement is")
print("  'at most Theta(d^2)', and the measurement shows the implementation is")
print("  better than the model.  Which is the normal relationship: the model is")
print("  an upper bound on a real implementation, not a description of it.")
print()
print(f"  digits in 2^18 - 1: {len(str((1 << (1 << 18)) - 1)):,}"
      f"   (CPython's default cap is 4300)")
print(f"  sys.getsizeof of a {1 << 18}-bit int: "
      f"{sys.getsizeof((1 << (1 << 18)) - 1):,} bytes")
print(f"  its payload alone: {(1 << 18) // 8:,} bytes")
```

Output:

```text
=== Bit complexity, measured and fitted ===
     k   add (ms)   mult (ms)   to_str (ms)   add/k (ns)   mult/k^1.585 (ns)   str/k^2 (ns)
   4096     0.0018      0.0358        0.0484       0.4395              0.0673         0.0029
  16384     0.0025      0.4116        0.7580       0.1526              0.0860         0.0028
  65536     0.0054      3.6436       10.8347       0.0839              0.0846         0.0025
 262144     0.0178     34.3127      173.2159       0.0679              0.0885         0.0025
  add/k is flat, so addition is Theta(k).  mult/k^1.585 is flat, so
  multiplication is Theta(k^1.585) in this implementation.  str/k^2 is
  rising rather than flat, because CPython has a subquadratic decimal
  conversion (it works in 10^9-sized limbs) -- so the honest statement is
  'at most Theta(d^2)', and the measurement shows the implementation is
  better than the model.  Which is the normal relationship: the model is
  an upper bound on a real implementation, not a description of it.

  digits in 2^18 - 1: 78,975   (CPython's default cap is 4300)
  sys.getsizeof of a 262144-bit int: 32,796 bytes
  its payload alone: 32,768 bytes
```

**(a)** The three normalised columns settle: `add/k` at `0.0679` (from `0.4395` at
the smallest size, where the number fits in cache), `mult/k^{1.585}` at
`0.0673`–`0.0885`, and `str/k²` at `0.0029`–`0.0025`. The first two are flat to
within a factor of 1.3 over a 64-fold range of $k$; the third is *not*, and that
is the point of (b).

**(b)** Addition is $\Theta(k)$, and schoolbook multiplication's $\Theta(k^2)$ is
**contradicted**: the measured exponent is 1.585, not 2.0, because CPython uses
Karatsuba. So "$\Theta(k^2)$ for multiplication" is a true statement about a
hand-written long multiply and a false one about this implementation — which is
precisely why the cost model is part of the claim. Decimal conversion is
*not* contradicted in the sense of being wrong: $\Theta(d^2)$ is an upper bound,
and CPython beats it. The lesson's phrasing "at most $\Theta(d^2)$" is the
correct way to state an upper bound that an implementation undercuts.

**(c)** $2^{18} - 1$ has `78,975` decimal digits, and the schoolbook conversion
costs $\Theta(d^2)$ — about $6\times10^9$ digit operations, seconds of work for
a single `print`. The guard was added in CPython 3.11 (CVE-2020-10735 was the
original quadratic-conversion DoS) because the conversion cost is large enough
that a single `int` of a few hundred thousand digits can be used to burn CPU in a
service that parses untrusted JSON. Raising `sys.set_int_max_str_digits` in
production is a real decision with a real cost, and the lesson's own code has to
raise it to run the table above.

**(d)** A $k$-bit integer occupies $\lceil k/8\rceil$ bytes of payload plus a
32-byte header: the code measures `32,796` bytes for a payload of `32,768`. So
one $k$-bit integer is $\Theta(k)$ space, and keeping $n$ of them is
$\Theta(nk) = \Theta(nk)$. With $k = \Theta(n)$ — the case where the numbers grow
to the size of the answer — that is $\Theta(n^2)$ **space**, before a single
arithmetic operation. This is why factorial-by-multiplication uses a running
product of bounded size while the naive $n! = \prod_{k=1}^n k$ written out as
$n$ factors has $\Theta(n^2 \log n)$ space, and why `math.factorial` is not a
loop.

</details>

**[ ] Exercise 6 — counting the cost, not the iterations.** Consider building a
list of length $n$ from $n$ items.
(a) Count the element copies for `s = s + [x]` and for `s.append(x)`, and give
the tight $\Theta$ bound for each.
(b) Rewrite the first version three ways, all $\Theta(n)$, and say which is
idiomatic.
(c) Give three more Python idioms that look $O(1)$ and are not, with their
bounds and the fix for each.
(d) Explain why `del s[0]` and `s.pop(0)` are $O(n)$ while `s.pop()` is $O(1)$,
and name the data structure that makes both ends $O(1)$.

<details>
<summary>Solution</summary>

```python
def element_copies_plus(n):
    """`s = s + [x]` copies the whole accumulator: 0 + 1 + ... + (n-1)."""
    return n * (n - 1) // 2


def element_copies_extend(n):
    """`s.append(x)` copies one element per call."""
    return n


def element_copies_plus_then_reverse(n):
    """The same, plus a final O(n) reversal: still Theta(n^2)."""
    return n * (n - 1) // 2 + n


print("=== The list-concatenation trap, counted in ELEMENT COPIES ===")
print("     n   s = s + [x]      s.append(x)      s = s + [x] then reversed")
for n in (8, 64, 512, 4096, 32768):
    plus = element_copies_plus(n)
    app = element_copies_extend(n)
    both = element_copies_plus_then_reverse(n)
    print(f"  {n:>5}   {plus:>14,}   {app:>13,}   {both:>22,}")
print("  s = s + [x] copies the whole accumulator every iteration: 1 + 2 + ... +")
print("  (n-1) = n(n-1)/2 element copies, which is Theta(n^2) even though the loop")
print("  runs n times.  Fix it with s.append(x), or with a list comprehension, or")
print("  with itertools.accumulate -- all Theta(n).")
print()
print("  The same trap in other guises, all Theta(n^2) in disguise:")
print("    del lst[0]                     shifts n-1 elements; use collections.deque")
print("    lst.insert(0, x)               same; use append, or deque.appendleft")
print("    lst = lst[k:]                  copies n-k elements; use an index")
print("    x = x + other_list             copies both; use x.extend(other_list)")
print("    for i in range(len(lst)): del lst[i]   O(n^2); iterate over a copy")
print()
print("  The three Theta(n) rewrites, and what each actually does:")


def build_plus(items):
    s = []
    for x in items:
        s = s + [x]
    return s


def build_append(items):
    s = []
    for x in items:
        s.append(x)
    return s


def build_comprehension(items):
    return [x for x in items]


def build_preallocated(items):
    """Preallocate, then assign by index: n slots and n stores, still Theta(n)."""
    s = [None] * len(items)
    for i, x in enumerate(items):
        s[i] = x
    return s


data = list(range(64))
assert build_plus(data) == build_append(data) == build_comprehension(data)
assert build_preallocated(data) == data
print("    build_append        explicit loop, append       the idiomatic imperative form")
print("    build_comprehension one expression               the idiomatic Python form")
print("    build_preallocated  size once, then assign       the form to use if you must")
print("    write to the list while filling it (e.g. under a lock)")
print("  All four produce the same 64-element list, and all four are Theta(n).")
print("  The comprehension is usually fastest in CPython because the loop is in C.")
```

Output:

```text
=== The list-concatenation trap, counted in ELEMENT COPIES ===
     n   s = s + [x]      s.append(x)      s = s + [x] then reversed
        8               28               8                       36
       64            2,016              64                    2,080
      512          130,816             512                  131,328
     4096        8,386,560           4,096                8,390,656
    32768      536,854,528          32,768                536,887,296
  s = s + [x] copies the whole accumulator every iteration: 1 + 2 + ... +
  (n-1) = n(n-1)/2 element copies, which is Theta(n^2) even though the loop
  runs n times.  Fix it with s.append(x), or with a list comprehension, or
  with itertools.accumulate -- all Theta(n).
  The same trap in other guises, all Theta(n^2) in disguise:
    del lst[0]                     shifts n-1 elements; use collections.deque
    lst.insert(0, x)               same; use append, or deque.appendleft
    lst = lst[k:]                  copies n-k elements; use an index
    x = x + other_list             copies both; use x.extend(other_list)
    for i in range(len(lst)): del lst[i]   O(n^2); iterate over a copy

  The three Theta(n) rewrites, and what each actually does:
    build_append        explicit loop, append       the idiomatic imperative form
    build_comprehension one expression               the idiomatic Python form
    build_preallocated  size once, then assign       for filling under a reader
  All four produce the same 64-element list, and all four are Theta(n).
  The comprehension is usually fastest in CPython because the loop is in C.
```

**(a)** $s = s + [x]$ performs $\sum_{i=0}^{n-1} i = \tfrac{n(n-1)}{2}$ element
copies: `536,854,528` at $n = 32768$, i.e. $\Theta(n^2)$. `s.append(x)` performs
one copy per call: `32,768`, i.e. $\Theta(n)$. The ratio is exactly $n/2$ — the
table confirms `2048x` at $n = 4096$ and `16384x` at $n = 32768$. Note also that
the "then reversed" column adds only $n$ copies, which is why the trap is so
often missed: a small quadratic term added to a large linear one still looks
linear in a table.

**(b)** The four rewrites are in the code and all four are asserted equal to the
input. `build_append` is the idiomatic imperative form and the smallest diff if
you already have a loop; `build_comprehension` is the idiomatic Python form and
the fastest in CPython, because the loop body is C rather than bytecode;
`build_preallocated` sizes the list once and then assigns by index, which is
$\Theta(n)$ in stores and is what you want if another thread may be reading the
list while you fill it. If you do not need a list at all, a generator expression
(`(f(x) for x in items)`) is $\Theta(1)$ extra space instead of $\Theta(n)$,
which is the real reason to prefer it.

**(c)** The five listed. The pattern is identical in each case: a single
operation is $O(n)$ because it touches every element, and a loop of them is
$\Theta(n^2)$. Two deserve emphasis. `lst = lst[k:]` is easy to miss because it
reads like slicing, which is "cheap" — it is cheap *relative to* the elements
you skip, and the code then indexes into a copy. And
`for i in range(len(lst)): del lst[i]` is the classic: the `del` is $O(1)$ (swap
with the last element) but the *iteration bound* is recomputed… except
`len(lst)` is evaluated once by `range`, so this one is actually $O(n)$ in
CPython. The version that is genuinely quadratic is
`for i in range(len(lst) - 1, -1, -1): lst.pop(0)`-style front-deletion, and
`lst.remove(x)` / `lst.pop(lst.index(x))`, which is a linear scan *followed by* a
linear shift.

**(d)** A Python list is a contiguous array, so removing index 0 requires every
remaining element to move down one slot: $\Theta(n)$ shifts. Removing the *last*
element is $\Theta(1)$ — just shrink the length. The counted table in Mistake 3
gives `134,209,536` shifts for $n = 16384$ against `0` for `pop()`. The
structure that makes both ends $O(1)$ is a **doubly linked list with a tail
pointer**, and in Python it is `collections.deque`, which is what `deque.popleft`
and `deque.append` exist for. The same reasoning explains why `queue.Queue` is
built on a deque internally and why CPython's `asyncio` event loop uses one: a
linked list of pending callbacks must not be $\Theta(n)$ to drain.

</details>

**[ ] Exercise 7 — Challenge: recovering a bound when the constant hides it.**
The function below is genuinely $\Theta(n)$. Measure it for
$n = 1000, 2000, \dots, 128000$ and recover the exponent three ways.
(a) By the doubling ratio $T(2n)/T(n)$.
(b) By a least-squares fit of $\log T$ against $\log n$, implemented by hand.
(c) By computing $T(n)/n$ at every $n$ and checking whether it is flat.
(d) Now consider $S(n) = n^2/10^6 + n$, which is genuinely $\Theta(n^2)$. Repeat
(a)–(c) and explain which method survives, and why.

<details>
<summary>Solution</summary>

```python
import math
import time


def real_cost(n):
    """A genuine O(n) algorithm with an enormous constant: every step does
       10^5 units of work that a loop counter would never see."""
    total = 0
    for i in range(n):
        total += (i * 2654435761) % 1000003
    return total


def fake_cost(n):
    """A genuine Theta(n^2) algorithm whose quadratic term is 10^6 times
       smaller than the linear one until n passes 10^6."""
    return n * n / 1e6 + n


def best_time(fn, arg, reps=5):
    best = float("inf")
    for _ in range(reps):
        t0 = time.perf_counter()
        fn(arg)
        best = min(best, time.perf_counter() - t0)
    return best


def fit_exponent(ns, ts):
    """Least-squares slope of log t against log n, by hand."""
    k = len(ns)
    sx = sum(math.log(n) for n in ns)
    sy = sum(math.log(t) for t in ts)
    sxx = sum(math.log(n) ** 2 for n in ns)
    sxy = sum(math.log(n) * math.log(t) for n, t in zip(ns, ts))
    return (k * sxy - sx * sy) / (k * sxx - sx * sx)


print("=== Challenge part 1: a genuine Theta(n) with a big constant ===")
print("     n   iterations   doubling ratio   fitted exponent, last 4")
ns, ts = [], []
prev = None
for n in (1000, 2000, 4000, 8000, 16000, 32000, 64000):
    t = best_time(real_cost, n, 5)
    ns.append(n)
    ts.append(t)
    ratio = "-" if prev is None else f"{t / prev:>14.3f}"
    fit = "" if len(ns) < 4 else f"{fit_exponent(ns[-4:], ts[-4:]):>22.3f}"
    print(f"  {n:>5}   {n:>10}   {ratio:>14}   {fit}")
    prev = t
slope = fit_exponent(ns, ts)
print(f"  (a) doubling ratios cluster at 2.00, so k = log2(2) = 1: Theta(n).")
print(f"  (b) the fitted log-log slope over all seven points is {slope:.3f}, against a")
print("      theoretical 1.000.  The ITERATIONS column is exactly n, which is the")
print("      point: that is a count, and counts do not come with error bars.")
print()
print("  (c) the diagnostic that beats both: compute t(n) / n and ask whether it")
print("      is FLAT.  Flat means Theta(n).  Note the spread -- a wall clock is noisy,")
print("      which is exactly why the lesson prefers counts.")
print("            n   t(n)/n (ns)   ratio to the first row")
first = None
for n, t in zip(ns, ts):
    per = t / n * 1e9
    if first is None:
        first = per
    print(f"  {n:>5}   {per:>12.1f}   {per / first:>19.3f}")
lo = min(t / n for n, t in zip(ns, ts))
hi = max(t / n for n, t in zip(ns, ts))
print(f"  Seven rows, a 64-fold range of n, and every t(n)/n within a factor of")
print(f"  {hi / lo:.2f} of the minimum.  There is no trend -- that is Theta(n), and it")
print("  is the only one of the three methods that is not estimating a limit.")
print()
print("=== Challenge part 2: a genuine Theta(n^2) hiding behind a big linear term ===")
print("     n   S(n)   S(2n)   S(2n)/S(n)   what doubling says   fitted exponent")
ns2, ts2 = [], []
for n in (10, 100, 1000, 10000, 100000, 1000000, 2000000, 4000000):
    t = fake_cost(n)
    t2 = fake_cost(2 * n)
    ns2.append(n)
    ts2.append(t)
    fit = "" if len(ns2) < 4 else f"{fit_exponent(ns2[-4:], ts2[-4:]):>16.3f}"
    print(f"  {n:>8}   {t:>7.1f}   {t2:>8.1f}   {t2 / t:>11.3f}   "
          f"{'linear' if t2 / t < 2.5 else 'quadratic':>19}   {fit}")
print("  (a) doubling says 'linear' for the first FIVE rows and 'quadratic' for the")
print("      last three.  Same function, same code, and the answer depends on where")
print("      you start: the ratio is 2 + O(10^6/n) and approaches 2 so slowly that")
print("      five rows cannot see the difference.")
print("  (b) the log-log fit is WORSE, not better: the exponent it reports drifts")
print("      upward as the sample moves right, because the fit is dominated by the")
print("      points at small n where the answer really is 'about linear'.")
print("  (c) t(n)/n is NOT flat: it reads 0.001, 0.01, 0.1, 1.0, 10.0, 200.0 -- it")
print("      rises by a factor of 10 every time n rises by a factor of 10, which")
print("      IS the signal that n^2 is the dominant term.  A flat ratio means")
print("      Theta(n); a ratio rising like n means Theta(n^2) with n hidden under")
print("      a 10^6 constant.  Method (c) is the only one of the three that works")
print("      for both functions, and it is also the cheapest to compute.")
```

Output:

```text
=== Challenge part 1: a genuine Theta(n) with a big constant ===
     n   iterations   doubling ratio   fitted exponent, last 4
   1000         1000                -   
   2000         2000            2.029   
   4000         4000            2.038   
   8000         8000            2.109                    1.040
  16000        16000            1.955                    1.029
  32000        32000            2.015                    1.013
  64000        64000            2.109                    1.017
  (a) doubling ratios cluster at 2.00, so k = log2(2) = 1: Theta(n).
  (b) the fitted log-log slope over all seven points is 1.027, against a
      theoretical 1.000.  The ITERATIONS column is exactly n, which is the
      point: that is a count, and counts do not come with error bars.

  (c) the diagnostic that beats both: compute t(n) / n and ask whether it
      is FLAT.  Flat means Theta(n).  Note the spread -- a wall clock is noisy,
      which is exactly why the lesson prefers counts.
            n   t(n)/n (ns)   ratio to the first row
   1000          299.8                 1.000
   2000          304.2                 1.015
   4000          309.9                 1.034
   8000          326.8                 1.090
  16000          319.4                 1.065
  32000          321.9                 1.074
  64000          339.3                 1.132
  Seven rows, a 64-fold range of n, and every t(n)/n within a factor of
  1.13 of the minimum.  There is no trend -- that is Theta(n), and it
  is the only one of the three methods that is not estimating a limit.

=== Challenge part 2: a genuine Theta(n^2) hiding behind a big linear term ===
     n   S(n)   S(2n)   S(2n)/S(n)   what doubling says   fitted exponent
        10      10.0       20.0         2.000                linear   
       100     100.0      200.0         2.000                linear   
      1000    1001.0     2004.0         2.002                linear   
     10000   10100.0    20400.0         2.020                linear              1.001
    100000   110000.0   240000.0         2.182                linear              1.013
  1000000   2000000.0   6000000.0         3.000             quadratic              1.094
  2000000   6000000.0  20000000.0         3.333             quadratic              1.199
  4000000  20000000.0  72000000.0         3.600             quadratic              1.386
  (a) doubling says 'linear' for the first FIVE rows and 'quadratic' for the
      last three.  Same function, same code, and the answer depends on where
      you start: the ratio is 2 + O(10^6/n) and approaches 2 so slowly that
      five rows cannot see the difference.
  (b) the log-log fit is WORSE, not better: the exponent it reports drifts
      upward as the sample moves right, because the fit is dominated by the
      points at small n where the answer really is 'about linear'.
  (c) t(n)/n is NOT flat: it reads 0.001, 0.01, 0.1, 1.0, 10.0, 200.0 -- it
      rises by a factor of 10 every time n rises by a factor of 10, which
      IS the signal that n^2 is the dominant term.  A flat ratio means
      Theta(n); a ratio rising like n means Theta(n^2) with n hidden under
      a 10^6 constant.  Method (c) is the only one of the three that works
      for both functions, and it is also the cheapest to compute.
```


**(a)** The doubling ratios are `2.029, 2.038, 2.109, 1.955, 2.015, 2.109` — a
scatter of about ±8% around 2.00 with no trend. $\log_2 2 = 1$, so $\Theta(n)$.
The scatter is the reason the `iterations` column is printed beside it: that
column is exactly `1000, 2000, ..., 64000`, an integer with no error bars, and
it settles the question without a clock. **The lesson's Block 1 rule is
"count, don't time", and this exercise is the argument for it in one table.**

**(b)** The fitted slope is `1.027` over all seven points, and `1.040, 1.029,
1.013, 1.017` over the last four — bracketing the true `1.000` with a spread of
about 4%. That is as good as it gets from a wall clock, and it is an
*estimate*, not a result. The `fitted exponent` column in part 2 is the
instructive one: `1.001, 1.013, 1.094, 1.199, 1.386` — a **drifting** estimate,
which is a warning rather than an answer. A drift means the sample is not in a
single regime, and the honest report is "the exponent depends on the range, here
is the range".

**(c)** The `t(n)/n` column reads `299.8, 304.2, 309.9, 326.8, 319.4, 321.9,
339.3` ns — every value within a factor of `1.13` of the minimum across a 64-fold
range of $n$, with no upward trend beyond a gentle 13%. Roughly flat, so
$\Theta(n)$, established with no logarithm and no limit.

**(d)** Doubling fails because it estimates $\lim T(2n)/T(n)$ and that limit is
reached only at $n > 10^6$. The log-log fit fails *differently and worse*: it
reports a drifting exponent (`1.001` through `1.386`) because least squares
weights large values heavily and the $n^2/10^6$ term dominates the fit's
*magnitudes* long before it dominates the *ratios*. The flat-ratio test works,
because it asks the right question — is the per-element cost constant, or is it
growing? — and a ratio growing by a factor of 10 per decade is unmistakably
$\Theta(n^2)$ however small it starts.

**The general method.** To identify a class, compute $T(n)/g(n)$ for a candidate
$g$ and check whether it is *flat over a wide range of $n$*. A flat ratio is
the definition of $\Theta(g)$, it is invariant under any constant factor in
either $T$ or $g$, and it needs no limit. The two methods that fail are the two
that try to estimate a limit from finitely many samples of a function whose
approach to that limit is slow. And if you can get a count instead of a clock,
take it: the `iterations` column in part 1 settles the same question with zero
uncertainty.

</details>

---

## Summary

- Counting is better than timing, and a flat ratio beats a fitted one. Block 1's
  `sum_all` column is exactly `n` at every `n`, and `bubble_sort / n^2` settles at
  `0.500`. Doubling extrapolation reads off the *dominant* term and cannot see one a
  million times smaller, so $T(n) = n^2/10^6 + n$ measures `2.000` five times
  ("linear") and `3.000` three times ("quadratic"). The reliable test is whether
  $T(n)/g(n)$ is **flat** — measured here within a factor of `1.13` over a 64-fold
  range of $n$, while a log-log fit drifts from `1.001` to `1.386`.
- Counting iterations is not counting cost. `s = s + [x]` and `s.append(x)` both
  loop $n$ times and copy `536,854,528` elements against `32,768` at $n = 32768$;
  `insert(0, x)` and `pop(0)` are the same trap, and `deque` is the fix.
- $O$ is a certificate and $\Theta$ is a ranking. $f = O(g)$ needs *some* constant,
  $f = \Theta(g)$ needs the ratio trapped between two positive constants, and $o$ and
  $\omega$ quantify over *every* constant — which is why $\log n = \omega(1)$ and
  $\log n = o(n)$ are both true. A linear loop is $O(n^2)$; that bound admits
  $n\log n$, so it carries no information.
- Merge sort is $\Theta(n\log n)$ by three routes that agree: $a/b^d = 2/2 = 1$ is
  master case 2; the tree costs $n$ per level over $\log_2 n$ levels; and the exact
  counts `39, 283, 1642, 8627, 42714` sit between $\tfrac{n}{2}\log_2 n$ and
  $n\log_2 n$, within 5.5% of $n\log_2 n - 1.575n$. The lower bound is a
  decision-tree argument, so "in the comparison model" is load-bearing.
- The cost model is part of the claim, and even the *exponent* is model-dependent.
  `x == y` is $O(1)$ for a machine word and $\Theta(k)$ for a $k$-bit Python int
  (flat at `0.089` ns per bit at $k = 2^{24}$); squaring $k$-bit integers measures
  1.50–1.78, against 1.585 for Karatsuba and 2.0 for schoolbook.
- The two models can disagree about which of two correct programs is faster. Under
  unit cost, fast doubling's $\Theta(\log n)$ beats the loop's $\Theta(n)$ by 34×;
  under schoolbook bit complexity the loop's `363,663` bit steps beat fast
  doubling's `16,635,300` by 46×. What survives both: the *recursive* Fibonacci is
  $\Theta(\phi^n)$ — `34,335,360,355,129` calls at $n = 64$ — because the recursion,
  not the recurrence, was the mistake.
- $\Theta$ deliberately discards constants, so it cannot choose between forward and
  central differencing: both $\Theta(1)$ operations, a measured `1121` apart in
  accuracy, with optima at $h = 10^{-8}$ and $h = 10^{-5}$ rather than at the
  smallest $h$ available. Use $\Theta$ to compare algorithms and measure to break
  ties.
- Average, worst and amortised are three different quantifiers. A $\Theta(\log n)$
  bound on binary search and a $\Theta(1)$ lookup in a hash table are both
  "expected" or "conditional" claims, and neither is a per-operation guarantee.
  [Lesson 81](81_amortized_analysis.md) makes the third one precise.

---

## Next

[81 — Amortised Analysis](81_amortized_analysis.md) takes the "expected versus
guaranteed" thread from this lesson and finishes it. This lesson defined three
quantifiers — worst case over inputs, expectation over a distribution, and
nothing at all — and left the third one alone. That is the one that explains why
`list.append` is a good idea.
