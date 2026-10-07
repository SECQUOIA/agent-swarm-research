"""Verify round-2 revisions from archived logs; never launch a solver."""
import hashlib
import json
import math
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def parse(path):
    text = path.read_text()
    def match(pattern):
        return re.search(pattern, text, re.M)
    def number(pattern):
        m = match(pattern)
        return float(m[1]) if m else None
    nodes = match(r'^Solving Nodes\s*:\s*(\d+)(?: \(total of (\d+) nodes)?')
    lps = [match(r'^  ' + kind + r' LP\s*:\s*\S+\s+(\d+)\s+(\d+)')
           for kind in ('dual', 'primal')]
    status = match(r'^SCIP Status\s*:\s*(.*)$')
    rows = []
    for line in text.splitlines():
        m = re.match(r'^[ a-zA-Z*]?\s*([\d.]+)s\|(.*)$', line)
        if m:
            columns = m[2].split('|')
            rows.append((float(m[1]), tuple(columns[:4] + columns[5:])))
    return dict(time=number(r'^Solving Time \(sec\)\s*:\s*(\S+)'),
                solved=bool(status and 'optimal solution found' in status[1]),
                nodes=int(nodes[1]) if nodes else None,
                total=int(nodes[2] or nodes[1]) if nodes else None,
                lp=tuple(tuple(int(v) for v in m.groups()) if m else None for m in lps),
                rows=rows)


def gm(values):
    return math.exp(math.fsum(math.log(v) for v in values) / len(values))


def sgm(values, shift):
    return gm([v + shift for v in values]) - shift


def ratio(data, pairs, a, b):
    return gm([(data[a, *p]['time'] + 1) / (data[b, *p]['time'] + 1) for p in pairs])


