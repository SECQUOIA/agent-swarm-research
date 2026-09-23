"""Exact stress checks for the scalar geometry, not a proof of the theorem."""
from fractions import Fraction as F
from random import Random
from collections import Counter

rng = Random(301)
counts = Counter()

class ConvexPL:
    def __init__(self, hinges, slope=F(0), offset=F(0)):
        self.hinges = hinges
        self.knots = sorted(set([F(0), F(1)] + [t for t, c in hinges]))
        self.slope, self.offset = slope, offset
    def __call__(self, x):
        return self.offset + self.slope*x + sum(c*max(F(0), x-t) for t,c in self.hinges)
    def J(self, a, b):
        return (self(a)+self(b))/2-self((a+b)/2)
    def chord(self, a, b, x):
        return self(a) if a == b else ((b-x)*self(a)+(x-a)*self(b))/(b-a)
    def error(self, a, b):
        return max(self.chord(a,b,x)-self(x) for x in [a,b]+[t for t in self.knots if a<t<b])
    def compatible(self, x, eta):
        # J(x,y) is piecewise affine; its breakpoints are y=t and y=2t-x.
        breaks = sorted(set([F(0),F(1),x]+[v for t in self.knots for v in [t,2*t-x] if 0<v<1]))
        feasible = [y for y in breaks if self.J(x,y)<=eta]
        for a,b in zip(breaks,breaks[1:]):
            va,vb = self.J(x,a)-eta,self.J(x,b)-eta
            if va*vb<0:
                feasible.append(a+(b-a)*(-va)/(vb-va))
        return min(feasible), max(feasible)

def trim(intervals):
    x=F(0); result=[]
    while x<1:
        b=max(b for a,b in intervals if a<=x)
        assert b>x
        result.append((x,b)); x=b
    assert len(result)<=len(intervals)
    return result

def refine(f,a,b,eta):
    assert f.error(a,b)<=2*eta
    if f.error(a,b)<=eta:
        return [(a,b)]
    knots=[a]+[t for t in f.knots if a<t<b]+[b]
    hits=[]
    for x,y in zip(knots,knots[1:]):
        vx=f.chord(a,b,x)-f(x)-eta
        vy=f.chord(a,b,y)-f(y)-eta
        if vx==0: hits.append(x)
        if vx*vy<0: hits.append(x+(y-x)*(-vx)/(vy-vx))
        if vy==0: hits.append(y)
    u,v=min(hits),max(hits)
    assert a<u<v<b
    return [(a,u),(u,v),(v,b)]

families=[ConvexPL([]),ConvexPL([(F(1,2),F(1))]),
          ConvexPL([(F(1,1024),F(1024))]),ConvexPL([(F(1023,1024),F(1024))])]
for _ in range(76):
    hinges=[(F(rng.randrange(1,64),64),F(rng.randrange(0,50),rng.randrange(1,12))) for _ in range(8)]
    families.append(ConvexPL(hinges,F(rng.randrange(-10,11)),F(rng.randrange(-10,11))))
for f in families:
    eta=max(F(1,1000),f.error(F(0),F(1))/8)
    selected=[]; compatible=[]
    while True:
        ordered=sorted(compatible)
        cursor=F(0); gap=None
        for a,b in ordered:
            if a>cursor:
                gap=(cursor,a); break
            cursor=max(cursor,b)
        if gap is None and cursor<1: gap=(cursor,F(1))
        if compatible and gap is None: break
        x=F(0) if not selected else sum(gap)/2
        assert all(f.J(x,y)>eta for y in selected)
        selected.append(x); compatible.append(f.compatible(x,eta))
        assert len(selected)<1000
    split=[]
    for x,(a,b) in zip(selected,compatible):
        assert f.J(a,x)<=eta and f.J(x,b)<=eta
        split.extend([(a,x),(x,b)])
    partition=trim(split)
    assert len(partition)<=2*len(selected)
    final=[]
    for a,b in partition:
        assert f.error(a,b)<=2*eta
        final.extend(refine(f,a,b,eta))
    assert len(final)<=6*len(selected)
    for a,b in final:
        assert f.error(a,b)<=eta
        counts['refined_cells']+=1
    counts['maximal_packings']+=1
    counts['packing_points']+=len(selected)
    for _ in range(20):
        pts=sorted(set(F(rng.randrange(0,65),64) for _ in range(5)))
        if len(pts)<2: continue
        a,b=pts[0],pts[-1]
        assert f.error(a,b)<=2*f.J(a,b)
        assert f.J(a,b)>=sum(f.J(x,y) for x,y in zip(pts,pts[1:]))
        for x,y in zip(pts,pts[1:]):
            assert f.J(x,y)<=f.J(a,b)
            assert f.error(x,y)<=f.error(a,b)
        counts['midpoint_and_superadditivity']+=1
print(dict(counts))
print('PASS: exact rational arithmetic throughout; continuous compatibility intervals, cover trimming, three-piece refinement, and Jensen superadditivity.')
