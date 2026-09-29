"""E12: 'choice of transformation' (Munoz-Serrano 2022, Sec. 6) as a selection space.
Sets C(L, lam) = {s : ||(L u)_y|| <= lam^T (L u)_x}, u = u(s, 1) Sylvester coordinates of the
homogenized quadratic, L in O(n, m) (the automorphism group of the form).  Every such set is
S-free.  Compare, for bilinear S (k = 3, signature (2,2)) and random 2-variable S:
  SCIP  : Chmiela-Munoz-Serrano maximal set (constant Gamma, eigen-coordinates, default lam)
  lam   : best constant lam, L = I (homogeneous sets)
  orbit : best (L, lam) over the O(n,m)-orbit (random restarts + Nelder-Mead)
against the exact corner bound z_K."""
import numpy as np, json, sys
from scipy.linalg import expm
from scipy.optimize import minimize
from sfree import ms_set, ic_bound, corner_bound, qval, step_length
import test_sfree
from test_sfree import rand_inst

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 31)
test_sfree.rng = rng


def sylvester(Q, b, c):
    k = len(b)
    Ab = np.zeros((k + 1, k + 1)); Ab[:k, :k] = Q; Ab[:k, k] = Ab[k, :k] = b / 2; Ab[k, k] = c
    th, V = np.linalg.eigh(Ab)
    ip = [i for i in range(k + 1) if th[i] > 1e-9]; im = [i for i in range(k + 1) if th[i] < -1e-9]
    W = np.vstack([np.sqrt(th[i]) * V[:, i] for i in ip] + [np.sqrt(-th[i]) * V[:, i] for i in im])
    return W, len(ip), len(im)


def lie_basis(n, m):
    d = n + m; J = np.diag([1.0] * n + [-1.0] * m); B = []
    for i in range(d):
        for j in range(i + 1, d):
            E = np.zeros((d, d)); E[i, j] = 1; E[j, i] = -1   # antisymmetric generator
            G = E @ J                                          # G^T J + J G = 0  <=>  G = E J with E antisym.
            B.append(G)
    return B


def make_G(W, n, m, L, lam):
    def G(s):
        u = L @ (W @ np.append(s, 1.0))
        return np.linalg.norm(u[n:]) - lam @ u[:n]
    return G


def orbit_bound(Q, b, c, sbar, P, w, restarts=12):
    W, n, m = sylvester(Q, b, c)
    basis = lie_basis(n, m)

    def unpack(p):
        L = expm(sum(pi * Bi for pi, Bi in zip(p[:len(basis)], basis)))
        v = p[len(basis):]
        lam = v / max(np.linalg.norm(v), 1e-12)
        return L, lam

    def f(p):
        L, lam = unpack(p)
        G = make_G(W, n, m, L, lam)
        if G(sbar) >= -1e-12:
            return 0.0
        return -min(ic_bound(G, sbar, P, w)[0], 1e9)

    ub = W @ np.append(sbar, 1.0)
    p0 = np.concatenate([np.zeros(len(basis)), ub[:n] / np.linalg.norm(ub[:n])])
    best_lam = -f(p0)                      # L = I, lam = x-part direction (homogeneous analog of default)
    # best lam with L = I
    for t in range(40):
        v = rng.normal(size=n)
        best_lam = max(best_lam, -f(np.concatenate([np.zeros(len(basis)), v])))
    best = best_lam
    for t in range(restarts):
        p = np.concatenate([rng.normal(scale=0.7, size=len(basis)), rng.normal(size=n)])
        if -f(p) <= 0:
            continue
        r = minimize(f, p, method='Nelder-Mead', options=dict(maxiter=600, xatol=1e-7, fatol=1e-10))
        best = max(best, -r.fun)
    return best_lam, best


if __name__ == '__main__':
    out = {}
    for label, k, n_, case, N in [('bilin k=3 n=3', 3, 3, 'bilinear', 25), ('gen k=2 n=3', 2, 3, None, 25)]:
        rows = []
        for t in range(N):
            Q, b, c, sbar, P, w = rand_inst(k, n_, case)
            zk = corner_bound(Q, b, c, sbar, P, w)
            if not np.isfinite(zk):
                continue
            G0, cs = ms_set(Q, b, c, sbar)
            z0 = ic_bound(G0, sbar, P, w)[0]
            zl, zo = orbit_bound(Q, b, c, sbar, P, w)
            rows.append((min(z0, zk) / zk, min(zl, zk) / zk, min(max(zo, zl), zk) / zk))
            print(label, [round(x, 4) for x in rows[-1]], flush=True)
        R = np.array(rows)
        out[label] = dict(n=len(R), scip_mean=float(R[:, 0].mean()), lam_mean=float(R[:, 1].mean()), orbit_mean=float(R[:, 2].mean()),
                          scip_min=float(R[:, 0].min()), lam_min=float(R[:, 1].min()), orbit_min=float(R[:, 2].min()),
                          orbit_frac_ge_0p99=float(np.mean(R[:, 2] >= 0.99)))
        print('SUMMARY', label, out[label], flush=True)
    json.dump(out, open('exp12_orbit.json', 'w'), indent=1)
