"""Lagrangian (Shor/SDP) dual of the quadratic relaxation R of pf_model, solved
numerically with cvxpy/Clarabel to obtain multipliers.  The multipliers are only
a starting point; pf_cert.py evaluates the bound rigorously for them.

Lagrangian: for multipliers w_r on the rows (free on equalities, sign-constrained
on inequalities),  L = obj(y) + sum_r w_r (expr_r - rhs_r)
            = const(w) + sum_y (sigma_y y^2 + kappa_y y) + x^T A(w) x.
Dual function: const + sum_y min_y(...) + [A(w) psd].
"""
import sys
from fractions import Fraction as Fr

import cvxpy as cp
import numpy as np
import scipy.sparse as sp

import pf_model as pm


def row_multipliers(M):
    """variables and the net multiplier expression w_r and constant c_r for every row."""
    ws, cs, vars_ = [], [], []
    for r in M["rows"]:
        if r["lb"] is not None and r["ub"] is not None and r["lb"] == r["ub"]:
            v = cp.Variable()
            ws.append(v); cs.append(-float(r["lb"]) * v); vars_.append(("eq", v))
        else:
            w, c = 0, 0
            vp = vm = None
            if r["ub"] is not None:
                vp = cp.Variable(nonneg=True)
                w = w + vp; c = c - float(r["ub"]) * vp
            if r["lb"] is not None:
                vm = cp.Variable(nonneg=True)
                w = w - vm; c = c + float(r["lb"]) * vm
            ws.append(w); cs.append(c); vars_.append(("ineq", vp, vm))
    return ws, cs, vars_


def build_A(M, wvec):
    """A(w) = sum_r w_r Qsym_r as a cvxpy expression (2n x 2n)."""
    n2 = 2 * M["n"]
    rows_i, cols_i, vals = [], [], []
    for k, r in enumerate(M["rows"]):
        for (i, j), c in r["Q"].items():
            c = float(c)
            if i == j:
                rows_i.append(i * n2 + i); cols_i.append(k); vals.append(c)
            else:
                rows_i.append(i * n2 + j); cols_i.append(k); vals.append(c / 2)
                rows_i.append(j * n2 + i); cols_i.append(k); vals.append(c / 2)
    B = sp.csr_matrix((vals, (rows_i, cols_i)), shape=(n2 * n2, len(M["rows"])))
    return cp.reshape(B @ wvec, (n2, n2), order="C")


def solve_dual(M, solver="CLARABEL", verbose=False):
    ws, cs, vars_ = row_multipliers(M)
    W = cp.hstack([w if isinstance(w, cp.Expression) else cp.Constant(w) for w in ws])
    A = build_A(M, W)
    obj = float(M["obj"]["const"]) + cp.sum(cp.hstack(cs))
    cons = [0.5 * (A + A.T) >> 0]
    # y terms
    ys = M["ys"]
    kappa = {y: float(M["obj"]["lin"].get(y, 0)) for y in ys}
    sig_const = {y: float(M["obj"]["qy"].get(y, 0)) for y in ys}
    kap_terms = {y: [] for y in ys}
    sig_terms = {y: [] for y in ys}
    for k, r in enumerate(M["rows"]):
        for y, c in r["lin"].items():
            kap_terms[y].append((k, float(c)))
        for y, c in r["qy"].items():
            sig_terms[y].append((k, float(c)))
    terms = []
    for y in ys:
        kap = kappa[y] + sum(c * ws[k] for k, c in kap_terms[y]) if kap_terms[y] else cp.Constant(kappa[y])
        sig = sig_const[y] + (sum(c * ws[k] for k, c in sig_terms[y]) if sig_terms[y] else 0)
        box = M["ybox"].get(y)
        if box is not None and box[0] is not None and box[1] is not None:
            l, u = float(box[0]), float(box[1])
            bp = cp.Variable(nonneg=True); bm = cp.Variable(nonneg=True)
            kk = kap + bp - bm
            terms.append(-bp * u + bm * l)
            if sig_terms[y] or sig_const[y] > 0:
                if sig_terms[y]:
                    terms.append(-cp.quad_over_lin(kk, 4 * sig))
                else:
                    terms.append(-cp.square(kk) / (4 * sig_const[y]))
            else:
                cons.append(kk == 0)
        else:
            assert box is None or (box[0] is None and box[1] is None), "half-bounded y not handled"
            if sig_terms[y]:
                terms.append(-cp.quad_over_lin(kap, 4 * sig))
            elif sig_const[y] > 0:
                terms.append(-cp.square(kap) / (4 * sig_const[y]))
            else:
                cons.append(kap == 0)
    prob = cp.Problem(cp.Maximize(obj + cp.sum(cp.hstack(terms))), cons)
    prob.solve(solver=solver, verbose=verbose)
    wval = np.array([float(w.value) if isinstance(w, cp.Expression) else float(w) for w in ws])
    # raw sign-split values for the certificate
    raw = []
    for v in vars_:
        if v[0] == "eq":
            raw.append(("eq", float(v[1].value)))
        else:
            raw.append(("ineq", None if v[1] is None else float(v[1].value), None if v[2] is None else float(v[2].value)))
    return prob.value, prob.status, raw


if __name__ == "__main__":
    import time
    name = sys.argv[1]
    M = pm.decode(name)
    t = time.time()
    val, st, raw = solve_dual(M, solver=sys.argv[2] if len(sys.argv) > 2 else "CLARABEL")
    print(name, "SDP dual value", val, st, f"{time.time()-t:.1f}s")


