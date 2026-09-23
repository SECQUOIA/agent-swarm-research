"""Potential-based flows on general graphs and cacti.

Model (Pfetsch, Schmidt, Skutella, Thuerauf, "Potential-Based Flows - An
Overview", 2026, eqs. (1), (3a), (3b)): for every arc a = (u, v)

    pi_u - pi_v = beta_a * psi(x_a),      psi(x) = sgn(x) |x|^r,

and flow conservation  sum_out x - sum_in x = b_v.  Loads b sum to zero.
Potentials are unique up to an additive constant (survey Theorem 1).

This module computes the unique flow for a given load vector b by
minimising the strictly convex energy  sum_a beta_a * |x_a|^(r+1)/(r+1)
subject to conservation, via the (unique) circulation on each independent
cycle.  On a cactus every cycle carries exactly one scalar circulation and
the cycles do not interact (each cycle's loop condition depends only on its
own circulation), so the computation is a sequence of 1-D root findings.
For general graphs we fall back to a damped Newton on the potentials.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq


def psi(x, r=2.0):
    return np.sign(x) * np.abs(x) ** r


def psi_prime(x, r=2.0):
    return r * np.abs(x) ** (r - 1.0)


class Graph:
    """Undirected multigraph with arcs (u, v, beta); arc index = position."""

    def __init__(self, n, arcs):
        self.n = n
        self.arcs = [(int(u), int(v), float(beta)) for (u, v, beta) in arcs]
        self.m = len(self.arcs)

    # ---- spanning tree / fundamental cycles -------------------------------
    def spanning_forest(self):
        parent = list(range(self.n))

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        tree = []
        non_tree = []
        for idx, (u, v, _) in enumerate(self.arcs):
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[ru] = rv
                tree.append(idx)
            else:
                non_tree.append(idx)
        return tree, non_tree

    def tree_flow(self, b, tree):
        """Flow on tree arcs that routes b (non-tree arcs carry 0)."""
        adj = [[] for _ in range(self.n)]
        for idx in tree:
            u, v, _ = self.arcs[idx]
            adj[u].append((v, idx, +1))
            adj[v].append((u, idx, -1))
        x = np.zeros(self.m)
        seen = [False] * self.n
        order = []
        par = [None] * self.n
        for root in range(self.n):
            if seen[root]:
                continue
            seen[root] = True
            stack = [root]
            while stack:
                u = stack.pop()
                order.append(u)
                for v, idx, sgn in adj[u]:
                    if not seen[v]:
                        seen[v] = True
                        par[v] = (u, idx, sgn)
                        stack.append(v)
        surplus = np.array(b, dtype=float).copy()
        for u in reversed(order):
            if par[u] is None:
                continue
            p, idx, sgn = par[u]
            # arc idx oriented p->u if sgn == +1 (as seen from p). Flow from u
            # to p equals surplus[u]; positive x means along arc orientation.
            # If arc is (p, u): flow u->p is -x  => x = -surplus[u].
            # If arc is (u, p): flow u->p is +x  => x = surplus[u].
            x[idx] = -surplus[u] if sgn == +1 else surplus[u]
            surplus[p] += surplus[u]
            surplus[u] = 0.0
        return x

    def cycle_vector(self, tree, idx):
        """Signed incidence vector of the fundamental cycle of non-tree arc idx."""
        u, v, _ = self.arcs[idx]
        adj = [[] for _ in range(self.n)]
        for j in tree:
            a, c, _ = self.arcs[j]
            adj[a].append((c, j, +1))
            adj[c].append((a, j, -1))
        # path from v back to u in the tree
        prev = {v: None}
        stack = [v]
        while stack:
            a = stack.pop()
            if a == u:
                break
            for c, j, sgn in adj[a]:
                if c not in prev:
                    prev[c] = (a, j, sgn)
                    stack.append(c)
        z = np.zeros(self.m)
        z[idx] = 1.0
        a = u
        while prev[a] is not None:
            p, j, sgn = prev[a]
            # we traverse from a back to p; moving p->a used sign sgn
            z[j] = float(sgn)
            a = p
        return z


def solve_flow(G: Graph, b, r=2.0, tol=1e-13):
    """Unique potential-based flow for loads b (sum b = 0).

    Returns (x, pi) with pi normalised to pi[0] = 0.
    Uses fundamental cycles; for a cactus the cycles are arc-disjoint and the
    loop equations decouple, which we exploit when they do.
    """
    b = np.asarray(b, dtype=float)
    assert abs(b.sum()) < 1e-9, "loads must balance"
    tree, non_tree = G.spanning_forest()
    x0 = G.tree_flow(b, tree)
    if not non_tree:
        x = x0
    else:
        Z = np.array([G.cycle_vector(tree, idx) for idx in non_tree])  # k x m
        beta = np.array([a[2] for a in G.arcs])
        supports = [set(np.nonzero(z)[0]) for z in Z]
        disjoint = all(
            supports[i].isdisjoint(supports[j])
            for i in range(len(Z))
            for j in range(i + 1, len(Z))
        )
        lam = np.zeros(len(Z))
        if disjoint:
            for i, z in enumerate(Z):
                s = np.nonzero(z)[0]

                def loop(l, s=s, z=z):
                    return float(np.sum(beta[s] * z[s] * psi(x0[s] + l * z[s], r)))

                # bracket
                lo, hi = -1.0, 1.0
                while loop(lo) > 0:
                    lo *= 2
                while loop(hi) < 0:
                    hi *= 2
                lam[i] = brentq(loop, lo, hi, xtol=tol, rtol=1e-15, maxiter=500)
        else:
            lam = _newton_circulations(Z, x0, beta, r)
        x = x0 + Z.T @ lam
    pi = potentials_from_flow(G, x, r)
    return x, pi


def _newton_circulations(Z, x0, beta, r):
    """Damped Newton on the convex dual in circulation space (general graphs)."""
    k = Z.shape[0]
    lam = np.zeros(k)

    def grad(l):
        x = x0 + Z.T @ l
        return Z @ (beta * psi(x, r))

    def energy(l):
        x = x0 + Z.T @ l
        return float(np.sum(beta * np.abs(x) ** (r + 1) / (r + 1)))

    for _ in range(200):
        x = x0 + Z.T @ lam
        g = grad(lam)
        if np.linalg.norm(g) < 1e-12:
            break
        W = beta * psi_prime(x, r) + 1e-14
        H = (Z * W) @ Z.T
        d = -np.linalg.solve(H, g)
        t = 1.0
        e0 = energy(lam)
        while energy(lam + t * d) > e0 + 1e-4 * t * g @ d and t > 1e-12:
            t *= 0.5
        lam = lam + t * d
    return lam


def potentials_from_flow(G: Graph, x, r=2.0):
    pi = np.full(G.n, np.nan)
    pi[0] = 0.0
    adj = [[] for _ in range(G.n)]
    for idx, (u, v, beta) in enumerate(G.arcs):
        adj[u].append((v, idx, +1))
        adj[v].append((u, idx, -1))
    stack = [0]
    while stack:
        u = stack.pop()
        for v, idx, sgn in adj[u]:
            if np.isnan(pi[v]):
                beta = G.arcs[idx][2]
                drop = beta * psi(x[idx], r)  # pi_tail - pi_head
                pi[v] = pi[u] - drop if sgn == +1 else pi[u] + drop
                stack.append(v)
    return pi


def check_flow(G: Graph, b, x, pi, r=2.0, tol=1e-7):
    """Residuals of conservation and potential equations (for tests)."""
    res_b = np.array(b, dtype=float).copy()
    for idx, (u, v, _) in enumerate(G.arcs):
        res_b[u] -= x[idx]
        res_b[v] += x[idx]
    res_p = np.array(
        [pi[u] - pi[v] - beta * psi(x[idx], r) for idx, (u, v, beta) in enumerate(G.arcs)]
    )
    return float(np.abs(res_b).max()), float(np.abs(res_p).max())


# ---- cactus constructors ----------------------------------------------------

def cycle_graph(k, betas=None):
    betas = [1.0] * k if betas is None else list(betas)
    arcs = [(i, (i + 1) % k, betas[i]) for i in range(k)]
    return Graph(k, arcs)


def chain_of_cycles(sizes, betas=None):
    """Cycles glued in a chain at single cut vertices.

    Cycle j has nodes offset..offset+sizes[j]-1 with node 0 of cycle j equal
    to the "opposite" node (index sizes[j-1]//2) of cycle j-1.  Returns
    (Graph, list_of_cycle_node_lists).
    """
    arcs = []
    cycles = []
    n = 0
    prev_exit = None
    for j, k in enumerate(sizes):
        if prev_exit is None:
            nodes = list(range(n, n + k))
            n += k
        else:
            nodes = [prev_exit] + list(range(n, n + k - 1))
            n += k - 1
        for i in range(k):
            beta = 1.0 if betas is None else betas[j][i]
            arcs.append((nodes[i], nodes[(i + 1) % k], beta))
        cycles.append(nodes)
        prev_exit = nodes[k // 2]
    return Graph(n, arcs), cycles
