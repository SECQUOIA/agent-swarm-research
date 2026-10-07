"""SENSITIVITY VARIANT (generated from indep_leafwise_and_discount.py): the bound uses discount 3 D' while psi' keeps D'; violations are expected.

Independent checks for the confirmation review of covering-upper-half.md.

Brute force on small random tree decompositions with private variables:
bag t (t != root) holds its own separator s_t, the separators s_u of its
children and one private variable y_t; the root holds its children's
separators and y_0.  All quantities (f*, m, U_t, w_t, W_t) are computed by
enumerating every full configuration, not by dynamic programming.

Part A (Lemma 1', leafwise form of Theorem 1').  Each separator range
{0..m-1} is cut into closed cells [b_k, b_{k+1}] that share endpoints.
Leaves of bag t are products of closed cells in the separator coordinates
(possibly subdivided) times pieces of the private range, so they overlap at
cell boundaries.  Each leaf has its own error err_{t,B} >= 0; each cell has
its own piece phi_{e,D} on the closed cell, so the split is two-valued at
boundaries.  Checks f* - rho~ <= bound of Lemma 1'.

Part B (remark after Proposition 1.3).  c* = min_{m(x)>0} m/(2 sum_e w_e).
Build the DP split psi of F' = F - 2 c* sum_e w_e (bag functions
F_t - c* b_t) and check that psi + c* a and psi - c* a are exact for F,
a_t = (-1)^depth(t) w_t.  Then check the necessary condition (1.1) directly:
for c = 1.01 c*, the two exactness conditions must be jointly infeasible
(tested by an LP over all splits).  Also checks c* >= 1/(2n).

usage: python3 indep_leafwise_and_discount.py
"""
import itertools
import numpy as np
from scipy.optimize import linprog
import scipy.sparse as sp


def random_parent(N, rng):
    return [None] + [int(rng.integers(0, t)) for t in range(1, N)]


class Inst:
    def __init__(self, N, m, k, rng):
        self.N, self.m, self.k = N, m, k
        self.par = random_parent(N, rng)
        self.ch = [[u for u in range(1, N) if self.par[u] == t] for t in range(N)]
        self.n = N - 1
        # variables: s_1..s_n (index e-1), y_0..y_{N-1} (index n + t)
        self.nv = self.n + N
        self.dims = [m] * self.n + [k] * N
        # scope of bag t: own separator first (if t != 0), children, private
        self.scope = []
        for t in range(N):
            sc = ([t - 1] if t != 0 else []) + [u - 1 for u in self.ch[t]] \
                + [self.n + t]
            self.scope.append(sc)
        self.F = []
        for t in range(N):
            shape = tuple(self.dims[v] for v in self.scope[t])
            kind = rng.integers(0, 2)
            if kind == 0:
                T = rng.uniform(0, 1, shape)
            else:  # smooth-ish: quadratic in grid coordinates plus noise
                grids = np.meshgrid(*[np.linspace(-1, 1, d) for d in shape],
                                    indexing="ij")
                T = sum(rng.uniform(-1, 1) * g + rng.uniform(0, 2) * g ** 2
                        for g in grids)
                if len(grids) >= 2:
                    T = T + rng.uniform(-1, 1) * grids[0] * grids[1]
                T = T + 0.1 * rng.uniform(0, 1, shape)
            self.F.append(T)
        self.enumerate()

    def depth(self, t):
        d = 0
        while t != 0:
            t = self.par[t]
            d += 1
        return d

    def sub(self, t):
        out, stack = [], [t]
        while stack:
            u = stack.pop()
            out.append(u)
            stack += self.ch[u]
        return out

    def enumerate(self):
        X = np.array(list(itertools.product(*[range(d) for d in self.dims])))
        self.X = X
        bagvals = [self.F[t][tuple(X[:, v] for v in self.scope[t])]
                   for t in range(self.N)]
        self.bagvals = bagvals
        Ftot = sum(bagvals)
        self.fstar = Ftot.min()
        self.mx = Ftot - self.fstar
        m = self.m
        self.U = [None] * self.N
        self.w = [None] * self.N
        for t in range(1, self.N):
            subval = sum(bagvals[u] for u in self.sub(t))
            s = X[:, t - 1]
            self.U[t] = np.array([subval[s == j].min() for j in range(m)])
            self.w[t] = np.array([self.mx[s == j].min() for j in range(m)])
        # W_t over the bag scope
        self.W = []
        for t in range(self.N):
            sc = self.scope[t]
            shape = tuple(self.dims[v] for v in sc)
            Wt = np.full(shape, np.inf)
            idx = tuple(X[:, v] for v in sc)
            np.minimum.at(Wt, idx, self.mx)
            self.W.append(Wt)
        self.E = [len(self.sub(t)) - 1 for t in range(self.N)]


