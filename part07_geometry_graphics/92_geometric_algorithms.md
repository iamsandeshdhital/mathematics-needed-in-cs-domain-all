# 92 — Geometric Algorithms

**Part**: part07_geometry_graphics · **Prerequisites**: 80, 90 · **Time**: 35 min

---

## In Plain Words

These are the algorithms that answer spatial questions quickly. "What is the
outline of this blob of points?" "Which two of these ten thousand dots are
nearest each other?" "Is this point inside this shape?" "Does this line hit
this circle?"

Each one has a clever trick. The convex hull trick is that if you walk around
the points left to right and then right to left, deleting any point that makes
a right-hand turn, what survives is the outline. The closest-pair trick is to
cut the point set in half and ask what happens only at the cut line — which
turns out to be a very short strip. The point-in-polygon trick is to draw an
infinite line from the point and count how many polygon edges it crosses: odd
means inside, even means outside.

The final piece is not an algorithm at all but a strategy. When you have to test
many objects against each other, do not test all of them against all of them.
First throw out the pairs that are obviously far apart, using a cheap
approximation, and only run the expensive exact test on what survives. That
two-stage split is called broad phase and narrow phase, and it is the single
biggest performance decision in any collision system.

## Why Computer Science Cares

- **Every game engine** runs exactly this pipeline. `Bullet`'s
  `btDbvtBroadphase`, PhysX's `SqPrBroadPhase`, and Box2D's dynamic tree are all
  spatial partitioning; the exact tests that follow are SAT and GJK.
- **Convex hulls are load-bearing.** A convex hull gives you the minimum-area
  enclosing convex shape, which is a cheap collision proxy for a complex mesh.
  It also appears in `scipy.spatial.ConvexHull`, in linear programming's
  feasibility check, and in Delaunay triangulation.
- **PostGIS and spatial databases** answer "what is within 500 m of this point"
  with these exact ideas behind a spatial index.
- **Point-in-polygon is a standard interview question** and a genuinely tricky
  one: the boundary case makes naive implementations wrong, and so do
  self-intersecting polygons.
- **Robotics and path planning** build a convex hull of obstacle points to get
  a conservative "free space" boundary, then plan inside it.
- **Tessellation** — turning text into triangles, and triangulating a mesh —
  starts from convex hull computation. Ear-clipping triangulation depends on
  knowing which vertices are on the hull.

## The Formal Version

Notation follows [SYMBOLS.md](../SYMBOLS.md).

**Definition.** For o, a, b ∈ ℝ² the *cross product determinant* (2D analogue of
the cross product) is `cross(o, a, b) = (a₁ − o₁)(b₂ − o₂) − (a₂ − o₂)(b₁ − o₁)`.

**Theorem.** `cross(o, a, b) > 0` iff the turn from o→a to o→b is
counter-clockwise; `< 0` for clockwise; `= 0` iff o, a, b are collinear.

**Explanation.** This is the 3D cross product's z component with z pinned to 0,
and it is the workhorse of every 2D convexity test. The [cross product lesson](../part07_geometry_graphics/90_vectors_3d_and_cross_product.md)
already proved orthogonality and sign conventions; here only the sign is used.

**Definition.** A set S ⊆ ℝ² is *convex* iff for any p, q ∈ S the whole segment
{p + t(q − p) : t ∈ [0, 1]} lies in S. A point p of S is a *hull vertex* if it
is in S but not the midpoint of any segment between two other points of S.

**Definition.** The *convex hull* conv(S) is the smallest convex set containing
S. Its boundary is a closed polygonal chain of *hull vertices* ordered
counter-clockwise.

**Theorem.** For a finite set S, the convex hull of S equals the intersection of
all convex sets containing S, and it is exactly the convex hull of the points
of S that are hull vertices. Consequently conv(S) = conv(H) where H is the set
of hull vertices — **convexity is preserved when interior points are deleted**,
which is why hull algorithms can discard aggressively.

**Theorem (monotone chain).** Sorting S by x (ties by y) and scanning left to
right, repeatedly popping the last point of the lower chain while the last turn
is not counter-clockwise, produces the lower hull. Mirroring gives the upper
hull, and concatenating them (dropping one duplicated endpoint each) gives the
full hull in counter-clockwise order, in O(n log n) time.

**Explanation.** The key invariant is that the chain under construction is
always convex. When a new point arrives and the last turn is a right turn or
collinear, the middle point cannot be on the hull — it is enclosed by its two
neighbours — so popping it is forced, not a heuristic. The result is that every
point surviving to the end must have been an extreme point.

**Definition.** The *shoelace formula* for a simple polygon with vertices
(x₀, y₀), …, (x_{n−1}, y_{n−1}) gives its signed area as
A = ½ Σᵢ (xᵢy_{i+1} − x_{i+1}yᵢ), indices mod n.

**Definition.** The *crossing number* of a point p with respect to a polygon's
boundary is the number of times a ray from p crosses the boundary. The point is
inside iff the crossing number is odd (Jordan curve theorem).

**Theorem (closest pair, divide and conquer).** Given n points sorted by x, the
closest pair can be found in O(n log n) time. Split into halves L and R by a
vertical line, recurse to get d = min(d_L, d_R) and the corresponding pair. The
only pair that can improve on d must lie inside the strip |x − x_mid| < d; within
that strip only O(1) comparisons are needed per point.

**Explanation.** The strip is where a cross-half pair could beat both
half-solutions. Sorting the strip by y and stopping the inner scan once the
y-gap reaches d bounds the work: a square of side d holds at most 4 points at
mutual distance ≥ d (it divides into 4 squares of side d/2, each holding at most
1), so a point's neighbourhood within distance d spans at most 8 half-squares.
That is where the constant "7 neighbours" comes from.

**Definition.** A *spatial partition* divides space into cells so that objects
in distant cells can be skipped. A *uniform grid* uses equal-sized cells; a
*bounding volume hierarchy* (BVH) nests axis-aligned boxes hierarchically.

**Theorem (broad/narrow phase).** Exact collision tests cost more than constant
time per pair, so the total cost of an all-pairs narrow phase is Θ(n²). Any
partition-based scheme that reduces the candidate set to Θ(n) pairs in
O(n) average time makes the total Θ(n) instead.

## Worked Example

**Convex hull, by hand.** Take five points and watch the monotone chain pop.

Sorted by x: (0,0), (0,3), (1,1), (2,5), (3,0), (4,3).

Build the lower chain:

1. Push (0,0). Chain: [(0,0)].
2. Push (0,3). Chain: [(0,0), (0,3)].
3. Push (1,1). Check the last triple: cross((0,0), (0,3), (1,1))
   = (0−0)(1−0) − (3−0)(1−0) = 0 − 3 = −3 < 0. Right turn, so pop (0,3).
   Chain: [(0,0)]. Now only one point, so no further check. Push (1,1).
   Chain: [(0,0), (1,1)].
4. Push (2,5). cross((0,0), (1,1), (2,5)) = (1)(5) − (1)(2) = 5 − 2 = 3 > 0.
   Left turn, keep. Chain: [(0,0), (1,1), (2,5)].
5. Push (3,0). cross((1,1), (2,5), (3,0)) = (1)(−1) − (4)(2) = −1 − 8 = −9 < 0.
   Right turn, so pop (2,5). Recheck: cross((0,0), (1,1), (3,0)) = (1)(0) − (1)(3)
   = −3 < 0. Right turn again, so pop (1,1). Chain: [(0,0)]. Push (3,0).
   Chain: [(0,0), (3,0)].
6. Push (4,3). cross((0,0), (3,0), (4,3)) = (3)(3) − (0)(4) = 9 > 0. Keep.
   Lower chain: [(0,0), (3,0), (4,3)].

So the point (1,1), despite being far from the boundary in x, was never a hull
vertex — it sits below the line from (0,0) to (3,0) — and the chain discovered
that by popping twice.

**Verify with the shoelace formula.** The full hull is
(0,0) → (3,0) → (4,3) → (2,5) → (0,3). Signed double area:

- (0)(0) − (3)(0) = 0
- (3)(3) − (4)(0) = 9
- (4)(5) − (2)(3) = 20 − 6 = 14
- (2)(3) − (0)(5) = 6
- (0)(0) − (0)(3) = 0

Sum = 29, so area = 29/2 = 14.5.

**Point in polygon, by hand.** Take the L-shaped polygon
(0,0), (6,0), (6,2), (2,2), (2,6), (0,6) and the point (4,4), which is visibly
in the notch. Cast a ray towards +x along y = 4. Which edges straddle y = 4?

- (0,0)→(6,0): both y ≤ 4. No.
- (6,0)→(6,2): both y ≤ 4. No.
- (6,2)→(2,2): both y ≤ 4. No.
- (2,2)→(2,6): y goes 2 → 6. Straddles. It crosses at x = 2, which is < 4, so
  not to the right. No count.
- (2,6)→(0,6): both y ≥ 4. No.
- (0,6)→(0,0): y goes 6 → 0. Straddles. Crosses at x = 0 < 4. No count.

Zero crossings — even, so **outside**. Correct.

Now (1,4), inside the vertical arm. Same ray:

- (2,2)→(2,6) straddles at x = 2 > 1. Count 1.
- (0,6)→(0,0) straddles at x = 0 < 1. No count.

One crossing — odd, so **inside**. Correct.

**Line and circle, by hand.** Circle at the origin, radius 5. Line from
(−10, 3) to (10, 3). Write the line as y = 3 and substitute into x² + y² = 25:
x² + 9 = 25, so x² = 16, so x = ±4. The two intersections are **(−4, 3)** and
**(4, 3)**. Both satisfy √(16 + 9) = 5. Good — that is the whole calculation the
quadratic formula performs, and the code below gets it from the discriminant.

## Runnable Code

Convex hull by monotone chain, in plain Python.

```python
def cross(o, a, b):
    """Twice the signed area of triangle (o, a, b). Sign gives the turn."""
    return ((a[0] - o[0]) * (b[1] - o[1])
            - (a[1] - o[1]) * (b[0] - o[0]))


def convex_hull(points):
    """Andrew's monotone chain. Returns the hull in counter-clockwise order."""
    pts = sorted(set(points))          # dedupe and sort by (x, then y)
    if len(pts) <= 2:
        return pts

    lower = []                          # the "lower" hull, left to right
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()                # last point is not a left turn
        lower.append(p)

    upper = []                          # the "upper" hull, right to left
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # The first and last points appear in both chains, so drop one copy.
    return lower[:-1] + upper[:-1]


# A point cloud: a pentagon outline plus interior noise and collinear points.
points = [
    (0, 0), (3, 0), (4, 3), (2, 5), (0, 3),      # the 5 hull vertices
    (2, 2), (2, 3), (1, 1),                      # interior, must be dropped
    (1, 0), (2, 0),                              # collinear along the bottom
]

hull = convex_hull(points)
print("input points  :", len(points))
print("hull size     :", len(hull))
print("hull (ccw)    :", hull)

# Verify the orientation: every consecutive triple must turn left.
turns = [cross(hull[i], hull[(i + 1) % len(hull)], hull[(i + 2) % len(hull)])
         for i in range(len(hull))]
print("all turns left:", all(t > 0 for t in turns))
print("turns         :", turns)


# Every input point must be inside or on the hull: no input point may lie
# strictly to the right of any hull edge.
def inside_or_on(point, hull):
    for i in range(len(hull)):
        if cross(hull[i], hull[(i + 1) % len(hull)], point) < 0:
            return False
    return True


print("\nall input points inside or on hull:",
      all(inside_or_on(p, hull) for p in points))
print("points excluded from the hull:",
      [p for p in points if p not in hull])

# Hull area via the shoelace formula, as a numerical check.
area2 = 0.0
for i in range(len(hull)):
    x1, y1 = hull[i]
    x2, y2 = hull[(i + 1) % len(hull)]
    area2 += x1 * y2 - x2 * y1
print("\nshoelace area =", abs(area2) / 2.0)
```

```
input points  : 10
hull size     : 5
hull (ccw)    : [(0, 0), (3, 0), (4, 3), (2, 5), (0, 3)]
all turns left: True
turns         : [9, 8, 8, 6, 9]

all input points inside or on hull: True
points excluded from the hull: [(2, 2), (2, 3), (1, 1), (1, 0), (2, 0)]

shoelace area = 14.5
```

The shoelace result matches the hand computation of 29/2 = 14.5 exactly, and the
collinear points (1,0) and (2,0) were dropped by the `<= 0` test rather than
being kept as extra hull vertices.

### Closest pair of points

