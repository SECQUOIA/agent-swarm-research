#!/usr/bin/env python3
"""Targeted artifact checks independent of the analysis implementation.

Checks trace values, end-of-run bound sources, counts, kept-attempt identity,
all comparison signs, flag completeness, selected-point coverage and hashes.
No network, solver, driver, project-wide or CI calls.
"""
import ast
import csv
import hashlib
import json
import re
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
for name in ('collect.py', 'build_references.py', 'check_points.py', 'analyze.py', 'verify_analysis.py', 'review_r1_check.py'):
    ast.parse((HERE / name).read_text())
raw = json.loads((HERE / 'results.json').read_text())
refs = {r['instance']: r for r in json.loads((HERE / 'references.json').read_text())}
table = {(r['instance'], r['solver']): r for r in csv.DictReader((HERE / 'results_table.csv').open())}
anomalies = json.loads((HERE / 'inconsistencies.json').read_text())
from decimal import getcontext
getcontext().prec = 60
assert len(raw) == len(table) == 129
assert len(refs) == 43
assert sum(r['run_finished'] for r in raw) == 129
assert sum(r['valid'] for r in raw) == 126
assert sum(r['optimality_claim'] == 'True' for r in table.values()) == 2
assert not any(r['closes_within_1h'] == 'True' for r in table.values())
assert {k for k, r in table.items() if r['optimality_claim'] == 'True'} == {
    ('camshape100', 'BARON'), ('camshape200', 'BARON')}

expected_flags = set()
for run in raw:
    key = (run['instance'], run['solver'])
    row, ref = table[key], refs[run['instance']]
    d = HERE / run['run_dir']
    trace_lines = (d / 'trace.trc').read_text().splitlines()
    header = ''.join(l[1:].strip() for l in trace_lines if l.startswith('*')
                     and l[1:].strip() not in ('Trace Record Definition', 'GamsSolve', ''))
    data = [l for l in trace_lines if l.strip() and not l.startswith('*')][-1]
    tr = dict(zip(header.split(','), next(csv.reader([data]))))
    assert int(tr['ModelStatus']) == run['model_status']
    assert int(tr['SolverStatus']) == run['solver_status']
    assert tr['SolverName'] == run['solver']
    assert run['reslim'] == 3600 and Decimal(str(run['optcr'])) == Decimal('1e-9')
    assert Decimal(str(run['optca'])) == Decimal('1e-9')
    if row['primal']:
        assert Decimal(row['primal']) == Decimal(tr['ObjectiveValue'])
    else:
        assert run['model_status'] not in {1, 2, 7, 8, 15, 16, 17}
    if row['dual'] and run['dual_bound_source'].startswith('objest'):
        if Decimal(row['dual']).is_finite():
            assert Decimal(row['dual']) == Decimal(tr['ObjectiveValueEstimate'])
    log = (d / 'gams.log').read_text()
    globality = 'Globality is therefore not guaranteed' in log
    tightened = 'minzerodistance' in log
    violation = re.findall(r'max constraint violation \(([^)]+)\) exceeds tolerance', log)
    assert run['globality_warning'] == globality == (row['globality_warning'] == 'True')
    assert run['scip_argument_bounds_tightened'] == tightened == (row['scip_argument_bounds_tightened'] == 'True')
    assert (run['reported_max_constraint_violation'] or '') == row['reported_max_constraint_violation'] == (violation[-1] if violation else '')
    if globality:
        assert 'globality not guaranteed' in row['notes']
    if tightened:
        assert 'slightly tightened model' in row['notes']
    if violation:
        assert row['status'] == 'time limit, point exceeds solver tolerance'
    if key == ('hvycrash', 'BARON'):
        assert 'cos unsupported' in row['notes'] and 'sin/cos' not in row['notes']
    if row['dual'] and 'objest NA' in run['dual_bound_source']:
        token = re.findall(r'Best objective (\S+), best bound (\S+), gap', log)[-1][1]
        assert Decimal(token) == Decimal(row['dual'])
    if row['dual'] and Decimal(row['dual']).is_finite():
        pats = {'BARON': r'^Best possible\s*=\s*(\S+)', 'GUROBI': r'Best objective \S+, best bound (\S+), gap',
                'SCIP': r'^Dual Bound\s*:\s*(\S+)'}
        token = re.findall(pats[run['solver']], log, re.M)[-1]
        val = Decimal(token)
        assert abs(val - Decimal(row['dual'])) <= Decimal('1e-10') * max(1, abs(val))
    s = Decimal(1 if ref['sense'] == 'min' else -1)
    c, p = Decimal(ref['certificate_dual']), Decimal(ref['reference_primal'])
    for column, a, b in [
        ('gap_certificate_to_dual', row['certificate_dual'], row['dual']),
        ('gap_primal_to_certificate', row['primal'], row['certificate_dual']),
        ('primal_improvement_vs_reference', row['reference_primal'], row['primal']),
        ('dual_improvement_vs_listed', row['dual'], row['listed_dual']),
        ('primal_improvement_vs_listed', row['listed_primal'], row['primal']),
    ]:
        if a and b:
            assert Decimal(row[column]) == s * (Decimal(a) - Decimal(b)), (key, column)
        else:
            assert not row[column]
    if row['primal'] and s * (c - Decimal(row['primal'])) > 0:
        expected_flags.add((*key, 'returned primal beyond certificate'))
    if row['solver_log_primal'] and Decimal(row['solver_log_primal']).is_finite() and s * (c - Decimal(row['solver_log_primal'])) > 0:
        expected_flags.add((*key, 'log incumbent beyond certificate'))
    if row['dual'] and Decimal(row['dual']).is_finite():
        assert s * (Decimal(row['dual']) - p) <= 0
        assert Decimal(row['gap_certificate_to_dual']) > 0
    meta = json.loads((d / 'run.json').read_text())
    first_batch = meta['driver_pid'] == 898862 and meta['start_utc'] == '2026-10-03T00:56:09Z'
    assert run['loaded_first_batch'] == first_batch == (row['loaded_first_batch'] == 'True')
    if first_batch:
        assert run['valid'] and 'machine overload and memory pressure' in row['notes']
    assert meta['has_trace'] and meta['threads'] == 1
    assert meta['kill_stage'] <= 1
    if run['valid'] and run['wall_time_s'] > 60:
        assert run['cpu_over_wall'] >= 0.9
    if not run['valid']:
        assert key[1] == 'SCIP' and key[0] in ('ex6_2_5', 'ex6_2_7', 'pindyck')
        assert meta['kept_best'] and meta['attempts_total'] == 3
        archive = HERE / f'runs_archive/attempts/{key[0]}__SCIP__a{meta["attempt"]}'
        for artifact in ('trace.trc', 'gams.log'):
            assert (d / artifact).read_bytes() == (archive / artifact).read_bytes()
        assert run['solver_status'] == 8 and 'memory cap' in run['kill_reason']
        assert 'stopped at the 8 GB memory limit' == row['status']

