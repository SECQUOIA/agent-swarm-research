# Exact rational evaluation of points in MINLPLib camshape (OSIL) and QPLIB camshape (.qplib).
# Decimal strings of points/coefficients are converted exactly to Fractions.
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import sys
from fractions import Fraction as Fr
from osil_lq import read as read_osil
from qplib_read import read as read_qp
def F(s): return Fr(s.replace('E','e')) if s not in ('INF','-INF') else None
def load_sol(path, offset=0, skip=()):
    from collections import defaultdict
    x=defaultdict(Fr)
    for l in open(path):
        p=l.split()
        if len(p)==2 and p[0].startswith('x'):
            x[int(p[0][1:])-offset]=Fr(p[1])
    return x
def eval_osil(m,x):   # x: dict 0-based var index -> Fraction
    worst=Fr(0); wrow=None
    for r,(nm,lb,ub,c) in enumerate(m['C']):
        v=F(c)
        for j,a in m['lin'].get(r,{}).items(): v+=F(a)*x[j]
        for i,j,a in m['quad'].get(r,[]): v+=F(a)*x[i]*x[j]
        viol=max(Fr(0), (F(lb)-v) if lb!='-INF' else Fr(0), (v-F(ub)) if ub!='INF' else Fr(0))
        if viol>worst: worst,wrow=viol,nm
    for k,(nm,lb,ub,t) in enumerate(m['V']):
        if lb!='-INF' and x[k]<F(lb): 
            if F(lb)-x[k]>worst: worst,wrow=F(lb)-x[k],nm
        if ub!='INF' and x[k]>F(ub):
            if x[k]-F(ub)>worst: worst,wrow=x[k]-F(ub),nm
    obj=sum(F(a)*x[j] for j,a in m['objlin'].items())
    return obj,worst,wrow
def eval_qp(q,x):  # x: dict 1-based
    rows={}
    for r,i,j,a in q['cq']: rows[r]=rows.get(r,Fr(0))+a/2*x[i]*x[j]
    for r,i,a in q['cl']: rows[r]=rows.get(r,Fr(0))+a*x[i]
    worst=Fr(0); wrow=None
    big=1e300
    for r in range(1,q['m']+1):
        v=rows.get(r,Fr(0)); lo=float(q['lhs'][r]); hi=float(q['rhs'][r])
        viol=Fr(0)
        if abs(lo)<big and v<Fr(q['lhs'][r]): viol=Fr(q['lhs'][r])-v
        if abs(hi)<big and v>Fr(q['rhs'][r]): viol=max(viol,v-Fr(q['rhs'][r]))
        if viol>worst: worst,wrow=viol,('row',r)
    for k in range(1,q['n']+1):
        lo=q['lb'][k]; hi=q['ub'][k]
        if abs(float(lo))<big and x[k]<Fr(lo) and Fr(lo)-x[k]>worst: worst,wrow=Fr(lo)-x[k],('lb',k)
        if abs(float(hi))<big and x[k]>Fr(hi) and x[k]-Fr(hi)>worst: worst,wrow=x[k]-Fr(hi),('ub',k)
    obj=sum(q['objlin'][k]*x[k] for k in range(1,q['n']+1))+q['objc']
    return obj,worst,wrow
name,qid=sys.argv[1],sys.argv[2]
m=read_osil(name); q=read_qp(f'web/qplib/QPLIB_{qid}.qplib')
# MINLPLib point p1 (x1..xn, 1-based names) ; QPLIB sol has objvar + x2..x(n+1)
xm=load_sol(f'{_PUBLIC_REPO}/research-20260929/open-instances/minlplib_sol/{name}.p1.sol')
xq=load_sol(f'web/qplib/QPLIB_{qid}.sol', offset=1)   # GAMS x(k+1) -> qplib var k
print('QPLIB  sol vars',len(xq),' MINLPLib p1 vars',len(xm))
# MINLPLib p1 in OSIL (0-based) and in QPLIB (1-based)
from collections import defaultdict
xm0=defaultdict(Fr,{k-1:v for k,v in xm.items()})
o,w,r=eval_osil(m,xm0); print('MINLPLib p1 in MINLPLib model: obj',float(o),'max viol',float(w),r)
o,w,r=eval_qp(q,xm); print('MINLPLib p1 in QPLIB model:    obj',float(o),'max viol',float(w),r)
xq0=defaultdict(Fr,{k-1:v for k,v in xq.items()})
o,w,r=eval_osil(m,xq0); print('QPLIB sol in MINLPLib model:   obj',float(o),'max viol',float(w),r)
o,w,r=eval_qp(q,xq); print('QPLIB sol in QPLIB model:      obj',float(o),'max viol',float(w),r)
