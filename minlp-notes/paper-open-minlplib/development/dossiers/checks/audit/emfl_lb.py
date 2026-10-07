# Independent weak-duality lower bound for emfl050_3_3 (own derivation and code; exact final check).
import sys, numpy as np, cvxpy as cp
from fractions import Fraction
from math import isqrt
from qosil_min import read
M=read(sys.argv[1]+'.osil'); V=M['V']; C=M['C']
qrows=[k for k in range(len(C)) if M['Q'][k]]; lrows=[k for k in range(len(C)) if not M['Q'][k]]
tv={}; cones=[]
for k in qrows:
    t=[a for a,b,cf in M['Q'][k] if cf==1]; w=[a for a,b,cf in M['Q'][k] if cf==-1]
    assert len(t)==1 and all(a==b for a,b,_ in M['Q'][k]) and len(t)+len(w)==len(M['Q'][k]) and C[k]['lb']==0 and C[k]['ub'] is None and not M['rows'][k]
    assert V[t[0]]['lb']==0
    cones.append((t[0],w))
wset={j for _,w in cones for j in w}; tset={t for t,_ in cones}
base=[j for j in range(len(V)) if j not in wset and j not in tset]
assert all(V[j]['lb']==0 and V[j]['ub'] is None for j in base)
assert all(V[j]['lb'] is None and V[j]['ub'] is None for j in wset)
bidx={j:i for i,j in enumerate(base)}
# w = A z + e  from rows coef_w*w + sum a_j z_j = rhs
A={}; e={}
for k in lrows:
    r=M['rows'][k]; ws=[j for j in r if j in wset]; assert len(ws)==1 and C[k]['lb']==C[k]['ub'] and C[k]['const']==0
    w=ws[0]; cw=r[w]; assert w not in A
    A[w]={bidx[j]:-r[j]/cw for j in r if j!=w}; assert all(j in bidx for j in r if j!=w)
    e[w]=C[k]['lb']/cw
assert set(A)==wset
c={t:M['oc'].get(t,Fraction(0)) for t,_ in cones}
assert all(v>=0 for v in c.values()) and set(M['oc'])<=tset and M['const']==0 and not M['Qobj']
nb=len(base); act=[(t,w) for t,w in cones if c[t]>0]
print('cones',len(cones),'weighted',len(act),'base',nb)
eta=float(sys.argv[2]) if len(sys.argv)>2 else 1e-9
ys=[cp.Variable(len(w)) for t,w in act]
g=0; obj=0; cons=[]
for (t,w),y in zip(act,ys):
    Ak=np.array([[float(A[j].get(i,0)) for i in range(nb)] for j in w]); ek=np.array([float(e[j]) for j in w])
    g=g+Ak.T@y; obj=obj+ek@y; cons.append(cp.norm(y,2)<=float(c[t])*(1-eta))
cons.append(g>=0)
prob=cp.Problem(cp.Maximize(obj),cons); prob.solve(solver=cp.CLARABEL)
print('numerical dual value',prob.value, prob.status)
# exact check
Y={}
for (t,w),y in zip(act,ys):
    yq=[Fraction(float(v)) for v in y.value]
    n2=sum(v*v for v in yq)
    if n2>c[t]**2:
        D=10**30; r=Fraction(isqrt(n2.numerator*D*D//n2.denominator)+1, D)
        s_=c[t]/r; yq=[v*s_ for v in yq]
    Y[t]=dict(zip(w,yq))
def gvec():
    g=[Fraction(0)]*nb
    for (t,w) in act:
        for j,v in Y[t].items():
            for i,a in A[j].items(): g[i]+=a*v
    return g
gex=gvec(); neg=[i for i in range(nb) if gex[i]<0]
print('negative g before repair',len(neg),'min',float(min(gex)))
for i in neg:
    best=None
    for (t,w) in act:
        for j in w:
            if set(A[j])=={i}:
                slack=c[t]**2-sum(v*v for v in Y[t].values())
                if best is None or slack>best[0]: best=(slack,t,j)
    slack,t,j=best; a=A[j][i]; Y[t][j]+= -gex[i]/a
    assert sum(v*v for v in Y[t].values())<=c[t]**2, 'repair broke norm'
gex=gvec(); assert all(v>=0 for v in gex)
assert all(sum(v*v for v in Y[t].values())<=c[t]**2 for t,_ in act)
L=sum(v*e[j] for t,_ in act for j,v in Y[t].items())
print('exact lower bound L =',float(L),' floor(L*1e15)/1e15 =',L.numerator*10**15//L.denominator)
for lab,val in [(a.split('=')[0],a.split('=')[1]) for a in sys.argv[3:]]:
    from decimal import Decimal
    v=Fraction(Decimal(val)); print(lab,val,'L - value =',float(L-v),'rel',float((L-v)/L))
