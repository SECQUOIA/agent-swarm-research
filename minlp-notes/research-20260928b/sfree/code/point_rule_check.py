"""Point rule vs full orbit, 2-variable quadratics of signature (2,1) (Revision after review, item 2).

Munoz-Serrano / Chmiela use lambda = xhat(T sbar)/||xhat(T sbar)||.  Then T sbar lies in the plane
spanned by the two tangency null lines of C_lambda; this is invariant under automorphisms, so every
*plain* set C_lambda cap H the rule produces (for any transformation) is {g1^T x >= y, g2^T x >= -y}
(Sylvester coordinates) with u_s = (xhat, yhat) = a (g1, 1) + b (g2, -1), a, b > 0.  Given
g1 = (cos th, sin th):  a = (|xhat|^2 - yhat^2) / (2 (g1.xhat - yhat)),  b = a - yhat,
g2 = (xhat - a g1)/b.  We scan th (1-parameter family) and compare with z_K (= best over the full orbit).
Instances: kappa > 0 (Chmiela Case 2, ||d|| < ||a||).  Corners with z_K = infinity are skipped (4 of
the 40 generated with seed 0).  These plain sets are NOT exactly the Munoz-Serrano sets: MS Section 5.2
enlarges a member whose tangency point lies on the wrong side of H; see ms_asymptote_check.py for
their full construction.  The optional second value (MS_UPPER) is only a loose relaxation that lets
the replaced halfspace be any null halfspace; it is not a bound for MS's construction in any useful
sense and is superseded by ms_asymptote_check.py.
Usage: python3 point_rule_check.py SEED NINST"""
import sys, numpy as np
from scipy.optimize import minimize_scalar
from core import corner_bound, qval
from orbit_n1 import sylvester


def case2_instance(rng):
    while True:
        A = rng.normal(size=(2, 2)); Q = (A + A.T) / 2
        th, V = np.linalg.eigh(Q)
        if not (th[0] < -0.1 and th[1] > 0.1):
            continue
        b = rng.normal(size=2)
        bb = V.T @ b
        kappa_minus_c = -0.25 * sum(bb[i] ** 2 / th[i] for i in range(2))
        c = kappa_minus_c * 0 + rng.uniform(0.1, 2.0) - kappa_minus_c   # kappa = c - (1/4) sum = U(0.1, 2) > 0
        sbar = rng.normal(size=2) * 2
        if qval(Q, b, c, sbar) <= 0.05:
            continue
        N = int(rng.integers(2, 5)); P = rng.normal(size=(2, N)); w = rng.uniform(0.1, 1, N)
        return Q, b, c, sbar, P, w


MS_UPPER = False


def point_rule_best(Q, b, c, sbar, P, w):
    W, n, m = sylvester(Q, b, c)
    assert (n, m) == (2, 1)
    us = W @ np.append(sbar, 1.0); xh, yh = us[:2], us[2]
    D = [W @ np.append(P[:, j], 0.0) for j in range(P.shape[1])]

    def bound(th):
        g1 = np.array([np.cos(th), np.sin(th)])
        den = g1 @ xh - yh
        if den <= 1e-14:
            return 0.0
        a = (xh @ xh - yh * yh) / (2 * den); bq = a - yh
        if a <= 0 or bq <= 1e-14:
            return 0.0
        g2 = (xh - a * g1) / bq
        vals = []
        for j, d in enumerate(D):
            al = np.inf
            for (g, s) in ((g1, 1.0), (g2, -1.0)):
                v0 = g @ xh - s * yh; sl = g @ d[:2] - s * d[2]
                if sl < 0:
                    al = min(al, v0 / -sl)
            if np.isfinite(al):
                vals.append(w[j] * al)
        return min(vals) if vals else np.inf

    ths = np.linspace(0, 2 * np.pi, 20001)
    vals = np.array([bound(t) for t in ths])
    k = int(np.argmax(vals)); best = vals[k]
    lo, hi = ths[max(0, k - 1)], ths[min(len(ths) - 1, k + 1)]
    r = minimize_scalar(lambda t: -bound(t), bounds=(lo, hi), method='bounded', options=dict(xatol=1e-13))
    if not MS_UPPER:
        return max(best, -r.fun)
    # Upper bound for Munoz-Serrano's full construction (their Section 5.2 enlarges the set when a
    # tangency point lies on the wrong side of H and keeps the halfspaces whose tangency point is on
    # the slice side).  For each member: if both tangency rays (g1, 1), (g2, -1) have homogenizing
    # coordinate >= 0, the construction returns the member itself; otherwise keep the good halfspace
    # and let the other one (any unit g) be chosen optimally.
    Wi = np.linalg.inv(W)
    hcoord = lambda nvec: (Wi @ nvec)[-1]
    angs = np.linspace(0, 2 * np.pi, 721)

    def pair_bound(g1, g2):
        vals = []
        for j, d in enumerate(D):
            al = np.inf
            for (g, s) in ((g1, 1.0), (g2, -1.0)):
                v0 = g @ xh - s * yh; sl = g @ d[:2] - s * d[2]
                if v0 <= 0:
                    return 0.0
                if sl < 0:
                    al = min(al, v0 / -sl)
            if np.isfinite(al):
                vals.append(w[j] * al)
        return min(vals) if vals else np.inf

    def ms_bound(th):
        g1 = np.array([np.cos(th), np.sin(th)])
        den = g1 @ xh - yh
        if den <= 1e-14:
            return 0.0
        a = (xh @ xh - yh * yh) / (2 * den); bq = a - yh
        if a <= 0 or bq <= 1e-14:
            return 0.0
        g2 = (xh - a * g1) / bq
        h1 = hcoord(np.append(g1, 1.0)); h2 = hcoord(np.append(g2, -1.0))
        if h1 >= 0 and h2 >= 0:
            return pair_bound(g1, g2)
        G = [np.array([np.cos(f), np.sin(f)]) for f in angs]
        if h1 >= 0:
            return max(pair_bound(g1, g) for g in G)
        return max(pair_bound(g, g2) for g in G)

    ths2 = np.linspace(0, 2 * np.pi, 2001)
    return max(best, -r.fun), max(ms_bound(t) for t in ths2)


if __name__ == '__main__':
    rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    NI = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    miss = []; NFIN = 0
    for i in range(NI):
        Q, b, c, sbar, P, w = case2_instance(rng)
        zk = corner_bound(Q, b, c, sbar, P, w)
        if not np.isfinite(zk):
            print('instance %2d  z_K = inf (no ray combination meets S): skipped' % i, flush=True)
            continue
        NFIN += 1
        MS_UPPER = True
        globals()['MS_UPPER'] = True
        zp, zms = point_rule_best(Q, b, c, sbar, P, w)
        print('instance %2d  N=%d  z_K=%.6f  plain point rule / z_K = %.6f   loose relaxation (any null halfspace) / z_K = %.6f'
              % (i, P.shape[1], zk, min(zp, zk) / zk, min(zms, zk) / zk), flush=True)
        if zp < zk * (1 - 1e-6):
            miss.append((round(zp / zk, 6), round(min(zms, zk) / zk, 6)))
    print('corners with finite z_K: %d; plain point rule misses z_K in %d; (plain, loose relaxation) ratios: %s' % (NFIN, len(miss), miss))
    print('loose relaxation below z_K in %d instances (not a statement about MS; see ms_asymptote_check.py)' % sum(1 for m_ in miss if m_[1] < 1 - 1e-6))
