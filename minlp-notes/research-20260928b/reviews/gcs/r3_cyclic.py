"""Theorem 5 / Corollary 5.1 audit on random cyclic digraphs.

For each instance (2D boxes and points, nonnegative lengths):
  * REL_H with and without degree constraints;
  * transition graph of the chain on edge-states; good set T, bad set U;
  * checks: no initial mass or inflow into U; expected visits
    (I - P_TT)^{-1} equal y on T; closed-form expected cost equals a Monte
    Carlo estimate; Dijkstra walk <= E[cost] <= sum_T y cav;
  * for a common norm (all l2): OPT <= sum_e y_e cav_e  (Cor. 5.1);
  * for other lengths: record OPT > sum y cav (path version fails).
An artificial circulation is also injected into a REL_H point to exercise U.
Usage: python3 r3_cyclic.py seed n_instances
"""
import sys
import numpy as np
from rgcs import *

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
NI = int(sys.argv[2]) if len(sys.argv) > 2 else 20
rng = np.random.default_rng(seed)


def rand_inst(kind):
    n = int(rng.integers(3, 6))
    sets = {"s": Pt(rng.uniform(-3, 3, 2)), "t": Pt(rng.uniform(-3, 3, 2) + np.array([6, 0]))}
    names = [f"n{i}" for i in range(n)]
    for i, v in enumerate(names):
        c = np.array([6.0 * (i + 0.5) / n, 0]) + rng.uniform(-2, 2, 2)
        if rng.random() < 0.25:
            sets[v] = Pt(c)
        else:
            h = rng.uniform(0.2, 1.5, 2)
            sets[v] = Box(c - h, c + h)
    E = []
    for v in names:
        if rng.random() < 0.6:
            E.append(("s", v))
        if rng.random() < 0.5:
            E.append((v, "t"))
    for u in names:
        for v in names:
            if u != v and rng.random() < 0.45:
                E.append((u, v))
    if not any(e[0] == "s" for e in E):
        E.append(("s", names[0]))
    if not any(e[1] == "t" for e in E):
        E.append((names[-1], "t"))
    if kind == "l2":
        lens = L2
    elif kind == "sq":
        lens = SQ
    else:  # different weights per edge: not a common quasi-metric
        lens = {e: Len("l2") for e in E}
        lens = {}
        for e in E:
            wgt = float(rng.uniform(0.2, 3.0))
            lens[e] = Weighted(wgt)
    return G(sets, E, "s", "t", lens)


class Weighted(Len):
    def __init__(self, wgt):
        super().__init__("l2")
        self.wgt = wgt

    def persp(self, z, zp, y):
        return self.wgt * cp.norm(zp - z, 2)

    def val(self, x, xp):
        return self.wgt * float(np.linalg.norm(np.asarray(xp) - np.asarray(x)))


import cvxpy as cp  # noqa: E402


def chain_analysis(g, sol, tol=1e-6, nmc=4000):
    y = sol["y"]
    P = pair_positions(g, sol, tol)
    states = sorted(set(k for kk in P for k in kk if k != "*"))
    idx = {e: i for i, e in enumerate(states)}
    n = len(states)
    Pm = np.zeros((n, n))
    absorb = np.zeros(n)
    pi0 = np.zeros(n)
    rows = {}
    for (d, e), (l, x) in P.items():
        if d != "*":
            rows[d] = rows.get(d, 0.0) + l
    for (d, e), (l, x) in P.items():
        if d == "*":
            pi0[idx[e]] += l
        elif e == "*":
            absorb[idx[d]] += l / rows[d]
        else:
            Pm[idx[d], idx[e]] += l / rows[d]
    # good set: can reach absorption
    good = set(i for i in range(n) if absorb[i] > tol)
    changed = True
    while changed:
        changed = False
        for i in range(n):
            if i not in good and any(Pm[i, j] > tol for j in good):
                good.add(i)
                changed = True
    T = sorted(good)
    U = [i for i in range(n) if i not in good]
    inflowU = sum(Pm[i, j] * y[states[i]] for i in T for j in U) + sum(pi0[j] for j in U)
    PTT = Pm[np.ix_(T, T)]
    N = np.linalg.solve((np.eye(len(T)) - PTT).T, pi0[T])
    visit_err = max(abs(N[k] - y[states[T[k]]]) for k in range(len(T)))
    # closed-form expected cost over T
    Ecl = 0.0
    ycavT = 0.0
    ycav = 0.0
    into, outof = {}, {}
    for (d, e), (l, x) in P.items():
        if e != "*":
            into.setdefault(e, []).append((l, x))
        if d != "*":
            outof.setdefault(d, []).append((l, x))
    for e in states:
        A, B = into.get(e, []), outof.get(e, [])
        sa = sum(la for la, _ in A)
        sb = sum(lb for lb, _ in B)
        c = sum(y[e] * (la / sa) * (lb / sb) * g.len[e].val(xa, xb) for la, xa in A for lb, xb in B)
        Vu, Vv = g.sets[e[0]].V, g.sets[e[1]].V
        cv = y[e] * cav_lp(g.len[e], Vu, Vv, sol["z"][e] / y[e], sol["zp"][e] / y[e])
        ycav += cv
        if idx[e] in good:
            Ecl += c
            ycavT += cv
    # Monte Carlo
    nxt = {}
    for (d, e), (l, x) in P.items():
        nxt.setdefault(d, []).append((e, l, x))
    tot = 0.0
    lens_ = []
    for _ in range(nmc):
        opts = nxt["*"]
        pr = np.array([o[1] for o in opts])
        k = rng.choice(len(opts), p=pr / pr.sum())
        e, _, xprev = opts[k]
        cost = 0.0
        steps = 0
        while True:
            opts = nxt[e]
            pr = np.array([o[1] for o in opts])
            k = rng.choice(len(opts), p=pr / pr.sum())
            f, _, x = opts[k]
            cost += g.len[e].val(xprev, x)
            steps += 1
            if f == "*":
                break
            e, xprev = f, x
            if steps > 10000:
                break
        tot += cost
        lens_.append(steps)
    Emc = tot / nmc
    walk = pair_graph_sp(g, sol, tol)
    return dict(inflowU=inflowU, visit_err=visit_err, Ecl=Ecl, Emc=Emc, ycavT=ycavT, ycav=ycav,
                walk=walk, nU=len(U), meansteps=np.mean(lens_))


