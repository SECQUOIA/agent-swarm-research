"""Cellwise-affine (PA) split classes on paths with one-dimensional
separators, on a grid: refinement rules, the Theorem 1 bound, direct gaps
of explicit splits, the LP optimum gap(PA) for given cells, and covering
numbers of separator projections of near-optimal sets.

Path: nodes 0..n (node 0 = root).  Edge e = 1..n joins node e-1 and node e
and carries the separator s_e in [-1, 1] (grid of m points).  Tables:
node 0: F0(s_1); node t (1..n-1): Ft(s_t, s_{t+1}); node n: Fn(s_n).
Floating point; exact minima over the grid.
"""
import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog
from tree_lib import Tree


# ---------------------------------------------------------------- instances
def kink(s, p, gamma, sigma):
    """min over y in [0,1] of y*gamma*sigma*(p - s): a concave kink at p."""
    return np.minimum(0.0, gamma * sigma * (p - s))


# ----------------------------------------------------------- cell brackets
def cell_bracket(s, A_up, B_lo):
    """inf over lambda of max(lambda s - A_up) + max(B_lo - lambda s);
    returns (g, lambda, beta) with both maxima equal to g/2 after the shift
    beta.  Convex piecewise-linear in lambda: golden-section search."""
    if len(s) == 1:
        g = B_lo[0] - A_up[0]
        return g, 0.0, (A_up[0] + B_lo[0]) / 2
    ds = np.diff(s)
    S = 2 * max(np.max(np.abs(np.diff(A_up) / ds)),
                np.max(np.abs(np.diff(B_lo) / ds))) + 1.0

    def f(lam):
        return np.max(lam * s - A_up) + np.max(B_lo - lam * s)

    a, b = -S, S
    gr = (np.sqrt(5) - 1) / 2
    x1, x2 = b - gr * (b - a), a + gr * (b - a)
    f1, f2 = f(x1), f(x2)
    for _ in range(120):
        if f1 <= f2:
            b, x2, f2 = x2, x1, f1
            x1 = b - gr * (b - a)
            f1 = f(x1)
        else:
            a, x1, f1 = x1, x2, f2
            x2 = a + gr * (b - a)
            f2 = f(x2)
    lam = (a + b) / 2
    p = np.max(lam * s - A_up)
    q = np.max(B_lo - lam * s)
    beta = (q - p) / 2
    return p + q, lam, beta


# -------------------------------------------------------------- refinement
def refine(s, split_test, max_level=None):
    """Dyadic refinement in index space (m - 1 must be a power of 2).
    split_test(i0, i1, level) -> bool, for the closed cell s[i0..i1].
    Returns the final list of (i0, i1) and a flag if the grid limited it."""
    m = len(s)
    assert (m - 1) & (m - 2) == 0, "m - 1 must be a power of 2"
    todo = [(0, m - 1, 0)]
    final, grid_limited = [], False
    while todo:
        i0, i1, lev = todo.pop()
        if split_test(i0, i1, lev):
            if i1 - i0 == 1 or (max_level is not None and lev >= max_level):
                grid_limited = True
                final.append((i0, i1))
            else:
                mid = (i0 + i1) // 2
                todo.append((i0, mid, lev + 1))
                todo.append((mid, i1, lev + 1))
        else:
            final.append((i0, i1))
    final.sort()
    return final, grid_limited


def cell_index(cells, m):
    """Assign each grid point to one cell (half-open, last cell closed)."""
    idx = np.empty(m, dtype=int)
    for k, (i0, i1) in enumerate(cells):
        idx[i0:i1] = k
    idx[cells[-1][1]] = len(cells) - 1
    return idx


