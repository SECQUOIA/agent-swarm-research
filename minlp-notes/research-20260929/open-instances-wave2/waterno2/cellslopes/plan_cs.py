"""Planning with cell-dependent slopes (SCIP estimates only; no bounds).

Loop (trust-region ascent on the cell slopes, with lazy SCIP evaluation):
  1. lazy evaluation at the current slopes: every pair whose path value in the
     planning DP is within delta_eval of the optimum and that has not been
     evaluated by SCIP at its current slopes is evaluated (all SCIP solutions
     become pool points); repeat until no such pair is left;
  2. slope LP (cs.slope_lp) with trust region delta -> candidate slopes;
  3. lazy evaluation at the candidate slopes;
  4. accept if the planning value rose, else revert (the new points stay in
     the pool) and shrink delta;
  5. every `split_every` iterations, or when delta is below `delta_min`, split
     cells on near-optimal paths between the two copies of the levels that the
     best pair points put in the same cell (as in ../sepbranch/plan.py).

usage: python3 plan_cs.py config.json
"""
import copy
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


class Planner:
    def __init__(self, cfg, st, log):
        self.cfg, self.st, self.log = cfg, st, log
        self.pool = mp.Pool(cfg["workers"], initializer=cs.init_worker, initargs=(st.T, cfg["implied"], True))
        self.nscip = 0
        self.scip_cpu = 0.0

    def evaluate(self, pairs):
        st, cfg = self.st, self.cfg
        tl = []
        for (t, r, c) in pairs:
            cin, cout = st.rcid(t, r), st.ccid(t, c)
            lin, lout = st.pair_slopes(t, cin, cout)
            bin_ = None if cin < 0 else tuple(map(list, st.leaf_box(t - 1, cin)))
            bout = None if cout < 0 else tuple(map(list, st.leaf_box(t, cout)))
            tl.append(((t, cin, cout, tuple(lin), tuple(lout)), t, bin_, bout, lin, lout, cfg["scip_tl"],
                       cfg["maxsols"]))
        for key, res in self.pool.imap_unordered(cs.scip_task, tl, chunksize=1):
            t, cin, cout, lin, lout = key
            st.add_eval(t, cin, cout, list(lin), list(lout), res)
            self.nscip += 1
            self.scip_cpu += res["time"]

    def state_value(self):
        st = self.st
        inc = st.incidence()
        tab = st.tables(inc)
        M = st.model(tab)
        V, f, g = st.dp(M)
        return V, f, g, M, tab, inc

    def lazy(self, delta_eval, cap, max_rounds=20):
        st = self.st
        n0 = self.nscip
        for rnd in range(max_rounds):
            V, f, g, M, tab, inc = self.state_value()
            cand = []
            for t in range(st.T):
                Pi = st.through(M, t, f, g)
                mask = (~tab[t]["FRESH"]) & (Pi < V + delta_eval)
                for r, c in zip(*np.nonzero(mask)):
                    cand.append((float(Pi[r, c]), t, int(r), int(c)))
            if not cand:
                break
            cand.sort()
            cand = cand[:cap]
            tic = time.time()
            self.evaluate([(t, r, c) for (p, t, r, c) in cand])
            self.log(f"    lazy round {rnd}: V={V:.4f}, evaluated {len(cand)} pairs in {time.time()-tic:.0f}s")
        V, f, g, M, tab, inc = self.state_value()
        return V, self.nscip - n0

    def split_round(self, delta_split, max_split):
        st, cfg = self.st, self.cfg
        V, f, g, M, tab, inc = self.state_value()
        T = st.T
        cells = []
        for link in range(T - 1):
            psi = f[link] + g[link]
            for pos in np.nonzero(psi < V + delta_split)[0]:
                cells.append((float(psi[pos]), link, int(pos)))
        cells.sort()
        todo = []
        for (p, link, pos) in cells:
            fin = np.zeros(1) if link == 0 else f[link - 1]
            r = int(np.argmin(fin + M[link][:, pos]))
            gout = np.zeros(1) if link + 1 == T - 1 else g[link + 1]
            c = int(np.argmin(M[link + 1][pos, :] + gout))
            pin = tab[link]["UARG"][r, pos]
            pout = tab[link + 1]["UARG"][pos, c]
            if pin < 0 or pout < 0:
                continue
            e = np.array(st.pts[link][pin][1])
            s = np.array(st.pts[link + 1][pout][0])
            cid = st.leaves[link][pos]
            lo, hi = st.leaf_box(link, cid)
            w = hi - lo
            score = np.abs(e - s) * np.abs(np.array(st.lam[link][cid]))
            score = np.where(w > cfg["min_width"], score, -1.0)
            k = int(np.argmax(score))
            if score[k] < cfg["min_score"]:
                continue
            m = 0.5 * (e[k] + s[k])
            m = min(max(m, lo[k] + cfg["clamp"] * w[k]), hi[k] - cfg["clamp"] * w[k])
            todo.append((link, cid, k, float(m)))
            if len(todo) >= max_split:
                break
        for (link, cid, k, m) in todo:
            st.split(link, cid, k, m)
        self.log(f"  split {len(todo)} cells: {[(l, k, round(m, 3)) for (l, c, k, m) in todo]}")
        return len(todo)


