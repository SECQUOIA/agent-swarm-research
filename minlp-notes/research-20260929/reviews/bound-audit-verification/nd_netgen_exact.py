"""Exact rational repair of nd_netgen-2000-3-4-b-a-ns_7 point p2 (own method).

Model (read from the OSIL file, checked below):
  min sum cb*b + sum cf*f + sum u
  f <= cap*b                                  (L rows, 2 entries)
  flow conservation                           (E rows, many entries, integer data)
  s = 0.5*(u - b), t = 0.5*(u + b)            (E rows, 3 entries)
  c*f^2 + s^2 - t^2 <= 0   (i.e. c f^2 <= u b) (L rows, quadratic)
  b binary, 0 <= f <= cap, u >= 0, s, t free.

Repair: keep b; fix flows on closed arcs at 0; correct the flows of a set of
open arcs strictly inside (0, cap) so that conservation holds exactly (exact
Fraction Gauss-Jordan on a nonsingular 74x74 submatrix chosen by numeric QR);
set u = c f^2 on open arcs (the least feasible value) and u = 0 on closed arcs
(variant A), or u = max(u_listed, c f^2) (variant B); set s, t from their rows.
Then every row, bound and integrality condition is checked in exact arithmetic
by the generic evaluator, and the objective is computed exactly.
"""
import os
import sys
from fractions import Fraction as F

import numpy as np
import scipy.linalg as sla

import evalpt
import osil

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = "nd_netgen-2000-3-4-b-a-ns_7"


