"""Recompute the sampled dynamism distribution from the saved SCIP dumps.

The analysis files identify the sampled attempts, but restriction coefficients below are
read from the raw dumps. The rounding diagnostic adapts reviews/r1-code/dyn_noise.py on
the reviewer's saved sample. Its 1e-12 dot-product tolerance is a heuristic, not an exact
zero test or a representative estimate of all aborts. Usage: python3 -B dynamism_after_r1.py
"""
import collections
import gzip
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT / 'logs'


def restriction_ratio(coefs):
    v = np.abs(np.array(coefs[:3], float))
    nz = v[v != 0]
    return float(nz.min() / nz.max()) if nz.size else 1.0


def distribution():
    wanted = collections.defaultdict(dict)
    for dirname in ('an_minlplib', 'an_minlplib2'):
        for path in sorted((LOGS / dirname).glob('*.jsonl')):
            for line in path.open():
                row = json.loads(line)
                if row.get('fail') == 'numerics':
                    wanted[row['inst']][row['k']] = row
    ratios = collections.defaultdict(list)
    for inst, rows in sorted(wanted.items()):
        found = set()
        with gzip.open(LOGS / 'runs_minlplib' / (inst + '.jsonl.gz'), 'rt') as f:
            k = -1
            for line in f:
                if not line.startswith('{"v":'):
                    continue
                k += 1
                if k not in rows:
                    continue
                rec = json.loads(line)
                assert rec['fail'] == 'numerics'
                assert rec['nbadray1'] - rec['nbadray0'] == 1
                e, = [e for e in rec['perray'] if e.get('fail')]
                assert e['i'] == rows[k]['fail_ray']
                ra = restriction_ratio(e['c1234a'])
                piece = '1-3/4a' if ra <= 1e-15 else '4b'
                ratio = ra if piece == '1-3/4a' else restriction_ratio(e['c4b'])
                assert ratio <= 1e-15
                if piece == '1-3/4a':
                    assert ra == rows[k]['fail_minabc'] / rows[k]['fail_maxabc']
                ratios[piece].append(ratio)
                found.add(k)
                if len(found) == len(rows):
                    break
        assert found == rows.keys(), (inst, rows.keys() - found)
        print('dump checked', inst, len(found), flush=True)
    print('sampled dynamism aborts', sum(map(len, ratios.values())))
    for piece, vals in ratios.items():
        v = np.array(vals)
        print('piece', piece, 'n', len(v), 'quantiles 10/50/90%', np.quantile(v, [.1, .5, .9]))
        for threshold in (1e-30, 1e-25, 1e-20, 1e-17, 1e-15):
            count = int(np.sum(v < threshold))
            print('min/max <', threshold, count, '/', len(v), '=', count / len(v))


def rounding_diagnostic():
    groups = collections.defaultdict(list)
    other_piece = 0
    sample = ROOT / 'reviews/r1-logs/sample_records.jsonl.gz'
    with gzip.open(sample, 'rt') as f:
        for line in f:
            rec = json.loads(line)
            if rec.get('fail') != 'numerics' or rec['set'] != 'minlplib':
                continue
            e, = [e for e in rec['perray'] if e.get('fail')]
            ratio = restriction_ratio(e['c1234a'])
            if ratio > 1e-15:
                other_piece += 1
                continue
            nq, sf = rec['nquad'], rec['sidefactor']
            th = sf * np.array(rec['eigval'], float)
            V = np.array(rec['eigvec'], float).reshape(nq, nq)
            ray = np.zeros(rec['nv'])
            for k, value in rec['rays'][e['i']]:
                ray[k] = value
            comp = V @ ray[:nq]
            scale = np.abs(V) @ np.abs(ray[:nq])
            neg, zero = th < -1e-9, np.abs(th) <= 1e-9
            consistent = bool(np.all(np.abs(comp[neg]) <= 1e-12 * np.maximum(scale[neg], 1e-300)))
            if rec['case4']:
                vb = np.array(rec['vb'], float)
                terms = list(vb[zero] * comp[zero])
                scales = list(np.abs(vb[zero]) * scale[zero])
                linear = sf * np.array(rec['lincoefs'], float) * ray[nq:nq + rec['nlin']]
                terms.extend(linear)
                scales.extend(np.abs(linear))
                if rec['auxvar'] is not None:
                    terms.append(-sf * ray[-1])
                    scales.append(abs(ray[-1]))
                consistent &= abs(sum(terms)) <= 1e-12 * max(sum(scales), 1e-300)
            key = 'A,B consistent with zero at tolerance' if consistent else 'components above tolerance'
            groups[key].append(ratio)
    print('rounding diagnostic: other-piece aborts excluded', other_piece)
    total = sum(map(len, groups.values()))
    for key, vals in groups.items():
        print(key, len(vals), '/', total, '=', len(vals) / total,
              'ratio quantiles 10/50/90%', np.quantile(vals, [.1, .5, .9]))


if __name__ == '__main__':
    distribution()
    rounding_diagnostic()
