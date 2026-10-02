# 113 — Error-Correcting Codes

**Part**: part09_number_theory_crypto · **Prerequisites**: 110, 111 · **Time**: 40 min

---

## In Plain Words

Signals get corrupted. A bit that arrived as a 1 arrives as a 0, a scratch on
a CD destroys a run of thousands of bits, a QR code gets folded. The fix is
not to prevent corruption — that is impossible — but to add a small amount of
carefully chosen extra information so the receiver can work out what was
damaged and undo it. Send a parity bit and you notice that something broke. Send
a Hamming code and you can put the broken bit back exactly. Send a
Reed-Solomon code and you can fix whole bytes at once. The whole subject is
governed by one number, the minimum distance between valid messages: a code
whose valid messages are never closer than `d` bits apart can detect `d − 1`
errors and repair `⌊(d−1)/2⌋` of them. Everything else in this lesson is
choosing `d` and paying for it.

## Why Computer Science Cares

- **QR codes.** Every QR code carries Reed-Solomon parity over GF(256), with
  between 10 and 30 parity symbols depending on the level you select. Level L
  recovers 7%, level H recovers 30%, and the printed pattern on the label tells
  you which one you are paying for.
- **CDs and DVDs.** A CD interleaves and Reed-Solomon encodes audio, and adds
  CIRC for the burst errors. That is why a scratch that would destroy a
  conventional disc only makes a few hundred milliseconds go quiet.
- **ECC memory.** Every x86 CPU since the Pentium has 7 extra bits per byte, a
  Hamming-derived SECDED code, so a cosmic ray flipping a bit in your RAM is
  repaired silently instead of crashing the machine.
- **Deep space.** Voyager, New Horizons and the Mars rovers send convolutional
  codes with interleaving, because a bit error 200 million kilometres away is
  just as likely as one next door and there is no retransmission.
- **RAID and transports.** RAID-5 uses parity, which is a distance-2 code:
  it detects a bad sector but cannot repair it without a second failure.

## The Formal Version

Notation follows [SYMBOLS.md](../SYMBOLS.md). Used here: `d(x, y)`, `d_min`,
`GF(2)`, `t`, `O()`.

### The noisy channel

**Definition.** The **binary symmetric channel** with bit error rate `p` flips
each bit independently with probability `p`. A `0` becomes a `1` and a `1`
becomes a `0` with equal probability.

**Definition.** **Detection** means noticing that something is wrong.
**Correction** means working out what was wrong and repairing it. Correction
implies detection and strictly costs more, because to correct you must be able
to tell two legitimate messages apart, not merely notice a third possibility.

### Distance

**Definition.** The **Hamming distance** `d(x, y)` is the number of positions
where two equal-length bit strings differ. The **weight** `w(x)` is
`d(x, 0)`, the number of 1s in `x`.

**Definition.** The **minimum distance** `d_min` of a code `C` is
`d_min = min { d(x, y) : x ≠ y ∈ C }`.

**Theorem.** A code with minimum distance `d` detects up to `d − 1` errors and
corrects up to `t = ⌊(d−1)/2⌋`.

*Explanation (detection).* One error moves a codeword to a vector at distance
exactly 1. If `d ≥ 2` no two codewords are at distance 1, so the corrupted
vector is not a codeword and the receiver notices. In general an error pattern
of weight `e` moves `x` to distance `e` from `x`; this can only be another
codeword if `d ≤ e`, so errors of weight up to `d − 1` are always caught. ∎

*Explanation (correction).* After `e` errors the received vector is at distance
`e` from the true codeword and at distance at least `d − e` from any other
(distance satisfies the triangle inequality). To identify the true word with
certainty we need `e < d − e`, i.e. `2e < d`, so `e ≤ ⌊(d−1)/2⌋`. Geometrically,
the balls of radius `t` around the codewords must be disjoint. ∎

The gap between the two numbers is the whole difficulty. Detection asks "is
this one of mine?", which one bit answers. Correction asks "which one of mine
is it?", which is a search — and the search is only conclusive because the
codewords are far enough apart.

### Repetition and parity as first codes

**Definition.** The **repetition-3 code** is `{000, 111}`, minimum distance 3,
so it detects 2 errors and corrects 1. Applied to `n` bits it costs `3n` bits
for `n` bits of data.

**Definition.** The **even-parity code** is `{x : w(x) ≡ 0 (mod 2)}`. Two of its
codewords differ in an even number of positions, so `d_min = 2`: it detects 1
error and corrects none. Adding a second, independent parity check gives
`d_min = 4`: detects 3, corrects 1. This is the extended Hamming code.

**Theorem.** The `d_min` of the even-parity code is exactly 2.

*Explanation.* `w(0000) = 0` and `w(0011) = 2`, both even, and they differ in
exactly 2 positions, so `d_min ≤ 2`. Flipping one bit changes parity, so no two
codewords differ in 1 position, so `d_min ≥ 2`. ∎

### Linear codes over GF(2)

**Definition.** `GF(2) = {0, 1}` with addition and multiplication mod 2; so
`1 + 1 = 0` and `x + x = 0`. **Addition is XOR**, which is why every operation
below is an `^`.

**Definition.** A code is **linear** if `u, v ∈ C` implies `u + v ∈ C`. Equivalently,
`C` is the row space of some matrix.

**Theorem.** A linear code has `d_min` equal to the smallest **weight** of any
nonzero codeword.

*Explanation.* If `x, y ∈ C` then `x + y ∈ C` and has weight `d(x, y)`. So the
smallest weight among nonzero codewords is attained by some pair, and equals the
minimum over all pairs. ∎

This is the practical reason linear codes are used: you do not check all pairs
of codewords, you check the `2^k − 1` nonzero XOR combinations of the basis — or
better, you just find the minimum row weight of a generator matrix.

**Definition.** A **generator matrix** `G` (`k × n`) maps data to codewords by
`c = m·G`, with multiplication over `GF(2)`. A **parity-check matrix** `H`
(`(n−k) × n`) is any matrix with `H·cᵀ = 0` exactly when `c` is a codeword.

**Definition.** The **syndrome** of a received word is `s = H·rᵀ`.

**Theorem.** `s = 0` iff `r` is a codeword. For a linear code, `s = H·(c + e)ᵀ =
H·eᵀ`, so the syndrome depends only on the **error**, not on the message.

*Explanation.* `H·cᵀ = 0` by construction, so only `e` survives. This is the
single most useful fact in the subject: the receiver can compute a small
function of the error alone, with no knowledge of the data. ∎

### Hamming codes and the syndrome as an index

**Definition.** The **Hamming(7,4) code** puts parity bits at positions 1, 2
and 4 (counting from 1) and data at 3, 5, 6, 7. Parity bit at position `2^k`
covers the positions whose binary index has bit `k` set.

**Construction.** `H` is the 3 × 7 matrix whose column `i` is the binary
expansion of `i`:

```
H = | 1 0 1 0 1 0 1 |
    | 0 1 1 0 0 1 1 |
    | 0 0 0 1 1 1 1 |
```

**Theorem.** Hamming(7,4) has `d_min = 3`, detects 2 errors, corrects 1.

**Key property.** If bit `i` (1-based) is the only error, the syndrome is
numerically equal to `i`.

*Explanation.* Column `i` of `H` is the binary expansion of `i`. The syndrome of
a single-bit error is that column, so reading it as a 3-bit number gives `i`
directly. That is why `r` parity bits locate up to `2^r − 1` error positions:
with `r` parity bits and `n = 2^r − 1` total, you can point at any of the `n`
positions. ∎

**Why three parity bits is minimal.** Two parity bits give a 2-bit syndrome,
naming at most 4 positions, so a 3-bit Hamming code can only protect 3
positions — worse than parity. Three parity bits name 7, which covers 4 data
bits plus 3 parity bits. The general family is **Hamming(2^r − 1, 2^r − 1 − r)**.

**Extended Hamming SECDED.** Add one overall parity bit, Hamming(8,4). The
overall parity plus the three positional checks give four syndromes for four
bits, and the mapping from error pattern to syndrome becomes injective for
weights 0, 1, 2, so the decoder can *distinguish* one error from two: it
corrects the first and reports the second. This is SECDED — single-error
correct, double-error detect — and it is exactly what x86 ECC memory uses.

### Reed-Solomon

**Definition.** `GF(2^m)` is the field of degree-`< m` polynomials over
`GF(2)`, modulo an irreducible polynomial of degree `m`. `GF(256) = GF(2^8)` is
the byte-sized field QR codes use, built mod `0x11d`.

**Definition.** A **symbol** is one element of `GF(2^m)`, carrying `m` bits. An RS
code over `GF(2^m)` treats symbols the way a binary code treats bits.

**Construction.** Take `g(x) = Π_{i=0}^{t−1} (x − α^i)`, the generator polynomial
with roots `α^0 … α^(t−1)`. Encode `m(x)` as the codeword
`m(x)·x^t + (m(x)·x^t mod g(x))` — the data followed by the remainder of
dividing the shifted message by `g`. This is **systematic** encoding.

**Theorem.** The codeword is divisible by `g`, so it evaluates to zero at
`α^0 … α^(t−1)`.

*Explanation.* `c(x) = m(x)x^t + r(x)` where `m(x)x^t = q(x)g(x) + r(x)`, so
`c(x) = q(x)g(x) + 2r(x) = q(x)g(x)` in characteristic 2. The remainder `r`
vanishes at every root of `g`. ∎

**Theorem.** The `t` values `S_j = c(α^j)`, called the **syndromes**, are zero
for a clean codeword and depend only on the error pattern.

*Explanation.* Same argument as the binary case: `c = codeword + error`, and the
codeword part evaluates to zero at every `α^j`. If the error has values `e_i` at
positions `i` (counting from the right as powers of `x`), then
`S_j = Σ e_i (α^j)^i = Σ e_i α^(ji)`. One error at power `i` therefore gives
`S_j = e·α^(ji)` for all `j`, and the ratios of syndromes reveal `i`. ∎

**Decoding by search.** One error: `e = S_0` and `i = log(S_1 / S_0)`. Two
errors: solve `S_0 = e₁ + e₂` and `S_1 = e₁L₁ + e₂L₂` for `e₁, e₂`, then verify
against `S_2, S_3`. Production decoders instead use Berlekamp-Massey to build an
error locator polynomial and Chien search to root it; the code below uses the
search because it fits on a page and gives identical answers.

**Why bytes, not bits.** One corrupted symbol can destroy up to `m` bits, so RS
is matched to *burst* errors, which is the CD situation. Binary Hamming codes
are better for isolated single-bit flips, which is the ECC-memory situation.

## Worked Example

Encode the data bits `1011` with Hamming(7,4) and then repair a single error.

**Step 1 — place the data.** Data occupies positions 3, 5, 6, 7. So
`1011` goes to position 3 = 1, position 5 = 0, position 6 = 1, position 7 = 1.

Current: `p₁  p₂  1  p₄  0  1  1`

**Step 2 — parity bit 1** (position 1) covers positions 1, 3, 5, 7 — those with
bit 0 set in their index. Among the data bits, positions 3 and 7 are 1; position
5 is 0. Two 1s is already even, so `p₁ = 0`.

**Step 3 — parity bit 2** (position 2) covers positions 2, 3, 6, 7. Data there:
position 3 = 1, position 6 = 1, position 7 = 1. Three 1s is odd, so `p₂ = 1`.

**Step 4 — parity bit 4** (position 4) covers positions 4, 5, 6, 7. Data there:
0, 1, 1 — two 1s, even, so `p₄ = 0`.

Codeword: `0 1 1 0 0 1 1`.

**Step 5 — verify by syndrome.** Check the three groups:

- positions 1, 3, 5, 7: `0 + 1 + 0 + 1 = 2`, even ✓
- positions 2, 3, 6, 7: `1 + 1 + 1 + 1 = 4`, even ✓
- positions 4, 5, 6, 7: `0 + 0 + 1 + 1 = 2`, even ✓

Syndrome 0, so the word is clean.

**Step 6 — corrupt bit 5.** Received `0 1 1 0 1 1 1`.

- positions 1, 3, 5, 7: `0 + 1 + 1 + 1 = 3`, odd → check 1 fails
- positions 2, 3, 6, 7: `1 + 1 + 1 + 1 = 4`, even → check 2 passes
- positions 4, 5, 6, 7: `0 + 1 + 1 + 1 = 3`, odd → check 4 fails

Failures at checks 1 and 4. Read as a binary number with check 1 as the low bit
and check 4 as the high bit: `1 + 0 + 4 = 5`. The syndrome is **5**, which is
exactly the position of the flipped bit. Flip it, and we recover `0110011` and
the data `1011`.

**Step 7 — why three bits of redundancy.** Seven positions need to be named,
and three bits give exactly `2³ = 8` names. Four positions for data, three for
naming, seven total. Notice the redundancy is 3/7 ≈ 43%, far cheaper than the
repetition code's 200%, and it detects two errors as well.

**Step 8 — two errors do not work.** Flip positions 3 and 5 of `0110011` to get
`0100111`. The syndrome is 6, so the decoder flips bit 6 and returns `0101` —
confidently wrong. It cannot tell: `0100111` is at distance 2 from `0110011`
and at distance 2 from some other codeword. This is the `⌊(d−1)/2⌋ = 1` bound
in action, and it is why x86 memory adds a fourth parity bit so that two errors
are *detected* rather than silently mis-corrected.

## Runnable Code

### 1. The noisy channel, parity bits, and repetition

