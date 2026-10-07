"""Cutting-plane loops with split inequalities.

mode 'bt'    : Buchheim-Traversi's experiment (Sec. 6.1 of OO 2013/07/3953):
               SDP relaxation + split inequalities only, separated exactly in
               the normalised sense (sep_ratio, all Dinkelbach iterates) plus the
               violated {0,+-1} splits with |supp w| <= 3.  Stops when no split
               has normalised violation > 1e-7 (then the point is in the split
               closure up to that tolerance).
mode 'btfam' : as 'bt' but only the {0,+-1} splits with |supp w| <= 3 are added
               (the exact separator is run only to measure what remains violated).
mode 'dmplus': de Meijer et al.'s families (triangle, pair, RLT, 1-/2-index
               splits, pentagonal heuristic) together with the split separators
               above, to measure what general splits add.
mode 'dmfam' : de Meijer et al.'s families plus the {0,+-1} splits with
               |supp w| <= 3 only (no general splits are added).
Each instance stops after MAX_ROUNDS rounds or when the wall-clock budget
BUDGET (seconds) is exceeded; the record then has stopped='rounds'/'budget'
and 'final' is still a valid lower bound.
Usage: python3 exp_splitloop.py MODE SET OUT.jsonl [workers [namefile [MAX_ROUNDS BUDGET]]]
"""
import itertools
import json
import os
import sys
import time
import traceback
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exp_points import instance_set, make  # noqa: E402
from instances import brute_force_opt  # noqa: E402
from lattice import sep_ratio  # noqa: E402
from sdp import Relaxation, SEP, sep_odd5, split_cut, eig_rank  # noqa: E402


def phi(t):
    f = t - np.floor(t)
    return f * (1 - f)


def family_top(Y, k, m=200, tol=1e-6):
    """Violated splits with w in {0,+-1}^n, |supp w| = k; returns list of
    (violation, v) for the m most violated (best v0 for each w)."""
    N = Y.shape[0]; n = N - 1
    x = Y[0, 1:]; S = Y[1:, 1:] - np.outer(x, x)
    C = np.array(list(itertools.combinations(range(n), k)))
    out = []
    for s in itertools.product([1.0, -1.0], repeat=k):
        if s[0] < 0:
            continue
        t = (x[C] * np.array(s)).sum(1)
        var = np.zeros(len(C))
        for a in range(k):
            for b in range(k):
                var += s[a] * s[b] * S[C[:, a], C[:, b]]
        viol = phi(t) - var
        idx = np.nonzero(viol > tol)[0]
        idx = idx[np.argsort(-viol[idx])[:m]]
        for i in idx:
            v = np.zeros(N, dtype=np.int64)
            v[1 + C[i]] = np.array(s, dtype=np.int64)
            # best v0 = round(-t - 1/2): the two integers around -t - 1/2
            cands = [np.floor(-t[i] - 0.5), np.ceil(-t[i] - 0.5)]
            best = None
            for v0 in cands:
                v[0] = int(v0)
                q = float(v @ Y @ v + v @ Y[:, 0])
                if best is None or q < best[0]:
                    best = (q, int(v0))
            v[0] = best[1]
            out.append((-best[0], v.copy()))
    out.sort(key=lambda p: -p[0])
    return out[:m]


MAX_ROUNDS = 150
BUDGET = float("inf")


