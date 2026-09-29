"""Check of Theorem E for 2-variable quadratics: the best cut over the Lorentz orbit of the
Munoz-Serrano sets equals the corner bound z_K.

Homogenize q to q_h(s,t) = [s;t]^T A_h [s;t] and write q_h = ||x||^2 - ||y||^2 in Sylvester
coordinates u = W (s, 1).  Signature (n, 1): the orbit sets are {g1^T x >= y, g2^T x >= -y}
with unit g1 != -g2; relaxing to ||g_i|| <= 1 keeps them Q_h-free, and containment of the
vertices of T_z is a pair of independent SOCP feasibility problems.  Signature (1, m): the
only maximal sets are {x >= ||y||} and {-x >= ||y||}.
"""
import sys, json, numpy as np, warnings
warnings.filterwarnings('ignore')
import cvxpy as cp
from core import corner_bound, qval



def sylvester(Q, b, c):
    k = len(b)
    Ah = np.zeros((k + 1, k + 1)); Ah[:k, :k] = Q; Ah[:k, k] = Ah[k, :k] = b / 2; Ah[k, k] = c
    th, V = np.linalg.eigh(Ah)
    ip = [i for i in range(k + 1) if th[i] > 1e-9]; im = [i for i in range(k + 1) if th[i] < -1e-9]
    W = np.vstack([np.sqrt(th[i]) * V[:, i] for i in ip] + [np.sqrt(-th[i]) * V[:, i] for i in im])
    return W, len(ip), len(im)


def contains_n1(Xs, ys, sign):
    """exists g, ||g||<=1: g^T x_v >= sign*y_v for all v, strictly for v = 0 (sbar)."""
    g = cp.Variable(Xs.shape[1]); t = cp.Variable()
    cons = [cp.norm(g) <= 1] + [g @ Xs[i] - sign * ys[i] >= (t if i == 0 else 0) for i in range(len(ys))]
    pr = cp.Problem(cp.Maximize(t), cons + [t <= 1])
    pr.solve(solver='CLARABEL')
    return pr.status in ('optimal', 'optimal_inaccurate') and t.value is not None and t.value > 1e-9


def best_orbit(Q, b, c, sbar, P, w, zk, iters=40):
    W, n, m = sylvester(Q, b, c)

    def feasible(z):
        pts = [sbar] + [sbar + z / w[j] * P[:, j] for j in range(P.shape[1])]
        U = np.array([W @ np.append(p, 1.0) for p in pts])
        if m == 1:
            Xs, ys = U[:, :n], U[:, n]
            return contains_n1(Xs, ys, 1.0) and contains_n1(Xs, ys, -1.0)
        if n == 1:
            xs, Ys = U[:, 0], U[:, 1:]
            nr = np.linalg.norm(Ys, axis=1)
            return any(np.all(sg * xs[1:] >= nr[1:] - 1e-12) and sg * xs[0] > nr[0] for sg in (1, -1))
        raise ValueError('signature not covered')
    lo, hi = 0.0, zk
    for _ in range(iters):
        mid = (lo + hi) / 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid
    return lo, (n, m)


if __name__ == '__main__':
    rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    T = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    rows = []
    for t in range(T):
        A = rng.normal(size=(2, 2)); Q = (A + A.T) / 2; b = rng.normal(size=2); c = float(rng.normal())
        ev = np.linalg.eigvalsh(Q)
        if ev.min() > 0 or ev.max() < 0:
            continue
        while True:
            sbar = rng.normal(size=2)
            if qval(Q, b, c, sbar) > 0.05:
                break
        N = int(rng.integers(2, 6)); P = rng.normal(size=(2, N)); w = rng.uniform(0.1, 1, N)
        zk = corner_bound(Q, b, c, sbar, P, w)
        if not np.isfinite(zk):
            continue
        zo, sig = best_orbit(Q, b, c, sbar, P, w, zk)
        rows.append((zo / zk, sig))
        print('signature %s  orbit/z_K = %.8f' % (sig, zo / zk), flush=True)
    r = np.array([x[0] for x in rows])
    print('instances', len(r), 'min ratio %.8f  mean %.8f' % (r.min(), r.mean()),
          'signatures', {str(s): sum(1 for x in rows if x[1] == s) for s in set(x[1] for x in rows)})
