"""Exact two-variable diagnostics; not a production convex-MIQP solver.

The first variable is binary and the second lies in [0,1]. Both integer
labels are enumerated solely to provide an exact small recourse oracle.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
import json


def value(poly, a):
    return poly[0] * a * a + poly[1] * a + poly[2]


def add(poly, linear):
    return poly[0], poly[1] + linear, poly[2]


def minimum(poly, lo, hi):
    points = [lo, hi]
    if poly[0]:
        stationary = -poly[1] / (2 * poly[0])
        if lo <= stationary <= hi:
            points.append(stationary)
    return min((value(poly, x), x) for x in points)


@dataclass
class Piece:
    label: Q
    slope: Q
    intercept: Q
    lo: object
    hi: object
    poly: tuple

    def contains(self, a):
        return (self.lo is None or self.lo <= a) and (self.hi is None or a <= self.hi)

    def covers(self, lo, hi):
        return self.contains(lo) and self.contains(hi)


class Model:
    alpha = Q(4)
    T = (Q(1, 4), Q(1, 2))

    def __init__(self, name, pii, pic, pcc, bi, bc):
        self.name = name
        self.pii, self.pic, self.pcc = map(Q, (pii, pic, pcc))
        self.bi, self.bc = map(Q, (bi, bc))
        assert self.pii > 0 and self.pii * self.pcc > self.pic ** 2
        self.aii = self.pii - self.alpha * self.T[0] ** 2
        self.aic = self.pic - self.alpha * self.T[0] * self.T[1]
        self.acc = self.pcc - self.alpha * self.T[1] ** 2

    def original(self, point, gamma):
        z, y = point
        return (self.aii * z*z / 2 + self.aic*z*y + self.acc*y*y/2
                + (self.bi+gamma[0])*z + (self.bc+gamma[1])*y)

    def setup(self, gamma):
        norm2 = sum(t*t for t in self.T)
        self.d = sum(t*g for t, g in zip(self.T, gamma)) / norm2
        self.r = tuple(g-t*self.d for t, g in zip(self.T, gamma))
        self.gamma = gamma
        self.pieces = []
        for z in (Q(0), Q(1)):
            offset = self.pic*z + self.bc + self.r[1]
            free_slope = self.alpha*self.T[1]/self.pcc
            free_intercept = -offset/self.pcc
            left = offset/(self.alpha*self.T[1])
            right = (self.pcc+offset)/(self.alpha*self.T[1])
            for slope, intercept, lo, hi in [(Q(0), Q(0), None, left),
                    (free_slope, free_intercept, left, right),
                    (Q(0), Q(1), right, None)]:
                a2 = self.pcc*slope*slope/2-self.alpha*self.T[1]*slope+self.alpha/2
                a1 = (self.pic*z*slope+self.pcc*slope*intercept
                      +(self.bc+self.r[1])*slope
                      -self.alpha*(self.T[0]*z+self.T[1]*intercept))
                a0 = (self.pii*z*z/2+self.pic*z*intercept+self.pcc*intercept*intercept/2
                      +(self.bi+self.r[0])*z+(self.bc+self.r[1])*intercept)
                self.pieces.append(Piece(z,slope,intercept,lo,hi,(a2,a1,a0)))

    def oracle(self, a):
        by_label = []
        for label in (Q(0),Q(1)):
            records = [(value(p.poly,a),p,(label,p.slope*a+p.intercept))
                       for p in self.pieces if p.label==label and p.contains(a)]
            assert records and len({record[0] for record in records})==1
            record=records[0]
            x=record[2]
            assert 0 <= x[1] <= 1
            direct=self.original(x,self.gamma)+self.alpha*(a-sum(t*v for t,v in zip(self.T,x)))**2/2-self.d*sum(t*v for t,v in zip(self.T,x))
            # original includes gamma; remove d*T*x to leave the residual.
            assert record[0]==direct
            by_label.append(record)
        order=sorted(range(2),key=lambda i:(by_label[i][0],i))
        winner=by_label[order[0]]
        other=by_label[order[1]]
        return winner,other,other[0]-winner[0]

    def true_cell(self, lo, hi):
        candidates=[]
        for p in self.pieces:
            left=lo if p.lo is None else max(lo,p.lo)
            right=hi if p.hi is None else min(hi,p.hi)
            if left<=right:
                candidates.append(minimum(add(p.poly,self.d),left,right))
        return min(candidates)

    def reference(self):
        candidates=[]
        for z in (Q(0),Q(1)):
            poly=(self.acc/2,self.aic*z+self.bc+self.gamma[1],
                  self.aii*z*z/2+(self.bi+self.gamma[0])*z)
            val,y=minimum(poly,Q(0),Q(1))
            candidates.append((val,(z,y)))
        return min(candidates)


def run(model,gamma,sigma,cap,stats):
    model.setup(gamma)
    enlarged=sigma*sum(abs(t) for t in model.T)/sum(t*t for t in model.T)/model.alpha
    lo,hi=-enlarged,sum(model.T)+enlarged
    width=hi-lo
    reference,reference_x=model.reference()
    star=reference-model.d**2/(2*model.alpha)
    assert model.true_cell(lo,hi)[0]==star
    cells=[(lo,hi)]
    incumbent=None
    incumbent_x=None
    for stage in range(cap+1):
        h=width/Q(2**stage)
        correction=model.alpha*h*h/8
        pending=[]
        for left,right in cells:
            stats['cells']+=1
            records=[]
            for a in (left,right):
                win,other,gap=model.oracle(a)
                val=win[0]+model.d*a
                records.append((a,win,other,gap,val))
                if incumbent is None or val<incumbent:
                    incumbent,incumbent_x=val,win[2]
            bound=min(r[4] for r in records)-correction
            assert bound<=model.true_cell(left,right)[0]
            closed=False
            for a,win,other,gap,val in records:
                piece=win[1]
                if piece.covers(left,right) and gap>=model.alpha*h:
                    # Exact independent check of this whole-cell dominance:
                    for alternate in model.pieces:
                        l=left if alternate.lo is None else max(left,alternate.lo)
                        u=right if alternate.hi is None else min(right,alternate.hi)
                        if l<=u:
                            difference=tuple(x-y for x,y in zip(alternate.poly,piece.poly))
                            assert minimum(difference,l,u)[0]>=0
                    optimum,aopt=minimum(add(piece.poly,model.d),left,right)
                    assert optimum==model.true_cell(left,right)[0]
                    x=(piece.label,piece.slope*aopt+piece.intercept)
                    if optimum<incumbent:
                        incumbent,incumbent_x=optimum,x
                    stats['closures']+=1
                    closed=True
                    break
            if not closed:
                pending.append((left,right,bound,min(records,key=lambda r:r[4])))
        assert star<=incumbent<=star+correction
        retained=[]
        for left,right,bound,record in pending:
            if bound>incumbent:
                stats['prunes']+=1
                continue
            a,win,other,gap,val=record
            assert val-star<=2*correction
            image=sum(t*x for t,x in zip(model.T,win[2]))
            assert (model.alpha*(a-image)+model.d)**2<=2*model.alpha*(val-star)
            if win[1].covers(left,right):
                assert gap<model.alpha*h
                for witness in (win[2],other[2]):
                    assert model.original(witness,gamma)<=reference+2*correction+gap
                stats['label_gap_events']+=1
            else:
                stats['slice_region_events']+=1
            retained.extend(((left,(left+right)/2),((left+right)/2,right)))
        stats['levels']+=1
        if not retained:
            assert incumbent==star
            assert model.original(incumbent_x,gamma)==reference
            stats['closure_solved']+=1
            break
        cells=retained
    else:
        assert model.original(reference_x,gamma)==reference
        stats['same_draw_fallbacks']+=1
    stats['cases']+=1


def main():
    stats=dict.fromkeys(('cases','levels','cells','closures','prunes','label_gap_events',
                         'slice_region_events','closure_solved','same_draw_fallbacks'),0)
    model=Model('interior competing integer well',2,1,1,Q(-15,16),0)
    model.setup((Q(0),Q(0)))
    ends=[model.oracle(a) for a in (Q(0),Q(1,2))]
    assert all(win[2][0]==0 and gap==Q(1,16) for win,other,gap in ends)
    middle=model.oracle(Q(1,4))[0]
    assert middle[2][0]==1 and middle[0]==Q(-1,16)
    assert model.true_cell(Q(0),Q(1,2))[0]==Q(-1,16)
    assert all(gap<model.alpha*Q(1,2) for win,other,gap in ends)
    stats['unsafe_corner_label_counterexamples']=1
    sigma=Q(3,32)
    noise=[-sigma,-sigma/3,sigma/3,sigma]
    for gamma in product(noise,repeat=2):
        run(model,gamma,sigma,9,stats)
    negative=Model('negative continuous slice curvature',3,1,Q(1,2),Q(-15,16),0)
    positive=Model('positive continuous slice curvature',Q(1,8),0,2,0,0)
    for other in (negative,positive):
        for gamma in (tuple(noise[:2]),tuple(noise[2:]),(noise[0],noise[-1])):
            run(other,gamma,sigma,9,stats)
    # The finite-grid endpoint/interior draw has two exactly optimal labels.
    model.setup((-sigma/3,-sigma))
    f0=model.original((Q(0),Q(1)),model.gamma)
    f1=model.original((Q(1),Q(0)),model.gamma)
    assert f0==f1==model.reference()[0]
    stats['literal_finite_grid_integer_tie']=1
    # A deliberately early cap tests the same-draw fallback independently
    # of whether this fixture would close at the theorem's larger cutoff.
    run(model,(-sigma/3,-sigma),sigma,0,stats)
    assert stats['closures'] and stats['label_gap_events'] and stats['same_draw_fallbacks']
    print(json.dumps({'status':'passed',**stats},indent=2))


if __name__=='__main__':
    main()
