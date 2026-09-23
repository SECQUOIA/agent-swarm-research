"""Compare independent full continuous-leader algorithms and boundary outcomes."""
from pathlib import Path
import sys, json, random
import sympy as s
import original_faces as faces
import compressed_solver as compressed
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'code/bilevel_nonconvex'))
import scalar_solver as old

def data(d,c,u,h,gamma=1,lower=None,upper=None,L=0,U=1):
    n=len(d)
    return dict(d=list(map(str,d)),c=list(map(str,c)),u=list(map(str,u)),h=str(h),gamma=str(gamma),
                lower=list(map(str,lower or [0]*n)),upper=list(map(str,upper or [1]*n)),x_lower=str(L),x_upper=str(U))

def inputs():
    jump=data([1,1],[-1,'-1/2'],[1,1],'3/5')
    false=data([1],[-1],[1],3,L=1,U=3)
    cases=[('capacity_jump',jump,[dict(a='0',b=['1','1'],rhs='1')]),
           ('unconstrained_jump',jump,[]),
           ('false_convexification',false,[dict(a='0',b=['1'],rhs='1/2'),dict(a='0',b=['-1'],rhs='-1/2')]),
           ('isolated_price',jump,[dict(a='1',b=['0','0'],rhs='17/20'),dict(a='-1',b=['0','0'],rhs='-17/20')]),
           ('isolated_response',data([1],[-1],[1],0),[dict(a='0',b=['1'],rhs='1/3'),dict(a='0',b=['-1'],rhs='-1/3')]),
           ('signed_zero_reversed',data([1,2,3],['-1/2','1/3',-2],[1,-1,0],'4/5',gamma=-1,lower=[-1,0,0],upper=[1,2,1],L=-2,U=2),[]),
           ('fixed_box',data([1,2],[0,-1],[1,1],'3/5',lower=[1,0],upper=[1,2],L=-2,U=2),[]),
           ('single_price_tie',data([1],[-1],[1],3,L=2,U=2),[])]
    rng=random.Random(61007)
    for j in range(10):
        n=2+j%3;d=[s.Rational(rng.randint(4,12),4) for _ in range(n)];u=[rng.choice([-2,-1,1,2]) for _ in range(n)]
        h=s.Rational(7,5)/sum(ui*ui/di for ui,di in zip(u,d))
        ins=data(d,[-s.Rational(rng.randint(0,12),4) for _ in range(n)],u,h,L=-1,U=3)
        rows=[] if j%2==0 else [dict(a='0',b=list(map(str,u)),rhs=str(sum(max(0,v) for v in u)/2))]
        cases.append((f'random_{j}',ins,rows))
    return cases

def validate_witness(out, ref, rows, semantics):
    if out is None:return
    out=out if isinstance(out,dict) else out.__dict__
    if not out['attained']:return
    x,w,z=out['x'],out['w'],out['z'];d=ref.data
    assert faces.compare(d['x_lower'],x)<=0 and faces.compare(x,d['x_upper'])<=0
    assert all(faces.compare(lo,v)<=0 and faces.compare(v,hi)<=0 for lo,v,hi in zip(d['lower'],z,d['upper']))
    assert faces.compare(w,sum(s.Rational(ui)*zi for ui,zi in zip(d['u'],z)))==0
    assert faces.compare(out['value'],x*w)==0
    assert all(faces.compare(s.Rational(r['a'])*x+sum(s.Rational(b)*v for b,v in zip(r['b'],z)),s.Rational(r['rhs']))<=0 for r in rows)
    cost=sum(s.Rational(di)*zi**2/2+s.Rational(ci)*zi for di,ci,zi in zip(d['d'],d['c'],z))-s.Rational(d['h'])*w**2/2+s.Rational(d['gamma'])*x*w
    eligible=[f for f in ref.faces if faces.compare(f.lo,x)<=0 and faces.compare(x,f.hi)<=0]
    assert eligible and all(faces.compare(cost,faces.evaluate(f.cost,x))<=0 for f in eligible)
    winners=[f for f in eligible if faces.compare(cost,faces.evaluate(f.cost,x))==0]
    assert any(all(faces.compare(a,b)==0 for a,b in zip(z,f.point(x))) for f in winners)
    if semantics=='pessimistic':
        assert all(faces.compare(out['value'],faces.evaluate((0,*f.w),x))<=0 for f in winners)
        assert all(faces.compare(s.Rational(r['a'])*x+sum(s.Rational(b)*v for b,v in zip(r['b'],f.point(x))),s.Rational(r['rhs']))<=0 for f in winners for r in rows)