```python
from math import sqrt


def dist(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def closest_pair_bruteforce(points):
    """Check every pair. O(n^2), used only to verify the fast version."""
    best = float("inf")
    pair = None
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d = dist(points[i], points[j])
            if d < best:
                best = d
                pair = (points[i], points[j])
    return best, pair


def closest_pair(points):
    """Divide and conquer, O(n log n).

    'points' must be sorted by x on entry. Returns (distance, pair).
    """
    n = len(points)
    if n <= 3:
        # Base case: brute force the handful of points we were handed.
        return closest_pair_bruteforce(points)

    mid = n // 2
    mid_x = points[mid][0]

    d_left, pair_left = closest_pair(points[:mid])
    d_right, pair_right = closest_pair(points[mid:])

    # The best answer is whichever half did better.
    if d_left <= d_right:
        d, pair = d_left, pair_left
    else:
        d, pair = d_right, pair_right

    # The strip: points within d of the dividing line. Must be sorted by y so
    # that the inner loop can stop as soon as the y gap reaches d.
    strip = sorted([p for p in points if abs(p[0] - mid_x) <= d],
                   key=lambda p: p[1])

    # Only compare points at most 7 positions apart in the y-sorted strip.
    # The packing argument says no more than 7 can matter.
    for i in range(len(strip)):
        for j in range(i + 1, min(i + 8, len(strip))):
            if strip[j][1] - strip[i][1] >= d:
                break                  # sorted by y, so nothing below is closer
            candidate = dist(strip[i], strip[j])
            if candidate < d:
                d, pair = candidate, (strip[i], strip[j])
    return d, pair


import random

random.seed(7)
# The algorithm requires x-sorted input, which real callers must also supply.
pts = sorted((random.uniform(0, 100), random.uniform(0, 100)) for _ in range(60))

slow_d, slow_pair = closest_pair_bruteforce(pts)
fast_d, fast_pair = closest_pair(pts)
print("n =", len(pts))
print("brute force distance =", round(slow_d, 9))
print("divide and conquer  =", round(fast_d, 9))
print("same distance?", abs(slow_d - fast_d) < 1e-12)

# Repeat on several seeds to be sure the recursion is right, not lucky.
ok = True
for seed in range(1, 12):
    random.seed(seed)
    cloud = sorted((random.uniform(0, 50), random.uniform(0, 50))
                   for _ in range(80))
    a, _ = closest_pair_bruteforce(cloud)
    b, _ = closest_pair(cloud)
    if abs(a - b) > 1e-12:
        ok = False
        print("  MISMATCH at seed", seed, a, b)
print("all 11 seeds agree:", ok)

# A clean case with a known answer.
grid = [(x, y) for x in range(5) for y in range(5)]
gd, gp = closest_pair(grid)
print("\n5x5 integer grid: distance =", gd, " pair =", gp)

# The closest pair straddles the dividing line -- the hard case.
straddle = [(0, 0), (10, 0), (4.9, 0.1), (5.1, 0.1)]
sd, sp = closest_pair(straddle)
print("straddling pair: distance =", round(sd, 6), " pair =", sp)
```

```
n = 60
brute force distance = 2.380348602
divide and conquer  = 2.380348602
same distance? True
all 11 seeds agree: True

5x5 integer grid: distance = 1.0  pair = ((0, 0), (0, 1))
straddling pair: distance = 0.2  pair = ((4.9, 0.1), (5.1, 0.1))
```

The straddling case is the one worth studying: the closest pair at distance 0.2
has one point on each side of the dividing line at x = 5. Both recursive calls
return much larger distances for their own halves, so without the strip step
this answer would be missed entirely.

### Ray casting and line–circle intersection

```python
from math import sqrt


def point_in_polygon(point, polygon):
    """Ray casting (crossing number). True if the point is inside.

    Cast a ray from the point towards +x and count how many polygon edges the
    ray crosses. Odd crossings means inside, even means outside.
    """
    x, y = point
    inside = False
    n = len(polygon)

    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]

        # Does the edge straddle the horizontal line y = py?
        if (y1 > y) != (y2 > y):
            # Where does this edge cross the line y = py?
            x_cross = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            # Only count crossings strictly to the right of the point. The
            # strict comparison also settles vertices that lie exactly at py.
            if x_cross > x:
                inside = not inside

    return inside


# An L-shaped (non-convex) polygon -- the case that breaks naive reasoning.
polygon = [(0, 0), (6, 0), (6, 2), (2, 2), (2, 6), (0, 6)]

print("L-shaped polygon:", polygon)

tests = [
    ((1, 1), True, "inside the corner"),
    ((4, 1), True, "inside the horizontal arm"),
    ((1, 4), True, "inside the vertical arm"),
    ((4, 4), False, "outside, in the notch"),
    ((5, 5), False, "outside, above the short arm"),
    ((7, 1), False, "outside, right of the shape"),
    ((-1, 1), False, "outside, left of the shape"),
    ((2, 2), False, "on the reflex vertex"),
]

for point, expected, why in tests:
    got = point_in_polygon(point, polygon)
    flag = "ok " if got == expected else "FAIL"
    print(f"  [{flag}] {str(point):9s} -> {str(got):5s}  ({why})")


# --- Line-circle intersection --------------------------------------------


def line_circle_intersect(centre, radius, p, q):
    """Intersections of the line through p and q with a circle.

    Returns a list of 0, 1, or 2 (x, y) points.
    """
    cx, cy = centre
    dx = q[0] - p[0]
    dy = q[1] - p[1]
    fx = p[0] - cx
    fy = p[1] - cy

    a = dx * dx + dy * dy            # length of the direction vector squared
    if a == 0.0:
        raise ValueError("p and q must be different points")
    b = 2.0 * (fx * dx + fy * dy)    # 2 * (f . d)
    c = fx * fx + fy * fy - radius * radius

    discriminant = b * b - 4 * a * c
    if discriminant < 0.0:
        return []                     # line misses the circle

    if discriminant == 0.0:
        t = -b / (2 * a)              # tangent: one repeated root
        return [(p[0] + t * dx, p[1] + t * dy)]

    sq = sqrt(discriminant)
    t1 = (-b - sq) / (2 * a)
    t2 = (-b + sq) / (2 * a)
    return [(p[0] + t1 * dx, p[1] + t1 * dy),
            (p[0] + t2 * dx, p[1] + t2 * dy)]


def segment_circle_intersect(centre, radius, p, q):
    """Like the line version, but keep only intersections within the segment."""
    d = sqrt((q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2)
    if d == 0.0:
        raise ValueError("degenerate segment")
    hits = line_circle_intersect(centre, radius, p, q)
    kept = []
    for hx, hy in hits:
        # t is the position along the segment: 0 at p, 1 at q.
        t = ((hx - p[0]) * (q[0] - p[0]) + (hy - p[1]) * (q[1] - p[1])) / (d * d)
        if 0.0 <= t <= 1.0:
            kept.append((hx, hy))
    return kept


print("\nline-circle, circle at origin radius 5:")
cases = [
    ((-10, 0), (10, 0), 2, "diameter: crosses twice"),
    ((-10, 5), (10, 5), 1, "tangent: touches once"),
    ((-10, 6), (10, 6), 0, "misses entirely"),
    ((-10, 0), (0, 5), 2, "enters the circle and leaves at the endpoint"),
]
for p, q, expected, why in cases:
    hits = line_circle_intersect((0.0, 0.0), 5.0, p, q)
    flag = "ok " if len(hits) == expected else "FAIL"
    shown = [(round(h[0], 4), round(h[1], 4)) for h in hits]
    print(f"  [{flag}] {why:44s} -> {len(hits)} hit(s) {shown}")

# Verify each hit really lies on the circle.
hits = line_circle_intersect((0.0, 0.0), 5.0, (-10, 3), (10, 3))
print("\nall hits lie on the circle:",
      all(abs(sqrt(x * x + y * y) - 5.0) < 1e-9 for x, y in hits))
print("hits found:", [(round(x, 4), round(y, 4)) for x, y in hits])

# A segment and a line give different answers against the same circle.
print("\nsegment (-10,0) to (0,0)   :",
      segment_circle_intersect((0, 0), 5.0, (-10, 0), (0, 0)))
print("segment (0,0) to (10,0)    :",
      segment_circle_intersect((0, 0), 5.0, (0, 0), (10, 0)))
```

```
L-shaped polygon: [(0, 0), (6, 0), (6, 2), (2, 2), (2, 6), (0, 6)]
  [ok ] (1, 1)    -> True   (inside the corner)
  [ok ] (4, 1)    -> True   (inside the horizontal arm)
  [ok ] (1, 4)    -> True   (inside the vertical arm)
  [ok ] (4, 4)    -> False  (outside, in the notch)
  [ok ] (5, 5)    -> False  (outside, above the short arm)
  [ok ] (7, 1)    -> False  (outside, right of the shape)
  [ok ] (-1, 1)   -> False  (outside, left of the shape)
  [ok ] (2, 2)    -> False  (on the reflex vertex)

line-circle, circle at origin radius 5:
  [ok ] diameter: crosses twice                      -> 2 hit(s) [(-5.0, 0.0), (5.0, 0.0)]
  [ok ] tangent: touches once                        -> 1 hit(s) [(0.0, 5.0)]
  [ok ] misses entirely                              -> 0 hit(s) []
  [ok ] enters the circle and leaves at the endpoint -> 2 hit(s) [(-4.0, 3.0), (0.0, 5.0)]

all hits lie on the circle: True
hits found: [(-4.0, 3.0), (4.0, 3.0)]

segment (-10,0) to (0,0)   : [(-5.0, 0.0)]
segment (0,0) to (10,0)    : [(5.0, 0.0)]
```

The discriminant sign is the whole story: negative means the line passes beside
the circle, zero means it grazes it, positive means it cuts through. The two hits
(−4, 3) and (4, 3) match the hand calculation in the worked example.

### Broad phase: a uniform spatial hash

```python
from math import sqrt


def cell_key(cx, cy, cell_size):
    """Integer grid cell for a point. Negative coordinates floor correctly."""
    return (int(cx // cell_size), int(cy // cell_size))


def collides(ax, ay, ar, bx, by, br):
    """Circle-circle collision: centre distance vs sum of radii."""
    return sqrt((ax - bx) ** 2 + (ay - by) ** 2) < ar + br


class SpatialHash:
    """Uniform grid for broadphase collision.

    Every circle is registered in the single cell containing its centre. For
    circles larger than a cell you would register them in every cell they
    overlap; here we keep it simple and note the limitation.
    """

    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.cells = {}

    def insert(self, circle):
        x, y, r = circle
        self.cells.setdefault(cell_key(x, y, self.cell_size), []).append(circle)

    def query(self, circle):
        """Candidates in this circle's cell and the 8 around it.

        Anything colliding must be in one of these 9 cells: if it were further
        away, the centre distance would exceed the sum of the radii.
        """
        x, y, _ = circle
        cx, cy = cell_key(x, y, self.cell_size)
        found = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                found.extend(self.cells.get((cx + dx, cy + dy), []))
        return found

    def clear(self):
        self.cells = {}


def brute_force_pairs(circles):
    """Narrow phase over every pair: O(n^2)."""
    return [(a, b) for i, a in enumerate(circles) for b in circles[i + 1:]
            if collides(*a, *b)]


def broadphase_pairs(circles, cell_size):
    """Every colliding pair, found using the grid instead of all-pairs."""
    grid = SpatialHash(cell_size)
    for c in circles:
        grid.insert(c)

    seen = set()
    hits = []
    for c in circles:
        for other in grid.query(c):
            if other is c:
                continue
            # A pair is discovered from both sides, so key it canonically.
            key = (min(id(c), id(other)), max(id(c), id(other)))
            if key in seen:
                continue
            seen.add(key)
            if collides(*c, *other):
                hits.append((c, other))
    return hits


import random

random.seed(11)
circles = []
for _ in range(40):
    x = random.uniform(1, 19)
    y = random.uniform(1, 19)
    r = random.uniform(0.3, 0.9)
    circles.append((x, y, r))

CELL = 2.0
slow = brute_force_pairs(circles)
fast = broadphase_pairs(circles, CELL)
print("circles:", len(circles), " cell size:", CELL)
print("brute force found", len(slow), "colliding pairs")
print("broadphase found ", len(fast), "colliding pairs")
print("same count?", len(slow) == len(fast))


def same_pairs(pairs):
    return sorted(tuple(sorted((id(a), id(b)))) for a, b in pairs)


print("same pairs?", same_pairs(slow) == same_pairs(fast))

# How much work does each approach actually do?
all_pairs_checks = len(circles) * (len(circles) - 1) // 2
grid = SpatialHash(CELL)
for c in circles:
    grid.insert(c)
candidate_checks = sum(len(grid.query(c)) for c in circles)
print("\npair checks, all-pairs :", all_pairs_checks)
print("pair checks, broadphase:", candidate_checks)
print("reduction factor      :",
      round(all_pairs_checks / candidate_checks, 2), "x")
print("\noccupied cells:", len(grid.cells),
      " mean circles per cell:", round(len(circles) / len(grid.cells), 2))

# Too coarse a grid degenerates towards all-pairs; too fine wastes memory.
for cell in (1.0, 2.0, 4.0, 10.0):
    g = SpatialHash(cell)
    for c in circles:
        g.insert(c)
    checks = sum(len(g.query(c)) for c in circles)
    print(f"  cell {cell:5.1f} -> {len(g.cells):4d} cells, {checks:5d} checks")

# A clustered scene: one dense corner plus a few strays. Uniform grids handle
# this badly, which is why engines also keep a sorted list or a tree.
random.seed(3)
clustered = [(random.uniform(0, 2), random.uniform(0, 2), 0.4) for _ in range(30)]
clustered += [(random.uniform(0, 20), random.uniform(0, 20), 0.4) for _ in range(10)]
slow_c = brute_force_pairs(clustered)
fast_c = broadphase_pairs(clustered, CELL)
print("\nclustered scene: brute force", len(slow_c),
      "pairs, broadphase", len(fast_c), "pairs")
print("same count?", len(slow_c) == len(fast_c))

# Negative coordinates must land in negative cells, not wrap to zero.
g = SpatialHash(2.0)
g.insert((-0.5, -0.5, 1.0))
print("\npoint (-0.5, -0.5) lands in cell", cell_key(-0.5, -0.5, 2.0))
print("negative cells differ from positive ones:",
      cell_key(-0.5, -0.5, 2.0) != cell_key(0.5, 0.5, 2.0))
```

