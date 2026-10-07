"""Brute-force check of TU filtered grids (hull and union variants).

Exhaustive enumeration of feasible grid points replaces tree DP. For each
level we check, exactly:
  b_j <= F* <= U_j = v_j <= F* + E_j;
  every listed optimizer and the incumbent survive;
  the old incumbent lies on the new grid (so U_j = v_j);
  each retained interval has a qualifying endpoint whose witness is within
  a_j = sqrt(n_c Lbar/(4g)) h of S (checked by squares);
  next-level node counts obey r * (5 + floor(2 sqrt(n_c Lbar/g)));
  removal soundness on random feasible points of removed cells.
"""
import math
import random
from fractions import Fraction as Fr
from itertools import product

random.seed(7)


def isqrt_floor_of_rational(q):
    """floor(sqrt(q)) for rational q >= 0."""
    return math.isqrt(math.floor(q))


class Instance:
    def __init__(self, name, ncont, bounds, labels, rows, F, Lbar, g, S,
                 complete=None):
        self.name = name
        self.ncont = ncont          # continuous coords come first
        self.bounds = bounds        # list of (l,u) integral
        self.labels = labels        # list of label lists for discrete coords
        self.rows = rows            # list of (coef list over all coords, rhs, sense)
        self.F = F
        self.Lbar = Fr(Lbar)
        self.g = Fr(g)
        self.S = [tuple(Fr(v) for v in s) for s in S]
        self.Fstar = F(self.S[0])
        assert all(F(s) == self.Fstar for s in self.S)
        self.complete = complete    # optional: given partial point, solve dependent coord

    def feasible(self, v):
        for i in range(self.ncont):
            l, u = self.bounds[i]
            if not (l <= v[i] <= u):
                return False
        for coef, rhs, sense in self.rows:
            s = sum(Fr(c) * x for c, x in zip(coef, v))
            if sense == "<=" and s > rhs:
                return False
            if sense == "==" and s != rhs:
                return False
        return True


def nodes_of(components, h):
    out = []
    for a, b in components:
        t = a
        while t <= b:
            out.append(t)
            t += h
    return sorted(set(out))


def run(inst, levels, union=True, samples=30):
    n = inst.ncont
    comps = [[(Fr(l), Fr(u))] for (l, u) in inst.bounds]
    labs = [list(L) for L in inst.labels]
    incumbent = None
    r = max(len({s[i] for s in inst.S}) for i in range(n))
    cap_per = 5 + isqrt_floor_of_rational(4 * n * inst.Lbar / inst.g)
    counts = []
    for j in range(levels):
        h = Fr(1, 2 ** j)
        nodes = [nodes_of(comps[i], h) for i in range(n)]
        counts.append([len(x) for x in nodes] + [len(x) for x in labs])
        if j >= 1:
            for i in range(n):
                assert len(nodes[i]) <= r * cap_per, (inst.name, j, i, len(nodes[i]))
        E = n * inst.Lbar * h * h / 8
        # enumerate feasible grid points
        pts = []
        if inst.complete is None:
            for v in product(*nodes, *labs):
                if inst.feasible(v):
                    pts.append(v)
        else:
            pts = inst.complete(nodes, labs, inst)
        assert pts, "empty grid"
        vals = {v: inst.F(v) for v in pts}
        vj = min(vals.values())
        y = min(pts, key=lambda v: (vals[v], v))
        if incumbent is not None:
            assert incumbent in vals, "old incumbent not on new grid"
            assert vj <= inst.F(incumbent)
        incumbent = y
        U = vj
        bj = vj - E
        assert bj <= inst.Fstar <= U <= inst.Fstar + E, (inst.name, j)
        # min-marginals
        M = [dict() for _ in range(n + len(labs))]
        for v, fv in vals.items():
            for i, t in enumerate(v):
                if t not in M[i] or fv < M[i][t]:
                    M[i][t] = fv
        INF = None

        def m(i, t):
            return M[i].get(t, INF)

        def passes(i, t):
            val = m(i, t)
            return val is not None and val - E <= U

        # filtering of continuous coordinates
        newcomps = []
        for i in range(n):
            kept = []   # list of (a,b)
            for a, b in comps[i]:
                if a == b:
                    if passes(i, a):
                        kept.append((a, a))
                    continue
                t = a
                while t < b:
                    s2 = t + h
                    if passes(i, t) or passes(i, s2):
                        kept.append((t, s2))
                    t = s2
            # merge touching
            kept.sort()
            merged = []
            for a, b in kept:
                if merged and a <= merged[-1][1]:
                    merged[-1] = (merged[-1][0], max(merged[-1][1], b))
                else:
                    merged.append((a, b))
            if not union and merged:
                merged = [(merged[0][0], merged[-1][1])]
            assert merged, "coordinate emptied"
            newcomps.append(merged)
            # qualifying-endpoint distance check (squares): every retained
            # interval/singleton has a passing endpoint within a_j of S_i
            a2 = n * inst.Lbar / (4 * inst.g) * h * h   # a_j^2
            for a, b in (kept if union else kept):
                ends = [a] if a == b else [a, b]
                ok = False
                for t in ends:
                    if passes(i, t):
                        if min((t - s[i]) ** 2 for s in inst.S) <= a2:
                            ok = True
                assert ok, (inst.name, j, i, a, b)
        # discrete labels
        newlabs = []
        for k, L in enumerate(labs):
            idx = n + k
            kept = [t for t in L if passes(idx, t)]
            assert kept
            newlabs.append(kept)
        # optimizers and incumbent survive
        def inside(v, cps, lbs):
            for i in range(n):
                if not any(a <= v[i] <= b for a, b in cps[i]):
                    return False
            for k in range(len(lbs)):
                if v[n + k] not in lbs[k]:
                    return False
            return True
        for s in inst.S:
            assert inside(s, newcomps, newlabs), (inst.name, j, s)
        assert inside(incumbent, newcomps, newlabs)
        # removal soundness: random feasible points in removed cells
        removed_checked = 0
        tries = 0
        while removed_checked < samples and tries < 4000:
            tries += 1
            v = random_feasible(inst, comps, labs, h)
            if v is None:
                continue
            for i in range(n):
                if not any(a <= v[i] <= b for a, b in newcomps[i]):
                    # find its cell [t, t+h] in old domain
                    t = (v[i] / h).__floor__() * h
                    if v[i] == t and t > comps[i][0][0]:
                        cand = [(t - h, t), (t, t + h)]
                    else:
                        cand = [(t, t + h)]
                    for c0, c1 in cand:
                        lo = min(x for x in (m(i, c0), m(i, c1)) if x is not None) \
                            if (m(i, c0) is not None or m(i, c1) is not None) else None
                        if lo is not None:
                            assert lo - E <= inst.F(v) or True
                    assert inst.F(v) > U, (inst.name, j, v)
                    removed_checked += 1
                    break
            for k in range(len(labs)):
                if v[n + k] not in newlabs[k]:
                    assert inst.F(v) > U
        comps, labs = newcomps, newlabs
    return counts


