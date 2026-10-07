"""Class bounds (Lemma 1.2 of robust-lower-bound.md) for path objectives with polynomial bond factors.

f(x) = sum_{e=0}^{n-2} W(x_e, x_{e+1}) + uL(x_0) + uR(x_{n-1}),   x in a box of [-1,1]^n,
with W a bivariate polynomial (2D coefficient array C[i, j] for x^i y^j), uL, uR univariate
polynomials added to the first and last factor.  A split class is given by univariate polynomial test
functions (the same at every interior variable).  LB_S(A) is computed by column generation:
  * primal LP over finitely many points per factor -> an S-consistent family, UPPER bound on LB_S;
  * LP duals -> a split r in S; sum_e min_{A_e} (shifted factor) is a LOWER bound on LB_S, with the
    factor minima found from critical points (corners, edges, and interior points from a resultant),
    plus a small grid as a safeguard.  Floating point, not interval arithmetic.
"""
import time
import numpy as np
from numpy.polynomial import polynomial as P
from numpy.polynomial import chebyshev as Cb
from scipy.optimize import linprog
from scipy import sparse


# ---------------------------------------------------------------- bivariate polynomial minimization
def _uroots(c, lo, hi):
    c = np.trim_zeros(np.asarray(c, float), "b")
    if len(c) <= 1:
        return []
    if np.max(np.abs(c[1:])) < 1e-14 * max(1.0, abs(c[0])):
        return []
    r = np.roots(c[::-1])
    return [z.real for z in r if abs(z.imag) < 1e-7 * max(1.0, abs(z)) and lo <= z.real <= hi]


def _dx(C):
    return np.array([[i * C[i, j] for j in range(C.shape[1])] for i in range(1, C.shape[0])]).reshape(C.shape[0] - 1, C.shape[1]) if C.shape[0] > 1 else np.zeros((1, C.shape[1]))


def _dy(C):
    return _dx(C.T).T


def _in_y(C, x):
    """coefficients in y of C(x, y)"""
    return np.array([P.polyval(x, C[:, j]) for j in range(C.shape[1])])


def _in_x(C, y):
    return _in_y(C.T, y)


def _sylvester_det(p, q):
    p = np.trim_zeros(np.asarray(p, float), "b"); q = np.trim_zeros(np.asarray(q, float), "b")
    m, k = len(p) - 1, len(q) - 1
    if m < 0 or k < 0:
        return 0.0
    if m == 0:
        return p[0] ** k
    if k == 0:
        return q[0] ** m
    N = m + k
    S = np.zeros((N, N))
    for i in range(k):
        S[i, i:i + m + 1] = p[::-1]
    for i in range(m):
        S[k + i, i:i + k + 1] = q[::-1]
    return np.linalg.det(S)


def _interior_crit(C, lx, ux, ly, uy):
    Px, Py = _dx(C), _dy(C)
    degx = (Px.shape[0] - 1) * (Py.shape[1] - 1) + (Py.shape[0] - 1) * (Px.shape[1] - 1) + 2
    N = max(degx + 4, 8)
    k = np.arange(N)
    xs = 0.5 * (lx + ux) + 0.5 * (ux - lx) * np.cos(np.pi * (k + 0.5) / N)
    vals = np.array([_sylvester_det(_in_y(Px, x), _in_y(Py, x)) for x in xs])
    out = []
    if np.max(np.abs(vals)) < 1e-300:
        return out
    t = (2 * xs - (lx + ux)) / (ux - lx)
    cc = Cb.chebfit(t, vals / np.max(np.abs(vals)), degx)
    cc[np.abs(cc) < 1e-12 * np.max(np.abs(cc))] = 0.0
    try:
        rt = Cb.chebroots(cc)
    except np.linalg.LinAlgError:
        rt = []
    for z in rt:
        if abs(z.imag) > 1e-6 or not (-1 - 1e-9 <= z.real <= 1 + 1e-9):
            continue
        x0 = 0.5 * (lx + ux) + 0.5 * (ux - lx) * z.real
        for y0 in _uroots(_in_y(Px, x0), ly, uy) + _uroots(_in_y(Py, x0), ly, uy):
            out.append((x0, y0))
    return out


def _newton(C, x, y, lx, ux, ly, uy, it=8):
    Px, Py = _dx(C), _dy(C)
    Pxx, Pxy, Pyy = _dx(Px), _dy(Px), _dy(Py)
    for _ in range(it):
        g = np.array([P.polyval2d(x, y, Px), P.polyval2d(x, y, Py)])
        H = np.array([[P.polyval2d(x, y, Pxx), P.polyval2d(x, y, Pxy)], [P.polyval2d(x, y, Pxy), P.polyval2d(x, y, Pyy)]])
        try:
            d = np.linalg.solve(H, g)
        except np.linalg.LinAlgError:
            break
        x, y = x - d[0], y - d[1]
        if not (lx <= x <= ux and ly <= y <= uy):
            return None
        if np.max(np.abs(d)) < 1e-14:
            break
    return (x, y)


