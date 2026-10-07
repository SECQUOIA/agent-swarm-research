"""Verifier check: compare every DOI-bearing entry of references.bib with its Crossref record.

Prints, per entry, the fields whose normalized values differ (title, first-author family
name, year, volume, number, pages). Differences are then read by hand: many are expected
(online year vs. issue year, TeX accents, title case).
"""
import json, re, sys, time, unicodedata, urllib.request

BIB = 'references.bib'
UA = 'minlp-notes-bib-verify/1.0 (mailto:noreply@example.org)'


def entries(path):
    t = open(path, encoding='utf8').read()
    for m in re.finditer(r'@(\w+)\{([^,]+),(.*?)\n\}', t, re.S):
        f = {}
        for g in re.finditer(r'^\s*(\w+)\s*=\s*\{(.*)\},?\s*$', m.group(3), re.M):
            f[g.group(1).lower()] = g.group(2)
        yield m.group(2), m.group(1).lower(), f


ACC = {"\\'": '\u0301', '\\`': '\u0300', '\\"': '\u0308', '\\~': '\u0303', '\\^': '\u0302',
       '\\c': '\u0327', '\\v': '\u030c', '\\u': '\u0306', '\\H': '\u030b'}


def norm(s):
    s = s or ''
    s = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', s)  # \emph{x} -> x
    for k in ACC:
        s = s.replace(k, '')
    s = s.replace('\\i', 'i').replace('\\L', 'L').replace('\\l', 'l').replace('\\o', 'o')
    s = s.replace('\\&', '&').replace('--', '-').replace('$', '')
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'<[^>]+>', '', s)  # Crossref JATS tags
    s = re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()
    return s


def fetch(doi):
    url = 'https://api.crossref.org/works/' + urllib.request.quote(doi, safe='/')
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)['message']
    except Exception as e:  # noqa: BLE001
        return {'error': str(e)}


def years(m):
    out = set()
    for k in ('published-print', 'published-online', 'issued', 'published'):
        d = m.get(k, {}).get('date-parts', [[None]])
        if d and d[0] and d[0][0]:
            out.add(str(d[0][0]))
    return out


only = set(sys.argv[1:])
for key, typ, f in entries(BIB):
    doi = f.get('doi')
    if not doi or (only and key not in only):
        continue
    m = fetch(doi)
    time.sleep(0.4)
    if 'error' in m:
        print(f'== {key} {doi}: ERROR {m["error"]}')
        continue
    issues = []
    ctitle = ' '.join(m.get('title', []))
    if norm(f.get('title')) != norm(ctitle):
        issues.append(f'title: bib={f.get("title")!r} | cr={ctitle!r}')
    auth = m.get('author') or m.get('editor') or []
    if auth:
        fam = auth[0].get('family', '') or auth[0].get('name', '')
        bfirst = (f.get('author') or f.get('editor') or '').split(' and ')[0].split(',')[0]
        if norm(fam) != norm(bfirst):
            issues.append(f'first author: bib={bfirst!r} | cr={fam!r}')
        if f.get('author') and len(f['author'].split(' and ')) != len(auth) and 'others' not in f['author']:
            issues.append(f'author count: bib={len(f["author"].split(" and "))} | cr={len(auth)}')
    if f.get('year') not in years(m):
        issues.append(f'year: bib={f.get("year")} | cr={sorted(years(m))}')
    for bf, cf in (('volume', 'volume'), ('number', 'issue'), ('pages', 'page')):
        bv, cv = f.get(bf), m.get(cf)
        if bf == 'volume' and typ in ('book', 'incollection', 'inproceedings'):
            continue  # series volumes are not in the work record
        if cv is None and bv is None:
            continue
        if norm(bv) != norm(cv):
            issues.append(f'{bf}: bib={bv!r} | cr={cv!r}')
    print(f'== {key} {doi}: ' + ('OK' if not issues else '\n   ' + '\n   '.join(issues)))
    sys.stdout.flush()
