"""Spot-check bibliography metadata against Crossref (title, first author, year, volume, issue, pages)."""
import re, sys, json, time, urllib.request, urllib.parse, unicodedata
bib = open('references.bib').read()
entries = {}
for m in re.finditer(r'@(\w+)\{([^,]+),(.*?)\n\}', bib, re.S):
    typ, key, body = m.groups()
    f = dict((k.lower(), v.strip()) for k, v in re.findall(r'(\w+)\s*=\s*\{(.*?)\}\s*,?\s*$', body, re.M | re.S))
    entries[key] = (typ, f)
def norm(s):
    s = unicodedata.normalize('NFKD', s or '')
    s = re.sub(r'[{}\\$]', '', s)
    return re.sub(r'[^a-z0-9]', '', s.lower())
keys = sys.argv[1:]
for k in keys:
    typ, f = entries[k]
    doi = f.get('doi')
    if not doi:
        print(f'{k}: no DOI'); continue
    url = 'https://api.crossref.org/works/' + urllib.parse.quote(doi)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'bibcheck/1.0 (mailto:noreply@example.org)'})
        d = json.load(urllib.request.urlopen(req, timeout=30))['message']
    except Exception as e:
        print(f'{k}: DOI {doi} ERROR {e}'); time.sleep(2); continue
    ct = (d.get('title') or [''])[0]
    au = d.get('author') or []
    fa = au[0].get('family', '') if au else ''
    yr = None
    for fld in ('published-print', 'issued', 'published-online'):
        if d.get(fld, {}).get('date-parts'):
            yr = d[fld]['date-parts'][0][0]; break
    issues = []
    if norm(ct)[:40] != norm(f.get('title'))[:40]:
        issues.append(f'title: bib="{f.get("title")}" CR="{ct}"')
    bfa = f.get('author', '').split(' and ')[0].split(',')[0]
    if norm(bfa) != norm(fa):
        issues.append(f'first author: bib="{bfa}" CR="{fa}"')
    if str(yr) != f.get('year'):
        issues.append(f'year: bib={f.get("year")} CR={yr} (issued={d.get("issued",{}).get("date-parts")})')
    for bf, cf in (('volume', 'volume'), ('number', 'issue'), ('pages', 'page')):
        bv, cv = f.get(bf), d.get(cf)
        if bv and cv and norm(bv.replace('--', '-')) != norm(cv):
            issues.append(f'{bf}: bib={bv} CR={cv}')
        if cv and not bv and bf != 'number':
            issues.append(f'{bf}: missing in bib, CR={cv}')
    print(f'{k}: ' + ('OK' if not issues else '; '.join(issues)))
    time.sleep(1.5)
