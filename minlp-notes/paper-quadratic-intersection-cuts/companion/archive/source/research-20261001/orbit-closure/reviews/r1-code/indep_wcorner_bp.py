"""Reviewer's numerical check of Theorem 11(c) (BP at the W-corner): inf over S > 0 of a_1 + a_2 equals
(sqrt 2 - 1)/2, attained at S = I.  Imports no stream code.

Corner: sbar = (1, -1, 1), projected rays p_1 = e_x, p_2 = -e_y.  Member: X = F^T M(sbar) = S > 0.
Two independent ways to get a_j = 1/alpha_j:
  (k) kept-vector bound sup{ n_j(v)/d(v) : v kept, n_j(v) > 0 } over a fine angular grid with local
      refinement (Lemma 6(a); exact by sfree Lemma 10(4));
  (p) direct membership: s in B_F iff A(s) - tau Z is PSD for some tau >= 0 (sfree Section 8.1);
      alpha_j by bisection on mu, max over tau of the minimum eigenvalue (concave in tau).
Then a_1 + a_2 is minimized over the trace-one disk by Nelder-Mead from many starts, and the case
bounds of the proof are sampled in their regions.
"""
import numpy as np
from scipy.optimize import minimize, minimize_scalar

Ms = np.array([[1.0, 1.0], [-1.0, 1.0]])            # M(sbar) = [[w, x], [y, 1]]
Mi = np.linalg.inv(Ms)
M0 = [np.array([[0.0, 1.0], [0.0, 0.0]]), np.array([[0.0, 0.0], [-1.0, 0.0]])]   # e_x, -e_y
E = np.array([[1.0, 0.0], [0.0, 0.0]])
TH = np.linspace(0, np.pi, 20001)[:-1]
VV = np.stack([np.cos(TH), np.sin(TH)])


def S_of(u):
    return np.array([[(1 + u[0]) / 2, u[1] / 2], [u[1] / 2, (1 - u[0]) / 2]])


def a_kept(S, j):
    FT = S @ Mi
    Z = FT @ E; A0 = FT @ Ms; Aj = FT @ M0[j]
    kept = np.einsum('ik,ij,jk->k', VV, Z, VV)
    d = np.einsum('ik,ij,jk->k', VV, A0, VV)
    n = -np.einsum('ik,ij,jk->k', VV, Aj, VV)
    r = np.where((kept >= -1e-13) & (n > 0), n / d, 0.0)
    k = int(np.argmax(r))
    best = r[k]
    # local refinement around the grid maximiser (kept constraint may be active: stay on kept side)
    def f(th):
        v = np.array([np.cos(th), np.sin(th)])
        if v @ Z @ v < -1e-13 or -(v @ Aj @ v) <= 0:
            return 0.0
        return -(-(v @ Aj @ v)) / (v @ A0 @ v)
    res = minimize_scalar(f, bounds=(TH[k] - 2e-4, TH[k] + 2e-4), method='bounded', options=dict(xatol=1e-14))
    best = max(best, -res.fun)
    # near singular S the window of kept vectors with n_j > 0 shrinks below the grid spacing; add the
    # isotropic directions of Z (boundary of the kept set), among them J S m (Lemma 8)
    Zs = (Z + Z.T) / 2
    w_, U = np.linalg.eigh(Zs)
    if w_[0] < 0 < w_[1]:
        for sg in (1, -1):
            v = U[:, 0] * np.sqrt(w_[1]) + sg * U[:, 1] * np.sqrt(-w_[0])
            nn, dd = -(v @ Aj @ v), v @ A0 @ v
            if nn > 0 and dd > 0:
                best = max(best, nn / dd)
    return best


def in_B(S, s):
    FT = S @ Mi
    A = FT @ np.array([[s[2], s[0]], [s[1], 1.0]]); A = (A + A.T) / 2
    Z = FT @ E; Z = (Z + Z.T) / 2
    g = lambda t: -np.linalg.eigvalsh(A - t * Z)[0]
    r = minimize_scalar(g, bounds=(0, 1e4), method='bounded', options=dict(xatol=1e-12))
    return min(-g(0.0), -r.fun) if False else max(-g(0.0), -r.fun) >= -1e-12


def a_pencil(S, j):
    p = [np.array([1.0, 0, 0]), np.array([0, -1.0, 0])][j]
    sb = np.array([1.0, -1.0, 1.0])
    lo, hi = 0.0, 1.0
    while in_B(S, sb + hi * p):
        lo, hi = hi, 2 * hi
        if hi > 1e8:
            return 0.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if in_B(S, sb + mid * p):
            lo = mid
        else:
            hi = mid
    return 1 / lo


target = (np.sqrt(2) - 1) / 2
rng = np.random.default_rng(1)
print('S = I: a_1 = %.12f, a_2 = %.12f (kept), %.10f, %.10f (pencil); sum %.12f vs (sqrt2-1)/2 = %.12f'
      % (a_kept(S_of([0, 0]), 0), a_kept(S_of([0, 0]), 1), a_pencil(S_of([0, 0]), 0), a_pencil(S_of([0, 0]), 1),
         a_kept(S_of([0, 0]), 0) + a_kept(S_of([0, 0]), 1), target))

