"""Independent check of Theorem 2, 2(b), 2(c) (and the unproved "2(c) with <=" remark) of
results/row-hull-separable-concave.md.

For each instance the support function  min c.z (+ d.y) + omega.tau,  omega >= 0,  is computed
  (V) exactly (fractions) over the generators obtained by brute-force enumeration of the vertices
      of the row polytope (written from the definition of the set, not from the theorem), and
  (D) by an LP (HiGHS, float) over the description claimed in the note (extended form), and for
      n <= 4 also over the closed form written as all 3^n selections.
Both directions of "hull = description" are tested because the support functions must agree.

Only delta_i = gamma_i(r) enters for equal widths, so gamma_i is represented by
gamma_i(z) = c_i * z * (w - z) (c_i = 0 allowed), evaluated exactly.
"""
import itertools
import random
import sys
from fractions import Fraction as Fr

import numpy as np
from scipy.optimize import linprog

TOL = 1e-7
rnd = random.Random(20260921)


def gamma(ci, w, z):
    return ci * z * (w - z)


def box_row_vertices(n, w, B, sense):
    """Vertices of {0<=z<=w, sum z (sense) B} by brute force: every coordinate at a bound except
    at most one; keep feasible points; (non-vertices that are feasible do no harm to a hull)."""
    pts = set()
    for pat in itertools.product((0, 1), repeat=n):
        base = [w * p for p in pat]
        s = sum(base)
        if (sense == "=" and s == B) or (sense == "<=" and s <= B) or (sense == ">=" and s >= B):
            pts.add(tuple(base))
        for j in range(n):
            rest = s - base[j]
            rj = B - rest
            if 0 <= rj <= w:
                v = list(base)
                v[j] = rj
                pts.add(tuple(v))
    return sorted(pts)


def lp(cost, A_ub, b_ub, A_eq, b_eq, bounds):
    res = linprog(cost, A_ub=np.array(A_ub, float) if A_ub else None, b_ub=np.array(b_ub, float) if A_ub else None,
                  A_eq=np.array(A_eq, float) if A_eq else None, b_eq=np.array(b_eq, float) if A_eq else None,
                  bounds=bounds, method="highs")
    return res


