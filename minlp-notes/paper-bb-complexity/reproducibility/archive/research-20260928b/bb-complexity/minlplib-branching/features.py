"""Structural features of the selected instances; writes results/features.json.

    python3 features.py

Per instance, from the OSiL file (parser: ../../../research-20260922/scouting/minlplib-open-data/osil.py):
- nl_cont: continuous variables in nonlinear terms; nl_cont_unb: those with an infinite bound;
- bilin: distinct bilinear pairs x_i*x_j (i != j) in quadratic or product terms;
- ops: operator names in nonlinear expressions (kinks: abs, min, max);
- quad_only: all nonlinear terms are quadratic coefficients (no nonlinearExpressions).
From the default seed-0 solution (results/sols/INSTANCE.json), if present:
- at_bound: fraction of nl_cont variables at a finite original bound
  (|x - bound| <= 1e-6 * max(1, |bound|)).
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../research-20260922/scouting/minlplib-open-data"))
import osil  # noqa: E402

OSIL_DIR = os.path.expanduser("~/.cache/minlplib/minlplib/osil")


def ops_of(t, acc):
    if t[0] not in ("num", "var"):
        acc.add(t[0])
        for c in t[1:]:
            ops_of(c, acc)
    return acc


def bilinear_pairs(t, acc):
    """Pairs of distinct variables multiplied directly in a product node."""
    if t[0] == "times":
        vs = [c[1] for c in t[1:] if c[0] == "var"]
        if len(vs) >= 2:
            for a in range(len(vs)):
                for b in range(a + 1, len(vs)):
                    if vs[a] != vs[b]:
                        acc.add((min(vs[a], vs[b]), max(vs[a], vs[b])))
    if t[0] not in ("num", "var"):
        for c in t[1:]:
            bilinear_pairs(c, acc)
    return acc


def features(inst):
    ins = osil.read(os.path.join(OSIL_DIR, inst + ".osil"))
    vt, lb, ub = ins["vt"], ins["lb"], ins["ub"]
    nlv, ops, bil = set(), set(), set()
    has_nl = False
    for row in ins["rows"].values():
        for i, j, _c in row["quad"]:
            nlv.update([i, j])
            if i != j:
                bil.add((min(i, j), max(i, j)))
        if row["nl"] is not None:
            has_nl = True
            nlv |= osil.V(row["nl"])
            ops_of(row["nl"], ops)
            bilinear_pairs(row["nl"], bil)
    cont = [v for v in nlv if vt[v] == "C"]
    out = dict(nl_cont=len(cont),
               nl_cont_unb=sum(1 for v in cont if math.isinf(lb[v]) or math.isinf(ub[v])),
               bilin=len(bil), ops=sorted(ops), quad_only=not has_nl,
               kink=bool(ops & {"abs", "min", "max"}))
    solf = os.path.join(HERE, "results/sols", inst + ".json")
    if os.path.exists(solf) and cont:
        sol = json.load(open(solf))
        byname = dict(zip(sol["names"], sol["vals"]))
        names = ins["names"]
        if all(names[v] in byname for v in cont):
            nb = 0
            for v in cont:
                x = byname[names[v]]
                for b in (lb[v], ub[v]):
                    if math.isfinite(b) and abs(x - b) <= 1e-6 * max(1.0, abs(b)):
                        nb += 1
                        break
            out["at_bound"] = nb / len(cont)
    return out


def main():
    sel = [ln.split()[0] for ln in open(os.path.join(HERE, "selected.txt")) if ln.strip()]
    res = {inst: features(inst) for inst in sel}
    with open(os.path.join(HERE, "results/features.json"), "w") as fh:
        json.dump(res, fh, indent=0, sort_keys=True)
    print(f"features for {len(res)} instances")


if __name__ == "__main__":
    main()
