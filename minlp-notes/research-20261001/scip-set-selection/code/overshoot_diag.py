"""List C step lengths that exceed the exact (bisection) step of the same set by more than 1e-7 relative, for
exact steps below 1e9, with the value of q at the C point (q > 0 means the C point is still outside S)."""
import sys, json, gzip
import numpy as np
from check_dump import Corner
lines = [json.loads(l.replace('-nan', 'NaN').replace('nan', 'NaN')) for l in gzip.open(sys.argv[1], 'rt')]
maxc = int(sys.argv[2]) if len(sys.argv) > 2 else 60
k = 0; nc = 0
while k < len(lines) and nc < maxc:
    d = lines[k]; fin = lines[k + 1] if k + 1 < len(lines) and lines[k + 1]['type'] == 'final' else None
    k += 2 if fin is not None else 1
    if d['type'] != 'corner':
        continue
    nc += 1
    c = Corner(d)
    for name, al, lam in (('alpha0', d['alpha0'], np.array(d['lam0'])),
                          ('alpha', d['alpha'], np.array(d['lam']) if d['changed'] else np.array(d['lam0'])),
                          ('final', fin['alpha'] if fin and fin['success'] else None,
                           np.array(d['lam']) if d['changed'] else np.array(d['lam0']))):
        if al is None:
            continue
        for j in range(c.P.shape[1]):
            a = np.inf if al[j] < 0 else al[j]
            b = c.step(lam, c.P[:, j])
            if np.isfinite(a) and np.isfinite(b) and b < 1e9 and a > b * (1 + 1e-7) + 1e-9:
                print(json.dumps(dict(corner=nc, which=name, ray=j, C=a, exact=b, rel=(a - b) / b,
                                      q_at_C=c.q(c.sbar + a * c.P[:, j]), qbar=c.q(c.sbar))))
