"""Independent signed/fixed-coordinate global-follower checks, exact arithmetic."""
from itertools import product
import random
import sympy as s
from scalar_solver import Instance, Constraint, build_atlas, fiber_pieces, optimize_tariff, _winners, sign, rational_between, rat, _insert_envelope, _roots, ordered, Branch, X


def face_minima(ins, x):
    """Enumerate original-space faces, not scalar fibers or solver branches.

    A minimum on a singular face can move along a Hessian null direction to
    a smaller face without changing its value. Thus nonsingular stationary
    faces plus vertices suffice for the global value, including flat problems.
    """
    n=len(ins.d); u=s.Matrix(ins.u)
    Q=s.diag(*ins.d)-ins.h*u*u.T
    c=s.Matrix(ins.c)+ins.gamma*x*u
    best=None; winners=[]
    for status in product((-1,0,1), repeat=n):
        free=[i for i,t in enumerate(status) if t==0]
        fixed=[i for i,t in enumerate(status) if t!=0]
        z=s.Matrix([ins.lower[i] if status[i]<=0 else ins.upper[i] for i in range(n)])
        if free:
            A=Q.extract(free,free)
            if A.det()==0: continue
            rhs=-c.extract(free,[0])-Q.extract(free,fixed)*z.extract(fixed,[0])
            zz=A.inv()*rhs
            for i,v in zip(free,zz): z[i]=v
        if any(z[i]<ins.lower[i] or z[i]>ins.upper[i] for i in range(n)): continue
        value=(z.T*Q*z)[0]/2+(c.T*z)[0]
        if best is None or value<best: best=value; winners=[tuple(z)]
        elif value==best and tuple(z) not in winners: winners.append(tuple(z))
    return best,winners


def check_response(ins,x):
    pieces=fiber_pieces(ins)
    # Independently use all endpoints plus stationary points at this fixed x.
    # Face enumeration remains the independently calculated reference value.
    ref,zref=face_minima(ins,x)
    found=[]
    for p in pieces:
        ws=[p.left,p.right]
        if p.A>0:
            w=-(p.B+ins.gamma*x)/(2*p.A)
            if p.left<=w<=p.right: ws.append(w)
        for w in ws:
            found.append(p.cost(x,w,ins.gamma))
            z=p.z(w)
            assert all(ins.lower[i]<=z[i]<=ins.upper[i] for i in range(len(z)))
            assert sum(ui*zi for ui,zi in zip(ins.u,z))==w
    assert min(found)==ref,(ins,x,min(found),ref)
    return len(zref)


