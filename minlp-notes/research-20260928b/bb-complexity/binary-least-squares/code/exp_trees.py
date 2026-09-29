"""E3: B&B tree sizes with the box relaxation (incumbent x*, improved by
rounding; certified bounds; best-first), for branching rules 'maxfrac' and
'static'.  rho is given either as 'rN' (rho = N/r) or 'cL' (rho = c log N).
Usage: python3 exp_trees.py OUT.jsonl Ns rhos beta nseeds cap [procs]
e.g.   python3 exp_trees.py trees.jsonl 32,64,128 r2,r4,r8,c4,c8 1 6 200000 5
"""
import sys, json, os, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np
from multiprocessing import Pool
from core import instance, bnb, fval_u


def rho_of(tag, N):
    if tag.startswith("r"):
        return N / float(tag[1:])
    return float(tag[1:]) * np.log(N)


def job(args):
    N, tag, beta, s, cap, rule = args
    M = int(round(beta * N)); rho = rho_of(tag, N)
    A, y, xs, B, w = instance(N, M, rho, s)
    t = time.time()
    r = bnb(B, w, rule=rule, max_nodes=cap)
    fstar = fval_u(B, w, np.zeros(N))
    return dict(N=N, M=M, beta=beta, tag=tag, rho=rho, seed=s, rule=rule,
                nodes=r["nodes"], done=r["done"], xstar_opt=bool(r["OPT"] >= fstar * (1 - 1e-12)),
                opt_gap_xstar=float(fstar - r["OPT"]), time=time.time() - t)


if __name__ == "__main__":
    out = sys.argv[1]; Ns = [int(v) for v in sys.argv[2].split(",")]
    tags = sys.argv[3].split(","); beta = float(sys.argv[4]); ns = int(sys.argv[5])
    cap = int(sys.argv[6]); procs = int(sys.argv[7]) if len(sys.argv) > 7 else 5
    rules = sys.argv[8].split(",") if len(sys.argv) > 8 else ["maxfrac", "static"]
    jobs = [(N, tag, beta, s, cap, rule) for N in Ns for tag in tags for s in range(ns) for rule in rules]
    jobs.sort(key=lambda j: (j[0], j[1]))
    with Pool(procs) as pool, open(out, "a") as f:
        for r in pool.imap_unordered(job, jobs):
            f.write(json.dumps(r) + "\n"); f.flush()
