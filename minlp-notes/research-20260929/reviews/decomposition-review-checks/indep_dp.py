"""Independent re-implementation of the fixed-slope decomposition certificate (note Sections 1.5, 3.3)
for the path family F = sum phi(x_i) + c_i x_i + b sum x_i x_{i+1}, phi(t) = t^2 - kappa t^4, on [-1,1]^n.

Written from the note's definitions, not from dp_certificate.py:
  * shell partition built geometrically (containment test on coordinates, not grid indices);
  * beta_{t,D} = min over (leaf B, cell D) with closed intersection of min_{z in B, z_t in D} Rel - lambda_t z_t,
    computed by golden-section search in z1 (90 steps) with z2 eliminated in closed form (bisection
    on the monotone derivative in the last bag);
  * the minimizing configuration is traced and re-checked from scratch (containments, intersections,
    value recomputed), which also tests Lemma 1.5 numerically.
Bags t = 0..n-2 with V_t = {t, t+1}; root bag 0; S_t = {t}; bag t holds phi(x_t) + c_t x_t + b x_t x_{t+1},
the last bag also phi(x_{n-1}) + c_{n-1} x_{n-1}.  alphaBB alpha = |b|/2 on each bilinear factor.

Usage: python3 indep_dp.py gap n mu j [b]         root gap at h = 2^-j, theta = 2^-mu, c = 0
       python3 indep_dp.py trace n mu j           trace and verify the minimizing configuration (c = 0)
       python3 indep_dp.py valid n seed mu j      validity l_{t,D}(s) <= phi_t(s) with c ~ U(-0.2,0.2)(seed)
       python3 indep_dp.py pairs mu j1 j2 ...     leaves, cells and (leaf, cell) pairs of one interior bag
"""
import math
import sys
import itertools
import numpy as np

KAPPA = 0.1
GR = (math.sqrt(5) - 1) / 2


def phi(t):
    return t * t - KAPPA * t ** 4


def dphi(t):
    return 2 * t - 4 * KAPPA * t ** 3


def shell_partition(p, h, mu, lo=-1.0, hi=1.0):
    p = np.atleast_1d(np.asarray(p, float))
    d = len(p)
    theta = 2.0 ** -mu
    J = max(0, math.ceil(math.log2((hi - lo) / h)))
    Ls, Us = [], []
    for e in itertools.product((0.0, 1.0), repeat=d):
        e = np.array(e)
        Ls.append(p + (e - 1) * h); Us.append(p + e * h)
    Ls, Us = [np.array(Ls)], [np.array(Us)]
    for j in range(1, J + 1):
        R, g = 2.0 ** j * h, theta * 2.0 ** (j - 1) * h
        N = int(round(2 * R / g))
        idx = np.array(list(itertools.product(range(N), repeat=d)))
        lo_c = p[None, :] - R + g * idx
        up_c = lo_c + g
        inner = np.all((lo_c >= p - R / 2 - 1e-12 * R) & (up_c <= p + R / 2 + 1e-12 * R), axis=1)
        Ls.append(lo_c[~inner]); Us.append(up_c[~inner])
    L = np.clip(np.concatenate(Ls), lo, hi)
    U = np.clip(np.concatenate(Us), lo, hi)
    keep = np.all(U - L > 1e-14, axis=1)
    return L[keep], U[keep]


def bag_value(z1, z2, l1, u1, l2, u2, b, lin1, lin2, last, cz1, cz2):
    ab = abs(b)
    v = phi(z1) + cz1 * z1 + lin1 * z1 + b * z1 * z2 - (ab / 2) * ((z1 - l1) * (u1 - z1) + (z2 - l2) * (u2 - z2)) + lin2 * z2
    if last:
        v = v + phi(z2) + cz2 * z2
    return v


def z2_opt(z1, l2, u2, b, lin2, last, cz2):
    ab = abs(b)
    if not last:
        return np.clip(((ab / 2) * (l2 + u2) - b * z1 - lin2) / ab, l2, u2)
    der = lambda z: dphi(z) + cz2 + b * z1 + (ab / 2) * (2 * z - l2 - u2) + lin2
    a, c = l2.copy(), u2.copy()
    for _ in range(64):
        m = 0.5 * (a + c)
        pos = der(m) > 0
        c = np.where(pos, m, c); a = np.where(pos, a, m)
    z = 0.5 * (a + c)
    z = np.where(der(l2) >= 0, l2, z)
    return np.where(der(u2) <= 0, u2, z)


