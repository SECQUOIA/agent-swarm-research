"""Separable 2D families: rules' leaves versus the exact guillotine optimum on a candidate grid.

Grid per axis: 17 uniform points, the component's kinks/minimizer, and a geometric
grid (4 points per octave, both sides) around the minimizer down to sqrt(eps)/16.
N_guill_grid >= N_guill (cuts restricted), so leaves/N_guill_grid understates the
true loss only if the grid misses good cuts.
Usage: python3 sep_families.py
"""
import math
import sys
import numpy as np
from poly1d import from_function
from nd_sep import run, guill_grid

A = [1 / 3, math.sqrt(2) - 1]


def grid(center, eps, extra=()):
    pts = set(np.linspace(0, 1, 17)) | set(extra)
    r = 0.5
    while r > math.sqrt(eps) / 16:
        for c in center:
            for s in (-1, 1):
                x = c + s * r
                if 0 < x < 1:
                    pts.add(x)
        r /= 2 ** 0.25
    return np.array(sorted(pts))


def comp(kind, a, eps):
    if kind == "sharp":
        return from_function(lambda t: 2 * abs(t - a) - (t - a) ** 2, eps, K=801, extra=[a]), [a]
    if kind == "shallow":
        return from_function(lambda t: 0.3 * abs(t - a), eps, K=801, extra=[a]), [a]
    if kind == "quad":
        return from_function(lambda t: (t - a) ** 2, eps, K=801, extra=[a]), [a]
    if kind == "quad_small":
        return from_function(lambda t: 0.05 * (t - a) ** 2, eps, K=801, extra=[a]), [a]
    if kind == "quartic":
        return from_function(lambda t: 4 * (t - a) ** 4, eps, K=801, extra=[a]), [a]
    if kind == "saw":
        P = [0, 0.21, 0.47, 0.8, 1]
        def g(t):
            j = min(np.searchsorted(P, t, side="right") - 1, len(P) - 2)
            return (t - P[j]) * (P[j + 1] - t)
        return from_function(g, eps, K=801, extra=P), P[1:-1]
    raise ValueError(kind)


FAMS = [("sharp", "sharp"), ("sharp", "quad"), ("shallow", "quad"), ("quad", "quad"),
        ("quad", "quad_small"), ("saw", "saw"), ("saw", "quad"), ("quartic", "sharp")]

if __name__ == "__main__":
    rules = ("omega", "deficit", "multi", "bis")
    for k1, k2 in FAMS:
        print(f"== {k1} x {k2}", flush=True)
        for e in (1e-3, 1e-5, 1e-7):
            I1, c1 = comp(k1, A[0], e / 2)
            I2, c2 = comp(k2, A[1], e / 2)
            g1, g2 = grid(c1, e, c1), grid(c2, e, c2)
            ng = guill_grid([I1, I2], [g1, g2])
            res = {r: run([I1, I2], r, cap=400000)[1] for r in rules}
            ratios = {r: (None if res[r] is None else round(res[r] / ng, 2)) for r in rules}
            print(f"  eps={e:.0e} G=({len(g1)},{len(g2)}) N_guill_grid={ng:4d} leaves={res} ratio={ratios}", flush=True)
