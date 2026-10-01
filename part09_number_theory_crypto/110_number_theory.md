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
print("which is exactly why RSA uses 2048- or 3072-bit moduli.")

# Factoring is genuinely hard, not just slow for a silly algorithm:
# a 2048-bit modulus has ~1234 digits.
bits = 2048
digits = bits * 0.30103
print()
print(f"A {bits}-bit modulus has about {digits:.0f} digits, so trial division")
print(f"needs about 10^{digits / 2:.0f} steps.  Better algorithms exist:")
print("Pollard's rho removes small factors in about n^(1/4) steps, and the")
print("general number field sieve (GNFS) is asymptotically the fastest known,")
print("roughly exp( (64/9)^(1/3) * (ln n)^(1/3) * (ln ln n)^(2/3) ) steps.")
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
print(f"modulus 2^61 - 1: H('ab') = {rabin('ab', modulus=2**61 - 1)}   "
      f"H('cb') = {rabin('cb', modulus=2**61 - 1)}   "
      f"{'COLLIDE' if rabin('ab', modulus=2**61 - 1) == rabin('cb', modulus=2**61 - 1) else 'differ'}")
print()
print("With modulus 256 only the final character survives, so anything that")
print("ends the same way collides.  With a big prime, collisions are rare.")
print()

# A composite modulus is a liability: knowing M lets an adversary multiply two
# differences together to build collisions deliberately.
M_COMPOSITE = 256 * 65536                  # 2^24
M_PRIME = 2**61 - 1                        # a Mersenne prime
for M, label in ((M_COMPOSITE, "composite"), (M_PRIME, "prime")):
    h1, h2 = rabin("ab", 256, M), rabin("cb", 256, M)
    print(f"modulus {M} ({label}): H('ab')={h1}  H('cb')={h2}  "
          f"{'COLLIDE' if h1 == h2 else 'differ'}")
print()

# Order information really does survive a large modulus: 'ab' and 'ba' get
# different values because the characters land on different powers of B.
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
    # An attacker knows n.  They need phi(n).  They can get it the moment they
    # find a prime factor: if p | n then phi(n) = n - n/p exactly.
    p_guess = next(d for d in range(2, isqrt(n) + 1) if n % d == 0)
    print(f"p={p:>4} q={q:>4} n={n:>7}  phi(n)={computed:>8}  "
          f"(p-1)(q-1)={formula:>8}  phi = n - n/{p_guess} = {n - n // p_guess}")
```

`φ(n)` counts residues `1 ≤ k ≤ n` with `gcd(k, n) = 1`. For `n = p·q` with
distinct primes, an integer is coprime to `n` exactly when it is neither a
multiple of `p` nor of `q`, giving `n − n/p − n/q + n/(pq) = n − q − p + 1 =
(p−1)(q−1)`. The attacker is refused one thing only: finding `p` from `n`, which
is factoring.

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