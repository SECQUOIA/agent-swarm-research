from itertools import combinations, product
import sympy as S
R=S.Rational

def minor(A,rows,cols):
 return A[list(rows),list(cols)].det() if rows else S.Integer(1)

minor_checks=0; normal_checks=0
for T in [S.Matrix([[R(1,2),R(-1,2)]]),S.Matrix([[R(1,3),R(1,3),R(1,3)],[R(1,2),R(-1,2),0]]),S.Matrix([[R(1,2),R(1,2),0,0],[0,0,R(1,2),R(-1,2)]])]:
 k,n=T.shape
 assert (S.eye(k)-T*T.T).is_positive_semidefinite
 V=S.Matrix.hstack(*T.nullspace()) if n>k else S.zeros(n,0)
 D=(T*T.T).inv()*T;Pi=S.eye(n)-T.T*D
 for scale in [R(1),R(1000),R(1,1000)]:
  B=T.T.row_join(scale*V)
  assert B.det()!=0
  for t in range(k+1):
   for Q in combinations(range(k),t):
    Qc=[i for i in range(n) if i not in Q]
    summed=0;squares=0
    for K in combinations(range(n),t):
     J=[i for i in range(n) if i not in K]
     left=abs(B.det())*abs(minor(B.inv(),Qc,J))
     right=abs(minor(T.T,K,Q))
     assert left==right
     summed+=right;squares+=right*right;minor_checks+=1
    gram=T[list(Q),:]*T[list(Q),:].T if Q else S.zeros(0,0)
    gramdet=gram.det() if Q else S.Integer(1)
    assert squares==gramdet
    assert summed*summed<=S.binomial(n,t)*gramdet
    assert gramdet<=1
 for u in [S.eye(k)[:,i] for i in range(k)]+([S.Matrix([R(3,5),R(4,5)])] if k==2 else []):
  for v in [S.zeros(n,1),S.Matrix(list(range(1,n+1)))]:
   L=D.T*u+Pi.T*v
   assert T*L==u
   assert (L.T*L)[0]>=1
   normal_checks+=1
print('PASS:',minor_checks,'complementary-minor identities;',normal_checks,'ambient-normal checks')

# Exact sections of E_v for F(x,y)=xy, P=I, T=(1/2,-1/2), alpha=4.
# Independent original noise is gamma=(z,g); d=z-g and r=(z+g)/2 each.
z=S.Symbol('z',real=True);sigma=R(1,2);alpha=R(4)

def val(a,g,variable,probe=None):
 residual=(variable+g)/2
 xs=[2*a-residual,-2*a-residual]
 if probe is not None:
  point=[x.subs(z,probe) for x in xs]
 else:point=xs
 xs=[S.Integer(0) if p<=0 else S.Integer(1) if p>=1 else x for x,p in zip(xs,point)]
 return S.expand(2*a*a+xs[0]**2/2+(residual-2*a)*xs[0]+xs[1]**2/2+(residual+2*a)*xs[1]+(variable-g)*a)

def section(v,h,g):
 queries=[v,v-h,v+h]
 knots={-sigma,sigma}
 for a in queries:
  for p in [4*a-g,4*a-g-2,-4*a-g,-4*a-g-2]:
   if -sigma<p<sigma:knots.add(p)
 knots=sorted(knots)
 pieces=[]
 for left,right in zip(knots,knots[1:]):
  mid=(left+right)/2
  qs=[val(a,g,z,mid) for a in queries]
  conditions=[qs[0]-qs[1]<=h*h,qs[0]-qs[2]<=h*h,z>=left,z<=right]
  pieces.append(S.reduce_inequalities(conditions,z).as_set())
 return S.Union(*pieces)

def components(region):
 if region is S.EmptySet:return []
 return list(region.args) if isinstance(region,S.Union) else [region]

sections=0;discrepancies=0;max_components=0
for h in [R(3,8),R(3,16),R(3,32)]:
 for v in [R(-3,8),R(0),R(3,16)]:
  for g in [R(-1,2),R(0),R(1,3)]:
   region=section(v,h,g)
   parts=components(region)
   # FiniteSet may contain multiple isolated components; count points separately.
   count=sum(len(part) if isinstance(part,S.FiniteSet) else 1 for part in parts)
   length=sum(part.measure for part in parts)
   continuous=S.simplify(length/(2*sigma))
   assert count<=(2*(2*1+1)*2**4+1)*(8*1+2)
   max_components=max(max_components,count)
   for N in [8,32,128]:
    grid=[-sigma+2*sigma*i/(N-1) for i in range(N)]
    observed=0
    for point in grid:
     q0=val(v,g,point);q1=val(v-h,g,point);q2=val(v+h,g,point)
     event=bool(q0<=q1+h*h and q0<=q2+h*h)
     assert event==bool(region.contains(point))
     observed+=int(event)
    error=S.Abs(R(observed,N)-continuous)
    assert bool(error<=R(2*count,N))
    discrepancies+=1
   sections+=1
print('PASS:',sections,'exact local-event line sections;',discrepancies,'finite-grid discrepancies; maximum actual components',max_components)

# Exact polygon areas for residual-dependent intervals after oblique projection.
# T=(1/2,-1/2), eta=(gamma1+gamma2)/2, d=gamma1-gamma2.
def clip(poly,normal,bound):
 if not poly:return []
 result=[]
 for x,y in zip(poly,poly[1:]+poly[:1]):
  sx=sum(a*b for a,b in zip(normal,x))-bound
  sy=sum(a*b for a,b in zip(normal,y))-bound
  if sx<=0:result.append(x)
  if (sx<0<sy) or (sy<0<sx):
   fraction=sx/(sx-sy)
   result.append(tuple(a+fraction*(b-a) for a,b in zip(x,y)))
 return result

areas=0
for beta,L,offset in product([R(-3),R(0),R(2)],[R(1,8),R(1,2),R(2)],[R(-1,4),R(0),R(1,4)]):
 normal=(1-beta/2,-1-beta/2)
 poly=[(-sigma,-sigma),(sigma,-sigma),(sigma,sigma),(-sigma,sigma)]
 poly=clip(poly,normal,offset+L)
 poly=clip(poly,tuple(-z for z in normal),-offset)
 area=abs(sum(x[0]*y[1]-x[1]*y[0] for x,y in zip(poly,poly[1:]+poly[:1])))/2 if poly else R(0)
 probability=area/(2*sigma)**2
 # The exact complementary-minor sum is |1/2|+|-1/2|=1.
 assert probability<=L/(2*sigma)
 areas+=1
print('PASS:',areas,'exact oblique fiber-volume probabilities with residual-dependent intervals')