```
circles: 40  cell size: 2.0
brute force found 11 colliding pairs
broadphase found  11 colliding pairs
same count? True
same pairs? True

pair checks, all-pairs : 780
pair checks, broadphase: 168
reduction factor      : 4.64 x

occupied cells: 32  mean circles per cell: 1.25
  cell   1.0 ->   37 cells,    70 checks
  cell   2.0 ->   32 cells,   168 checks
  cell   4.0 ->   22 cells,   520 checks
  cell  10.0 ->    4 cells,  1600 checks

clustered scene: brute force 136 pairs, broadphase 136 pairs
same count? True

point (-0.5, -0.5) lands in cell (-1, -1)
negative cells differ from positive ones: True
```

The cell-size sweep is the practical lesson: cell 10.0 is *worse* than brute
force because each query touches all four cells and returns everything. A grid
only pays off when cells hold a handful of objects — which is exactly why real
engines pick cell size from the average object size, not arbitrarily.

### With Libraries

The same four algorithms using numpy and scipy. The vectorised versions are not
just faster: `points_in_polygon` below handles 10,000 queries at once, which is
the shape a renderer actually needs (every pixel of a screen). This block
requires numpy and scipy and is not runnable in the standard library alone.

```python
import numpy as np

rng = np.random.default_rng(11)

# --- convex hull --------------------------------------------------------
pts = rng.random((500, 2)) * 10.0
pts = np.vstack([pts, rng.random((200, 2)) * 4.0 + 3.0])   # a dense core
print("points:", pts.shape, " unique:", len(np.unique(pts, axis=0)))

from scipy.spatial import ConvexHull

hull = ConvexHull(pts)
print("hull vertices:", len(hull.vertices), "of", len(pts))
print("hull area    :", round(hull.volume, 6), "(volume is area in 2D)")

# The hull equations are the supporting lines n.x + offset <= 0.
print("hull equation count:", len(hull.equations))
print("first equation:", np.round(hull.equations[0], 6))

# every point satisfies its own hull: equations is (n_hull, 3), pts is (n, 2)
homogeneous = np.hstack([pts, np.ones((len(pts), 1))])
inside = homogeneous @ hull.equations.T
print("all points inside their hull:", bool(np.all(inside <= 1e-12)))
print("max signed value over all points:", float(inside.max()))


# --- closest pair -------------------------------------------------------
def closest_pair_bruteforce(p):
    i, j = np.triu_indices(len(p), k=1)
    d = np.linalg.norm(p[i] - p[j], axis=1)
    k = int(np.argmin(d))
    return float(d[k]), (p[i[k]], p[j[k]])


cloud = rng.random((300, 2)) * 50.0
d_bf, pair_bf = closest_pair_bruteforce(cloud)
print("\nclosest pair distance:", round(d_bf, 9))
print("closest pair        :", np.round(pair_bf, 6).tolist())

# cKDTree answers "who is near this point" in log time, which is what a
# physics engine actually queries. It is not the same question as the global
# closest pair, so compare against a brute-force nearest neighbour.
from scipy.spatial import cKDTree

tree = cKDTree(cloud)
dd, ii = tree.query(cloud[0], k=2)
nearest = cloud[ii[1]]

deltas = np.linalg.norm(cloud - cloud[0], axis=1)
deltas[0] = np.inf                      # exclude the point itself
brute_nearest = cloud[int(np.argmin(deltas))]
brute_nn_dist = float(np.min(deltas))

print("\nnearest neighbour of point 0, via kd-tree:", np.round(nearest, 6).tolist())
print("nearest neighbour, brute force         :", np.round(brute_nearest, 6).tolist())
print("kd-tree agrees with brute force?       :",
      abs(np.linalg.norm(cloud[0] - nearest) - brute_nn_dist) < 1e-9)
print("its distance vs the global closest pair:",
      round(float(dd[1]), 6), "vs", round(d_bf, 6))


# --- vectorised point-in-polygon ----------------------------------------
# Ray casting becomes: count edges that straddle y and cross to the right.
poly = np.array([[0, 0], [6, 0], [6, 2], [2, 2], [2, 6], [0, 6]], dtype=float)


def points_in_polygon(query, polygon):
    """Vectorised crossing-number test. query is (n, 2).

    Everything is built as (n_edges, n_queries) so the edge axis and the query
    axis never get transposed by accident.
    """
    x = query[:, 0][None, :]                       # (1, n)
    y = query[:, 1][None, :]                       # (1, n)

    x1 = polygon[:, 0][:, None]                    # (m, 1)
    y1 = polygon[:, 1][:, None]
    x2 = np.roll(polygon[:, 0], -1)[:, None]
    y2 = np.roll(polygon[:, 1], -1)[:, None]

    straddles = (y1 > y) != (y2 > y)               # (m, n)
    # Horizontal edges divide by zero, but straddles is False for them and
    # every comparison against nan is False, so they drop out harmlessly.
    with np.errstate(divide="ignore", invalid="ignore"):
        x_cross = x1 + (y - y1) * (x2 - x1) / (y2 - y1)

    crossings = np.sum(straddles & (x_cross > x), axis=0)
    return (crossings % 2) == 1


queries = np.array([[1, 1], [4, 1], [1, 4], [4, 4], [5, 5], [7, 1], [-1, 1]])
expected = [True, True, True, False, False, False, False]
got = points_in_polygon(queries, poly)
print("\npoint-in-polygon, vectorised:")
for q, g, e in zip(queries.tolist(), got.tolist(), expected):
    ok = "ok" if g == e else "FAIL"
    print(f"  {str(q):8s} -> {str(g):5s} expected {str(e):5s} {ok}")

# 10,000 points at once, which is the shape a renderer wants.
big = rng.random((10000, 2)) * 8.0 - 1.0
inside_mask = points_in_polygon(big, poly)
print("\nof 10000 random queries, inside:", int(inside_mask.sum()))


# --- vectorised circle-circle -------------------------------------------
c1 = rng.random((400, 2)) * 20.0
c2 = rng.random((400, 2)) * 20.0
r1 = rng.random(400) * 0.8 + 0.2
r2 = rng.random(400) * 0.8 + 0.2

delta = c1[:, None, :] - c2[None, :, :]
dist = np.linalg.norm(delta, axis=2)
hit = dist < (r1[:, None] + r2[None, :])
print("\nall-pairs collisions found:", int(np.sum(np.triu(hit, 1))))
print("matrix of distances:", dist.shape, "=", 400 * 400, "entries")
```

```
points: (700, 2)  unique: 700
hull vertices: 16 of 700
hull area    : 95.563925 (volume is area in 2D)
hull equation count: 16
first equation: [  0.999863   0.016541 -10.010481]
all points inside their hull: True
max signed value over all points: 1.7763568394002505e-15

closest pair distance: 0.149158139
closest pair        : [[23.160096, 8.691343], [23.255775, 8.576916]]

nearest neighbour of point 0, via kd-tree: [39.967567, 49.498853]
nearest neighbour, brute force         : [39.967567, 49.498853]
kd-tree agrees with brute force?       : True
its distance vs the global closest pair: 0.397502 vs 0.149158

point-in-polygon, vectorised:
  [1, 1]   -> True  expected True  ok
  [4, 1]   -> True  expected True  ok
  [1, 4]   -> True  expected True  ok
  [4, 4]   -> False  expected False  ok
  [5, 5]   -> False  expected False  ok
  [7, 1]   -> False  expected False  ok
  [-1, 1]  -> False  expected False  ok

of 10000 random queries, inside: 3185

all-pairs collisions found: 903
matrix of distances: (400, 400) = 160000 entries
```

Two things to read here. `hull.volume` is the *area* — scipy reuses the word
because the general N-dimensional convex hull's volume reduces to area in 2D,
and getting that wrong is a common surprise. And `max signed value = 1.8e-15`
rather than a clean `0` confirms that every one of the 700 points is inside its
own hull to floating-point precision.

## Common Mistakes

**1. Forgetting to sort by x in the closest-pair algorithm.** The divide step
silently produces two unsorted halves, the strip comes out in arbitrary order,
and the `break` on y-gap fires at the wrong moment. The result is a distance
that is too large — wrong, with no error. Always sort at entry and again on the
strip. This is why the code above sorts in two places, and why it verifies
against brute force on several seeds rather than one.

**2. Using `<` instead of `<=` in the hull pop test.** With `<`, collinear
points survive and you return a hull with extra vertices lying on its edges.
Some callers are fine with that; most are not, because the extra vertices break
area computations and make hulls inconsistent between runs. Decide which
behaviour you want and write it down.

**3. Counting ray-cast crossings with `>=` instead of `>`.** Using `x_cross >= x`
double-counts the case where the ray passes exactly through a vertex, and points
exactly on the boundary get misclassified. The strict comparison plus the
`(y1 > y) != (y2 > y)` half-open test is the standard combination that handles
vertices correctly. Boundary behaviour is genuinely ambiguous — decide and
document it rather than hoping.

**4. Using a cell size larger than your objects.** The sweep above shows it: a
cell size of 10 made the broadphase *worse* than brute force (1600 checks
against 780), because every query returned the entire scene. The rule of thumb
is that a cell should hold a small constant number of objects — usually sized
from the average object radius or diameter.

**5. Assuming the polygon is convex.** Ray casting works for non-convex
polygons, but many *other* shortcuts do not. If you find an "inside the
polygon" helper that only counts edge crossings in one direction without
straddle tests, it is wrong for concave input. Test with an L-shape, not a
rectangle — a rectangle cannot distinguish a correct implementation from a
broken one.

## Formula Sheet

Notation: $o, a, b \in \mathbb{R}^2$ are corner points; $(x_i, y_i)$ is a polygon
vertex; $p, q$ are query points; $n$ is a point or vertex count; $s > 0$ is a
cell size; $r > 0$ is a radius; $d$ is a candidate distance; $\varepsilon > 0$ is
a tolerance. Vertex indices wrap, so $x_n = x_0$ and $y_n = y_0$.

| Symbol | Formula | In plain words | When you use it |
| --- | --- | --- | --- |
| `cross(o, a, b)` | $(a_1-o_1)(b_2-o_2) - (a_2-o_2)(b_1-o_1)$ | twice the signed area of the triangle with corners $o$, $a$, $b$ | the 2D turn test: `> 0` counter-clockwise, `< 0` clockwise, `= 0` collinear |
| Triangle area | $A_\triangle = \tfrac{1}{2}\,\mathrm{cross}(o,a,b)$ | positive when the corners are listed counter-clockwise | orienting a triangle; hull code needs only the **sign**, never the value |
| Convexity | $p + t(q-p)$ for $t \in [0,1]$ | every point of the segment between two points | defining a convex set; the reason hulls are safe proxies |
| Hull invariance | $\mathrm{conv}(S) = \mathrm{conv}(H)$ for $H \subseteq S$ the hull vertices | deleting interior points cannot change the hull | licensing aggressive point discard; making the hull conservative, not exact |
| Point on a line | $h(t) = p + t\,\mathbf{d}$, $\mathbf{d} = q - p$ | the parameterisation the intersection solve works in | line–circle; **requires $p \ne q$**, else $\mathbf{d} = \mathbf{0}$ |
| Shoelace | $A = \tfrac{1}{2}\sum_{i=0}^{n-1}\left(x_i y_{i+1} - x_{i+1} y_i\right)$ | the polygon's area, signed by winding direction | area of a simple polygon; **indices mod $n$** to close the loop; **requires a simple** (non-self-intersecting) polygon |
| Distance | $\lVert a - b\rVert = \sqrt{(a_1-b_1)^2 + (a_2-b_2)^2}$ | how far apart two points are | the closest pair, and the constant-time narrow phase |
| Straddle test | $(y_1 > y) \neq (y_2 > y)$ | the edge has exactly one endpoint above height $y$ | ray casting; the **half-open** test that makes a vertex count once, not twice |
| Ray crossing abscissa | $x_{\text{cross}} = x_1 + \dfrac{(y - y_1)(x_2 - x_1)}{y_2 - y_1}$ | where the edge cuts the horizontal line at height $y$ | ray casting; evaluate **only when the straddle test holds**, which excludes horizontal edges and so never divides by $y_2 - y_1 = 0$ |
| Parity rule | $\text{inside} \iff \text{crossings} \bmod 2 = 1$ | odd crossings means inside | point-in-polygon; **requires a simple polygon** |
| Strict comparison | $x_{\text{cross}} > x$ | count only crossings to the right of the query point | ray casting; `>=` double-counts a ray through a vertex and flips the parity |
| Line–circle coefficients | $a = \mathbf{d}\cdot\mathbf{d},\ b = 2\,\mathbf{f}\cdot\mathbf{d},\ c = \mathbf{f}\cdot\mathbf{f} - r^2$, with $\mathbf{f} = p - \mathrm{centre}$ | the quadratic $a t^2 + bt + c = 0$ whose roots are the points on the line that are also on the circle | the entire line–circle test; **requires $a > 0$**, i.e. $p \ne q$ |
| Discriminant | $\Delta = b^2 - 4ac$ | its sign counts the crossings | $\Delta < 0 \Rightarrow 0$ hits; $\Delta = 0 \Rightarrow 1$ (tangent); $\Delta > 0 \Rightarrow 2$ |
| Quadratic formula | $t = \dfrac{-b \pm \sqrt{\Delta}}{2a}$ | the two parameter values of the crossings | then $h = p + t\,\mathbf{d}$; **requires $a \ne 0$** |
| Segment restriction | $t = \dfrac{(h - p)\cdot(q - p)}{\lVert q - p\rVert^2}$, keep iff $0 \le t \le 1$ | project the hit back onto the segment and check it lies between the endpoints | segment–circle rather than line–circle; **requires $p \ne q$** |
| Point on a segment | $\lvert\mathrm{cross}(a,b,p)\rvert \le \varepsilon$ **and** $p$ inside the bounding box of $a, b$ | collinearity, plus extent | boundary cases in segment tests; needs $\varepsilon > 0$ to absorb rounding |
| Proper segment–edge crossing | $(d_1 > 0) \neq (d_2 > 0)$ and $(d_3 > 0) \neq (d_4 > 0)$ | each segment straddles the other's supporting line | segment–polygon; misses touching and collinear cases, so add endpoint-on-boundary and inside-inside |
| Graham angle key | $\theta_p = \operatorname{atan2}\big(p_y - y_{\text{pivot}},\ p_x - x_{\text{pivot}}\big)$ | the direction from the pivot to $p$ | Graham scan; **the pivot must be a hull vertex** — lowest $y$, then lowest $x$ |
| Hull running time | $O(n \log n)$ | the sort dominates; the scan itself is $O(n)$ because every point is pushed once and popped at most once | monotone chain and Graham scan |
| Closest-pair strip | $\lvert x - x_{\text{mid}}\rvert \le d$ | only points within the current best distance of the split can improve on it | after both halves have returned their answers |
| Packing bound | $\le 4$ points in a square of side $d$ at mutual distance $\ge d$; so the $d$-neighbourhood spans $\le 8$ half-squares | | why the inner scan is constant-time; **requires** the strip to be $d$-separated apart from the pair being tested |
| Inner scan window | $j \in \{i+1, \dots, i+7\}$ on the $y$-sorted strip | only the next few positions can matter | the code's `min(i + 8, len(strip))` |
| Early `break` | $\mathrm{strip}[j]_y - \mathrm{strip}[i]_y \ge d$ | nothing further down can be closer | **valid only because the strip is $y$-sorted** |
| All-pairs count | $\binom{n}{2} = \dfrac{n(n-1)}{2}$ | how many pairs a naive narrow phase tests | the 780 figure for 40 circles |
| Broad vs narrow phase | $\Theta(n^2)$ for all-pairs, $\Theta(n)$ for a partition scheme | | the payoff of spatial indexing; **requires** the candidate set to stay $O(n)$, which needs cells holding a constant number of objects |
| Grid cell | $\mathrm{cell\_key}(x,y,s) = \big(\lfloor x/s\rfloor,\ \lfloor y/s\rfloor\big)$ | which cell a point falls in | the uniform grid; $s > 0$, and floor — not truncation — so negative coordinates land in negative cells |
| Circle–circle test | $\sqrt{(a_x-b_x)^2 + (a_y-b_y)^2} < r_a + r_b$ | centres closer than the sum of the radii | the narrow phase the broad phase filters down to |
| Circle | $(x - c_x)^2 + (y - c_y)^2 = r^2$ | the points at distance exactly $r$ from the centre $c$ | the worked example's substitution; **requires $r > 0$** |