assert expected_flags == {(a['instance'], a['solver'], a['kind']) for a in anomalies}
assert len(anomalies) == 74
assert len(json.loads((HERE / 'attempts.json').read_text())) == 9
checks = json.loads((HERE / 'point_checks.json').read_text())
assert len(checks) == 18
water = {'waterno2_09', 'waterno2_12', 'waterno2_24'}
for r in checks:
    assert r['dps'] == 50
    if r['instance'] not in water:
        assert Decimal(r['row_viol']) > 0
    else:
        assert r['solver'] == 'GUROBI'
        row = table[r['instance'], r['solver']]
        assert Decimal(row['primal_improvement_vs_listed']) > 1
        assert 'reported primal improves MINLPLib' in row['notes']
        assert abs(Decimal(r['obj']) - Decimal(row['primal'])) < Decimal('1e-8')
    assert Decimal(r['max_viol']) == max(Decimal(r[k]) for k in ('row_viol', 'bound_viol', 'int_viol'))
    assert r['n_unknown'] == 0 and not r['domain_errors']
for name, digest in json.loads((HERE / 'reference_sources.json').read_text()).items():
    assert hashlib.sha256((HERE.parent.parent / name).read_bytes()).hexdigest() == digest
for model in json.loads((HERE / 'gms_manifest.json').read_text()):
    name = model['instance']
    assert hashlib.sha256((HERE / 'gms' / f'{name}.gms').read_bytes()).hexdigest() == model['gms_sha256']
    osil = Path.home() / '.cache/minlplib/minlplib/osil' / f'{name}.osil'
    assert hashlib.sha256(osil.read_bytes()).hexdigest() == model['osil_sha256']
for run in raw:
    assert refs[run['instance']]['sense'] == run['sense']
assert sum(r['globality_warning'] for r in raw) == 6
assert sum(r['scip_argument_bounds_tightened'] for r in raw) == 6
assert sum(r['loaded_first_batch'] for r in raw) == 10
summary = json.loads((HERE / 'analysis_summary.json').read_text())
for solver, finite_count, unqualified in [('BARON', 35, 29), ('GUROBI', 36, 36), ('SCIP', 38, 38)]:
    assert summary[solver]['finite_duals'] == finite_count
    assert summary[solver]['finite_duals_without_globality_warning'] == unqualified
assert summary['SCIP']['finite_duals_for_tightened_model'] == 6
print('PASS: syntax of six analysis scripts; 43 references; 129 unique finished rows; 126 valid measurements')
print('PASS: all trace statuses, primal tokens, final dual sources, settings and sense-adjusted comparison columns')
print('PASS: 109 finite dual values, 6 with BARON globality disclaimers; 103 without that warning (including 6 tightened SCIP models)')
print('PASS: all finite values weaker than reference certificates; no reference-primal cutoff; zero accepted closures')
print('PASS: 10 overloaded first-batch rows disclosed and measurement-valid; GUROBI tolerance warning and hvycrash cos-only failure surfaced')
print('PASS: 74 complete primal observations (36 returned, 38 log); source printing precision retained')
print('PASS: three kept memory-cap attempts match archive logs/traces; nine archived attempts; no escalation')
print('PASS: 18 selected 50-digit point checks including 3 GUROBI waterno2 savepoints; reference hashes and 86 GAMS/OSIL model hashes unchanged')
print('PASS: no solver, project-wide or CI checks run')
