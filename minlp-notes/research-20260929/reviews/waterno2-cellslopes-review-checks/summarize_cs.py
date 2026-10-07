"""Summary of the vbb2 re-bounding and the exact DP from vbb2-certified values
alone (own code).

For every leaf pair (t, r, c) the record rid = brid[t][r][c] chosen by
ind_verify_cs.py is used.  Its vbb2 value on the record's own box and slopes:
  certified  -> the target (= the rbb bound; 1e4 for rbb +inf records),
  infeasible -> +inf (vbb2 proved the record box empty without objective cutoff),
  limit      -> vbb2's own (lower) bound,
  not run    -> reported; the DP is then also given with the rbb value
                (marked as NOT independent).
The leaf-pair value is the vbb2 value plus the exact Lemma-2 correction to the
leaf slopes over the leaf boxes; the shortest path is computed exactly.

usage: python3 summarize_cs.py cert.pkl.gz ind_verify.json rebound.jsonl [prev_review_rebound.jsonl prev_cert3.pkl]
"""
import json
import math
import sys
from collections import Counter
from fractions import Fraction as F

import numpy as np

import load_cs
from ind_verify_cs import corr_exact

T = 6


def main():
    d = load_cs.load(sys.argv[1])
    R = json.load(open(sys.argv[2]))
    recs, cells, leaves, lam = d["recs"], d["cells"], d["leaves"], d["lam"]
    brid = R["brid"]
    used = R["used_records"]
    res = {}
    for line in open(sys.argv[3]):
        x = json.loads(line)
        res[x["key"]] = x
    # ---------------------------------------------------------------- records
    val = {}
    missing = []
    cnt = Counter()
    times = []
    for rid in used:
        x = res.get(f"r{rid}")
        rb = recs[rid]["bound"]
        kind = "inf" if rb == math.inf else "finite"
        if x is None:
            missing.append(rid)
            cnt[(kind, "not run")] += 1
            continue
        times.append(x["time"])
        st = x["vbb2_status"]
        if st == "infeasible":
            val[rid] = None                      # +inf
        elif x["vbb2_bound"] in ("None", None):
            val[rid] = "unbounded"
        else:
            val[rid] = F(x["vbb2_bound"])
            if st == "certified":
                assert val[rid] == F(x["target"])
        cnt[(kind, st)] += 1
    print(f"records used by the DP: {len(used)}; re-bounded: {len(used) - len(missing)}; not run: {len(missing)}")
    for k, v in sorted(cnt.items()):
        print(f"   rbb {k[0]:6s} vbb2 {k[1]:10s}: {v}")
    if times:
        t = np.array(times)
        print(f"   vbb2 time: sum {t.sum():.0f}s, median {np.median(t):.2f}s, max {t.max():.1f}s")
    lim = [rid for rid in used if f"r{rid}" in res and res[f"r{rid}"]["vbb2_status"] == "limit"]
    for rid in lim:
        x = res[f"r{rid}"]
        print(f"   limit: record {rid} t={recs[rid]['t']} rbb bound {recs[rid]['bound']!r} vbb2 bound "
              f"{float(F(x['vbb2_bound'])) if x['vbb2_bound'] != 'None' else None} nodes {x['nodes']} time {x['time']}")
    by_src = Counter()
    for rid in used:
        if f"r{rid}" in res:
            s = recs[rid]["src"]
            by_src[s[0] if s[0] == "cert3" else s[1]] += 1
    print("   re-bounded records by origin:", dict(by_src))
    # ---------------------------------------------------------------- leaf checks
    lc = [x for x in res.values() if x["kind"] == "leaf"]
    print(f"leaf-pair checks (leaf boxes, leaf slopes, target = exact DP pair bound rounded down): {len(lc)}; "
          f"{Counter((x['group'], x['vbb2_status']) for x in lc)}")

    # ---------------------------------------------------------------- exact DP from vbb2 values
    def dp(use_rbb_for_missing):
        Bq = []
        nmiss = 0
        for t in range(T):
            M = []
            for r, row in enumerate(brid[t]):
                out = []
                for c, rid in enumerate(row):
                    if rid in val:
                        v = val[rid]
                        if v == "unbounded":
                            raise RuntimeError("unbounded vbb2 value")
                    else:
                        nmiss += 1
                        if not use_rbb_for_missing:
                            out.append("missing")
                            continue
                        b = recs[rid]["bound"]
                        v = None if b == math.inf else F(b)
                    if v is None:
                        out.append(None)
                        continue
                    rec = recs[rid]
                    if t > 0:
                        cid = leaves[t - 1][r]
                        v += corr_exact(lam[t - 1][cid], rec["lam_in"], cells[t - 1][cid]["lo"],
                                        cells[t - 1][cid]["hi"], 1)
                    if t < T - 1:
                        cid = leaves[t][c]
                        v += corr_exact(lam[t][cid], rec["lam_out"], cells[t][cid]["lo"], cells[t][cid]["hi"], -1)
                    out.append(v)
                M.append(out)
            Bq.append(M)
        if any(v == "missing" for M in Bq for row in M for v in row):
            return None, nmiss
        f = list(Bq[0][0])
        for t in range(1, T):
            g = []
            for c in range(len(Bq[t][0])):
                best = None
                for r in range(len(f)):
                    if f[r] is None or Bq[t][r][c] is None:
                        continue
                    v = f[r] + Bq[t][r][c]
                    if best is None or v < best:
                        best = v
                g.append(best)
            f = g
        return f[0], nmiss
    V, nm = dp(False)
    if V is not None:
        down = F(V.numerator * 10**9 // V.denominator, 10**9)
        print(f"EXACT DP FROM vbb2 VALUES ONLY: {V} = {float(V)!r}; rounded down {float(down):.9f}; "
              f"authors' value {R['value']}: {'identical' if str(V) == R['value'] else 'DIFFERENT'}")
    else:
        V2, nm = dp(True)
        print(f"not all records re-bounded ({nm} leaf pairs use a record not yet re-bounded); DP with rbb values "
              f"for those (NOT independent): {float(V2)!r}")
    if len(sys.argv) > 5:
        # cross-reference with the earlier review's full re-bounding of cert3's DP records
        import pickle
        import types
        prev = {json.loads(l)["rid"]: json.loads(l) for l in open(sys.argv[4])}
        mod = types.ModuleType("dpcells")

        class CellPlan:
            pass
        mod.CellPlan = CellPlan
        sys.modules["dpcells"] = mod
        P = pickle.load(open(sys.argv[5], "rb")).__dict__
        c3 = [rid for rid in used if recs[rid]["src"][0] == "cert3"]
        inprev = [rid for rid in c3 if recs[rid]["src"][1] in prev]
        print(f"cert3 records used by this DP: {len(c3)}; of these re-bounded by the earlier review: {len(inprev)}")
        same = sum(1 for rid in c3 if P["crecs"][recs[rid]["src"][1]]["bound"] == recs[rid]["bound"])
        print(f"   cert3 records whose bound equals the cert3 pickle's record: {same} of {len(c3)}")


if __name__ == "__main__":
    main()
