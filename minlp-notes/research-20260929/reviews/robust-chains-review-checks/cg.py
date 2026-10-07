"""Reviewer's independent class-bound code (column generation) for path objectives.

Factor e on (x_e, x_{e+1}):  F_e(x, y) = sum_{i,j} C[i,j] x^i y^j + A_e(x) + B_e(y),
A_e, B_e piecewise polynomials of degree <= 3.  Split class: test functions per interior variable
(piecewise polynomials, the same at every interior variable).  LB_S(box) via LP over point columns:
  primal LP value  = an S-consistent family  -> UPPER bound on LB_S;
  duals -> split; sum of factor minima of the shifted factors -> LOWER bound on LB_S.
Factor minimization (different from the note's resultant method): exact in y (the shifted factor is a
piecewise polynomial of degree <= 3 in y for fixed x: endpoints + roots of the derivative), a grid of x
values, then bounded Brent refinement around the best grid minima.  Floating point.
"""
import numpy as np
from scipy.optimize import linprog, minimize_scalar
from scipy import sparse


class PP:
    """piecewise polynomial on [-1,1]; coefs ascending, padded to length 4."""

    def __init__(self, bps, coefs):
        self.bps = np.asarray(bps, float)
        self.c = np.array([np.pad(np.asarray(c, float), (0, 4 - len(c))) for c in coefs])

    @staticmethod
    def poly(c):
        return PP([-1.0, 1.0], [c])

    def __call__(self, x):
        x = np.asarray(x, float)
        k = np.clip(np.searchsorted(self.bps, x, side="right") - 1, 0, len(self.c) - 1)
        C = self.c[k]
        return C[..., 0] + x * (C[..., 1] + x * (C[..., 2] + x * C[..., 3]))

    def comb(self, terms):
        """sum_k w_k * PP_k  with self as the first term (weight 1); returns a PP on the union of breakpoints"""
        allpp = [(1.0, self)] + list(terms)
        bps = np.unique(np.concatenate([pp.bps for _, pp in allpp]))
        coefs = []
        for lo, hi in zip(bps[:-1], bps[1:]):
            mid = 0.5 * (lo + hi)
            c = np.zeros(4)
            for w, pp in allpp:
                k = min(np.searchsorted(pp.bps, mid) - 1, len(pp.c) - 1)
                c = c + w * pp.c[k]
            coefs.append(c)
        return PP(bps, coefs)


ZERO = PP.poly([0.0])


def _min_y(cy, Bp, ly, uy):
    """cy: (Nx, 4) coefficients in y from the coupling; Bp: PP in y. Returns (min over y, argmin) per row."""
    Nx = cy.shape[0]
    best = np.full(Nx, np.inf); arg = np.full(Nx, ly)
    for k in range(len(Bp.c)):
        lo, hi = max(ly, Bp.bps[k]), min(uy, Bp.bps[k + 1])
        if lo > hi:
            continue
        C = cy + Bp.c[k][None, :]
        cands = [np.full(Nx, lo), np.full(Nx, hi)]
        c1, c2, c3 = C[:, 1], 2 * C[:, 2], 3 * C[:, 3]
        with np.errstate(divide="ignore", invalid="ignore"):
            lin = np.abs(c3) < 1e-14
            r_lin = np.where(lin & (np.abs(c2) > 1e-300), -c1 / c2, lo)
            disc = c2 * c2 - 4 * c3 * c1
            sq = np.sqrt(np.maximum(disc, 0))
            r1 = np.where(lin, r_lin, (-c2 + sq) / (2 * c3))
            r2 = np.where(lin, r_lin, (-c2 - sq) / (2 * c3))
            ok = lin | (disc >= 0)
        for r in (r1, r2):
            r = np.where(ok & np.isfinite(r), np.clip(r, lo, hi), lo)
            cands.append(r)
        for yy in cands:
            v = C[:, 0] + yy * (C[:, 1] + yy * (C[:, 2] + yy * C[:, 3]))
            m = v < best
            best = np.where(m, v, best); arg = np.where(m, yy, arg)
    return best, arg


