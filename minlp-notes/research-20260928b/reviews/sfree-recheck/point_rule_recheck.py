"""Independent recheck of Section 6.1 (point rule vs full orbit) of the sfree note.

Only the instance generator is taken from the note (sfree/code/point_rule_check.py: case2_instance, seed 0),
so that the same 40 corners are used.  Everything else is my own code:
  * z_K for k = 2 (supports of size <= 2 suffice, Lemma 3): exact one-ray roots, two-ray direction scan
    (dense + bounded refinement);
  * Sylvester form W of the homogenized form (x1^2 + x2^2 - y^2), slice t = l^T v;
  * full orbit: all maximal sets {g1^T x >= y, g2^T x >= -y}, scan over (g1, g2) in S^1 x S^1 + refinement;
  * point rule (plain sets C_lambda cap H under every transformation), two parametrizations:
      (i) the note's theta-formula (s-bar in the span of the tangency lines),
      (ii) independently, L = B(eta) R(phi) in SO+(2,1) and lambda = xbar'/|xbar'| in the L-coordinates;
  * the full Munoz-Serrano Section 5.2 construction (Case 2, |d| < |a| = 1; m = 1) with the point rule,
    under every transformation L:  for beta = +-1, the inequality -lambda^T x + beta y <= 0 is kept when
    lambda^T a + d beta <= 0; otherwise it becomes -lambda^T x + grad phi(beta) y <= r(beta) with
    phi(beta) = sqrt((1-d^2)(1-(lambda^T a)^2)) - d beta lambda^T a, grad phi(beta) = beta phi(beta),
    r(beta) = (d beta + lambda^T a phi)/(phi + d beta lambda^T a)  (MS eq. (12), Lemma 2, Theorem 10).
    On H (a^T x + d y = -1) the constant r is homogenized as -r (a^T x + d y).
Usage: python3 point_rule_recheck.py [NINST=40]
"""
import sys, os
sys.dont_write_bytecode = True     # do not write __pycache__ into the note's code directory
import numpy as np
from scipy.optimize import minimize_scalar, minimize

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'sfree', 'code'))
from point_rule_check import case2_instance        # instance generator only

J = np.diag([1.0, 1.0, -1.0])


def q_of(Q, b, c, s):
    return s @ Q @ s + b @ s + c


# ----------------------------------------------------------------- z_K (own)
def first_hit(A, B, g0):
    """smallest tau > 0 with A tau^2 + B tau + g0 <= 0 (g0 > 0); inf if none."""
    if abs(A) < 1e-14:
        return -g0 / B if B < 0 else np.inf
    D = B * B - 4 * A * g0
    if A > 0:
        if D < 0 or B >= 0:
            return np.inf
        return (-B - np.sqrt(D)) / (2 * A)
    return (-B - np.sqrt(D)) / (2 * A)          # A < 0: roots of opposite sign, the positive one


def zK(Q, b, c, sbar, P, w, n=20001):
    g0 = q_of(Q, b, c, sbar); gs = 2 * Q @ sbar + b
    best = np.inf
    N = P.shape[1]
    for j in range(N):
        p = P[:, j]
        best = min(best, w[j] * first_hit(p @ Q @ p, gs @ p, g0))
    for i in range(N):
        for j in range(i + 1, N):
            def tau(th):
                d = th / w[i] * P[:, i] + (1 - th) / w[j] * P[:, j]
                return first_hit(d @ Q @ d, gs @ d, g0)
            ths = np.linspace(0, 1, n)
            vals = np.array([tau(t) for t in ths])
            k = int(np.argmin(vals))
            best = min(best, vals[k])
            if np.isfinite(vals[k]):
                lo, hi = ths[max(k - 1, 0)], ths[min(k + 1, n - 1)]
                r = minimize_scalar(lambda t: tau(t) if np.isfinite(tau(t)) else 1e300, bounds=(lo, hi),
                                    method='bounded', options=dict(xatol=1e-14))
                best = min(best, r.fun)
    return best


# ----------------------------------------------------------------- Sylvester form (own)
def sylv(Q, b, c):
    A = np.zeros((3, 3)); A[:2, :2] = Q; A[:2, 2] = A[2, :2] = b / 2; A[2, 2] = c
    mu, V = np.linalg.eigh(A)
    order = np.argsort(-mu)            # positives first
    mu, V = mu[order], V[:, order]
    assert mu[0] > 0 and mu[1] > 0 and mu[2] < 0, mu
    W = np.diag(np.sqrt(np.abs(mu))) @ V.T      # u^T A u = (Wu)^T J (Wu)
    assert np.allclose(W.T @ J @ W, A)
    l = np.linalg.inv(W).T @ np.array([0, 0, 1.0])  # t = l^T v
    return W, l


