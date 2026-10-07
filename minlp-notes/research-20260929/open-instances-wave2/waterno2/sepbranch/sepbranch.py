"""Separator branching for waterno2_T: cells on the tank-level links, rigorous
period bounds per (entry cell, exit cell) pair, dynamic programming over the
periods, adaptive refinement of the cells on near-optimal DP paths.

Bound.  For every link t (period t -> t+1) the cells P_t cover the level box
of that link.  Every feasible x has a cell sequence D_0, ..., D_{T-2} with
x's link-t levels in D_t.  Since the link residuals of x are zero,

    f(x) = sum_t cost_t(x) + sum_t lam_t . (s_{t+1}(x) - e_t(x))
         + mu (c - sum_t h_t(x)) + [nonpositive]                   (mu >= 0)
         >= sum_t phi_t(D_{t-1}, D_t)        (core.PeriodBounder),

so  optimum >= mu*c + min over cell sequences of sum_t B_t(D_{t-1}, D_t)
for any rigorous lower bounds B_t of the pair values (a shortest path).
The slopes lam_t (one per link) and mu are fixed floats; any values are valid.

Inheritance.  When a cell is split, the pairs of its two children inherit the
parent pair's bound: the child box is a subset and the objective is the same.

Refinement.  Pairs on near-optimal DP paths are evaluated (SCIP supplies only a
target and a solution; rbb supplies the bound).  When the near-optimal paths
are fully evaluated, their cells are split between the two copies of the
levels that the pair solutions put in the same cell (the "jump").

usage: python3 sepbranch.py config.json
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

HERE = os.path.dirname(os.path.abspath(__file__))
INF = math.inf
_W = {}


# ---------------------------------------------------------------- workers
def _init(T, implied, term):
    D = core.setup(T, implied)
    if term:
        terminal.add_terminal_row(D)
    _W["D"] = D
    _W["PB"] = {}


def _levels(D, t, x):
    S = D["S"]
    s = [x[b] for (i, a, b) in S["link"][t - 1]] if t > 0 else None
    e = [x[a] for (i, a, b) in S["link"][t]] if t < D["T"] - 1 else None
    return s, e


def _task(a):
    import period
    import bundle
    (t, cin, cout, lam_in, lam_out, mu, cap, node_limit, time_limit, scip_tl) = a
    D = _W["D"]
    T = D["T"]
    if t not in _W["PB"]:
        _W["PB"][t] = core.PeriodBounder(D, t)
    PB = _W["PB"][t]
    cin = None if cin is None else (np.array(cin[0]), np.array(cin[1]))
    cout = None if cout is None else (np.array(cout[0]), np.array(cout[1]))
    tic = time.time()
    # SCIP: target and solution only (never a bound)
    box = {}
    S = D["S"]
    if cin is not None:
        for k, (i, va, vb) in enumerate(S["link"][t - 1]):
            box[vb] = (float(cin[0][k]), float(cin[1][k]))
    if cout is not None:
        for k, (i, va, vb) in enumerate(S["link"][t]):
            box[va] = (float(cout[0][k]), float(cout[1][k]))
    lam = [[0.0, 0.0, 0.0] for _ in range(T - 1)]
    if t > 0:
        lam[t - 1] = list(lam_in)
    if t < T - 1:
        lam[t] = list(lam_out)
    est, s, e, sst = INF, None, None, "none"
    try:
        r = period.solve_window(D, t, t + 1, lam, mu, scip_tl, bundle.NOPROP, box)
        sst = r["status"]
        if r["x"] is not None:
            est = r["primal"]
            s, e = _levels(D, t, r["x"])
    except ValueError:
        sst = "empty"
    tscip = time.time() - tic
    target = min(est - max(1e-4, 1e-7 * abs(est)), cap) if est < INF else cap
    res = PB.bound(cin, cout, lam_in, lam_out, mu, target, node_limit=node_limit, time_limit=time_limit)
    return dict(bound=float(res["bound"]), status=res["status"], nodes=int(res.get("nodes", 0)),
                t_rbb=float(res.get("time", 0.0)), t_scip=tscip, est=float(est), scip_status=sst,
                target=float(target), s=s, e=e, lam_in=[float(v) for v in lam_in],
                lam_out=[float(v) for v in lam_out], mu=float(mu), cin_box=a[1], cout_box=a[2])


# ---------------------------------------------------------------- state
class State:
    def __init__(self, T, lam, mu, boxes):
        self.T, self.lam, self.mu = T, lam, mu
        # cells[t]: list of dict(lo, hi, parent, split=(k, m, c1, c2) or None)
        self.cells = [[dict(lo=list(map(float, lo)), hi=list(map(float, hi)), parent=None, split=None)]
                      for (lo, hi) in boxes]
        self.leaves = [[0] for _ in range(T - 1)]
        self.records = []
        # tables per period: B (bound), SRC (record id giving B, -1: none), OWN (own record id, -1)
        self.B = [np.full((1, 1), -INF) for _ in range(T)]
        self.SRC = [np.full((1, 1), -1, dtype=np.int64) for _ in range(T)]
        self.OWN = [np.full((1, 1), -1, dtype=np.int64) for _ in range(T)]

    def nrow(self, t):
        return 1 if t == 0 else len(self.leaves[t - 1])

    def ncol(self, t):
        return 1 if t == self.T - 1 else len(self.leaves[t])

    def cell_of(self, link, pos):
        if link < 0 or link >= self.T - 1:
            return None
        c = self.cells[link][self.leaves[link][pos]]
        return (c["lo"], c["hi"])

    def cell_id(self, link, pos):
        if link < 0 or link >= self.T - 1:
            return -1
        return self.leaves[link][pos]

    def split(self, link, pos, k, m):
        cid = self.leaves[link][pos]
        c = self.cells[link][cid]
        assert c["lo"][k] < m < c["hi"][k]
        lo1, hi1 = list(c["lo"]), list(c["hi"])
        hi1[k] = float(m)
        lo2, hi2 = list(c["lo"]), list(c["hi"])
        lo2[k] = float(m)
        n = len(self.cells[link])
        self.cells[link].append(dict(lo=lo1, hi=hi1, parent=cid, split=None))
        self.cells[link].append(dict(lo=lo2, hi=hi2, parent=cid, split=None))
        c["split"] = (k, float(m), n, n + 1)
        self.leaves[link][pos] = n
        self.leaves[link].append(n + 1)
        # period `link`: column pos -> child 1, new column -> child 2
        t = link
        for A, fill in ((self.B, None), (self.SRC, None)):
            A[t] = np.hstack([A[t], A[t][:, pos:pos + 1]])
        self.OWN[t][:, pos] = -1
        self.OWN[t] = np.hstack([self.OWN[t], np.full((self.OWN[t].shape[0], 1), -1, dtype=np.int64)])
        # period link+1: row pos -> child 1, new row -> child 2
        t = link + 1
        for A in (self.B, self.SRC):
            A[t] = np.vstack([A[t], A[t][pos:pos + 1, :]])
        self.OWN[t][pos, :] = -1
        self.OWN[t] = np.vstack([self.OWN[t], np.full((1, self.OWN[t].shape[1]), -1, dtype=np.int64)])

    def dp(self):
        T = self.T
        f = [None] * T  # f[t]: best value up to and including period t, per link-t cell
        f[0] = self.B[0][0, :].copy()
        for t in range(1, T - 1):
            f[t] = (f[t - 1][:, None] + self.B[t]).min(axis=0)
        V = float((f[T - 2] + self.B[T - 1][:, 0]).min())
        g = [None] * T  # g[t]: best value of periods t+1.. per link-t cell
        g[T - 2] = self.B[T - 1][:, 0].copy()
        for t in range(T - 2, 0, -1):
            g[t - 1] = (self.B[t] + g[t][None, :]).min(axis=1)
        return V, f, g

    def through(self, t, f, g):
        """Best path value through each pair of period t."""
        T = self.T
        fin = np.zeros(1) if t == 0 else f[t - 1]
        gout = np.zeros(1) if t == T - 1 else g[t]
        return fin[:, None] + self.B[t] + gout[None, :]

    def best_path(self, f, g):
        T = self.T
        path = [None] * (T - 1)
        # last link
        v = f[T - 2] + self.B[T - 1][:, 0]
        path[T - 2] = int(np.argmin(v))
        for t in range(T - 2, 0, -1):
            j = path[t]
            path[t - 1] = int(np.argmin(f[t - 1] + self.B[t][:, j]))
        return path


def lam_for(st, t):
    T = st.T
    lin = st.lam[t - 1] if t > 0 else None
    lout = st.lam[t] if t < T - 1 else None
    return lin, lout


def make_task(st, t, r, c, cfg, cap):
    lin, lout = lam_for(st, t)
    cin = st.cell_of(t - 1, r)
    cout = st.cell_of(t, c)
    return (t, cin, cout, lin or [0.0] * 3, lout or [0.0] * 3, st.mu, cap,
            cfg["node_limit"], cfg["time_limit"], cfg["scip_tl"])


def apply_result(st, t, r, c, res):
    rid = len(st.records)
    res = dict(res)
    res.update(t=t, cin=st.cell_id(t - 1, r), cout=st.cell_id(t, c))
    st.records.append(res)
    st.OWN[t][r, c] = rid
    if res["bound"] > st.B[t][r, c]:
        st.B[t][r, c] = res["bound"]
        st.SRC[t][r, c] = rid


def choose_split(st, link, pos, f, g, cfg):
    """Split rule for cell `pos` of link `link` on its best path: separate the
    end levels of the best entering pair from the start levels of the best
    leaving pair.  Returns (k, m) or None."""
    T = st.T
    t = link
    fin = np.zeros(1) if t == 0 else f[t - 1]
    r = int(np.argmin(fin + st.B[t][:, pos]))
    gout = np.zeros(1) if t + 1 == T - 1 else g[t + 1]
    c = int(np.argmin(st.B[t + 1][pos, :] + gout))
    oin, oout = st.OWN[t][r, pos], st.OWN[t + 1][pos, c]
    if oin < 0 or oout < 0:
        return "unevaluated"
    e = st.records[oin]["e"]
    s = st.records[oout]["s"]
    cell = st.cells[link][st.leaves[link][pos]]
    lo, hi = np.array(cell["lo"]), np.array(cell["hi"])
    w = hi - lo
    if e is None or s is None:
        return None
    e, s = np.array(e), np.array(s)
    jump = np.abs(e - s)
    score = jump * np.abs(np.array(st.lam[link])) if cfg.get("weight_by_lam", True) else jump
    score = np.where(w > cfg["min_width"], score, -1.0)
    k = int(np.argmax(score))
    if score[k] < cfg["min_score"]:
        return None
    m = 0.5 * (e[k] + s[k])
    m = min(max(m, lo[k] + cfg["clamp"] * w[k]), hi[k] - cfg["clamp"] * w[k])
    return k, float(m)


def link_areas(D):
    """Tank area of each link row (from the balance row of period t that
    contains the row's end-level variable)."""
    out = []
    for t in range(D["T"] - 1):
        area = {e: a for (i, s, e, a) in terminal.balance_rows(D, t)}
        out.append([area[va] for (i, va, vb) in D["S"]["link"][t]])
    return out


def save(st, path):
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        pickle.dump(st, fh)
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

    implied = cfg.get("implied")
    term = cfg.get("terminal", True)
    D = core.setup(T, implied)
    if term:
        poly, lb = terminal.add_terminal_row(D)
        log(f"terminal row: {poly} >= {lb}")
    mult = json.load(open(cfg["mult"]))
    lam = [[float(v) for v in l] for l in mult["lam"]]
    mu = float(mult["mu"])
    if cfg.get("fold_mu", True):
        # fold mu into the link slopes (valid for any floats); mu := 0
        lam = [[l[k] + mu * float(ar[k]) / 3600.0 for k in range(3)]
               for l, ar in zip(lam, link_areas(D))]
        log(f"folded slopes: {[[round(v, 4) for v in l] for l in lam]}")
        mu = 0.0
    assert mu >= 0
    if os.path.exists(out + ".pkl") and cfg.get("resume", True):
        st = pickle.load(open(out + ".pkl", "rb"))
        log(f"resumed: {len(st.records)} records")
    else:
        boxes = [core.level_box(D, t) for t in range(T - 1)]
        st = State(T, lam, mu, boxes)
    UB = cfg["ub"]
    hc = mu * float(D["hor_rhs"])
    pool = mp.Pool(cfg["workers"], initializer=_init, initargs=(T, implied, term))
    tic = time.time()
    rnd = 0
    while True:
        V, f, g = st.dp()
        Vt = V + hc
        el = time.time() - tic
        ncell = [len(l) for l in st.leaves]
        log(f"round {rnd} t={el:.0f}s DP={Vt:.6f} cells={ncell} records={len(st.records)}")
        if Vt >= UB - cfg.get("stop_gap", 1e-3) or el > cfg["wall"]:
            break
        # candidates: unevaluated pairs on near-optimal paths
        cand = []
        for t in range(T):
            P = st.through(t, f, g)
            if np.isfinite(V):
                mask = (st.OWN[t] < 0) & (P < V + cfg["delta_eval"])
            else:
                mask = st.OWN[t] < 0
            for (r, c) in zip(*np.nonzero(mask)):
                cand.append((float(P[r, c]), t, int(r), int(c)))
        cand.sort()
        cand = cand[:cfg["batch"]]
        if cand:
            tasks = []
            for (p, t, r, c) in cand:
                fin = 0.0 if t == 0 else f[t - 1][r]
                gout = 0.0 if t == T - 1 else g[t][c]
                cap = UB - hc - fin - gout + 1e-6 if np.isfinite(fin + gout) else 1e6
                tasks.append(make_task(st, t, r, c, cfg, cap))
            t0 = time.time()
            res = pool.map(_task, tasks, chunksize=1)
            for (p, t, r, c), rr in zip(cand, res):
                apply_result(st, t, r, c, rr)
            nl = sum(1 for rr in res if rr["status"] == "limit")
            log(f"  evaluated {len(cand)} pairs in {time.time()-t0:.0f}s "
                f"(rbb limit {nl}, max rbb {max(rr['t_rbb'] for rr in res):.0f}s, "
                f"max nodes {max(rr['nodes'] for rr in res)})")
        else:
            # split cells on near-optimal paths
            cells = []
            for link in range(T - 1):
                psi = f[link] + g[link]
                for pos in np.nonzero(psi < V + cfg["delta_split"])[0]:
                    cells.append((float(psi[pos]), link, int(pos)))
            cells.sort()
            nsplit = 0
            todo = []
            for (p, link, pos) in cells:
                sp = choose_split(st, link, pos, f, g, cfg)
                if sp is None or sp == "unevaluated":
                    continue
                todo.append((link, pos, sp))
                if len(todo) >= cfg["max_split"]:
                    break
            for (link, pos, (k, m)) in todo:
                st.split(link, pos, k, m)
                nsplit += 1
            log(f"  split {nsplit} cells: {[(l, k, round(m, 4)) for (l, p, (k, m)) in todo]}")
            if nsplit == 0:
                log("  no cell to split on near-optimal paths; stop")
                break
        save(st, out + ".pkl")
        rnd += 1
    save(st, out + ".pkl")
    V, f, g = st.dp()
    path = st.best_path(f, g)
    log(f"final DP (float, not the certificate) = {V + hc:.6f}; best path cells {path}")
    pool.close()


if __name__ == "__main__":
    main()
