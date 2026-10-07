"""Read saved evidence with exact arithmetic; import no scientific project code."""
import hashlib
import json
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from pathlib import Path
import re

import numpy as np

R = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
records = []


def check(label, condition, value=None):
    assert condition, label
    record = dict(check=label, passed=True)
    if value is not None:
        record['exact'] = str(value)
        if isinstance(value, Q):
            with localcontext() as ctx:
                ctx.prec = 50
                record['decimal'] = str(Decimal(value.numerator) / Decimal(value.denominator))
    records.append(record)
    print('PASS', label, record.get('decimal', record.get('exact', '')))


pages = {p['name']: p for p in json.loads((R / 'bound-audit/pages.json').read_text())}
for name in ('camshape100', 'lnts50'):
    print('SAVED LISTING', name, pages[name])
for name, optimum, listed, bad, safe in (
        ('camshape100', '-4.28414712174675', '-4.28415233', '1.2e-6', '1.3e-6'),
        ('lnts50', '0.5546687649381', '0.55464755', '3.8e-5', '3.9e-5')):
    gap = (Q(optimum) - Q(listed)) / abs(Q(optimum))
    check(name + ' historical relative gap', Q(bad) < gap < Q(safe), gap)

for name, display in (('eg_int_s', '6.4531031593842275'),
                      ('eg_disc_s', '5.7605396164535107')):
    text = (R / f'open-instances-wave3/eg/retry/sol/{name}.retry.sol').read_text()
    exact = Q(re.search(r'^objvar\s+(\S+)', text, re.M)[1])
    check(name + ' upward primal', Q(display) >= exact, Q(display) - exact)

for suffix, display, gap_display in (('09', '914.012', '10.82'),
                                    ('12', '2233.821346', '6.90'),
                                    ('18', '5023.983', '4.90'),
                                    ('24', '6963.795181', '5.90')):
    name = 'waterno2_' + suffix
    primal = Q(json.loads((R / f'publication/primal/water-ann-kan/points/{name}.exact.json').read_text())['objective'])
    dual = Q(json.loads((R / f'open-instances-wave2/waterno2/logs/cert_{suffix}_w1_impl.json').read_text())['certified_bound_exact'])
    check(name + ' upward primal', Q(display) >= primal, Q(display) - primal)
    gap = 100 * (primal - dual) / dual
    check(name + ' upward percent gap', Q(gap_display) >= gap, gap)

part_bounds = []
for k in range(2):
    text = (R / f'open-instances-wave3/eg/retry/logs/disc9_p{k}.log').read_text()
    part_bounds.append(re.search(r'certified lower bound np.float64\(([^)]+)\)', text)[1])
check('eg_disc_s binding part is 1', Q(part_bounds[1]) < Q(part_bounds[0]), part_bounds[1])
excess = Q('5.760539610694994') - Q(float(part_bounds[1]))
check('eg_disc_s decimal exceeds binary64', 0 < excess < Q('2.4e-16'), excess)
leaflog = (R / 'reviews/eg-retry-review-checks/logs/verify_disc_p1.log').read_text()
check('eg_disc_s exact-decimal independent leaf check', '40573' in leaflog and '5.760539610694994' in leaflog)

chunks = sorted((R / 'publication/eg-recheck/res').glob('p*_c*.npz'))
wall = Q(0)
leaves = failures = 0
for path in chunks:
    with np.load(path, allow_pickle=False) as z:
        wall += Q(float(z['time']))
        leaves += len(z['ok'])
        failures += int((~z['ok']).sum())
check('38 chunks, 1114361 leaves, zero failures', len(chunks) == 38 and leaves == 1114361 and failures == 0)
check('chunk wall seconds round once to 41162', Q('41161.5') <= wall < Q('41162.5'), wall)
for rel in ('publication/eg-recheck/recheck_leaves.py', 'open-instances-wave3/eg/retry/egbb.py'):
    check(rel + ' uses wall clock', 'time.time() - t0' in (R / rel).read_text())

bug = R / 'publication/scip-bug/logs'
binary = [line for line in (bug / 'binary_p4.log').read_text().splitlines() if line.startswith('10.1.0 seed')]
check('p4 10.1.0 wrong for all ten seeds', len(binary) == 10 and all(line.endswith('WRONG') for line in binary))
for path in sorted(bug.glob('*gams*')):
    if path.is_file():
        text = path.read_text()
        if 'p4' in text:
            print('GAMS P4 SOURCE', path.name, '\n'.join(line for line in text.splitlines() if 'p4' in line))

lic = R / 'publication/reviews/integration-r2/agent-licence/sources'
check('optrove SIF MIT source notice', 'MIT License' in (lic / 'bitbucket_optrove_sif_LICENSE').read_text())
check('MATPOWER case data qualification', 'In most cases' in (lic / 'matpower_LICENSE').read_text())
check('MATPOWER 8.1 citation request', 'request that publications derived' in (R / 'publication/literature/network/sources/MATPOWER-manual-8.1.txt').read_text())
check('QPLIB citation request', 'please cite' in (R / 'publication/literature/control/sources/qplib_index.html').read_text())
gams = (R / 'publication/scip-bug/gams/logs/scan_p4.txt').read_text().splitlines()
seeds = [line for line in gams if re.match(r'p4 seed \d+:', line)]
check('p4 GAMS/SCIP wrong for all ten seeds', len(seeds) == 10 and all('WRONG' in line for line in seeds))
for line in (lic / 'SHA256SUMS').read_text().splitlines():
    digest, name = line.split(maxsplit=1)
    if name.startswith('(not saved)'):
        continue
    p = lic / Path(name.lstrip('*')).name
    if not p.exists():
        p = Path('/tmp/lic') / p.name
    check('saved licence hash ' + p.name, hashlib.sha256(p.read_bytes()).hexdigest() == digest)

(OUT / 'review-r2-evidence.json').write_text(json.dumps(records, indent=2) + '\n')
print('ALL REVIEW R2 EVIDENCE CHECKS PASSED', len(records))
