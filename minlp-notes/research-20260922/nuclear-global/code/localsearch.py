"""Swap local search over F1 assignments (primal heuristic, for comparison with listed primal values).
usage: localsearch.py name restarts seed"""
import sys, json, numpy as np
from nucsim import Data, equilibrium, random_asg


def score(r, D):
    # feasible first, then lam_T; infeasible points ranked by peaking excess
    return r["lam_T"] if r["feasible"] else -10 - (r["peak"] - D.c)


def slots_of(D):
    tied = {j: i for i, j in D.ties}
    return [i for i in range(D.N) if i not in tied]


def set_slot(D, typ, s, g):
    typ[s] = g
    for i, j in D.ties:
        if i == s: typ[j] = g


def local_search(D, typ, k1=None):
    S = slots_of(D)
    cur = equilibrium(D, typ, k1); best = score(cur, D)
    improved = True
    while improved:
        improved = False
        for a in range(len(S)):
            for b in range(a + 1, len(S)):
                sa, sb = S[a], S[b]
                if typ[sa] == typ[sb]: continue
                t2 = list(typ); ga, gb = typ[sa], typ[sb]
                set_slot(D, t2, sa, gb); set_slot(D, t2, sb, ga)
                r = equilibrium(D, t2, cur["k1"])
                sc = score(r, D)
                if sc > best + 1e-12:
                    typ, cur, best, improved = t2, r, sc, True
    return typ, cur, best


if __name__ == "__main__":
    name, restarts, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    D = Data(name); rng = np.random.default_rng(seed)
    out = []
    for r in range(restarts):
        typ, cur, sc = local_search(D, random_asg(D, rng))
        out.append(dict(lam_T=cur["lam_T"], feasible=bool(cur["feasible"]), peak=cur["peak"], typ=[int(x) for x in typ]))
        print(f"{name} restart {r}: lam_T={cur['lam_T']:.8f} feasible={cur['feasible']} peak={cur['peak']:.5f} typ={typ}", flush=True)
    json.dump(out, open(f"../runs/ls_{name}_{seed}.json", "w"))