def compare_case(name,ins,rows):
    ref=faces.build(ins);atlas=compressed.build_atlas(compressed.Instance(**ins))
    cons=[compressed.Constraint(**r) for r in rows]
    for semantics in ('optimistic','pessimistic'):
        a=faces.optimize(ref,rows,semantics);b=compressed.optimize_tariff(atlas,cons,semantics)
        assert (a is None)==(b is None),(name,semantics,a,b)
        if name=='false_convexification':
            assert b is None,(name,semantics,b)
            assert compressed.optimize_tariff(atlas,iter(cons),semantics) is None,('constraint iterator',semantics)
        if a is not None:
            assert faces.compare(a['value'],b.value)==0 and a['attained']==b.attained,(name,semantics,a,b)
            validate_witness(a,ref,rows,semantics);validate_witness(b,ref,rows,semantics)
    # All baseline cut prices and rational cell samples: compare the full response SET.
    for x,win in ref.points+[(faces.interior(a,b),win) for a,b,win in ref.cells]:
        expected={tuple(map(s.simplify,ref.faces[i].point(x))) for i in win}
        actual=set()
        for p,rs in atlas.points:
            if faces.compare(p,x)==0:
                for r in rs:
                    assert r.left==r.right # baseline contract excludes flat directions
                    actual.add(tuple(map(s.simplify,r.piece.z(r.left))))
        if not actual:
            for a,b,win2 in atlas.cells:
                if faces.compare(a,x)<0 and faces.compare(x,b)<0:
                    for i in win2:
                        br=atlas.branches[i];w=br.w.subs(compressed.X,x) if hasattr(br.w,'subs') else br.w
                        actual.add(tuple(map(s.simplify,br.piece.z(w))))
        assert actual==expected,(name,x,expected,actual)
    return dict(name=name,faces=len(ref.faces),cuts=len(ref.cuts),patterns=ref.patterns_examined)

def main():
    (Path(__file__).resolve().parents[1]/'verification/stage06-author').mkdir(parents=True,exist_ok=True)
    records=[]
    for name,ins,rows in inputs():
        record=compare_case(name,ins,rows);records.append(record);print('PASS',record,flush=True)
    # Deliberate excluded singular input: reject, while compressed method retains continuum.
    flat=data([1],[0],[1],1,L=-1,U=1)
    try: faces.build(flat)
    except ValueError as err: assert 'Singular principal' in str(err)
    else: raise AssertionError('Singular minor was accepted')
    atlas=compressed.build_atlas(compressed.Instance(**flat))
    assert any(x==0 and any(r.left==0 and r.right==1 for r in rs) for x,rs in atlas.points)
    assert compressed.optimize_tariff(atlas,[compressed.Constraint(0,(1,),'1/2'),compressed.Constraint(0,(-1,),'-1/2')]).attained
    # Fast paths: compare the entire scalar atlas and upper outputs against unchanged solver.
    special=[flat,data([1,2],[-1,-2],[0,0],1,L=-2,U=1),data([1],[0],[1],1,lower=[1],upper=[1],L=-2,U=1)]
    for ins in special:
        a=compressed.build_atlas(compressed.Instance(**ins));b=old.build_atlas(old.Instance(**ins))
        assert str(a)==str(b)
        for semantics in ('optimistic','pessimistic'):
            assert str(compressed.optimize_tariff(a,semantics=semantics))==str(old.optimize_tariff(b,semantics=semantics))
    print('PASS: singular-minor rejection, flat continuum, singleton aggregate, fixed box and exact fast-path regressions')
    (Path(__file__).resolve().parents[1]/'verification/stage06-author/full-task-checks.json').write_text(json.dumps(records,indent=2)+'\n')
if __name__=='__main__':main()
