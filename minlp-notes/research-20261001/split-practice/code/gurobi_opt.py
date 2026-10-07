"""Optimal values of the ternary instances with the Gurobi 13.0.2 command line
(nonconvex MIQP, x in {-1,0,1}^n, plus 1^T x = 0 for TQP-Linear).
Usage: python3 gurobi_opt.py SET OUT.jsonl [timelimit] [name-filter-file]
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exp_points import instance_set, make  # noqa: E402
from miqp_sep import GRB, GRB_ENV  # noqa: E402


def solve(inst, timelimit):
    n, Q, c = inst["n"], inst["Q"], inst["c"]
    with tempfile.TemporaryDirectory() as td:
        lp = os.path.join(td, "m.lp"); log = os.path.join(td, "m.log"); sol = os.path.join(td, "m.sol")
        lin = " ".join(f"{c[i]:+.17g} x{i}" for i in range(n))
        quad = []
        for i in range(n):
            quad.append(f"{2 * Q[i, i]:+.17g} x{i} ^ 2")
            for j in range(i + 1, n):
                if Q[i, j] != 0:
                    quad.append(f"{4 * Q[i, j]:+.17g} x{i} * x{j}")
        with open(lp, "w") as f:
            f.write("Minimize\n obj: " + lin + " + [ " + " ".join(quad) + " ] / 2\nSubject To\n")
            if inst["linear"]:
                f.write(" bal: " + " + ".join(f"x{i}" for i in range(n)) + " = 0\n")
            f.write("Bounds\n" + "".join(f" -1 <= x{i} <= 1\n" for i in range(n)))
            f.write("General\n " + " ".join(f"x{i}" for i in range(n)) + "\nEnd\n")
        t = time.time()
        subprocess.run([GRB, f"TimeLimit={timelimit}", "Threads=1", "MIPGap=1e-6",
                        f"LogFile={log}", "LogToConsole=0", f"ResultFile={sol}", lp],
                       env=GRB_ENV, capture_output=True, text=True)
        dt = time.time() - t
        txt = open(log).read()
        m = re.findall(r"Best objective ([-+0-9.eE]+), best bound ([-+0-9.eE]+), gap ([-+0-9.eE]+|-)%?", txt)
        status = "optimal" if "Optimal solution found" in txt else ("timelimit" if "Time limit" in txt else "other")
        best, bound = (float(m[-1][0]), float(m[-1][1])) if m else (None, None)
    return dict(name=inst["name"], status=status, best=best, bound=bound, time=dt)


if __name__ == "__main__":
    setname, outp = sys.argv[1], sys.argv[2]
    tl = int(sys.argv[3]) if len(sys.argv) > 3 else 600
    specs = instance_set(setname)
    if len(sys.argv) > 4:
        keep = set(open(sys.argv[4]).read().split())
        specs = [s for s in specs if make(s)["name"] in keep]
    done = set()
    if os.path.exists(outp):
        done = {json.loads(l)["name"] for l in open(outp)}
    with open(outp, "a") as f:
        for s in specs:
            inst = make(s)
            if inst["name"] in done:
                continue
            r = solve(inst, tl)
            f.write(json.dumps(r) + "\n"); f.flush()
            print(r, flush=True)
