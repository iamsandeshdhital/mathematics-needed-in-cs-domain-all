# 112 — Hashing

**Part**: part09_number_theory_crypto · **Prerequisites**: 110 · **Time**: 35 min

---

## In Plain Words

A hash function turns anything — a string, a file, an integer — into a fixed
size number. The same input always gives the same number, different inputs
usually give different numbers, and it is fast. That is the whole idea, and it
is enough to build the dictionary type you use every day: instead of comparing
two keys to see whether they are equal, you compute a number for each, look the
numbers up in an array, and compare one thing instead of many. Because the
number is fixed size while the input is not, some inputs must collide, and the
clever part of a good hash table is deciding where colliding keys go and
keeping that decision cheap. Later in the lesson the same function is used for
something completely different — proving that a file has not changed, and
proving that a message came from someone who holds a key — and for that job the
requirements are much stricter.

## Why Computer Science Cares

- **`dict` and `set` in Python.** A CPython dict is an open-addressing table
  with a load-factor threshold of 2/3 and a resize that rehashes every key.
  `frozenset` works the same way.
- **JavaScript object properties, Rust `HashMap`, Go maps** — every one is a
  hash table, and every one has a documented load factor and a documented
  worst case that is `O(n)`.
- **`zlib.crc32`, `hashlib.sha256`, git object IDs, Docker content digests,
  BitTorrent info hashes** — the same mathematical object used as a
  fingerprint rather than an index.
- **Content addressing.** In git, IPFS and every blockchain, the address of a
  block *is* its hash, so the hash is what detects tampering. This is the
  bridge to [Lesson 113](113_error_correcting_codes.md), which asks the
  complementary question: how do you *repair* a corrupted block instead of
  detecting it?
- **Interview questions.** "Implement a hash map", "why does deletion in
  open addressing need a tombstone", "what is the birthday paradox and why
  should I care" are three of the most common follow-ups in systems interviews.

## The Formal Version

Notation follows [SYMBOLS.md](../SYMBOLS.md). Used here: `O()`, `Θ()`,
`α`, `√`.

### Hash functions

**Definition.** A **hash function** `h: K → {0, 1, …, m−1}` maps keys to bucket
indices. Keys `x ≠ y` with `h(x) = h(y)` **collide**; such pairs are unavoidable
whenever `|K| > m`, because the pigeonhole principle
([Lesson 23](../part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md))
guarantees it.

**Definition.** The **load factor** `α` is `α = n / m`, the number of keys
divided by the number of buckets.

**Definition.** The **multiplicative order**-free notion of *uniformity*: for
random `x` and a random `y ≠ x`,
`Pr[h(x) = h(y)]` should be close to `1/m`. This is the property that makes
lookups cheap.

### What a good table hash needs

**Definition.** A hash function is **good for tables** when:

1. **Deterministic** — the same key always hashes to the same bucket, or
   `get` cannot find what `put` stored.
2. **Fast** — `O(len(key))` with a small constant. It runs on every operation.
3. **Uniform** — collisions are rare and spread out, so chains stay short.
4. **Cheap to fit** — a power-of-two table size lets the bucket index be
   `h(k) & (m−1)` instead of a division. This only works if the hash function
   mixes the *high* bits down into the low ones.
5. **Known to be unhurried by the key distribution** — if your keys are
   consecutive integers, `k % m` is useless. This is the classic hash-flooding
   denial-of-service: PHP's `md5` bucket distribution was defeated for years by
   sending keys that all hashed to the same bucket.

It is *not* required to be hard to invert. Collisions in a table are handled;
they are not an attack.

### Expected cost, and why tables resize

**Theorem.** With chaining, a lookup or insert walks one chain whose expected
length is `α`, so the expected cost is `Θ(1 + α)`.

*Explanation.* Balls-in-bins: `n` balls thrown uniformly into `m` bins give
bin loads distributed around `α = n/m` with standard deviation `√α`. A
particular lookup walks the bin its own key landed in, whose length is
distributed as `α`. ∎

**Theorem.** With linear probing, the expected number of probes for an
unsuccessful search is `Θ(1 / (1 − α))`.

*Explanation.* A cluster of `k` consecutive occupied slots is entered by any of
roughly `k` different home slots, so cluster lengths are not binomial but
growing with the occupancy. Solving the recurrence gives `1/(1 − α)`. The
consequence is that as `α → 1` the table stops being `O(1)` in any useful
sense. ∎

**Design consequence.** Every implementation therefore caps `α` and resizes
when it is exceeded. Doubling the table on overflow makes the amortised cost of
an insertion `O(1)` by the amortised analysis of
[Lesson 81](../part06_algorithms_math/81_amortized_analysis.md): each element is
rehashed `O(log n)` times over `n` doublings, so the total is `Θ(n)`.

### The birthday paradox

**Theorem.** Drawing `n` items independently and uniformly from `m` buckets,
the probability of at least one collision is

```
Pr[collision] = 1 - Π_{k=0}^{n-1} (1 - k/m)  ≈  1 - exp(-n² / 2m)
```

*Explanation.* The `k`-th draw avoids all `k` earlier buckets with probability
`1 - k/m`; multiply the independent steps and subtract from 1. For `n ≪ √m` use
`ln(1 - x) ≈ -x`. ∎

**Corollary.** Collisions become likely at `n ≈ √(2m ln 2) ≈ 1.177 √m`, not at
`n ≈ m`.

**Consequence for security.** For an `n`-bit hash:
- **preimage attack**: `2^n` work;
- **collision attack**: `2^(n/2)` work by the birthday bound.

So SHA-256 gives 256-bit preimage resistance and 128-bit collision resistance.
That is why a 32-bit CRC is a corrupt-data detector and never a security
control: `2^16 = 65,536` random items collide with probability 1/2.

### Cryptographic hash requirements

**Definition.** `H` is **preimage resistant** if no algorithm finds `m` with
`H(m) = y` faster than exhaustive search. **Second-preimage resistant** if,
given `m`, no algorithm finds `m' ≠ m` with `H(m') = H(m)`. **Collision
resistant** if no algorithm finds any `m₁ ≠ m₂` with `H(m₁) = H(m₂)`.

**Definition.** **Avalanche** means a one-bit input change flips about half the
output bits. Formalised: for uniform random `x` and a random bit `i`,
`Pr[bit j of H(x) ≠ bit j of H(x with bit i flipped)] ≈ 1/2` for every `j`.

**Theorem.** Collision resistance implies second-preimage resistance; the
converse is not known to hold. So collision resistance is the strong requirement
and everything else is easier.

**Caveat — length extension.** A Merkle–Damgård construction such as SHA-1 or
SHA-256 satisfies `H(m ‖ glue ‖ m')` computable from `H(m)` alone. For the Rabin
polynomial hash `H(m) = Σ cᵢBⁱ mod M` this is explicit:
`H(m ‖ extra) = H(m)·B^len(extra) + H(extra) mod M`. HMAC avoids it; SHA-3
avoids it by using a sponge instead.

**Definition.** **Domain separation** means prefixing the message with a label
identifying what it is for, so a digest for one purpose can never be replayed
as a digest for another.

### Merkle trees

**Definition.** A **Merkle tree** hashes leaves pairwise bottom-up to a single
**root**. A **Merkle proof** for leaf `i` is the `⌈log₂ n⌉` sibling hashes on
the path from that leaf to the root.

**Theorem.** A Merkle proof is `O(log n)` hashes and is sound: if
`verify` accepts, the leaf really is in the tree, because the verifier
recomputes the same root.

*Why it matters.* Detecting a change anywhere in an `n`-item file costs one
hash of the root. Proving one item is present costs `log n` hashes. Content
addressing, git, IPFS and blockchain headers are all this.

