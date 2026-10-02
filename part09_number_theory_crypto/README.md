# Part 09 — Number Theory and Cryptography

The arithmetic behind security, hashing, and error correction.

## What this part covers

Four lessons on the mathematics that runs underneath every system you rely on
for integrity, confidentiality, and availability. The through-line is that all
four are the *same* mathematics — modular arithmetic, plus the linear algebra
from [Part 03](../part03_linear_algebra/) and the combinatorics from
[Part 02](../part02_discrete_combinatorics/) — pointed at four different
problems.

| # | Lesson | What it gives you |
| --- | --- | --- |
| 110 | [Number Theory](110_number_theory.md) | Divisibility, primes, the Fundamental Theorem of Arithmetic, `gcd`/`lcm`, the Euclidean algorithm with a proof, Bézout's identity, the Sieve of Eratosthenes, and why factoring is hard |
| 111 | [Modular Arithmetic and Public-Key Crypto](111_modular_arithmetic_and_crypto.md) | Congruences, modular inverses, Fermat's little theorem, Euler's theorem, primitive roots, the Chinese Remainder Theorem, RSA end to end with toy numbers, why textbook RSA is insecure, OAEP, and Diffie-Hellman |
| 112 | [Hashing](112_hashing.md) | Hash functions and their four requirements, hash tables with chaining and open addressing, load factor and resizing, collision resolution, tombstones, the birthday paradox, Merkle trees, and why cryptographic hashes need different properties |
| 113 | [Error-Correcting Codes](113_error_correcting_codes.md) | Noisy channels, parity bits, Hamming distance and minimum distance, linear codes over `GF(2)`, Hamming(7,4) and (8,4), syndromes, Reed-Solomon over `GF(256)`, and why QR codes and CDs work |

## The three ideas that connect them

**Arithmetic modulo a number is different arithmetic.** Lesson 110 gives you
`gcd` and Bézout's identity; Lesson 111 turns those into modular inverses,
which unlocks Fermat's little theorem, and Fermat's little theorem is what
makes RSA invertible. Nothing new is invented in 111 — the same Bezout
coefficient from 110 becomes the decryption key.

**Some directions are easy and the reverse is hard.** Multiplying two numbers
is trivial; factoring one is not, which is RSA's whole security basis.
Evaluating a hash is trivial; inverting it is not, which is why a hash is a
one-way function you can check but not forge. Raising to a power is trivial;
finding the exponent is the discrete logarithm, which is Diffie-Hellman's
security basis. This asymmetry appears in three lessons in three costumes.

**Redundancy can undo damage, not just reveal it.** A hash detects a change and
stops. An error-correcting code *repairs* it, and the amount of redundancy
needed is governed by one number: the minimum distance between valid messages.
Lesson 113 is where the part stops talking about security and starts talking
about reliability.

## What this part assumes

- Lesson 24 (recurrence relations) — for the `π(N) ≈ N / ln N` counting result,
  and nothing more.
- Lesson 23 (pigeonhole principle) — collisions are unavoidable by that theorem,
  and it is the cleanest proof that hashing cannot be injective.
- Lesson 32 (Gaussian elimination) and Lesson 34 (rank and dimension) — helpful
  for the generator and parity-check matrices in Lesson 113, though both are
  introduced from scratch there.
- Lesson 80 (big-O) — the `O(log n)` claims about Euclid and modular
  exponentiation only mean something with it.
- Basic Python, including classes. Every code example is standard library only.

Nothing else. You do not need prior cryptography, and you do not need to know
what a finite field is before Lesson 113 — it is built there from scratch.

## A suggested route

Read them in order. The dependency chain is real:

```
110 (gcd, Bezout)
  -> 111 (inverses, Fermat, RSA, CRT)
       -> 112 (modular hashing, birthday paradox)
            -> 113 (GF(2), GF(256), Hamming, Reed-Solomon)
```

If you only want the security material, read 110, 111 and 112 and skip 113.
If you only want the reliability material — ECC memory, storage, deep-space
links — read 110 for the sieve and 113, and skim 111's Chinese Remainder
Theorem section.

## Exercises

Every lesson ends with worked exercises and full solutions in the same file, so
the repository is usable offline. Several exercises are deliberately
measurable rather than proveable: you are asked to print the number and then
explain why it is that number.

The most satisfying exercise in the part is Exercise 4 of Lesson 111, which
asks you to build a working OAEP padding and then break PKCS#1 v1.5 with it —
including the specific error-message distinction that made every SSL server in
1998 vulnerable. The most surprising is Exercise 4 of Lesson 113, where the same
burst of 12 corrupted symbols destroys a codeword outright and is repaired
perfectly once you interleave, with the code itself completely unchanged.

## Where to go next

[Part 10 — Tensors and Numerical Methods](../part10_tensors_numerical/) applies
the same themes to floating point: modular arithmetic is *exact*, so it never
rounds, while real arithmetic does, and the difference is where most numerical
bugs come from.