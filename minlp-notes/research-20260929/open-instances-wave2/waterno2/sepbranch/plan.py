"""Phase 1 of separator branching (planning, SCIP estimates only; no bounds).

1. Cells: a uniform grid per link (config "breaks"), stored as a split tree.
2. Every leaf pair of every period gets a SCIP estimate (value of SCIP's
   incumbent for the pair subproblem with the Lagrangian slopes of the two
   cells).  The DP over these estimates predicts the separator bound.
3. Refinement: cells on near-optimal estimated paths are split between the two
   copies of the levels that the pair solutions put in the same cell ("jump");
   new pairs inherit the parent's estimate and are re-estimated lazily when
   they lie on a near-optimal estimated path.

Phase 2 (certify_dp.py) certifies the pair bounds with rbb.

usage: python3 plan.py config.json
"""
import json
import math
import os
import pickle
import sys
import time
import multiprocessing as mp

import numpy as np

import core
import terminal
import tasks
from dpcells import CellPlan

INF = math.inf


def link_areas(D):
    out = []
    for t in range(D["T"] - 1):
        area = {e: a for (i, s, e, a) in terminal.balance_rows(D, t)}
        out.append([area[va] for (i, va, vb) in D["S"]["link"][t]])
    return out


def load_slopes(D, cfg):
    """Link slopes: multipliers of the link rows with the horizon multiplier
    folded in (lam_t + mu * area / 3600); any floats give a valid bound."""
    m = json.load(open(cfg["mult"]))
    mu = float(m["mu"])
    return [[float(l[k]) + mu * float(ar[k]) / 3600.0 for k in range(3)]
            for l, ar in zip(m["lam"], link_areas(D))]


def save(P, path):
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        pickle.dump(P, fh)
    os.replace(tmp, path)


def est_tasks(P, pairs, cfg):
    out = []
    for (t, r, c) in pairs:
        cin_id, cout_id = P.leaf_id(t - 1, r), P.leaf_id(t, c)
        lin, lout = P.slopes(t)
        out.append(((t, cin_id, cout_id), t, P.cell_box(t - 1, cin_id), P.cell_box(t, cout_id),
                    lin, lout, P.mu, cfg["scip_tl"]))
    return out


def apply_est(P, key, res):
    t, cin_id, cout_id = key
    rid = len(P.erecs)
    res = dict(res)
    res.update(t=t, cin=cin_id, cout=cout_id)
    P.erecs.append(res)
    rows = P.leaf_positions_under(t - 1, cin_id)
    cols = P.leaf_positions_under(t, cout_id)
    v = res["est"]
    for r in rows:
        for c in cols:
            own = (P.leaf_id(t - 1, r) == cin_id and P.leaf_id(t, c) == cout_id)
            if own:
                P.tables["EOWN"][t][r, c] = rid
            if own or P.tables["EOWN"][t][r, c] < 0:
                P.tables["EST"][t][r, c] = v
                P.tables["ESRC"][t][r, c] = rid


def run_batch(pool, P, pairs, cfg, log):
    if not pairs:
        return
    tic = time.time()
    ts = est_tasks(P, pairs, cfg)
    n = 0
    for key, res in pool.imap_unordered(tasks.scip_task, ts, chunksize=cfg.get("chunk", 2)):
        apply_est(P, key, res)
        n += 1
        if n % 1000 == 0:
            log(f"    {n}/{len(ts)} estimates, {time.time()-tic:.0f}s")
    log(f"  SCIP estimates for {n} pairs in {time.time()-tic:.0f}s")


def choose_split(P, link, pos, f, g, cfg):
    T = P.T
    EST = P.tables["EST"]
    fin = np.zeros(1) if link == 0 else f[link - 1]
    r = int(np.argmin(fin + EST[link][:, pos]))
    gout = np.zeros(1) if link + 1 == T - 1 else g[link + 1]
    c = int(np.argmin(EST[link + 1][pos, :] + gout))
    oin, oout = P.tables["EOWN"][link][r, pos], P.tables["EOWN"][link + 1][pos, c]
    if oin < 0 or oout < 0:
        return "unevaluated"
    e, s = P.erecs[oin]["e"], P.erecs[oout]["s"]
    if e is None or s is None:
        return None
    cell = P.cells[link][P.leaves[link][pos]]
    lo, hi = np.array(cell["lo"]), np.array(cell["hi"])
    w = hi - lo
    e, s = np.array(e), np.array(s)
    score = np.abs(e - s) * np.abs(np.array(P.lam[link]))
    score = np.where(w > cfg["min_width"], score, -1.0)
    k = int(np.argmax(score))
    if score[k] < cfg["min_score"]:
        return None
    m = 0.5 * (e[k] + s[k])
    m = min(max(m, lo[k] + cfg["clamp"] * w[k]), hi[k] - cfg["clamp"] * w[k])
    return k, float(m)


