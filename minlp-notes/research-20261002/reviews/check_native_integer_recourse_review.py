#!/usr/bin/env python3
"""Exact reviewer diagnostics for the uniform integer-label certificate."""

from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path


def main():
    labels = [z for z in product(range(5), repeat=3)
              if z[0]+z[1]+2*z[2] == 4 and z[0] >= z[2]]
    assert len(labels) > 1
    coupling = [Q(3, 2), Q(-1), Q(1, 2)]
    weights = [Q(1, 3), Q(1, 5), Q(1, 7)]
    counts = {'gap_tests': 0, 'restricted_calls': 0,
              'accepted_uniform_labels': 0, 'endpoint_comparisons': 0}
    for residual_noise in product([Q(-1, 2), Q(0), Q(1, 2)], repeat=3):
        for core_noise in [Q(-1, 3), Q(0), Q(1, 3)]:
            def value(v, z):
                return (v**4-v*v+core_noise*v
                        +sum(weight*(zi-1)**2+noise*zi+v*b*zi
                             for weight, noise, b, zi in
                             zip(weights, residual_noise, coupling, z)))
            # A monomial derivative bound, valid uniformly on v in [0,1].
            G = 6+max(abs(core_noise+sum(b*zi for b, zi in zip(coupling, z)))
                      for z in labels)
            for center in [Q(0), Q(1, 4), Q(1, 2), Q(3, 4), Q(1)]:
                costs = {z: value(center, z) for z in labels}
                chosen = min(labels, key=lambda z: (costs[z], z))
                base = costs[chosen]
                excluded_union = set()
                excluded_values = []
                for i in range(3):
                    for direction in [-1, 1]:
                        restricted = [z for z in labels
                                      if direction*(z[i]-chosen[i]) >= 1]
                        excluded_union.update(restricted)
                        if restricted:
                            excluded_values.append(min(costs[z] for z in restricted))
                        counts['restricted_calls'] += 1
                assert excluded_union == set(labels)-{chosen}
                other = min(excluded_values)
                assert other == min(costs[z] for z in labels if z != chosen)
                for radius in [Q(1, 4), Q(1, 32), Q(1, 512)]:
                    lo, hi = max(Q(0), center-radius), min(Q(1), center+radius)
                    width = hi-lo
                    counts['gap_tests'] += 1
                    if other-base <= 2*G*width:
                        continue
                    counts['accepted_uniform_labels'] += 1
                    for z in labels:
                        if z == chosen:
                            continue
                        # The common quartic core term cancels. Every label
                        # gap is affine in v, so endpoint positivity proves
                        # positivity on the entire continuum [lo,hi].
                        for endpoint in [lo, hi]:
                            gap = value(endpoint, z)-value(endpoint, chosen)
                            assert gap >= other-base-2*G*width > 0
                            counts['endpoint_comparisons'] += 1
    assert counts['accepted_uniform_labels'] > 0

    # Strictness matters at the exact threshold, not just at zero-width hulls.
    # F(v,z)=(1-2z)v+z/2, z in {0,1}, v in [0,1/4], G=1.
    width = Q(1, 4)
    def threshold_value(v, z):
        return (1-2*z)*v+Q(z, 2)
    threshold_gap = threshold_value(0, 1)-threshold_value(0, 0)
    assert threshold_gap == 2*width
    assert threshold_value(width, 0) == threshold_value(width, 1)

    # An excluded feasible upper value can certify a false winner.
    # At c=0 the true excluded winner is label 1, but returning label 2
    # as an upper witness hides the crossover inside the core hull.
    def bad_upper_value(v, z):
        return 50*z*(z-1)+z*(2-z)*(Q(1, 1000)-v)
    center, endpoint, G = Q(0), Q(1, 100), Q(1)
    chosen_value = bad_upper_value(center, 0)
    true_other = min(bad_upper_value(center, z) for z in [1, 2])
    false_upper = bad_upper_value(center, 2)
    assert true_other-chosen_value <= 2*G*endpoint < false_upper-chosen_value
    assert bad_upper_value(endpoint, 1) < bad_upper_value(endpoint, 0)

    # Base-only precision arithmetic at widely separated native widths.
    # No labels are enumerated in these budget fixtures.
    budgets = []
    for width_bits in [1, 23, 200]:
        native_width = 2**width_bits
        k, n, L, sigma = 1, 2, Q(10), Q(1, 8)
        S = 1+native_width
        K = 9*(native_width+1)
        B = 2**(3*width_bits+10)
        C_tail = 2**(2*width_bits+5)
        G, M1, T = Q(1+native_width**3), Q(15), Q(24)
        rho = Q(1, 4*B)
        g0, tau = rho*sigma/(2*S), rho*sigma/(2*K)
        A0 = 2+k*L/g0
        label_cutoff = min(1/(4*A0), g0/(16*G*A0))
        label_h, label_J = Q(1), 0
        while label_h > label_cutoff:
            label_h /= 2
            label_J += 1
        assert k*L*label_h**2/8 <= g0/8
        assert 4*G*A0*label_h <= g0/4
        label_minimum_M = max(2, 2**label_J, int(4*n*C_tail/rho))
        label_M = 1 << (label_minimum_M-1).bit_length()
        assert S*g0/sigma+Q(2*n*C_tail, label_M) <= rho
        cutoff = min(1/(4*A0), g0/(16*G*A0),
                     tau/(8*M1*A0), g0/(4*T*A0))
        h, J = Q(1), 0
        while h > cutoff:
            h /= 2
            J += 1
        minimum_M = max(2, 2**J, int(4*n*C_tail/rho), int(2*K/rho))
        M = 1 << (minimum_M-1).bit_length()
        error = k*L*h*h/8
        assert error <= g0/8
        assert g0-error >= 7*g0/8
        assert 4*G*A0*h <= g0/4
        assert 2*M1*A0*h < tau/2 and 2*T*A0*h <= g0/2
        assert S*g0/sigma+Q(2*n*C_tail, M) <= rho
        assert K*(tau/sigma+Q(1, M)) <= rho
        assert 2*rho*B == Q(1, 2)
        budgets.append({'native_width_bits': width_bits,
                        'label_only_cutoff_level': label_J,
                        'label_only_sampling_bits': label_M.bit_length()-1,
                        'cutoff_level': J, 'sampling_bits': M.bit_length()-1})

    # A successful label certificate permits a whole-core algebraic solve.
    # F(v,z)=v^4-v+(z-1)^2, v in [0,1], z in {0,1,2}.
    # The winner z=1 has a constant unit gap. The exact core minimizer
    # alpha is the unique positive root of 4alpha^3-1, and its value is
    # -3alpha/4, the unique real root of 256 value^3+27.
    assert Q(1) > 2*Q(3)*Q(1, 20)  # uniform-label certificate on a thin hull
    for candidate in [Q(sign, denominator)
                      for sign in [-1, 1] for denominator in [1, 2, 4]]:
        assert 4*candidate**3-1 != 0
    expanded_cases = 0
    for bits in [8, 32, 96]:
        lo, hi = Q(1, 2), Q(3, 4)
        while hi-lo > Q(1, 2**bits):
            mid = (lo+hi)/2
            if 4*mid**3-1 < 0:
                lo = mid
            else:
                hi = mid
        assert 4*lo**3-1 < 0 < 4*hi**3-1
        value_lo, value_hi = -3*hi/4, -3*lo/4
        assert 256*value_lo**3+27 < 0 < 256*value_hi**3+27
        feasible_core = (lo+hi)/2
        rational_value = feasible_core**4-feasible_core
        assert rational_value-value_lo <= 3*(hi-lo)
        expanded_cases += 1

    report = {'status': 'passed', 'scope': 'finite exact reviewer diagnostics',
              'coupled_labels': len(labels), 'counts': counts,
              'strict_threshold_guard': True, 'excluded_upper_counterexample': True,
              'expanded_algebraic_refinements': expanded_cases,
              'budgets': budgets}
    Path(__file__).with_name('native-integer-recourse-review-results.json').write_text(
        json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
