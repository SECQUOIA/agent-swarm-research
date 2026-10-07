from itertools import combinations
import sympy as S
R=S.Rational
a=S.Symbol('a')

def original_min(A,b,M,d,tilt):
 n=A.rows; best=None
 for count in range(n+1):
  for J in combinations(range(M.rows),count):
   E=M[list(J),:] if J else S.zeros(0,n)
   e=d[list(J),:] if J else S.zeros(0,1)
   K=A.row_join(E.T).col_join(E.row_join(S.zeros(count,count)))
   if K.det()==0:continue
   x=(K.inv()*(-b-tilt).col_join(e))[:n,0]
   if any(z>0 for z in M*x-d):continue
   val=(x.T*A*x)[0]/2+((b+tilt).T*x)[0]
   if best is None or val<best[0]:best=(val,x)
 assert best is not None
 return best

def prepare(A,b,M,d,T,alpha):
 n=A.rows;P=A+alpha*T.T*T;out=[]
 assert P.is_positive_semidefinite
 assert all(T*z==S.zeros(1,1) for z in P.nullspace())
 D=S.ilcm(*[S.denom(v) for mat in [P,M,b,d,alpha*T.T] for v in mat])
 C0=max([S.Integer(1)]+[abs(D*v) for mat in [P,M,b,d,alpha*T.T] for v in mat])
 U=S.factorial(2*n)*C0**(2*n)
 H0=alpha*(1+n*U)
 for count in range(n+1):
  for J in combinations(range(M.rows),count):
   E=M[list(J),:] if J else S.zeros(0,n)
   e=d[list(J),:] if J else S.zeros(0,1)
   K=P.row_join(E.T).col_join(E.row_join(S.zeros(count,count)))
   if K.det()==0:continue
   sol=K.inv()*(-b+alpha*T.T*a).col_join(e)
   x=sol[:n,0];lam=sol[n:,0]
   assert all(abs(z.subs(a,0))<=U and abs(S.diff(z,a))<=U for z in x)
   rows=[S.expand(z) for z in M*x-d]+[-S.expand(z) for z in lam]
   q=S.expand((x.T*A*x)[0]/2+(b.T*x)[0]+alpha*(a-(T*x)[0])**2/2)
   assert S.expand(S.diff(q,a)-alpha*(a-(T*x)[0]))==0
   assert abs(S.diff(q,a,2))<=H0
   out.append((J,x,rows,q,S.diff(q,a,2),S.diff(q,a).subs(a,0)))
 return out

def feasible(piece,v):return all(z.subs(a,v)<=0 for z in piece[2])
def oracle(pieces,v):
 valid=[p for p in pieces if feasible(p,v)]
 assert valid
 vals={p[3].subs(a,v) for p in valid}
 grads={S.diff(p[3],a).subs(a,v) for p in valid}
 assert len(vals)==len(grads)==1
 return vals.pop(),valid[0]

def check(name,A,b,M,d,T,alpha,bounds,noises,expected_residual=None):
 pieces=prepare(A,b,M,d,T,alpha)
 H=max(abs(p[4]) for p in pieces)
 bad=set()
 for _,_,rows,q,h,p in pieces:
  if h==0:bad.add(-p)
  else:
   for row in rows:
    slope=S.diff(row,a)
    if slope:bad.add(S.simplify(-h*(-row.subs(a,0)/slope)-p))
 counts=[0,0,0]
 for noise in noises:
  fstar,_=original_min(A,b,M,d,T.T*noise)
  star=fstar-noise**2/(2*alpha)
  cells=[bounds];U=None
  for level in range(6):
   h=(bounds[1]-bounds[0])/2**level;B=alpha*h*h/8
   pending=[]
   for left,right in cells:
    corner=[];selected=[]
    for v in (left,right):
     w,p=oracle(pieces,v)
     direct,_=original_min(A+alpha*T.T*T,b,M,d,-alpha*T.T*v)
     assert w==direct+alpha*v*v/2
     val=w+noise*v
     U=val if U is None else min(U,val)
     corner.append(val);selected.append(p);counts[0]+=1
    covering=[p for p in selected if feasible(p,left) and feasible(p,right)]
    if covering:
     p=covering[0];q=p[3]+noise*a
     candidates=[left,right]
     if p[4]!=0:
      stationary=-(p[5]+noise)/p[4]
      if left<=stationary<=right:candidates.append(stationary)
     v=min(candidates,key=lambda z:q.subs(a,z));val=q.subs(a,v)
     assert feasible(p,v)
     w,_=oracle(pieces,v)
     assert val==w+noise*v
     U=min(U,val);counts[1]+=1
    else:pending.append((left,right,min(corner)-B,min(corner)))
   kept=[v for v in pending if v[2]<=U]
   assert U>=star and U-star<=B
   for left,right,lb,corner in kept:
    assert corner-star<=2*B
    assert min(abs(noise-z) for z in bad)<=(alpha+H)*h
    counts[2]+=1
   if not kept:
    assert U==star
    break
   cells=[part for l,r,_,_ in kept for part in [(l,(l+r)/2),((l+r)/2,r)]]
  if noise==expected_residual:
   assert kept, "The literal noise atom should exercise unresolved-cell fallback"
  # Exact same-draw fallback independently supplies the already checked fstar.
 print('PASS',name,'basis count',len(pieces),'bad points',len(bad),'query/closure/retained',counts)
 return pieces,counts