def check_plain(n, k, w, r, cs, sense, dirs):
    """Theorem 2 (sense '=') and 2(b) (senses '<=', '>=')."""
    B = k * w + r
    delta = [gamma(c, w, r) for c in cs]
    V = box_row_vertices(n, w, B, sense)
    gens = [(v, [gamma(cs[i], w, v[i]) for i in range(n)]) for v in V]
    # direction "Q subset description": closed form evaluated exactly at generators
    for v, g in gens:
        m = []
        for i in range(n):
            ent = [v[i] / r, (w - v[i]) / (w - r)]
            if delta[i] != 0:
                ent.append(g[i] / delta[i])
            m.append(min(ent))
        sz = sum(v)
        rhs = Fr(1) if sense == "=" else ((sz - k * w) / r if sense == "<=" else ((k + 1) * w - sz) / (w - r))
        assert sum(m) >= rhs, ("closed form violated at generator", n, k, w, r, sense, v)
    worst = 0.0
    for (c, om) in dirs:
        exact = min(sum(c[i] * v[i] for i in range(n)) + sum(om[i] * g[i] for i in range(n)) for v, g in gens)
        # variables: z(n), tau(n), zeta(n)
        N = 3 * n
        cost = [float(x) for x in c] + [float(x) for x in om] + [0.0] * n
        A_ub, b_ub, A_eq, b_eq = [], [], [], []
        for i in range(n):
            row = [0.0] * N; row[2 * n + i] = float(r); row[i] = -1.0; A_ub.append(row); b_ub.append(0.0)
            row = [0.0] * N; row[2 * n + i] = float(w - r); row[i] = 1.0; A_ub.append(row); b_ub.append(float(w))
            row = [0.0] * N; row[2 * n + i] = float(delta[i]); row[n + i] = -1.0; A_ub.append(row); b_ub.append(0.0)
        zrow = [1.0] * n + [0.0] * (2 * n)
        zetarow = [0.0] * (2 * n) + [1.0] * n
        if sense == "=":
            A_eq.append(zrow); b_eq.append(float(B))
            A_eq.append(zetarow); b_eq.append(1.0)
        elif sense == "<=":
            A_ub.append(zrow); b_ub.append(float(B))
            A_ub.append(zetarow); b_ub.append(1.0)   # implied, harmless
            # sum zeta >= (sum z - k w)/r
            A_ub.append([1.0 / float(r)] * n + [0.0] * n + [-1.0] * n); b_ub.append(float(k * w / r))
        else:
            A_ub.append([-x for x in zrow]); b_ub.append(-float(B))
            A_ub.append(zetarow); b_ub.append(1.0)
            # sum zeta >= ((k+1) w - sum z)/(w-r)
            A_ub.append([-1.0 / float(w - r)] * n + [0.0] * n + [-1.0] * n); b_ub.append(-float((k + 1) * w / (w - r)))
        bounds = [(0, float(w))] * n + [(0, None)] * n + [(0, None)] * n
        res = lp(cost, A_ub, b_ub, A_eq, b_eq, bounds)
        assert res.status == 0, (res.status, n, k, sense)
        worst = max(worst, abs(res.fun - float(exact)))
        assert abs(res.fun - float(exact)) <= TOL * (1 + abs(float(exact))), ("EF mismatch", n, k, w, r, sense, c, om, res.fun, float(exact))
        if n <= 4:  # closed form as 3^n selections (note: "Linear description")
            A2, b2 = [], []
            for ch in itertools.product(range(3), repeat=n):
                if any(ch[i] == 0 and delta[i] == 0 for i in range(n)):
                    continue
                row = [0.0] * (2 * n); const = 0.0
                for i in range(n):
                    if ch[i] == 0:
                        row[n + i] += 1.0 / float(delta[i])
                    elif ch[i] == 1:
                        row[i] += 1.0 / float(r)
                    else:
                        row[i] += -1.0 / float(w - r); const += float(w / (w - r))
                # sum_i sel_i >= rhs
                if sense == "=":
                    rr = [0.0] * (2 * n); rc = 1.0
                elif sense == "<=":
                    rr = [1.0 / float(r)] * n + [0.0] * n; rc = -float(k * w / r)
                else:
                    rr = [-1.0 / float(w - r)] * n + [0.0] * n; rc = float((k + 1) * w / (w - r))
                A2.append([rr[t] - row[t] for t in range(2 * n)]); b2.append(const - rc)
            if sense == "=":
                res2 = lp(cost[:2 * n], A2, b2, [zrow[:2 * n]], [float(B)], bounds[:2 * n])
            elif sense == "<=":
                res2 = lp(cost[:2 * n], A2 + [zrow[:2 * n]], b2 + [float(B)], None, None, bounds[:2 * n])
            else:
                res2 = lp(cost[:2 * n], A2 + [[-x for x in zrow[:2 * n]]], b2 + [-float(B)], None, None, bounds[:2 * n])
            assert res2.status == 0
            assert abs(res2.fun - float(exact)) <= TOL * (1 + abs(float(exact))), ("closed-form mismatch", n, k, sense)
    return worst


def check_indicator(n, k, w, r, cs, sense, dirs):
    """Theorem 2(c) (sense '=') and the closing remark "the same elimination with 2(b) handles <=" ."""
    B = k * w + r
    delta = [gamma(c, w, r) for c in cs]
    V = box_row_vertices(n, w, B, sense)
    gens = []
    for v in V:
        supp = [i for i in range(n) if v[i] > 0]
        free = [i for i in range(n) if v[i] == 0]
        for sub in itertools.product((0, 1), repeat=len(free)):
            y = [1 if i in supp else 0 for i in range(n)]
            for t, i in enumerate(free):
                y[i] = sub[t]
            gens.append((v, y, [gamma(cs[i], w, v[i]) for i in range(n)]))
    worst = 0.0
    for (c, d, om) in dirs:
        exact = min(sum(c[i] * v[i] + d[i] * y[i] + om[i] * g[i] for i in range(n)) for v, y, g in gens)
        N = 4 * n  # z, y, tau, zeta
        cost = [float(x) for x in c] + [float(x) for x in d] + [float(x) for x in om] + [0.0] * n
        A_ub, b_ub, A_eq, b_eq = [], [], [], []
        for i in range(n):
            row = [0.0] * N; row[3 * n + i] = float(r); row[i] = -1.0; A_ub.append(row); b_ub.append(0.0)
            row = [0.0] * N; row[3 * n + i] = float(w - r); row[i] = 1.0; row[n + i] = -float(w); A_ub.append(row); b_ub.append(0.0)
            row = [0.0] * N; row[3 * n + i] = float(delta[i]); row[2 * n + i] = -1.0; A_ub.append(row); b_ub.append(0.0)
        zrow = [1.0] * n + [0.0] * (3 * n)
        zetarow = [0.0] * (3 * n) + [1.0] * n
        if sense == "=":
            A_eq.append(zrow); b_eq.append(float(B)); A_eq.append(zetarow); b_eq.append(1.0)
        else:
            A_ub.append(zrow); b_ub.append(float(B)); A_ub.append(zetarow); b_ub.append(1.0)
            A_ub.append([1.0 / float(r)] * n + [0.0] * (2 * n) + [-1.0] * n); b_ub.append(float(k * w / r))
        bounds = [(None, None)] * n + [(None, 1.0)] * n + [(0, None)] * n + [(0, None)] * n
        res = lp(cost, A_ub, b_ub, A_eq, b_eq, bounds)
        assert res.status == 0, (res.status, n, k, sense)
        worst = max(worst, abs(res.fun - float(exact)))
        assert abs(res.fun - float(exact)) <= TOL * (1 + abs(float(exact))), ("2(c) EF mismatch", n, k, w, r, sense, c, d, om, res.fun, float(exact))
    return worst