def main():
    cfg = json.load(open(sys.argv[1]))
    out = cfg["out"]
    logf = open(out + ".log", "a")

    def log(msg):
        print(msg, flush=True)
        logf.write(msg + "\n")
        logf.flush()

    if os.path.exists(out + ".pkl"):
        st = pickle.load(open(out + ".pkl", "rb"))
        log(f"resumed {out}.pkl")
    else:
        st = pickle.load(open(cfg["start"], "rb"))
        log(f"start from {cfg['start']}")
    PL = Planner(cfg, st, log)
    delta = np.array(cfg.get("delta_now", cfg["delta"]), float)
    tic = time.time()
    V, n = PL.lazy(cfg["delta_eval"], cfg["cap"])
    log(f"init: V={V:.4f} after {n} SCIP evaluations, {time.time()-tic:.0f}s; cells {[len(l) for l in st.leaves]}")
    save(st, out + ".pkl")
    it = 0
    since_split = 0
    while time.time() - tic < cfg["wall"]:
        it += 1
        t0 = time.time()
        Vc, fc, gc, Mc, tab, inc = PL.state_value()
        active = None
        if cfg.get("lp_cells"):
            cand = []
            for link in range(st.T - 1):
                psi = fc[link] + gc[link]
                for pos in np.nonzero(psi < Vc + cfg["lp_cell_delta"])[0]:
                    cand.append((float(psi[pos]), link, int(pos)))
            cand.sort()
            active = [np.zeros(len(st.leaves[l]), bool) for l in range(st.T - 1)]
            for (p, link, pos) in cand[:cfg["lp_cells"]]:
                active[link][pos] = True
        z, new, info = cs.slope_lp(st, tab, inc, delta, active=active, pmargin=cfg.get("pmargin", INF))
        old = [st.lam_arr(l) for l in range(st.T - 1)]
        cs.set_slopes(st, new)
        moved = sum(int((np.abs(new[l] - old[l]).max(1) > 1e-9).sum()) for l in range(st.T - 1))
        Vn, n = PL.lazy(cfg["delta_eval"], cfg["cap"])
        acc = Vn > V + 1e-6
        if acc:
            gain = Vn - V
            V = Vn
            delta = np.minimum(delta * cfg["grow"], cfg["delta_max"])
        else:
            cs.set_slopes(st, old)
            delta = delta * cfg["shrink"]
            Vb, n2 = PL.lazy(cfg["delta_eval"], cfg["cap"])
            n += n2
            V = Vb
        log(f"it {it} t={time.time()-tic:.0f}s LP z={z:.4f} (rows {info['rows']}, {info['time']:.0f}s) moved {moved} "
            f"V_new={Vn:.4f} {'ACCEPT' if acc else 'reject'} V={V:.4f} delta={np.round(delta, 3).tolist()} "
            f"evals {n} ({time.time()-t0:.0f}s) SCIP total {PL.nscip} cpu {PL.scip_cpu:.0f}s "
            f"cells {[len(l) for l in st.leaves]} pts {[len(p) for p in st.pts]}")
        since_split += 1
        if since_split >= cfg["split_every"] or delta[0] < cfg["delta_min"]:
            ns = PL.split_round(cfg["delta_split"], cfg["max_split"])
            V, n = PL.lazy(cfg["delta_eval"], cfg["cap"])
            log(f"  after split: V={V:.4f} ({n} evaluations) t={time.time()-tic:.0f}s SCIP total {PL.nscip} cpu {PL.scip_cpu:.0f}s cells {[len(l) for l in st.leaves]}")
            since_split = 0
            if delta[0] < cfg["delta_min"]:
                delta = np.array(cfg["delta"], float)
        save(st, out + ".pkl")
        if V >= cfg["stop_at"]:
            break
    log(f"final V={V:.6f}; SCIP evaluations {PL.nscip}, cpu {PL.scip_cpu:.0f}s; wall {time.time()-tic:.0f}s")
    save(st, out + ".pkl")
    PL.pool.close()


if __name__ == "__main__":
    main()