## Worked Example

Insert `"a"`, `"i"`, `"b"`, `"j"`, `"c"` into a table with 8 buckets using the
deliberately weak hash `h(k) = ord(k)`.

**Step 1.** `ord('a') = 97`, and `97 mod 8 = 1`. So `'a'` goes in bucket 1.
**Step 2.** `ord('i') = 105`, and `105 mod 8 = 1`. Bucket 1 is occupied, so we
chaining append: bucket 1 is now `a → i`.
**Step 3.** `ord('b') = 98`, `98 mod 8 = 2`. Bucket 2 gets `b`.
**Step 4.** `ord('j') = 106`, `106 mod 8 = 2`. Bucket 2 becomes `b → j`.
**Step 5.** `ord('c') = 99`, `99 mod 8 = 3`. Bucket 3 gets `c`.

Table state: `[1] a→i`, `[2] b→j`, `[3] c`, load factor `5/8 = 0.62`, longest
chain 2. Now insert `d`, `e`, `f`: after `f` the load factor is `8/8 = 1.0`,
which crossed 0.75, so the table doubles to 16 buckets and every key is
rehashed. Now `97 mod 16 = 1` and `105 mod 16 = 9`, so `a` and `i` finally
separate.

Two things to notice. First, chaining turned a would-be failure into a 2-element
list. Second, **resizing changes every bucket index**, because the modulus
changed — a key's location is not a property of the key, it is a property of
the key *and the current table size*. This is why `hash()` values must never be
persisted.

Now suppose we delete `a` from the original 8-bucket table. `get('i')` starts at
bucket 1, finds `EMPTY` where `a` used to be, and reports "not found" — `i` is
still there, one step further along. Open addressing has exactly this problem,
and the fix is a tombstone: a marker that means *keep probing, never match*.

## Runnable Code

### 1. Hash functions and how they spread keys

```python
"""Several small hash functions, and what they do to a table.

A good hash function has four jobs: be deterministic, be fast, spread keys
evenly across buckets, and be hard to invert.  These examples all satisfy the
first two and fail the third in instructive ways.
"""


def sum_hash(s: str, m: int) -> int:
    """The worst kind: position independent, so every anagram collides."""
    return sum(ord(c) for c in s) % m


def djb2(s: str, m: int) -> int:
    """Classic: h = h * 33 + c, starting from 5381."""
    h = 5381
    for ch in s:
        h = (h * 33 + ord(ch)) % m
    return h


def djb2_xor(s: str, m: int) -> int:
    """The same, but XOR instead of add."""
    h = 5381
    for ch in s:
        h = ((h * 33) ^ ord(ch)) % m
    return h


def fnv1a(s: str, m: int = 2**64) -> int:
    """FNV-1a: XOR the byte, then multiply by the FNV prime, mod a power of 2."""
    h = 0xCBF29CE484222325
    for byte in s.encode():
        h = ((h ^ byte) * 0x100000001B3) & (m - 1)
    return h


WORDS = """a an and are as at be but by for from has he in is it its of on that
to was were will with apple banana cherry date elderberry fig grape honeydew
kiwi lemon mango nectarine orange papaya quince raspberry strawberry
blueberry blackberry clementine dragonfruit""".split()

print(f"{len(WORDS)} keys, 64 buckets.  Occupied buckets and worst chain:")
for name, fn in [("sum", sum_hash), ("djb2", djb2), ("djb2-xor", djb2_xor),
                 ("fnv1a", lambda s, m: fnv1a(s) % m)]:
    b = [fn(w, 64) for w in WORDS]
    occupied = len(set(b))
    worst = max(b.count(i) for i in range(64))
    print(f"   {name:>9}: {occupied:>2} of 64 used, longest chain {worst}, "
          f"{len(WORDS) - occupied} collisions")
print()
print("Every function here collides about as often as chance predicts; the")
print("difference is *which* keys collide, and that decides whether the worst")
print("case stays small.")
print()

# Anagrams are the killer test for a position-independent hash.
PAIRS = [("abc", "cba"), ("salt", "slat"), ("listen", "silent"),
         ("dormitory", "dirty room")]
for name, fn in [("sum", sum_hash), ("djb2", djb2),
                 ("fnv1a", lambda s, m: fnv1a(s) % m)]:
    hits = sum(1 for a, b in PAIRS if fn(a, 64) == fn(b, 64))
    print(f"   {name:>9}: {hits} of {len(PAIRS)} anagram pairs collide mod 64")
print()

print("But djb2 degenerates if the modulus shares a factor with 33.  With")
print("m = 16 we get 33 mod 16 = 1, so djb2(s, 16) collapses to a shifted sum:")
print("   djb2(s, 16) =", [djb2(w, 16) for w in WORDS[:6]])
print("   sum(s, 16)  =", [sum_hash(w, 16) for w in WORDS[:6]])
offsets = {(djb2(w, 16) - sum_hash(w, 16)) % 16 for w in WORDS}
print("   the difference is the constant", offsets, "for every key")
print()
print("The other direction is worse.  With m = 33, the multiplier vanishes:")
print("   djb2(s, 33) = (h*33 + c) mod 33 = c mod 33, so only the LAST")
print("   character of the key matters.  WORDS[:6] end in",
      [w[-1] for w in WORDS[:6]])
print("   djb2(w, 33) =", [djb2(w, 33) for w in WORDS[:6]])
print("A multiplier coprime to the table size is not optional.")
print()

# Modulo a prime versus masking with a power of two.
print("Why power-of-two tables use a mask instead of a division:")
P, N = 1009, 2048
print(f"   x mod {N} equals x & {N - 1} whenever x is already below {N}, and the")
print("   mask is one machine instruction while a remainder is a division.")
print(f"   x mod {P} is a real remainder, and {N} mod {P} = {N % P}, so the table")
print("   size must itself be a power of two for the mask to be usable.")
print()

# Masking without mixing is fragile: keys with similar low bits all collide.
clustered = [(2 * i) & (N - 1) for i in range(8)]
mixed = [fnv1a(str(2 * i)) & (N - 1) for i in range(8)]
print("Masking without mixing is fragile:")
print(f"   the keys 0, 2, 4, ... 14 land on {clustered} if masked directly")
print(f"   the same keys through fnv1a land on {mixed}")
print("Real hashers therefore finish with a finalizer that pushes high bits")
print("down, for example murmur3's:")
MASK = (1 << 64) - 1


def mix64(h: int) -> int:
    h ^= h >> 33
    h = (h * 0xFF51AFD7ED558CCD) & MASK
    h ^= h >> 33
    return h


h = fnv1a("hello")
print(f"   fnv1a('hello')             = {h}")
print(f"   after the murmur3 finalizer = {mix64(h)}")
print(f"   and masked with 2047: fnv1a gives {h & (N - 1):>5}, "
      f"mixed gives {mix64(h) & (N - 1):>5}")
```

### 2. A hash table with separate chaining

