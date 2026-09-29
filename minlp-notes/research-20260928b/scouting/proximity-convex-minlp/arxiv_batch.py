import sys, time, urllib.request, urllib.parse, xml.etree.ElementTree as ET
ns={'a':'http://www.w3.org/2005/Atom'}
qs = sys.argv[1:]
for q in qs:
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode({"search_query": q, "start": 0, "max_results": 30, "sortBy": "submittedDate", "sortOrder": "descending"})
    for attempt in range(3):
        try:
            data = urllib.request.urlopen(url, timeout=60).read()
            break
        except Exception as ex:
            print("ERR", ex); time.sleep(10)
    else:
        continue
    print("### ", q)
    t = ET.fromstring(data)
    for e in t.findall('a:entry', ns):
        i = e.find('a:id', ns).text.split('/abs/')[-1]
        ti = ' '.join(e.find('a:title', ns).text.split())
        d = e.find('a:published', ns).text[:10]
        au = ', '.join(a.find('a:name', ns).text for a in e.findall('a:author', ns))[:60]
        print(d, i, '|', ti[:105], '|', au)
    time.sleep(5)
