import csv, math
from decimal import Decimal as D
rows=list(csv.DictReader(open('results_table.csv')))
refs={r['instance']:r for r in csv.DictReader(open('references.csv'))}
out=[]
for r in rows:
    try: d=D(r['dual'])
    except Exception: continue
    if not d.is_finite(): continue
    sg=D(1) if r['sense'].lower().startswith('min') else D(-1)
    C=D(refs[r['instance']]['certificate_dual'])
    m=sg*(C-d); rel=m/abs(C) if C!=0 else None
    out.append((m,rel,r['instance'],r['solver'],r['globality_warning']))
out.sort()
for x in out[:8]: print('smallest',x[2],x[3],'abs %.4g'%x[0],'rel %.3g'%x[1] if x[1] is not None else '', 'warn' if x[4].lower()=='true' else '')
for x in out[-3:]: print('largest',x[2],x[3],'abs %.4g'%x[0])
from collections import Counter
dec=Counter(math.floor(math.log10(float(x[1]))) for x in out if x[1] is not None and x[1]>0)
print('relative margin decades',sorted(dec.items()))
# per instance strongest dual vs certificate
best={}
for x in out:
    i=x[2]
    if i not in best or x[0]<best[i][0]: best[i]=x
print('instances with a finite dual',len(best))
for i,x in sorted(best.items(), key=lambda t:t[1][1] if t[1][1] is not None else 0):
    print('  %-16s %-6s abs %.4g rel %.3g'%(i,x[3],x[0],x[1]))
