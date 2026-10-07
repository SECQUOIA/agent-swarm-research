from itertools import combinations, product
import sympy as S
R=S.Rational

def qp(Q,b,c,cons):
    n=Q.rows; best=None
    for k in range(n+1):
      for inds in combinations(range(len(cons)),k):
        G=S.Matrix.vstack(*(cons[i][0] for i in inds)) if k else S.zeros(0,n)
        rhs=S.Matrix([cons[i][1] for i in inds]) if k else S.zeros(0,1)
        K=Q.row_join(G.T).col_join(G.row_join(S.zeros(k,k)))
        if K.det()==0: continue
        sol=K.inv()*(-b).col_join(rhs)
        x=sol[:n,0]
        if any((g*x)[0]>a for g,a in cons): continue
        val=(x.T*Q*x)[0]/2+(b.T*x)[0]+c
        if best is None or val<best[0]: best=val,x
    assert best is not None
    return best

A=S.Matrix([[0,2],[2,0]]); T=S.Matrix([[1,-1]]); P=A+T.T*T
b=S.Matrix([1,R(1,3)]); c=R(-1,3); tstar=R(1,3); growth=R(1,2); cons=[(S.Matrix([[1,0]]),R(4,3)),(S.Matrix([[-1,0]]),R(-1,3)),(S.Matrix([[0,1]]),2),(S.Matrix([[0,-1]]),0)]
assert qp(A,b,c,cons)[0]==0
assert A.eigenvals()=={-2:1,2:1}
assert P.eigenvals()=={0:1,2:1}
cells=[(R(-5,3),R(4,3))]; incumbent=None; total=0; retained_counts=[]
for level in range(7):
    solved=[]
    for a,z in cells:
      sliced=cons+[(T,z),(-T,-a)]
      lin=b-(a+z)*T.T/2
      lb,x=qp(P,lin,c+a*z/2,sliced)
      f=(x.T*A*x)[0]/2+(b.T*x)[0]+c
      t=(T*x)[0]; delta=(z-a)**2/8
      assert 0<=f-lb<=delta
      assert f-lb==(t-a)*(z-t)/2
      assert f>=growth*(t-tstar)**2
      if incumbent is None or f<incumbent: incumbent=f
      solved.append((a,z,lb,x,f)); total+=1
    keep=[v for v in solved if v[2]<incumbent]
    mesh=R(3,2**level); delta=mesh*mesh/8
    assert 0<=incumbent<=delta
    assert min([incumbent]+[v[2] for v in keep])<=0<=incumbent
    assert incumbent-min([incumbent]+[v[2] for v in keep])<=delta
    for a,z,lb,x,f in keep:
      assert growth*((T*x)[0]-tstar)**2<2*delta
    retained_counts.append(len(keep))
    cells=[v for a,z,*_ in keep for v in [(a,(a+z)/2),((a+z)/2,z)]]
    if not cells: break

for n in range(2,11):
 A=S.eye(n)-R(2,n)*S.ones(n)
 assert sum(mult for eig,mult in A.eigenvals().items() if eig<0)==1
 for size in range(1,n+1):
  sub=A[:size,:size]
  assert all(v>=0 for v in sub.eigenvals())==(size<=n//2)
for m in (2,3,4):
 n=m*m
 B=2*S.eye(n)+R(2,n)*S.ones(n)
 cross=R(4,m)*S.ones(n,1)
 A=S.Matrix([[2]]).row_join(cross.T).col_join(cross.row_join(B))
 assert A.det()<0
 assert B.is_positive_definite
print('PASS: spectral kink, exact slab branch-and-bound',total,'cells; retained',retained_counts)
print('PASS: inertia/deletion examples n=2..10; dense residual examples m=2,3,4')