```python
"""A hash table with separate chaining, built from scratch.

Every method is O(1) expected and O(n) worst case.  The worst case happens
when every key lands in one bucket, which is exactly when the adversary knows
your hash function.
"""

EMPTY = object()               # a sentinel distinct from None, so None is storable


class ChainingHashTable:
    def __init__(self, capacity: int = 8, hash_fn=None):
        self.capacity = capacity
        self.hash_fn = hash_fn or self._default_hash
        self.buckets: list[list] = [[] for _ in range(capacity)]
        self.size = 0

    @staticmethod
    def _default_hash(key) -> int:
        if isinstance(key, str):
            h = 0xCBF29CE484222325
            for byte in key.encode():
                h = ((h ^ byte) * 0x100000001B3) & ((1 << 64) - 1)
            return h
        return hash(key)

    def index(self, key) -> int:
        return self.hash_fn(key) % self.capacity

    def __len__(self):
        return self.size

    @property
    def load_factor(self) -> float:
        return self.size / self.capacity

    def put(self, key, value) -> None:
        bucket = self.buckets[self.index(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)     # update in place
                return
        bucket.append((key, value))
        self.size += 1
        if self.load_factor > 0.75:
            self.resize(self.capacity * 2)

    def get(self, key, default=None):
        for k, v in self.buckets[self.index(key)]:
            if k == key:
                return v
        return default

    def remove(self, key) -> bool:
        bucket = self.buckets[self.index(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return True
        return False

    def __contains__(self, key) -> bool:
        return any(k == key for k, _ in self.buckets[self.index(key)])

    def __getitem__(self, key):
        sentinel = object()
        v = self.get(key, sentinel)
        if v is sentinel:
            raise KeyError(key)
        return v

    def resize(self, new_capacity: int) -> None:
        old = self.buckets
        self.capacity = new_capacity
        self.buckets = [[] for _ in range(new_capacity)]
        self.size = 0
        for bucket in old:
            for k, v in bucket:
                self.buckets[self.index(k)].append((k, v))
                self.size += 1

    def longest_chain(self) -> int:
        return max(len(b) for b in self.buckets) if self.buckets else 0

    def show(self) -> str:
        rows = []
        for i, bucket in enumerate(self.buckets):
            if bucket:
                rows.append(f"   [{i:>2}] " +
                            " -> ".join(f"{k}" for k, _ in bucket))
        return "\n".join(rows) if rows else "   (empty)"


# Deliberately weak hash so the chains are visible: h('a') = ord('a') = 97.
t = ChainingHashTable(capacity=8, hash_fn=ord)
KEYS = ["a", "i", "b", "j", "c"]
for c in KEYS:
    t.put(c, ord(c))
print("A table of 8 buckets with hash = ord(character), holding "
      f"{KEYS}:")
print(t.show())
print(f"   size = {len(t)}, capacity = {t.capacity}, "
      f"load factor = {t.load_factor:.2f}, longest chain = {t.longest_chain()}")
print("   97 mod 8 = 1 and 105 mod 8 = 1, so 'a' and 'i' share bucket 1;")
print("   98 and 106 share bucket 2.  That is what chaining exists for.")
print()
for c in ["d", "e", "f"]:
    t.put(c, ord(c))
print(f"Three more puts took the load factor past 0.75, so the table grew to")
print(f"capacity {t.capacity} and every key was rehashed:")
print(t.show())
print(f"   size = {len(t)}, load factor = {t.load_factor:.2f}, "
      f"longest chain = {t.longest_chain()}")
print()

print("lookups:")
print("   get('c')      =", t.get("c"), " chr =", chr(t.get("c")))
print("   get('z')      =", t.get("z"), " (the default, meaning 'absent')")
print("   'b' in table  =", "b" in t, "  'z' in table =", "z" in t)
print("   t['d']        =", t["d"], " chr =", chr(t["d"]))
try:
    t["q"]
except KeyError as err:
    print("   t['q'] raised KeyError", err)
print()

print("update in place, so size does not change:")
before = len(t)
t.put("a", 1000)
print(f"   put('a', 1000) -> t['a'] = {t['a']}, size still {len(t)} "
      f"(was {before})")
print()

print("removal and the strong-hash table that resized on its own:")
t2 = ChainingHashTable(capacity=4)
for c in "abcde":
    t2.put(c, ord(c))
print(f"   after 5 puts with FNV: capacity = {t2.capacity} "
      f"(grew from 4 at load factor 0.75)")
print(t2.show())
print("   remove('a') ->", t2.remove("a"), "  remove('a') again ->",
      t2.remove("a"))
print("   'a' in table =", "a" in t2, " size =", len(t2))
print(t2.show())
print()

# Load factor and the cost of a lookup, measured rather than asserted.
import random  # noqa: E402

random.seed(5)
WORDS = [f"key-{i}" for i in range(4096)]
print("measured cost of get() as the table fills up:")
table = ChainingHashTable(capacity=16)
probes = 0
for n, key in enumerate(WORDS, start=1):
    table.put(key, n)
    if n in (16, 64, 256, 1024, 4096):
        print(f"   n = {n:>5}  capacity = {table.capacity:>5}  "
              f"load factor = {table.load_factor:.3f}  "
              f"longest chain = {table.longest_chain()}")
print()
print("Load factor alpha = size / capacity.  With chaining, a lookup walks")
print("one chain whose expected length is alpha, so the expected cost is")
print("O(1 + alpha).  Keeping alpha below about 0.75 is what makes the")
print("constant small; that is the whole reason a table ever resizes.")
```

### 3. A hash table with open addressing

