"""Certification for a cell-slope plan: rbb runs on the leaf pairs that need them.

Every leaf pair (D, D') of period t already has a rigorous bound from earlier
records (cert3 records and earlier runs), corrected for the change of slopes:
    B_r + min_{s in D}(l_D - a_in).s + min_{e in D'} -(l_D' - a_out).e
(cs.State.tables, float here; verify_cs.py recomputes the bound exactly).

Targets (as in ../sepbranch/certify_dp.py).  E(p) is the planning value (SCIP
pool estimate at the current slopes; BIG for pairs SCIP reports infeasible),
V_E the shortest path over E, G = min(V_E, goal) - margin, and
    tau(p) = E(p) - max(slack, 1e-7 |E(p)|) - max(0, (pi(p) - G) / T),
pi(p) the best E-path value through p.  A pair is skipped if its present
rigorous bound is >= tau(p), or if every path through it already has a
rigorous value >= G + skip_margin under the present rigorous bounds (bounds
only grow, so such a pair cannot bring the final value below G + skip_margin).
Whatever rbb returns is a valid bound; targets only steer the work.

usage: python3 certify_cs.py config.json
"""
import json
import math
import os
import pickle
import sys
import time
import multiprocessing as mp

import numpy as np

import cs

INF = math.inf


def save(st, path):
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        pickle.dump(st, fh)
    os.replace(tmp, path)


def plan_tasks(st, cfg, log):
    T = st.T
    inc = st.incidence()
    tab = st.tables(inc)
    M = st.model(tab)
    BIG = cfg["big"]
    E = [np.where(np.isinf(m), BIG, m) for m in M]
    for t in range(T):
        E[t] = np.where(tab[t]["L"] == INF, INF, E[t])
    VE, f, g = st.dp(E)
    G = min(VE, cfg["goal"]) - cfg["margin"]
    Lt = [d["L"] for d in tab]
    VL, fL, gL = st.dp(Lt)
    log(f"V_E={VE:.6f}  G={G:.6f}  present rigorous DP (float)={VL:.6f}  cells={[len(l) for l in st.leaves]}")
    todo = []
    nskip_path = nskip_L = 0
    for t in range(T):
        PiE = st.through(E, t, f, g)
        PiL = st.through(Lt, t, fL, gL)
        for r in range(st.nrow(t)):
            for c in range(st.ncol(t)):
                L = Lt[t][r, c]
                if L == INF:
                    continue
                if PiL[r, c] >= G + cfg["skip_margin"]:
                    nskip_path += 1
                    continue
                e = E[t][r, c]
                tau = e - max(cfg["slack"], 1e-7 * abs(e)) - max(0.0, (PiE[r, c] - G) / T)
                if L >= tau:
                    nskip_L += 1
                    continue
                todo.append((float(e - tau), t, r, c, float(tau), bool(tab[t]["FRESH"][r, c]), float(PiE[r, c] - G)))
    todo.sort()
    log(f"rbb tasks {len(todo)} ({sum(1 for x in todo if not x[5])} with a stale estimate); skipped {nskip_path} "
        f"(paths already >= G+{cfg['skip_margin']}), {nskip_L} (present bound >= target)")
    return todo, G


def main():
    cfg = json.load(open(sys.argv[1]))
    out = cfg["out"]
    logf = open(out + ".log", "a")

    def log(msg):
        print(msg, flush=True)
        logf.write(msg + "\n")
        logf.flush()

    st = pickle.load(open(out + ".pkl" if os.path.exists(out + ".pkl") else cfg["plan"], "rb"))
    T = st.T
    tic0 = time.time()
    if cfg.get("refresh_stale"):
        # SCIP estimates at the current slopes for task pairs whose estimate is stale
        # (planning values only; they set better rbb targets)
        from plan_cs import Planner
        PL = Planner(dict(cfg, workers=cfg["workers"]), st, log)
        for it in range(cfg["refresh_stale"]):
            todo, G = plan_tasks(st, cfg, log)
            stale = [(t, r, c) for (gap, t, r, c, tau, fr, pig) in todo if not fr and pig < cfg["refresh_window"]]
            if not stale:
                break
            tic = time.time()
            PL.evaluate(stale)
            log(f"refreshed {len(stale)} stale estimates in {time.time()-tic:.0f}s (SCIP cpu so far {PL.scip_cpu:.0f}s)")
            save(st, out + ".pkl")
        PL.pool.close()
    pool = mp.Pool(cfg["workers"], initializer=cs.init_worker, initargs=(T, cfg["implied"], True))
    for rnd in range(cfg.get("rounds", 1)):
        todo, G = plan_tasks(st, cfg, log)
        if not todo:
            break
        tl = []
        for (gap, t, r, c, tau, fr, pig) in todo:
            cin, cout = st.rcid(t, r), st.ccid(t, c)
            lin, lout = st.pair_slopes(t, cin, cout)
            bin_ = None if cin < 0 else tuple(map(list, st.leaf_box(t - 1, cin)))
            bout = None if cout < 0 else tuple(map(list, st.leaf_box(t, cout)))
            tl.append(((t, cin, cout), t, bin_, bout, lin, lout, tau, cfg["node_limit"], cfg["time_limit"]))
        tic = time.time()
        n = nfail = 0
        cpu = 0.0
        for key, res in pool.imap_unordered(cs.rbb_task, tl, chunksize=1):
            t, cin, cout = key
            res.update(t=t, cin=cin, cout=cout, src=("cellslopes", out, rnd))
            st.recs.append(res)
            n += 1
            cpu += res["time"]
            if res["bound"] < res["target"]:
                nfail += 1
            if n % 1000 == 0:
                log(f"  {n}/{len(tl)} done, {nfail} below target, {time.time()-tic:.0f}s")
                save(st, out + ".pkl")
        save(st, out + ".pkl")
        log(f"round {rnd}: {n} rbb runs, {nfail} below target, rbb cpu {cpu:.0f}s, wall {time.time()-tic:.0f}s")
    tab = st.tables()
    VL = st.dp([d["L"] for d in tab])[0]
    log(f"DP over rigorous bounds (float; verify_cs.py gives the exact value): {VL:.6f}; wall {time.time()-tic0:.0f}s")
    pool.close()


if __name__ == "__main__":
    main()
