"""Diagnostics claimed in extension.md Section 5: active constraints and reduced Hessian at u*,
x772 and distance to the optimum at the centres of the 1800 s frontier boxes."""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import sys
sys.dont_write_bytecode = True
import numpy as np, mpmath as mp
import annx, annv
M = annx.Model(); D = M.D; N = D["N"]; idx = D["idx"]
ustar = [370.9280572920674, 0.7863373968889928, 1.620252679906157, 0.9494678019619749, 0.734065236105183]
lo0, hi0 = M.lo0, M.hi0; W = hi0 - lo0
mp.mp.dps = 40
q = lambda F: mp.mpf(F.numerator) / F.denominator
def ev(u):
    x = annv.forward_mp(D, u)
    return annv.fobj(D, x, q), x
f0, x0 = ev([mp.mpf(v) for v in ustar])
act = []
for j, lo, hi in D["cb"]:
    for b, s in ((lo, 1), (hi, -1)):
        if b is not None and abs(x0[j] - q(b)) < mp.mpf("1e-9"):
            act.append((N[j], s, float(x0[j])))
print("f(u*) =", mp.nstr(f0, 20), " active bounds (|x - b| < 1e-9):", act)
print("inputs at bounds:", [(i, float(ustar[i]), float(lo0[i]), float(hi0[i])) for i in range(5) if abs(ustar[i] - lo0[i]) < 1e-12 or abs(ustar[i] - hi0[i]) < 1e-12])
lam = {"x647": mp.mpf("58.509053436320386"), "x772": mp.mpf("20891.433722402617")}
def L(t):   # t: normalized coords offset
    u = [mp.mpf(ustar[i]) + t[i] * mp.mpf(float(W[i])) for i in range(5)]
    f, x = ev(u)
    return f - lam["x647"] * (x[idx["x647"]] + 1) - lam["x772"] * (x[idx["x772"]] - mp.mpf("0.999")), x[idx["x647"]], x[idx["x772"]]
h = mp.mpf("1e-5")
e = lambda i: [h if k == i else 0 for k in range(5)]
L0, g0a, g0b = L([0] * 5)
H = mp.matrix(5, 5); ga = mp.matrix(5, 1); gb = mp.matrix(5, 1); gL = mp.matrix(5, 1)
for i in range(5):
    Lp, ap, bp = L(e(i)); Lm, am, bm = L([-v for v in e(i)])
    ga[i] = (ap - am) / (2 * h); gb[i] = (bp - bm) / (2 * h); gL[i] = (Lp - Lm) / (2 * h)
    H[i, i] = (Lp - 2 * L0 + Lm) / h ** 2
    for k in range(i + 1, 5):
        pp = L([e(i)[r] + e(k)[r] for r in range(5)])[0]; pm = L([e(i)[r] - e(k)[r] for r in range(5)])[0]
        mp_ = L([-e(i)[r] + e(k)[r] for r in range(5)])[0]; mm = L([-e(i)[r] - e(k)[r] for r in range(5)])[0]
        H[i, k] = H[k, i] = (pp - pm - mp_ + mm) / (4 * h * h)
print("grad of Lagrangian (normalized coords):", [mp.nstr(v, 4) for v in gL])
print("grad x647:", [mp.nstr(v, 4) for v in ga], " grad x772:", [mp.nstr(v, 4) for v in gb])
G = np.array([[float(ga[i]) for i in range(5)], [float(gb[i]) for i in range(5)]])
Hn = np.array([[float(H[i, k]) for k in range(5)] for i in range(5)])
# tangent space of the constraints active among x647, x772 (and input bounds if any)
Q, _ = np.linalg.qr(G.T, mode="complete")
Z = Q[:, 2:]
print("eig full Hessian of L (normalized):", np.round(np.linalg.eigvalsh(Hn), 3))
print("eig reduced Hessian Z'HZ (tangent of x647, x772):", np.round(np.linalg.eigvalsh(Z.T @ Hn @ Z), 3))
# frontier diagnostics (1800 s)
Zf = np.load(_REPRO_ROOT + "/research-20260929/open-instances-wave3/ann/ext_logs/open1800_v1.npz")
FM = annx.float_model()
cen = 0.5 * (Zf["lo"] + Zf["hi"])
f, s, X = FM.eval(cen)
x772 = X[idx["x772"]]; x647 = X[idx["x647"]]
d = np.linalg.norm((cen - np.array(ustar)) / W, axis=1)
print(f"1800 s frontier: {len(cen)} boxes; centre x772 quantiles (1,10,50,90,99%) {np.round(np.quantile(x772, [0.01, 0.1, 0.5, 0.9, 0.99]), 5)}")
print(f"  centre x647 quantiles {np.round(np.quantile(x647, [0.01, 0.1, 0.5, 0.9, 0.99]), 4)}; share with centre x772 >= 0.999: {(x772 >= 0.999).mean():.3f}")
print(f"  normalized distance to u*: quantiles (0,10,50,90,100%) {np.round(np.quantile(d, [0, 0.1, 0.5, 0.9, 1]), 3)}")
print(f"  f(centre) - UB quantiles {np.round(np.quantile(f + 3379.982394046125, [0.01, 0.1, 0.5, 0.9, 0.99]), 2)}")
Z2 = np.load(_REPRO_ROOT + "/research-20260929/open-instances-wave3/ann/ext_logs/open_run2.npz")
cen = 0.5 * (Z2["lo"] + Z2["hi"]); f, s, X = FM.eval(cen); d = np.linalg.norm((cen - np.array(ustar)) / W, axis=1)
print(f"run-2 frontier: {len(cen)} boxes; centre x772 quantiles {np.round(np.quantile(X[idx['x772']], [0.01, 0.1, 0.5, 0.9, 0.99]), 5)}; "
      f"distance quantiles {np.round(np.quantile(d, [0, 0.1, 0.5, 0.9, 1]), 3)}")