def rand_dirs(n, count, with_y=False):
    out = []
    for t in range(count):
        mode = t % 4
        c = [Fr(rnd.randint(-9, 9), rnd.randint(1, 5)) for _ in range(n)]
        om = [Fr(rnd.randint(0, 9), rnd.randint(1, 5)) for _ in range(n)]
        if mode == 1:   # many zero components
            c = [x if rnd.random() < 0.5 else Fr(0) for x in c]
            om = [x if rnd.random() < 0.5 else Fr(0) for x in om]
        elif mode == 2:  # pure tau direction, unit weights on a random subset
            c = [Fr(0)] * n
            om = [Fr(rnd.randint(0, 1)) for _ in range(n)]
        elif mode == 3:  # pure z direction
            om = [Fr(0)] * n
        if with_y:
            d = [Fr(rnd.randint(-9, 9), rnd.randint(1, 5)) if rnd.random() < 0.8 else Fr(0) for _ in range(n)]
            out.append((c, d, om))
        else:
            out.append((c, om))
    return out


def main():
    ninst = 0
    worst = 0.0
    rs = [Fr(1, 1000), Fr(999, 1000), Fr(1, 2), Fr(1, 3), Fr(7, 10)]
    for n in range(2, 7):
        for k in sorted({0, n - 1, n // 2, 1} & set(range(0, n))):
            for rfrac in rs:
                w = Fr(rnd.choice([1, 2, 5]), rnd.choice([1, 3]))
                r = rfrac * w
                cs = [Fr(rnd.randint(0, 6), rnd.randint(1, 3)) for _ in range(n)]
                if rnd.random() < 0.5:
                    cs[rnd.randrange(n)] = Fr(0)          # item with delta_i = 0
                if rnd.random() < 0.15:
                    cs = [Fr(0)] * n                      # all delta zero
                for sense in ("=", "<=", ">="):
                    worst = max(worst, check_plain(n, k, w, r, cs, sense, rand_dirs(n, 12)))
                    ninst += 1
                if n <= 5:
                    for sense in ("=", "<="):
                        worst = max(worst, check_indicator(n, k, w, r, cs, sense, rand_dirs(n, 12, True)))
                        ninst += 1
    print(f"instances checked: {ninst}; all support functions agree; worst abs LP-vs-exact difference {worst:.2e}")

    # Theorem 2(c) as literally stated ("y <= 1, tau >= 0, the row and the min-inequality"):
    # the point below satisfies all four but has z_4 < 0, so it is not in conv(X^y).
    w, r, k = Fr(1), Fr(1, 2), 1
    e = Fr(1, 10)
    z = [Fr(1, 2), Fr(1, 2), Fr(1, 2) + e, -e]
    y = [Fr(1)] * 4
    tau = [Fr(100)] * 4
    dl = [Fr(1, 4)] * 4
    lhs = sum(min(z[i] / r, (w * y[i] - z[i]) / (w - r), tau[i] / dl[i]) for i in range(4))
    print("2(c) literal statement: sum z =", sum(z), "(= k w + r =", k * w + r, "), y<=1, tau>=0, min-sum =", lhs,
          ">= 1 holds:", lhs >= 1, "; but z_4 =", z[3], "< 0")


if __name__ == "__main__":
    sys.exit(main())
