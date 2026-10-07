"""Structural summary of MINLPLib OSIL instances for the target list.

For each instance: variable types and bounds (unbounded continuous
variables, overall and among nonlinear ones), nonlinear operators, row
counts, the most common nonlinear atom and row signatures (osil.analyze),
dense rows and hub variables, and min-degree width upper bounds of the
factor-incidence graph (as in the treewidth census) before and after
removing
  - hub variables (in >= max(20, 5% of rows) rows; e.g. a global step size), and
  - the 3 densest rows (candidates for Lagrangian relaxation).
Also the number and largest size of connected components of the nonlinear
primal graph after removing hub variables.

Usage: python3 structure.py name [name ...]   (appends to structure.jsonl)
"""
import json, math, os, sys
from collections import Counter

from pathlib import Path
_REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO / "research-20260922/scouting/minlplib-open-data"))
sys.path.insert(0, str(_REPO / "research-20260929/treewidth-census"))
import osil
from census import graphs, factor_incidence, min_degree_width, primal

OSIL_DIR = os.path.expanduser("~/.cache/minlplib/minlplib/osil")
HERE = os.path.dirname(os.path.abspath(__file__))


def ops(t, acc):
    if t[0] in ("num", "var"):
        return
    acc[t[0]] += 1
    for c in t[1:]:
        ops(c, acc)


def components(adj):
    seen, sizes = set(), []
    for v in adj:
        if v in seen:
            continue
        stack, k = [v], 0
        seen.add(v)
        while stack:
            a = stack.pop(); k += 1
            for b in adj[a]:
                if b not in seen:
                    seen.add(b); stack.append(b)
        sizes.append(k)
    return sizes


def width_without(n, rowterms, drop_rows=(), drop_vars=frozenset()):
    rt = []
    for k, (lin, terms) in enumerate(rowterms):
        if k in drop_rows:
            continue
        lin2 = set(lin) - drop_vars
        terms2 = [s - drop_vars for s in terms]
        terms2 = [s for s in terms2 if s]
        if lin2 or terms2:
            rt.append((lin2, terms2))
    return min_degree_width(factor_incidence(n, rt), tmax=60)


def summarize(name):
    I = osil.read(os.path.join(OSIL_DIR, name + ".osil"))
    vt, lb, ub = I["vt"], I["lb"], I["ub"]
    nv = len(vt)
    n, rowvars, nlsets, rowterms = graphs(I)
    nlvars = set().union(*nlsets) if nlsets else set()
    unb = [j for j in range(nv) if vt[j] == "C" and (math.isinf(lb[j]) or math.isinf(ub[j]))]
    fixed = sum(1 for j in range(nv) if lb[j] == ub[j])
    opc = Counter()
    for r, row in I["rows"].items():
        if row["nl"] is not None:
            ops(row["nl"], opc)
    for k in ("sum", "negate", "times"):
        opc.pop(k, None)
    if any(row["quad"] for row in I["rows"].values()):
        opc["quadratic"] += 1
    nlrow_eq = nlrow_in = lin_eq = lin_in = 0
    for r, row in I["rows"].items():
        if r < 0:
            continue
        nl = bool(row["quad"]) or row["nl"] is not None
        eq = row["lb"] == row["ub"]
        if nl:
            nlrow_eq += eq; nlrow_in += not eq
        else:
            lin_eq += eq; lin_in += not eq
    obj = I["rows"][-1]
    objvars = set(obj["lin"]) | {a for a, b, c in obj["quad"]} | {b for a, b, c in obj["quad"]} | \
        (osil.V(obj["nl"]) if obj["nl"] is not None else set())
    # rows as in census order (rows with at least one variable, objective first)
    sizes = [len(s) for s in rowvars]
    dense = sorted(range(len(sizes)), key=lambda k: -sizes[k])[:3]
    deg = Counter(v for s in rowvars for v in s)
    thr = max(20, 0.05 * len(rowvars))
    hubs = frozenset(v for v, d in deg.items() if d >= thr)
    ana = osil.analyze(os.path.join(OSIL_DIR, name + ".osil"))
    rec = dict(
        name=name, nvars=nv, nbin=vt.count("B"), nint=vt.count("I"), ncons=I["ncons"],
        sense=I["sense"], n_nl=len(nlvars), fixed=fixed, unbounded=len(unb),
        unbounded_nl=len(set(unb) & nlvars),
        nl_ops=dict(opc), nlrow_eq=nlrow_eq, nlrow_in=nlrow_in, lin_eq=lin_eq, lin_in=lin_in,
        obj_nvars=len(objvars), obj_nonlinear=bool(obj["quad"]) or obj["nl"] is not None,
        max_row_size=max(sizes), dense_row_sizes=[sizes[k] for k in dense],
        rows_over_20=sum(1 for s in sizes if s > 20),
        hub_vars=len(hubs), hub_max_deg=max(deg.values()),
        tw_fac=width_without(n, rowterms),
        tw_fac_no_hubs=width_without(n, rowterms, drop_vars=hubs) if hubs else None,
        tw_fac_no_dense3=width_without(n, rowterms, drop_rows=set(dense)),
        atoms=ana["atoms"][:8], rowsigs=ana["rowsigs"][:6],
    )
    gn = primal(n, [s - hubs for s in nlsets if len(s - hubs) >= 2])
    comp = components(gn) if gn else []
    rec["nlprimal_components_no_hubs"] = len(comp)
    rec["nlprimal_largest_component_no_hubs"] = max(comp) if comp else 0
    return rec


if __name__ == "__main__":
    with open(os.path.join(HERE, "structure.jsonl"), "a") as f:
        for nm in sys.argv[1:]:
            rec = summarize(nm)
            f.write(json.dumps(rec, default=str) + "\n"); f.flush()
            print(json.dumps({k: rec[k] for k in rec if k not in ("atoms", "rowsigs")}, default=str))
