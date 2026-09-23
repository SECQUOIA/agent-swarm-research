"""Independent exact-arithmetic check of Stage 1 factorization and refinement."""
import itertools
import json
import random
import sympy as s
from pathlib import Path
rng = random.Random(20260907)
# Two triangles sharing articulation 2, a parallel pair attached at 4,
# a bridge, a loop, a disconnected edge, and an isolated vertex.
undirected = [(0,1),(1,2),(2,0),(2,3),(3,4),(4,2),(4,5),(4,5),(5,6),(3,3),(7,8)]
blocks = [[0,1,2],[3,4,5],[6,7],[9]]
bridges = [8,10]
weights_cases = [(0,s.Rational(1,3),s.Rational(2,3),0), (1,0,0,0), (s.Rational(1,4),)*4]
checks = 0
for trial in range(36):
    edges = [(v,u) if rng.randrange(2) else (u,v) for u,v in undirected]
    A = s.zeros(10,len(edges))
    for e,(u,v) in enumerate(edges):
        A[u,e] -= 1; A[v,e] += 1
    bases = []
    for block in blocks:
        # Derive each local circulation independently, including loop columns.
        local = A[:,block].nullspace()
        assert len(local) == 1
        c = s.zeros(len(edges),1)
        for i,e in enumerate(block): c[e] = local[0][i]
        assert A*c == s.zeros(10,1)
        bases.append(c)
    assert len(A.nullspace()) == len(bases)
    for g in A.nullspace():
        assert all(g[e] == 0 for e in bridges)
        for block in blocks:
            assert A[:,block]*g[block,0] == s.zeros(10,1)
    base = s.ones(len(edges),1)/2
    b = A*base
    v = base + 3*sum(bases,s.zeros(len(edges),1))
    assert A*v == b and any(t < 0 or t > 1 for t in v)
    states = []
    for k in range(4):
        f = base + sum((s.Rational(rng.randint(-2,2),20)*c for c in bases), s.zeros(len(edges),1))
        assert A*f == b and all(0 <= t <= 1 for t in f)
        states.append(f)
    for weights in weights_cases:
        for labels in [({1,2},{2,3},set(),{1}), (set(),set(),set(),set()), ({1,2,3},)*4]:
            x = sum((weights[k]*states[k] for k in range(4)),s.zeros(len(edges),1))
            refined = [s.zeros(len(edges),1) for _ in range(4)]
            for block,J in zip(blocks,labels):
                missing = set(range(4))-J
                star_weight = sum(weights[k] for k in missing)
                merged = sum((weights[k]*(states[k][block,0]-v[block,0]) for k in missing),s.zeros(len(block),1))
                assert star_weight > 0 or merged == s.zeros(len(block),1)
                local = []
                for k in range(4):
                    h = weights[k]*(states[k][block,0]-v[block,0]) if k in J else (weights[k]*merged/star_weight if star_weight else s.zeros(len(block),1))
                    assert A[:,block]*h == s.zeros(10,1)
                    for i,e in enumerate(block):
                        assert -weights[k]*v[e] <= h[i] <= weights[k]*(1-v[e])
                        refined[k][e] = h[i]
                        if k in J: assert h[i]+weights[k]*v[e] == weights[k]*states[k][e]
                    local.append(h)
                assert sum(local,s.zeros(len(block),1)) == x[block,0]-v[block,0]
            recovered = [weights[k]*v+refined[k] for k in range(4)]
            assert sum(recovered,s.zeros(len(edges),1)) == x
            for k in range(4):
                assert A*recovered[k] == weights[k]*b
                assert all(0 <= t <= weights[k] for t in recovered[k])
                for e in bridges: assert recovered[k][e] == weights[k]*v[e]
            checks += 1
record = {'status':'PASS','exact_refinements':checks,'orientations':36,'arithmetic':'SymPy Rational','features':['articulation blocks','parallel arcs','self-loop','bridges','disconnected components','isolated vertex','infeasible reference bounds','zero residual/explicit/merged weights','different local mergers','unobserved blocks']}
Path(__file__).with_name('result.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
