"""Certified Lagrangian dual bound for waterno2_T.

    L(lam, mu) = mu * c_hor + sum_W phi_W(lam, mu) <= optimal value,

for any float multipliers lam (free) and mu >= 0, where phi_W is the minimum
of the window problem with the Lagrangian objective.  Each phi_W is bounded
from below by rbb.solve (rigorous B&B; see rbb.py).  The target handed to rbb
is an upper estimate of phi_W minus a small slack; rbb either proves
phi_W >= target or returns the smallest rigorous bound of its open nodes.
The final sum is formed in exact rational arithmetic.

usage: python3 certify.py T multipliers.json windows out.json [workers] [node_limit] [time_limit]
  windows: e.g. "0-1,1-2,..." (half-open ranges t0-t1) or "1" / "2" for a uniform size
"""
import os
import sys
import json
import time
import multiprocessing as mp
from fractions import Fraction

import period
import rbb
import bundle

_D = None


def _init(T):
    global _D
    _D = period.setup(T, os.environ.get("WATERNO2_IMPLIED"))


def upper_estimate(D, t0, t1, lam, mu, tl):
    """Smallest objective value of SCIP incumbents (default and no-propagation
    settings); a feasible point's value is an upper bound on phi_W (up to SCIP's
    feasibility tolerance, which only affects the choice of the target)."""
    vals = []
    for prm in ({}, bundle.NOPROP):
        r = period.solve_window(D, t0, t1, lam, mu, tl, prm)
        if r["x"] is not None:
            vals.append(r["primal"])
    return min(vals) if vals else None


def _certify(args):
    t0, t1, lam, mu, slack, node_limit, time_limit, scip_tl, target_in = args
    D = _D
    tic = time.time()
    ub = target_in if target_in is not None else upper_estimate(D, t0, t1, lam, mu, scip_tl)
    target = ub - max(slack, 1e-7 * abs(ub))
    W = rbb.Window(D, t0, t1)
    c = W.objective(lam, mu)
    obbt_vars = obbt_candidates(W)
    res = rbb.solve(W, c, target, node_limit=node_limit, time_limit=time_limit,
                    obbt_vars=obbt_vars)
    res.update(t0=t0, t1=t1, upper_estimate=ub, target=target, total_time=time.time() - tic)
    return res


def obbt_candidates(W):
    """Continuous arguments of nonlinear monomials (flows, speeds)."""
    s = set()
    for kind, args in W.auxdef:
        for a in args:
            if not W.isbin[a]:
                s.add(a)
    return sorted(s)


def parse_windows(spec, T):
    if "-" not in spec:
        k = int(spec)
        return [(a, min(a + k, T)) for a in range(0, T, k)]
    out = []
    for w in spec.split(","):
        a, b = w.split("-")
        out.append((int(a), int(b)))
    return out


def main():
    T = int(sys.argv[1])
    mult = json.load(open(sys.argv[2]))
    lam, mu = mult["lam"], mult["mu"]
    assert mu >= 0
    windows = parse_windows(sys.argv[3], T)
    cover = sorted(t for a, b in windows for t in range(a, b))
    assert cover == list(range(T)), "windows must partition the horizon"
    out = sys.argv[4]
    workers = int(sys.argv[5]) if len(sys.argv) > 5 else 6
    node_limit = int(sys.argv[6]) if len(sys.argv) > 6 else 100000
    time_limit = float(sys.argv[7]) if len(sys.argv) > 7 else 3600.0
    D = period.setup(T, os.environ.get("WATERNO2_IMPLIED"))
    print("implied bounds:", os.environ.get("WATERNO2_IMPLIED"), len(D["extra"]))
    pool = mp.Pool(workers, initializer=_init, initargs=(T,))
    tic = time.time()
    res = pool.map(_certify, [(a, b, lam, mu, 1e-4, node_limit, time_limit, 120.0, None)
                              for a, b in windows], chunksize=1)
    pool.close()
    total = Fraction(mu) * D["hor_rhs"]
    for r in res:
        total += Fraction(r["bound"])
    ests = mu * float(D["hor_rhs"]) + sum(r["upper_estimate"] for r in res)
    for r in res:
        print(f"window {r['t0']}-{r['t1']-1}: estimate {r['upper_estimate']:.6f} target {r['target']:.6f} "
              f"certified {r['bound']:.6f} status {r['status']} nodes {r['nodes']} time {r['total_time']:.0f}s")
    print(f"sum of estimates (SCIP, not certified): {ests:.6f}")
    down = Fraction(int(total * 10**9 // 1), 10**9)  # rounded down to 9 decimals
    print(f"CERTIFIED Lagrangian bound >= {float(down):.9f}  wall {time.time()-tic:.0f}s")
    json.dump(dict(T=T, windows=windows, lam=[[repr(v) for v in l] for l in lam], mu=repr(mu),
                   results=[{k: v for k, v in r.items()} for r in res],
                   certified_bound_rounded_down=str(down), certified_bound_exact=str(total),
                   estimate=ests), open(out, "w"), indent=1)


if __name__ == "__main__":
    main()
