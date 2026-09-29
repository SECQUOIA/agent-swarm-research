"""Anisotropic smooth minimum m = eps + (x-a)^2 + g (z-b)^2: rule leaves versus guillotine grid optimum.
Usage: python3 aniso.py"""
import math
import numpy as np
from sep_families import comp, grid, A
from poly1d import from_function
from nd_sep import run, guill_grid

for g in (0.05, 0.01):
    print(f"== (x-a)^2 + {g} (z-b)^2", flush=True)
    for e in (1e-3, 1e-5, 1e-7, 1e-9):
        I1 = from_function(lambda t: (t - A[0]) ** 2, e / 2, K=801, extra=[A[0]])
        I2 = from_function(lambda t, g=g: g * (t - A[1]) ** 2, e / 2, K=801, extra=[A[1]])
        g1, g2 = grid([A[0]], e, [A[0]]), grid([A[1]], e, [A[1]])
        ng = guill_grid([I1, I2], [g1, g2])
        res = {r: run([I1, I2], r, cap=400000) for r in ("omega", "deficit", "multi", "bis")}
        print(f"  eps={e:.0e} N_guill_grid={ng:4d} " + " ".join(f"{r}: leaves={v[1]} nodes={v[0]} ratio={v[1]/ng:.2f}" for r, v in res.items()), flush=True)
