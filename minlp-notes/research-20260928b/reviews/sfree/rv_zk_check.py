"""Independent checks of z_K (Theorem 11 / core.corner_bound) and of the inertia bound (Theorem 4).

my_supp2: exact single-ray values + two-ray values by a dense direction scan (20001 angles) with
          local refinement -- reviewer's own code, no closed forms from the note.
scip:     global solve of min w^T lam s.t. q(sbar + P lam) <= 0, lam >= 0 (PySCIPOpt, SCIP 10).
core:     the note's corner_bound (imported only to compare).

Families (k = 3 unless stated):
  bil     : bilinear q = w - x y (rho = 2), random reals, N in {3,4,6}
  bilint  : bilinear, small-integer/half-integer data (degenerate ties, tangencies)
  sig12   : Q = V diag(1,-1,-1) V^T, random b, c  (n+ = 1, n0 = 0 -> rho = 2 < k = 3)
  ker_out : Q = diag(1,-1,0) rotated, b with a kernel component (rho = 2)
  sig21   : Q = V diag(1,1,-1) V^T  (rho = 3): POSITIVE CONTROL, 3-ray minimizers expected
For rho = 2 families, Theorem 4 predicts scip == my_supp2 (up to tolerance).
"""
import sys, itertools, time
import numpy as np
from scipy.optimize import minimize_scalar
import pyscipopt as ps

sys.path.insert(0, '../../sfree/code')
import core  # only for comparison

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
NPER = int(sys.argv[2]) if len(sys.argv) > 2 else 20


def qv(Q, b, c, s):
    return s @ Q @ s + b @ s + c


def first_hit(Q, b, c, sbar, d):
    A = d @ Q @ d; B = 2 * d @ Q @ sbar + b @ d; C = qv(Q, b, c, sbar)
    if abs(A) < 1e-14 * max(1, abs(B), C):
        return -C / B if B < 0 else np.inf
    D = B * B - 4 * A * C
    if D < 0:
        return np.inf
    r = np.sqrt(D)
    roots = sorted([(-B - r) / (2 * A), (-B + r) / (2 * A)])
    pos = [t for t in roots if t > 0]
    if not pos:
        return np.inf
    return pos[0] if A > 0 else (roots[1] if roots[1] > 0 else np.inf)


def my_supp2(Q, b, c, sbar, P, w):
    N = P.shape[1]
    best = min(w[j] * first_hit(Q, b, c, sbar, P[:, j]) for j in range(N))
    for i, j in itertools.combinations(range(N), 2):
        f = lambda th: first_hit(Q, b, c, sbar, th / w[i] * P[:, i] + (1 - th) / w[j] * P[:, j])
        ths = np.linspace(0, 1, 20001)
        vals = np.array([f(t) for t in ths])
        k = int(np.argmin(vals))
        v = vals[k]
        if np.isfinite(v):
            lo, hi = ths[max(0, k - 1)], ths[min(len(ths) - 1, k + 1)]
            r = minimize_scalar(f, bounds=(lo, hi), method='bounded', options=dict(xatol=1e-14))
            v = min(v, r.fun)
        best = min(best, v)
    return best


def scip(Q, b, c, sbar, P, w, ub):
    k, N = P.shape
    m = ps.Model(); m.hideOutput()
    m.setParam('limits/time', 20); m.setParam('limits/gap', 1e-9); m.setParam('numerics/feastol', 1e-9)
    U = (ub if np.isfinite(ub) else 1e3)
    lam = [m.addVar(lb=0, ub=U / w[j] * 1.01 + 1e-6) for j in range(N)]
    s = [sbar[i] + ps.quicksum(P[i, j] * lam[j] for j in range(N)) for i in range(k)]
    expr = ps.quicksum(Q[i, l] * s[i] * s[l] for i in range(k) for l in range(k)) + ps.quicksum(b[i] * s[i] for i in range(k)) + c
    m.addCons(expr <= 0)
    m.setObjective(ps.quicksum(w[j] * lam[j] for j in range(N)), 'minimize')
    m.optimize()
    if m.getStatus() == 'infeasible':
        return np.inf, None
    sol = m.getBestSol()
    return m.getDualbound(), np.array([m.getSolVal(sol, l) for l in lam]) if m.getNSols() else None


