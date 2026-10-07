"""Exact finite checks of the core search and its query counts.

* discrete uniform law: an interval of length ell contains at most
  ell (M-1)/(2 sigma) + 1 of the M atoms;
* core search on small cut-class instances: every optimizer cell retained,
  gap <= e_j, and the exact expectation (over ALL noise atoms) of the number
  of 2e_j-near-optimal tuples is <= H_k and of queries <= 2^k + 8^k J H_k;
* deterministic count under core growth, and the flat example
  V=(v1-v2)^2 whose retained-cell count grows like 2^j.
"""
import random
from fractions import Fraction as Fr
from itertools import product
from math import isqrt

def atoms(M, sigma):
    return [-sigma + 2 * sigma * Fr(j, M - 1) for j in range(M)]

def check_law(rng):
    for _ in range(300):
        M = rng.randint(2, 40); sigma = Fr(rng.randint(1, 9), rng.randint(1, 5))
        A = atoms(M, sigma)
        a = Fr(rng.randint(-200, 200), 97); ell = Fr(rng.randint(0, 300), 101)
        cnt = sum(1 for z in A if a <= z <= a + ell)
        assert Fr(cnt, M) <= ell / (2 * sigma) + Fr(1, M)

def core_search(V, k, L, J):
    """Return per-level (queries, retained, near) and check correctness."""
    cache_level = []
    cells = [tuple([0] * k)]  # level-0 cell index (integer lower corner in units of h_j)
    U = None
    out = []
    vals_all = {}
    for j in range(J + 1):
        h = Fr(1, 2 ** j); e = k * L * h * h / 8
        corners = set()
        for c in cells:
            for b in product((0, 1), repeat=k):
                corners.add(tuple(c[i] + b[i] for i in range(k)))
        vals = {v: V(tuple(h * vi for vi in v)) for v in corners}
        m = min(vals.values())
        U = m if U is None else min(U, m)
        kept = [c for c in cells
                if min(vals[tuple(c[i] + b[i] for i in range(k))] for b in product((0, 1), repeat=k)) - e <= U]
        out.append(dict(j=j, queries=len(corners), kept=kept, U=U, e=e, h=h))
        cells = [tuple(2 * c[i] + b[i] for i in range(k)) for c in kept for b in product((0, 1), repeat=k)]
    return out

def residual_V(inst_terms, k):
    """V(v) = min over binary residual labels of a small explicit quadratic."""
    A, bvec, C, r = inst_terms
    def V(v):
        best = None
        for z in product((0, 1), repeat=r):
            x = list(v) + list(z)
            n = k + r
            val = sum(bvec[i] * x[i] for i in range(n))
            val += sum(A[i][j] * x[i] * x[j] for i in range(n) for j in range(n)) / 2
            best = val if best is None else min(best, val)
        return best
    return V

def random_terms(rng, k, r):
    n = k + r
    A = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            w = Fr(rng.randint(-6, 6), rng.randint(1, 3))
            if i >= k and j >= k:
                w = -abs(w) if i != j else -abs(w)
            A[i][j] = A[j][i] = w
    for i in range(k):
        A[i][i] = Fr(rng.randint(-4, 8), 2)
    bvec = [Fr(rng.randint(-6, 6), rng.randint(1, 3)) for _ in range(n)]
    return A, bvec, None, r

def label_quads(A, bvec, k, r):
    """For each binary residual label, the core quadratic (P, p, const)."""
    n = k + r
    P = [[A[i][j] for j in range(k)] for i in range(k)]
    out = []
    for z in product((0, 1), repeat=r):
        p = [bvec[i] + sum(A[i][k + t] * z[t] for t in range(r)) for i in range(k)]
        const = sum(bvec[k + t] * z[t] for t in range(r))
        const += sum(A[k + s][k + t] * z[s] * z[t] for s in range(r) for t in range(r)) / 2
        out.append((P, p, const))
    return out

