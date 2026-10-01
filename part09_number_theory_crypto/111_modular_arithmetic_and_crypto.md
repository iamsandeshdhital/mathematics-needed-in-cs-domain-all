# 111 — Modular Arithmetic and Public-Key Crypto

**Part**: part09_number_theory_crypto · **Prerequisites**: 110 · **Time**: 40 min

---

## In Plain Words

Modular arithmetic is arithmetic where you throw away the multiples of some
number and keep only the remainder. It is the arithmetic of clocks: on a
twelve-hour clock, adding thirteen hours gives the same as adding one, because
twelve hours is zero. Most of the surprising theorems in computer science live
in this arithmetic, and one of them — that raising a number to a large power
and taking the remainder is easy, but undoing it is hard — is the entire basis
of public-key cryptography. In this lesson we build that asymmetry from
scratch: first the small tools (remainders, inverses, Fermat's theorem), then
RSA end to end with numbers small enough to check with a pencil, then why the
textbook version is unsafe and what fixes it, plus a toy version of
Diffie-Hellman key exchange.

## Why Computer Science Cares

- **Every TLS connection you make.** In TLS 1.3 the key exchange is X25519 or
  Kyber, both built on the same easy-forward/hard-backward idea as this lesson.
  In TLS 1.2 it was finite-field or elliptic-curve Diffie-Hellman, the same
  construction in a different arithmetic.
- **`pow(a, b, m)` in Python** is a modular exponentiation implemented in C.
  It is how RSA signing happens, how JWT signature checks happen, and how
  `secrets.randbelow` avoids the modulo bias in random number generation.
- **`hashlib` and checksums** are polynomials over modular fields, so the
  arithmetic in this lesson is the arithmetic of
  [Lesson 112](112_hashing.md) with a different goal.
- **Interview questions.** "Find the modular inverse", "compute 2^100 mod 13",
  "solve x ≡ 2 (mod 3), x ≡ 3 (mod 5)" appear constantly, and almost everyone
  gets the inverse wrong at least once.

## The Formal Version

Notation follows [SYMBOLS.md](../SYMBOLS.md). Used here: `a ≡ b (mod m)`,
`gcd(a, b)`, `φ(n)`, `a⁻¹ mod m`, `O()`.

### Congruences

**Definition.** For integers `a, b` and a positive integer `m`, we write
**`a ≡ b (mod m)`**, read "`a` is congruent to `b` modulo `m`", if
`m | (a − b)`, equivalently `a mod m = b mod m`. `m` is a **modulus**, and
`ℤ_m = {0, 1, …, m−1}` is the set of residue classes modulo `m`. Two integers
are the same element of `ℤ_m` exactly when they are congruent, so congruence is
an equivalence relation partitioning the integers — the setup of
[Lesson 25](../part02_discrete_combinatorics/25_relations_and_equivalence_classes.md).

**Theorem.** `≡ (mod m)` is preserved by addition and multiplication: `a ≡ b`
and `c ≡ d` imply `a + c ≡ b + d` and `a·c ≡ b·d (mod m)`.

*Explanation.* Substituting `a = b + k₁m` and `c = d + k₂m`, the difference
`a + c − (b + d) = (k₁ + k₂)m` and `a·c − b·d = (k₁d + k₂b + k₁k₂)m` are both
multiples of `m`. ∎

**What breaks.** Cancellation and division. `6 ≡ 0 (mod 4)` does *not* imply
`3 ≡ 0 (mod 4)`, because 2 is not invertible mod 4, and `3·2 ≡ 0 (mod 4)` even
though neither factor is `0 (mod 4)`. The difference from ordinary arithmetic
is entirely because `m` can be a zero divisor.

### Units and modular inverses

**Definition.** `a` is a **unit** modulo `m` if some `a⁻¹` satisfies
`a·a⁻¹ ≡ 1 (mod m)`.

**Theorem.** `a` is a unit mod `m` **iff** `gcd(a, m) = 1`.

*Explanation.* If `a·x ≡ 1` then `m | ax − 1`, so `gcd(a, m) | 1`, forcing
`gcd(a, m) = 1`. Conversely Bézout's identity
([Lesson 110](110_number_theory.md)) gives `s·a + t·m = 1` when the gcd is 1,
and reducing mod `m` gives `s·a ≡ 1 (mod m)`. ∎

`ℤ_m` with addition and multiplication, with 0 absorbing, is a **ring**. When
every nonzero element is a unit it is a **field**. Prime modulus gives a field;
composite modulus does not — `gcd(6, 9) = 3`, so 6 is not a unit mod 9, while
`gcd(4, 9) = 1`, so it is. That distinction is the whole reason cryptography
uses primes.

### Fermat's little theorem and Euler's theorem

**Theorem (Fermat's little theorem).** If `p` is prime and `p ∤ a` then
`a^(p−1) ≡ 1 (mod p)`.

*Explanation.* The residues `a, a², …, a^(p−1)` are pairwise distinct mod `p`
(if `a^i ≡ a^j` with `i < j`, then `a^i` is invertible so `a^(i−j) ≡ 1`),
hence a permutation of the nonzero residues. Multiplying them and cancelling
`(p−1)!` from `a^(p(p−1)/2) ≡ (p−1)!` leaves `a^(p−1) ≡ 1`. ∎

**Theorem (Euler's theorem).** If `gcd(a, m) = 1` then `a^φ(m) ≡ 1 (mod m)`.

*Explanation.* The `φ(m)` units mod `m` form a group under multiplication, and
Lagrange's theorem says the order of any element divides the group size, so
`a^φ(m) = (a^ord)^(φ/ord) = 1`. Fermat is the case `m = p`, since
`φ(p) = p − 1`. ∎

Both need coprimality: `pow(5, 4, 5) = 0`, not 1.

### Orders and primitive roots

**Definition.** The **multiplicative order** of `a` mod `m` is the least
positive `k` with `a^k ≡ 1 (mod m)`. `g` is a **primitive root** mod `m` if
`ord_m(g) = φ(m)`, in which case `g, g², …, g^φ(m)` are exactly the units.

**Theorem.** A primitive root exists mod `m` exactly when `m` is `1`, `2`, `4`,
`p^k`, or `2p^k` for odd prime `p`. So every prime `p` has one, and `φ(φ(p))`
of them.

**The discrete logarithm problem.** Given `g`, `p` and `y = g^x mod p`, recover
`x`. For a random unit `x` this is believed as hard as factoring `p`, and it is
the one-way function behind Diffie-Hellman, ElGamal and DSA.

### The Chinese Remainder Theorem

**Theorem (CRT).** Let `m₁, …, m_k` be pairwise coprime and `r₁, …, r_k` given.
Then `x ≡ r_i (mod m_i)` has exactly one solution in `0 ≤ x < M`, where
`M = m₁⋯m_k`.

*Explanation.* For each `i`, Bézout gives `t_i` with `t_i·(M/m_i) ≡ 1 (mod m_i)`
and `0 (mod m_j)` for `j ≠ i`, so `x = Σ r_i t_i (M/m_i)` satisfies every
congruence. Uniqueness: two solutions differ by a multiple of every `m_i`, hence
of `M`, and both lie in `[0, M)`. ∎

RSA's proof below uses this in reverse: prove a relation mod `p` and mod `q`,
then lift it to mod `n`.

### RSA

For distinct primes `p, q` set `n = p·q`, `φ(n) = (p−1)(q−1)`, choose `e` with
`gcd(e, φ(n)) = 1`, and let `d = e⁻¹ mod φ(n)`. **Key generation** is choosing
`p, q, e` and computing `n, d`. The **public key** is `(e, n)`, the **private
key** is `(d, n)`. **Encryption** is `c = m^e mod n`; **decryption** is
`m' = c^d mod n`.

**Theorem (RSA correctness).** For every `0 ≤ m < n`, `(m^e)^d ≡ m (mod n)`.

*Explanation.* `ed − 1` is a multiple of `φ(n) = (p−1)(q−1)`, hence of both
`p−1` and `q−1`. Work `mod p`: if `p | m` both sides are 0; otherwise Fermat
gives `m^(p−1) ≡ 1`, so `m^(ed) = m·(m^(p−1))^((ed−1)/(p−1)) ≡ m (mod p)`.
The same argument holds `mod q`, and CRT gives `m^(ed) ≡ m (mod n)`. ∎

The two cases are why padding matters: the short textbook proof uses Euler's
theorem and needs `gcd(m, n) = 1`, and this case split is what repairs it.

### Why breaking it is hard and exponentiation is fast

**Theorem.** `m^e mod n` needs `O(log e)` modular multiplications.

*Explanation.* Write `e = Σ b_i 2^i` in binary. Then
`m^e = Π (m^(2^i))^{b_i}`, and each `m^(2^i)` follows from the previous by one
squaring. `e` has `⌊log₂ e⌋ + 1` bits, so that is the whole cost. ∎

The exponent's *length*, not its value, is what costs. With a 2048-bit modulus
and `e = 65537`, encryption is about 34 modular multiplications and is
microseconds.

**Converse.** Inverting `c = m^e mod n` without `d` essentially requires a
factor of `n`: given `p` and `q`, `φ(n) = (p−1)(q−1)` follows immediately, then
`d = e⁻¹ mod φ(n)`, then `m = c^d mod n`. Factoring a 2048-bit modulus is
estimated at about `2^112` operations by the best known method (the general
number field sieve), against `2^11` for RSA itself. That ratio is the whole
security margin, and it is the same asymmetry that makes Diffie-Hellman work:
exponentiation is cheap, the discrete logarithm is not.

### Why textbook RSA is insecure

**Attack 1 — determinism.** No randomness anywhere, so `E(m₁) = E(m₂)` whenever
`m₁ = m₂`. Known-plaintext pairs become a lookup table, and low-entropy
plaintexts are guessable.

**Attack 2 — malleability.** Encryption is a homomorphism:
`E(m₁m₂) = E(m₁)E(m₂) mod n`. An attacker who sees two ciphertexts can produce
a *valid* ciphertext for the product, and the receiver cannot distinguish it
from an honest one. Combined with determinism this yields chosen-ciphertext
attacks such as Bleichenbacher's 1998 attack on PKCS#1 v1.5.

**Attack 3 — small messages.** If `m^e < n` there is no reduction at all, so
`m` is the integer `e`-th root of `c`. With `e = 3` and a 2048-bit `n`, every
message shorter than about 682 bits is recovered with a cube root.

**Attack 4 — no integrity.** Nothing binds a ciphertext to a sender or prevents
replay. This is why TLS signs its transcript as well as encrypting it.

**The fix, OAEP.** Optimised Asymmetric Encryption Padding builds

```
em = 0x00 || maskedSeed || maskedDB        db = lHash || PS || 0x01 || M
```

where `maskedSeed` and `maskedDB` are XORed with output from MGF1 (a
counter-mode hash) and `seed` is fresh randomness. It supplies the randomness
textbook RSA lacks, hides the length, guarantees coprimality, and makes every
failure indistinguishable. A 2048-bit RSA key carries at most
`256 − 2·32 − 2 = 190` bytes per OAEP operation, which is why TLS encrypts a
random symmetric key with RSA and everything else with AES.

## Worked Example

Full RSA by hand with `p = 61`, `q = 53`, `e = 17`, `m = 65`.

**Step 1 — the modulus.** `n = 61 · 53 = 3233`.

**Step 2 — the totient.** `φ(n) = 60 · 52 = 3120`.

**Step 3 — is `e` usable?** `gcd(17, 3120)`: `3120 = 183·17 + 9`,
`17 = 1·9 + 8`, `9 = 1·8 + 1`. The last remainder is 1, so the gcd is 1. Good.

**Step 4 — find `d`.** Extend the chain backwards to write 1 as a combination
of 17 and 3120:

- `1 = 9 − 8`
- `8 = 17 − 9`, so `1 = 9 − (17 − 9) = 2·9 − 17`
- `9 = 3120 − 183·17`, so `1 = 2·3120 − 366·17 − 17 = 2·3120 − 367·17`

So `−367·17 ≡ 1 (mod 3120)` and `d = −367 mod 3120 = 3120 − 367 = 2753`.
Check: `17 · 2753 = 46,801`, and `46,801 = 15 · 3120 + 1`. ✓

**Step 5 — encrypt.** `c = 65^17 mod 3233`. Since `17 = 16 + 1`:

- `65² = 4225`, and `4225 − 3233 = 992`, so `65² ≡ 992`
- `65⁴ ≡ 992² = 984,064`. `3233 · 300 = 969,900`, remainder `14,164`;
  `3233 · 4 = 12,932`, remainder `1,232`. So `65⁴ ≡ 1232`
- `65⁸ ≡ 1232² = 1,517,824`. `3233 · 469 = 1,516,277`, remainder `1,547`.
  So `65⁸ ≡ 1547`
- `65¹⁶ ≡ 1547² = 2,393,209`. `3233 · 740 = 2,392,420`, remainder `789`.
  So `65¹⁶ ≡ 789`
- `65¹⁷ = 65¹⁶ · 65 ≡ 789 · 65 = 51,285`. `3233 · 15 = 48,495`, remainder
  `2,790`. So **`c = 2790`**

**Step 6 — decrypt.** `m' = 2790^2753 mod 3233`, which the code below does in 12
squarings. The answer is `65`.

**Step 7 — why it works.** `ed − 1 = 46,800`, and `46,800 / 60 = 780`,
`46,800 / 52 = 900`, `46,800 / 3120 = 15`. So `m^(ed) = m · (m^(p−1))^780`,
and `m^60 ≡ 1 (mod 61)` by Fermat; likewise `mod 53`. CRT then gives
`m^(ed) ≡ m (mod 3233)`. Every value here is small enough to check with a
pencil, which is the whole reason for choosing these two primes.

## Runnable Code

### 1. Inverses and modular exponentiation

```python
def extended_gcd(a, b):
    old_r, r, old_s, s, old_t, t = a, b, 1, 0, 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t


def mod_inverse(a, m):
    """The inverse of a mod m, or None if there is none.

    Why gcd is the whole test: a has an inverse mod m exactly when some x
    satisfies a*x = 1 (mod m), i.e. a*x - y*m = 1 for some integer y.  If such
    an x exists then gcd(a, m) divides 1, so gcd(a, m) = 1.  The converse is
    Bezout's identity from the extended Euclidean algorithm.
    """
    g, s, _ = extended_gcd(a, m)
    return None if g != 1 else s % m


def mod_pow(base, exp, m):
    """Repeated squaring: O(log exp) modular multiplications.

    The idea: writing exp in binary, base^exp is the product of base^(2^i) over
    the set bits i.  Each squaring doubles the exponent for free.
    """
    result, b = 1, base % m
    while exp:
        if exp & 1:
            result = result * b % m
        b = b * b % m
        exp >>= 1
    return result


def mod_pow_trace(base, exp, m):
    """The same computation, logging every intermediate value."""
    result, b, step = 1, base % m, 0
    lines = [f"start: result = 1, base = {b}, exp = {exp} = {exp:b} in binary"]
    while exp:
        if exp & 1:
            result = result * b % m
            lines.append(f"   bit {step} = 1: result = {result}")
        else:
            lines.append(f"   bit {step} = 0: result = {result} (unchanged)")
        b = b * b % m
        exp >>= 1
        step += 1
    return result, lines


for a, m in [(3, 11), (10, 17), (7, 13), (6, 9), (4, 8)]:
    inv = mod_inverse(a, m)
    if inv is None:
        g = extended_gcd(a, m)[0]
        print(f"{a} mod {m}: no inverse, because gcd({a}, {m}) = {g} != 1")
    else:
        print(f"{a} mod {m}: inverse is {inv:>3}   check {a}*{inv} = {a * inv}"
              f", and {a * inv} mod {m} = {(a * inv) % m}")
print()
print("'Division' that fails in modular arithmetic: 4 has no inverse mod 6,")
print(f"because 4 and 6 share the factor 2.  Mod 13 it does: "
      f"mod_inverse(4, 13) = {mod_inverse(4, 13)}, and 4 * "
      f"{mod_inverse(4, 13)} = 40 = 3*13 + 1.")
print("Over a prime modulus nothing obstructs an inverse, because nothing but")
print("1 divides a prime.  Over a composite modulus some residues are units")
print("and some are not, which is the difference between a ring and a field.")
print()

print("compute 7^13 mod 11 by repeated squaring")
print("   13 = 1101 in binary, so 7^13 = 7^1 * 7^4 * 7^8")
val, trace = mod_pow_trace(7, 13, 11)
for line in trace:
    print("  ", line)
print("  result =", val, " and 7^13 =", 7**13, "so 7^13 mod 11 =", 7**13 % 11)
print()

import math
import time

print("the exponent's length is all that matters, not its value:")
t0 = time.perf_counter()
for _ in range(2000):
    mod_pow(7, 2**1000, 11)
elapsed = (time.perf_counter() - t0) / 2000
print(f"   7^(2^1000) mod 11 by squaring: {elapsed * 1e6:.1f} us"
      f"   (1001 squarings, about 600 multiplies)")
print(f"   the naive method needs 2^1000 multiplies and the number it builds")
print(f"   has about {2**1000 * math.log10(7):.3e} digits, so it cannot be stored")
print()

print("Python's builtin pow(a, b, m) is exactly this algorithm, in C:")
print("   pow(7, 13, 11)       =", pow(7, 13, 11), " vs 7**13 % 11 =", 7**13 % 11)
print("   pow(7, 2**1000, 11)  =", pow(7, 2**1000, 11))
print("   pow(a, -1, m)        =", pow(4, -1, 13), " (mod_inverse agrees)")
print("   pow(a, -1, 6) raises ValueError, because no inverse exists")
```

### 2. Fermat, Euler, orders, and primitive roots

```python
from math import gcd


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


def order(a: int, m: int) -> int:
    """The smallest k >= 1 with a^k = 1 (mod m)."""
    assert gcd(a, m) == 1
    val, k = 1, 0
    while True:
        val = val * a % m
        k += 1
        if val == 1:
            return k


print("Fermat's little theorem: prime p, p not dividing a, then a^(p-1) = 1 mod p")
for p, a in [(11, 7), (13, 3), (17, 5), (23, 6)]:
    print(f"   p={p:>3} a={a}   a^(p-1) mod p = {pow(a, p - 1, p)}")
print(f"   but p=5, a=5 gives 5^4 mod 5 = {pow(5, 4, 5)}, not 1, so the")
print("   coprimality hypothesis is not optional.")
print()

print("Euler's theorem: any m, gcd(a, m) = 1, then a^phi(m) = 1 mod m")
for m, a in [(11, 7), (12, 5), (15, 4), (10, 3), (8, 3)]:
    print(f"   m={m:>3} a={a}   phi(m)={totient(m):>3}   a^phi(m) mod m = "
          f"{pow(a, totient(m), m)}")
print(f"   and gcd(4, 10) = 2, so Euler says nothing: 4^4 mod 10 = "
      f"{pow(4, 4, 10)}")
print()

print("units mod m, and the order of each one")
for m in (7, 9, 11):
    units = [k for k in range(1, m) if gcd(k, m) == 1]
    orders = {u: order(u, m) for u in units}
    roots = [u for u in units if orders[u] == totient(m)]
    print(f"   m={m:>3}  phi(m)={totient(m):>3}  units={units}")
    print(f"          orders={orders}")
    print(f"          primitive roots (order = phi(m)): {roots}")
print()
print("Every order divides phi(m), which is Lagrange's theorem, and that is")
print("why a^phi(m) = 1 holds for every unit.  A primitive root's powers run")
print("through every unit exactly once -- here 2 mod 11, which has order 10:")
print("  ", [pow(2, k, 11) for k in range(10)])
print()
print("The reverse direction is the hard one.  Given g, p and y = g^x mod p,")
print("recovering x is the discrete logarithm problem, and it is what")
print("Diffie-Hellman, ElGamal and DSA are built on.  Brute force just tries")
print("every exponent, which is fine at these sizes and hopeless at 2048 bits:")
for m, g in ((11, 2), (13, 2)):
    target = pow(g, 5, m)
    found = next(x for x in range(m - 1) if pow(g, x, m) == target)
    print(f"   mod {m}: g = {g}, target {g}^5 mod {m} = {target}, "
          f"brute force finds x = {found}")
```

### 3. The Chinese Remainder Theorem

```python
def extended_gcd(a, b):
    old_r, r, old_s, s, old_t, t = a, b, 1, 0, 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t


def crt_brute(residues, moduli):
    """The definition, used to check the fast version: search all of 0..M-1."""
    M = 1
    for m in moduli:
        M *= m
    for x in range(M):
        if all(x % m == r % m for r, m in zip(residues, moduli)):
            return x, M
    return None, M


def crt(residues, moduli):
    """Combine congruences x = ri (mod mi) with pairwise coprime moduli."""
    M = 1
    for m in moduli:
        M *= m
    x = 0
    for r, m in zip(residues, moduli):
        Mi = M // m
        # Bezout gives t with t*Mi + u*m = 1, so t*Mi = 1 mod m and 0 mod
        # every other modulus.  Summing r_i * t_i * M_i satisfies all of them.
        _, t, _ = extended_gcd(Mi, m)
        x += r * (t * Mi)
    return x % M, M


for residues, moduli in [([2, 3, 2], [3, 5, 7]), ([1, 0, 5], [2, 3, 5]),
                         ([4], [9]), ([123, 456, 789], [1000, 1001, 1003])]:
    fast, M = crt(residues, moduli)
    note = ""
    if M <= 100_000:                              # only brute force small ones
        assert fast == crt_brute(residues, moduli)[0]
        note = "  (confirmed by exhaustive search)"
    print("solve  " + "  and  ".join(f"x = {r} (mod {m})"
                                     for r, m in zip(residues, moduli)))
    print(f"   x = {fast}, unique in 0..{M - 1}{note}")
    for r, m in zip(residues, moduli):
        print(f"      {fast} mod {m} = {fast % m}, wanted {r % m}")
    print()

import random

random.seed(3)
for _ in range(300):
    moduli = [random.choice([2, 3, 5, 7, 11]) for _ in range(2)]
    if moduli[0] != moduli[1]:
        residues = [random.randrange(m) for m in moduli]
        assert crt(residues, moduli)[0] == crt_brute(residues, moduli)[0]
print("300 random congruence systems also agree with the brute-force search")
print()
print("Inconsistent system: x = 1 (mod 4) and x = 2 (mod 6).  The first says x")
print("is odd and the second says it is even, so no solution exists.  Two")
print("congruences are compatible exactly when they agree modulo gcd(m1, m2).")
print("search over one period finds:",
      [k for k in range(24) if k % 4 == 1 and k % 6 == 2])
print()
x = 2000000
print(f"Storing {x} mod 15 = {x % 15} as the pair ({x % 3}, {x % 5}) is cheaper,")
print(f"and CRT rebuilds it: {crt([x % 3, x % 5], [3, 5])[0]}")
```

### 4. RSA from scratch, with every intermediate value

```python
"""Textbook RSA from scratch.  Every primitive is written out; nothing is
imported.  The primes are deliberately tiny so you can check every number by
hand on paper."""


def extended_gcd(a, b):
    old_r, r, old_s, s, old_t, t = a, b, 1, 0, 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t


def mod_inverse(a, m):
    g, s, _ = extended_gcd(a, m)
    assert g == 1, "no inverse: a and m are not coprime"
    return s % m


def mod_pow(base, exp, m):
    """Repeated squaring: O(log exp) modular multiplications."""
    result, b = 1, base % m
    while exp:
        if exp & 1:
            result = result * b % m
        b = b * b % m
        exp >>= 1
    return result


# ---------------------------------------------------------------- keygen
p, q = 61, 53
n, phi = p * q, (p - 1) * (q - 1)
e = 17
d = mod_inverse(e, phi)

print("=== RSA key generation ===")
print(f"two distinct primes   p = {p}, q = {q}")
print(f"modulus               n = p*q = {n}")
print(f"totient               phi(n) = (p-1)(q-1) = {phi}")
print(f"public exponent       e = {e}   (gcd(e, phi(n)) = {extended_gcd(e, phi)[0]})")
print(f"private exponent      d = e^-1 mod phi(n) = {d}")
print(f"   check: e*d = {e * d} = {phi}*{e * d // phi} + {(e * d) % phi}"
      f", so e*d = 1 (mod phi(n))")
print(f"PUBLIC KEY  (e, n) = ({e}, {n})    PRIVATE KEY (d, n) = ({d}, {n})")
print()

# ------------------------------------------------------------ encrypt
message = 65                                  # the ASCII code of 'A'
print("=== encryption with the public key ===")
print(f"m = {message},  e = {e} = {e:b} in binary, so m^e = m * m^16")
b, result = message, 1
for i in range(e.bit_length() - 1, -1, -1):
    print(f"   bit {i} of e is {(e >> i) & 1}   running base = {b}")
    if (e >> i) & 1:
        result = result * b % n
    b = b * b % n
ciphertext = mod_pow(message, e, n)
print(f"ciphertext c = m^e mod n = {ciphertext}")
print()

# ------------------------------------------------------------ decrypt
recovered = mod_pow(ciphertext, d, n)
print("=== decryption with the private key ===")
print(f"d = {d}, which has {d.bit_length()} bits, so {2 * d.bit_length()}"
      f" modular multiplications at most")
print(f"c^d mod n = {recovered}   original m = {message}   match = "
      f"{recovered == message}")
print()

# -------------------------------------------------------- why it works
print("=== why decryption inverts encryption ===")
print(f"ed - 1 = {e * d - 1},  p-1 = {p - 1},  q-1 = {q - 1}")
print(f"(ed-1)/(p-1) = {(e * d - 1) // (p - 1)},  (ed-1)/(q-1) = "
      f"{(e * d - 1) // (q - 1)},  (ed-1)/phi(n) = {(e * d - 1) // phi}")
print("Work mod p: if p | m then m^(ed) = m = 0.  Otherwise Fermat gives")
print(f"m^(p-1) = 1 (mod p) and m^(ed) = m * (m^(p-1))^({(e * d - 1) // (p - 1)}) = m (mod p).")
print("The same holds mod q, and CRT lifts it to mod n.  Both cases, so the")
print("theorem holds for every message, including m = p and m = q:")
for m in (0, 1, 65, p, q, 2 * p, n - 1):
    c = mod_pow(m, e, n)
    print(f"   m={m:>5}  c = {c:>5}  c^d mod n = {mod_pow(c, d, n):>5}  "
          f"correct: {mod_pow(c, d, n) == m}")
print()

# --------------------------------------------- three attacks, no factoring
print("=== breaking textbook RSA without factoring ===")
print("1. Deterministic: the same plaintext always gives the same ciphertext,")
print("   so known-plaintext pairs become a lookup table.")
seen = {mod_pow(w, e, n): w for w in (65, 66, 67, 90, 256, 1024)}
print(f"   ciphertext -> guessed plaintext: {seen}")
print()
print("2. Malleable: encryption is a homomorphism, E(m1*m2) = E(m1)E(m2) mod n.")
m1, m2 = 65, 66
c1, c2 = mod_pow(m1, e, n), mod_pow(m2, e, n)
forged = (c1 * c2) % n
print(f"   c1 = {c1}, c2 = {c2}, product = {forged}")
print(f"   decrypting the forgery gives {mod_pow(forged, d, n)}, which is "
      f"{m1}*{m2} = {m1 * m2} reduced mod {n}.")
print("   The attacker encrypted nothing, and the receiver cannot tell.")
print()
print("3. Small messages leak: if m^e < n then no reduction happened and m is")
print("   just the integer e-th root of c.")
e_small, m_small = 3, 5
c_small = pow(m_small, e_small, n)
print(f"   e = 3, m = {m_small}: c = {m_small}^3 = {c_small} < n = {n}, so")
print(f"   round(c ** (1/3)) = {round(c_small ** (1 / 3))} with no factoring at all.")
print(f"   With a 2048-bit n and e = 3 this recovers the first "
      f"{2048 // 3} bits of the message.")
print("   Hence real RSA uses e = 65537 and pads, so m is always about the")
print("   size of n.")
```

### 5. Padding, primality testing, and what real RSA adds

```python
"""Textbook RSA is never used on its own.  Real RSA is textbook RSA plus
padding, and the padding supplies the randomness textbook RSA lacks, hides the
message length, guarantees coprimality with n, and gives the decryptor a
structure to check so a tampered ciphertext is rejected rather than silently
becoming a different message.

This is PKCS#1 v1.5, the padding a 1994-era implementation would use.  It is
deterministic once the random padding is fixed, which is the weakness
Bleichenbacher exploited in 1998; OAEP fixed it, and the lessons are the same.
The two primes are the primes just above 2^62 (found with the Miller-Rabin code
below), so n is 16 bytes and a 5-byte message fits.
"""
import time

BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def is_prime(n: int) -> bool:
    """Deterministic Miller-Rabin for n < 3.3 * 10^24: no false positives.

    Trial division would need 2^31 operations per candidate at this size, so
    real key generation cannot use it.  Miller-Rabin needs 12 modular
    exponentiations, which is why every crypto library ships it.
    """
    if n < 2:
        return False
    for small in BASES:
        if n % small == 0:
            return n == small
    d, s = n - 1, 0                 # write n - 1 = 2^s * d with d odd
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in BASES:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue                # this base found no witness
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False             # a is a witness: n is composite
    return True


def next_prime(k: int) -> int:
    k = k + 1 if k % 2 == 0 else k + 2
    while not is_prime(k):
        k += 2
    return k


def extended_gcd(a, b):
    old_r, r, old_s, s, old_t, t = a, b, 1, 0, 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t


def mod_pow(base, exp, m):
    result, b = 1, base % m
    while exp:
        if exp & 1:
            result = result * b % m
        b = b * b % m
        exp >>= 1
    return result


t0 = time.perf_counter()
p, q = next_prime(2**62), 0
q = next_prime(p + 2)
n, phi = p * q, (p - 1) * (q - 1)
e = 65537
d = extended_gcd(e, phi)[1] % phi
k = (n.bit_length() + 7) // 8
print(f"found p = {p} and q = {q} in {time.perf_counter() - t0:.4f} s with")
print(f"Miller-Rabin; trial division would have needed up to 2^31 steps each.")
print(f"n = {n}  ({n.bit_length()} bits, {k} bytes)   e = {e}   d = {d}")
print()


def pad(message: bytes, filler: bytes) -> bytes:
    """0x00 0x02, at least 8 bytes of non-zero filler, 0x00, then the message.
    The PS >= 8 rule exists because of early-1990s attacks on short messages."""
    if len(message) > k - 11:
        raise ValueError("message too long for this modulus")
    return b"\x00\x02" + filler[:k - len(message) - 3] + b"\x00" + message


def unpad(em: bytes) -> bytes:
    if em[0] != 0x00:
        raise ValueError("first byte is not 0x00")
    if em[1] != 0x02:
        raise ValueError("second byte is not 0x02")
    sep = em.find(b"\x00", 2)
    if sep == -1:
        raise ValueError("no 0x00 separator")
    if sep - 2 < 8:
        raise ValueError("padding string shorter than 8 bytes")
    return em[sep + 1:]


def encrypt(message: bytes, filler: bytes) -> int:
    return mod_pow(int.from_bytes(pad(message, filler), "big"), e, n)


def decrypt(c: int) -> bytes:
    return unpad(mod_pow(c, d, n).to_bytes(k, "big"))


print("1. The same message gives a different ciphertext every time")
for filler in (bytes(range(1, k)), bytes(range(k, 2 * k)), bytes([255] * k)):
    c = encrypt(b"HELLO", filler)
    print(f"   filler {filler.hex()} -> c = {c}")
print()
print("2. The padded block always starts 00 02, so it is below 2^120 while p")
print("   and q are both above 2^61.  Neither can divide it, so gcd(block, n)")
print("   = 1 always, and the short textbook proof applies with no case split.")
print()
print("3. A tampered ciphertext is rejected.")
c = encrypt(b"HELLO", bytes(range(1, k)))
print(f"   the genuine ciphertext {c} unpads to {decrypt(c)!r}")
for delta in (1, 2, 10**12):
    try:
        print(f"   c+{delta:<13} -> {decrypt((c + delta) % n)!r}")
    except ValueError as err:
        print(f"   c+{delta:<13} -> rejected: {err}")
print("   Textbook RSA returns a plain number for each, with nothing to check:")
for delta in (1, 2, 10**12):
    print(f"   (c+{delta})^d mod n = {mod_pow((c + delta) % n, d, n)}")
print()
print("4. Even v1.5 is breakable, because those rejections are distinguishable.")
print("   An attacker who can tell 'bad first byte' from 'missing separator'")
print("   shrinks the set of acceptable ciphertexts until only the real one is")
print("   left.  Bleichenbacher did that against every SSL server of 1998 at")
print("   about one request per second.  OAEP's fix is one indistinguishable")
print("   error for every kind of failure.")
print()
print("5. RSA has no integrity even with perfect padding: an attacker can replay")
print("   an old ciphertext or swap Bob's for Alice's.  TLS therefore signs the")
print("   transcript too.  RSA encrypts; it does not authenticate.")
```

### 6. Diffie-Hellman

```python
"""Diffie-Hellman key exchange: two parties who share nothing agree on a
secret, and an eavesdropper who sees every message learns nothing (as long as
the discrete logarithm problem stays hard)."""


def mod_pow(base, exp, m):
    result, b = 1, base % m
    while exp:
        if exp & 1:
            result = result * b % m
        b = b * b % m
        exp >>= 1
    return result


def order(a, m):
    val, k = 1, 0
    while True:
        val = val * a % m
        k += 1
        if val == 1:
            return k


# A toy, completely insecure instance: p = 23, g = 5.
p, g = 23, 5
print(f"public parameters: p = {p}, g = {g}")
print(f"   the order of g mod p is {order(g, p)} and p - 1 = {p - 1}, so g is a")
print("   primitive root: its powers hit every nonzero residue exactly once.")
print(f"   powers of {g} mod {p}: {[pow(g, k, p) for k in range(p - 1)]}")
print()

a, b = 6, 15                             # Alice's and Bob's secret exponents
A, B = mod_pow(g, a, p), mod_pow(g, b, p)  # what they send
shared_a = mod_pow(B, a, p)               # Alice computes B^a
shared_b = mod_pow(A, b, p)               # Bob computes A^b

print(f"Alice keeps a = {a} and sends A = g^a mod p = {A}")
print(f"Bob   keeps b = {b} and sends B = g^b mod p = {B}")
print(f"   Alice computes B^a mod p = {B}^{a} mod {p} = {shared_a}")
print(f"   Bob   computes A^b mod p = {A}^{b} mod {p} = {shared_b}")
print(f"   they agree: {shared_a == shared_b}")
print(f"   the shared value is g^(ab) mod p = {g}^{a * b} mod {p} = {shared_a},")
print(f"   and {a * b} = a*b = b*a, which is why both routes give the same number.")
print()

print("An eavesdropper sees A =", A, "and B =", B, "and nothing else.")
print("Getting the shared secret from those means solving g^x = A (mod p), the")
print("discrete logarithm problem.  With p = 23 that is a lookup table:")
table = {pow(g, x, p): x for x in range(p - 1)}
print(f"   {table}")
print(f"   A = {A} is at position {table[A]}, which is Alice's secret.")
print()
print("Why toy parameters are hopeless, one line each:")
print("   * a small p can be brute forced, exactly as above;")
print("   * a smooth p - 1 lets Pohlig-Hellman split the problem into small")
print("     pieces, each of which is solvable by brute force;")
print("   * a generator of small order leaks through small subgroups.")
print("Real Diffie-Hellman therefore uses a 2048-bit safe prime p = 2q + 1 with")
print("q also prime, and a generator checked for full order.  The cost is that")
print("exponentiation stays cheap while the discrete logarithm stays expensive,")
print("which is the same asymmetry that makes RSA work.")
```

## Common Mistakes

**Wrong.** Using `a ** b % m` for modular exponentiation.

```python
a, b, m = 7, 13, 1000003
naive, fast = a ** b % m, pow(a, b, m)
print(f"a**b % m = {naive}, pow(a, b, m) = {fast}, equal: {naive == fast}")
print(f"but a**b built the whole of 7^13 = {a ** b} before taking the modulo")
```

**Right.**

```python
a, b, m = 7, 13, 1000003
print("c = pow(a, b, m) =", pow(a, b, m), " -- never builds a**b at all")
print("for a 2048-bit exponent, a**b has about 2^11 bits before the modulo,")
print("which costs milliseconds per multiply instead of microseconds")
```

Why the wrong version is tempting: `**` and `%` both exist and the expression
reads like textbook notation. It also passes every test you write on small
numbers. The failure is a performance and memory cliff, not a wrong answer,
which is exactly the kind of bug that survives review.

---

**Wrong.** Assuming a modular inverse always exists.

```python
from math import gcd

# crashes deep inside a library, with a message about modular inverse
# rather than about your data
def inverse(a, m):
    return pow(a, -1, m)


print(inverse(4, 13))                  # 10
try:
    print(inverse(2, 6))               # raises ValueError
except ValueError as err:
    print("crash far from the cause:", err)
```

**Right.**

```python
from math import gcd


def inverse(a, m):
    g = gcd(a, m)
    if g != 1:
        raise ValueError(f"no inverse mod {m}: gcd({a}, {m}) = {g}")
    return pow(a, -1, m)


print(inverse(4, 13))
try:
    print(inverse(2, 6))
except ValueError as err:
    print("rejected at the boundary:", err)
```

Why the wrong version is tempting: `pow(a, -1, m)` does raise, so the check
*feels* present. But in C or Java you frequently get `0` back with no error at
all, and even in Python the message tells you nothing about which of your two
inputs was wrong.

---

**Wrong.** Applying Fermat's little theorem to a composite modulus.

```python
def fermat_wrong(a, m):
    return pow(a, m - 1, m) == 1        # correct only when m is prime


print("fermat_wrong(3, 1001)  =", fermat_wrong(3, 1001),
      " but phi(1001) = 720, not 1000")
print("3^1000 mod 1001 =", pow(3, 1000, 1001),
      " and 3^720 mod 1001 =", pow(3, 720, 1001))
print("fermat_wrong(4, 10)   =", fermat_wrong(4, 10),
      " but gcd(4, 10) = 2, so Euler does not apply either")
```

**Right.**

```python
from math import gcd


def phi(m):
    return sum(1 for k in range(1, m + 1) if gcd(k, m) == 1)


def euler(a, m):
    if gcd(a, m) != 1:
        return None                      # the hypothesis fails
    return pow(a, phi(m), m) == 1


print("euler(3, 1001) =", euler(3, 1001), " because phi(1001) =", phi(1001))
print("euler(4, 10)   =", euler(4, 10), " because gcd(4, 10) = 2")
```

Why the wrong version is tempting: the formula is right, the code is short, and
it passes on every small prime you test. The failure appears only at
`m = 2^61 − 1` versus `m = 2^60`.

---

**Wrong.** Verifying a signature without a range check.

```python
def verify_naive(signature, e, n, digest):
    return pow(signature, e, n) == int.from_bytes(digest, "big")


n, e = 3233, 17
digest = (65).to_bytes(2, "big")
signature = pow(65, 17, n)
print("genuine signature verifies:", verify_naive(signature, e, n, digest))
print("signature + n also verifies:", verify_naive(signature + n, e, n, digest))
print("   because (m^e + n)^e = m^e (mod n), so signatures are not unique")
```

**Right.**

```python
def verify(signature, e, n, digest, nbits=2048):
    if not 0 <= signature < n:            # reject out-of-range values
        return False
    recovered = pow(signature, e, n)
    # compare in constant time, and never say *why* it failed
    return recovered == int.from_bytes(digest, "big") and n.bit_length() <= nbits


print("genuine signature verifies:",
      verify(pow(65, 17, 3233), 17, 3233, (65).to_bytes(2, "big"), nbits=12))
print("out-of-range signature rejected:",
      verify(pow(65, 17, 3233) + 3233, 17, 3233, (65).to_bytes(2, "big"),
             nbits=12))
```

Why the wrong version is tempting: textbook RSA signatures really are
`s^e mod n = m`, so the check looks right. Without the range test, `s + n` is a
second valid signature for the same message, which breaks any scheme that
treats signatures as unique.

## Formula Sheet

Every formula, notation and definition this lesson uses. Symbols follow
[SYMBOLS.md](../SYMBOLS.md). "Restriction" columns are not optional: dropping
the coprimality condition is the single most common way to get one of these wrong.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `$a \equiv b \pmod m$` | `$m \mid (a - b)$`, equivalently `a mod m == b mod m` | `a` and `b` leave the same remainder on division by `m` | comparing answers without the numbers; the basis of a hash's "same answer" check |
| `$\mathbb{Z}_m$ | `$\{0, 1, \dots, m-1\}$` | the `m` residue classes modulo `m` — the "numbers" of modular arithmetic | counting units; the domain `E` and `D` act on |
| cancellation failure | `3·2 ≡ 0 (mod 4)` although `3 ≢ 0` and `2 ≢ 0`; `6 ≡ 0 (mod 4)` does not give `3 ≡ 0` | multiplying by something with no inverse collapses two different values into one | why you cannot divide out of a congruence; why composite moduli are dangerous |
| unit / inverse | `a` is a unit mod `m` iff `$gcd(a, m) = 1$`; then `a·a⁻¹ ≡ 1 (mod m)` | the multiplicative inverse exists exactly when the two numbers share no factor | `pow(a, -1, m)`, which raises `ValueError` when `gcd(a, m) > 1` |
| `$a^{-1} \bmod m$` from Bézout | `s` with `s·a + t·m = 1`, then `a⁻¹ ≡ s (mod m)` | the coefficient of `a` in Bézout's identity *is* the inverse | extended Euclid; the same loop as [Lesson 110](110_number_theory.md), one extra output. `4⁻¹ mod 13 = 10`, since `4·10 = 40 = 3·13 + 1` |
| ring vs field | prime modulus ⟹ field (every nonzero element invertible); composite ⟹ ring with zero divisors | a field lets you cancel | the structural reason cryptography uses primes |
| `$\varphi(m)$ | `$m \prod_{p \mid m}\left(1 - \frac{1}{p}\right)$` over distinct primes `p` dividing `m` | how many residues are coprime to `m` — the size of the unit group | RSA key generation. `φ(3233) = φ(61·53) = 60·52 = 3120` |
| **Fermat's little theorem** | `$a^{p-1} \equiv 1 \pmod p$` | raise to one less than the prime and you get back to 1 | Miller–Rabin; the RSA proof worked out mod `p`. **Restriction: `p` must be prime *and* `p ∤ a`** |
| **Euler's theorem** | `$a^{\varphi(m)} \equiv 1 \pmod m$` | the same statement with the prime modulus generalised | composite moduli. **Restriction: `gcd(a, m) = 1`** — not "any `a`". Fermat is the case `m = p`, since `φ(p) = p − 1` |
| why the restriction matters | `pow(5, 4, 5) = 0`, not 1, because 5 divides 5; and `4^4 mod 10 = 6`, not 1, because `gcd(4, 10) = 2` | both theorems return something other than 1 when the base shares a factor with the modulus | the lesson's counterexamples; any RSA code must guarantee `gcd(message, n) = 1` or pad |
| `$\mathrm{ord}_m(a)$ | least `k >= 1` with `$a^k \equiv 1 \pmod m$` | how long a full cycle takes; defined only for units | `ord_11(2) = 10`, `ord_7(2) = 3` |
| Lagrange | `$\mathrm{ord}_m(a) \mid \varphi(m)$ | the cycle length always divides the number of units | this is the one-line proof of Euler's theorem |
| primitive root `g` | `$\mathrm{ord}_m(g) = \varphi(m)$`; exists iff `m` is `1, 2, 4, p^k` or `2p^k` | `g, g², …` run through every unit exactly once, and there are `φ(φ(p))` of them mod a prime `p` | Diffie–Hellman needs one. `ord_11(2) = 10 = φ(11)`, and the powers `1, 2, 4, 8, 5, 10, 9, 7, 3, 6` hit every nonzero residue |
| discrete logarithm | given `g`, prime `p`, `y = g^x mod p`, recover `x` | unscramble an exponentiation; believed as hard as factoring `p` when `x` is a random unit | the one-way function behind Diffie–Hellman, ElGamal and DSA |
| **CRT** | `x ≡ r_i (mod m_i)` with `m_i` pairwise coprime, `M = m₁⋯m_k` | there is exactly one `x` in `[0, M)`, and `M` is the period | rebuilding `x` from `x mod 3` and `x mod 5`: `2000000 mod 15 = 5` is stored as `(2, 0)` |
| CRT construction | `$x = \sum_i r_i t_i \frac{M}{m_i} \pmod M$` with `$t_i \frac{M}{m_i} \equiv 1 \pmod {m_i}$ | each summand is 1 in the `i`-th slot and 0 in all the others | `x ≡ 2,3,2 (mod 3,5,7)` gives `x = 23`; `x ≡ 123,456,789 (mod 1000,1001,1003)` gives `446,113,123` |
| CRT solvability | solvable iff `$r_i \equiv r_j \pmod{\gcd(m_i, m_j)}$` for all `i, j` | the residues must agree wherever the moduli overlap | `x ≡ 1 (mod 4)` forces `x ≡ 1 (mod 2)` and `x ≡ 2 (mod 6)` forces `x ≡ 0 (mod 2)`, so no solution exists |
| **RSA modulus** | `$n = p \cdot q$`, `p ≠ q` primes | two secret primes multiplied into one public number | key generation. `61 · 53 = 3233` |
| **RSA totient** | `$\varphi(n) = (p-1)(q-1)$` | the number of residues coprime to `n` | `60 · 52 = 3120` |
| **RSA public exponent** | `$e$ with `$gcd(e, \varphi(n)) = 1$` | any exponent that is invertible mod `φ(n)` | real systems fix `e = 65537`; for `φ(3233) = 3120`, `e = 3`, `5` and `13` are all **rejected** because each divides 3120 |
| **RSA private exponent** | `$d = e^{-1} \bmod \varphi(n)$`, i.e. `$ed \equiv 1 \pmod{\varphi(n)}$` | the exponent that undoes `e` **modulo `φ(n)`, not modulo `n`** | `d = 2753`, since `17 · 2753 = 46,801 = 15 · 3120 + 1`. Reducing mod `n` instead gives the useless `e⁻¹ mod 3233 = 2092` |
| **encryption** | `$c = m^e \bmod n$ | raise to the **public** exponent | sending. `65^{17} mod 3233 = 2790` |
| **decryption** | `$m' = c^d \bmod n$ | raise to the **private** exponent | receiving. `2790^{2753} mod 3233 = 65`. Applying `e` instead gives `m^{e^2} = 1452`, not 65 |
| RSA correctness | `$ed - 1 = k(p-1) = k'(q-1)`; then `$m^{ed} = m\,(m^{p-1})^k \equiv m \pmod p$`, the same mod `q`, and CRT lifts it to mod `n` | do the work in each factor separately, then combine | the proof, and *why* the private exponent is `d`. The case where `p` divides `m` is what repairs the short Euler proof |
| repeated squaring | `$e = \sum_i b_i 2^i$ ⟹ `$m^e = \prod_i (m^{2^i})^{b_i}$` | squaring doubles the exponent for free, so you only touch the bits of `e` | `⌊log₂ e⌋ + 1` squarings. `65^{17} = 65^{16}·65` needs 4 squarings and 1 multiply |
| `$m^e \bmod n$` cost | `$O(\log e)$` modular multiplications | the exponent's **length** is the cost, not its value | `e = 65537` has 17 bits, so about 34 multiplications of 2048-bit numbers; `d` has about 2048 bits, so about 4096. `pow(m, e, n)` is this in C |
| security margin | a 2048-bit modulus: RSA costs about `$2^{11}$`, factoring (the general number field sieve) about `$2^{112}$` | the attack is astronomically more expensive than the defence | the reason 2048 bits is the baseline, and the ratio *is* the security budget |
| Miller–Rabin | write `$n-1 = 2^s d$ with `d` odd, then test each base `a` | a probabilistic-looking test that is exact for `n < 3.3·10^{24}` with the bases `2 … 37` | finding the two primes above `2^62`, `4611686018427388039` and `4611686018427388073`, in about 1.4 ms. Trial division would need up to `$2^{31}$` steps per candidate |
| PKCS#1 v1.5 padding | `em = 0x00 ‖ 0x02 ‖ PS ‖ 0x00 ‖ M`, `PS` at least 8 non-zero bytes | pad the message to a fixed size with random filler | on the lesson's 16-byte modulus the block starts `00 02` so it is below `2^120` while `p, q > 2^61`, which guarantees `gcd(block, n) = 1` |
| OAEP | `em = 0x00 ‖ maskedSeed ‖ maskedDB`, `db = lHash ‖ PS ‖ 0x01 ‖ M`, masks from MGF1 | mask a fixed-structure block with fresh randomness and unpad by reversing it | adds randomness, hides length, forces `gcd(em, n) = 1`, and breaks the homomorphism |
| OAEP capacity | `$k - 2hLen - 2 = 256 - 2·32 - 2 = 190$` bytes | the most a 2048-bit RSA key can encrypt once | why TLS encrypts a random AES key with RSA and everything else with AES |
| Diffie–Hellman | `A = g^a mod p`, `B = g^b mod p`, shared `$= g^{ab} mod p = B^a mod p = A^b mod p$` | both sides raise the other's public value to their own secret, and land on the same number | the lesson's toy: `p = 23`, `g = 5` (order 22), `a = 6`, `b = 15` give `A = 8`, `B = 19`, shared `= 2`; the eavesdropper's table lookup returns `6` and hands over the secret |
| small-message leak | if `$m^e < n$ there is no reduction at all, so `$m = \mathrm{round}(c^{1/e})$` | the ciphertext is the exact power, so take the root | with `e = 3` and a 2048-bit `n`, every message under `n^{1/3}`, i.e. about 682 bits, falls to a cube root |
| `secrets.randbelow` | rejection sampling: redraw until in range, so no modulo bias | only possible because you can test `a mod m` cheaply | why `random.randrange` is fine for simulation and `secrets` is required for keys |

## Multiple Choice Questions

**Q1.** A key-generation routine validates a candidate exponent with
`pow(a, p - 1, p) == 1` for prime `p`. What happens at `p = 5`, `a = 5`, and what
is the correct reading?

- A) It returns 1, the check passes, and the exponent is valid
- B) It returns 0, and Fermat's little theorem does not apply because `p` divides `a`
- C) It returns 0, which means Fermat's little theorem is false for `p = 5`
- D) It returns 1, because `a^(p−1) ≡ 1 (mod p)` holds for every `a`

<details>
<summary>Answer and explanation</summary>

**B) It returns 0, and Fermat's little theorem does not apply because `p` divides
`a`.**

`5^4 = 625 = 125·5`, so `pow(5, 4, 5)` is `0`. Fermat's little theorem has **two**
hypotheses: `p` is prime *and* `p ∤ a`. Here `p = 5` is prime, so the first holds,
but `a = 5` is a multiple of `p`, so the second fails and the theorem says nothing
whatsoever. The lesson flags this on the first line of the pair of theorems:
"Both need coprimality: `pow(5, 4, 5) = 0`, not 1." The operational consequence
follows: RSA also needs `gcd(message, n) = 1`, or padding so that it holds.

Option A is the mistake the second case split in the RSA proof is designed to
prevent. Checking that the modulus is prime is necessary but not sufficient, and
the check fails silently on precisely the input you are least likely to try.

Option C is the wrong diagnosis of a correct number. A counterexample to a theorem
whose hypotheses are unmet tells you nothing about the theorem: `p = 7`, `a = 2`
gives `2^6 mod 7 = 1`, so the theorem is perfectly fine.

Option D is a real mathematical error — a genuinely universal claim. The
generalisation that *is* true needs coprimality: for `gcd(a, m) = 1` you get
`a^{φ(m)} ≡ 1 (mod m)`, which is Euler's theorem. At `m = 5` the two coincide,
since `φ(5) = 4`.

</details>

**Q2.** What is `4^φ(10) mod 10`, and why?

- A) 1, because `φ(10) = 4` and Euler's theorem applies to any base
- B) 6, and Euler's theorem does not apply because `gcd(4, 10) = 2 ≠ 1`
- C) 6, and Euler's theorem simply fails for composite moduli
- D) 0, because a base that shares a factor with the modulus eventually gives 0

<details>
<summary>Answer and explanation</summary>

**B) 6, and Euler's theorem does not apply because `gcd(4, 10) = 2 ≠ 1`.**

`φ(10) = 4` (only 1, 3, 7, 9 are coprime to 10) and `4^4 = 256 = 25·10 + 6`, so
the value is 6. The obstruction is visible without any theorem: every power of 4 is
even, so no power of 4 is ever `≡ 1 (mod 10)`, since 1 is odd. Fermat and Euler are
statements about *units*, and 4 is not a unit mod 10.

Option A is the tempting version. `φ(10) = 4` is correct, and "Euler's theorem says
`a^φ(m) ≡ 1`" is a correct quotation of a theorem. The error is the missing
hypothesis: what has been quoted is a *conditional*, and the condition fails.

Option C draws the wrong lesson. Composite moduli are fine — the lesson's own
examples run Euler's theorem over them without trouble, with `φ(12) = 4`,
`φ(15) = 8` and `φ(8) = 4`. What fails is non-coprime *bases*, and that is exactly
the "why the restriction matters" row in the formula sheet.

Option D is a plausible-sounding pattern that is simply false here. `4^4 = 256` is
not a multiple of 10; it is 6 more than one. Powers of a non-unit do converge
towards losing information mod the shared factor, but they do not become 0 mod `m`
unless the base is a zero divisor, and even then only mod the shared part.

</details>

**Q3.** Alice publishes `(e, n) = (17, 3233)` and sends Bob the ciphertext
`c = 2790`, which is `65^17 mod 3233`. What single computation gives Bob the
plaintext?

- A) `2790^17 mod 3233`
- B) `2790^2753 mod 3233`
- C) `2790^2092 mod 3233`
- D) `2790^-1 mod 3233`

<details>
<summary>Answer and explanation</summary>

**B) `2790^2753 mod 3233`.**

`d = e⁻¹ mod φ(n) = 2753` is the *private* exponent, and decryption is
`m' = c^d mod n`, which returns 65. The confusion this question targets is the
single most common one in the subject: the public exponent encrypts, the private
exponent decrypts, and they are different numbers. If Bob could decrypt with
`e = 17`, the key would not be secret.

Option A is the exponent swap, and it is worth being precise about why it fails
rather than merely asserting it. `c^e = (m^e)^e = m^{e^2} = m^{289}`, and there is
no reason for that to equal `m`: it would require `e^2 ≡ 1 (mod λ(n))`, and
`289 mod 780 = 289 ≠ 1`. The value is **1452**. It is tempting to think the swap
"accidentally works" because `(m^e)^d ≡ m` does hold — but that is the entire point,
namely that only `d` is an inverse.

Option C uses `d' = e⁻¹ mod n = 2092`, obtained by reducing the inverse modulo the
wrong number. `17 · 2092 = 35,564 = 11 · 3233 + 1`, so it genuinely is an inverse
of 17; it is just not the inverse that matters. `35,564 mod 3120 = 1,244 ≠ 1`, and
decrypting with it gives 2699.

Option D inverts the ciphertext multiplicatively. An inverse of 2790 mod 3233
exists, but inverting `c` is not inverting `m^e`. The lesson's last `Common
Mistakes` entry is exactly this point: modular *division* (`pow(a, -1, m)`, which
is extended Euclid and easy) is not the same operation as recovering `m` from
`m^e mod n`, which is a discrete logarithm.

</details>

**Q4.** The toy key has `n = 3233`, `φ(n) = 3120`, `e = 17`. Suppose the key
generator computed `d = e⁻¹ mod n` instead of `d = e⁻¹ mod φ(n)`. What is `d`, and
does decryption still work?

- A) `d = 2753`; nothing changes, because the inverse of `e` does not depend on
  which modulus you reduce by
- B) `d = 2092`; decryption fails, because RSA needs `e·d ≡ 1 (mod φ(n))`, and
  `17 · 2092 mod 3120 = 1,244`, not 1
- C) `d = 2092`; decryption works, because `17 · 2092 = 11 · 3233 + 1`, so
  `e·d ≡ 1 (mod n)`
- D) `d = 3120`; decryption fails, because `d` must be smaller than `φ(n)`

<details>
<summary>Answer and explanation</summary>

**B) `d = 2092`; decryption fails, because RSA needs `e·d ≡ 1 (mod φ(n))`, and
`17 · 2092 mod 3120 = 1,244`, not 1.**

Running extended Euclid on 17 and 3233 gives `1 = 6·3233 − 1141·17`, so
`17⁻¹ mod 3233 = 3233 − 1141 = 2092`. But `35,564 mod 3120 = 1,244`, so the
identity the proof needs is false, and `2790^2092 mod 3233 = 2699` instead of 65.
The working value is `d = 2753`, where `17 · 2753 = 46,801 = 15 · 3120 + 1`.

Option A is the "it must be the same number" intuition. The inverse of `e` is a
whole family of integers, one per modulus you reduce by, and only one family
member is useful. What matters is not *which* integer you land on but which
congruence it satisfies.

Option C contains a true statement — `17 · 2092 = 35,564 = 11 · 3233 + 1` is
correct arithmetic — and draws the wrong conclusion from it. The modulus must be
`φ(n)`, because the proof rewrites `m^{ed} = m·(m^{p−1})^k` and needs
`(p−1) | (ed−1)`. The integer `n` never appears in the exponent arithmetic at
all. This is the single most common implementation bug in hand-rolled RSA.

Option D confuses a bound with a condition. `17 · 3120 mod 3233 = 1,312`, so 3120
is not an inverse of 17 in any sense, and the genuine requirement on `d` is a
congruence, not a range. Relatedly, the lesson's `mod_inverse` returns `s % m`,
which reduces into `[0, m)` for tidiness rather than for correctness.

</details>

**Q5.** An attacker sees `c₁ = E(m₁)` and `c₂ = E(m₂)` and sends Bob
`(c₁·c₂) mod n`, a perfectly valid-looking ciphertext. With the lesson's values
`m₁ = 65`, `m₂ = 2000`, `c₁ = 2790`, `c₂ = 2698`, the forgery is 996, and Bob
decrypts it to 680. Which property of textbook RSA is being exploited?

- A) Determinism: `E` is a function, so the same plaintext always yields the same
  ciphertext
- B) The homomorphism `E(m₁m₂) = E(m₁)E(m₂) mod n`, that is, malleability
- C) Small messages, because `m₁` and `m₂` are short and therefore guessable
- D) The absence of a signature scheme, so Bob cannot authenticate the sender

<details>
<summary>Answer and explanation</summary>

**B) The homomorphism `E(m₁m₂) = E(m₁)E(m₂) mod n`, that is, malleability.**

`(m^e mod n)·(k^e mod n) = (mk)^e mod n`, because reduction mod `n` is a ring
homomorphism. The lesson states this as Attack 2. Check the numbers:
`65 · 2000 = 130,000`, and `130,000 mod 3233 = 680` — exactly what Bob decrypted
from the forged ciphertext 996. The attacker multiplied two values the protocol
never combined and produced a message neither sender transmitted. Exercise 4 builds
precisely this forgery and confirms it by decryption.

Option A is the other real weakness, and it does interact with this one, but it is
a different mechanism. Determinism says the same plaintext always gives the same
ciphertext, so an attacker with known-plaintext pairs gets a lookup table. Here the
attacker's new ciphertext corresponds to a message nobody sent, so nothing is being
looked up.

Option C is incoherent as a description of this attack: the attacker never needs to
know or guess `m₁` or `m₂` at all, which is what makes the attack cheap. Small
messages are Attack 3 and need `m^e < n`; `65^3 = 274,625` is far bigger than 3233,
so that attack does not apply to these values.

Option D is true in general — Attack 4 is the absence of integrity, and that is why
TLS signs its transcript — but it is not this mechanism. A signature would *detect*
the forgery; the homomorphism is what lets it be *constructed*. And a correctly
signed message would still be malleable if the scheme were encryption-only.

</details>

**Q6.** Textbook RSA with a 2048-bit modulus is not deployed; OAEP is. Which
addition is load-bearing, and why does the *error behaviour* matter as much as the
randomness?

- A) A longer modulus, so the message is harder to guess
- B) A fresh random seed plus MGF1 masking, together with one indistinguishable
  error for every failure mode, so an attacker cannot narrow the set of acceptable
  ciphertexts
- C) A signature over the ciphertext, so the recipient can authenticate the sender
- D) A much larger public exponent, so encryption is too slow to attack cheaply

<details>
<summary>Answer and explanation</summary>

**B) A fresh random seed plus MGF1 masking, together with one indistinguishable
error for every failure mode, so an attacker cannot narrow the set of acceptable
ciphertexts.**

This is the lesson's Attack 1 plus its OAEP box, and the second half is the
interesting half. Randomness alone would fix determinism: the lesson's PKCS#1 v1.5
demo encrypts the same 5-byte message under three different fillers and gets three
different ciphertexts. But Bleichenbacher's 1998 attack did not break v1.5's
randomness — it broke its *error handling*. Because v1.5 decryptors distinguish
"first byte wrong" from "missing separator", a chosen-ciphertext attacker learns
which ciphertexts are plausible, shrinks the candidate set, and converges on the
real plaintext at about one request per second against every SSL server of the day.
The fix is to report one indistinguishable error for everything, which is what the
lesson's Challenge solution does with a single
`raise ValueError("decryption error") from None`.

Option A confuses computational hardness with message-space size. The modulus is
already 2048 bits; making it longer protects against none of the four attacks and
costs performance for nothing. Note the opposite trap: padding already *shrinks*
the usable message to 190 bytes, and that is the right trade.

Option C describes OAEP's neighbour, not OAEP. OAEP is encryption padding and
provides confidentiality; it authenticates nothing. Integrity and sender
authentication are separate jobs done in TLS by signing the transcript, which is
the lesson's Attack 4 and the point 5 of its padding section: "RSA encrypts; it
does not authenticate."

Option D is backwards. Security never comes from making the honest party slow —
that is denial of service, not cryptography. Real RSA deliberately uses a *small*
public exponent, `65537`, so that encryption is about 34 modular multiplications
and microseconds. A large `e` would be a performance bug, not a security feature.

</details>

**Q7.** Solve `x ≡ 2 (mod 3)`, `x ≡ 3 (mod 5)`, `x ≡ 2 (mod 7)`. What is `x` in
`[0, 105)`?

- A) 8
- B) 23
- C) 53
- D) 68

<details>
<summary>Answer and explanation</summary>

**B) 23.**

`23 mod 3 = 2` ✓, `23 mod 5 = 3` ✓, `23 mod 7 = 2` ✓. The lesson's CRT section
solves this exact system and prints `x = 23, unique in 0..104 (confirmed by
exhaustive search)`.

Option A satisfies the first *two* congruences only: `8 mod 3 = 2` and
`8 mod 5 = 3`, but `8 mod 7 = 1`. This is the commonest CRT error — solving the
easy subset and stopping. Note also that `M = 3·5·7 = 105`, so the period is 105,
not 15, which means 8 is simply in the wrong equivalence class.

Option C passes the first two and fails the third: `53 mod 3 = 2`, `53 mod 5 = 3`,
`53 mod 7 = 4`. It is `8 + 45`, correct modulo 15 but not modulo 7 — the same
mistake as A with a different offset.

Option D also passes the first two: `68 mod 3 = 2`, `68 mod 5 = 3`, `68 mod 7 = 5`,
and it is `8 + 60`, again a multiple of 15. All three wrong options solve the
two-congruence subsystem, which is precisely the diagnosis: the third congruence
was never used.

</details>

**Q8.** Why does cryptography insist on a prime modulus, given that composite
moduli support ordinary arithmetic perfectly well?

- A) A prime modulus provides more residues, so hash values spread out better
- B) A prime modulus makes every nonzero residue a unit, so there are no zero
  divisors and cancellation works; a composite modulus has `3·2 ≡ 0 (mod 4)` with
  neither factor zero
- C) Prime moduli are faster to compute with, because `pow(a, b, m)` special-cases
  them
- D) A prime modulus guarantees that every message is smaller than the modulus

<details>
<summary>Answer and explanation</summary>

**B) A prime modulus makes every nonzero residue a unit, so there are no zero
divisors and cancellation works; a composite modulus has `3·2 ≡ 0 (mod 4)` with
neither factor zero.**

Nothing but 1 divides a prime, so `gcd(a, p) = 1` for every `1 <= a < p` and `ℤ_p`
is a field: every nonzero element is invertible, and you may cancel. Over a
composite modulus some residues are units and some are not — the lesson's example
is `gcd(6, 9) = 3`, so 6 has no inverse mod 9, while `gcd(4, 9) = 1`, so it does.
And multiplication destroys information: `3·2 ≡ 3·6 ≡ 0 (mod 12)`, so you cannot
cancel the 3 to conclude `2 ≡ 6`.

This is the mechanism behind every `gcd(...) = 1` guard in the lesson. Fermat needs
`p ∤ a`, Euler needs `gcd(a, m) = 1`, `d` needs `gcd(e, φ(n)) = 1`, and
Diffie–Hellman needs a primitive root of a prime modulus. They are the same
requirement in different clothes.

Option A is a hashing argument, and hashing is [Lesson 112](112_hashing.md). It is
not why cryptography uses primes, and it is not even true as stated: a prime
modulus `p` gives exactly `p` residues, whatever `p` happens to be.

Option C is a performance claim with no basis. `pow(a, b, m)` is repeated squaring
regardless of `m`, and the lesson implements it with a single loop containing no
branch on the modulus. The 16-byte-modulus demo runs the same `mod_pow`.

Option D is a non sequitur and false. The lesson's padded block is 16 bytes and `n`
is 16 bytes, and what keeps the block a unit is the `0x00 0x02` prefix putting it
below `2^120` while `p` and `q` are above `2^61` — an explicit, deliberate
construction. Nothing about primality enforces it.

</details>

**Q9.** Real key generation needs 1024-bit primes. Trial division is unusable at
that size; Miller–Rabin is not. What is the actual reason?

- A) Trial division costs `Θ(n)` rather than `Θ(√n)`, and Miller–Rabin is a proof of
  primality for all `n`
- B) Trial division needs up to `√n ≈ 2^512` divisions per candidate, while
  Miller–Rabin needs `O(log n)` modular multiplications per base, and the small base
  set makes it deterministic below `3.3 · 10^24`
- C) Miller–Rabin is exact, whereas trial division returns only a probable prime
- D) Trial division cannot test odd numbers, so it fails on every large prime

<details>
<summary>Answer and explanation</summary>

**B) Trial division needs up to `√n ≈ 2^512` divisions per candidate, while
Miller–Rabin needs `O(log n)` modular multiplications per base, and the small base
set makes it deterministic below `3.3 · 10^24`.**

A 1024-bit number is about `2^1024`, so trial division must grind up to
`√n = 2^512` — 154 decimal digits — *per candidate*, and you need about
`ln(2^1024) ≈ 710` candidates on average. The lesson makes the same point at
62 bits, where trial division "would have needed up to 2^31 steps each", and finds
`p = 4611686018427388039` and `q = 4611686018427388073` in about 1.4 milliseconds.
Miller–Rabin instead writes `n − 1 = 2^s d` with `d` odd and does a few dozen
multiplications per base.

Option A gets both facts backwards. Trial division *is* `Θ(√n)` — the lesson's
`factor` stops at `isqrt(n)` precisely because factors come in pairs — and
Miller–Rabin is not a proof for all `n`. It is a randomised test that becomes
deterministic only because a small, verified set of bases suffices below a bound.

Option C is the reverse of the truth, and it is a common source of genuine
confusion. Below `3.3 · 10^24` Miller–Rabin *is* exact, so "exact" is the property
trial division has and Miller–Rabin borrows. Above that bound Miller–Rabin has a
small but nonzero false-positive rate, and libraries switch to more bases or extra
rounds rather than pretending the guarantee is absolute.

Option D is false. The odd-only `is_prime` in [Lesson 110](110_number_theory.md)
skips even divisors entirely and tests `3, 5, 7, …` up to `isqrt(n)`; it handles
odd numbers perfectly well. Large primes are the *easy* case for trial division's
structure — the problem is only that `2^512` is a lot of candidates' worth of work.

</details>

**Q10.** The lesson contrasts `2^11` with `2^112` for a 2048-bit modulus. What are
those two numbers, and what does their ratio buy?

- A) `2^11` operations for RSA itself; `2^112` operations to factor `n` by the best
  known general method — the ratio is the entire security margin
- B) `2^112` for RSA and `2^11` for factoring, because factoring is the cheap direction
- C) 17 for RSA, because `e = 65537` has 17 bits, and 2048 for factoring
- D) Both are `2^11`, because the best known attack on RSA is as fast as RSA itself

<details>
<summary>Answer and explanation</summary>

**A) `2^11` operations for RSA itself; `2^112` operations to factor `n` by the best
known general method — the ratio is the entire security margin.**

RSA's own work is tiny: `e = 65537` has 17 bits, so encryption is about
`2 · 17 = 34` modular multiplications of 2048-bit numbers, microseconds in
practice. The `2^112` figure is the general number field sieve estimate for
factoring a 2048-bit modulus. The lesson's own framing is the right one: the
point is not the absolute numbers but that one side is polynomial in the bit
length and the other is not, so the gap widens as keys get longer. The same
asymmetry is what makes Diffie–Hellman work — exponentiation is cheap, the
discrete logarithm is not.

Option B is the direction that would destroy the scheme, and it is the natural
misreading: "the attacker has to undo one modular exponentiation, so it should
cost about the same." But undoing it needs `φ(n)`, and `φ(n)` needs the factors.
The lesson is explicit that inverting `c = m^e mod n` without `d` "essentially
requires a factor of `n`".

Option C picks up two real numbers from the lesson and misassigns them. 17 is the
bit length of `e`, so it measures *encryption* cost, not the whole scheme; and
2048 is the bit length of `d`, which likewise describes decryption, not an attack.
RSA costs far less than `2^11` for a single encryption; the `2^11` figure is for a
full key operation.

Option D is the failure mode the whole lesson exists to rule out. If the best
attack were as cheap as the defence, no public-key cryptography would exist, and
there would be no `secrets` module, no TLS handshake, and no [Lesson 112](112_hashing.md).

</details>

**Q11.** In the lesson's toy Diffie–Hellman, `p = 23`, `g = 5`, Alice keeps `a = 6`
and Bob keeps `b = 15`, so `A = 8` and `B = 19`. An eavesdropper sees `A` and `B`.
What must they break, and what do they get?

- A) They must factor 23, which is easy, giving `p` and hence the shared secret
- B) They must solve `5^x ≡ 8 (mod 23)`, the discrete logarithm problem; at this
  size that is a table lookup, returning `x = 6`, and hence `19^6 mod 23 = 2`
- C) They must compute `8⁻¹ mod 23`, the multiplicative inverse
- D) They must apply Fermat's little theorem to `p = 23`, which reveals the secret

<details>
<summary>Answer and explanation</summary>

**B) They must solve `5^x ≡ 8 (mod 23)`, the discrete logarithm problem; at this
size that is a table lookup, returning `x = 6`, and hence `19^6 mod 23 = 2`.**

The lesson builds exactly this table and reports that `A = 8` sits at position 6,
"which is Alice's secret". The shared value is `g^{ab} = 5^{90} mod 23 = 2`, computed
by Alice as `B^a = 19^6 mod 23` and by Bob as `A^b = 8^{15} mod 23`, and the lesson
confirms both agree. Diffie–Hellman's security rests entirely on that being
intractable, which is why the lesson closes on small `p`, smooth `p − 1`, and
small-order generators, and on real parameters being a 2048-bit safe prime
`p = 2q + 1` with a checked generator.

Option A confuses the parameters with the security assumption. 23 is prime and
factoring it is trivial, but the secret was never hidden in the factors of `p`; it
is hidden in the *exponent*, and no factorisation of `p` helps find it. This is the
sharp contrast with RSA, where the whole secret *is* the factorisation.

Option C inverts a value rather than unscrambling an exponent. `8⁻¹ ≡ 3` mod 23
since `8 · 3 = 24 ≡ 1`, but that is neither `19^6` nor a step towards the shared
secret. This is the "fast forward direction, no fast inverse" mistake in the
lesson's final `Common Mistakes` entry.

Option D applies a correct theorem to the wrong question. Fermat gives
`a^22 ≡ 1 (mod 23)` for every unit, and the lesson's own order-computing code does
rely on it, but it tells you the size of the group, not the discrete log of 8. It
says nothing about which power of 5 produced 8.

</details>

## Subjective Questions

### Short Answer

**Q1. State the criterion under which `a` has a modular inverse modulo `m`, and say
what Python's `pow(a, -1, m)` does when the criterion fails.**

<details>
<summary>Model answer</summary>

`a` has an inverse modulo `m` **iff** `gcd(a, m) = 1`; equivalently, `a` is a unit
of `ℤ_m`.

One direction: if `a·x ≡ 1 (mod m)` then `m | ax − 1`, so `gcd(a, m)` divides
`ax − 1` and hence divides 1, forcing `gcd(a, m) = 1`. The other: Bézout's identity
from [Lesson 110](110_number_theory.md) gives `s·a + t·m = 1` when the gcd is 1, and
reducing mod `m` gives `s·a ≡ 1`, so `s` is the inverse.

Python's `pow(a, -1, m)` raises `ValueError` when no inverse exists. That is
correct behaviour, but it raises deep inside a library with a message about
modular inverse rather than about your data, and in C or Java you often get `0`
back with no error at all. Guard with an explicit `gcd` check.

</details>

**Q2. State Fermat's little theorem and Euler's theorem, and state exactly what each
one requires.**

<details>
<summary>Model answer</summary>

**Fermat's little theorem.** If `p` is prime and `p ∤ a`, then
`a^(p−1) ≡ 1 (mod p)`. Requires *two* things: `p` prime, and the base coprime to
`p`.

**Euler's theorem.** If `gcd(a, m) = 1`, then `a^φ(m) ≡ 1 (mod m)`. Requires only
coprimality, and works for any modulus.

Fermat is the special case `m = p`, since `φ(p) = p − 1`.

The requirements are not decoration. `pow(5, 4, 5) = 0`, not 1, because `5 | 5`.
And `4^4 mod 10 = 6`, not 1, because `gcd(4, 10) = 2`. This is why any RSA
implementation must guarantee `gcd(message, n) = 1`, either by checking it or by
padding so that it holds automatically.

</details>

**Q3. What is the multiplicative order of `a` modulo `m`, and what does Lagrange's
theorem tell you about it?**

<details>
<summary>Model answer</summary>

`ord_m(a)` is the least positive integer `k` with `a^k ≡ 1 (mod m)` — the length of
the cycle `a, a², a³, …` before returning to 1. It is defined only for units.

Lagrange's theorem says the order of any element of a finite group divides the order
of the group. The units modulo `m` form a group of size `φ(m)`, so
`ord_m(a) | φ(m)`.

That single fact *is* Euler's theorem in one line: write `φ(m) = k · ord_m(a)`, and
`a^φ(m) = (a^ord)^k ≡ 1`. Examples: `ord_11(2) = 10 = φ(11)`, so 2 is a primitive
root mod 11; `ord_7(2) = 3`; and 1 always has order 1.

</details>

**Q4. Write out RSA key generation, including every restriction, and say which of
the values is public.**

<details>
<summary>Model answer</summary>

1. Choose two distinct primes `p` and `q`. **Restriction:** `p ≠ q`.
2. `n = p·q`. For the toy key, `61 · 53 = 3233`.
3. `φ(n) = (p−1)(q−1)`, here `60 · 52 = 3120`.
4. Choose `e` with `gcd(e, φ(n)) = 1`. **Restriction:** this is what makes `e`
   invertible. Real systems fix `e = 65537`; for `φ(3233) = 3120`, `e = 3`, `5` and
   `13` are all **rejected**, because each of them divides 3120.
5. `d = e⁻¹ mod φ(n)`, so `ed ≡ 1 (mod φ(n))`. Here `d = 2753`.

The **public key** is `(e, n)` — publish it. The **private key** is `(d, n)` — never
publish it. Because `n` is public, nothing in the public key reveals `p`, `q` or
`φ(n)`.

</details>

**Q5. State the Chinese Remainder Theorem, and state the condition under which a
system of congruences has no solution.**

<details>
<summary>Model answer</summary>

**CRT.** Let `m₁, …, m_k` be pairwise coprime and `r₁, …, r_k` given. Then
`x ≡ r_i (mod m_i)` has exactly one solution in `0 <= x < M`, where `M = m₁⋯m_k`.
The solution is `x = Σ r_i t_i (M/m_i) mod M`, where `t_i` is chosen so that
`t_i·(M/m_i) ≡ 1 (mod m_i)`.

**Solvability.** The theorem needs pairwise-coprime moduli. In general two
congruences are compatible exactly when they agree modulo `gcd(m₁, m₂)`, and a
whole system is solvable iff `r_i ≡ r_j (mod gcd(m_i, m_j))` for all pairs.

The lesson's example: `x ≡ 1 (mod 4)` forces `x ≡ 1 (mod 2)`, while `x ≡ 2 (mod 6)`
forces `x ≡ 0 (mod 2)`. `gcd(4, 6) = 2`, the residues disagree mod 2, and an
exhaustive search over one period finds nothing.

</details>

**Q6. Why is `e = 65537` used in real RSA rather than `e = 3`, and what does the
OAEP size limit force on the design of a protocol like TLS?**

<details>
<summary>Model answer</summary>

`e = 65537 = 2^16 + 1` is prime, coprime to `φ(n)`, and — crucially — *small in
bits*. It has 17 bits, so `m^e mod n` costs about `2 · 17 = 34` modular
multiplications instead of thousands. A large public exponent would make every
encryption slow and buys no security, because the private exponent is where the
real work is.

`e = 3` is small in a different and dangerous sense. If `m^3 < n` there is no
modular reduction at all, so `m` is just the integer cube root of `c`: every
message under `n^{1/3}`, about 682 bits, falls to a cube root. This is Attack 3.

The OAEP limit then shapes the protocol. A 2048-bit RSA key carries at most
`k − 2hLen − 2 = 256 − 64 − 2 = 190` bytes per operation, and you cannot amortise
that over a long session. So TLS does not encrypt a conversation with RSA. It
generates one random AES key, encrypts *that* with RSA once, and encrypts the
actual traffic with AES. Hybrid encryption is not an optimisation; it is what the
size limit forces.

</details>

### Long Answer

**Q1. Why does an attacker who knows the public key `(e, n)` break textbook RSA
instantly, and what does padding actually change?**

<details>
<summary>Model answer</summary>

**The reason.** Textbook RSA gives an attacker a *deterministic public function*
`E: ℤ_n → ℤ_n`, `E(m) = m^e mod n`, and that function is exactly what the private
key inverts. The public function is therefore not the bottleneck — the *inverse* is.
The public key tells the attacker the modulus `n` and the exponent `e`; it does not
tell them `φ(n)`, and `φ(n)` is what they need:

- factor `n = p·q` — the hard step, estimated at about `2^112` for a 2048-bit
  modulus by the best known general method;
- `φ(n) = (p−1)(q−1)` follows immediately, the moment you have one prime factor;
- `d = e⁻¹ mod φ(n)` by extended Euclid;
- then `m = c^d mod n` for any ciphertext.

So the entire security of RSA is a single assumption — *balanced semiprimes are hard
to factor* — plus a small amount of arithmetic. The lesson's own summary of the
asymmetry is the right one: "Everything else in this part is bookkeeping."

**What padding changes, precisely.** It does not change that fact. Padding cannot
make factoring hard. What it changes is that the attacker's assumed function is no
longer the real one.

1. *Randomness.* Textbook RSA has none, so `E` is a function and `E(m₁) = E(m₂)`
   whenever `m₁ = m₂`. That is a dictionary attack. With a fresh random seed masked
   in by MGF1, the same message produces a different ciphertext every time, so
   there is nothing to look up.
2. *The length channel.* Ciphertext length reveals plaintext length. OAEP pads to a
   fixed `k − 2hLen − 2 = 190` bytes, so the length is hidden.
3. *Coprimality.* The padded block begins `0x00 0x02 …`, so it is below `2^120`
   while `p` and `q` are above `2^61`. Neither prime can divide it, so
   `gcd(block, n) = 1` and the short Euler-based proof of correctness applies with no
   case split.
4. *Malleability.* Textbook RSA is a ring homomorphism, so `(c₁·c₂) mod n` decrypts
   to `m₁m₂ mod n` — with the lesson's numbers, `2790 · 2698 mod 3233 = 996`
   decrypts to `680 = 65 · 2000 mod 3233`, a message nobody sent. Masking the
   padding breaks the homomorphism, because the attacker can no longer predict what
   the unmasked block will decrypt to.
5. *Error indistinguishability.* This is the one people forget. PKCS#1 v1.5
   decryptors reported "first byte wrong" and "separator wrong" as *different*
   errors, and Bleichenbacher's 1998 attack used that information to shrink the set
   of acceptable ciphertexts until only the real one remained — at about one request
   per second against every SSL server of the day. OAEP's fix is to raise one
   indistinguishable error for every failure.

**What padding does *not* fix.** It gives no integrity and no sender
authentication. An attacker can still replay an old ciphertext, or swap Bob's
ciphertext for Alice's. That is why TLS signs the transcript as well as encrypting
it: RSA encrypts, it does not authenticate.

</details>

**Q2. The RSA correctness proof works mod `p` and mod `q` separately and then lifts
with CRT. Why not simply apply Euler's theorem directly mod `n`? And what would go
wrong if we did?**

<details>
<summary>Model answer</summary>

**What the direct attempt says.** Euler's theorem states that if `gcd(m, n) = 1`
then `m^φ(n) ≡ 1 (mod n)`. Since `ed ≡ 1 (mod φ(n))`, we have `ed − 1 = k·φ(n)`,
so `m^ed = m·(m^φ(n))^k ≡ m (mod n)`. Two lines — and it is exactly what the
lesson calls the short textbook proof.

**Why it is not enough.** The proof is conditional on `gcd(m, n) = 1`, and that
condition is not under the sender's control. `m` ranges over all of
`0 <= m < n`, and the residues with `gcd(m, n) > 1` are precisely the multiples of
`p` and of `q` — among them `m = 0`, `m = p`, and `m = q`. The short proof
therefore silently omits a class of legal inputs, and the class is far from empty.

**The fix, and why the lesson's version is unconditional.** Work in each factor
separately, and add a case split:

- `m^{ed} = m·(m^{p−1})^k`, and `(p−1) | (ed−1)` because `ed − 1` is a multiple of
  `φ(n) = (p−1)(q−1)`.
- *Case 1: `p | m`.* Both `m^{ed}` and `m` are `0 (mod p)`. Done — and note that
  Fermat is never invoked, which is precisely why this case needs handling at all.
- *Case 2: `p ∤ a`, i.e. `p ∤ m`.* Now `m` is a unit mod `p`, so Fermat applies:
  `m^{p−1} ≡ 1`, hence `m^{ed} ≡ m (mod p)`.

The identical argument with `q` gives `m^{ed} ≡ m (mod q)`. Since `p` and `q` are
coprime, CRT says a congruence holding mod both holds mod `pq = n`. The proof is
now valid for *every* `m`, with no hypothesis on the message at all.

**The structural point.** The lesson remarks that the CRT proof and the RSA proof
use the same two ingredients in opposite directions: CRT goes *up* from `mod p` and
`mod q` to `mod n`, and Fermat comes back *down* inside each factor. That round trip
is the whole reason RSA can be correct unconditionally while a naive Euler argument
cannot. And it is exactly the situation padding removes: because the padded block is
always a unit, you never need the case split. That is not a proof the case split is
unnecessary — only that padding makes you indifferent to it. A hand-rolled
implementation that trusts `gcd(m, n) = 1` and is handed `m = p` will still fail.

</details>

**Q3.** Textbook RSA's determinism is attacked by building a dictionary of
ciphertexts. With a 2048-bit modulus, brute force over messages is hopeless. Why is
determinism still fatal, and what exactly does an attacker exploit?

<details>
<summary>Model answer</summary>

**Why brute force is the wrong frame.** The lesson concedes the point: with a
2048-bit modulus and short messages, "guessing is hopeless". The attacker is not
guessing. The leverage is not the *size* of the message space but the *absence of
randomness*, which converts a one-way function into a lookup table whose entries
come from somewhere else.

**The actual exploit: side information, not search.** `E` is a deterministic
function, so every time the same plaintext is encrypted it produces the identical
ciphertext, forever. That makes the ciphertext a *stable identifier* for the
plaintext. An attacker with any source of correspondence between plaintexts and
ciphertexts gets every other plaintext for free:

- A protocol where the start of the message is a known constant — a cookie, a file
  type, a version number, a JSON key — supplies known-plaintext pairs, hence a
  dictionary entry per observed value.
- Low-entropy plaintexts (a status code, an amount, a "yes") are guessable in
  principle, and a stable ciphertext lets the attacker *confirm* a guess by
  encrypting it themselves. They do not need to break anything, only to match.
- A small public exponent makes confirming cheap: `x^3 mod n` is cheap, whereas
  `x^65537 mod n` is not, so `e = 3` turns "low entropy is unguessable" into "low
  entropy is cheaply checkable".
- The lesson's dictionary is the smallest possible version: a handful of candidate
  values, the same number of ciphertexts, all recovered, with no attack on the
  mathematics whatsoever.

**The compounding effect.** Determinism also *enables* chosen-ciphertext attacks.
Because the decryptor is deterministic, an attacker who submits a ciphertext learns
whether it was one the honest sender would have produced. That is the property
Bleichenbacher exploited, and it is why the fix is a random seed, not merely a
longer key: a fresh random seed per encryption makes the ciphertext a one-time
value with no history and no stable identifier.

**The general lesson.** The security of a one-way function is a claim about *all*
efficient algorithms in one direction. It says nothing about determinism, message
length, or the shape of your plaintexts. Those are protocol properties, and a
mathematically perfect one-way function wrapped in a deterministic protocol is
still insecure. This is the same lesson [Lesson 112](112_hashing.md) teaches about
hash functions: the mathematics can be flawless and the engineering still wrong.

</details>

**Q4. Why is *one indistinguishable decryption error* the load-bearing part of
OAEP, and what exactly did Bleichenbacher's attack do with more than one?**

<details>
<summary>Model answer</summary>

**The oracle.** In PKCS#1 v1.5 the padded block is
`0x00 ‖ 0x02 ‖ PS ‖ 0x00 ‖ M`. The decryptor must check several independent things:
the first byte is `0x00`, the second is `0x02`, a `0x00` separator exists after at
least 8 bytes of filler, and then it extracts the message. Each is a separate
check, and the natural implementation reports each as a *separate* error — "first
byte is not 0x00" versus "no 0x00 separator" versus "padding string shorter than 8
bytes". The lesson's `unpad` raises three different messages, and then immediately
flags this as the weakness.

**What the attacker does with it.** A chosen-ciphertext attacker submits trial
ciphertexts and watches *which* error returns. Each query is at least one bit of
information about the plaintext. Crucially, the attacker does not need to recover
the plaintext directly — only to shrink the set of ciphertexts that *could* be
valid. If a wrong first byte and a wrong separator are distinguishable, then every
ciphertext producing "separator wrong" is known to have a correct first byte. So a
stage that eliminates most ciphertexts still leaves a large set *provably* carrying
the right prefix. Repeat at the next byte and the set collapses to a single
candidate: the real ciphertext, which then decrypts to the real plaintext.

Bleichenbacher's 1998 attack did exactly this against essentially every deployed
SSL server, at roughly one request per second — cheap, patient, and completely
sound. It is often called the "million message attack", because about `2^24`
adaptive queries suffice to recover any RSA-PKCS#1 v1.5 message, which is entirely
practical.

**Why one error fixes it.** If *every* failure — bad first byte, bad second byte,
missing separator, short padding, non-invertible ciphertext, anything — returns an
identical response, the oracle conveys no information at all. Every query's answer
is constant, so the attacker's filter never reduces the candidate set and the
adaptive strategy collapses. The lesson's Challenge solution does precisely this:
one `except ValueError: raise ValueError("decryption error") from None`, converting
every internal failure into one external one.

**The general principle.** A decryption routine is a program processing
attacker-controlled input, so every distinguishable branch in it is a potential
side channel. This is the same family of bug as a timing leak — the lesson's
signature code says to "compare in constant time, and never say *why* it failed" —
and identical failures must be identical in *time* as well as in *message*.
Cryptographic code must be constant-time in its control flow, not merely in its
arithmetic, which is why constant-time implementations are written in careful
low-level languages rather than left to a compiler.

</details>

## Exercises and Solutions

**[ ] Exercise 1 —** Write `mod_inverse(a, m)` from scratch using your own
extended Euclidean algorithm (no `pow(a, -1, m)`). Verify it against `pow` for
5000 random pairs of coprime integers, and check that it returns `None`
exactly when `gcd(a, m) > 1`.

<details>
<summary>Solution</summary>

```python
import random
from math import gcd


def extended_gcd(a, b):
    old_r, r, old_s, s, old_t, t = a, b, 1, 0, 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t


def mod_inverse(a, m):
    g, s, _ = extended_gcd(a % m, m)
    return None if g != 1 else s % m


random.seed(11)
matched = 0
for _ in range(5000):
    m = random.randint(2, 500)
    a = random.randint(0, 4 * m)
    inv = mod_inverse(a, m)
    if gcd(a, m) == 1:
        assert inv is not None and (a * inv) % m == 1
        assert inv == pow(a, -1, m)
        matched += 1
    else:
        assert inv is None
print(f"{matched} of 5000 pairs were coprime; all matched pow(a, -1, m),")
print("and every non-coprime pair returned None")
print("mod_inverse(0, 7) =", mod_inverse(0, 7), " (gcd(0,7) = 7)")
print("mod_inverse(7, 7) =", mod_inverse(7, 7), " (gcd(7,7) = 7)")
```

The `a % m` before calling `extended_gcd` keeps the returned coefficient in
range after the final `% m`, even when `a` is much larger than `m`.

</details>

**[ ] Exercise 2 —** Without using `pow`, compute `2^1000 mod 1000003` by
repeated squaring and confirm it matches `2**1000 % 1000003`. Then compute
`3^(2**64) mod (2^61 − 1)` and confirm it agrees with `pow`. Finally, use
Euler's criterion to decide which of 2, 3, 5, 7 are quadratic residues modulo
`2^61 − 1`, and explain in one sentence why that is a membership test you can
run without taking any square root.

<details>
<summary>Solution</summary>

```python
def mod_pow(base, exp, m):
    result, b = 1, base % m
    while exp:
        if exp & 1:
            result = result * b % m
        b = b * b % m
        exp >>= 1
    return result


m = 1000003
ours, direct, builtin = mod_pow(2, 1000, m), 2**1000 % m, pow(2, 1000, m)
print(f"2^1000 mod {m}:")
print(f"   repeated squaring = {ours}")
print(f"   2**1000 % m       = {direct}")
print(f"   pow(2, 1000, m)   = {builtin}")
assert ours == direct == builtin
print("   all three agree")

p = 2**61 - 1
print()
print(f"p = 2^61 - 1 is prime (Fermat): pow(2, p-1, p) == "
      f"{pow(2, p - 1, p) == 1}")
big = 2**64
print(f"3^(2^64) mod p: ours = {mod_pow(3, big, p)}, pow = {pow(3, big, p)}")
assert mod_pow(3, big, p) == pow(3, big, p)
print(f"   agree; 2^64 has {big.bit_length()} bits, so 65 squarings sufficed")

print()
print("Euler's criterion: a^((p-1)/2) is 1 if a is a square mod p, else p-1")
for a in (2, 3, 5, 7):
    v = pow(a, (p - 1) // 2, p)
    print(f"   a={a}: a^((p-1)/2) mod p = {v}  -> "
          f"{'square' if v == 1 else 'not a square'}")

print()
print("Euler's criterion is one modular exponentiation, and it is how you")
print("decide whether a square root exists without taking the root.")
```

Euler's criterion: for prime `p`, `a^((p−1)/2) ≡ ±1 (mod p)`, with `+1` exactly
when `a` is a square mod `p`. It is a membership test because it never has to
construct the root.

</details>

**[ ] Exercise 3 —** Solve `x ≡ 2 (mod 3)`, `x ≡ 3 (mod 5)` and
`x ≡ 4 (mod 9)`, `x ≡ 2 (mod 7)`, `x ≡ 6 (mod 11)` by hand, then check with a
CRT function. Finally explain in one sentence why `x ≡ 1 (mod 4)` together with
`x ≡ 2 (mod 6)` has no solution.

<details>
<summary>Solution</summary>

Hand solution of the first: `x = 2, 5, 8, …` from mod 3; `x = 3, 8, 13, …` from
mod 5. The first common value is `8`, and solutions repeat with period 15, so
`x ≡ 8 (mod 15)`.

```python
def extended_gcd(a, b):
    old_r, r, old_s, s, old_t, t = a, b, 1, 0, 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t


def crt(residues, moduli):
    M = 1
    for m in moduli:
        M *= m
    x = 0
    for r, m in zip(residues, moduli):
        _, t, _ = extended_gcd(M // m, m)
        x += r * (t * (M // m))
    return x % M, M


print(crt([2, 3], [3, 5]))           # (8, 15), matching the hand solution
x, M = crt([4, 2, 6], [9, 7, 11])
print(crt([4, 2, 6], [9, 7, 11]))
print(f"   {x} mod 9 = {x % 9}, mod 7 = {x % 7}, mod 11 = {x % 11}, M = {M}")
print("   brute force over one period:",
      [k for k in range(M) if k % 9 == 4 and k % 7 == 2 and k % 11 == 6])
print()
print("inconsistent: x = 1 (mod 4) and x = 2 (mod 6)")
print("   brute force over one period:",
      [k for k in range(24) if k % 4 == 1 and k % 6 == 2])
```

Two congruences modulo `m₁` and `m₂` are simultaneously satisfiable exactly when
they agree modulo `gcd(m₁, m₂)`; here they would force `x ≡ 1 (mod 2)` and
`x ≡ 0 (mod 2)` at the same time.

</details>

**[ ] Exercise 4 —** Build the full RSA key pair for `p = 61`, `q = 53` and
encrypt/decrypt the messages `1`, `65`, `2000` and `3232`. Then show that
multiplying two ciphertexts yields the ciphertext of the product of the
plaintexts, and confirm it by decrypting.

<details>
<summary>Solution</summary>

```python
def extended_gcd(a, b):
    old_r, r, old_s, s, old_t, t = a, b, 1, 0, 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t


def mod_inverse(a, m):
    g, s, _ = extended_gcd(a, m)
    return None if g != 1 else s % m


def mod_pow(base, exp, m):
    result, b = 1, base % m
    while exp:
        if exp & 1:
            result = result * b % m
        b = b * b % m
        exp >>= 1
    return result


p, q = 61, 53
n, phi = p * q, (p - 1) * (q - 1)
e = 17
d = mod_inverse(e, phi)
print(f"n = {n}, phi(n) = {phi}, e = {e}, d = {d}, e*d mod phi(n) = {e * d % phi}")
print()

for m in (1, 65, 2000, 3232):
    c = mod_pow(m, e, n)
    print(f"m = {m:>5}  ->  c = {c:>5}  ->  m' = {mod_pow(c, d, n):>5}"
          f"   round trip: {mod_pow(c, d, n) == m}")
print()

m1, m2 = 65, 2000
c1, c2 = mod_pow(m1, e, n), mod_pow(m2, e, n)
forged = (c1 * c2) % n
print(f"c1 = {c1}, c2 = {c2}, (c1*c2) mod n = {forged}")
print(f"decrypting the forgery gives {mod_pow(forged, d, n)}")
print(f"m1*m2 mod n = {(m1 * m2) % n}   match: "
      f"{mod_pow(forged, d, n) == (m1 * m2) % n}")
print()
print("Note m = 3232 = n - 1 round trips with c = m: the only units mod n are")
print("+-1, and 1^e = 1.  Textbook RSA does almost nothing to the plaintext.")
```

</details>

**[ ] Exercise 5 —** Do a complete RSA key generation **by hand, on paper**, for
`p = 61` and `q = 53`, and decrypt a ciphertext by hand. Write out every
intermediate value; do not use a computer until the end, where you check your
answer.

1. Find `n` and `φ(n)`.
2. Show `gcd(17, 3120) = 1` by running the Euclidean algorithm.
3. Find `d` by back-substitution, showing the chain
   `1 = 9 − 8 = 2·9 − 17 = 2·3120 − 367·17`, and reduce `−367` to get `d`.
4. Encrypt `m = 65` by hand with repeated squaring: compute `65^2`, `65^4`, `65^8`,
   `65^16` reduced mod 3233, then combine using `17 = 16 + 1`.
5. Decrypt the resulting ciphertext by hand. Write `2753` in binary, build the
   table of `x^(2^i)` values, and multiply in only those whose bit is set.
6. Finally write code that reproduces every number above and asserts your two hand
   results. Then explain in two sentences why `d` must satisfy `e·d ≡ 1 (mod φ(n))`
   and not `e·d ≡ 1 (mod n)`.

<details>
<summary>Solution</summary>

**1. The modulus and the totient.**

```
n      = 61 * 53 = 3233
phi(n) = (p-1)(q-1) = 60 * 52 = 3120
```

**2. Is `e = 17` legal?** Euclidean algorithm on 3120 and 17:

```
3120 = 183 * 17 + 9
17   =   1 *  9 + 8
9    =   1 *  8 + 1
8    =   8 *  1 + 0
```

The last non-zero remainder is 1, so `gcd(17, 3120) = 1` and 17 is invertible mod
3120. Worth noting how narrow that is: `3`, `5` and `13` all divide 3120, so all
three would be rejected.

**3. Find `d` by back-substitution.** Start from the last non-zero remainder and
work back up the chain:

```
1 = 9 - 8
8 = 17 - 9          so   1 = 9 - (17 - 9) = 2*9 - 17
9 = 3120 - 183*17   so   1 = 2*3120 - 366*17 - 17 = 2*3120 - 367*17
```

So `−367 * 17 ≡ 1 (mod 3120)`, and

```
d = -367 mod 3120 = 3120 - 367 = 2753
```

Check: `17 * 2753 = 46,801`, and `46,801 = 15 * 3120 + 1`. ✓

**4. Encrypt `m = 65` by hand.** `17 = 16 + 1`, so `65^17 = 65^16 * 65`. Build the
squaring table, reducing mod 3233 at every step:

```
65^2  = 4225              = 1 * 3233 + 992        ->  992
65^4  = 992^2 = 984,064   = 304 * 3233 + 1,232   -> 1232
65^8  = 1232^2 = 1,517,824 = 469 * 3233 + 1,547   -> 1547
65^16 = 1547^2 = 2,393,209 = 740 * 3233 + 789     ->  789
65^17 = 789 * 65 = 51,285  = 15 * 3233 + 2,790
```

So **`c = 2790`**. Four squarings and one multiply, which is the whole content of
the `O(log e)` claim.

**5. Decrypt `c = 2790` by hand.** `d = 2753`, and in binary

```
2753 = 101011000001  = 2048 + 512 + 128 + 64 + 1
```

so the set bits are at positions 0, 6, 7, 9 and 11. Square-and-multiply from the
bottom bit up. Each row is the running `base` (squared every time) and the running
`result` (multiplied only when the bit is 1):

```
step  bit  exp after  base = x^(2^step)   result
  0     1      2753              2790          2790
  1     0      1376              2269          2790
  2     0       688              1425          2790
  3     0       344               301          2790
  4     0       172                77          2790
  5     0        86              2696          2790
  6     1        43               632    2790*632   = 1766280  -> 1295
  7     1        21              1765    1295*1765  = 2285675  -> 3177
  8     0        10              1846          3177
  9     1         5               134    3177*134   = 425718   -> 2195
 10     0         2              1791          2195
 11     1         1               545    2195*545   = 1196275  -> 65
```

Twelve steps, and the answer is **`m = 65`**. One row is easy to lose: at step 11 the
exponent halves from 2 to 1, the bit is *still* 1, and you must multiply before the
exponent reaches 0.

**6. Verify, then explain.**

```python
def mod_pow(base, exp, m):
    result, b = 1, base % m
    while exp:
        if exp & 1:
            result = result * b % m
        b = b * b % m
        exp >>= 1
    return result


p, q, e = 61, 53, 17
n, phi = p * q, (p - 1) * (q - 1)
d = 2753

# every value from the hand work above
assert n == 3233 and phi == 3120 and d == 2753
assert 17 * d == 15 * phi + 1                 # 46801 = 15*3120 + 1
assert 65 ** 2 % n == 992                     # the squaring table
assert 65 ** 4 % n == 1232
assert 65 ** 8 % n == 1547
assert 65 ** 16 % n == 789
assert mod_pow(65, e, n) == 2790              # encryption
assert mod_pow(2790, d, n) == 65              # decryption
print("hand answer: c = 2790, m = 65 -- both confirmed")

print(f"2753 in binary is {d:b}, set bits at "
      f"{[i for i in range(12) if (d >> i) & 1]}")
d_right = pow(e, -1, phi)
d_wrong = pow(e, -1, n)
print(f"d = e^-1 mod phi(n)        = {d_right}   (the correct one)")
print(f"e^-1 mod n                 = {d_wrong}   (the wrong one)")
print(f"17 * {d_wrong} mod phi(n)     = {(e * d_wrong) % phi}, not 1")
print(f"decrypting with the wrong one gives {mod_pow(2790, d_wrong, n)}, not 65")
print(f"decrypting with e instead of d gives {mod_pow(2790, e, n)}, not 65")
```

Output:

```
hand answer: c = 2790, m = 65 -- both confirmed
2753 in binary is 101011000001, set bits at [0, 6, 7, 9, 11]
d = e^-1 mod phi(n)        = 2753   (the correct one)
e^-1 mod n                 = 2092   (the wrong one)
17 * 2092 mod phi(n)     = 1244, not 1
decrypting with the wrong one gives 2699, not 65
decrypting with e instead of d gives 1452, not 65
```

**Why `φ(n)` and not `n`.** RSA correctness needs `m^(ed) = m·(m^(p−1))^k` to have
`(p−1) | (ed−1)`, and `p−1` divides `φ(n) = (p−1)(q−1)`, so `ed ≡ 1 (mod φ(n))`
is what supplies `k`. The modulus `n` appears nowhere in that exponent arithmetic.
Reducing the inverse mod `n` gives `d = 2092`, which satisfies
`17·2092 ≡ 1 (mod 3233)` but only `≡ 1244 (mod 3120)`, so the required
`(p−1) | (ed−1)` fails and decryption returns 2699. And using `e` instead of `d`
gives `m^{e^2} = m^{289} = 1452`, which is the same lesson from the other direction:
only `d` is an inverse of `e`.

</details>

**[ ] Exercise 6 (Challenge) — The small-message attack, and what it says about
`e`.** With `e = 3` and modulus `n = 3233`, an attacker who sees `c` can try to
recover `m` by *integer* cube root, using no key material at all. Write
`recover_small(c, e)` using an exact integer `e`-th root — no floating point — and:

1. For every `m` in `0..n-1`, check exactly when `recover_small(m^3 mod n, 3)`
   returns `m`. Report how many, the largest, and explain the pattern.
2. Show the attack fails from the first `m` beyond that, and explain in terms of
   what `m^3 mod n` actually is once `m^3 > n`.
3. Scale up: with `e = 3` and a real 2048-bit `n`, how many bits of plaintext are
   exposed? And with `e = 65537`? Then say what the *real* reason for 65537 is,
   given that the small-message attack is already dead at that exponent.
4. Explain in two sentences why OAEP kills this attack even at `e = 3`.

<details>
<summary>Solution</summary>

```python
def mod_pow(base, exp, m):
    result, b = 1, base % m
    while exp:
        if exp & 1:
            result = result * b % m
        b = b * b % m
        exp >>= 1
    return result


def iroot(value: int, k: int) -> int:
    """The exact integer k-th root: the largest r with r**k <= value.

    Newton's method on the integers.  A float-based k-th root silently returns
    the wrong answer for large values, which is precisely the case that matters.
    """
    if value < 0:
        raise ValueError("negative")
    if value in (0, 1):
        return value
    r = 1 << ((value.bit_length() + k - 1) // k)     # start above the root
    while True:
        nxt = ((k - 1) * r + value // r ** (k - 1)) // k
        if nxt >= r:
            return r
        r = nxt


def recover_small(c: int, e: int) -> int:
    """Try to invert c = m^e mod n with no key material at all.

    Valid only while m^e < n, because then the modular reduction was a no-op
    and c is the exact e-th power.
    """
    r = iroot(c, e)
    return r if r ** e == c else -1


n = 3233
E_SMALL = 3

# ---- 1. exactly which messages the attack solves -----------------------------
solved = [m for m in range(n) if recover_small(mod_pow(m, E_SMALL, n), E_SMALL) == m]
broken = [m for m in range(n) if mod_pow(m, E_SMALL, n) != m]
print(f"e = {E_SMALL}, n = {n}")
print(f"messages the attack solves  : {len(solved)} of {n}")
print(f"messages it does not solve : {len(broken)}")
print(f"the largest solved message  : m = {solved[-1]}")
print(f"  and indeed 14^3 = {14 ** 3} < n = {n}, while 15^3 = {15 ** 3} > {n}")
print("so the attack works exactly while m^e < n")
print()

# ---- 2. the first failure, explained ----------------------------------------
m = 15
c = mod_pow(m, E_SMALL, n)
print(f"m = {m}, m^3 = {m ** 3}, m^3 mod n = {c}")
print(f"  integer cube root of the ciphertext: {iroot(c, E_SMALL)}  (wanted {m})")
print(f"  recovery returns {recover_small(c, E_SMALL)}")
print("  Once m^3 > n the reduction really reduces, and the ciphertext stops")
print("  being a cube at all: 3375 - 3233 = 142.  142 is not a cube of anything,")
print("  so the structure the attack relied on is simply gone.")
print()

# ---- 3. the same reasoning at 2048 bits --------------------------------------
BITS = 2048
print(f"a {BITS}-bit modulus, so n < 2^{BITS}")
for e in (3, 65537):
    exposed = (BITS - 1) // e
    print(f"   e = {e:<7} messages up to n^(1/{e}) < 2^{exposed} fall to a plain "
          f"{e}-th root   ({exposed} bits of plaintext exposed)")
print()
print("At e = 65537 the exposed window is 0 bits, so the small-message attack is")
print("already dead.  So why 65537?  Not to stop this attack -- a small public")
print("exponent is chosen for SPEED, and e = 3 is rejected for a different reason:")
print("with deterministic textbook RSA, an attacker can confirm a guessed message")
print("by encrypting it, and x^3 mod n is cheap while x^65537 mod n is not.  That")
print(f"turns 'low entropy is unguessable' into 'low entropy is cheaply checkable'.")
print(f"65537 = 2^16 + 1 is prime, coprime to phi(n), and has only {(65537).bit_length()} bits,")
print(f"so encryption costs about 2 * {(65537).bit_length()} = {2 * (65537).bit_length()} modular multiplications")
print("instead of 65536.  Security comes from the modulus; e is a speed choice.")
print()

# ---- 4. why padding kills it --------------------------------------------------
print("With OAEP the attacker is not handed x^e mod n at all, but em^e mod n for a")
print("padded block em = 0x00 || maskedSeed || maskedDB of a fixed")
print("k - 2*hLen - 2 = 190 bytes.  The seed is fresh randomness and the mask is a")
print("one-way function of it, so knowing e tells the attacker nothing about the")
print("structure of em, and 'take the e-th root' has nothing to take a root of.")
print("Padding defeats this attack by removing the algebraic structure, not by")
print("making the modulus bigger.")
```

Output:

```
e = 3, n = 3233
messages the attack solves  : 15 of 3233
messages it does not solve : 3224
the largest solved message  : m = 14
  and indeed 14^3 = 2744 < n = 3233, while 15^3 = 3375 > 3233
so the attack works exactly while m^e < n

m = 15, m^3 = 3375, m^3 mod n = 142
  integer cube root of the ciphertext: 5  (wanted 15)
  recovery returns -1
  Once m^3 > n the reduction really reduces, and the ciphertext stops
  being a cube at all: 3375 - 3233 = 142.  142 is not a cube of anything,
  so the structure the attack relied on is simply gone.

a 2048-bit modulus, so n < 2^2048
   e = 3       messages up to n^(1/3) < 2^682 fall to a plain 3-th root   (682 bits of plaintext exposed)
   e = 65537   messages up to n^(1/65537) < 2^0 fall to a plain 65537-th root   (0 bits of plaintext exposed)

At e = 65537 the exposed window is 0 bits, so the small-message attack is
already dead.  So why 65537?  Not to stop this attack -- a small public
exponent is chosen for SPEED, and e = 3 is rejected for a different reason:
with deterministic textbook RSA, an attacker can confirm a guessed message
by encrypting it, and x^3 mod n is cheap while x^65537 mod n is not.  That
turns 'low entropy is unguessable' into 'low entropy is cheaply checkable'.
65537 = 2^16 + 1 is prime, coprime to phi(n), and has only 17 bits,
so encryption costs about 2 * 17 = 34 modular multiplications
instead of 65536.  Security comes from the modulus; e is a speed choice.

With OAEP the attacker is not handed x^e mod n at all, but em^e mod n for a
padded block em = 0x00 || maskedSeed || maskedDB of a fixed
k - 2*hLen - 2 = 190 bytes.  The seed is fresh randomness and the mask is a
one-way function of it, so knowing e tells the attacker nothing about the
structure of em, and 'take the e-th root' has nothing to take a root of.
Padding defeats this attack by removing the algebraic structure, not by
making the modulus bigger.
```

**The pattern in part 1.** The attack succeeds on exactly the 15 messages
`m = 0, 1, …, 14`, which are precisely the `m` with `m^3 < 3233`. Everything from
`m = 15` upward is a genuine one-way problem: recovering `m` from 142 requires
factoring, which at 3233 bits is trivial but on a real modulus is the hard
assumption. "15 of 3233" looks safe, and that is exactly the trap — scale the
modulus to 2048 bits and the vulnerable window becomes about 682 bits, or roughly
85 bytes, of *every short message*.

**Why integer roots and not floats.** `c ** (1/3)` on a 2048-bit integer is
evaluated in floating point and will be silently wrong for any `c` above about
`2^53`. A small-message attack implemented with floats simply does not work at real
key sizes — a security bug that is really a *precision* bug, and one that would
survive a casual test on toy values. Newton's method on the integers has no such
caveat.

**The honest answer to part 3.** `e = 65537` is *not* chosen to defeat this attack;
it is chosen for speed, and `e = 3` is rejected for a more embarrassing reason. This
is the same lesson as Bleichenbacher: the danger is never "the attacker can compute
this fast", it is "the attacker can *verify* a guess fast". Padding fixes all of it,
and the lesson is right that RSA encrypts but does not authenticate — which is why
TLS signs as well as encrypts.

</details>

**Challenge** — Implement OAEP-style padding from scratch (a 1-byte SHA-256
label and 1-byte MGF1 output are enough for a toy modulus), then show three
things: (a) the same message encrypts differently under different seeds; (b) a
single-bit change to the ciphertext is always rejected, with the *same* error
message every time; (c) an oversized message is rejected at encryption time
rather than silently truncated.

<details>
<summary>Solution</summary>

```python
from hashlib import sha256

p, q = 4611686018427388039, 4611686018427388073
n = p * q
phi = (p - 1) * (q - 1)
e = 65537


def extended_gcd(a, b):
    old_r, r, old_s, s, old_t, t = a, b, 1, 0, 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t


d = extended_gcd(e, phi)[1] % phi
k = (n.bit_length() + 7) // 8
H = 1                                     # bytes of hash kept; real OAEP: 32
LABEL = sha256(b"").digest()[:H]


def mod_pow(base, exp, m):
    result, b = 1, base % m
    while exp:
        if exp & 1:
            result = result * b % m
        b = b * b % m
        exp >>= 1
    return result


def mgf1(data: bytes, length: int) -> bytes:
    """Hash the seed, then the seed with a counter, until we have enough."""
    out, counter = b"", 0
    while len(out) < length:
        out += sha256(data + counter.to_bytes(4, "big")).digest()
        counter += 1
    return out[:length]


def encrypt(message: bytes, seed: int) -> int:
    # (c) reject an oversized message rather than truncating it
    if len(message) > k - 2 * H - 2:
        raise ValueError(f"message of {len(message)} bytes exceeds "
                         f"{k - 2 * H - 2}")
    ps = b"\x00" * (k - 2 * H - 2 - len(message))
    db = LABEL + ps + b"\x01" + message        # the 0x01 marks where M starts
    db_mask = mgf1(seed.to_bytes(H, "big"), k - H - 1)
    masked_db = bytes(a ^ b for a, b in zip(db, db_mask))
    seed_mask = mgf1(masked_db, H)
    masked_seed = bytes(a ^ b for a, b in zip(seed.to_bytes(H, "big"), seed_mask))
    em = b"\x00" + masked_seed + masked_db
    if int.from_bytes(em, "big") >= n:
        raise ValueError("encoded message is not smaller than n")
    return mod_pow(int.from_bytes(em, "big"), e, n)


def decrypt(c: int) -> bytes:
    # One error type for every failure.  Bleichenbacher's attack on PKCS#1
    # v1.5 worked precisely because the failures were distinguishable.
    try:
        em = mod_pow(c, d, n).to_bytes(k, "big")
        if em[0] != 0:
            raise ValueError
        masked_seed, masked_db = em[1:1 + H], em[1 + H:]
        seed = bytes(a ^ b for a, b in zip(masked_seed, mgf1(masked_db, H)))
        db = bytes(a ^ b for a, b in zip(masked_db, mgf1(seed, k - H - 1)))
        if db[:H] != LABEL or 0x01 not in db[H:]:
            raise ValueError
        return db[db.index(0x01, H) + 1:]
    except ValueError:
        raise ValueError("decryption error") from None


print("(a) the same message, three different seeds")
for seed in (0x11, 0x22, 0x33):
    c = encrypt(b"OK", seed)
    print(f"   seed={seed:#04x}  c={c}  decrypts to {decrypt(c)!r}")
print()
print("(b) flipping one bit of the ciphertext is always rejected")
c = encrypt(b"OK", 0x11)
rejected = 0
for bit in range(0, c.bit_length(), 7):
    try:
        decrypt(c ^ (1 << bit))
    except ValueError:
        rejected += 1
print(f"   {rejected} of {len(range(0, c.bit_length(), 7))} single-bit flips "
      f"were rejected with the same error")
print()
print("(c) oversized messages are rejected at encryption time")
for size in (k - 2 * H - 2, k - 2 * H - 1):
    try:
        encrypt(b"x" * size, 0x11)
        print(f"   {size} bytes: accepted")
    except ValueError as err:
        print(f"   {size} bytes: {err}")
```

The single indistinguishable error in `decrypt` is the whole point of OAEP
versus PKCS#1 v1.5. Bleichenbacher's attack worked precisely because v1.5
decryptors returned *different* messages for different failures.

</details>

## Summary

- `a ≡ b (mod m)` means `m` divides `a − b`; it survives addition and
  multiplication, but not cancellation or division, because `m` can be a zero
  divisor.
- `a` has an inverse mod `m` **iff** `gcd(a, m) = 1`. Over a prime modulus
  every nonzero residue is invertible; that is why primes are used.
- Fermat gives `a^(p−1) ≡ 1 (mod p)` for prime `p ∤ a`; Euler gives
  `a^φ(m) ≡ 1 (mod m)` for `gcd(a, m) = 1`; both fail without coprimality.
- The order of an element divides `φ(m)` (Lagrange), and a primitive root has
  order exactly `φ(m)`. Recovering the exponent from `g^x mod p` is the
  discrete logarithm problem — the one-way function behind Diffie-Hellman.
- The CRT combines pairwise-coprime moduli; RSA's proof uses it in reverse,
  proving the relation mod `p` and mod `q` and lifting it to mod `n`.
- RSA keygen is `n = pq`, `φ(n) = (p−1)(q−1)`, `d = e⁻¹ mod φ(n)`. Encryption
  is `c = m^e mod n`, decryption is `m = c^d mod n`, and correctness follows
  from Fermat in each factor plus CRT.
- `m^e mod n` costs `O(log e)` modular multiplications because squaring
  doubles the exponent, while inverting it needs `φ(n)`, which needs the
  factorisation. That asymmetry is the security of everything in this part.
- Textbook RSA is insecure because it is deterministic, malleable, and has no
  integrity; OAEP fixes the first two with random masking and a single
  indistinguishable decryption error, and TLS adds a signature for the third.

## Next

[112 — Hashing](112_hashing.md) takes the modular arithmetic of this lesson and
the prime moduli of [Lesson 110](110_number_theory.md) and builds hash tables
with chaining and open addressing, explains the birthday paradox, and shows why
cryptographic hash functions need properties that ordinary ones do not.