# ----------------------------------------------------------------- bound of a polyhedral cone {n_i^T v >= 0}
def bound_normals(Ns, us, Ds, w):
    """Ns: (..., k, 3) inward normals; returns (...,) one-cut bound min_j w_j alpha_j (0 if us not interior)."""
    s0 = Ns @ us                                   # (..., k)
    inside = np.all(s0 > 1e-12, axis=-1)
    out = np.full(s0.shape[:-1], np.inf)
    for j, d in enumerate(Ds):
        sl = Ns @ d                                # (..., k)
        with np.errstate(divide='ignore', invalid='ignore'):
            al = np.where(sl < 0, s0 / np.where(sl < 0, -sl, 1.0), np.inf)
        out = np.minimum(out, w[j] * al.min(axis=-1))
    return np.where(inside, out, 0.0)


def orbit_normals(g1, g2):
    """{g1^T x >= y, g2^T x >= -y}: inward normals (g1, -1), (g2, +1)."""
    n1 = np.concatenate([g1, -np.ones(g1.shape[:-1] + (1,))], axis=-1)
    n2 = np.concatenate([g2, np.ones(g2.shape[:-1] + (1,))], axis=-1)
    return np.stack([n1, n2], axis=-2)


def unit(a):
    return np.stack([np.cos(a), np.sin(a)], axis=-1)


def full_orbit(us, Ds, w, n=721):
    a = np.linspace(0, 2 * np.pi, n, endpoint=False)
    A1, A2 = np.meshgrid(a, a, indexing='ij')
    vals = bound_normals(orbit_normals(unit(A1), unit(A2)), us, Ds, w)
    f = lambda x: -float(bound_normals(orbit_normals(unit(np.array(x[0])), unit(np.array(x[1]))), us, Ds, w))
    idx = np.argsort(-vals.ravel())[:8]
    best = vals.max()
    for k in idx:
        i, j = np.unravel_index(k, vals.shape)
        r = minimize(f, [A1[i, j], A2[i, j]], method='Nelder-Mead', options=dict(xatol=1e-12, fatol=1e-15, maxiter=3000))
        best = max(best, -r.fun)
    return best


# ----------------------------------------------------------------- point rule, parametrization (i): theta
def pr_theta_normals(th, us):
    xh, yh = us[:2], us[2]
    g1 = unit(th)
    den = g1 @ xh - yh
    a = (xh @ xh - yh * yh) / (2 * np.where(den > 1e-14, den, np.nan))
    bq = a - yh
    g2 = (xh[None, :] - a[:, None] * g1) / bq[:, None]
    ok = (den > 1e-14) & (a > 0) & (bq > 1e-14)
    return orbit_normals(g1, g2), ok


def point_rule_theta(us, Ds, w, n=200001):
    th = np.linspace(0, 2 * np.pi, n)
    Ns, ok = pr_theta_normals(th, us)
    vals = np.where(ok, bound_normals(np.nan_to_num(Ns), us, Ds, w), 0.0)
    k = int(np.argmax(vals))
    f = lambda t: -float(np.where(pr_theta_normals(np.array([t]), us)[1], bound_normals(np.nan_to_num(pr_theta_normals(np.array([t]), us)[0]), us, Ds, w), 0.0)[0])
    r = minimize_scalar(f, bounds=(th[max(k - 1, 0)], th[min(k + 1, n - 1)]), method='bounded', options=dict(xatol=1e-14))
    return max(vals[k], -r.fun)


# ----------------------------------------------------------------- transformations L = B(eta) R(phi)
def Lmat(eta, phi):
    ch, sh = np.cosh(eta), np.sinh(eta); c, s = np.cos(phi), np.sin(phi)
    B = np.array([[ch, 0, sh], [0, 1, 0], [sh, 0, ch]])
    Rm = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    return B @ Rm


def Lmats(E, P_):
    ch, sh = np.cosh(E), np.sinh(E); c, s = np.cos(P_), np.sin(P_)
    L = np.zeros(E.shape + (3, 3))
    # B @ R
    L[..., 0, 0] = ch * c; L[..., 0, 1] = -ch * s; L[..., 0, 2] = sh
    L[..., 1, 0] = s; L[..., 1, 1] = c; L[..., 1, 2] = 0
    L[..., 2, 0] = sh * c; L[..., 2, 1] = -sh * s; L[..., 2, 2] = ch
    return L


