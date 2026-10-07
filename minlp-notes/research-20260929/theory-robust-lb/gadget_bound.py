"""Product lower bound for chains of 3-variable gadgets (Theorem 3 of robust-lower-bound.md).

Gadget  f(x,y,z) = ux(x) + b x y + c y^2 + uz(z) + bp y z  on [-1,1]^3, f* = 0 at the origin.
All quantities reduce to one-dimensional computations:

* core gap gamma(K): K = [-kx,kx]x[-ky,ky]x[-kz,kz]; h1(y) = min_{|x|<=kx} ux + b x y,
  h2(y) = min_{|z|<=kz} uz + bp y z, k_i(s) = h_i(sqrt s); the symmetric fooling pair gives
  LB_S(K) <= min_p [vex k1(p) + vex k2(p) + c p]  (convex envelopes on [0, ky^2]),
  valid for split classes (a) and (b_d), d <= 3.  gamma(K) = -that value (explicit fooling, so a
  valid lower bound on the true gap).
* Psi(mu) = sup over boxes B not containing the smallest core of vol(B) exp(mu min_B f),
  bounded with a grid sandwich (inner/outer grid intervals) and the separable form
  min_B f <= e^{..}: for y0 in B_y, min_B f <= min_{B_x}(ux + b x y0) + c y0^2 + min_{B_z}(uz + bp y0 z).
* Phi(mu) = max(Psi(mu), max_i (1 - tau_{i+1}) e^{-mu gamma_i}, e^{-mu gamma_last});
  N >= exp(-mu eps') Phi(mu)^(-G).
"""
import sys
import numpy as np

FINE = 40          # fine points per coarse cell


class Gadget:
    def __init__(self, ux, uz, b, c, bp, name=""):
        self.ux, self.uz, self.b, self.c, self.bp, self.name = ux, uz, b, c, bp, name

    def f(self, x, y, z):
        return self.ux(x) + self.b * x * y + self.c * y * y + self.uz(z) + self.bp * y * z


def lower_hull_vals(s, v):
    """Lower convex envelope of points (s_i, v_i) (s increasing), evaluated at s."""
    hull = []
    for i in range(len(s)):
        while len(hull) >= 2:
            i1, i2 = hull[-2], hull[-1]
            if (v[i2] - v[i1]) * (s[i] - s[i1]) >= (v[i] - v[i1]) * (s[i2] - s[i1]):
                hull.pop()
            else:
                break
        hull.append(i)
    return np.interp(s, s[hull], v[hull])


def core_gap(g, kx, ky, kz, ns=4001, nx=8001):
    """gamma(K) from the symmetric fooling pair (a valid fooling: all points lie in K)."""
    s = np.linspace(0.0, ky * ky, ns)
    y = np.sqrt(s)
    xs = np.linspace(-kx, kx, nx)
    zs = np.linspace(-kz, kz, nx)
    ux, uz = g.ux(xs), g.uz(zs)
    k1 = np.array([np.min(ux + g.b * xs * yy) for yy in y])
    k2 = np.array([np.min(uz + g.bp * zs * yy) for yy in y])
    R = lower_hull_vals(s, k1) + lower_hull_vals(s, k2) + g.c * s
    j = int(np.argmin(R))
    return -R[j], s[j]


