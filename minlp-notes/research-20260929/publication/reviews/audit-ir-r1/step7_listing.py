"""Compare the listing fields of instances.html (reviewer's parse) with pages.json."""
import collections, json
import step4_pages as S

pj = json.load(open(S.BA + 'pages.json'))
recs = {r['name']: r for r in pj}
raw = open(S.PAGES + 'instances.html', encoding='utf-8').read()
p = S.Rows(raw)
p.feed(raw)
rows = [r for r in p.rows if len(r) == 14]
print('listing rows with 14 cells:', len(rows))
marks = collections.Counter()
diff = []
nf = 0
seen = set()
for r in rows:
    c = [S.text(x) for x in r]
    name = c[0]
    seen.add(name)
    marks[(c[3], c[10])] += 1
    mine = {'type': c[2], 'convex': c[3] not in ('-', '', '\xa0'), 'nvars': c[4], 'ncons': c[7],
            'solved': c[10] not in ('', '\xa0'), 'listing_dual': c[11].replace('\xa0', ''),
            'listing_primal': c[12].replace('\xa0', '')}
    rec = recs.get(name)
    if rec is None:
        diff.append((name, 'not in pages.json'))
        continue
    for k, v in mine.items():
        nf += 1
        if v != rec[k]:
            diff.append((name, k, v, rec[k]))
print('cell marks (convex, solved):', dict(marks))
print('fields compared', nf, 'differences', len(diff), diff[:8])
print('names identical to pages.json:', seen == set(recs))
