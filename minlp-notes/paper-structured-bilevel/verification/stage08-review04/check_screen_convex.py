from pathlib import Path
import sys,json,itertools
from fractions import Fraction as F
import sympy as s
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[2]
sys.path.insert(0,str(ROOT/'code/bilevel_reopened'))
import approximate_structure_checks as a
import quadratic_solver as q
records=[]
for seed in (809041,809042,809043):
 Q,Qh,c,C,obj,rows=a.dense_family(3,seed,200)
 cells=a.diagonal_cells(list(Qh.diagonal()),c,C)
 ans,stats=a.optimize_screened(Q,Qh,c,C,cells,obj,rows)
 ref=a.optimize_exhaustive(Q,c,C,obj,rows)
 assert (ans is None)==(ref is None)
 if ans is not None:assert ans[0]==ref[0];a.check_kkt(Q,c,C,ans[1],ans[2])
 qi=Q.inv()
 for cell in cells:
  status,eta=a.screen(Q,Qh,qi,c,C,cell)
  for x in (cell.lo,(cell.lo+cell.hi)/2,cell.hi):
   ansx=a.optimize_exhaustive(Q,c,C,(0,s.zeros(3,1)),[],x,x);z=ansx[2];y=cell.intercept+cell.slope*x
   e=z-y;p=(Q-Qh)*y
   assert (e.T*Q*e+p.T*e)[0]<=0
   for vec in (s.Matrix([1,-2,3]),s.Matrix([-1,0,2])):
    center=(vec.T*e+vec.T*qi*p/2)[0]
    assert 4*center**2 <= (vec.T*qi*vec)[0]*(p.T*qi*p)[0]
   g=Q*z+c+C*x
   for i,tag in enumerate(status):
    assert tag=='?' or (tag=='L' and z[i]==0) or (tag=='U' and z[i]==1) or (tag=='F' and g[i]==0)
 records.append(stats)
for h in (F(-1,10),F(0),F(1,3)):
 p=q.Problem((2,3,4),((1,),(-1,),(0,)),((h,),),(-1,F(1,3),-2),(2,-2,0),F(-2),F(3))
 path=q.exhaustive_path(p);assert q.verify_path(p,path)
 rows=[(F(1,2),(1,-1,2),F(3,2))]
 kw=dict(objective_xx=F(-1,5),objective_xz=(1,-2,3))
 f=q.optimize_path(p,path,F(1,4),(1,2,-1),iter(rows),**kw)
 g=q.optimize_aligned_rank_one(p,F(1,4),(1,2,-1),iter(rows),gamma=2,**kw)
 assert (f is None)==(g is None)
 if f is not None:assert f['objective']==g['objective']
print('PASS: three new dense screening families, exact directional ellipsoid and whole-cell statuses; signed/zero aligned convex sweeps with negative/zero/positive rank coefficient and quadratic upper data')
(BASE/'screen-convex-checks.json').write_text(json.dumps(records,indent=2))
