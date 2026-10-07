"""Run arXiv API queries; print id, date, title, authors. Usage: python3 arxiv_search.py 'q1' 'q2' ..."""
import sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
ns = {"a": "http://www.w3.org/2005/Atom"}
for q in sys.argv[1:]:
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": q, "start": 0, "max_results": 50, "sortBy": "submittedDate", "sortOrder": "descending"})
    for k in range(5):
        try:
            data = urllib.request.urlopen(url, timeout=60).read(); break
        except Exception:
            time.sleep(10)
    root = ET.fromstring(data)
    es = root.findall("a:entry", ns)
    print(f"### {q}  ({len(es)} hits)")
    for e in es:
        i = e.find("a:id", ns).text.split("/abs/")[-1]
        t = " ".join(e.find("a:title", ns).text.split())
        au = ", ".join(a.find("a:name", ns).text for a in e.findall("a:author", ns)[:5])
        print(f"{i} | {e.find('a:published', ns).text[:10]} | {t} | {au}")
    time.sleep(4)
