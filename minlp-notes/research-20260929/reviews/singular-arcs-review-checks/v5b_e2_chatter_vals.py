"""Print the chattering values of v5 precisely (same procedure)."""
import numpy as np
from fractions import Fraction as Fr
import importlib.util
spec = importlib.util.spec_from_file_location('v4', 'v4_e2_discrete.py'); v4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v4)
for N in (50, 100, 200, 400):
    Hp, gp = v4.float_qp(0.5, N)
    c0 = float(v4.cost(*v4.build(Fr(1, 2), N), [Fr(0)]*N))
    rng = np.random.default_rng(1)
    best = None
    for s in [np.where(np.arange(N) % 2 == 0, 1.0, -1.0)] + [rng.uniform(-1, 1, N) for _ in range(30)]:
        uc = v4.solve_float(Hp, gp, [s])
        J = 0.5*uc@Hp@uc + gp@uc + c0
        if best is None or J < best[0]:
            best = (J, uc)
    J, uc = best
    nfree = int(np.sum((uc > -1 + 1e-7) & (uc < 1 - 1e-7)))
    print('N=%d best J over 31 starts = %.8f  fractional stages = %d' % (N, J, nfree), flush=True)