def min_pair(A1, B1, l1, u1, l2, u2, b, lin1, lin2, last, cz1, cz2):
    """min over z1 in [A1,B1], z2 in [l2,u2] of the (convex) bag relaxation; golden section in z1."""
    f = lambda z1: bag_value(z1, z2_opt(z1, l2, u2, b, lin2, last, cz2), l1, u1, l2, u2, b, lin1, lin2, last, cz1, cz2)
    a, c = A1.copy(), B1.copy()
    x1 = c - GR * (c - a); x2 = a + GR * (c - a)
    f1, f2 = f(x1), f(x2)
    for _ in range(90):
        left = f1 <= f2
        c = np.where(left, x2, c); a = np.where(left, a, x1)
        nx1 = c - GR * (c - a); nx2 = a + GR * (c - a)
        x1n = np.where(left, nx1, x2); x2n = np.where(left, x1, nx2)
        f1n = np.where(left, f(nx1), f2); f2n = np.where(left, f1, f(nx2))
        x1, x2, f1, f2 = x1n, x2n, f1n, f2n
    cands = [a, c, 0.5 * (a + c), A1, B1]
    vals = np.stack([f(z) for z in cands])
    k = np.argmin(vals, axis=0)
    z1 = np.stack(cands)[k, np.arange(len(A1))]
    return vals.min(axis=0), z1, z2_opt(z1, l2, u2, b, lin2, last, cz2)


def certificate(n, b, c, xc, h, mu, slopes, keep=False):
    """xc: center; slopes: array lam[t] for t=1..n-2 (lam[0] unused). Returns root value, size, pairs, store."""
    size = pairs = 0
    child = None
    store = {}
    for t in range(n - 2, -1, -1):
        last = t == n - 2
        L, U = shell_partition(xc[t:t + 2], h, mu)
        size += len(L)
        l1, u1, l2, u2 = L[:, 0], U[:, 0], L[:, 1], U[:, 1]
        if child is None:
            off = np.zeros(len(L)); offarg = np.full(len(L), -1); lin2 = 0.0
        else:
            clo, chi, cbeta = child
            M = np.where((clo[None, :] <= u2[:, None]) & (chi[None, :] >= l2[:, None]), cbeta[None, :], np.inf)
            off, offarg = M.min(axis=1), M.argmin(axis=1)
            lin2 = slopes[t + 1]
        cz2 = c[n - 1]
        if t == 0:
            v, z1, z2 = min_pair(l1, u1, l1, u1, l2, u2, b, 0.0, lin2, last, c[0], cz2)
            v = v + off
            i = int(np.argmin(v))
            store[0] = dict(leaf=i, z=(z1[i], z2[i]), childcell=int(offarg[i]), L=L, U=U, off=off)
            return float(v[i]), size, pairs, store
        Pl, Pu = shell_partition(xc[t:t + 1], h, mu)
        size += len(Pl)
        plo, phi_ = Pl[:, 0], Pu[:, 0]
        bi, di = np.nonzero((plo[None, :] <= u1[:, None]) & (phi_[None, :] >= l1[:, None]))
        pairs += len(bi)
        A1, B1 = np.maximum(l1[bi], plo[di]), np.minimum(u1[bi], phi_[di])
        v, z1, z2 = min_pair(A1, B1, l1[bi], u1[bi], l2[bi], u2[bi], b, -slopes[t], lin2, last, c[t], cz2)
        v = v + off[bi]
        beta = np.full(len(plo), np.inf); arg = np.full(len(plo), -1)
        order = np.argsort(v)[::-1]                       # assign so that the smallest value wins
        beta[di[order]] = v[order]; arg[di[order]] = order
        child = (plo, phi_, beta)
        if keep:
            store[t] = dict(cells=(plo, phi_), beta=beta, arg=arg, bi=bi, z1=z1, z2=z2, L=L, U=U, offarg=offarg)