M=S.Matrix([[-1,0],[1,0],[0,-1],[0,1]])
# Flat inner residual coordinate, with P singular but ker(P) subset ker(T).
p1,c1=check('flat residual',S.diag(-1,0),S.Matrix([R(1,3),0]),M,S.ones(4,1),S.Matrix([[1,0]]),R(2),(R(-5,4),R(5,4)),[R(-1,3),R(0),R(1,3)])
# F=xy has a lower-dimensional critical region at a=0 and singular pieces.
d=S.Matrix([0,1,0,2])
p2,c2=check('lower-dimensional critical region',S.Matrix([[0,1],[1,0]]),S.zeros(2,1),M,d,S.Matrix([[R(1,2),R(-1,2)]]),R(4),(R(-9,8),R(5,8)),[R(-1,3),R(0),R(1,3)])
point_regions=[p for p in p2 if feasible(p,R(0)) and not feasible(p,R(1,100)) and not feasible(p,R(-1,100))]
assert point_regions and any(p[4]==0 for p in p2)
# An affine feasible set with duplicate equality rows.
Me=M.col_join(S.Matrix([[1,-1],[-1,1],[2,-2]]));de=S.ones(4,1).col_join(S.zeros(3,1))
p3,c3=check('lower-dimensional original polytope',S.Matrix([[0,-1],[-1,0]]),S.zeros(2,1),Me,de,S.Matrix([[R(1,2),R(1,2)]]),R(4),(R(-9,8),R(9,8)),[R(-1,3),R(0),R(1,3)])
# Dropping the kernel hypothesis permits W=a^2/2-|a|, not C1.
assert S.diff(a*a/2-a,a).subs(a,0)!=S.diff(a*a/2+a,a).subs(a,0)
print('PASS: lower-dimensional piece and kernel-hypothesis counterexample checks')

T=S.Matrix([[R(1,2),R(-1,2)]])
p4,c4=check('literal endpoint atom requiring fallback',S.Matrix([[0,1],[1,0]]),-T.T,M,S.Matrix([0,1,0,1]),T,R(4),(R(-3,4),R(3,4)),[R(1)],expected_residual=R(1))
print('TOTAL:',sum(c[0] for c in [c1,c2,c3,c4]),'corner queries;',sum(c[1] for c in [c1,c2,c3,c4]),'closed cells;',sum(c[2] for c in [c1,c2,c3,c4]),'retained unresolved cells')

# Atomic term is indispensable, including for a literal endpoint in an even grid.
grid=[R(-1),R(-1,3),R(1,3),R(1)]
eta=R(1,1000)
for point in [R(-1),R(-1,3),R(0),R(1,3),R(1)]:
 probability=R(sum(int(bool(abs(z-point)<=eta)) for z in grid),len(grid))
 assert probability<=eta+R(1,len(grid))
assert R(1,len(grid))>eta
print('PASS: Cramer coefficient/curvature bounds and finite-grid hyperplane atom term')
