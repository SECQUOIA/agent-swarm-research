"""Round-3 recovery check using existing trajectories only.

For a switching rule, compare its change in fraction of the root gap closed
with continued orbit rounds on the same instances:
    (rule - orbit)(20) - (rule - orbit)(start).
Positive means that switching gains over continued orbit rounds. Also print
the changes against SCIP to distinguish these from compression of a deficit.
Use starts 3, 5 and 10; start 5 excludes all orbit rounds of o5s.
Holm adjustments cover the 12 contrasts per span (4 rules, 2 sizes and pooled),
and, as a sensitivity check, all 36 contrasts across the three spans.
These are exploratory comparisons; intervals are unadjusted paired t-intervals.
Usage: python3 analyze_rev3.py (paths are relative to this script).
"""

from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

import recio


LOGS = Path(__file__).resolve().parent.parent / 'logs'
SIZES = ('6x8', '10x20')
RULES = ('first_orbit', 'o2s', 'o3s', 'o5s')
STARTS = (3, 5, 10)
GROUPS = (('6x8', ('6x8',)), ('10x20', ('10x20',)), ('pooled', SIZES))


def summary(values):
    values = np.asarray(values, dtype=float)
    n = len(values)
    assert n > 1 and np.isfinite(values).all()
    mean = values.mean()
    se = values.std(ddof=1) / np.sqrt(n)
    half = stats.t.ppf(0.975, n - 1) * se
    p = float(stats.ttest_1samp(values, 0).pvalue) if se else float(mean == 0)
    return mean, mean - half, mean + half, p


def holm(pvalues):
    order = sorted(pvalues, key=pvalues.get)
    adjusted = {}
    previous = 0.0
    for rank, key in enumerate(order):
        previous = max(previous, min(1.0, (len(order) - rank) * pvalues[key]))
        adjusted[key] = previous
    return adjusted


def main():
    trajectories = defaultdict(dict)
    nfiles = nrecords = nduplicates = 0
    for size in SIZES:
        for directory, prefix in (('main', 'main'), ('new', 'new'),
                                  ('rev1', 'rev1'), ('rev1', 'rev1b')):
            pattern = str(LOGS / directory / f'{prefix}_{size}_*.jsonl')
            for path in recio.files(pattern):
                nfiles += 1
                for _, record in recio.records(path):
                    nrecords += 1
                    assert record['status'] == 'ok', (path, record['inst'], record['rule'])
                    rule = record['rule']
                    if rule not in RULES + ('scip', 'orbit'):
                        continue
                    key = (size, record['inst'])
                    closed = np.asarray(record['closed'], dtype=float)
                    assert len(closed) == 21 and np.isfinite(closed).all(), (path, key, rule)
                    if key in trajectories[rule]:
                        assert np.array_equal(trajectories[rule][key], closed), (path, key, rule)
                        nduplicates += 1
                    trajectories[rule][key] = closed
    print(f'Input: {nfiles} files, {nrecords} records; '
          f'{nduplicates} duplicate selected trajectories checked, 0 differing')
    scip = trajectories['scip']
    assert len(scip) == 110
    assert all(set(trajectories[rule]) == set(scip) for rule in RULES + ('orbit',))
    results = {}
    for label, sizes in GROUPS:
        keys = sorted(key for key in scip if key[0] in sizes)
        expected = {'6x8': 60, '10x20': 50, 'pooled': 110}[label]
        assert len(keys) == expected
        print(f'\n== {label} (n {len(keys)}): changes against SCIP, unadjusted')
        print('SCIP mean remaining root gap: ' + ', '.join(
            f'r{r} {np.mean([1 - scip[key][r] for key in keys]):.7f}' for r in (3, 5, 10, 20)))
        for rule in RULES + ('orbit',):
            display = 'o1s' if rule == 'first_orbit' else rule
            for start in STARTS:
                deficit_change = np.array([
                    (trajectories[rule][key][20] - scip[key][20])
                    - (trajectories[rule][key][start] - scip[key][start]) for key in keys])
                mean, low, high, p = summary(deficit_change)
                print(f'{display:5s} {start:2d}->20: {mean:+.7f} [{low:+.7f}, {high:+.7f}] p {p:.7f}')
                if rule == 'orbit':
                    continue
                contrast = np.array([
                    (trajectories[rule][key][20] - trajectories['orbit'][key][20])
                    - (trajectories[rule][key][start] - trajectories['orbit'][key][start])
                    for key in keys])
                orbit_change = np.array([
                    (trajectories['orbit'][key][20] - scip[key][20])
                    - (trajectories['orbit'][key][start] - scip[key][start]) for key in keys])
                assert np.allclose(contrast, deficit_change - orbit_change, atol=1e-14, rtol=0)
                results[(start, label, rule)] = summary(contrast)
    all_holm = holm({key: result[3] for key, result in results.items()})
    for start in STARTS:
        span_holm = holm({key: result[3] for key, result in results.items() if key[0] == start})
        print(f'\n== Control contrast {start}->20: (rule - orbit)(20) - (rule - orbit)({start})')
        print('95% paired t-intervals; p raw; Holm12 for this span; Holm36 across all spans')
        for label, _ in GROUPS:
            for rule in RULES:
                key = (start, label, rule)
                mean, low, high, p = results[key]
                display = 'o1s' if rule == 'first_orbit' else rule
                print(f'{label:7s} {display:3s}: {mean:+.7f} [{low:+.7f}, {high:+.7f}] '
                      f'p {p:.7f} Holm12 {span_holm[key]:.7f} Holm36 {all_holm[key]:.7f}')
    print('\nALL PASS: matched instance sets, finite 21-state trajectories, identical duplicates, '
          'and both formulas for each paired control contrast')


if __name__ == '__main__':
    main()