def part_a(rng, trials=300, disc=1.0):
    worst, ratios, viol = -np.inf, [], 0
    for trial in range(trials):
        N = int(rng.integers(2, 5))
        m = int(rng.integers(4, 7))
        inst = Inst(N, m, 2, rng)
        n = inst.n
        Dp = 1.0 / (3 * n + 1)
        theta = [None] + [(3 * inst.E[t] + 2) * Dp for t in range(1, N)]
        psi = [None] + [inst.U[t] - theta[t] * inst.w[t] for t in range(1, N)]
        # closed cells sharing endpoints
        cells = [None]
        for e in range(1, N):
            nb = int(rng.integers(0, m - 1))
            inner = sorted(rng.choice(np.arange(1, m - 1), size=nb,
                                      replace=False).tolist()) if nb else []
            b = [0] + inner + [m - 1]
            cells.append([(b[i], b[i + 1]) for i in range(len(b) - 1)])
        # pieces on closed cells: psi' + perturbation of a random scale
        scale = 10 ** rng.uniform(-3, 0)
        mode = trial % 3
        phi = [None]
        for e in range(1, N):
            pcs = []
            for (a, b) in cells[e]:
                idx = np.arange(a, b + 1)
                if mode == 0:     # random noise
                    r = scale * rng.normal(size=len(idx))
                elif mode == 1:   # within the sliver (bound's separator part <= 0)
                    r = Dp * inst.w[e][idx] * rng.uniform(-1, 1, len(idx))
                else:             # affine pieces (cellwise-affine class)
                    lam, c0 = rng.normal(), rng.normal()
                    r = scale * (lam * (idx / (m - 1)) + c0)
                pcs.append((a, b, psi[e][idx] + r))
            phi.append(pcs)
        # leaves of bag t: product of closed cells of its separators (each
        # possibly halved, still inside the closed cell) x private pieces
        total_rho, sep_bound, bag_bound = 0.0, 0.0, 0.0
        for t in range(N):
            sc = inst.scope[t]
            seps = [v + 1 for v in sc if v < n]          # edge ids in scope
            choices = []
            for e in seps:
                opts = []
                for ci, (a, b) in enumerate(cells[e]):
                    if b - a >= 2 and rng.uniform() < 0.5:
                        mid = (a + b) // 2
                        opts += [(ci, a, mid), (ci, mid, b)]
                    else:
                        opts.append((ci, a, b))
                choices.append(opts)
            priv_opts = [(0, 1)] if rng.uniform() < 0.5 else [(0, 0), (1, 1)]
            best = np.inf
            bagb = -np.inf
            for combo in itertools.product(*choices, priv_opts):
                sepbox, pv = combo[:-1], combo[-1]
                ranges = [np.arange(lo, hi + 1) for (_, lo, hi) in sepbox] + \
                    [np.arange(pv[0], pv[1] + 1)]
                grid = np.meshgrid(*ranges, indexing="ij")
                z = tuple(g.ravel() for g in grid)
                Fz = inst.F[t][z]
                Wz = inst.W[t][z]
                err = rng.uniform(0, 1) * rng.uniform(0, 0.5, size=Fz.shape)
                val = Fz - err
                for pos, e in enumerate(seps):
                    ci = sepbox[pos][0]
                    a, b, vals = phi[e][ci]
                    contrib = vals[z[pos] - a]
                    if t != 0 and pos == 0:
                        val = val - contrib              # own separator
                    else:
                        val = val + contrib              # child separator
                best = min(best, val.min())
                bagb = max(bagb, np.max(err - disc * Dp * Wz))
            total_rho += best
            bag_bound += bagb
        for e in range(1, N):
            up = max(np.max(vals - psi[e][a:b + 1] - disc * Dp * inst.w[e][a:b + 1])
                     for (a, b, vals) in phi[e])
            dn = max(np.max(-(vals - psi[e][a:b + 1]) - disc * Dp * inst.w[e][a:b + 1])
                     for (a, b, vals) in phi[e])
            sep_bound += up + dn
        lhs = inst.fstar - total_rho
        rhs = sep_bound + bag_bound
        worst = max(worst, lhs - rhs)
        if lhs > rhs + 1e-9:
            viol += 1
        if rhs > 1e-9 and lhs > 0:
            ratios.append(lhs / rhs)
    print(f"Part A (Lemma 1'): {trials} instances; violations {viol}; "
          f"max (lhs - bound) = {worst:.2e}; median ratio lhs/bound "
          f"{np.median(ratios):.3f}, max {np.max(ratios):.4f} "
          f"(over {len(ratios)} cases with positive lhs and bound)")
    return viol == 0


def bag_minima_ok(inst, extra, tol=1e-9):
    """extra[t]: table over scope of bag t (split terms).  Returns rho - f*."""
    rho = 0.0
    for t in range(inst.N):
        rho += (inst.F[t] + extra[t]).min()
    return rho - inst.fstar


def split_terms(inst, phi):
    """Tables sum_{u in ch(t)} phi_u(s_u) - phi_t(s_t) over scope of t."""
    out = []
    for t in range(inst.N):
        sc = inst.scope[t]
        shape = tuple(inst.dims[v] for v in sc)
        T = np.zeros(shape)
        for pos, v in enumerate(sc):
            if v >= inst.n:
                continue
            e = v + 1
            sh = [1] * len(sc)
            sh[pos] = inst.m
            sgn = -1.0 if (t != 0 and pos == 0) else 1.0
            T = T + sgn * phi[e].reshape(sh)
        out.append(T)
    return out


