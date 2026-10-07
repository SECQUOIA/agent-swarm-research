"""R7: compare cited references.bib entries that carry a DOI against Crossref (title, first author,
year, volume, pages). Prints only mismatches and a summary. Read-only."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import re, glob, json, time, urllib.request, urllib.parse, difflib, unicodedata
ROOT = (_PUBLIC_REPO + '/paper-decomposition-aware')
txt = "".join(open(f).read() for f in glob.glob(ROOT + "/sections/*.tex"))
cited = set()
for m in re.finditer(r'\\cite[a-z]*\*?(?:\[[^\]]*\])?\{([^}]*)\}', txt, re.S):
    cited |= {k.strip() for k in m.group(1).split(',')}
bib = open(ROOT + "/references.bib").read()
entries = {}
for e in re.split(r'\n(?=@)', bib):
    m = re.match(r'\s*@(\w+)\{([^,]+),', e)
    if not m: continue
    f = dict((k.lower(), v.strip()) for k, v in re.findall(r'(\w+)\s*=\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}', e))
    entries[m.group(2)] = f
def norm(s):
    s = re.sub(r'\\.|[{}$]', '', s or ''); s = unicodedata.normalize('NFKD', s)
    return re.sub(r'[^a-z0-9 ]', '', s.lower())
n = bad = 0
for k in sorted(cited):
    f = entries.get(k, {}); doi = f.get('doi')
    if not doi: continue
    n += 1
    try:
        url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/()")
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "r7-audit"}), timeout=30) as r:
            m = json.load(r)["message"]
    except Exception as ex:
        print(f"{k}: DOI {doi} lookup failed: {ex}"); bad += 1; time.sleep(1); continue
    issues = []
    t1, t2 = norm(f.get('title')), norm((m.get('title') or [''])[0])
    if difflib.SequenceMatcher(None, t1, t2).ratio() < 0.85: issues.append(f"title bib='{f.get('title')}' cr='{(m.get('title') or [''])[0]}'")
    fa = norm(f.get('author', '').split(' and ')[0].split(',')[0])
    ca = norm((m.get('author') or [{}])[0].get('family', '')) if m.get('author') else ''
    if ca and fa and fa.split()[-1] not in ca and ca.split()[-1] not in fa: issues.append(f"first author bib='{fa}' cr='{ca}'")
    yr = str(((m.get('published-print') or m.get('published-online') or m.get('issued'))['date-parts'][0][0]))
    yrs = {str(x['date-parts'][0][0]) for x in [m.get('published-print'), m.get('published-online'), m.get('issued')] if x}
    if f.get('year') and f.get('year') not in yrs: issues.append(f"year bib={f.get('year')} cr={sorted(yrs)}")
    if f.get('volume') and m.get('volume') and norm(f['volume']).replace(' ', '') != norm(m['volume']).replace(' ', ''): issues.append(f"volume bib={f['volume']} cr={m['volume']}")
    if f.get('pages') and m.get('page'):
        bp = re.sub(r'[^0-9]+', '-', f['pages']).strip('-'); cp = re.sub(r'[^0-9]+', '-', m['page']).strip('-')
        if bp != cp: issues.append(f"pages bib={f['pages']} cr={m['page']}")
    if issues:
        bad += 1; print(f"{k} ({doi}): " + "; ".join(issues))
    time.sleep(0.7)
print(f"checked {n} cited DOI entries; {bad} with differences")
