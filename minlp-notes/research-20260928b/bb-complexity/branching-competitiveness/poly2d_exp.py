"""Non-separable 2D exact-gap instances: omega / multi / bisection leaves versus the exact
guillotine optimum on a candidate grid (uniform 9 points, triple-point coordinates, and
omega's own cut coordinates, subsampled to at most 30 per axis).  Including omega's cuts
makes N_guill_grid <= leaves(omega) whenever they all fit.
Usage: python3 poly2d_exp.py NINST SEED"""
import sys
import numpy as np
from poly2d import Poly2, run, guill


def omega_cuts(inst, cap=20000):
    cuts = [set(), set()]
    stack = [((0.0, 1.0), (0.0, 1.0))]
    n = 0
    while stack:
        box = stack.pop(); n += 1
        if n > cap:
            return None
        v, y = inst.node(box)
        if v >= -1e-12:
            continue
        a = [(y[i] - box[i][0]) * (box[i][1] - y[i]) for i in range(2)]
        i = int(np.argmax(a)); s = float(y[i]); cuts[i].add(s)
        l, u = box[i]
        b1 = list(box); b1[i] = (l, s); b2 = list(box); b2[i] = (s, u)
        stack += [tuple(b1), tuple(b2)]
    return cuts


def grid_axis(pts, cap=30):
    pts = sorted(set(pts))
    if len(pts) > cap:
        idx = np.round(np.linspace(0, len(pts) - 1, cap)).astype(int)
        pts = [pts[i] for i in sorted(set(idx))]
    return np.array(pts)


if __name__ == "__main__":
    ninst, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = np.random.default_rng(seed)
    for t in range(ninst):
        K = int(rng.integers(4, 8))
        P = rng.uniform(0, 1, (K, 2)); mu = np.exp(rng.uniform(np.log(1e-3), np.log(0.3), K))
        eps = 10 ** rng.uniform(-6, -3)
        inst = Poly2(2 * P, -(P ** 2).sum(1) + mu, eps)
        res = {r: run(inst, r, cap=20000) for r in ("omega", "multi", "bis")}
        cuts = omega_cuts(inst)
        if cuts is None or res["omega"][0] is None:
            print(t, "skipped (cap)"); continue
        T = inst.tri[(inst.tri >= 0).all(1) & (inst.tri <= 1).all(1)] if len(inst.tri) else np.zeros((0, 2))
        g1 = grid_axis(list(np.linspace(0, 1, 9)) + T[:, 0].tolist() + list(cuts[0]))
        g2 = grid_axis(list(np.linspace(0, 1, 9)) + T[:, 1].tolist() + list(cuts[1]))
        ng, _ = guill(inst, g1, g2)
        lv = {r: v[1] for r, v in res.items()}
        print(f"{t:2d} K={K} eps={eps:.1e} G=({len(g1)},{len(g2)}) N_guill_grid={ng} leaves={lv} "
              f"ratios omega={lv['omega']/ng:.2f} multi={lv['multi']/ng:.2f} bis={lv['bis']/ng:.2f}", flush=True)
