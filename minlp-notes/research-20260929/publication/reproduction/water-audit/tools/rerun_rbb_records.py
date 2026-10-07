"""Re-run the authors' rbb on stored pair records of a waterno2_06 separator certificate.

Reproduction check (author code, clean checkout): for each selected record of
cellslopes/logs/certB_cert.pkl.gz, call cellslopes/cs.rbb_task (the function that
produced the records; it wraps core.PeriodBounder -> rbb.solve with the rc=False
retry of sepbranch/tasks.py) with the record's own period, entry/exit boxes,
slopes and target, and compare bound, status and node count with the record.
Records that came from cert3 were made by sepbranch/tasks.rbb_task with mu = 0,
which runs the same PeriodBounder.bound call; cert3 used time limit 600 s,
certA/certB 300 s; node limit 20000 throughout.

Run from open-instances-wave2/waterno2/cellslopes with PYTHONPATH=../sepbranch:..

usage: python3 rerun_rbb_records.py cert.pkl.gz selection.json out.jsonl workers
  selection.json: list of {"rid": int, "group": str}
"""
import gzip
import json
import math
import multiprocessing as mp
import pickle
import sys

import cs


def run(a):
    rid, group, rec = a
    tl = 600.0 if rec["src"][0] == "cert3" else 300.0
    t = rec["t"]
    key, res = cs.rbb_task((rid, t, rec["cin_box"], rec["cout_box"], rec["lam_in"], rec["lam_out"],
                            rec["target"], 20000, tl))
    same_bound = (res["bound"] == rec["bound"]) or (math.isinf(res["bound"]) and math.isinf(rec["bound"]))
    return dict(rid=rid, group=group, t=t, src=list(rec["src"]), stored_bound=repr(rec["bound"]),
                stored_status=rec["status"], stored_nodes=rec["nodes"], new_bound=repr(res["bound"]),
                new_status=res["status"], new_nodes=res["nodes"], same_bound=same_bound,
                new_ge_stored=(res["bound"] >= rec["bound"]), retry=res["retry"], time=round(res["time"], 2))


def main():
    pkl, selp, outp, workers = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    st = pickle.load(gzip.open(pkl) if pkl.endswith(".gz") else open(pkl, "rb"))
    recs = st.recs
    sel = json.load(open(selp))
    tasks = [(s["rid"], s.get("group", ""), recs[s["rid"]]) for s in sel]
    pool = mp.Pool(workers, initializer=cs.init_worker, initargs=(st.T, "../logs/implied_06.json", True))
    n = same = ge = 0
    with open(outp, "w") as f:
        for r in pool.imap_unordered(run, tasks, chunksize=1):
            f.write(json.dumps(r) + "\n")
            f.flush()
            n += 1
            same += r["same_bound"]
            ge += r["new_ge_stored"]
    pool.close()
    print(f"records re-run: {n}; identical bound: {same}; new bound >= stored: {ge}")


if __name__ == "__main__":
    main()