def run():
    rng=random.Random(72641); cases=0; tied=0
    for k in range(70):
        n=rng.randint(1,4)
        lo=tuple(rng.randint(-2,0) for _ in range(n))
        hi=tuple(v+rng.randint(0,3) for v in lo)
        ins=Instance(tuple(rng.randint(1,4) for _ in range(n)),
                     tuple(rng.randint(-3,3) for _ in range(n)),
                     tuple(rng.randint(-2,2) for _ in range(n)),lo,hi,
                     s.Rational(rng.randint(0,8),3),rng.choice((-2,-1,1,2)),-2,2)
        for x in map(s.Rational,(-2,-1,0,1,2)):
            tied+=check_response(ins,x)>1; cases+=1
    # Flat continuum, negative tariff, exact universal upper rows.
    flat=Instance((1,),(0,),(1,),(-1,),(1,),1,1,0,0)
    atlas=build_atlas(flat)
    assert any(r.left==-1 and r.right==1 for _,rr in atlas.points for r in rr)
    row=Constraint(0,(1,),0)
    assert optimize_tariff(atlas,(row,), 'optimistic').attained
    assert optimize_tariff(atlas,(row,), 'pessimistic') is None
    # Opposite upper rows force an interior flat response, not an endpoint.
    rows=(Constraint(0,(1,),s.Rational(1,3)),Constraint(0,(-1,),-s.Rational(1,3)))
    assert optimize_tariff(atlas,rows).w==s.Rational(1,3)
    # Gamma sign: response is increasing for gamma<0; optimum at a positive endpoint.
    neg=Instance((1,),(0,),(1,),(0,),(1,),0,-1,0,1)
    opt=optimize_tariff(build_atlas(neg)); assert opt.value==1 and opt.x==1 and opt.w==1
    # Every coordinate fixed or irrelevant to the aggregate.
    fixed=Instance((1,2),(3,-1),(2,0),(2,-1),(2,1),3,-2,-1,1)
    opt=optimize_tariff(build_atlas(fixed)); assert opt.value==4 and opt.z==(2,s.Rational(1,2))
    # A genuine discontinuous global switch: pessimistic revenue loses its
    # maximizing tie response, so a supremum need not be attained.
    jump=Instance((1,),(0,),(1,),(0,),(1,),2,1,0,1)
    atlas=build_atlas(jump)
    optimistic=optimize_tariff(atlas)
    pessimistic=optimize_tariff(atlas,semantics='pessimistic')
    assert optimistic.value==s.Rational(1,2) and optimistic.attained
    assert pessimistic.value==s.Rational(1,2) and not pessimistic.attained
    assert pessimistic.limit_x==s.Rational(1,2) and pessimistic.limit_w==1
    # A rational sample avoids accidental degree-four witnesses.
    sample=rational_between(s.sqrt(2),s.sqrt(3))
    assert sample.is_Rational and s.sqrt(2)<sample<s.sqrt(3)
    for value in (0.1,s.Float('0.1'),s.sqrt(2)):
        try: rat(value)
        except TypeError: pass
        else: raise AssertionError(('nonrational accepted',value))
    # Source-positioning regression: convexification preserves values but
    # fabricates a follower response at a noncontact point.
    false_feasible=Instance((1,),(-1,),(1,),(0,),(1,),3,1,1,3)
    equal_half=(Constraint(0,(1,),s.Rational(1,2)),Constraint(0,(-1,),-s.Rational(1,2)))
    assert optimize_tariff(build_atlas(false_feasible),equal_half) is None
    # Test the insertion primitive independently of special branch generation.
    # A tangent must survive even if it changes no open-cell winner.
    p=fiber_pieces(jump)[0]
    synthetic=[Branch(p,0,s.S.Zero,-2,2),Branch(p,X,X**2,-1,1)]
    cells,contacts=_insert_envelope(synthetic,-2,2)
    assert any(sign(t)==0 for t in contacts)
    assert all(winner==0 for _,_,winner in cells)
    # An isolated candidate domain is visible through its retained endpoints.
    synthetic.append(Branch(p,1,-s.S.One,0,0))
    cells,contacts=_insert_envelope(synthetic,-2,2)
    assert any(sign(t)==0 for t in contacts)
    assert _winners(synthetic,s.S.Zero)[0]==[2]
    atlas_checks=0
    for k in range(8):
        n=2
        ins=Instance(tuple(rng.randint(1,3) for _ in range(n)),
                     tuple(rng.randint(-2,2) for _ in range(n)),
                     tuple(rng.choice((-2,-1,1,2)) for _ in range(n)),
                     (-1,0),(1,1),s.Rational(rng.randint(1,7),3),
                     rng.choice((-1,1)),-2,2)
        atlas=build_atlas(ins)
        for x,responses in atlas.points:
            ref,_=face_minima(ins,x)
            for response in responses:
                for w in (response.left,response.right,(response.left+response.right)/2):
                    assert sign(response.piece.cost(x,w,ins.gamma)-ref)==0
            atlas_checks+=1
        for left,right,winners in atlas.cells:
            x=rational_between(left,right)
            ref,_=face_minima(ins,x)
            for i in winners:
                branch=atlas.branches[i]
                value=branch.cost.subs(X,x) if hasattr(branch.cost,'subs') else branch.cost
                assert sign(value-ref)==0
            atlas_checks+=1
    envelope_checks=0
    for trial in range(5):
        branches=[Branch(p,0,s.S.Zero,-2,2)]
        for j in range(5):
            left=rng.randint(-2,1); right=rng.randint(left+1,2)
            cost=-rng.randint(0,2)*X**2+rng.randint(-3,3)*X+rng.randint(-2,2)
            branches.append(Branch(p,j+1,cost,left,right))
        env,contacts=_insert_envelope(branches,-2,2)
        cuts=[s.Integer(-2),s.Integer(2)]
        for i,b in enumerate(branches):
            cuts.extend((b.left,b.right))
            for c in branches[:i]:
                lo=max(b.left,c.left); hi=min(b.right,c.right)
                if lo<=hi:
                    cuts.extend(r for r in _roots(b.cost-c.cost) if sign(r-lo)>=0 and sign(r-hi)<=0)
        cuts=ordered(cuts)
        for left,right in zip(cuts,cuts[1:]):
            sample=rational_between(left,right)
            expected,best=_winners(branches,sample)
            actual=[winner for a,b,winner in env if sign(sample-a)>0 and sign(sample-b)<0]
            assert len(actual)==1 and actual[0] in expected
            envelope_checks+=1
        for x in cuts:
            win,_=_winners(branches,x)
            if len(win)>1 and any(branches[i].cost!=branches[win[0]].cost for i in win[1:]):
                assert any(sign(x-t)==0 for t in contacts)
    print({'random_original_space_face_comparisons':cases,'random_tied_cases':tied,
           'atlas_point_and_cell_face_comparisons':atlas_checks,
           'incremental_envelope_full_partition_comparisons':envelope_checks,
           'explicit_edge_cases':11,'status':'passed'})

if __name__=='__main__':run()