```python
"""The noisy channel, and the simplest thing that helps: parity bits.

A parity bit is one extra bit that makes the number of 1s even (or odd).  It
cannot tell you WHICH bit flipped, so it detects but does not correct.  That
single fact is the whole reason Hamming codes have the shape they do.
"""
import random


def parity(data: str, kind: str = "even") -> str:
    """Append one parity bit so the total number of 1s has the given parity."""
    ones = data.count("1")
    if kind == "even":
        return data + ("0" if ones % 2 == 0 else "1")
    return data + ("1" if ones % 2 == 0 else "0")


def check_parity(block: str, kind: str = "even") -> bool:
    ones = block.count("1")
    return ones % 2 == 0 if kind == "even" else ones % 2 == 1


def flip(block: str, position: int) -> str:
    chars = list(block)
    chars[position] = "1" if chars[position] == "0" else "0"
    return "".join(chars)


def channel(bits: str, p: float) -> str:
    """The binary symmetric channel: flip each bit independently with prob p."""
    return "".join("1" if random.random() < p else b for b in bits)


random.seed(4)
print("4 data bits, one parity bit:")
for data in ("0000", "1010", "1101", "0111"):
    block = parity(data)
    print(f"   data {data} -> {block}   ones = {block.count('1')} "
          f"(even)   check: {check_parity(block)}")
print()

TRIALS = 4000
print("Now corrupt it.")
for n_errors, label in ((1, "single-bit"), (2, "two-bit")):
    undetected = 0
    for _ in range(TRIALS):
        block = parity("".join(random.choice("01") for _ in range(4)))
        for pos in random.sample(range(5), n_errors):
            block = flip(block, pos)
        if check_parity(block):
            undetected += 1
    print(f"   {label} errors NOT detected: {undetected} of {TRIALS}")
print("   parity catches every single-bit error and never a two-bit error,")
print("   because two flips change the count of 1s by 0 or by 2, both even.")
print()

print("Repeating each bit three times fixes any single-bit error by majority")
print("vote, but costs three times the bandwidth:")
for data in ("1011", "0100"):
    tripled = "".join(b * 3 for b in data)
    print(f"   data {data} -> {tripled}   ({len(tripled)} bits for {len(data)})")
print()

print("Now measure all three schemes over a channel with bit error rate p.")
print("Each trial sends a random 4-bit message and checks whether the receiver")
print("recovers it.  'parity' is scored on *detecting* the error, which is all")
print("it can do.")
print(f"{'p':>7} {'uncoded':>10} {'parity detects':>16} {'repetition corrects':>20}")
for p in (0.01, 0.05, 0.1, 0.2):
    runs = 4000
    uncoded = detected = corrected = 0
    for _ in range(runs):
        data = "".join(random.choice("01") for _ in range(4))

        received = channel(data, p)
        uncoded += received == data

        block = parity(data)
        received = channel(block, p)
        detected += not check_parity(received)

        received = channel("".join(b * 3 for b in data), p)
        voted = "".join(
            "1" if received[3 * i:3 * i + 3].count("1") >= 2 else "0"
            for i in range(4))
        corrected += voted == data
    print(f"{p:>7.2f} {uncoded / runs:>10.3f} {detected / runs:>16.3f} "
          f"{corrected / runs:>20.3f}")
print()
print("Repetition corrects; parity only detects.  Repetition also needs 3x the")
print("bandwidth, which is why real systems add just enough redundancy to fix")
print("exactly the errors they expect.  That is what the rest of this lesson is")
print("about.")
```

### 2. Distance, minimum distance, and what it buys

```python
"""Hamming distance, minimum distance, and what it buys you.

The minimum distance d of a code is the smallest number of bit positions in
which any two valid codewords differ.  Everything about error correction
follows from one number:

    * the code detects up to d - 1 errors
    * the code corrects up to floor((d - 1) / 2) errors

Everything here is computed by brute force, so the numbers are exact.
"""


def hamming(x: str, y: str) -> int:
    """The number of positions in which two equal-length bit strings differ."""
    assert len(x) == len(y)
    return sum(1 for a, b in zip(x, y) if a != b)


def weight(bits: str) -> int:
    return bits.count("1")


def all_codewords_uncoded(n_bits: int) -> list[str]:
    return [format(i, f"0{n_bits}b") for i in range(2**n_bits)]


def min_distance(words: list[str]) -> int:
    best = len(words[0]) + 1
    for i, x in enumerate(words):
        for y in words[i + 1:]:
            best = min(best, hamming(x, y))
    return best


print("Hamming distance is just 'how many bits differ':")
pairs = [("0000", "0000"), ("0000", "1111"), ("1010", "1011"),
         ("1010", "0101"), ("11000", "00011")]
for x, y in pairs:
    print(f"   d({x}, {y}) = {hamming(x, y)}")
print()

print("Three codes, and the minimum distance of each:")
codes = {
    "no redundancy (4 bits)": all_codewords_uncoded(4),
    "even parity (5 bits)": [f"{i:05b}" for i in range(32)
                             if bin(i).count("1") % 2 == 0],
    "repetition 3x (12 bits)": ["".join(b * 3 for b in f"{i:04b}")
                                for i in range(16)],
}
for name, words in codes.items():
    d = min_distance(words)
    print(f"   {name:>24}: {len(words):>3} codewords, d = {d}, "
          f"detects {d - 1}, corrects {(d - 1) // 2}")
print()

print("Why: a single-bit error moves a codeword to a distance-1 neighbour,")
print("which is not a codeword, so it is detected.  A two-bit error moves it")
print("to distance 2, and if two codewords sit at distance 2 the receiver")
print("cannot tell a corrupted word from a different valid word, so d = 2")
print("detects one error and nothing more.  The even-parity code above has")
print("d = 2, exactly as the theory says.")
print()

# Correcting is harder than detecting, and the factor of two is forced.
print("Why correction only reaches floor((d-1)/2):")
print("   Suppose two codewords are d apart and t errors occur.  The received")
print("   word is then at distance t from one and at least d - t from the other.")
print("   To be sure which codeword was sent you need t < d - t, i.e. 2t < d.")
print("   So t <= floor((d - 1) / 2).  The balls of radius t around codewords")
print("   must be disjoint, and that is exactly the sphere-packing bound.")
print()

d = 2
print(f"   with d = {d}: detects {d - 1}, corrects {(d - 1) // 2}")
d = 3
print(f"   with d = {d}: detects {d - 1}, corrects {(d - 1) // 2}")
d = 5
print(f"   with d = {d}: detects {d - 1}, corrects {(d - 1) // 2}")
d = 7
print(f"   with d = {d}: detects {d - 1}, corrects {(d - 1) // 2}")
print()
print("Doubling the redundancy roughly doubles the correctable error count.")
print("This is the trade: for a length-n binary code, d and the rate cannot")
print("both be large.  The Hamming bound makes that precise:")
print()
print("   t = (d - 1) // 2,  so  2^n >= |C| * sum_{i=0}^{t} C(n, i)")
print()
print("   for n = 8 and d = 4 (t = 1):  |C| <= 256 / (1 + 8) = ", 256 // 9)
print("   for n = 8 and d = 5 (t = 2):  |C| <= 256 / (1 + 8 + 28) = ",
      256 // 37)
print("   for n = 7 and d = 3 (t = 1):  |C| <= 128 / (1 + 7) = ", 128 // 8)
print()
print("The Hamming(7,4) code reaches 16 codewords out of a bound of 16, so")
print("it is a perfect code: the spheres around its codewords tile the whole")
print("128-bit space exactly, with no gaps and no overlaps.")
```

### 3. Hamming(7,4) encode and decode

```python
"""Hamming(7,4): encode four bits, protect against one error, with the minimum
possible redundancy, and decode by computing a 3-bit syndrome.

The structure is: three parity bits sit at positions 1, 2 and 4.  Parity bit
at position 2^k covers the positions whose binary index has bit k set.  That
way, the *index* of a flipped bit, read in binary, is exactly the set of parity
checks that fail -- so the failed checks identify the bad bit directly.
"""

# Parity positions are 1, 2, 4 (1-based); data occupies 3, 5, 6, 7.
DATA_POSITIONS = [3, 5, 6, 7]           # 1-based
PARITY_POSITIONS = [1, 2, 4]            # 1-based


def hamming74_encode(data: str) -> str:
    """Return the 7-bit codeword for the 4-bit string `data`.

    Each parity bit is the XOR of the data bits it covers, so the codeword is
    a linear function of the data:  codeword = data * G over GF(2).
    """
    assert len(data) == 4 and set(data) <= {"0", "1"}
    bits = ["0"] * 7
    for pos, b in zip(DATA_POSITIONS, data):
        bits[pos - 1] = b
    for k, p in enumerate(PARITY_POSITIONS):
        # parity position p covers every position whose index has bit k set,
        # excluding p itself (p has only that one bit set)
        covered = [i for i in range(1, 8)
                   if i != p and (i >> k) & 1]
        bits[p - 1] = str(sum(int(bits[j - 1]) for j in covered) % 2)
    return "".join(bits)


def syndrome(codeword: str) -> int:
    """Which parity checks fail, read as a binary index of the bad bit.

    Check k fails exactly when the codeword has odd parity over the positions
    whose index has bit k set.  If bit i (1-based) flipped, check k failed iff
    bit k of i is 1 -- so the three check results *are* the index.
    """
    s = 0
    for k in range(3):
        covered = [i for i in range(1, 8) if (i >> k) & 1]
        if sum(int(codeword[i - 1]) for i in covered) % 2 == 1:
            s |= 1 << k
    return s


def hamming74_decode(received: str) -> tuple[str, int]:
    """Correct at most one error, then return (data, number of errors fixed)."""
    s = syndrome(received)
    if s == 0:
        return "".join(received[i - 1] for i in DATA_POSITIONS), 0
    fixed = list(received)
    fixed[s - 1] = "1" if fixed[s - 1] == "0" else "0"
    corrected = "".join(fixed)
    return "".join(corrected[i - 1] for i in DATA_POSITIONS), 1


def flip(word: str, pos_1based: int) -> str:
    chars = list(word)
    chars[pos_1based - 1] = "1" if chars[pos_1based - 1] == "0" else "0"
    return "".join(chars)


print("all 16 messages, encoded:")
for i in range(16):
    data = format(i, "04b")
    code = hamming74_encode(data)
    print(f"   {data} -> {code}   weight {code.count('1')}   "
          f"syndrome {syndrome(code)}")
print()

print("The 16 codewords:")
codewords = [hamming74_encode(format(i, "04b")) for i in range(16)]
print("   " + "  ".join(codewords))
print()


def d(x, y):
    return sum(1 for a, b in zip(x, y) if a != b)


smallest = min(d(a, b) for k, a in enumerate(codewords) for b in codewords[k + 1:])
print(f"minimum distance = {smallest}, so this code detects {smallest - 1} errors")
print(f"and corrects {(smallest - 1) // 2}.")
weights = sorted({int(c, 2).bit_count() for c in codewords})
print(f"the weights that occur are {weights}.  Note the code is NOT even-weight:")
print("   each of the three parity GROUPS has even parity, but the groups")
print("   overlap, so their sum is not the total number of 1s.")
print()

print("Now corrupt each codeword in each of its 7 positions and decode:")
data = "1011"
code = hamming74_encode(data)
print(f"   sent data {data} as codeword {code}")
print(f"   {'flipped pos':>12} {'received':>10} {'syndrome':>10} {'decoded':>8} "
      f"{'fixed':>6}")
ok = True
for pos in range(1, 8):
    received = flip(code, pos)
    s = syndrome(received)
    got, fixed = hamming74_decode(received)
    ok &= (got == data and s == pos)
    print(f"   {pos:>12} {received:>10} {s:>10} {got:>8} {fixed:>6}")
print(f"   every single-bit error corrected: {ok}")
print("   The syndrome column equals the flipped position, which is the whole")
print("   point: 3 parity bits identify 7 possible error locations.")
print()

print("Two errors are worse than useless -- the decoder 'corrects' the wrong bit:")
data = "1011"
code = hamming74_encode(data)
bad = flip(flip(code, 3), 5)
got, fixed = hamming74_decode(bad)
print(f"   {code} with positions 3 and 5 flipped -> {bad}")
print(f"   syndrome {syndrome(bad)} points at position {syndrome(bad)}")
print(f"   decoded as {got}, which is wrong, and the decoder had no way to know.")
print("   This is why d = 3 detects 2 errors but corrects only 1.")
print()

# Three errors land back on a valid codeword and are undetectable.
three = flip(flip(flip(code, 3), 5), 6)
print(f"   with three flips (3, 5, 6) -> {three}, syndrome {syndrome(three)}")
print("   The syndrome is 0, so the decoder thinks the word is perfect, and it")
print("   decodes to the wrong data.  Nothing can fix that with d = 3.")
print()

print("The generator matrix, which is the whole encoder in matrix form.")
print("Row i is the codeword for data 1000, 0100, 0010, 0001:")
G = [hamming74_encode("1000"), hamming74_encode("0100"),
     hamming74_encode("0010"), hamming74_encode("0001")]
print("   G = " + "\n       ".join(" ".join(r) for r in G))
print()
print("Check: data * G over GF(2) is a bitwise XOR of the rows 1 bits select.")
for i in range(16):
    data = format(i, "04b")
    rows = [G[j] for j in range(4) if data[j] == "1"]
    word = [str(sum(int(r[b]) for r in rows) % 2) for b in range(7)]
    assert "".join(word) == hamming74_encode(data)
print("   for all 16 messages, row XOR equals the encoder above")
print()

print("The parity-check matrix H is 3x7, and a codeword is exactly a vector")
print("with H * c = 0.  Its rows are the three parity checks:")
checks = []
for k in range(3):
    row = ["1" if (i >> k) & 1 else "0" for i in range(1, 8)]
    checks.append("".join(row))
print("   H = " + "\n       ".join(" ".join(r) for r in checks))
print()
print("   The syndrome is H * c computed mod 2, which is the same number the")
print("   decoder derives from the parity checks directly:")
for pos in range(1, 8):
    bad = flip(code, pos)
    prod = [sum(int(checks[r][j]) * int(bad[j]) for j in range(7)) % 2
            for r in range(3)]
    value = prod[0] + 2 * prod[1] + 4 * prod[2]
    print(f"   H * (codeword with bit {pos} flipped) = "
          f"{''.join(map(str, prod))} = {value}, and the position is {pos}")
print()
print("   That is the whole algorithm: multiply by H, read the 3-bit result as")
print("   an index, flip that bit if the index is nonzero.")
```

### 4. Extended Hamming(8,4): detect what you cannot correct