def min_bivar(C, lx, ux, ly, uy, ngrid=9):
    """Global minimum of the bivariate polynomial C over [lx,ux]x[ly,uy] (floating point)."""
    cands = [(x, y) for x in (lx, ux) for y in (ly, uy)]
    for x in (lx, ux):
        cands += [(x, y) for y in _uroots(P.polyder(_in_y(C, x)), ly, uy)]
    for y in (ly, uy):
        cands += [(x, y) for x in _uroots(P.polyder(_in_x(C, y)), lx, ux)]
    if ux > lx and uy > ly:
        for (x0, y0) in _interior_crit(C, lx, ux, ly, uy):
            p = _newton(C, x0, y0, lx, ux, ly, uy, it=4)
            cands.append(p if p is not None else (x0, y0))
        gx = np.linspace(lx, ux, ngrid); gy = np.linspace(ly, uy, ngrid)
        X, Y = np.meshgrid(gx, gy, indexing="ij")
        V = P.polyval2d(X, Y, C)
        k = np.unravel_index(np.argmin(V), V.shape)
        p = _newton(C, gx[k[0]], gy[k[1]], lx, ux, ly, uy)
        cands.append((gx[k[0]], gy[k[1]]))
        if p is not None:
            cands.append(p)
    xs = np.array([c[0] for c in cands]); ys = np.array([c[1] for c in cands])
    vals = P.polyval2d(xs, ys, C)
    order = np.argsort(vals)
    v = float(vals[order[0]])
    return v, [cands[k] for k in order[:3] if vals[k] <= v + 1e-12]


# ---------------------------------------------------------------- chain and relaxation
def bivar(coefs):
    """dict {(i,j): c} -> 2D array"""
    dx = max(i for i, _ in coefs) + 1; dy = max(j for _, j in coefs) + 1
    C = np.zeros((max(dx, 1), max(dy, 1)))
    for (i, j), c in coefs.items():
        C[i, j] += c
    return C


def add_x(C, p):
    p = np.asarray(p, float)
    D = np.zeros((max(C.shape[0], len(p)), C.shape[1])); D[:C.shape[0], :C.shape[1]] = C
    D[:len(p), 0] += p
    return D


def add_y(C, p):
    return add_x(C.T, p).T


class PolyChain:
    def __init__(self, n, W, uL, uR):
        self.n, self.W = n, np.asarray(W, float)
        self.uL, self.uR = np.asarray(uL, float), np.asarray(uR, float)

    def factor(self, e):
        C = self.W.copy()
        if e == 0:
            C = add_x(C, self.uL)
        if e == self.n - 2:
            C = add_y(C, self.uR)
        return C

    def f(self, x):
        x = np.asarray(x, float)
        v = float(np.sum(P.polyval2d(x[:-1], x[1:], self.W)))
        return v + float(P.polyval(x[0], self.uL)) + float(P.polyval(x[-1], self.uR))


def poly_class(d):
    return [np.eye(k + 1)[k] for k in range(1, d + 1)]


