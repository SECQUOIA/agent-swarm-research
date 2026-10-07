"""Independent recount of the coupling-row census shares (recheck of
theory-coupling/coupling.md, Section 7.3, second revision).

Reads only the author's raw JSONL records and the census metadata; the
counting code below is written from scratch (no import of the author's
analysis code). Checks:
  - baseline k = 0 with min(w_full, w_free) <= 12;
  - shares at k <= K for all rows, linear rows, linear equality rows;
  - the "classification" shares (bag-rule selections) 16.3% / 17.2%,
    using the saved census_k_rows.log for the per-instance row classes;
  - the candidate lists: 1 <= k <= 16, nonlinear width <= 12, open counts.

Usage: python3 r1_census_recount.py
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import json
import re

ROOT = (_PUBLIC_REPO + '/research-20260929/')
LOGS = ROOT + "theory-coupling/logs/"
meta = {r["name"]: r for r in json.load(open(ROOT + "treewidth-census/census_merged.json"))}
pop = sorted(n for n, m in meta.items() if (not m["convex"]) and m["n_nl"] >= 100)


def load(path):
    out = {}
    for line in open(path):
        r = json.loads(line)
        out[r["name"]] = r
    return out


dense = load(LOGS + "census_k.jsonl")
bag = load(LOGS + "census_k2.jsonl")
restr = load(LOGS + "census_k3.jsonl")


def is_open(name):
    g = meta[name]["gap"]
    if g in (None, ""):
        return False
    return g == "inf" or float(g) > 1e-4


def start_ok(name):
    r = dense.get(name)
    if r is None:
        return False
    ws = [w for w in (r["w_full"], r["w_free"]) if w is not None]
    return len(ws) > 0 and min(ws) <= 12


def k_any(name):
    if name not in dense:
        return None
    if start_ok(name):
        return 0
    ks = [x for x in (dense[name].get("k_heur"), bag.get(name, {}).get("k_bag")) if x is not None]
    return min(ks) if ks else None


def k_mode(name, mode):
    k0 = k_any(name)
    if k0 is None or k0 == 0:
        return k0
    r = restr.get(name)
    if r is None:
        return None
    ks = [x for x in (r[f"k_dense_{mode}"], r[f"k_bag_{mode}"]) if x is not None]
    return min(ks) if ks else None


N = len(pop)
print(f"population {N}; processed by census_k.py: {sum(n in dense for n in pop)}; "
      f"census_k3 records: {len(restr)}")
for label, fn in [("any rows", k_any), ("linear rows", lambda n: k_mode(n, "lin")),
                  ("linear equality rows", lambda n: k_mode(n, "lineq"))]:
    cells = []
    for K in (0, 2, 4, 8, 16, 32, 64):
        c = sum(1 for n in pop if fn(n) is not None and fn(n) <= K)
        cells.append(f"k<={K}: {c} ({100 * c / N:.1f}%)")
    print(f"[{label}] " + "; ".join(cells))

# consistency: census_k3 must cover every instance with 1 <= k_any <= 64
need = [n for n in pop if k_any(n) is not None and 1 <= k_any(n) <= 64]
missing = [n for n in need if n not in restr]
print(f"instances with 1 <= k_any <= 64: {len(need)}; missing from census_k3: {missing}")
# instances whose baseline changed because w_full < w_free
moved = [n for n in pop if n in dense and start_ok(n) and not
         (dense[n]["w_free"] is not None and dense[n]["w_free"] <= 12)]
print(f"k=0 only thanks to min(w_full, w_free): {moved}")

# classification shares from the saved row-class log
cls = {}
for line in open(LOGS + "census_k_rows.log"):
    m = re.match(r"^(\S+): k=\d+ .* -> (linear equality only|linear, some inequality|some nonlinear):", line)
    if m:
        cls[m.group(1)] = m.group(2)
k0 = sum(1 for n in pop if k_any(n) == 0)
gained = [n for n in pop if k_any(n) is not None and 1 <= k_any(n) <= 8]
eq = [n for n in gained if cls.get(n) == "linear equality only"]
lin = [n for n in gained if cls.get(n) in ("linear equality only", "linear, some inequality")]
print(f"k=0: {k0}; gained at k<=8 (any rows): {len(gained)}; of which linear-eq selections "
      f"{len(eq)}, linear selections {len(lin)}")
print(f"classification shares at k<=8: lineq {k0 + len(eq)} ({100 * (k0 + len(eq)) / N:.1f}%), "
      f"lin {k0 + len(lin)} ({100 * (k0 + len(lin)) / N:.1f}%)")
print(f"  with old baseline 85: lineq {(85 + len(eq))} ({100 * (85 + len(eq)) / N:.1f}%), "
      f"lin {85 + len(lin)} ({100 * (85 + len(lin)) / N:.1f}%)")

# candidates
c_any = [n for n in pop if k_any(n) is not None and 1 <= k_any(n) <= 16]
print(f"\ncandidates, any rows, 1<=k<=16: {len(c_any)}, open {sum(map(is_open, c_any))}")
for mode in ("lin", "lineq"):
    c = [n for n in pop if k_mode(n, mode) is not None and 1 <= k_mode(n, mode) <= 16
         and meta[n]["tw_nlprimal_ub"] is not None and meta[n]["tw_nlprimal_ub"] <= 12]
    op = sorted(n for n in c if is_open(n))
    print(f"candidates, {mode}, nonlinear width <= 12, 1<=k<=16: {len(c)}, open {len(op)}")
    print("  all:", ", ".join(f"{n}(k={k_mode(n, mode)})" for n in sorted(c)))
    print("  open:", ", ".join(op))
    entered = sorted(set(c) - set(c_any))
    left = sorted(set(c_any) - set(c))
    print(f"  entered vs any-rows list: {entered}; left: {left}")
for n in ("casctanks", "kall_ellipsoids_tc03c", "powerflow0030r", "tln12", "wastepaper6",
          "powerflow0057r"):
    print(f"  {n}: nlw={meta[n]['tw_nlprimal_ub']} open={is_open(n)} k_any={k_any(n)} "
          f"k_lin={k_mode(n, 'lin')} k_lineq={k_mode(n, 'lineq')} "
          f"w_full={dense[n]['w_full']} w_free={dense[n]['w_free']}")

# gap class stop reasons (bag rule), from raw traces
gap = [n for n in pop if meta[n]["tw_nlprimal_ub"] is not None and meta[n]["tw_nlprimal_ub"] <= 12
       and not (meta[n]["tw_fac_ub"] is not None and meta[n]["tw_fac_ub"] <= 12)]
cnt = {}
for n in gap:
    r = bag.get(n)
    tr = r["trace"]
    if tr[0][1] is None:
        why = "no start width"
    elif r["k_bag"] is not None:
        why = "reached"
    elif tr[-1][0] >= 64:
        why = "cap64"
    elif r["secs"] >= 240:
        why = "time"
    else:
        why = "no hub/other"
    cnt[why] = cnt.get(why, 0) + 1
print(f"\ngap class size {len(gap)}; bag-rule stop reasons {cnt}")
