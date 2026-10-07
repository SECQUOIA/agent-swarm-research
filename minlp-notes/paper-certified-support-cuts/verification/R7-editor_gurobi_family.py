"""R7-editor: Gurobi (nonconvex MIQCP, one thread) on path-family instances.
Usage: python R7-editor_gurobi_family.py timelimit n:seed [...]
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import json, sys
from fractions import Fraction as Fr
import gurobipy as gp
tl = float(sys.argv[1])
for arg in sys.argv[2:]:
    n, seed = map(int, arg.split(':'))
    case = json.load(open(f'{_PUBLIC_REPO}/paper-certified-support-cuts/experiments/v3/runs/partC/cases/interleaved_path_n{n}_s{seed}.json'))
    env = gp.Env(empty=True); env.setParam('OutputFlag', 0); env.start()
    m = gp.Model(env=env)
    m.Params.Threads = 1; m.Params.TimeLimit = tl; m.Params.MIPGap = 1e-4; m.Params.NonConvex = 2
    ts, ys = [], []
    for tr in case['mechanism']['triples']:
        a1, a2 = [float(Fr(v)) for v in tr['a']]; c1, c2 = [float(Fr(v)) for v in tr['c']]
        x = m.addVar(0, 1); y = m.addVar(0, 1); z = m.addVar(0, 1); t = m.addVar(-10, 10)
        u = y - a1 - (a2 - a1) * x; v = y - c1 - (c2 - c1) * z
        m.addQConstr(u * u + v * v + x - x * x + z - z * z - t <= 0)
        ts.append(t); ys.append(y)
    m.addConstr(gp.quicksum(ys) <= 0.8 * n)
    m.setObjective(gp.quicksum(ts), gp.GRB.MINIMIZE)
    m.optimize()
    print(f'n={n} seed={seed} opt={case["known_optimum"]:.5f} status={m.Status} obj={m.ObjVal:.5f} bound={m.ObjBound:.5f} nodes={m.NodeCount:.0f} time={m.Runtime:.1f}s', flush=True)
