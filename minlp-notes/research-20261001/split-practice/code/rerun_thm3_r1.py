"""Rerun only Theorem 3 on all 113 selected rank-at-most-12 stored points.

Keep the original pivot-row rationalization for comparison. Also check the
first-column grid neighbour at fractional rank-1 roots, as in review r1.
Write exact rational values and vectors; all timings include shortening.
Usage from split-practice/: python3 code/rerun_thm3_r1.py OUT.jsonl
"""
import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path

import numpy as np

from exp_separate import rationalize_rank
from lattice import thm3_exact, q_exact

ROOT = Path(__file__).resolve().parents[1]


def run(Y, r, first_column=False):
    start = time.monotonic()
    if first_column:
        p = [F(1)] + [F(round(float(a) * 10**6), 10**6)
                         for a in Y[0, 1:] / Y[0, 0]]
        X = [[a * b for b in p] for a in p]
        fac = ([p], [[F(1)]])
        err = float(np.max(np.abs(np.array(X, float) - Y)))
    else:
        X, err, fac = rationalize_rank(Y, r)
    rat_time = time.monotonic() - start
    res = thm3_exact(X, max_nodes=2 * 10**6, factor=fac)
    v = res['v']
    if v is not None:
        assert q_exact(X, v) == res['q']
        YF = [[F(float(a)) for a in row] for row in Y]
        qe = q_exact(YF, v)
        res.update(q_at_Y=float(qe), q_at_Y_exact=str(qe),
                   supp=sum(a != 0 for a in v[1:]),
                   ratio_at_Y=float(-qe / sum(a * a for a in v[1:])))
    else:
        res.update(q_at_Y=None, supp=None, ratio_at_Y=None)
    res.update(q_exact=str(res['q']), q=float(res['q']), err=err,
               rationalization_time=rat_time, total_time=time.monotonic() - start)
    return res


if __name__ == '__main__':
    records = [json.loads(line) for k in range(3)
               for line in (ROOT / f'logs/sep_run2_s{k}.jsonl').read_text().splitlines()]
    with open(sys.argv[1], 'w') as out:
        for d in records:
            r = d['rank']['1e-05']
            if r > 12:
                continue
            file = d['file']
            size = file.split('_n')[1].split('_')[0]
            family = 'BT' if file.startswith('bt') else 'DM'
            Y = np.load(ROOT / f'data/points_{family}{size}' / file)['Y']
            Y = (Y + Y.T) / 2
            rec = dict(file=file, rank=r)
            try:
                rec['thm3'] = run(Y, r)
                if r == 1 and file.endswith('root.npz'):
                    rec['rank1_grid'] = run(Y, 1, first_column=True)
            except Exception as e:
                rec['error'] = f'{type(e).__name__}: {e}'
            out.write(json.dumps(rec) + '\n')
            out.flush()
            print(file, 'error' if 'error' in rec else
                  {k: rec['thm3'].get(k) for k in ('q', 'vmax', 'supp', 'q_at_Y', 'first_complete', 'second_complete', 'total_time')}, flush=True)