def trace(n, mu, j, b=0.8):
    c = np.zeros(n); xc = np.zeros(n); lam = np.zeros(n); h = 2.0 ** -j
    root, size, pairs, st = certificate(n, b, c, xc, h, mu, lam, keep=True)
    print("n=%d theta=2^-%d h=2^-%d: root l_r = %.6e, size = %d, (leaf,cell) pairs = %d" % (n, mu, j, root, size, pairs))
    r = st[0]
    leaves = [(r['L'][r['leaf']], r['U'][r['leaf']])]
    zs = [np.array(r['z'])]
    cells = [None]
    cell = r['childcell']
    for t in range(1, n - 1):
        s = st[t]
        q = s['arg'][cell]
        bi = s['bi'][q]
        cells.append((s['cells'][0][cell], s['cells'][1][cell]))
        leaves.append((s['L'][bi], s['U'][bi]))
        zs.append(np.array([s['z1'][q], s['z2'][q]]))
        cell = s['offarg'][bi] if t < n - 2 else -1
    # verify the configuration from scratch
    ok = True
    total = 0.0
    tol = 1e-12
    for t in range(n - 1):
        (Lb, Ub), z = leaves[t], zs[t]
        ok &= bool(np.all(z >= Lb - tol) and np.all(z <= Ub + tol))
        if t >= 1:
            dlo, dhi = cells[t]
            ok &= bool(dlo - tol <= z[0] <= dhi + tol)                        # z^t_{S_t} in D_t
            plo_, phi__ = leaves[t - 1][0][1], leaves[t - 1][1][1]           # parent leaf, coordinate t
            ok &= bool(max(dlo, plo_) <= min(dhi, phi__) + tol)              # D_t meets (B_p)_{S_t}
        last = t == n - 2
        total += float(bag_value(z[0], z[1], Lb[0], Ub[0], Lb[1], Ub[1], b, 0.0, 0.0, last, 0.0, 0.0))
    print("configuration checks pass: %s; recomputed configuration value = %.6e (difference to l_r %.1e)" % (ok, total, total - root))
    for t in range(n - 1):
        (Lb, Ub), z = leaves[t], zs[t]
        drift = abs(z[0] - zs[t - 1][1]) if t >= 1 else 0.0
        last = t == n - 2
        bv = float(bag_value(z[0], z[1], Lb[0], Ub[0], Lb[1], Ub[1], b, 0.0, 0.0, last, 0.0, 0.0))
        print("  bag %2d leaf [% .4f,% .4f]x[% .4f,% .4f] z=(% .4f,% .4f) drift %.4f bag value % .5f" % (
            t, Lb[0], Ub[0], Lb[1], Ub[1], z[0], z[1], drift, bv))


def gap(n, mu, j, b=0.8):
    c = np.zeros(n)
    r, size, pairs, _ = certificate(n, b, c, np.zeros(n), 2.0 ** -j, mu, np.zeros(n))
    return -r, size, pairs


def xstar_and_values(n, b, c, G=4001):
    """grid DP for x*, refined; V_t(s) = phi_t(s) on the grid (upper approximations)."""
    from scipy.optimize import minimize
    y = np.linspace(-1, 1, G)
    V = phi(y) + c[n - 1] * y
    Vs = {n - 1: V}
    args = {}
    for i in range(n - 2, -1, -1):
        M = (phi(y) + c[i] * y)[:, None] + b * y[:, None] * y[None, :] + V[None, :]
        args[i] = M.argmin(axis=1)
        V = M.min(axis=1)
        Vs[i] = V
    F = lambda x: float(np.sum(phi(x) + c * x) + b * np.sum(x[:-1] * x[1:]))
    def gF(x):
        g = dphi(x) + c; g[:-1] += b * x[1:]; g[1:] += b * x[:-1]; return g
    k = int(np.argmin(V)); path = [k]
    for i in range(n - 1):
        path.append(int(args[i][path[-1]]))
    r = minimize(F, y[path], jac=gF, bounds=[(-1, 1)] * n, method="L-BFGS-B", options={"ftol": 1e-16, "gtol": 1e-14})
    return r.x, r.fun, y, Vs, args, F


