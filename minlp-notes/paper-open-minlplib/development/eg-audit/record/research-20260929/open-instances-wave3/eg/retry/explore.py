"""Float exploration (not rigorous): local minimax solves for every integer assignment
(or a sample of them) to locate near-optimal regions.

    python3 explore.py <name> [nstarts] [seed]
"""
import itertools
import sys
import time

import numpy as np
from scipy.optimize import minimize

import egdata


def local(D, x0, cont, margin=1e-9):
    ci = np.where(cont)[0]
    side = np.arange(24, 28)

    def full(z):
        x = x0.copy()
        x[ci] = z[:-1]
        return x

    def cons(z):
        g, G = D.g(full(z))
        g = g[0]
        return np.concatenate([z[-1] - (D.c[:24] + g[:24]),
                               g[side] - D.glo[side] - margin, D.ghi[side] - g[side] - margin])

    def jac(z):
        g, G = D.g(full(z))
        G = G[0][:, ci]
        J1 = np.hstack([-G[:24], np.ones((24, 1))])
        J2 = np.hstack([G[side], np.zeros((4, 1))])
        J3 = np.hstack([-G[side], np.zeros((4, 1))])
        return np.vstack([J1, J2, J3])
    g0, _ = D.g(x0)
    z0 = np.concatenate([x0[ci], [np.max(D.c[:24] + g0[0][:24])]])
    bnds = [(D.lb[i], D.ub[i]) for i in ci] + [(None, None)]
    keep = np.isfinite(np.concatenate([np.zeros(24), D.glo[side], D.ghi[side]]))
    r = minimize(lambda z: z[-1], z0, jac=lambda z: np.eye(len(z))[-1], bounds=bnds,
                 constraints=[dict(type="ineq", fun=lambda z: cons(z)[keep], jac=lambda z: jac(z)[keep])],
                 method="SLSQP", options=dict(maxiter=300, ftol=1e-14))
    z = r.x.copy()
    z[:-1] = np.clip(z[:-1], [b[0] for b in bnds[:-1]], [b[1] for b in bnds[:-1]])
    x = full(z)
    f, v, _ = D.F(x[None])
    return x, f[0], v[0]


def main(name, nst=20, seed=0):
    D = egdata.Data(name)
    rng = np.random.default_rng(seed)
    cont = ~D.isint
    ints = [np.arange(int(D.lb[i]), int(D.ub[i]) + 1) for i in np.where(D.isint)[0]]
    combos = list(itertools.product(*ints))
    print(f"{name}: {len(combos)} integer assignments, {cont.sum()} continuous", flush=True)
    res = []
    t0 = time.time()
    for comb in combos:
        best = (np.inf, None, None)
        for s in range(nst):
            x0 = D.lb + rng.random(D.d) * (D.ub - D.lb)
            x0[D.isint] = comb
            try:
                x, f, v = local(D, x0, cont)
            except Exception:
                continue
            if v <= 1e-7 and f < best[0]:
                best = (f, x, v)
        res.append((best[0], comb, best[1]))
    res.sort(key=lambda t: t[0])
    for f, comb, x in res[:15]:
        print(f"  {f:.10f} ints {comb} x {None if x is None else np.round(x, 6).tolist()}")
    print(f"time {time.time()-t0:.0f}s")
    np.save(f"logs/explore_{name}.npy", np.array([(r[0],) + tuple(r[1]) for r in res]))


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 20, int(sys.argv[3]) if len(sys.argv) > 3 else 0)
