#!/usr/bin/env python3
"""Reviewer comparison of re-extracted solver values with certificates and MINLPLib listings.

Inputs: mine_pd.json (from extract.py + reviewer check), extract.json,
../../solver-runs/references.csv (values only; each certificate/primal string
is checked for presence in the research-tree source documents below),
../../../bound-audit/pages.json (MINLPLib listings, recomputed here).
"""
import csv
import json
import re
from decimal import Decimal as D, getcontext
from pathlib import Path

getcontext().prec = 50
HERE = Path(__file__).resolve().parent
TOP = HERE.parents[2]  # research-20260929
SR = TOP / "publication" / "solver-runs"

mine = json.load(open(HERE / "mine_pd.json"))
ext = {f"{r['instance']}__{r['solver']}": r for r in json.load(open(HERE / "extract.json"))}
refs = {r["instance"]: r for r in csv.DictReader(open(SR / "references.csv"))}
pages = {p["name"]: p for p in json.load(open(TOP / "bound-audit" / "pages.json"))}

# --- 1. are the reference strings present in source documents (outside publication/solver-runs)?
src_text = ""
for p in list(TOP.glob("*.md")) + list(TOP.glob("reviews/**/*.md")) + list(TOP.glob("open-instances-*/**/*.md")) \
        + list(TOP.glob("publication/primal/**/*.md")) + list(TOP.glob("publication/reviews/primal-*.md")) \
        + list(TOP.glob("publication/literature/**/*.md")):
    src_text += p.read_text(errors="replace").replace("−", "-").replace(" ", "").replace(",", "") + "\n"


def present(tok):
    t = tok.lstrip("-")
    # allow the source to print more digits than the token
    return t in src_text


missing = []
for inst, r in refs.items():
    for col in ("certificate_dual", "reference_primal"):
        if not present(r[col]):
            missing.append((inst, col, r[col]))
print("reference strings not found verbatim in sources:", missing)

# --- 2. MINLPLib listed best dual / primal recomputed from pages.json
lst_issues = []
listed = {}
for inst, r in refs.items():
    p = pages[inst]
    sense = p["sense"]
    assert sense == r["sense"], (inst, sense, r["sense"])
    duals = [D(d["value"]) for d in p["duals"] if d.get("value") not in (None, "")]
    prim = [D(x["value"]) for x in p["points"] if x.get("value") not in (None, "") and x.get("section") == "primal"]
    bd = (max(duals) if sense == "min" else min(duals)) if duals else None
    bp = (min(prim) if sense == "min" else max(prim)) if prim else None
    listed[inst] = (bd, bp)
    ad = D(r["listed_dual"]) if r["listed_dual"] else None
    ap = D(r["listed_primal"]) if r["listed_primal"] else None
    if ad != bd or ap != bp:
        lst_issues.append((inst, "mine", bd, bp, "author", ad, ap))
print("listed best dual/primal mismatches:", lst_issues)

# --- 3. comparisons
INF = D("Infinity")
rows = []
for key, m in sorted(mine.items()):
    inst, solver = key.split("__")
    r = refs[inst]
    s = 1 if r["sense"] == "min" else -1
    C, Pref = D(r["certificate_dual"]), D(r["reference_primal"])
    P = D(m["P"]) if m["P"] else None
    Dv = D(m["D"]) if m["D"] else None
    logP = D(m["logP"]) if m["logP"] not in (None, "", "-") else None
    if logP is not None and abs(logP) >= D("1e20"):
        logP = None
    if solver == "SCIP" and logP is not None and ext[key]["log_primal"] and "e+20" in ext[key]["log_primal"]:
        logP = None
    bd, bp = listed[inst]
    rows.append(dict(
        key=key, inst=inst, solver=solver, s=s, scope=r["certificate_scope"], ms=m["ms"], ss=m["ss"],
        P=P, D=Dv, logP=logP, C=C, Pref=Pref, bd=bd, bp=bp,
        deficit=None if Dv is None else (s * (C - Dv) if Dv.is_finite() else INF),
        dual_beats_cert=Dv is not None and Dv.is_finite() and s * (Dv - C) > 0,
        dual_cuts_ref=Dv is not None and Dv.is_finite() and s * (Dv - Pref) > 0,
        dual_beats_listed=Dv is not None and Dv.is_finite() and bd is not None and s * (Dv - bd) > 0,
        P_beyond_cert=P is not None and s * (P - C) < 0,
        logP_beyond_cert=logP is not None and s * (logP - C) < 0,
        P_beats_listed=P is not None and bp is not None and s * (bp - P) > 0,
        P_beats_ref=P is not None and s * (Pref - P) > 0,
    ))