def run(args):
    mode, spec = args[:2]
    max_rounds, budget = (args[2], args[3]) if len(args) > 2 else (MAX_ROUNDS, BUDGET)
    try:
        inst = make(spec)
        base = "BT" if inst["family"] == "BT" else "DM"
        rel = Relaxation(inst, base)
        opt = brute_force_opt(inst)[0] if inst["n"] <= 12 else None
        dm_fams = (["tri", "pair", "rlt", "split1", "split2"] if base == "BT"
                   else ["tri", "pair", "rlt", "split2", "odd5"])
        hist = []
        t0 = time.time()
        res = rel.solve()
        root = res["obj"]
        rng = np.random.default_rng(1)
        stopped = "converged"; retries = 0
        for rnd in range(max_rounds):
            Y = res["Y"]
            ts = time.time()
            added = 0; nsplit = 0; ndm = 0
            # de Meijer families
            if mode in ("dmplus", "dmfam"):
                pool = []
                for f in dm_fams:
                    out = sep_odd5(Y, 1e-3, rng=rng) if f == "odd5" else SEP[f](Y, 1e-3)
                    viol, I, J, C, rhs = out
                    for r in np.nonzero(viol > 1e-3)[0]:
                        pool.append((viol[r], f, I[r], J[r], C[r], rhs[r]))
                pool.sort(key=lambda p: -p[0])
                for viol, f, I, J, C, rhs in pool[:5000]:
                    ndm += rel.cuts.add(I[None], J[None], C[None], np.array([rhs]), f)
            # split separation
            sr = sep_ratio(Y, max_nodes=2 * 10**6)
            vs = [np.array(v, dtype=np.int64) for v in sr["cands"]] if mode in ("bt", "dmplus") else []
            bv = None if sr["v"] is None else np.array(sr["v"], dtype=np.int64)
            fam_viol = {}
            for k in (1, 2, 3):
                if k == 3 and inst["n"] > 70:
                    continue
                ft = family_top(Y, k, m=100, tol=1e-6)
                fam_viol[k] = ft[0][0] if ft else 0.0
                vs += [v for _, v in ft]
            for v in vs:
                q = float(v.astype(float) @ Y @ v.astype(float) + v.astype(float) @ Y[:, 0])
                if q < -1e-6:
                    I, J, C, rhs = split_cut(v)
                    nsplit += rel.cuts.add(I, J, C, rhs, "gsplit")
            tsep = time.time() - ts
            rk = eig_rank(Y)[0]
            hist.append(dict(round=rnd, obj=res["obj"], status=res["status"], rank=rk,
                             ratio=sr["ratio"], ratio_q=sr["q"], ratio_nodes=sr["nodes"],
                             ratio_complete=bool(sr["complete"]), ratio_time=sr["time"],
                             fam_viol=fam_viol, nsplit_added=nsplit, ndm_added=ndm,
                             ratio_supp=None if bv is None else int((bv[1:] != 0).sum()),
                             ratio_vmax=None if bv is None else int(np.abs(bv).max()),
                             ncuts=rel.cuts.m, t_sep=tsep, t_solve=res["time"]))
            if nsplit + ndm == 0:
                break
            if rnd == max_rounds - 1:
                stopped = "rounds"
                break
            if time.time() - t0 > budget:
                stopped = "budget"
                break
            try:
                res = rel.solve()
            except Exception:
                # Clarabel occasionally fails at tolerance 1e-9; retry at 1e-7,
                # then with SCS; otherwise keep the last bound and stop
                try:
                    res = rel.solve(tol=1e-7)
                    retries += 1
                except Exception:
                    try:  # last resort: SCS (first-order, accuracy about 1e-7)
                        res = rel.solve(tol=1e-7, solver="SCS")
                        retries += 1
                    except Exception:
                        stopped = "solver_error"
                        break
        return dict(name=inst["name"], mode=mode, base=base, n=inst["n"], root=root,
                    final=res["obj"], opt=opt, rounds=len(hist), time=time.time() - t0,
                    stopped=stopped, retries=retries, final_status=res["status"],
                    final_rank=eig_rank(res["Y"])[0], hist=hist)
    except Exception:
        return dict(spec=list(spec), mode=mode, error=traceback.format_exc())


if __name__ == "__main__":
    mode, setname, outp = sys.argv[1], sys.argv[2], sys.argv[3]
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    specs = instance_set(setname)
    if len(sys.argv) > 5 and sys.argv[5] != "-":   # optional filter file with instance names
        keep = set(open(sys.argv[5]).read().split())
        specs = [s for s in specs if make(s)["name"] in keep]
    lim = (int(sys.argv[6]), float(sys.argv[7])) if len(sys.argv) > 7 else (MAX_ROUNDS, BUDGET)
    done = set()
    if os.path.exists(outp):
        done = {json.loads(l).get("name") for l in open(outp)}
    todo = [(mode, s) + lim for s in specs if make(s)["name"] not in done]
    print(len(todo), "to do", flush=True)

    def clean(o):
        if isinstance(o, dict):
            return {str(k): clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [clean(v) for v in o]
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.integer):
            return int(o)
        return o
    with Pool(workers) as pool, open(outp, "a") as f:
        for d in pool.imap_unordered(run, todo):
            f.write(json.dumps(clean(d)) + "\n"); f.flush()
            print(d.get("name"), d.get("root"), d.get("final"), d.get("opt"), d.get("rounds"),
                  d.get("error", "")[:300], flush=True)
