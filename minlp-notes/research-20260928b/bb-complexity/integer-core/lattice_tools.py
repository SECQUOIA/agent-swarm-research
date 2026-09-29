"""Small lattice utilities for the random-CVP checks (floating point).

- lll(B): LLL reduction (delta = 0.99) of the columns of B.
- enum_ball(R, tt, r2): all integer z with ||R z - tt||^2 <= r2, where R is
  upper triangular (B = Q R).  Schnorr-Euchner style depth-first search.
- gm_basis / gauss_basis: random bases of determinant 1.
- gh_radius(n): radius of the ball of volume 1 in R^n.
Written for this workstream; no scout code is reused.
"""
import math
import numpy as np


def gh_radius(n):
    # vol(B_r) = pi^{n/2} r^n / Gamma(n/2+1) = 1
    return math.exp((math.lgamma(n / 2 + 1) - (n / 2) * math.log(math.pi)) / n)


def lll(B, delta=0.99):
    B = np.array(B, dtype=float, copy=True)
    n = B.shape[1]

    def gso(B):
        Bs = np.zeros_like(B)
        mu = np.zeros((n, n))
        for i in range(n):
            v = B[:, i].copy()
            for j in range(i):
                mu[i, j] = B[:, i] @ Bs[:, j] / (Bs[:, j] @ Bs[:, j])
                v -= mu[i, j] * Bs[:, j]
            Bs[:, i] = v
        return Bs, mu

    Bs, mu = gso(B)
    k = 1
    it = 0
    while k < n:
        it += 1
        if it > 200000:
            break
        for j in range(k - 1, -1, -1):
            q = round(mu[k, j])
            if q != 0:
                B[:, k] -= q * B[:, j]
                mu[k, :j + 1] -= q * np.append(mu[j, :j], 1.0)
        bk = Bs[:, k] @ Bs[:, k]
        bk1 = Bs[:, k - 1] @ Bs[:, k - 1]
        if bk >= (delta - mu[k, k - 1] ** 2) * bk1:
            k += 1
        else:
            B[:, [k - 1, k]] = B[:, [k, k - 1]]
            Bs, mu = gso(B)
            k = max(k - 1, 1)
    return B


def enum_ball(R, tt, r2, exclude_zero=False, limit=None):
    """Return list of (dist2, z) with ||R z - tt||^2 <= r2 (R upper triangular)."""
    n = R.shape[0]
    out = []
    z = np.zeros(n)
    diag = np.diag(R)

    def rec(i, partial):
        # coordinates i+1..n-1 fixed; choose z[i]
        c = (tt[i] - R[i, i + 1:] @ z[i + 1:]) / R[i, i]
        rem = r2 - partial
        if rem < 0:
            return
        w = math.sqrt(rem) / abs(diag[i])
        lo = math.ceil(c - w - 1e-12)
        hi = math.floor(c + w + 1e-12)
        for v in range(lo, hi + 1):
            d = (R[i, i] * (v - c)) ** 2
            if partial + d > r2:
                continue
            z[i] = v
            if i == 0:
                if exclude_zero and not np.any(z):
                    continue
                out.append((partial + d, z.copy()))
                if limit is not None and len(out) > limit:
                    raise RuntimeError("enumeration limit exceeded")
            else:
                rec(i - 1, partial + d)
        z[i] = 0

    rec(n - 1, 0.0)
    return out


def gm_basis(n, rng, logp_bits=None):
    """Goldstein-Mayer lattice {x in Z^n : x_1 = a.x_{2..n} mod p}, scaled to det 1.
    Equidistributes to Haar measure as p -> infinity (Goldstein-Mayer 2003)."""
    from sympy import nextprime
    # Cap for float LLL precision. The n <= 20 data in cvp_bounds.jsonl were generated
    # before the cap, with 2n + 8 bits (48 bits at n = 20); rerunning n = 20 gives other lattices.
    bits = logp_bits if logp_bits is not None else min(2 * n + 8, 44)
    p = int(nextprime(int(2 ** bits) + int(rng.integers(0, 10 ** 6))))
    B = np.eye(n)
    B[0, 0] = float(p)
    B[0, 1:] = rng.integers(0, p, n - 1).astype(float)
    B /= p ** (1.0 / n)
    return B


def gauss_basis(n, rng):
    B = rng.standard_normal((n, n))
    B /= abs(np.linalg.det(B)) ** (1.0 / n)
    return B


def max_clique(adj):
    """Exact maximum clique of a boolean adjacency matrix (bitset branch and bound)."""
    nv = len(adj)
    nb = [0] * nv
    for i in range(nv):
        m = 0
        for j in range(nv):
            if adj[i][j]:
                m |= 1 << j
        nb[i] = m
    best = [0]

    def color_bound(P):
        # greedy coloring bound: returns list of (vertex, color) in order
        order = []
        col = 0
        U = P
        while U:
            col += 1
            Q = U
            while Q:
                v = (Q & -Q).bit_length() - 1
                Q &= ~(1 << v)
                Q &= ~nb[v]
                U &= ~(1 << v)
                order.append((v, col))
        return order

    def expand(size, P):
        order = color_bound(P)
        for v, c in reversed(order):
            if size + c <= best[0]:
                return
            newP = P & nb[v]
            if newP:
                expand(size + 1, newP)
            elif size + 1 > best[0]:
                best[0] = size + 1
            P &= ~(1 << v)

    expand(0, (1 << nv) - 1)
    return best[0]


def greedy_clique(adj, starts=60):
    nv = len(adj)
    best = 0
    deg = adj.sum(1)
    order = np.argsort(-deg)
    for s in order[:starts]:
        cl = [s]
        cand = adj[s].copy()
        for j in order:
            if cand[j]:
                cl.append(j)
                cand &= adj[j]
        best = max(best, len(cl))
    return best
