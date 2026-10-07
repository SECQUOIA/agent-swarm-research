#!/usr/bin/env python3
"""Fetch Crossref metadata for DOIs (one per line on stdin) and print a compact record.
Used by the lit-ext audit to verify BibTeX metadata (authors, title, venue, year, volume, issue, pages)."""
import sys, json, time, urllib.request, urllib.parse, concurrent.futures as cf
def get(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    req = urllib.request.Request(url, headers={"User-Agent": "lit-audit/1.0 (mailto:noreply@example.org)"})
    for attempt in range(4):
        try:
            m = json.load(urllib.request.urlopen(req, timeout=40))["message"]
            break
        except Exception as e:
            err = e
            time.sleep(3 * (attempt + 1))
    else:
        return f"{doi}\n   ERROR {err}"
    au = "; ".join(f"{a.get('family','?')}, {a.get('given','')}" for a in m.get("author", []))
    ed = "; ".join(f"{a.get('family','?')}, {a.get('given','')}" for a in m.get("editor", []))
    yr = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
    return (f"{doi}\n   AU: {au}\n   TI: {' '.join(m.get('title', ['?']))}\n"
            f"   IN: {' | '.join(m.get('container-title', []))}  vol={m.get('volume')} no={m.get('issue')} pp={m.get('page')} art={m.get('article-number')} yr={yr} type={m.get('type')}"
            + (f"\n   ED: {ed}" if ed else "") + (f"\n   PUB: {m.get('publisher')}" if m.get('type') in ('book','book-chapter','monograph','edited-book','proceedings-article') else ""))
dois = [l.strip() for l in sys.stdin if l.strip() and not l.startswith('#')]
with cf.ThreadPoolExecutor(2) as ex:
    for r in ex.map(get, dois):
        print(r)
