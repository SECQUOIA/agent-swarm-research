"""Targeted check of omega's drift on m = eps + (2|x-a| - (x-a)^2) + (z-b)^2 (sharp x, quadratic z).

Grids: x = 17 uniform points + a + geometric (G_X points per octave) around a;
       z = 17 uniform points + b + geometric (G_Z points per octave) around b,
both down to sqrt(eps)/16.  N_guill_grid (exact DP on the grid) >= N_guill, so
leaves/N_guill_grid is a lower bound on the true ratio.
Usage: python3 sharp_quad.py GX GZ"""
import math
import sys
import numpy as np
from poly1d import from_function
from nd_sep import run, guill_grid

A = [1 / 3, math.sqrt(2) - 1]


def geo_grid(c, eps, per_oct):
    pts = set(np.linspace(0, 1, 17)) | {c}
    r = 0.5
    while r > math.sqrt(eps) / 16:
        for s in (-1, 1):
            x = c + s * r
            if 0 < x < 1:
                pts.add(x)
        r /= 2 ** (1 / per_oct)
    return np.array(sorted(pts))


if __name__ == "__main__":
    gx, gz = int(sys.argv[1]), int(sys.argv[2])
    for e in (1e-3, 1e-5, 1e-7, 1e-9, 1e-11):
        I1 = from_function(lambda t: 2 * abs(t - A[0]) - (t - A[0]) ** 2, e / 2, K=801, extra=[A[0]])
        I2 = from_function(lambda t: (t - A[1]) ** 2, e / 2, K=801, extra=[A[1]])
        g1, g2 = geo_grid(A[0], e, gx), geo_grid(A[1], e, gz)
        ng = guill_grid([I1, I2], [g1, g2])
        res = {r: run([I1, I2], r, cap=400000)[1] for r in ("omega", "deficit", "multi", "bis")}
        print(f"eps={e:.0e} G=({len(g1)},{len(g2)}) N_guill_grid={ng} leaves={res} "
              f"ratios " + " ".join(f"{r}={v/ng:.2f}" for r, v in res.items()), flush=True)
