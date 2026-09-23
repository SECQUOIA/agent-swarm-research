"""SCIP 10 and Gurobi 13 on the same problems (context, not like-for-like).

Jobs: every non-GELU network x sense x solver, 600 s, single thread, relative
gap 1e-4 and absolute gap 1e-6. Output: results/solvers/<net>_<min|max>_<solver>.json.
The returned x is re-evaluated with the numpy network (true objective value).
"""
import json
import sys
from multiprocessing import Pool
from pathlib import Path

from nets import Net, NETDIR
from solvers import SUPPORTED, solve_gurobi, solve_scip

OUT = Path(__file__).resolve().parent / "results" / "solvers"
TIME_LIMIT = 600.0


def job(args):
    name, sense, solver = args
    f = OUT / ("%s_%s_%s.json" % (name, "min" if sense > 0 else "max", solver))
    if f.exists():
        return name, sense, solver, "cached"
    net = Net.load(NETDIR / (name + ".npz"))
    try:
        r = (solve_scip if solver == "scip" else solve_gurobi)(net, sense, time_limit=TIME_LIMIT)
        r["true_value"] = float(sense * net.forward(r["x"])[0]) if r["x"] is not None else None
    except Exception as ex:  # record failures instead of dropping them
        r = dict(solver=solver, status="error: %r" % ex)
    r.update(name=name, act=net.actname, d=net.d, widths=net.widths, sense=sense, time_limit=TIME_LIMIT)
    f.write_text(json.dumps(r, default=str))
    return name, sense, solver, str(r.get("status")), r.get("time")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    idx = json.loads((NETDIR / "index.json").read_text())
    idx.sort(key=lambda e: -(e["d"] * 100 + sum(e["hidden"])))
    jobs = [(e["name"], s, sv) for e in idx if e["act"] in SUPPORTED for s in (1, -1) for sv in ("scip", "gurobi")]
    if len(sys.argv) > 2 and sys.argv[2] == "reverse":  # second driver working from the other end
        jobs = jobs[::-1]
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 16, maxtasksperchild=1) as pool:
        for res in pool.imap_unordered(job, jobs):
            print(*res, flush=True)
