"""Independent small-instance audit of affine recourse recognition/composition."""
from pathlib import Path
import sys
from fractions import Fraction as F
from itertools import product
from copy import deepcopy
from types import SimpleNamespace
import random

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'solver'))
sys.path.insert(0, str(ROOT / 'solver' / 'extra-benchmarks'))
from certified_grid import BoxQP
from recourse import recognize_affine, transform, lift, solve_with_recourse
from verify_recourse import verify_selector, verify_pipeline, RecourseCertificateError
from corpus import exact_face_minimum as _face_minimum

def exact_face_minimum(p):
    return _face_minimum(SimpleNamespace(A=p.A, b=p.b, c=p.constant, bounds=p.bounds, integers=p.integers))


def problem(A, b, bounds, integers=(), constant=0):
    return BoxQP(A, b, bounds, integers, [list(range(len(b)))], [], constant)


def run():
    rng = random.Random(782341)
    scalar_count = planted_count = tamper_count = 0
    for case in range(80):
        c, d, h = F(rng.randrange(0, 5)), F(rng.randrange(-6, 7)), F(rng.randrange(-6, 7))
        zl, zu = F(rng.randrange(-3, 0)), F(rng.randrange(1, 4))
        yl, yu = F(rng.randrange(-3, 1)), F(rng.randrange(1, 4))
        p = problem([[-1, d], [d, c]], [F(1, 7), h], [(zl, zu), (yl, yu)])
        gmin, gmax = min(h+d*zl, h+d*zu), max(h+d*zl, h+d*zu)
        # Direct scalar classification: the affine unclipped optimizer must
        # remain inside, or every optimizer must be the same bound.
        if c:
            low, high = -gmax/c, -gmin/c
            expected = high <= yl or low >= yu or yl <= low <= high <= yu
        else:
            expected = gmin >= 0 or gmax <= 0
        result = recognize_affine(p, [1])
        assert result['status'] == ('affine' if expected else 'no_affine_selector'), (case, result, c,d,h,zl,zu,yl,yu)
        if expected:
            verify_selector(p, result['proof'])
            reduced, _ = transform(p, result['proof'])
            assert F(exact_face_minimum(p)['objective']) == F(exact_face_minimum(reduced)['objective'])
        scalar_count += 1

    for case in range(24):
        k, r = 1 + case % 2, 1 + case % 3
        n = k + r
        vectors = [[F(rng.randrange(-2, 3)) for _ in range(r)] for _ in range(1 + case % r)]
        C = [[sum((row[i]*row[j] for row in vectors), F(0)) for j in range(r)] for i in range(r)]
        a = [F(1,2)] * r
        B = [[F(rng.randrange(-1, 2), 4*k) for _ in range(k)] for _ in range(r)]
        # F=1/2(y-a-Bz)'C(y-a-Bz) + diagonal indefinite core.
        T = [[-B[i][j] if j<k else F(j-k == i) for j in range(n)] for i in range(r)]
        A = [[sum((T[s][i]*C[s][t]*T[t][j] for s in range(r) for t in range(r)), F(0)) for j in range(n)] for i in range(n)]
        for j in range(k):
            A[j][j] += F((-1)**j, j+1)
        b = [-sum((T[s][i]*C[s][t]*a[t] for s in range(r) for t in range(r)), F(0)) for i in range(n)]
        constant = sum((a[s]*C[s][t]*a[t] for s in range(r) for t in range(r)), F(0))/2
        p = problem(A,b,[(0,1)]*n, integers=[0] if case%4==0 else (), constant=constant)
        result = recognize_affine(p, list(range(k,n)))
        assert result['status'] == 'affine', (case,result)
        verify_selector(p,result['proof'])
        reduced,_=transform(p,result['proof'])
        assert F(exact_face_minimum(p)['objective']) == F(exact_face_minimum(reduced)['objective'])
        for z in product((F(0),F(1,3),F(1)), repeat=k):
            x=lift(p,result['proof'],z)
            assert p.value(x)==reduced.value(z)
        cert=solve_with_recourse(p,blocks=[list(range(k,n))],discover=False,backend='grid',max_stages=4,time_limit=3)
        assert verify_pipeline(cert,p)['valid']
        assert F(cert['lower']) <= F(exact_face_minimum(p)['objective']) <= F(cert['upper'])
        planted_count+=1

    # Genuine approximation: its exact-request flag must not be forgeable.
    p=problem([[2,2],[2,0]],[F(-1,3),-1],[(0,1),(0,1)])
    cert=solve_with_recourse(p,discover=False,backend='grid',epsilon=1,max_stages=1)
    for key,value in [('exact_requested', 'yes'),('exact_requested', True)]:
        bad=deepcopy(cert);bad[key]=value
        try:
            verify_pipeline(bad,p)
        except RecourseCertificateError:
            tamper_count+=1
        else:
            raise AssertionError(('invalid request accepted', key, value, bad['status'], bad['gap']))
    print({'scalar_classifications':scalar_count,'planted_psd_blocks':planted_count,'exact_request_tampers_rejected':tamper_count})

if __name__ == '__main__':
    run()
