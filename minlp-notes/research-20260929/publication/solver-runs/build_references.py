#!/usr/bin/env python3
"""Build the frozen, sourced reference table; no network or solver calls."""
import csv
import hashlib
import json
import re
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent.parent
summary = RESEARCH / 'open-instances-summary.md'
names = (HERE / 'instances.txt').read_text().split()
pages = {r['name']: r for r in json.loads((RESEARCH / 'bound-audit/pages.json').read_text())}
refs = {}
for line in summary.read_text().splitlines():
    if not line.startswith('| '):
        continue
    cells = [c.strip().replace('−', '-') for c in line.split('|')[1:-1]]
    name = cells[0].replace(' (max)', '')
    if name not in names:
        continue
    dual = re.search(r'-?\d+(?:\.\d+)?(?:e[+-]?\d+)?', cells[2])
    primal = re.search(r'-?\d+(?:\.\d+)?(?:e[+-]?\d+)?', cells[3])
    refs[name] = dict(instance=name, certificate_dual=dual[0] if dual else None,
                      reference_primal=primal[0] if primal else None,
                      certificate_scope='OSIL', primal_kind='numerical',
                      source='open-instances-summary.md')

def setref(name, dual, primal, kind, source, scope='OSIL'):
    refs[name] = dict(instance=name, certificate_dual=dual, reference_primal=primal,
                      certificate_scope=scope, primal_kind=kind, source=source)

for n in (100, 200, 400, 800):
    name = f'camshape{n}'
    val = json.loads((RESEARCH / f'open-instances/logs/{name}_bound.json').read_text())['dual_interval'][0]
    # The verifier proves an attained rational optimum. Enclose the displayed
    # 20-digit value outward rather than treating its rounded decimal as exact.
    upper = str(Decimal(val) + Decimal('1e-19'))
    refs[name].update(reference_primal=upper, primal_kind='exact feasible upper enclosure',
                      source='open-instances-summary.md; reviews/open-instances-verification/verification-report.md, Section 5')

for n in (50, 100, 200, 400):
    p = RESEARCH / f'open-instances-wave2/cops/logs/chain{n}_bound.json'
    r = json.loads(p.read_text())
    setref(f'chain{n}', str(r['target']), r['primal']['obj_double_point'], 'numerical',
           str(p.relative_to(RESEARCH)))

catmix = {
    100: ('-0.04806943203114456', '-0.048069432030979596'),
    200: ('-0.04805914559907277', '-0.0480591455801143916'),
    400: ('-0.04805654782467129', '-0.048056547756611555'),
    800: ('-0.04805590147967565', '-0.0480559013312308003'),
}
for n, (d, p) in catmix.items():
    setref(f'catmix{n}', d, p, 'exact feasible upper enclosure',
           'reviews/cops-verification/verification-report.md, Section 2d' if n <= 200 else 'reviews/catmix-recheck.md')

kan = {
    'kan_r3_h1_n4': ('0.0027812371525814', '0.0027812372214418141291'),
    'kan_r3_h1_n5': ('-0.011042679521782', '-0.011042679414487295306'),
    'kan_r3_h1_n9': ('0.012963659963475', '0.012963660053039328497'),
    'kan_r5_h1_n3': ('-262.86422590922', '-262.86422588506524044'),
    'kan_r5_h1_n5': ('0.27258325385485', '0.27258325395662269731'),
    'kan_r5_h1_n8': ('0.069327860510525', '0.069327860606191085327'),
}
for name, (d, p) in kan.items():
    setref(name, d, p, 'network relaxation R, numerical',
           'open-instances-wave3/report.md, table 1c; reviews/wave3-verification/verification-report.md, Sections 1c-1e',
           'R only; OSIL exactly infeasible')

for name, primal in {
    'hvycrash': '-0.2185', 'ex6_2_7': '-0.16084761546360086',
    'ex6_2_5': '-70.75207783344770558', 'etamac': '-15.2946756433680896',
    'pricing050': '-1813.8290784519730578',
}.items():
    refs[name].update(reference_primal=primal, primal_kind='exact feasible enclosure',
                      source='open-instances-summary.md; reviews/wave2-small-verification/verification-report.md')
refs['optcdeg2'].update(reference_primal='293.87607509587509328', primal_kind='exact feasible upper enclosure')
refs['pindyck'].update(reference_primal='-1170.486285436088562087577', primal_kind='exact feasible upper enclosure',
                       source='open-instances-summary.md; open-instances-wave2/small/pindyck-extension.md')
for name in ('eg_disc_s', 'eg_disc2_s', 'eg_int_s'):
    refs[name]['primal_kind'] = 'exact feasible upper enclosure'
refs['waterno2_06']['reference_primal'] = '282.8880374'
refs['waterno2_06']['primal_kind'] = 'listed, tolerance feasible'
for name, primal in {'waterno2_09': '914.011970350', 'waterno2_12': '2233.821335282',
                     'waterno2_18': '5023.982735143', 'waterno2_24': '6963.795154460'}.items():
    refs[name].update(reference_primal=primal, primal_kind='numerical, row violation 1e-9 to 4.44e-9',
                      source='open-instances-summary.md; open-instances-wave2/waterno2/report.md, Section on window re-optimization')
refs['ann_cumene_tanh'].update(reference_primal='-3379.9823940717715481', primal_kind='numerical, row violation 4.6e-27',
                              source='open-instances-summary.md; reviews/ann-extension-review.md')

assert set(refs) == set(names)
for name in names:
    r, page = refs[name], pages[name]
    r['sense'] = page['sense']
    choose = max if r['sense'] == 'min' else min
    duals = [d for d in page['duals'] if d['value'] not in ('', '-', 'NA')]
    best = choose(duals, key=lambda d: Decimal(d['value'])) if duals else None
    points = [p for p in page['points'] if p['section'] == 'primal']
    bestp = (min if r['sense'] == 'min' else max)(points, key=lambda p: Decimal(p['value']))
    r.update(listed_dual=best['value'] if best else None,
             listed_dual_solver=best['solver'] if best else None,
             listed_primal=bestp['value'], listed_primal_point=bestp['point'],
             listed_primal_infeas=bestp['infeas'],
             listed_source=f'bound-audit/pages/{name}.html (cached September 2026); bound-audit/pages.json')
rows = [refs[n] for n in sorted(names)]
(HERE / 'references.json').write_text(json.dumps(rows, indent=2) + '\n')
with (HERE / 'references.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
sources = {summary, RESEARCH / 'bound-audit/pages.json'}
sources.update(RESEARCH / r['source'].split(';')[0].split(',')[0] for r in rows)
sources.update(RESEARCH / f'open-instances/logs/camshape{n}_bound.json' for n in (100, 200, 400, 800))
sources.update(RESEARCH / p for p in ('reviews/wave2-small-verification/verification-report.md',
                                     'reviews/open-instances-verification/verification-report.md',
                                     'reviews/wave3-verification/verification-report.md',
                                     'open-instances-wave2/waterno2/report.md',
                                     'reviews/ann-extension-review.md',
                                     'open-instances-wave2/small/pindyck-extension.md'))
(HERE / 'reference_sources.json').write_text(json.dumps({str(p.relative_to(RESEARCH)): hashlib.sha256(p.read_bytes()).hexdigest()
                                                        for p in sorted(sources)}, indent=2) + '\n')
print(f'{len(rows)} sourced references written')
