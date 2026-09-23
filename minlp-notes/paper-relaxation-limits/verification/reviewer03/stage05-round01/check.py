"""Independent finite rational checks; not a proof of asymptotic width."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json


def add(a, b):
    c = a.copy()
    for k, v in b.items():
        c[k] = c.get(k, Q(0)) + v
    return {k: v for k, v in c.items() if v}


def scale(a, t):
    return {k: v*t for k, v in a.items() if v*t}


def mul(a, b):
    c = {}
    for i, x in a.items():
        for j, y in b.items():
            c[i ^ j] = c.get(i ^ j, Q(0)) + x*y
    return {k: v for k, v in c.items() if v}


one = {0: Q(1)}


def substitute(p, fixed, witness):
    out = {}
    for mask, coeff in p.items():
        sign = (-1)**((mask & fixed & witness).bit_count())
        out = add(out, {mask & ~fixed: coeff*sign})
    return out


def localizers():
    # Coefficient tuples, constant first. These are all valid on {+-1};
    # some are also valid on nonclosed sets with those endpoints.
    generators = [(1, 1), (1, -1), (1, 0, -1),
                  (1, 2, 1), (Q(1, 2), Q(3, 2), 1)]
    cases = 0
    zero_indicators = 0
    for D in [1, 2, 3]:
        supports = [s for s in range(1, 16) if s.bit_count() <= D]
        for s, t in product(supports, repeat=2):
            # Signed overlapping or repeated coordinates and a coupled P.
            z, y = {s: Q(1)}, {t: Q(-1)}
            P = add(one, add(scale(z, 2), scale(y, -3)))
            for g, k in product(generators, repeat=2):
                a, d = len(g)+len(k)-2, 1
                r = (a+2*d+1)//2
                assert a+2*d <= 2*r
                assert D*(a+d) <= 2*r*D
                direct = one
                expanded = [(Q(1), one)]
                for coeffs, coord in [(g, z), (k, y)]:
                    value, power = {}, one
                    for c in coeffs:
                        value = add(value, scale(power, c))
                        power = mul(power, coord)
                    direct = mul(direct, value)
                    choices = []
                    for sign in [-1, 1]:
                        weight = sum(c*sign**i for i, c in enumerate(coeffs))
                        assert weight >= 0
                        choices.append((weight, scale(add(one, scale(coord, sign)), Q(1, 2))))
                    expanded = [(c*w, mul(I, J)) for c, I in expanded for w, J in choices]
                rhs = {}
                for weight, I in expanded:
                    assert mul(I, I) == I
                    zero_indicators += int(not I)
                    rhs = add(rhs, scale(mul(mul(I, P), mul(I, P)), weight))
                lhs = mul(direct, mul(P, P))
                assert lhs == rhs
                # Includes fixing signs without assuming positive event mass.
                for fixed, witness in [(0, 0), (s, 5), (s | t, 10)]:
                    assert substitute(lhs, fixed, witness) == substitute(rhs, fixed, witness)
                cases += 1
    # Explicit local equality with a coupled multiplier is zero in the quotient.
    for s in range(1, 16):
        z = {s: Q(-1)}
        eq = add(mul(z, z), scale(one, -1))
        assert mul(eq, add(one, {7: Q(2), 12: Q(-5)})) == {}
    # Smallest lifted order: zero or two local factors, or one linear square.
    r = 1
    for D in [2, 3]:
        for a, d in [(0, 1), (1, 0), (2, 0)]:
            assert a+2*d <= 2*r and 2*D*(a+d) <= 4*r*D
        assert 3 <= 2*r*D
    return {'localizer_identities': cases, 'zero_indicator_summands': zero_indicators,
            'arithmetic': 'exact rational Boolean quotient'}


def upper():
    intervals = [(Q(-1), Q(-1)), (Q(-1), Q(-1, 2)),
                 (Q(-1, 2), Q(0)), (Q(0), Q(1, 3)),
                 (Q(1, 3), Q(1)), (Q(1), Q(1))]
    count = 0
    for box in product(intervals, repeat=3):
        a = tuple(i[0] for i in box)
        h = max(u-l for l, u in box)
        for x in product(*box):
            for u, v, b in product([-1, 1], repeat=3):
                q = 3*h/2-Q(b, 2)*(u*(x[2]-a[2])+a[2]*(x[0]*x[1]-a[0]*a[1]))
                assert q >= 0
                lhs = Q(1-b*v, 2)-(1-b*a[0]*a[1]*a[2])/2+3*h/2
                rhs = q-Q(b, 2)*((v-u*x[2])+a[2]*(u-x[0]*x[1]))
                assert lhs == rhs
                count += 1
    return {'box_vertex_cases': count, 'unequal_width_and_singleton_boxes': True,
            'arithmetic': 'exact rational'}


result = {'localizers': localizers(), 'upper_certificate': upper(),
          'finite_only': True, 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
