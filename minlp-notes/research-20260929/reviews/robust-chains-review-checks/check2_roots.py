"""Self-test of cg.min_factor; chiral root gaps (P1, P2, P3) n = 3..12; UD root gaps (balanced, unsplit, class (a))."""
import sys, json, time
import numpy as np
from cg import *

rng = np.random.default_rng(1)
worst = 0.0; worst_other = 0.0
for trial in range(300):
    C = rng.normal(size=(4, 4)) * (np.add.outer(np.arange(4), np.arange(4)) <= 3)
    A = PP.poly(rng.normal(size=4)); B = PP([-1, -0.2, 0.4, 1], [rng.normal(size=3), rng.normal(size=3), rng.normal(size=3)])
    lx, ly = rng.uniform(-1, 0.5, 2); ux, uy = lx + rng.uniform(0.02, 1 - lx), ly + rng.uniform(0.02, 1 - ly)
    ux, uy = min(ux, 1), min(uy, 1)
    v, xa, ya = min_factor(C, A, B, lx, ux, ly, uy)
    gx = np.linspace(lx, ux, 1201); gy = np.linspace(ly, uy, 1201)
    X, Y = np.meshgrid(gx, gy, indexing="ij")
    Z = sum(C[i, j] * X**i * Y**j for i in range(4) for j in range(4)) + A(X) + B(Y)
    worst = max(worst, v - Z.min())
print("min_factor self-test: max(claimed min - 1201^2 grid min) over 300 random cubic/piecewise factors =", worst, flush=True)

mode = sys.argv[1] if len(sys.argv) > 1 else "chiral"
if mode == "chiral":
    b, g, ev = 0.6, 0.3, 0.05
    for n in [3, 4, 5, 6, 7, 8, 9, 10, 12]:
        out = dict(n=n)
        for d in (1, 2, 3):
            cb = ClassBound(chiral_chain(n, b, g, ev), poly_tests(d), K=7)
            t0 = time.time()
            lo, up, it = cb.bound(np.full(n, -1.0), np.full(n, 1.0), None, maxit=300, tol=1e-10)
            out[f"P{d}"] = [round(-up, 6), round(-lo, 6), it]
        print(json.dumps(out), flush=True)
else:
    u = ud_u(); B = 0.6
    for n in [3, 4, 5, 6, 8, 10, 12, 16]:
        out = dict(n=n)
        for name, tests, base in [("bal", [PP.poly([0, 1])], "balanced"), ("unsplit", [PP.poly([0, 1])], "unsplit"),
                                  ("a", [PP.poly([0, 1]), PP.poly([0, 0, 1]), u], "balanced")]:
            cb = ClassBound(uniform_chain(n, u, B, base), tests, K=7)
            lo, up, it = cb.bound(np.full(n, -1.0), np.full(n, 1.0), None, maxit=300, tol=1e-10)
            out[name] = [lo, up, it]
        print(json.dumps(out), flush=True)
