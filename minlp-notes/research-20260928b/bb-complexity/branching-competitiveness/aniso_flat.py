"""m = eps + gx (x-a)^2 + gz (z-b)^2 with gz in {0, 0.001}: rule leaves (no DP; omega and bisection as references).
Usage: python3 aniso_flat.py"""
import numpy as np
from sep_families import A
from poly1d import from_function
from nd_sep import run

for gx, gz in ((1.0, 0.0), (1.0, 0.001), (10.0, 0.01)):
    print(f"== {gx} (x-a)^2 + {gz} (z-b)^2", flush=True)
    for e in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6):
        I1 = from_function(lambda t: gx * (t - A[0]) ** 2, e / 2, K=801, extra=[A[0]])
        I2 = from_function(lambda t: gz * (t - A[1]) ** 2, e / 2, K=801, extra=[A[1]])
        res = {r: run([I1, I2], r, cap=2_000_000)[1] for r in ("omega", "multi", "bis")}
        print(f"  eps={e:.0e} leaves {res}  multi/omega={res['multi']/res['omega']:.2f}  multi/bis={res['multi']/res['bis']:.2f}", flush=True)
