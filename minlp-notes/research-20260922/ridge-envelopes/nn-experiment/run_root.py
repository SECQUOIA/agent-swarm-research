"""Root-node experiment: R0 vs R1 dual bounds with IBP and with IBP+OBBT bounds.

For every network and sense (min, max): multistart primal, then each relaxation
with the cut loop run to convergence (max 200 rounds). Every cut added in the
root runs is checked by sampling. Times are process CPU times. Output:
results/root/<net>.json.
"""
import json
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

from envelope import cut_violation_samples
from nets import load_all, Net, NETDIR
from primal import multistart
from relax import ibp, obbt, root_bound

OUT = Path(__file__).resolve().parent / "results" / "root"


def job(name):
    net = Net.load(NETDIR / (name + ".npz"))
    out = dict(name=name, act=net.actname, d=net.d, widths=net.widths, runs=[])
    rng = np.random.default_rng(7)
    viol_max, n_checked, outside = -np.inf, 0, []
    for sense in (1, -1):
        t0 = time.process_time()
        pr = multistart(net, sense)
        tp = time.process_time() - t0
        B = ibp(net, net.lo, net.hi)
        t0 = time.process_time()
        Bo, nlp = obbt(net, B)
        tob = time.process_time() - t0
        for bname, BB in (("ibp", B), ("obbt", Bo)):
            for mode in ("R0", "R1"):
                rec = []
                t0 = time.process_time()
                r = root_bound(net, sense, BB, mode, max_rounds=200, record=rec)
                el = time.process_time() - t0
                r["lp"].dispose()
                for P in rec:
                    v, fo = cut_violation_samples(net.actname, P, npts=500, rng=rng, return_outside=True)
                    viol_max = max(viol_max, v)
                    n_checked += 1
                    if len(P.a) > 1:
                        outside.append(fo)
                out["runs"].append(dict(sense=sense, bounds=bname, mode=mode, bound=r["bound"], rounds=r["rounds"],
                                        status=r["status"], cuts_r0=r["cuts_r0"], cuts_r1=r["cuts_r1"],
                                        t_lp=r["t_lp"], t_sep=r["t_sep"], t_init=r["t_init"], time=el,
                                        primal=pr["value"], primal_x=pr["x"].tolist(), t_primal=tp,
                                        obbt_time=tob if bname == "obbt" else 0.0, obbt_lps=nlp if bname == "obbt" else 0,
                                        mean_z_width=BB.width_summary(), hist=r["hist"]))
    out["cut_check"] = dict(cuts=n_checked, max_violation=viol_max,
                            mean_fraction_outside_simplex=float(np.mean(outside)) if outside else None)
    (OUT / (name + ".json")).write_text(json.dumps(out))
    return name, n_checked, viol_max


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    names = [e["name"] for e in json.loads((NETDIR / "index.json").read_text())]
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 16) as pool:
        for name, nc, vm in pool.imap_unordered(job, names):
            print("%-36s cuts checked %6d  max violation %.2e" % (name, nc, vm), flush=True)
