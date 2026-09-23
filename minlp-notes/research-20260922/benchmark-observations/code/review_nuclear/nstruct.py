import sys, collections
from fractions import Fraction as F
from parse import load
def analyze(name, verbose=True):
    V,C,O=load(name)
    rep={}
    n=len(V)
    assert O['sense']=='min' and O['const']==0 and len(O['lin'])==1 and not O.get('quad')
    (L,cL),=O['lin'].items(); assert cL==-1
    # burnup rows: 2 linear (-1 on kt, +1 on kt1), one quad a*phi*kt, equality 0
    burn={}; alphas=set()
    for r,c in enumerate(C):
        if len(c['lin'])==2 and len(c['quad'])==1 and c['lb']==0 and c['ub']==0 and sorted(c['lin'].values())==[-1,1]:
            kt=[j for j,v in c['lin'].items() if v==-1][0]; kt1=[j for j,v in c['lin'].items() if v==1][0]
            (a,b),al=list(c['quad'].items())[0]
            assert kt in (a,b); ph=b if a==kt else a
            burn[kt]=(kt1,ph,al,r); alphas.add(al)
    # chains
    nxt={kt:v[0] for kt,v in burn.items()}; heads=set(nxt)-set(nxt.values())
    chains=[]
    for h in heads:
        ch=[h]
        while ch[-1] in nxt: ch.append(nxt[ch[-1]])
        chains.append(ch)
    Ts=set(len(ch) for ch in chains); assert len(Ts)==1; T=Ts.pop(); N=len(chains)
    kvar={}  # (node,t)->var
    phi={}
    for i,ch in enumerate(sorted(chains)):
        for t,kv in enumerate(ch):
            kvar[(i,t)]=kv
            if t<T-1: phi[(i,t)]=burn[kv][1]
    kpos={v:k for k,v in kvar.items()}
    # peaking rows: single quad (phi,k) coef 1 ub c
    peak={}
    for r,c in enumerate(C):
        if not c['lin'] and len(c['quad'])==1 and c['lb']=='-INF':
            (a,b),co=list(c['quad'].items())[0]; assert co==1
            kk=a if a in kpos else b; pp=b if kk==a else a
            it=kpos[kk]
            if it in phi: assert phi[it]==pp
            else: phi[it]=pp
            peak[it]=c['ub']
    assert len(peak)==N*T, (len(peak),N*T)
    ppos={v:k for k,v in phi.items()}
    # eigen rows
    eig={}; lam={}
    G={}
    norm={}
    for r,c in enumerate(C):
        if c['lin'] or not c['quad']: continue
        terms=list(c['quad'].items())
        if all(( (a in ppos and b in kpos) or (b in ppos and a in kpos)) for (a,b),v in terms):
            # normalization
            if len(terms)>1 and c['lb']==c['ub']==1:
                ts=set()
                for (a,b),v in terms:
                    pa,kb=(a,b) if a in ppos else (b,a); assert ppos[pa]==kpos[kb]; ts.add(ppos[pa][1])
                assert len(ts)==1; t=ts.pop(); assert t not in norm
                norm[t]={ppos[a if a in ppos else b][0]:v for (a,b),v in terms}
            continue
        lamterms=[(a,b,v) for (a,b),v in terms if not((a in ppos and b in kpos) or (b in ppos and a in kpos))]
        if len(lamterms)!=1: continue
        a,b,v=lamterms[0]
        if not (a in ppos or b in ppos): continue
        pv,lv=(a,b) if a in ppos else (b,a)
        if lv in kpos: continue
        assert v==-1 and c['lb']==0 and c['ub']==0, (name,r)
        i,t=ppos[pv]
        assert (i,t) not in eig
        eig[(i,t)]=r; lam.setdefault(t,set()).add(lv)
        for (x,y),co in terms:
            if (x,y)==(min(a,b),max(a,b)): continue
            px,ky=(x,y) if x in ppos else (y,x)
            j,tt=ppos[px]; assert kpos[ky]==(j,tt) and tt==t
            G.setdefault(t,{})[(i,j)]=G.get(t,{}).get((i,j),0)+co
    assert len(eig)==N*T
    lamv={t:s.pop() for t,s in lam.items() if len(s)==1}; assert len(lamv)==T
    # consistency of G across t
    G0=G[T-1]
    for t in range(T): assert G[t]==G0, ('G differs',t)
    assert all(v>0 for v in G0.values())
    assert L==lamv[T-1], 'objective is not lam_T'
    assert set(norm)==set(range(T))
    Vw=norm[T-1]; assert all(norm[t]==Vw for t in range(T)) and len(Vw)==N
    # bounds
    def lb(j): return V[j]['lb']
    rep.update(name=name,N=N,T=T,alpha=sorted(alphas),
        phi_lb=sorted(set(lb(v) for v in phi.values())),k_lb=sorted(set(lb(v) for v in kvar.values())),
        lam_lb=sorted(set(lb(v) for v in lamv.values())),
        phi_ub=sorted(set(str(V[v]['ub']) for v in phi.values())),k_ub=sorted(set(str(V[v]['ub']) for v in kvar.values())),
        peak=sorted(set(peak.values())),V=sorted(set(Vw.values())),burn_all=len(burn)==N*(T-1))
    return V,C,O,rep,dict(kvar=kvar,phi=phi,lam=lamv,G=G0,Vw=Vw,peak=peak,T=T,N=N,kpos=kpos,ppos=ppos)
if __name__=='__main__':
    for nm in sys.argv[1:]:
        V,C,O,rep,S=analyze(nm)
        print(rep)
        used=set(S['kvar'].values())|set(S['phi'].values())|set(S['lam'].values())
        neg=[j for j,v in enumerate(V) if v['lb']=='-INF' or (v['lb']!='-INF' and v['lb']<0)]
        print(' negative-lb vars:',len(neg),' any among phi/k/lam:',bool(set(neg)&used))
        print(' rowsums G min/max:',float(min(sum(v for (i,j),v in S['G'].items() if i==r) for r in range(S['N']))),float(max(sum(v for (i,j),v in S['G'].items() if i==r) for r in range(S['N']))))
