"""R9 (literature lens): check references.bib against Crossref (DOI entries) and the
arXiv API (arXiv-only entries). Single-threaded, polite. Prints only mismatches and
writes a JSON record next to this script.

Fields compared: title (normalized), author family names (order and count), container,
volume, issue, first/last page, year (print year, falling back to issued year).
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import json, re, time, unicodedata, urllib.request, urllib.parse
import xml.etree.ElementTree as ET

BIB = (_PUBLIC_REPO + '/paper-certified-support-cuts/references.bib')
OUT = (_PUBLIC_REPO + '/paper-certified-support-cuts/verification/R9_literature_crossref.json')
UA = {"User-Agent": "R9-literature-audit/1.0 (mailto:noreply@example.org)"}


def parse_bib(text):
    out = []
    for m in re.finditer(r'@(\w+)\s*\{\s*([^,]+),', text):
        i, depth = m.end(), 1
        while depth and i < len(text):
            depth += {'{': 1, '}': -1}.get(text[i], 0)
            i += 1
        body = text[m.end():i - 1]
        fields, pos = {}, 0
        pat = re.compile(r'\s*(\w+)\s*=\s*')
        while True:
            fm = pat.match(body, pos)
            if not fm:
                nxt = body.find(',', pos)
                if nxt < 0:
                    break
                pos = nxt + 1
                continue
            name, pos = fm.group(1).lower(), fm.end()
            if pos < len(body) and body[pos] == '{':
                d, k = 1, pos + 1
                while d:
                    d += {'{': 1, '}': -1}.get(body[k], 0)
                    k += 1
                val, pos = body[pos + 1:k - 1], k
            else:
                k = pos
                while k < len(body) and body[k] not in ',\n':
                    k += 1
                val, pos = body[pos:k].strip(), k
            fields[name] = val
            nxt = body.find(',', pos)
            if nxt < 0:
                break
            pos = nxt + 1
        out.append((m.group(1).lower(), m.group(2).strip(), fields))
    return out


def norm(s):
    s = s or ''
    s = s.replace('{\\ss}', 'ss').replace('\\l', 'l')
    s = re.sub(r'\\[a-zA-Z]+\s*', '', s)
    s = s.replace('{', '').replace('}', '').replace('\\', '').replace('$', '')
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()


def bib_families(auth):
    fams = []
    for a in re.split(r'\s+and\s+', auth or ''):
        a = a.strip()
        if not a:
            continue
        if ',' in a:
            fam = a.split(',')[0]
        else:
            # braces protect multiword family names
            mm = re.search(r'\{([^{}]*)\}\s*$', a)
            fam = mm.group(1) if mm else a.split()[-1]
        fams.append(norm(fam).split()[-1] if norm(fam) else '')
    return fams


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read()


def crossref(doi):
    try:
        return json.loads(get("https://api.crossref.org/works/" + urllib.parse.quote(doi)))["message"]
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}


def arxiv(aid):
    try:
        x = get("http://export.arxiv.org/api/query?id_list=" + aid)
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}
    ns = {"a": "http://www.w3.org/2005/Atom", "ar": "http://arxiv.org/schemas/atom"}
    root = ET.fromstring(x)
    ent = root.find("a:entry", ns)
    if ent is None or ent.find("a:title", ns) is None:
        return {"error": "not found"}
    return {
        "title": " ".join(ent.find("a:title", ns).text.split()),
        "authors": [a.find("a:name", ns).text for a in ent.findall("a:author", ns)],
        "published": ent.find("a:published", ns).text,
        "updated": ent.find("a:updated", ns).text,
        "journal_ref": (ent.find("ar:journal_ref", ns).text if ent.find("ar:journal_ref", ns) is not None else None),
        "doi": (ent.find("ar:doi", ns).text if ent.find("ar:doi", ns) is not None else None),
    }


def main():
    entries = parse_bib(open(BIB).read())
    report = []
    for typ, key, f in entries:
        rec = {"key": key, "type": typ}
        doi = f.get("doi")
        aid = None
        for fld in ("howpublished", "url", "eprint"):
            mm = re.search(r'(\d{4}\.\d{4,5})', f.get(fld, ''))
            if mm:
                aid = mm.group(1)
                break
        issues = []
        if doi and not doi.startswith("10.3929"):
            msg = crossref(doi)
            time.sleep(0.4)
            if "error" in msg:
                issues.append("crossref error: " + msg["error"])
            else:
                cr_title = " ".join((msg.get("title") or [""])[0].split())
                cr_sub = " ".join((msg.get("subtitle") or [""])[0].split()) if msg.get("subtitle") else ""
                cr_cont = (msg.get("container-title") or [""])[0]
                cr_fams = [norm(a.get("family", a.get("name", ""))).split()[-1] if norm(a.get("family", a.get("name", ""))) else ''
                           for a in msg.get("author", [])]
                yp = (msg.get("published-print") or msg.get("issued") or {}).get("date-parts", [[None]])[0][0]
                rec["crossref"] = {"title": cr_title, "subtitle": cr_sub, "container": cr_cont,
                                   "volume": msg.get("volume"), "issue": msg.get("issue"),
                                   "page": msg.get("page"), "year": yp, "authors": cr_fams}
                bt = norm(f.get("title"))
                ct = norm(cr_title + (" " + cr_sub if cr_sub else ""))
                if bt != ct and bt != norm(cr_title):
                    issues.append(f"title: bib='{f.get('title')}' crossref='{cr_title}{(': ' + cr_sub) if cr_sub else ''}'")
                bf = bib_families(f.get("author"))
                if cr_fams and bf != cr_fams:
                    issues.append(f"authors: bib={bf} crossref={cr_fams}")
                if f.get("volume") and msg.get("volume") and norm(f["volume"]) != norm(msg["volume"]):
                    issues.append(f"volume: bib={f['volume']} crossref={msg['volume']}")
                if msg.get("issue") and norm(f.get("number", "")) != norm(msg["issue"]):
                    issues.append(f"issue: bib={f.get('number')} crossref={msg['issue']}")
                if msg.get("page"):
                    bp = re.sub(r'-+', '-', f.get("pages", "")).replace(' ', '')
                    if bp != msg["page"].replace(' ', ''):
                        issues.append(f"pages: bib={f.get('pages')} crossref={msg['page']}")
                if yp and str(yp) != f.get("year", "").strip():
                    issues.append(f"year: bib={f.get('year')} crossref(print/issued)={yp}")
                bc = norm(f.get("journal") or f.get("booktitle") or "")
                if typ == "article" and cr_cont and bc and bc != norm(cr_cont):
                    issues.append(f"container: bib='{f.get('journal')}' crossref='{cr_cont}'")
        elif aid:
            a = arxiv(aid)
            time.sleep(3.0)
            rec["arxiv"] = a
            if "error" in a:
                issues.append("arxiv error: " + a["error"])
            else:
                if norm(a["title"]) != norm(f.get("title")):
                    issues.append(f"title: bib='{f.get('title')}' arXiv='{a['title']}'")
                af = [norm(x).split()[-1] for x in a["authors"]]
                bf = bib_families(f.get("author"))
                if af != bf:
                    issues.append(f"authors: bib={bf} arXiv={af}")
                if a.get("journal_ref") or a.get("doi"):
                    issues.append(f"arXiv lists journal_ref={a.get('journal_ref')} doi={a.get('doi')}")
                rec["arxiv_dates"] = (a["published"], a["updated"])
        else:
            rec["note"] = "no DOI or arXiv id; not checked"
        rec["issues"] = issues
        report.append(rec)
        if issues:
            print(key)
            for s in issues:
                print("   ", s)
    json.dump(report, open(OUT, "w"), indent=1)
    print("checked", len(report), "entries;", sum(1 for r in report if r["issues"]), "with issues")


if __name__ == "__main__":
    main()