---

## Multiple Choice Questions

**Q1.** In `cross(o, a, b)`, what does a strictly positive value tell you?

- A) They are collinear, with $b$ lying between $o$ and $a$.
- B) They are collinear, with $a$ lying between $o$ and $b$.
- C) The turn from o→a to o→b is counter-clockwise.
- D) The turn from o→a to o→b is clockwise.

<details>
<summary>Answer and explanation</summary>

**C) The turn from o→a to o→b is counter-clockwise.**

`cross` is twice the signed area of the triangle $o, a, b$, and the sign
convention is that counter-clockwise order gives a positive value. The lesson's
own numbers confirm it: `cross((0,0), (3,0), (4,3)) = 9 > 0`, and the hull is
traversed $(0,0) \to (3,0) \to (4,3)$, which is a left turn — the same left turn
the code asserts with `all turns left: True`.

A) and B) are wrong because collinearity is the `= 0` case, not the `> 0` case.
A positive value rules out collinearity outright, and it says nothing about
which of $a$ or $b$ is in the middle: both readings collapse to $cross = 0$ when
the middle-point condition holds.

D) reverses the convention. The worked example's clockwise turn is
`cross((0,0), (0,3), (1,1)) = (0-0)(1-0) - (3-0)(1-0) = 0 - 3 = -3`, and it is
exactly that negative value that forces the chain to pop. Getting this sign
backwards is not a cosmetic slip — it would make the monotone chain keep every
right turn and produce a hull that is inside the true one.

</details>

**Q2.** The monotone chain pops the last point of the lower chain whenever
`cross(lower[-2], lower[-1], p) <= 0`. Why is that pop *forced* rather than a
heuristic that happens to work?

- A) Because that point is necessarily closer to the origin than the other two.
- B) Because the point is enclosed by its two neighbours, so it cannot be a hull
  vertex, and keeping it would destroy the invariant that the chain so far is
  convex.
- C) Because the upper chain will contain the same point, so keeping it would
  create a duplicate.
- D) Because a non-left turn makes the accumulated shoelace sum negative.

<details>
<summary>Answer and explanation</summary>

**B) Because the point is enclosed by its two neighbours, so it cannot be a hull
vertex, and keeping it would destroy the invariant that the chain so far is
convex.**

The chain under construction is always convex. When a new point arrives and the
last turn is a right turn or collinear, the middle point lies inside the
triangle formed with its two neighbours, so no convex set containing those three
can have the middle one on its boundary. Since every hull vertex must be on the
boundary, the middle point is disqualified — the pop is forced by the definition
of a hull vertex, not chosen for convenience. The worked example shows it twice
in a row: pushing $(3,0)$ pops $(2,5)$ on `cross = -9`, then rechecks and pops
$(1,1)$ on `cross = -3`.

A) is wrong because distance from the origin is irrelevant to hull membership, and
the hull need not even touch the origin. The example's hull *does* contain
$(0,0)$ as a vertex, but that is a coincidence of the input, not the rule.

C) is wrong because duplicates are not what the pop prevents — the code handles
duplicates separately, at the splice (`lower[:-1] + upper[:-1]`, "the first and
last points appear in both chains, so drop one copy"). And the popped points
$(1,1)$ and $(2,5)$ are exactly the points that appear on *neither* chain, which
is the opposite of what C claims.

D) is wrong because the shoelace sum is computed on the finished hull, and its
sign reflects the winding of the final counter-clockwise chain, not any local
turn during construction. A right turn during the scan does not make the partial
sum negative in any way the algorithm looks at.

</details>

**Q3.** The pop test is changed from `cross(...) <= 0` to `cross(...) < 0`, and
nothing else is touched. What changes in the returned hull?

- A) Extreme points are lost, so the hull no longer contains all the input points.
- B) The hull comes out clockwise instead of counter-clockwise.
- C) Collinear points lying on hull edges now survive, so the hull gains extra
  vertices that are not extreme points.
- D) Nothing measurable changes — both tests compute the same convex region.

<details>
<summary>Answer and explanation</summary>

**C) Collinear points lying on hull edges now survive, so the hull gains extra
vertices that are not extreme points.**

With `< 0`, a `cross` of exactly 0 no longer triggers a pop, so a run of
collinear points along an edge all stay on the chain. On the lesson's input that
means $(1,0)$ and $(2,0)$ — the two points on the bottom edge — are kept, and
the code's `points excluded from the hull` list drops from five entries to
three. The region enclosed is genuinely the same convex set, which is exactly why
D is tempting: the area would still come out 14.5 from the shoelace formula.

A) is wrong and would be alarming if true, but it is the opposite of what
happens. `< 0` is *more* permissive about which points to keep, not less: the
middle point of a strict right turn is still popped. The lesson's
`all input points inside or on hull: True` check passes either way.

B) is wrong because the winding is set by the direction of the scan — lower chain
left to right, upper chain right to left — not by the comparison operator. The
code indexes `hull[(i + 1) % len(hull)]`, which walks the chain forward either
way.

D) is wrong for two reasons. The *region* is the same, but the *vertex list* is
not, and downstream code cares: the extra points break hull-to-hull consistency
between runs, and the `all turns left` assertion in the lesson would now fail,
because a collinear triple gives `cross = 0`, which is not `> 0`. This is why the
lesson's Common Mistakes section says to decide which behaviour you want and
write it down.

</details>

**Q4.** In the worked example, the chain pops $(1,1)$ after evaluating
`cross((0,0), (1,1), (3,0))`. What is that value?

- A) 3
- B) −3
- C) 9
- D) 0

<details>
<summary>Answer and explanation</summary>

**B) −3.**

Substituting directly: $(a_1-o_1)(b_2-o_2) - (a_2-o_2)(b_1-o_1)$ with
$o = (0,0)$, $a = (1,1)$, $b = (3,0)$ gives $(1-0)(0-0) - (1-0)(3-0) = 0 - 3 = -3$.
The lesson prints the same computation inline: "Recheck:
cross((0,0), (1,1), (3,0)) = (1)(0) − (1)(3) = −3 < 0. Right turn again, so pop
(1,1)." It is negative, which is exactly what authorises the second pop.

A) is wrong because it is the magnitude with the sign dropped — the single most
common arithmetic slip in this formula. The magnitude alone tells you the triangle
has area 1.5, but the algorithm needs the direction, and 3 would send you down
the left-turn branch instead.

C) is wrong because 9 is a real number from this lesson but a different
evaluation: `cross((0,0), (3,0), (4,3)) = 9`, the first turn of the finished hull.
Reading 9 here would mean confusing the triple used in the recheck with the
triple used at the end.

D) is wrong because a value of 0 would mean $(0,0)$, $(1,1)$ and $(3,0)$ are
collinear, and they plainly are not — the line from the origin through $(1,1)$ is
$y = x$, and $(3,0)$ is nowhere near it. A 0 would still pop, but by the
collinear branch, not by the right-turn branch the example is illustrating.

</details>

**Q5.** Why must the closest-pair strip be sorted by $y$ before the inner scan
runs?

- A) So that the filter `abs(x - mid_x) <= d` keeps the correct set of points.
- B) So the inner loop can `break` as soon as the $y$-gap reaches $d$; without the
  sort the `break` fires at an arbitrary point and the scan silently misses closer
  pairs.
- C) Because Euclidean distance is only well defined for $y$-sorted input.
- D) Because the divide step actually splits on $y$ rather than on $x$.

<details>
<summary>Answer and explanation</summary>

**B) So the inner loop can `break` as soon as the $y$-gap reaches $d$; without the
sort the `break` fires at an arbitrary point and the scan silently misses closer
pairs.**

The code's inner condition is `if strip[j][1] - strip[i][1] >= d: break`, with
the comment "sorted by y, so nothing below is closer". That argument is only
available because the y-coordinates are non-decreasing down the strip: once the
gap reaches $d$, every later point is at least $d$ away in $y$ alone, so no
remaining comparison can beat $d$. Sorting is what converts an O(n) scan into an
O(1) one.

A) is wrong because the filter is a pure x test and the order of the list cannot
change which points it selects — `strip = sorted([...], key=lambda p: p[1])`
filters first, then sorts. A permutation of the same set is still the same set.

C) is wrong because the distance function is order-free:
`sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)` reads two coordinates and is done. This
is also why Common Mistake 1 lists "forgetting to sort by x in the closest-pair
algorithm" as a distinct failure: the input precondition and the strip sort are
two different sorts, and the lesson's code does both.

D) is wrong because the split is vertical. `mid = n // 2` and
`mid_x = points[mid][0]` split on $x$, which is why the input must be x-sorted;
the strip is then *chosen* by an x test and *sorted* by $y$ so that the scan can
stop early. Confusing the two sorts is exactly the bug.

</details>

**Q6.** On what packing argument does the "next 7 points" window in the strip scan
rest?

- A) 7 is the empirically best constant found by tuning.
- B) A square of side $d$ holds at most 4 points at mutual distance $\ge d$, so the
  $d$-neighbourhood of a strip point spans at most 8 half-squares and only a
  constant number of candidates can lie within distance $d$.
- C) A uniform grid query with a 3×3 neighbourhood returns 8 neighbours.
- D) A double-precision float carries about 7 significant digits.

<details>
<summary>Answer and explanation</summary>

**B) A square of side $d$ holds at most 4 points at mutual distance $\ge d$, so the
$d$-neighbourhood of a strip point spans at most 8 half-squares and only a
constant number of candidates can lie within distance $d$.**

The lesson states the packing argument in the Formal Version: subdivide a square
of side $d$ into four squares of side $d/2$, each of which holds at most one
point, so at most four in total; the neighbourhood therefore spans at most eight
of those half-squares, and "that is where the constant '7 neighbours' comes
from". The consequence is that the inner scan needs a fixed, input-independent
number of steps, which is what keeps the whole algorithm $O(n \log n)$ rather than
$O(n^2)$ after the recursion has already delivered its halves.

A) is wrong because the constant is not a tuning parameter; it is a consequence
of the packing bound. If it were empirical, enlarging it would never change the
answer and shrinking it below the bound would give a wrong distance — and
Common Mistake 1 describes exactly that failure mode, where the result is "wrong,
with no error".

C) is wrong because it confuses two different data structures. The 9-cell
neighbourhood is the *broad phase*'s spatial hash query, where cells are a fixed
size unrelated to $d$. The 7-neighbour bound lives in the closest-pair strip,
where the relevant scale is the distance $d$ just discovered, not a grid
resolution. The numbers coincide; the reasoning does not.

D) is wrong because floating-point precision plays no part in the bound. If the
argument were about representation, doubling the precision would change the
complexity class, which it plainly does not.

</details>

**Q7.** In ray casting, a point's crossing number comes out even. What does that
mean?

- A) The point lies exactly on the polygon boundary.
- B) The point is outside the polygon.
- C) The point is inside the polygon.
- D) The polygon is non-convex.

