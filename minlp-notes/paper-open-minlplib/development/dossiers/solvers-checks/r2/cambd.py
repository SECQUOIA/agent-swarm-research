import sys, time
from fractions import Fraction as F
from gparse import parse_gms
sys.set_int_max_str_digits(0)
def ceil_grid(x,Q):  # smallest multiple of 1/Q >= x
    return F(-((-x.numerator*Q)//x.denominator),Q)
def structure(path):
    eqs,lo,up,pos=parse_gms(path)
    # objective row: contains objvar
    objrows=[k for k,(g,s) in eqs.items() if ('objvar',) in g]
    assert len(objrows)==1; g,s=eqs[objrows[0]]; assert s=='E'
    a=g[('objvar',)]
    assert all(len(k)<=1 for k in g)
    radii=[k[0] for k in g if k and k[0]!='objvar']
    w={v:-g[(v,)]/a for v in radii}; const=-g.get((),F(0))/a   # objvar = const + sum w_v v
    R=set(radii)
    # slope rows: linear E rows with two radii (+1,-1) and one non-radius with coeff +-1, rhs 0
    slope={}; used={objrows[0]}
    for k,(g,s) in eqs.items():
        if s!='E' or k in used: continue
        if all(len(m)==1 for m in g) and () not in g and len(g)==3:
            rv=[m[0] for m in g if m[0] in R]; dv=[m[0] for m in g if m[0] not in R]
            if len(rv)==2 and len(dv)==1:
                ca,cb=g[(rv[0],)],g[(rv[1],)]; cd=g[(dv[0],)]
                assert {ca,cb}=={F(1),F(-1)} and abs(cd)==1,(k,g)
                # d = +-(r_b - r_a)
                slope[frozenset(rv)]=(dv[0],k); used.add(k)
    # first convexity row: monomials {ra*rb:-1, ra:-1, rb:c}, sense L, no constant
    first=[]; interior={}; others=[]
    for k,(g,s) in eqs.items():
        if k in used: continue
        if s=='E': others.append(k); continue
        sg=1 if s=='L' else -1
        gg={m:sg*v for m,v in g.items()}       # gg <= 0
        bil=[m for m in gg if len(m)==2 and m[0]!=m[1]]
        lin=[m for m in gg if len(m)==1]
        if len(gg)==3 and len(bil)==1 and len(lin)==2 and () not in gg:
            ra,rb=bil[0]
            if gg[bil[0]]==-1 and gg.get((ra,))==-1: first.append((k,ra,rb,gg[(rb,)])); continue
            if gg[bil[0]]==-1 and gg.get((rb,))==-1: first.append((k,rb,ra,gg[(ra,)])); continue
        if len(gg)==3 and len(bil)==3 and () not in gg:
            vs=sorted({v for m in bil for v in m})
            # middle variable appears in two bilinear terms with coeff -1
            for mid in vs:
                ms=[m for m in bil if mid in m]
                if len(ms)==2 and all(gg[m]==-1 for m in ms):
                    outer=[m for m in bil if mid not in m][0]
                    interior[mid]=(k,outer,gg[outer]); break
            else: others.append(k)
            continue
        others.append(k)
    assert len(first)==1,first
    k1,r1,r2,c=first[0]
    # chain order via slope pairs, starting at r1 -> r2
    adj={v:set() for v in R}
    for pr in slope: a_,b_=tuple(pr); adj[a_].add(b_); adj[b_].add(a_)
    order=[r1]; prev=None; cur=r1
    while True:
        nxt=[v for v in adj[cur] if v!=prev]
        if not nxt: break
        assert len(nxt)==1; prev,cur=cur,nxt[0]; order.append(cur)
    assert order[1]==r2 and len(order)==len(R),(len(order),len(R))
    n=len(order); idx={v:i+1 for i,v in enumerate(order)}
    # interior rows j=2..n-1: middle r_j, outer (r_{j-1},r_{j+1}) coefficient c
    for j in range(2,n):
        k,outer,cc=interior[order[j-1]]
        assert set(outer)=={order[j-2],order[j]},(j,outer)
        assert cc==c,(j,cc,c)
    # slope bounds
    alpha={}
    for j in range(1,n):
        d,k=slope[frozenset((order[j-1],order[j]))]
        l=lo.get(d); u=up.get(d)
        if l is None and u is None and d not in pos: alpha[j]=None
        else:
            assert l==-u,(d,l,u); alpha[j]=u
    lb=[None]+[lo.get(v) for v in order]; ub=[None]+[up.get(v) for v in order]
    W=[None]+[w[v] for v in order]
    return dict(n=n,c=c,alpha=alpha,lb=lb,ub=ub,w=W,const=const,others=others,objrow=objrows[0])
def bound(st,eps=F(0),Q=10**40):
    n,c=st['n'],st['c']
    assert all(x<0 for x in st['w'][1:])
    assert all(l is not None and l>=1 for l in st['lb'][1:])
    U=[F(1),c]
    while len(U)<n: U.append(c*U[-1]-U[-2])
    assert min(U[:n])>=0
    W=[F(0)]*(n+1)
    for j in range(2,n+1): W[j]=W[j-1]+U[j-2]
    delta=eps/(1-eps)**3
    ub=[None]+[u+eps for u in st['ub'][1:]]
    S=[F(1),1/ub[1]]
    for j in range(1,n): S.append(c*S[j]-S[j-1])
    E=[None]
    for j in range(1,n+1):
        L=S[j]-delta*W[j]
        E.append(min(ub[j],ceil_grid(1/L,Q)) if L>0 else ub[j])
    al={j:(None if a is None else a+2*eps) for j,a in st['alpha'].items()}
    for j in range(2,n+1):
        if al[j-1] is not None: E[j]=min(E[j],E[j-1]+al[j-1])
    for j in range(n-1,0,-1):
        if al[j] is not None: E[j]=min(E[j],E[j+1]+al[j])
    val=st['const']+sum(st['w'][j]*E[j] for j in range(1,n+1))
    return val,max(U[:n]),W[n]
if __name__=='__main__':
    for p in sys.argv[1:]:
        t=time.time(); st=structure(p); v,mU,Wn=bound(st)
        print(f"{p}: n={st['n']} c={float(st['c'])!r} free_alpha={[j for j,a in st['alpha'].items() if a is None]} unused_rows={st['others']} bound_down={float(v):.17g} ({time.time()-t:.1f}s)")
        print('   exact-ish:', str(v.numerator*10**25//v.denominator))
