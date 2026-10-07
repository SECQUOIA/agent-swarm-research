"""Targeted consistency checks for the October 3 note closeout; run from code/."""
import json
import re
from pathlib import Path

from method_table import load

note_path = Path('../note.md')
note = note_path.read_text()
assert not re.search(r'\b(?:SPAR_[A-Z_]+|AP_[A-Z_]+|SCS_[A-Z_]+|TODO|TBD|FIXME|PLACEHOLDER)\b', note)
assert 'Status: revised after review round 2;\nnot re-reviewed.' in note
for name in ('chain', 'cactus', 'ht', 'spar'):
    suffix = '' if name == 'spar' else '_compact'
    table = Path('../logs/table_' + name + suffix + '.md').read_text().strip()
    assert table in note, name

summary = json.loads(Path('../logs/revision_summary.json').read_text())
assert len(summary['spar']) == 17
assert len(summary['late_gurobi']) == 6
assert sum(r['optimal'] for r in summary['late_gurobi'].values()) == 1
assert summary['late_gurobi']['ht_plus_n30_k2_s1']['optimal']
for tag, r in summary['late_gurobi'].items():
    assert ('%.11f' % r['ub']).rstrip('0') in note, (tag, 'incumbent')
    assert ('%.11f' % r['lb']).rstrip('0') in note, (tag, 'bound')
for rows in summary['queues'].values():
    for r in rows:
        assert r['exists'], r
        if 'completed_starts' in r:
            assert r['completed_starts'] >= r['requested_starts'], r
        if 'completed_seeds' in r:
            assert r['completed_seeds'] == r['requested_seeds'], r
        if 'completed_json' in r:
            assert r['completed_json'], r
        if 'recorded_methods' in r:
            assert set(r['requested_methods']) <= set(r['recorded_methods']), r

methods = load('../logs/ap_gap_methods.jsonl')
B = methods['B'][-1]['safe']
ap_section = note[note.index('### 4.2'):note.index('### 4.3')]
for m in ('K', 'A', 'KA', 'F', 'KAF', 'X'):
    safe = methods[m][-1]['safe']
    row = '| %s | %.8f | %.4f |' % (m, safe, (safe - B) / (-289 - B))
    assert row in ap_section, row
assert methods['F'][-1]['size']['F'] == 2
assert methods['KAF'][-1]['size']['F'] == 0

missing = []
for href in re.findall(r'\]\(([^)]+)\)', note):
    if '://' not in href and not href.startswith('#'):
        target = note_path.parent / href.split('#')[0]
        if not target.exists():
            missing.append(href)
assert not missing, missing
print('PASS: no placeholders; revision is explicitly not re-reviewed')
print('PASS: four generated tables match note; six late Gurobi references agree')
print('PASS: all queued outputs and requested counts/methods present')
print('PASS: AP table agrees with selective solve logs; F=2 blocks, KAF=0 added blocks')
print('PASS: all local note links resolve')
