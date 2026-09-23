"""Independent exact checks of Stage 3; no repository producer imports."""
from itertools import combinations, product
from pathlib import Path
import json
import sympy as s

R = s.Rational
counts = {}

def psd(M):
    return M == M.T and all(M.extract(I, I).det() >= 0
        for r in range(1, M.rows + 1) for I in combinations(range(M.rows), r))

def bases(A):
    q = A.rows
    return [I for I in combinations(range(A.cols), q) if A[:, I].det() != 0]

def profile_polynomial(A, w):
    y = s.symbols('y:2')
    M = s.zeros(A.rows)
    for e in range(A.cols):
        M += (y[0]**w[e][0] * y[1]**w[e][1]) * A[:, e] * A[:, e].T
    return s.Poly(M.det(method='domain-ge'), *y)

# Separate tensor interpolation from direct symbolic determinants.
def interpolate(A, w):
    q = A.rows
    D = q * max(max(x) for x in w)
    grid = list(range(1, D + 2))
    V = s.Matrix([[x**i for i in range(D + 1)] for x in grid])
    values = s.zeros(D + 1)
    for i, j in product(range(D + 1), repeat=2):
        M = s.zeros(q)
        for e in range(A.cols):
            M += grid[i]**w[e][0] * grid[j]**w[e][1] * A[:, e] * A[:, e].T
        values[i, j] = M.det()
    coeff = V.inv() * values * V.inv().T
    return {(i, j): coeff[i, j] for i, j in product(range(D+1), repeat=2) if coeff[i,j]}

fixtures = [
    s.Matrix([[1, 0, 1, 2, 0], [0, 1, 1, -1, 0]]),
    s.Matrix([[1,0,0,1,R(1,3),0], [0,1,0,-1,R(2,7),0], [0,0,1,1,R(1,11),0]]),
    s.Matrix.hstack(s.eye(4), s.ones(4,1), s.Matrix([1,-1,1,-1])),
]
total_profiles = total_bases = total_deletions = 0
for A in fixtures:
    q, m = A.shape
    original_bases = bases(A)
    total_bases += len(original_bases)
    w = [(e % 2, (e // 2) % 2) for e in range(m)]
    poly = profile_polynomial(A, w)
    explicit = {}
    for B in original_bases:
        u = tuple(sum(w[e][i] for e in B) for i in range(2))
        explicit[u] = explicit.get(u, 0) + A[:,B].det()**2
    assert dict(poly.terms()) == explicit == interpolate(A,w)
    total_profiles += len(explicit)
    for u in explicit:
        keep = list(range(m))
        for e in range(m):
            trial = [j for j in keep if j != e]
            # Retain q rows if trial loses rank, as the manuscript requires.
            cp = profile_polynomial(A[:,trial], [w[j] for j in trial])
            if cp.coeff_monomial(u) > 0:
                keep = trial
            total_deletions += 1
        assert tuple(keep) in original_bases
        assert tuple(sum(w[e][i] for e in keep) for i in range(2)) == u
    for B in original_bases:
        for nf in range(q+1):
            F = B[:nf]
            D = A[:,B]
            optional = [e for e in range(m) if e not in F]
            Ac = (D.inv() * A)[nf:,optional]
            assert Ac.rank() == q-nf
            for C in combinations(range(len(optional)), q-nf):
                lifted = tuple(sorted(F + tuple(optional[j] for j in C)))
                assert (Ac[:,C].det() != 0) == (lifted in original_bases)
counts.update(profile_fixtures=len(fixtures), exact_profiles=total_profiles,
              enumerated_bases=total_bases, deletion_tests=total_deletions)

# Singular oblique PSD atoms with multiple factors per owner and a prior.
U = s.Matrix([[1,0],[-2,R(1,2**40)],[3,-R(1,2**40)]])
factors = [
    [(R(1,2**60),U[:,0]), (R(3,2),U[:,1])],
    [(R(4,3),U*s.Matrix([1,-1]))],
    [(R(1,7),U*s.Matrix([1,2])), (R(5,11),U*s.Matrix([2,1]))],
    [(R(2**30),U*s.Matrix([0,1]))],
]
prior_factors = [(R(1,13), U[:,0])]
atoms = [sum((w*v*v.T for w,v in ff), s.zeros(3)) for ff in factors]
prior = sum((w*v*v.T for w,v in prior_factors), s.zeros(3))
normalizations=0
for B in combinations(range(4), 2):
    labels = [(None,w,v) for w,v in prior_factors]
    labels += [(e,w,v) for e in B for w,v in factors[e]]
    def volume(C):
        V = s.Matrix.hstack(*(labels[j][2] for j in C))
        return (V.T*V).det() * s.prod(labels[j][1] for j in C)
    C = max(combinations(range(len(labels)),2), key=volume)
    assert volume(C)>0
    V = s.Matrix.hstack(*(labels[j][2] for j in C))
    L = (V.T*V).inv()*V.T
    tau=[]
    for j in C:
        w=labels[j][1]; t=s.Integer(1)
        while t*t*w<1:t*=2
        while t*t*w>=4:t/=2
        tau.append(t)
    T=s.diag(*tau)*L; K=V*s.diag(*(1/t for t in tau)); Pi=V*L
    transformed=[]
    for Q in [prior]+[atoms[e] for e in B]:
        assert Pi*Q==Q
        Aq=T*Q*T.T
        assert all(Aq[i,i]<=12 for i in range(2))
        assert K*Aq*K.T==Q
        transformed.append(Aq)
    J=sum(transformed,s.zeros(2))
    assert psd(J-s.eye(2))
    owners={labels[j][0] for j in C}-{None}
    assert owners.issubset(B) and len(owners)<=2
    normalizations+=1
counts['oblique_singular_normalizations']=normalizations

# Three exact scope counterexamples and rank-drop protection.
assert (s.Matrix([[1,1]])*s.Matrix([[1,-1]]).T).det()==0
assert s.Matrix([[1,1,0],[1,0,1],[0,1,1]]).det()==-2
assert profile_polynomial(s.Matrix([[1,1],[0,0]]),[(0,0),(0,0)]).is_zero
assert profile_polynomial(s.Matrix([[1,1]]),[(0,0),(0,0)]).coeff_monomial((0,0))==2
counts['status']='passed'
Path(__file__).with_name('results.json').write_text(json.dumps(counts,indent=2)+'\n')
print(json.dumps(counts))
