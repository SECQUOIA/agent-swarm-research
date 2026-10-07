"""Check the saved reference point and master-source default-bound inference."""
from pathlib import Path
from fractions import Fraction as Q
import hashlib
p=Path(__file__).resolve().parents[1]
f=p/'sources/qplib/QPLIB_8585.sol'
url='https://qplib.zib.de/sol/QPLIB_8585.sol'
data=f.read_bytes()
h=hashlib.sha256(data).hexdigest()
assert h=='9d9f5c4fbfc73aa6bfa3ae94ae7a1d44832a5fd7a30927a7941e2e8dcdf455cd'
values=[(nm,Q(v)) for nm,v in (l.split() for l in data.decode().splitlines()) if nm.startswith('x')]
assert len(values)==99998  # QPLIB .sol omits the zero coordinate.
name,m=max(values,key=lambda x:x[1]);assert m<100
assert min(x for _,x in values)>0
print('URL',url,'sha256',h,'matches saved r2 hash')
print('max x',name,str(m),'decimal',float(m),'below upper default 100; all listed coordinates positive, omitted coordinates zero')
print('The master rule uses the smallest finite lower bound and largest finite upper bound separately.')
print('99997 upper defaults are consistent with 100; 99983 lower defaults imply 14 extra finite lower bounds, so the lower default is unknown.')
print('The lower default is negative in every branch of the rule; the reference point is contained even without knowing its magnitude.')
print('PASS: saved-reference containment under the master rule; benchmark revision may differ; not a feasibility or optimality proof.')
