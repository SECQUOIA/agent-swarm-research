"""Single-tree spatial B&B on a path with per-factor convex envelopes and split classes.

Objective  f(x) = sum_i u_i(x_i) + sum_e b_e x_e x_{e+1}   on [-1,1]^n,  u_i piecewise polynomials.
Factor e = (e, e+1), e = 0..n-2.  Base split: balanced (interior u_i half to each factor, u_0 and
u_{n-1} wholly to the end factors) or 'unsplit' (u_e to factor e, u_{n-1} to the last factor).

Relaxation of a box A for a split class with test functions Phi_i (per interior coordinate i):
    LB_Phi(A) = sup_{rho_i in span Phi_i} sum_e min_{A_e} (f_e + rho_{e+1} - rho_e)
              = min { sum_e int f_e dnu_e : nu_e prob. on A_e,
                      int phi dnu_{e-1}^{(i)} = int phi dnu_e^{(i)} for phi in Phi_i }
(Lemma 2 of robust-lower-bound.md; with Phi_i = {x} this is the per-factor envelope bound of the
base split).  Computed by column generation:
  * primal LP over finitely many points per factor: an UPPER bound on LB_Phi (a fooling value);
  * LP duals give a split rho; sum_e exact min_{A_e} (f_e + rho_{e+1} - rho_e) is a LOWER bound
    (floating-point exact: critical points of the polynomial pieces, edges, corners);
  * the argmin points are added as columns.
Stop when lower >= target (box valid), upper < target (box certainly invalid), or the gap is small.

Classes: env (Phi = {x}, base split fixed), a (x, x^2, u_i), a0 (x, u_i), bD (x, ..., x^D).
Floating-point illustration, not a certified count.
"""
import sys
import time
import numpy as np
from numpy.polynomial import polynomial as P
from scipy.optimize import linprog
from scipy import sparse


class PW:
    """Piecewise polynomial on [-1,1]: breakpoints -1 = t0 < ... < tk = 1, coefficient arrays."""

    def __init__(self, bps, coefs):
        self.bps = np.array(bps, float)
        self.coefs = [np.array(c, float) for c in coefs]

    @staticmethod
    def poly(c):
        return PW([-1.0, 1.0], [c])

    def __call__(self, x):
        x = np.asarray(x, float)
        idx = np.clip(np.searchsorted(self.bps, x, side="right") - 1, 0, len(self.coefs) - 1)
        out = np.zeros_like(x)
        for k, c in enumerate(self.coefs):
            m = idx == k
            if np.any(m):
                out[m] = P.polyval(x[m], c)
        return out if out.ndim else float(out)

    def lin(self, a, other=None, b=0.0):
        """a*self + b*other (other PW or poly coef array)."""
        if other is None:
            return PW(self.bps, [a * c for c in self.coefs])
        if not isinstance(other, PW):
            other = PW.poly(other)
        bps = np.union1d(self.bps, other.bps)
        coefs = []
        for lo, hi in zip(bps[:-1], bps[1:]):
            mid = 0.5 * (lo + hi)
            c1 = self.coefs[min(np.searchsorted(self.bps, mid) - 1, len(self.coefs) - 1)]
            c2 = other.coefs[min(np.searchsorted(other.bps, mid) - 1, len(other.coefs) - 1)]
            coefs.append(P.polyadd(a * c1, b * c2))
        return PW(bps, coefs)

    def pieces(self, lo, hi):
        out = []
        for k, c in enumerate(self.coefs):
            a, b = max(lo, self.bps[k]), min(hi, self.bps[k + 1])
            if a <= b:
                out.append((a, b, c))
        return out

    def is_poly_deg(self, d):
        return len(self.coefs) == 1 and len(np.trim_zeros(self.coefs[0], "b")) <= d + 1


class Family:
    def __init__(self, u, b):
        self.u = [ui if isinstance(ui, PW) else PW.poly(ui) for ui in u]
        self.b = np.array(b, float)
        self.n = len(self.u)

    def f(self, x):
        return sum(self.u[i](x[i]) for i in range(self.n)) + float(np.sum(self.b * x[:-1] * x[1:]))


def program_family(n, kappa=0.1, b=0.8, c=None):
    c = np.zeros(n) if c is None else c
    return Family([[0.0, c[i], 1.0, 0.0, -kappa] for i in range(n)], [b] * (n - 1))


def bangbang_uz(y1, eta):
    """Conjugate realisation of h2(y) = -eta y^2 - (1-eta)(|y|-y1)_+^2 with coupling bp y z on |z|<=1."""
    bp = 2 * eta + 2 * (1 - eta) * (1 - y1)
    z1 = 2 * eta * y1 / bp
    k = 2 * (1 - eta) * y1
    right = np.array([k * k / 4 - (1 - eta) * y1 * y1, bp * k / 2, bp * bp / 4])
    left = np.array([right[0], -right[1], right[2]])
    mid = np.array([0.0, 0.0, bp * bp / (4 * eta)])
    return PW([-1.0, -z1, z1, 1.0], [left, mid, right]), bp


