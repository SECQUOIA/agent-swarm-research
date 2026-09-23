"""Exact weighted resistance design on a cactus supplied as independent blocks.

Cycle input has coherent orientation, x_e=q+offset_e, objective sum w_e*beta_e*
x_e*abs(x_e), and independent positive resistance intervals. Optional rational
flow bounds filter scenarios. Bridges have fixed flows. Graph-to-block mapping
is outside this module: callers must supply a valid fixed-nomination cactus
block decomposition and the corresponding objective coefficients.

All optimization and feasibility arithmetic is exact. Each block's objective
is stored in its own quadratic field; the global value is a sum of these terms,
with a certified rational interval. No exact global threshold oracle is claimed.

CLI: python exact_weighted_cactus.py INPUT.json [--bits 40]
Rationals in JSON are integers or strings such as "3/2"; floating-point input
is rejected. See notes/potential-flow-exact-weighted-cactus-solver.md.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt
import argparse
import json


def rational(value):
    if isinstance(value, (float, bool)):
        raise ValueError('Use integer or rational-string input, not float/bool')
    return F(value)


def sign(x):
    return (x > 0) - (x < 0)


def radical_sign(a, b, d):
    """Sign of a+b*sqrt(d), for nonnegative rational d."""
    if b == 0 or d == 0:
        return sign(a)
    if a == 0:
        return sign(b)
    if sign(a) == sign(b):
        return sign(a)
    return sign(a) * sign(a*a-b*b*d)


@dataclass(frozen=True, eq=False)
class Quadratic:
    a: F = F(0)
    b: F = F(0)
    d: F = F(0)

    def __post_init__(self):
        a, b, d = rational(self.a), rational(self.b), rational(self.d)
        if d < 0:
            raise ValueError('Negative radicand')
        if b == 0 or d == 0:
            b, d = F(0), F(0)
        else:
            sn, sd = isqrt(d.numerator), isqrt(d.denominator)
            if sn*sn == d.numerator and sd*sd == d.denominator:
                a, b, d = a+b*F(sn, sd), F(0), F(0)
        object.__setattr__(self, 'a', a)
        object.__setattr__(self, 'b', b)
        object.__setattr__(self, 'd', d)

    @staticmethod
    def coerce(value):
        return value if isinstance(value, Quadratic) else Quadratic(rational(value))

    def __neg__(self):
        return Quadratic(-self.a, -self.b, self.d)

    def __add__(self, other):
        other = self.coerce(other)
        if self.b and other.b and self.d != other.d:
            raise ValueError('Addition requires matching stored radicands')
        return Quadratic(self.a+other.a, self.b+other.b, self.d if self.b else other.d)

    __radd__ = __add__

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        if self.b and other.b and self.d != other.d:
            raise ValueError('Multiplication requires matching stored radicands')
        d = self.d if self.b else other.d
        return Quadratic(self.a*other.a+self.b*other.b*d,
                         self.a*other.b+self.b*other.a, d)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = rational(other)
        return Quadratic(self.a/other, self.b/other, self.d)

    def compare(self, other):
        other = self.coerce(other)
        # Difference is U+V, U=a+b sqrt(d), V=c sqrt(e).
        a, b, d, c, e = self.a-other.a, self.b, self.d, -other.b, other.d
        su = radical_sign(a, b, d)
        sv = sign(c) if e else 0
        if not su:
            return sv
        if not sv or su == sv:
            return su
        # U and V have opposite signs. Compare their squared magnitudes.
        return su * radical_sign(a*a+b*b*d-c*c*e, 2*a*b, d)

    def __eq__(self, other):
        try:
            return self.compare(other) == 0
        except (TypeError, ValueError):
            return False

    def __lt__(self, other):
        return self.compare(other) < 0

    def __le__(self, other):
        return self.compare(other) <= 0

    def __gt__(self, other):
        return self.compare(other) > 0

    def __ge__(self, other):
        return self.compare(other) >= 0

    def interval(self, bits=40):
        if type(bits) is not int or bits < 0:
            raise ValueError('bits must be a nonnegative integer')
        if not self.b:
            return self.a, self.a
        extra = max(0, abs(self.b.numerator).bit_length()-self.b.denominator.bit_length()+1)
        k = bits+extra
        scaled = (self.d.numerator << (2*k)) // self.d.denominator
        lo = F(isqrt(scaled), 1 << k)
        hi = lo + F(1, 1 << k)
        bounds = (self.a+self.b*lo, self.a+self.b*hi)
        return min(bounds), max(bounds)

    def as_dict(self):
        return {'rational': str(self.a), 'sqrt_coefficient': str(self.b),
                'radicand': str(self.d)}


def polynomial(offsets, signs, multipliers):
    return (sum(k*s for k, s in zip(multipliers, signs)),
            sum(2*k*s*t for k, s, t in zip(multipliers, signs, offsets)),
            sum(k*s*t*t for k, s, t in zip(multipliers, signs, offsets)))


def evaluate(poly, q):
    a, b, c = poly
    return (q*a+b)*q+c


def roots(poly):
    a, b, c = poly
    if not a:
        return [Quadratic(-c/b)] if b else []
    d = b*b-4*a*c
    if d < 0:
        return []
    return [Quadratic(-b/(2*a), F(-1)/(2*a), d),
            Quadratic(-b/(2*a), F(1)/(2*a), d)]


def check_cycle_witness(offsets, weights, lower, upper, flow_lower, flow_upper,
                        q, beta, objective):
    """Recompute every physical equation and bound using exact arithmetic."""
    if not all(l <= v <= u for l, v, u in zip(lower, beta, upper)):
        raise ArithmeticError('Resistance witness violates interval')
    flows = [q+t for t in offsets]
    for i, x in enumerate(flows):
        if ((flow_lower[i] is not None and x < flow_lower[i]) or
                (flow_upper[i] is not None and x > flow_upper[i])):
            raise ArithmeticError('Flow witness violates capacity')
    drops = [v*x*x*(1 if x >= 0 else -1) for x, v in zip(flows, beta)]
    if sum(drops, Quadratic()) != 0:
        raise ArithmeticError('Cycle potential conservation fails')
    value = sum((w*y for w, y in zip(weights, drops)), Quadratic())
    if value != objective:
        raise ArithmeticError('Objective reconstruction fails')


def solve_cycle(offsets, weights, lower, upper, flow_lower=None, flow_upper=None,
                sense='max'):
    """Return exact optimal q, rational resistances, and objective, or None."""
    if sense not in ('max', 'min'):
        raise ValueError('sense must be max or min')
    offsets, weights, lower, upper = [list(map(rational, values))
                                      for values in (offsets, weights, lower, upper)]
    n = len(offsets)
    if n < 2 or any(len(a) != n for a in (weights, lower, upper)):
        raise ValueError('Cycle arrays must have equal length at least two')
    if any(l <= 0 or u < l for l, u in zip(lower, upper)):
        raise ValueError('Resistance intervals must be positive and nonempty')
    def bounds(values):
        if values is None:
            return [None]*n
        if len(values) != n:
            raise ValueError('Capacity arrays must match cycle length')
        return [None if v is None else rational(v) for v in values]
    flow_lower, flow_upper = bounds(flow_lower), bounds(flow_upper)
    if any(l is not None and u is not None and l > u for l, u in zip(flow_lower, flow_upper)):
        raise ValueError('Empty flow interval')
    direction = 1 if sense == 'max' else -1
    work_weights = [direction*w for w in weights]
    left, right = min(-x for x in offsets), max(-x for x in offsets)
    for t, l, u in zip(offsets, flow_lower, flow_upper):
        if l is not None:
            left = max(left, l-t)
        if u is not None:
            right = min(right, u-t)
    if left > right:
        return None
    cuts = sorted({left, right} | {-t for t in offsets if left < -t < right})
    panels = list(zip(cuts, cuts[1:])) if len(cuts) > 1 else [(left, right)]
    best = None
    for left, right in panels:
        middle = (left+right)/2
        signs = [1 if middle+t >= 0 else -1 for t in offsets]
        for lam in sorted(set(work_weights)):
            tied = [i for i, w in enumerate(work_weights) if w == lam]
            endpoints = [upper[i] if (work_weights[i]-lam)*signs[i] > 0 else lower[i]
                         for i in range(n)]
            low, high = list(endpoints), list(endpoints)
            for i in tied:
                low[i], high[i] = ((lower[i], upper[i]) if signs[i] > 0
                                  else (upper[i], lower[i]))
            lo_poly = polynomial(offsets, signs, low)
            hi_poly = polynomial(offsets, signs, high)
            objective_poly = polynomial(offsets, signs,
                                        [(w-lam)*v for w, v in zip(work_weights, endpoints)])
            candidates = [Quadratic(left), Quadratic(right)] + roots(lo_poly) + roots(hi_poly)
            a, b, _ = objective_poly
            if a:
                candidates.append(Quadratic(-b/(2*a)))
            # A flat objective needs only boundary candidates, which include
            # aggregate-feasibility roots and rational panel/capacity limits.
            for q in candidates:
                if not left <= q <= right:
                    continue
                lo_value, hi_value = evaluate(lo_poly, q), evaluate(hi_poly, q)
                if lo_value > 0 or hi_value < 0:
                    continue
                value = evaluate(objective_poly, q)
                if best is not None and value <= best['comparison_value']:
                    continue
                if q.b:
                    if lo_value == 0:
                        beta = low
                    elif hi_value == 0:
                        beta = high
                    else:
                        raise ArithmeticError('Irrational candidate has no active aggregate boundary')
                else:
                    f = [(q.a+t)*abs(q.a+t) for t in offsets]
                    beta = list(low)
                    remaining = -sum(v*x for v, x in zip(beta, f))
                    for i in tied:
                        amount = min(remaining, abs(f[i])*(upper[i]-lower[i]))
                        if f[i]:
                            beta[i] += amount/f[i]
                        remaining -= amount
                    if remaining:
                        raise ArithmeticError('Exact tied-contribution recovery failed')
                original_value = direction*value
                check_cycle_witness(offsets, weights, lower, upper, flow_lower, flow_upper,
                                    q, beta, original_value)
                best = {'circulation': q, 'resistances': tuple(beta),
                        'objective': original_value, 'comparison_value': value,
                        'threshold': direction*lam}
    if best is not None:
        del best['comparison_value']
    return best


def solve_cactus(problem, bits=40):
    """Solve independent cycle/bridge blocks; return a JSON-compatible result."""
    if type(bits) is not int or bits < 0:
        raise ValueError('bits must be a nonnegative integer')
    if not isinstance(problem, dict):
        raise ValueError('Problem must be a JSON object')
    unknown = set(problem)-{'sense', 'cycles', 'bridges'}
    if unknown:
        raise ValueError(f'Unknown problem keys: {sorted(unknown)}')
    if not ({'cycles', 'bridges'} & set(problem)):
        raise ValueError('Supply an explicit cycles or bridges list')
    schemas = (
        ('cycles', {'offsets', 'weights', 'lower', 'upper'}, {'flow_lower', 'flow_upper'}),
        ('bridges', {'flow', 'weight', 'lower', 'upper'}, {'flow_lower', 'flow_upper'}),
    )
    for kind, required, optional in schemas:
        blocks = problem.get(kind, [])
        if not isinstance(blocks, list):
            raise ValueError(f'{kind} must be a list')
        for block in blocks:
            if not isinstance(block, dict):
                raise ValueError(f'Each {kind} entry must be an object')
            missing, extra = required-set(block), set(block)-required-optional
            if missing or extra:
                raise ValueError(f'Invalid {kind} keys: missing={sorted(missing)}, unknown={sorted(extra)}')
            if kind == 'cycles':
                for key in required | (optional & set(block)):
                    if block[key] is not None and not isinstance(block[key], list):
                        raise ValueError(f'Cycle {key} must be an array')
                if any(block[key] is None for key in required):
                    raise ValueError('Required cycle arrays cannot be null')
    sense = problem.get('sense', 'max')
    if sense not in ('max', 'min'):
        raise ValueError('sense must be max or min')
    results, terms = [], []
    infeasible = False
    for block in problem.get('cycles', []):
        result = solve_cycle(**block, sense=sense)
        if result is None:
            infeasible = True
            continue
        terms.append(result['objective'])
        results.append({'circulation': result['circulation'].as_dict(),
                        'resistances': list(map(str, result['resistances'])),
                        'objective': result['objective'].as_dict(),
                        'threshold': str(result['threshold'])})
    bridges = []
    for block in problem.get('bridges', []):
        x, w, l, u = [rational(block[key]) for key in ('flow', 'weight', 'lower', 'upper')]
        if l <= 0 or u < l:
            raise ValueError('Bridge resistance interval must be positive and nonempty')
        flo = None if block.get('flow_lower') is None else rational(block['flow_lower'])
        fhi = None if block.get('flow_upper') is None else rational(block['flow_upper'])
        if flo is not None and fhi is not None and flo > fhi:
            raise ValueError('Empty bridge flow interval')
        if (flo is not None and x < flo) or (fhi is not None and x > fhi):
            infeasible = True
            continue
        coefficient = w*x*abs(x)
        beta = u if coefficient*(1 if sense == 'max' else -1) > 0 else l
        term = Quadratic(coefficient*beta)
        terms.append(term)
        bridges.append({'flow': str(x), 'resistance': str(beta), 'objective': term.as_dict()})
    if infeasible:
        return {'status': 'infeasible'}
    term_bits = bits+max(0, (len(terms)-1).bit_length())
    intervals = [term.interval(term_bits) for term in terms]
    return {'status': 'optimal', 'sense': sense, 'cycles': results, 'bridges': bridges,
            'objective_terms': [t.as_dict() for t in terms],
            'objective_interval': [str(sum(v[0] for v in intervals)),
                                   str(sum(v[1] for v in intervals))],
            'interval_width_bound': str(F(1, 1 << bits))}


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='JSON file containing cycle and bridge blocks')
    parser.add_argument('--bits', type=int, default=40)
    args = parser.parse_args()
    with open(args.input, encoding='utf-8') as handle:
        problem = json.load(handle, object_pairs_hook=reject_duplicate_keys)
    print(json.dumps(solve_cactus(problem, args.bits), indent=2))


if __name__ == '__main__':
    main()
