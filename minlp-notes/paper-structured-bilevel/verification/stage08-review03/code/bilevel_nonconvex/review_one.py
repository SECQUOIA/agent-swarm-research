"""Independent exact adversarial checks of envelope and upper semantics."""
from pathlib import Path
import importlib.util
import sys
import sympy as s

spec = importlib.util.spec_from_file_location('reviewed_scalar_solver', Path(__file__).with_name('scalar_solver.py'))
solver = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = solver
spec.loader.exec_module(solver)
I, C = solver.Instance, solver.Constraint
checks = 0


def expect_equal(a, b):
    global checks
    assert s.simplify(a-b) == 0, (a,b)
    checks += 1


def check_opt(ins, value, attained, constraints=(), semantics='optimistic'):
    global checks
    out = solver.optimize_tariff(solver.build_atlas(ins), constraints, semantics)
    assert out is not None
    expect_equal(out.value, value)
    assert out.attained == attained, out
    checks += 1
    if attained:
        expect_equal(sum(ui*zi for ui,zi in zip(ins.u,out.z)),out.w)
        for l,z,r in zip(ins.lower,out.z,ins.upper):
            assert solver.sign(z-l)>=0 and solver.sign(r-z)>=0
            checks += 1
    return out


# Full flat interval at tariff 1; all points of the interval are global responses.
flat = I((1,),(-1,),(1,),(0,),(1,),1,1,0,2)
atlas = solver.build_atlas(flat)
responses = next(rs for x,rs in atlas.points if x == 1)
assert any(r.left == 0 and r.right == 1 for r in responses)
checks += 1
check_opt(flat,1,True)
check_opt(flat,1,False,semantics='pessimistic')
# Feasibility can consist of a single point inside a continuum of responses.
rows = (C(0,(1,),s.Rational(3,4)), C(0,(-1,),-s.Rational(1,4)))
check_opt(flat,s.Rational(3,4),True,rows)
assert solver.optimize_tariff(atlas,rows,'pessimistic') is None
checks += 1
point_rows = (C(0,(1,),s.Rational(2,3)),C(0,(-1,),-s.Rational(2,3)))
check_opt(flat,s.Rational(2,3),True,point_rows)
# Strictly nonconvex follower: its two endpoints tie at tariff 1/2.
nonconvex = I((1,),(0,),(1,),(0,),(1,),2,1,0,2)
check_opt(nonconvex,s.Rational(1,2),True)
check_opt(nonconvex,s.Rational(1,2),False,semantics='pessimistic')
# Negative tariffs reverse optimistic response selection within a flat interval.
negative = I((1,),(1,),(1,),(0,),(1,),1,1,-2,0)
require_half = (C(0,(-1,),-s.Rational(1,2)),)
check_opt(negative,-s.Rational(1,2),True,require_half)
check_opt(negative,-1,False,require_half,'pessimistic')
# Constant aggregate, unused coordinates, fixed coordinates, singleton tariff domain.
constant = I((2,3),(-1,5),(0,0),(-2,-2),(2,2),3,-2,-1,1)
result = check_opt(constant,0,True)
expect_equal(result.z[0],s.Rational(1,2))
expect_equal(result.z[1],-s.Rational(5,3))
fixed = I((1,2),(3,-4),(2,-1),(1,2),(1,2),4,-1,-3,7)
check_opt(fixed,0,True)
one_tariff = I((1,),(-1,),(1,),(0,),(1,),1,1,1,1)
check_opt(one_tariff,1,True)
check_opt(one_tariff,0,True,semantics='pessimistic')

# Fiber invariance under coordinate sign flips and nonzero rational aggregate scaling.
base = I((2,3,1),(-2,1,-1),(1,2,0),(-1,0,-2),(2,1,2),2,1,-2,2)
flip = I(base.d,(-base.c[0],base.c[1],base.c[2]),(-1,2,0),
         (-2,0,-2),(1,1,2),base.h,base.gamma,base.x_lower,base.x_upper)
a,b = solver.build_atlas(base),solver.build_atlas(flip)
for x in map(s.Rational,(-2,-1,0,1,2)):
    wa,va = solver._winners(a.branches,x)
    wb,vb = solver._winners(b.branches,x)
    expect_equal(va,vb)
    # gamma sign change x -> -x leaves follower objective unchanged.
reverse = I(base.d,base.c,base.u,base.lower,base.upper,base.h,-base.gamma,-2,2)
r = solver.build_atlas(reverse)
for x in map(s.Rational,(-2,-1,0,1,2)):
    expect_equal(solver._winners(a.branches,x)[1],solver._winners(r.branches,-x)[1])

# Exact comparisons of close quadratic algebraic numbers must not use tolerances.
for k in (1,20,100):
    small = s.sqrt(2+s.Rational(1,10**k))-s.sqrt(2)
    assert solver.sign(small) == 1
    assert solver.sign(-small) == -1
    checks += 2
# Rational-input-only interface must reject values already rounded to floating point.
import numpy as np
for value in (0.1,s.Float('0.1'),np.float32('0.1'),np.float64('0.1')):
    try:
        solver.rat(value)
    except TypeError:
        checks += 1
    else:
        raise AssertionError(('inexact input silently accepted',value))
for a,b in ((s.sqrt(2),s.sqrt(3)),(-s.sqrt(3),-s.sqrt(2)),
            (s.sqrt(2),s.sqrt(2)+s.Rational(1,10**30))):
    sample = solver.rational_between(a,b)
    assert sample.is_Rational is True
    assert solver.sign(sample-a)>0 and solver.sign(b-sample)>0
    checks += 2
print({'independent_exact_checks':checks, 'status':'passed'})

# Direct envelope tests separate contact preservation from follower generation.
# A tangency never changes the winning open branch but must remain a point event.
piece = solver.FiberPiece(0,0,(0,),(0,),0,0,0)
def artificial(cost,left=-2,right=2):
    return solver.Branch(piece,s.S.Zero,s.sympify(cost),s.Rational(left),s.Rational(right))
X=solver.X
branches = [artificial(0),artificial((X-s.Rational(1,3))**2),
            artificial(-1,s.Rational(2,3),s.Rational(2,3))]
envelope,contacts = solver._insert_envelope(branches,s.Rational(-2),s.Rational(2))
assert s.Rational(1,3) in contacts and s.Rational(2,3) in contacts
assert all(old==0 for _,_,old in envelope)
assert solver._winners(branches,s.Rational(1,3))[0]==[0,1]
assert solver._winners(branches,s.Rational(2,3))[0]==[2]
checks += 4
# Later dominance must not erase the contact registry; final global comparison
# removes the obsolete tie without asserting it remains globally optimal.
branches.append(artificial(-2))
envelope,contacts = solver._insert_envelope(branches,s.Rational(-2),s.Rational(2))
assert s.Rational(1,3) in contacts
assert all(old==3 for _,_,old in envelope)
assert solver._winners(branches,s.Rational(1,3))[0]==[3]
checks += 3
# Two crossings plus a bounded-domain insertion test the interval split logic.
branches=[artificial(0),artificial(X**2-1),artificial(-2,-s.Rational(1,2),s.Rational(1,2))]
envelope,contacts=solver._insert_envelope(branches,s.Rational(-2),s.Rational(2))
for x in (s.Rational(-3,2),s.Rational(-3,4),s.S.Zero,s.Rational(3,4),s.Rational(3,2)):
    predicted = next(old for a,b,old in envelope if a<x<b)
    assert predicted in solver._winners(branches,x)[0]
    checks += 1
print({'independent_exact_checks_including_incremental_envelope':checks,'status':'passed'})
