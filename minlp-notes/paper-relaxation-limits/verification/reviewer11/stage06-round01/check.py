"""Independent exact finite FBBT checks; no universal theorem certification."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json

out = Path(__file__).parent
snap = out.parents[2] / 'process/snapshots/stage06-round01'
checks = {'arithmetic': 'exact fractions', 'finite_scope': True}

# Exhaust the normalized integer outputs, including equal outputs and c=0,1.
count = 0
for L in range(1, 4):
    M = 2 ** (2 ** L)
    b = Q(1, 2 ** (2 ** (L + 2)))
    assert b <= Q(1, 8*M)
    for U, V in product(range(M+1), repeat=2):
        c = Q(1, 2) + Q(U-V, 2*M)
        d = 1-c
        a = Q(1) if c <= Q(1, 2) else d/c
        assert a == d+c*a*a
        z = b/(1-(1-b)*a)
        assert 0 <= a <= 1 and 0 < z <= 1
        if U > V:
            assert 1-a >= Q(1,M)
            assert z <= b*M <= Q(1,8)
            assert z+Q(1,4) < Q(1,2)
        else:
            assert z == 1 and z-Q(1,4) > Q(1,2)
        assert c*a <= Q(1,2)
        count += 1
checks['detector_amplifier_cases'] = count

# Exact interval hulls with b,c fixed; enumerate every update word through
# length 12. States contain lz,uz,lw,uw and the number of affine applications.
states_checked = 0
for n in range(1, 5):
    b = Q(1,2**(2**n)); c = 1-b
    states = {(Q(0), Q(1), Q(0), Q(1), 0)}
    for step in range(12):
        nxt = set()
        for lz,uz,lw,uw,K in states:
            # z=b+w: exact coordinate hull of the affine intersection.
            aff = (max(lz,b+lw), min(uz,b+uw),
                   max(lw,lz-b), min(uw,uz-b), K+1)
            # w=c*z: exact coordinate hull since c is a positive constant.
            mul = (max(lz,lw/c), min(uz,uw/c),
                   max(lw,c*lz), min(uw,c*uz), K)
            for v in (aff,mul):
                zlo,zup,wlo,wup,k = v
                assert zup == 1 and wup in (Q(1),c)
                assert 0 <= wlo <= c*zlo <= c
                assert zlo <= 1-c**k <= k*b
                if zlo >= Q(1,2):
                    assert k >= 2**(2**n-1)
                nxt.add(v); states_checked += 1
        states = nxt
checks['primitive_transitions_checked'] = states_checked

# The exact scalar error comparison used for the inherited Kleene chain.
for n in range(1,5):
    x = [Q(0)]*(n+1)
    for k in range(9):
        err = [1-t for t in x]
        assert err[0] >= Q(1,k+1)
        for i in range(1,n+1):
            assert err[i]**2 >= err[i-1]
        assert err[n]**(2**n) >= Q(1,k+1)
        x = [(x[0]**2+1)/2] + [(x[i]**2+x[i-1])/2 for i in range(1,n+1)]
checks['kleene_cases'] = 36
pdf = snap/'main.pdf'
checks['frozen_pdf_sha256'] = hashlib.sha256(pdf.read_bytes()).hexdigest()
assert checks['frozen_pdf_sha256'] == '343b29156e275df970236babbab1077b3a53261317e0995a6a7ea0398b583916'
(out/'check.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
