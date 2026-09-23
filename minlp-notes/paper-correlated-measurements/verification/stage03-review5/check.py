from itertools import combinations, product
import sympy as s
R=s.Rational
checks=0

def psd(a):
    return all(a.extract(ix,ix).det()>=0 for k in range(1,a.rows+1) for ix in combinations(range(a.rows),k))

# Independent, exact normalization trials for rank-one and tied rank-two atoms.
p=2
vectors=[s.Matrix(v) for v in [(1,0),(0,1),(1,1),(1,-1),(1,R(1,1024)),(0,0)]]
factors=[[(R(1,2**20),vectors[0])],[(R(2**20),vectors[1])],[(R(3,7),vectors[2]),(R(2,9),vectors[3])],[(R(1),vectors[4])],[],[(R(5,3),vectors[0])]]
atoms=[sum((w*v*v.T for w,v in fs),s.zeros(p)) for fs in factors]
prior=s.zeros(p)
labels=[(i,w,v) for i,fs in enumerate(factors) for w,v in fs]
eta=R(1,3);N=3
covered=set(); objects=[ix for k in (1,2,3) for ix in combinations(range(len(atoms)),k)]
for rank in (1,2):
 for chosen in combinations(labels,rank):
    V=s.Matrix.hstack(*(v for _,w,v in chosen))
    if V.rank()!=rank: continue
    L=(V.T*V).inv()*V.T
    tau=[]
    for _,w,v in chosen:
      t=R(1)
      while t*t*w<1:t*=2
      while t*t*w>=4:t/=2
      tau.append(t)
    T=s.diag(*tau)*L; K=V*s.diag(*(1/t for t in tau)); Pi=V*L
    forced={i for i,w,v in chosen}
    normalized=[T*a*T.T for a in atoms]
    eligible={i for i,(a,b) in enumerate(zip(atoms,normalized)) if Pi*a==a and all(b[j,j]<=4*p for j in range(rank))}
    h=eta/(rank*N); profiles={}
    for obj in objects:
      if not forced<=set(obj)<=eligible:continue
      AA=sum((normalized[i] for i in obj),s.zeros(rank))
      assert psd(AA-s.eye(rank))
      prof=tuple(sum(s.floor(normalized[e][i,j]/h) for e in obj) for i in range(rank) for j in range(i,rank))
      profiles.setdefault(prof,[]).append((obj,AA))
      covered.add(obj)
    for group in profiles.values():
      rep=group[0][1]
      for obj,A in group:
        assert psd(rep-(1-eta)*A) and psd((1+eta)*A-rep)
        assert K*A*K.T==sum((atoms[i] for i in obj),s.zeros(p))
        checks+=1
assert all(obj in covered or sum((atoms[i] for i in obj),s.zeros(p))==s.zeros(p) for obj in objects)

# Exact determinant profile polynomial, interpolation, and deletion witness.
A=s.Matrix([[1,0,1,1],[0,1,1,-1]])
w=[(0,2),(1,0),(2,1),(1,1)]; y,z=s.symbols('y z')
def poly(cols):
    C=A[:,cols]
    return s.Poly(s.expand((C*s.diag(*(y**w[e][0]*z**w[e][1] for e in cols))*C.T).det()),y,z)
full=poly(list(range(4)))
direct={}
for B in combinations(range(4),2):
    coef=A[:,B].det()**2
    key=tuple(sum(w[e][j] for e in B) for j in range(2))
    direct[key]=direct.get(key,0)+coef
assert full.as_dict()=={k:v for k,v in direct.items() if v}
D=4
V=s.Matrix([[s.Integer(x)**i for i in range(D+1)] for x in range(1,D+2)])
vals=s.Matrix([[full.eval({y:i,z:j}) for j in range(1,D+2)] for i in range(1,D+2)])
coefs=V.inv()*vals*(V.T).inv()
assert all(coefs[i,j]==full.coeff_monomial(y**i*z**j) for i in range(D+1) for j in range(D+1))
for target in full.monoms():
    cols=list(range(4))
    for e in range(4):
      rest=[j for j in cols if j!=e]
      if poly(rest).coeff_monomial(y**target[0]*z**target[1])>0: cols=rest
    assert len(cols)==2 and A[:,cols].det()!=0
    assert tuple(sum(w[e][j] for e in cols) for j in range(2))==target
    checks+=1

# Cubic reduction witness K_4: every subset size >=2 is non-independent.
Adj=s.ones(4)-s.eye(4); C=s.eye(4)+Adj/12
for k in range(1,5):
 for ix in combinations(range(4),k):
    one=s.ones(k,1); value=(one.T*C.extract(ix,ix).inv()*one)[0]
    assert value==k if k==1 else value<=k-R(1,9)
    checks+=1

# Exact graph feasibility counters against exhaustive selection, L=0 included.
for n,k,g,L in product(range(1,6),range(6),range(1,8),range(3)):
    gg=min(g,n+1); states={(0,0,0)}
    for t in range(n):
      new=set()
      for count,c,hist in states:
        mask=(hist<<1)&((1<<L)-1)
        new.add((count,max(0,c-1),mask))
        if c==0 and count<k:new.add((count+1,gg-1,mask|int(L>0)))
      states=new
    reachable=any(count==k for count,c,h in states)
    expected=any(all(b-a>=g for a,b in zip(obj,obj[1:])) for obj in combinations(range(n),k))
    assert reachable==expected
    checks+=1
print(f'PASS: {checks} exact normalization/profile/feasibility cases; all feasible positive-rank objects covered.')
