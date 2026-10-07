"""Why certify_zB.py uses the midpoints: at rank-one X = a b^T with a = (g0, -rho), b = (1, -rho)
(a degenerate cone whose plane is tangent to dS along the ruling x = rho), the closed conditions for sbar,
P1, P2 and the vertical line hold (margin 0 up to rounding), but the midpoints m01, m02 fail by a wide margin.
Prints, for the Theorem B family at rho = 200, the maximum over admissible lowerings tau in [0, q(s)] of the
smallest eigenvalue of sym(X M(s - tau e_w)) for each test point, and the same for the line condition."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from fractions import Fraction
import certify_zB as c

rho = 200.0
pts = c.points(Fraction(200), 'B')
names = ['sbar', 'P1', 'P2', 'm01', 'm02', 'm12']
for g0 in (0.0, 0.5, 1.0):
    a, b = (g0, -rho), (1.0, -rho)
    X = [[a[0] * b[0], a[0] * b[1]], [a[1] * b[0], a[1] * b[1]]]
    Z = c.symXN(X, c.E)
    out = []
    for nm, s in zip(names, pts):
        A = c.symXN(X, c.Mmat(s))
        q = s[2] - s[0] * s[1]
        f = lambda t: c.lmin_vec(c.comb(A, Z, -t))[0]
        out.append('%s %.3e' % (nm, c.maxconc(f, 0.0, q)[0]))
    A0 = c.symXN(X, c.Mmat((rho, rho, rho * rho)))
    fl = lambda t: c.lmin_vec(c.comb(A0, Z, t))[0]
    T = 1.0
    while fl(2 * T) > fl(T) and T < 1e30:
        T *= 2
    out.append('line %.3e' % c.maxconc(fl, 0.0, 2 * T)[0])
    print('g0 =', g0, ':', ', '.join(out))
