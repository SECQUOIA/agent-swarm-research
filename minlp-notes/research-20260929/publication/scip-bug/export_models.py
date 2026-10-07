"""Export the SCIP test models of the waterno2 findings as standalone files.

Each model is first written as a JSON "spec" (exact decimal strings), in the
same variable order, row order and row splitting as period.build, the model
builder used in the original reproductions.  The spec is then written as
  <name>.cip  (SCIP's native format; read by SCIP and by exact_check.py)
  <name>.gms  (GAMS scalar model, for GAMS/SCIP)
Coefficients are the OSIL decimal strings; objective coefficients and
bounds that were floats in period.build are written as repr(float), which
SCIP parses back to the identical double.

Models:
  p0, p4, p5   single-period Lagrangian subproblems of waterno2_06 at the
               multipliers logs/scip_repro_mult.json (wave-2 report, Sec. 5)
  pair2236     cert2 record 2236 (period 3 on one entry/exit cell pair, with
               implied bounds; sepbranch/check_fail.py)
usage: python3 export_models.py
"""
import json
import os
import pickle
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
W2 = os.path.join(HERE, "..", "..", "open-instances-wave2", "waterno2")
sys.path.insert(0, W2)
sys.path.insert(0, os.path.join(W2, "sepbranch"))

import period  # noqa: E402

OUT = os.path.join(HERE, "models")


def dec(a):
    """Canonical plain decimal string (exact; no exponent, leading 0 before '.')."""
    from decimal import Decimal
    return None if a is None else format(Decimal(a), "f")


def isinf(s):
    return s is None or s.upper() in ("INF", "+INF", "-INF")


def spec_from(D, t, objc, box=None, name=""):
    """Same variables, bounds and rows as period.build(D, t, t+1, objc, box)."""
    M, S = D["M"], D["S"]
    vars_ = []
    for v in S["per_vars"][t]:
        lb, ub = M["lb"][v], M["ub"][v]
        lb = None if lb.upper() in ("-INF", "INF") else lb
        ub = None if ub.upper() in ("INF", "+INF") else ub
        for src in (D.get("extra", {}), box or {}):
            if v in src:
                el, eu = src[v]
                # period.build compares floats; keep the exact string when it wins
                lb = repr(float(el)) if lb is None or float(el) > float(lb) else lb
                ub = repr(float(eu)) if ub is None or float(eu) < float(ub) else ub
        vars_.append(dict(name=M["names"][v], type="B" if M["vt"][v] == "B" else "C", lb=dec(lb), ub=dec(ub)))
    rows = []
    for i in S["per_rows"][t]:
        r = M["rows"][i]
        terms = [[dec(a), [M["names"][v] for v in mono]] for mono, a in r["poly"].items()]
        lb, ub = r["lb"], r["ub"]
        lbs = None if lb.upper() == "-INF" else dec(lb)
        ubs = None if ub.upper() in ("INF", "+INF") else dec(ub)
        if lbs is not None and ubs is not None and float(lbs) == float(ubs):
            assert Fraction(lbs) == Fraction(ubs)
            rows.append(dict(name=r["name"], terms=terms, lhs=lbs, rhs=ubs))
        else:
            if lbs is not None:
                rows.append(dict(name=r["name"] + "_lo", terms=terms, lhs=lbs, rhs=None))
            if ubs is not None:
                rows.append(dict(name=r["name"] + "_up", terms=terms, lhs=None, rhs=ubs))
    obj = [[M["names"][v], dec(repr(float(a)))] for v, a in objc.items()]
    return dict(name=name, vars=vars_, rows=rows, obj=obj)


def fmt_term(a, names):
    if not names:
        return a
    return a + "*" + "*".join(f"<{n}>" for n in names)


def write_cip(spec, path):
    """CIP: variables in spec order with type and bounds; rows in spec order;
    linear rows as [linear], others as [nonlinear]."""
    obj = dict(spec["obj"])
    L = ["STATISTICS", f"  Problem name     : {spec['name']}",
         f"  Variables        : {len(spec['vars'])}",
         f"  Constraints      : {len(spec['rows'])}",
         "OBJECTIVE", "  Sense            : minimize", "VARIABLES"]
    for v in spec["vars"]:
        lb = "-inf" if v["lb"] is None else v["lb"]
        ub = "+inf" if v["ub"] is None else v["ub"]
        typ = "binary" if v["type"] == "B" else "continuous"
        L.append(f"  [{typ}] <{v['name']}>: obj={obj.get(v['name'], '0')}, original bounds=[{lb},{ub}]")
    L.append("CONSTRAINTS")
    for r in spec["rows"]:
        lin = all(len(n) == 1 for a, n in r["terms"])
        if lin:
            body =" ".join(("" if a.startswith("-") else "+") + f"{a}<{n[0]}>" for a, n in r["terms"])
            kind = "linear"
        else:
            body = " ".join(("" if a.startswith("-") else "+") + fmt_term(a, n) for a, n in r["terms"])
            kind = "nonlinear"
        if r["lhs"] is not None and r["rhs"] is not None:
            assert r["lhs"] == r["rhs"]
            L.append(f"  [{kind}] <{r['name']}>: {body} == {r['rhs']};")
        elif r["lhs"] is not None:
            L.append(f"  [{kind}] <{r['name']}>: {body} >= {r['lhs']};")
        else:
            L.append(f"  [{kind}] <{r['name']}>: {body} <= {r['rhs']};")
    L.append("END")
    open(path, "w").write("\n".join(L) + "\n")


