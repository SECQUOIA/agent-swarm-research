"""Full binary-vertex envelope LPs for the dyadic construction at L=2,3.

Independent 2026-09-25 reproduction of the unarchived review-time check in
notes/review-positive-multilinear.md ("Supplementary exact finite checks") for
results/positive-multilinear-gap.md. It was written from the review's
description; the reviewer's original code and vectors are not available.

For consecutive dyadic partitions, the script enumerates every binary vertex
and solves with Gurobi the distribution LPs
    min / max  sum_v pi_v f(v)   s.t.  sum_v pi_v = 1,  sum_v pi_v v = x,
    pi >= 0,
whose values are the convex and concave envelopes at x (a_j = 2^-j,
z_i = 1 - 1/m). From Gurobi's optimal basis it rebuilds an exact rational
primal distribution and dual vector with fractions.Fraction and checks
every mean equation, primal nonnegativity, every dual inequality at every
vertex, and equality of the primal and dual values. It also checks, at every
vertex, the defect identity sum_{B in P_j} A_j prod_B Z = A_j (2^j - N_j) and
N_j <= min(2^j, R), and computes the termwise gap from the exact
single-monomial envelope formulas.
"""
import itertools
from fractions import Fraction as F

import gurobipy as gp
import numpy as np
from gurobipy import GRB

REPORTED = {2: (F(1, 2), F(2), F(3, 2), F(4, 3)),   # review table: conv, cav,
            3: (F(1), F(3), F(2), F(3, 2))}          # hull gap, gap ratio


def construction(L):
    m = 2 ** L
    n = L + m                                   # a_1..a_L, then z_1..z_m
    blocks = [[range(b * 2 ** (L - j), (b + 1) * 2 ** (L - j))
               for b in range(2 ** j)] for j in range(1, L + 1)]
    monomials = [[j - 1] + [L + i for i in B]
                 for j in range(1, L + 1) for B in blocks[j - 1]]
    x = [F(1, 2 ** j) for j in range(1, L + 1)] + [1 - F(1, m)] * m
    return n, m, blocks, monomials, x


def solve_exact(M, rhs):
    """Solve the square system M y = rhs over the rationals."""
    k = len(M)
    A = [list(row) + [r] for row, r in zip(M, rhs)]
    for c in range(k):
        p = next(r for r in range(c, k) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        A[c] = [v / A[c][c] for v in A[c]]
        for r in range(k):
            if r != c and A[r][c] != 0:
                A[r] = [a - A[r][c] * b for a, b in zip(A[r], A[c])]
    return [A[r][k] for r in range(k)]


def certified_envelope(verts, fvals, x, sense):
    n = len(x)
    rows = lambda v: [1] + list(v)              # constraint column of vertex v
    b = [F(1)] + x
    model = gp.Model()
    model.Params.OutputFlag = 0
    model.Params.Threads = 4
    model.Params.Method = 0
    pi = model.addMVar(len(verts), lb=0)
    A = np.array([rows(v) for v in verts], dtype=float).T
    model.addConstr(A @ pi == np.array([float(t) for t in b]))
    model.setObjective(np.array([float(t) for t in fvals]) @ pi,
                       GRB.MINIMIZE if sense == 'min' else GRB.MAXIMIZE)
    model.optimize()
    assert model.Status == GRB.OPTIMAL
    vb = model.getAttr('VBasis', model.getVars())
    cb = model.getAttr('CBasis', model.getConstrs())
    # Basis columns: basic vertex columns plus unit columns for basic slacks.
    cols = [('v', i) for i, s in enumerate(vb) if s == 0]
    cols += [('s', r) for r, s in enumerate(cb) if s == 0]
    assert len(cols) == n + 1
    colvec = lambda c: (rows(verts[c[1]]) if c[0] == 'v'
                        else [int(r == c[1]) for r in range(n + 1)])
    B = [[F(colvec(c)[r]) for c in cols] for r in range(n + 1)]
    z = solve_exact(B, b)
    cB = [fvals[c[1]] if c[0] == 'v' else F(0) for c in cols]
    y = solve_exact([list(col) for col in zip(*B)], cB)
    primal = {c[1]: val for c, val in zip(cols, z) if c[0] == 'v'}
    assert all(val == 0 for c, val in zip(cols, z) if c[0] == 's')
    # Exact certificate checks.
    assert all(w >= 0 for w in primal.values())
    for r in range(n + 1):
        assert sum(w * rows(verts[i])[r] for i, w in primal.items()) == b[r]
    pval = sum(w * fvals[i] for i, w in primal.items())
    dval = sum(yi * bi for yi, bi in zip(y, b))
    for v, fv in zip(verts, fvals):
        lhs = sum(yi * ri for yi, ri in zip(y, rows(v)))
        assert (lhs <= fv) if sense == 'min' else (lhs >= fv)
    assert pval == dval
    assert abs(float(pval) - model.ObjVal) < 1e-7
    return pval, len([w for w in primal.values() if w > 0])


def check(L):
    n, m, blocks, monomials, x = construction(L)
    verts = list(itertools.product((0, 1), repeat=n))
    fvals = [F(sum(all(v[i] for i in mon) for mon in monomials)) for v in verts]
    # Defect identity and N_j bounds at every vertex.
    for v in verts:
        R = m - sum(v[L:])
        for j in range(1, L + 1):
            hit = sum(any(v[L + i] == 0 for i in B) for B in blocks[j - 1])
            level = sum(v[j - 1] * all(v[L + i] for i in B)
                        for B in blocks[j - 1])
            assert level == v[j - 1] * (2 ** j - hit)
            assert hit <= min(2 ** j, R)
    conv, conv_support = certified_envelope(verts, fvals, x, 'min')
    cav, cav_support = certified_envelope(verts, fvals, x, 'max')
    gap = cav - conv
    # Termwise gap from exact monomial envelopes min x_i - max(0, sum x_i - (k-1)).
    tbt = sum(min(x[i] for i in mon) - max(F(0), sum(x[i] for i in mon)
                                            - (len(mon) - 1))
              for mon in monomials)
    ratio = tbt / gap
    print(f'L={L} variables={n} vertices={len(verts)} monomials={len(monomials)}'
          f' conv={conv} cav={cav} hull_gap={gap} tbt_gap={tbt} ratio={ratio}'
          f' (primal supports: conv {conv_support}, cav {cav_support})')
    ok = (conv, cav, gap, ratio) == REPORTED[L]
    print(f'  matches review table: {ok}')
    return ok


if __name__ == '__main__':
    results = [check(L) for L in (2, 3)]
    print('ALL CHECKS PASSED' if all(results) else 'MISMATCH WITH REVIEW TABLE')
