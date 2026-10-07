"""Lagrangian probing on pump configurations (exploratory, SCIP estimates).

For multipliers u with Lagrangian value L(u) = mu*c + sum_t phi_t and a cutoff
value UB, a configuration kappa of period t (number of pumps on in each of the
four pump groups) can be excluded if
    L(u) - phi_t + phi_t(kappa) > UB,
where phi_t(kappa) is the period value with the binaries fixed to kappa.  The
certified form is  opt >= min(UB, bound computed on the reduced problem),
which does not require a feasible point of value UB.

usage: python3 probe_config.py T mult.json UB out.json [workers]
"""
import os
import sys
import json
import itertools
import multiprocessing as mp

import numpy as np

import period

_D = None


def _init(T):
    global _D
    _D = period.setup(T, os.environ.get("WATERNO2_IMPLIED"))


def groups(D, t):
    """Pump groups of period t from the ordering rows b_i - b_j >= 0 (chains)."""
    M, S = D["M"], D["S"]
    bins = [v for v in S["per_vars"][t] if M["vt"][v] == "B"]
    nxt = {}
    for i in S["per_rows"][t]:
        r = M["rows"][i]
        p = r["poly"]
        if len(p) == 2 and all(len(k) == 1 and M["vt"][k[0]] == "B" for k in p) and r["lb"] == "0":
            (k1, a1), (k2, a2) = p.items()
            if float(a1) == 1 and float(a2) == -1:
                nxt[k1[0]] = k2[0]
            elif float(a1) == -1 and float(a2) == 1:
                nxt[k2[0]] = k1[0]
    heads = [b for b in bins if b not in nxt.values()]
    out = []
    for h in sorted(heads):
        chain = [h]
        while chain[-1] in nxt:
            chain.append(nxt[chain[-1]])
        out.append(chain)
    assert sorted(v for g in out for v in g) == sorted(bins)
    return out


def configs(D, t):
    G = groups(D, t)
    for counts in itertools.product(*[range(len(g) + 1) for g in G]):
        box = {}
        for g, n in zip(G, counts):
            for k, v in enumerate(g):
                box[v] = (1.0, 1.0) if k < n else (0.0, 0.0)
        yield counts, box


def _task(args):
    t, counts, box, lam, mu = args
    r = period.solve_window(_D, t, t + 1, lam, mu, 120, {}, box)
    val = r["dual"] if r["status"] != "infeasible" else np.inf
    return (t, counts, val, r["primal"] if r["x"] is not None else np.inf, r["status"])


def main():
    T = int(sys.argv[1])
    mult = json.load(open(sys.argv[2]))
    lam, mu = mult["lam"], mult["mu"]
    UB = float(sys.argv[3])
    out = sys.argv[4]
    workers = int(sys.argv[5]) if len(sys.argv) > 5 else 5
    D = period.setup(T, os.environ.get("WATERNO2_IMPLIED"))
    tasks = [(t, counts, box, lam, mu) for t in range(T) for counts, box in configs(D, t)]
    pool = mp.Pool(workers, initializer=_init, initargs=(T,))
    res = pool.map(_task, tasks, chunksize=2)
    pool.close()
    phi = {}
    for (t, counts, val, pr, st) in res:
        phi.setdefault(t, {})[counts] = (val, pr, st)
    best = {t: min(v[1] for v in phi[t].values()) for t in phi}
    L = mu * float(D["hor_rhs"]) + sum(best.values())
    gap = UB - L
    print(f"L(u) (SCIP) = {L:.4f}, UB = {UB}, gap = {gap:.4f}")
    keep = {}
    for t in range(T):
        keep[t] = sorted([c for c, (v, pr, st) in phi[t].items() if v - best[t] <= gap])
        print(f"period {t}: {len(keep[t])} of {len(phi[t])} configurations survive: {keep[t]}")
    json.dump(dict(T=T, UB=UB, L=L, keep={str(t): keep[t] for t in keep},
                   phi={str(t): {str(c): v for c, v in phi[t].items()} for t in phi}), open(out, "w"))


if __name__ == "__main__":
    main()
