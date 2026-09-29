"""Does the Munoz-Serrano construction with its *point-dependent* lambda = x'(T sbar)/|x'(T sbar)|,
applied under every admissible transformation T in SO+(2,1), reach z_K for 2-variable quadratics
of homogenized signature (2,1)?  Theorem 8 is about the orbit {L(C_lambda)} with lambda free.

Observation checked here: T sbar lies in the 2-plane spanned by the two tangency null lines of
C_{lambda(T sbar)}, so the point-rule family at a fixed sbar is (at most) one-parameter, while the
maximal sets containing sbar form a two-parameter family.

For each random instance (N = 2 rays): z_K (fine 1-D scan), the best full-family bound over all
pairs (gamma1, gamma2) (with the MPS completion G), and the best point-rule bound over T (with and
without the completion), each maximized by grid + Nelder-Mead.
"""
import sys
import numpy as np
from scipy.optimize import minimize

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
NINST = int(sys.argv[2]) if len(sys.argv) > 2 else 20


def sylvester(Qh):
    ev, V = np.linalg.eigh(Qh)
    pos = [i for i in range(3) if ev[i] > 1e-12]; neg = [i for i in range(3) if ev[i] < -1e-12]
    if len(pos) != 2 or len(neg) != 1:
        return None
    order = pos + neg
    # u = W xi with xi = (x1, x2, y) and u^T Qh u = x1^2 + x2^2 - y^2
    W = V[:, order] / np.sqrt(np.abs(ev[order]))
    return W


def zK_two(Qh, ubar, P, w):
    th = np.linspace(0, 1, 200001)
    D = np.outer(th / w[0], P[:, 0]) + np.outer((1 - th) / w[1], P[:, 1])   # direction per unit cost
    Dh = np.hstack([D, np.zeros((len(th), 1))])
    a = np.einsum('ij,jk,ik->i', Dh, Qh, Dh); b = 2 * Dh @ Qh @ ubar; c = ubar @ Qh @ ubar
    # smallest tau > 0 with a tau^2 + b tau + c <= 0
    tau = np.full(len(th), np.inf)
    disc = b * b - 4 * a * c
    for i in range(len(th)):
        if abs(a[i]) < 1e-14:
            if b[i] < 0:
                tau[i] = -c / b[i]
            continue
        if disc[i] < 0:
            continue
        r = np.sqrt(disc[i])
        roots = sorted([(-b[i] - r) / (2 * a[i]), (-b[i] + r) / (2 * a[i])])
        pos = [t for t in roots if t > 0]
        if not pos:
            continue
        tau[i] = pos[0] if a[i] > 0 else (roots[1] if roots[1] > 0 else np.inf)
    return tau.min()


def bound_of(cons, ubar, P, w):
    """cons: list of row vectors c (in u-coordinates, u = (s, t)) of constraints c.u >= 0."""
    val = np.inf
    for j in range(P.shape[1]):
        dirn = np.append(P[:, j], 0.0)
        al = np.inf
        for c in cons:
            c0 = c @ ubar; c1 = c @ dirn
            if c0 <= 0:
                return 0.0
            if c1 < 0:
                al = min(al, -c0 / c1)
        val = min(val, w[j] * al)
    return val


def set_from_gammas(g1, g2, Winv, ad, complete=True):
    """C_Gamma with Gamma(1)=g1, Gamma(-1)=g2 in xi-coordinates: g1.x - y >= 0, g2.x + y >= 0.
    MPS completion: keep beta iff a.Gamma(beta) + d beta <= 0 (with H = {a.x + d y = -1})."""
    a, d = ad[:2], ad[2]
    # MPS Thm 4 applies only if ||a|| <= |d|; if |d| < ||a|| (Thm 5) dropping inequalities may
    # destroy Q_g-freeness, so no completion is applied there.
    complete = complete and np.linalg.norm(a) <= abs(d) + 1e-12
    cons = []
    for g, beta in ((g1, 1.0), (g2, -1.0)):
        if complete and a @ g + d * beta > 0:
            continue
        row = np.append(g, -beta)          # g.x - beta y
        cons.append(row @ Winv)            # as a function of u
    return cons


