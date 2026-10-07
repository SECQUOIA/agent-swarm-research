from itertools import combinations
from functools import reduce
import sympy as S
R=S.Rational

def vertices(M,d,E,f):
 n=M.cols
 rows=[E[i,:] for i in range(E.rows)]+[M[i,:] for i in range(M.rows)]
 rhs=list(f)+list(d)
 out={}
 for inds in combinations(range(len(rows)),n):
  B=S.Matrix.vstack(*(rows[i] for i in inds))
  if B.det()==0: continue
  x=B.inv()*S.Matrix([rhs[i] for i in inds])
  if E*x!=f or any(z>0 for z in M*x-d):continue
  out[tuple(x)]=x
 return list(out.values())

def basis(rows,n):
 if not rows:return S.zeros(0,n)
 mat=S.Matrix.vstack(*rows)
 piv=mat.T.rref()[1]
 return S.Matrix.vstack(*(mat[i,:] for i in piv)) if piv else S.zeros(0,n)

def nullint(E,n):
 cols=[]
 for z in E.nullspace():
  den=S.ilcm(*[v.q for v in z]) if n>1 else z[0].q
  cols.append(z*den)
 return S.Matrix.hstack(*cols) if cols else S.zeros(n,0)

def value(A,b,c,x):return (x.T*A*x)[0]/2+(b.T*x)[0]+c

def check(name,A,b,c,M,d,integer,makepoint,optimum):
 n=A.rows
 D=S.ilcm(*[S.denom(v) for mat in [A,b,S.Matrix([c]),M,d] for v in mat])
 Ab,bb,Mb,db=D*A,D*b,D*M,D*d
 C=max([S.Integer(1)]+[abs(v) for mat in [Ab,Mb] for v in mat])
 Z0=(n*C)**n; B0=n*C*Z0; H=(n*B0)**n
 tau=1/(4*max(1,M.rows)*H); delta=tau/(2*n*C)
 s,y=makepoint(delta)
 assert sum(v*v for v in y-s)<=delta**2
 assert all(v<=0 for v in M*y-d)
 assert value(A,b,c,s)==optimum
 assert all(y[i]==s[i] and y[i].q==1 for i in integer)
 active=[i for i in range(M.rows) if (Mb*s)[i]==db[i]]
 selected=[i for i in range(M.rows) if db[i]-(Mb*y)[i]<=tau]
 assert set(active)<=set(selected)
 units=[S.eye(n)[i,:] for i in integer]
 E=basis([Mb[i,:] for i in active]+units,n)
 Z=nullint(E,n)
 assert all(abs(v)<=Z0 for v in Z)
 Eq=E.col_join(Z.T*Ab); rhs=(E*s).col_join(-Z.T*bb)
 vs=vertices(Mb,db,Eq,rhs)
 assert vs
 extra=[i for i in selected if i not in active]
 qs=[]
 for x in vs:
  den=S.ilcm(*[v.q for v in x]) if n>1 else x[0].q
  assert den<=H
  assert value(A,b,c,x)==optimum
  q=sum(db[i]-(Mb*x)[i] for i in extra)
  assert q==0 or q>=1/H
  qs.append(q)
 assert min(qs)==0
 selectedrows=[Mb[i,:] for i in selected]+units
 Er=basis(selectedrows,n)
 Zr=nullint(Er,n)
 selectedrhs=S.Matrix([db[i] for i in selected]+[y[i] for i in integer]) if selected or integer else S.zeros(0,1)
 Eall=S.Matrix.vstack(*selectedrows) if selectedrows else S.zeros(0,n)
 ER=Eall.col_join(Zr.T*Ab); fr=selectedrhs.col_join(-Zr.T*bb)
 returned=vertices(Mb,db,ER,fr)
 assert returned
 for x in returned:
  assert value(A,b,c,x)==optimum
 midpoint=sum(returned,S.zeros(n,1))/len(returned)
 assert value(A,b,c,midpoint)==optimum
 return len(vs),len(returned),len(extra)

box=S.Matrix([[-1,0],[0,-1],[1,0],[0,1]])
one=S.Matrix([0,0,1,1])
A=2*S.Matrix([[1,-1],[-1,1]]); b=S.zeros(2,1)
cases=[]
# Redundant nonzero and identically tight rows; both lower constraints extra.
Mr=box.col_join(S.Matrix([[2,0],[0,0]])); dr=one.col_join(S.Matrix([2,0]))
cases.append(('redundant diagonal',A,b,0,Mr,dr,[],lambda e:(S.Matrix([e/4,e/4]),S.Matrix([e/2,e/4])),R(0)))
cases.append(('interior flat segment',A,b,0,box,one,[],lambda e:(S.Matrix([R(1,2),R(1,2)]),S.Matrix([R(1,2)+e/4,R(1,2)])),R(0)))
triangle=S.Matrix([[-1,0],[0,-1],[1,1]])
cases.append(('extra coupled facet',A,b,0,triangle,S.Matrix([0,0,1]),[],lambda e:(S.Matrix([R(1,2)-e/8,R(1,2)-e/8]),S.Matrix([R(1,2),R(1,2)-e/8])),R(0)))
line=box.col_join(S.Matrix([[1,1],[-1,-1]])); dl=one.col_join(S.Matrix([1,-1]))
cases.append(('lower-dimensional line',A,b,0,line,dl,[],lambda e:(S.Matrix([R(1,2),R(1,2)]),S.Matrix([R(1,2)+e/4,R(1,2)-e/4])),R(0)))
cases.append(('disconnected optimal edges',S.diag(-2,0),S.Matrix([1,0]),0,box,one,[],lambda e:(S.Matrix([1,R(1,2)]),S.Matrix([1-e/4,R(1,2)])),R(0)))
cases.append(('integer slice extra snap',S.diag(2,0),S.Matrix([-2,0]),1,box,S.Matrix([0,0,2,1]),[0],lambda e:(S.Matrix([1,e/4]),S.Matrix([1,e/2])),R(0)))
Mc=box.col_join(S.Matrix([[1,1]])); dc=S.Matrix([0,0,2,1,R(3,2)])
cases.append(('coupled mixed rational',2*S.eye(2),S.Matrix([-2,R(-2,3)]),R(10,9),Mc,dc,[0],lambda e:(S.Matrix([1,R(1,3)]),S.Matrix([1,R(1,3)+e/4])),R(0)))
# Negative curvature normal to an affine hull is harmless to stationarity recovery.
cases.append(('indefinite normal curvature',S.Matrix([[0,-2],[-2,0]]),S.zeros(2,1),R(1,2),line,dl,[],lambda e:(S.Matrix([R(1,2),R(1,2)]),S.Matrix([R(1,2)+e/4,R(1,2)-e/4])),R(0)))
tot=[0,0,0]
for case in cases:
 r=check(*case)
 tot=[a+b for a,b in zip(tot,r)]
 print('PASS',case[0],r)
print('TOTAL',len(cases),'cases;',tot,'stationary vertices, recovered vertices, extra snaps')
