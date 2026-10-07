"""One SCIP run: python3 run_one.py INSTANCE SETTING EPS [--trans FILE].

Prints one compact JSON line on the real stdout. C-level output of SCIP and
SoPlex goes to a temporary file; lines "Cannot set ... tolerance" (SoPlex
refusing LP tolerances below 1e-10) are counted and reported.
"""
import ctypes
import json
import os
import re
import sys
import tempfile
import time

import pyscipopt
from pyscipopt import SCIP_PARAMSETTING

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from instances import INSTANCES, cip_text, f_eval, cons_violation  # noqa: E402

TIME_LIMIT = 120.0
NODE_LIMIT = 100000

# Applied to every run: absolute gap = eps, no relative gap, tight feasibility.
BASE = {
    "limits/gap": 0.0,
    "limits/time": TIME_LIMIT,
    "limits/nodes": NODE_LIMIT,
    "numerics/feastol": 1e-9,
    "numerics/epsilon": 1e-12,
    "numerics/sumepsilon": 1e-10,
    "numerics/dualfeastol": 1e-9,
    "display/verblevel": 0,
    "randomization/randomseedshift": 0,
}

PROP_OFF = {"propagating/%s/freq" % p: -1 for p in
            ["dualfix", "genvbounds", "nlobbt", "obbt", "probing", "pseudoobj",
             "redcost", "rootredcost", "symmetry", "vbounds"]}
PROP_OFF.update({"constraints/nonlinear/propfreq": -1, "constraints/linear/propfreq": -1,
                 "constraints/varbound/propfreq": -1})
CUTOFF_OFF = {"propagating/pseudoobj/freq": -1, "propagating/rootredcost/freq": -1,
              "propagating/redcost/freq": -1, "propagating/genvbounds/freq": -1}
BISECT = {"branching/midpull": 1.0, "branching/midpullreldomtrig": 0.0}
WIDEST = {"constraints/nonlinear/branching/domainweight": 1.0,
          "constraints/nonlinear/branching/violweight": 0.0,
          "constraints/nonlinear/branching/dualweight": 0.0,
          "constraints/nonlinear/branching/pscostweight": 0.0,
          "constraints/nonlinear/branching/vartypeweight": 0.0}
BFS = {"nodeselection/bfs/stdpriority": 1000000, "nodeselection/bfs/maxplungedepth": 0,
       "nodeselection/bfs/minplungedepth": 0}

# name -> (params, flags). Flags: presolve_off, heur_off, known_opt.
SETTINGS = {
    "default": ({}, set()),
    "nopresolve": ({}, {"presolve_off"}),
    "noprop": (PROP_OFF, set()),
    "nocutoffprop": (CUTOFF_OFF, set()),
    "obbtoff": ({"propagating/obbt/freq": -1}, set()),
    "obbtall": ({"propagating/obbt/freq": 1}, set()),
    "lppoint": ({"branching/midpull": 0.0}, set()),
    "midpoint": (BISECT, set()),
    "widestbisect": ({**BISECT, **WIDEST}, set()),
    # closest to the theory's model: incumbent f* from the start, prune by
    # bound only, best-first order (processed nodes = nodes with LB < f*-eps)
    "model": (BFS, {"heur_off", "known_opt"}),
    "modelnoprop": ({**BFS, **PROP_OFF}, {"heur_off", "known_opt"}),
    "toy": ({**BFS, **PROP_OFF, **BISECT, **WIDEST}, {"heur_off", "known_opt", "presolve_off"}),
    # targeted switches
    "noexpand": ({"expr/pow/expandmaxexponent": 1}, set()),
    "withlocks": ({"constraints/nonlinear/checkvarlocks": "t"}, set()),
    # removes every use of the objective cutoff for domain reductions,
    # including pseudoobj presolving (propagating/pseudoobj/freq=-1 does not)
    "noweakdual": ({"misc/allowweakdualreds": False}, set()),
    # branch only on x1 while x1 is a candidate (branching priority)
    # smaller minimal relative bound improvement accepted by propagation
    "smallstreps": ({"numerics/boundstreps": 1e-6}, set()),
    "nonlprop": ({"constraints/nonlinear/propfreq": -1}, set()),
    "xprio": ({}, {"xprio"}),
    "xpriomidpoint": (BISECT, {"xprio"}),
    "xpriolppoint": ({"branching/midpull": 0.0}, {"xprio"}),
    "xpriotoy": ({**BFS, **PROP_OFF, **BISECT, **WIDEST},
                 {"heur_off", "known_opt", "presolve_off", "xprio"}),
    # candidates passed to SCIP's generic branching rules, which honour priorities
    "exttoy": ({**BFS, **PROP_OFF, **BISECT, "constraints/nonlinear/branching/external": True},
               {"heur_off", "known_opt", "presolve_off"}),
    "xprioexttoy": ({**BFS, **PROP_OFF, **BISECT, "constraints/nonlinear/branching/external": True},
                    {"heur_off", "known_opt", "presolve_off", "xprio"}),
    "nosym": ({"misc/usesymmetry": 0}, set()),
}