fin = [x for x in rows if x["D"] is not None and x["D"].is_finite()]
print("finite duals:", len(fin), {s: sum(1 for x in fin if x["solver"] == s) for s in ("BARON", "GUROBI", "SCIP")})
print("  OSIL scope:", sum(1 for x in fin if x["scope"] == "OSIL"), "R scope:", sum(1 for x in fin if x["scope"] != "OSIL"))
print("dual beats certificate:", [x["key"] for x in rows if x["dual_beats_cert"]])
print("dual cuts off reference primal:", [x["key"] for x in rows if x["dual_cuts_ref"]])
print("min positive deficit:", min((x["deficit"], x["key"]) for x in fin))
print("dual beats MINLPLib listed best dual:", [(x["key"], str(x["D"]), str(x["bd"])) for x in rows if x["dual_beats_listed"]])
pb = [x for x in rows if x["P_beyond_cert"]]
lb = [x for x in rows if x["logP_beyond_cert"]]
print("returned primal beyond certificate:", len(pb), "OSIL", sum(1 for x in pb if x["scope"] == "OSIL"))
print("log incumbent beyond certificate:", len(lb))
print("distinct pairs:", len({x["key"] for x in pb} | {x["key"] for x in lb}))
print("log-only:", sorted({x["key"] for x in lb} - {x["key"] for x in pb}))
print("returned-only:", sorted({x["key"] for x in pb} - {x["key"] for x in lb}))
for x in sorted(pb, key=lambda x: x["key"]):
    print(f"  {x['key']:28s} {x['scope'][:4]} ms{x['ms']} P-C (sense adj) {x['s'] * (x['P'] - x['C']):.6e}")
print("returned primal better than MINLPLib listed best primal:",
      [(x["key"], str(x["P"]), str(x["bp"])) for x in rows if x["P_beats_listed"]])
print("returned primal better than reference primal:", [(x["key"], f"{x['s'] * (x['Pref'] - x['P']):.3e}") for x in rows if x["P_beats_ref"]])
# global optimality claims
print("model status 1 rows:", [(x["key"], str(x["P"]), str(x["D"])) for x in rows if x["ms"] == "1"])
print("model status 2 rows:", [x["key"] for x in rows if x["ms"] == "2"])
# solver primal better than our certificate dual for the OSIL scope by more than 1e-6 rel
big = [(x["key"], f"{x['s'] * (x['C'] - x['P']):.3e}") for x in pb if x["s"] * (x["C"] - x["P"]) > D("1e-6") * max(1, abs(x["C"]))]
print("primal beyond certificate by more than MINLPLib 1e-6 rel:", big)
# dual > primal inconsistencies within a run
print("dual on wrong side of own primal:", [x["key"] for x in rows if x["P"] is not None and x["D"] is not None
                                             and x["D"].is_finite() and x["s"] * (x["D"] - x["P"]) > 0])
json.dump([{k: (str(v) if isinstance(v, D) else v) for k, v in x.items()} for x in rows],
          open(HERE / "compare.json", "w"), indent=1)

# --- 4. paper-table deficit column check
tab = {f"{r['instance']}__{r['solver']}": r for r in csv.DictReader(open(SR / "results_table.csv"))}
bad = []
for x in rows:
    t = tab[x["key"]]
    v = t.get("gap_certificate_to_dual", "")
    want = "" if x["deficit"] is None else ("Infinity" if x["deficit"] == INF else x["deficit"])
    if (v in ("", None)) != (want == ""):
        bad.append((x["key"], v, want))
    elif want != "" and (D(v) != want if want != "Infinity" else v != "Infinity"):
        bad.append((x["key"], v, want))
print("table deficit mismatches:", bad)
