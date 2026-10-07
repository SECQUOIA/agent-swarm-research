import numpy as np
from bilinear import kappa_pencil, kappa_ok_B
exec(open('rational_kappa.py').read().split("Q, b, c =")[0])
kg = np.unique(np.concatenate([-np.logspace(7, -7, 4000), [0.0], np.logspace(-7, 7, 4000), np.linspace(-20, 20, 40001)]))
for k, (sb, v1, v2, v3, t0, d) in inst.items():
    G0, G1 = kappa_pencil('+', t0, d)
    per = [np.array([kappa_ok_B(G0, G1, '+', v, kk) for kk in kg]) for v in (sb, v1, v2, v3)]
    allok = np.logical_and.reduce(per)
    rng_ = lambda o: (kg[o].min(), kg[o].max()) if o.any() else None
    print(k, 'B kappa sets (grid):', [rng_(o) for o in per], 'intersection:', rng_(allok))
