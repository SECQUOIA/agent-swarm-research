"""Prop. 8 row condition and the many-term example, via exact OBBT (Clarabel)
on the tangent problem Q(d, xi) <= 0 (zero remainder, eps = 0)."""
import numpy as np, cvxpy as cp
rng = np.random.default_rng(1)

def Phi(H, dm, dp, c=0.0):
    n = len(dm); lo, hi = -np.asarray(dm, float), np.asarray(dp, float)
    x = cp.Variable(n); t = cp.Variable((n, n))
    cons = [x >= lo, x <= hi]; obj = cp.sum(cp.multiply(np.diag(H) / 2, cp.square(x)))
    for i in range(n):
        for j in range(i + 1, n):
            h = H[i, j]
            if h == 0: continue
            if h > 0:
                P = [(lo[j], lo[i], -lo[i]*lo[j]), (hi[j], hi[i], -hi[i]*hi[j])]
            else:
                P = [(hi[j], lo[i], -lo[i]*hi[j]), (lo[j], hi[i], -hi[i]*lo[j])]
            for (ci, cj, c0) in P:   # t_ij >= h * piece
                cons.append(t[i, j] >= h * (ci * x[i] + cj * x[j] + c0))
            obj = obj + t[i, j]
    cons.append(obj <= c)
    nlo, nhi = np.zeros(n), np.zeros(n)
    for i in range(n):
        p = cp.Problem(cp.Maximize(x[i]), cons); p.solve(solver=cp.CLARABEL, tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10)
        nhi[i] = x.value[i]
        p = cp.Problem(cp.Minimize(x[i]), cons); p.solve(solver=cp.CLARABEL, tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10)
        nlo[i] = x.value[i]
    return -nlo, nhi

def row_ok(H):
    A = np.abs(np.triu(H, 1)); tot = A.sum()
    offrow = np.abs(H - np.diag(np.diag(H))).sum(1)
    return np.diag(H) / 2 + offrow - tot   # < 0 for all k  <=> condition

print("many-term example (cube, eps=0): max extent of Phi(1)")
for n, a in [(3, 0.5), (5, 0.3), (6, 0.1), (7, 0.1), (10, 0.1)]:
    H = 2*np.eye(n) + a*(np.ones((n, n)) - np.eye(n))
    dm, dp = Phi(H, np.ones(n), np.ones(n))
    print(f"  n={n} a={a} a(n-1)(n-2)/2={a*(n-1)*(n-2)/2:.2f} row margin max={row_ok(H).max():+.3f}  Phi(1) in [{min(dm.min(),dp.min()):.6f},{max(dm.max(),dp.max()):.6f}]")

print("random H, cube: row condition holds -> expect Phi(1) = 1")
stats = {"hold_stall": 0, "hold_nostall": 0, "fail_stall": 0, "fail_nostall": 0}
for trial in range(60):
    n = rng.integers(3, 8)
    H = rng.normal(size=(n, n)); H = (H + H.T) / 2
    np.fill_diagonal(H, rng.uniform(0, 3, n))
    s = rng.uniform(0.3, 3.0); off = H - np.diag(np.diag(H)); H = np.diag(np.diag(H)) + s * off
    m = row_ok(H)
    dm, dp = Phi(H, np.ones(n), np.ones(n))
    stall = min(dm.min(), dp.min()) > 1 - 1e-6
    key = ("hold" if m.max() < 0 else "fail") + ("_stall" if stall else "_nostall")
    stats[key] += 1
    if m.max() < 0 and not stall:
        print("  COUNTEREXAMPLE", n, m, dm, dp)
print(" ", stats)

print("random H with half-widths h: condition on S H S -> expect Phi(h,h) = (h,h)")
bad = 0; tested = 0
for trial in range(40):
    n = rng.integers(3, 7)
    H = rng.normal(size=(n, n)); H = (H + H.T) / 2; np.fill_diagonal(H, rng.uniform(0, 2, n))
    h = rng.uniform(0.3, 2.0, n); S = np.diag(h)
    if row_ok(S @ H @ S).max() >= 0: continue
    tested += 1
    dm, dp = Phi(H, h, h)
    if max(np.abs(dm - h).max(), np.abs(dp - h).max()) > 1e-6 * h.max(): bad += 1
print(f"  tested {tested}, failures {bad}")