def b_table(inst, t):
    sc = inst.scope[t]
    shape = tuple(inst.dims[v] for v in sc)
    T = np.zeros(shape)
    for pos, v in enumerate(sc):
        if v >= inst.n:
            continue
        sh = [1] * len(sc)
        sh[pos] = inst.m
        T = T + inst.w[v + 1].reshape(sh)
    return T


def dp_split(inst, tables):
    """DP split for bag tables `tables`: phi_t = subtree value function."""
    phi = [None] * inst.N
    order = sorted(range(1, inst.N), key=lambda t: -inst.depth(t))
    for t in order:
        sc = inst.scope[t]
        T = tables[t].copy()
        for pos, v in enumerate(sc):
            if v < inst.n and not (pos == 0):
                sh = [1] * len(sc)
                sh[pos] = inst.m
                T = T + phi[v + 1].reshape(sh)
        axes = tuple(range(1, len(sc)))
        phi[t] = T.min(axis=axes)
    return phi


def lp_two_pattern_feasible(inst, a, c):
    """Is there psi with psi + c a and psi - c a both exact?  Exact iff each
    bag function attains its min at x*."""
    i_star = int(np.argmin(inst.mx))
    xstar = inst.X[i_star]
    n, m = inst.n, inst.m
    rows, cols, vals, rhs = [], [], [], []
    r = 0
    for sgn in (1.0, -1.0):
        for t in range(inst.N):
            sc = inst.scope[t]
            zs = tuple(int(xstar[v]) for v in sc)
            for z in np.ndindex(*inst.F[t].shape):
                if z == zs:
                    continue
                const = inst.F[t][z] - inst.F[t][zs]
                coef = {}
                for pos, v in enumerate(sc):
                    if v >= n:
                        continue
                    e = v + 1
                    sg = -1.0 if (t != 0 and pos == 0) else 1.0
                    for j, vv in ((z[pos], sg), (zs[pos], -sg)):
                        key = (e - 1) * m + j
                        coef[key] = coef.get(key, 0.0) + vv
                    const += sgn * c * sg * (a[e][z[pos]] - a[e][zs[pos]])
                # const + sum coef psi >= 0  ->  -sum coef psi <= const
                for key, vv in coef.items():
                    if vv != 0.0:
                        rows.append(r)
                        cols.append(key)
                        vals.append(-vv)
                rhs.append(const)
                r += 1
    A = sp.csr_matrix((vals, (rows, cols)), shape=(r, n * m))
    res = linprog(np.zeros(n * m), A_ub=A, b_ub=np.array(rhs),
                  bounds=[(None, None)] * (n * m), method="highs")
    return res.status == 0


def part_b(rng, trials=120):
    worst_exact, below, lp_ok, lp_bad, cs = 0.0, 0, 0, 0, []
    for trial in range(trials):
        N = int(rng.integers(2, 6))
        inst = Inst(N, int(rng.integers(3, 5)), 2, rng)
        n = inst.n
        # sum_e w_e(x_{S_e}) over all configurations
        sw = sum(inst.w[e][inst.X[:, e - 1]] for e in range(1, N))
        mask = inst.mx > 1e-12
        cstar = np.min(inst.mx[mask] / (2 * np.maximum(sw[mask], 1e-300)))
        cstar = min(cstar, 1e6)
        cs.append(2 * n * cstar)
        if cstar < 1 / (2 * n) - 1e-12:
            below += 1
        a = [None] + [(-1) ** inst.depth(e) * inst.w[e] for e in range(1, N)]
        tabs = [inst.F[t] - cstar * b_table(inst, t) for t in range(N)]
        psi = dp_split(inst, tabs)
        for sg in (1.0, -1.0):
            phi = [None] + [psi[e] + sg * cstar * a[e] for e in range(1, N)]
            d = bag_minima_ok(inst, split_terms(inst, phi))
            worst_exact = max(worst_exact, abs(d))
        if cstar < 1e5:
            if lp_two_pattern_feasible(inst, a, cstar * (1 - 1e-6)):
                lp_ok += 1
            if lp_two_pattern_feasible(inst, a, cstar * 1.01):
                lp_bad += 1
    print(f"Part B (Proposition 1.3 remark): {trials} trees with private "
          f"variables; DP split of F - 2c* sum w gives psi +- c* a with "
          f"max |rho - f*| = {worst_exact:.2e}; c* < 1/(2n) in {below} cases; "
          f"2n c* in [{min(cs):.3f}, {max(cs):.3f}]; LP feasible at "
          f"(1 - 1e-6) c*: {lp_ok}; LP feasible at 1.01 c*: {lp_bad}")
    return worst_exact < 1e-9 and below == 0 and lp_bad == 0


def main():
    rng = np.random.default_rng(20260930)
    ok = part_a(rng, disc=3.0)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
