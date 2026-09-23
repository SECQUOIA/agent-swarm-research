import re, sys
from fractions import Fraction as F
import xml.etree.ElementTree as ET
NS='{os.optimizationservices.org}'
def num(s):
    s=s.strip()
    if s in ('INF','+INF'): return 'INF'
    if s=='-INF': return '-INF'
    return F(s)
def expand(elem):
    out=[]
    for el in elem.findall(NS+'el'):
        v=el.text.strip(); m=int(el.get('mult','1')); inc=el.get('incr')
        if inc is None:
            out += [num(v)]*m if not v.lstrip('-').isdigit() else [int(v)]*m
        else:
            if '.' in v or 'e' in v.lower() or '.' in inc:
                b=F(v); d=F(inc); out += [b+d*i for i in range(m)]
            else:
                b=int(v); d=int(inc); out += [b+d*i for i in range(m)]
    return out
def load(name):
    t=ET.parse(f'/home/sgusev/.cache/minlplib/minlplib/osil/{name}.osil').getroot()
    d=t.find(NS+'instanceData')
    V=[]
    for v in d.find(NS+'variables').findall(NS+'var'):
        lb=v.get('lb','0'); ub=v.get('ub','INF')
        V.append(dict(name=v.get('name'),lb=num(lb),ub=num(ub),type=v.get('type','C')))
    C=[]
    for c in d.find(NS+'constraints').findall(NS+'con'):
        C.append(dict(name=c.get('name'),lb=num(c.get('lb','-INF')),ub=num(c.get('ub','INF')),const=F(c.get('constant','0')),lin={},quad={}))
    obj=d.find(NS+'objectives').find(NS+'obj')
    O=dict(sense=obj.get('maxOrMin'),const=F(obj.get('constant','0')),lin={int(c.get('idx')):F(c.text) for c in obj.findall(NS+'coef')})
    L=d.find(NS+'linearConstraintCoefficients')
    if L is not None:
        start=expand(L.find(NS+'start'))
        val=expand(L.find(NS+'value'))
        val=[F(x) if not isinstance(x,F) else x for x in val]
        ci=L.find(NS+'colIdx'); ri=L.find(NS+'rowIdx')
        if ci is not None:
            idx=expand(ci)
            for r in range(len(start)-1):
                for p in range(start[r],start[r+1]): C[r]['lin'][idx[p]]=C[r]['lin'].get(idx[p],0)+val[p]
        else:
            idx=expand(ri)
            for c in range(len(start)-1):
                for p in range(start[c],start[c+1]): C[idx[p]]['lin'][c]=C[idx[p]]['lin'].get(c,0)+val[p]
    Q=d.find(NS+'quadraticCoefficients')
    if Q is not None:
        for q in Q.findall(NS+'qTerm'):
            r=int(q.get('idx')); a,b=int(q.get('idxOne')),int(q.get('idxTwo'))
            key=(min(a,b),max(a,b))
            tgt=O if r==-1 else C[r]
            tgt.setdefault('quad',{})
            tgt['quad'][key]=tgt['quad'].get(key,0)+F(q.get('coef'))
    assert d.find(NS+'nonlinearExpressions') is None
    return V,C,O
def show(V,C,i):
    c=C[i]
    s=' + '.join([f'{v}*x{j+1}' for j,v in sorted(c['lin'].items())]+[f'{v}*x{a+1}*x{b+1}' for (a,b),v in sorted(c['quad'].items())])
    return f"e{i+1}: {c['lb']} <= {s} <= {c['ub']}"
