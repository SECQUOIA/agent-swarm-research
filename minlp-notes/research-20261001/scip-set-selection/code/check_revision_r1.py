"""Final targeted checks of raw stock records, aggregates and revised claims."""
from collections import Counter
from pathlib import Path
import ast
import json
import math
import re

from scipy.stats import wilcoxon

BASE = Path(__file__).resolve().parent.parent


def main():
    for name in ('build_stock_r1.py', 'check_stock_r1.py', 'run_stock_r1.py',
                 'audit_revision_r1.py', 'stock_analysis_r1.py', 'check_revision_r1.py'):
        ast.parse((BASE / 'code' / name).read_text())
    report = json.loads((BASE / 'logs/stock_analysis_r1.json').read_text())
    records = report['records']
    assert len(records) == 600
    raw = {}
    stock = []
    for record in records:
        path = BASE / record['path']
        text = path.read_text()
        status = re.findall(r'^SCIP Status\s*:\s*(.*)$', text, re.M)
        solved = bool(status and status[-1] == 'problem is solved [optimal solution found]')
        times = re.findall(r'^Solving Time \(sec\)\s*:\s*([\d.]+)$', text, re.M)
        nodes = re.findall(r'^Solving Nodes\s*:\s*(\d+)(?: \(.*\))?$', text, re.M)
        rc = re.findall(r'@@ wallclock [\d.]+ returncode (\S+)', text)[-1]
        assert solved == ('optimal solution found' in (record['status'] or ''))
        assert (float(times[-1]) if times else None) == record['time']
        assert (int(nodes[-1]) if nodes else None) == record['nodes']
        raw[record['inst'], record['seed'], record['setting']] = dict(
            solved=solved and rc == '0', cpu=float(times[-1]) if solved and rc == '0' else 300,
            nodes=int(nodes[-1]) if nodes else None)
        if record['setting'] == 'stock-scip':
            assert rc == '0' and status and nodes and times
            assert float(times[-1]) >= 0
            stock.append(record)
    assert len(stock) == 120
    settings = ('off', 'stock-scip', 'patched-scip', 'corner', 'eff')
    def mean(values, shift):
        return math.exp(math.fsum(math.log(v+shift) for v in values)/len(values))-shift
    for row in report['tables']:
        keys = [(i, s) for i, s, setting in raw if setting == row['setting'] and
                (row['scope'] not in ('seed 1', 'seed 2') or s == int(row['scope'][-1])) and
                (row['scope'] != 'exclude off failure' or (i, s) != ('ex5_4_2', 1))]
        observations = [raw[i, s, row['setting']] for i, s in keys]
        assert row['n'] == len(observations)
        assert row['solved'] == sum(r['solved'] for r in observations)
        independent = math.exp(math.fsum(math.log(r['cpu']+1) for r in observations)/len(observations))-1
        assert math.isclose(independent, row['cpu'], rel_tol=1e-12)
        balanced = [p for p in keys if all(raw[*p, s]['nodes'] is not None for s in settings)]
        common = [p for p in keys if all(raw[*p, s]['solved'] for s in settings)]
        assert len(balanced) == row['nodes_n'] and len(common) == row['common_n']
        assert math.isclose(mean([raw[*p, row['setting']]['nodes'] for p in balanced], 100), row['nodes'], rel_tol=1e-12)
        assert math.isclose(mean([raw[*p, row['setting']]['cpu'] for p in common], 1), row['common_cpu'], rel_tol=1e-12)
        assert math.isclose(mean([raw[*p, row['setting']]['nodes'] for p in common], 100), row['common_nodes'], rel_tol=1e-12)
    for comparison in report['comparisons']:
        a, b = comparison['a'], comparison['b']
        keys = sorted({(i, s) for i, s, setting in raw if setting == a and
                       (comparison['scope'] == 'pooled' or s == int(comparison['scope'][-1]))})
        subset = comparison['subset']
        if subset == 'pair solved':
            keys = [p for p in keys if raw[*p, a]['solved'] and raw[*p, b]['solved']]
        elif subset == 'all five solved':
            keys = [p for p in keys if all(raw[*p, s]['solved'] for s in settings)]
        elif subset == 'exclude off failure':
            keys = [p for p in keys if p != ('ex5_4_2', 1)]
        assert len(keys) == comparison['n']
        for field, shift, ratio_key, test_key in (('cpu', 1, 'cpu_ratio', 'cpu_test'),
                                                 ('nodes', 100, 'node_ratio', 'node_test')):
            if comparison[ratio_key] is None:
                continue
            differences = [math.log((raw[*p, a][field]+shift)/(raw[*p, b][field]+shift)) for p in keys]
            ratio = math.exp(math.fsum(differences)/len(differences))
            assert math.isclose(ratio, comparison[ratio_key], rel_tol=1e-12)
            if comparison['scope'] == 'pooled':
                differences = [math.fsum(v for p, v in zip(keys, differences) if p[0] == i)/sum(p[0] == i for p in keys)
                               for i in sorted({p[0] for p in keys})]
            nz = [v for v in differences if abs(v) > 1e-12]
            expected = float(wilcoxon(nz).pvalue) if len(nz) >= 10 else None
            actual = comparison[test_key]['p']
            assert expected is None and actual is None or expected is not None and actual is not None and math.isclose(expected, actual, rel_tol=1e-12)
    audit = json.loads((BASE / 'logs/audit_revision_r1.json').read_text())
    assert audit['helper']['rows'] == 73 and audit['helper']['after_incumbent'] == 0
    assert len(audit['local_secants']) == 9 and len(audit['search']) == 7
    assert audit['selection']['corner']['n'] == audit['selection']['eff']['n'] == 267
    assert round(audit['search_costs_common251']['corner']['ms_per_search'], 3) == 0.507
    assert round(audit['search_costs_common251']['eff']['ms_per_search'], 3) == 0.550
    note = (BASE / 'note.md').read_text()
    prose = re.sub(r'```.*?```', '', note, flags=re.S)
    assert re.findall(r'^## (\d+)\.', prose, re.M) == [str(i) for i in range(1, 11)]
    assert 'revised after review' in prose and 'not re-reviewed' in prose
    assert 'Nothing here has been committed' not in prose
    assert 'defaults reproduce SCIP exactly' not in prose
    assert '1.25–1.65' not in prose
    assert 'The rerun is in progress' not in prose and 'analysis is\n  pending' not in prose
    for row in report['tables']:
        if row['scope'] in ('seed 1', 'seed 2', 'pooled') and row['setting'] in ('off', 'stock-scip', 'patched-scip'):
            assert f"{row['cpu']:.3f}" in prose
    driver = [json.loads(line) for line in (BASE / 'logs/full_stock/driver.jsonl').read_text().splitlines()]
    assert driver[-1]['event'] == 'finish' and not driver[-1]['stopped']
    assert all(e['workers'] <= 8 for e in driver if e['event'] == 'start')
    print('PASS: six script syntax checks; 600 records independently read; all 120 stock runs have final statistics and rc 0; CPU/node means, solved counts, paired ratios and instance-averaged tests match raw logs; revised claims and status checked; driver finished with <=8 workers.')
    print('Stock statuses:', dict(Counter(r['status'] for r in stock)))
    print('Stock reference flags:', report['stock_reference_flags'])


if __name__ == '__main__':
    main()
