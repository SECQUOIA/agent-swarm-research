"""Float IEP with only the fresh-fuel slots assigned (depth = #chains), reviewer's implementation.
Unassigned (old-fuel) nodes: k_1 in [min_j kl_{T,j}, max_j kh_{T,j}] (a V-weighted mean of end-of-cycle
values of some slot). Tests whether IEP proves infeasibility of strongly peaking-violating fresh placements.
usage: partial_iep.py name npatterns seed"""
import sys
import numpy as np
from scipy.optimize import linprog
from rv_common import D, equilibrium

nm, npat, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
d = D(nm); rng = np.random.default_rng(seed); N, T = d.N, d.T
tied = {j for _, j in d.S.ties}; partner = dict(d.S.ties)
slots = [i for i in range(N) if i not in tied]
rho = lambda k: max(abs(np.linalg.eigvals(d.G * k[None, :])))


def iep_fresh(freshmask, sweeps=60):
    lo = d.KF - d.a * d.c * (T - 1) * d.maxage
    kl = [np.where(freshmask, d.KF, lo)] + [None] * (T - 1)
    kh = [np.full(N, d.KF)] + [None] * (T - 1)
    last = None
    for s in range(sweeps):
        for t in range(T - 1):
            Ll, Lh = rho(kl[t]), rho(kh[t])
            A = np.vstack([np.diag(np.full(N, Ll)) - kh[t][:, None] * d.G, kl[t][:, None] * d.G - np.diag(np.full(N, Lh))])
            pl, ph = np.zeros(N), np.zeros(N)
            for i in range(N):
                for sg in (1, -1):
                    e = np.zeros(N); e[i] = sg
                    r = linprog(e, A_ub=A, b_ub=np.zeros(2 * N), A_eq=d.V[None], b_eq=[1], bounds=[(0, d.c)] * N, method="highs")
                    if r.status == 2: return "infeasible"
                    (pl if sg == 1 else ph)[i] = sg * r.fun
            nl, nh = kl[t] - d.a * ph, kh[t] - d.a * pl
            kl[t + 1] = nl if kl[t + 1] is None else np.maximum(kl[t + 1], nl)
            kh[t + 1] = nh if kh[t + 1] is None else np.minimum(kh[t + 1], nh)
        old = ~freshmask
        kl[0][old] = np.maximum(kl[0][old], kl[T - 1].min()); kh[0][old] = np.minimum(kh[0][old], kh[T - 1].max())
        ub = rho(kh[T - 1])
        if last is not None and last - ub < 1e-9: break
        last = ub
    return f"{ub:.6f}"


for q in range(npat):
    perm = rng.permutation(d.ng); typ = [None] * N
    for s, g in zip(slots, perm):
        typ[s] = int(g)
        if s in partner: typ[partner[s]] = int(g)
    e = equilibrium(d, typ)
    fm = np.array([d.fresh[g] for g in typ])
    print(f"pattern {q}: value {e['lam']:.6f} peak {e['peak']:.4f} feasible {e['feasible']}; fresh-only IEP: {iep_fresh(fm)}", flush=True)
