"""Targeted checks of round-1 corrections using saved results; no solver runs.

Usage: python3 -B check_revision_r1.py
"""
import collections
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np

import dumpio as D
import summarize as S

ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT / 'logs'
REVIEW = ROOT / 'reviews/r1-logs'


def rows(path):
    with path.open() as f:
        return [json.loads(line) for line in f]


def saved_results():
    samples = [S.load(sorted((LOGS / d).glob('*.jsonl'))) for d in ('an_minlplib', 'an_minlplib2')]
    for i, sample in enumerate(samples, 1):
        print('sample', i, len(sample), dict(collections.Counter(r['status'] for r in sample)))
        print('no-ray records by instance', dict(collections.Counter(r['inst'] for r in sample if r['status'] == 'norays')))
    allrows = samples[0] + samples[1]
    valid = [r for r in allrows if r.get('status') == 'ok']
    scaled = max(valid, key=lambda r: abs(r['kappa_py'] - r['kappa']) / max(1, abs(r['kappa'])))
    nz = [r for r in valid if r['kappa'] != 0]
    rel = max(nz, key=lambda r: abs(r['kappa_py'] - r['kappa']) / abs(r['kappa']))
    for name, r, denom in [('scaled', scaled, max(1, abs(scaled['kappa']))), ('relative', rel, abs(rel['kappa']))]:
        print('kappa', name, abs(r['kappa_py'] - r['kappa']) / denom, r['inst'], r['k'], r['kappa'])
    for name in ('gurobi_zk', 'gurobi_zk_validate', 'gurobi_zk_lowratio'):
        records = rows(LOGS / (name + '.jsonl'))
        print(name, len(records), dict(collections.Counter(r['status'] for r in records)))
        if name != 'gurobi_zk':
            for r in records:
                if r['obj'] is not None:
                    r['rel_diff'] = (r['obj'] - r['zK_analysis']) / r['zK_analysis']
            compared = [r for r in records if r['status'] == 'optimal']
            worst = max(compared, key=lambda r: abs(r['rel_diff']))
            print('optimal max abs relative difference', abs(worst['rel_diff']), worst['inst'], worst['k'],
                  'signed', worst['rel_diff'], 'median', np.median([abs(r['rel_diff']) for r in compared]))
            if name.endswith('lowratio'):
                for r in records:
                    print('lowratio', r['inst'], r['k'], r['status'], 'obj', r['obj'], 'zK', r['zK_analysis'],
                          'relative difference', r.get('rel_diff'))
    rr = [S.ratio_of(r) for r in valid if S.rclass(r) == 'ratio']
    rr = [r for r in rr if r is not None]
    bracket = [r for r in rr if r['kind'] == 'bracket']
    print('table ratio records', len(rr), 'below 0.5', sum(r['r'] < .5 for r in rr))
    print('solver-reported brackets', len(bracket), 'max ratio upper estimate', max(r['r_hi'] for r in bracket))
    assert len(allrows) == 4785 and len(valid) == 4578
    assert len(rr) == 1067 and sum(r['r'] < .5 for r in rr) == 371
    lo = np.array([r['r'] for r in rr])
    hi = np.array([r['r_hi'] if r['kind'] == 'bracket' else r['r'] for r in rr])
    print('conditional bracket sensitivity: mean', hi.mean() - lo.mean(),
          'quantiles', np.quantile(hi, [.25, .5, .75]) - np.quantile(lo, [.25, .5, .75]))
    old, new = set(), set()
    for r in valid:
        if S.rclass(r) != 'ratio':
            continue
        key = r['inst'], r['k']
        zc = r['zC_scip'] if r['zC_scip'] is not None else r['zC_fixed']
        if zc is not None and np.isfinite(r['zK']) and r['zK'] > 0 and zc / r['zK'] < .5:
            old.add(key)
        ratio = S.ratio_of(r)
        if ratio is not None and ratio['r'] < .5:
            new.add(key)
    print('mechanism selection old/new', len(old), len(new))
    print('added records', sorted(new - old))
    print('removed records', sorted(old - new))
    status, restarted = collections.Counter(), []
    for path in sorted((LOGS / 'runs_minlplib').glob('*.log')):
        text = path.read_text()
        if 'time limit reached' in text:
            status['time limit'] += 1
        elif 'optimal solution found' in text:
            status['optimal'] += 1
        else:
            raise AssertionError(path)
        if 'restarting after' in text:
            restarted.append(path.stem)
    print('MINLPLib run statuses', dict(status), 'restarted', restarted)
    ex = [r for r in rows(LOGS / 'index/minlplib__ex1264.jsonl') if 'outcome' in r]
    before, after = [r for r in ex if r['lp'] < 113], [r for r in ex if r['lp'] == 113]
    oldexpr = {r['expr'] for r in before}
    print('ex1264 before restart max LP', max(r['lp'] for r in before),
          'max counter', max(r['exprncuts'] for r in before))
    for r in after:
        print('ex1264 LP 113', r['cons'], 'new expression', r['expr'] not in oldexpr, 'counter', r['exprncuts'])
        assert r['expr'] not in oldexpr and r['exprncuts'] == 0
    for name in ('summary', 'outcomes', 'lp_entry'):
        original = (LOGS / (name + '.log')).read_bytes()
        rerun = (LOGS / (name + '_after_r1.log')).read_bytes()
        assert original == rerun, name
        print('rerun byte-identical', name)
    original = (LOGS / 'explain_mismatch.log').read_bytes()
    assert original == (REVIEW / 'explain_mismatch_rerun.log').read_bytes()
    print('saved mismatch author/reviewer logs byte-identical')
    for line in original.decode().splitlines():
        if line.startswith('classes') or line.startswith('== bisection') or line.startswith('   rel diff max 0.000592'):
            print('saved mismatch statistic', line)
    fullspace = rows(REVIEW / 'gurobi_fullspace.jsonl')
    upper = [r for r in fullspace if r['zK_kind'] == 'upper']
    print('reviewer full-space upper-kind records', len(upper), dict(collections.Counter(r['status'] for r in upper)))
    for r in upper:
        if (r['inst'], r['k']) in {('waterund25', 410), ('waterund32', 1250), ('blend480', 365)}:
            print('reviewer inconsistent solver optimum', r['inst'], r['k'],
                  'obj', r['obj'], 'bound', r['bound'], 'stream zK', r['zK_stream'])
    for seed in (11, 12):
        certs = rows(LOGS / ('certify_two_ray_%d.log' % seed))
        assert all(r['lower_bound_certified'] and r['upper_bound_certified'] for r in certs)
        print('saved exact generator certificates', seed, len(certs))


