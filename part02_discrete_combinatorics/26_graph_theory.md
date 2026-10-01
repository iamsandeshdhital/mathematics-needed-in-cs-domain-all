# 26 — Graph Theory

**Part**: part02_discrete_combinatorics · **Prerequisites**: 25 · **Time**: 40 min

---

## In Plain Words

A graph is a set of things and a set of which pairs of those things are joined
together. That is the whole definition. The things are **vertices** (or nodes),
and the joins are **edges**. A road network is a graph: towns are vertices, roads
are edges. A social network is a graph: people are vertices, friendships are
edges. A program's control flow is a graph: instructions are vertices, jumps are
edges. Once you see that a problem is a graph, a large pile of standard questions
becomes available, and they are all named.

Each vertex has a **degree**: how many edges touch it. A useful and slightly
surprising fact is that the degrees of all vertices add up to an even number,
exactly twice the number of edges, because every edge has two ends. That is the
**handshake lemma**, and it immediately lets you rule out some graphs without
building them.

A **path** is a way of getting from one vertex to another along edges. A graph is
**connected** if there is a path between every pair of vertices, and that is what
you check with **BFS** or **DFS** — the two algorithms behind "reachability",
"shortest hop count", "find cycles", "count components", and "topological sort".

A graph is **bipartite** if you can colour every vertex with two colours so that
no edge joins two vertices of the same colour. The test for that is worth
memorising: a graph is bipartite exactly when it contains no odd-length cycle. That
single criterion decides scheduling problems, matching problems, and a surprising
number of modelling questions.

A graph is **planar** if you can draw it on paper with no edges crossing. Planar
graphs are constrained — Euler's formula ties vertices, edges, and faces together
— and the constraint is severe enough to rule out some graphs entirely. This is
why circuit board design, graph drawing, and map colouring are hard in exactly the
way graph theory predicts.

## Why Computer Science Cares

- **BFS and DFS are the two traversal algorithms you will write again and again.**
  `networkx`, `scipy.sparse.csgraph`, and every graph library provide them. BFS
  gives shortest paths in an unweighted graph; DFS gives cycle detection,
  topological sort, strongly connected components, and bridge-finding.
- **Shortest path is a whole product category.** Dijkstra, A\*, and Bellman–Ford
  are graph algorithms on weighted graphs, and they underpin routing protocols,
  link-state routing, and every map API. Lesson
  [27](../part02_discrete_combinatorics/27_trees_and_spanning_trees.md) implements Dijkstra and explains when
  Dijkstra's non-negativity requirement matters.
- **Minimum spanning trees.** A network designer's problem — connect everything as
  cheaply as possible — is exactly Kruskal's or Prim's algorithm, and it is how
  cable networks, cluster topologies, and image segmentation boundaries get
  designed. They use union–find from [Lesson 25](../part02_discrete_combinatorics/25_relations_and_equivalence_classes.md).
- **Bipartite matching and flow.** Bipartite graphs are the structure underneath
  the Hungarian algorithm, Hopcroft–Karp, and every assignment problem: matching
  candidates to jobs, users to ads, packets to links.
- **Planarity as a design constraint.** A circuit board that must avoid crossovers
  needs a planar embedding. Google's Mapbox and OpenStreetMap render graphs with
  crossing-minimising heuristics precisely because you cannot always avoid them,
  and the planar/non-planar distinction is what decides.
- **PageRank as a random walk.** The PageRank algorithm is a random walk on a
  directed graph, and its matrix formulation is exactly the adjacency-matrix
  powers from this lesson. See Lesson
  [41](../part03_linear_algebra/41_matrices_graphs_and_applications.md).
- **Dependency and build graphs.** `make`, `ninja`, Maven, npm, and Cargo all
  model the build as a directed acyclic graph and topologically sort it. A cycle
  in that graph is a real error, and the detection is a DFS with three colours.
- **Counting walks by matrix multiplication.** (Aᵏ)ᵢⱼ counts walks of length k
  from i to j. That single fact drives PageRank, centrality measures, and the
  "how many ways can a token move" questions that appear in model checking.

## The Formal Version

Symbols follow [SYMBOLS.md](../SYMBOLS.md).

**Definition.** A **graph** G = (V, E) has a finite vertex set V and a set E of
unordered pairs of vertices. G is **simple** if it has no loops and no multiple
edges. The **order** is |V| and the **size** is |E|. A **directed graph** has
ordered edges (arcs). A **subgraph** of G is a graph with V' ⊆ V and E' ⊆ E.

**Definition.** The **degree** of v is deg(v) = |{u : {u, v} ∈ E}|. The **degree
sequence** is the multiset of degrees, and the **average degree** is 2|E|/|V|.

**Theorem (Handshake lemma).** Σ_{v ∈ V} deg(v) = 2|E|.

*Explanation.* Count the endpoints of edges. Each edge {u, v} contributes one
endpoint at u and one at v, so counting endpoints edge-by-edge gives 2|E|, and
counting vertex-by-vertex gives the sum of degrees. Both count the same set of
endpoints.

**Corollary.** No simple graph has all vertices of odd degree when |V| is odd, and
the average degree of a simple graph is at most |V| − 1.

*Explanation.* The first because the degree sum 2|E| is even, so an odd number of
odd degrees cannot occur. The second because deg(v) ≤ |V| − 1 for every v in a
simple graph.

**Definition.** A **walk** is a sequence v₀, v₁, …, v_k with {v_{i−1}, v_i} ∈ E.
It is a **path** if all vertices are distinct, a **circuit** if it ends where it
started, and a **cycle** if it is a circuit with all interior vertices distinct. A
path of length k has k edges.

**Definition.** G is **connected** if every pair of vertices is joined by a path.
The maximal connected subgraphs are its **components**. A **spanning tree** is a
connected acyclic subgraph containing every vertex.

