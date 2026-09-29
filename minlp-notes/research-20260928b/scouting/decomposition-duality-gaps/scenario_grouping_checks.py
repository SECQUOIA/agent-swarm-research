"""Scenario-(group-)decomposition duality gaps with integer recourse.

Scratch code for the decomposition-duality-gaps scouting report.

Model: continuous first stage x in [0, X]; integer recourse
    F_s(x) = c*x + V(ceil(h_s - x)),
with V the value function of a small pure-integer program.  For a partition of
the S equiprobable SAA scenarios into groups G, the Lagrangian dual of the
group nonanticipativity constraints x_G = x equals
    D = min_x sum_G p_G * conv(F_G)(x),     F_G = average of F_s over s in G
(Caroe-Schultz; compact domain, lsc F_G).  The SAA optimum is
    P = min_x (1/S) sum_s F_s(x).
All quantities are computed exactly (up to floating point): F_G is piecewise
linear with positive slope c between the points x = h_s - j and jumps down
(lsc) at those points, so its convex envelope is the lower hull of its values
at those points and at the two endpoints.
"""
import math
import numpy as np

EPS = 1e-9


def lower_hull(px, py):
    """Lower convex hull of points (sorted by x)."""
    order = np.lexsort((py, px))
    pts = []
    for i in order:
        x, y = px[i], py[i]
        if pts and abs(pts[-1][0] - x) < 1e-13:
            continue  # keep the lower value (lexsort puts lower y first)
        while len(pts) >= 2:
            (x1, y1), (x2, y2) = pts[-2], pts[-1]
            if (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1) <= 1e-13:
                pts.pop()
            else:
                break
        pts.append((x, y))
    a = np.array(pts)
    return a[:, 0], a[:, 1]


class Model:
    def __init__(self, V, c, X):
        self.V, self.c, self.X = V, c, X

    def F(self, h, x):
        """F for scenario array h at points x (lsc value)."""
        t = np.ceil(h[:, None] - x[None, :] - EPS)
        return self.c * x[None, :] + self.V(t)

    def cand(self, h):
        js = np.arange(math.floor(h.min() - self.X) - 1, math.ceil(h.max()) + 2)
        pts = (h[:, None] - js[None, :]).ravel()
        pts = pts[(pts >= 0) & (pts <= self.X)]
        return np.unique(np.r_[pts, 0.0, self.X])

    def group_envelope(self, hG):
        xs = self.cand(hG)
        vals = self.F(hG, xs).mean(axis=0)
        return lower_hull(xs, vals)

    def primal(self, h):
        xs = self.cand(h)
        vals = self.F(h, xs).mean(axis=0)
        k = int(np.argmin(vals))
        return vals[k], xs[k]

    def dual(self, h, groups):
        hulls = [self.group_envelope(h[g]) for g in groups]
        w = np.array([len(g) for g in groups], float); w /= w.sum()
        grid = np.unique(np.concatenate([hx for hx, _ in hulls]))
        tot = np.zeros_like(grid)
        for (hx, hy), wg in zip(hulls, w):
            tot += wg * np.interp(grid, hx, hy)
        return tot.min()


def groups_random(S, k, rng):
    p = rng.permutation(S)
    return [p[i:i + k] for i in range(0, S, k)]


def groups_stratified(h, k, modulus):
    """Sort by phase h mod modulus; scenario of phase-rank r goes to group r mod (S/k)."""
    S = len(h)
    ng = S // k
    order = np.argsort(np.mod(h, modulus))
    return [order[g::ng] for g in range(ng)]


def groups_similar(h, k):
    """Bundle scenarios with similar h (consecutive after sorting): a common clustering heuristic."""
    order = np.argsort(h)
    return [order[i:i + k] for i in range(0, len(h), k)]


def V_simple(t):
    return np.maximum(t, 0.0)                 # min{y : y >= t, y integer >= 0}


def make_V_two():
    """V(t) = min{3y1 + 5y2 : 2y1 + 3y2 >= t, y in Z_+^2} for integer t."""
    cache = {}
    def Vint(t):
        if t <= 0:
            return 0.0
        if t not in cache:
            cache[t] = min(5 * y2 + 3 * math.ceil(max(t - 3 * y2, 0) / 2) for y2 in range(0, t // 3 + 2))
        return cache[t]
    vec = np.vectorize(lambda t: Vint(int(t)))
    return vec


def run(model, name, S, mu, sigma, ks, moduli, seed=0):
    rng = np.random.default_rng(seed)
    h = rng.normal(mu, sigma, S)
    P, xP = model.primal(h)
    grid = np.linspace(0, model.X, 2001)
    EF = model.F(h, grid).mean(axis=0)
    print(f"== {name}: S={S}, h~N({mu},{sigma}^2); SAA optimum P={P:.4f} at x={xP:.3f};"
          f" SAA objective range over x-grid: [{EF.min():.4f}, {EF.max():.4f}]")
    for k in ks:
        line = (f"   k={k:4d}  similar-h gap={P - model.dual(h, groups_similar(h, k)):.4f}"
                f"  random gap={P - model.dual(h, groups_random(S, k, rng)):.4f}")
        for M in moduli:
            line += f"  strat(mod {M}) gap={P - model.dual(h, groups_stratified(h, k, M)):.4f}"
        print(line)


if __name__ == "__main__":
    ks = (1, 2, 4, 8, 16, 32, 64, 128)
    run(Model(V_simple, 1.0, 2.0), "simple integer recourse, F=x+ceil(h-x)", 2048, 10.0, 3.0, ks, (1,))
    run(Model(make_V_two(), 1.5, 4.0), "V=min{3y1+5y2: 2y1+3y2>=t}, F=1.5x+V(ceil(h-x))", 2048, 30.0, 6.0, ks, (1, 2))