<details>
<summary>Answer and explanation</summary>

**B) The point is outside the polygon.**

The parity rule is "inside iff the crossing number is odd", which follows from the
Jordan curve theorem: a ray from an interior point must leave the region, so it
crosses the boundary an odd number of times; a ray from an exterior point crosses
an even number of times. The worked example walks through it twice on the
L-shaped polygon: $(4,4)$ gets zero counted crossings, even, so **outside**; and
$(1,4)$ gets one, odd, so **inside**.

A) is wrong because a boundary point is a separate case entirely, decided by the
straddle and strict-comparison rules rather than by parity. The lesson's test
list makes this concrete: $((2,2), False, "on the reflex vertex")$. A ray from a
point exactly on an edge is degenerate, and the code's half-open test settles it
by convention rather than by counting — the lesson says "boundary behaviour is
genuinely ambiguous — decide and document it rather than hoping".

C) is wrong because that is the odd case, and getting it backwards is the
characteristic sign error. It is easy to make here because the test list contains
four `True` and four `False` rows, so a reader who glances at the shape rather
than the parity can rationalise either answer.

D) is wrong because convexity of the polygon is irrelevant to the parity rule.
Ray casting is valid for the non-convex L-shape precisely because the code
brackets each edge with the straddle test; Common Mistake 5 names "assuming the
polygon is convex" as an error and points at the wrong shortcut, not at ray
casting itself.

</details>

**Q8.** The code tests `(y1 > y) != (y2 > y)` and then compares `x_cross > x`,
rather than using `>=` in both places. What is the strict form buying?

- A) Speed — the strict comparison is a micro-optimisation on the inner loop.
- B) Together they settle the case where the ray passes exactly through a vertex
  or along a horizontal edge: the half-open test counts such a crossing exactly
  once, and the strict comparison keeps boundary points out. With `>=`, the
  parity can flip and boundary points get misclassified.
- C) Protection against division by zero on horizontal edges.
- D) A way of counting crossings in both directions along the ray.

<details>
<summary>Answer and explanation</summary>

**B) Together they settle the case where the ray passes exactly through a vertex
or along a horizontal edge: the half-open test counts such a crossing exactly
once, and the strict comparison keeps boundary points out. With `>=`, the parity
can flip and boundary points get misclassified.**

The lesson's Common Mistake 3 says this directly: using `x_cross >= x`
double-counts the case where the ray passes exactly through a vertex, and points
on the boundary get misclassified; "the strict comparison plus the
`(y1 > y) != (y2 > y)` half-open test is the standard combination that handles
vertices correctly". The code comment agrees: "Only count crossings strictly to
the right of the point. The strict comparison also settles vertices that lie
exactly at py."

A) is wrong because the strictness changes the answer, not the runtime. There is
no measurable speed difference between `>` and `>=` on a float comparison; both
compile to the same instruction. If this were purely about speed there would be
nothing to explain in a Common Mistakes section.

C) is wrong because division by zero is prevented by the *straddle* test, not by
the comparison. A horizontal edge has $y_1 = y_2$, so
`$y_1 > y$ != $y_2 > y$` is False and `x_cross` is never evaluated — the code
reaches the division only when $y_2 \ne y_1$. The vectorised numpy block says the
same thing, relying on `nan` comparisons being False rather than on an epsilon.
The `>` after the division is about parity, not about zeros.

D) is wrong because the ray is cast in one direction only, towards $+x$, and
only crossings to the right are counted. There is no second direction to count,
and adding one would make every crossing count twice and flip every parity.

</details>

**Q9.** A circle sits at the origin with radius 5, and the line runs from
$(−10, 6)$ to $(10, 6)$. How many intersections are there, and what in the
quadratic says so?

- A) 2, because the discriminant is positive.
- B) 1, because the discriminant is exactly zero.
- C) 0, because the line's height $y = 6$ already exceeds the radius 5, and the
  discriminant comes out negative.
- D) 0, because the leading coefficient $a = dx^2 + dy^2 = 400$ is too large.

<details>
<summary>Answer and explanation</summary>

**C) 0, because the line's height $y = 6$ already exceeds the radius 5, and the
discriminant comes out negative.**

Worked through: $\mathbf{d} = (20, 0)$, $\mathbf{f} = (−10, 6)$, so
$a = \mathbf{d}\cdot\mathbf{d} = 400$, $b = 2\,\mathbf{f}\cdot\mathbf{d} = −400$,
and $c = \mathbf{f}\cdot\mathbf{f} − 25 = 136 − 25 = 111$. Then
$\Delta = b^2 − 4ac = 160000 − 177600 = −17600 < 0$, and the code returns `[]`
because of `if discriminant < 0.0: return []`. Geometrically, $y = 6 > 5$ means the
whole line is outside the circle, and the tangent case in the lesson's own test
list is the line $y = 5$, which returns exactly one hit at $(0, 5)$.

A) is wrong because a positive discriminant requires $\Delta > 0$. The same
coefficients with $y = 3$ instead of $y = 6$ give $c = 84$ and
$\Delta = 160000 − 134400 = 25600 > 0$, which is the two-hit case the worked
example computes by hand as $(−4, 3)$ and $(4, 3)$.

B) is wrong because $\Delta = 0$ is the tangent case, and it is exactly the line
$y = 5$ in the code's case list: `((-10, 5), (10, 5), 1, "tangent: touches once")`
prints `1 hit(s) [(0.0, 5.0)]`. Reaching $\Delta = 0$ requires $y = 5$ exactly, not
$y = 6$.

D) is wrong because $a$ scales the parameter $t$ and says nothing about whether
the line meets the circle; a positive $a$ is the only thing the quadratic needs
for the formula $t = (−b \pm \sqrt\Delta)/(2a)$ to be defined. The lesson's
`a == 0.0` guard exists only to catch $p = q$, a degenerate line. The same
$a = 400$ appears for the $y = 3$ and $y = 5$ lines, which do intersect.

</details>

**Q10.** The lesson prints `segment (-10,0) to (0,0) : [(-5.0, 0.0)]`, even though
running `line_circle_intersect` on the same two endpoints returns both
$(−5, 0)$ and $(5, 0)$. Why the difference?

- A) The segment version uses a smaller radius than the line version.
- B) The second root is $t = 1.5$, which lies beyond the endpoint $q = (0,0)$, so
  only the root $t = 0.5$ survives the test $0 \le t \le 1$.
- C) The endpoint $(0,0)$ is the centre of the circle, so it is rejected.
- D) There is no difference; the printout is a bug in the lesson.

<details>
<summary>Answer and explanation</summary>

**B) The second root is $t = 1.5$, which lies beyond the endpoint $q = (0,0)$, so
only the root $t = 0.5$ survives the test $0 \le t \le 1$.**

Compute it: $\mathbf{d} = (10, 0)$, $\mathbf{f} = (−10, 0)$, $a = 100$,
$b = −200$, $c = 75$, so $\Delta = 40000 − 30000 = 10000$ and
$t = (200 \pm 100)/200$, which is $0.5$ or $1.5$. The line parameterises
$h(t) = p + t\mathbf{d} = (−10 + 10t,\ 0)$, so $t = 0.5$ gives $(−5, 0)$ and
$t = 1.5$ gives $(5, 0)$. The line contains both; the segment from $(−10,0)$ to
$(0,0)$ contains only the first. The code's projection
$t = (h − p)\cdot(q − p)/\lVert q − p\rVert^2$ recovers exactly that $t$ for each
hit and keeps only those in $[0, 1]$.

A) is wrong because both functions are called with the same arguments — `5.0` in
both cases — and the line function is called *inside* the segment function, so
it cannot be using a different radius. A radius discrepancy would also change the
positions of the hits, not just their count.

C) is wrong because $(0,0)$ is an endpoint, not a hit, and the endpoint is never
filtered out. The projection for $h = (5, 0)$ gives $t = 1.5$, which is rejected
for being *past* the endpoint, not for being the endpoint. And $(0,0)$ being the
centre is irrelevant: a segment from the centre outwards still has a well-defined
near intersection, which is the $(−5,0)$ the lesson keeps.

D) is wrong because the printed output is consistent with the same code, run with
the same circle. The lesson pairs the two prints deliberately, and the comment
above them reads "a segment and a line give different answers against the same
circle" — the contrast is the teaching point, not an oversight.

</details>

**Q11.** The cell-size sweep reports 1600 pair checks at cell size 10.0 for the
40-circle scene, against 780 for plain brute force. What has gone wrong?

- A) The grid is buggy at coarse cell sizes.
- B) At cell size 10 the whole scene fits in 4 cells, so every query's 3×3
  neighbourhood returns essentially everything — the cheap filter has become more
  expensive than the exact test it was meant to avoid.
- C) Coarse cells make the narrow-phase `collides` test less accurate.
- D) Coarse cells overflow the memory of the cell dictionary.

<details>
<summary>Answer and explanation</summary>

**B) At cell size 10 the whole scene fits in 4 cells, so every query's 3×3
neighbourhood returns essentially everything — the cheap filter has become more
expensive than the exact test it was meant to avoid.**

The sweep is printed directly: `cell 10.0 -> 4 cells, 1600 checks`, against
`cell 2.0 -> 32 cells, 168 checks` and `40 circles` all-pairs at 780. With only 4
occupied cells, the 9 cells a query looks at are a superset of the entire scene,
so `grid.query(circle)` returns all 40 circles and the "candidates" are 40 × 40
= 1600 — more than the 780 unordered pairs brute force would even consider. The
lesson states the rule: "A grid only pays off when cells hold a handful of
objects", and at 10.0 they hold 10 each.

A) is wrong because the same code is correct at cell size 2.0, finding the same 11
colliding pairs as brute force (`same pairs? True`). A bug would not be
size-dependent in exactly the way that tracks occupancy, and the brute-force
count 780 is confirmed by $40 \times 39 / 2$, so the 1600 is real work, not a
counting artefact.

C) is wrong because the narrow phase is untouched by the grid — `collides` takes
two circles and a radius and compares `sqrt(dx**2 + dy**2)` against `ar + br`. A
coarse grid changes only *which pairs reach it*, never what it computes, which is
why `broadphase found 11` equals `brute force found 11` at every cell size that is
still correct.

D) is wrong because 4 cells is the *smallest* occupancy in the sweep, not the
largest — finer cells use more memory (`cell 1.0 -> 37 cells`, and in the
challenge, 4464 cells at size 0.5). Memory pressure is the argument against small
cells, never against large ones.

</details>

**Q12.** In the challenge, a broad phase that registers each circle only in the
cell containing its centre finds 16 of the 42 colliding pairs at cell size 0.5.
What is it missing?

- A) Duplicate pairs, because the canonical `seen` key drops them.
- B) Circles whose diameter (up to 1.8) exceeds the cell size, so they span a 2×2
  block of 0.5-cells but are filed under one — two overlapping circles in
  different cells are therefore never compared.
- C) Circles whose coordinates are negative, because `int()` truncates towards
  zero.
- D) Circles within floating-point distance of a cell boundary.

<details>
<summary>Answer and explanation</summary>

**B) Circles whose diameter (up to 1.8) exceeds the cell size, so they span a 2×2
block of 0.5-cells but are filed under one — two overlapping circles in different
cells are therefore never compared.**

The lesson's own diagnosis: "a circle of radius 0.9 has diameter 1.8, so it covers
a 2×2 block of 0.5-cells, but it is filed under one cell. Two overlapping circles
in different cells never get compared." The printed table shows exactly where the
error disappears — the `naive` column reads 16 at cell 0.5, 38 at 1.0, and 42 from
1.5 upward, because only at 1.5 does the cell finally exceed the largest diameter.
The fix is not a bigger cell: `multi-cell` is correct at *every* size, including
0.5, because it registers each object in every cell its bounding box touches.

A) is wrong because deduplication can only remove a pair that was already found
once; it cannot suppress a pair that was never examined. And the
`multi-cell` version uses the identical canonical key
`min(id(c), id(other)), max(id(c), id(other))` and still finds all 42.

C) is wrong because `cell_key` uses `int(cx // cell_size)`, which floors, and the
lesson verifies it: `point (-0.5, -0.5) lands in cell (-1, -1)` and "negative
cells differ from positive ones: True". Truncation towards zero would put −0.5 in
cell 0, colliding with positives — a real bug, but a different one, and the scene
here has no negative coordinates at all.

D) is wrong because the failure is structural, not numerical. A circle near a cell
boundary still gets registered in its own cell and is still found by the 3×3
query of its neighbours; what is lost is any circle whose *extent*, not whose
centre, reaches across the boundary. No epsilon fixes a missing registration.

</details>

**Q13.** Why is the convex hull called a *conservative* collision proxy rather
than an exact one?

- A) Because the hull's centroid can fall outside the shape it stands for.
- B) Because hull vertices are a subset of the input points, so a hull can never
  represent a curved mesh edge.
- C) Because $\mathrm{conv}(S) = \mathrm{conv}(H)$ makes interior points
  irrelevant and the hull contains the whole shape — so it never *misses* a
  collision — but for the L-shape the hull area is 28.0 against the shape's 20.0,
  so it also reports hits that are not real.
- D) Because the shoelace formula only bounds the area from above.

<details>
<summary>Answer and explanation</summary>

**C) Because $\mathrm{conv}(S) = \mathrm{conv}(H)$ makes interior points
irrelevant and the hull contains the whole shape — so it never *misses* a
collision — but for the L-shape the hull area is 28.0 against the shape's 20.0,
so it also reports hits that are not real.**