def _i(tok):
    try:
        return int(tok)
    except ValueError:
        return 0


def parse_stats(txt):
    out = {}
    sec = None
    for line in txt.splitlines():
        m = re.match(r"^(\S[^:]*?)\s*:", line)
        if m and not line.startswith(" "):
            sec = m.group(1).strip()
            continue
        if sec == "Constraints" and line.strip().startswith("nonlinear"):
            f = line.split(":")[1].split()
            out["nl_prop_calls"], out["nl_cutoffs"], out["nl_domreds"] = _i(f[1]), _i(f[8]), _i(f[9])
            out["nl_cuts"], out["nl_children"] = _i(f[10]), _i(f[13])
        elif sec == "Propagators" and ":" in line:
            name, rest = line.split(":")
            f = rest.split()
            if len(f) == 4 and _i(f[3]) + _i(f[2]) > 0:
                out[f"prop_{name.strip()}_domreds"] = _i(f[3])
                out[f"prop_{name.strip()}_cutoffs"] = _i(f[2])
        elif sec == "Nlhdlrs" and ":" in line:
            name, rest = line.split(":")
            f = rest.split()
            if _i(f[0]) > 0:
                out[f"nlhdlr_{name.strip()}"] = dict(detects=_i(f[0]), domreds=_i(f[7]),
                                                     cutoffs=_i(f[8]), cuts=_i(f[11]))
        elif sec == "B&B Tree":
            m2 = re.match(r"\s+nodes left\s*:\s*(\d+)", line)
            if m2:
                out["nodes_left"] = int(m2.group(1))
            m2 = re.match(r"\s+nodes \(total\)\s*:\s*(\d+) \((\d+) internal, (\d+) leaves\)", line)
            if m2:
                out["internal"], out["leaves_processed"] = int(m2.group(2)), int(m2.group(3))
            m2 = re.match(r"\s+number of runs\s*:\s*(\d+)", line)
            if m2:
                out["nruns"] = int(m2.group(1))
            m2 = re.match(r"\s+max depth \(total\)\s*:\s*(\d+)", line)
            if m2:
                out["max_depth"] = int(m2.group(1))
            for key in ("feasible leaves", "infeas. leaves", "objective leaves"):
                m2 = re.match(r"\s+%s\s*:\s*(\d+)" % re.escape(key), line)
                if m2:
                    out[key.replace(" ", "_").replace(".", "")] = int(m2.group(1))
        elif sec == "Root Node":
            m2 = re.match(r"\s+Final Dual Bound\s*:\s*(\S+)", line)
            if m2 and m2.group(1) != "-":
                out["root_dual"] = float(m2.group(1))
        elif sec == "Solution":
            m2 = re.match(r"\s+Primal Bound\s*:.*found by <(\w+)>", line)
            if m2:
                out["best_sol_by"] = m2.group(1)
        elif sec == "Primal Heuristics" and ":" in line:
            name, rest = line.split(":")
            f = rest.split()
            if len(f) == 5 and name.strip() in ("LP solutions", "relax solutions", "pseudo solutions"):
                out[f"sols_{name.strip().split()[0]}"] = _i(f[3])
    return out