def pa_from_brackets(s, cells, A_up, B_lo):
    """PA function whose cell pieces are the minimizers of the brackets."""
    m = len(s)
    phi = np.empty(m)
    gs = []
    idx = cell_index(cells, m)
    pieces = []
    for (i0, i1) in cells:
        g, lam, beta = cell_bracket(s[i0:i1 + 1], A_up[i0:i1 + 1],
                                    B_lo[i0:i1 + 1])
        gs.append(g)
        pieces.append((lam, beta))
    for i in range(m):
        lam, beta = pieces[idx[i]]
        phi[i] = lam * s[i] + beta
    return phi, np.array(gs)


# ------------------------------------------------------------ LP for gap(PA)
def lp_gap(s, tree, cells_per_edge, fstar):
    """max over PA splits on the given cells of rho; returns f* - max."""
    n = tree.n_edges
    m = len(s)
    # variable layout: for edge e (1..n): 2*len(cells) entries (lam, beta)
    offs, nv = [0] * (n + 1), 0
    idxs = [None] * (n + 1)
    for e in range(1, n + 1):
        offs[e] = nv
        nv += 2 * len(cells_per_edge[e])
        idxs[e] = cell_index(cells_per_edge[e], m)
    coff = nv
    nv += n + 1
    rows, cols, vals, rhs = [], [], [], []
    r = 0

    def add_phi(row_ids, e, pts, sign):
        # adds sign * phi_e(s[pts]) to the given rows
        k = idxs[e][pts]
        rows.extend(row_ids)
        cols.extend(offs[e] + 2 * k)
        vals.extend(sign * s[pts])
        rows.extend(row_ids)
        cols.extend(offs[e] + 2 * k + 1)
        vals.extend(sign * np.ones(len(pts)))

    # constraint form: c_t - [phi terms of F_t^phi] <= F_t
    # node 0: F0 + phi_1(b)
    ids = np.arange(r, r + m)
    rows.extend(ids); cols.extend([coff] * m); vals.extend([1.0] * m)
    add_phi(ids, 1, np.arange(m), -1.0)
    rhs.extend(tree.F[0])
    r += m
    for t in range(1, n):
        A_ = np.repeat(np.arange(m), m)
        B_ = np.tile(np.arange(m), m)
        ids = np.arange(r, r + m * m)
        rows.extend(ids); cols.extend([coff + t] * (m * m))
        vals.extend([1.0] * (m * m))
        add_phi(ids, t + 1, B_, -1.0)   # + phi_{t+1}(s_{t+1})
        add_phi(ids, t, A_, +1.0)       # - phi_t(s_t)
        rhs.extend(tree.F[t].ravel())
        r += m * m
    ids = np.arange(r, r + m)
    rows.extend(ids); cols.extend([coff + n] * m); vals.extend([1.0] * m)
    add_phi(ids, n, np.arange(m), +1.0)
    rhs.extend(tree.F[n])
    r += m
    Amat = sp.csr_matrix((vals, (rows, cols)), shape=(r, nv))
    cost = np.zeros(nv)
    cost[coff:] = -1.0
    # gauge: fix beta of the first cell of each edge to 0 (constants telescope)
    bounds = [(None, None)] * nv
    for e in range(1, n + 1):
        bounds[offs[e] + 1] = (0.0, 0.0)
    res = linprog(cost, A_ub=Amat, b_ub=np.array(rhs), bounds=bounds,
                  method="highs")
    if res.status != 0:
        raise RuntimeError(res.message)
    return fstar + res.fun


# --------------------------------------------------------------- coverings
def cover_count(points, side):
    """Least number of intervals of length `side` covering a finite set of
    reals (greedy is optimal in 1D)."""
    if len(points) == 0:
        return 0
    pts = np.sort(points)
    cnt, i, N = 0, 0, len(pts)
    while i < N:
        cnt += 1
        x = pts[i] + side
        i = np.searchsorted(pts, x, side="right")
    return cnt