Exercise 2 supplies both halves of that claim with numbers. The hull of the
L-shape is $(0,0), (6,0), (6,2), (2,6), (0,6)$: the reflex vertex $(2,2)$ has
been swallowed and the edge now runs as a straight diagonal from $(6,2)$ to
$(2,6)$ across the notch. The printed areas are `L-shape area : 20.0` and
`hull area (fills in): 28.0`, and the notch point $(3,3)$ is reported as outside
the real L but inside the hull. The lesson's judgement is explicit: "The hull is
cheap, and it never *misses* a collision, so you get false positives instead of
objects tunnelling through walls."

A) is wrong because the centroid of a convex polygon is always inside it — the
exercise prints `centroid: (1.8, 2.2)` and `centroid inside hull? True`, and the
proof is that the centroid is a convex combination of the vertices and a convex
set contains all convex combinations of its points. So the hull cannot be blamed
for a centroid that escapes it.

B) is wrong because being a subset of the input points is exactly the property
that makes the hull *cheap*, not that makes it inaccurate. The inaccuracy comes
from the hull adding area the shape never had, not from the vertices being input
points. A mesh edge being curved is irrelevant: hulls are used precisely because
they replace such meshes with a handful of straight edges.

D) is wrong because the shoelace formula is exact. For the lesson's hull the
signed double area is exactly 29, so the area is exactly 14.5 — and the code
agrees with the hand computation to the digit. Nothing about it is a bound.

</details>

**Q14.** What does the identity $\mathrm{conv}(S) = \mathrm{conv}(H)$ license a hull
algorithm to do?

- A) Discard interior points and keep only the hull vertices, because removing them
  cannot change the convex region returned.
- B) Return the hull in either winding order, since convexity does not depend on
  direction.
- C) Skip the initial sort, since the hull does not depend on input order.
- D) Use `<` instead of `<=` in the pop test without changing what is returned.

<details>
<summary>Answer and explanation</summary>

**A) Discard interior points and keep only the hull vertices, because removing them
cannot change the convex region returned.**

This is the Formal Version theorem stated as "convexity is preserved when
interior points are deleted, which is why hull algorithms can discard
aggressively". Exercise 2 demonstrates it empirically: adding the noise points
$(2,2), (2,3), (1,1), (3,1)$ to a convex pentagon leaves a byte-identical hull and
an unchanged centroid (`hull unchanged? True`, `centroid unchanged? True`), and
the code excludes five of the ten input points from the hull without the result
changing. The identity is what makes an aggressive pop policy *sound* rather than
merely fast.

B) is wrong because winding is a separate property from convexity. The theorem
says nothing about order, yet the code's own verification walks
`hull[(i + 1) % len(hull)]` and asserts `all(t > 0 for t in turns)`, which only
holds for the counter-clockwise hull. A clockwise hull is the same convex region
and a different vertex list, and it fails that check.

C) is wrong because the hull is order-independent as a *set*, but the algorithm is
not. The monotone chain's correctness argument is local — "pop the last point
while the last turn is not counter-clockwise" — and it presupposes a left-to-right
scan. Fed unordered input, the chain pops points that are genuine extreme points
relative to the wrong chain. The initial `sorted(set(points))` is load-bearing.

D) is wrong because option C of the third question is the counterexample: with
`<`, the collinear points $(1,0)$ and $(2,0)$ survive on the hull's bottom edge.
The *region* is unchanged but the *vertex list* is not, which is what most
callers consume.

</details>

---

## Subjective Questions

### Short Answer

**Q1. Define the *crossing number* of a point with respect to a polygon, and
state the parity rule that follows from it.**

<details>
<summary>Answer</summary>

The crossing number of a point $p$ with respect to a polygon $P$ is the number of
times a ray starting at $p$ crosses $P$'s boundary. By the Jordan curve theorem,
$p$ is inside $P$ if and only if the crossing number is odd, and outside if and
only if it is even.

Two conditions come with the rule. The polygon must be *simple* — not
self-intersecting — because a self-intersecting curve does not separate the plane
into a single inside and outside. And the count must be taken with a half-open
straddle test, $(y_1 > y) \neq (y_2 > y)$, plus a strict $x_{\text{cross}} > x$,
so that a ray passing exactly through a vertex is counted once rather than twice.

</details>

**Q2. Write the shoelace formula for a polygon with vertices
$(x_0, y_0), \dots, (x_{n-1}, y_{n-1})$, and say what the factor of $\tfrac{1}{2}$
and the mod-$n$ indexing each accomplish.**

<details>
<summary>Answer</summary>

$$
A = \tfrac{1}{2}\sum_{i=0}^{n-1}\left(x_i y_{i+1} - x_{i+1} y_i\right)
$$

Indices are taken mod $n$, so $y_n = y_0$: that is what closes the polygon,
turning the sum into a cycle over the edges $i \to (i+1) \bmod n$. Without it the
last edge back to vertex 0 is simply absent and the shape is not the polygon.

The $\tfrac{1}{2}$ is because the sum is the *signed doubled* area — every
triangle in the triangulation is counted on both of its sides. In the lesson's
worked example the five cross terms sum to 29 and the area is $29/2 = 14.5$, which
is exactly what the code prints as `shoelace area = 14.5`. The formula requires a
simple polygon; on a self-intersecting one it computes the winding-weighted
algebraic area instead. The sign is positive for counter-clockwise winding.

</details>

**Q3. State the monotone-chain pop rule, and explain why the pop is forced by the
definition of a hull vertex rather than chosen for convenience.**

<details>
<summary>Answer</summary>

Sort $S$ by $x$ (ties by $y$); scanning left to right, push each point and then
pop the last point of the chain while the last turn is not counter-clockwise, i.e.
while $\mathrm{cross}(\text{chain}[-2], \text{chain}[-1], p) \le 0$.

The pop is forced because the middle point of a non-left triple lies inside the
triangle formed with its two neighbours. A hull vertex, by definition, is a point
of $S$ that is not inside any segment between two other points of $S$ — and the
whole chain must stay convex, since a convex set containing the three corners must
contain their triangle. So the middle point cannot be a hull vertex of any
convex set containing the input. Keeping it would either break the convexity
invariant the algorithm relies on or put a non-extreme point on the reported hull.

</details>

**Q4. Write the quadratic that the line–circle test solves, and state what each of
the three discriminant cases means geometrically.**

<details>
<summary>Answer</summary>

With $\mathbf{d} = q - p$ and $\mathbf{f} = p - \mathrm{centre}$, substitute
$h(t) = p + t\mathbf{d}$ into $(x - c_x)^2 + (y - c_y)^2 = r^2$ to get

$$
a = \mathbf{d}\cdot\mathbf{d}, \qquad b = 2\,\mathbf{f}\cdot\mathbf{d}, \qquad c = \mathbf{f}\cdot\mathbf{f} - r^2,
$$
$$a t^2 + bt + c = 0, \qquad \Delta = b^2 - 4ac, \qquad t = \tfrac{-b \pm \sqrt{\Delta}}{2a}.$$

$\Delta < 0$ means the line passes beside the circle — 0 hits. $\Delta = 0$ means
it grazes it — 1 hit, a tangent, computed as $t = -b/2a$. $\Delta > 0$ means it
cuts through — 2 hits, the two roots.

The restriction is $a > 0$, i.e. $p \ne q$: with $p = q$ there is no line and
the formula divides by zero.

</details>

**Q5. What precondition does the closest-pair divide-and-conquer place on its
input, and what exactly goes wrong if that precondition is violated?**

<details>
<summary>Answer</summary>

The input must be sorted by $x$ on entry, and the strip built from it must
separately be sorted by $y$.

If the input is not x-sorted, `points[mid][0]` is not the dividing line, so
`mid_x` is not the $x$-coordinate of the split. The halves then mix points from
both sides of the true split, and the filter
`|x - mid_x| <= d` no longer describes the strip "within $d$ of the dividing
line" — it admits some cross-half candidates and excludes others. The recursive
answers $d_L$ and $d_R$ are still correct for their own subsets, so the algorithm
returns a distance that is too large with no error, no exception, and no failed
assertion.

If the strip is not y-sorted, the `break` on
`strip[j][1] - strip[i][1] >= d` fires at an arbitrary position and discards
candidates that were still worth comparing. Both failures are silent, which is
why the lesson's code sorts in two places and checks itself against brute force
on eleven separate seeds.

</details>

**Q6. Define *broad phase* and *narrow phase*, and name one grid-based and one
tree-based spatial partition.**

<details>
<summary>Answer</summary>

The **broad phase** is the cheap, conservative filter: it decides which pairs
*could* interact, using an approximation and never rejecting a pair that really
does interact. The **narrow phase** is the exact test — centre distance against
the sum of radii, SAT, GJK — run only on the survivors.

A **uniform grid** is the grid-based partition: space is cut into equal cells and
each object is registered in the cell(s) its bounding box touches; a query reads
its own cell plus the 8 around it. A **bounding volume hierarchy** (BVH) is the
tree-based partition: nested axis-aligned boxes, tested top-down with an
early-out, which is what Box2D's dynamic tree and `btDbvtBroadphase` are. kd-trees
(`scipy.spatial.cKDTree`) are a third structure of the same family.

The dividing line between the phases is what makes the split worth doing: an
all-pairs narrow phase is $\Theta(n^2)$, and a partition that keeps the candidate
set at $\Theta(n)$ pairs makes the total $\Theta(n)$.

</details>

### Long Answer

**Q1. Why does the divide-and-conquer closest-pair algorithm get away with only a
constant number of comparisons per strip point — and what would actually break if
you removed the y-sort, the `break`, or the 7-cap?**

<details>
<summary>Model answer</summary>

The recursion hands back two correct answers, $d_L$ from the left half and $d_R$
from the right, and takes $d = \min(d_L, d_R)$. Any cross-half pair that could
beat $d$ must satisfy two constraints at once: its two points are within distance
$d$ of each other, and their $x$-coordinates are within $d$ of the split
$x_{\text{mid}}$. That is why the strip filter is $|\,x - x_{\text{mid}}\,| \le d$:
it is not an approximation, it is a *necessary* condition, derived from
$\lvert a_x - b_x\rvert \le \lVert a - b\rVert < d$.

The strip is then sorted by $y$ so that a third fact becomes usable. If
$\mathrm{strip}[j]_y - \mathrm{strip}[i]_y \ge d$, then for every $k > j$ the
same inequality holds, so $\mathrm{strip}[k]$ is already at least $d$ away from
$\mathrm{strip}[i]$ in the vertical direction alone and cannot beat $d$ whatever
its $x$. That is the whole justification for the `break`, and it is a statement
about the *suffix* of a sorted list — which is why the sort is not optional. Remove
the y-sort and the break throws away real candidates: the answer comes back too
large, silently.

The 7-cap comes from packing. Every point in the strip other than the pair under
test is at least $d$ from every other, so a square of side $d$ holds at most 4 of
them (subdivide it into four squares of side $d/2$, each of which can hold at most
one). The $d$-neighbourhood of a strip point therefore spans at most 8 such
half-squares, and only a constant number of strip positions can be within distance
$d$ of it. So the inner loop can look ahead a fixed 7 and stop.

Now the failure modes, which are different in character. Remove the y-sort and
you get the break described above — a wrong answer, no error. Remove the `break`
and the algorithm is still correct, but the inner scan runs to the end of the
strip for every strip point, which makes the combine step $O(n^2)$ and the whole
algorithm $O(n^2)$ — a silently quadratic version of an intended $O(n \log n)$.
Remove the 7-cap, or shrink it, and you get the first failure mode again: a pair
that could beat $d$ sits beyond the window and is never compared.

The asymmetry is the useful lesson. Two of the three pieces are *correctness*
premises and one is a *performance* premise, and the code makes no distinction
between them. Common Mistake 1 is about exactly this: the "distance too large —
wrong, with no error" outcome. That is why the lesson's implementation verifies
itself against brute force on eleven seeds rather than on one.

</details>

**Q2. Why is a convex hull a safe but not an exact collision proxy, and what would
actually go wrong in a physics engine if you treated it as an exact one?**

<details>
<summary>Model answer</summary>

"Safe" and "exact" fail in opposite directions, and only one of them is a bug.

The hull contains the shape. Since $\mathrm{conv}(S)$ is a convex set containing
$S$, and a segment between any two points of $S$ lies in it, every point of the
shape — and every segment between two of its points — lies inside the hull. So a
hull test never reports "no overlap" when there is one. That is the direction you
cannot afford to get wrong: a missed collision in a physics engine is an object
tunnelling through a wall, and tunnelling is silent and often unrecoverable.

The hull is also *not much bigger* than the shape in the sense that matters,
because $\mathrm{conv}(S) = \mathrm{conv}(H)$: interior points cannot change it,
so a hull computed from a million sampled surface points is exactly the hull of
the few hundred genuinely extreme ones. That is what makes it a cheap proxy —
polygon intersection instead of triangle-versus-mesh intersection.

But it is strictly larger. The lesson's L-shape is the counterexample: the hull
$(0,0), (6,0), (6,2), (2,6), (0,6)$ has area 28.0 against the shape's 20.0,
because the reflex vertex $(2,2)$ is swallowed and a straight edge runs diagonally
from $(6,2)$ to $(2,6)$ across the notch. The point $(3,3)$ is outside the real
L-shape and inside its hull. If you treated the hull as exact, an object sitting
in that notch would be reported as colliding with the wall when it is standing in
open space.

Now put that in an engine and the consequences are specific rather than
theoretical. Contacts would be created between objects that are not touching, so
the solver would push them apart — an object would be shoved out of a notch it
legally occupies, or jitter against a wall it is nowhere near. Worse, the error
is *systematic and directional*: it only ever adds area, so the artefact is
always a spurious push outward from the wall, which reads to a player as the
level being broken rather than as a collision bug. And because the artefact is
consistent, it does not average out over frames the way random numerical noise
would; it becomes a permanent, reproducible force.

