"""Targeted test of the endpoint rule in Theorem 3.1: f = x^2 written as
-3x^2 + 2x^2 + 2x^2 (three separate power nodes) on C = [-1, 1].
Endpoint formula: Phi([-a, a]) = -3a^2 + max(0, 2a^2, 2a^2) = -a^2, so
pi_D(C) = -1.  Full-range formula: min over sub-boxes = 0 (would predict exact
propagation).  Also the one-sided monomial form x^2 (exact)."""
from ifbbt import DAG
d = DAG(1); p1 = d.pow(0, 2); p2 = d.pow(0, 2); p3 = d.pow(0, 2); d.sum([p1, p2, p3], [-3, 2, 2])
print('three-term x^2: pi_D([-1,1]) =', round(d.pi([(-1.0, 1.0)], hi=0.0), 8),
      ' pi_D([-0.1,0.1]) =', round(d.pi([(-0.1, 0.1)], hi=0.0), 8),
      ' pi_D([-0.1,0.3]) =', round(d.pi([(-0.1, 0.3)], hi=0.0), 8))
for eps in (1e-2, 1e-6):
    st, Z, r = d.propagate([(-1.0, 1.0)], -eps)
    print(f'  cutoff -{eps:g}: {st} after {r} rounds; x-box {d.xbox(Z) if Z else None}; '
          f'term intervals {[tuple(round(v, 6) for v in Z[k]) for k in (p1, p2, p3)] if Z else None}')
e = DAG(1); q = e.pow(0, 2); e.sum([q], [1.0])
print('single-term x^2: pi_D([-1,1]) =', round(e.pi([(-1.0, 1.0)], hi=0.0), 8))
