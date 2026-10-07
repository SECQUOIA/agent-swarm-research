import csv
from decimal import Decimal, getcontext
getcontext().prec=60
rows=list(csv.DictReader(open('results_table.csv')))
print(len(rows))
from collections import Counter
fin=Counter(); prim=Counter(); claims=Counter(); valid=Counter(); warn=Counter()
def finite(s):
    if s in ('','—','-Infinity','Infinity','NA','-inf','inf'): return False
    try:
        v=Decimal(s); return abs(v)<Decimal('1e50')
    except Exception: return False
mind=None
osil=0; R=0
for r in rows:
    s=r['solver']
    if r['valid_time_measurement']=='True': valid[s]+=1
    if finite(r['dual']):
        fin[s]+=1
        if r['globality_warning']=='True': warn[s]+=1
        sgn = 1 if r['sense']=='min' else -1
        C=Decimal(r['certificate_dual']); D=Decimal(r['dual'])
        deficit=sgn*(C-D)
        if mind is None or deficit<mind[0]: mind=(deficit,r['instance'],s)
        if r['certificate_scope']=='OSIL': osil+=1
        else: R+=1
        P=Decimal(r['reference_primal'])
        if sgn*(D-P)>0: print('CUTOFF', r['instance'], s)
    if finite(r['primal']) : prim[s]+=1
    if r['optimality_claim']=='True': claims[s]+=1
print('finite',fin,sum(fin.values()),'warn',warn)
print('primal(finite field)',prim)
print('claims',claims,'valid',valid)
print('min deficit',mind)
print('osil',osil,'R',R)
print(Counter(r['certificate_scope'] for r in rows))
print(Counter(r['status'] for r in rows))