This is why the lesson's judgement is that the hull is a *conservative* proxy, and
why real engines keep it as a first-stage filter rather than a final answer —
exactly the broad-phase/narrow-phase split: the hull rejects cheaply and safely,
and the exact mesh test only ever runs on the handful of pairs that survive.

</details>

**Q3. Why does splitting collision detection into broad and narrow phase turn
$\Theta(n^2)$ into $\Theta(n)$, and what does that depend on?**

<details>
<summary>Model answer</summary>

Start with the count. An exact narrow-phase test — centre distance against the
sum of radii, or a separating-axis test — is constant work per pair, but the
number of pairs in a scene of $n$ objects is $\binom{n}{2} = n(n-1)/2$, which is
$\Theta(n^2)$. For the lesson's 40 circles that is 780 pairs. At $n = 10^4$ it is
about 50 million. Nothing about the exact test is slow; the problem is that you
are asking it about pairs that were never close.

The broad phase changes the *count*, not the cost. It is a cheap, conservative
filter: it uses an approximation — which cells does this object's bounding box
touch — and its only obligation is to never reject a pair that truly interacts.
Everything that survives becomes a candidate, and the candidate set is what the
exact test has to chew through.

The $\Theta(n)$ result requires the candidate set to stay $O(n)$ in total, and
that in turn requires each object to have a *constant* number of neighbours. The
lesson's grid achieves it by looking at one cell plus its 8 neighbours: if two
circles are within range of each other, their centres must be in the same or
adjacent cells, which is why a 3×3 query cannot miss a collision. The measured
numbers bear this out — 780 all-pairs checks become 168 candidate checks at cell
size 2.0, a reduction of 4.64×, with the same 11 colliding pairs found. In the
challenge the gap widens from 1,237× at $N = 100$ to 13,317× at $N = 800$, and
the doubling ratios say why: all-pairs work multiplies by about 4.0 each time,
while broad-phase work multiplies by 1.75, 2.43 and 1.41 — roughly 2, which is
linear.