```python
"""A hash table with open addressing and linear probing, built from scratch.

Open addressing stores every key directly in the array.  A collision is
resolved by moving to the next slot, which means a deletion cannot simply blank
the slot out -- that would cut the probe sequence in half and hide keys.  The
fix is a tombstone.
"""

EMPTY = None           # never used
TOMBSTONE = object()   # a deleted entry: keep probing, never a match


class OpenAddressingTable:
    def __init__(self, capacity: int = 8, hash_fn=None, max_load: float = 0.7):
        self.capacity = capacity
        self.hash_fn = hash_fn or self._default_hash
        self.max_load = max_load
        self.slots: list = [EMPTY] * capacity
        self.size = 0
        self.deleted = 0
        self.probes = 0              # total probes, for statistics

    @staticmethod
    def _default_hash(key) -> int:
        if isinstance(key, str):
            h = 0xCBF29CE484222325
            for byte in key.encode():
                h = ((h ^ byte) * 0x100000001B3) & ((1 << 64) - 1)
            return h
        return hash(key)

    def index(self, key) -> int:
        return self.hash_fn(key) % self.capacity

    @property
    def load_factor(self) -> float:
        return self.size / self.capacity

    def _find(self, key):
        """Return (slot, state) with state 'found', 'absent' or 'tomb'."""
        start = self.index(key)
        first_tomb = -1
        for step in range(self.capacity):
            self.probes += 1
            j = (start + step) % self.capacity
            entry = self.slots[j]
            if entry is EMPTY:
                # The key would have been stored at first_tomb if one was seen.
                return (first_tomb, "tomb") if first_tomb >= 0 else (j, "absent")
            if entry is TOMBSTONE:
                if first_tomb < 0:
                    first_tomb = j
                continue
            if entry[0] == key:
                return j, "found"
        return first_tomb, "tomb"

    def put(self, key, value) -> None:
        i, state = self._find(key)
        if state == "found":
            self.slots[i] = (key, value)
            return
        if state == "tomb":
            self.deleted -= 1
        else:
            self.size += 1
        self.slots[i] = (key, value)
        if self.size / self.capacity > self.max_load:
            self.resize(self.capacity * 2)

    def get(self, key, default=None):
        i, state = self._find(key)
        return self.slots[i][1] if state == "found" else default

    def remove(self, key) -> bool:
        i, state = self._find(key)
        if state != "found":
            return False
        self.slots[i] = TOMBSTONE
        self.size -= 1
        self.deleted += 1
        if self.deleted > self.capacity // 4:
            self.resize(self.capacity)      # clean up, do not shrink
        return True

    def resize(self, new_capacity: int) -> None:
        old = self.slots
        self.capacity = new_capacity
        self.slots = [EMPTY] * new_capacity
        self.size = 0
        self.deleted = 0
        for slot in old:
            if slot is not EMPTY and slot is not TOMBSTONE:
                self.put(slot[0], slot[1])

    def __contains__(self, key) -> bool:
        return self._find(key)[1] == "found"

    def longest_cluster(self) -> int:
        run = best = 0
        for slot in self.slots:
            run = 0 if slot is EMPTY else run + 1
            best = max(best, run)
        return best

    def show(self) -> str:
        rows = []
        for i, slot in enumerate(self.slots):
            if slot is EMPTY:
                rows.append(f"   [{i:>2}] .")
            elif slot is TOMBSTONE:
                rows.append(f"   [{i:>2}] X   <- deleted, keep probing")
            else:
                rows.append(f"   [{i:>2}] {slot[0]}")
        return "\n".join(rows)


# h(k) = k, so 3, 11 and 19 all want slot 3 in a table of 8.
t = OpenAddressingTable(capacity=8, hash_fn=lambda k: k)
print("8 slots, h(k) = k, inserting 3, 11, 19:")
for k in (3, 11, 19):
    t.put(k, f"v{k}")
print(t.show())
print("   3, 11 and 19 all hash to 3 and probe forward into 4, 5, 6.  That")
print("   cluster is the price of linear probing: collisions cause collisions.")
print()

print("deleting from the middle of a cluster needs a tombstone, not EMPTY:")
print("   remove(11) ->", t.remove(11))
print(t.show())
print("   19 is still reachable:", 19 in t, "=", t.get(19))
print("   Writing EMPTY at slot 4 instead would have made slot 5 look like the")
print("   end of 19's probe sequence, and get(19) would return None.")
print()

before = t.probes
t.put(11, "v11")
print(f"put(11) again reused the tombstone at slot 4: {t.probes - before} probes")
print("   19 is still reachable:", 19 in t, "=", t.get(19))
print()

# Primary clustering: how the cost grows with the load factor.
# The hash is Knuth's multiplicative one plus the murmur3 finalizer.  Shifting
# before masking is what makes it work: (k * odd) mod 2**12 is a bijection on
# 0..4095, so sequential keys would never collide and the measurement would be
# meaningless.  max_load is raised so the table never resizes during the test.
MASK64 = (1 << 64) - 1


def knuth(k: int) -> int:
    h = (k * 2654435761) & MASK64
    h ^= h >> 33
    h = (h * 0xFF51AFD7ED558CCD) & MASK64
    h ^= h >> 33
    return h >> 20          # top 12 bits, for the 4096-slot table below


print("linear probing measured on a 4096-slot table (no resizing):")
print(f"{'load factor':>12} {'probes/insert':>14} {'longest cluster':>16}")
CAP = 4096
for target in (0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.99):
    table = OpenAddressingTable(capacity=CAP, hash_fn=knuth, max_load=1.0)
    total = 0
    count = int(CAP * target)
    for i in range(1, count + 1):
        p0 = table.probes
        table.put(i, i)
        total += table.probes - p0
    print(f"{count / CAP:>12.2f} {total / count:>14.2f} "
          f"{table.longest_cluster():>16}")
print()
print("Linear probing degrades towards O(n) as the load factor approaches 1,")
print("because the average successful probe goes like 1/(1 - alpha).  Robin")
print("Hood hashing, cuckoo hashing and quadratic probing all attack this;")
print("the cheapest fix is simply to keep the load factor low.")
```

### 4. The birthday paradox, measured

```python
"""The birthday paradox: with n items dropped into m buckets, the chance of at
least one collision is about 1 - exp(-n^2 / (2m)).  A collision becomes likely
when n is about sqrt(m), not m.

This is why an n-bit hash is safe against preimage attack but only about
n/2 bits against collision attack.
"""
import math
import random


def collision_probability_by_count(n: int, m: int) -> float:
    """Exact: the probability that n independent draws from m buckets collide."""
    if n > m:
        return 1.0
    p = 1.0
    for k in range(n):
        p *= 1 - k / m          # kth draw must miss all k previous buckets
    return 1 - p


def threshold(m: int) -> float:
    """The n at which collisions reach 50 percent: sqrt(2 m ln 2)."""
    return math.sqrt(2 * m * math.log(2))


print(f"{'buckets m':>12} {'bits of m':>11} {'50% at n':>14} {'as sqrt(m)':>11}")
for bits in (8, 16, 32, 64, 128):
    m = 2**bits
    t = threshold(m)
    print(f"{m:>12,} {bits:>11} {t:>14.3g} {t / math.sqrt(m):>11.3f}")
print()
print("The 50 percent point sits at about 1.177 * sqrt(m).  So a 256-bit hash,")
print("which needs 2^256 work to invert, has collisions after about")
print(f"{2 ** 128:.3e} items.")
print()

print("exact probabilities for a table of 1000, against the approximation")
print(f"{'n':>4} {'exact':>9} {'1 - exp(-n^2/2m)':>18}")
for n in (1, 10, 30, 40, 50, 80, 100):
    exact = collision_probability_by_count(n, 1000)
    approx = 1 - math.exp(-n * n / (2 * 1000))
    print(f"{n:>4} {exact:>9.4f} {approx:>18.4f}")
print()
print(f"the approximation reaches 50 percent at n = {threshold(1000):.1f},")
print("which is where the number 1.177 * sqrt(m) comes from.")
print()

# A simulation, so the effect is visible rather than merely tabulated.
random.seed(2024)
M = 366
print(f"simulation: 2000 independent runs, table of {M} buckets")
print(f"{'items n':>9} {'probability of a collision':>26}")
for n in (10, 20, 30, 40, 50, 100):
    hits, trials = 0, 2000
    for _ in range(trials):
        seen = set()
        for _ in range(n):
            b = random.randrange(M)
            if b in seen:
                hits += 1
                break
            seen.add(b)
    print(f"{n:>9} {hits / trials:>26.3f}")
print()
print(f"   sqrt({M}) = {math.sqrt(M):.1f}, so the transition really does sit near")
print("   the square root of the table size, not near the table size.")
print()

print("Consequences for real systems:")
print(f"   a 32-bit CRC covers 2^32 values; 50% collision at n = {2 ** 16:.0f} items")
print(f"   a 64-bit hash; 50% collision at n = {2 ** 32:.3e} items")
print(f"   a 128-bit hash; 50% collision at n = {2 ** 64:.3e} items")
print(f"   SHA-256; 50% collision at n = {2 ** 128:.3e} items")
print()
print("But the *preimage* cost is 2^bits, not 2^(bits/2).  So an attacker who")
print("needs to invert a 256-bit hash works 2^128 times harder than one who")
print("merely needs two inputs with the same hash.  That factor of two in the")
print("exponent is the most important number in hash security.")
```

### 5. Table hashes versus cryptographic hashes

