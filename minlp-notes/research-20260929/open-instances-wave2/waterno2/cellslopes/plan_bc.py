"""Planning with cell-dependent slopes by block-coordinate ascent over links
(SCIP estimates only; no bounds).

For a fixed link t and fixed slopes on all other links, every path passes
through exactly one cell D of link t, so the DP value is
    V = min_D H_D(lam_D),   H_D(lam) = In_D(lam) + Out_D(lam),
    In_D(lam)  = min_r f_{t-1}(r) + phi_t(r, D; lam_r, lam)       (= f_t(D))
    Out_D(lam) = min_c phi_{t+1}(D, c; lam, lam_c) + g_{t+1}(c)   (= g_t(D)).
H_D depends on lam_D only, so the slopes of the cells of one link can be
improved independently: for every cell a small trust-region LP over the pool
model of its pairs proposes lam_D; the pairs of periods t and t+1 that attain
(or nearly attain) In_D and Out_D are evaluated by SCIP at the new slopes; the
new slope is kept only if H_D rose (else the old one is restored).  This step
cannot lower V (up to SCIP's estimate quality).  Every `split_every` link
passes, cells on near-optimal paths are split (as in plan_cs.py).

usage: python3 plan_bc.py config.json
"""
import json
import math
import os
import pickle
import sys
import time

import numpy as np
from scipy.optimize import linprog

import cs
from plan_cs import Planner, save

INF = math.inf


def cell_lp(st, t, pos, tab, M, f, g, delta, LAMC, BOX):
    """Trust-region LP for the slope of leaf `pos` of link t (others fixed).
    Variables: lam (3), a, b, uo (3), ui (3).  max a + b."""
    T = st.T
    lam_c = LAMC[t][pos]
    lo, hi = BOX[t][0][pos], BOX[t][1][pos]
    A, rhs = [], []
    # period t: entering pairs (r, pos)
    d = tab[t]
    S, E, C0 = PTS[t]
    P, R, C = INC[t]
    sel = np.nonzero(C == pos)[0]
    fin = np.zeros(1) if t == 0 else f[t - 1]
    for i in sel:
        p, r = P[i], R[i]
        if not np.isfinite(d["U"][r, pos]) or d["L"][r, pos] == INF or not np.isfinite(fin[r]):
            continue
        const = fin[r] + C0[p]
        if t > 0:
            const += float(np.dot(LAMC[t - 1][r], S[p]))
        row = np.zeros(11)
        row[0:3] = E[p]
        row[3] = 1.0
        A.append(row); rhs.append(const)
    okL = (~np.isfinite(d["U"][:, pos])) & (~d["SINF"][:, pos]) & (d["L"][:, pos] < INF) & np.isfinite(fin)
    for r in np.nonzero(okL)[0]:
        row = np.zeros(11)
        row[3] = 1.0
        row[5:8] = -1.0
        A.append(row); rhs.append(fin[r] + d["L"][r, pos])
    # period t+1: leaving pairs (pos, c)
    d = tab[t + 1]
    S, E, C0 = PTS[t + 1]
    P, R, C = INC[t + 1]
    sel = np.nonzero(R == pos)[0]
    gout = np.zeros(1) if t + 1 == T - 1 else g[t + 1]
    for i in sel:
        p, c = P[i], C[i]
        if not np.isfinite(d["U"][pos, c]) or d["L"][pos, c] == INF or not np.isfinite(gout[c]):
            continue
        const = gout[c] + C0[p]
        if t + 1 < T - 1:
            const -= float(np.dot(LAMC[t + 1][c], E[p]))
        row = np.zeros(11)
        row[0:3] = -S[p]
        row[4] = 1.0
        A.append(row); rhs.append(const)
    okL = (~np.isfinite(d["U"][pos, :])) & (~d["SINF"][pos, :]) & (d["L"][pos, :] < INF) & np.isfinite(gout)
    for c in np.nonzero(okL)[0]:
        row = np.zeros(11)
        row[4] = 1.0
        row[8:11] = -1.0
        A.append(row); rhs.append(gout[c] + d["L"][pos, c])
    if not A:
        return None
    # corrections: uo_k <= -(lam_k - lc_k) lo_k, -(lam_k - lc_k) hi_k ; ui_k <= (lam_k - lc_k) lo_k, hi_k
    for k in range(3):
        for v in (lo[k], hi[k]):
            row = np.zeros(11); row[5 + k] = 1.0; row[k] = v
            A.append(row); rhs.append(v * lam_c[k])
            row = np.zeros(11); row[8 + k] = 1.0; row[k] = -v
            A.append(row); rhs.append(-v * lam_c[k])
    bounds = [(lam_c[k] - delta[k], lam_c[k] + delta[k]) for k in range(3)] + [(-1e7, 1e7)] * 8
    cvec = np.zeros(11); cvec[3] = -1.0; cvec[4] = -1.0
    res = linprog(cvec, A_ub=np.array(A), b_ub=np.array(rhs), bounds=bounds, method="highs")
    if res.status != 0:
        return None
    return res.x[0:3], -res.fun


PTS, INC = {}, {}


def refresh(st):
    global PTS, INC
    inc = st.incidence()
    for t in range(st.T):
        PTS[t] = st.point_arrays(t)
        INC[t] = inc[t]
    tab = st.tables(inc)
    M = st.model(tab)
    V, f, g = st.dp(M)
    return V, f, g, M, tab


