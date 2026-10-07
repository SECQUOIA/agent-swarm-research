"""Round-2 literature review: check references.bib against Crossref and arXiv.

For every entry with a DOI, compare title, author family names (count and
order), container title, volume, issue, pages and year with Crossref.  For
every arXiv-only entry, compare title and authors with the arXiv API and
search Crossref by title for a later journal version.  Also report entries
that are in the .bib file but not cited in the sections.

Output: R9_literature_bibcheck.json next to this script, and a short text
summary on stdout.  Network access to api.crossref.org and export.arxiv.org
is required.  Single-threaded, polite delays.
"""
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
BIB = PAPER / "references.bib"
SECTIONS = PAPER / "sections"
UA = {"User-Agent": "minlp-notes-bibcheck/1.0 (mailto:noreply@example.org)"}


def parse_bib(text):
    entries = {}
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        etype, key = m.group(1).lower(), m.group(2)
        i = m.end()
        depth = 1
        j = i
        while j < len(text) and depth > 0:
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
            j += 1
        body = text[i:j - 1]
        fields = {}
        k = 0
        while k < len(body):
            fm = re.compile(r"\s*,?\s*(\w+)\s*=\s*").match(body, k)
            if not fm:
                break
            name = fm.group(1).lower()
            k = fm.end()
            if k < len(body) and body[k] == "{":
                d = 1
                s = k + 1
                k += 1
                while k < len(body) and d > 0:
                    if body[k] == "{":
                        d += 1
                    elif body[k] == "}":
                        d -= 1
                    k += 1
                val = body[s:k - 1]
            elif k < len(body) and body[k] == '"':
                e = body.index('"', k + 1)
                val = body[k + 1:e]
                k = e + 1
            else:
                vm = re.compile(r"[^,]+").match(body, k)
                val = vm.group(0).strip() if vm else ""
                k = vm.end() if vm else k + 1
            fields[name] = val
        entries[key] = (etype, fields)
    return entries


TEX_ACCENTS = {
    '"': "\u0308", "'": "\u0301", "`": "\u0300", "^": "\u0302",
    "~": "\u0303", "c": "\u0327", "v": "\u030c", "=": "\u0304",
}


def detex(s):
    s = re.sub(r"\\([\"'`^~=])\{?([A-Za-z])\}?", lambda m: m.group(2) + TEX_ACCENTS[m.group(1)], s)
    s = re.sub(r"\\([cv])\{([A-Za-z])\}", lambda m: m.group(2) + TEX_ACCENTS[m.group(1)], s)
    s = s.replace("\\i", "i").replace("\\l", "l").replace("\\o", "o")
    s = s.replace("\\&", "&").replace("---", "-").replace("--", "-")
    s = re.sub(r"\$[^$]*\$", "", s)
    s = re.sub(r"[{}\\]", "", s)
    return unicodedata.normalize("NFC", s)


def norm(s):
    s = unicodedata.normalize("NFKD", detex(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s.lower())


def bib_families(author_field):
    fams = []
    for a in re.split(r"\s+and\s+", author_field):
        a = a.strip()
        if not a:
            continue
        if "," in a:
            fam = a.split(",")[0]
        else:
            a2 = re.sub(r"\{([^}]*)\}", lambda m: m.group(1).replace(" ", "_"), a)
            fam = a2.split()[-1].replace("_", " ")
        fams.append(norm(fam))
    return fams


def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode())


def crossref(doi):
    try:
        return get_json("https://api.crossref.org/works/" + urllib.parse.quote(doi))["message"]
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


def crossref_search(title, author):
    q = urllib.parse.urlencode({"query.bibliographic": title, "query.author": author, "rows": 5})
    try:
        items = get_json("https://api.crossref.org/works?" + q)["message"]["items"]
    except Exception as exc:  # noqa: BLE001
        return [{"error": str(exc)}]
    out = []
    for it in items:
        out.append({
            "doi": it.get("DOI"), "title": (it.get("title") or [""])[0],
            "container": (it.get("container-title") or [""])[0],
            "type": it.get("type"),
            "issued": (it.get("issued", {}).get("date-parts") or [[None]])[0],
        })
    return out


def arxiv(aid):
    url = "https://export.arxiv.org/api/query?id_list=" + aid
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            root = ET.fromstring(r.read())
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}
    ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
    e = root.find("a:entry", ns)
    if e is None:
        return {"error": "no entry"}
    return {
        "id": e.findtext("a:id", default="", namespaces=ns),
        "title": " ".join((e.findtext("a:title", default="", namespaces=ns)).split()),
        "authors": [a.findtext("a:name", default="", namespaces=ns) for a in e.findall("a:author", ns)],
        "published": e.findtext("a:published", default="", namespaces=ns),
        "updated": e.findtext("a:updated", default="", namespaces=ns),
        "journal_ref": e.findtext("x:journal_ref", default="", namespaces=ns),
        "doi": e.findtext("x:doi", default="", namespaces=ns),
    }