def gms_num(a):
    return a


def write_gms(spec, path):
    """GAMS scalar model; objective variable 'objvar' defined by equation 'objdef'."""
    L = [f"* {spec['name']}: exported by export_models.py (see README in this folder)"]
    names = [v["name"] for v in spec["vars"]]
    cont = [v["name"] for v in spec["vars"] if v["type"] == "C"]
    bins = [v["name"] for v in spec["vars"] if v["type"] == "B"]
    L.append("Variables objvar;")
    for k in range(0, len(cont), 10):
        L.append("Variables " + ",".join(cont[k:k + 10]) + ";")
    for k in range(0, len(bins), 10):
        L.append("Binary Variables " + ",".join(bins[k:k + 10]) + ";")
    for v in spec["vars"]:
        if v["type"] == "B":
            if v["lb"] is not None and Fraction(v["lb"]) != 0:
                L.append(f"{v['name']}.lo = {v['lb']};")
            if v["ub"] is not None and Fraction(v["ub"]) != 1:
                L.append(f"{v['name']}.up = {v['ub']};")
            continue
        if v["lb"] is not None and v["ub"] is not None and Fraction(v["lb"]) == Fraction(v["ub"]):
            L.append(f"{v['name']}.fx = {v['lb']};")
            continue
        if v["lb"] is not None:
            L.append(f"{v['name']}.lo = {v['lb']};")
        if v["ub"] is not None:
            L.append(f"{v['name']}.up = {v['ub']};")
    eqn = [r["name"] for r in spec["rows"]]
    L.append("Equations objdef;")
    for k in range(0, len(eqn), 10):
        L.append("Equations " + ",".join(eqn[k:k + 10]) + ";")

    def term(a, n):
        f = Fraction(a)
        s = "+" if f >= 0 else "-"
        mag = a.lstrip("+-")
        if not n:
            return f"{s}{mag}"
        cnt = {}
        for x in n:
            cnt[x] = cnt.get(x, 0) + 1
        fac = "*".join(x if k == 1 else f"power({x},{k})" for x, k in cnt.items())
        return f"{s}{mag}*{fac}"
    L.append("objdef.. objvar =e= " + " ".join(term(a, [n]) for n, a in spec["obj"]) + ";")
    for r in spec["rows"]:
        body = " ".join(term(a, n) for a, n in r["terms"])
        if r["lhs"] is not None and r["rhs"] is not None:
            L.append(f"{r['name']}.. {body} =e= {r['rhs']};")
        elif r["lhs"] is not None:
            L.append(f"{r['name']}.. {body} =g= {r['lhs']};")
        else:
            L.append(f"{r['name']}.. {body} =l= {r['rhs']};")
    L.append(f"Model m / all /;")
    L.append("m.optcr = 0; m.optca = 0;")
    L.append("option minlp = scip, threads = 1, reslim = 600;")
    L.append("$if set scipopt m.optfile = 1;")
    L.append("Solve m using minlp minimizing objvar;")
    L.append("display objvar.l, m.objest, m.modelstat, m.solvestat;")
    open(path, "w").write("\n".join(L) + "\n")


def period_specs():
    D = period.setup(6)
    k = json.load(open(os.path.join(W2, "logs", "scip_repro_mult.json")))
    lam = [[float(v) for v in l] for l in k["lam"]]
    mu = float(k["mu"])
    out = {}
    for t in (0, 4, 5):
        objc = period.window_objective(D, t, t + 1, lam, mu)
        out[f"p{t}"] = spec_from(D, t, objc, name=f"waterno2_06_period{t}")
    return out


def pair_spec():
    import tasks
    from dpcells import CellPlan  # noqa: F401
    P = pickle.load(open(os.path.join(W2, "sepbranch", "logs", "cert2.pkl"), "rb"))
    rec = P.crecs[2236]
    cwd = os.getcwd()
    os.chdir(os.path.join(W2, "sepbranch"))
    try:
        tasks.init(P.T, "../logs/implied_06.json", True)
    finally:
        os.chdir(cwd)
    D = tasks._W["D"]
    t = rec["t"]
    box = tasks._box(D, t, rec["cin_box"], rec["cout_box"])
    lam = [[0.0] * 3 for _ in range(P.T - 1)]
    lam[t - 1] = rec["lam_in"]
    lam[t] = rec["lam_out"]
    objc = period.window_objective(D, t, t + 1, lam, 0.0)
    return spec_from(D, t, objc, box=box, name="waterno2_06_period3_cellpair2236"), (D, t, lam, box)


def main():
    os.makedirs(OUT, exist_ok=True)
    specs = period_specs()
    specs["pair2236"], _ = pair_spec()
    for key, spec in specs.items():
        json.dump(spec, open(os.path.join(OUT, f"{key}.json"), "w"), indent=0)
        write_cip(spec, os.path.join(OUT, f"{key}.cip"))
        write_gms(spec, os.path.join(OUT, f"{key}.gms"))
        print(key, len(spec["vars"]), "vars", len(spec["rows"]), "rows", len(spec["obj"]), "obj terms")


if __name__ == "__main__":
    main()
