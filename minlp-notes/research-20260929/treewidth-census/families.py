"""Family table and aggregate width counts for the census report (reads census_merged.json)."""
import json, re, collections
recs = json.load(open("census_merged.json"))
nc = [r for r in recs if not r["convex"]]
def g(r):
    try: return float(r["gap"])
    except (TypeError, ValueError): return None
fam = collections.defaultdict(list)
for r in nc:
    m = re.match(r"^(.*?)(\d+)$", r["name"])
    if m: fam[m.group(1)].append(r)
for f, L in sorted(fam.items()):
    if len(L) < 3: continue
    L = sorted(L, key=lambda r: r["n_nl"])
    ws = [r["tw_fac_ub"] for r in L if r["tw_fac_ub"] is not None]
    if not ws or max(ws) > 12 or L[-1]["n_nl"] < 3 * L[0]["n_nl"]: continue
    print("FAMILY", f)
    for r in L: print("   ", r["name"], r["n_nl"], r["tw_fac_ub"], r["tw_nlprimal_ub"], g(r))
big = [r for r in nc if r["n_nl"] >= 100]
print("nonconvex with n_nl>=100:", len(big))
for thr in [4, 8, 12, 20]:
    k = sum(1 for r in big if r["tw_fac_ub"] is not None and r["tw_fac_ub"] <= thr)
    k2 = sum(1 for r in big if r["tw_nlprimal_ub"] is not None and r["tw_nlprimal_ub"] <= thr)
    print(f"  tw_fac_ub<={thr}: {k} ({100*k/len(big):.1f}%)   tw_nl_ub<={thr}: {k2} ({100*k2/len(big):.1f}%)")
open_big = [r for r in big if g(r) is not None and g(r) > 1e-4]
print("open (gap>1e-4) nonconvex with n_nl>=100:", len(open_big))
for thr in [4, 8, 12]:
    print(f"  of which tw_fac_ub<={thr}:", sum(1 for r in open_big if r["tw_fac_ub"] is not None and r["tw_fac_ub"] <= thr))
