"""Spot check of the reported local/sampled contraction numbers (float, finite differences).
usage: spot_contraction.py name npatterns npoints seed"""
import sys
import numpy as np
from rv_common import D, cycle, equilibrium

nm, npat, npt, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
d = D(nm); rng = np.random.default_rng(seed)
tied = {j for _, j in d.S.ties}; partner = dict(d.S.ties)
slots = [i for i in range(d.N) if i not in tied]
lo = d.KF - d.a * d.c * (d.T - 1) * d.maxage
m = d.maxage + 1
for q in range(npat):
    perm = rng.permutation(d.ng); typ = [None] * d.N
    for s, g in zip(slots, perm):
        typ[s] = int(g)
        if s in partner: typ[partner[s]] = int(g)
    f, R = d.reload(typ)
    Phi = lambda k: d.KF * f + R @ cycle(d, k)[0][-1]
    def Phim(k):
        for _ in range(m): k = Phi(k)
        return k
    def jac(F, k, h=1e-6):
        J = np.zeros((d.N, d.N))
        for j in range(d.N):
            e = np.zeros(d.N); e[j] = h; J[:, j] = (F(k + e) - F(k - e)) / (2 * h)
        return J
    e = equilibrium(d, typ)
    rhoJ = max(abs(np.linalg.eigvals(jac(Phi, e["k1"]))))
    worst = max(np.abs(jac(Phim, rng.uniform(lo, d.KF, d.N))).sum(1).max() for _ in range(npt))
    print(f"pattern {q}: lam_T {e['lam']:.6f} feasible {e['feasible']} rho(dPhi at fp) {rhoJ:.3f} max ||d(Phi^{m})||_inf over {npt} box points {worst:.3f}")
