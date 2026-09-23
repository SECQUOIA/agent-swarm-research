import sys, json
from fractions import Fraction as F
import numpy as np
import importlib.util
spec=importlib.util.spec_from_file_location('kchk',__import__('os').path.join(__import__('os').path.dirname(__file__),'kchk.py')); kc=importlib.util.module_from_spec(spec); spec.loader.exec_module(kc)
auth={d['name']:d for d in json.load(open(__import__('os').path.join(__import__('os').path.dirname(__file__),'..','..','nuclear_cw_bounds.json')))}
def irreducible(G,N):
    adj={i:[j for (a,j) in G if a==i] for i in range(N)}
    def reach(s,adj):
        seen={s};st=[s]
        while st:
            u=st.pop()
            for v in adj[u]:
                if v not in seen: seen.add(v); st.append(v)
        return seen
    radj={i:[a for (a,j) in G if j==i] for i in range(N)}
    return len(reach(0,adj))==N and len(reach(0,radj))==N
def cw(G,N,w):
    assert all(x>0 for x in w)
    Gw=[F(0)]*N
    for (i,j),v in G.items(): Gw[i]+=v*w[j]
    return max(Gw[i]/w[i] for i in range(N))
def peak_theta(G,N,y,Vw,c):
    assert all(x>=0 for x in y)
    g=[F(0)]*N
    for (i,j),v in G.items(): g[j]+=y[i]*v
    Vv=[Vw[i] for i in range(N)]
    assert sum(Vv)*c>=1
    def knap(r):
        order=sorted(range(N),key=lambda i:r[i]/Vv[i],reverse=True)
        p=[F(0)]*N; cap=F(1)
        for i in order:
            if cap<=0: break
            take=min(c,cap/Vv[i]); p[i]=take; cap-=take*Vv[i]
        assert cap==0
        return p
    pm=knap([-y[i] for i in range(N)]); miny=sum(y[i]*pm[i] for i in range(N)); assert miny>0, 'y.p can vanish on P'
    th=F(0); it=0
    while True:
        p=knap([g[i]-th*y[i] for i in range(N)])
        val=sum((g[i]-th*y[i])*p[i] for i in range(N))
        if val<=0: break
        th=sum(g[i]*p[i] for i in range(N))/sum(y[i]*p[i] for i in range(N)); it+=1
    assert val==0
    return th
def rat(v,den=10**9): return [F(float(x)).limit_denominator(den) for x in v]
for nm in sys.argv[1:]:
    rep,info,S=kc.check(nm)
    N,G,Vw,KF=S['N'],S['G'],S['Vw'],info['KF']
    T=S['T']
    cT=[S['peak'][(i,T-1)] for i in range(N)]; assert len(set(cT))==1; c=cT[0]
    A=np.zeros((N,N))
    for (i,j),v in G.items(): A[i,j]=float(v)
    ev,R=np.linalg.eig(A); k=np.argmax(ev.real); rho=ev[k].real
    wr=np.abs(R[:,k].real); ev2,Lv=np.linalg.eig(A.T); yl=np.abs(Lv[:,np.argmax(ev2.real)].real)
    w=rat(wr/wr.max()); y=rat(yl/yl.max())
    rs=[sum(v for (a,b),v in G.items() if a==i) for i in range(N)]
    cwb=KF*cw(G,N,w); pb=KF*peak_theta(G,N,y,Vw,c)
    a=auth[nm]
    aw=[F(s) for s in a['w']]; ay=[F(s) for s in a['y']]
    acw=KF*cw(G,N,aw); ap=KF*peak_theta(G,N,ay,Vw,c); nz=sum(1 for q in ay if q==0)
    # check author's peak_c vs file c
    print(f"{nm:11s} N={N} irreducible={irreducible(G,N)} rho={rho:.6f} rowsum[min,max]=[{float(min(rs)):.4f},{float(max(rs)):.4f}] c_file={float(c):.16g} zeros_in_author_y={sum(1 for q in a['y'] if F(q)==0)}")
    print(f"    mine: CW={float(cwb):.7f} P(leftPerron)={float(pb):.7f} | author cert rechecked: CW={float(acw):.7f} P={float(ap):.7f} | author best={float(a['best_bound']):.7f} listed primal={a['listed_primal']}")
    best=min(cwb,pb,acw,ap)
    lp=a['listed_primal']
    if lp not in (None,'None'): assert -float(lp)<=float(best)
    print(f"    best certified (min of the four)={float(best):.7f}  (author claims {float(a['best_bound']):.7f}; diff {float(best)-float(a['best_bound']):+.2e})")
    if N==104:
        for i in range(N):
            if abs(rs[i]-1)>F(1,1000):
                r=[rr for (ii,t),rr in S['kpos'].items()] if False else None
                print('   anomalous G row node',i,'sum',float(rs[i]),sorted([str(v) for (a,b),v in G.items() if a==i]))
    print('    exact best:',best, '=', f"{float(best):.10f}")