def _cy(Cmat, xs):
    """coefficients in y of sum C[i,j] x^i y^j for each x (padded to 4)."""
    out = np.zeros((len(xs), 4))
    for i in range(Cmat.shape[0]):
        xi = xs ** i
        for j in range(Cmat.shape[1]):
            if Cmat[i, j] != 0:
                out[:, j] += Cmat[i, j] * xi
    return out


def min_factor(Cmat, Ax, By, lx, ux, ly, uy, Nx=97):
    """min over [lx,ux]x[ly,uy] of sum C x^i y^j + Ax(x) + By(y)."""
    if ux - lx < 1e-15:
        xs = np.array([lx])
    else:
        xs = np.unique(np.concatenate([np.linspace(lx, ux, Nx), Ax.bps[(Ax.bps > lx) & (Ax.bps < ux)]]))
    prof = lambda X: _min_y(_cy(Cmat, X), By, ly, uy)
    v, ya = prof(xs)
    v = v + Ax(xs)
    k0 = int(np.argmin(v))
    best = (float(v[k0]), float(xs[k0]), float(ya[k0]))
    if len(xs) > 2:
        # refine around the 3 best local minima of the profile
        locmin = [k for k in range(len(xs)) if (k == 0 or v[k] <= v[k - 1]) and (k == len(xs) - 1 or v[k] <= v[k + 1])]
        locmin = sorted(locmin, key=lambda k: v[k])[:3]
        for k in locmin:
            a_, b_ = xs[max(k - 1, 0)], xs[min(k + 1, len(xs) - 1)]
            f1 = lambda X: float(prof(np.array([X]))[0][0] + Ax(np.array([X]))[0])
            r = minimize_scalar(f1, bounds=(a_, b_), method="bounded", options={"xatol": 1e-11})
            if r.fun < best[0]:
                yy = prof(np.array([r.x]))[1][0]
                best = (float(r.fun), float(r.x), float(yy))
    return best


class Chain:
    """factors e = 0..n-2: (Cmat, A_e, B_e)."""

    def __init__(self, factors):
        self.F = factors
        self.n = len(factors) + 1

    def value(self, x):
        return sum(float(_cy(C, np.array([x[e]]))[0] @ np.array([1, x[e + 1], x[e + 1] ** 2, x[e + 1] ** 3]))
                   + float(A(np.array([x[e]]))[0]) + float(B(np.array([x[e + 1]]))[0]) for e, (C, A, B) in enumerate(self.F))


