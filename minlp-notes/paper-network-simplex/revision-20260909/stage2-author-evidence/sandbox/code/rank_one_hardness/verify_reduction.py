"""
Computational sanity check of the reductions
  maximum edge biclique  ->  min <C,W> over U^row ∩ U^col   (strong NP-hardness)
  PARTITION              ->  min <C,W> over U^row ∩ U^col   (alternative, weak)

U^row ∩ U^col = { W >= 0, rank(W) <= 1, l <= rowsums(W) <= u, l' <= colsums(W) <= u' }.
Every nonzero W in this set is W = r c^T / S with r = rowsums, c = colsums, S = sum r = sum c,
and <C,W> = r^T C c / S.  Since S >= 1 in all instances built here (fixed row with l_0 = u_0 = 1),
the sign of min <C,W> equals the sign of  min r^T C c  over r in [l,u], c in [l',u'], sum r = sum c,
which is the bilinear program solved below (globally, Gurobi NonConvex=2).  The printed value is
this bilinear optimum (numerator), not the value of <C,W>.
"""
import itertools, random, sys
import numpy as np
import gurobipy as gp
from gurobipy import GRB


def solve_rank_one_lp(C, l, u, lp, up, verbose=False):
    """Sign-exact surrogate: min r^T C c over r in [l,u], c in [lp,up], sum r = sum c.
    Every nonzero W in U^row ∩ U^col is r c^T / S with S = sum r > 0 and <C,W> = r^T C c / S,
    so min <C,W> <= 0 iff this bilinear program has value <= 0. Returns the bilinear optimum."""
    n1, n2 = C.shape
    m = gp.Model()
    m.Params.OutputFlag = 1 if verbose else 0
    m.Params.NonConvex = 2
    m.Params.MIPGapAbs = 1e-4
    m.Params.TimeLimit = 60
    r = m.addVars(n1, lb=l, ub=u, name="r")
    c = m.addVars(n2, lb=lp, ub=up, name="c")
    m.addConstr(gp.quicksum(r[i] for i in range(n1)) == gp.quicksum(c[j] for j in range(n2)))
    m.setObjective(gp.quicksum(float(C[i, j]) * r[i] * c[j] for i in range(n1) for j in range(n2) if C[i, j] != 0), GRB.MINIMIZE)
    m.optimize()
    if m.Status not in (GRB.OPTIMAL, GRB.TIME_LIMIT):
        return None
    if m.Status == GRB.TIME_LIMIT:
        print("   (time limit; abs gap %.2e)" % abs(m.ObjVal - m.ObjBound))
    return m.ObjVal


def max_edge_biclique(L, R, E):
    """brute force: max |A||B| over A⊆L, B⊆R with A×B ⊆ E."""
    best = 0
    for k in range(1, len(L) + 1):
        for A in itertools.combinations(L, k):
            B = [j for j in R if all((i, j) in E for i in A)]
            best = max(best, k * len(B))
    return best


def biclique_instance(L, R, E, k):
    """Build (C, l, u, lp, up) so that  min <C,W> <= 0  iff  a biclique with >= k edges exists."""
    nL, nR = len(L), len(R)
    n = max(nL, nR)
    M = n * n
    # index layout rows: 0 = fixed row, 1..nL = left vertices, nL+1..nL+n = dummy rows
    # cols: 0 = fixed col, 1..nR = right vertices, nR+1..nR+n = dummy cols
    n1 = 1 + nL + n
    n2 = 1 + nR + n
    C = np.zeros((n1, n2))
    C[0, 0] = k
    for a, i in enumerate(L):
        for b, j in enumerate(R):
            C[1 + a, 1 + b] = -1.0 if (i, j) in E else float(M)
    l = np.zeros(n1); u = np.ones(n1); l[0] = 1.0
    lp = np.zeros(n2); up = np.ones(n2); lp[0] = 1.0
    return C, l, u, lp, up


def partition_instance(a):
    """PARTITION numbers a -> (C, l, u, lp, up) with  min <C,W> <= 0  iff partition exists; min >= 0 always."""
    m = len(a); A = sum(a); mu = 1.0
    n = m + 1
    C = np.zeros((n, n))
    for i in range(1, n):
        for j in range(1, n):
            C[i, j] = mu - (1.0 if i == j else 0.0)
        C[i, 0] = a[i - 1]
        C[0, i] = -mu * A
    C[0, 0] = mu * A * A / 4.0
    l = np.zeros(n); u = np.zeros(n); l[0] = u[0] = 1.0
    for i in range(1, n):
        u[i] = a[i - 1]
    return C, l, u, l.copy(), u.copy()


def has_partition(a):
    A = sum(a)
    if A % 2: return False
    reach = {0}
    for x in a:
        reach |= {y + x for y in reach}
    return A // 2 in reach


if __name__ == "__main__":
    random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    print("=== biclique reduction ===")
    ok = True
    for trial in range(12):
        nL, nR = random.randint(2, 4), random.randint(2, 4)
        L = list(range(nL)); R = list(range(nR))
        E = {(i, j) for i in L for j in R if random.random() < 0.6}
        meb = max_edge_biclique(L, R, E)
        for k in sorted({max(1, meb - 1), meb, meb + 1}):
            C, l, u, lp, up = biclique_instance(L, R, E, k)
            val = solve_rank_one_lp(C, l, u, lp, up)
            claim = (meb >= k)
            got = (val is not None and val <= 1e-3)
            flag = "OK " if claim == got else "MISMATCH"
            if claim != got: ok = False
            print(f"{flag} |L|={nL} |R|={nR} |E|={len(E)} meb={meb} k={k} min r^T C c={val:.6f}")
    print("=== partition reduction ===")
    for trial in range(10):
        a = [random.randint(1, 9) for _ in range(random.randint(3, 5))]
        C, l, u, lp, up = partition_instance(a)
        val = solve_rank_one_lp(C, l, u, lp, up)
        claim = has_partition(a)
        got = (val is not None and val <= 1e-3)
        flag = "OK " if claim == got else "MISMATCH"
        if claim != got: ok = False
        print(f"{flag} a={a} partition={claim} min r^T C c={val:.6f}")
    print("ALL OK" if ok else "SOME MISMATCH")
