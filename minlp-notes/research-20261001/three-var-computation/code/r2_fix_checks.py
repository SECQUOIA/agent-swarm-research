"""Recompute round-2 corrections from saved records, without solving an SDP.

The strict-bound calculation follows reviews/r2-code/r2_strict_bounds.py.
Run from the stream directory: timeout 60 python code/r2_fix_checks.py
"""
import itertools
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent


def emit(topic, **values):
    print(json.dumps(dict(topic=topic, **values)))


def residuals(x, Y, triples):
    i, j, k = triples.T
    triangle = np.maximum.reduce([
        Y[i, j] + Y[i, k] - x[i] - Y[j, k],
        Y[i, j] + Y[j, k] - x[j] - Y[i, k],
        Y[i, k] + Y[j, k] - x[k] - Y[i, j],
        x[i] + x[j] + x[k] - Y[i, j] - Y[i, k] - Y[j, k] - 1,
    ])
    cap = np.diag(Y) - x
    return triangle, cap, cap[triples].max(axis=1)


def strict_bounds():
    name = 'spar090-075-1'
    with np.load(ROOT / 'logs/strict_r1' / (name + '.base.npz')) as z:
        x, Y = z['x'], z['Y']
        info = json.loads(str(z['info']))
    with np.load(ROOT / 'logs/strict_r1' / (name + '.depth.npz')) as z:
        depths = z['depths']
    triples = np.array(list(itertools.combinations(range(len(x)), 3)))
    assert len(depths) == len(triples) == 117480
    assert np.isfinite(depths).all()
    tv, cap, capT = residuals(x, Y, triples)
    # The triangle and cap polynomials have uniform means 1/4 and 1/6.
    bound = np.minimum(-4 * tv, -6 * capT)
    # Here every triple has a positive cap residual, so clipping in the
    # reviewer's calculation leaves these bounds unchanged.
    assert np.all(capT > 0)
    worst = int(np.argmin(bound))
    assert triples[worst].tolist() == [0, 11, 47]
    assert bound.min() < depths.min()
    assert int((depths > bound + 1e-9).sum()) == 73615
    source = next((ROOT / 'sources/BoxQP_instances-master').glob('*/' + name + '.in'))
    tok = source.read_text().split()
    n, v = int(tok[0]), np.array(tok[1:], float)
    H, g = -v[n:].reshape(n, n) / 2, -v[:n]
    fc = np.trace(H) / 3 + (H.sum() - np.trace(H)) / 4 + g.sum() / 2
    optima = {}
    for line in (ROOT / 'sources/BoxQP_instances-master/README.txt').read_text().splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[0].startswith('spar'):
            optima[parts[0]] = -float(parts[1])
    gap = optima[name] - info['B_safe']
    margin = info['B'] - info['B_safe']
    emit('strict depths', stored_min=float(depths.min()), exact_min_upper_bound=float(bound.min()),
         triple=triples[worst].tolist(), triangle_residual=float(tv[worst]),
         max_stored_excess=float((depths - bound).max()),
         triples_above_bound_plus_1e9=int((depths > bound + 1e-9).sum()),
         gap=gap, primal_to_safe_margin=margin)
    for assumption, eps in (
        ('computed depths', max(0, -float(depths.min()))),
        ('exact triangle/cap bound: lower bound on gain term', -float(bound.min())),
        ('exact minimum depth >= -1e-7', 1e-7),
        ('each stored depth overestimates exact depth by <= 1e-7', 1e-7 - float(depths.min())),
    ):
        gain = eps * (fc - info['B']) / (1 + eps)
        emit('strict gain sensitivity', assumption=assumption, eps=eps, gain=gain,
             percent_of_gap=100 * gain / gap, percent_with_margin=100 * (gain + margin) / gap)
    return optima


