"""Adversarial search for a PRs3 gap (Dey-Kocuk Conjecture 2, kappa = 2).

Random-restart hill climbing on (alpha, beta), maximizing exact - PRs3 and
recording exact - PR at the same points. Floating-point evidence only.
"""
import sys
import numpy as np
from dey_kocuk_conj2_check import exact, relax


def gap(a, b, mode):
    return exact(a, b) - relax(a, b, mode)


if __name__ == "__main__":
    rng = np.random.default_rng(int(sys.argv[1]))
    n = int(sys.argv[2]); target = sys.argv[3]
    best_overall = (-1, None)
    for restart in range(6):
        a = rng.uniform(-1, 1, n); b = rng.uniform(-1, 1, n)
        g = gap(a, b, target); step = 0.3
        for it in range(60):
            a2 = a + step * rng.normal(size=n); b2 = b + step * rng.normal(size=n)
            s = max(np.abs(a2).max(), np.abs(b2).max()); a2 /= s; b2 /= s
            g2 = gap(a2, b2, target)
            if g2 > g:
                a, b, g = a2, b2, g2
            else:
                step *= 0.97
        other = "PRs3" if target == "PR" else "PR"
        print(f"restart {restart}: {target} gap {g:.3e}; {other} gap {gap(a, b, other):.3e}")
        if g > best_overall[0]:
            best_overall = (g, (a.round(4).tolist(), b.round(4).tolist()))
    print("best", best_overall)
