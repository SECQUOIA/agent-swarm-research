"""Confirm-recheck C1: T3 attainment counts of the lower end of Theorem 3.1,
recomputed with formulations independent of the note's check_tree.py.

Same random instances as the note (numpy default_rng(0); per trial
a ~ N(0,1)^5, c ~ N(0,1)^5, b ~ N(0,1)^{5x5}; separator grid linspace(-1,1,5);
classes P_0, P_1, P_2).  Differences from the note's code:

- gap: the *measure* LP of Theorem 1.1 (bag measures muA, muB, muC; the
  s1-marginal of muB agrees with muA on Phi_1, the s2-marginal of muB agrees
  with muC on Phi_2), not the split LP;
- per-edge 2 dist(Phi_e, Band_e): the one-separator band LP of Theorem 2.1 on
  the explicit DP value functions U_e, L_e = f* - V_e, not a tree LP with a
  full class on the other edge;
- basis: Legendre instead of Chebyshev;
- degree 0: closed forms, exact up to rounding:
    gap = f* - min a - min b - min c,
    2 dist_1 = f* - min a - min_{s1,s2}(b + c),
    2 dist_2 = f* - min_{s1,s2}(a + b) - min c.
"""
import numpy as np
from numpy.polynomial import legendre as Lg
from scipy.optimize import linprog

out = None


def log(m):
    print(m)
    if out is not None:
        out.write(m + "\n")
        out.flush()


def measure_rho(a, b, c, B):
    """min muA.a + muB.b + muC.c over probability vectors with
    B^T muA = B^T (row sums of muB) and B^T muC = B^T (column sums of muB)."""
    k = len(a)
    d = B.shape[1]
    nA, nB, nC = k, k * k, k
    nv = nA + nB + nC
    cost = np.concatenate([a, b.reshape(-1), c])
    rows, rhs = [], []
    # normalizations
    for lo, n in [(0, nA), (nA, nB), (nA + nB, nC)]:
        r = np.zeros(nv); r[lo:lo + n] = 1; rows.append(r); rhs.append(1.0)
    # edge 1: sum_i muA_i B_ij = sum_{i,l} muB_il B_ij
    for j in range(d):
        r = np.zeros(nv)
        r[:nA] = B[:, j]
        r[nA:nA + nB] = -np.repeat(B[:, j], k)      # muB index i*k + l, s1 = i
        rows.append(r); rhs.append(0.0)
    # edge 2: sum_l muC_l B_lj = sum_{i,l} muB_il B_lj
    for j in range(d):
        r = np.zeros(nv)
        r[nA + nB:] = B[:, j]
        r[nA:nA + nB] = -np.tile(B[:, j], k)        # s2 = l
        rows.append(r); rhs.append(0.0)
    res = linprog(cost, A_eq=np.array(rows), b_eq=np.array(rhs), bounds=[(0, None)] * nv,
                  method="highs")
    assert res.status == 0, res.message
    return res.fun


def band_dist2(B, U, L):
    """Delta = min over phi in span(B) of max(phi - U) + max(L - phi) (= 2 dist, Theorem 2.1)."""
    k, d = B.shape
    cost = np.zeros(d + 2); cost[d] = cost[d + 1] = 1
    A1 = np.hstack([B, -np.ones((k, 1)), np.zeros((k, 1))])
    A2 = np.hstack([-B, np.zeros((k, 1)), -np.ones((k, 1))])
    res = linprog(cost, A_ub=np.vstack([A1, A2]), b_ub=np.concatenate([U, -L]),
                  bounds=[(None, None)] * (d + 2), method="highs")
    assert res.status == 0, res.message
    return res.fun


def main():
    rng = np.random.default_rng(0)
    k = 5
    s = np.linspace(-1, 1, k)
    tot = att = both = sumlt = 0
    closed_err = 0.0
    att0 = both0 = 0
    examples = []
    for trial in range(300):
        a = rng.normal(size=k)
        c = rng.normal(size=k)
        b = rng.normal(size=(k, k))
        fs = np.min(a[:, None] + b + c[None, :])
        # edge 1: child A, parent {B, C};  edge 2: child {A, B}, parent C
        U1 = a
        L1 = fs - np.min(b + c[None, :], axis=1)
        U2 = np.min(a[:, None] + b, axis=0)
        L2 = fs - c
        for deg in [0, 1, 2]:
            B = Lg.legvander(s, deg)
            g = fs - measure_rho(a, b, c, B)
            d1 = band_dist2(B, U1, L1)
            d2 = band_dist2(B, U2, L2)
            if deg == 0:
                g0 = fs - a.min() - b.min() - c.min()
                d10 = fs - a.min() - np.min(b + c[None, :])
                d20 = fs - np.min(a[:, None] + b) - c.min()
                closed_err = max(closed_err, abs(g - g0), abs(d1 - d10), abs(d2 - d20))
                if g0 == max(d10, d20):           # exact float equality (combinatorial event)
                    att0 += 1
                    if min(d10, d20) > 1e-4:
                        both0 += 1
            tot += 1
            if g > d1 + d2 + 1e-7:
                sumlt += 1
            if abs(g - max(d1, d2)) <= 1e-7:
                att += 1
                if min(d1, d2) > 1e-4:
                    both += 1
                    if trial in (1, 2, 5):
                        examples.append((trial, deg, g, d1, d2))
            assert max(d1, d2) <= g + 1e-7, (trial, deg, g, d1, d2)
    log(f"{tot} cases (measure LP for the gap, band LP on explicit value functions for 2dist_e):")
    log(f"  lower end attained (|gap - max_e 2dist_e| <= 1e-7): {att}; of these, both 2dist_e > 1e-4: {both}")
    log(f"  per-edge sum below the gap (by more than 1e-7): {sumlt}")
    log(f"  degree 0 closed forms: max |LP - closed form| = {closed_err:.2e}; "
        f"exact attainment {att0} of 300, with both per-edge terms > 1e-4 in {both0}")
    for e in examples:
        log("  trial %d deg %d: gap = %.10f, 2dist_1 = %.10f, 2dist_2 = %.10f" % e)


if __name__ == "__main__":
    import os
    os.makedirs("logs", exist_ok=True)
    out = open("logs/c1_tree_T3.log", "w")
    main()
