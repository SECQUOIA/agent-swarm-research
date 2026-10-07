"""Split relaxations on tree decompositions with one-dimensional separators,
on finite grids (exact bag minima).

Every non-root bag t has one parent separator variable s_t (the separator of
the edge from t to its parent), taking m values.  A bag table F[t] is an
ndarray whose axes are [s_t (if t is not the root), s_u for u in ch(t)].
Private bag variables are assumed minimized out already.

A split phi = (phi_u) (one array of length m per non-root bag u) gives bag
functions F_t + sum_{u in ch(t)} phi_u(s_u) - phi_t(s_t), and

    rho(phi) = sum_t min F_t^phi,     gap(phi) = f* - rho(phi).

All functions below are exact on the grid (finite minima); they are
floating-point computations.
"""
import numpy as np


class Tree:
    def __init__(self, parent, tables):
        """parent[t] = parent of t (-1 for the root, which must be node 0)."""
        self.parent = list(parent)
        self.N = len(parent)
        self.children = [[] for _ in range(self.N)]
        for t, p in enumerate(parent):
            if p >= 0:
                self.children[p].append(t)
        self.F = tables
        self.order = self._postorder()
        self.n_edges = self.N - 1
        # E[t] = number of edges strictly inside sub(t)
        self.E = [0] * self.N
        for t in self.order:
            self.E[t] = sum(self.E[u] + 1 for u in self.children[t])

    def _postorder(self):
        out, stack = [], [(0, False)]
        while stack:
            t, done = stack.pop()
            if done:
                out.append(t)
            else:
                stack.append((t, True))
                for u in self.children[t]:
                    stack.append((u, False))
        return out

    def _axis(self, t, u):
        """Axis of child u in the table of t."""
        off = 0 if t == 0 else 1
        return off + self.children[t].index(u)

    def _add_child_terms(self, t, funcs, skip=None):
        """F_t + sum_{u in ch(t), u != skip} funcs[u](s_u) (broadcast)."""
        G = self.F[t].copy()
        nd = G.ndim
        for u in self.children[t]:
            if u == skip:
                continue
            ax = self._axis(t, u)
            shape = [1] * nd
            shape[ax] = -1
            G = G + funcs[u].reshape(shape)
        return G

    def value_functions(self):
        """U[t], V[t] for non-root t, and f*."""
        U = [None] * self.N
        for t in self.order:
            if t == 0:
                continue
            G = self._add_child_terms(t, U)
            U[t] = G.reshape(G.shape[0], -1).min(axis=1)
        G0 = self._add_child_terms(0, U)
        fstar = G0.min()
        V = [None] * self.N
        for t in reversed(self.order):  # preorder: parents first
            for u in self.children[t]:
                G = self._add_child_terms(t, U, skip=u)
                if t != 0:
                    shape = [1] * G.ndim
                    shape[0] = -1
                    G = G + V[t].reshape(shape)
                ax = self._axis(t, u)
                G = np.moveaxis(G, ax, 0)
                V[u] = G.reshape(G.shape[0], -1).min(axis=1)
        return U, V, fstar

    def rho(self, phi):
        tot = 0.0
        for t in range(self.N):
            G = self._add_child_terms(t, phi)
            if t != 0:
                shape = [1] * G.ndim
                shape[0] = -1
                G = G - phi[t].reshape(shape)
            tot += G.min()
        return tot

    def bag_deficits(self, phi, U, fstar):
        """Per-bag deficits with the DP split U as reference (sum = gap)."""
        out = []
        for t in range(self.N):
            G = self._add_child_terms(t, phi)
            if t != 0:
                shape = [1] * G.ndim
                shape[0] = -1
                G = G - phi[t].reshape(shape)
                out.append(-G.min())
            else:
                out.append(fstar - G.min())
        return out


def graded_theta(tree):
    n = tree.n_edges
    return [None if t == 0 else (2 * tree.E[t] + 1) / (2 * n)
            for t in range(tree.N)]


def graded_split(tree, U, V, fstar, theta=None):
    """psi_t = (1 - theta_t) U_t + theta_t L_t, L_t = f* - V_t."""
    if theta is None:
        theta = graded_theta(tree)
    psi = [None] * tree.N
    for t in range(1, tree.N):
        L = fstar - V[t]
        psi[t] = (1 - theta[t]) * U[t] + theta[t] * L
    return psi


def sliver_bound(tree, r, w):
    """sum_e [max(r_e - w_e/(2n)) + max(-r_e - w_e/(2n))]  (Theorem 1)."""
    n = tree.n_edges
    tot = 0.0
    for t in range(1, tree.N):
        tot += np.max(r[t] - w[t] / (2 * n)) + np.max(-r[t] - w[t] / (2 * n))
    return tot


def random_tree(n_nodes, max_children, rng):
    parent = [-1]
    counts = [0]
    for t in range(1, n_nodes):
        cand = [p for p in range(t) if counts[p] < max_children]
        p = int(rng.choice(cand))
        parent.append(p)
        counts[p] += 1
        counts.append(0)
    return parent


def random_tables(parent, m, rng, scale=1.0, kind="uniform"):
    N = len(parent)
    ch = [0] * N
    for t, p in enumerate(parent):
        if p >= 0:
            ch[p] += 1
    tables = []
    for t in range(N):
        nd = ch[t] + (0 if t == 0 else 1)
        shape = (m,) * max(nd, 1) if nd > 0 else (1,)
        if kind == "uniform":
            T = rng.uniform(0, scale, size=shape)
        else:  # smooth-ish: random quadratic forms on a grid plus noise
            grids = np.meshgrid(*[np.linspace(-1, 1, m)] * len(shape),
                                indexing="ij")
            T = np.zeros(shape)
            for g in grids:
                T += rng.uniform(-1, 1) * g + rng.uniform(-1, 1) * g ** 2
            for i in range(len(grids)):
                for j in range(i + 1, len(grids)):
                    T += rng.uniform(-1, 1) * grids[i] * grids[j]
            T = scale * T + 0.1 * scale * rng.uniform(0, 1, size=shape)
        tables.append(T)
    return tables