```python
"""Avalanche, and why a good table hash is not a cryptographic hash.

A cryptographic hash must satisfy three requirements that an ordinary hash
function never promises:
  * preimage resistance -- you cannot find m from H(m)
  * second-preimage resistance -- you cannot find m' != m with H(m') = H(m)
  * collision resistance -- you cannot find any m1 != m2 with equal hashes

The reason FNV-1a or Python's built-in hash() do not qualify is not their
avalanche.  It is the width of their output.
"""
import hashlib
import random


def fnv1a(data: bytes) -> int:
    h = 0xCBF29CE484222325
    for byte in data:
        h = ((h ^ byte) * 0x100000001B3) & ((1 << 64) - 1)
    return h


def avalanche(h1: int, h2: int, bits: int = 64) -> float:
    return bin(h1 ^ h2).count("1") / bits


random.seed(2)
sha_changed, fnv_changed = [], []
for _ in range(500):
    msg = bytes(random.randrange(256) for _ in range(16))
    pos, bit = random.randrange(16), random.randrange(8)
    other = bytearray(msg)
    other[pos] ^= 1 << bit
    a = hashlib.sha256(msg).digest()
    b = hashlib.sha256(bytes(other)).digest()
    sha_changed.append(avalanche(int.from_bytes(a, "big"),
                                 int.from_bytes(b, "big"), 256) * 256)
    fa, fb = fnv1a(msg), fnv1a(bytes(other))
    fnv_changed.append(avalanche(fa, fb, 64) * 64)

print("1. The avalanche effect.  About half the output bits should flip when")
print("   one input bit flips.  Averaged over 500 random single-bit flips:")
print(f"      SHA-256 changes {sum(sha_changed) / 500:.1f} of 256 bits")
print(f"      FNV-1a  changes {sum(fnv_changed) / 500:.1f} of 64 bits")
print("   Both are fine for a hash table.  Avalanche is necessary but nowhere")
print("   near sufficient.")
print()

print("2. Python's built-in hash() is not a cryptographic hash at all.")
print(f"   hash('abc') = {hash('abc')}   (differs on every process start)")
print(f"   hash(12345) = {hash(12345)}   (it is the integer itself)")
print("   Small integers hash to themselves, so a table keyed on ints 0..n")
print("   degenerates into a plain array: no collisions, and no scrambling")
print("   either, which means every bucket index is guessable.  Never use")
print("   hash() for a signature, a password, or a persistent cache key.")
print()

print("3. Length extension.  A Rabin-style polynomial hash (the one from")
print("   Lesson 110) has H(m) = sum c_i * B^i (mod M), so")
print()
print("       H(m || extra) = H(m) * B^len(extra) + H(extra)   (mod M)")
print()
print("   An attacker who knows only H(m) can compute H of any longer message.")
print("   Here is the attack on a naive MAC that appends the digest:")
B, M = 257, 2**61 - 1


def rabin(data: bytes) -> int:
    h = 0
    for byte in data:
        h = (h * B + byte) % M
    return h


secret = b"user=bob;admin=0"
leaked = rabin(secret)                    # all the attacker is given
extra = b"\x00" * 63 + b"admin=1"
forged = (leaked * pow(B, len(extra), M) + rabin(extra)) % M
real = rabin(secret + extra)
print(f"   secret   = {secret!r}")
print(f"   leaked H = {leaked}")
print(f"   extra    = {extra[:12]!r}... ({len(extra)} bytes)")
print(f"   real   H(secret || extra) = {real}")
print(f"   forged from the digest alone = {forged}")
print(f"   they match: {real == forged}")
print()
print("   SHA-1 and SHA-256 share the weakness, since both are Merkle-Damgard")
print("   constructions.  HMAC fixes it by hashing the key twice and never")
print("   exposing the inner state; SHA-3 avoids the structure with a sponge.")
print()

print("4. Domain separation: label what the hash is for.")
a = hashlib.sha256(b"transfer:1000:alice->bob").hexdigest()[:16]
b = hashlib.sha256(b"login:bob").hexdigest()[:16]
print(f"   sha256('transfer:1000:...') = {a}")
print(f"   sha256('login:bob')         = {b}")
print("   Without a prefix an attacker can move a message from one protocol")
print("   into the other, which is a real attack on unversioned protocols.")
```

### 6. Merkle trees and content addressing

```python
"""Merkle trees: what a hash is for when it is not looking things up.

A Merkle tree hashes pairs of nodes bottom-up.  It gives three things a flat
hash cannot:
  * a change anywhere produces a completely different root;
  * a proof that one leaf is in the tree costs O(log n) hashes instead of O(n);
  * a proof that two leaves are different costs the same.

Git objects, IPFS, Merkle-Damgard file systems, and blockchain transactions all
use exactly this.
"""
import hashlib


def h(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


class MerkleTree:
    def __init__(self, leaves: list[bytes]):
        self.leaves = list(leaves)
        # pad to a power of two; duplicating the last real leaf would break
        # proofs, so use a distinct filler
        n = 1
        while n < len(self.leaves):
            n *= 2
        self.leaves += [b"\x00" * 32] * (n - len(self.leaves))
        # layer 0 holds the hashes of the leaves, not the leaves themselves
        self.layers: list[list[bytes]] = [[h(leaf) for leaf in self.leaves]]
        level = self.layers[0]
        while len(level) > 1:
            level = [h(level[i] + level[i + 1]) for i in range(0, len(level), 2)]
            self.layers.append(level)

    @property
    def root(self) -> bytes:
        return self.layers[-1][0]

    def proof(self, index: int) -> list[tuple[bytes, str]]:
        """The sibling hashes needed to recompute the root from leaf `index`.

        The side recorded is the side *our* node sits on, because a parent is
        always h(left || right): an even index is the left child.
        """
        proof = []
        i = index
        for layer in self.layers[:-1]:
            proof.append((layer[i ^ 1], "left" if i % 2 == 0 else "right"))
            i //= 2
        return proof

    def verify(self, index: int, leaf: bytes, proof) -> bool:
        node = h(leaf)
        for sibling, side in proof:
            node = h(sibling + node) if side == "right" else h(node + sibling)
        return node == self.root


BLOCKS = [f"block {i}".encode() for i in range(8)]
tree = MerkleTree(BLOCKS)
print(f"{len(BLOCKS)} blocks, {len(tree.layers)} layers, "
      f"height = log2(8) = 3")
for depth, layer in enumerate(tree.layers):
    print(f"   layer {depth}: {len(layer)} node(s), "
          f"first = {layer[0].hex()[:16]}...")
print(f"root = {tree.root.hex()}")
print()

print("verification: prove block 5 is in the tree")
p = tree.proof(5)
for digest, side in p:
    print(f"   sibling {digest.hex()[:16]}...  we sit on the {side}")
print(f"   verify(5, {BLOCKS[5]!r}, proof) = {tree.verify(5, BLOCKS[5], p)}")
print(f"   proof size = {len(p)} hashes = log2({len(BLOCKS)}), so membership is")
print("   proven in O(log n) hashes rather than O(n).")
print()

print("change one byte of one block and the root changes completely:")
tampered = list(BLOCKS)
tampered[5] = b"block 5!"
root2 = MerkleTree(tampered).root
print(f"   original root = {tree.root.hex()[:32]}...")
print(f"   tampered root = {root2.hex()[:32]}...")
print(f"   roots equal: {tree.root == root2}")
print()

print("and the old proof no longer verifies:")
bad = tree.verify(5, b"block 5!", p)
print(f"   verify(5, b'block 5!', old proof) = {bad}")
print()

print("This is content addressing: the address of a file *is* its hash, so the")
print("hash detects any change anywhere in the file.  That property is why")
print("git can trust a tree of hashes, and why a blockchain can use a chain of")
print("them as a tamper-evident log.")
print()
print("A different structure shares the name: the Merkle-Damgard")
print("construction inside SHA-2, where the compression function is chained")
print("block by block.  The length-extension weakness above belongs to that")
print("structure, not to tree-shaped Merkle trees.")
```

## Common Mistakes

**Wrong.** Writing `EMPTY` when deleting from an open-addressing table.

```python
def remove_wrong(slots, key, cap, hash_fn):
    i = hash_fn(key) % cap
    while slots[i] is not None and slots[i][0] != key:
        i = (i + 1) % cap
    slots[i] = None          # a hole in the middle of a probe sequence
```

**Right.**

```python
TOMBSTONE = object()


def remove_right(slots, key, cap, hash_fn):
    i = hash_fn(key) % cap
    while slots[i] is not None and slots[i] is not TOMBSTONE \
            and slots[i][0] != key:
        i = (i + 1) % cap
    if slots[i] is not None and slots[i][0] == key:
        slots[i] = TOMBSTONE
        return True
    return False


def demo():
    slots = [None] * 8
    slots[3], slots[4], slots[5] = (3, 3), (11, 11), (19, 19)

    def label(s):
        if s is None:
            return "."
        return "X" if s is TOMBSTONE else str(s[0])

    print("   before removal:", [label(s) for s in slots])
    remove_right(slots, 11, 8, lambda k: k)
    print("   after removal: ", [label(s) for s in slots])
    i = 19 % 8
    while slots[i] is None:
        i = (i + 1) % 8
    print("   19 found by probing forward to slot", i)


demo()
```

