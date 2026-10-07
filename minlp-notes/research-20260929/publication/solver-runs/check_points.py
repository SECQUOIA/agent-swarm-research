#!/usr/bin/env python3
"""Cheap, sequential, 50-digit checks of selected GDX points; no solves.

Exact binary64 levels are converted to exact decimal strings before numerical
evaluation of the decimal OSIL model. This detects infeasibility; it does not
certify feasibility or repair points.
"""
import json
import re
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / 'bound-audit'))
import audit_eval as ev
from mpmath import mp

SELECTED = ['camshape100__BARON', 'camshape200__BARON', 'camshape400__BARON',
            'camshape800__BARON', 'camshape800__GUROBI', 'camshape100__SCIP',
            'etamac__BARON', 'etamac__GUROBI', 'pricing050__BARON', 'pricing050__SCIP',
            'pindyck__BARON', 'chain50__GUROBI', 'powerflow0039p__GUROBI',
            'kan_r3_h1_n4__SCIP', 'kan_r5_h1_n3__GUROBI',
            'waterno2_09__GUROBI', 'waterno2_12__GUROBI', 'waterno2_24__GUROBI']
out = []
for tag in SELECTED:
    name, solver = tag.split('__')
    raw = subprocess.check_output(['gdxdump', str(HERE / 'runs' / tag / 'm_p.gdx'),
                                   'dFormat=hexponential'], text=True)
    vals = {}
    for name_, body in re.findall(r'^(?:\w+\s+)?Variable (\w+) /(.*?)/;', raw, re.M | re.S):
        level = re.search(r'\bL\s+(\S+)', body)
        vals[name_] = str(Decimal.from_float(float.fromhex(level[1].rstrip(',')))) if level else '0'
    model = ev.load(name)
    assert set(model['names']) <= vals.keys(), (tag, set(model['names']) - vals.keys())
    result = ev.evaluate(model, {n: vals[n] for n in model['names']}, dps=50)
    result['max_viol'] = max(result['row_viol'], result['bound_viol'], result['int_viol'])
    row = {k: mp.nstr(v, 40) if isinstance(v, type(mp.mpf(0))) else v for k, v in result.items()}
    row.update(instance=name, solver=solver, savepoint=f'runs/{tag}/m_p.gdx', dps=50)
    out.append(row)
    print(tag, 'objective', row['obj'], 'max violation', row['max_viol'],
          'row violation', row['row_viol'], row['worst_row'], flush=True)
(HERE / 'point_checks.json').write_text(json.dumps(out, indent=2) + '\n')
