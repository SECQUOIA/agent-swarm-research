"""diagnostics of saved open boxes (not part of the certificate)"""
import sys
import numpy as np
import ann_tm as at
Z = np.load(sys.argv[1])
M = at.SepModel(); N = M.names
UB, u = at.incumbent(M); M.lag, _ = at.kkt_lag(M, u)
lo, hi, key = Z["lo"], Z["hi"], Z["key"]
sc = M.hi0 - M.lo0
print("open", len(key), "key quantiles", np.quantile(key, [0, 0.01, 0.1, 0.5, 0.9]))
relw = (hi - lo) / sc
print("median rel widths", np.median(relw, axis=0), "max", relw.max(axis=0))
cen = (0.5 * (lo + hi) - M.lo0) / sc
# distance to optimum (normalized)
d = np.linalg.norm(cen - (u - M.lo0) / sc, axis=1)
print("distance to optimum quantiles", np.quantile(d, [0, 0.1, 0.5, 0.9, 1]))
o = np.argsort(key)[:12]
R = M.fbound_combo(lo[o], hi[o], UB)
T = M.tmbound(lo[o], hi[o], UB=UB)
for q, i in enumerate(o):
    c = 0.5 * (lo[i] + hi[i])
    f, g, X, G = M.ffun(c)
    print(f"key {key[i]:.1f} lb {R['lb'][q]:.1f} tm {R['lb_tm'][q]:.1f} old {R['lb_old'][q]:.1f} relw {np.round(relw[i], 5)} cen {np.round(cen[i], 3)} "
          f"f(c) {f:.1f} x647 {X[N.index('x647')]:.4f} x772 {X[N.index('x772')]:.5f} rf {T['rf'][q]:.3g} |af| {np.abs(T['af'][q]).sum():.3g} "
          f"sel {[N[M.side_var[s]] + ('+' if M.side_sgn[s] > 0 else '-') for s, us in zip(T['sel'][q], T['use'][q]) if us]} mu {np.round(T['mu'][q], 1)}")
# cluster analysis: how many open boxes are within distance 0.01 / 0.05 of the optimum
for rr in [0.001, 0.01, 0.05, 0.1, 0.2]:
    print(f"open boxes with center within {rr} of optimum: {np.sum(d < rr)}")