def phi_t_refined(t, s, n, b, c, y, Vs, args):
    """accurate phi_t(s): grid DP start for x_{t+1..n-1}, then L-BFGS-B on the subtree variables."""
    from scipy.optimize import minimize
    k = int(np.argmin(np.abs(y - s)))
    # best continuation from s on the grid
    vals = b * s * y + Vs[t + 1]
    path = [int(np.argmin(vals))]
    for i in range(t + 1, n - 1):
        path.append(int(args[i][path[-1]]))
    x0 = y[path]
    def fsub(x):
        xx = np.concatenate([[s], x])
        cc = c[t:]
        return float(np.sum(phi(xx) + cc * xx) + b * np.sum(xx[:-1] * xx[1:]))
    def gsub(x):
        xx = np.concatenate([[s], x]); cc = c[t:]
        g = dphi(xx) + cc; g[:-1] += b * xx[1:]; g[1:] += b * xx[:-1]
        return g[1:]
    r = minimize(fsub, x0, jac=gsub, bounds=[(-1, 1)] * len(x0), method="L-BFGS-B", options={"ftol": 1e-16, "gtol": 1e-14})
    return min(r.fun, fsub(x0))


def valid(n, seed, mu, j, b=0.8):
    c = np.random.default_rng(seed).uniform(-0.2, 0.2, n)
    xs, fs, y, Vs, args, F = xstar_and_values(n, b, c)
    lam = np.zeros(n)
    for t in range(1, n - 1):
        lam[t] = dphi(xs[t]) + c[t] + b * xs[t + 1]
    for name, sl in (("affine", lam), ("zero", np.zeros(n))):
        root, size, pairs, st = certificate(n, b, c, xs, 2.0 ** -j, mu, sl, keep=True)
        worst, worst_at = -np.inf, None
        npts = 0
        for t in range(1, n - 1):
            plo, phi_ = st[t]['cells']; beta = st[t]['beta']
            for D in range(len(plo)):
                # test points: both endpoints and midpoint of every cell, plus 3 interior points near x*
                pts = [plo[D], phi_[D], 0.5 * (plo[D] + phi_[D])]
                for s in pts:
                    val = sl[t] * s + beta[D] - phi_t_refined(t, s, n, b, c, y, Vs, args)
                    npts += 1
                    if val > worst:
                        worst, worst_at = val, (t, s)
        print("n=%d seed=%d theta=2^-%d h=2^-%d slopes=%s: f*=%.10f l_r=%.10f (l_r <= f*: %s), points=%d, max(l - phi_t) = %.3e at t=%d s=%.5f" % (
            n, seed, mu, j, name, fs, root, root <= fs + 1e-12, npts, worst, worst_at[0], worst_at[1]), flush=True)


def pairs_count(mu, js):
    for j in js:
        h = 2.0 ** -j
        L, U = shell_partition(np.zeros(2), h, mu)
        P, Pu = shell_partition(np.zeros(1), h, mu)
        m = (P[None, :, 0] <= U[:, None, 0]) & (Pu[None, :, 0] >= L[:, None, 0])
        per = m.sum(axis=1)
        print("theta=2^-%d h=2^-%2d: leaves %6d, cells %4d, pairs %7d, pairs/leaves %.2f, max cells per leaf %d" % (
            mu, j, len(L), len(P), int(m.sum()), m.sum() / len(L), per.max()), flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "gap":
        n, mu, j = map(int, sys.argv[2:5]); b = float(sys.argv[5]) if len(sys.argv) > 5 else 0.8
        g, s, p = gap(n, mu, j, b)
        print("n=%d theta=2^-%d h=2^-%d b=%.2f: gap %.4e size %d pairs %d" % (n, mu, j, b, g, s, p))
    elif cmd == "sweep":
        # usage: sweep j b n1,n2,.. mu1,mu2,..
        j = int(sys.argv[2]); b = float(sys.argv[3])
        ns = [int(a) for a in sys.argv[4].split(",")]; mus = [int(a) for a in sys.argv[5].split(",")]
        for mu in mus:
            row = []
            for n in ns:
                g, s, p = gap(n, mu, j, b)
                row.append("n=%d:%.3e" % (n, g))
            print("b=%.2f c_g=%.2f theta=2^-%d h=2^-%d  " % (b, 1 - KAPPA - b, mu, j) + " ".join(row), flush=True)
    elif cmd == "trace":
        n, mu, j = map(int, sys.argv[2:5]); trace(n, mu, j)
    elif cmd == "valid":
        n, seed, mu, j = map(int, sys.argv[2:6]); valid(n, seed, mu, j)
    elif cmd == "pairs":
        mu = int(sys.argv[2]); pairs_count(mu, [int(a) for a in sys.argv[3:]])