class PsiEval:
    """Upper bound on Psi_K(mu) = sup_{B subset [-1,1]^3, B not containing K} vol(B) e^{mu min_B f}."""

    def __init__(self, g, N=80):
        self.g, self.N = g, N
        self.t = np.linspace(-1, 1, N + 1)
        self.h = 2.0 / N
        nf = N * FINE + 1
        self.xf = np.linspace(-1, 1, nf)
        self.uxf = g.ux(self.xf)
        self.uzf = g.uz(self.xf)
        self.y0 = self.t.copy()   # y0 candidates = grid points
        # for each y0: phi_x(inner interval [t_i,t_j]) = min over fine points in [t_i,t_j]
        # computed via cell minima + range-min over cells, plus the grid points themselves
        self.fx = [self._interval_min_table(self.uxf + g.b * self.xf * y0) for y0 in self.y0]
        self.fz = [self._interval_min_table(self.uzf + g.bp * self.xf * y0) for y0 in self.y0]
        self.fxmax = [np.max(self.uxf + g.b * self.xf * y0) for y0 in self.y0]
        self.fzmax = [np.max(self.uzf + g.bp * self.xf * y0) for y0 in self.y0]

    def _interval_min_table(self, vals):
        """M[i,j] = min of vals over fine points in [t_i, t_j] (i<=j); an upper bound on the
        true minimum over any interval containing [t_i,t_j]."""
        N = self.N
        cell = vals[:-1].reshape(N, FINE).min(axis=1)       # cell k covers [t_k, t_{k+1})
        cell = np.minimum(cell, vals[FINE::FINE])            # include right endpoint
        M = np.full((N + 1, N + 1), np.inf)
        for i in range(N + 1):
            M[i, i] = vals[i * FINE]
            cur = vals[i * FINE]
            for j in range(i + 1, N + 1):
                cur = min(cur, cell[j - 1])
                M[i, j] = cur
        return M

    def _sup_1d(self, M, fmax, mu, forbid_core=None):
        """sup over intervals B of rho_out(B) exp(mu phi(inner B)); intervals with no grid point
        inside get rho <= h/2 and phi <= fmax. forbid_core=k: only intervals not containing [-k,k]."""
        N, t = self.N, self.t
        i = np.arange(N + 1)[:, None]
        j = np.arange(N + 1)[None, :]
        lo = np.maximum(i - 1, 0)
        hi = np.minimum(j + 1, N)
        rho = (t[hi] - t[lo]) / 2.0
        ok = j >= i
        if forbid_core is not None:
            k = forbid_core
            # B = [l,u] not containing [-k,k] means l > -k or u < k; its inner grid interval
            # [t_i,t_j] then has t_i >= l > -k or t_j <= u < k (a necessary condition, so the sup
            # below is over a superset of the relevant intervals).
            ok = ok & ((t[i] > -k + 1e-12) | (t[j] < k - 1e-12))
        with np.errstate(over="ignore", invalid="ignore"):
            val = np.where(ok, rho * np.exp(mu * np.where(ok, M, 0.0)), 0.0)
        return max(val.max(), (self.h / 2) * np.exp(mu * fmax))

    def psi(self, mu, core):
        """Upper bound on sup over boxes B not containing core=(kx,ky,kz)."""
        g, N, t = self.g, self.N, self.t
        best = 0.0
        for which in range(3):
            X = np.array([self._sup_1d(self.fx[a], self.fxmax[a], mu, core[0] if which == 0 else None)
                          for a in range(N + 1)])
            Z = np.array([self._sup_1d(self.fz[a], self.fzmax[a], mu, core[2] if which == 2 else None)
                          for a in range(N + 1)])
            F = np.exp(mu * g.c * self.y0 ** 2) * X * Z
            # outer sup over B_y: rho_out * min_{grid y0 in inner}
            i = np.arange(N + 1)[:, None]; j = np.arange(N + 1)[None, :]
            Mn = np.full((N + 1, N + 1), np.inf)
            for a in range(N + 1):
                cur = np.inf
                for bb in range(a, N + 1):
                    cur = min(cur, F[bb]); Mn[a, bb] = cur
            lo = np.maximum(i - 1, 0); hi = np.minimum(j + 1, N)
            rho = (t[hi] - t[lo]) / 2.0
            ok = j >= i
            if which == 1:
                k = core[1]
                ok = ok & ((t[i] > -k + 1e-12) | (t[j] < k - 1e-12))
            val = np.where(ok, rho * np.where(ok, Mn, 0.0), 0.0).max()
            # tiny B_y (no grid point inside): rho <= h/2, bound F by its max over all y0 and
            # neighbouring cells (crude: max F times exp(mu * c * h))
            # for y in a grid cell, phi_x and phi_z change by at most |b| h and |bp| h, c y^2 by 2 c h
            val = max(val, (self.h / 2) * F.max() * np.exp(mu * (2 * g.c + abs(g.b) + abs(g.bp)) * self.h))
            best = max(best, val)
        return best


