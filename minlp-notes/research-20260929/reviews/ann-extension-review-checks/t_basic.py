"""basic checks of annx: rigorous tanh, tanh_lin, forward pass at points (vs 50 digits)."""
import sys, time
sys.dont_write_bytecode = True
import numpy as np, mpmath as mp
import annx
rng = np.random.default_rng(1)
# 1. tanh enclosure vs mpmath (60 digits)
z = np.concatenate([rng.normal(0, 3, 3000), rng.uniform(-40, 40, 1000), 10.0 ** rng.uniform(-300, 2, 1000) * rng.choice([-1, 1], 1000), [0.0, -0.0, 5e-324, 1e-320, 19.06, 350.0, -350.0]])
T = annx.itanh_pt(z)
bad = 0; wmax = 0
with mp.workdps(60):
    for k, v in enumerate(z):
        t = mp.tanh(mp.mpf(float(v)))
        if not (mp.mpf(float(T.lo[k])) <= t <= mp.mpf(float(T.hi[k]))):
            bad += 1
        wmax = max(wmax, float((T.hi[k] - T.lo[k]) / max(abs(float(t)), 1e-300)))
print(f"tanh enclosure: {len(z)} points, violations {bad}, max relative width {wmax:.2e}")
# 2. tanh_lin: dense sampling against mpmath
nint = 400
L = rng.normal(0, 2, nint); W = 10.0 ** rng.uniform(-8, 1.3, nint)
L = np.concatenate([L, [-0.5, -3, 0.1, -1e-9]]); W = np.concatenate([W, [1.0, 6.0, 2.0, 2e-9]])
Tt = L + W
al, be, de = annx.tanh_lin(L, Tt)
worst = -1e9; bad = 0
with mp.workdps(40):
    for k in range(len(L)):
        ss = np.concatenate([np.linspace(L[k], Tt[k], 301), [L[k], Tt[k]]])
        for sv in ss:
            e = abs(mp.tanh(mp.mpf(float(sv))) - mp.mpf(float(al[k])) * mp.mpf(float(sv)) - mp.mpf(float(be[k])))
            r = float(e / mp.mpf(float(de[k]))) if de[k] > 0 else (0.0 if e == 0 else 1e9)
            worst = max(worst, r)
            if e > mp.mpf(float(de[k])):
                bad += 1
print(f"tanh_lin: {len(L)} intervals x 303 points: violations {bad}, max |err|/delta = {worst:.6f}")
# tightness: compare delta with the sampled max error (should be close to 1 in ratio worst)
# 3. forward pass on degenerate boxes vs 50-digit evaluation
M = annx.Model()
D = M.D
U = M.lo0 + (M.hi0 - M.lo0) * rng.random((20, 5))
U = np.vstack([U, [370.9280572920674, 0.7863373968889928, 1.620252679906157, 0.9494678019619749, 0.734065236105183]])
m, h, C, A, R, S = M.forward(U, U)
Cf, Af, Rf = M.objective(C, A, R, S)
bad = 0
for n in range(U.shape[0]):
    f, sl, inb = annx.mp_eval(D, U[n])
    ok = (mp.mpf(float(Cf[n] - (Rf[n] + np.abs(Af[n]).sum()) * (1 + 1e-9))) <= f <= mp.mpf(float(Cf[n] + (Rf[n] + np.abs(Af[n]).sum()) * (1 + 1e-9))))
    bad += not ok
    if n >= U.shape[0] - 2:
        print(f"  point {n}: f50 {mp.nstr(f, 20)}  Cf {Cf[n]!r}  rad {Rf[n] + np.abs(Af[n]).sum():.3e}  slack {mp.nstr(sl, 5)}")
print(f"forward/objective at {U.shape[0]} points: enclosure failures {bad}")
t0 = time.time()
lb, info, plain = M.bound(U[-1:] - 1e-6 * (M.hi0 - M.lo0), U[-1:] + 1e-6 * (M.hi0 - M.lo0))
print("box 1e-6 around u*: lb", lb, info, "plain", plain, f"{time.time()-t0:.2f}s")