def add_circulation(g, sol, amount=0.3):
    """Inject a zero-cost-irrelevant circulation on a 2-cycle among internal vertices, if any."""
    for (u, v) in g.E:
        if (v, u) in g.E and u not in ("s", "t") and v not in ("s", "t"):
            sol = {k: dict(val) for k, val in sol.items()}
            xu = g.sets[u].V[0]
            xv = g.sets[v].V[0]
            e1, e2 = (u, v), (v, u)
            for e, (a, b) in [(e1, (xu, xv)), (e2, (xv, xu))]:
                sol["y"][e] += amount
                sol["z"][e] = sol["z"][e] + amount * a
                sol["zp"][e] = sol["zp"][e] + amount * b
            for (d, e), pos in [((e2, e1), xu), ((e1, e2), xv)]:
                sol["lam"][(d, e)] = sol["lam"].get((d, e), 0.0) + amount
                sol["w"][(d, e)] = sol["w"].get((d, e), np.zeros(2)) + amount * pos
            return sol, True
    return sol, False


viol = 0
path_fail = 0
worst_excess = -np.inf
for it in range(NI):
    kind = ["l2", "sq", "wl2"][it % 3]
    g = rand_inst(kind)
    o = opt(g)
    if not np.isfinite(o):
        continue
    for deg in (False, True):
        val, sol = relax(g, hull=True, deg=deg, return_vars=True)
        ca = chain_analysis(g, sol)
        bad = []
        rt = 2e-4 * max(1.0, abs(o))
        if ca["inflowU"] > 1e-4:
            bad.append("inflowU")
        if ca["visit_err"] > 1e-4:
            bad.append("visits")
        if abs(ca["Emc"] - ca["Ecl"]) > 0.05 * max(1, ca["Ecl"]):
            bad.append("MC")
        if ca["walk"] > ca["Ecl"] + rt or ca["Ecl"] > ca["ycavT"] + rt or ca["ycavT"] > ca["ycav"] + rt:
            bad.append("chain")
        if (not deg) and val > ca["walk"] + rt:
            bad.append("REL_H(nodeg)>walk")
        if kind == "l2" and o > ca["ycav"] + rt:
            bad.append("Cor5.1")
        pf = kind != "l2" and o > ca["ycav"] + rt
        worst_excess = max(worst_excess, (ca["Ecl"] - ca["ycavT"]) / max(1, abs(o)),
                           ((o - ca["ycav"]) / max(1, abs(o))) if kind == "l2" else -1)
        path_fail += pf
        viol += bool(bad)
        print(f"#{it:2d} {kind:3s} deg={int(deg)} |E|={len(g.E):2d} REL_H={val:.4f} OPT={o:.4f} walk={ca['walk']:.4f} "
              f"E={ca['Ecl']:.4f} (MC {ca['Emc']:.4f}, steps {ca['meansteps']:.1f}) sumTycav={ca['ycavT']:.4f} "
              f"sumycav={ca['ycav']:.4f} |U|={ca['nU']}" + ("  OPT>sum y cav" if pf else "")
              + (f"  VIOL {bad}" if bad else ""), flush=True)
    # inject a circulation and re-run the chain analysis
    val, sol = relax(g, hull=True, deg=False, return_vars=True)
    sol2, ok = add_circulation(g, sol)
    if ok:
        ca = chain_analysis(g, sol2, nmc=500)
        print(f"    circulation injected: |U|={ca['nU']} inflowU={ca['inflowU']:.2e} visit_err={ca['visit_err']:.2e} "
              f"E_T={ca['Ecl']:.4f} MC={ca['Emc']:.4f} sumTycav={ca['ycavT']:.4f} sumycav={ca['ycav']:.4f}")
print("violations:", viol, " path-version failures (non-common lengths):", path_fail)
print("worst relative excess of E over sum_T y cav, or of OPT over sum y cav (l2):", worst_excess)
