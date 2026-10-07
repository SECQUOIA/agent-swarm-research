"""Where are the leaves?  Leaf statistics for the path family (face-exact-exponential.md, Section 6).

For each run: number of leaves by sup-distance of the leaf from x* (dyadic bands), number of leaves
inside the cube [-0.577, 0.577]^n on which f is convex for kappa = 0.1 (2 - 12 kappa x^2 > 2 b),
and the largest volume fraction of a leaf (to compare with the Theorem 1 bound theta^n e^lam).
Usage: python3 analyze_leaves.py rel rule kappa cmode eps n1 n2 ...
"""
import math
import sys
import numpy as np
from bb_path import Inst, run


def main():
    rel, rule, kappa, cmode, eps = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4], float(sys.argv[5])
    rc = math.sqrt((1 - 0.8) / (6 * kappa)) if kappa > 0 else 1.0
    for n in [int(a) for a in sys.argv[6:]]:
        I = Inst(n, kappa, cmode)
        r = run(I, rel, rule, eps, record=True)
        info = np.array(r["leafinfo"])          # (max width, volume, sup-distance to x*)
        wid, vol, dist, far = info[:, 0], info[:, 1], info[:, 2], info[:, 3]
        bands = [0.0, 1e-3, 1e-2, 0.03, 0.1, 0.3, 1.0, 3.0]
        counts = [int(np.sum((dist >= bands[k]) & (dist < bands[k + 1]))) for k in range(len(bands) - 1)]
        # leaf inside the convex cube: all corners within rc of 0 -> need the box itself; use width+dist proxy
        print(f"{rel} {rule} kappa={kappa} {cmode} eps={eps:.0e} n={n}: leaves={r['leaves']}")
        print("   leaves by sup-distance from x*: " + ", ".join(
            f"[{bands[k]:g},{bands[k+1]:g}): {counts[k]}" for k in range(len(counts))))
        widths = [0.0, 0.01, 0.03, 0.1, 0.3, 1.0, 2.01]
        wc = [int(np.sum((wid >= widths[k]) & (wid < widths[k + 1]))) for k in range(len(widths) - 1)]
        print("   leaves by largest side: " + ", ".join(f"[{widths[k]:g},{widths[k+1]:g}): {wc[k]}" for k in range(len(wc))))
        frac = vol / 2.0 ** n
        print(f"   largest leaf volume fraction = {frac.max():.4g} (fraction^(1/n) = {frac.max() ** (1 / n):.4f}; "
              f"Theorem 1 allows fraction <= {0.6 ** n * math.exp(5 / 9 * (1 + eps / 0.8)):.4g}); "
              f"leaves with sup-distance < 0.1: {int(np.sum(dist < 0.1))}")
        if kappa > 0:
            print(f"   (convexity cube half-side for kappa={kappa}: {rc:.3f}); leaves contained in the cube "
                  f"x* + [-1/sqrt(3), 1/sqrt(3)]^n: {int(np.sum(far <= 1 / math.sqrt(3) + 1e-12))}")


if __name__ == "__main__":
    main()
