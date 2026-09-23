"""Independent exact enclosure checks for rational_affine_flow.

The reference uses a Lagrange exponential remainder with a rational upper
bound on exp(||M||), separate from the implementation's geometric tail.
Run directly with the existing isolated project environment.
"""

from fractions import Fraction as Q
from itertools import product
from math import factorial
import json
import random
from rational_affine_flow import Slab, certify_affine_flow


def mm(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),Q(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def interval_exponential(a):
    """Independent Lagrange remainder with e^q <= (1-q/m)^(-m)."""
    n=len(a)
    q=max(sum(map(abs,row),Q(0)) for row in a)
    identity=[[Q(i==j) for j in range(n)] for i in range(n)]
    if q==0:
        return [[(x,x) for x in row] for row in identity]
    order=70
    result=[row[:] for row in identity]
    power=identity
    nilpotent=False
    for j in range(1,order+1):
        power=mm(power,a)
        if not any(any(row) for row in power):
            nilpotent=True
            break
        for i in range(n):
            for k in range(n):
                result[i][k]+=power[i][k]/factorial(j)
    m=q.numerator//q.denominator+2
    remainder=Q(0) if nilpotent else (1-q/m)**(-m)*q**(order+1)/factorial(order+1)
    return [[(x-remainder,x+remainder) for x in row] for row in result]


def imul(a,b):
    output=[]
    for i in range(len(a)):
        row=[]
        for j in range(len(b[0])):
            low=high=Q(0)
            for k in range(len(b)):
                terms=[x*y for x in a[i][k] for y in b[k][j]]
                low+=min(terms); high+=max(terms)
            row.append((low,high))
        output.append(row)
    return output


def reference(initial,slabs,p):
    n=len(initial)
    v=[[(Q(x),Q(x)) for x in row] for row in initial]
    bottom=[[(Q(i==j),Q(i==j)) for j in range(p+1)] for i in range(p+1)]
    for s in slabs:
        a=[[Q(s.duration)*Q(x) for x in list(s.B[i])+list(s.A[i])+[s.d[i]]]
           for i in range(n)]+[[Q(0)]*(n+p+1) for _ in range(p+1)]
        v=imul(interval_exponential(a)[:n],v+bottom)
    return v


def check(initial,slabs,box,order,denominator):
    cert=certify_affine_flow(slabs,initial,box,order=order,grid_denominator=denominator)
    exact=reference(initial,slabs,len(box))
    rowerror=max(sum(max(abs(x-lo),abs(x-hi)) for x,(lo,hi) in zip(row,target))
                 for row,target in zip(cert.approximate,exact))
    assert rowerror<=cert.coefficient_error, (initial,slabs,order,denominator,rowerror,cert)
    corners=list(product(*box)) if box else [()]
    for p in corners:
        lower=cert.evaluate(p)
        vector=list(p)+[Q(1)]
        for value,row in zip(lower,exact):
            reference_lower=sum(min(c*x for c in interval) for interval,x in zip(row,vector))
            assert value<=reference_lower, (value,reference_lower,cert)
    return len(corners), float(rowerror/cert.coefficient_error) if cert.coefficient_error else 0


def high_precision_diagnostics():
    """An external matrix-exponential comparison; not part of the proof."""
    import mpmath as mp

    def mpx(x):
        x=Q(x)
        return mp.mpf(x.numerator)/x.denominator

    maximum_ratio=mp.mpf(0)
    with mp.workdps(120):
        for trial in range(24):
            n,p=1+trial%3,trial%2
            initial=[[Q((i+1)*(j+1),7) for j in range(p+1)] for i in range(n)]
            numerical=mp.matrix([[mpx(x) for x in row] for row in initial])
            slabs=[]
            for k in range(1+trial%4):
                b=[[Q((-1 if (trial+k)%2 else 1)*(i+1),3) if i==j
                    else Q((i+j+k)%3,5) for j in range(n)] for i in range(n)]
                a=[[Q((-1)**(i+j+k),3) for j in range(p)] for i in range(n)]
                d=[Q(i-k,3) for i in range(n)]
                h=Q(1,4)
                slabs.append(Slab(h,b,a,d))
                m=mp.matrix(n+p+1)
                for i in range(n):
                    for j,x in enumerate(b[i]+a[i]+[d[i]]):
                        m[i,j]=mpx(h*x)
                augmented=mp.matrix(n+p+1,p+1)
                for i in range(n):
                    for j in range(p+1):
                        augmented[i,j]=numerical[i,j]
                for i in range(p+1):
                    augmented[n+i,i]=1
                numerical=(mp.expm(m)*augmented)[:n,:]
            certificate=certify_affine_flow(slabs,initial,[[-3,5]]*p,
                                           order=30,grid_denominator=10**40)
            observed=max(sum(abs(numerical[i,j]-mpx(certificate.approximate[i][j]))
                             for j in range(p+1)) for i in range(n))
            bound=mpx(certificate.coefficient_error)
            assert observed<=bound
            maximum_ratio=max(maximum_ratio,observed/bound)
    return {'cases':24,'decimal_precision':120,'max_observed_error_over_bound':float(maximum_ratio)}


def main():
    rng=random.Random(3921071)
    cases=100
    corners=0
    maximum_ratio=0
    for trial in range(cases):
        n,p=1+trial%3,trial%3
        order=(0,1,2,6,18)[trial%5]
        denominator=(1,7,10**8,10**20)[trial%4]
        initial=[[Q(rng.randrange(-10,11),7) for _ in range(p+1)] for _ in range(n)]
        slabs=[]
        for _ in range(1+trial%4):
            b=[[Q(rng.randrange(-5,6) if i==j else rng.randrange(0,6),3)
                for j in range(n)] for i in range(n)]
            a=[[Q(rng.randrange(-5,6),3) for _ in range(p)] for _ in range(n)]
            d=[Q(rng.randrange(-5,6),3) for _ in range(n)]
            norm=max(sum(map(abs,b[i]+a[i]+[d[i]])) for i in range(n))
            h=Q(rng.randrange(0,5),10)
            if norm*h>=order+2:
                h=(order+1)/(norm+1)
            slabs.append(Slab(h,b,a,d))
        box=[(Q(-100 if trial%7==0 else -2),Q(73 if trial%11==0 else 3)) for _ in range(p)]
        c,r=check(initial,slabs,box,order,denominator)
        corners+=c; maximum_ratio=max(maximum_ratio,r)
    special=[
        ([[Q(1,3)]],[],[],0,1),
        ([[Q(1,3)]],[Slab(0,[[0]],[[]],[0])],[],0,1),
        ([[0]],[Slab(1,[[0]],[[]],[1])],[],0,1),
        ([[0]],[Slab(1,[[0]],[[]],[-1])],[],0,1),
        ([[Q(-1,2)]],[Slab(0,[[0]],[[]],[0])],[],0,1),
        ([[0,0]],[Slab(1,[[0]],[[1]],[1])],[(-1,1)],2,1),
        ([[0,0]],[Slab(3,[[0]],[[1]],[0])],[(2,2)],2,1),
        ([[1],[0],[0]],[Slab(1,[[0,1,0],[0,0,1],[0,0,0]],[[],[],[]],[0,0,2])],[],4,1),
        ([[1,0],[0,1]],[Slab(Q(1,2),[[0,2],[0,0]],[[1],[-1]],[0,1]),Slab(Q(1,2),[[0,0],[2,0]],[[-1],[1]],[1,0])],[(-3,4)],4,10**12),
    ]
    for args in special:
        c,r=check(*args); corners+=c; maximum_ratio=max(maximum_ratio,r)
    bad=[
        lambda: certify_affine_flow([], [], []),
        lambda: certify_affine_flow([], [[1]], [], order=True),
        lambda: certify_affine_flow([], [[1]], [], order=-1),
        lambda: certify_affine_flow([], [[1]], [], order=1.0),
        lambda: certify_affine_flow([], [[1]], [], grid_denominator=True),
        lambda: certify_affine_flow([], [[1]], [], grid_denominator=0),
        lambda: certify_affine_flow([], [[1]], [], grid_denominator=1.0),
        lambda: certify_affine_flow([], [[True]], []),
        lambda: certify_affine_flow([], [[0.1]], []),
        lambda: certify_affine_flow([], [[1,2]], []),
        lambda: certify_affine_flow([], [[1]], [[0,1]]),
        lambda: certify_affine_flow([], [[1]], [[0]]),
        lambda: certify_affine_flow([], [[1]], [[0,1,2]]),
        lambda: certify_affine_flow([], [[1]], [[1,0]]),
        lambda: certify_affine_flow([], [[1]], [[0,True]]),
        lambda: certify_affine_flow([Slab(-1,[[0]],[[]],[0])], [[0]], []),
        lambda: certify_affine_flow([Slab(1,[[0,0]],[[]],[0])], [[0]], []),
        lambda: certify_affine_flow([Slab(1,[[0]],[],[0])], [[0]], []),
        lambda: certify_affine_flow([Slab(1,[[0]],[[]],[])], [[0]], []),
        lambda: certify_affine_flow([Slab(1,[[0]],[[]],[0.0])], [[0]], []),
        lambda: certify_affine_flow([Slab(1,[[0,-1],[0,0]],[[],[]],[0,0])], [[0],[0]], []),
        lambda: certify_affine_flow([Slab(2,[[1]],[[]],[0])], [[0]], [],order=0),
        lambda: certify_affine_flow([], [[0,1]], [[0,1]]).evaluate([]),
        lambda: certify_affine_flow([], [[0,1]], [[0,1]]).evaluate([2]),
        lambda: certify_affine_flow([], [[0,1]], [[0,1]]).evaluate([0.5]),
    ]
    for fn in bad:
        try:
            fn()
        except (ValueError,TypeError):
            pass
        else:
            raise AssertionError('Malformed input was accepted')
    print(json.dumps({'random_exact_enclosures':cases,'special_exact_enclosures':len(special),'box_corner_checks':corners,'max_exact_error_enclosure_over_certificate':maximum_ratio,'malformed_inputs_rejected':len(bad),'high_precision_diagnostics':high_precision_diagnostics()},indent=2))

if __name__=='__main__':
    main()
