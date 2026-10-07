"""Targeted data/text/patch checks; never import or execute scientific code."""
import ast
from decimal import Decimal
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

W = Path(__file__).resolve().parent
P = W.parents[1]
R = P.parent
os.sched_setaffinity(0, sorted(os.sched_getaffinity(0))[:2])

def read(rel):
    return (R / rel).read_text()

# Exact older lnts dual displays, including uncertainty in nstr(h2, 20).
verifier = json.loads((R / 'reviews/open-instances-verification/logs/lnts_verify.json').read_text())
displays = {(100, 'cert_1e-12'): ('0.5545954011663566', '0.5545954011663565'),
            (200, 'cert_1e-12'): ('0.5545770161025291', '0.5545770161025290'),
            (200, 'cert_1e-10'): ('0.554577016047626', '0.5545770160476259'),
            (400, 'cert_1e-10'): ('0.5545724136452299', '0.5545724136452298')}
for item in verifier:
    n = int(item['name'][4:])
    for cert in ['cert_1e-12', 'cert_1e-10']:
        if (n, cert) not in displays:
            continue
        h = Decimal(item[cert]['h2'])
        unit = Q(10) ** (h.as_tuple().exponent + len(h.as_tuple().digits) - 20)
        lo, hi = n * (Q(h) - unit), n * (Q(h) + unit)
        old, new = map(Q, displays[n, cert])
        assert old > hi and new <= lo, (n, cert)
        print('lnts', n, cert, 'old exceeds enclosure; new lower display valid; margin', float(lo-new))
text = read('reviews/open-instances-verification/verification-report.md')
for old, new in displays.values():
    assert old not in text and new in text
assert '0.5545954011663565' in read('reviews/closing-audit-a.md')

# Check telescope coefficients, rather than repeating the incorrect proof constant.
for n in [50, 100, 200, 400]:
    coefficients = [Q(0)] * (n+1)
    for i in range(n):
        coefficients[i] += 50
        coefficients[i+1] += 50
    weights = [Q(1, 2)] + [Q(1)] * (n-1) + [Q(1, 2)]
    assert coefficients == [100*w for w in weights]
lnts = (P / 'primal/lnts/report.md').read_text()
assert '45/(100h)' in lnts and '45/(50h)' not in lnts
assert 'trapezoid weights w = (1/2, 1, …, 1, 1/2)' in lnts
assert '- logs/review_r2_check.log:' in lnts
print('lnts telescope: vx_N = 100h sum(w_j cos(theta_j)); weights verified for all four N.')

cops = read('open-instances-wave2/cops/report.md')
for n, primal, dual, gap in [(50, '5.0722614939828724', '5.0722614939828627', '9.7e-15'),
                            (200, '5.0689173417931710', '5.0689173417931616', '9.4e-15')]:
    row = next(line for line in cops.splitlines() if line.startswith(f'| chain{n} |'))
    assert f'| {dual} | {gap} |' in row
    saved = json.loads((R / f'open-instances-wave2/cops/logs/chain{n}_bound.json').read_text())
    assert Q(dual) <= Q(saved['bnb']['bound'])
    assert Q(primal)-Q(dual) == Q(gap)
    print('chain', n, 'safe dual and exact displayed gap', gap)
for rel in ['open-instances-wave2/cops/report.md', 'reviews/cops-verification/verification-report.md',
            'reviews/closing-audit-a.md', 'publication/reviews/solver-campaign-review-r1.md']:
    text = read(rel)
    assert '5.072261493982863' not in text
    assert '5.068917341793162' not in text
assert 'as claimed (against the original binary64 displays)' in read('reviews/cops-verification/verification-report.md')

scip = (P / 'scip-bug/report.md').read_text()
b64 = (P / 'scip-bug/logs/binary64_scip_solution.log').read_text()
pair = (P / 'scip-bug/logs/pair_semantics.log').read_text()
claims = [Q(value) for value in re.findall(r'claimed ([^;\s]+)', b64)]
assert len(claims) == 3 and claims[2] == Q('-1.337')
assert claims[0] > Q(153, 250) and claims[1] > Q('168.108652029808')
pairs = [Q(value) for value in re.findall(r'claimed optimum ([^,\s]+)', pair)]
assert len(pairs) == 2 and pairs[0] < Q('55.689908409449') < pairs[1]
assert 'Of these five examined solutions, three are refuted wrong claims:' in scip
assert 'tiny2 with default settings returns the correct decimal optimum −1.337' in scip
assert 'pair2236 seed 0 returns the low claim 55.689773, which is not refuted' in scip
assert 'All instrumented cutoffs in Section 5.3 involve the 0.7 station' in scip
body = scip.split('## Response to review')[0]
assert '(10.0.2/10.0.3 acceptance: `../reviews/scip-bug-r1/rv_runs.log`)' in body
acceptance = (P / 'reviews/scip-bug-r1/rv_runs.log').read_text()
for version in ['10.0.2', '10.0.3']:
    assert f'[{version} fm336 readsol] 1/1 feasible solution given by solution candidate storage' in acceptance
table = scip.split('### 5.3 ', 1)[1].split('### 5.4 ', 1)[0]
rows = [line for line in table.splitlines() if line.startswith('| dbgsol ') or line.startswith('| master dbgsol ')]
assert len(rows) == 14
assert sum(2 if 'p5, 0 and 2' in row else 1 for row in rows) == 15
for seed in [0, 2]:
    trace = (P / f'scip-bug/logs/dbgsol_expr_p5_seed{seed}.log').read_text()
    assert 'reverseprop declared INFEASIBLE' in trace and 'x547>)^3-<t_x997>' in trace
