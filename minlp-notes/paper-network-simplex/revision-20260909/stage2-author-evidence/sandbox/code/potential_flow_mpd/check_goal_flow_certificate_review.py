"""Independent exact review of goal certificates; also run with python -O.

Physical solutions are constructed from rational potentials and edge laws.
The one-cycle Hessian factor is checked against a separate scalar calculation.
No optional packages or optimizer statuses are used.
"""
from dataclasses import replace
from fractions import Fraction as F
from copy import deepcopy

from envelope_rational_certificates import make_certificate
from goal_flow_certificate import (
    HessianCertificate, SupportCertificate, make_hessian, make_support,
    optimal_goal_potentials, verify_hessian, verify_support,
)


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def rejects(fn, message):
    try:
        fn()
    except ValueError:
        return
    raise RuntimeError(message)


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), F(0))


def independent_energy(q, cp, cm):
    return sum((a*x*x*x/3 if x >= 0 else -b*x*x*x/3
                for x, a, b in zip(q, cp, cm)), F(0))


def integration_review():
    import certified_envelope as pipeline
    edges = [[0, 1], [1, 2], [0, 2]]
    b, c = [F(2), F(0), F(-2)], [F(1), F(1), F(2)]
    eps = F(1, 10000)
    y = [1+eps, 1+eps, 1-eps]
    base = make_certificate(edges, b, c, c, y, [F(2), F(1), F(0)])
    instance = dict(edges=edges, b=list(map(str, b)), target=0, sense='max',
                    resistances=[{'values': [str(v)]} for v in c])
    payload = dict(version=1, instance=instance, envelope=pipeline.encode_certificate(base),
                   scenario=dict(resistances=list(map(str, c)),
                                 certificate=pipeline.encode_certificate(base)))
    old = pipeline.verify(payload)
    witness = pipeline.encode_goal(pipeline.target_goal(edges, b, c, c, base, 0))
    original_goal = pipeline.target_goal(edges, b, c, c, base, 0)
    for flow_scale, coefficient_scale in [(F(1, 10**30), F(10**40)),
                                           (F(10**15), F(1, 10**20))]:
        energy_scale = coefficient_scale*flow_scale**3
        scaled_base = replace(base,
                              flow=[flow_scale*x for x in base.flow],
                              potentials=[coefficient_scale*flow_scale**2*x
                                          for x in base.potentials],
                              root_upper=[energy_scale*x for x in base.root_upper],
                              gap=energy_scale*base.gap, radius=flow_scale*base.radius)
        scaled_b = [flow_scale*x for x in b]
        scaled_c = [coefficient_scale*x for x in c]
        scaled_goal = pipeline.target_goal(edges, scaled_b, scaled_c, scaled_c,
                                           scaled_base, 0)
        check(scaled_goal.radius == flow_scale*original_goal.radius,
              'target radius lost exact scaling covariance')
        check(scaled_goal.factor == original_goal.factor/(coefficient_scale*flow_scale),
              'target factor scaling is wrong')
        check(scaled_goal.intervals == [(flow_scale*lo, flow_scale*hi)
                                       for lo, hi in original_goal.intervals],
              'target intervals lost exact scaling covariance')
    payload['goal_bounds'] = dict(envelope=witness, scenario=deepcopy(witness))
    report = pipeline.verify(payload)
    for name in ['optimum_interval', 'scenario_interval']:
        lo, hi = report[name]
        check(lo <= 1 <= hi, 'integrated physical goal enclosure')
        check(old[name][0] <= lo <= hi <= old[name][1], 'intersection widened interval')
        check(hi-lo < old[name][1]-old[name][0], 'expected fixture improvement absent')
    bad_paths = [(['goal_bounds'], None),
                 (['goal_bounds', 'envelope', 'factor'], '-1'),
                 (['goal_bounds', 'envelope', 'radius'], '0'),
                 (['goal_bounds', 'scenario', 'radius'], '0'),
                 (['goal_bounds', 'envelope', 'intervals'], []),
                 (['goal_bounds', 'scenario', 'potentials'], []),
                 (['goal_bounds', 'envelope', 'radius'], 1.0),
                 (['goal_bounds', 'envelope', 'intervals', 0], ['0']),
                 (['goal_bounds', 'scenario', 'extra'], 'unsupported')]
    for path, value in bad_paths:
        bad = deepcopy(payload)
        dest = bad
        for key in path[:-1]:
            dest = dest[key]
        dest[path[-1]] = value
        rejects(lambda bad=bad: pipeline.verify(bad), 'malformed integrated goal accepted')
    # A valid zero-radius cut-goal witness must not be accepted as an edge goal.
    cut = make_hessian(edges, b, c, c, base, [F(1), F(1), F(2)])
    bad = deepcopy(payload)
    bad['goal_bounds']['envelope'] = pipeline.encode_goal(cut)
    rejects(lambda: pipeline.verify(bad), 'pipeline trusted an unrelated goal witness')
    # Null witnesses intentionally retain the original Bregman-only format.
    payload['goal_bounds'] = dict(envelope=None, scenario=None)
    check(pipeline.verify(payload)['optimum_interval'] == old['optimum_interval'],
          'explicit null fallback changed bound')
    zero_b = [F(0)]*3
    zero_c = [F(1)]*3
    circulation = [eps, eps, -eps]
    zero_base = make_certificate(edges, zero_b, zero_c, zero_c, circulation, zero_b)
    check(pipeline.target_goal(edges, zero_b, zero_c, zero_c, zero_base, 0) is None,
          'known zero-curvature obstruction did not yield documented fallback')
    print('Pipeline integration passed: 10 malformed goal witnesses rejected, '
          'both physical intervals improved, reconstructed goal and null fallback checked.')


