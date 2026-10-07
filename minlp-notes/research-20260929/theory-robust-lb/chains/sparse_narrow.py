"""Upper-bound side for the chiral chain ("sparse-narrow" covers): are boxes that are full in all
coordinates except every PERIOD-th one, which is narrow (an interval of width 2w from a uniform
partition of [-1,1]), certified for class P_D at tolerance eps?  If every such box is certified, these
boxes form a cover with (1/w)^{#narrow} members (a computed, floating-point check).
Usage: python3 sparse_narrow.py B G EV D EPS n PERIOD w1 w2 ...  (narrow coordinates j with j % PERIOD == PERIOD-1)
"""
import sys, json
import numpy as np
from polychain import RelaxPoly, poly_class
from chiral import chain
b, g, ev = map(float, sys.argv[1:4]); d = int(sys.argv[4]); eps = float(sys.argv[5]); n = int(sys.argv[6]); PERIOD = int(sys.argv[7])
period = PERIOD
import itertools
narrow = [j for j in range(n) if j % period == period - 1]
for w in map(float, sys.argv[8:]):
    m = int(round(1 / w))
    edges = np.linspace(-1, 1, m + 1)
    worst = np.inf; worst_box = None; count = 0
    rel = RelaxPoly(chain(n, b, g, ev), poly_class(d), K=5)
    for combo in itertools.product(range(m), repeat=len(narrow)):
        l = np.full(n, -1.0); u = np.full(n, 1.0)
        for j, c in zip(narrow, combo):
            l[j], u[j] = edges[c], edges[c + 1]
        lo, up, _ = rel.bound(l, u, -eps, maxit=120)
        count += 1
        if lo < worst:
            worst, worst_box = lo, [(round(l[j], 3), round(u[j], 3)) for j in narrow]
    print(json.dumps(dict(b=b, g=g, ev=ev, cls=f"P{d}", eps=eps, n=n, narrow=narrow, w=w, boxes=count,
                          min_lower_bound=worst, certified=bool(worst >= -eps), worst_narrow=worst_box)), flush=True)
