"""Compare forced-affine recognition with the complete LP fallback."""
from fractions import Fraction as F
from random import Random
from unittest.mock import patch
from check_affine_pipeline import problem
from recourse import recognize_affine
from verify_recourse import verify_selector


def run():
    rng=Random(936247)
    cases=[]
    # Singular full Hessian, positive central multiplier in coordinate1,
    # nonsingular zero-gradient face in coordinate2; selector (0,z).
    cases.append(problem([[0,-2,-2],[-2,2,2],[-2,2,2]], [0,1,0], [(0,1)]*3))
    # An identically zero-curvature coordinate fixed by a nonzero multiplier.
    cases.append(problem([[0,0,-2],[0,0,0],[-2,0,2]], [0,1,0], [(0,1)]*3))
    # Zero multiplier at a central bound must remain a zero-gradient row.
    cases.append(problem([[0,-2,0],[-2,2,0],[0,0,2]], [0,0,1], [(-1,1),(0,1),(0,1)]))
    for case in range(60):
        rank=case%3
        vectors=[[F(rng.randrange(-2,3)) for _ in range(2)] for _ in range(rank)]
        C=[[sum((v[i]*v[j] for v in vectors),F(0)) for j in range(2)] for i in range(2)]
        D=[F(rng.randrange(-4,5)) for _ in range(2)]
        b=[F(rng.randrange(-4,5)) for _ in range(2)]
        A=[[F(-1),D[0],D[1]],[D[0],C[0][0],C[0][1]],[D[1],C[1][0],C[1][1]]]
        cases.append(problem(A,[0]+b,[(-1,1),(0,1),(0,1)]))
    forced=0
    for i,p in enumerate(cases):
        result=recognize_affine(p,[1,2])
        with patch('rational_optimization.solve_nonsingular',return_value=None):
            fallback=recognize_affine(p,[1,2])
        assert result['status']==fallback['status'], (i,result,fallback)
        assert result['status']!='resource_limit'
        if result.get('recognition')=='nonsingular_pattern':
            forced+=1
        if result['status']=='affine':
            verify_selector(p,result['proof'])
            verify_selector(p,fallback['proof'])
    assert forced > 0
    print({'fastpath_vs_complete_lp':len(cases),'forced_patterns_exercised':forced})

if __name__=='__main__':
    run()