def main():
    artifacts = {}
    for directory in ('r2-code', 'r2-logs'):
        for path in sorted((BASE / 'reviews' / directory).rglob('*')):
            if path.is_file():
                content = path.read_bytes()
                content.decode()  # Read every code/log artifact, including the 16 solver logs.
                artifacts[str(path.relative_to(BASE))] = hashlib.sha256(content).hexdigest()
    saved = BASE / 'logs/audit_revision_r2.json'
    if saved.exists():
        assert json.loads(saved.read_text())['review_artifact_sha256'] == artifacts
        print('PASS: all 39 review artifacts unchanged from the first successful evidence audit.')
    inst = (BASE / 'logs/testset_full.txt').read_text().split()
    pairs = [(i, seed) for i in inst for seed in (1, 2)]
    data = {(setting, *p): parse(BASE / 'logs' / directory / f'{p[0]}.{name}.s{p[1]}.log')
            for setting, directory, name in [('off', 'full', 'off'), ('scip', 'full', 'scip'),
                                             ('corner', 'full', 'corner'), ('eff', 'full', 'eff'),
                                             ('stock', 'full_stock', 'scip')]
            for p in pairs}
    both = [p for p in pairs if data['stock', *p]['solved'] and data['scip', *p]['solved']]
    same = [p for p in both if all(data['stock', *p][key] == data['scip', *p][key]
                                 for key in ('nodes', 'lp'))]
    assert len(both) == 74 and len(same) == 69
    changed = sorted(set(both) - set(same))
    assert changed == [('blend531', 2), ('carton9', 1), ('carton9', 2),
                       ('edgecross14-039', 1), ('edgecross14-039', 2)]
    effects = []
    for lo, hi, n, expected in [(0, 1, 41, 1.0398), (1, 10, 19, 1.3033),
                                (10, 300, 9, 1.4384), (0, 300, 69, 1.1544)]:
        subset = [p for p in same if lo <= data['stock', *p]['time'] < hi]
        value = ratio(data, subset, 'scip', 'stock')
        assert len(subset) == n and round(value, 4) == expected
        effects.append(dict(stock_cpu_range=[lo, hi], n=n, patched_stock=value))
    shared = [p for p in same if data['off', *p]['solved']]
    assert len(shared) == 68
    within = ratio(data, shared, 'scip', 'off')
    cross = ratio(data, shared, 'stock', 'off')
    assert round(within, 4) == 1.1029 and round(cross, 4) == 0.9535
    print('Identical stock/patched signatures:', len(same), 'of', len(both), 'both solved')
    print('Changed solved node/LP signatures:', changed)
    for row in effects:
        print('Batch effect:', row)
    print(f'68 shared-path pairs: within-batch patched/off {within:.4f}; cross-batch stock/off {cross:.4f}')

    same_load = []
    for i, archived, now in [('kall_diffcircles_5b', 5.61, 3.96), ('nvs24', 10.87, 7.44),
                            ('crudeoil_pooling_ct2', 26.34, 19.03), ('pointpack08', 52.49, 32.98)]:
        row = dict(instance=i)
        for setting in ('off', 'scip'):
            runs = {binary: parse(BASE / f'reviews/r2-logs/sameload/{i}.{setting}.s1.{binary}.log')
                    for binary in ('stock', 'patched')}
            for binary, run in runs.items():
                assert run['solved'] and run['nodes'] == data[setting, i, 1]['nodes']
            assert runs['stock']['lp'] == runs['patched']['lp']
            value = runs['patched']['time'] / runs['stock']['time']
            assert abs(value - 1) < 0.03
            row[setting + '_patched_stock'] = value
        assert data['off', i, 1]['time'] == archived
        off_stock = parse(BASE / f'reviews/r2-logs/sameload/{i}.off.s1.stock.log')
        assert off_stock['time'] == now
        row.update(archived_off=archived, same_load_off=now, archived_now=archived / now)
        same_load.append(row)
        print('Same-load:', row)

    a, b = data['stock', 'gabriel01', 2], data['scip', 'gabriel01', 2]
    k = 0
    while k < min(len(a['rows']), len(b['rows'])) and a['rows'][k][1] == b['rows'][k][1]:
        k += 1
    assert k == 103 and a['rows'][k-1][0] == 29.0 and b['rows'][k-1][0] == 44.6
    assert a['rows'][k-1][1][0].strip() == '6600' and a['time'] == 256.83
    projected = a['time'] * 44.6 / 29.0
    assert round(projected) == 395 and not b['solved']
    print(f'gabriel01 s2: {k} identical display rows, 29.0 vs 44.6 s at node 6600; 256.83 * 44.6 / 29.0 = {projected:.6f} s (estimate)')
    for i, seed, stock_nodes, patched_nodes in [('blend852', 1, 84509, 99192),
                                               ('blend852', 2, 96144, 101835),
                                               ('tln7', 1, 584309, 308290)]:
        assert data['stock', i, seed]['nodes'] == stock_nodes
        assert data['scip', i, seed]['nodes'] == patched_nodes
        assert data['stock', i, seed]['solved'] == (i == 'blend852')
        assert data['scip', i, seed]['solved'] == (i == 'tln7')
        print(f'Path outcome: {i} s{seed}, stock {stock_nodes} nodes, patched {patched_nodes} nodes')

    max_node_change = 0
    max_displayed_change = 0
    for mode, key in [('last', 'nodes'), ('total', 'total')]:
        report = (BASE / f'reviews/r2-logs/recompute_stock_{mode}nodes.md').read_text()
        for line in report.splitlines():
            fields = [f.strip() for f in line.split('|')[1:-1]]
            if not fields or fields[0] not in ('1', '2', '1+2'):
                continue
            seeds, setting, solved, cpu, nodes, nc, ccpu, cnodes = fields
            subset = [p for p in pairs if p[1] in [int(s) for s in seeds.split('+')]]
            balanced = [p for p in subset if all(data[s, *p]['nodes'] is not None
                                               for s in ('off', 'stock', 'scip', 'corner', 'eff'))]
            common = [p for p in subset if all(data[s, *p]['solved']
                                             for s in ('off', 'stock', 'scip', 'corner', 'eff'))]
            rs = [data[setting, *p] for p in subset]
            assert solved == f'{sum(r["solved"] for r in rs)}/{len(rs)}' and int(nc) == len(common)
            assert f'{sgm([r["time"] if r["solved"] else 300 for r in rs], 1):.3f}' == cpu
            assert f'{sgm([data[setting, *p][key] for p in balanced], 100):.1f}' == nodes
            assert f'{sgm([data[setting, *p]["time"] for p in common], 1):.3f}' == ccpu
            assert f'{sgm([data[setting, *p][key] for p in common], 100):.1f}' == cnodes
            for scope in (balanced, common):
                total_mean = sgm([data[setting, *p]['total'] for p in scope], 100)
                last_mean = sgm([data[setting, *p]['nodes'] for p in scope], 100)
                delta = total_mean - last_mean
                max_node_change = max(max_node_change, delta)
                max_displayed_change = max(max_displayed_change, round(total_mean, 1) - round(last_mean, 1))
    assert round(max_displayed_change, 1) == 0.5 and max_node_change < 0.6
    print(f'PASS: all 30 reviewer table rows match 600 raw logs; total-node sgm change at most {max_displayed_change:.1f} at table precision ({max_node_change:.6f} unrounded).')
    print(f'PASS: read all {len(artifacts)} round-2 code/log artifacts; 16 same-load logs parsed; no solver launched.')
    if '--check-note' in sys.argv:
        note = (BASE / 'note.md').read_text()
        assert 'round 2 on 2026-10-04; not re-reviewed' in note
        assert '## Revision after review round 2' in note
        for withdrawn in ('modest observed benefit', 'genuine additional', 'true enabling comparison',
                          'instrumentation distortion', 'more favourable'):
            assert withdrawn not in note
        assert 'last run after a restart' in note and '1.103' in note
        assert 'neither that enabling' in note and 'interleaved' in note
        assert re.findall(r'^## (\d+)\.', note, re.M) == [str(i) for i in range(1, 11)]
        for target in re.findall(r'\]\(([^)]+)\)', note):
            if not target.startswith(('http', '/')):
                assert (BASE / target).exists(), target
        print('PASS: withdrawn claims absent; round-2 status, node definition, scoped ratio, follow-up, section numbering and local links checked.')
    (BASE / 'logs/audit_revision_r2.json').write_text(json.dumps(dict(
        review_artifact_sha256=artifacts, batch_effect=effects, within_batch=within,
        cross_batch=cross, same_load=same_load, gabriel_estimated_archived_cpu=projected,
        max_total_node_sgm_change=max_node_change), indent=2) + '\n')


if __name__ == '__main__':
    main()
