"""Independent finite exact checks for Stage 4 review06; not a universal proof."""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
from math import comb
import hashlib
import json

counts = dict(boxes=0, rlt=0, covariance_entries=0, equality_rows=0,
              affine_products=0, scalar_boundary_cases=0, avoidance_cases=0)

def check_box(k, m, z, restricted, mode):
    n = k + m + z
    K, p = Q(2*k+1, 2), Q(1, 2*m)
    w = [Q(1)]*k + [p]*m + [Q(0)]*z
    R = set(restricted)
    U = set(range(n))-R
    s = len(U)
    t = K-sum(w[i] for i in R)
    assert 1 <= t <= s-1
    c, d = t/s, t*(t-1)/(s*(s-1))
    mu = [w[i] if i in R else c for i in range(n)]
    X = [[mu[i]*mu[j] if i in R or j in R else c if i == j else d
          for j in range(n)] for i in range(n)]
    # Three interval styles include singleton, endpoint-attached and interior
    # intervals. All contain the exact witness and have the intended R.
    a, b = [], []
    for i in range(n):
        if i not in R:
            ai, bi = Q(0), Q(1)
        elif mode == 0:
            ai = bi = w[i]
        elif mode == 1:
            ai, bi = w[i]/2, (1+w[i])/2
        elif w[i] == 1:
            ai, bi = Q(1, 3), Q(1)
        elif w[i] == 0:
            ai, bi = Q(0), Q(2, 3)
        else:
            ai, bi = Q(0), (1+w[i])/2
        a.append(ai)
        b.append(bi)
        assert ai <= w[i] <= bi and ai <= mu[i] <= bi
    assert sum(mu) == K
    for i in range(n):
        assert sum(X[i]) == K*mu[i]
        counts['equality_rows'] += 1
        for j in range(n):
            target = (c-d)*(Q(i == j)-Q(1, s)) if i in U and j in U else 0
            assert X[i][j]-mu[i]*mu[j] == target
            counts['covariance_entries'] += 1
            for slack in [X[i][j]-a[i]*mu[j]-a[j]*mu[i]+a[i]*a[j],
                          b[j]*mu[i]-X[i][j]-a[i]*b[j]+a[i]*mu[j],
                          b[i]*mu[j]-X[i][j]-b[i]*a[j]+a[j]*mu[i],
                          b[i]*b[j]-b[i]*mu[j]-b[j]*mu[i]+X[i][j]]:
                assert slack >= 0
                counts['rlt'] += 1
    assert c-d >= 0  # The verified covariance is a PSD projection multiple.
    assert sum(mu[i]-X[i][i] for i in range(n)) == sum(w[i]*(1-w[i]) for i in R)

    # Original-space affine Farkas representations: arbitrary equality
    # coefficients, nonnegative constants and nonnegative slack coefficients.
    affine = []
    for seed in range(4):
        lam = Q((-1)**seed*(seed+1), 3)
        constant = Q(seed, 5)-lam*K
        linear = [lam]*n
        for i in range(n):
            al, be = Q((i+seed)%4, 3), Q((2*i+seed)%5, 4)
            constant += -al*a[i]+be*b[i]
            linear[i] += al-be
        affine.append((constant, linear))
    for alpha, v in affine:
        for beta, u in affine:
            val = alpha*beta + sum((alpha*u[i]+beta*v[i])*mu[i] for i in range(n))
            val += sum(v[i]*u[j]*X[i][j] for i in range(n) for j in range(n))
            assert val >= 0
            counts['affine_products'] += 1
    counts['boxes'] += 1

for n in range(3, 10):
    for k in range(1, n-1):
        for m in range(1, n-k):
            z = n-k-m
            for size in range(min(k, z)):
                for R in combinations(range(n), size):
                    for mode in range(3):
                        check_box(k, m, z, R, mode)

for s in range(2, 13):
    for t in {Q(1), Q(s-1), Q(s, 2), Q(3*s-2, 4)}:
        if not 1 <= t <= s-1:
            continue
        c, d = t/s, t*(t-1)/(s*(s-1))
        assert c+(s-1)*d == t*c
        assert d-c*c == -(c-d)/s
        assert min(d, c-d, 1-2*c+d) >= 0
        assert 1-2*c+d == (s-t)*(s-t-1)/(s*(s-1))
        counts['scalar_boundary_cases'] += 1

# Marginal avoidance, including empty classes and impossible events, exactly.
for n in range(2, 15):
    for z in range(n):
        for a in range(n+1):
            prob = Q(comb(n-a, z), comb(n, z)) if n-a >= z else Q(0)
            assert prob <= Q(n-z, n)**a
            counts['avoidance_cases'] += 1

assert Q(1,4)-Q(1,32)*Q(11,4)-Q(1,32) == Q(17,128)
assert Q(2)*Q(17,128)/6 == Q(17,384)

paper = Path(__file__).resolve().parents[3]
snapshot = paper/'process/snapshots/stage04-round01'
manifest = json.loads((snapshot/'manifest.json').read_text())
for name, digest in manifest.items():
    assert hashlib.sha256((snapshot/name).read_bytes()).hexdigest() == digest, name
build = json.loads((snapshot/'verification/build-report.json').read_text())
assert hashlib.sha256((snapshot/'main.pdf').read_bytes()).hexdigest() == build['pdf_sha256']
output = {'status':'PASS','arithmetic':'exact rational', 'counts':counts,
          'snapshot_manifest_files_checked':len(manifest),
          'frozen_pdf_matches_build_report':True,
          'limit':'Finite checks supplement the independently reconstructed proofs; no numerical PSD test or exhaustive affine-inequality test is claimed.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
