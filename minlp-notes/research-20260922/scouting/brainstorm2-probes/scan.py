import sys, csv, math, collections, os
sys.path.insert(0,'/home/sgusev/repo/minlp-notes/research-20260922/scouting/minlplib-open-data')
from osil import read, V
D='/home/sgusev/.cache/minlplib/minlplib/osil/'
rows=list(csv.DictReader(open('/home/sgusev/repo/minlp-notes/research-20260922/scouting/minlplib-open-data/open.csv')))
def bil_terms(R):
    """yield (i,j) bilinear var products and univariate atoms from a row"""
    out=[(i,j) for i,j,c in R['quad'] if i!=j]
    uni=[('sq',i) for i,j,c in R['quad'] if i==j]
    def walk(t,coef_ok=True):
        op=t[0]
        if op in('num','var'): return
        if op in('sum','negate'):
            for c in t[1:]: walk(c)
            return
        if op=='times':
            nc=[c for c in t[1:] if V(c)]
            if len(nc)==2 and all(c[0]=='var' for c in nc): out.append((nc[0][1],nc[1][1])); return
            if len(nc)==1: walk(nc[0]); return
            for c in nc: walk(c)
            return
        vs=V(t)
        if len(vs)==1:
            v=next(iter(vs))
            if op in ('power','square','signpower'):
                p=t[2][1] if len(t)>2 and t[2][0]=='num' else 2
                uni.append((f'{op}{p:g}',v)); 
            else: uni.append((op,v))
            return
        for c in t[1:]: walk(c)
    if R['nl'] is not None: walk(R['nl'])
    return out,uni
res=[]
for x in rows:
    f=D+x['name']+'.osil'
    if not os.path.exists(f) or os.path.getsize(f)>40e6: continue
    try: I=read(f)
    except Exception as e: print('ERR',x['name'],e); continue
    lam_rows=collections.defaultdict(set)   # candidate lambda -> rows where it multiplies something (equality rows)
    lam_part=collections.defaultdict(set)
    uniatoms=collections.defaultdict(set)
    trig_unb=set()
    for r,R in I['rows'].items():
        b,u=bil_terms(R)
        eq = r>=0 and R['lb']==R['ub']
        for i,j in b:
            if eq:
                lam_rows[i].add(r); lam_part[i].add(j); lam_rows[j].add(r); lam_part[j].add(i)
        for kind,v in u:
            uniatoms[v].add(kind)
            if kind in('sin','cos') and (math.isinf(I['lb'][v]) or math.isinf(I['ub'][v])): trig_unb.add(v)
        if R['nl'] is not None:
            def tw(t):
                if t[0] in('sin','cos'):
                    for v in V(t[1]):
                        if math.isinf(I['lb'][v]) or math.isinf(I['ub'][v]): trig_unb.add(v)
                if t[0] not in('num','var'):
                    for c in t[1:]: tw(c)
            tw(R['nl'])
    # eigen-like: variable multiplying >=4 distinct partners each in distinct equality rows, partners continuous
    eig=[v for v in lam_rows if len(lam_rows[v])>=4 and len(lam_part[v])>=4 and I['vt'][v]=='C' and len(lam_rows[v])==len(lam_part[v])]
    multi=[v for v,s in uniatoms.items() if len(s)>=2]
    res.append((x['name'],x['family'],len(eig),len(multi),len(trig_unb),x['gap'][:6]))
    print(*res[-1],flush=True)