print('SCIP: three wrong claims refuted; two correct/unrefuted cases separated; acceptance restored; 14 rows cover 15 runs.')
# The developer-facing draft was not modified.
before_scip = (W / 'before-r3/publication__scip-bug__report.md').read_text()
draft_marker = '## upstream-report-draft.md (content)'
assert draft_marker in scip
assert scip.split(draft_marker, 1)[1].split('## Response to review', 1)[0] == before_scip.split(draft_marker, 1)[1].split('## Response to review', 1)[0]

audit = (P / 'audit-ir/report.md').read_text()
assert 'The 10th-digit floor is a conservative choice; it changes no screened pair (Section 1).' in audit
assert 'define the counts as displayed entries (35 ' in audit
assert 'This is the coarsest rounding the page display could have applied.' not in audit
water = (P / 'primal/water-ann-kan/report.md').read_text()
assert 'by the same author. Independent review r1' in water
assert 'Use 1.68% for an upward two-decimal display; the gap is measured against an exactly feasible point.' in water
assert '| 3 | Changed waterno2_12 to 6.90% and waterno2_06 from 1.67% to 1.68%;' in water
control = (P / 'literature/control/report.md').read_text()
assert '| 9 | Propagated the rigorous lnts gap display' in control
response2 = (W / 'response-r2.md').read_text()
assert 'waterno2_06 1.67% → 1.68% in the report' in response2
assert 'Propagated ≤ 5.55e-13 to literature/control/report.md' in response2
assert 'primal/water-ann-kan/logs/minor_review_check.log' in json.loads((W / 'FILES-r2.json').read_text())
commands2 = json.loads((W / 'commands-r2.json').read_text())
assert commands2[-1]['command'] == commands2[0]['command'] and 'retrospectively' in commands2[-1]['note']

for track, prefix in [('primal/lnts', '| 5. Tiny middle control |'),
                      ('primal/powerflow', '| 6. Uniqueness citation |')]:
    row = next(line for line in (P / track / 'report.md').read_text().splitlines() if line.startswith(prefix))
    assert len(re.findall(r'(?<!\\)\|', row)) == 3, row
print('Assigned wording, retrospective records and escaped response-table pipes pass.')

for track in ['primal/chain', 'primal/lnts', 'primal/powerflow', 'primal/water-ann-kan',
              'audit-ir', 'scip-bug', 'literature/control']:
    report = P / track / 'report.md'
    text = report.read_text()
    marker = '### Round 3: independent minor-fixes review (2026-10-03)'
    assert text.count(marker) == 1, track
    for target in re.findall(r'\]\(([^)]+)\)', text.split(marker)[1]):
        assert (report.parent / target).resolve().is_file(), (track, target)
response3 = (W / 'response-r3.md').read_text()
assert [int(n) for n in re.findall(r'^\| (\d+)\.', response3, re.M)] == [1, 3, 7, 8, 9, 10, 11]
for rel, expected in json.loads((W / 'protected-r3.json').read_text()).items():
    assert hashlib.sha256((R / rel).read_bytes()).hexdigest() == expected, rel
for script in ['edit_r3.py', 'finish_r3.py', 'check_r3.py']:
    ast.parse((W / script).read_text())
ast.parse((P / 'literature/control/checks/dtoc5_reference_check.py').read_text())
check_output = (W / 'dtoc5_reference_r3.log').read_text()
assert '99999 variables; 2 finite upper bounds; 16 finite lower bounds' in check_output
assert '99997 upper defaults' in check_output and '99983 lower defaults imply 14' in check_output
assert 'min listed x x49999' in check_output and 'PASS:' in check_output
print('Seven response sections, links, script syntax, computed control counts and protected scientific bytes pass.')

# GNU patch must accept the regenerated historical patch in a disposable copy.
with tempfile.TemporaryDirectory(prefix='minor-fixes-r3-patch-') as directory:
    dest = Path(directory)
    for f in sorted((W / 'before').glob('*.txt')):
        report = dest / f.stem.replace('__', '/') / 'report.md'
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_bytes(f.read_bytes())
    bad = W / 'before-r3/publication__reviews__minor-fixes__report_changes.patch'
    result = subprocess.run(['patch', '--dry-run', '--batch', '--fuzz=0', '-p1', '-i', str(bad)],
                            cwd=dest, text=True, capture_output=True)
    assert result.returncode != 0 and 'malformed patch' in result.stderr, result
    print('Original round-1 patch reproduced GNU rejection:', result.stderr.strip())
    result = subprocess.run(['patch', '--batch', '--fuzz=0', '-p1', '-i', str(W / 'report_changes.patch')],
                            cwd=dest, text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr
    for f in sorted((W / 'before').glob('*.txt')):
        track = f.stem.replace('__', '/')
        assert (dest / track / 'report.md').read_bytes() == (W / 'before-r2' / (f.stem+'__report.md')).read_bytes(), track
    print('Regenerated round-1 patch: GNU patch --batch --fuzz=0 -p1 accepted; all ten final round-1 snapshots reproduced byte for byte.')
print('PASS: assigned round-3 track, record and patch checks; no project-wide or CI checks.')
