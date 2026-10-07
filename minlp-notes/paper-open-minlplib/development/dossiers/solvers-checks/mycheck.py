# Independent exact checker written for the dossier (no shared code with track/reviewer).
import re, json, sys
from fractions import Fraction as F
def num(s):
    s=s.strip()
    if s in ('+inf','inf'): return None
    if s=='-inf': return None
    return F(s)
def parse(path):
    txt=open(path).read()
    sense=re.search(r'Sense\s*:\s*(\w+)',txt).group(1)
    vars={}
    for m in re.finditer(r'\[(binary|continuous|integer)\]\s*<([^>]+)>:\s*obj=([^,]+),\s*original bounds=\[([^,]+),([^\]]+)\]',txt):
        t,n,o,lo,hi=m.groups()
        vars[n]=(t,F(o),None if 'inf' in lo else F(lo),None if 'inf' in hi else F(hi))
    cons=[]
    body=txt.split('CONSTRAINTS',1)[1]
    for line in body.splitlines():
        line=line.strip()
        if not line.startswith('['): continue
        m=re.match(r'\[(linear|nonlinear)\]\s*<([^>]+)>:\s*(.*);$',line)
        kind,name,expr=m.groups()
        # ranged?  lhs <= expr <= rhs
        rm=re.match(r'^(-?[0-9.e+\-]+)\s*<=\s*(.*)\s*<=\s*(-?[0-9.e+\-]+)$',expr)
        if rm:
            lhs,ex,rhs=rm.groups(); sides=[('>=',F(lhs)),('<=',F(rhs))]
        else:
            mm=re.match(r'^(.*?)\s*(==|<=|>=)\s*([-+0-9.e]+)$',expr)
            ex,op,rhs=mm.groups(); sides=[(op,F(rhs))]
        terms=[]
        if kind=='linear':
            for c,v in re.findall(r'([+-][0-9.e+\-]*?)<([^>]+)>',ex):
                terms.append((F(c+'1') if c in '+-' else F(c),[v]))
        else:
            for c,vs in re.findall(r'([+-]?[0-9.e+\-]+)\*((?:<[^>]+>\*?)+)',ex):
                terms.append((F(c),re.findall(r'<([^>]+)>',vs)))
        # sanity: re-render count of '<'
        assert sum(len(t[1]) for t in terms)==ex.count('<'), (name,ex,terms)
        cons.append((name,terms,sides))
    return sense,vars,cons
def check(cip,wit):
    sense,vars,cons=parse(cip)
    w={k:F(v) for k,v in json.load(open(wit)).items()}
    missing=[v for v in vars if v not in w]
    x={v:w.get(v,F(0)) for v in vars}
    viol=[]
    for n,(t,o,lo,hi) in vars.items():
        if lo is not None and x[n]<lo: viol.append(('lb',n))
        if hi is not None and x[n]>hi: viol.append(('ub',n))
        if t in('binary','integer') and x[n].denominator!=1: viol.append(('int',n))
    for name,terms,sides in cons:
        val=F(0)
        for c,vs in terms:
            p=c
            for v in vs: p*=x[v]
            val+=p
        for op,r in sides:
            ok = (val==r) if op=='==' else (val<=r if op=='<=' else val>=r)
            if not ok: viol.append((name,op,float(val-r)))
    obj=sum(o*x[n] for n,(t,o,lo,hi) in vars.items())
    return len(vars),len(cons),len(missing),viol,obj
for cip,wit,claim in [('p0.cip','p0.json','169.950250085232'),('p4.cip','p4.json','-6.72988938834578'),('p5.cip','p5.json','-231.905843299873'),('pair2236.cip','pair2236.json','56.4920384487893'),('fm336_v1010.cip','fm336_v1010.witness.json','0.814125'),('fm318_master.cip','fm318_master.witness.json','2.0'),('tiny2.cip','tiny2_witness.json','-1.23108446311479'),('pumps_default.cip','pumps_default_witness.json','1.19799998144798')]:
    nv,nc,miss,viol,obj=check(cip,wit)
    print(f"{cip}: vars {nv} rows {nc} missing-in-witness {miss} violations {len(viol)} {viol[:3]} obj {float(obj):.12f} exact={obj if obj.denominator<10**6 else ''} obj-claim {float(obj-F(claim)):.4e}")
