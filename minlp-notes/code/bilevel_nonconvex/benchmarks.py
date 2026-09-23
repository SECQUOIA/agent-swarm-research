"""Independent original-coordinate checks and reproducible small benchmarks.

Run with the repository Python environment. Singular active faces are skipped:
if a global minimizer has a singular free Hessian, its stationary null direction
can be followed to a smaller box face without changing objective. Repeating
reaches a nonsingular stationary face or a vertex. Thus this enumerator computes
the exact global value, but does not describe all points of a flat minimizer set.
"""
import itertools
import json
from pathlib import Path
import random
import platform
import statistics
import time
import sympy as s
from scalar_solver import Instance, Constraint, X, build_atlas, optimize_tariff


def exact_sign(v):
    v = s.simplify(v)
    if v == 0:
        return 0
    return 1 if bool(v > 0) else -1


def objective(ins, x, z):
    w = sum(ui*zi for ui, zi in zip(ins.u,z))
    return s.expand(sum(di*zi**2/2+ci*zi for di,ci,zi in zip(ins.d,ins.c,z))
                    -ins.h*w*w/2+ins.gamma*x*w)


def enumerate_faces(ins):
    """Original-coordinate candidate affine responses, without fiber machinery."""
    n = len(ins.d)
    Q = s.diag(*ins.d)-ins.h*s.Matrix(ins.u)*s.Matrix(ins.u).T
    candidates = []
    singular = 0
    for pattern in itertools.product((-1,0,1), repeat=n):
        free = [i for i,p in enumerate(pattern) if p == 0]
        fixed = [i for i,p in enumerate(pattern) if p != 0]
        z = [None if p == 0 else ins.lower[i] if p == -1 else ins.upper[i]
             for i,p in enumerate(pattern)]
        if free:
            A = Q.extract(free,free)
            if A.det() == 0:
                singular += 1
                continue
            rhs = s.Matrix([-ins.c[i]-ins.gamma*X*ins.u[i]
                            -sum(Q[i,j]*z[j] for j in fixed) for i in free])
            sol = A.inv()*rhs
            for i,v in zip(free,sol):
                z[i] = s.expand(v)
        candidates.append(tuple(z))
    return candidates,singular


def original_global(ins,x,candidates):
    best = None
    best_z = []
    for branch in candidates:
        z = tuple(v.subs(X,x) if hasattr(v,'subs') else v for v in branch)
        if any(exact_sign(v-l)<0 or exact_sign(v-r)>0
               for v,l,r in zip(z,ins.lower,ins.upper)):
            continue
        val = objective(ins,x,z)
        cmp = -1 if best is None else exact_sign(val-best)
        if cmp < 0:
            best,best_z = val,[z]
        elif cmp == 0:
            best_z.append(z)
    return best,best_z


def atlas_responses(atlas,x):
    for p,rs in atlas.points:
        if exact_sign(p-x) == 0:
            return [r.piece.z(w) for r in rs
                    for w in (r.left,(r.left+r.right)/2,r.right)]
    for a,b,indices in atlas.cells:
        if exact_sign(x-a)>0 and exact_sign(x-b)<0:
            return [atlas.branches[i].piece.z(atlas.branches[i].w.subs(X,x)
                    if hasattr(atlas.branches[i].w,'subs') else atlas.branches[i].w)
                    for i in indices]
    raise AssertionError('Price missing from atlas')


def family(n, seed=17):
    rng = random.Random(seed+n)
    d = tuple(s.Rational(rng.randint(8,16),8) for _ in range(n))
    u = tuple(s.Rational(rng.randint(4,8),4) for _ in range(n))
    # Negative local linear costs model consumer benefit; positive tariff reduces use.
    c = tuple(-s.Rational(rng.randint(4,24),8) for _ in range(n))
    h = s.Rational(7,5)/sum(ui*ui/di for ui,di in zip(u,d))
    return Instance(d,c,u,(0,)*n,(1,)*n,h,1,0,5)


def verify_suite():
    cases = [
        ('flat',Instance((1,),(0,),(1,),(0,),(1,),1,1,-1,1)),
        ('tariff_jump',Instance((1,),(-1,),(1,),(0,),(1,),2,1,0,2)),
        ('two_wells',Instance((1,1),(0,1),(1,1),(0,0),(1,1),'3/4',1,-2,2)),
        ('signed_zero',Instance((1,2,3),('-1/2','1/3',-2),(1,-1,0),(-1,0,0),(1,2,1),1,-1,-2,2)),
        ('fixed_coordinate',Instance((1,2),(0,-1),(1,1),(1,0),(1,2),1,1,-2,2)),
    ]
    cases += [(f'heterogeneous_{n}_{seed}',family(n,seed))
              for n,seed in ((2,3),(3,7),(4,11))]
    records=[]
    for name,ins in cases:
        start=time.perf_counter(); atlas=build_atlas(ins)
        cand,singular=enumerate_faces(ins)
        prices=[p for p,_ in atlas.points]
        prices += [ins.x_lower+(ins.x_upper-ins.x_lower)*s.Rational(k,8) for k in range(9)]
        checked=0
        for x in prices:
            best,_=original_global(ins,x,cand)
            rs=atlas_responses(atlas,x)
            assert rs
            for z in rs:
                assert all(exact_sign(v-l)>=0 and exact_sign(v-r)<=0
                           for v,l,r in zip(z,ins.lower,ins.upper))
                assert exact_sign(objective(ins,x,z)-best)==0,(name,x,z,best)
                checked += 1
        optima={}
        for semantics in ('optimistic','pessimistic'):
            opt=optimize_tariff(atlas,semantics=semantics)
            if opt.attained:
                best,zs=original_global(ins,opt.x,cand)
                assert exact_sign(objective(ins,opt.x,opt.z)-best)==0
                revenues=[opt.x*sum(ui*zi for ui,zi in zip(ins.u,z)) for z in zs]
                extreme=max(revenues) if semantics=='optimistic' else min(revenues)
                assert exact_sign(opt.value-extreme)==0
            optima[semantics]=dict(value=str(opt.value),attained=opt.attained,
                                   x=str(opt.x),limit_x=str(opt.limit_x))
        records.append(dict(name=name,n=len(ins.d),prices=len(prices),response_checks=checked,optima=optima,
                            original_face_candidates=len(cand),singular_faces_skipped=singular,
                            seconds=time.perf_counter()-start))
        print('verified',records[-1],flush=True)
    return records


