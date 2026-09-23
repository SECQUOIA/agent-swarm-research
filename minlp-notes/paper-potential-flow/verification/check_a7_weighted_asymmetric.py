#!/usr/bin/env python3
"""S4b directional-coefficient checks; no varying-nomination optimizer.

Check original 2m-coordinate LPs against active-coefficient threshold
elimination, then use the reviewed symmetric block solver on separately
capacity-restricted sign panels. Independently solve the original asymmetric
cycle equation for sampled coefficient pairs, including sign crossings.
This is a test harness, not an extension of the public block solver API.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from random import Random
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'code/potential_flow_mpd'))
from check_reopened_joint_weighted_review import threshold_optimum
from exact_weighted_cactus import solve_cycle


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def original_lp(flows, weights, lp, up, lm, um):
    """Enumerate vertices in the ORIGINAL 2m-dimensional coefficient box."""
    a = [max(x, 0)**2 for x in flows] + [-min(x, 0)**2 for x in flows]
    w = weights + weights
    lower, upper = lp + lm, up + um
    if not any(a):
        return F(0)
    best = None
    for free in range(len(a)):
        if not a[free]:
            continue
        other = [i for i in range(len(a)) if i != free]
        for bits in product((0, 1), repeat=len(other)):
            theta = lower[:]
            for i, bit in zip(other, bits):
                theta[i] = upper[i] if bit else lower[i]
            theta[free] = -sum(a[i]*theta[i] for i in other)/a[free]
            if lower[free] <= theta[free] <= upper[free]:
                v = sum(wi*ai*ti for wi, ai, ti in zip(w, a, theta))
                best = v if best is None else max(best, v)
    return best


def directional_optimum(offsets, weights, lp, up, lm, um):
    cuts = sorted(set(-x for x in offsets))
    panels = list(zip(cuts, cuts[1:])) or [(cuts[0], cuts[0])]
    best = None
    for a, b in panels:
        middle = (a+b)/2
        lower = [lp[i] if middle+t >= 0 else lm[i] for i, t in enumerate(offsets)]
        upper = [up[i] if middle+t >= 0 else um[i] for i, t in enumerate(offsets)]
        found = solve_cycle(offsets, weights, lower, upper,
                            [a+t for t in offsets], [b+t for t in offsets])
        if found is None:
            continue
        if best is None or found['objective'] > best['objective']:
            best = found
    require(best is not None, 'Unfiltered directional cycle must be feasible')
    q = best['circulation']
    positive, negative = lp[:], lm[:]
    for i, t in enumerate(offsets):
        if q+t > 0:
            positive[i] = best['resistances'][i]
        elif q+t < 0:
            negative[i] = best['resistances'][i]
    require(all(lo <= x <= hi for lo, x, hi in zip(lp, positive, up)), 'Positive bounds')
    require(all(lo <= x <= hi for lo, x, hi in zip(lm, negative, um)), 'Negative bounds')
    drops = [(positive[i] if q+t >= 0 else -negative[i])*(q+t)*(q+t)
             for i, t in enumerate(offsets)]
    require(sum(drops) == 0, 'Original asymmetric conservation')
    require(sum(w*g for w, g in zip(weights, drops)) == best['objective'], 'Original objective')
    require(all(isinstance(x, F) for x in positive+negative), 'Rational original profile')
    return best


def state(offsets, positive, negative):
    lower, upper = -max(offsets), -min(offsets)
    for _ in range(90):
        q = (lower+upper)/2
        value = sum((positive[i] if q+t >= 0 else -negative[i])*(q+t)**2
                    for i, t in enumerate(offsets))
        if value > 0:
            upper = q
        else:
            lower = q
    q = (lower+upper)/2
    flows = [q+t for t in offsets]
    drops = [(positive[i] if x >= 0 else -negative[i])*x*x for i, x in enumerate(flows)]
    potential = [0.0]
    for g in drops[:-1]:
        potential.append(potential[-1]-g)
    return flows, potential, drops


def run():
    rng = Random(9412026)
    exact, feasible, sampled, sensitivity = 0, 0, 0, 0
    for case in range(120):
        n = 3 if case % 3 else 4
        flows = [F(rng.randint(-2, 2)) for _ in range(n)]
        if case == 0:
            flows = [F(0)]*n
        weights = [F(rng.randint(-2, 2)) for _ in range(n)]
        lp = [F(rng.randint(1, 3)) for _ in range(n)]
        lm = [F(rng.randint(1, 3)) for _ in range(n)]
        up = [v+rng.randint(0, 3) for v in lp]
        um = [v+rng.randint(0, 3) for v in lm]
        expected = original_lp(flows, weights, lp, up, lm, um)
        active_l = [lp[i] if x >= 0 else lm[i] for i, x in enumerate(flows)]
        active_u = [up[i] if x >= 0 else um[i] for i, x in enumerate(flows)]
        got = threshold_optimum([x*abs(x) for x in flows], weights, active_l, active_u)[0]
        require(got == expected, 'Original coefficient LP versus active threshold')
        exact += 1
        feasible += got is not None

    for case in range(32):
        n = 3 + case % 2
        offsets = [F(rng.randint(-3, 3)) for _ in range(n)]
        weights = [F(rng.randint(-3, 3)) for _ in range(n)]
        lp = [F(rng.randint(1, 3)) for _ in range(n)]
        lm = [F(rng.randint(1, 3)) for _ in range(n)]
        up = [v+rng.randint(0, 3) for v in lp]
        um = [v+rng.randint(0, 3) for v in lm]
        best = directional_optimum(offsets, weights, lp, up, lm, um)
        reverse = directional_optimum([-t for t in offsets], [-w for w in weights],
                                      lm, um, lp, up)
        require(best['objective'] == reverse['objective'], 'Reorientation swaps directional intervals')
        floats = [float(t) for t in offsets]
        lower, upper = lp+lm, up+um
        for _ in range(40):
            theta = [float(lo)+(float(hi-lo))*rng.random() for lo, hi in zip(lower, upper)]
            x, pi, drops = state(floats, theta[:n], theta[n:])
            value = sum(float(w)*g for w, g in zip(weights, drops))
            # Interval endpoint is certified by exact arithmetic in the reviewed solver.
            _, certified_upper = best['objective'].interval(45)
            require(value <= float(certified_upper)+1e-9, 'Independent physical sample exceeds optimum')
            sampled += 1
            other = [max(float(lo), min(float(hi), t+rng.uniform(-.01, .01)))
                     for lo, hi, t in zip(lower, upper, theta)]
            y, pj, _ = state(floats, other[:n], other[n:])
            b = [floats[i]-floats[i-1] for i in range(n)]
            B = max(1., sum(max(v, 0) for v in b))
            l1 = sum(abs(a-b) for a, b in zip(theta, other))
            delta = max(abs(a-b) for a, b in zip(theta, other))
            drop_changes = [a-b for a, b in zip(pi, pj)]
            require(max(drop_changes)-min(drop_changes) <= B*B*l1+1e-9,
                    'All terminal coefficient Lipschitz bounds')
            require(max(abs(a-b) for a, b in zip(x, y))**2 <=
                    2*B*B*(2*n+1)*delta/min(map(float, lower))+1e-9,
                    'Directional inverse-law flow bound')
            sensitivity += 1

    # Changing positive loss at the final edge reverses the middle flow.
    offsets = [-1., 0., 1.]
    x, pi, _ = state(offsets, [1., 1., 1.], [4., 1., 1.])
    y, pj, _ = state(offsets, [1., 1., 9.], [4., 1., 1.])
    require(x[1] > 0 > y[1], 'Explicit coefficient-induced sign crossing')
    changes = [a-b for a, b in zip(pi, pj)]
    require(max(changes)-min(changes) <= 4*8, 'Crossing terminal sensitivity')
    return dict(original_directional_lp_cases=exact, feasible_lp_cases=feasible,
                exact_directional_cycles=32, interval_swap_reorientations=32,
                independent_physical_profiles=sampled, joint_sensitivity_cases=sensitivity,
                explicit_sign_crossing=True)


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True))
