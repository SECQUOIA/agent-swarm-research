"""Root bound from the tilted simple generalized flow cover inequalities of Lim, Linderoth and
Luedtke (2018, Theorem 4 with the SGFCI as base inequality), specialized to indicator-free rows
(their z = 1), applied to both orientations of an equality row.  Covers are enumerated by brute
force, so the bound is the closure of this family (rows with at most 16 items).

In normalized row variables (z, tau) with widths u, right-hand side d, cover C with
mu = u(C) - d > 0, F subset of {i in C: u_i > mu}, m_i = u_i - mu:

    sum_{C\\F} z_i + sum_F [ (mu/u_i) z_i - (mu m_i / (u_i gamma_i(m_i))) tau_i ] <= d - sum_F m_i.

Every generated inequality is checked at all row vertices before it is added.
"""
import sys
from pathlib import Path

import numpy as np
import gurobipy as gp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rowhull.strengthen import problem_rows, root_lp, _row_point
from rowhull.rows import NormRow


def reflect(row):
    """Row in the complemented variables z' = w - z (the other orientation of an equality row)."""
    import copy
    items = []
    for it in row.items:
        jt = copy.copy(it)
        jt.a = -it.a
        items.append(jt)
    out = NormRow(items, float(row.widths.sum() - row.B), None, row.name + "-refl")
    return out


def covers(row):
    n, u, d = row.n, row.widths, row.B
    masks = np.arange(1, 1 << n, dtype=np.int64)
    bits = (masks[:, None] >> np.arange(n)) & 1
    tot = bits @ u
    ok = tot > d + 1e-9
    return bits[ok].astype(bool), tot[ok] - d


def row_vertices(row):
    n, B, w = row.n, row.B, row.widths
    out = []
    for mask in range(1 << n):
        tot = sum(w[i] for i in range(n) if mask >> i & 1)
        for j in range(n):
            if not mask >> j & 1 and -1e-9 <= B - tot <= w[j] + 1e-9:
                v = np.array([w[i] if mask >> i & 1 else 0.0 for i in range(n)]); v[j] = min(max(B - tot, 0), w[j])
                g = np.zeros(n); g[j] = row.items[j].gap(np.array([v[j]]))[0]
                out.append((v, g))
    return out


def separate(row, C, MU, z, tau, verts):
    """Most violated tilted cover: returns (coef_z, coef_tau, rhs) for  coef_z.z - coef_tau.tau <= rhs."""
    u, d = row.widths, row.B
    best = (1e-6, None)
    for c, mu in zip(C, MU):
        m = u - mu
        cand = c & (m > 1e-9) & np.array([it.f is not None for it in row.items])
        gm = np.array([row.items[i].gap(np.array([m[i]]))[0] if cand[i] else 1.0 for i in range(row.n)])
        cand &= gm > 1e-9
        kappa = np.where(cand, mu * m / (u * gm), 0.0)
        tilted = (mu / u) * z - kappa * tau + m          # contribution if i in F (moved m_i to the left)
        plain = z
        F = cand & (tilted > plain)
        lhs = np.where(F, tilted, plain)[c].sum()
        if lhs - d > best[0]:
            cz = np.where(c, np.where(F, mu / u, 1.0), 0.0)
            ct = np.where(F, kappa, 0.0)
            best = (lhs - d, (cz, ct, d - m[F].sum()))
    if best[1] is not None:
        cz, ct, rhs = best[1]
        for v, g in verts:
            assert cz @ v - ct @ g <= rhs + 1e-7, "tilted cover invalid at a vertex"
    return best[1]


def lll_bound(p, max_rounds=200):
    rows = [r for r in problem_rows(p) if r.n <= 16 and r.slack is None]
    both = [(r, False) for r in rows] + [(reflect(r), True) for r in rows]
    data = [(r, *covers(r), row_vertices(r)) for r, _ in both]
    m, v = root_lp(p)
    ncuts = 0
    for _ in range(max_rounds):
        m.optimize()
        val = {k: var.X for k, var in v.items()}
        new = 0
        for row, C, MU, verts in data:
            z, tp = _row_point(row, val)
            tau = np.array([tp.get(k, 0.0) for k in range(row.n)])
            cut = separate(row, C, MU, z, tau, verts)
            if cut is None:
                continue
            cz, ct, rhs = cut
            expr = gp.LinExpr()
            for k, it in enumerate(row.items):
                zk = it.a * (v[it.var] - it.lo) if it.a > 0 else (-it.a) * (it.hi - v[it.var])
                expr += cz[k] * zk
                if ct[k] != 0.0:
                    tk = gp.quicksum(c * v[t] for t, c in it.tvar.items()) - it.chord[0] - it.chord[1] * v[it.var]
                    expr -= ct[k] * tk
            m.addConstr(expr <= rhs)
            new += 1
        ncuts += new
        if new == 0:
            break
    m.optimize()
    return m.ObjVal, ncuts


if __name__ == "__main__":
    from instances import transport
    from rowhull.strengthen import cut_loop
    mm, nn = int(sys.argv[1]), int(sys.argv[2])
    for cap in sys.argv[3].split(","):
        for cost in sys.argv[4].split(","):
            for seed in range(int(sys.argv[5])):
                p = transport(mm, nn, seed, cap, cost)
                lb, nc = lll_bound(p)
                _, _, info = cut_loop(p)
                print(f"{p.name}: termwise {info['bound0']:.4f}  tilted-cover closure {lb:.4f} ({nc} cuts)  "
                      f"row hull {info['bound']:.4f}", flush=True)
