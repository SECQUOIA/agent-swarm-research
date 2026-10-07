"""Re-fetch the 23 finding pages from www.minlplib.org (sequential, 1 s
delay) and compare their parsed points and dual bounds with the parse of the
stored copies in bound-audit/pages/ (fetched 2026-09-30)."""
import os
import time
import urllib.request

import parse_check as pc

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'pages_live')
os.makedirs(OUT, exist_ok=True)

same = diff = 0
for name in pc.finding_pages():
    data = urllib.request.urlopen('https://www.minlplib.org/%s.html' % name,
                                  timeout=60).read()
    path = os.path.join(OUT, name + '.html')
    open(path, 'wb').write(data)
    a = pc.parse_page(os.path.join(pc.PAGES, name + '.html'))
    b = pc.parse_page(path)
    keys = ('problem_type', 'sense', 'points', 'duals')
    ok = all(a[k] == b[k] for k in keys)
    same += ok
    diff += not ok
    print(name, 'unchanged' if ok else 'CHANGED: ' + ', '.join(k for k in keys if a[k] != b[k]))
    time.sleep(1)
print('unchanged %d, changed %d' % (same, diff))
