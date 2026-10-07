"""Check review-r2 claims directly from saved data; no solver or stream imports.

Run from any directory with OMP_NUM_THREADS=1 timeout 300s python3 -B
research-20261001/scip-rule-fidelity/code/check_revision_r2.py.
Uses one process and the standard library. Review files are read only.
Ray rescaling is optimized analytically, independently of the reviewer's grid.
"""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import gzip
import hashlib
import json
import math
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT / 'logs'
U = 2.0 ** -53


def ratio(coefs):
    nonzero = [abs(x) for x in coefs if x != 0]
    return min(nonzero) / max(nonzero) if nonzero else 1.0


def pattern(coefs):
    largest = max(map(abs, coefs))
    return ''.join(name for name, x in zip('ABC', coefs)
                   if x != 0 and abs(x) <= 1e-15 * largest)


def best_ratio(coefs):
    """Maximize min_nonzero/max for (lambda^2 A, lambda B, C).

    In log space the range is convex and piecewise linear. Its minimum
    occurs at a crossing of two lines (or everywhere for a single line).
    Zero entries remain zero and are excluded, as in SCIP's test.
    """
    lines = [(2 - i, math.log(abs(x))) for i, x in enumerate(coefs) if x]
    if len(lines) < 2:
        return 1.0
    crossings = [(b2 - b1) / (m1 - m2)
                 for j, (m1, b1) in enumerate(lines)
                 for m2, b2 in lines[j + 1:]]
    spread = min(max(m * t + b for m, b in lines)
                 - min(m * t + b for m, b in lines) for t in crossings)
    return math.exp(-spread)


def recompute_a(rec, ray):
    """First-piece A and absolute evaluation, including all of w(ray).

    The absolute evaluation replaces each eigenvector dot product by the
    sum of its absolute terms. A <= 64u * absolute evaluation is only a
    heuristic rounded-zero diagnostic for arithmetic on the dumped inputs.
    It does not assess errors already present in LP values or eigenvectors.
    """
    nq, sf = rec['nquad'], rec['sidefactor']
    a = absolute = wray = wabsolute = 0.0
    for i, eigenvalue in enumerate(rec['eigval']):
        terms = [rec['eigvec'][i * nq + k] * v for k, v in ray if k < nq]
        dot = scale = 0.0
        for term in terms:
            dot += term
            scale += abs(term)
        if abs(eigenvalue) <= 1e-9:
            if rec['case4']:
                wray += rec['vb'][i] * dot
                wabsolute += abs(rec['vb'][i]) * scale
        elif sf * eigenvalue < 0:
            a -= (sf * eigenvalue) * (dot * dot)
            absolute -= (sf * eigenvalue) * (scale * scale)
    if rec['case4']:
        for k, value in reversed(ray):
            if k >= nq:
                coefficient = -sf if k == nq + rec['nlin'] else sf * rec['lincoefs'][k - nq]
                wray += coefficient * value
                wabsolute += abs(coefficient * value)
        divisor = 4 * math.sqrt(1 + rec['kappa'] ** 2)
        a += wray * wray / divisor
        absolute += wabsolute * wabsolute / divisor
    return a, absolute


def water_check(rec, k):
    """Exact restriction using the original quadratic, without eigen data."""
    j = next(j for j, name in enumerate(rec['rayname']) if name == 't_x612')
    p = dict((i, F(v)) for i, v in rec['rays'][j])
    s = list(map(F, rec['zlp']))
    sf = -1 if rec['over'] else 1
    b = list(map(F, rec['qlin'] + rec['lincoefs']))
    if rec['auxvar'] is not None:
        b.append(F(-1))
        c = F(rec['constant'])
    else:
        c = F(rec['constant']) - F(rec['rhs']) if sf == 1 else F(rec['constant']) - F(rec['lhs'])
    q0 = c + sum(x * y for x, y in zip(b, s))
    linear = [b[i] * v for i, v in p.items()]
    m = F(0)
    partners = []
    for i, a in enumerate(rec['qsqr']):
        a = F(a)
        q0 += a * s[i] ** 2
        linear.append(2 * a * s[i] * p.get(i, 0))
        m += a * p.get(i, 0) ** 2
    for i, h, a in rec['bilin']:
        a = F(a)
        q0 += a * s[i] * s[h]
        term = a * (s[i] * p.get(h, 0) + s[h] * p.get(i, 0))
        linear.append(term)
        m += a * p.get(i, 0) * p.get(h, 0)
        if term:
            partner = i if p.get(h, 0) else h
            partners.append((rec['vars'][partner], rec['zlp'][partner], float(a)))
    q0, l, m = sf * q0, sf * sum(linear), sf * m
    assert q0 > 0 and l < 0 and m == 0
    assert len([x for x in linear if x]) == len(partners) == 1
    assert len(p) == 1 and list(p.values()) == [F(-1)]
    assert abs(l) == F(partners[0][1]) and partners[0][2] == 1
    assert rec['rayrate'][j] == 0
    return dict(k=k, ray=j, partner=partners[0][0], partner_lp=partners[0][1],
                q0=float(q0), L=float(l), M=float(m), reaches_S=True, step=float(-q0 / l))