def run(iname, sname, eps, trans_file=None):
    d = INSTANCES[iname]
    params, flags = SETTINGS[sname]
    tmpdir = tempfile.mkdtemp(prefix="scipnx_")
    cip = os.path.join(tmpdir, iname + ".cip")
    with open(cip, "w") as fh:
        fh.write(cip_text(d))
    capture = os.path.join(tmpdir, "stdout.txt")
    saved, saved2 = os.dup(1), os.dup(2)
    fd = os.open(capture, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    os.dup2(fd, 1)
    os.dup2(fd, 2)
    try:
        m = pyscipopt.Model()
        m.readProblem(cip)
        for k, v in {**BASE, **d["params"], **params, "limits/absgap": eps}.items():
            m.setParam(k, v)
        if "presolve_off" in flags:
            m.setPresolve(SCIP_PARAMSETTING.OFF)
        if "heur_off" in flags:
            m.setHeuristics(SCIP_PARAMSETTING.OFF)
        if "xprio" in flags:
            m.chgVarBranchPriority({v.name: v for v in m.getVars()}["x1"], 10)
        if "known_opt" in flags:
            vs = {v.name: v for v in m.getVars()}
            sol = m.createSol()
            for i, x in enumerate(d["xstar"]):
                m.setSolVal(sol, vs[f"x{i + 1}"], x)
            tval = float(f_eval(d, d["xstar"])) + 1e-15
            m.setSolVal(sol, vs["t"], tval)
            accepted = m.addSol(sol, free=True)
        else:
            accepted = None
        if trans_file:
            m.presolve()
            m.writeProblem(trans_file, trans=True)
        t0 = time.time()
        m.optimize()
        wall = time.time() - t0
        statsf = os.path.join(tmpdir, "stats.txt")
        m.writeStatistics(statsf)
        with open(statsf) as fh:
            stats = parse_stats(fh.read())
        res = dict(inst=iname, setting=sname, eps=eps, status=m.getStatus(),
                   nodes=m.getNNodes(), totalnodes=m.getNTotalNodes(),
                   lpiters=m.getNLPIterations(), time=round(m.getSolvingTime(), 3),
                   wall=round(wall, 3), primal=m.getPrimalbound(), dual=m.getDualbound(),
                   fstar=d["fstar"], knownopt_accepted=accepted)
        res["primal_minus_fstar"] = res["primal"] - d["fstar"]
        res["dual_minus_fstar"] = res["dual"] - d["fstar"]
        if m.getNSols() > 0:
            best = m.getBestSol()
            byname = {v.name: v for v in m.getVars()}
            x = [m.getSolVal(best, byname[f"x{i + 1}"]) for i in range(d["n"])]
            res["sol_true_f_minus_fstar"] = float(f_eval(d, x) - d["fstar"])
            res["sol_cons_viol"] = float(cons_violation(d, x))
        res.update(stats)
    finally:
        sys.stdout.flush()
        sys.stderr.flush()
        ctypes.CDLL(None).fflush(None)
        os.dup2(saved, 1)
        os.dup2(saved2, 2)
        os.close(fd)
    with open(capture, errors="replace") as fh:
        txt = fh.read()
    res["soplex_tol_warnings"] = txt.count("Cannot set")
    other = [ln for ln in txt.splitlines() if ln.strip() and "Cannot set" not in ln
             and not ln.startswith("wrote problem")]
    if other:
        res["other_output"] = other[:5]
    for fn in os.listdir(tmpdir):
        os.remove(os.path.join(tmpdir, fn))
    os.rmdir(tmpdir)
    print(json.dumps(res, separators=(",", ":")), flush=True)


if __name__ == "__main__":
    tf = None
    if "--trans" in sys.argv:
        tf = sys.argv[sys.argv.index("--trans") + 1]
    run(sys.argv[1], sys.argv[2], float(sys.argv[3]), tf)
