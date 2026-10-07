"""F-consistency: recompute numbers that the paper quotes in several places
(Sections 6.5, 11 and Appendix H) from experiments/results/*.csv."""
import csv, statistics, os
from collections import defaultdict
R = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'experiments', 'results')
L = lambda f: list(csv.DictReader(open(os.path.join(R, f))))
# Section 6.5 / 11.4: S1
s1 = L('S1_localized.csv'); acc = [r for r in s1 if r['status'] == 'accepted']
print('S1: n range', min(int(r['n']) for r in s1), max(int(r['n']) for r in s1),
      'accepted', len(acc), '/', len(s1), 'max face stage idx', max(int(r['face_first_stage']) for r in acc),
      'max single-run stages (Omega)', max(int(r['single_run_stages_lemma']) for r in s1),
      'max EX stages', max(int(r['height_rule_stages']) for r in s1))
# Section 6.5 / 11.4 / App H: E4 bits
e4 = [r for r in L('E4_exact.csv') if r['status'] == 'exact']
print('E4: n max', max(int(r['n']) for r in e4), 'lemma bits', round(min(float(r['required_gap_bits_lemma']) for r in e4), 1),
      round(max(float(r['required_gap_bits_lemma']) for r in e4), 1))
# Section 11.2 / App H: 876 stages and ratios
st = ([r for r in L('E1_stages.csv') if r['method'] == 'geometric_pruned'] +
      [r for r in L('E2_stages.csv') if r['method'] == 'geom_theorem'] +
      [r for r in L('E3_stages.csv') if r['method'] == 'geom_theorem'])
print('E1-E3 theorem-grading stages', len(st), 'gap/bound', round(max(float(r['D_y_over_Lnh2']) for r in st) / (9 / 16), 3),
      'radius', round(max(float(r['radius_ratio_lemma']) for r in st), 3),
      'nodes/cap', max(int(r['max_nodes']) / int(r['cap_nodes_lemma']) for r in st))
# Section 11.6 / App H / Table 5
e6 = defaultdict(dict)
for r in L('E6_random_growth.csv'): e6[r['name']][int(r['q'])] = r
print('E6: instances', len(e6), 'same largest grid', sum(1 for d in e6.values() if len({d[q]['max_nodes'] for q in d}) == 1),
      'certified', sum(1 for d in e6.values() if d[50]['growth_status'] == 'certified'),
      'localized', sum(1 for d in e6.values() if d[50]['optimality_proof'] == 'localized'))
# Section 11.5 / App H: SCIP
sh = L('E5_scip_shortfall.csv')
print('E5 shortfall', min(float(r['shortfall']) for r in sh), max(float(r['shortfall']) for r in sh),
      'bound share', round(min(float(r['bound_share']) for r in sh), 3), round(max(float(r['bound_share']) for r in sh), 3))