def main():
    cfg = json.load(open(sys.argv[1]))
    T = cfg["T"]
    out = cfg["out"]
    logf = open(out + ".log", "a")

    def log(msg):
        print(msg, flush=True)
        logf.write(msg + "\n")
        logf.flush()

    D = core.setup(T, cfg["implied"])
    poly, lb = terminal.add_terminal_row(D)
    log(f"terminal row {poly} >= {lb}")
    pool = mp.Pool(cfg["workers"], initializer=tasks.init, initargs=(T, cfg["implied"], True))
    if os.path.exists(out + ".pkl"):
        P = pickle.load(open(out + ".pkl", "rb"))
        log(f"resumed: {[len(l) for l in P.leaves]} cells, {len(P.erecs)} estimates")
    else:
        lam = load_slopes(D, cfg)
        log(f"slopes (folded): {[[round(v, 3) for v in l] for l in lam]}")
        P = CellPlan(T, lam, 0.0, [core.level_box(D, t) for t in range(T - 1)])
        for link in range(T - 1):
            P.grid(link, cfg["breaks"])
        log(f"grid cells per link: {[len(l) for l in P.leaves]}")
        pairs = [(t, r, c) for t in range(T) for r in range(P.nrow(t)) for c in range(P.ncol(t))]
        run_batch(pool, P, pairs, cfg, log)
        save(P, out + ".pkl")
    tic = time.time()
    rnd = 0
    while True:
        EST = P.tables["EST"]
        nan = sum(int(np.isnan(EST[t]).sum()) for t in range(T))
        if nan:
            log(f"  {nan} pairs without estimate (SCIP gave no solution and no proof); treated as -1e6")
            for t in range(T):
                EST[t][np.isnan(EST[t])] = -1e6
        V, f, g = P.dp("EST")
        el = time.time() - tic
        log(f"round {rnd} t={el:.0f}s V_est={V:.4f} cells={[len(l) for l in P.leaves]} estimates={len(P.erecs)}")
        if el > cfg["wall"] or V >= cfg["stop_at"]:
            break
        cand = []
        for t in range(T):
            Pi = P.through(t, f, g, "EST")
            mask = (P.tables["EOWN"][t] < 0) & (Pi < V + cfg["delta_eval"])
            for (r, c) in zip(*np.nonzero(mask)):
                cand.append((float(Pi[r, c]), t, int(r), int(c)))
        cand.sort()
        cand = cand[:cfg["batch"]]
        if cand:
            run_batch(pool, P, [(t, r, c) for (p, t, r, c) in cand], cfg, log)
        else:
            cells = []
            for link in range(T - 1):
                psi = f[link] + g[link]
                for pos in np.nonzero(psi < V + cfg["delta_split"])[0]:
                    cells.append((float(psi[pos]), link, int(pos)))
            cells.sort()
            todo = []
            for (p, link, pos) in cells:
                sp = choose_split(P, link, pos, f, g, cfg)
                if sp is None or sp == "unevaluated":
                    continue
                todo.append((link, pos, sp))
                if len(todo) >= cfg["max_split"]:
                    break
            for (link, pos, (k, m)) in todo:
                P.split(link, pos, k, m)
            log(f"  split {len(todo)} cells: {[(l, k, round(m, 3)) for (l, p, (k, m)) in todo]}")
            if not todo:
                log("  nothing to split on near-optimal estimated paths; stop")
                break
        save(P, out + ".pkl")
        rnd += 1
    save(P, out + ".pkl")
    V, f, g = P.dp("EST")
    path = P.best_path(f, g, "EST")
    log(f"final V_est={V:.6f} path {path}")
    for t in range(T):
        r = 0 if t == 0 else path[t - 1]
        c = 0 if t == T - 1 else path[t]
        rid = P.tables["EOWN"][t][r, c]
        rec = P.erecs[rid] if rid >= 0 else None
        log(f"  period {t}: est {P.tables['EST'][t][r, c]:.4f} in {P.cell_box(t - 1, P.leaf_id(t - 1, r))} "
            f"out {P.cell_box(t, P.leaf_id(t, c))} s {rec and rec['s']} e {rec and rec['e']}")
    pool.close()


if __name__ == "__main__":
    main()
