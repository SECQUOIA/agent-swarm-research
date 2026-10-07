# Critic: evaluate MINLPLib chain p1 points (objective and max row violation) in 80-digit mpmath (evidence).
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import xml.etree.ElementTree as ET
from fractions import Fraction as F
from mpmath import mp, mpf
mp.dps = 80
NS='{os.optimizationservices.org}'
def q(s): f=F(s); return mpf(f.numerator)/f.denominator
def ev(e,x):
    k=e.tag.replace(NS,''); ch=list(e)
    if k=='number': return q(e.get('value'))
    if k=='variable': return q(e.get('coef','1'))*x[int(e.get('idx'))]
    if k=='sqrt': return mp.sqrt(ev(ch[0],x))
    if k=='square': return ev(ch[0],x)**2
    if k=='sum': return mp.fsum(ev(c,x) for c in ch)
    if k=='product':
        r=mpf(1)
        for c in ch: r*=ev(c,x)
        return r
    raise ValueError(k)
def expand(p):
    out=[]
    for el in p:
        m=int(el.get('mult','1')); inc=el.get('incr'); v=el.text.strip()
        out += [v]*m if inc is None else [str(int(v)+i*int(inc)) for i in range(m)]
    return out
duals={'chain50':'5.07226149398286274561087338952347636222','chain100':'5.06978461073875052989023970440030097961','chain200':'5.06891734179316166830631118500605225563','chain400':'5.06862169460400924236864739214070141315'}
for n,L in duals.items():
    d=ET.parse(f'{_PUBLIC_HOME}/.cache/minlplib/minlplib/osil/{n}.osil').getroot().find(NS+'instanceData')
    V=list(d.find(NS+'variables')); sol={}
    for l in open(f'{n}.p1.sol'):
        p=l.split()
        if len(p)>=2:
            try: sol[p[0]]=q(p[1])
            except Exception: pass
    x=[sol.get(v.get('name'),mpf(0)) for v in V]
    C=list(d.find(NS+'constraints')); Lc=d.find(NS+'linearConstraintCoefficients')
    st=[int(z) for z in expand(Lc.find(NS+'start'))]; col=[int(z) for z in expand(Lc.find(NS+'colIdx'))]; val=expand(Lc.find(NS+'value'))
    nl={int(e.get('idx')):list(e)[0] for e in d.find(NS+'nonlinearExpressions')}
    viol=mpf(0)
    for i,c in enumerate(C):
        r=mp.fsum(q(val[k])*x[col[k]] for k in range(st[i],st[i+1]))
        if i in nl: r+=ev(nl[i],x)
        lb=c.get('lb'); ub=c.get('ub')
        if lb not in (None,'-INF'): viol=max(viol,q(lb)-r)
        if ub not in (None,'INF'): viol=max(viol,r-q(ub))
    for v,xv in zip(V,x):
        lb=v.get('lb','0'); ub=v.get('ub','INF')
        if lb!='-INF': viol=max(viol,q(lb)-xv)
        if ub!='INF': viol=max(viol,xv-q(ub))
    f=ev(nl[-1],x)
    print(n, 'f(p1)=', mp.nstr(f,20), ' f(p1) - certified dual =', mp.nstr(f-q(L),5), ' max viol', mp.nstr(viol,3))