def cell_lazy(PL, t, cids, cfg):
    """Evaluate (SCIP, current slopes) the stale pairs of periods t and t+1 that
    attain, within delta_eval, In_D or Out_D of the given cells of link t."""
    st = PL.st
    T = st.T
    n0 = PL.nscip
    for rnd in range(cfg["max_rounds"]):
        V, f, g, M, tab = refresh(st)
        cand = []
        fin = np.zeros(1) if t == 0 else f[t - 1]
        gout = np.zeros(1) if t + 1 == T - 1 else g[t + 1]
        for cid in cids:
            pos = st.leaves[t].index(cid)
            col = fin + M[t][:, pos]
            mn = col.min()
            if np.isfinite(mn):
                for r in np.nonzero((col < mn + cfg["delta_eval"]) & (~tab[t]["FRESH"][:, pos]))[0]:
                    cand.append((float(col[r] - mn), t, int(r), pos))
            row = M[t + 1][pos, :] + gout
            mn = row.min()
            if np.isfinite(mn):
                for c in np.nonzero((row < mn + cfg["delta_eval"]) & (~tab[t + 1]["FRESH"][pos, :]))[0]:
                    cand.append((float(row[c] - mn), t + 1, pos, int(c)))
        if not cand:
            break
        cand.sort()
        PL.evaluate([(tt, r, c) for (p, tt, r, c) in cand[:cfg["cap"]]])
    return PL.nscip - n0


def link_step(PL, t, cfg, dmap, log):
    st = PL.st
    T = st.T
    V, f, g, M, tab = refresh(st)
    H = f[t] + g[t]
    touched = [st.leaves[t][int(p)] for p in np.nonzero(H < V + cfg["cell_delta"])[0]]
    n_old = cell_lazy(PL, t, touched, cfg)
    V, f, g, M, tab = refresh(st)
    H_old = {cid: (f[t] + g[t])[st.leaves[t].index(cid)] for cid in touched}
    LAMC = [st.lam_arr(l) for l in range(T - 1)]
    BOX = [st.boxes(l) for l in range(T - 1)]
    old = {}
    for cid in touched:
        pos = st.leaves[t].index(cid)
        delta = dmap.setdefault((t, cid), np.array(cfg["delta"], float))
        r = cell_lp(st, t, pos, tab, M, f, g, delta, LAMC, BOX)
        if r is None:
            continue
        lam_new, val = r
        if val <= H_old[cid] + cfg["min_pred_gain"]:
            continue
        old[cid] = list(st.lam[t][cid])
        st.lam[t][cid] = [float(v) for v in lam_new]
    if not old:
        log(f"  link {t}: touched {len(touched)}, no predicted gain (V={V:.4f}); evals {n_old}")
        return V, n_old
    n_new = cell_lazy(PL, t, list(old), cfg)
    V, f, g, M, tab = refresh(st)
    H_new = f[t] + g[t]
    nacc = 0
    gains = []
    for cid, lam_old in old.items():
        pos = st.leaves[t].index(cid)
        if H_new[pos] > H_old[cid] + 1e-6:
            nacc += 1
            gains.append(H_new[pos] - H_old[cid])
            dmap[(t, cid)] = np.minimum(dmap[(t, cid)] * cfg["grow"], cfg["delta_max"])
        else:
            st.lam[t][cid] = lam_old
            dmap[(t, cid)] = np.maximum(dmap[(t, cid)] * cfg["shrink"], cfg["delta_floor"])
    V2, f, g, M, tab = refresh(st)
    log(f"  link {t}: touched {len(touched)}, proposed {len(old)}, accepted {nacc} "
        f"(mean gain {np.mean(gains) if gains else 0:.3f}); evals {n_old}+{n_new}; V {V2:.4f}")
    return V2, n_old + n_new


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
    dmap = getattr(st, "dmap", {})
    PL = Planner(cfg, st, log)
    tic = time.time()
    V, n = PL.lazy(cfg["delta_eval_global"], cfg["cap"])
    log(f"init: V={V:.4f} after {n} SCIP evaluations; cells {[len(l) for l in st.leaves]}")
    cyc = 0
    while time.time() - tic < cfg["wall"]:
        cyc += 1
        for t in cfg.get("links", list(range(st.T - 1))):
            V, n = link_step(PL, t, cfg, dmap, log)
            st.dmap = dmap
            save(st, out + ".pkl")
        V, n = PL.lazy(cfg["delta_eval_global"], cfg["cap"])
        log(f"cycle {cyc} t={time.time()-tic:.0f}s V={V:.4f} (global lazy {n}) SCIP total {PL.nscip} "
            f"cpu {PL.scip_cpu:.0f}s cells {[len(l) for l in st.leaves]}")
        if cfg["split_every"] and cyc % cfg["split_every"] == 0:
            PL.split_round(cfg["delta_split"], cfg["max_split"])
            V, n = PL.lazy(cfg["delta_eval_global"], cfg["cap"])
            log(f"  after split: V={V:.4f} ({n} evaluations) t={time.time()-tic:.0f}s SCIP total {PL.nscip} "
                f"cpu {PL.scip_cpu:.0f}s cells {[len(l) for l in st.leaves]}")
        st.dmap = dmap
        save(st, out + ".pkl")
        if V >= cfg["stop_at"] or os.path.exists(out + ".stop"):
            break
    log(f"final V={V:.6f}; SCIP evaluations {PL.nscip}, cpu {PL.scip_cpu:.0f}s; wall {time.time()-tic:.0f}s")
    PL.pool.close()


if __name__ == "__main__":
    main()
