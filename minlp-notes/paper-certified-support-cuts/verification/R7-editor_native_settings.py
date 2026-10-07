"""R7-editor: root bounds of native SCIP with nondefault nonconvex separators on one
path-family instance (built directly from the case triples). Single thread, root only.
Usage: python R7-editor_native_settings.py n seed
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import json, sys
from fractions import Fraction as Fr
from pyscipopt import Model, quicksum
n, seed = int(sys.argv[1]), int(sys.argv[2])
case = json.load(open(f'{_PUBLIC_REPO}/paper-certified-support-cuts/experiments/v3/runs/partC/cases/interleaved_path_n{n}_s{seed}.json'))
tri = case['mechanism']['triples']
def build(settings):
    m = Model(); m.hideOutput()
    m.setParam('parallel/maxnthreads', 1); m.setParam('lp/threads', 1)
    m.setParam('limits/nodes', 1); m.setParam('limits/time', 60)
    ts, ys = [], []
    for i, tr in enumerate(tri):
        a1, a2 = [float(Fr(v)) for v in tr['a']]; c1, c2 = [float(Fr(v)) for v in tr['c']]
        x = m.addVar(f'x{i}', lb=0, ub=1); y = m.addVar(f'y{i}', lb=0, ub=1); z = m.addVar(f'z{i}', lb=0, ub=1)
        t = m.addVar(f't{i}', lb=-10, ub=10)
        D = (y - a1 - (a2 - a1) * x) ** 2 + (y - c1 - (c2 - c1) * z) ** 2 + x * (1 - x) + z * (1 - z)
        m.addCons(D - t <= 0); ts.append(t); ys.append(y)
    m.addCons(quicksum(ys) <= 0.8 * n)
    m.setObjective(quicksum(ts), 'minimize')
    for k, v in settings.items():
        m.setParam(k, v)
    return m
runs = {
    'default': {},
    'eccuts on': {'separating/eccuts/freq': 0},
    'intersection cuts on': {'nlhdlr/quadratic/useintersectioncuts': True},
    'rlt hidden + interminor on': {'separating/rlt/detecthidden': True, 'separating/rlt/hiddenrlt': True, 'separating/interminor/freq': 0},
    'checkvarlocks off (relaxation only)': {'constraints/nonlinear/checkvarlocks': 'd'},
}
print('optimum', case['known_optimum'])
for name, s in runs.items():
    m = build(s); m.optimize()
    print(f'{name:38s} root dual {m.getDualbound():.5f}  time {m.getSolvingTime():.1f}s')
