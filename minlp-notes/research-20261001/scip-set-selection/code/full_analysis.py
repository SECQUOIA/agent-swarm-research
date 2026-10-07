"""Analyse completed full solves; never launch SCIP.

Usage: python3 code/full_analysis.py > logs/full_analysis.md
Writes parsed records and unrounded summaries to logs/full_analysis.json.
CPU means penalize every unsuccessful run at its logged CPU limit (300 s).
Node means use observed counts only, on a balanced subset of pairs when a
setting lacks statistics. Nodes on time-limited runs measure truncated work.
Pooled tests first average paired log differences over seeds per instance.
"""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import json
import math
import re

import numpy as np
from scipy.stats import binomtest, wilcoxon

from parse_logs import parse
from root_analysis import load_ref

BASE = Path(__file__).resolve().parent.parent
SETS = ('off', 'scip', 'corner', 'eff')


def solved(r):
    return (r.get('returncode') == '0' and not r['error']
            and 'optimal solution found' in (r['status'] or ''))


def sgm(values, shift):
    return math.expm1(float(np.mean(np.log(np.asarray(values) + shift)))
                      - math.log(shift)) * shift if len(values) else None


def signedrank(values):
    nz = np.asarray(values)[np.abs(values) > 1e-12]
    return dict(n=len(values), nonzero=len(nz),
                p=float(wilcoxon(nz, method='auto').pvalue) if len(nz) >= 10 else None)


def reference_flags(r, ref, tag, sense):
    i = r['inst']
    sign = -1 if sense[i] == 'max' else 1
    tol = 1e-6 * max(1, abs(ref[i]))
    flags = []
    if r['dual'] is not None and sign * (r['dual'] - ref[i]) > tol:
        flags.append('dual excludes feasible reference')
    if solved(r) and tag[i] == '=opt=' and abs(r['primal'] - ref[i]) > tol:
        flags.append('reported optimum differs from =opt= reference')
    if solved(r) and tag[i] == '=best=' and sign * (r['primal'] - ref[i]) > tol:
        flags.append('reported optimum worse than =best= feasible reference')
    return flags


