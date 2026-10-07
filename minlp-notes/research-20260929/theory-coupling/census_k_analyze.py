"""Summarize logs/census_k.jsonl (see census_k.py).

Usage: python3 census_k_analyze.py
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import json, statistics as st

CENSUS = (_PUBLIC_REPO + '/research-20260929/treewidth-census/census_merged.json')
meta = {r["name"]: r for r in json.load(open(CENSUS))}
pop = [r for r in meta.values() if not r["convex"] and r["n_nl"] >= 100]
recs = {}
for line in open("logs/census_k.jsonl"):
    r = json.loads(line)
    recs[r["name"]] = r
recs2 = {}
try:
    for line in open("logs/census_k2.jsonl"):
        r = json.loads(line)
        recs2[r["name"]] = r
except FileNotFoundError:
    pass
for nm, r in recs.items():
    r2 = recs2.get(nm, {})
    r["k_bag"] = r2.get("k_bag")
    cands = [v for v in (r.get("k_heur"), r["k_bag"]) if v is not None]
    r["k_best"] = min(cands) if cands else None


def isopen(m):
    g = m.get("gap")
    return g not in (None, "") and (g == "inf" or float(g) > 1e-4)


KEY = "k_heur"


def kval(r):
    return r.get(KEY) if r else None


print(f"population (nonconvex, >=100 nonlinear vars): {len(pop)}; processed: "
      f"{sum(1 for m in pop if m['name'] in recs)}")
groups = {
    "all": pop,
    "nlprimal<=12": [m for m in pop if m["tw_nlprimal_ub"] is not None and m["tw_nlprimal_ub"] <= 12],
    "nlprimal<=12, fac>12 (gap class)": [m for m in pop if m["tw_nlprimal_ub"] is not None
                                         and m["tw_nlprimal_ub"] <= 12
                                         and not (m["tw_fac_ub"] is not None and m["tw_fac_ub"] <= 12)],
    "open (gap>1e-4)": [m for m in pop if isopen(m)],
}
Ks = [0, 1, 2, 4, 8, 16, 32, 64]
for KEY in ["k_heur", "k_bag", "k_best"]:
 print(f"\n===== {KEY} =====")
 for gname, g in groups.items():
     done = [m for m in g if m["name"] in recs]
     row = []
     for K in Ks:
         c = sum(1 for m in done if kval(recs[m["name"]]) is not None and kval(recs[m["name"]]) <= K)
         row.append(f"k<={K}: {c} ({100*c/len(g):.1f}%)")
     unf = sum(1 for m in done if kval(recs[m["name"]]) is None)
     print(f"\n[{gname}] n={len(g)}, processed={len(done)}, k not reached/limit={unf}")
     print("  " + "; ".join(row))

# effect of free rows alone
done = [m for m in pop if m["name"] in recs]
fr = [recs[m["name"]] for m in done]
c_full = sum(1 for r in fr if r["w_full"] is not None and r["w_full"] <= 12)
c_free = sum(1 for r in fr if r["w_free"] is not None and r["w_free"] <= 12)
print(f"\nwidth<=12 with all rows (recomputed): {c_full}; after dropping objective/"
      f"objective-defining rows only: {c_free} (of {len(done)} processed)")
degs = [r["deg_kth"] for r in fr if r.get("deg_kth")]
if degs:
    print(f"degree of the last removed row (k-th densest), median {st.median(degs)}, "
          f"quartiles {st.quantiles(degs, n=4)}")
ks = [r["k_heur"] for r in fr if r.get("k_heur")]
print(f"k_heur among instances needing >=1 row: median {st.median(ks) if ks else None}, n={len(ks)}")

print("\nnamed families:")
for pref in ["waterno2_", "lnts", "camshape", "rocket", "kriging", "catmix", "chain",
             "dtoc", "optcdeg", "lukvle"]:
    names = sorted(n for n in recs if n.startswith(pref))
    for n in names[:6]:
        r = recs[n]
        print(f"  {n}: w_full={r['w_full']} w_free={r['w_free']} k={r['k_heur']} "
              f"trace={r['trace']} top_deg={r['top_degrees'][:3]}")

print("\nsample of gap-class instances with small k (k in 1..8):")
sel = [m for m in groups["nlprimal<=12, fac>12 (gap class)"] if m["name"] in recs
       and kval(recs[m["name"]]) and kval(recs[m["name"]]) <= 8]
for m in sorted(sel, key=lambda m: m["name"])[:40]:
    r = recs[m["name"]]
    print(f"  {m['name']}: n={m['n']} nl_w={m['tw_nlprimal_ub']} fac_w={m['tw_fac_ub']} "
          f"w_free={r['w_free']} k={r['k_heur']} trace={r['trace']} gap={m['gap']}")

# ---------------------------------------------------------------------------
# Revision after review (F10-F13): gap-class statistics, stop reasons of the
# bag-targeted rule, non-monotone baseline, and shares for linear rows only.
import os
print("\n===== revision: gap class and stop reasons (bag-targeted rule) =====")
gapc = groups["nlprimal<=12, fac>12 (gap class)"]
wf = [recs[m["name"]]["w_free"] for m in gapc if m["name"] in recs and recs[m["name"]]["w_free"] is not None]
print(f"gap class: w_free median {st.median(wf)}, quartiles {st.quantiles(wf, n=4)}, n={len(wf)}")
reasons = {}
for m in gapc:
    r2 = recs2.get(m["name"])
    if not r2 or not r2["trace"]:
        continue
    tr = r2["trace"]
    if tr[0][1] is None:
        why = "width timeout at start"
    elif r2.get("k_bag") is not None:
        why = "reached width 12"
    elif tr[-1][0] >= 64:
        why = "64-row cap"
    elif r2.get("secs", 0) >= 240:
        why = "time cap"
    elif tr[-1][1] is None:
        why = "width timeout later"
    else:
        why = "no row hub in the widest bag"
    ws = [w for (_, w) in tr if w is not None]
    reasons.setdefault(why, []).append((tr[-1][0], ws[0] if ws else None, ws[-1] if ws else None))
for why, lst in sorted(reasons.items()):
    rem = [a for a, _, _ in lst]
    w0 = [b for _, b, _ in lst if b is not None]
    w1 = [c for _, _, c in lst if c is not None]
    print(f"  {why}: {len(lst)} instances; rows removed median {st.median(rem) if rem else None}; "
          f"width median {st.median(w0) if w0 else None} -> {st.median(w1) if w1 else None}")
allrem = [a for lst in reasons.values() for a, b, c in lst if b is not None]
allw0 = [b for lst in reasons.values() for a, b, c in lst if b is not None]
allw1 = [c for lst in reasons.values() for a, b, c in lst if b is not None]
print(f"  all with a starting width: {len(allrem)}; rows removed median {st.median(allrem)}; "
      f"width median {st.median(allw0)} -> {st.median(allw1)}")
degs = [d for m in gapc if m["name"] in recs2 for d in recs2[m["name"]].get("removed_degrees", [])]
print(f"  degree of rows removed by the bag rule: median {st.median(degs)}, quartiles {st.quantiles(degs, n=4)}")

print("\n===== revision: baseline min(w_full, w_free) and linear-row shares =====")
rec3 = {}
if os.path.exists("logs/census_k3.jsonl"):
    for line in open("logs/census_k3.jsonl"):
        r = json.loads(line)
        rec3[r["name"]] = r


def k_all(name):
    r = recs.get(name)
    if r is None:
        return None
    wf_, wu_ = r.get("w_free"), r.get("w_full")
    base = min(w for w in (wf_, wu_) if w is not None) if (wf_ is not None or wu_ is not None) else None
    if base is not None and base <= 12:
        return 0
    return r["k_best"]


def k_restricted(name, mode):
    k0 = k_all(name)
    if k0 == 0 or k0 is None:
        return k0
    r = rec3.get(name)
    if r is None:
        return None
    ks = [v for v in (r.get(f"k_dense_{mode}"), r.get(f"k_bag_{mode}")) if v is not None]
    return min(ks) if ks else None


for label, fn in [("all rows (baseline fixed)", k_all),
                  ("linear rows", lambda n: k_restricted(n, "lin")),
                  ("linear equality rows", lambda n: k_restricted(n, "lineq"))]:
    print(f"\n[{label}]")
    for gname, g in groups.items():
        row = []
        for K in Ks:
            c = sum(1 for m in g if fn(m["name"]) is not None and fn(m["name"]) <= K)
            row.append(f"k<={K}: {c} ({100*c/len(g):.1f}%)")
        print(f"  [{gname}] n={len(g)}: " + "; ".join(row))