class ClassBound:
    def __init__(self, chain, tests, K=5, Nx=97):
        self.ch, self.tests, self.K, self.Nx = chain, tests, K, Nx
        self.lpfail = 0

    def bound(self, l, u, target=None, maxit=150, tol=1e-9):
        n = self.ch.n; T = len(self.tests)
        pts = []
        for e in range(n - 1):
            gx = np.linspace(l[e], u[e], self.K); gy = np.linspace(l[e + 1], u[e + 1], self.K)
            pts.append({(float(a), float(b)) for a in gx for b in gy})
        row = lambda i, k: (n - 1) + (i - 1) * T + k
        nrow = (n - 1) + (n - 2) * T
        lower, upper = -np.inf, np.inf
        self.last = None
        for it in range(maxit):
            cost, I, J, V, Plist = [], [], [], [], []
            col = 0
            for e in range(n - 1):
                Pe = np.array(sorted(pts[e])); Plist.append(Pe)
                C, A, B = self.ch.F[e]
                xs, ys = Pe[:, 0], Pe[:, 1]
                cost.append(np.einsum("ij,ij->i", _cy(C, xs), np.stack([ys ** 0, ys, ys ** 2, ys ** 3], 1)) + A(xs) + B(ys))
                m = len(Pe); cols = np.arange(col, col + m)
                I.append(np.full(m, e)); J.append(cols); V.append(np.ones(m))
                if e + 1 <= n - 2:
                    for k, ph in enumerate(self.tests):
                        I.append(np.full(m, row(e + 1, k))); J.append(cols); V.append(ph(ys))
                if e >= 1:
                    for k, ph in enumerate(self.tests):
                        I.append(np.full(m, row(e, k))); J.append(cols); V.append(-ph(xs))
                col += m
            Amat = sparse.csr_matrix((np.concatenate(V), (np.concatenate(I), np.concatenate(J))), shape=(nrow, col))
            beq = np.zeros(nrow); beq[:n - 1] = 1.0
            res = linprog(np.concatenate(cost), A_eq=Amat, b_eq=beq, bounds=(0, None), method="highs")
            if res.status != 0:
                self.lpfail += 1
                return lower, upper, it
            if res.fun < upper:
                upper = res.fun
                self.last = (Plist, res.x.copy())
            yd = res.eqlin.marginals
            tot = 0.0; new = []
            for e in range(n - 1):
                C, A, B = self.ch.F[e]
                At, Bt = [], []
                if e + 1 <= n - 2:
                    Bt = [(-yd[row(e + 1, k)], ph) for k, ph in enumerate(self.tests)]
                if e >= 1:
                    At = [(yd[row(e, k)], ph) for k, ph in enumerate(self.tests)]
                As = A.comb(At); Bs = B.comb(Bt)
                v, xa, ya = min_factor(C, As, Bs, l[e], u[e], l[e + 1], u[e + 1], self.Nx)
                tot += v; new.append((xa, ya))
            lower = max(lower, tot)
            if (target is not None and (lower >= target or upper < target)) or upper - lower <= tol:
                return lower, upper, it + 1
            added = 0
            for e in range(n - 1):
                if new[e] not in pts[e]:
                    pts[e].add(new[e]); added += 1
            if added == 0:
                return lower, upper, it + 1
        return lower, upper, maxit

    def spread(self):
        Plist, w = self.last
        n = self.ch.n
        sc = np.zeros(n); col = 0
        for e in range(n - 1):
            Pe = Plist[e]; m = len(Pe)
            we = np.maximum(w[col:col + m], 0); col += m
            s = we.sum()
            if s <= 0:
                continue
            for j, k in ((0, e), (1, e + 1)):
                mu = we @ Pe[:, j] / s
                sc[k] += we @ (Pe[:, j] - mu) ** 2 / s
        return sc


def bb(cb, n, target, rule="bisect", maxnodes=200000):
    stack = [(np.full(n, -1.0), np.full(n, 1.0))]
    leaves = nodes = 0
    while stack:
        l, u = stack.pop(); nodes += 1
        lo, up, _ = cb.bound(l, u, target)
        if lo >= target:
            leaves += 1
            continue
        w = u - l
        if rule == "spread" and cb.last is not None:
            sc = cb.spread() * (w > 1e-9)
            j = int(np.argmax(sc)) if sc.max() > 1e-14 else int(np.argmax(w))
        else:
            j = int(np.argmax(w))
        m = 0.5 * (l[j] + u[j])
        u1 = u.copy(); u1[j] = m; l2 = l.copy(); l2[j] = m
        stack.append((l, u1)); stack.append((l2, u))
        if nodes > maxnodes:
            return None, nodes
    return leaves, nodes


# ------------------------------------------------------------------ families
def chiral_chain(n, b, g, ev):
    a = b + ev
    C = np.zeros((3, 3))
    C[2, 0] = a / 2; C[0, 2] = a / 2; C[1, 1] = b; C[1, 2] = g / 2; C[2, 1] = -g / 2
    F = []
    for e in range(n - 1):
        A = PP.poly([0, 0, a / 2]) if e == 0 else ZERO
        B = PP.poly([0, 0, a / 2]) if e == n - 2 else ZERO
        F.append((C, A, B))
    return Chain(F)


def poly_tests(d):
    return [PP.poly(np.eye(k + 1)[k]) for k in range(1, d + 1)]


def ud_u():
    return PP([-1.0, 0.3, 0.6, 1.0], [[0.168, -1.44, 3.0], [-0.237, 1.26, -1.5], [1.023, -2.94, 2.0]])


def uniform_chain(n, u, b, base="balanced"):
    C = np.zeros((2, 2)); C[1, 1] = b
    F = []
    for e in range(n - 1):
        if base == "balanced":
            wa = 1.0 if e == 0 else 0.5
            wb = 1.0 if e == n - 2 else 0.5
        else:  # unsplit
            wa = 1.0
            wb = 1.0 if e == n - 2 else 0.0
        F.append((C, ZERO.comb([(wa, u)]), ZERO.comb([(wb, u)])))
    return Chain(F)