def rule_sets(L, us, l, ms):
    """Inward normals (in v-coordinates) of the point-rule set for transformations L (..., 3, 3).
    ms=False: plain C_lambda; ms=True: Munoz-Serrano Section 5.2 construction (Case 2)."""
    up = L @ us                                          # (..., 3)
    lam = up[..., :2] / np.linalg.norm(up[..., :2], axis=-1, keepdims=True)
    Ns = []
    info = {}
    if ms:
        lp = np.linalg.solve(np.swapaxes(L, -1, -2), np.broadcast_to(l, L.shape[:-1])[..., None])[..., 0]   # l' = L^{-T} l
        a_raw, d_raw = -lp[..., :2], -lp[..., 2]
        na = np.linalg.norm(a_raw, axis=-1)
        assert np.all(np.abs(d_raw) < na), 'not Case 2'
        a, d = a_raw / na[..., None], d_raw / na
        la = np.sum(lam * a, axis=-1)
        info['changed'] = np.zeros(L.shape[:-2], dtype=int)
    for beta in (1.0, -1.0):
        m_keep = np.concatenate([lam, -beta * np.ones(lam.shape[:-1] + (1,))], axis=-1)   # lam^T x - beta y >= 0
        if not ms:
            m = m_keep
        else:
            sb = la + d * beta
            phi = np.sqrt((1 - d ** 2) * (1 - la ** 2)) - d * beta * la
            r = (d * beta + la * phi) / (phi + d * beta * la)
            nprime = np.concatenate([-lam + r[..., None] * a, (beta * phi + r * d)[..., None]], axis=-1)   # n'^T v' <= 0
            m = np.where((sb > 0)[..., None], -nprime, m_keep)
            info['changed'] += (sb > 0)
            info.setdefault('nprime', []).append(np.where((sb > 0)[..., None], nprime, np.nan))
            info.setdefault('lp', lp)
        Ns.append(np.einsum('...ji,...j->...i', L, m))     # L^T m
    return np.stack(Ns, axis=-2), info


def rule_scan(us, Ds, w, l, ms, ne=601, nphi=721, emax=7.0):
    E = np.sinh(np.linspace(-np.arcsinh(emax * 30), np.arcsinh(emax * 30), ne)) / 30   # dense near 0, up to +-emax
    Ph = np.linspace(0, 2 * np.pi, nphi, endpoint=False)
    EE, PP = np.meshgrid(E, Ph, indexing='ij')
    Ns, info = rule_sets(Lmats(EE, PP), us, l, ms)
    vals = bound_normals(Ns, us, Ds, w)
    f = lambda x: -float(bound_normals(rule_sets(Lmat(x[0], x[1])[None], us, l, ms)[0], us, Ds, w)[0])
    idx = np.argsort(-vals.ravel())[:6]
    best = vals.max(); arg = None
    for k in idx:
        i, j = np.unravel_index(k, vals.shape)
        r = minimize(f, [EE[i, j], PP[i, j]], method='Nelder-Mead', options=dict(xatol=1e-12, fatol=1e-15, maxiter=3000))
        if -r.fun > best:
            best = -r.fun; arg = r.x
    return best, vals, EE, PP, Ns, info


def ms_sanity(Q, b, c, sbar, W, l, us, Ds, w, rng):
    """Checks of the MS implementation on random L: normals null, tangency line of a modified halfspace lies in
    H_0 = {t = 0}; MS set contains the plain member; S-free (sampled points of S are not interior)."""
    Wi = np.linalg.inv(W)
    worst_null = worst_H0 = 0.0; contain_ok = True; free_ok = True; nchanged = 0
    # sample S cap H points: s with q(s) <= 0
    pts = rng.normal(size=(20000, 2)) * 6
    pts = pts[np.einsum('ij,jk,ik->i', pts, Q, pts) + pts @ b + c <= 0]
    V = (W @ np.vstack([pts.T, np.ones(len(pts))])).T      # v-coordinates of S points
    for _ in range(300):
        L = Lmat(rng.normal() * 2, rng.uniform(0, 2 * np.pi))[None]
        Nms, info = rule_sets(L, us, l, True)
        Npl, _ = rule_sets(L, us, l, False)
        for npr in info['nprime']:
            npr = npr[0]
            if np.all(np.isfinite(npr)):
                nchanged += 1
                worst_null = max(worst_null, abs(npr[:2] @ npr[:2] - npr[2] ** 2) / (npr @ npr))
                tl = J @ npr                               # tangency null line in v'-coords
                worst_H0 = max(worst_H0, abs(info['lp'][0] @ tl) / (np.linalg.norm(info['lp'][0]) * np.linalg.norm(tl)))
        # containment: along each ray, MS step >= plain step
        for d in Ds:
            bm = bound_normals(Nms, us, [d], np.ones(1))[0]; bp = bound_normals(Npl, us, [d], np.ones(1))[0]
            if bm < bp * (1 - 1e-9):
                contain_ok = False
        # S-freeness: no sampled S point strictly inside (all normals > 0)
        s0 = V @ Nms[0].T
        if np.any(np.all(s0 > 1e-9 * np.linalg.norm(V, axis=1)[:, None], axis=1)):
            free_ok = False
        if not (Nms[0] @ us > 0).all():
            free_ok = False
    return nchanged, worst_null, worst_H0, contain_ok, free_ok