def gadget_chain(G, y1=0.38, eta=0.05, epsf=0.02, delta=0.0):
    """G gadgets (x,y,z): y1^2 x^2 + 2 y1 x y + c y^2 + uz(z) + bp y z, c = 1 + eta + epsf;
    consecutive gadgets coupled by delta z_g x_{g+1}.  Unique minimiser 0 for small delta."""
    uz, bp = bangbang_uz(y1, eta)
    c = 1 + eta + epsf
    u, bs = [], []
    for g in range(G):
        u += [PW.poly([0.0, 0.0, y1 * y1]), PW.poly([0.0, 0.0, c]), uz]
        bs += [2 * y1, bp]
        if g < G - 1:
            bs += [delta]
    return Family(u, bs)


def test_funcs(cls, u_i):
    x = PW.poly([0.0, 1.0])
    if cls == "env":
        return [x]
    if cls == "a":
        out = [x, PW.poly([0.0, 0.0, 1.0])]
        if not u_i.is_poly_deg(2):
            out.append(u_i)
        return out
    if cls == "a0":
        return [x] + ([] if u_i.is_poly_deg(1) else [u_i])
    if cls.startswith("b"):
        d = int(cls[1:])
        return [PW.poly(np.eye(k + 1)[k]) for k in range(1, d + 1)]
    raise ValueError(cls)


def base_weights(n, base):
    """w[e] = (weight of u_e in factor e, weight of u_{e+1} in factor e).
    balanced: interior u_i half to each factor; unsplit: u_e to factor e;
    gadget (chains, n = 3G): all unary terms in the gadget factors, as in Theorems 4.2-4.3:
    (x_g, y_g) gets u(x_g) and half of c y_g^2, (y_g, z_g) gets the other half and u(z_g),
    the connecting factor (z_g, x_{g+1}) gets no unary term."""
    w = []
    for e in range(n - 1):
        if base == "balanced":
            a = 1.0 if e == 0 else 0.5
            c = 1.0 if e == n - 2 else 0.5
        elif base == "gadget":
            assert n % 3 == 0
            a, c = [(1.0, 0.5), (0.5, 1.0), (0.0, 0.0)][e % 3]
        else:
            a = 1.0
            c = 1.0 if e == n - 2 else 0.0
        w.append((a, c))
    return w


def _real_roots(c, lo, hi):
    c = np.trim_zeros(np.asarray(c, float), "b")
    if len(c) <= 1:
        return []
    r = np.roots(c[::-1])
    return [z.real for z in r if abs(z.imag) < 1e-7 and lo < z.real < hi]


def min_poly_factor(pa, pb, bb, lx, ux, ly, uy):
    """Candidate minimisers of pa(x) + pb(y) + bb x y over [lx,ux]x[ly,uy] (polynomials)."""
    cands = [(x, y) for x in (lx, ux) for y in (ly, uy)]
    for x in (lx, ux):
        for r in _real_roots(P.polyder(P.polyadd(pb, [0.0, bb * x])), ly, uy):
            cands.append((x, r))
    for y in (ly, uy):
        for r in _real_roots(P.polyder(P.polyadd(pa, [0.0, bb * y])), lx, ux):
            cands.append((r, y))
    da, db = P.polyder(pa), P.polyder(pb)
    if bb == 0:
        for xr in _real_roots(da, lx, ux):
            for yr in _real_roots(db, ly, uy):
                cands.append((xr, yr))
    else:
        ypoly = -np.asarray(da, float) / bb
        comp = np.zeros(1)
        for k, ck in enumerate(db):
            comp = P.polyadd(comp, ck * P.polypow(ypoly, k) if k > 0 else [ck])
        comp = P.polyadd(comp, [0.0, bb])
        for xr in _real_roots(comp, lx, ux):
            yr = P.polyval(xr, ypoly)
            if ly < yr < uy:
                cands.append((xr, yr))
    return cands


def min_factor(A, B, bb, lx, ux, ly, uy):
    cands = []
    for (ax, bx, ca) in A.pieces(lx, ux):
        for (ay, by, cb) in B.pieces(ly, uy):
            cands += min_poly_factor(ca, cb, bb, ax, bx, ay, by)
    gx = np.linspace(lx, ux, 7); gy = np.linspace(ly, uy, 7)
    cands += [(x, y) for x in gx for y in gy]
    xs = np.array([c[0] for c in cands]); ys = np.array([c[1] for c in cands])
    vals = A(xs) + B(ys) + bb * xs * ys
    j = int(np.argmin(vals)); v = float(vals[j])
    arg = [cands[k] for k in np.argsort(vals)[:3] if vals[k] <= v + 1e-12]
    return v, arg


