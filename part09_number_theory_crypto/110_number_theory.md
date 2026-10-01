# 110 — Number Theory

**Part**: part09_number_theory_crypto · **Prerequisites**: 24 · **Time**: 35 min

---

## In Plain Words

Everything in this part rests on a handful of facts about whole numbers. One
number divides another when the second is a whole-number multiple of the
first. Some numbers have no factors except one and themselves — those are
primes, and every integer greater than one can be broken into primes in
exactly one way. To find the largest factor two numbers share, you repeatedly
take a remainder, and the answer appears in about a dozen steps no matter how
huge the numbers are. The strange and extremely useful fact is that primes,
while being the most evenly spread-out numbers we know, are also the hardest to
take apart: given a big number built from two secret primes, no known method
recovers those primes quickly. Every technique in this lesson is either a tool
for computing with numbers or a reason that computing with numbers is hard.

## Why Computer Science Cares

- **`openssl genrsa` and every TLS handshake.** Generating a 2048-bit RSA key
  means finding two 1024-bit primes. `openssl prime 1024` prints one; the time
  it takes is the time it takes.
- **`math.gcd` in the standard library** is the Euclidean algorithm. It is the
  workhorse behind reducing fractions, computing the lowest common denominator,
  the modular inverse, and the Chinese Remainder Theorem — all of this part.
- **`zlib.crc32` and `hashlib`** compute polynomials over finite fields, which
  is the same algebra as Lesson 110, run many times in parallel.
- **Random number generation.** Python's `random` is a Mersenne Twister with
  prime period 2^19937 − 1; a cryptographic generator such as ChaCha20 or
  AES-CTR is built on prime fields mod 2^32 − 5 and 2^256 − 2^32 − 977.
- **Interview questions.** "Compute gcd without recursion", "factor a number
  in O(sqrt n)", "is this number prime" appear in essentially every algorithms
  interview, because they separate people who know loops from people who know
  number theory.

## The Formal Version

Notation follows [SYMBOLS.md](../../SYMBOLS.md). Symbols used here: `a | b`,
`a mod b`, `gcd(a, b)`, `lcm(a, b)`, `π(N)`, `O()`, `Θ()`.

### Divisibility and the division algorithm

**Definition.** For integers `a` and `b` with `a ≠ 0`, we say **`a` divides `b`**
(written `a | b`) if and only if there is an integer `k` with `b = a·k`. We call
`a` a *divisor* of `b` and `b` a *multiple* of `a`.

The `k` is not unique in general — `12 | 60` because `60 = 12·5`, and also
`60 = 12·5` only once for integers, so the *quotient is unique once the divisor
is positive*. That uniqueness is exactly the division algorithm.

**Theorem (division algorithm).** Let `b` be an integer and let `a > 0`. Then
there exist unique integers `q` and `r` such that

```
b = a·q + r        with        0 ≤ r < a
```

**Why it matters.** It says division is well defined. There is exactly one
remainder, so `a mod b` is a *function*, and every later piece of arithmetic in
this part is built on it. Python's `divmod(b, a)` returns that `(q, r)` pair.

**Definition.** `a | b` is called **proper** if `a | b` and `|a| < |b|`. We
write `a ∥ b` for "a divides b, but b does not divide a".

### Primes and the Fundamental Theorem of Arithmetic

**Definition.** An integer `p > 1` is **prime** if its only positive divisors
are `1` and `p`. An integer `n > 1` that is not prime is **composite** and can
be written `n = a·b` with `1 < a < n`.

**Definition.** The **greatest common divisor** `gcd(a, b)` is the largest
positive integer dividing both. **The least common multiple** `lcm(a, b)` is the
smallest positive integer divisible by both, defined as `|a·b| / gcd(a, b)`.

**Theorem (Fundamental Theorem of Arithmetic, FTA).** Every integer `n > 1` has
exactly one factorisation `n = p₁^{e₁} p₂^{e₂} ⋯ p_k^{e_k}` into primes, up to
reordering.

*Explanation.* Existence: `n` is either prime (done) or composite, and a
composite has a factor strictly between 1 and `n`, so the process terminates.
Uniqueness: suppose two prime factorisations of `n` agree on the smallest prime
appearing in either, say `p` with exponent `e` in one. Then `p^e | n`, so
`p | n`, so `p` divides every prime in the other factorisation too (a prime
dividing a product of primes must equal one of them). Cancelling `p` from both
sides and repeating forces the two factorisations to coincide. ∎

*Why CS cares.* The FTA is what makes "this integer is uniquely determined by its
prime factors" true, which in turn makes certificates, checksums, addresses, and
hashes well defined. Without it, "the same object" would not have a canonical
representation.

### The Euclidean algorithm

**Lemma (the key step).** For `a ≥ b > 0`, `gcd(a, b) = gcd(b, a mod b)`.

*Explanation.* Every common divisor of `a` and `b` divides `a − q·b` for any
integer `q`, and conversely every common divisor of `b` and `a − q·b` divides
`a`. The divisors of the two pairs are literally the same set, so the largest
one is the same. ∎

**Algorithm (Euclid).**

```
gcd(a, b):
    while b ≠ 0:
        (a, b) ← (b, a mod b)
    return a
```

**Theorem.** The loop terminates and returns `gcd(a₀, b₀)`.

*Termination.* If the loop ran forever, `b` would stay positive forever while
`a mod b < b`, so `a` would strictly decrease on every iteration past the
first. `a` is a positive integer and cannot decrease indefinitely. ∎

*Correctness.* Loop invariant: `gcd(a, b) = gcd(a₀, b₀)`. It holds initially,
is preserved by the lemma above, and at termination `b = 0`, so the result is
`gcd(a, 0) = a`. ∎

**Theorem (number of steps).** The loop runs in `Θ(log(min(a, b)))` divisions
and is therefore optimal among the natural algorithms, because the Fibonacci
sequence `F₁ = 1, F₂ = 1, F_{k+2} = F_{k+1} + F_k` achieves exactly this many
steps for input `(F_{k+1}, F_k)`.

*Explanation.* Each step replaces `(a, b)` by a pair whose larger entry is
smaller, and after `k` steps the larger entry has shrunk by at least a factor
of 2 every two steps — the halving argument. So `log₂` of the input bounds the
step count. Fibonacci numbers are the worst case because consecutive
Fibonacci numbers are the pairs with the *slowest* possible shrink, since each
step makes the remainder as large as it can be while staying smaller than `b`. ∎

This is the payoff of Lesson 80: `O(log n)` on an `n`-bit input is `O(bit
length)`, i.e. linear in the size of the input as written. That makes the
Euclidean algorithm bit-complexity optimal, up to a constant, for its problem.

### Bézout's identity

**Theorem (Bézout).** For any integers `a, b` there exist integers `s, t` with
`gcd(a, b) = s·a + t·b`.

**Corollary.** If `g = gcd(a, m)` then `1` is a multiple of `g`, so if `g = 1`
there exist `s, t` with `s·a + t·m = 1`. Reducing mod `m` gives `s·a ≡ 1`,
so `a` has an inverse mod `m` exactly when `gcd(a, m) = 1`. This single
corollary is the gateway to all of Lesson 111.

**All solutions.** If `(s₀, t₀)` is one solution then so is
`(s₀ + k·m/g, t₀ − k·a/g)` for every integer `k`.

### The sieve and the growth of π(N)

**Definition.** `π(N)`, read "pi of N", is the number of primes at most `N`.

**Algorithm (Sieve of Eratosthenes).** Mark all of `2..N` as prime. For `p`
from 2 while `p² ≤ N`, if `p` is still marked prime, mark `p², p²+p, p²+2p, …`
as composite.

*Correctness.* A marked composite is a multiple of a smaller number, so it is
indeed composite. Conversely every composite `c ≤ N` has a prime factor `p ≤
sqrt(c) ≤ sqrt(N)`, and `c ≥ p²`, so `c` is crossed out during `p`'s pass. ∎

**Complexity.** The mark count is `Σ_{p prime, p ≤ sqrt(N)} N/p`, which is
`Θ(N ln ln N)`. Primes get sparser as `N` grows, and the reciprocal sum of the
primes is the "harmonic series over primes", which behaves like `ln ln N`. So
the sieve is `Θ(N ln ln N)` time and `Θ(N)` space — not `Θ(N²)`, because we only
touch multiples of primes and we skip all of them below `p²`.

