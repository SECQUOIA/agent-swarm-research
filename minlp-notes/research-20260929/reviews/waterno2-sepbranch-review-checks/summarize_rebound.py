"""Summarize the vbb2 re-bounding of cert3 and recompute the DP exactly from
vbb2-certified values only.

Value used per record:
  finite rbb bound, vbb2 certified          -> the rbb bound (= vbb2 target)
  finite rbb bound, vbb2 not certified      -> vbb2's own lower bound
  rbb bound +inf, vbb2 proved empty         -> +inf
  rbb bound +inf, vbb2 certified 'required' -> the required value
  record not re-bounded                     -> -inf (treated as unknown)
Leaf pairs take the value of their CSRC record (containment checked by
ind_verify.py).
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import collections
import json
import math
import sys
from fractions import Fraction as F

import load_cert

T = 6
CERT = _RESEARCH + "/open-instances-wave2/waterno2/sepbranch/logs/cert3.pkl"


def main():
    P = load_cert.load(CERT).__dict__
    L = {}
    for line in open("logs/rebound_cert3_all.jsonl"):
        x = json.loads(line)
        L[x["rid"]] = x
    used = {int(v) for t in range(T) for v in P["tables"]["CSRC"][t].ravel()}
    print(f"records used by the DP: {len(used)}; re-bounded: {len(used & set(L))}")
    cnt = collections.Counter()
    by_group = collections.defaultdict(collections.Counter)
    val = {}
    for rid in used:
        rec = P["crecs"][rid]
        x = L.get(rid)
        if x is None:
            cnt["missing"] += 1
            val[rid] = None  # -inf
            continue
        st = x["vbb2_status"]
        fin = math.isfinite(rec["bound"])
        key = ("finite" if fin else "inf") + ":" + str(st)
        cnt[key] += 1
        by_group[x["group"]][key] += 1
        if st in ("infeasible", "empty box"):
            val[rid] = "inf"
        elif st == "certified":
            val[rid] = F(rec["bound"]) if fin else F(x["target"])
        else:
            b = x["vbb2_bound"]
            val[rid] = F(b) if b not in (None, "None") else None
    print("status counts:", dict(cnt))
    for g, c in sorted(by_group.items()):
        print(f"  group {g}: {dict(c)}")
    xs = [L[r] for r in used if r in L]
    tt = [x["time"] for x in xs]
    nn = [x["vbb2_nodes"] or 0 for x in xs]
    print(f"vbb2 time total {sum(tt):.0f} s, longest {max(tt):.1f} s; nodes total {sum(nn)}, max {max(nn)}")
    worst = sorted(xs, key=lambda x: -x["time"])[:3]
    print("longest runs:", [(x["rid"], x["t"], x["time"], x["vbb2_nodes"]) for x in worst])
    # finite rbb records certified by vbb2 where vbb2 target != rbb bound? (sanity)
    assert all(x["target"] == P["crecs"][x["rid"]]["bound"] for x in xs if math.isfinite(P["crecs"][x["rid"]]["bound"]))
    # exact DP over vbb2-based values
    M = []
    for t in range(T):
        CS = P["tables"]["CSRC"][t]
        rows = []
        for r in range(CS.shape[0]):
            row = []
            for c in range(CS.shape[1]):
                v = val[int(CS[r, c])]
                row.append(v)
            rows.append(row)
        M.append(rows)
    NEG = "neg"

    def conv(v):
        return NEG if v is None else v

    def add(a, b):
        if a == NEG or b == NEG:
            return NEG if "inf" not in (a, b) else "inf"
        if a == "inf" or b == "inf":
            return "inf"
        return a + b

    def better(a, b):  # a < b ?
        if a == NEG:
            return b != NEG
        if b == NEG:
            return False
        if a == "inf":
            return False
        if b == "inf":
            return True
        return a < b
    f = [conv(v) for v in M[0][0]]
    for t in range(1, T):
        nc = len(M[t][0])
        g = []
        for c in range(nc):
            best = "inf"
            for r in range(len(f)):
                v = add(f[r], conv(M[t][r][c]))
                if better(v, best):
                    best = v
            g.append(best)
        f = g
    V = f[0]
    if V in (NEG, "inf"):
        print("DP over vbb2 values:", V)
    else:
        down = F(V.numerator * 10**9 // V.denominator, 10**9)
        print(f"DP over vbb2-certified values (exact): {V} = {float(V)!r}; rounded down {float(down):.9f}")
        print("equals the authors' exact value:", V == F(19181443079783745, 70368744177664))


if __name__ == "__main__":
    main()
