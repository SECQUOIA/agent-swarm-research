"""Critic: exact feasibility of the envelope (own parser, own envelope, generic row evaluation), n = 100, 200."""
import sys
from fractions import Fraction as Fr
sys.set_int_max_str_digits(0)
sys.path.insert(0, '/tmp/camcrit')
from mine import parse, structure, envelope_exact, digits
for n in (100, 200):
    V, C, oc, lin, quad = parse(f'camshape{n}.osil'); K = structure(f'camshape{n}.osil', n)
    U, S, B, E = envelope_exact(K, n)
    x = E[1:] + [E[i + 1] - E[i] for i in range(1, n)]
    worst = Fr(0); active = 0
    for i, (nm, lb, ub) in enumerate(C):
        v = sum(k * x[j] for j, k in lin[i].items()) + sum(k * x[a] * x[b] for (a, b), k in quad[i].items())
        worst = max(worst, (v - ub) if ub is not None else 0, (lb - v) if lb is not None else 0)
        if i <= n and ub == 0 and lb is None and v == 0: active += 1
    bv = max(max((lo - x[k]) if lo is not None else 0, (x[k] - hi) if hi is not None else 0) for k, (lo, hi) in enumerate(V))
    obj = sum(k * x[j] for j, k in oc.items())
    print(n, 'row viol', worst, 'bound viol', bv, 'active conv rows', active, 'obj floor14', digits(obj, 14), '|E2-E1|', float(E[2] - E[1]))