```python
"""Extended Hamming(8,4): add one more parity bit so two errors are detected
as well as corrected, and run both codes over a real noisy channel.

An even parity bit over the whole 7-bit codeword changes the meaning of the
syndrome from "0 means clean" to "a table lookup".  With the extra bit, the
syndrome can distinguish one error from two, so the decoder corrects one and
reports two.
"""

DATA_POSITIONS = [3, 5, 6, 7]
PARITY_POSITIONS = [1, 2, 4]


def hamming74_encode(data: str) -> str:
    bits = ["0"] * 7
    for pos, b in zip(DATA_POSITIONS, data):
        bits[pos - 1] = b
    for k, p in enumerate(PARITY_POSITIONS):
        covered = [i for i in range(1, 8) if i != p and (i >> k) & 1]
        bits[p - 1] = str(sum(int(bits[j - 1]) for j in covered) % 2)
    return "".join(bits)


def hamming84_encode(data: str) -> str:
    """The (8,4) code: Hamming(7,4) plus an overall even parity bit at pos 8."""
    cw = hamming74_encode(data)
    overall = str(cw.count("1") % 2)      # 0 when the 7-bit word has even parity
    return cw + overall


def hamming84_decode(received: str) -> tuple[str, str]:
    """Return (data, verdict) where verdict is 'ok', 'corrected 1' or '2 errors'."""
    overall_bad = received.count("1") % 2
    s = 0
    for k in range(3):
        covered = [i for i in range(1, 8) if (i >> k) & 1]
        if sum(int(received[i - 1]) for i in covered) % 2 == 1:
            s |= 1 << k

    if overall_bad == 0:
        # even number of errors.  With d = 4 at most 3 errors are possible, so
        # syndrome 0 means exactly two.
        return extract(received), "2 errors" if s else "ok"
    # odd number of errors: exactly one, so s names the bit.
    fixed = list(received)
    fixed[s - 1] = "1" if fixed[s - 1] == "0" else "0"
    return extract("".join(fixed)), "corrected 1"


def extract(word: str) -> str:
    return "".join(word[i - 1] for i in DATA_POSITIONS)


def syndrome74(word: str) -> int:
    s = 0
    for k in range(3):
        covered = [i for i in range(1, 8) if (i >> k) & 1]
        if sum(int(word[i - 1]) for i in covered) % 2 == 1:
            s |= 1 << k
    return s


def flip(word: str, pos: int) -> str:
    chars = list(word)
    chars[pos - 1] = "1" if chars[pos - 1] == "0" else "0"
    return "".join(chars)


def syndrome84(word: str) -> int:
    return syndrome74(word[:7])


print("(8,4) codes, one for each message:")
for i in range(16):
    data = format(i, "04b")
    print(f"   {data} -> {hamming84_encode(data)}")
print()

print("Now the key property: one error is corrected, two are DETECTED")
print(f"{'errors':>7} {'codeword':>10} {'syndrome':>10} {'verdict':>13} "
      f"{'data':>6} {'right?':>7}")
data = "1011"
cw = hamming84_encode(data)
print(f"{0:>7} {cw:>10} {syndrome84(cw):>10} {hamming84_decode(cw)[1]:>13} "
      f"{hamming84_decode(cw)[0]:>6} {'yes':>7}")
for pos in (1, 3, 7, 8):
    bad = flip(cw, pos)
    got, verdict = hamming84_decode(bad)
    print(f"{1:>7} {bad:>10} {syndrome84(bad):>10} {verdict:>13} {got:>6} "
          f"{'yes' if got == data else 'NO':>7}")
for p1, p2 in ((1, 2), (3, 5), (7, 8), (2, 6)):
    bad = flip(flip(cw, p1), p2)
    got, verdict = hamming84_decode(bad)
    print(f"{2:>7} {bad:>10} {syndrome84(bad):>10} {verdict:>13} {got:>6} "
          f"{'yes' if got == data else 'NO':>7}")
print()
print("The (8,4) code still mis-corrects a two-bit error -- it reports '2")
print("errors' and the data it returns is garbage -- but it never reports")
print("success.  Detection without correction is what you want when the")
print("receiver can ask for a retransmission, which is what a TCP sender does.")
```

### 5. Reed-Solomon over GF(256)

```python
"""Reed-Solomon, worked over GF(256) the way QR codes and CDs use it.

The idea in one line: run the syndrome machinery of Hamming codes, but over a
field with 256 elements instead of 2, so one symbol carries 8 bits and NPARITY
parity symbols fix NPARITY/2 corrupted symbols.

GF(256) is NOT the integers mod 256 -- 256 is not prime, so there are zero
divisors.  It is the field of polynomials mod an irreducible polynomial;
x^8 + x^4 + x^3 + x^2 + 1 (0x11d) is the one QR codes chose.
"""
import random


class GF256:
    """Arithmetic on GF(2^8) using the irreducible polynomial 0x11d."""

    PRIMITIVE = 0x11D
    ORDER = 255

    def __init__(self):
        self.exp = [0] * 512
        self.log = [0] * 256
        x = 1
        for i in range(self.ORDER):
            self.exp[i] = x
            self.log[x] = i
            x <<= 1
            if x & 0x100:          # reduce mod x^8 + x^4 + x^3 + x^2 + 1
                x ^= self.PRIMITIVE
        for i in range(self.ORDER, 512):    # wrap so exp[i + j] always works
            self.exp[i] = self.exp[i - self.ORDER]

    def mul(self, a: int, b: int) -> int:
        if a == 0 or b == 0:
            return 0
        return self.exp[self.log[a] + self.log[b]]

    def div(self, a: int, b: int) -> int:
        assert b != 0
        return 0 if a == 0 else self.exp[(self.log[a] - self.log[b]) % self.ORDER]

    def inv(self, a: int) -> int:
        assert a != 0
        return self.exp[(self.ORDER - self.log[a]) % self.ORDER]

    def power(self, a: int, e: int) -> int:
        result, base = 1, a
        while e:
            if e & 1:
                result = self.mul(result, base)
            base = self.mul(base, base)
            e >>= 1
        return result

    # A codeword is stored highest power first, which is transmission order.
    def poly_eval(self, p, x: int) -> int:
        acc = 0                              # Horner's rule
        for c in p:
            acc = self.mul(acc, x) ^ c
        return acc

    def poly_rem(self, p, g):
        """Remainder of p divided by g.  Synthetic division works because the
        leading coefficient of g is 1, so no division is needed."""
        out = list(p)
        n = len(g)
        for i in range(len(out) - n + 1):
            if out[i]:
                coef = out[i]
                for j in range(n):
                    out[i + j] ^= self.mul(coef, g[j])
        return out[len(out) - n + 1:]

    # Berlekamp-Massey indexes coefficients by power, so it needs these.
    def poly_mul_pow(self, p, q):
        out = [0] * (len(p) + len(q) - 1)
        for i, a in enumerate(p):
            if a:
                for j, b in enumerate(q):
                    if b:
                        out[i + j] ^= self.mul(a, b)
        return out

    def poly_eval_pow(self, p, x: int) -> int:
        acc = 0
        for c in reversed(p):
            acc = self.mul(acc, x) ^ c
        return acc


F = GF256()
NPARITY = 4

print("GF(256) built with the QR code's irreducible polynomial 0x11d =")
print("   x^8 + x^4 + x^3 + x^2 + 1")
print(f"   3 * 7 = {F.mul(3, 7)},  7^-1 = {F.inv(7)},  7 * {F.inv(7)} = "
      f"{F.mul(7, F.inv(7))}")
print(f"   3^100 = {F.power(3, 100)},  (3^100)^255 = {F.power(F.power(3, 100), 255)}")
print("   every nonzero element has an inverse, because 0x11d is prime.")
print("   In Z/256Z we would have 16 * 16 = 0, so there would be no inverse.")
print()

# Build g(x) = (x - a^0)(x - a^1)...(x - a^(NPARITY-1)) in power order, then
# flip to transmission order (highest power first) exactly once.
_g = [1]
for i in range(NPARITY):
    _g = F.poly_mul_pow(_g, [F.exp[i], 1])     # multiply by (a^i + x)
GENERATOR = list(reversed(_g))

print("generator polynomial g(x) = (x-a^0)(x-a^1)(x-a^2)(x-a^3)")
print(f"   coefficients, highest power first: {GENERATOR}")
print(f"   roots among the powers of a: "
      f"{[i for i in range(255) if F.poly_eval(GENERATOR, F.exp[i]) == 0]}")
print()


def rs_encode(data):
    """Systematic Reed-Solomon: the data, then the remainder of the shifted
    message divided by g(x).  The result is divisible by g, so it evaluates
    to zero at a^0..a^3, so all four syndromes vanish."""
    return list(data) + F.poly_rem(list(data) + [0] * NPARITY, GENERATOR)


def rs_syndromes(block):
    return [F.poly_eval(block, F.exp[i]) for i in range(NPARITY)]


def berlekamp_massey(synd, nsym):
    """The error locator polynomial, indexed by power (Lambda[0] == 1).

    One pass: at step n compute the discrepancy d = S_n + sum C_i S_{n-i}.
    If d is zero, extend the shift.  Otherwise add a shifted copy of the last
    discrepancy polynomial, and if 2L <= n also raise L to n + 1 - L.
    """
    C, B = [1], [1]
    L, m, b = 0, 1, 1
    for n in range(nsym):
        d = synd[n]
        for i in range(1, L + 1):
            if i < len(C) and C[i]:
                d ^= F.mul(C[i], synd[n - i])
        if d == 0:
            m += 1
            continue
        coef = F.div(d, b)
        previous = list(C)
        shifted = [0] * m + [F.mul(coef, c) for c in B]
        if len(shifted) > len(C):
            C = C + [0] * (len(shifted) - len(C))
        for j, c in enumerate(shifted):
            C[j] ^= c
        if 2 * L <= n:
            L, B, b, m = n + 1 - L, previous, d, 1
        else:
            m += 1
    return C, L


def rs_decode(block):
    """Correct up to NPARITY//2 unknown symbol errors.

    Three steps, the standard Berlekamp-Massey algorithm:
      1. Berlekamp-Massey turns the syndromes into an error locator Lambda,
         whose degree is the number of errors;
      2. Chien search finds the roots of Lambda, which are the error positions;
      3. Forney's formula recovers the error value at each root.
    """
    synd = rs_syndromes(block)
    if not any(synd):
        return list(block), 0

    n = len(block)
    locator, L = berlekamp_massey(synd, NPARITY)
    if L == 0 or L > NPARITY // 2:
        return list(block), -1

    # Chien search.  Symbol p sits at power n-1-p, so its locator value is
    # X = a^(n-1-p) and Lambda's root is X^-1.
    positions = [p for p in range(n)
                 if F.poly_eval_pow(locator, F.exp[(F.ORDER - (n - 1 - p))
                                                  % F.ORDER]) == 0]
    if len(positions) != L:
        return list(block), -1

    # Omega(x) = S(x) * Lambda(x) mod x^nsym, then Forney:
    #     e_p = X_p * Omega(X_p^-1) / Lambda'(X_p^-1)
    omega = F.poly_mul_pow(synd, locator)[:NPARITY]
    # In characteristic 2 the formal derivative keeps only odd powers.
    derivative = [locator[i] if i % 2 == 1 else 0 for i in range(1, len(locator))]
    if not any(derivative):
        return list(block), -1

    fixed = list(block)
    for p in positions:
        X = F.exp[(n - 1 - p) % F.ORDER]
        xinv = F.inv(X)
        den = F.poly_eval_pow(derivative, xinv)
        if den == 0:
            return list(block), -1
        fixed[p] ^= F.mul(X, F.div(F.poly_eval_pow(omega, xinv), den))
    return fixed, len(positions)


DATA = [0x40, 0xD2, 0x75, 0x47, 0x76, 0x17, 0x32, 0x06, 0x27, 0x26, 0x96,
        0xC6]
encoded = rs_encode(DATA)
print(f"a {len(DATA)}-symbol message with {NPARITY} parity symbols, "
      f"which corrects {NPARITY // 2} errors:")
print(f"   data       = {' '.join(f'{b:02x}' for b in DATA)}")
print(f"   parity     = {' '.join(f'{b:02x}' for b in encoded[len(DATA):])}")
print(f"   codeword   = {' '.join(f'{b:02x}' for b in encoded)}")
print(f"   syndromes  = {rs_syndromes(encoded)}  (all zero: it is a codeword)")
print()

print("corrupt symbols and decode:")
for bad_positions in ([0], [7], [0, 5], [3, 11], [15]):
    corrupted = list(encoded)
    for p in bad_positions:
        corrupted[p] ^= 0x5A
    fixed, nerr = rs_decode(corrupted)
    print(f"   {len(bad_positions)} error(s) at {bad_positions}: syndromes "
          f"{' '.join(f'{s:02x}' for s in rs_syndromes(corrupted))}")
    print(f"      decoder reported {nerr} error(s); data recovered: "
          f"{fixed[:len(DATA)] == DATA}")
print()

random.seed(3)
for nerr in (NPARITY // 2 + 1, NPARITY // 2 + 2):
    corrupted = list(encoded)
    for p in random.sample(range(len(encoded)), nerr):
        corrupted[p] ^= 0x33
    fixed, nerr_found = rs_decode(corrupted)
    print(f"{nerr} errors: decoder reported {nerr_found} "
          f"({'gave up' if nerr_found < 0 else 'claimed success'}), "
          f"data correct: {fixed[:len(DATA)] == DATA}")
print("   With 4 parity symbols the code promises exactly 2 corrections, and")
print("   the decoder refuses to guess beyond that instead of returning")
print("   plausible garbage.")
print()

print("Reed-Solomon fixes symbols, not bits.  One corrupted symbol can mean 8")
print("wrong bits, which is exactly the CD case: a scratch there is thousands")
print("of bits long.  QR codes and CDs both interleave as well as code,")
print("spreading a burst across many short blocks so no block sees more than")
print("t errors.  Interleaving plus RS is what lets a 700 MB disc survive a")
print("2 cm scratch and a QR code survive a folded corner.")
print()
print("CDs use RS(28,24) inside CIRC; QR codes use RS over GF(256) with 10 to")
print("30 parity symbols depending on the error-correction level; deep-space")
print("probes use convolutional codes with interleaving.  All of them add just")
print("enough redundancy to fix the errors they expect, no more.")
```

## Common Mistakes

**Wrong.** Treating a parity bit as if it can correct.

```python
def encode(data):
    return data + str(sum(int(b) for b in data) % 2)


def decode_and_fix(block):
    if sum(int(b) for b in block) % 2 == 0:
        return block, "clean"
    # WRONG: there is no way to know WHICH bit is wrong
    return block, "cannot fix this"
```

**Right.**

```python
def encode(data):
    return data + str(sum(int(b) for b in data) % 2)


def decode_and_report(block):
    if sum(int(b) for b in block) % 2 == 0:
        return block, "clean"
    return block, "1 error somewhere, position unknown"
```

Why the wrong version is tempting: "detect" and "correct" sound like the same
job, and the parity bit does tell you *something* is wrong. But a distance-2
code can only distinguish "valid" from "not valid" — one bit of information,
whereas correction requires naming one of `n` positions. That is the whole
factor-of-two gap between `d − 1` and `⌊(d−1)/2⌋`.

---

**Wrong.** Trusting a Hamming(7,4) decoder to tell you the channel was clean.

```python
def decode(received):
    s = syndrome(received)
    if s:
        flip_bit(received, s - 1)
    return received            # WRONG: 3 errors give syndrome 0 too
```

**Right.**

```python
def decode(received):
    s = syndrome(received)
    if s == 0:
        return received, "no error detected"
    fixed = list(received)
    fixed[s - 1] ^= 1
    return "".join(fixed), "1 error corrected"
```

Why the wrong version is tempting: `d = 3` sounds reassuring, and every
single-error test passes. The failure is three flips: the syndrome is `0`, the
decoder reports "clean", and the data is wrong. Detection bounds are the ones
that describe what a `0` syndrome actually means, and Hamming(7,4) detects
exactly two errors — not three.

---

**Wrong.** Using an RS decoder that guesses when it cannot correct.

```python
def rs_decode(block):
    synd = rs_syndromes(block)
    if not any(synd):
        return list(block)
    # WRONG: it will "correct" some arbitrary bit and return garbage
    fixed = list(block)
    fixed[0] ^= synd[0]
    return fixed
```

**Right.**

