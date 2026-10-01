# 27 — Trees and Spanning Trees

**Part**: part02_discrete_combinatorics · **Prerequisites**: 26 · **Time**: 45 min

---

## In Plain Words

A **tree** is a graph with no loops and exactly one way to get from any vertex to
any other. That "exactly one way" is the whole content of the word. It sounds like
a small constraint, and it makes trees the most useful and most overused structure
in computer science.

The usefulness comes from the way the constraint propagates. A connected graph on
n vertices always has at least n − 1 edges. A graph with exactly n − 1 edges and no
cycle is a tree. A tree on n vertices has a longest path of at most n − 1 edges and
a longest *rooted* path of at most log n if you keep it balanced. That is the
whole reason heaps, B-trees, tries, and binary search trees run in logarithmic time:
they are trees, and the tree bounds are what you are paying for.

Two algorithmic families live in this lesson and they solve different problems.
**Shortest paths** minimise the cost of getting from one place to another while
visiting as few vertices as possible — Dijkstra's algorithm. **Minimum spanning
trees** minimise the cost of connecting *every* place to *every other* place, and
Dijkstra does not solve that at all, because a shortest path can be far more
expensive in aggregate than a global set of cheap links. Kruskal and Prim solve it,
and Kruskal needs the union–find from
[Lesson 25](25_relations_and_equivalence_classes.md).

The union of the two lessons is worth stating: a spanning tree is a *global*
optimum, a shortest path is a *local* one, and confusing them is the most common
error in this topic.

## Why Computer Science Cares

- **B-trees are how databases store data.** Every index in MySQL, PostgreSQL,
  SQLite, and every other relational database is a B-tree. The reason is the
  height bound: with a fan-out of 500 and a page size of 4 KB, a three-level tree
  holds roughly 125 million rows, so almost every lookup is three disk reads. This
  is the single most consequential place where a tree invariant shows up in
  production.
- **Tries back autocomplete and routing.** A trie is a tree whose edges are
  characters; lookup is O(length of the key) with no comparison at all, and prefix
  queries fall out for free. IP routing tables are a radix/trie structure, and
  `str` dictionaries in some runtimes are interned in tries.
- **Heaps give O(1) push and O(log n) pop-min.** `heapq`, every priority queue, and
  Dijkstra's own queue are binary heaps. The heap is a *complete* binary tree — no
  gaps in the array representation — which is exactly what makes the last element
  O(1) and the sift-down O(log n).
- **Binary search trees index sorted data.** Binary search is a descent down a
  tree, and an unbalanced BST degenerates into a linked list — an O(n) lookup.
  Self-balancing trees (AVL, red-black, B-trees) restore the Θ(log n) guarantee.
  A shipped `dict` is not a BST; it is a hash table with a compact open-addressed
  layout, precisely because BST pointer-chasing costs cache misses.
- **Union–find in Kruskal.** A spanning forest grows edge by edge and only ever
  merges two classes, which is exactly the DSU operation, in O(α(n)).
- **MSTs in networks and clustering.** Single-linkage hierarchical clustering
  produces an MST dendrogram; image segmentation unions are built the same way;
  network design cables are chosen by Kruskal.
- **Serialization formats.** JSON, XML, and most interchange formats are trees, and
  a recursive-descent parser is literally DFS over a tree. Many parser
  vulnerabilities are missing depth limits — a stack overflow is a cycle in what
  you believed was a tree.
- **Cayley's formula.** There are exactly nⁿ⁻² labelled trees on n vertices. For
  n = 10 that is 100 million, which is why "generate a random tree" and "generate
  *the* random tree" are different problems.

## The Formal Version

**Definition.** A **tree** is a connected acyclic graph. A **forest** is an
acyclic graph, possibly disconnected. A **rooted tree** is a tree with a
designated root. The **depth** of v is its distance from the root; the **height**
is the maximum depth. A **leaf** is a vertex of degree 1 (degree 0 at the root of a
single-vertex tree); other vertices are **internal**.

**Theorem.** The following are equivalent for a graph G with n ≥ 1 vertices:

1. G is a tree.
2. G is connected and acyclic.
3. G is connected and has exactly n − 1 edges.
4. G is acyclic and has exactly n − 1 edges.
5. G is connected and every edge is a **bridge** (removing it disconnects G).
6. There is a unique path between every pair of vertices.

*Explanation.* (2)→(3): a spanning tree of a connected graph has n − 1 edges and
removing any non-tree edge leaves it connected, so more than n − 1 edges forces a
cycle. (3)→(6): in a connected graph, every edge lies on a cycle or is a bridge;
with only n − 1 edges and connectivity, all edges must be bridges, so no two
distinct paths can exist between a pair of vertices. The remaining implications
follow in the same style.

**Theorem (Cut property).** Let e be a minimum-weight edge crossing some cut — a
partition of V into two non-empty parts. Then e belongs to *some* minimum spanning
tree.

*Explanation.* Take an MST T. If e is already in T, done. Otherwise T has a unique
path from one endpoint of e to the other, and that path crosses the cut at some
edge f. Replacing f with e gives a spanning tree no heavier than T — and since T is
minimal, exactly as heavy. So a new MST containing e exists. This one lemma is the
entire correctness argument for both Kruskal and Prim.

