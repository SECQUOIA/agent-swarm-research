"""Pilot: link auxiliary variables of distinct univariate terms of the same variable.
  trig:   s = sin(v), c = cos(v), s^2 + c^2 = 1
  powers: for v >= 0 (or v > 0 when a negative exponent occurs) and exponents p_1..p_m of v found in the
          model: t_k = v^{p_k}, and t_k = t_ref^{p_k/p_ref} with p_ref the exponent of smallest magnitude.
SCIP shares common subexpressions, so the new t_k are the solver's own auxiliary variables.
python link_pilot.py <instance> {native|linked} [tl]"""
import json, math, os, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "univariate_envelopes"))
import pyscipopt as ps
from uenv.osil import read_osil, build_scip


def walk(t, trig, pw):
    op = t[0]
    if op in ("sin", "cos") and t[1][0] == "var":
        trig.setdefault(t[1][1], set()).add(op)
    elif op == "power" and t[1][0] == "var" and t[2][0] == "num":
        pw.setdefault(t[1][1], set()).add(float(t[2][1]))
    elif op == "square" and t[1][0] == "var":
        pw.setdefault(t[1][1], set()).add(2.0)
    elif op == "sqrt" and t[1][0] == "var":
        pw.setdefault(t[1][1], set()).add(0.5)
    elif op == "divide" and t[1][0] == "num" and t[2][0] == "var":
        pw.setdefault(t[2][1], set()).add(-1.0)
    elif op == "times":
        vs = [c[1] for c in t[1:] if c[0] == "var"]
        for v in set(vs):
            if vs.count(v) >= 2:
                pw.setdefault(v, set()).add(float(vs.count(v)))
    if op not in ("num", "var"):
        for c in t[1:]:
            walk(c, trig, pw)


def main():
    name, mode = sys.argv[1], sys.argv[2]
    tl = float(sys.argv[3]) if len(sys.argv) > 3 else 60
    inst = read_osil(os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil"))
    trig, pw = {}, {}
    for r in inst.rows:
        if r["nl"] is not None:
            walk(r["nl"], trig, pw)
        for i, j, c in r["quad"]:
            if i == j:
                pw.setdefault(i, set()).add(2.0)
    trig = [v for v, k in trig.items() if len(k) == 2]
    pw = {v: sorted(p - {1.0, 0.0}) for v, p in pw.items()}
    pw = {v: p for v, p in pw.items() if len(p) >= 2 and inst.var_lb[v] >= 0 and math.isfinite(inst.var_ub[v])
          and (min(p) > 0 or inst.var_lb[v] > 0)}
    m, _h, _st = build_scip(inst, "native")
    xs = {int(v.name[1:]): v for v in m.getVars() if v.name.startswith("v") and v.name[1:].isdigit()}
    nlinks = 0
    if mode == "linked":
        for v in trig:
            s = m.addVar(lb=-1, ub=1); c = m.addVar(lb=-1, ub=1)
            m.addCons(s == ps.sin(xs[v])); m.addCons(c == ps.cos(xs[v])); m.addCons(s * s + c * c == 1)
            nlinks += 1
        for v, ps_ in pw.items():
            lo, hi = inst.var_lb[v], inst.var_ub[v]
            ref = min(ps_, key=abs)
            tv = {}
            for p in ps_:
                a, b = sorted((lo ** p, hi ** p))
                tv[p] = m.addVar(lb=a, ub=b)
                m.addCons(tv[p] == xs[v] ** p)
            for p in ps_:
                if p != ref:
                    m.addCons(tv[p] == tv[ref] ** (p / ref))
                    nlinks += 1
    m.hideOutput(); m.setParam("limits/time", tl); m.setParam("limits/gap", 1e-4)
    t0 = time.time(); m.optimize()
    print(json.dumps({"name": name, "mode": mode, "trig": len(trig), "power_vars": len(pw), "links": nlinks,
                      "sense": inst.obj_sense, "status": m.getStatus(), "primal": m.getObjVal() if m.getNSols() else None,
                      "dual": m.getDualbound(), "nodes": m.getNTotalNodes(), "time": time.time() - t0}))


main()
