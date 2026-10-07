"""Own Shor-SDP solve + exact Lagrangian certificate for the 0039r children of the
first branching step (angle of W_{1,29} split at w_I = 0), in the authors' bus
indexing for the rectangular model (bus k = k-th voltage-row variable pair,
pairs sorted by variable index; x_{2k}, x_{2k+1} = the pair).

The two children {g <= 0} and {g >= 0}, g = x_{b1} x_{a29} - x_{a1} x_{b29},
cover every point, so min(L_child1, L_child2) is a valid bound for the whole
problem.  Multipliers come from cvxpy/Clarabel (primal Shor SDP); the bound is
evaluated exactly by pfv.lagrangian and PSD is proved by exact LDL^T.

    python3 sdp_node.py powerflow0039r [root|kids]
"""
import sys
import time
from fractions import Fraction as Fr

import cvxpy as cp
import numpy as np
import scipy.sparse as sp

import pfv

SOLVER_KW = {}


def solve(M, extra_rows=()):
    rows = list(M["rows"]) + list(extra_rows)
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
                Bi.append(t); Bj.append(i * n2 + j); Bv.append(float(c))
            for y, c in r["lin"].items():
                Li.append(t); Lj.append(yi[y]); Lv.append(float(c))
            for y, c in r["qy"].items():
                Qi.append(t); Qj.append(yi[y]); Qv.append(float(c))
        m = len(idx)
        return (sp.csr_matrix((Bv, (Bi, Bj)), shape=(m, n2 * n2)),
                sp.csr_matrix((Lv, (Li, Lj)), shape=(m, ny)),
                sp.csr_matrix((Qv, (Qi, Qj)), shape=(m, ny)))

    pat = [pfv.pattern(r) for r in rows]
    ie = [k for k, p in enumerate(pat) if p[0] == "eq"]
    iu = [k for k, p in enumerate(pat) if p[0] == "ineq" and p[1]]
    il = [k for k, p in enumerate(pat) if p[0] == "ineq" and p[2]]
    cons = [W >> 0]
    Be, Le, Qe = mats(ie)
    assert Qe.nnz == 0
    ce = Be @ vw + Le @ z == np.array([float(rows[k]["lb"]) for k in ie])
    Bu, Lu, Qu = mats(iu)
    assert (Qu.data >= 0).all()
    cu = Bu @ vw + Lu @ z + Qu @ cp.square(z) <= np.array([float(rows[k]["ub"]) for k in iu])
    Bl, Ll, Ql = mats(il)
    assert Ql.nnz == 0
    cl = Bl @ vw + Ll @ z >= np.array([float(rows[k]["lb"]) for k in il])
    cons += [ce, cu, cl]
    for y, (lo, hi) in M["box"].items():
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
    prob.solve(solver="CLARABEL", chordal_decomposition_enable=False, **SOLVER_KW)
    print(f"  SDP primal value {prob.value!r} ({prob.status}), {time.time()-t:.0f}s")
    de, du, dl = ce.dual_value, cu.dual_value, cl.dual_value
    raws = []
    for sgn in (1.0, -1.0):
        raw = [None] * len(rows)
        for t_, k in enumerate(ie):
            raw[k] = ["eq", sgn * float(de[t_])]
        up = {k: float(du[t_]) for t_, k in enumerate(iu)}
        lo = {k: float(dl[t_]) for t_, k in enumerate(il)}
        for k, p in enumerate(pat):
            if p[0] == "ineq":
                raw[k] = ["ineq", up.get(k) if p[1] else None, lo.get(k) if p[2] else None]
        raws.append(raw)
    return rows, raws, prob.value


def certify(M, rows, raw):
    MM = dict(M, rows=rows)
    res = pfv.lagrangian(MM, raw, log=lambda s: print(s))
    A = np.array([[float(v) for v in r] for r in res["A"]])
    lmin = np.linalg.eigvalsh(A)[0]
    print(f"  float min eig A(w) = {lmin:.3e}")
    eps = 0.0
    for attempt in range(6):
        if attempt:
            # shift: add eps to the upper-side multiplier of one volt row per bus -> A += eps I
            eps = max(2 * abs(lmin), 1e-9) * 10 ** (attempt - 1)
            raw2 = [list(x) for x in raw]
            seen = set()
            for k, r in enumerate(rows):
                if r["kind"] == "volt" and r["ub"] is not None:
                    bus = frozenset(i for (i, j) in r["Q"])
                    if bus not in seen:
                        seen.add(bus)
                        raw2[k][1] = (raw2[k][1] or 0.0) + eps
            assert set().union(*seen) == set(range(2 * M["n"]))
            res = pfv.lagrangian(MM, raw2, log=lambda s: None)
        ok, piv, zeros = pfv.ldl_psd(res["A"])
        if ok:
            L = res["const"] + res["inner"]
            print(f"  exact LDL^T psd (pivots {len(piv)}, zero {zeros}); shift eps {eps:g}; L = {float(L)!r}")
            return L
    return None


if __name__ == "__main__":
    name = sys.argv[1]
    mode = sys.argv[2]
    if len(sys.argv) > 3:
        t_ = float(sys.argv[3])
        SOLVER_KW.update(tol_gap_abs=t_, tol_gap_rel=t_, tol_feas=t_, tol_ktratio=t_, max_iter=500)
        print("Clarabel tolerances", SOLVER_KW)
    M = pfv.build(name)
    if mode == "root":
        rows, raws, val = solve(M)
        L = certify(M, rows, raws[0])
        print("  root: rigorous bound", repr(float(L)) if L is not None else None)
        sys.exit(0)
    assert not M["polar"]
    X = M["vmap"]["X"]
    xi = {j: q for q, j in enumerate(X)}
    # authors' bus pairs: voltage-row variable pairs sorted by index
    pairs = sorted({tuple(sorted(i for (i, j) in r["Q"])) for r in M["rows"] if r["kind"] == "volt"})
    pairs = [tuple(X[i] for i in p) for p in pairs]
    print("bus 1 pair", [M["I"]["names"][j] for j in pairs[1]], "bus 29 pair", [M["I"]["names"][j] for j in pairs[29]])
    (a1, b1), (a29, b29) = pairs[1], pairs[29]

    def g_row(sign, nm):
        Q = {}
        for (i, j), c in (((xi[b1], xi[a29]), Fr(sign)), ((xi[a1], xi[b29]), Fr(-sign))):
            Q[tuple(sorted((i, j)))] = c
        return dict(name=nm, kind="branch", lin={}, qy={}, Q=Q, lb=None, ub=Fr(0))

    todo = [("root", [])] if mode == "root" else [("child w_I<=0", [g_row(1, "wI<=0")]), ("child w_I>=0", [g_row(-1, "wI>=0")])]
    out = []
    for label, extra in todo:
        print("==", label)
        rows, raws, val = solve(M, extra)
        best = None
        for sgn, raw in zip((1, -1), raws):
            print(f" eq-dual sign {sgn:+d}")
            try:
                L = certify(M, rows, raw)
            except AssertionError as e:
                print("  certificate failed:", repr(e)[:200])
                L = None
            if L is not None and (best is None or L > best):
                best = L
        print(f"  {label}: rigorous bound {float(best)!r}" if best is not None else f"  {label}: no bound")
        out.append(best)
    if mode != "root" and all(b is not None for b in out):
        m = min(out)
        print("min over the two children:", repr(float(m)), "| claimed 41867.77921432582; difference", float(m) - 41867.77921432582)
