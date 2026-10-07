"""Exact diagnostics for the new irrational-core cubic completion interface.

This does not implement the general core Cauchy or convex optimization oracle.
The coupled fixture has an explicit quadratic-radical optimal core; its
rational regularized completion reduces to a monotone scalar derivative.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
import json


@dataclass(frozen=True)
class Radical:
    p: Q
    q: Q
    d: Q

    def cv(self, other):
        if isinstance(other, Radical):
            assert self.d == other.d
            return other
        return Radical(Q(other), Q(0), self.d)

    def __add__(self, other):
        o = self.cv(other)
        return Radical(self.p + o.p, self.q + o.q, self.d)

    __radd__ = __add__

    def __neg__(self):
        return Radical(-self.p, -self.q, self.d)

    def __sub__(self, other):
        return self + (-self.cv(other))

    def __rsub__(self, other):
        return self.cv(other) - self

    def __mul__(self, other):
        o = self.cv(other)
        return Radical(self.p * o.p + self.q * o.q * self.d,
                       self.p * o.q + self.q * o.p, self.d)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Q(other)
        assert other
        return Radical(self.p / other, self.q / other, self.d)

    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        result = self.cv(1)
        for _ in range(n):
            result = result * self
        return result

    def sign(self):
        def sg(x):
            return (x > 0) - (x < 0)
        if not self.q:
            return sg(self.p)
        if not self.p or sg(self.p) == sg(self.q):
            return sg(self.q)
        return sg(self.p) * sg(self.p * self.p - self.q * self.q * self.d)


def nonnegative(x):
    return x.sign() >= 0 if isinstance(x, Radical) else x >= 0


def le(x, y):
    return nonnegative(y - x)


def approximate_core(a, delta):
    lo, hi = Q(0), Q(1)
    while hi - lo > delta:
        mid = (lo + hi) / 2
        if le(mid, a):
            lo = mid
        else:
            hi = mid
    b = (lo + hi) / 2
    assert le((b - a) ** 2, delta ** 2)
    assert b.denominator & (b.denominator - 1) == 0
    return b


def norm_squared(x):
    return sum(t * t for t in x)


counts = dict(radical_noise_fixtures=0, rational_row_checks=0,
              lifted_fourth_root_bounds=0, canonical_completions=0,
              tangent_gap_certificates=0, perturbation_budgets=0,
              tie_selector_checks=0, affine_rank_zero_checks=0,
              max_core_denominator_bits=0)
alpha, beta, sigma = Q(2), Q(3), Q(1, 8)
m, R0, B0, M = 3, Q(2), Q(5), Q(8)
lambda0 = Q(1, 64)
Cperp = 108 * R0 ** 2 * B0 * M / lambda0 ** 2
N = beta + sigma
Cres = 3 + 2 * N + M * (1 + B0 * R0) * Cperp
# x=(v,z,w,t), t=v+z; reduced center=(1/2,1/2,-1/2,1).
# H0=[[6,-2,0],[-2,2,0],[0,0,0]], g0=(1,0,0), E=(1,0,0).
# The affine lift's entrywise one-norm is 5; all cleared rows <=6.
Gamma = 5 * (m * 6) ** (m - 1) * Cres
Rx = Q(5)

for c in (Q(-1, 8), Q(0), Q(1, 8)):
    ell = Q(1, 4) + c
    a = Radical(Q(1, 3), Q(1, 3), 1 + 3 * ell)
    assert (3 * a ** 2 - 2 * a - ell).sign() == 0
    assert le(Q(2, 3), a) and le(a, 1)
    fstar = a ** 3 - a ** 2 - ell * a
    counts['radical_noise_fixtures'] += 1
    for v in (Q(0), Q(1, 4), Q(1, 2), Q(3, 4), Q(1)):
        for z in (Q(0), Q(1, 3), Q(2, 3), Q(1)):
            f = z ** 2 - 2 * v * z + v ** 3 - ell * v
            delta = f - fstar + beta * (v - a) ** 2 / 2
            assert nonnegative(f - fstar)
            assert le(beta * (v - a) ** 2 / 2, delta)
            d1, d2 = v - a, z - a
            # Rational equality residual and physical distance to the fiber.
            residual2 = (6 * d1 - 2 * d2) ** 2 + (-2 * d1 + 2 * d2) ** 2
            residual2 += d1 ** 2 + d1 ** 2
            counts['rational_row_checks'] += 1
            if le(delta, 1):
                assert le(residual2 ** 2, Cres ** 4 * delta)
                physical_distance2 = d1 ** 2 + d2 ** 2 + (d1 + d2) ** 2
                assert le(physical_distance2 ** 2, Gamma ** 4 * delta)
                counts['lifted_fourth_root_bounds'] += 1
    for q in (0, 4, 12):
        eps = Q(1, 2 ** q)
        tau = eps ** 6 / (1024 * Rx ** 4 * Gamma ** 4)
        eta = tau * eps ** 2 / 8
        delta_core = tau * eps ** 2 / (32 * beta)
        b = approximate_core(a, delta_core)
        counts['max_core_denominator_bits'] = max(
            counts['max_core_denominator_bits'], b.denominator.bit_length())
        assert eta + 2 * beta * delta_core <= tau * eps ** 2 / 4
        assert 2 * Rx * tau * Gamma ** 4 <= (eps ** 2 / (8 * Rx)) ** 3
        counts['perturbation_budgets'] += 1
        # Eliminate z from the strictly convex rational completion. w=0.
        rho = (1 - tau) / (1 + 2 * tau)
        linear = beta + 4 * tau - 2 * (1 - tau) * rho
        constant = ell + beta * b
        derivative = lambda v: 3 * v * v + linear * v - constant
        lo, hi = Q(0), Q(1)
        assert derivative(lo) < 0 < derivative(hi)
        while True:
            v = (lo + hi) / 2
            dv = derivative(v)
            if abs(dv) <= eta:
                break
            if dv < 0:
                lo = v
            else:
                hi = v
        z, w, t = rho * v, Q(0), (1 + rho) * v
        assert 0 <= v <= 1 and 0 <= z <= 1 and -2 <= w <= 1
        assert t == v + z
        # In the reduced box, gradient=(dv,0,0). The exact tangent-LP
        # gap is dv*v for dv>=0, and (-dv)*(1-v) otherwise.
        tangent_gap = dv * v if dv >= 0 else -dv * (1 - v)
        assert 0 <= tangent_gap <= abs(dv) <= eta
        counts['tangent_gap_certificates'] += 1
        point_error2 = (v - a) ** 2 + (z - a) ** 2 + (t - 2 * a) ** 2
        assert le(point_error2, eps ** 2)
        # The target's flat coordinate is fixed by the ORIGINAL norm.
        assert w == 0
        counts['canonical_completions'] += 1

# Tied core: F(v)=v(1-v), alpha=2, beta=3. The original minima are
# v=0,1; a=0 is selected. T_a=v+v^2/2 selects only v=0.
for v in (Q(0), Q(1, 5), Q(1, 2), Q(4, 5), Q(1)):
    f = v * (1 - v)
    target = f + Q(3, 2) * v * v
    assert target == v + v * v / 2
    assert target >= 0 and (target == 0) == (v == 0)
    counts['tie_selector_checks'] += 1

# Rank-zero reduced Hessian: original core is fixed, and the remaining
# objective is affine z on {z>=0,w>=0,z+w<=1}. Equality row g0=(1,0)
# describes its entire optimal edge; the min-norm point is the origin.
for z in (Q(0), Q(1, 4), Q(1, 2), Q(1)):
    for w in (Q(0), (1 - z) / 2, 1 - z):
        assert z >= 0 and w >= 0 and z + w <= 1
        distance_to_edge = z
        assert distance_to_edge ** 4 <= z
        counts['affine_rank_zero_checks'] += 1

result = {'status': 'pass', 'arithmetic': 'exact rational and quadratic-radical',
          'scope': 'composition fixtures; no general core/GLS oracle implementation',
          **counts}
path = Path(__file__).with_name('cubic-core-completion-results.json')
path.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
