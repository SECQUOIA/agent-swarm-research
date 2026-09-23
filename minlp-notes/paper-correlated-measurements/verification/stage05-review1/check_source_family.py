"""Independent explicit source-window feasibility and exact ranking-summary audit."""
from pathlib import Path
from itertools import product
from fractions import Fraction as Q
from collections import Counter
import hashlib, json

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parents[1]/'supplement'/'source_kinetics'
source = Path('/tmp/minlp-measurement-source-audit-20260912/measurement-opt')
record = json.loads((PACKAGE/'exact-rankings.json').read_text())
assert (PACKAGE/'kinetics_Q_drop0.csv').read_bytes() == (source/'kinetics_source_data/Q_drop0.csv').read_bytes()
# Source passes linspace(0,60,9), and optimizer reads the first eight elements.
# Test its actual 10-minute sliding windows rather than replacing by adjacency.
source_times = [Q(15*i,2) for i in range(8)]
reported_times = [Q(15*(i+1),2) for i in range(8)]
windows = [[j for j in range(t,8) if source_times[j]-source_times[t] < 10] for t in range(8)]
assert windows == [[j for j in range(t,8) if reported_times[j]-reported_times[t] < 10] for t in range(8)]
found = set()
by_static = Counter()
for modes in product(range(4), repeat=8):
    if any(sum(modes[t] != 0 for t in win) > 1 for win in windows):
        continue
    manual = tuple((t, modes[t]-1) for t in range(8) if modes[t])
    if len(manual) > 10 or any(sum(s == species for _,s in manual) > 10 for species in range(3)):
        continue
    for static in range(8):
        if not (manual or static): continue
        if any(static & (1 << species) for _, species in manual): continue
        found.add((static, manual))
        by_static[static.bit_count()] += 1
saved = {(a['selection']['static_mask'],tuple(map(tuple,a['selection']['manual_indices']))) for a in record['all_schedules']}
assert len(found) == 2347 and found == saved
assert {(c['budget'],c['criterion']) for c in record['comparisons']} == set(product(range(1000,5001,400), ['trace_information','determinant_information','trace_inverse_information']))
changed = []
min_relative_margin = {}
for c in record['comparisons']:
    optimal_sets=[]
    for formula in ('marginal','gated'):
        r=c[formula]
        assert len(r['optimal_indices']) == 1
        assert r['winning_index'] == r['optimal_indices'][0]
        assert r['winning_selection'] == record['all_schedules'][r['winning_index']]['selection']
        assert Q(r['margin_to_runner_up']) > 0
        optimal_sets.append(r['optimal_indices'])
        ratio=Q(r['margin_to_runner_up'])/abs(Q(r['objective']))
        name=c['criterion']
        min_relative_margin[name]=min(ratio,min_relative_margin.get(name,ratio))
    assert c['same_exact_optimal_set'] == (optimal_sets[0] == optimal_sets[1])
    if optimal_sets[0] != optimal_sets[1]: changed.append((c['budget'],c['criterion']))
assert changed == [(3000,'trace_information')]
report={'status':'PASS','source_hash':hashlib.sha256((source/'kinetics_MO.py').read_bytes()).hexdigest(),'schedules':len(found),'counts_by_static_species':dict(sorted(by_static.items())),'all_66_exact_optima_unique':True,'changed':changed,'minimum_relative_runner_up_margins':{k:str(v) for k,v in min_relative_margin.items()},'uniform_time_shift_leaves_every_source_spacing_window_unchanged':True}
(HERE/'source-family-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