class Relax:
    def __init__(self, fam, cls, base="balanced", K=5):
        self.fam, self.cls, self.K = fam, cls, K
        n = fam.n
        self.w = base_weights(n, base)
        self.phi = {i: test_funcs(cls, fam.u[i]) for i in range(1, n - 1)}
        self.failures = 0

    def factor_parts(self, e):
        a, c = self.w[e]
        return self.fam.u[e].lin(a), self.fam.u[e + 1].lin(c), self.fam.b[e]

    def bound(self, l, u, target, maxit=80, tol=1e-9):
        """Returns (lower, upper, iterations)."""
        n = self.fam.n
        parts = [self.factor_parts(e) for e in range(n - 1)]
        pts = []
        for e in range(n - 1):
            gx = np.linspace(l[e], u[e], self.K); gy = np.linspace(l[e + 1], u[e + 1], self.K)
            pts.append({(float(x), float(y)) for x in gx for y in gy})
        rows = [(i, k) for i in range(1, n - 1) for k in range(len(self.phi[i]))]
        rindex = {r: j for j, r in enumerate(rows)}
        nrow = (n - 1) + len(rows)
        lower, upper = -np.inf, np.inf
        for it in range(maxit):
            cost, I, J, V = [], [], [], []
            col = 0
            for e in range(n - 1):
                A, B, bb = parts[e]
                P_e = np.array(sorted(pts[e]))
                xs, ys = P_e[:, 0], P_e[:, 1]
                cost.append(A(xs) + B(ys) + bb * xs * ys)
                m = len(P_e); cols = np.arange(col, col + m)
                I.append(np.full(m, e)); J.append(cols); V.append(np.ones(m))
                if 1 <= e + 1 <= n - 2:
                    for k, ph in enumerate(self.phi[e + 1]):
                        I.append(np.full(m, (n - 1) + rindex[(e + 1, k)])); J.append(cols); V.append(ph(ys))
                if 1 <= e <= n - 2:
                    for k, ph in enumerate(self.phi[e]):
                        I.append(np.full(m, (n - 1) + rindex[(e, k)])); J.append(cols); V.append(-ph(xs))
                col += m
            Amat = sparse.csr_matrix((np.concatenate(V), (np.concatenate(I), np.concatenate(J))), shape=(nrow, col))
            beq = np.zeros(nrow); beq[: n - 1] = 1.0
            res = linprog(np.concatenate(cost), A_eq=Amat, b_eq=beq, bounds=(0, None), method="highs")
            if res.status != 0 or res.eqlin is None or res.eqlin.marginals is None:
                self.failures += 1
                return lower, upper, it + 1
            if res.fun < upper:
                upper = res.fun
                self.last_primal = ([np.array(sorted(p)) for p in pts], res.x.copy())
            y = res.eqlin.marginals
            tot = 0.0; newpts = []; shifted = []
            for e in range(n - 1):
                A, B, bb = parts[e]
                if 1 <= e + 1 <= n - 2:
                    for k, ph in enumerate(self.phi[e + 1]):
                        B = B.lin(1.0, ph, -y[(n - 1) + rindex[(e + 1, k)]])
                if 1 <= e <= n - 2:
                    for k, ph in enumerate(self.phi[e]):
                        A = A.lin(1.0, ph, y[(n - 1) + rindex[(e, k)]])
                v, arg = min_factor(A, B, bb, l[e], u[e], l[e + 1], u[e + 1])
                tot += v; newpts.append(arg)
                shifted.append((A, B, bb))
            self._shifted = shifted
            if tot > lower:
                lower = tot
                self.last_split = [(A_, B_, bb_, l[e_], u[e_], l[e_ + 1], u[e_ + 1]) for e_, (A_, B_, bb_) in enumerate(self._shifted)]
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


def bb(fam, cls, eps, base="balanced", fstar=0.0, maxnodes=500_000, K=5, record=None, record_split=None):
    n = fam.n
    rel = Relax(fam, cls, base, K)
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
            if record is not None:
                record.append((l.copy(), u.copy(), rel.last_split, lo))
            continue
        if up >= target:
            ambiguous += 1
        elif record_split is not None:
            record_split.append((l.copy(), u.copy(), rel.last_primal, up))
        j = int(np.argmax(u - l))
        m = 0.5 * (l[j] + u[j])
        u1 = u.copy(); u1[j] = m
        l2 = l.copy(); l2[j] = m
        stack.append((l, u1)); stack.append((l2, u))
        if nodes > maxnodes:
            return dict(leaves=None, nodes=nodes, aborted=True)
    return dict(leaves=leaves, nodes=nodes, ambiguous=ambiguous, lpfail=rel.failures, time=round(time.time() - t0, 1))


if __name__ == "__main__":
    # usage: python3 robust_bb.py chain CLS EPS DELTA G1 G2 ...   (gadget chains, y1=.38 eta=.05 eps_f=.02,
    #        theorem base split 'gadget')
    #        python3 robust_bb.py program CLS BASE EPS KAPPA B n1 n2 ...
    kind = sys.argv[1]
    if kind == "chain":
        cls, eps, delta = sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
        for G in map(int, sys.argv[5:]):
            fam = gadget_chain(G, delta=delta)
            r = bb(fam, cls, eps, base="gadget")
            print(f"chain cls={cls} eps={eps} delta={delta} G={G} n={3*G} {r}", flush=True)
    else:
        cls, base, eps, kappa, b = sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6])
        for n in map(int, sys.argv[7:]):
            r = bb(program_family(n, kappa, b), cls, eps, base)
            print(f"program cls={cls} base={base} kappa={kappa} b={b} eps={eps} n={n} {r}", flush=True)