Why the wrong version is tempting: it reuses the one sentinel you already have,
and every test that inserts and removes a *single* key passes. It only breaks
when a later key's probe path crossed the deleted slot — which is exactly the
situation linear probing creates.

---

**Wrong.** Storing `hash(key)` and calling it later to find the key.

```python
FILES = ["a.txt", "b.txt", "c.txt"]

LOCATIONS = {}
for path in FILES:
    # wrong: PYTHONHASHSEED randomises string hashing per process, so this
    # map is meaningless after a restart
    LOCATIONS[hash(path)] = path
print("built-in hash() values, all process-local and untrustworthy:")
print("  ", {hash(p): p for p in FILES})
print("   hash('a.txt') in this process =", hash("a.txt"))
```

**Right.**

```python
import hashlib

FILES = ["a.txt", "b.txt", "c.txt"]

LOCATIONS = {}
for path in FILES:
    digest = hashlib.blake2b(path.encode(), digest_size=16).digest()
    LOCATIONS[digest] = path
print("blake2b digests are stable across processes, runs and Python versions:")
for path in FILES:
    d = hashlib.blake2b(path.encode(), digest_size=16).digest()
    print(f"   {path} -> {d.hex()}")
print("   and re-running this script prints exactly the same values.")
```

Why the wrong version is tempting: it halves the work and looks like an
optimisation. But Python randomises string hashing per process by default
(`PYTHONHASHSEED`), so the map is garbage after a restart; small integers hash
to themselves; and resizing a table changes every index. A digest is stable.

---

**Wrong.** Using a CRC or a table hash where a security control is needed.

```python
import zlib

# 32 bits of public, invertible checksum: fine for a zip, useless as security
token = zlib.crc32(b"admin=1")
print(f"   crc32(b'admin=1') = {token:#010x}   (32 bits, no key, no randomness)")
```

**Right.**

```python
import hashlib
import hmac
import secrets

key = secrets.token_bytes(32)
token = hmac.new(key, b"admin=1", hashlib.sha256).hexdigest()
same = hmac.new(key, b"admin=1", hashlib.sha256).hexdigest()
other = hmac.new(key, b"admin=2", hashlib.sha256).hexdigest()
print(f"   hmac-sha256 over a random {len(key)}-byte key:")
print(f"      token for 'admin=1' = {token[:32]}...")
print(f"      constant-time compare passes: "
      f"{hmac.compare_digest(token, same)}")
print(f"      a different message gives a different token: "
      f"{token != other}")
```

Why the wrong version is tempting: `crc32` is called a "hash" and it is fast,
well tested, and in the standard library. But `2^32` work finds a CRC-32
collision, and a birthday attack needs `2^16 = 65,536` random messages — so an
attacker builds one in seconds. Randomness from `random` instead of `secrets`
compounds it, since Mersenne Twister output is recoverable from 624 values.

---

## Exercises and Solutions

**[ ] Exercise 1 —** Write a chaining hash table that counts how many insertions
hit a non-empty bucket, resizes at a load factor of 0.75, and reports its load
factor and longest chain. Insert 2000 keys and check every lookup against the
built-in `dict`.

<details>
<summary>Solution</summary>

```python
import random


class Chaining:
    """Separate chaining with statistics, checked against the built-in dict."""

    def __init__(self, capacity=8, max_load=0.75):
        self.capacity = capacity
        self.max_load = max_load
        self.buckets = [[] for _ in range(capacity)]
        self.size = 0
        self.collisions = 0        # puts that found a non-empty bucket

    def index(self, key):
        return hash(key) % self.capacity

    def put(self, key, value):
        bucket = self.buckets[self.index(key)]
        if bucket:
            self.collisions += 1
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.size += 1
        if self.size / self.capacity > self.max_load:
            self.resize(self.capacity * 2)

    def get(self, key, default=None):
        for k, v in self.buckets[self.index(key)]:
            if k == key:
                return v
        return default

    def resize(self, new_capacity):
        old = self.buckets
        self.capacity = new_capacity
        self.buckets = [[] for _ in range(new_capacity)]
        self.size = 0
        self.collisions = 0
        for bucket in old:
            for k, v in bucket:
                self.put(k, v)

    def longest_chain(self):
        return max(len(b) for b in self.buckets)


random.seed(31)
t = Chaining()
d = {}
for i in range(2000):
    k = f"k{i}"
    t.put(k, i)
    d[k] = i
    assert t.get(k) == d[k]
print(f"2000 keys: capacity {t.capacity}, size {t.size}, "
      f"load factor {t.size / t.capacity:.3f}")
print(f"collisions during construction (counting rehashes): {t.collisions}")
print(f"longest chain: {t.longest_chain()}")
print("every key agrees with the built-in dict")

# The Poisson picture: the longest chain among m buckets of mean alpha is
# about ln(alpha) / ln(1 - alpha).
import math

alpha = t.size / t.capacity
expected = math.log(alpha) / math.log(1 - alpha)
print()
print(f"with alpha = {alpha:.3f} the predicted longest chain is about "
      f"{expected:.2f}")
print(f"measured: {t.longest_chain()}")
print("The prediction is asymptotic and slightly low at this size, but the")
print("shape is right: the longest chain grows like ln(n)/ln(ln(n)), not like n.")
```

</details>

**[ ] Exercise 2 —** Implement an open-addressing table with quadratic probing
(`0, +1, -1, +4, -4, +9, -9, ...`) and correct deletion using backward-shift
deletion. Then measure, against linear probing, the average probes per insert
and the longest run of occupied slots at load factors from 0.5 to 0.99.

<details>
<summary>Solution</summary>

