"""Reviewer: largest value of int_{circle cap B} q_B^{-1/2} ds over boxes B (absolute, not normalised).
Uses curve_integral from key_lemma_stress.py (independent integrator). Usage: python3 circle_sup.py"""
import math, numpy as np
from scipy.optimize import minimize
from key_lemma_stress import curve_integral, circle, box_from
rng = np.random.default_rng(11)
C = circle()
best, bp = 0.0, None
for _ in range(600):
    p = np.concatenate([rng.normal(0, 0.3, 2), np.log(rng.uniform(0.5, 2.6, 2))])
    v = curve_integral(C, *box_from(p, 2), N=3001)[0]
    if v > best: best, bp = v, p
for start in (bp, np.array([0, 0, math.log(2), math.log(2)])):
    r = minimize(lambda x: -curve_integral(C, *box_from(x, 2), N=3001)[0], start, method="Nelder-Mead",
                 options={"maxiter": 400, "xatol": 1e-8, "fatol": 1e-10})
    v, ms, _ = curve_integral(C, *box_from(r.x, 2), N=20001)
    l, u = box_from(r.x, 2)
    print(f"local max {v:.5f} at box [{l[0]:.4f},{u[0]:.4f}]x[{l[1]:.4f},{u[1]:.4f}], local sum M = {ms}; 2pi = {2*math.pi:.5f}; lemma bound 4*pi*sqrt2 = {4*math.pi*math.sqrt(2):.4f}")
