import json, glob, csv, math, statistics as st
rows = {}
for f in glob.glob("census_part*.jsonl"):
    for line in open(f):
        r = json.loads(line)
        if "error" in r: continue
        rows[r["name"]] = r
meta = {}
with open("instancedata.csv") as fh:
    for r in csv.DictReader(fh, delimiter=";"):
        meta[r["name"]] = r
def b(x): return x == "True"
recs = []
for nm, r in rows.items():
    m = meta.get(nm)
    if m is None: continue
    r["convex"] = b(m["convex"]); r["nvars"] = int(m["nvars"]); r["gap"] = m.get("gap")
    r["solved"] = (m.get("gap") not in (None, "", "inf") and float(m["gap"]) <= 1e-4) if m.get("gap") not in (None,"") else None
    recs.append(r)
nc = [r for r in recs if not r["convex"]]
print("instances analyzed:", len(recs), "nonconvex:", len(nc))
def summ(sel, key):
    vals = [r[key] for r in sel if r.get(key) is not None]
    return len(vals), (st.median(vals) if vals else None)
for lo, hi in [(0, 50), (50, 200), (200, 1000), (1000, 10**9)]:
    sel = [r for r in nc if lo <= r["n_nl"] < hi]
    k1, med_inc = summ(sel, "tw_fac_ub"); k2, med_nl = summ(sel, "tw_nlprimal_ub")
    small_inc = sum(1 for r in sel if r.get("tw_fac_ub") is not None and r["tw_fac_ub"] <= 10)
    small_nl = sum(1 for r in sel if r.get("tw_nlprimal_ub") is not None and r["tw_nlprimal_ub"] <= 10)
    ratio = [r["tw_nlprimal_ub"]/r["n_nl"] for r in sel if r.get("tw_nlprimal_ub") is not None and r["n_nl"]>0]
    print(f"n_nl in [{lo},{hi}): {len(sel)} inst; median tw_fac_ub {med_inc} (known {k1}), tw_inc<=10: {small_inc}; median tw_nl_ub {med_nl}, tw_nl<=10: {small_nl}; median tw_nl/n_nl {st.median(ratio) if ratio else None:.3f}")
# unsolved nonconvex with small incidence treewidth
uns = [r for r in nc if r.get("gap") not in (None, "") and r["gap"] != "inf" and float(r["gap"]) > 1e-4]
print("nonconvex with positive gap (open or unsolved per MINLPLib):", len(uns))
sel = sorted([r for r in uns if r.get("tw_fac_ub") is not None and r["tw_fac_ub"] <= 12 and r["n_nl"] >= 50], key=lambda r: r["n_nl"])
print("open/positive-gap, n_nl>=50, tw_fac_ub<=12:", len(sel))
for r in sel[:40]:
    print(r["name"], r["n"], r["n_nl"], r["tw_fac_ub"], r["tw_nlprimal_ub"], r["gap"])
json.dump(recs, open("census_merged.json", "w"))
