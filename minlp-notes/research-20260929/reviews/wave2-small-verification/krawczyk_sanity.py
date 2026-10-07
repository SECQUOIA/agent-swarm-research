"""Negative controls for krawczyk.test (not part of the proof): a centre moved
off the solution by 1e-8 in one coordinate, or a radius too small to contain the
solution, must fail; the unperturbed case must pass."""
import numpy as np
from mpmath import iv

import common
import krawczyk
import v_lindo

m = common.load("rocket100")
fixed, U, rows, x0, info = v_lindo.setup_rocket(m, 100)
iv.dps = 40
xt, res = krawczyk.newton_polish(m, rows, U, x0, fixed, iters=3)
r = 1e-12 * np.maximum(1.0, np.abs(xt))
print("unperturbed:", krawczyk.test(m, rows, U, xt, r, fixed)[0]["ok"])
xb = xt.copy(); xb[150] += 1e-8
print("centre moved by 1e-8, r=1e-12:", krawczyk.test(m, rows, U, xb, r, fixed)[0]["ok"])
print("centre moved by 1e-8, r=1e-6 (contains solution):", krawczyk.test(m, rows, U, xb, 1e-6 * np.maximum(1.0, np.abs(xt)), fixed)[0]["ok"])
