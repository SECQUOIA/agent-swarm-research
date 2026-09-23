from pathlib import Path
import sys, json, random
import sympy as s
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
sys.path.insert(0,str(ROOT/'code/bilevel_nonconvex'))
sys.path.insert(0,str(BASE/'isolated/code'))
import check_full_task as checks
import compressed_solver as comp
import original_faces as faces
records=[]
for name,ins,rows in checks.inputs():
    records.append(checks.compare_case(name,ins,rows));print('existing',name,flush=True)
rng=random.Random(80904)
for j in range(12):
    n=1+j%3
    d=[s.Rational(rng.randint(2,9),3) for _ in range(n)]
    u=[rng.choice([-2,-1,0,1,2]) for _ in range(n)]
    c=[s.Rational(rng.randint(-5,5),2) for _ in range(n)]
    h=s.Rational(rng.randint(0,8),7)
    ins=checks.data(d,c,u,h,gamma=rng.choice([-2,1,3]),lower=[-1]*n,upper=[2]*n,L=-2,U=3)
    rows=[dict(a='1/3',b=[str(rng.randint(-2,2)) for _ in range(n)],rhs='2/3')]
    try:records.append(checks.compare_case('new_'+str(j),ins,rows))
    except ValueError as e:
        assert 'Singular principal' in str(e);print('declared singular rejection',j)
    print('fresh',j,flush=True)
ins=checks.data([1,1],[0,0],[1,-1],'1/2',lower=[-1,-1],upper=[1,1],L=-1,U=1)
a=comp.build_atlas(comp.Instance(**ins))
rs=next(rs for x,rs in a.points if x==0)
assert any(r.left==-2 and r.right==2 for r in rs)
for w in [s.Rational(-3,2),s.Rational(1,2),s.Rational(7,4)]:
    z=(w/2,-w/2);assert sum(v*v/2 for v in z)-w*w/4==0
rows=[comp.Constraint(0,(1,0),'1/4'),comp.Constraint(0,(-1,0),'-1/4')]
o=comp.optimize_tariff(a,iter(rows),'optimistic');p=comp.optimize_tariff(a,iter(rows),'pessimistic')
assert o.value==0 and o.attained and o.x==0 and o.w==s.Rational(1,2) and o.z==(s.Rational(1,4),-s.Rational(1,4)) and p is None
(BASE/'independent-checks.json').write_text(json.dumps(records,indent=2))
print('PASS: full response sets and both upper tasks; independent two-coordinate signed flat continuum')
