"""Sanity check of Theorem 1.1 (duality) and Theorem 2.1 (band identity) on
discretized two-bag problems with explicit private variables.

E1 bags:  A(s, x) = -x s,  x in [-1, 1];   B(s, z) = z,  |s| <= z <= 1.
E4 bags:  A(s, x, y) = x^2 + 2 x s + 0.7 s + 0.5 y (s + 0.5), x in [-2, 2], y in [-1, 1];
          B(s, z) = -L4(s) + z^2, z in [-1, 1].
Grids are aligned so that the grid value functions equal U and -L exactly.
Three numbers must agree up to LP tolerance:
  split LP     max m_A + m_B  s.t. A - phi >= m_A, B + phi >= m_B  (phi in P_n)
  measure LP   min E_muA[A] + E_muB[B], separator marginals agree on P_n
  band formula f* - inf_phi [max(phi - U) + max(L - phi)] on the separator grid
"""
import numpy as np
from scipy.optimize import linprog
from consistency_lib import cheb_basis, band_gap

out = open("logs/check_duality.log", "w")


def log(m):
    print(m)
    out.write(m + "\n")
    out.flush()


def split_lp(SA, FA, SB, FB, n):
    """SA: separator index per A-point, FA values; same for B.  Variables [c, mA, mB]."""
    B_A = cheb_basis(S[SA], n)
    B_B = cheb_basis(S[SB], n)
    d = n + 1
    rowsA = np.hstack([B_A, np.ones((len(FA), 1)), np.zeros((len(FA), 1))])   # phi + mA <= FA
    rowsB = np.hstack([-B_B, np.zeros((len(FB), 1)), np.ones((len(FB), 1))])  # -phi + mB <= FB
    cost = np.zeros(d + 2); cost[d] = cost[d + 1] = -1
    r = linprog(cost, A_ub=np.vstack([rowsA, rowsB]), b_ub=np.concatenate([FA, FB]),
                bounds=[(None, None)] * (d + 2), method="highs")
    return -r.fun


def measure_lp(SA, FA, SB, FB, n):
    nA, nB = len(FA), len(FB)
    T = cheb_basis(S, n)[:, 1:]  # moments 1..n
    Aeq = np.zeros((2 + n, nA + nB))
    Aeq[0, :nA] = 1
    Aeq[1, nA:] = 1
    Aeq[2:, :nA] = T[SA].T
    Aeq[2:, nA:] = -T[SB].T
    beq = np.concatenate([[1, 1], np.zeros(n)])
    r = linprog(np.concatenate([FA, FB]), A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * (nA + nB),
                method="highs")
    mu = r.x
    return r.fun, mu[:nA], mu[nA:]


S = np.round(np.linspace(-1, 1, 41), 12)


def run(name, SA, FA, SB, FB, U, L, fs):
    for n in [1, 2, 4, 6, 8]:
        v1 = split_lp(SA, FA, SB, FB, n)
        v2, muA, muB = measure_lp(SA, FA, SB, FB, n)
        g, _, _, _ = band_gap(cheb_basis(S, n), U, L)
        # mass of the optimal measures off the conditional minimizers
        vA = np.full(len(S), np.inf); vB = np.full(len(S), np.inf)
        np.minimum.at(vA, SA, FA); np.minimum.at(vB, SB, FB)
        offA = muA[FA > vA[SA] + 1e-9].sum(); offB = muB[FB > vB[SB] + 1e-9].sum()
        log(f"  {name} n={n}: split LP = {v1:.8f}, measure LP = {v2:.8f}, f* - band gap = {fs - g:.8f}; "
            f"optimal-measure mass off conditional minimizers: {offA:.1e}, {offB:.1e}")


def main():
    # E1
    X = np.round(np.linspace(-1, 1, 21), 12)
    Z = np.round(np.linspace(0, 1, 21), 12)
    SA = np.repeat(np.arange(len(S)), len(X)); XA = np.tile(X, len(S))
    FA = -XA * S[SA]
    SB, FB = [], []
    for i, s in enumerate(S):
        for z in Z:
            if z >= abs(s) - 1e-12:
                SB.append(i); FB.append(z)
    SB, FB = np.array(SB), np.array(FB)
    run("E1", SA, FA, SB, FB, -np.abs(S), -np.abs(S), 0.0)
    # E4
    Xg = np.round(np.linspace(-2, 2, 81), 12)
    Yg = np.array([-1.0, -0.5, 0.0, 0.5, 1.0])
    Zg = np.round(np.linspace(-1, 1, 21), 12)
    L4 = lambda s: -0.28 - 0.4 * (s - 0.3) - 1.5 * (s - 0.3) ** 2
    U4 = lambda s: 0.7 * s - s ** 2 - 0.5 * np.abs(s + 0.5)
    ii, xx, yy = np.meshgrid(np.arange(len(S)), Xg, Yg, indexing="ij")
    SA = ii.ravel(); s = S[SA]
    FA = xx.ravel() ** 2 + 2 * xx.ravel() * s + 0.7 * s + 0.5 * yy.ravel() * (s + 0.5)
    jj, zz = np.meshgrid(np.arange(len(S)), Zg, indexing="ij")
    SB = jj.ravel()
    FB = -L4(S[SB]) + zz.ravel() ** 2
    fs = min(FA[SA == i].min() + FB[SB == i].min() for i in range(len(S)))
    log(f"  E4 grid f* = {fs:.3e}")
    run("E4", SA, FA, SB, FB, U4(S), L4(S), fs)


if __name__ == "__main__":
    main()