def timings(cases=((2,17),(4,17),(8,17),(12,17),(24,17),(48,17),(8,31),(8,43))):
    records=[]
    for n,seed in cases:
        ins=family(n,seed)
        builds=[]; opts=[]; faces=[]; queries=[]
        for _ in range(3):
            t=time.perf_counter(); atlas=build_atlas(ins); builds.append(time.perf_counter()-t)
            t=time.perf_counter(); opt=optimize_tariff(atlas); opts.append(time.perf_counter()-t)
            if n<=4:
                t=time.perf_counter(); candidates,_=enumerate_faces(ins); faces.append(time.perf_counter()-t)
                t=time.perf_counter()
                for k in range(9):
                    original_global(ins,s.Rational(5*k,8),candidates)
                queries.append(time.perf_counter()-t)
        row=dict(n=n,seed=seed,rank_one_nonconvexity=str(ins.h*sum(ui*ui/di for ui,di in zip(ins.u,ins.d))),
                 fiber_pieces=len(atlas.pieces),candidate_branches=len(atlas.branches),
                 atlas_points=len(atlas.points),revenue=str(opt.value),attained=opt.attained,
                 build_seconds=builds,optimize_seconds=opts,
                 build_median=statistics.median(builds),optimize_median=statistics.median(opts),
                 original_face_build_seconds=faces,original_nine_price_seconds=queries)
        records.append(row); print('timed',row,flush=True)
    return records


def grouped_timings():
    base=Instance((1,1),(-1,s.Rational(-1,2)),(1,1),(0,0),(1,1),s.Rational(3,5),1,0,1)
    candidates,_=enumerate_faces(base)
    base_value,base_z=original_global(base,s.Rational(17,20),candidates)
    assert base_value==s.Rational(-9,320)
    assert set(base_z)=={(s.Rational(3,8),0),(1,s.Rational(5,8))}
    records=[]
    for n in (20,200,1000):
        m=n//2
        ins=Instance((1,)*n,(-1,)*m+(s.Rational(-1,2),)*m,(1,)*n,
                     (0,)*n,(1,)*n,s.Rational(3,5*m),1,0,1)
        row=Constraint(0,(1,)*n,m)
        builds=[]; opts=[]
        for _ in range(3):
            t=time.perf_counter(); atlas=build_atlas(ins); builds.append(time.perf_counter()-t)
            t=time.perf_counter(); opt=optimize_tariff(atlas,[row]); opts.append(time.perf_counter()-t)
            assert opt.attained and opt.x==s.Rational(17,20)
            assert opt.w==s.Rational(3*m,8) and opt.value==s.Rational(51*m,160)
        pess=optimize_tariff(atlas,[row],semantics='pessimistic')
        assert not pess.attained and exact_sign(pess.value-opt.value)==0
        records.append(dict(n=n,fiber_pieces=len(atlas.pieces),atlas_points=len(atlas.points),
                            build_seconds=builds,optimize_seconds=opts,
                            build_median=statistics.median(builds),optimize_median=statistics.median(opts),
                            revenue=str(opt.value),optimistic_attained=True,pessimistic_attained=False))
        print('grouped',records[-1],flush=True)
    return records


def local_trap():
    # For f(z)=z/4-z^2/2 on [0,1], z=0 is a strict local boundary minimum,
    # while z=1 is the unique global minimum. Both satisfy first-order KKT.
    from scipy.optimize import minimize
    runs=[]
    for initial in (0.0,0.05,0.5,1.0):
        result=minimize(lambda z: z[0]/4-z[0]**2/2,[initial],
                        jac=lambda z:[0.25-z[0]],bounds=[(0,1)],method='L-BFGS-B')
        runs.append(dict(initial=initial,z=float(result.x[0]),value=float(result.fun)))
    return dict(exact_global_z='1',exact_global_value='-1/4',runs=runs)


def main():
    out=dict(description='Exact nonconvex scalar tariff specialization; synthetic repeated runs.',
             sympy_version=s.__version__,python_version=platform.python_version(),
             platform=platform.platform(),verification=verify_suite(),timings=timings(),grouped_timings=grouped_timings(),local_trap=local_trap())
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':
    main()