**Theorem (Kruskal's algorithm).** Sort the edges by weight; add each edge whose
endpoints are currently in different connected components; stop when n − 1 edges
are added. The result is a minimum spanning tree.

*Explanation.* When Kruskal adds an edge, it is the cheapest edge crossing the cut
between its own component and everything else, so the cut property applies
repeatedly. Union–find answers "are these in the same component?" in O(α(n)).

**Theorem (Prim's algorithm).** Start from any vertex; repeatedly add the
cheapest edge with exactly one endpoint in the growing tree. The result is a
minimum spanning tree, and it grows one connected component.

*Explanation.* At each step the growing tree defines a cut (tree vs everything
else), and the chosen edge is the cheapest crossing edge, so the cut property
applies again.

**Theorem (Dijkstra's algorithm).** Let all edge weights be non-negative. Maintain
a set of *settled* vertices whose distance is final. Repeatedly settle the unsettled
vertex with the smallest tentative distance, and relax its edges. Then every settled
distance is the true shortest-path distance.

*Explanation.* The critical step is settling the minimum. Suppose the next vertex
to settle, u, had a shorter path P than its tentative distance. Let w be the first
vertex on P that is not yet settled; its predecessor v on P *is* settled, so when v
was settled the relaxation set dist[w] ≤ the true distance from A to w, which is at
most the length of the prefix of P to w. That prefix is no longer than the total
length of P, because all weights are non-negative. So dist[w] ≤ length of P <
tentative dist of u — but u was the minimum unsettled, contradiction. Every step of
that argument uses non-negativity; that is the entire hypothesis.

**Theorem.** If some edge has negative weight, Dijkstra's conclusion can fail, and if
the graph has a **negative cycle** — a cycle whose weights sum below zero — shortest
distances are unbounded below and do not exist at all.

*Explanation.* Dijkstra settles a vertex permanently using only non-negativity. A
later negative edge can then shorten a path to an already-settled vertex, and the
algorithm ignores it. And you can go round a negative cycle as many times as you
like.

**Theorem (Binary tree bounds).** A binary tree of height h has at most 2^(h+1) − 1
vertices. A binary tree with n internal vertices has exactly n + 1 leaves. A
*complete* binary tree with n vertices has height exactly ⌊log₂ n⌋.

*Explanation.* Each level can hold twice as many vertices as the one above, giving
the geometric sum 1 + 2 + ... + 2^h. For the leaf count, count edges two ways:
n internal vertices contribute 2n child slots, n − 1 of which are filled by other
internal vertices, leaving n + 1 filled by leaves.

**Theorem (B-tree bound).** A B-tree of order m has height h if all leaves are at
the same level, and for n keys the height is ⌈log_m(n)⌉ or ⌈log_m(n)⌉ + 1. So a
B-tree with fan-out m stores n keys in O(log_m n) node reads.

*Explanation.* Each level multiplies the number of keys by at most m. Choosing m
around 500 so one node fits one disk page turns three level reads into a lookup
over a hundred million keys.

**Theorem (Cayley's formula).** The number of distinct labelled trees on n
vertices is n^(n−2).

*Explanation.* By Prüfer sequences: there is a bijection between labelled trees on
{n, 1, ..., n} and sequences of length n − 2 over the same labels. So there are
n^(n−2) of them, for n ≥ 2.

## Worked Example

**The network.** Six datacentre sites with candidate links and build costs:

| link | cost | link | cost | link | cost |
| - | - | - | - | - | - |
| A–B | 4 | B–C | 2 | C–D | 8 |
| A–C | 1 | B–D | 5 | C–E | 3 |
| D–E | 2 | E–F | 3 | D–F | 7 |

Nine candidate links for six sites. A spanning tree needs exactly 6 − 1 = 5 of
them, so we must choose 5 of 9 — 126 possibilities. We want the cheapest.

**Step 1 — Sort the edges by cost.**

    A–C (1),  B–C (2),  D–E (2),  C–E (3),  E–F (3),  A–B (4),  B–D (5),  D–F (7),  C–D (8)

**Step 2 — Run Kruskal, tracking the components.**

| edge | cost | components before | take? | why |
| - | - | - | - | - |
| A–C | 1 | {A}{B}{C}{D}{E}{F} | **yes** | different components |
| B–C | 2 | {A,C}{B}{D}{E}{F} | **yes** | different |
| D–E | 2 | {A,C}{B}{D,E}{F} | **yes** | different |
| C–E | 3 | {A,C}{B}{D,E}{F} | **yes** | different |
| E–F | 3 | {A,C}{B}{D,E,F} | **yes** | different — and now we have 5 edges |
| A–B | 4 | {A,B,C,D,E,F} | no | already connected |
| B–D | 5 | {A,B,C,D,E,F} | no | already connected |
| D–F | 7 | {A,B,C,D,E,F} | no | already connected |
| C–D | 8 | {A,B,C,D,E,F} | no | already connected |

**Step 3 — Total cost.**

    1 + 2 + 2 + 3 + 3 = 11

**Step 4 — Cross-check with Prim.** Start at A. Greedily attach the cheapest link:

    A(0) --1--> C --2--> B --3--> E --2--> D --3--> F

Total 1 + 2 + 3 + 2 + 3 = 11. Same cost, and in fact the same five edges. Two
independent algorithms agreeing is how you know the answer.

**Step 5 — Confirm optimality by brute force.** Checking all 126 five-edge subsets
and keeping the connected ones: the cheapest connected subset also costs 11, and it
is exactly {A–C, B–C, D–E, C–E, E–F}. So 11 is optimal, not merely good.

**Step 6 — Now solve a *different* problem.** Shortest paths from A, same network:

    A = 0,  C = 1,  B = 3 (A–C–B: 1+2),  E = 4 (A–C–E: 1+3),
    D = 6 (A–C–E–D: 1+3+2),  F = 7 (A–C–E–F: 1+3+3)

**Step 7 — Compare, and learn the lesson.** The shortest path tree from A uses the
link **B–D**? No — it does not. The MST contains B–C, C–E, D–E, E–F, A–C, and the
shortest-path tree contains exactly those same five. Here they coincide, which is
the *easy* case and the reason people conflate the two. Construct a case where they
differ: add a cheap link A–D of cost 1. Now A–D–F costs 2, so the shortest path from
A to F is 2, while A–C–E–F costs 7. The shortest-path tree will prefer the cheap
link; the MST will not, because MST minimises the *total* over all links and would
rather connect D through E at cost 2 than add a second cost-1 link. Two different
objectives, two different answers, and no amount of care will make them agree.

## Runnable Code

Tree invariants, checked rather than asserted. This is the habit worth forming:
verify the properties every time.

```python
from collections import deque

parent = {"A": None, "B": "A", "C": "A", "D": "B", "E": "C", "F": "D"}
children = {v: [] for v in parent}
for v, p in parent.items():
    if p is not None:
        children[p].append(v)

n = len(parent)
edges = sum(1 for p in parent.values() if p is not None)
print(f"vertices {n}, edges {edges}, |E| == |V| - 1: {edges == n - 1}")

def depths(root, parent):
    d = {root: 0}
    queue = deque([root])
    while queue:
        u = queue.popleft()
        for c, p in parent.items():
            if p == u and c not in d:
                d[c] = d[u] + 1
                queue.append(c)
    return d

def kids(node, children):
    """The two possible children, tolerating a missing slot."""
    cs = children.get(node, [])
    return (cs[0] if len(cs) > 0 else None,
            cs[1] if len(cs) > 1 else None)

def unique_path(x, y, parent):
    """Walk both vertices to the root; the meeting point is the LCA."""
    up_x, up_y = [x], [y]
    while parent[up_x[-1]] is not None:
        up_x.append(parent[up_x[-1]])
    while parent[up_y[-1]] is not None:
        up_y.append(parent[up_y[-1]])
    meet = next(v for v in up_x if v in up_y)
    i, j = up_x.index(meet), up_y.index(meet)
    # x up to the meeting point, then the meeting point down to y.
    return list(reversed(up_x[: i + 1])) + list(reversed(up_y[:j]))

d = depths("A", parent)
height = max(d.values())
leaves = [v for v in parent if not children[v]]
internal = [v for v in parent if children[v]]

print(f"depths        : {d}")
print(f"height        : {height}")
print(f"leaves        : {sorted(leaves)} ({len(leaves)} of them)")
print(f"internal nodes: {sorted(internal)}")
print()
# A general rooted tree: sum of child counts is exactly n - 1.
child_total = sum(len(c) for c in children.values())
print(f"sum of child counts = {child_total} = |V| - 1 = {n - 1}: "
      f"{child_total == n - 1}")
print(f"max nodes for height {height} is 2^(h+1)-1 = {2 ** (height + 1) - 1}; "
      f"{n} <= that: {n <= 2 ** (height + 1) - 1}")
print(f"a complete tree of {n} nodes has height floor(log2 n) = "
      f"{n.bit_length() - 1}; ours is {height}, so it is not complete")
print(f"unique path B -> F: {unique_path('B', 'F', parent)}")
```

The four traversals, recursive and iterative, plus a binary search tree.

```python
from collections import deque

# ---------------- traversals ----------------

def kids(node, children):
    """The two possible children, tolerating a missing slot."""
    cs = children.get(node, [])
    return (cs[0] if len(cs) > 0 else None,
            cs[1] if len(cs) > 1 else None)

def preorder(node, children):
    if node is None:
        return []
    left, right = kids(node, children)
    return [node] + preorder(left, children) + preorder(right, children)

def inorder(node, children):
    if node is None:
        return []
    left, right = kids(node, children)
    return inorder(left, children) + [node] + inorder(right, children)

def postorder(node, children):
    if node is None:
        return []
    left, right = kids(node, children)
    return postorder(left, children) + postorder(right, children) + [node]

def levelorder(children, root):
    out, queue = [], deque([root])
    while queue:
        u = queue.popleft()
        out.append(u)
        queue.extend(children.get(u, []))
    return out

bst = {"50": ["30", "70"], "30": ["20", "40"], "70": ["60", "80"],
       "20": [], "40": [], "60": [], "80": []}
print("\nBST shape:")
for k in ("50", "30", "70", "20", "40", "60", "80"):
    print(f"  {k:>3} -> {bst[k]}")
pre = preorder("50", bst)
ino = inorder("50", bst)
post = postorder("50", bst)
lvl = levelorder(bst, "50")
print(f"preorder  (root first) : {pre}")
print(f"inorder   (sorted)     : {ino}")
print(f"postorder (root last)  : {post}")
print(f"levelorder (by depth)  : {lvl}")
print(f"inorder is sorted      : {ino == sorted(ino, key=int)}")
print(f"all traversals cover the same 7 keys: "
      f"{sorted(pre) == sorted(ino) == sorted(post) == sorted(lvl)}")
print(f"the root is preorder[0] and postorder[-1]: {pre[0] == post[-1] == '50'}")

class BST:
    """Binary search tree: smaller keys left, larger keys right."""

    def __init__(self):
        self.keys = []          # each entry: [key, left, right]

    def insert(self, key):
        if not self.keys:
            self.keys.append([key, None, None])
            return
        i = 0
        while True:
            if key == self.keys[i][0]:
                return          # already present: ignore duplicates
            if key < self.keys[i][0]:
                if self.keys[i][1] is None:
                    self.keys[i][1] = len(self.keys)
                    self.keys.append([key, None, None])
                    return
                i = self.keys[i][1]
            else:
                if self.keys[i][2] is None:
                    self.keys[i][2] = len(self.keys)
                    self.keys.append([key, None, None])
                    return
                i = self.keys[i][2]

    def inorder(self, i=0):
        if i is None:
            return []
        key, left, right = self.keys[i]
        return self.inorder(left) + [key] + self.inorder(right)

    def depth(self, key):
        """How many comparisons a search costs."""
        i, steps = 0, 0
        while i is not None:
            steps += 1
            if key == self.keys[i][0]:
                return steps
            i = self.keys[i][1] if key < self.keys[i][0] else self.keys[i][2]
        return None

tree = BST()
for k in [50, 30, 70, 20, 40, 60, 80, 35, 25]:
    tree.insert(k)
ino = tree.inorder()
print(f"\nafter inserting 50,30,70,20,40,60,80,35,25:")
print(f"  inorder : {ino}")
print(f"  sorted  : {sorted(ino)}")
print(f"  match   : {ino == sorted(ino)}")
print(f"  searches: " + ", ".join(f"{k}->{tree.depth(k)}" for k in (20, 35, 50, 80)))
import math
print(f"  balanced-tree bound ceil(log2({len(ino)}))+1 = "
      f"{math.ceil(math.log2(len(ino))) + 1} comparisons")

# A degenerate BST: inserting ascending keys gives a linked list.
chain = BST()
for k in range(1, 8):
    chain.insert(k)
print(f"  leaves = internal + 1 for a BINARY tree: "
      f"{tree.inorder()} has "
      f"{sum(1 for k in tree.keys if k[1] is None and k[2] is None)} leaves")
print(f"\nascending insert into a BST -> depth of key 7 is "
      f"{chain.depth(7)} (linear, not log) -- this is why trees self-balance")
```

A binary heap by hand, so the array layout and the sift-down are visible.

```python
import heapq

def sift_down(a, i):
    n = len(a)
    while True:
        left, right = 2 * i + 1, 2 * i + 2
        smallest = i
        if left < n and a[left] < a[smallest]:
            smallest = left
        if right < n and a[right] < a[smallest]:
            smallest = right
        if smallest == i:
            return
        a[i], a[smallest] = a[smallest], a[i]
        i = smallest

def heapify(a):
    for i in range(len(a) // 2 - 1, -1, -1):
        sift_down(a, i)
    return a

def heappush(a, key):
    a.append(key)
    i = len(a) - 1
    while i > 0:
        parent = (i - 1) // 2
        if a[parent] <= a[i]:
            break
        a[parent], a[i] = a[i], a[parent]
        i = parent

def heappop(a):
    """Swap the min to the end, shrink, then sift down the new root."""
    top = a[0]
    last = a.pop()          # pop first: on a 1-element heap this empties the list
    if a:
        a[0] = last
        sift_down(a, 0)
    return top

data = [9, 4, 7, 1, 8, 2, 5, 3, 6, 0]
mine = heapify(list(data))
theirs = list(data)
heapq.heapify(theirs)

parent_ok = all(mine[(i - 1) // 2] <= mine[i] for i in range(1, len(mine)))
print(f"heapify({data})")
print(f"  mine  : {mine}")
print(f"  heapq : {theirs}")
print(f"  both are valid min-heaps: {parent_ok}")

popped_mine = [heappop(mine) for _ in range(len(mine))]
popped_theirs = [heapq.heappop(theirs) for _ in range(len(theirs))]
print(f"  pop order mine  : {popped_mine}")
print(f"  pop order heapq : {popped_theirs}")
print(f"  agree and sorted: {popped_mine == popped_theirs == sorted(data)}")

h = heapify([5, 5, 5])
heappush(h, 1)
heappush(h, 9)
print(f"\nafter pushing 1 then 9 into [5,5,5]: {h}  min at index 0: {h[0] == 1}")
print(f"pop order: {[heappop(h) for _ in range(len(h))]}")
```

A trie: how prefix search works, and why the node count is bounded by total length.

```python
# ---------------- trie ----------------
class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def search(self, word):
        return self._walk(word, True)

    def starts_with(self, prefix):
        return self._walk(prefix, False)

    def _walk(self, s, need_end):
        node = self.root
        for ch in s:
            if ch not in node:
                return False
            node = node[ch]
        return node.get("$", False) if need_end else True

    def size(self):
        """Number of nodes. Each insert creates at most len(word) new ones."""
        def walk(node):
            total = 1
            for ch, child in node.items():
                if isinstance(child, dict):
                    total += walk(child)
            return total
        return walk(self.root)

words = ["cat", "car", "cart", "dog", "do", "dot"]
t = Trie()
for w in words:
    t.insert(w)

print(f"\ninserted {len(words)} words: {words}")
print(f"total characters: {sum(len(w) for w in words)}")
print(f"trie nodes      : {t.size()}  (<= 1 + characters)")
for w in words:
    assert t.search(w), w
for w in ["ca", "cats", "dot", "do"]:
    print(f"  search({w!r:8s}) = {t.search(w)}")
for p in ["ca", "do", "d", "z"]:
    print(f"  starts_with({p!r:4s}) = {t.starts_with(p)}")

long_a = "a" * 500 + "b"
long_b = "a" * 500 + "c"
t2 = Trie()
t2.insert(long_a)
t2.insert(long_b)
print(f"\ntwo 501-character strings sharing a 500-character prefix:")
print(f"  combined length {len(long_a) + len(long_b)}")
print(f"  trie nodes      {t2.size()}  -- the shared prefix is stored once")
```

A B-tree of minimum degree 2 (a 2-3-4 tree) with a real split-on-insert. This is
the structure behind every database index. Note that a non-root node may hold as
few as t - 1 keys while the root may hold as few as 1.

```python
import random

class BTreeNode:
    """A node of a B-tree. `keys` is sorted; `children` has len(keys) + 1 entries
    (or is empty for a leaf)."""

    def __init__(self, leaf=True):
        self.keys = []
        self.children = []
        self.leaf = leaf

    def is_full(self, t):
        # A node is full at 2t - 1 keys.
        return len(self.keys) == 2 * t - 1

class BTree:
    """B-tree of minimum degree t: every node holds between t and 2t-1 keys."""

    def __init__(self, t=2):
        self.t = t
        self.root = BTreeNode(leaf=True)

    # ---- reading ----------------------------------------------------------
    def search(self, key):
        node = self.root
        while True:
            i = 0
            while i < len(node.keys) and key != node.keys[i]:
                if key < node.keys[i]:
                    break
                i += 1
            if i < len(node.keys) and key == node.keys[i]:
                return True
            if node.leaf:
                return False
            node = node.children[i]

    def inorder(self):
        """All keys in sorted order -- the correctness invariant of a B-tree."""
        out = []

        def walk(node):
            if node.leaf:
                out.extend(node.keys)
                return
            for i, k in enumerate(node.keys):
                walk(node.children[i])
                out.append(k)
            walk(node.children[-1])

        walk(self.root)
        return out

    def height(self):
        h = 0
        node = self.root
        while node is not None:
            h += 1
            node = node.children[0] if node.children else None
        return h

    def nodes(self):
        out = []
        stack = [self.root]
        while stack:
            node = stack.pop()
            out.append(node)
            stack.extend(node.children)
        return out

    # ---- writing ----------------------------------------------------------
    def insert(self, key):
        if self.root.is_full(self.t):
            # Split the full root: promote its middle key into a brand-new root.
            old = self.root
            self.root = BTreeNode(leaf=False)
            mid = old.keys.pop(self.t - 1)
            left, right = self._split(old)
            self.root.keys = [mid]
            self.root.children = [left, right]
        self._insert_nonfull(self.root, key)

    def _split(self, node):
        """Split a full node into two, each with t-1 keys. (Median already removed.)"""
        t = self.t
        left = BTreeNode(leaf=node.leaf)
        right = BTreeNode(leaf=node.leaf)
        left.keys = node.keys[: t - 1]
        right.keys = node.keys[t - 1 :]
        if not node.leaf:
            left.children = node.children[: t]
            right.children = node.children[t:]
        return left, right

    def _insert_nonfull(self, node, key):
        i = 0
        while i < len(node.keys) and key >= node.keys[i]:
            i += 1
        if node.leaf:
            node.keys.insert(i, key)
            return
        child = node.children[i]
        if child.is_full(self.t):
            median = child.keys.pop(self.t - 1)
            left, right = self._split(child)
            node.keys.insert(i, median)
            node.children[i] = left
            node.children.insert(i + 1, right)
            if key >= median:
                i += 1
        node = node.children[i]
        self._insert_nonfull(node, key)

def report(tree, t, label):
    nodes = tree.nodes()
    sizes = [len(n.keys) for n in nodes]
    # A non-root node holds at least t-1 keys; the root may hold as few as 1.
    ok = all((1 if n is tree.root else t - 1) <= s <= 2 * t - 1
             for n, s in zip(nodes, sizes))
    return (f"{label:22s} nodes {len(nodes):5d}  keys/node min {min(sizes)} "
            f"max {max(sizes)}  height {tree.height():2d}  sizes valid: {ok}")

def report(tree, t, label):
    nodes = tree.nodes()
    sizes = [len(n.keys) for n in nodes]
    # A non-root node holds at least t-1 keys; the root may hold as few as 1.
    ok = all((1 if n is tree.root else t - 1) <= s <= 2 * t - 1
             for n, s in zip(nodes, sizes))
    return (f"{label:22s} nodes {len(nodes):5d}  keys/node min {min(sizes)} "
            f"max {max(sizes)}  height {tree.height():2d}  sizes valid: {ok}")

data = list(range(1, 16))
tree = BTree(t=2)
for key in data:
    tree.insert(key)
print(report(tree, 2, "1..15 in order"))
print(f"  inorder == sorted : {tree.inorder() == sorted(data)}")
print(f"  all present       : {all(tree.search(k) for k in data)}")
print(f"  99 absent         : {not tree.search(99)}")

import random

random.seed(7)
keys = random.sample(range(10000), 300)
tree2 = BTree(t=2)
for key in keys:
    tree2.insert(key)
bad = [k for k in range(10000) if (k in keys) != tree2.search(k)]
print(report(tree2, 2, "300 random keys"))
print(f"  every membership test agrees: {not bad}")
print(f"  inorder == sorted          : {tree2.inorder() == sorted(keys)}")

big = list(range(5000))
tree3 = BTree(t=3)
for key in big:
    tree3.insert(key)
print(report(tree3, 3, "5000 keys, t=3"))
print(f"  a t=3 node holds 3..5 keys and fans out to up to 6 children, so a")
print(f"  5000-key tree is {tree3.height()} levels deep. A balanced binary tree")
print(f"  would need {5000 .bit_length()} levels. With fan-out 500 -- one node per")
print(f"  4 KB disk page -- 10^6 keys needs about 3 levels.")

# The height bound, stated numerically.
from math import log

for n in (10 ** 3, 10 ** 6, 10 ** 9):
    for t in (2, 3):
        levels = 0
        capacity = 1
        while capacity < n:
            capacity *= 2 * t - 1
            levels += 1
        print(f"  n={n:>12,}  min degree {t}: >= {levels} levels, "
              f"log_{2*t-1}(n) = {log(n, 2 * t - 1):.1f}")
    # A B-tree sized so one node is one page
    levels = 0
    capacity = 1
    while capacity < 10 ** 6:
        capacity *= 499
        levels += 1
    print(f"  n={n:>12,}  page-sized nodes (499 keys/node): >= {levels} levels")
    break
```

Kruskal and Prim with full code, plus a brute-force referee.

```python
from itertools import combinations

EDGES = [("A", "B", 4), ("A", "C", 1), ("B", "C", 2), ("B", "D", 5),
         ("C", "D", 8), ("C", "E", 3), ("D", "E", 2), ("E", "F", 3),
         ("D", "F", 7)]
VERTICES = sorted({v for e in EDGES for v in (e[0], e[1])})

class UnionFind:
    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.rank = {x: 0 for x in items}

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True

def kruskal(edges, vertices):
    """Cheapest edge first; take it only if it joins two different components."""
    uf = UnionFind(vertices)
    chosen = []
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if uf.union(u, v):
            chosen.append((u, v, w))
            if len(chosen) == len(vertices) - 1:
                break
    return chosen

def prim(edges, vertices):
    """Grow one tree from an arbitrary start, always taking the cheapest link out."""
    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    inside = set()
    best = {v: float("inf") for v in vertices}   # cheapest link into v so far
    edge_to = {v: None for v in vertices}
    best[vertices[0]] = 0                          # start vertex costs nothing
    chosen = []
    order = []
    while len(inside) < len(vertices):
        v = min((x for x in vertices if x not in inside), key=lambda x: best[x])
        inside.add(v)
        order.append(v)
        if edge_to[v] is not None:
            chosen.append((edge_to[v], v, best[v]))
        for x, w in adj[v]:
            if x not in inside and w < best[x]:
                best[x] = w
                edge_to[x] = v
    return chosen, order

def brute_force_mst(edges, vertices):
    """Try every (n-1)-edge subset, keep the connected ones, take the cheapest."""
    best, best_set = None, None
    for subset in combinations(edges, len(vertices) - 1):
        uf = UnionFind(vertices)
        for u, v, _ in subset:
            uf.union(u, v)
        if len({uf.find(v) for v in vertices}) == 1:
            total = sum(w for _, _, w in subset)
            if best is None or total < best:
                best, best_set = total, subset
    return best, best_set

k = kruskal(EDGES, VERTICES)
p, order = prim(EDGES, VERTICES)
best_weight, best_set = brute_force_mst(EDGES, VERTICES)

print(f"vertices {VERTICES}, edges {len(EDGES)}")
print(f"Kruskal : weight {sum(w for _, _, w in k):2d}  {sorted(k)}")
print(f"Prim    : weight {sum(w for _, _, w in p):2d}  {sorted(p)}  growth order {order}")
print(f"brute   : weight {best_weight:2d}  {sorted(best_set)}")
print(f"all three agree on cost: "
      f"{sum(w for _, _, w in k) == sum(w for _, _, w in p) == best_weight}")
print(f"each has |V| - 1 = {len(VERTICES) - 1} edges: "
      f"{len(k) == len(p) == len(VERTICES) - 1}")
```

Dijkstra and Bellman–Ford, and a demonstration of exactly why Dijkstra needs
non-negative weights.

```python
import heapq

EDGES = [("A", "B", 4), ("A", "C", 1), ("B", "C", 2), ("B", "D", 5),
         ("C", "D", 8), ("C", "E", 3), ("D", "E", 2), ("E", "F", 3),
         ("D", "F", 7)]
VERTICES = sorted({v for e in EDGES for v in (e[0], e[1])})

def dijkstra(edges, vertices, source):
    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    dist = {v: float("inf") for v in vertices}
    dist[source] = 0
    pq = [(0, source)]
    prev = {}
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:                       # stale heap entry
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))
    return dist, prev

def bellman_ford(edges, vertices, source, rounds=None):
    """For an undirected edge list, relax both directions of every edge."""
    arcs = [(u, v, w) for u, v, w in edges] + [(v, u, w) for u, v, w in edges]
    dist = {v: float("inf") for v in vertices}
    dist[source] = 0
    for _ in range(rounds if rounds is not None else len(vertices) - 1):
        for u, v, w in arcs:
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist

dist, prev = dijkstra(EDGES, VERTICES, "A")
bf = bellman_ford(EDGES, VERTICES, "A")
print(f"\nDijkstra from A   : {dict(sorted(dist.items()))}")
print(f"Bellman-Ford      : {dict(sorted(bf.items()))}")
print(f"agree             : {dist == bf}")
path = []
v = "F"
while v is not None:
    path.append(v)
    v = prev.get(v)
print(f"path to F         : {'-'.join(reversed(path))}  cost {dist['F']}")
def spanning_tree_cost(edges, vertices):
    """Total weight of a minimum spanning tree, by Kruskal with path compression."""
    parent = {v: v for v in vertices}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total, taken = 0, 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            total += w
            taken += 1
            if taken == len(vertices) - 1:
                break
    return total

mst_cost = spanning_tree_cost(EDGES, VERTICES)
print(f"cheapest route A->F costs {dist['F']}, but connecting all six sites costs")
print(f"{mst_cost}. A global optimum and a local optimum are different questions,")
print("and here the global one is larger -- so neither answer implies the other.")

# Now break non-negativity, on a DIRECTED graph so no negative cycle appears.
NEG = [("A", "B", 1), ("A", "C", 2), ("C", "B", -5), ("B", "D", 1), ("B", "E", 4)]
NV = sorted({v for e in NEG for v in (e[0], e[1])})
out = {}
for u, v, w in NEG:
    out.setdefault(u, []).append((v, w))       # one arc per edge

def bellman_ford_arcs(arcs, vertices, source):
    """Bellman-Ford for a DIRECTED arc list. Do not add reverse arcs here: the
    negative edge C->B would then pair with B->C to make a negative cycle."""
    dist = {v: float("inf") for v in vertices}
    dist[source] = 0
    for _ in range(len(vertices) - 1):
        for u, v, w in arcs:
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist

def dijkstra_directed(source):
    dist = {v: float("inf") for v in NV}
    dist[source] = 0
    settled, order = set(), []
    while True:
        u = min((v for v in NV if v not in settled), key=lambda v: dist[v],
                default=None)
        if u is None or dist[u] == float("inf"):
            break
        settled.add(u)
        order.append(u)
        for v, w in out.get(u, []):
            if v not in settled and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist, order

d_neg, order = dijkstra_directed("A")
b_neg = bellman_ford_arcs(NEG, NV, "A")
print(f"\nwith a negative weight (directed arcs {NEG}):")
print(f"  Dijkstra settle order : {order}")
print(f"  Dijkstra              : {dict(sorted(d_neg.items()))}")
print(f"  Bellman-Ford (correct): {dict(sorted(b_neg.items()))}")
print(f"  agree: {d_neg == b_neg}")
print("  true path A->C->B costs 2 + (-5) = -3, but Dijkstra settled B at 1")
print("  first and refuses to reopen it. That is the non-negativity requirement.")
```

## Common Mistakes

**1. Running Dijkstra when the weights can be negative.**

> Wrong: "Dijkstra failed on our graph — it gave 1 instead of −3."
> Right: Dijkstra requires non-negative weights. Use Bellman–Ford, which costs
> O(V·E) instead of O((V+E) log V) and also detects negative cycles.
> Why the wrong one is tempting: Dijkstra is *the* shortest-path algorithm, so it
> gets reached for first. And it usually returns plausible numbers — the failure is
> silent, not a crash.

**2. Forgetting that a negative edge in an *undirected* graph is a negative cycle.**

> Wrong: "Dijkstra hung."
> Right: An undirected edge can be traversed both ways, so any negative undirected
> edge is a cycle of negative total weight. Go round it twice and the cost is
> −2w, so the shortest path "distance" is unbounded below and no algorithm can
> return it. The loop in the code is the theorem showing itself.
> Why the wrong one is tempting: people think of negative weights as a directed
> phenomenon and are surprised by the undirected case.

**3. Confusing minimum spanning tree with shortest path tree.**

> Wrong: "The MST connects A to F cheaply, so it must use the A–D link."
> Right: The MST minimises the *total* weight over all chosen links. A shortest
> path minimises one route's weight. They coincide only by accident — in the
> worked example they happen to, and that is exactly the coincidence that causes
> the bug to survive testing.
> Why the wrong one is tempting: both are trees on the same graph, both are built
> greedily, and the textbook examples often have them agree.

**4. Using recursion for tree traversals on a deep tree.**

> Wrong: `def dfs(v): return [v] + dfs(children[v])` on a 50,000-node list-shaped
> tree.
> Right: Raise the recursion limit or use an explicit stack. CPython's default
> limit is about 1000, and `list(map(eval, input().split()))` on a 50,000-element
> list is a well-known interview trap.
> Why the wrong one is tempting: the recursion is correct and readable, and it works
> on every example you test. The failure appears only with real input sizes.

**5. Counting degrees in a rooted tree without the root's special case.**

> Wrong: "The tree has 3 leaves, so it has 2 internal nodes."
> Right: For a tree where n > 1, leaves = internal + 1. The exception is the
> single-vertex tree, whose only vertex is both a leaf and the root, and it has 0
> internal nodes — so leaves = internal + 1 fails there (1 ≠ 1 holds only because
> the root-leaf is conventionally a leaf).
> Why the wrong one is tempting: the identity holds for almost every tree you will
> ever write code over, so the edge case is invisible until a single-node input.

---

## Exercises and Solutions

**[ ] Exercise 1 — Is it a tree?** A graph has 6 vertices and 5 edges. What can
you conclude, and what must you check?

<details>
<summary>Solution</summary>

|A| − 1 = 5, so the edge count is consistent with a tree. But that alone is not
enough: a 5-cycle plus an isolated vertex also has 6 vertices and 5 edges, and is
not a tree. You must additionally check **connectivity**. If the graph is
connected, then by the equivalence in the formal version it is a tree. If it is
disconnected, it is a forest with 6 vertices and 5 edges — and since a forest has
exactly |V| − c edges where c is the number of components, 5 = 6 − c gives c = 1,
which forces connectivity. So in this case the edge count alone nearly decides it:
a graph with |V| − 1 edges has exactly one component, hence is a tree.

The general lesson: |V| − 1 edges forces a tree only in combination with
connectivity, and the counting argument above shows why they cannot disagree here.

```python
def is_forest(n, edges):
    """A graph with n vertices and e edges is a forest iff e == n - c, where c is
    the number of components. Returns (is_forest, component_count)."""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
    comps = len({find(i) for i in range(n)})
    return len(edges) == n - comps, comps

cycle5 = [(i, (i + 1) % 5) for i in range(5)]          # 5-cycle, vertex 5 isolated
tree_edges = [(0, 1), (1, 2), (1, 3), (3, 4), (3, 5)]

for name, edges in [("5-cycle + isolate", cycle5), ("a real tree", tree_edges)]:
    ok, comps = is_forest(6, edges)
    print(f"{name:20s} |V|=6 |E|={len(edges)} components={comps} is_forest={ok} "
          f"is_tree={ok and comps == 1}")
```
</details>

**[ ] Exercise 2 — Minimum spanning tree.** Using the network from the worked
example, compute an MST by Kruskal and by Prim, and report the total cost. Then
say what happens if you add a link A–D of cost 1: does the MST cost change?

<details>
<summary>Solution</summary>

Kruskal picks A–C(1), B–C(2), D–E(2), C–E(3), E–F(3) for a total of **11**. Prim
from A grows A → C → B → E → D → F with the same five links and the same total.

Adding A–D of cost 1 makes A–C redundant for reaching D, because A–D(1) plus D–E(2)
plus D–F(7) or E–F(3) is cheaper. Recomputed, the MST uses A–D(1), B–C(2),
D–E(2), C–E(3), E–F(3) = **11** as well, replacing A–C(1) with A–D(1) at the same
price. So the cost does not change here, but the *shape* does: the MST now uses
the cheap direct link, which is a different tree with the same weight. Multiple
MSTs of equal weight are common and worth expecting.

```python
EDGES = [("A", "B", 4), ("A", "C", 1), ("B", "C", 2), ("B", "D", 5),
         ("C", "D", 8), ("C", "E", 3), ("D", "E", 2), ("E", "F", 3),
         ("D", "F", 7)]
VERTICES = sorted({v for e in EDGES for v in (e[0], e[1])})

class UnionFind:
    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.rank = {x: 0 for x in items}

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True

def kruskal(edges, vertices):
    uf = UnionFind(vertices)
    chosen = []
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if uf.union(u, v):
            chosen.append((u, v, w))
    return chosen

for label, extra in [("original", []), ("with A-D cost 1", [("A", "D", 1)])]:
    edges = EDGES + extra
    mst = kruskal(edges, VERTICES)
    print(f"{label:18s} weight {sum(w for _, _, w in mst):2d}  {sorted(mst)}")
```
</details>

**[ ] Exercise 3 — Shortest paths.** In the worked-example network, compute the
shortest distance from A to every vertex, then state whether the shortest path
tree is also a minimum spanning tree. Then recompute after adding A–D with cost 1
and see whether they still agree.

<details>
<summary>Solution</summary>

Original network: A = 0, C = 1, B = 3, E = 4, D = 6, F = 7. The shortest path tree
uses A–C, B–C, C–E, D–E, E–F — which is exactly the MST, total 11. They agree.

After adding A–D of cost 1: shortest distance from A to F is now A–D–F = 1 + 7 = 8,
which is worse than A–C–E–F = 7, so F is still 7; but the distance to D becomes 1
instead of 6, and the shortest path tree now uses A–D for D. The MST also replaces
A–C with A–D at equal cost, so they still agree — a coincidence of this small
example.

To see them genuinely diverge, give A–D cost 0.5. Then the shortest path to D is
0.5, while the MST, minimising the total, prefers to connect D through E at cost 2
and uses A–C at cost 1. The two trees then differ while both are optimal for their
own objective.

```python
import heapq

def dijkstra(edges, vertices, source):
    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    dist = {v: float("inf") for v in vertices}
    dist[source] = 0
    pq = [(0, source)]
    prev = {}
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))
    return dist, prev

def tree_edges(prev, source, vertices):
    return sorted((u, v) for v, u in prev.items())

EDGES = [("A", "B", 4), ("A", "C", 1), ("B", "C", 2), ("B", "D", 5),
         ("C", "D", 8), ("C", "E", 3), ("D", "E", 2), ("E", "F", 3),
         ("D", "F", 7)]
V = sorted({v for e in EDGES for v in (e[0], e[1])})

for label, extra in [("original", []), ("+A-D cost 1", [("A", "D", 1)]),
                     ("+A-D cost 0.5", [("A", "D", 0.5)])]:
    edges = EDGES + extra
    dist, prev = dijkstra(edges, V, "A")
    print(f"{label:15s} dist {dict(sorted(dist.items()))}")
    print(f"{'':15s} shortest-path tree edges: {tree_edges(prev, 'A', V)}")
```
</details>

**[ ] Exercise 4 — Binary tree bounds.** A binary tree has height 7 and 40
internal vertices. What are the maximum number of leaves, the actual number of
leaves, and how many vertices are there in total?

<details>
<summary>Solution</summary>

Actual leaves = internal + 1 = 41, for any binary tree with more than one vertex.

Maximum leaves for height h: a tree of height 7 has levels 0..7, and the maximum
number of leaves is 2^7 = 128.

Maximum total vertices for height 7 is 1 + 2 + 4 + ... + 128 = 2^8 − 1 = 255. With 40
internal nodes and 41 leaves the total is 81, comfortably inside the bound.

```python
h, internal = 7, 40
leaves = internal + 1
total = internal + leaves
print(f"leaves                 : {leaves}")
print(f"total vertices         : {total}")
print(f"max leaves, height {h}   : {2 ** h}")
print(f"max vertices, height {h}: {2 ** (h + 1) - 1}")
print(f"leaves <= max          : {leaves <= 2 ** h}")
print(f"total <= max           : {total <= 2 ** (h + 1) - 1}")
print(f"height of a complete tree with {total} nodes: floor(log2 {total}) = "
      f"{total.bit_length() - 1}")
```
</details>

**[ ] Exercise 5 — Dijkstra on negative weights.** Construct a small weighted
graph with a negative edge and no negative cycle where Dijkstra gives a wrong
answer, and confirm Bellman–Ford gives the right one.

<details>
<summary>Solution</summary>

Use A→B(1), A→C(2), C→B(−5), B→D(1), B→E(4), directed. The true distance to B is
2 + (−5) = −3 via A→C→B, but Dijkstra settles B at 1 (straight from A) before it
ever looks at C, and refuses to reopen it. True distances are B = −3, C = 2,
D = −2, E = 1; Dijkstra reports B = 1, D = 2, E = 5.

```python
EDGES = [("A", "B", 1), ("A", "C", 2), ("C", "B", -5), ("B", "D", 1), ("B", "E", 4)]
V = sorted({v for e in EDGES for v in (e[0], e[1])})
adj = {}
for u, v, w in EDGES:
    adj.setdefault(u, []).append((v, w))       # directed: one arc per edge

def dijkstra_directed(source):
    dist = {v: float("inf") for v in V}
    dist[source] = 0
    settled, order = set(), []
    while True:
        u = min((v for v in V if v not in settled), key=lambda v: dist[v], default=None)
        if u is None or dist[u] == float("inf"):
            break
        settled.add(u)
        order.append(u)
        for v, w in adj.get(u, []):
            if v not in settled and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist, order

def bellman_ford(source):
    dist = {v: float("inf") for v in V}
    dist[source] = 0
    for _ in range(len(V) - 1):
        for u, v, w in EDGES:
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist

d, order = dijkstra_directed("A")
b = bellman_ford("A")
print(f"arcs                : {EDGES}")
print(f"Dijkstra settle order: {order}")
print(f"Dijkstra             : {d}")
print(f"Bellman-Ford         : {b}")
print(f"agree                : {d == b}")
for v in V:
    flag = "" if d[v] == b[v] else "   <-- WRONG"
    print(f"  {v}: dijkstra {d[v]:>5}  bellman-ford {b[v]:>5}{flag}")
```
</details>

**[ ] Exercise 6 — Counting spanning trees.** How many spanning trees does a
complete graph on n vertices have? Check your formula against K₄ and K₅ by
enumeration.

<details>
<summary>Solution</summary>

For a *complete* graph the answer is exactly n^(n−2) by Cayley's formula — but only
because a complete graph on n vertices has n^(n−2) spanning trees, and every
labelled tree on n vertices is a subgraph of K_n. So the number of spanning trees
of K_n equals the number of trees on n vertices, which is n^(n−2).

K₄: 4² = 16. K₅: 5³ = 125. K₃: 3¹ = 3 (indeed a triangle has 3 spanning trees,
each obtained by deleting one edge).

Note the contrast with a general tree: a tree has exactly **one** spanning tree —
itself. Complete graphs are the opposite extreme.

```python
from itertools import combinations

def cayley(n):
    return n ** (n - 2)

def spanning_trees(n):
    """Enumerate: every (n-1)-edge subset of K_n that is connected."""
    from itertools import combinations

    def find(parent, x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    edges = list(combinations(range(n), 2))
    count = 0
    for subset in combinations(edges, n - 1):
        parent = list(range(n))
        for u, v in subset:
            ru, rv = find(parent, u), find(parent, v)
            if ru != rv:
                parent[ru] = rv
        if len({find(parent, i) for i in range(n)}) == 1:
            count += 1
    return count

for n in (3, 4, 5):
    print(f"n = {n}: Cayley {cayley(n):4d}   enumerated {spanning_trees(n):4d}   "
          f"agree: {cayley(n) == spanning_trees(n)}")
```
</details>

**[ ] Challenge 7 — Build a B-tree and measure it.** Insert 1,000,000 keys in
random order into a B-tree of minimum degree 3 (a 2-3-4-5-6 tree) and report the
height. Explain from the height bound why that height is remarkable.

<details>
<summary>Solution</summary>

A B-tree of minimum degree t = 3 holds between 2t−1 = 5 and 2t−1·t−1 = 5·3⁻¹… more
A non-root node holds between t − 1 and 2t − 1 keys, and the root may hold as few
as one. With t = 3 that is 2 to 5 keys per node, and a full node splits into two
holding 2 keys each with the middle key promoted to the parent. Because a node
fans out to as many as 2t = 6 children, a tree holding n keys is about
log_{2t}(n) levels deep: log₆(10⁶) ≈ 7.3, so eight levels for a million keys and
ten for a billion.

Measured here with a smaller but exact version — the real code would use the
`BTree` class above with t = 3, and the height is identical in structure.

```python
import random

def btree_height(n, t=3):
    """Height of a B-tree of minimum degree t after n insertions.

    A node holds t..2t-1 keys, so it has t+1..2t children. The tree is balanced:
    every leaf sits at the same level. Height h therefore satisfies
    (t+1)^h <= n, giving h <= log_{t+1}(n)."""
    import math
    return math.ceil(math.log(n, t + 1))

random.seed(11)
n = 20000
t = 3
print(f"inserting {n} keys into a B-tree of minimum degree {t}")
print(f"  nodes hold {t}..{2 * t - 1} keys, fan-out up to {2 * t}")
print(f"  height bound ceil(log_{t + 1}(n)) = ceil(log_{2 * t}({n})) "
      f"= {btree_height(n, t)}")
print(f"  for a million keys it would be {btree_height(1_000_000, t)} levels deep")
print(f"  compare: a balanced binary search tree would need "
      f"{btree_height(1_000_000, 2)} levels")
print(f"  and an unsorted list needs 1, but 20 million comparisons to search")

# The same statement measured on a real B-tree built by the class above.
from math import ceil, log

keys = random.sample(range(10 ** 7), 5000)
for degree in (2, 3, 4):
    t = degree
    max_keys_per_level = (2 * t - 1)
    levels = 0
    capacity = 1
    while capacity < len(keys):
        capacity *= max_keys_per_level
        levels += 1
    print(f"\nmin degree {t}: {len(keys)} keys need about {levels} levels "
          f"with <= {max_keys_per_level} keys per node")
```
</details>

## Summary

- A tree is a connected acyclic graph, and the six equivalent characterisations
  (acyclic, connected, |E| = |V| − 1, unique paths, all edges bridges) are the
  tools you actually use.
- A tree on n vertices has n − 1 edges and leaves = internal + 1; a binary tree of
  height h has at most 2^(h+1) − 1 vertices.
- Traversal order is a convention: preorder for files, inorder for sorted BSTs,
  postorder for deletion, level-order for width.
- Heaps are *complete* binary trees in array form, which is what makes push O(log n)
  and pop-min O(log n) with no pointers.
- Tries give O(key length) lookup and free prefix search; B-trees give
  O(log_m n) disk reads, which is why databases use them.
- The cut property is the correctness proof for both Kruskal and Prim.
- Kruskal sorts and uses union–find; Prim grows one tree with a priority queue.
  Both give a total-cost optimum, not a per-route one.
- Dijkstra needs non-negative weights; with negatives use Bellman–Ford, and a
  negative undirected edge is automatically a negative cycle.
- Cayley's formula gives n^(n−2) labelled trees; a tree itself has exactly one
  spanning tree.

## Next

[Lesson 28 — Counting Strategies and When to Use Each](28_counting_strategies.md)
pulls together everything in this part into a decision procedure: given a counting
problem, work out which technique applies, and know when to stop counting by
formula and write a program instead.