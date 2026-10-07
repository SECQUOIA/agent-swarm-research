"""Recount the census tables of Section 7.3 from the author's JSONL logs
(independent of census_k_analyze.py), list the 25 candidates, and break down
why the bag-targeted rule stopped in the gap class.

Usage: python3 c10_census_recount.py
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import json, statistics as st
from collections import Counter
D = (_PUBLIC_REPO + '/research-20260929/theory-coupling/logs/')
CENSUS = (_PUBLIC_REPO + '/research-20260929/treewidth-census/census_merged.json')
meta = {r["name"]: r for r in json.load(open(CENSUS))}
pop = [r for r in meta.values() if not r["convex"] and r["n_nl"] >= 100]
r1 = {json.loads(l)["name"]: json.loads(l) for l in open(D + "census_k.jsonl")}
r2 = {json.loads(l)["name"]: json.loads(l) for l in open(D + "census_k2.jsonl")}
def isopen(m):
    g = m.get("gap"); return g not in (None, "") and (g == "inf" or float(g) > 1e-4)
kb = {}
for m in pop:
    c = [v for v in (r1.get(m["name"], {}).get("k_heur"), r2.get(m["name"], {}).get("k_bag")) if v is not None]
    kb[m["name"]] = min(c) if c else None
groups = {"all": pop,
          "nl<=12": [m for m in pop if m["tw_nlprimal_ub"] is not None and m["tw_nlprimal_ub"] <= 12],
          "gap": [m for m in pop if m["tw_nlprimal_ub"] is not None and m["tw_nlprimal_ub"] <= 12 and not (m["tw_fac_ub"] is not None and m["tw_fac_ub"] <= 12)],
          "open": [m for m in pop if isopen(m)]}
print("population", len(pop), "census_k processed", sum(m["name"] in r1 for m in pop), "census_k2 processed", sum(m["name"] in r2 for m in pop))
for g, ms in groups.items():
    row = [sum(1 for m in ms if kb[m["name"]] is not None and kb[m["name"]] <= K) for K in (0, 2, 4, 8, 16, 32, 64)]
    print(g, len(ms), row, [f"{100*x/len(ms):.1f}%" for x in row])
cand = sorted(n for n, v in kb.items() if v is not None and 1 <= v <= 16)
print(len(cand), "candidates with 1<=k_best<=16;", sum(isopen(meta[n]) for n in cand), "open")
for n in cand:
    print(f"  {n}: k_heur={r1[n].get('k_heur')} k_bag={r2[n].get('k_bag')} nl_w={meta[n]['tw_nlprimal_ub']} fac_w={meta[n]['tw_fac_ub']} open={isopen(meta[n])}")
def reason(r):
    if r.get("k_bag") is not None: return "reached width<=12"
    if r["trace"] and r["trace"][-1][1] is None: return "width timeout"
    if len(r["removed_degrees"]) >= 64: return "hit 64-row cap"
    if r["secs"] >= 240: return "hit time cap"
    return "stopped: no row hub in width bag"
gap = groups["gap"]
print("gap class stop reasons:", dict(Counter(reason(r2[m["name"]]) for m in gap)))
for why in sorted(set(reason(r2[m["name"]]) for m in gap)):
    sel = [r2[m["name"]] for m in gap if reason(r2[m["name"]]) == why]
    rem = [len(r["removed_degrees"]) for r in sel]
    w0 = [r["trace"][0][1] for r in sel if r["trace"] and r["trace"][0][1] is not None]
    wf = [w for w in (next((w for _, w in reversed(r["trace"]) if w is not None), None) for r in sel) if w is not None]
    print(f"  {why}: n={len(sel)} removed median={st.median(rem) if rem else None} start width median={st.median(w0) if w0 else None} final width median={st.median(wf) if wf else None}")
sel = [r2[m["name"]] for m in gap if r2[m["name"]]["trace"] and r2[m["name"]]["trace"][0][1] is not None]
w0 = [r["trace"][0][1] for r in sel]; wf = [next(w for _, w in reversed(r["trace"]) if w is not None) for r in sel]
print("note's gap-class statistics recomputed: n", len(sel), "removed median", st.median([len(r['removed_degrees']) for r in sel]),
      "start median", st.median(w0), "final median", st.median(wf), "halved", sum(b <= a / 2 for a, b in zip(w0, wf)))
