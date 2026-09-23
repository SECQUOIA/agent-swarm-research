"""Exact rational stress checks of arbitrary-factor level cuts and overlays."""
from fractions import Fraction as F
from random import Random
from collections import Counter
r=Random(401); counts=Counter()
class PL:
    def __init__(self, hinges):
        self.hinges=hinges
        self.knots=sorted(set([F(0),F(1)]+[x for x,c in hinges]))
    def f(self,x): return sum(c*max(F(0),x-t) for t,c in self.hinges)-3*x+2
    def gap(self,a,b,x):
        return F(0) if a==b else ((b-x)*self.f(a)+(x-a)*self.f(b))/(b-a)-self.f(x)
    def error(self,a,b): return max(self.gap(a,b,x) for x in [a,b]+[x for x in self.knots if a<x<b])
    def cuts(self,a,b,tau,H):
        assert self.error(a,b)<=H*tau
        cuts={a,b}; knots=[a]+[x for x in self.knots if a<x<b]+[b]
        for j in range(1,H):
            level=j*tau
            if level>=self.error(a,b): continue
            hits=[]
            for x,y in zip(knots,knots[1:]):
                u,v=self.gap(a,b,x)-level,self.gap(a,b,y)-level
                if u==0: hits.append(x)
                if v==0: hits.append(y)
                if u*v<0: hits.append(x+(y-x)*(-u)/(v-u))
            cuts.update([min(hits),max(hits)])
        cuts=sorted(cuts)
        assert len(cuts)-1<=2*H-1
        for x,y in zip(cuts,cuts[1:]): assert self.error(x,y)<=tau
        return cuts
functions=[PL([]),PL([(F(1,4),F(4)),(F(3,4),F(4))]),PL([(F(1,1024),F(1024))]),PL([(F(1023,1024),F(1024))])]
for _ in range(36):
    functions.append(PL([(F(r.randrange(1,32),32),F(r.randrange(1,20),r.randrange(1,5))) for _ in range(5)]))
for f in functions:
    for H in range(1,11):
        a,b=F(0),F(1)
        tau=max(F(1,10000),f.error(a,b)/H)
        cuts=f.cuts(a,b,tau,H)
        counts['level_refinements']+=1; counts['valid_cells']+=len(cuts)-1
# Simultaneous cuts: component-specific H=2 and normalized tolerance E/2.
for offset in range(0,36,3):
    fs=functions[offset:offset+3]
    ts=[max(F(1,10000),f.error(F(0),F(1))/2) for f in fs]
    cuts=sorted(set(x for f,t in zip(fs,ts) for x in f.cuts(F(0),F(1),t,2)))
    assert len(cuts)-1<=2*len(fs)+1
    for a,b in zip(cuts,cuts[1:]):
        for f,t in zip(fs,ts): assert f.error(a,b)<=t
        counts['valid_vector_cells']+=1
    counts['vector_overlays']+=1
# Ordered target decisions, despite inconsistent mass approximations at nodes.
for trial in range(20):
    thresholds={}
    def evaluate(target):
        lo,hi=F(0),F(1)
        for depth in range(7):
            mid=(lo+hi)/2
            if mid not in thresholds: thresholds[mid]=F(r.randrange(-10,111),100)
            value=thresholds[mid]; err=F(1,20)
            if target<value-err: hi=mid
            elif target>value+err: lo=mid
            else: return mid
        return (lo+hi)/2
    vals=[F(0)]+[evaluate(F(k,128)) for k in range(1,128)]+[F(1)]
    assert vals==sorted(vals)
    counts['ordered_uncertain_trees']+=1; counts['target_outputs']+=len(vals)
print(dict(counts))
print('PASS: exact rational level cuts, convex vector overlays, and ordered uncertain bisection.')
