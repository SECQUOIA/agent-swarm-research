"""Re-bound records of a cell-slope certificate with the recheck's vbb2.py
(exact-rational node bounds; no code shared with rbb.py).

The driver is the independent review's `rebound.run`
(reviews/waterno2-sepbranch-review-checks/rebound.py): first verifier's model
and implied bounds, the review's own terminal row, the record's boxes and the
record's own slopes (lam_in, lam_out), mu = 0.  Target: the record's rbb bound;
records with bound +inf get target 1e4 (vbb2 must prove the box empty).

Selection: the records verify_cs.py uses on the minimizing path, plus
`nrand` random records among the used records that were created by the
cell-slope runs (not cert3), plus optionally all used new records ("all").

usage: python3 crosscheck_cs.py state.pkl verify.json out.jsonl nrand seed workers time_limit [all]
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../../..'))
import json
import math
import multiprocessing as mp
import pickle
import random
import sys

import gzip
import cs  # noqa: F401  (unpickling)

sys.path.insert(0, _RESEARCH + "/reviews/waterno2-sepbranch-review-checks")
import rebound  # noqa: E402


def main():
    stp, vp, outp = sys.argv[1], sys.argv[2], sys.argv[3]
    nrand, seed, workers, tl = int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), float(sys.argv[7])
    allnew = len(sys.argv) > 8 and sys.argv[8] == "all"
    leafmode = len(sys.argv) > 8 and sys.argv[8] == "leaf"
    st = pickle.load(gzip.open(stp, "rb") if stp.endswith(".gz") else open(stp, "rb"))
    V = json.load(open(vp))
    used = V["used_records"]
    path = [r["rid"] for r in V["path_rows"]]
    new_used = [rid for rid in used if st.recs[rid].get("src", ("cert3",))[0] != "cert3"]
    sel = [(rid, "path") for rid in path]
    rest = [rid for rid in new_used if rid not in path]
    random.seed(seed)
    nearmode = len(sys.argv) > 8 and sys.argv[8] == "near"
    if nearmode:
        sel += [(rid, "near") for rid in V["near_records"] if rid not in path]
        sel += [(rid, "random-new") for rid in random.sample(rest, min(nrand, len(rest)))
                if rid not in V["near_records"]]
    elif allnew:
        sel += [(rid, "new") for rid in rest]
    else:
        sel += [(rid, "random-new") for rid in random.sample(rest, min(nrand, len(rest)))]
    done = set()
    try:
        for line in open(outp):
            done.add(json.loads(line)["rid"])
    except FileNotFoundError:
        pass
    tasks = []
    group = {}
    for rid, g in sel:
        if rid in done:
            continue
        rec = st.recs[rid]
        target = rec["bound"] if math.isfinite(rec["bound"]) else 1e4
        tasks.append((rid, rec, target, tl))
        group[rid] = g
    if leafmode:
        # re-bound LEAF pairs (leaf boxes, leaf slopes) at the exact pair bound used by the DP
        # (rounded down to a float); checks the slope corrections as well as the records
        from fractions import Fraction
        tasks = []
        for i, lc in enumerate(V["leaf_checks"]):
            key = 10**7 + i
            if key in done:
                continue
            b = Fraction(lc["bound"])
            tf = float(b)
            if Fraction(tf) > b:
                tf = math.nextafter(tf, -math.inf)
            rec = dict(t=lc["t"], cin_box=lc["cin_box"], cout_box=lc["cout_box"], lam_in=lc["lam_in"],
                       lam_out=lc["lam_out"], bound=tf, status="leafcheck", src=("leaf", lc["group"], lc["rid"]))
            st.recs.append(rec)
            group[len(st.recs) - 1] = lc["group"]
            tasks.append((len(st.recs) - 1, rec, tf, tl))
    print(f"{len(tasks)} records to re-bound ({len(new_used)} new records used; path {path})", flush=True)
    fh = open(outp, "a")
    with mp.Pool(workers) as pool:
        for rid, res in pool.imap_unordered(rebound.run, tasks, chunksize=1):
            rec = st.recs[rid]
            line = dict(rid=rid, t=rec["t"], group=group[rid], src=str(rec.get("src")), rbb_bound=rec["bound"],
                        rbb_status=rec["status"], vbb2_status=res.get("status"), vbb2_bound=str(res.get("bound")),
                        vbb2_nodes=res.get("nodes"), time=round(res["time"], 1), target=res["target"])
            fh.write(json.dumps(line) + "\n")
            fh.flush()
            print(json.dumps(line), flush=True)


if __name__ == "__main__":
    main()
