"""Hill-climb for instances maximizing T_min / (2 N_opt - 1) for the 1D minimizer rule.

Instance: H = max(chords of y^2 over consecutive breakpoints (rigid certificate),
extra lines tangent to y^2 + mu at points p near breakpoints, end lines).
Usage: python3 search_ratio.py K_BREAKPOINTS EXTRA_PER_BP RESTARTS STEPS SEED
"""
import sys
import numpy as np
from poly1d import Inst, from_lines, r_min

EPS = 1e-6


def build(S, P, R):
    Sx = np.concatenate([[0.0], np.sort(S), [1.0]])
    lines = [(Sx[j] + Sx[j + 1], -Sx[j] * Sx[j + 1]) for j in range(len(Sx) - 1)]
    for p, r in zip(P, R):
        # tangent to y^2 + mu at p, with mu below the distance-squared to the nearest breakpoint
        d = np.min(np.abs(Sx - p))
        mu = d * d * r
        lines.append((2 * p, -p * p + mu))
    for s in Sx[1:-1]:
        lines.append((2 * s, -s * s + EPS))
    lines.append((0.0, EPS)); lines.append((2.0, -1.0 + EPS))
    xs, ms = from_lines(lines)
    return Inst(xs, ms)


def score(S, P, R):
    try:
        I = build(S, P, R)
    except ValueError:
        return -1, 0, 0
    T = I.tree(r_min, cap=100000)
    N = I.nopt()
    return T / (2 * N - 1), T, N


if __name__ == "__main__":
    K, E, restarts, steps, seed = map(int, sys.argv[1:6])
    rng = np.random.default_rng(seed)
    best = (0,)
    for rep in range(restarts):
        S = np.sort(rng.uniform(0.05, 0.95, K))
        P = np.repeat(S, E) + rng.normal(0, 0.05, K * E)
        P = np.clip(P, 1e-3, 1 - 1e-3)
        R = rng.uniform(0, 1, K * E)
        cur = score(S, P, R)
        for it in range(steps):
            S2 = np.clip(S + rng.normal(0, 0.01, K) * (rng.uniform(size=K) < 0.2), 0.01, 0.99)
            P2 = np.clip(P + rng.normal(0, 1, K * E) * 0.02 * (rng.uniform(size=K * E) < 0.2), 1e-4, 1 - 1e-4)
            R2 = np.clip(R + rng.normal(0, 0.2, K * E) * (rng.uniform(size=K * E) < 0.2), 0, 1)
            new = score(S2, P2, R2)
            if new[0] >= cur[0]:
                S, P, R, cur = S2, P2, R2, new
        print(rep, "ratio %.3f T=%d N=%d" % cur, flush=True)
        if cur[0] > best[0]:
            best = cur
            bestpar = (S.copy(), P.copy(), R.copy())
    print("BEST ratio %.4f T=%d N=%d" % best)
    np.savez(f"search_ratio_best_{K}_{E}_{seed}.npz", S=bestpar[0], P=bestpar[1], R=bestpar[2])
