"""Independent small exact exercise of the written normalization/profile algorithm."""
import itertools
import json
from pathlib import Path
import sympy as s

Z = s.zeros(2)

def psd(a):
    return a == a.T and all(a.extract(ix, ix).det() >= 0
                           for r in range(1, a.rows + 1)
                           for ix in itertools.combinations(range(a.rows), r))

def factors(a):
    rem = a.copy()
    ans = []
    while rem != s.zeros(a.rows):
        i = next(i for i in range(a.rows) if rem[i, i] > 0)
        w = rem[i, i]
        v = rem[:, i] / w
        ans.append((w, v))
        rem -= w * v * v.T
        assert psd(rem)
    return ans

def exercise(name, edges, prior, vertices=4, eta=s.Rational(4,5)):
    # Edge tuple is (source, destination, information). Distinct parallel edges permitted.
    n = vertices - 1
    paths = [[] for _ in range(vertices)]
    paths[0] = [()]
    for u in range(vertices):
        for i, (a,b,q) in enumerate(edges):
            if a == u:
                paths[b] += [p+(i,) for p in paths[u]]
    targets = paths[-1]
    matrices = {p: prior + sum((edges[i][2] for i in p), Z) for p in targets}
    labels = [(owner,w,v) for owner,q in [(-1,prior)]+[(i,e[2]) for i,e in enumerate(edges)]
              for w,v in factors(q)]
    returned = set()
    surviving = {p:0 for p in targets if matrices[p].rank() > 0}
    counts = dict(trials=0, accepted_trials=0, merges=0, owner_floor_checks=0)
    for rank in (1,2):
        for inds in itertools.combinations(range(len(labels)),rank):
            chosen = [labels[i] for i in inds]
            v = s.Matrix.hstack(*(x[2] for x in chosen))
            if v.rank() != rank:
                continue
            counts['trials'] += 1
            left = (v.T*v).inv()*v.T
            proj = v*left
            tau = []
            for owner,w,col in chosen:
                d=s.Integer(1)
                while d*d*w < 1: d *= 2
                while d*d*w >= 4: d /= 2
                tau.append(d)
            t=s.diag(*tau)*left
            k=v*s.diag(*(1/x for x in tau))
            assert t*k == s.eye(rank)
            if proj*prior != prior: continue
            a0=t*prior*t.T
            if any(a0[i,i]>8 for i in range(rank)): continue
            atoms={i:t*q*t.T for i,(_,_,q) in enumerate(edges)
                   if proj*q==q and all((t*q*t.T)[j,j]<=8 for j in range(rank))}
            for i,a in atoms.items():
                assert k*a*k.T == edges[i][2]
                assert max(abs(x) for x in a)<=8
            forced=set(owner for owner,_,_ in chosen if owner>=0)
            valid=[p for p in targets if set(p)<=set(atoms) and forced<=set(p)]
            if not valid: continue
            counts['accepted_trials']+=1
            for p in valid:
                aa=a0+sum((atoms[i] for i in p),s.zeros(rank))
                assert psd(aa-s.eye(rank))
                assert matrices[p].rank()==rank
                surviving[p]+=1
                counts['owner_floor_checks']+=1
            h=eta/(rank*n)
            coords=list(itertools.combinations_with_replacement(range(rank),2))
            profiles={i:tuple(s.floor(a[j,l]/h) for j,l in coords) for i,a in atoms.items()}
            state=[{} for _ in range(vertices)]
            state[0][(frozenset(),(0,)*len(coords))]=()
            for u in range(vertices):
                for i,(a,b,q) in enumerate(edges):
                    if a!=u or i not in atoms: continue
                    for (mask,z),p in list(state[u].items()):
                        key=(mask|({i} if i in forced else set()),tuple(x+y for x,y in zip(z,profiles[i])))
                        if key in state[b]: counts['merges']+=1
                        state[b][key]=p+(i,)
            returned.update(p for (mask,z),p in state[-1].items() if mask==forced)
    if prior == Z:
        zeros=[p for p in targets if matrices[p]==Z]
        if zeros: returned.add(zeros[0])
    assert all(surviving.values())
    for p in targets:
        matches=[q for q in returned if psd(matrices[q]-(1-eta)*matrices[p])
                 and psd((1+eta)*matrices[p]-matrices[q])]
        assert matches, p
        assert all(matrices[p].nullspace()==matrices[q].nullspace() for q in matches)
    return dict(name=name,paths=len(targets),returned=len(returned),**counts)

v=s.Matrix([1,-1]); close=s.Matrix([1,s.Rational(-9999,10000)])
a=v*v.T; b=close*close.T
small=s.diag(s.Rational(1,2**80),s.Rational(1,2**120))
edges=[(0,1,a),(0,1,b),(0,1,Z),(1,2,s.diag(1,0)),
       (1,2,s.diag(s.Rational(10001,10000),0)),(1,2,Z),
       (2,3,small),(2,3,Z),(0,3,a),(0,3,Z)]
results=[exercise('singular_zero_close_ranges_and_ill_conditioned',edges,Z),
         exercise('rank_one_common_prior',edges,a),
         exercise('positive_definite_prior',edges,small)]
# Counterexample to deleting dominated representatives in a two-sided cover.
assert not psd(s.eye(2)*s.Rational(6,5)-s.eye(2)*2)
# Worst endpoint rational check for the local-to-true claimed bound.
x=s.symbols('x',positive=True)
excess=((1+x/4)*(1+x/8)/(1-x/8)-1)
assert s.simplify(s.Rational(17,28)*x-excess-6*x*(1-x)/(7*(8-x))) == 0
out=Path(__file__).with_name('results.json')
out.write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
