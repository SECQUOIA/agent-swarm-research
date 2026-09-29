"""Remaining separable families (sawtooth, quartic) with a coarser candidate grid:
17 uniform points, the kinks, and 2 geometric points per octave around each
minimizer/kink (sep_families.py used 4 per octave; for three sawtooth kinks that
grid needed a 4D DP table of several GB, so that run was stopped after one row).
Usage: python3 sep_families2.py"""
import math
import numpy as np
from sep_families import comp, A
from nd_sep import run, guill_grid


def grid(center, eps, extra=()):
    pts = set(np.linspace(0, 1, 17)) | set(extra)
    r = 0.5
    while r > math.sqrt(eps) / 16:
        for c in center:
            for s in (-1, 1):
                x = c + s * r
                if 0 < x < 1:
                    pts.add(x)
        r /= 2 ** 0.5
    return np.array(sorted(pts))


if __name__ == "__main__":
    rules = ("omega", "deficit", "multi", "bis")
    for k1, k2 in (("saw", "saw"), ("saw", "quad"), ("quartic", "sharp")):
        print(f"== {k1} x {k2}", flush=True)
        for e in (1e-3, 1e-5, 1e-7):
            I1, c1 = comp(k1, A[0], e / 2)
            I2, c2 = comp(k2, A[1], e / 2)
            g1, g2 = grid(c1, e, c1), grid(c2, e, c2)
            if len(g1) * len(g2) > 130 * 130:
                print(f"  eps={e:.0e} grid too large ({len(g1)},{len(g2)}), skipped", flush=True)
                continue
            ng = guill_grid([I1, I2], [g1, g2])
            res = {r: run([I1, I2], r, cap=400000)[1] for r in rules}
            ratios = {r: round(res[r] / ng, 2) for r in rules}
            print(f"  eps={e:.0e} G=({len(g1)},{len(g2)}) N_guill_grid={ng:4d} leaves={res} ratio={ratios}", flush=True)
