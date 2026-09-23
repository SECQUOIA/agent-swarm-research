"""Stress test for Theorem 12: random factorable DAGs (sums, scalings, products,
exp, sin, cos, sqr, log(c + sqr)), random x*, shapes and scaled points.
Reports the worst |(cv - v)/w^2 + E^cv|, |(cc - v)/w^2 - E^cc| over all factors
for w = 1e-2, 1e-3, 1e-4; the error should decrease linearly in w (C^3 case).
Run with ~/miniconda3/envs/exact-quadratic-hull/bin/python random_factorable.py
"""
import numpy as np
from mccormick_expansion import var, uni, check

def random_expr(rng, nv, depth):
    if depth == 0 or rng.random() < 0.15:
        return var(int(rng.integers(nv))) if rng.random() < 0.85 else 0.0 * var(0) + float(rng.normal())
    r = rng.random()
    a = random_expr(rng, nv, depth - 1)
    if r < 0.25:
        return a + random_expr(rng, nv, depth - 1)
    if r < 0.35:
        return float(rng.normal()) * a
    if r < 0.65:
        return a * random_expr(rng, nv, depth - 1)
    name = rng.choice(["exp", "sin", "cos", "sqr", "log"])
    if name == "log":
        return uni("log", 0.5 + uni("sqr", a))
    if name == "exp":
        return uni("exp", 0.3 * a)
    return uni(name, a)

if __name__ == "__main__":
    rng = np.random.default_rng(1)
    worst_ratio = 0.0
    for t in range(25):
        nv = int(rng.integers(2, 4))
        e = random_expr(rng, nv, 5)
        xs = rng.normal(size=nv) * 0.8
        xs[rng.random(nv) < 0.3] = 0.0           # degenerate points
        errs = check(f"random #{t}", e, xs, nsamp=60, ws=(1e-2, 1e-3, 1e-4), seed=t)
        if errs[-2] > 1e-7:     # below this the error is floating-point rounding / w^2
            worst_ratio = max(worst_ratio, errs[-1] / errs[-2])
    print(f"\nmax over expressions (error above rounding level) of err(1e-4)/err(1e-3): "
          f"{worst_ratio:.3f} (linear rate gives 0.1)")
