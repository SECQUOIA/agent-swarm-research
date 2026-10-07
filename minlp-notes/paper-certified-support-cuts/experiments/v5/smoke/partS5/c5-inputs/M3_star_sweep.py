"""M3: independent O((m+k) log(m+k)) sweep for constrained quadratic stars.

Problem (all data rational, exact Fractions):
    min a0 + a1*y + a2*y^2 + sum_i [d_i x_i^2 + (e_i y + f_i) x_i]
    s.t. ly <= y <= uy, center-only rows, l_i <= x_i <= u_i,
         rows  p*y + b*x_i <= c  (b != 0)  for leaf i.

This file is independent of research-*/theory/quadratic_star.py.  It provides
  * sweep_star(...)   -- the envelope + sorted-sweep algorithm of M3.md,
  * kkt_oracle(...)   -- exhaustive exact KKT face enumeration (exponential),
and, when run, cross-checks both against the inherited oracle support_star
on random and degenerate instances, and checks the breakpoint-count bounds
B_i <= s_i + 2 (d_i > 0) and B_i <= 2 s_i - 3 (d_i <= 0).
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[6])

import sys
sys.dont_write_bytecode = True
from fractions import Fraction as F
from itertools import combinations
import random

INF = None


# ---------------------------------------------------------------- envelopes
def max_envelope(lines, lo, hi):
    """Upper envelope of lines (alpha, beta) = alpha + beta*y on [lo, hi].

    Returns [(start, end, line)] with start < end consecutive (or a single
    degenerate piece if lo == hi).  O(n log n): sort by slope, stack.
    """
    if lo == hi:
        best = max(lines, key=lambda l: (l[0] + l[1] * lo, l))
        return [(lo, hi, best)]
    by_slope = {}
    for a, b in lines:
        if b not in by_slope or a > by_slope[b]:
            by_slope[b] = a
    ls = sorted((a, b) for b, a in by_slope.items())
    ls.sort(key=lambda l: l[1])
    hull = []

    def cross(l1, l2):  # y where l1 = l2 (slopes differ)
        return (l1[0] - l2[0]) / (l2[1] - l1[1])

    for l in ls:
        while len(hull) >= 2 and cross(hull[-2], l) <= cross(hull[-2], hull[-1]):
            hull.pop()
        hull.append(l)
    # hull lines are active left to right; breakpoints between consecutive
    pieces = []
    start = lo
    for j, l in enumerate(hull):
        end = cross(l, hull[j + 1]) if j + 1 < len(hull) else hi
        s, e = max(start, lo), min(end, hi)
        if s < e:
            pieces.append((s, e, l))
        start = max(start, end)
    return pieces


def min_envelope(lines, lo, hi):
    neg = [(-a, -b) for a, b in lines]
    return [(s, e, (-l[0], -l[1])) for s, e, l in max_envelope(neg, lo, hi)]


def merge_pieces(p1, p2):
    """Common refinement of two piece lists over the same interval."""
    pts = sorted({p[0] for p in p1} | {p[1] for p in p1} | {p[0] for p in p2} | {p[1] for p in p2})
    if len(pts) == 1:
        return [(pts[0], pts[0], p1[0][2], p2[0][2])]
    out, i, j = [], 0, 0
    for s, e in zip(pts, pts[1:]):
        while p1[i][1] <= s:
            i += 1
        while p2[j][1] <= s:
            j += 1
        out.append((s, e, p1[i][2], p2[j][2]))
    return out


def at(l, y):
    return l[0] + l[1] * y


def root(l, s, e):
    """Root of affine l strictly inside (s, e), or None (also if l == 0)."""
    if l[1] == 0:
        return None
    r = -l[0] / l[1]
    return r if s < r < e else None


# ---------------------------------------------------------------- leaf data
def leaf_lines(leaf):
    """leaf = dict(l, u, d, e, f, rows=[(p, b, c)]) with p*y + b*x <= c."""
    lower, upper = [(leaf["l"], F(0))], [(leaf["u"], F(0))]
    for p, b, c in leaf["rows"]:
        line = (c / b, -p / b)
        (upper if b > 0 else lower).append(line)
    return lower, upper


def projection(lower, upper, lo, hi):
    """{y in [lo,hi]: L(y) <= U(y)} as (a, b) or None; L-U is convex."""
    merged = merge_pieces(max_envelope(lower, lo, hi), min_envelope(upper, lo, hi))
    left = right = None
    for s, e, L, U in merged:
        h = (L[0] - U[0], L[1] - U[1])  # L - U affine on [s, e]
        hs, he = at(h, s), at(h, e)
        cand = []
        if hs <= 0:
            cand.append(s)
        if he <= 0:
            cand.append(e)
        if (hs < 0 < he) or (he < 0 < hs):
            cand.append(-h[0] / h[1])
        if cand:
            left = min(cand) if left is None else min(left, min(cand))
            right = max(cand) if right is None else max(right, max(cand))
    return None if left is None else (left, right)


def leaf_rules(leaf, lower, upper, lo, hi):
    """Sorted list [(start, end, rule)] of affine minimizer rules on I=[lo,hi]."""
    d, e, f = leaf["d"], leaf["e"], leaf["f"]
    merged = merge_pieces(max_envelope(lower, lo, hi), min_envelope(upper, lo, hi))
    out = []
    for s, t, L, U in merged:
        cuts = {s, t}
        if d > 0:
            v = (-f / (2 * d), -e / (2 * d))
            for bound in (L, U):
                r = root((v[0] - bound[0], v[1] - bound[1]), s, t)
                if r is not None:
                    cuts.add(r)
        else:
            g = (d * (L[0] + U[0]) + f, d * (L[1] + U[1]) + e)
            r = root(g, s, t)
            if r is not None:
                cuts.add(r)
        cuts = sorted(cuts)
        spans = list(zip(cuts, cuts[1:])) or [(s, t)]
        for a, b in spans:
            mid = (a + b) / 2
            if d > 0:
                v = (-f / (2 * d), -e / (2 * d))
                if at(v, mid) <= at(L, mid):
                    rule = L
                elif at(v, mid) >= at(U, mid):
                    rule = U
                else:
                    rule = v
            else:
                g = (d * (L[0] + U[0]) + f, d * (L[1] + U[1]) + e)
                rule = L if at(g, mid) * (at(U, mid) - at(L, mid)) >= 0 else U
            if out and out[-1][2] == rule and out[-1][1] == a:
                out[-1] = (out[-1][0], b, rule)
            else:
                out.append((a, b, rule))
    return out


def contribution(leaf, rule):
    """Coefficients (c0, c1, c2) of q_i(y, alpha + beta y)."""
    d, e, f = leaf["d"], leaf["e"], leaf["f"]
    al, be = rule
    return (d * al * al + f * al, 2 * d * al * be + e * al + f * be, d * be * be + e * be)


def min_quadratic(c, a, b):
    c0, c1, c2 = c
    cand = [a, b]
    if c2 > 0:
        s = -c1 / (2 * c2)
        if a < s < b:
            cand.append(s)
    return min((c0 + c1 * y + c2 * y * y, y) for y in cand)


def sweep_star(center, leaves):
    """center = dict(ly, uy, a0, a1, a2, rows=[(p, c)] meaning p*y <= c)."""
    lo, hi = center["ly"], center["uy"]
    for p, c in center["rows"]:
        if p > 0:
            hi = min(hi, c / p)
        elif p < 0:
            lo = max(lo, c / p)
        elif c < 0:
            return None
    if lo > hi or any(lf["l"] > lf["u"] for lf in leaves):
        return None
    env = [leaf_lines(lf) for lf in leaves]
    for lower, upper in env:
        pr = projection(lower, upper, lo, hi)
        if pr is None:
            return None
        lo, hi = max(lo, pr[0]), min(hi, pr[1])
        if lo > hi:
            return None
    rules = [leaf_rules(lf, lw, up, lo, hi) for lf, (lw, up) in zip(leaves, env)]
    # events: (y, leaf index, new rule)
    events = sorted((r[0], i, j) for i, rl in enumerate(rules) for j, r in enumerate(rl) if j > 0)
    cur = [0] * len(leaves)
    coef = [center["a0"], center["a1"], center["a2"]]
    contrib = []
    for i, lf in enumerate(leaves):
        cc = contribution(lf, rules[i][0][2])
        contrib.append(cc)
        coef = [x + y for x, y in zip(coef, cc)]
    best, left, k = None, lo, 0
    n_pieces = 0
    while True:
        right = events[k][0] if k < len(events) else hi
        if right > left or (lo == hi):
            cand = min_quadratic(coef, left, right)
            n_pieces += 1
            if best is None or cand < best[:2]:
                best = (cand[0], cand[1], [rules[i][cur[i]][2] for i in range(len(leaves))])
        if k >= len(events):
            break
        while k < len(events) and events[k][0] == right:
            _, i, j = events[k]
            new = contribution(leaves[i], rules[i][j][2])
            coef = [x - y + z for x, y, z in zip(coef, contrib[i], new)]
            contrib[i], cur[i] = new, j
            k += 1
        left = right
    value, y, rl = best
    point = [y] + [at(r, y) for r in rl]
    return dict(value=value, point=point, interval=(lo, hi),
                breakpoints=[len(r) - 1 for r in rules], pieces=n_pieces,
                lines=[len(lw) + len(up) for lw, up in env])


# ---------------------------------------------------------------- KKT oracle
def solve(matrix, rhs):
    n = len(rhs)
    a = [list(map(F, row)) + [F(v)] for row, v in zip(matrix, rhs)]
    for col in range(n):
        piv = next((r for r in range(col, n) if a[r][col] != 0), None)
        if piv is None:
            return None
        a[col], a[piv] = a[piv], a[col]
        pv = a[col][col]
        a[col] = [v / pv for v in a[col]]
        for r in range(n):
            if r != col and a[r][col] != 0:
                fac = a[r][col]
                a[r] = [v - fac * w for v, w in zip(a[r], a[col])]
    return [row[-1] for row in a]


def to_dense(center, leaves):
    """Return (H, g, const, A, b) for 0.5 x'Hx + g'x + const, Ax <= b; x=(y,x_1..)."""
    n = 1 + len(leaves)
    H = [[F(0)] * n for _ in range(n)]
    g = [F(0)] * n
    H[0][0] = 2 * center["a2"]
    g[0] = center["a1"]
    A, b = [], []

    def row(entries, rhs):
        r = [F(0)] * n
        for j, v in entries:
            r[j] += v
        A.append(r)
        b.append(rhs)

    row([(0, 1)], center["uy"])
    row([(0, -1)], -center["ly"])
    for p, c in center["rows"]:
        row([(0, p)], c)
    for i, lf in enumerate(leaves, start=1):
        H[i][i] = 2 * lf["d"]
        H[0][i] = H[i][0] = lf["e"]
        g[i] = lf["f"]
        row([(i, 1)], lf["u"])
        row([(i, -1)], -lf["l"])
        for p, bb, c in lf["rows"]:
            row([(0, p), (i, bb)], c)
    return H, g, center["a0"], A, b


def kkt_oracle(center, leaves):
    H, g, c0, A, b = to_dense(center, leaves)
    n = len(g)
    best = None
    for k in range(n + 1):
        for act in combinations(range(len(A)), k):
            M = [H[i] + [A[r][i] for r in act] for i in range(n)]
            M += [A[r] + [F(0)] * k for r in act]
            sol = solve(M, [-v for v in g] + [b[r] for r in act])
            if sol is None:
                continue
            x = sol[:n]
            if all(sum(ai * xi for ai, xi in zip(A[r], x)) <= b[r] for r in range(len(A))):
                val = c0 + sum(gi * xi for gi, xi in zip(g, x)) + F(1, 2) * sum(
                    H[i][j] * x[i] * x[j] for i in range(n) for j in range(n))
                best = val if best is None or val < best else best
    return best


# ---------------------------------------------------------------- inherited oracle adapter
def inherited(center, leaves):
    sys.path.insert(0, (_PUBLIC_REPO + '/research-20261002-convexification/theory'))
    from quadratic_star import support_star
    n = 1 + len(leaves)
    bounds = [(center["ly"], center["uy"])] + [(lf["l"], lf["u"]) for lf in leaves]
    rows = []
    for p, c in center["rows"]:
        a = [F(0)] * n
        a[0] = p
        rows.append((a, c))
    coeff = {}

    def put(exp, v):
        coeff[tuple(exp)] = coeff.get(tuple(exp), F(0)) + v

    z = [0] * n
    put(z, center["a0"])
    e1 = z[:]; e1[0] = 1; put(e1, center["a1"])
    e2 = z[:]; e2[0] = 2; put(e2, center["a2"])
    for i, lf in enumerate(leaves, start=1):
        for p, bb, c in lf["rows"]:
            a = [F(0)] * n
            a[0], a[i] = p, bb
            rows.append((a, c))
        ex = z[:]; ex[i] = 2; put(ex, lf["d"])
        ex = z[:]; ex[i] = 1; put(ex, lf["f"])
        ex = z[:]; ex[i] = 1; ex[0] = 1; put(ex, lf["e"])
    res = support_star(bounds, rows, coeff, 0)
    return None if res["status"] == "empty" else F(res["bound"])


# ---------------------------------------------------------------- random tests
def rq(rng, a=5, den=3):
    return F(rng.randint(-a, a), rng.randint(1, den))


def random_instance(rng, k, rows_per_leaf, degenerate=False):
    """Random star; rows are anchored at a common point so most are feasible."""
    ly = rq(rng, 2)
    uy = ly + (F(0) if degenerate and rng.random() < 0.15 else F(rng.randint(0, 4), rng.randint(1, 2)))
    y0 = ly + (uy - ly) * F(rng.randint(0, 4), 4)
    crow = []
    if rng.random() < 0.3:
        p = F(rng.choice([-1, 1, 2]))
        crow.append((p, p * y0 + F(rng.randint(-1, 3), 2)))
    center = dict(ly=ly, uy=uy, a0=rq(rng), a1=rq(rng), a2=rq(rng), rows=crow)
    leaves = []
    for _ in range(k):
        l = rq(rng, 3)
        u = l + (F(0) if degenerate and rng.random() < 0.15 else F(rng.randint(0, 4), rng.randint(1, 2)))
        x0 = l + (u - l) * F(rng.randint(0, 4), 4)
        d = rng.choice([F(0), rq(rng, 3), -abs(rq(rng, 3)), abs(rq(rng, 3))])
        rows = []
        for _ in range(rng.randint(0, rows_per_leaf)):
            p = rq(rng, 3, 2)
            b = F(rng.choice([-3, -2, -1, 1, 2, 3]), rng.randint(1, 2))
            slack = F(rng.randint(-1, 4), 2) if rng.random() < 0.9 else F(-1)
            c = p * y0 + b * x0 + (0 if degenerate and rng.random() < 0.3 else slack)
            rows.append((p, b, c))
            if degenerate and rng.random() < 0.25:  # equality row or duplicate
                rows.append((-p, -b, -c) if rng.random() < 0.5 else (p, b, c))
        leaves.append(dict(l=l, u=u, d=d, e=rq(rng, 4) if rng.random() < 0.9 else F(0), f=rq(rng, 4), rows=rows))
    return center, leaves


def main():
    rng = random.Random(3003)
    stats = dict(cases=0, feasible=0, empty=0)
    worst_ratio = 0
    for trial in range(400):
        k = 1 + trial % 3
        center, leaves = random_instance(rng, k, 4, degenerate=(trial % 2 == 0))
        sw = sweep_star(center, leaves)
        inh = inherited(center, leaves)
        orc = kkt_oracle(center, leaves) if k <= 2 else inh
        stats["cases"] += 1
        if sw is None:
            assert inh is None and orc is None, (center, leaves, inh, orc)
            stats["empty"] += 1
            continue
        stats["feasible"] += 1
        assert sw["value"] == inh == orc, (center, leaves, sw["value"], inh, orc)
        # minimizer feasibility and value
        H, g, c0, A, b = to_dense(center, leaves)
        x = sw["point"]
        assert all(sum(ai * xi for ai, xi in zip(A[r], x)) <= b[r] for r in range(len(A)))
        val = c0 + sum(gi * xi for gi, xi in zip(g, x)) + F(1, 2) * sum(
            H[i][j] * x[i] * x[j] for i in range(len(x)) for j in range(len(x)))
        assert val == sw["value"]
        # breakpoint bounds per leaf (s_i = number of lines incl. two box lines)
        for lf, B, s in zip(leaves, sw["breakpoints"], sw["lines"]):
            bound = s + 2 if lf["d"] > 0 else 2 * s - 3
            assert B <= bound, (B, s, lf)
            worst_ratio = max(worst_ratio, F(B, s))
    print(f"sweep vs inherited vs KKT: {stats['cases']} cases, {stats['feasible']} feasible, "
          f"{stats['empty']} empty; all values equal; per-leaf rule changes within bounds "
          f"(max B_i/s_i = {worst_ratio})")


if __name__ == "__main__":
    main()