def main():
    gurobi = [json.loads(line) for line in (LOGS / 'gurobi_zk.jsonl').open()]
    incumbents = {(r['inst'], r['k']): r['obj'] for r in gurobi if r['obj'] is not None}
    samples = {}
    table = []
    for directory in ('an_minlplib', 'an_minlplib2'):
        for path in sorted((LOGS / directory).glob('*.jsonl')):
            for line in path.open():
                row = json.loads(line)
                if 'k' not in row:
                    continue
                if row.get('fail') == 'numerics':
                    samples[(row['inst'], row['k'])] = row
                if row.get('status') == 'ok' and row['wmax'] > 0 and not row.get('zeroface_meets_S'):
                    zc = row['zC_scip'] if row['zC_scip'] is not None else row['zC_fixed']
                    zk = row['zK']
                    key = (row['inst'], row['k'])
                    if row['zK_kind'] == 'upper' and key in incumbents:
                        zk = min(zk, incumbents[key])
                    if zc is not None and zk is not None and 0 < zk < math.inf:
                        table.append(row)
    groups = {'all': [], 'sampled': []}
    a_levels, a_errors, water = [], [], []
    counts = Counter()
    for path in sorted((LOGS / 'runs_minlplib').glob('*.jsonl.gz')):
        k = -1
        with gzip.open(path, 'rt') as src:
            for line in src:
                if not line.startswith('{"v":'):
                    continue
                k += 1
                iswater = path.stem == 'waterund32.jsonl' and k in (651, 715, 1138, 1292)
                if '"fail":"numerics"' not in line and not iswater:
                    continue
                rec = json.loads(line)
                if iswater:
                    water.append(water_check(rec, k))
                if rec.get('fail') != 'numerics':
                    continue
                assert rec['nbadray1'] - rec['nbadray0'] == 1
                failed = [r for r in rec['perray'] if r.get('fail')]
                assert len(failed) == 1
                failure = failed[0]
                first = failure['c1234a'][:3]
                piece = 'first' if ratio(first) <= 1e-15 else '4b'
                assert ratio(first if piece == 'first' else failure['c4b'][:3]) <= 1e-15
                counts[piece] += 1
                key = (path.name.removesuffix('.jsonl.gz'), k)
                sampled = key in samples
                if sampled:
                    analysis = samples[key]
                    assert (rec['lp'], rec['cons'], failure['i']) == (analysis['lp'], analysis['cons'], analysis['fail_ray'])
                    counts['sampled_' + piece] += 1
                if piece != 'first':
                    continue
                ray = rec['rays'][failure['i']]
                entry = dict(pattern=pattern(first), best=best_ratio(first),
                             rayqmax=max([abs(v) for i, v in ray if i < rec['nquad']] or [0]))
                groups['all'].append(entry)
                if sampled:
                    groups['sampled'].append(entry)
                    if entry['pattern'] == 'A':
                        a, scale = recompute_a(rec, ray)
                        a_errors.append(abs(a - first[0]) / abs(first[0]))
                        a_levels.append(abs(first[0]) / (U * scale) if scale else math.inf)
        print('read', path.name, flush=True)
    assert (counts['first'], counts['4b'], counts['sampled_first'], counts['sampled_4b']) == (34834, 3271, 1799, 175)
    print('abort counts', dict(counts))
    for name, rows in groups.items():
        tiny = Counter(r['pattern'] for r in rows)
        passed = sum(r['best'] > 1e-15 for r in rows)
        print(name, 'patterns', dict(tiny), 'A-only %.1f%%' % (100 * tiny['A'] / len(rows)))
        print(name, 'rescaled first-piece passes', f'{passed}/{len(rows)} ({passed / len(rows):.1%})',
              'median best ratio', median(r['best'] for r in rows),
              'median quadratic-variable ray max', median(r['rayqmax'] for r in rows))
        assert (tiny['A'], passed) == ((28071, 31926) if name == 'all' else (1270, 1728))
    outside = sum(x > 64 for x in a_levels)
    assert outside == 1209
    print('sampled A-only outside 64u rounded-zero diagnostic', f'{outside}/{len(a_levels)}',
          'median A/(u*absolute evaluation)', median(a_levels), 'max relative recomputation error', max(a_errors))
    assert len(water) == 4
    for row in water:
        print('waterund32', json.dumps(row, sort_keys=True))
    infeasible = {(r['inst'], r['k']) for r in gurobi if r['status'] == 'infeasible'}
    uncertain = [r for r in table if (r['inst'], r['k']) in infeasible]
    assert len(table) == 1067 and len(uncertain) == 10
    assert all(r['zK_kind'] == 'upper' and (r['zC_scip'] if r['zC_scip'] is not None else r['zC_fixed']) / r['zK'] < 0.5 for r in uncertain)
    print('N4: 10/1067 = %.12f percentage points; ratios can only rise, fractions below thresholds can only fall' % (1000 / 1067))
    source = Path((_PUBLIC_HOME + '/build-scip/scipoptsuite-10.0.3/scip/src/scip/nlhdlr_quadratic.c'))
    print('source read', source, 'sha256', hashlib.sha256(source.read_bytes()).hexdigest())
    lines = source.read_text().splitlines()
    for lo, hi in ((814, 825), (1008, 1034), (1612, 1617), (1692, 1697), (2076, 2092), (2638, 2645)):
        for i in range(lo, hi + 1):
            print(f'{i}: {lines[i - 1]}')
    print('PASS: all r2 numerical assertions; one process, no solver calls')


if __name__ == '__main__':
    main()