def cr_pages(m):
    return (m.get("page") or "").replace("\u2013", "-")


def compare(key, fields, m):
    issues = []
    if "error" in m:
        return ["crossref error: " + m["error"]]
    ct = (m.get("title") or [""])[0]
    if norm(ct) != norm(fields.get("title", "")):
        issues.append(f"title differs: bib='{detex(fields.get('title',''))}' crossref='{ct}'")
    cf = [norm(a.get("family", a.get("name", ""))) for a in m.get("author", [])]
    bf = bib_families(fields.get("author", "")) if "author" in fields else []
    if bf and cf and bf != cf:
        issues.append(f"authors differ: bib={bf} crossref={cf}")
    cont = (m.get("container-title") or [""])
    cont = cont[0] if cont else ""
    bcont = fields.get("journal") or fields.get("booktitle") or fields.get("series") or ""
    if fields.get("journal") and norm(cont) != norm(bcont):
        issues.append(f"journal differs: bib='{detex(bcont)}' crossref='{cont}'")
    for fld, cval in (("volume", m.get("volume")), ("number", m.get("issue"))):
        bval = fields.get(fld)
        if bval and cval and norm(bval) != norm(cval):
            issues.append(f"{fld} differs: bib={bval} crossref={cval}")
        if not bval and cval and fields.get("journal"):
            issues.append(f"{fld} missing in bib (crossref {cval})")
    bp = fields.get("pages", "").replace("--", "-")
    cp = cr_pages(m)
    if bp and cp and norm(bp) != norm(cp):
        issues.append(f"pages differ: bib={bp} crossref={cp}")
    years = []
    for k in ("published-print", "issued", "published-online"):
        dp = m.get(k, {}).get("date-parts")
        if dp and dp[0] and dp[0][0]:
            years.append((k, dp[0][0]))
    by = fields.get("year")
    if by and years and int(by) not in [y for _, y in years]:
        issues.append(f"year differs: bib={by} crossref={years}")
    return issues


def main():
    text = BIB.read_text()
    entries = parse_bib(text)
    cited = set()
    for f in SECTIONS.glob("*.tex"):
        for m in re.finditer(r"\\cite[a-z]*\*?(?:\[[^\]]*\])*\{([^}]*)\}", f.read_text()):
            cited.update(k.strip() for k in m.group(1).split(","))
    res = {"uncited_bib_entries": sorted(set(entries) - cited),
           "cited_missing_from_bib": sorted(cited - set(entries)), "entries": {}}
    for key, (etype, fields) in entries.items():
        rec = {"type": etype}
        doi = fields.get("doi")
        aid = None
        for src in (fields.get("eprint", ""), fields.get("howpublished", ""), fields.get("url", "")):
            mm = re.search(r"(\d{4}\.\d{4,5})", src)
            if mm:
                aid = mm.group(1)
                break
        if doi and not doi.startswith("10.3929") and not doi.startswith("10.48550"):
            m = crossref(doi)
            rec["doi"] = doi
            rec["issues"] = compare(key, fields, m)
            time.sleep(0.3)
        if aid:
            a = arxiv(aid)
            rec["arxiv"] = a
            if "error" not in a:
                t_ok = norm(a["title"]) == norm(fields.get("title", ""))
                bf = bib_families(fields.get("author", ""))
                af = [norm(x.split()[-1]) for x in a["authors"]]
                rec.setdefault("issues", [])
                if not t_ok:
                    rec["issues"].append(f"arXiv title differs: '{a['title']}'")
                if bf and af and bf != af:
                    rec["issues"].append(f"arXiv authors differ: bib={bf} arxiv={af}")
            if not doi:
                first = bib_families(fields.get("author", "x"))[0] if fields.get("author") else ""
                rec["journal_search"] = crossref_search(detex(fields.get("title", "")), first)
            time.sleep(3.1)
        res["entries"][key] = rec
    out = HERE / "R9_literature_bibcheck.json"
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False))
    n_doi = sum(1 for r in res["entries"].values() if "doi" in r)
    n_arx = sum(1 for r in res["entries"].values() if "arxiv" in r)
    print(f"entries={len(entries)} doi_checked={n_doi} arxiv_checked={n_arx}")
    print("uncited:", res["uncited_bib_entries"])
    print("cited but missing:", res["cited_missing_from_bib"])
    for key, r in res["entries"].items():
        if r.get("issues"):
            print(f"- {key}: " + " | ".join(r["issues"]))
        if r.get("journal_search"):
            for hit in r["journal_search"][:3]:
                if "error" in hit:
                    continue
                if hit.get("type") == "journal-article" and norm(hit["title"])[:40] == norm(entries[key][1].get("title", ""))[:40]:
                    print(f"  * {key}: possible journal version {hit}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
