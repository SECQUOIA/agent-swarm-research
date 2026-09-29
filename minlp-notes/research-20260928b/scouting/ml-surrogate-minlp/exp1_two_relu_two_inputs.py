"""Experiment 1: facets of conv{(x, ReLU(w1 x + b1), ReLU(w2 x + b2)) : x in box}, n = 2."""
from fractions import Fraction as Fr
from hull_tools import graph_points, facets, fmt_ineq
import random

def run(name, W, b, lo, hi):
    pts = graph_points(W, b, lo, hi)
    F = facets(pts)
    names = ["x1", "x2", "y1", "y2"]
    joint = [f for f in F if f[3] != 0 and f[4] != 0]
    print(f"== {name}: W={W} b={b} box=[{lo},{hi}]  graph vertices={len(pts)}  facets={len(F)}  joint facets={len(joint)}")
    for f in F:
        tag = "JOINT" if f in joint else ("y1" if f[3] else ("y2" if f[4] else "box"))
        print(f"   [{tag:5}] {fmt_ineq(f, names)}")
    return F, joint

run("A: sign-incompatible", [[1, 1], [1, -1]], [0, 0], [-1, -1], [1, 1])
run("B: sign-compatible", [[1, 1], [2, 1]], [0, -1], [-1, -1], [1, 1])
run("C: sign-compatible, shifted", [[1, 1], [1, 2]], [Fr(-1,2), -1], [0, 0], [1, 1])
run("D: parallel planes", [[1, 1], [1, 1]], [0, -1], [-1, -1], [1, 1])
random.seed(1)
stats = []
for t in range(200):
    W = [[random.choice([-3,-2,-1,1,2,3]) for _ in range(2)] for _ in range(2)]
    b = [random.randint(-2, 2) for _ in range(2)]
    pts = graph_points(W, b, [-1, -1], [1, 1])
    try:
        F = facets(pts)
    except AssertionError:
        continue  # some neuron stable on the box -> hull not full-dimensional
    joint = [f for f in F if f[3] != 0 and f[4] != 0]
    # sign pattern compatibility: same or opposite sign pattern of weights up to flipping inputs
    s1 = [1 if v > 0 else -1 for v in W[0]]
    s2 = [1 if v > 0 else -1 for v in W[1]]
    compat = s1 == s2 or s1 == [-v for v in s2]
    stats.append((compat, len(F), len(joint), [f for f in joint]))
import collections
agg = collections.defaultdict(list)
for compat, nf, nj, J in stats:
    agg[compat].append((nf, nj))
for k, v in agg.items():
    print(f"random n=2: sign-{'compatible' if k else 'incompatible'} instances={len(v)}  mean facets={sum(a for a,_ in v)/len(v):.2f}  mean joint={sum(b for _,b in v)/len(v):.2f}  max joint={max(b for _,b in v)}  frac with joint>0={sum(1 for _,b in v if b>0)/len(v):.2f}")
# sign structure of joint facets: coefficients of (y1, y2)
sgn = collections.Counter()
for compat, nf, nj, J in stats:
    for f in J:
        sgn[(compat, (f[3] > 0) - (f[3] < 0), (f[4] > 0) - (f[4] < 0))] += 1
print("joint facet y-coefficient signs (compat, sign y1, sign y2) [ineq c0 + c.z >= 0]:", dict(sgn))
