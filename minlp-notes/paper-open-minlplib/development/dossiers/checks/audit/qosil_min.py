# Minimal independent OSiL reader for linear/quadratic models (exact Fractions). Written for this dossier.
import re, xml.etree.ElementTree as ET
from fractions import Fraction
from decimal import Decimal
NS='{os.optimizationservices.org}'
def fr(s):
    s=s.strip()
    if s in ('INF','+INF','inf'): return None
    if s in ('-INF','-inf'): return None
    return Fraction(Decimal(s))
def expand(elem):
    out=[]
    for el in elem.findall(NS+'el'):
        m=int(el.get('mult','1')); inc=el.get('incr')
        v=el.text.strip()
        if inc is None:
            out += [v]*m
        else:
            base=Fraction(Decimal(v)); d=Fraction(Decimal(inc))
            out += [str(base+k*d) for k in range(m)]
    return out
def read(path):
    root=ET.parse(path).getroot(); D=root.find(NS+'instanceData')
    V=[]
    for v in D.find(NS+'variables').findall(NS+'var'):
        t=v.get('type','C'); lb=v.get('lb'); ub=v.get('ub')
        lbv = Fraction(0) if lb is None else (None if lb.strip().upper()=='-INF' else Fraction(Decimal(lb)))
        if t=='B' and ub is None: ub='1'
        ubv = None if (ub is None or ub.strip().upper() in ('INF','+INF')) else Fraction(Decimal(ub))
        V.append(dict(name=v.get('name'),type=t,lb=lbv,ub=ubv))
    ob=D.find(NS+'objectives').find(NS+'obj')
    assert ob.get('weight') in (None,'1')
    sense=ob.get('maxOrMin'); const=Fraction(Decimal(ob.get('constant','0')))
    oc={int(c.get('idx')):Fraction(Decimal(c.text)) for c in ob.findall(NS+'coef')}
    C=[]
    for c in D.find(NS+'constraints').findall(NS+'con'):
        lb=c.get('lb'); ub=c.get('ub')
        C.append(dict(name=c.get('name'),lb=None if lb is None or lb.upper()=='-INF' else Fraction(Decimal(lb)),
                      ub=None if ub is None or ub.upper() in('INF','+INF') else Fraction(Decimal(ub)),
                      const=Fraction(Decimal(c.get('constant','0')))))
    rows=[dict() for _ in C]
    L=D.find(NS+'linearConstraintCoefficients')
    if L is not None:
        start=[int(Fraction(s)) for s in expand(L.find(NS+'start'))]
        if L.find(NS+'colIdx') is not None:
            idx=[int(Fraction(s)) for s in expand(L.find(NS+'colIdx'))]; byrow=True
        else:
            idx=[int(Fraction(s)) for s in expand(L.find(NS+'rowIdx'))]; byrow=False
        val=[Fraction(Decimal(s)) for s in expand(L.find(NS+'value'))]
        for k in range(len(start)-1):
            for j in range(start[k],start[k+1]):
                if byrow: rows[k][idx[j]]=rows[k].get(idx[j],0)+val[j]
                else: rows[idx[j]][k]=rows[idx[j]].get(k,0)+val[j]
    Q=[[] for _ in C]; Qobj=[]
    QC=D.find(NS+'quadraticCoefficients')
    if QC is not None:
        for q in QC.findall(NS+'qTerm'):
            i=int(q.get('idx')); a=int(q.get('idxOne')); b=int(q.get('idxTwo')); cf=Fraction(Decimal(q.get('coef','1')))
            (Qobj if i==-1 else Q[i]).append((a,b,cf))
    assert D.find(NS+'nonlinearExpressions') is None, 'nonlinear'
    return dict(V=V,sense=sense,oc=oc,const=const,C=C,rows=rows,Q=Q,Qobj=Qobj)
def readsol(path,V):
    names={v['name']:i for i,v in enumerate(V)}; x=[Fraction(0)]*len(V)
    for line in open(path):
        t=line.split()
        if len(t)==2 and t[0] in names: x[names[t[0]]]=Fraction(Decimal(t[1]))
    return x
def rowval(M,k,x):
    return sum(c*x[j] for j,c in M['rows'][k].items())+sum(cf*x[a]*x[b] for a,b,cf in M['Q'][k])+M['C'][k]['const']
def objval(M,x):
    return sum(c*x[j] for j,c in M['oc'].items())+sum(cf*x[a]*x[b] for a,b,cf in M['Qobj'])+M['const']
def violations(M,x):
    bad=[]
    for i,v in enumerate(M['V']):
        if v['lb'] is not None and x[i]<v['lb']: bad.append(('lb',v['name'],x[i]-v['lb']))
        if v['ub'] is not None and x[i]>v['ub']: bad.append(('ub',v['name'],x[i]-v['ub']))
        if v['type'] in ('I','B') and x[i].denominator!=1: bad.append(('int',v['name']))
    for k,c in enumerate(M['C']):
        r=rowval(M,k,x)
        if c['lb'] is not None and r<c['lb']: bad.append(('row<lb',c['name'],r-c['lb']))
        if c['ub'] is not None and r>c['ub']: bad.append(('row>ub',c['name'],r-c['ub']))
    return bad
