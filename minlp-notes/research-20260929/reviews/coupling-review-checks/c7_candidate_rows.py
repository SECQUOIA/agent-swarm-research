"""Classify the rows removed by the bag-targeted rule for all 25 census
candidates (1 <= k_best <= 16) of Section 7.3: linear equality (the scope of
Theorems 3.1/4.5), linear inequality (Section 2 only; slacks in Section 4),
nonlinear (outside Sections 3-4). Uses c6_census_sample.replay_bag.

Usage: python3 c7_candidate_rows.py
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import json
from c6_census_sample import replay_bag, LOGD, os

CENSUS = (_PUBLIC_REPO + '/research-20260929/treewidth-census/census_merged.json')
meta = {r["name"]: r for r in json.load(open(CENSUS))}
L1 = {json.loads(l)["name"]: json.loads(l) for l in open(os.path.join(LOGD, "census_k.jsonl"))}
L2 = {json.loads(l)["name"]: json.loads(l) for l in open(os.path.join(LOGD, "census_k2.jsonl"))}
cands = []
for nm, m in meta.items():
    if m["convex"] or m["n_nl"] < 100:
        continue
    ks = [v for v in (L1.get(nm, {}).get("k_heur"), L2.get(nm, {}).get("k_bag")) if v is not None]
    if ks and 1 <= min(ks) <= 16:
        cands.append(nm)
tot = {"all linear equality": 0, "linear (some inequality)": 0, "some nonlinear": 0}
for nm in sorted(cands):
    kb = L2[nm].get("k_bag"); kh = L1.get(nm, {}).get("k_heur")
    w, removed, cls = replay_bag(nm)
    nl = any(c.startswith("NL") for c in cls)
    ineq = any("<>" in c for c in cls)
    cat = "some nonlinear" if nl else ("linear (some inequality)" if ineq else "all linear equality")
    note = "" if (kb is not None and (kh is None or kb <= kh)) else f"  [k_best from densest-first rule, k_heur={kh}; classification is for the bag rule's rows]"
    tot[cat] += 1
    g = meta[nm]["gap"]
    op = g not in (None, "") and (g == "inf" or float(g) > 1e-4)
    print(f"{nm}: k_bag={kb} open={op} -> {cat}: {cls}{note}")
print(tot)
