"""Primal Shor SDP of the relaxation R (pf_model) with explicit W = x x^T and y variables
(cvxpy/Clarabel).  Diagnostic use only: residuals, eigenvalues, leaf quantities.  Returns
the constraint duals in the pf_cert 'raw' format so that pf_cert.certify can evaluate a
rigorous bound for them.

    rows: lb <= lin(y) + <Q, W> + sum qy y^2 <= ub
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../../..'))
import sys
import time

import cvxpy as cp
import numpy as np
import scipy.sparse as sp

sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3/powerflow")


def solve_primal(M, rows=None, extra=(), solver_kw=None, verbose=False):
    rows = list(M["rows"] if rows is None else rows) + list(extra)
    ys = M["ys"]
    yi = {y: q for q, y in enumerate(ys)}
    ny, n2 = len(ys), 2 * M["n"]
    z = cp.Variable(ny)
    W = cp.Variable((n2, n2), symmetric=True)
    vw = cp.vec(W, order="C")

    def mats(idx):
        Bi, Bj, Bv, Li, Lj, Lv, Qi, Qj, Qv = [], [], [], [], [], [], [], [], []
        for t, k in enumerate(idx):
            r = rows[k]
            for (i, j), c in r["Q"].items():
                c = float(c)
                if i == j:
                    Bi.append(t); Bj.append(i * n2 + i); Bv.append(c)
                else:
                    Bi += [t, t]; Bj += [i * n2 + j, j * n2 + i]; Bv += [c / 2, c / 2]
            for y, c in r["lin"].items():
                Li.append(t); Lj.append(yi[y]); Lv.append(float(c))
            for y, c in r["qy"].items():
                Qi.append(t); Qj.append(yi[y]); Qv.append(float(c))
        m = len(idx)
        return (sp.csr_matrix((Bv, (Bi, Bj)), shape=(m, n2 * n2)),
                sp.csr_matrix((Lv, (Li, Lj)), shape=(m, ny)),
                sp.csr_matrix((Qv, (Qi, Qj)), shape=(m, ny)))

    ie = [k for k, r in enumerate(rows) if r["lb"] is not None and r["ub"] is not None and r["lb"] == r["ub"]]
    iu = [k for k, r in enumerate(rows) if k not in set(ie) and r["ub"] is not None]
    il = [k for k, r in enumerate(rows) if k not in set(ie) and r["lb"] is not None]
    cons = [W >> 0]
    Be, Le, Qe = mats(ie)
    assert Qe.nnz == 0
    ce = Be @ vw + Le @ z == np.array([float(rows[k]["lb"]) for k in ie])
    Bu, Lu, Qu = mats(iu)
    assert (Qu.data >= 0).all()
    cu = Bu @ vw + Lu @ z + (Qu @ cp.square(z) if Qu.nnz else 0) <= np.array([float(rows[k]["ub"]) for k in iu])
    Bl, Ll, Ql = mats(il)
    assert Ql.nnz == 0
    cl = Bl @ vw + Ll @ z >= np.array([float(rows[k]["lb"]) for k in il])
    cons += [ce, cu, cl]
    for y, (lo, hi) in M["ybox"].items():
        if lo is not None:
            cons.append(z[yi[y]] >= float(lo))
        if hi is not None:
            cons.append(z[yi[y]] <= float(hi))
    o = M["obj"]
    c0 = np.array([float(o["lin"].get(y, 0)) for y in ys])
    q0 = np.array([float(o["qy"].get(y, 0)) for y in ys])
    obj = float(o["const"]) + c0 @ z + q0 @ cp.square(z)
    prob = cp.Problem(cp.Minimize(obj), cons)
    t = time.time()
    prob.solve(solver="CLARABEL", chordal_decomposition_enable=False, verbose=verbose, **(solver_kw or {}))
    dt = time.time() - t
    de, du, dl = ce.dual_value, cu.dual_value, cl.dual_value
    raw = [None] * len(rows)
    for t_, k in enumerate(ie):
        raw[k] = ("eq", float(de[t_]))
    up = {k: float(du[t_]) for t_, k in enumerate(iu)}
    lo = {k: float(dl[t_]) for t_, k in enumerate(il)}
    for k in range(len(rows)):
        if raw[k] is None:
            raw[k] = ("ineq", up.get(k), lo.get(k))
    return dict(rows=rows, raw=raw, W=W.value, y=z.value, value=prob.value, status=prob.status, time=dt)


def residuals(M, res):
    """max violation of every row at the primal SDP solution (W, y)."""
    W, yv = res["W"], res["y"]
    yi = {y: q for q, y in enumerate(M["ys"])}
    out = []
    for r in res["rows"]:
        v = sum(float(c) * yv[yi[y]] for y, c in r["lin"].items())
        v += sum(float(c) * W[i, j] for (i, j), c in r["Q"].items())
        v += sum(float(c) * yv[yi[y]] ** 2 for y, c in r["qy"].items())
        viol = 0.0
        if r["lb"] is not None:
            viol = max(viol, float(r["lb"]) - v)
        if r["ub"] is not None:
            viol = max(viol, v - float(r["ub"]))
        out.append((viol, r["name"]))
    return sorted(out, reverse=True)


def complex_W(M, W):
    n = M["n"]
    Wc = np.zeros((n, n), complex)
    for a in range(n):
        for b in range(n):
            Wc[a, b] = (W[2 * a, 2 * b] + W[2 * a + 1, 2 * b + 1]) + 1j * (W[2 * a + 1, 2 * b] - W[2 * a, 2 * b + 1])
    return Wc
