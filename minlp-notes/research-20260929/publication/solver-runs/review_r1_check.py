#!/usr/bin/env python3
"""Recheck review-round-1 evidence from raw artifacts without running solvers."""
import csv
import json
import re
from decimal import Decimal
from pathlib import Path
from statistics import median

HERE = Path(__file__).resolve().parent
REVIEW = HERE.parent / 'reviews/solver-analysis-r1'
logs, meta = {}, {}
for d in sorted((HERE / 'runs').iterdir()):
    if d.is_dir() and '__' in d.name:
        logs[d.name] = (d / 'gams.log').read_text()
        meta[d.name] = json.loads((d / 'run.json').read_text())
globality = sorted(k for k, v in logs.items() if 'Globality is therefore not guaranteed' in v)
assert globality == sorted(f'{n}__BARON' for n in
                          ('catmix100', 'catmix200', 'catmix400', 'catmix800', 'dtoc5', 'optcdeg2'))
tightened = {k: re.findall(r'Changing lower bound for child of (.*?) from (.*?) to (.*?)\.', v)
             for k, v in logs.items() if 'minzerodistance' in v}
assert set(tightened) == {f'{n}__SCIP' for n in
                         ('ex6_2_5', 'ex6_2_7', 'etamac', 'hvycrash', 'lukvle10', 'pindyck')}
assert all(changes and all(Decimal(c[2]) == Decimal('1e-9') for c in changes)
           for changes in tightened.values())
gurobi_warnings = {k: re.findall(r'max constraint violation \(([^)]+)\) exceeds tolerance', v)
                  for k, v in logs.items() if 'exceeds tolerance' in v}
assert gurobi_warnings == {'eg_int_s__GUROBI': ['5.9580e-05']}
capabilities = {k: sorted(set(re.findall(r"Cannot handle function '([^']+)'", v)))
                for k, v in logs.items() if "Cannot handle function '" in v}
assert capabilities['hvycrash__BARON'] == ['cos']
assert not re.search(r'\bsin\s*\(', (HERE / 'gms/hvycrash.gms').read_text())
first = sorted(k for k, v in meta.items() if v['start_utc'] == '2026-10-03T00:56:09Z')
expected = {f'{n}__{s}' for n in ('dtoc5', 'optcdeg2', 'waterno2_24')
            for s in ('BARON', 'GUROBI', 'SCIP')} | {'kan_r3_h1_n9__BARON'}
assert set(first) == expected
assert all(meta[k]['valid'] and meta[k]['end_kind'] == 'completed' for k in first)
long = sorted((v['cpu_over_wall'], k) for k, v in meta.items() if v['wall_s'] > 60)
assert len(long) == 117 and {k for _, k in long[:10]} == expected
assert long[10][0] == 0.9991
end = max(meta[k]['end_utc'] for k in first)
machine = [r for r in csv.DictReader((HERE / 'machine_load.csv').open())
           if '2026-10-03T00:56:09Z' <= r['utc'] <= end]
overruns = {}
for k, log in logs.items():
    if k.endswith('__BARON'):
        lines = (HERE / 'runs' / k / 'trace.trc').read_text().splitlines()
        header = ''.join(l[1:].strip() for l in lines if l.startswith('*')
                         and l[1:].strip() not in ('Trace Record Definition', 'GamsSolve', ''))
        data = [l for l in lines if l.strip() and not l.startswith('*')][-1]
        tr = dict(zip(header.split(','), next(csv.reader([data]))))
        wall = Decimal(tr['SolverTime'])
        if wall > Decimal('3603'):
            cpu = re.findall(r'Total CPU time used:\s*(\S+)', log)[-1]
            overruns[k] = dict(solver_wall_s=str(wall), baron_cpu_s=cpu)
assert set(overruns) == {k for k in first if k.endswith('__BARON')}
assert max(Decimal(r['solver_wall_s']) for r in overruns.values()) == Decimal('3728.4')
tab = {f"{r['instance']}__{r['solver']}": r for r in csv.DictReader((HERE / 'results_table.csv').open())}
review_values = json.loads((REVIEW / 'mine_pd.json').read_text())
assert tab.keys() == review_values.keys()
for k, row in tab.items():
    reviewed = review_values[k]
    for column, original in [('primal', 'P'), ('dual', 'D')]:
        assert (Decimal(row[column]) if row[column] else None) == (
            Decimal(reviewed[original]) if reviewed[original] is not None else None), (k, column)
    assert int(row['model_status']) == int(reviewed['ms'])
    assert int(row['solver_status']) == int(reviewed['ss'])
finite = [r for r in tab.values() if r['dual'] and Decimal(r['dual']).is_finite()]
assert len(finite) == 109
assert sum(r['certificate_scope'] == 'OSIL' for r in finite) == 91
assert sum(Decimal(r['dual_improvement_vs_listed']) > 0 for r in finite
           if r['dual_improvement_vs_listed'] and Decimal(r['dual_improvement_vs_listed']).is_finite()) == 5
anomalies = json.loads((HERE / 'inconsistencies.json').read_text())
assert sum(r['kind'] == 'returned primal beyond certificate' for r in anomalies) == 36
assert sum(r['kind'] == 'log incumbent beyond certificate' for r in anomalies) == 38
assert len({(r['instance'], r['solver']) for r in anomalies}) == 39
water = {}
for n in ('waterno2_09', 'waterno2_12', 'waterno2_24'):
    r = tab[f'{n}__GUROBI']
    water[n] = dict(primal=r['primal'], listed_primal=r['listed_primal'],
                    improvement=str(Decimal(r['listed_primal']) - Decimal(r['primal'])),
                    savepoint_available=(HERE / 'runs' / f'{n}__GUROBI/m_p.gdx').exists())
    assert Decimal(water[n]['improvement']) > 1
evidence = dict(globality_warnings=globality, scip_tightenings=tightened,
                gurobi_warnings=gurobi_warnings, capability_functions=capabilities,
                first_batch=dict(start_utc='2026-10-03T00:56:09Z', end_utc=end, runs=first,
                    cpu_ratio_range=[long[0][0], long[9][0]], other_long_min_ratio=long[10][0],
                    mean_load_range=[min(meta[k]['load1_mean'] for k in first), max(meta[k]['load1_mean'] for k in first)],
                    other_mean_load_median=median(v['load1_mean'] for k, v in meta.items()
                                                 if k not in first and v['wall_s'] > 60),
                    min_mem_available_gb=min(meta[k]['machine_mem_available_min_gb'] for k in first),
                    max_machine_swap_gb=max(meta[k]['machine_swap_used_max_gb'] for k in first),
                    sampled_peak_load=max(float(r['load1']) for r in machine),
                    sampled_peak_own_swap_gb=max(float(r['our_swap_gb']) for r in machine)),
                baron_overruns=overruns, waterno2_primals=water)
(HERE / 'review_r1_evidence.json').write_text(json.dumps(evidence, indent=2) + '\n')
print(json.dumps(evidence, indent=2))
print('PASS: all 129 primal/dual/status rows match independent review; 109 finite values (91 OSIL, 18 R), 5 listed-dual improvements, 36/38 primal flags on 39 pairs')
print('PASS: all six review issues confirmed from existing artifacts; no solver run')
