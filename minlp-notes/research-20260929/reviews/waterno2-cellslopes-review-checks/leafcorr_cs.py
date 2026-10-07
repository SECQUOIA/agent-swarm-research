"""Size of the Lemma-2 corrections in the distinct leaf-pair checks (own code).

usage: python3 leafcorr_cs.py cert.pkl.gz sel.json rebound.jsonl
"""
import json
import sys
from collections import Counter
from fractions import Fraction as F

import load_cs

d = load_cs.load(sys.argv[1])
recs = d["recs"]
sel = [s for s in json.load(open(sys.argv[2])) if s["kind"] == "leaf"]
res = {}
for line in open(sys.argv[3]):
    x = json.loads(line)
    res[x["key"]] = x
corr = []
c = Counter()
for s in sel:
    rec = recs[s["rid"]]
    delta = F(s["bound"]) - F(rec["bound"])
    corr.append(float(delta))
    c[(s["group"], "corrected" if delta != 0 else "no correction (smaller box, same slopes)",
       rec["src"][0] if rec["src"][0] == "cert3" else rec["src"][1], res[s["key"]]["vbb2_status"])] += 1
for k, v in sorted(c.items()):
    print(k, v)
neg = [x for x in corr if x != 0]
print(f"{len(neg)} of {len(sel)} leaf checks have a nonzero correction; range {min(neg):.4f} .. {max(neg):.4f}")
