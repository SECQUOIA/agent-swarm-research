"""Independent check: price() lower bound vs brute-force minimum over all row vertices.
Focus: widths with 2 decimals (as in cap='random'), where different subsets have sums that are
equal in exact arithmetic but differ by rounding."""
import sys, itertools
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rowhull.rows import normalize_row
from rowhull.pricing import price


def brute(row, pi, omega):
    n, B, w = row.n, row.B, row.widths
    best = np.inf
    for mask in range(1 << n):
        tot = sum(w[i] for i in range(n) if mask >> i & 1)
        prof = sum(pi[i] * w[i] for i in range(n) if mask >> i & 1)
        for j in range(n):
            if mask >> j & 1:
                continue
            r = B - tot
            if -1e-9 <= r <= w[j] + 1e-9:
                r = min(max(r, 0.0), w[j])
                val = omega[j] * row.items[j].gap(np.array([r]))[0] - pi[j] * r - prof
                best = min(best, val)
    return best


def main(decimals, trials, n, kmax):
    rng = np.random.default_rng(1)
    bad = 0; worst = 0.0
    for t in range(trials):
        U = np.round(rng.uniform(2, 8, n), decimals) if decimals is not None else rng.uniform(2, 8, n)
        entries = []
        for i in range(n):
            q = rng.uniform(0.5, 1.5) / U[i]
            entries.append((f"x{i}", 1.0, 0.0, float(U[i]), f"w{i}", lambda v, q=q, u=U[i]: (2 * q * u + 1) * v - q * v ** 2))
        B = round(float(rng.uniform(0.2, 0.8) * U.sum()), 4 if decimals is not None else 12)
        row = normalize_row(entries, "==", B)
        pi = rng.normal(size=n); omega = rng.uniform(0, 1, n) * (rng.random(n) < 0.7)
        lower, cols = price(row, pi, omega, kmax=kmax)
        ref = brute(row, pi, omega)
        if lower > ref + 1e-7 * max(1, abs(ref)):
            bad += 1; worst = max(worst, lower - ref)
    print(f"decimals={decimals} n={n} kmax={kmax}: {bad}/{trials} rows with lower > true min; worst excess {worst:.3g}")


if __name__ == "__main__":
    main(2, 300, 10, 4000)
    main(1, 300, 10, 4000)
    main(0, 300, 10, 4000)
    main(None, 300, 10, 4000)
    main(2, 300, 10, 30)
    main(None, 300, 10, 30)