```python
M64 = (1 << 64) - 1
EMPTY = None


def home(k, cap):
    """A mixing hash, so consecutive keys do not land in consecutive slots."""
    h = (k * 2654435761) & M64
    h ^= h >> 33
    h = (h * 0xFF51AFD7ED558CCD) & M64
    h ^= h >> 33
    return h % cap


def linear(start, cap, i):
    """The i-th probe of linear probing is simply start + i."""
    return (start + i) % cap


def quadratic(start, cap, i):
    """Probe offsets 0, +1, -1, +4, -4, +9, -9, ..."""
    if i == 0:
        return start % cap
    sign = 1 if i % 2 else -1
    return (start + sign * (((i + 1) // 2) ** 2)) % cap


def build(probe, target_load, cap=1024):
    slots = [EMPTY] * cap
    n = int(cap * target_load)
    probes = 0
    for k in range(1, n + 1):
        start = home(k, cap)
        i = 0
        while slots[probe(start, cap, i)] is not None:
            i += 1
            probes += 1
            if i > 2 * cap:
                raise RuntimeError("probe sequence found no free slot")
        slots[probe(start, cap, i)] = k
    return slots, probes / n


def longest_run(slots):
    best = run = 0
    for s in slots:
        run = 0 if s is EMPTY else run + 1
        best = max(best, run)
    return best


print(f"{'load':>6} {'linear probes':>15} {'quadratic probes':>18} "
      f"{'lin longest run':>17} {'quad longest run':>18}")
for load in (0.5, 0.7, 0.85, 0.95, 0.99):
    lin, lp = build(linear, load)
    quad, qp = build(quadratic, load)
    print(f"{load:>6.2f} {lp:>15.2f} {qp:>18.2f} {longest_run(lin):>17} "
          f"{longest_run(quad):>18}")
print()
print("Linear probing forms one long cluster; the longest run grows with the")
print("load factor.  Quadratic probing spreads keys out, so its runs stay")
print("shorter even when the probe counts are comparable.")
print()


def build_rw(target_load, cap=1024):
    slots = [EMPTY] * cap
    for k in range(1, int(cap * target_load) + 1):
        start = home(k, cap)
        i = 0
        while slots[quadratic(start, cap, i)] is not None:
            i += 1
            if i > 2 * cap:
                raise RuntimeError("probe sequence found no free slot")
        slots[quadratic(start, cap, i)] = k
    return slots


def remove_rw(slots, key, cap=1024):
    start = home(key, cap)
    i = 0
    while slots[quadratic(start, cap, i)] != key:
        i += 1
        if i > 2 * cap:
            raise KeyError(key)
    hole = quadratic(start, cap, i)
    slots[hole] = EMPTY
    j = i + 1
    while True:
        nxt = quadratic(start, cap, j)
        if slots[nxt] is EMPTY:
            return
        h_start = home(slots[nxt], cap)
        d = (nxt - hole) % cap
        h = (h_start - hole) % cap
        if 0 < h <= d:
            slots[hole] = slots[nxt]
            slots[nxt] = EMPTY
            hole = nxt
        j += 1
        if j > 2 * cap:
            raise RuntimeError("scan ran away")


slots = build_rw(0.7)
n = sum(1 for s in slots if s is not None)
victim = next(s for s in slots if s is not None)
print(f"built a 0.7-load table with {n} keys; removing {victim}")
remove_rw(slots, victim)
missing = [k for k in range(1, n + 1) if k != victim and k not in slots]
print(f"keys still present: {n - 1 - len(missing)} of {n - 1}")
print(f"keys lost: {missing if missing else 'none'}")
assert not missing
lost = []
for k in range(1, n + 1):
    if k == victim:
        continue
    i = 0
    while slots[quadratic(home(k, 1024), 1024, i)] != k:
        i += 1
        if i > 2 * 1024:
            lost.append(k)
            break
print(f"keys unreachable from their home slot: {lost if lost else 'none'}")
print("backward-shift deletion lost nothing and left no tombstones.")
```

</details>

**[ ] Exercise 3 —** Using the exact birthday formula, find the smallest `n`
for which the collision probability exceeds 0.5 in a table of `2^16` buckets.
Then simulate the same thing with 3000 trials at `n = 100, 200, 300, 400, 1000`
and explain in two sentences why a 32-bit CRC is adequate for a zip file but
inadequate as a security control.

<details>
<summary>Solution</summary>

```python
import math
import random


def exact_collision_probability(n, m):
    if n > m:
        return 1.0
    p = 1.0
    for k in range(n):
        p *= 1 - k / m
    return 1 - p


m = 2**16
lo, hi = 1, m
while lo < hi:                      # binary search for the first n over 0.5
    mid = (lo + hi) // 2
    if exact_collision_probability(mid, m) > 0.5:
        hi = mid
    else:
        lo = mid + 1
print(f"table of m = 2^16 = {m} buckets")
print(f"first n with collision probability above 0.5: {lo}")
print(f"   exact  = {exact_collision_probability(lo, m):.4f}")
print(f"   at n-1 = {exact_collision_probability(lo - 1, m):.4f}")
print(f"   sqrt(2 * m * ln 2) = {math.sqrt(2 * m * math.log(2)):.1f}")
print()

random.seed(7)
M = 2**16
print("simulation with m = 2^16, 3000 trials per row")
print(f"{'n':>7} {'simulated':>10} {'exact':>8}")
for n in (100, 200, 300, 400, 1000):
    hits = 0
    for _ in range(3000):
        seen = bytearray(M)
        for _ in range(n):
            b = random.randrange(M)
            if seen[b]:
                hits += 1
                break
            seen[b] = 1
    print(f"{n:>7} {hits / 3000:>10.3f} {exact_collision_probability(n, M):>8.3f}")
print()
print("So a 16-bit checksum is already 50% likely to collide after about 300")
print("items.  A 32-bit CRC needs about 77,000 items; a 64-bit value about")
print(f"{2 ** 32:.3e}; a 128-bit value about {2 ** 64:.3e}.")
print()
print("This is why `zlib.crc32` is fine for a zip file and useless as a")
print("security control: a CRC-32 collision takes about 2^32 work, or minutes")
print("on a GPU, while SHA-256 collisions are out of reach entirely.")
```

The birthday bound says collisions arrive at `n ≈ 1.177 √m`, and `√(2^16) = 256`
— so the answer is a few hundred, not a few tens of thousands. A zip file is
trusted to be handed to you intact, so an accidental collision at 1/2 over 65,536
entries would be a problem worth catching; but an adversary who *wants* a
collision just runs the birthday search themselves.

</details>

**[ ] Exercise 4 —** Measure the avalanche of FNV-1a, then of FNV-1a followed
by the murmur3 finalizer, over 20,000 random single-bit flips, both on the
whole 64-bit output and on the low 16 bits. Then run a birthday collision
search on SHA-256 truncated to 8, 12, 16 and 20 bits, and use the results to
explain in three sentences why avalanche is not what makes a hash
cryptographic.

<details>
<summary>Solution</summary>

```python
import hashlib
import random
import time


def fnv1a(data: bytes) -> int:
    h = 0xCBF29CE484222325
    for byte in data:
        h = ((h ^ byte) * 0x100000001B3) & ((1 << 64) - 1)
    return h


M64 = (1 << 64) - 1


def mix64(h: int) -> int:
    """The murmur3 finalizer, used as a diffusion step."""
    h ^= h >> 33
    h = (h * 0xFF51AFD7ED558CCD) & M64
    h ^= h >> 33
    return h


def avalanche(h1: int, h2: int, bits: int = 64) -> float:
    return bin(h1 ^ h2).count("1") / bits


random.seed(9)
trials = 20000
rows = []
for name, fn in [("fnv1a", fnv1a),
                 ("fnv1a + mix64", lambda d: mix64(fnv1a(d)))]:
    whole, low16 = [], []
    for _ in range(trials):
        msg = bytes(random.randrange(256) for _ in range(8))
        pos, bit = random.randrange(8), random.randrange(8)
        other = bytearray(msg)
        other[pos] ^= 1 << bit
        a, b = fn(msg), fn(bytes(other))
        whole.append(avalanche(a, b))
        low16.append(avalanche(a & 0xFFFF, b & 0xFFFF, 16))
    rows.append((name, sum(whole) / trials, sum(low16) / trials))

print(f"{trials} random single-bit flips; ideal avalanche = 0.5")
print(f"{'':>15} {'all 64 bits':>13} {'low 16 bits':>13}")
for name, whole, low16 in rows:
    print(f"{name:>15} {whole:>13.4f} {low16:>13.4f}")
print()
print("FNV-1a sits a little under the ideal; the murmur3 finalizer brings it")
print("to the ideal.  Both are perfectly adequate for a hash table, and this")
print("measurement is NOT the reason FNV-1a is unsuitable for security.")
print()

# The real reason is cost: a birthday search takes about 2^(bits/2) work.
def birthday_collision(bits, h_fn, tries):
    mask = (1 << bits) - 1
    seen = {}
    t0 = time.perf_counter()
    for i in range(tries):
        h = h_fn(str(i).encode()) & mask
        if h in seen:
            return i, time.perf_counter() - t0
        seen[h] = i
    return -1, time.perf_counter() - t0


def sha(d: bytes) -> int:
    return int.from_bytes(hashlib.sha256(d).digest()[:8], "big")


print("collision search, truncated SHA-256, measured on this machine")
print(f"{'bits kept':>10} {'predicted 2^(b/2)':>19} {'tries used':>14} "
      f"{'seconds':>9}")
for bits, tries in ((8, 2000), (12, 40000), (16, 800000), (20, 2000000)):
    t, secs = birthday_collision(bits, sha, tries)
    print(f"{bits:>10} {2 ** (bits / 2):>19.0f} {t if t > 0 else '> ' + f'{tries:,}':>14} "
          f"{secs:>9.3f}")
print()
print("Each extra bit kept roughly squares the trials needed, which is the")
print("birthday bound 2^(bits/2) in action.  Extrapolating:")
print(f"   128 bits of SHA-256 -> about 2^64 = {2 ** 64:.2e} trials")
print(f"   256 bits of SHA-256 -> about 2^128 = {2 ** 128:.2e} trials")
print()
t, secs = birthday_collision(16, fnv1a, 800000)
print(f"the same 16-bit search on FNV-1a found a collision after {t:,} trials "
      f"in {secs:.4f} s")
print()
print("So the three requirements cost different amounts:")
print("   preimage resistance       -- 2^bits work: how hard to invert")
print("   second-preimage resistance -- 2^bits work, with a known input")
print("   collision resistance       -- 2^(bits/2) work: the birthday bound")
print("FNV-1a emits 64 bits, so its collision cost is 2^32 -- easy.  SHA-256")
print("emits 256, so its collision cost is 2^128 -- not.  The output width is")
print("the whole difference; the avalanche numbers are a distraction.")
```