def degeneracy_and_exact_point():
    mine = {(r['inst'], r['k']): r for path in sorted(REVIEW.glob('indep_check_*.jsonl')) for r in rows(path)}
    share, kinds, reached = [], collections.Counter(), 0
    with gzip.open(REVIEW / 'sample_records.jsonl.gz', 'rt') as f:
        for line in f:
            rec = json.loads(line)
            if rec['inst'] == 'waterund25' and rec['k'] == 410:
                exact_point(rec)
            if rec['set'] != 'minlplib' or not mine[(rec['inst'], rec['k'])].get('degenerate'):
                continue
            Q, b, c = D.quadratic(rec)
            P, w, _, _ = D.rays(rec)
            sbar = np.array(rec['zlp'])
            keep = ~D.fixed_rays(rec)
            zr = keep & (w <= 1e-9 * w[keep].max())
            share.append(zr.sum() / keep.sum())
            q0 = sbar @ Q @ sbar + b @ sbar + c
            g = 2 * Q @ sbar + b
            singles = []
            for j in np.where(zr)[0]:
                L, M = g @ P[:, j], P[:, j] @ Q @ P[:, j]
                if M < 0 or (L < 0 and L * L - 4 * M * q0 >= 0):
                    singles.append(j)
            reached += bool(singles)
            if singles:
                j = singles[0]
                kind = 'row slack' if rec['raylppos'][j] < 0 else (
                    'constraint variable' if rec['rayname'][j] in rec['vars'] else 'other variable')
                kinds[kind] += 1
    print('degenerate reviewer sample', len(share), 'single zero-rate ray reaches S', reached,
          'zero-rate share median', np.median(share), 'kinds', dict(kinds))
    assert reached == len(share) == 115


def exact_point(rec):
    Q, b, c = D.quadratic(rec)
    P, w, _, _ = D.rays(rec)
    keep = ~D.fixed_rays(rec)
    P, w = P[:, keep], w[keep]
    wf = np.maximum(w, 1e-9 * w.max())
    j = 62  # reviewer support-1 witness, among non-fixed rays
    sb, p = list(map(F, rec['zlp'])), list(map(F, P[:, j]))
    Qf = [[F(x) for x in row] for row in Q]
    bf, cf = list(map(F, b)), F(c)
    n = len(sb)
    q0 = sum(sb[a] * Qf[a][m] * sb[m] for a in range(n) for m in range(n)) + sum(bf[a] * sb[a] for a in range(n)) + cf
    L = sum(2 * sb[a] * Qf[a][m] * p[m] for a in range(n) for m in range(n)) + sum(bf[a] * p[a] for a in range(n))
    M = sum(p[a] * Qf[a][m] * p[m] for a in range(n) for m in range(n))
    t = F(43722.473165419404)
    for sign in (-1, 1):
        tau = t * (1 + F(sign, 10**9))
        q = q0 + L * tau + M * tau**2
        assert (q > 0) if sign < 0 else (q < 0)
        print('waterund25 k=410 exact rational check sign', sign, 'q', float(q), 'cost', float(F(wf[j]) * tau))
    print('exact-data root cost approx', float(F(wf[j]) * t), '(feasible upper bound; no global optimality certificate)')


if __name__ == '__main__':
    saved_results()
    degeneracy_and_exact_point()
    # Read every review artifact and record its hash so a confirming reviewer can check preservation.
    for path in sorted((ROOT / 'reviews').rglob('*')):
        if path.is_file():
            print('review artifact sha256', hashlib.sha256(path.read_bytes()).hexdigest(), path.relative_to(ROOT))
