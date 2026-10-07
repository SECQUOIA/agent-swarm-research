"""Recompute the October 3 closeout numbers from existing outputs; run from code/."""
import glob
import json
import shlex
from pathlib import Path

from audit_table import best_ub
from chain_table import gurobi_ref

opts = {}
for line in Path('../sources/BoxQP_instances-master/README.txt').read_text().splitlines():
    fields = line.split()
    if len(fields) == 2 and fields[0].startswith('spar'):
        opts[fields[0]] = -float(fields[1])

spar = {}
for path in glob.glob('../logs/audit/spar*.json') + glob.glob('../logs/spar_audit/*.json'):
    if path.endswith('.tri.json'):
        continue
    r = json.loads(Path(path).read_text())
    gap = opts[r['name']] - r['B_safe']
    spar[r['name']] = {
        'source': path, 'min_depth': r['min_depth'], 'gap_safe': gap,
        'gain_term': r['max_triple_level_improvement'],
        'gain_term_over_gap': r['max_triple_level_improvement'] / gap,
        'gain_plus_primal_dual_margin_over_gap':
            (r['max_triple_level_improvement'] + r['B'] - r['B_safe']) / gap,
        'pinf': r['pinf'], 'triangle_violation': r.get('max_triangle_violation'),
        'count_depth_lt_1e-6': r['count_depth_lt_1e-6'],
        'family_stqp_min': r['family_stqp_min'],
    }

small = {}
for variant, pattern in [('spar', 'n*.jsonl'), ('ap', 'ap_*.jsonl')]:
    records = [json.loads(line) for p in glob.glob('../logs/small_dense/' + pattern)
               for line in Path(p).read_text().splitlines()]
    small[variant] = {
        'count': len(records), 'gap_count': sum('X' in r for r in records),
        'max_primal_relative_gap': max((r['opt'] - r['B']) / max(1, abs(r['opt'])) for r in records),
        'max_safe_relative_gap': max((r['opt'] - r['B_safe']) / max(1, abs(r['opt'])) for r in records),
    }

refs = {}
for p in sorted(glob.glob('../logs/gurobi2/*.log')):
    tag = Path(p).stem
    g = gurobi_ref(tag)
    status, ub, lb = Path(p).with_suffix('.res').read_text().split()
    assert abs(g['ub'] - float(ub)) < 1e-10 and abs(g['lb'] - float(lb)) < 1e-10
    assert g['optimal'] == (status == 'optimal')
    refs[tag] = dict(g, U=best_ub(tag))

queues = {}
for p in sorted(glob.glob('../data/tmp/queue_*.txt')):
    outputs = []
    for line in Path(p).read_text().splitlines():
        args = shlex.split(line)
        if '>' not in args:
            continue
        target = Path(args[args.index('>') + 1])
        entry = {'output': str(target), 'exists': target.exists()}
        if target.exists() and 'ub_local.py' in args:
            entry['completed_starts'] = json.loads(target.read_text().splitlines()[-1])['starts']
            entry['requested_starts'] = int(args[args.index('ub_local.py') + 2])
        if 'small_dense.py' in args:
            data = Path(args[args.index('small_dense.py') + 5])
            entry['completed_seeds'] = len(data.read_text().splitlines()) if data.exists() else 0
            entry['requested_seeds'] = int(args[args.index('small_dense.py') + 4])
        if 'gurobi_solve.py' in args and target.exists():
            entry['result'] = target.read_text().strip()
        if 'driver.py' in args:
            data = Path(args[args.index('--log') + 1])
            records = [json.loads(l) for l in data.read_text().splitlines()] if data.exists() else []
            entry['requested_methods'] = args[args.index('--methods') + 1].split(',')
            entry['recorded_methods'] = sorted({r['method'] for r in records})
        if 'chain_audit.py' in args or 'sparse_audit.py' in args or 'kall.py' in args:
            data = Path(args[args.index('>') - 1])
            entry['completed_json'] = data.exists()
            if data.exists():
                json.loads(data.read_text())
        outputs.append(entry)
    queues[p] = outputs

sparse_gap = {}
for p in glob.glob('../logs/sparse_audit/plus_*.json'):
    r = json.loads(Path(p).read_text())
    gap = best_ub(Path(p).stem) - r['B_safe']
    if gap / abs(r['B_safe']) > 1e-8:
        sparse_gap[Path(p).stem] = r['max_triple_level_improvement'] / gap

result = {'spar': spar, 'small_dense': small, 'late_gurobi': refs,
          'queues': queues, 'sparse_gain_term_over_gap': sparse_gap}
Path('../logs/revision_summary.json').write_text(json.dumps(result, indent=2) + '\n')
print('spar audited:', len(spar))
print('spar minimum-depth range:', min(r['min_depth'] for r in spar.values()),
      max(r['min_depth'] for r in spar.values()))
print('spar maximum gain term / gap:', max((r['gain_term_over_gap'], tag) for tag, r in spar.items()))
print('small dense:', small)
print('late Gurobi:', refs)
print('sparse gain term / gap:', sparse_gap)
print('missing queue outputs:', [r['output'] for rows in queues.values() for r in rows if not r['exists']])
