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

## Formula Sheet

Every symbol and formula this lesson introduces. `G = (V, E)` with `V` vertices and
`E` edges, `|V|` the **order** and `|E|` the **size**, `n = |V|`, `m = |E|`.
Subscripts on `A` index vertices; `Aᵏ` is the `k`-th matrix power.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| Graph | `$G = (V, E)$` with `E ⊆ {{u,v} : u,v ∈ V}` | a set of things and a set of which pairs are joined | road networks, social graphs, build graphs, control flow |
| Order and size | `$\lvert V\rvert = n$`, `$\lvert E\rvert = m$` | how many vertices, how many edges | almost every bound in the lesson is a statement about `n` and `m` |
| Simple graph | no loops, no multiple edges | a plain undirected graph | required for the bounds `m ≤ 3n − 6`, `deg ≤ n − 1`, `m ≤ C(n,2)` |
| Degree | `$\deg(v) = \lvert\{u : \{u,v\} \in E\}\rvert$` | how many edges touch `v` | the input to the handshake lemma and to Euler's theorem |
| Degree sequence | the multiset of all degrees | the degrees, order irrelevant | checking a proposed graph is graphical |
| Average degree | `$\bar d = 2\lvert E\rvert/\lvert V\rvert$` | total degree divided by number of vertices | sparse vs dense; `16/6 ≈ 2.67` for the worked graph |
| Handshake lemma | `$\sum_{v\in V}\deg(v) = 2\lvert E\rvert$` | every edge has two ends, so endpoints are counted twice | the cheapest possible check on an edge list |
| Parity corollary | a simple graph cannot have all `n` vertices of odd degree when `n` is odd | the degree sum `2m` is even | rejects whole degree sequences in one step |
| Degree ceiling | `$\deg(v) \le n - 1$`, hence `$\bar d \le n-1$` | a vertex cannot be joined to itself | saturates only for the complete graph `K_n` |
| Walk | `$v_0, v_1, \dots, v_k$` with `$v_{i-1}v_i \in E$` | a trip that may revisit vertices | what the adjacency matrix counts |
| Path | a walk with all vertices distinct | no repeats | the shortest-path object; requires a traversal, not a matrix power |
| Circuit | a walk returning to its start | closed, repeats allowed | a route you can trace in one stroke |
| Cycle | a circuit with all interior vertices distinct | a minimal closed loop | the object the bipartiteness criterion forbids when odd |
| Connected / components | every pair joined by a path; the maximal such subgraphs | one piece, or several | components are the equivalence classes of [Lesson 25](../part02_discrete_combinatorics/25_relations_and_equivalence_classes.md) |
| Spanning tree | a connected acyclic subgraph with all `n` vertices | the skeleton | has **exactly `n − 1`** edges, always |
| Bipartite | `$V = X \cup Y$, `$X \cap Y = \emptyset$`, every edge one endpoint in each | 2-colourable | the structure under matching, flow, and scheduling |
| Bipartite criterion | `$G$ bipartite $\iff$ `$G$ has no odd-length cycle$` | two-colourable exactly when no odd cycle | the single test worth memorising |
| Euler circuit | a closed trail using every edge exactly once | one-stroke drawing | exists **iff every vertex has even degree** (connected) |
| Euler trail | uses every edge once, not closed | one-stroke open drawing | exists **iff exactly two** vertices have odd degree |
| Neither | four or more odd-degree vertices | cannot be drawn in one stroke | the build graph has four: 1, 3, 4, 5 |
| Hierholzer's algorithm | walk until stuck, then splice closed walks from vertices on the circuit | constructive Euler trail | the lesson's `hierholzer` |
| Euler's formula | `$V - E + F = 2$` | vertices minus edges plus faces | for a **connected plane** graph, `F` counting the outer face; cube: `8 − 12 + 6 = 2` |
| Face-degree incidence | `$3F \le 2E$` | each face has ≥ 3 sides, each edge borders exactly 2 faces | combine with Euler to get the planar bound |
| Planar edge bound | `$E \le 3V - 6$` | simple planar, **`V ≥ 3`** | **necessary only** — passing proves nothing |
| Bipartite planar bound | `$E \le 2V - 4$` | simple planar **and** bipartite, **`V ≥ 3`** | uses `4F ≤ 2E`; valid *only* for bipartite graphs |
| Non-planarity by counting | `$K_5`: `10 > 9 = 3·5−6`; `$K_{3,3}$`: `9 > 8 = 2·6−4` | the bound rejects these outright | the two canonical non-planar graphs |
| Four colour theorem | every planar graph is 4-colourable | stated as fact, not proved | the algorithmic shadow is `Δ + 1` colours greedily |
| Adjacency matrix | `$A_{ij} = 1$ if `$i,j\in E$`, else 0 | `n × n` 0/1 matrix | `O(V²)` memory, `O(1)` edge test |
| Matrix-power theorem | `$(A^{k})_{ij}$` = number of **walks** of length `k` from `i` to `j` | multiply: sum over the intermediate vertex | drives PageRank, centrality, and interleaving counts |
| Diagonal consequence | `$(A^{2})_{ii} = \deg(i)$` | a 2-walk from `v` back to `v` is neighbour-and-back | the tell that you are counting walks, not paths |
| Row sums of `Aᵏ` | total `k`-step walks anywhere in `G` | 16 for `k = 1`, 48 for `k = 2`, 142 for `k = 3` | `k = 1` recovers `2m` — the handshake lemma again |
| BFS | enqueue each vertex once; distances are shortest hop counts | `O(V + E)` | unweighted shortest paths, components, reachability |
| DFS three-colour | white / grey / black marking | cycle detection, topological sort, SCCs, bridges | `O(V + E)`; needed for weighted paths only via other tools |
| Complete graph | `$K_n$` has `$C(n,2)$` edges and degree `n−1` everywhere | everything joined to everything | `K_5` = 10 edges, `K_4` = 6 edges (bound tight) |

---

## Multiple Choice Questions

**Q1.** The build graph in the worked example has `E = {0–1, 0–2, 1–2, 1–3, 2–3,
2–4, 3–4, 4–5}`, so `|V| = 6` and `|E| = 8`. What does the handshake lemma
give you?

- A) The degrees are 2, 3, 4, 3, 3, 1, and their sum 16 must equal `2 × 8`
- B) The degrees sum to 8, because each edge contributes one degree
- C) Vertex 2 has degree 4, so `|E| = 4`
- D) The average degree is `8/6`, so the graph is sparse enough to be planar

<details>
<summary>Answer and explanation</summary>

**A) The degrees are 2, 3, 4, 3, 3, 1, and their sum 16 must equal `2 × 8`.**

`2 + 3 + 4 + 3 + 3 + 1 = 16` and `2|E| = 16`, so the check passes. The average
degree is `16/6 ≈ 2.67`, which Step 2 notes is about a third as connected as
`K₆`, where every degree would be 5.

- B) is the off-by-one that Mistake 1 of this lesson warns about: it forgets
  that each edge has *two* endpoints. The lemma is "degrees sum to twice the
  number of edges", and dropping the 2 is the standard error.
- C) is Mistake 1 in its purest form — the lemma constrains the *total* over all
  vertices, not any individual degree. `deg(2) = 4` happens to be true here
  because 2 is adjacent to 0, 1, 3 and 4, but it is not something the lemma
  tells you.
- D) is a non-sequitur. `8/6` is not the average degree — the average degree uses
  the degree *sum*, so it is `16/6`. And planarity is not settled by a density
  figure in either direction; see Q5.

</details>

**Q2.** Why is the build graph not bipartite?

- A) Because it has 8 edges and 6 vertices, so it is too dense to 2-colour
- B) Because vertices 0, 1 and 2 form a 3-cycle, and bipartite ⟺ no odd cycle
- C) Because vertex 2 has degree 4, which is even and so incompatible with two
  colours
- D) Because it contains a cycle at all, and bipartite graphs have no cycles

<details>
<summary>Answer and explanation</summary>

**B) Because vertices 0, 1 and 2 form a 3-cycle, and bipartite ⟺ no odd cycle.**

`0–1`, `1–2` and `0–2` are all edges, so those three vertices form a triangle, and
a triangle is a cycle of length 3 — odd. The lesson's step-by-step version is the
same argument in colouring form: put 0 in `X`; then 1 and 2 must both be in `Y`;
but 1 and 2 are adjacent, contradiction.

- A) is meaningless as stated. Density has nothing to do with 2-colourability: a
  star `K_{1,5}` has 5 edges on 6 vertices and is bipartite, and `K_{3,3}` has 9
  edges on 6 vertices and is also bipartite.
- C) gets the parity backwards, and parity of degree is an Euler-theorem
  condition, not a bipartiteness condition. `C₄` is bipartite with every degree
  equal to 2.
- D) is Mistake 4 of this lesson. "No odd cycles" is the criterion; "no cycles"
  is far stronger and excludes `C₄`, `C₆`, and every grid, all of which are
  bipartite.

</details>

**Q3.** Does the build graph have an Euler trail — a route using every edge
exactly once?

- A) Yes, because it has eight edges and six vertices
- B) No, because it has **four** odd-degree vertices (1, 3, 4, 5), and Euler's
  theorem allows only zero or two
- C) Yes, because it is connected
- D) No, because it contains a cycle

<details>
<summary>Answer and explanation</summary>

**B) No, because it has **four** odd-degree vertices (1, 3, 4, 5), and Euler's
theorem allows only zero or two.**

Degrees are 2, 3, 4, 3, 3, 1, so vertices 1, 3, 4 and 5 have odd degree — four
of them. A connected graph has an Euler circuit when every degree is even and an
Euler trail when exactly two are odd; four means neither, so you cannot draw the
dependency graph without lifting your pen.

- A) confuses "uses every edge" with "is possible". The edge count is
  irrelevant; the degree parities decide it.
- C) is a necessary condition, not a sufficient one. The square `0–1–2–3–0` is
  connected and has an Euler circuit because all its degrees are 2; connectivity
  alone says nothing about parity.
- D) is irrelevant to Euler trails. In fact, having a cycle is what makes Euler
  circuits *possible* in the first place — each visit to a vertex consumes edges
  in pairs, one in and one out, which is exactly why even degrees are required.

</details>

**Q4.** The build graph passes the test `E ≤ 3V − 6` since `8 ≤ 12`. What has been
established?

- A) The graph is planar
- B) The graph is not planar
- C) Nothing about planarity: the bound is necessary, not sufficient
- D) The graph is bipartite

<details>
<summary>Answer and explanation</summary>

**C) Nothing about planarity: the bound is necessary, not sufficient.**

`E ≤ 3V − 6` must hold for every simple planar graph with `V ≥ 3`, so a violation
proves non-planarity. Satisfying it proves nothing. The lesson is careful: "The
necessary condition is `E ≤ 3V − 6`: here `8 ≤ 12`, so the bound does not reject
G. It does *not* prove G is planar." To prove planarity you need a drawing; to
disprove it you need either the bound failing or a non-planarity result such as
containing `K₅` or `K₃,₃` as a minor. This is Mistake 3 of the lesson.

- A) is the over-strong reading, and Mistake 3 names it exactly: "a passing test
  feels like a green light, and the bound is famous enough to feel authoritative."
- B) is backwards — failing the bound would prove non-planarity, and this graph
  passes it. (The graph happens to *be* planar, being a triangle with two pendant
  chains, but you need a drawing to know that.)
- D) is Step 4's separate question. The triangle 0–1–2 already settles it: not
  bipartite.

</details>

**Q5.** Why is `K₅` not planar?

- A) It has 5 vertices and 10 edges, and `10 > 9 = 3V − 6`, violating the planar
  bound
- B) It has an odd cycle, so it is not bipartite, and bipartite graphs cannot be
  planar
- C) It has 4 vertices of odd degree, so it has no Euler circuit
- D) It is not connected

<details>
<summary>Answer and explanation</summary>

**A) It has 5 vertices and 10 edges, and `10 > 9 = 3V − 6`, violating the planar
bound.**

Every simple planar graph with `V ≥ 3` satisfies `E ≤ 3V − 6`, so `K₅` with
10 edges against a limit of 9 is rejected outright, with no drawing required. The
lesson's candidate table prints `E<=3V-6: FAIL` and the verdict
`NOT planar (3V-6 fails)`.

- B) is a non-sequitur wrapped in a true statement. `K₅` is indeed not bipartite,
  but many bipartite graphs are planar — `K_{3,3}` is bipartite and non-planar,
  the grid is bipartite and planar, and `K_{2,3}` is bipartite and planar.
  Non-planarity has nothing to do with bipartiteness.
- C) is a true statement about `K₅` — all four degrees are 3 — with an irrelevant
  conclusion. Euler's theorem concerns drawing the graph in one stroke, not
  drawing it without crossings.
- D) is false: `K₅` is complete and therefore connected.

</details>

**Q6.** Why is `K₃,₃` not planar, and which bound does the counting use?

- A) It has 6 vertices and 9 edges, and `9 > 9 = 3V − 6`, so the general bound
  rejects it
- B) It has 6 vertices and 9 edges, and `9 > 8 = 2V − 4`, so the **bipartite**
  bound rejects it
- C) It has odd degree vertices, so it cannot be 2-coloured
- D) It has `C(6,2) = 15` edges

<details>
<summary>Answer and explanation</summary>

**B) It has 6 vertices and 9 edges, and `9 > 8 = 2V − 4`, so the **bipartite**
bound rejects it.**

`K_{3,3}` is the complete bipartite graph with parts of size 3 and 3, so
`V = 6` and `E = 9`. Because it is bipartite — every edge runs from one part to
the other — the tighter bound `E ≤ 2V − 4` applies, and `9 > 8`. The lesson's code
notes explicitly that the bipartite bound "is only consulted for graphs that are
bipartite".

- A) applies the general bound and gets lucky in its arithmetic: `3V − 6 = 12`,
  not 9. So `9 ≤ 12` and the general bound *passes*. The stronger bipartite
  bound is the only one of the two that rejects.
- C) inverts the definition. Being bipartite means a 2-colouring **exists**;
  `K_{3,3}` has the perfectly good colouring "left part one colour, right part the
  other".
- D) counts all pairs of 6 vertices. `K_{3,3}` has only the 9 cross-part pairs as
  edges.

</details>

**Q7.** What does `(A³)ᵢⱼ` count for the adjacency matrix of a simple graph?

- A) The number of **paths** of length 3 from `i` to `j`
- B) The number of **walks** of length 3 from `i` to `j`, where vertices may be
  revisited
- C) The number of distinct vertices reachable from `i` in 3 steps
- D) The number of 3-cycles containing `i` and `j`

<details>
<summary>Answer and explanation</summary>

**B) The number of **walks** of length 3 from `i` to `j`, where vertices may be
revisited.**

Matrix multiplication sums over the intermediate vertex — `(A²)ᵢⱼ =
Σ_m A_im A_mj` counts `i → m → j` — and the same expansion compounds by induction.
The tell is the diagonal: `(A²)ᵢᵢ = deg(i)`, which is 0 for a tree but 2, 3, 4,
3, 3, 1 on the build graph's diagonal. A count of *paths* would have a zero
diagonal wherever there are no cycles.

- A) is Mistake 2 of this lesson. It is the error that hides perfectly well on
  trees, where walks and paths coincide, and surfaces the first time you meet a
  cycle — which is why the diagonal is the diagnostic to check.
- C) mixes up "count of sequences" with "size of a set". Walks are distinct
  objects; reachable *vertices* are deduplicated, and `(A³)ᵢⱼ` does no
  deduplication. Row sums of `A³` give 142 walks for the build graph, far more
  than the 6 reachable vertices.
- D) would require a cycle, and `(A^k)_{ij}` never checks that the start and end
  coincide or that the walk is simple. It counts every sequence of edges.

</details>

**Q8.** In the worked example, `(A²)₀₀ = 2`. Why?

- A) There are two shortest paths of length 2 from 0 back to 0
- B) A 2-walk from `v` to itself is exactly "step to a neighbour and back", so
  `(A²)ᵢᵢ = deg(i)`, and `deg(0) = 2`
- C) The matrix is symmetric, so the diagonal must be 2
- D) Vertex 0 appears in exactly two shortest paths to vertex 3

<details>
<summary>Answer and explanation</summary>

**B) A 2-walk from `v` to itself is exactly "step to a neighbour and back", so
`(A²)ᵢᵢ = deg(i)`, and `deg(0) = 2`.**

The two walks are `0 → 1 → 0` and `0 → 2 → 0` — 0's two neighbours. The lesson
states the general fact: "`(A²)₀₀ = 2` is the number of 2-walks from 0 back to 0:
`0 → 1 → 0` and `0 → 2 → 0`. That number is `deg(0) = 2`, exactly as the theorem
predicts, because a 2-walk from `v` to `v` is exactly a neighbour-and-back."

- A) is the same count described in the vocabulary of *paths*, and the two
  descriptions coincide here only because the walks in question do repeat
  vertices. That coincidence is precisely what makes the walk/path confusion
  survive small examples.
- C) misreads what symmetry gives. Symmetry of `A` gives `Aᵢⱼ = Aⱼᵢ`; it says
  nothing about the diagonal, whose values are the degrees. For the build graph
  the diagonal of `A²` is `[2, 3, 4, 3, 3, 1]`, not all 2s.
- D) is a different entry. The number of 2-walks from 0 to 3 is 2 — via 1 and via
  2 — which is `(A²)₀₃`, not the diagonal.

</details>

**Q9.** The row sums of `A¹` for the build graph total 16. Why does that number
look familiar?

- A) It is `|V|`, the number of vertices
- B) It is `2|E| = 16`, because each edge contributes two entries to the adjacency
  matrix — the handshake lemma, seen a second way
- C) It is the number of walks of length 1 that return to their start
- D) It is `n(n − 1)`, the maximum possible degree sum

<details>
<summary>Answer and explanation</summary>

**B) It is `2|E| = 16`, because each edge contributes two entries to the adjacency
matrix — the handshake lemma, seen a second way.**

Each undirected edge `{u, v}` puts a 1 at `(u, v)` and a 1 at `(v, u)`, so
`Σᵢⱼ Aᵢⱼ = 2|E| = 16`. The lesson notes this explicitly: "16 for `k = 1` (which
must equal `2|E| = 16` by the handshake lemma — the same fact again), 48 for
`k = 2`, and 142 for `k = 3`."

- A) is `|V| = 6`, off by nearly a factor of three. It is a natural slip because
  the matrix is indexed by vertices, but its *sum* is over entries, not vertices.
- C) describes the diagonal, whose values are the degrees and whose total is
  `2|E|` as well — but by a different count. The diagonal of `A¹` is `[0,0,0,0,0,0]`
  for a loop-free graph, so there are no such walks at all.
- D) is `6 × 5 = 30`, the degree sum of `K₆`. The build graph is far sparser than
  complete, so 16 is right and 30 is the ceiling, not the value.

</details>

**Q10.** You want to detect a cycle in a graph whose edges carry weights. Which
tool is wrong, and why?

- A) BFS, because BFS revisits vertices constantly and that is how it avoids
  re-exploring
- B) DFS with three-colour marking, because DFS is too slow on weighted graphs
- C) BFS, because it returns hop counts rather than distances, silently
- D) BFS, because weighted graphs are never connected

<details>
<summary>Answer and explanation</summary>

**C) BFS, because it returns hop counts rather than distances, silently.**

This is Mistake 5 of this lesson, and its worst feature is that BFS does not
fail — it returns a confident, wrong-shaped answer. BFS assigns `dist[v] =
dist[u] + 1`, one per hop, so on a weighted graph it reports the number of edges
on the cheapest *hop* route while any caller believes it is reporting cost. Cycle
detection itself needs the DFS three-colour marking, and weighted shortest paths
need Dijkstra, not BFS.

- A) is true but does not answer the question, and it understates the problem:
  revisiting vertices is not why BFS is *wrong* here, it is why BFS is silent.
- B) is false. DFS is `O(V + E)` on any graph, weighted or not; and it is the
  *correct* tool for cycle detection, which BFS is not.
- D) is false — weights have no bearing on connectivity. The lesson's graph
  `H` is disconnected for structural reasons, and the same `H` with weighted
  edges would be no more or less connected.

</details>

**Q11.** How many edges does any spanning tree of a connected graph on `n`
vertices have?

- A) `n`
- B) `n − 1`
- C) `C(n, 2)`
- D) `2n − 2`

<details>
<summary>Answer and explanation</summary>

**B) `n − 1`.**

A spanning tree is a connected acyclic subgraph containing every vertex. The
existence theorem says every connected graph on `n` vertices has one, and every
spanning tree has exactly `n − 1` edges. The lesson's Step 8 uses this on the
six-vertex build graph: "Any spanning tree of G has exactly `6 − 1 = 5` edges",
which is why
[Lesson 27](../part02_discrete_combinatorics/27_trees_and_spanning_trees.md) chooses
exactly 5 of the 9 candidate links.

- A) is one too many, and that is not a rounding detail: `n` edges in a connected
  graph forces at least one cycle, since the smallest cycle in a simple graph is
  a triangle formed by an edge plus an existing path.
- C) is the size of the *complete* graph on `n` vertices. It is the maximum
  possible, not what a spanning subgraph contains.
- D) is `2n − 2`, which happens to equal the number of directed arcs needed for a
  tree on `n` vertices — `n − 1` edges, each used in both directions. For an
  undirected edge list that would double-count every edge.

</details>

---

## Subjective Questions

### Short Answer

**Q1. Define *walk*, *path*, *circuit* and *cycle*. What does a path of length `k`
have?**

<details>
<summary>Answer</summary>

A **walk** is a sequence `v₀, v₁, …, v_k` with `{v_{i−1}, v_i} ∈ E` for every `i`.
A **path** is a walk in which all vertices are distinct. A **circuit** is a walk
that ends where it started. A **cycle** is a circuit whose interior vertices are
all distinct.

A path of length `k` has `k` **edges** — length counts edges, not vertices, so
`v₀ … v_k` spans `k + 1` vertices.

The distinction between walk and path is the one that matters computationally: the
adjacency matrix theorem counts walks, and the difference is invisible on trees.

</details>

**Q2. State the handshake lemma, and prove it in one sentence.**

<details>
<summary>Answer</summary>

$$\sum_{v\in V}\deg(v) = 2\lvert E\rvert$$

Count the endpoints of edges. Each edge `{u, v}` contributes one endpoint at `u`
and one at `v`, so counting endpoint-by-endpoint gives `2|E|`; counting
vertex-by-vertex gives the sum of degrees. Both count the same set of endpoints.

</details>

**Q3. State the bipartite criterion and prove it in both directions.**

<details>
<summary>Answer</summary>

**Theorem.** A graph is bipartite if and only if it contains no cycle of odd
length.

*If bipartite:* every edge flips colour, so returning to the start of a cycle of
length `k` takes `k` flips, and that is possible only for even `k`.

*Conversely:* in each connected component pick a root and colour each vertex by the
parity of the length of its path from the root. If an edge ever joined two
vertices of the same colour, the two root-paths plus that edge would close an odd
cycle. So no edge does, and the colouring works.

</details>

**Q4. State Euler's theorem on trails. What is the correct construction, and why do
the parities decide it?**

<details>
<summary>Answer</summary>

A connected graph has an **Euler circuit** — a closed trail using every edge once
— if and only if every vertex has even degree. It has an **Euler trail** (open)
if and only if exactly two vertices have odd degree. Otherwise it has neither.

Each visit to a vertex consumes edges in pairs, one arriving and one leaving, so
degrees must be even — except possibly at the two endpoints of an open trail. The
construction is **Hierholzer's algorithm**: keep walking unused edges; when stuck,
pop the vertex onto the circuit; then reverse.

</details>

**Q5. State Euler's formula and the two planar edge bounds, including every
hypothesis.**

<details>
<summary>Answer</summary>

**Euler's formula.** For a connected **plane** graph with `V` vertices, `E` edges
and `F` faces including the outer one:

$$V - E + F = 2$$

**Planar edge bound.** A simple planar graph with `V ≥ 3` has `E ≤ 3V − 6`.
Derived from Euler plus `3F ≤ 2E`.

**Bipartite planar bound.** A simple planar **and bipartite** graph with `V ≥ 3`
has `E ≤ 2V − 4`, from `4F ≤ 2E` (no triangles, so every face has length ≥ 4).

Both bounds are **necessary only**. Passing one proves nothing about planarity;
failing one proves non-planarity.

</details>

**Q6. State the adjacency-matrix theorem, and what the diagonal tells you.**

<details>
<summary>Answer</summary>

For a simple graph with adjacency matrix `A` (`Aᵢⱼ = 1` if `{i,j} ∈ E`), the
entry `(Aᵏ)ᵢⱼ` is the number of **walks** of length `k` from `i` to `j`.

Matrix multiplication sums over the intermediate vertex:
`(A²)ᵢⱼ = Σ_m A_im A_mj` counts `i → m → j`, and the same expansion compounds by
induction.

The diagnostic is the diagonal: `(A²)ᵢᵢ = deg(i)`, because a 2-walk from `v` back
to `v` is exactly a step to a neighbour and back. That is zero for a tree and
nonzero in general — the tell that you are counting walks, not paths.

</details>

### Long Answer

**Q1. Why is `E ≤ 3V − 6` necessary but not sufficient? What would you actually
need to prove planarity, and what would you need to disprove it?**

<details>
<summary>Model answer</summary>

Necessary-not-sufficient is the standard shape of a bound derived by counting, and
the derivation shows exactly why. Euler's formula gives `V − E + F = 2`, and
`3F ≤ 2E` because every face is bounded by at least 3 edges and every edge borders
exactly 2 faces. Eliminating `F` gives `E ≤ 3V − 6`. Every step in that chain is a
one-sided inequality, so the conclusion is a one-sided constraint: violating it is
a certificate of non-planarity, and satisfying it leaves you with nothing.

There is also a counting reason, and it is the more interesting one. The bound
counts *edge slots available for faces* per face, and it is tight only when every
face is a triangle. `K₄` hits `3V − 6 = 6` exactly, and so does every maximal
planar graph. But a graph can be very sparse and still non-planar: `K₃,₃` has 9
edges and 6 vertices, so `9 ≤ 12` and the general bound passes comfortably — it
takes the *bipartite* bound `E ≤ 2V − 4 = 8` to reject it. A graph can be sparse
and non-planar because non-planarity is about *how* edges are arranged, not how
many there are. Counting cannot see arrangement.

So what does it take to settle planarity?

To prove planarity you need an **embedding**: an actual drawing with no crossings,
or an algorithmically verified rotation system. That is why every planarity tool
in practice is constructive — Kuratowski-style subgraph detection, Boyer–Myrvold,
planar graph drawing libraries. The bound can never help here, because "no
crossing-free drawing exists" and "the edge count is under the limit" are simply
different statements.

To disprove planarity you have three routes, in increasing strength. The counting
bounds first: `10 > 9` rejects `K₅`, `9 > 8` rejects `K₃,₃`. Then a **Kuratowski
subgraph**: a subdivision of `K₅` or `K₃,₃` anywhere inside `G` is a certificate
of non-planarity, since subdivisions of non-planar graphs are non-planar. And
most powerfully, the **Wagner theorem** via minors: `G` is planar iff it has no
minor isomorphic to `K₅` or `K₃,₃`, and minors are what contraction-based
algorithms produce.

The practical discipline this implies: run the counting test as a cheap screen
because it costs one subtraction and catches `K₅` and `K₃,₃` outright. Never
report planarity on the strength of a passing test. And when you need the answer,
reach for the constructive route — which is exactly the situation the lesson
describes for Google Mapbox and OpenStreetMap, which "render graphs with
crossing-minimising heuristics precisely because you cannot always avoid them".

</details>

**Q2. Why does the adjacency matrix count walks rather than paths, and why is the
diagonal the fastest way to notice?**

<details>
<summary>Model answer</summary>

Because the matrix power sums over *sequences of edges*, and nothing in the
algebra enforces distinctness of vertices. The expansion is
`(Aᵏ)ᵢⱼ = Σ_{v₁, …, v_{k−1}} A_{i v₁} A_{v₁ v₂} ⋯ A_{v_{k−1} j}`, and each
product is 1 exactly when every consecutive pair is an edge. So each surviving
summand *is* a sequence `i → v₁ → ⋯ → v_{k−1} → j` of length `k` with every step
legal — and nothing in the sum forbids `v₁ = v₃`, or `v₁ = i`, or any other
repetition. Summation counts sequences; deduplication is a different operation
entirely, and there is no way to express it as a fixed matrix power. (There are
better objects for path counting — the characteristic polynomial of `A`, whose
`k`-th coefficient is the number of closed walks of length `k` — but that is a
different formula, not this one.)

The diagonal is the fastest detector because it is *always* wrong for paths and
*always* right for walks, in a way you can read off one line. `(A²)ᵢᵢ = Σ_m A_{im}
A_{mi} = Σ_m A_{im}² = deg(i)`, since a simple graph has `A_{im} ∈ {0,1}`. So the
diagonal of `A²` is the degree sequence: `[2, 3, 4, 3, 3, 1]` for the build
graph, and `[0, 0, 0, 0]` for any tree. A count of paths would have a zero
diagonal everywhere, because a path cannot revisit its start.

This matters practically because of exactly where the two coincide. On a tree,
every walk is a path, so `(Aᵏ)ᵢⱼ` computes genuine path counts and the error is
invisible. That is Mistake 2's mechanism: "`path` is the friendlier word, and for a
tree the two coincide, so the error hides until you meet a cycle." The lesson's
build graph contains the triangle 0–1–2 precisely so that the diagonal is nonzero
and the lesson's own numbers demonstrate the point.

The same walk/path gap is why `(Aᵏ)ᵢⱼ` is the right tool for some questions and the
wrong one for others. "How many execution interleavings of depth `k` are
possible?" wants walks — the lesson reports 16, 48 and 142 total walks for
`k = 1, 2, 3`, and interleavings genuinely repeat vertices. "How many distinct
routes" wants paths. Choosing wrongly does not produce an error; it produces a
plausible integer that is too large, and the only reliable test is the one the
lesson suggests: compare against a traversal that actually enforces the
constraint, such as BFS with a visited set.

</details>

**Q3. Why is BFS the right tool for reachability and unweighted shortest paths,
and the wrong tool for cycles and weighted paths? What breaks in each case?**

<details>
<summary>Model answer</summary>

The reason is structural, and it comes down to what BFS maintains: a *level*
structure. Each vertex is enqueued exactly once and stamped with
`dist[v] = dist[u] + 1`, so levels are non-decreasing in enqueue order. Two
properties fall straight out of that, and everything BFS is good at is a
consequence of them.

**Reachability and hop distance.** Because each vertex is stamped once at the
earliest level it can be reached, `dist[v]` is minimal by construction — a vertex
enqueued later from a neighbour at a smaller distance cannot happen, since that
neighbour would have been processed first. So BFS gives shortest hop count
correctly in `O(V + E)`, with each vertex visited exactly once. On the worked
graph it gives `dist = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3}` and the path
`0 → 2 → 4 → 5` to vertex 5, three hops. Components fall out for free by running
it from each unvisited vertex, which is exactly the `components` function.

**What breaks, and why.** Three separate failures, and none of them raises an
error.

*Cycles.* BFS revisits vertices constantly — that is how it avoids re-exploring
— so "BFS complained about a revisit" is a complaint about BFS, not about the
graph. Cycle detection needs the DFS three-colour marking: white (unvisited),
grey (on the current recursion stack), black (finished). An edge to a grey vertex
is a back edge and closes a cycle. The lesson is explicit that this is the tool for
"find cycles, topological sort, strongly connected components, bridge-finding".

*Weighted paths.* `dist[v] = dist[u] + 1` counts **hops**, so on a weighted graph
BFS silently reports the cheapest hop route while any caller believes it is
reporting cost. This is Mistake 5, and its danger is the silence: you get a
number, the number is plausible, and the answer is wrong. Dijkstra's fix is a
priority queue plus relaxation (`dist[v] ← min(dist[v], dist[u] + w)`), which needs
non-negative weights for the same reason BFS needs its level structure; negative
weights need Bellman–Ford, and
[Lesson 27](../part02_discrete_combinatorics/27_trees_and_spanning_trees.md)
shows exactly how Dijkstra fails when they appear.

*Topological order.* BFS cannot produce one in general because it does not carry
the recursion-stack information that makes a back edge visible. DFS can, and a
cycle in the result is a real error — the lesson notes that `make`, `ninja`,
Maven, npm and Cargo all model builds as DAGs and topologically sort them, where
a cycle is a genuine bug rather than an inconvenience.

So the rule is short: BFS for "how far, in hops" and "what is reachable"; DFS for
"is there a cycle", "what is the order", and "what are the strongly connected
pieces". Pick by the question, not by habit, because the two algorithms fail
silently and in opposite directions.

</details>

**Q4. Why is the handshake lemma so useful, and what specifically does it *not*
tell you?**

<details>
<summary>Model answer</summary>

Useful because it is the cheapest possible consistency check and it rejects
entire families of graphs at once. On the worked graph it takes one subtraction:
`2 + 3 + 4 + 3 + 3 + 1 = 16 = 2 × 8`, and any miscounted edge list fails it
immediately. The lesson leans on it as a referee on the *implementation*, not
just the mathematics — if your `degrees()` and your `edge_list` disagree, one of
them is wrong, and that is a bug you can find in a line of code.

Its real power is the parity corollary, which rejects *degree sequences* rather
than graphs. Since the sum is `2|E|`, it is always even, so an odd number of odd
degrees is impossible: a simple graph with 7 vertices cannot have all 7 vertices
of odd degree. This rejects a proposed degree sequence without constructing
anything. The degree ceiling `deg(v) ≤ n − 1`, giving `d̄ ≤ n − 1`, does the same
job from the other end — the `6` in the worked example's Exercise 1 is allowed
precisely because `n − 1 = 6`.

What it does **not** tell you, and this is where the lesson's Mistake 1 bites, is
anything about *individual* degrees. The lemma constrains the total
`Σ_v deg(v)`, not any single term. Reading a 4 out of the degree *sequence* and
concluding `deg(2) = 4` is Mistake 1 exactly: the `deg(2) = 4` happens to be
true on the build graph because 2 is adjacent to 0, 1, 3 and 4 — but it is not
something the lemma provides. Degrees can be permuted freely among vertices
without disturbing the lemma, and many sequences are graphical and many are not
while all passing the parity test.

Two more limitations worth stating plainly. First, a satisfying degree sequence
is not sufficient: the sum being even does not make the sequence realisable, and
the characterisation that does — the Erdős–Gallai inequalities — is a genuinely
harder result. Second, the lemma says nothing about *structure*: two graphs with
the same degree sequence can have completely different connectivity, cycle
structure and planarity, and the lemma cannot distinguish them. Degree sequences
are a necessary condition for being simple and connected, and a rather weak one.

The practical discipline: use the lemma as a fast assertion on every graph you
build or read, treat it as an early filter, and never let it substitute for
actually checking the property you care about — connectivity, acyclicity,
planarity, bipartiteness. Those need their own theorems, which is why the rest of
the lesson is about graphs.

</details>

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