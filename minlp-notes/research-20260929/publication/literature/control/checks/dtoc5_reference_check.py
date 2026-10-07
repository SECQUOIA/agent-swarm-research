"""Check the saved reference point and master-source default-bound inference."""
from pathlib import Path
from fractions import Fraction as Q
import hashlib
import re
p=Path(__file__).resolve().parents[1]
f=p/'sources/qplib/QPLIB_8585.sol'
url='https://qplib.zib.de/sol/QPLIB_8585.sol'
data=f.read_bytes()
h=hashlib.sha256(data).hexdigest()
assert h=='9d9f5c4fbfc73aa6bfa3ae94ae7a1d44832a5fd7a30927a7941e2e8dcdf455cd'
values=[(nm,Q(v)) for nm,v in (l.split() for l in data.decode().splitlines()) if nm.startswith('x')]
assert len(values)==99998  # QPLIB .sol omits the zero coordinate.
name,m=max(values,key=lambda x:x[1]);assert m<100
min_name,min_value=min(values,key=lambda x:x[1]);assert min_value>0
log=(p/'sources/mittelmann_cnconv/logs/QPLIB_8585.mnt').read_text()
defaults={side:int(re.search(r'Default '+side+r' bound was assumed for (\d+) variables',log)[1])
          for side in ['lower','upper']}
excerpt=(p/'sources/qplib/QPLIB_8585_excerpt.txt').read_text()
nvars=int(re.search(r'^(\d+) # number of variables$',excerpt,re.M)[1])
assert len(values)+1==nvars
finite_lower=nvars-defaults['lower'];finite_upper=nvars-defaults['upper']
extra_lower=finite_lower-finite_upper
assert (defaults['upper'],defaults['lower'],extra_lower)==(99997,99983,14)
print('Saved file',f.name,'URL',url,'sha256',h,'matches saved r2 hash')
print('min listed x',min_name,str(min_value),'decimal',float(min_value))
print('max x',name,str(m),'decimal',float(m),'below upper default 100; all listed coordinates positive, omitted coordinates zero')
print('The master rule uses the smallest finite lower bound and largest finite upper bound separately.')
print(f'{nvars} variables; {finite_upper} finite upper bounds; {finite_lower} finite lower bounds (from saved warning counts).')
print(f"{defaults['upper']} upper defaults are consistent with 100; {defaults['lower']} lower defaults imply {extra_lower} extra finite lower bounds, so the lower default is unknown.")
print('The lower default is negative in every branch of the rule; the reference point is contained even without knowing its magnitude.')
print('PASS: saved-reference containment under the master rule; benchmark revision may differ; not a feasibility or optimality proof.')