# agreement of the two computations
diffs = []
for _ in range(200):
    r, t = np.sqrt(rng.uniform(0, 0.99)), rng.uniform(0, 2 * np.pi)
    S = S_of([r * np.cos(t), r * np.sin(t)])
    for j in range(2):
        k, p = a_kept(S, j), a_pencil(S, j)
        diffs.append(abs(k - p) / max(1.0, abs(p)))   # pencil bisection is capped at mu = 1e8, so a_j = 0 shows as ~1e-5
print('kept-vector vs pencil a_j on 200 random S: max difference |k - p|/max(1, |p|) = %.2e' % max(diffs))


def obj(u):
    if u[0] ** 2 + u[1] ** 2 >= 0.999999:
        return 10.0
    S = S_of(u)
    return a_kept(S, 0) + a_kept(S, 1)


vals = []
for _ in range(40000):
    r, t = np.sqrt(rng.uniform(0, 0.9999)), rng.uniform(0, 2 * np.pi)
    vals.append((obj([r * np.cos(t), r * np.sin(t)]), r * np.cos(t), r * np.sin(t)))
vals.sort()
print('40000 random S: min a_1 + a_2 = %.9f at u = (%.4f, %.4f); target %.9f' % (vals[0][0], vals[0][1], vals[0][2], target))
best = None
for k in range(60):
    x0 = np.array(vals[k][1:]) if k < 20 else rng.uniform(-0.7, 0.7, 2)
    r = minimize(obj, x0, method='Nelder-Mead', options=dict(xatol=1e-10, fatol=1e-13, maxiter=3000))
    if best is None or r.fun < best.fun:
        best = r
print('Nelder-Mead (60 starts): min a_1 + a_2 = %.12f at u = %s; target %.12f; difference %.2e'
      % (best.fun, np.round(best.x, 6), target, best.fun - target))
# near the boundary circle, in particular near the point S ~ (1,-1)(1,-1)^T (u = (0, -1))
nb = []
for t in np.linspace(0, 2 * np.pi, 3601)[:-1]:
    for r in (0.99, 0.999, 0.99999):
        nb.append(obj([r * np.cos(t), r * np.sin(t)]))
print('near the boundary (r = 0.99, 0.999, 0.99999; 3600 angles): min a_1 + a_2 = %.6f' % min(nb))

# case bounds of the proof, normalised a = 1, b = -beta
cnt = {'iv': 0, 'v': 0}
worst = {'iv': np.inf, 'v': np.inf}
bad = 0
for _ in range(400000):
    beta = rng.uniform(-3, 1)            # a + b > 0  <=>  beta < 1
    c = beta ** 2 + rng.exponential(0.3) * rng.choice([1e-3, 1e-1, 1.0])
    a, b = 1.0, -beta
    if not (c > b and b + c < 0):
        continue
    det = a * c - b * b
    # ray-1 maximiser s* (formula of the note)
    sstar = (a * (b + c) + np.sqrt(a * det * (a + 2 * b + c))) / (a * (a + b))
    tK = -(a + b) / (b + c)
    G1 = (np.sqrt(a * (a + 2 * b + c) / det) - 1) / 4
    # t* by direct maximisation of f2 on the line
    f2 = lambda t: ((c - b) * t - (a - b)) / (2 * (a + 2 * b * t + c * t * t))
    ts = np.linspace(-50, 50, 20001)
    tstar = ts[np.argmax(f2(ts))]
    adm2 = tstar <= tK                   # b + c < 0: restriction (a+b) + t(b+c) >= 0 means t <= tK
    if sstar < 0:
        cnt['iv'] += 1
        cond = beta ** 2 < c < 2 * beta ** 2 / (1 + beta)
        s = -(b + c) / (2 * c) - (b + c) / (a + 2 * b + c)
        worst['iv'] = min(worst['iv'], s)
        bad += (not cond) or s < 0.75 - 1e-12
    elif not adm2:
        cnt['v'] += 1
        worst['v'] = min(worst['v'], G1)
        bad += G1 <= 0.2887 - 1e-4 or not (beta < (np.sqrt(17) - 1) / 8)
print('case (iv) samples %d: min of f_1(0) + kb_2 = %.5f (claim > 3/4); case (v) samples %d: min G_1 = %.5f '
      '(claim > 0.2887), all beta < 0.3904; violations %d' % (cnt['iv'], worst['iv'], cnt['v'], worst['v'], bad))
ok = abs(best.fun - target) < 1e-7 and best.fun >= target - 1e-9 and min(nb) >= target and vals[0][0] >= target - 1e-9 and bad == 0
print('ALL PASS' if ok else 'SOME CHECK FAILED')
