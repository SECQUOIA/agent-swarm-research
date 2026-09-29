"""Independent numerical checks of Lemma 1.5 (midpoint formula, (a), (b)),
the conflict inequality derived from (b), and Lemma 4.2.

g(z) is computed on the n-side, g(z) = y' (I + X diag(z) X'/lam)^{-1} y,
which is NOT the formula used by the author's code (p-side ridge solve).
The midpoint formula is evaluated by an explicit weighted-ridge solve.
"""
import numpy as np

rng = np.random.default_rng(20260929)


def g_nside(X, y, lam, z):
    n = X.shape[0]
    M = np.eye(n) + (X * z) @ X.T / lam
    return float(y @ np.linalg.solve(M, y))


def wridge(X, y, U, pen):
    """min_b ||y - X_U b||^2 + sum pen_i b_i^2 ; returns value and b."""
    XU = X[:, U]
    b = np.linalg.solve(XU.T @ XU + np.diag(pen), XU.T @ y)
    r = y - XU @ b
    return float(r @ r + np.sum(pen * b * b)), b


worst = dict(formula=0.0, a_viol=-np.inf, a_eq=0.0, b_viol=-np.inf, cf_mismatch=0,
             l42_viol=-np.inf, segment_viol=-np.inf)
ntr = 0
for trial in range(400):
    n = int(rng.integers(5, 60))
    p = int(rng.integers(6, 50))
    k = int(rng.integers(1, min(p // 2, 8) + 1))
    lam = float(10 ** rng.uniform(-2, 2))
    X = rng.standard_normal((n, p))
    y = rng.standard_normal(n) * rng.uniform(0.1, 3)
    if rng.random() < 0.5:  # planted signal sometimes
        Sst = rng.choice(p, k, replace=False)
        y = y + X[:, Sst] @ rng.standard_normal(k)
    S = sorted(rng.choice(p, k, replace=False).tolist())
    # T with a random overlap (sometimes disjoint, sometimes equal-size overlap)
    if rng.random() < 0.3:
        rest = [j for j in range(p) if j not in S]
        T = sorted(rng.choice(rest, min(k, len(rest)), replace=False).tolist())
    else:
        T = sorted(rng.choice(p, k, replace=False).tolist())
    if S == T:
        continue
    ntr += 1
    z = np.zeros(p); z[S] += 0.5; z[T] += 0.5
    gm = g_nside(X, y, lam, z)
    U = sorted(set(S) | set(T)); C = set(S) & set(T)
    pen = np.array([lam if u in C else 2 * lam for u in U])
    val, _ = wridge(X, y, U, pen)
    worst['formula'] = max(worst['formula'], abs(gm - val) / gm)
    # (a)
    f2, _ = wridge(X, y, U, 2 * lam * np.ones(len(U)))
    worst['a_viol'] = max(worst['a_viol'], (gm - f2) / gm)
    if not C:
        worst['a_eq'] = max(worst['a_eq'], abs(gm - f2) / gm)
    # (b)
    fS, bS = wridge(X, y, S, lam * np.ones(len(S)))
    fT, bT = wridge(X, y, T, lam * np.ones(len(T)))
    bSf = np.zeros(p); bSf[S] = bS; bTf = np.zeros(p); bTf[T] = bT
    Cl = sorted(C)
    rhs = (fS + fT) / 2 - np.sum((X @ (bSf - bTf)) ** 2) / 4 - lam * np.sum((bSf[Cl] - bTf[Cl]) ** 2) / 4
    worst['b_viol'] = max(worst['b_viol'], (gm - rhs) / gm)
    # F1 consistency: g(1_S) = f(S)
    zS = np.zeros(p); zS[S] = 1
    assert abs(g_nside(X, y, lam, zS) - fS) <= 1e-9 * fS
    # conflict inequality equivalence with the (b) bound: for a threshold OPTt,
    # rhs < OPTt - eps  <=>  A > 2(fS-OPTt) + 2(fT-OPTt) + 4 eps
    OPTt = min(fS, fT) * rng.uniform(0.7, 1.0); eps = rng.uniform(0, 0.05) * OPTt
    A = np.sum((X @ (bSf - bTf)) ** 2) + lam * np.sum((bSf[Cl] - bTf[Cl]) ** 2)
    lhs1 = rhs < OPTt - eps
    lhs2 = A > 2 * (fS - OPTt) + 2 * (fT - OPTt) + 4 * eps
    if lhs1 != lhs2 and abs(rhs - (OPTt - eps)) > 1e-9 * OPTt:
        worst['cf_mismatch'] += 1
    # any point of the segment: g along the segment is convex, so max over segment <= max endpoint
    for t in (0.1, 0.3, 0.7, 0.9):
        zt = np.zeros(p); zt[S] += t; zt[T] += 1 - t
        worst['segment_viol'] = max(worst['segment_viol'], (g_nside(X, y, lam, zt) - max(fS, fT)) / gm)
    # Lemma 4.2 (deterministic inequality)
    yhat = y / np.linalg.norm(y)
    c = X.T @ yhat
    Xp = X - np.outer(yhat, c)
    sU = float(np.sum(c[U] ** 2))
    Q = float(np.sum((Xp[:, U] @ c[U]) ** 2))
    bnd = float(y @ y) * (1 - sU / (sU + Q / sU + 2 * lam))
    worst['l42_viol'] = max(worst['l42_viol'], (gm - bnd) / gm)

print("trials:", ntr)
print("Lemma 1.5 formula, max relative error (n-side g vs weighted ridge): %.2e" % worst['formula'])
print("Lemma 1.5(a) g(mid) - f_2lam(U), max relative (must be <= ~0): %.2e" % worst['a_viol'])
print("Lemma 1.5(a) equality when C empty, max relative error: %.2e" % worst['a_eq'])
print("Lemma 1.5(b) g(mid) - bound, max relative (must be <= ~0): %.2e" % worst['b_viol'])
print("conflict-inequality equivalence mismatches: %d" % worst['cf_mismatch'])
print("segment points: g - max(fS,fT), max relative (<= 0 by convexity): %.2e" % worst['segment_viol'])
print("Lemma 4.2 g(mid) - bound, max relative (must be <= ~0): %.2e" % worst['l42_viol'])
