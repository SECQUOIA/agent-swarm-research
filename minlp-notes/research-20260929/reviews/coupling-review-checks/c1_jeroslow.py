"""Independent check of Theorem 5.1 (coupling note): Jeroslow-type instance

    min sum_i c y_i (1 - y_i)  s.t.  sum_i y_i = n/2,  y in [0,1]^n,  n odd.

Written from scratch (does not import the author's jeroslow_bb.py).

1. Node bound = coupling-Lagrangian dual on the box: compares the chord
   knapsack bound with max_mu L_B(mu) computed by exact breakpoint search
   on random boxes.
2. Leaf counts of depth-first B&B (not best-first) for several branching
   rules, compared with C(n+1, (n+1)/2).
3. Outside the theorem's model: the same B&B with FBBT on the row before
   bounding (the theorem excludes bound tightening), to see whether the
   count survives.

Usage: python3 c1_jeroslow.py
"""
import random
from math import comb

c = 1.0


def f(y):
    return c * y * (1 - y)


def chord_bound(box, T):
    """min sum chord_i(y_i) s.t. sum y = T, y in box (continuous knapsack)."""
    lo = sum(l for l, u in box)
    hi = sum(u for l, u in box)
    if T < lo - 1e-12 or T > hi + 1e-12:
        return float("inf"), None
    val = sum(f(l) for l, u in box)
    y = [l for l, u in box]
    need = T - lo
    slopes = []
    for i, (l, u) in enumerate(box):
        s = (f(u) - f(l)) / (u - l) if u - l > 1e-15 else 0.0
        slopes.append((s, i))
    for s, i in sorted(slopes):
        if need <= 0:
            break
        l, u = box[i]
        step = min(u - l, need)
        y[i] += step
        val += s * step
        need -= step
    return val, y


def lagr_dual(box, T):
    """max_mu min_{y in box} sum f(y_i) + mu (sum y - T). Inner min of a
    concave f + linear at endpoints. L(mu) is concave piecewise linear with
    breakpoints at mu = -(f(u)-f(l))/(u-l); evaluate at all of them."""
    def L(mu):
        return sum(min(f(l) + mu * l, f(u) + mu * u) for l, u in box) - mu * T
    bps = [-(f(u) - f(l)) / (u - l) for l, u in box if u - l > 1e-15]
    cands = bps + [min(bps) - 10, max(bps) + 10] if bps else [0.0]
    return max(L(m) for m in cands)


def fbbt(box, T):
    lo = sum(l for l, u in box)
    hi = sum(u for l, u in box)
    nb = []
    for (l, u) in box:
        nl = max(l, T - (hi - u))
        nu = min(u, T - (lo - l))
        if nl > nu + 1e-12:
            return None
        nb.append((nl, max(nl, nu)))
    return nb


def bb(n, eps, rule, use_fbbt=False, rng=None, cap=2_000_000):
    T = n / 2
    ub = c / 4
    stack = [[(0.0, 1.0)] * n]
    leaves = 0
    nodes = 0
    while stack:
        box = stack.pop()
        nodes += 1
        if nodes > cap:
            return None
        if use_fbbt:
            box = fbbt(box, T)
            if box is None:
                leaves += 1
                continue
        v, y = chord_bound(box, T)
        if y is None or v >= ub - eps:
            leaves += 1
            continue
        gaps = []
        for i, (l, u) in enumerate(box):
            s = (f(u) - f(l)) / (u - l) if u - l > 1e-15 else 0.0
            gaps.append(f(y[i]) - (f(l) + s * (y[i] - l)))
        if rule == "maxgap-mid":
            i = max(range(n), key=lambda j: gaps[j]); l, u = box[i]; m = (l + u) / 2
        elif rule == "maxgap-at-y":
            i = max(range(n), key=lambda j: gaps[j]); l, u = box[i]
            m = min(max(y[i], l + 0.05 * (u - l)), u - 0.05 * (u - l))
        elif rule == "widest-mid":
            i = max(range(n), key=lambda j: box[j][1] - box[j][0]); l, u = box[i]; m = (l + u) / 2
        elif rule == "random":
            cand = [j for j in range(n) if gaps[j] > 1e-12] or list(range(n))
            i = rng.choice(cand); l, u = box[i]; m = l + (u - l) * rng.uniform(0.2, 0.8)
        else:
            raise ValueError(rule)
        for a, b in ((l, m), (m, u)):
            nb = list(box); nb[i] = (a, b); stack.append(nb)
    return leaves


if __name__ == "__main__":
    rng = random.Random(7)
    # 1. node bound equals the box Lagrangian dual
    worst = 0.0
    for trial in range(3000):
        n = rng.choice([3, 5, 7, 9])
        box = []
        for _ in range(n):
            a, b = sorted((rng.random(), rng.random()))
            if rng.random() < 0.3:
                a, b = 0.0, 1.0
            if b - a < 1e-3:
                b = a + 1e-3
            box.append((a, min(b, 1.0)))
        T = n / 2
        v, y = chord_bound(box, T)
        if y is None:
            continue
        d = lagr_dual(box, T)
        worst = max(worst, abs(v - d))
    print(f"[1] max |chord-knapsack bound - max_mu L_B(mu)| over random feasible boxes: {worst:.2e}")

    # 2./3. leaf counts
    print("[2] n  C(n+1,(n+1)/2)  leaves by rule (no FBBT)  | [3] with FBBT (outside model)")
    for n in [3, 5, 7, 9, 11, 13]:
        lb = comb(n + 1, (n + 1) // 2)
        res = {}
        for rule in ["maxgap-mid", "maxgap-at-y", "widest-mid", "random"]:
            res[rule] = bb(n, 0.01, rule, rng=random.Random(n))
        resf = {}
        for rule in ["maxgap-mid", "maxgap-at-y", "widest-mid"]:
            resf[rule] = bb(n, 0.01, rule, use_fbbt=True, rng=random.Random(n))
        ok = all(v is None or v >= lb for v in res.values())
        print(f"    {n:2d} {lb:7d}  {res}  ok={ok} | FBBT {resf}")
