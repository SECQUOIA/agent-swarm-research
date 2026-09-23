"""Global solve: Python spatial B&B with R0 or R1, 600 s limit per run.

Jobs: every network x sense (min, max) x mode (R0, R1). Both modes start from
the same multistart incumbent (seed 0) and use root OBBT. Output:
results/bnb/<net>_<min|max>_<mode>.json (existing files are skipped).
"""
import json
import sys
import time
from multiprocessing import Pool
from pathlib import Path

from bnb import bnb
from nets import Net, NETDIR
from primal import multistart

OUT = Path(__file__).resolve().parent / "results" / "bnb"
TIME_LIMIT = 600.0


def job(args):
    name, sense, mode = args
    f = OUT / ("%s_%s_%s.json" % (name, "min" if sense > 0 else "max", mode))
    if f.exists():
        return name, sense, mode, "cached"
    net = Net.load(NETDIR / (name + ".npz"))
    pr = multistart(net, sense)
    t0 = time.time()
    r = bnb(net, sense, mode, pr, time_limit=TIME_LIMIT)
    r.update(name=name, act=net.actname, d=net.d, widths=net.widths, sense=sense, mode=mode,
             incumbent0=pr["value"], wall=time.time() - t0, time_limit=TIME_LIMIT)
    f.write_text(json.dumps(r))
    return name, sense, mode, "%s nodes=%d time=%.1f gap=%.2e" % (r["status"], r["nodes"], r["time"], r["gap"])


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    idx = json.loads((NETDIR / "index.json").read_text())
    # larger networks first so that long runs start early
    idx.sort(key=lambda e: -(e["d"] * 100 + sum(e["hidden"])))
    jobs = [(e["name"], s, m) for e in idx for s in (1, -1) for m in ("R0", "R1")]
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 16, maxtasksperchild=1) as pool:
        for res in pool.imap_unordered(job, jobs):
            print(*res, flush=True)
