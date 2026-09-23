"""Separate full paired cohorts for the two declared baseline followups."""
import collections
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
source = HERE / 'analysis.json'
data = json.loads(source.read_text())
by = {(r['run'], r['instance'], r['method']): r for r in data['records']}
out = dict(input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
           script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           meaning='Outcome-triggered supplementary cohorts; original results retained, no best-run substitution.',
           summaries=[], paired=[])
fields = ('category', 'feasible', 'solved', 'wall_time', 'objective', 'dual_bound',
          'absolute_gap', 'raw_status', 'max_normalized_violation', 'validation_issues')
for run, original, suffix, count in (
    ('gurobi_trig_sensitivity_v1', 'main_generated_v1', '-feas1e8', 9),
    ('legacy_initialization_v1', 'legacy_external_v1', '-initialized', 24),
):
    rows = sorted((r for r in data['records'] if r['run'] == run),
                  key=lambda r: (r['instance'], r['method']))
    assert len(rows) == count
    for method in sorted({r['method'] for r in rows}):
        selected = [r for r in rows if r['method'] == method]
        primary = [by[original, r['instance'], method.removesuffix(suffix)] for r in selected]
        out['summaries'].append(dict(run=run, method=method, scheduled=len(selected),
            original_categories=dict(collections.Counter(r['category'] for r in primary)),
            followup_categories=dict(collections.Counter(r['category'] for r in selected)),
            original_feasible=sum(r['feasible'] for r in primary),
            followup_feasible=sum(r['feasible'] for r in selected),
            original_solved=sum(r['solved'] for r in primary),
            followup_solved=sum(r['solved'] for r in selected)))
    for r in rows:
        prior = by[original, r['instance'], r['method'].removesuffix(suffix)]
        pair = dict(run=run, instance=r['instance'], method=r['method'], size=r['size'])
        for label, record in [('original', prior), ('followup', r)]:
            pair.update({label + '_' + key: record[key] for key in fields})
        out['paired'].append(pair)
(HERE / 'followups.json').write_text(json.dumps(out, indent=2) + '\n')
with (HERE / 'followups.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(out['paired'][0]))
    writer.writeheader()
    for row in out['paired']:
        writer.writerow({k: json.dumps(v) if isinstance(v, list) else v for k, v in row.items()})
print(json.dumps(out['summaries'], indent=2))