```python
def rs_decode(block):
    synd = rs_syndromes(block)
    if not any(synd):
        return list(block), 0
    fixed, nerr = search_for_error_pattern(block, synd)
    if nerr < 0:
        raise ValueError("uncorrectable: too many symbol errors")
    return fixed, nerr
```

Why the wrong version is tempting: the syndromes are nonzero, so *something*
is definitely wrong, and the code "produces output". But beyond `t` errors the
syndrome pattern is consistent with many wrong corrections, and returning one
silently is worse than failing — the caller cannot distinguish a repaired
symbol from a corrupted one.

---

**Wrong.** Choosing `t` parity symbols and expecting `t` symbol corrections.

**Right.** `t` parity symbols correct `⌊t/2⌋` symbols and detect `t − 1`.

Why the wrong version is tempting: it matches the intuition that each parity
symbol "covers" one error. But the triangle-inequality argument is unavoidable:
with `t` parity symbols you have `t` syndrome values and need to distinguish
`1 + t` cases (no error, or one of `t` locations), and the same logic that
gives the factor of two for binary codes applies unchanged to symbols. QR code
level M has 10 parity bytes and corrects 5 symbols, not 10.

## Formula Sheet

Every formula, notation and definition this lesson uses. Symbols follow
[SYMBOLS.md](../SYMBOLS.md). Note that `m` is used twice with different meanings:
`m` is the *field degree* in `GF(2^m)` and the *data length* in `Hamming(n, m)`.
Read the subscript to tell them apart.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| **Hamming distance** `d(x, y)` | `$\#\{\, i : x_i \ne y_i \,\}$` | how many positions two equal-length bit strings differ in | comparing codewords, and a received word against a codeword. **Restriction: `x` and `y` must have equal length.** `d("11000", "00011") = 5` |
| **weight** `w(x)` | `$w(x) = d(x, 0)$` | the number of 1s | for a *linear* code, `d_min` is just the smallest nonzero weight — so you check `2^k − 1` combinations, not every pair |
| **minimum distance** `$d_{\min}$` | `$\min\{\, d(x,y) : x \ne y \in C \,\}$` | the closest pair of valid codewords | the one number that decides what a code can do. Hamming(7,4): `d = 3`. Even parity: `d = 2`. Repetition-3: `d = 3`. Extended Hamming(8,4): `d = 4` |
| detection bound | `$\text{detects} = d - 1$` | how many errors are *noticed* | an error of weight `e` moves `x` to distance `e`, and can only be another codeword if `d \le e` |
| **correction bound** | `$t = \lfloor (d-1)/2 \rfloor$` | how many errors are *repaired* | `d = 2` ⟹ `t = 0`; `d = 3` ⟹ `1`; `d = 4` ⟹ `1`; `d = 5` ⟹ `2`; `d = 7` ⟹ `3`. **Never `⌊d/2⌋` — the `−1` is what keeps the balls disjoint** |
| why correction is halved | after `e` errors the word is at distance `e` from the truth and at least `d-e` from any other codeword; certainty needs `e < d-e`, i.e. `2e < d` | the triangle inequality, with no exceptions | the entire derivation of `t`. Detection asks "is this one of mine?" (one bit answers it); correction asks "which one?" (a search) |
| repetition-3 | `$C = \{000, 111\}$`, `d = 3`; on `k` data bits the codeword is `3k` bits | each bit three times, majority vote | corrects 1 error, detects 2. **Restriction: 200% redundancy** — far worse than Hamming's 3/7 |
| even-parity code | `$C = \{x : w(x) \equiv 0 \pmod 2\}` | the number of 1s is even | `d_{\min} = 2` exactly: detects 1 error, corrects 0. **Restriction: never detects a two-bit error** — two flips change the 1-count by 0 or 2, both even. Two independent checks ⟹ `d = 4` ⟹ detects 3, corrects 1 |
| `GF(2)` arithmetic | `1 + 1 = 0`, `x + x = 0`; addition **is** XOR, so every `^` in the code is field addition | arithmetic on two values | Hamming codes. **Restriction: this is not arithmetic mod 2, and `GF(2)` is the only case where `−` and `+` coincide** |
| linearity | `$u, v \in C \Rightarrow u + v \in C$`, i.e. closed under XOR | the code is a subspace | `C` is the row space of some matrix `G`. This is what makes decoding a lookup rather than a search |
| `d_{\min}` of a linear code | `$\min\{\, w(c) : c \in C,\ c \ne 0 \,\}$` | the lightest nonzero codeword | Hamming(7,4)'s weights are exactly `{0, 3, 4, 7}`, so `d_{\min} = 3` |
| generator matrix `G` | `$c = m \cdot G$`, `G` is `$k \times n$` | multiply the message by the encoder | encode. Hamming(7,4)'s `G` is the four codewords for `1000`, `0100`, `0010`, `0001`, and `m·G` is the bitwise XOR of the rows `m` selects |
| parity-check matrix `H` | `H` is `$(n-k) \times n$`; `$c \in C \iff H \cdot c^{T} = 0$` | a matrix whose kernel *is* the code | decode. **Restriction: `H` is not invertible** — it has `n` columns and only `n-k` rows, and `C` is exactly the part of the kernel it cannot see |
| **syndrome** | `$s = H \cdot r^{T}$`; `$s = 0 \iff r$ is a codeword | three parity checks condensed into one 3-bit number | the receiver's entire diagnosis. `Hamming(7,4)`: three checks, so `s ∈ {0,…,7}` |
| syndrome depends only on the error | `$s = H\cdot(c+e)^{T} = H\cdot c^{T} + H\cdot e^{T} = H\cdot e^{T}$` | the codeword part cancels | the single most useful fact in the lesson: the receiver computes a function of the *error alone*, with no knowledge of the data |
| Hamming(7,4) layout | parity at positions 1, 2, 4; data at 3, 5, 6, 7; parity at `$2^k$` covers positions whose index has bit `k` set | the index of a bit, read in binary, is exactly which checks fail | `1011` ⟹ `0110011`. The 7-bit word is **not** even-weight (`1111111` has weight 7): the three parity *groups* overlap, so their sum is not the total |
| `H` for Hamming(7,4) | `H = [1 0 1 0 1 0 1; 0 1 1 0 0 1 1; 0 0 0 1 1 1 1]`, column `i` = binary expansion of `i` | each column names one position | multiply, read the 3-bit result as an index |
| **syndrome = position** | single error at bit `i` ⟹ `$s = i$` | the syndrome *is* the address | flip and recover. **Restriction: single error only.** Two errors give `s = i \oplus j`, naming a position where nothing is wrong (`0110011` with 3 and 5 flipped ⟹ `s = 6` ⟹ data `0101`) |
| Hamming family | `$\mathrm{Hamming}(2^{r}-1,\; 2^{r}-1-r)$` | `r` parity bits can name `2^r - 1` positions | `r = 3` ⟹ (7,4); `r = 4` ⟹ (15,11); `r = 5` ⟹ (31,26). Three is minimal: two parity bits name only 4 positions, so a 3-bit code could protect 3 — worse than parity |
| extended Hamming(8,4), SECDED | `d = 4`: corrects 1, **detects** 2 | one overall parity bit makes the error count's parity visible | x86 ECC memory. **Restriction: it still returns wrong data on a two-bit error — it just never reports success.** `01100110` with 3 and 5 flipped ⟹ verdict `2 errors`, data `0111` |
| rate and redundancy | `$R = k/n$`; redundancy `$(n-k)/n = r/n$` | how much of the word is payload | Hamming(7,4): `R = 4/7`, redundancy `3/7 ≈ 0.4286`; Hamming(15,11): `4/15 ≈ 0.2667`; Hamming(31,26): `5/31 ≈ 0.1613`. **Restriction: `d` and `R` cannot both be large** — that is what the Hamming bound says |
| **Hamming bound** (sphere packing) | `$2^{n} \ge \|C\| \cdot \sum_{i=0}^{t} \binom{n}{i}$` | the radius-`t` balls around the codewords must be disjoint inside `2^n` words | `n = 7`, `d = 3`, `t = 1`: `128/(1+7) = 16`, and Hamming(7,4) has exactly 16 codewords. `n = 8`, `d = 4`: `256/9 = 28`; `n = 8`, `d = 5`: `256/37 = 6` |
| general Hamming bound | `$q^{n} \ge \|C\| \cdot V(n,t)$` with `$V(n,t) = \sum_{i=0}^{t} \binom{n}{i}(q-1)^{i}$` | the same counting over a `q`-ary alphabet | the Reed–Solomon case, where `q = 256` |
| **perfect code** | equality in the Hamming bound | the balls *tile* the space: no gaps, no overlaps | Hamming(7,4), Hamming(15,11), Hamming(31,26) and repetition-3 are perfect. **Restriction: over the binary alphabet these are the only perfect codes that exist.** The (8,4) extension has `\|C\| = 16 < 28`, so it is *not* perfect |
| Singleton bound | `$\|C\| \le q^{\,n-d+1}$` | project onto any `n-d+1` coordinates and the projection is injective | a cruder structural bound; for Hamming(7,4) it gives `2^5 = 32` against the Hamming bound's tighter `16` |
| `GF(2^m)` | polynomials of degree `< m` over `GF(2)`, modulo an irreducible of degree `m`; `GF(256) = GF(2^8)` mod `0x11d = x^8+x^4+x^3+x^2+1` | a field with `2^m` elements | Reed–Solomon. **Restriction: this is *not* arithmetic modulo 256** — in `ℤ/256ℤ` we have `16·16 ≡ 0`, so `16` has no inverse and the syndrome decoder's division would break |
| **symbol** | one element of `GF(2^m)`, carrying `m` bits | the unit RS repairs | one corrupted symbol can be 8 wrong bits, which is why RS matches *burst* errors (a CD scratch) and binary Hamming codes match isolated flips (ECC memory) |
| RS generator polynomial | `$g(x) = \prod_{i=0}^{t-1}(x - \alpha^{i})$`, roots `$\alpha^{0}\dots\alpha^{t-1}$` | a polynomial with `t` known roots | `NPARITY = 4` ⟹ `g = [1, 15, 54, 120, 64]`, roots exactly `α^0, α^1, α^2, α^3` |
| systematic RS encoding | `$c(x) = m(x)x^{t} + \big(m(x)x^{t} \bmod g(x)\big)$` | the data, then the remainder of dividing the shifted message by `g` | encode; the data is readable without decoding. The codeword is divisible by `g`, so it vanishes at every `α^i` |
| RS syndromes | `$S_j = c(\alpha^{j}) = \sum_i e_i \alpha^{ji}$`; all zero for a clean word | evaluate the received polynomial at `t` field elements | depend only on the error pattern. The lesson's 12-symbol message with `NPARITY = 4` has parity `1e d4 af c1` and syndromes `[0,0,0,0]` |
| one-symbol RS decode | `$e = S_0` and `$i = \log_{\alpha}(S_1/S_0)$` | the ratios of syndromes reveal the position | verify against `S_2, S_3`. Production decoders use Berlekamp–Massey plus Chien search; the lesson's search decoder gives identical answers |
| RS power | `t` parity symbols correct `⌊t/2⌋` **symbols** and detect `t-1` | the same factor of two as binary codes | **Restriction: not `t`.** QR level M has 10 parity bytes ⟹ 5 corrections and 9 detections. QR levels carry 10 to 30 parity symbols and recover 7% (L) to 30% (H) |
| interleaving | a run of `b` consecutive errors becomes about `⌈b / words⌉` errors in each codeword | spread a burst across many short codewords | converts a *fatal* burst into independent correctable errors. The lesson's 12-symbol burst over 6 words becomes 2 per word, exactly the capacity — without interleaving the same burst puts 10 errors in one word |

---

## Multiple Choice Questions

**Q1.** A code has minimum distance `d = 4`. How many errors can it detect, and how
many can it correct?

- A) Detects 4, corrects 2
- B) Detects 3, corrects 1
- C) Detects 3, corrects 2
- D) Detects 2, corrects 2

<details>
<summary>Answer and explanation</summary>

**B) Detects 3, corrects 1.**

Detection is `d − 1 = 3`. Correction is `⌊(d−1)/2⌋ = ⌊1.5⌋ = 1`. The lesson's
worked example of exactly this code is the extended Hamming(8,4) SECDED code used
by x86 ECC memory: it repairs one error and *notices* two.

Option A is the two standard slips at once. Detection is `d − 1`, not `d`; and
correction is `⌊(d−1)/2⌋ = ⌊1.5⌋`, which is 1 — rounding `1.5` up to 2 is exactly
the step that breaks the Hamming bound, because it puts two radius-2 balls where
only radius-1 balls are disjoint.

Option C rounds `1.5` up. This is the most consequential arithmetic mistake in the
subject, because it *looks* like the answer. The floor is not conservatism: for
`d = 4` a received word at distance 2 from two different codewords is consistent
with either, and flipping bit 6 of `0100111` returns `0101` from the true data
`1011`.

Option D applies the correction formula `⌊(d−1)/2⌋ = 1` to the wrong quantity,
substituting 2 for the detection count. `⌊d/2⌋ = 2` is a real expression, but it
is not the bound; the `−1` inside the floor is what guarantees disjointness.

</details>

**Q2.** `0110011` is the Hamming(7,4) codeword for `1011`. Bit 5 is flipped in
transit. What syndrome does the receiver compute, and what does it do?

- A) Syndrome 0, so it reports the word clean
- B) Syndrome 3, so it flips bit 3
- C) Syndrome 5, so it flips bit 5 and recovers the data `1011`
- D) Syndrome 2, so it flips bit 2

<details>
<summary>Answer and explanation</summary>

**C) Syndrome 5, so it flips bit 5 and recovers the data `1011`.**

The key property is that column `i` of `H` is the binary expansion of `i`, so a
single-bit error at position `i` produces a syndrome *numerically equal* to `i`.
The lesson's worked example checks all three parity groups by hand: positions 1, 3,
5, 7 hold `0+1+1+1 = 3`, odd; positions 4, 5, 6, 7 hold `0+1+1+1 = 3`, odd;
positions 2, 3, 6, 7 hold `1+1+1+1 = 4`, even. Checks 1 and 4 fail, and read with
check 1 as the low bit that is `1 + 0 + 4 = 5`.

Option A is what a *two*-error or *no*-error case looks like, not a single flip.
Syndrome 0 means "this is one of my own codewords", and a single error can never
produce it with `d = 3` — the corrupted word would be at distance 1 from a
codeword, and no two codewords are that close.

Option B is the syndrome for a *pair* of errors. Two flips at positions `i` and `j`
give `s = i ⊕ j`; positions 1 and 2 flipped give `1 ⊕ 2 = 3`. Reading 3 as an index
and flipping bit 3 is exactly the failure the lesson's Step 8 demonstrates, where
two flips at 3 and 5 give `s = 6` and the decoder confidently returns `0101` instead
of `1011`.

Option D mixes up which check number maps to which weight. The syndrome is read
with check `k` as bit `k`, so a value of 2 means "check 2 failed, checks 1 and 4
passed", i.e. the error is at position 2 — but that is a different received word
(`0010011`).

</details>

**Q3.** `0110011` has its bits 3, 5 and 6 flipped, arriving as `0100101`. What does
a Hamming(7,4) decoder report?

- A) Syndrome 6, so it corrects bit 6 and returns wrong data
- B) Syndrome 0, so it reports no error detected and returns the wrong data `0101`
- C) Syndrome 3, so it corrects bit 3 and returns wrong data
- D) Syndrome 7, so it reports the word uncorrectable

<details>
<summary>Answer and explanation</summary>

**B) Syndrome 0, so it reports no error detected and returns the wrong data
`0101`.**

With three errors, `s = 3 ⊕ 5 ⊕ 6 = 0`, and the syndrome of the received word is 0
— which is the definition of "this is a codeword". The lesson's code prints
exactly this: `with three flips (3, 5, 6) -> 0100101, syndrome 0`, and then "The
syndrome is 0, so the decoder thinks the word is perfect, and it decodes to the
wrong data. Nothing can fix that with `d = 3`."

Option A is the *two*-error behaviour, reused here. `6` is `3 ⊕ 5`, so syndrome 6
is what two flips at 3 and 5 give. With a third flip the third column enters the
sum and the answer cancels to 0.

Option C is again `i ⊕ j` from a two-error pattern. The whole point of `s = i ⊕ j`
is that XOR is not injective on pairs, which is precisely why `d = 3` corrects one
error and not two.

Option D reads a nonzero syndrome as a failure code. The decoder has no "give up"
state in Hamming(7,4) — a nonzero syndrome *is* an instruction to flip a bit. This
is exactly the mistake the lesson's second `Common Mistakes` entry warns about:
trusting a `0` syndrome as a clean bill of health.

</details>

**Q4.** Why does the syndrome `s = H·rᵀ` let a decoder work without ever knowing the
message?

- A) Because `H` is invertible, so `r` can be recovered from `s` alone
- B) Because `H·cᵀ = 0` for every codeword, so `s = H·(c+e)ᵀ = H·eᵀ` — a function
  of the error alone
- C) Because the parity bits are part of the codeword, so the receiver can subtract
  them off to get back the data
- D) Because `H` has `n − k` rows and `s` therefore pins down the `k` data bits
  directly

<details>
<summary>Answer and explanation</summary>

**B) Because `H·cᵀ = 0` for every codeword, so `s = H·(c+e)ᵀ = H·eᵀ` — a function
of the error alone.**

Write the received word as `r = c + e` with `c` a codeword. Then
`s = H·cᵀ + H·eᵀ = 0 + H·eᵀ`. The message term vanishes identically, so the receiver
computes a small function of the corruption alone with no knowledge of the data.
Exercise 3 verifies it numerically: for each of the 7 single-bit error patterns,
the syndrome is the *same* across all 16 codewords. The lesson calls it "the
single most useful fact in the subject."

Option A is flatly impossible. `H` is `(n−k) × n` with `n > n−k`, so it has a
kernel of dimension at least `k`; it cannot be invertible. Indeed the kernel
*contains* the entire code, which is the point of option B.

Option C describes the *mechanism* but mistakes it for the *reason*. In
Hamming(7,4) the parity bits really are transmitted, and recomputing them does
reproduce the failing checks — but that works only because of the structure of
`H`'s columns. It breaks the moment the error lands in a data bit: there is no
stored copy of the parity bits to subtract, and the check still works, precisely
because of the cancellation in B. Linear codes need no transmitted redundancy
beyond the codeword itself.

Option D confuses the syndrome's role. `s` names *where the error is*, not what the
data is. All the `s = 0` cases yield different data and all give `s = 0`; the
decoder keeps the received word as-is rather than reconstructing anything from the
syndrome.

</details>

**Q5.** Even parity adds one bit to a 4-bit block. Two bits of the 5-bit block flip
in transit. What does the receiver see, and what can it do about it?

- A) The parity check fails, so the error is detected but uncorrectable
- B) The parity check passes, so the error goes undetected; and even a *failing*
  check could not say which bit is wrong, since `d = 2` names no position
- C) The parity check passes, and the receiver can still correct, because two
  flipped bits move the word to a different but still valid codeword
- D) The parity check fails, and the receiver corrects, because the parity bit
  itself must be the damaged one

<details>
<summary>Answer and explanation</summary>

**B) The parity check passes, so the error goes undetected; and even a *failing*
check could not say which bit is wrong, since `d = 2` names no position.**

Two flips change the count of 1s by 0 or by 2 — both even — so the parity of the
block is unchanged. The lesson's code confirms it over 4000 trials: "parity catches
every single-bit error and never a two-bit error." The even-parity code has
`d_min = 2`, detects exactly 1 and corrects 0, and this is what its `Common
Mistakes` entry means by "there is no way to know WHICH bit flipped": detection
answers "is this one of mine?" with one bit of information, while correction has
to name one of `n` positions.

Option A is the single-flip case. One flip changes the 1-count by 1, the parity
fails, and the receiver reports a problem — but still cannot repair anything,
because `d = 2` gives `t = 0`.

Option C contains the deep truth and draws the wrong conclusion. Two flips really
can move a codeword to distance 2 from another codeword, which is why two-bit
errors are undetectable — but "moved to a different codeword" means the receiver
cannot tell which one it holds, not that it can choose correctly. Correction
requires the radius-`t` balls to be disjoint, and with `d = 2` the bound is
`⌊(2−1)/2⌋ = 0`, so there is nothing to correct with at all.

Option D confuses a check with a stored copy. The parity bit is recomputed over the
group it covers; it is not metadata that survives corruption, and a failing check
says only that the group has odd parity.

</details>

**Q6.** Hamming(7,4) has `n = 7`, `d = 3`, so `t = 1`. The Hamming bound gives
`|C| ≤ 2^7 / Σ_{i=0}^{1} C(7,i)`. What is the bound, and how does Hamming(7,4)
relate to it?

- A) `|C| ≤ 16`, and Hamming(7,4) has exactly 16 codewords — a perfect code, with
  the radius-1 balls tiling all 128 words
- B) `|C| ≤ 16`, and Hamming(7,4) has 16 codewords, so the radius-1 balls must
  overlap somewhere
- C) `|C| ≤ 32`, and Hamming(7,4) has 16 codewords, so it leaves the space half empty
- D) `|C| ≤ 128`, and Hamming(7,4) has 16 codewords, so the bound is vacuous at
  these parameters

<details>
<summary>Answer and explanation</summary>

**A) `|C| ≤ 16`, and Hamming(7,4) has exactly 16 codewords — a perfect code, with
the radius-1 balls tiling all 128 words.**

`Σ_{i=0}^{1} C(7,i) = 1 + 7 = 8`, and `128/8 = 16`. Hamming(7,4) has `2^4 = 16`
codewords, so it achieves the bound exactly. `16 × 8 = 128` — every one of the 128
possible received words is exactly one error away from exactly one codeword. The
lesson's Challenge solution states the consequence: "over the binary alphabet the
only perfect codes are the trivial ones, repetition-3, and
Hamming(2^r − 1, 2^r − r − 1), and it has been proven that no others exist. That is
why every ECC controller ever made is a Hamming code."

Option B contradicts itself: disjointness is exactly what *perfect* means. If the
balls overlapped, the bound would be violated. Equality is not slack — it is a
tiling of a finite space with no gaps and no overlaps, and the lesson notes such
tilings are extremely constrained.

Option C is the bound computed with the wrong ball. Getting `|C| ≤ 32` from `128`
would need a 4-word sphere, i.e. `1 + 3`, but `C(7,1) = 7` and the radius-1 ball is
8 words. Halving the `C(7,1)` term is easy to do by accident, and it makes the
code look better than it is.

Option D is the bound for `t = 0`, i.e. for a code that detects nothing and corrects
nothing — the `i = 0` term alone, `1`. Forgetting to include the `t` corrections in
the ball is the single most common error when applying the bound by hand.

</details>

**Q7.** A QR code uses Reed–Solomon over `GF(256)` with 10 parity symbols at
error-correction level M. What does the code actually guarantee?

- A) 10 symbol corrections
- B) 5 symbol corrections, and detection of up to 9 symbol errors
- C) 5 symbol corrections, and detection of up to 4 symbol errors
- D) 9 symbol detections and 10 symbol corrections, in that order

<details>
<summary>Answer and explanation</summary>

**B) 5 symbol corrections, and detection of up to 9 symbol errors.**

`t` parity symbols correct `⌊t/2⌋` symbols and detect `t − 1`, exactly as binary
codes do — the factor of two comes from the triangle inequality and is not affected
by the alphabet size. `⌊10/2⌋ = 5` and `10 − 1 = 9`. The lesson states this as its
fourth `Common Mistakes` entry: "QR code level M has 10 parity bytes and corrects 5
symbols, not 10."

Option A is the misconception the lesson singles out by name: "it matches the
intuition that each parity symbol 'covers' one error." The intuition is wrong
because `t` syndrome values must distinguish `1 + t` cases — no error, or one of
`t` locations — which needs about `log₂ t` bits, not `t`.

Option C mixes the two formulas. `⌊t/2⌋ − 1 = 4` applies the *binary* correction
count and then subtracts one for detection. Detection uses `d − 1` with the *full*
distance; a symbol code with `t` parity symbols has distance `t + 1`, so detection
is `t`.

Option D swaps the two roles. The lesson's `Common Mistakes` list is instructive
here: "Using an RS decoder that guesses when it cannot correct" is listed as a real
error, and the code prints "the decoder refuses to guess beyond that instead of
returning plausible garbage". Reporting more errors than you can repair is the
opposite of what a decoder should do.

</details>

**Q8.** Why does Reed–Solomon work over `GF(2^8)` rather than over arithmetic
modulo 256?

- A) Because modular arithmetic mod 256 is slower in software
- B) Because mod 256 has zero divisors — `16 · 16 ≡ 0` — so nonzero values have no
  inverse and the syndrome decoder's division breaks
- C) Because `GF(256)` can hold byte values larger than 255
- D) Because `ℤ/256ℤ` is not closed under the XOR that the binary structure needs

<details>
<summary>Answer and explanation</summary>

**B) Because mod 256 has zero divisors — `16 · 16 ≡ 0` — so nonzero values have no
inverse and the syndrome decoder's division breaks.**

The lesson's code says it outright: "every nonzero element has an inverse, because
0x11d is prime. In `Z/256Z` we would have `16 * 16 = 0`, so there would be no
inverse." The syndrome decoder computes `i = log(S_1/S_0)` and Forney's formula
divides by a locator derivative; division by zero is a real outcome, not a
rounding concern. `256` is not prime, so `ℤ/256ℤ` is a ring with zero divisors, not a
field — the same distinction [Lesson 111](111_modular_arithmetic_and_crypto.md)
draws for `ℤ_m`.

Option A is not a reason, and not one the lesson offers. Both representations are
implemented with the same log/exp table lookups; the choice is algebraic, not about
the clock.

Option C is simply false. Both structures have 256 elements and range over
`0..255`. `GF(256)` stores bytes in exactly the same 8 bits; only the *arithmetic*
differs.

Option D is a real confusion, because `ℤ/256ℤ` *is* closed under XOR — that is
genuinely true. But closure under XOR is not the problem. The problem is that
division is not possible, and division is what syndrome decoding does.

</details>

**Q9.** `01100110` is the extended Hamming(8,4) codeword for `1011`. Two of its
bits flip, at positions 3 and 5. What does the lesson's decoder report, and what
does it return?

- A) Syndrome 6, verdict `2 errors`, and it returns the correct data `1011`
- B) Syndrome 0, verdict `ok`, and it returns the correct data `1011`
- C) Syndrome 6, verdict `2 errors`, and the data it returns is wrong
- D) Syndrome 3, verdict `corrected 1`, and it returns the correct data `1011`

<details>
<summary>Answer and explanation</summary>

**C) Syndrome 6, verdict `2 errors`, and the data it returns is wrong.**

The lesson's decoder prints this row: errors `2`, received `01001110`, syndrome `6`,
verdict `2 errors`, data `0111`, right? `NO`. The overall parity bit is intact (two
flips preserve parity), so `overall_bad = 0`, and the three positional checks
disagree — syndrome `3 ⊕ 5 = 6` — which the decoder interprets as "an even number
of errors, and they are not zero", i.e. exactly two. With `d = 4`, three is the most
errors possible, so even-and-nonzero can only be two.

What SECDED buys is *honesty*, not repair. The lesson says it: "The (8,4) code
still mis-corrects a two-bit error — it reports '2 errors' and the data it returns is
garbage — but it never reports success." That is the property a receiver needs
when it can ask for a retransmission, which is what a TCP sender does.

Option A gets the verdict right and then assumes repair follows. Correction is
`⌊(d−1)/2⌋ = 1` for `d = 4`; with two errors the word is at distance 2 from two
different codewords and there is no way to choose. Detection was extended; it was
not correction.

Option B is the failure the fourth parity bit exists to prevent. Two flips leave
the overall parity even, so parity alone says "ok" — and the payload has silently
changed from `1011` to `0111`. That is the undetectable corruption SECDED rules
out.

Option D confuses `6` with a different two-error pattern: `6` is `3 ⊕ 5`, while `3`
is `1 ⊕ 2`. And `corrected 1` is the verdict for an *odd* error count — the
overall parity bit came out even, which is precisely what rules a single error out.

</details>

**Q10.** A CD interleaves as well as Reed–Solomon encodes. What exactly does
interleaving change about a burst of 12 consecutive corrupted symbols?

- A) The encoder, the decoder and the amount of redundancy stay identical; only the
  order of symbols on the wire changes, so the burst arrives as 2 errors in each of
  6 codewords instead of 10 in one
- B) It adds one extra parity symbol per codeword, raising the per-word correction
  capacity from 2 to 3
- C) It converts the burst into 12 independent single-bit errors, which a binary
  Hamming code can then repair
- D) It detects the burst instead of correcting it, and triggers a retransmission

<details>
<summary>Answer and explanation</summary>

**A) The encoder, the decoder and the amount of redundancy stay identical; only the
order of symbols on the wire changes, so the burst arrives as 2 errors in each of 6
codewords instead of 10 in one.**

The lesson's Exercise 4 measures exactly this. Without interleaving, a
12-consecutive-symbol burst lands inside one 10-symbol codeword and puts 10 errors
into a word that can correct 2 — the message is lost. With interleaving, the
transmitter emits one symbol from each codeword in turn, so the *same* 12
consecutive channel errors arrive as exactly 2 errors in each of the 6 words, and
every word is recoverable. The lesson's summary of the result: "The encoder, the
decoder, and the amount of redundancy are identical — only the ordering on the wire
changed."

Option B is the "just add more parity" reflex, which costs bandwidth and still
fails. Even doubling the parity symbols would only raise the capacity to 4, still
short of 10. Interleaving is free, which is why it is universal.

Option C changes the error model. Nothing converts symbol errors into bit errors;
the code is still Reed–Solomon over `GF(256)`, and 12 errors spread over 6 words is
still 12 errors. Concentrated bursts are exactly the case binary Hamming codes
handle badly, which is why the lesson pairs RS with interleaving for CDs and saves
Hamming for isolated flips in ECC memory.

Option D misreads what interleaving is for. Nothing is detected and no
retransmission is requested — a CD has no back channel at all. The lesson's QR
example makes the correction side clear: QR levels carry 10 to 30 parity symbols
and recover 7% (level L) to 30% (level H) of codewords, which is a repair rate, not
a retry protocol.

</details>

**Q11.** In Hamming(7,4), the data `1000` is placed at positions 3, 5, 6, 7. What
is the resulting codeword, and what is its weight?

- A) `1110000`, weight 3
- B) `1000000`, weight 1
- C) `1111111`, weight 7
- D) `0001000`, weight 1

<details>
<summary>Answer and explanation</summary>

**A) `1110000`, weight 3.**

Data goes to position 3, leaving positions 5, 6 and 7 as `0`. Then each parity bit
is the XOR of the positions it covers: parity at position 1 covers 1, 3, 5, 7, which
holds a single 1, so `p₁ = 1`; parity at position 2 covers 2, 3, 6, 7, again one 1,
so `p₂ = 1`; parity at position 4 covers 4, 5, 6, 7, all zero, so `p₄ = 0`. That
gives `1 1 1 0 0 0 0`. Weight 3 is consistent with `d_min = 3`: the lightest
nonzero codeword *is* `d_min` for a linear code.

Option B copies the data and forgets the parity bits entirely — the encoder's job
is exactly the three XOR steps omitted here. `1000000` is not a codeword: its
syndrome is `1`, so a decoder would flip bit 1 and corrupt a perfectly good
position.

Option C is the codeword for `1111`, weight 7. It is a genuine Hamming(7,4)
codeword — the lesson's output lists `1111 -> 1111111 weight 7` — which is a good
reminder that the code contains both weight 3 and weight 7 words, and `d_min` is
the *minimum*, not the typical weight.

Option D puts the 1 in position 4, which is a *parity* position, not a data
position. Data positions are 3, 5, 6, 7; the powers of two 1, 2, 4 are reserved
for the checks. This is the single most common placement error when writing a
Hamming encoder by hand.

</details>

---

## Subjective Questions

### Short Answer

**Q1. Define the *minimum distance* of a code, and state exactly what it
determines.**

<details>
<summary>Answer</summary>

`d_min = min { d(x, y) : x ≠ y ∈ C }` — the smallest number of bit positions in
which any two distinct codewords of `C` differ.

It determines everything else:

- the code **detects** `d_min − 1` errors;
- the code **corrects** `t = ⌊(d_min − 1)/2⌋` errors.

Detection: an error pattern of weight `e` leaves the received word at distance `e`
from `x`, and that word can only be another codeword if `d_min ≤ e`, so weights up
to `d_min − 1` are always caught. Correction is halved by the triangle inequality:
after `e` errors the word is `e` from the truth and at least `d_min − e` from any
other codeword, so certainty requires `e < d_min − e`.

For a *linear* code, `d_min` is also the smallest nonzero codeword weight, so you
can find it from a generator matrix instead of checking every pair.

</details>

**Q2. State the Hamming bound, define a *perfect* code, and evaluate both for
Hamming(7,4).**

<details>
<summary>Answer</summary>

**The bound.** Correcting `t` errors means every word within distance `t` of a
codeword must decode back to it, so the radius-`t` balls around the codewords must
be pairwise disjoint. Counting:

$$2^{n} \;\ge\; |C| \cdot \sum_{i=0}^{t} \binom{n}{i}.$$

For a `q`-ary alphabet the same counting gives
`q^n ≥ |C| · V(n,t)` with `V(n,t) = Σ_{i=0}^{t} C(n,i)(q−1)^i`.

**Perfect** means equality: the balls *tile* the whole space, with no gaps and no
overlaps, so every possible received word is exactly one error from exactly one
codeword.

**Hamming(7,4).** `n = 7`, `d = 3`, `t = 1`, so `Σ_{i=0}^{1} C(7,i) = 1 + 7 = 8`
and `128/8 = 16`. The code has `2^4 = 16` codewords, so `16 × 8 = 128` — it
achieves the bound exactly. It is perfect.

Contrast the extended Hamming(8,4): `n = 8`, `d = 4`, `t = 1`, bound
`256/9 = 28`, and it has only 16 codewords, so it is *not* perfect.

</details>

**Q3. Define the *syndrome*, and state the property that makes it useful.**

<details>
<summary>Answer</summary>

For a parity-check matrix `H` and a received word `r`, the **syndrome** is
`s = H · rᵀ`. It is `0` if and only if `r` is a codeword.

The property that makes it useful is that, for a linear code, it depends only on
the **error** and not on the message. Writing `r = c + e` with `c` a codeword:

`s = H·(c + e)ᵀ = H·cᵀ + H·eᵀ = 0 + H·eᵀ = H·eᵀ`.

So the receiver computes a small function of the corruption alone, with no
knowledge of the data — which turns decoding from a search over the `2^k` codewords
into a constant amount of arithmetic. In Hamming(7,4), three parity checks give a
3-bit syndrome, and because column `i` of `H` is the binary expansion of `i`, the
syndrome of a single-bit error at position `i` *is* `i`.

</details>

**Q4. What does a Reed–Solomon code with `t` parity symbols guarantee, and what
does the lesson's `NPARITY = 4` codec actually repair?**

<details>
<summary>Answer</summary>

`t` parity symbols correct `⌊t/2⌋` **symbols** and detect `t − 1`. The factor of two
is forced by the same triangle inequality as in binary codes: `t` syndrome values
must distinguish `1 + t` cases (no error, or one of `t` locations). It is *not* `t`
corrections.

The lesson's codec uses `NPARITY = 4` over `GF(256)`, so it corrects exactly
**2** symbols and detects 3. With `g(x) = (x−α⁰)(x−α¹)(x−α²)(x−α³)` and
coefficients `[1, 15, 54, 120, 64]`, the 12-symbol message
`40 d2 75 47 76 17 32 06 27 26 96 c6` gets parity `1e d4 af c1` and syndromes
`[0, 0, 0, 0]`.

With 3 or 4 corrupted symbols the decoder reports failure (`-1`) rather than
returning a plausible wrong answer — which is the behaviour the lesson insists on.

</details>

**Q5. Define `GF(2^m)`, and say why Reed–Solomon does not use arithmetic modulo
`2^m` instead.**

<details>
<summary>Answer</summary>

`GF(2^m)` is the field of degree-`< m` polynomials over `GF(2)`, taken modulo an
irreducible polynomial of degree `m`. `GF(256) = GF(2^8)` is the byte-sized field QR
codes use, built mod `0x11d = x^8 + x^4 + x^3 + x^2 + 1`. It has 256 elements, each
a byte, and every nonzero element has a multiplicative inverse.

Arithmetic modulo `2^m` is *not* the same structure. `2^m` is not prime for `m > 1`,
so `ℤ/256ℤ` has zero divisors: `16 · 16 ≡ 0`, and `16` has no inverse. RS decoding
needs division — `i = log(S_1/S_0)`, and Forney's formula divides by the locator
derivative — so zero divisors make the decoder unsound rather than merely
unusual.

This is the same `ring` versus `field` distinction as in
[Lesson 111](111_modular_arithmetic_and_crypto.md), and it is why the lesson
carries log and antilog tables for the field.

</details>

**Q6. Distinguish *detection* from *correction*, and give the argument for why the
second is strictly harder.**

<details>
<summary>Answer</summary>

**Detection** means noticing that something is wrong. **Correction** means working
out what was wrong and repairing it. Correction implies detection, and strictly
costs more.

The argument is about how much information the receiver must extract. Detection
asks "is this one of my words?", a yes/no question that one parity check answers —
the corrupted word is at distance `e` from `x`, and it is another codeword only if
`d_min ≤ e`. Correction asks "which one of my words is it?", and with `e` errors the
received word sits at distance `e` from the truth and at least `d_min − e` from any
other codeword. To be certain you need `e < d_min − e`, i.e. `2e < d_min`.

Hence `detects = d_min − 1` but `corrects = ⌊(d_min − 1)/2⌋`. A parity bit costs
one extra bit and detects exactly one error; naming *which* bit is wrong costs
`⌈log₂ n⌉` bits at minimum, which is exactly what the Hamming family spends.

</details>

### Long Answer

**Q1. Why is the correction bound `⌊(d−1)/2⌋` rather than the detection bound
`d−1`, and what concretely goes wrong if a decoder spends the full detection
budget on correction?**

<details>
<summary>Model answer</summary>

**The derivation.** Suppose the sent codeword was `x` and `e` bits flip, giving
received word `r`. Then `d(x, r) = e` exactly. By the triangle inequality, for any
other codeword `y`, `d(y, r) ≥ d(y, x) − d(x, r) = d_min − e`. So `r` is at
distance `e` from the truth and at least `d_min − e` from every alternative. A
decoder can only be certain when the nearer candidate is strictly nearer:
`e < d_min − e`, i.e. `2e < d_min`, i.e. `e ≤ ⌊(d_min − 1)/2⌋`. Geometrically this is
the statement that the radius-`t` balls around the codewords are disjoint, which is
the Hamming bound's counting requirement.

**Why the floor, not a rounding.** `⌊3/2⌋ = 1`, not 2. With `d_min = 3` and `e = 2`,
the guarantee `d(y, r) ≥ d_min − e = 1` permits another codeword to sit at distance
2 — exactly as far from the received word as the truth — so the decoder is choosing
between two equally good explanations. The failure case is concrete and the lesson
computes it in Step 8. From `0110011` (data `1011`), flipping bits 3 and 5 gives
`0100111`. The decoder computes syndrome `3 ⊕ 5 = 6`, flips bit 6, and returns the
data `0101` — confidently, and wrongly. It has no way to know: `1100110`, the
codeword for `0110`, is also at distance 2 from `0100111`, so both readings of the
evidence fit equally well.

**What goes wrong with the detection budget.** If you let the decoder correct up to
`d − 1` errors, you have told it to always flip *something* whenever the syndrome is
nonzero, and nothing about the output distinguishes "repaired" from "corrupted
differently". Two concrete symptoms. First, silent mis-correction: two errors
become a confident wrong answer rather than an error report, so a caller cannot
distinguish a repaired word from a wrong one. Second, undetectable errors get
*worse*: at `d − 1` and beyond, error patterns that sum to a zero syndrome — three
flips in Hamming(7,4), where `3 ⊕ 5 ⊕ 6 = 0` — produce a word the decoder accepts as
clean.

**The engineering fix, and its price.** Adding one more parity check takes
`d_min` from 3 to 4. Then `⌊(4−1)/2⌋ = 1` still, but `d_min − 1 = 3` detectable, and
the added overall parity bit makes the error count's parity visible: even-and-
nonzero syndrome means exactly two. That is SECDED, it is what x86 ECC memory uses,
and it is bought with one bit per codeword. You still cannot *correct* two errors —
you can only refuse to claim you did, which is the honest half of the guarantee.

</details>

**Q2. Why does the syndrome depend only on the error? What breaks — in running
time, and in what the decoder returns — for a code that is not linear?**

<details>
<summary>Model answer</summary>

**Why.** Let `H` be a parity-check matrix, so `H·cᵀ = 0` for every codeword `c`. Write
the received word as `r = c + e`. Then
`s = H·rᵀ = H·(c + e)ᵀ = H·cᵀ + H·eᵀ = H·eᵀ`. The message term is *identically* zero,
so the syndrome is a function of the error alone. Exercise 3 checks this
numerically: for each of the 7 single-bit error patterns, the syndrome is identical
across all 16 codewords.

**What it buys in running time.** With the syndrome in hand, the decoder computes
`n − k` parity checks, reads the answer as an index, and flips one bit. That is
constant work per word. Without it, the only correct procedure is to compare `r`
against every codeword and take the closest — a search over the codebook. In
Hamming(7,4) that is 16 comparisons instead of 3 checks; in Hamming(31,26) it is
`2^26` comparisons. Exercise 3 puts the contrast as "the difference between `O(n)`
and `O(1)` per word", and in the extension families the gap becomes the difference
between a usable memory controller and an unusable one.

**What breaks for a non-linear code.** Two things, and the second is worse.

1. *The syndrome is not available.* For a non-linear code the kernel of `H` is no
   longer the code, so there is no `n − k`-bit summary of the error. Decoding
   degenerates to nearest-neighbour search over the codebook, and there is no
   cheap way to invert it, which is why Berlekamp–Massey and Chien search exist for
   Reed–Solomon and nothing comparable exists in the binary Hamming case.
2. *The "zero syndrome means clean" reading is unsound.* For Hamming(7,4), three
   errors give syndrome 0 while the data is wrong. A decoder that reports
   "no error detected" on `s = 0` is making a claim it cannot justify. The
   lesson's `Common Mistakes` entry is exactly this: trusting `s = 0` is
   mistaking a *detection* bound for a *guarantee*. The detection bound is `d − 1 =
   2`; three errors are beyond it, and the fact that they land back on a valid
   codeword is the same phenomenon as undetected two-bit errors in a parity code.

**The general principle.** Linearity buys you the ability to compute a diagnosis
from the error side rather than the data side. Everything downstream — the index
lookup in Hamming codes, the ratio `S_1/S_0` in Reed–Solomon, the error-locator
polynomial — is a way of *reading* that small number. Lose linearity and you lose
the number, and with it the ability to decode in constant time.

</details>

**Q3. A CD interleaves as well as Reed–Solomon encodes. Why is interleaving
necessary, and what exactly does it change about the same 12 consecutive errors?**

<details>
<summary>Model answer</summary>

**Why it is necessary.** Reed–Solomon corrects `⌊t/2⌋` *symbols* anywhere in a
codeword — but its power is bounded per codeword, not per transmission. A physical
scratch on an optical disc is not a scattering of independent symbol errors; it is
one contiguous region of the medium. A burst of 12 consecutive corrupted symbols
does not distribute itself. Without interleaving, all 12 land inside a single
10-symbol codeword — 10 errors in one word — and a word with 4 parity symbols can
correct 2. The message is lost, and the redundancy you paid for was wasted, because
it was concentrated where it could not help. Binary Hamming codes have the same
weakness, which is why they are matched to isolated single-bit flips (the
ECC-memory situation) rather than to bursts.

**What changes, precisely.** Nothing about the code. Exercise 4 sends six
codewords of `k + 4` symbols and compares two framings of the identical codeword
set. *Without* interleaving the transmitter writes each word's symbols
consecutively, so the burst produces `errors per word = [10, 2, 0, 0, 0, 0]` and the
data is not recovered. *With* interleaving the transmitter reads one symbol from
each word in turn — row by row across the six words — so the same 12 consecutive
*channel* errors are distributed as exactly `2` errors in each of the six words.
Two is precisely the correction capacity, so every word is recoverable and the
message comes back intact.

**Why that is the right way to think about it.** The lesson's summary of the
exercise is the whole idea: "The encoder, the decoder, and the amount of redundancy
are identical — only the ordering on the wire changed." Interleaving is a
*reordering* with no coding cost at all — no extra symbols, no extra arithmetic, no
change to the error-detection power. It converts a *fatal* burst into `⌈b / words⌉`
independent, individually correctable errors. The design question it answers is not
"how much parity do I need" but "how many independent pieces must I cut my data
into, given the burst length I actually expect."

**Where you see it.** A 700 MB disc survives a 2 cm scratch and a QR code survives
a folded corner because both interleave *and* code. QR codes make the trade visible
in print: levels L through H carry 10 to 30 parity symbols and recover 7% to 30% of
codewords. Deep-space probes do the same with convolutional codes, because a bit
error 200 million kilometres away is as likely as one next door and there is no
retransmission available.

</details>

**Q4. Hamming(7,4) is a perfect code but the extended Hamming(8,4) is not. Why,
and what does that tell you about ECC memory?**

<details>
<summary>Model answer</summary>

**The arithmetic.** For `n = 7`, `d = 3`, `t = 1`: the radius-1 ball has
`1 + C(7,1) = 8` words, so the bound is `2^7 / 8 = 16`, and Hamming(7,4) has
`2^4 = 16` codewords. Equality: the balls tile all 128 words. For `n = 8`, `d = 4`,
`t = 1`: the ball still has `1 + C(8,1) = 9` words, so the bound is
`2^8 / 9 = 28`, and Hamming(8,4) has only 16 codewords. Since `16 < 28`, it is not
perfect — there are gaps. A received word inside a gap is at distance 2 from two
different codewords, which is precisely the two-bit ambiguity the (8,4) decoder
reports.

**Why, structurally.** Extending the code raises `d` from 3 to 4 without raising `t`,
which is still `⌊(4−1)/2⌋ = 1`. A sphere of radius 1 around each codeword grows in
*relative* terms (a 9-word ball in a 256-word space versus 8 in a 128-word space) but
the codeword count stays at 16, so coverage falls short of the bound. You paid one
extra bit and bought detection, not correction. Perfectness is not a design goal you
can reach by adding parity; it is an extraordinarily rare structural accident. Over
the binary alphabet the only perfect codes are the trivial ones, repetition-3, and
`Hamming(2^r − 1, 2^r − r − 1)`, and it has been *proven* that no others exist. The
Singleton bound `q^(n−d+1)` is looser still — it gives `2^5 = 32` for Hamming(7,4)
against the Hamming bound's tighter `16`.

**What that means for hardware.** The lesson's conclusion is direct: Hamming codes
"have therefore been the only sensible choice for single-error correction in hardware
for sixty years: they are the unique perfect codes, so they waste nothing, and their
syndrome is an `(n−k)`-bit number that *is* the address of the bad bit." Two
properties matter together. Perfectness means no capacity is wasted on structure
that corrects nothing. And the syndrome being the error *address* means correction
is a handful of XOR gates and one conditional flip — the decoder is trivially small,
fast and branch-free, which is what a memory controller needs on every single access.

That is also why x86 ECC memory settles for SECDED rather than something with a
better rate: the failure it must survive is a cosmic ray flipping one bit in
cheap DRAM, which happens often enough that a single soft error would be
unacceptable, and rare enough that double-bit errors do not justify a more complex
code. `⌊d/2⌋` versus `d` is the trade, and the hardware answer is: detect the second
error, never claim to have corrected it, and let the operating system re-fetch the
page.

</details>

**Q5. Why must a Reed–Solomon decoder refuse to guess when it has more errors than
`t`, rather than return its best candidate?**

<details>
<summary>Model answer</summary>

**The arithmetic reason.** The decoder's only source of information is the `t`
syndrome values `S_j = Σ e_i α^(ji)`, and past `⌊t/2⌋` errors that vector is
consistent with many different error patterns. Berlekamp–Massey returns an error
locator polynomial of degree `L`; the decoder refuses when `L > ⌊t/2⌋`, because no
pattern inside the promised radius is consistent with the syndromes — the
corruption is not one the code can explain. Returning *something* then means
picking an arbitrary pattern among all the ones that fit, and the lesson's code
shows the alternative plainly: a decoder that flips `block[0] ^= synd[0]` "will
'correct' some arbitrary bit and return garbage". The lesson's own run, with 3 and
4 corrupted symbols, prints `decoder reported -1 (gave up)` on both.

**The systems reason, which is stronger.** A decoder that returns wrong data is
worse than one that fails, because the caller cannot tell the difference. A
returned byte array looks identical whether it was repaired or corrupted; the caller
proceeds. A failure is *actionable*: the memory controller can signal the error, the
disk layer can request a re-read, the TCP sender can retransmit — and the lesson
makes this point when discussing the (8,4) code, where reporting "2 errors" and
returning garbage at least prevents the worst outcome of falsely reporting success.
"Detection without correction is what you want when the receiver can ask for a
retransmission, which is what a TCP sender does."

**The same principle inside the arithmetic.** Even within the correctable range the
decoder must *verify*. One error is confirmed against `S_2, S_3`; two errors are
solved for `e₁, e₂` and then checked against the remaining syndromes; and the
production pipeline — Berlekamp–Massey for the locator, Chien search for the roots,
Forney's formula for the magnitudes — exists partly so that the count of found roots
(`len(positions) != L`) and the invertibility of the locator derivative can be
checked. A decoder that skips verification cannot distinguish "the errors I found
explain the syndromes" from "the errors I found are one of many explanations".

**The general lesson.** A correcting code's promise is a *bounded* one: `⌊t/2⌋`
symbols, no more. The system's integrity depends on the failure mode at the
boundary being honest, which is why the lesson's `Common Mistakes` list treats
"using an RS decoder that guesses when it cannot correct" as an error in its own
right rather than a stylistic choice.

</details>

## Exercises and Solutions

**[ ] Exercise 1 —** Compute `d_min` by brute force for these codes and check
each against the prediction `detects = d − 1`, `corrects = ⌊(d−1)/2⌋`: (a) the
8-bit uncoded code, (b) the 9-bit even-weight code, (c) repetition-3 of 3 bits,
(d) the 4-bit single-parity-0 code (all words with even weight), (e) the
4-bit single-parity-1 code (odd weight). Then explain in two sentences why (d)
and (e) have the same distance.

<details>
<summary>Solution</summary>

```python
def hamming(x, y):
    return sum(1 for a, b in zip(x, y) if a != b)