def main():
    ref, tag, sense = load_ref()
    insts = [l.strip() for l in (BASE / 'logs/testset_full.txt').read_text().splitlines() if l.strip()]
    records = []
    for f in sorted((BASE / 'logs/full').glob('*.log')):
        r = parse(str(f))
        txt = f.read_text(errors='replace')
        r['limit'] = int(re.search(r'^limits/time = (\d+)$', txt, re.M)[1])
        assert 'timing/clocktype = 1' in txt
        r['reference_flags'] = reference_flags(r, ref, tag, sense)
        r['reference'] = ref[r['inst']]
        r['reference_tag'] = tag[r['inst']]
        records.append(r)
    seeds = sorted({r['seed'] for r in records})
    R = {(r['inst'], r['seed'], r['setting']): r for r in records}
    assert len(R) == len(records) == len(insts) * len(seeds) * len(SETS)
    assert set(R) == set(product(insts, seeds, SETS))
    assert {r['limit'] for r in records} == {300}
    summary = dict(records=records, tables=[], comparisons=[], seed_variation=[])
    allpairs = list(product(insts, seeds))
    print('# Completed full-solve analysis\n')
    print(f'{len(records)} logs; {len(insts)} instances; seeds {seeds}; settings {SETS}.')
    print('CPU limit 300 s; unsolved/error CPU observations count as 300 s. '
          'Node means use the same pairs for every setting, excluding a pair if any node count is missing. '
          'These include observed truncated work on time-limited runs.\n')
    print('Return codes:', dict(Counter(r['returncode'] for r in records)))
    print('Statuses:', dict(Counter(r['status'] for r in records)))
    print('\n## Aggregates\n')
    print('| scope | setting | runs | solved | errors / nonzero rc | time sgm | nodes n | nodes sgm | all-solved n | all-solved time sgm | all-solved nodes sgm |')
    print('|---|---|---|---|---|---|---|---|---|---|---|')

    def table(label, pairs):
        common = [p for p in pairs if all(solved(R[*p, s]) for s in SETS)]
        nodes = [p for p in pairs if all(R[*p, s]['nodes'] is not None for s in SETS)]
        for s in SETS:
            rs = [R[*p, s] for p in pairs]
            row = dict(scope=label, setting=s, runs=len(rs), solved=sum(map(solved, rs)),
                       errors=sum(r['error'] or r['returncode'] != '0' for r in rs),
                       time=sgm([r['time'] if solved(r) else r['limit'] for r in rs], 1),
                       nodes_n=len(nodes), nodes=sgm([R[*p, s]['nodes'] for p in nodes], 100),
                       common_n=len(common), common_time=sgm([R[*p, s]['time'] for p in common], 1),
                       common_nodes=sgm([R[*p, s]['nodes'] for p in common], 100))
            summary['tables'].append(row)
            print('| {scope} | {setting} | {runs} | {solved} | {errors} | {time:.3f} | {nodes_n} | {nodes:.3f} | {common_n} | {common_time:.3f} | {common_nodes:.3f} |'.format(**row))
        return common

    for sd in seeds:
        table(f'seed {sd}', [p for p in allpairs if p[1] == sd])
    common = table('all pairs', allpairs)
    failures = {p for p in allpairs if any(R[*p, s]['error'] or R[*p, s]['returncode'] != '0' for s in SETS)}
    table('exclude failure pair', [p for p in allpairs if p not in failures])
    suspect = {r['inst'] for r in records if r['reference_flags']}
    table('exclude flagged instance', [p for p in allpairs if p[0] not in suspect])

    print('\n## Reference and error audit\n')
    for r in records:
        if r['reference_flags'] or r['error'] or r['returncode'] != '0':
            print(f"- {r['log']}: status={r['status']}; rc={r['returncode']}; "
                  f"primal={r['primal']}; dual={r['dual']}; reference={r['reference']} "
                  f"{r['reference_tag']}; flags={r['reference_flags']}")
    print('Final dual bounds excluding reference:', sum('dual excludes feasible reference' in r['reference_flags'] for r in records))
    print('Reported optimum mismatches at relative tolerance 1e-4:',
          sum(solved(r) and tag[r['inst']] == '=opt=' and abs(r['primal'] - ref[r['inst']]) > 1e-4 * max(1, abs(ref[r['inst']])) for r in records))

    print('\n## Paired comparisons\n')
    print('Ratios are geometric means of (X+shift)/(Y+shift), so <1 favours X. '
          'Tests use paired log ratios, with zero differences dropped. All-pair CPU uses the 300 s penalty; '
          'nodes are tested only on solved subsets. Per-seed p values treat instances as observations; '
          'pooled p values average the two log ratios within each instance first. '
          'Tests are exploratory, without multiplicity adjustment.\n')
    print('| scope | subset | X vs Y | n pairs | CPU shifted ratio | faster / slower >10% | CPU Wilcoxon n / p | node shifted ratio | nodes Wilcoxon n / p | solved only X / only Y | exact solved-count p |')
    print('|---|---|---|---|---|---|---|---|---|---|---|')
    for sd in [*seeds, None]:
        scope = f'seed {sd}' if sd else 'all pairs (instance-averaged tests)'
        pairs = [p for p in allpairs if sd is None or p[1] == sd]
        for a, b in combinations(SETS, 2):
            # Orient all comparisons as enabled vs off, or searched vs SCIP.
            a, b = b, a
            only_a = sum(solved(R[*p, a]) and not solved(R[*p, b]) for p in pairs)
            only_b = sum(solved(R[*p, b]) and not solved(R[*p, a]) for p in pairs)
            bp = float(binomtest(only_a, only_a + only_b).pvalue) if sd and only_a + only_b else None
            for subset in ('all', 'all settings solved', 'pair solved'):
                selected = [p for p in pairs if subset == 'all' or
                            (p in common if subset == 'all settings solved' else solved(R[*p, a]) and solved(R[*p, b]))]
                def diffs(key, shift):
                    out = []
                    for p in selected:
                        ra, rb = R[*p, a], R[*p, b]
                        va = ra['time'] if solved(ra) else ra['limit']
                        vb = rb['time'] if solved(rb) else rb['limit']
                        if key == 'nodes':
                            va, vb = ra[key], rb[key]
                        out.append((p[0], math.log((va + shift) / (vb + shift))))
                    return out
                dt = diffs('time', 1)
                dn = diffs('nodes', 100) if subset != 'all' else []
                def test(d):
                    if sd is not None:
                        return signedrank([v for _, v in d])
                    return signedrank([np.mean([v for j, v in d if j == i]) for i in sorted({j for j, _ in d})])
                tr, nr = test(dt), test(dn)
                row = dict(scope=scope, subset=subset, a=a, b=b, pairs=len(selected),
                           time_ratio=math.exp(np.mean([v for _, v in dt])), time_test=tr,
                           faster=sum(v < -math.log(1.1) for _, v in dt), slower=sum(v > math.log(1.1) for _, v in dt),
                           node_ratio=math.exp(np.mean([v for _, v in dn])) if dn else None, node_test=nr,
                           only_a=only_a, only_b=only_b, solved_count_p=bp)
                summary['comparisons'].append(row)
                def fmt_p(t):
                    return f"{t['n']} / {t['p']:.4g}" if t['p'] is not None else f"{t['n']} / —"
                node_ratio = f"{row['node_ratio']:.4f}" if dn else '—'
                print(f"| {scope} | {subset} | {a} vs {b} | {len(selected)} | {row['time_ratio']:.4f} | "
                      f"{row['faster']} / {row['slower']} | {fmt_p(tr)} | "
                      f"{node_ratio}", end='')
                print(f" | {fmt_p(nr)} | {only_a} / {only_b} | {bp:.4g} |" if bp is not None else
                      f" | {fmt_p(nr)} | {only_a} / {only_b} | — |")

    print('\n## Seed-to-seed variability\n')
    print('| setting | solved both | solved seed 1 only / seed 2 only | shifted CPU ratio seed 2 / 1 | median absolute log CPU ratio | CPU differs >10% | shifted node ratio seed 2 / 1 | median absolute log node ratio | nodes differ >10% |')
    print('|---|---|---|---|---|---|---|---|---|')
    assert seeds == [1, 2]
    for s in SETS:
        both = [i for i in insts if all(solved(R[i, sd, s]) for sd in seeds)]
        dt = [math.log((R[i, 2, s]['time'] + 1) / (R[i, 1, s]['time'] + 1)) for i in both]
        dn = [math.log((R[i, 2, s]['nodes'] + 100) / (R[i, 1, s]['nodes'] + 100)) for i in both]
        row = dict(setting=s, n=len(both), seed1_only=sum(solved(R[i, 1, s]) and not solved(R[i, 2, s]) for i in insts),
                   seed2_only=sum(solved(R[i, 2, s]) and not solved(R[i, 1, s]) for i in insts),
                   time_ratio=math.exp(np.mean(dt)), time_median_abs_log=float(np.median(np.abs(dt))),
                   time_changes=sum(abs(v) > math.log(1.1) for v in dt), node_ratio=math.exp(np.mean(dn)),
                   node_median_abs_log=float(np.median(np.abs(dn))), node_changes=sum(abs(v) > math.log(1.1) for v in dn))
        summary['seed_variation'].append(row)
        print('| {setting} | {n} | {seed1_only} / {seed2_only} | {time_ratio:.4f} | {time_median_abs_log:.4f} | {time_changes} | {node_ratio:.4f} | {node_median_abs_log:.4f} | {node_changes} |'.format(**row))

    print('\n## Per-instance observations\n')
    print('| instance | seed | off CPU / nodes | scip CPU / nodes | corner CPU / nodes | eff CPU / nodes |')
    print('|---|---|---|---|---|---|')
    for i, sd in allpairs:
        cells = []
        for s in SETS:
            r = R[i, sd, s]
            prefix = '' if solved(r) else 'TL ' if 'time limit' in (r['status'] or '') else 'ERROR '
            cells.append(f"{prefix}{r['time']} / {r['nodes']}")
        print(f"| {i} | {sd} | " + ' | '.join(cells) + ' |')
    def clean(value):
        if isinstance(value, dict):
            return {k: clean(v) for k, v in value.items()}
        if isinstance(value, list):
            return [clean(v) for v in value]
        if isinstance(value, float) and not math.isfinite(value):
            return str(value)
        return value
    (BASE / 'logs/full_analysis.json').write_text(json.dumps(clean(summary), indent=2, allow_nan=False) + '\n')


if __name__ == '__main__':
    main()