class RelaxPoly:
    def __init__(self, chain, phis, K=5):
        self.ch, self.phis, self.K = chain, [np.asarray(p, float) for p in phis], K
        self.failures = 0

    def bound(self, l, u, target, maxit=80, tol=1e-9):
        n = self.ch.n; nphi = len(self.phis)
        facs = [self.ch.factor(e) for e in range(n - 1)]
        pts = []
        for e in range(n - 1):
            gx = np.linspace(l[e], u[e], self.K); gy = np.linspace(l[e + 1], u[e + 1], self.K)
            pts.append({(float(x), float(y)) for x in gx for y in gy})
        ninter = n - 2
        nrow = (n - 1) + ninter * nphi
        row = lambda i, k: (n - 1) + (i - 1) * nphi + k
        lower, upper = -np.inf, np.inf
        for it in range(maxit):
            cost, I, J, V = [], [], [], []
            col = 0
            Plist = []
            for e in range(n - 1):
                Pe = np.array(sorted(pts[e])); Plist.append(Pe)
                xs, ys = Pe[:, 0], Pe[:, 1]
                cost.append(P.polyval2d(xs, ys, facs[e]))
                m = len(Pe); cols = np.arange(col, col + m)
                I.append(np.full(m, e)); J.append(cols); V.append(np.ones(m))
                if 1 <= e + 1 <= n - 2:
                    for k, ph in enumerate(self.phis):
                        I.append(np.full(m, row(e + 1, k))); J.append(cols); V.append(P.polyval(ys, ph))
                if 1 <= e <= n - 2:
                    for k, ph in enumerate(self.phis):
                        I.append(np.full(m, row(e, k))); J.append(cols); V.append(-P.polyval(xs, ph))
                col += m
            A = sparse.csr_matrix((np.concatenate(V), (np.concatenate(I), np.concatenate(J))), shape=(nrow, col))
            beq = np.zeros(nrow); beq[: n - 1] = 1.0
            res = linprog(np.concatenate(cost), A_eq=A, b_eq=beq, bounds=(0, None), method="highs")
            if res.status != 0 or res.eqlin is None or res.eqlin.marginals is None:
                self.failures += 1
                return lower, upper, it + 1
            if res.fun < upper:
                upper = res.fun
                self.last_primal = (Plist, res.x.copy())
            y = res.eqlin.marginals
            tot = 0.0; newpts = []
            split = []
            for e in range(n - 1):
                C = facs[e]
                if 1 <= e + 1 <= n - 2:
                    for k, ph in enumerate(self.phis):
                        C = add_y(C, -y[row(e + 1, k)] * ph)
                if 1 <= e <= n - 2:
                    for k, ph in enumerate(self.phis):
                        C = add_x(C, y[row(e, k)] * ph)
                v, arg = min_bivar(C, l[e], u[e], l[e + 1], u[e + 1])
                tot += v; newpts.append(arg); split.append(C)
            if tot > lower:
                lower = tot; self.last_split = split
            if (target is not None and (lower >= target or upper < target)) or upper - lower <= tol:
                return lower, upper, it + 1
            added = 0
            for e in range(n - 1):
                for p in newpts[e]:
                    p = (float(p[0]), float(p[1]))
                    if p not in pts[e]:
                        pts[e].add(p); added += 1
            if added == 0:
                return lower, upper, it + 1
        return lower, upper, maxit


def spread_scores(rel, n):
    pts, w = rel.last_primal
    score = np.zeros(n); col = 0
    for e in range(n - 1):
        Pe = pts[e]; m = len(Pe)
        we = np.maximum(w[col:col + m], 0.0); col += m
        s = we.sum()
        if s <= 0:
            continue
        for j, k in ((0, e), (1, e + 1)):
            mu = np.dot(we, Pe[:, j]) / s
            score[k] += np.dot(we, (Pe[:, j] - mu) ** 2) / s
    return score


def bb(chain, phis, eps, fstar, rule="bisect", maxnodes=400_000, K=5, timelimit=7200):
    n = chain.n
    rel = RelaxPoly(chain, phis, K)
    target = fstar - eps
    stack = [(np.full(n, -1.0), np.full(n, 1.0))]
    leaves = nodes = ambiguous = 0
    t0 = time.time()
    while stack:
        l, u = stack.pop()
        nodes += 1
        lo, up, _ = rel.bound(l, u, target)
        if lo >= target:
            leaves += 1
            continue
        if up >= target:
            ambiguous += 1
        width = u - l
        if rule == "spread" and hasattr(rel, "last_primal"):
            sc = spread_scores(rel, n) * (width > 1e-9)
            j = int(np.argmax(sc)) if sc.max() > 1e-14 else int(np.argmax(width))
        else:
            j = int(np.argmax(width))
        m = 0.5 * (l[j] + u[j])
        u1 = u.copy(); u1[j] = m
        l2 = l.copy(); l2[j] = m
        stack.append((l, u1)); stack.append((l2, u))
        if nodes > maxnodes or time.time() - t0 > timelimit:
            return dict(leaves=None, nodes=nodes, aborted=True, time=round(time.time() - t0, 1))
    return dict(leaves=leaves, nodes=nodes, ambiguous=ambiguous, lpfail=rel.failures, time=round(time.time() - t0, 1))


if __name__ == "__main__":
    # self-test of min_bivar against a dense grid on random cubic/quartic polynomials
    rng = np.random.default_rng(0)
    worst = 0.0
    for trial in range(300):
        C = rng.normal(size=(4, 4)) * (np.add.outer(np.arange(4), np.arange(4)) <= 4)
        lx, ly = rng.uniform(-1, 0.5, 2); ux, uy = lx + rng.uniform(0.05, 1.0), ly + rng.uniform(0.05, 1.0)
        v, _ = min_bivar(C, lx, ux, ly, uy)
        gx = np.linspace(lx, ux, 801); gy = np.linspace(ly, uy, 801)
        X, Y = np.meshgrid(gx, gy, indexing="ij")
        vg = P.polyval2d(X, Y, C).min()
        worst = max(worst, v - vg)
    print("min_bivar self-test: max (claimed min - grid min) over 300 random quartics =", worst)