def run():
    cases = samples = rejected = 0
    edges = [(0, 1), (1, 2), (0, 2)]
    cycle = [F(1), F(1), F(-1)]
    # Last case exercises a genuine zero-flow edge and a solvable constrained
    # Laplacian, rather than the special zero-gap exit.
    physical_cases = [
        ([F(1), F(1), F(1)], [F(2), F(1), F(0)],
         [F(1), F(1), F(2)], [F(7), F(5), F(3)]),
        ([F(-1), F(-1), F(-1)], [F(-2), F(-1), F(0)],
         [F(7), F(5), F(3)], [F(1), F(1), F(2)]),
        ([F(0), F(1), F(1)], [F(1), F(1), F(0)],
         [F(2), F(1), F(1)], [F(5), F(7), F(11)]),
    ]
    goals = [[F(1), F(0), F(0)], [F(2), F(-3), F(4)],
             [F(1), F(1), F(2)]]  # Third goal is a cut: exactly fixed.
    eps = F(1, 10000)
    for exact, physical_p, cp, cm in physical_cases:
        b = [exact[0]+exact[2], exact[1]-exact[0], -exact[1]-exact[2]]
        for e, (u, v) in enumerate(edges):
            q = exact[e]
            drop = (cp[e] if q >= 0 else cm[e])*q*abs(q)
            check(drop == physical_p[u]-physical_p[v], 'constructed physical law')
        y = [q+eps*c for q, c in zip(exact, cycle)]
        base = make_certificate(edges, b, cp, cm, y, physical_p)
        check(base.gap > 0, 'nonzero-gap review case')
        for w in goals:
            hc = make_hessian(edges, b, cp, cm, base, w)
            check(abs(dot(w, [q-v for q, v in zip(exact, y)])) <= hc.radius,
                  'physical goal outside Hessian interval')
            # On a one-cycle graph any conserved error is t*cycle. Thus the
            # optimal quadratic dual factor is (w.cycle)^2 / sum_e h_e.
            hs = []
            for (lo, hi), a, bb in zip(hc.intervals, cp, cm):
                hs.append(2*a*lo if lo > 0 else -2*bb*hi if hi < 0 else F(0))
            independent_factor = dot(w, cycle)**2/sum(hs)
            check(hc.factor == independent_factor, 'wrong one-cycle factor')
            if all(h > 0 for h in hs):
                loose_factor = sum((we*we/he for we, he in zip(w, hs)), F(0))
                loose_radius = 1+2*base.gap*loose_factor
                loose = HessianCertificate(hc.intervals, [F(0)]*3,
                                           loose_factor, loose_radius)
                check(verify_hessian(edges, b, cp, cm, base, w, loose),
                      'valid nonoptimal Hessian witness rejected')
            shifted = replace(hc, potentials=[p+F(7, 11) for p in hc.potentials])
            check(verify_hessian(edges, b, cp, cm, base, w, shifted), 'gauge rejection')
            for direction in [F(1), F(-1)]:
                wd = [direction*v for v in w]
                sc = make_support(edges, b, cp, cm, y, wd, F(2, 3), physical_p)
                check(dot(wd, exact) <= sc.upper, 'physical goal outside support')
                for k in range(-20, 21):
                    q = [x+F(k, 20)*eps*c for x, c in zip(exact, cycle)]
                    if independent_energy(q, cp, cm) <= independent_energy(y, cp, cm):
                        check(dot(wd, q) <= sc.upper, 'energy sublevel not enclosed')
                        samples += 1
                bads = [replace(sc, upper=sc.upper-F(1)),
                        replace(sc, multiplier=F(-1)),
                        replace(sc, potentials=sc.potentials[:-1]),
                        replace(sc, root_upper=[F(-1)]*3),
                        replace(sc, upper=float(sc.upper))]
                if any(sc.root_upper):
                    bads.append(replace(sc, root_upper=[F(0)]*3))
                for bad in bads:
                    rejects(lambda bad=bad: verify_support(edges, b, cp, cm, y, wd, bad),
                            'accepted corrupted support')
                    rejected += 1
            bads = [replace(hc, factor=hc.factor+1),
                    replace(hc, radius=F(-1)),
                    replace(hc, potentials=hc.potentials[:-1]),
                    replace(hc, intervals=[(y[0], y[0])]+hc.intervals[1:]),
                    replace(hc, factor=float(hc.factor))]
            if hc.factor:
                bads.append(replace(hc, radius=F(0)))
            for bad in bads:
                rejects(lambda bad=bad: verify_hessian(edges, b, cp, cm, base, w, bad),
                        'accepted corrupted Hessian certificate')
                rejected += 1
            cases += 1

    # All curvatures zero: cut goals are exact despite a positive energy gap;
    # a genuine cycle goal has no finite bound from this quadratic modulus.
    exact = [F(0)]*3
    b = [F(0)]*3
    cp = cm = [F(1)]*3
    y = [eps*c for c in cycle]
    base = make_certificate(edges, b, cp, cm, y, [F(0)]*3)
    cut = [F(1), F(1), F(2)]
    hc = make_hessian(edges, b, cp, cm, base, cut)
    check(hc.radius == hc.factor == 0 and base.gap > 0, 'zero-curvature cut goal')
    sc = make_support(edges, b, cp, cm, y, cut, 0, [2, 1, 0])
    check(sc.upper == 0, 'zero-multiplier exact cut bound')
    cycle_goal = [F(1), F(0), F(0)]
    rejects(lambda: make_hessian(edges, b, cp, cm, base, cycle_goal),
            'zero-curvature cycle producer did not reject')
    rejects(lambda: verify_hessian(edges, b, cp, cm, base, cycle_goal, hc),
            'zero-curvature residual not checked')
    rejects(lambda: verify_support(edges, b, cp, cm, y, cycle_goal,
                                   SupportCertificate(F(0), [F(0)]*3, [], F(0))),
            'zero multiplier noncut accepted')
    rejected += 3

    # Exact minimizers do not need a nondegenerate Hessian, even for cycle goals.
    exact_base = make_certificate(edges, b, cp, cm, exact, [F(0)]*3)
    exact_hc = make_hessian(edges, b, cp, cm, exact_base, cycle_goal)
    check(exact_hc.radius == exact_hc.factor == 0, 'zero-gap noncut exact goal')
    rejects(lambda: verify_hessian(edges, b, cp, cm,
                                   replace(exact_base, gap=F(1)), cycle_goal, exact_hc),
            'base certificate was not independently rechecked')
    rejected += 1

    # Disconnected components, an isolated node, parallel edges, and independent
    # component gauges are legitimate for the exact certificate checker.
    edges2 = [(0, 1), (0, 1), (2, 3)]
    b2 = [F(2), F(-2), F(0), F(0), F(0)]
    y2 = [1+eps, 1-eps, F(0)]
    p2 = [F(1), F(0), F(0), F(0), F(0)]
    c2 = [F(1)]*3
    base2 = make_certificate(edges2, b2, c2, c2, y2, p2)
    for w2 in [[F(1), F(0), F(0)], [F(0), F(0), F(1)]]:
        h2 = make_hessian(edges2, b2, c2, c2, base2, w2)
        pshift = [v+(F(7) if i < 2 else F(-9) if i < 4 else F(100))
                  for i, v in enumerate(h2.potentials)]
        check(verify_hessian(edges2, b2, c2, c2, base2, w2,
                             replace(h2, potentials=pshift)), 'disconnected gauge')
        check(abs(dot(w2, [F(1)-y2[0], F(1)-y2[1], F(0)])) <= h2.radius,
              'disconnected physical goal')
        if w2[-1]:
            check(h2.radius == 0, 'zero-flow bridge should be fixed')
    # The constrained solve may have multiple zero-edge multipliers, besides
    # gauge freedom. Redundant consistent constraints must still be accepted.
    p = optimal_goal_potentials(edges, 4, cut, [F(0)]*3)
    check(all(p[u]-p[v] == w for (u, v), w in zip(edges, cut)),
          'redundant zero-edge constraints')
    print(f'Independent review passed: {cases} asymmetric/zero-edge goal cases, '
          f'{samples} conserved sublevel samples, {rejected} malformed witnesses, '
          'zero-curvature cuts/cycles, parallel edges, disconnected gauges.')


if __name__ == '__main__':
    run()
    integration_review()