def cost_split():
    for kind in ('chain', 'cactus'):
        ratios, shares = [], []
        for path in sorted((ROOT / 'logs' / kind).glob(kind + '_*.jsonl')):
            by = {}
            for line in path.read_text().splitlines():
                r = json.loads(line)
                by.setdefault(r['method'], []).append(r)
            separate = 'XF' not in by
            if separate:
                xf = ROOT / 'logs/chain' / ('xf_' + path.name)
                for line in xf.read_text().splitlines():
                    r = json.loads(line)
                    if r['method'] == 'XF':
                        by.setdefault('XF', []).append(r)
            # Exclude the shared base record, as method_table.stage does.
            times = {m: sum(r['time_solve'] for r in by[m][1:]) for m in ('F', 'XF', 'X')}
            F, XF, X = (times[m] for m in ('F', 'XF', 'X'))
            share = math.log(X / XF) / math.log(X / F)
            msize = int(path.stem.split('_m')[1].split('_')[0])
            if kind == 'cactus' or msize >= 300:
                ratios.append(XF / F)
                shares.append(share)
            emit('cost split', instance=path.stem, solve_seconds=times, XF_over_F=XF / F,
                 X_over_XF=X / XF, selection_share_of_log_ratio=share, separate_XF_run=separate,
                 blocks={m: by[m][-1]['size']['F' if m == 'F' else 'X'] for m in times})
        emit('cost ranges', kind=kind, scope='all cacti' if kind == 'cactus' else 'm >= 300',
             XF_over_F=[min(ratios), max(ratios)], selection_share=[min(shares), max(shares)])


def original_sets(optima):
    records = {}
    for directory in ('audit', 'spar_audit'):
        for p in (ROOT / 'logs' / directory).glob('spar*.json'):
            if not p.name.endswith('.tri.json'):
                r = json.loads(p.read_text())
                records[r['name']] = r
    deep = {'spar090-075-1', 'spar100-050-1', 'spar100-050-2', 'spar125-050-1'}
    other_original = sorted(set(records) - deep)
    larger_gap = sorted(name for name, r in records.items() if name != 'spar090-075-1'
                        and (optima[name] - r['B_safe']) / abs(optima[name]) > 1e-5)
    assert len(other_original) == len(larger_gap) == 13
    assert set(larger_gap) - set(other_original) == deep - {'spar090-075-1'}
    emit('two sets of 13', other_original=other_original, larger_gap_except_strict=larger_gap)


def optional_residues():
    name = 'spar125-050-1'
    base = ROOT / 'logs/spar_audit' / (name + '.json')
    with np.load(str(base) + '.base.npz') as z:
        x, Y = z['x'], z['Y']
    with np.load(str(base) + '.depth.npz') as z:
        depths = z['depths']
    triples = np.array(list(itertools.combinations(range(len(x)), 3)))
    tv, cap, capT = residuals(x, Y, triples)
    emit('original cap residues', name=name, positive_caps=int((cap > 0).sum()),
         max_cap=float(cap.max()), triangle_feasible_min_depth=float(depths[tv <= 0].min()),
         triangle_feasible_min_cap_bound=float((-6 * capT)[tv <= 0].min()),
         median_depth=float(np.median(depths)), triples_below_minus_1e7=int((depths < -1e-7).sum()),
         triples=len(triples))
    r = json.loads((ROOT / 'logs/audit/cactus_m300_s1.json').read_text())
    w = min(r['worst'], key=lambda w: w['depth'])
    M = np.array(w['M'])
    tv, _, _ = residuals(M[0, 1:], M[1:, 1:], np.array([[0, 1, 2]]))
    depth, tri_bound = w['depth'], -4 * float(tv[0])
    assert depth == r['min_depth']
    # Compare at the displayed precision; the saved solver depth is not exact.
    assert abs(depth - tri_bound) < 0.001 * abs(tri_bound)
    emit('cactus final triangle', triple=w['triple'], stored_depth=depth,
         triangle_residual=float(tv[0]), normalized_triangle_bound=tri_bound,
         depth_minus_bound=depth - tri_bound, depth_over_bound=depth / tri_bound)


if __name__ == '__main__':
    optima = strict_bounds()
    cost_split()
    original_sets(optima)
    optional_residues()
    print('PASS: round-2 quantities reproduced from saved records; no SDP solved')
