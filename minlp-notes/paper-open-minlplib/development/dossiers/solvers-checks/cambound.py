# Independent exact-rational comparison bound for camshape-type GAMS models (dossier check).
import re, sys
from fractions import Fraction as F
def parse(path):
    txt=open(path).read()
    # equations
    eqs={}
    for m in re.finditer(r'^(e\d+)\.\.(.*?);\s*$',txt,re.S|re.M):
        name,body=m.group(1),' '.join(m.group(2).split())
        mm=re.match(r'(.*)=([ELG])=(.*)',body)
        lhs,sense,rhs=mm.groups()
        lhs=re.sub(r'\((-?[^()]*?)\)(?!\s*\*)',lambda k:k.group(1) if 'sqr' not in k.group(0) else k.group(0),lhs)
        lhs=lhs.replace(' ','')
        if not lhs.startswith(('+','-')): lhs='+'+lhs
        mon={}
        pos=0
        pat=re.compile(r'([+-])((?:\d[\d.]*(?:[eE][+-]?\d+)?\*)?)((?:sqr\(\w+\))|\w+)(\*\w+)?')
        consumed=''
        for t in pat.finditer(lhs):
            sg,co,v1,v2=t.groups()
            consumed+=t.group(0)
            c=F(co[:-1]) if co else F(1)
            if sg=='-': c=-c
            if v1.startswith('sqr('):
                v=v1[4:-1]; key=(v,v)
            else:
                key=tuple(sorted([v1]+([v2[1:]] if v2 else [])))
            if re.fullmatch(r'\d[\d.]*',v1): raise ValueError('const in lhs '+lhs)
            mon[key]=mon.get(key,F(0))+c
        assert consumed==lhs,(name,lhs,consumed)
        eqs[name]=(mon,sense,F(rhs.strip()))
    lo={};up={}
    for m in re.finditer(r'(\w+)\.(lo|up|fx)\s*=\s*([-+0-9.eE]+)\s*;',txt):
        v,k,val=m.groups(); val=F(val)
        if k in('lo','fx'): lo[v]=val
        if k in('up','fx'): up[v]=val
    return eqs,lo,up
def bound(path):
    eqs,lo,up=parse(path)
    obj=[n for n,(mon,s,r) in eqs.items() if ('objvar',) in mon]
    assert len(obj)==1; mon,s,rhs=eqs[obj[0]]; assert s=='E'
    a=mon[('objvar',)]
    rv=[k[0] for k in mon if k!=('objvar',)]
    rv.sort(key=lambda v:int(v[1:]))
    coef={v:-mon[(v,)]/a for v in rv}   # objvar = rhs/a + sum coef_v * v
    const=rhs/a
    assert all(c<0 for c in coef.values())
    n=len(rv); idx={v:i+1 for i,v in enumerate(rv)}   # r_1..r_n
    # slope rows
    alpha={}  # pair j -> alpha (pair (j,j+1))
    used=set()
    for name,(mon,s,r) in eqs.items():
        if s=='E' and name!=obj[0] and len(mon)==3 and all(len(k)==1 for k in mon) and r==0:
            vs=[k[0] for k in mon]
            rs=[v for v in vs if v in idx]; sv=[v for v in vs if v not in idx]
            if len(rs)==2 and len(sv)==1:
                a1,b1=sorted(rs,key=lambda v:idx[v]); s1=sv[0]
                assert idx[b1]==idx[a1]+1 and mon[(a1,)]==1 and mon[(b1,)]==-1 and mon[(s1,)]==1,(name,mon)
                l=lo.get(s1); u=up.get(s1)
                if l is None and u is None: alpha[idx[a1]]=None
                else:
                    assert l==-u; alpha[idx[a1]]=u
                used.add(name)
    assert sorted(alpha)==list(range(1,n)),(sorted(alpha)[:5],n)
    # convexity rows
    cs={}
    for name,(mon,s,r) in eqs.items():
        if s!='L' or r!=0 or name in used or name==obj[0]: continue
        keys=set(mon)
        # interior: (j-1,j):-1,(j,j+1):-1,(j-1,j+1):c
        bil=[k for k in keys if len(k)==2 and k[0]!=k[1]]
        if len(bil)==3 and len(keys)==3:
            js=sorted({idx[v] for k in bil for v in k})
            if len(js)==3 and js[2]-js[0]==2:
                jm,j,jp=js
                rv_=lambda i: rv[i-1]
                kk=lambda x,y: tuple(sorted([rv_(x),rv_(y)]))
                assert mon[kk(jm,j)]==-1 and mon[kk(j,jp)]==-1,(name,mon)
                cs[j]=mon[kk(jm,jp)]; continue
        if len(keys)==3 and len(bil)==1:
            k=bil[0]; js=sorted(idx[v] for v in k)
            if js==[1,2]:
                assert mon[k]==-1 and mon[(rv[0],)]==-1
                cs[1]=mon[(rv[1],)]; continue
    assert sorted(cs)==list(range(1,n)),('rows',len(cs),n)
    cvals=set(cs.values()); assert len(cvals)==1,cvals
    c=cvals.pop()
    # Chebyshev U_m(c/2) >= 0 for m=0..n-1
    U=[F(1),c]
    for m in range(2,n): U.append(c*U[-1]-U[-2])
    minU=min(U[:n]); assert minU>=0,('U negative',)
    # S recurrence
    ub=[None]+[up[v] for v in rv]; lb=[None]+[lo[v] for v in rv]
    assert all(l>0 for l in lb[1:])
    S=[F(1),1/ub[1]]
    for j in range(1,n): S.append(c*S[j]-S[j-1])
    B=[None]
    Q=10**60
    for j in range(1,n+1):
        if S[j]>0:
            Rj=1/S[j]
            Rj=F(-((-Rj.numerator*Q)//Rj.denominator),Q)   # round UP to 1e-60 grid: still an upper bound on r_j
            B.append(min(ub[j],Rj))
        else:
            B.append(ub[j])
    E=B[:]
    for j in range(2,n+1):
        a_=alpha[j-1]
        if a_ is not None: E[j]=min(E[j],E[j-1]+a_)
    for j in range(n-1,0,-1):
        a_=alpha[j]
        if a_ is not None: E[j]=min(E[j],E[j+1]+a_)
    val=const+sum(coef[rv[j-1]]*E[j] for j in range(1,n+1))
    # feasibility of E in bounds (lower) for information
    inb=all(lb[j]<=E[j]<=ub[j] for j in range(1,n+1))
    return n,c,val,inb,float(min(S[1:])),alpha[1]
if __name__=='__main__':
    for p in sys.argv[1:]:
        n,c,val,inb,minS,a1=bound(p)
        print(f"{p}: n={n} c={float(c)!r} bound={float(val):.17g} E within bounds={inb} minS={minS:.4f} d1 free={a1 is None}")
        pass
