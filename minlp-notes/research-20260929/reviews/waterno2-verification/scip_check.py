"""Independent check of the claim that SCIP 10.0.2 reports 'optimal' at wrong
values on period subproblems of waterno2_06 (multipliers logs/scip_repro_mult.json).

The SCIP model is built here from osilx data (vmodel), not with the authors'
period.build.  For each period t in {0, 4, 5}:
  1. solve with the cheaper pump configuration fixed (feastol 1e-9) -> point x*;
  2. evaluate x* exactly (Fraction) on the period rows and bounds;
  3. ask SCIP's own checker (checkSol, original problem) whether x* is feasible;
  4. full solves under many settings; flag 'WRONG' when SCIP claims optimal with
     a dual bound above value(x*) + 1e-4.
usage: python3 scip_check.py [periods] [settings-group]
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import json
import sys
import time
from fractions import Fraction as F

import pyscipopt as ps

import veval
import vmodel

W2 = _RESEARCH + "/open-instances-wave2/waterno2/"
T = 6
I = vmodel.instance(T)
m = I["m"]
import os
K = json.load(open(os.environ.get("WV_MULT", W2 + "logs/scip_repro_mult.json")))
LAM = [[float(v) for v in l] for l in K["lam"]]
MU = float(K["mu"])
CHEAP = {0: [0] * 9, 4: [1, 1, 0, 0, 0, 0, 0, 0, 0], 5: [1, 0, 0, 0, 0, 0, 0, 0, 0]}


def build(t, params=None, emphasis=None, presolve_off=False, heur_off=False):
    M = ps.Model()
    M.hideOutput()
    M.setParam("parallel/maxnthreads", 1)
    M.setParam("lp/threads", 1)
    if emphasis is not None:
        M.setEmphasis(emphasis)
    if presolve_off:
        M.setPresolve(ps.SCIP_PARAMSETTING.OFF)
    if heur_off:
        M.setHeuristics(ps.SCIP_PARAMSETTING.OFF)
    for k, v in (params or {}).items():
        M.setParam(k, v)
    X = {}
    for v in I["per_vars"][t]:
        lb = None if m["lb"][v].upper() == "-INF" else float(F(m["lb"][v]))
        ub = None if m["ub"][v].upper() in ("INF", "+INF") else float(F(m["ub"][v]))
        X[v] = M.addVar(name=m["names"][v], vtype="B" if m["vt"][v] == "B" else "C", lb=lb, ub=ub)
    for i in I["per_rows"][t]:
        c = m["cons"][i]
        e = 0
        for mono, a in vmodel.poly(c).items():
            if len(mono) == 1:
                term = X[mono[0]]
            elif len(set(mono)) == 1:
                term = X[mono[0]] ** len(mono)
            else:
                term = X[mono[0]] * X[mono[1]]
            e = e + float(a) * term
        lb = None if c["lb"].upper() == "-INF" else float(F(c["lb"]))
        ub = None if c["ub"].upper() in ("INF", "+INF") else float(F(c["ub"]))
        if lb is not None and ub is not None and lb == ub:
            M.addCons(e == lb, name=c["name"])
        else:
            if lb is not None:
                M.addCons(e >= lb, name=c["name"] + "_lo")
            if ub is not None:
                M.addCons(e <= ub, name=c["name"] + "_up")
    obj = vmodel.period_objective(I, t, LAM, MU)
    M.setObjective(ps.quicksum(float(a) * X[v] for v, a in obj.items()), "minimize")
    return M, X, obj


def bins(t):
    return [v for v in I["per_vars"][t] if m["vt"][v] == "B"]


def config(M, X, t):
    s = M.getBestSol()
    return [int(round(M.getSolVal(s, X[v]))) for v in bins(t)]


def cheap_point(t):
    M, X, obj = build(t, {"numerics/feastol": 1e-9, "limits/time": 300})
    for v, b in zip(bins(t), CHEAP[t]):
        M.fixVar(X[v], b)
    M.optimize()
    s = M.getBestSol()
    x = {v: M.getSolVal(s, X[v]) for v in X}
    st, pb, db = M.getStatus(), M.getPrimalbound(), M.getDualbound()
    M.freeProb()
    return x, st, pb, db


def exact_eval(t, x, obj):
    xf = [F(0)] * len(m["names"])
    for v, val in x.items():
        xf[v] = F(val)
    e = veval.evaluate(m, xf, rows=I["per_rows"][t], vars_=I["per_vars"][t])
    e["lagr"] = sum(a * xf[v] for v, a in obj.items())
    return e


def scip_check(t, x):
    M, X, obj = build(t)
    s = M.createSol()
    for v, val in x.items():
        M.setSolVal(s, X[v], val)
    ok = M.checkSol(s, printreason=False, completely=True, checkbounds=True, checkintegrality=True,
                    checklprows=True, original=True)
    M.freeProb()
    return ok


EMPH = ps.SCIP_PARAMEMPHASIS
SETTINGS = {
    "default": {},
    "feastol1e-9": dict(params={"numerics/feastol": 1e-9}),
    "feastol1e-9+dualfeastol1e-9": dict(params={"numerics/feastol": 1e-9, "numerics/dualfeastol": 1e-9}),
    "emph_numerics": dict(emphasis=EMPH.NUMERICS),
    "emph_numerics+feastol1e-9": dict(emphasis=EMPH.NUMERICS, params={"numerics/feastol": 1e-9}),
    "presolve_off": dict(presolve_off=True),
    "noprop": dict(params={"propagating/maxrounds": 0, "propagating/maxroundsroot": 0}),
    "sepa_off": dict(params={"separating/maxrounds": 0, "separating/maxroundsroot": 0}),
    "heur_off": dict(heur_off=True),
}
PROPS = ["dualfix", "genvbounds", "nlobbt", "obbt", "probing", "pseudoobj", "redcost", "rootredcost",
         "symmetry", "vbounds"]
for p in PROPS:
    SETTINGS["no_" + p] = dict(params={f"propagating/{p}/freq": -1})
SETTINGS["nonlinear_noprop"] = dict(params={"constraints/nonlinear/maxproprounds": 0})
SETTINGS["no_reduce_dual"] = dict(params={"misc/allowstrongdualreds": False, "misc/allowweakdualreds": False})
SETTINGS["no_symmetry"] = dict(params={"misc/usesymmetry": 0})
SETTINGS["no_conflict"] = dict(params={"conflict/enable": False})


def run_setting(t, name, cfg, vstar, tl=300):
    kw = dict(cfg)
    M, X, obj = build(t, dict(kw.get("params", {}), **{"limits/time": tl}), kw.get("emphasis"),
                      kw.get("presolve_off", False), kw.get("heur_off", False))
    tic = time.time()
    M.optimize()
    st, db = M.getStatus(), M.getDualbound()
    pb = M.getPrimalbound() if M.getNSols() else float("inf")
    conf = config(M, X, t) if M.getNSols() else None
    flag = "WRONG" if (st == "optimal" and db > vstar + 1e-4) else "ok"
    print(f"period {t} {name:28s} {st:9s} dual {db:.6f} primal {pb:.6f} config {conf} "
          f"nodes {M.getNNodes()} {time.time()-tic:.1f}s  {flag}", flush=True)
    M.freeProb()
    return flag


def main():
    periods = [int(a) for a in sys.argv[1].split(",")] if len(sys.argv) > 1 else [0, 4, 5]
    group = sys.argv[2] if len(sys.argv) > 2 else "all"
    print("SCIP version", ps.Model().version(), "PySCIPOpt", ps.__version__, flush=True)
    for t in periods:
        x, st, pb, db = cheap_point(t)
        obj = vmodel.period_objective(I, t, LAM, MU)
        e = exact_eval(t, x, obj)
        ok = scip_check(t, x)
        print(f"period {t}: cheaper configuration {CHEAP[t]} fixed, feastol 1e-9: {st} primal {pb:.9f} dual {db:.9f}")
        print(f"   exact: Lagrangian value {float(e['lagr']):.9f}, max row violation {float(e['maxrow']):.3e} ({e['row']}),"
              f" max bound violation {float(e['maxbnd']):.3e} ({e['bvar']}), binaries integral {e['int_ok']}")
        print(f"   SCIP checkSol (default tolerances, original problem): feasible = {ok}", flush=True)
        json.dump({m["names"][v]: repr(val) for v, val in x.items()}, open(f"logs/cheap_point_p{t}.json", "w"))
        vstar = float(e["lagr"])
        names = list(SETTINGS) if group == "all" else group.split(",")
        for name in names:
            run_setting(t, name, SETTINGS[name], vstar)


if __name__ == "__main__":
    main()
