"""Negative control for rebound.py: on the six records of the minimizing path,
ask vbb2 (same driver, same bounds, same terminal row) to certify the pair's
SCIP estimate + 0.05, i.e. a value above a point SCIP found (feasible up to
its tolerances).  vbb2 must NOT certify it.  If the driver over-constrained
the pair (for example, cell boxes put on the wrong variables), vbb2 would
certify such targets.
usage: python3 control.py cert.pkl out.jsonl
"""
import json
import sys
import multiprocessing as mp

import load_cert
import rebound

PATH_RECORDS = [1, 16, 30, 14, 10, 3]


def main():
    P = load_cert.load(sys.argv[1]).__dict__
    tasks = []
    for rid in PATH_RECORDS:
        rec = P["crecs"][rid]
        t = rec["t"]
        # the estimate record of exactly this pair (same cells)
        est = [e for e in P["erecs"] if e["t"] == t and e["cin"] == rec["cin"] and e["cout"] == rec["cout"]]
        assert est, rid
        E = min(e["est"] for e in est)
        tasks.append((rid, rec, E + 0.05, 120.0))
    fh = open(sys.argv[2], "w")
    with mp.Pool(6) as pool:
        for (rid, res), task in zip(pool.map(rebound.run, tasks), tasks):
            line = dict(rid=rid, t=P["crecs"][rid]["t"], rbb_bound=P["crecs"][rid]["bound"], target=task[2],
                        vbb2_status=res.get("status"), vbb2_bound_float=res.get("bound_float"),
                        nodes=res.get("nodes"), time=round(res["time"], 1))
            fh.write(json.dumps(line) + "\n")
            print(json.dumps(line), flush=True)


if __name__ == "__main__":
    main()
