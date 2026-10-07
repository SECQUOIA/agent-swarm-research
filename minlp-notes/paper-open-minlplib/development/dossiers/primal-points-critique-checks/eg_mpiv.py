# Critic's independent cross-check: mpmath iv at 120 digits, own reader.
import sys, xml.etree.ElementTree as ET
from fractions import Fraction as F
from mpmath import iv, mpf, mp
iv.dps = 120; mp.dps = 120
NS='{os.optimizationservices.org}'
def q(s):
    f = F(s); return iv.mpf(f.numerator)/f.denominator
def ev(e,x):
    k=e.tag.replace(NS,''); ch=list(e)
    if k=='number': return q(e.get('value'))
    if k=='variable': return q(e.get('coef','1'))*x[int(e.get('idx'))]
    if k=='negate': return -ev(ch[0],x)
    if k=='square': v=ev(ch[0],x); return v**2
    if k=='exp': return iv.exp(ev(ch[0],x))
    if k=='sum':
        r=iv.mpf(0)
        for c in ch: r=r+ev(c,x)
        return r
    if k=='product':
        r=iv.mpf(1)
        for c in ch: r=r*ev(c,x)
        return r
    raise ValueError(k)
def expand(p):
    out=[]
    for el in p:
        m=int(el.get('mult','1')); inc=el.get('incr'); v=el.text.strip()
        out += [v]*m if inc is None else [str(int(v)+i*int(inc)) for i in range(m)]
    return out
for name in sys.argv[1:]:
    d=ET.parse(f'eg/{name}.osil').getroot().find(NS+'instanceData')
    V=list(d.find(NS+'variables')); sol=dict(l.split() for l in open(f'eg/{name}.retry.sol') if l.strip())
    x=[q(sol[v.get('name')]) for v in V]
    C=list(d.find(NS+'constraints')); L=d.find(NS+'linearConstraintCoefficients')
    st=[int(z) for z in expand(L.find(NS+'start'))]; col=[int(z) for z in expand(L.find(NS+'colIdx'))]; val=expand(L.find(NS+'value'))
    nl={int(e.get('idx')):list(e)[0] for e in d.find(NS+'nonlinearExpressions')}
    res=[]
    for i,c in enumerate(C):
        r=iv.mpf(0)
        for k in range(st[i],st[i+1]): r=r+q(val[k])*x[col[k]]
        if i in nl: r=r+ev(nl[i],x)
        m=[]
        if c.get('lb') not in (None,'-INF'): m.append(r.a-q(c.get('lb')).b)
        if c.get('ub') not in (None,'INF'): m.append(q(c.get('ub')).a-r.b)
        res.append((min(m),c.get('name')))
    res.sort(key=lambda t:t[0])
    print(name, 'min margins:', [(mp.nstr(mp.mpf(a.a if hasattr(a,'a') else a),6),n) for a,n in res[:3]], 'all>0:', all((a.a if hasattr(a,'a') else a)>0 for a,_ in res))
