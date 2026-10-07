"""Reviewer's independent exact checks on the two-switch toy of kappa-negative.md Section 9.1.

Toy: x' = u, |u| <= 1, x0 = 0, T = 2, a = 4 on [0, t1), -4 on [t1, t2), 4 on [t2, 2], Phi = (x - 3)^2 / 2
(phi1 = -3, phi2 = 1, constant 9/2 dropped), k constant, box |x| <= 4.
usage: python3 v_two.py K t1 t2 N g1 g2   (g1, g2: guesses for the switching stages)
"""
import json
import sys
import time
from fractions import Fraction as Fr

import numpy as np

from vtoy import Toy, traj, H_entry, kkt_check, node_bound, stage_loss, terminal_loss, coord_refine


def toy2(k, t1, t2):
    return Toy(a_pts=((0, 4), (t1, -4), (t2, 4)), k_pts=((0, k),), phi1=-3, phi2=1, R=4)


def pattern(N, m1, v1, m2, v2):
    u = [Fr(1)] * N
    for t in range(m1, m2):
        u[t] = Fr(-1)
    u[m1] = v1
    u[m2] = v2
    return u


def qp2(g, H, lo, hi):
    """min g.z + z'Hz/2 over a 2-box, exact, by faces."""
    import itertools
    best = None
    for pat in itertools.product((0, 1, 2), repeat=2):
        z = [lo[i] if pat[i] == 0 else hi[i] for i in range(2)]
        free = [i for i in range(2) if pat[i] == 2]
        if len(free) == 1:
            i = free[0]; j = 1 - i
            if H[i][i] == 0:
                continue
            z[i] = -(g[i] + H[i][j] * z[j]) / H[i][i]
            if not lo[i] <= z[i] <= hi[i]:
                continue
        elif len(free) == 2:
            det = H[0][0] * H[1][1] - H[0][1] ** 2
            if det == 0:
                continue
            z = [(-g[0] * H[1][1] + H[0][1] * g[1]) / det, (H[0][1] * g[0] - H[0][0] * g[1]) / det]
            if not all(lo[i] <= z[i] <= hi[i] for i in range(2)):
                continue
        val = g[0] * z[0] + g[1] * z[1] + (H[0][0] * z[0] ** 2 + 2 * H[0][1] * z[0] * z[1] + H[1][1] * z[1] ** 2) / 2
        if best is None or val < best[0]:
            best = (val, z)
    return best


def scan(toy, N, g1, g2, W):
    """All patterns (m1, v1, m2, v2) with m1, m2 within W of the guesses; (v1, v2) exact 2-D QP optimum.
    Returns list of (J, m1, v1, m2, v2) sorted, exact."""
    _, k = toy.data(N)
    h = toy.T / N
    res = []
    for m1 in range(g1 - W, g1 + W + 1):
        for m2 in range(g2 - W, g2 + W + 1):
            E0 = traj(toy, N, pattern(N, m1, Fr(0), m2, Fr(0)))
            g = [h * E0["sig"][m1], h * E0["sig"][m2]]
            H = [[H_entry(toy, N, k, m1, m1), H_entry(toy, N, k, m1, m2)],
                 [H_entry(toy, N, k, m2, m1), H_entry(toy, N, k, m2, m2)]]
            val, z = qp2(g, H, [Fr(-1)] * 2, [Fr(1)] * 2)
            res.append((E0["J"] + val, m1, z[0], m2, z[1]))
    res.sort(key=lambda q: q[0])
    return res


def lifted_interval(toy, E, P, n):
    N, h, k = E["N"], E["h"], E["k"]
    dlo, dhi = Fr(-1) - E["u"][n], Fr(1) - E["u"][n]
    for t in range(N):
        if t == n:
            continue
        ut = E["u"][t]
        if ut not in (Fr(-1), Fr(1)):
            return None
        omf = Fr(-2) if ut == 1 else Fr(2)
        kap = P[t + 1]
        e = H_entry(toy, N, k, t, n) / h
        c0 = h * E["sig"][t] * omf + h * h * kap * omf * omf / 2
        c1 = h * e * omf
        if c1 == 0:
            if c0 < 0:
                return None
            continue
        root = -c0 / c1
        if c1 > 0:
            dlo = max(dlo, root)
        else:
            dhi = min(dhi, root)
    if not dlo <= 0 <= dhi:
        return None
    return E["u"][n] + dlo, E["u"][n] + dhi


