"""Own checks of minlplib-status saved data (json only)."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[6])

import json, collections, re
S = (_PUBLIC_REPO + '/research-20260929/publication/minlplib-status/data/')
B = (_PUBLIC_REPO + '/research-20260929/bound-audit/')
a = json.load(open(S + 'part_a.json'))
inst = a['instances']
print('site identical:', {k: v['identical'] for k, v in a['site'].items()})
bad = []
for n, r in inst.items():
    ok = (not r['listing_changed']) and all(c['byte_identical'] for c in r['page_comparisons']) \
         and r['pages_json_match'] and r['osil']['identical_to_cache']
    if not ok: bad.append(n)
print('instances', len(inst), 'not fully unchanged:', bad)
res = json.load(open(B + 'results.json'))
need = collections.defaultdict(set)
for r in res:
    c = r['cls']
    key = '(i)' if c.startswith('(i) ') else '(i-r)' if c.startswith('(i-r)') else 'emfl' if r['name'].startswith('emfl') else None
    if key: need[key].add(r['name'])
for k, v in need.items():
    print(k, len(v), 'missing from refresh:', sorted(v - set(inst)))
# fetch manifest dates
m = json.load(open(S + 'fetch_manifest.json'))
txt = json.dumps(m)
print('dates in fetch_manifest:', collections.Counter(re.findall(r'(20\d\d-\d\d-\d\d)T', txt)) or collections.Counter(re.findall(r'\d\d (?:Oct|Sep) 2026', txt)))
# archived listings
al = json.load(open(S + 'archived_listings.json'))
print('archived_listings type', type(al), len(al))
items = al.items() if isinstance(al, dict) else enumerate(al)
names = set()
stat = collections.Counter()
for k, v in items:
    s = json.dumps(v)
    names.add(v.get('name', k) if isinstance(v, dict) else k)
    for w in re.findall(r'"(?:status|result|verdict|compare)": "([^"]+)"', s): stat[w] += 1
print('archived listing instances:', len(names), sorted(names))
print('listing statuses:', stat)
print('class (i)/(i-r) not in archived listings:', sorted((need['(i)'] | need['(i-r)']) - names))
ef = json.load(open(S + 'exact_forms.json'))
for n in ef if isinstance(ef, dict) else []:
    s = json.dumps(ef[n])
    print(n, s[:300])