def main(pk="p2"):
    M = evalpt.model(NAME)
    x0, missing, _ = osil.read_sol(os.path.join(HERE, "data", f"{NAME}.{pk}.sol"), M)
    x = list(x0)
    B = [j for j in range(M.n) if M.vtype[j] == "B"]
    assert all(x[j] in (0, 1) for j in B)
    # classify rows
    cap_rows, cons_rows, def_rows, cone_rows = [], [], [], []
    for i in range(M.m):
        eq = M.clb[i] is not None and M.clb[i] == M.cub[i]
        if M.quad[i]:
            assert not M.lin[i] and M.nl[i] is None and M.clb[i] is None and M.cub[i] == 0
            cone_rows.append(i)
        elif not eq:
            assert M.clb[i] is None and M.cub[i] == 0 and len(M.lin[i]) == 2
            cap_rows.append(i)
        elif len(M.lin[i]) == 3 and any(M.vtype[j] == "B" for j in M.lin[i]):
            def_rows.append(i)
        else:
            assert all(M.vtype[j] == "C" for j in M.lin[i]) and M.cconst[i] == 0
            cons_rows.append(i)
    print(f"rows: cap {len(cap_rows)}, conservation {len(cons_rows)}, s/t definitions {len(def_rows)}, cone {len(cone_rows)}")
    # arc structure from cap rows: f - cap*b <= 0
    arc = {}  # f index -> (b index, cap)
    for i in cap_rows:
        (j1, c1), (j2, c2) = M.lin[i].items()
        if M.vtype[j1] == "B":
            j1, c1, j2, c2 = j2, c2, j1, c1
        assert c1 == 1 and c2 < 0 and M.vtype[j2] == "B"
        arc[j1] = (j2, -c2)
    flows = sorted(arc)
    fset = set(flows)
    for i in cons_rows:
        assert set(M.lin[i]) <= fset and all(abs(c) == 1 for c in M.lin[i].values())
    # closed arcs: listed flow must be 0 already (check), set exactly 0
    closed = [j for j in flows if x[arc[j][0]] == 0]
    print("closed arcs:", len(closed), " with nonzero listed flow:", sum(1 for j in closed if x[j] != 0))
    for j in closed:
        x[j] = F(0)
    # interior open arcs
    inter = [j for j in flows if x[arc[j][0]] == 1 and 0 < x[j] < min(arc[j][1], M.ub[j] if M.ub[j] is not None else arc[j][1])]
    print("open arcs strictly inside bounds:", len(inter))
    res0 = [M.cub[i] - osil.row_exact(M, i, x) for i in cons_rows]
    print("max |conservation residual| before:", float(max(abs(r) for r in res0)))
    A = np.array([[float(M.lin[i].get(j, 0)) for j in inter] for i in cons_rows])
    Q, R, piv = sla.qr(A, pivoting=True, mode="economic")
    m = len(cons_rows)
    rank = int(np.sum(np.abs(np.diag(R)) > 1e-9))
    print("rank of conservation rows on interior arcs:", rank, "of", m)
    basis = [inter[p] for p in piv[:rank]]
    # exact Gauss-Jordan on rows x basis (use only the first `rank` independent rows)
    rows_used = list(range(m))
    Ab = [[F(M.lin[cons_rows[r]].get(j, 0)) for j in basis] + [res0[r]] for r in rows_used]
    # eliminate
    piv_rows = []
    rr = 0
    for c in range(len(basis)):
        p = next((k for k in range(rr, len(Ab)) if Ab[k][c] != 0), None)
        assert p is not None, "singular"
        Ab[rr], Ab[p] = Ab[p], Ab[rr]
        pv = Ab[rr][c]
        Ab[rr] = [v / pv for v in Ab[rr]]
        for k in range(len(Ab)):
            if k != rr and Ab[k][c] != 0:
                fct = Ab[k][c]
                Ab[k] = [a - fct * b for a, b in zip(Ab[k], Ab[rr])]
        rr += 1
    # remaining rows (if rank < m) must be consistent: 0 = rhs
    for k in range(rr, len(Ab)):
        assert all(v == 0 for v in Ab[k][:-1])
        assert Ab[k][-1] == 0, "inconsistent dependent row"
    delta = {basis[c]: Ab[c][-1] for c in range(len(basis))}
    for j, d in delta.items():
        x[j] = x[j] + d
    print("max |flow change|:", float(max(abs(d) for d in delta.values())))
    for i in cons_rows:
        assert osil.row_exact(M, i, x) == M.cub[i]
    # u, s, t
    cone_of = {}
    for i in cone_rows:
        q = {(a, b): c for a, b, c in M.quad[i]}
        diag = [(a, c) for (a, b), c in q.items() if a == b]
        assert len(diag) == 3
        fj = [a for a, c in diag if a in fset]
        assert len(fj) == 1
        fj = fj[0]
        cone_of[fj] = (i, q[(fj, fj)], [a for a, c in diag if c == 1][0], [a for a, c in diag if c == -1][0])
    uvars = {fj: cone_of[fj] + (arc[fj][0],) for fj in flows}
    # build lookups for definition rows once (faster)
    by_var = {}
    for i in def_rows:
        for j in M.lin[i]:
            if M.vtype[j] == "C" and M.lb[j] is None:
                by_var[j] = i
    out = {}
    for variant in ("A", "B"):
        y = list(x)
        for fj in flows:
            ci, cc, sj, tj, bj = uvars[fj]
            i_s, i_t = by_var[sj], by_var[tj]
            uj = [j for j in M.lin[i_s] if j not in (sj, bj)]
            assert len(uj) == 1
            uj = uj[0]
            need = cc * y[fj] ** 2 if y[bj] == 1 else F(0)
            y[uj] = need if variant == "A" else max(x0[uj], need)
            for i, j in ((i_s, sj), (i_t, tj)):
                # row: const + sum lin = rhs, solve for variable j
                rest = M.cconst[i] + sum(c * y[k] for k, c in M.lin[i].items() if k != j)
                y[j] = (M.cub[i] - rest) / M.lin[i][j]
        vi = evalpt.violations(M, y)
        worst = max(vi, key=lambda t: t[0])
        obj = osil.obj_exact(M, y)
        print(f"variant {variant}: max violation (exact) = {worst[0]} at {worst[1:]}; objective = {obj} ~ {float(obj)!r}")
        out[variant] = obj
    return out


if __name__ == "__main__":
    out = main(*(sys.argv[1:] or []))
    for d, nm in ((F("10729659.03"), "CPLEX"), (F("10729661.15"), "GUROBI")):
        for v, o in out.items():
            print(f"{nm} {float(d)} - objective({v}) = {float(d - o):.6f}  rel {float((d - o) / d):.3e}")
