"""Phase 2 of separator branching: certify pair bounds with rbb and form the
rigorous shortest-path bound.

Targets.  Let E(p) be the planning value of pair p (SCIP estimate; pairs that
SCIP reports infeasible get E = BIG), V_E the shortest path over E, and
G <= V_E the goal.  Pair p on period t gets the target
    tau(p) = E(p) - slack(p) - max(0, (pi(p) - G) / T),
where pi(p) is the best E-path value through p.  For any path P,
sum_{p in P} (pi(p) - G)^+ / T <= max_p (pi(p) - G)^+ <= (sum_P E - G)^+,
so if every pair is certified at its target, every path has certified sum
>= G - sum slack.  Targets only steer the work: whatever rbb returns is a
valid bound, and the final value is the shortest path over the certified
bounds (verify.py recomputes it exactly).

Pairs whose estimate was inherited from an ancestor pair (lazy refinement)
are certified on the ancestor pair's box (one rbb run per ancestor, target =
max over its leaf pairs, which is <= the ancestor's estimate - slack); the
bound is valid for every sub-pair because the box shrinks and the slopes are
the same.

usage: python3 certify_dp.py config.json
"""
import json
import math
import os
import pickle
import sys
import time
import multiprocessing as mp

import numpy as np

import tasks
from dpcells import CellPlan  # noqa: F401

INF = math.inf


def save(P, path):
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        pickle.dump(P, fh)
    os.replace(tmp, path)


def main():
    cfg = json.load(open(sys.argv[1]))
    T = cfg["T"]
    out = cfg["out"]
    logf = open(out + ".log", "a")

    def log(msg):
        print(msg, flush=True)
        logf.write(msg + "\n")
        logf.flush()

    resumed = os.path.exists(out + ".pkl")
    P = pickle.load(open(out + ".pkl" if resumed else cfg["plan"] + ".pkl", "rb"))
    BIG = cfg["big"]
    EST = P.tables["EST"]
    for t in range(T):
        assert not np.isnan(EST[t]).any()
    E = [np.where(np.isinf(EST[t]), BIG, EST[t]) for t in range(T)]
    P.tables["E"] = E
    V, f, g = P.dp("E")
    del P.tables["E"]
    G = min(V, cfg["goal"]) - cfg["margin"]
    log(f"V_E={V:.6f}  goal G={G:.6f}  cells={[len(l) for l in P.leaves]}  resumed={resumed}")
    groups = {}
    for t in range(T):
        fin = np.zeros(1) if t == 0 else f[t - 1]
        gout = np.zeros(1) if t == T - 1 else g[t]
        Pi = fin[:, None] + E[t] + gout[None, :]
        for r in range(P.nrow(t)):
            for c in range(P.ncol(t)):
                rid = P.tables["CSRC"][t][r, c]
                if rid >= 0 and P.crecs[rid]["bound"] >= P.crecs[rid]["target"]:
                    continue  # certified at its target in an earlier (interrupted) run
                e = E[t][r, c]
                own = P.tables["EOWN"][t][r, c] >= 0
                rec = P.erecs[P.tables["ESRC"][t][r, c]]
                key = (t, P.leaf_id(t - 1, r), P.leaf_id(t, c)) if own else (t, rec["cin"], rec["cout"])
                tau = e - max(cfg["slack"], 1e-7 * abs(e)) - max(0.0, (Pi[r, c] - G) / T)
                if key not in groups or tau > groups[key][0]:
                    groups[key] = (tau, e)
    # tight tasks (target close to the estimate) first
    todo = sorted(groups.items(), key=lambda kv: kv[1][1] - kv[1][0])
    ninf = sum(1 for k, (tau, e) in todo if e >= BIG)
    log(f"rbb tasks: {len(todo)} ({ninf} on pairs SCIP reported infeasible)")
    tl = []
    for (key, (tau, e)) in todo:
        t, a, b = key
        lin, lout = P.slopes(t)
        tl.append((key, t, P.cell_box(t - 1, a), P.cell_box(t, b), lin, lout, P.mu, float(tau),
                   cfg["node_limit"], cfg["time_limit"]))
    pool = mp.Pool(cfg["workers"], initializer=tasks.init, initargs=(T, cfg["implied"], True))
    tic = time.time()
    n = nfail = 0
    for key, res in pool.imap_unordered(tasks.rbb_task, tl, chunksize=1):
        t, a, b = key
        rid = len(P.crecs)
        res.update(t=t, cin=a, cout=b)
        P.crecs.append(res)
        for r in P.leaf_positions_under(t - 1, a):
            for c in P.leaf_positions_under(t, b):
                if res["bound"] > P.tables["CB"][t][r, c]:
                    P.tables["CB"][t][r, c] = res["bound"]
                    P.tables["CSRC"][t][r, c] = rid
        n += 1
        if res["bound"] < res["target"]:
            nfail += 1
        if n % 1000 == 0:
            log(f"  {n}/{len(tl)} done, {nfail} below target, {time.time()-tic:.0f}s")
            save(P, out + ".pkl")
    pool.close()
    save(P, out + ".pkl")
    Vc, fc, gc = P.dp("CB")
    times = [r["time"] for r in P.crecs]
    nodes = [r["nodes"] for r in P.crecs]
    log(f"records {len(P.crecs)}; {nfail} of {n} tasks of this run below target; rbb time total "
        f"{sum(times):.0f}s, max {max(times):.0f}s; nodes total {sum(nodes)}; wall {time.time()-tic:.0f}s")
    log(f"DP over certified bounds (float; verify.py gives the exact value): {Vc:.6f} (mu = {P.mu})")


if __name__ == "__main__":
    main()
