import math, sys
sys.path.insert(0,'/tmp/scout'); from osil import read
def ev(t,x):
    op=t[0]
    if op=='num': return t[1]
    if op=='var': return x[t[1]]
    a=[ev(c,x) for c in t[1:]]
    if op=='sum': return sum(a)
    if op=='times':
        p=1.0
        for v in a: p*=v
        return p
    if op=='negate': return -a[0]
    if op=='divide': return a[0]/a[1]
    if op=='power': return a[0]**a[1]
    if op=='square': return a[0]**2
    if op=='sqrt': return math.sqrt(a[0])
    if op in('sin','cos','exp','tanh'): return getattr(math,op)(a[0])
    if op=='ln': return math.log(a[0])
    raise NotImplementedError(op)
def check(I,x,tol=1e-7):
    worst=0; obj=None
    for j,(l,u) in enumerate(zip(I['lb'],I['ub'])):
        worst=max(worst,l-x[j],x[j]-u)
    for r,R in I['rows'].items():
        v=sum(c*x[j] for j,c in R['lin'].items())+sum(c*x[i]*x[j] for i,j,c in R['quad'])+(ev(R['nl'],x) if R['nl'] is not None else 0)
        if r==-1: obj=v; continue
        worst=max(worst,R['lb']-v,v-R['ub'])
    return obj,worst