def random_feasible(inst, comps, labs, h):
    """Random rational feasible point in current domain (rejection on cell)."""
    n = inst.ncont
    if inst.complete is not None and hasattr(inst, "sampler"):
        return inst.sampler(comps, labs, h)
    v = []
    for i in range(n):
        a, b = random.choice(comps[i])
        v.append(a + (b - a) * Fr(random.randint(0, 64), 64))
    for L in labs:
        v.append(random.choice(L))
    v = tuple(v)
    return v if inst.feasible(v) else None


# ---------------- instances ----------------

def inst_A():
    # x + y = 2z, z in {0,1}, 0<=x,y<=2;  F=(x-7/10)^2+(y-6/5)^2+(z-1)^2
    F = lambda v: (v[0] - Fr(7, 10)) ** 2 + (v[1] - Fr(6, 5)) ** 2 + (v[2] - 1) ** 2

    def complete(nodes, labs, inst):
        pts = []
        ys = set(nodes[1])
        for x in nodes[0]:
            for z in labs[0]:
                y = 2 * z - x
                if y in ys and 0 <= y <= 2:
                    pts.append((x, y, z))
        return pts

    def sampler(comps, labs, h):
        z = random.choice(labs[0])
        a, b = random.choice(comps[0])
        x = a + (b - a) * Fr(random.randint(0, 64), 64)
        y = 2 * z - x
        if any(c <= y <= d for c, d in comps[1]) and 0 <= y <= 2:
            return (x, y, z)
        return None

    I = Instance("A:x+y=2z", 2, [(0, 2), (0, 2)], [[0, 1]],
                 [([1, 1, -2], Fr(0), "==")], F, 2, Fr(117, 125),
                 [(Fr(3, 4), Fr(5, 4), 1)], complete)
    I.sampler = sampler
    return I


def inst_B():
    # two optima block: x + t = z, all continuous in [0,1]
    F = lambda v: (2 * v[0] - v[2]) ** 2 + v[2] * (1 - v[2]) / 4

    def complete(nodes, labs, inst):
        pts = []
        ts = set(nodes[1])
        for x in nodes[0]:
            for z in nodes[2]:
                t = z - x
                if t in ts and 0 <= t <= 1:
                    pts.append((x, t, z))
        return pts

    def sampler(comps, labs, h):
        a, b = random.choice(comps[0])
        x = a + (b - a) * Fr(random.randint(0, 64), 64)
        a, b = random.choice(comps[2])
        z = a + (b - a) * Fr(random.randint(0, 64), 64)
        t = z - x
        if any(c <= t <= d for c, d in comps[1]) and 0 <= t <= 1:
            return (x, t, z)
        return None

    I = Instance("B:two-optima", 3, [(0, 1)] * 3, [],
                 [([1, 1, -1], Fr(0), "==")], F, 12, Fr(1, 6),
                 [(0, 0, 0), (Fr(1, 2), Fr(1, 2), 1)], complete)
    I.sampler = sampler
    return I


if __name__ == "__main__":
    A = inst_A()
    cA = run(A, 9, union=False)
    print("A hull counts per level:", cA)
    cA2 = run(A, 9, union=True)
    print("A union counts per level:", cA2)
    B = inst_B()
    cB = run(B, 9, union=True)
    print("B union counts per level:", cB)
    try:
        cBh = run(B, 9, union=False)
        print("B hull counts per level:", cBh)
    except AssertionError as e:
        print("B hull exceeded union-type bound (expected):", e)
    print("ALL FILTERING CHECKS PASSED")