def min_distance(words):
    return min(hamming(words[i], words[j])
               for i in range(len(words))
               for j in range(i + 1, len(words)))


codes = {
    "uncoded 8-bit": [format(i, "08b") for i in range(256)],
    "even weight 9-bit": [f"{i:09b}" for i in range(512) if bin(i).count("1") % 2 == 0],
    "repetition-3 of 3 bits": ["".join(b * 3 for b in f"{i:03b}")
                               for i in range(8)],
    "parity-0 4-bit (even)": [f"{i:04b}" for i in range(16)
                              if bin(i).count("1") % 2 == 0],
    "parity-1 4-bit (odd)": [f"{i:04b}" for i in range(16)
                             if bin(i).count("1") % 2 == 1],
}

print(f"{'code':>26} {'words':>6} {'d_min':>6} {'detects':>9} {'corrects':>10}")
for name, words in codes.items():
    d = min_distance(words)
    print(f"{name:>26} {len(words):>6} {d:>6} {d - 1:>9} {(d - 1) // 2:>10}")
```

Output:

```
                      code  words  d_min   detects   corrects
             uncoded 8-bit    256      1         0          0
         even weight 9-bit    256      2         1          0
repetition-3 of 3 bits      8      3         2          1
  parity-0 4-bit (even)      8      2         1          0
   parity-1 4-bit (odd)      8      2         1          0
