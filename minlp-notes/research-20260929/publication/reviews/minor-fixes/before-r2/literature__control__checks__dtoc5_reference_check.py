"""Fetch one reference point and check its scale; do not solve the model."""
from pathlib import Path
from fractions import Fraction as Q
import urllib.request,hashlib
p=Path(__file__).resolve().parents[1]
f=p/'sources/qplib/QPLIB_8585.sol'
url='https://qplib.zib.de/sol/QPLIB_8585.sol'
with urllib.request.urlopen(url,timeout=30) as r:data=r.read()
f.write_bytes(data)
h=hashlib.sha256(data).hexdigest()
assert h=='9d9f5c4fbfc73aa6bfa3ae94ae7a1d44832a5fd7a30927a7941e2e8dcdf455cd'
values=[(nm,abs(Q(v))) for nm,v in (l.split() for l in data.decode().splitlines()) if nm.startswith('x')]
assert len(values)==99998  # QPLIB .sol omits the zero coordinate.
name,m=max(values,key=lambda x:x[1]);assert m<100
print('URL',url,'sha256',h,'matches saved r2 hash')
print('max |x|',name,str(m),'decimal',float(m),'inside [-100,100]; omitted zero coordinates cannot increase the maximum')
print('PASS: sole-finite-bound default box contains the saved reference point; not a feasibility or optimality proof.')
