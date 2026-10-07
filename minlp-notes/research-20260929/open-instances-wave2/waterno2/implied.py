"""Implied bounds on the tank levels (and other variables) of waterno2_T,
valid for every exactly feasible point of the full problem.

Method: rigorous FBBT on the full-horizon model, then rigorous OBBT over its
LP relaxation (rbb.Window.obbt with no objective cutoff), repeated.  Bounds of
the period variables are then intersected into the period subproblems; since
they are implied by the constraints of the full problem, the Lagrangian bound
of the tightened problem is still a lower bound on the optimum.

usage: python3 implied.py T out.json [rounds]
"""
import sys
import json
import time

import numpy as np

import period
import rbb


def level_vars(D):
    S = D["S"]
    out = []
    for t in range(D["T"] - 1):
        for (i, a, b) in S["link"][t]:
            out += [a, b]
    return sorted(set(out))


def main():
    T = int(sys.argv[1])
    out = sys.argv[2]
    rounds = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    D = period.setup(T)
    W = rbb.Window(D, 0, T)
    tic = time.time()
    lo, hi = W.fbbt(W.lo0, W.hi0)
    lv = [W.loc[v] for v in level_vars(D)]
    # continuous nonlinear arguments (flows, speeds) as well
    nl = sorted({a for kind, args in W.auxdef for a in args if not W.isbin[a]})
    cand = lv if T > 6 else lv + [j for j in nl if j not in lv]
    c = np.zeros(W.n)
    for r in range(rounds):
        res = W.obbt(c, np.inf, lo, hi, cand, 1)
        assert res is not None
        lo, hi = res
        print(f"round {r}: time {time.time()-tic:.0f}s", flush=True)
    M = D["M"]
    bounds = {}
    for j in cand:
        v = W.gv[j]
        bounds[M["names"][v]] = (float(lo[j]), float(hi[j]))
    for v in level_vars(D):
        j = W.loc[v]
        print(M["names"][v], "period", D["per_of"][v], "osil", M["lb"][v], M["ub"][v],
              "implied [%.6f, %.6f]" % (lo[j], hi[j]))
    json.dump(dict(T=T, bounds=bounds), open(out, "w"), indent=0)


if __name__ == "__main__":
    main()