</details>

**Challenge** — Implement **cuckoo hashing**: two tables, two independent hash
functions, and an insert that kicks out the occupant and retries. Insert 2000
keys into two tables of 1024 slots, show that every lookup succeeds, and then
compare its *worst-case* probe count against the linear-probing table from the
lesson. Explain in two sentences why the worst case matters more than the
average in a hash-flooding attack.

<details>
<summary>Solution</summary>

```python
EMPTY = None
MAX_KICKS = 100
M64 = (1 << 64) - 1


def mix(x: int) -> int:
    """A cheap avalanche mixer.  Two rounds give two independent hashes."""
    x = (x * 0x9E3779B97F4A7C15) & M64
    x ^= x >> 29
    return x


def h1(k: int, cap: int) -> int:
    return mix(k * 2 + 0x1) % cap


def h2(k: int, cap: int) -> int:
    return mix(k * 2 + 0x2) % cap


class Cuckoo:
    """Two tables, two hashes, insert by kicking out the occupant.

    When a kick sequence closes a cycle the table cannot hold the key, so the
    whole table is rehashed at twice the capacity.  The displaced key must be
    carried across too: the failed insert has already overwritten a slot, so
    there is nothing to roll back to.
    """

    def __init__(self, cap: int = 1024):
        self.cap = cap
        self.tables = [[EMPTY] * cap for _ in range(2)]
        self.size = 0
        self.max_kicks = 0
        self.grows = 0

    def _place(self, key):
        """Insert key, kicking out occupants.  On failure, return the key that
        got displaced last, which is now nowhere in the table."""
        table = 0
        for kick in range(MAX_KICKS):
            slot = (h1 if table == 0 else h2)(key, self.cap)
            victim = self.tables[table][slot]
            self.tables[table][slot] = key
            self.max_kicks = max(self.max_kicks, kick + 1)
            if victim is EMPTY:
                self.size += 1
                return None
            key, table = victim, 1 - table
        return key          # the cycle closed; this key is displaced

    def get(self, key):
        return (self.tables[0][h1(key, self.cap)] == key
                or self.tables[1][h2(key, self.cap)] == key)

    def keys(self):
        return [k for t in self.tables for k in t if k is not EMPTY]

    def grow(self, extra):
        saved = self.keys() + extra
        self.cap *= 2
        self.tables = [[EMPTY] * self.cap for _ in range(2)]
        self.size = 0
        self.grows += 1
        for k in saved:
            assert self._place(k) is None, "failed after doubling, which is a bug"

    def put(self, key):
        if self.get(key):
            return
        leftover = self._place(key)
        if leftover is not None:
            self.grow([leftover])


def measure_linear(n_keys, cap):
    """The same keys in a linear-probing table of the same total capacity."""
    slots = [EMPTY] * cap
    worst = 0
    for k in range(1, n_keys + 1):
        start = h1(k, cap)
        i = 0
        while slots[(start + i) % cap] is not EMPTY:
            i += 1
        worst = max(worst, i + 1)
        slots[(start + i) % cap] = k
    return worst


NKEYS, CAP = 2000, 1024
c = Cuckoo(cap=CAP)
for k in range(1, NKEYS + 1):
    c.put(k)
print(f"cuckoo: {NKEYS} keys, starting from two tables of {CAP}")
print(f"   final capacity {c.cap} per table, grows: {c.grows}")
print(f"   combined load factor {c.size / (2 * c.cap):.3f}")
print(f"   worst kick sequence during construction: {c.max_kicks}")
missing = [k for k in range(1, NKEYS + 1) if not c.get(k)]
print(f"   keys not found by lookup: {len(missing)}")
assert not missing

lin = measure_linear(NKEYS, 2 * CAP)
print(f"linear probing on one {2 * CAP}-slot table: worst probe length {lin}")
print(f"cuckoo hashing: worst kick sequence length {c.max_kicks}")
print()
print("The average is similar; the worst case is not.  A linear-probing table")
print("has a single degenerate configuration -- every key in one long cluster --")
print("and an attacker who can construct keys hashing into it makes every")
print("operation O(n), which is a denial of service.  Cuckoo hashing has no")
print("such configuration, because a key lives in two tables and an attacker")
print("cannot force collisions in both at once.")
```

</details>

## Summary

- A hash function maps keys to bucket indices; collisions are unavoidable, and
  a table hash needs only to be deterministic, fast, and uniform.
- A good table hash needs no inversion resistance — collisions are handled, not
  attacked — but it does need to mix high bits into low ones, because the bucket
  index comes from the low bits of the output.
- Separate chaining makes a lookup cost `Θ(1 + α)`; open addressing with linear
  probing costs `Θ(1 / (1 − α))`. Capping `α` and resizing is what keeps both
  `O(1)`, and the amortised analysis in
  [Lesson 81](../part06_algorithms_math/81_amortized_analysis.md) proves the
  doubling strategy totals `Θ(n)`.
- Open addressing cannot delete with a plain `EMPTY`, because the hole breaks
  later keys' probe sequences. The fix is a tombstone, and quadratic probing
  needs backward-shift deletion instead.
- A key's location is a property of the key *and the current table size*, so
  `hash()` values must never be persisted across processes or resizes.
- The birthday paradox says collisions arrive at `n ≈ 1.177 √m`, giving `2^(bits/2)`
  collision work against `2^bits` preimage work. That factor of two is the most
  important number in hash security.
- Cryptographic hashes need preimage, second-preimage and collision resistance,
  avalanche, no length extension (HMAC or SHA-3), and domain separation. FNV-1a
  and Python's `hash()` fail because their outputs are too narrow, not because
  their mixing is poor.
- Merkle trees turn a hash into a tamper-evident structure: one root detects any
  change anywhere, and one `log n` proof shows one item is present. This is what
  content addressing, git and blockchains are built from.

## Next

[113 — Error-Correcting Codes](113_error_correcting_codes.md) turns the picture
around. So far a hash detects corruption but cannot repair it. Error-correcting
codes add just enough carefully chosen redundancy to *undo* errors, introduces
minimum distance as the quantity that decides how many errors are correctable,
and shows why QR codes, CDs, ECC memory and every deep-space probe use exactly
this machinery.
