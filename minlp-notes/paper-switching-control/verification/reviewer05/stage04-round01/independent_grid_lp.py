"""Independent full cell-allocation LPs and rational extremizer evaluation."""
from fractions import Fraction as Q
from random import Random
import numpy as np
from scipy.optimize import linprog

def formula(n,t):
    T=t[-1];c=next(j for j in range(1,len(t)) if t[j]>=T/3)
    best=min((T+t[c])/4,(T-t[c-1])/2); witness=('H',c)
    for a in range(1,len(t)):
        for b in range(a,len(t)):
            A,B,P,R=t[a],t[b],t[a-1],t[b-1]
            lower=max(T/3,Q(n-1,n)*T-B,((n-1)*T-A-(n-1)*B)/n)
            upper=min(A,((n-2)*A+B)/n,Q(n-1,n)*T-P,((n-1)*T-P-(n-1)*R)/n,(T-P+(n-2)*A)/n)
            if (n-2)*(T-A)<=(n-1)*B and lower<=upper and upper>best:
                best=upper;witness=('A',a,b)
    return best,witness

def full_lp(n,t):
    N=len(t)-1;nv=n*N+1;err=nv-1
    def pref(i,j):return {i*N+k:1 for k in range(j)}
    def combine(*terms):
        v=np.zeros(nv)
        for scale,coeff in terms:
            for i,c in coeff.items():v[i]+=scale*c
        return v
    unit={err:1}
    equal=np.zeros((N,nv))
    for j in range(N):
        for i in range(n):equal[j,i*N+j]=1
    best=-float('inf');programs=0
    for a in range(1,N+1):
        for b in range(a,N+1):
            rows=[];rhs=[]
            def add(v,r):rows.append(v);rhs.append(float(r))
            add(combine((1,pref(1,N)),(-1,pref(0,N))),0)
            for i in range(2,n):add(combine((1,pref(i,N)),(-1,pref(1,N))),0)
            for i,j in [(0,a),(1,b)]:
                add(combine((1,unit),(1,pref(i,N))),t[-1]-t[j-1])
                add(combine((-1,unit),(-1,pref(i,N))),-(t[-1]-t[j]))
            add(combine((1,unit),(1,pref(1,a))),t[a])
            add(combine((1,unit),(1,pref(0,b))),t[b])
            for family in [1,2]:
                R=list(rows);B=list(rhs)
                if family==1:
                    for i in range(2,n):R.append(combine((1,unit),(1,pref(i,a))));B.append(float(t[a]))
                else:R.append(combine((1,unit),(-1,pref(1,N))));B.append(0)
                objective=np.zeros(nv);objective[err]=-1
                result=linprog(objective,A_ub=np.array(R),b_ub=np.array(B),A_eq=equal,b_eq=np.array([float(t[j+1]-t[j]) for j in range(N)]),bounds=[(0,None)]*(nv-1)+[(float(t[-1]/3),None)],method='highs')
                assert result.status in [0,2],result.message
                if result.status==0:best=max(best,-result.fun)
                programs+=1
    return best,programs

def exact_witness(n,t,E,w):
    T=t[-1]
    if w[0]=='H':
        C=t[w[1]];x=max(Q(0),(C-T+2*E)/2)
        mid=[x,x]+[min(C,T-2*E)/(n-2)]*(n-2)
        final=[E,E]+[(T-2*E)/(n-2)]*(n-2)
        knots=[(Q(0),[Q(0)]*n),(C,mid),(T,final)]
    else:
        a,b=w[1:];A,B,P,R=t[a],t[b],t[a-1],t[b-1]
        M=max(T/n,T-A-E,(n-1)*(E+R)-(n-2)*T,(n-1)*E-(n-2)*A)
        x=max(Q(0),(n-1)*E-(n-2)*A,A-T+M);y=max(x,B-T+M)
        knots=[(Q(0),[Q(0)]*n),(A,[x]+[(A-x)/(n-1)]*(n-1)),(B,[y]+[(B-y)/(n-1)]*(n-1)),(T,[M]+[(T-M)/(n-1)]*(n-1))]
    for (lo,a),(hi,b) in zip(knots,knots[1:]):
        assert all(x<=y for x,y in zip(a,b)) and sum(b)==hi
        if lo==hi:assert a==b
    def allocation(ti):
        if ti==0:return [Q(0)]*n
        for (lo,a),(hi,b) in zip(knots,knots[1:]):
            if hi>lo and lo<=ti<=hi:return [x+(y-x)*(ti-lo)/(hi-lo) for x,y in zip(a,b)]
        raise AssertionError
    values=[allocation(ti) for ti in t]
    optimum=T
    for p in range(n):
        for q in range(n):
            if p==q:continue
            for tau in t:
                value=max(abs(A[i]-(min(ti,tau) if i==p else 0)-(max(Q(0),ti-tau) if i==q else 0)) for ti,A in zip(t,values) for i in range(n))
                optimum=min(optimum,value)
    assert optimum==E,(n,t,E,optimum)

rng=Random(540105);cases=[]
for n in [3,4,5,9]:
    for N in [1,2,3,5]:
        t=[Q(0)]
        for _ in range(N):t.append(t[-1]+Q(rng.randrange(1,20),rng.randrange(1,10)))
        cases.append((n,t))
cases += [(5,list(map(Q,range(10)))),(9,list(map(Q,[0]))+[Q(19,2),Q(61,6),Q(265,24),Q(481,24),Q(2669,120)])]
programs=0
for n,t in cases:
    expected,w=formula(n,t);actual,count=full_lp(n,t);programs+=count
    assert abs(actual-float(expected))<1e-8*max(1,float(t[-1])),(n,t,expected,actual)
    exact_witness(n,t,expected,w)
print('PASS',len(cases),'arbitrary rational grids;',programs,'independent full-mode full-cell LP comparisons')
print('PASS reconstructed compressed extremizers by exact absolute-error enumeration of all one-switch schedules')
print('LP optima are numerical corroboration; extremizer and schedule checks use exact rational arithmetic')
