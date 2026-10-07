"""Re-fetch the four (i-r) instance pages and their five points (sequential,
1 s delay); compare with the stored copies; also parse the author's
pages_live/ copies with the reviewer's parser."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import hashlib, os, time, urllib.request
import step4_pages as S

AU = (_PUBLIC_REPO + '/research-20260929/publication/audit-ir/pages_live/')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'live')
for n in ['eniplac', 'lop97icx', 'spring', 'stockcycle']:
    data = urllib.request.urlopen('https://www.minlplib.org/%s.html' % n, timeout=60).read()
    open(os.path.join(OUT, n + '.html'), 'wb').write(data)
    a, _ = S.parse_page(S.PAGES + n + '.html')
    b, _ = S.parse_page(os.path.join(OUT, n + '.html'))
    print(n, 'page parse unchanged since 2026-09-30:', a == b)
    time.sleep(1)
for p in ['eniplac.p2', 'lop97icx.p2', 'spring.p2', 'spring.p3', 'stockcycle.p2']:
    data = urllib.request.urlopen('https://www.minlplib.org/sol/%s.sol' % p, timeout=60).read()
    open(os.path.join(OUT, p + '.sol'), 'wb').write(data)
    old = open(S.BA + 'sol/' + p + '.sol', 'rb').read()
    print(p, 'sol identical to bound-audit/sol:', old == data)
    time.sleep(1)
same = 0
fs = sorted(f for f in os.listdir(AU) if f.endswith('.html'))
for f in fs:
    a, _ = S.parse_page(S.PAGES + f)
    b, _ = S.parse_page(AU + f)
    same += a == b
print("author's live copies: %d of %d parse identical to stored pages" % (same, len(fs)))
