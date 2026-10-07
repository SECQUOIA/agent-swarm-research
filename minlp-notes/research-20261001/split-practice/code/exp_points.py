"""Compute 'practical points': optimal solutions of the SDP relaxations, before
and after de Meijer et al.'s cut families, plus lower-rank optimal solutions
found by re-optimising over the optimal face.

Usage: python3 exp_points.py SET [workers]
  SET in {BT10, BT20, BT30, BT50, DM30, DM60}
Writes data/points_SET/<name>__<stage>.npz and logs/points_SET.jsonl.
"""
import json
import os
import sys
import time
import traceback
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from instances import bt_instance, dm_instance, brute_force_opt  # noqa: E402
from sdp import Relaxation, cut_loop, eig_rank  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def instance_set(name):
    if name == "BT10":
        return [("BT", 10, p, s) for p in range(11) for s in range(10)]
    if name in ("BT20", "BT30"):
        n = int(name[2:])
        return [("BT", n, p, s) for p in range(0, n + 1, n // 5) for s in range(3)]
    if name == "BT50":
        return [("BT", 50, p, 0) for p in (0, 10, 25, 40, 50)]
    if name in ("DM30", "DM60"):
        n = int(name[2:])
        return [("DM", k, t, n, p, 0) for k in ("QUTO", "LIN") for t in (1, 2, 3)
                for p in (25, 50, 75)]
    raise ValueError(name)


def make(spec):
    if spec[0] == "BT":
        return bt_instance(*spec[1:])
    return dm_instance(*spec[1:])


def face_reopt(rel, opt, kind, seed=0):
    """Re-optimise over the (approximate) optimal face:
    min <W, Y> s.t. relaxation constraints and objective <= opt + 1e-7 (1 + |opt|).
    kind 'trace': W = I;  kind 'rand': W = G G^T / N with G Gaussian."""
    import cvxpy as cp
    N = rel.N
    if kind == "trace":
        W = np.eye(N)
    else:
        G = np.random.default_rng(seed).normal(size=(N, N))
        W = G @ G.T / N
    bound = opt + 1e-7 * (1 + abs(opt))
    res = rel.solve(extra_obj=lambda Y: cp.trace(W @ Y), obj_bound=bound)
    return res


def run(spec):
    out = []
    try:
        inst = make(spec)
        name = inst["name"]
        setname = sys.argv[1]
        ddir = os.path.join(ROOT, "data", f"points_{setname}")
        os.makedirs(ddir, exist_ok=True)
        opt = None
        if inst["n"] <= 12:
            opt, _ = brute_force_opt(inst)
        bases = ["BT"] if inst["family"] == "BT" else ["DM"]
        for base in bases:
            fams = (["tri", "pair", "rlt", "split1", "split2"] if base == "BT"
                    else ["tri", "pair", "rlt", "split2", "odd5"])
            rel = Relaxation(inst, base)
            t0 = time.time()
            root = rel.solve()
            hist_log = []
            res, hist = cut_loop(rel, fams, tol=1e-3, cap=5000, max_rounds=40,
                                 stop_rule="none", odd5_rng=np.random.default_rng(1))
            tl = time.time() - t0
            stages = {"root": root, "cut": res}
            # lower-rank optimal solutions over the optimal face of the cut relaxation
            for kind in ("trace", "rand"):
                try:
                    r2 = face_reopt(rel, res["obj"], kind)
                    stages[f"cut_{kind}"] = r2
                except Exception as e:  # solver failure is recorded, not fatal
                    stages[f"cut_{kind}"] = dict(status="error:" + str(e)[:80])
            for st, r in stages.items():
                if "Y" not in r:
                    out.append(dict(name=name, base=base, stage=st, status=r["status"]))
                    continue
                rk, w = eig_rank(r["Y"])
                np.savez_compressed(os.path.join(ddir, f"{name}__{base}__{st}.npz"),
                                    Y=r["Y"], Q=inst["Q"], c=inst["c"], linear=inst["linear"])
                out.append(dict(name=name, base=base, stage=st, status=r["status"],
                                obj=r["obj"], opt=opt, rank=rk,
                                eig=[float(a) for a in w[:40]], lam_min=float(w[-1]),
                                time=r["time"], n=inst["n"],
                                rounds=len(hist) if st == "cut" else None,
                                ncuts=rel.cuts.m if st == "cut" else None,
                                loop_time=tl if st == "cut" else None,
                                hist=hist if st == "cut" else None))
    except Exception:
        out.append(dict(spec=list(spec), error=traceback.format_exc()))
    return out


def _clean(o):
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    return o


if __name__ == "__main__":
    setname = sys.argv[1]
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    specs = instance_set(setname)
    logf = os.path.join(ROOT, "logs", f"points_{setname}.jsonl")
    done = set()
    if os.path.exists(logf):
        for line in open(logf):
            d = json.loads(line)
            if "name" in d:
                done.add(d["name"])
    todo = [s for s in specs if make(s)["name"] not in done]
    print(f"{setname}: {len(specs)} instances, {len(todo)} to do", flush=True)
    with Pool(workers) as pool, open(logf, "a") as f:
        for out in pool.imap_unordered(run, todo):
            for d in out:
                f.write(json.dumps(_clean(d)) + "\n")
            f.flush()
            print(out[0].get("name", out[0]), flush=True)
