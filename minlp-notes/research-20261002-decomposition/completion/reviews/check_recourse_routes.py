"""Independent wrapper routing, model binding and budget regression checks."""
from copy import deepcopy
from fractions import Fraction as F
from check_affine_pipeline import problem, exact_face_minimum
from recourse import solve_with_recourse
from verify_recourse import verify_pipeline, RecourseCertificateError


def run():
    checked = rejected = 0
    clipped = problem([[0,0,0],[0,6,-4],[0,-4,2]], [2,0,0],
                      [(F(1,3),F(1,3)),(0,1),(0,1)])
    mixed = problem([[2,-2],[-2,F(-1,2)]], [0,1], [(0,1),(0,2)], integers=[1])
    for backend in ('convex','submodular','auto'):
        p = clipped if backend == 'convex' else mixed
        options = {'blocks': [[2]]} if backend == 'convex' else {'discover': False}
        optimum = F(exact_face_minimum(p)['objective'])
        for exact in (False, True):
            for budget in ({}, {'time_limit':0}, {'max_faces':0,'max_pivots':0}):
                cert = solve_with_recourse(p, backend=backend, exact=exact,
                                          max_stages=24, **options, **budget)
                assert verify_pipeline(cert,p)['valid']
                assert F(cert['lower']) <= optimum <= F(cert['upper'])
                if not budget:
                    assert cert['method'] == ('convex' if backend=='convex' else 'submodular')
                    bad=deepcopy(cert);bad['inner']['problem']['b'][0]='17'
                    try:
                        verify_pipeline(bad,p)
                    except RecourseCertificateError:
                        rejected+=1
                    else:
                        raise AssertionError('unbound inner model')
                checked+=1
    for backend in ('submodular','auto'):
        for exact in (False, True):
            cert=solve_with_recourse(mixed,discover=False,backend=backend,
                                     exact=exact,max_cuts=0)
            assert verify_pipeline(cert,mixed)['valid']
            assert F(cert['lower']) <= -2 <= F(cert['upper'])
            assert cert['status'] in ('resource_limit','exact','epsilon_optimal')
            checked+=1
    # Explicit convex blocks refer to ORIGINAL indices after fixed substitution.
    cert=solve_with_recourse(clipped,backend='convex',blocks=[[2]],exact=True)
    assert cert['steps'][0]['private']==[0]
    assert cert['inner']['blocks']==[[1]]
    assert cert['point']==['1/3','2/3','1']
    assert verify_pipeline(cert,clipped)['valid']
    checked+=1
    try:
        verify_pipeline(cert,clipped,max_table_states=1)
    except RecourseCertificateError:
        rejected+=1
    else:
        raise AssertionError('wrapper lost convex replay table cap')
    print({'composed_routes_and_limits':checked,'binding_or_budget_rejections':rejected})

if __name__=='__main__':
    run()
