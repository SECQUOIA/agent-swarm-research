"""Soundness test of kan_bnb.Model.evaluate (verifier's own code).

  python3 kan_soundness.py <name> <nboxes> [center-json]

Random boxes at several scales (around random centres, around the given
centre, and straddling knots of the input grids); in each box, sample points
(including points exactly at knot interval endpoints) and evaluate the
objective of R at 50 digits for EVERY admissible combination of pieces at
that point.  Every R-feasible sample must satisfy value >= box lower bound.
"""
import itertools
import json
import sys
from fractions import Fraction as Fr

import numpy as np
from mpmath import mp, mpf

from kan_bnb import Model

mp.dps = 50


def fr2mp(q):
    return mpf(q.numerator) / q.denominator


def main(name, nbox, center=None, seed=1):
    M = Model(name)
    D = M.D
    rng = np.random.default_rng(seed)
    d = M.d

    def adm(e, z):
        return [k for k, (a, b) in enumerate(e["I"]) if fr2mp(a) <= z <= fr2mp(b)]

    def phi(e, k, z):
        return sum(fr2mp(c) * z ** p for p, c in enumerate(e["P"][k])) + fr2mp(e["wb"]) * z / (1 + mp.exp(-z))

    def values(u):
        """min over admissible piece combinations of V(u); None if infeasible"""
        u = [mpf(float(t)) for t in u]
        for i, inp in enumerate(D["inputs"]):
            if not (fr2mp(inp["lo"]) <= u[i] <= fr2mp(inp["hi"])):
                return None
        # layer 1: per hidden, the set of possible h values
        best = mpf(0)
        y = fr2mp(D["beta0"])
        for h in D["hiddens"]:
            opts = []
            for i in range(d):
                e = h["edge_from"][i]
                ks = adm(e, u[i])
                if not ks:
                    return None
                opts.append([phi(e, k, u[i]) for k in ks])
            hv_all = [fr2mp(h["beta"]) + sum(c) for c in itertools.product(*opts)]
            vals = []
            for hv in hv_all:
                if not (fr2mp(h["lo"]) <= hv <= fr2mp(h["hi"])):
                    continue
                ks = adm(h["edge2"], hv)
                vals += [phi(h["edge2"], k, hv) for k in ks]
            if not vals:
                return None
            y += min(vals)        # hidden neurons do not share edges -> min separates
        return fr2mp(D["A"]) * y + fr2mp(D["B"])

    knots = [sorted({float(a) for e in inp["edges"] for (a, b) in e["I"]} |
                    {float(b) for e in inp["edges"] for (a, b) in e["I"]}) for inp in D["inputs"]]
    nviol, ntest, worst = 0, 0, None
    for t in range(nbox):
        kind = t % 3
        scale = 10.0 ** rng.uniform(-6, 0)
        if kind == 0 or center is None:
            c = M.ulo + rng.random(d) * (M.uhi - M.ulo)
        else:
            c = np.array(center) + rng.normal(size=d) * scale * 0.3
        if kind == 2:
            i = rng.integers(d)
            ks = [k for k in knots[i] if M.ulo[i] < k < M.uhi[i]]
            c[i] = ks[rng.integers(len(ks))]
        w = scale * (M.uhi - M.ulo) * rng.random(d)
        lo = np.maximum(c - w / 2, M.ulo)
        hi = np.minimum(c + w / 2, M.uhi)
        lb, ub, lb1, lb2 = M.evaluate(lo[None, :], hi[None, :], thr=np.inf, wmax3=np.inf, force3=True)
        pts = [lo + rng.random(d) * (hi - lo) for _ in range(6)] + [lo, hi, 0.5 * lo + 0.5 * hi]
        # points exactly at knot endpoints inside the box
        for i in range(d):
            for k in knots[i]:
                if lo[i] <= k <= hi[i]:
                    p = 0.5 * lo + 0.5 * hi
                    p[i] = k
                    pts.append(p)
                    break
        for p in pts:
            v = values(p)
            if v is None:
                continue
            ntest += 1
            gap = v - mpf(float(lb[0]))
            if worst is None or gap < worst[0]:
                worst = (gap, t, float(lb1[0]), float(lb2[0]))
            if gap < 0:
                nviol += 1
                print("VIOLATION box %d: value %s < lb %r" % (t, mp.nstr(v, 20), float(lb[0])))
    print("%s: %d boxes, %d feasible sample evaluations, %d violations; smallest value - lb = %s (box %d, lb1 %.6g, lb2 %.6g)"
          % (name, nbox, ntest, nviol, mp.nstr(worst[0], 5), worst[1], worst[2], worst[3]))


if __name__ == "__main__":
    center = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
    main(sys.argv[1], int(sys.argv[2]), center)
