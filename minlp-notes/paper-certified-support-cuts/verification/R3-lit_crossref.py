"""R3-lit: compare references.bib entries that have DOIs with Crossref metadata.
Single-threaded, polite (sleeps between requests). Writes JSON to R3-lit_crossref.json."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import json, re, sys, time, unicodedata, urllib.request, urllib.parse

BIB = (_PUBLIC_REPO + '/paper-certified-support-cuts/references.bib')
OUT = (_PUBLIC_REPO + '/paper-certified-support-cuts/verification/R3-lit_crossref.json')

def parse_bib(text):
    entries = []
    for m in re.finditer(r'@(\w+)\s*\{\s*([^,]+),', text):
        start = m.end()
        depth = 1; i = start
        while depth and i < len(text):
            if text[i] == '{': depth += 1
            elif text[i] == '}': depth -= 1
            i += 1
        body = text[start:i-1]
        fields = {}
        j = 0
        for fm in re.finditer(r'(\w+)\s*=\s*', body):
            pass
        # simple field parser
        pos = 0
        while True:
            fm = re.compile(r'\s*(\w+)\s*=\s*').match(body, pos)
            if not fm:
                nxt = body.find(',', pos)
                if nxt < 0: break
                pos = nxt + 1
                continue
            name = fm.group(1).lower(); pos = fm.end()
            if body[pos] == '{':
                d = 1; k = pos + 1
                while d:
                    if body[k] == '{': d += 1
                    elif body[k] == '}': d -= 1
                    k += 1
                val = body[pos+1:k-1]; pos = k
            else:
                k = pos
                while k < len(body) and body[k] not in ',\n': k += 1
                val = body[pos:k].strip(); pos = k
            fields[name] = val
            nxt = body.find(',', pos)
            if nxt < 0: break
            pos = nxt + 1
        entries.append((m.group(1).lower(), m.group(2).strip(), fields))
    return entries

def norm(s):
    s = re.sub(r'\\[a-zA-Z]+\s*', '', s or '')
    s = s.replace('{', '').replace('}', '').replace('\\', '')
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()

def fetch(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    req = urllib.request.Request(url, headers={"User-Agent": "R3-lit-citation-audit/1.0 (mailto:noreply@example.org)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)["message"]
    except Exception as e:
        return {"error": str(e)}

def main():
    entries = parse_bib(open(BIB).read())
    res = []
    for typ, key, f in entries:
        doi = f.get('doi')
        if not doi:
            res.append({"key": key, "doi": None}); continue
        msg = fetch(doi); time.sleep(0.5)
        if "error" in msg:
            res.append({"key": key, "doi": doi, "error": msg["error"]}); print(key, "ERROR", msg["error"]); continue
        cr = {
            "title": (msg.get("title") or [""])[0],
            "container": (msg.get("container-title") or [""])[0],
            "volume": msg.get("volume"), "issue": msg.get("issue"), "page": msg.get("page"),
            "year_print": (msg.get("published-print") or msg.get("issued") or {}).get("date-parts", [[None]])[0][0],
            "year_issued": (msg.get("issued") or {}).get("date-parts", [[None]])[0][0],
            "year_online": (msg.get("published-online") or {}).get("date-parts", [[None]])[0][0],
            "authors": [ (a.get("given",""), a.get("family","")) for a in msg.get("author", [])],
            "editors": [ (a.get("given",""), a.get("family","")) for a in msg.get("editor", [])],
            "type": msg.get("type"),
        }
        issues = []
        if norm(cr["title"]) != norm(f.get("title")):
            issues.append(f"title: bib='{f.get('title')}' cr='{cr['title']}'")
        bauth = [a.strip() for a in re.split(r'\s+and\s+', f.get('author',''))]
        bfam = []
        for a in bauth:
            if ',' in a: bfam.append(norm(a.split(',')[0]))
            else: bfam.append(norm(a.split()[-1]) if a.split() else '')
        cfam = [norm(a[1]) for a in cr["authors"]]
        if cfam and [x.split()[-1] if x else x for x in bfam] != [x.split()[-1] if x else x for x in cfam]:
            issues.append(f"authors: bib={bfam} cr={cfam}")
        for fld, crf in (("volume","volume"),("number","issue")):
            if f.get(fld) and cr[crf] and norm(f[fld]) != norm(cr[crf]):
                issues.append(f"{fld}: bib={f[fld]} cr={cr[crf]}")
            if not f.get(fld) and cr[crf]:
                issues.append(f"{fld} missing in bib; cr={cr[crf]}")
        if f.get('pages') and cr["page"] and norm(f['pages'].replace('--','-')) != norm(cr["page"]):
            issues.append(f"pages: bib={f['pages']} cr={cr['page']}")
        if not f.get('pages') and cr['page']:
            issues.append(f"pages missing in bib; cr={cr['page']}")
        y = f.get('year')
        if y and str(cr["year_print"]) != y:
            issues.append(f"year: bib={y} cr_print={cr['year_print']} cr_issued={cr['year_issued']} cr_online={cr['year_online']}")
        venue = f.get('journal') or f.get('booktitle') or f.get('series') or ''
        res.append({"key": key, "doi": doi, "bib": f, "crossref": cr, "issues": issues})
        print(key, "OK" if not issues else "ISSUES", *issues, sep="\n   ")
        print("   venue bib:", venue, "| cr:", cr["container"])
    json.dump(res, open(OUT, "w"), indent=1)

main()
