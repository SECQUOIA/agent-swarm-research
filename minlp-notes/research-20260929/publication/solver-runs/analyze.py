#!/usr/bin/env python3
"""Compare every kept run with frozen references; never launches solvers."""
import csv
import json
from collections import Counter
from decimal import Decimal, localcontext
from pathlib import Path

import collect

HERE = Path(__file__).resolve().parent

def dec(v):
    if v is None or v == '':
        return None
    return Decimal(str(v))

def finite(v):
    return v is not None and v.is_finite()

def diff(a, b, sign):
    return str(sign * (a - b)) if a is not None and b is not None else None

def save_csv(name, rows):
    with (HERE / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def fmt(v):
    if v is None:
        return '—'
    d = dec(v)
    return format(d, '.12g') if d.is_finite() else str(d)

refs = {r['instance']: r for r in json.loads((HERE / 'references.json').read_text())}
runs = json.loads((HERE / 'results.json').read_text())
checks = {(r['instance'], r['solver']): r for r in json.loads((HERE / 'point_checks.json').read_text())}
rows, anomalies = [], []
with localcontext() as ctx:
    ctx.prec = 60
    for run in runs:
        name, solver = run['instance'], run['solver']
        ref = refs[name]
        sign = Decimal(1 if ref['sense'] == 'min' else -1)
        assert run['sense'] == ref['sense']
        tr = collect.parse_trace(HERE / run['run_dir'] / 'trace.trc')
        log = collect.parse_log((HERE / run['run_dir'] / 'gams.log').read_text(), solver, ref['sense'])
        primal = dec(tr.get('ObjectiveValue')) if run['primal_objective'] is not None else None
        dual = dec(run['dual_bound_text']) if run['dual_bound_text'] else dec(run['dual_bound'])
        cert, refp, listd, listp = map(dec, [ref['certificate_dual'], ref['reference_primal'],
                                           ref['listed_dual'], ref['listed_primal']])
        logp = dec(log['final_primal_tok']) if run['solver_log_primal'] is not None else None
        notes, flags = [], []
        scope_r = ref['certificate_scope'] != 'OSIL'
        if scope_r:
            notes.append('OSIL exactly infeasible; certificate and reference primal concern R only')
        if not run['valid']:
            status = 'stopped at the 8 GB memory limit'
            notes.append(f'INVALID time measurement; kept attempt {run["attempt"]} of {run["attempts_total"]}; final bound retained')
        elif run['solver_status'] == 6:
            status = 'capability failure'
            notes.append('tanh unsupported' if name == 'ann_cumene_tanh' else
                         'cos unsupported' if name == 'hvycrash' else 'sin/cos unsupported')
        elif run['solver_status'] == 13:
            status = 'interface/model-expression failure'
            notes.append('GUROBI error 10024: POW needs at least one constant argument')
        elif run['model_status'] == 1:
            status = 'optimality claim contradicted'
        elif run['primal_objective'] is None:
            status = 'time limit, no primal'
        elif run['model_status'] == 2:
            status = 'time limit, locally optimal point'
        else:
            status = 'time limit, feasible point'
        if run['reported_max_constraint_violation']:
            status = 'time limit, point exceeds solver tolerance'
        if run['globality_warning']:
            notes.append('BARON: globality not guaranteed (inappropriate variable bounds)')
        if run['scip_argument_bounds_tightened']:
            notes.append('SCIP: log/pow argument lower bounds tightened to 1e-9; dual is for a slightly tightened model')
        if run['reported_max_constraint_violation']:
            notes.append(f'GUROBI reports max constraint violation {run["reported_max_constraint_violation"]} beyond its tolerance')
        if run['loaded_first_batch']:
            notes.append('first admitted batch: machine overload and memory pressure; passed measurement validity rule')

        def anomaly(kind, value, reference, margin, token, relation):
            precision = collect.half_unit(token) if token else Decimal(0)
            printing = margin <= precision
            if scope_r:
                classification = 'R comparison only; known exact infeasibility of OSIL'
            elif printing:
                classification = 'within source printing precision; no established contradiction'
            elif (name, solver) in checks and kind == 'returned primal beyond certificate':
                classification = 'returned point numerically infeasible; feasibility-tolerance effect'
            else:
                classification = 'certificate-inconsistent primal; tolerance effect suspected, this point unchecked'
            if kind == 'dual cuts off reference primal':
                classification = ('dual cuts off proved exactly feasible point' if ref['primal_kind'].startswith('exact')
                                  else 'dual cuts off numerical reference; exact infeasibility not established')
            record = dict(instance=name, solver=solver, kind=kind, value=str(value),
                          reference=str(reference), forbidden_margin=str(margin),
                          source_print_halfunit=str(precision), within_source_print_precision=printing,
                          relation=relation, classification=classification,
                          known_issue=('known kan OSIL infeasibility' if scope_r else
                                      'known feasibility-tolerance phenomenon; this campaign observation is new'),
                          model_status=run['model_status'], solver_status=run['solver_status'],
                          point_checked=(name, solver) in checks and kind == 'returned primal beyond certificate')
            anomalies.append(record)
            flags.append(kind + (' (printing-scale)' if printing else ''))

        if primal is not None and sign * (cert - primal) > 0:
            anomaly('returned primal beyond certificate', primal, cert, sign * (cert - primal),
                    tr['ObjectiveValue'], 'primal < certificate (min); primal > certificate (max)')
        if finite(logp) and sign * (cert - logp) > 0:
            anomaly('log incumbent beyond certificate', logp, cert, sign * (cert - logp),
                    log['final_primal_tok'], 'log incumbent < certificate (min); > certificate (max)')
        if finite(dual) and sign * (dual - refp) > 0:
            anomaly('dual cuts off reference primal', dual, refp, sign * (dual - refp),
                    run['dual_bound_text'], 'dual > feasible upper bound (min); < feasible lower bound (max)')

        claim = run['model_status'] == 1 and run['solver_status'] == 1
        contradicted = any(f.startswith('returned primal beyond') or f.startswith('dual cuts off') for f in flags)
        if claim and contradicted:
            flags.append('optimality claim inconsistent with certificate')
        if finite(logp) and primal is not None and collect.differ_beyond_print(log['final_primal_tok'], tr['ObjectiveValue']):
            notes.append('GAMS returned point differs from solver log incumbent; both compared in CSV')
        if run['dual_bound_source'] and 'objest NA' in run['dual_bound_source'] and finite(dual):
            notes.append('dual from 13-digit GUROBI log; see printing half-unit in results.csv')
        if (name, solver) in checks:
            check = checks[name, solver]
            notes.append(f'50-digit point check: max row violation {float(check["row_viol"]):.3g} ({check["worst_row"]})')
        if solver == 'GUROBI' and name in ('waterno2_09', 'waterno2_12', 'waterno2_24'):
            notes.append(f'reported primal improves MINLPLib listed primal by {diff(listp, primal, sign)}; '
                         f'50-digit maximum violation {float(checks[name, solver]["max_viol"]):.6g}')
        notes.extend(flags)
        if not finite(dual):
            notes.append('no finite final dual bound')
        row = dict(instance=name, sense=ref['sense'], solver=solver, status=status,
                   model_status=run['model_status'], solver_status=run['solver_status'],
                   valid_time_measurement=run['valid'], attempt=run['attempt'], attempts_total=run['attempts_total'],
                   solver_time_s=run['solver_time_s'], wall_time_s=run['wall_time_s'], cpu_time_s=run['cpu_time_s'],
                   cpu_over_wall=run['cpu_over_wall'], primal=str(primal) if primal is not None else None,
                   globality_warning=run['globality_warning'],
                   scip_argument_bounds_tightened=run['scip_argument_bounds_tightened'],
                   reported_max_constraint_violation=run['reported_max_constraint_violation'],
                   loaded_first_batch=run['loaded_first_batch'],
                   solver_log_primal=str(logp) if logp is not None else None,
                   dual=str(dual) if dual is not None else None,
                   certificate_dual=str(cert), reference_primal=str(refp),
                   certificate_scope=ref['certificate_scope'], reference_primal_kind=ref['primal_kind'],
                   listed_dual=str(listd) if listd is not None else None, listed_primal=str(listp),
                   gap_certificate_to_dual=diff(cert, dual, sign),
                   gap_primal_to_certificate=diff(primal, cert, sign),
                   primal_improvement_vs_reference=diff(refp, primal, sign),
                   log_primal_improvement_vs_reference=diff(refp, logp, sign),
                   dual_improvement_vs_listed=diff(dual, listd, sign),
                   primal_improvement_vs_listed=diff(listp, primal, sign),
                   log_primal_improvement_vs_listed=diff(listp, logp, sign),
                   log_primal_gap_to_certificate=diff(logp, cert, sign),
                   optimality_claim=claim,
                   closes_within_1h=bool(claim and run['valid'] and not contradicted and not scope_r
                                         and run['solver_time_s'] <= 3600),
                   notes='; '.join(notes))
        rows.append(row)

save_csv('results_table.csv', rows)
save_csv('inconsistencies.csv', anomalies)
(HERE / 'inconsistencies.json').write_text(json.dumps(anomalies, indent=2) + '\n')
stats = {}
for solver in ('BARON', 'GUROBI', 'SCIP'):
    rr = [r for r in rows if r['solver'] == solver]
    raw = [r for r in runs if r['solver'] == solver]
    long = [r for r in raw if r['valid'] and r['wall_time_s'] > 60]
    stats[solver] = dict(runs=len(rr), valid_time_measurements=sum(r['valid_time_measurement'] for r in rr),
                         raw_optimality_claims=sum(r['optimality_claim'] for r in rr),
                         closes_within_1h=sum(r['closes_within_1h'] for r in rr),
                         finite_duals=sum(finite(dec(r['dual'])) for r in rr),
                         finite_duals_without_globality_warning=sum(finite(dec(r['dual'])) and not r['globality_warning'] for r in rr),
                         finite_duals_with_globality_warning=sum(finite(dec(r['dual'])) and r['globality_warning'] for r in rr),
                         finite_duals_for_tightened_model=sum(finite(dec(r['dual'])) and r['scip_argument_bounds_tightened'] for r in rr),
                         loaded_first_batch_runs=sum(r['loaded_first_batch'] for r in rr),
                         duals_weaker_than_certificate=sum(dec(r['gap_certificate_to_dual']) > 0 for r in rr
                                                           if finite(dec(r['gap_certificate_to_dual']))),
                         duals_improve_listed=sum(dec(r['dual_improvement_vs_listed']) > 0 for r in rr
                                                 if finite(dec(r['dual_improvement_vs_listed']))),
                         primal_points=sum(r['primal'] is not None for r in rr),
                         capability_failures=sum(r['solver_status'] == 6 for r in rr),
                         other_failures=sum(r['solver_status'] >= 9 for r in rr),
                         memory_stops=sum(not r['valid_time_measurement'] for r in rr),
                         long_valid_cpu_ratio_range=[min(r['cpu_over_wall'] for r in long), max(r['cpu_over_wall'] for r in long)],
                         long_valid_cpu_seconds_range=[min(r['cpu_time_s'] for r in long), max(r['cpu_time_s'] for r in long)],
                         peak_group_swap_mb=max(r['peak_group_swap_mb'] or 0 for r in raw))
stats['overall'] = dict(instances=len(refs), rows=len(rows),
                        unresolved_by_all_three=len(refs) - len({r['instance'] for r in rows if r['closes_within_1h']}),
                        feasible_class_instances_unclosed=37, exactly_infeasible_kan_instances=6,
                        anomaly_counts=dict(Counter(a['kind'] for a in anomalies)),
                        returned_primal_flags_beyond_printing=sum(a['kind'] == 'returned primal beyond certificate'
                                                                and not a['within_source_print_precision'] for a in anomalies),
                        point_checks=len(checks))
(HERE / 'analysis_summary.json').write_text(json.dumps(stats, indent=2) + '\n')

md = ['# Final solver campaign: per-instance results', '',
      'All values are solver reports, not rigorous certificates. Full printed values and all comparisons are in '
      '[results_table.csv](results_table.csv); reference sources are in [references.csv](references.csv).', '',
      'BARON makes two optimality claims, both contradicted by our certified bounds. Accepted closures: '
      '**BARON 0, GUROBI 0, SCIP 0**. All 37 instances outside the six exactly infeasible kan models remain '
      'unclosed by all three solvers in this campaign. All 43 lack an accepted campaign closure.', '',
      'There are **109 finite dual values, including six BARON values without a globality guarantee** '
      '(catmix100/200/400/800, dtoc5, optcdeg2). The other 103 comprise BARON 29, GUROBI 36 and SCIP 38; '
      'six SCIP values concern slightly tightened models, as noted per row. No solver supplies a finite '
      'catmix bound with an unqualified globality claim. Ten rows flag the first admitted batch under '
      'machine overload and memory pressure; all passed the measurement validity rule.', '',
      '`Time` is GAMS solver time in seconds; for BARON it is wall clock while the 3600 s limit is CPU time. '
      'Four BARON values are 3706.37, 3708.98, 3709.5 and 3728.4 s; CSV also gives wall/CPU time. `C−D` means certificate minus '
      'solver dual for minimization, solver dual minus certificate for maximization: positive means the '
      'certificate is stronger. Infinite or missing duals give Infinity or —. Negative `P−C` in the CSV '
      'flags a primal beyond the certificate. For kan, comparisons concern R and do not certify the OSIL model.', '',
      '`Closes` requires a valid run, a global optimality claim within the 3600 s solver budget and consistency '
      'with the certificates. Capability failures and the three memory stops are explicit outcomes; memory '
      'stops use the kept attempt and are excluded from full-hour measurements. Markdown numbers use 12 '
      'significant digits; CSV preserves source decimal tokens.', '',
      '| Instance | Solver | Status | Time (s) | Primal P | Dual D | C−D (sense adjusted) | Closes | Notes |',
      '|---|---|---|---:|---:|---:|---:|---|---|']
for r in rows:
    md.append('| ' + ' | '.join([r['instance'], r['solver'], r['status'], fmt(r['solver_time_s']),
                                fmt(r['primal']), fmt(r['dual']), fmt(r['gap_certificate_to_dual']),
                                'yes' if r['closes_within_1h'] else 'no', r['notes']]) + ' |')
(HERE / 'results_table.md').write_text('\n'.join(md) + '\n')
grouped = {}
for a in anomalies:
    grouped.setdefault((a['instance'], a['solver']), {})[a['kind']] = a
im = ['# Certificate inconsistencies in the final campaign', '',
      'Every positive forbidden-side difference is retained, including differences explained by printing. '
      'The returned GAMS point and the solver log incumbent are distinct observations; their duplicate '
      'flags are not independent failures. No final solver dual cuts off a reference primal. Full decimal '
      'margins and classifications are in [inconsistencies.csv](inconsistencies.csv).', '',
      'All rows below are primal discrepancies. For minimization the margin is C−P; for pricing050 (max) '
      'it is P−C. A positive margin contradicts exact feasibility unless source printing explains it. '
      'The kan rows compare with R, whose certificate does not apply to tolerance-feasible OSIL points. '
      'All six original kan models are exactly infeasible.', '',
      '| Instance | Solver | Returned primal forbidden margin | Log incumbent forbidden margin | Interpretation |',
      '|---|---|---:|---:|---|']
for (name, solver), items in grouped.items():
    p = items.get('returned primal beyond certificate')
    l = items.get('log incumbent beyond certificate')
    interpretation = (p or l)['classification']
    if name in ('camshape100', 'camshape200') and solver == 'BARON':
        interpretation += '; reported optimal with zero solver gap'
    im.append(f"| {name} | {solver} | {p['forbidden_margin'] if p else '—'} | "
              f"{l['forbidden_margin'] if l else '—'} | {interpretation} |")
im += ['', 'The known waterno2 nonlinear propagation defect in [scip-bug/report.md](../scip-bug/report.md) '
       'is a different failure mode: an invalid cutoff and a too-high dual/optimal value. No whole-instance '
       'SCIP run here claims optimality or cuts off our reference point. These results do not test whether '
       'the defect occurred internally. The new campaign discrepancies match known feasibility-tolerance '
       'phenomena; no new solver defect is established.', '',
       'Selected savepoints were evaluated at 50 digits from exact binary64 levels against the decimal OSIL '
       'model. The original 15 selected points have positive row violations; three additional GUROBI '
       'waterno2 points are recorded in point_checks.json and the report. These are numerical checks, '
       'not interval proofs or repairs; log incumbent vectors were not independently available.']
(HERE / 'inconsistencies.md').write_text('\n'.join(im) + '\n')
print(json.dumps(stats, indent=2))
