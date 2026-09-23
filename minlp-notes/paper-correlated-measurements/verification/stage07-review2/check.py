"""Independent final-review rational fixtures; no manuscript/helper imports."""
from itertools import combinations, product
from collections import Counter
from pathlib import Path
import json
import sympy as s
R=s.Rational
stats=Counter()

def psd(A):
    return A==A.T and all(A.extract(ix,ix).det()>=0 for k in range(1,A.rows+1) for ix in combinations(range(A.rows),k))

def factors(A):
    # Independent rank-one peeling in original coordinates.
    out=[]
    while A!=s.zeros(A.rows):
        i=next(i for i in range(A.rows) if A[i,i]>0)
        w=A[i,i];v=A[:,i]/w;out.append((w,v));A=A-w*v*v.T
        assert psd(A)
    return out

def check_cover(atoms, prior, objects, eta):
    p=prior.rows;N=max(1,max(map(len,objects)))
    matrices=[prior+sum((atoms[e] for e in obj),s.zeros(p)) for obj in objects]
    labels=[(owner,w,v) for owner,A in [(-1,prior),*enumerate(atoms)] for w,v in factors(A)]
    covered=set(i for i,A in enumerate(matrices) if A==s.zeros(p))
    for r in range(1,p+1):
      for basis in combinations(labels,r):
        V=s.Matrix.hstack(*(v for _,_,v in basis))
        if V.rank()!=r:continue
        L=(V.T*V).inv()*V.T;Pi=V*L;taus=[]
        for _,w,_ in basis:
          tau=s.Integer(1)
          while tau*tau*w<1:tau*=2
          while tau*tau*w>=4:tau/=2
          taus.append(tau)
        T=s.diag(*taus)*L;K=V*s.diag(*(1/a for a in taus))
        assert T*K==s.eye(r) and K*T==Pi
        def retained(A):return Pi*A==A and all((T*A*T.T)[i,i]<=4*p for i in range(r))
        if not retained(prior):continue
        good={e for e,A in enumerate(atoms) if retained(A)}
        forced={e for e,_,_ in basis if e>=0}
        profiles={};h=eta/(r*N)
        for i,obj in enumerate(objects):
          if not set(obj)<=good or not forced<=set(obj):continue
          B=T*matrices[i]*T.T
          assert psd(B-s.eye(r)) and K*B*K.T==matrices[i]
          profile=tuple(sum(s.floor((T*atoms[e]*T.T)[a,b]/h) for e in obj) for a in range(r) for b in range(a,r))
          if profile in profiles:
              j=profiles[profile];stats['profile_collisions']+=1
          else:profiles[profile]=i;j=i
          assert psd(matrices[j]-(1-eta)*matrices[i])
          assert psd((1+eta)*matrices[i]-matrices[j])
          assert matrices[j].nullspace()==matrices[i].nullspace()
          covered.add(i);stats['normalized_objects']+=1
        stats['normalization_trials']+=1
    assert len(covered)==len(objects)
    stats['covered_targets']+=len(objects)

# Oblique rank-two ranges in three dimensions, enormous scale disparity,
# singular/zero targets, signed entries and multiple labels owned by one atom.
V=s.Matrix([[1,1],[2,0],[-1,R(1,2**85)]])
lift=lambda A:V*A*V.T
atoms=[lift(s.diag(1,0)),lift(s.diag(0,R(1,2**100))),
       lift(s.Matrix([[1,-R(1,2**55)],[-R(1,2**55),R(1,2**100)]])),
       lift(s.Matrix([[R(1001,1000),-R(1,2**55)],[-R(1,2**55),R(1,2**100)]])),s.zeros(3)]
# Every listed object can be made a separate branch of an explicit acyclic graph.
objects=[(),(0,),(1,),(2,),(3,),(4,),(0,1),(0,4),(2,4),(3,4),(0,1,4)]
check_cover(atoms,s.zeros(3),objects,R(3,4))
# Rank-three rational representation with parallel columns and a loop;
# independent forced owners and rejection of rank-losing restrictions.
A=s.Matrix([[1,0,0,1,1,0],[0,1,0,1,0,0],[0,0,1,1,0,0]])
bases=[b for b in combinations(range(6),3) if A[:,b].det()!=0]
atoms2=[s.diag(R(100+i,100),R(1,2**80)) for i in range(6)]
check_cover(atoms2,s.diag(0,R(1,2**81)),bases,R(2,3))
for F in [(),(0,),(0,1),(0,1,2),(0,4)]:
    if A[:,F].rank()!=len(F):stats['dependent_forced_rejections']+=1;continue
    basis=next(b for b in bases if set(F)<=set(b))
    order=list(F)+[e for e in basis if e not in F]
    D=A[:,order];optional=[e for e in range(A.cols) if e not in F]
    Ac=(D.inv()*A[:,optional])[len(F):,:];qp=3-len(F)
    for C in combinations(optional,qp):
        contracted=Ac[:,[optional.index(e) for e in C]].det()!=0 if qp else True
        assert contracted==(tuple(sorted(F+C)) in bases)
        stats['contraction_equivalences']+=1

# Tensor interpolation and deletion with the original row count retained.
# Polynomial coordinates are independent of spectral rounding in this fixture.
M=s.Matrix([[1,0,1,2,0],[0,1,1,2,0]])
weights=[(0,1),(1,0),(1,1),(1,1),(0,0)]
D=4;Vd=s.Matrix([[x**j for j in range(D+1)] for x in range(1,D+2)]);Vi=Vd.inv()
def coefficients(cols):
    values=s.zeros(D+1)
    for x,y in product(range(1,D+2),repeat=2):
        B=sum((M[:,e]*M[:,e].T*x**weights[e][0]*y**weights[e][1] for e in cols),s.zeros(2))
        values[x-1,y-1]=B.det()
    coeff=Vi*values*Vi.T
    assert all(v>=0 and v.q==1 for v in coeff)
    stats['interpolation_runs']+=1
    return {(i,j):coeff[i,j] for i,j in product(range(D+1),repeat=2) if coeff[i,j]}
expected=Counter()
for C in combinations(range(5),2):
    expected[tuple(sum(weights[e][j] for e in C) for j in range(2))]+=M[:,C].det()**2
expected={k:v for k,v in expected.items() if v}
assert coefficients(range(5))==expected
assert coefficients([0,2,3])=={(1,2):s.Integer(5)}
assert coefficients([2,3])=={} # dependent columns, still two original rows
for profile in expected:
    remaining=list(range(5))
    for e in range(5):
        test=[j for j in remaining if j!=e]
        if profile in coefficients(test):remaining=test
    assert len(remaining)==2 and M[:,remaining].det()!=0
    assert tuple(sum(weights[e][j] for e in remaining) for j in range(2))==profile
    stats['profile_witnesses_recovered']+=1
report={'status':'passed','checks':dict(stats),'scope':'Independent exact finite fixtures, not general proof or production algorithm benchmark'}
(Path(__file__).parent/'results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