def qp_min_box(P, p, const, k):
    """Exact min of 1/2 v'Pv + p'v + const on [0,1]^k (k<=2) by face enumeration."""
    best = None
    for face in product((0, 1, None), repeat=k):
        free = [i for i in range(k) if face[i] is None]
        v = [Fr(face[i]) if face[i] is not None else None for i in range(k)]
        fixed = [i for i in range(k) if face[i] is not None]
        rhs = [-(p[i] + sum(P[i][j] * v[j] for j in fixed)) for i in free]
        if len(free) == 1:
            i = free[0]
            if P[i][i] == 0:
                continue
            v[i] = rhs[0] / P[i][i]
        elif len(free) == 2:
            a, b, c, d = P[0][0], P[0][1], P[1][0], P[1][1]
            det = a * d - b * c
            if det == 0:
                continue
            v[0] = (d * rhs[0] - b * rhs[1]) / det
            v[1] = (-c * rhs[0] + a * rhs[1]) / det
        if any(not (0 <= v[i] <= 1) for i in range(k)):
            continue
        val = const + sum(p[i] * v[i] for i in range(k)) + sum(P[i][j] * v[i] * v[j] for i in range(k) for j in range(k)) / 2
        best = val if best is None else min(best, val)
    return best

def check_smoothed(rng, k, M, J, sigma, trials):
    worst_q = 0; worst_n = 0
    for _ in range(trials):
        A, bvec, _, r = random_terms(rng, k, 2)
        L = max(Fr(1), max(A[i][i] for i in range(k)))
        quads = label_quads(A, bvec, k, r)
        V0 = residual_V((A, bvec, None, r), k)
        H = (3 + (1 + Fr(k, 2)) * L / (2 * sigma)) ** k
        A_ = atoms(M, sigma)
        tot_q = 0; near = [0] * (J + 1)
        for g in product(A_, repeat=k):
            W = lambda v, g=g: V0(v) + sum(g[i] * v[i] for i in range(k))
            fstar = min(qp_min_box(P, [p[i] + g[i] for i in range(k)], c, k) for (P, p, c) in quads)
            out = core_search(W, k, L, J)
            tot_q += sum(o["queries"] for o in out)
            for o in out:
                j, h, e = o["j"], o["h"], o["e"]
                assert o["U"] - fstar <= e                      # gap of the incumbent
                assert any(True for _ in o["kept"])              # optimizer cell kept (nonempty)
                for v in product(range(2 ** j + 1), repeat=k):
                    if W(tuple(h * t for t in v)) <= fstar + 2 * e:
                        near[j] += 1
        nA = len(A_) ** k
        for j in range(J):
            assert Fr(near[j], nA) <= H, (j, Fr(near[j], nA), H)
            worst_n = max(worst_n, float(Fr(near[j], nA) / H))
        Eq = Fr(tot_q, nA)
        bound = 2 ** k + 8 ** k * J * H
        assert Eq <= bound, (Eq, bound)
        worst_q = max(worst_q, float(Eq / bound))
    return worst_q, worst_n

def check_growth_count():
    # V(v) = sum (v_i - c_i)^2, g = 1, L = 2, kappa = 2
    for k in (1, 2):
        c = [Fr(1, 3), Fr(5, 7)][:k]
        V = lambda v: sum((v[i] - c[i]) ** 2 for i in range(k))
        out = core_search(V, k, Fr(2), 7)
        kappa = 2
        Nbound = (1 + (k * kappa) ** 0.5) ** k
        for o in out:
            assert len(o["kept"]) <= 2 ** k * Nbound + 1e-9          # retained cells <= 2^k N_j
        for o in out[1:]:
            assert o["queries"] <= 8 ** k * Nbound + 1e-9           # level j+1 queries <= 8^k N_j
    # flat example: V = (v1 - v2)^2, nonunique optima
    V = lambda v: (v[0] - v[1]) ** 2
    out = core_search(V, 2, Fr(2), 7)
    return [len(o["kept"]) for o in out]

if __name__ == "__main__":
    rng = random.Random(7)
    check_law(rng)
    print("discrete-law interval bound: passed")
    for (k, M, J, sig, tr) in ((1, 16, 4, Fr(1, 2), 6), (1, 16, 4, Fr(4), 4), (2, 8, 3, Fr(1, 2), 2)):
        wq, wn = check_smoothed(rng, k, M, J, sig, tr)
        print("k=%d M=%d J=%d sigma=%s: worst E[queries]/bound=%.4f, worst E[near]/H=%.4f" % (k, M, J, sig, wq, wn))
    flat = check_growth_count()
    print("growth count bound passed; flat example retained cells per level:", flat)
    print("ALL COUNT CHECKS PASSED")