Two dependencies are worth stating plainly. First, cell size must be chosen so
cells hold a small constant number of objects. The sweep in the lesson shows both
failure directions from one mechanism: at 4.0 there are only 22 occupied cells so
each query returns a slab of the world (520 checks), and at 10.0 there are 4 and
every query returns everything (1600 checks — *worse* than brute force's 780).
The rule of thumb is to size cells from the average object radius or diameter,
which is what real engines do.

Second, measuring the scaling requires holding density constant. The lesson notes
that an earlier version with a fixed 100×100 arena showed broad-phase checks
growing by about 4× per doubling — the same as brute force — because rising
density means every object's neighbourhood grows, so the linear behaviour never
appears. Scaling experiments that fix the arena measure the wrong thing, and this
one is a good example of a methodological error hiding inside a correct algorithm.

</details>

**Q4. Why must ray casting use a half-open straddle test together with a strict
comparison, and what breaks at vertices and on the boundary if you do not?**

<details>
<summary>Model answer</summary>

The parity rule counts how many times a ray from the query point crosses the
polygon boundary. For an ordinary edge that number is unambiguous. The trouble is
that the ray is a one-dimensional object in a two-dimensional plane, so it has a
non-trivial intersection with the polygon only at isolated, degenerate
configurations — and those are exactly the cases real input hits, because test
data is full of lattice points, axis-aligned edges and shapes whose corners line
up with query coordinates.

The specific failure is a ray that passes exactly through a vertex. That vertex
belongs to two edges, and both of them straddle the ray's height. A naive test
that counts every edge whose endpoints lie on opposite sides of the ray's
horizontal line counts that single geometric crossing *twice*. Two crossings are
even, so the parity flips and a point inside the polygon is reported outside.
One spurious count is enough — the rule does not tolerate a majority vote, only
parity.

The half-open straddle test $(y_1 > y) \neq (y_2 > y)$ is the fix. It is
*half-open* because it uses a strict `>` on the query height against one endpoint
and compares the two results for inequality, so an endpoint sitting exactly at
height $y$ is treated as *not above* it. Exactly one of the two edges meeting at
a vertex therefore straddles, and the crossing is counted once. The same test
handles the ray lying *along* a horizontal edge: both endpoints have equal $y$,
so $(y_1 > y) \neq (y_2 > y)$ is False and that edge contributes nothing.

The strict comparison $x_{\text{cross}} > x$ is the second half. Where the ray
meets a vertex, `x_cross` can come out exactly equal to $x$, and only counting
crossings strictly to the right keeps a boundary hit from flipping the parity.
The lesson is careful about what it claims here: boundary behaviour is genuinely
ambiguous — is a point on an edge inside or outside is a convention, not a fact —
and the lesson's own test list records the choice it made, `((2,2), False, "on the
reflex vertex")`, alongside the sentence "decide and document it rather than
hoping".

Note that the two tests are not independent extras. The straddle test is also
what makes the arithmetic safe: it is evaluated before the division, and a
horizontal edge fails it, so $y_2 - y_1 \ne 0$ whenever
$x_{\text{cross}} = x_1 + (y - y_1)(x_2 - x_1)/(y_2 - y_1)$ is actually
evaluated. The vectorised numpy block relies on the same property from the other
side: horizontal edges produce `nan` after division with floating-point
arithmetic, and every comparison against `nan` is False, so they drop out
harmlessly. Common Mistake 3's real content is that the *pair* of tests is the
standard, and using `>=` in the second one gives you a plausible-looking
implementation that is wrong exactly where the geometry is interesting.

</details>

---

## Exercises and Solutions

**[ ] Exercise 1 — ** Implement Graham scan and compare it against the monotone
chain on the same point sets. Start from a point known to be on the hull (the
lowest-y, then lowest-x point) rather than an arbitrary interior point, and
show both produce the same hull vertex count.

<details>
<summary>Solution</summary>

```python
def cross(o, a, b):
    return ((a[0] - o[0]) * (b[1] - o[1])
            - (a[1] - o[1]) * (b[0] - o[0]))


def convex_hull_monotone(points):
    """Andrew's monotone chain: O(n log n), no pivot needed."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def convex_hull_graham(points):
    """Graham scan: sort by angle around a pivot, then stack.

    The pivot must itself be a hull vertex, otherwise the first sort step is
    meaningless. Lowest y then lowest x is a safe choice.
    """
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    pivot = min(pts, key=lambda p: (p[1], p[0]))
    rest = [p for p in pts if p != pivot]

    def angle_key(p):
        # Sort by angle from the positive x axis, measured counter-clockwise.
        # cross(pivot, rest[0], p) > 0 means p is counter-clockwise from rest[0].
        dx, dy = p[0] - pivot[0], p[1] - pivot[1]
        import math
        return math.atan2(dy, dx)

    rest.sort(key=angle_key)

    hull = [pivot]
    for p in rest:
        while len(hull) >= 2 and cross(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)
    return hull


import random

random.seed(5)
tests = [
    [(0, 0), (3, 0), (4, 3), (2, 5), (0, 3), (2, 2), (2, 3), (1, 1), (1, 0), (2, 0)],
]
for _ in range(6):
    n = random.randint(4, 40)
    tests.append([(random.randrange(0, 20), random.randrange(0, 20))
                  for _ in range(n)])

for i, pts in enumerate(tests):
    m = convex_hull_monotone(pts)
    g = convex_hull_graham(pts)
    same = sorted(set(m)) == sorted(set(g))
    print(f"case {i}: n={len(pts):3d}  monotone={len(m):3d}  graham={len(g):3d}"
          f"  same vertices: {same}")

# Show the angle ordering for the hand example.
pts = tests[0]
pivot = min(set(pts), key=lambda p: (p[1], p[0]))
print("\npivot =", pivot)
print("monotone hull:", convex_hull_monotone(pts))
print("graham  hull:", convex_hull_graham(pts))
```

Output:

```
case 0: n= 10  monotone=  5  graham=  5  same vertices: True
case 1: n= 20  monotone=  7  graham=  7  same vertices: True
case 2: n= 17  monotone=  6  graham=  6  same vertices: True
case 3: n= 39  monotone=  8  graham=  8  same vertices: True
case 4: n= 14  monotone=  6  graham=  6  same vertices: True
case 5: n= 23  monotone=  5  graham=  5  same vertices: True
case 6: n= 21  monotone=  9  graham=  9  same vertices: True

pivot = (0, 0)
monotone hull: [(0, 0), (3, 0), (4, 3), (2, 5), (0, 3)]
graham  hull: [(0, 0), (3, 0), (4, 3), (2, 5), (0, 3)]
```

Both agree on all seven cases, which is the real content: they are genuinely
different algorithms reaching the same answer. The key difference is the pivot.
Monotone chain needs no pivot because it scans by x-coordinate; Graham scan
needs one, and using an interior point makes the angle sort meaningless — the
first point in the sorted order may not be a hull vertex, and the resulting
polygon can be a subset of the true hull.

</details>

**[ ] Exercise 2 — ** The convex hull of a set of points is a subset of the
points themselves. Show that the *centroid* of the hull is inside the hull, and
show why this means a convex hull is a safe collision proxy: any point inside
the hull is guaranteed to be inside the shape, and any point outside is
guaranteed to be outside.

Add a test using a point cloud with a genuinely concave outline (an L-shape) and
confirm the hull correctly *fills in* the notch — explaining why that makes the
hull a conservative proxy rather than an exact one.

<details>
<summary>Solution</summary>

```python
def cross(o, a, b):
    return ((a[0] - o[0]) * (b[1] - o[1])
            - (a[1] - o[1]) * (b[0] - o[0]))


def convex_hull(points):
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def centroid(poly):
    n = len(poly)
    return (sum(p[0] for p in poly) / n, sum(p[1] for p in poly) / n)


def point_in_polygon(point, polygon):
    x, y = point
    inside = False
    n = len(polygon)
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            x_cross = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x_cross > x:
                inside = not inside
    return inside


def area(poly):
    a = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        a += x1 * y2 - x2 * y1
    return abs(a) / 2.0


# A convex pentagon.
convex_pts = [(0, 0), (3, 0), (4, 3), (2, 5), (0, 3)]
h = convex_hull(convex_pts)
c = centroid(h)
print("convex pentagon hull:", h)
print("centroid:", c)
print("centroid inside hull?", point_in_polygon(c, h))

# The same shape with interior noise: hull and centroid must not move.
noisy = convex_pts + [(2, 2), (2, 3), (1, 1), (3, 1)]
h2 = convex_hull(noisy)
print("\nwith interior noise, hull:", h2)
print("hull unchanged?", h2 == h)
print("centroid unchanged?", centroid(h2) == c)

# A concave L-shape: the hull fills in the notch.
L_points = [(0, 0), (6, 0), (6, 2), (2, 2), (2, 6), (0, 6)]
lh = convex_hull(L_points)
print("\nL-shape hull:", lh)
print("L-shape area      :", area(L_points))
print("hull area (fills in):", area(lh))
print("hull is larger:", area(lh) > area(L_points))

# A point in the notch: outside the real L, inside the hull.
notch = (3, 3)
print("\nnotch point", notch)
print("  inside the real L-shape?", point_in_polygon(notch, L_points))
print("  inside the hull?        ", point_in_polygon(notch, lh))
```

Output:

```
convex pentagon hull: [(0, 0), (3, 0), (4, 3), (2, 5), (0, 3)]
centroid: (1.8, 2.2)
centroid inside hull? True

with interior noise, hull: [(0, 0), (3, 0), (4, 3), (2, 5), (0, 3)]
hull unchanged? True
centroid unchanged? True

L-shape hull: [(0, 0), (6, 0), (6, 2), (2, 6), (0, 6)]
L-shape area      : 20.0
hull area (fills in): 28.0
hull is larger: True

notch point (3, 3)
  inside the real L-shape? False
  inside the hull?         True
```

Three facts, each useful:

1. **Interior points cannot change the hull.** Adding noise produced a
   byte-identical hull and centroid. This is the theorem
   `conv(S) = conv(H)` in action, and it is why hull algorithms are allowed to
   discard points so aggressively.
2. **The centroid of a convex polygon is inside it.** True here and true in
   general: the centroid is a convex combination of the vertices, and a convex
   set contains all convex combinations of its points. That is precisely the
   property [Lesson 100](../part08_optimization/100_convexity.md) develops.
3. **The hull is conservative, not exact.** The L-shape's real area is 20.0 but
   the hull's is 28.0: the reflex vertex (2, 2) is swallowed, and the hull's
   edge runs as a straight diagonal from (6, 2) to (2, 6) across the notch. A
   hull-based collision test therefore reports hits that are not real — which is
   the correct trade-off. The hull is cheap, and it never *misses* a collision,
   so you get false positives instead of objects tunnelling through walls.

</details>

**[ ] Exercise 3 — ** Write a segment–polygon intersection test by combining ray
casting with an edge-crossing check, and use it to answer: does the segment from
(7, 1) to (5, 1) cross the L-shaped polygon? Does the segment from (4, 1) to
(4, 5) cross it? The second one starts inside and ends outside; the first
starts and ends outside.

<details>
<summary>Solution</summary>

A segment crosses a polygon boundary if (a) its endpoints lie on opposite sides
of some edge's line, or (b) one of its endpoints is exactly on an edge. The
cleanest robust version combines a crossing count with an inside/outside test of
the endpoints.

```python
def cross(o, a, b):
    return ((a[0] - o[0]) * (b[1] - o[1])
            - (a[1] - o[1]) * (b[0] - o[0]))


def point_on_segment(p, a, b, eps=1e-9):
    """Is p on the segment a-b? Collinearity plus a bounding-box check."""
    if abs(cross(a, b, p)) > eps:
        return False
    return (min(a[0], b[0]) - eps <= p[0] <= max(a[0], b[0]) + eps
            and min(a[1], b[1]) - eps <= p[1] <= max(a[1], b[1]) + eps)


def point_in_polygon(point, polygon):
    x, y = point
    inside = False
    n = len(polygon)
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            x_cross = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x_cross > x:
                inside = not inside
    return inside


def segment_polygon_intersect(a, b, polygon):
    """True if segment a-b touches the polygon at all.

    Three cases cover everything:
      1. an endpoint lies exactly on the boundary,
      2. the segment properly crosses a polygon edge,
      3. the segment is entirely inside (both endpoints inside).
    """
    n = len(polygon)

    # Case 1: endpoint on the boundary.
    for v in polygon:
        if point_on_segment(a, v, polygon[(polygon.index(v) + 1) % n]) \
                or point_on_segment(b, v, polygon[(polygon.index(v) + 1) % n]):
            return True

    # Case 2: the segment crosses a polygon edge (proper crossing).
    for i in range(n):
        c = polygon[i]
        d = polygon[(i + 1) % n]
        # Orientations of the segment against the edge, in both directions.
        d1 = cross(a, b, c)
        d2 = cross(a, b, d)
        d3 = cross(c, d, a)
        d4 = cross(c, d, b)
        if ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0)):
            return True

    # Case 3: both endpoints strictly inside.
    return point_in_polygon(a, polygon) and point_in_polygon(b, polygon)


polygon = [(0, 0), (6, 0), (6, 2), (2, 2), (2, 6), (0, 6)]

cases = [
    ((7, 1), (5, 1), True, "outside to inside, horizontal"),
    ((4, 1), (4, 5), True, "inside to outside, vertical"),
    ((1, 1), (1, 4), True, "entirely inside"),
    ((7, 1), (8, 1), False, "entirely outside"),
    ((-2, 3), (-1, 3), False, "outside on the left"),
    ((4, 4), (5, 5), False, "in the notch to outside"),
]

for a, b, expected, why in cases:
    got = segment_polygon_intersect(a, b, polygon)
    flag = "ok " if got == expected else "FAIL"
    print(f"  [{flag}] {str(a):7s} -> {str(b):7s} : {str(got):5s}  ({why})")

# The specific questions from the exercise.
print()
print("(7,1)->(5,1) crosses?",
      segment_polygon_intersect((7, 1), (5, 1), polygon))
print("(4,1)->(4,5) crosses?",
      segment_polygon_intersect((4, 1), (4, 5), polygon))
```

Output:

```
  [ok ] (7, 1)  -> (5, 1)  : True   (outside to inside, horizontal)
  [ok ] (4, 1)  -> (4, 5)  : True   (inside to outside, vertical)
  [ok ] (1, 1)  -> (1, 4)  : True   (entirely inside)
  [ok ] (7, 1)  -> (8, 1)  : False  (entirely outside)
  [ok ] (-2, 3) -> (-1, 3) : False  (outside on the left)
  [ok ] (4, 4)  -> (5, 5)  : False  (in the notch to outside)

(7,1)->(5,1) crosses? True
(4,1)->(4,5) crosses? True
```

The two questions from the exercise both answer `True`, but for different
reasons, and that is the point. `(7,1) -> (5,1)` enters the shape through the
edge x = 6 and so trips case 2 (proper crossing). `(4,1) -> (4,5)` starts inside
and exits through the edge y = 2, which is also case 2. A naive implementation
that only tested "is an endpoint inside?" would get both of these wrong in one
direction or the other, which is exactly why all three cases are needed.

</details>

**Challenge — ** Build a small collision system: broad phase via spatial hash,
narrow phase via exact circle–circle distance. First find a bug — the obvious
"register each object in the cell containing its centre" version silently misses
collisions when the cell is smaller than the objects. Fix it by registering each
object in every cell it overlaps, then measure how the work grows with N and find
the cell size that minimises checks.

<details>
<summary>Solution</summary>

```python
from math import sqrt


def cell_key(cx, cy, cell_size):
    """Integer cell. Using // means negatives floor away from zero correctly."""
    return (int(cx // cell_size), int(cy // cell_size))


def collides(ax, ay, ar, bx, by, br):
    """Narrow phase: centre distance vs sum of radii."""
    return sqrt((ax - bx) ** 2 + (ay - by) ** 2) < ar + br


def make_scene(n, seed, arena=100.0):
    import random
    random.seed(seed)
    return [(random.uniform(0, arena), random.uniform(0, arena),
             random.uniform(0.3, 0.9)) for _ in range(n)]


def cells_for(circle, cell_size):
    """Every cell the circle's bounding box touches."""
    x, y, r = circle
    x0 = cell_key(x - r, y, cell_size)[0]
    x1 = cell_key(x + r, y, cell_size)[0]
    y0 = cell_key(x, y - r, cell_size)[1]
    y1 = cell_key(x, y + r, cell_size)[1]
    return [(cx, cy) for cx in range(x0, x1 + 1) for cy in range(y0, y1 + 1)]


def broadphase(circles, cell_size):
    """Correct broadphase: register each object in EVERY cell it overlaps."""
    cells = {}
    for c in circles:
        for key in cells_for(c, cell_size):
            cells.setdefault(key, []).append(c)

    seen = set()
    hits = []
    checks = 0
    for c in circles:
        for key in cells_for(c, cell_size):
            for other in cells.get(key, []):
                if other is c:
                    continue
                # A pair is found from both sides, so key it canonically.
                pair = (min(id(c), id(other)), max(id(c), id(other)))
                if pair in seen:
                    continue
                seen.add(pair)
                checks += 1
                if collides(*c, *other):
                    hits.append((c, other))
    return hits, checks, len(cells)


def broadphase_naive(circles, cell_size):
    """The bug: register only in the cell containing the centre."""
    cells = {}
    for c in circles:
        cells.setdefault(cell_key(c[0], c[1], cell_size), []).append(c)

    seen = set()
    hits = []
    for c in circles:
        cx, cy = cell_key(c[0], c[1], cell_size)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for other in cells.get((cx + dx, cy + dy), []):
                    if other is c:
                        continue
                    pair = (min(id(c), id(other)), max(id(c), id(other)))
                    if pair in seen:
                        continue
                    seen.add(pair)
                    if collides(*c, *other):
                        hits.append((c, other))
    return hits


def brute(circles):
    """The ground truth: every pair, tested exactly."""
    return [(a, b) for i, a in enumerate(circles) for b in circles[i + 1:]
            if collides(*a, *b)]


scene = make_scene(400, seed=7)
truth = len(brute(scene))
print("N = 400, brute force finds", truth, "colliding pairs")
print()
print(f"{'cell':>6} {'multi-cell':>12} {'naive':>8} {'cells':>7} {'correct?':>9}")
for cell in (0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0):
    hits, checks, ncells = broadphase(scene, cell)
    naive = broadphase_naive(scene, cell)
    ok = "yes" if len(hits) == truth else "NO"
    print(f"{cell:6.1f} {len(hits):12d} {len(naive):8d} {ncells:7d} {ok:>9}")

print()
print("The 'naive' column is the bug. At cell 0.5 the circles (diameter up to")
print("1.8) span four cells but are registered in only one, so collisions across")
print("cell walls are lost: 16 found instead of 42. From cell 1.5 upward the")
print("cell finally exceeds the largest diameter and the naive version is right.")

# Sweep for the cheapest cell size.
print("\ncell size sweep on narrow-phase checks (N = 400):")
best_cell, best_checks = None, None
for cell in (0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0):
    _, checks, _ = broadphase(scene, cell)
    if best_checks is None or checks < best_checks:
        best_cell, best_checks = cell, checks
    print(f"  cell {cell:5.1f} -> {checks:6d} checks")
print("best:", best_cell, "with", best_checks, "checks")

# Growth with N. The arena must grow too, or density rises and every object's
# neighbourhood grows with it, which hides the linear behaviour.
print("\ngrowth with N at cell =", best_cell, "(arena scaled as 10*sqrt(N))")
print(f"{'N':>6} {'all-pairs':>12} {'broadphase':>12} {'ratio':>10} {'hits':>6}")
results = {}
for n in (100, 200, 400, 800):
    s = make_scene(n, seed=7, arena=10.0 * n ** 0.5)
    all_pairs = n * (n - 1) // 2
    hits, checks, _ = broadphase(s, best_cell)
    results[n] = (all_pairs, checks)
    print(f"{n:6d} {all_pairs:12d} {checks:12d} "
          f"{all_pairs / checks:9.2f}x {len(hits):6d}")

print("\nratios when N doubles:")
for lo, hi in ((100, 200), (200, 400), (400, 800)):
    ap_lo, ck_lo = results[lo]
    ap_hi, ck_hi = results[hi]
    print(f"  {lo:3d} -> {hi:3d}: all-pairs x{ap_hi / ap_lo:.2f},"
          f" broadphase x{ck_hi / ck_lo:.2f}")
```

Output:

```
N = 400, brute force finds 42 colliding pairs

  cell  multi-cell    naive    cells  correct?
   0.5           42       16    4464       yes
   1.0           42       38    1773       yes
   1.5           42       42    1135       yes
   2.0           42       42     832       yes
   3.0           42       42     559       yes
   5.0           42       42     330       yes
  10.0           42       42     112       yes

The 'naive' column is the bug. At cell 0.5 the circles (diameter up to
1.8) span four cells but are registered in only one, so collisions across
cell walls are lost: 16 found instead of 42. From cell 1.5 upward the
cell finally exceeds the largest diameter and the naive version is right.

cell size sweep on narrow-phase checks (N = 400):
  cell   0.5 ->     79 checks
  cell   1.0 ->    108 checks
  cell   1.5 ->    131 checks
  cell   2.0 ->    161 checks
  cell   3.0 ->    256 checks
  cell   5.0 ->    445 checks
  cell  10.0 ->   1175 checks
best: 0.5 with 79 checks

growth with N at cell = 0.5 (arena scaled as 10*sqrt(N))
     N    all-pairs   broadphase      ratio   hits
   100         4950            4   1237.50x      3
   200        19900            7   2842.86x      4
   400        79800           17   4694.12x     10
   800       319600           24  13316.67x      7

ratios when N doubles:
  100 -> 200: all-pairs x4.02, broadphase x1.75
  200 -> 400: all-pairs x4.01, broadphase x2.43
  400 -> 800: all-pairs x4.01, broadphase x1.41
```

Three results, in increasing order of usefulness.

**The bug.** `naive` finds only 16 of 42 collisions at cell size 0.5, and the
reason is specific: a circle of radius 0.9 has diameter 1.8, so it covers a 2×2
block of 0.5-cells, but it is filed under one cell. Two overlapping circles in
different cells never get compared. This is the single most common bug in
hand-written spatial hashes, and it is invisible unless you test against brute
force — which is why the first line of the output establishes ground truth.
Note that `multi-cell` is correct at *every* cell size, including 0.5: the fix
is not "don't use small cells", it is "register the object everywhere it
appears".

**The tuning.** Cell size 0.5 minimised checks at 79, and larger cells are
strictly worse — 10.0 needed 1,175, more than brute force's 79,800 / 2 pairs in
that neighbourhood, because every query returns a huge slab of the world. So the
cheapest grid here is a *fine* one, which is the opposite of the folk wisdom that
coarse cells are cheaper. The reason is that these objects are sparse: at 400
circles over a 100×100 arena the mean density is one object per 25 cells.

**The scaling.** Doubling N multiplies all-pairs work by ~4.0 every time, which
is quadratic. Broadphase work grows by 1.75, 2.43 and 1.41 — around 2, which is
linear. The ratio all-pairs/broadphase therefore climbs from 1,237× to 13,317×,
and that growing ratio *is* the result: the gap widens without bound.

One methodological note worth keeping: the arena has to grow with N here. In an
earlier version with a fixed 100×100 arena, broadphase checks grew by ~4× per
doubling — same as brute force — because rising density means every object's
neighbourhood grows, and you never see the linear behaviour at all. Measuring
scaling requires holding density constant.

</details>
## Summary

- `cross(o, a, b)` is the 2D turn test; its sign tells you left turn, right turn,
  or collinear, and it is the basis of every 2D convexity algorithm.
- Convex hull = the smallest convex set containing the points, and its vertices
  are a subset of the points, so interior points can be discarded entirely.
- Monotone chain runs in O(n log n) by scanning left to right and popping every
  right turn; Graham scan needs a pivot that is itself a hull vertex.
- The closest pair can be found in O(n log n) because a better pair can only lie
  within distance d of the dividing line, and only O(1) neighbours matter there.
- Ray casting decides point-in-polygon by the parity of edge crossings, using a
  half-open straddle test and a strict comparison to handle vertices.
- Line–circle intersection is a quadratic whose discriminant sign gives 0, 1, or
  2 intersections.
- Broad/narrow phase separation is the key performance idea: cheap conservative
  rejection first, exact test only on survivors.
- Uniform grids, BVHs and kd-trees are spatial partitioning; cell size should be
  around the mean object size, and too coarse a grid can be worse than brute
  force.

## Next

[Part 08 — Optimisation](../part08_optimization/) starts at
[100 — Convexity](../part08_optimization/100_convexity.md). Convexity appeared in
this lesson as the property that makes the hull a valid proxy and the centroid
safe; next it is the property that makes optimisation tractable.