```

Parity-0 and parity-1 both consist of the even-weight words shifted by one bit,
so they are the same set of pairwise distances — changing the parity
convention moves the code but does not change its geometry. That is also why
"even" and "odd" parity differ only in *which* errors are caught, never *how
many*: both have `d = 2` and detect exactly one error.

</details>

**[ ] Exercise 2 —** Generalise Hamming(7,4) to Hamming(15,11): parity bits at
positions 1, 2, 4, 8, data in the other 11. Encode the all-ones message, then
flip each of the 15 bits in turn and confirm that in every case the syndrome
equals the flipped position and the decoder recovers the message. Report the
redundancy ratio for (7,4), (15,11) and (31,26).

<details>
<summary>Solution</summary>

```python
def hamming_encode(data: str, r: int) -> str:
    """Hamming(2^r - 1, 2^r - 1 - r) systematic encoder."""
    n = (1 << r) - 1
    assert len(data) == n - r
    data_positions = [i for i in range(1, n + 1) if (i & (i - 1)) != 0]
    bits = ["0"] * n
    for pos, b in zip(data_positions, data):
        bits[pos - 1] = b
    for k in range(r):
        p = 1 << k                       # parity positions are 1, 2, 4, 8, ...
        covered = [i for i in range(1, n + 1) if i != p and (i >> k) & 1]
        bits[p - 1] = str(sum(int(bits[j - 1]) for j in covered) % 2)
    return "".join(bits)


