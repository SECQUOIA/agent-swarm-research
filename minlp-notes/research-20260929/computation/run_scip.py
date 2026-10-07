"""Run SCIP on the probe3 chain family and append one JSON line per solve.

Example:
  python3 run_scip.py --variants default --eps 1e-4 1e-6 --n 2 4 6 8 --seeds 0 1 2 \
      --tl 300 --workers 24 --out scip_default.jsonl
"""
import argparse, json, os, time
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np

import instances as I

# Parameter changes per variant (in addition to limits/time, limits/absgap, limits/gap=0).
VARIANT_PARAMS = {
    "default": {},
    "single": {},  # formulation change only (one nonlinear constraint for the objective)
    "bestfirst": {"nodeselection/bfs/stdpriority": 10**7, "nodeselection/bfs/maxplungedepth": 0},
    "obbt": {"propagating/obbt/freq": 1},
    "emph_opt": "setEmphasis(SCIP_PARAMEMPHASIS.OPTIMALITY)",
    "combo": "formulation 'single' + OPTIMALITY emphasis + bestfirst params + obbt freq 1",
    "warm": "optimal point (local minimizer from x=0) added with addSol before solving",
}


def solve(n, seed, eps, variant, tl, amp=0.3):
    from pyscipopt import SCIP_PARAMEMPHASIS
    m, x, tvars, c = I.build_scip(n, seed, "single" if variant == "combo" else variant, amp=amp)
    m.setParam("timing/clocktype", 1)  # CPU time: time limits are robust to machine load
    m.setParam("limits/time", tl)
    m.setParam("limits/absgap", eps)
    m.setParam("limits/gap", 0.0)
    if variant == "emph_opt":
        m.setEmphasis(SCIP_PARAMEMPHASIS.OPTIMALITY)
    elif variant == "combo":
        m.setEmphasis(SCIP_PARAMEMPHASIS.OPTIMALITY)
        for k, v in {**VARIANT_PARAMS["bestfirst"], **VARIANT_PARAMS["obbt"]}.items():
            m.setParam(k, v)
    elif isinstance(VARIANT_PARAMS[variant], dict):
        for k, v in VARIANT_PARAMS[variant].items():
            m.setParam(k, v)
    fstar_local = None
    if variant == "warm":
        xs, fstar_local = I.local_min(np.zeros(n), c)
        sol = m.createSol()
        for i in range(n):
            m.setSolVal(sol, x[i], float(xs[i]))
            g = xs[i] ** 2 - I.KAPPA * xs[i] ** 4 + (I.B * xs[i] * xs[i + 1] if i < n - 1 else 0.0)
            m.setSolVal(sol, tvars[i], float(g) + 1e-12)
        m.addSol(sol)
    t0 = time.time()
    m.optimize()
    wall = time.time() - t0
    pb, db = m.getPrimalbound(), m.getDualbound()
    rec = dict(family="probe3" if amp == 0.3 else f"probe3_amp{amp}", amp=amp, n=n, seed=seed, eps=eps, variant=variant, tl=tl,
               status=m.getStatus(), nodes=m.getNNodes(), totalnodes=m.getNTotalNodes(),
               time=m.getSolvingTime(), wall=wall, primal=pb, dual=db, absgap=pb - db,
               lpiters=m.getNLPIterations(), maxdepth=m.getMaxDepth(), clock="cpu")
    if fstar_local is not None:
        rec["warm_f"] = fstar_local
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variants", nargs="+", default=["default"])
    ap.add_argument("--eps", nargs="+", type=float, default=[1e-4])
    ap.add_argument("--n", nargs="+", type=int, required=True)
    ap.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2])
    ap.add_argument("--tl", type=float, default=300)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", required=True)
    ap.add_argument("--amp", type=float, default=0.3)
    a = ap.parse_args()
    done = set()
    if os.path.exists(a.out):
        for line in open(a.out):
            r = json.loads(line)
            done.add((r["n"], r["seed"], r["eps"], r["variant"], r["tl"], r.get("amp", 0.3)))
    jobs = [(n, s, e, v, a.tl, a.amp) for v in a.variants for e in a.eps for n in a.n for s in a.seeds]
    jobs = [j for j in jobs if j not in done]
    jobs.sort(key=lambda j: -j[0])  # long jobs first
    with ProcessPoolExecutor(a.workers) as ex, open(a.out, "a") as f:
        futs = {ex.submit(solve, *j): j for j in jobs}
        for fu in as_completed(futs):
            r = fu.result()
            f.write(json.dumps(r) + "\n")
            f.flush()
            print(r["variant"], r["n"], r["seed"], r["eps"], r["status"], r["nodes"],
                  round(r["time"], 1), f"{r['absgap']:.2e}", flush=True)


if __name__ == "__main__":
    main()