def rot3():
    A = rng.standard_normal((3, 3)); Qm, _ = np.linalg.qr(A); return Qm


def gen(fam):
    if fam in ('bil', 'bilint'):
        Q = np.zeros((3, 3)); Q[0, 1] = Q[1, 0] = -0.5; b = np.array([0, 0, 1.0]); c = 0.0
    elif fam == 'sig12':
        V = rot3(); Q = V @ np.diag(rng.uniform(.5, 2, 3) * np.array([1, -1, -1])) @ V.T; b = rng.standard_normal(3); c = rng.standard_normal()
    elif fam == 'sig21':
        V = rot3(); Q = V @ np.diag(rng.uniform(.5, 2, 3) * np.array([1, 1, -1])) @ V.T; b = rng.standard_normal(3); c = rng.standard_normal()
    elif fam == 'ker_out':
        V = rot3(); Q = V @ np.diag([rng.uniform(.5, 2), -rng.uniform(.5, 2), 0]) @ V.T
        b = rng.standard_normal(3); c = rng.standard_normal()
    N = int(rng.choice([3, 4, 6]))
    if fam == 'bilint':
        P = rng.integers(-4, 5, (3, N)).astype(float) / 2; w = rng.integers(1, 4, N).astype(float)
        sbar = rng.integers(-4, 5, 3).astype(float) / 2
    else:
        P = rng.standard_normal((3, N)); w = rng.uniform(.2, 2, N); sbar = rng.standard_normal(3)
    return Q, b, c, sbar, P, w


def main():
    fams = sys.argv[3].split(',') if len(sys.argv) > 3 else ['bil', 'bilint', 'sig12', 'ker_out', 'sig21']
    for fam in fams:
        n = 0; worst_core = 0; n_sup3 = 0; worst_T4 = 0; skipped = 0
        t0 = time.time()
        while n < NPER:
            Q, b, c, sbar, P, w = gen(fam)
            if qv(Q, b, c, sbar) <= 1e-3 or np.linalg.matrix_rank(P) < 3 and fam != 'bilint':
                continue
            m2 = my_supp2(Q, b, c, sbar, P, w)
            if not np.isfinite(m2) and fam != 'sig21':
                skipped += 1
                if skipped > 200:
                    break
                continue
            sc, lam = scip(Q, b, c, sbar, P, w, m2 if np.isfinite(m2) else np.inf)
            try:
                cb = core.corner_bound(Q, b, c, sbar, P, w)
            except Exception as e:
                cb = np.nan
            n += 1
            ref = sc
            rel_core = abs(cb - m2) / max(1e-9, abs(m2)) if np.isfinite(m2) and np.isfinite(cb) else (0 if cb == m2 else np.inf)
            rel_T4 = (m2 - sc) / max(1e-9, abs(sc)) if np.isfinite(m2) else np.inf
            if fam in ('bil', 'bilint', 'sig12', 'ker_out'):
                worst_core = max(worst_core, rel_core)
            worst_T4 = max(worst_T4, rel_T4)
            if rel_T4 > 1e-5:
                n_sup3 += 1
                print('   %s: supp<=2 value %.8f  SCIP %.8f  core %.8f  lam_scip %s' % (fam, m2, sc, cb, np.round(lam, 5) if lam is not None else None))
        print('%-8s n=%d  max rel |core - my_supp2| = %.2e ;  #(SCIP < supp<=2 by >1e-5) = %d ; max rel gap = %.3e  (%.0fs)'
              % (fam, n, worst_core, n_sup3, worst_T4, time.time() - t0), flush=True)


if __name__ == '__main__':
    main()