def core_terms(cores, gam, mu):
    terms = [np.exp(-mu * gam[-1])]
    for a in range(len(cores) - 1):
        tau = min((1 - cores[a + 1][q]) / 2 for q in range(3))
        terms.append((1 - tau) * np.exp(-mu * gam[a]))
    return max(terms)


def evaluate(g, cores, N=80, eps=0.0, verbose=True, gam=None, P=None):
    """cores: nested list of (kx,ky,kz); Phi(mu) = max(core terms (decreasing), Psi (increasing)),
    minimised by bisection on log mu.  Returns (base per gadget, mu, gammas)."""
    if gam is None:
        gam = [core_gap(g, *K)[0] for K in cores]
    if verbose:
        for K, gv in zip(cores, gam):
            print("  core", tuple(round(v, 3) for v in K), "gamma = %.5f" % gv)
    if P is None:
        P = PsiEval(g, N)
    lo, hi = np.log(1e-3), np.log(1e3)
    best = None
    for _ in range(40):
        m1 = lo + (hi - lo) / 3; m2 = hi - (hi - lo) / 3
        vals = []
        for m in (m1, m2):
            mu = np.exp(m)
            ct = core_terms(cores, gam, mu); ps = P.psi(mu, cores[0])
            vals.append(max(ct, ps))
            if best is None or max(ct, ps) < best[0]:
                best = (max(ct, ps), mu, ps, ct)
        if vals[0] < vals[1]:
            hi = m2
        else:
            lo = m1
    Phi, mu, ps, ct = best
    if verbose:
        print("  best mu = %.3f  Phi = %.5f (Psi %.5f, core terms %.5f)  base per gadget = %.5f, per variable = %.5f"
              % (mu, Phi, ps, ct, 1 / Phi, (1 / Phi) ** (1 / 3)))
    return 1 / Phi, mu, gam


def bangbang(y1, eta, epsf, zscale=None):
    """Idealised gadget: h1(y) = -y^2 (|y|<=y1), -(2 y1 |y| - y1^2) beyond (from ux = y1^2 x^2, b = 2 y1);
    h2(y) = -eta y^2 - (1-eta)(|y|-y1)_+^2 realised by uz = conjugate with bp = |h2'(1)|."""
    b = 2 * y1
    ux = lambda x: y1 * y1 * x * x
    bp = 2 * eta + 2 * (1 - eta) * (1 - y1) if zscale is None else zscale
    yy = np.linspace(-3, 3, 30001)
    h2 = -eta * yy ** 2 - (1 - eta) * np.maximum(np.abs(yy) - y1, 0) ** 2

    def uz(z):
        z = np.atleast_1d(z)
        out = np.empty_like(z, dtype=float)
        for k0 in range(0, len(z), 2000):
            zz = z[k0:k0 + 2000]
            out[k0:k0 + 2000] = np.max(h2[None, :] - bp * zz[:, None] * yy[None, :], axis=1)
        return out
    c = 1 + eta + epsf
    return Gadget(ux, uz, b, c, bp, name=f"bangbang y1={y1} eta={eta} eps={epsf}")


if __name__ == "__main__":
    y1, eta, epsf = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
    g = bangbang(y1, eta, epsf)
    print(g.name, "b=%.3f bp=%.3f c=%.3f" % (g.b, g.bp, g.c))
    thetas = [float(v) for v in sys.argv[4].split(",")] if len(sys.argv) > 4 else [0.6, 0.7, 0.8, 0.9, 1.0]
    cores = [(th, th, th) for th in thetas]
    evaluate(g, cores, N=int(sys.argv[5]) if len(sys.argv) > 5 else 60)
