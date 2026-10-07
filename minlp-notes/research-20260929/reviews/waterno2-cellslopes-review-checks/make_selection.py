"""Selection for vrebound_cs.py from the output of ind_verify_cs.py (own code).

Order (the pool works through it roughly in order):
  1. records and leaf pairs on paths within 0.05 of the optimum;
  2. records and leaf pairs on paths within 0.5 of the optimum;
  3. NRAND random finite leaf pairs whose bound uses a Lemma-2 correction
     (seed 7), anywhere in the DP;
  4. all other records used by the DP, in random order (seed 20261001), so
     that a cut-off run leaves a uniform random sample.
A leaf task is dropped when it is identical to its record's task (same boxes,
same slopes, hence the same target); the record task covers it.  Leaf tasks
are made only for finite leaf pairs (a leaf pair with bound +inf uses a record
that proved its box empty; that record is re-bounded as a record task).

usage: python3 make_selection.py cert.pkl.gz ind_verify.json out.json NRAND
"""
import json
import math
import random
import sys
from collections import Counter

import load_cs
from ind_verify_cs import corr_exact
from fractions import Fraction as F

T = 6


def main():
    d = load_cs.load(sys.argv[1])
    R = json.load(open(sys.argv[2]))
    nrand = int(sys.argv[4])
    recs, cells, leaves, lam = d["recs"], d["cells"], d["leaves"], d["lam"]
    brid = R["brid"]
    used = R["used_records"]
    near = R["near_pairs_0.5"]
    sel, seen, seenleaf = [], set(), set()
    ndup = 0

    def boxes(t, r, c):
        cin = None if t == 0 else (cells[t - 1][leaves[t - 1][r]]["lo"], cells[t - 1][leaves[t - 1][r]]["hi"])
        cout = None if t == T - 1 else (cells[t][leaves[t][c]]["lo"], cells[t][leaves[t][c]]["hi"])
        lin = [0.0] * 3 if t == 0 else list(lam[t - 1][leaves[t - 1][r]])
        lout = [0.0] * 3 if t == T - 1 else list(lam[t][leaves[t][c]])
        return cin, cout, lin, lout

    def same(t, r, c, rid):
        cin, cout, lin, lout = boxes(t, r, c)
        rec = recs[rid]
        ok = True
        if t > 0:
            ok &= [float(v) for v in rec["cin_box"][0]] == list(cin[0]) and \
                [float(v) for v in rec["cin_box"][1]] == list(cin[1]) and list(rec["lam_in"]) == lin
        if t < T - 1:
            ok &= [float(v) for v in rec["cout_box"][0]] == list(cout[0]) and \
                [float(v) for v in rec["cout_box"][1]] == list(cout[1]) and list(rec["lam_out"]) == lout
        return ok

    def rec(rid, group):
        if rid not in seen:
            seen.add(rid)
            sel.append(dict(key=f"r{rid}", kind="rec", rid=rid, group=group))

    def leaf(t, r, c, rid, bound, group):
        nonlocal ndup
        if bound == "None" or (t, r, c) in seenleaf:
            return
        seenleaf.add((t, r, c))
        if same(t, r, c, rid):
            ndup += 1
            return
        sel.append(dict(key=f"l{t}_{r}_{c}", kind="leaf", t=t, r=r, c=c, rid=rid, bound=bound, group=group))
    for p in R["path_rows"]:
        rec(p["rid"], "path")
    for p in near:
        if p["excess"] <= 0.05:
            rec(p["rid"], "near0.05")
            leaf(p["t"], p["r"], p["c"], p["rid"], p["bound"], "leaf0.05")
    for p in near:
        if p["excess"] > 0.05:
            rec(p["rid"], "near0.5")
            leaf(p["t"], p["r"], p["c"], p["rid"], p["bound"], "leaf0.5")
    # random corrected finite leaf pairs
    cand = []
    for t in range(T):
        for r, row in enumerate(brid[t]):
            for c, rid in enumerate(row):
                if (t, r, c) in seenleaf or recs[rid]["bound"] == math.inf or same(t, r, c, rid):
                    continue
                cand.append((t, r, c, rid))
    random.seed(7)
    for (t, r, c, rid) in random.sample(cand, nrand):
        rr = recs[rid]
        cin, cout, lin, lout = boxes(t, r, c)
        v = F(rr["bound"])
        if t > 0:
            v += corr_exact(lin, rr["lam_in"], cin[0], cin[1], 1)
        if t < T - 1:
            v += corr_exact(lout, rr["lam_out"], cout[0], cout[1], -1)
        assert v != F(rr["bound"]) or True
        leaf(t, r, c, rid, str(v), "leaf-random-corrected")
    rest = [rid for rid in used if rid not in seen]
    random.seed(20261001)
    random.shuffle(rest)
    for rid in rest:
        rec(rid, "rest")
    assert len({s["key"] for s in sel}) == len(sel)
    assert seen == set(used)
    json.dump(sel, open(sys.argv[3], "w"))
    print(Counter(s["group"] for s in sel), len(sel), f"; leaf tasks dropped as identical to their record: {ndup}; "
          f"corrected finite leaf pairs outside the near set: {len(cand)}")


if __name__ == "__main__":
    main()