def sup_cover(s, w, eps, M, etas=None):
    if etas is None:
        top = max(w.max(), eps)
        etas = np.concatenate([[0.0], np.logspace(np.log10(eps / 100),
                                                  np.log10(top), 80)])
    best = 0
    for eta in etas:
        pts = s[w <= eta + 1e-15]
        best = max(best, cover_count(pts, 2 * np.sqrt((eps + eta) / M)))
    return best


# ------------------------------------------------- structured large-grid path
class PathFast:
    """Path whose middle tables are kappa (s_t - s_{t+1})^2 + u_t(s_{t+1});
    node 0 table u_0(s_1), leaf table u_n(s_n).  Minima are computed in
    chunks, so grids of 10^4 points are feasible.  Same conventions as the
    Tree class (phi[e] subtracted from node e, added to node e-1)."""

    def __init__(self, s, kappa, unaries, chunk=512):
        self.s, self.kappa, self.u = s, kappa, unaries
        self.n = len(unaries) - 1
        self.n_edges = self.n
        self.chunk = chunk

    def _minconv(self, g, out_axis):
        """out_axis='a': h(a) = min_b [kappa (a-b)^2 + g(b)];
        out_axis='b': h(b) = min_a [g(a) + kappa (a-b)^2]  (symmetric)."""
        s, k, m = self.s, self.kappa, len(self.s)
        h = np.empty(m)
        for i0 in range(0, m, self.chunk):
            i1 = min(m, i0 + self.chunk)
            D = k * (s[i0:i1, None] - s[None, :]) ** 2 + g[None, :]
            h[i0:i1] = D.min(axis=1)
        return h

    def value_functions(self):
        n = self.n
        U = [None] * (n + 1)
        U[n] = self.u[n].copy()
        for t in range(n - 1, 0, -1):          # node t: edges t (parent), t+1
            U[t] = self._minconv(self.u[t] + U[t + 1], "a")
        fstar = np.min(self.u[0] + U[1])
        V = [None] * (n + 1)
        V[1] = self.u[0].copy()
        for t in range(1, n):
            V[t + 1] = self._minconv(V[t], "b") + self.u[t]
        return U, V, fstar

    def rho(self, phi):
        n, s, k, m = self.n, self.s, self.kappa, len(self.s)
        tot = np.min(self.u[0] + phi[1])
        for t in range(1, n):
            g = self.u[t] + phi[t + 1]
            best = np.inf
            for i0 in range(0, m, self.chunk):
                i1 = min(m, i0 + self.chunk)
                D = (k * (s[i0:i1, None] - s[None, :]) ** 2 + g[None, :]
                     - phi[t][i0:i1, None])
                best = min(best, D.min())
            tot += best
        tot += np.min(self.u[n] - phi[n])
        return tot


def path_unaries(n, s, A, v, kinks, tilt=None, centers=(0.0,)):
    """Unary terms of the structured path: node t < n acts on s_{t+1}, the
    leaf on s_n.  Valley: A * min_c (|s - c| - v)_+^2 over the centers (a
    minimum of convex terms: semiconcave, concave kinks where the terms
    cross).  Plus concave kinks and the tilt +-amp*sin(freq*s) at the root
    and the leaf."""
    val = np.min([A * np.maximum(np.abs(s - c) - v, 0.0) ** 2
                  for c in centers], axis=0)
    out = []
    for node in range(n + 1):
        f = val.copy()
        for (p, g, sg) in kinks.get(node, []):
            f = f + kink(s, p, g, sg)
        if tilt is not None and node == 0:
            f = f + tilt[0] * np.sin(tilt[1] * s)
        if tilt is not None and node == n:
            f = f - tilt[0] * np.sin(tilt[1] * s)
        out.append(f)
    return out


def tree_from_unaries(s, kappa, unaries):
    n = len(unaries) - 1
    tables = [unaries[0]]
    for t in range(1, n):
        tables.append(kappa * (s[:, None] - s[None, :]) ** 2
                      + unaries[t][None, :])
    tables.append(unaries[n])
    return Tree([-1] + list(range(n)), tables)
