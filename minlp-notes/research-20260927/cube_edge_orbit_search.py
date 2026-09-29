"""Discovery-only edge-contact search; no completeness claim."""
import itertools as it, numpy as np
from scipy.optimize import linprog
from scipy.linalg import null_space
V=list(it.product((0,1),repeat=3)); VI={v:i for i,v in enumerate(V)}
E=[(VI[v],VI[tuple(v[j]+(j==k) for j in range(3))],k) for v in V for k in range(3) if not v[k]]
EI={tuple(sorted((a,b))):i for i,(a,b,k) in enumerate(E)}
trans=[]
for p in it.permutations(range(3)):
 for c in V:
  f=[VI[tuple(v[p[j]]^c[j] for j in range(3))] for v in V]
  trans.append([EI[tuple(sorted((f[a],f[b])))] for a,b,k in E])
def canon(I):return min(tuple(sorted(t[i] for i in I)) for t in trans)
orbits=sorted(set(canon(I) for I in it.combinations(range(12),5)))
rng=np.random.default_rng(9017);sgn=np.array([(-1)**sum(v) for v in V])
def F(u):return sgn@(u[:8]**2)
def mat(u):
 s=u[:8];d=u[8:];a=s*s;c=a[0];q=np.diag(d*d);l=np.empty(3)
 for i in range(3):
  v=tuple(int(j==i) for j in range(3));l[i]=a[VI[v]]-c-d[i]**2
 for i,j in it.combinations(range(3),2):
  vi=tuple(int(k==i) for k in range(3));vj=tuple(int(k==j) for k in range(3));vij=tuple(int(k==i or k==j) for k in range(3))
  q[i,j]=q[j,i]=(a[VI[vij]]-a[VI[vi]]-a[VI[vj]]+c)/2
 return c,l,q
def rank(u,I):
 rows=[]
 for idx in I:
  a,b,k=E[idx];z=np.array(V[a],float);z[k]=u[a]/u[8+k];x,y,z=z
  rows.append([1,x,y,z,x*x,y*y,z*z,x*y,x*z,y*z])
  rows.append([[0,1,0,0,2*x,0,0,y,z,0],[0,0,1,0,0,2*y,0,x,0,z],[0,0,0,1,0,0,2*z,0,x,y]][k])
 return np.linalg.matrix_rank(rows,tol=1e-7)
print('orbits',len(orbits),flush=True)
for oi,I in enumerate(orbits):
 dirs=tuple(sorted(sum(E[e][2]==k for e in I) for k in range(3)))
 if dirs!=(1,2,2):continue
 A=[];B=[]
 for e,(a,b,k) in enumerate(E):
  row=np.zeros(11);row[a]=row[b]=1;row[8+k]=-1
  (A if e in I else B).append(row)
 row=np.zeros(11);row[8:]=1;A.append(row);rhs=[0]*5+[3]
 samples=[]
 for t in range(100):
  r=linprog(rng.normal(size=11),A_ub=-np.array(B),b_ub=-np.full(len(B),.02),A_eq=A,b_eq=rhs,bounds=[(.02,5)]*8+[(.1,3)]*3,method='highs')
  if r.success:samples.append(r.x)
 pos=[u for u in samples if F(u)>1e-8];neg=[u for u in samples if F(u)<-1e-8]
 if not pos or not neg:
  print('orbit',oi,'no signs',I,len(pos),len(neg),flush=True);continue
 done=False
 for trial in range(300):
  a=pos[rng.integers(len(pos))];b=neg[rng.integers(len(neg))];delta=b-a
  coeff=[F(delta),2*(sgn*a[:8])@delta[:8],F(a)]
  roots=np.roots(coeff)
  for t in roots:
   if abs(t.imag)>1e-8 or not 0<t.real<1:continue
   u=a+t.real*delta;c,l,q=mat(u)
   minors=[np.linalg.det(q[np.ix_([i,j],[i,j])]) for i,j in it.combinations(range(3),2)]
   if max(minors)<-1e-7 and rank(u,I)==9:
    print('FOUND',oi,I,'u',u.tolist(),'c',c,'l',l.tolist(),'Q',q.tolist(),'minors',minors,'a',a.tolist(),'b',b.tolist(),'t',t.real,flush=True)
    np.savez('/tmp/cube_edge_orbit_'+str(oi)+'.npz',u=u,a=a,b=b,E=np.array(I),c=c,l=l,Q=q)
    done=True;break
  if done:break
 if not done:print('orbit',oi,'no valid negative minors/rank',I,flush=True)
