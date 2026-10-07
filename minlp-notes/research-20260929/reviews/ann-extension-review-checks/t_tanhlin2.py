"""tanh_lin on wide and extreme intervals: dense sampling at 40 digits plus the interval ends and
the exact stationary points of tanh(s) - alpha s."""
import sys
sys.dont_write_bytecode = True
import numpy as np, mpmath as mp
import annx
rng = np.random.default_rng(9)
n = 300
L = np.concatenate([rng.uniform(-500, 500, n), rng.normal(0, 0.5, n), rng.uniform(-30, 0, n)])
W = np.concatenate([10.0 ** rng.uniform(-3, 3, n), 10.0 ** rng.uniform(-14, -2, n), 10.0 ** rng.uniform(-1, 2, n)])
T = L + W
al, be, de = annx.tanh_lin(L, T)
bad = 0; worst = 0.0
with mp.workdps(40):
    for k in range(len(L)):
        pts = [mp.mpf(float(v)) for v in np.linspace(L[k], T[k], 201)] + [mp.mpf(float(L[k])), mp.mpf(float(T[k]))]
        a = mp.mpf(float(al[k]))
        if 0 < a < 1:
            s0 = mp.acosh(1 / mp.sqrt(a))
            pts += [s for s in (s0, -s0) if mp.mpf(float(L[k])) <= s <= mp.mpf(float(T[k]))]
        for s in pts:
            e = abs(mp.tanh(s) - a * s - mp.mpf(float(be[k])))
            if e > mp.mpf(float(de[k])):
                bad += 1
            if de[k] > 0:
                worst = max(worst, float(e / mp.mpf(float(de[k]))))
print(f"tanh_lin extreme test: {len(L)} intervals (|s| up to 1000, widths 1e-14..1e3), violations {bad}, max |err|/delta {worst:.6f}")