def main():
    k = Fr(sys.argv[1])
    # 'f:0.7' = Fraction(float 0.7), the author's convention (binary value of the decimal)
    t1, t2 = [Fr(float(s[2:])) if s.startswith('f:') else Fr(s) for s in sys.argv[2:4]]
    N, g1, g2 = int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
    t0 = time.time()
    toy = toy2(k, t1, t2)
    h = toy.T / N
    res = scan(toy, N, g1, g2, 6)
    out = dict(k=float(k), t1=float(t1), t2=float(t2), N=N)
    top = []
    for (J, m1, v1, m2, v2) in res[:6]:
        E = traj(toy, N, pattern(N, m1, v1, m2, v2))
        ok, frac = kkt_check(E)
        top.append(dict(J_minus_best_h2=float((J - res[0][0]) / h ** 2), m1=m1, v1=float(v1), m2=m2, v2=float(v2), kkt=ok,
                        frac=frac if ok else None))
    out["top_patterns"] = top
    J, m1, v1, m2, v2 = res[0]
    E = traj(toy, N, pattern(N, m1, v1, m2, v2))
    ok, frac = kkt_check(E)
    assert ok
    P = [-k] * (N + 1)
    lo = [Fr(-1)] * N; hi = [Fr(1)] * N
    B0, losses, LN = node_bound(toy, E, P, lo, hi)
    fail = [(t, float(v / h ** 2)) for t, v in enumerate(losses) if v > 0]
    out.update(best=dict(m1=m1, v1=float(v1), m2=m2, v2=float(v2), frac=frac), J=float(E["J"]),
               plain_gap_h2=float((E["J"] - B0) / h ** 2), failing=fail, terminal_loss=float(LN),
               margins_sig_over_h={t: [round(float(E["sig"][s] / h), 4) for s in (t - 1, t, t + 1)] for t in (m1, m2)})
    if len(fail) == 1:
        n = fail[0][0]
        V = lifted_interval(toy, E, P, n)
        out["V"] = None if V is None else [float(V[0]), float(V[1])]
        if V is not None:
            # end checks from scratch
            ends = []
            for v in V:
                u = list(E["u"]); u[n] = v
                Z = traj(toy, N, u)
                ends.append(float(max(stage_loss(Z, P, t, Fr(-1), Fr(1), toy.R) for t in range(N) if t != n)))
            Hnn = H_entry(toy, N, E["k"], n, n)
            cands = list(V)
            if Hnn > 0:
                vs = E["u"][n] - h * E["sig"][n] / Hnn
                if V[0] <= vs <= V[1]:
                    cands.append(vs)
            Bl = min(E["J"] + h * E["sig"][n] * (v - E["u"][n]) + Hnn * (v - E["u"][n]) ** 2 / 2 for v in cands)
            out.update(ends_max_loss=ends, lifted_minus_J=float(Bl - E["J"]))
            outs = []
            near = sorted(set(range(m1 - 4, m1 + 5)) | set(range(m2 - 4, m2 + 5)))

            def cover(l, r, depth):
                u = list(E["u"]); u[n] = r if E["u"][n] > r else l
                lo2 = list(lo); hi2 = list(hi); lo2[n], hi2[n] = l, r
                A = coord_refine(toy, traj(toy, N, u), lo2, hi2, near)
                B, Ls, LN2 = node_bound(toy, A, P, lo2, hi2)
                rec = dict(l=float(l), r=float(r), anchor_minus_J_h2=float((A["J"] - E["J"]) / h ** 2),
                           bound_minus_J_h2=float((B - E["J"]) / h ** 2),
                           failing=[(t, float(v / h ** 2)) for t, v in enumerate(Ls) if v > 0])
                if A["J"] < E["J"]:
                    rec["BETTER_POINT"] = True
                if B >= E["J"] or depth >= 8:
                    outs.append(rec)
                    return
                rec["split"] = True
                outs.append(rec)
                m = (l + r) / 2
                cover(l, m, depth + 1)
                cover(m, r, depth + 1)
            for (l, r) in ((Fr(-1), V[0]), (V[1], Fr(1))):
                if r > l:
                    cover(l, r, 0)
            out["outer"] = outs
            leaves = [o for o in outs if not o.get("split")]
            out["certified"] = (Bl >= E["J"] and all(e == 0 for e in ends) and all(o["bound_minus_J_h2"] >= 0 for o in leaves))
            out["n_nodes_total"] = 1 + len(outs)
            out["n_leaves"] = 1 + len(leaves)
    out["time"] = round(time.time() - t0, 1)
    print(json.dumps(out), flush=True)


if __name__ == "__main__":
    main()
