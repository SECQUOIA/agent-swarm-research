"""Gibbs instances: own multipliers and own primal point.

Method (differs from the authors' multistart SLSQP):
  1. Tangent-plane LP on a dense simplex grid: maximise lambda.b subject to
     lambda.y <= G_type(y) at every grid point y, for every phase type present.
     (This is the dual of the convexified problem; it finds the global phase
     split directly, not a local minimum.)
  2. Active grid points are clustered; each cluster seeds one phase.
  3. 60-digit Newton on the KKT system grad G_p(n_p) = lambda, sum_p n_p = b.
Output: logs/<name>_kkt.json with lambda (40 digits) and the phase amounts.
"""
import json
import sys

import mpmath
import numpy as np
import sympy as sp
from scipy.optimize import linprog

import common
import gibbs_sym


def main(name):
    A = gibbs_sym.analyse(name, verbose=False)
    G, y, b = A["G"], A["y"], [sp.Rational(v) for v in A["b"]]
    bf = np.array([float(v) for v in b])
    types = [0] if name == "ex6_2_7" else [0, 2]  # distinct phase types
    slot_type = {0: 0, 1: 0, 2: 0} if name == "ex6_2_7" else {0: 0, 1: 0, 2: 2}
    fnum = {p: sp.lambdify(y, G[p], "numpy") for p in types}
    # grid: mixed log/uniform nodes in each coordinate
    nodes = np.unique(np.concatenate([np.logspace(-9, -1, 120), np.linspace(0, 1, 401)[1:-1]]))
    U, V = np.meshgrid(nodes, nodes, indexing="ij")
    W = 1 - U - V
    ok = W > 1e-9
    Y = np.stack([U[ok], V[ok], W[ok]], 1)
    rows, rhs, tag = [], [], []
    with np.errstate(all="ignore"):
        for p in types:
            g = fnum[p](Y[:, 0], Y[:, 1], Y[:, 2])
            good = np.isfinite(g)
            rows.append(Y[good]); rhs.append(g[good]); tag += [p] * int(good.sum())
    Ag = np.concatenate(rows); bg = np.concatenate(rhs); tag = np.array(tag)
    res = linprog(-bf, A_ub=Ag, b_ub=bg, bounds=[(None, None)] * 3, method="highs")
    assert res.status == 0, res.message
    lam0 = res.x
    slack = bg - Ag @ lam0
    print(name, "grid points", len(bg), "LP lambda", lam0, "LP value", -res.fun)
    # cluster near-active points per type
    seeds = []
    for p in types:
        idx = np.where((tag == p) & (slack < 1e-4 * max(1, np.abs(bg).max())))[0]
        idx = idx[np.argsort(slack[idx])]
        cl = []
        for i in idx:
            if all(np.abs(Ag[i] - Ag[j]).max() > 0.05 for j in cl):
                cl.append(i)
        seeds += [(p, Ag[i], slack[i]) for i in cl[:4]]
    for s in seeds:
        print("  seed type", s[0], "y", s[1], "slack", s[2])
    # assign seeds to slots, then solve the phase amounts from the LP-like mass balance
    slots = sorted(slot_type)
    used = []
    assign = {}
    for sl in slots:
        cand = [k for k, s in enumerate(seeds) if s[0] == slot_type[sl] and k not in used]
        k = min(cand, key=lambda k: seeds[k][2])
        used.append(k); assign[sl] = seeds[k][1]
    Ymat = np.array([assign[sl] for sl in slots]).T  # columns = phase compositions
    tvec = np.linalg.solve(Ymat, bf)
    print("  initial phase totals", tvec)
    # Newton at 60 digits on the 12x12 KKT system
    mpmath.mp.dps = 60
    nsym = sp.symbols("n0:9", positive=True)
    lsym = sp.symbols("l0:3")
    eqs = []
    for sl in slots:
        Gs = G[slot_type[sl]].subs({y[i]: nsym[3 * i + sl] for i in range(3)}, simultaneous=True)
        for i in range(3):
            eqs.append(sp.diff(Gs, nsym[3 * i + sl]) - lsym[i])
    for i in range(3):
        eqs.append(nsym[3 * i] + nsym[3 * i + 1] + nsym[3 * i + 2] - b[i])
    varsx = list(nsym) + list(lsym)
    Jsym = sp.Matrix(eqs).jacobian(varsx)
    fF = sp.lambdify(varsx, eqs, "mpmath")
    fJ = sp.lambdify(varsx, Jsym, "mpmath")
    z = [mpmath.mpf(0)] * 12
    for sl in slots:
        for i in range(3):
            z[3 * i + sl] = mpmath.mpf(float(tvec[slots.index(sl)] * Ymat[i, slots.index(sl)]))
    for i in range(3):
        z[9 + i] = mpmath.mpf(float(lam0[i]))
    for it in range(60):
        Fv = mpmath.matrix(fF(*z))
        nr = max(abs(v) for v in Fv)
        if nr < mpmath.mpf(10) ** -55:
            break
        Jv = mpmath.matrix(fJ(*z))
        dz = mpmath.lu_solve(Jv, -Fv)
        step = 1
        while any(z[k] + step * dz[k] <= 0 for k in range(9)):
            step /= 2
        z = [z[k] + step * dz[k] for k in range(12)]
    Fv = mpmath.matrix(fF(*z))
    nr = max(abs(v) for v in Fv)
    print("  Newton iterations", it, "residual", mpmath.nstr(nr, 3))
    lam = z[9:]
    nn = z[:9]
    # objective value at the KKT point
    x = [nn[j] for j in range(9)]
    f = common.obj_value(A["m"], x, common.mpnum, common.MPFNS)
    lb = sum(lam[i] * b[i] for i in range(3))
    tot = [sum(nn[3 * i + sl] for i in range(3)) for sl in slots]
    comp = [[nn[3 * i + sl] / tot[k] for i in range(3)] for k, sl in enumerate(slots)]
    print("  lambda", [mpmath.nstr(v, 20) for v in lam])
    print("  f(KKT)", mpmath.nstr(f, 25), " lambda.b", mpmath.nstr(lb, 25))
    for k, sl in enumerate(slots):
        print("  slot", sl, "t", mpmath.nstr(tot[k], 8), "y", [mpmath.nstr(v, 6) for v in comp[k]])
    out = dict(name=name, lam=[mpmath.nstr(v, 45) for v in lam], n=[mpmath.nstr(v, 45) for v in nn],
               kkt_residual=mpmath.nstr(nr, 3), f_kkt=mpmath.nstr(f, 30), lam_dot_b=mpmath.nstr(lb, 30),
               lp_lambda=list(map(float, lam0)), lp_value=float(-res.fun),
               phases=[dict(slot=sl, t=mpmath.nstr(tot[k], 20), y=[mpmath.nstr(v, 20) for v in comp[k]])
                       for k, sl in enumerate(slots)])
    json.dump(out, open("logs/%s_kkt.json" % name, "w"), indent=1)


if __name__ == "__main__":
    for nm in sys.argv[1:]:
        main(nm)
