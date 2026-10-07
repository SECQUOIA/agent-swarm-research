"""Compare the 120 stock runs with archived off and patched point-rule runs.

Usage: python3 code/stock_analysis_r1.py > logs/stock_analysis_r1.md
Writes records, aggregates, paired tests, path differences and load to JSON.
CPU/node measures and pooled tests match full_analysis.py (Section 5).
"""
from collections import Counter
from itertools import product
from pathlib import Path
import json
import math
import re

import numpy as np

from full_analysis import solved, sgm, signedrank, reference_flags
from parse_logs import parse
from root_analysis import load_ref

BASE = Path(__file__).resolve().parent.parent
SETS = ('off', 'stock-scip', 'patched-scip', 'corner', 'eff')


def main():
    instances = (BASE / 'logs/testset_full.txt').read_text().split()
    pairs = list(product(instances, (1, 2)))
    ref, tag, sense = load_ref()
    records = []
    signatures = {}
    for setting in SETS:
        directory = 'full_stock' if setting == 'stock-scip' else 'full'
        label = 'scip' if setting in ('stock-scip', 'patched-scip') else setting
        for inst, seed in pairs:
            path = BASE / f'logs/{directory}/{inst}.{label}.s{seed}.log'
            text = path.read_text()
            record = parse(str(path))
            record.update(setting=setting, limit=300, path=str(path.relative_to(BASE)))
            assert 'timing/clocktype = 1' in text and 'limits/time = 300' in text
            assert f'randomization/permutationseed = {seed}' in text
            assert 'limits/memory = 6000' in text
            if setting == 'stock-scip':
                assert record['returncode'] == '0' and not record['error']
                assert record['status'] and record['nodes'] is not None
                assert 'Quadratic SetSel' not in text
                assert 'nlhdlr/quadratic/useintersectioncuts = TRUE' in text
            record['reference_flags'] = reference_flags(record, ref, tag, sense)
            records.append(record)
            fields = ('status', 'nodes', 'primal', 'dual', 'firstlp', 'rootdual', 'gencuts', 'addcuts')
            signature = {key: record.get(key) for key in fields}
            for key in ('primal LP', 'dual LP'):
                found = re.findall(r'\n  ' + key + r'\s*:\s*\S+\s+(\d+)\s+(\d+)', text)
                signature[key] = found[-1] if found else None
            signatures[inst, seed, setting] = signature
    R = {(r['inst'], r['seed'], r['setting']): r for r in records}
    report = dict(records=records, tables=[], comparisons=[], path_differences=[])
    print('# Stock rerun after review round 1\n')
    print('120 stock runs; same 300 CPU-second limit, clock type 1 and seeds 1/2. '
          'Unsolved/error CPU counts as 300 s; shifts: CPU 1 s, nodes 100. '
          'All-setting subsets use all five settings. Truncated node counts measure '
          'work performed, not effort to solve an unsolved instance.\n')
    print('Stock statuses:', dict(Counter(R[*p, 'stock-scip']['status'] for p in pairs)))
    print('Stock return codes:', dict(Counter(R[*p, 'stock-scip']['returncode'] for p in pairs)))
    print('\n| scope | setting | solved / runs | CPU sgm | nodes n / sgm | all-five-solved n | CPU / nodes sgm there |')
    print('|---|---|---|---|---|---|---|')
    for scope, selected in [('seed 1', [p for p in pairs if p[1] == 1]),
                            ('seed 2', [p for p in pairs if p[1] == 2]),
                            ('pooled', pairs),
                            ('exclude off failure', [p for p in pairs if p != ('ex5_4_2', 1)])]:
        common = [p for p in selected if all(solved(R[*p, s]) for s in SETS)]
        nodes = [p for p in selected if all(R[*p, s]['nodes'] is not None for s in SETS)]
        for setting in SETS:
            rs = [R[*p, setting] for p in selected]
            row = dict(scope=scope, setting=setting, solved=sum(map(solved, rs)), n=len(rs),
                cpu=sgm([r['time'] if solved(r) else 300 for r in rs], 1), nodes_n=len(nodes),
                nodes=sgm([R[*p, setting]['nodes'] for p in nodes], 100), common_n=len(common),
                common_cpu=sgm([R[*p, setting]['time'] for p in common], 1),
                common_nodes=sgm([R[*p, setting]['nodes'] for p in common], 100))
            report['tables'].append(row)
            print('| {scope} | {setting} | {solved} / {n} | {cpu:.3f} | {nodes_n} / {nodes:.1f} | {common_n} | {common_cpu:.3f} / {common_nodes:.1f} |'.format(**row))
    print('\nP-values are exploratory. Pooled tests average the seed log ratios within '
          'each instance before testing; pair-solved subsets may differ by comparison. '
          'Tests with fewer than ten nonzero differences are not reported (—).\n')
    print('| scope | subset | X vs Y | n pairs / instances | CPU shifted ratio / p | nodes shifted ratio / p | only X / only Y solved |')
    print('|---|---|---|---|---|---|---|')
    def test(differences, selected, seed):
        if seed:
            return signedrank(differences)
        values = [float(np.mean([v for p, v in zip(selected, differences) if p[0] == i]))
                  for i in sorted({p[0] for p in selected})]
        return signedrank(values)
    for seed in (1, 2, None):
        selected = [p for p in pairs if seed is None or p[1] == seed]
        for a, b in (('stock-scip', 'off'), ('patched-scip', 'stock-scip')):
            only_a = [p for p in selected if solved(R[*p, a]) and not solved(R[*p, b])]
            only_b = [p for p in selected if solved(R[*p, b]) and not solved(R[*p, a])]
            for subset in ('all', 'pair solved', 'all five solved', 'exclude off failure'):
                keys = [p for p in selected if subset == 'all' or
                        (subset == 'pair solved' and solved(R[*p, a]) and solved(R[*p, b])) or
                        (subset == 'all five solved' and all(solved(R[*p, s]) for s in SETS)) or
                        (subset == 'exclude off failure' and p != ('ex5_4_2', 1))]
                dt = [math.log(((R[*p, a]['time'] if solved(R[*p, a]) else 300)+1) /
                               ((R[*p, b]['time'] if solved(R[*p, b]) else 300)+1)) for p in keys]
                dn = [math.log((R[*p, a]['nodes']+100)/(R[*p, b]['nodes']+100)) for p in keys] if subset in ('pair solved', 'all five solved') else []
                row = dict(scope=f'seed {seed}' if seed else 'pooled', a=a, b=b, subset=subset,
                    n=len(keys), instances=len({p[0] for p in keys}), cpu_ratio=math.exp(float(np.mean(dt))),
                    cpu_test=test(dt, keys, seed), node_ratio=math.exp(float(np.mean(dn))) if dn else None,
                    node_test=test(dn, keys, seed) if dn else None, only_a=only_a, only_b=only_b)
                report['comparisons'].append(row)
                def fmt_p(value):
                    return f'{value:.4g}' if value is not None else '—'
                node_text = f"{row['node_ratio']:.4f} / {fmt_p(row['node_test']['p'])}" if dn else '—'
                print(f"| {row['scope']} | {subset} | {a} vs {b} | {len(keys)} / {row['instances']} | {row['cpu_ratio']:.4f} / {fmt_p(row['cpu_test']['p'])} | {node_text} | {len(only_a)} / {len(only_b)} |")
    for p in pairs:
        a, b = signatures[*p, 'patched-scip'], signatures[*p, 'stock-scip']
        changed = {key: [a[key], b[key]] for key in a if a[key] != b[key]}
        if changed:
            report['path_differences'].append(dict(instance=p[0], seed=p[1], differences=changed))
    report['both_solved_path_differences'] = [r for r in report['path_differences'] if
        solved(R[r['instance'], r['seed'], 'stock-scip']) and
        solved(R[r['instance'], r['seed'], 'patched-scip'])]
    report['root_differences'] = [dict(instance=p[0], seed=p[1], stock=R[*p, 'stock-scip']['rootdual'],
                                      patched=R[*p, 'patched-scip']['rootdual']) for p in pairs if
                                 (R[*p, 'stock-scip']['firstlp'], R[*p, 'stock-scip']['rootdual']) !=
                                 (R[*p, 'patched-scip']['firstlp'], R[*p, 'patched-scip']['rootdual'])]
    report['root_available_pairs'] = sum(all(R[*p, s][key] is not None for s in ('stock-scip', 'patched-scip')
                                            for key in ('firstlp', 'rootdual')) for p in pairs)
    print('\nPatched vs stock non-timing final signatures differ on', len(report['path_differences']), 'pairs.')
    print('Both-solved signature differences:', len(report['both_solved_path_differences']), report['both_solved_path_differences'])
    print('First-LP / root dual bound differences:', report['root_differences'])
    print('Pairs with both root statistics available:', report['root_available_pairs'])
    print('Time-limited pairs can differ in truncated work because of load; this is not a pure count of capture-caused divergences.')
    for comp in report['comparisons']:
        if comp['scope'] == 'pooled' and comp['subset'] == 'all':
            print(comp['a'], 'vs', comp['b'], 'solved only X', comp['only_a'], 'only Y', comp['only_b'])
    report['stock_reference_flags'] = [dict(instance=r['inst'], seed=r['seed'], flags=r['reference_flags'], primal=r['primal'], dual=r['dual'])
                                       for r in records if r['setting'] == 'stock-scip' and r['reference_flags']]
    print('Stock reference flags:', report['stock_reference_flags'])
    events = [json.loads(line) for line in (BASE / 'logs/full_stock/driver.jsonl').read_text().splitlines()]
    report['load'] = dict(first=events[0]['utc'], last=events[-1]['utc'],
        load1_min=min(e['load'][0] for e in events), load1_max=max(e['load'][0] for e in events),
        wall_timeouts=[e for e in events if e.get('returncode') in (124, 137)],
        stock_median_wall_cpu=float(np.median([r['wall']/r['time'] for r in records if r['setting'] == 'stock-scip' and r['time'] > 5])))
    print('Load:', report['load'])
    def clean(value):
        if isinstance(value, dict):
            return {k: clean(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [clean(v) for v in value]
        if isinstance(value, float) and not math.isfinite(value):
            return str(value)
        return value
    (BASE / 'logs/stock_analysis_r1.json').write_text(json.dumps(clean(report), indent=2, allow_nan=False) + '\n')


if __name__ == '__main__':
    main()
