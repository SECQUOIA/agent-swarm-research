"""Classify the rows removed by the bag-targeted rule (census_k2.py) on the
candidate instances (1 <= k_best <= 16): linear equality (L=), linear
inequality (L<>), nonlinear (NL). Revision after review (F10).

Usage: python3 census_k_rows.py
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import sys, os, json, time
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260929/theory-coupling'))
from census_k import rowdata, fac_graph, read, OSIL_DIR, TARGET  # noqa: E402
from census_k2 import width_and_bag, ROWBASE, MAXR, TCAP  # noqa: E402
from census_k3 import row_types, free_rows  # noqa: E402

base = (_PUBLIC_REPO + '/research-20260929/theory-coupling/logs/')
r1 = {json.loads(l)["name"]: json.loads(l) for l in open(base + "census_k.jsonl")}
r2 = {json.loads(l)["name"]: json.loads(l) for l in open(base + "census_k2.jsonl")}
meta = {r["name"]: r for r in json.load(open(
    (_PUBLIC_REPO + '/research-20260929/treewidth-census/census_merged.json')))}
cands = []
for n in sorted(set(r1) | set(r2)):
    ks = [v for v in (r1.get(n, {}).get("k_heur"), r2.get(n, {}).get("k_bag")) if v is not None]
    if ks and 1 <= min(ks) <= 16:
        cands.append(n)
summary = {}
classes = {}
for name in cands:
    I = read(os.path.join(OSIL_DIR, name + ".osil"))
    rows = rowdata(I)
    types = row_types(I)
    free = free_rows(I, rows)
    removed, order, t0 = set(), [], time.time()
    while True:
        adj = fac_graph(rows, free | removed)
        w, bag = width_and_bag(adj)
        if w is None or w <= TARGET or len(removed) >= MAXR or time.time() - t0 > TCAP:
            break
        rn = [v for v in bag if isinstance(v, int) and v >= ROWBASE]
        if not rn:
            break
        best = max(rn, key=lambda v: len(adj[v]))
        r = best - ROWBASE - 1
        removed.add(r)
        order.append(r)
    labels = ["L=" if types[r] == (True, True) else ("L<>" if types[r][0] else "NL") for r in order]
    cls = ("some nonlinear" if "NL" in labels else
           ("linear, some inequality" if "L<>" in labels else "linear equality only"))
    summary[cls] = summary.get(cls, 0) + 1
    classes[name] = cls
    g = meta[name]["gap"]
    op = g == "inf" or (g not in ("", None) and float(g) > 1e-4)
    print(f"{name}: k={len(order)} final width={w} open={op} nlw={meta[name]['tw_nlprimal_ub']} "
          f"-> {cls}: {labels}")
print(summary)

# shares at k <= 8 by classification of the removed rows (baseline min(w_full, w_free))
pop = [n for n, m in meta.items() if not m["convex"] and m["n_nl"] >= 100]


def base_ok(n):
    r = r1.get(n, {})
    ws = [w for w in (r.get("w_full"), r.get("w_free")) if w is not None]
    return bool(ws) and min(ws) <= TARGET


def kbest(n):
    ks = [v for v in (r1.get(n, {}).get("k_heur"), r2.get(n, {}).get("k_bag")) if v is not None]
    return min(ks) if ks else None


k0 = sum(1 for n in pop if base_ok(n))
gained = [n for n in pop if not base_ok(n) and kbest(n) is not None and 1 <= kbest(n) <= 8]
eq = sum(1 for n in gained if classes.get(n) == "linear equality only")
lin = sum(1 for n in gained if classes.get(n) in ("linear equality only", "linear, some inequality"))
N = len(pop)
print(f"k=0 (baseline min(w_full,w_free)): {k0} ({100*k0/N:.1f}%); gained at k<=8: {len(gained)}")
print(f"k<=8 counting only linear-equality selections: {k0+eq} ({100*(k0+eq)/N:.1f}%); "
      f"only linear selections: {k0+lin} ({100*(k0+lin)/N:.1f}%)")
