"""Solve a model file with PySCIPOpt under named settings and print the result.

usage: python3 run_scip.py MODEL [SETTING ...]
A SETTING is a name from SETTINGS below or 'param=value' pairs joined by ','
(for example randomization/randomseedshift=7,numerics/feastol=1e-8).
Prints one line per setting: status, claimed optimum (dual bound), primal
value, nodes, time.  With WRITE_SOL=dir the best solution is written there.
"""
import os
import sys
import time

import pyscipopt as ps

SETTINGS = {
    "default": {},
    "noprop": {"propagating/maxrounds": 0, "propagating/maxroundsroot": 0},
    "noobbt": {"propagating/obbt/freq": -1},
    "seed7": {"randomization/randomseedshift": 7},
    "feastol1e-8": {"numerics/feastol": 1e-8},
    "noobbt_seed7_feastol1e-8": {"propagating/obbt/freq": -1, "randomization/randomseedshift": 7,
                                 "numerics/feastol": 1e-8},
}


def parse(s):
    if s in SETTINGS:
        return SETTINGS[s]
    out = {}
    for kv in s.split(","):
        if not kv:
            continue
        k, v = kv.split("=")
        for conv in (int, float):
            try:
                v = conv(v)
                break
            except ValueError:
                pass
        if v in ("TRUE", "FALSE", "True", "False"):
            v = v in ("TRUE", "True")
        out[k] = v
    return out


def solve(path, prm, timelimit=600.0, quiet=True, debugsol=None):
    m = ps.Model()
    if quiet:
        m.hideOutput()
    m.readProblem(path)
    m.setParam("limits/time", timelimit)
    for k, v in prm.items():
        m.setParam(k, v)
    tic = time.time()
    m.optimize()
    el = time.time() - tic
    res = dict(status=m.getStatus(), dual=m.getDualbound(),
               primal=m.getPrimalbound() if m.getNSols() > 0 else float("inf"),
               nodes=m.getNNodes(), time=el)
    if os.environ.get("WRITE_SOL") and m.getNSols() > 0:
        d = os.environ["WRITE_SOL"]
        os.makedirs(d, exist_ok=True)
        m.writeBestSol(os.path.join(d, os.path.basename(path) + "." + str(abs(hash(str(prm)))) + ".sol"))
    m.freeProb()
    return res


def main():
    path = sys.argv[1]
    names = sys.argv[2:] or ["default"]
    print("# pyscipopt", ps.__version__, flush=True)
    ps.Model().printVersion()
    sys.stdout.flush()
    for s in names:
        r = solve(path, parse(s))
        print(f"{os.path.basename(path)} {s:30s} status {r['status']:9s} claimed optimum {r['dual']:.6f} "
              f"primal {r['primal']:.6f} nodes {r['nodes']} time {r['time']:.1f}s", flush=True)


if __name__ == "__main__":
    main()