**Theorem (Bertrand's postulate).** For every `n > 1` there is a prime `p` with
`n < p < 2n`. This is why the prime gap near `n` averages about `ln n`, and it
is the reason generating a large prime takes a variable, unbounded amount of
time.

### Factoring is hard

**Observation.** To factor `n` by trial division you must test every `d` with
`d ≤ sqrt(n)`, because the smallest factor of a composite is at most its square
root. So trial division costs `Θ(sqrt(n))` divisions in the worst case, which
in *bit operations* is exponential.

**Observation.** Better algorithms exist but none is polynomial. Pollard's rho
finds a factor `p` in about `sqrt(p) = n^{1/4}` steps. The general number field
sieve (GNFS) is asymptotically the fastest known, at
`exp( (64/9)^{1/3} · (ln n)^{1/3} · (ln ln n)^{2/3} )` — subexponential, but
still exponential in `log n`.

**Consequence.** For a 3072-bit RSA modulus (925 decimal digits), trial
division would need about `10^462` steps. Nobody has ever factored an RSA
modulus of that size. This asymmetry — multiplication and modular exponentiation
are polynomial-time and easy, factoring is believed not to be — is the entire
economic basis of public-key cryptography.

## Worked Example

Take `a = 1071` and `b = 462`. We want `gcd(1071, 462)`.

**Step 1.** `1071 mod 462`. `462 × 2 = 924`, and `1071 − 924 = 147`. So the
first division is `1071 = 2 × 462 + 147`.

**Step 2.** `462 mod 147`. `147 × 3 = 441`, and `462 − 441 = 21`. So
`462 = 3 × 147 + 21`.

**Step 3.** `147 mod 21`. `21 × 7 = 147`, remainder `0`. So `147 = 7 × 21 + 0`.

The remainder is now `0`, so the algorithm stops and returns the last non-zero
remainder, `21`. Check: `1071 = 21 × 51` and `462 = 21 × 22`, and `51` and
`22` share no factor. So `gcd(1071, 462) = 21`.

Three divisions. The naive method — testing every `d` from 1 to 462 — would
take 462 tests. And by hand the numbers stay small: the largest is the input
itself, and it shrinks monotonically.

**Now do it again keeping the coefficients**, to get Bézout's identity. Run the
same three divisions but track the coefficients of the original 1071 and 462:

| step | equation | coefficients |
| --- | --- | --- |
| start | `1·1071 + 0·462 = 1071` | `(1, 0)` |
| step 1 | `1071 = 2·462 + 147` → `147 = 1·1071 − 2·462` | `(1, −2)` |
| step 2 | `462 = 3·147 + 21` → `21 = 462 − 3·147` | `(−3, 7)` |
| step 3 | `147 = 7·21 + 0` | stops |

So `21 = −3 × 1071 + 7 × 462`. Verify: `−3 × 1071 = −3213` and
`7 × 462 = 3234`, and `−3213 + 3234 = 21`. ✓

**Finally, lcm.** `lcm(1071, 462) = 1071 × 462 / 21 = 494,802 / 21 = 23,562`.
Check: `1071 × 22 = 23,562` ✓ and `462 × 51 = 23,562` ✓.

Three numbers, one short loop, and you have the gcd, a Bezout certificate, and
the lcm. Every one of those is a two-line function in production, and the
modular inverse in [Lesson 111](111_modular_arithmetic_and_crypto.md) is this
same loop with one extra line of output.

## Runnable Code

### 1. Divisibility, remainders, and primality

```python
def divides(a: int, b: int) -> bool:
    """a divides b exactly when b = a * k for some whole number k.
    In Python "b % a == 0" is precisely that test."""
    return b % a == 0

print("12 divides 60 :", divides(12, 60))   # 60 = 12 * 5
print("12 divides 61 :", divides(12, 61))   # 61 = 12 * 5 + 1
print()

# The division algorithm: for any integers b and any positive a there is one
# and only one way to write  b = a * q + r  with  0 <= r < a.
# Python's // and % compute exactly that q and r.
for a, b in [(7, 60), (7, -60), (13, 0)]:
    q, r = divmod(b, a)
    print(f"b={b:4d}  a={a:3d}  ->  q={q:4d}  r={r:3d}   (0 <= r < a: {0 <= r < a})")
print()

# A prime has no factor other than 1 and itself; "composite" means it has one.
def is_prime_trial(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:      # any factor pairs with another, so one is <= sqrt(n)
        if n % d == 0:
            return False
        d += 1
    return True

print("primes below 30:", [n for n in range(2, 30) if is_prime_trial(n)])
print()

# 1 has no divisors at all except 1, but it is NOT prime.
print("is_prime_trial(1) :", is_prime_trial(1))
print("is_prime_trial(2) :", is_prime_trial(2))
print("is_prime_trial(9) :", is_prime_trial(9))
```

### 2. The Euclidean algorithm, with a correctness check

```python
def naive_gcd(a: int, b: int) -> int:
    """gcd by definition: the largest shared positive factor.
    The special case gcd(a, 0) = |a| matters, because 0 is a multiple of a."""
    a, b = abs(a), abs(b)
    if b == 0:
        return a
    best = 1
    for d in range(1, min(a, b) + 1):
        if a % d == 0 and b % d == 0:
            best = d
    return best


def euclid(a: int, b: int) -> tuple[int, int]:
    """Return (gcd(a, b), number of divisions used)."""
    a, b = abs(a), abs(b)
    target = naive_gcd(a, b) if min(a, b) <= 10_000 else None
    steps = 0
    while b != 0:
        # The invariant gcd(a, b) == gcd(a0, b0) is preserved by this swap,
        # because gcd(a, b) = gcd(b, a mod b).
        a, b = b, a % b
        steps += 1
        if target is not None:
            assert naive_gcd(a, b) == target, "loop invariant broken"
    return a, steps


def show(a: int, b: int) -> None:
    """Print every division of the Euclidean algorithm for a and b."""
    x, y = a, b
    lines = []
    while y != 0:
        q, r = divmod(x, y)
        lines.append(f"{x} = {q} * {y} + {r}")
        x, y = y, r
    print(f"gcd({a}, {b}) = {x}")
    for line in lines:
        print("     ", line)
    print()


show(1071, 462)
show(17, 5)
show(48, 18)

g, steps = euclid(1071, 462)
print(f"gcd(1071, 462) = {g} in {steps} divisions (the naive search needs 462)")
g, steps = euclid(2**40 + 1, 987654321)
print(f"gcd(2^40+1, 987654321) = {g} in {steps} divisions")

# The loop invariant really does hold: check 4000 random small pairs against
# the definition-based gcd.
import math
import random

random.seed(0)
worst = 0
for _ in range(4000):
    x, y = random.randint(1, 9999), random.randint(1, 9999)
    got, steps = euclid(x, y)
    assert got == naive_gcd(x, y)
    worst = max(worst, steps)
print(f"4000 random pairs: every result matched, worst case {worst} divisions")
print(f"log2(9999) is only {math.log2(9999):.1f}, so a couple of dozen")
print("divisions at worst, instead of the thousands a naive search needs")
```

### 3. Bézout's identity (extended Euclid)

```python
def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Return (g, s, t) with  g = gcd(a, b)  and  g = s*a + t*b.

    Plain Euclid only returns the gcd.  This version carries the Bezout
    coefficients along, updating them with the same rules that update a and b.
    """
    old_r, r = a, b
    old_s, s = 1, 0        # coefficients of a
    old_t, t = 0, 1        # coefficients of b
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r       # old_r, r <- r, old_r - q*r
        old_s, s = s, old_s - q * s       # same rule applied to the coefficients
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t


for a, b in [(252, 105), (1071, 462), (240, 46), (17, 5)]:
    g, s, t = extended_gcd(a, b)
    print(f"gcd({a}, {b}) = {g}")
    print(f"   {s} * {a} + {t} * {b} = {s * a + t * b}")
    print(f"   check: {s}*{a} = {s * a}, {t}*{b} = {t * b}, total {s * a + t * b}")
    print()

# The identity is not just true, it is essentially unique: every solution has
# the form  s = s0 + (b/g)k,  t = t0 - (a/g)k  for integer k, where g = 21 here.
print("all Bezout solutions for 252 and 105, by searching k:")
s0, t0 = -2, 5
for k in range(4):
    s, t = s0 + (105 // 21) * k, t0 - (252 // 21) * k
    print(f"   k={k}:  s={s:3d}  t={t:4d}  ->  {s}*252 + {t}*105 = {s * 252 + t * 105}")
```

### 4. The Sieve of Eratosthenes

```python
def sieve_of_eratosthenes(n: int) -> tuple[list[bool], int]:
    """Return a boolean list marking primes up to n, and how many times the
    inner marking loop ran.

    Insight behind the algorithm: when we discover that p is prime, every
    multiple of p that is >= p*p has p as a smaller factor sitting next to it,
    so it is composite and can be crossed out.
    """
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False      # 0 and 1 are not prime
    marks = 0
    p = 2
    while p * p <= n:                     # stop once p*p exceeds n
        if is_prime[p]:
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False
                marks += 1
        p += 1
    return is_prime, marks


N = 100
flags, marks = sieve_of_eratosthenes(N)
print(f"primes below {N}:", [i for i, f in enumerate(flags) if f])
print(f"crossed out {marks} times")
print()

# The work done is sum over primes p <= sqrt(N) of  N/p, which is the harmonic
# series over primes: about N * ln ln N.  That is why the sieve costs
# O(N log log N) and not O(N^2).
def primes_upto(n: int) -> list[int]:
    flags, _ = sieve_of_eratosthenes(n)
    return [i for i, f in enumerate(flags) if f]


for limit in (10**3, 10**4, 10**5, 10**6):
    ps = primes_upto(limit)
    print(f"pi({limit:>9,}) = {len(ps):>7,}   largest prime found: {ps[-1]}")

print()
print("pi(N) is the number of primes up to N, written pi(N).")
print("pi(10^6) = 78,498: about one prime in every 13 numbers on average,")
print("and primes get rarer as N grows (pi(N) ~ N / ln N).")
print()

# Why only sieve up to sqrt(N): every composite number has a prime factor no
# larger than its square root, so the outer loop can stop at sqrt(N).
ps = set(primes_upto(N))
checked = [n for n in range(4, N) if not sieve_of_eratosthenes(n)[0][n]]
covered = [n for n in checked if any(p in ps and n % p == 0 for p in ps if p * p <= n)]
print(f"composites below {N}: {len(checked)}")
print(f"of those, {len(covered)} are hit by a prime p with p*p <= {N}, "
      f"and p <= {int(N ** 0.5)}")
print("so the outer loop never needs to go past sqrt(N) = 10")
```

### 5. What factoring costs

```python
import time


def trial_factor(n: int) -> tuple[list[int], int]:
    """Factor n by trying every candidate divisor in turn.

    Returns the list of prime factors (with repeats) and the number of
    divisions performed.  We can skip even numbers after 2, so we only test
    2 and then the odd numbers -- that halves the work.
    """
    factors: list[int] = []
    divisions = 0
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
            divisions += 1
        d = 3 if d == 2 else d + 2
        divisions += 1
    if n > 1:
        factors.append(n)          # whatever is left must be prime
    return factors, divisions


def is_prime(n: int) -> bool:
    """Trial division up to sqrt(n).  Fast enough for small n only."""
    if n < 2:
        return False
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return n % 2 != 0 or n == 2


for n in [360, 1000003, 2**31 - 1]:
    start = time.perf_counter()
    facs, divs = trial_factor(n)
    elapsed = time.perf_counter() - start
    print(f"{n:>12,} = {' * '.join(map(str, facs))}")
    print(f"{'':>12}  {divs:,} divisions, {elapsed * 1000:.2f} ms")
print()

# The hard case for trial division: a semiprime pq where both p and q are
# large.  The algorithm cannot stop until d*d > n, so it must grind through
# every candidate up to sqrt(n), and sqrt(n) is huge.
def next_prime(k: int) -> int:
    k += 1
    while not is_prime(k):
        k += 1
    return k


def semiprime_of_size(digits: int) -> int:
    """Build p*q with p and q of about half the digit count, i.e. hard."""
    root = 10 ** (digits // 2)
    p = next_prime(root)
    q = next_prime(p + 2)
    return p * q


print("cost of trial division for a semiprime, by number of digits:")
print(f"{'digits':>7} {'n = p*q':>22} {'divisions needed':>18}")
for digits in (6, 10, 14, 18):
    n = semiprime_of_size(digits)
    # We do NOT actually factor it; we just count how far the loop would go.
    approx = int(n**0.5) // 2
    print(f"{digits:>7} {n:>22,} {approx:>18,}")
print()
print("Each extra 4 digits of n multiplies the work by about 100, because")
print("the loop has to reach sqrt(n) and sqrt(n) grows like 10^(digits/2).")
print()

# Extrapolate to a real RSA key.  A 3072-bit modulus has 925 decimal digits,
# so trial division would need about 10^462 operations.
bits = 3072
decimal_digits = bits * 0.30103
print(f"A {bits}-bit RSA modulus has about {decimal_digits:.0f} decimal digits.")
print(f"Trial division would need on the order of 10^{decimal_digits / 2:.0f} steps.")
print("At a billion steps per second that is longer than the age of the universe,")
print("which is why nobody attacks real RSA that way -- and why nobody can")
print("attack it any other way either.  Pollard's rho removes small factors in")
print("about n^(1/4) steps, and the fastest known general method, the general")
print("number field sieve, costs exp( (64/9)^(1/3) * (ln n)^(1/3) * (ln ln n)^(2/3) ),")
print("which is subexponential but still hopeless at 925 digits.")
```

### 6. Why primes are the right modulus (Rabin fingerprint)

```python
# A rolling hash ("Rabin fingerprint") turns a string into a number, so two
# strings can be compared in O(1) instead of O(length).  The standard
# construction evaluates a polynomial at a base, taken modulo a number:
#
#     H(s) = (c0 * B^1 + c1 * B^2 + ... + cn * B^(n+1)) mod M
#
# Each character gets its own power of B, so order matters.

def rabin(text: str, base: int = 256, modulus: int = 256) -> int:
    h = 0
    for ch in text:
        h = (h * base + ord(ch)) % modulus
    return h


# A tiny modulus keeps only the last few characters' worth of information, so
# strings that agree at the end collide.
small, big = rabin("ab", modulus=256), rabin("cb", modulus=256)
print(f"modulus 256:      H('ab') = {small}   H('cb') = {big}   "
      f"{'COLLIDE' if small == big else 'differ'}")
print()
print("With modulus 256 only the final character survives, so anything that")
print("ends the same way collides.  With a big prime, collisions are rare.")
print()

# A composite modulus built out of the base is worse:
# modulus 256^3, every character before the last three gets weight 256^3 or
# more, which is 0 mod M.  Only the final three characters affect the result.
M_COMPOSITE = 256 ** 3                      # 16777216 = 256 * 256 * 256
M_PRIME = 2**61 - 1                         # a Mersenne prime
for s, t in [("ab", "cb"), ("helloabc", "worldabc"), ("pay now", "refund now")]:
    h1, h2 = rabin(s, 256, M_COMPOSITE), rabin(t, 256, M_COMPOSITE)
    j1, j2 = rabin(s, 256, M_PRIME), rabin(t, 256, M_PRIME)
    print(f"{s!r:>12} vs {t!r:>12}:  mod 256^3 -> {h1} / {h2} "
          f"{'COLLIDE' if h1 == h2 else 'differ':>8}   "
          f"mod 2^61-1 -> {'COLLIDE' if j1 == j2 else 'differ'}")
print()
print("Over a prime field the collisions are governed by a clean polynomial")
print("count; over a composite modulus an attacker factors M and attacks each")
print("factor separately, which is why fingerprints always use prime moduli.")
print()

# Order information survives a large modulus: 'ab' and 'ba' get different
# values because the characters land on different powers of B.
a, b = rabin("ab", 256, M_PRIME), rabin("ba", 256, M_PRIME)
print(f"H('ab') = {a}   H('ba') = {b}   {'COLLIDE' if a == b else 'differ'}")
print()
print("Where primes show up in ordinary code:")
print("  * hash table sizes are often prime, so 'value mod size' spreads keys")
print("    out evenly instead of piling them onto shared factors")
print("  * CRC and Rabin fingerprints use a prime field so collisions are rare")
print("  * Diffie-Hellman and ElGamal need a prime modulus and a generator")
print("  * the Mersenne Twister (Python's random) has prime period 2^19937 - 1")
print("  * SHA-256 adds up words modulo the prime 2^32 - 5")
```

### 7. Primes in the systems you use

```python
import math
import random
from math import isqrt


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    for d in range(3, isqrt(n) + 1, 2):
        if n % d == 0:
            return False
    return True


def next_prime(n: int) -> int:
    """Smallest prime greater than n.  Systems use this to pick a hash table
    size, or to search for an RSA prime."""
    candidate = n + 1
    if candidate % 2 == 0:
        candidate += 1
    while not is_prime(candidate):
        candidate += 2
    return candidate


print("next prime above various sizes:")
for s in (10_000, 100_000, 1_000_000, 10_000_000):
    p = next_prime(s)
    print(f"   above {s:>12,} -> {p:>12,}   ({p - s} steps of 2)")
print()

# Random numbers: the standard library's Mersenne Twister is fast and fine for
# simulation, but it is completely predictable from 624 outputs, so it must
# never be used for keys or passwords.
print("Mersenne Twister warning:")
seeded = random.Random(1234)
print("   Random(1234) three draws:", [round(seeded.random(), 6) for _ in range(3)])
a, b = random.Random(99), random.Random(99)
print(f"   Random(99) twice in a row: {a.random()} and {b.random()} (identical)")
print("   'secrets' is the module to use for tokens and keys, not 'random'.")
print()


def sieve_primes(limit: int) -> list[int]:
    flags = [True] * (limit + 1)
    flags[0] = flags[1] = False
    p = 2
    while p * p <= limit:
        if flags[p]:
            for k in range(p * p, limit + 1, p):
                flags[k] = False
        p += 1
    return [i for i, f in enumerate(flags) if f]


# The distribution of primes gets thinner as numbers grow, so picking a large
# prime is not free: the average gap near n is about ln(n).
print("average gap between consecutive primes, by size:")
for limit in (10**2, 10**3, 10**4, 10**5, 10**6):
    ps = sieve_primes(limit)
    gaps = [b - a for a, b in zip(ps, ps[1:])]
    avg = sum(gaps) / len(gaps)
    print(f"   below {limit:>9,}: {len(ps):>7,} primes, average gap {avg:5.2f}, "
          f"ln(limit) = {math.log(limit):5.2f}")
print()
print("Average gap tracks ln(n).  A 2048-bit prime needs about 1400 tries on")
print("average, which is why real libraries use Miller-Rabin rather than trial")
print("division -- 2048 candidates per test is hopeless at that size.")
```

## Common Mistakes

**Wrong.** `if n % 2 == 0: return n == 2; return True`

```python
def is_prime(n):
    return n % 2 != 0 or n == 2      # 9 is odd, so this calls 9 prime
```

**Right.**

```python
from math import isqrt


def is_prime(n):
    if n < 2:
        return False
    for d in range(2, isqrt(n) + 1):
        if n % d == 0:
            return False
    return True


print([n for n in range(2, 30) if is_prime(n)])
```

Why the wrong version is tempting: it reads like the definition ("a prime is not
divisible by two"), and it passes every casual test with small even numbers. The
trap is that checking 2 is not checking all primes.

---

**Wrong.** Testing divisors up to `n` instead of up to `sqrt(n)`.

```python
def factor(n):
    for d in range(2, n):
        if n % d == 0:
            return d
```

**Right.**

```python
from math import isqrt


def factor(n):
    for d in range(2, isqrt(n) + 1):
        if n % d == 0:
            return d
    return None


print("smallest prime factor of 2024:", factor(2024))
```

Why the wrong version is tempting: it is obviously correct, since you checked
everything. The cost is the whole point: `n = 2**31 - 1` is a prime, so the
loop runs 2.1 billion times, and a 2048-bit number would run about 10^308 times.
The insight you must add is that factors come in pairs, so if `d | n` then
`n/d | n`, and at least one of the two is at most `sqrt(n)`.

---

**Wrong.** Returning the last non-zero remainder by remembering it in a variable
initialised to `b`.

```python
def gcd_wrong(a, b):
    g = b
    while b:
        a, b = b, a % b
        g = b
    return g


print("gcd_wrong(1071, 462) =", gcd_wrong(1071, 462))
```

**Right.**

```python
def gcd_right(a, b):
    while b:
        a, b = b, a % b
    return a


print("gcd_right(1071, 462) =", gcd_right(1071, 462))
```

Why the wrong version is tempting: it looks symmetric with the loop body. But
`a` already *is* the answer when the loop exits — after the final swap, `b` is 0
and `a` holds the last non-zero remainder. Writing `g = b` captures the zero and
returns 0.

---

**Wrong.** Assuming a composite number might have a prime factor bigger than its
square root, and so sieving to `n`.

**Right.** Composite `c = a·b` with `a ≤ b` has `a² ≤ c`, so `a ≤ sqrt(c)`.
Sieve to `sqrt(n)` and stop.

Why the wrong version is tempting: "I want to be sure I catch every composite"
feels safer than an inequality you have not checked. Here the inequality is the
entire algorithm.

---

**Wrong.** Calling the number of primes below `N` "the density of primes", then
concluding primes are common because there are lots of them.

**Right.** The *density* is `π(N)/N ≈ 1/ln N`, which goes to **zero**. There are
infinitely many primes (Euclid, [Lesson 24](../part02_discrete_combinatorics/24_recurrence_relations.md)
for the counting side) but they get rarer and rarer, which is exactly why
finding a 2048-bit prime takes a variable number of tries.

## Formula Sheet

Every formula, notation and definition this lesson uses. Symbols follow
[SYMBOLS.md](../../SYMBOLS.md). A prime is always taken positive.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$a \mid b$` | `$b = a \cdot k$` for some integer `k` | `a` divides `b`: `b` is a whole-number multiple of `a` | any divisibility test; in Python, `b % a == 0` |
| `$a \parallel b$` | `$a \mid b$ and $b \nmid a$` | `a` divides `b` but `b` does not divide back — a *proper* divisor | separating a real factor from the degenerate cases `a = 1` and `a = b` |
| `$b = a \cdot q + r$` with `$0 \le r < a$`, `$a > 0$` | division algorithm | dividing `b` by `a` has exactly one quotient `q` and exactly one remainder `r` in that range | this is *why* `a mod b = r` is a function and not a relation; it is the reason `%` is well defined |
| `divmod(b, a)` | returns the pair `(q, r)` | both halves of one division in a single call | the body of the Euclidean loop, and asserting `0 <= r < a` |
| `$\gcd(a,b)$` | the largest `d > 0` with `d \mid a` and `d \mid b` | the biggest factor the two numbers share | reducing fractions; the input to everything in [Lesson 111](111_modular_arithmetic_and_crypto.md) |
| `$\mathrm{lcm}(a,b)$` | `$a \cdot b \,/\, \gcd(a,b)$`, and `a*b == gcd*lcm` | the smallest positive number both `a` and `b` divide | common denominators. The division is needed because `a * b` counts every *shared* prime factor twice |
| `$n = p_1^{e_1} \cdots p_k^{e_k}$` | Fundamental Theorem of Arithmetic | every integer above 1 has exactly one prime factorisation, up to reordering | gives every integer a canonical form — the reason "the same integer" is a well defined idea at all |
| `$\gcd(a,b) = \gcd(b,\; a \bmod b)$` | the one-line reduction | the gcd of two numbers equals the gcd of the smaller number and the remainder | the body of the Euclidean loop, and a strictly decreasing measure of progress |
| `$\Theta(\log \min(a,b))$` | divisions performed by Euclid on input `(a, b)` | the step count tracks the number of **bits** in the input, not the size of the input | complexity claims about gcd; `O(log n)` on an `n`-bit input is linear in the input as written |
| `$F_1 = F_2 = 1$`, `$F_{k+2} = F_{k+1} + F_k$` | Fibonacci sequence | consecutive Fibonacci numbers are the slowest-shrinking pair Euclid can meet, so they are the worst case | makes the `Θ(log min(a,b))` bound *tight* rather than merely true; Lamé's theorem |
| `$a_{i+2} < a_i / 2$` | the halving argument | the working value drops by at least half every **two** steps | the proof that the logarithm is the right bound |
| `$\gcd(a,b) = s \cdot a + t \cdot b$` | Bézout's identity | some whole-number combination of `a` and `b` equals their gcd — and `s`, `t` may be negative | the extended Euclidean algorithm; a *certificate* for a gcd, and the gateway to [Lesson 111](111_modular_arithmetic_and_crypto.md) |
| `$s = s_0 + k\frac{b}{g}$`, `$t = t_0 - k\frac{a}{g}`, `k ∈ ℤ`, `g = gcd(a,b)` | all Bézout solutions | one solution generates every other one. For this lesson's `a = 1071`, `b = 462`, `g = 21`: `s = -3 + 22k`, `t = 7 - 51k` | the `for k in range(4)` search in Runnable Code 3; reducing `s` modulo `m` gives the canonical modular inverse |
| `$a^{-1} \bmod m$ exists $\iff \gcd(a,m) = 1$` | Bézout corollary | an inverse is exactly a solution of `s*a + t*m = 1`; `1` is reachable only if `gcd(a, m) = 1` | deciding whether `pow(a, -1, m)` is even legal in Python |
| `n` prime `$\iff$` no `d` with `2 <= d <= isqrt(n)` divides `n` | trial division up to the square root | small factors come in pairs (`d` and `n/d`), so at least one of each pair is `≤ sqrt(n)` | the naive `is_prime` in the code. **Restriction:** real libraries use Miller–Rabin, because a 2048-bit candidate would need 2048 trial divisions |
| `$\pi(N)$` | the number of primes `≤ N` | how many primes are up to here | prime density; `pi(10^6) = 78,498` |
| `$\pi(N) \approx N / \ln N$`, so density `$\pi(N)/N \approx 1/\ln N$` | asymptotic prime number theorem | the *fraction* of integers that are prime falls without bound, even though there are infinitely many primes | why finding a 2048-bit prime takes about `ln(2^2048) ≈ 1419` tries on average |
| `$n < p < 2n$` for some prime `p`, `n > 1` | Bertrand's postulate | there is always a prime strictly between `n` and `2n` | prime gaps are bounded, so `next_prime` always terminates |
| `$\sum_{p \le \sqrt N,\; p \ \mathrm{prime}} \frac{N}{p} = \Theta(N \ln \ln N)$` | crossings-out performed by the sieve | the reciprocal sum over primes behaves like `ln ln N`, not like `ln N` | the sieve is `Θ(N ln ln N)` time and `Θ(N)` space, not `Θ(N²)` |
| `$\Theta(\sqrt n)$` | trial-division divisions needed to factor `n` | the loop cannot stop before `d * d > n`, because that is where the smallest factor can hide | why a semiprime is expensive: `sqrt(n)` is exponential in the bit length of `n` |
| `$\approx n^{1/4}$` | Pollard's rho, to expose a factor `p` | it needs about the square root of the *factor*, not of `n` | stripping small factors quickly before a full factoring run |
| `$\exp\!\big((64/9)^{1/3}(\ln n)^{1/3}(\ln \ln n)^{2/3}\big)$` | GNFS cost | subexponential — faster than any `2^{n^ε}` and slower than any polynomial in `log n` | the asymptotically best known general factoring estimate |
| `$\mathrm{digits} \approx \mathrm{bits} \cdot 0.30103$` | `log10(2) ≈ 0.30103` | a 3072-bit modulus is about 925 decimal digits | converting a key size into a workload: trial division on 925 digits needs about `10^462` steps |
| `$H(c_0 \cdots c_{k-1}) = c_0 B^{k-1} + c_1 B^{k-2} + \cdots + c_{k-1} \pmod M$` | `c_i` = code of the `i`-th character, most significant **first**; exactly what `h = (h*base + ord(ch)) % modulus` computes. With `B = M = 256`: `H("ab") = 98` | read the string as a base-`B` number and reduce. Order matters, because each character lands on its own power of `B` | cheap string comparison; CRC and Rabin fingerprints; `H("ab") = 24930` but `H("ba") = 25185` under `M = 2^61 - 1` |
| `$h \leftarrow (h B - c_{\mathrm{out}} B^{m} + c_{\mathrm{in}}) \bmod M$` | sliding the window forward one position | subtract the outgoing character's weight, add the incoming one | turns each window from `O(m)` into `O(1)` — the rolling update in Exercise 5 |
| `$\varphi(n) = n\prod_{p \mid n}\left(1 - \frac{1}{p}\right)$` | Euler's totient | how many integers in `1..n` are coprime to `n` | the number RSA hides. `φ(360) = 96`, `φ(3233) = φ(61·53) = 3120` |
| `$\varphi(pq) = (p-1)(q-1) = n - p - q + 1$` | for distinct primes `p`, `q`, with `n = pq` | inclusion–exclusion: `n - n/p - n/q + n/(pq)` collapses because `n/(pq) = 1` | what an RSA attacker is refused: the value is one factoring step away. Used in Exercise 4, and in [Lesson 111](111_modular_arithmetic_and_crypto.md) |

## Multiple Choice Questions

**Q1.** Running the Euclidean algorithm on `a = 1071` and `b = 462`, what comes out, and how many divisions does it take?

- A) 147, in 2 divisions
- B) 21, in 3 divisions
- C) 42, in 3 divisions
- D) 21, in 4 divisions

<details>
<summary>Answer and explanation</summary>

**B) 21, in 3 divisions.**

The three divisions are `1071 = 2·462 + 147`, `462 = 3·147 + 21`, and
`147 = 7·21 + 0`. The last **non-zero** remainder is 21, and three divisions were
performed, which is what the lesson's `euclid(1071, 462)` prints.

Option A is the trap: 147 is only the *first* remainder. It is a valid common
divisor of nothing relevant — `462 / 147` is not an integer, so 147 is not even a
divisor of 462. Option C comes from doubling the answer, which is what happens if
you keep the result of `a % b` in the wrong variable. Option D counts the final
swap that sets `b = 0` as if it were another division; the loop condition
`while b != 0` is what detects the end, and the third division is the one that
produces the zero remainder.

</details>

**Q2.** The lesson's `factor` function stops at `isqrt(n)`. Which statement actually
justifies that?

- A) Every composite has a factor pair `(d, n/d)`, and in every such pair at least one factor is `≤ sqrt(n)`
- B) Every prime factor of a composite `n` is at most `sqrt(n)`
- C) The largest divisor of a composite `n` is at most `sqrt(n)`
- D) `isqrt(n)` is faster than `int(n ** 0.5)` and correctness follows from speed

<details>
<summary>Answer and explanation</summary>

**A) Every composite has a factor pair `(d, n/d)`, and in every such pair at least one factor is `≤ sqrt(n)`.**

Write the composite as `n = d · e` and order it so `d ≤ e`. Then
`d² ≤ d·e = n`, so `d ≤ sqrt(n)`. So the *smallest* factor is always within reach.

Option B is false and the counterexample is small: `6 = 2 · 3` is composite, and
its prime factor 3 is larger than `sqrt(6) ≈ 2.45`. This is the single most common
misstatement of the argument, and it is tempting because "small factors are what we
look for" feels like the same claim.

Option C is false for the same number: the largest divisor of 6 is 6 itself, far
above `sqrt(6)`. Confusing "largest" with "smallest" is what produces this option.

Option D confuses a performance detail with a correctness argument. `isqrt` is
indeed exact where `n ** 0.5` can round, but that is a numerical-accuracy
argument, not a reason the search may stop. Loop bounds and correctness are
separate questions, and conflating them is a classic source of silent bugs.

</details>

**Q3.** The `Common Mistakes` section shows `return n % 2 != 0 or n == 2` as a wrong
primality test. It correctly rejects every even `n > 2`, so the first failure must be
odd. What is the smallest `n` it wrongly reports as prime, and why?

- A) 9, because 3 divides 9 and the test never tries a divisor other than 2
- B) 15, because 5 divides 15 and the test never tries a divisor other than 2
- C) 25, because 5 divides 25 and the test never tries a divisor other than 2
- D) 27, because 3 divides 27 and the test never tries a divisor other than 2

<details>
<summary>Answer and explanation</summary>

**A) 9, because 3 divides 9 and the test never tries a divisor other than 2.**

`9 % 2 = 1`, so `9 % 2 != 0` is true and the whole expression short-circuits to
True — the test calls 9 prime. But `9 = 3 · 3`. Every odd number below 9 is
either 1, 3, 5 or 7, and the test's answer happens to be right for all of them,
which is exactly why this bug survives casual testing.

Options B, C and D are also odd composites that the test accepts, and the reasoning
in each is identical and correct — the diagnosis is right and only the *smallest*
counterexample is wrong. 9, 15, 25 and 27 are 9 < 15 < 25 < 27, so 9 is the first
one you meet. This is worth internalising: in a lesson about primality, 9 is the
canonical witness, and any test that only rules out the divisor 2 is not a primality
test at all.

</details>

**Q4.** With `base = 256` and `M = 2^24 = 16,777,216`, the lesson's fingerprint
`H` reads the string most-significant-character-first. Which statement is true?

- A) `H` cannot distinguish the **first** character of any 4-character string, because `256^3 = 2^24 ≡ 0 (mod M)`
- B) `H` cannot distinguish the **last** character of any 4-character string, because `256^3 = 2^24 ≡ 0 (mod M)`
- C) `H` cannot distinguish the last character of any 3-character string, because `256^2 = 65,536 ≡ 0 (mod M)`
- D) `H` distinguishes every character, because `2^24` is a large modulus

<details>
<summary>Answer and explanation</summary>

**A) `H` cannot distinguish the first character of any 4-character string, because
`256^3 = 2^24 ≡ 0 (mod M)`.**

For a 4-character string the running value is
`H = c_0·256^3 + c_1·256^2 + c_2·256 + c_3 (mod 2^24)`, and the leading term is
exactly `2^24` times `c_0`, which vanishes. So `H` is a function of the last three
characters only. You can watch it happen: `H("Xabc") = H("zabc") = H(" habc") = 6,382,179`.
Worse, `H("abc")` is also 6,382,179 — the fingerprint cannot even see how long the
string is.

Option B is the most tempting wrong answer, because the lesson's own loop keeps the
*most recent* character at the low-order end, so it is natural to assume the newest
character is the fragile one. The weights run the other way: the newest character
has weight `256^0 = 1`, the most fragile position is the far end, `B^3`.

Option C fails on arithmetic: `256^2 = 65,536`, and `65,536` is not a multiple of
`16,777,216`. The collapse needs a power of the base that is a multiple of the
modulus, and `256^3` is the first one.

Option D is a size argument, and size is the wrong variable. The danger here is not
that `2^24` is small in absolute terms; it is that `2^24` is a *power of the base*.
The general rule, which Exercise 6 develops, is that a modulus sharing a factor with
the base is the problem. Swapping in the prime `2^61 - 1` gives
`H("Xabc") = 1,482,777,187` and `H("zabc") = 2,053,202,531`, and the collapse is gone.

</details>

**Q5.** The lesson states that a 2048-bit RSA prime needs "about 1400 tries on
average". Which pair of statements produces that number?

- A) The prime density is `1/ln N`, and `ln(2^2048) = 2048·ln 2 ≈ 1419`, so one in about 1419 candidates is prime
- B) The prime density is `ln N / N`, and there are about 1400 primes below `2^2048`
- C) The prime density is `1/N`, so finding a prime takes `2^2048` tries
- D) The prime density is `1/ln N`, and `2^2048 / ln(2^2048)` tries are needed

<details>
<summary>Answer and explanation</summary>

**A) The prime density is `1/ln N`, and `ln(2^2048) = 2048·ln 2 ≈ 1419`, so one in
about 1419 candidates is prime.**

This is Bertrand's postulate made quantitative: the average gap between consecutive
primes near `N` is about `ln N`, so if you test candidates spaced one apart, roughly
every `ln N`-th one hits. With `N = 2^2048`, `ln N = 2048 · 0.693147 ≈ 1419.4`.

Option B inverts the ratio. `ln N / N` is a vanishing number, not a count; the count
of primes below `N` is `π(N) ≈ N / ln N`, which is astronomically large, but that is
the count over an *enormous* interval, not the local success rate of a single
candidate.

Option C uses the density of primes among *all* integers below `1`, which is
meaningless — the density is not `1/N`, and `2^2048` tries is not an average but a
count of all the candidates in existence.

Option D is the right ingredients arranged into the wrong formula. Dividing the
number of candidates by the density gives a rate per *unit length*, not the number
of trials. The whole answer is that "one in `ln N`" is already a rate.

</details>

**Q6.** The sieve is `Θ(N ln ln N)` rather than `Θ(N²)`. What is doing the work?

- A) Only multiples of primes up to `sqrt(N)` are crossed out, and `Σ 1/p` over primes behaves like `ln ln N`
- B) The outer loop only runs to `sqrt(N)`, so the total work is `N^{3/2}`
- C) Crossings-out are independent, so a machine with many cores does less total work
- D) Each pass only crosses out even multiples, halving the work once per prime

<details>
<summary>Answer and explanation</summary>

**A) Only multiples of primes up to `sqrt(N)` are crossed out, and `Σ 1/p` over
primes behaves like `ln ln N`.**

Prime `p` does about `N/p` crossings-out, so the total is
`Σ_{p ≤ sqrt(N)} N/p = N · Σ 1/p`. The reciprocal sum over primes up to `x` grows
like `ln ln x`, which is why the bound carries a double logarithm: the outer `ln`
is the harmonic series, and the inner `ln` is the prime-sparseness correction.

Option B confuses the loop bound with the work inside the loop. Stopping the outer
loop at `sqrt(N)` is a *correctness* argument (every composite has a factor below
`sqrt(N)`), not a savings estimate; each pass still walks `N/p` entries.

Option C is a real effect but it is a wall-clock effect, not a change in the
operation count. The single-threaded count is unchanged, and the asymptotic statement
in the lesson is about that count.

Option D describes one of the micro-optimisations the code actually does — the mark
loop starts at `p*p`, which skips the `p` multiples below `p²` — but "halving once
per prime" is not the mechanism. Primes halve nothing; the saving comes from summing
`1/p` over *fewer and fewer* primes as `p` grows.

</details>

**Q7.** The lesson finds `21 = -3·1071 + 7·462`, so `gcd(1071, 462) = 21`. Which of
the following is *also* a valid Bézout identity for the same pair?

- A) `19·1071 - 44·462 = 21`
- B) `3·1071 + 7·462 = 6,447`
- C) `3·1071 - 7·462 = -21`
- D) `22·1071 + 51·462 = 47,118`

<details>
<summary>Answer and explanation</summary>

**A) `19·1071 - 44·462 = 21`.**

`19·1071 = 20,349` and `44·462 = 20,328`, and `20,349 - 20,328 = 21`. This is the
lesson's own general rule with `k = 1`: `s = s_0 + k·b/g = -3 + 462/21 = -3 + 22 = 19`
and `t = t_0 - k·a/g = 7 - 1071/21 = 7 - 51 = -44`.

Option B has the right magnitudes and the wrong sign on `s`: `3·1071 + 7·462 =
3,213 + 3,234 = 6,447`, not 21. Flipping the sign of one Bézout coefficient is
very easy to do by hand, precisely because Bézout coefficients are *not* required to
be positive and `-3` looks like it wants a plus sign.

Option C gets the shape exactly right — the correct step sizes in the correct
directions — and still fails, because both coefficients ended up negated, so the
sum is `-gcd` rather than `+gcd`. `3·1071 - 7·462 = 3,213 - 3,234 = -21`. This is
the near-miss that catches people out: it produces a number of the right magnitude,
just the wrong one, and it will survive any check that only compares absolute values.

Option D uses `22` and `51`, which are the *step sizes* `b/g` and `a/g`, in place of
the coefficients. `22·1071 + 51·462 = 23,562 + 23,562 = 47,118` — and note that
23,562 is precisely the `lcm(1071, 462)` from the worked example. Mixing up the
coefficients with the step sizes of the general solution is the most common way to
lose points on this family of questions.

</details>

**Q8.** The lesson says public-key cryptography rests on an asymmetry. Which row of
that table is the real one?

- A) Trial division is polynomial in the bit length of `n`; modular exponentiation is not
- B) Multiplying two `n`-bit numbers and computing `a^k mod n` by repeated squaring are polynomial in `n`; recovering `p` from `n = pq` is believed not to be
- C) Both factoring and modular exponentiation are believed to require superpolynomial time
- D) Factoring a 3072-bit modulus is believed to cost exponential time in the *decimal digit count*, which grows linearly with the bit length

<details>
<summary>Answer and explanation</summary>

**B) Multiplying two `n`-bit numbers and computing `a^k mod n` by repeated squaring
are polynomial in `n`; recovering `p` from `n = pq` is believed not to be.**

The two operations an RSA *user* performs are the easy direction. `pow(m, e, n)` in
Python is `O(log e)` modular multiplications. The one operation an RSA *attacker*
wants — turning `n` into `p` — is the hard direction, believed to need
`exp((64/9)^{1/3} (ln n)^{1/3} (ln ln n)^{2/3})` steps.

Option A swaps the two columns. Trial division costs `Θ(sqrt(n))` divisions, and
`sqrt(n) = 2^{n/2}`, which is exponential in the bit length `n`. Modulo exponentiation
by repeated squaring is `O(log k)` multiplications, i.e. linear in the bit length of
the exponent.

Option C is wrong about the easy half, which is the whole point: if computing
`a^k mod n` were hard, a legitimate key holder could not encrypt either. The
practicality of encryption is exactly what makes the asymmetry worth paying for.

Option D is the subtlest wrong answer, and it is a units error. A 3072-bit modulus
is about 925 decimal digits (`3072 · 0.30103 ≈ 924.6`). Cost `exp(c·(ln n)^{1/3}
(ln ln n)^{2/3})` is exponential in the **bit length** and merely subexponential in
the digit count, which is a *linear* function of the bit length. The reason 3072
bits is considered safe is precisely that the cost is not exponential in the number
of digits a human writes down.

</details>

**Q9.** The lesson computes `lcm(1071, 462) = 23,562` as `|a·b| / gcd(a,b)`. Why is
the division necessary, and what would you get without it?

- A) `a·b` counts each shared prime factor twice — here `1071 = 3²·7·17` and `462 = 2·3·7·11` share `3·7 = 21` — so the true common multiple is smaller; without the division you would get 494,802, which is `gcd · lcm`, not the lcm
- B) The division is needed only to make the result an integer
- C) The lcm of two integers is always prime, so the division strips off the composite part
- D) The gcd and the lcm are unrelated quantities; the formula happens to work for this pair

<details>
<summary>Answer and explanation</summary>

**A) `a·b` counts each shared prime factor twice — here `1071 = 3²·7·17` and
`462 = 2·3·7·11` share `3·7 = 21` — so the true common multiple is smaller; without
the division you would get 494,802, which is `gcd · lcm`, not the lcm.**

The identity is `a · b = gcd(a,b) · lcm(a,b)`, and it is exact: `494,802 = 21 ·
23,562`. The lesson's own checks confirm it, `1071 × 22 = 23,562` and
`462 × 51 = 23,562`, while `1071 × 462` is 194 times larger than that.

Option B gets the arithmetic backwards. Division by the gcd is not a formatting step
— `1071 · 462 / 21` is an integer because the gcd divides the product, and the
formula works precisely *because* it factors out the duplication.

Option C is nonsense on its face, and it is included because "least common multiple"
invokes the word "multiple", which novices sometimes read as "must be prime". The lcm
of 1071 and 462 is 23,562, which is manifestly composite.

Option D denies an identity the lesson relies on. The formula is universal: writing
`a = g·a'`, `b = g·b'` with `gcd(a', b') = 1`, the smallest common multiple is
`g·a'·b' = a·b/g`, and it is *because* `a'` and `b'` are coprime that no further
factor can be removed. This is the same coprimality condition that
`a^{-1} mod m` needs in [Lesson 111](111_modular_arithmetic_and_crypto.md).

</details>

**Q10.** The sieve's outer loop condition is `while p * p <= N`. Suppose it were
changed to `while p <= N`. What happens?

- A) Nothing breaks and nothing is missed: for every `p > sqrt(N)` the marking range `range(p*p, N+1, p)` is empty, so the extra cost is only the wasted outer-loop iterations
- B) Composites between `sqrt(N)` and `N` would be missed, because the sieve needs every prime up to `N` as a base prime
- C) The sieve would run in `Θ(N^{3/2})` time instead of `Θ(N ln ln N)`
- D) The sieve would mark the primes themselves as composite, since a pass starting at `p*p` can still reach `p`

<details>
<summary>Answer and explanation</summary>

**A) Nothing breaks and nothing is missed: for every `p > sqrt(N)` the marking range
`range(p*p, N+1, p)` is empty, so the extra cost is only the wasted outer-loop
iterations.**

This is a genuinely surprising result and worth computing rather than guessing. Once
`p > sqrt(N)` we have `p·p > N`, so `range(p*p, N+1, p)` is the empty range and the
inner loop body never executes. Correctness is already complete by the time
`p = sqrt(N)`, because every composite `c ≤ N` has a prime factor `≤ sqrt(c) ≤
sqrt(N)`. The relaxed loop therefore returns the identical `is_prime` list, at the
cost of `N - sqrt(N)` extra iterations that do nothing.

Option B is the intuition that the `sqrt(N)` bound was chosen to *save work*. It
was not — it was chosen for *correctness*, and there is no composite in
`(sqrt(N), N]` that a prime below `sqrt(N)` failed to cross out.

Option C is the plausible-looking cost objection, and it is quantitatively wrong: no
extra markings are performed at all, so the count of crossings-out is unchanged and
the Θ class is unchanged. The only extra work is the linear scan for `p > sqrt(N)`.

Option D confuses the start of the marking range with the prime being sieved. A pass
marks `p², p²+p, …`, all of which exceed `p`, so `p` itself is never marked by its own
pass. A prime is only ever crossed out if some *smaller* prime divides it, which is
impossible. This is also why the code sets `is_prime[0] = is_prime[1] = False`
manually — 0 and 1 are never crossed out by anybody.

</details>

## Subjective Questions

### Short Answer

**Q1. State the division algorithm and say why it is the reason `a mod b` is a
function rather than a relation.**

<details>
<summary>Model answer</summary>

For any integer `b` and any positive integer `a`, there exist unique integers `q`
and `r` with

```
b = a·q + r        and        0 <= r < a
```

The uniqueness of `r` in that range is the whole point. Division in Python and in
every other language leaves a remainder, and if two different remainders could both
legitimately be "the remainder", then `a mod b` would be a *relation* — several
values related to the input — rather than a function. The theorem says exactly one
value is admissible, so `a mod b` is well defined everywhere and `divmod(b, a)` has
a single answer. Every later construction in this part, congruences, inverses and the
Chinese Remainder Theorem, is built on `r` being unique.

</details>

**Q2. What is the Euclidean algorithm's loop invariant, and what does it become at
termination?**

<details>
<summary>Model answer</summary>

The loop invariant is `gcd(a, b) = gcd(a0, b0)` for the *original* input pair
`(a0, b0)`: at every point in the loop, the current `(a, b)` is some pair with the
same set of common divisors as the input. It holds on entry trivially, and the
lemma `gcd(a, b) = gcd(b, a mod b)` preserves it on each iteration.

At termination `b = 0`, and the invariant then reads `gcd(a, 0) = gcd(a0, b0)`. Since
0 is a multiple of every integer, the divisors of `(a, 0)` are exactly the divisors
of `a`, so `gcd(a, 0) = a`. The loop returns `a`, and the invariant turns that into
the claim we wanted. Termination is proved separately, by noting that `a` strictly
decreases once `b < a`.

</details>

**Q3. State Bézout's identity and the condition under which `a` has a modular
inverse modulo `m`.**

<details>
<summary>Model answer</summary>

Bézout's identity: for any integers `a, b` there exist integers `s, t` with
`gcd(a, b) = s·a + t·b`. The coefficients may be negative, and are not unique —
all solutions are `s = s0 + k·b/g`, `t = t0 - k·a/g` for `g = gcd(a, b)`.

For the inverse, set `g = gcd(a, m)`. If `g = 1` then 1 is a multiple of `g`, so the
identity gives `s·a + t·m = 1` for some integers. Reducing mod `m`, the second term
vanishes and `s·a ≡ 1 (mod m)`, so `s` is the inverse of `a` modulo `m`. If
`g > 1`, no such `s` can exist, because `s·a` is a multiple of `g` and can never be
`≡ 1 (mod m)`. So the inverse exists **exactly when `gcd(a, m) = 1`**.

</details>

**Q4. Why does the sieve only need base primes up to `sqrt(N)`, and what time bound
does that give?**

<details>
<summary>Model answer</summary>

Let `c ≤ N` be composite. Then `c = d·e` with `1 < d ≤ e`, so `d² ≤ d·e = c ≤ N`,
giving `d ≤ sqrt(N)`. And `d` has some prime factor `p ≤ d ≤ sqrt(N)`, so `p` is one
of the base primes the sieve processes, and `c ≥ p²`, meaning `c` is crossed out
during `p`'s pass. No prime above `sqrt(N)` is needed.

The work is therefore `Σ_{p ≤ sqrt(N), p prime} N/p = N · Σ 1/p`. The reciprocal
sum over primes behaves like `ln ln N`, so the sieve is `Θ(N ln ln N)` time and
`Θ(N)` space — not `Θ(N²)`, because we only touch multiples of *primes*, and we
skip everything below `p²`.

</details>

**Q5. `pi(N) ≈ N / ln N` implies the density of primes is `≈ 1/ln N`. How does that
square with "there are infinitely many primes", and what does it cost in practice?**

<details>
<summary>Model answer</summary>

There is no contradiction. `N / ln N` grows without bound — slowly, but
unboundedly — so the *count* of primes goes to infinity while the *fraction* of
integers that are prime, `1/ln N`, goes to zero. Infinitely many primes that are
progressively rarer is exactly what the two statements say together.

In practice the local gap matters: by Bertrand's postulate there is always a prime
between `n` and `2n`, and on average the gap near `N` is about `ln N`. So testing
candidates spaced 2 apart below `N` hits a prime roughly every `ln N` tries. For a
2048-bit RSA prime, `ln(2^2048) ≈ 1419` tries on average — and because the gaps vary,
the actual number is a random variable with an unbounded tail, which is why key
generation has no fixed cost.

</details>

**Q6. Give the closed form of the lesson's Rabin fingerprint after `k` characters,
and say which position in the string a modulus can silently erase.**

<details>
<summary>Model answer</summary>

The code computes `h = (h*base + ord(ch)) % modulus` from `h = 0`, so after `k`
characters

```
H(c0 c1 ... c_{k-1}) = c0·B^{k-1} + c1·B^{k-2} + ... + c_{k-1}   (mod M)
```

where `c_i` is the code of the `i`-th character. The **first** character therefore
carries the *highest* power of the base, and the most recent character carries
weight `B^0 = 1`.

A modulus erases the far end. If `B^t ≡ 0 (mod M)` for some `t`, then in any string
of length `≥ t` the term `c_0·B^{t-1}` vanishes, and the fingerprint cannot see the
first character at all. With `B = 256` and `M = 2^24`, `256^3 = 2^24 ≡ 0`, so
`H("Xabc") = H("zabc") = 6,382,179`. This is exactly the failure the lesson's
"composite modulus is a liability" warning is about; Exercise 6 develops it.

</details>

### Long Answer

**Q1. The lesson says the whole of public-key cryptography rests on factoring being
hard. What exactly is the assumption, and what would break the argument if it
turned out to be false?**

<details>
<summary>Model answer</summary>

The assumption is narrow and it is an assumption, not a theorem. Precisely: *no
probabilistic polynomial-time algorithm is known that, given a modulus `n = pq` with
`p` and `q` distinct primes of comparable size, outputs `p` or `q`.* Nobody has
proved this; nobody has proved the opposite either. "Factoring is hard" is not even
true as a blanket statement, and the qualifications matter.

Factorization is *easy* for many inputs. If `n` has a factor below `10^6`, trial
division or Pollard's rho finds it in microseconds. If `n` has five or more
distinct prime factors, the ECM and quadratic-sieve methods are fast. If `n` is a
prime power, detection is easy. Only **balanced semiprimes** — the product of two
primes of roughly equal size — are believed hard, and that is exactly the shape RSA
chooses. So the security claim is: *this specific, deliberately chosen family of
numbers is hard*, and the rest is not being relied upon.

The consequence chain is short and mechanical. An attacker who factors `n = pq`
computes `φ(n) = (p-1)(q-1)` by Exercise 4's formula, computes
`d = e^{-1} mod φ(n)` by extended Euclid, and then decrypts anything: for every
ciphertext `c` produced with the public exponent `e`, `m = c^d mod n`. There is no
second line of defence — textbook RSA has exactly one secret, and it *is* the factor
pair.

What would break it: a polynomial-time factoring algorithm on classical hardware
would render every deployed RSA key forgeable the day it appeared. But note the
qualifier, because it is the part people get wrong. A *quantum* algorithm already
exists — Shor's algorithm factors in polynomial time on a sufficiently large
fault-tolerant quantum computer — and it does **not** break the argument as stated,
because the argument is about classical computation. That is precisely why
post-quantum schemes (lattice-based key exchange such as Kyber and Dilithium) exist
alongside RSA rather than instead of it. The honest statement is: RSA's security is a
belief, resting on a well-defined hardness assumption, that is only as good as our
confidence that no classical polynomial-time factoring algorithm exists.

</details>

**Q2. Why can the Euclidean algorithm not be made asymptotically faster, and what
does "optimal" mean here?**

<details>
<summary>Model answer</summary>

The bound `Θ(log min(a, b))` divisions is tight, and the tightness is a real
statement about the *problem*, not an accident of the code. Consider what a step
does. From `a_{i+1} = q·b_i + b_{i+1}` with `b_{i+1} < b_i` and `q ≥ 1` we get
`a_{i+1} ≥ b_i + b_{i+1} > 2·b_{i+1}` when `b_{i+1} < b_i`. So the working value
drops by at least a factor of 2 every *two* steps — that gives the upper bound.

For the lower bound, run the argument forwards. Since `b_{i+1} = a_{i+1} - q·b_i` and
`a_{i+1} < b_{i-1} + b_i`, the remainder satisfies
`b_{i+1} > b_{i-1} - b_i`. This is a *lower* bound on how fast the sequence may
fall, and it is minimised — the slowest possible descent — exactly when the sequence
is the Fibonacci sequence, with quotients all equal to 1. Consecutive Fibonacci
numbers are therefore the hardest input, which is Lamé's theorem: Euclid on
`(F_{k+1}, F_k)` takes exactly `k-1` divisions, and since `F_k ≈ φ^k/√5` with
`φ ≈ 1.618`, that is `Θ(log min(a, b))` steps. The lesson's Exercise 2 shows this
numerically: `(F_41, F_40) = (165,580,141, 102,334,155)` takes 39 divisions.

So "optimal" is used in a precise sense: **no algorithm of this shape — one that
repeatedly replaces the pair by the smaller number and the remainder — can use
asymptotically fewer divisions.** It is not a claim that no cleverer algorithm
exists in a different model. And on the bit level the picture is stronger still:
`O(log n)` divisions on an `n`-bit input is `O(n)` steps in the input as written, so
the algorithm is linear in the size of the problem. You cannot even read the input
in less time than that, which is the honest sense in which nothing better is
possible.

</details>

**Q3. The extended Euclidean algorithm returns a Bézout pair, but the pair is not
unique. Why is it not unique, how do you pin down a canonical one, and why does
that matter for the code that follows?**

<details>
<summary>Model answer</summary>

**Why.** Suppose `(s0, t0)` satisfies `s0·a + t0·b = g`. For any integer `k`, so does
`(s0 + k·b/g, t0 - k·a/g)`, because the added terms cancel:

```
(s0 + k·b/g)·a + (t0 - k·a/g)·b = s0·a + t0·b + k·(a·b/g) - k·(a·b/g) = g
```

The step sizes `b/g` and `a/g` come from Bézout itself: `g` is a linear combination
of `a` and `b`, and the lattice of all combinations of `a` and `b` is generated by
`(b/g, -a/g)`. The lesson's Runnable Code 3 searches exactly this family, and finds
for `(252, 105)` that `g = 21`, `s0 = -2`, `t0 = 5`, so the solutions are
`s = -2 + 5k`, `t = 5 - 12k` — giving `k = 0 → (-2, 5)`, `k = 1 → (3, -7)`,
`k = 2 → (8, -19)`, `k = 3 → (13, -31)`. All of them work, and the starting pair
checks: `-2·252 + 5·105 = -504 + 525 = 21`.

**How to canonicalise.** Reduce modulo the thing you care about. For a modular
inverse, only `s` matters modulo `m`, so the canonical answer is `s` reduced to
`[0, m)`, which `pow(a, -1, m)` in Python and `BN_mod_inverse` in OpenSSL both do
for you. The `t` coefficient is then uniquely determined.

**Why it matters.** Three practical reasons. First, correctness and
interoperability: if one library returns `s` in `(-m, 0)` and another in `[0, m)`,
their raw "inverse" outputs differ while both are right, which turns into
test failures and format bugs. Second, side channels: a variable-time search over
`k` leaks information about the secret through timing, which is why cryptographic
code uses *constant-time* reduction rather than a loop. Third, proof work: a Bézout
pair is a *certificate* of a gcd, and if you want the certificate to be short or
canonical — for a verifier, or for a published proof — you must pin `k` down
rather than return an arbitrary witness.

</details>

**Q4. The lesson warns that "a composite modulus is a liability: knowing M lets an
adversary multiply two differences together to build collisions deliberately".
State exactly when a modulus destroys a Rabin fingerprint, prove it, and explain
what to choose instead.**

<details>
<summary>Model answer</summary>

**The exact condition.** The fingerprint is safe from erasure if and only if
`gcd(base, M) = 1`. The danger is precisely that some power of the base is
`0 (mod M)`.

**Proof.** If `d = gcd(B, M) > 1`, factor `M = ∏ p_i^{a_i}` and `B = ∏ p_i^{c_i} · u`
with `c_i ≥ 1` for every `p_i` that divides `M`. Then
`B^{a_i} = ∏ p_j^{c_j a_i} u^{a_i}` is divisible by `p_i^{a_i}`, since
`c_i · a_i ≥ a_i`. Taking `t = max_i a_i` gives `B^t ≡ 0 (mod M)` for **every**
prime power in `M`, hence for `M`. So if `gcd(B, M) > 1`, a power of the base
vanishes. Conversely, if `gcd(B, M) = 1` then `B` is a unit mod `M`, so `B^t` is a
unit and in particular is never `0 (mod M)` for `t ≥ 1`. ∎

**What it costs you.** In
`H = c_0·B^{k-1} + c_1·B^{k-2} + ··· + c_{k-1}`, any term whose power is at least
`t` disappears. With `B = 256 = 2^8` and `M = 2^24`, the smallest vanishing power is
`t = 3`, so for every string of length 4 the leading character is invisible:
`H("Xabc") = H("zabc") = H(" habc") = 6,382,179`. It is worse than losing one
position: `"abc"` hashes to the same value, so length information is lost too. The
same collapse for a DNA alphabet (base 4, `M = 2^24 = 4^12`) erases the first symbol
of any 13-symbol read.

**Why an adversary can aim for it.** The lesson's intuition — multiply two
differences together — is right in the following sense. If you know `M`, you know the
vanishing power `t`, and you can place a difference at a position whose weight is
`B^{t-1} ≡ 0` while leaving every other character identical. You do not need to
search; you construct. In fact, the general construction here is even easier than
the multiplicative one: **any two strings sharing the same last `t-1` characters
collide**, whatever their prefixes and lengths.

**What to choose instead.** Pick `M` coprime to `B`, which for a prime modulus is
automatic unless `M` divides `B`. That is exactly why real fingerprints use prime
moduli: `M = 2^61 - 1` is prime, `gcd(256, 2^61-1) = 1`, no power of 256 vanishes,
and the collapse disappears — `H("Xabc") = 1,482,777,187` while
`H("zabc") = 2,053,202,531`. Primes are not safer because they are "more random";
they are safer because they have no non-trivial factors to share with the base. The
same principle is why Lesson 112 will insist that a *compression function* be a
function on the whole domain and not merely on the inputs it happens to like.

</details>

## Exercises and Solutions

**[ ] Exercise 1 —** Write `gcd_list(nums)` returning the gcd of a list, and
`lcm_two(a, b)` using `lcm = |a·b| / gcd`. Use the Euclidean algorithm, not
`math.gcd`. Verify your answers against `math.gcd` and `math.lcm` for 200 random
pairs.

<details>
<summary>Solution</summary>

```python
import math
import random


def gcd(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def gcd_list(nums: list[int]) -> int:
    g = 0                      # gcd(a, 0) = a, so this seeds the fold correctly
    for n in nums:
        g = gcd(g, n)
    return g


random.seed(1)
for _ in range(200):
    a, b = random.randint(1, 10**6), random.randint(1, 10**6)
    assert gcd(a, b) == math.gcd(a, b)
    assert lcm(a, b) == math.lcm(a, b)
    assert gcd_list([a, b, 24]) == math.gcd(math.gcd(a, b), 24)
print("all 200 random cases agree with math.gcd and math.lcm")
print("gcd_list([]) =", gcd_list([]), " gcd_list([7]) =", gcd_list([7]))
```

`gcd_list` folds from `0` because `gcd(a, 0) = a`; that makes the empty list
return `0` and a single-element list return that element.

</details>

**[ ] Exercise 2 —** Prove by hand that the Euclidean algorithm terminates in
at most `2·log₂(min(a, b)) + 1` divisions. Then verify experimentally that
consecutive Fibonacci numbers `(F_{k+1}, F_k)` are the worst case: run Euclid on
those pairs for `k = 10, 20, 40` and print the number of divisions.

<details>
<summary>Solution</summary>

*Proof sketch.* Suppose `b_{i+2} = a_{i+1} mod b_{i+1}`. Since `b_{i+2} < b_{i+1}`,
and by the division algorithm `a_{i+1} = q·b_{i+1} + b_{i+2}` with `q ≥ 1`, we
get `a_{i+1} ≥ b_{i+1} + b_{i+2} > 2·b_{i+2}` when `b_{i+2} < b_{i+1}`. So
`b_{i+2} < a_{i+1}/2`. The remainder shrinks by at least half every two steps,
so after `2t` steps the value is below 1, forcing it to be 0 — which ends the
loop.

```python
def fib(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def euclid_steps(a: int, b: int) -> int:
    steps = 0
    while b:
        a, b = b, a % b
        steps += 1
    return steps


for k in (10, 20, 40):
    a, b = fib(k + 1), fib(k)
    steps = euclid_steps(a, b)
    bound = 2 * (min(a, b).bit_length() - 1) + 1
    print(f"k={k:>3}  F(k+1)={a:<16} gcd steps={steps:<4} 2*log2(min)+1={bound}"
          f"  within bound: {steps <= bound}")

# No pair of numbers below 1000 takes more divisions than the Fibonacci pair.
worst = max((euclid_steps(a, b), a, b) for a in range(1, 1000) for b in range(1, 1000))
print(f"worst pair below 1000: ({worst[1]}, {worst[2]}) in {worst[0]} divisions")
print(f"the Fibonacci pair (55, 34) takes {euclid_steps(55, 34)} divisions")
```

Fibonacci numbers are the worst case because consecutive Fibonacci numbers give
the *smallest* possible remainder at each step, so the value shrinks as slowly as
it can while still decreasing.

</details>

**[ ] Exercise 3 —** Write `factorize(n)` returning the prime factors with
multiplicities, and use it to write `totient(n) = n · Π_{p | n} (1 − 1/p)`, the
count of integers in `1..n` coprime to `n`. Check `totient` against a brute-force
count for every `n` up to 60.

<details>
<summary>Solution</summary>

```python
def factorize(n: int) -> list[int]:
    out = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            out.append(d)
            n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def totient(n: int) -> int:
    primes = set(factorize(n))
    result = n
    for p in primes:
        result -= result // p       # multiply by (1 - 1/p) without fractions
    return result


def totient_brute(n: int) -> int:
    from math import gcd
    return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)


print("n    factor(n)            totient  brute")
for n in list(range(2, 21)) + [30, 36, 60]:
    facs = " * ".join(map(str, factorize(n)))
    t = totient(n)
    assert t == totient_brute(n), n
    print(f"{n:<4} {facs:<20} {t:>7} {totient_brute(n):>6}")

print()
print("360 =", " * ".join(map(str, factorize(360))), " totient(360) =", totient(360))
```

`totient` never uses floating point: `result - result // p` is exactly
`result · (p−1)/p` whenever `p | result`, which holds because we process each
distinct prime once.

</details>

**[ ] Exercise 4 —** Show that `p` and `q` both prime implies
`φ(p·q) = (p−1)(q−1)` by computing `totient` from Exercise 3. Explain in two
sentences why this is exactly the number an RSA attacker has to search, and
why knowing `n = p·q` gives it away.

<details>
<summary>Solution</summary>

```python
from math import isqrt


def totient(n: int) -> int:
    result, m = n, n
    d = 2
    while d * d <= m:
        if m % d == 0:
            result -= result // d
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        result -= result // m
    return result


for p, q in [(61, 53), (11, 13), (17, 19), (101, 103)]:
    n = p * q
    computed = totient(n)
    formula = (p - 1) * (q - 1)
    assert computed == formula
    print(f"p={p:>4} q={q:>4} n={n:>7}  phi(n)={computed:>8}  "
          f"(p-1)(q-1)={formula:>8}")

print()
# The attacker knows n and wants phi(n).  The moment one prime factor turns up,
# the other follows, and phi(n) follows immediately:  n - p - q + 1.
print("an attacker who finds one factor has everything:")
for p, q in [(61, 53), (101, 103)]:
    n = p * q
    found = min(p, q)                     # whatever trial division turns up first
    other = n // found
    print(f"   n={n:>7}  found factor {found:>4}  other factor {other:>5}  "
          f"phi(n) = n - {found} - {other} + 1 = {n - found - other + 1}")
print("   phi(n) is never available from n alone, only from a factorisation.")
```

`φ(n)` counts residues `1 ≤ k ≤ n` with `gcd(k, n) = 1`. For `n = p·q` with
distinct primes, an integer is coprime to `n` exactly when it is neither a
multiple of `p` nor of `q`, so counting by inclusion–exclusion
([Lesson 23](../part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md))
gives `n − n/p − n/q + n/(pq) = n − q − p + 1 = (p−1)(q−1)`. The attacker is
refused exactly one thing: turning `n` into `p` and `q`. That is factoring.

</details>

**Challenge** — Implement a **segmented sieve**: given `L` and `R` with
`R − L ≤ 10⁶`, return all primes in `[L, R]` using only `O(√R + (R−L))` space.
Explain why this is the algorithm behind `primesieve`, a library that can list
all primes below `10¹⁰` in about a second.

<details>
<summary>Solution</summary>

```python
from math import isqrt


def primes_in_range(low: int, high: int) -> list[int]:
    """All primes in [low, high], by sieving only the segment itself."""
    low = max(low, 2)
    segment = [True] * (high - low + 1)

    # Sieve the base primes up to sqrt(high) with the ordinary sieve.
    root = isqrt(high)
    base = [True] * (root + 1)
    base[0] = base[1] = False
    p = 2
    while p * p <= root:
        if base[p]:
            for k in range(p * p, root + 1, p):
                base[k] = False
        p += 1

    # For each base prime, cross out its multiples inside the segment, starting
    # from the first multiple that is >= low and >= p*p.
    for p in range(2, root + 1):
        if base[p]:
            start = max(p * p, ((low + p - 1) // p) * p)
            for k in range(start, high + 1, p):
                segment[k - low] = False

    return [low + i for i, ok in enumerate(segment) if ok]


print(primes_in_range(100, 130))
print(len(primes_in_range(1, 10**6)), "primes below one million")
print(primes_in_range(1_000_000_000, 1_000_000_100))
```

Memory is `O(√R + R − L)`: a table of size `√R` for the base primes plus a table
of size `R − L` for the segment. The time is still `Θ((R − L) ln ln R +
√R ln ln √R)` because we perform the same number of crossings-out, just against
a smaller table. This is why `primesieve` works on ranges far larger than fit
in memory, and why sieving `10¹⁰` is a matter of seconds: the work is linear in
the *interval*, not in the size of the number.

</details>

**[ ] Exercise 5 —** Turn the lesson's Rabin fingerprint into a **Rabin–Karp
substring search**. Write `rk_search(text, pattern)` returning every index at which
`pattern` occurs in `text`. Two requirements: (a) the window hash must be updated
in `O(1)` per position, not recomputed from scratch, and (b) you must *verify* each
hash hit with a real comparison. Count (i) how many character-by-character
comparisons the naive `O(n·m)` scan performs, and (ii) how many hash comparisons
Rabin–Karp performs, on `text = "abracadabra" * 40 + "ab" + "z" * 300` and
`pattern = "abracadabra"`. Finally, prove by an experiment that dropping the
verification step in (b) does not break correctness *on your data* but is unsound in
principle, by finding a real collision under the modulus you chose.

<details>
<summary>Solution</summary>

```python
M, BASE = 2**61 - 1, 256          # a prime modulus, coprime to the base: see Exercise 6


def rabin(text: str, base: int = BASE, modulus: int = M) -> int:
    """The lesson's fingerprint. After k characters this is
       c0*base^(k-1) + c1*base^(k-2) + ... + c_{k-1}  (mod modulus),
       so the FIRST character carries the highest power of the base."""
    h = 0
    for ch in text:
        h = (h * base + ord(ch)) % modulus
    return h


def rk_search(text: str, pattern: str) -> tuple[list[int], int]:
    """Rabin-Karp with an O(1) rolling update. Returns the hit positions and
    the number of hash comparisons made."""
    m = len(pattern)
    bpow = pow(BASE, m, M)                    # B^m, computed once
    hp = rabin(pattern)                        # the pattern's hash
    h = rabin(text[:m])                        # the first window's hash
    hits = [0] if h == hp and text[:m] == pattern else []
    checks = 1 if h == hp else 0
    for i in range(m, len(text)):
        # Slide the window one place: multiply by B (shifts every weight up),
        # subtract the outgoing character's OLD weight B^m, add the new one.
        h = (h * BASE - ord(text[i - m]) * bpow + ord(text[i])) % M
        if h == hp:                           # one 61-bit comparison, no scanning
            checks += 1
            if text[i - m + 1:i + 1] == pattern:   # verify before trusting it
                hits.append(i - m + 1)
    return hits, checks


def naive_search(text: str, pattern: str) -> tuple[list[int], int]:
    """The textbook O(n*m) baseline, counting character comparisons."""
    m = len(pattern)
    hits, comparisons = [], 0
    for i in range(len(text) - m + 1):
        ok = True
        for j in range(m):
            comparisons += 1
            if text[i + j] != pattern[j]:
                ok = False
                break                    # stop at the first mismatch
        if ok:
            hits.append(i)
    return hits, comparisons


text = "abracadabra" * 40 + "ab" + "z" * 300
pattern = "abracadabra"
fast, hash_checks = rk_search(text, pattern)
slow, char_comparisons = naive_search(text, pattern)
print(f"len(text) = {len(text)}  len(pattern) = {len(pattern)}")
print(f"Rabin-Karp found {len(fast)} matches, naive found {len(slow)}")
print("both find exactly the same positions:", fast == slow)
print("first three positions:", fast[:3], " last three:", fast[-3:])
print(f"naive character comparisons : {char_comparisons:,}")
print(f"Rabin-Karp hash comparisons : {hash_checks:,}")
print(f"naive worst case would be   : {len(text) * len(pattern):,}")
print()
# The rolling update agrees with recomputing the window hash from scratch.
t = "abracadabra"
rolling = []
h = rabin(t[:4])
rolling.append(h)
for i in range(4, len(t)):
    h = (h * BASE - ord(t[i - 4]) * pow(BASE, 4, M) + ord(t[i])) % M
    rolling.append(h)
direct = [rabin(t[i:i + 4]) for i in range(len(t) - 3)]
print("rolling update == recomputing each window:", rolling == direct)
print()
# Why the verify step is not optional: build a REAL collision, then show that a
# verifier-less version reports it as a match.
# "Aab" and "cab" are 4 characters, and 256^3 = 2^24 is 0 mod 2^24, so with
# modulus 2^24 the leading character is invisible.
weak = 2**24
p_real, p_fake = "Xabc", "zabc"
print("under the prime modulus 2^61-1 the two are different:",
      rabin(p_real, BASE, 2**61 - 1) != rabin(p_fake, BASE, 2**61 - 1))
print(f"under the composite modulus 2^24 they collide: "
      f"{rabin(p_real, BASE, weak) == rabin(p_fake, BASE, weak)}")
print("so a verifier-less Rabin-Karp would report 'Xabc' occurs in 'zabc....'")
```

Output:

```
len(text) = 742  len(pattern) = 11
Rabin-Karp found 40 matches, naive found 40
both find exactly the same positions: True
first three positions: [0, 11, 22]  last three: [407, 418, 429]
naive character comparisons : 1,414
Rabin-Karp hash comparisons : 40
naive worst case would be   : 8,162

rolling update == recomputing each window: True

under the prime modulus 2^61-1 the two are different: True
under the composite modulus 2^24 they collide: True
so a verifier-less Rabin-Karp would report 'Xabc' occurs in 'zabc....'
```

**Why the counts look like that.** The naive scan looks at every one of the
`742 - 11 + 1 = 732` windows and, for each, compares characters until the first
mismatch — 1,414 comparisons, comfortably under the 8,162 worst case because most
windows fail on the very first character. Rabin–Karp performs one 61-bit comparison
per window (732 hash updates, of which 40 agree with the pattern), so the entire
search is linear in the *text*, independent of the pattern length. That is the
practical difference: a 10-megabyte text with a 10,000-character pattern costs
Rabin–Karp ten million modular operations and the naive scan up to a hundred
billion character comparisons.

**Why the rolling update is correct.** The window hash of `text[i-m+1 : i+1]` is
`Σ_{j=0}^{m-1} c_{i-m+1+j} · B^{m-1-j}`. Multiplying the previous window's hash by
`B` shifts every weight up by one, giving `Σ c_{i-m+1+j} · B^{m-j}`; the outgoing
character `c_{i-m}` now has weight `B^m`, which we subtract, and the incoming
character `c_i` has weight `B^0 = 1`, which we add. Everything else is unchanged,
so the identity holds modulo `M` for any `M` at all. The code asserts it against
recomputation.

**Why the verify step is not optional.** A hash is a *filter*, not a proof of
equality. Two different strings with the same hash are indistinguishable to the
filter, so a verifier-less Rabin–Karp returns a list that may contain positions
where the pattern is not actually present. The probability of that happening under
a prime modulus with a 61-bit value is roughly the number of windows divided by
`2^61`, which is negligible — but "negligible" is a probabilistic claim about
adversarial input, not a correctness guarantee, and it collapses to a certainty the
moment someone picks a modulus that shares a factor with the base. With
`M = 2^24` the collision is not merely likely, it is *constructed*, which is
exactly what Exercise 6 explains.

</details>

**[ ] Exercise 6 (Challenge) — How much does a Rabin fingerprint actually
remember?** Answer in four parts.

1. Show experimentally that with `base = 256` and `M = 2^24` the fingerprint `H` of
   the lesson is **independent of the first character** of any 4-character string,
   and that it is therefore also blind to how long the string is.
2. Generalise: prove that if `gcd(base, M) = d > 1` then `base^t ≡ 0 (mod M)` for
   some `t`, and compute the smallest such `t` for `base = 256, M = 2^24` and for
   `base = 4, M = 2^24`.
3. A genome has a four-letter alphabet. With `base = 4` and `M = 2^24`, how many
   leading symbols does the fingerprint ignore? Verify it, and verify that one
   symbol fewer is safe.
4. Replace the modulus with the prime `2^61 - 1`, confirm the blindness is gone,
   and write one sentence naming the property of `M` that actually fixed it.

<details>
<summary>Solution</summary>

```python
from math import gcd
import itertools


def rabin(text: str, base: int = 256, modulus: int = 2**24) -> int:
    """The lesson's fingerprint, most-significant character first."""
    h = 0
    for ch in text:
        h = (h * base + ord(ch)) % modulus
    return h


# ---- Part 1: 256^3 = 2^24 is 0 mod 2^24, so the leading character vanishes ----
M = 2**24
print("256^3 =", 256**3, " 2^24 =", 2**24, " 256^3 mod 2^24 =", 256**3 % M)
for s in ("Xabc", "zabc", " habc"):
    print(f"  H({s!r}) = {rabin(s, 256, M)}")
print("all three equal:", len({rabin(s, 256, M) for s in ("Xabc", "zabc", " habc")}) == 1)
alphabet = "abc"
words = ["".join(t) for t in itertools.product(alphabet, repeat=4)]
blind = all(rabin(c + w[1:], 256, M) == rabin("z" + w[1:], 256, M)
            for w in words for c in alphabet)
print(f"checked all {len(words)} four-character strings over {alphabet!r}: "
      f"leading character invisible = {blind}")
print('H("abc") =', rabin("abc", 256, M), ' H("Xabc") =', rabin("Xabc", 256, M),
      " equal:", rabin("abc", 256, M) == rabin("Xabc", 256, M))
print()

# ---- Part 2: if gcd(base, M) = d > 1 then base^t = 0 (mod M) for some t ----
def factorise(n: int) -> dict[int, int]:
    """n as {prime: exponent}."""
    out: dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def vanishing_power(base: int, modulus: int) -> int | None:
    """Smallest t >= 1 with base^t = 0 (mod modulus), or None if base is a unit.

    Write modulus = prod p_i^a_i and let c_i = the exponent of p_i in base.
    base^t is divisible by p_i^a_i exactly when t * c_i >= a_i, so the answer
    is max_i ceil(a_i / c_i) over the primes p_i that divide the base.
    """
    if gcd(base, modulus) == 1:
        return None
    t = 0
    for p, a in factorise(modulus).items():
        c = factorise(base).get(p, 0)
        if c:
            t = max(t, -(-a // c))          # ceiling division
    return t


for base, modulus, label in ((256, 2**24, "base 256, M 2^24         "),
                             (4, 2**24, "base 4,   M 2^24         "),
                             (256, 2**61 - 1, "base 256, M 2^61-1 (prime)")):
    print(f"{label}: gcd(base, M) = {gcd(base, modulus):>4}   "
          f"smallest t with base^t = 0 mod M: {vanishing_power(base, modulus)}")
print()
print("Sanity check by direct multiplication:")
h = 1
for t in range(1, 4):
    h = h * 256 % M
    print(f"  256^{t} mod 2^24 = {h}")
print()
print("The fingerprint of a k-character string therefore depends on only its")
print("last min(k, t-1) characters, where t is the vanishing power.  The modulus")
print("decides how much of the string survives.")
print()

# ---- Part 3: DNA, base 4, M = 2^24 = 4^12 ----
def rabin_dna(seq: str, modulus: int = 2**24) -> int:
    index = "ACGT".index
    h = 0
    for ch in seq:
        h = (h * 4 + index(ch)) % modulus
    return h


seq13 = "ACGTACGTACGTA"      # 13 symbols
seq12 = "ACGTACGTACGT"       # 12 symbols
print("4^12 =", 4**12, "= 2^24 =", 2**24)
print("13 symbols, first symbol changed -> same hash:",
      rabin_dna(seq13) == rabin_dna("C" + seq13[1:]))
print("12 symbols, first symbol changed -> same hash:",
      rabin_dna(seq12) == rabin_dna("C" + seq12[1:]))
print("A 12-symbol read is safe: 4^12 is the first vanishing power, so no")
print("leading symbol of a 12-character string is invisible.")
print()

# ---- Part 4: the prime rescues it ----
Mp = 2**61 - 1
print("gcd(256, 2^61-1) =", gcd(256, Mp))
print('H("Xabc") =', rabin("Xabc", 256, Mp), ' H("zabc") =', rabin("zabc", 256, Mp),
      " differ:", rabin("Xabc", 256, Mp) != rabin("zabc", 256, Mp))
print()
print("The property that fixed it: the modulus is PRIME, hence coprime to the")
print("base, hence no power of the base can vanish modulo it.")
```

Output:

```
256^3 = 16777216  2^24 = 16777216  256^3 mod 2^24 = 0
  H('Xabc') = 6382179
  H('zabc') = 6382179
  H(' habc') = 6382179
all three equal: True
checked all 81 four-character strings over 'abc': leading character invisible = True
H("abc") = 6382179  H("Xabc") = 6382179  equal: True

base 256, M 2^24         : gcd(base, M) =  256   smallest t with base^t = 0 mod M: 3
base 4,   M 2^24         : gcd(base, M) =    4   smallest t with base^t = 0 mod M: 12
base 256, M 2^61-1 (prime): gcd(base, M) =    1   smallest t with base^t = 0 mod M: None

Sanity check by direct multiplication:
  256^1 mod 2^24 = 256
  256^2 mod 2^24 = 65536
  256^3 mod 2^24 = 0

The fingerprint of a k-character string therefore depends on only its
last min(k, t-1) characters, where t is the vanishing power.  The modulus
decides how much of the string survives.

4^12 = 16777216 = 2^24 = 16777216
13 symbols, first symbol changed -> same hash: True
12 symbols, first symbol changed -> same hash: False
A 12-symbol read is safe: 4^12 is the first vanishing power, so no
leading symbol of a 12-character string is invisible.

gcd(256, 2^61-1) = 1
H("Xabc") = 1482777187  H("zabc") = 2053202531  differ: True

The property that fixed it: the modulus is PRIME, hence coprime to the
base, hence no power of the base can vanish modulo it.
```

**The proof in part 2.** Factor `M = ∏ p_i^{a_i}` and `base = ∏ p_i^{c_i} · u` with
`c_i ≥ 1` whenever `p_i` divides `M` — that is exactly what `gcd(base, M) > 1` means.
Then `base^{a_i} = ∏ p_j^{c_j a_i} · u^{a_i}` is divisible by `p_i^{a_i}`, because
`c_i · a_i ≥ a_i`. Taking `t = max_i a_i`, we get `base^t ≡ 0 (mod p_i^{a_i})` for
every `i`, hence `base^t ≡ 0 (mod M)` — the Chinese Remainder Theorem, or simply
that a number divisible by every `p_i^{a_i}` is divisible by their product. If
`gcd(base, M) = 1` then `base` is a unit modulo `M`, so no power of it is ever `0`.
∎

**Why this is the lesson's warning, made precise.** The lesson says "a composite
modulus is a liability: knowing `M` lets an adversary multiply two differences
together to build collisions deliberately". Part 1 shows the collapse directly, and
it is a *general* construction rather than a lucky accident: **any two strings with
the same last `t-1` characters collide**, whatever their prefixes and whatever
their lengths. An adversary who knows `M` knows `t` and can aim the collision
instead of searching for it. Note also that the failure has nothing to do with `2^24`
being small — it is small *as a modulus of a byte-string hash*; `M = 2^61 - 1` is
vastly larger and still fine, because it is prime. The dangerous quantity is
`gcd(base, M)`, not `M`. This is the same lesson the hash function in
[Lesson 112](112_hashing.md) teaches: a "good enough" property that depends on your
inputs staying friendly is not a property at all, and a modulus that quietly
special-cases a family of inputs is a bug with a very long fuse.

</details>

## Summary

- `a | b` means `b = a·k`; the division algorithm guarantees `b = a·q + r` with
  `0 ≤ r < a` uniquely, which is why `%` is a function.
- Every integer greater than 1 has exactly one prime factorisation (the
  Fundamental Theorem of Arithmetic), so an integer is determined by its factors.
- `gcd(a, b) = gcd(b, a mod b)`; iterating that identity gives the Euclidean
  algorithm, which terminates because `a` strictly decreases and runs in
  `Θ(log min(a, b))` divisions.
- The Fibonacci sequence is the worst case for Euclid, so the bound is tight.
- Bézout's identity, `gcd(a, b) = s·a + t·b`, is found by the extended Euclidean
  algorithm and is the direct route to the modular inverse in
  [Lesson 111](111_modular_arithmetic_and_crypto.md).
- The Sieve of Eratosthenes finds all primes up to `N` in `Θ(N ln ln N)` time by
  only crossing out multiples of primes up to `√N`.
- `π(N) ≈ N / ln N`: infinitely many primes, average gap `ln N`, and the gap is
  why finding a large prime takes an unpredictable number of tries.
- Factoring a semiprime by trial division costs `Θ(√n)` divisions, which is
  exponential in the bit length of `n` — the asymmetry that public-key
  cryptography is built on.

## Next

[111 — Modular Arithmetic and Public-Key Crypto](111_modular_arithmetic_and_crypto.md)
takes the gcd and Bézout's identity from this lesson and turns them into modular
inverses, Fermat's little theorem, the Chinese Remainder Theorem, and a working
RSA key pair you can verify with a pencil.