def hamming_syndrome(codeword: str, r: int) -> int:
    s = 0
    for k in range(r):
        covered = [i for i in range(1, len(codeword) + 1) if (i >> k) & 1]
        if sum(int(codeword[i - 1]) for i in covered) % 2 == 1:
            s |= 1 << k
    return s


def hamming_decode(received: str, r: int):
    s = hamming_syndrome(received, r)
    if s == 0:
        data_positions = [i for i in range(1, len(received) + 1)
                          if (i & (i - 1)) != 0]
        return "".join(received[i - 1] for i in data_positions), 0
    fixed = list(received)
    fixed[s - 1] = "1" if fixed[s - 1] == "0" else "0"
    data_positions = [i for i in range(1, len(received) + 1)
                      if (i & (i - 1)) != 0]
    return "".join("".join(fixed)[i - 1] for i in data_positions), 1


def flip(word, pos):
    c = list(word)
    c[pos - 1] = "1" if c[pos - 1] == "0" else "0"
    return "".join(c)


for r in (3, 4, 5):
    n = (1 << r) - 1
    k = n - r
    data = "1" * k
    code = hamming_encode(data, r)
    assert hamming_syndrome(code, r) == 0
    ok = True
    for pos in range(1, n + 1):
        received = flip(code, pos)
        s = hamming_syndrome(received, r)
        got, nerr = hamming_decode(received, r)
        if not (s == pos and got == data and nerr == 1):
            ok = False
    print(f"Hamming({n},{k}): all {n} single-bit errors located and fixed: {ok}")
    print(f"   redundancy {r}/{n} = {r / n:.4f}")

print()
print("redundancy falls as the code grows:")
for r in (3, 4, 5, 6, 7):
    n = (1 << r) - 1
    print(f"   r={r}: Hamming({n},{n - r}), redundancy {r}/{n} = "
          f"{r / n:.4f}")
```

The syndromes equal the flipped position for every single-bit error, because
column `i` of the parity-check matrix is the binary expansion of `i`. The
redundancy ratio `r / (2^r − 1)` halves each time `r` grows by one, so large
Hamming codes are cheap — the reason ECC memory adds 7 bits per 64-bit word
rather than the 64 a naive repetition scheme would need.

</details>

**[ ] Exercise 3 —** Verify the linearity claim on Hamming(7,4): for all 16
codewords `c`, check that `syndrome(c) = 0` and that the XOR of any two
codewords is itself a codeword. Then show that the syndrome of `c + e` depends
only on `e` and not on `c`, by taking a fixed error `e` and checking that all
16 codewords give the same syndrome. Explain in two sentences why that property
is what makes Hamming decoding a lookup rather than a search.

<details>
<summary>Solution</summary>

```python
DATA_POSITIONS = [3, 5, 6, 7]
PARITY_POSITIONS = [1, 2, 4]


def encode(data):
    bits = ["0"] * 7
    for pos, b in zip(DATA_POSITIONS, data):
        bits[pos - 1] = b
    for k, p in enumerate(PARITY_POSITIONS):
        covered = [i for i in range(1, 8) if i != p and (i >> k) & 1]
        bits[p - 1] = str(sum(int(bits[j - 1]) for j in covered) % 2)
    return "".join(bits)


def syndrome(c):
    s = 0
    for k in range(3):
        covered = [i for i in range(1, 8) if (i >> k) & 1]
        if sum(int(c[i - 1]) for i in covered) % 2 == 1:
            s |= 1 << k
    return s


def xor(a, b):
    return "".join(str(int(x) ^ int(y)) for x, y in zip(a, b))


def weight(c):
    return c.count("1")


codewords = {encode(format(i, "04b")) for i in range(16)}
assert len(codewords) == 16

print(f"all 16 codewords have syndrome 0: "
      f"{all(syndrome(c) == 0 for c in codewords)}")

closed = True
for c in sorted(codewords):
    for d in sorted(codewords):
        if xor(c, d) not in codewords:
            closed = False
print(f"the set is closed under XOR: {closed}")

print()
print("syndrome of a fixed error pattern, across all 16 codewords:")
for pos in range(1, 8):
    e = ["0"] * 7
    e[pos - 1] = "1"
    e = "".join(e)
    values = {syndrome(xor(c, e)) for c in codewords}
    print(f"   error at position {pos}: syndromes over all codewords = "
          f"{values}, all equal: {len(values) == 1}")
```

Because `H·c = 0` for every codeword, `syndrome(c + e) = H·c + H·e = H·e`, so the
syndrome is a function of the error alone. That means the decoder does not have
to compare the received word against all 16 codewords — it computes three
parity checks, reads the answer as an index, and flips one bit. Without
linearity, every decode would be a search over the codebook, which is exactly
the difference between `O(n)` and `O(1)` per word.

</details>

**[ ] Exercise 4 —** Build a parameterised RS codec with 4, 8 and 16
parity symbols and confirm that it corrects exactly 2, 4 and 8 symbol
errors. Then show why a *burst* of 12 consecutive errors destroys a
non-interleaved code that recovers happily from 12 scattered errors, and
demonstrate that interleaving fixes it without changing the code at all.

<details>
<summary>Solution</summary>

```python
"""Exercise 4 solution: RS at several parity levels, plus interleaving.

Verified with the Berlekamp-Massey decoder from the lesson.
"""
import random


