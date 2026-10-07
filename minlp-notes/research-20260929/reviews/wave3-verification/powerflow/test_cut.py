"""Randomized exact test OF the authors' node-row generator pf_bb2.node_rows
(envelope cut + cone rows + magnitude rows).  Not used to produce any bound.

For random nodes (cone of width < pi given by rational directions, magnitude
boxes) and random rank-one points V (rational coordinates), every point that
satisfies the node's cone and magnitude rows exactly must satisfy the cut row
exactly.  Sampling concentrates on the sector edges and box corners.
"""
import math
import os
import random
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "open-instances-wave3", "powerflow"))
import pf_bb2  # noqa: E402  (the code under test)

random.seed(1)


def qval(Q, x):
    return sum(c * x[i] * x[j] for (i, j), c in Q.items())


def rat(v):
    return Fr(v).limit_denominator(10**12)


checked = cut_rows = 0
worst = None
for trial in range(400):
    n = 3
    p, q = 0, 2
    a1 = random.uniform(-math.pi, math.pi)
    width = random.choice([random.uniform(0.001, 0.05), random.uniform(0.05, 1.0), random.uniform(1.0, 3.0)])
    k1 = random.choice([1, 2, Fr(1, 3)])          # non-unit directions are allowed
    d1 = (k1 * rat(math.cos(a1)), k1 * rat(math.sin(a1)))
    d2 = (rat(math.cos(a1 + width)), rat(math.sin(a1 + width)))
    lo = [Fr(random.randint(90, 100), 100), Fr(random.randint(90, 100), 100)]
    hi = [l + Fr(random.randint(1, 20), 100) for l in lo]
    node = dict(vbox={p: (lo[0], hi[0]), q: (lo[1], hi[1])}, cone={(p, q): (d1, d2)},
                vdef={k: (Fr(9, 10), Fr(11, 10)) for k in range(n)})
    rows = pf_bb2.node_rows(node)
    cut = [r for r in rows if r["kind"] == "cut"]
    if not cut:
        continue
    cut_rows += 1
    cone_rows = [r for r in rows if r["kind"] in ("branch", "volt")]
    A1 = math.atan2(float(d1[1]), float(d1[0]))
    A2 = math.atan2(float(d2[1]), float(d2[0]))
    while A2 < A1:
        A2 += 2 * math.pi
    for s in range(300):
        u = random.choice([0.0, 1.0, random.random(), 1e-9, 1 - 1e-9])
        phi = A1 + u * (A2 - A1)
        mp_ = float(random.choice([lo[0], hi[0]]) if random.random() < 0.5 else random.uniform(float(lo[0]), float(hi[0])))
        mq_ = float(random.choice([lo[1], hi[1]]) if random.random() < 0.5 else random.uniform(float(lo[1]), float(hi[1])))
        tq = random.uniform(-math.pi, math.pi)
        tp = tq + phi
        x = [Fr(0)] * (2 * n)
        x[2 * p], x[2 * p + 1] = rat(mp_ * math.cos(tp)), rat(mp_ * math.sin(tp))
        x[2 * q], x[2 * q + 1] = rat(mq_ * math.cos(tq)), rat(mq_ * math.sin(tq))
        # keep only points that satisfy the node's cone and magnitude rows exactly
        if not all((r["lb"] is None or qval(r["Q"], x) >= r["lb"]) and (r["ub"] is None or qval(r["Q"], x) <= r["ub"])
                   for r in cone_rows):
            continue
        checked += 1
        for r in cut:
            slack = r["ub"] - qval(r["Q"], x)
            assert slack >= 0, ("CUT VIOLATED", trial, s, float(slack))
            if worst is None or slack < worst:
                worst = slack
print(f"nodes with a cut: {cut_rows}; rank-one points inside the node checked: {checked}; "
      f"smallest cut slack {float(worst):.3e} (>= 0 required)")
