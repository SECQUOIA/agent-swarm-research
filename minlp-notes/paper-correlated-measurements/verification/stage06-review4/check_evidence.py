"""Independent integration-to-record checks; standard library only."""
from pathlib import Path
from fractions import Fraction as Q
from decimal import Decimal, localcontext
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
SUP = ROOT / 'supplement'
read = lambda p: json.loads(p.read_text())
freeze = read(ROOT / 'process/stage06-r01-freeze.json')
assert all(hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == h for p,h in freeze.items())
counts = {}
for name,key in [('archive-manifest.json','destination'),('source-manifest.json','path')]:
    m = read(SUP/name)
    entries = m if isinstance(m,list) else m['files']
    assert all(hashlib.sha256((SUP/e[key]).read_bytes()).hexdigest() == e['sha256'] for e in entries)
    counts[name] = len(entries)

s = read(SUP/'source_kinetics/exact-rankings.json')
assert len(s['all_schedules']) == 2347 and len(s['comparisons']) == 33
changed = [c for c in s['comparisons'] if not c['same_exact_optimal_set']]
assert len(changed) == 1 and changed[0]['budget'] == 3000 and changed[0]['criterion'] == 'trace_information'

f = read(SUP/'results/fresh-all.json')
n = f['nested']; levels = n['nested']
assert n['schedule_count'] == 56 and n['exact_schur_identities_checked'] == 224
assert all(Q(a['upper']) < Q(b['lower']) for a,b in zip(levels,levels[1:]))
assert Q(n['common_discrete_log_interval'][1]) < Q(levels[0]['lower'])
assert Q(n['dense']['upper_bound']) < Q(levels[-1]['lower'])
assert Q(levels[-2]['upper']) < Q(n['dense']['continuous_lower_bound'])
b = f['blocks']
assert b['schedule_count'] == 56
assert Q(b['sharp_far_delta']) < Q(b['old_delta']) < 1
assert Q(b['true_lower']) <= Q(b['exhaustive_true_optimum']) <= Q(b['sharp_far_upper']) < Q(b['old_upper'])

diag = read(SUP/'legacy/results/diagonal-split-kinetics-certificate.json')
assert Q(diag['all_diagonal_lower_bound']) - Q(diag['memory_upper_bound']) == Q(diag['separation']) > Q('0.0925444163328848')
cert = read(SUP/'legacy/results/robust-kinetic-n96-polished-certificate.json')
r = cert['standardized']; lo,hi,gap = (Q(r[k]) for k in ['lower_bound','upper_bound','gap'])
assert hi-lo == gap == Q('0.011487999119') and hi < 0
with localcontext() as ctx:
    ctx.prec = 60
    decimal = lambda q: Decimal(q.numerator)/Decimal(q.denominator)
    assert (decimal(lo)/3).exp()*100 > Decimal('97.1737')
    assert (-decimal(gap)/3).exp()*100 > Decimal('99.6177')

report = {'status':'passed','frozen_files_checked':len(freeze),'manifest_counts':counts,
          'source_schedules':2347,'source_comparisons':33,'changed_choices':1,
          'nested_strict_comparisons':3,'common_integer_and_dense_comparisons':'passed',
          'block_improvement':'passed','diagonal_separation':'passed','robust_efficiencies':'passed',
          'scope':'Checks integrated claims against exact stored records and hashes; does not replace mathematical certificate replay or whole-paper proof review.'}
(Path(__file__).parent/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
