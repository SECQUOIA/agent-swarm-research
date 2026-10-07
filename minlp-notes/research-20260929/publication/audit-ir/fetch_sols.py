"""Re-download the MINLPLib points used by the (i-r) check, sequentially
with a 1 s delay, and compare them byte for byte with bound-audit/sol/.
spring.p1 (the 2001 point whose value equals the five listed duals) is not
in bound-audit/sol/ and is fetched for reference."""
import hashlib
import os
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OLD = os.path.join(HERE, '..', '..', 'bound-audit', 'sol')
NEW = os.path.join(HERE, 'sol_live')
POINTS = ['eniplac.p2', 'lop97icx.p2', 'spring.p2', 'spring.p3', 'stockcycle.p2',
          'spring.p1']

os.makedirs(NEW, exist_ok=True)
for p in POINTS:
    url = 'https://www.minlplib.org/sol/%s.sol' % p
    data = urllib.request.urlopen(url, timeout=60).read()
    open(os.path.join(NEW, p + '.sol'), 'wb').write(data)
    old = os.path.join(OLD, p + '.sol')
    if os.path.exists(old):
        same = open(old, 'rb').read() == data
        print(p, 'bytes', len(data), 'identical to bound-audit/sol' if same else 'DIFFERENT',
              hashlib.sha256(data).hexdigest()[:16])
    else:
        print(p, 'bytes', len(data), 'not in bound-audit/sol (reference only)',
              hashlib.sha256(data).hexdigest()[:16])
    time.sleep(1)
