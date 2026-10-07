# Independent exact checker for SCIP CIP files (subset used here) and JSON witnesses.
import re, json, sys
from fractions import Fraction as F
def parse_cip(path):
    txt=open(path).read()
    sense=re.search(r'Sense\s*:\s*(\w+)',txt).group(1)
    off=re.search(r'Offset\s*:\s*([-+\d.eE]+)',txt)
    V={}
    for m in re.finditer(r'\[(binary|integer|continuous)\]\s*<([^>]+)>:\s*obj=([-+\d.eE]+),\s*original bounds=\[([^,\]]+),([^\]]+)\]',txt):
        t,n,o,l,u=m.groups()
        cv=lambda s:None if s.strip() in('-inf','+inf','inf') else F(s.strip())
        V[n]=(t,F(o),cv(l),cv(u))
    C=[]
    for m in re.finditer(r'\[(linear|nonlinear)\]\s*<([^>]+)>:\s*(.*?);\s*$',txt,re.M):
        typ,name,body=m.groups()
        mm=re.match(r'^(?:([-+\d.eE]+)\s*<=\s*)?(.*?)\s*(<=|>=|==)\s*([-+\d.eE]+)$',body.strip())
        lhs_lo,expr,op,rhs=mm.groups()
        terms=[]
        if typ=='linear':
            for t in re.finditer(r'([-+][\d.eE+-]*?)<([^>]+)>',expr):
                c=t.group(1); c=F(c+'1') if c in('+','-') else F(c); terms.append((c,(t.group(2),)))
            chk=re.sub(r'([-+][\d.eE+-]*?)<([^>]+)>','',expr).strip()
        else:
            for t in re.finditer(r'([-+][\d.eE]+)((?:\*<[^>]+>)+)',expr):
                c=F(t.group(1)); vs=tuple(re.findall(r'<([^>]+)>',t.group(2))); terms.append((c,vs))
            chk=re.sub(r'([-+][\d.eE]+)((?:\*<[^>]+>)+)','',expr).strip()
        assert chk=='',(path,name,chk)
        C.append((name,terms,op,F(rhs),F(lhs_lo) if lhs_lo else None))
    return sense,V,C,(F(off.group(1)) if off else F(0))
def check(cip,wit,claims):
    sense,V,C,off=parse_cip(cip); x={k:F(v) for k,v in json.load(open(wit)).items()}
    bad=[]
    miss=[n for n in V if n not in x]
    for n,(t,o,l,u) in V.items():
        v=x.get(n,F(0))
        if l is not None and v<l: bad.append(('lb',n))
        if u is not None and v>u: bad.append(('ub',n))
        if t=='binary' and v not in (0,1): bad.append(('int',n))
    for name,terms,op,rhs,lo in C:
        val=F(0)
        for c,vs in terms:
            p=c
            for v in vs: p*=x.get(v,F(0))
            val+=p
        ok = (val<=rhs) if op=='<=' else (val>=rhs) if op=='>=' else (val==rhs)
        if lo is not None: ok = ok and val>=lo
        if not ok: bad.append(('row',name,float(val-rhs)))
    obj=off+sum(o*x.get(n,F(0)) for n,(t,o,l,u) in V.items())
    print(f"{cip}: vars {len(V)} cons {len(C)} missing {len(miss)} violations {bad[:3]} obj={obj} ~ {float(obj):.12f}; min claim - obj = {float(min(claims)-obj):.4e}")
    return obj
cases=[('p0.cip','p0.json',['169.950250085232']),('p4.cip','p4.json',['-6.72988938834578']),('p5.cip','p5.json',['-231.905843299873']),
 ('pair2236.cip','pair2236.json',['56.4920384487893']),('tiny2.cip','tiny2_witness.json',['-1.23108446311479']),
 ('pumps_default.cip','pumps_default_witness.json',['1.19799998144798']),('fm336_v1010.cip','fm336_v1010.witness.json',['0.814125','1.50521312595154']),
 ('fm318_master.cip','fm318_master.witness.json',['2.0'])]
for cip,w,cl in cases: check(cip,w,[F(c) for c in cl])
# mutation test on p4
import copy
sense,V,C,off=parse_cip('p4.cip'); base={k:F(v) for k,v in json.load(open('p4.json')).items()}
for mut in [('x546',F(1,10**30)),('x995',F(-1,10**30)),('b6',None)]:
    x=dict(base)
    if mut[1] is None: x['b6']=F(1,2)
    else: x[mut[0]]+=mut[1]
    json.dump({k:str(v) for k,v in x.items()},open('/tmp/solv2/scip/mut.json','w'))
    try: check('p4.cip','mut.json',[F('-6.72988938834578')])
    except Exception as e: print('mut err',e)
