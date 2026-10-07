"""Verify changed review numbers from raw archived logs; never launch SCIP."""
from decimal import Decimal, localcontext
from datetime import datetime
from pathlib import Path
import hashlib
import json
import math
import re
from zoneinfo import ZoneInfo

import numpy as np

from parse_logs import parse
from root_analysis import load_ref, rgc, tl_hit, SETS

BASE = Path(__file__).resolve().parent.parent


def main():
    report = dict(review_inventory=[], search=[], local_secants=[], selection={}, timing={})
    # Read every supplied review artifact; retain a reproducible inventory.
    for directory in ('r1-code', 'r1-logs'):
        for path in sorted((BASE / 'reviews' / directory).rglob('*')):
            if path.is_file():
                data = path.read_bytes()
                report['review_inventory'].append(dict(path=str(path.relative_to(BASE)),
                    bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
    fairness = BASE / 'reviews/r1-logs/fairness'
    report['fairness'] = []
    # The review filenames use node limit rather than setting and seed.
    def fairness_signature(path):
        txt = path.read_text()
        found = {}
        for key, pattern in {'nodes': r'Solving Nodes\s*:\s*(\d+)',
                             'primal': r'\nPrimal Bound\s*:\s*(\S+)',
                             'dual': r'\nDual Bound\s*:\s*(\S+)',
                             'dual_lp': r'\n  dual LP\s*:\s*\S+\s+(\d+\s+\d+)'}.items():
            found[key] = re.findall(pattern, txt)[-1]
        return found
    for patched in sorted(fairness.glob('*.P.log')):
        stock = patched.with_name(patched.name.replace('.P.log', '.U.log'))
        a, b = fairness_signature(patched), fairness_signature(stock)
        report['fairness'].append(dict(case=patched.name, same=a == b, patched=a, stock=b))
    assert sum(r['same'] for r in report['fairness'] if '.n1.' in r['case']) == 13
    assert [r['case'] for r in report['fairness'] if not r['same']] == ['tln7.n2000.P.log']
    assert fairness_signature(fairness / 'tln7.n2000.NC.log') == fairness_signature(fairness / 'tln7.n2000.U.log')
    for path in sorted((BASE / 'logs/dumps').glob('search_opt_*.out')):
        summaries = re.findall(r'^SUMMARY (.*)$', path.read_text(), re.M)
        data = json.loads(summaries[-1]) if summaries else dict(n=0, crashed=True)
        data['dump'] = path.stem.removeprefix('search_opt_')
        report['search'].append(data)
        assert data.get('best_outside_halfcircle', 0) == 0
    assert len(report['search']) == 7
    gains = []
    for path in (BASE / 'logs/dumps').glob('*.r1.check.json'):
        data = json.loads(path.read_text())
        if data['rel_gain']['n']:
            gains.append(data['rel_gain']['median'])
    report['gain_range'] = [min(gains), max(gains)]
    rows = []; incumbent_reports = 0
    terms = re.compile(r'([-+]\d[\d.eE+-]*)<([^>]+)>\[([^\]]+)\]')
    for path in sorted((BASE / 'logs/debugsol').glob('st_glmp_fp2.*.log')):
        incumbent = False
        lines = path.read_text().splitlines()
        for k, line in enumerate(lines):
            if re.match(r'^[*a-zA-Z]?\s*\d+\.\d+s\|', line) and not re.search(r'\|\s+--\s+\|', line):
                incumbent = True
            if line.startswith('***** debug: violated row <under_intersection'):
                m = re.fullmatch(r'\s*(\S+) <= (\S+)(.*) <= (\S+)\s*', lines[k+1])
                lhs, constant, body, rhs = m.groups()
                activity = float(constant)
                coefficients = {}
                for coefficient, variable, value in terms.findall(body):
                    coefficients[variable] = float(coefficient)
                    activity += float(coefficient) * (7.6275 if variable == 't_nlobjvar' else float(value))
                assert set(coefficients) <= {'t_x1', 't_x2', 't_nlobjvar'}
                assert coefficients['t_nlobjvar'] > 0
                rows.append(min(activity-float(lhs), float(rhs)-activity))
                incumbent_reports += incumbent
            if line.startswith('***** debug: violated row <overestimate_pow'):
                # Secant over [l,u]: (l+u)*x - aux >= l*u.
                m = re.fullmatch(r'\s*(\S+) <= 0 \+(\S+)<t_x2>\[5.65\] -1<auxvar_pow_2>\[31.9225\] <= 1e\+20', lines[k+1])
                assert m
                with localcontext() as ctx:
                    ctx.prec = 40
                    product, total = map(Decimal, m.groups())
                    gap = (total*total - 4*product).sqrt()
                    lower, upper = (total-gap)/2, (total+gap)/2
                assert lower > Decimal('5.65')
                report['local_secants'].append(dict(log=path.name, lower=str(lower), upper=str(upper)))
    assert len(rows) == 73 and incumbent_reports == 0
    assert math.isclose(min(rows), 0.0175438188008, abs_tol=2e-12)
    assert len(report['local_secants']) == 9
    report['helper'] = dict(rows=len(rows), minimum_slack=min(rows), after_incumbent=incumbent_reports,
                            supplied_objective=5.65*1.35)
    reference_line = [line for line in (BASE / 'sources/minlplib.solu').read_text().splitlines()
                      if 'st_glmp_fp2' in line][0].split()
    assert reference_line[0] == '=opt=' and float(reference_line[2]) == 7.3445454180
    assert report['helper']['supplied_objective'] > float(reference_line[2])
    for setting in ('corner', 'eff'):
        records = [parse(str(p)) for p in (BASE / 'logs/root').glob(f'*.{setting}.s0.log')]
        changed = [r for r in records if r.get('selchanged', 0) > 0]
        report['selection'][setting] = dict(searches=sum(r.get('selcalls', 0) for r in records),
            changed=sum(r.get('selchanged', 0) for r in records), n=len(changed),
            median_gain=float(np.median([r['selgain'] for r in changed])))
    assert report['selection']['corner']['changed'] == 173928
    assert report['selection']['corner']['searches'] == 228135
    assert report['selection']['eff']['changed'] == 184473
    assert report['selection']['eff']['searches'] == 233699
    assert all(r['n'] == 267 for r in report['selection'].values())
    root = [parse(str(p)) for p in (BASE / 'logs/root').glob('*.log')]
    grouped = {(r['inst'], r['setting']): r for r in root}
    ref, _, sense = load_ref()
    common = [i for i in sorted({r['inst'] for r in root}) if i in ref and
              all(not tl_hit(grouped.get((i, s))) and
                  rgc(grouped[i, s], ref[i], -1 if sense[i] == 'max' else 1) is not None for s in SETS)]
    assert len(common) == 251
    report['search_costs_common251'] = {}
    for s in ('corner', 'eff'):
        selected = [grouped[i, s] for i in common]
        elapsed = sum(r['seltime'] for r in selected)
        generated = sum(r['gencuts'] for r in selected)
        searches = sum(r['selcalls'] for r in selected)
        report['search_costs_common251'][s] = dict(seconds=elapsed, generated=generated, searches=searches,
            ms_per_generated=1000*elapsed/generated, ms_per_search=1000*elapsed/searches)
    full = [parse(str(p)) for p in (BASE / 'logs/full').glob('*.log')]
    for setting in ('off', 'scip', 'corner', 'eff'):
        records = [r for r in full if r['setting'] == setting and r['time'] is not None and r['time'] > 5]
        report['timing'][setting] = dict(n=len(records), median_wall_cpu=float(np.median([r['wall']/r['time'] for r in records])))
    report['archive_log_times'] = {}
    for directory in ('full', 'debugsol'):
        timestamps = [p.stat().st_mtime for p in (BASE / 'logs' / directory).glob('*.s*.log')]
        report['archive_log_times'][directory] = dict(
            first=datetime.fromtimestamp(min(timestamps), ZoneInfo('America/New_York')).isoformat(),
            last=datetime.fromtimestamp(max(timestamps), ZoneInfo('America/New_York')).isoformat())
    # Benchmark launch order is instance, setting, seed (run_bench.py).
    quadratic = (BASE / 'reviews/r1-logs/kall_c52.eff.s2.log').read_text()
    assert 'solution is feasible in original problem' in quadratic
    assert '9.51357e-07' in quadratic and '1.34291e-08' in quadratic and '9.73643e-10' in quadratic
    assert 'Solving Nodes      : 3830' in quadratic
    assert '+1.53710868841930e+00' in quadratic
    report['kall'] = dict(nodes=3830, primal=1.5371086884193, constraints=9.51357e-7,
                          lp_rows=1.34291e-8, bounds=9.73643e-10)
    path = BASE / 'logs/audit_revision_r1.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    for key, value in report.items():
        if key not in ('review_inventory', 'fairness'):
            print(key, json.dumps(value))
    print('PASS: read all', len(report['review_inventory']), 'review artifacts; 13 root identities, capture-only diagnosis, search summaries, 73 corrected rows, 9 local false alarms, selection counts and timing ratios.')


if __name__ == '__main__':
    main()