def boost(eta):
    c, s = np.cosh(eta), np.sinh(eta)
    return np.array([[c, 0, s], [0, 1, 0], [s, 0, c]])


def rot(p):
    c, s = np.cos(p), np.sin(p)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def point_rule_set(params, W, ubar, ad, complete):
    T = rot(params[0]) @ boost(params[1]) @ rot(params[2])
    Winv = np.linalg.inv(W)
    xi = T @ Winv @ ubar
    lam = xi[:2] / np.linalg.norm(xi[:2])
    # in xi' = T xi coordinates C_lambda = {lam.x' >= |y'|}; hyperplane (a', d') = ad T^{-1}
    adp = ad @ np.linalg.inv(T)
    return set_from_gammas(lam, lam, T @ Winv, adp, complete)


def main():
    done = 0
    ratios = []
    while done < NINST:
        Q = rng.standard_normal((2, 2)); Q = (Q + Q.T) / 2
        b = rng.standard_normal(2); c = rng.standard_normal()
        Qh = np.block([[Q, b[:, None] / 2], [b[None, :] / 2, np.array([[c]])]])
        W = sylvester(Qh)
        if W is None:
            continue
        sbar = rng.standard_normal(2) * 1.5
        ubar = np.append(sbar, 1.0)
        if ubar @ Qh @ ubar <= 0.05:
            continue
        P = rng.standard_normal((2, 2)); w = rng.uniform(0.3, 1.5, 2)
        zk = zK_two(Qh, ubar, P, w)
        if not np.isfinite(zk):
            continue
        ad = -W[2, :]        # t = W[2,:] xi = 1  <=>  a.x + d y = -1 with (a,d) = -W[2,:]
        Winv = np.linalg.inv(W)
        # full family over (theta1, theta2), with completion
        def ffull(th):
            g1 = np.array([np.cos(th[0]), np.sin(th[0])]); g2 = np.array([np.cos(th[1]), np.sin(th[1])])
            return bound_of(set_from_gammas(g1, g2, Winv, ad, True), ubar, P, w)
        grid = np.linspace(0, 2 * np.pi, 121)
        best_full = max((ffull((t1, t2)), t1, t2) for t1 in grid for t2 in grid)
        r = minimize(lambda th: -ffull(th), best_full[1:], method='Nelder-Mead', options=dict(xatol=1e-10, fatol=1e-12, maxiter=3000))
        zfull = max(best_full[0], -r.fun)
        out = [zk, zfull]
        for complete in (False, True):
            f = lambda p: bound_of(point_rule_set(p, W, ubar, ad, complete), ubar, P, w)
            g1 = np.linspace(0, 2 * np.pi, 25); ge = np.linspace(-4, 4, 33)
            best = max((f((p1, e, p2)), p1, e, p2) for p1 in g1 for e in ge for p2 in g1)
            for _ in range(3):
                r = minimize(lambda p: -f(p), best[1:], method='Nelder-Mead', options=dict(xatol=1e-10, fatol=1e-12, maxiter=4000))
                if -r.fun > best[0]:
                    best = (-r.fun, *r.x)
            out.append(best[0])
        if max(out[1:]) > zk * (1 + 1e-4):
            print('   WARNING: a bound exceeds z_K (set not S-free?)', out)
        done += 1
        ratios.append(out)
        print('inst %2d  z_K=%.6f  full/zK=%.6f  point-rule/zK=%.6f  point-rule+G/zK=%.6f' % (done, zk, out[1] / zk, out[2] / zk, out[3] / zk), flush=True)
    R = np.array(ratios)
    print('summary: full family ratio min %.6f; point-rule min %.6f mean %.4f; point-rule+completion min %.6f mean %.4f; #instances point-rule+G < 0.999: %d / %d'
          % ((R[:, 1] / R[:, 0]).min(), (R[:, 2] / R[:, 0]).min(), (R[:, 2] / R[:, 0]).mean(), (R[:, 3] / R[:, 0]).min(), (R[:, 3] / R[:, 0]).mean(),
             int(((R[:, 3] / R[:, 0]) < 0.999).sum()), len(R)))


if __name__ == '__main__':
    main()