class GF256:
    PRIMITIVE = 0x11D
    ORDER = 255

    def __init__(self):
        self.exp = [0] * 512
        self.log = [0] * 256
        x = 1
        for i in range(self.ORDER):
            self.exp[i] = x
            self.log[x] = i
            x <<= 1
            if x & 0x100:
                x ^= self.PRIMITIVE
        for i in range(self.ORDER, 512):
            self.exp[i] = self.exp[i - self.ORDER]

    def mul(self, a, b):
        return 0 if a == 0 or b == 0 else self.exp[self.log[a] + self.log[b]]

    def div(self, a, b):
        assert b
        return 0 if a == 0 else self.exp[(self.log[a] - self.log[b]) % self.ORDER]

    def inv(self, a):
        assert a
        return self.exp[(self.ORDER - self.log[a]) % self.ORDER]

    def power(self, a, e):
        r, b = 1, a
        while e:
            if e & 1:
                r = self.mul(r, b)
            b = self.mul(b, b)
            e >>= 1
        return r

    def poly_eval(self, p, x):
        acc = 0
        for c in p:
            acc = self.mul(acc, x) ^ c
        return acc

    def poly_rem(self, p, g):
        out = list(p)
        n = len(g)
        for i in range(len(out) - n + 1):
            if out[i]:
                coef = out[i]
                for j in range(n):
                    out[i + j] ^= self.mul(coef, g[j])
        return out[len(out) - n + 1:]

    def poly_mul_pow(self, p, q):
        out = [0] * (len(p) + len(q) - 1)
        for i, a in enumerate(p):
            if a:
                for j, b in enumerate(q):
                    if b:
                        out[i + j] ^= self.mul(a, b)
        return out

    def poly_eval_pow(self, p, x):
        acc = 0
        for c in reversed(p):
            acc = self.mul(acc, x) ^ c
        return acc


F = GF256()


def make_codec(nsym):
    g = [1]
    for i in range(nsym):
        g = F.poly_mul_pow(g, [F.exp[i], 1])
    g = list(reversed(g))

    def encode(data):
        return list(data) + F.poly_rem(list(data) + [0] * nsym, g)

    def syndromes(block):
        return [F.poly_eval(block, F.exp[i]) for i in range(nsym)]

    def berlekamp_massey(synd):
        C, B = [1], [1]
        L, m, b = 0, 1, 1
        for n in range(nsym):
            d = synd[n]
            for i in range(1, L + 1):
                if i < len(C) and C[i]:
                    d ^= F.mul(C[i], synd[n - i])
            if d == 0:
                m += 1
                continue
            coef = F.div(d, b)
            previous = list(C)
            shifted = [0] * m + [F.mul(coef, c) for c in B]
            if len(shifted) > len(C):
                C = C + [0] * (len(shifted) - len(C))
            for j, c in enumerate(shifted):
                C[j] ^= c
            if 2 * L <= n:
                L, B, b, m = n + 1 - L, previous, d, 1
            else:
                m += 1
        return C, L

    def decode(block):
        synd = syndromes(block)
        if not any(synd):
            return list(block), 0
        n = len(block)
        locator, L = berlekamp_massey(synd)
        if L == 0 or L > nsym // 2:
            return list(block), -1
        positions = [p for p in range(n)
                     if F.poly_eval_pow(locator, F.exp[(F.ORDER - (n - 1 - p))
                                                      % F.ORDER]) == 0]
        if len(positions) != L:
            return list(block), -1
        omega = F.poly_mul_pow(synd, locator)[:nsym]
        deriv = [locator[i] if i % 2 == 1 else 0 for i in range(1, len(locator))]
        if not any(deriv):
            return list(block), -1
        fixed = list(block)
        for p in positions:
            X = F.exp[(n - 1 - p) % F.ORDER]
            xinv = F.inv(X)
            den = F.poly_eval_pow(deriv, xinv)
            if den == 0:
                return list(block), -1
            fixed[p] ^= F.mul(X, F.div(F.poly_eval_pow(omega, xinv), den))
        return fixed, len(positions)

    return encode, decode, syndromes


DATA = [0x40, 0xD2, 0x75, 0x47, 0x76, 0x17, 0x32, 0x06, 0x27, 0x26, 0x96,
        0xC6]

random.seed(21)
for nsym in (4, 8, 16):
    encode, decode, syndromes = make_codec(nsym)
    block = encode(DATA)
    assert syndromes(block) == [0] * nsym
    print(f"{nsym} parity symbols, promises {nsym // 2} corrections")
    for nerr in range(nsym // 2 + 1):
        ok, trials = 0, 300
        for _ in range(trials):
            bad = list(block)
            for p in random.sample(range(len(block)), nerr):
                bad[p] ^= random.randrange(1, 256)
            fixed, _ = decode(bad)
            ok += fixed[:len(DATA)] == DATA
        print(f"   {nerr} random error(s): recovered {ok} of {trials}")
    beyond = []
    for _ in range(50):
        bad = list(block)
        for p in random.sample(range(len(block)), nsym // 2 + 1):
            bad[p] ^= random.randrange(1, 256)
        fixed, reported = decode(bad)
        beyond.append(reported < 0 or fixed[:len(DATA)] == DATA)
    print(f"   {nsym // 2 + 1} errors: refused or accidentally right in "
          f"{sum(beyond)} of 50")
    print()

# ------------------------------------------------------------- interleaving
# Split a long message into many short codewords, interleave them row by row,
# transmit, then de-interleave and decode each word independently.
encode, decode, syndromes = make_codec(4)      # corrects 2 symbols per word
K, NSYM = 6, 4
WORD = K + NSYM
MESSAGE = [(0x10 + 7 * i) % 256 for i in range(36)]     # 6 words of 6
NWORDS = len(MESSAGE) // K


def rs_interleave_encode(data, k):
    """Split into words, encode each, then read the words out row by row."""
    words = [encode(data[i:i + k]) for i in range(0, len(data), k)]
    stream = []
    for row in range(k + NSYM):
        for w in words:
            stream.append(w[row])
    return words, stream


def rs_interleave_decode(stream, k, nwords):
    """Undo the row-by-row reading, decode each word, and reassemble."""
    words = [[] for _ in range(nwords)]
    i = 0
    for row in range(k + NSYM):
        for w in range(nwords):
            words[w].append(stream[i])
            i += 1
    out = []
    for w in words:
        fixed, _ = decode(w)
        out.extend(fixed[:k])
    return out


words, stream = rs_interleave_encode(MESSAGE, K)
plain = [s for w in words for s in w]           # same code, not interleaved
print(f"interleaving: {NWORDS} RS words of {WORD} symbols, "
      f"stream of {len(stream)} symbols")
print(f"   word 0 by itself:      {' '.join(f'{b:02x}' for b in words[0])}")
print(f"   plain concatenation:   {' '.join(f'{b:02x}' for b in plain[:WORD])}")
print(f"   interleaved stream:    {' '.join(f'{b:02x}' for b in stream[:WORD])}")
print("   the stream takes one symbol from each word in turn, so a run of")
print("   consecutive errors is shared out instead of concentrated")
print()

BURST = 12

# --- no interleaving: the burst lands inside one word
damaged = list(plain)
for p in range(BURST):
    damaged[p] ^= 0x77
pieces = [damaged[i * WORD:(i + 1) * WORD] for i in range(NWORDS)]
errors_per_word = [sum(1 for a, b in zip(piece, words[i]) if a != b)
                   for i, piece in enumerate(pieces)]
out = []
for piece in pieces:
    fixed, _ = decode(piece)
    out.extend(fixed[:K])
print(f"without interleaving: burst of {BURST} symbols")
print(f"   errors per word: {errors_per_word}  "
      f"(correction capacity is {NSYM // 2})")
print(f"   data recovered: {out == MESSAGE}")
print()

# --- interleaved: the burst is shared out, 2 errors in each word
damaged = list(stream)
for p in range(BURST):
    damaged[p] ^= 0x77
errors_per_word = []
for w in range(NWORDS):
    nerr = sum(1 for row in range(WORD)
               if damaged[row * NWORDS + w] != stream[row * NWORDS + w])
    errors_per_word.append(nerr)
out = rs_interleave_decode(damaged, K, NWORDS)
print(f"with interleaving: the same burst of {BURST} symbols")
print(f"   errors per word: {errors_per_word}  "
      f"(correction capacity is {NSYM // 2})")
print(f"   data recovered: {out == MESSAGE}")
print()
print(f"A burst of {BURST} symbols spreads over {NWORDS} words, so each word sees")
print(f"about {BURST // NWORDS} errors and its {NSYM} parity symbols fix that.")
print("Without interleaving the same burst lands inside one word and destroys")
print("it. The code is identical; only the order of symbols on the wire is.")
```

The `errors per word` lines are the whole lesson. Without interleaving the burst
puts 10 errors into a single word that can only fix 2, so the message is lost.
With interleaving the same 12 consecutive channel errors arrive as exactly 2
errors in each of the 6 words, and every word is recoverable. The encoder,
the decoder, and the amount of redundancy are identical — only the ordering on
the wire changed. That is why a CD and a QR code both interleave: it converts a
*fatal* burst error into `ceil(burst / words)` independent, individually
correctable errors.

</details>

**Challenge** — Compute the **Singleton bound** and the **Hamming bound**
for the codes below and identify which are *perfect*, i.e. achieve the
Hamming bound with equality. Then explain in three sentences why a perfect
code is rare, and why that rarity is why every ECC controller ever made is
a Hamming code.

<details>
<summary>Solution</summary>

```python
from math import comb


def singleton_bound(n, d, q):
    """Any length-n code over an alphabet of size q with distance d."""
    return q ** (n - d + 1)


def hamming_bound(n, d, q):
    """The correction spheres around the codewords must fit inside q^n."""
    t = (d - 1) // 2
    ball = sum(comb(n, i) * (q - 1) ** i for i in range(t + 1))
    return q ** n // ball


CODES = [
    # name,                      q,    n,  d,  |C|
    ("uncoded binary",            2,    8,  1,  256),
    ("even-parity binary",        2,    9,  2,  256),
    ("repetition-3",              2,    3,  3,    2),
    ("Hamming(7,4)",              2,    7,  3,   16),
    ("extended Hamming(8,4)",     2,    8,  4,   16),
    ("Hamming(15,11)",            2,   15,  3, 2048),
    ("Hamming(31,26)",            2,   31,  3, 2**26),
    ("RS(16, 3) over GF(256)",  256,   16, 13,  256),
]

print("the Singleton bound q^(n-d+1):  no code can beat it")
print(f"{'code':>24} {'q':>4} {'n':>4} {'d':>3} {'|C|':>9} {'bound':>16}")
for name, q, n, d, size in CODES:
    print(f"{name:>24} {q:>4} {n:>4} {d:>3} {size:>9} "
          f"{singleton_bound(n, d, q):>16}")

print()
print("the Hamming bound, which is about correction rather than structure")
print(f"{'code':>24} {'|C|':>9} {'bound':>16} {'perfect?':>10}")
for name, q, n, d, size in CODES:
    hb = hamming_bound(n, d, q)
    print(f"{name:>24} {size:>9} {hb:>16} {str(size == hb):>10}")

print()
perfect = [name for name, q, n, d, size in CODES
           if size == hamming_bound(n, d, q)]
print("perfect codes among these:", perfect)
print("Hamming(7,4), Hamming(15,11), Hamming(31,26) and repetition-3 all")
print("reach the bound exactly: their radius-1 spheres tile the space with")
print("no gaps and no overlaps.  Binary perfect codes are known only at")
print("lengths 1, 3, 7, 15 and 31, and it has been proven that no others")
print("exist.  That is why every ECC controller ever made is a Hamming code.")
```

The Singleton bound is the easy one.  Project every codeword onto any
`n − d + 1` of its `n` coordinates: two codewords cannot agree on all of
those, because agreeing on `n − d + 1` positions means differing in at most
`d − 1`.  So the projection is injective, and there are only
`q^(n−d+1)` possible projections.

The Hamming bound is about geometry.  Correcting `t` errors means every received
word within distance `t` of a codeword must decode back to it, so the spheres
of radius `t` around the codewords must be pairwise disjoint; disjoint sets
inside a space of `q^n` words must satisfy `|C| · V(n, t) ≤ q^n`, where
`V(n, t) = Σ C(n, i)(q−1)^i` counts the words in one sphere.

A **perfect** code achieves equality: the spheres tile the entire space with no
gaps and no overlaps, so every possible received word is exactly one error away
from exactly one codeword.  That is a tiling of a finite space by spheres, and
such tilings are extremely constrained — over the binary alphabet the only
perfect codes are the trivial ones, repetition-3, and
Hamming(2^r − 1, 2^r − r − 1), and it has been proven that no others
exist.  Hamming codes have therefore been the only sensible choice for
single-error correction in hardware for sixty years: they are the unique
perfect codes, so they waste nothing, and their syndrome is a `(n − k)`-bit
number that *is* the address of the bad bit.

</details>

## Summary

- The binary symmetric channel flips each bit independently with probability `p`;
  no sender can prevent it, only prepare for it.
- **Detection** asks "is this one of my words?", **correction** asks "which one?",
  and the second is strictly harder. Hence `detects = d − 1` but
  `corrects = ⌊(d−1)/2⌋`.
- Hamming distance is the count of differing positions; minimum distance `d`
  over a code decides both numbers. The correction bound comes from the triangle
  inequality: after `e` errors you must be closer to the truth than to anything
  else, so `2e < d`.
- **Parity** gives `d = 2`: detects one error, corrects none. **Repetition-3**
  gives `d = 3` at 3× the bandwidth. Both are the crude ends of the trade.
- Over `GF(2)` addition is XOR, so linear codes are XOR-combinations of a basis
  row, and a linear code's `d_min` is its smallest nonzero codeword weight.
- The **syndrome** `s = H·rᵀ` depends only on the error, not the message, so
  decoding is a lookup rather than a search over the codebook.
- In **Hamming(7,4)** the parity-check columns are the binary expansions of
  `1..7`, so the syndrome of a single-bit error *is* the flipped position.
  Three parity bits buy 43% redundancy and correction of one bit.
- **Hamming(8,4)** adds an overall parity bit so a decoder can tell one error
  from two — SECDED, which is what x86 ECC memory uses.
- **Reed-Solomon** runs the same syndrome machinery over `GF(2^m)`, correcting
  `t/2` corrupted *symbols* rather than bits, which is what burst errors like
  CD scratches and QR folds actually look like. Interleaving is what spreads a
  burst across codewords so it becomes correctable.

## Next

This is the last lesson in Part 09. The three ideas here — that arithmetic
modulo a number is a different algebra from arithmetic on numbers, that a
hash is a way of making a fixed-size fingerprint that is hard to invert, and
that redundancy can be spent to undo corruption as well as to detect it — are
the toolkit for [Part 10: Tensors and Numerical Methods](../part10_tensors_numerical/),
where the same themes reappear as floating-point precision, broadcasting rules,
and the difference between an exact computation and a stable one.