def ms_example8():
    """MS Example 8: a = (-1, 1)/sqrt2, d = 1/sqrt2, lambda = (-1, -1)/sqrt2 gives r(-1) = 0 (kept) and, for
    beta = 1, phi = 1/sqrt2, r = 1:  C1 = {(x1+x2)/sqrt2 - y <= 0, (x1+x2)/sqrt2 + y/sqrt2 <= 1}."""
    s2 = np.sqrt(2.0)
    a = np.array([-1, 1]) / s2; d = 1 / s2; lam = np.array([-1, -1]) / s2
    la = lam @ a
    out = {}
    for beta in (1.0, -1.0):
        sb = la + d * beta
        if sb <= 0:
            out[beta] = ('kept', None, None)
        else:
            phi = np.sqrt((1 - d ** 2) * (1 - la ** 2)) - d * beta * la
            r = (d * beta + la * phi) / (phi + d * beta * la)
            out[beta] = ('modified', phi, r)
    ok = out[-1.0][0] == 'kept' and out[1.0][0] == 'modified' and abs(out[1.0][1] - 1 / s2) < 1e-15 and abs(out[1.0][2] - 1) < 1e-15
    print('MS Example 8 reproduced (beta=-1 kept; beta=+1: phi = 1/sqrt2, r = 1): %s' % ok, flush=True)
    return ok


if __name__ == '__main__':
    assert ms_example8()
    NI = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    rng = np.random.default_rng(0)
    rng2 = np.random.default_rng(12345)
    finite = misses = 0; ms_miss = 0; rows = []
    for i in range(NI):
        Q, b, c, sbar, P, w = case2_instance(rng)
        zk = zK(Q, b, c, sbar, P, w)
        if not np.isfinite(zk):
            print('instance %2d  N=%d  z_K = inf (no ray combination meets S): skipped' % (i, P.shape[1]), flush=True)
            continue
        finite += 1
        W, l = sylv(Q, b, c)
        us = W @ np.append(sbar, 1.0)
        Ds = [W @ np.append(P[:, j], 0.0) for j in range(P.shape[1])]
        zo = full_orbit(us, Ds, w)
        zt = point_rule_theta(us, Ds, w)
        zl, *_ = rule_scan(us, Ds, w, l, False)
        zm, vals, EE, PP, Ns, info = rule_scan(us, Ds, w, l, True)
        # sanity of the MS implementation
        nch, wn, wh, cont, free = ms_sanity(Q, b, c, sbar, W, l, us, Ds, w, rng2)
        frac_changed = float(np.mean(info['changed'] > 0))
        miss = zt < zk * (1 - 1e-6)
        misses += miss
        ms_miss += zm < zk * (1 - 1e-6)
        print('instance %2d  N=%d  z_K=%.6f | full orbit %.6f | point rule: theta-family %.6f, L-scan %.6f | '
              'MS full construction (L-scan) %.6f | MS modified an inequality on %.0f%% of the L-grid; '
              'sanity: %d modified, null err %.1e, H0 err %.1e, contains plain %s, S-free %s'
              % (i, P.shape[1], zk, zo / zk, zt / zk, zl / zk, zm / zk, 100 * frac_changed, nch, wn, wh, cont, free),
              flush=True)
        rows.append((i, zk, zo / zk, zt / zk, zl / zk, zm / zk))
    print('corners with finite z_K: %d of %d' % (finite, NI))
    print('full orbit attains z_K (ratio >= 1 - 1e-6): %d of %d' % (sum(r[2] >= 1 - 1e-6 for r in rows), finite))
    print('plain point rule misses z_K: %d; ratios %s' % (misses, sorted(round(r[3], 3) for r in rows if r[3] < 1 - 1e-6)))
    print('max |theta-family - L-scan| (ratio): %.2e' % max(abs(r[3] - r[4]) for r in rows))
    print('MS full construction with the point rule misses z_K: %d; ratios %s'
          % (ms_miss, sorted(round(r[5], 4) for r in rows if r[5] < 1 - 1e-6)))
