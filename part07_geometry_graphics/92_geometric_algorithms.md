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

Notation follows [SYMBOLS.md](../../SYMBOLS.md).

**Definition.** For o, a, b ∈ ℝ² the *cross product determinant* (2D analogue of
the cross product) is `cross(o, a, b) = (a₁ − o₁)(b₂ − o₂) − (a₂ − o₂)(b₁ − o₁)`.

**Theorem.** `cross(o, a, b) > 0` iff the turn from o→a to o→b is
counter-clockwise; `< 0` for clockwise; `= 0` iff o, a, b are collinear.

**Explanation.** This is the 3D cross product's z component with z pinned to 0,
and it is the workhorse of every 2D convexity test. The [cross product lesson](90_vectors_3d_and_cross_product.md)
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
[100 — Convexity](part08_optimization/100_convexity.md). Convexity appeared in
this lesson as the property that makes the hull a valid proxy and the centroid
safe; next it is the property that makes optimisation tractable.
