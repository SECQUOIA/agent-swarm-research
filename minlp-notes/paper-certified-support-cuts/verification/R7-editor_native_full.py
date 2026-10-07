"""R7-editor: full native-SCIP solves of path-family instances with
constraints/nonlinear/checkvarlocks='d' (no implicit-discreteness presolve).
Usage: python R7-editor_native_full.py timelimit n:seed [n:seed ...]
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import sys, importlib.util
spec = importlib.util.spec_from_file_location('ns', (_PUBLIC_REPO + '/paper-certified-support-cuts/verification/R7-editor_native_settings.py'))
tl = float(sys.argv[1])
import json
from fractions import Fraction as Fr
from pyscipopt import Model, quicksum
def build(n, seed, settings):
    case = json.load(open(f'{_PUBLIC_REPO}/paper-certified-support-cuts/experiments/v3/runs/partC/cases/interleaved_path_n{n}_s{seed}.json'))
    m = Model(); m.hideOutput()
    m.setParam('parallel/maxnthreads', 1); m.setParam('lp/threads', 1)
    m.setParam('limits/time', tl); m.setParam('limits/gap', 1e-4)
    ts, ys = [], []
    for i, tr in enumerate(case['mechanism']['triples']):
        a1, a2 = [float(Fr(v)) for v in tr['a']]; c1, c2 = [float(Fr(v)) for v in tr['c']]
        x = m.addVar(lb=0, ub=1); y = m.addVar(lb=0, ub=1); z = m.addVar(lb=0, ub=1); t = m.addVar(lb=-10, ub=10)
        m.addCons((y - a1 - (a2 - a1) * x) ** 2 + (y - c1 - (c2 - c1) * z) ** 2 + x * (1 - x) + z * (1 - z) - t <= 0)
        ts.append(t); ys.append(y)
    m.addCons(quicksum(ys) <= 0.8 * n)
    m.setObjective(quicksum(ts), 'minimize')
    for k, v in settings.items(): m.setParam(k, v)
    return m, case['known_optimum']
for arg in sys.argv[2:]:
    n, seed = map(int, arg.split(':'))
    m, opt = build(n, seed, {'constraints/nonlinear/checkvarlocks': 'd'})
    m.optimize()
    print(f'n={n} seed={seed} opt={opt:.5f} status={m.getStatus()} primal={m.getPrimalbound():.5f} dual={m.getDualbound():.5f} nodes={m.getNNodes()} time={m.getSolvingTime():.1f}s', flush=True)