**Theorem.** Every connected graph on n vertices has a spanning tree, and every
spanning tree has exactly n − 1 edges.

*Explanation.* Take a spanning tree of minimum total edge count among all acyclic
spanning subgraphs; it exists because the single-vertex graph is acyclic. If it
were disconnected, an edge of G joining two components could be added without
creating a cycle, contradicting minimality. Now count: a tree on n vertices has
n − 1 edges, proved by induction or by the planar formula below.

**Definition.** G is **bipartite** if V = X ∪ Y with X ∩ Y = ∅ and every edge has
one endpoint in X and one in Y.

**Theorem.** A graph is bipartite if and only if it contains no cycle of odd
length.

*Explanation.* If bipartite, every edge flips colour, so a cycle of length k
returns to its start after k flips — possible only for even k. Conversely, in each
connected component pick a root, colour by the parity of the path length from the
root; if an edge ever joined two vertices of the same colour it would close an odd
cycle, so no edge does.

**Theorem (Euler's theorem on trails).** A connected graph has an Euler circuit
(a closed trail using every edge once) if every vertex has even degree, and an
Euler trail (using every edge once, not closed) if exactly two vertices have odd
degree. Otherwise it has none.

*Explanation.* Each visit to a vertex uses edges in pairs (one in, one out), so
degrees must be even, except possibly at the two endpoints of an open trail. The
construction is Hierholzer's algorithm: walk until stuck, splice in further closed
walks from vertices on the current circuit.

**Theorem (Euler's formula).** For a connected plane graph (a planar graph drawn
without crossings), with V vertices, E edges, and F faces including the outer one,

    V − E + F = 2

**Explanation.* Counting face-edge incidences: every face is bounded by at least 3
edges, and every edge is on the boundary of exactly 2 faces, so 3F ≤ 2E. Counting
vertex-edge incidences with a spanning tree gives E ≥ V − 1. Combining these with
Euler's formula yields the bounds below. The formula itself is proved by induction
on E, adding an edge that splits a face and increasing V − E + F by exactly 0 —
adding a new vertex and edge instead increases V and E together.

**Corollary (Planar edge bounds).** A simple planar graph with V ≥ 3 has
E ≤ 3V − 6. A simple planar **bipartite** graph with V ≥ 3 has E ≤ 2V − 4.

*Explanation.* Euler plus 3F ≤ 2E gives E ≤ 3V − 6. For bipartite graphs every
face has length at least 4 (no triangles), giving 4F ≤ 2E and E ≤ 2V − 4.

**Corollary (Non-planarity by counting).** K₅ has V = 5, E = 10, but 3V − 6 = 9,
so K₅ is not planar. K₃,₃ has V = 6, E = 9; the bipartite bound gives 2V − 4 = 8,
so K₃,₃ is not planar either.

**Theorem (Four colour theorem).** Every planar graph admits a proper colouring
with at most four colours.

*Explanation.* Stated here as a fact, not proved — the proof runs to hundreds of
pages and was first completed in 1976. Its algorithmic shadow is a greedy
colouring using at most Δ + 1 colours, where Δ is the maximum degree, and that
bounds the general graph case too.

**Theorem (Adjacency matrix).** For a simple graph on n vertices let A be the
n × n matrix with A_ij = 1 if {i, j} ∈ E and 0 otherwise. Then (Aᵏ)ᵢⱼ is the
number of **walks** of length k from i to j.

*Explanation.* Matrix multiplication sums over the intermediate vertex: (A²)ᵢⱼ =
Σ_m A_im A_mj counts ways to go i → m → j, i.e. two-step walks. The same expansion
compounds, so by induction (Aᵏ)ᵢⱼ counts k-step walks. Note *walks*, not paths —
revisiting vertices is allowed, which is why (A²)ᵢᵢ = deg(i).

## Worked Example

**The graph.** A build system for a package with six modules. Undirected edges
list mutual build dependencies:

    E = {0–1, 0–2, 1–2, 1–3, 2–3, 2–4, 3–4, 4–5}

So |V| = 6 and |E| = 8.

**Step 1 — Degrees by inspection.** Count the edges touching each vertex:

| vertex | neighbours | degree |
| - | - | - |
| 0 | 1, 2 | 2 |
| 1 | 0, 2, 3 | 3 |
| 2 | 0, 1, 3, 4 | 4 |
| 3 | 1, 2, 4 | 3 |
| 4 | 2, 3, 5 | 3 |
| 5 | 4 | 1 |

**Step 2 — Check against the handshake lemma.** Sum = 2 + 3 + 4 + 3 + 3 + 1 = 16,
and 2|E| = 2 × 8 = 16. ✓ The check passes, which is a cheap way to catch a
miscounted edge list. Average degree is 16/6 ≈ 2.67, so this is a sparse graph —
about a third as connected as the complete graph on 6 vertices, which would have
degree 5 everywhere.

**Step 3 — Connectivity.** BFS from vertex 0 reaches 0 → {1, 2} → {3, 4} → {5}. All
six vertices are reached, so G is connected and has one component.

**Step 4 — Bipartiteness.** Try 2-colouring: put 0 in X. Then 1 and 2 must be in
Y (both adjacent to 0). But 1 and 2 are *also* adjacent to each other, so we would
need one of them in X. Contradiction. G is not bipartite.

The quicker test also works: vertices 0, 1, 2 form a 3-cycle, and 3 is odd. Since
bipartite iff no odd cycle, G is not bipartite. Notice the *reason* matters — if
you only know "not bipartite" you cannot conclude "there is a triangle"; odd cycles
can be 5 or 7 long too. Here we found the triangle directly.

**Step 5 — Euler trail.** Count odd-degree vertices: 1, 3, 4, 5 have degrees 3, 3,
3, 1. That is **four** odd-degree vertices. Euler's theorem needs zero or two, so
G has no Euler trail: you cannot draw the dependency graph without lifting your
pen and you cannot do it in one stroke. By contrast the square 0–1–2–3–0 has all
degrees 2 and does have an Euler circuit.

**Step 6 — Planarity.** The necessary condition is E ≤ 3V − 6: here 8 ≤ 12, so the
bound does not reject G. It does *not* prove G is planar — the bound is necessary,
not sufficient. (G is planar in fact: it is a triangle with two pendant chains, but
you would need a drawing to know that.) Contrast K₅, where 10 > 9 rejects it
outright.

**Step 7 — Walks from the adjacency matrix.** With the vertices in order 0..5, the
adjacency matrix is

|     | 0 | 1 | 2 | 3 | 4 | 5 |
| - | - | - | - | - | - | - |
| 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 2 | 1 | 1 | 0 | 1 | 1 | 0 |
| 3 | 0 | 1 | 1 | 0 | 1 | 0 |
| 4 | 0 | 0 | 1 | 1 | 0 | 1 |
| 5 | 0 | 0 | 0 | 0 | 1 | 0 |

The entry (A²)₀₀ = 2 is the number of 2-walks from 0 back to 0: 0 → 1 → 0 and
0 → 2 → 0. That number is deg(0) = 2, exactly as the theorem predicts, because a
2-walk from v to v is exactly a neighbour-and-back. Row 0 of A² is
[2, 1, 1, 2, 1, 0]: two 2-walks to 0, one to 1 (0 → 2 → 1), one to 2
(0 → 1 → 2), two to 3 (via 1 and via 2), one to 4 (via 2), and none to 5.

The row sums of Aᵏ are the total number of k-step walks anywhere in G: 16 for k = 1
(which must equal 2|E| = 16 by the handshake lemma — the same fact again), 48 for
k = 2, and 142 for k = 3. This is how you count "all possible execution
interleavings of depth k" without enumerating anything by hand.

**Step 8 — What a spanning tree would cost.** Any spanning tree of G has exactly
6 − 1 = 5 edges. Choosing the 5 cheapest by some weight is a minimum spanning tree,
which is [Lesson 27](../part02_discrete_combinatorics/27_trees_and_spanning_trees.md).

## Runnable Code

A small graph class that keeps both an adjacency list and an adjacency matrix, so
you can see the trade-off directly.

```python
from collections import deque

class Graph:
    def __init__(self, vertices, edges=(), directed=False):
        self.vertices = list(vertices)
        self.directed = directed
        self.adj = {v: set() for v in self.vertices}
        self.edge_list = []
        for u, v in edges:
            self.add_edge(u, v)

    def add_edge(self, u, v):
        self.edge_list.append((u, v))
        self.adj[u].add(v)
        if not self.directed:
            self.adj[v].add(u)

    # ---- representations -------------------------------------------------
    def matrix(self):
        """Adjacency matrix. O(V^2) memory, O(1) edge test."""
        index = {v: i for i, v in enumerate(self.vertices)}
        n = len(self.vertices)
        return [[1 if index[y] in self.adj[x] else 0 for y in self.vertices]
                for x in self.vertices]

    def degree(self, v):
        """Out-degree for a directed graph, degree otherwise."""
        return len(self.adj[v])

    def average_degree(self):
        return sum(self.degree(v) for v in self.vertices) / len(self.vertices)

    def __str__(self):
        rows = "\n".join(
            f"{v!s:>3}: {sorted(self.adj[v], key=str)}" for v in self.vertices
        )
        return f"Graph(|V|={len(self.vertices)}, |E|={len(self.edge_list)})\n{rows}"

G = Graph(range(6), [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5)])
print(G)
print()
print("degree sequence :", {v: G.degree(v) for v in G.vertices})
print("handshake lemma: sum of degrees =", sum(G.degree(v) for v in G.vertices),
      "| 2|E| =", 2 * len(G.edge_list))
print("average degree :", f"{G.average_degree():.4f}")
print("odd-degree vertices:",
      [v for v in G.vertices if G.degree(v) % 2 == 1])
print()
print("adjacency matrix (rows/cols 0..5):")
for row in G.matrix():
    print("  ", row)
```

BFS and DFS. BFS gives shortest hop distance; DFS with three colours detects
cycles and finds components.

```python
from collections import deque

# Undirected adjacency list, written out so this block stands on its own.
BUILD_EDGES = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5)]

def make_adj(nodes, edges):
    adj = {v: set() for v in nodes}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj

def bfs(adj, start):
    """Shortest-path distances from `start`, plus the predecessor tree.

    Each vertex is enqueued once, so this is O(V + E)."""
    dist = {v: float("inf") for v in adj}
    prev = {v: None for v in adj}
    dist[start] = 0
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for w in sorted(adj[u]):
            if dist[w] == float("inf"):
                dist[w] = dist[u] + 1
                prev[w] = u
                queue.append(w)
    return dist, prev

def path_to(prev, target, start):
    path = [target]
    while path[-1] != start:
        path.append(prev[path[-1]])
    return path[::-1]

def dfs_order(adj, start):
    """Preorder from `start`, using an explicit stack (so no recursion limit)."""
    seen, order, stack = {start}, [], [start]
    while stack:
        u = stack.pop()
        order.append(u)
        for w in sorted(adj[u], reverse=True):
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return order

def components(adj):
    """Connected components -- the equivalence classes from Lesson 25."""
    seen, comps = set(), []
    for v in sorted(adj):
        if v in seen:
            continue
        dist, _ = bfs(adj, v)
        comp = frozenset(w for w, d in dist.items() if d != float("inf"))
        seen |= comp
        comps.append(comp)
    return sorted(comps, key=sorted)

G = make_adj(range(6), BUILD_EDGES)
dist, prev = bfs(G, 0)
print("BFS distances from 0:", {v: (int(d) if d != float("inf") else None) for v, d in dist.items()})
print("shortest path 0 -> 5:", path_to(prev, 5, 0))
print("BFS visit order   :", dfs_order(G, 0))
print("components        :", [sorted(c) for c in components(G)])

# A disconnected graph: BFS from one vertex cannot reach the other component.
H = make_adj(range(7), [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5)])
dist, _ = bfs(H, 0)
print("\nH: BFS from 0 reaches",
      sorted(v for v, d in dist.items() if d != float("inf")),
      "-- but H also has the edge 3-4, so 3 and 4 are a separate component")
print("H: components:", [sorted(c) for c in components(H)])
print("H: 'reachable from 0' is NOT transitive-safe without taking the closure:")
print("   3 -> 4 and 4 -> 5, yet 3 and 0 are not equivalent")
```

Bipartiteness by 2-colouring, cross-checked against the odd-cycle criterion.

```python
from collections import deque

def make_adj(nodes, edges):
    adj = {v: set() for v in nodes}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj

def two_colour(adj):
    """BFS 2-colouring. Returns (ok, colours). False means an odd cycle exists."""
    colour = {}
    for start in sorted(adj):
        if start in colour:
            continue
        colour[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for w in adj[u]:
                if w not in colour:
                    colour[w] = 1 - colour[u]
                    queue.append(w)
                elif colour[w] == colour[u]:
                    return False, colour
    return True, colour

def conflict_edge(adj):
    """The first edge whose endpoints get the same colour -- it closes an odd
    cycle, which is the certificate that the graph is not bipartite."""
    ok, colour = two_colour(adj)
    if ok:
        return None
    for u in adj:
        for w in adj[u]:
            if w in colour and colour[w] == colour[u]:
                return (u, w)
    return None

G = make_adj(range(6), [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5)])
ok, colour = two_colour(G)
print(f"G two-colourable: {ok} | offending edge: {conflict_edge(G)}")

# The same graph with the triangle edge 1-2 removed IS bipartite.
H = make_adj(range(6), [(0, 1), (0, 2), (1, 3), (1, 4), (2, 3), (2, 4)])
ok, colour = two_colour(H)
print(f"H two-colourable: {ok} | colouring: {colour}")
if ok:
    print("   bipartition:",
          sorted(v for v, c in colour.items() if c == 0),
          sorted(v for v, c in colour.items() if c == 1))

# Cycle graphs: even is bipartite, odd is not.
for size in (4, 5, 6, 7):
    C = make_adj(range(size), [(i, (i + 1) % size) for i in range(size)])
    ok, _ = two_colour(C)
    print(f"C{size} bipartite: {ok}")
```

Euler circuits via Hierholzer's algorithm, and Euler's theorem as a check.

```python
def hierholzer(nodes, edges):
    """An Euler trail found by Hierholzer's algorithm.

    Keep walking unused edges; when stuck, pop the vertex onto the circuit. Then
    reverse. Returns (trail, is_closed, is_valid_euler) where is_valid_euler means
    every edge was used exactly once -- which is false when the degree
    conditions of Euler's theorem are violated."""
    adj = {v: [] for v in nodes}
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i))
        adj[v].append((u, i))
    start = next((v for v in nodes if adj[v]), None)
    if start is None:
        return None, False, False

    used = [False] * len(edges)
    stack, circuit = [start], []
    while stack:
        v = stack[-1]
        moved = False
        while adj[v]:
            w, i = adj[v].pop()
            if not used[i]:          # skip edges already traversed
                used[i] = True
                stack.append(w)
                moved = True
                break
        if not moved:
            circuit.append(stack.pop())

    trail = circuit[::-1]
    if not all(used):
        return trail, False, False
    keys = [frozenset((a, b)) for a, b in zip(trail, trail[1:])]
    if len(set(keys)) != len(edges):
        return trail, False, False   # some edge was traversed twice
    return trail, trail[0] == trail[-1], True

def degrees(nodes, edges):
    deg = {v: 0 for v in nodes}
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1
    return deg

def euler_verdict(nodes, edges):
    """Euler's theorem, stated as code: 0 odd degrees -> circuit, 2 -> trail."""
    deg = degrees(nodes, edges)
    odd = [v for v in nodes if deg[v] % 2 == 1]
    if not odd:
        return "circuit exists"
    if len(odd) == 2:
        return "trail only (start/end at the two odd vertices)"
    return "neither"

examples = {
    "square 0-1-2-3-0": (list(range(4)), [(0, 1), (1, 2), (2, 3), (3, 0)]),
    "K4 (complete on 4)": (list(range(4)),
                           [(i, j) for i in range(4) for j in range(i + 1, 4)]),
    "square + diagonal 0-2": (list(range(4)), [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]),
}
print(f"{'graph':24s} {'degrees':16s} {'odd':11s} {'theorem':22s} walk found")
for name, (nodes, edges) in examples.items():
    deg = degrees(nodes, edges)
    odd = [v for v in nodes if deg[v] % 2 == 1]
    trail, closed, valid = hierholzer(nodes, edges)
    verdict = ("Euler circuit" if closed else "Euler trail, open") if valid \
        else "no Euler trail exists"
    print(f"{name:24s} {str([deg[v] for v in nodes]):16s} {str(odd):11s} "
          f"{verdict:22s} {trail}")
```

Planarity: the edge bounds as a rejection test, and Euler's formula on graphs
that are drawn.

```python
def planarity_bound_ok(V_count, E_count, bipartite=False):
    """Necessary condition only. Passing does NOT prove planarity."""
    if V_count < 3:
        return True
    limit = 2 * V_count - 4 if bipartite else 3 * V_count - 6
    return E_count <= limit

from itertools import combinations

def complete(n):
    return [(i, j) for i, j in combinations(range(n), 2)]

K3_3 = [(u, v) for u in range(3) for v in range(3, 6)]

candidates = [
    # name, V, E, is_bipartite
    ("K4 (tetrahedron)", 4, len(complete(4)), False),
    ("K5", 5, len(complete(5)), False),
    ("K6", 6, len(complete(6)), False),
    ("K3,3 (complete bipartite)", 6, len(K3_3), True),
    ("our build graph", 6, 8, False),
    ("cube Q3", 8, 12, False),
]
print(f"{'graph':26s} {'V':>2} {'E':>3} {'E<=3V-6':>9} {'E<=2V-4':>9}  verdict")
for name, V, E, bip in candidates:
    simple = planarity_bound_ok(V, E, False)
    bbound = planarity_bound_ok(V, E, True)
    # The bipartite bound only applies when the graph really is bipartite.
    if not simple:
        verdict = "NOT planar (3V-6 fails)"
    elif bip and not bbound:
        verdict = "NOT planar (2V-4 fails)"
    else:
        verdict = "inconclusive -- need a drawing or Kuratowski"
    print(f"{name:26s} {V:2d} {E:3d} {'pass' if simple else 'FAIL':>9} "
          f"{('pass' if bbound else 'FAIL') + ('*' if bip else ' '):>9}  {verdict}")
print("* the bipartite bound is only consulted for graphs that are bipartite")

# Euler's formula on a graph we can actually draw: the cube, V - E + F = 2.
# The cube has V = 8, E = 12, and 6 faces (6 squares + the outside).
V_cube, E_cube = 8, 12
F_cube = 6
print(f"\ncube: V - E + F = {V_cube} - {E_cube} + {F_cube} = "
      f"{V_cube - E_cube + F_cube}")
print(f"K4 (tetrahedron): V - E + F = 4 - 6 + {2 - 4 + 6} = {4 - 6 + (2 - 4 + 6)}")
print("check 3V - 6 for K4:", 3 * 4 - 6, "== E =", len(complete(4)), "(tight)")
```

Adjacency matrix powers counting walks — the bridge to linear algebra in
[Lesson 41](../part03_linear_algebra/41_matrices_graphs_and_applications.md).

```python
def matmul(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in range(len(Y)))
             for j in range(len(Y[0]))] for i in range(len(X))]

def walk_counts(adj, nodes, k):
    """The k-th power of the adjacency matrix.

    (A^k)[i][j] = number of walks of exactly length k from node i to node j.
    Walks may revisit vertices, which is why the diagonal is nonzero."""
    A = [[1 if y in adj[x] else 0 for y in nodes] for x in nodes]
    P = A
    for _ in range(k - 1):
        P = matmul(P, A)
    return P

nodes = list(range(6))
edges = {v: set() for v in nodes}
for u, v in [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5)]:
    edges[u].add(v)
    edges[v].add(u)

P1 = walk_counts(edges, nodes, 1)
P2 = walk_counts(edges, nodes, 2)
P3 = walk_counts(edges, nodes, 3)
n_edges = sum(len(edges[v]) for v in nodes) // 2
print(f"total walks of length 1: {sum(map(sum, P1))} = 2|E| = {2 * n_edges}")
print(f"total walks of length 2: {sum(map(sum, P2))}")
print(f"total walks of length 3: {sum(map(sum, P3))}")
print(f"\nrow 0 of A^2 (2-walks starting at 0): {P2[0]}")
print(f"  (A^2)[0][0] = {P2[0][0]} = deg(0) = {len(edges[0])}: a 2-walk from v")
print("  back to v is exactly neighbour-and-back, so the count is the degree.")

# The same on a path graph, where every walk is a simple path.
path_nodes = list(range(4))
path_edges = {v: set() for v in path_nodes}
for i in range(3):
    path_edges[i].add(i + 1)
    path_edges[i + 1].add(i)
P = walk_counts(path_edges, path_nodes, 3)
print("\npath 0-1-2-3:")
print("  A^3 =", P)
print("  row sums (walks from each vertex):", [sum(r) for r in P],
      "total", sum(map(sum, P)))
A2 = walk_counts(path_edges, path_nodes, 2)
print("  A^2 diagonal:", [A2[i][i] for i in path_nodes],
      "= degrees:", [len(path_edges[v]) for v in path_nodes])
```

## Common Mistakes

**1. Dividing the degree sum by 2 and reporting edges, then using it as degree.**

> Wrong: "Vertex 2 has degree 4 because the degree sequence contains a 4."
> Right: deg(2) = 4 = |{0, 1, 3, 4}|. The handshake lemma constrains the *total*
> over all vertices (16 = 2 × 8), not individual degrees.
> Why the wrong one is tempting: the lemma is remembered as "degrees sum to twice
> edges" and gets misapplied per-vertex.

**2. Treating a walk as a path in the adjacency-matrix theorem.**

> Wrong: "(A³)ᵢⱼ is the number of paths of length 3 from i to j."
> Right: (Aᵏ)ᵢⱼ counts **walks**, where vertices may repeat. The tell is the
> diagonal: (A²)ᵢᵢ = deg(i), which is zero for a tree but nonzero in general.
> Why the wrong one is tempting: "path" is the friendlier word, and for a tree the
> two coincide, so the error hides until you meet a cycle.

**3. Treating the planarity bound as a proof of planarity.**

> Wrong: "Our graph has 8 edges and 6 vertices, 8 ≤ 3·6 − 6 = 12, so it is
> planar."
> Right: The bound is a necessary condition. Passing it means nothing. To prove
> planarity you need a drawing; to disprove it you need either the bound failing
> or a genuine non-planarity result such as containing K₅ or K₃,₃ as a minor.
> Why the wrong one is tempting: a passing test feels like a green light, and the
> bound is famous enough to feel authoritative.

**4. Confusing bipartite with "no cycles".**

> Wrong: "This graph is bipartite — it has no cycles at all."
> Right: It is bipartite, and the correct reason is that it has no odd cycles.
> Trees and forests are bipartite; so are even cycles, grids, and bipartite
> multi-layer networks. "No cycles" is a much stronger property than needed.
> Why the wrong one is tempting: trees are the first bipartite example everyone
> sees, so the two get glued together.

**5. Using BFS to detect cycles in a graph with weighted edges.**

> Wrong: "Run BFS and complain when you revisit a vertex."
> Right: BFS revisits vertices constantly — that is how it avoids re-exploring.
> Cycle detection needs the DFS three-colour marking, and weighted shortest paths
> need Dijkstra, not BFS. Choosing BFS for a weighted problem silently returns
> hop counts while claiming to return distances.
> Why the wrong one is tempting: BFS finds shortest paths, so it looks like the
> right tool for anything path-shaped.

---

## Exercises and Solutions

**[ ] Exercise 1 — Handshake lemma.** A simple graph has 7 vertices, three of
which have degree 4, and the other four have degrees 2, 3, 5, and 6. Is such a
graph possible? If so, exhibit one.

<details>
<summary>Solution</summary>

**Parity check first.** Sum of degrees = 4 + 4 + 4 + 2 + 3 + 5 + 6 = 28, which is
even, so the handshake lemma does not rule it out, and |E| = 28 / 2 = 14. Also,
deg = 6 on 7 vertices means one vertex is adjacent to all others, which is allowed.

**It is possible.** Havel–Hakimi constructs it greedily: take the highest remaining
degree, join that vertex to that many other vertices of highest remaining degree,
subtract, repeat. The result below has degrees 2, 3, 4, 4, 4, 5, 6 — exactly the
target multiset — with 14 edges.

```python
def havel_hakimi(degrees):
    """Build a simple graph with the given degree multiset, or None if impossible.

    Repeatedly take the highest remaining degree, connect that vertex to that many
    other highest-degree vertices, and subtract 1 from each of them."""
    n = len(degrees)
    deg = list(degrees)
    adj = [set() for _ in range(n)]
    while True:
        alive = [i for i in range(n) if deg[i] > 0]
        if not alive:
            break
        u = max(alive, key=lambda i: deg[i])
        others = sorted((i for i in alive if i != u), key=lambda i: -deg[i])
        if deg[u] > len(others):
            return None
        for v in others[: deg[u]]:
            adj[u].add(v)
            adj[v].add(u)
            deg[v] -= 1
        deg[u] = 0
    return adj

target = [4, 4, 4, 2, 3, 5, 6]
adj = havel_hakimi(target)
achieved = sorted(len(a) for a in adj)
print(f"target degrees sorted : {sorted(target)}")
print(f"achieved degrees      : {achieved}")
print(f"same multiset         : {achieved == sorted(target)}")
print(f"sum of degrees        : {sum(achieved)} (even: {sum(achieved) % 2 == 0})")
print(f"|E|                   : {sum(achieved) // 2}")
# Adjacency sets cannot hold duplicates or loops, but check the edge count too.
no_loops = all(i not in a for i, a in enumerate(adj))
edge_keys = {frozenset((i, j)) for i in range(7) for j in adj[i] if i != j}
incidences = sum(len(a) for a in adj)
print(f"no loops        : {no_loops}")
print(f"distinct edges  : {len(edge_keys)}")
print(f"edge incidences : {incidences} = 2 x {len(edge_keys)} "
      f"-> {incidences == 2 * len(edge_keys)}")
print("edges:", sorted(tuple(sorted((i, j))) for i in range(7) for j in adj[i] if i < j))
```
</details>

**[ ] Exercise 2 — Average degree and density.** For a simple graph on 10 vertices
with 20 edges, compute the average degree and the fraction of possible edges
present. What is the degree of the vertex of highest degree at least?

<details>
<summary>Solution</summary>

Average degree = 2|E|/|V| = 40/10 = 4.

Fraction present = 20 / C(10,2) = 20/45 ≈ 0.444.

Highest degree: the average is 4, so the maximum is at least 4. If *every* vertex
had degree below 4 the average would be below 4, so some vertex has degree ≥ 4. In
a graph with this density you can say a little more: with 20 edges on 10 vertices,
some vertex has degree ≥ ⌈40/10⌉ = 4, and by the convexity argument a simple graph
this dense must have a vertex of degree at least 5 — because if all degrees were
≤ 4 and even, the only way to average exactly 4 is all degrees exactly 4, which is
possible (the 4-regular graph on 10 vertices, e.g. the pentagonal prism), so 4 is
the correct tight bound.

```python
from math import comb

V, E = 10, 20
print(f"average degree : {2 * E / V}")
print(f"possible edges : C({V},2) = {comb(V, 2)}")
print(f"edge density   : {E}/{comb(V, 2)} = {E / comb(V, 2):.3f}")
print(f"max degree at least ceil(avg) = {-(-2 * E // V)}")
print("and it is tight: the 4-regular graph on 10 vertices has all degrees 4")
```
</details>

**[ ] Exercise 3 — Bipartite or not.** Decide whether each of these is bipartite,
and for the ones that are, exhibit the 2-colouring.

(a) the 5-cycle C₅; (b) the 4-cycle C₄; (c) a triangle with a pendant edge;
(d) the Petersen graph (outer 5-cycle, inner pentagram, five spokes).

<details>
<summary>Solution</summary>

(a) C₅: not bipartite — it is itself an odd cycle.
(b) C₄: bipartite, colouring {0, 2} and {1, 3}.
(c) triangle with a pendant edge: not bipartite, because the triangle is an odd
cycle. The pendant edge is irrelevant to bipartiteness.
(d) Petersen graph: not bipartite. It is 3-regular on 10 vertices, so 3 + 3 is odd
— a quick certificate: any bipartite graph that is regular of odd degree on an
even number of vertices is impossible, because each side has equal size, so
|V| = 2 × (degree). Here 10 ≠ 2 × 3. So it is not bipartite.

```python
from collections import deque

def two_colour(nodes, edges):
    adj = {v: set() for v in nodes}
    for u, v in edges:
        adj[u].add(v); adj[v].add(u)
    colour = {}
    ok = True
    for s in nodes:
        if s in colour:
            continue
        colour[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for w in adj[u]:
                if w not in colour:
                    colour[w] = 1 - colour[u]
                    q.append(w)
                elif colour[w] == colour[u]:
                    ok = False
    return ok, colour

def cycle(n):
    return list(range(n)), [(i, (i + 1) % n) for i in range(n)]

# Petersen: outer 0-4 cycle, inner 5-9 pentagram, spokes i-(i+5)
pn = list(range(10))
pe = [(i, (i + 1) % 5) for i in range(5)] + [(5 + i, 5 + (i + 2) % 5) for i in range(5)] \
     + [(i, i + 5) for i in range(5)]

cases = {
    "C5": cycle(5),
    "C4": cycle(4),
    "triangle + pendant": ([0, 1, 2, 3], [(0, 1), (1, 2), (2, 0), (2, 3)]),
    "Petersen": (pn, pe),
}
for name, (nodes, edges) in cases.items():
    ok, colour = two_colour(nodes, edges)
    deg = {v: 0 for v in nodes}
    for u, v in edges:
        deg[u] += 1; deg[v] += 1
    sides = (sorted(v for v in nodes if colour.get(v) == 0),
             sorted(v for v in nodes if colour.get(v) == 1)) if ok else None
    print(f"{name:20s} bipartite={ok!s:5} regular={len(set(deg.values())) == 1} "
          f"degrees={sorted(set(deg.values()))} sides={sides}")
```
</details>

**[ ] Exercise 4 — Euler circuits.** For each graph, say whether an Euler circuit
exists, whether an Euler trail exists but no circuit, and give the trail or
circuit when one exists.

(a) the square 0–1–2–3–0; (b) K₄; (c) the square plus the diagonal 0–2.

<details>
<summary>Solution</summary>

(a) Square: all degrees 2, so 0 odd-degree vertices, connected ⇒ Euler circuit
exists. One is 0 → 1 → 2 → 3 → 0.
(b) K₄: all degrees 3, so 4 odd-degree vertices ⇒ neither circuit nor trail.
(c) Square plus diagonal 0–2: degrees become 0:3, 1:2, 2:3, 3:2, so exactly 2 odd
vertices (0 and 2). Connected with exactly two odd vertices ⇒ an Euler *trail*
exists but no circuit, and it must start at 0 or 2 and end at the other. One is
0 → 1 → 2 → 3 → 0 → 2.

```python
def degrees(nodes, edges):
    deg = {v: 0 for v in nodes}
    for u, v in edges:
        deg[u] += 1; deg[v] += 1
    return deg

cases = {
    "square 0-1-2-3-0": (list(range(4)), [(0, 1), (1, 2), (2, 3), (3, 0)]),
    "K4": (list(range(4)), [(i, j) for i in range(4) for j in range(i + 1, 4)]),
    "square + diagonal 0-2": (list(range(4)), [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]),
}
for name, (nodes, edges) in cases.items():
    deg = degrees(nodes, edges)
    odd = sorted(v for v in nodes if deg[v] % 2 == 1)
    kind = ("circuit" if not odd else "trail only" if len(odd) == 2 else "neither")
    print(f"{name:24s} degrees={[deg[v] for v in nodes]} odd={odd} -> {kind}")

def euler_trail(nodes, edges):
    """Hierholzer. Returns None unless every edge is used exactly once."""
    adj = {v: [] for v in nodes}
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i))
        adj[v].append((u, i))
    start = next((v for v in nodes if adj[v]), None)
    if start is None:
        return None
    used = [False] * len(edges)
    stack, out = [start], []
    while stack:
        v = stack[-1]
        moved = False
        while adj[v]:
            w, i = adj[v].pop()
            if not used[i]:
                used[i] = True
                stack.append(w)
                moved = True
                break
        if not moved:
            out.append(stack.pop())
    trail = out[::-1]
    if not all(used):
        return None
    keys = {frozenset((a, b)) for a, b in zip(trail, trail[1:])}
    return trail if len(keys) == len(edges) else None

for name, (nodes, edges) in cases.items():
    trail = euler_trail(nodes, edges)
    print(f"{name:24s} euler trail: {trail}")
```
</details>

**[ ] Exercise 5 — Planarity bound.** Use E ≤ 3V − 6 and E ≤ 2V − 4 to prove that
K₅ and K₃,₃ are not planar. Then use the bound to decide whether a graph with
20 vertices and 55 edges is planar.

<details>
<summary>Solution</summary>

K₅: V = 5, E = C(5,2) = 10. The bound gives 3(5) − 6 = 9. Since 10 > 9, K₅ is not
planar.

K₃,₃: V = 6, E = 9. The simple bound gives 3(6) − 6 = 12, which does not reject
it. But K₃,₃ is bipartite, so use E ≤ 2V − 4 = 8. Since 9 > 8, K₃,₃ is not planar.

20 vertices and 55 edges: 3(20) − 6 = 54, and 55 > 54, so the graph is not planar.
This is a nice tight case — the bound is only just exceeded.

```python
from itertools import combinations

k5 = list(combinations(range(5), 2))
k33 = [(u, v) for u in range(3) for v in range(3, 6)]

print(f"K5  : V=5 E={len(k5)} bound 3V-6={3*5-6} -> non-planar: {len(k5) > 3*5-6}")
print(f"K3,3: V=6 E={len(k33)} bound 2V-4={2*6-4} -> non-planar: {len(k33) > 2*6-4}")
print(f"     (the simple bound 3V-6 = {3*6-6} does not reject it: {len(k33)} <= {3*6-6})")
print(f"20 vertices, 55 edges: bound 3V-6 = {3*20-6} -> non-planar: {55 > 3*20-6}")
```
</details>

**[ ] Exercise 6 — Walks in a matrix.** For the path graph 0–1–2–3, compute the
number of walks of length 2 from each vertex to each vertex, and verify that the
diagonal entries equal the degrees.

<details>
<summary>Solution</summary>

Adjacency matrix A:

    0 1 0 0
    1 0 1 0
    0 1 0 1
    0 0 1 0

A² = A·A, so (A²)ᵢⱼ = Σₘ Aᵢₘ Aₘⱼ:

    1 0 1 0
    0 2 0 1
    1 0 2 0
    0 1 0 1

The diagonal is (1, 2, 2, 1), which are exactly the degrees. ✓

Reading a row: from vertex 0 there is 1 two-walk to vertex 0 (0→1→0), 1 to vertex
2 (0→1→2), and 0 elsewhere.

```python
def matmul(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in range(len(Y)))
             for j in range(len(Y[0]))] for i in range(len(X))]

n = 4
A = [[1 if abs(i - j) == 1 else 0 for j in range(n)] for i in range(n)]
A2 = matmul(A, A)
for row in A2:
    print(row)
print("diagonal of A^2:", [A2[i][i] for i in range(n)])
print("degrees of path :", [sum(A[i]) for i in range(n)])
print("diagonal == degrees:", [A2[i][i] for i in range(n)] == [sum(A[i]) for i in range(n)])
```
</details>

**[ ] Challenge 7 — Connectivity in a directed graph.** The build dependency graph
is *directed*: an edge a → b means "build a before b". Give an example where
"reachable from" is not symmetric, and explain why a build system must additionally
reject cycles rather than just reporting reachability.

<details>
<summary>Solution</summary>

Example: build graph with edges 0 → 1 and 1 → 2, plus an isolated 3. Then
0 → 1 (0 reaches 1) but 1 does not reach 0. "Reaches" is reflexive and transitive
but not symmetric, so it is *not* an equivalence relation and its classes are
undefined until you take the closure.

The fix for reachability is the transitive closure, which is symmetric only after
you symmetrise. But a build system needs something stronger: it needs a
**topological order**, which exists if and only if the directed graph is acyclic
(DAG). A cycle like 0 → 1 → 2 → 0 means every member requires another to be built
first, so no valid ordering exists at all. Reachability queries cannot detect this
— they just report "everything reaches everything". Detecting the cycle is a
separate DFS with three colours, and it is a genuine error condition, not a
performance concern.

```python
from collections import deque

def reachable(dag, start):
    seen, stack = {start}, [start]
    while stack:
        u = stack.pop()
        for v in dag.get(u, ()):
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return seen

edges = {0: [1], 1: [2], 2: [], 3: []}
r = reachable(edges, 0)
print("reachable from 0:", sorted(r))
print("0 reaches 1:", 1 in r, "| 1 reaches 0:", 0 in reachable(edges, 1),
      "-> not symmetric, so not an equivalence relation")

def has_cycle(dag):
    """Three-colour DFS: white (unvisited), grey (on stack), black (done)."""
    colour = {}
    def visit(u):
        colour[u] = 1
        for v in dag.get(u, ()):
            if colour.get(v) == 1:
                return True
            if colour.get(v, 0) == 0 and visit(v):
                return True
        colour[u] = 2
        return False
    return any(colour.get(u, 0) == 0 and visit(u) for u in dag)

print("acyclic build graph has_cycle:", has_cycle(edges))
cyclic = {0: [1], 1: [2], 2: [0]}
print("cyclic build graph has_cycle:", has_cycle(cyclic))
```
</details>

## Summary

- A graph is vertices plus edges; degree, order, and size are the basic counts.
- The handshake lemma, Σ deg = 2|E|, gives cheap validity checks on any edge list.
- BFS gives shortest hop counts in O(V + E); DFS with three colours gives cycle
  detection, components, and topological sort.
- A graph is bipartite iff it has no odd cycle — the single most useful structural
  test in the subject.
- Euler's theorem: a circuit needs all degrees even, a trail needs exactly two odd
  degrees; Hierholzer's algorithm constructs one in O(E).
- Euler's formula V − E + F = 2 gives E ≤ 3V − 6 and, for bipartite graphs,
  E ≤ 2V − 4 — enough to prove K₅ and K₃,₃ non-planar.
- The planarity bounds are *necessary*, never sufficient: passing proves nothing.
- (Aᵏ)ᵢⱼ counts k-step **walks** from i to j, not paths; the diagonal (A²)ᵢᵢ =
  deg(i) is the tell.
- Connected components are exactly the equivalence classes of the reflexive
  transitive closure, which is why union–find solves them.

## Next

[Lesson 27 — Trees and Spanning Trees](../part02_discrete_combinatorics/27_trees_and_spanning_trees.md) assumes you
can use degrees, connectivity, and the handshake lemma; it takes the special
graph with exactly n − 1 edges and builds shortest paths, minimum spanning trees,
and the tree data structures that index every database you have ever used.