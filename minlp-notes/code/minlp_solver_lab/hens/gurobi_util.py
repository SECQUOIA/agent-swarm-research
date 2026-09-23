"""Solve a Pyomo MINLP with gurobipy 13 through Pyomo's GurobiMINLPWriter (general nonlinear constraints)."""
import re
import time

import gurobipy as gp
from pyomo.contrib.solver.solvers.gurobi.gurobi_direct_minlp import GurobiMINLPWriter


def solve_gurobi(m, time_limit, threads=4, logfile=None, params=None, load=True):
    """Returns dict with primal, dual, nodes, time, status, root bound (parsed from log)."""
    grb, var_map, pyo_obj, grb_cons, pyo_cons = GurobiMINLPWriter().write(m)
    grb.Params.TimeLimit = time_limit
    grb.Params.Threads = threads
    grb.Params.NonConvex = 2
    grb.Params.MIPGap = 1e-4
    if logfile:
        grb.Params.LogFile = str(logfile)
    grb.Params.OutputFlag = 1 if logfile else 0
    for k, v in (params or {}).items():
        grb.setParam(k, v)
    t0 = time.time()
    grb.optimize()
    t = time.time() - t0
    out = {"status": grb.Status, "time": t, "nodes": grb.NodeCount,
           "primal": grb.ObjVal if grb.SolCount > 0 else float("inf"),
           "dual": grb.ObjBound}
    if logfile:
        out["root_bound"] = parse_root_bound(logfile)
    if load and grb.SolCount > 0:
        for pv, gv in var_map.items():
            pv.set_value(gv.X, skip_validation=True)
    grb.dispose()
    return out


def parse_root_bound(logfile):
    """Root relaxation objective from the Gurobi log ('Root relaxation: objective ...')."""
    txt = open(logfile).read()
    mm = re.findall(r"Root relaxation: objective ([-\d.e+]+)", txt)
    if mm:
        return float(mm[-1])
    return None


def parse_baron_log(txt):
    """Root lower bound (first iteration row) and node count from a BARON log."""
    out = {}
    rows = re.findall(r"^\s*\*?\s*(\d+)\s+(\d+)\s+([\d.]+)\s+([-\d.e+]+)\s+([-\d.e+]+)\s*$", txt, re.M)
    if rows:
        out["root_bound"] = float(rows[0][3])
    mm = re.search(r"Total no\. of BaR iterations:\s*(\d+)", txt)
    if mm:
        out["nodes"] = int(mm.group(1))
    mm = re.search(r"Lower bound after root node\s*:\s*([-\d.e+]+)", txt)
    if mm:
        out["root_bound"] = float(mm.group(1))
    return out