def solve_dual_vec(M, solver="CLARABEL", verbose=False, **kw):
    """Same dual as solve_dual, with vectorized multipliers (fast cvxpy compile)."""
    rows = M["rows"]
    R = len(rows)
    iseq = np.array([r["lb"] is not None and r["ub"] is not None and r["lb"] == r["ub"] for r in rows])
    hasub = np.array([(r["ub"] is not None) and not e for r, e in zip(rows, iseq)])
    haslb = np.array([(r["lb"] is not None) and not e for r, e in zip(rows, iseq)])
    ne, nu, nl = iseq.sum(), hasub.sum(), haslb.sum()
    me = cp.Variable(ne); mu = cp.Variable(nu, nonneg=True); ml = cp.Variable(nl, nonneg=True)
    # w = Pe me + Pu mu - Pl ml
    def sel(mask):
        idx = np.where(mask)[0]
        return sp.csr_matrix((np.ones(len(idx)), (idx, np.arange(len(idx)))), shape=(R, len(idx)))
    Pe, Pu, Pl = sel(iseq), sel(hasub), sel(haslb)
    w = Pe @ me + Pu @ mu - Pl @ ml
    rhs_e = np.array([float(r["lb"]) for r, e in zip(rows, iseq) if e])
    ub_u = np.array([float(r["ub"]) for r, e in zip(rows, hasub) if e])
    lb_l = np.array([float(r["lb"]) for r, e in zip(rows, haslb) if e])
    const = float(M["obj"]["const"]) - rhs_e @ me - ub_u @ mu + lb_l @ ml
    A = build_A(M, w)
    cons = [0.5 * (A + A.T) >> 0]
    ys = M["ys"]
    yi = {y: q for q, y in enumerate(ys)}
    ny = len(ys)
    kr, kc, kv, sr, sc, sv = [], [], [], [], [], []
    for k, r in enumerate(rows):
        for y, c in r["lin"].items():
            kr.append(yi[y]); kc.append(k); kv.append(float(c))
        for y, c in r["qy"].items():
            sr.append(yi[y]); sc.append(k); sv.append(float(c))
    Kmat = sp.csr_matrix((kv, (kr, kc)), shape=(ny, R))
    Smat = sp.csr_matrix((sv, (sr, sc)), shape=(ny, R))
    k0 = np.array([float(M["obj"]["lin"].get(y, 0)) for y in ys])
    s0 = np.array([float(M["obj"]["qy"].get(y, 0)) for y in ys])
    kap = k0 + Kmat @ w
    sig = s0 + Smat @ w
    hasq = np.array([Smat.getrow(q).nnz > 0 for q in range(ny)])
    box = [M["ybox"].get(y) for y in ys]
    isbox = np.array([b is not None for b in box])
    terms = []
    # boxed y: box multipliers
    bi = np.where(isbox)[0]
    if len(bi):
        bp = cp.Variable(len(bi), nonneg=True); bm = cp.Variable(len(bi), nonneg=True)
        l = np.array([float(box[q][0]) for q in bi]); u = np.array([float(box[q][1]) for q in bi])
        kk = kap[bi] + bp - bm
        terms.append(-u @ bp + l @ bm)
        q1 = [q for q in range(len(bi)) if not hasq[bi[q]] and s0[bi[q]] > 0]
        q0 = [q for q in range(len(bi)) if not hasq[bi[q]] and s0[bi[q]] == 0]
        q2 = [q for q in range(len(bi)) if hasq[bi[q]]]
        if q2:
            t2 = cp.Variable(len(q2))
            sg2 = sig[bi[q2]]
            cons.append(cp.SOC(sg2 + t2, cp.vstack([kk[q2], sg2 - t2]), axis=0))
            terms.append(-cp.sum(t2))
        if q1:
            c2 = s0[bi[q1]]
            terms.append(-cp.sum_squares(cp.multiply(1 / np.sqrt(4 * c2), kk[q1])))
        if q0:
            cons.append(kk[q0] == 0)
    fi = np.where(~isbox)[0]
    f1 = [q for q in fi if hasq[q]]
    f0 = [q for q in fi if not hasq[q] and s0[q] == 0]
    f2 = [q for q in fi if not hasq[q] and s0[q] > 0]
    assert not f2
    if f1:
        t = cp.Variable(len(f1))
        sg = sig[f1]
        cons.append(cp.SOC(sg + t, cp.vstack([kap[f1], sg - t]), axis=0))   # kap^2 <= 4 sig t
        terms.append(-cp.sum(t))
    if f0:
        cons.append(kap[f0] == 0)
    prob = cp.Problem(cp.Maximize(const + cp.sum(cp.hstack(terms))), cons)
    prob.solve(solver=solver, verbose=verbose, **kw)
    raw = []
    ie = iu = il = 0
    for r, e, hu, hl in zip(rows, iseq, hasub, haslb):
        if e:
            raw.append(("eq", float(me.value[ie]))); ie += 1
        else:
            a = b = None
            if hu:
                a = float(mu.value[iu]); iu += 1
            if hl:
                b = float(ml.value[il]); il += 1
            raw.append(("ineq", a, b))
    solve_dual_vec.W = cons[0].dual_value
    return prob.value, prob.status, raw
